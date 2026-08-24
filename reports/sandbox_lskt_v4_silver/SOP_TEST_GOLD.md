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

JobBERT-zh **1M** CRF：`output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/`（不要覆盖）。同一份预测、换测试金标（typed exact / IoU≥0.5 / 差距）：

| 测试金标 | exact | partial | 差距 |
|---|---:|---:|---:|
| 规则 v4 全量 2601（train/test 同 SOP） | 0.3170 | 0.5663 | +0.249 |
| 模拟人工 980 | 0.3229 | 0.5811 | +0.258 |
| 补丁 2601（980 换 SOP，其余仍 Codex） | 0.2624 | 0.4902 | +0.228 |
| Codex 银标 2601 | 0.1246 | 0.2837 | +0.159 |

现成 3M goldstyle CRF（**未**用 v4 训练）对规则 v4 2601：exact **0.2178** / partial **0.5010**。对照：`existing_encoder_on_sop/`。

3M+v4 CRF 另开目录：`output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/`（训完才有同协议数字）。

**GitHub 备份 ≠ 论文主表。** 上表可进私有仓库；人工 SOP 金标完成并重打分后，才能考虑写入 `notes/confirmed-results.md`。0.32 是规则银标自洽，不是人工 Gold。

## SHA256（推送时）

| 文件 | SHA256 |
|---|---|
| `test_lskt_v4_rule_g2ids.jsonl` | `f5e3534d6b503a2eaa3659bdf5e2b6f23a40c91e9a441a94d52c5d085f75ef40` |
| `train_lskt_v4_silver.jsonl` | `1dbf8f447e82f2e4c2d3d5df26aaa357e53cfc39c9724d04ebb3188de747680e` |
| `dev_lskt_v4_silver.jsonl` | `005d062f9c07f84f4fd9935a79e8dbb5599b440284f8230eed862eb0428fd637` |
| `test_lskt_v4_simhuman980.jsonl` | `e8614c922620c10dc5225f973ed25878ccd957ab8c29271ab76aa2fa133d3339` |
