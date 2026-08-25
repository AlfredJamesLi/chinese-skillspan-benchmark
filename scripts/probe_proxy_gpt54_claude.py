#!/usr/bin/env python3
"""Smoke-test whether the current ysaikeji proxy can call gpt-5.4 and Claude.

One sentence only. Does not overwrite dumps or start 2601 inference.
"""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
KEY_PATH = Path.home() / ".config/ysaikeji/api_key"
OUT = PAPER / "reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100/proxy_smoke_gpt54_claude.json"
PROMPT = (
    PAPER / "reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100/PROMPT_gpt4o_sop_extract.txt"
).read_text(encoding="utf-8")
BASES = [
    (os.environ.get("YSAIKEJI_BASE") or "https://claudeed.ysaikeji.cn").rstrip("/"),
]
MODELS = [
    "gpt-5.4",
    "claude-haiku-4-5",
    "claude-3-5-haiku-20241022",
    "claude-sonnet-4-6",
]
SENT = "熟悉 Python 和英语六级，沟通能力强。"
PAYLOAD = [{"id": "smoke-1", "sentence": SENT}]
USER = (
    "请从下面这一批句子抽出 LSKT 跨度。只输出 JSON 数组，不要 markdown。"
    "id 必须与输入完全一致、顺序一致、不增不删。"
    "text 必须是 sentence 的连续原文子串。不要参考银标或 Gold。\n"
)
CTX = ssl.create_default_context()


def load_key() -> str:
    key = (os.environ.get("YSAIKEJI_API_KEY") or "").strip()
    if key.startswith("sk-") and len(key) >= 20:
        return key
    if KEY_PATH.is_file():
        key = KEY_PATH.read_text(encoding="utf-8").strip()
        if key.startswith("sk-") and len(key) >= 20:
            return key
    raise SystemExit("missing YSAIKEJI_API_KEY or ~/.config/ysaikeji/api_key")


def unique_bases() -> list[str]:
    out = []
    for b in BASES:
        if b and b not in out:
            out.append(b)
    return out


def chat(key: str, base: str, model: str, timeout: int = 40) -> dict:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": USER + json.dumps(PAYLOAD, ensure_ascii=False)},
        ],
        "max_tokens": 512,
        "temperature": 0,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(base + "/v1/chat/completions", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    t0 = time.time()
    rec = {"base": base, "model": model, "ok": False, "status": None, "elapsed_s": None, "upstream": None, "preview": "", "err": None}
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            parsed = json.loads(resp.read().decode("utf-8"))
            content = (((parsed.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
            rec.update(
                {
                    "ok": bool(str(content).strip()),
                    "status": resp.status,
                    "elapsed_s": round(time.time() - t0, 2),
                    "upstream": parsed.get("model"),
                    "preview": str(content)[:400],
                }
            )
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace") if e.fp else ""
        rec.update({"status": e.code, "elapsed_s": round(time.time() - t0, 2), "err": raw[:800]})
    except Exception as e:
        rec.update({"elapsed_s": round(time.time() - t0, 2), "err": f"{type(e).__name__}: {e}"})
    return rec


def main() -> int:
    key = load_key()
    rows = []
    for base in unique_bases():
        for model in MODELS:
            rec = chat(key, base, model)
            rows.append(rec)
            print(json.dumps({"base": base, "model": model, "ok": rec["ok"], "status": rec["status"]}, ensure_ascii=False), flush=True)
    usable = [r for r in rows if r["ok"]]
    out = {
        "prompt": "SOP extract v4, 1 sentence, no gold",
        "n_ok": len(usable),
        "usable": [{"base": r["base"], "model": r["model"], "upstream": r["upstream"]} for r in usable],
        "calls": rows,
        "note": "Connectivity smoke only. Not a 2601 run. Do not overwrite frozen dumps.",
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(OUT), "n_ok": out["n_ok"], "usable": out["usable"]}, ensure_ascii=False), flush=True)
    return 0 if usable else 2


if __name__ == "__main__":
    raise SystemExit(main())
