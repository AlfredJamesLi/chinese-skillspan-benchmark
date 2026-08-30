# 手册 B / C — 操作化定义的文献出处

**手册版本：** 仍为 `B.sop_v4.2`。2026-08-30 只补出处，**不改**标签、边界、空句或评测数字。  
权威 SOP：`handbook_B_sop_v4.md`。重叠：`handbook_B_overlap_adjudication.md`。人标口令：`handbook_C_human_sop_v4.md`。

**读法：** 每条规则后的方括号是出处键。`[本协议]` = 中文招聘句上的操作化选择，文献只提供类比，**不是**被某篇论文强制的金标准。不要把 Zhang et al. (2022) 的英文长跨度 F1 写进本手册。

| 键 | 文献 | 我们用它证明什么 |
|---|---|---|
| [ESCO14] | le Vrang et al., 2014, *Computer* | ESCO 技能柱：Knowledge / Skill / Attitude |
| [ESCO-L] | ESCO portal *skill_main*；ESCOpedia *Skills pillar* | 独立支 **Language skills and knowledge**（层级字母 L） |
| [Z22] | Zhang et al., 2022, NAACL（SkillSpan） | 招聘句 span 级 skill / knowledge；附录 B 操作细则；嵌套用**两列** BIO，不是四类抢一格 |
| [AP08] | Artstein & Poesio, 2008, *CL* | 切段（unitization）≠ 分类；span IAA 不能只用预先切好单位的 κ |
| [TKS02] | Tjong Kim Sang, 2002, CoNLL | 平坦 BIO / 一字一标签；与嵌套任务不同 |
| [FM09] | Finkel & Manning, 2009, EMNLP | 嵌套实体是合法现象（如 `[Bank of [China]]`），但是**另一项任务** |
| [Yu20] | Yu, Bohnet & Poesio, 2020, ACL | 嵌套/重叠用 span 打分（biaffine），不是单列 BIO+CRF |
| [UD20] | Nivre et al., 2020, LREC；UD Chinese `orphan` | 并列省略（gapping）：表面是名词，底层仍是被删动词的论元 |
| [D18] | Nakayama et al., 2018, doccano | 平台：人标偏移权威；Complete 才算完成 |
| [Dec22] | Decorte et al., 2022, RecSys in HR | **阶段 B 之后**把已有 span 挂到最具体的 ESCO 细码；本轮不画框 |

---

## 标签：文献说了什么，本协议定了什么

| 操作化定义 | 出处 | 文献覆盖到哪；何处是本协议 |
|---|---|---|
| 四类 L / K / S / T，评测可投影到 Zhang 的 KNOWLEDGE / SKILL | [Z22] [ESCO14] [本协议] | [Z22] 只有 skill / knowledge 两层（态度并进 skill）。四类与 L、T 分列是本资源 schema，不是 SkillSpan 原表。 |
| **K** = 学历、专业、领域知识、技术标准、非语言职业认证 | [ESCO14] [Z22] | ESCO：knowledge = 学习所得的事实/原则/理论/实践。SkillSpan 附录 B：知识是「能学会、本身不能做」的对象。 |
| **S** = 工具、方法、可执行职业技能（对知识的应用） | [ESCO14] [Z22] | ESCO：skill = ability to apply knowledge。SkillSpan：对知识对象做事的片段标 skill。 |
| **T** = 软技能 / 特质 | [ESCO14] [Z22] [本协议] | ESCO 的 attitudes / transversal；SkillSpan 把态度标成 skill。本协议单开 **T**，不并进 S。 |
| **L** = 语种、水平、语言考试/证书；不并进 K 或 S | [ESCO-L] [本协议] | ESCO 技能柱有独立语言支（语种名≈knowledge concept，听说读写/CEFR≈skill）。语言考试整段归 L 是本协议（对齐原银标 API）。Gold v2 / 手册 A 曾把六级标 K，**不回改该文件**。 |
| 评测 L+K→KNOWLEDGE、S+T→SKILL | [Z22] [本协议] | 只为和 SkillSpan 二类表对齐。**不是** ESCO 把 L 并进 Knowledge。 |
| 编程语言 / 办公软件 / 框架，岗位可执行使用 → **S** | [ESCO14] [Z22] [本协议] | ESCO 可将 Python 等列为 knowledge；SkillSpan 允许其作 K 或嵌在 S 内。本协议：**岗位里当工具用 → S**；只有明确原理/课程才 K（见 SQL 条）。 |
| SQL / Python：岗位使用 → 光杆名 S；课程/原理/基础/语法 → 整段知识 NP 为 K | [ESCO14] [本协议] | 同一表面、两种许可（apply vs know-that）。`掌握…如 R, Python, C` 全是 S。「了解 Python 语言原理」圈 `Python语言原理` K，不要只圈三个字。上下文不够勿猜，写入裁决日志。 |

---

## 跨度：文献说了什么，本协议定了什么

| # | 操作化定义 | 出处 | 说明 |
|---:|---|---|---|
| 1 | 连续原文；`sentence[start:end] == span` | [Z22] [D18] [本协议] | SkillSpan / Doccano 都要求原文子串。本协议：人标字符偏移是 Gold。 |
| 1 | 禁止半词（`支持服`） | [本协议] | 中文无空格分词；半词不是合法 mention。jieba 只校验，不生成 Gold（下条）。 |
| 2 | **短而独立，优先 2–8 字**；不要整段职责一条 S | **[本协议]** | **不要引 [Z22] 当这条的出处。** SkillSpan 的 skill/knowledge 往往更长，且允许 knowledge 嵌在 skill 里。短跨度是 V4 为平坦 BIO 与 IAA 做的 unitization 选择 [AP08]。 |
| 3 | 顿号/逗号/「和、与、或」连接的**独立**能力 → 各自一条 | [Z22] [本协议] | SkillSpan：独立技能分开标。若是同一动词统辖的并列宾语（优化曝光与转化率），见重叠附录，不要机械拆成无关 S。 |
| 4 | 「熟悉 / 掌握 / 了解 / 精通 / 具备」只标后面的对象 | [Z22] [本协议] | SkillSpan 附录常去掉冠词等功能词。中文这些是态度/程度轻动词，不是 ESCO 意义上的 apply 动词。 |
| 5 | 工具、语言、框架 → S（见上表） | [ESCO14] [本协议] | 同上，岗位用法优先于词表默认 K。 |
| 6 | 语种 / 水平 / 语言考试 → L；ISO / OCJP → K | [ESCO-L] [本协议] | 见标签表。 |
| 7–8 | 流程、福利、鸡汤、外貌、年限数字 → 空句 | [Z22] [本协议] | SkillSpan 只标对候选人的 competence。空句清单是本语料操作化。 |
| 9 | 平坦、不重叠；一条跨度一个类型 | [TKS02] [Z22] [本协议] | 本轮喂标准 BERT+BIO/CRF [TKS02]。SkillSpan 用**两列**允许 S∩K；本轮主层不做 nested NER [FM09] [Yu20]。 |
| 9 | L–K–S–T 只是口诀，**禁止** `L > S > K > T` | [本协议] [AP08] | 文献没有这条总序。类型冲突用成对规则，边界冲突是 unitization 不是优先级。 |
| 10 | SQL 岗位用 S / 原理 K | [ESCO14] [本协议] | 见标签表。 |
| 11 | 人标偏移权威；jieba 只校验或派生视图 | [AP08] [D18] [本协议] | 切段由人定 [AP08]。CWS/jieba 是评测对齐，不是标注员。 |
| 11 | 同界 / 嵌套 / 交叉写入裁决日志，不进主层 Gold | [FM09] [Yu20] [Z22] [本协议] | 嵌套现象记审计；主层仍平坦。阶段 B 若做内层 K，格式对齐 [Z22] 双列，模型对齐 [Yu20]，另开实验。 |

---

## 重叠裁决（附录）

| 操作 | 出处 | 说明 |
|---|---|---|
| 先拆成最短完整、意义独立的跨度 | [AP08] [Z22] | 先 unitize 再 typing。 |
| 宾语/修饰若只被管辖动词许可，只留完整 mention | [Z22] [UD20] | 外层 skill 覆盖 apply+对象，同 SkillSpan「K 可嵌在 S」。并列省略（v′=v）按一条 VP，不能靠 POS 自动补空动词 [UD20]。 |
| 同一 `(start,end)` 不得两标签进主层 Gold | [TKS02] [本协议] | 单列 BIO 的硬约束。 |
| 备选写入日志；交叉禁止 | [FM09] [本协议] | 交叉不是标准 nested containment。 |
| 六对冲突（L/K … S/T），不是总序 | [本协议] [ESCO-L] | L/K：语言考试整段 L，技术认证 K [ESCO-L]。K/S：apply vs know-that [ESCO14]。S/T：特质 T，具名工具 S。 |
| 双盲、先冻 A/B 再算 IAA、再第三人裁决 | [AP08] [Z22] | SkillSpan 分 TOKEN κ 与 SPAN κ。旧 Table 2 n=100 是手册 A，**不是**本协议 IAA。A/B 文件尚未存在，禁止编造。 |

---

## 阶段 B（本轮不进主实验）

若日后在长 S 内补短 K，或把 span 挂 ESCO 细码：

- 导出格式对齐 [Z22]：skill 一列、knowledge 一列，允许重叠。
- 模型对齐 [Yu20] / [FM09]，不要宣称 BERT+BIO 已学会嵌套。
- 细码映射对齐 [Dec22]：已有 span 上选最具体 ESCO；找不到则 `LABEL NOT PRESENT`。
- 并列省略的管辖范围仍需人定 [UD20]，不能从外层 S 自动可靠拆出 K₁…Kₙ。

---

## 完整条目（可贴论文 / 手册附录）

1. **le Vrang, M.**, Papantoniou, A., Pauwels, E., Fannes, P., Vandensteen, D., and De Smedt, J. 2014. ESCO: Boosting job matching in Europe with semantic interoperability. *Computer* 47(10):57–64. DOI: 10.1109/MC.2014.283. 门户：[skill_main](https://esco.ec.europa.eu/en/classification/skill_main)；[Skills pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar)。

2. **Zhang, M.**, Jensen, K. N., Sonniks, S., and Plank, B. 2022. SkillSpan: Hard and Soft Skill Extraction from English Job Postings. In *NAACL-HLT*, 4962–4984. https://aclanthology.org/2022.naacl-main.366/ （操作细则见其 Appendix B。）

3. **Artstein, R.**, and Poesio, M. 2008. Inter-Coder Agreement for Computational Linguistics. *Computational Linguistics* 34(4):555–596. https://aclanthology.org/J08-4004/

4. **Tjong Kim Sang, E. F.** 2002. Introduction to the CoNLL-2002 Shared Task: Language-Independent Named Entity Recognition. In *CoNLL*. https://aclanthology.org/W02-2024/

5. **Finkel, J. R.**, and Manning, C. D. 2009. Nested Named Entity Recognition. In *EMNLP*, 141–150. https://aclanthology.org/D09-1015/

6. **Yu, J.**, Bohnet, B., and Poesio, M. 2020. Named Entity Recognition as Dependency Parsing. In *ACL*, 6470–6476. https://aclanthology.org/2020.acl-main.577/

7. **Nivre, J.**, et al. 2020. Universal Dependencies v2: An Evergrowing Multilingual Treebank Collection. In *LREC*, 4034–4043. https://aclanthology.org/2020.lrec-1.497/ ；中文省略：https://universaldependencies.org/zh/dep/orphan.html

8. **Nakayama, H.**, Kubo, T., Kamura, J., Taniguchi, Y., and Liang, X. 2018. doccano. https://github.com/doccano/doccano

9. **Decorte, J.-J.**, Deleu, J., Develder, C., and Demeester, T. 2022. Design of Negative Sampling Strategies for Distantly Supervised Skill Extraction. In *RecSys in HR*. https://arxiv.org/abs/2209.05987

**不要写进手册或论文的：** 标长技能后 exact span F1 会更好；标准 BERT-CRF 同时学会外层 S 与内层 K；`L > S > K > T` 来自 ESCO 或 SkillSpan。
