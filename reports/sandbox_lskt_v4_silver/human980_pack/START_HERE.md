# 980 句人工标 — 开始这里

测试句，**不要写入训练集**。不要覆盖 `gold_canonical_v2.jsonl`。标完重打分后才能考虑进论文主表。

## 怎么标

1. 读 `../GUIDELINES.md`（L/K/S/T；短而完整；熟悉/掌握只标对象；流程/福利空句；禁半词）。
2. 预标是 **rule_v4**，不是 Codex。三家 LLM 只在 `meta` / CSV 里当对照，不要多数决。
3. 先做 `batches/batch_01.jsonl`（50 句）。Doccano 导入后改跨度即可。
4. 没有 Doccano 时填 `worksheet.csv` 的 `human_spans`（格式同预标：`Python/S | 沟通能力/T`），空句留空。
5. `status` 从 `todo` 改成 `done`。

## 文件

| 文件 | 用途 |
|---|---|
| `doccano_rule_v4_prelabel.jsonl` | 全量 980，Doccano 导入 |
| `batches/batch_01.jsonl` … `batch_20.jsonl` | 每批 50 句 |
| `worksheet.csv` | 表格备选 |
| `manifest.json` | 句数与冲突类型 |

当前队列：980 句。rule_v4 空预标 17 句。冲突类型：{'span_mismatch': 702, 'empty_mismatch': 270, 'type_only': 8}。
