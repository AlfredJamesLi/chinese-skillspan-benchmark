# Changelog — Chinese-SkillSpan / Chinese JobBERT

Dates and version numbers that are not verified in this repository are left as `[TODO: ...]`. This file distinguishes preprint, dataset, code, model, and PeerJ submission lines. It does not invent a public release that has not occurred.

---

## `[TODO: public release version]` — not yet published

**Status (2026-09-04):** GitHub repository and JobBERT-zh model are **public**. GitHub Release `v0.1.0` exists but its Zenodo hook failed (`Citation metadata load failed`). `v0.1.1` retries archival with a Zenodo-safe `CITATION.cff`. Public links are GitHub and Hugging Face only.

- Code: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark
- Model: https://huggingface.co/AlfredJames/jobbert-zh
- Dataset HF / Zenodo DOI: `[TODO]`
- JobBERT-zh licence remains `other` pending job-ad text-rights confirmation

---

## PeerJ Computer Science submission version

- Venue recorded in this repository: **PeerJ Computer Science** (not DASFAA).
- Submission date: `[TODO: PeerJ submission date]`.
- Manuscript version hash / Overleaf revision: `[TODO]`.
- Data Availability Statement: placeholders in `DATA_AVAILABILITY.md` until DOI and URLs exist.

---

## Dataset releases

| Identifier | What it is | Date | Notes |
|---|---|---|---|
| Corpus Table 1 split | 22,840 sentences (`17,460` / `2,143` / `3,237`) | `[TODO: collection / freeze date]` | SHA-256 in `REPRODUCIBILITY.md` |
| Gold v2 | 2,601 unique IDs; sha `7a26e32b…504ff6` | Frozen 2026-08-22 (protocol note) | Appendix / provenance; do not overwrite |
| V4 hybrid (paper main) | Same 2,601 IDs; sha `2ad6342d…818d99` | Protocol amended 2026-08-27 | 980 SimHuman + 1,621 SOP-CWS; not human Doccano Gold |
| Handbook B | `B.sop_v4.2.1` | 2026-08-31 | Paper SOP |
| Human page-1 overlay | 200 sentences; sha `fcecb522…617490` | 2026-09-03 | Supplement; not abstract gold |
| `repartition_v1` | Same 22,840, other split | `[TODO]` | Draft; not main gold |
| Public dataset tag | `[TODO: e.g. chineseskillspan-1.0]` | `[TODO]` | Hugging Face + Zenodo |

---

## Code releases

| Identifier | What it is | Date |
|---|---|---|
| Scorer `cnss-lskt-1.2.0` | Official typed / relaxed micro-F1 | Present in `scorer/score_lskt.py` (file date not treated as a SemVer release) |
| Private working backup | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark | `[TODO: first public tag date]` |
| Public GitHub Release | `[TODO: tag]` | `[TODO]` |

---

## Model releases

| Identifier | What it is | Date |
|---|---|---|
| Chinese JobBERT 1M / 3M v4 (laboratory) | MLM + CRF; frozen preds in `data/frozen_preds/` | `[TODO: training date]` |
| Public Hugging Face model | `[TODO: repo name and revision]` | `[TODO]` |

No model weights are versioned in Git.

---

## arXiv / preprint versions

| Version | Identifier | Date |
|---|---|---|
| This paper’s preprint | `[TODO: arXiv id — do not use 2604.21525 or 2604.23009]` | `[TODO]` |

Draft PDFs in the working tree still carry DASFAA / “ESCO-Aligned” filenames. Those names are **not** preprint versions.

---

## Unreleased laboratory notes (not public version numbers)

Internal Chinese README preserved as `docs/INTERNAL_RESULTS_README.md`. Gold v2 unique-first views, human-200 overlay, and vanilla-WWM unverified rows live in `notes/` and `tables/` and are not separate public releases.
