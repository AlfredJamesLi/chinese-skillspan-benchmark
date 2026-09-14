#!/usr/bin/env python3
"""Call gpt-6-astra for one Codex Silver wave. Writes batches_out/ in Codex JSON.

Does not touch Gold150 / V4 / v6a / the 2500 run / other waves.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from run_silver_public_api import call_one_batch
from silver_public_api_lib import (
    DEFAULT_BASE,
    REQUEST_MODEL,
    dump_json,
    dump_jsonl,
    load_jsonl,
    load_key,
    repair_parsed_records,
    to_student_row,
    validate_records,
)

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PKG = PAPER / "data/silver_plus_10k_prep_20260913/codex_remaining_5436"
HELD = PKG / "ids_held_2500.txt"
REMAINING = PKG / "remaining.jsonl"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_src_map() -> dict[str, dict]:
    rows = load_jsonl(REMAINING)
    return {r["id"]: r for r in rows}


def batch_ok(dest: Path, src_records: list[dict]) -> bool:
    if not dest.is_file():
        return False
    try:
        parsed = json.loads(dest.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if "records" not in parsed and isinstance(parsed.get("parsed"), dict):
        parsed = parsed["parsed"]
    parsed, _ = repair_parsed_records(src_records, parsed)
    return bool(validate_records(src_records, parsed).get("ok"))


def write_progress(wave_dir: Path, index: list[dict], src_by_id: dict[str, dict]) -> dict:
    labeled = []
    failed = []
    n_ok = 0
    for row in index:
        dest = wave_dir / row["out_file"]
        src = json.loads((wave_dir / row["file"]).read_text(encoding="utf-8"))["records"]
        if not batch_ok(dest, src):
            if dest.is_file():
                failed.append(row["batch"])
            continue
        n_ok += 1
        parsed = json.loads(dest.read_text(encoding="utf-8"))
        if "records" not in parsed and isinstance(parsed.get("parsed"), dict):
            parsed = parsed["parsed"]
        parsed, _ = repair_parsed_records(src, parsed)
        for rec in parsed["records"]:
            labeled.append(to_student_row(src_by_id[rec["id"]], rec))
    prog = {
        "n_labeled": len(labeled),
        "n_expected": sum(int(r["n"]) for r in index),
        "n_ok_batches": n_ok,
        "n_batches": len(index),
        "n_failed_batches": len(failed),
        "failed_batches": failed,
        "status_counts": dict(Counter(r.get("status") for r in labeled)),
        "domain_counts": dict(Counter(r.get("source_domain") for r in labeled)),
        "n_spans": sum(len(r.get("spans") or []) for r in labeled),
        "updated": utcnow(),
    }
    dump_jsonl(wave_dir / "labeled.jsonl", labeled)
    dump_json(wave_dir / "progress.json", prog)
    dump_json(
        wave_dir / "STATUS.json",
        {"wave": wave_dir.name, "n_out": n_ok, "n_batches": len(index), "n_labeled": len(labeled)},
    )
    return prog


def patch_parent_progress(wave_name: str, status: str) -> None:
    p = PKG / "waves" / "PROGRESS.json"
    if not p.is_file():
        return
    obj = json.loads(p.read_text(encoding="utf-8"))
    for w in obj.get("waves") or []:
        if w.get("wave") == wave_name:
            w["status"] = status
            w["updated"] = utcnow()
    dump_json(p, obj)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave-dir", required=True)
    ap.add_argument("--prompt", default="")
    ap.add_argument("--model", default=REQUEST_MODEL)
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--sleep", type=float, default=0.4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    wave_dir = Path(args.wave_dir).resolve()
    wave_name = wave_dir.name
    if wave_name not in {"wave1", "wave2", "wave3"}:
        raise SystemExit(f"refusing unknown wave dir: {wave_dir}")
    index = load_jsonl(wave_dir / "BATCH_INDEX.jsonl")
    if not index:
        raise SystemExit(f"empty BATCH_INDEX in {wave_dir}")
    held = {x.strip() for x in HELD.read_text(encoding="utf-8").splitlines() if x.strip()}
    src_by_id = load_src_map()
    ids = []
    for row in index:
        ids.extend(row["ids"])
    leak = sorted(set(ids) & held)
    if leak:
        raise SystemExit(f"wave includes held-2500 ids: {leak[:8]}")
    missing = [i for i in ids if i not in src_by_id]
    if missing:
        raise SystemExit(f"ids not in remaining.jsonl: {missing[:8]}")

    prompt_path = Path(args.prompt) if args.prompt else wave_dir / "PROMPT_silver_public_api_v1.0.txt"
    print(
        json.dumps(
            {
                "wave": wave_name,
                "n_batches": len(index),
                "n_sents": len(ids),
                "batch_lo": index[0]["batch"],
                "batch_hi": index[-1]["batch"],
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    if args.dry_run:
        return 0

    system = prompt_path.read_text(encoding="utf-8").strip()
    key = load_key()
    (wave_dir / "batches_out").mkdir(parents=True, exist_ok=True)
    patch_parent_progress(wave_name, "running")

    call_kw = dict(
        model=args.model,
        base=args.base,
        timeout=args.timeout,
        max_tokens=args.max_tokens,
        retries=args.retries,
        sleep_s=args.sleep,
    )
    for row in index:
        src_payload = json.loads((wave_dir / row["file"]).read_text(encoding="utf-8"))
        src = src_payload["records"]
        dest = wave_dir / row["out_file"]
        bno = row["batch"]
        if batch_ok(dest, src):
            print(json.dumps({"skip": bno, "n": len(src)}, ensure_ascii=False), flush=True)
            continue
        print(json.dumps({"start": bno, "n": len(src), "ids": [r["id"] for r in src]}, ensure_ascii=False), flush=True)
        result = call_one_batch(key, system, src, **call_kw)
        if not result.get("ok") and len(src) > 1:
            print(json.dumps({"fallback_per_record": bno}, ensure_ascii=False), flush=True)
            recs = []
            fallback_ok = True
            for one in src:
                sub = call_one_batch(key, system, [one], **call_kw)
                if not sub.get("ok"):
                    fallback_ok = False
                    result = sub
                    break
                recs.extend((sub.get("parsed") or {}).get("records") or [])
                time.sleep(args.sleep)
            if fallback_ok:
                parsed = {"records": recs}
                parsed, _ = repair_parsed_records(src, parsed)
                val = validate_records(src, parsed)
                result = {
                    "ok": bool(val.get("ok")),
                    "fallback": "per_record",
                    "parsed": parsed,
                    "validation": val,
                    "http_status": 200,
                    "response_model": args.model,
                }
        if result.get("ok"):
            parsed = result.get("parsed") or {}
            parsed, _ = repair_parsed_records(src, parsed)
            dump_json(dest, parsed)
        else:
            dump_json(
                dest.with_name(dest.stem + ".failed.json"),
                {"ok": False, "batch": bno, "validation": result.get("validation"), "at": utcnow()},
            )
        print(
            json.dumps(
                {
                    "done": bno,
                    "ok": result.get("ok"),
                    "http_status": result.get("http_status"),
                    "elapsed_s": result.get("elapsed_s"),
                    "n_errors": (result.get("validation") or {}).get("n_errors"),
                    "fallback": result.get("fallback"),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        write_progress(wave_dir, index, src_by_id)
        if not result.get("ok"):
            print(json.dumps({"batch_failed": bno, "errors": (result.get("validation") or {}).get("errors", [])[:8]}, ensure_ascii=False), flush=True)
        time.sleep(args.sleep)

    prog = write_progress(wave_dir, index, src_by_id)
    done = prog["n_labeled"] == prog["n_expected"] and prog["n_failed_batches"] == 0
    patch_parent_progress(wave_name, "done" if done else "incomplete")
    print(json.dumps({"finished": True, "wave": wave_name, **{k: prog[k] for k in ("n_labeled", "n_expected", "n_ok_batches", "n_failed_batches")}}, ensure_ascii=False))
    return 0 if done else 2


if __name__ == "__main__":
    raise SystemExit(main())
