# Manuscript revision: annotation workflow and presentation

The [3 October review integration](review_integration_20261003/README.md) records decisions on 48 references and 58 writing suggestions, including evidence limits.

The abstract now leads with the measured Qwen adaptation result and span-length diagnostics; see the [3 October Results revision](abstract_results_focus_20261003/README.md).

Current title: *Chinese-SkillSpan: a benchmark for competency span extraction in Chinese job advertisements*.

The introduction clarifies competency-span terminology across L/K/S/T; see the [3 October terminology update](competency_terminology_20261003/README.md).

This 39-page version implements the supervisor's presentation comments and describes independent blinded annotation by three coders. [Read the revised PDF](Chinese_SkillSpan_revised_20261002.pdf).

The abstract leads with the measured Qwen adaptation result. Chinese examples are paired with English explanations in the main-text example figure, and section openings state the purpose of each analysis. Figure 2 retains the existing illustration style and adds the separate agreement study. The main agreement table presents the formal 50-sentence results; historical coding and assisted review remain in Appendix B. The data-layer and access tables, conclusions, and cross-references have been updated.

The coders could see neither machine suggestions nor one another's annotations. Five familiarization and 15 training sentences are excluded from the formal 50. Agreement uses the preserved pre-discussion labels. The random draw is confirmed by the authors; the available exports establish sample membership and source counts but do not include the complete candidate frame or execution log. Bootstrap stratification is an analysis procedure, not proof of the original draw method.

The formal 50 are not added to Gold150 and are not a model test set. Historical coverage remains 500 sentences; no unverified combined total is reported. Model scores, agreement estimates, equations, and citation keys were retained. The frozen [agreement release](../agreement/finalguide_abc_20261002/README.md) is unchanged.

[Editable Figure 2](source/figures/Figure2_illustrated.svg) · [Vector PDF](source/figures/Figure2_illustrated.pdf) · [Chinese change log](CHANGELOG_zh.md)

The `source` directory contains changed manuscript files and figure assets, not a standalone complete LaTeX project. Full before/after project backups were retained with the local delivery. The hash manifest identifies this PDF and the published files.

The [title-alignment update](title_benchmark_alignment_20261003/README.md) aligns the abstract, introduction, conclusion, Table 1, PDF metadata, and repository entry points. Table 1 summarizes annotation layers; Table 2 retains the detailed counts and data roles.

The [paragraph-layout revision](short_line_polish_20261003/README.md) removes conspicuously short prose endings through wording changes. Experimental values, equations, references, and annotation-rule meanings are retained.

The 4 October update uses GPT (API) and Claude (API) as display names, identifies the adopted Codex expansion and supplementary alternative, and preserves access metadata in Appendix C. Experimental values are unchanged. The current PDF also retains the page-10 paragraph and page-27 float-layout corrections.

## Current table and figure positions

Figure 4 now shows five traceable original corpus records with all four L/K/S/T types. It replaces the short handbook illustrations. Source IDs, excerpt ranges and preserved historical labels are documented in [the provenance note](corpus_examples_20261003/README.md).

| Item | PDF page | Source label |

|---|---:|---|

| Table 1 | 3 | `tab:related-span` |

| Figure 1 | 5 | `fig:macro-micro` |

| Figure 2 | 6 | `fig:coding-detail` |

| Figure 3 | 9 | `fig:length-distributions-r40` |

| Table 2 | 7 | `tab:annotation-lineage` |

| Figure 4 | 10 | `fig:illustrative-annotations` |

| Table 3 | 11 | `tab:quality-main` |

| Table 4 | 13 | `tab:training-settings` |

| Table 5 | 15 | `tab:gold150-shared-r7` |

| Table 6 | 15 | `tab:core-paired` |

| Table 7 | 16 | `tab:gold150-main` |

| Table 8 | 17 | `tab:external-chinese` |

| Table 9 | 17 | `tab:external-common` |

| Table 10 | 20 | `tab:guide-types` |

| Table 11 | 20 | `tab:guide-boundaries` |

| Table 12 | 21 | `tab:guide-scope` |

| Table 13 | 24 | `tab:qa150-pairs` |

| Table 14 | 26 | `tab:model-identity` |

| Figure 5 | 28 | `fig:qwen-diagnostics` |

| Table 15 | 28 | `tab:expanded-silver-main` |

| Table 16 | 30 | `tab:component-access` |

| Table 17 | 31 | `tab:source-stages` |

| Table 18 | 33 | `tab:external-common-ci` |

| Table 19 | 33 | `tab:external-native` |

| Table 20 | 33 | `tab:external-gnehm` |

| Table 21 | 34 | `tab:external-kompetencer-classification` |

| Table 22 | 35 | `tab:external-nnose` |

