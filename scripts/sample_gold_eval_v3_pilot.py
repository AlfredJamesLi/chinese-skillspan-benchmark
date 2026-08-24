#!/usr/bin/env python3
"""Stratified 300-item dual-IAA pilot from Gold v2 for a future eval Gold.

Does not rewrite gold_canonical_v2.jsonl or train.json.
Annotator sheets do not include v2 spans (adjudicator-only reference).
"""
from __future__ import annotations

import csv
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from goldstyle_empty_rules import empty_hint

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
GOLD = PAPER / "data/gold_canonical_v2.jsonl"
OUT = PAPER / "reports/gold_eval_v3"
SEED = 20260823
N_TARGET = 300


def load_gold() -> list[dict]:
    return [json.loads(l) for l in GOLD.read_text(encoding="utf-8").splitlines() if l.strip()]


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


def v2_spans(rec: dict) -> list[list]:
    tags = rec.get("list_of_selection_bio4") or []
    toks = rec.get("tokens") or []
    out = []
    i = 0
    while i < len(tags):
        t = tags[i]
        if isinstance(t, str) and t.startswith("B-"):
            typ = t[2:]
            j = i + 1
            while j < len(tags) and tags[j] == f"I-{typ}":
                j += 1
            text = "".join(toks[i:j]) if toks else ""
            out.append({"start": i, "end": j, "type": typ, "text": text})
            i = j
        else:
            i += 1
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_gold()
    rng = random.Random(SEED)
    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for rec in rows:
        cells[(rec.get("source_domain") or "NA", bucket(rec))].append(rec)
    domains = ["人工智能招聘", "阿里云公开数据集", "事业单位招聘"]
    buckets = ["empty", "low", "high"]
    per = N_TARGET // (len(domains) * len(buckets))
    leftover = N_TARGET - per * len(domains) * len(buckets)
    quota = {(d, b): per for d in domains for b in buckets}
    # leftover → 事业单位 empty (lock the empty rule)
    quota[("事业单位招聘", "empty")] = quota[("事业单位招聘", "empty")] + leftover
    picked: list[dict] = []
    short: list[str] = []
    for key, n in quota.items():
        pool = list(cells.get(key) or [])
        rng.shuffle(pool)
        got = pool[:n]
        picked.extend(got)
        if len(got) < n:
            short.append(f"{key[0]}|{key[1]} want={n} got={len(got)}")
    rng.shuffle(picked)

    manifest = []
    ref = []
    for rec in picked:
        d = rec.get("source_domain") or ""
        sent = rec.get("sentence") or ""
        item = {
            "id": rec.get("id"),
            "global_id": rec.get("global_id"),
            "source_domain": d,
            "bucket_v2": bucket(rec),
            "n_v2_spans": bio_n(rec),
            "empty_hint": empty_hint(sent, d),
            "sentence": sent,
        }
        manifest.append(item)
        ref.append({**item, "v2_spans": v2_spans(rec), "tokens": rec.get("tokens") or []})

    (OUT / "pilot300_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "pilot300_v2_reference.json").write_text(
        json.dumps(ref, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    fields = ["id", "source_domain", "bucket_v2", "n_v2_spans", "empty_hint", "sentence", "spans_json", "comment"]
    for name in ("annotator_A", "annotator_B"):
        with (OUT / f"pilot300_{name}.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for row in manifest:
                w.writerow({**{k: row[k] for k in fields if k in row}, "spans_json": "", "comment": ""})

    sha = GOLD.read_bytes()
    import hashlib

    meta = {
        "seed": SEED,
        "n": len(manifest),
        "gold_v2": str(GOLD),
        "gold_v2_sha256": hashlib.sha256(sha).hexdigest(),
        "quota": {f"{d}|{b}": quota[(d, b)] for d in domains for b in buckets},
        "actual": dict(Counter(f"{r['source_domain']}|{r['bucket_v2']}" for r in manifest)),
        "short_cells": short,
        "empty_hint_n": sum(1 for r in manifest if r["empty_hint"]),
        "overwrote_gold_v2": False,
        "overwrote_train": False,
        "note": "Worksheet only. Dual IAA not started. v2 spans are in pilot300_v2_reference.json for adjudication only.",
    }
    (OUT / "pilot300_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
