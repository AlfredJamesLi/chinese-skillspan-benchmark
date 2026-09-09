# Gold150 follow-ups (2026-09-09)

Scores only. No LoRA / CRF weights. Official Tables A–D are **unchanged**.

Scorer `cnss-lskt-1.2.0`. Gold150 SHA-256  
`ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`.  
SD is **n=3 sample SD**, not a test CI.

## Official cells (do not rewrite)

- V4 hybrid 2601 JobBERT-zh 3M + jieba **0.4331**
- Official Qwen SOP extract **0.1724**
- Gold150 JobBERT v6a B2 **0.5536±0.0054**
- Gold150 Qwen P0 **0.1215±0.0092**
- HEM-E **0.4345±0.0235**

## 1. P1 prompt contrast (does not replace P0)

Same `v6a_nocross` 2150/169, same LoRA budget, seeds 42/43/44. Only the instruction changes. Select on frozen-dev $k=0$. Same checkpoint: $k=0$ / random $k=3$ / $k$NN $k=3$.

| Condition | Gold150 exact | Gold150 relaxed |
|---|---:|---:|
| Official P0 (reused) | **0.1215±0.0092** | 0.4459±0.0237 |
| P1 $k=0$ | 0.1455±0.0196 | 0.4905±0.0109 |
| P1 random $k=3$ | 0.0452±0.0067 | 0.3507±0.0085 |
| P1 $k$NN $k=3$ | 0.0315±0.0047 | 0.3491±0.0122 |

P1 $k=0$ seeds: 0.1293 / 0.1399 / 0.1673. Mean +0.024 vs P0, but sample SDs overlap. Demonstrations collapse exact F1.

## 2. Frozen V4/SOP preds on Gold150 (no new API)

Same 150 IDs, new human gold. SOP extract v4, raw, no jieba.

| System | exact | relaxed |
|---|---:|---:|
| Claude Sonnet 4.5 SOP | 0.3153 | 0.4287 |
| GPT-5.4 SOP | 0.3103 | 0.4471 |
| Kimi k2.6 SOP | 0.3070 | 0.4244 |
| DeepSeek v4-pro SOP | 0.2951 | 0.4131 |
| Qwen2.5-14B SOP parsed | 0.2498 | 0.3475 |

Official `gpt-4o`+SOP was never run. Older ChatGPT `@@span##` dump is a different prompt (0.2614 raw). Do not rank against 0.5536.

## 3. Watermark peel + retrain (no lift)

About 1% of Silver-plus train sentences carry `macrodatas.cn` / 马克数据网. Gold150 has **0**. New list **2138/168** (does not overwrite official v6a / nocross).

| Condition | Official | After peel |
|---|---:|---:|
| JobBERT B2 | 0.5536±0.0054 | 0.5509±0.0054 |
| JobBERT B1 | 0.1422±0.0138 | 0.1507±0.0062 |
| Qwen P0 | 0.1215±0.0092 | 0.1071±0.0102 |
| HEM-E | 0.4345±0.0235 | 0.4355±0.0250 |

Overleaf-synced appendix TeX and numeric provenance: [`../silver_plus_followups_20260909/`](../silver_plus_followups_20260909/README.md).

Weights (do **not** overwrite V4): [`AlfredJames/jobbert-zh-v6a`](https://huggingface.co/AlfredJames/jobbert-zh-v6a). Encoder is the same 3M dump as [`AlfredJames/jobbert-zh`](https://huggingface.co/AlfredJames/jobbert-zh).

## Files

- `P1_CONTRAST_REPORT.md`, `P1_summary.json`, `P1_CONTRAST_RESULTS.public.json`
- `sop_gold150_SUMMARY.json`, `sop_gold150_DIAGNOSTIC.md`
- `PEEL_RERUN_REPORT.md`, `PEEL_RERUN_RESULTS.json`
- `peel_manifest/` — ID lists for the unofficial 2138/168 peel set (no job-ad text)
- `overleaf/` — paste-ready TeX; `tables_EFG_appendix.tex` matches the Overleaf appendix
