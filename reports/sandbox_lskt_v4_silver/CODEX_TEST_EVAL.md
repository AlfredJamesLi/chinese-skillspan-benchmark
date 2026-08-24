# Codex-corrected test eval (sandbox, not for paper)

Gold v2 frozen. Test silver = Codex 50+51 on 2601 Gold-v2 IDs. No retraining. Do not copy into confirmed-results.md.

| Model | Gold v2 typed F1 | Codex silver typed F1 | Gold v2 collapsed | Codex collapsed | Codex 2-way | align |
|---|---:|---:|---:|---:|---:|---|
| GPT-4o | 0.6365 | **0.2988** | 0.6403 | 0.3452 | 0.3045 | True/True |
| DeepSeek | 0.1327 | **0.1144** | 0.3569 | 0.3314 | 0.2588 | True/True |
| Qwen2.5-14B | 0.0791 | **0.1060** | 0.1075 | 0.1512 | 0.1233 | True/True |
| JobBERT-zh_1M_goldstyle-v3_s42 | 0.1224 | **0.1371** | 0.1352 | 0.1532 | 0.1388 | True/True |
| JobBERT-zh_1M_rule-v4_s42 | 0.1079 | **0.1246** | 0.1187 | 0.1366 | 0.1252 | True/True |
| JobBERT-zh_1M_s2026 | 0.1348 | **0.1394** | 0.1472 | 0.1564 | 0.1414 | True/True |
| RoBERTa-wwm_goldstyle-v3_s42 | 0.1156 | **0.1198** | 0.1291 | 0.1394 | 0.1220 | True/True |

JobBERT-zh_1M_rule-v4 was trained on rule silver, not Codex. Codex test is out-of-distribution for that run.
