# Silver-plus follow-ups (Overleaf E/F/G, 2026-09-09)

Public archive for the appendix studies Codex wrote into Overleaf.  
**Scores and manifests only.** No LoRA / CRF weights, no job-ad full text, no API keys.

Official Tables A–D are **unchanged**:

- V4 hybrid 2601 JobBERT-zh 3M + jieba **0.4331**
- Gold150 JobBERT v6a B2 **0.5536±0.0054**
- Gold150 Qwen P0 **0.1215±0.0092**
- HEM-E **0.4345±0.0235**

Scorer `cnss-lskt-1.2.0`. Gold150 SHA-256  
`ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`.  
SD is **n=3 sample SD**, not a test CI. Gold150 is **not** in Zenodo v0.1.1.

Companion score JSON and ID lists: [`../gold150_followups_20260909/`](../gold150_followups_20260909/README.md).

## Files in this directory

| File | Role |
|---|---|
| `tables_EFG_appendix.tex` | Overleaf-synced appendix (Studies E/F/G) |
| `NUMERIC_PROVENANCE.md` / `.csv` | 36 numeric locations in the manuscript |
| `AUDIT.json` | Abstract / main-table freeze check |
| `COMPLETION_RECEIPT.md` | Overleaf push receipt (2026-09-09) |
| `NUMBER_CHECK.json` | Cursor re-check against laboratory score JSON |

P1 prompt text: [`docs/qwen_lskt_sft_v1_prompt.txt`](../../docs/qwen_lskt_sft_v1_prompt.txt)  
(SHA-256 in `NUMBER_CHECK.json`).
