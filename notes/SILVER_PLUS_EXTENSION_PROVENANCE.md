# Silver-plus extension provenance

Status: **on GitHub `main` (2026-09-11)**. Not in Zenodo `v0.1.1` or `v0.1.2`. Not paper-main gold. Silver-plus rows are teacher supervision, not extra Gold150 test labels.

Do not call this document isolation. Isolation wording: **句级隔离扩展版** (sentence-level isolation, extended).

---

## Role

| Artifact | Path | Evaluation gold? |
|---|---|---|
| V4 hybrid 2,601 IDs | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | Yes (derived SOP+SimHuman) |
| Human-200 | `data/human_gold_page1_200.jsonl` | Diagnostic overlay; in Release `v0.1.1` |
| Gold150 | `data/gold150_test.jsonl` | Later test reference; on GitHub `main` only |
| Silver-plus B2 `v6a_nocross` | `data/silver_plus_v6a_nocross/` | No |

---

## Frozen identifiers

| File | n | Bytes | SHA-256 |
|---|---:|---:|---|
| `data/gold150_test.jsonl` | 150 | 67,116 | `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` |
| `data/silver_plus_v6a_nocross/train_b2.jsonl` | 2,150 | 1,757,307 | `8921e5fc4b89a0fa83bd942f919c3325546b9938e099b6a13e378736b6717d2e` |
| `data/silver_plus_v6a_nocross/dev_b2.jsonl` | 169 | 151,873 | `e67a3eb5229b94c6c1b552d5f40ece9ad362197236c20cd66b7f2600c9636fef` |

Gold150 IDs are not in the B2 train/dev lists. A new Zenodo version under concept `10.5281/zenodo.22288337` has **not** been minted for these files. Do not silently replace record `22288338` or `22685143`.

---

## Reporting scope

- Paper-main encoder row remains JobBERT-zh 3M typed exact **0.4331** on V4 hybrid 2,601.
- Gold150 is a **separate protocol**. Do not rank Gold150 F1 against 0.4331 in one sentence.
- Qwen2.5-14B LoRA adapters are **not** a public model release.

Checksums are repeated in `REPRODUCIBILITY.md`. PeerJ Data Availability wording is in `DATA_AVAILABILITY.md`.
