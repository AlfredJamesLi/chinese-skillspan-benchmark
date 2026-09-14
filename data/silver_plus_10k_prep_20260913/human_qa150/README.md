# 新增 Silver 人工质量检查 150

抽中不换样。不是独立盲标 Gold，也不代表全部 10,000 条质量。
不要把论文人工覆盖量改成 500，直到这 150 条人检完成。

若这 150 条以后当作 test：从学生 train/dev 去掉这些 ID 后重训；不要另抽一套替换。
当前 JobBERT 合并银标学生已经见过其中一部分（见 SAMPLING_MANIFEST overlap）。

- 任务：`qa150_human_task.jsonl`（human_label 现为 null）
- AI 原标：`qa150_ai_original.jsonl`
- 域配额：阿里云 60 / 事业单位 45 / 上市公司 45
- 与当前 student train 重叠：136；dev 重叠：10
- Doccano：`doccano/qa150.jsonl`。人标用 **L/K/S/T**（导入时空）；对照层 **L1=Astra、L2=Grok**；不一致为红 **DIFF**。对照两套机器独立打标，不要只改 Astra，也不要多数决。导入说明见 `doccano/IMPORT.md`。
