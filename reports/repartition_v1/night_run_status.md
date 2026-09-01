# Night run status — repartition_v1

Slurm **50733** **COMPLETED** 2026-08-28 03:34:58–07:42:27, ExitCode **0:0**, RunTime 04:07:29. Pair `CUDA_VISIBLE_DEVICES=0,1`. No Traceback / OOM in run logs.

All **15/15** GPU processes finished with 4222/4222 ID coverage and `alignment_ok`.

| run_id | status | typed exact |
|---|---|---:|
| jobbert_1m seeds 42/123/2026 | done | 0.2985 / 0.2989 / 0.2996 |
| jobbert_3m seeds 42/123/2026 | done | 0.2921 / 0.2868 / 0.2886 |
| roberta_wwm seeds 42/123/2026 | done | 0.3060 / 0.3035 / 0.3115 |
| STL S/K/T/L then combined | done | combined 0.2905 |
| Qwen2.5-14B SOP 2 shards | done 2111+2111 | 0.1473 |

Bookkeeping only (not failed GPU jobs): `qwen25_sop/score_official.json` was not written; F1 is in `reports/repartition_v1/main_results_by_seed.csv`. `stl_1m/seed_42/combined/` has `test_pred.jsonl` + `stl_results.json`. CSV has a duplicate jobbert_1m seed 42 row from smoke+skip.

Not in this job: commercial APIs, Qwen LoRA, Llama-8B, MLM re-DAPT.
