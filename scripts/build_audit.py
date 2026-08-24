#!/usr/bin/env python3
"""Build freeze manifests, ID diffs, Table 3 rescores, dataset stats."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import (  # noqa: E402
    SCORER_VERSION,
    extract_spans,
    index_by_id,
    load_records,
    rec_id,
    score,
    sha256_file,
    tags_to_spans,
    pick_tags,
    GOLD_FIELDS,
    PRED_FIELDS,
)

CANON = {
    "corpus_train": ROOT / "data/annotated/processed/chinese_skillspan/train.json",
    "corpus_dev": ROOT / "data/annotated/processed/chinese_skillspan/dev.json",
    "corpus_test": ROOT / "data/annotated/processed/chinese_skillspan/test.json",
    "bench_gold": ROOT / "chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl",
    "forbidden_prep_test": ROOT / "chinese_skillspan_preprocessing/data/annotated/processed/chinese_skillspan/test.json",
}

PREDS = {
    "ChatGPT": ROOT / "chinese_skillspan_preprocessing/output/dir/test-gpt/silver_gpt4o_sent_ner_test_1005_last_test.jsonl",
    "Claude": ROOT / "chinese_skillspan_preprocessing/output/dir/test_claude/merged_test_cluade.jsonl",
    "Kimi": ROOT / "chinese_skillspan_preprocessing/output/dir/test-kimi/merged_test_kimi.jsonl",
    "DeepSeek": ROOT / "chinese_skillspan_preprocessing/output/dir/test-deepseek/ds_test_.merged.jsonl",
    "Qwen": ROOT / "output/chinese_skillspan_qwen25-14b_test_all.jsonl",
    "JobBERT-skill": ROOT / "Baseline_Models_Collection/out_jobbert_skill_chinese_encoder_aligned.jsonl",
    "JobBERT-knowledge": ROOT / "Baseline_Models_Collection/out_jobbert_knowledge_chinese_encoder_skillaligned.jsonl",
}

BANNED_EVAL = [
    ROOT / "chinese_skillspan_preprocessing/output/dir/test-gpt/silver_gpt4o_sent_ner_test_1005_last_test.eval_ner.json",
    ROOT / "chinese_skillspan_preprocessing/output/dir/test_claude/merged_test_cluade.eval_ner.json",
    ROOT / "chinese_skillspan_preprocessing/output/dir/test-kimi/merged_test_kimi.eval_ner.json",
]


def has_esco(rec: dict) -> bool:
    blob = json.dumps(rec, ensure_ascii=False)
    keys = " ".join(rec.keys()).lower()
    if any(s in keys for s in ("esco_id", "concept_id", "esco_uri", "concepturi")):
        return True
    return "http://data.europa.eu/esco" in blob


def layer_status(name: str) -> str:
    if name.startswith("corpus_"):
        return "SILVER_OR_MIXED_IN_CORPUS_TREE"
    if name == "bench_gold":
        return "BENCHMARK_GOLD"
    if name == "forbidden_prep_test":
        return "UNLABELED_FORBIDDEN"
    return "PRED"


def file_row(name: str, path: Path) -> dict:
    exists = path.is_file()
    recs = load_records(str(path)) if exists else []
    ids = [rec_id(r) for r in recs] if recs else []
    uniq = set(ids)
    spans = []
    esco = 0
    label_fields = Counter()
    if recs:
        for r in recs:
            if has_esco(r):
                esco += 1
            for f in ("list_of_selection_bio4", "list_of_selection", "pred_tags", "tags_skill_clean"):
                if isinstance(r.get(f), list) and r.get(f):
                    label_fields[f] += 1
            try:
                spans.extend(extract_spans(r, GOLD_FIELDS if "pred" not in name.lower() else PRED_FIELDS))
            except Exception:
                pass
    types = Counter(t for *_, t in spans)
    return {
        "name": name,
        "path": str(path.resolve()) if exists else str(path),
        "exists": exists,
        "sha256": sha256_file(str(path)) if exists else "",
        "bytes": path.stat().st_size if exists else 0,
        "n_rows": len(recs),
        "n_unique_ids": len(uniq),
        "n_duplicate_ids": sum(1 for c in Counter(ids).values() if c > 1),
        "layer": layer_status(name),
        "label_fields": "|".join(f"{k}:{v}" for k, v in label_fields.most_common()),
        "n_lskt_spans": sum(types[t] for t in "LKST"),
        "n_skill_spans": types.get("SKILL", 0) + sum(types[t] for t in "LKST"),
        "spans_L": types.get("L", 0),
        "spans_K": types.get("K", 0),
        "spans_S": types.get("S", 0),
        "spans_T": types.get("T", 0),
        "n_rows_with_esco_id": esco,
        "has_esco_concept_id": esco > 0,
    }


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def split_stats(name: str, path: Path) -> dict:
    recs = load_records(str(path))
    lens = []
    span_lens = []
    types = Counter()
    domains = Counter()
    empty = 0
    texts = []
    ids = []
    for r in recs:
        ids.append(rec_id(r))
        sent = r.get("sentence") or r.get("text") or ""
        texts.append(sent)
        lens.append(len(sent))
        domains[r.get("source_domain") or r.get("title") and "has_title" or "?"] += 1
        domains  # keep
        sp = extract_spans(r, GOLD_FIELDS)
        if not sp:
            empty += 1
        for a, b, t in sp:
            types[t] += 1
            span_lens.append(b - a)
    n = len(recs)
    return {
        "split": name,
        "n_rows": n,
        "n_unique_ids": len(set(ids)),
        "avg_chars": (sum(lens) / n) if n else 0,
        "n_spans_total": sum(types.values()),
        "avg_4d": (sum(types.values()) / n) if n else 0,
        "L": types.get("L", 0),
        "K": types.get("K", 0),
        "S": types.get("S", 0),
        "T": types.get("T", 0),
        "avg_L": types.get("L", 0) / n if n else 0,
        "avg_K": types.get("K", 0) / n if n else 0,
        "avg_S": types.get("S", 0) / n if n else 0,
        "avg_T": types.get("T", 0) / n if n else 0,
        "frac_no_skill": empty / n if n else 0,
        "mean_span_tokens": (sum(span_lens) / len(span_lens)) if span_lens else 0,
        "source_domain": dict(Counter(r.get("source_domain") for r in recs)),
        "has_year_field": any("year" in r or "date" in r for r in recs[:20]),
        "unique_esco_concepts": 0,
        "ids": ids,
        "texts": texts,
    }


def exact_dups(splits: dict[str, dict]) -> list[dict]:
    seen: dict[str, list[str]] = defaultdict(list)
    rows = []
    for name, st in splits.items():
        for i, text in zip(st["ids"], st["texts"]):
            key = " ".join((text or "").split())
            if not key:
                continue
            seen[key].append(f"{name}:{i}")
    for text, locs in seen.items():
        splits_hit = {x.split(":")[0] for x in locs}
        if len(locs) > 1:
            rows.append({
                "n": len(locs),
                "cross_split": int(len(splits_hit) > 1),
                "locations": "|".join(locs[:12]),
                "text_preview": text[:120],
            })
    return rows


def main() -> int:
    reports = PAPER / "reports"
    manifests = PAPER / "manifests"
    reports.mkdir(exist_ok=True)
    manifests.mkdir(exist_ok=True)

    man_rows = [file_row(k, p) for k, p in CANON.items()]
    for k, p in PREDS.items():
        man_rows.append(file_row(f"pred_{k}", p))
    for i, p in enumerate(BANNED_EVAL):
        row = file_row(f"BANNED_eval_ner_{i}", p)
        row["layer"] = "BANNED_WRONG_GOLD_EVAL"
        man_rows.append(row)

    fields = [
        "name", "path", "exists", "sha256", "bytes", "n_rows", "n_unique_ids",
        "n_duplicate_ids", "layer", "label_fields", "n_lskt_spans", "n_skill_spans",
        "spans_L", "spans_K", "spans_S", "spans_T", "n_rows_with_esco_id",
        "has_esco_concept_id",
    ]
    write_csv(manifests / "data_pred_manifest.csv", man_rows, fields)
    (manifests / "data_pred_manifest.json").write_text(
        json.dumps(man_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    test = load_records(str(CANON["corpus_test"]))
    gold = load_records(str(CANON["bench_gold"]))
    test_map, test_info = index_by_id(test, "first")
    gold_map, gold_info = index_by_id(gold, "first")
    test_ids, gold_ids = set(test_map), set(gold_map)

    miss_rows = []
    for i in sorted(test_ids - gold_ids):
        r = test_map[i]
        miss_rows.append({
            "set": "test_not_in_gold",
            "id": i,
            "global_id": r.get("global_id", ""),
            "source_domain": r.get("source_domain", ""),
            "model": "",
            "empty_gold_span": "",
        })
    for i in sorted(gold_ids - test_ids):
        r = gold_map[i]
        miss_rows.append({
            "set": "gold_not_in_test",
            "id": i,
            "global_id": r.get("global_id", ""),
            "source_domain": r.get("source_domain", ""),
            "model": "",
            "empty_gold_span": int(not extract_spans(r, GOLD_FIELDS)),
        })
    gold_counts = Counter(rec_id(r) for r in gold)
    for i, c in sorted(gold_counts.items()):
        if c > 1:
            r = gold_map[i]
            miss_rows.append({
                "set": "gold_duplicate_id",
                "id": i,
                "global_id": r.get("global_id", ""),
                "source_domain": r.get("source_domain", ""),
                "model": "",
                "empty_gold_span": c,
            })
    for r in gold:
        if not extract_spans(r, GOLD_FIELDS):
            miss_rows.append({
                "set": "gold_empty_span",
                "id": rec_id(r),
                "global_id": r.get("global_id", ""),
                "source_domain": r.get("source_domain", ""),
                "model": "",
                "empty_gold_span": 1,
            })

    for model, path in PREDS.items():
        if not path.is_file():
            continue
        rows = load_records(str(path))
        pmap, pinfo = index_by_id(rows, "first")
        pids = set(pmap)
        for i in sorted(gold_ids - pids):
            r = gold_map[i]
            miss_rows.append({
                "set": "pred_missing_gold",
                "id": i,
                "global_id": r.get("global_id", ""),
                "source_domain": r.get("source_domain", ""),
                "model": model,
                "empty_gold_span": "",
            })
        for i in sorted(pids - gold_ids):
            r = pmap[i]
            miss_rows.append({
                "set": "pred_extra_not_in_gold",
                "id": i,
                "global_id": r.get("global_id", ""),
                "source_domain": r.get("source_domain", ""),
                "model": model,
                "empty_gold_span": "",
            })
        pc = Counter(rec_id(r) for r in rows)
        for i, c in pc.items():
            if c > 1:
                miss_rows.append({
                    "set": "pred_duplicate_id",
                    "id": i,
                    "global_id": "",
                    "source_domain": "",
                    "model": model,
                    "empty_gold_span": c,
                })

    write_csv(
        reports / "missing_ids.csv",
        miss_rows,
        ["set", "id", "global_id", "source_domain", "model", "empty_gold_span"],
    )

    id_summary = {
        "test_rows": len(test),
        "test_unique_ids": len(test_ids),
        "gold_rows": len(gold),
        "gold_unique_ids": len(gold_ids),
        "gold_duplicate_ids": gold_info["n_duplicate_ids"],
        "gold_subset_of_test": gold_ids <= test_ids,
        "n_test_not_in_gold": len(test_ids - gold_ids),
        "n_gold_not_in_test": len(gold_ids - test_ids),
        "test_not_in_gold_by_domain": dict(Counter(test_map[i].get("source_domain") for i in test_ids - gold_ids)),
        "verdict": (
            "2676 is a row count, not 2676 unique sentences. Unique Gold IDs = 2601, "
            "all contained in the 3237-sentence test. 636 test IDs have no Gold row. "
            "Gold also repeats 75 extra rows (duplicate IDs). Do not merge the two sets."
        ),
    }
    (reports / "gold_vs_test_summary.json").write_text(
        json.dumps(id_summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    paper_f1 = {
        "ChatGPT": 0.6700,
        "Claude": 0.6300,
        "Kimi": 0.5700,
        "DeepSeek": 0.5130,
        "Qwen": 0.2130,
        "JobBERT-skill": 0.0045,
        "JobBERT-knowledge": 0.0038,
    }
    table3 = []
    for model, path in PREDS.items():
        if not path.is_file():
            table3.append({"model": model, "status": "MISSING_DUMP"})
            continue
        extra_fields = None
        if model.startswith("JobBERT"):
            extra_fields = ("pred_tags",)
        official = score(str(CANON["bench_gold"]), str(path), align_mode="official",
                         pred_fields=extra_fields or PRED_FIELDS, n_boot=200)
        legacy = score(str(CANON["bench_gold"]), str(path), align_mode="legacy",
                       pred_fields=extra_fields or PRED_FIELDS, n_boot=200)
        le = legacy.get("collapsed_exact") or {}
        te = legacy.get("typed_exact") or {}
        table3.append({
            "model": model,
            "paper_s_f1": paper_f1.get(model, ""),
            "legacy_alignment_ok": int(legacy.get("alignment_ok") or 0),
            "official_alignment_ok": int(official.get("alignment_ok") or 0),
            "official_error": official.get("error", ""),
            "pred_rows": legacy.get("pred", {}).get("n_rows", ""),
            "pred_unique_ids": legacy.get("pred", {}).get("n_unique_ids", ""),
            "n_missing_gold": legacy.get("id_sets", {}).get("n_missing_in_pred", ""),
            "n_extra_pred": legacy.get("id_sets", {}).get("n_extra_in_pred", ""),
            "n_scored_legacy": legacy.get("id_sets", {}).get("n_scored", ""),
            "typed_exact_f1": te.get("f1", ""),
            "typed_exact_p": te.get("precision", ""),
            "typed_exact_r": te.get("recall", ""),
            "collapsed_exact_f1": le.get("f1", ""),
            "collapsed_exact_p": le.get("precision", ""),
            "collapsed_exact_r": le.get("recall", ""),
            "typed_relaxed_f1": (legacy.get("typed_relaxed") or {}).get("f1", ""),
            "collapsed_relaxed_f1": (legacy.get("collapsed_relaxed") or {}).get("f1", ""),
            "delta_collapsed_vs_paper": (le.get("f1", 0) - paper_f1[model]) if model in paper_f1 else "",
            "gold_sha256": legacy.get("gold_sha256", ""),
            "pred_sha256": legacy.get("pred_sha256", ""),
            "scorer_version": SCORER_VERSION,
            "action": (
                "REUSE_DUMP_RESCORE_ONLY" if model in {"ChatGPT", "DeepSeek", "JobBERT-skill", "JobBERT-knowledge"}
                else "FILL_MISSING_GOLD_IDS_ONLY" if model in {"Claude", "Kimi"}
                else "PROVENANCE_THEN_RERUN_DECLARED_CONFIG"
            ),
        })
        (reports / f"score_{model.replace(' ', '_')}_legacy.json").write_text(
            json.dumps(legacy, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (reports / f"score_{model.replace(' ', '_')}_official.json").write_text(
            json.dumps(official, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    t3_fields = list(table3[0].keys()) if table3 else []
    write_csv(reports / "table3_reproduction.csv", table3, t3_fields)

    splits = {
        "train": split_stats("train", CANON["corpus_train"]),
        "dev": split_stats("dev", CANON["corpus_dev"]),
        "test": split_stats("test", CANON["corpus_test"]),
        "gold2676": split_stats("gold2676", CANON["bench_gold"]),
    }
    dups = exact_dups({k: splits[k] for k in ("train", "dev", "test")})
    write_csv(
        reports / "cross_split_duplicates.csv",
        dups,
        ["n", "cross_split", "locations", "text_preview"],
    )
    slim = {k: {kk: vv for kk, vv in st.items() if kk not in {"ids", "texts"}} for k, st in splits.items()}
    slim["_meta"] = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Avg 4D uses list_of_selection_bio4 via unified scorer. Paper Table 1 test Avg 4D 2.306 is not reproduced.",
        "n_cross_split_near_exact_dups": sum(1 for r in dups if r["cross_split"]),
        "n_within_or_cross_dups": len(dups),
    }
    (reports / "table1_recompute.json").write_text(
        json.dumps(slim, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("wrote", manifests / "data_pred_manifest.csv")
    print("wrote", reports / "missing_ids.csv", "rows", len(miss_rows))
    print("wrote", reports / "table3_reproduction.csv")
    print("gold unique", len(gold_ids), "test unique", len(test_ids), "test-only", len(test_ids - gold_ids))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
