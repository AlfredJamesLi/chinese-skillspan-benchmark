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

## If GPU 3 frees after 3-seed and time remains

1. Domain-filter DAPT is 12h — only start if ≥12h left
2. Hybrid/RAG needs Qwen GPU — only if 3-seed + fill are done
3. Snapshot every `run_summary.json` even if GitHub push fails
