# Data availability — Chinese-SkillSpan

This note separates **what this repository contains**, **what is already archived**, and **what must not be described as openly licensed** until the authors confirm rights. GitHub Release `v0.1.1` is archived at https://doi.org/10.5281/zenodo.22288338.

---

## 1. What can be publicly redistributed (pending author confirmation)

The following are *candidates* for a public GitHub + Zenodo + Hugging Face release. **Job-advertisement prose is not openly licensed until confirmed** (Section 7).

| Material | In this tree | Public redistribution |
|---|---|---|
| Annotation guidelines (Handbook B v4.2.1 and English one-pager) | `notes/handbooks/` | Yes, if authors own the text (laboratory-authored) |
| Official scorer and evaluation scripts | `scorer/`, `scripts/` | Yes, after a code licence is chosen and laboratory paths are stripped |
| Predefined Table 1 split *indices* / `id` lists | Embedded in `data/corpus_splits/` and gold files | IDs and split membership: yes |
| BIO annotations (`list_of_selection_bio4`) aligned to `id` | Gold, silver, and hybrid files | Derived labels: intended for release |
| Frozen encoder predictions (tags only + sentence text) | `data/frozen_preds/` | Predictions: yes; accompanying sentence text: same restriction as the corpus |
| Committed score CSVs and this documentation | `tables/`, `docs/`, `release/` | Yes |
| JobBERT-zh weights | https://huggingface.co/AlfredJames/jobbert-zh | Public model + card; licence still `other` pending text-rights confirmation |
| Raw recruitment CSV / XLSX | Present in the **working** tree (`应届生招聘大数据*.csv`, `人工智能招聘大数据2025年.xlsx`) | **Do not upload** until platform terms and copyright are confirmed |
| Continued-pretraining sentence dumps | `data/jobbert_*_sents.jsonl` | Same restriction as raw ads |
| `output/` checkpoints, caches, virtualenvs | Local only | Do not archive |

---

## 2. Annotations, IDs, splits, statistics, and derived data

Included in the candidate public dataset:

- Sentence `id` (e.g. `1802-s0004`) and optional `global_id` / `sentence_order`
- Character-level `tokens` and `list_of_selection_bio4` (tags `O`, `B-L`, `I-L`, `B-K`, `I-K`, `B-S`, `I-S`, `B-T`, `I-T`)
- Auxiliary fields present on Gold v2: `skill_spans`, `tags_skill`, `list_of_selection` (untyped B/I), `source_domain`, `title`, `_canon`
- Split membership: train / dev / test for the 22,840-sentence Table 1 corpus
- V4 hybrid metadata (`hybrid_source`: `simhuman980_cws` or `sop_cws`)
- Silver train/dev for V4 CRF
- Frozen prediction tag sequences for Chinese JobBERT 1M/3M v4
- Score tables with SHA-256-backed gold

**Not included:** ESCO concept IDs, applicant CVs, annotator identities beyond Doccano display names already in internal packs, API keys.

**Statistics that must be stated together, not collapsed:**

| Quantity | Value | Source |
|---|---:|---|
| Corpus sentences (Table 1) | 22,840 = 17,460 + 2,143 + 3,237 | `data/corpus_splits/` |
| Same *N*, other assignment | 16,350 + 2,268 + 4,222 | `data/repartition_v1` (not main gold) |
| Evaluation unique IDs | 2,601 | Gold v2 and V4 hybrid |
| Raw Doccano Gold rows | 2,676 | Freeze protocol |
| Human overlay (page 1) | 200 | `data/human_gold_page1_200.jsonl` |

Source labels in the files: `人工智能招聘`, `应届生招聘`, `阿里云公开数据集`, `事业单位招聘`.

---

## 3. Where the code will be hosted

- **Public GitHub:** https://github.com/AlfredJamesLi/chinese-skillspan-benchmark (visibility **public**, verified 2026-09-04)
- **Versioned GitHub Release tag:** `v0.1.0` (first public snapshot); `v0.1.1` (Zenodo citation-metadata fix)

---

## 4. Where the archived dataset version will be hosted

- **Zenodo version DOI (`v0.1.1`, this snapshot):** https://doi.org/10.5281/zenodo.22288338 (record https://zenodo.org/records/22288338)
- **Zenodo concept DOI (all versions):** https://doi.org/10.5281/zenodo.22288337
- **Hugging Face dataset mirror:** not published. Reviewers should use GitHub Release `v0.1.1` or the Zenodo record above.
- Reviewers should use **GitHub**, **Hugging Face (model)**, and **Zenodo** only. Do not list a Google Sites or Drive page in the PeerJ form.

---

## 5. Where the model will be hosted

- **Hugging Face model (JobBERT-zh):** https://huggingface.co/AlfredJames/jobbert-zh (**public**, verified 2026-09-04)
- Encoder (`model.safetensors`) and V4 CRF (`crf/best.pt`) are in that repository. Git still does not store weights.
- Base initialisation: `hfl/chinese-roberta-wwm-ext` (Hugging Face card metadata: Apache-2.0). JobBERT-zh remains `other` until job-ad text rights are confirmed.

---

## 6. Manuscript preprint versus data/code/model

This paper does not yet have a public preprint identifier. **An arXiv URL is not a substitute for the dataset, code, or model repository.**

Do **not** use sister-paper identifiers `2604.21525` or `2604.23009` as this paper’s preprint.

---

## 7. Copyright, platform terms, privacy, and redistribution of advertisement text

> **[TODO: authors must confirm redistribution rights for original job-advertisement text before any public upload.]**

This working tree contains:

- Full sentence strings and job `title` fields (often including employer names) inside gold, silver, corpus splits, frozen predictions, and human overlay files
- Original bulk exports (`应届生招聘大数据*.csv`, `人工智能招聘大数据2025年.xlsx`)

No licence file, terms-of-use waiver, or written permission from the four recruitment platforms is present in the repository. Therefore:

- **Do not claim** that the full raw advertisement text is openly licensed (CC-BY or otherwise).
- **Do not upload** the CSV / XLSX source dumps with the public archive until counsel or the corresponding author confirms platform terms.
- A possible restricted release (IDs + BIO tags + hashes, text on request) is **not** implemented; it is listed here only as an option for the authors if full-text rights fail.

Privacy: advertisements may include workplace locations and organisational names. They are not a curated personal-data corpus, but they are not demonstrably free of personal data either. `[TODO: complete a personal-data review before PeerJ submission]`.

---

## 8. Proposed PeerJ Data Availability Statement

Use this wording in the PeerJ form. Cite the **version** DOI for this snapshot.

> The Chinese-SkillSpan dataset, annotation guidelines, predefined data splits, and documentation are available at https://doi.org/10.5281/zenodo.22288338 (version v0.1.1; concept DOI https://doi.org/10.5281/zenodo.22288337). The source code, preprocessing scripts, and evaluation tools are available at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The pretrained JobBERT-zh model, tokenizer, configuration files, and model card are available at https://huggingface.co/AlfredJames/jobbert-zh.

Longer form (optional methods paragraph):

> Chinese-SkillSpan (22,840 sentences; evaluation gold: 2,601 unique IDs under the V4 hybrid protocol) and the official scorer `cnss-lskt-1.2.0` are archived at https://doi.org/10.5281/zenodo.22288338. The source code is at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. Chinese JobBERT (JobBERT-zh) is distributed at https://huggingface.co/AlfredJames/jobbert-zh. Redistribution of original job-advertisement wording remains subject to the source platforms’ terms. This work was supported by the National Social Science Fund of China, Grant No. 21BGL142.

---

## 9. Authors, corresponding author, and funding

Author order: Guojing Li, Zichuan Fu, Junyi Li, Wenlin Zhang, Kaifeng Guo, Jinning Yang, Jingtong Gao, Xiangyu Zhao.

- Guojing Li: Renmin University of China and City University of Hong Kong (equal contribution with Zichuan Fu).
- Zichuan Fu, Junyi Li, Wenlin Zhang, Kaifeng Guo, Jinning Yang, Jingtong Gao, Xiangyu Zhao: City University of Hong Kong.
- Corresponding author: Xiangyu Zhao (`xianzhao@cityu.edu.hk`).

National Social Science Fund of China, Grant No. **21BGL142**.
