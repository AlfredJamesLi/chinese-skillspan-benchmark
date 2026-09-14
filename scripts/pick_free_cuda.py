#!/usr/bin/env python3
"""Print the first GPU index with used memory below a threshold. Exit 1 if none."""
from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-used-mib", type=float, default=800.0)
    ap.add_argument("--exclude", default="", help="Comma-separated GPU indices to skip.")
    args = ap.parse_args()
    exclude = {x.strip() for x in args.exclude.split(",") if x.strip()}
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=index,memory.used", "--format=csv,noheader,nounits"],
            text=True,
        )
    except Exception as e:
        print(f"nvidia-smi failed: {e}", file=sys.stderr)
        return 1
    free: list[str] = []
    for line in out.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 2:
            continue
        idx, mem = parts[0], parts[1]
        if idx in exclude:
            continue
        try:
            used = float(mem)
        except ValueError:
            continue
        if used < args.max_used_mib:
            free.append(idx)
    if not free:
        return 1
    print(free[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
