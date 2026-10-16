# Qwen no-adapter Gold150 shared-guidelines baseline — original files from A

- Host: **DS209213** (server A), IP 144.214.209.213
- Packed: 2026-10-17 (local). Sources dated 2026-09-10.
- Workspace: `/home/guojingli3/SCESC-LLM-skill-extraction`
- Run tree: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910`
- **Original generation entry found: yes** (`scripts/run_qwen_worker.py`)
- Not rewritten. Copies are `cp -a` / shutil.copy2 unless marked excerpt.
- Not SFT. `infer_gold150_sft.py` was not used as this entry.
- No weights, no API keys, no MacroData CSV, no full silver, no GitHub push.

## How it was started (not re-run)

1. `sbatch .../scripts/gold150_qwen.sbatch` → Slurm **50966** (`g150qwen`).
2. Two `srun` workers: `jpy-qwen25` python `-u run_qwen_worker.py --worker 0|1 --phase smoke-then-formal`.
3. Job 50966 worker1 OOM; worker0 completed. Then `sbatch .../gold150_qwen_shard1.sbatch` → Slurm **50967** (`g150qw1`) for worker 1 only, then `merge_qwen_shards.py`.

`run_qwen_worker.py` loads `Qwen2.5-14B-Instruct` with `AutoModelForCausalLM.from_pretrained` (no `PeftModel`). Fingerprint `"adapter": null`, `do_sample: false`, `max_new_tokens: 2048`, parser `occurrence_v1.1` / `parser_occurrence_v1_1.py`, system/user rev2 patch1 freeze hashes in `FREEZE_REGISTRY.json`.

Typed exact F1 in `run_bind/SCORE.json` → `qwen25-14b-instruct.typed_exact_f1` = **0.3611650485436893** (display 0.3612). Pred file: 150 lines.

## Expected SHA-256 (verified on this pack)

| file | SHA-256 |
|---|---|
| fingerprints/worker0.CONFIG_FINGERPRINT.json | c5f872beeedaa8e9df76529f5b0b11c7c6966cd65a17262c7578a06530d9dd5f |
| fingerprints/worker1.CONFIG_FINGERPRINT.json | 9ed5c44e92af1818cf96cbe31206b1ba7f81ef86b9d934c330364c326383ab80 |
| run_bind/pred_for_score.jsonl | 85cfc0ff493cbb97c52c62c6306ad3fc141b9bc9710c667fafe4418f8a8763ea |

PeerJ layout `01_shared_prompt/configs/qwen25-14b-instruct/worker0.CONFIG_FINGERPRINT.json` is a **renamed copy** of `runs/qwen25-14b-instruct/worker0/CONFIG_FINGERPRINT.json` (also in `output/gold150_final_experiment_handoff_20260911/pack/...`). Same bytes.

## Searched (not used as this entry)

- `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/scripts/` — no second original worker; launchers live in the run tree.
- `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/qwen_shared_guidelines_sft_20260910/` — SFT (`infer_gold150_sft.py` needs LoRA); excluded.
- `run_gold150_shared_prompt.py` — paid API runner for other models; **not** the Qwen no-adapter generator; not copied.
- `infer_gold150_sft.py`, `train_sft.py`, JSON-offset infer scripts, gold150_benchmark_audit eval-adapt v4210 — excluded.

## Not in this pack

Worker `states/*.json` / `records.jsonl` (full generations). Qwen weights. Gold150 text shards under `inputs/` (job-ad text). API logs.
