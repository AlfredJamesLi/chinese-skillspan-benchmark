# Annotation and training terminology

The benchmark uses LLM-generated discrete span labels for supervised model training and evaluation. Human coding builds the reference; sampled review checks selected model annotations. These are distinct roles.

| Earlier wording | Current wording | Meaning |
|---|---|---|
| Teacher model / teacher configuration | LLM annotator / annotation-model configuration | Model and access configuration used to generate labels |
| Teacher annotation / teacher-generated labels | LLM annotation / LLM-generated labels | Discrete competency spans and types |
| Teacher supervision and sampled review | LLM annotation and sampled review | Label generation followed by review of sampled records |
| Student model | Fine-tuned model | JobBERT or Qwen trained using the specified labels |
| Student learning | Supervised fine-tuning | Task adaptation with labelled training examples |
| Admitted records | Retained records | Records included after the documented annotation checks |
| Manifest | Split manifest | Exact record list for a training, validation or test subset |

Silver-plus denotes the model-annotated resource, including documented reviewed subsets; it does not imply that every label has been manually checked. The human-reference set contains 150 sentences. Total human coding or review covers 500 unique sentences with different designs; this is not a 500-sentence Gold test set.

The paper describes the implemented annotation and supervised-training procedure without claiming a separate knowledge-distillation method. Literature uses distillation in different senses, including learning from generated labels. References to distillation in descriptions of other published methods retain their original meaning. `Supervision`, `fine-tuning`, `LoRA`, `CRF`, and `domain-adaptive pretraining` remain appropriate where they describe the actual experiment.

Current prose and figure captions use these terms. Historical snapshots, frozen prompt text, command-line options, model IDs, source paths, result keys, labels and hashes keep their original bytes. A historical `teacher` or `student` identifier is an alias, not evidence of an additional training objective. See [the resource mapping](../PAPER_NAMES.md) and [evaluation guide](../reproduction/EVALUATION_ENTRY.md).

Background: [Tan et al. (2024), Large Language Models for Data Annotation and Synthesis](https://aclanthology.org/2024.emnlp-main.54/).
