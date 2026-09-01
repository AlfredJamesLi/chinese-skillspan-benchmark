# Span character length diagnostic (short ≤5 vs long >5)

**Status:** 待验证. Does not change paper F1. Does not authorize split training.

Script: `scripts/diag_span_charlen.py`  
Scorer: `cnss-lskt-1.2.0` `match_exact` / `match_relaxed`  
Short = surface characters of `''.join(tokens[start:end])` ≤ 5.

Overall micro exact matched confirmed-results: Gold v2 ChatGPT **0.6365**, JobBERT 1M goldstyle **0.1224**; V4 JobBERT 3M **0.4331**, ChatGPT dump+jieba **0.2854**.

See `f1_short_long.csv`, `span_char_hist.csv`.
