# Abstract Results revision — 3 October 2026

The abstract now leads with the measured benefit of Silver-supervised Qwen adaptation on the fixed human reference. It reports the no-adapter score of 0.361 and the adapted mean of 0.540 ± 0.035 (sample standard deviation over three training seeds). The baseline remains a single run. The following sentence reports the increase in exact recall in every assessed span-length group for each adapted model.

The independent blinded annotation study is summarized by its finding that boundary-only agreement exceeds typed-span agreement. Its full coefficients and confidence intervals remain in the main annotation-quality section. The secondary ESCO-initialization comparison also remains in the manuscript; it is no longer listed in the abstract.

This edit changes only the abstract Results paragraph. The title, contribution statements, numerical results in the body, and the abstract's qualification about development-used reference data are preserved. No claim of universally high annotation reliability or generalization to unseen advertisements is added.

## Evidence

- `source/tex/silver_plus_results.tex` and `source/tex/stage2_result_values.tex`: Qwen adaptation scores and their seed-summary definition.
- `source/3Experiments.tex`: exact-recall improvements in all reported span-length groups.
- `source/tex/annotation_quality_R12.tex`: typed-span and boundary-only agreement, with full uncertainty estimates.

The revised manuscript compiles to 40 pages. The first page was rendered and visually inspected: the complete abstract fits on the page, with no clipping. Extracted text on pages 2–40 is unchanged apart from continuous review line numbers. The local revision folder retains a complete source archive and the previous master file and PDF.
