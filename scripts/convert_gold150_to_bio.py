#!/usr/bin/env python3
"""Convert frozen human-reference (artifact Gold150) Doccano jsonl to scorer BIO jsonl.

The freeze (`data/gold150_test.jsonl`) uses `source_id` and Doccano type
strings, including the misspelling `Tranversial SKills`. This script maps
those at read time and writes a **derived** file. It never overwrites the freeze.

Paper names: human reference set = challenge cohort + calibration cohort.
Do not rename this file or the freeze.

Offsets are Unicode code points, half-open [start, end), on `list(text)`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from cnss_paths import paper_root

PAPER = paper_root()
FREEZE = PAPER / "data/gold150_test.jsonl"
FREEZE_SHA256 = "ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0"
DEFAULT_OUT = PAPER / "data/gold150_test.bio.jsonl"

# Keep freeze spellings as keys. Do not rename the source file.
TYPE_MAP = {
    "Language_Skills&Knowledge": "L",
    "knowledge": "K",
    "skills": "S",
    "Tranversial SKills": "T",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def spans_to_bio(text: str, labels: list) -> list[str]:
    tokens = list(text)
    tags = ["O"] * len(tokens)
    for item in labels or []:
        if not isinstance(item, (list, tuple)) or len(item) < 3:
            raise ValueError(f"bad label triple: {item!r}")
        start, end, raw_type = int(item[0]), int(item[1]), str(item[2])
        if raw_type not in TYPE_MAP:
            raise ValueError(f"unknown Doccano type {raw_type!r} (keep freeze spelling)")
        if start < 0 or end > len(tokens) or start >= end:
            raise ValueError(f"span [{start},{end}) out of range for len={len(tokens)}")
        typ = TYPE_MAP[raw_type]
        for i in range(start, end):
            if tags[i] != "O":
                raise ValueError(f"overlapping span at {i}: {tags[i]} vs {typ}")
        tags[start] = f"B-{typ}"
        for i in range(start + 1, end):
            tags[i] = f"I-{typ}"
    return tags


def convert_record(rec: dict) -> dict:
    source_id = rec.get("source_id")
    if not source_id:
        raise ValueError("record missing source_id")
    text = rec.get("text") or ""
    tags = spans_to_bio(text, rec.get("label") or [])
    return {
        "id": str(source_id).strip(),
        "source_id": str(source_id).strip(),
        "sentence": text,
        "tokens": list(text),
        "list_of_selection_bio4": tags,
        "split": rec.get("split"),
        "handbook": rec.get("handbook"),
        "seq": rec.get("seq"),
        "example_id": rec.get("example_id"),
        "n_spans": rec.get("n_spans"),
        "annotators": rec.get("annotators"),
        "derived_from": "gold150_test.jsonl",
    }


def convert_path(src: Path, dst: Path) -> dict:
    if dst.resolve() == src.resolve():
        raise SystemExit("refusing to overwrite the Gold150 freeze")
    digest = sha256_file(src)
    if src.resolve() == FREEZE.resolve() and digest != FREEZE_SHA256:
        raise SystemExit(f"freeze SHA-256 is {digest}, expected {FREEZE_SHA256}")
    rows_in = []
    with src.open(encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            rows_in.append(json.loads(line))
    out = [convert_record(r) for r in rows_in]
    ids = [r["id"] for r in out]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate source_id in Gold150")
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n_non_o = sum(1 for r in out if any(t != "O" for t in r["list_of_selection_bio4"]))
    return {
        "n": len(out),
        "n_with_spans": n_non_o,
        "src": str(src),
        "dst": str(dst),
        "src_sha256": digest,
        "dst_sha256": sha256_file(dst),
        "type_map": TYPE_MAP,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Gold150 Doccano freeze → scorer BIO (derived file).")
    ap.add_argument("--in_path", default=str(FREEZE))
    ap.add_argument("--out_path", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    src = Path(args.in_path)
    dst = Path(args.out_path)
    meta = convert_path(src, dst)
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    after = sha256_file(src)
    if src.resolve() == FREEZE.resolve() and after != FREEZE_SHA256:
        raise SystemExit("Gold150 freeze SHA-256 changed during convert")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
