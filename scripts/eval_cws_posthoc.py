#!/usr/bin/env python3
"""Post-hoc jieba snap on existing CRF preds. Sandbox; not for confirmed-results."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from score_lskt import score  # noqa: E402

OUT_DIR = PAPER / "reports/sandbox_lskt_v4_silver/cws_snap"
PREDS = [
    (
        "jobbert_1m_v4",
        PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl",
        PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred_cws.jsonl",
    ),
    (
        "jobbert_3m_v4",
        PAPER / "output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/test_pred.jsonl",
        PAPER / "output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/test_pred_cws.jsonl",
    ),
]
GOLDS = [
    ("gold_v2_official", PAPER / "data/gold_canonical_v2.jsonl"),
    ("sop_rule_v4_2601", PAPER / "data/test_lskt_v4_rule_g2ids.jsonl"),
    ("sop_cws_2601", PAPER / "data/test_lskt_v4_cws_g2ids.jsonl"),
]


def one(gold: Path, pred: Path) -> dict:
    r = score(str(gold), str(pred), align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    return {
        "gold": gold.name,
        "alignment_ok": r.get("alignment_ok"),
        "n_gold": r.get("gold_n_unique_ids"),
        "typed_exact_f1": te["f1"],
        "typed_relaxed_f1": tr["f1"],
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "collapsed_exact_f1": r["collapsed_exact"]["f1"],
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "not_for_confirmed_results": True,
        "gold_v2_untouched": True,
        "note": "Post-hoc jieba snap on frozen CRF preds. Not a retrain. Not Table 3.",
        "runs": [],
    }
    lines = [
        "# CWS post-hoc snap (sandbox)",
        "",
        "Existing JobBERT CRF predictions, spans snapped to jieba words. **Not** Gold v2 freeze. Do not copy into `confirmed-results.md`.",
        "",
        "| Pred | Gold | exact F1 | IoU≥0.5 F1 | P / R |",
        "|---|---|---:|---:|---|",
    ]
    for name, src, dst in PREDS:
        if not src.is_file():
            report["runs"].append({"name": name, "missing": str(src)})
            continue
        raw = cws.load_jsonl(src)
        rows = [cws.rewrite_record(r, tag_field="pred_tags") for r in raw]
        cws.write_jsonl(dst, rows)
        before_rows = []
        for r in raw:
            spans = cws.g.bio_spans(cws.tags_of(r, "pred_tags"))
            before_rows.append({**r, "cws_spans": [[a, b, t] for a, b, t in spans], "cws_n_changed": 0})
        before = cws.span_stats(before_rows)
        after = cws.span_stats(rows)
        run = {
            "name": name,
            "pred_raw": str(src),
            "pred_cws": str(dst),
            "before": before,
            "after": after,
            "scores_raw": [],
            "scores_cws": [],
        }
        for gname, gold in GOLDS:
            if not gold.is_file():
                continue
            s_raw = {"gold_name": gname, **one(gold, src)}
            s_cws = {"gold_name": gname, **one(gold, dst)}
            run["scores_raw"].append(s_raw)
            run["scores_cws"].append(s_cws)
            lines.append(
                f"| {name} raw | {gname} | {s_raw['typed_exact_f1']:.4f} | {s_raw['typed_relaxed_f1']:.4f} | {s_raw['typed_exact_p']:.4f}/{s_raw['typed_exact_r']:.4f} |"
            )
            lines.append(
                f"| {name} **cws** | {gname} | {s_cws['typed_exact_f1']:.4f} | {s_cws['typed_relaxed_f1']:.4f} | {s_cws['typed_exact_p']:.4f}/{s_cws['typed_exact_r']:.4f} |"
            )
        report["runs"].append(run)
        lines.append("")
    lines += [
        "",
        "Retrain (whether BERT *learns* complete words) is a separate run: `output/jobbert_zh_1m/crf_lskt_v4_cws_seed42/` on `train_lskt_v4_cws.jsonl`.",
        "",
    ]
    (OUT_DIR / "posthoc_eval.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "POSTHOC.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
