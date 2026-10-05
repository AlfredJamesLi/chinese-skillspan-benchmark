# Chinese-SkillSpan: current manuscript

**Chinese-SkillSpan: a benchmark for competency span extraction in Chinese job advertisements**

[Read the current PDF](Chinese_SkillSpan_revised_20261002.pdf). Updated 5 October 2026; 41 pages. Existing directory and PDF filenames remain stable for links.

The manuscript uses descriptive names for the source corpus, human reference, Silver supervision, and review/agreement samples. [The resource naming guide](../../docs/terminology.md) distinguishes the original Silver candidate pool, model-specific training/development sets, and overlapping expanded pools. Archived identifiers and data remain unchanged.

The main results retain the current JobBERT baseline and the matched Qwen adaptation comparison. The historical JobBERT label-version comparison, which changes both training and development labels, is retained in Appendix C and [supplementary documentation](../experimental_notes/jobbert_label_versions.md).

[Figure 1 SVG](source/figures/Figure1_drawio_restored_20261004.svg) · [Figure 2 SVG](source/figures/Figure2_drawio_restored_20261004.svg) · [Figure 3 SVG](source/figures/benchmark_profile.svg)

Figure 3 preserves the sentence- and span-length panels and adds the complete adopted Expanded Silver pool to the competency-composition panel: 9,540 records, 21,101 spans, and 2,492 records with empty annotations (26.1%). Additional-review type distributions and the expanded train/validation/test counts appear in Appendix B. The [figure reproduction package](../benchmark_profile/README.md) supplies aggregate JSON/CSV statistics and plotting code. These groups overlap; their counts are not additive.

The Data Availability statement and Appendix D link the current [Chinese encoder audit archive](https://doi.org/10.5281/zenodo.22942441). Dataset labels, predictions, scores, and checkpoints remain unchanged.

The source mirror includes the active LaTeX files, bibliography, class, and figure assets. It requires XeLaTeX and the Noto CJK fonts named in `source/0main.tex`; font binaries are not bundled here. The Overleaf project provides the complete working build. `manifest.json` records the Overleaf source revision, PDF/source hashes, and compilation verification; older revision notes remain available as historical records.

The [reviewer-supplement analysis](../reviewer_supplement_20261004/README.md) and [data/statistical checks](../major_revision_20261004/README.md) document source-document overlaps and the scope of sentence-exclusion checks. The [blinded agreement release](../agreement/finalguide_abc_20261003/README.md) preserves independent individual labels with self-review allowed; those layers support annotation-agreement analysis.

The submission revision adds annotator backgrounds and their handbook-development roles, documents the two preserved agreement-export stages, and clarifies confidential access to the complete expanded pools. Figure captions identify drawing assistance, and the frozen prompt archive and Qwen patience unit are explicit. Scientific scores and frozen labels are unchanged.

The model-name audit verifies vendor display names against official documentation while preserving recorded request/response identifiers, access routes and frozen experiment results. Figure 5 now uses reference-span terminology and explicit seed labels. Table headings distinguish encoders trained with Chinese supervision and candidate versus retained record counts. All 21 tables and five figures were checked after compilation. See the [model-name mapping](../../PAPER_NAMES.md).

The October 5 reviewer revision reconciles human annotation and review coverage (550 distinct sentences), adds a post hoc comparison of final Silver labels with three blinded annotation layers on 49 retained sentences, and moves detailed completion diagnostics and preparation history to the [revision evidence](../reviewer_revision_20261005/README.md). Original model predictions and scores are unchanged.

The subsequent prose revision consolidates AI-use disclosure in the methods, shortens repeated qualifications, and reports the main findings in a 192-word abstract. Calculation chronology and a bibliography/DOI audit are provided in the [prose revision documentation](../style_revision_20261005/README.md). The current manuscript has 41 pages, 21 tables and five figures. No experiment scores, labels, predictions or model settings changed.
