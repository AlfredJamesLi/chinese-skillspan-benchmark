# 980 句标注指南（手册 B / SOP v4.2）

**用途：** 给标注员。协议与 `notes/handbooks/handbook_B_sop_v4.md` 相同。  
**出处对照：** `doccano/handbook_B_citations.md`（与 `notes/handbooks/handbook_B_citations.md` 同文）。键：[ESCO14] [ESCO-L] [Z22] [AP08] [TKS02] [FM09] [Yu20] [UD20] [D18]。`[本协议]` = 本资源操作化，不是被一篇论文强制的金标准。  
**方式：** 一过预标复核——看见草稿就改，不是双盲，也不是多数决三个 LLM。  
**不是** 已完成的人工 Gold。标完之前不得写入 `confirmed-results.md`，不得覆盖 `gold_canonical_v2.jsonl`。

旧 Table 2 IAA（n=100）测的是 Gold v2 长跨度（手册 A），与本轮 **不是同一套边界**。

## 标签

| 键 | 标签 | 标什么 | 不要标成 | 出处 |
|---|---|---|---|---|
| `l` | L | 语种、水平、语言考试/证书：英语、英语六级、CET-6、日语N2 | 把六级并进 K；ISO/OCJP 才是 K | [ESCO-L] [本协议] |
| `k` | K | 学历、专业、领域知识、非语言职业认证 | Python / Spring（那是 **S**）；英语六级（那是 **L**） | [ESCO14] [Z22] |
| `s` | S | 工具、方法、可执行职业技能 | 整段岗位职责 | [ESCO14] [Z22] |
| `t` | T | 软技能、特质 | 形象外貌、身体健康 | [ESCO14] [Z22] [本协议] |

快捷键与 Doccano `labels.json` 一致：`l` `k` `s` `t` [D18]。

L 既是知识也是能力，故单独列支（对齐 ESCO *Language skills and knowledge* [ESCO-L]），不并进 K 也不并进 S。概念来源 [ESCO14]。

## 跨度规则（必须）

1. 跨度是句中**连续原文**。不要改写、不要补字。[Z22] [D18]  
2. **禁止半词**：不要 `支持服`、`操作系统的问`、`培训其`。[本协议]  
3. **短而独立，优先 2–8 字**：`Python`、`计算机专业`、`沟通能力`。不要一整段职责收成一条 S。**[本协议]**（不要引 SkillSpan 当短跨度出处 [Z22]）。切段见 [AP08]。  
4. 顿号/逗号/「和、与、或」连接的**独立**能力 → **各自一条**。[Z22] 同一动词统辖的并列宾语不要机械拆成无关 S [UD20]。  
5. 「熟悉 / 掌握 / 了解 / 精通 / 具备 / 具有」**只标后面的对象**，不标这些动词。[Z22] [本协议]  
6. 编程语言、框架、办公软件、具体工具 → **S**。[ESCO14] [本协议]  
7. 语种名、语言水平、语言考试（大学英语六级 / CET-6 / 日语N2）→ **L**。ISO / OCJP 等技术或职业认证 → **K**。[ESCO-L] [本协议]  
8. 平坦、不重叠。一条跨度一个类型。不要嵌套。[TKS02] [本协议] 嵌套是另一项任务 [FM09] [Yu20]。L–K–S–T **不是**优先级 [本协议] [AP08]。潜在同界/嵌套/交叉：能拆就拆；否则只留完整能力，备选写入裁决日志，不要猜 [AP08] [Z22]。  
9. 不标：形象外貌、身体健康、年限数字本身（只留能力）、非司机岗驾照、留学优先套话。[Z22] [本协议]

## 空句（一条都不标）

整句没有对候选人的能力要求 → 全部删掉预标。[Z22] [本协议] 常见空：

- 事业单位**流程**：报名、资格审查、笔试面试时间、准考证、体检、公示、咨询电话、岗位代码、招聘人数。  
- **福利/班次**：五险一金、带薪年假、包吃住、加班费、节日福利、班次、地点。  
- 鸡汤、公司简介、工位家具、弹性上班时刻表。  
- 仅「欢迎应届生」而无能力短语。

`empty_hint` 只是提示。句中若有明确能力短语，仍要标。

## 预标怎么用

- 黄/绿高亮是 **rule_v4 草稿**。对的留下，错的改边界或改类型，多的删，缺的补。  
- Comment 里的 Codex / 豆包 / Kimi **只是对照**。三家不一致正是这句进队列的原因，不要投票。  
- 若 Comment 以「预标已清空」开头：三个模型看的不是当前这句话，**忽略建议，按当前全文从零标**。  
- 不要改句子正文。

## 对照例

| 句 | 应标 | 不要 | 出处 |
|---|---|---|---|
| 熟悉使用Word，Excel，PPT等办公软件 | Word S，Excel S，PPT S | 标「熟悉使用」；或收成一条长 S | [Z22] [本协议] |
| 本科及以上学历，大学英语6级 | 学历 K；六级 **L** | 六级标 K（那是 Gold v2 旧规） | [ESCO-L] [本协议] |
| 维护和支持服务 | `维护` S + `支持服务` S（完整词） | `支持服` | [本协议] |
| 五险一金，带薪年假 | 空 | 硬标福利 | [Z22] [本协议] |

## 文献条目（与 `handbook_B_citations.md` 一致）

1. **[ESCO14]** le Vrang, M., et al. 2014. ESCO: Boosting job matching in Europe with semantic interoperability. *Computer* 47(10):57–64.  
2. **[ESCO-L]** ESCO *Language skills and knowledge*：[skill_main](https://esco.ec.europa.eu/en/classification/skill_main)；[Skills pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar)。  
3. **[Z22]** Zhang, M., Jensen, K. N., Sonniks, S., and Plank, B. 2022. SkillSpan. *NAACL-HLT*, 4962–4984. https://aclanthology.org/2022.naacl-main.366/  
4. **[AP08]** Artstein, R., and Poesio, M. 2008. Inter-Coder Agreement for Computational Linguistics. *CL* 34(4):555–596. https://aclanthology.org/J08-4004/  
5. **[TKS02]** Tjong Kim Sang, E. F. 2002. Introduction to the CoNLL-2002 Shared Task. https://aclanthology.org/W02-2024/  
6. **[FM09]** Finkel, J. R., and Manning, C. D. 2009. Nested Named Entity Recognition. *EMNLP*, 141–150. https://aclanthology.org/D09-1015/  
7. **[Yu20]** Yu, J., Bohnet, B., and Poesio, M. 2020. Named Entity Recognition as Dependency Parsing. *ACL*, 6470–6476. https://aclanthology.org/2020.acl-main.577/  
8. **[UD20]** Nivre, J., et al. 2020. Universal Dependencies v2. *LREC*, 4034–4043. 中文省略：https://universaldependencies.org/zh/dep/orphan.html  
9. **[D18]** Nakayama, H., et al. 2018. doccano. https://github.com/doccano/doccano  

规则与数字未改。不要把「标长技能后 exact F1 会更好」或 `L > S > K > T` 写成上述文献的规定。
