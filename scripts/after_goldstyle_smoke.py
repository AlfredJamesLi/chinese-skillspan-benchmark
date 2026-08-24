#!/usr/bin/env python3
"""Summarize Gold-style smoke vs silver smoke. Does not write paper numbers."""
from __future__ import annotations

import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
GS = PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/run_summary.json"
SILVER = PAPER / "output/cn_roberta_wwm_crf/smoke_seed42_gpu1/run_summary.json"
OUT = PAPER / "reports/gold_style_relabel/goldstyle_smoke_result.md"
THRESH = 0.05  # below this: do not start 3-seed; consider tighter rewrite


def f1_of(path: Path) -> dict:
    if not path.is_file():
        return {"ok": False, "path": str(path)}
    r = json.loads(path.read_text(encoding="utf-8"))
    te = r.get("typed_exact") or {}
    cr = r.get("collapsed_exact") or {}
    return {
        "ok": True,
        "align": r.get("alignment_ok"),
        "best_dev": r.get("best_dev_typed_f1"),
        "typed_f1": te.get("f1"),
        "typed_tp": te.get("tp"),
        "typed_pred": te.get("pred"),
        "typed_gold": te.get("gold"),
        "collapsed_f1": cr.get("f1"),
        "scorer": r.get("scorer_version"),
        "gold_sha": r.get("gold_sha256"),
    }


def main() -> int:
    gs = f1_of(GS)
    sv = f1_of(SILVER)
    tf = gs.get("typed_f1")
    rec = "unknown"
    if gs.get("ok") and isinstance(tf, (int, float)):
        if tf >= THRESH:
            rec = "consider_3seed"
        elif tf > (sv.get("typed_f1") or 0) + 0.01:
            rec = "improved_but_tighten"
        else:
            rec = "still_near_zero_tighten"
    lines = [
        "# Gold-style v1 smoke vs silver smoke",
        "",
        "Do **not** copy these numbers into the PDF or confirmed-results.md until protocol + labels are accepted.",
        "",
        f"- silver smoke: `{SILVER}`",
        f"- goldstyle smoke: `{GS}`",
        f"- recommendation: **{rec}** (3-seed only if `consider_3seed`)",
        "",
        "| run | align | dev typed | official typed F1 | collapsed | TP/pred/gold |",
        "|---|---|---:|---:|---:|---|",
        f"| silver | {sv.get('align')} | {sv.get('best_dev')} | {sv.get('typed_f1')} | {sv.get('collapsed_f1')} | {sv.get('typed_tp')}/{sv.get('typed_pred')}/{sv.get('typed_gold')} |",
        f"| goldstyle v1 | {gs.get('align')} | {gs.get('best_dev')} | {gs.get('typed_f1')} | {gs.get('collapsed_f1')} | {gs.get('typed_tp')}/{gs.get('typed_pred')}/{gs.get('typed_gold')} |",
        "",
        f"Threshold for auto 3-seed: typed F1 ≥ {THRESH}. Current rec=`{rec}`.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"rec": rec, "goldstyle": gs, "silver": sv, "report": str(OUT)}, ensure_ascii=False, indent=2))
    return 0 if gs.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
