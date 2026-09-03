# Reproducibility guide — Chinese-SkillSpan

This document states only what this repository can actually re-run. Placeholders mark facts that are not verified in the tree.

Companion files: [README.md](README.md), [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md), `notes/DATA_PROTOCOL_FREEZE.md`, `REPRO_GITHUB.md` (Chinese laboratory notes; not replaced).

---

## 1. Tested software environment

| Item | Verified in this repository | Notes |
|---|---|---|
| Official scorer | Python 3, standard library; version string `cnss-lskt-1.2.0` in `scorer/score_lskt.py` | No GPU |
| Jieba alignment | `requirements-repro.txt` → `jieba>=0.42.1` | Required for the paper-main table |
| Encoder training pins | Parent `requirements.txt`: `torch==2.1.2`, `transformers==4.37.1`, `seqeval==1.2.2`, `numpy==1.26.3`, `datasets==2.16.1` | Plus `pytorch-crf` on `PYTHONPATH` |
| Laboratory conda env name | `adasparse` appears in wrapper scripts | Not required; path is machine-specific |
| OS / Python patch / CUDA / GPU model | `[TODO: record OS, Python, CUDA, and GPU used for the 0.4331 run]` | Not in the frozen notes |
| Approximate wall-clock | `[TODO: record runtime for MLM, CRF, and eval]` | Not verified |

Scripts under `scripts/` and several evaluators still contain a laboratory absolute root. A clean public clone will not execute those files until that root is parameterised. `[TODO: remove laboratory absolute paths from public scripts]`.

---

## 2. Dependency installation

**Scoring only (recommended for reviewers who only need the main table):**

```bash
python3 -m pip install -r requirements-repro.txt
```

**Training Chinese JobBERT + CRF** (after obtaining encoder weights):

```bash
python3 -m pip install -r ../requirements.txt   # parent laboratory pins
# add pytorch-crf to PYTHONPATH, or install an equivalent CRF package
```

Do not invent additional pip packages. LLM *generation* is not required to reproduce the frozen ChatGPT row.

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
| `notes/handbooks/handbook_B_sop_v4.md` | Handbook B (Chinese) | 7,186 | `e9e7677b248d75ede523c2d53c6a55fe641aed4e3eb004bd59b8c16a7875751b` |
| `notes/handbooks/handbook_B_sop_v4.en.md` | Handbook B (English) | 4,446 | `aee5c4137b858e4e801548796c18a6516134fb64e3ec9dc5620319d2fceaa9ce` |

Release version string: `[TODO: dataset / code release version]`.

`scripts/eval_hybrid_cws_simhuman.py` can **rewrite** the hybrid gold from SOP-CWS + SimHuman sources. After any such run, re-check the SHA-256 above before treating the file as the frozen paper gold.

---

## 4. Random seeds

Verified in `scripts/train_cn_roberta_crf.py` and the 3M V4 wrapper:

- Default / paper CRF recipe: **seed 42**, 6 epochs, patience 2, batch size 16, max length 256, learning rate `2e-5`.
- Three-seed encoder appendix runs use **42, 123, 2026**.
- Five-seed 1M notes mention additional seeds **7** and **13**. `[TODO: confirm 5-seed list if those rows are published]`.

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
# CRF on V4 silver (edit --model_dir to a local Chinese JobBERT encoder)
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

Wrappers that exist but are laboratory-bound:

- `scripts/run_jobbert_zh_3m_lskt_v4.sh`
- `scripts/run_jobbert_zh_1m.sh`
- `scripts/jobbert_zh_3m.sbatch`, `scripts/jobbert_zh_1m.sbatch`

MLM continued pre-training scripts exist (`prepare_jobbert_*`, `jobbert_zh_*.sbatch`). The 1M / 3M sentence corpora (`data/jobbert_*_sents.jsonl`) are large reconstructed job texts and must not be published until rights are confirmed.

Chinese JobBERT **weights are not in Git**. `[TODO: publish encoder + CRF on Hugging Face after licence checks]`.

---

## 8. Evaluation commands

### Paper-main table (V4 hybrid, jieba-aligned)

```bash
python3 scripts/eval_hybrid_cws_simhuman.py
```

Writes `tables/hybrid_cws_simhuman980_all_models.csv`. Uses `data/frozen_preds/` when `output/` is missing for the v4 encoder rows.

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

---

## 9. Expected output files

| Output | Producer |
|---|---|
| `tables/hybrid_cws_simhuman980_all_models.csv` | `eval_hybrid_cws_simhuman.py` |
| `tables/hybrid_cws_llm_old_dumps.csv` | `eval_hybrid_llm_old_dumps.py` |
| `test_pred.jsonl`, `best.pt`, `run_summary.json`, `score_official.json` | `train_cn_roberta_crf.py` |
| JSON object on stdout / `--out` | `scorer/score_lskt.py` |

---

## 10. Expected benchmark results (verified from repository outputs)

From `tables/hybrid_cws_simhuman980_all_models.csv` (`full2601_typed_exact_f1` unless noted):

| System | Typed exact | Typed relaxed (IoU ≥ 0.5) |
|---|---:|---:|
| JobBERT_3M_v4 (Chinese JobBERT 3M, V4 + jieba) | 0.433118 | 0.587322 |
| JobBERT_1M_v4 | 0.427162 | 0.595170 |
| ChatGPT (`gpt-4o`, frozen dump + jieba) | 0.285361 | 0.624869 |
| JobBERT_1M_cws_retrain | 0.404863 | 0.590381 |

Gold v2 appendix (from `notes/confirmed-results.md` / freeze notes; do not rank against the V4 column): ChatGPT typed **0.6365**; encoder 3-seed mean **0.1288**.

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

---

## 13. Reproducing tables and figures

| Artifact | Source |
|---|---|
| Paper-main model comparison | Re-run `eval_hybrid_cws_simhuman.py`; compare to `tables/hybrid_cws_simhuman980_all_models.csv` |
| LLM-only hybrid rows | `eval_hybrid_llm_old_dumps.py` |
| Gold v2 appendix | `scorer/score_lskt.py` on `gold_canonical_v2.jsonl` |
| Handbook / span rules | `notes/handbooks/handbook_B_sop_v4.en.md` (version `B.sop_v4.2.1`) |
| SkillSpan-style figures | `scripts/build_skillspan_style_figures.py` plus `figures/` / `tex/skillspan_style_*.tex` — `[TODO: confirm which figure PDFs are final]` |
| Human-200 supplement | `scripts/build_and_eval_human200_page1.py` (not abstract) |

Do not rebuild Table 1 *N* from `repartition_v1`. Do not insert Concept Accuracy or Time-OOD from older drafts.
