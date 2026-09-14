#!/usr/bin/env python3
"""Qwen LoRA SFT helpers for public-API Silver-2500 (silver_public_api_v1.0).

Not the frozen Gold150 shared-guidelines protocol (job 50981 / 0.5403).
Not JSON-offset Table C. Not V4 0.4331. Do not write F1 into confirmed-results.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from cnss_paths import paper_root

PAPER = paper_root()
WORKSPACE = PAPER.parent
MODEL_PATH = WORKSPACE / "Qwen2.5-14B-Instruct"
PROMPT_PATH = PAPER / "silver_prompt.txt"
SILVER_DATA = PAPER / "output/silver_public_2500_student_20260913/data"
OUT_ROOT = PAPER / "output/qwen_silver2500_sft_20260914"
PY_QWEN = Path("/opt/anaconda3/envs/jpy-qwen25/bin/python")

PROTOCOL_ID = "silver_public_api_v1.0_qwen_lora_sft"
ALLOWED = frozenset({"L", "K", "S", "T"})
STATUS_OK = frozenset({"candidate_complete", "confirmed_empty", "adjudication_required"})
MAX_SEQ = 8192
MAX_NEW = 1024  # gold assistant max ~532 tokens under the new schema
TARGET_SEP = (",", ":")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_system() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def render_user(sample_id: str, text: str) -> str:
    return json.dumps({"records": [{"id": sample_id, "text": text}]}, ensure_ascii=False)


def _span_tuple(item: Any, sentence: str) -> tuple[int, int, str, str]:
    if isinstance(item, dict):
        a, b = int(item["start"]), int(item["end"])
        t = str(item.get("label") or item.get("type") or "").strip().upper()
        tx = item.get("text") if isinstance(item.get("text"), str) else sentence[a:b]
        return a, b, t, tx
    a, b, t = int(item[0]), int(item[1]), str(item[2]).strip().upper()
    return a, b, t, sentence[a:b]


def gold_span_objs(row: dict) -> list[dict]:
    sent = row.get("sentence") or row.get("text") or ""
    out = []
    for item in row.get("spans") or []:
        a, b, t, tx = _span_tuple(item, sent)
        if t not in ALLOWED:
            raise ValueError(f"{row.get('id')}: bad_type {t}")
        if not (0 <= a < b <= len(sent)) or sent[a:b] != tx:
            raise ValueError(f"{row.get('id')}: span_mismatch {a}:{b}")
        out.append({"start": a, "end": b, "text": tx, "label": t})
    out.sort(key=lambda s: (s["start"], s["end"]))
    return out


def format_target(row: dict) -> str:
    spans = gold_span_objs(row)
    status = row.get("status")
    if status not in STATUS_OK:
        status = "confirmed_empty" if not spans else "candidate_complete"
    rec = {
        "id": row["id"],
        "spans": spans,
        "status": status,
        "note": row.get("note") or "",
        "issues": row.get("issues") if isinstance(row.get("issues"), list) else [],
    }
    return json.dumps({"records": [rec]}, ensure_ascii=False, separators=TARGET_SEP)


def _strip_fence(raw: str) -> str:
    s = (raw or "").strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s)
        s = re.sub(r"\s*```$", "", s)
    return s.strip()


def _load_json_blob(raw: str) -> Any:
    s = _strip_fence(raw)
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    i = s.find("{")
    if i < 0:
        i = s.find("[")
    if i < 0:
        raise json.JSONDecodeError("no_json", s, 0)
    dec = json.JSONDecoder()
    obj, _ = dec.raw_decode(s[i:])
    return obj


def _keep_spans(text: str, raw_spans: list, rejected: list) -> list[dict]:
    resolved = []
    for i, sp in enumerate(raw_spans):
        try:
            if isinstance(sp, dict):
                a, b = int(sp["start"]), int(sp["end"])
                t = str(sp.get("label") or sp.get("type") or "").strip().upper()
                tx = sp.get("text") if isinstance(sp.get("text"), str) else text[a:b]
            elif isinstance(sp, (list, tuple)) and len(sp) >= 3:
                a, b, t = int(sp[0]), int(sp[1]), str(sp[2]).strip().upper()
                tx = text[a:b]
            else:
                rejected.append({"i": i, "reason": "not_span", "span": sp})
                continue
        except (TypeError, ValueError, KeyError):
            rejected.append({"i": i, "reason": "bad_fields", "span": sp})
            continue
        if t not in ALLOWED:
            rejected.append({"i": i, "reason": "bad_type", "span": sp})
            continue
        if not (0 <= a < b <= len(text)) or text[a:b] != tx:
            rejected.append({"i": i, "reason": "offset_mismatch", "span": sp})
            continue
        resolved.append({"start": a, "end": b, "text": tx, "type": t, "_i": i})
    resolved.sort(key=lambda x: (x["start"], x["_i"]))
    kept = []
    for r in resolved:
        item = {k: r[k] for k in ("start", "end", "text", "type")}
        if any(k["start"] == r["start"] and k["end"] == r["end"] for k in kept):
            rejected.append({"reason": "duplicate_or_type_conflict", "span": item})
            continue
        if any(not (r["end"] <= k["start"] or r["start"] >= k["end"]) for k in kept):
            rejected.append({"reason": "overlap_conflict", "span": item})
            continue
        kept.append(item)
    return kept


def parse_response(raw: str, expected_id: str, text: str) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "id": expected_id,
        "spans": [],
        "format_failed": False,
        "rejected": [],
        "raw": raw,
        "outcome": None,
    }
    try:
        data = _load_json_blob(raw)
    except Exception as e:
        rec["format_failed"] = True
        rec["parse_error"] = f"json:{e}"
        rec["outcome"] = "format_failed"
        return rec
    spans_in: list | None = None
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        hit = None
        for item in data["records"]:
            if isinstance(item, dict) and str(item.get("id")) == str(expected_id):
                hit = item
                break
        if hit is None and len(data["records"]) == 1 and isinstance(data["records"][0], dict):
            hit = data["records"][0]
        if hit is None:
            rec["format_failed"] = True
            rec["parse_error"] = "id_mismatch"
            rec["outcome"] = "format_failed"
            return rec
        spans_in = hit.get("spans")
    elif isinstance(data, dict) and str(data.get("id")) == str(expected_id) and isinstance(data.get("spans"), list):
        spans_in = data["spans"]
    elif isinstance(data, list):
        spans_in = data
    else:
        rec["format_failed"] = True
        rec["parse_error"] = "bad_root"
        rec["outcome"] = "format_failed"
        return rec
    if not isinstance(spans_in, list):
        rec["format_failed"] = True
        rec["parse_error"] = "spans_not_list"
        rec["outcome"] = "format_failed"
        return rec
    n_model = len(spans_in)
    kept = _keep_spans(text, spans_in, rec["rejected"])
    rec["spans"] = kept
    if n_model == 0:
        rec["outcome"] = "ok_empty"
    elif not kept:
        rec["outcome"] = "all_spans_rejected"
    elif not rec["rejected"]:
        rec["outcome"] = "ok_nonempty"
    else:
        rec["outcome"] = "partial_rejected"
    return rec


def to_bio(text: str, spans: list[dict]) -> list[str]:
    tags = ["O"] * len(text)
    for s in spans:
        a, b, t = int(s["start"]), int(s["end"]), str(s.get("type") or s.get("label"))
        if not (0 <= a < b <= len(tags)) or t not in ALLOWED:
            continue
        if any(tags[i] != "O" for i in range(a, b)):
            continue
        tags[a] = f"B-{t}"
        for i in range(a + 1, b):
            tags[i] = f"I-{t}"
    return tags


def gold_row(row: dict) -> dict:
    sent = row.get("sentence") or row.get("text") or ""
    bio = row.get("list_of_selection_bio4")
    if not isinstance(bio, list) or len(bio) != len(sent):
        bio = to_bio(sent, [{"start": s["start"], "end": s["end"], "type": s["label"]} for s in gold_span_objs(row)])
    return {
        "id": row["id"],
        "sentence": sent,
        "tokens": row.get("tokens") if isinstance(row.get("tokens"), list) and len(row["tokens"]) == len(sent) else list(sent),
        "list_of_selection_bio4": bio,
        "source_domain": row.get("source_domain"),
        "status": row.get("status"),
    }


def pred_row(sample_id: str, text: str, parsed: dict, extra: dict | None = None) -> dict:
    rec = {
        "id": sample_id,
        "sentence": text,
        "tokens": list(text),
        "pred_tags": to_bio(text, parsed.get("spans") or []),
        "list_of_selection_bio4": to_bio(text, parsed.get("spans") or []),
        "pred_spans": parsed.get("spans") or [],
        "outcome": parsed.get("outcome"),
        "format_failed": parsed.get("format_failed"),
        "parse_error": parsed.get("parse_error"),
    }
    if extra:
        rec.update(extra)
    return rec


def convert_split(src: Path) -> list[dict]:
    out = []
    for row in load_jsonl(src):
        sent = row["sentence"]
        asst = format_target(row)
        parsed = parse_response(asst, row["id"], sent)
        exp = [(s["start"], s["end"], s["label"]) for s in gold_span_objs(row)]
        got = [(s["start"], s["end"], s["type"]) for s in parsed.get("spans") or []]
        if got != exp:
            raise SystemExit(f"roundtrip_mismatch {row['id']}: {exp} vs {got}")
        out.append(
            {
                "id": row["id"],
                "text": sent,
                "sentence": sent,
                "assistant": asst,
                "source_spans_offset": [{"start": a, "end": b, "type": t} for a, b, t in exp],
                "status": row.get("status"),
                "source_domain": row.get("source_domain"),
                "list_of_selection_bio4": gold_row(row)["list_of_selection_bio4"],
                "tokens": gold_row(row)["tokens"],
            }
        )
    return out
