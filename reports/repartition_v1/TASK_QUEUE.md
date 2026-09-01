# repartition_v1 GPU task queue

New split changes which sentences are train vs test. Old checkpoints leak: **3163** old-train IDs sit in the new test. Anything that trains or scores on the old files must be re-run on `data/repartition_v1/{train,dev,test}.jsonl`. New output dirs only.

Account: **MaxJobs=1**, no `--gres=gpu`, legal pair **0+1 or 2+3**. One Slurm job holds both cards; pin one process per card. Do not `nohup` trainers.

## In this job (50733) — 15 GPU processes, packed onto 2 cards

| # | Task | Why | GPUs | Waves |
|---|---|---|---|---|
| 9 | Joint CRF: JobBERT 1M / 3M / RoBERTa-wwm × seeds 42, 123, 2026 | Same encoder ranking as the old V4 table; must retrain on new train/dev and score new test | 1 CRF / card | smoke 1M-s42, then 4 pairs |
| 4 | STL L/K/S/T, JobBERT 1M seed 42 | Appendix ablation vs joint; old STL used old silver + 2601 hybrid | 1 head / card | 2 pairs (S+K, T+L) |
| 2 | Qwen2.5-14B-Instruct SOP extract, 2 ID shards of 4222 | Local LLM row; frozen dump covers only 702/4222; no API | 1 shard / card | 1 pair |

Wall after smoke (~20 min left at epoch 4): CRF ~1.2 h + STL ~0.6 h + Qwen ~1–2 h ≈ **3–4 h**, target **~07:30–08:30**.

## Not in this Slurm job (and why)

| Item | Reason |
|---|---|
| ChatGPT / Claude / Kimi / DeepSeek / gpt-5.4 SOP | External API; this pass is local GPU only |
| Qwen LoRA SFT | Old LoRA never finished; must rebuild alpaca from **new** train first; 1×14B SFT is a later job |
| Llama-3-8B SOP extract | Optional local twin; submit after this job if still wanted |
| JobBERT 1M/3M MLM | Unlabeled DAPT, not this split; reuse frozen encoders |
| Goldstyle 5-seed, domain-mix, listed-mix | Wrong gold / extra corpus; keep as old appendix |
| jieba CWS post-hoc | CPU after preds; new gold is character v4 silver, not the 2601 hybrid |
| Old 2601 hybrid / Gold v2 scores | Frozen appendix transfer; do not overwrite |

## Submit / resume

Job **50733** already holds pair `0,1`. Night rest is chained inside `run_repartition_v1_crf_pair.sh` (do not `sbatch` a second job while it runs).

If 50733 dies after some `run_summary.json` files exist:

```bash
cd /home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper
sbatch scripts/repartition_v1.sbatch
```

The pair script skips finished CRF dirs. STL / Qwen skip existing `test_pred.jsonl` / shard raw files.
