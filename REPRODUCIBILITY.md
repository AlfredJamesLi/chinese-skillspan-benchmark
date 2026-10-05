# Reproduce Chinese-SkillSpan results

[Annotation roles and blinded-sample membership](reproduction/reviewer_supplement_20261004/README.md) clarify which results use human references and which use generated targets.

The [4 October revision and checks](reproduction/major_revision_20261004/README.md) update the current manuscript, data accounting, source-document analysis and uncertainty estimates. Earlier experiments remain archived.

Choose the task below. Each guide uses the same descriptive names as the manuscript; exact file names are listed only where needed to run a command or identify a result.

| Task | Start here | What it establishes |
|---|---|---|
| Inspect paper results | [Paper-to-file index](reproduction/PAPER_INDEX.md) | Published values and their experimental context |
| Check companion files | Command below | File checksums, counts, arithmetic, and links |
| Score saved predictions | [Evaluation guide](reproduction/EVALUATION_ENTRY.md) | Scores from compatible prediction files |
| Rerun training or inference | [Model guide](docs/models.md), [access matrix](DATA_AVAILABILITY.md) | Requires the corresponding data, model artifacts, and configuration |

From the repository root:

```bash
python reproduction/verify_companion.py
```

This check uses Python's standard library. It makes no model call, performs no training, and does not regenerate predictions.

## Qwen adapters and frozen predictions

Download the [Qwen model-reproduction archive](https://doi.org/10.5281/zenodo.22851581) and follow the included `README.md`. `MODEL_INDEX.csv` maps the three Qwen LoRA seeds trained on the 2,150/169 Silver sets and the selected expanded-pool adapters to checkpoints and predictions. The archive includes loading configurations, frozen prompts, the occurrence parser, human reference set, scoring tools and an offline-scoring receipt. It excludes base-model weights and complete expanded training texts. The shared-guideline package does not replace the historical JSON-offset experiment.

## Match the experiment

- **Shared-guideline inference:** six configurations evaluated on the 150-sentence human reference.
- **Matched Qwen adaptation:** 2,150/169 Silver training/development records; no adapter versus three LoRA seeds under the same inference protocol.
- **Silver-trained JobBERT-zh + CRF:** 2,156/169 training/development records. The [historical label-version comparison](reproduction/experimental_notes/jobbert_label_versions.md) uses matched texts with different training and development labels. The publicly released 2,150-row Qwen file is not that 2,156-row manifest.
- **Expanded Silver pools:** the adopted Codex pool and a supplementary alternative pool, with separate Qwen Silver testing and an additional human-reference check. See [expanded experiments](reproduction/expanded_silver/README.md).
- **Historical protocols:** [historical results](reproduction/historical_results/README.md) retain the earlier JSON-offset and hybrid-reference studies.

The [resource naming guide](PAPER_NAMES.md) and [file inventory](reproduction/evaluation/materials_inventory.json) resolve original identifiers. The inventory records an earlier audit, not a complete inventory of subsequent releases. The [access matrix](DATA_AVAILABILITY.md) states the current release scope.

## Supporting analyses

[Coding agreement](reproduction/agreement/README.md) · [Qwen diagnostics](reproduction/qwen_diagnostics/README.md) · [Output outcomes](reproduction/output_outcomes/README.md) · [Supplementary tables](reproduction/supplementary_tables/README.md) · [Experimental details](reproduction/experimental_notes/README.md)

Frozen data, prediction, parser, and scorer paths retain their original names. This keeps existing commands and archived checksums usable.

## Recreate Figure 3

The [annotation-profile reproduction guide](reproduction/benchmark_profile/README.md) provides exact aggregate counts, source-file hashes, the plotting script, and a pinned plotting environment. No recruitment text or model inference is needed to reconstruct this descriptive figure.
