# Wake / VPN-drop resume (2026-08-23 04:03 +08)

This window is Chinese-SkillSpan only. Do not edit `access_paper/`. Do not write F1 into the PDF or `confirmed-results.md`.

## What survives lock + GlobalProtect drop

| Piece | Needs VPN / unlocked laptop? | Status at 04:03 |
|---|---|---|
| v1 GPU smoke (`setsid`, PPID 1, GPU 3) | **No** — local GPU, `TRANSFORMERS_OFFLINE=1` | running pid **2766720** / python **2766726**, epoch 1 step ~1000 |
| overnight waiter pid **2770903** | **No** — polls local files, then local train | waiting for `run_summary.json` |
| Cursor 45-min agent check | **Yes** — dies if VPN / SSH / Cursor drops | best-effort only |
| v1/v2 jsonl, scripts, IAA worksheet | already on disk | done |

If GlobalProtect asks for a phone code, **do not treat that as a failed experiment**. Reconnect, then run the checklist below. Server processes usually keep going while the laptop is locked, as long as **the server itself** does not sleep.

## Already finished (no more prep needed)

- Gold-style v1 train/dev: `Chinese_skill_benchmark_Paper/data/train_goldstyle_v1.jsonl`
- Gold-style tight v2 train/dev: `.../train_goldstyle_v2.jsonl` (mean span ~11.4 tokens; 80 human rows locked)
- Scorer + train script + v1/v2 smoke wrappers
- After-smoke report script: `scripts/after_goldstyle_smoke.py`
- IAA-300 worksheet only: `reports/iaa300/` (no dual labels yet)
- 80-item human lock: `reports/gold_style_relabel/sample80_final.json`

## When you wake (or after VPN reconnect)

```bash
# A. still running?
ps -p 2766720,2766726,2770903 -o pid,ppid,etime,cmd
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv

# B. v1 finished?
cat Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/run_summary.json
tail -n 40 Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/overnight.log
cat Chinese_skill_benchmark_Paper/reports/gold_style_relabel/goldstyle_smoke_result.md

# C. v2 started after low F1?
ls Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42/run_summary.json
```

Interpretation (do not copy into the paper):

- Compare official **typed exact F1** to silver smoke **0.012**
- `alignment_ok` must be true
- If typed F1 ≥ 0.05 → consider 3-seed **on goldstyle labels**, not silver; ask before launching
- If typed F1 still ~0.01 → v2 tight smoke is the next 1-seed; do not 3-seed

## If v1 died (no `run_summary.json`)

```bash
OUT=Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42
nvidia-smi --query-gpu=index,memory.used --format=csv
# pick a free GPU; if last.ckpt exists, resume instead of full restart
setsid env CUDA_VISIBLE_DEVICES=<gpu> OUT_DIR="$OUT" \
  bash Chinese_skill_benchmark_Paper/scripts/run_cn_roberta_crf_goldstyle_smoke.sh \
  < /dev/null > "$OUT/nohup.out" 2>&1 &
```

## If v1 finished but waiter did not start v2 (F1 < 0.05)

v2 jsonl is already written. Only this is missing:

```bash
setsid env CUDA_VISIBLE_DEVICES=<gpu> \
  bash Chinese_skill_benchmark_Paper/scripts/run_cn_roberta_crf_goldstyle_v2_smoke.sh \
  < /dev/null > Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42/nohup.out 2>&1 &
```

## Do not do until you are back

- 3-seed on silver `train.json`
- overwrite corpus `train.json` or Gold v2
- IAA dual annotation
- paper number updates
- depend on the Cursor 45-min check
