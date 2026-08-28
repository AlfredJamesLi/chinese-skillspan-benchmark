#!/usr/bin/env python3
"""Validate LSKT char/BIO spans. Does not overwrite Gold or invent IAA."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

TYPES = {"L", "K", "S", "T"}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rec_id(r: dict) -> str:
    return str(r.get("id") or r.get("source_id") or r.get("meta", {}).get("id") or "")


def token_char_map(sentence: str, tokens: list) -> list[tuple[int, int]]:
    pos = 0
    out = []
    for tok in tokens:
        t = str(tok)
        idx = sentence.find(t, pos)
        if idx < 0:
            idx = pos
            end = pos + len(t)
        else:
            end = idx + len(t)
        out.append((idx, end))
        pos = end
    return out


def bio_to_char(sentence: str, tokens: list, tags: list) -> list[tuple[int, int, str]]:
    mapping = token_char_map(sentence, tokens)
    n = min(len(tokens), len(tags), len(mapping))
    spans = []
    i = 0
    while i < n:
        tag = str(tags[i] or "O")
        if tag.startswith("B-"):
            typ = tag[2:]
            a, b = mapping[i]
            j = i + 1
            while j < n and str(tags[j]) == f"I-{typ}":
                b = mapping[j][1]
                j += 1
            if typ in TYPES and 0 <= a < b <= len(sentence):
                spans.append((a, b, typ))
            i = j
        else:
            i += 1
    return spans


def extract_spans(r: dict) -> tuple[str, list[tuple[int, int, str]]]:
    sent = r.get("text") or r.get("sentence") or ""
    raw = r.get("label") or r.get("labels") or r.get("v4_spans") or r.get("cws_spans")
    spans: list[tuple[int, int, str]] = []
    if isinstance(raw, list) and raw and not isinstance(raw[0], str):
        for item in raw:
            if isinstance(item, dict):
                a, b, t = int(item["start"]), int(item["end"]), str(item.get("type") or item.get("label") or "")
            else:
                a, b, t = int(item[0]), int(item[1]), str(item[2]) if len(item) > 2 else "S"
            spans.append((a, b, t))
        # hybrid v4_spans are token indices; accept if they fit the sentence, else BIO
        if spans and any(b > len(sent) for _a, b, _t in spans):
            spans = []
    if not spans:
        toks = r.get("tokens") or list(sent)
        tags = r.get("list_of_selection_bio4") or r.get("tags_skill_clean") or []
        if tags:
            spans = bio_to_char(sent, [str(t) for t in toks], tags)
    return sent, spans


def classify_pair(a1: int, b1: int, a2: int, b2: int) -> str:
    if b1 <= a2 or b2 <= a1:
        return "none"
    if a1 == a2 and b1 == b2:
        return "same-boundary"
    if (a1 <= a2 and b1 >= b2) or (a2 <= a1 and b2 >= b1):
        return "nested"
    return "crossing"


def validate(path: Path) -> dict:
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    ids = [rec_id(r) for r in rows]
    id_c = Counter(ids)
    dup_ids = [i for i, n in id_c.items() if i and n > 1]
    n_empty = 0
    n_bad_off = 0
    n_bad_lab = 0
    n_dup_span = 0
    type_c: Counter = Counter()
    ov = Counter()
    pair_c: Counter = Counter()
    for r in rows:
        sent, spans = extract_spans(r)
        if not spans:
            n_empty += 1
            continue
        seen = set()
        for a, b, t in spans:
            type_c[t] += 1
            if t not in TYPES:
                n_bad_lab += 1
            if not (0 <= a < b <= len(sent)):
                n_bad_off += 1
                continue
            if sent[a:b] == "":
                n_bad_off += 1
            key = (a, b, t)
            if key in seen:
                n_dup_span += 1
            seen.add(key)
        for i in range(len(spans)):
            for j in range(i + 1, len(spans)):
                a1, b1, t1 = spans[i]
                a2, b2, t2 = spans[j]
                kind = classify_pair(a1, b1, a2, b2)
                if kind != "none":
                    ov[kind] += 1
                    labs = tuple(sorted([t1, t2]))
                    pair_c[f"{labs[0]}/{labs[1]}"] += 1
    return {
        "path": str(path),
        "n_rows": len(rows),
        "n_unique_ids": len([i for i in id_c if i]),
        "n_duplicate_ids": len(dup_ids),
        "n_empty_sentence": n_empty,
        "label_counts": dict(type_c),
        "n_bad_offsets": n_bad_off,
        "n_illegal_labels": n_bad_lab,
        "n_duplicate_spans": n_dup_span,
        "overlap": dict(ov),
        "overlap_pairs": dict(pair_c),
        "sha256": sha256_file(path),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    reports = [validate(p) for p in args.jsonl]
    text = json.dumps(reports, ensure_ascii=False, indent=2) + "\n"
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
