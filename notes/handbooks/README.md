# 编码手册与版本记录

## 当前人工编码与培训

当前手册为[2026年10月7日中英文版](reader_20261007/README.md)，基于 B.sop_v4.2.14 系列修订，提供 Word、PDF 和文件校验值。手册供阅读与后续标注参考，尚待复核的案例在相应位置注明。复现历史实验时，请使用对应批次的归档材料。[10月2日论文对齐版](reader_20261002/README.md)、[历史 Markdown](handbook_B_sop_v4.md) 和原 Word 文件继续保留。

[培训目录](training/README.md)记录 5 句＋15 句培训与正式 50 句三人独立编码；研究结果见[一致性分析](../../reproduction/agreement/finalguide_abc_20261002/README.md)。

## 历史版本与实验记录

以下按当时的实验方案和记录介绍手册 A、B、C 及早期修订。表中的评测数字、材料状态和论文位置均对应历史阶段；当前标注规则请参阅上方手册。

### 手册 A、B、C 与早期评测

**2026年8月27日的方案**采用 V4（手册 B）作为主评测。V4 测试集从 Gold v2 派生，包含同一批 2601 个 ID。原始 Gold v2 保存于 `data/gold_canonical_v2.jsonl`；V4 hybrid 为混合标签数据，与人工 Doccano 标注数据分别记录。

| | 手册 A（早期版本） | 手册 B（当时主评测，2601 条） | 手册 C（重新划分后的人工标注） |
|---|---|---|---|
| 标注与处理方案 | P1 Gold-length（Doccano 原文跨度） | **P2** 匹配 SOP+jieba | 与 B 相同 SOP，对象是 **repartition_v1 test** |
| 中文说明 | `handbook_A_gold_v2.md` | `handbook_B_sop_v4.md` | `handbook_C_human_sop_v4.md` |
| 文献出处 | 见早期版本 | `handbook_B_citations.md`（B/C 共用） | 同左 |
| 文件 | `data/gold_canonical_v2.jsonl`（归档） | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | 人工标注包 `reports/repartition_v1/human_pack/` |
| 当时论文中的用途 | 方法沿革及附录 F1 | 方案 2 金标完成前的主表结果 | 尚未完成复核，未作为主评测金标 |
| 当时记录的结果 | ChatGPT typed **0.6365**；编码器 3-seed **0.1288** | JobBERT 3M v4 exact **0.4331**；ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249** | 尚无评测结果 |

其中 980 句经过 SimHuman **rule_v4** 规则处理。当时 Table 2 的一致性分析（IAA，n=100）基于 Doccano 原文跨度。上述结果对应不同的标签来源和处理方案，比较时需结合各自的评测设置。

### 早期规则修订

以下记录各版本的主要变化。历史标签和评测结果按原批次归档。

**v4.2.14（2026-09-09）：** 在 v4.2.13 上增加 R23（案例 194 / `1838-s0008`，James1 提出的并列拆分），保留 R19–R22。Word 文件为 `Chinese_SkillSpan_中文版编码簿_v4.2.14.docx`。当时归档的提示词文件为 `PROMPT_silver_plus_v4212.txt`，生成批次使用 rev2。

**v4.2.12（2026-09-07）：** 语言考试和证书（CET-6 / 英语六级 / 日语 N2）归 **L**，与原银标 API 的分类一致，概念参照 ESCO 的 *Language skills and knowledge* 类别。ISO / OCJP 等非语言认证归 **K**。Gold v2 / 手册 A 的历史记录将六级标为 K。相关文件包括重叠标注处理附录 `handbook_B_overlap_adjudication.md`、规则日志 `LSKT_V4_RULE_CHANGELOG.md`、提示词 `prompts/LSKT_V4_ANNOTATION_PROMPT.txt` 及人工标注草稿 `reports/human980_doccano/`。按当时记录，该方案的双盲一致性分析和分歧复核后的金标尚未完成。

**v4.2.9（2026-09-05）：** 补充“售前”相关表达的边界规则：`大项目售前经验` 提取为 `大项目售前`，标 **S**，去掉“经验”。

**v4.2.8（2026-09-05）：** 补充五类判断规则：含“能力”的表达、同一词语的不同用法、“保证／确保”类表达、经验要求，以及纳入金标的条件。

**v4.2.7（2026-09-05）：** 当时的工具名规则区分岗位运用与知识要求：岗位运用提取工具名，标 **S**；课程、原理等知识要求保留完整片段，标 **K**；无法区分时按 **S**。这是该历史版本的项目规则；当前疑难记录的处理见最新手册。

**v4.2.6（2026-09-05）：** 将边界原则调整为“在语义完整的前提下尽量简短”，替代“能不拆就不拆／一个动词一条长 S”的早期做法。该版采用非嵌套标注。

**v4.2.1（2026-08-31）：** 补充 Python/SQL 对照：在岗位运用语境中提取工具名，标 **S**（如 R、Python、C）；课程、原理、基础、语法等知识要求保留完整片段，标 **K**，例如 `Python语言原理`。该版采用非嵌套标注。

**2026-08-30：** 为 B/C 操作性定义补充文献索引（`handbook_B_citations.md`）。当时“短跨度 2–8 字”的表述属于项目规则，在旧文档中以 **[本协议]** 标识。
