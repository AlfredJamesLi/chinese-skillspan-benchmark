#!/usr/bin/env python3
"""Copy Codex wave batches_out into the parent 5436 package for merge."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

PKG = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/data/silver_plus_10k_prep_20260913/codex_remaining_5436")
WAVES = PKG / "waves"


def main() -> int:
    dest = PKG / "batches_out"
    dest.mkdir(exist_ok=True)
    copied = []
    missing = []
    for wave in ("wave1", "wave2", "wave3"):
        src = WAVES / wave / "batches_out"
        if not src.is_dir():
            missing.append(wave)
            continue
        n = 0
        for p in sorted(src.glob("batch_*.json")):
            shutil.copyfile(p, dest / p.name)
            n += 1
        copied.append({"wave": wave, "n_out": n})
    report = {"copied": copied, "parent_batches_out": sum(1 for _ in dest.glob("batch_*.json"))}
    (WAVES / "SYNC_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
