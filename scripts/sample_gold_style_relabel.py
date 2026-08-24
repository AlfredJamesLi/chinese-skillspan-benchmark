#!/usr/bin/env python3
"""Stratified 80-item train sample for Gold-style boundary relabel (review only).

Does not rewrite train.json. Does not touch Gold v2. Silver spans are written
only to the human worksheet, never to the LLM prompt input.
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
OUT = PAPER / "reports/gold_style_relabel"
SEED = 20260823
N_SAMPLE = 80


def bio_spans(tags: list) -> list[tuple[int, int, str]]:
    out: list[tuple[int, int, str]] = []
    i, n = 0, len(tags)
    while i < n:
        t = tags[i] or "O"
        if str(t).startswith("B-"):
            typ = t[2:]
            j = i + 1
            while j < n and tags[j] == f"I-{typ}":
                j += 1
            out.append((i, j, typ))
            i = j
        else:
            i += 1
    return out


def bucket(rec: dict) -> str:
    n = len(bio_spans(rec.get("list_of_selection_bio4") or []))
    if n == 0:
        return "empty"
    if n <= 2:
        return "low"
    return "high"


def tokens_of(rec: dict) -> list[str]:
    return [str(t) for t in (rec.get("tokens") or list(rec.get("sentence") or ""))]


def span_texts(rec: dict) -> list[str]:
    toks = tokens_of(rec)
    return [f"{typ}:{''.join(toks[a:b])}" for a, b, typ in bio_spans(rec.get("list_of_selection_bio4") or [])]


def numbered_tokens(toks: list[str]) -> str:
    return " ".join(f"{i}:{toks[i]}" for i in range(len(toks)))


def main() -> None:
    rows = json.loads(TRAIN.read_text(encoding="utf-8"))
    rng = random.Random(SEED)
    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for rec in rows:
        domain = rec.get("source_domain") or "NA"
        cells[(domain, bucket(rec))].append(rec)

    # 2 domains × 3 buckets. Empty/process sentences matter; high-frag is the
    # main Gold mismatch. Slightly overweight 应届生/high and 人工智能/high.
    quota = {
        ("应届生招聘", "empty"): 12,
        ("应届生招聘", "low"): 12,
        ("应届生招聘", "high"): 16,
        ("人工智能招聘", "empty"): 12,
        ("人工智能招聘", "low"): 12,
        ("人工智能招聘", "high"): 16,
    }
    picked: list[dict] = []
    for key, n in quota.items():
        pool = list(cells.get(key, []))
        rng.shuffle(pool)
        if len(pool) < n:
            raise SystemExit(f"not enough rows for {key}: {len(pool)} < {n}")
        for rec in pool[:n]:
            picked.append(rec)

    picked.sort(key=lambda r: (r.get("source_domain") or "", r.get("id") or ""))
    OUT.mkdir(parents=True, exist_ok=True)

    llm_items = []
    for rec in picked:
        toks = tokens_of(rec)
        llm_items.append(
            {
                "id": rec.get("id"),
                "source_domain": rec.get("source_domain"),
                "sentence": rec.get("sentence"),
                "tokens": toks,
                "n_tokens": len(toks),
            }
        )
    (OUT / "sample80_llm_input.json").write_text(
        json.dumps(llm_items, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    man_path = OUT / "sample80_manifest.csv"
    with man_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "source_domain",
                "silver_bucket",
                "n_silver_spans",
                "n_tokens",
                "silver_spans",
                "sentence",
            ],
        )
        w.writeheader()
        for rec in picked:
            sp = bio_spans(rec.get("list_of_selection_bio4") or [])
            w.writerow(
                {
                    "id": rec.get("id"),
                    "source_domain": rec.get("source_domain"),
                    "silver_bucket": bucket(rec),
                    "n_silver_spans": len(sp),
                    "n_tokens": len(tokens_of(rec)),
                    "silver_spans": " | ".join(span_texts(rec)),
                    "sentence": rec.get("sentence"),
                }
            )

    ws_path = OUT / "sample80_worksheet.csv"
    with ws_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "source_domain",
                "sentence",
                "silver_spans_do_not_copy",
                "reviewer_spans_json",
                "decision",
                "note",
            ],
        )
        w.writeheader()
        for rec in picked:
            w.writerow(
                {
                    "id": rec.get("id"),
                    "source_domain": rec.get("source_domain"),
                    "sentence": rec.get("sentence"),
                    "silver_spans_do_not_copy": " | ".join(span_texts(rec)),
                    "reviewer_spans_json": "",
                    "decision": "",
                    "note": "",
                }
            )

    md = [
        "# Gold-style train relabel — 80-item review sheet",
        "",
        f"Seed `{SEED}`. Source: corpus `train.json` only. **Do not write these labels into Gold v2.**",
        "Silver spans below are contrast only; Gold-style labels should be complete requirements, not 2–4 character fragments.",
        "",
        "Fill `spans` as `[[start,end,\"L|K|S|T\"], ...]` on **token index** (left-closed, right-open).",
        "Empty sentence → `[]`. Decision: `accept` / `edit` / `empty`.",
        "",
    ]
    for i, rec in enumerate(picked, 1):
        toks = tokens_of(rec)
        md.append(f"## {i}. `{rec.get('id')}` · {rec.get('source_domain')} · silver={bucket(rec)}")
        md.append("")
        md.append(rec.get("sentence") or "")
        md.append("")
        md.append("tokens: `" + numbered_tokens(toks) + "`")
        md.append("")
        md.append("silver (do not copy): " + ("；".join(span_texts(rec)) or "(none)"))
        md.append("")
        md.append("your spans: `[]`")
        md.append("")
    (OUT / "sample80_worksheet.md").write_text("\n".join(md), encoding="utf-8")

    meta = {
        "seed": SEED,
        "n": len(picked),
        "train_path": str(TRAIN),
        "quota": {f"{a}|{b}": n for (a, b), n in quota.items()},
        "realized": dict(Counter(f"{r.get('source_domain')}|{bucket(r)}" for r in picked)),
        "ids": [r.get("id") for r in picked],
    }
    (OUT / "sample80_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"n": len(picked), "out": str(OUT), "cells": meta["realized"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
