# Annotation agreement and review samples

Current names and sample relationships are defined in the [resource guide](../../docs/terminology.md). Historical calibration belongs to the human reference set; the additional review sample has two layers on the same 150 sentences. The separate 50-sentence blinded agreement sample is described below and supplies the current manuscript's main agreement results.



The historical calibration-study exports contain 50 paired sentences and 2,571 Unicode code points. Original texts are aligned by source ID; spaces and punctuation remain included. The flat character labels are L/K/S/T/O. In this sample both coders have zero L frequency.



1. Assign each character its coder's span type, or O outside spans.

2. Count the paired labels and each coder's marginal frequencies.

3. Compute observed agreement p_o = 0.7709062621548036.

4. Compute expected agreement p_e = sum_c p_A(c)p_B(c) = 0.4705642521733224.

5. Cohen's kappa = (p_o-p_e)/(1-p_e) = 0.5672869865972949, printed **0.5673**.

6. Independently compare exact typed span sets: 98 matches between 211 Coder A and 230 Coder B spans yield F1 = 196/441 = **0.4444**.



[Calculation data](calculation.json) includes the confusion matrix, marginal counts, input hashes and the optional collapsed-category projection (kappa 0.5916). Matrix orientation is Coder B followed by Coder A. Names in this legacy calculation are display aliases. The [25 September annotation-layer release](../evidence_review_20260925/annotation_layers/README.md) supplies pseudonymized analytical copies; original files remain unchanged. Coder letter order follows each file and must not be assumed identical across historical reports.





The 2,571 characters are nested within 50 sentences, not independent sample units. Original freeze byte identity remains unresolved.



## Additional coder and review comparisons



| Sample | Design | Character kappa | Exact span F1 |

|---|---|---:|---:|

| Dual15 auditor subset | Machine-assisted double review within QA100 (author-corrected) | 1.0000 | 1.0000 |

| Additional review sample | Two reviewers with machine suggestions visible | 0.8827 | 0.8160 |



The author-supplied September 17 Dual15 export records both coders' 15/15 confirmations. Its seven manifest file hashes were checked and the coefficients independently recalculated over 719 characters and 27 matching spans. The administrative seed layer equals both human layers. The author subsequently corrected the design on 25 September: machine coding suggestions were available to the annotators. The earlier strict-blind interpretation is withdrawn. These coefficients describe assisted-review agreement and do not establish independent blind reliability. The 50-sentence historical raw-text study remains a separate design.



The additional review sample's nominal Krippendorff alpha is 0.8826, calculated over 5,990 unambiguous positions. Exact span sets agree on 101/150 sentences. Two conflicting-type positions are excluded from the character calculation, while all original spans remain in span F1. The [annotation-layer release](../evidence_review_20260925/annotation_layers/README.md) now supplies sentence texts and both human layers with pseudonymized account fields, preserving offsets and the design caveats. Administrative originals remain with the authors.



The nested 15 records add no unique sentences. Human reference construction and the two original review samples cover 350 sentences; the non-overlapping additional review sample raises coverage to 500. These designs do not form a common before/after reliability experiment.



The author reports four chronological stages (50, early150 including15, later150, another150). [File-level reconciliation](../evidence_review_20260925/COHORT_RECONCILIATION.json) currently reconstructs the human reference set + initial Silver review sample + post-generation Silver review sample + additional review sample as 500 unique texts. These stage names are not yet one-to-one matched; do not commission duplicate annotation or count multiple exports as new samples.





## Blinded agreement sample (latest exports: October 3, 2026)



The [completed statistical release](finalguide_abc_20261003/README.md) provides frozen pseudonymized labels for 50 sentences, pairwise agreement, source-stratified confidence intervals, a manifest and executable scoring code. Mean typed exact F1 is 0.818; three-rater character alpha is 0.907. The latest separate labels include individual self-review with access to the handbook. All three coders and all 50 sentences remain in the analysis. Training sets of five and fifteen sentences are excluded. The release records both the original plan and documented execution, and does not turn this blinded agreement sample into an independent Gold test set.

