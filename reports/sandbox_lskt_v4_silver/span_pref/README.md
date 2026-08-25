# JobBERT vs silver / LLM span preferences (sandbox)

Gold v2 2601 IDs. Incomplete = span ends with a bound char in `INCOMPLETE_END` (的/和/服/技/…) or fails `looks_complete`. Not for paper.

## What JobBERT copies

Sentence-level exact span+type agreement with 1M+v4 CRF:

| vs | exact agree |
|---|---:|
| rule_v4 silver | **0.399** |
| RoBERTa-wwm (no DAPT) | 0.410 |
| 3M+v4 (same SOP) | 0.549 |
| Doubao / Kimi | 0.366 / 0.364 |
| Codex | 0.319 |
| Gold v2 | 0.311 |

RoBERTa-wwm goldstyle CRF (no JobBERT DAPT) already mid-word-cuts. Preference is **token-CRF + silver**, not MLM 1M→3M.

## Corpus stats (2601)

| Source | empty sent | spans/sent | mean len | % sents w/ incomplete |
|---|---:|---:|---:|---:|
| Gold v2 | 0.351 | 2.55 | 4.90 | 0.224 |
| rule v4 silver | 0.348 | 1.61 | 5.39 | **0.368** |
| JobBERT 1M v4 | 0.388 | 1.37 | 4.92 | **0.324** |
| JobBERT 3M v4 | 0.389 | 1.38 | 4.82 | 0.303 |
| RoBERTa-wwm v3 | 0.389 | 1.43 | 5.98 | 0.297 |
| Codex | **0.456** | 1.39 | **3.14** | 0.062 |
| Doubao | **0.528** | 1.57 | 3.95 | 0.090 |
| Kimi | 0.437 | 2.02 | 4.11 | 0.122 |

JSON: `span_pref.json`.
