# Zenodo archive — Chinese-SkillSpan

This folder is a **template** for a future Zenodo deposit. Nothing has been uploaded.

## Purpose

Zenodo should be the **primary permanent archive** (DOI) for the version of Chinese-SkillSpan that PeerJ reviewers download without requesting access. Public access otherwise goes through GitHub and Hugging Face. Do not list a Google Sites or Drive page in the PeerJ form.

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

Placeholders remain for DOI, version, licences, GitHub, Hugging Face, arXiv, affiliations, and communities. **No Zenodo community id is set**, because none is confirmed.

The JSON `license` value is `other-closed` as a conservative stand-in so that an accidental upload would not advertise CC-BY. `[TODO: replace after legal review]`.

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

After minting: add the DOI to `CITATION.cff`, `README.md`, both Hugging Face cards, the manuscript Data Availability statement, and the PeerJ form. Then create a GitHub Release whose assets match this manifest.

## Reviewer access

Zenodo records used for PeerJ must be **open** (or a reviewer link that does not require a request). `[TODO: confirm the record is publicly downloadable before submission]`.
