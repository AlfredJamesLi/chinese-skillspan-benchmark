# Experimental details and reproduction reminders

This guide accompanies the reader-focused manuscript revision of 13 September 2026. It consolidates implementation details, unsuccessful outcomes, historical comparisons, and provenance checks previously repeated throughout the paper. The underlying results and their limitations are unchanged. Material restrictions on sampling, comparison design, and generalization remain summarized in the manuscript.

These notes accompany the Round 2 repository synchronization. Historical availability statements below describe the earlier audit; the current file-level status is in [the evaluation entry](../EVALUATION_ENTRY.md). This documentation update is not a new Zenodo deposit.

## How to use these notes

1. Select the experiment and its frozen data, labels, prompt, parser, and model configuration.
2. Distinguish reproducing a score from rerunning inference or training.
3. Read the relevant limitations below before interpreting differences between experiments.
4. Consult [the original passages and location map](DETAILED_PASSAGES.md) for exact details. [RELOCATION_MAP.json](RELOCATION_MAP.json) records the previous and revised wording; Complete pre-edit manuscript source backups remain local; this public package preserves the relevant original passages and mappings.

## 1. Which comparison answers which question?

| Comparison | Interpretation | Reproduction reminder |
|---|---|---|
| Six shared-guideline inference configurations | Extraction with common instructions and output schema | Access paths, models, and inference budgets differ; this is a descriptive comparison of recorded configurations. |
| Qwen without adapter versus B2 LoRA | Task adaptation under a fixed inference protocol | Use the same base model, messages, examples, occurrence schema, parser, decoding, and reference. There is no B1 Qwen fine-tuning condition. |
| JobBERT B1 versus B2 | Revised training supervision together with development-based checkpoint selection | Both training and development labels change. This does not isolate teacher identity, an individual rule, or label quality alone. |
| Historical SOP or JSON-offset experiments | Earlier extraction and supervision settings | Keep their original inputs, output contracts, labels, and selection conditions. Do not substitute them for the current Qwen no-adapter baseline. |
| Historical training-source, pool-extension, and cleaning studies | Supplementary sensitivity observations | These studies also change composition, initialization, or selection; they are not controlled sample-size or single-factor effects. |

The Qwen and JobBERT panels are separate uses of the resource, not a matched architecture ranking. Their initialization and learning conditions differ. All original results, including unfavorable changes, remain in [supplementary tables](../supplementary_tables/) with their historical context.

## 2. Reference and collection provenance

The corpus has 22,840 sentences and an original 17,460/2,143/3,237 split. Its AI, Cloud, public-sector, and graduate collection names are not mutually exclusive occupational categories. Available materials do not fully recover platform identities, collection dates, inclusion criteria, sentence segmentation and deduplication procedures, conflict-admission criteria, challenge-selection procedures, or coder qualifications. These points require reconciliation with the original collection and annotation records; collection names alone do not establish representativeness.

The 2,601-record study lineage combines a 980-record disagreement queue and 1,621 SOP–CWS records. It is not established as a random subset of the original test partition. Historical SOP+jieba and Gold v2 labels on these identifiers are distinct from the present human-reference and Silver-plus layers.

The human reference includes a 50-sentence calibration cohort and a 100-sentence challenge cohort. It was involved in handbook development and repeatedly examined. Absence of exact train/reference text matches does not remove this development exposure or establish a fresh blind evaluation. Independent testing on newly collected sources is needed for transfer claims.

The reference contains 663 spans, including only two L spans; its micro scores are dominated by S. Identifier prefixes provide 61 document groupings, not independently reconstructed advertisements. Original wording redistribution and implemented privacy treatment require collection-record confirmation; public webpage access alone does not establish redistribution rights.

## 3. Student manifests and duplicate handling

The primary JobBERT v6a uses 2,156 training and 169 development records, including six training records that match three development texts under NFC. Removing these yields the Qwen `v6a_nocross` split of 2,150/169. Both are sentence-level extensions rather than document-isolated splits. JobBERT and Qwen retain 1,913 and 1,910 distinct NFC training texts, respectively. No human-reference identifier or full NFC reference text occurs in these train/development splits. NFC comparisons do not change the original scored strings or character offsets.

Historical v3 uses 1,382/169 records under document isolation; v4 extends training to 1,913 through other sentences from shared documents; v5 repeats records to reach 2,200. v6a removes 44 training copies of development sentences. The cleaning study uses 2,138/168. These stages change composition as well as sample size and must not silently replace the designated manifests.

B1 and B2 share IDs and texts within each v6a split, with different labels in 1,440 training and 107 development records. Each condition selects on its own development targets. Selection scores are development scores, not test results, and do not share identical target labels.

The Qwen manifest's A100/H730/E1621 origins contribute 96/637/1,417 training and 4/53/112 development records. Training spans contain 2,218 S, 641 K, 763 T, and 24 L; development has 207 S, 61 K, 77 T, and no L. These are annotation-origin groups, not a recovered four-source distribution. Empty-label frequencies differ substantially by layer: 869/2,150 training, 82/169 development, and 8/150 reference sentences. These frequencies describe sampling composition, not relative annotation quality.

## 4. Annotation review and frozen-file identity

The original independent 50-sentence coding study and the machine-prefilled review samples are distinct designs. Available later coder exports reproduce character-level Cohen's kappa 0.5673 and exact typed span F1 0.4444; byte identity with the initial pre-adjudication freeze is unresolved. The two-class-plus-O projection gives kappa 0.5916 and does not recreate SkillSpan's potentially overlapping annotation layers. Character positions are nested in sentences, not independent test observations.

The later QA100 review has 140 exact matches between 144 machine and 148 reviewed spans, giving P/R/F1 0.9722/0.9459/0.9589. Ninety-five sentences have identical complete span sets. Stratified sampling used 2,179 eligible records; two small strata totaling 11 records were unsampled. This is a reviewed-sample result, not an unbiased corpus-wide accuracy estimate.

The pre-generation A100 has historical 419-span supervision and a later 432-span review layer. These versions do not overwrite labels used in completed runs. The authors report an earlier independent 15-sentence A100 exercise without exposure to machine predictions or the other coder's spans. Its original exports, mapping, chronology, and metric have not been reconciled with the retained files. Archived Dual15 instead belongs to machine-prefilled QA100, with 27 identical spans in each layer. It cannot supply an independent agreement coefficient for the earlier exercise or a matched pre/post reliability result.

Human-coding diagnostics record 21 Coder B typing disagreements involving job-use tools labeled K rather than adjudicated S, Coder A K recall of 0.29, and missed T mentions. Both coders missed the single L span in the calibration cohort. These are human-coding observations and cannot be reinterpreted as student-model error frequencies. The existing historical rounding discrepancy for Coder A recall is retained with its explanation in Appendix B.

## 5. JobBERT implementation and checkpoint recovery

Continuation reuses the released 3M encoder and historical CRF. The earlier 1M and 3M models differ in recorded pretraining schedules and extraction checkpoints, so their contrast is not a controlled pretraining-volume ablation. The training-source comparison initializes a fresh task head/CRF and is not the designated continuation experiment.

Saved continuation configurations identify the shared model directory and `crf/best.pt`. The executed training/export source, saved tokenizer revision, exact token-to-character conversion, and long-input handling were not recovered. A maximum-input setting of 256 tokens therefore does not establish which original spans were truncated or retained. The inherited CRF's original selection history is unresolved. Published default B2 continuation is seed 42, not the three-seed mean.

## 6. Qwen training and inference

Qwen B2 training uses the unchanged 2,150/169 records with lossless BIO-to-occurrence conversion. Training uses AdamW, linear learning-rate scheduling, zero warmup and weight decay, gradient checkpointing, BF16, and A100 80GB hardware. Loss applies only to assistant JSON and the closing turn token. No sequence exceeds the 8,192-token training limit. Development exact F1 selects checkpoints, preferring the earlier epoch when scores differ by at most 1e-4.

Baseline and adapters share messages, examples, parser, deterministic decoding, and a 2,048-token output cap. The baseline predictions are reused throughout the matched comparisons. Qwen adapters are not publicly released. Its Hub revision was not recorded, and byte identity with the earlier JSON-offset checkpoint is not established. Template/input hashes do not recover outbound requests that were not archived.

## 7. Provider access and computation budgets

Qwen runs locally; GPT and Claude used a proxy; Kimi and DeepSeek used provider endpoints. Proxy-returned names, including `gpt-5.6-terra`, are metadata rather than independently verified checkpoint or routing identities. Full outbound request arrays and model weights were absent from the audit package.

Both DeepSeek configurations use API model `deepseek-v4-pro`. Non-thinking and thinking modes set output caps of 2,048 and 8,192 respectively; 8,192 is not a verified number of reasoning tokens. Kimi uses non-thinking mode and endpoint-required temperature 0.6. No equivalent GPT/Claude switch was recorded. Shared task instructions therefore do not equalize computation budgets. DeepSeek thinking has higher precision and lower recall; aggregate scores do not isolate output-format failures as the cause.

## 8. Scoring, rejected outputs, and failure cases

All 150 reference sentences remain in evaluation. The parser checks IDs/JSON, literal nonempty substrings, occurrence indices, types, and output fields. After sorting by start and original output order, it removes duplicates and rejects later conflicts/overlaps. Accepted spans from partially rejected outputs remain scored. Wholly rejected or malformed outputs yield empty predictions; missing reference spans then count as false negatives. Empty–empty cases contribute no span counts. No test-guided boundary snapping is used.

The coverage count of 150 is not the span-level F1 denominator. Relaxed matching measures boundary tolerance, not independent semantic correctness. Structural output validity is distinct from semantic accuracy, and exact–relaxed differences are not a pure boundary-error rate. Three training seeds describe run variability on a common test set; their SD is not a test confidence interval, and they do not create 450 independent observations.

Complete mutually exclusive output-status counts remain in [output outcomes](../output_outcomes/). These include the 18 format failures for the DeepSeek thinking configuration and the partially accepted and fully rejected outputs of other configurations. They must remain included under the documented coverage rules.

The Qwen no-adapter diagnostic has 168 rejected candidates: 167 occurrence errors and one overlap conflict. Of the occurrence errors, 155 are unique literal strings assigned a nonzero occurrence index and 12 are absent from the source. None is a repeated-string out-of-range case. These observations do not establish a one-based counting mechanism. Rejected candidates were not repaired or added to accepted-span diagnostics.

Figure 5 preserves all four runs' accepted-span results. The eight empty-reference sentences have no format-failure or all-spans-rejected outcomes in these runs. Their FP span counts are 19/6/4/0, affected-sentence counts 2/2/1/0, and legal-empty counts 6/6/7/8. L has only two gold spans, with 0/2 recovered without an adapter and 2/2 for each adapter; each run has one extra L prediction. Full metrics remain in [Qwen diagnostics](../qwen_diagnostics/).

## 9. Version compatibility and admission decisions

The reference, V4.2.12-based teacher prompt, shared `rev2 patch1` protocol, and V4.2.14 handbook have separate identities. Later amendments did not regenerate earlier labels or execution protocols. Case `1838-s0008` changes from S `[9,25)` to `[9,16)` and `[17,19)`, retaining S `[26,37)`. It is present in the teacher layer and absent from the 150-sentence reference by ID and exact text. This targeted check does not establish full compatibility of later rules with all frozen annotations.

The historical 82-record adjudication queue is not a permanent exclusion set. Its later registry has 53 resolved, three confirmed-empty, and 26 undetermined records. The Qwen manifest admits 51 resolved and three confirmed-empty records to training and one resolved record to development, with none of the 26 undetermined records. These are Qwen membership counts, not a replacement JobBERT manifest.

## 10. Available artifacts versus missing rerun requirements

Archived accepted predictions reproduce the reported exact and relaxed scores. Current inventories include input/reference files, message templates, occurrence parser, final outputs or accepted predictions, manifests, and configuration/selection summaries. The freeze registry identifies the scorer version but lacks its executable hash; full outbound requests, some checkpoint identities, and JobBERT conversion implementation remain unresolved.

Consequently, offline score reproduction is better supported than fully pinned rerunning or retraining. A fixed public commit binding every current table artifact was not verified. Do not infer public release from an existing local path. The human reference and B2 data are in Zenodo v0.1.3; later portable scoring tools are on GitHub, and earlier v0.1.1/v0.1.2 snapshots lack those current data files. The relevant old appendix passages and links are preserved in DETAILED_PASSAGES.md; the complete manuscript backup remains local.

The original passage archive preserves both favorable and unfavorable context. Changes in the manuscript concern presentation and location, not the experimental record.
