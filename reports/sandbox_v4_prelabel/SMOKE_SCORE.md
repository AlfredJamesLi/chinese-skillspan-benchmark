# Sandbox smoke scores (NOT for the paper)

Predictor: `encoder_3seed/jobbert_zh_1m/seed_2026/test_pred.jsonl` (Gold-v2 typed F1 0.1348 on 2601).
Gold files below are **300-id subsets or v3/sandbox labels**. Do not copy into confirmed-results.md.

**只换测试答案、不重训 CRF，typed F1 没有变好看**（0.13 → 0.09）。collapsed 在 2-way 种子上从 0.14 升到 0.17，仍不到 0.2。若要沙盒分数上升，必须用同一套 v4 标签 **重训 CRF** 再测；那是「模型拟合新银标」，不能写进论文主表。

| Setting | typed P/R/F1 | collapsed F1 | align_ok | missing |
|---|---|---:|---|---:|
| JobBERT-zh_1M_s2026 vs Gold-v2 300-subset | 0.2128/0.0932/0.1296 | 0.1358 | True | 0 |
| JobBERT-zh_1M_s2026 vs eval-v3 LLM-adjudicated 300 | 0.1216/0.0730/0.0913 | 0.1445 | True | 0 |
| JobBERT-zh_1M_s2026 vs v3→2way seed 300 | 0.0912/0.0849/0.0879 | 0.1726 | True | 0 |
