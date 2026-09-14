# Doccano 导入（新增 Silver 人检 150）

冻结 150 句，**不要写入训练集**。抽中不换样。不是独立盲标 Gold，也不是 Gold150。

**协议：对照两套机器标，用人层 L/K/S/T 独立打标。不要只改 Astra，也不要多数决合并。**

导入时人层为空；画布只预填机器对照层。

| 标签 | 谁 | 颜色 | 快捷键 |
|---|---|---|---|
| **L / K / S / T** | **人标工作层（导入时空）** | 蓝 / 绿 / 橙 / 紫 | l k s t |
| L1 / K1 / S1 / T1 | gpt-6-astra 对照（只看不改） | 深蓝同族 | 5 6 7 8 |
| L2 / K2 / S2 / T2 | Cursor-Grok 对照（只看不改） | 浅色同族 | 1 2 3 4 |
| **DIFF** | 两套占用不一致的字 | **红** | d |

一致句：L1 与 L2 叠在同一跨度上。不一致句：另有红 DIFF。Comments 里有两套摘要。

## 建项目

1. Create → **Sequence Labeling**。
2. **打开 overlapping**（人层会叠在机器层上）。可开嵌套。
3. 先导入 `labels.json`（**13** 个标签）。
4. Dataset → Import → **JSONL**。文本=`text`，标签=`label`。
5. 若界面有 Comments 列，会显示 Astra / Grok 对照摘要。

## 导入哪个文件

| 文件 | 用途 |
|---|---|
| **`qa150.jsonl`**（同 `doccano_qa150_dual.jsonl`） | 全量 150：人层空 + Astra L1 + Grok L2 + 红 DIFF |
| `batches/batch_01.jsonl` | 先标 50 句 |
| `doccano_qa150_astra_prelabel.jsonl` | 仅 Astra 的 L/K/S/T（关 overlapping 时用，不是人检主文件） |
| `doccano_qa150_grok_prelabel.jsonl` | 仅 Grok |

已导入旧版的项目：请先重新导入 `labels.json`（13 类），再导入本 `qa150.jsonl`。

`meta.id` 是冻结句子 ID，不要改 `text`。不要改 L1/L2/DIFF。导出后我们只保留你画的 L/K/S/T。

## 导出后怎么还

人标 JSONL 放到本目录 `exports/`。不要覆盖 Gold150 / v6a / `qa150_human_task.jsonl`。
