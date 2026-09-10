# Reader terminology crosswalk

This note maps **paper reader wording** (PeerJ CS / Chinese-SkillSpan) onto **original artifact identifiers** and **paths verified in this repository**. It does not rename files, splits, JSON keys, experiment directories, or code variables.

Alignment target: Overleaf commit `7b9be398e8093493054ccbf3cb799c7ee9ed1483` (2026-09-11). The prompt named `PUSH_RECEIPT.md` in this directory; **that file is not in this clone**. This GitHub pass does not edit Overleaf.

Historical snapshots, published-tag notes, and existing run reports keep their original wording. Current entry points should link here rather than rewriting those archives.

---

## How to write after the first definition

Define the professional phrase once, then use the short form. Keep the artifact identifier in parentheses the first time a file or table needs it.

| Original identifier | First-mention reader wording | Later short form | Must keep |
|---|---|---|---|
| Gold150 | a 150-sentence human-annotated reference set | the human reference set | Artifact identifier **Gold150**. Do not rename `gold150_test.jsonl`. |
| Audit-50 / IAA-50 | a 50-sentence calibration cohort | the calibration cohort | For the older dual-coding study: **initial independent-coding study**. Do not mix that study with later audits. |
| Challenge-100 | a 100-sentence challenge cohort | the challenge cohort | Keep the file mapping to `gold100_page1`. |
| A100 | initial teacher-label review cohort | the A100 cohort | Still **Silver-plus**. Not automatically promoted to Gold. |
| QA100 | post-generation review sample | the QA100 sample | Machine-prefilled then human-reviewed. Not independent blind coding. |
| Dual15 | nested dual-review subset | the nested dual-review subset | Nested inside another sample. Not 15 extra independent sentences. |
| H / E / M | conflict-origin / non-conflict-origin / mixed training conditions | H / E / M conditions | Historical-source labels, not objective difficulty. Do not mix with generation pools H730 / E1621. |
| B1 / B2 | earlier / revised supervision | B1 / B2 | Keep the condition codes. The contrast is the whole supervision package (handbook + teacher + adjudication). |
| Silver-plus | resource **release-layer** name | Silver-plus | Generic prose: teacher-generated silver annotations, LLM-annotated silver data, or silver supervision — pick one term per passage. |

**Silver-plus** is a release-layer name, not a recognised quality grade. Do not call the whole layer item-by-item human verified or near-Gold. Allowed: automated validation and sampled human review. Review status and adjudication status are recorded separately.

Do **not** describe the full 150 sentences as independent dual-blind coding. Independent-coding evidence applies to the corresponding 50-sentence historical study.

Do **not** back-label early annotation as Handbook V4.2.14. Execution versions and later rule revisions stay distinct.

---

## Verified paths and split keys

Paths below were checked with `git ls-files` and/or a direct filesystem listing of this clone. A **missing** path is listed as missing; it is not guessed into existence.

### Human reference set (Gold150)

| Role | Identifier / key | In this clone? | Evidence |
|---|---|---|---|
| Artifact identifier | Gold150 | yes (docs, scores) | `docs/paper_body_silver_plus.md`, `release/huggingface-model-v6a/README.md` |
| Locked test file | `gold150_test.jsonl` | **no** | Expected by `scripts/eval_gold150_ext.py` at `Gold150_locked_complete_20260908/gold150_test.jsonl`. Same path recorded in `notes/silver_plus_extensions_20260908/DATA_MANIFEST.json`. |
| Documented SHA-256 | `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` | hash in-tree; file not in-tree | `DATA_MANIFEST.json` `hashes.gold150_test`; `docs/paper_body_silver_plus.md` |
| Eval helper | `scripts/eval_gold150_ext.py` | yes | Reads `split` values `gold100_page1` and `iaa50`. Default `--gold_test` path unchanged. |

Scoring use: the human reference set is for **evaluation only** (not training, early stopping, or prompt choice). Gold150 IDs sit inside V4 hybrid 2,601; scoring the same student again on 2,601 is not an independent test.

### Challenge cohort (Challenge-100)

| Role | Identifier / key | In this clone? | Evidence |
|---|---|---|---|
| Split key inside Gold150 | `gold100_page1` | code/docs only | `scripts/eval_gold150_ext.py` (`chal = … == "gold100_page1"`); `docs/paper_body_silver_plus.md` |
| Package file | `gold100_locked.jsonl` | **no** | Named in the Gold150 lock package; not `git ls-files` |

### Calibration cohort (Audit-50 / IAA-50)

| Role | Identifier / key | In this clone? | Evidence |
|---|---|---|---|
| Split key inside Gold150 | `iaa50` | code/docs only | `scripts/eval_gold150_ext.py`; `docs/paper_body_silver_plus.md` |
| Historical locked file | `iaa50_gold_locked.jsonl` | **no** | Cited by `reports/human_gold85_iaa50/README.md` |
| Diagnostic report (keep original wording) | `reports/human_gold85_iaa50/` | yes | Existing run report. Independent-coding evidence belongs here, not to all 150 sentences. |
| Unstarted standardized IAA design | `reports/annotation_v4/iaa/README.md` | yes | Separate protocol; files `annotator_A.jsonl` / `annotator_B.jsonl` still do not exist. |

### Silver-plus release layer

| Role | Identifier / key | In this clone? | Evidence |
|---|---|---|---|
| Release-layer name | Silver-plus | yes | `docs/paper_body_silver_plus.md`; `notes/silver_plus_extensions_20260908/README.md` |
| Teacher prompts (frozen; do not edit) | `notes/handbooks/PROMPT_silver_plus_v4211.txt`, `PROMPT_silver_plus_v4212.txt` | yes | Frozen prompt files |
| v6a train/dev counts | 2156 / 169 | docs only | `DATA_MANIFEST.json` `v6a_n_train` / `v6a_n_dev` |
| Extension list | `v6a_nocross` 2150 / 169 | docs only | `DATA_MANIFEST.json` `extension_list` |
| Hold-82 process proof | `notes/silver_plus_hold82_process_proof_20260908/` | yes | Not used for training ([PR #1](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/pull/1)) |
| v6a / extension JSONL train files | laboratory `output/` paths | **no** | Paths in `DATA_MANIFEST.json` point outside this Git tree |

V4 CRF silver (`data/train_lskt_v4_silver.jsonl`, `data/dev_lskt_v4_silver.jsonl`) is an earlier SOP silver protocol, not the Silver-plus v6a lists.

### A100, H730, E1621, HEM conditions

| Role | Identifier / key | In this clone? | Evidence |
|---|---|---|---|
| A100 count in v6a train records | `A100` = 96 | yes (manifest) | `DATA_MANIFEST.json` `v6a_cohort_train_records` |
| Generation-pool counts | `H730` = 637, `E1621` = 1423 | yes (manifest) | same key; these are **pools**, not HEM sample sizes |
| HEM condition codes | `H_468`, `E_468`, `M_468` | yes | `notes/silver_plus_extensions_20260908/HEM_CONFIG.json`, `HEM_BALANCE_REPORT.md`, `HEM_SAMPLING_MANIFEST.json` |
| HEM construction | A100 base 96 + 468 source sentences → 564 unique texts per condition | yes | `HEM_BALANCE_REPORT.md` |

H / E / M on the HEM student are **conflict-origin / non-conflict-origin / mixed** training conditions. They are not an objective difficulty taxonomy and must not be confused with the H730 / E1621 generation pools.

### B1 / B2

Condition codes for **earlier** versus **revised** supervision on the same sentences. Keep `B1` / `B2` in tables and filenames. Do not rewrite frozen score JSON keys.

Reader interpretation: the gap compares the handbook + teacher + adjudication package, not two prompts and not a teacher-architecture ablation. See `docs/paper_body_silver_plus.md`.

### Handbook execution versus later revision

| What | Verified in-tree wording | Do not write |
|---|---|---|
| Paper SOP in `REPRODUCIBILITY.md` | Handbook B `B.sop_v4.2.1` (`notes/handbooks/handbook_B_sop_v4.md`) | That this file *was* V4.2.14 at execution time |
| Gold150 freeze note (package, not in Git) | `B.sop_v4.2.10` / operating `B.sop_v4.2.11` | Back-dating those runs to V4.2.14 |
| Later handbook files in `notes/handbooks/` | subsequent dated revisions | That every earlier label pass used the latest revision |

---

## Figure 1 (workflow)

Archived caption: `notes/manuscript_display_archive_20260910/displays/figure_01.tex` (`fig:macro-micro`). That archive is a snapshot; this note states the current reader interpretation.

1. Multi-source Chinese job-ad sentences → human-led specification and the human reference set.
2. Frozen specification / prompts + candidate text → teacher-generated **Silver-plus**.
3. Eligible silver supervision → **JobBERT-zh + CRF** and **Qwen2.5-14B-Instruct + LoRA**.
4. The human reference set enters **scoring only**.
5. Domain-adaptive pre-training is the **JobBERT** branch.
6. LLM **inference baselines** and **teacher annotation** are different roles.

Do not read the flowchart as “every system shares one protocol” or as a fresh independent blind test of all rows.

---

## Unresolved mappings

These identifiers are required by the paper wording table but **have no file, split key, or path in this clone**:

| Identifier | Intended reader wording | Status in this repository |
|---|---|---|
| QA100 | post-generation review sample | No `QA100` path, filename, or JSON key under `git ls-files`. |
| Dual15 | nested dual-review subset | No `Dual15` path. `reports/sandbox_lskt_v4_silver/DUAL_EVAL.md` is a **model dual-eval**, not this nested review subset. |
| `gold150_test.jsonl` bytes | human reference set | Documented and hashed; **file not shipped in this Git tree**. |
| `PUSH_RECEIPT.md` | Overleaf 2026-09-11 receipt | Missing from this clone. |

Do not invent substitute filenames for QA100 or Dual15.

---

## What this pass does not change

- Labels, spans, sentence IDs, split membership, training/dev lists, statistics, or result status.
- Frozen prompts, parsers, weights, predictions, score files, or hashes.
- Command examples: filenames, flags, JSON keys, split names, experiment directories, code variables.
- Published tag `v0.1.1` notes in `CHANGELOG.md`.
- Existing run reports under `notes/gold150_followups_20260909/`, `notes/silver_plus_extensions_20260908/`, `notes/silver_plus_followups_20260909/`, and `reports/human_gold85_iaa50/`.

---

## Hugging Face (prepare locally; do not change the live Hub in this pass)

Local card sources to copy later, after review:

| Local source | Live target | Change in this pass |
|---|---|---|
| `release/huggingface-dataset/README.md` | no public dataset repo | Reader wording only. Do not publish a new dataset version. |
| `release/huggingface-model/README.md` | https://huggingface.co/AlfredJames/jobbert-zh | Reader wording only. Do not replace V4 weights. |
| `release/huggingface-model-v6a/README.md` | https://huggingface.co/AlfredJames/jobbert-zh-v6a | Reader wording only. Do not replace v6a weights. |
| `release/huggingface-model-v6a/crf/README.md` | Hub `crf/` note | Reader wording only. |

Pending Hub sync: the three README files above. This GitHub PR does **not** upload them.
