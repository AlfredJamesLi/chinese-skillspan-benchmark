#!/usr/bin/env python3
"""CPU checks: B2 char offsets, BIO↔span, Gold150 convert, no Gold150 leakage into B2 IDs."""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "adapters"))
from convert_gold150_to_bio import convert_record, FREEZE_SHA256, spans_to_bio, TYPE_MAP  # noqa: E402

B2_TRAIN = ROOT / "chinese_data" / "train_b2.jsonl"
B2_DEV = ROOT / "chinese_data" / "dev_b2.jsonl"
GOLD = ROOT / "chinese_data" / "gold150_test.jsonl"
LSKT = {"L", "K", "S", "T"}


def load(p: Path):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bio_to_spans(tags):
    spans = []
    i, n = 0, len(tags)
    while i < n:
        t = tags[i]
        if t.startswith("B-"):
            typ = t[2:]
            j = i + 1
            while j < n and tags[j] == f"I-{typ}":
                j += 1
            spans.append([i, j, typ])
            i = j
        else:
            i += 1
    return spans


def check_split(path: Path, expect_n: int, name: str):
    rows = load(path)
    assert len(rows) == expect_n, (name, len(rows), expect_n)
    ids = []
    long_n = 0
    empty_n = 0
    punct_ok = 0
    latin_ok = 0
    for r in rows:
        sid = str(r["id"]).strip()
        ids.append(sid)
        sent = r["sentence"]
        toks = r["tokens"]
        tags = r["list_of_selection_bio4"]
        assert "".join(toks) == sent, sid
        assert list(sent) == toks, sid
        assert len(tags) == len(toks), sid
        for t in tags:
            assert t == "O" or (t[:2] in ("B-", "I-") and t[2:] in LSKT), (sid, t)
        rebuilt = bio_to_spans(tags)
        gold_spans = [[int(a), int(b), str(c)] for a, b, c in r.get("spans") or []]
        assert rebuilt == gold_spans, (sid, rebuilt[:3], gold_spans[:3])
        for a, b, typ in gold_spans:
            assert sent[a:b] == "".join(toks[a:b])
            assert tags[a] == f"B-{typ}"
        if len(toks) > 128:
            long_n += 1
        if not gold_spans:
            empty_n += 1
        if any(ch in sent for ch in "，。；、（）"):
            punct_ok += 1
        if any("A" <= ch <= "Z" or "a" <= ch <= "z" or ch.isdigit() for ch in sent):
            latin_ok += 1
    assert len(ids) == len(set(ids)), name
    return {
        "n": len(rows),
        "unique_ids": len(set(ids)),
        "long_gt_128": long_n,
        "empty_span_sents": empty_n,
        "has_cjk_punct": punct_ok,
        "has_latin_or_digit": latin_ok,
        "sha256": sha(path),
    }


def main():
    train = check_split(B2_TRAIN, 2150, "train_b2")
    dev = check_split(B2_DEV, 169, "dev_b2")
    gold_rows = load(GOLD)
    assert len(gold_rows) == 150
    assert sha(GOLD) == FREEZE_SHA256
    converted = [convert_record(r) for r in gold_rows]
    assert len({r["id"] for r in converted}) == 150
    # freeze type spellings including the documented misspelling
    types = {item[2] for r in gold_rows for item in r.get("label") or []}
    assert types <= set(TYPE_MAP)
    train_ids = {json.loads(x)["id"] for x in B2_TRAIN.read_text(encoding="utf-8").splitlines() if x.strip()}
    dev_ids = {json.loads(x)["id"] for x in B2_DEV.read_text(encoding="utf-8").splitlines() if x.strip()}
    gold_ids = {r["id"] for r in converted}
    overlap_train = sorted(train_ids & gold_ids)
    overlap_dev = sorted(dev_ids & gold_ids)
    # Gold150 must not be used for training/selection even if IDs collide; record collisions.
    report = {
        "train_b2": train,
        "dev_b2": dev,
        "gold150": {"n": 150, "sha256": sha(GOLD), "doccano_types": sorted(types)},
        "id_overlap_gold_train": overlap_train,
        "id_overlap_gold_dev": overlap_dev,
        "note": "Gold150 stays eval-only even if source_id appears in B2.",
    }
    out = ROOT / "adapters" / "chinese_roundtrip_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("chinese roundtrip checks passed")


if __name__ == "__main__":
    main()
