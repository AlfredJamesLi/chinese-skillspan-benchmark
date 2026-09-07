# Handbook B — LSKT v4 SOP (current human coding rules; English summary)

**Integrated revision:** R14–R18, final adjudication consolidation.

**Current machine prompt:** `PROMPT_silver_plus_v4212.txt` (silver_plus_v4212_rev1). References to the V4.2.11 prompt below are historical. The Word summary is exported from this text; it is not a full translation of the Chinese handbook.

**Handbook version:** `B.sop_v4.2.12` (2026-09-07; final adjudication consolidation). ESCO-informed concepts with explicit project operationalizations. Shortest-complete cuts: completeness before length. Context-sensitive tools; experience follows the distinctions below. The task remains contiguous, flat extraction. Consolidated clauses R14–R18 do not retroactively version historical data.  
**Keys:** [ESCO14] [EQF] [ESCO-L] [ESCO-T] [ESCO-Q] [Z22] [Say18] [AP08] [Kr95] [TKS02] [FM09] [Yu20] [UD20] [D18] [ONET] [Nav09] [PB05]. `[本协议]` / *this protocol* = Chinese-job operationalization, not a gold standard forced by one paper. Full entries at the end.

**Use:** current human coding rules. This revision does not retroactively change the reported evaluation protocol or results. Historical P2 bindings follow: Train silver: `train_lskt_v4_silver`. Test gold: `test_lskt_v4_cws_simhuman980_hybrid.jsonl` (2601 = 980 SimHuman rule_v4 + 1621 SOP-CWS; **same IDs as Gold v2**; jieba snap on **gold and** predictions).  
**Not** human Doccano Gold. **Do not overwrite** `gold_canonical_v2.jsonl`. The 980 overlay is rule-based, not a full human pass under this handbook.

P2 main LLM rows remain **frozen old dumps** + jieba, not an official `gpt-4o` SOP re-call.

## R14 Semantic-preserving splits and necessary long spans (user-confirmed addendum, 2026-09-07)

Explicit clarification to B.sop_v4.2.11, revision marker `boundary-addendum-20260907`. Record the new file hash; historical prompts, labels and evaluations are not retroactively changed.

Semantic completeness comes first: split independent mentions when local context preserves the requirement; retain the shortest complete longer span when splitting loses a necessary action, object, experience or intention, creates fragments, or changes the semantic type. Shared modifiers need not always be repeated inside a span. No hard length limit; no merging of independent duties. Length does not determine S. Containment alone does not justify splitting. Keep original contiguous text, flat and non-overlapping; never supply missing words.

**130:** `5.熟悉Linux基本操作和原理，在云计算、深度学习等领域者有工作实践经验优先；` Split boundaries confirmed: `Linux基本操作` S; `原理` K; separate `云计算` and `深度学习`. The latter two are S under explicit local practice, not universally S as domain names. The shared practice-experience context still informs typing even though outside the extracted spans. The earlier whole-experience-span proposal is not the confirmed boundary.

**134:** ` 任职要求： 1、熟练掌握自然语言处理NLP相关理论与技术方法；` Confirm separate spans `自然语言处理NLP相关理论` K and `技术方法`. The latter inherits the local NLP context and is K here as general methodological knowledge without explicit execution. Do not generate “NLP技术方法”. Both split spans are now K; the earlier whole-span proposal is superseded.

Necessary long spans may be logged with the shared component, semantic loss caused by splitting, final span and type, for a diagnostic subset. Length alone is not the criterion. Cases used in handbook development or correction are not independent test data; a held-out test requires separately sampled, uncontaminated cases. No test subset or experiment is created by this addendum.

Status: all 38 flagged cases have been resolved under user review/authorized rules and applied to a separately saved 100-record release. Earlier releases are preserved; unrelated legacy examples are not automatically resolved.

## Labels — ESCO concepts and project operationalizations

**Conceptual reference:** the four ESCO skills-pillar classes (Knowledge / Language skills and knowledge / Skills / Transversal). ESCO uses the EQF wording for knowledge and skill [ESCO14] [EQF]. **Do not** redefine S/K/T/L from SkillSpan or from `L＞S＞K＞T`. [Z22] supplies span and knowledge/skill examples and the optional L+K→KNOWLEDGE, S+T→SKILL comparison. Degree-to-K, industry-experience-to-broad-K and contextual tool-to-S mappings are project operationalizations, not literal ESCO concept labels.

| Tag | ESCO class | Authoritative wording (ESCO / EQF) | This protocol | Examples | → Zhang |
|---|---|---|---|---|---|
| **K** | Knowledge | *“Knowledge means the outcome of the assimilation of information through learning. Knowledge is the body of facts, principles, theories and practices that is related to a field of work or study.”* Knowledge terms do not use action verbs. | Domain facts/principles; core industry names in explicit industry-background/experience requirements (project broad K); **names** of degrees and non-language certificates (no Q label → map to K) | 本科及以上学历, ISO 27001, PMP | KNOWLEDGE |
| **S** | Skills | *“Skill means the ability to apply knowledge and use know-how to complete tasks and solve problems.”* | Applying knowledge: tools, methods, executable job actions | 维护, 测试, 接口对接, job-use shell | SKILL |
| **T** | Transversal skills | *“TSCs are learned and proven abilities … valuable for effective action in virtually any kind of work, learning or life activity … not exclusively related to any particular context (job, occupation…).”* T4.1 includes `report facts`. | Cross-occupation soft skills. A duty wrapper does not change reusability. | 沟通管理, 客户汇报, 责任心 | SKILL |
| **L** | Language skills and knowledge | A **sibling** class (hierarchy letter L), not inside K or S. Language names ≈ knowledge concepts; CEFR use ≈ skill. | Language name, level, or language exam/certificate as one L span | 英语, CET-6, 英文阅读能力 | KNOWLEDGE |

Portals: [skill_main](https://esco.ec.europa.eu/en/classification/skill_main); [knowledge](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/knowledge); [skill](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill); [TSC 2022](https://esco.ec.europa.eu/en/about-esco/publications/publication/towards-structured-and-consistent-terminology-transversal); [`report facts`](https://esco.ec.europa.eu/en/classification/skills?uri=http://data.europa.eu/esco/skill/be6ab363-3de1-427f-a8ef-85d5b0250822); [qualifications](https://esco.ec.europa.eu/en/classification/qualifications).

## Conflicts: no global rank

ESCO’s four sub-classifications are siblings; there is **no** `L＞S＞K＞T` [ESCO14] [ESCO-L] [ESCO-T]. SkillSpan App. B.3: if in doubt mark **skill**; prefer skill over knowledge/attitude — that fallback assumes **nested two-column** BIO, not a four-type rank [Z22]. Unitization ≠ typing [AP08] [Kr95]. Flat main layer: one label per token [TKS02]; nesting is another task [FM09] [Yu20].

**Do:** pairwise tests (overlap addendum) → shortest complete independent spans → if type still unresolved, provisionally mark **S** and log `adjudication_required` (not automatic Gold admission) [Z22] [AP08]. **Do not** attribute `L＞S＞K＞T` to ESCO or SkillSpan.

## Degrees / qualification names → K

`本科及以上学历` / `Bachelor Degree` → **K** (SkillSpan B.2.8) [Z22]. ESCO places degrees in the Qualifications pillar; we map the name to K [ESCO-Q] [EQF]. Do **not** write “degree shells unmarked.” Year counts (`5年以上`) stay empty [Z22] [本协议].

## Communication / reporting → T even in duties

`沟通能力` / `沟通管理` / `客户汇报` / `英语沟通` → **T** [ESCO-T] [Z22] [Say18]. ESCO `report facts` sits under T4.1 communicating (reusability: transversal) [ESCO-T]. SkillSpan/Sayfullina put communication in SKILL (no T); we keep T and project to SKILL [Z22] [本协议]. A duty wrapper (`负责…工作`) does **not** change transversal reusability [ESCO-T]. Occupation-specific technical actions stay S (`接口对接`, object-bearing `处理问题`); human liaison is not automatically S. Keep the complete `协调外部资源` as T [Z22] [本协议].

## Key distinction

Ask first whether the span is **what to do** or **what to achieve** [Z22] [本协议]. SkillSpan: skills often start with a verb; “participation / contribute” is usually not a skill [Z22]. KPI/result clauses are this protocol [本协议].

- **"What to do" (action / method) → may be S**
- **"What to achieve" (result / goal / KPI) → do not mark**

Examples: `分析推广效果` / `制定有效的推广策略` / `优化曝光与转化率` → **S**. `保证流量/用户增长` / `确保渠道目标达成` → **empty**.

## Frozen oral 会 + soft skill

If 会 is the competency itself, **keep 会**: `会聊天` / `会说话` / `会来事` / `会做人` → one **T** [本协议]. If 会 only means “can do the following tool/duty”, drop 会: `会使用Excel` → `Excel` **S**. Peel 善于 / 熟悉 / 有 [Z22] (B.3.6 triggers).

## Spans (short, complete, original)

Contiguous original substring; **no mid-word cuts** [Z22] [D18] [AP08] [本协议]. **Only cut: shortest span that keeps the meaning** (no hard length cap; the old 2–8 preference never licenses truncation) [本协议]. Split independent coordinated skills [Z22]. Keep one span when splitting would lose necessary shared material, cut a word, or change type (e.g. `优化曝光与转化率`). **Do not** apply “one verb = one long S”. Generated or nested labels are outside this task. Mark only the **object** of 熟悉/掌握/精通/了解 [Z22]. Same tool name is **S or K by predicate**: apply/job-use → bare **S**; know-that/course/principles → full NP **K**; unclear → **S** + log [EQF] [本协议] (ESCO inventory / SkillSpan B.2 default bare Python=K; this flat layer does not follow one-type-per-concept). Language names/levels/exams → **L** [ESCO-L]. ISO / OCJP / degree names → **K** [ESCO-Q] [Z22]. Applicant administration (报名/体检/公示) and benefits themselves are excluded; a sentence is empty only if it contains no eligible requirement. Recruitment, interviewing and background checks performed by a recruiter are occupational activities, not excluded applicant administration [Z22] (B.3.12: only competences the employee must have). Flat, non-overlapping [TKS02]; not nested NER [FM09] [Yu20]. **No** `L > S > K > T` [ESCO14] [Z22] [AP08]. Human offsets are Gold; jieba is a validator [AP08] [D18].

**Headline numbers (P2 only):** JobBERT 3M v4+jieba typed exact **0.4331**; frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**. Never claim these beat ChatGPT **0.6365** on Gold v2.

## 2026-09-07 correction-round rules

This is a rule-level synthesis of the user's approximately 100 correction cases, not a deduplicated 100-record adjudicated Gold release. See the [decision register](handbook_B_review_20260907.md) for unresolved cases. This English file summarizes the Chinese handbook; it is not a second, competing protocol.

### R01 — Experience and background

- Generic 工作经验 / 项目经验 / 丰富经验 without a specific field or activity: exclude.
- Explicit industry background/work experience: mark each core industry name **K**, excluding years, experience/background wrappers and preference conditions. `有银行、咨询、服务行业工作经验优先考虑` → `银行` K, `咨询` K, `服务行业` K. Keep 行业 when needed to disambiguate 服务.
- This is a **project broad-K proxy**, not an assertion that ESCO defines experience as knowledge. Company publicity, recruitment-target roles and incidental market modifiers do not qualify.
- Specific occupational activities: strip 经验 when meaning remains complete, e.g. `大项目售前`, `数据分析`, `大数据开发`, `大数据项目实施`, `BI项目实施` → S.
- Specific function/product-type experience: retain 经验 when removing it leaves only a category and changes meaning: `产品经验`, `内容型产品经验` → S. Do not generalize this to every noun + 经验.
- Exclude experience duration and 者优先. Degree qualifiers such as 及以上 remain inside the complete qualification name, e.g. `本科及以上学历` K. Generic 相关专业 is not a separate knowledge mention.

### R02–R07 — Scope, boundaries and types

1. Scope first, then boundary and type. Technical nouns in company publicity or learning benefits are not automatically requirements. 网络课程 in training reimbursement does not license an inner 网络 K; company encouragement is not automatically a personal T. Assess mixed clauses separately.
2. Executable technical methods can be S: `Linux内核调试方法` S. Theory/principles/standards can be K: `Linux系统原理`, `编码规范` K. Do not classify all 方法 as K. Preserve 方法 when necessary.
3. T can retain its object: `协调外部资源` T. Keep discriminating modifiers in `严谨的工作态度` T. A system's 稳定性 is a system property, not a person's T. Do not nest 产品文档 K inside a writing activity S.
4. Split independent tools. Preserve necessary shared material in `口头、书面表达能力` T or `KVM的开发和实施` S. Neither conjunctions nor one common verb mechanically determine splitting. Complex elliptical lists remain subject to adjudication.
5. Extract only original continuous text. Do not synthesize Memory开发经验 from a non-contiguous list. Preserve spelling, case and spaces; join screenshots against the actual sentence before assigning offsets to 缓存 or RocketMQ. Normalization is a separate field.
6. Category nouns such as framework/database/design tool do not automatically add K. Test whether they independently express a knowledge requirement. 熟悉 or 了解 alone is not a universal type switch: examine use versus explicit knowledge/principles in the full clause; unresolved cases remain logged.
7. Screenshot skills/knowledge/建议/GPT6/不一致 are annotation candidates and comparison metadata, not authority. Provisional S with adjudication_required is not final Gold. Record source, candidate/final spans, type, reason, rule ID, reviewer and version. Corrections after viewing model suggestions are not independent blind IAA.

The R IDs are defined in the shared decision register. Historical P2, Gold and IAA remain unchanged. Pending examples are not newly frozen rules.

## Silver-plus prompt review amendments R08–R13

These user-confirmed amendments apply prospectively. They do not freeze all previous suggestions or pending register entries. The matching prompt is `PROMPT_silver_plus_v4211.txt`; preserve the original v4.2.10 prompt and the v4.2.9 provenance of earlier GPT-6.0 batches.

### R08 Experience suffix and attribution

When an explicit practice-experience requirement would lose its meaning if reduced to a category, field or competition name, retain the original suffix: `工艺经验` and `机器人竞赛经验` may be **S** in that context. This does not make bare 工艺 or 机器人竞赛 universally S. Complete activities such as 数据分析 still lose the suffix; industry-background names remain broad K and generic experience remains excluded.

Retain, never invent: the suffix must occur in the continuous source span. Shared trailing 经验 requires a complete shared-span test or boundary adjudication; do not generate reconstructed labels, add E, or label 经验 alone.

ESCO [skill](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill) concerns applying knowledge and know-how to tasks; [competence](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/competence) concerns proven use of knowledge, skills and personal abilities in work or study contexts. Neither definition prescribes Chinese experience-suffix boundaries or tags. Retention and S mapping here are project operationalizations, not literal ESCO concept mappings.

### R09 Generic problem solving and methods

Without a specific occupational object, `解决问题` and `分析问题` are **T**; split them in 善于解决问题和分析问题 and remove 善于. Explicit technical/business objects require contextual S testing. A technical job title alone does not convert generic competencies to S.

`嵌入式软件设计方法` is S in the reviewed example because of the executable method and context; `计算机原理` is K. Do not equate 熟练 with use automatically. 熟悉/了解/熟练 neither enter the span nor independently determine type.

### R10 Supplementary examples and decision status

Examples 1–4 below adopt the confirmed decisions; example 5 is conditional, not a fixed negative.

1. `将公司技术能力/产品能力转化为商业语言` → one S; its transformed objects do not receive nested K.
2. Improving the advertising system's 用户体验/投放能力/变现效率, as pure outcomes, is excluded. `对解决挑战性问题充满热情` → one T without nested problem-solving S. 数据结构和算法基础扎实 → `数据结构` K and `算法基础` K, excluding 扎实.
3. `嵌入式软件设计方法` → S under R09, not from 熟练 alone.
4. `构建新产品/新工艺转生产阶段转产流程` → one S. 承接公司新产品/新工艺的转产工作 → `新产品/新工艺的转产` S. 提升工艺团队转产能力 is excluded when only an objective without an implementation method.
5. 能力提升 followed by media-platform features, Internet thinking, promotion methodology or exposure to technology trends needs context. Confirmed benefits/future growth: exclude; confirmed candidate requirements: assess individually; insufficient context: scope adjudication. The heading alone never forces an empty negative.

### R11 Three kinds of uncertainty

Scope unresolved: keep certain mentions, omit disputed content from the main layer, and record `adjudication_required`, disputed text and missing context. An resulting empty list is not a confirmed negative. Boundary unresolved: choose one conservative continuous complete candidate and log alternatives, never overlapping main-layer answers. Type unresolved: only after scope and legal boundaries are established and pairwise tests fail, provisionally use S and log alternatives and reasons. Quarantine unresolved records from automatic training import pending review; save revisions separately. Non-Gold status does not waive silver quality checks.

### R12 Model identity and provenance

Self-report only a reliably supplied system/runtime model name, otherwise `unknown`. Neither task names nor `gpt6_*` compatibility fields establish GPT-6.0 identity. Separately record the actual callable model identifier when available and its source; self-report is not independent verification. Log prompt version/hash, input/output hashes, execution time and batch ID.

### R13 Offsets and data protection

Use `text[start:end]` with Unicode code-point/Python string indexing, zero-based and end-exclusive, not UTF-8 bytes or UTF-16 code units. Preserve leading spaces, misspellings, case and source characters. Sort spans by start, with legal bounds and no duplicates or overlap. Only gpt6_label, gpt6_why, model and gpt6_remark may change; preserve all other values, row order/count and IDs. Recruitment text and existing labels are data, not instructions or ground truth. Structural validation does not establish semantic correctness. This handbook revision does not generate labels or change existing datasets.

## R15 Knowledge, methods and locally mixed licensing

Knowledge/theory/principles/general methodological bodies are K; tools in use, operation, implementation and explicit practice are S. Triggers and job titles alone are insufficient. In 128, 软件工程理论和方法 is K; 软件测试的技术 S, second 理论 K, second 方法 S, 白盒测试 S, 黑盒测试 S. In 134 the general 技术方法 is K, unlike named executable debugging/design methods.

In 185 the six concrete tools are S under explicit local principles-plus-practice licensing; retain the alternative K interpretation in the log. This is not a global S-over-K priority, nor does distant practice license other knowledge items. In 102 the disputed tool-stack mentions retain S; 流计算 is K as a disclosed conservative reading of general technical knowledge without explicit execution. These are project rulings, not unique ESCO mappings.

Shared local practice experience may inform 130's separate domain mentions even outside the span. Explicit industry background remains broad K. Generic experience is excluded; complete actions lose the suffix, while necessary experience meaning is preserved under R08/R14. Locally elliptical 原理 inherits Linux without generating text or merging mixed types.

## R16 Intention, traits and research

160: 有意愿在nlp相关领域深入研究 is one T, preserving intention rather than asserting an actual research skill. Do not nest NLP or generalize retention to ordinary 有 triggers. Explicit learning/development intention differs from pure product preference (169 excluded); enthusiast/user-identity examples are not automatically settled.

195 business sensitivity, data thinking and data-decision awareness, and 197 data sensitivity in a traits list are T; concrete data analysis/modeling can be S. 158 academic research follows the existing default T rule; unspecified competition experience is not reconstructed. Annotation captures stated requirements, not measured competence. Conceptual support for learning intention: [ESCO expert report §5.3](https://esco.ec.europa.eu/system/files/2022-05/MSWG%2014-04%20Report%20of%20the%20expert%20group%20on%20transversal%20skills%20and%20competences.pdf); Chinese boundaries are project decisions.

## R17 Professional functions, coordination and outcomes

Cross-industry use does not entail T: project management as a named professional function in 152 and reviewed product/translation contexts is S; generic organizing/leading remains T, courses/principles may be K. See [ESCO reusability levels](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill-reusability-level).

153 translation-resource interface is liaison T, not software development; 154 developing/reserving translation resources is S. Resource coordination remains T. In 124 quality assurance alongside testing is S, unlike promising a quality outcome; never strip 保证 mechanically from that occupational term.

127 generic workplace reflection/improvement is T; 117 analysis inherits the adjacent cloud fault object and is S. Retain necessary long objects in 102; in 179 extract document preparation/review, not each preceding lifecycle stage as a separate duty. Shorten 103 product exploration; split architecture-design and operations in 120. Preserve shared heads in 129 testing, 143 consultation and 167 design lists; do not invent missing verbs or nest object K.

## R18 Provenance and release boundaries

The 38 decisions comprise 31 user-reviewed recommendations, two conditionally authorized literature-supported cases and five resolved under the accepted knowledge/use rule. Not blind IAA; preserve the provenance of 102's 流计算 K interpretation.

The reviewed release has 100 records, 419 spans (K87/S255/T77/L0), 13 records with actual label/boundary changes, 62 originally unflagged records entirely unchanged, and zero pending records. These are version counts, not accuracy/reliability. This handbook consolidates already-applied decisions; do not retrospectively claim the model originally ran with v4.2.12. Preserve original protocol/model/execution data, hashes and adjudication logs.

Retain historical pending entries with current case overrides, without treating all legacy P01–P10 topics as resolved. Future uncertain cases follow R11. Long/shared-span examples support diagnostics, not an independent test if used for rules or training. No new training/test or changes to historical Gold/IAA/results. This edition includes Chinese Word, English-summary Word and the V4.2.12 prompt. Previous editions remain preserved. Companion appendices have not undergone a full new audit; remote publication is established by the GitHub commit, not by local file existence.

## References

Bracket keys in the text match the entries below. `[本协议]` / *this protocol* is not a publication. See `handbook_B_citations.md` for what each source licenses.

1. **[ESCO14]** le Vrang, M., Papantoniou, A., Pauwels, E., Fannes, P., Vandensteen, D., and De Smedt, J. 2014. ESCO: Boosting job matching in Europe with semantic interoperability. *Computer* 47(10):57–64. DOI: 10.1109/MC.2014.283. Portal: [skill_main](https://esco.ec.europa.eu/en/classification/skill_main); [Skills pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar); [Knowledge](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/knowledge); [Skill](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill).

2. **[EQF]** European Union. 2017. Council Recommendation of 22 May 2017 on the European Qualifications Framework for lifelong learning (2017/C 189/03). *OJ C* 189:15–28.

3. **[ESCO-L]** European Commission. ESCO skills pillar, class *Language skills and knowledge* (hierarchy letter L). https://esco.ec.europa.eu/en/classification/skill_main ; https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar

4. **[ESCO-T]** European Commission / Cedefop. 2022. *Towards a structured and consistent terminology on transversal skills and competences.* https://esco.ec.europa.eu/en/about-esco/publications/publication/towards-structured-and-consistent-terminology-transversal ; `report facts`: http://data.europa.eu/esco/skill/be6ab363-3de1-427f-a8ef-85d5b0250822

5. **[ESCO-Q]** European Commission. ESCO *Qualifications* pillar. https://esco.ec.europa.eu/en/classification/qualifications

6. **[Z22]** Zhang, M., Jensen, K. N., Sonniks, S., and Plank, B. 2022. SkillSpan: Hard and Soft Skill Extraction from English Job Postings. In *NAACL-HLT*, 4962–4984. https://aclanthology.org/2022.naacl-main.366/

7. **[Say18]** Sayfullina, L., Malmi, E., and Kannala, J. 2018. Learning Representations for Soft Skill Matching. In *AIST 2018*, LNCS 11179, 141–152. https://doi.org/10.1007/978-3-030-11027-7_15

8. **[AP08]** Artstein, R., and Poesio, M. 2008. Inter-Coder Agreement for Computational Linguistics. *Computational Linguistics* 34(4):555–596. https://aclanthology.org/J08-4004/

9. **[Kr95]** Krippendorff, K. 1995. On the reliability of unitizing contiguous data. *Sociological Methodology* 25:47–76.

10. **[TKS02]** Tjong Kim Sang, E. F. 2002. Introduction to the CoNLL-2002 Shared Task. In *CoNLL*. https://aclanthology.org/W02-2024/

11. **[FM09]** Finkel, J. R., and Manning, C. D. 2009. Nested Named Entity Recognition. In *EMNLP*, 141–150. https://aclanthology.org/D09-1015/

12. **[Yu20]** Yu, J., Bohnet, B., and Poesio, M. 2020. Named Entity Recognition as Dependency Parsing. In *ACL*, 6470–6476. https://aclanthology.org/2020.acl-main.577/

13. **[UD20]** Nivre, J., de Marneffe, M.-C., Ginter, F., Hajič, J., Manning, C. D., Pyysalo, S., Schuster, S., Tyers, F., and Zeman, D. 2020. Universal Dependencies v2: An Evergrowing Multilingual Treebank Collection. In *LREC*, 4034–4043. https://aclanthology.org/2020.lrec-1.497/

14. **[D18]** Nakayama, H., Kubo, T., Kamura, J., Taniguchi, Y., and Liang, X. 2018. doccano. https://github.com/doccano/doccano

15. **[ONET]** Peterson, N. G., Mumford, M. D., Borman, W. C., Jeanneret, P. R., Fleishman, E. A., Levin, K. Y., Campion, M. A., Mayfield, M. S., Morgeson, F. P., Pearlman, K., Gowing, M. K., Lancaster, A. R., Silver, M. B., and Dye, D. M. 2001. Understanding Work Using the Occupational Information Network (O*NET). *Personnel Psychology* 54(2):451–477.

16. **[Nav09]** Navigli, R. 2009. Word Sense Disambiguation: A Survey. *ACM Computing Surveys* 41(2):1–69.

17. **[PB05]** Palmer, M., Gildea, D., and Kingsbury, P. 2005. The Proposition Bank: An Annotated Corpus of Semantic Roles. *Computational Linguistics* 31(1):71–106.

Gold admission (“agreement ≠ correctness”) also uses **[LK77]** Landis, J. R., and Koch, G. G. 1977. The Measurement of Observer Agreement for Categorical Data. *Biometrics* 33(1):159–174 (overlap addendum).
