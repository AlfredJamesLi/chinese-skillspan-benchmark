# Reproducibility guide — Chinese-SkillSpan

This document states only what this repository can actually re-run. Placeholders mark facts that are not verified in the tree.

Companion files: [README.md](README.md), [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md), `notes/DATA_PROTOCOL_FREEZE.md`. SHA-256 values belong in this file, not in the manuscript Data Availability paragraph.

---

## 1. Tested software environment

| Item | Verified in this repository | Notes |
|---|---|---|
| Official scorer | Python 3, standard library; version string `cnss-lskt-1.2.0` in `scorer/score_lskt.py` | No GPU |
| Jieba alignment | `requirements-repro.txt` → `jieba>=0.42.1` | Required for the paper-main table. Second host DS210039 used 0.42.1 (2026-09-11). |
| Encoder + CRF training pins | `requirements-train.txt`: `torch==2.1.2`, `transformers==4.37.1`, `numpy==1.26.3`, `pytorch-crf==0.7.2`, `jieba>=0.42.1` | CUDA torch wheel from pytorch.org if needed. Bitwise match to 0.4331 is **not** claimed. DS210039 `--smoke` used an already-installed torch 2.10.0+cu130 and laboratory `pytorch-crf`; it did not install this pin file. |
| Second-host public entry | DS210039, 2026-09-11, git `09897d9` | P0 JobBERT 3M **0.433118**. The same host also scored the frozen `gpt-4o` dump (**0.285361** / **0.624869**); that dump is not the 0911 SOP LLM table. P2 parser 13/13; P1 smoke not a paper F1. Laboratory receipt is not in the public clone. |
| Laboratory conda env name | Wrapper scripts may name a local environment | Not required; path is machine-specific |
| OS / Python patch / CUDA / GPU model | Not recorded in the frozen notes | — |
| Approximate wall-clock | Not verified for MLM / CRF / eval | — |

Paper-main scoring entry points resolve the tree from `Path(__file__)` or `$CNSS_PAPER_ROOT` (`scripts/cnss_paths.py`). Other scripts under `scripts/` may still contain a laboratory absolute root.

---

## 2. Dependency installation

**Scoring only (recommended for reviewers who only need the main table):**

```bash
python3 -m pip install -r requirements-repro.txt
```

**Training Chinese JobBERT + CRF** (after obtaining encoder weights from the Hub):

```bash
python3 -m pip install -r requirements-train.txt
python3 scripts/train_cn_roberta_crf.py --smoke --out_dir output/p1_crf_smoke
bash scripts/run_crf_v4_from_hub.sh
```

`--smoke` is a Hub connectivity check (16/8/8 rows, 1 epoch). Write `--out_dir` under this clone (`output/` is gitignored); do not use a full root `/tmp`. Smoke skips the optimizer `last.ckpt`. It is **not** a paper F1. The frozen headline remains JobBERT 3M typed exact **0.4331** after jieba. Do not install a parent-lab `../requirements.txt`.

---

## 3. Dataset version and checksums

SHA-256 values below were computed from the files in this workspace.

| File | Role | Bytes | SHA-256 |
|---|---|---:|---|
| `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | Paper-main gold (V4 hybrid, 2,601 IDs) | 2,709,105 | `2ad6342d8b762cf1abb289295315e2521bec0c540f4320113409fceab0818d99` |
| `data/gold_canonical_v2.jsonl` | Gold v2 provenance / appendix (2,601 IDs) | 5,370,667 | `7a26e32b89d4e501175cb96443e35e171cea08d91501d2a32779b96ee8504ff6` |
| `data/corpus_splits/train.json` | Table 1 train (17,460) | 42,645,522 | `0a24841b97416a0b50e80c5e848bc6b232be91c7bc2f81c05ddb937a2924a44b` |
| `data/corpus_splits/dev.json` | Table 1 dev (2,143) | 5,647,111 | `ea0dabb8dbf295d4edc046fa2ecf9610d33557216095aa54ac9690a77954b1ac` |
| `data/corpus_splits/test.json` | Table 1 test (3,237) | 10,653,736 | `263edc8b07db139f078f1023bad7f46dc2c6bf3e7ec1bdfb7cbccded2ded3142` |
| `data/train_lskt_v4_silver.jsonl` | V4 CRF train silver | 13,853,137 | `1dbf8f447e82f2e4c2d3d5df26aaa357e53cfc39c9724d04ebb3188de747680e` |
| `data/dev_lskt_v4_silver.jsonl` | V4 CRF dev silver | 1,816,201 | `005d062f9c07f84f4fd9935a79e8dbb5599b440284f8230eed862eb0428fd637` |
| `data/train_goldstyle_v3.jsonl` | Gold-style v3 train (appendix protocol) | 14,171,835 | `1643f360237e4b0dd3a4da8325bad0207a7fbe0f35da5e442d09b749d6681523` |
| `data/dev_goldstyle_v3.jsonl` | Gold-style v3 dev | 1,861,640 | `d4357d90df918236a1a02c70a562a22efd375c7ce3771f7eae28a8150761ed9e` |
| `data/frozen_preds/jobbert_3m_v4.jsonl` | Frozen Chinese JobBERT 3M v4 predictions | 3,088,621 | `f073f7e696d03ad6cd1ce21177747a40a4148c1372635dc12f5683c9eb5b6bc9` |
| `data/frozen_preds/jobbert_1m_v4.jsonl` | Frozen Chinese JobBERT 1M v4 predictions | 3,089,077 | `7169c2604dcadbbcd920a759074e69bc352303a6b41d5642d77024ce3d226f33` |
| `data/frozen_preds/jobbert_1m_v4_cws_retrain.jsonl` | Frozen 1M CWS-retrain predictions | 3,085,433 | `f0b873345501c93dafdc0ac5547768f61a2c6bfc4f555cacc48b681bbf20fbbb` |
| `data/human_gold_page1_200.jsonl` | Human overlay, first 200 of 980 (not main gold) | 328,087 | `fcecb522fbdf6571caaaa02c592b6ba4a552c4a9cfa52a0ed1f36b0fe9617490` |
| `tables/hybrid_cws_simhuman980_all_models.csv` | Committed paper-main score table | 4,058 | `448c1281c0027d9ec0a83b0d5c51c5f1d412ccf9fb64e4321a583c4a4b534c1e` |
| `scorer/score_lskt.py` | Official scorer | 16,513 | `90624fa545434ebe0442c3243709f5e64ef2f95f4ccbacdb5f5d0696b65d69a7` |
| `notes/handbooks/handbook_B_sop_v4.md` | Handbook B (Chinese, `B.sop_v4.2.14`) | 50,533 | `5a4883d9350d7fb3756e46fac68624e929a2dfbdc1e3014c5f7d222a39757d19` |
| `notes/handbooks/handbook_B_sop_v4.en.md` | Handbook B (English summary) | 29,556 | `d05ba55991f5e03522fbd3d0f010ad29a8bd7033b260bed749801e2c4b66da3f` |
| `data/gold150_test.jsonl` | Human reference set (artifact Gold150: challenge + calibration cohorts) | 67,116 | `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` |
| `data/silver_plus_v6a_nocross/train_b2.jsonl` | Silver-plus B2 teacher train (`v6a_nocross`) | 1,757,307 | `8921e5fc4b89a0fa83bd942f919c3325546b9938e099b6a13e378736b6717d2e` |
| `data/silver_plus_v6a_nocross/dev_b2.jsonl` | Silver-plus B2 teacher development | 151,873 | `e67a3eb5229b94c6c1b552d5f40ece9ad362197236c20cd66b7f2600c9636fef` |

Last minted archive: GitHub / Zenodo **`v0.1.3`** (DOI `10.5281/zenodo.22698504`; includes the human reference set). Earlier snapshots: **`v0.1.2`** (`10.5281/zenodo.22685143`) and **`v0.1.1`** (`10.5281/zenodo.22288338`). The human reference freeze, Silver-plus B2, and Handbook B v4.2.14 are **not** in the `v0.1.1` or `v0.1.2` tarballs.

`scripts/eval_hybrid_cws_simhuman.py` **loads** the frozen hybrid gold and does not rewrite it. Lab-only `--rebuild-gold` would change the SHA-256; do not use that flag for paper-main scoring. The human-reference freeze (`data/gold150_test.jsonl`) is converted with `scripts/convert_gold150_to_bio.py` to a derived BIO file; the freeze bytes must stay `ca8db0bc…`.

---

## 4. Random seeds

Verified in `scripts/train_cn_roberta_crf.py` and the 3M V4 wrapper:

- Default / paper CRF recipe: **seed 42**, 6 epochs, patience 2, batch size 16, max length 256, learning rate `2e-5`.
- Three-seed encoder appendix runs use **42, 123, 2026**.
- Five-seed 1M notes mention additional seeds **7** and **13**. Those rows are not paper-main results.

`set_seed` sets `random`, `numpy`, `torch`, and `torch.cuda.manual_seed_all`. Full bitwise GPU determinism is **not** claimed.

---

## 5. Preprocessing pipeline

1. Job-advertisement sentences are stored as JSON / JSONL with character-level `tokens` and BIO field `list_of_selection_bio4`.
2. V4 silver train/dev are SOP-derived labels, not human Gold.
3. Paper-main test labels: start from SOP-CWS on the Gold v2 ID set, overlay 980 SimHuman `rule_v4` sentences, jieba-snap gold **and** predictions (`scripts/cws_snap.py`).
4. Official alignment: one prediction per gold `id`; extra predicted IDs are counted but not scored (`--align-mode official`).

Character offsets in human annotation are authoritative; jieba is a validator / derived view (Handbook B).

---

## 6. Train / development / test splits

### Table 1 corpus (22,840 sentences)

Source-domain counts computed from `data/corpus_splits/*.json`:

| Split | N | 人工智能招聘 | 应届生招聘 | 阿里云公开数据集 | 事业单位招聘 |
|---|---:|---:|---:|---:|---:|
| train | 17,460 | 7,148 | 10,312 | 0 | 0 |
| dev | 2,143 | 2,143 | 0 | 0 | 0 |
| test | 3,237 | 1,423 | 0 | 473 | 1,341 |

Four sources are present in the resource. The Table 1 split is **source-imbalanced**: graduate ads appear only in train; cloud and public-institution ads appear only in test; development is AI-only.

### Evaluation gold (not the full 3,237-row test file)

- **2,601** unique IDs shared by Gold v2 and the V4 hybrid.
- Raw Doccano export: **2,676** rows collapsing to those 2,601 IDs.
- Gold v2 domain mix (from laboratory notes, not re-counted here): 人工智能招聘 1,407 / 事业单位招聘 737 / 阿里云公开数据集 457.

### `repartition_v1` (same 22,840, different assignment)

Draft split `16,350` / `2,268` / `4,222`. **Not** the paper-main gold. Do not substitute its scores for the V4 hybrid.

---

## 7. Training commands

These files exist. They do **not** by themselves emit the 0.4331 CSV.

```bash
# CRF on V4 silver from Hub JobBERT-zh (does not overwrite frozen_preds/)
python3 -m pip install -r requirements-train.txt
python3 scripts/train_cn_roberta_crf.py \
  --seed 42 \
  --model_dir AlfredJames/jobbert-zh \
  --train data/train_lskt_v4_silver.jsonl \
  --dev data/dev_lskt_v4_silver.jsonl \
  --test data/corpus_splits/test.json \
  --gold data/gold_canonical_v2.jsonl \
  --out_dir output/crf_v4_from_hub_seed42 \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5
# equivalent:
bash scripts/run_crf_v4_from_hub.sh
```

`--gold` is a Gold v2 side diagnostic. Paper-main typed exact **0.4331** still requires jieba snap against `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` (`scripts/eval_hybrid_cws_simhuman.py --paper-main-only --use-frozen`). A new CRF run is not automatically the abstract cell.

To reload the published CRF head without retraining (`AlfredJames/jobbert-zh` `crf/best.pt`):

```bash
python3 scripts/train_cn_roberta_crf.py \
  --model_dir AlfredJames/jobbert-zh \
  --init_crf hub --predict_only --skip_score \
  --out_dir output/cnss_crf_hub_predict
```

Wrappers that exist but are laboratory-bound:

- `scripts/run_jobbert_zh_3m_lskt_v4.sh`
- `scripts/run_jobbert_zh_1m.sh`
- `scripts/jobbert_zh_3m.sbatch`, `scripts/jobbert_zh_1m.sbatch`

MLM continued pre-training scripts exist (`prepare_jobbert_*`, `jobbert_zh_*.sbatch`). The 1M / 3M sentence corpora (`data/jobbert_*_sents.jsonl`) are large reconstructed job texts and must not be published until rights are confirmed.

Chinese JobBERT **weights are not in Git**. Paper-main encoder + V4 CRF: https://huggingface.co/AlfredJames/jobbert-zh. Contrast 1M: https://huggingface.co/AlfredJames/jobbert-zh-1m. Human-reference v6a: https://huggingface.co/AlfredJames/jobbert-zh-v6a. Qwen LoRA is not published.

---

## 8. Evaluation commands

### Paper-main encoder (V4 hybrid, jieba-aligned)

`--paper-main-only` scores **JobBERT_3M_v4 only**. Guaranteed cell: typed exact **0.433118** (paper **0.4331**). It does **not** print the 0911 SOP LLM table.

```bash
python3 scripts/eval_hybrid_cws_simhuman.py --paper-main-only --use-frozen
```

Writes an eval JSON under `--out-dir` (default `reports/sandbox_lskt_v4_silver/hybrid_cws_eval`). Does **not** rewrite hybrid gold. `--write-committed-csv` is lab-only.

### SOP LLM table (0911; committed CSV, no API recall)

```bash
python3 -c "
import csv
from pathlib import Path
with Path('tables/sop_extract_p2_2601.csv').open(encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        if row['split'] == 'P2_hybrid_2601' and 'SOP extract' in row['system']:
            print(row['system'], row['typed_exact_f1'], row['typed_relaxed_f1'])
"
```

Headline 2,601-ID cells: gpt-5.4 **0.2132** / **0.4199**; Qwen2.5-14B Instruct SOP **0.1724** / **0.3279**. Do not rank them against JobBERT **0.4331** in one SOTA sentence. This clone does not re-call those APIs.

### Official scorer API

```bash
python3 scorer/score_lskt.py \
  --gold data/test_lskt_v4_cws_simhuman980_hybrid.jsonl \
  --pred path/to/jieba_snapped_pred.jsonl \
  --align-mode official
```

### Frozen LLM dumps

```bash
python3 scripts/eval_hybrid_llm_old_dumps.py
```

### Appendix Gold v2

```bash
python3 scorer/test_regression.py
python3 scorer/score_lskt.py \
  --gold data/gold_canonical_v2.jsonl \
  --pred reports/views/ChatGPT_unique_first_v2.jsonl \
  --align-mode official
```

### Direct frozen dump without jieba (verified, not the paper headline)

Scoring `data/frozen_preds/jobbert_3m_v4.jsonl` on the V4 hybrid with `--align-mode official` and **no** CWS snap yields typed exact F1 **0.2552** (this workspace). Do not report that figure as the abstract result.

### Human reference set (later protocol; not the abstract table)

JSON-offset Qwen LoRA is Table C **0.1215±0.0092**. Shared-handbook SFT is **0.5403±0.0354**. JobBERT-zh v6a B2 is **0.5536±0.0054**. Do not rank those cells against V4 hybrid **0.4331**. Qwen adapters are not published; `train_qwen_ext_sft.py` is laboratory JSON-offset only (`--protocol json_offset`). Paper names: human reference / challenge cohort / calibration cohort; files keep the Gold150 paths.

```bash
python3 scripts/convert_gold150_to_bio.py
python3 scripts/test_qwen_ext_parser.py --out output/p2_qwen_parser_test.json
python3 scripts/eval_gold150_ext.py \
  --protocol json_offset \
  --pred path/to/gold150_predictions.jsonl \
  --out output/gold150_score.json
```

`--gold_eval` defaults to derived BIO or converts the freeze in memory. It does **not** rewrite `data/gold150_test.jsonl` (SHA-256 `ca8db0bc…`).

---

## 9. Expected output files

| Output | Producer |
|---|---|
| `tables/hybrid_cws_simhuman980_all_models.csv` | `eval_hybrid_cws_simhuman.py` |
| `tables/hybrid_cws_llm_old_dumps.csv` | `eval_hybrid_llm_old_dumps.py` |
| `test_pred.jsonl`, `best.pt`, `run_summary.json`, `score_official.json` | `train_cn_roberta_crf.py` |
| JSON object on stdout / `--out` | `scorer/score_lskt.py` |
| `data/gold150_test.bio.jsonl` (derived; gitignored) | `convert_gold150_to_bio.py` |
| Human-reference split JSON (`--out`) | `eval_gold150_ext.py` |

---

## 10. Expected benchmark results (verified from repository outputs)

From `tables/hybrid_cws_simhuman980_all_models.csv` (`full2601_typed_exact_f1` unless noted):

| System | Typed exact | Typed relaxed (IoU ≥ 0.5) |
|---|---:|---:|
| JobBERT_3M_v4 (paper-main encoder, V4 + jieba) | 0.433118 | 0.587322 |
| JobBERT_1M_v4 | 0.427162 | 0.595170 |
| ChatGPT (`gpt-4o`, frozen dump + jieba; **not** the 0911 SOP table) | 0.285361 | 0.624869 |
| JobBERT_1M_cws_retrain | 0.404863 | 0.590381 |

0911 SOP LLM table (`tables/sop_extract_p2_2601.csv`, `split=P2_hybrid_2601`): gpt-5.4 **0.2132** / **0.4199**; Qwen2.5-14B Instruct SOP **0.1724** / **0.3279**; Llama-3-8B **0.0582** / **0.1178**. Frozen `gpt-4o` dump **0.2854** is a different protocol.

Gold v2 appendix (from `notes/DATA_PROTOCOL_FREEZE.md` and this file; do not rank against the V4 column): ChatGPT typed **0.6365**; encoder 3-seed mean **0.1288**.

**Not verified as paper results:** vanilla-WWM seed-42 **0.4341 / 0.4289**; human-200-only F1; overlay 0.3884 as a replacement abstract number.

---

## 11. Hardware and runtime

`[TODO: GPU model, driver, and wall-clock for MLM 1M/3M and CRF]`. No hardware string suitable for a paper “experimental setup” paragraph is recorded in the freeze files. Do not invent one.

---

## 12. Troubleshooting

| Symptom | Likely cause |
|---|---|
| Script cannot find files under `/home/guojingli3/...` | Laboratory absolute path; edit the script or set a wrapper |
| Typed F1 ≈ 0.255 on frozen 3M preds | Missing jieba snap; use `eval_hybrid_cws_simhuman.py` |
| Typed F1 ≈ 0.46 on old dumps | Forbidden global-set scorer bug (v1.0–v1.1); use `cnss-lskt-1.2.0` |
| `alignment_ok` false | Duplicate or missing gold IDs in the prediction file |
| Claude / Kimi far below ChatGPT | Incomplete dumps (98 / 293 IDs); empty-filled in the hybrid eval |
| `local_files_only=True` tokenizer error | Encoder directory missing; weights are not in Git |
| Hybrid SHA-256 changed after eval | `eval_hybrid_cws_simhuman.py` rewrote the gold; restore the frozen file |
| Paper directory has no `.git` | Laboratory copy; clone the GitHub repo and run from that clone (server B used worktree `_verify_origin_main`) |
| JSON-offset Qwen F1 mixed with 0.5403 | Two human-reference Qwen protocols; pass `--protocol json_offset` or `shared_prompt` and do not share a checkpoint path |

---

## 13. Reproducing tables and figures

| Artifact | Source |
|---|---|
| Paper-main model comparison | Re-run `eval_hybrid_cws_simhuman.py`; compare to `tables/hybrid_cws_simhuman980_all_models.csv` |
| LLM-only hybrid rows | `eval_hybrid_llm_old_dumps.py` |
| Gold v2 appendix | `scorer/score_lskt.py` on `gold_canonical_v2.jsonl` |
| Handbook / span rules | `notes/handbooks/handbook_B_sop_v4.md` (version `B.sop_v4.2.14`) |
| SkillSpan-style figures | `scripts/build_skillspan_style_figures.py` plus `figures/` / `tex/skillspan_style_*.tex` — `[TODO: confirm which figure PDFs are final]` |
| Human-200 supplement | `scripts/build_and_eval_human200_page1.py` (not abstract) |

Do not rebuild Table 1 *N* from `repartition_v1`. Do not insert Concept Accuracy or Time-OOD from older drafts.
