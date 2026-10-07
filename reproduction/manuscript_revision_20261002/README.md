# Chinese-SkillSpan: current manuscript

**Chinese-SkillSpan: a benchmark for competency span extraction in Chinese job advertisements**

[Read the manuscript](Chinese_SkillSpan_revised_20261002.pdf). Updated 7 October 2026: **41 pages, 8 figures, and 24 tables**. The PDF and active sources match Overleaf revision `b84d27e529c91ba85d4aa95c32799c8cdd4ab76c`. The dated directory and PDF filenames are retained so that existing links continue to work; [manifest.json](manifest.json) identifies the actual source revision and file checksums.

An [earlier preprint](https://arxiv.org/abs/2604.23009v1) describes an earlier stage of this work. The present manuscript substantially revises the resource definitions, annotation procedures, and evaluation.

## Figures, tables, and study materials

The [figure index](FIGURE_INDEX.md) maps all eight current figures to their final assets, editable sources, and generation instructions. Figure 2 presents aligned Chinese and English annotation examples; Figure 3 describes the annotation process; Figure 4 presents dataset characteristics; and Figure 5 compares model results on the human reference. Additional examples and review-sample distributions appear in Figures 7 and 8. Table numbers and stable LaTeX labels are listed in the [paper-to-file index](../PAPER_INDEX.md).

The [annotation-stage documentation](../annotation_documentation_20261007/README.md) explains reference construction and handbook use. Human annotation and review cover 550 distinct sentences, including the separate 50-sentence blinded study. The [7 October bilingual handbook](../../notes/handbooks/reader_20261007/README.md) supports reading and subsequent annotation; archived study materials remain the basis for reproducing earlier experiments.

Manuscript-preparation assistance is disclosed in Acknowledgements. Funding is reported separately. The [data-access guide](../../DATA_AVAILABILITY.md) describes available components, reuse conditions, and access to complete expanded-pool inputs. Preserved labels, predictions, scoring code, and experimental results are unchanged by this manuscript synchronization.

## Build the manuscript

The `source/` directory contains the active LaTeX inputs, bibliography, bibliography style, class, and figure assets listed in `manifest.json`. Use XeLaTeX, BibTeX, then XeLaTeX twice from that directory. The Noto CJK fonts named in `source/0main.tex` must be supplied in `source/fonts/noto-cjk/`; font binaries are not bundled in this mirror. The Overleaf project includes the working font files. Other retained source files may describe earlier layouts; the manifest identifies the current inputs.

The mirror is checked by compilation with those font dependencies and by comparison with the Overleaf PDF text. [Earlier revision notes](REVISION_HISTORY_20261006.md) retain the preceding editorial history and its original numbering.
