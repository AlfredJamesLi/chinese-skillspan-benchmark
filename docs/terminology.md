# Resource, annotation, and training terminology

The benchmark uses LLM-generated discrete span labels for supervised model training and evaluation. Human coding builds the reference; sampled review checks selected model annotations. These are distinct roles.

## Resource names and relationships

Use these names in prose, tables, and figures. Historical identifiers locate frozen files and checkpoints; this naming update does not change data, labels, membership, versions, or scores.

| Resource name | Size | Role | Historical identifier / relationship |
|---|---|---|---|
| Source corpus | 22,840 sentences | Source collection; original document partitions | Not the later labeled experimental splits |
| Human reference set | 150 sentences; 663 spans | Diagnostic model evaluation; also used in handbook development | Gold150/gold150; frozen reference, not a new test set |
| Original Silver pool | 2,451 records | Candidate supervision from the original annotation study | Silver-plus; not identical to either training split |
| Silver training/development sets (Qwen and encoders) | 2,150 / 169 records | Main Qwen and encoder fitting/selection | B2; v6a_nocross |
| Silver training/development sets (JobBERT) | 2,156 / 169 records | Historical JobBERT fitting/selection | Revised labels B2; v6a; six more training records than Qwen |
| Expanded Silver pool | 9,540 records; 8,842/348/350 train/validation/test | Adopted expanded supervision and silver-target evaluation | Codex; includes earlier supervision; not additional to all previous pools |
| Alternative expanded Silver pool | 9,646 records; 8,943/351/352 train/validation/test | Supplementary annotation-channel configuration | Alternative/proxy; not a disjoint dataset |
| Initial Silver review sample | 100 sentences | Review before bulk annotation | A100 |
| Post-generation Silver review sample | 100 sentences | Review after original bulk annotation | QA100; Dual15 is a nested review subset |
| Additional review sample | 150 sentences | Assisted review of new Silver annotations | QA150; A/B are two annotation layers on the same sentences |
| Blinded agreement sample | 50 sentences | Independent agreement under the final handbook; self-review allowed | Five learning and 15 practice sentences excluded; individual layers, not consensus model-test labels |

- The initial annotation dataset has **2,601 records = 150 human-reference sentences + 2,451 original Silver candidate records**. The original Silver pool differs from the 2,150/169 Qwen and encoder split and the 2,156/169 JobBERT split. Model-specific admission and duplicate handling determine those inputs.
- The adopted expanded Silver pool includes earlier supervision. The 9,646-record alternative overlaps with the adopted 9,540-record pool; their counts must not be added as disjoint datasets.
- Reviewers A and B annotate the **same 150-sentence additional review sample**. Their two annotation layers do not create 300 unique sentences. The initial and post-generation review samples are separate 100-sentence samples.
- Historical human coverage is **150 reference + 100 initial review + 100 post-generation review + 150 additional review = 500 unique sentences**. The nested 15-sentence review subset adds no unique sentences. The separate 50-sentence blinded agreement study is reported separately from that historical coverage.
- The blinded agreement sample measures independent annotation agreement under the final handbook. Its individual layers are not consensus labels for model testing; five learning and fifteen practice sentences are excluded.
- **B1 and B2 identify historical label versions, not resource proper names.** Use Earlier labels / Revised labels for the supplementary JobBERT comparison and Qwen + LoRA for the adapted Qwen model. Keep `train_b2.jsonl`, `dev_b2.jsonl`, `v6a`, `v6a_nocross`, model repository IDs, hashes, and archived keys unchanged.

See the [historical JobBERT label-version comparison](../reproduction/experimental_notes/jobbert_label_versions.md) for the joint training-label and checkpoint-selection comparison. Frozen handbook versions remain distinct: changing a display name does not relabel a historical annotation layer.

## Annotation and training language

| Earlier wording | Current wording | Meaning |
|---|---|---|
| Teacher model / teacher configuration | LLM annotator / annotation-model configuration | Model and access configuration used to generate labels |
| Teacher annotation / teacher-generated labels | LLM annotation / LLM-generated labels | Discrete competency spans and types |
| Teacher supervision and sampled review | LLM annotation and sampled review | Label generation followed by review of sampled records |
| Student model | Fine-tuned model | JobBERT or Qwen trained using the specified labels |
| Student learning | Supervised fine-tuning | Task adaptation with labelled training examples |
| Admitted records | Retained records | Records included after the documented annotation checks |
| Manifest | Split manifest | Exact record list for a training, validation or test subset |

The original Silver pool (historical identifier `Silver-plus`) contains generated candidate supervision, including documented reviewed subsets; it does not imply that every label has been manually checked. The human-reference set contains 150 sentences. Total human coding or review covers 500 unique sentences with different designs; this is not a 500-sentence Gold test set.

The paper describes the implemented annotation and supervised-training procedure without claiming a separate knowledge-distillation method. Literature uses distillation in different senses, including learning from generated labels. References to distillation in descriptions of other published methods retain their original meaning. `Supervision`, `fine-tuning`, `LoRA`, `CRF`, and `domain-adaptive pretraining` remain appropriate where they describe the actual experiment.

Current prose and figure captions use these terms. Historical snapshots, frozen prompt text, command-line options, model IDs, source paths, result keys, labels and hashes keep their original bytes. A historical `teacher` or `student` identifier is an alias, not evidence of an additional training objective. See [the resource mapping](../PAPER_NAMES.md) and [evaluation guide](../reproduction/EVALUATION_ENTRY.md).

Background: [Tan et al. (2024), Large Language Models for Data Annotation and Synthesis](https://aclanthology.org/2024.emnlp-main.54/).
