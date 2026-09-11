# Chinese-SkillSpan

**Chinese-SkillSpan** is a benchmark for competency span extraction from Chinese job advertisements. **JobBERT-zh** is the accompanying Chinese job-domain encoder used as a reproducible baseline.

Manuscript under review at **PeerJ Computer Science** (single-anonymized review: reviewers see author names). The source manuscript is maintained on Overleaf; this repository does not host a draft PDF.

![Chinese-SkillSpan workflow](figures/fig_pipeline_overview.jpg)

Draft overview: (a) corpus construction and annotation; (b) domain pretraining, student fine-tuning, and scoring. This figure is a working sketch, not a camera-ready plate.

| Resource | URL |
|---|---|
| Code and data | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark |
| Current archive (`v0.1.3`, includes the human reference set) | https://doi.org/10.5281/zenodo.22698504 |
| Previous snapshot (`v0.1.2`) | https://doi.org/10.5281/zenodo.22685143 |
| First snapshot (`v0.1.1`) | https://doi.org/10.5281/zenodo.22288338 |
| Concept DOI | https://doi.org/10.5281/zenodo.22288337 |
| JobBERT-zh (paper-main encoder, V4 hybrid) | https://huggingface.co/AlfredJames/jobbert-zh |
| JobBERT-zh 1M (DAPT contrast) | https://huggingface.co/AlfredJames/jobbert-zh-1m |
| JobBERT-zh v6a (human-reference B2 continuation) | https://huggingface.co/AlfredJames/jobbert-zh-v6a |

Do not send reviewers through a Google Sites or Drive page. There is no separate Hugging Face dataset repository. Hugging Face user `AlfredJames` is not the GitHub user `AlfredJamesLi`. The 150-sentence **human reference set** (`data/gold150_test.jsonl`) is in GitHub Release / Zenodo **`v0.1.3`**, not in `v0.1.1` or `v0.1.2`. Paper-main JobBERT-zh typed exact is **0.4331** on V4 hybrid 2,601. The v6a human-reference cell **0.5536±0.0054** is a later protocol; do not rank the two numbers in one table.

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

A later Handbook-B human diagnostic (project-26 first **85** official spans + frozen **IAA-50**, plus span-length bins) is in [`reports/human_gold85_iaa50/`](reports/human_gold85_iaa50/README.md). On that gold, typed exact scales with instruction-model size (JobBERT-zh CRF **0.13** / Qwen2.5-14B SOP+jieba **0.26** / Kimi on IAA-50 **0.62**). **Not** a replacement for V4 hybrid JobBERT 3M **0.4331**.

The **human reference set** (`data/gold150_test.jsonl`: 150 sentences = challenge cohort + calibration cohort) and Silver-plus B2 teacher files (`data/silver_plus_v6a_nocross/`, 2,150 / 169) are in GitHub Release / Zenodo **`v0.1.3`**. They are a later protocol, not the abstract gold, and they are not in Zenodo `v0.1.1` or `v0.1.2`. Paper names and repository identifiers: [`data/gold150/README.md`](data/gold150/README.md). See also [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) and [notes/SILVER_PLUS_EXTENSION_PROVENANCE.md](notes/SILVER_PLUS_EXTENSION_PROVENANCE.md).

---

## Human reference set and Silver-plus (manuscript body)

The manuscript names the frozen 150-sentence evaluation **human reference set** (challenge cohort + calibration cohort). Laboratory identifier **Gold150** and filename `gold150_test.jsonl` stay in Appendix D / this repository (`data/gold150/README.md`). Methods and human-reference numbers intended for the PeerJ **main text** — including the JobBERT-zh CRF (no prompt) versus Qwen2.5-14B JSON-offset LoRA (fixed prompt, no demonstrations) — are in [`docs/paper_body_silver_plus.md`](docs/paper_body_silver_plus.md).

That section does **not** replace V4 hybrid JobBERT 3M **0.4331**. Official Qwen P0 remains **0.1215±0.0092**. A later P1 / SOP-on-human-reference / watermark-peel contrast is archived in [`notes/gold150_followups_20260909/`](notes/gold150_followups_20260909/README.md) and the Overleaf E/F/G pack [`notes/silver_plus_followups_20260909/`](notes/silver_plus_followups_20260909/README.md) and does **not** replace Tables A–D. Tentative human-reference main cell: JobBERT-zh 3M, v6a, B2 typed exact **0.5536±0.0054** (n=3 sample SD). Qwen JSON-offset is a supplement and is **not** official SOP extract **0.1724**.

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

Paper-main encoder and LLM rows (jieba-aligned). The eval script is **read-only** on the hybrid gold (SHA-256 `2ad6342d…`); it does not rewrite that file:

```bash
python3 scripts/eval_hybrid_cws_simhuman.py --paper-main-only --use-frozen
```

When `output/` is absent, or with `--use-frozen`, JobBERT-zh v4 rows come from `data/frozen_preds/`. The human-reference freeze uses `source_id` and Doccano type names; convert before scoring. JSON-offset Qwen (**0.1215±0.0092**) is not shared-handbook SFT (**0.5403±0.0354**) and is not V4 hybrid **0.4331**:

```bash
python3 scripts/convert_gold150_to_bio.py
python3 scripts/test_qwen_ext_parser.py
python3 scripts/eval_gold150_ext.py \
  --protocol json_offset \
  --pred path/to/gold150_predictions.jsonl \
  --out output/gold150_score.json
# Optional: after convert_gold150_to_bio.py, score_lskt can read the derived BIO file
# data/gold150_test.bio.jsonl (gitignored; not in the clone).
```

Do not overwrite `data/gold150_test.jsonl`. Qwen LoRA adapters are not in this release. CRF training uses `requirements-train.txt` and Hub `AlfredJames/jobbert-zh` (see [REPRODUCIBILITY.md](REPRODUCIBILITY.md) §7). `--smoke` checks that the trainer loads; it is not the abstract F1. An independent second-host check (2026-09-11, git `09897d9`, jieba 0.42.1) matched the P0 paper-main cells and left both freeze SHA-256 values unchanged.

Weights are not stored in Git. Encoder + V4 CRF (0.4331): https://huggingface.co/AlfredJames/jobbert-zh. Human-reference v6a B2 continuation (0.5536±0.0054): https://huggingface.co/AlfredJames/jobbert-zh-v6a.

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
requirements-train.txt
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
  gold150_test.jsonl    # human reference set (artifact Gold150); Zenodo v0.1.3
  silver_plus_v6a_nocross/
docs/                   # manuscript-body drafts
notes/handbooks/        # Handbook B (paper SOP; v4.2.14)
figures/fig_pipeline_overview.jpg
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
  doi          = {10.5281/zenodo.22698504},
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
- Job advertisements can contain employer names and workplace locations. Do not scrape, republish, or re-identify individuals.
- Domain shift across the four sources is large.
- Do not use the resource to profile applicants, infer protected attributes, or claim ESCO concept-ID accuracy.

---

## Acknowledgements

This work was supported by the National Social Science Fund of China, Grant No. **21BGL142**.
