#!/usr/bin/env python3
"""Score predictions on frozen Gold150. Does not overwrite gold files."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/Chinese-Skillspan-Benchmark/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import score  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    r = score(args.gold, args.pred, align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    out = {
        "gold": args.gold,
        "pred": args.pred,
        "scorer_version": r.get("scorer_version"),
        "alignment_ok": bool(r.get("alignment_ok")),
        "n_gold": r.get("gold_n_unique_ids"),
        "n_matched": r.get("n_matched"),
        "n_missing": r.get("n_missing"),
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "typed_exact_f1": te["f1"],
        "typed_relaxed_f1": tr["f1"],
        "not_comparable_to_0.4331": True,
        "not_comparable_to_0.1724": True,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
