#!/usr/bin/env python3
"""10-sentence smoke test for silver_public_api_v1.0 on gpt-6-astra.

Does not label the full 7,936 pool. Does not rewrite Gold150 / V4 / paper counts.
"""
from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
WORK = PAPER / "data/silver_plus_10k_prep_20260913/annotation_input/work.jsonl"
PROMPT = PAPER / "silver_prompt.txt"
OUT = PAPER / "data/silver_plus_10k_prep_20260913/pilot10_public_api_v1"
KEY_FILE = Path.home() / ".config/ysaikeji/api_key"
BASE = "https://claudeed.ysaikeji.cn"
REQUEST_MODEL = "gpt-6-astra"
PROMPT_ID = "silver_public_api_v1.0"
N = 10
ALLOWED_STATUS = {"candidate_complete", "confirmed_empty", "adjudication_required"}
ALLOWED_LABEL = {"L", "K", "S", "T"}
ALLOWED_KIND = {"scope", "boundary", "type"}
REC_KEYS = {"id", "spans", "status", "note", "issues"}
SPAN_KEYS = {"start", "end", "text", "label"}
ISSUE_KEYS = {"kind", "text", "alternatives", "reason"}


def load_key() -> str:
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key.startswith("sk-") or len(key) < 20:
        raise SystemExit("API key file missing or malformed")
    return key


def load_records() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    with WORK.open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= N:
                break
            rows.append(json.loads(line))
    if len(rows) != N:
        raise SystemExit(f"expected {N} rows, got {len(rows)}")
    payload = [{"id": r["id"], "text": r["text"]} for r in rows]
    return rows, payload


def extract_json(text: str):
    raw = (text or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        if raw.endswith("```"):
            raw = raw[: raw.rfind("```")].rstrip()
        if raw.startswith("json"):
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


def post_chat(key: str, system: str, user: str, timeout: int = 240):
    payload = {
        "model": REQUEST_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 8192,
        "temperature": 0,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=data, method="POST")
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


def overlaps(a: dict, b: dict) -> bool:
    return not (a["end"] <= b["start"] or b["end"] <= a["start"])


def validate(src: list[dict], parsed) -> dict:
    issues: list[dict] = []
    by_id = {r["id"]: r["text"] for r in src}
    if not isinstance(parsed, dict):
        return {"ok": False, "errors": [{"kind": "root", "msg": "not a JSON object"}]}
    recs = parsed.get("records")
    extra_top = sorted(k for k in parsed.keys() if k != "records")
    if extra_top:
        issues.append({"kind": "extra_top", "msg": extra_top})
    if not isinstance(recs, list):
        return {"ok": False, "errors": [{"kind": "records", "msg": "records missing or not a list"}]}
    if len(recs) != len(src):
        issues.append({"kind": "count", "msg": f"got {len(recs)} records, expected {len(src)}"})
    for i, (want, got) in enumerate(zip(src, recs)):
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
        note = got.get("note")
        if not isinstance(note, str):
            issues.append({"kind": "note", "id": loc, "msg": type(note).__name__})
        spans = got.get("spans")
        if not isinstance(spans, list):
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
                    {
                        "kind": "offset_mismatch",
                        "id": loc,
                        "i": j,
                        "msg": {"got": stxt, "slice": text[start:end]},
                    }
                )
            if last is not None and overlaps(last, {"start": start, "end": end}):
                issues.append({"kind": "overlap", "id": loc, "i": j, "msg": (last, start, end)})
            if start < prev_end:
                issues.append({"kind": "unsorted_or_nested", "id": loc, "i": j, "msg": (prev_end, start)})
            prev_end = max(prev_end, end)
            last = {"start": start, "end": end}
        iss = got.get("issues")
        if not isinstance(iss, list):
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


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    key = load_key()
    src, payload = load_records()
    system = PROMPT.read_text(encoding="utf-8").strip()
    user = json.dumps({"records": payload}, ensure_ascii=False)
    (OUT / "input.json").write_text(json.dumps({"records": payload}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "source_rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in src), encoding="utf-8")

    status, body, elapsed, err = post_chat(key, system, user)
    content = ""
    choices = (body.get("choices") if isinstance(body, dict) else None) or []
    if choices:
        content = (choices[0].get("message") or {}).get("content") or ""
    parsed, parse_note = extract_json(content)
    val = validate(payload, parsed) if parsed is not None else {"ok": False, "n_errors": 1, "errors": [{"kind": "parse", "msg": parse_note}]}

    raw_out = {
        "at": datetime.now(timezone.utc).isoformat(),
        "endpoint": BASE + "/v1/chat/completions",
        "requested_model": REQUEST_MODEL,
        "prompt_id": PROMPT_ID,
        "prompt_path": str(PROMPT),
        "n": N,
        "ids": [r["id"] for r in src],
        "http_status": status,
        "elapsed_s": round(elapsed, 3),
        "error_tag": err,
        "response_model": body.get("model") if isinstance(body, dict) else None,
        "usage": body.get("usage") if isinstance(body, dict) else None,
        "finish_reason": (choices[0].get("finish_reason") if choices else None),
        "assistant_content": content,
        "api_error": body.get("error") if isinstance(body, dict) else None,
        "parse_note": parse_note,
        "validation": val,
    }
    (OUT / "raw_meta.json").write_text(json.dumps(raw_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if parsed is not None:
        (OUT / "parsed.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("http_status", status)
    print("elapsed_s", round(elapsed, 3))
    print("response_model", raw_out["response_model"])
    print("finish_reason", raw_out["finish_reason"])
    print("usage", raw_out["usage"])
    print("parse_ok", parsed is not None, parse_note)
    print("validation_ok", val.get("ok"), "n_errors", val.get("n_errors"))
    if val.get("errors"):
        print("errors", json.dumps(val["errors"][:20], ensure_ascii=False)[:4000])
    if parsed and isinstance(parsed.get("records"), list):
        for rec, src_rec in zip(parsed["records"], src):
            text = src_rec["text"]
            print("---")
            print(rec.get("id"), rec.get("status"))
            print("TEXT:", text)
            for sp in rec.get("spans") or []:
                print(f"  [{sp.get('start')}:{sp.get('end')}] {sp.get('label')} {sp.get('text')!r}")
            print("NOTE:", rec.get("note"))
            if rec.get("issues"):
                print("ISSUES:", json.dumps(rec["issues"], ensure_ascii=False))
    print("saved", OUT)
    return 0 if status == 200 and val.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
