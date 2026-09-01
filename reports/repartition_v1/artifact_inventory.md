# Artifact path list (repartition_v1)

| artifact | path | rows | unique IDs | source coverage | annotation provenance | current role | proposed role | action |
|---|---|---:|---:|---|---|---|---|---|
| corpus train | `/home/guojingli3/SCESC-LLM-skill-extraction/data/annotated/processed/chinese_skillspan/train.json` | 17460 | 17460 | AI+Grad | v4 silver | old train | keep | do not overwrite |
| corpus dev | `/home/guojingli3/SCESC-LLM-skill-extraction/data/annotated/processed/chinese_skillspan/dev.json` | 2143 | 2143 | AI | v4 silver | old dev | keep | do not overwrite |
| corpus test | `/home/guojingli3/SCESC-LLM-skill-extraction/data/annotated/processed/chinese_skillspan/test.json` | 3237 | 3237 | AI+Cloud+Public | mixed | processed test 3237 | keep | do not overwrite |
| Gold v2 | `data/gold_canonical_v2.jsonl` | 2601 | 2601 | AI+Cloud+Public | Doccano | appendix | appendix | do not overwrite |
| V4 hybrid | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | 2601 | 2601 | AI+Cloud+Public | 980 simhuman+1621 sop_cws | old main eval | appendix transfer | do not overwrite |
| v4 silver train/dev/test | `data/*_lskt_v4_silver.jsonl` | 17460/2143/3237 | same | see Table 1 | rule_v4 drafts | old labels | source for new BIO | copy into new files only |
| new train | `data/repartition_v1/train.jsonl` | 16350 | 16350 | all four | v4 character | new | main train | created |
| new dev | `data/repartition_v1/dev.jsonl` | 2268 | 2268 | all four | v4 character | new | main dev | created |
| new test | `data/repartition_v1/test.jsonl` | 4222 | 4222 | all four | v4 character | new | main test | created |
| encoder train | `scripts/train_cn_roberta_crf.py` | — | — | — | — | CRF trainer | reuse | new out_dir |
| scorer | `scorer/score_lskt.py` cnss-lskt-1.2.0 | — | — | — | — | official | reuse | — |
| 1M encoder | `output/jobbert_zh_1m/mlm/encoder` | — | — | — | — | frozen DAPT | reuse | do not overwrite |
