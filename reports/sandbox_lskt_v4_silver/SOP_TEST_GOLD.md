# LSKT v4 新 SOP 测试金标（sandbox）

**不是官方 Gold。** 官方评测仍只用 `data/gold_canonical_v2.jsonl`。本文件中的 F1 不进 `notes/confirmed-results.md`、不进 PDF Table 3。

操作性定义：`GUIDELINES.md`（L/K/S/T；2–8 token；熟悉/掌握只标对象；流程/福利空句）。规则改写：`scripts/rewrite_train_lskt_v4.py`。

## 测试金标该用哪份

| 角色 | 路径 | 说明 |
|---|---|---|
| **新 SOP 测试金标（主）** | `data/test_lskt_v4_rule_g2ids.jsonl` | 与 train/dev 同一套 rule_v4，Gold v2 的 2601 个 ID |
| 训练 / 开发银标 | `data/train_lskt_v4_silver.jsonl`、`data/dev_lskt_v4_silver.jsonl` | 未覆盖 `train.json` |
| 冲突句模拟人工 | `data/test_lskt_v4_simhuman980.jsonl` | 980 句；963 来自 rule_v4 |
| Codex 银标（对照，不是 SOP 金标） | `data/test_lskt_v4_silver_g2ids.jsonl` | 切法更空/更碎 |
| 豆包 / Kimi 银标 | `data/test_lskt_v4_doubao_g2ids.jsonl`、`data/test_lskt_v4_kimi_g2ids.jsonl` | 分歧分析，多数决不当 Gold |

JobBERT-zh **1M** CRF：`output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/`（不要覆盖）。对规则测试金标 sandbox typed exact **0.3170**、typed IoU≥0.5 **0.5663**。

3M+v4 CRF 另开目录：`output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/`。

## SHA256（推送时）

| 文件 | SHA256 |
|---|---|
| `test_lskt_v4_rule_g2ids.jsonl` | `f5e3534d6b503a2eaa3659bdf5e2b6f23a40c91e9a441a94d52c5d085f75ef40` |
| `train_lskt_v4_silver.jsonl` | `1dbf8f447e82f2e4c2d3d5df26aaa357e53cfc39c9724d04ebb3188de747680e` |
| `dev_lskt_v4_silver.jsonl` | `005d062f9c07f84f4fd9935a79e8dbb5599b440284f8230eed862eb0428fd637` |
| `test_lskt_v4_simhuman980.jsonl` | `e8614c922620c10dc5225f973ed25878ccd957ab8c29271ab76aa2fa133d3339` |
