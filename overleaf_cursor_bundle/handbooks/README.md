# 手册 A / 手册 B

投稿 **PeerJ Computer Science**。

**2026-08-27 决定：论文主评测只用 V4（手册 B）。** V4 测试金标与 Gold v2 **同一批 2601 ID**（从 V2 派生，不是新抽样）。不要覆盖 `data/gold_canonical_v2.jsonl`。不要把 V4 hybrid 写成「人工 Doccano Gold」。

| | 手册 A（沿革） | 手册 B（论文主协议） |
|---|---|---|
| 协议 | P1 Gold-length（Doccano 源跨度） | **P2** 匹配 SOP+jieba |
| 中文一页 | `handbook_A_gold_v2.md` | `handbook_B_sop_v4.md` |
| 英文一页 | `handbook_A_gold_v2.en.md` | `handbook_B_sop_v4.en.md` |
| 文件 | `data/gold_canonical_v2.jsonl`（冻结，不改） | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` |
| 论文位置 | Methods 沿革 + **附录** F1 | **摘要 / 主结果表** |
| 数字 | ChatGPT typed **0.6365**；编码器 3-seed **0.1288** | JobBERT 3M v4 exact **0.4331**；ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249** |

980 句是 SimHuman **rule_v4** 叠加，不是按手册 B 做完的全量人标。Table 2 IAA（n=100）测的是 Doccano 源跨度，**不是** V4 hybrid。

**v4.1：** 重叠裁决 `../notes/handbooks/handbook_B_overlap_adjudication.md`（仓库路径）。证书仍为 **K**。禁止把未完成人标写成 Gold。

禁止：覆盖 Gold v2；把 **0.4331** 与 **0.6365** 写进同一句 SOTA。

Overleaf 咨询稿：服务器 `overleaf_cursor_bundle/CODEX_PROMPT_HANDBOOK.md`；拷进 Overleaf 根后为 `CODEX_PROMPT_HANDBOOK.md`。
