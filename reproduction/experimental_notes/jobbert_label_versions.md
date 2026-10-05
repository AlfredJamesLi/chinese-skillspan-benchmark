# Historical JobBERT label-version comparison

This supplementary comparison is retained alongside the current Silver-trained JobBERT-zh + CRF baseline. Resource names follow the [terminology guide](../../docs/terminology.md); frozen files, manifest names, checkpoints, and scores keep their original identities.

## Design and results

Earlier labels (B1) use historical extraction labels. Revised labels (B2) incorporate updated guidelines, LLM annotations, and adjudication. Both JobBERT conditions start from the same released encoder and inherited CRF and use the same 2,156 training and 169 development texts. Labels change in 1,440 training records and 107 development records. Development typed exact-span F1 selects checkpoints against the corresponding labels, so training supervision and checkpoint-selection targets both change.

| Supervision and selection labels | Train / development records | Typed exact F1 on the human reference set |
|---|---:|---:|
| Earlier labels | 2,156 / 169 | 0.1422 ± 0.0138 |
| Revised labels | 2,156 / 169 | 0.5536 ± 0.0054 |

Scores are means ± sample standard deviations across seeds 42, 43, and 44. The revised-label row is the current Silver-trained JobBERT-zh + CRF baseline. The difference reflects combined changes in training labels and checkpoint-selection labels; it does not isolate label quality, a guideline rule, or an annotation model.

The reported JobBERT settings are learning rate 2e-5, batch size 16, maximum input length 256 tokens, up to six epochs, and patience two. The [historical experimental notes](README.md) retain implementation and exposure limitations; the [model guide](../../docs/models.md) documents initialization, CRF loading, and checkpoint access.

## Relation to the other Silver resources

The released Qwen and encoder sets use 2,150/169 records after removing six training records matching three development texts after NFC normalization. They are not the 2,156/169 JobBERT manifest or the 2,451-record original Silver candidate pool. Earlier/revised are historical label versions; B1/B2 are retained as archive identifiers, not resource proper names.

The main Qwen comparison remains no adapter versus Qwen + LoRA under fixed inference rules, 0.3612 versus 0.5403 ± 0.0354. There is no earlier-label Qwen fine-tuning condition in that comparison. These model designs do not provide a controlled architecture ranking. The [evaluation entry](../EVALUATION_ENTRY.md) separates the scoring protocols.
