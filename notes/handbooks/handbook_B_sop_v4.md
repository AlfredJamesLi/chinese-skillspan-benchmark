# 手册 B — LSKT v4 SOP（论文主协议）· 一页

**手册版本：** `B.sop_v4.2.9`（2026-09-05）。四类定义以 ESCO 为权威。**唯一切段：语义不变则尽量短**。工具名按谓语分流。嵌套 Long_S 留给下一篇。经验默认剥：「大项目售前」是行内话，不留「经验」。重叠裁决与 Gold 准入见 `handbook_B_overlap_adjudication.md`；出处对照 `handbook_B_citations.md`；规则日志 `LSKT_V4_RULE_CHANGELOG.md`。  
**文献键：** [ESCO14] [EQF] [ESCO-L] [ESCO-T] [ESCO-Q] [Z22] [Say18] [AP08] [Kr95] [TKS02] [FM09] [Yu20] [UD20] [D18]。`[本协议]` = 中文招聘句上的操作化，不是被某篇论文强制的金标准。

**用途：** 论文 **主评测** 的操作性定义（短跨度、禁半词、jieba 词边界）。绑定：训练银标 `train_lskt_v4_silver`；测试金标 `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`（2601 = **980 SimHuman rule_v4** + **1621 SOP-CWS**，与 Gold v2 **同一批 ID**，预测与金标都 jieba snap）。  
**不是** 人工 Doccano Gold，**不要覆盖** `gold_canonical_v2.jsonl`。980 句是规则叠加，不是按本手册做完的全量人标。

**LLM：** P2 主表仍用**旧 dump** 事后 jieba，不是官方 `gpt-4o` 的 SOP 重呼。SOP extract 提示词（`PROMPT_gpt4o_sop_extract.txt`）与本手册一致，只作诊断表。

## 标签（类型定义 = ESCO 权威；评测可投影到 Zhang）

**权威层级：** 四类含义 **只跟 ESCO 技能柱四支**（K / L / S / T）。ESCO 与 EQF 共用 knowledge / skill 措辞。[ESCO14] [EQF]  
SkillSpan [Z22]：**不是**四类定义的出处；只用于「跨度是原文子串、态度在他们那里并进 Skill、评测二类投影」。不要用 SkillSpan 或 `L＞S＞K＞T` 改写下表。

| 本协议 | ESCO 门户支 | 权威定义（ESCO / EQF 原文） | 中文招聘操作 | 例 | 投影 [Z22] |
|---|---|---|---|---|---|
| **K** | Knowledge | *“Knowledge means the outcome of the assimilation of information through learning. Knowledge is the body of facts, principles, theories and practices that is related to a field of work or study.”* 知识术语不用动作动词。 | 领域事实/原则/理论；学历与**非语言**职业认证的**名称**（资格柱无单独标签，映射到 K） | 本科及以上学历、计算机专业、ISO 27001、PMP | → KNOWLEDGE |
| **S** | Skills | *“Skill means the ability to apply knowledge and use know-how to complete tasks and solve problems.”* | 对知识的运用：工具、方法、可执行职业动作 | 维护、测试、对接、熟悉后的 shell | → SKILL |
| **T** | Transversal skills | *“Transversal skills and competences (TSCs) are learned and proven abilities which are commonly seen as necessary or valuable for effective action in virtually any kind of work, learning or life activity. They are ‘transversal’ because they are not exclusively related to any particular context (job, occupation…).”* 社会与沟通簇含 communicating、leading others；`report facts` 在 T4.1。 | 跨行业软技能/特质。写在职责里也不改 transversal | 沟通能力、沟通管理、客户汇报、责任心 | → SKILL |
| **L** | Language skills and knowledge | ESCO 技能柱**独立第四支**（层级字母 L），与 Knowledge / Skills / Transversal **并列**，不并进 K 或 S。支内：语种名是 knowledge concept，听说读写/CEFR 是 skill。 | 语种、水平、语言考试/证书整段留在 L | 英语、英语六级、CET-6、日语N2、英文阅读能力 | → KNOWLEDGE |

**权威链接（编码时以此为准）：**  
- 技能柱四支：[skill_main](https://esco.ec.europa.eu/en/classification/skill_main) · [Skills pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar) [ESCO-L] [ESCO14]  
- Knowledge：[escopedia/knowledge](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/knowledge) [EQF]  
- Skill：[escopedia/skill](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill) [EQF]  
- Transversal / `report facts`：[TSC 2022](https://esco.ec.europa.eu/en/about-esco/publications/publication/towards-structured-and-consistent-terminology-transversal) · [report facts](https://esco.ec.europa.eu/en/classification/skills?uri=http://data.europa.eu/esco/skill/be6ab363-3de1-427f-a8ef-85d5b0250822) [ESCO-T]  
- Qualification（无 Q 标签，名称→K）：[qualifications](https://esco.ec.europa.eu/en/classification/qualifications) *“the formal outcome of an assessment and validation process…”* [ESCO-Q]

语言考试整段归 L、不归 ISCED-F 领域知识，是本协议对 [ESCO-L] 的操作化。[本协议] 评测 L+K→KNOWLEDGE、S+T→SKILL 只为对齐 SkillSpan 二类表，**不是** ESCO 把 L 并进 Knowledge、也不是把 T 并进 Skills。[Z22] [本协议]

## 冲突怎么裁（禁止总序）

ESCO 四支并列，**没有** `L＞S＞K＞T`。[ESCO14] [ESCO-L] [ESCO-T]  
SkillSpan 附录 B.3：拿不准标 **skill**；skill 优先于 knowledge；skill 优先于 attitude——那是他们**可以嵌套两列**时的兜底，不是四类总序。[Z22]  
切段（unitization）≠ 分类（typing）；不要用一条优先级同时裁边界和类型。[AP08] [Kr95]  
平坦主层一字一类 [TKS02]；嵌套是另一项任务 [FM09] [Yu20]。

**操作：**  
1. 先按成对检验（L/K、L/S、L/T、K/S、K/T、S/T），见重叠附录。  
2. 边界冲突先拆成最短完整、意义独立的跨度；拆不开只留完整 mention，备选写裁决日志。[AP08] [Z22] [Kr95]  
3. 类型仍拿不准 → 对齐 SkillSpan「If in doubt, annotate it as a skill」：标 **S**，并写 `adjudication_required`。[Z22]  
4. **禁止**把 `L＞S＞K＞T` 写成 ESCO 或 SkillSpan 的规定。[本协议]

## 学历与资格名 → K

`本科及以上学历` / `大学本科及以上` / `Bachelor Degree` → **K**。[Z22] 附录 B.2.8 把 `[Bachelor Degree]` 标 KNOWLEDGE，专业名另条。  
ESCO 把学历放在 **Qualifications** 柱，不是 skill；本协议无 Q 标签，资格名映射到 K。[ESCO-Q] [EQF]  
**不要**写成「学历壳不标」。年限数字（`5年以上`）仍不标。[Z22] [本协议]  
「及以上 / 含以上」留在学历跨度里，与完整资格名一起圈；不要只圈「本科」而丢掉「学历」。[Z22] [本协议]

## 沟通 / 汇报 → T（即使写在职责里）

`沟通能力`、`沟通管理`、`客户汇报`、`英语沟通` → **T**。[ESCO-T] [Z22] [Say18]  
ESCO：`report facts` 在 T4.1 communicating，可复用级别 transversal；社会与沟通含 communicating / leading others。[ESCO-T]  
SkillSpan 没有 T，把 communication / customer service 标成 SKILL（态度并进 skill）。[Z22] [Say18] 本协议单开 T，评测投影到 SKILL。[本协议]  
写在「负责…工作」里**不改变** ESCO 的 transversal：跨行业沟通不因职责外壳变成职业 S。[ESCO-T]  
职业动作仍是 S：`对接`、`信息梳理`（有具体业务对象）、`处理问题`+对象。[Z22] [本协议]

## 「××能力」两步检验（禁止「能做事→S」）

不要用「能做事就标 S」：沟通/科研/学习也能做事，但应是 T。[ESCO-T] [ONET] [本协议]

1. **领域依赖**：是否必须绑特定工具 / 方法 / 岗位对象？**是 → S**。`编码能力`、`产品设计能力`、`数据分析能力`。  
2. **否则看可迁移**：换行业还能问「有没有这个本事」？**是 → T**。`沟通能力`、`学习能力`、`沟通管理`。  
3. **科研能力**默认 **T**（已裁）。仅当句中出现「论文 / 实验 / 课题」且强调研究方法 → **S**。[本协议]

## 网络 / 安全 / ICT：一词三语境

同一词按语境消歧，不要查词表硬判。[Nav09] [Z22] [本协议]

| 语境 | 标志 | 标 |
|---|---|---|
| 学科 / 认证 / 专业名 | 前有专业 / 认证 / 学科 / 学历清单 | **K**。`网络安全专业`；认证里的 `安全` / `网络` |
| 规划 / 运维 / 实施对象 | 后有规划 / 运维 / 管理 / 实施 / 集成，或岗位在做这件事 | **S**。`规划网络及ICT…运维计划` → `网络` `ICT` `运维计划` 各 S |
| 泛化领域修饰 | 网络行业 / 安全领域 / ICT市场，无独立能力 | **不标** |

`保证安全` / `确保安全` 是结果状态，走下节，不要和认证「安全」混。

## 关键区分原则

先问这段是「做什么」还是「达成什么」，再决定标不标。SkillSpan：skill 常以动词起头；participation / contribute 一类通常不是 skill。[Z22] 结果/KPI 从句不标是本协议。[本协议]

- **「做什么」（动作 / 方法）→ 可能标 S**
- **「达成什么」（结果 / 目标）→ 不标**

| 片段 | 判定 | 处理 |
|---|---|---|
| 分析推广效果 | 做什么（方法） | **S** |
| 制定有效的推广策略 | 做什么（方法） | **S** |
| 优化曝光与转化率 | 做什么；拆开会漂成指标 | **一条 S**（例外，不是「能不拆就不拆」） |
| 保证流量/用户增长 | 达成什么（结果 / KPI） | **不标** |
| 确保渠道目标达成 | 达成什么 | **不标** |

「保证 / 确保」本身**永远不标**（命题态度，不是能力实体）。[PB05] [本协议] 后面单独看有没有独立能力：

| 后面是什么 | 处理 | 例 |
|---|---|---|
| 纯结果 / 状态名词 | **整段不标** | 增长、流量、目标、业绩、稳定、质量、满意度、达标、合规、可靠、高效、优质；`保证系统稳定`；`确保服务质量`；`保证安全` |
| 具体技术 / 方法对象 | **只标对象**，不标「保证」 | `确保数据备份策略有效` → `数据备份` 按运用/了解分流 |
| 动作 + 结果 | **只标动作** | `保证按SLA完成故障响应` → `故障响应` **S** |

「分析 / 制定 / 优化」后面的指标是做事对象，仍可标 S。不要因为前面有「保证」就自动全空或自动全 S。

## 「经验」何时进跨度

默认**剥「经验」**。行内话（`售前`、`开发`、`运维`）去掉「经验」仍好懂，按「语义不变则尽量短」不要留。[本协议] [Z22]

| 条件 | 处理 | 例 |
|---|---|---|
| `工作经验` / `项目经验` / `者优先` / 年限+经验 | **不标** | `5年以上工作经验` |
| 去掉「经验」仍是完整能力 / 行内话 | **剥「经验」** | `大项目售前经验` → `大项目售前` **S**；`数据分析经验` → `数据分析` **S**；`大数据开发经验` → `大数据开发` **S** |
| 剥了会半词或类型漂 | 才把「经验」留下 | 极少；写入裁决日志 |

## 「会××」口语软素质

招聘口语里「会」已经是本事本身 → **「会」进跨度**，整段 **T**。**[本协议]**  
「会」只表示「能做后面那件工具/职责」→ **仍剥「会」**。SkillSpan 把态度标成 skill，并去掉冠词等功能词。[Z22]

| 原文 | 处理 |
|---|---|
| 会聊天、会说话、会来事、会做人 | 整段 **T**（含「会」） |
| 会使用Excel、会修电脑、会写SQL | 剥「会」；后面按工具/职责标 **S** |

「善于 / 熟悉 / 掌握 / 了解 / 精通 / 具备 / 有」仍只标后面的对象：`善于与人沟通` → `与人沟通`；`有服务意识` → `服务意识`。[Z22]（附录 B.3.6：advanced knowledge of / proficient in 是 trigger，不进跨度。）

## 跨度（短、完整、原文）

1. 连续原文；`sentence[start:end] == span`。禁止半词（`支持服`、`操作系统的问`）。[Z22] [D18] [本协议] 中文无空格，半词不是合法 mention [AP08] [本协议]。  
2. **唯一切段：语义不变则尽量短**（优先 2–8 字/token）。`Python`、`计算机专业`、`沟通能力`。独立能力各一条。不要整段岗位职责一条 S。**废止**「能不拆就不拆 / 一个动词一条长 S」。**[本协议]** SkillSpan 附录 B.3.5 也是 as short as possible；不要引 [Z22] 当「必须标长」。切段见 [AP08] [Kr95]。  
3. 顿号/逗号/「和、与、或」连接的**独立**能力 **各自一条**。[Z22] 附录 B.1.2。只有拆开会半词或类型会漂，才留一条（`优化曝光与转化率`：拆开「曝光」「转化率」会漂成指标）。这不是「能不拆就不拆」。[UD20] [本协议]  
4. 「熟悉 / 掌握 / 了解 / 精通 / 具备」**只标后面的对象**，不标这些动词。[Z22] [本协议] 「会聊天」类口语软素质除外，见上节。[本协议]  
5. 编程语言、框架、办公软件、具体工具：**不是固定一类**。运用/岗位工具 → 光杆名 **S**；了解/课程/原理/基础/语法 → **整段知识短语 K**（`Python语言原理`，不要只圈 `Python`）；看不出 → **S** 并写不确定。[本协议] [EQF] ESCO 词表与 SkillSpan B.2 默认光杆 Python=K（一词一类，且他们可嵌套）；本轮平坦一层，用谓语分流，不要写成「一律 S」或「一律 K」。[ESCO14] [Z22]  
6. 语种名、语言水平、语言考试（英语六级 / CET-6 / 日语N2）→ **L**。ISO / OCJP 等技术或职业认证 → **K**。[ESCO-L] [ESCO-Q] [本协议] Gold v2 / 手册 A 曾把六级标成 K，**不要用本规则去改 Gold 文件**。  
7. 报名、体检、公示、资格审查、福利、五险一金、班次、地点、鸡汤 → **空句** `spans: []`。[Z22] 附录 B.3.12：只标与该职位相关、候选人须具备的能力；公司自我介绍不标。空句清单是本语料操作化 [本协议]。  
8. 不标：形象外貌、身体健康、年限数字（只留能力本身）、非司机岗驾照。[Z22] [本协议]  
9. 平坦不重叠。一条跨度一个类型。[TKS02] [本协议] 本轮不做 nested NER [FM09] [Yu20]。L–K–S–T 只是口诀，**不是**优先级；禁止 `L > S > K > T`。[ESCO14] [Z22] [AP08] [本协议]  
10. `SQL` / `Python` 等同表面词：岗位里当工具用 → **S**（只圈光杆名）；句里当课/原理/基础/语法 → **K**，且圈**完整知识短语**，不要只圈三个字。[ESCO14] [本协议] 见下节。  
11. 人工字符偏移是权威（`sentence[start:end] == span`）。jieba 只做校验或派生视图，不是标注员，也不自动生成 Gold。[AP08] [D18] [本协议] 潜在同界/嵌套/交叉写入裁决日志，**不要**写进主层 Gold。[FM09] [Z22] 详见 `handbook_B_overlap_adjudication.md`。
12. 「做什么」才可能是 S；「达成什么」（结果 / 目标 / KPI）不标。见上节关键区分。[Z22] [本协议]

## 工具名 S vs 知识短语 K（Python / SQL）

口令（第 3–4 点，已冻结）：同一表面可以是 S 也可以是 K，看这句话要的是「会用」还是「懂原理」。**运用 / 岗位工具** → 光杆名 **S**。**了解 / 课程 / 原理 / 基础 / 语法** → **整段知识 NP** **K**。看不出 → **S**，写 `adjudication_required`。「熟悉 / 掌握 / 了解」仍剥，改的是后面对象的类型。「如」后面的举例与前面同一类型，不是自动改 K。本轮禁止外层 S 再叠内层 K。[本协议] [EQF]  
（ESCO 词表 / SkillSpan B.2 把光杆 Python 标 K；那是一词一类 + 可嵌套。本轮平坦 BIO 跟谓语分流，评测 typed F1 不可与 SkillSpan 直接比。）

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
| 本科及以上学历，大学英语6级 | 学历 **K**；六级 **L** | 学历不标；六级标 K | [Z22] [ESCO-Q] [ESCO-L] |
| 维护和支持服务 | `维护` S + `支持服务` S（或完整词边界） | `支持服` | [Z22] [本协议] |
| 五险一金，带薪年假 | `[]` | 硬标福利 | [Z22] |
| 掌握…如 R, Python, C | `R`/`Python`/`C` 各 **S**（岗位运用） | 举例一律改 K；或只标长类别 | [本协议] |
| 了解 Python 语言原理 | `Python语言原理` **K** | 只标 `Python` | [ESCO14] [本协议] |
| 分析推广效果，保证流量/用户增长 | `分析推广效果` **S**；`制定…策略` 同类 **S** | `保证流量/用户增长` 标 S | [Z22] [本协议] |
| 编码能力 / 沟通能力 / 科研能力 | 编码 **S**；沟通 **T**；科研默认 **T** | 一律「能做事→S」 | [ESCO-T] [ONET] [本协议] |
| 认证清单「安全」；规划网络…运维计划 | `安全` **K**；`网络`/`ICT`/`运维计划` **S** | 一词固定一类 | [Nav09] [本协议] |
| 大项目售前经验 | `大项目售前` **S**（剥「经验」） | 整段连「经验」留下 | [本协议] |
| 负责与客户的沟通管理工作，…客户汇报工作 | `沟通管理` **T**；`客户汇报` **T** | 因「负责」改标 S | [ESCO-T] [Z22] |
| 拿不准且成对检验仍分不开 | 标 **S**，写裁决日志 | 套用 `L＞S＞K＞T` | [Z22] [AP08] |

**主结果（仅 P2）：** JobBERT 3M v4+jieba typed exact **0.4331**；冻结 ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**。禁止写成「超过 Gold v2 上的 ChatGPT 0.6365」。
