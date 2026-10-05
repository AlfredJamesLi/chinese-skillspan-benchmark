# Reproduction details accompanying the prose revision

These notes retain calculation and chronology details moved from the article during its prose revision. Dataset membership, labels, predictions, reported scores, and scoring rules are unchanged by this edit.

## Blinded annotation stages

The first three-annotator export was saved on 2 October 2026. Mean pairwise typed exact-span F1 was 0.663. The export after individual handbook-based self-review was saved on 3 October 2026 and gives 0.818. Machine suggestions and other annotators' labels were hidden during the study. The article reports both stages explicitly; the later stage supplies its final agreement estimates. The stages are not separate cohorts.

- [Before self-review: annotations and calculations](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/main/reproduction/agreement/finalguide_abc_20261002)
- [After self-review: annotations and calculations](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/main/reproduction/agreement/finalguide_abc_20261003)

All 10,000 bootstrap resamples produced defined values for the coefficients reported for the final study.

## Additional assisted review

The two exported review layers cover the 150 identifiers in the stratified draw. Reviewer confirmations were stored separately. The draw contains 60 cloud, 45 public-sector, and 45 listed-company sentences, with no normalized complete-text overlap with the original 350 human-reference and review sentences.

The source-stratified sentence bootstrap uses 10,000 resamples and random seed **20260917**. This random seed belongs to the additional-review agreement analysis, not the paired source-document bootstrap for model comparisons. The original comparison layers, counts, and interval results remain unchanged.

## API chronology and completion records

The baseline API calls were completed on **10–11 September 2026**. Request and response model identifiers, output budgets, and service modes remain specified in the manuscript's model-configuration table. The completion and parser records are preserved in the [DeepSeek and output audit](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/main/reproduction/reviewer_revision_20261005).

The 18 empty final answers from the DeepSeek thinking configuration remain empty predictions in the 150-sentence evaluation. These requests returned HTTP 200 and exhausted their output budget. This prose revision removes neither their records nor their contribution to the reported score.

## Numerical presentation and scoring checks

Scores and differences are calculated at full precision before rounding. Displayed scores normally use three decimal places; scientific notation is used where needed to preserve the sign of a near-zero interval endpoint. The sentence-level counts reproduce the reported exact scores before bootstrap resampling.

All supplied sentence identifiers were checked before scoring. Boundary-only exact F1 is computed from the same accepted spans by dropping types and removing duplicate coordinates within each sentence. No new model training or inference is involved in that score.

The bootstrap for paired model comparisons samples 61 complete source-document groups with replacement, using the same draw for all compared models. Earlier sentence-bootstrap results and the source-group random seed remain in the linked reproduction package; the article continues to specify the source-group method used for its reported intervals.

## Expanded-pool configurations

The article now identifies the pools by their roles: **adopted expanded pool** (9,540 records) and **alternative expanded pool** (9,646 records). Codex and the API gateway identify annotation channels for the replaced candidate batch; they are not dataset names. Legacy filenames and experiment identifiers are retained for reproducibility.

The adopted expanded JobBERT configuration uses 8,842 training and 698 development records. The expanded Qwen configuration uses 8,842 / 348 / 350 training / validation / test records. The separate 7,117-record JobBERT result is identified by its actual training set rather than described as a preceding run. These configurations and their scores are unchanged.

## Manuscript-preparation chronology

The preparation tools were used in September–October 2026. The preparation records do not identify every underlying model version. The article's AI-use statement reports the known tool roles and available identifiers; evaluation-model identifiers should not be substituted for unrecorded manuscript-preparation versions.
