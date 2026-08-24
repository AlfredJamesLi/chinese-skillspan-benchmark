# LSKT v4 silver + JobBERT-zh CRF（旧 Gold v2 不动）

**`gold_canonical_v2.jsonl` 冻结。** `train.json` 不覆盖。本轨道 F1 不进论文主表 / `confirmed-results.md`。

## 操作性定义（标注仍是 LSKT 四类）

| 标签 | 含义 |
|---|---|
| L | 语种 |
| K | 学历、专业、证书、领域知识 |
| S | 工具、可执行技能、方法 |
| T | 软技能 / 特质 |

跨度：原文连续、完整词（禁半词）、长度 **2–8 token**、熟悉/掌握只标对象、流程/福利空句。评测时可再报二分类（L/K→KNOWLEDGE，S/T→SKILL），**标签时不二分类**。

## 本轮银标怎么来的

Corpus 银标 BIO → `scripts/rewrite_train_lskt_v4.py`（empty lock + 切短到 8）。  
这是 **Cursor 按新 SOP 规则改写的银标**，不是 1.7 万句人工，也还不是 Codex 逐句生成。Codex 提示在 `PROMPT_codex.md`，可后补抽查。

## 训练

- 编码器：已有 JobBERT-zh 1M MLM（不再 DAPT）
- CRF：`output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/`，seed 42
- train/dev：`data/train_lskt_v4_silver.jsonl`、`dev_lskt_v4_silver.jsonl`

## 两套测试（同一份 `test_pred.jsonl`）

1. **旧 Gold v2**（主对照，官方协议）
2. **新 SOP 测试金标** `data/test_lskt_v4_rule_g2ids.jsonl`（与 train 同 SOP；说明见 `SOP_TEST_GOLD.md`）。Codex 文件 `test_lskt_v4_silver_g2ids.jsonl` 只作对照，不是 SOP 金标。

数字见 `DUAL_EVAL.md`（sandbox，不进论文）。2026-08-24 seed42：Gold v2 typed **0.1079**（低于同编码器 goldstyle v3 的 0.1224）；v4 silver typed **0.3170**（与训练同 SOP，非人工 Gold）。
