#!/usr/bin/env python3
"""Score domain-mix 1M CRF vs JobBERT 1M baseline 0.1224.

Internal only. Does not write paper numbers or confirmed-results.md.
Success: test typed F1 > 0.1224 and/or 事业单位 domain F1 >> 0.015.
Do not auto-launch 3M (listed-3M already skipped).
"""
from __future__ import annotations

import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
OUT = PAPER / "output/jobbert_zh_domain_1m"
JOB = OUT / "crf_v3_seed42/run_summary.json"
BASELINE = PAPER / "output/jobbert_zh_1m/crf_v3_seed42/run_summary.json"
LISTED = PAPER / "output/jobbert_zh_listed_1m/crf_v3_seed42/run_summary.json"
BEST3M = PAPER / "output/jobbert_zh_3m/crf_ckpt65000_ep1/run_summary.json"
DEC = OUT / "decision.json"
BASELINE_F1 = 0.1224
SY_FAIL = 0.015


def from_summary(path: Path) -> dict:
    if not path.is_file():
        return {"ok": False, "path": str(path)}
    r = json.loads(path.read_text(encoding="utf-8"))
    te = r.get("typed_exact") or {}
    return {
        "ok": True,
        "path": str(path),
        "typed_f1": te.get("f1"),
        "p": te.get("precision"),
        "r": te.get("recall"),
        "best_dev": r.get("best_dev_typed_f1"),
        "scorer": r.get("scorer_version"),
    }


def seed_row(seed: int) -> dict:
    p = OUT / f"crf_v3_seed{seed}" / "run_summary.json"
    d = from_summary(p)
    d["seed"] = seed
    return d


def main() -> int:
    job = from_summary(JOB)
    base = from_summary(BASELINE)
    listed = from_summary(LISTED)
    best = from_summary(BEST3M)
    jf = job.get("typed_f1")
    vs_base = None
    if isinstance(jf, (int, float)):
        vs_base = round(jf - BASELINE_F1, 4)
    seeds = [seed_row(s) for s in (42, 123, 2026)]
    f1s = [s["typed_f1"] for s in seeds if isinstance(s.get("typed_f1"), (int, float))]
    mean = sum(f1s) / len(f1s) if f1s else None
    if isinstance(jf, (int, float)) and jf > BASELINE_F1:
        rec = "keep_domain_mix_encoder"
        why = (
            f"seed42 typed F1 {jf:.4f} > JobBERT-1M baseline {BASELINE_F1}. "
            "Do not launch listed/domain 3M unless 事业单位 F1 also rises."
        )
        launch_3m = False
    elif isinstance(jf, (int, float)) and jf <= BASELINE_F1:
        rec = "drop_hold_no_3m"
        why = (
            f"seed42 typed F1 {jf:.4f} ≤ baseline {BASELINE_F1} (Δ={vs_base}). "
            "Same stop rule as listed-1M. Do not scale to 3M."
        )
        launch_3m = False
    else:
        rec = "pending"
        why = "CRF seed42 summary missing."
        launch_3m = False
    dec = {
        "ok": bool(job.get("ok")),
        "rec": rec,
        "launch_3m": launch_3m,
        "why": why,
        "baseline_f1": BASELINE_F1,
        "shiye_fail_ref": SY_FAIL,
        "vs_baseline": vs_base,
        "domain_1m_seed42": job,
        "seeds": seeds,
        "mean_typed_f1": mean,
        "jobbert_1m": base,
        "listed_1m": listed,
        "jobbert_3m_ckpt65000": best,
        "paper_numbers": False,
        "note": (
            "Per-domain 事业单位 F1 is the secondary success criterion "
            "(encoder failure mode ~0.015). Recompute with scripts/build_max_tables.py "
            "after predictions exist."
        ),
    }
    DEC.write_text(json.dumps(dec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dec, ensure_ascii=False, indent=2))
    return 0 if job.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
