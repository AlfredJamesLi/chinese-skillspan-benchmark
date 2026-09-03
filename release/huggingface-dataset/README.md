---
language:
  - zh
pretty_name: Chinese-SkillSpan
task_categories:
  - token-classification
task_ids:
  - named-entity-recognition
size_categories:
  - 10K<n<100K
tags:
  - chinese-skillspan
  - job-advertisements
  - competency-extraction
  - span-extraction
  - lskt
license: other
# [TODO: dataset licence after redistribution rights for advertisement text are confirmed]
# [TODO: Hugging Face dataset repo id]
---

# Dataset card: Chinese-SkillSpan

**Chinese-SkillSpan** is a Chinese job-advertisement corpus for **competency span extraction**. Models such as **Chinese JobBERT** are evaluated on this resource.

`[TODO: Hugging Face dataset URL]` · `[TODO: Zenodo DOI]` · Code: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark

---

## Dataset description

Each record is one sentence (or sentence-like segment) from a Chinese recruitment notice, with character-level tokens and flat BIO labels in four types (LSKT). The resource does **not** contain ESCO concept IDs.

The manuscript title used for this release is:

> Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements

Draft PDFs in the laboratory tree still use an older “ESCO-Aligned” / DASFAA filename. That filename is not the dataset name.

---

## Task definition

**Input:** a Chinese job-advertisement sentence.  
**Output:** a set of non-overlapping typed spans.  
**Types:** L (language), K (knowledge), S (skill / tool), T (trait).  
**Primary metric:** typed exact micro-F1 (`cnss-lskt-1.2.0`, `--align-mode official`). Relaxed F1 uses IoU ≥ 0.5.

Paper-main test labels are the **V4 hybrid** (derived). Gold v2 is a separately frozen human/Doccano-derived file on the **same 2,601 IDs**. Do not mix the two protocols when reporting a single SOTA number.

---

## Dataset size and source composition

**Corpus (Table 1), verified by counting `data/corpus_splits/*.json`:**

| Split | Sentences | 人工智能招聘 | 应届生招聘 | 阿里云公开数据集 | 事业单位招聘 |
|---|---:|---:|---:|---:|---:|
| train | 17,460 | 7,148 | 10,312 | 0 | 0 |
| development | 2,143 | 2,143 | 0 | 0 | 0 |
| test (full split) | 3,237 | 1,423 | 0 | 473 | 1,341 |
| **Total** | **22,840** | 10,714 | 10,312 | 473 | 1,341 |

Four Chinese recruitment sources appear in the files. The Table 1 split is source-imbalanced (see [REPRODUCIBILITY.md](../../REPRODUCIBILITY.md)).

**Inconsistency (do not hide):** `data/repartition_v1` also sums to 22,840 but uses `16,350` / `2,268` / `4,222`. That assignment is a draft and is **not** the paper-main gold.

**Evaluation gold (2,601 unique IDs), not the full 3,237-row test split:**

| File | IDs | Role |
|---|---:|---|
| `test_lskt_v4_cws_simhuman980_hybrid.jsonl` | 2,601 | Paper main (980 SimHuman rule_v4 + 1,621 SOP-CWS) |
| `gold_canonical_v2.jsonl` | 2,601 | Provenance / appendix (same IDs, different spans) |
| Raw Doccano export (not in the Hugging Face preview) | 2,676 rows → 2,601 IDs | Construction history |
| `human_gold_page1_200.jsonl` | 200 | Human overlay; not abstract gold |

---

## Annotation schema and categories

Handbook B (`B.sop_v4.2.1`):

| Tag | Meaning (English handbook) |
|---|---|
| L | Language name, proficiency, or language exam/certificate (e.g. 英语, CET-6, 日语N2) |
| K | Degree, major, domain knowledge, technical or occupational certification (non-language) |
| S | Tool, method, executable skill |
| T | Trait / soft skill |

Optional evaluation-only Zhang projection (L+K → KNOWLEDGE, S+T → SKILL) is **not** stored as a field in the JSONL.

---

## Span-boundary rules (Handbook B)

- Contiguous original substring; **no mid-word cuts**; flat, **non-overlapping**.
- Prefer short complete spans (handbook: **2–8** tokens as a preference, not a hard filter).
- Split independent coordinated skills; mark the **object** of 熟悉 / 掌握 / 精通 / 了解, not the verb.
- Job-use tools and programming languages → **S**; course / principle / basics / syntax → full knowledge NP as **K**.
- CET-6 / 英语六级 → **L** under Handbook B (Gold v2 / Handbook A placed CET-6 in **K**; that file must not be relabelled).
- Application / medical / notice / benefit boilerplate → empty.
- No `L > S > K > T` type priority.

---

## Train / development / test splits

Use `data/corpus_splits/{train,dev,test}.json` for the 22,840-sentence resource.

For the **paper-main benchmark score**, evaluate on the V4 hybrid JSONL (2,601 IDs), not on all 3,237 test sentences.

CRF training for the main encoder row uses V4 **silver** (`train_lskt_v4_silver.jsonl` / `dev_lskt_v4_silver.jsonl`), not Gold v2.

---

## Recommended loading example

Records are JSON Lines (gold / hybrid / silver) or a JSON array (corpus splits). Schema is **not** CoNLL-2003 columns.

```python
from datasets import load_dataset

# After the public repository exists:
# ds = load_dataset("[TODO: Hugging Face dataset id]")

# Local files from this paper repository:
gold = load_dataset(
    "json",
    data_files="data/test_lskt_v4_cws_simhuman980_hybrid.jsonl",
    split="train",
)
assert gold.num_rows == 2601
row = gold[0]
assert "id" in row and "list_of_selection_bio4" in row
```

```python
import json
from pathlib import Path

train = json.loads(Path("data/corpus_splits/train.json").read_text(encoding="utf-8"))
assert len(train) == 17460
```

---

## Field-level data dictionary (from the files)

Fields vary by file. The following were read from actual records.

### Shared / typical fields

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Sentence id (`{global}-{sNNNN}`) |
| `global_id` | int or string | Parent advertisement id |
| `sentence_order` | int | Order within the advertisement |
| `sentence` | string | Original sentence text |
| `tokens` | list[string] | Character tokens (same length as the BIO sequence) |
| `list_of_selection_bio4` | list[string] | Official LSKT BIO tags |
| `source_domain` | string | One of the four source labels |
| `title` | string | Job title line (may include employer name) |

### Gold v2 extras (`gold_canonical_v2.jsonl`)

| Field | Meaning |
|---|---|
| `skill_spans` | Inclusive character offset pairs |
| `tags_skill`, `tags_skill_clean` | Legacy skill-only BIO |
| `list_of_selection` | Untyped `B`/`I`/`O` |
| `sentence_with_tags`, `sentence_with_tags_4d` | Display strings |
| `_canon` | Unique-ID adjudication metadata |

### V4 hybrid extras (`test_lskt_v4_cws_simhuman980_hybrid.jsonl`)

| Field | Meaning |
|---|---|
| `hybrid_source` | `simhuman980_cws` or `sop_cws` |
| `v4_spans`, `cws_spans` | Derived span triples `[start, end, type]` |
| `v4_source`, `cws_source`, `cws_n_changed` | Provenance of the snap |

### Frozen predictions (`data/frozen_preds/*.jsonl`)

| Field | Meaning |
|---|---|
| `pred_tags` | Model BIO sequence (also copied to `list_of_selection_bio4`) |

There is **no** `esco_id` field.

---

## Annotation and adjudication

- Gold v2: Doccano-derived labels, unique-ID freeze, 18 conflicts adjudicated (protocol note 2026-08-22). Table 2 IAA in older drafts (n=100, exact 0.532 / κ 0.554) is **Gold-era**, not V4.
- V4 hybrid: **not** a second full human pass. 980 IDs are SimHuman `rule_v4`; 1,621 are SOP-CWS; both are jieba-snapped.
- Human page-1 200: first 200 of a 980-sentence queue; annotator display names appear in internal packs; **not** dual-blind IAA.
- Official annotator SOP: Handbook B only. Handbook A is provenance.

`[TODO: publish the exact IAA design for any future full-human V4 gold.]`

---

## Evaluation considerations

- Score with `scorer/score_lskt.py --align-mode official`.
- Jieba-snap predictions when comparing to the V4 hybrid.
- One prediction per gold `id`.
- Do not use the v1.0–v1.1 global-set scorer (inflated F1).

Verified paper-main cells: Chinese JobBERT 3M typed exact **0.4331**; ChatGPT dump+jieba **0.2854** / relaxed **0.6249** (`tables/hybrid_cws_simhuman980_all_models.csv`).

---

## Source and length effects

- Development data are entirely `人工智能招聘`.
- Graduate (`应届生招聘`) sentences occur in train only under Table 1.
- Cloud and public-institution sentences occur in test only.
- Gold v2 notes record much lower encoder F1 on 事业单位招聘 than on 人工智能招聘. Treat source as a shift variable, not as a balanced stratum.

Length statistics for publication: `[TODO: add a verified token-length table from corpus_splits if required by PeerJ]`.

---

## Known limitations

- Paper-main test file is derived, not fully human.
- Character BIO can disagree with jieba word boundaries.
- Titles may contain employer names.
- `repartition_v1` and Table 1 must not be treated as one split.
- No Time-OOD year field is guaranteed on Gold v2.

---

## Personal-data and copyright assessment

- **Copyright / platform terms:** **unverified**. Original advertisements come from four recruitment sources. This card does **not** claim that the full raw text is openly licensed. `[TODO: author confirmation of redistribution rights]`.
- **Personal data:** not a dedicated PII corpus; workplace and organisation names appear. `[TODO: formal personal-data review]`.
- Raw CSV / XLSX source dumps that exist in the laboratory tree are **out of scope** for the public Hugging Face dataset until cleared.

---

## Appropriate and inappropriate uses

**Appropriate:** academic research on span extraction; training and evaluating Chinese JobBERT; reproducing committed tables.

**Inappropriate:** scraping additional ads without permission; re-identifying people or firms for outreach; applicant ranking in production; uploading extra copyrighted postings in pull requests.

---

## Citation

Guojing Li, Zichuan Fu, Junyi Li, Wenlin Zhang, Kaifeng Guo, Jinning Yang, Jingtong Gao, Xiangyu Zhao. *Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements*. `[TODO: year, PeerJ / arXiv]`.

Funding: National Social Science Fund of China, Grant No. **21BGL142**.

See [`CITATION.cff`](../../CITATION.cff).

---

## Licence

```
license: other
```

`[TODO: assign a data licence (or a dual licence for annotations vs. text) only after Section 7 of DATA_AVAILABILITY.md is resolved.]`

---

## Links

| Resource | URL |
|---|---|
| GitHub | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark |
| Zenodo | `[TODO: Zenodo DOI]` |
| JobBERT-zh | https://huggingface.co/AlfredJames/jobbert-zh |
| Paper | `[TODO: this paper's arXiv / PeerJ URL]` |
