# Silver-plus 补跑（2026-09-08）

主机 B（`DS210039`）。评分器 `cnss-lskt-1.2.0`。Gold150 SHA-256  
`ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`。

本目录只归档**分数、协议、清单和脚本**。不含 LoRA / CRF 权重、不含 Gold150 原文预测、不含招聘广告全文。

## 不改动的数字

- V4 hybrid 2601 上 JobBERT-zh 3M typed exact **0.4331**
- 官方零样本 Qwen SOP extract **0.1724**
- 既有 Gold150 主配置：JobBERT-zh 3M、v6a、B2 typed exact **0.5536±0.0054**（n=3 样本标准差，不是测试集置信区间）

本轮结果**不能**与 0.4331 / 0.1724 放进同一主表相减。

## 本轮做了什么

| 实验 | 训练 | 测试 | 结果 |
|---|---|---|---|
| Qwen2.5-14B JSON-offset LoRA SFT（仅 B2） | `v6a_nocross` 2150/169，种子 42/43/44 | Gold150 | typed exact **0.1215±0.0092**；relaxed **0.4459±0.0237** |
| JobBERT-zh 3M HEM 等量对照 | H/E/M 各 564 条 × 3 种子；DAPT encoder + 重初始化 CRF | Gold150 | H **0.4541±0.0103**；E **0.4345±0.0235**；M **0.4562±0.0236** |
| JobBERT-zh 1M | 未跑 | — | 见 `JOBBERT1M_SKIP.md` |

Qwen 相对 v3 JSON-offset（Gold 0.0788±0.0108）同时改了数据（1382→2150）和选模（最后一轮 → 开发集 typed exact）。不能把差值全部写成扩量。本轮只有 B2，不能独立证明 B2>B1。JSON-offset **不是** SOP extract 0.1724。

HEM 是等样本量的来源对照，不是难度真值，也不能替换 v6a 全量 0.5536。

## 文件

- `EXTENSION_RESULTS.csv` / `EXTENSION_RESULTS.json`：12 个正式训练的 Gold150 分数
- `CODEX_EXTENSION_HANDOFF.md`：给文稿的完整交接（含禁止项）
- `METHOD_AND_LIMITATIONS.md`、`PRECHECK.md`、`QWEN_PROTOCOL.md`
- `HEM_SAMPLING_MANIFEST.json`：H/E/M 抽样 ID（无正文）
- `scores/`：逐 run 的 `score*.json`、`run_config.json`、`RESOURCE.json`
- `scripts/`：本轮训练/推断/汇总脚本副本；仓库根目录 `scripts/` 亦有同名文件

Slurm job **7360**。官方训练 12 次（3 Qwen + 9 HEM）。
