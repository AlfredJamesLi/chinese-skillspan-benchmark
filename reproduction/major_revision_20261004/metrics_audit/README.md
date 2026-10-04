# Source-group uncertainty and macro-F1 sensitivity

Run `python reproduce_cluster_bootstrap.py` with Python 3 and NumPy. Keep `sentence_counts.csv` and `cluster_bootstrap_and_macro_public.json` in the same directory. No recruitment text or API access is needed.

The script recomputes exact micro-F1 and paired percentile intervals from accepted-span counts. It samples 61 complete source-ID groups with replacement for each of 10,000 draws, using the same draw for all fixed models and training seeds. It checks the reported pointwise intervals and supplies wider Bonferroni sensitivity intervals for the six displayed comparisons. It also verifies K/S/T macro-F1 means and sample SD from the per-type counts in the result file.

These calculations preserve the historical predictions and reference labels. Group resampling does not remove reference use during guideline development, change training inputs, or produce an independent model test. The original sentence-level exclusion checks and the later source-group overlap checks concern different units.

Input hashes and package-relative artifact paths identify the archived files. `cluster_reproduction_check.json` records a successful local reproduction. No unpublished human subtype annotations are included.
