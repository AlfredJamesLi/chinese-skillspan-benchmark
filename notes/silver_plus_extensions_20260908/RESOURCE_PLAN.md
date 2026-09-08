# Resource plan

## Caps

- Official new trains ≤ 18: Qwen 3 + H/E/M 9 + 1M 6.
- 1M official block **skipped** → official cap this round = **12 trains**.
- Qwen official Gold evals = 3 (SFT × seeds 42/43/44). Not 9 A/B/C evals.
- Smoke / parser / leftover index builds are extra and logged separately.
- This experiment chain uses **at most two GPUs at any time**.

## Scheduler

- Partition: `LocalQ`. Account `student`, QOS `gpu_limit_2`（MaxJobs=1，MaxWall=1 天，最多 2 卡）。
- 提交时加 `--account=student --gres=gpu:2`。未写 account 时 24h 墙钟会被 AssocMaxWall 拒绝。
- 作业内只使用调度器下发的 `CUDA_VISIBLE_DEVICES`，不写死物理 GPU 2/3。
- 本链同时最多一张作业、两张卡。不终止 7322 或其他用户进程。
- 已提交：**job 7349** `ext_silver`（2026-09-08 13:24–14:08，FAILED 2:0）。42/43 SFT 已完成；脚本在续跑时因运行中被改写而解析失败，44 / Gold / HEM 未开始。
- 续跑：**job 7360**（2026-09-08 14:36 提交）。42/43 训练跳过，接着 44 → Gold ×3 → HEM ×9。

## Qwen (first)

| Item | Plan |
|---|---|
| Model | Qwen2.5-14B-Instruct, 1 GPU / run |
| Seeds | 42 and 43 in parallel, then 44 |
| Train | B2 only, SFT, no demos |
| Select | one checkpoint per seed on **dev typed exact** |
| Gold | 3 SFT evals after freeze |
| Effective batch | 1 × 16 accum, same for all seeds |

## JobBERT H/E/M (second)

| Item | Plan |
|---|---|
| Student | 3M DAPT encoder + **new** CRF (no released `best.pt`) |
| Parallelism | one run per GPU; two at a time; leftover third seed |
| Official trains | 9 |

## 1M (third)

Skipped. See `MODEL_PROVENANCE.json`.

## Logging per run

Each completed run writes `RESOURCE.json` when the process supports it:

- `job_id`, `hostname`, `cuda_visible_devices`
- `start_iso`, `end_iso`
- `peak_allocated_gib`
- `gpu_hours` = elapsed hours × n_visible_gpus (here 1)

A chain ledger is appended at `output/silver_plus_extensions/RESOURCE_LOG.jsonl`.
Seeds 42/43 started before RESOURCE.json was added to the trainer; their wall time is taken from `run_config.json` / `train.log` after finish.
