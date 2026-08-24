# Overnight commands (2026-08-23)

Do **not** write F1 into `confirmed-results.md` or the PDF. Do **not** start 3-seed on silver. Do **not** train on Gold v2.

VPN / lock: Cursor 45-min check is best-effort. Server `setsid` jobs do not need GlobalProtect. Wake file: `WAKE_RESUME.md`.

## 1. Current v1 smoke (already running, GPU 3)

```bash
# status
ps -p 2766720,2766726 -o pid,ppid,etime,cmd
tail -n 30 Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/smoke.log
cat Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/run_summary.json
```

## 2. After v1 finishes (auto-run by wait_and_continue_goldstyle.sh)

```bash
python3 Chinese_skill_benchmark_Paper/scripts/after_goldstyle_smoke.py
cat Chinese_skill_benchmark_Paper/reports/gold_style_relabel/goldstyle_smoke_result.md
```

Decision baked into the waiter:

- official typed F1 **≥ 0.05** → stop; leave 3-seed for you
- official typed F1 **< 0.05** → rewrite tight v2 + 1-seed smoke (emptiest GPU)

## 3. Manual relaunch if v1 died (SIGKILL / no run_summary)

```bash
OUT=Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42
# pick empty GPU
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv
setsid env CUDA_VISIBLE_DEVICES=<gpu> OUT_DIR="$OUT" \
  bash Chinese_skill_benchmark_Paper/scripts/run_cn_roberta_crf_goldstyle_smoke.sh \
  < /dev/null > "$OUT/nohup.out" 2>&1 &
```

If `last.ckpt` exists, prefer `--resume` on `train_cn_roberta_crf.py` instead of a full restart.

## 4. Manual v2 (only if waiter did not start it)

```bash
python3 Chinese_skill_benchmark_Paper/scripts/rewrite_train_goldstyle.py --tight \
  --out_train Chinese_skill_benchmark_Paper/data/train_goldstyle_v2.jsonl \
  --out_dev Chinese_skill_benchmark_Paper/data/dev_goldstyle_v2.jsonl \
  --out_meta Chinese_skill_benchmark_Paper/reports/gold_style_relabel/goldstyle_v2_meta.json
setsid env CUDA_VISIBLE_DEVICES=<gpu> \
  bash Chinese_skill_benchmark_Paper/scripts/run_cn_roberta_crf_goldstyle_v2_smoke.sh \
  < /dev/null > Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42/nohup.out 2>&1 &
```

## 5. Overnight waiter log

```bash
tail -n 50 Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/overnight.log
```

## 6. Do not run tonight

- 3-seed on silver `train.json`
- overwrite corpus `train.json` / Gold v2
- IAA dual annotation (worksheet only is ready under `reports/iaa300/`)
- paper number updates
