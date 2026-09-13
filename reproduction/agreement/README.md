# Coding agreement: current Table 3 and Appendix B

The available later exports contain 50 paired sentences and 2,571 Unicode code points. Original texts are aligned by source ID; spaces and punctuation remain included. The flat character labels are L/K/S/T/O. In this sample both coders have zero L frequency.

1. Assign each character its coder's span type, or O outside spans.
2. Count the paired labels and each coder's marginal frequencies.
3. Compute observed agreement p_o = 0.7709062621548036.
4. Compute expected agreement p_e = sum_c p_A(c)p_B(c) = 0.4705642521733224.
5. Cohen's kappa = (p_o-p_e)/(1-p_e) = 0.5672869865972949, printed **0.5673**.
6. Independently compare exact typed span sets: 98 matches between 211 Coder A and 230 Coder B spans yield F1 = 196/441 = **0.4444**.

[Calculation data](calculation.json) includes the confusion matrix, marginal counts, input hashes and the optional collapsed-category projection (kappa 0.5916). Matrix orientation is Coder B followed by Coder A. Names in this public summary are display aliases; original input files are unchanged and are not newly published here.

The 2,571 characters are nested in 50 sentences. They are not 2,571 independent sampling units. Byte identity with the initial pre-adjudication freeze remains unresolved. QA100 and its machine-prefilled Dual15 subset are different review designs and receive no independent-coder kappa. This update does not invent Krippendorff's alpha or replace the original category system with the more favorable collapsed score.
