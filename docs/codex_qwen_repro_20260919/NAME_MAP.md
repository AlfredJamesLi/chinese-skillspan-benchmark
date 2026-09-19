# Original path → pack path

Filenames inside each model directory keep original hashes. This map is names only.

## Protocol

| Original | Pack |
|---|---|
| `qwen_shared_guidelines_sft_20260910/inference/PROMPT_gold150_shared_guidelines_v2_rev2_patch1.DRAFT.system.txt` | `protocol/PROMPT_gold150_shared_guidelines_v2_rev2_patch1.DRAFT.system.txt` |
| `.../USER_TEMPLATE_v2_rev2_patch1.DRAFT.txt` | `protocol/USER_TEMPLATE_v2_rev2_patch1.DRAFT.txt` |
| `.../parser_occurrence_v1_1.py` | `protocol/parser_occurrence_v1_1.py` |
| public clone `data/gold150_test.jsonl` | `protocol/gold150_test.jsonl` |

## B2 (server A: DS209213)

Root: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/qwen_shared_guidelines_sft_20260910/`

Handoff copy also existed as `gold150_final_experiment_handoff_20260911/pack/02_sft/`. Inventory keys `02_sft/*` are `shared_guidelines_b2/02_sft/*`.

| Original | Pack |
|---|---|
| `runs/seed{42,43,44}/adapter/adapter_model.safetensors` (+ tokenizer files, `adapter_config.json`) | `shared_guidelines_b2/seed{42,43,44}/adapter/` |
| `runs/seed*/{selected_checkpoint,epoch_history,run_config}.json` | `shared_guidelines_b2/seed*/` |
| `runs/seed*/gold150/*` | `shared_guidelines_b2/seed*/gold150/` |
| `TRAIN_CONFIG.json`, `DATA_MANIFEST.json`, `MODEL_PROVENANCE.json`, … | `shared_guidelines_b2/configs/` and `shared_guidelines_b2/02_sft/configs/` |
| `scripts/infer_gold150_sft.py`, `train_sft.py`, `common.py`, sbatch | `shared_guidelines_b2/scripts/` |

`adapter/dev_pred.jsonl` and `dev_gold.jsonl` (Silver-dev sentences) were **not** copied.

## Expanded Silver pools (server B: DS210039)

| Original | Pack |
|---|---|
| `.../output/qwen_mixed_student_sft_20260915/runs/seed42/adapter/` | `expanded_silver/proxy_seed42/adapter/` |
| `.../qwen_mixed_student_sft_20260915/runs/seed42/gold150/` | `expanded_silver/proxy_seed42/gold150/` |
| `.../qwen_mixed_student_sft_20260915/data/SPLIT.json` | `expanded_silver/proxy_seed42/data/SPLIT.json` |
| `.../output/qwen_mixed_codex2500_sft_20260916/runs/seed42/adapter/` | `expanded_silver/codex_seed42/adapter/` |
| `.../qwen_mixed_codex2500_sft_20260916/runs/seed42/gold150/` | `expanded_silver/codex_seed42/gold150/` |

Occurrence jsonl (`train_occurrence.jsonl` etc.) were **not** copied. ID-only lists: `data/split_ids_{train,val,test}.jsonl`.

## Optional Table H (not substitutes)

| Original | Pack |
|---|---|
| `output/qwen_wave12_only_sft_20260915/` | `expanded_silver/optional_table_h/wave12_seed42/` |
| `output/qwen_wave3_only_sft_20260915/` | `expanded_silver/optional_table_h/wave3_proxy_seed42/` |
| `output/qwen_wave3_codex_sft_20260915/` | `expanded_silver/optional_table_h/wave3_codex_seed42/` |
| `output/qwen_new_silver_sft_20260914/` | `expanded_silver/optional_table_h/silver7117_fulldev_seed42/` |

The 7,117/559 tree is the path named in private pack notes. It is **not** B2 seed 42/43/44 and **not** the 9,646 / 9,540 pool models.

## Eval

| Original | Pack |
|---|---|
| `chinese-skillspan-benchmark/scripts/eval_gold150_ext.py` | `eval_runtime/scripts/eval_gold150_ext.py` |
| `chinese-skillspan-benchmark/scorer/score_lskt.py` | `eval_runtime/scorer/score_lskt.py` |
