# 剩余 5,436 已拆成 3 波（给 Codex 看进度）

一次只开一波。推荐顺序：wave1 → wave2 → wave3。

| 波次 | 句子 | JSON 批 | 批号 | Codex 提示词 |
|------|-----:|--------:|------|--------------|
| wave1 | 1810 | 181 | 0001–0181 | `waves/wave1/CODEX_PROMPT.md` |
| wave2 | 1810 | 181 | 0182–0362 | `waves/wave2/CODEX_PROMPT.md` |
| wave3 | 1816 | 182 | 0363–0544 | `waves/wave3/CODEX_PROMPT.md` |

合计 5,436 句、544 批。不要标 `ids_held_2500.txt`。模型 gpt-6-astra，每批最多 10 条。

进度：看各波 `batches_out/` 文件数，或 `waves/PROGRESS.json`。
三波齐后在 scripts 下：`python3 sync_codex_wave_outputs.py && python3 merge_codex_remaining_silver.py`
