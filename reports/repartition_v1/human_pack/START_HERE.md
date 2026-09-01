# 新测试集人工标注 — 从这里开始

训练可以继续跑。本包只准备**人标材料**，不改 Gold v2、不改 V4 hybrid、不改 `data/repartition_v1/*.jsonl`。

协议：**手册 C**（与手册 B 同一套短跨度 SOP）。旧 980 SimHuman **不是**已完成人标。

## 先做什么（本周）

1. 两名标注员各自读 `GUIDELINES.md`（与 `notes/handbooks/handbook_C_human_sop_v4.md` 相同）。  
2. Doccano 建**两个** Sequence Labeling 项目（A / B），关闭重叠/嵌套。  
3. 每个项目：先导入 `doccano/labels.json`，再导入 `doccano/iaa100_batches/batch_01.jsonl`。  
4. 没有 Doccano：用 `worksheets/iaa100_annotator_A.csv` / `_B.csv`，把跨度写进 `human_spans`（格式 `原文/类型|原文/类型`）。  
5. 100 句完成后告诉我导出路径，再开 `iaa300` 剩余批次。

**不要**把预标 980 和 IAA 放进同一个项目。

## 文件

| 文件 | 给谁 | 预标 |
|---|---|---|
| `doccano/iaa100_blank.jsonl` + `iaa100_batches/` | A/B 双盲，本周 | 无 |
| `doccano/iaa300_blank.jsonl` + `iaa300_batches/` | A/B 双盲，100 句之后 | 无 |
| `doccano/iaa300_annotator_A.jsonl` / `_B.jsonl` | 两个项目各导一份（内容相同，空标签） | 无 |
| `worksheets/iaa100_*.csv` `iaa300_*.csv` | 无 Doccano 时 | 无 |
| `doccano/review980_test_prelabel.jsonl` | 复核员，**另一项目** | v4 银标草稿 |
| `adjudicator/` | 仅第三人 | 银标参考 |
| `manifests/sample_manifest.json` | 抽样冻结（种子 13，未用任何模型 F1） | — |

新 test 共 4222 句，本包**先标 100+300 IAA**，不是一次标完全集。

- IAA 100 / 300 按来源配额抽样（种子 13，未用模型 F1）：AI/Grad/Cloud/Public = 40/40/10/10 与 120/120/30/30。含测试集全部 50 句带 L 的句子（L 极稀，所以 100 句里 L 句会偏多，这是故意的）。  
- 旧 980 SimHuman：新划分后 **test 201 / train 709 / dev 70**。只复核 test 的 201 句；train/dev 那些 ID **不要当成测试金标**（见 `manifests/simhuman980_by_new_split.csv`）。

导出放到 `exports/`。覆盖 Gold 或把 IAA 写进训练集都禁止。
