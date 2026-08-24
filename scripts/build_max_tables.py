#!/usr/bin/env python3
"""Build paper-facing tables from existing dumps (no new training).

Writes:
  paper_results/repo/relaxed_f1_gold_v2.json
  paper_results/repo/per_domain_gold_v2.json
  paper_results/repo/per_domain_gold_v2.csv
  paper_results/repo/encoder_gold_v2.json  (refresh)
  paper_results/repo/encoder_gold_v2.csv
  tables/*.csv copies
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import (  # noqa: E402
    GOLD_FIELDS,
    PRED_FIELDS,
    extract_spans,
    index_by_id,
    load_records,
    match_exact,
    match_relaxed,
    rec_id,
    collapse,
    prf,
)

GOLD = PAPER / "data/gold_canonical_v2.jsonl"
TEST = ROOT / "data/annotated/processed/chinese_skillspan/test.json"
OUT = PAPER / "paper_results/repo"
SNAP = PAPER / "results_snapshots"
TABLES = PAPER / "tables"

MODELS = {
    "ChatGPT": PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl",
    "Claude": PAPER / "reports/views/Claude_unique_first_v2.jsonl",
    "Kimi": PAPER / "reports/views/Kimi_unique_first_v2.jsonl",
    "DeepSeek": PAPER / "reports/views/DeepSeek_unique_first_v2.jsonl",
    "Qwen": PAPER / "reports/views/Qwen_unique_first_v2.jsonl",
    "JobBERT-skill": PAPER / "reports/views/JobBERT-skill_unique_first_v2.jsonl",
    "JobBERT-knowledge": PAPER / "reports/views/JobBERT-knowledge_unique_first_v2.jsonl",
}

ENCODER_PREDS = [
    ("jobbert_zh_3m/crf_ckpt65000_ep1", PAPER / "output/jobbert_zh_3m/crf_ckpt65000_ep1/test_pred.jsonl"),
    ("jobbert_zh_1m/crf_v3_seed42", PAPER / "output/jobbert_zh_1m/crf_v3_seed42/test_pred.jsonl"),
    ("jobbert_1m_human380_v3merge_seed42", PAPER / "output/jobbert_1m_human380_v3merge_seed42/test_pred.jsonl"),
    ("jobbert_zh_listed_1m/crf_v3_seed42", PAPER / "output/jobbert_zh_listed_1m/crf_v3_seed42/test_pred.jsonl"),
    ("cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42", PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/test_pred.jsonl"),
    ("jobbert_zh_demo/crf_v3_seed42", PAPER / "output/jobbert_zh_demo/crf_v3_seed42/test_pred.jsonl"),
]


def domain_of(rec: dict, fallback: dict[str, str]) -> str:
    d = rec.get("source_domain")
    if d:
        return str(d)
    return fallback.get(rec_id(rec), "UNKNOWN")


def score_subset(gold_rows: list[dict], pred_by: dict[str, dict], ids: list[str]) -> dict:
    te_tp = te_p = te_g = 0
    re_tp = re_p = re_g = 0
    ce_tp = ce_p = ce_g = 0
    n_missing = 0
    g_by = {rec_id(r): r for r in gold_rows}
    for iid in ids:
        g = g_by[iid]
        p = pred_by.get(iid)
        gs = extract_spans(g, GOLD_FIELDS)
        if p is None:
            n_missing += 1
            ps = []
        else:
            ps = extract_spans(p, PRED_FIELDS)
        te = match_exact(gs, ps)
        re = match_relaxed(gs, ps, 0.5)
        ce = match_exact(collapse(gs), collapse(ps))
        te_tp += te["tp"]
        te_p += te["pred"]
        te_g += te["gold"]
        re_tp += re["tp"]
        re_p += re["pred"]
        re_g += re["gold"]
        ce_tp += ce["tp"]
        ce_p += ce["pred"]
        ce_g += ce["gold"]
    return {
        "n": len(ids),
        "n_missing": n_missing,
        "typed_exact": prf(te_tp, te_p, te_g),
        "typed_relaxed": prf(re_tp, re_p, re_g),
        "collapsed_exact": prf(ce_tp, ce_p, ce_g),
    }


def load_test_domains() -> dict[str, str]:
    raw = TEST.read_text(encoding="utf-8")
    rows = json.loads(raw) if raw.lstrip().startswith("[") else [json.loads(l) for l in raw.splitlines() if l.strip()]
    return {str(r["id"]): str(r.get("source_domain") or "UNKNOWN") for r in rows}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    gold = load_records(str(GOLD))
    gold_ids = [rec_id(r) for r in gold]
    fb = load_test_domains()
    for r in gold:
        if not r.get("source_domain"):
            r["source_domain"] = fb.get(rec_id(r), "UNKNOWN")
    domains = sorted(set(domain_of(r, fb) for r in gold))
    by_dom: dict[str, list[str]] = defaultdict(list)
    for r in gold:
        by_dom[domain_of(r, fb)].append(rec_id(r))

    relaxed_rows = []
    domain_rows = []
    for name, path in MODELS.items():
        if not path.is_file():
            continue
        preds = load_records(str(path))
        p_by, _ = index_by_id(preds, "first")
        overall = score_subset(gold, p_by, gold_ids)
        relaxed_rows.append(
            {
                "model": name,
                "status": "complete" if overall["n_missing"] == 0 else "incomplete",
                "n_missing": overall["n_missing"],
                "typed_exact_f1": overall["typed_exact"]["f1"],
                "typed_relaxed_f1": overall["typed_relaxed"]["f1"],
                "collapsed_exact_f1": overall["collapsed_exact"]["f1"],
                "typed_exact_p": overall["typed_exact"]["precision"],
                "typed_exact_r": overall["typed_exact"]["recall"],
            }
        )
        for d in domains:
            sub = score_subset(gold, p_by, by_dom[d])
            domain_rows.append(
                {
                    "system": name,
                    "family": "llm_dump",
                    "domain": d,
                    "n": sub["n"],
                    "n_missing": sub["n_missing"],
                    "typed_exact_f1": sub["typed_exact"]["f1"],
                    "typed_relaxed_f1": sub["typed_relaxed"]["f1"],
                    "collapsed_exact_f1": sub["collapsed_exact"]["f1"],
                }
            )

    for run, path in ENCODER_PREDS:
        if not path.is_file():
            continue
        preds = load_records(str(path))
        p_by, _ = index_by_id(preds, "first")
        for d in domains:
            sub = score_subset(gold, p_by, by_dom[d])
            domain_rows.append(
                {
                    "system": run,
                    "family": "encoder_crf",
                    "domain": d,
                    "n": sub["n"],
                    "n_missing": sub["n_missing"],
                    "typed_exact_f1": sub["typed_exact"]["f1"],
                    "typed_relaxed_f1": sub["typed_relaxed"]["f1"],
                    "collapsed_exact_f1": sub["collapsed_exact"]["f1"],
                }
            )

    (OUT / "relaxed_f1_gold_v2.json").write_text(
        json.dumps(
            {
                "gold": str(GOLD),
                "gold_n": len(gold),
                "domains": dict(Counter(domain_of(r, fb) for r in gold)),
                "rows": relaxed_rows,
                "note": "Typed relaxed = IoU≥0.5 on Gold v2 unique IDs. Incomplete dumps still scored (missing IDs = empty pred).",
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT / "per_domain_gold_v2.json").write_text(
        json.dumps({"domains": dict(Counter(domain_of(r, fb) for r in gold)), "rows": domain_rows}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    with (OUT / "per_domain_gold_v2.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["system", "family", "domain", "n", "n_missing", "typed_exact_f1", "typed_relaxed_f1", "collapsed_exact_f1"],
        )
        w.writeheader()
        w.writerows(domain_rows)
    with (OUT / "relaxed_f1_gold_v2.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(relaxed_rows[0].keys()) if relaxed_rows else ["model"])
        w.writeheader()
        w.writerows(relaxed_rows)

    # refresh encoder index from snapshots
    encoder = []
    for p in sorted(SNAP.glob("*.json")):
        if p.name == "index.json":
            continue
        s = json.loads(p.read_text(encoding="utf-8"))
        encoder.append(
            {
                "run": p.stem.replace("__", "/"),
                "status": "complete",
                "test_typed_f1": (s.get("typed_exact") or {}).get("f1"),
                "test_collapsed_f1": (s.get("collapsed_exact") or {}).get("f1"),
                "dev_typed_f1": s.get("best_dev_typed_f1"),
                "precision": (s.get("typed_exact") or {}).get("precision"),
                "recall": (s.get("typed_exact") or {}).get("recall"),
                "snapshot": f"results_snapshots/{p.name}",
            }
        )
    encoder.sort(key=lambda r: -(r["test_typed_f1"] or -1))
    (OUT / "encoder_gold_v2.json").write_text(json.dumps(encoder, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (OUT / "encoder_gold_v2.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["run", "status", "test_typed_f1", "test_collapsed_f1", "dev_typed_f1", "precision", "recall", "snapshot"],
        )
        w.writeheader()
        w.writerows(encoder)

    for src, dst in [
        (OUT / "per_domain_gold_v2.csv", TABLES / "per_domain_gold_v2.csv"),
        (OUT / "relaxed_f1_gold_v2.csv", TABLES / "relaxed_f1_gold_v2.csv"),
        (OUT / "encoder_gold_v2.csv", TABLES / "encoder_gold_v2.csv"),
    ]:
        TABLES.joinpath(dst.name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    print(json.dumps({"relaxed": len(relaxed_rows), "domain_rows": len(domain_rows), "encoder": len(encoder)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
