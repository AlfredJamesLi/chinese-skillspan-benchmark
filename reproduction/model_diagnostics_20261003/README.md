# Chinese model diagnostics on Gold150

These records support the Chinese-SkillSpan manuscript's Tables 7 and 8. They add Qwen boundary-exact scoring and a comparison of typed exact F1 by competency category. They do not contain new training runs or model inference.

## What changed

Qwen's four frozen prediction sets were rescored with the official `cnss-lskt-1.2.0` scorer. Typed exact and relaxed results reproduced their archived values. Boundary exact is the scorer's `collapsed_exact`: exact coordinate matching after removing type, with unique coordinates counted within each sentence. Independent set matching reproduced its counts. Replaying the frozen occurrence parser for all 600 outputs reproduced the accepted spans and parser outcomes.

The six encoder scoring records were already archived. Their type-specific F1 values were recomputed from TP/FP/FN, and means and sample SDs were calculated from the full-precision per-seed scores. All ten runs cover the same 150 sentences and 663 reference spans. The Qwen and encoder gold files have different serialized formats but identical IDs, source text, and L/K/S/T spans.

## Reported results

| Model | Typed exact | Typed relaxed | Boundary exact |
|---|---:|---:|---:|
| Qwen, no adapter | 0.361 | 0.470 | 0.414 |
| Qwen B2 LoRA | 0.540 ± 0.035 | 0.662 ± 0.033 | 0.571 ± 0.038 |
| XLM-R-large | 0.522 ± 0.022 | 0.650 ± 0.021 | 0.571 ± 0.022 |
| ESCOXLM-R | 0.538 ± 0.021 | 0.662 ± 0.022 | 0.582 ± 0.024 |

| Model | S (448 spans) | K (125 spans) | T (88 spans) | L (2 spans) |
|---|---:|---:|---:|---:|
| Qwen, no adapter | 0.377 | 0.302 | 0.380 | 0.000 |
| Qwen B2 LoRA | 0.525 ± 0.039 | 0.512 ± 0.063 | 0.638 ± 0.017 | 0.800 |
| XLM-R-large | 0.506 ± 0.024 | 0.495 ± 0.037 | 0.627 ± 0.006 | 0.800 |
| ESCOXLM-R | 0.518 ± 0.029 | 0.537 ± 0.009 | 0.631 ± 0.020 | 0.800 |

Category scores are typed exact F1 from jointly predicted L/K/S/T labels. Every reference sentence is retained, including sentences without spans of the evaluated category. The no-adapter result is one run. Other rows report the mean and sample SD over training seeds 42, 43, and 44. Each trained run has L counts of 2 TP, 1 FP, and 0 FN; the no-adapter run has 0 TP, 1 FP, and 2 FN. Full-precision summaries retain the zero L seed SD, which is omitted from the paper table because it provides no evidence of reliability with only two reference spans.

Qwen's mean S and K improvements are 0.148 and 0.210 F1 units after rounding. All three adapters improve K/S/T F1 over the no-adapter run. These are descriptive category findings; no category-specific significance test is reported.

## Files and reproduction

- `official_scores/`: four newly generated Qwen receipts and the six existing encoder receipts.
- `summaries/per_run_metrics.csv`: full-precision P/R/F1 and TP/FP/FN, including exact and relaxed results for every L/K/S/T category.
- `summaries/summary.csv` and `summary.json`: full-precision mean and sample SD; blank/null SD identifies a single run.
- `qwen_boundary_audit.json`: input hashes, coverage, parser replay, independent count comparisons, and canonical gold comparison.
- `encoder_types_audit.json`: independent encoder count and summary verification.
- `provenance.json`: receipt origins and hashes, with the pre-revision repository commit.

Rebuild the summaries with Python's standard library:

```text
python summarize_metrics.py --records official_scores --out summaries
```

For prediction-level verification, obtain the frozen Qwen pack and scorer through the [Qwen reproduction archive](https://doi.org/10.5281/zenodo.22851581) and [project reproduction guide](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/REPRODUCIBILITY.md). The audit records the exact scorer and parser hashes. Supply the pack directory containing `00_freeze`, `01_shared_prompt`, and `02_sft`:

```text
python audit_qwen_boundary.py --pack PATH_TO_PACK --scorer PATH_TO_SCORE_LSKT_PY --out verification
```

The optional `--encoder-gold PATH_TO_GOLD_BIO_JSONL` checks the canonical reference against the encoder release. Encoder materials are indexed by the [encoder audit archive](https://doi.org/10.5281/zenodo.22937245). Scoring verification does not require training or model inference. Redistribution of the original inputs remains governed by their existing access terms; no sentence text is added here.

## Interpretation

Gold150 informed guideline development. These scores are diagnostic comparisons on that reference, not a new blind model test. The three adapted systems use the 2,150/169 B2 training/development split, but their prediction heads, training budgets, and inference procedures differ. Small cross-model point-score differences do not establish architectural superiority.

The Qwen adaptation comparison supports the training value of the recorded Silver supervision under fixed inference conditions. It does not estimate the accuracy of the complete Silver pool or establish the correctness of the Gold reference. S/K category scores are not a reproduction of the English SkillSpan annotation protocol, and no cross-language ranking is claimed. JobBERT metrics not verified in this update are not filled by inference or borrowed from another model.

The optional `SK_combined_typed_exact` field in the Qwen audit filters both the existing joint predictions and reference spans to S/K while retaining all sentences. It is not a two-type retraining run or a SkillSpan score and is not added to the manuscript.
