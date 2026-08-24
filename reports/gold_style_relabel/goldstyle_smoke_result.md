# Gold-style v1 smoke vs silver smoke

Do **not** copy these numbers into the PDF or confirmed-results.md until protocol + labels are accepted.

- silver smoke: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_seed42_gpu1/run_summary.json`
- goldstyle smoke: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/run_summary.json`
- recommendation: **still_near_zero_tighten** (3-seed only if `consider_3seed`)

| run | align | dev typed | official typed F1 | collapsed | TP/pred/gold |
|---|---|---:|---:|---:|---|
| silver | True | 0.5714285714285714 | 0.012034070485269987 | 0.01437836993045245 | 77/6170/6627 |
| goldstyle v1 | True | 0.656926406926407 | 0.0 | 0.0 | 0/1850/6627 |

Threshold for auto 3-seed: typed F1 ≥ 0.05. Current rec=`still_near_zero_tighten`.


## Gold-style v2 smoke

- typed F1: 0.023807292154841127
- collapsed: 0.027369013028400033
- align: True
- best_dev: 0.559161826671222
