#!/usr/bin/env python3
"""Prepare remaining new-Silver sentences for Codex → gpt-6-astra.

Excludes the frozen 2500-id list in run2500_public_api_v1/sample_manifest.json.
Does not call APIs, does not rewrite Gold150 / V4 / v6a / the 2500 run.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from silver_public_api_lib import dump_json, dump_jsonl, load_jsonl

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
WORK = PAPER / "data/silver_plus_10k_prep_20260913/annotation_input/work.jsonl"
HELD = PAPER / "data/silver_plus_10k_prep_20260913/run2500_public_api_v1/sample_manifest.json"
PROMPT = PAPER / "silver_prompt.txt"
OUT = PAPER / "data/silver_plus_10k_prep_20260913/codex_remaining_5436"
BATCH_SIZE = 10
PROMPT_ID = "silver_public_api_v1.0"
MODEL = "gpt-6-astra"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    work = load_jsonl(WORK)
    held_obj = json.loads(HELD.read_text(encoding="utf-8"))
    held_ids = held_obj["ids"]
    held_set = set(held_ids)
    if len(held_ids) != 2500 or len(held_set) != 2500:
        raise SystemExit(f"held list must be 2500 unique, got n={len(held_ids)} unique={len(held_set)}")
    missing_held = [i for i in held_ids if i not in {r["id"] for r in work}]
    if missing_held:
        raise SystemExit(f"held ids not in work.jsonl: {missing_held[:5]}")
    remaining = [r for r in work if r["id"] not in held_set]
    overlap = [r["id"] for r in remaining if r["id"] in held_set]
    if overlap:
        raise SystemExit("overlap leaked into remaining")
    expect = len(work) - 2500
    if len(remaining) != expect:
        raise SystemExit(f"remaining {len(remaining)} != {expect}")
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "batches").mkdir(parents=True)
    (OUT / "batches_out").mkdir()
    shutil.copyfile(PROMPT, OUT / "PROMPT_silver_public_api_v1.0.txt")
    slim = [{"id": r["id"], "text": r["text"]} for r in remaining]
    dump_jsonl(OUT / "remaining.jsonl", remaining)
    dump_jsonl(OUT / "remaining_id_text.jsonl", slim)
    (OUT / "ids_remaining.txt").write_text("\n".join(r["id"] for r in remaining) + "\n", encoding="utf-8")
    (OUT / "ids_held_2500.txt").write_text("\n".join(held_ids) + "\n", encoding="utf-8")

    index = []
    n_batches = (len(remaining) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(n_batches):
        chunk = remaining[i * BATCH_SIZE : (i + 1) * BATCH_SIZE]
        payload = {"records": [{"id": r["id"], "text": r["text"]} for r in chunk]}
        name = f"batch_{i + 1:04d}.json"
        dest = OUT / "batches" / name
        dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index.append(
            {
                "batch": i + 1,
                "file": f"batches/{name}",
                "out_file": f"batches_out/{name}",
                "n": len(chunk),
                "ids": [r["id"] for r in chunk],
                "source_domains": dict(Counter(r["source_domain"] for r in chunk)),
            }
        )
    dump_jsonl(OUT / "BATCH_INDEX.jsonl", index)
    counts = {
        "created": datetime.now(timezone.utc).isoformat(),
        "prompt_id": PROMPT_ID,
        "model": MODEL,
        "batch_size": BATCH_SIZE,
        "n_work": len(work),
        "n_held_2500": 2500,
        "n_remaining": len(remaining),
        "n_batches": n_batches,
        "last_batch_n": len(remaining) % BATCH_SIZE or BATCH_SIZE,
        "remaining_domains": dict(Counter(r["source_domain"] for r in remaining)),
        "held_domains": held_obj.get("domain_counts"),
        "held_manifest": str(HELD),
        "sha256_work": sha256_file(WORK),
        "sha256_prompt": sha256_file(PROMPT),
        "sha256_ids_remaining": sha256_file(OUT / "ids_remaining.txt"),
        "overlap_with_2500": 0,
        "not_gold150": True,
        "do_not_relabel_2500": True,
    }
    dump_json(OUT / "COUNTS.json", counts)

    how = """# Codex 调用 gpt-6-astra — 剩余 Silver（不含已抽的 2500）

系统消息：整份粘贴 `PROMPT_silver_public_api_v1.0.txt`（即公开版 silver_public_api_v1.0）。
用户消息：只贴一个 `batches/batch_XXXX.json`（顶层 `records`，每项仅 `id`+`text`）。
模型：gpt-6-astra。每批最多 10 条（最后一批 6 条）。不要用 20 条一批。

只输出一个 JSON 对象，顶层字段 records。不要 Markdown 围栏，不要 JSONL。
records 的数量、顺序、id 必须与输入一致。
每条恰好：id, spans, status, note, issues。
spans[].start/end 为 Unicode 码点、0 起始、左闭右开；输入 text[start:end] 必须等于 spans[].text。

把模型输出存成 `batches_out/batch_XXXX.json`（与输入同名）。
不要标注 `ids_held_2500.txt` 里的 2500 条。不要改 Gold150 / V4 / v6a。

实验室通道（若 Codex 走同一代理）：
POST https://claudeed.ysaikeji.cn/v1/chat/completions
temperature=0, max_tokens=8192。

合并（全部 544 批齐后，在仓库 scripts 目录）：

python3 merge_codex_remaining_silver.py
"""
    (OUT / "HOW_TO_RUN.txt").write_text(how, encoding="utf-8")

    print(json.dumps({k: counts[k] for k in ("n_remaining", "n_batches", "last_batch_n", "remaining_domains")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
