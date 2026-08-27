# 手册 A / 手册 B（两页协议，不要合成一本）

投稿 **PeerJ Computer Science**。官方人标仍是 Gold v2。不要覆盖 `data/gold_canonical_v2.jsonl`。

| | 手册 A | 手册 B |
|---|---|---|
| 协议 | **P1** 官方人工 Gold v2 | **P2** 匹配 SOP+jieba |
| 中文一页 | `handbook_A_gold_v2.md` | `handbook_B_sop_v4.md` |
| 英文一页（Overleaf Methods） | `handbook_A_gold_v2.en.md` | `handbook_B_sop_v4.en.md` |
| 测试金标 | `data/gold_canonical_v2.jsonl`（2601） | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`（2601） |
| 主数字 | ChatGPT typed **0.6365**；编码器 3-seed **0.1288** | JobBERT 3M v4 exact **0.4331**；ChatGPT dump+jieba exact **0.2854** |

禁止：用手册 B 重标后的跨度替换 Gold v2；把 0.4331 与 0.6365 写进同一句 SOTA。

Overleaf 咨询稿：服务器路径 `overleaf_cursor_bundle/CODEX_PROMPT_HANDBOOK.md`；拷进 Overleaf 仓库根后为 `CODEX_PROMPT_HANDBOOK.md`。
