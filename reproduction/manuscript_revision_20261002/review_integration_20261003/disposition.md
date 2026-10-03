# Chinese-SkillSpan：逐项审查处置

2026-10-03。本文对应最新40页主稿。建议编号沿用来稿，行号以本轮源文件为准；旧PDF页码仅作为定位线索。

“采纳”指已落实文本或元数据修改，不表示补齐了新的实验。对仅有网页、发布摘要或执行回执的事项，保留相应证据边界。

## 文献 R01–R48

### R01 — 已解决

- **位置：** file: 1Introduction.tex; line: 14; citation_keys: artstein2008agreement; context: The original corpus and its smaller training, reference, and agreement subsets have distinct roles. The 150-sentence human reference contributed to guideline development, so model comparisons on it are diagnostic. External recruitment experiments provide additional task-specific comparisons. We document the role and availability of each subset following guidance on dataset documentation and annotation agreement~\citep{bender2018datastatements,gebru2021datasheets,artstein2008agreement}.; file: 5Relatedwork.tex; line: 14; citation_keys: artstein2008agreement; context: ESCO provides a multilingual vocabulary for labor-market information~\citep{levrang2014esco,ESCOv1_2_2024}. SkiLLens combines human involvement, skill extraction, and ESCO linking across European job advertisements~\citep{desanto2026skilllens}. Chinese-SkillSpan adapts ESCO's high-level categories to LSKT annotation in Chinese. The handbook specifies when tool use denotes S rather than K, when coordinated objects must retain a shared action, and when an experience qualifier belongs inside the span. Agreement analysis and adjudication consequently address both unitization and categorization~\citep{artstein2008agreement}.; file: 2Framework.tex; line: 44; citation_keys: artstein2008agreement; context: Adjudication treats scope, boundaries, and type as separate decisions~\citep{artstein2008agreement}. There is no total priority order among L, K, S, and T. Under the current handbook, a mention with settled scope and boundaries but unresolved type may receive provisional S in the adjudication record, with alternatives logged. The handbook requires exclusion of the whole unresolved record from final training targets; provisional S is not an accepted target. Same-boundary alternatives, nested candidates, and unresolved overlaps are kept in the adjudication record rather than duplicated in the flat annotation layer. \hyperref[app:a]{Appendix A} gives the full rules and their history. Each completed experiment retains the labels assigned under its original handbook.; file: tex/annotation_quality_R12.tex; line: 28; citation_keys: artstein2008agreement; context: Independent blinded coding leaves substantial span-level disagreement. Mean typed F1 is 0.663, below the planned 0.80 project target, which is not a universal reliability cutoff. Boundary F1 is higher at 0.757 (95\% CI [0.654, 0.846]), indicating additional type disagreement. Character-level $\alpha=0.817$ (95\% CI [0.755, 0.873]) measures a different unit and does not override these span disagreements~\citep{artstein2008agreement}. Of the 21 fully agreed sentences, ten are empty. The two L spans occur in one sentence, limiting category-level conclusions. Frozen labels and diagnostics accompany the \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/main/reproduction/agreement/finalguide_abc_20261002}{reproduction materials}.; file: tex/appendix_A_guide_R19.tex; line: 23; citation_keys: artstein2008agreement; context: \noindent\textit{Source key.} E: ESCO's \href{https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar}{skills hierarchy} and \href{https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/transversal-knowledge-skills-and-competences}{transversal concepts} \citep{ESCOv1_2_2024}; Q: EQF definitions \citep{council2017eqf}; Z: related annotation guidance in SkillSpan, Appendix B \citep{zhang2022skillspan}; I: unitization and categorization in agreement analysis \citep{artstein2008agreement}; P: our V4.2.14 operational decision. Combined marks indicate adaptation, not a verbatim source rule. Chinese examples and their exact boundaries are project illustrations.; file: tex/appendix_B_quality_R16.tex; line: 60; citation_keys: artstein2008agreement; context: Here $D_o=0.066$ and $D_e=0.560$, giving $\alpha=0.883$. The character coefficients and span F1 describe different units of agreement~\citep{artstein2008agreement}; the many O positions contribute to the character calculation. Agreement between two machine suggestion layers likewise measures concordance, not accuracy against an independent human reference. Export hashes, calculation code, and detailed diagnostics accompany the reproduction record.

- **判断依据：** ACL 官方元数据与当前作者、年份、卷期、页码和 DOI 相符；Survey Article 是文献类型前缀，可不纳入题名。现引文承担单位划分与类别判定的一致性背景，不能为临时 S 或项目0.80目标提供规范性依据。

- **证据层级：** 已核对官方元数据，并对照当前稿件检查方法支持范围。

- **实际处理：** 保留现有书目和一致性方法引用；未把项目临时 S 规则或一致性目标写成该文规定。

- **来源：** https://aclanthology.org/J08-4004/

### R02 — 已解决

- **位置：** file: tex/external_benchmarks/paper_methods.tex; line: 4; citation_keys: beauchemin2022fijo; context: To test whether domain-pretrained initialization helps consistently across recruitment tasks, the experiments compare XLM-R-large~\citep{conneau2020xlmr} and ESCOXLM-R~\citep{zhang2023escoxlmr}. They use six public datasets: SkillSpan~\citep{zhang2022skillspan}, Kompetencer~\citep{jensen2022kompetencer}, German ICT~\citep{gnehm2022transfer}, Green~\citep{green2022benchmark}, Sayfullina~\citep{sayfullina2018softskills}, and FIJO~\citep{beauchemin2022fijo}. Separate skill and knowledge streams in SkillSpan and Kompetencer give eight extraction tasks, each retaining its original entity types.

- **判断依据：** CAIAC正式会议页核实四位作者、2022L34、2022年及DOI。作为法语保险软技能外部数据来源相关。平台文章的CC-BY许可不自动证明本文使用的派生数据包许可。

- **证据层级：** 已核对正式出版页面、摘要及元数据。

- **实际处理：** 保留 FIJO 正式论文引用及外部任务用途；没有依据论文页面许可替数据包作授权确认。

- **尚需核实：** 本轮核实的是正式论文出处，未独立验证本文所用派生数据包的许可、完整版本与转换过程。

- **来源：** https://caiac.pubpub.org/pub/72bhunl6/release/1

### R03 — 已解决

- **位置：** file: 1Introduction.tex; line: 14; citation_keys: bender2018datastatements; context: The original corpus and its smaller training, reference, and agreement subsets have distinct roles. The 150-sentence human reference contributed to guideline development, so model comparisons on it are diagnostic. External recruitment experiments provide additional task-specific comparisons. We document the role and availability of each subset following guidance on dataset documentation and annotation agreement~\citep{bender2018datastatements,gebru2021datasheets,artstein2008agreement}.

- **判断依据：** ACL官方元数据与当前条目相符；支持数据声明与文档设计，当前正文未把引用等同于完成全部数据披露。

- **证据层级：** 已核对官方元数据及摘要；不等同于逐页复核全文。

- **实际处理：** 保留数据声明方法引用；未新增“已通过披露认证”等断言。

- **来源：** https://aclanthology.org/Q18-1041/

### R04 — 采纳

- **位置：** file: 1Introduction.tex; line: 4; citation_keys: bhola2020retrieving; context: Online job advertisements describe the knowledge and skills employers seek and provide evidence of changing occupational requirements~\citep{ILO_2020_OJVs_BigData,senger2024survey}. Document-level methods retrieve skills from predefined inventories~\citep{bhola2020retrieving}, whereas span extraction locates the words expressing a requirement~\citep{gnehm2022skills}. Job Skill Named Entity Recognition (JobSkillNER) identifies these mentions and assigns a type to each span. Keeping the source wording makes boundary and type assignments available for inspection.; file: 1Introduction.tex; line: 8; citation_keys: bhola2020retrieving; context: Existing resources provide precedents, but their annotation schemes differ. English SkillSpan permits overlapping SKILL and KNOWLEDGE layers~\citep{zhang2022skillspan}. Kompetencer adds ESCO-derived fine-grained classification to Danish and English spans~\citep{jensen2022kompetencer}. German recruitment work extracts education, experience, and language requirements before finer classification~\citep{gnehm2022skills}. Document-level retrieval and Chinese skill-demand forecasting use other prediction targets~\citep{bhola2020retrieving,chen2024jobsdf}.; file: 5Relatedwork.tex; line: 4; citation_keys: bhola2020retrieving; context: \paragraph{Skill extraction and recruitment datasets.} Recruitment datasets differ first in what a system must predict. \citet{sayfullina2018softskills} ask whether a candidate soft-skill phrase refers to an applicant, whereas \citet{bhola2020retrieving} retrieve skills from a predefined inventory for an entire advertisement. Span extraction locates the words expressing a requirement. Within that task, SkillSpan annotates English SKILL and KNOWLEDGE in two potentially overlapping layers; hard and soft skills describe its coverage rather than its label inventory~\citep{zhang2022skillspan}. Kompetencer combines manually identified skill and knowledge spans with ESCO-derived fine-grained labels in Danish and English, with manual correction of the distantly supervised Danish test labels~\citep{jensen2022kompetencer}. \citet{gnehm2022skills} extract coarse EDU/EXP/LNG spans before refining skill areas for taxonomy matching.

- **判断依据：** ACL摘要明确为文档级预定义技能极端多标签检索，且恢复未显式写出的相关技能。引言require both ... words强于所引研究支持；相关工作目前的文档级表述正确。

- **证据层级：** 已核对官方摘要、元数据及当前稿件引用上下文。

- **实际处理：** 已重写引言首段：将该文限定为从预定义清单检索文档级技能，与本稿定位原文跨度的目标区分；删除原先缺少直接依据的 job–curriculum matching 必要性断言。

- **来源：** https://aclanthology.org/2020.coling-main.513/

### R05 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 6; citation_keys: cao2021occupational; context: Chinese recruitment research includes both forecasting and entity extraction. Job-SDF evaluates skill-demand forecasting at several aggregation levels~\citep{chen2024jobsdf}. For occupational profiling, \citet{cao2021occupational} manually annotated skill and specialty requirements using BIOES and trained a BERT--BiLSTM--CRF model. Chinese-SkillSpan instead uses flat character spans with four types and explicit rules for coordination and contextual interpretation.; file: tex/skillspan_style_related.tex; line: 15; citation_keys: cao2021occupational; context: \citet{cao2021occupational}; Chinese & Recruitment entities & Manually annotated skill / specialty entities; BIOES & Article and supporting data; full NER corpus access not established here \\

- **判断依据：** PLOS正文核实四位作者、e0253308及BIOES人工标注和BERT--BiLSTM--CRF。中文招聘先行工作直接相关。原文数据可得性声称材料在论文/补充文件，但不据此推断完整NER原文语料可获得。

- **证据层级：** 已核对出版方全文，包括数据标注方法小节。

- **实际处理：** 保留中文招聘 BIOES 与 BERT–BiLSTM–CRF 的先行研究及审慎的数据可得性描述。

- **尚需核实：** 本轮未证实该先行研究完整 NER 原文语料的独立下载可得性；不能由论文数据声明推断全部原始标注数据已公开。

- **来源：** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0253308

### R06 — 已解决

- **位置：** file: 1Introduction.tex; line: 6; citation_keys: chen2021boundary; context: For Chinese advertisements, even a short phrase can require several annotation decisions. A technology name can denote tool use in one clause and knowledge of principles in another. Coordination may express separate activities or share an action that must remain attached to its objects. Chinese text normally lacks spaces between words, so tokenization alone cannot resolve these semantic boundaries~\citep{peng2015weibo,chen2021boundary}. Similar ambiguities occur in other languages~\citep{nguyen2024rethinking}, but translating their datasets does not determine which Chinese substrings to select. The task calls for explicit, context-sensitive rules; Figure~\ref{fig:illustrative-annotations} pairs Chinese examples with English explanations.; file: 5Relatedwork.tex; line: 12; citation_keys: chen2021boundary; context: \paragraph{Chinese span annotation and competency guidelines.} Chinese NER resources cover social-media text~\citep{peng2015weibo} and fine-grained entity categories~\citep{cluener2020}. Multilingual studies examine recognition in noisy text~\citep{multiconer2023} and changes in contextual entity types~\citep{dynamicner2025}. These tasks provide useful background, but do not specify how recruitment requirements should be divided into LSKT spans. Chinese boundary detection is complicated by the absence of explicit word delimiters~\citep{chen2021boundary}; recruitment annotation additionally distinguishes knowledge, occupational actions, and transversal competences within each clause.

- **判断依据：** ACL作者、题名和20--25页相符。中文无显式词界与边界建模支持背景；不替代LSKT语义规则的项目依据。

- **证据层级：** 已核对官方元数据及摘要；不等同于逐页复核全文。

- **实际处理：** 保留中文词界与跨度边界的背景引用；未用它替代 LSKT 语义类别规则。

- **来源：** https://aclanthology.org/2021.acl-short.4/

### R07 — 已解决

- **位置：** file: 1Introduction.tex; line: 8; citation_keys: chen2024jobsdf; context: Existing resources provide precedents, but their annotation schemes differ. English SkillSpan permits overlapping SKILL and KNOWLEDGE layers~\citep{zhang2022skillspan}. Kompetencer adds ESCO-derived fine-grained classification to Danish and English spans~\citep{jensen2022kompetencer}. German recruitment work extracts education, experience, and language requirements before finer classification~\citep{gnehm2022skills}. Document-level retrieval and Chinese skill-demand forecasting use other prediction targets~\citep{bhola2020retrieving,chen2024jobsdf}.; file: 5Relatedwork.tex; line: 6; citation_keys: chen2024jobsdf; context: Chinese recruitment research includes both forecasting and entity extraction. Job-SDF evaluates skill-demand forecasting at several aggregation levels~\citep{chen2024jobsdf}. For occupational profiling, \citet{cao2021occupational} manually annotated skill and specialty requirements using BIOES and trained a BERT--BiLSTM--CRF model. Chinese-SkillSpan instead uses flat character spans with four types and explicit rules for coordination and contextual interpretation.

- **判断依据：** 当前BibTeX已含NeurIPS官方URL、卷37与官方页显示的DOI；旧报告建议补官方页面已经解决。摘要确认任务为多个聚合层级的技能需求预测。

- **证据层级：** 已核对 NeurIPS 官方出版页面及作者、题名、卷号与 DOI。

- **实际处理：** 保留已有 NeurIPS 正式页面、卷号和 DOI；当前已具备旧报告要求的正式出处。

- **来源：** https://proceedings.neurips.cc/paper_files/paper/2024/file/e997325c6f4045aa646c81e674076297-Paper-Datasets_and_Benchmarks_Track.pdf; https://proceedings.neurips.cc/paper_files/paper/2024/hash/e997325c6f4045aa646c81e674076297-Abstract-Datasets_and_Benchmarks_Track.html

### R08 — 已解决

- **位置：** file: tex/external_benchmarks/paper_methods.tex; line: 4; citation_keys: conneau2020xlmr; context: To test whether domain-pretrained initialization helps consistently across recruitment tasks, the experiments compare XLM-R-large~\citep{conneau2020xlmr} and ESCOXLM-R~\citep{zhang2023escoxlmr}. They use six public datasets: SkillSpan~\citep{zhang2022skillspan}, Kompetencer~\citep{jensen2022kompetencer}, German ICT~\citep{gnehm2022transfer}, Green~\citep{green2022benchmark}, Sayfullina~\citep{sayfullina2018softskills}, and FIJO~\citep{beauchemin2022fijo}. Separate skill and knowledge streams in SkillSpan and Kompetencer give eight extraction tasks, each retaining its original entity types.

- **判断依据：** ACL核实10位作者、题名、8440--8451及DOI；实际XLM-R模型来源引用适当。Grave名字可选规范为带重音Édouard，但不构成身份错配。

- **证据层级：** 已核对官方元数据。

- **实际处理：** 保留 XLM-R 原始模型文献及正确元数据；本轮未实施作者名重音的可选排印调整。

- **来源：** https://aclanthology.org/2020.acl-main.747/

### R09 — 部分采纳

- **位置：** file: 1Introduction.tex; line: 10; citation_keys: council2017eqf; context: We introduce Chinese-SkillSpan to study these decisions. It combines a corpus of 22,840 sentences from four recruitment collections with a handbook for language (L), knowledge (K), occupational skills (S), and transversal competences (T). In Chinese-SkillSpan, we use \emph{competency spans} for contiguous source-text mentions across all four categories and \emph{occupational skills} specifically for S. The scheme follows ESCO's high-level categories and the knowledge--skill distinction in the European Qualifications Framework~\citep{ESCOv1_2_2024,council2017eqf}, without assigning ESCO concept identifiers. Character offsets preserve the wording of each mention.; file: 2Framework.tex; line: 21; citation_keys: council2017eqf; context: The handbook assigns L to language requirements, including language names, proficiency levels, examinations, and certificates. K covers facts, principles, theories, and fields of study. S covers occupational actions, methods, and tool use. T covers transversal capabilities such as communication, cooperation, cognition, and self-management. These categories draw on ESCO and the knowledge--skill distinction in the European Qualifications Framework~\citep{ESCOv1_2_2024,council2017eqf}.; file: tex/appendix_A_guide_R19.tex; line: 23; citation_keys: council2017eqf; context: \noindent\textit{Source key.} E: ESCO's \href{https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar}{skills hierarchy} and \href{https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/transversal-knowledge-skills-and-competences}{transversal concepts} \citep{ESCOv1_2_2024}; Q: EQF definitions \citep{council2017eqf}; Z: related annotation guidance in SkillSpan, Appendix B \citep{zhang2022skillspan}; I: unitization and categorization in agreement analysis \citep{artstein2008agreement}; P: our V4.2.14 operational decision. Combined marks indicate adaptation, not a verbatim source rule. Chinese examples and their exact boundaries are project illustrations.

- **判断依据：** EUR-Lex原文确认2017/C189/03、15--28页及2017年知识/技能定义。当前简化题名可识别文献；附录已明确学历及非语言资格映射K是项目约定，不是EQF直接规则。

- **证据层级：** 已核对 EUR-Lex 官方原文、附件定义与书目记录。

- **实际处理：** 保留现有可识别的官方题名与定义引用；附录继续区分 EQF 定义与学历/非语言资格映射到 K 的项目约定，未加长书目题名。

- **来源：** https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=oj%3AJOC_2017_189_R_0003

### R10 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 14; citation_keys: desanto2026skilllens; context: ESCO provides a multilingual vocabulary for labor-market information~\citep{levrang2014esco,ESCOv1_2_2024}. SkiLLens combines human involvement, skill extraction, and ESCO linking across European job advertisements~\citep{desanto2026skilllens}. Chinese-SkillSpan adapts ESCO's high-level categories to LSKT annotation in Chinese. The handbook specifies when tool use denotes S rather than K, when coordinated objects must retain a shared action, and when an experience qualifier belongs inside the span. Agreement analysis and adjudication consequently address both unitization and categorization~\citep{artstein2008agreement}.

- **判断依据：** ACL正式2026年EACL Industry条目确认五位作者、877--885及ESCO链接任务；年份较新不是错误证据。当前相关工作已与本文四类跨度标注区别。

- **证据层级：** 已核对官方元数据及摘要；不等同于逐页复核全文。

- **实际处理：** 保留已核实的 2026 年正式文献，保持 ESCO 概念链接与本文高层类型标注的区别。

- **来源：** https://aclanthology.org/2026.eacl-industry.65/

### R11 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 18; citation_keys: devlin2019bert; context: Encoder models offer one way to learn from these labels. Pretrained encoders and structured decoding~\citep{devlin2019bert,lafferty2001crf} can be combined with continued pretraining on recruitment text~\citep{gururangan2020dapt,zhang2022skillspan}. SkillSpan introduced the domain-adapted JobBERT and JobSpanBERT baselines~\citep{zhang2022skillspan}. ESCOXLM-R uses taxonomy-driven multilingual pretraining~\citep{zhang2023escoxlmr}, and NNOSE retrieves training-data representations to support extraction, including infrequent patterns~\citep{zhang2024nnose}. Reproducing these methods on their original tasks and adapting them to Chinese LSKT extraction require separate protocols because the languages, annotation layers, and splits differ.; file: tex/external_benchmarks/paper_appendix.tex; line: 5; citation_keys: devlin2019bert; context: We reran BERT~\citep{devlin2019bert}, SpanBERT~\citep{joshi2020spanbert}, JobBERT, and JobSpanBERT~\citep{zhang2022skillspan} separately for skills and knowledge on SkillSpan's public HOUSE and TECH subsets. The MaChAmp~\citep{vandergoot2021machamp} \texttt{seq\_bio} CRF runs used 20 epochs, development-set checkpoint selection, and five seeds listed in the \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/source/tex/external_benchmarks/paper_appendix.tex}{experiment records}. BIG was unavailable; multi-task training was not rerun. Table~\ref{tab:external-native} gives MaChAmp per-site span-F1. The \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/README.md#skillspan-pooled-scores-previous-table-25}{archived pooled scores} report BIO rescoring of the same predictions with the correct task column. These scoring procedures yield different results. The native runs contain 3,570 test sentences, compared with 3,569 in the common-protocol release; the one-record difference has not been resolved by matching IDs. For published test references, we use only the original paper's TEST/STL rows. Its HOUSE/TECH rows report development results.

- **判断依据：** ACL元数据核实作者、NAACL2019、4171--4186、DOI。作为编码器及SkillSpan复跑模型依据合适。

- **证据层级：** 已核对官方元数据。

- **实际处理：** 保留 BERT 正式原始文献及编码器用途。

- **来源：** https://aclanthology.org/N19-1423/

### R12 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 16; citation_keys: ding2023annotator; context: \paragraph{Model-assisted annotation and extraction models.} LLMs can supply first-pass labels, with their usefulness depending on task instructions and human validation~\citep{ding2023annotator,li2023coannotating,ulhaq2026nerannotation}. GoLLIE and subsequent guideline-refinement work study how annotation instructions shape model outputs~\citep{gollie2024,kim2026guidelines}. In recruitment, JobSkape generates synthetic advertisements for skill-to-taxonomy matching~\citep{magron2024jobskape}. Chinese-SkillSpan retains collected recruitment texts and adds model-generated annotations with documented review. The annotation prompts follow the handbook used at each stage.

- **判断依据：** ACL元数据核实七位作者与11173--11195。当前句子说明模型首轮标注与任务/人工验证的依赖，无本文模型准确率保证。

- **证据层级：** 已核对官方元数据及摘要；不等同于逐页复核全文。

- **实际处理：** 保留模型首轮标注的方法背景；未把其他任务性能作为本项目标签准确率证明。

- **来源：** https://aclanthology.org/2023.acl-long.626/

### R13 — 部分采纳

- **位置：** file: 1Introduction.tex; line: 10; citation_keys: ESCOv1_2_2024; context: We introduce Chinese-SkillSpan to study these decisions. It combines a corpus of 22,840 sentences from four recruitment collections with a handbook for language (L), knowledge (K), occupational skills (S), and transversal competences (T). In Chinese-SkillSpan, we use \emph{competency spans} for contiguous source-text mentions across all four categories and \emph{occupational skills} specifically for S. The scheme follows ESCO's high-level categories and the knowledge--skill distinction in the European Qualifications Framework~\citep{ESCOv1_2_2024,council2017eqf}, without assigning ESCO concept identifiers. Character offsets preserve the wording of each mention.; file: 5Relatedwork.tex; line: 14; citation_keys: ESCOv1_2_2024; context: ESCO provides a multilingual vocabulary for labor-market information~\citep{levrang2014esco,ESCOv1_2_2024}. SkiLLens combines human involvement, skill extraction, and ESCO linking across European job advertisements~\citep{desanto2026skilllens}. Chinese-SkillSpan adapts ESCO's high-level categories to LSKT annotation in Chinese. The handbook specifies when tool use denotes S rather than K, when coordinated objects must retain a shared action, and when an experience qualifier belongs inside the span. Agreement analysis and adjudication consequently address both unitization and categorization~\citep{artstein2008agreement}.; file: 2Framework.tex; line: 21; citation_keys: ESCOv1_2_2024; context: The handbook assigns L to language requirements, including language names, proficiency levels, examinations, and certificates. K covers facts, principles, theories, and fields of study. S covers occupational actions, methods, and tool use. T covers transversal capabilities such as communication, cooperation, cognition, and self-management. These categories draw on ESCO and the knowledge--skill distinction in the European Qualifications Framework~\citep{ESCOv1_2_2024,council2017eqf}.; file: tex/appendix_A_guide_R19.tex; line: 23; citation_keys: ESCOv1_2_2024; context: \noindent\textit{Source key.} E: ESCO's \href{https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar}{skills hierarchy} and \href{https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/transversal-knowledge-skills-and-competences}{transversal concepts} \citep{ESCOv1_2_2024}; Q: EQF definitions \citep{council2017eqf}; Z: related annotation guidance in SkillSpan, Appendix B \citep{zhang2022skillspan}; I: unitization and categorization in agreement analysis \citep{artstein2008agreement}; P: our V4.2.14 operational decision. Combined marks indicate adaptation, not a verbatim source rule. Chinese examples and their exact boundaries are project illustrations.

- **判断依据：** 官方当前技能页显示v1.2.1并列四个高层类；另有官方v1.2专页及2024-05-13发布公告确认v1.2.0在2024年存在。动态页更新不能推翻作者研究时版本声明。论文是高层类别借鉴，并非版本级concept ID映射；下载包哈希不是此背景引用成立的前提。研究实际采用的快照仍未在本次24项书目审查中核实。

- **证据层级：** 已核对官方现行技能层级和 v1.2 发布文件；未核实本项目实际使用的历史快照。

- **实际处理：** 保留 ESCO-informed 表述及作者声明的 v1.2.0；现书目仍链接动态技能页面，未把使用版本改为当前 v1.2.1。

- **尚需核实：** 研究实际使用的 ESCO v1.2.0 快照未在本轮书目审查中核实；可在仓库补官方 v1.2 专页作为稳定版本入口，但不得改称使用现行 v1.2.1。

- **来源：** https://esco.ec.europa.eu/en/classification/skill_main; https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-v12; https://esco.ec.europa.eu/en/news/esco-v12-live; https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-versions

### R14 — 采纳

- **位置：** file: 5Relatedwork.tex; line: 12; citation_keys: multiconer2023; context: \paragraph{Chinese span annotation and competency guidelines.} Chinese NER resources cover social-media text~\citep{peng2015weibo} and fine-grained entity categories~\citep{cluener2020}. Multilingual studies examine recognition in noisy text~\citep{multiconer2023} and changes in contextual entity types~\citep{dynamicner2025}. These tasks provide useful background, but do not specify how recruitment requirements should be divided into LSKT spans. Chinese boundary detection is complicated by the absence of explicit word delimiters~\citep{chen2021boundary}; recruitment annotation additionally distinguishes knowledge, occupational actions, and transversal competences within each clause.

- **判断依据：** ACL正式题名为Fine-grained Multilingual Named Entity Recognition (MultiCoNER 2)，当前MultiCoNER II Multilingual Complex...不一致。作者、2247--2265和DOI一致。背景用途合理。

- **证据层级：** 已核对官方完整书目导出与摘要。

- **实际处理：** 已按 ACL 官方记录更正 MultiCoNER 2 的完整题名及 SemEval-2023 会议名；作者、页码、DOI 保留。

- **来源：** https://aclanthology.org/2023.semeval-1.310/

### R15 — 已解决

- **位置：** file: 1Introduction.tex; line: 14; citation_keys: gebru2021datasheets; context: The original corpus and its smaller training, reference, and agreement subsets have distinct roles. The 150-sentence human reference contributed to guideline development, so model comparisons on it are diagnostic. External recruitment experiments provide additional task-specific comparisons. We document the role and availability of each subset following guidance on dataset documentation and annotation agreement~\citep{bender2018datastatements,gebru2021datasheets,artstein2008agreement}.

- **判断依据：** 作者所在Microsoft Research出版页确认七位作者、CACM64(12):86--92、2021。当前用于数据文档依据合理。

- **证据层级：** 已核对作者所属机构提供的出版元数据及摘要。

- **实际处理：** 保留数据说明文档的方法来源；未把该引用视为项目审计通过的证据。

- **来源：** https://www.microsoft.com/en-us/research/publication/datasheets-for-datasets/

### R16 — 采纳

- **位置：** file: 1Introduction.tex; line: 4; citation_keys: gnehm2022skills; context: Online job advertisements describe the knowledge and skills employers seek and provide evidence of changing occupational requirements~\citep{ILO_2020_OJVs_BigData,senger2024survey}. Document-level methods retrieve skills from predefined inventories~\citep{bhola2020retrieving}, whereas span extraction locates the words expressing a requirement~\citep{gnehm2022skills}. Job Skill Named Entity Recognition (JobSkillNER) identifies these mentions and assigns a type to each span. Keeping the source wording makes boundary and type assignments available for inspection.; file: 1Introduction.tex; line: 8; citation_keys: gnehm2022skills; context: Existing resources provide precedents, but their annotation schemes differ. English SkillSpan permits overlapping SKILL and KNOWLEDGE layers~\citep{zhang2022skillspan}. Kompetencer adds ESCO-derived fine-grained classification to Danish and English spans~\citep{jensen2022kompetencer}. German recruitment work extracts education, experience, and language requirements before finer classification~\citep{gnehm2022skills}. Document-level retrieval and Chinese skill-demand forecasting use other prediction targets~\citep{bhola2020retrieving,chen2024jobsdf}.; file: 5Relatedwork.tex; line: 4; citation_keys: gnehm2022skills; context: \paragraph{Skill extraction and recruitment datasets.} Recruitment datasets differ first in what a system must predict. \citet{sayfullina2018softskills} ask whether a candidate soft-skill phrase refers to an applicant, whereas \citet{bhola2020retrieving} retrieve skills from a predefined inventory for an entire advertisement. Span extraction locates the words expressing a requirement. Within that task, SkillSpan annotates English SKILL and KNOWLEDGE in two potentially overlapping layers; hard and soft skills describe its coverage rather than its label inventory~\citep{zhang2022skillspan}. Kompetencer combines manually identified skill and knowledge spans with ESCO-derived fine-grained labels in Danish and English, with manual correction of the distantly supervised Danish test labels~\citep{jensen2022kompetencer}. \citet{gnehm2022skills} extract coarse EDU/EXP/LNG spans before refining skill areas for taxonomy matching.; file: tex/skillspan_style_related.tex; line: 12; citation_keys: gnehm2022skills; context: \citet{gnehm2022skills}; German & Spans, then finer areas & Coarse EDU/EXP/LNG; finer skill areas and taxonomy matching & Article and model; full annotated corpus access not established here \\; file: tex/external_benchmarks/paper_methods.tex; line: 4; citation_keys: gnehm2022transfer; context: To test whether domain-pretrained initialization helps consistently across recruitment tasks, the experiments compare XLM-R-large~\citep{conneau2020xlmr} and ESCOXLM-R~\citep{zhang2023escoxlmr}. They use six public datasets: SkillSpan~\citep{zhang2022skillspan}, Kompetencer~\citep{jensen2022kompetencer}, German ICT~\citep{gnehm2022transfer}, Green~\citep{green2022benchmark}, Sayfullina~\citep{sayfullina2018softskills}, and FIJO~\citep{beauchemin2022fijo}. Separate skill and knowledge streams in SkillSpan and Kompetencer give eight extraction tasks, each retaining its original entity types.; file: tex/external_benchmarks/paper_methods.tex; line: 12; citation_keys: gnehm2022skills; gnehm2022transfer; context: \hyperref[app:e]{Appendix E} gives separate protocols for five-seed MaChAmp-CRF reruns on SkillSpan and German ICT, five-seed Kompetencer classification, and single-seed NNOSE retrieval. These preserve their task-specific scoring: Danish BIO extraction differs from fine-grained classification of supplied spans, and the public German ICT task~\citep{gnehm2022transfer} is distinct from the EDU/EXP/LNG extraction and taxonomy-classification pipeline~\citep{gnehm2022skills}. The datasets' languages and annotation schemes also differ, so their absolute scores do not measure relative extraction difficulty across languages.; file: tex/external_benchmarks/paper_appendix.tex; line: 7; citation_keys: gnehm2022skills; gnehm2022transfer; context: For the German public ICT task~\citep{gnehm2022transfer}, jobBERT-de used a 20-epoch MaChAmp configuration and ESCOXLM-R used its released five-epoch configuration~\citep{zhang2023escoxlmr}. Both used five recorded seeds. Compatibility fields were added for newer MaChAmp without changing the learning rate or epoch limit; the exact changes are archived. The runs therefore use the public releases with compatibility changes, rather than recreating every original environment. They contain 2,557 test sentences, whereas the ESCOXLM-R paper reports 2,943. The ICT extraction task differs from the EDU/EXP/LNG extraction and taxonomy-classification pipeline described by \citet{gnehm2022skills}.

- **判断依据：** 两篇确为不同文章：四作者NLP+CSS2022论文14--24页研究EDU/EXP/LNG及细分类；三作者LREC2022论文3892--3901页提供ICT抽取与领域模型。ESCOXLM-R原文GNEHM段及其参考文献明确指向三作者LREC文。当前paper_methods把German ICT引到四作者文，需拆分；原相关工作四作者引用应保留。

- **证据层级：** 已核对两篇官方文献的元数据、全文任务小节，以及 ESCOXLM-R 原文的 GNEHM 描述和参考文献。

- **实际处理：** 已新增三作者 LREC 2022 文献 gnehm2022transfer，并将 German ICT 数据/方法引用改到该文；四作者 NLP+CSS 文献 gnehm2022skills 保留用于 EDU/EXP/LNG 及 taxonomy matching。正文和附录明确两者是不同任务，删除“仅为同一流水线子集”的说法。

- **来源：** https://aclanthology.org/2022.nlpcss-1.2/; https://aclanthology.org/2022.lrec-1.414/; https://aclanthology.org/2022.lrec-1.414.pdf; https://aclanthology.org/2022.nlpcss-1.2.pdf; https://aclanthology.org/2023.acl-long.662.pdf

### R17 — 已解决

- **位置：** file: tex/external_benchmarks/paper_methods.tex; line: 4; citation_keys: green2022benchmark; context: To test whether domain-pretrained initialization helps consistently across recruitment tasks, the experiments compare XLM-R-large~\citep{conneau2020xlmr} and ESCOXLM-R~\citep{zhang2023escoxlmr}. They use six public datasets: SkillSpan~\citep{zhang2022skillspan}, Kompetencer~\citep{jensen2022kompetencer}, German ICT~\citep{gnehm2022transfer}, Green~\citep{green2022benchmark}, Sayfullina~\citep{sayfullina2018softskills}, and FIJO~\citep{beauchemin2022fijo}. Separate skill and knowledge streams in SkillSpan and Kompetencer give eight extraction tasks, each retaining its original entity types.

- **判断依据：** ACL正式页确认3位作者、1201--1208及五类实体；与本研究保留native types方案相容。

- **证据层级：** 已核对官方元数据及摘要；不等同于逐页复核全文。

- **实际处理：** 保留 Green 数据集正式出处以及保留原生类型的实验描述。

- **尚需核实：** 本文所用派生数据包的具体转换、版本和许可须依其发布记录另行核对；论文真实性不等于包级复核。

- **来源：** https://aclanthology.org/2022.lrec-1.128/

### R18 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 18; citation_keys: gururangan2020dapt; context: Encoder models offer one way to learn from these labels. Pretrained encoders and structured decoding~\citep{devlin2019bert,lafferty2001crf} can be combined with continued pretraining on recruitment text~\citep{gururangan2020dapt,zhang2022skillspan}. SkillSpan introduced the domain-adapted JobBERT and JobSpanBERT baselines~\citep{zhang2022skillspan}. ESCOXLM-R uses taxonomy-driven multilingual pretraining~\citep{zhang2023escoxlmr}, and NNOSE retrieves training-data representations to support extraction, including infrequent patterns~\citep{zhang2024nnose}. Reproducing these methods on their original tasks and adapting them to Chinese LSKT extraction require separate protocols because the languages, annotation layers, and splits differ.

- **判断依据：** ACL正式元数据和领域/任务继续预训练主题相符。当前引用用作训练方法背景，不保证JobBERT或ESCO初始化必然改善。

- **证据层级：** 已核对官方元数据及摘要；不等同于逐页复核全文。

- **实际处理：** 保留继续预训练的方法背景，不据此承诺 JobBERT 或 ESCO 初始化一定提高性能。

- **来源：** https://aclanthology.org/2020.acl-main.740/

### R19 — 已解决

- **位置：** file: tex/annotation_quality_R12.tex; line: 9; citation_keys: hripcsak2005agreement; context: We computed agreement from the preserved pre-discussion exports, retaining all 50 sentences and all three coder pairs. Typed exact F1 measures agreement on complete spans without designating a coder as gold~\citep{hripcsak2005agreement}; boundary-only F1 ignores type. Nominal Krippendorff's $\alpha$ uses L/K/S/T/O assignments to all 2,111 source code points. Percentile 95\% intervals use 10,000 source-stratified sentence-bootstrap samples, retaining all three annotations together. These intervals condition on the observed source mixture and coders.

- **判断依据：** OUP官方期刊页/期目录与PubMed作者条目确认两名作者、12(3):296--298、DOI。摘要直接讨论专家两两F度量与一致性，跨医学领域但方法高度相关。Crossref接口只给第一作者，不能据此删除Rothschild。

- **证据层级：** 已交叉核对出版方卷期/文章元数据、PubMed 作者记录及摘要；Crossref 的作者字段不完整，未据此删作者。

- **实际处理：** 保留两名作者和两两 F 度量的方法引用；没有用不完整 Crossref 元数据覆盖出版方/PubMed 记录。

- **来源：** https://pubmed.ncbi.nlm.nih.gov/15684123/; https://academic.oup.com/jamia/issue/12/3; https://academic.oup.com/jamia/article-abstract/12/3/296/812057?login=false; https://api.crossref.org/works/10.1197/jamia.M1733

### R20 — 已解决

- **位置：** file: tex/external_benchmarks/paper_appendix.tex; line: 5; citation_keys: joshi2020spanbert; context: We reran BERT~\citep{devlin2019bert}, SpanBERT~\citep{joshi2020spanbert}, JobBERT, and JobSpanBERT~\citep{zhang2022skillspan} separately for skills and knowledge on SkillSpan's public HOUSE and TECH subsets. The MaChAmp~\citep{vandergoot2021machamp} \texttt{seq\_bio} CRF runs used 20 epochs, development-set checkpoint selection, and five seeds listed in the \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/source/tex/external_benchmarks/paper_appendix.tex}{experiment records}. BIG was unavailable; multi-task training was not rerun. Table~\ref{tab:external-native} gives MaChAmp per-site span-F1. The \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/README.md#skillspan-pooled-scores-previous-table-25}{archived pooled scores} report BIO rescoring of the same predictions with the correct task column. These scoring procedures yield different results. The native runs contain 3,570 test sentences, compared with 3,569 in the common-protocol release; the one-record difference has not been resolved by matching IDs. For published test references, we use only the original paper's TEST/STL rows. Its HOUSE/TECH rows report development results.

- **判断依据：** ACL TACL正式条目确认6位作者、卷8:64--77、DOI。附录确实用于SpanBERT复跑引用，不是无用未引用条目。

- **证据层级：** 已核对官方元数据及当前附录 E 的实际引用用途。

- **实际处理：** 保留 SpanBERT 原始文献及附录复跑用途；没有据此补造原 SkillSpan 未报告的 SpanBERT TEST 数值。

- **来源：** https://aclanthology.org/2020.tacl-1.5/

### R21 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 16; citation_keys: kim2026guidelines; context: \paragraph{Model-assisted annotation and extraction models.} LLMs can supply first-pass labels, with their usefulness depending on task instructions and human validation~\citep{ding2023annotator,li2023coannotating,ulhaq2026nerannotation}. GoLLIE and subsequent guideline-refinement work study how annotation instructions shape model outputs~\citep{gollie2024,kim2026guidelines}. In recruitment, JobSkape generates synthetic advertisements for skill-to-taxonomy matching~\citep{magron2024jobskape}. Chinese-SkillSpan retains collected recruitment texts and adds model-generated annotations with documented review. The annotation prompts follow the handbook used at each stage.

- **判断依据：** ACL2026正式条目确认3位作者与37951--37964；高页码和新年份并非错误。当前用作指南改进如何影响LLM输出的方法类比。

- **证据层级：** 已核对官方元数据及摘要；不等同于逐页复核全文。

- **实际处理：** 保留已核实的 2026 年指南改进文献；不把其生物医学结果当作中文招聘标注可靠性证明。

- **来源：** https://aclanthology.org/2026.acl-long.1760/

### R22 — 已解决

- **位置：** file: tex/annotation_quality_R12.tex; line: 7; citation_keys: klie2024annotationquality; context: Three annotators used handbook B.sop\_v4.2.14 after familiarization and training on sets of five and 15 sentences, following the training-and-feedback approach discussed by \citet{klie2024annotationquality}. They then independently coded the same random sample of 50 Silver teacher-pool sentences in separate Doccano projects, blinded to both machine suggestions and one another's labels. Training sentences are excluded from formal agreement. The sample contains one sentence from each of 50 recorded advertisement identifiers; it assesses annotation agreement and is not a new model test set. Source counts and sampling-record limits appear in \hyperref[app:b]{Appendix B}.

- **判断依据：** ACL/CL正式元数据确认50(3):817--866与三位作者。当前仅称following training-and-feedback approach，未把5+15样本量说成来源要求。

- **证据层级：** 已核对官方元数据及当前稿件的方法引用上下文。

- **实际处理：** 保留培训与反馈的方法依据；5+15 句仍是本项目实际培训安排，并非文献规定的样本量。

- **来源：** https://aclanthology.org/2024.cl-3.1/

### R23 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 18; citation_keys: lafferty2001crf; context: Encoder models offer one way to learn from these labels. Pretrained encoders and structured decoding~\citep{devlin2019bert,lafferty2001crf} can be combined with continued pretraining on recruitment text~\citep{gururangan2020dapt,zhang2022skillspan}. SkillSpan introduced the domain-adapted JobBERT and JobSpanBERT baselines~\citep{zhang2022skillspan}. ESCOXLM-R uses taxonomy-driven multilingual pretraining~\citep{zhang2023escoxlmr}, and NNOSE retrieves training-data representations to support extraction, including infrequent patterns~\citep{zhang2024nnose}. Reproducing these methods on their original tasks and adapting them to Chinese LSKT extraction require separate protocols because the languages, annotation layers, and splits differ.

- **判断依据：** 作者CMU官方出版清单核实三位作者、题名和ICML2001；本次未逐字段核实出版方页码，但282--289无已发现冲突。CRF序列标注引用直接相关。

- **证据层级：** 已核对作者官方出版清单；本轮未独立复核页码。

- **实际处理：** 保留 CRF 原始文献及现有页码；未以猜测地址替换旧链接。

- **尚需核实：** 本轮未独立复核页码 282–289；没有发现冲突，故保留，不写成已逐字段完成核验。

- **来源：** https://www.cs.cmu.edu/afs/cs/usr/lafferty/www/publications.html

### R24 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 14; citation_keys: levrang2014esco; context: ESCO provides a multilingual vocabulary for labor-market information~\citep{levrang2014esco,ESCOv1_2_2024}. SkiLLens combines human involvement, skill extraction, and ESCO linking across European job advertisements~\citep{desanto2026skilllens}. Chinese-SkillSpan adapts ESCO's high-level categories to LSKT annotation in Chinese. The handbook specifies when tool use denotes S rather than K, when coordinated objects must retain a shared action, and when an experience qualifier belongs inside the span. Agreement analysis and adjudication consequently address both unitization and categorization~\citep{artstein2008agreement}.

- **判断依据：** IEEE存入Crossref的元数据核实6位作者、Computer47(10):57--64和DOI；publisher DOI网页工具访问受限，不能据此否定论文。当前用于ESCO互操作性背景适当。

- **证据层级：** 已核对出版方提交的 Crossref 元数据；本轮网页工具未能读取 IEEE 直接页面。

- **实际处理：** 保留 ESCO 互操作性文献及已核实的出版元数据。

- **来源：** https://mastic.ulb.ac.be/wp-content/uploads/2014/10/agis_papantoniou.pdf; https://api.crossref.org/works/10.1109/MC.2014.283; https://doi.org/10.1109/MC.2014.283

### R25 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 16; citation_keys: li2023coannotating; context: \paragraph{Model-assisted annotation and extraction models.} LLMs can supply first-pass labels, with their usefulness depending on task instructions and human validation~\citep{ding2023annotator,li2023coannotating,ulhaq2026nerannotation}. GoLLIE and subsequent guideline-refinement work study how annotation instructions shape model outputs~\citep{gollie2024,kim2026guidelines}. In recruitment, JobSkape generates synthetic advertisements for skill-to-taxonomy matching~\citep{magron2024jobskape}. Chinese-SkillSpan retains collected recruitment texts and adds model-generated annotations with documented review. The annotation prompts follow the handbook used at each stage.

- **判断依据：** 当前相关工作只将其作为人机协作标注依据，没有声称本研究实施其 uncertainty-guided allocation 算法。官方七作者、EMNLP 2023、1487--1505 与稿件相符。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留人机协作标注背景引用；未声称本研究执行了该文的不确定性分配算法。

- **来源：** https://aclanthology.org/2023.emnlp-main.92/

### R26 — 部分采纳

- **位置：** file: 5Relatedwork.tex; line: 20; citation_keys: uie2022; context: Other approaches use text-to-structure generation in UIE~\citep{uie2022}, distilled supervision in UniversalNER~\citep{universalner}, open-type encoder extraction in GLiNER~\citep{gliner-naacl24}, and generative extraction with self-verification in GPT-NER~\citep{gptner2025}. These approaches provide methodological context; they are not additional evaluated baselines. The models tested here, their supervision, and their scoring protocols are specified in \nameref{sec:experiments}.

- **判断依据：** UIE文本到结构归类正确；当前位于相关工作，未作为结果表模型，但最后一句 each comparison 可能使读者误会列举模型均有实测。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 已在相关工作段尾明确 UIE 等是方法背景，并非额外实测基线；实际模型与协议另指向实验章节。

- **来源：** https://aclanthology.org/2022.acl-long.395/

### R27 — 部分采纳

- **位置：** file: 5Relatedwork.tex; line: 12; citation_keys: dynamicner2025; context: \paragraph{Chinese span annotation and competency guidelines.} Chinese NER resources cover social-media text~\citep{peng2015weibo} and fine-grained entity categories~\citep{cluener2020}. Multilingual studies examine recognition in noisy text~\citep{multiconer2023} and changes in contextual entity types~\citep{dynamicner2025}. These tasks provide useful background, but do not specify how recruitment requirements should be divided into LSKT spans. Chinese boundary detection is complicated by the absence of explicit word delimiters~\citep{chen2021boundary}; recruitment annotation additionally distinguishes knowledge, occupational actions, and transversal competences within each clause.

- **判断依据：** 官方记录确认题名、11作者、EMNLP 2025、16511--16535。当前一句同时引 MultiCoNER 和 DynamicNER，来源分工仍可明确。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 已将多语种噪声文本识别对应 MultiCoNER，将上下文类型变化对应 DynamicNER，分别限定两篇文献支持的论点。

- **来源：** https://aclanthology.org/2025.emnlp-main.835/

### R28 — 待核实

- **位置：** file: tex/silver_plus_methods.tex; line: 6; citation_keys: macrodataPlatform; context: Texts came from three routes: commercial collections purchased from MacroData~\citep{macrodataPlatform}; public-institution recruitment announcements collected by the research team; and the Recruitment Dataset (dataset ID 163746) on Alibaba Cloud Tianchi~\citep{tianchiRecruitment163746}. For public-institution announcements, team members selected pages from government portals, university and hospital websites, and public recruitment platforms across regions of China. A crawler revisited the registered URLs weekly or monthly. Screening and cleaning produced the public-institution subset. \hyperref[app:d]{Appendix D} records the available source metadata and gaps in the original collection history.

- **判断依据：** 平台出处不是采购产品、批次、授权证据。当前正文和附录已承认来源记录缺口，本轮不能由主页恢复私有采购台账。官方公司名的英文仍是作者译名。

- **证据层级：** 本轮直接GET官方页面返回200及平台标题，静态正文未含运营公司；原审查的公司核验为线索，产品级批次/许可仍未核实

- **实际处理：** 保留平台出处与现有来源记录缺口说明；未把平台页面存在改写为采购批次或授权已证实。

- **尚需核实：** 具体采购产品、批次、下载日期、文件哈希与授权范围仍需原始台账。; 本轮可确认平台页面存在，静态页面未独立确认运营公司；英文公司名仍是作者译名，不能称已核实官方英文名称。

- **来源：** https://www.macrodatas.cn/about_firm.html

### R29 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 16; citation_keys: magron2024jobskape; context: \paragraph{Model-assisted annotation and extraction models.} LLMs can supply first-pass labels, with their usefulness depending on task instructions and human validation~\citep{ding2023annotator,li2023coannotating,ulhaq2026nerannotation}. GoLLIE and subsequent guideline-refinement work study how annotation instructions shape model outputs~\citep{gollie2024,kim2026guidelines}. In recruitment, JobSkape generates synthetic advertisements for skill-to-taxonomy matching~\citep{magron2024jobskape}. Chinese-SkillSpan retains collected recruitment texts and adds model-generated annotations with documented review. The annotation prompts follow the handbook used at each stage.

- **判断依据：** 官方五作者、2024、43--58相符。当前明确 JobSkape 合成广告、本文收集真实招聘文本并添加模型标签，两者已区分。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留 JobSkape 文献，继续区分合成招聘广告与本稿采集真实招聘文本后添加模型标签的流程。

- **来源：** https://aclanthology.org/2024.nlp4hr-1.4/

### R30 — 已解决

- **位置：** file: 1Introduction.tex; line: 6; citation_keys: nguyen2024rethinking; context: For Chinese advertisements, even a short phrase can require several annotation decisions. A technology name can denote tool use in one clause and knowledge of principles in another. Coordination may express separate activities or share an action that must remain attached to its objects. Chinese text normally lacks spaces between words, so tokenization alone cannot resolve these semantic boundaries~\citep{peng2015weibo,chen2021boundary}. Similar ambiguities occur in other languages~\citep{nguyen2024rethinking}, but translating their datasets does not determine which Chinese substrings to select. The task calls for explicit, context-sensitive rules; Figure~\ref{fig:illustrative-annotations} pairs Chinese examples with English explanations.; file: 5Relatedwork.tex; line: 8; citation_keys: nguyen2024rethinking; context: Taxonomy-based weak supervision can reduce manual annotation work~\citep{zhang2022weak}, but generated labels still need validation. \citet{nguyen2024rethinking} report difficulties with conjoined and ambiguous mentions across six recruitment datasets. \citet{senger2024survey} also identify scarce public annotations and inconsistent terminology. Table~\ref{tab:related-span} compares the prediction units, annotation layers, and available materials of selected resources.

- **判断依据：** 官方四作者、2024、27--42相符；核心相关工作涉及技能抽取、多数据集及复杂跨度。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留技能抽取、多数据集及复杂跨度问题的直接相关工作。

- **来源：** https://aclanthology.org/2024.nlp4hr-1.3/

### R31 — 部分采纳

- **位置：** file: 1Introduction.tex; line: 6; citation_keys: peng2015weibo; context: For Chinese advertisements, even a short phrase can require several annotation decisions. A technology name can denote tool use in one clause and knowledge of principles in another. Coordination may express separate activities or share an action that must remain attached to its objects. Chinese text normally lacks spaces between words, so tokenization alone cannot resolve these semantic boundaries~\citep{peng2015weibo,chen2021boundary}. Similar ambiguities occur in other languages~\citep{nguyen2024rethinking}, but translating their datasets does not determine which Chinese substrings to select. The task calls for explicit, context-sensitive rules; Figure~\ref{fig:illustrative-annotations} pairs Chinese examples with English explanations.; file: 5Relatedwork.tex; line: 12; citation_keys: peng2015weibo; context: \paragraph{Chinese span annotation and competency guidelines.} Chinese NER resources cover social-media text~\citep{peng2015weibo} and fine-grained entity categories~\citep{cluener2020}. Multilingual studies examine recognition in noisy text~\citep{multiconer2023} and changes in contextual entity types~\citep{dynamicner2025}. These tasks provide useful background, but do not specify how recruitment requirements should be divided into LSKT spans. Chinese boundary detection is complicated by the absence of explicit word delimiters~\citep{chen2021boundary}; recruitment annotation additionally distinguishes knowledge, occupational actions, and transversal competences within each clause.

- **判断依据：** 中文微博NER研究是真实背景；现书目缺DOI/URL但其他关键字段无冲突。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留真实的中文社交媒体 NER 背景，并在相关工作按该范围引用；当前书目仍未添加可选 DOI/URL 字段。

- **尚需核实：** 可选格式完善未实施：补 DOI 10.18653/v1/D15-1064 与官方 ACL URL；不影响当前文献识别。

- **来源：** https://aclanthology.org/D15-1064/

### R32 — 部分采纳

- **位置：** file: 1Introduction.tex; line: 4; citation_keys: ILO_2020_OJVs_BigData; context: Online job advertisements describe the knowledge and skills employers seek and provide evidence of changing occupational requirements~\citep{ILO_2020_OJVs_BigData,senger2024survey}. Document-level methods retrieve skills from predefined inventories~\citep{bhola2020retrieving}, whereas span extraction locates the words expressing a requirement~\citep{gnehm2022skills}. Job Skill Named Entity Recognition (JobSkillNER) identifies these mentions and assigns a type to each span. Keeping the source wording makes boundary and type assignments available for inspection.

- **判断依据：** ILO机构库直接列 Ana Podjanin 与 Olga Strietska-Ilina、2020、Geneva、ISBN9789220328545；当前仅缩写作者、techreport，未构成错误。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留原 ILO 机构出版物的年份、机构、题名和链接；本轮未实施改为书籍类型、全名和 ISBN 的可选格式规范。

- **尚需核实：** 可选格式完善未实施：作者全名、机构书籍类型、ISBN 9789220328545 与稳定机构库入口。

- **来源：** https://researchrepository.ilo.org/esploro/outputs/book/The-feasibility-of-using-big-data/995218969402676?institution=41ILO_INST

### R33 — 不采纳

- **位置：** file: 5Relatedwork.tex; line: 16; citation_keys: gollie2024; context: \paragraph{Model-assisted annotation and extraction models.} LLMs can supply first-pass labels, with their usefulness depending on task instructions and human validation~\citep{ding2023annotator,li2023coannotating,ulhaq2026nerannotation}. GoLLIE and subsequent guideline-refinement work study how annotation instructions shape model outputs~\citep{gollie2024,kim2026guidelines}. In recruitment, JobSkape generates synthetic advertisements for skill-to-taxonomy matching~\citep{magron2024jobskape}. Chinese-SkillSpan retains collected recruitment texts and adds model-generated annotations with documented review. The annotation prompts follow the handbook used at each stage.

- **判断依据：** ICLR官方网站BibTeX已成功取得，明确列 volume=2024、pages=47083--47107。原审查的卷页未核实状态在本次被解除，不应删除真实字段。正式PDF第一页明确署名 Oier Lopez de Lacalle，与现稿一致；官网BibTeX缩写成Lacalle不应覆盖正式论文署名。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 未采纳删除卷号和页码的建议：当前书目保留 volume=2024 与 pages=47083–47107，符合 ICLR 官方 BibTeX；作者署名亦保留正式论文写法。

- **来源：** https://proceedings.iclr.cc/paper_files/paper/4265-/bibtex

### R34 — 部分采纳

- **位置：** file: 5Relatedwork.tex; line: 4; citation_keys: sayfullina2018softskills; context: \paragraph{Skill extraction and recruitment datasets.} Recruitment datasets differ first in what a system must predict. \citet{sayfullina2018softskills} ask whether a candidate soft-skill phrase refers to an applicant, whereas \citet{bhola2020retrieving} retrieve skills from a predefined inventory for an entire advertisement. Span extraction locates the words expressing a requirement. Within that task, SkillSpan annotates English SKILL and KNOWLEDGE in two potentially overlapping layers; hard and soft skills describe its coverage rather than its label inventory~\citep{zhang2022skillspan}. Kompetencer combines manually identified skill and knowledge spans with ESCO-derived fine-grained labels in Danish and English, with manual correction of the distantly supervised Danish test labels~\citep{jensen2022kompetencer}. \citet{gnehm2022skills} extract coarse EDU/EXP/LNG spans before refining skill areas for taxonomy matching.; file: tex/skillspan_style_related.tex; line: 11; citation_keys: sayfullina2018softskills; context: \citet{sayfullina2018softskills}; English & Candidate phrase in context & Relevance to an applicant; binary disambiguation, not open-boundary extraction & Annotated soft-skill contexts \\; file: tex/external_benchmarks/paper_methods.tex; line: 4; citation_keys: sayfullina2018softskills; context: To test whether domain-pretrained initialization helps consistently across recruitment tasks, the experiments compare XLM-R-large~\citep{conneau2020xlmr} and ESCOXLM-R~\citep{zhang2023escoxlmr}. They use six public datasets: SkillSpan~\citep{zhang2022skillspan}, Kompetencer~\citep{jensen2022kompetencer}, German ICT~\citep{gnehm2022transfer}, Green~\citep{green2022benchmark}, Sayfullina~\citep{sayfullina2018softskills}, and FIJO~\citep{beauchemin2022fijo}. Separate skill and knowledge streams in SkillSpan and Kompetencer give eight extraction tasks, each retaining its original entity types.

- **判断依据：** Aalto作者机构库确认三作者、2018、LNCS11179、141--152及二元候选短语消歧。正文已经正确区分该原任务；外部BIO任务需更明确指向 jjzha/sayfullina 派生版。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 已在附录明确通用协议采用公开发布的 BIO 抽取流；Sayfullina 是派生抽取任务，区别于原论文候选短语消歧。已有发布版链接保留。

- **尚需核实：** 派生 BIO 流与原任务的区别已写明；具体转换过程和实验使用版本仍以发布包/实验清单为准，不声称逐条回溯完成。

- **来源：** https://research.aalto.fi/en/publications/learning-representations-for-soft-skill-matching/

### R35 — 部分采纳

- **位置：** file: 1Introduction.tex; line: 4; citation_keys: senger2024survey; context: Online job advertisements describe the knowledge and skills employers seek and provide evidence of changing occupational requirements~\citep{ILO_2020_OJVs_BigData,senger2024survey}. Document-level methods retrieve skills from predefined inventories~\citep{bhola2020retrieving}, whereas span extraction locates the words expressing a requirement~\citep{gnehm2022skills}. Job Skill Named Entity Recognition (JobSkillNER) identifies these mentions and assigns a type to each span. Keeping the source wording makes boundary and type assignments available for inspection.; file: 5Relatedwork.tex; line: 8; citation_keys: senger2024survey; context: Taxonomy-based weak supervision can reduce manual annotation work~\citep{zhang2022weak}, but generated labels still need validation. \citet{nguyen2024rethinking} report difficulties with conjoined and ambiguous mentions across six recruitment datasets. \citet{senger2024survey} also identify scarce public annotations and inconsistent terminology. Table~\ref{tab:related-span} compares the prediction units, annotation layers, and available materials of selected resources.

- **判断依据：** 官方四作者、页码1--15及2024相符。现booktitle略简，不影响真实性。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留正确作者、年份、页码及 DOI/URL；当前会议名称仍为可识别的简写，本轮未实施可选的 First Workshop / 2024 扩展。

- **尚需核实：** 可选格式完善未实施：会议全名可补为 Proceedings of the First Workshop on Natural Language Processing for Human Resources (NLP4HR 2024)。

- **来源：** https://aclanthology.org/2024.nlp4hr-1.1/

### R36 — 待核实

- **位置：** file: tex/silver_plus_methods.tex; line: 6; citation_keys: tianchiRecruitment163746; context: Texts came from three routes: commercial collections purchased from MacroData~\citep{macrodataPlatform}; public-institution recruitment announcements collected by the research team; and the Recruitment Dataset (dataset ID 163746) on Alibaba Cloud Tianchi~\citep{tianchiRecruitment163746}. For public-institution announcements, team members selected pages from government portals, university and hospital websites, and public recruitment platforms across regions of China. A crawler revisited the registered URLs weekly or monthly. Screening and cleaning produced the public-institution subset. \hyperref[app:d]{Appendix D} records the available source metadata and gaps in the original collection history.

- **判断依据：** 当前天池页面仅返回 招聘数据集，dataset ID163746真实。无法从页面验证发布者身份、许可、具体下载批次；Tianchi作为平台署名需避免读者理解为原数据创作者。

- **证据层级：** 本轮web可读标题与ID；没有发布者/许可/批次字段

- **实际处理：** 保留天池平台署名、英文译名、原年份和含数据集编号 163746 的链接；已将 note 精简为“Title translated from Chinese; accessed 20 September 2026.”，删除重复标题/编号说明，以避免参考文献跨页仅余访问年份。该排版去重不代表原始发布者、下载批次或许可已核实。

- **尚需核实：** 原始发布者、授权范围和实际下载批次仍未核实；Tianchi 是托管平台，不能推定其为原始数据创建者。

- **来源：** https://tianchi.aliyun.com/dataset/163746/

### R37 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 16; citation_keys: ulhaq2026nerannotation; context: \paragraph{Model-assisted annotation and extraction models.} LLMs can supply first-pass labels, with their usefulness depending on task instructions and human validation~\citep{ding2023annotator,li2023coannotating,ulhaq2026nerannotation}. GoLLIE and subsequent guideline-refinement work study how annotation instructions shape model outputs~\citep{gollie2024,kim2026guidelines}. In recruitment, JobSkape generates synthetic advertisements for skill-to-taxonomy matching~\citep{magron2024jobskape}. Chinese-SkillSpan retains collected recruitment texts and adds model-generated annotations with documented review. The annotation prompts follow the handbook used at each stage.

- **判断依据：** 官方LREC2026、524--548、三作者与稿件相符；标题及DOI真实。当前用为标注质量相关研究，相关性合理。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留已核实的 LREC 2026 正式文献和标注质量背景用途。

- **来源：** https://aclanthology.org/2026.lrec-1.37/

### R38 — 已解决

- **位置：** file: tex/external_benchmarks/paper_appendix.tex; line: 5; citation_keys: vandergoot2021machamp; context: We reran BERT~\citep{devlin2019bert}, SpanBERT~\citep{joshi2020spanbert}, JobBERT, and JobSpanBERT~\citep{zhang2022skillspan} separately for skills and knowledge on SkillSpan's public HOUSE and TECH subsets. The MaChAmp~\citep{vandergoot2021machamp} \texttt{seq\_bio} CRF runs used 20 epochs, development-set checkpoint selection, and five seeds listed in the \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/source/tex/external_benchmarks/paper_appendix.tex}{experiment records}. BIG was unavailable; multi-task training was not rerun. Table~\ref{tab:external-native} gives MaChAmp per-site span-F1. The \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/README.md#skillspan-pooled-scores-previous-table-25}{archived pooled scores} report BIO rescoring of the same predictions with the correct task column. These scoring procedures yield different results. The native runs contain 3,570 test sentences, compared with 3,569 in the common-protocol release; the one-record difference has not been resolved by matching IDs. For published test references, we use only the original paper's TEST/STL rows. Its HOUSE/TECH rows report development results.

- **判断依据：** 官方EACL Demos2021、176--197、五作者与稿件相符。MaChAmp是实际执行工具，引用必要。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留实际执行工具 MaChAmp 的原始论文引用。

- **来源：** https://aclanthology.org/2021.eacl-demos.22/

### R39 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 20; citation_keys: gptner2025; context: Other approaches use text-to-structure generation in UIE~\citep{uie2022}, distilled supervision in UniversalNER~\citep{universalner}, open-type encoder extraction in GLiNER~\citep{gliner-naacl24}, and generative extraction with self-verification in GPT-NER~\citep{gptner2025}. These approaches provide methodological context; they are not additional evaluated baselines. The models tested here, their supervision, and their scoring protocols are specified in \nameref{sec:experiments}.

- **判断依据：** 官方Findings NAACL2025、4257--4275与现书目相符；无需回退预印本年份。自验证描述正确。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留 Findings NAACL 2025 正式记录；相关工作已明确 GPT-NER 属于方法背景而非本文实测模型。

- **来源：** https://aclanthology.org/2025.findings-naacl.239/

### R40 — 采纳

- **位置：** file: 5Relatedwork.tex; line: 12; citation_keys: cluener2020; context: \paragraph{Chinese span annotation and competency guidelines.} Chinese NER resources cover social-media text~\citep{peng2015weibo} and fine-grained entity categories~\citep{cluener2020}. Multilingual studies examine recognition in noisy text~\citep{multiconer2023} and changes in contextual entity types~\citep{dynamicner2025}. These tasks provide useful background, but do not specify how recruitment requirements should be divided into LSKT spans. Chinese boundary detection is complicated by the absence of explicit word delimiters~\citep{chen2021boundary}; recruitment annotation additionally distinguishes knowledge, occupational actions, and transversal competences within each clause.

- **判断依据：** 已直接读取arXiv官方BibTeX：正式题名含 Dataset and Benchmark，10作者含第二人 Yu tong；现稿题名不全且漏此作者。arXiv预印本身份本身不是删除理由；只用于一般中文细粒度NER背景。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 已补全 CLUENER2020 正式题名及第十名作者，第二作者按官方原样保留为 Yu tong；固定 arXiv v4 入口，正文限定为一般中文细粒度 NER 背景。

- **来源：** https://arxiv.org/bibtex/2001.04351

### R41 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 20; citation_keys: gliner-naacl24; context: Other approaches use text-to-structure generation in UIE~\citep{uie2022}, distilled supervision in UniversalNER~\citep{universalner}, open-type encoder extraction in GLiNER~\citep{gliner-naacl24}, and generative extraction with self-verification in GPT-NER~\citep{gptner2025}. These approaches provide methodological context; they are not additional evaluated baselines. The models tested here, their supervision, and their scoring protocols are specified in \nameref{sec:experiments}.

- **判断依据：** 官方NAACL2024、5364--5376、四作者与稿件相符。开放类型双向编码器归类准确，当前仅方法背景。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留 GLiNER 正式文献；相关工作已明确其开放类型编码器方法是背景，不是新增实测基线。

- **来源：** https://aclanthology.org/2024.naacl-long.300/

### R42 — 部分采纳

- **位置：** file: 1Introduction.tex; line: 8; citation_keys: jensen2022kompetencer; context: Existing resources provide precedents, but their annotation schemes differ. English SkillSpan permits overlapping SKILL and KNOWLEDGE layers~\citep{zhang2022skillspan}. Kompetencer adds ESCO-derived fine-grained classification to Danish and English spans~\citep{jensen2022kompetencer}. German recruitment work extracts education, experience, and language requirements before finer classification~\citep{gnehm2022skills}. Document-level retrieval and Chinese skill-demand forecasting use other prediction targets~\citep{bhola2020retrieving,chen2024jobsdf}.; file: 5Relatedwork.tex; line: 4; citation_keys: jensen2022kompetencer; context: \paragraph{Skill extraction and recruitment datasets.} Recruitment datasets differ first in what a system must predict. \citet{sayfullina2018softskills} ask whether a candidate soft-skill phrase refers to an applicant, whereas \citet{bhola2020retrieving} retrieve skills from a predefined inventory for an entire advertisement. Span extraction locates the words expressing a requirement. Within that task, SkillSpan annotates English SKILL and KNOWLEDGE in two potentially overlapping layers; hard and soft skills describe its coverage rather than its label inventory~\citep{zhang2022skillspan}. Kompetencer combines manually identified skill and knowledge spans with ESCO-derived fine-grained labels in Danish and English, with manual correction of the distantly supervised Danish test labels~\citep{jensen2022kompetencer}. \citet{gnehm2022skills} extract coarse EDU/EXP/LNG spans before refining skill areas for taxonomy matching.; file: tex/skillspan_style_related.tex; line: 14; citation_keys: jensen2022kompetencer; context: \citet{jensen2022kompetencer}; Danish / English & Spans and fine-grained labels & Manual skill/knowledge spans; ESCO API distant labels; Danish test-label correction & Dataset and code \\; file: tex/external_benchmarks/paper_methods.tex; line: 4; citation_keys: jensen2022kompetencer; context: To test whether domain-pretrained initialization helps consistently across recruitment tasks, the experiments compare XLM-R-large~\citep{conneau2020xlmr} and ESCOXLM-R~\citep{zhang2023escoxlmr}. They use six public datasets: SkillSpan~\citep{zhang2022skillspan}, Kompetencer~\citep{jensen2022kompetencer}, German ICT~\citep{gnehm2022transfer}, Green~\citep{green2022benchmark}, Sayfullina~\citep{sayfullina2018softskills}, and FIJO~\citep{beauchemin2022fijo}. Separate skill and knowledge streams in SkillSpan and Kompetencer give eight extraction tasks, each retaining its original entity types.; file: tex/external_benchmarks/paper_A_native.tex; line: 2; citation_keys: jensen2022kompetencer; context: Kompetencer fine-grained classification~\citep{jensen2022kompetencer} and NNOSE~\citep{zhang2024nnose} were run on an NVIDIA A100 (80 GB). Software versions and compatibility records are provided in the \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/1d1c24e20ee049fc768034b5baf58fa882e08e2c/reproduction/process_archive_20260924/secondary_review/source/tex/external_benchmarks/paper_A_native.tex}{native-task configurations}. These experiments retain their task-specific metrics and are separate from the common linear-head protocol.

- **判断依据：** 官方LREC2022、436--447、三作者与稿件相符。原任务为细粒度分类；当前把原任务分类和公共BIO流分开，已披露指标/选模不同。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 已明确公开 BIO 抽取流与给定跨度的细粒度分类是不同任务；新增 RemBERT 原始文献，并保留实际 uncased 初始化、英文开发集选模和非加权指标的限定。

- **尚需核实：** 实际 uncased 初始化与原始 cased 配置、指标和选模协议差异已披露；本轮未将结果升级为逐项匹配复现。

- **来源：** https://aclanthology.org/2022.lrec-1.46/

### R43 — 已解决

- **位置：** file: 1Introduction.tex; line: 8; citation_keys: zhang2022skillspan; context: Existing resources provide precedents, but their annotation schemes differ. English SkillSpan permits overlapping SKILL and KNOWLEDGE layers~\citep{zhang2022skillspan}. Kompetencer adds ESCO-derived fine-grained classification to Danish and English spans~\citep{jensen2022kompetencer}. German recruitment work extracts education, experience, and language requirements before finer classification~\citep{gnehm2022skills}. Document-level retrieval and Chinese skill-demand forecasting use other prediction targets~\citep{bhola2020retrieving,chen2024jobsdf}.; file: 5Relatedwork.tex; line: 4; citation_keys: zhang2022skillspan; context: \paragraph{Skill extraction and recruitment datasets.} Recruitment datasets differ first in what a system must predict. \citet{sayfullina2018softskills} ask whether a candidate soft-skill phrase refers to an applicant, whereas \citet{bhola2020retrieving} retrieve skills from a predefined inventory for an entire advertisement. Span extraction locates the words expressing a requirement. Within that task, SkillSpan annotates English SKILL and KNOWLEDGE in two potentially overlapping layers; hard and soft skills describe its coverage rather than its label inventory~\citep{zhang2022skillspan}. Kompetencer combines manually identified skill and knowledge spans with ESCO-derived fine-grained labels in Danish and English, with manual correction of the distantly supervised Danish test labels~\citep{jensen2022kompetencer}. \citet{gnehm2022skills} extract coarse EDU/EXP/LNG spans before refining skill areas for taxonomy matching.; file: 5Relatedwork.tex; line: 18; citation_keys: zhang2022skillspan; context: Encoder models offer one way to learn from these labels. Pretrained encoders and structured decoding~\citep{devlin2019bert,lafferty2001crf} can be combined with continued pretraining on recruitment text~\citep{gururangan2020dapt,zhang2022skillspan}. SkillSpan introduced the domain-adapted JobBERT and JobSpanBERT baselines~\citep{zhang2022skillspan}. ESCOXLM-R uses taxonomy-driven multilingual pretraining~\citep{zhang2023escoxlmr}, and NNOSE retrieves training-data representations to support extraction, including infrequent patterns~\citep{zhang2024nnose}. Reproducing these methods on their original tasks and adapting them to Chinese LSKT extraction require separate protocols because the languages, annotation layers, and splits differ.; file: tex/skillspan_style_related.tex; line: 13; citation_keys: zhang2022skillspan; context: \citet{zhang2022skillspan}; English & Source-text spans & SKILL / KNOWLEDGE; overlap permitted between the two layers & Dataset, code, and annotation guidance \\; file: 2Framework.tex; line: 36; citation_keys: zhang2022skillspan; context: We adapted SkillSpan's semantic-completeness and coordination principles for Chinese annotation~\citep{zhang2022skillspan}. Our handbook asks annotators to select the shortest source span that preserves the complete requirement, without a fixed length cap. Generic proficiency triggers usually remain outside the span, but a modal can remain inside a complete colloquial capability expression. Necessary action heads and complements are retained. Coordinated activities are split only when each remains interpretable; a shared action and its objects stay together. Figure~\ref{fig:illustrative-annotations} illustrates these distinctions.; file: tex/external_benchmarks/paper_methods.tex; line: 4; citation_keys: zhang2022skillspan; context: To test whether domain-pretrained initialization helps consistently across recruitment tasks, the experiments compare XLM-R-large~\citep{conneau2020xlmr} and ESCOXLM-R~\citep{zhang2023escoxlmr}. They use six public datasets: SkillSpan~\citep{zhang2022skillspan}, Kompetencer~\citep{jensen2022kompetencer}, German ICT~\citep{gnehm2022transfer}, Green~\citep{green2022benchmark}, Sayfullina~\citep{sayfullina2018softskills}, and FIJO~\citep{beauchemin2022fijo}. Separate skill and knowledge streams in SkillSpan and Kompetencer give eight extraction tasks, each retaining its original entity types.; file: tex/appendix_A_guide_R19.tex; line: 23; citation_keys: zhang2022skillspan; context: \noindent\textit{Source key.} E: ESCO's \href{https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar}{skills hierarchy} and \href{https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/transversal-knowledge-skills-and-competences}{transversal concepts} \citep{ESCOv1_2_2024}; Q: EQF definitions \citep{council2017eqf}; Z: related annotation guidance in SkillSpan, Appendix B \citep{zhang2022skillspan}; I: unitization and categorization in agreement analysis \citep{artstein2008agreement}; P: our V4.2.14 operational decision. Combined marks indicate adaptation, not a verbatim source rule. Chinese examples and their exact boundaries are project illustrations.; file: tex/external_benchmarks/paper_appendix.tex; line: 5; citation_keys: zhang2022skillspan; context: We reran BERT~\citep{devlin2019bert}, SpanBERT~\citep{joshi2020spanbert}, JobBERT, and JobSpanBERT~\citep{zhang2022skillspan} separately for skills and knowledge on SkillSpan's public HOUSE and TECH subsets. The MaChAmp~\citep{vandergoot2021machamp} \texttt{seq\_bio} CRF runs used 20 epochs, development-set checkpoint selection, and five seeds listed in the \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/source/tex/external_benchmarks/paper_appendix.tex}{experiment records}. BIG was unavailable; multi-task training was not rerun. Table~\ref{tab:external-native} gives MaChAmp per-site span-F1. The \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/README.md#skillspan-pooled-scores-previous-table-25}{archived pooled scores} report BIO rescoring of the same predictions with the correct task column. These scoring procedures yield different results. The native runs contain 3,570 test sentences, compared with 3,569 in the common-protocol release; the one-record difference has not been resolved by matching IDs. For published test references, we use only the original paper's TEST/STL rows. Its HOUSE/TECH rows report development results.; file: tex/external_benchmarks/paper_tables_appendix.tex; line: 40; citation_keys: zhang2022skillspan; context: \par\smallskip\RaggedRight\footnotesize Published values are the TEST/STL results in Table 5 of \citet{zhang2022skillspan}, converted from percent and rounded to three decimal places; their HOUSE/TECH rows report development results. Our reruns use MaChAmp per-site span-F1 on public HOUSE+TECH, excluding BIG. The evaluation samples differ, so score differences cannot be interpreted as matched replication gaps. The source table gives no SpanBERT TEST score. Multi-task training was not rerun.

- **判断依据：** 官方NAACL2022、4962--4984、四作者相符；两层技能/知识与论文吻合。已读当前附录限定 HOUSE/TECH、排除BIG、区分DEV与TEST。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留 SkillSpan 原始文献与 HOUSE/TECH、排除 BIG、原始 TEST/STL 对比的限定；SpanBERT 无已发表 TEST 项继续留空且不补造。

- **尚需核实：** 公开 HOUSE/TECH 子集与原文总体 TEST 的样本差异仍存在，不能把分数差认作匹配复现误差。

- **来源：** https://aclanthology.org/2022.naacl-main.366/

### R44 — 已解决

- **位置：** file: 5Relatedwork.tex; line: 8; citation_keys: zhang2022weak; context: Taxonomy-based weak supervision can reduce manual annotation work~\citep{zhang2022weak}, but generated labels still need validation. \citet{nguyen2024rethinking} report difficulties with conjoined and ambiguous mentions across six recruitment datasets. \citet{senger2024survey} also identify scarce public annotations and inconsistent terminology. Table~\ref{tab:related-span} compares the prediction units, annotation layers, and available materials of selected resources.

- **判断依据：** CEUR官方Vol3218目录直接确认该论文题名、四作者与2022年。弱监督方法相关；当前论断不称其标签为Gold。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留 CEUR 正式目录支持的弱监督文献，未将其弱标签表述为 Gold。

- **来源：** https://ceur-ws.org/Vol-3218/

### R45 — 部分采纳

- **位置：** file: 5Relatedwork.tex; line: 18; citation_keys: zhang2024nnose; context: Encoder models offer one way to learn from these labels. Pretrained encoders and structured decoding~\citep{devlin2019bert,lafferty2001crf} can be combined with continued pretraining on recruitment text~\citep{gururangan2020dapt,zhang2022skillspan}. SkillSpan introduced the domain-adapted JobBERT and JobSpanBERT baselines~\citep{zhang2022skillspan}. ESCOXLM-R uses taxonomy-driven multilingual pretraining~\citep{zhang2023escoxlmr}, and NNOSE retrieves training-data representations to support extraction, including infrequent patterns~\citep{zhang2024nnose}. Reproducing these methods on their original tasks and adapting them to Chinese LSKT extraction require separate protocols because the languages, annotation layers, and splits differ.; file: tex/external_benchmarks/paper_A_native.tex; line: 2; citation_keys: zhang2024nnose; context: Kompetencer fine-grained classification~\citep{jensen2022kompetencer} and NNOSE~\citep{zhang2024nnose} were run on an NVIDIA A100 (80 GB). Software versions and compatibility records are provided in the \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/1d1c24e20ee049fc768034b5baf58fa882e08e2c/reproduction/process_archive_20260924/secondary_review/source/tex/external_benchmarks/paper_A_native.tex}{native-task configurations}. These experiments retain their task-specific metrics and are separate from the common linear-head protocol.

- **判断依据：** 官方EACL2024、589--608、四作者相符。当前已说明仅in-dataset datastore、单种子；末尾 no consistent retrieval benefit 需始终限定为这些运行。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留 NNOSE 原方法引用；当前结论明确为这些单种子运行，表题和注释限定为同数据集训练 datastore，并说明未评价全数据集 datastore。

- **尚需核实：** 未评价跨数据集 datastore，且仅单种子；仍不能据此判定原方法整体无效。

- **来源：** https://aclanthology.org/2024.eacl-long.35/

### R46 — 部分采纳

- **位置：** file: 5Relatedwork.tex; line: 18; citation_keys: zhang2023escoxlmr; context: Encoder models offer one way to learn from these labels. Pretrained encoders and structured decoding~\citep{devlin2019bert,lafferty2001crf} can be combined with continued pretraining on recruitment text~\citep{gururangan2020dapt,zhang2022skillspan}. SkillSpan introduced the domain-adapted JobBERT and JobSpanBERT baselines~\citep{zhang2022skillspan}. ESCOXLM-R uses taxonomy-driven multilingual pretraining~\citep{zhang2023escoxlmr}, and NNOSE retrieves training-data representations to support extraction, including infrequent patterns~\citep{zhang2024nnose}. Reproducing these methods on their original tasks and adapting them to Chinese LSKT extraction require separate protocols because the languages, annotation layers, and splits differ.; file: tex/external_benchmarks/paper_methods.tex; line: 4; citation_keys: zhang2023escoxlmr; context: To test whether domain-pretrained initialization helps consistently across recruitment tasks, the experiments compare XLM-R-large~\citep{conneau2020xlmr} and ESCOXLM-R~\citep{zhang2023escoxlmr}. They use six public datasets: SkillSpan~\citep{zhang2022skillspan}, Kompetencer~\citep{jensen2022kompetencer}, German ICT~\citep{gnehm2022transfer}, Green~\citep{green2022benchmark}, Sayfullina~\citep{sayfullina2018softskills}, and FIJO~\citep{beauchemin2022fijo}. Separate skill and knowledge streams in SkillSpan and Kompetencer give eight extraction tasks, each retaining its original entity types.; file: tex/external_benchmarks/paper_appendix.tex; line: 7; citation_keys: zhang2023escoxlmr; context: For the German public ICT task~\citep{gnehm2022transfer}, jobBERT-de used a 20-epoch MaChAmp configuration and ESCOXLM-R used its released five-epoch configuration~\citep{zhang2023escoxlmr}. Both used five recorded seeds. Compatibility fields were added for newer MaChAmp without changing the learning rate or epoch limit; the exact changes are archived. The runs therefore use the public releases with compatibility changes, rather than recreating every original environment. They contain 2,557 test sentences, whereas the ESCOXLM-R paper reports 2,943. The ICT extraction task differs from the EDU/EXP/LNG extraction and taxonomy-classification pipeline described by \citet{gnehm2022skills}.; file: tex/external_benchmarks/paper_tables_appendix.tex; line: 56; citation_keys: zhang2023escoxlmr; context: \par\smallskip\RaggedRight\footnotesize Reruns use 2,557 test sentences. The published ESCOXLM-R score comes from Table 2 of \citet{zhang2023escoxlmr}, whose Table 1 reports 2,943 test sentences. These different releases prevent a matched comparison with the published score. No corresponding published jobBERT-de score is supplied. Epoch budgets differ between the two models here, unlike in the common-protocol comparison.

- **判断依据：** 官方ACL2023、11871--11890、三作者相符，Taxonomy-driven initialization描述正确。German ICT出处应另引Gnehm LREC2022而非四作者NLP+CSS。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 保留 ESCOXLM-R 正式文献；配合 R16 将 German ICT 原始出处改引 LREC 2022 文献，不改实验数值。

- **尚需核实：** 公开 German ICT 测试记录数与原文不同，且原任务复跑训练预算不同；保留不作匹配分数比较的限定。

- **来源：** https://aclanthology.org/2023.acl-long.662/

### R47 — 部分采纳

- **判断依据：** PMC正式全文直接确认四作者、PeerJ CS9:e1535、2023，并确实讨论长/嵌套实体。并非完全无关，但本稿flat招聘跨度与此任务不同，跨领域例句对当前论证贡献有限。

- **证据层级：** 本轮web已读取PMC全文；脚本取不到正文不影响已有web全文证据

- **实际处理：** 为聚焦招聘跨度问题，已删除康复医学跨领域例句和正文引用；zhong2023bertspan 的真实书目仍保留。删除原因是篇幅与论证重点，不是文献不实。

- **来源：** https://pmc.ncbi.nlm.nih.gov/articles/PMC10495977/

### R48 — 部分采纳

- **位置：** file: 5Relatedwork.tex; line: 20; citation_keys: universalner; context: Other approaches use text-to-structure generation in UIE~\citep{uie2022}, distilled supervision in UniversalNER~\citep{universalner}, open-type encoder extraction in GLiNER~\citep{gliner-naacl24}, and generative extraction with self-verification in GPT-NER~\citep{gptner2025}. These approaches provide methodological context; they are not additional evaluated baselines. The models tested here, their supervision, and their scoring protocols are specified in \nameref{sec:experiments}.

- **判断依据：** ICLR官方记录确认五作者及2024，distillation方法概述正确。现书目无URL。

- **证据层级：** 本轮已读取官方网页/元数据；相关性依据当前引用上下文；非声称全文均精读

- **实际处理：** 已明确 UniversalNER 只是方法背景；现有正确作者、年份与会议保留，当前尚未添加可选官方 URL 字段。

- **尚需核实：** 可选格式完善未实施：补 ICLR 官方永久链接；现有书目仍可识别。

- **来源：** https://proceedings.iclr.cc/paper_files/paper/2024/hash/34678d08b36076de986df95c5bbba92f-Abstract-Conference.html

## 文字 W01–W58

### W01 — 采纳

- **位置：** 0main.tex；line 144: Chinese job advertisements express competencies
- **依据：** 摘要现以中文并列结构、语境依赖和字符边界开头。 本轮修改记录与当前源码匹配：0main.tex。
- **判断：** 原must泛化为所有benchmark的要求，改具体任务动机更准确。
- **实际处理：** 改为中文招聘表达特点及系统比较所需的一致边界和类型判断。
- **边界或后续事项：** 无新增实证声明。

### W02 — 不采纳

- **位置：** 0main.tex；line 145: We developed Chinese-SkillSpan from a corpus
- **依据：** 原文from a corpus限定22,840为来源语料；正文数据层表逐项记录150、2,451、9,540和独立50句。
- **判断：** 用户明确要求摘要突出三项贡献，不能强制堆入所有历史样本量；也无证据认定原摘要把来源语料写成全量gold。
- **实际处理：** 保留摘要的来源规模、手册形成、人工/Silver层及盲编设计，未追加150/9,540/50数字串。
- **边界或后续事项：** 完整规模与用途仍须以正文数据层表为准。

### W03 — 已解决

- **位置：** 0main.tex；line 146: Silver-supervised Qwen adaptation improved
- **依据：** 现摘要准确报告no-adapter 0.361与三种子均值0.540±0.035，并说明所有长度组recall均提升。
- **判断：** 本轮此前已按用户意见先呈现正向核心结果；不必将全部区间和不显著的ESCO对比塞回摘要。
- **实际处理：** 保留已改好的Qwen结果开头及独立编码的定性发现，未恢复ESCO区间或以0.663开头。
- **边界或后续事项：** ESCO差值和配对区间继续完整保留于正文；摘要不得把均值±SD称为CI。

### W04 — 采纳

- **位置：** 0main.tex；line 147: Chinese-SkillSpan pairs source-text spans
- **依据：** 现结论句明确原文跨度、标注规则、人工/Silver标签及边界类型错误检查。 本轮修改记录与当前源码匹配：0main.tex。
- **判断：** 替换抽象interpretable表述可让资源贡献对应可操作对象。
- **实际处理：** 改为资源配对内容及模型比较、错误检查用途；保留发展使用参考集限制。
- **边界或后续事项：** 不由可检查性推断独立泛化或全量标注准确性。

### W05 — 采纳

- **位置：** 1Introduction.tex；line 4: Document-level methods retrieve skills
- **依据：** Bhola对应预定义词表检索；Gnehm对应招聘要求原文跨度。 本轮修改记录与当前源码匹配：1Introduction.tex。
- **判断：** 不能由文档级检索论文推出所有应用必须保留词串。
- **实际处理：** 拆开两类任务及引文；删除缺直接支撑的job–curriculum匹配强断言。
- **边界或后续事项：** 未新增未经核实的课程匹配来源。

### W06 — 采纳

- **位置：** 1Introduction.tex；line 12: The study addresses three linked questions
- **依据：** 现研究目的连贯对应规则、标注一致性和模型表现。 本轮修改记录与当前源码匹配：1Introduction.tex。
- **判断：** 原三次问答交替显得像提纲，实际内容可保留。
- **实际处理：** 改为一段三个关联问题及其证据设计，取消问答式拼接。
- **边界或后续事项：** 不把研究目的写成已获证实的贡献。

### W07 — 采纳

- **位置：** 1Introduction.tex；line 14: The original corpus and its smaller
- **依据：** 现保留语料/子集用途及150句参考用于指南开发。 本轮修改记录与当前源码匹配：1Introduction.tex。
- **判断：** 删抽象贡献总结和提前重复跨语限制，不应删参考集依赖事实。
- **实际处理：** 压缩为数据角色、诊断用途和外部任务比较三句。
- **边界或后续事项：** 独立性与跨任务可比条件在方法/局限保留。

### W08 — 采纳

- **位置：** tex/silver_plus_methods.tex；line 46: Lengths count source Unicode code points
- **依据：** 字符计数提醒从相关工作转入长度统计说明。 本轮修改记录与当前源码匹配：5Relatedwork.tex, tex/silver_plus_methods.tex。
- **判断：** 正确计量单位应随统计结果给出，而非打断中文先行研究介绍。
- **实际处理：** 移至语料统计，明确Unicode码点包含标点空格且不可直接比英语token。
- **边界或后续事项：** 数值和重复B2记录处理未变。

### W09 — 部分采纳

- **位置：** 5Relatedwork.tex；line 12: Chinese NER resources cover social-media
- **依据：** 现分别将社交媒体、细粒度类别、噪声、多语语境归于相应来源。 本轮修改记录与当前源码匹配：5Relatedwork.tex。
- **判断：** 邻域论文是真实背景，但不能为招聘LSKT规则直接背书。
- **实际处理：** 重写各来源作用；删除医学长嵌套例以聚焦任务，保留合理通用NER背景。
- **边界或后续事项：** 删医学引文是论证取舍，不是判论文不真实或毫无关联。

### W10 — 采纳

- **位置：** 5Relatedwork.tex；line 14: The handbook specifies when tool use
- **依据：** 现句列出工具S/K、共享动作及经验边界。 本轮修改记录与当前源码匹配：5Relatedwork.tex。
- **判断：** 具体操作决策比重复贡献口号有信息量。
- **实际处理：** 以三类规则替换operational guidance泛称。
- **边界或后续事项：** 仍为项目操作化，不冒称ESCO直接规定中文边界。

### W11 — 采纳

- **位置：** 5Relatedwork.tex；line 20: These approaches provide methodological context
- **依据：** UIE等段落现明确未作为新增实测基线。 本轮修改记录与当前源码匹配：5Relatedwork.tex。
- **判断：** 避免相关方法与实际comparison指代混淆。
- **实际处理：** 明确方法背景身份，并交叉引用实际Evaluation Protocol。
- **边界或后续事项：** 本轮未运行所列未测方法。

### W12 — 采纳

- **位置：** 2Framework.tex；line 2: \section{Corpus and Annotation}
- **依据：** 原must式章节预告已删除，直接进入任务定义。 本轮修改记录与当前源码匹配：2Framework.tex。
- **判断：** 与标题和后文重复，无需再次作规范性宣告。
- **实际处理：** 删除空泛章节概述；直接进入任务定义。
- **边界或后续事项：** 定义、公式及后续动机未改变。

### W13 — 采纳

- **位置：** 2Framework.tex；line 17: Figure~\ref{fig:coding-detail} separates
- **依据：** 现用Figure2及数据层表承接三个研究角色。 本轮修改记录与当前源码匹配：2Framework.tex。
- **判断：** 短交叉引用足以引导，减少重复铺垫。
- **实际处理：** 改为图示分离角色、表格列规模及用途；删此处外部任务插句。
- **边界或后续事项：** 图2的历史人工、Silver和独立IAA三层保持。

### W14 — 采纳

- **位置：** tex/silver_plus_methods.tex；line 4: The corpus contains 22,840
- **依据：** 现语料节直接说明来源及原始划分。 本轮修改记录与当前源码匹配：tex/silver_plus_methods.tex。
- **判断：** 抽象cover varied并不解释子集用途，后续实体信息更清楚。
- **实际处理：** 删除泛化目的句，保留可核验规模与角色表引用。
- **边界或后续事项：** 四类来源名称不等于互斥行业覆盖。

### W15 — 部分采纳

- **位置：** tex/silver_plus_methods.tex；line 37: The expanded Codex Silver pool contains
- **依据：** 9,540主池突出，9,646仍标为另一注释通道的独立版本。 本轮修改记录与当前源码匹配：tex/silver_plus_methods.tex。
- **判断：** 无需把所有准备阶段计数放正文，但不能隐藏实际采用的另一个版本。
- **实际处理：** 压缩原2,064+7,936准备过程，前置9,540；抽样排除细节指向附录D。
- **边界或后续事项：** 9,540与9,646不可相加，实验版本仍分别保留。

### W16 — 部分采纳

- **位置：** tex/silver_plus_methods.tex；line 22: Original corpus & 22,840
- **依据：** 角色列现为Source corpus and original partition。 本轮修改记录与当前源码匹配：tex/silver_plus_methods.tex。
- **判断：** 去除可能暗示整库统一标注的角色名称，不据此断言原语料完全没有任何标注。
- **实际处理：** 仅改该单元格的用途描述；规模及原始分区未动。
- **边界或后续事项：** 原始各层标签版本仍需逐文件追溯，不以本次措辞代替审计。

### W17 — 采纳

- **位置：** 2Framework.tex；line 36: We adapted SkillSpan's semantic-completeness
- **依据：** 现将完整性/并列原则归于SkillSpan改编，具体中文要求归本项目手册。 本轮修改记录与当前源码匹配：2Framework.tex。
- **判断：** 原引用紧贴无长度上限易被理解成原文直接规定。
- **实际处理：** 拆为参考原则与本手册操作要求两句。
- **边界或后续事项：** 最短完整跨度、无固定长度上限等规则含义未变。

### W18 — 部分采纳

- **位置：** 2Framework.tex；line 42: Type depends on what the clause requires
- **依据：** 现英语举using SQL与knowledge of SQL principles，图4仍为真实原文例。 本轮修改记录与当前源码匹配：2Framework.tex。
- **判断：** 具体对照有帮助，但不必把新的中文教学片段再塞回行文。
- **实际处理：** 改开头两句为英文S/K语境例，保留图4及附录引用。
- **边界或后续事项：** 不能将SQL固定为S或K；不能称图4为当前版本重标样本。

### W19 — 部分采纳

- **位置：** 2Framework.tex；line 44: Under the current handbook
- **依据：** 现明确provisional S在裁决记录中且全条未决记录不得进入最终训练。 本轮修改记录与当前源码匹配：2Framework.tex。
- **判断：** 手册规则有据，历史执行全覆盖未核实；不能靠改写宣称实现已闭合。
- **实际处理：** 把句子限定为current handbook要求，明确临时S不是accepted target。
- **边界或后续事项：** 历史导出状态字段及逐记录过滤执行仍待核实。

### W20 — 采纳

- **位置：** 2Framework.tex；line 49: Historical human coding informed
- **依据：** 工作流段仅保留手册/参考形成、bulk前审核及结构/语义检查。 本轮修改记录与当前源码匹配：2Framework.tex, tex/annotation_quality_R12.tex。
- **判断：** 与紧邻质量节的盲编/辅助复核原理重复。
- **实际处理：** 删重复原则描述；原则统一于annotation_quality_R12开头。
- **边界或后续事项：** 原始Silver实际抽样审核范围未扩张。

### W21 — 采纳

- **位置：** tex/annotation_quality_R12.tex；line 4: Independent coding assesses whether
- **依据：** 开头合并盲编与辅助复核区分，随后直接进入三人协议。 本轮修改记录与当前源码匹配：2Framework.tex, tex/annotation_quality_R12.tex。
- **判断：** 原则必要，保留一次并保留历史样本版本不同的限制。
- **实际处理：** 压缩为一次定义、当前IAA表指向及历史不可纵比说明。
- **边界或后续事项：** 未把历史15句可见机器建议研究改称盲编。

### W22 — 部分采纳

- **位置：** 2Framework.tex；line 56: We cannot verify from the retained release records
- **依据：** 保留记录不足这一事实，未发现可证明系统脱敏的资料。 本轮修改记录与当前源码匹配：2Framework.tex。
- **判断：** 原第三方审计口吻可改主动语态；不能据记录不全断言没有做过。
- **实际处理：** 改为无法从保留记录核实系统审核/删除，说明删除率不可得。
- **边界或后续事项：** 需实际隐私审计与记录，不能补造脱敏率或机构许可。

### W23 — 采纳

- **位置：** 3Experiments.tex；line 4: The evaluation compares prompted extraction
- **依据：** 方法开头明确提示抽取、Qwen适配、encoder初始化及类型/长度/空句诊断。 本轮修改记录与当前源码匹配：3Experiments.tex。
- **判断：** informative比较过抽象，应列可检验目标。
- **实际处理：** 改成具体比较目的并说明不同评测层使用各自协议。
- **边界或后续事项：** 未扩大外部任务和中文任务的可比性。

### W24 — 采纳

- **位置：** tex/appendix_C_experiments_R16.tex；line 5: Scores and differences are calculated
- **依据：** 舍入规则移入补充评测开头；主方法不再占一长句。 本轮修改记录与当前源码匹配：3Experiments.tex, tex/appendix_C_experiments_R16.tex。
- **判断：** 显示细节是必要统计说明，但不应打断核心方法。
- **实际处理：** 统一说明先计算后舍入、三位小数及近零端点科学计数法。
- **边界或后续事项：** 所有分数和区间仍以原始计算值为准。

### W25 — 部分采纳

- **位置：** 3Experiments.tex；line 46: JobBERT-zh provides a sequence-labeling baseline
- **依据：** 现直接写sequence labeling及generative extraction，并引qwen2025report/hu2022lora。 本轮修改记录与当前源码匹配：3Experiments.tex。
- **判断：** 结构与核心方法出处应明确；来源文献不等于已核实每个历史权重版本。
- **实际处理：** 重写比较目的并补Qwen2.5与LoRA原始引用键。
- **边界或后续事项：** 执行时Qwen原始Hub commit未保留的限制仍存在，不能由当前model ID补造。

### W26 — 采纳

- **位置：** tex/external_benchmarks/paper_methods.tex；line 6: Both models process the original Chinese
- **依据：** 保留首subword、128字符chunk、remainder、占位及原offset评分。 本轮修改记录与当前源码匹配：tex/external_benchmarks/paper_methods.tex。
- **判断：** 以可复现输入算法描述代替回应误解式executed pipeline。
- **实际处理：** 改正向方法叙述并明确新BIO头，未改变直接中文输入事实。
- **边界或后续事项：** 翻译数据或英语任务头均不是本实验方法；广告级独立性未建立。

### W27 — 部分采纳

- **位置：** tex/external_benchmarks/paper_methods.tex；line 8: Its linear heads and training budget differ
- **依据：** 训练预算、L稀少、条件bootstrap及跨任务差异在方法保留。 本轮修改记录与当前源码匹配：tex/external_benchmarks/paper_results.tex。
- **判断：** 限制有实质作用，可删结果末端重复，不能全部移除。
- **实际处理：** 删paper_results.tex重复跨语排名限制，保留方法完整条件。
- **边界或后续事项：** 非受控跨架构排名、聚类及多重比较限制仍有效。

### W28 — 采纳

- **位置：** tex/silver_plus_results.tex；line 4: The improvement includes better output compliance
- **依据：** 原始拒收计数69与2/4/1、固定parser及F1未变。 本轮修改记录与当前源码匹配：tex/silver_plus_results.tex。
- **判断：** 增益先报结果，再简要说明输出合规共同贡献。
- **实际处理：** 合并conditional解释为端到端改进及未分离语义/格式效应两句。
- **边界或后续事项：** 不能将增益归因为纯语义抽取能力。

### W29 — 部分采纳

- **位置：** 3Experiments.tex；line 73: Exploratory experiments with expanded supervision
- **依据：** 正文已将扩展研究标探索性，附录说明各因素未隔离。 本轮修改记录与当前源码匹配：tex/expanded_silver_results_20260917.tex。
- **判断：** 这是实证缺口，润色只能准确限定，不能宣布已诊断。
- **实际处理：** 配合W50压缩未完成诊断清单，保留JobBERT下降未解释。
- **边界或后续事项：** 标签版本、窗口截断、解码与预测逐项诊断尚未完成。

### W30 — 采纳

- **位置：** tex/external_benchmarks/paper_results.tex；line 4: The Chinese comparison does not establish
- **依据：** 删除higher relaxed/boundary表明sensitivity的泛化尾句；原得分在表中保留。 本轮修改记录与当前源码匹配：tex/external_benchmarks/paper_results.tex。
- **判断：** 放宽匹配得分提高不能单独说明语言机制。
- **实际处理：** 仅删除无额外证据的概括句，保留精确F1、区间及macro敏感性。
- **边界或后续事项：** 需要裁决错误分析才能确定具体语言构造原因。

### W31 — 采纳

- **位置：** tex/external_benchmarks/paper_results.tex；line 8: The original-task reruns answer
- **依据：** 相同限制仍在paper_methods末端明确。 本轮修改记录与当前源码匹配：tex/external_benchmarks/paper_results.tex。
- **判断：** 不必每个结果段再完整展开跨语不可排名。
- **实际处理：** 删结果末尾重复限定，保留任务不同与附录协议指向。
- **边界或后续事项：** 不能将绝对得分视为跨语言难度排序。

### W32 — 部分采纳

- **位置：** 3Experiments.tex；line 79: The three-annotator study shows
- **依据：** 现仍解释字符与完整typed span的不同以及历史例子不代表独立样本错误分布。 本轮修改记录与当前源码匹配：3Experiments.tex。
- **判断：** 核心解释有用，仅结尾supports retaining句空泛。
- **实际处理：** 删除泛化总结尾句，保留已有单位区别与边界/类型解释。
- **边界或后续事项：** 未新增精确错误成因分解；高字符alpha不替代span一致性。

### W33 — 采纳

- **位置：** 3Experiments.tex；line 83: The no-adapter Qwen score rises
- **依据：** 0.361 exact与0.470 relaxed对应同一Qwen基线表。 本轮修改记录与当前源码匹配：3Experiments.tex。
- **判断：** 具体匹配差异优于substantive benchmark outcome。
- **实际处理：** 改为明确0.109量级的匹配容忍影响并指向未裁决mismatch例。
- **边界或后续事项：** 聚合差值不能归因特定中文结构。

### W34 — 采纳

- **位置：** tex/expanded_silver_results_20260917.tex；line 8: Table~\ref{tab:expanded-silver-main} reports
- **依据：** 主文保留0.809/0.585及两套文本/目标不同；附录保留完整实验表。 本轮修改记录与当前源码匹配：tex/expanded_silver_results_20260917.tex。
- **判断：** 同一解释保留主文一次即可，附录职责是配置与数字。
- **实际处理：** 压缩附录重复成绩和解释为表格及主文讨论指向。
- **边界或后续事项：** 差值不能估计Silver标签错误率；不拼接成B2三种子结果。

### W35 — 部分采纳

- **位置：** 6Conclusion.tex；line 4: \textbf{Reference design and coverage.}
- **依据：** 现局限已有参考设计、数据/可复现性、实验比较三块。 本轮修改记录与当前源码匹配：6Conclusion.tex。
- **判断：** 不必机械套另一个三分框架；应保留关键可比性条件。
- **实际处理：** 删除泛化总括一句，保留三段有层次的实际限制。
- **边界或后续事项：** 新独立泛化、版本兼容、完整输入与历史选择缺口未由润色消除。

### W36 — 部分采纳

- **位置：** 6Conclusion.tex；line 13: It links original text and character offsets
- **依据：** 结论已解释原文/offset/手册/双层数据及独立编码作用。 本轮修改记录与当前源码匹配：6Conclusion.tex。
- **判断：** 用事实替换口号合理，但不宜再次用0.663作为整篇贡献的唯一总结。
- **实际处理：** 将versioned/inspectable口号改为可检查对象，保留一致性发现但不重复数字。
- **边界或后续事项：** 不把明确操作规则等同于所有标注均无歧义。

### W37 — 采纳

- **位置：** 6Conclusion.tex；line 15: Released Chinese-supervised encoder checkpoints
- **依据：** 记录支持公开checkpoint、prediction、本地重评分及服务器重推理，不是完整重训。 本轮修改记录与当前源码匹配：6Conclusion.tex。
- **判断：** reproducible alternatives容易超出已验证范围。
- **实际处理：** 改为允许inference checks and rescoring，保留配对区间限定。
- **边界或后续事项：** 未证明完整训练可重复。

### W38 — 部分采纳

- **位置：** tex/review20260923/access_matrix.tex；line 8: Core v0.1.3
- **依据：** 现有access matrix已补三个固定DOI（dataset、Qwen、encoder audit）、三编码员agreement release及pinned HF模型索引直接入口；与additional_edits.json逐条匹配。
- **判断：** 复用现有访问表并补直接链接比再建重复表更清楚；不能把PDF已有链接一概认定为无入口。
- **实际处理：** 在现有表中加入数据档案、模型档案、IAA及encoder模型/审计链接，保留各组件版本、能执行的检查和限制；未新增表。
- **边界或后续事项：** 独立IAA链接仍指main分支；本台账核实的是源码链接和记录，不能由此宣称所有训练材料公开可重训。

### W39 — 部分采纳

- **位置：** tex/appendix_A_guide_R19.tex；line 17: reader-facing v4.2.14 edition
- **依据：** 文档修订日与标注时规则版本已区分；A.4保留历史版本解释。 本轮修改记录与当前源码匹配：tex/appendix_A_guide_R19.tex。
- **判断：** 无需再建冗余版本表，改表达可解决交接式口吻。
- **实际处理：** 将October2改为reader-facing版，说明不替换冻结版本/标签。
- **边界或后续事项：** 不能声称之前编码员使用后来的10月2日文件。

### W40 — 不采纳

- **位置：** tex/appendix_A_guide_R19.tex；line 47: G1--G15 are quick-reference identifiers
- **依据：** G仅用作附录速查ID，R/B.sop跨表已放release。
- **判断：** 现稿已把正文改为方法叙述；去掉附录G编号或强制正文用G反而降低可检索性。
- **实际处理：** 保留附录编号及简短crosswalk说明，未增加操作编号。
- **边界或后续事项：** 不将display ID当成新规范规则版本。

### W41 — 采纳

- **位置：** tex/appendix_A_guide_R19.tex；line 108: Figure~\ref{fig:illustrative-annotations} reproduces
- **依据：** 图注、5个真实样本provenance及源码都指v4.2.10。 本轮修改记录与当前源码匹配：tex/appendix_A_guide_R19.tex。
- **判断：** 冲突是历史图例与当前教学表被统称current decisions，不是已证明标注错误。
- **实际处理：** 改为图4冻结v4.2.10，Tables10–12当前v4.2.14；历史标签/分数不追改。
- **边界或后续事项：** 全集语义版本兼容尚未证明；本轮未重标。

### W42 — 部分采纳

- **位置：** tex/appendix_B_quality_R16.tex；line 6: These calculations use the available later exports
- **依据：** 历史50句重算使用现存较晚导出；原冻结文件对应关系未核实。 本轮修改记录与当前源码匹配：tex/appendix_B_quality_R16.tex。
- **判断：** 可去byte审计措辞，但不能把未核验写成原件不存在。
- **实际处理：** 改为later exports及exact correspondence未核实。
- **边界或后续事项：** 原始冻结文件对应关系仍待证据。

### W43 — 不采纳

- **位置：** tex/appendix_B_quality_R16.tex；line 23: The 15-sentence auditor subset
- **依据：** 该段明示两人见机器建议，1.000属于assisted review，不是blind/corpuswide。
- **判断：** 限定直接随分数出现有必要；另建质量设计表会增篇幅且重复既有图2/数据层表。
- **实际处理：** 保留现有紧凑历史15句段落及必要限定。
- **边界或后续事项：** 不能将1.000作为最终手册独立一致性宣传。

### W44 — 部分采纳

- **位置：** tex/appendix_B_quality_R16.tex；line 51: We have not verified final adjudication
- **依据：** 现存raw QA150两层一致性可重算；final adjudication和训练传播未核实。 本轮修改记录与当前源码匹配：tex/appendix_B_quality_R16.tex。
- **判断：** 主动语态适当，不能据未核实断言仲裁从未发生。
- **实际处理：** 改为作者尚未核实最终仲裁、未追踪传播；系数指原始review层。
- **边界或后续事项：** 逐记录仲裁及进入训练目标的传播证据仍需补。

### W45 — 部分采纳

- **位置：** tex/appendix_B_quality_R16.tex；line 63: We used random sampling to select
- **依据：** 用户确认先熟悉/培训再独立编码；现存导出支持50句membership/sourcecounts。 本轮修改记录与当前源码匹配：tex/appendix_B_quality_R16.tex。
- **判断：** 作者论文不必第三人称说由作者确认；但抽样日志缺口不能用bootstrap替代。
- **实际处理：** 改为主动说明随机抽样与每人编码前培训；保留候选框/日志未随release提供、不可重建draw。
- **边界或后续事项：** 不推断随机抽样发生在培训之后；缺失释放记录不等于从未有记录。

### W46 — 已解决

- **位置：** tex/appendix_C_experiments_R16.tex；line 5: supporting records
- **依据：** supporting records本身已链接到1d1c24e固定提交secondary_review/README.md。
- **判断：** 报告所指无精确入口在当前源码不成立；锚文本概括不代表URL泛化。
- **实际处理：** 保留已有pinned链接及所含per-run/scorer/protocol说明。
- **边界或后续事项：** 本条不等于所有链接内部文件或完整训练均已验证。

### W47 — 部分采纳

- **位置：** tex/review20260923/model_identity.tex；line 3: Model identity and access roles
- **依据：** 现表已有服务ID、teacher/baseline/expansion角色、proxy/provider/local路线及日期说明。
- **判断：** 补齐真实元数据合理；不能为满足表格而用现时服务名伪造底层checkpoint。
- **实际处理：** 保留已具备的身份表、9月10/11日期记录及unknown限定，未编造模型身份。
- **边界或后续事项：** 缺失provider checkpoint/逐call日期字段仍不可由现材料确认。

### W48 — 部分采纳

- **位置：** tex/appendix_C_shared_R16.tex；line 35: These frozen outputs illustrate boundary
- **依据：** 现提供source IDs、offset、中文+英文释义、预测/参考及mismatch计数。 本轮修改记录与当前源码匹配：tex/appendix_C_shared_R16.tex。
- **判断：** 去连续否定说明合理，但无需为两例新建宽表；未裁决身份须保留。
- **实际处理：** 压缩为未单独裁决的边界/类型mismatch，计数只表示span关系。
- **边界或后续事项：** 完整语言错误taxonomy仍未裁决。

### W49 — 部分采纳

- **位置：** tex/expanded_silver_results_20260917.tex；line 23: Differences are calculated before rounding
- **依据：** 0.011来自未舍入计算，展示分数差0.012不应反改真实计算。 本轮修改记录与当前源码匹配：tex/expanded_silver_results_20260917.tex。
- **判断：** 统一舍入注释足够，不必违背全文三位小数偏好增精度或新列。
- **实际处理：** 删除单个算术差异长解释，统一写先计算后舍入。
- **边界或后续事项：** 原始差值和分数未变。

### W50 — 部分采纳

- **位置：** tex/expanded_silver_results_20260917.tex；line 30: The lower expanded JobBERT scores remain unexplained
- **依据：** 扩展训练改变标签、来源、development及输入实施，缺可隔离诊断。 本轮修改记录与当前源码匹配：tex/expanded_silver_results_20260917.tex。
- **判断：** 与W29合并真实研究缺口，压缩待办清单不等于解决下降。
- **实际处理：** 改简短原因未隔离句，明确exploratory。
- **边界或后续事项：** 仍需版本兼容、窗口截断与解码诊断。

### W51 — 部分采纳

- **位置：** tex/appendix_D_reproduction_R16.tex；line 7: Table~\ref{tab:component-access} summarizes
- **依据：** 现已有访问表、REPRODUCIBILITY与PAPER_INDEX。 本轮修改记录与当前源码匹配：tex/appendix_D_reproduction_R16.tex。
- **判断：** 应优先一个现有总入口而非再新增表；保留必要固定档案链接。
- **实际处理：** 删resource naming guide并以component-access表开头，压缩多重导航。
- **边界或后续事项：** W38已在同一访问表补充直接入口；完整expanded训练输入仍未公开。

### W52 — 采纳

- **位置：** tex/appendix_D_reproduction_R16.tex；line 19: \subsection{Resource Access and Sampling Scope}
- **依据：** 表中仍区分locally verified files与public access/可重训范围。 本轮修改记录与当前源码匹配：tex/appendix_D_reproduction_R16.tex。
- **判断：** 重复文件identity/公开/重训三者区别无需连续重述。
- **实际处理：** 删表后重复完整expanded哈希审计段；表及前文split审计保留。
- **边界或后续事项：** 删除文字不代表提供了完整公开expanded训练集。

### W53 — 采纳

- **位置：** tex/appendix_D_reproduction_R16.tex；line 28: The retained records do not resolve whether
- **依据：** 现前句保留主3.2m dump无contenthash、其他dump的143/4919匹配。 本轮修改记录与当前源码匹配：tex/appendix_D_reproduction_R16.tex。
- **判断：** 具体未知来源比every possible不可穷尽命题准确。
- **实际处理：** 结句改为其他dump匹配是否进入实际pretraining未能确定。
- **边界或后续事项：** 完整预训练排除证据仍不足。

### W54 — 待核实

- **位置：** tex/external_benchmarks/paper_appendix.tex；line 5: The native runs contain 3,570
- **依据：** 现稿保留3570/3569、2557/2943及publicsubset含义，未有matched-ID差集。
- **判断：** 原始样本协议差异是实证追溯项，不能靠语言宣布闭合。
- **实际处理：** 本轮未补造ID对照；保留public-subset rerun及未匹配复现限制。
- **边界或后续事项：** 需源版本和记录ID差集才能解释样本差异。

### W55 — 采纳

- **位置：** tex/external_benchmarks/paper_appendix.tex；line 28: versioned experiment records
- **依据：** 训练数量仍104+36；硬件信息在实际协议段保留。 本轮修改记录与当前源码匹配：tex/external_benchmarks/paper_appendix.tex, tex/review20260923/access_matrix.tex。
- **判断：** serverA/B对读者理解科学比较作用有限。
- **实际处理：** 改为common protocol、Chinese adaptation、publicsubset、classification和retrieval，访问表同步命名。
- **边界或后续事项：** 不改变训练运行数或原始服务器台账。

### W56 — 部分采纳

- **位置：** tex/external_benchmarks/paper_A_native.tex；line 4: The recorded DaJobBERT initialization is
- **依据：** 正文现给实际jjzha/dajobbert-base-uncased并链接b84f218b7142c97ab03a60499a9b30e7ec332cab冻结A_NATIVE_RECEIPT.md，其中保留full revision；additional_edits.json记录两处改动。
- **判断：** 用已执行checkpoint身份及任务专属rerun命名解决叙述歧义，不能借此抹除与原cased/weighted设置的差异。
- **实际处理：** 补实际uncased模型名、固定服务器回执链接及RemBERT原始文献；明确task-specific rerun，不称matched reproduction。
- **边界或后续事项：** 未重新训练匹配原论文的cased setting；unweighted指标与英文development选择差异仍限制直接复现比较。

### W57 — 采纳

- **位置：** tex/external_benchmarks/paper_A_native.tex；line 48: Combined English/Danish training improved
- **依据：** 原任务结尾已给组合语言对丹麦的效果与NNOSE各数据集变化。 本轮修改记录与当前源码匹配：tex/external_benchmarks/paper_A_native.tex。
- **判断：** 不必再用broadenmethodcoverage口号及独立中文测试限定结尾。
- **实际处理：** 删泛化重复句，保留任务具体结论。
- **边界或后续事项：** NNOSE单种子in-dataset不能代表全方法跨库收益。

### W58 — 部分采纳

- **位置：** 0main.tex；line 204: These tools were used in September and October 2026
- **依据：** 实际本轮继续Codex润色，工具披露保留；历史imagegen具体模型版本无记录。 本轮修改记录与当前源码匹配：0main.tex。
- **判断：** 披露不能为去AI味删除；日期可按实际使用扩展，不能杜撰版本。
- **实际处理：** 将September更新为September and October，保留范围、责任和未知版本。
- **边界或后续事项：** 历史工具/模型精确版本仍未恢复；不据此识别每句作者。

## 新增方法文献

| 编号 | 引用键 | 用途 |
|---|---|---|
| N01 | `hu2022lora` | Qwen适配所用LoRA方法出处 |
| N02 | `qwen2025report` | Qwen2.5模型系列技术报告 |
| N03 | `chung2021rembert` | Kompetencer比较中的RemBERT方法出处 |

## 未由本次修改解决的证据问题

- **抽样与冻结记录：** 保留实际的三名编码员独立盲编设计；尚需采样框、随机抽样日志及原始冻结文件对应关系。文档缺失不等于该步骤没有执行。

- **数据访问与隐私：** 来源网页和数据集条目不能替代采购授权、可再分发范围、实际批次或隐私检查记录；完整扩展训练输入仍未全部公开。

- **标注版本与仲裁传播：** 已区分图4的冻结v4.2.10标签、当前v4.2.14教学规则及后续读者版；五个例子与规则族检查不能证明全集兼容。逐记录过滤、仲裁以及训练目标传播仍需历史记录。

- **JobBERT下降诊断：** 需分别核查监督版本、窗口截断、解码和预测；本轮没有重新训练或虚构下降原因。

- **外部复现的可比性：** 已修正German ICT任务出处、区分BIO提取与分类任务、明确实际uncased初始化。原论文与公开子集的ID差集及匹配cased设置仍未补做，不能把分数差异解释为完全同条件复现差距。

- **模型与调用溯源：** 保留未记录的精确模型版本和调用字段限制；当前Hub链接不能反推当时执行版本。

- **独立泛化：** Gold150曾用于指南开发；独立50句一致性研究衡量标注者一致性，不自动成为新的模型盲测结果。
