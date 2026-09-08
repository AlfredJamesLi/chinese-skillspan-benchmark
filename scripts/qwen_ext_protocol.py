#!/usr/bin/env python3
"""Shared Qwen extension protocol: JSON-offset LSKT, not a full SpanAnchor reproduction."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from typing import Any

TYPES = {"L", "K", "S", "T"}
JSON_ARR = re.compile(r"\[[\s\S]*?\]")
SYS = (
    "从中文招聘句子中抽取能力跨度。类型只能是 L（语言）、K（知识）、S（技能）、T（特质/软技能）。"
    "只输出一个 JSON 数组，元素为 {\"start\":整数,\"end\":整数,\"type\":\"S\"}。"
    "偏移是原文 Unicode 码点，0 起始、左闭右开。不要改写招聘原文。"
    "同一短语多次出现时必须给出该次出现的确定偏移。没有跨度则输出 []。"
)
PROTOCOL_ID = "qwen_lskt_spananchor_inspired_json_offset_v1"
K_DEMOS = 3
MAX_NEW_TOKENS = 256


def nfc_key(text: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFC", text or ""))


def load_jsonl(path) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                rows.append(json.loads(ln))
    return rows


def dump_jsonl(path, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def spans_to_payload(spans: list) -> list[dict]:
    out = []
    for item in spans or []:
        if isinstance(item, dict):
            a, b, t = int(item["start"]), int(item["end"]), str(item.get("type") or "").upper()
        else:
            a, b, t = int(item[0]), int(item[1]), str(item[2]).upper()
        out.append({"start": a, "end": b, "type": t})
    return out


def find_all_occurrences(sentence: str, phrase: str) -> list[tuple[int, int]]:
    if not sentence or not phrase:
        return []
    out = []
    start = 0
    while True:
        i = sentence.find(phrase, start)
        if i < 0:
            return out
        out.append((i, i + len(phrase)))
        start = i + 1


def resolve_surface(sentence: str, phrase: str, used: set[tuple[int, int]]) -> tuple[int, int] | None:
    """Left-to-right first unused occurrence. Never uses Gold to pick a match."""
    for a, b in find_all_occurrences(sentence, phrase):
        if (a, b) not in used:
            used.add((a, b))
            return a, b
    return None


def parse_spans(text: str, sentence: str) -> tuple[list[list], dict]:
    """Parse model output. Unparseable rows are kept; spans may be empty."""
    n = len(sentence or "")
    report: dict[str, Any] = {
        "parse_status": "ok",
        "n_raw_items": 0,
        "n_kept": 0,
        "n_dropped_invalid": 0,
        "n_surface_resolved": 0,
        "n_unresolvable": 0,
        "failures": [],
    }
    raw_text = text or ""
    m = JSON_ARR.search(raw_text)
    if not m:
        report["parse_status"] = "no_json"
        report["failures"].append("no_json_array")
        return [], report
    try:
        raw = json.loads(m.group(0))
    except json.JSONDecodeError:
        report["parse_status"] = "bad_json"
        report["failures"].append("json_decode_error")
        return [], report
    if not isinstance(raw, list):
        report["parse_status"] = "not_list"
        report["failures"].append("root_not_list")
        return [], report

    used: set[tuple[int, int]] = set()
    out: list[list] = []
    for i, item in enumerate(raw):
        report["n_raw_items"] += 1
        if not isinstance(item, dict):
            report["n_dropped_invalid"] += 1
            report["failures"].append(f"item_{i}_not_object")
            continue
        t = str(item.get("type") or "").strip().upper()
        if t not in TYPES:
            report["n_dropped_invalid"] += 1
            report["failures"].append(f"item_{i}_bad_type")
            continue
        a = item.get("start")
        b = item.get("end")
        if a is not None and b is not None:
            try:
                a_i, b_i = int(a), int(b)
            except (TypeError, ValueError):
                report["n_dropped_invalid"] += 1
                report["failures"].append(f"item_{i}_bad_offset")
                continue
            if 0 <= a_i < b_i <= n:
                out.append([a_i, b_i, t])
                used.add((a_i, b_i))
                report["n_kept"] += 1
                continue
            report["n_dropped_invalid"] += 1
            report["failures"].append(f"item_{i}_offset_oob")
            continue
        phrase = item.get("text") or item.get("span") or item.get("surface")
        if isinstance(phrase, str) and phrase:
            resolved = resolve_surface(sentence, phrase, used)
            if resolved:
                out.append([resolved[0], resolved[1], t])
                report["n_kept"] += 1
                report["n_surface_resolved"] += 1
            else:
                report["n_unresolvable"] += 1
                report["failures"].append(f"item_{i}_surface_unresolved:{phrase[:40]}")
            continue
        report["n_dropped_invalid"] += 1
        report["failures"].append(f"item_{i}_missing_offset_and_surface")
    if report["parse_status"] == "ok" and report["n_raw_items"] and not report["n_kept"]:
        report["parse_status"] = "all_items_invalid"
    return out, report


def to_bio(n: int, spans: list) -> list[str]:
    tags = ["O"] * n
    for a, b, t in spans:
        if a < 0 or b > n or a >= b:
            continue
        if any(tags[i] != "O" for i in range(a, b)):
            continue
        tags[a] = f"B-{t}"
        for i in range(a + 1, b):
            tags[i] = f"I-{t}"
    return tags


def format_example(sentence: str, spans: list) -> str:
    payload = json.dumps(spans_to_payload(spans), ensure_ascii=False)
    return f"句子：{sentence}\n输出：{payload}"


def user_prompt(sentence: str, demos: list[dict] | None = None) -> str:
    parts = [SYS]
    if demos:
        parts.append("以下是若干训练示例，格式与目标输出相同。不要复制与当前句无关的跨度。")
        for i, d in enumerate(demos, 1):
            parts.append(f"示例{i}：\n{format_example(d['sentence'], d.get('spans') or [])}")
    parts.append(f"句子：{sentence}\n输出：")
    return "\n".join(parts)


def chat_texts(tok, sentence: str, spans: list | None = None, demos: list[dict] | None = None):
    user = user_prompt(sentence, demos)
    if spans is None:
        messages = [{"role": "user", "content": user}]
        prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        return user, prompt, None
    payload = json.dumps(spans_to_payload(spans), ensure_ascii=False)
    messages = [
        {"role": "user", "content": user},
        {"role": "assistant", "content": payload},
    ]
    full = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    prompt = tok.apply_chat_template([{"role": "user", "content": user}], tokenize=False, add_generation_prompt=True)
    return user, prompt, full


def length_bucket(n_chars: int) -> int:
    if n_chars <= 20:
        return 0
    if n_chars <= 50:
        return 1
    if n_chars <= 100:
        return 2
    if n_chars <= 200:
        return 3
    return 4


def format_target(spans: list) -> str:
    return json.dumps(spans_to_payload(spans), ensure_ascii=False)


def build_user_prompt(sentence: str, demos: list[dict] | None = None) -> str:
    return user_prompt(sentence, demos)


def parse_model_output(raw: str, sentence: str) -> dict:
    if raw is None or not str(raw).strip():
        return {"spans": [], "status": "empty_output", "failures": [{"reason": "empty_output"}], "raw": raw or "", "report": {}}
    spans, report = parse_spans(raw, sentence)
    status = report.get("parse_status") or "ok"
    if status == "all_items_invalid" and any("offset_oob" in str(x) for x in report.get("failures") or []):
        status = "oob"
    return {
        "spans": spans,
        "status": status,
        "failures": report.get("failures") or [],
        "raw": raw,
        "report": report,
    }


def length_bin(n: int) -> int:
    return length_bucket(n)


def stable_int(*parts: object) -> int:
    h = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def pred_row(rid: str, sentence: str, parsed: dict, extra: dict | None = None) -> dict:
    return pred_record(rid, sentence, parsed.get("spans") or [], {"parse_status": parsed.get("status"), "failures": parsed.get("failures")}, extra)


def pred_record(row_id: str, sentence: str, spans: list, parse_report: dict, extra: dict | None = None) -> dict:
    rec = {
        "id": row_id,
        "sentence": sentence,
        "tokens": list(sentence),
        "list_of_selection_bio4": to_bio(len(sentence), spans),
        "pred_tags": to_bio(len(sentence), spans),
        "pred_spans": spans,
        "parse_status": parse_report.get("parse_status"),
        "parse_report": parse_report,
    }
    if extra:
        rec.update(extra)
    return rec
