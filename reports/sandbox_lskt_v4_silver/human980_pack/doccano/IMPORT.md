# Doccano 导入（SOP 980）

测试句，**不要写入训练集**。不要覆盖 `gold_canonical_v2.jsonl`。

格式与本仓库以前用的 `doccano_imports/doccano_window.jsonl` 一致：`text` + `label` + `labels` + `meta`。

## 建项目

1. Create → **Sequence Labeling**（序列标注 / NER）。
2. 关闭 overlapping / 嵌套（本任务平面标注）。
3. 先导入标签：`labels.json`（L / K / S / T）。快捷键 l / k / s / t。
4. Dataset → Import → **JSONL** → 选下面其中一个文件。
5. 列映射：文本=`text`，标签=`label`（若界面要 `labels` 也行，两份都写了）。

## 导入哪个文件

| 文件 | 用途 |
|---|---|
| `batches/batch_01.jsonl` | **先标这 50 句** |
| `batches/batch_02.jsonl` … `batch_20.jsonl` | 每批 50 |
| `human980.jsonl` | 全量 980，一次导入 |

预标是 **rule_v4**。`meta.suggest_codex/doubao/kimi` 只是对照，不要多数决。  
`meta.id` 是 Gold v2 句子 ID，导出后靠它对齐，不要改 `text`。

## 导出后怎么还

导出 JSONL 放到本目录 `exports/`（自己建）。不要覆盖 Gold。打分前告诉我文件路径。
