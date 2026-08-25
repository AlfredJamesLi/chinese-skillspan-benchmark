# CWS post-hoc snap (sandbox)

Existing JobBERT CRF predictions, spans snapped to jieba words. **Not** Gold v2 freeze. Do not copy into `confirmed-results.md`.

| Pred | Gold | exact F1 | IoU≥0.5 F1 | P / R |
|---|---|---:|---:|---|
| jobbert_1m_v4 raw | gold_v2_official | 0.1079 | 0.3320 | 0.1543/0.0830 |
| jobbert_1m_v4 **cws** | gold_v2_official | 0.1454 | 0.3411 | 0.2099/0.1112 |
| jobbert_1m_v4 raw | sop_rule_v4_2601 | 0.3170 | 0.5663 | 0.3442/0.2938 |
| jobbert_1m_v4 **cws** | sop_rule_v4_2601 | 0.2609 | 0.5835 | 0.2857/0.2401 |
| jobbert_1m_v4 raw | sop_cws_2601 | 0.2527 | 0.5748 | 0.2743/0.2343 |
| jobbert_1m_v4 **cws** | sop_cws_2601 | 0.4278 | 0.5960 | 0.4682/0.3939 |

| jobbert_3m_v4 raw | gold_v2_official | 0.1104 | 0.3404 | 0.1571/0.0851 |
| jobbert_3m_v4 **cws** | gold_v2_official | 0.1479 | 0.3470 | 0.2125/0.1135 |
| jobbert_3m_v4 raw | sop_rule_v4_2601 | 0.3229 | 0.5624 | 0.3493/0.3002 |
| jobbert_3m_v4 **cws** | sop_rule_v4_2601 | 0.2608 | 0.5793 | 0.2843/0.2408 |
| jobbert_3m_v4 raw | sop_cws_2601 | 0.2558 | 0.5690 | 0.2766/0.2379 |
| jobbert_3m_v4 **cws** | sop_cws_2601 | 0.4341 | 0.5884 | 0.4730/0.4011 |


Retrain (whether BERT *learns* complete words) is a separate run: `output/jobbert_zh_1m/crf_lskt_v4_cws_seed42/` on `train_lskt_v4_cws.jsonl`.
