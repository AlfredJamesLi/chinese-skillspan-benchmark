# Chinese-SkillSpan

**Chinese-SkillSpan** is a benchmark for competency span extraction from Chinese job advertisements. **JobBERT-zh** is the accompanying Chinese job-domain encoder used as a reproducible baseline.

Manuscript under review at **PeerJ Computer Science** (single-anonymized review: reviewers see author names). The source manuscript is maintained on Overleaf; this repository does not host a draft PDF.

| Resource | URL |
|---|---|
| Code and data | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark |
| Versioned archive (`v0.1.1`) | https://doi.org/10.5281/zenodo.22288338 |
| Concept DOI | https://doi.org/10.5281/zenodo.22288337 |
| JobBERT-zh (V4; hybrid 2601 exact **0.4331**) | https://huggingface.co/AlfredJames/jobbert-zh |
| JobBERT-zh v6a (Gold150 B2 exact **0.5536±0.0054**) | https://huggingface.co/AlfredJames/jobbert-zh-v6a |

Do not send reviewers through a Google Sites or Drive page. There is no separate Hugging Face dataset repository; use GitHub Release `v0.1.1` or the Zenodo record. Zenodo `v0.1.1` does **not** contain Gold150. Do not rank 0.5536 against 0.4331 in one table.

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

A later Handbook-B human diagnostic (project-26 first **85** official spans + the frozen **50-sentence calibration cohort**, artifact **IAA-50**, plus span-length bins) is in [`reports/human_gold85_iaa50/`](reports/human_gold85_iaa50/README.md). Independent-coding evidence on that report is for the **initial independent-coding study**, not for the full 150-sentence human reference set. On that gold, typed exact scales with instruction-model size (JobBERT-zh CRF **0.13** / Qwen2.5-14B SOP+jieba **0.26** / Kimi on IAA-50 **0.62**). **Not** a replacement for V4 hybrid JobBERT 3M **0.4331**.

Reader names for Gold150, Silver-plus, B1/B2, and H/E/M: [`docs/TERMINOLOGY_CROSSWALK.md`](docs/TERMINOLOGY_CROSSWALK.md).

---

## Silver-plus and the human reference set (manuscript body)

**Silver-plus** is the resource **release-layer** name for teacher-generated silver annotations (LLM-annotated silver data with automated validation and sampled human review). Plus is not a recognised quality grade. The layer is not item-by-item human verified and is not near-Gold. Review status and adjudication status are recorded separately.

A **150-sentence human-annotated reference set** (artifact **Gold150**; file `gold150_test.jsonl`, not renamed) is used for **scoring only**. After this mention, this README calls it **the human reference set**. It is not independent dual-blind coding of all 150 sentences. It comprises a **100-sentence challenge cohort** (split `gold100_page1`) and a **50-sentence calibration cohort** (split `iaa50`). Isolation wording remains **sentence-level isolation (extended)**; do not call it document isolation after v4.

Methods and Gold150 numbers intended for the PeerJ **main text** — including the JobBERT-zh CRF (no prompt) versus Qwen2.5-14B JSON-offset LoRA (fixed prompt, no demonstrations) — are in [`docs/paper_body_silver_plus.md`](docs/paper_body_silver_plus.md). B1/B2 keep those condition codes and compare **earlier** versus **revised** supervision (handbook + teacher + adjudication). H/E/M are conflict-origin / non-conflict-origin / mixed training conditions, not an objective difficulty taxonomy.

That section does **not** replace V4 hybrid JobBERT 3M **0.4331**. Official Qwen P0 remains **0.1215±0.0092**. A later P1 / SOP-on-Gold150 / watermark-peel contrast is archived in [`notes/gold150_followups_20260909/`](notes/gold150_followups_20260909/README.md) and the Overleaf E/F/G pack [`notes/silver_plus_followups_20260909/`](notes/silver_plus_followups_20260909/README.md) and does **not** replace Tables A–D. Tentative Gold150 main cell: JobBERT-zh 3M, v6a, B2 typed exact **0.5536±0.0054** (n=3 sample SD). Qwen JSON-offset is a supplement and is **not** official SOP extract **0.1724**.

### Figure 1 (workflow)

The manuscript overview figure is archived as `notes/manuscript_display_archive_20260910/displays/figure_01.tex`. Read it as:

1. Multi-source Chinese corpus → human-led specification and the human reference set.
2. Frozen specification / prompts + candidate text → teacher-generated Silver-plus.
3. Eligible silver supervision → JobBERT-zh + CRF and Qwen2.5-14B-Instruct + LoRA.
4. The human reference set enters scoring only.
5. Domain-adaptive pre-training is the JobBERT branch.
6. LLM inference baselines and teacher annotation are different roles.

The figure does **not** mean that every system shares one protocol, or that later rows are a fresh independent blind test.

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

Weights are not stored in Git. Encoder + V4 CRF (0.4331): https://huggingface.co/AlfredJames/jobbert-zh. Gold150 v6a B2 continuation (0.5536±0.0054): https://huggingface.co/AlfredJames/jobbert-zh-v6a.

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
docs/                   # manuscript-body drafts; reader terminology in TERMINOLOGY_CROSSWALK.md
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

Related English dataset (cite, do not host the PDF here): Zhang et al., 2022, *SkillSpan: Hard and Soft Skill Extraction from English Job Postings*, NAACL-HLT, https://aclanthology.org/2022.naacl-main.366/.

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
- The 150-sentence human reference set is not a freshly blinded re-test of every protocol; handbook-development exposure and sentence-level isolation remain in force.
- Job advertisements can contain employer names and workplace locations. Do not scrape, republish, or re-identify individuals.
- Domain shift across the four sources is large.
- Do not use the resource to profile applicants, infer protected attributes, or claim ESCO concept-ID accuracy.

---

## Acknowledgements

This work was supported by the National Social Science Fund of China, Grant No. **21BGL142**.
