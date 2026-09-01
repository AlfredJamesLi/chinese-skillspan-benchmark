# JobBERT-zh 1M / 3M v4 vs Sonnet-4.6 round-1 (n=980) + jieba CWS

**Not Gold. Not human-final. Not for Table 3 / confirmed-results / abstract.**

Preds (frozen, no retrain):
- 1M raw / cws: `output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl` (+ `test_pred_cws.jsonl`)
- 3M raw / cws: `output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/test_pred.jsonl` (+ `test_pred_cws.jsonl`)

Jieba snap = same `cws_snap.rewrite_record` as SOP-CWS (userdict, cap=8). Both-sides CWS is same-rule inflation, not official Gold.

## Sonnet-4.6 round-1 SOP (n=980)

| Model | decode | test gold | typed exact F1 | typed relaxed F1 |
|---|---|---|---|---|
| 1M v4 | raw | Sonnet-980 | **0.1121** | 0.3404 |
| 3M v4 | raw | Sonnet-980 | **0.1135** | 0.3429 |
| 1M v4 | jieba post-hoc | Sonnet-980 (unsnapped) | 0.1469 | 0.3525 |
| 3M v4 | jieba post-hoc | Sonnet-980 (unsnapped) | 0.1474 | 0.3528 |
| 1M v4 | jieba post-hoc | **Sonnet-980 + jieba (both sides)** | **0.1491** | 0.3556 |
| 3M v4 | jieba post-hoc | **Sonnet-980 + jieba (both sides)** | **0.1503** | 0.3545 |

Sonnet labels already look like complete short spans: jieba changed 69/980 sentences (7.0%), mid-word rate ~0.18%. Both-sides CWS therefore barely moves exact (+0.037 vs raw), unlike SOP-rule silver.

## Same-rule SOP / simhuman (for contrast)

| Model | decode | test gold | n | typed exact F1 | typed relaxed F1 |
|---|---|---|---|---|---|
| 1M v4 | raw | rule_v4 simhuman 980 | 980 | 0.3229 | 0.5811 |
| 3M v4 | raw | rule_v4 simhuman 980 | 980 | 0.3239 | 0.5756 |
| 1M v4 | jieba post-hoc | simhuman 980 + jieba | 980 | **0.4333** | 0.6110 |
| 3M v4 | jieba post-hoc | simhuman 980 + jieba | 980 | **0.4401** | 0.6032 |
| 1M v4 | jieba post-hoc | SOP-CWS same 980 IDs | 980 | 0.4343 | 0.6123 |
| 3M v4 | jieba post-hoc | SOP-CWS same 980 IDs | 980 | 0.4415 | 0.6048 |
| 1M v4 | jieba post-hoc | SOP-CWS 2601 | 2601 | 0.4278 | 0.5960 |
| 3M v4 | jieba post-hoc | SOP-CWS 2601 | 2601 | 0.4341 | 0.5884 |

## Gold v2 (official test; jieba is decode-only)

| Model | decode | test gold | n | typed exact F1 | typed relaxed F1 |
|---|---|---|---|---|---|
| 1M v4 | raw | Gold v2 | 2601 | 0.1079 | 0.3320 |
| 3M v4 | raw | Gold v2 | 2601 | 0.1104 | 0.3404 |
| 1M v4 | jieba post-hoc | Gold v2 | 2601 | 0.1454 | 0.3411 |
| 3M v4 | jieba post-hoc | Gold v2 | 2601 | 0.1479 | 0.3470 |
| 1M v4 | jieba post-hoc | Gold v2 same 980 IDs | 980 | 0.1406 | 0.3455 |
| 3M v4 | jieba post-hoc | Gold v2 same 980 IDs | 980 | 0.1434 | 0.3519 |

JSON: `jobbert_cws_sonnet980_eval.json`. Snapped Sonnet gold: `gold_sonnet46_980_cws.jsonl`.
