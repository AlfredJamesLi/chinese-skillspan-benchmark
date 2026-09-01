# Sonnet 4.6 第一轮 → 人工复核

预标是 **claude-sonnet-4-6**（SOP v4）。这不是 Gold，不要写入训练集。

1. 读 `../GUIDELINES.md`。
2. Doccano 先导入 `../doccano/labels.json`（L/K/S/T）。
3. 再导入 `batches/batch_01.jsonl`（50 句），改跨度即可。
4. 全量：`doccano_sonnet46.jsonl`。
5. 或填 `worksheet_review.csv` 的 `human_spans`。

`meta.unaligned` 非空的句子请重点看。
