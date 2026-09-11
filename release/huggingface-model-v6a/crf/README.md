# JobBERT-zh v6a CRF heads (human reference)

These `best.pt` files are `BertCRF` state dicts continued from the released V4 head on Silver-plus v6a B2. They are **not** `AutoModelForTokenClassification` dumps.

| Path | Seed | Human-reference typed exact |
|---|---:|---:|
| `best.pt` (default) | 42 | 0.5544 |
| `seed42/best.pt` | 42 | 0.5544 |
| `seed43/best.pt` | 43 | 0.5479 |
| `seed44/best.pt` | 44 | 0.5587 |

Paper cell **0.5536±0.0054** is the three-seed mean. Do not upload `last.ckpt`.
