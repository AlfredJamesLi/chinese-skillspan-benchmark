# Blinded agreement sample: latest individual annotations

This release supplies the annotation-agreement results for Chinese-SkillSpan. The blinded agreement sample is reported separately from historical human-reference and review coverage. Its individual layers measure agreement and do not form a consensus model test set; see the [resource relationships](../../../docs/terminology.md). Three coders independently annotated the same 50 sentences under B.sop_v4.2.14, with machine suggestions and one another's labels hidden. They could consult the handbook, check their own work, and revise their own labels. The analysis uses their latest separate exports dated 3 October 2026. The five learning and fifteen practice sentences are excluded.

## Results

| Pair | Character κ | Typed exact F1 [95% CI] | Boundary F1 | Equal sentence span sets |
|---|---:|---|---:|---:|
| A–B | 0.880 | 0.793 [0.694, 0.884] | 0.828 | 36/50 |
| A–C | 0.930 | 0.848 [0.752, 0.926] | 0.876 | 39/50 |
| B–C | 0.909 | 0.814 [0.721, 0.899] | 0.847 | 37/50 |
| Mean | — | 0.818 [0.732, 0.894] | 0.850 | All three: 34/50 |

Three-rater nominal character α is 0.907 [0.851, 0.954]; mean boundary F1 is 0.850 [0.766, 0.923]. Mean typed F1 exceeds the project's 0.80 target at the point estimate, while its interval includes values below the target. That criterion is not a universal reliability threshold. Eleven of the 34 identical sentence-level span sets are empty. The two L spans occur in one sentence, so they do not establish reliability across language requirements.

## Recalculation

Run `python recompute.py output.json` with Python 3.9+ and NumPy. The three `data/latest50_*.jsonl` files preserve source text, offsets, labels and confirmation status, with coders named A/B/C. Records are aligned by `study_id`, not original export order. The coders supplied 104/123/113 spans. No coder is designated as gold, and no labels or sentences are removed to raise agreement.

Within each pair, typed exact F1 pools exact span-and-type matches over all sentences. Boundary F1 ignores type. The reported means average the three pairwise micro-F1 values equally. Character κ and α use all 2,111 original Unicode code points, including spaces and punctuation, assigned O/L/K/S/T. Source text is not normalized for scoring.

Intervals use 10,000 source-stratified sentence resamples, seed 20260927 and NumPy default_rng/PCG64. All three annotations of a selected sentence are resampled together. The fixed source counts are 8 listed-company, 16 public-institution and 26 Tianchi sentences, with one sentence per recorded advertisement ID. Intervals condition on this sample and coder group; all resampled reported coefficients are defined. The original sampling frame is not reconstructed by this bootstrap.

`recomputed_metrics.json` contains full-precision results, per-type counts and intervals. `disagreements_16.jsonl` preserves all remaining non-identical sentence annotations without inventing an adjudicated answer. `verification.json` records input validation and comparison with the earlier snapshot. Two independent implementations agree on all checked point estimates.

## Export provenance

The received archive names the latest export directory `live_doccano_postdiscussion_20261003`. On 4 October 2026, the authors clarified that the labels were produced independently and that revisions consisted of each coder checking their own annotations and consulting the rules. The current analysis follows that clarification. The directory name is retained in the provenance record rather than used to infer a consensus-coding stage.

The [2 October snapshot](../finalguide_abc_20261002/) remains available with its original labels and results. It is superseded for the current manuscript, not overwritten. Both releases contain the same 50 texts and study IDs. This update does not change the human reference set, model predictions, training targets, historical assisted-review scores or model-evaluation results.

Reuse follows the repository's component-specific terms. The release does not grant additional rights over third-party recruitment text.
