# Chinese-SkillSpan

**Chinese-SkillSpan** is a benchmark for competency span extraction from Chinese job advertisements. **JobBERT-zh** is the accompanying Chinese job-domain encoder used as a reproducible baseline.

Venue recorded here: **PeerJ Computer Science**. Draft PDF filenames that still mention DASFAA or “ESCO-Aligned” are local drafts only.

| Resource | URL |
|---|---|
| Code and data | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark |
| Versioned archive (`v0.1.1`) | https://doi.org/10.5281/zenodo.22288338 |
| Concept DOI | https://doi.org/10.5281/zenodo.22288337 |
| JobBERT-zh | https://huggingface.co/AlfredJames/jobbert-zh |

Do not send reviewers through a Google Sites or Drive page. There is no separate Hugging Face dataset repository; use GitHub Release `v0.1.1` or the Zenodo record.

---

## Task

Each record is one sentence from a Chinese recruitment notice. The model must recover **flat, non-overlapping** character spans in four types (LSKT):

| Tag | Meaning |
|---|---|
| L | Language skills and knowledge |
| K | Knowledge |
| S | Occupational skills |
| T | Transversal skills and competences |

The inventory is ESCO-derived at the **type** level. This release does **not** include ESCO concept IDs.

**Primary metric:** typed exact-span micro-F1 (`cnss-lskt-1.2.0`, identifier-strict). Relaxed F1 uses IoU ≥ 0.5.

---

## Corpus

**22,840 sentences** from four Chinese recruitment sources. The paper-main split is:

| Split | Sentences |
|---|---:|
| train | 17,460 |
| development | 2,143 |
| test | 3,237 |
| **Total** | **22,840** |

A later draft assignment (`repartition_v1`: 16,350 / 2,268 / 4,222) sums to the same *N* and is **not** the main gold.

The evaluation reference uses **2,601** unique test IDs (not all 3,237 test sentences). Two label files share those IDs and must not be ranked in one sentence:

| Protocol | File | Role | Headline typed exact F1 |
|---|---|---|---|
| **V4 / Handbook B (paper main)** | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | Abstract and main results | JobBERT-zh 3M **0.4331**; frozen ChatGPT dump + jieba **0.2854** exact / **0.6249** relaxed |
| **Gold v2 / Handbook A** | `data/gold_canonical_v2.jsonl` | Construction history / appendix | ChatGPT **0.6365** |

The V4 hybrid is **derived** (980 SimHuman rule_v4 spans + 1,621 SOP-CWS spans). It is not a fully human Doccano gold. Do not overwrite `gold_canonical_v2.jsonl`.

A first-page human overlay of **200** sentences is at `data/human_gold_page1_200.jsonl`. It is not the abstract gold. Checksums live in [REPRODUCIBILITY.md](REPRODUCIBILITY.md), not in running prose.

---

## Quick start

```bash
python3 -m pip install -r requirements-repro.txt
python3 scorer/test_regression.py
python3 scorer/score_lskt.py \
  --gold data/test_lskt_v4_cws_simhuman980_hybrid.jsonl \
  --pred path/to/predictions.jsonl \
  --align-mode official
```

Predictions must use the same sentence `id`s as gold. Scoring `data/frozen_preds/jobbert_3m_v4.jsonl` **without** jieba snap yields typed exact F1 **0.2552** and is **not** the paper headline.

Paper-main encoder and LLM rows (jieba-aligned):

```bash
python3 scripts/eval_hybrid_cws_simhuman.py
```

That script writes `tables/hybrid_cws_simhuman980_all_models.csv`. When `output/` is absent it falls back to `data/frozen_preds/` for the JobBERT-zh v4 rows. Several trainers still contain a laboratory root path; see [REPRODUCIBILITY.md](REPRODUCIBILITY.md) before retraining.

Weights are not stored in Git. Encoder + V4 CRF: https://huggingface.co/AlfredJames/jobbert-zh.

---

## Repository layout

```
README.md
REPRODUCIBILITY.md
DATA_AVAILABILITY.md
CITATION.cff
CHANGELOG.md
CONTRIBUTING.md
requirements-repro.txt
scorer/                 # cnss-lskt-1.2.0
scripts/
data/
  corpus_splits/        # train / dev / test (22,840)
  gold_canonical_v2.jsonl
  test_lskt_v4_cws_simhuman980_hybrid.jsonl
  train_lskt_v4_silver.jsonl
  dev_lskt_v4_silver.jsonl
  frozen_preds/
  human_gold_page1_200.jsonl
notes/handbooks/        # Handbook B (paper SOP)
tables/
release/                # Hugging Face and Zenodo templates
```

---

## Citation

```bibtex
@misc{li2026chineseskillspan,
  title        = {Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements},
  author       = {Li, Guojing and Fu, Zichuan and Li, Junyi and Zhang, Wenlin and Guo, Kaifeng and Yang, Jinning and Gao, Jingtong and Zhao, Xiangyu},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.22288338},
  url          = {https://github.com/AlfredJamesLi/chinese-skillspan-benchmark}
}
```

Machine-readable metadata: [`CITATION.cff`](CITATION.cff).

**Authors (order fixed).** Guojing Li<sup>1,2,†</sup>, Zichuan Fu<sup>2,†</sup>, Junyi Li<sup>2</sup>, Wenlin Zhang<sup>2</sup>, Kaifeng Guo<sup>2</sup>, Jinning Yang<sup>2</sup>, Jingtong Gao<sup>2</sup>, Xiangyu Zhao<sup>2</sup>.

1. Renmin University of China  
2. City University of Hong Kong  
† Equal contribution.

Corresponding author: Xiangyu Zhao (`xianzhao@cityu.edu.hk`).

---

## Licence

Code and dataset licences are **not yet assigned**. Do not treat the raw advertisement wording as CC-BY or any other open licence. JobBERT-zh is `other` on Hugging Face until job-ad text rights are confirmed. The Zenodo GitHub hook labelled the `v0.1.1` record `cc-by-4.0` by platform default; that is not an author licence decision. See [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md).

---

## Limitations

- Labels are flat and non-overlapping. Nested or crossing spans are out of scope.
- The paper-main V4 test file is derived, not a completed human gold.
- Job advertisements can contain employer names and workplace locations. Do not scrape, republish, or re-identify individuals.
- Domain shift across the four sources is large.
- Do not use the resource to profile applicants, infer protected attributes, or claim ESCO concept-ID accuracy.

---

## Acknowledgements

This work was supported by the National Social Science Fund of China, Grant No. **21BGL142**.
