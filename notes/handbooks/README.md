# 手册 A / 手册 B / 手册 C

投稿 **PeerJ Computer Science**。

**2026-08-27 决定：论文主评测只用 V4（手册 B）。** V4 测试金标与 Gold v2 **同一批 2601 ID**（从 V2 派生，不是新抽样）。不要覆盖 `data/gold_canonical_v2.jsonl`。不要把 V4 hybrid 写成「人工 Doccano Gold」。

| | 手册 A（沿革） | 手册 B（旧主协议，2601） | 手册 C（新划分人标） |
|---|---|---|---|
| 协议 | P1 Gold-length（Doccano 源跨度） | **P2** 匹配 SOP+jieba | 与 B 相同 SOP，对象是 **repartition_v1 test** |
| 中文一页 | `handbook_A_gold_v2.md` | `handbook_B_sop_v4.md` | `handbook_C_human_sop_v4.md` |
| 文献出处 | （沿革，不改） | `handbook_B_citations.md`（B/C 共用） | 同左 |
| 文件 | `data/gold_canonical_v2.jsonl`（冻结，不改） | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | 人标包 `reports/repartition_v1/human_pack/` |
| 论文位置 | Methods 沿革 + **附录** F1 | 在方案2金标完成前仍是已发表主表数字 | **未完成**；未裁决不得当主金标 |
| 数字 | ChatGPT typed **0.6365**；编码器 3-seed **0.1288** | JobBERT 3M v4 exact **0.4331**；ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249** | 无；禁止编造 F1 |

980 句是 SimHuman **rule_v4** 叠加，不是按手册 B/C 做完的全量人标。Table 2 IAA（n=100）测的是 Doccano 源跨度，**不是** V4 hybrid，也不是本轮双盲 100 句。

**v4.2（2026-08-28）：** 手册 B 仍是权威 SOP。语言考试/证书（CET-6 / 英语六级 / 日语N2）归 **L**（恢复原银标 API；对齐 ESCO *Language skills and knowledge*：语言既是知识也是能力，故单独列支）。ISO / OCJP 等非语言认证仍为 **K**。Gold v2 / 手册 A 沿革仍把六级记为 K，**不改 Gold 文件**。重叠裁决附录 `handbook_B_overlap_adjudication.md`；规则日志 `LSKT_V4_RULE_CHANGELOG.md`。新提示词：`prompts/LSKT_V4_ANNOTATION_PROMPT.txt`。人标队列：`reports/human980_doccano/`（草稿）。标准化协议双盲 IAA 与裁决后 Gold **尚未存在**。

**2026-08-30：** 为 B/C 操作化定义补文献键（`handbook_B_citations.md`）。规则与数字未改。短跨度 2–8 字标 **[本协议]**，不要写成 Zhang et al. (2022) 的规定。

**v4.2.1（2026-08-31）：** 补 Python/SQL 对照：岗位用法光杆名 **S**（掌握…如 R, Python, C）；课程/原理/基础/语法标**整段** **K**（`Python语言原理`，不要只圈 `Python`）。不引入嵌套 Long_S。不改论文数字。

禁止：覆盖 Gold v2；把 **0.4331** 与 **0.6365** 写进同一句 SOTA；把未裁决人标写成 Gold。

Overleaf 咨询稿：服务器 `overleaf_cursor_bundle/CODEX_PROMPT_HANDBOOK.md`；拷进 Overleaf 根后为 `CODEX_PROMPT_HANDBOOK.md`。
