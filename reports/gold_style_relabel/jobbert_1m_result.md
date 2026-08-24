# JobBERTa-zh 1M vs encoder / dumps

Internal smoke only. Do **not** copy into the PDF or `confirmed-results.md`.
Primary metric: typed exact micro F1 on Gold v2 (`cnss-lskt`).

- recommendation: **lift_continue_1m_encoder_3p2m_2ep**
- launch_3m: `True`
- 1M − vanilla v3: `+0.0069`
- 1M − 80k demo: `+0.0072`
- next init: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_1m/mlm/encoder`
- next epochs: `2`
- why: 1M typed F1 above vanilla; continue DAPT on Zhang-scale 3.2M for 2 epochs.

| system | align | dev typed | official typed F1 | P | R | collapsed | TP/pred/gold |
|---|---|---:|---:|---:|---:|---:|---|
| JobBERTa-zh 1M CRF (1M×3 MLM + v3) | True | 0.3185 | 0.1224 | 0.1745 | 0.0943 | 0.1352 | 625/3582/6627 |
| JobBERT-zh demo CRF (80k×1 MLM + v3) | True | 0.3231 | 0.1152 | 0.1569 | 0.0910 | 0.1290 | 603/3842/6627 |
| RoBERTa-wwm + CRF (no DAPT, v3) | True | 0.3210 | 0.1156 | 0.1607 | 0.0902 | 0.1291 | 598/3721/6627 |
| RoBERTa-wwm + CRF goldstyle v2 | True | 0.5592 | 0.0238 | 0.0314 | 0.0192 | 0.0274 | 127/4042/6627 |
| RoBERTa-wwm + CRF silver | True | 0.5714 | 0.0120 | 0.0125 | 0.0116 | 0.0144 | 77/6170/6627 |
| Qwen dump (Gold v2 unique) | True | — | 0.0791 | 0.2178 | 0.0483 | 0.1075 | 320/1469/6627 |
| English JobBERT-skill transfer | True | — | 0.0000 | 0.0000 | 0.0000 | 0.0045 | 0/13105/6627 |

Notes:
- 3.2M target follows Zhang JobBERT / JobBERTa sentence scale, not paper numbers.
- Mix stays corpus-train 59:41 (应届生/人工智能). Gold has 阿里云/事业单位; those CSVs are still missing.
