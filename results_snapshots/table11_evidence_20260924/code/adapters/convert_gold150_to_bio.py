#!/usr/bin/env python3
"""Gold150 Doccano freeze → scorer BIO. Never overwrites the freeze.

Standalone copy for the external-benchmark tree (no cnss_paths import).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "chinese_data" / "gold150_test.jsonl"
FREEZE_SHA256 = "ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0"
DEFAULT_OUT = ROOT / "chinese_data" / "gold150_test.bio.jsonl"

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
    if digest != FREEZE_SHA256 and src.name == "gold150_test.jsonl":
        raise SystemExit(f"freeze SHA-256 is {digest}, expected {FREEZE_SHA256}")
    rows_in = []
    with src.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows_in.append(json.loads(line))
    out = [convert_record(r) for r in rows_in]
    ids = [r["id"] for r in out]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate source_id in Gold150")
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return {
        "n": len(out),
        "src": str(src),
        "dst": str(dst),
        "src_sha256": digest,
        "dst_sha256": sha256_file(dst),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_path", default=str(FREEZE))
    ap.add_argument("--out_path", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    print(json.dumps(convert_path(Path(args.in_path), Path(args.out_path)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
