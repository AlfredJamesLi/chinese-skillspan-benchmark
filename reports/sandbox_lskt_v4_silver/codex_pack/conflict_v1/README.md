# LSKT v4 冲突表初版（sandbox）

Gold v2 未改。Kimi 列为官方 `kimi-k2.6`（思考关闭）test 52 批。

- 句子: **2601**（Gold v2 ID）
- Codex ↔ 豆包 一致: **1101**（空句一致 1007，有跨度一致 94）
- 不一致（建议人工先看 Codex↔豆包）: **1500**
  - 跨度边界不同: 939
  - 一边空一边非空: 547
  - 边界相同类型不同: 14
- 三家跨度+类型完全一致: **939**
- Kimi↔Codex 一致: 1012；Kimi↔豆包 一致: 1386
- 豆包有跨度对不上原文被丢掉: 928 句
- Kimi: 2601/2601

全表: `conflict_table.csv`  |  旧人工优先（Codex↔豆包 1500）: `human_review_priority.csv`

缩小后的队列（Kimi 站边，不是多数决）见 `REVIEW_QUEUE.md`：
- 批量接受 939：`auto_accept_three_agree.csv`
- 主队列 980：`human_must_review.csv`
- 抽查 100：`sample100_kimi_vs_codex.csv`

不要写入 confirmed-results.md。不要用 test 冲突表训练。
