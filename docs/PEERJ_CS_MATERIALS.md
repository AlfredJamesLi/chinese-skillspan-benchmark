# PeerJ Computer Science — data, code, and model materials

Venue rules (PeerJ CS author instructions / policies, checked 2026-09-10):

- Code **and** the data needed to reproduce the reported results must be available at submission.
- GitHub alone is not enough: a GitHub repo **must** have an archival DOI (Zenodo hook is the usual route).
- Files must be machine-readable (not PDF/screenshots of tables).
- If a dataset grows after the cited archive, say so: what is in the DOI, what is later, and how it will be versioned.
- Do not invent a Hugging Face **dataset** URL. JobBERT-zh is the model repo only.

This note is the working inventory for that policy. Checksums stay in `REPRODUCIBILITY.md`, not in the running DAS paragraph.

---

## Three layers (do not collapse)

| Layer | What reviewers download today | Persistent ID | Contains Gold150 / Silver-plus B2? |
|---|---|---|---|
| **A. Cited archive** | GitHub Release `v0.1.2` via Zenodo | version DOI [10.5281/zenodo.22685143](https://doi.org/10.5281/zenodo.22685143); first snapshot [10.5281/zenodo.22288338](https://doi.org/10.5281/zenodo.22288338); concept [10.5281/zenodo.22288337](https://doi.org/10.5281/zenodo.22288337) | **No** |
| **B. Public code + paper-main data** | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark (`main`) | same repo; Release tag `v0.1.2` is one snapshot behind `main` | Human-200 yes. Gold150 / B2 **yes on `main`**, not in the `v0.1.2` tag |
| **C. Still laboratory-only** | Qwen2.5-14B LoRA adapters | no public Hub repo | adapters not released |

JobBERT-zh (paper-main encoder): https://huggingface.co/AlfredJames/jobbert-zh

---

## PeerJ form — paste this Data Availability text

Use `\url{...}` in TeX so long DOIs do not collapse word spaces.

The Chinese-SkillSpan dataset, annotation guidelines, predefined data splits, and documentation are available at https://doi.org/10.5281/zenodo.22685143 (version v0.1.2; concept DOI https://doi.org/10.5281/zenodo.22288337). The first archival snapshot is https://doi.org/10.5281/zenodo.22288338 (version v0.1.1). The source code, preprocessing scripts, and evaluation tools are available at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The paper-main JobBERT-zh model, tokenizer, configuration files, and model card are available at https://huggingface.co/AlfredJames/jobbert-zh. Two later public model repositories are available at https://huggingface.co/AlfredJames/jobbert-zh-1m and https://huggingface.co/AlfredJames/jobbert-zh-v6a; they do not replace the paper-main encoder. Gold150 (`data/gold150_test.jsonl`) and Silver-plus B2 train/development files are on the GitHub repository and are not included in Zenodo v0.1.1 or v0.1.2.

Companion files: `DATA_AVAILABILITY.md`, `REPRODUCIBILITY.md`, `notes/SILVER_PLUS_EXTENSION_PROVENANCE.md`, `docs/RELEASE_CHECKLIST.md`.
