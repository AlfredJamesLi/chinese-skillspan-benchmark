# Frozen encoder predictions for table repro

These jsonl files are copies of `output/.../test_pred.jsonl` for the matched-protocol encoder rows. They are **not** checkpoints. Do not overwrite Gold v2.

| File | Source |
|---|---|
| `jobbert_1m_v4.jsonl` | `output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl` |
| `jobbert_3m_v4.jsonl` | `output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/test_pred.jsonl` |
| `jobbert_1m_v4_cws_retrain.jsonl` | `output/jobbert_zh_1m/crf_lskt_v4_cws_seed42/test_pred.jsonl` |

`scripts/eval_hybrid_cws_simhuman.py` uses these paths when `output/` is missing.
