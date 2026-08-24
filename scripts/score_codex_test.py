#!/usr/bin/env python3
"""Score frozen preds on Gold v2 vs Codex-corrected LSKT v4 test silver. No training."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = PAPER.parent
sys.path.insert(0, str(PAPER / "scorer"))
sys.path.insert(0, str(PAPER / "scripts"))
from eval_lskt_projection import project_2way, prf_from_counts  # noqa: E402
from score_lskt import (  # noqa: E402
    GOLD_FIELDS,
    extract_spans,
    index_by_id,
    load_records,
    match_exact,
    score,
)

G2 = PAPER / "data/gold_canonical_v2.jsonl"
CODEX = PAPER / "data/test_lskt_v4_silver_g2ids.jsonl"
OUT_JSON = PAPER / "reports/sandbox_lskt_v4_silver/CODEX_TEST_EVAL.json"
OUT_MD = PAPER / "reports/sandbox_lskt_v4_silver/CODEX_TEST_EVAL.md"

MODELS = [
    ("GPT-4o", PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl", "llm"),
    ("DeepSeek", PAPER / "reports/views/DeepSeek_unique_first_v2.jsonl", "llm"),
    ("Qwen2.5-14B", PAPER / "reports/views/Qwen_unique_first_v2.jsonl", "llm"),
    ("JobBERT-zh_1M_goldstyle-v3_s42", PAPER / "output/jobbert_zh_1m/crf_v3_seed42/test_pred.jsonl", "encoder"),
    ("JobBERT-zh_1M_rule-v4_s42", PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl", "encoder"),
    ("JobBERT-zh_1M_s2026", PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_2026/test_pred.jsonl", "encoder"),
    ("RoBERTa-wwm_goldstyle-v3_s42", PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/test_pred.jsonl", "encoder"),
]


def way2(gold: Path, pred: Path) -> dict:
    gidx, ginfo = index_by_id(load_records(str(gold)), "first")
    pidx, _ = index_by_id(load_records(str(pred)), "first")
    tp = fp = fn = 0
    miss = 0
    for gid, g in gidx.items():
        p = pidx.get(gid)
        if p is None:
            miss += 1
            continue
        gs = extract_spans(g, GOLD_FIELDS)
        ps = extract_spans(p, ("pred_tags", "list_of_selection_bio4", "list_of_selection"))
        m = match_exact(project_2way(gs), project_2way(ps))
        tp += m["tp"]
        fp += m["fp"]
        fn += m["fn"]
    d = prf_from_counts(tp, tp + fp, tp + fn)
    d.update(miss=miss, n_gold=ginfo["n_unique_ids"])
    return d


def one(model: str, pred: Path, gold: Path, gold_name: str) -> dict:
    r = score(str(gold), str(pred), align_mode="official", n_boot=0)
    te, ce = r["typed_exact"], r["collapsed_exact"]
    w2 = way2(gold, pred)
    return {
        "model": model,
        "gold": gold_name,
        "pred": str(pred),
        "alignment_ok": r.get("alignment_ok"),
        "n_missing": r.get("n_missing"),
        "typed_p": te["precision"],
        "typed_r": te["recall"],
        "typed_f1": te["f1"],
        "collapsed_f1": ce["f1"],
        "way2_f1": w2["f1"],
        "error": r.get("error"),
    }


def main() -> int:
    rows = []
    skipped = []
    for name, path, fam in MODELS:
        if not path.is_file():
            skipped.append({"model": name, "path": str(path)})
            continue
        for gold, gname in ((G2, "Gold v2"), (CODEX, "Codex v4 silver")):
            row = one(name, path, gold, gname)
            row["family"] = fam
            rows.append(row)
            print(f"{name:32} {gname:18} typed={row['typed_f1']:.4f} coll={row['collapsed_f1']:.4f} way2={row['way2_f1']:.4f} align={row['alignment_ok']}", flush=True)
    OUT_JSON.write_text(json.dumps({"rows": rows, "skipped": skipped}, ensure_ascii=False, indent=2), encoding="utf-8")
    by = {}
    for r in rows:
        by.setdefault(r["model"], {})[r["gold"]] = r
    lines = [
        "# Codex-corrected test eval (sandbox, not for paper)",
        "",
        "Gold v2 frozen. Test silver = Codex 50+51 on 2601 Gold-v2 IDs. No retraining. Do not copy into confirmed-results.md.",
        "",
        "| Model | Gold v2 typed F1 | Codex silver typed F1 | Gold v2 collapsed | Codex collapsed | Codex 2-way | align |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for name, _, _ in MODELS:
        if name not in by:
            continue
        a, b = by[name]["Gold v2"], by[name]["Codex v4 silver"]
        lines.append(
            f"| {name} | {a['typed_f1']:.4f} | **{b['typed_f1']:.4f}** | {a['collapsed_f1']:.4f} | {b['collapsed_f1']:.4f} | {b['way2_f1']:.4f} | {a['alignment_ok']}/{b['alignment_ok']} |"
        )
    lines.append("")
    if skipped:
        lines.append("Skipped missing preds: " + ", ".join(s["model"] for s in skipped))
        lines.append("")
    lines.append("JobBERT-zh_1M_rule-v4 was trained on rule silver, not Codex. Codex test is out-of-distribution for that run.")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
