# Codex：剩余 5,436 已拆成 3 波

**一次只跑一波。** 把对应波次的 `CODEX_PROMPT.md` 交给 Codex。模型 **gpt-6-astra**。不要标正在跑的 2500 句。

顺序：

1. `waves/wave1/CODEX_PROMPT.md` — 1,810 句，批 0001–0181
2. `waves/wave2/CODEX_PROMPT.md` — 1,810 句，批 0182–0362
3. `waves/wave3/CODEX_PROMPT.md` — 1,816 句，批 0363–0544（最后一批 6 条）

进度看各波 `batches_out/` 文件数，或 `waves/PROGRESS.json`。

三波齐后：

```bash
cd Chinese_skill_benchmark_Paper/scripts
python3 sync_codex_wave_outputs.py
python3 merge_codex_remaining_silver.py
```

不要改 Gold150 / V4 / v6a / `run2500_public_api_v1/`。
