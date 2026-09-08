# Changelog — Chinese-SkillSpan / Chinese JobBERT

This file distinguishes preprint, dataset, code, model, and PeerJ submission lines. It does not invent a PeerJ article URL or an arXiv id.

---

## Unreleased notes (2026-09-09b)

- Design-only Qwen P1 prompt and optional kNN plan: `docs/qwen_lskt_sft_v1_proposal_20260909.md`, `docs/qwen_sft_knn_optional_plan_20260909.md`. Not trained. Does **not** replace official P0 Gold150 **0.1215±0.0092** or V4 hybrid JobBERT 3M **0.4331**.

## Unreleased notes (2026-09-09)

- Removed leftover root PDFs: the rejected DASFAA draft, an outdated 0828 PeerJ-named draft, the SkillSpan NAACL 2022 reprint, the unverified `Chinese-SkillSpan-local-preview-optimized.pdf`, and the sister-paper IEEE Access PDF. Cite SkillSpan from the ACL Anthology. Do not host a manuscript PDF until it can be checked against Overleaf.
- Manuscript-body draft for Silver-plus methods and Gold150 results: `docs/paper_body_silver_plus.md`. States the JobBERT CRF (no prompt) vs Qwen2.5-14B JSON-offset LoRA (fixed prompt) split. kNN / longer SOP prompts are discussed as **unrun** future conditions, not official rows. Does **not** change V4 hybrid JobBERT 3M **0.4331**.

## Unreleased notes (2026-09-08)

- Silver-plus laboratory extensions on Gold150: Qwen2.5-14B JSON-offset SFT (B2 only) and JobBERT-zh 3M H/E/M equal-n CRF. Archive: `notes/silver_plus_extensions_20260908/`. JobBERT-zh 1M was skipped. Does **not** change V4 hybrid JobBERT 3M **0.4331**, official Qwen SOP extract **0.1724**, or the existing Gold150 JobBERT v6a B2 main cell.

## Unreleased notes (2026-09-07)

- Appendix diagnostic only: `reports/human_gold85_iaa50/` (Gold85 + IAA-50 typed exact, Qwen2.5-14B SOP, span character-length bins). Does **not** change V4 hybrid JobBERT 3M **0.4331**.

---

## 0.1.1 — 2026-09-04 (public snapshot)

GitHub, JobBERT-zh, and Zenodo `v0.1.1` are **public**.

- Code: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark
- Model: https://huggingface.co/AlfredJames/jobbert-zh
- Version DOI: https://doi.org/10.5281/zenodo.22288338
- Concept DOI: https://doi.org/10.5281/zenodo.22288337
- `v0.1.0` Zenodo ingest failed (citation-metadata parse) and was superseded. Do not re-issue that tag.
- JobBERT-zh licence remains `other` pending job-ad text-rights confirmation.
- The Zenodo GitHub hook labelled the record `cc-by-4.0`; that is the platform default, not an author licence decision.
- Public links are GitHub, Hugging Face, and Zenodo only.

---

## PeerJ Computer Science submission

- Target venue: **PeerJ Computer Science** (single-anonymized review). Rejected DASFAA drafts are not kept in the public tree.
- Proposed Data Availability wording is in `DATA_AVAILABILITY.md` (Zenodo version DOI + GitHub + JobBERT-zh).
- Submission date and Overleaf revision are not recorded here.

---

## Dataset releases

| Identifier | What it is | Date | Notes |
|---|---|---|---|
| Corpus Table 1 split | 22,840 sentences (`17,460` / `2,143` / `3,237`) | — | SHA-256 in `REPRODUCIBILITY.md` |
| Gold v2 | 2,601 unique IDs; sha `7a26e32b…504ff6` | Frozen 2026-08-22 | Appendix / provenance; do not overwrite |
| V4 hybrid (paper main) | Same 2,601 IDs; sha `2ad6342d…818d99` | Protocol amended 2026-08-27 | 980 SimHuman + 1,621 SOP-CWS; not human Doccano Gold |
| Handbook B | `B.sop_v4.2.1` | 2026-08-31 | Paper SOP |
| Human page-1 overlay | 200 sentences; sha `fcecb522…617490` | 2026-09-03 | Supplement; path `data/human_gold_page1_200.jsonl` |
| `repartition_v1` | Same 22,840, other split (`16,350` / `2,268` / `4,222`) | — | Draft; not main gold |
| Public archive | GitHub / Zenodo `v0.1.1` | 2026-09-04 | No separate Hugging Face dataset repo |

---

## Code releases

| Identifier | What it is | Date |
|---|---|---|
| Scorer `cnss-lskt-1.2.0` | Official typed / relaxed micro-F1 | Present in `scorer/score_lskt.py` |
| Public GitHub | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark | Public as of 2026-09-04 |
| GitHub Release | `v0.1.1` | 2026-09-04 |

---

## Model releases

| Identifier | What it is | Date |
|---|---|---|
| JobBERT-zh 1M / 3M v4 (laboratory) | MLM + CRF; frozen preds in `data/frozen_preds/` | — |
| Public Hugging Face model | https://huggingface.co/AlfredJames/jobbert-zh | Public as of 2026-09-04 |

No model weights are versioned in Git.

---

## arXiv / preprint versions

This paper does not yet have an arXiv identifier. Do not use sister-paper ids `2604.21525` or `2604.23009`. This repository does not host a manuscript PDF.
