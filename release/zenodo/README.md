# Zenodo archive — Chinese-SkillSpan

This folder holds metadata for the Zenodo deposit created from GitHub Release `v0.1.1`.

**Version DOI:** https://doi.org/10.5281/zenodo.22288338 (`v0.1.1`, record https://zenodo.org/records/22288338)  
**Concept DOI:** https://doi.org/10.5281/zenodo.22288337

## Purpose

Zenodo is the **primary permanent archive** (DOI) for the version of Chinese-SkillSpan that PeerJ reviewers download without requesting access. Public access otherwise goes through GitHub and Hugging Face. Do not list a Google Sites or Drive page in the PeerJ form.

## Record metadata

Machine-readable metadata: [`.zenodo.json`](.zenodo.json).

Verified fields already filled:

- Title
- Creator order (Guojing Li … Xiangyu Zhao)
- Description outline
- Keywords
- Upload type: `dataset`
- Grant mentioned in the description: National Social Science Fund of China, **21BGL142**
- Related identifiers that exist today: the public GitHub repository and the JobBERT-zh Hugging Face model

The GitHub-minted record already carries version DOI `10.5281/zenodo.22288338` and concept DOI `10.5281/zenodo.22288337`. **No Zenodo community id is set.**

The JSON `license` value is `other-closed` as a conservative stand-in. The live GitHub-hook record was labelled `cc-by-4.0` by platform default; that is not an author licence decision.

## What to upload (see RELEASE_MANIFEST.md)

Include guidelines, splits, BIO files, scorer, scripts, frozen predictions, committed tables, and the public Markdown docs.

Exclude:

- `output/` and other checkpoints
- virtual environments and caches
- API keys, tokens, `.env`
- raw `应届生招聘大数据*.csv` and `人工智能招聘大数据2025年.xlsx`
- `data/jobbert_*_sents.jsonl` until text rights are confirmed
- sister-project (IEEE Access / SRICL) materials
- laboratory restore notes that contain personal cloud paths (`REPRO_FROM_BAIDU.md`, `MODELS_CATALOG.md`) unless they are rewritten

## How this DOI should be cited

The minted DOI is already in `README.md`, `DATA_AVAILABILITY.md`, and the Hugging Face model-card template. The Overleaf Data Availability paragraph still needs the same wording.

## Reviewer access

The Zenodo record https://zenodo.org/records/22288338 is the open archive for PeerJ. Confirm in an incognito window that files download without a request.
