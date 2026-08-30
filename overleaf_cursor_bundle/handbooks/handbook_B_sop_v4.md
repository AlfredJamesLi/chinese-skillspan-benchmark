# 手册 B — LSKT v4 SOP（论文主协议）· 一页

**手册版本：** `B.sop_v4.2.1`（2026-08-31）。在 v4.2 上补 Python/SQL 的 S vs K 整段例句，不改四类定义、不改数字。重叠裁决见 `handbook_B_overlap_adjudication.md`；出处对照 `handbook_B_citations.md`；规则日志 `LSKT_V4_RULE_CHANGELOG.md`。新 LLM 提示词：`prompts/LSKT_V4_ANNOTATION_PROMPT.txt`。  
**文献键：** [ESCO14] [ESCO-L] [Z22] [AP08] [TKS02] [FM09] [Yu20] [UD20] [D18]。`[本协议]` = 中文招聘句上的操作化，不是被某篇论文强制的金标准。

**用途：** 论文 **主评测** 的操作性定义（短跨度、禁半词、jieba 词边界）。绑定：训练银标 `train_lskt_v4_silver`；测试金标 `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`（2601 = **980 SimHuman rule_v4** + **1621 SOP-CWS**，与 Gold v2 **同一批 ID**，预测与金标都 jieba snap）。  
**不是** 人工 Doccano Gold，**不要覆盖** `gold_canonical_v2.jsonl`。980 句是规则叠加，不是按本手册做完的全量人标。

**LLM：** P2 主表仍用**旧 dump** 事后 jieba，不是官方 `gpt-4o` 的 SOP 重呼。SOP extract 提示词（`PROMPT_gpt4o_sop_extract.txt`）与本手册一致，只作诊断表。

## 标签（仍是四类；评测可投影）

| 标签 | 含义 | 例 | 投影到 Zhang | 出处 |
|---|---|---|---|---|
| L | 自然语言：语种、水平、语言考试/证书。既是知识也是能力，故单独列支，不并进 K 也不并进 S | 英语、商务英语、英语六级、CET-6、日语N2 | → KNOWLEDGE | [ESCO-L] [本协议] |
| K | 学历、专业、领域知识、技术标准、**非语言**职业认证 | 本科及以上学历、计算机专业、ISO 27001、OCJP-Java认证 | → KNOWLEDGE | [ESCO14] [Z22] |
| S | 工具、方法、可执行职业技能（对知识的应用） | Python、Excel、维护、测试 | → SKILL | [ESCO14] [Z22] |
| T | 软技能、特质 | 沟通能力、责任心、抗压能力 | → SKILL | [ESCO14] [Z22] [本协议] |

L 对齐 ESCO skills pillar 的独立支 **Language skills and knowledge**（门户层级字母 L），与 Knowledge（K）和 Skills（S）并列，不是二者之一 [ESCO-L]。门户：[skill_main](https://esco.ec.europa.eu/en/classification/skill_main)；[ESCOpedia: Skills pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar)。概念来源 [ESCO14]。该支内部：语种名是 knowledge concept，听说读写/CEFR 是 skill；语言考试水平归 L，不归 ISCED-F 领域知识 [本协议]。评测上的 L+K→KNOWLEDGE 只是 [Z22] 二类投影，**不是** ESCO 把 L 并进 Knowledge。四类分列（含独立 T）是本资源 schema，不是 SkillSpan 原表 [Z22] [本协议]。

## 跨度（短、完整、原文）

1. 连续原文；禁止半词（`支持服`、`操作系统的问`）。[Z22] [D18] [本协议]  
2. **短而独立，优先 2–8 字/token**：`Python`、`计算机专业`、`沟通能力`。不要整段岗位职责一条 S。**[本协议]**（不要引 [Z22]：SkillSpan 跨度往往更长，且允许 K 嵌在 S 内。）切段选择见 [AP08]。  
3. 顿号/逗号/「和、与、或」连接的**独立**能力 **各自一条**。[Z22] [本协议] 同一动词统辖的并列宾语见重叠附录 [UD20]。  
4. 「熟悉 / 掌握 / 了解 / 精通 / 具备」**只标后面的对象**，不标这些动词。[Z22] [本协议]  
5. 编程语言、框架、办公软件、具体工具 → **S**。不要把 Spring/Python 标成 K。[ESCO14] [本协议]（ESCO/SkillSpan 可将 Python 列为 knowledge；本协议岗位工具用法 → S。）  
6. 语种名、语言水平、语言考试（英语六级 / CET-6 / 日语N2）→ **L**。ISO / OCJP 等技术或职业认证 → **K**。[ESCO-L] [本协议] Gold v2 / 手册 A 曾把六级标成 K，**不要用本规则去改 Gold 文件**。  
7. 报名、体检、公示、资格审查、福利、五险一金、班次、地点、鸡汤 → **空句** `spans: []`。[Z22] [本协议]  
8. 不标：形象外貌、身体健康、年限数字（只留能力本身）、非司机岗驾照。[Z22] [本协议]  
9. 平坦不重叠。一条跨度一个类型。[TKS02] [本协议] 本轮不做 nested NER [FM09] [Yu20]。L–K–S–T 只是口诀，**不是**优先级；禁止 `L > S > K > T`。[本协议] [AP08]  
10. `SQL` / `Python` 等同表面词：岗位里当工具用 → **S**（只圈光杆名）；句里当课/原理/基础/语法 → **K**，且圈**完整知识短语**，不要只圈三个字。[ESCO14] [本协议] 见下节。  
11. 人工字符偏移是权威（`sentence[start:end] == span`）。jieba 只做校验或派生视图，不是标注员，也不自动生成 Gold。[AP08] [D18] [本协议] 潜在同界/嵌套/交叉写入裁决日志，**不要**写进主层 Gold。[FM09] [Z22] 详见 `handbook_B_overlap_adjudication.md`。

## 工具名 S vs 知识短语 K（Python / SQL）

口令：岗位里**能用来做事** → 光杆名 **S**。句里**知不知道这门东西**（课程/原理/基础/语法）→ **整段知识 NP** **K**。「如」后面的举例与前面同一类型，不是自动改 K。禁止外层 S 再叠内层 K。

| 句 | 应标 | 不要 |
|---|---|---|
| 掌握常用算法编程语言，如R, Python, C等 | `R` **S**；`Python` **S**；`C` **S**。不标「掌握」；「常用算法编程语言」可不标 | 后面改成 K；整段长 S 再叠 K |
| 熟悉使用 Word，Excel，PPT | `Word` S；`Excel` S；`PPT` S | 标「熟悉使用」 |
| 计算机专业课程包括 Python、数据结构 | `计算机专业` **K**；`Python` **K**；`数据结构` **K** | Python 标 S |
| 了解 Python 语言原理 / 解释器实现 | `Python语言原理` **K**；`解释器实现` **K** | 只圈光杆 `Python` |
| 具备 Python 基础知识（后文不再要求开发） | `Python基础知识` **K** | 只圈 `Python`；标「具备」 |
| 教材：Python 语法与标准库 | `Python语法` **K**；`标准库` **K**（或一条 `Python语法与标准库` **K**） | 只圈光杆 `Python` |
| 了解 SQL 原理 / 用 SQL 查库 | 原理 → `SQL原理` **K**；查库 → `SQL` **S** | 两种许可混成一个跨度 |

## 对照例

| 句 | 手册 B | 不要 | 出处 |
|---|---|---|---|
| 熟悉使用Word，Excel，PPT等办公软件 | Word S，Excel S，PPT S | 标「熟悉使用」；或收成一条长 S | [Z22] [本协议] |
| 本科及以上学历，大学英语6级 | 学历 **K**；六级 **L** | 六级标 K（那是 Gold v2 / 手册 A） | [ESCO-L] [本协议] |
| 维护和支持服务 | `维护` S + `支持服务` S（或完整词边界） | `支持服` | [本协议] |
| 五险一金，带薪年假 | `[]` | 硬标福利 | [Z22] [本协议] |
| 掌握…如 R, Python, C | `R`/`Python`/`C` 各 **S** | 举例改 K；或只标长类别 | [本协议] |
| 了解 Python 语言原理 | `Python语言原理` **K** | 只标 `Python` | [ESCO14] [本协议] |

**主结果（仅 P2）：** JobBERT 3M v4+jieba typed exact **0.4331**；冻结 ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**。禁止写成「超过 Gold v2 上的 ChatGPT 0.6365」。
