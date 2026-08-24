# 7-day server window (2026-08-24 → 08-31)

Lab machine may disappear. Maximize scorable artifacts + GitHub private backup.

**Repo:** https://github.com/AlfredJamesLi/chinese-skillspan-benchmark  
**After every finished run:** `bash scripts/backup_push_github.sh "why"`

## Running now (2026-08-24 15:40)

| Job | Where | Goal |
|---|---|---|
| Encoder 3-seed CRF | GPU 3, `output/encoder_3seed/` | seeds 123/2026 × ckpt65000, 1M, vanilla |
| Claude/Kimi fill | CPU + API | 98 + 293 missing Gold IDs |

Do not cancel SLURM 50644 (other user job on this account).

## Done this afternoon

- Relaxed F1 Gold v2 table
- Per-domain / Industry-OOD proxy table (事业单位 is encoder failure mode)
- GitHub landing README updated

## Do not spend remaining wall-clock on

- listed-3M (1M lost to 0.1224)
- Concept Accuracy / Time-OOD (no fields)
- Uploading `output/` weights to GitHub (53GB)

## Domain-mix 1M DAPT (submitted 2026-08-24 16:05)

Mix: 人工智能 35% / 应届生 25% / 阿里云 22% / 事业单位 14%. No listed.
Corpus builder + `wait_then_domain_1m.sh` (local GPU waiter; SLURM MaxJobs=1).
Do not cancel 50644 `hyb_panelB` / 50645 `aseries_rest`.
Do not stack on busy GPUs. 3-seed CRF on GPU 2/3 keeps running.

## If GPU 3 frees after 3-seed and time remains

1. Domain-mix 1M waiter should already grab the first idle card
2. Hybrid/RAG needs Qwen GPU — only if 3-seed + domain-1M are done
3. Snapshot every `run_summary.json` even if GitHub push fails
