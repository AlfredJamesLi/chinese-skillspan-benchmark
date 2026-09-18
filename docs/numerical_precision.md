# Numerical display precision

The manuscript uses three decimal places for precision, recall, F1, agreement coefficients, their reported intermediate quantities, mean ± sample standard deviation, confidence-interval endpoints, and score differences. Descriptive percentages use one decimal place.

Counts remain integers. Exact thresholds and hyperparameters retain their specified values (for example IoU ≥ 0.5, dropout 0.05, and learning rate 2e-5). Model names, software versions, DOI strings, and file identifiers are not numerical results. Plot tick labels use compact scales rather than three-decimal formatting. Confidence levels such as 95% are exact design specifications.

Rounding is a display operation, not a change to annotations or scoring. Machine-readable result files, scorer outputs and frozen snapshots retain their available precision. Means, uncertainty summaries and differences should be computed before display rounding; consequently subtracting two rounded table cells can differ from the displayed difference.

For the shared-guideline result tables, the three-decimal displays use the archived full-precision CSVs. In particular, seed-42 Qwen relaxed F1 is 0.6244579358196011 → **0.624**, not 0.625 obtained by rounding 0.6245 a second time. Other manuscript values use their highest locally documented precision; values available only as four-decimal summaries are rounded from those summaries and are not represented as recovered full-precision scores.

Example: the fifteen-sentence subset has expected agreement 0.5574830596505346, displayed as **0.557**, observed agreement **1.000**, and Cohen's κ **1.000**. QA150 κ and α both display as **0.883**; this does not imply that their unrounded values are identical.

See the [paper index](../reproduction/PAPER_INDEX.md) for source artifacts and [reproduction guide](../REPRODUCIBILITY.md) for evaluation protocols. Historical result tables and snapshots retain their original formatting and numbers.
