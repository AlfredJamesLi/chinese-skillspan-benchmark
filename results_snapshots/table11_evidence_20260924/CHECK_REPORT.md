# Table 11 check report (2026-09-24)

## 1. Recovered execution

### Code

- Actual trainer: `run_chinese_encoder.py` SHA-256 `388589abdcfd3e040f2221ca1f52e3763e89edcc409025bc1f000704c6a26494`
- Official scorer used at training time: `adapters/score_lskt.py` SHA-256 `90624fa545434ebe0442c3243709f5e64ef2f95f4ccbacdb5f5d0696b65d69a7`
- That file is **byte-identical** to public `chinese-skillspan-benchmark/scorer/score_lskt.py` (`SCORER_VERSION = cnss-lskt-1.2.0`).
- Gold150 converter: `adapters/convert_gold150_to_bio.py` (standalone copy; SHA differs from the public script because it has no `cnss_paths` import). Freeze SHA constant is the same.

### Launch (from logs, not from the protocol draft)

| Cell | Command evidence |
|---|---|
| XLM-R 42 | `chinese_full_2gpu.sbatch` GPU0, `logs/chinese_full.out` start 2026-09-22T04:51:14+08:00; detailed log `chinese_full_xlm-roberta-large_42.out`. Full argv reconstructed from sbatch + `models.json` + `config.json` (log has no `# CMD` prefix). |
| XLM-R 43 | Same sbatch, GPU1. |
| XLM-R 44, ESCO 42/43/44 | `run_remaining_today.py`; `# CMD` lines in `logs/chinese_full_*_try1.out`. |

Default CLI (not overridden): `--epochs 20 --batch-size 8 --lr 2e-5`, train/dev/gold150 under `chinese_data/`.

### Environment (written into each `config.json`)

Python 3.10.21, torch 2.14.0+cu130, transformers 4.40.2, CUDA 13.0, GPU `NVIDIA RTX PRO 6000 Blackwell Server Edition`. Saved dtype float32. **No AMP/autocast** in the trainer. `cudnn.deterministic=True`.

### Encoder revisions (cache, not just declared strings)

| Encoder | Declared | Snapshot dir exists | `model.safetensors` blob SHA-256 (filename = digest) | Base architecture in cache config |
|---|---|---|---|---|
| FacebookAI/xlm-roberta-large | `c23d21b0620b635a76227c604d44e43a9f0ee389` | yes | `2dfa19f1…e23b` | `XLMRobertaForMaskedLM` |
| jjzha/esco-xlm-roberta-large | `8093cc37ac619a25c5166355acba7be878eb6402` | yes | `5ab9c8c2…dae0` | `RobertaForCustomMaskedLM` |

Logs for every cell: `Some weights of XLMRobertaForTokenClassification were not initialized … ['classifier.bias', 'classifier.weight']`. The saved run `config.json` architecture is `XLMRobertaForTokenClassification` with 9 LSKT labels. The MLM `lm_head` is not in the task checkpoint.

### Fine-tune vs freeze

`optimizer = AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)` — **encoder is not frozen**. “frozen_b2_gold150” in the receipt is the **evaluation freeze**, not encoder freeze. No extra data, no English-head transfer.

### Six checkpoints

All six `best/model.safetensors` exist (~2,235,448,756 bytes). Digests in `hashes/heavy_sha256.txt`. Live `config.json` / `gold150_predictions.jsonl` / `gold150_official.json` SHA-256 match `receipts/results.jsonl` and GitHub snapshot `46d1166`.

## 2. Translation and evaluation target

Executed `normalize_b2` requires `list(sentence) == tokens` (Unicode characters). Gold150 uses `rec["text"]` and integer character offsets. Training script has **no** translate/transcribe/re-label/gold-hint/post-edit path (`translation_and_eval_target.json`).

Gold150 freeze on disk is byte-identical to public `data/gold150_test.jsonl` (and `data/gold150/gold150_test.jsonl`):

- 150 unique IDs, 663 Doccano spans, L=2, K=125, S=448, T=88
- 150/150 sentences contain Han; 0 Latin-only; 0 empty text; 0 OOB/overlap/illegal spans
- 8 sentences have zero gold spans; 8 sentences have >128 characters (chunked at 128, remainder kept — not dropped)

B2 train/dev SHA-256 match published `data/silver_plus_v6a_nocross/`. Train 2,150 / dev 169. ID overlap train–dev–Gold150 = 0. Exact text overlap = 0. NFC text overlap = 0.

Train has 5 Latin-without-Han strings (English fragments inside Chinese ads). That is not an English→Chinese translation of SkillSpan.

**Ad-level isolation: cannot prove.** IDs are handbook-sentence keys (`1801-s0004`). No advertisement parent ID in these files.

Each `history.json` has 20 epochs of **dev** typed exact F1 only. No Gold150 keys. Selected epoch = argmax dev F1, earliest tie, matching `result.json` and the receipt (11/14/14 and 19/15/10). Gold150 was encoded with all-O tags; gold BIO is written after prediction for the scorer only.

Unknown (no historical log): whether any human edited predictions after the run. Code path does not do that.

## 3. Independent rescore and re-inference

Scorer command (equivalent to the in-process call used here):

```bash
env/bin/python adapters/score_lskt.py \
  --gold runs/chinese/full/<enc>/<seed>/gold150_gold.bio.jsonl \
  --pred runs/chinese/full/<enc>/<seed>/gold150_predictions.jsonl \
  --align-mode official --n-boot 2000 \
  --out TABLE11_EVIDENCE_20260924/rescore_20260924/<enc>/<seed>/gold150_official.rescore.json
```

(`run_chinese_encoder.py` also passed `boot_seed=20260921`; CLI default seed is the same constant inside `score()` when using the library call.)

New typed exact P/R/F1, TP/FP/FN, gold/pred support, relaxed, collapsed-boundary, per-type, four-type macro, and empty-sentence false positives are in `rescore_20260924/` and `cell_reports.json`.

Old vs new typed exact F1: **identical** on all six cells. Mean±sample SD (ddof=1):

| Encoder | Exact | Relaxed | Boundary | Macro-F1 |
|---|---|---|---|---|
| XLM-R-large | 0.522 ± 0.022 | 0.650 ± 0.021 | 0.571 ± 0.022 | 0.607 ± 0.016 |
| ESCOXLM-R | 0.538 ± 0.021 | 0.662 ± 0.022 | 0.582 ± 0.024 | 0.622 ± 0.010 |

Re-inference from the six checkpoints on 2026-09-24 (GPU 1, same venv): **0/150 tag diffs** per cell; F1 unchanged. This is checkpoint reproduction of the frozen predictions, not a training rerun.

Empty-gold false positives (8 gold sentences with zero spans): XLM-R 42 predicted spans on 3 of them (`1804-s0005`, `1815-s0008`, `1816-s0012`). Other seeds differ; see `cell_reports.json`. These are scored as FP in typed exact, not hidden.

## 4. Scope

This check does not retrain models and does not replace the original `gold150_official.json` or `results.jsonl` files. The six weight files are on Hugging Face (`HF_RELEASE.md`). The Zenodo archive https://zenodo.org/records/22937244 stores this audit pack, tokenizer/config sidecars, and SHA-256 checksums; the 2.1 GiB `model.safetensors` files are served from Hugging Face. The Chinese-SkillSpan corpus snapshots (v0.1.1–v0.1.3) are separate records.
