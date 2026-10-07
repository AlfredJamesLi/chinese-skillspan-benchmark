# Human-reference model comparison (Figure 5)

This figure summarizes typed exact-span micro-F1 on the same 150-sentence Chinese-SkillSpan human reference set. It combines six prompted configurations with four Silver-supervised models in separate panels. The panels share a zero-based 0–1 axis.

## Data and interpretation

`model_comparison_data.json` transcribes the three-decimal values displayed in the manuscript. The plotting coordinates and value labels use that display precision; this figure performs no rescoring, rounding-based inference, or recomputation of uncertainty. Each model entry identifies its source file and result entry.

| Result group | Source in the current manuscript mirror | Values used |
| --- | --- | --- |
| Six prompted configurations | [tex/stage2_result_values.tex](../manuscript_revision_20261002/source/tex/stage2_result_values.tex), `SharedResultRows` | Typed exact-span micro-F1 |
| Qwen + LoRA | [tex/stage2_result_values.tex](../manuscript_revision_20261002/source/tex/stage2_result_values.tex), `QwenLoraExact`; [tex/silver_plus_results.tex](../manuscript_revision_20261002/source/tex/silver_plus_results.tex) | Mean 0.540, sample SD 0.035 |
| JobBERT-zh + CRF | [tex/silver_plus_results.tex](../manuscript_revision_20261002/source/tex/silver_plus_results.tex), Silver-trained JobBERT baseline | Mean 0.554, sample SD 0.005 |
| ESCOXLM-R and XLM-R-large | [tex/external_benchmarks/paper_tables_main.tex](../manuscript_revision_20261002/source/tex/external_benchmarks/paper_tables_main.tex), overall F1 panel | Means 0.538 / 0.522; sample SDs 0.021 / 0.022 |

Panel (a) contains single runs. Their `sample_sd` is `null`, which means that a between-seed standard deviation is unavailable. Panel (b) shows means and sample standard deviations across training seeds 42, 43, and 44. Its error bars are one sample SD on either side of the mean, not confidence intervals or significance tests. Models are ordered by the reported score within each panel.

The comparison is descriptive because training and inference protocols differ across model families. In particular, the JobBERT supervision split contains 2,156 training records, whereas Qwen and the compared multilingual encoders use 2,150; the development sets contain 169 records. The fixed-inference Qwen comparison is explained separately in the manuscript. A restrained accent identifies the Chinese JobBERT baseline without asserting statistical superiority.

All displayed scores are from the Chinese human-reference evaluation. No English or Danish external-task scores are included. Model names follow the evaluated configurations documented in the manuscript.

## Rebuild

From the repository root, with Python and Matplotlib installed:

```text
python reproduction/model_comparison_20261006/plot_model_comparison.py --output-dir output/model_comparison
```

Outputs are editable vector assets:

- `output/model_comparison/model_comparison_20261006.pdf`
- `output/model_comparison/model_comparison_20261006.svg`

To also save a PNG preview and a layout audit, supply `--qa-dir <output-directory>`. The PDF embeds TrueType fonts, and the SVG preserves text as text. The figure is 8.2 × 4.1 inches. Numerical data, axis limits, uncertainty types, and non-clipping checks are validated during generation.

The [current figure index](../manuscript_revision_20261002/FIGURE_INDEX.md) links to the archived manuscript PDF and SVG. Rebuilding uses the saved summary values and makes no model calls or changes to evaluation outputs.
