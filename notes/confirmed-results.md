# Confirmed results (Chinese-SkillSpan)

Extracted from uploaded PDF:

`Chinese_skill_benchmark_Paper/2026_New_DASFAA_Chinese_SkillSpan__A_Span_Level_Dataset_for_ESCO_Aligned_Competency_Extraction_from_Chinese_Job_Ads.pdf`

Venue on filename: DASFAA 2026 (new). Task: Chinese JobSkillNER, ESCO-1.20, flat **LSKT** (L/K/S/T).  
Metrics in paper: Exact-span F1 (S-F1), Relaxed F1 (IoU≥0.5), Concept Accuracy.

## Table 1 — corpus (paper)

| Split | #Sent | Avg Len | Avg 4D | Avg L | Avg K | Avg S | Avg T |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 17460 | 37.41 | 2.354 | 0.019 | 0.639 | 1.183 | 0.513 |
| dev | 2143 | 40.37 | 3.607 | 0.016 | 1.276 | 1.810 | 0.504 |
| test | 3237 | 43.85 | 2.306 | 0.010 | 0.822 | 1.141 | 0.332 |

Repo **root** `data/annotated/processed/chinese_skillspan/`: #Sent and Avg Len **match**.  
Repo **preprocessing** `test.json` is 2639 and **unlabeled** — do not use as the paper split.

## Table 2 — IAA (paper, n=100)

| Metric | P | R | F1 / κ |
|---|---:|---:|---:|
| Strict exact span | 0.707 | 0.426 | 0.532 |
| Relaxed overlap | 0.829 | 0.500 | 0.624 |
| Token Cohen’s κ | — | — | 0.554 |

No IAA script or 100-sample subset found in the repo (**missing**).

## Table 3 — strict S-F1 (paper vs this repo, 2026-08-22 rescore)

Gold for rescore: `chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl` (2676).  
Span metric: exact (start, end, type) or collapsed to SKILL.

| Model | Paper S-F1 | Repo typed F1 | Repo collapsed F1 | Pred dump n | Verdict |
|---|---:|---:|---:|---:|---|
| ChatGPT | 0.6700 | 0.6836 | **0.6703** | 3237 | **Match** (collapsed) |
| Claude | 0.6300 | 0.5712 | 0.6062 | 2536 | Close; dump incomplete |
| Kimi | 0.5700 | 0.5310 | 0.5618 | 2341 | Close; dump incomplete |
| DeepSeek | 0.5130 | **0.5149** | 0.5479 | 2639 | **Match** (typed) |
| Qwen | 0.2130 | 0.3442 | 0.3949 | 3237 / 2601 aligned | **Gap** |
| JobBERT-skill | 0.0045 | — | **0.0045** | metrics file | **Match** |
| JobBERT-knowledge | 0.0038 | — | **0.0038** | metrics file | **Match** |

Do not cite `*.eval_ner.json` silver scores (~0.004 F1). Those used the unlabeled preprocessing gold. See `REPRO_GAP.md`.

JobBERT sources:

- `Baseline_Models_Collection/metrics_jobbert_skill_chinese_encoder_aligned.txt`
- `Baseline_Models_Collection/metrics_jobbert_knowledge_chinese_encoder_skillaligned.txt`

## Gold v2 unique-first (repo scored 2026-08-24; add tables, do not overwrite PDF Table 3)

Gold: `data/gold_canonical_v2.jsonl` (2601 unique IDs). Scorer: `cnss-lskt-1.2.0`.  
Primary metric: **typed exact micro F1**. Relaxed: IoU≥0.5.  
CSV: `tables/table3_gold_v2_unique_view.csv`, `tables/relaxed_f1_gold_v2.csv`.

| Model | Paper S-F1 | typed exact | collapsed exact | typed relaxed | Align |
|---|---:|---:|---:|---:|---|
| ChatGPT | 0.6700 | 0.6365 | 0.6403 | **0.7221** | OK |
| DeepSeek | 0.5130 | 0.1327 | 0.3569 | 0.1798 | OK |
| Qwen | 0.2130 | 0.0791 | 0.1075 | 0.1272 | OK |
| JobBERT-skill | 0.0045 | 0.0000 | 0.0045 | 0.0000 | OK |
| JobBERT-knowledge | 0.0038 | 0.0000 | 0.0037 | 0.0000 | OK |
| Claude | 0.6300 | **0.2583** | 0.2970 | 0.3861 | OK (98 IDs filled with sonnet-4-6; dump is haiku+sonnet mix) |
| Kimi | 0.5700 | 0.1651 | 0.3349 | 0.2130* | Missing 293 IDs |

Claude Gold v2 is complete at 2601/2601 via `reports/views/Claude_filled_v2.jsonl` (original haiku dump + 98 sonnet-4-6 fills). Original `merged_test_cluade.jsonl` untouched. Incomplete unique-first view is still 0.2570 typed (matched-only). Kimi original dump still misses 293 IDs; use `Kimi_filled_v2.jsonl` for the filled row.

## Per-domain typed exact F1 (Industry-OOD proxy; Gold v2)

Domains: 人工智能招聘 1407 / 事业单位招聘 737 / 阿里云公开数据集 457.  
No `year` field → **do not claim Time-OOD**. CSV: `tables/per_domain_gold_v2.csv`.

| System | 人工智能 | 阿里云 | 事业单位 |
|---|---:|---:|---|
| ChatGPT | 0.6489 | 0.5650 | **0.7032** |
| DeepSeek | 0.1392 | 0.1293 | 0.0805 |
| Qwen | 0.0887 | 0.0646 | 0.0207 |
| JobBERT 3M ckpt65000 | **0.1323** | 0.1259 | 0.0150 |
| JobBERT 1M | 0.1287 | 0.1332 | 0.0181 |
| listed mix 1M | 0.1282 | 0.1240 | 0.0153 |
| domain-mix 1M (seed 42) | 0.1276 | **0.1372** | 0.0287 |
| RoBERTa-wwm v3 | 0.1242 | 0.1191 | 0.0115 |

Encoder fails on 事业单位 (~0.015–0.029) vs ~0.13 on 人工智能/阿里云. ChatGPT is strongest on 事业单位 (0.7032). Domain-mix seed 42 raises 事业单位 to 0.0287; still a failure mode.

## Encoder CRF ranking (Gold v2 typed exact; seed 42)

CSV: `tables/encoder_gold_v2.csv`. Encoder is a **weak baseline**, not competitive with ChatGPT 0.6365 typed.

| Run | test F1 | dev F1 | vs 0.1224 |
|---|---:|---:|---|
| domain-mix 1M (seed 42) | **0.1234** | 0.3190 | +0.0010 |
| JobBERT 3M ckpt65000 | 0.1233 | 0.3205 | +0.0009 |
| JobBERT 1M + goldstyle v3 | **0.1224** | 0.3185 | baseline |
| human380 + v3 merge | 0.1207 | 0.3163 | −0.0017 |
| listed mix 1M | 0.1201 | 0.3257 | −0.0023 |
| JobBERT 3M final encoder | 0.1170 | 0.3209 | −0.0054 |
| JobBERT 3M ckpt100k | 0.1167 | 0.3207 | −0.0057 |
| JobBERT demo 80k | 0.1152 | 0.3231 | −0.0072 |
| RoBERTa-wwm goldstyle v3 | 0.1156 | 0.3210 | −0.0068 |

listed mix 1M **lost**; do **not** add listed-3M. Domain-mix seed 42 is +0.0010 vs 1M; it does **not** beat ChatGPT.

## Encoder 3-seed typed exact (Gold v2; `cnss-lskt-1.2.0`)

CSV: `tables/encoder_3seed_gold_v2.csv`. Sample std over three seeds. RoBERTa-wwm v3 seed 123 still running → no vanilla mean.

| Run | seed 42 | seed 123 | seed 2026 | mean | std |
|---|---:|---:|---:|---:|---:|
| JobBERT 1M | 0.1224 | 0.1292 | 0.1348 | **0.1288** | 0.0062 |
| domain-mix 1M | 0.1234 | 0.1280 | 0.1294 | 0.1269 | 0.0031 |
| JobBERT 3M ckpt65000 | 0.1233 | 0.1295 | 0.1246 | 0.1258 | 0.0033 |
| RoBERTa-wwm v3 | 0.1156 | — | — | — | — |

3-seed mean: domain-mix 0.1269 **below** JobBERT 1M 0.1288. Do not scale domain-mix to 3M. Encoder remains a weak baseline (~0.13 vs ChatGPT 0.6365 typed).

## Diagnostic — LSKT v4 SOP / jieba CWS (Overleaf appendix; not Table 3)

Authorized 2026-08-25 for a **separate** diagnostic table. CSV: `tables/sop_v4_cws_diagnostic.csv`.  
These numbers are scored and reproducible. They are **not** interchangeable with ChatGPT 0.6365 or PDF Table 3 S-F1.

Do **not** put any row below into PDF Table 3, the Gold v2 unique-first LLM table, the abstract SOTA sentence, or the encoder 3-seed ranking. Caption must name train silver, decode, and test gold.

| Pred | Train silver | Decode | Test gold | typed exact | IoU≥0.5 | Paper role |
|---|---|---|---|---:|---:|---|
| JobBERT 1M CRF | goldstyle v3 | raw | Gold v2 | 0.1224 | — | official encoder baseline (already in encoder table) |
| JobBERT 1M CRF | SOP v4 silver | raw | Gold v2 | 0.1079 | 0.3320 | ablation: SOP train vs official gold |
| JobBERT 3M CRF | SOP v4 silver | raw | Gold v2 | 0.1104 | 0.3404 | same ablation |
| JobBERT 1M CRF | SOP v4 silver | jieba post-hoc | Gold v2 | 0.1454 | 0.3411 | decode-time CWS snap, not a new trained model |
| JobBERT 3M CRF | SOP v4 silver | jieba post-hoc | Gold v2 | 0.1479 | 0.3470 | same decode ablation |
| JobBERT 1M CRF | SOP v4 silver | raw | SOP rule silver (2601) | 0.3170 | 0.5663 | train≈test same-rule **consistency**; not official gold |
| JobBERT 3M CRF | SOP v4 silver | raw | SOP rule silver (2601) | 0.3229 | 0.5624 | same consistency check |
| JobBERT 1M CRF | SOP v4 silver | jieba post-hoc | SOP rule silver (2601) | 0.2609 | 0.5835 | snap hurts exact when SOP gold still has 半词 |
| JobBERT 1M CRF | SOP v4 silver | jieba post-hoc | SOP-CWS silver (2601) | 0.4278 | 0.5960 | both sides snapped; same-rule inflation |
| JobBERT 3M CRF | SOP v4 silver | jieba post-hoc | SOP-CWS silver (2601) | 0.4341 | 0.5884 | same-rule inflation |

Allowed claim: SOP v4 silver training **lowers** Gold v2 typed exact vs goldstyle v3 (0.1079/0.1104 vs 0.1224). Jieba post-hoc snap **raises** Gold v2 exact of the same v4 preds (0.1454/0.1479) but does not replace the goldstyle encoder ranking. 0.3170 and ~0.43 measure agreement with SOP silver, not human Gold v2.

## Matched-protocol test gold — SOP-CWS + SimHuman 980, jieba bilateral (authorized 2026-08-25)

User-requested reproducible benchmark eval for submission. **Does not overwrite Gold v2.** Not PDF Table 3 S-F1. Not comparable to ChatGPT 0.6365 on Gold v2.

Gold: `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` (2601 = 980 SimHuman rule_v4 jieba-snapped + 1621 SOP-CWS; sha256 `2ad6342d…818d99`).  
980 subset: `data/test_lskt_v4_simhuman980_cws.jsonl` (sha256 `05765161…adec1580`).  
Preds jieba-snapped with the same `cws_snap.rewrite_record`. Missing Gold IDs filled empty. Scorer `cnss-lskt-1.2.0`.  
Encoder CSV: `tables/hybrid_cws_simhuman980_all_models.csv`.  
**LLM rows below = frozen old dumps only** (no new API): `tables/hybrid_cws_llm_old_dumps.csv`, script `scripts/eval_hybrid_llm_old_dumps.py`. Fill queues: `reports/sandbox_lskt_v4_silver/hybrid_cws_eval/fill_later/`. Write-up: `reports/sandbox_lskt_v4_silver/hybrid_cws_eval/RESULTS.md`.

| Model | n=2601 exact | n=2601 relaxed | n=980 exact | n=980 relaxed |
|---|---:|---:|---:|---:|
| JobBERT 3M v4 + jieba | **0.4331** | 0.5873 | **0.4401** | 0.6032 |
| JobBERT 1M v4 + jieba | **0.4272** | **0.5952** | **0.4333** | **0.6110** |
| JobBERT 1M CWS retrain + jieba | 0.4049 | 0.5904 | 0.4020 | 0.6084 |
| domain-mix 1M (3-seed mean) | 0.3037 | 0.5278 | — | — |
| JobBERT 1M goldstyle v3 (3-seed mean) | 0.3032 | 0.5332 | — | — |
| listed-mix 1M | 0.2964 | 0.5267 | — | — |
| JobBERT 3M ckpt65000 (3-seed mean) | 0.2961 | 0.5278 | — | — |
| JobBERT demo 80k | 0.2931 | 0.5321 | — | — |
| RoBERTa-wwm v3 (3-seed mean) | 0.2875 | 0.5206 | — | — |
| ChatGPT (old dump, complete) | 0.2854 | **0.6249** | 0.2836 | **0.6447** |
| Claude (old dump, 98 empty) | 0.1483 | 0.3349 | 0.1757 | 0.4062 |
| Kimi (old dump, 293 empty) | 0.0964 | 0.1997 | 0.1011 | 0.2183 |
| DeepSeek (old dump, complete) | 0.0802 | 0.1577 | 0.0738 | 0.1573 |
| Qwen (old dump, complete) | 0.0501 | 0.1409 | 0.0483 | 0.1361 |
| JobBERT-skill EN head | 0.0096 | 0.0676 | 0.0124 | 0.0919 |
| JobBERT-knowledge EN head | 0.0088 | 0.0644 | 0.0122 | 0.0862 |

Allowed claim: under this matched SOP+jieba test gold, JobBERT-zh 1M/3M v4 lead typed exact (**0.4272 / 0.4331**); ChatGPT leads typed relaxed (**0.6249**). 980 SimHuman is consistent with full 2601 (Δ exact <0.01 for 1M/3M v4). Do not write these as beating ChatGPT on Gold v2.

LLM coverage on hybrid 2601 (old dumps, **no API this pass**): ChatGPT / DeepSeek / Qwen complete (miss=0). Claude miss **98** (all 人工智能招聘; 45 of them in SimHuman 980). Kimi miss **293** (人工智能 246 + 阿里云 47; 160 in SimHuman 980). Incomplete rows empty-fill missing IDs; they are **not** complete main-table rows until the queues are filled. Queues: `fill_later/missing_queue_Claude.jsonl`, `missing_queue_Kimi.jsonl`.

Optional later (do not use as this pass): Claude filled haiku+sonnet 0.1519 / 0.3416; Kimi filled 0.1093 / 0.2321.

## SOP extract re-call pilots (2026-08-25/26; not main tables)

Scored with `cnss-lskt-1.2.0`. Prompt = SOP extract v4 (sentence only, no rule_v4 silver). **Do not** put these rows in PDF Table 3, Gold v2 unique-first, the abstract SOTA sentence, or the matched-protocol 2601 table. They answer: does a new SOP prompt lift LLM exact F1 on hybrid vs the frozen `@@span##` dumps? **No.**

Same 100 hybrid IDs (seed `20260825`; 38 SimHuman + 62 SOP-CWS). Model `gpt-5.4` via `https://claudeed.ysaikeji.cn`. JSON: `reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100/summary_gpt-5.4.json`.

| System (n=100) | hybrid jieba exact | hybrid jieba relaxed | Gold v2 raw exact | Gold v2 raw relaxed |
|---|---:|---:|---:|---:|
| gpt-5.4 SOP extract | 0.2338 | 0.4623 | 0.4016 | 0.5236 |
| ChatGPT old dump (same 100 IDs) | 0.3356 | 0.6299 | 0.7016 | 0.8065 |

Partial `deepseek-v4-pro` (official API, `reasoning_effort=high` + thinking; **46/100**, stopped). JSON: `summary_deepseek-v4-pro_n46.json`. Same 46 IDs vs old dump.

| System (n=46) | hybrid jieba exact | hybrid jieba relaxed | Gold v2 raw exact | Gold v2 raw relaxed |
|---|---:|---:|---:|---:|
| deepseek-v4-pro SOP extract | 0.2353 | 0.5000 | 0.3678 | 0.4943 |
| ChatGPT old dump (same 46 IDs) | 0.3648 | 0.6667 | 0.6701 | 0.8223 |

Allowed claim: SOP extract re-calls of gpt-5.4 and DeepSeek V4 Pro **did not** raise hybrid typed exact above the frozen ChatGPT dump on the same IDs. Do not expand these two models to 2601 for the matched-protocol LLM column. Official `gpt-4o` + same SOP prompt is still the missing fair LLM re-call.

## Still missing / blocked (paper claims)

- Concept Accuracy / ESCO concept-ID eval — **blocked**, no concept IDs; delete the claim
- Time-OOD — **blocked**, no `year` field; delete the claim
- RoBERTa-wwm v3 3-seed mean **on Gold v2** — seeds exist on disk; mean not yet copied into the Gold v2 encoder table above
- BERT-CRF span-based, XLM-R zero-shot, ESCO lexicon rows
- SelfCheck + reflection as a frozen “our method” recipe
- Public data card / 200-item Gold analysis set as a named file
