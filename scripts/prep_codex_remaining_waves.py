#!/usr/bin/env python3
"""Split remaining 5,436 Silver sentences into 3 Codex waves.

Does not call APIs. Does not touch the local 2500 run, Gold150, V4, or v6a.
"""
from __future__ import annotations

import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from silver_public_api_lib import dump_json, dump_jsonl, load_jsonl

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PKG = PAPER / "data/silver_plus_10k_prep_20260913/codex_remaining_5436"
WAVES = PKG / "waves"
# 181 + 181 + 182 JSON batches = 544
WAVE_BATCH_COUNTS = (181, 181, 182)
MODEL = "gpt-6-astra"
PROMPT_ID = "silver_public_api_v1.0"


def wave_prompt(wave_id: str, batch_lo: int, batch_hi: int, n_sents: int, n_batches: int, last_n: int) -> str:
    return f"""# Codex 任务：{wave_id} — gpt-6-astra 标剩余 Silver

你在仓库 `/home/guojingli3/SCESC-LLM-skill-extraction` 的 **Chinese-SkillSpan** 窗口。
**只做这一波：{wave_id}。** 不要做 wave1/wave2/wave3 中的其它波，不要重标 `ids_held_2500.txt` 的 2500 句。
不要改 `access_paper/`、Gold150、V4 hybrid、`data/silver_plus_v6a_nocross/`、`run2500_public_api_v1/`。不要写论文 F1。

## 本波

目录：`Chinese_skill_benchmark_Paper/data/silver_plus_10k_prep_20260913/codex_remaining_5436/waves/{wave_id}/`

- 句子 **{n_sents}**；JSON 批 **{n_batches}**（`batch_{batch_lo:04d}.json` … `batch_{batch_hi:04d}.json`）
- 每批最多 10 条；本波最后一批 {last_n} 条
- 系统提示词：本目录 `PROMPT_silver_public_api_v1.0.txt`
- 用户输入：`batches/batch_XXXX.json`（仅 `records[].id` + `text`）
- 输出：同名写入 `batches_out/batch_XXXX.json`

## 调用

模型：**gpt-6-astra**。  
`POST https://claudeed.ysaikeji.cn/v1/chat/completions`，密钥 `~/.config/ysaikeji/api_key`。  
temperature=0，max_tokens=8192，超时 ≥ 180s。不要改成 20 条一批。

系统消息 = 提示词全文。用户消息 = 该批 JSON。各记录独立。

## 输出格式

只返回一个 JSON 对象（不要 Markdown 围栏）：顶层 `records`；条数/顺序/id 与输入一致；每条恰好 `id, spans, status, note, issues`。  
`spans[].start/end` 为 Python Unicode 码点；`text[start:end]` 必须等于 `spans[].text`。  
`status` ∈ candidate_complete | confirmed_empty | adjudication_required。  
失败重试最多 3 次；不要编造跨度。

全部 {n_batches} 批写完后，把 `PROGRESS.json` 的 `{wave_id}.status` 改成 `done`（若没有该文件，在本波目录写 `STATUS.json`：`{{"wave":"{wave_id}","n_out": <已写批次数>}}`）。

不要合并 5,436、不要抽 150、不要训练。合并由主窗口在三波都齐后执行：

```bash
cd Chinese_skill_benchmark_Paper/scripts
python3 sync_codex_wave_outputs.py
python3 merge_codex_remaining_silver.py
```
"""


def how_to(wave_id: str, batch_lo: int, batch_hi: int) -> str:
    return f"""本波 {wave_id}：只处理 batches/batch_{batch_lo:04d}.json … batch_{batch_hi:04d}.json
系统消息：PROMPT_silver_public_api_v1.0.txt
输出：batches_out/ 同名 JSON
模型：gpt-6-astra
"""


def main() -> int:
    index = load_jsonl(PKG / "BATCH_INDEX.jsonl")
    if len(index) != 544:
        raise SystemExit(f"expected 544 batches, got {len(index)}")
    prompt_src = PKG / "PROMPT_silver_public_api_v1.0.txt"
    if WAVES.exists():
        shutil.rmtree(WAVES)
    WAVES.mkdir(parents=True)

    start = 0
    wave_rows = []
    for i, n_b in enumerate(WAVE_BATCH_COUNTS, start=1):
        chunk = index[start : start + n_b]
        start += n_b
        wave_id = f"wave{i}"
        wdir = WAVES / wave_id
        (wdir / "batches").mkdir(parents=True)
        (wdir / "batches_out").mkdir()
        shutil.copyfile(prompt_src, wdir / "PROMPT_silver_public_api_v1.0.txt")
        n_sents = sum(r["n"] for r in chunk)
        domains: Counter = Counter()
        ids = []
        for row in chunk:
            src = PKG / row["file"]
            shutil.copyfile(src, wdir / "batches" / Path(row["file"]).name)
            ids.extend(row["ids"])
            for d, c in (row.get("source_domains") or {}).items():
                domains[d] += c
        dump_jsonl(wdir / "BATCH_INDEX.jsonl", chunk)
        (wdir / "ids.txt").write_text("\n".join(ids) + "\n", encoding="utf-8")
        batch_lo = chunk[0]["batch"]
        batch_hi = chunk[-1]["batch"]
        last_n = chunk[-1]["n"]
        counts = {
            "wave": wave_id,
            "status": "ready",
            "batch_lo": batch_lo,
            "batch_hi": batch_hi,
            "n_batches": len(chunk),
            "n_sents": n_sents,
            "last_batch_n": last_n,
            "batch_size": 10,
            "model": MODEL,
            "prompt_id": PROMPT_ID,
            "domains": dict(domains),
            "created": datetime.now(timezone.utc).isoformat(),
        }
        dump_json(wdir / "COUNTS.json", counts)
        (wdir / "CODEX_PROMPT.md").write_text(
            wave_prompt(wave_id, batch_lo, batch_hi, n_sents, len(chunk), last_n),
            encoding="utf-8",
        )
        (wdir / "HOW_TO_RUN.txt").write_text(how_to(wave_id, batch_lo, batch_hi), encoding="utf-8")
        wave_rows.append(counts)

    if start != len(index):
        raise SystemExit(f"wave split leftover: {start} vs {len(index)}")

    progress = {
        "n_remaining": 5436,
        "n_waves": 3,
        "model": MODEL,
        "do_one_wave_per_codex_session": True,
        "order": ["wave1", "wave2", "wave3"],
        "waves": wave_rows,
        "how_to_track": "Count files in waves/waveN/batches_out/. Compare to COUNTS.json n_batches.",
        "merge_when_all_done": [
            "python3 scripts/sync_codex_wave_outputs.py",
            "python3 scripts/merge_codex_remaining_silver.py",
        ],
    }
    dump_json(WAVES / "PROGRESS.json", progress)

    parent = """# 剩余 5,436 已拆成 3 波（给 Codex 看进度）

一次只开一波。推荐顺序：wave1 → wave2 → wave3。

| 波次 | 句子 | JSON 批 | 批号 | Codex 提示词 |
|------|-----:|--------:|------|--------------|
| wave1 | {w1s} | {w1b} | {w1lo:04d}–{w1hi:04d} | `waves/wave1/CODEX_PROMPT.md` |
| wave2 | {w2s} | {w2b} | {w2lo:04d}–{w2hi:04d} | `waves/wave2/CODEX_PROMPT.md` |
| wave3 | {w3s} | {w3b} | {w3lo:04d}–{w3hi:04d} | `waves/wave3/CODEX_PROMPT.md` |

合计 5,436 句、544 批。不要标 `ids_held_2500.txt`。模型 gpt-6-astra，每批最多 10 条。

进度：看各波 `batches_out/` 文件数，或 `waves/PROGRESS.json`。
三波齐后在 scripts 下：`python3 sync_codex_wave_outputs.py && python3 merge_codex_remaining_silver.py`
""".format(
        w1s=wave_rows[0]["n_sents"],
        w1b=wave_rows[0]["n_batches"],
        w1lo=wave_rows[0]["batch_lo"],
        w1hi=wave_rows[0]["batch_hi"],
        w2s=wave_rows[1]["n_sents"],
        w2b=wave_rows[1]["n_batches"],
        w2lo=wave_rows[1]["batch_lo"],
        w2hi=wave_rows[1]["batch_hi"],
        w3s=wave_rows[2]["n_sents"],
        w3b=wave_rows[2]["n_batches"],
        w3lo=wave_rows[2]["batch_lo"],
        w3hi=wave_rows[2]["batch_hi"],
    )
    (WAVES / "README.md").write_text(parent, encoding="utf-8")
    print(json.dumps({"waves": [{k: r[k] for k in ("wave", "n_sents", "n_batches", "batch_lo", "batch_hi", "domains")} for r in wave_rows]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
