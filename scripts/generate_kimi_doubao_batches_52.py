#!/usr/bin/env python3
"""Build 52-batch pack for Kimi/Doubao from rule silver. Does not touch Gold v2.

batch_00 = original sample_50 (rule_v4, same input Codex already corrected).
batch_01..51 = remaining 2551 Gold-v2 IDs (same as Codex batches_51).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PACK = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack"
SAMPLE50 = PACK / "sample_50.jsonl"
SRC51 = PACK / "batches_51"
OUT = PACK / "batches_52"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def compact(rec: dict) -> dict:
    return {
        "id": rec.get("id"),
        "sentence": rec.get("sentence") or "",
        "domain": rec.get("domain") or rec.get("source_domain") or "",
        "spans": rec.get("spans") or [],
        "v4_source": rec.get("v4_source") or "rule_v4",
    }


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    b0 = [compact(r) for r in load_jsonl(SAMPLE50)]
    with (OUT / "batch_00.jsonl").open("w", encoding="utf-8") as f:
        for rec in b0:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    copied = []
    for src in sorted(SRC51.glob("batch_*.jsonl")):
        dst = OUT / src.name
        shutil.copy2(src, dst)
        copied.append(dst.name)
    ids = []
    files = sorted(OUT.glob("batch_*.jsonl"))
    batches = []
    for p in files:
        rows = load_jsonl(p)
        ids.extend(str(r["id"]) for r in rows)
        batches.append({"file": p.name, "n": len(rows), "id_first": rows[0]["id"], "id_last": rows[-1]["id"]})
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate ids")
    meta = {
        "gold_v2_untouched": True,
        "for": "Kimi and Doubao local correction (same rule-silver input as Codex)",
        "n_batches": len(files),
        "n_sentences": len(ids),
        "n_unique_ids": len(set(ids)),
        "batch_00": "original sample_50.jsonl (rule_v4), 50 sentences",
        "batch_01_51": "same files as batches_51/",
        "do_not_use_codex_corrected_spans_as_input": True,
        "batches": batches,
    }
    (OUT / "manifest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("n_batches", "n_sentences", "n_unique_ids")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
