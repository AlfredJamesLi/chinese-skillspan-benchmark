# Chinese-SkillSpan

[Annotation roles and IAA50 membership](reproduction/reviewer_supplement_20261004/README.md) clarify which results use human references and which use generated targets.

The [4 October revision and checks](reproduction/major_revision_20261004/README.md) update the current manuscript, data accounting, source-document analysis and uncertainty estimates. Earlier experiments remain archived.

A benchmark for competency span extraction in Chinese job advertisements, with annotation guidelines, Silver supervision, a human reference set, and evaluation tools.

Current manuscript: **Chinese-SkillSpan: a benchmark for competency span extraction in Chinese job advertisements**. [Read the manuscript and revision notes](reproduction/manuscript_revision_20261002/README.md).

**[Data and access](DATA_AVAILABILITY.md) · [Reproduce results](REPRODUCIBILITY.md) · [Models](docs/models.md) · [Paper-to-file index](reproduction/PAPER_INDEX.md)**

![Chinese-SkillSpan workflow](reproduction/manuscript_revision_20261002/source/image/chinese-skillspan-workflow-neutral-icons-20261004.png)

## What is included?

| Component | Size | Use |
|---|---:|---|
| Original corpus | 22,840 sentences | Four recruitment collections |
| Human reference | 150 sentences, 663 spans | Frozen targets used in guideline development; diagnostic model evaluation |
| Original Silver-plus pool | 2,451 records | LLM-generated labels |
| Released Qwen B2 split | 2,150 training / 169 development | Matched Qwen adaptation study |
| Adopted expanded Codex pool | 9,540 retained sentences | Final adopted expansion; complete partitions are not publicly released |
| Historical human coding and review | 500 unique sentences | Reference construction and quality checks; not 500 Gold test sentences |
| Independent blinded agreement study | 50 sentences; three annotators | Final-handbook agreement; separate from historical coverage and not a model test set |

Terminology follows the [annotation and training guide](docs/terminology.md). Manuscript numbers follow the [display-precision policy](docs/numerical_precision.md); source result files retain their original precision.

The task uses flat character spans with four types: language (L), knowledge-related requirements (K), occupational skills (S), and transversal competencies (T). The categories are ESCO-informed; the task does not assign ESCO concept IDs.

The authors confirm that the adopted Silver labels were generated through official OpenAI Codex, with the original teacher recorded as `gpt-6-astra`. The alternative expanded annotation pool is retained only for supplementary comparison. DeepSeek and Kimi used official provider APIs. API baseline predictions were evaluated under a frozen protocol and checked by offline rescoring; recorded identifiers and access routes are listed in the [resource naming guide](PAPER_NAMES.md).

## Get started

1. **Use the data:** download the [v0.1.3 archive](https://doi.org/10.5281/zenodo.22698504), then read the [human-reference guide](data/gold150/README.md) and [annotation handbook](notes/handbooks/handbook_B_sop_v4.md).
2. **Inspect results:** open the [paper-to-file index](reproduction/PAPER_INDEX.md). It separates shared-guideline inference, supervised adaptation, and expanded-Silver experiments.
3. **Reproduce a score:** follow the [evaluation guide](reproduction/EVALUATION_ENTRY.md) with the matching protocol and saved predictions.
4. **Use a model:** see the [model guide](docs/models.md). The encoder and CRF checkpoint have separate loading requirements.

## Main fine-tuning comparisons

| Study | Comparison | Typed exact F1 on the human reference |
|---|---|---:|
| Qwen adaptation | No adapter → B2 LoRA | 0.3612 → 0.5403 ± 0.0354 |
| JobBERT supervision and selection | Earlier labels → revised labels | 0.1422 ± 0.0138 → 0.5536 ± 0.0054 |

Training summaries are means and sample standard deviations across seeds 42, 43, and 44. These are two different experimental designs. Expanded-pool results and their access requirements are listed in the [expanded-study guide](reproduction/expanded_silver/README.md).

## Downloads and models

| Resource | Entry |
|---|---|
| Versioned data archive | [Zenodo v0.1.3](https://doi.org/10.5281/zenodo.22698504) |
| Qwen LoRA adapters and frozen predictions | [Qwen model-reproduction archive](https://doi.org/10.5281/zenodo.22851581) |
| All dataset archive versions | [Zenodo concept DOI](https://doi.org/10.5281/zenodo.22288337) |
| JobBERT-zh initialization | [Hugging Face model](https://huggingface.co/AlfredJames/jobbert-zh) |
| JobBERT-zh B2 continuation | [Hugging Face model](https://huggingface.co/AlfredJames/jobbert-zh-v6a) |

The archive covers the earlier released benchmark components. Later expansion materials on GitHub are partial; complete expanded training partitions are not supplied. Qwen adapters and frozen predictions are available in the separate model-reproduction archive. [Availability and licensing](DATA_AVAILABILITY.md) describes what readers can obtain and reuse.

## Citation

Use the metadata in [CITATION.cff](CITATION.cff) and cite [Zenodo v0.1.3](https://doi.org/10.5281/zenodo.22698504) for that archived dataset version. This citation identifies the archived dataset version, whose release title is retained. The current manuscript title, PDF, and source revision are available in the [manuscript directory](reproduction/manuscript_revision_20261002/README.md).

Related English resource: Zhang et al. (2022), [SkillSpan](https://aclanthology.org/2022.naacl-main.366/).

## Responsible use

This resource supports analysis of recruitment text, not measurement or profiling of individual applicants. The selected human reference is not a random population sample. Source wording has separate reuse conditions from the software; see [LICENSE](LICENSE) and [data access](DATA_AVAILABILITY.md).

Supported by the National Social Science Fund of China, Grant No. 21BGL142.

Data provenance: [data sources and collection](docs/data_sources.md).
