# LSKT v4 人工范围缩小（sandbox）

Gold v2 未改。Kimi 是 `kimi-k2.6`，不是多数决 Gold。

| 队列 | 句数 | 用法 |
|---|---:|---|
| 三家完全一致 | **939** | 批量接受 |
| Codex≠豆包，Kimi=豆包 | 447 | 建议跟豆包，有空再抽查 |
| Codex≠豆包，Kimi=Codex | 73 | 建议跟 Codex，有空再抽查 |
| Codex=豆包，Kimi不同 | 162 | 次优先：两家已同，看 Kimi 是否多标/少标 |
| **三家各不相同** | **980** | **现在人工主队列** |

原先 Codex↔豆包 1500 句。用 Kimi 站边后，主队列从 1500 收到 **980**。
抽查 100 句（seed=42）：三家分裂 50 + 站边各 15 + 两家同Kimi异 20。

- 主队列: `human_must_review.csv`
- 100 句对照: `sample100_kimi_vs_codex.csv`
- 批量接受: `auto_accept_three_agree.csv`

不要写入 confirmed-results.md。不要用这些 test 句训练。
