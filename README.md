# Chinese-SkillSpan

**Chinese-SkillSpan** is a benchmark for **competency span extraction** from Chinese job advertisements. The associated encoder, **Chinese JobBERT**, is a Chinese job-domain language model used as a reproducible span-extraction baseline.

This repository contains annotation guidelines, predefined splits, preprocessing and training code, evaluation scripts, frozen prediction files for the principal encoder rows, and documentation for a public PeerJ Computer Science release.

> The working copy of this project is currently private. Public GitHub, Zenodo, and Hugging Face URLs are placeholders until the authors publish them. A legacy project page exists at [https://sites.google.com/view/cn-skillspan-resources](https://sites.google.com/view/cn-skillspan-resources); it may be kept as a homepage, but it is **not** the primary permanent archive.

**Manuscript title:** Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements.

On-disk draft PDFs in this tree still use an older filename that mentions DASFAA and “ESCO-Aligned” extraction. Treat those filenames as drafts. The submission venue recorded in this repository is **PeerJ Computer Science**.

---

## Chinese-SkillSpan and Chinese JobBERT

| Resource | Role |
|---|---|
| **Chinese-SkillSpan** | Annotated corpus and evaluation protocol for flat LSKT span extraction (Language / Knowledge / Skill / Trait) from Chinese job-advertisement sentences. |
| **Chinese JobBERT** | Domain-adapted encoder (continued masked language modelling on Chinese job text, initialised from `hfl/chinese-roberta-wwm-ext`) plus a CRF token classifier. Repository scripts also call it JobBERT-zh. |

The dataset defines the task and the gold files. Chinese JobBERT is a baseline trained on that resource. Weights are **not** stored in Git; principal encoder numbers can be reproduced from `data/frozen_preds/` plus the official scorer after the documented jieba alignment step.

---

## Main contributions

1. A Chinese job-advertisement span corpus of **22,840 sentences** drawn from **four Chinese recruitment sources**, with character-level BIO labels in four types (L, K, S, T).
2. Written annotation guidelines (Handbook B, SOP v4.2.1) and predefined train / development / test splits.
3. An official span scorer (`cnss-lskt-1.2.0`) with typed exact and relaxed (IoU ≥ 0.5) micro-F1.
4. Reproducible encoder and frozen-prediction baselines, including **Chinese JobBERT**.
5. Release documentation for GitHub, Hugging Face, Zenodo, and the PeerJ data-availability statement.

---

## Evaluation protocol (do not mix)

Two test-label files share the **same 2,601 sentence IDs** and must not be ranked against each other in one sentence.

| Protocol | File | Role in the paper | Verified headline (typed exact micro-F1) |
|---|---|---|---|
| **V4 / Handbook B (paper main)** | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | Abstract and main results | Chinese JobBERT 3M: **0.4331**. Frozen ChatGPT dump + jieba: **0.2854** exact / **0.6249** relaxed. |
| **Gold v2 / Handbook A (provenance)** | `data/gold_canonical_v2.jsonl` | Construction history and appendix | ChatGPT: **0.6365**. Encoder 3-seed mean: **0.1288**. |

The V4 hybrid is **derived** (980 SimHuman rule_v4 spans + 1,621 SOP-CWS spans). It is **not** human Doccano Gold. Do not overwrite `gold_canonical_v2.jsonl`.

**Inconsistencies recorded (not silently resolved):**

- **22,840** is the sum of the Table 1 corpus split (`17,460` / `2,143` / `3,237`) **and** of a later `repartition_v1` draft (`16,350` / `2,268` / `4,222`). Same *N*, different assignment. `repartition_v1` is **not** the main gold.
- Corpus **test** has **3,237** sentences; raw Doccano Gold has **2,676** rows / **2,601** unique IDs; both V4 hybrid and Gold v2 evaluate **2,601** unique IDs.
- A first-page human overlay of **200** sentences exists (`data/human_gold_page1_200.jsonl`) and is **not** the abstract gold.
- A vanilla-WWM seed-42 figure of **0.4341 / 0.4289** is marked **unverified** in the laboratory notes and must not be stated as a result.

---

## Repository structure

```
Chinese_skill_benchmark_Paper/
├── README.md                      # this file
├── REPRODUCIBILITY.md
├── DATA_AVAILABILITY.md
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── requirements-repro.txt         # scoring / jieba only
├── scorer/                        # official scorer cnss-lskt-1.2.0
├── scripts/                       # train, eval, preprocessing
├── data/
│   ├── corpus_splits/             # train.json / dev.json / test.json (22,840)
│   ├── gold_canonical_v2.jsonl    # Gold v2 (appendix)
│   ├── test_lskt_v4_cws_simhuman980_hybrid.jsonl   # paper-main gold
│   ├── train_lskt_v4_silver.jsonl
│   ├── dev_lskt_v4_silver.jsonl
│   ├── frozen_preds/              # encoder dumps for the main table
│   └── human_gold_page1_200.jsonl # 200-sentence human overlay (not main gold)
├── notes/handbooks/               # Handbook B (paper SOP) and related
├── tables/                        # committed CSV results
├── release/                       # Hugging Face and Zenodo templates
└── docs/                          # release checklist; internal notes
```

Internal laboratory notes (Chinese working README, Baidu restore guides, private GitHub push scripts) remain in this tree for authors. They are not the public-facing documentation.

---

## Installation

Scoring and jieba alignment need only the extra listed in `requirements-repro.txt`:

```bash
python3 -m pip install -r requirements-repro.txt
```

That file pins **`jieba>=0.42.1`**. The official scorer itself is standard-library Python.

Encoder training (Chinese JobBERT MLM + CRF) additionally needs the **parent** laboratory `requirements.txt` (verified pins include `torch==2.1.2`, `transformers==4.37.1`, `seqeval==1.2.2`, `numpy==1.26.3`) and `pytorch-crf` on `PYTHONPATH`. A local laboratory environment named `adasparse` has been used for development; that name is not required.

**Known gap before a public clone will run the `.py` / `.sh` trainers as-is:** several scripts hard-code a laboratory absolute path. Those paths must be edited or wrapped before a third party can train. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and `[TODO: remove laboratory absolute paths from public scripts]`.

---

## Data preparation

Files needed for the **paper-main** evaluation (no retraining):

- `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` (SHA-256 `2ad6342d8b762cf1abb289295315e2521bec0c540f4320113409fceab0818d99`)
- `data/frozen_preds/jobbert_3m_v4.jsonl` (and `jobbert_1m_v4.jsonl` if the 1M row is needed)
- Frozen LLM views under `reports/views/` for the ChatGPT / other LLM rows
- `scorer/score_lskt.py`, `scripts/cws_snap.py`, `scripts/eval_hybrid_cws_simhuman.py`

Files needed to **retrain** the V4 CRF head (weights not in Git):

- `data/train_lskt_v4_silver.jsonl`, `data/dev_lskt_v4_silver.jsonl`
- A local Chinese JobBERT encoder directory (continued MLM from `hfl/chinese-roberta-wwm-ext`)
- `[TODO: public Hugging Face model URL for Chinese JobBERT]`

**Do not** add the raw recruitment CSV / XLSX files that sit in this working tree to a public release until redistribution rights are confirmed. See [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md).

---

## Training, evaluation, and inference

Commands below exist in this repository. Do not treat a command as reproducing a published number unless that pairing is stated.

### Official scorer

```bash
python3 scorer/score_lskt.py \
  --gold data/test_lskt_v4_cws_simhuman980_hybrid.jsonl \
  --pred path/to/predictions.jsonl \
  --align-mode official
```

Predictions must use the same sentence `id`s as gold. Label fields accepted by the scorer include `pred_tags` and `list_of_selection_bio4`.

Scoring `data/frozen_preds/jobbert_3m_v4.jsonl` **directly** against the V4 hybrid (no jieba snap) was verified in this workspace to yield typed exact F1 **0.2552**. That is **not** the paper headline.

### Paper-main encoder + LLM table (jieba-aligned)

```bash
python3 scripts/eval_hybrid_cws_simhuman.py
```

This script applies bilateral jieba snapping, fills missing gold IDs with empty predictions, and writes `tables/hybrid_cws_simhuman980_all_models.csv`. When `output/` checkpoints are absent it falls back to `data/frozen_preds/` for the Chinese JobBERT v4 rows. It currently hard-codes a laboratory root path.

### Frozen LLM dumps (no API calls)

```bash
python3 scripts/eval_hybrid_llm_old_dumps.py
```

Writes `tables/hybrid_cws_llm_old_dumps.csv`. Claude and Kimi source dumps are incomplete (98 and 293 gold IDs missing, respectively, before fill).

### CRF training (exists; does not by itself write the 0.4331 CSV)

```bash
python3 scripts/train_cn_roberta_crf.py \
  --seed 42 \
  --model_dir /path/to/chinese-jobbert-encoder \
  --train data/train_lskt_v4_silver.jsonl \
  --dev data/dev_lskt_v4_silver.jsonl \
  --test data/corpus_splits/test.json \
  --gold data/gold_canonical_v2.jsonl \
  --out_dir /path/to/crf_run \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5
```

The wrapper `scripts/run_jobbert_zh_3m_lskt_v4.sh` calls the same trainer but is bound to laboratory absolute paths and a local `output/jobbert_zh_3m/mlm/encoder_ckpt65000` checkpoint that is **not** in Git.

Trainer outputs: `test_pred.jsonl`, `best.pt`, `run_summary.json`, `score_official.json`. Paper-main F1 still requires jieba snap via `eval_hybrid_cws_simhuman.py` (or an equivalent `cws_snap` rewrite) against the V4 hybrid.

### Inference

There is no published `pipeline("token-classification")` entry point. Inference is the `predict_tags` path inside `scripts/train_cn_roberta_crf.py` (Hugging Face `AutoTokenizer` + a custom BERT+CRF module). See `release/huggingface-model/README.md`.

### Appendix / Gold v2 (not abstract SOTA)

```bash
python3 scorer/test_regression.py
python3 scorer/score_lskt.py \
  --gold data/gold_canonical_v2.jsonl \
  --pred reports/views/ChatGPT_unique_first_v2.jsonl \
  --align-mode official
```

### Scorer self-test

```bash
python3 scorer/test_regression.py
```

---

## Reproducing the principal results

| Claim | How it is reproduced here | Required files |
|---|---|---|
| Chinese JobBERT 3M typed exact **0.4331** on V4 hybrid | `python3 scripts/eval_hybrid_cws_simhuman.py` (jieba snap + frozen or local preds). The committed CSV cell is `JobBERT_3M_v4` → `full2601_typed_exact_f1` = `0.433118`. | Hybrid gold, `data/frozen_preds/jobbert_3m_v4.jsonl` or `output/.../test_pred.jsonl`, jieba |
| ChatGPT exact **0.2854** / relaxed **0.6249** | Same script, row `ChatGPT`. | `reports/views/ChatGPT_unique_first_v2.jsonl` |
| ChatGPT Gold v2 typed **0.6365** | Official scorer on `gold_canonical_v2.jsonl` (appendix only). | Gold v2 + ChatGPT unique-first view |

**Inputs.** JSONL records with `id`, `sentence` and/or `tokens`, and BIO tags in `list_of_selection_bio4` (gold) or `pred_tags` (predictions).

**Outputs.** JSON score reports from `score_lskt.py`; CSV tables under `tables/`; trainer dumps `test_pred.jsonl`.

---

## Links

| Resource | URL |
|---|---|
| Public GitHub repository | `[TODO: public GitHub URL]` |
| Zenodo archived release (DOI) | `[TODO: Zenodo DOI]` |
| Hugging Face dataset | `[TODO: Hugging Face dataset URL]` |
| Hugging Face model (Chinese JobBERT) | `[TODO: Hugging Face model URL]` |
| arXiv preprint (this paper only) | `[TODO: this paper's arXiv URL and identifier — do not use 2604.21525 or 2604.23009]` |
| PeerJ Computer Science article | `[TODO: PeerJ article URL]` |
| Legacy project homepage (not the archive) | https://sites.google.com/view/cn-skillspan-resources |

A private working backup currently exists at `https://github.com/AlfredJamesLi/chinese-skillspan-benchmark`. That URL is **not** the PeerJ archival location.

---

## Citation

```bibtex
@article{li_chineseskillspan_TODO,
  title   = {Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements},
  author  = {Li, Guojing and Fu, Zichuan and Li, Junyi and Zhang, Wenlin and Guo, Kaifeng and Yang, Jinning and Gao, Jingtong and Zhao, Xiangyu},
  year    = {[TODO: publication year]},
  journal = {[TODO: PeerJ Computer Science or preprint venue]},
  doi     = {[TODO: Zenodo or article DOI]},
  url     = {[TODO: public GitHub or article URL]}
}
```

Machine-readable metadata: [`CITATION.cff`](CITATION.cff). Corresponding author: Xiangyu Zhao. `[TODO: corresponding-author email and affiliations]`.

---

## Licence summary

- **Code licence:** `[TODO: confirm SPDX licence for scripts and scorer; do not publish as MIT/Apache-2.0 until chosen]`.
- **Dataset licence:** `[TODO: confirm a data licence after redistribution rights for job-advertisement text are verified]`. **Do not treat the full raw advertisement text as openly licensed.**
- **Chinese JobBERT licence:** `[TODO: must be compatible with the base model hfl/chinese-roberta-wwm-ext and with training-data rights]`. A local snapshot of that base model in the laboratory tree has **no** `LICENSE` file; the Hugging Face card licence was not re-fetched for this documentation pass.

See [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md).

---

## Limitations and responsible use

- Labels are **flat, non-overlapping** spans. Nested or crossing spans are out of scope.
- The paper-main V4 test file is a **derived** hybrid, not a fully human gold set. A 200-sentence human overlay is documented separately and is incomplete relative to the 980-sentence disagreement queue.
- Job advertisements can contain employer names, locations, and other workplace information. Do not scrape, republish, or re-identify individuals from the text.
- English JobBERT skill/knowledge heads transferred to this Chinese task score near zero on the V4 hybrid (committed CSV: 0.0096 / 0.0088 typed exact) and are not a substitute for Chinese JobBERT.
- Domain shift across the four sources is large; public-institution sentences are particularly difficult for encoders under Gold v2.
- Do not use the resource to profile job applicants, to infer protected attributes, or to claim ESCO concept-ID accuracy. This release does **not** include ESCO concept IDs. Concept Accuracy and Time-OOD claims are not supported by the frozen files.

---

## Acknowledgements

This work was supported by the National Social Science Fund of China, Grant No. **21BGL142**.

The previous Chinese working README is preserved at [`docs/INTERNAL_RESULTS_README.md`](docs/INTERNAL_RESULTS_README.md).
