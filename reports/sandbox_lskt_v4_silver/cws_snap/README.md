# Jieba CWS snap (sandbox)

Diagnostic numbers are now in `notes/confirmed-results.md` (appendix only). Still do **not** copy them into PDF Table 3 or the Gold v2 LLM unique-first table.

JobBERT/RoBERTa mid-word cuts (`培训其`, `机器学`, `当前服`) come from **token-CRF + incomplete silver**, not from 1M vs 3M DAPT. SOP already forbids 半词; `looks_complete` in rule v4 does not enforce jieba word bounds (~40% of v4 train spans start or end inside a jieba word).

## What we did

1. Snap existing LSKT v4 **training** spans to jieba words (complete the cut word if ≤8 tokens; otherwise drop the half word). New files only.
2. Same snap as **decode-time** post-processing on frozen CRF preds (no retrain).
3. Retrain JobBERT-zh 1M CRF on the snapped silver (`crf_lskt_v4_cws_seed42`) to see if the encoder *learns* complete words. Does not overwrite `crf_lskt_v4_silver_seed42`.

Tool: `jieba` + `data/cws_userdict.txt`. Scripts: `scripts/cws_snap.py`, `scripts/rewrite_train_lskt_v4_cws.py`, `scripts/eval_cws_posthoc.py`, `scripts/run_jobbert_zh_1m_lskt_v4_cws.sh`.

Untouched: Gold v2, `train.json`, `train_lskt_v4_silver.jsonl` (sha `1dbf8f44…`), SOP rule test gold.

## Silver (train 17460)

| | mid-word spans | sents w/ mid-word | incomplete (looks_complete) |
|---|---:|---:|---:|
| v4 silver | **0.403** | 0.390 | 0.304 |
| v4 + jieba snap | **0.000** | 0.000 | 0.277 |

39% of train sentences changed. `looks_complete` barely moves: leftover incompletes are NP fragments (`协调各`, `分析和解决与`), not 半词.

Named fixes on SOP test: `培训其`→`培训其他`, `机器学`→`机器学习`, `存储和备`→`存储和备份`, `量化分析领`→`量化分析领域`. At cap=8, `监控和管理当前服` cannot grow to `服务器`, so it **trims** to `监控和管理当前`.

## Post-hoc snap (same CRF weights)

| Pred | Gold | exact | IoU≥0.5 |
|---|---|---:|---:|
| 1M+v4 raw | Gold v2 | 0.1079 | 0.3320 |
| 1M+v4 **cws** | Gold v2 | **0.1454** | 0.3411 |
| 3M+v4 raw | Gold v2 | 0.1104 | 0.3404 |
| 3M+v4 **cws** | Gold v2 | **0.1479** | 0.3470 |
| RoBERTa-wwm v3 raw | Gold v2 | 0.1156 | 0.3073 |
| RoBERTa-wwm v3 **cws** | Gold v2 | 0.1407 | 0.3238 |
| 1M+v4 raw | SOP rule v4 | 0.3170 | 0.5663 |
| 1M+v4 cws | SOP rule v4 | 0.2609 | 0.5835 |
| 1M+v4 cws | SOP CWS test | 0.4278 | 0.5960 |

Decode-time jieba is a larger Gold-v2 move than 1M→3M DAPT. SOP **rule** exact drops because that gold still contains 半词; snapping both pred and test (SOP CWS) inflates exact the same way 0.32 did — not a stronger model.

## Engine compare (same 1M+v4 pred, snap only)

jieba+userdict remains the baseline. pkuseg domain models via `spacy_pkuseg` (upstream `pkuseg` does not compile on Python 3.11). HanLP 2.x Electra tok downloaded but **cannot run** here (`encode_plus` removed in current transformers; do not downgrade — CRF uses the same env).

| Engine | Gold v2 exact | IoU≥0.5 | SOP rule exact | vs jieba sent-agree |
|---|---:|---:|---:|---:|
| raw CRF (no snap) | 0.1079 | 0.3320 | 0.3170 | — |
| **jieba + dict** | **0.1454** | 0.3411 | 0.2609 | — |
| pkuseg mixed + dict | 0.1441 | 0.3412 | 0.2630 | 0.927 |
| pkuseg news + dict | 0.1424 | 0.3418 | 0.2639 | 0.931 |
| pkuseg web + dict | 0.1437 | 0.3415 | 0.2620 | 0.922 |
| pkuseg news, no extra dict | 0.1409 | 0.3409 | 0.2646 | 0.920 |

No pkuseg variant beats jieba on official Gold v2. Named fixes (`培训其`→`培训其他`, `机器学`→`机器学习`) are the same. Keep jieba as the snap engine; pkuseg is a close but slightly worse alternative. Details: `ENGINE_COMPARE.md`.

## Retrain

`output/jobbert_zh_1m/crf_lskt_v4_cws_seed42/` on `data/train_lskt_v4_cws.jsonl`. Question: does raw CRF (no snap) stop emitting `培训其`? Official number remains Gold v2 typed exact.

If retrain still mid-word-cuts, keep jieba as a decode constraint. Do not retarget human 980 to JobBERT.
