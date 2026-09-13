# Detailed passages and relocation map

These passages preserve the original experimental and provenance details. They were condensed in the manuscript for readability; they remain part of the interpretation and reproduction record. See README.md for a task-oriented guide.

## N001: Resource positioning

Source: `1Introduction.tex`

### Original detail

```tex
Our aim is to supply this combination, rather than to replace other representations of skill demand.
```

### Current manuscript wording

```tex
This combination supports the analysis of competency mentions in Chinese recruitment text.
```

## N002: Experimental questions

Source: `1Introduction.tex`

### Original detail

```tex
These experiments provide complementary evidence about using the resource; the JobBERT comparison concerns the combined supervision-and-selection scheme rather than an isolated teacher or handbook effect.
```

### Current manuscript wording

```tex
These complementary experiments examine Qwen task adaptation and the joint contribution of revised training supervision and development-based selection in JobBERT.
```

## N003: Overview

Source: `1Introduction.tex`

### Original detail

```tex
Its evaluation branch is interpreted according to each protocol's documented reference and provenance restrictions.
```

### Current manuscript wording

```tex
The evaluation branch connects the human reference to the system and student comparisons.
```

## N004: Overview caption

Source: `1Introduction.tex`

### Original detail

```tex
Comparisons retain their protocol-specific reference and provenance restrictions.
```

### Current manuscript wording

```tex
(Consolidated in the other cited sections.)
```

## N005: Abstract: future direction; material development exposure retained in Limitations

Source: `0main.tex`

### Original detail

```tex
Because the human reference was involved in guideline development and has been repeatedly examined, generalization to new recruitment sources requires independent evaluation.
```

### Current manuscript wording

```tex
Future work will extend source and label coverage and evaluate transfer to newly collected recruitment text.
```

## N006: Reference design

Source: `3Experiments.tex`

### Original detail

```tex
The supervision study evaluates students on the frozen 150-sentence human reference set described in \nameref{sec:challenge-audit}, using separate Silver-plus training and development manifests. Reference annotations and original character offsets remain unchanged throughout these comparisons. The reference's handbook-development history and the inherited checkpoint's earlier evaluation lineage limit independent-generalization claims; removing overlapping training identifiers does not remove those histories.
```

### Current manuscript wording

```tex
The supervision study evaluates students on the frozen 150-sentence human reference described in \nameref{sec:challenge-audit}, using separate Silver-plus training and development manifests. Reference annotations and original character offsets are fixed throughout the comparisons. The reference's calibration history is described in Corpus and Annotation and considered in \nameref{sec:limitations}.
```

## N007: Split composition and residual overlap

Source: `3Experiments.tex`

### Original detail

```tex
The primary JobBERT continuation uses 2,156 training and 169 development records. Removing six training records that match three development texts under NFC yields the Qwen training/development split with 2,150/169 records. Both are sentence-level extensions, not document-disjoint splits, and retain repeated training texts: the recorded JobBERT audit counts 1,913 distinct NFC training texts, and the Qwen manifest contains 1,910. NFC is used only to compare texts; the original strings and offsets are scored unchanged. The split audits find no human-reference identifier or complete NFC-normalized sentence in either training or development. The residual JobBERT train/development matches and the reference's development exposure nevertheless remain relevant limitations.
```

### Current manuscript wording

```tex
The primary JobBERT continuation uses 2,156 training and 169 development records. Removing six training records that match three development texts under NFC gives the Qwen split of 2,150/169 records. These sentence-level extensions retain repeated training texts. Neither split contains human-reference identifiers or complete NFC-normalized reference sentences. NFC is used for text comparison; evaluation retains the original strings and offsets. Full manifest and duplicate counts accompany the reproduction notes (\hyperref[app:d]{Appendix D}).
```

## N008: Historical reference inventories

Source: `3Experiments.tex`

### Original detail

```tex
Historical results use an archived 2,601-record SOP+jieba reference associated with the original corpus split of 17,460/2,143/3,237 training/development/test sentences. These counts describe the original corpus partition, not the later student manifests. These historical conditions are distinct from the current results below; \hyperref[app:d]{Appendix D} records their reference identities.
```

### Current manuscript wording

```tex
Historical SOP+jieba evaluations and their original corpus partitions are documented in the companion reproduction materials alongside the current manifest definitions.
```

## N009: Metric interpretation

Source: `3Experiments.tex`

### Original detail

```tex
Relaxed matching measures boundary tolerance rather than independent semantic correctness.
```

### Current manuscript wording

```tex
Relaxed matching quantifies tolerance to boundary differences.
```

## N010: Coverage and invalid outputs

Source: `3Experiments.tex`

### Original detail

```tex
All current inference configurations and student runs retain the complete 150-sentence reference, including empty or malformed outputs. Protocol-specific parsers retain accepted spans from partially rejected responses and assign empty predictions to wholly rejected or malformed responses. The 150 sentences are the coverage count, not the numerical denominator in Eq.~\eqref{eq:micro-prf}. An empty prediction contributes false negatives for any reference spans, whereas an empty--empty sentence adds no span counts. No test-guided boundary snapping is used.
```

### Current manuscript wording

```tex
All configurations are scored on all 150 reference sentences. Partially rejected responses contribute their accepted spans; fully rejected or malformed responses contribute empty predictions. Empty predictions incur false negatives for annotated reference spans, while empty--empty sentences add no span counts. The reproduction notes specify parser decisions and edge cases.
```

## N011: Run variability

Source: `3Experiments.tex`

### Original detail

```tex
Results are displayed as $\bar f\pm s_f$, not as test-set confidence intervals; inference-only results are single runs.
```

### Current manuscript wording

```tex
Results are displayed as $\bar f\pm s_f$ across training seeds; inference-only results are single runs.
```

## N012: Model roles

Source: `3Experiments.tex`

### Original detail

```tex
JobBERT-zh uses a Chinese recruitment-domain-pretrained encoder and a CRF sequence-labeling head. Domain pretraining uses unlabelled recruitment text; the subsequent B1/B2 supervision comparison concerns task-specific continuation, not a newly isolated test of pretraining. Qwen2.5-14B-Instruct is a separate pretrained instruction model, adapted through LoRA in the student experiments; it does not undergo the JobBERT domain-pretraining stage.
```

### Current manuscript wording

```tex
JobBERT-zh combines a Chinese recruitment-domain-pretrained encoder with a CRF sequence-labeling head. Its B1/B2 experiments continue supervised training from a shared checkpoint. Qwen2.5-14B-Instruct uses its pretrained instruction-model weights and is adapted through LoRA.
```

## N013: Historical comparator contracts

Source: `3Experiments.tex`

### Original detail

```tex
Archived SOP-extract-v4 predictions and the earlier Qwen JSON-offset SFT use different instructions or output contracts. They remain separate diagnostics, not matched baselines for the occurrence-based shared-guideline study. Common reference labels alone do not make supervision, initialization, or inference budgets identical.
```

### Current manuscript wording

```tex
The no-adapter Qwen configuration is the comparator for the current occurrence-based LoRA study. Earlier SOP-extract-v4 and JSON-offset experiments are catalogued with their original protocols in the reproduction notes.
```

## N014: RQ1 contribution and comparison scope

Source: `3Experiments.tex`

### Original detail

```tex
Table~\ref{tab:gold150-shared-r7} reports all six inference configurations on the same 150-sentence human reference. Typed exact micro-F1 ranges from 0.3612 for Qwen2.5-14B-Instruct without a project adapter to 0.6667 for the configuration recorded as \texttt{gpt-5.6-terra}; DeepSeek with thinking disabled obtains 0.6469. This ordering is descriptive of the recorded configurations, which share instructions but differ in model access and inference budgets. All scores use the coverage and invalid-output rules specified in the evaluation protocol.
```

### Current manuscript wording

```tex
Table~\ref{tab:gold150-shared-r7} reports six inference configurations on the same 150-sentence reference. Typed exact micro-F1 ranges from 0.3612 for Qwen2.5-14B-Instruct without a project adapter to 0.6667 for the configuration recorded as \texttt{gpt-5.6-terra}; DeepSeek with thinking disabled obtains 0.6469. These results characterize extraction under common instructions and the configuration-specific inference budgets reported below.
```

## N015: Qwen diagnostic findings and parser failures

Source: `3Experiments.tex`

### Original detail

```tex
Figure~\ref{fig:qwen-diagnostics} separates accepted-span recovery from output rejection. Exact recall increases in all three pre-specified gold-length bins for each LoRA seed, although the reference contains only 74 spans of nine or more characters. On the eight empty-reference sentences, accepted false positives occur in two sentences without an adapter and in two, one, and zero sentences for seeds 42, 43, and 44. The baseline's 167 occurrence rejections include 155 unique strings assigned a nonzero occurrence and 12 strings absent from the source; these patterns do not establish a one-based counting mechanism. No rejected candidate is repaired, and these descriptive results do not isolate format adherence from semantic learning.
```

### Current manuscript wording

```tex
Figure~\ref{fig:qwen-diagnostics} shows how the Qwen gains vary by competency type and span length. Each LoRA seed increases exact recall in all three pre-specified length bins. On the eight empty-reference sentences, accepted false-positive spans decrease from 19 without an adapter to 6, 4, and 0 for seeds 42, 43, and 44; the corresponding affected-sentence counts are 2, 2, 1, and 0. The figure and companion reproduction notes retain the type-specific results, sample support, and parser diagnostics.
```

## N016: Human disagreement details

Source: `3Experiments.tex`

### Original detail

```tex
\rev{The historical 50-sentence independent-coding analysis records 21 typing disagreements for Coder B involving job-use tools labeled K rather than the adjudicated S. Coder A's K recall was 0.29, with certificate and algorithm mentions among the K/S disagreements. The analysis also records missed T mentions involving communication, reporting, or research ability. Both coders missed the single L span in the 50-sentence calibration cohort, \zh{英文阅读能力}; this isolated case does not support a general conclusion about language requirements. These examples motivate contextual rules, but they are human-coding observations, not a frequency analysis of student-model errors.}
```

### Current manuscript wording

```tex
\rev{The 50-sentence calibration analysis identified recurring decisions about tool use, knowledge requirements, and transversal competences. Job-use tools and certificate or algorithm mentions prompted K/S disagreements; communication, reporting, and research-ability mentions motivated clearer T guidance. These human-coding observations inform the contextual tests and adjudication procedure in \nameref{sec:annotation-guidelines-r36}. Detailed disagreement counts and rare-label cases are retained in the reproduction notes.}
```

## N017: Synthesis

Source: `3Experiments.tex`

### Original detail

```tex
\rev{The annotation analysis and supervision comparison address different aspects of the resource. Human disagreements show why boundary and contextual-type decisions need explicit rules and adjudication records. The two student comparisons illustrate complementary uses of the resource: adapting Qwen under a fixed inference protocol and comparing JobBERT supervision-and-selection schemes on matched texts. Neither comparison isolates an individual handbook rule or establishes performance on independently collected recruitment data.}
```

### Current manuscript wording

```tex
\rev{The annotation and student-learning analyses illustrate complementary uses of Chinese-SkillSpan. Human coding motivates explicit boundary and contextual-type rules. The student comparisons demonstrate Qwen adaptation under a fixed inference protocol and higher JobBERT agreement under revised supervision and development-based selection.}
```

## N018: Resource use

Source: `3Experiments.tex`

### Original detail

```tex
\rev{Resource users should select an annotation layer and evaluation protocol for their research question. The human reference set supports comparison against a frozen human reference with a documented calibration history; eligible Silver-plus records provide versioned student supervision; earlier snapshots retain their role in historical diagnostics. Multi-source corpus coverage alone does not establish cross-source generalization. Keeping these roles separate makes both improvements and failure cases interpretable without choosing a benchmark version on the basis of its highest model score.}

```

### Current manuscript wording

```tex
\rev{The resource offers a frozen human reference for evaluation, versioned Silver-plus supervision for training, and historical snapshots for tracing earlier experiments. Selecting the appropriate layer and protocol allows users to compare extraction systems, study supervision, and reuse annotation decisions with a clear account of the underlying data.}
```

## N019: Initialization histories

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
JobBERT-zh uses an encoder domain-adapted on unlabelled Chinese job-advertisement sentences, followed by supervised sequence labeling. The continuation experiments reuse the released 3M DAPT encoder and its CRF checkpoint; they do not repeat pretraining for each B1/B2 run. The archived 1M and 3M models differ in their recorded pretraining schedules and extraction checkpoints, so their comparison is not a controlled pretraining-volume ablation. Qwen retains its separate pretrained Instruct weights and receives no recruitment-domain pretraining in this study.
```

### Current manuscript wording

```tex
JobBERT-zh continuation reuses the released 3M domain-adapted encoder and CRF checkpoint. Qwen starts from its pretrained Instruct weights. The historical 1M/3M training schedules and checkpoint lineage are recorded in the reproduction notes.
```

## N020: B1/B2 estimand

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
Earlier supervision (B1) retains SOP labels, whereas revised supervision (B2) combines the revised handbook, teacher annotations, and adjudication. Within the primary v6a configuration, B1 and B2 have matched training texts and matched development texts, but not identical labels. The manifest audit records label differences in 1,440 of the 2,156 training records and 107 of the 169 development records. Thus, the comparison changes both training supervision and the development targets used for selection; it is not a training-label-only intervention or an isolated teacher-model effect. Later handbook maintenance does not retrospectively change these training labels.
```

### Current manuscript wording

```tex
Earlier supervision (B1) uses SOP labels; revised supervision (B2) combines the revised handbook, teacher annotations, and adjudication. In primary v6a, B1 and B2 share training and development texts, with label changes in 1,440 training records and 107 development records. This design compares a joint change in training supervision and the development targets used for checkpoint selection.
```

## N021: JobBERT implementation recovery

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
JobBERT-zh continuation starts from the same published 3M encoder and CRF checkpoint for B1 and B2. Table~\ref{tab:training-settings} summarizes the recorded training settings. Development typed exact F1 selects the checkpoint within each condition; the per-seed selected epochs and development scores accompany the reproduction materials; \hyperref[app:d]{Appendix D} explains their interpretation. A targeted check recovered saved run configurations identifying the shared model directory and \path{crf/best.pt}, but not the executed training/export source or saved tokenizer revision. The retained continuation configurations do not establish the tokenizer revision or the exact token-to-character conversion and long-input handling. Thus, the 256-token setting alone does not establish which source spans were truncated or retained. The original selection history of the inherited CRF remains unavailable. These runs therefore compare supervision-and-selection schemes from a shared starting point, not independently held-out generalization of that checkpoint.
```

### Current manuscript wording

```tex
Both JobBERT conditions start from the same encoder and CRF. Table~\ref{tab:training-settings} summarizes their recorded settings, and development typed exact F1 selects each checkpoint. The reproduction notes contain per-seed selection records, implementation-recovery details, and the inherited checkpoint's unresolved selection history (\hyperref[app:d]{Appendix D}).
```

## N022: Qwen training

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
The matched Qwen study fits a fresh LoRA adapter for each of seeds 42, 43, and 44 on the 2,150/169 B2 manifest. Training retains the frozen system instruction, user template, and five schematic examples; targets are literal span text, occurrence index, and type. Loss applies only to the assistant JSON and closing turn token. The LoRA and optimization settings are listed in Table~\ref{tab:training-settings}; Qwen training uses BF16. Development typed exact F1 selects the adapter; the human reference is not used for selection. Per-seed selection records accompany the reproduction materials; \hyperref[app:d]{Appendix D} retains the remaining training settings.
```

### Current manuscript wording

```tex
The Qwen study fits a fresh LoRA adapter for each of seeds 42, 43, and 44 on the 2,150/169 B2 manifest. Training uses the frozen system instruction, user template, and five schematic examples, with literal span text, occurrence index, and type as targets. Loss applies to the assistant JSON and closing turn token. Table~\ref{tab:training-settings} reports the settings; training uses BF16. Development exact F1 selects each adapter, with the human reference reserved for evaluation.
```

## N023: Training table caption

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
Both select checkpoints by development typed exact F1. The JobBERT input-length setting does not resolve the tokenizer and truncation limitations described above.
```

### Current manuscript wording

```tex
Both select checkpoints by development typed exact F1; implementation and selection records accompany the reproduction notes.
```

## N024: Inference settings

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
All shared-guideline systems receive the same frozen system instruction and user template, with one sentence's ID and text per request. The prompt is \texttt{rev2 patch1}, not the later V4.2.14 handbook; it includes five fixed schematic examples and contains no per-sentence reference labels. Local parser v1.1 converts the occurrence-based output to character spans outside the model context. Qwen inference uses the same base checkpoint, parser, prompts, BF16, deterministic decoding, and 2,048-token generation cap with or without the adapter. Shared guidelines do not imply matched reasoning budgets: DeepSeek-V4-Pro is evaluated in non-thinking and thinking modes, with configured output caps of 2,048 and 8,192 tokens respectively. Model identities and the other recorded inference settings are documented in \hyperref[app:c]{Appendices C}--\hyperref[app:d]{D}.
```

### Current manuscript wording

```tex
All systems receive the frozen \texttt{rev2 patch1} instruction and user template, with one sentence's ID and text per request and five fixed schematic examples. Local parser v1.1 resolves occurrence-based output to character spans. Qwen baseline and adapter inference share the checkpoint, prompts, parser, BF16, deterministic decoding, and 2,048-token output cap. DeepSeek-V4-Pro uses non-thinking and thinking modes with output caps of 2,048 and 8,192 tokens, respectively. \hyperref[app:c]{Appendix C} summarizes the configurations; the reproduction notes record model-access metadata and full settings.
```

## N025: Supplementary setup

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
Earlier JSON-offset, training-source, demonstration, and cleaning analyses retain their own settings in the companion reproduction materials. The training-source comparison initializes a new task head and CRF; these supplementary conditions do not replace the designated continuation result.

```

### Current manuscript wording

```tex
Training-source, JSON-offset, demonstration, and cleaning studies are retained with their original settings and results in the companion reproduction materials.
```

## N026: Student comparison roles

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
Their different initialization and learning conditions preclude a matched architecture ranking.
```

### Current manuscript wording

```tex
The two panels address adaptation and supervision-and-selection, respectively.
```

## N027: Student caption variability

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
SD is run variation, not a test confidence interval.
```

### Current manuscript wording

```tex
(Consolidated in the other cited sections.)
```

## N028: Student table scope

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
The inherited checkpoint history and residual train/development text matches limit interpretation.
```

### Current manuscript wording

```tex
The split and checkpoint limitations are summarized in \nameref{sec:limitations}.
```

## N029: Qwen adaptation result

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
Under the same base checkpoint, frozen messages, occurrence-based schema, parser, and decoding settings, all three B2-trained LoRA adapters improve over the no-adapter Qwen baseline. Typed exact micro-F1 increases from 0.3612 to 0.5403 $\pm$ 0.0354 across seeds 42, 43, and 44 (Table~\ref{tab:gold150-main}, panel A). Exact precision and recall both increase in each run. Partially rejected responses become less frequent in all three runs, although improved output validity alone does not establish semantic accuracy. This comparison demonstrates task adaptation using the supplied B2 supervision; it contains no B1 fine-tuning condition.
```

### Current manuscript wording

```tex
All three B2-trained LoRA adapters improve over the no-adapter Qwen baseline under the fixed inference protocol. Typed exact micro-F1 rises from 0.3612 to 0.5403 $\pm$ 0.0354 across seeds 42, 43, and 44 (Table~\ref{tab:gold150-main}, panel A). Exact precision and recall both increase in every run. These results demonstrate task adaptation using the supplied Silver-plus supervision; detailed output-validity diagnostics accompany the reproduction materials.
```

## N030: JobBERT result

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
The JobBERT-zh comparison evaluates two supervision-and-selection schemes from a shared encoder and CRF checkpoint. B1 and B2 use the same training and development texts within the primary configuration, but their labels differ in 1,440 training records and 107 development records. Typed exact micro-F1 is 0.1422 $\pm$ 0.0138 under B1 and 0.5536 $\pm$ 0.0054 under B2 (Table~\ref{tab:gold150-main}, panel B). The result therefore concerns the combined change in training supervision and development-based selection, not an isolated effect of label quality, teacher identity, or an individual rule. The inherited checkpoint history and residual training–development text matches remain limitations of this comparison. Training-pool variants are retained as supplementary diagnostics rather than a controlled sample-size ablation.
```

### Current manuscript wording

```tex
JobBERT-zh reaches typed exact micro-F1 of 0.5536 $\pm$ 0.0054 under B2, compared with 0.1422 $\pm$ 0.0138 under B1 (Table~\ref{tab:gold150-main}, panel B). Starting from the same encoder and CRF on matched texts, the revised training labels and development-based selection yield higher agreement with the human reference. Per-seed results and training-pool variants are retained in the companion reproduction materials.
```

## N031: Supplementary analyses

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
Supplementary analyses examine earlier JSON-offset generation, demonstration selection, training-source composition, training-pool extensions, and crawler-tail cleaning. They retain their original data and selection conditions and are not substitutes for the current matched comparisons. Complete results, including unfavorable changes and their original settings, are retained in the companion reproduction materials.
\FloatBarrier

```

### Current manuscript wording

```tex
The companion reproduction materials report JSON-offset generation, demonstration selection, training-source composition, pool extensions, and crawler-tail cleaning, together with their original settings, complete results, and practical reproduction notes.
```

## N032: System table scope

Source: `tex/stage2_shared_main.tex`

### Original detail

```tex
Scores describe the recorded inference configurations; inference budgets differ, and no test of intersystem differences is reported.
```

### Current manuscript wording

```tex
Inference budgets are configuration-specific.
```

## N033: Model provenance

Source: `tex/stage2_shared_main.tex`

### Original detail

```tex
The GPT name is returned metadata from proxy access, not independent verification of provider routing.
```

### Current manuscript wording

```tex
The GPT name follows proxy-returned metadata.
```

## N034: Consolidated material limitations and contribution-focused conclusion

Source: `6Conclusion.tex`

### Original detail

```tex
\section{Limitations and Responsible Use}
\label{sec:limitations}

% [R13] Condensed to the four comparator limitation passages' mean character length.
% Detailed Qwen/HEM/P1/cleaning qualifications remain in the existing supplementary sections.
\rev{Chinese-SkillSpan has limited source and label coverage. Rare labels constrain per-type conclusions. The human reference set is not a representative random sample: it includes handbook-calibration data and has been repeatedly examined. Machine-assisted review may anchor annotators and cannot replace independent agreement assessment.}

% [R42] Distinguish the matched Qwen adaptation contrast from bundled B1/B2 changes.
\rev{JobBERT's inherited CRF has an undocumented selection history. Sentence-level isolation and residual JobBERT training/development matches limit independent generalization claims. B1/B2 changes both training and development labels. Qwen's matched LoRA study uses B2 only, so it does not isolate teacher or handbook effects. Proxy-returned model names do not independently verify provider routing. Detailed protocol qualifications accompany the supplementary analyses.}

\rev{The resource supports competency extraction, not applicant ranking or individual-ability inference. Deployment requires external validation, human oversight, source permissions, and privacy safeguards.}

\section{Conclusion}
\label{sec:conclusion}

% [Stage2] Resource, guidelines, and two complementary student uses.
\rev{Chinese-SkillSpan combines a multi-source Chinese recruitment corpus, operational LSKT annotation guidelines, and evaluation protocols with explicitly separated human-reference and teacher-supervision layers. The resource makes decisions about complete boundaries, coordinated expressions, and contextual types available for inspection and reuse.}

\rev{The experiments demonstrate two uses of the supplied supervision. Qwen adaptation improves extraction under a fixed inference contract, while the matched-text JobBERT comparison yields higher agreement with the human reference under revised training and development labels. These findings support student learning under the documented conventions, not isolated teacher or rule effects. The reference's development history, rare-type support, and model-provenance limitations constrain broader generalization claims.}

```

### Current manuscript wording

```tex
\section{Limitations and Responsible Use}
\label{sec:limitations}

Chinese-SkillSpan covers four recruitment collections with uneven label frequencies, including only two L spans in the human reference. The reference is a selected calibration/challenge sample used in guideline development and repeatedly examined; independent evaluation on new sources is needed to assess transfer. Machine-prefilled review is reported separately from independent human coding.

The student studies evaluate Qwen adaptation with B2 supervision and a joint B1/B2 change in JobBERT training and development labels. Sentence-level splits, residual JobBERT training/development text matches, and the inherited CRF's undocumented selection history limit independent-generalization claims. These studies do not isolate individual teacher or handbook effects. Recorded inference configurations have different budgets, and proxy-reported model identities remain unverified. Detailed failure analyses and reproducibility gaps are documented in the companion reproduction notes (\hyperref[app:d]{Appendix D}).

The resource supports competency extraction from advertisements. Applications require external validation, human oversight, source permissions, and privacy safeguards; the annotations do not measure individual applicants' abilities.

\section{Conclusion}
\label{sec:conclusion}

Chinese-SkillSpan brings together multi-source Chinese recruitment text, operational LSKT annotation guidelines, and versioned evaluation protocols. Its human-reference and Silver-plus layers support complementary uses in system evaluation and student training. The handbook makes decisions about complete boundaries, coordinated expressions, and contextual typing available for inspection and reuse.

The experiments demonstrate student learning from the supplied supervision. Qwen LoRA improves precision, recall, and exact F1 under a fixed inference protocol, while JobBERT achieves higher reference agreement with revised training and development labels. Together, the data, guidelines, companion models, and evaluation materials provide a foundation for further research on competency extraction from Chinese recruitment text.

```

## N035: Annotation-layer roles

Source: `tex/silver_plus_methods.tex`

### Original detail

```tex
Conflict origin describes sampling history, not independently rated difficulty. Human review does not promote Silver-plus records into the evaluation reference.
```

### Current manuscript wording

```tex
Conflict origin records the sampling history; reviewed Silver-plus records retain their supervision role.
```

## N036: Collection and selection provenance

Source: `tex/silver_plus_methods.tex`

### Original detail

```tex
The 2,601-record lineage combines the 980-record model-disagreement queue with 1,621 SOP--CWS records; it is not established as a random subset of the original 3,237 test sentences. The calibration sample was drawn from the conflict queue with recorded seed 20260902. Collection names alone do not establish the original platforms, collection dates, inclusion criteria, or occupational representativeness. The retained materials also do not fully recover sentence segmentation and deduplication rules, the conflict-admission criterion, the challenge-selection procedure, or coder qualifications. These source and selection details remain to be reconciled with the original collection and annotation records. The 22,840-sentence layer contains corpus-scale model annotations and is not a current human-gold training set.
```

### Current manuscript wording

```tex
The study lineage combines the 980-record model-disagreement queue with 1,621 SOP--CWS records. Calibration sampling used seed 20260902. This selected lineage supports targeted annotation and supervision studies within the larger corpus; collection and selection provenance is documented in the reproduction notes. The corpus-scale model annotations and the adjudicated human reference are separately identified.
```

## N037: Empty-label proportions

Source: `tex/silver_plus_methods.tex`

### Original detail

```tex
These proportions characterize differently sampled annotation layers and are not evidence of their relative annotation quality.
```

### Current manuscript wording

```tex
They reflect the different sampling compositions of the supervision and reference layers.
```

## N038: Supervision composition inventories

Source: `tex/silver_plus_methods.tex`

### Original detail

```tex
The available Qwen manifest records sampling origin: A100/H730/E1621 contribute 96/637/1,417 training records and 4/53/112 development records. Training spans comprise 2,218 S, 641 K, 763 T, and 24 L; development spans comprise 207 S, 61 K, 77 T, and no L. These origins are review/conflict-queue categories, not a recovered AI/Cloud/public-sector/graduate source distribution. The original four-source corpus split therefore cannot substitute for the current reference or supervision-source composition.
```

### Current manuscript wording

```tex
The Qwen manifest records sampling origin and LSKT support separately for training and development. Detailed A100/H730/E1621 counts and type distributions accompany the reproduction materials; these origin groups describe annotation history.
```

## N039: Descriptive distributions

Source: `tex/silver_plus_methods.tex`

### Original detail

```tex
These distributions describe different annotation layers and sample compositions; they do not measure annotation quality or model performance.
```

### Current manuscript wording

```tex
The distributions characterize the inputs and annotation lengths encountered in each layer.
```

## N040: Workflow roles

Source: `2Framework.tex`

### Original detail

```tex
A model suggestion is not an independent human annotation.
```

### Current manuscript wording

```tex
(Consolidated in the other cited sections.)
```

## N041: Teacher generation and admission history

Source: `2Framework.tex`

### Original detail

```tex
Silver-plus generation used Handbook B and a versioned extraction prompt, with the teacher recorded as \texttt{gpt-6-astra}. An initial sampled review preceded bulk generation. Substring validity, character offsets, label membership, and record coverage were checked, alongside review and adjudication of annotation decisions. These structural checks do not establish semantic correctness. The historical 82-record queue records cases requiring adjudication, not a permanent exclusion set. Later records distinguish resolved labels, confirmed-empty examples, and still-undetermined cases; actual admission follows each experiment's manifest (\hyperref[app:d]{Appendix D}).
```

### Current manuscript wording

```tex
Silver-plus generation used Handbook B and a versioned extraction prompt, with the teacher recorded as \texttt{gpt-6-astra}. An initial sampled review preceded bulk generation. Structural validation checked substrings, offsets, types, and record coverage; human review and adjudication addressed annotation decisions. Each experiment's manifest records the admitted supervision subset, with review and admission histories retained in the reproduction notes.
```

## N042: Handbook maintenance chronology

Source: `2Framework.tex`

### Original detail

```tex
Generation and later guideline maintenance retain separate version identities. The initial teacher-label review cohort used an earlier frozen prompt and retained its later adjudication record. The remaining 2,351 records used the frozen prompt based on Handbook B V4.2.12. Subsequent V4.2.13--V4.2.14 amendments did not regenerate or retrospectively relabel these records; \hyperref[app:a]{Appendix A} explains these version boundaries, with the complete execution map in the companion reproduction materials. The next subsection reports independent-coding and machine-review evidence separately.
```

### Current manuscript wording

```tex
The remaining 2,351 teacher records used the frozen V4.2.12-based prompt. Later V4.2.13--V4.2.14 handbook amendments are versioned separately, preserving the labels and protocols of completed experiments. \hyperref[app:a]{Appendix A} presents the current guide, and the reproduction materials provide its execution-version map.
```

## N043: Coder export provenance: retained in table and Appendix B

Source: `tex/annotation_quality_R12.tex`

### Original detail

```tex
These later exports do not establish byte identity with the original pre-adjudication freeze.
```

### Current manuscript wording

```tex
(Consolidated in the other cited sections.)
```

## N044: Review design

Source: `tex/annotation_quality_R12.tex`

### Original detail

```tex
These review comparisons are not independent inter-coder reliability estimates or a common pre--post reliability study.
```

### Current manuscript wording

```tex
Their machine-prefilled review design is distinguished from independent human coding in the table.
```

## N045: Quality caption

Source: `tex/annotation_quality_R12.tex`

### Original detail

```tex
These are annotation comparisons, not model-test scores.
```

### Current manuscript wording

```tex
(Consolidated in the other cited sections.)
```

## N046: Agreement interpretation

Source: `tex/annotation_quality_R12.tex`

### Original detail

```tex
Later machine-assisted review cannot replace independent coding because the samples, guidelines, and exposure to suggestions differ.
```

### Current manuscript wording

```tex
The independent-coding and machine-review designs are interpreted separately.
```

## N047: Coder provenance details

Source: `tex/annotation_quality_R12.tex`

### Original detail

```tex
, including the unresolved author-reported earlier independent 15-sentence exercise
```

### Current manuscript wording

```tex
.
```

## N048: Appendix C scope

Source: `tex/appendix_C_experiments_R16.tex`

### Original detail

```tex
Earlier JSON-offset generation, training-pool and source-composition comparisons, and instruction, demonstration and cleaning sensitivities are retained in the companion reproduction materials, including unfavorable outcomes. Their data, initialization and selection conditions differ from the current matched comparisons; they do not establish isolated sample-size, source-composition or cleaning effects. This appendix retains the current shared-guideline protocol, per-seed Qwen results and frozen-prediction diagnostics.
```

### Current manuscript wording

```tex
This appendix reports the current shared-guideline configurations, per-seed Qwen results, and frozen-prediction diagnostics. Historical JSON-offset, training-source, demonstration, and cleaning experiments are collected with their complete outcomes in the companion reproduction materials.
```

## N049: Prompt and reference provenance

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
The shared-guideline protocol \texttt{rev2 patch1} evaluates all six inference configurations on the complete frozen human reference set. Reference metadata remain \texttt{B.sop\_v4.2.10}; the protocol adapts general rules from the V4.2.12-based teacher prompt, not later V4.2.14 relabeling. Its five fixed schematic examples do not match or occur in full within human-reference sentences under exact/NFC checks, but that does not establish independent example selection. The reference's handbook-development and observation history remains relevant.
```

### Current manuscript wording

```tex
The shared-guideline protocol \texttt{rev2 patch1} evaluates six configurations on the complete human reference. It uses the frozen \texttt{B.sop\_v4.2.10} reference with general instructions adapted from the V4.2.12-based teacher prompt and five schematic examples. The version map and example-selection checks are retained in the reproduction notes.
```

## N050: Output protocol

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
Models return an ID and spans as literal \texttt{text}, zero-based \texttt{occurrence}, and L/K/S/T \texttt{type}. Local parser v1.1 resolves these to Unicode offsets; it is not part of model context. Evaluation uses character-BIO representations with the span-level exact/relaxed scorer \texttt{cnss-lskt-1.2.0}. Unlike the archived SOP inputs, all supplied input texts match the frozen human reference set. Prompt, schema, and request granularity also differ, so this is not a prompt-only comparison.
```

### Current manuscript wording

```tex
Models return an ID and spans as literal \texttt{text}, zero-based \texttt{occurrence}, and L/K/S/T \texttt{type}. Local parser v1.1 resolves spans to Unicode offsets for exact and relaxed scoring with \texttt{cnss-lskt-1.2.0}. All supplied input texts match the frozen reference.
```

## N051: Model settings and access metadata

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
Qwen2.5-14B-Instruct is evaluated locally without a project adapter, using deterministic decoding; it is not the Qwen Base variant, and identity to the historical weights is not established. Kimi disables thinking but its endpoint requires temperature 0.6. Both DeepSeek configurations use DeepSeek-V4-Pro (API model \texttt{deepseek-v4-pro}). The non-thinking condition disables thinking and sets \texttt{max\_tokens}=2,048; the thinking condition enables thinking and sets \texttt{max\_tokens}=8,192. These are inference settings, not distinct model names; 8,192 is the configured output cap, not a separately verified count of reasoning tokens. GPT/Claude have no reported equivalent switch. Common instructions therefore do not imply equal computation budgets.
```

### Current manuscript wording

```tex
Qwen2.5-14B-Instruct runs locally with deterministic decoding. Kimi uses non-thinking mode and temperature 0.6. DeepSeek-V4-Pro (API model \texttt{deepseek-v4-pro}) uses non-thinking and thinking modes with configured output caps of 2,048 and 8,192 tokens. GPT and Claude are accessed through a proxy, while Kimi and DeepSeek use provider endpoints. Configuration and access metadata accompany the reproduction notes.
```

## N052: Provider identity verification

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
GPT and Claude were accessed through a proxy, whereas Kimi and DeepSeek used their provider endpoints. GPT responses identify the model as \texttt{gpt-5.6-terra}; this does not independently verify the underlying checkpoint or routing, or establish the identity of historical SOP outputs.
```

### Current manuscript wording

```tex
The reproduction notes document provider-access metadata, archived outputs, and the scope of score reproduction for these configurations.
```

## N053: Parser failure taxonomy

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
The parser rejects invalid IDs/JSON, nonliteral or empty substrings, invalid occurrence indices/types, and candidates using offset fields. After sorting by start and original output order, it removes duplicates and rejects later conflicting or overlapping spans. Accepted spans from partial responses remain in scoring; fully rejected and malformed responses count as empty predictions. Detailed output-status counts are retained in the companion reproduction materials. Structural validity alone does not establish semantic correctness.
```

### Current manuscript wording

```tex
The parser validates response structure, literal substrings, occurrences, labels, and span compatibility. Accepted spans are scored under the coverage rules in Evaluation Metrics; detailed rejection rules and output-status counts accompany the reproduction materials.
```

## N054: Rescoring versus rerunning

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
Offline rescoring reproduces the exact and relaxed scores for all six inference configurations and all three Qwen LoRA runs. Actual outbound requests were not archived, and model-weight files were not included in the audit package; this verification therefore establishes score reproducibility, not independent verification of provider routing or checkpoint identity.
```

### Current manuscript wording

```tex
Offline rescoring reproduces the exact and relaxed results for all six inference configurations and all three Qwen LoRA runs. The reproduction notes distinguish the available scoring artifacts from the requirements for rerunning model inference.
```

## N055: DeepSeek precision-recall pattern

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
DeepSeek-V4-Pro in thinking mode has higher precision but lower recall than in non-thinking mode; aggregate scores do not isolate the contribution of output-format failures from other errors. Common task instructions do not make these reasoning and output budgets a controlled single-factor contrast.
```

### Current manuscript wording

```tex
DeepSeek-V4-Pro in thinking mode shows higher precision and lower recall than the non-thinking configuration under their respective output budgets.
```

## N056: Qwen design stated in heading and condition table

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
This study has no B1 fine-tuning condition.
```

### Current manuscript wording

```tex
(Consolidated in the other cited sections.)
```

## N057: Baseline prediction reuse

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
The no-adapter prediction is reused, not regenerated.
```

### Current manuscript wording

```tex
The same no-adapter prediction is used throughout.
```

## N058: Seed summaries

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
(mean $\pm$ sample SD across three seeds, not a test confidence interval).
```

### Current manuscript wording

```tex
(mean $\pm$ sample SD across three seeds).
```

## N059: Author-selected passage: contribution instead of repeated exclusions

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
All three adapters improve exact F1 over the no-adapter checkpoint. The contrast supports fine-tuning on the supplied B2 supervision under a fixed inference protocol; it does not separate handbook, teacher, or adjudication effects. The earlier JSON-offset score and historical SOP scores use different contracts and must not be substituted for the no-adapter baseline. Likewise, the JobBERT continuation is a different supervision-and-selection comparison, not a matched architecture ranking.

```

### Current manuscript wording

```tex
All three B2-trained adapters improve exact F1 over the no-adapter checkpoint. With the base model and inference protocol held fixed, the results demonstrate Qwen task adaptation using the supplied Silver-plus supervision. The separate JobBERT study examines revised supervision and development-based selection on matched texts.
```

## N060: Diagnostic sampling unit

Source: `tex/qwen_diagnostics_round2.tex`

### Original detail

```tex
Seeds remain separate runs on the same test set, not 450 independent observations.
```

### Current manuscript wording

```tex
Each seed is evaluated separately on the same test set.
```

## N061: Diagnostic caption

Source: `tex/qwen_diagnostics_round2.tex`

### Original detail

```tex
The three seeds share the test set; no significance claim is made.
```

### Current manuscript wording

```tex
Each run is shown separately on the shared test set.
```

## N062: Diagnostic edge cases

Source: `tex/qwen_diagnostics_round2.tex`

### Original detail

```tex
L has only two gold spans: the no-adapter run recovers 0/2 and each LoRA run 2/2, with one extra L prediction in every run. On the eight empty-reference sentences, legal empty outputs occur in 6/8, 6/8, 7/8 and 8/8 sentences in the plotted run order; none has a format failure or all-spans-rejected outcome. Full TP/FP/FN, precision/recall/F1, and parser-rejection counts accompany the reproduction materials. Accepted-span errors and output rejection are distinct; exact--relaxed differences are not a pure boundary-error rate.
```

### Current manuscript wording

```tex
L has two gold spans: the no-adapter run recovers 0/2 and each LoRA run 2/2, with one extra L prediction in every run. Legal empty outputs occur in 6/8, 6/8, 7/8, and 8/8 sentences in the plotted order. Complete TP/FP/FN, precision/recall/F1, and parser-rejection diagnostics are retained in the reproduction materials.
```

## N063: Guide-version audit trail

Source: `tex/appendix_A_guide_R19.tex`

### Original detail

```tex
Version differences concern more than wording. The historical rule log distinguishes type conventions (for example, language certificates versus occupational tool use), scope eligibility, and boundary construction. V4.2.13 separates confirmed-empty, unresolved, and training-admission states; an empty label array alone does not certify a negative example. V4.2.14 rule R23 changes the boundary guidance for shared-experience coordination: in case \texttt{1838-s0008}, the earlier S span $[9,25)$ becomes $[9,16)$ and $[17,19)$, while $[26,37)$ remains S. This is a boundary change, not merely a wording update. These documented cases do not constitute a full compatibility audit of the frozen reference or Silver-plus against V4.2.14; no such universal compatibility is claimed.
```

### Current manuscript wording

```tex
The reproduction notes record version-specific changes to type conventions, scope eligibility, admission states, and shared-experience boundaries. They include the original and revised spans for case \texttt{1838-s0008}, complementing the worked example in A.3.
```

## N064: Frozen-reference execution details

Source: `tex/appendix_A_guide_R19.tex`

### Original detail

```tex
For current evaluation, pair \path{gold150_test.jsonl} with the shared \texttt{rev2 patch1} system instruction and user template, the occurrence schema and parser v1.1, and scorer \texttt{cnss-lskt-1.2.0}. The local evaluation-entry inventory records the actual file hashes and remaining scorer binding gap (\hyperref[app:d]{Appendix D}). Case \texttt{1838-s0008} is present in the teacher layer but absent from all 150 reference records by both identifier and exact text. This targeted R23 check does not establish full semantic compatibility of later rules with every frozen annotation.

```

### Current manuscript wording

```tex
For current evaluation, use \path{gold150_test.jsonl}, the shared \texttt{rev2 patch1} instruction and template, the occurrence schema and parser v1.1, and scorer \texttt{cnss-lskt-1.2.0}. File identities and compatibility checks are documented in the companion reproduction notes (\hyperref[app:d]{Appendix D}).
```

## N065: Review-layer versions

Source: `tex/appendix_B_quality_R16.tex`

### Original detail

```tex
The pre-generation A100 cohort has a historical 419-span supervision layer and a later 432-span reviewed layer. These are different versions; the later layer does not replace labels used in completed student runs.
```

### Current manuscript wording

```tex
The pre-generation A100 review and the later QA100 review retain separate versioned annotation layers; their exact counts and chronology are documented in the reproduction notes.
```

## N066: Unverified earlier independent exercise

Source: `tex/appendix_B_quality_R16.tex`

### Original detail

```tex
The authors report a 15-sentence independent raw-text exercise within the pre-generation 100, before machine-prefilled review and bulk generation. Neither coder saw machine predictions or the other coder's spans, and they did not discuss the exercise before completing it. This is an author-reported design, not a verified independent agreement estimate.
```

### Current manuscript wording

```tex
The authors also report an earlier independent 15-sentence exercise within A100. Its original exports have not been reconciled with the archived machine-prefilled Dual15 subset, so no independent-agreement coefficient is assigned to that exercise.
```

## N067: Dual15 provenance and nesting

Source: `tex/appendix_B_quality_R16.tex`

### Original detail

```tex
The archived Dual15 files describe a machine-prefilled subset of the post-generation 100-sentence sample. Their comparison layers each contain the same 27 spans. This archive does not establish the author-reported chronology of an independent 15-sentence exercise within the pre-generation 100: the original independent exports, sample mapping, and metric definition for that exercise have not been reconciled with these files. No independent-agreement coefficient is assigned to that exercise here. Subsequent cross-library adjudications are retained separately rather than silently changing those agreement files. The union of the human reference set and the two teacher-label review samples contains 350 sentences with no shared identifiers or complete NFC-normalized texts between those three cohorts; neither nested 15-sentence description increases that union. These checks do not replace experiment-specific admission checks, and the contrast between initial independent coding and later machine-assisted review is not a matched pre/post reliability study.
```

### Current manuscript wording

```tex
The archived Dual15 subset belongs to QA100 and contains 27 identical spans in each machine-prefilled comparison layer. The human reference and the two teacher-review cohorts comprise 350 distinct sentences; the nested subset adds no new sentences. Full comparison-layer provenance, file limitations, and chronology are retained in the reproduction notes.
```

## N068: Detailed experimental inventory moved to reproduction notes

Source: `tex/appendix_D_reproduction_R16.tex`

### Original detail

```tex
% [R16-D] Reader-facing access index; detailed source histories retained, not discarded.
\section{Appendix D. Reproduction and Versioned Materials}
\phantomsection
\label{app:d}
\label{sec:extension-provenance}
\label{sec:display-archive-r14}
% [R38-REPRO] Public main-branch archive pointer; version checksums are maintained in repository documentation.
The public repository's \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/REPRODUCIBILITY.md}{reproduction guide} provides file inventories, checksums, and scoring instructions. Historical analyses retain their original evaluation conditions. Public availability follows the release inventory; not every archived experiment artifact is publicly released.

The manuscript source package retains the full English handbook, its execution-version map, and the frozen teacher prompt. Detailed file mappings and execution records accompany the reproduction materials; this appendix retains the experimental distinctions needed to interpret the results. The human reference set and Silver-plus B2 training/development files are included in Zenodo v0.1.3, but not in v0.1.1 or v0.1.2.

% [R37-MOVE] Historical identities and superseded plans formerly repeated in the corpus chapter.
\paragraph{Historical references.}
The archived SOP+jieba reference contains 2,601 identifier-aligned records: 980 from the three-model disagreement queue and 1,621 SOP--CWS records. The same identifiers occur in Gold v2, the historical Handbook A reference. Both label sets remain distinct from the current human reference and Silver-plus allocation (\nameref{sec:challenge-audit}). The earlier 200-sentence mixed-annotator analysis and historical length-distribution plots concern different samples; neither describes the current human reference set.

\paragraph{Version identification and access.}
The audit protocol records each benchmark version's manifest, file checksums, schema, guidelines, and scorer identity. Results from different annotation conventions retain separate version identities. Public availability is specified in Data Availability rather than inferred from the existence of a local artifact.

% [R39-MOVE] Earlier DOIs and contrast-model details relocated from Data Availability.
\begin{sloppypar}
Earlier snapshots are available at \url{https://doi.org/10.5281/zenodo.22685143} (v0.1.2) and \url{https://doi.org/10.5281/zenodo.22288338} (v0.1.1); the all-version concept DOI is \url{https://doi.org/10.5281/zenodo.22288337}. Later portable scoring tools and terminology mappings are on GitHub's default branch, not in the immutable v0.1.3 archive.

The public contrast-model repositories are \url{https://huggingface.co/AlfredJames/jobbert-zh-1m} for the 1M DAPT condition and \url{https://huggingface.co/AlfredJames/jobbert-zh-v6a} for the human-reference B2 continuation. The 3M DAPT initialization checkpoint at \url{https://huggingface.co/AlfredJames/jobbert-zh} includes the historical V4 CRF. The v6a repository corresponds to the current human-reference B2 continuation, while the 1M repository is a historical DAPT contrast. Loading the default v6a seed-42 checkpoint does not reproduce a three-seed mean.

\end{sloppypar}

\paragraph{Training-manifest interpretation.}
% [R41-MOVE] Version chronology relocated from Evaluation Protocol; historical identities unchanged.
The earlier v3 configuration contains 1,382 training and 169 development records under document isolation. The v4 sentence-level extension admits checked different sentences from shared documents, increasing training to 1,913; v5 adds repeated records to reach 2,200. These stages change sample composition as well as size.
The primary v6a result uses 2,156/169 training/development records after removing 44 training copies of development sentences from v5. Its audit still identifies six training records matching three development texts under NFC; removing those gives the Qwen \texttt{v6a\_nocross} manifest, 2,150/169. Both are sentence-level extensions, not document isolation. The separate cleaning study uses 2,138/168 and does not overwrite either designated manifest.

The historical 82-record adjudication queue must not be read as 82 permanently excluded records. The later Silver-plus registry classifies these as 53 resolved, three confirmed empty, and 26 still undetermined. The actual Qwen manifest admits 51 resolved and three confirmed-empty records to training and one resolved record to development; it admits none of the 26 still-undetermined cases. Thus, a historical queue, a later admission pool, and a training split are different objects. These membership counts describe Qwen's manifest, not a replacement JobBERT manifest.

% [R41-NEW] CHECK_B1B2_OVERLAP_SELECTION.json, cross-checked with per-run histories/configurations.
The audit records 1,913 distinct NFC training texts in v6a and 1,910 in \texttt{v6a\_nocross}. For v6a, B1 and B2 have identical IDs and NFC-normalized texts within each split, with label differences in 1,440 training records and 107 development records. Each condition uses its own development labels for checkpoint selection. The companion reproduction materials record the per-seed selected epochs and development scores; these development scores must not be read as test results or compared as if they used identical target labels.



The inherited JobBERT CRF's original selection history remains unresolved. The training-source comparison uses a fresh head, and Qwen selection differs between the earlier and shared-guideline runs; these distinctions remain attached to the corresponding results.

% [R42] A TRAIN_CONFIG / DATA_MANIFEST / PROMPT_MANIFEST / selection records.
\paragraph{Shared-guideline Qwen training and provenance.}
Qwen training preserves the 2,150/169 B2 records through lossless conversion from BIO spans to occurrence-based JSON, without resampling or label regeneration. Training uses AdamW, a linear learning-rate schedule, no warmup or weight decay, and gradient checkpointing on NVIDIA A100 80GB hardware. No sequence exceeds the 8,192-token training limit. Checkpoints are selected on development exact F1, preferring the earlier epoch when the difference is at most $10^{-4}$ (per-seed selection records are retained in the companion reproduction materials).

Baseline and adapter inference use the same Qwen checkpoint, prompts, and parser. The shared-protocol freeze records byte hashes for the system instruction, user template, and parser; the scorer is identified by version but lacks an executable hash in that registry. Full outbound request arrays were not saved, so template and input-file identity do not independently establish every transmitted request byte. Its Hub revision was not recorded, and byte identity with the earlier JSON-offset checkpoint has not been established. Human-reference labels, the V4.2.12-based teacher prompt, the shared-guideline protocol, and the later V4.2.14 handbook retain separate version identities; later handbook maintenance does not change frozen labels or execution protocols.

% Full source paths, hashes, and audit narration: retained unchanged in
% tex/extension_provenance.tex, tex/gold150_shared_rev2_patch1_unverified.tex,
% tex/quality_provenance_R12.tex, and revisions/before_R16. See REVISION_R16.md.

% [R21] Public-facing terminology maps to unchanged artifact identifiers.
\paragraph{Terminology and artifact identifiers.}
The human reference set retains the artifact identifier \texttt{Gold150} (\path{gold150_test.jsonl}). The challenge cohort corresponds to \texttt{Challenge-100}, with artifact name \texttt{gold100\_page1}. The calibration cohort corresponds to \texttt{Audit-50} (also called IAA-50), with artifact name \texttt{iaa50}. The initial teacher-label review cohort and post-generation sample retain the identifiers \texttt{A100} and \texttt{QA100}. The archived machine-prefilled subset is \texttt{Dual15}; that file name does not establish identity with the author-reported independent exercise (\hyperref[app:b]{Appendix B}). H730/E1621 denote generation pools, whereas H/E/M denote conflict-origin, non-conflict-origin, and mixed training conditions. These naming clarifications do not alter sample membership, annotation status, or files.
The public \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150/README.md}{terminology index} maps these names to canonical files and scoring entry points. Artifact names are unchanged to preserve compatibility with released code.


\paragraph{Materials for current result tables.}
The local evidence inventory distinguishes rescoring from rerunning. For Table~\ref{tab:gold150-shared-r7}, retained files include the common input/reference, system and user templates, occurrence parser, final records or accepted predictions for all six configurations, and configuration/score summaries. The execution registry names the scorer version but does not bind its executable bytes. For the Qwen block of Table~\ref{tab:gold150-main}, the same baseline and all three LoRA predictions, B2 manifests, selection histories and training/inference settings are retained; this inventory does not establish publicly downloadable adapters or a fully pinned retraining environment. For the JobBERT block, per-condition seed predictions and selection/configuration records are retained, but the executed tokenizer, token-to-character export and inherited-checkpoint selection remain unresolved. These are distinct gaps: accepted predictions support diagnostics, while rerunning requires the actual model and conversion implementation.

The local evaluation-entry and materials checklists identify file paths and hashes without claiming that every file is in the public archives. A fixed public commit binding all current table materials was not verified in this check. Original text redistribution permissions and the implemented privacy treatment also require confirmation from collection records before submission; public webpage access alone does not establish redistribution rights.

```

### Current manuscript wording

```tex
\section{Appendix D. Reproduction and Versioned Materials}
\phantomsection
\label{app:d}
\label{sec:extension-provenance}
\label{sec:display-archive-r14}

The public repository's \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/REPRODUCIBILITY.md}{reproduction guide} provides file inventories, checksums, and scoring instructions. The source package's \path{reproduction/experimental_notes/} consolidates detailed experimental conditions, failure analyses, provenance checks, and practical reproduction reminders. It includes the original passages and a location map for details condensed in this manuscript. Public access follows the release inventory in Data Availability.

\paragraph{Current comparisons.}
The shared-guideline inference study uses the frozen human reference, common messages, occurrence parser, and configuration-specific settings. The Qwen adaptation study holds the base model and inference protocol fixed across the no-adapter baseline and three B2 LoRA runs. JobBERT B1/B2 compares revised training supervision and development-based selection from a shared encoder/CRF. The reproduction notes supply manifest counts, selection histories, archived predictions, and the implementation information available for each comparison.

\paragraph{Version and artifact mapping.}
The human reference retains the identifier \texttt{Gold150} (\path{gold150_test.jsonl}); its challenge and calibration cohorts correspond to \texttt{Challenge-100} and \texttt{Audit-50}/\texttt{iaa50}. Teacher-review cohorts retain \texttt{A100} and \texttt{QA100}, with \texttt{Dual15} naming the archived machine-prefilled subset. The \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150/README.md}{terminology index} maps these names to canonical files. Version maps distinguish the frozen reference, teacher prompt, shared inference protocol, and current handbook.

\paragraph{Access and reproduction.}
Zenodo v0.1.3 contains the human reference and B2 training/development data identified in Data Availability. GitHub maintains the later portable scoring tools. The released JobBERT initialization and B2 continuation are distinct checkpoints; the default continuation represents seed 42. Qwen adapters remain unreleased. The reproduction notes distinguish reproducing scores from rerunning inference or training and list the remaining artifact and implementation gaps. Earlier releases, historical model variants, and complete supplementary results are indexed with their original conditions.

```


## N069: Compact reproduction index and layout

Source: `tex/appendix_D_reproduction_R16.tex`

### Original detail

```tex
\section{Appendix D. Reproduction and Versioned Materials}
\phantomsection
\label{app:d}
\label{sec:extension-provenance}
\label{sec:display-archive-r14}

The public repository's \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/REPRODUCIBILITY.md}{reproduction guide} provides file inventories, checksums, and scoring instructions. The source package's \path{reproduction/experimental_notes/} consolidates detailed experimental conditions, failure analyses, provenance checks, and practical reproduction reminders. It includes the original passages and a location map for details condensed in this manuscript. Public access follows the release inventory in Data Availability.

\paragraph{Current comparisons.}
The shared-guideline inference study uses the frozen human reference, common messages, occurrence parser, and configuration-specific settings. The Qwen adaptation study holds the base model and inference protocol fixed across the no-adapter baseline and three B2 LoRA runs. JobBERT B1/B2 compares revised training supervision and development-based selection from a shared encoder/CRF. The reproduction notes supply manifest counts, selection histories, archived predictions, and the implementation information available for each comparison.

\paragraph{Version and artifact mapping.}
The human reference retains the identifier \texttt{Gold150} (\path{gold150_test.jsonl}); its challenge and calibration cohorts correspond to \texttt{Challenge-100} and \texttt{Audit-50}/\texttt{iaa50}. Teacher-review cohorts retain \texttt{A100} and \texttt{QA100}, with \texttt{Dual15} naming the archived machine-prefilled subset. The \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150/README.md}{terminology index} maps these names to canonical files. Version maps distinguish the frozen reference, teacher prompt, shared inference protocol, and current handbook.

\paragraph{Access and reproduction.}
Zenodo v0.1.3 contains the human reference and B2 training/development data identified in Data Availability. GitHub maintains the later portable scoring tools. The released JobBERT initialization and B2 continuation are distinct checkpoints; the default continuation represents seed 42. Qwen adapters remain unreleased. The reproduction notes distinguish reproducing scores from rerunning inference or training and list the remaining artifact and implementation gaps. Earlier releases, historical model variants, and complete supplementary results are indexed with their original conditions.

```

### Current manuscript wording

```tex
\section{Appendix D. Reproduction and Versioned Materials}
\phantomsection
\label{app:d}
\label{sec:extension-provenance}
\label{sec:display-archive-r14}

The public repository's \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/REPRODUCIBILITY.md}{reproduction guide} provides inventories, checksums, and scoring instructions. The source package's \path{reproduction/experimental_notes/} consolidates experimental settings, failed-output analyses, implementation gaps, and practical reproduction reminders. Original passages and a location map preserve the details condensed in this manuscript.

The materials distinguish shared-guideline inference, Qwen adaptation under a fixed protocol, and JobBERT supervision-and-selection comparisons. They retain each study's manifests, selection records, available predictions, and historical context. The \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150/README.md}{terminology index} and companion version map connect paper names to canonical files and earlier releases.

Public access follows Data Availability and the release inventory. Archived predictions support score reproduction; the notes separately specify the artifacts required for rerunning inference or training, including unreleased Qwen adapters and unresolved implementation details. Full supplementary results accompany their original conditions.

```


## N070: Access statement points to consolidated maps

Source: `0main.tex`

### Original detail

```tex
\hyperref[app:d]{Appendix D} identifies earlier releases and maps paper terminology to repository files
```

### Current manuscript wording

```tex
\hyperref[app:d]{Appendix D} directs readers to release and terminology maps
```


## N071: Second reading: consolidate repeated archive signposts

Source: `3Experiments.tex`

### Original detail

```tex
Historical SOP+jieba evaluations and their original corpus partitions are documented in the companion reproduction materials alongside the current manifest definitions.
```

### Current manuscript wording

```tex
(Consolidated in Appendix D and the supplementary-materials paragraph.)
```


## N072: Second reading: consolidate repeated archive signposts

Source: `3Experiments.tex`

### Original detail

```tex
The no-adapter Qwen configuration is the comparator for the current occurrence-based LoRA study. Earlier SOP-extract-v4 and JSON-offset experiments are catalogued with their original protocols in the reproduction notes.
```

### Current manuscript wording

```tex
(Consolidated in Appendix D and the supplementary-materials paragraph.)
```


## N073: Second reading: consolidate repeated archive signposts

Source: `3Experiments.tex`

### Original detail

```tex
The figure and companion reproduction notes retain the type-specific results, sample support, and parser diagnostics.
```

### Current manuscript wording

```tex
Per-type F1 and gold-span support are shown alongside these counts.
```


## N074: Second reading: consolidate repeated archive signposts

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
 The historical 1M/3M training schedules and checkpoint lineage are recorded in the reproduction notes.
```

### Current manuscript wording

```tex
(Consolidated in Appendix D and the supplementary-materials paragraph.)
```


## N075: Second reading: consolidate repeated archive signposts

Source: `tex/student_protocol_R12.tex`

### Original detail

```tex
Training-source, JSON-offset, demonstration, and cleaning studies are retained with their original settings and results in the companion reproduction materials.
```

### Current manuscript wording

```tex
(Consolidated in Appendix D and the supplementary-materials paragraph.)
```


## N076: Second reading: consolidate repeated archive signposts

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
These results demonstrate task adaptation using the supplied Silver-plus supervision; detailed output-validity diagnostics accompany the reproduction materials.
```

### Current manuscript wording

```tex
These results demonstrate task adaptation using the supplied Silver-plus supervision.
```


## N077: Second reading: consolidate repeated archive signposts

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
 Per-seed results and training-pool variants are retained in the companion reproduction materials.
```

### Current manuscript wording

```tex
(Consolidated in Appendix D and the supplementary-materials paragraph.)
```


## N078: Second reading: consolidate repeated archive signposts

Source: `tex/silver_plus_results.tex`

### Original detail

```tex
; historical JobBERT training-pool diagnostics accompany the reproduction materials.
```

### Current manuscript wording

```tex
.
```


## N079: Second reading: consolidate repeated archive signposts

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
The reproduction notes document provider-access metadata, archived outputs, and the scope of score reproduction for these configurations.
```

### Current manuscript wording

```tex
(Consolidated in Appendix D and the supplementary-materials paragraph.)
```


## N080: Second reading: consolidate repeated archive signposts

Source: `tex/appendix_C_shared_R16.tex`

### Original detail

```tex
 The version map and example-selection checks are retained in the reproduction notes.
```

### Current manuscript wording

```tex
(Consolidated in Appendix D and the supplementary-materials paragraph.)
```


## N081: Second reading: consolidate repeated archive signposts

Source: `tex/appendix_B_quality_R16.tex`

### Original detail

```tex
The pre-generation A100 review and the later QA100 review retain separate versioned annotation layers; their exact counts and chronology are documented in the reproduction notes.
```

### Current manuscript wording

```tex
The pre-generation A100 review and later QA100 review retain separate versioned annotation layers.
```
