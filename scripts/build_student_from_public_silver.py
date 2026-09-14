#!/usr/bin/env python3
"""Build JobBERT student train/dev from public-API Silver labels. Does not rewrite v6a."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

from silver_public_api_lib import dump_json, dump_jsonl, load_jsonl

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
DEFAULT_LABELED = PAPER / "data/silver_plus_10k_prep_20260913/run2500_public_api_v1/labeled.jsonl"
DEFAULT_OUT = PAPER / "output/silver_public_2500_student_20260913/data"
GOLD150 = PAPER / "data/gold150_test.jsonl"
V6A_RATIO = 2150 / (2150 + 169)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labeled", default=str(DEFAULT_LABELED))
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--seed", type=int, default=20260913)
    ap.add_argument("--min-n", type=int, default=100)
    args = ap.parse_args()
    raw = Path(args.labeled).read_text(encoding="utf-8")
    if raw and not raw.endswith("\n"):
        raw = raw.rsplit("\n", 1)[0]
    rows = [json.loads(l) for l in raw.splitlines() if l.strip()]
    if len(rows) < args.min_n:
        raise SystemExit(f"too few labeled rows: {len(rows)} < {args.min_n}")
    bad = []
    for r in rows:
        tokens = r.get("tokens") or []
        tags = r.get("list_of_selection_bio4") or []
        sent = r.get("sentence") or ""
        if not sent or not tokens or len(tokens) != len(tags) or len(tokens) != len(sent):
            bad.append(r.get("id"))
    if bad:
        raise SystemExit(f"token/tag/sentence length mismatch: {bad[:8]}")
    gold_ids = set()
    gold_sents = set()
    if GOLD150.is_file():
        for r in load_jsonl(GOLD150):
            gold_ids.add(str(r.get("source_id") or r.get("id") or "").strip())
            gold_sents.add((r.get("text") or r.get("sentence") or "").strip())
    leak = [r["id"] for r in rows if r["id"] in gold_ids or (r.get("sentence") or "").strip() in gold_sents]
    if leak:
        raise SystemExit(f"Gold150 overlap in labeled silver: {leak[:10]}")
    n_train = int(round(len(rows) * V6A_RATIO))
    n_dev = len(rows) - n_train
    rng = random.Random(args.seed)
    by_d: dict[str, list] = {}
    for r in rows:
        by_d.setdefault(r.get("source_domain") or "unk", []).append(r)
    train, dev = [], []
    for d, grp in sorted(by_d.items()):
        rng.shuffle(grp)
        k = int(round(len(grp) * V6A_RATIO))
        train.extend(grp[:k])
        dev.extend(grp[k:])
    # fix rounding so totals match
    rng.shuffle(train)
    rng.shuffle(dev)
    while len(train) > n_train and train:
        dev.append(train.pop())
    while len(dev) > n_dev and dev:
        train.append(dev.pop())
    for r in train:
        r["split"] = "train"
    for r in dev:
        r["split"] = "dev"
    out = Path(args.out_dir)
    dump_jsonl(out / "train.jsonl", train)
    dump_jsonl(out / "dev.jsonl", dev)
    dump_json(
        out / "SPLIT.json",
        {
            "n_labeled": len(rows),
            "n_train": len(train),
            "n_dev": len(dev),
            "seed": args.seed,
            "ratio_copied_from_v6a": V6A_RATIO,
            "train_domains": dict(Counter(r.get("source_domain") for r in train)),
            "dev_domains": dict(Counter(r.get("source_domain") for r in dev)),
            "status_counts": dict(Counter(r.get("status") for r in rows)),
            "n_spans": sum(len(r.get("spans") or []) for r in rows),
            "sha256_train": sha256_file(out / "train.jsonl"),
            "sha256_dev": sha256_file(out / "dev.jsonl"),
            "gold150_overlap": 0,
            "note": "New public-API Silver. Not v6a_nocross. Do not write 0.5536 onto this run.",
        },
    )
    print(json.dumps({"n_train": len(train), "n_dev": len(dev), "n_spans": sum(len(r.get("spans") or []) for r in rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
