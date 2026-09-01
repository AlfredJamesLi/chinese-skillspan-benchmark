# Drop the 980 must-human IDs (sandbox)

**Not for paper.** Same CRF preds; gold files filtered by ID. Extra pred IDs are not scored (`cnss-lskt-1.2.0` official). Gold v2 files were not overwritten.

Remaining **1621** = Gold v2 2601 minus `human_must_review.csv`. This is the easier LLM-agreement slice, not a random hold-out.

Typed micro F1:

| Pred | Gold | full 2601 exact / partial | drop 980 (1621) | only 980 |
|---|---|---:|---:|---:|
| 1M+v4 | Gold v2 | 0.1079 / 0.3320 | **0.1147 / 0.3243** | 0.1047 / 0.3358 |
| 3M+v4 | Gold v2 | 0.1104 / 0.3404 | **0.1211 / 0.3323** | 0.1053 / 0.3443 |
| 1M+v4 | SOP rule v4 | 0.3170 / 0.5663 | **0.3034 / 0.5334** | 0.3235 / 0.5822 |
| 3M+v4 | SOP rule v4 | 0.3229 / 0.5624 | **0.3187 / 0.5319** | 0.3249 / 0.5770 |
| ChatGPT (`gpt-4o`) | Gold v2 | 0.6365 / 0.7221 | 0.6961 / 0.7690 | 0.6076 / 0.6995 |

JSON: `drop980_scores.json`.
