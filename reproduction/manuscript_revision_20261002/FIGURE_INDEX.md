# Current manuscript figure index

This index follows the Overleaf manuscript synchronized on 7 October 2026.
The current manuscript contains eight figures. Existing filenames are retained
to preserve links; their embedded numbers or dates are not the current figure
numbers. The manuscript version and file checksums are recorded in this
directory's manifest.

| Figure | Content | Manuscript asset | Editable source or generation input |
| --- | --- | --- | --- |
| 1 | Study overview | [PDF](source/figures/Figure1_drawio_restored_20261004.pdf) | [draw.io](source/figures/Figure1_drawio_restored_20261004.drawio), [SVG](source/figures/Figure1_drawio_restored_20261004.svg) |
| 2 | Bilingual annotation examples | [PDF](source/figures/annotation_examples_main_20261006.pdf) | [Renderer](source/figures/generate_corpus_examples_20261003.py), [Chinese spans and English alignments](source/figures/annotation_examples_corpus_20261003.json); use `--selection main` |
| 3 | Human-reference construction, assisted annotation, and blinded agreement study | [PDF](source/figures/Figure2_drawio_restored_20261004.pdf) | [draw.io](source/figures/Figure2_drawio_restored_20261004.drawio), [SVG](source/figures/Figure2_drawio_restored_20261004.svg) |
| 4 | Dataset profile | [PDF](source/figures/benchmark_profile_main_20261006.pdf) | [SVG](source/figures/benchmark_profile_main_20261006.svg), [renderer and aggregate inputs](../benchmark_profile/README.md); use `--main-only` |
| 5 | Human-reference model comparison | [PDF](source/figures/model_comparison_20261006.pdf) | [SVG](source/figures/model_comparison_20261006.svg), [renderer and summary scores](../model_comparison_20261006/README.md) |
| 6 | Qwen extraction diagnostics | [PDF](source/figures/qwen_diagnostics_chart_0913.pdf) | [SVG](source/figures/qwen_diagnostics_chart_0913.svg), [archived counts and chart data](../qwen_diagnostics/README.md) |
| 7 | Additional bilingual annotation examples | [PDF](source/figures/annotation_examples_additional_20261006.pdf) | [Renderer](source/figures/generate_corpus_examples_20261003.py), [Chinese spans and English alignments](source/figures/annotation_examples_corpus_20261003.json); use `--selection additional` |
| 8 | Length distributions in the additional assisted-review sample | [PDF](source/figures/additional_review_profile_20261006.pdf) | [SVG](source/figures/additional_review_profile_20261006.svg), [renderer and aggregate inputs](../benchmark_profile/README.md); use `--review-only` |

## Bilingual examples

Figures 2 and 7 pair frozen Chinese annotations with English translation
alignments. The English highlights correspond one-to-one to Chinese spans and
preserve their L/K/S/T types; they are display alignments, not independently
annotated English evaluation labels. Original advertisement list numbers are
omitted in the illustration, while the source texts and offsets remain in the
JSON. Only the five already released reference examples are included.

With Python and ReportLab installed, run from the repository root:

```sh
python reproduction/manuscript_revision_20261002/source/figures/generate_corpus_examples_20261003.py --selection main --output output/annotation_examples_main_20261006.pdf
python reproduction/manuscript_revision_20261002/source/figures/generate_corpus_examples_20261003.py --selection additional --output output/annotation_examples_additional_20261006.pdf
```

The renderer defaults to Windows SimSun and Arial fonts. On other systems,
set `CNSS_CN_FONT`, `CNSS_EN_FONT`, and `CNSS_EN_BOLD` to locally installed
TrueType fonts with the required Chinese/English coverage. Fonts are not
distributed here, and substitutions can change line wrapping. The saved PDFs
preserve the manuscript layout. Optional `--layout-report <path>` writes the
alignment and clipping-check output.

## Diagram and statistical sources

Figures 1 and 3 can be edited in draw.io using the linked `.drawio` files or in
a vector editor using the SVGs. Figure 3 retains the historical filename
`Figure2_drawio_restored_20261004`; this does not indicate its current number.

The benchmark-profile renderer now has explicit options for current Figures 4
and 8. Its default invocation still produces the earlier combined layout for
compatibility. The linked reproduction notes distinguish these outputs.

Figure 5 uses the manuscript's saved, three-decimal summary scores. Error bars
are sample standard deviations across three training seeds where available;
the single-run panel has no between-seed uncertainty estimate. Figure 6's
editable SVG and saved counts are supplied; this index does not claim that an
exact-layout rendering script for that archived chart has been identified.

These drawing commands do not rerun model inference, alter annotations, or
recalculate evaluation scores. Older figure numbers in dated archives refer
to those manuscript versions.
