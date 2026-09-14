#!/usr/bin/env python3
"""Merge public-API Silver (2500 + Codex wave1/2 zip + wave3) into a v6a-ratio student split.

Drops adjudication_required. Does not rewrite frozen v6a or Gold150.
"""
from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from pathlib import Path

from silver_public_api_lib import dump_json, dump_jsonl, load_jsonl, to_student_row

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ZIP_DIR = PAPER / "data/silver_plus_10k_prep_20260913/cnss_silver_wave1_wave2_20260914T040731Z"
RUN2500 = PAPER / "data/silver_plus_10k_prep_20260913/run2500_public_api_v1/labeled.jsonl"
WAVE3 = PAPER / "data/silver_plus_10k_prep_20260913/codex_remaining_5436/waves/wave3/labeled.jsonl"
REMAINING = PAPER / "data/silver_plus_10k_prep_20260913/codex_remaining_5436/remaining.jsonl"
GOLD150 = PAPER / "data/gold150_test.jsonl"
DEFAULT_OUT = PAPER / "output/silver_new_merged_student_20260914/data"
V6A_RATIO = 2150 / (2150 + 169)
TRAIN_STATUSES = {"candidate_complete", "confirmed_empty"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def nfc_text(s: str) -> str:
    import unicodedata

    return unicodedata.normalize("NFC", s or "")


def check_offsets(text: str, spans: list) -> None:
    for sp in spans or []:
        if isinstance(sp, dict):
            start, end, frag = int(sp["start"]), int(sp["end"]), sp.get("text")
        else:
            start, end, frag = int(sp[0]), int(sp[1]), None
        if not (0 <= start < end <= len(text)):
            raise ValueError(f"bad bounds {start}:{end} len={len(text)}")
        if frag is not None and text[start:end] != frag:
            raise ValueError(f"slice mismatch {start}:{end}")


def gold_sets() -> tuple[set[str], set[str]]:
    ids, sents = set(), set()
    if GOLD150.is_file():
        for r in load_jsonl(GOLD150):
            ids.add(str(r.get("source_id") or r.get("id") or "").strip())
            sents.add(nfc_text((r.get("text") or r.get("sentence") or "").strip()))
    return ids, sents


def from_student_labeled(path: Path, wave: str) -> tuple[list[dict], list[dict]]:
    keep, dropped = [], []
    for r in load_jsonl(path):
        rec = dict(r)
        rec["wave"] = wave
        check_offsets(rec.get("sentence") or "", rec.get("spans") or [])
        if rec.get("status") in TRAIN_STATUSES:
            keep.append(rec)
        else:
            dropped.append(rec)
    return keep, dropped


def from_zip(zip_dir: Path, remaining: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    keep, dropped = [], []
    for r in load_jsonl(zip_dir / "data/all_candidates_3620.jsonl"):
        src = remaining.get(r["id"])
        if src is None:
            raise SystemExit(f"wave1/2 id not in remaining.jsonl: {r['id']}")
        if nfc_text(src["text"]) != nfc_text(r["text"]):
            raise SystemExit(f"text mismatch vs remaining: {r['id']}")
        check_offsets(r["text"], r.get("spans") or [])
        rec = to_student_row(src, r)
        rec["wave"] = "wave1_wave2_zip"
        rec["status"] = r.get("status")
        rec["note"] = r.get("note")
        rec["issues"] = r.get("issues") or []
        if r.get("status") in TRAIN_STATUSES:
            keep.append(rec)
        else:
            dropped.append(rec)
    return keep, dropped


def main() -> int:
    remaining = {r["id"]: r for r in load_jsonl(REMAINING)}
    gold_ids, gold_sents = gold_sets()
    blocks = []
    k2500, d2500 = from_student_labeled(RUN2500, "run2500")
    kw12, dw12 = from_zip(ZIP_DIR, remaining)
    kw3, dw3 = from_student_labeled(WAVE3, "wave3")
    keep = k2500 + kw12 + kw3
    dropped = d2500 + dw12 + dw3
    ids = [r["id"] for r in keep]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate ids in trainable pool")
    all_ids = ids + [r["id"] for r in dropped]
    if len(all_ids) != len(set(all_ids)):
        raise SystemExit("duplicate ids across keep/drop")
    leak = [r["id"] for r in keep if r["id"] in gold_ids or nfc_text((r.get("sentence") or "").strip()) in gold_sents]
    if leak:
        raise SystemExit(f"Gold150 overlap: {leak[:10]}")
    ai = [r["id"] for r in keep if (r.get("source_domain") or "") == "人工智能招聘"]
    if ai:
        raise SystemExit(f"unexpected 人工智能招聘 in new silver: {ai[:8]}")
    n_train = int(round(len(keep) * V6A_RATIO))
    n_dev = len(keep) - n_train
    rng = random.Random(20260914)
    by_d: dict[str, list] = {}
    for r in keep:
        by_d.setdefault(r.get("source_domain") or "unk", []).append(r)
    train, dev = [], []
    for _, grp in sorted(by_d.items()):
        rng.shuffle(grp)
        k = int(round(len(grp) * V6A_RATIO))
        train.extend(grp[:k])
        dev.extend(grp[k:])
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
    out = Path(DEFAULT_OUT)
    dump_jsonl(out / "train.jsonl", train)
    dump_jsonl(out / "dev.jsonl", dev)
    dump_jsonl(out / "adjudication_held.jsonl", dropped)
    report = {
        "not_v6a_nocross": True,
        "not_paper_main": True,
        "exclude_adjudication_required": True,
        "n_all_labeled": len(keep) + len(dropped),
        "n_trainable": len(keep),
        "n_train": len(train),
        "n_dev": len(dev),
        "n_adjudication_held": len(dropped),
        "ratio_copied_from_v6a": V6A_RATIO,
        "seed": 20260914,
        "sources": {
            "run2500": {"keep": len(k2500), "adj": len(d2500)},
            "wave1_wave2_zip": {"keep": len(kw12), "adj": len(dw12), "zip_train_candidates": 3407},
            "wave3": {"keep": len(kw3), "adj": len(dw3)},
        },
        "status_trainable": dict(Counter(r.get("status") for r in keep)),
        "train_domains": dict(Counter(r.get("source_domain") for r in train)),
        "dev_domains": dict(Counter(r.get("source_domain") for r in dev)),
        "n_spans_train": sum(len(r.get("spans") or []) for r in train),
        "n_spans_dev": sum(len(r.get("spans") or []) for r in dev),
        "gold150_overlap": 0,
        "ai_jobs": 0,
        "sha256_train": sha256_file(out / "train.jsonl"),
        "sha256_dev": sha256_file(out / "dev.jsonl"),
        "prompt_id": "silver_public_api_v1.0",
        "zip_prompt_sha256": "b6223e9a2e9b02afa19cba79ba908766d9240acb233723fbe6f53b40e6b04fd6",
        "note": "New public-API Silver student. Not comparable to JobBERT-zh v6a 0.5536. Do not write into confirmed-results.md.",
    }
    dump_json(out / "SPLIT.json", report)
    print(json.dumps({k: report[k] for k in ("n_trainable", "n_train", "n_dev", "n_adjudication_held", "train_domains", "dev_domains")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
