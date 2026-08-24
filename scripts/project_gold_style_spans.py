#!/usr/bin/env python3
"""Map LLM {text, type} spans onto train tokens (leftmost exact match).

Used after human/LLM return. Does not write train.json or Gold v2.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def find_span(tokens: list[str], text: str) -> tuple[int, int] | None:
    flat = "".join(tokens)
    needle = (text or "").strip()
    if not needle:
        return None
    pos = flat.find(needle)
    if pos < 0:
        return None
    acc = 0
    start = None
    for i, tok in enumerate(tokens):
        nxt = acc + len(tok)
        if start is None and acc <= pos < nxt:
            start = i
        if start is not None and nxt >= pos + len(needle):
            return start, i + 1
        acc = nxt
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm_json", required=True, help="JSON array from the model")
    ap.add_argument("--input_json", required=True, help="sample80_llm_input.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    items = {r["id"]: r for r in json.loads(Path(args.input_json).read_text(encoding="utf-8"))}
    raw = json.loads(Path(args.llm_json).read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw.get("items") or raw.get("data") or []
    out = []
    n_miss = 0
    for rec in raw:
        iid = rec.get("id")
        src = items.get(iid)
        if src is None:
            out.append({**rec, "error": "unknown_id"})
            continue
        toks = src["tokens"]
        aligned = []
        misses = []
        for sp in rec.get("spans") or []:
            text = sp.get("text") if isinstance(sp, dict) else None
            typ = (sp.get("type") if isinstance(sp, dict) else None) or "S"
            typ = str(typ).strip().upper()[:1]
            if typ not in {"L", "K", "S", "T"}:
                typ = "S"
            hit = find_span(toks, str(text or ""))
            if hit is None:
                misses.append(text)
                n_miss += 1
            else:
                aligned.append([hit[0], hit[1], typ, text])
        out.append(
            {
                "id": iid,
                "sentence": src["sentence"],
                "tokens": toks,
                "spans_token": [[a, b, t] for a, b, t, _ in aligned],
                "spans_text": [{"start": a, "end": b, "type": t, "text": tx} for a, b, t, tx in aligned],
                "unaligned": misses,
                "comment": rec.get("comment"),
            }
        )
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"n": len(out), "unaligned_spans": n_miss, "out": args.out}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
