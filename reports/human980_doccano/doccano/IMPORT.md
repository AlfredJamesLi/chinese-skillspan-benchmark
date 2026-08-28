# Doccano 导入（原 980 分歧队列）

测试句。**不要写入训练集。** 不要覆盖 `gold_canonical_v2.jsonl`。划分等 980 句标完再做。

格式：`text` + `label` + `labels` + `Comments` + `meta`。`meta.id` 是句子 ID，导出后靠它对齐。

## 建项目

1. Create → **Sequence Labeling**（序列标注 / NER）。  
2. 关闭 overlapping / 嵌套（平面四类）。  
3. 先导入标签：`labels.json`（L / K / S / T）。快捷键 l / k / s / t。  
4. Dataset → Import → **JSONL**。  
5. 列映射：文本=`text`，标签=`label`（界面若要 `labels` 也可以，两份都写了）。若有 Comment 列，映射到 `Comments`。

## 导入哪个文件

| 文件 | 用途 |
|---|---|
| `batches/batch_01.jsonl` | **先标这 50 句** |
| `batches/batch_02.jsonl` … `batch_19.jsonl` | 每批 50 |
| `batches/batch_20.jsonl` | 末批 30 |
| `human980.jsonl` | 全量 980，机器够稳可一次导入 |
| `human980_blank.jsonl` | 不要预标时才用 |
| `flagged_text_mismatch.jsonl` | 24 句空预标，可抽时间先看 |

本项目 **不要** 和 Gold v2 2601、IAA-300、repartition 预标包混在一起。

预标是 rule_v4。三模型建议只在 Comment，不要多数决。不要改 `text`。

## 导出

导出 JSONL 放到 `../exports/`（自建）。打分前把路径发回本窗口。
