# LSKT v4 冲突表初版（sandbox）

Gold v2 未改。Kimi 尚未入库，第三列全部 `pending`。Kimi 到齐后用同一脚本重跑即可。

- 句子: **2601**（Gold v2 ID）
- Codex ↔ 豆包 一致: **1101**（空句一致 1007，有跨度一致 94）
- 不一致（建议人工先看）: **1500**
  - 跨度边界不同: 939
  - 一边空一边非空: 547
  - 边界相同类型不同: 14
- 豆包有跨度对不上原文被丢掉: 928 句
- Kimi: 0/2601

全表: `conflict_table.csv`  |  人工优先: `human_review_priority.csv`
不要写入 confirmed-results.md。不要用 test 冲突表训练。
