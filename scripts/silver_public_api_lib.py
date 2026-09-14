#!/usr/bin/env python3
"""Shared helpers for silver_public_api_v1.0 GPT calls. No API key in logs."""
from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

ALLOWED_STATUS = {"candidate_complete", "confirmed_empty", "adjudication_required"}
ALLOWED_LABEL = {"L", "K", "S", "T"}
ALLOWED_KIND = {"scope", "boundary", "type"}
REC_KEYS = {"id", "spans", "status", "note", "issues"}
SPAN_KEYS = {"start", "end", "text", "label"}
ISSUE_KEYS = {"kind", "text", "alternatives", "reason"}
DEFAULT_BASE = "https://claudeed.ysaikeji.cn"
PROMPT_ID = "silver_public_api_v1.0"
REQUEST_MODEL = "gpt-6-astra"


def load_key(path: Path | None = None) -> str:
    p = path or (Path.home() / ".config/ysaikeji/api_key")
    key = p.read_text(encoding="utf-8").strip()
    if not key.startswith("sk-") or len(key) < 20:
        raise SystemExit("API key file missing or malformed")
    return key


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def hamilton(counts: dict[str, int], n: int) -> dict[str, int]:
    if n < 0:
        raise ValueError("n must be >= 0")
    total = sum(counts.values())
    if total <= 0:
        raise ValueError("empty counts")
    raw = {k: n * v / total for k, v in counts.items()}
    base = {k: int(v) for k, v in raw.items()}
    rem = n - sum(base.values())
    order = sorted(raw, key=lambda k: (raw[k] - base[k], k), reverse=True)
    out = dict(base)
    for k in order[:rem]:
        out[k] += 1
    return out


def sample_by_domain(rows: list[dict], n: int, domain_key: str = "source_domain") -> list[dict]:
    counts = Counter(r[domain_key] for r in rows)
    quota = hamilton(dict(counts), n)
    picked: list[dict] = []
    used = Counter()
    for r in rows:
        d = r[domain_key]
        if used[d] < quota.get(d, 0):
            picked.append(r)
            used[d] += 1
        if len(picked) >= n:
            break
    if len(picked) != n:
        raise SystemExit(f"sample_by_domain got {len(picked)} != {n}")
    return picked


def extract_json(text: str) -> tuple[Any, str | None]:
    raw = (text or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        if raw.endswith("```"):
            raw = raw[: raw.rfind("```")].rstrip()
        if raw.lower().startswith("json"):
            raw = raw[4:].lstrip()
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as e:
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(raw[start : end + 1]), f"extracted_object:{e}"
            except json.JSONDecodeError as e2:
                return None, f"{e}; extract_failed:{e2}"
        return None, str(e)


def overlaps(a: dict, b: dict) -> bool:
    return not (a["end"] <= b["start"] or b["end"] <= a["start"])


def _find_occurrences(text: str, needle: str) -> list[int]:
    if not needle:
        return []
    out = []
    start = 0
    while True:
        i = text.find(needle, start)
        if i < 0:
            return out
        out.append(i)
        start = i + 1


def repair_span_offsets(text: str, spans: list) -> tuple[list, list[dict]]:
    """Snap span.text onto the sentence when reported offsets miss by a few code points."""
    if not isinstance(spans, list):
        return spans, []
    repaired = []
    notes = []
    for j, sp in enumerate(spans):
        if not isinstance(sp, dict):
            repaired.append(sp)
            continue
        stxt = sp.get("text")
        try:
            start, end = int(sp.get("start")), int(sp.get("end"))
        except (TypeError, ValueError):
            repaired.append(sp)
            continue
        if isinstance(stxt, str) and 0 <= start < end <= len(text) and text[start:end] == stxt:
            repaired.append(sp)
            continue
        if not isinstance(stxt, str) or not stxt:
            repaired.append(sp)
            continue
        hits = _find_occurrences(text, stxt)
        if not hits:
            repaired.append(sp)
            notes.append({"i": j, "action": "unrepaired_missing", "text": stxt})
            continue
        try:
            reported = int(sp.get("start"))
        except (TypeError, ValueError):
            reported = 0
        chosen = min(hits, key=lambda i: (abs(i - reported), i))
        new = dict(sp)
        new["start"] = chosen
        new["end"] = chosen + len(stxt)
        repaired.append(new)
        notes.append({"i": j, "action": "snapped", "from": [start, end], "to": [new["start"], new["end"]], "text": stxt})
    return repaired, notes


def repair_parsed_records(src: list[dict], parsed) -> tuple[Any, list[dict]]:
    if not isinstance(parsed, dict) or not isinstance(parsed.get("records"), list):
        return parsed, []
    by_id = {r["id"]: r["text"] for r in src}
    notes = []
    recs = []
    for rec in parsed["records"]:
        if not isinstance(rec, dict):
            recs.append(rec)
            continue
        text = by_id.get(rec.get("id"))
        if text is None:
            recs.append(rec)
            continue
        new_spans, span_notes = repair_span_offsets(text, rec.get("spans") or [])
        recs.append({**rec, "spans": new_spans})
        if span_notes:
            notes.append({"id": rec.get("id"), "repairs": span_notes})
    out = dict(parsed)
    out["records"] = recs
    return out, notes


def validate_records(src: list[dict], parsed: Any) -> dict:
    issues: list[dict] = []
    by_id = {r["id"]: r["text"] for r in src}
    if not isinstance(parsed, dict):
        return {"ok": False, "n_errors": 1, "errors": [{"kind": "root", "msg": "not a JSON object"}]}
    recs = parsed.get("records")
    extra_top = sorted(k for k in parsed.keys() if k != "records")
    if extra_top:
        issues.append({"kind": "extra_top", "msg": extra_top})
    if not isinstance(recs, list):
        return {"ok": False, "n_errors": 1, "errors": [{"kind": "records", "msg": "records missing or not a list"}]}
    if len(recs) != len(src):
        issues.append({"kind": "count", "msg": f"got {len(recs)} records, expected {len(src)}"})
    for want, got in zip(src, recs):
        loc = want["id"]
        if not isinstance(got, dict):
            issues.append({"kind": "record", "id": loc, "msg": "not an object"})
            continue
        extra = sorted(set(got) - REC_KEYS)
        missing = sorted(REC_KEYS - set(got))
        if extra:
            issues.append({"kind": "extra_fields", "id": loc, "msg": extra})
        if missing:
            issues.append({"kind": "missing_fields", "id": loc, "msg": missing})
        if got.get("id") != want["id"]:
            issues.append({"kind": "id", "id": loc, "msg": got.get("id")})
        text = by_id[want["id"]]
        status = got.get("status")
        if status not in ALLOWED_STATUS:
            issues.append({"kind": "status", "id": loc, "msg": status})
        if not isinstance(got.get("note"), str):
            issues.append({"kind": "note", "id": loc, "msg": type(got.get("note")).__name__})
        spans = got.get("spans") if isinstance(got.get("spans"), list) else None
        if spans is None:
            issues.append({"kind": "spans", "id": loc, "msg": "not a list"})
            spans = []
        prev_end = -1
        last = None
        for j, sp in enumerate(spans):
            if not isinstance(sp, dict):
                issues.append({"kind": "span", "id": loc, "i": j, "msg": "not an object"})
                continue
            extra_s = sorted(set(sp) - SPAN_KEYS)
            missing_s = sorted(SPAN_KEYS - set(sp))
            if extra_s:
                issues.append({"kind": "span_extra", "id": loc, "i": j, "msg": extra_s})
            if missing_s:
                issues.append({"kind": "span_missing", "id": loc, "i": j, "msg": missing_s})
                continue
            try:
                start, end = int(sp["start"]), int(sp["end"])
            except (TypeError, ValueError):
                issues.append({"kind": "offset_type", "id": loc, "i": j, "msg": (sp.get("start"), sp.get("end"))})
                continue
            stxt = sp.get("text")
            lab = sp.get("label")
            if lab not in ALLOWED_LABEL:
                issues.append({"kind": "label", "id": loc, "i": j, "msg": lab})
            if not (0 <= start < end <= len(text)):
                issues.append({"kind": "offset_range", "id": loc, "i": j, "msg": (start, end, len(text))})
            elif text[start:end] != stxt:
                issues.append(
                    {"kind": "offset_mismatch", "id": loc, "i": j, "msg": {"got": stxt, "slice": text[start:end]}}
                )
            if last is not None and overlaps(last, {"start": start, "end": end}):
                issues.append({"kind": "overlap", "id": loc, "i": j, "msg": (last["start"], last["end"], start, end)})
            if start < prev_end:
                issues.append({"kind": "unsorted_or_nested", "id": loc, "i": j, "msg": (prev_end, start)})
            prev_end = max(prev_end, end)
            last = {"start": start, "end": end}
        iss = got.get("issues") if isinstance(got.get("issues"), list) else None
        if iss is None:
            issues.append({"kind": "issues", "id": loc, "msg": "not a list"})
            iss = []
        for k, it in enumerate(iss):
            if not isinstance(it, dict):
                issues.append({"kind": "issue_obj", "id": loc, "i": k, "msg": "not an object"})
                continue
            extra_i = sorted(set(it) - ISSUE_KEYS)
            missing_i = sorted(ISSUE_KEYS - set(it))
            if extra_i:
                issues.append({"kind": "issue_extra", "id": loc, "i": k, "msg": extra_i})
            if missing_i:
                issues.append({"kind": "issue_missing", "id": loc, "i": k, "msg": missing_i})
            if it.get("kind") not in ALLOWED_KIND:
                issues.append({"kind": "issue_kind", "id": loc, "i": k, "msg": it.get("kind")})
            if not isinstance(it.get("alternatives"), list):
                issues.append({"kind": "issue_alts", "id": loc, "i": k, "msg": type(it.get("alternatives")).__name__})
        if status == "confirmed_empty" and spans:
            issues.append({"kind": "empty_inconsistent", "id": loc, "msg": "confirmed_empty has spans"})
        if status == "candidate_complete" and not spans:
            issues.append({"kind": "complete_inconsistent", "id": loc, "msg": "candidate_complete has no spans"})
        if status == "candidate_complete" and iss:
            issues.append({"kind": "complete_has_issues", "id": loc, "msg": len(iss)})
        if status == "adjudication_required" and not iss:
            issues.append({"kind": "adj_no_issues", "id": loc, "msg": "adjudication_required but issues=[]"})
        if status == "confirmed_empty" and iss:
            issues.append({"kind": "empty_has_issues", "id": loc, "msg": len(iss)})
    return {"ok": not issues, "n_errors": len(issues), "errors": issues}


def post_chat(
    key: str,
    system: str,
    user: str,
    model: str = REQUEST_MODEL,
    base: str = DEFAULT_BASE,
    timeout: int = 240,
    max_tokens: int = 8192,
    temperature: float = 0.0,
) -> tuple[int | None, dict, float, str | None]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(base.rstrip("/") + "/v1/chat/completions", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    t0 = time.time()
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return resp.status, body, time.time() - t0, None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"raw": raw[:4000]}
        return e.code, parsed, time.time() - t0, "http_error"
    except Exception as e:
        return None, {"error": str(e)}, time.time() - t0, type(e).__name__


def assistant_content(body: dict) -> tuple[str, str | None]:
    choices = body.get("choices") or []
    if not choices:
        return "", None
    msg = choices[0].get("message") or {}
    return msg.get("content") or "", choices[0].get("finish_reason")


def spans_to_bio(text: str, spans: list[dict]) -> tuple[list[str], list[list]]:
    tokens = list(text)
    tags = ["O"] * len(tokens)
    triples = []
    for sp in spans or []:
        start, end, lab = int(sp["start"]), int(sp["end"]), str(sp["label"])
        if not (0 <= start < end <= len(tokens)):
            raise ValueError(f"bad span {[start, end, lab]}")
        if any(t != "O" for t in tags[start:end]):
            raise ValueError(f"overlap at {[start, end, lab]}")
        tags[start] = f"B-{lab}"
        for i in range(start + 1, end):
            tags[i] = f"I-{lab}"
        triples.append([start, end, lab])
    return tags, triples


def to_student_row(src: dict, rec: dict) -> dict:
    text = src["text"]
    tags, triples = spans_to_bio(text, rec.get("spans") or [])
    return {
        "id": src["id"],
        "sentence": text,
        "tokens": list(text),
        "spans": triples,
        "list_of_selection_bio4": tags,
        "status": rec.get("status"),
        "note": rec.get("note"),
        "issues": rec.get("issues") or [],
        "source_domain": src.get("source_domain"),
        "source_file": src.get("source_file"),
        "nfc_sha1": src.get("nfc_sha1"),
        "prompt_id": PROMPT_ID,
        "model": REQUEST_MODEL,
        "condition": "b2",
        "split": None,
        "not_gold": True,
    }
