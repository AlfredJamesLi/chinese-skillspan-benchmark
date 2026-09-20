# Expanded-Silver experiments

These later experiments combine earlier B2 supervision with new annotations. They are separate from the matched three-seed Qwen comparison.

| Pool | Train / validation / test | Qwen Silver-test exact F1 | Human-reference exact F1 |
|---|---|---:|---:|
| Proxy variant | 8,943 / 351 / 352 | 0.7585 | 0.5966 |
| Codex variant | 8,842 / 348 / 350 | 0.8092 | 0.5854 |

Both Qwen runs use seed 42. The variants replace labels for a 2,500-sentence candidate subset and differ in which records are retained; they are not a controlled comparison of annotation channels alone. The complete retained pools contain 9,646 and 9,540 records, respectively, rather than the initial target of 10,000.

## Files and access

- [Result values (CSV)](results.csv): seven Qwen subset/pool rows and JobBERT footnote results. Its historical Table H identifier maps to current manuscript Tables 7 and 14.
- [Qwen Codex-pool score snapshot](../../results_snapshots/qwen_pooled_9540_codex2500_gold150_20260916.json).
- [JobBERT Codex-pool score snapshot](../../results_snapshots/jobbert_pooled_9540_codex2500_gold150_20260916.json).
- [Source-selection records](../../data/silver_plus_10k_prep_20260913/README.md).

The public tree contains partial annotations and preparation records. Selected Qwen adapters, frozen Gold150 predictions, split identifiers, configurations, prompts, parser, and scoring tools are published in the [Qwen model-reproduction archive](https://doi.org/10.5281/zenodo.22851581). Its `MODEL_INDEX.csv` maps checkpoints to experimental conditions. Complete expanded-Silver training, validation, and test texts and labels are not included, so the package supports inference and rescoring but does not by itself supply every input needed for retraining. See the [archive notes](../../docs/archive_notes.md) for corrections to older release-status wording.

JobBERT's latest recorded run uses 8,842 training and 698 development records, so Qwen's separate Silver-test interpretation does not apply to it. Its human-reference exact F1 is 0.2317; the proxy-pool run gives 0.2416. These results remain part of the record.

Gold150 is excluded from gradients and checkpoint selection. Scores against Silver targets measure agreement with generated labels; scores against Gold150 provide an additional check against the selected human reference.

The `results.tex` copy preserves the original historical table bytes. [Original table location](../../docs/overleaf_paste_20260915/tables_H_public_api_silver.tex) remains available for older links.
