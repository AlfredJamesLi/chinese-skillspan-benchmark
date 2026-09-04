# Changelog — Chinese-SkillSpan / Chinese JobBERT

This file distinguishes preprint, dataset, code, model, and PeerJ submission lines. It does not invent a PeerJ article URL or an arXiv id.

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

- Venue recorded in this repository: **PeerJ Computer Science** (not DASFAA).
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

This paper does not yet have an arXiv identifier. Do not use sister-paper ids `2604.21525` or `2604.23009`. Draft PDFs in the working tree may still carry DASFAA / “ESCO-Aligned” filenames; those names are not preprint versions.
