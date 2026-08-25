# 980 句人工复核 — 开始这里

Sonnet 4.6 第一轮已打完。测试句，**不要写入训练集**，不要覆盖 `gold_canonical_v2.jsonl`。

## 怎么核

1. 读 `../GUIDELINES.md`（L/K/S/T；短而完整；熟悉/掌握只标对象；流程/福利空句；禁半词）。
2. 预标是 **claude-sonnet-4-6**（SOP v4）。rule_v4 / Codex / 豆包 / Kimi 只在 `meta` 里对照，不要多数决。
3. Doccano：导入 `doccano/labels.json`，再导入 `sonnet46_round1/batches/batch_01.jsonl`（50 句）。
4. 没有 Doccano 时填 `sonnet46_round1/worksheet_review.csv` 的 `human_spans`。
5. `unaligned` 非空的 57 句请重点看（模型写了原文对不上的片段，已丢掉）。

## 文件

| 文件 | 用途 |
|---|---|
| `sonnet46_round1/REVIEW.md` | 复核说明 |
| `sonnet46_round1/batches/batch_01.jsonl` | 先核这 50 句 |
| `sonnet46_round1/doccano_sonnet46.jsonl` | 全量 980 |
| `sonnet46_round1/worksheet_review.csv` | 表格备选 |
| `PROMPT_sonnet46.txt` | 本轮提示词 |
| `doccano/labels.json` | L/K/S/T 标签 |

第一轮：980 句，3434 条 span（S 2061 / K 867 / T 491 / L 15），空句 87。不是 Gold，不进主表。
