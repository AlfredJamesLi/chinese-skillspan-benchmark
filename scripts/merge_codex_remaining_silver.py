#!/usr/bin/env python3
"""Merge Codex batches_out into labeled jsonl. Does not touch the 2500 run or v6a."""
from __future__ import annotations

import json
from pathlib import Path

from silver_public_api_lib import dump_json, dump_jsonl, load_jsonl, repair_parsed_records, to_student_row, validate_records

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PKG = PAPER / "data/silver_plus_10k_prep_20260913/codex_remaining_5436"


def main() -> int:
    remaining = {r["id"]: r for r in load_jsonl(PKG / "remaining.jsonl")}
    index = load_jsonl(PKG / "BATCH_INDEX.jsonl")
    labeled = []
    failed = []
    for row in index:
        dest = PKG / row["out_file"]
        src_payload = json.loads((PKG / row["file"]).read_text(encoding="utf-8"))
        src = src_payload["records"]
        if not dest.is_file():
            failed.append({"batch": row["batch"], "reason": "missing"})
            continue
        parsed = json.loads(dest.read_text(encoding="utf-8"))
        if "records" not in parsed and isinstance(parsed.get("parsed"), dict):
            parsed = parsed["parsed"]
        parsed, repairs = repair_parsed_records(src, parsed)
        val = validate_records(src, parsed)
        if not val.get("ok"):
            failed.append({"batch": row["batch"], "reason": "invalid", "errors": val.get("errors", [])[:8], "repairs": repairs})
            continue
        for rec in parsed["records"]:
            labeled.append(to_student_row(remaining[rec["id"]], rec))
    dump_jsonl(PKG / "labeled.jsonl", labeled)
    dump_json(PKG / "MERGE_REPORT.json", {"n_labeled": len(labeled), "n_expected": len(remaining), "n_failed_batches": len(failed), "failed": failed})
    print(json.dumps({"n_labeled": len(labeled), "n_expected": len(remaining), "n_failed_batches": len(failed)}, ensure_ascii=False))
    return 0 if not failed and len(labeled) == len(remaining) else 2


if __name__ == "__main__":
    raise SystemExit(main())
