# Chinese-SkillSpan model guide

Choose models by their study role below. The eight Hugging Face repositories cover two JobBERT roles and two encoder initializations trained with three seeds each. Qwen adapters are distributed through their separate Zenodo archive.

| Manuscript name | Release | Purpose |
|---|---|---|
| JobBERT-zh initialization | [jobbert-zh](https://huggingface.co/AlfredJames/jobbert-zh) | Domain-adapted encoder and inherited CRF checkpoint |
| Silver-trained JobBERT-zh + CRF | [jobbert-zh-v6a](https://huggingface.co/AlfredJames/jobbert-zh-v6a) | Continuation evaluated on the 150-sentence human reference |
| Silver-trained XLM-R-large | [Seed 42](https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s42) · [Seed 43](https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s43) · [Seed 44](https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s44) | Three trained checkpoints for the Chinese-supervised encoder comparison |
| Silver-trained ESCOXLM-R | [Seed 42](https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s42) · [Seed 43](https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s43) · [Seed 44](https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s44) | Three trained checkpoints for the Chinese-supervised encoder comparison |
| Qwen + LoRA | [Qwen model-reproduction archive](https://doi.org/10.5281/zenodo.22851581) | Adapters, frozen predictions, and loading/scoring materials |

Keep these model IDs when downloading. The repository identifiers preserve the original `table11`, `b2`, and seed labels for existing links and commands. Each seed repository contains a separate trained checkpoint. The [Chinese encoder audit archive](https://doi.org/10.5281/zenodo.22942441) supplies the associated code, configurations, predictions, and model index.

## JobBERT loading

The model packages combine an encoder with a custom CRF module. Loading the encoder alone does not reproduce span extraction. The cards provide the custom class and checkpoint-loading instructions; these are not standard `AutoModelForTokenClassification` exports. The continuation's default `crf/best.pt` is seed 42; the three-seed mean is a reported statistic, not a separate checkpoint.

## JobBERT result scope

The initialization model's historical 0.4331 result uses the hybrid 2,601-record protocol with span alignment. The Silver-trained continuation's 0.5536 ± 0.0054 result uses the human reference and seeds 42/43/44. Their evaluation targets differ.

## Training-record clarification

The current manuscript reports Silver training/development sets of 2,156/169 records for JobBERT; the downloadable `v6a_nocross` data contain 2,150/169 records for Qwen and the encoder comparison. The training-file aliases and the [historical label-version comparison](../reproduction/experimental_notes/jobbert_label_versions.md) are documented separately. Exact training-file binding should be verified from the original run manifest before treating the downloadable Qwen split as the JobBERT training input. This guide does not change a checkpoint or infer a missing training history.

## Chinese-supervised encoder comparison

XLM-R-large and ESCOXLM-R use nine-label BIO token-classification heads and the same 2,150/169 Silver training/development records. Seeds 42, 43, and 44 provide the three runs summarized in the manuscript. The model cards and [evidence guide](../reproduction/evidence_review_20260925/README.md) give the character-to-subword mapping, chunking, and scoring requirements. These encoder checkpoints have their own loading and evaluation protocol, distinct from JobBERT's custom CRF.

## Qwen adapters

Qwen's pretrained model is `Qwen/Qwen2.5-14B-Instruct`. Project LoRA adapters are available in the [Qwen model-reproduction archive](https://doi.org/10.5281/zenodo.22851581). Download `CNSS_Qwen_Reproduction.zip` and start with its `README.md` and `MODEL_INDEX.csv`. The package contains the three Qwen LoRA seeds trained on the 2,150/169 Silver sets, two expanded-pool checkpoints and four supplementary adapters, with loading configurations, prompts, parser, frozen predictions and scoring commands. Base-model weights and complete expanded-Silver training texts are not included. Base-model provenance is recorded through local snapshot file hashes; no unrecorded Hub revision is asserted. Component-specific terms are in `LICENSE_NOTICE.md`. See [data access](../DATA_AVAILABILITY.md) and [evaluation instructions](../reproduction/EVALUATION_ENTRY.md).

<details>
<summary>Historical contrast: JobBERT-zh 1M domain pretraining</summary>

[JobBERT-zh 1M](https://huggingface.co/AlfredJames/jobbert-zh-1m) preserves a separate domain-adaptive pretraining run for the historical 1M-versus-3M comparison. Its 0.4272 typed exact F1 and the 3M model's 0.4331 use the historical hybrid-reference/jieba protocol. The current human-reference results use the Silver-trained continuation listed above. The [historical-results guide](../reproduction/historical_results/README.md) and model card retain this experiment's context and reproduction evidence.

</details>
