# Existing encoders scored on SOP-v4 test gold (sandbox)

**Not for paper. Not `confirmed-results.md`.** Gold v2 files were not overwritten.

Scored existing `test_pred.jsonl` with `scripts/score_sop_v4_pred.py` on 2026-08-25. Did not retrain. GPU 1 still running 3M+v4 CRF separately.

Typed micro F1 (exact / IoU≥0.5):

| Pred (CRF train labels) | SOP rule v4 2601 | simhuman 980 | Codex 2601 | Gold v2 |
|---|---:|---:|---:|---:|
| 3M ckpt65000, goldstyle v3 | 0.2178 / 0.5010 | 0.2165 / 0.5128 | 0.1343 / 0.2474 | 0.1233 / 0.3144 |
| 3M crf_v3, goldstyle v3 | 0.2163 / 0.4994 | 0.2175 / 0.5135 | 0.1286 / 0.2382 | 0.1170 / 0.3041 |
| 1M crf_v3, goldstyle v3 | 0.2142 / 0.5050 | 0.2200 / 0.5189 | 0.1371 / 0.2550 | 0.1224 / 0.3176 |
| 1M CRF, LSKT v4 silver | 0.3170 / 0.5663 | 0.3229 / 0.5811 | 0.1246 / 0.2837 | 0.1079 / 0.3320 |
| 3M CRF, LSKT v4 silver | 0.3229 / 0.5624 | 0.3239 / 0.5756 | 0.1272 / 0.2924 | 0.1104 / 0.3404 |

JSON: `sop_eval_*.json` in this directory. 3M+v4 finished 2026-08-25 05:09.
