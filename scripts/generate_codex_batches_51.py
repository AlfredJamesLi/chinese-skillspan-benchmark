#!/usr/bin/env python3
"""Split remaining test_g2ids compact silver into 51 local Codex batches. No Gold v2 write."""
from __future__ import annotations

import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
SRC = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/test_g2ids_compact.jsonl"
OUT = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/batches_51"
SKIP_PREFIX = "codex_"
BATCH = 50
N_BATCHES = 51


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
        "v4_source": rec.get("v4_source"),
    }


def main() -> int:
    rows = [compact(r) for r in load_jsonl(SRC)]
    remaining = [r for r in rows if not str(r.get("v4_source") or "").startswith(SKIP_PREFIX)]
    done = [r for r in rows if str(r.get("v4_source") or "").startswith(SKIP_PREFIX)]
    if OUT.exists():
        for p in OUT.glob("batch_*.jsonl"):
            p.unlink()
    OUT.mkdir(parents=True, exist_ok=True)

    n = len(remaining)
    # 50 batches of 50 + last batch with the remainder (51st has 51 when n=2551)
    sizes = [BATCH] * (N_BATCHES - 1)
    last = n - BATCH * (N_BATCHES - 1)
    if last <= 0:
        raise SystemExit(f"remaining={n} does not fill {N_BATCHES} batches of {BATCH}")
    sizes.append(last)

    manifest = []
    i = 0
    for b, sz in enumerate(sizes, start=1):
        chunk = remaining[i : i + sz]
        i += sz
        path = OUT / f"batch_{b:02d}.jsonl"
        with path.open("w", encoding="utf-8") as f:
            for rec in chunk:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        manifest.append(
            {
                "batch": b,
                "file": path.name,
                "n": len(chunk),
                "id_first": chunk[0]["id"] if chunk else None,
                "id_last": chunk[-1]["id"] if chunk else None,
            }
        )
    meta = {
        "gold_v2_untouched": True,
        "source": str(SRC),
        "already_codex": len(done),
        "remaining": n,
        "n_batches": len(manifest),
        "batch_size": BATCH,
        "last_batch_n": last,
        "ids_covered": i,
        "output_dir": str(OUT),
        "expected_output": "outputs/batch_XX_corrected.json (JSON array, same ids)",
        "batches": manifest,
    }
    (OUT / "manifest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("already_codex", "remaining", "n_batches", "last_batch_n", "ids_covered")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
