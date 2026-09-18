# Chinese-SkillSpan

A benchmark for extracting competency spans from Chinese job advertisements, with annotation guidelines, Silver supervision, a human reference set, and evaluation tools.

**[Data and access](DATA_AVAILABILITY.md) · [Reproduce results](REPRODUCIBILITY.md) · [Models](docs/models.md) · [Paper-to-file index](reproduction/PAPER_INDEX.md)**

![Chinese-SkillSpan workflow](figures/round2/workflow.png)

## What is included?

| Component | Size | Use |
|---|---:|---|
| Original corpus | 22,840 sentences | Four recruitment collections |
| Human reference | 150 sentences, 663 spans | Evaluation against human annotations |
| Original Silver-plus pool | 2,451 records | LLM-generated labels |
| Released Qwen B2 split | 2,150 training / 169 development | Matched Qwen adaptation study |
| Expanded Codex pool | 9,540 retained sentences | Later experiment; final partitions are not fully released |
| Human coding and review | 500 unique sentences | Reference construction and quality checks; not 500 Gold test sentences |

Terminology follows the [annotation and training guide](docs/terminology.md). Manuscript numbers follow the [display-precision policy](docs/numerical_precision.md); source result files retain their original precision.

The task uses flat character spans with four types: language (L), knowledge (K), occupational skills (S), and transversal competences (T). The categories are ESCO-informed; the task does not assign ESCO concept IDs.

## Get started

1. **Use the data:** download the [v0.1.3 archive](https://doi.org/10.5281/zenodo.22698504), then read the [human-reference guide](data/gold150/README.md) and [annotation handbook](notes/handbooks/handbook_B_sop_v4.md).
2. **Inspect results:** open the [paper-to-file index](reproduction/PAPER_INDEX.md). It separates shared-guideline inference, supervised adaptation, and expanded-Silver experiments.
3. **Reproduce a score:** follow the [evaluation guide](reproduction/EVALUATION_ENTRY.md) with the matching protocol and saved predictions.
4. **Use a model:** see the [JobBERT model guide](docs/models.md). The encoder and CRF checkpoint have separate loading requirements.

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
| All archive versions | [Zenodo concept DOI](https://doi.org/10.5281/zenodo.22288337) |
| JobBERT-zh initialization | [Hugging Face model](https://huggingface.co/AlfredJames/jobbert-zh) |
| JobBERT-zh B2 continuation | [Hugging Face model](https://huggingface.co/AlfredJames/jobbert-zh-v6a) |

The archive covers the earlier released benchmark components. Later expansion materials on GitHub are partial; complete expanded partitions and Qwen adapters are not supplied. [Availability and licensing](DATA_AVAILABILITY.md) describes what readers can obtain and reuse.

## Citation

Use the metadata in [CITATION.cff](CITATION.cff) and cite [Zenodo v0.1.3](https://doi.org/10.5281/zenodo.22698504) for that archived dataset version. The manuscript is maintained separately on Overleaf; this repository does not distribute a draft PDF.

Related English resource: Zhang et al. (2022), [SkillSpan](https://aclanthology.org/2022.naacl-main.366/).

## Responsible use

This resource supports analysis of recruitment text, not measurement or profiling of individual applicants. The selected human reference is not a random population sample. Source wording has separate reuse conditions from the software; see [LICENSE](LICENSE) and [data access](DATA_AVAILABILITY.md).

Supported by the National Social Science Fund of China, Grant No. 21BGL142.
