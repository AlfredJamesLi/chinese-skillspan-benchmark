# Dual eval (sandbox, not for paper)

**Do not copy into `confirmed-results.md` or the PDF.** Gold v2 is frozen. This track only asks whether JobBERT-zh CRF, trained on LSKT v4 silver, moves F1 on two test sets.

Pred: `output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl`  
Encoder: JobBERT-zh 1M MLM (same as previous CRF). Seed 42. Scorer `cnss-lskt-1.2.0`. Alignment OK, 2601 unique IDs, 0 missing.

Silver how: Cursor rule rewrite (`rewrite_train_lskt_v4.py`: empty lock + cap 8) on corpus silver BIO. **Not** human Gold, **not** a Codex 17k dump. Codex prompt is in `PROMPT_codex.md` for later spot-check.

## Same pred, two golds

| Test gold | typed P / R / F1 | 2-way F1 | boundary F1 |
|---|---|---:|---:|
| Gold v2 (frozen official) | 0.1543 / 0.0830 / **0.1079** | 0.1097 | 0.1187 |
| LSKT v4 silver (same Gold-v2 IDs) | 0.3442 / 0.2938 / **0.3170** | 0.3206 | 0.3418 |

Gold v2: 6627 gold spans, 3565 pred, TP 550.  
v4 silver g2ids: 4177 gold spans, same 3565 pred, TP 1227.

## vs previous JobBERT-zh 1M CRF seed 42 (goldstyle v3 train)

| | Gold-v2 typed F1 | Gold-v2 collapsed | best dev typed |
|---|---:|---:|---:|
| CRF on goldstyle v3 (`crf_v3_seed42`) | **0.1224** | 0.1352 | 0.3185 (v3 train/dev) |
| CRF on LSKT v4 silver (this run) | **0.1079** | 0.1187 | 0.3537 (v4 silver train/dev) |

On frozen Gold v2, typed F1 **dropped** about 0.015 (0.1224 → 0.1079). Recall 0.0943 → 0.0830. Precision 0.1745 → 0.1543. 2-way lift on Gold v2 is only +0.0018, same pattern as the earlier projection audit.

On the new SOP silver test, typed F1 is 0.3170. That set uses the **same rewrite rule as train**, so this is in-distribution SOP fit, not a human Gold gain.

## Read this as

1. New operational definition is **learnable** by JobBERT-zh (dev 0.35, silver-test 0.32).
2. It does **not** raise official Gold v2 F1; it slightly hurts it, as expected if v4 spans are shorter/emptier than Gold v2.
3. Next real lift on Gold v2 still needs labels that match Gold v2 (or a new human Gold). Codex/GPT-5.6 chunk relabel + Doccano polish is the remaining silver path, not another CRF seed.
