#!/usr/bin/env python3
"""Score one CRF pred on SOP-v4 test golds (exact + IoU≥0.5). Sandbox; not Gold v2 freeze."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import score  # noqa: E402

GOLDS = [
    ("sop_rule_v4_2601", PAPER / "data/test_lskt_v4_rule_g2ids.jsonl"),
    ("simhuman_980", PAPER / "data/test_lskt_v4_simhuman980.jsonl"),
    ("codex_2601", PAPER / "data/test_lskt_v4_silver_g2ids.jsonl"),
    ("gold_v2_official", PAPER / "data/gold_canonical_v2.jsonl"),
    ("sop_cws_2601", PAPER / "data/test_lskt_v4_cws_g2ids.jsonl"),
]


def one(name: str, gold: Path, pred: Path) -> dict:
    r = score(str(gold), str(pred), align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    return {
        "name": name,
        "gold": str(gold),
        "alignment_ok": r.get("alignment_ok"),
        "n_gold": r.get("gold_n_unique_ids"),
        "typed_exact_f1": te["f1"],
        "typed_relaxed_f1": tr["f1"],
        "gap_relaxed_minus_exact": tr["f1"] - te["f1"],
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "collapsed_exact_f1": r["collapsed_exact"]["f1"],
        "collapsed_relaxed_f1": r["collapsed_relaxed"]["f1"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    pred = Path(args.pred)
    if not pred.is_file():
        print("missing pred", pred)
        return 2
    rows = [one(n, g, pred) for n, g in GOLDS if g.is_file()]
    out = {
        "pred": str(pred),
        "gold_v2_untouched": True,
        "not_for_confirmed_results": True,
        "scores": rows,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
