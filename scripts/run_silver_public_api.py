#!/usr/bin/env python3
"""Batch caller for silver_public_api_v1.0 on gpt-6-astra.

Resumes completed batches. Does not rewrite Gold150 / V4 / v6a / paper counts.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from silver_public_api_lib import (
    DEFAULT_BASE,
    PROMPT_ID,
    REQUEST_MODEL,
    assistant_content,
    dump_json,
    dump_jsonl,
    extract_json,
    load_jsonl,
    load_key,
    post_chat,
    repair_parsed_records,
    sample_by_domain,
    to_student_row,
    validate_records,
)

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
WORK = PAPER / "data/silver_plus_10k_prep_20260913/annotation_input/work.jsonl"
PROMPT = PAPER / "silver_prompt.txt"
PILOT10 = PAPER / "data/silver_plus_10k_prep_20260913/pilot10_public_api_v1/parsed.json"
DEFAULT_OUT = PAPER / "data/silver_plus_10k_prep_20260913/run2500_public_api_v1"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def chunks(rows: list[dict], n: int) -> list[list[dict]]:
    return [rows[i : i + n] for i in range(0, len(rows), n)]


def payload_of(batch: list[dict]) -> list[dict]:
    return [{"id": r["id"], "text": r["text"]} for r in batch]


def load_reuse_map(paths: list[Path]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in paths:
        if not p.is_file():
            continue
        obj = json.loads(p.read_text(encoding="utf-8"))
        for rec in obj.get("records") or []:
            if isinstance(rec, dict) and rec.get("id"):
                out[rec["id"]] = rec
    return out


def call_one_batch(
    key: str,
    system: str,
    batch: list[dict],
    *,
    model: str,
    base: str,
    timeout: int,
    max_tokens: int,
    retries: int,
    sleep_s: float,
) -> dict:
    src = payload_of(batch)
    user = json.dumps({"records": src}, ensure_ascii=False)
    last = None
    for attempt in range(1, retries + 1):
        status, body, elapsed, err = post_chat(
            key, system, user, model=model, base=base, timeout=timeout, max_tokens=max_tokens
        )
        content, finish = assistant_content(body if isinstance(body, dict) else {})
        parsed, parse_note = extract_json(content)
        repairs = []
        if parsed is not None:
            parsed, repairs = repair_parsed_records(src, parsed)
            val = validate_records(src, parsed)
        else:
            val = {"ok": False, "n_errors": 1, "errors": [{"kind": "parse", "msg": parse_note}]}
        last = {
            "attempt": attempt,
            "http_status": status,
            "elapsed_s": round(elapsed, 3),
            "error_tag": err,
            "response_model": body.get("model") if isinstance(body, dict) else None,
            "usage": body.get("usage") if isinstance(body, dict) else None,
            "finish_reason": finish,
            "parse_note": parse_note,
            "repairs": repairs,
            "validation": val,
            "api_error": body.get("error") if isinstance(body, dict) else None,
            "assistant_content": content,
            "parsed": parsed,
        }
        if status == 200 and val.get("ok"):
            last["ok"] = True
            return last
        last["ok"] = False
        if attempt < retries:
            time.sleep(min(30.0, sleep_s * attempt * 2))
    return last or {"ok": False}


def merge_progress(out_dir: Path, batches: list[list[dict]], src_by_id: dict[str, dict]) -> None:
    labeled = []
    failed = []
    for i, batch in enumerate(batches, start=1):
        p = out_dir / "batches" / f"batch_{i:04d}.json"
        if not p.is_file():
            continue
        obj = json.loads(p.read_text(encoding="utf-8"))
        if not obj.get("ok"):
            failed.append(i)
            continue
        recs = (obj.get("parsed") or {}).get("records") or []
        for src, rec in zip(batch, recs):
            labeled.append(to_student_row(src_by_id[src["id"]], rec))
    dump_jsonl(out_dir / "labeled.jsonl", labeled)
    dump_json(
        out_dir / "progress.json",
        {
            "n_labeled": len(labeled),
            "n_failed_batches": len(failed),
            "failed_batches": failed,
            "status_counts": dict(Counter(r.get("status") for r in labeled)),
            "domain_counts": dict(Counter(r.get("source_domain") for r in labeled)),
            "n_spans": sum(len(r.get("spans") or []) for r in labeled),
            "updated": utcnow(),
        },
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2500)
    ap.add_argument("--batch-size", type=int, default=10)
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--prompt", default=str(PROMPT))
    ap.add_argument("--work", default=str(WORK))
    ap.add_argument("--model", default=REQUEST_MODEL)
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--sleep", type=float, default=0.4)
    ap.add_argument("--ids", default="", help="comma-separated ids; overrides --n sample")
    ap.add_argument("--probe", action="store_true", help="live probe only; do not write the 2500 run dir")
    ap.add_argument("--no-reuse-pilot10", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    work = load_jsonl(Path(args.work))
    if args.ids:
        want = [x.strip() for x in args.ids.split(",") if x.strip()]
        by = {r["id"]: r for r in work}
        selected = [by[i] for i in want]
    else:
        selected = sample_by_domain(work, args.n)
    batches = chunks(selected, args.batch_size)
    out_dir = Path(args.out_dir)
    if args.probe:
        out_dir = out_dir / "_probe" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "batches").mkdir(exist_ok=True)
    dump_json(
        out_dir / "sample_manifest.json",
        {
            "prompt_id": PROMPT_ID,
            "prompt_path": args.prompt,
            "model": args.model,
            "n": len(selected),
            "batch_size": args.batch_size,
            "n_batches": len(batches),
            "ids": [r["id"] for r in selected],
            "domain_counts": dict(Counter(r["source_domain"] for r in selected)),
            "created": utcnow(),
            "probe": bool(args.probe),
        },
    )
    if args.dry_run:
        print(json.dumps({"dry_run": True, "n": len(selected), "n_batches": len(batches), "domains": dict(Counter(r["source_domain"] for r in selected))}, ensure_ascii=False))
        return 0

    system = Path(args.prompt).read_text(encoding="utf-8").strip()
    key = load_key()
    reuse = {} if args.no_reuse_pilot10 else load_reuse_map([PILOT10])
    src_by_id = {r["id"]: r for r in selected}

    for i, batch in enumerate(batches, start=1):
        dest = out_dir / "batches" / f"batch_{i:04d}.json"
        if dest.is_file():
            prev = json.loads(dest.read_text(encoding="utf-8"))
            if prev.get("ok"):
                print(json.dumps({"skip": i, "n": len(batch)}, ensure_ascii=False), flush=True)
                continue
        src = payload_of(batch)
        if reuse and all(r["id"] in reuse for r in batch):
            parsed = {"records": [reuse[r["id"]] for r in batch]}
            val = validate_records(src, parsed)
            if val.get("ok"):
                dump_json(
                    dest,
                    {
                        "ok": True,
                        "batch": i,
                        "ids": [r["id"] for r in batch],
                        "reused": "pilot10",
                        "parsed": parsed,
                        "validation": val,
                        "at": utcnow(),
                    },
                )
                print(json.dumps({"reused": i, "ids": [r["id"] for r in batch]}, ensure_ascii=False), flush=True)
                merge_progress(out_dir, batches, src_by_id)
                continue
        print(json.dumps({"start": i, "n": len(batch), "ids": [r["id"] for r in batch]}, ensure_ascii=False), flush=True)
        call_kw = dict(
            model=args.model,
            base=args.base,
            timeout=args.timeout,
            max_tokens=args.max_tokens,
            retries=args.retries,
            sleep_s=args.sleep,
        )
        result = call_one_batch(key, system, batch, **call_kw)
        if not result.get("ok") and len(batch) > 1:
            print(json.dumps({"fallback_per_record": i}, ensure_ascii=False), flush=True)
            recs = []
            parts = []
            fallback_ok = True
            for row in batch:
                sub = call_one_batch(key, system, [row], **call_kw)
                parts.append(
                    {
                        "id": row["id"],
                        "ok": sub.get("ok"),
                        "n_errors": (sub.get("validation") or {}).get("n_errors"),
                        "repairs": sub.get("repairs") or [],
                    }
                )
                if not sub.get("ok"):
                    fallback_ok = False
                    result = {**sub, "fallback": "per_record_failed", "parts": parts}
                    break
                recs.extend((sub.get("parsed") or {}).get("records") or [])
                time.sleep(args.sleep)
            if fallback_ok:
                parsed = {"records": recs}
                val = validate_records(src, parsed)
                result = {
                    "ok": bool(val.get("ok")),
                    "fallback": "per_record",
                    "parsed": parsed,
                    "validation": val,
                    "parts": parts,
                    "http_status": 200,
                    "response_model": args.model,
                }
        save = dict(result)
        save["batch"] = i
        save["ids"] = [r["id"] for r in batch]
        save["at"] = utcnow()
        dump_json(dest, save)
        print(
            json.dumps(
                {
                    "done": i,
                    "ok": result.get("ok"),
                    "http_status": result.get("http_status"),
                    "elapsed_s": result.get("elapsed_s"),
                    "response_model": result.get("response_model"),
                    "n_errors": (result.get("validation") or {}).get("n_errors"),
                    "finish_reason": result.get("finish_reason"),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        merge_progress(out_dir, batches, src_by_id)
        if not result.get("ok"):
            print(json.dumps({"batch_failed": i, "errors": (result.get("validation") or {}).get("errors", [])[:8]}, ensure_ascii=False), flush=True)
        time.sleep(args.sleep)

    merge_progress(out_dir, batches, src_by_id)
    prog = json.loads((out_dir / "progress.json").read_text(encoding="utf-8"))
    print(json.dumps({"finished": True, **{k: prog[k] for k in ("n_labeled", "n_failed_batches", "status_counts", "n_spans")}}, ensure_ascii=False))
    return 0 if prog.get("n_failed_batches") == 0 and prog.get("n_labeled") == len(selected) else 2


if __name__ == "__main__":
    raise SystemExit(main())
