# How to adjust so the repo matches the paper

## Use these paths (canonical)

| Role | Path |
|---|---|
| Table 1 splits | `data/annotated/processed/chinese_skillspan/{train,dev,test}.json` |
| Table 3 gold | `chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl` |
| GPT-4o pred | `chinese_skillspan_preprocessing/output/dir/test-gpt/silver_gpt4o_sent_ner_test_1005_last_test.jsonl` |
| Claude pred | `.../output/dir/test_claude/merged_test_cluade.jsonl` (incomplete) |
| Kimi pred | `.../output/dir/test-kimi/merged_test_kimi.jsonl` (incomplete) |
| DeepSeek pred | `.../output/dir/test-deepseek/ds_test_.merged.jsonl` |
| Qwen pred | `output/chinese_skillspan_qwen25-14b_test_all.jsonl` (do **not** use `*_test_all_1`, only 163 rows) |

Do **not** score `chinese_skillspan_preprocessing/data/annotated/processed/chinese_skillspan/test.json` — 2639 sentences, empty labels.

## Pitfalls (do not re-use these numbers as Table 3)

1. `evaluate_src.py` dumps such as `silver_gpt4o_sent_ner_test_1005_last_test.eval_ner.json` report GPT F1 ≈ **0.004**. That is scoring silver `pred` against empty/untyped `gold` on the preprocessing tree, not against `admin_Baseline_test.jsonl`. The paper number 0.6700 comes from collapsed exact-span vs that Gold file.
2. `LLaMA-Factory/data/train_lkst_S.json` has **2142** rows (dev-sized), not the 17460-sentence train split. S-only LoRA (`sft_CN_skillspan_ner_skills_2000`) was not trained on full train.
3. Root test sanity: `output/chinese_skillspan/gold_as_pred.eval_ner.json` is 3237 sents / 6864 spans at F1=1.0 — that only proves the scorer matches the root tree, not Table 3.

## P0 — make Table 3 reproducible

1. Freeze one scorer: exact-span F1, skill-collapsed for ChatGPT/JobBERT (already 0.6703 / 0.0045 / 0.0038). Decide whether DeepSeek stays **typed** (0.5149 ≈ 0.5130).
2. Finish Claude + Kimi shards to full 3237, merge, rescore on the same 2676 gold IDs.
3. Isolate the paper’s Qwen: paper 0.2130 is not the current dump (0.34–0.39). Check size (7B vs 14B), SFT vs base, and whether they scored only dimension S (`qwen2p5_S_predictions.metrics.json` F1=0.078). Re-run that setting; do not overwrite `output/chinese_skillspan_qwen25-14b_test_all.jsonl` until copied.

## P1 — Table 1 span averages

#Sent and Avg Len already match. Avg 4D / L/K/S/T on root `list_of_selection_bio4` are ~8% lower than the PDF. Either recount from the silver+gold merge used when the table was written, or update the PDF to the current bio4 counts.

## P2 — paper items not in the repo

Implement or drop from the camera-ready: Relaxed IoU F1, Concept Accuracy, IAA n=100, Time/Industry OOD, encoder/lexicon baselines, 3 seeds. Test `source_domain` already has 应届生 / 人工智能 / 阿里云 / 事业单位 — usable for Industry-OOD after a written hold-out list.
