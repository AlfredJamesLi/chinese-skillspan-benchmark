#!/usr/bin/env python3
"""Gold150 shared-prompt occurrence parser v1.1 (patch1).

Hardening vs reviewed v1.0 (SHA 1993aed3...):
- no default occurrence=0
- occurrence must satisfy type(value) is int and >= 0 (reject bool/float/str)
- type must be exactly one of {"L","K","S","T"} (no first-letter truncation)
- text must be non-empty str
- per-span field errors reject that span only (no batch abort / TypeError leak)
- overlap: sort by start asc; same start keep earlier original output order
- exact duplicate (same start/end/type) recorded as duplicate
- same start/end different type recorded as position_type_conflict
"""
from __future__ import annotations

import json
import re
from typing import Any

ALLOWED_TYPES = frozenset({"L", "K", "S", "T"})


def find_all_starts(text: str, needle: str) -> list[int]:
    if not needle:
        return []
    starts, i = [], 0
    while True:
        j = text.find(needle, i)
        if j < 0:
            break
        starts.append(j)
        i = j + 1
    return starts


def resolve_span(text: str, sp: Any, output_index: int) -> tuple[dict | None, str | None]:
    if not isinstance(sp, dict):
        return None, "not_dict"
    missing = [k for k in ("text", "occurrence", "type") if k not in sp]
    if missing:
        return None, "missing_fields:" + ",".join(missing)
    if "start" in sp or "end" in sp:
        return None, "offset_fields_not_allowed"

    needle = sp.get("text")
    if not isinstance(needle, str):
        return None, "text_not_str"
    if needle == "":
        return None, "text_empty"

    occ = sp.get("occurrence")
    # bool is a subclass of int in Python — reject explicitly
    if type(occ) is not int:
        return None, "occurrence_not_int"
    if occ < 0:
        return None, "occurrence_negative"

    typ = sp.get("type")
    if not isinstance(typ, str) or typ not in ALLOWED_TYPES:
        return None, "bad_type"

    starts = find_all_starts(text, needle)
    if occ >= len(starts):
        return None, "occurrence_oob"
    start = starts[occ]
    end = start + len(needle)
    if text[start:end] != needle:
        return None, "slice_mismatch"
    return {
        "start": start,
        "end": end,
        "text": needle,
        "type": typ,
        "_output_index": output_index,
    }, None


def parse_response(raw: str, expected_id: str, text: str) -> dict[str, Any]:
    """Return parsed record with outcome classification.

    outcome:
      - ok_empty: legal empty spans []
      - ok_nonempty: at least one kept span, no rejects
      - format_failed: illegal whole response
      - all_spans_rejected: non-empty model spans list but none kept
      - partial_rejected: some kept and some rejected
    """
    rec: dict[str, Any] = {
        "id": expected_id,
        "spans": [],
        "format_failed": False,
        "rejected": [],
        "raw": raw,
        "outcome": None,
    }
    s = (raw or "").strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s)
        s = re.sub(r"\s*```$", "", s)
    try:
        data = json.loads(s)
    except Exception as e:
        rec["format_failed"] = True
        rec["parse_error"] = f"json:{e}"
        rec["outcome"] = "format_failed"
        return rec
    if not isinstance(data, dict):
        rec["format_failed"] = True
        rec["parse_error"] = "not_object"
        rec["outcome"] = "format_failed"
        return rec
    if str(data.get("id")) != str(expected_id):
        rec["format_failed"] = True
        rec["parse_error"] = "id_mismatch"
        rec["outcome"] = "format_failed"
        return rec
    spans = data.get("spans")
    if not isinstance(spans, list):
        rec["format_failed"] = True
        rec["parse_error"] = "spans_not_list"
        rec["outcome"] = "format_failed"
        return rec

    n_model_spans = len(spans)
    resolved = []
    for i, sp in enumerate(spans):
        try:
            r, err = resolve_span(text, sp, i)
        except Exception as e:
            rec["rejected"].append(
                {"i": i, "reason": f"span_exception:{type(e).__name__}", "span": sp}
            )
            continue
        if err:
            rec["rejected"].append({"i": i, "reason": err, "span": sp})
            continue
        resolved.append(r)

    # Overlap policy: start ascending; same start -> original output order
    resolved.sort(key=lambda x: (x["start"], x["_output_index"]))
    kept = []
    for r in resolved:
        if any(
            k["start"] == r["start"] and k["end"] == r["end"] and k["type"] == r["type"]
            for k in kept
        ):
            rec["rejected"].append(
                {
                    "reason": "duplicate",
                    "span": {kk: r[kk] for kk in ("start", "end", "text", "type")},
                }
            )
            continue
        if any(
            k["start"] == r["start"] and k["end"] == r["end"] and k["type"] != r["type"]
            for k in kept
        ):
            rec["rejected"].append(
                {
                    "reason": "position_type_conflict",
                    "span": {kk: r[kk] for kk in ("start", "end", "text", "type")},
                }
            )
            continue
        if any(not (r["end"] <= k["start"] or r["start"] >= k["end"]) for k in kept):
            rec["rejected"].append(
                {
                    "reason": "overlap_conflict",
                    "span": {kk: r[kk] for kk in ("start", "end", "text", "type")},
                }
            )
            continue
        kept.append({kk: r[kk] for kk in ("start", "end", "text", "type")})

    rec["spans"] = kept
    if rec["format_failed"]:
        rec["outcome"] = "format_failed"
    elif n_model_spans == 0:
        rec["outcome"] = "ok_empty"
    elif len(kept) == 0:
        rec["outcome"] = "all_spans_rejected"
    elif len(rec["rejected"]) == 0:
        rec["outcome"] = "ok_nonempty"
    else:
        rec["outcome"] = "partial_rejected"
    return rec


if __name__ == "__main__":
    import argparse
    from pathlib import Path as P

    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--id", default="syn-1")
    ap.add_argument("--raw-file", required=True)
    args = ap.parse_args()
    raw = P(args.raw_file).read_text(encoding="utf-8")
    print(json.dumps(parse_response(raw, args.id, args.text), ensure_ascii=False, indent=2))
