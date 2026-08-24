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
| Claude | 0.6300 | 0.2570 | 0.2952 | 0.3789* | Missing 98 IDs |
| Kimi | 0.5700 | 0.1651 | 0.3349 | 0.2130* | Missing 293 IDs |

\* Claude/Kimi relaxed treats missing Gold IDs as empty predictions. **Not** complete main-table rows.

## Per-domain typed exact F1 (Industry-OOD proxy; Gold v2)

Domains: 人工智能招聘 1407 / 事业单位招聘 737 / 阿里云公开数据集 457.  
No `year` field → **do not claim Time-OOD**. CSV: `tables/per_domain_gold_v2.csv`.

| System | 人工智能 | 阿里云 | 事业单位 |
|---|---:|---:|---|
| ChatGPT | 0.6489 | 0.5650 | **0.7032** |
| DeepSeek | 0.1392 | 0.1293 | 0.0805 |
| Qwen | 0.0887 | 0.0646 | 0.0207 |
| JobBERT 3M ckpt65000 | **0.1323** | 0.1259 | 0.0150 |
| JobBERT 1M | 0.1287 | **0.1332** | 0.0181 |
| listed mix 1M | 0.1282 | 0.1240 | 0.0153 |
| RoBERTa-wwm v3 | 0.1242 | 0.1191 | 0.0115 |

Encoder fails on 事业单位 (~0.015) vs ~0.13 on 人工智能/阿里云. ChatGPT is strongest on 事业单位 (0.7032).

## Encoder CRF ranking (Gold v2 typed exact; seed 42)

CSV: `tables/encoder_gold_v2.csv`. Encoder is a **weak baseline**, not competitive with ChatGPT 0.6365 typed.

| Run | test F1 | dev F1 | vs 0.1224 |
|---|---:|---:|---|
| JobBERT 3M ckpt65000 | **0.1233** | 0.3205 | +0.0009 |
| JobBERT 1M + goldstyle v3 | **0.1224** | 0.3185 | baseline |
| human380 + v3 merge | 0.1207 | 0.3163 | −0.0017 |
| listed mix 1M | 0.1201 | 0.3257 | −0.0023 |
| JobBERT 3M final encoder | 0.1170 | 0.3209 | −0.0054 |
| JobBERT 3M ckpt100k | 0.1167 | 0.3207 | −0.0057 |
| JobBERT demo 80k | 0.1152 | 0.3231 | −0.0072 |
| RoBERTa-wwm goldstyle v3 | 0.1156 | 0.3210 | −0.0068 |

listed mix 1M **lost**; do **not** add listed-3M. Domain-mix 1M (AI 36.8% / 应届生 29.0% / 阿里云 22.0% / 事业单位 12.2%) is **running, no F1 yet**.

## Still missing / blocked (paper claims)

- Concept Accuracy / ESCO concept-ID eval — **blocked**, no concept IDs; delete the claim
- Time-OOD — **blocked**, no `year` field; delete the claim
- Encoder 3-seed **mean** — seeds 123/2026 still running; only seed 42 is confirmed
- BERT-CRF span-based, XLM-R zero-shot, ESCO lexicon rows
- SelfCheck + reflection as a frozen “our method” recipe
- Public data card / 200-item Gold analysis set as a named file
- Domain-mix 1M JobBERT F1 — corpus ready, **not scored**
