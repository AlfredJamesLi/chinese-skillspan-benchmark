# 手册 B / C — 操作化定义的文献出处

**手册版本：** `B.sop_v4.2.9`（2026-09-05）。权威 SOP：`handbook_B_sop_v4.md`。重叠：`handbook_B_overlap_adjudication.md`。人标口令：`handbook_C_human_sop_v4.md`。

**权威层级（必须遵守）：**  
- **S / K / T / L 的类型定义 = ESCO 技能柱四支原文**（Knowledge / Skills / Transversal / Language skills and knowledge）。ESCO 的 knowledge / skill 措辞与 EQF 相同。[ESCO14] [EQF] [ESCO-L] [ESCO-T]  
- SkillSpan [Z22]、Sayfullina [Say18]、CoNLL/嵌套 NER 文献：**只约束跨度怎么切、IAA 怎么报、评测怎么投影**，不得改写四类定义。  
- `[本协议]` = 中文招聘句上的操作化（例如语言考试整段留 L、资格名映射 K），必须不违背上列 ESCO 定义。

**读法：** 每条规则后的方括号是出处键。不要把 Zhang et al. (2022) 的英文长跨度 F1 写进本手册。

| 键 | 文献 | 我们用它证明什么 |
|---|---|---|
| [ESCO14] | le Vrang et al., 2014, *Computer*；ESCOpedia Knowledge / Skill / Skills pillar | 技能柱；知识术语不用动词；skill = apply knowledge |
| [EQF] | EQF 2017/C 189/03；ESCO 采用同一套 knowledge / skill 定义 | Knowledge = 学习同化的事实/原则/理论/实践；Skill = 运用知识完成任务 |
| [ESCO-L] | ESCO portal *skill_main*；ESCOpedia *Skills pillar* | 独立支 **Language skills and knowledge**（层级字母 L） |
| [ESCO-T] | ESCO TSC 专家组 2022；`report facts`（T4.1 communicating） | Transversal 定义；沟通 / 汇报跨行业，不因职责外壳变职业技能 |
| [ESCO-Q] | ESCO Qualifications pillar；Europass / EQF 资格 | 学历/证书是评估后的正式结果；四类无 Q → 资格名映射 K |
| [Z22] | Zhang et al., 2022, NAACL（SkillSpan）附录 B | span 级 skill / knowledge；Bachelor Degree=K；拿不准标 skill；态度并进 skill；trigger 不进跨度 |
| [Say18] | Sayfullina et al., 2018, COLING | 招聘句软技能跨度；SkillSpan 软技能操作的前身 |
| [AP08] | Artstein & Poesio, 2008, *CL* | 切段 ≠ 分类；span IAA 不能只用预先切好单位的 κ |
| [Kr95] | Krippendorff, 1995, *Sociological Methodology* | 连续文本上的 unitizing（先定边界再分类） |
| [TKS02] | Tjong Kim Sang, 2002, CoNLL | 平坦 BIO / 一字一标签；与嵌套任务不同 |
| [FM09] | Finkel & Manning, 2009, EMNLP | 嵌套实体是合法现象，但是**另一项任务** |
| [Yu20] | Yu, Bohnet & Poesio, 2020, ACL | 嵌套/重叠用 span 打分，不是单列 BIO+CRF |
| [UD20] | Nivre et al., 2020, LREC；UD Chinese `orphan` | 并列省略（gapping）：表面是名词，底层仍是被删动词的论元 |
| [D18] | Nakayama et al., 2018, doccano | 平台：人标偏移权威；Complete 才算完成 |
| [Dec22] | Decorte et al., 2022, RecSys in HR | **阶段 B 之后**把已有 span 挂到最具体的 ESCO 细码；本轮不画框 |
| [ONET] | Peterson et al., 2001, *Personnel Psychology* | Technical / job-specific skills vs Basic / transferable skills。只用于「××能力」第二步，不改 ESCO 四类定义 |
| [Nav09] | Navigli, 2009, *ACM Computing Surveys* | 一词多义按语境消歧（网络/安全/ICT），不是词表硬判 |
| [PB05] | Palmer et al., 2005, *CL*（PropBank） | 「保证/确保」是命题态度，本身不是能力实体；宾语另判。[本协议] |
| [LK77] | Landis & Koch, 1977, *Biometrics* | κ 高只说明一致，不说明正确 |

---

## 标签：文献说了什么，本协议定了什么

| 操作化定义 | 出处 | 文献覆盖到哪；何处是本协议 |
|---|---|---|
| 四类 L / K / S / T 的**定义** | **[ESCO14] [EQF] [ESCO-L] [ESCO-T]（权威）** | 对齐 ESCO 技能柱四支。四类分列不是 SkillSpan 原表；[Z22] 只提供评测投影。 |
| **K** = 学历/资格名、专业、领域知识、技术标准、非语言职业认证 | [EQF] [ESCO14] [ESCO-Q] [Z22] | EQF/ESCO：knowledge = 学习所得事实/原则/理论/实践。SkillSpan B.2：能学会、通常不能「做」的对象；B.2.8 `[Bachelor Degree]`=K。ESCO 资格柱是 Q，本协议映射到 K。 |
| **S** = 工具、方法、可执行职业技能（对知识的应用） | [EQF] [ESCO14] [Z22] | EQF/ESCO：skill = apply knowledge to complete tasks。SkillSpan：对知识对象做事的片段标 skill；拿不准标 skill（B.3.1）。 |
| **T** = 跨行业软技能 / 特质 | [ESCO-T] [Z22] [Say18] [本协议] | ESCO transversal（T4 沟通含 report facts）。SkillSpan / Sayfullina 把软技能标成 skill。本协议单开 **T**，评测并进 SKILL。 |
| **L** = 语种、水平、语言考试/证书；不并进 K 或 S | [ESCO-L] [本协议] | ESCO 独立语言支。语言考试整段归 L 是本协议。Gold v2 / 手册 A 曾把六级标 K，**不回改该文件**。 |
| 评测 L+K→KNOWLEDGE、S+T→SKILL | [Z22] [本协议] | 只为和 SkillSpan 二类表对齐。**不是** ESCO 把 L 并进 Knowledge。 |
| 禁止 `L＞S＞K＞T`；成对检验；拿不准标 S | [ESCO14] [Z22] [AP08] [Kr95] [本协议] | ESCO 四支并列无总序。SkillSpan B.3 兜底是 prefer skill（可嵌套）。AP08/Kr95：先 unitize 再 typing。 |
| `沟通管理` / `客户汇报` → **T** | [ESCO-T] [Z22] [Say18] | ESCO `report facts` = T4.1 transversal。职责外壳不改可复用级别。SkillSpan 同类进 SKILL。 |
| 编程语言 / 办公软件 / 框架：**同一表面两种许可** | [EQF] [本协议] | **运用/岗位工具 → 光杆名 S**；**了解/课程/原理/基础/语法 → 整段知识 NP K**；看不出 → S + 日志。ESCO 词表与 SkillSpan B.2 默认光杆 Python=K（一词一类、可嵌套）。本轮平坦一层，不跟词表，也不写「一律 S」。 |
| SQL / Python：岗位使用 → 光杆名 S；课程/原理 → 整段知识 NP 为 K | [ESCO14] [EQF] [本协议] | 第 3–4 点已冻结。同一表面、两种许可（apply vs know-that）。上下文不够勿猜，写入裁决日志。 |

---

## 跨度：文献说了什么，本协议定了什么

| # | 操作化定义 | 出处 | 说明 |
|---:|---|---|---|
| 1 | 连续原文；`sentence[start:end] == span` | [Z22] [D18] [本协议] | SkillSpan / Doccano 都要求原文子串。本协议：人标字符偏移是 Gold。 |
| 1 | 禁止半词（`支持服`） | [AP08] [本协议] | 中文无空格分词；半词不是合法 mention。jieba 只校验，不生成 Gold。 |
| 2 | **唯一切段：语义不变则尽量短**（优先 2–8 字）；不要整段职责一条 S。废止「能不拆就不拆」 | **[本协议]** [AP08] [Kr95] | **不要引 [Z22] 当「必须标长」。** SkillSpan B.3.5 也是 as short as possible。嵌套 Long_S 留给下一篇。 |
| 3 | 顿号/逗号/「和、与、或」连接的**独立**能力 → 各自一条 | [Z22] [本协议] | SkillSpan B.1.2：有连词则拆。同一动词统辖**不是**默认一条长 S；拆开会漂类型才留一条（`优化曝光与转化率`）。[UD20] |
| 4 | 「熟悉 / 掌握 / 了解 / 精通 / 具备」只标后面的对象 | [Z22] [本协议] | SkillSpan B.3.6：advanced knowledge of / proficient in 是 trigger。中文这些不是 ESCO 的 apply 动词。 |
| 5 | 工具、语言、框架按谓语分流（运用 S / 了解 K） | [EQF] [本协议] | 平坦一层的操作化，不是 ESCO 词表一词一类。评测 typed F1 不可与 SkillSpan 直接比。 |
| 6 | 语种 / 水平 / 语言考试 → L；ISO / OCJP / 学历名 → K | [ESCO-L] [ESCO-Q] [Z22] | 见标签表。 |
| 7–8 | 流程、福利、鸡汤、外貌、年限数字 → 空句 | [Z22] [本协议] | SkillSpan B.3.12：只标职位要求的能力，不标公司自我介绍。空句清单是本语料操作化。 |
| 9 | 平坦、不重叠；一条跨度一个类型 | [TKS02] [Z22] [本协议] | 本轮喂标准 BERT+BIO/CRF [TKS02]。SkillSpan 用**两列**允许 S∩K；本轮主层不做 nested NER [FM09] [Yu20]。 |
| 9 | L–K–S–T 只是口诀，**禁止** `L > S > K > T` | [ESCO14] [Z22] [AP08] [本协议] | 文献没有四类总序。类型用成对规则；边界是 unitization。 |
| 10 | SQL 岗位用 S / 原理 K | [ESCO14] [本协议] | 见标签表。 |
| 11 | 人标偏移权威；jieba 只校验或派生视图 | [AP08] [D18] [本协议] | 切段由人定 [AP08]。CWS/jieba 是评测对齐，不是标注员。 |
| 11 | 同界 / 嵌套 / 交叉写入裁决日志，不进主层 Gold | [FM09] [Yu20] [Z22] [本协议] | 嵌套现象记审计；主层仍平坦。 |
| 12 | 「做什么」才可能 S；结果/KPI 不标 | [Z22] [本协议] | SkillSpan：skill 常以动词起头；participation/contribute 通常不是 skill。KPI 从句清单是本协议。 |
| 13 | 「××能力」两步：领域依赖→S，否则可迁移→T | [ESCO-T] [ONET] [本协议] | 禁止「能做事→S」。科研能力默认 T。 |
| 14 | 网络/安全/ICT 三语境（认证 K / 运维 S / 领域修饰不标） | [Nav09] [Z22] [本协议] | 一词多义，先看谓语/清单。 |
| 15 | 「保证/确保」不进跨度；纯结果整段空；有对象只标对象 | [PB05] [本协议] | 结果名词清单是本协议。 |
| 16 | 「经验」默认剥；行内话（售前/开发）去掉仍好懂 | [本协议] [Z22] | `大项目售前经验` → `大项目售前` S。只在半词/类型漂时才留「经验」。 |
| 17 | 双方一致是 Gold **候选**，不是自动准入 | [AP08] [LK77] [本协议] | 一致≠正确。第三人抽查一致句。 |

---

## 重叠裁决（附录）

| 操作 | 出处 | 说明 |
|---|---|---|
| 先拆成最短完整、意义独立的跨度 | [AP08] [Kr95] [Z22] | 先 unitize 再 typing。 |
| 宾语/修饰若只被管辖动词许可，只留完整 mention | [Z22] [UD20] | 外层 skill 覆盖 apply+对象。并列省略（v′=v）按一条 VP [UD20]。 |
| 同一 `(start,end)` 不得两标签进主层 Gold | [TKS02] [本协议] | 单列 BIO 的硬约束。 |
| 备选写入日志；交叉禁止 | [FM09] [本协议] | 交叉不是标准 nested containment。 |
| 六对冲突，不是总序；拿不准标 S | [Z22] [AP08] [ESCO-T] | L/K：语言考试 L，技术认证/学历名 K。K/S：apply vs know-that。S/T：沟通/汇报 T，具名工具或职业动作 S。 |
| 双盲、先冻 A/B 再算 IAA、再第三人裁决 | [AP08] [Z22] | SkillSpan 分 TOKEN κ 与 SPAN κ。旧 Table 2 n=100 是手册 A，**不是**本协议 IAA。 |

---

## 阶段 B（本轮不进主实验）

若日后在长 S 内补短 K，或把 span 挂 ESCO 细码：

- 导出格式对齐 [Z22]：skill 一列、knowledge 一列，允许重叠。
- 模型对齐 [Yu20] / [FM09]，不要宣称 BERT+BIO 已学会嵌套。
- 细码映射对齐 [Dec22]：已有 span 上选最具体 ESCO；找不到则 `LABEL NOT PRESENT`。`沟通管理` / `客户汇报` 应对到 T4 communicating / `report facts` [ESCO-T]。
- 并列省略的管辖范围仍需人定 [UD20]。

---

## 完整条目（可贴论文 / 手册附录）

1. **le Vrang, M.**, Papantoniou, A., Pauwels, E., Fannes, P., Vandensteen, D., and De Smedt, J. 2014. ESCO: Boosting job matching in Europe with semantic interoperability. *Computer* 47(10):57–64. DOI: 10.1109/MC.2014.283. 门户：[skill_main](https://esco.ec.europa.eu/en/classification/skill_main)；[Skills pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar)；[Knowledge](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/knowledge)；[Skill](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill)。

2. **European Union.** 2017. Council Recommendation of 22 May 2017 on the European Qualifications Framework for lifelong learning (2017/C 189/03). *OJ C* 189:15–28. ESCO 采用同一套 knowledge / skill 定义。

3. **European Commission / Cedefop.** 2022. *Towards a structured and consistent terminology on transversal skills and competences.* ESCO/EQF expert group final report. https://esco.ec.europa.eu/en/about-esco/publications/publication/towards-structured-and-consistent-terminology-transversal ；概念 `report facts`：http://data.europa.eu/esco/skill/be6ab363-3de1-427f-a8ef-85d5b0250822

4. **European Commission.** ESCO *Qualifications* pillar. https://esco.ec.europa.eu/en/classification/qualifications （资格 = 评估后的正式结果。）

5. **Zhang, M.**, Jensen, K. N., Sonniks, S., and Plank, B. 2022. SkillSpan: Hard and Soft Skill Extraction from English Job Postings. In *NAACL-HLT*, 4962–4984. https://aclanthology.org/2022.naacl-main.366/ （操作细则见 Appendix B。）

6. **Sayfullina, L.**, Malmi, E., and Kannala, J. 2018. Learning Representations for Soft Skill Matching. In *Analysis of Images, Social Networks and Texts* (AIST 2018), LNCS 11179, 141–152. https://doi.org/10.1007/978-3-030-11027-7_15 ；arXiv:1807.07741. SkillSpan §2 引用的软技能跨度前身：只标指向候选人的软技能，不标描述公司/团队的同一表面词。

7. **Artstein, R.**, and Poesio, M. 2008. Inter-Coder Agreement for Computational Linguistics. *Computational Linguistics* 34(4):555–596. https://aclanthology.org/J08-4004/

8. **Krippendorff, K.** 1995. On the reliability of unitizing contiguous data. *Sociological Methodology* 25:47–76.

9. **Tjong Kim Sang, E. F.** 2002. Introduction to the CoNLL-2002 Shared Task: Language-Independent Named Entity Recognition. In *CoNLL*. https://aclanthology.org/W02-2024/

10. **Finkel, J. R.**, and Manning, C. D. 2009. Nested Named Entity Recognition. In *EMNLP*, 141–150. https://aclanthology.org/D09-1015/

11. **Yu, J.**, Bohnet, B., and Poesio, M. 2020. Named Entity Recognition as Dependency Parsing. In *ACL*, 6470–6476. https://aclanthology.org/2020.acl-main.577/

12. **Nivre, J.**, et al. 2020. Universal Dependencies v2: An Evergrowing Multilingual Treebank Collection. In *LREC*, 4034–4043. https://aclanthology.org/2020.lrec-1.497/ ；中文省略：https://universaldependencies.org/zh/dep/orphan.html

13. **Nakayama, H.**, Kubo, T., Kamura, J., Taniguchi, Y., and Liang, X. 2018. doccano. https://github.com/doccano/doccano

14. **Decorte, J.-J.**, Deleu, J., Develder, C., and Demeester, T. 2022. Design of Negative Sampling Strategies for Distantly Supervised Skill Extraction. In *RecSys in HR*. https://arxiv.org/abs/2209.05987

15. **Peterson, N. G.**, et al. 2001. Understanding Work Using the Occupational Information Network (O*NET). *Personnel Psychology* 54(2):451–477.

16. **Navigli, R.** 2009. Word Sense Disambiguation: A Survey. *ACM Computing Surveys* 41(2):1–69.

17. **Palmer, M.**, Gildea, D., and Kingsbury, P. 2005. The Proposition Bank: An Annotated Corpus of Semantic Roles. *Computational Linguistics* 31(1):71–106.

18. **Landis, J. R.**, and Koch, G. G. 1977. The Measurement of Observer Agreement for Categorical Data. *Biometrics* 33(1):159–174.

**不要写进手册或论文的：** 标长技能后 exact span F1 会更好；标准 BERT-CRF 同时学会外层 S 与内层 K；`L > S > K > T` 来自 ESCO 或 SkillSpan；岗位工具=S 来自 SkillSpan 附录 B 或 ESCO 词表（附录 B.2 / 词表例是 Python=K）。本协议谓语分流不要写成文献强制。
