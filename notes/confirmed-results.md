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

## Not found in repo (paper claims)

- Relaxed F1 (IoU≥0.5) official table
- Concept Accuracy / ESCO concept-ID eval
- Industry-OOD and Time-OOD splits (no `year` field; test domains exist)
- 3-seed averages
- BERT-CRF, span-based, XLM-R zero-shot, ESCO lexicon rows
- SelfCheck + reflection as a frozen “our method” recipe
- Public data card / 200-item Gold analysis set as a named file
