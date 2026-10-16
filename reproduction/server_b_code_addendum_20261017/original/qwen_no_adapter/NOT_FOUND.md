# Qwen no-adapter generation entry — 本次未找到

This directory is **not** the original generator of the 0.3612 paired baseline.

Searched on DS210039 (2026-10-17): scripts under `Chinese_skill_benchmark_Paper/`, `SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/scripts/`, and `CNSS_Qwen_Reproduction/`. No file was found that writes `output/gold150_shared_prompt_rev2_run_20260910` with `adapter: null`.

`infer_gold150_sft.py` **requires** a LoRA adapter and is **not** included here. It must not be presented as the baseline generator.

What is included: pairing fingerprints only (`BASELINE_COMPATIBILITY.md`, frozen system/user/parser). Those documents say the missing run lived on **DS209213**, Slurm **50966/50967**. Look there next.

Do not rewrite a no-adapter infer script and claim it was the original.
