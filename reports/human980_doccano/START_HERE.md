# 980 句人工标注 — 从这里开始

这是论文原定的 **三模型分歧必须人标队列**（Codex / 豆包 / Kimi 对不上的 980 句），不是新划分后的 201 句，也不是 IAA-300。

**先把这 980 句标完。划分、写进测试金标、覆盖 hybrid，全部等标注结束再做。**

不要覆盖 `data/gold_canonical_v2.jsonl`，不要覆盖 V4 hybrid，不要把这些句写进训练集。旧包 `reports/sandbox_lskt_v4_silver/human980_pack/` 有截断正文，**不要再用**。

## 本轮怎么标

1. 读同目录 `GUIDELINES.md`（手册 B：短跨度、禁半词、平面 L/K/S/T）。  
2. Doccano 建 **一个** Sequence Labeling 项目（一过预标复核，**不是**双盲）。关闭重叠/嵌套。  
3. 先导入 `doccano/labels.json`，再导入 `doccano/batches/batch_01.jsonl`（50 句）。  
4. 预标是 SimHuman rule_v4 **草稿**，用来改错，不是答案。Codex / 豆包 / Kimi 只在 Comment / `meta` 里对照，**不要多数决**。大学英语六级仍标 **K**。潜在重叠写入 `reports/annotation_v4/adjudication_log.csv`，不要在主层给同一区间两个标签。  
5. 没有 Doccano：填 `worksheets/human980.csv` 的 `human_spans`（格式 `原文/类型|原文/类型`；空句留空）。

## 文件

| 文件 | 用途 |
|---|---|
| `GUIDELINES.md` | 标注规则 |
| `doccano/IMPORT.md` | Doccano 导入步骤 |
| `doccano/labels.json` | L / K / S / T |
| `doccano/batches/batch_01.jsonl` … `batch_20.jsonl` | 每批 50 句（末批 30） |
| `doccano/human980.jsonl` | 全量 980（带预标） |
| `doccano/human980_blank.jsonl` | 全量空标，一般不用 |
| `doccano/flagged_text_mismatch.jsonl` | 24 句正文曾对错号，已空预标，请当新句标 |
| `worksheets/human980.csv` | 无 Doccano 时 |
| `SHA256SUMS` | 冻结校验 |

## 规模

- 980 句，Gold v2 **全文**（不再用「技术设...」那种截断）。  
- 来源：人工智能招聘 741 / 阿里云 205 / 事业单位 34。  
- 分歧类型：span_mismatch 702 / empty_mismatch 270 / type_only 8。  
- 24 句 SimHuman 正文和 Gold ID 对不上：预标已清空，三模型建议也作废。名单见 `worksheets/flagged_nonexact.csv`。

导出 JSONL 放到 `exports/`（自建）。不要改 `text`，保留 `meta.id`。标完把路径发回来，再谈划分。
