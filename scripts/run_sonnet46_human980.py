#!/usr/bin/env python3
"""Round-1 SOP labels for human980 with claude-sonnet-4-6.

Input = rule_v4 prelabel. Output is for human review (Doccano), not Gold v2.
Does not overwrite gold_canonical_v2.jsonl, train.json, or rule_v4 source files.
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
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PACK = PAPER / "reports/sandbox_lskt_v4_silver/human980_pack"
PROMPT = (PACK / "PROMPT_sonnet46.txt").read_text(encoding="utf-8")
SRC = PACK / "doccano/human980.jsonl"
OUT = PACK / "sonnet46_round1"
KEY_PATH = Path.home() / ".config/ysaikeji/api_key"
BASE = "https://claudeplus.ysaikeji.cn"
MODEL = "claude-sonnet-4-6"
CTX = ssl.create_default_context()
BATCH = 8
TYPES = {"L", "K", "S", "T"}
USER_PREFIX = (
    "请纠正下面这一批规则银标。只输出 JSON 数组，不要 markdown。"
    "id 必须与输入完全一致、顺序一致、不增不删。"
    "text 必须是 sentence 的连续原文子串。\n"
)


def load_key() -> str:
    key = (os.environ.get("YSAIKEJI_API_KEY") or "").strip()
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
        if typ not in TYPES or not (0 <= a < b <= len(text)):
            continue
        out.append({"text": text[a:b], "type": typ})
    return out


def locate_span(sentence: str, text: str) -> tuple[int, int] | None:
    t = (text or "").strip()
    if not t:
        return None
    i = sentence.find(t)
    if i >= 0:
        return i, i + len(t)
    compact = re.sub(r"\s+", "", t)
    if compact and compact != t:
        j = sentence.find(compact)
        if j >= 0:
            return j, j + len(compact)
    return None


def flatten(spans: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    kept: list[tuple[int, int, str]] = []
    for a, b, t in sorted(spans, key=lambda x: (x[0], x[1], x[2])):
        if kept and a < kept[-1][1]:
            continue
        kept.append((a, b, t))
    return kept


def extract_json_array(raw: str) -> list:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\[.*\]", text, re.S)
        if not m:
            raise
        blob = m.group(0)
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            blob2 = re.sub(r'("comment"\s*:\s*")(.*?)("\s*})', lambda mm: mm.group(1) + mm.group(2).replace('"', "「") + mm.group(3), blob, flags=re.S)
            data = json.loads(blob2)
    if isinstance(data, dict):
        for k in ("results", "items", "data", "annotations"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
        else:
            raise ValueError("json_object_without_array")
    if not isinstance(data, list):
        raise ValueError("not_a_list")
    return data


def parse_results(raw: str, expected_ids: list[str]) -> list[dict]:
    data = extract_json_array(raw)
    rows = []
    for item in data:
        if not isinstance(item, dict):
            continue
        spans = []
        for sp in item.get("spans") or []:
            if not isinstance(sp, dict):
                continue
            typ = str(sp.get("type") or "").strip().upper()[:1]
            txt = str(sp.get("text") or "").strip()
            if txt and typ in TYPES:
                spans.append({"text": txt, "type": typ})
        rows.append(
            {
                "id": str(item.get("id") or "").strip(),
                "spans": spans,
                "comment": str(item.get("comment") or ""),
            }
        )
    if len(rows) == len(expected_ids):
        for rec, cid in zip(rows, expected_ids):
            rec["id"] = cid
        return rows
    by_id = {r["id"]: r for r in rows if r["id"]}
    out = []
    for cid in expected_ids:
        out.append(by_id.get(cid) or {"id": cid, "spans": [], "comment": "missing_in_model_output"})
    return out


def chat(key: str, payload: list[dict], timeout: int = 180) -> tuple[int | None, str, str | None]:
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": USER_PREFIX + json.dumps(payload, ensure_ascii=False)},
        ],
        "temperature": 0,
        "max_tokens": 8192,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            parsed = json.loads(resp.read().decode("utf-8"))
            content = (((parsed.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
            return resp.status, content, None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace") if e.fp else ""
        return e.code, "", raw[:800]
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"


def to_doccano(cid: str, sentence: str, labels: list, meta: dict) -> dict:
    return {
        "id": cid,
        "text": sentence,
        "label": labels,
        "labels": labels,
        "meta": meta,
    }


def fmt_spans(spans: list[dict]) -> str:
    if not spans:
        return "[]"
    return " | ".join(f"{s['text']}/{s['type']}" for s in spans)


def main() -> int:
    key = load_key()
    src_rows = []
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                src_rows.append(json.loads(line))
    payloads = []
    for rec in src_rows:
        meta = rec.get("meta") or {}
        cid = str(rec.get("id") or meta.get("id") or "").strip()
        text = rec.get("text") or rec.get("sentence") or ""
        payloads.append(
            {
                "id": cid,
                "sentence": text,
                "domain": meta.get("source_domain") or "",
                "spans": char_to_text_spans(text, rec.get("labels") or rec.get("label") or []),
                "_src_meta": meta,
            }
        )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "raw").mkdir(exist_ok=True)
    (OUT / "prompt_used.txt").write_text(PROMPT, encoding="utf-8")
    done_path = OUT / "records.jsonl"
    done: dict[str, dict] = {}
    if done_path.is_file():
        for line in done_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done[str(rec["id"])] = rec
    pending = [p for p in payloads if p["id"] not in done]
    print(
        json.dumps(
            {"n": len(payloads), "done": len(done), "pending": len(pending), "batch": BATCH, "model": MODEL},
            ensure_ascii=False,
        ),
        flush=True,
    )
    with done_path.open("a", encoding="utf-8") as fout:
        for b in range(0, len(pending), BATCH):
            chunk = pending[b : b + BATCH]
            ids = [c["id"] for c in chunk]
            send = [{"id": c["id"], "sentence": c["sentence"], "domain": c["domain"], "spans": c["spans"]} for c in chunk]
            parsed = None
            last_err = None
            raw_text = ""
            for attempt in range(5):
                code, raw_text, err = chat(key, send)
                if code != 200 or not (raw_text or "").strip():
                    last_err = err or f"http_{code}"
                    time.sleep(1 + attempt)
                    continue
                try:
                    parsed = parse_results(raw_text, ids)
                    if any(r.get("comment") == "missing_in_model_output" for r in parsed):
                        raise ValueError("missing_ids")
                    last_err = None
                    break
                except Exception as e:
                    last_err = f"{type(e).__name__}: {e}"
                    time.sleep(1 + attempt)
            (OUT / "raw" / f"batch_{b:04d}.txt").write_text(raw_text or (last_err or ""), encoding="utf-8")
            if parsed is None:
                print(json.dumps({"batch_start": b, "error": last_err, "ids": ids}), flush=True)
                continue
            for src, hit in zip(chunk, parsed):
                sentence = src["sentence"]
                aligned = []
                miss = []
                for sp in hit["spans"]:
                    loc = locate_span(sentence, sp["text"])
                    if loc is None:
                        miss.append(sp["text"])
                    else:
                        aligned.append((loc[0], loc[1], sp["type"]))
                aligned = flatten(aligned)
                labels = [[a, b, t] for a, b, t in aligned]
                text_spans = [{"text": sentence[a:b], "type": t} for a, b, t in aligned]
                row = {
                    "id": src["id"],
                    "sentence": sentence,
                    "domain": src["domain"],
                    "rule_v4": src["spans"],
                    "spans": text_spans,
                    "labels": labels,
                    "comment": hit.get("comment") or "",
                    "unaligned": miss,
                    "model": MODEL,
                    "prelabel": "sonnet46_round1",
                    "do_not_train": True,
                    "source_meta": src["_src_meta"],
                }
                fout.write(json.dumps(row, ensure_ascii=False) + "\n")
                fout.flush()
                done[src["id"]] = row
            print(json.dumps({"wrote": min(b + len(chunk), len(pending)), "of": len(pending), "unaligned_in_batch": sum(len(r.get("unaligned") or []) for r in [done[i] for i in ids])}), flush=True)
            time.sleep(0.2)
    if any(p["id"] not in done for p in payloads):
        missing = [p["id"] for p in payloads if p["id"] not in done]
        print(json.dumps({"incomplete": True, "missing_n": len(missing), "missing_head": missing[:10]}), flush=True)
        return 1
    ordered = [done[p["id"]] for p in payloads]
    docc = []
    ws = []
    n_empty = 0
    n_unaligned = 0
    types = Counter()
    for rec in ordered:
        if not rec["spans"]:
            n_empty += 1
        if rec.get("unaligned"):
            n_unaligned += 1
        for sp in rec["spans"]:
            types[sp["type"]] += 1
        meta = dict(rec.get("source_meta") or {})
        meta.update(
            {
                "id": rec["id"],
                "prelabel": "sonnet46_round1",
                "sandbox": "human980_sop_v4",
                "do_not_train": True,
                "rule_v4": fmt_spans(rec.get("rule_v4") or []),
                "unaligned": rec.get("unaligned") or [],
                "sonnet_comment": rec.get("comment") or "",
                "status": "todo_human_review",
            }
        )
        docc.append(to_doccano(rec["id"], rec["sentence"], rec["labels"], meta))
        ws.append(
            {
                "id": rec["id"],
                "status": "todo",
                "source_domain": rec["domain"],
                "sentence": rec["sentence"],
                "prelabel_rule_v4": fmt_spans(rec.get("rule_v4") or []),
                "prelabel_sonnet46": fmt_spans(rec["spans"]),
                "unaligned": " | ".join(rec.get("unaligned") or []),
                "comment": rec.get("comment") or "",
                "human_spans": "",
            }
        )
    write_jsonl = lambda path, rows: path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    write_jsonl(OUT / "doccano_sonnet46.jsonl", docc)
    (OUT / "batches").mkdir(exist_ok=True)
    for i in range(0, len(docc), 50):
        write_jsonl(OUT / "batches" / f"batch_{i // 50 + 1:02d}.jsonl", docc[i : i + 50])
    import csv

    fields = ["id", "status", "source_domain", "sentence", "prelabel_rule_v4", "prelabel_sonnet46", "unaligned", "comment", "human_spans"]
    with (OUT / "worksheet_review.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(ws)
    summary = {
        "n": len(ordered),
        "n_empty": n_empty,
        "n_with_unaligned": n_unaligned,
        "n_spans": sum(len(r["spans"]) for r in ordered),
        "types": dict(types),
        "model": MODEL,
        "base": BASE,
        "prompt": str(PACK / "PROMPT_sonnet46.txt"),
        "doccano": str(OUT / "doccano_sonnet46.jsonl"),
        "start_human": str(OUT / "batches/batch_01.jsonl"),
        "gold_v2_untouched": True,
        "do_not_train": True,
        "not_for_confirmed_results": True,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    review = f"""# Sonnet 4.6 第一轮 → 人工复核

预标已换成 **claude-sonnet-4-6**（SOP v4）。这不是 Gold，不要写入训练集。

1. 读 `../GUIDELINES.md`。
2. Doccano 导入 `labels.json`（仍用 `../doccano/labels.json`）。
3. 先导入 `{OUT / "batches/batch_01.jsonl"}`（50 句），改跨度。
4. 全量：`doccano_sonnet46.jsonl`。
5. 或填 `worksheet_review.csv` 的 `human_spans`。

`unaligned` 非空的句子是模型写了对不上原文的片段（已丢掉），请重点看。
"""
    (OUT / "REVIEW.md").write_text(review, encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
