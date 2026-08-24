#!/usr/bin/env python3
"""Label Gold-v2 test (52 batches) with official kimi-k2.6. Does not touch Gold v2 or Codex test."""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
from merge_codex_corrections import align_record, load_json, spans_to_bio, write_jsonl  # noqa: E402

PACK = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack"
B52 = PACK / "batches_52"
OUT = PACK / "outputs_kimi"
KEY_PATH = Path.home() / ".config/moonshot/api_key"
PROMPT = (B52 / "PROMPT_kimi.txt").read_text(encoding="utf-8")
TEMPLATE = PAPER / "data/test_lskt_v4_silver_g2ids.jsonl"
G2IDS_OUT = PAPER / "data/test_lskt_v4_kimi_g2ids.jsonl"
SOURCE = "kimi_k2.6_test52"
MODEL = "kimi-k2.6"
BASE = "https://api.moonshot.cn/v1"
CTX = ssl.create_default_context()


def load_key() -> str:
    key = KEY_PATH.read_text(encoding="utf-8").strip()
    if not key.startswith("sk-") or len(key) < 20:
        raise SystemExit(f"bad key file: {KEY_PATH}")
    return key


def compact_in(rec: dict) -> dict:
    return {
        "id": rec["id"],
        "sentence": rec.get("sentence") or "",
        "domain": rec.get("domain") or rec.get("source_domain") or "",
        "spans": rec.get("spans") or [],
    }


def parse_results(text: str) -> list[dict]:
    raw = (text or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    data = None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"(\{.*\}|\[.*\])", raw, re.S)
        if m:
            data = json.loads(m.group(1))
    if data is None:
        raise ValueError("no_json")
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
            spans.append({"text": str(sp.get("text") or "").strip(), "type": str(sp.get("type") or "").strip()})
        out.append({"id": str(item["id"]), "spans": spans, "comment": str(item.get("comment") or "")})
    return out


def chat(key: str, messages: list[dict], timeout: int = 180) -> tuple[int, dict | None, str | None]:
    body = {
        "model": MODEL,
        "messages": messages,
        "thinking": {"type": "disabled"},
        "response_format": {"type": "json_object"},
        "max_tokens": 32768,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE + "/chat/completions", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            parsed = json.loads(resp.read().decode("utf-8"))
            return resp.status, parsed, None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace") if e.fp else ""
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"_raw": raw[:800]}
        return e.code, parsed, None
    except Exception as e:
        return None, None, f"{type(e).__name__}: {e}"


def call_chunk(key: str, rows: list[dict], retries: int = 6) -> list[dict]:
    payload = [compact_in(r) for r in rows]
    user = (
        "请纠正下面这一批规则银标。输出 JSON 对象，键 results 为数组，"
        "数组长度必须等于输入句数，id 顺序与输入完全一致。\n"
        + json.dumps(payload, ensure_ascii=False)
    )
    messages = [
        {"role": "system", "content": PROMPT + "\n\n最终只输出 JSON 对象：{\"results\":[...]}。"},
        {"role": "user", "content": user},
    ]
    last_err = None
    for attempt in range(retries):
        st, body, err = chat(key, messages)
        if err:
            last_err = err
        elif st in (429, 500, 502, 503):
            last_err = f"http_{st}:{(body or {}).get('error')}"
        elif st != 200:
            last_err = f"http_{st}:{(body or {}).get('error')}"
        else:
            content = (((body or {}).get("choices") or [{}])[0].get("message") or {}).get("content") or ""
            try:
                parsed = parse_results(content)
            except Exception as e:
                last_err = f"parse:{e}"
                parsed = None
            if parsed is not None:
                by = {r["id"]: r for r in parsed}
                ordered = []
                missing = []
                for rec in rows:
                    rid = str(rec["id"])
                    if rid in by:
                        ordered.append(by[rid])
                    else:
                        missing.append(rid)
                if not missing:
                    return ordered
                last_err = f"missing_ids:{missing[:8]}"
                if len(rows) == 1:
                    return [{"id": str(rows[0]["id"]), "spans": [], "comment": "model_skipped"}]
        wait = min(60, 2 ** attempt)
        time.sleep(wait)
    raise RuntimeError(last_err or "call_failed")


def label_rows(key: str, rows: list[dict]) -> list[dict]:
    if len(rows) <= 12:
        return call_chunk(key, rows)
    try:
        return call_chunk(key, rows)
    except Exception:
        out = []
        for i in range(0, len(rows), 10):
            out.extend(call_chunk(key, rows[i : i + 10]))
            time.sleep(0.4)
        return out


def smoke(key: str) -> dict:
    rows = load_json(B52 / "batch_00.jsonl")[:2]
    labeled = call_chunk(key, rows)
    ok = [r["id"] for r in labeled] == [str(r["id"]) for r in rows]
    return {
        "ok": ok,
        "model": MODEL,
        "n": len(labeled),
        "ids": [r["id"] for r in labeled],
        "sample": labeled,
    }


def merge_all(raw_by_id: dict[str, dict]) -> dict:
    template = {str(r["id"]): r for r in load_json(TEMPLATE)}
    expected = []
    for b in range(52):
        expected.extend(str(r["id"]) for r in load_json(B52 / f"batch_{b:02d}.jsonl"))
    report = {
        "gold_v2_untouched": True,
        "codex_test_untouched": True,
        "source": SOURCE,
        "model": MODEL,
        "n_expected": len(expected),
        "n_raw": len(raw_by_id),
        "missing_ids": sorted(set(expected) - set(raw_by_id)),
        "n_empty": 0,
        "n_align_error_sents": 0,
        "n_dropped_spans": 0,
        "n_kept_spans": 0,
        "n_over_cap8": 0,
        "type_counts": {},
        "align_errors_head": [],
    }
    types: Counter[str] = Counter()
    out_rows = []
    compact = []
    all_results = []
    align_head: list[dict] = []
    for rid in expected:
        base = dict(template[rid])
        toks = [str(t) for t in (base.get("tokens") or list(base.get("sentence") or ""))]
        sent = base.get("sentence") or ""
        raw = raw_by_id[rid]
        spans, errs = align_record(toks, sent, raw.get("spans") or [])
        if errs:
            report["n_align_error_sents"] += 1
            report["n_dropped_spans"] += len(errs)
            if len(align_head) < 40:
                align_head.append({"id": rid, "n_errs": len(errs), "errs": errs[:8]})
        report["n_kept_spans"] += len(spans)
        if not spans:
            report["n_empty"] += 1
        for a, b, t in spans:
            types[t] += 1
            if b - a > 8:
                report["n_over_cap8"] += 1
        comment = raw.get("comment") or ""
        base["tokens"] = toks
        base["v4_spans"] = [[a, b, t] for a, b, t in spans]
        base["list_of_selection_bio4"] = spans_to_bio(len(toks), spans)
        base["v4_source"] = SOURCE
        base["comment"] = comment
        out_rows.append(base)
        compact.append(
            {
                "id": rid,
                "sentence": sent,
                "domain": base.get("source_domain") or "",
                "spans": [{"start": a, "end": b, "type": t, "text": "".join(toks[a:b])} for a, b, t in spans],
                "v4_source": SOURCE,
                "comment": comment,
            }
        )
        all_results.append({"id": rid, "spans": raw.get("spans") or [], "comment": comment})
    report["type_counts"] = dict(types)
    report["align_errors_head"] = align_head
    write_jsonl(G2IDS_OUT, out_rows)
    write_jsonl(PACK / "kimi_g2ids_compact.jsonl", compact)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "lskt_all_results.json").write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    report["output"] = str(G2IDS_OUT)
    md = [
        "# Kimi k2.6 test 52 merge (sandbox)",
        "",
        "Gold v2 untouched. Codex test silver untouched. Kimi written to a **new** file.",
        "",
        f"- model: `{MODEL}` thinking disabled",
        f"- n={report['n_expected']} raw={report['n_raw']} missing={len(report['missing_ids'])}",
        f"- align-error sentences: {report['n_align_error_sents']}",
        f"- kept spans {report['n_kept_spans']}, dropped {report['n_dropped_spans']}",
        f"- empty: {report['n_empty']}; spans>8 kept: {report['n_over_cap8']}",
        f"- types: {report['type_counts']}",
        "",
        f"Output: `{G2IDS_OUT}`",
        "Do not copy into confirmed-results.md. Do not train on this test file.",
        "",
    ]
    (PACK / "MERGE_kimi52.md").write_text("\n".join(md), encoding="utf-8")
    (PACK / "MERGE_kimi52.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def run_all(key: str) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    raw_by_id: dict[str, dict] = {}
    batch_status = []
    for b in range(52):
        out_path = OUT / f"batch_{b:02d}_corrected.json"
        gold_rows = load_json(B52 / f"batch_{b:02d}.jsonl")
        gold_ids = [str(r["id"]) for r in gold_rows]
        if out_path.is_file():
            labeled = load_json(out_path)
            got = [str(r["id"]) for r in labeled]
            if got == gold_ids:
                for rec in labeled:
                    raw_by_id[str(rec["id"])] = rec
                batch_status.append({"batch": b, "n": len(labeled), "cached": True})
                print(json.dumps({"batch": b, "cached": True, "n": len(labeled)}), flush=True)
                continue
        t0 = time.time()
        labeled = label_rows(key, gold_rows)
        out_path.write_text(json.dumps(labeled, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for rec in labeled:
            raw_by_id[str(rec["id"])] = rec
        batch_status.append({"batch": b, "n": len(labeled), "cached": False, "sec": round(time.time() - t0, 1)})
        print(json.dumps({"batch": b, "n": len(labeled), "sec": round(time.time() - t0, 1)}), flush=True)
        time.sleep(0.5)
    report = merge_all(raw_by_id)
    report["batches"] = batch_status
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    key = load_key()
    if args.smoke or not args.all:
        sm = smoke(key)
        print(json.dumps({"smoke": sm}, ensure_ascii=False, indent=2), flush=True)
        if not sm["ok"]:
            return 2
        if args.smoke and not args.all:
            return 0
    report = run_all(key)
    keep = (
        "gold_v2_untouched",
        "codex_test_untouched",
        "n_expected",
        "n_raw",
        "missing_ids",
        "n_empty",
        "n_align_error_sents",
        "n_dropped_spans",
        "n_kept_spans",
        "n_over_cap8",
        "type_counts",
        "output",
    )
    print(json.dumps({k: report[k] for k in keep}, ensure_ascii=False, indent=2), flush=True)
    return 0 if not report["missing_ids"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
