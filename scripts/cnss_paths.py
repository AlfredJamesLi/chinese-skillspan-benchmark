#!/usr/bin/env python3
"""Resolve the paper tree without laboratory absolute paths.

Works on server A, server B (with or without the old SCESC symlink), and a
plain GitHub clone. Optional: CNSS_PAPER_ROOT or CNSS_ROOT.
"""
from __future__ import annotations

import os
from pathlib import Path


def paper_root() -> Path:
    env = os.environ.get("CNSS_PAPER_ROOT") or os.environ.get("CNSS_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if (p / "scorer" / "score_lskt.py").is_file():
            return p
        cand = p / "Chinese_skill_benchmark_Paper"
        if (cand / "scorer" / "score_lskt.py").is_file():
            return cand
        raise SystemExit(f"CNSS_ROOT={env!r} is not a paper or repo root")
    here = Path(__file__).resolve()
    if here.parent.name in {"scripts", "scorer"}:
        return here.parents[1]
    return here.parents[1]
