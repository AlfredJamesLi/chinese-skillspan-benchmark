# Handbook B — LSKT v4 SOP (paper main protocol), one page

**Handbook version:** `B.sop_v4.2.9` (2026-09-05). ESCO-authoritative types. Shortest-complete cuts. Tools by predicate. Peel 经验 by default (`大项目售前经验` → `大项目售前` S). Nested Long_S is the next paper.  
**Keys:** [ESCO14] [EQF] [ESCO-L] [ESCO-T] [ESCO-Q] [Z22] [Say18] [AP08] [Kr95] [TKS02] [FM09] [Yu20] [UD20] [D18] [ONET] [Nav09] [PB05]. `[本协议]` / *this protocol* = Chinese-job operationalization, not a gold standard forced by one paper. Full entries at the end.

**Use:** the **reported** evaluation operationalization. Train silver: `train_lskt_v4_silver`. Test gold: `test_lskt_v4_cws_simhuman980_hybrid.jsonl` (2601 = 980 SimHuman rule_v4 + 1621 SOP-CWS; **same IDs as Gold v2**; jieba snap on **gold and** predictions).  
**Not** human Doccano Gold. **Do not overwrite** `gold_canonical_v2.jsonl`. The 980 overlay is rule-based, not a full human pass under this handbook.

P2 main LLM rows remain **frozen old dumps** + jieba, not an official `gpt-4o` SOP re-call.

## Labels — ESCO is the authority (Zhang projection is eval-only)

**Authority:** type meanings follow the four ESCO skills-pillar classes (Knowledge / Language skills and knowledge / Skills / Transversal). ESCO uses the EQF wording for knowledge and skill [ESCO14] [EQF]. **Do not** redefine S/K/T/L from SkillSpan or from `L＞S＞K＞T`. [Z22] is span unitization + the optional L+K→KNOWLEDGE, S+T→SKILL projection only.

| Tag | ESCO class | Authoritative wording (ESCO / EQF) | This protocol | Examples | → Zhang |
|---|---|---|---|---|---|
| **K** | Knowledge | *“Knowledge means the outcome of the assimilation of information through learning. Knowledge is the body of facts, principles, theories and practices that is related to a field of work or study.”* Knowledge terms do not use action verbs. | Domain facts/principles; **names** of degrees and non-language certificates (no Q label → map to K) | 本科及以上学历, ISO 27001, PMP | KNOWLEDGE |
| **S** | Skills | *“Skill means the ability to apply knowledge and use know-how to complete tasks and solve problems.”* | Applying knowledge: tools, methods, executable job actions | 维护, 测试, 对接, shell | SKILL |
| **T** | Transversal skills | *“TSCs are learned and proven abilities … valuable for effective action in virtually any kind of work, learning or life activity … not exclusively related to any particular context (job, occupation…).”* T4.1 includes `report facts`. | Cross-occupation soft skills. A duty wrapper does not change reusability. | 沟通管理, 客户汇报, 责任心 | SKILL |
| **L** | Language skills and knowledge | A **sibling** class (hierarchy letter L), not inside K or S. Language names ≈ knowledge concepts; CEFR use ≈ skill. | Language name, level, or language exam/certificate as one L span | 英语, CET-6, 英文阅读能力 | KNOWLEDGE |

Portals: [skill_main](https://esco.ec.europa.eu/en/classification/skill_main); [knowledge](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/knowledge); [skill](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill); [TSC 2022](https://esco.ec.europa.eu/en/about-esco/publications/publication/towards-structured-and-consistent-terminology-transversal); [`report facts`](https://esco.ec.europa.eu/en/classification/skills?uri=http://data.europa.eu/esco/skill/be6ab363-3de1-427f-a8ef-85d5b0250822); [qualifications](https://esco.ec.europa.eu/en/classification/qualifications).

## Conflicts: no global rank

ESCO’s four sub-classifications are siblings; there is **no** `L＞S＞K＞T` [ESCO14] [ESCO-L] [ESCO-T]. SkillSpan App. B.3: if in doubt mark **skill**; prefer skill over knowledge/attitude — that fallback assumes **nested two-column** BIO, not a four-type rank [Z22]. Unitization ≠ typing [AP08] [Kr95]. Flat main layer: one label per token [TKS02]; nesting is another task [FM09] [Yu20].

**Do:** pairwise tests (overlap addendum) → shortest complete independent spans → if type still unresolved, mark **S** and log `adjudication_required` [Z22] [AP08]. **Do not** attribute `L＞S＞K＞T` to ESCO or SkillSpan.

## Degrees / qualification names → K

`本科及以上学历` / `Bachelor Degree` → **K** (SkillSpan B.2.8) [Z22]. ESCO places degrees in the Qualifications pillar; we map the name to K [ESCO-Q] [EQF]. Do **not** write “degree shells unmarked.” Year counts (`5年以上`) stay empty [Z22] [本协议].

## Communication / reporting → T even in duties

`沟通能力` / `沟通管理` / `客户汇报` / `英语沟通` → **T** [ESCO-T] [Z22] [Say18]. ESCO `report facts` sits under T4.1 communicating (reusability: transversal) [ESCO-T]. SkillSpan/Sayfullina put communication in SKILL (no T); we keep T and project to SKILL [Z22] [本协议]. A duty wrapper (`负责…工作`) does **not** change transversal reusability [ESCO-T]. Occupation-specific actions stay S (`对接`, object-bearing `处理问题`) [Z22] [本协议].

## Key distinction

Ask first whether the span is **what to do** or **what to achieve** [Z22] [本协议]. SkillSpan: skills often start with a verb; “participation / contribute” is usually not a skill [Z22]. KPI/result clauses are this protocol [本协议].

- **"What to do" (action / method) → may be S**
- **"What to achieve" (result / goal / KPI) → do not mark**

Examples: `分析推广效果` / `制定有效的推广策略` / `优化曝光与转化率` → **S**. `保证流量/用户增长` / `确保渠道目标达成` → **empty**.

## Frozen oral 会 + soft skill

If 会 is the competency itself, **keep 会**: `会聊天` / `会说话` / `会来事` / `会做人` → one **T** [本协议]. If 会 only means “can do the following tool/duty”, drop 会: `会使用Excel` → `Excel` **S**. Peel 善于 / 熟悉 / 有 [Z22] (B.3.6 triggers).

## Spans (short, complete, original)

Contiguous original substring; **no mid-word cuts** [Z22] [D18] [AP08] [本协议]. **Only cut: shortest span that keeps the meaning** (prefer 2–8) [本协议]. Split independent coordinated skills [Z22]. Keep one span only if splitting would change type (e.g. `优化曝光与转化率`). **Do not** apply “one verb = one long S”. Nested Long_S is the next paper. Mark only the **object** of 熟悉/掌握/精通/了解 [Z22]. Same tool name is **S or K by predicate**: apply/job-use → bare **S**; know-that/course/principles → full NP **K**; unclear → **S** + log [EQF] [本协议] (ESCO inventory / SkillSpan B.2 default bare Python=K; this flat layer does not follow one-type-per-concept). Language names/levels/exams → **L** [ESCO-L]. ISO / OCJP / degree names → **K** [ESCO-Q] [Z22]. 报名/体检/公示/福利 → empty [Z22] (B.3.12: only competences the employee must have). Flat, non-overlapping [TKS02]; not nested NER [FM09] [Yu20]. **No** `L > S > K > T` [ESCO14] [Z22] [AP08]. Human offsets are Gold; jieba is a validator [AP08] [D18].

**Headline numbers (P2 only):** JobBERT 3M v4+jieba typed exact **0.4331**; frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**. Never claim these beat ChatGPT **0.6365** on Gold v2.

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
