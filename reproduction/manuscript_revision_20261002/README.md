# Chinese-SkillSpan: current manuscript

**Chinese-SkillSpan: a benchmark for competency span extraction in Chinese job advertisements**

[Read the current PDF](Chinese_SkillSpan_revised_20261002.pdf). Updated 5 October 2026; 41 pages. Existing directory and PDF filenames remain stable for links.

This revision uses descriptive names for the source corpus, human reference, Silver supervision, and review/agreement samples. [The resource naming guide](../../docs/terminology.md) distinguishes the original Silver candidate pool, model-specific training/development sets, and overlapping expanded pools. Archived identifiers and data remain unchanged.

The main results retain the current JobBERT baseline and the matched Qwen adaptation comparison. The historical JobBERT label-version comparison, which changes both training and development labels, is retained in Appendix C and [supplementary documentation](../experimental_notes/jobbert_label_versions.md).

[Figure 1 SVG](source/figures/Figure1_drawio_restored_20261004.svg) · [Figure 2 SVG](source/figures/Figure2_drawio_restored_20261004.svg) · [Annotation-profile SVG](source/figures/benchmark_profile.svg)

Figure 3 now labels the Qwen/encoder supervision as Silver train/dev. Its underlying counts, statistical summaries, and graphic layout are unchanged. No dataset labels, predictions, scores, or checkpoints were modified.

The source mirror includes the active LaTeX files, bibliography, class, and figure assets. It requires XeLaTeX and the Noto CJK fonts named in `source/0main.tex`; font binaries are not bundled here. The Overleaf project provides the complete working build. `manifest.json` records this source/PDF revision and local compilation checks; older unused source files and historical revision notes remain archived.

The [reviewer-supplement analysis](../reviewer_supplement_20261004/README.md) and [data/statistical checks](../major_revision_20261004/README.md) document source-document overlaps and the scope of sentence-exclusion checks. The [blinded agreement release](../agreement/finalguide_abc_20261003/README.md) preserves independent individual labels with self-review allowed; these are not consensus model-test labels.
