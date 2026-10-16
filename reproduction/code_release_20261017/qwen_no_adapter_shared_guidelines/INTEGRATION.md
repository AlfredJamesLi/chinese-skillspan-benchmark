# Recovered Qwen no-adapter shared-guideline entry (server A)

The laboratory supplied the original `run_qwen_worker.py`, two Slurm launchers and `merge_qwen_shards.py` from **DS209213 (server A)**. This closes the missing-original-generation-entry item. It does not establish that server B executed this worker; B supplied only pairing documents.

## Evidence and scope

- Original run tree: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910`.
- Generation entry: [scripts/run_qwen_worker.py](scripts/run_qwen_worker.py). [gold150_qwen.sbatch](scripts/gold150_qwen.sbatch) launches workers 0 and 1 in job 50966. Retained logs show worker1 OOM; [gold150_qwen_shard1.sbatch](scripts/gold150_qwen_shard1.sbatch) resumes worker1 in job 50967, followed by [merge_qwen_shards.py](scripts/merge_qwen_shards.py).
- Interpreter in the launchers: `/opt/anaconda3/envs/jpy-qwen25/bin/python`. No baseline runtime lock is inferred from the separately recorded SFT environment or from server B's current environment.
- Static source and both worker fingerprints agree: `AutoModelForCausalLM`, no PEFT loading, `adapter: null`, `do_sample: false`, `max_new_tokens: 2048`, bfloat16, frozen prompt/parser hashes. `infer_gold150_sft.py` still requires an adapter and is **not this baseline generator**.
- [SCORE.json](run_bind/SCORE.json) records typed exact F1 `0.3611650485436893`, displayed as `0.3612`. The 150-row prediction has SHA-256 `85cfc0ff493cbb97c52c62c6306ad3fc141b9bc9710c667fafe4418f8a8763ea`; it matches the existing repository inventory and the prediction hash in [the retained official score](../../model_diagnostics_20261003/official_scores/qwen_no_adapter/single.json), whose F1 also agrees. No rescoring was performed. The separately supplied older `score_qwen25-14b-instruct.json` references another prediction-file hash (`37fa887b...`) and is retained unchanged, not asserted to score these exact prediction-file bytes.
- Worker0 fingerprint SHA-256: `c5f872beeedaa8e9df76529f5b0b11c7c6966cd65a17262c7578a06530d9dd5f`.
- Worker1 fingerprint SHA-256: `9ed5c44e92af1818cf96cbe31206b1ba7f81ef86b9d934c330364c326383ab80`.

The supplied manifest records each A source path and checksum. Source files are copied unchanged. Sanitized log heads are explicitly marked as excerpts; they are not byte-identical full logs. Local verification establishes identity to the received ZIP and its manifest, not independent server access or a new reproduction run.

## Layout and execution prerequisites

All 24 received files remain at their supplied relative paths. The ZIP placed `FREEZE_REGISTRY.json` and `inference/` under `scripts/`, but the original worker resolves them at its parent run root. Four additional exact-byte copies restore those expected root locations; [INTEGRATION_AUDIT.json](INTEGRATION_AUDIT.json) records the mapping. Filenames and original source bytes are unchanged. The original `SHA256SUMS` verifies the received 23 listed files; the repository companion manifest also covers the added layout copies and audit documents.

This package omits Qwen base weights, adapters, the original input shards/synthetic smoke input, and complete worker states/generations. The retained prediction contains the already recorded evaluation tokens and predictions, not a full pretraining or expanded-silver collection. Source-text terms continue to apply. Launchers retain original A paths, and the worker uses a hard-coded model path. Re-execution requires the matching authorized inputs, model and compatible environment and a separate locally configured working copy. Do not run the historical launchers unchanged elsewhere. This audit did not run them.

ZIP SHA-256: `dd72adf7a27fd7538abf28f2e0646a74e494f667f8239b2e1491e0e278f2452d`. All 22 manifest entries and 23 SHA256SUMS entries pass. Three Python files parse, and both unique Slurm launchers pass Bash syntax validation. Other JobBERT runtime and native-stack gaps are unchanged.
