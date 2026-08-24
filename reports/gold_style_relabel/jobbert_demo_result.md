# JobBERT-zh demo vs encoder / LLM dumps

Internal smoke only. Do **not** copy into the PDF or `confirmed-results.md`.
Primary metric: typed exact micro F1 on Gold v2 (`cnss-lskt`).

- recommendation: **demo_mlm_no_lift**
- JobBERT − vanilla v3: `-0.0004`
- JobBERT − Qwen dump: `+0.0361`

| system | align | dev typed | official typed F1 | P | R | collapsed | TP/pred/gold |
|---|---|---:|---:|---:|---:|---:|---|
| JobBERT-zh demo CRF (80k×1 MLM + v3) | True | 0.3231 | 0.1152 | 0.1569 | 0.0910 | 0.1290 | 603/3842/6627 |
| RoBERTa-wwm + CRF (no DAPT, v3) | True | 0.3210 | 0.1156 | 0.1607 | 0.0902 | 0.1291 | 598/3721/6627 |
| RoBERTa-wwm + CRF goldstyle v2 | True | 0.5592 | 0.0238 | 0.0314 | 0.0192 | 0.0274 | 127/4042/6627 |
| RoBERTa-wwm + CRF silver | True | 0.5714 | 0.0120 | 0.0125 | 0.0116 | 0.0144 | 77/6170/6627 |
| Qwen dump (Gold v2 unique) | True | — | 0.0791 | 0.2178 | 0.0483 | 0.1075 | 320/1469/6627 |
| DeepSeek dump (Gold v2 unique) | True | — | 0.1327 | 0.1384 | 0.1274 | 0.3569 | 844/6098/6627 |
| ChatGPT dump (Gold v2 unique) | True | — | 0.6365 | 0.6264 | 0.6469 | 0.6403 | 4287/6844/6627 |
| English JobBERT-skill transfer | True | — | 0.0000 | 0.0000 | 0.0000 | 0.0045 | 0/13105/6627 |

Notes:
- Paper Qwen 0.2130 is unreproducible; not used here.
- Old Qwen typed ~0.34 used raw Gold 2676, not Gold v2.
- Demo is 80k sentences × 1 MLM epoch, not Zhang 3.2M / 3-epoch JobBERT.
