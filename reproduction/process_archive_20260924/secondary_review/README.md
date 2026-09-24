# Secondary review: supporting calculation and run details

This archive preserves records removed or condensed during the second editorial pass on the 41-page Chinese-SkillSpan manuscript. Numbers refer to that draft, not subsequent table numbering. Relocation does not add experiments or raise the verification status of the results. See the [complete 25-table audit](TABLE_AUDIT.md).

## Previous Table 13: calibration agreement calculation

Observed character agreement is 0.771, expected agreement 0.471, Cohen's kappa 0.567, and typed exact span F1 0.444. Support is 2,571 Unicode positions and 211/230 coder spans with 98 exact matches. These quantities remain in the paper's text; the duplicate [calculation table](tables/iaa50.tex) is retained here. The available exports do not establish identity with the original frozen files.

## Previous Table 16: final parser outcomes

The [complete nine-row ledger](tables/output_outcomes.tex) retains every configuration, including failed and rejected responses. Each row covers 150 sentences. Legal empty output is not necessarily a correct negative. Partial outputs retain accepted spans; malformed or fully rejected responses count as empty predictions. The paper keeps the key failure counts and their interpretation; the ledger is also preserved in [its original source](source/tex/review20260923/output_outcomes.tex).

## Previous Table 17: Qwen per-seed and cohort scores

All rows evaluate the same 150-sentence human reference, which was used in guideline development and is not an independent blind test. Checkpoints are selected on development data. Values below are manuscript display precision, not raw full-precision results.

| Condition | Precision | Recall | Exact F1 | Relaxed F1 | Challenge 100 F1 | Calibration 50 F1 |
|---|---:|---:|---:|---:|---:|---:|
| No adapter | 0.507 | 0.281 | 0.361 | 0.470 | 0.345 | 0.390 |
| LoRA, seed 42 | 0.588 | 0.434 | 0.500 | 0.624 | 0.511 | 0.480 |
| LoRA, seed 43 | 0.634 | 0.507 | 0.563 | 0.686 | 0.571 | 0.549 |
| LoRA, seed 44 | 0.633 | 0.499 | 0.558 | 0.676 | 0.567 | 0.543 |

The no-adapter prediction is shared across comparisons. LoRA exact F1 is 0.540 ± 0.035 (mean ± sample SD across seeds 42, 43, 44). The main comparison and paired intervals remain in the manuscript. [CSV](tables/qwen_per_seed.csv), [original table](tables/qwen_per_seed.tex), [unchanged values and macro definitions](source/tex/stage2_result_values.tex).

## Previous Table 25: NNOSE settings

The paper retains all six rows of linear-head and kNN test results, test sizes, single-seed status and datastore restrictions. Selected epochs and development-selected k, lambda and temperature are preserved in the [complete original table](tables/nnose_full.tex). Settings were selected on development data; this archive must not be read as evidence of a fresh rerun or improved test performance.

## Supporting procedural records

- [Original agreement discussion](source/tex/appendix_B_quality_R16.tex): sample selection, Dual15 administrative/export details, character counts, conflict record ID, and agreement calculations. The paper retains sample design, coding units, exclusions and lack of blind final-handbook reliability.
- [Parser/scorer, numerical conventions and mismatch ledger](source/tex/appendix_C_shared_R16.tex): identifier checks, deterministic ordering and tie handling, BIO edge cases, full precision policy, and structural mismatch counting. The paper retains matching definitions, malformed-output treatment, concrete errors and uncertainty assumptions.
- [Historical protocol context](source/tex/appendix_C_experiments_R16.tex) and [expanded experiment settings](source/tex/expanded_silver_results_20260917.tex): older JSON-offset comparison and repeat parameter descriptions.
- [Qwen diagnostic details](source/tex/qwen_diagnostics_round2.tex): full descriptive counts underlying the retained figure.
- [Original native-task methods](source/tex/external_benchmarks/paper_A_native.tex): software-stack versions, hardware-compatibility history, full NNOSE settings, and uncompleted configurations. The paper retains hardware, actual model/task/scoring choices, restrictions and findings.
- [Resource documentation](source/tex/appendix_D_reproduction_R16.tex): file-index descriptions and preparation records. Access and leakage limitations remain in the manuscript.

All excerpts are from Overleaf commit `5bc2ffb844a732d9e3660ebea4769818ef6ab895`. Internal LaTeX references remain original and these excerpts are not standalone manuscripts. [Manifest](manifest.json) verifies the archived files. No recruitment data, private coder exports, model weights, or new full-precision metrics are added by this archive. See the [earlier process archive](../README.md) for previously relocated tables and upstream result snapshots.
