# New-silver Qwen SFT / JobBERT student — 2026-09-14 服务器状态

**待验证。** 不得写入 `notes/confirmed-results.md`。不得与论文主结果 JobBERT 3M exact **0.4331**、v6a **0.5536**、或共同指南 Qwen SFT **0.5403** 排同一句。

检查时刻：2026-09-14 22:37 +08。权重仍只在 `output/`，不上 GitHub。

## Qwen2.5-14B LoRA SFT（public-API Silver-2500 teacher，n_dev=182）

评测：silver-dev typed exact F1（教师银标，不是 Gold150）。

| seed | 作业 | 状态 | 选定 epoch | silver-dev typed exact |
|---|---|---|---:|---:|
| 43 | 51056（12h TIMEOUT 后已写完） | 完成 | 6 | 0.3469 |
| 42 | 51067 从 epoch_5 resume | 完成 | 6 | 0.3861 |
| 44 | 51068 | **训练中**（已绑 GPU 3） | — | — |

- 51056 原计划两卡 seed 42+43；12h 到点时 seed 43 完成，seed 42 停在 epoch 5（当时 0.3842，无 HF optimizer ckpt）。
- 51067 续训 seed 42 剩余 1 epoch，lr `1.67e-5`。epoch 6 = **0.3861**，因此选定 epoch 6。
- 51069 `qwen_s2500_sum` 等 51068 结束后汇总。

快照：`results_snapshots/qwen_silver2500_sft_20260914_seed42.json`、`..._seed43.json`、`..._STATUS.json`。

## JobBERT 新银标学生（待验证）

| 学生 | Gold150 typed exact mean | 说明 |
|---|---:|---|
| public-API Silver-2500 学生 | 0.2035 | `results_snapshots/jobbert_public_silver2500_20260913.json` |
| 合并新银标学生（7117/559） | 0.2367 | `results_snapshots/jobbert_new_silver_merged_20260914.json`；silver-dev teacher mean 0.2588 |

不可与 v6a 0.5536 比较。

## QA150 人检（新增 Silver，不是 Gold150）

冻结任务 SHA-256 `258613a73c9cd396bb6bab0ec19102b56b8fb62f6eebc81a16e6f50a25434cfe`。Doccano 画布：人层 L/K/S/T 空；L1=Astra；L2=Grok；DIFF 红。导入 `data/silver_plus_10k_prep_20260913/human_qa150/doccano/qa150.jsonl`。
