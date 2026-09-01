# Doccano 导入（repartition_v1 人标）

测试句。**不要写入训练集。** 不要覆盖 `gold_canonical_v2.jsonl`。

格式与旧包一致：`text` + `label` + `labels` + `meta`。`meta.id` 是句子 ID，导出后靠它对齐。

## 建项目

1. Create → **Sequence Labeling**。  
2. 关闭 overlapping / 嵌套。  
3. 导入标签：`labels.json`（L/K/S/T，快捷键 l/k/s/t）。  
4. Dataset → Import → **JSONL**。  
5. 列映射：文本=`text`，标签=`label`（界面若要 `labels` 也可以，两份都写了）。

## 导入哪个文件

| 项目 | 文件 | 说明 |
|---|---|---|
| Annotator A（本周） | `iaa100_batches/batch_01.jsonl` 起 | 空标签，双盲 |
| Annotator B（本周） | 同上另一项目 | 不要复制 A 的已标结果 |
| A/B（100 句之后） | `iaa300_batches/` | 含本周 100 句，可跳过已标 ID |
| 预标复核（另开项目） | `review980_batches/` | 带银标，仅改错 |

一次不要把 300 和 980 混进同一项目。

## 导出

导出 JSONL 放到 `../exports/`。不要改 `text`。打分前把路径发回本窗口。
