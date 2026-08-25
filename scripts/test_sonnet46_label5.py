#!/usr/bin/env python3
"""Smoke-test claude-sonnet-4-6 on 5 human980 sentences with SOP v4 prompt.

Does not overwrite Gold v2, train.json, or the 980 pack source files.
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
from expand_goldstyle_train import apply_text_spans  # noqa: E402

PACK = PAPER / "reports/sandbox_lskt_v4_silver/human980_pack"
PROMPT = (PACK / "PROMPT_sonnet46.txt").read_text(encoding="utf-8")
SRC = PACK / "doccano/batches/batch_01.jsonl"
OUT = PACK / "sonnet46_smoke"
KEY_PATH = Path.home() / ".config/ysaikeji/api_key"
BASE = "https://claudeplus.ysaikeji.cn"
MODEL = "claude-sonnet-4-6"
CTX = ssl.create_default_context()
N = 5


def load_key() -> str:
    for raw in (os.environ.get("YSAIKEJI_API_KEY") or "",):
        key = raw.strip()
        if key.startswith("sk-") and len(key) >= 20:
            return key
    if KEY_PATH.is_file():
        key = KEY_PATH.read_text(encoding="utf-8").strip()
        if key.startswith("sk-") and len(key) >= 20:
            return key
    raise SystemExit("missing YSAIKEJI_API_KEY or ~/.config/ysaikeji/api_key")


def char_to_text_spans(text: str, labels: list) -> list[dict]:
    out = []
    for item in labels or []:
        if not isinstance(item, (list, tuple)) or len(item) < 3:
            continue
        a, b, typ = int(item[0]), int(item[1]), str(item[2]).strip().upper()[:1]
        if typ not in {"L", "K", "S", "T"} or not (0 <= a < b <= len(text)):
            continue
        out.append({"text": text[a:b], "type": typ})
    return out


def parse_results(raw: str) -> list[dict]:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    data = json.loads(text)
    if isinstance(data, dict):
        for k in ("results", "items", "data", "annotations"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
        else:
            raise ValueError("json_object_without_array")
    if not isinstance(data, list):
        raise ValueError("not_a_list")
    out = []
    for item in data:
        if not isinstance(item, dict) or "id" not in item:
            continue
        spans = []
        for sp in item.get("spans") or []:
            if not isinstance(sp, dict):
                continue
            spans.append(
                {
                    "text": str(sp.get("text") or "").strip(),
                    "type": str(sp.get("type") or "").strip().upper()[:1],
                }
            )
        out.append(
            {
                "id": str(item["id"]).strip(),
                "spans": [s for s in spans if s["text"] and s["type"] in {"L", "K", "S", "T"}],
                "comment": str(item.get("comment") or ""),
            }
        )
    return out


def chat(key: str, payload: list[dict]) -> tuple[int | None, str, str | None]:
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": PROMPT},
            {
                "role": "user",
                "content": "请纠正下面这一批规则银标。只输出 JSON 数组。\n"
                + json.dumps(payload, ensure_ascii=False),
            },
        ],
        "temperature": 0,
        "max_tokens": 4096,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120, context=CTX) as resp:
            parsed = json.loads(resp.read().decode("utf-8"))
            content = (((parsed.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
            return resp.status, content, None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace") if e.fp else ""
        return e.code, "", raw[:800]
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"


def gold_like(rec: dict) -> dict:
    return {
        "id": rec["id"],
        "sentence": rec["sentence"],
        "tokens": list(rec["sentence"]),
    }


def main() -> int:
    key = load_key()
    rows = []
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
                if len(rows) >= N:
                    break
    payload = []
    for rec in rows:
        text = rec.get("text") or ""
        meta = rec.get("meta") or {}
        payload.append(
            {
                "id": rec.get("id") or meta.get("id"),
                "sentence": text,
                "domain": meta.get("source_domain") or "",
                "spans": char_to_text_spans(text, rec.get("labels") or rec.get("label") or []),
            }
        )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prompt_used.txt").write_text(PROMPT, encoding="utf-8")
    (OUT / "input5.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("===== PROMPT START =====")
    print(PROMPT.rstrip())
    print("===== PROMPT END =====")
    print(json.dumps({"n": len(payload), "ids": [r["id"] for r in payload], "model": MODEL, "base": BASE}, ensure_ascii=False))
    t0 = time.time()
    code, text, err = chat(key, payload)
    elapsed = round(time.time() - t0, 2)
    (OUT / "raw_output.txt").write_text(text or (err or ""), encoding="utf-8")
    if err or code != 200 or not (text or "").strip():
        print(json.dumps({"http": code, "error": err or "empty", "sec": elapsed}, ensure_ascii=False))
        return 1
    parsed = parse_results(text)
    by_id = {r["id"]: r for r in parsed}
    aligned = []
    for rec in payload:
        cid = rec["id"]
        hit = by_id.get(cid) or {"id": cid, "spans": [], "comment": "missing_in_model_output"}
        tags, miss = apply_text_spans(gold_like(rec), hit["spans"])
        aligned.append(
            {
                "id": cid,
                "sentence": rec["sentence"],
                "domain": rec["domain"],
                "rule_v4": rec["spans"],
                "sonnet46": hit["spans"],
                "comment": hit.get("comment") or "",
                "unaligned": miss,
                "n_non_o": sum(1 for t in tags if t != "O"),
            }
        )
    (OUT / "aligned5.json").write_text(json.dumps(aligned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"http": code, "sec": elapsed, "n_out": len(parsed), "path": str(OUT / "aligned5.json")}, ensure_ascii=False))
    print(json.dumps(aligned, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
