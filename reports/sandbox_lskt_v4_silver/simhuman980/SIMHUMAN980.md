# Simulated SOP-v4 labels on 980 (sandbox)

Gold v2 / Codex test / train.json / train_lskt_v4 未改。不是人工 Gold，不进论文。

模拟规则：先 empty-lock，再 **rule_v4**（CRF 训练 SOP：2–8 token、完整词、熟悉/掌握只标对象）。
仅当规则把技能句放空、且至少两家 LLM 跨度 SOP 合法且一致时，才 rescue。
980 是 Gold v2 测试 ID，**没有**并进 CRF 训练集。现有 `crf_lskt_v4_silver_seed42` 预测直接重打分。

- 980 空句: **7**
- 来源: `{'rule_v4': 963, 'rescue_llm_agree2': 10, 'rule_empty': 5, 'empty_process': 1, 'empty_shiye_process': 1}`

| Gold | typed P/R/F1 | collapsed | align |
|---|---|---:|---|
| Gold v2 (frozen official) | 0.1543/0.0830/0.1079 | 0.1187 | True |
| Codex test silver (current g2ids) | 0.1257/0.1236/0.1246 | 0.1366 | True |
| rule_v4 recomputed on 2601 | 0.3442/0.2938/0.3170 | 0.3418 | True |
| patched 2601 (980 simhuman, rest Codex) | 0.2769/0.2494/0.2624 | 0.2837 | True |
| simhuman 980 only | 0.3509/0.2990/0.3229 | 0.3481 | True |

前 20 条见 `summary.json` → examples20。

