# Data availability — Chinese-SkillSpan

This note separates **what this repository contains**, **what is already archived**, and **what must not be described as openly licensed** until the authors confirm rights.

- **Current Zenodo snapshot (`v0.1.3`, includes Gold150):** https://doi.org/10.5281/zenodo.22698504
- **Previous snapshot (`v0.1.2`):** https://doi.org/10.5281/zenodo.22685143
- **First archival snapshot (`v0.1.1`, PDF-cited, immutable):** https://doi.org/10.5281/zenodo.22288338
- **Concept DOI (all versions):** https://doi.org/10.5281/zenodo.22288337
- **GitHub:** https://github.com/AlfredJamesLi/chinese-skillspan-benchmark — tag `v0.1.3` matches this Zenodo version.

---

## 1. What can be publicly redistributed (pending author confirmation)

The following are *candidates* for a public GitHub + Zenodo + Hugging Face release. **Job-advertisement prose is not openly licensed until confirmed** (Section 7).

| Material | In this tree | Public redistribution |
|---|---|---|
| Annotation guidelines (Handbook B v4.2.14 and English summary) | `notes/handbooks/` | Yes, if authors own the text (laboratory-authored) |
| Official scorer and evaluation scripts | `scorer/`, `scripts/` | Yes, after a code licence is chosen and laboratory paths are stripped |
| Predefined Table 1 split *indices* / `id` lists | Embedded in `data/corpus_splits/` and gold files | IDs and split membership: yes |
| BIO annotations (`list_of_selection_bio4`) aligned to `id` | Gold, silver, and hybrid files | Derived labels: intended for release |
| Frozen encoder predictions (tags only + sentence text) | `data/frozen_preds/` | Predictions: yes; accompanying sentence text: same restriction as the corpus |
| Gold150 test freeze | `data/gold150_test.jsonl` | In GitHub tag / Zenodo `v0.1.3`; not in `v0.1.1` or `v0.1.2` |
| Silver-plus B2 `v6a_nocross` train/dev | `data/silver_plus_v6a_nocross/` | Teacher labels only; same `v0.1.3` archive |
| Committed score CSVs and this documentation | `tables/`, `docs/`, `release/` | Yes |
| JobBERT-zh weights (paper-main 3M V4) | https://huggingface.co/AlfredJames/jobbert-zh | Public model + card; licence still `other` pending text-rights confirmation |
| JobBERT-zh 1M weights (different DAPT; not a replacement) | https://huggingface.co/AlfredJames/jobbert-zh-1m | Public contrast checkpoint; not in Zenodo `v0.1.1` |
| JobBERT-zh v6a weights (Gold150 B2 CRF continuation) | https://huggingface.co/AlfredJames/jobbert-zh-v6a | Public later checkpoint; do not rank against the paper-main encoder |
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
- Gold150 (`source_id` + Doccano `label`) and Silver-plus B2 BIO teacher files
- Score tables with SHA-256-backed gold

**Not included:** ESCO concept IDs, applicant CVs, annotator identities beyond Doccano display names already in internal packs, API keys, Qwen LoRA adapters.

**Statistics that must be stated together, not collapsed:**

| Quantity | Value | Source |
|---|---:|---|
| Corpus sentences (Table 1) | 22,840 = 17,460 + 2,143 + 3,237 | `data/corpus_splits/` |
| Same *N*, other assignment | 16,350 + 2,268 + 4,222 | `data/repartition_v1` (not main gold) |
| Evaluation unique IDs (paper main) | 2,601 | Gold v2 and V4 hybrid |
| Raw Doccano Gold rows | 2,676 | Freeze protocol |
| Human overlay (page 1) | 200 | `data/human_gold_page1_200.jsonl` |
| Gold150 | 150 = Challenge-100 + Audit-50 | `data/gold150_test.jsonl` (Zenodo `v0.1.3`) |
| Silver-plus B2 `v6a_nocross` | 2,150 / 169 | `data/silver_plus_v6a_nocross/` (teacher; Zenodo `v0.1.3`) |

Source labels in the files: `人工智能招聘`, `应届生招聘`, `阿里云公开数据集`, `事业单位招聘`.

---

## 3. Where the code will be hosted

- **Public GitHub:** https://github.com/AlfredJamesLi/chinese-skillspan-benchmark (visibility **public**, verified 2026-09-04)
- **Versioned GitHub Release tag:** `v0.1.0` (first public snapshot); `v0.1.1` (Zenodo citation-metadata fix); `v0.1.2` (2026-09-10 snapshot); `v0.1.3` (2026-09-11; Gold150 + Silver-plus B2).

---

## 4. Where the archived dataset version will be hosted

- **Zenodo version DOI (`v0.1.3`, current archive; includes Gold150):** https://doi.org/10.5281/zenodo.22698504 (record https://zenodo.org/records/22698504). Related identifier: `…/tree/v0.1.3`.
- **Zenodo version DOI (`v0.1.2`):** https://doi.org/10.5281/zenodo.22685143 (record https://zenodo.org/records/22685143). Does **not** contain Gold150.
- **Zenodo version DOI (`v0.1.1`, first archival snapshot; PDF-cited):** https://doi.org/10.5281/zenodo.22288338 (record https://zenodo.org/records/22288338). This DOI is **immutable** and will always show `…/tree/v0.1.1`.
- **Zenodo concept DOI (all versions / latest):** https://doi.org/10.5281/zenodo.22288337
- **Hugging Face dataset mirror:** not published. Reviewers who want Gold150 should use GitHub Release `v0.1.3` or DOI `10.5281/zenodo.22698504`, not only `v0.1.1` / `v0.1.2`.
- Reviewers should use **GitHub**, **Hugging Face (model)**, and **Zenodo** only. Do not list a Google Sites or Drive page in the PeerJ form.
- Do not describe Gold150 as part of DOI `10.5281/zenodo.22288338` or `10.5281/zenodo.22685143`. See `notes/SILVER_PLUS_EXTENSION_PROVENANCE.md`.

---

## 5. Where the model will be hosted

Three public Hugging Face repositories. Do **not** rank the Gold150 v6a score against the paper-main V4 hybrid 2601 encoder row in one sentence.

- **Paper-main JobBERT-zh (3M V4):** https://huggingface.co/AlfredJames/jobbert-zh (**public**, verified 2026-09-04). Encoder (`model.safetensors`) and V4 CRF (`crf/best.pt`). This is the manuscript encoder URL.
- **JobBERT-zh 1M (different DAPT, same V4 protocol):** https://huggingface.co/AlfredJames/jobbert-zh-1m (**public**, verified 2026-09-07). Contrast / ablation encoder. Not a replacement for the 3M paper-main row. Not in Zenodo `v0.1.1`.
- **JobBERT-zh v6a (Gold150 B2 CRF on the same 3M encoder):** https://huggingface.co/AlfredJames/jobbert-zh-v6a (**public**, verified 2026-09-09). Later Gold150 continuation. Not a replacement for the paper-main encoder. Not in Zenodo `v0.1.1`.
- Git still does not store weights. Packaging notes: `release/huggingface-model/` (3M) and `release/huggingface-model-v6a/`. There is no `release/huggingface-model-1m/` tree in this repository; the 1M card lives on the Hub.
- Base initialisation: `hfl/chinese-roberta-wwm-ext` (Hugging Face card metadata: Apache-2.0). JobBERT-zh family cards remain `other` until job-ad text rights are confirmed.
- **Qwen2.5-14B-Instruct** (local laboratory weights) and any shared-guidelines LoRA are **not** published on those Hub repos. Do not add Gold150 LLM scores to the JobBERT cards.

---

## 6. Manuscript preprint versus data/code/model

This paper does not yet have a public preprint identifier. **An arXiv URL is not a substitute for the dataset, code, or model repository.**

Do **not** use sister-paper identifiers `2604.21525` or `2604.23009` as this paper’s preprint.

---

## 7. Copyright, platform terms, privacy, and redistribution of advertisement text

> **[TODO: authors must confirm redistribution rights for original job-advertisement text before any public upload.]**

This working tree contains:

- Full sentence strings and job `title` fields (often including employer names) inside gold, silver, corpus splits, frozen predictions, human overlay, Gold150, and Silver-plus files
- Original bulk exports (`应届生招聘大数据*.csv`, `人工智能招聘大数据2025年.xlsx`)

No licence file, terms-of-use waiver, or written permission from the four recruitment platforms is present in the repository. Therefore:

- **Do not claim** that the full raw advertisement text is openly licensed (CC-BY or otherwise).
- **Do not upload** the CSV / XLSX source dumps with the public archive until counsel or the corresponding author confirms platform terms.
- A possible restricted release (IDs + BIO tags + hashes, text on request) is **not** implemented; it is listed here only as an option for the authors if full-text rights fail.

Privacy: advertisements may include workplace locations and organisational names. They are not a curated personal-data corpus, but they are not demonstrably free of personal data either. `[TODO: complete a personal-data review before PeerJ submission]`.

---

## 8. Proposed PeerJ Data Availability Statement

Use this wording in the PeerJ form. The clickable “available at” should be **`v0.1.3`** plus the concept DOI. Keep **`v0.1.1`** as the first archival snapshot (do not delete it). Do **not** put SHA-256 values in the running paragraph; they live in `REPRODUCIBILITY.md`.

> The Chinese-SkillSpan dataset, annotation guidelines, predefined data splits, and documentation are available at https://doi.org/10.5281/zenodo.22698504 (version v0.1.3; concept DOI https://doi.org/10.5281/zenodo.22288337). Earlier snapshots are https://doi.org/10.5281/zenodo.22685143 (version v0.1.2) and https://doi.org/10.5281/zenodo.22288338 (version v0.1.1). The source code, preprocessing scripts, and evaluation tools are available at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The paper-main JobBERT-zh model, tokenizer, configuration files, and model card are available at https://huggingface.co/AlfredJames/jobbert-zh. Two later public model repositories are available at https://huggingface.co/AlfredJames/jobbert-zh-1m (1M DAPT contrast) and https://huggingface.co/AlfredJames/jobbert-zh-v6a (Gold150 B2 continuation); they do not replace the paper-main encoder. Gold150 (`data/gold150_test.jsonl`) and Silver-plus B2 train/development files (`data/silver_plus_v6a_nocross/`) are included in v0.1.3 and are not in Zenodo v0.1.1 or v0.1.2.

Longer form (optional methods paragraph):

> Chinese-SkillSpan (22,840 sentences; evaluation gold: 2,601 unique IDs under the V4 hybrid protocol) and the official scorer `cnss-lskt-1.2.0` are archived at https://doi.org/10.5281/zenodo.22698504 (v0.1.3). Earlier snapshots are https://doi.org/10.5281/zenodo.22685143 (v0.1.2) and https://doi.org/10.5281/zenodo.22288338 (v0.1.1). The source code is at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The paper-main Chinese JobBERT (JobBERT-zh) is distributed at https://huggingface.co/AlfredJames/jobbert-zh. Later public checkpoints are at https://huggingface.co/AlfredJames/jobbert-zh-1m and https://huggingface.co/AlfredJames/jobbert-zh-v6a; they are not substitutes for the paper-main encoder. Redistribution of original job-advertisement wording remains subject to the source platforms’ terms. This work was supported by the National Social Science Fund of China, Grant No. 21BGL142.

Optional Gold150 sentence (still **no** SHA-256 in the running paragraph). Use `\url` in TeX:

> A historical first 200-sentence human analysis set, `data/human_gold_page1_200.jsonl`, is distinct from the later Gold150 reference. Gold150 and versioned Silver-plus train/development manifests, checksums, and reporting scope are listed in the appendix “Silver-plus Extension Provenance” and `notes/SILVER_PLUS_EXTENSION_PROVENANCE.md`. Silver-plus records, including those reviewed by humans, retain their role as teacher supervision rather than additional Gold test labels.

---

## 9. Authors, corresponding author, and funding

Author order: Guojing Li, Zichuan Fu, Junyi Li, Wenlin Zhang, Kaifeng Guo, Jinning Yang, Jingtong Gao, Xiangyu Zhao.

- Guojing Li: Renmin University of China and City University of Hong Kong (equal contribution with Zichuan Fu).
- Zichuan Fu, Junyi Li, Wenlin Zhang, Kaifeng Guo, Jinning Yang, Jingtong Gao, Xiangyu Zhao: City University of Hong Kong.
- Corresponding author: Xiangyu Zhao (`xianzhao@cityu.edu.hk`).

National Social Science Fund of China, Grant No. **21BGL142**.
