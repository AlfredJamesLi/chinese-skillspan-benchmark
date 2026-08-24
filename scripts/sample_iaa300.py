#!/usr/bin/env python3
"""Stratified ~300-item dual-IAA sample from corpus train.

Locks out the Gold-style 80 finals. Does not rewrite train.json or Gold v2.
This is a worksheet only — no labels are invented.
"""
from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
FINAL80 = PAPER / "reports/gold_style_relabel/sample80_final.json"
OUT = PAPER / "reports/iaa300"
SEED = 20260823
N_TARGET = 300


def load_json(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(l) for l in raw.splitlines() if l.strip()]


def bio_n(rec: dict) -> int:
    tags = rec.get("list_of_selection_bio4") or []
    return sum(1 for t in tags if str(t).startswith("B-"))


def bucket(rec: dict) -> str:
    n = bio_n(rec)
    if n == 0:
        return "empty"
    if n <= 2:
        return "low"
    return "high"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    locked = {r["id"] for r in load_json(FINAL80)}
    rows = [r for r in load_json(TRAIN) if r.get("id") not in locked]
    rng = random.Random(SEED)
    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for rec in rows:
        cells[(rec.get("source_domain") or "NA", bucket(rec))].append(rec)
    domains = sorted({d for d, _ in cells})
    buckets = ["empty", "low", "high"]
    # even split; leftover goes to high
    per = N_TARGET // max(1, len(domains) * len(buckets))
    leftover = N_TARGET - per * len(domains) * len(buckets)
    quota = {}
    for d in domains:
        for b in buckets:
            quota[(d, b)] = per
    for d in domains:
        quota[(d, "high")] = quota.get((d, "high"), 0) + leftover // max(1, len(domains))
    picked = []
    for key, n in quota.items():
        pool = cells.get(key) or []
        rng.shuffle(pool)
        picked.extend(pool[:n])
    rng.shuffle(picked)
    manifest = []
    for rec in picked:
        manifest.append(
            {
                "id": rec.get("id"),
                "global_id": rec.get("global_id"),
                "source_domain": rec.get("source_domain"),
                "bucket": bucket(rec),
                "n_silver_spans": bio_n(rec),
                "sentence": rec.get("sentence"),
            }
        )
    (OUT / "iaa300_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (OUT / "iaa300_worksheet.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "source_domain", "bucket", "n_silver_spans", "sentence"])
        w.writeheader()
        for row in manifest:
            w.writerow({k: row[k] for k in w.fieldnames})
    meta = {
        "seed": SEED,
        "n": len(manifest),
        "excluded_human80": len(locked),
        "quota": {f"{d}|{b}": n for (d, b), n in quota.items()},
        "actual": dict(Counter(f"{r['source_domain']}|{r['bucket']}" for r in manifest)),
        "overwrote_train": False,
        "touched_gold_v2": False,
        "note": "TRAIN human Gold-style 300 (excludes lock80). Not the eval Gold v3 pilot. Dual annotation not started.",
    }
    (OUT / "iaa300_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
