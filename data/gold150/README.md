# Gold150 test freeze

Canonical scoring path: [`../gold150_test.jsonl`](../gold150_test.jsonl) (same bytes as `gold150_test.jsonl` in this folder).

| File | n | Bytes | SHA-256 |
|---|---:|---:|---|
| `gold150_test.jsonl` | 150 | 67,116 | `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` |
| `gold100_locked.jsonl` | 100 (Challenge-100) | 41,329 | `a9fe43b79f58631876f00515f6a60649d8d2ceb57ebee111fe471cc70766864c` |
| `iaa50_gold_locked.copied.jsonl` | 50 (Audit-50) | 18,232 | `68b47bdbad1622ca39d89a2dceaf8117ee44a2227272e901a7673bc676531686` |

Gold150 = Challenge-100 (`split=gold100_page1`) + Audit-50 (`split=iaa50`). Fields use `source_id` and Doccano `label` triples; it is **not** V4 hybrid 2,601 and **not** Gold v2. Do not overwrite `gold_canonical_v2.jsonl` or `test_lskt_v4_cws_simhuman980_hybrid.jsonl`.

These files are on GitHub `main`. They are **not** in Zenodo `v0.1.1` or `v0.1.2`. Teacher Silver-plus B2: [`../silver_plus_v6a_nocross/`](../silver_plus_v6a_nocross/).
