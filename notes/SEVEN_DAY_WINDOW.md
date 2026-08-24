# 7-day server window (2026-08-24 → 08-31)

Lab machine may disappear. Maximize scorable artifacts + GitHub private backup.

**Repo:** https://github.com/AlfredJamesLi/chinese-skillspan-benchmark  
**After every finished run:** `bash scripts/backup_push_github.sh "why"`

## Running now (2026-08-24 20:20)

| Job | Where | Goal |
|---|---|---|
| RoBERTa-wwm v3 CRF seed 123 | GPU 3 (unschedled, stacked with Access 50645) | vanilla 3-seed |
| Access `aseries_rest` 50645 | GPU 3 Slurm | Sayfullina A4 then SkillSpan oldPrompt / FIJO k=7 |
| SLURM 50649 `jbzh_domain1m` | PD AssocMaxJobsLimit | **redundant** — domain-mix MLM + CRF already scored |

Do not cancel 50645. Domain-mix F1 is already in `confirmed-results.md`. 50649 can be cancelled if the user agrees.

## Done this afternoon / evening

- Relaxed F1 Gold v2 table
- Per-domain / Industry-OOD proxy table (事业单位 is encoder failure mode)
- JobBERT 1M / 3M ckpt65000 / domain-mix **3-seed** typed exact
- Domain-mix 1M seed 42 事业单位 0.0287 (still a failure mode)
- GitHub landing README updated

## Do not spend remaining wall-clock on

- listed-3M (1M lost to 0.1224)
- Concept Accuracy / Time-OOD (no fields)
- Uploading `output/` weights to GitHub (53GB)

## Domain-mix 1M DAPT (scored 2026-08-24)

Mix was AI / 应届生 / 阿里云 / 事业单位 (no listed). MLM + CRF finished locally; SLURM 50649 is leftover/redundant.
Seed 42 typed F1 **0.1234**; 3-seed mean **0.1269** (below JobBERT 1M 0.1288). 事业单位 0.0287 — still a failure mode. Do not scale to 3M.
Do not cancel 50645 `aseries_rest`.

## If GPU 3 frees after RoBERTa seed 123

1. RoBERTa seed 2026 for vanilla 3-seed mean
2. Snapshot every `run_summary.json` even if GitHub push fails
3. Hybrid/RAG on Qwen only if the user asks
