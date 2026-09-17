# Coding agreement: current Table 3 and Appendix B

The available later exports contain 50 paired sentences and 2,571 Unicode code points. Original texts are aligned by source ID; spaces and punctuation remain included. The flat character labels are L/K/S/T/O. In this sample both coders have zero L frequency.

1. Assign each character its coder's span type, or O outside spans.
2. Count the paired labels and each coder's marginal frequencies.
3. Compute observed agreement p_o = 0.7709062621548036.
4. Compute expected agreement p_e = sum_c p_A(c)p_B(c) = 0.4705642521733224.
5. Cohen's kappa = (p_o-p_e)/(1-p_e) = 0.5672869865972949, printed **0.5673**.
6. Independently compare exact typed span sets: 98 matches between 211 Coder A and 230 Coder B spans yield F1 = 196/441 = **0.4444**.

[Calculation data](calculation.json) includes the confusion matrix, marginal counts, input hashes and the optional collapsed-category projection (kappa 0.5916). Matrix orientation is Coder B followed by Coder A. Names in this public summary are display aliases; original input files are unchanged and are not newly published here.


The 2,571 characters are nested within 50 sentences, not independent sample units. Original freeze byte identity remains unresolved.

## Additional coder and review comparisons

| Sample | Design | Character kappa | Exact span F1 |
|---|---|---:|---:|
| Dual15 auditor subset | Separate coder queues within QA100 | 1.0000 | 1.0000 |
| New QA150 | Two reviewers with machine suggestions visible | 0.8827 | 0.8160 |

The author-supplied September 17 Dual15 export records both coders' 15/15 confirmations. Its seven manifest file hashes were checked and the coefficients independently recalculated over 719 characters and 27 matching spans. The administrative seed layer equals both human layers. Separate submissions are documented; blind raw-text coding is not established by those files.

QA150 nominal Krippendorff alpha is 0.8826, calculated over 5,990 unambiguous positions. Exact span sets agree on 101/150 sentences. Two conflicting-type positions are excluded from the character calculation, while all original spans remain in span F1. Raw human exports for these recent checks were supplied to the authors' revision workspace; this documentation update publishes the summary, not those private exports.

The nested 15 records add no unique sentences. Human reference construction and the two original review samples cover 350 sentences; the new non-overlapping QA150 raises coverage to 500. These designs do not form a common before/after reliability experiment.
