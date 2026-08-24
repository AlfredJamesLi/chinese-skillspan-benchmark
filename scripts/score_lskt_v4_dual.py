#!/usr/bin/env python3
"""Score one pred dump on Gold v2 and on LSKT v4 silver (g2 ids). Does not train."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import score  # noqa: E402

PRED = PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl"
G2 = PAPER / "data/gold_canonical_v2.jsonl"
V4 = PAPER / "data/test_lskt_v4_silver_g2ids.jsonl"
OUT = PAPER / "reports/sandbox_lskt_v4_silver/dual_eval.json"
MD = PAPER / "reports/sandbox_lskt_v4_silver/DUAL_EVAL.md"


def one(name: str, gold: Path) -> dict:
    r = score(str(gold), str(PRED), align_mode="official", n_boot=0)
    te, ce = r["typed_exact"], r["collapsed_exact"]
    return {
        "name": name,
        "gold": str(gold),
        "alignment_ok": r.get("alignment_ok"),
        "n_gold": r.get("gold_n_unique_ids"),
        "n_missing": r.get("n_missing"),
        "typed_p": te["precision"],
        "typed_r": te["recall"],
        "typed_f1": te["f1"],
        "collapsed_f1": ce["f1"],
        "error": r.get("error"),
    }


def main() -> int:
    if not PRED.is_file():
        print("pred not ready:", PRED)
        return 2
    rows = [
        one("Gold v2 (frozen official)", G2),
        one("LSKT v4 silver on Gold-v2 IDs", V4),
    ]
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Dual eval (sandbox, not for paper)",
        "",
        f"Pred: `{PRED}`",
        "",
        "| Gold | typed P/R/F1 | collapsed F1 | align |",
        "|---|---|---:|---|",
    ]
    for s in rows:
        prf = f"{s['typed_p']:.4f}/{s['typed_r']:.4f}/{s['typed_f1']:.4f}"
        lines.append(f"| {s['name']} | {prf} | {s['collapsed_f1']:.4f} | {s['alignment_ok']} |")
    lines.append("")
    lines.append("Do not copy into confirmed-results.md.")
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
