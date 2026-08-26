# Confirmed results (Chinese-SkillSpan)

Extracted from uploaded PDF:

`Chinese_skill_benchmark_Paper/2026_New_DASFAA_Chinese_SkillSpan__A_Span_Level_Dataset_for_ESCO_Aligned_Competency_Extraction_from_Chinese_Job_Ads.pdf`

Venue: **PeerJ Computer Science** (submission target). The extracted PDF filename still contains DASFAA 2026; treat that as a draft filename only. Task: Chinese JobSkillNER, ESCO-1.20, flat **LSKT** (L/K/S/T).  
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

## Model IDs (dump `model` field; do not invent dates)

CSV: `tables/model_ids.csv`. Use these strings in every results table. Counted on unique-first views.

| Paper name | Dump model id | Coverage |
|---|---|---|
| ChatGPT | `gpt-4o` | 2639/2639 |
| Claude | `claude-3-5-haiku-20241022` | 2536; miss 98. Filled view adds 98× `claude-sonnet-4-6` |
| Kimi | `kimi-k2-0711-preview` | 2341; miss 293. Filled view uses `kimi-k2.6` |
| DeepSeek | `deepseek-r1` | 2639/2639 |
| Qwen | `Qwen2.5-14B-Instruct` | 3237/3237 |
| JobBERT-zh | `chinese-roberta-wwm-ext` + JD MLM + CRF | 1M/3M = DAPT size |
| RoBERTa-wwm | `chinese-roberta-wwm-ext` | vanilla CRF |

## Table 3 — strict S-F1 (paper vs this repo, 2026-08-22 rescore)

Gold for rescore: `chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl` (2676).  
Span metric: exact (start, end, type) or collapsed to SKILL.

| Model | Paper S-F1 | Repo typed F1 | Repo collapsed F1 | Pred dump n | Verdict |
|---|---:|---:|---:|---:|---|
| ChatGPT (`gpt-4o`) | 0.6700 | 0.6836 | **0.6703** | 3237 | **Match** (collapsed) |
| Claude (`claude-3-5-haiku-20241022`) | 0.6300 | 0.5712 | 0.6062 | 2536 | Close; dump incomplete |
| Kimi (`kimi-k2-0711-preview`) | 0.5700 | 0.5310 | 0.5618 | 2341 | Close; dump incomplete |
| DeepSeek (`deepseek-r1`) | 0.5130 | **0.5149** | 0.5479 | 2639 | **Match** (typed) |
| Qwen (`Qwen2.5-14B-Instruct`) | 0.2130 | 0.3442 | 0.3949 | 3237 / 2601 aligned | **Gap** |
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
| ChatGPT (`gpt-4o`) | 0.6700 | 0.6365 | 0.6403 | **0.7221** | OK |
| DeepSeek (`deepseek-r1`) | 0.5130 | 0.1327 | 0.3569 | 0.1798 | OK |
| Qwen (`Qwen2.5-14B-Instruct`) | 0.2130 | 0.0791 | 0.1075 | 0.1272 | OK |
| JobBERT-skill | 0.0045 | 0.0000 | 0.0045 | 0.0000 | OK |
| JobBERT-knowledge | 0.0038 | 0.0000 | 0.0037 | 0.0000 | OK |
| Claude (`claude-3-5-haiku-20241022` + 98× `claude-sonnet-4-6`) | 0.6300 | **0.2583** | 0.2970 | 0.3861 | OK (haiku dump + 98 sonnet fills) |
| Kimi (`kimi-k2-0711-preview`) | 0.5700 | 0.1651 | 0.3349 | 0.2130* | Missing 293 IDs |

Claude Gold v2 is complete at 2601/2601 via `reports/views/Claude_filled_v2.jsonl` (original haiku dump + 98 sonnet-4-6 fills). Original `merged_test_cluade.jsonl` untouched. Incomplete unique-first view is still 0.2570 typed (matched-only). Kimi original dump still misses 293 IDs; use `Kimi_filled_v2.jsonl` for the filled row.

## Per-domain typed exact F1 (Industry-OOD proxy; Gold v2)

Domains: 人工智能招聘 1407 / 事业单位招聘 737 / 阿里云公开数据集 457.  
No `year` field → **do not claim Time-OOD**. CSV: `tables/per_domain_gold_v2.csv`.

| System | 人工智能 | 阿里云 | 事业单位 |
|---|---:|---:|---|
| ChatGPT (`gpt-4o`) | 0.6489 | 0.5650 | **0.7032** |
| DeepSeek (`deepseek-r1`) | 0.1392 | 0.1293 | 0.0805 |
| Qwen (`Qwen2.5-14B-Instruct`) | 0.0887 | 0.0646 | 0.0207 |
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

CSV: `tables/encoder_3seed_gold_v2.csv`. Sample std over three seeds.

| Run | seed 42 | seed 123 | seed 2026 | mean | std |
|---|---:|---:|---:|---:|---:|
| JobBERT 1M | 0.1224 | 0.1292 | 0.1348 | **0.1288** | 0.0062 |
| domain-mix 1M | 0.1234 | 0.1280 | 0.1294 | 0.1269 | 0.0031 |
| JobBERT 3M ckpt65000 | 0.1233 | 0.1295 | 0.1246 | 0.1258 | 0.0033 |
| RoBERTa-wwm v3 | 0.1156 | 0.1187 | 0.1254 | 0.1199 | 0.0050 |

3-seed mean: domain-mix 0.1269 **below** JobBERT 1M 0.1288. RoBERTa-wwm v3 **0.1199** is the weakest of the four. Do not scale domain-mix to 3M. Encoder remains a weak baseline (~0.13 vs ChatGPT 0.6365 typed). JobBERT 1M goldstyle **5-seed** (add seeds 7 and 13) is running; do **not** write a 5-seed mean until those two `run_summary.json` files exist.

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
| ChatGPT (`gpt-4o`, old dump, complete) | 0.2854 | **0.6249** | 0.2836 | **0.6447** |
| Claude (`claude-3-5-haiku-20241022`, 98 empty) | 0.1483 | 0.3349 | 0.1757 | 0.4062 |
| Kimi (`kimi-k2-0711-preview`, 293 empty) | 0.0964 | 0.1997 | 0.1011 | 0.2183 |
| DeepSeek (`deepseek-r1`, old dump, complete) | 0.0802 | 0.1577 | 0.0738 | 0.1573 |
| Qwen (`Qwen2.5-14B-Instruct`, old dump, complete) | 0.0501 | 0.1409 | 0.0483 | 0.1361 |
| JobBERT-skill EN head | 0.0096 | 0.0676 | 0.0124 | 0.0919 |
| JobBERT-knowledge EN head | 0.0088 | 0.0644 | 0.0122 | 0.0862 |

Allowed claim: under this matched SOP+jieba test gold, JobBERT-zh 1M/3M v4 lead typed exact (**0.4272 / 0.4331**); ChatGPT leads typed relaxed (**0.6249**). 980 SimHuman is consistent with full 2601 (Δ exact <0.01 for 1M/3M v4). Do not write these as beating ChatGPT on Gold v2.

LLM coverage on hybrid 2601 (old dumps, **no API this pass**): ChatGPT / DeepSeek / Qwen complete (miss=0). Claude miss **98** (all 人工智能招聘; 45 of them in SimHuman 980). Kimi miss **293** (人工智能 246 + 阿里云 47; 160 in SimHuman 980). Incomplete rows empty-fill missing IDs; they are **not** complete main-table rows until the queues are filled. Queues: `fill_later/missing_queue_Claude.jsonl`, `missing_queue_Kimi.jsonl`.

Optional later (do not use as this pass): Claude filled haiku+sonnet 0.1519 / 0.3416; Kimi filled 0.1093 / 0.2321.

## SOP extract re-call pilots (2026-08-25; subset IDs; not main tables)

Scored with `cnss-lskt-1.2.0`. Prompt = SOP extract v4 (sentence only, no rule_v4 silver). **Do not** put these rows in PDF Table 3, Gold v2 unique-first, the abstract SOTA sentence, or the matched-protocol 2601 table.

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

Allowed claim: on these **subset** IDs, SOP extract did **not** beat the frozen ChatGPT dump. The n=100 gpt-5.4 cell **0.2338 is not** the full-n number (full-n is 0.2132 below). Do not mix n=100 with n=2601.

## SOP extract full P2-2601 (2026-08-26; diagnostic LLM table, not P2 main)

Authorized 2026-08-26. Same SOP extract v4 prompt, jieba snap, scorer `cnss-lskt-1.2.0`, gold `test_lskt_v4_cws_simhuman980_hybrid.jsonl`. Coverage 2601/2601, `alignment_ok`. CSV: `tables/sop_extract_p2_2601.csv`.

**Do not** put these rows into PDF Table 3, Gold v2 unique-first, the abstract SOTA sentence, or the matched-protocol **main** 2601 table (that table stays **frozen `@@span##` dumps** + jieba). These are **new models / new prompt**, not replacements for `gpt-4o` / `claude-3-5-haiku-20241022` / `kimi-k2-0711-preview` / `deepseek-r1`.

| System | n=2601 exact | n=2601 relaxed | n=980 exact | n=980 relaxed | Source |
|---|---:|---:|---:|---:|---|
| gpt-5.4 SOP extract | **0.2132** | **0.4199** | 0.2063 | 0.4207 | `sop_extract_p2_2601/gpt-5.4/summary_gpt-5.4.json` |
| kimi-k2.6 SOP extract | 0.1979 | 0.4032 | 0.1912 | 0.4108 | `sop_extract_p2_2601/kimi-k2.6/summary_kimi-k2.6.json` |
| deepseek-v4-pro SOP extract | 0.1980 | 0.3931 | 0.1847 | 0.3973 | `sop_extract_p2_2601/deepseek-v4-pro/summary_deepseek-v4-pro.json` |
| claude-sonnet-4-5 SOP extract | 0.1972 | 0.3987 | 0.1861 | 0.3945 | `sop_extract_p2_2601/claude-sonnet-4-5/summary_claude-sonnet-4-5.json` |
| Qwen2.5-14B-Instruct SOP extract (local, no LoRA) | 0.1724 | 0.3279 | 0.1711 | 0.3390 | `reports/qwen25_14b_instruct_sopv4_p2_2601_scores.csv` |
| Llama-3-8B-Instruct SOP extract (local, no LoRA) | 0.0582 | 0.1178 | 0.0544 | 0.1140 | `reports/llama3_8b_instruct_sopv4_p2_2601_scores.csv` |
| ChatGPT (`gpt-4o`, frozen dump + jieba) | 0.2854 | **0.6249** | 0.2836 | 0.6447 | P2 main table (not a SOP re-call) |
| JobBERT 3M v4 + jieba | **0.4331** | 0.5873 | 0.4401 | 0.6032 | P2 main table |

Qwen SOP extract vs the **same model’s frozen dump** on P2: 0.1724 vs 0.0501 (prompt lift). Qwen SOP preds scored **raw** on Gold v2 (diagnostic only): typed exact **0.2134** / relaxed 0.2999. That is **not** a reproduction of paper Qwen S-F1 0.2130 (different gold and prompt). Do not put 0.2134 into Gold v2 unique-first (frozen Qwen dump there is 0.0791). Llama SOP raw-on-Gold-v2 diagnostic: typed exact **0.0641** / relaxed 0.0952 (parser failures 324/2601); do not put into Gold v2 unique-first.

Allowed claim: full-n SOP extract re-calls **did not** beat frozen ChatGPT P2 exact **0.2854** or relaxed **0.6249**, and **did not** beat JobBERT 3M v4 exact **0.4331**. Official `gpt-4o` + the same SOP prompt is still missing.

**Not yet scored (do not invent F1):** claude-sonnet-4-6 SOP extract paused at **460/2601** (user stop; 4.5 already covers the same prompt); Qwen LoRA SFT on SOP extract (died ~step 980/4365; only `checkpoint-500` on disk; **no test F1**). Job 50649 `jbzh_domain1m` remains `JobHeldUser` and is redundant given the 3-seed domain-mix already in the encoder table.

## Workload vs SkillSpan 2022 (main-text claim; counts, not English F1)

CSV: `tables/appendix_workload_vs_skillspan.csv`. Source for SkillSpan counts: Zhang et al. NAACL 2022 (391 English JPs, 14.5K sentences). Do **not** write SkillSpan English span-F1 next to our Gold v2 0.1288 as the same task.

Allowed main-text sentence: relative to SkillSpan, this resource is larger (17,460 training sentences vs 14.5K annotated sentences in total), uses a four-type LSKT schema rather than two nested labels, reports two evaluation protocols, includes Chinese DAPT at 1M and 3M plus encoder ablations with three seeds, and evaluates frozen and re-prompted LLMs that SkillSpan did not study. We do **not** clone SpanBERT-from-scratch or their 4×STL/MTL grid.

## Appendix — typed P/R (Gold v2; SkillSpan Table 6 analogue)

CSV: `tables/appendix_pr_gold_v2.csv`. Encoder cells = 3-seed mean ± sample std. LLM = single dump. Scorer `cnss-lskt-1.2.0`. Kimi empty-fills 293 missing IDs (F1 **0.1522**); unique-first matched-only Kimi remains **0.1651** in the Gold v2 LLM table — do not overwrite.

| System | P | R | F1 |
|---|---:|---:|---:|
| ChatGPT (`gpt-4o`) | 0.6264 | 0.6469 | **0.6365** |
| Claude filled (haiku+98 sonnet-4-6) | 0.2300 | 0.2947 | 0.2583 |
| JobBERT 1M goldstyle v3 (3-seed) | 0.1864±0.0137 | 0.0984±0.0037 | 0.1288±0.0062 |
| domain-mix 1M (3-seed) | 0.1841±0.0029 | 0.0969±0.0033 | 0.1269±0.0031 |
| JobBERT 3M ckpt65000 (3-seed) | 0.1785±0.0055 | 0.0972±0.0030 | 0.1258±0.0033 |
| RoBERTa-wwm v3 (3-seed) | 0.1695±0.0126 | 0.0928±0.0024 | 0.1199±0.0050 |
| DeepSeek (`deepseek-r1`) | 0.1384 | 0.1274 | 0.1327 |
| Kimi empty-fill (293 missing) | 0.1677 | 0.1393 | 0.1522 |
| Qwen (`Qwen2.5-14B-Instruct`) | 0.2178 | 0.0483 | 0.0791 |

Allowed: encoders are **precision-low, recall-lower** (~0.17–0.19 P / ~0.09–0.10 R). Qwen dump is high-P low-R (0.2178 / 0.0483). ChatGPT is the only balanced high-P high-R system on Gold v2.

## Appendix — domain × 3-seed typed F1 (Gold v2)

CSV: `tables/appendix_domain_mean_gold_v2.csv`. Seed-42 point estimates in `per_domain_gold_v2.csv` stay as the main per-domain table. This appendix adds seed std. n=1407 / 457 / 737.

| System | 人工智能 | 阿里云 | 事业单位 |
|---|---:|---:|---:|
| ChatGPT (`gpt-4o`) | 0.6489 | 0.5650 | **0.7032** |
| JobBERT 1M (3-seed) | 0.1365±0.0081 | 0.1354±0.0039 | 0.0213±0.0034 |
| domain-mix 1M (3-seed) | 0.1334±0.0052 | 0.1352±0.0021 | 0.0234±0.0071 |
| JobBERT 3M (3-seed) | 0.1344±0.0021 | 0.1315±0.0078 | 0.0147±0.0007 |
| RoBERTa-wwm v3 (3-seed) | 0.1301±0.0072 | 0.1186±0.0025 | 0.0126±0.0014 |
| DeepSeek (`deepseek-r1`) | 0.1392 | 0.1293 | 0.0805 |
| Qwen (`Qwen2.5-14B-Instruct`) | 0.0887 | 0.0646 | 0.0207 |

Allowed: 3-seed std does **not** rescue 事业单位 (encoder means 0.0126–0.0234). Domain-mix 3-seed 事业单位 0.0234±0.0071 still fails vs ChatGPT 0.7032.

## Appendix — span-length F1 (Gold v2; token length = end−start)

CSV: `tables/appendix_span_length_f1_gold_v2.csv`, `tables/appendix_span_length_mean_gold_v2.csv`. Exact typed F1 inside each gold/pred length bucket. Mean gold span length **4.90** tokens.

| System | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10+ | mean pred len |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT (`gpt-4o`) | 0.0357 | **0.7265** | 0.5643 | **0.7292** | 0.5095 | 0.6702 | 0.5066 | 0.5962 | 0.5183 | 0.5054 | 4.19 |
| JobBERT 1M seed 42 | 0.0000 | 0.1229 | 0.1347 | 0.1923 | 0.0758 | 0.1570 | 0.0669 | 0.0858 | 0.0743 | 0.0357 | 5.94 |
| JobBERT 1M seed 123 | 0.0000 | 0.1293 | 0.1452 | 0.1999 | 0.0879 | 0.1631 | 0.0636 | 0.0994 | 0.0737 | 0.0365 | 6.06 |
| RoBERTa-wwm v3 seed 42 | 0.0000 | 0.1105 | 0.1146 | 0.1882 | 0.0924 | 0.1357 | 0.0629 | 0.0851 | 0.0890 | 0.0372 | 5.98 |

Allowed: ChatGPT is weak on length-1 (0.0357) but strong on 2 and 4. Encoders predict **longer** spans than gold (5.94 vs 4.90) and collapse on length 1 and 10+.

## Appendix — encoder seed win-rate (ASO-style; n=3)

CSV: `tables/appendix_aso_encoder_3seed_gold_v2.csv`. Cell = P(row seed F1 > col seed F1) over 3×3 pairs. **Not** SkillSpan’s full ASO+Bonferroni (they used 5 seeds). Caption must say n=3 is under-powered.

| row \ col | JobBERT 1M | domain-mix | JobBERT 3M | RoBERTa-wwm |
|---|---:|---:|---:|---:|
| JobBERT 1M | — | 0.5556 | 0.5556 | **0.8889** |
| domain-mix | 0.4444 | — | 0.5556 | **0.8889** |
| JobBERT 3M | 0.4444 | 0.4444 | — | 0.7778 |
| RoBERTa-wwm | 0.1111 | 0.1111 | 0.2222 | — |

Allowed: JobBERT 1M / domain-mix / 3M are **not** separable at n=3. All three beat RoBERTa-wwm more often than not. Do not claim stochastic dominance among the three JobBERT variants.

## Appendix — matched-protocol P/R (P2; not Gold v2)

CSV: `tables/appendix_pr_p2_matched.csv` (from `hybrid_cws_simhuman980_all_models.csv`). Round to 4 decimals. **Not** comparable to Gold v2 ChatGPT 0.6365.

| System | P | R | F1 |
|---|---:|---:|---:|
| JobBERT 3M v4 + jieba | 0.4730 | 0.3994 | **0.4331** |
| JobBERT 1M v4 + jieba | 0.4685 | 0.3925 | 0.4272 |
| JobBERT 1M CWS retrain + jieba | 0.4537 | 0.3655 | 0.4049 |
| ChatGPT (`gpt-4o`, frozen + jieba) | 0.2371 | 0.3584 | 0.2854 |
| DeepSeek (`deepseek-r1`, frozen + jieba) | 0.0682 | 0.0974 | 0.0802 |
| Qwen (`Qwen2.5-14B-Instruct`, frozen + jieba) | 0.0999 | 0.0334 | 0.0501 |

Allowed: on P2, JobBERT v4 leads **both** P and exact F1; ChatGPT still leads relaxed (0.6249 in the P2 main table).

## Still missing / blocked (paper claims)

- Concept Accuracy / ESCO concept-ID eval — **blocked**, no concept IDs; delete the claim
- Time-OOD — **blocked**, no `year` field; delete the claim
- JobBERT 1M goldstyle **5-seed mean** (seeds 7 and 13 launched 2026-08-26; 42/123/2026 already scored)
- BERT-CRF span-based, XLM-R zero-shot, ESCO lexicon rows
- SelfCheck + reflection as a frozen “our method” recipe
- Public data card / 200-item Gold analysis set as a named file
