# Benchmark annotation profiles

The current manuscript separates the dataset profile (Figure 4) from the
additional assisted-review profile (Figure 8). Both use the same archived
aggregate statistics as the earlier combined layout.

- **Figure 4** shows input and span lengths for the original silver
  training/development sets used by Qwen and the encoder comparison
  (2,150/169 records) and the human reference (150 sentences). Its type-composition
  panel also includes the complete adopted expanded silver pool.
- **Figure 8** shows the shared input-length distribution of the additional
  150-sentence review sample and the two reviewers' span-length distributions
  (358 spans for A and 365 for B). A and B are annotation layers on the same
  sentences, not separate samples.

The adopted expanded pool contains 9,540 records and 21,101 spans; 2,492 records
(26.1%) have no annotated span. Its type counts are L = 155, S = 11,528,
K = 5,265, and T = 4,153. It includes earlier supervision, so the displayed
groups are not additive. The alternative 9,646-record pool and the separate
blinded agreement sample are outside these plots. Record multiplicities,
identifiers, and frozen annotations are unchanged.

See the [current figure index](../manuscript_revision_20261002/FIGURE_INDEX.md)
for the manuscript assets and editable sources.

## Rebuild the current Figures 4 and 8

From the repository root, with the packages in `requirements.txt` installed:

```sh
python reproduction/benchmark_profile/benchmark_profile.py --aggregate reproduction/benchmark_profile/benchmark_profile_data.json --output output/benchmark_profile --main-only --stem benchmark_profile_main_20261006
python reproduction/benchmark_profile/benchmark_profile.py --aggregate reproduction/benchmark_profile/benchmark_profile_data.json --output output/benchmark_profile --review-only --stem additional_review_profile_20261006
```

The two view options select different panels from the same aggregate JSON. They
do not resample records, alter annotations, or recompute model performance.
Each command writes PDF, SVG, PNG, and grayscale previews. Font availability and
plotting-library versions may affect appearance; use the archived PDF/SVG files
when the exact submitted artwork is needed.

## Rebuild the earlier combined layout

The command below is retained for compatibility. Without either view option,
the script includes the additional-review layers together with supervision and
reference distributions. This is the earlier combined layout, not the exact
layout of current Figure 4 or Figure 8.

```sh
python reproduction/benchmark_profile/benchmark_profile.py --aggregate reproduction/benchmark_profile/benchmark_profile_data.json --output output/benchmark_profile
```

The aggregate JSON contains the five unchanged historical groups and a separate
`expanded_silver` object with complete-pool and split-level counts, histograms,
source-file hashes, and validation results. No sentence texts, record identifiers,
span offsets, credentials, or model predictions are included. The standalone
`expanded_silver_profile.json` and `expanded_silver_class_counts.csv` provide the
same expanded-pool statistics for reuse.

## Recompute from frozen annotation files

The original five groups can be recomputed by researchers with access to the frozen source files:

```sh
python reproduction/benchmark_profile/benchmark_profile.py --evidence /path/to/Gold150_shared_prompt_eval_for_Overleaf_20260910 --qa /path/to/QA150_all_layers.jsonl --expanded-profile reproduction/benchmark_profile/expanded_silver_profile.json --output output/benchmark_profile
```

To recompute expanded-pool statistics from the private frozen split archive and
cross-check them against the published Qwen reproduction package:

```sh
python reproduction/benchmark_profile/derive_expanded_profile.py --source-zip /path/to/expanded_silver_splits_20260920_docs_20260921.zip --reference-package /path/to/CNSS_Qwen_Reproduction.zip --output output/expanded_profile
```

The script verifies the frozen archive hash, original Qwen split-file hashes
and identifier order, Unicode offsets, BIO tags, occurrence targets, assistant
JSON, and every count and histogram sum. It reads source archives without
changing them. JobBERT's 698-record development file is the union of Qwen's
348 validation and 350 test records and is not counted as another partition.

## Measurement and display conventions

- Input lengths: unmodified Unicode code points, including spaces and punctuation;
  empty-target records remain in the ECDFs. A log axis retains the observed tail.
- Span-length violins: all observed spans in the selected layers (three in the main view, two in the review view, and five in the earlier combined view);
  Gaussian KDE with Scott bandwidth and equal maximum widths. The 0--20 detail
  view and full-range overview use the same full-data densities. White dots mark
  medians, thick lines the middle 50%, and the upper labels mark maxima.
- Heatmap: exact type counts and percentages of spans **within each row**, with
  a shared 0--70% blue scale. Rounded percentages need not sum to exactly 100%.
- Empty-label proportions use records as the denominator, not spans. Appendix B
  reports these proportions and counts separately for train/validation/test.
- Frozen record multiplicities are retained. Duplicate checks and stronger
  normalization matches are reported in the expanded aggregate; no deduplicated
  training experiment is implied. Review-layer overlaps are retained as spans.
- PDF and SVG are vector outputs. A 300 dpi PNG and a grayscale preview are also
  produced. These descriptive profiles do not measure annotation accuracy.

## Design references

SkillSpan Figure 2 motivates the span-length violins with medians and quartiles:
https://arxiv.org/pdf/2204.12811

CLUENER2020 motivates reporting category composition by data split:
https://arxiv.org/pdf/2001.04351

The figure is drawn from Chinese-SkillSpan counts; no published image or
cross-dataset numerical comparison is reproduced. English token counts are
not equated with Chinese character lengths.
