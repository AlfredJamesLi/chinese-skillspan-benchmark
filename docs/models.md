# JobBERT model guide

| Manuscript name | Hugging Face repository | Purpose |
|---|---|---|
| JobBERT-zh initialization | [jobbert-zh](https://huggingface.co/AlfredJames/jobbert-zh) | Domain-adapted encoder and inherited CRF checkpoint |
| Silver-trained JobBERT-zh + CRF | [jobbert-zh-v6a](https://huggingface.co/AlfredJames/jobbert-zh-v6a) | Continuation evaluated on the 150-sentence human reference |

Keep these model IDs when downloading. The display names explain their roles; they do not rename the repositories or weights.

## Loading

The model packages combine an encoder with a custom CRF module. Loading the encoder alone does not reproduce span extraction. The cards provide the custom class and checkpoint-loading instructions; these are not standard `AutoModelForTokenClassification` exports. The continuation's default `crf/best.pt` is seed 42; the three-seed mean is a reported statistic, not a separate checkpoint.

## Result scope

The initialization model's historical 0.4331 result uses the hybrid 2,601-record protocol with span alignment. The Silver-trained continuation's 0.5536 ± 0.0054 result uses the human reference and seeds 42/43/44. Their evaluation targets differ.

## Training-record clarification

The current manuscript reports Silver training/development sets of 2,156/169 records for JobBERT; the downloadable `v6a_nocross` data contain 2,150/169 records for Qwen and the encoder comparison. The training-file aliases and the [historical label-version comparison](../reproduction/experimental_notes/jobbert_label_versions.md) are documented separately. Exact training-file binding should be verified from the original run manifest before treating the downloadable Qwen split as the JobBERT training input. This guide does not change a checkpoint or infer a missing training history.

Qwen's pretrained model is `Qwen/Qwen2.5-14B-Instruct`. Project LoRA adapters are available in the [Qwen model-reproduction archive](https://doi.org/10.5281/zenodo.22851581). Download `CNSS_Qwen_Reproduction.zip` and start with its `README.md` and `MODEL_INDEX.csv`. The package contains the three Qwen LoRA seeds trained on the 2,150/169 Silver sets, two expanded-pool checkpoints and four supplementary adapters, with loading configurations, prompts, parser, frozen predictions and scoring commands. Base-model weights and complete expanded-Silver training texts are not included. Base-model provenance is recorded through local snapshot file hashes; no unrecorded Hub revision is asserted. Component-specific terms are in `LICENSE_NOTICE.md`. See [data access](../DATA_AVAILABILITY.md) and [evaluation instructions](../reproduction/EVALUATION_ENTRY.md).
