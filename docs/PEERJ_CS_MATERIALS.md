# PeerJ Computer Science — data, code, and model materials

Venue rules (PeerJ CS author instructions / policies, checked 2026-09-18):

- Code **and** the data needed to reproduce the reported results must be available at submission.
- GitHub alone is not enough: a GitHub repo **must** have an archival DOI (Zenodo).
- Files must be machine-readable (not PDF/screenshots of tables).
- If a dataset grows after the cited archive, say so: what is in the DOI, what is later, and how it will be versioned.
- Do not invent a Hugging Face **dataset** URL. JobBERT repositories are model repos only.
- Do not list Google Sites, Google Drive, or a private GitHub URL in the PeerJ form.
- The manuscript PDF must be PeerJ Computer Science format: US Letter, line numbers, 12 pt, left-justified, 2.5 cm margins. Abstract subheadings are **Background. Methods. Results. Conclusions.**
- CRediT contributions are entered in the PeerJ form by the authors. This file does not invent them.

Checksums stay in `REPRODUCIBILITY.md`, not in the running DAS paragraph.

---

## Three layers (do not collapse)

| Layer | What reviewers download today | Persistent ID | Contains human reference / Silver-plus B2? |
|---|---|---|---|
| **A. Cited archive** | Zenodo `v0.1.3` | version DOI [10.5281/zenodo.22698504](https://doi.org/10.5281/zenodo.22698504); earlier [v0.1.2](https://doi.org/10.5281/zenodo.22685143); first snapshot [v0.1.1](https://doi.org/10.5281/zenodo.22288338) remains on Zenodo; concept [10.5281/zenodo.22288337](https://doi.org/10.5281/zenodo.22288337) | **Yes in `v0.1.3` only** |
| **B. Public code** | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark | current default branch; GitHub Release `v0.1.3` | Human reference / B2 from `v0.1.3` |
| **C. Still laboratory-only** | Qwen2.5-14B LoRA adapters | no public Hub repo | adapters not released |

GitHub tags `v0.1.0` and `v0.1.1` have been withdrawn. Do not send reviewers to those tags. No `v0.1.4` has been minted.

JobBERT-zh initialization: https://huggingface.co/AlfredJames/jobbert-zh  
JobBERT-zh B2 continuation: https://huggingface.co/AlfredJames/jobbert-zh-v6a

---

## PeerJ form — paste this Data Availability text

Use `\url{...}` in TeX so long DOIs do not collapse word spaces.

The Chinese-SkillSpan dataset, annotation guidelines, predefined data splits, and documentation are available at https://doi.org/10.5281/zenodo.22698504 (version v0.1.3; concept DOI https://doi.org/10.5281/zenodo.22288337). An earlier snapshot is https://doi.org/10.5281/zenodo.22685143 (version v0.1.2). The first archival snapshot remains at https://doi.org/10.5281/zenodo.22288338 (version v0.1.1) on Zenodo; the corresponding GitHub tags v0.1.0 and v0.1.1 have been withdrawn. The source code, preprocessing scripts, and evaluation tools are available at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The JobBERT-zh initialization encoder and inherited CRF are available at https://huggingface.co/AlfredJames/jobbert-zh. The JobBERT-zh B2 continuation is available at https://huggingface.co/AlfredJames/jobbert-zh-v6a (default checkpoint is seed 42). The 150-sentence human reference set and Silver-plus B2 training/development files are included in v0.1.3 and are not in Zenodo v0.1.1 or v0.1.2. Qwen LoRA adapters are not published. These materials are released for academic research and peer review. Original job-advertisement wording is not licensed as CC-BY.

Companion files: `DATA_AVAILABILITY.md`, `REPRODUCIBILITY.md`, `docs/models.md`.

---

## PeerJ form — other fields (do not invent)

| Field | Use |
|---|---|
| Funding | National Social Science Fund of China, Grant No. 21BGL142 |
| Competing interests | Authors complete this; do not invent |
| Ethics | Recruitment advertisements only; not a curated applicant-CV corpus. Authors confirm any remaining title/workplace-name review |
| CRediT | Authors complete in the PeerJ form |
| Data / code URLs | The three public URLs above only |

Do not upload weights, LoRA adapters, or vendor CSV/XLSX dumps as PeerJ supplements.
