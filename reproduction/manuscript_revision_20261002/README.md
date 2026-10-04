# Chinese-SkillSpan: current manuscript

**Chinese-SkillSpan: a benchmark for competency span extraction in Chinese job advertisements**

[Read the revised PDF](Chinese_SkillSpan_revised_20261002.pdf). The current revision is dated 4 October 2026 and contains 36 pages. The directory and PDF filename are retained so existing links continue to work.

This revision clarifies the original corpus split and subsequent labeled experimental splits, reconciles the Silver-pool counts, and adds source-group bootstrap intervals and K/S/T macro-F1. It uses the latest independent annotation results (typed F1 0.818), replaces the two workflow illustrations with editable vector diagrams, and moves external-task experiments into [separate supplementary materials](../major_revision_20261004/external_experiments/README.md). The benchmark title is retained; conclusions distinguish diagnostic comparison from new-document generalization.

[Data and statistical checks](../major_revision_20261004/README.md) explain the calculations and their scope. The previous leakage checks remain valid: original source-document partitions are disjoint, and later B2 files exclude reference sentences. Different sentences from shared source documents are reported separately.

The independent three-annotator study permits individual self-review with the handbook while hiding model suggestions and peer labels. Its 5 learning and 15 practice sentences are excluded. The 50 formal sentences are not added to Gold150 or used as a model test set. [Labels and agreement code](../agreement/finalguide_abc_20261003/README.md) retain the original exports and author clarification.

[Workflow SVG](source/figures/workflow_major_revision_20261004.svg) · [Annotation paths SVG](source/figures/annotation_paths_major_revision_20261004.svg) · [Historical revision notes](CHANGELOG_zh.md)

The source directory contains the revised manuscript files and figure assets; it is not a complete standalone LaTeX project. Historical files remain archived. The manifest records current file hashes and validation. No labels, model predictions or checkpoint artifacts were changed in this revision.
