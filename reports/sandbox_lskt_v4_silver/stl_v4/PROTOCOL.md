# STL L / K / S / T (appendix backup)

**Not the main table.** Joint JobBERT-zh 1M v4 typed exact **0.4272** stays the reported encoder row until the user moves a better STL number.

Does **not** overwrite `gold_canonical_v2.jsonl`, `train_lskt_v4_silver.jsonl`, or `output/jobbert_zh_1m/crf_lskt_v4_silver_seed42`.

## What runs

| | Joint (already scored) | STL (this job) |
|---|---|---|
| Encoder | JobBERT-zh 1M MLM | same frozen encoder |
| Train / dev | `train_lskt_v4_silver` / `dev_lskt_v4_silver` | same, other types → O |
| CRF tags | 9 (`O` + B/I for L,K,S,T) | 3 (`O`, `B-X`, `I-X`) |
| Seed / hparams | 42, 6 ep, patience 2, bs 16, lr 2e-5 | same |
| Test gold | V4 hybrid + jieba | same |
| Scorer | `cnss-lskt-1.2.0` | same |

Order: S → K → T → L. Combined = greedy non-overlap union (longer span first, then S≻K≻T≻L). Gold is flat (overlap 0), so overlapping STL heads drop one span.

**Submit only via Slurm** (`sbatch scripts/stl_lskt_v4.sbatch`). The 2026-08-27 `nohup` run was **Killed** mid STL-S epoch 3; resume from `S/last.ckpt` (epoch 2). Do not `nohup` this trainer. Account `MaxJobs=1`; no `--gres=gpu`.

## Paper rule

- CSV written 2026-08-27 23:33: combined typed exact **0.4100** vs joint **0.4272**. **Stay in appendix**; do not move to main unless the user says so.
- Do **not** mix with SkillSpan nested SKILL/KNOWLEDGE STL/MTL F1.
- Do **not** write Gold v2 trainer `typed_exact` (STL predicts one type; that micro is not comparable to 0.1224).
