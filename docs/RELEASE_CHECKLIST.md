# Release and PeerJ submission checklist — Chinese-SkillSpan

Complete every item before a public upload. This document does **not** authorise GitHub, Hugging Face, Zenodo, or PeerJ publication. No remote action has been taken.

Proposed PeerJ wording (keep placeholders until the links exist):

> The Chinese-SkillSpan dataset, annotation guidelines, predefined data splits, and documentation are available at [DATASET DOI OR PERMANENT URL]. The source code, preprocessing scripts, and evaluation tools are available at [GITHUB URL]. The pretrained Chinese JobBERT model, tokenizer, configuration files, and model card are available at [HUGGING FACE MODEL URL].

---

## Code review

- [ ] Public scripts no longer contain laboratory absolute paths (`/home/guojingli3/...`).
- [ ] No `openai` / Moonshot / Anthropic keys, cookies, or `.env` files.
- [ ] Sister-project (IEEE Access / SRICL) code and English six-dataset claims are absent.
- [ ] Scorer string is `cnss-lskt-1.2.0`.
- [ ] Trainers match `scripts/train_cn_roberta_crf.py` (do not invent a second entry point).

## Clean installation test

- [ ] Fresh environment: `python3 -m pip install -r requirements-repro.txt`.
- [ ] `python3 scorer/test_regression.py` exits 0.
- [ ] Training extra deps documented only from the parent `requirements.txt` pins.

## End-to-end reproduction test

- [ ] `python3 scripts/eval_hybrid_cws_simhuman.py` reproduces `tables/hybrid_cws_simhuman980_all_models.csv` cells for Chinese JobBERT 3M (**0.433118** typed exact) and ChatGPT (**0.285361** / **0.624869**).
- [ ] Direct `score_lskt.py` on `data/frozen_preds/jobbert_3m_v4.jsonl` **without** jieba snap is documented as **not** the paper headline (workspace check: 0.2552).
- [ ] Gold v2 appendix command still yields ChatGPT typed **0.6365** and is not written into the abstract.

## Dataset validation

- [ ] SHA-256 of the V4 hybrid is `2ad6342d8b762cf1abb289295315e2521bec0c540f4320113409fceab0818d99`.
- [ ] SHA-256 of Gold v2 is `7a26e32b89d4e501175cb96443e35e171cea08d91501d2a32779b96ee8504ff6`.
- [ ] Corpus counts remain 17,460 / 2,143 / 3,237 (total **22,840**).
- [ ] Evaluation ID count remains **2,601**.
- [ ] `repartition_v1` is labelled as a draft split, not main gold.
- [ ] Schema matches the dataset card (`list_of_selection_bio4`, no ESCO IDs).

## Removal of secrets and personal data

- [ ] No API keys, tokens, or private emails in the public tree.
- [ ] Annotator packs with comments / model suggestions reviewed.
- [ ] `[TODO: personal-data review of job titles and sentences]`.

## Copyright and redistribution rights

- [ ] **[TODO: written confirmation]** that original advertisement text from the four sources may be redistributed.
- [ ] Raw `应届生招聘大数据*.csv` and `人工智能招聘大数据2025年.xlsx` are **excluded** unless that confirmation covers them.
- [ ] MLM dumps `data/jobbert_*_sents.jsonl` excluded or cleared.
- [ ] If full text cannot be released, implement a tags-and-IDs-only package and rewrite the Data Availability statement.

## Code licence confirmation

- [ ] `[TODO: choose SPDX for scorer and scripts]`.
- [ ] Add a root `LICENSE` file (none is present today).

## Data licence confirmation

- [ ] `[TODO: choose a data licence or a split licence (annotations vs. text)]`.
- [ ] Do not advertise CC-BY until rights are clear.

## Base-model licence compatibility

- [ ] `[TODO: record the licence of hfl/chinese-roberta-wwm-ext from Hugging Face]`.
- [ ] Chinese JobBERT public licence is compatible with that base licence and with training-data rights.
- [ ] Local snapshot has no `LICENSE` file; do not guess Apache-2.0 in the card until verified.

## Hugging Face Model Card validation

- [ ] YAML front matter parses.
- [ ] Names: **Chinese JobBERT**, **Chinese-SkillSpan**.
- [ ] Licence field remains `other` until the item above is done.
- [ ] Loading example still matches `BertCRF` (not a fake `pipeline`).

## Hugging Face Dataset Card validation

- [ ] YAML front matter parses.
- [ ] Size 22,840 and 2,601 IDs both stated.
- [ ] Real schema documented (`list_of_selection_bio4`).
- [ ] Rights TODO still visible.

## Zenodo metadata validation

- [ ] `.zenodo.json` is valid JSON.
- [ ] Creator order matches the paper.
- [ ] Grant **21BGL142** appears.
- [ ] No invented community.
- [ ] `related_identifiers` placeholders replaced with real URLs/DOIs (invalid placeholder strings will fail Zenodo ingest).

## DOI creation

- [ ] GitHub repository exists and is **public**.
- [ ] Zenodo–GitHub integration or a manual deposit creates a version DOI.
- [ ] Concept DOI (if any) recorded separately from the version DOI.

## GitHub release tag

- [ ] `[TODO: tag name]`.
- [ ] Release assets match `release/zenodo/RELEASE_MANIFEST.md`.
- [ ] Private backup `https://github.com/AlfredJamesLi/chinese-skillspan-benchmark` is not presented as the archival URL.

## Synchronise URLs

Replace every `[TODO: … URL]` / DOI in:

- [ ] Manuscript Data Availability paragraph
- [ ] PeerJ submission form
- [ ] `README.md`
- [ ] `CITATION.cff`
- [ ] `DATA_AVAILABILITY.md`
- [ ] `release/huggingface-model/README.md`
- [ ] `release/huggingface-dataset/README.md`
- [ ] `release/zenodo/.zenodo.json`

Use the **same** GitHub URL, the **same** Zenodo DOI, and the **same** Hugging Face dataset/model URLs everywhere. Do not paste the arXiv abstract URL into the dataset or model fields.

## Legacy Google Sites page

- [ ] https://sites.google.com/view/cn-skillspan-resources either points to the DOI / GitHub / Hugging Face trio or is clearly labelled “homepage, not archive”.
- [ ] PeerJ form does **not** list that Sites URL as the dataset DOI.

## Reviewer download test

- [ ] An incognito browser can download dataset, code, and model card **without** requesting access.
- [ ] GitHub is public (the current working backup is private).
- [ ] Hugging Face repos are public (or have a documented gated-but-automatic licence click that PeerJ accepts).
- [ ] Zenodo files match the manifest checksums.

## Consistency gate

- [ ] Title string is exactly: `Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements`.
- [ ] Author order is exactly: Guojing Li, Zichuan Fu, Junyi Li, Wenlin Zhang, Kaifeng Guo, Jinning Yang, Jingtong Gao, Xiangyu Zhao.
- [ ] Corresponding author: Xiangyu Zhao.
- [ ] Dataset name **Chinese-SkillSpan**; model name **Chinese JobBERT**.
- [ ] Funding: National Social Science Fund of China, Grant No. **21BGL142**.
- [ ] Inconsistencies (22,840 vs. two splits; 3,237 vs. 2,601; V4 vs. Gold v2; draft PDF filenames) remain **reported**, not silently “fixed”.

## Publication sequence (do not skip)

1. Finalise local files and licences (this checklist).
2. Create the **public** GitHub repository.
3. Create a **versioned GitHub Release**.
4. Archive that release in **Zenodo** and obtain a DOI.
5. Publish the Hugging Face **dataset** and **model** repositories.
6. Update every link listed above (including the Sites homepage).
7. Enter the permanent links in the **PeerJ** form.

Do not invert steps 4–7 (PeerJ must not receive a private GitHub URL or a Sites page as the archive).
