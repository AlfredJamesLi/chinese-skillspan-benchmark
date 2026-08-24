# JobBERT-zh small demo (not paper numbers)

Uses whatever 2014–2025 JD files are already on disk. **80k unique sentences × 1 MLM epoch**, then CRF on goldstyle v3. Not Zhang 3.2M / 3-epoch JobBERT.

- Drops exact test / Gold v2 sentences from MLM.
- Does not overwrite `train.json` or Gold v2.
- Comparison: vanilla `chinese-roberta-wwm-ext` + CRF on the same v3 labels.

Logs:

- demo: `output/jobbert_zh_demo/demo.log`
- vanilla v3: `output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/smoke.log`
