#!/usr/bin/env bash
# Local fallback when SLURM MaxJobs=1 blocks sbatch.
# Build corpus if needed, wait for an idle GPU (never stack), then MLM+CRF.
set -euo pipefail
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="$PAPER/output/jobbert_zh_domain_1m"
CORPUS="$PAPER/data/jobbert_domain_mix_1m_sents.jsonl"
META="$PAPER/data/jobbert_domain_mix_1m_sents.meta.json"
mkdir -p "$OUT"
echo $$ > "$OUT/wait_then_run.pid"
echo "[wait] domain-1M waiter start $(date -Is)" | tee -a "$OUT/wait.log"

if [[ ! -f "$META" || ! -s "$CORPUS" ]]; then
  echo "[wait] corpus missing; waiting for corpus_prep $(date -Is)" | tee -a "$OUT/wait.log"
  for _ in $(seq 1 240); do
    if [[ -f "$META" && -s "$CORPUS" ]]; then
      break
    fi
    sleep 15
  done
fi
if [[ ! -f "$META" || ! -s "$CORPUS" ]]; then
  echo "[wait] building corpus now $(date -Is)" | tee -a "$OUT/wait.log"
  "$PY" "$PAPER/scripts/prepare_jobbert_domain_mix_corpus.py" \
    --n 1000000 --out "$CORPUS" --seed 20260824 \
    2>&1 | tee -a "$OUT/wait.log"
fi
echo "[wait] corpus ready n=$(wc -l < "$CORPUS") $(date -Is)" | tee -a "$OUT/wait.log"

# Wait indefinitely for idle pair, then one idle card. Never stack on hyb/3-seed.
GPU=$(USED_MAX_MIB=4096 PAIR_WAIT_SEC=600 ALLOW_SINGLE=1 \
  bash "$PAPER/scripts/wait_idle_gpu_pair.sh" | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
export OUT_DIR="$OUT"
export CORPUS
export CORPUS_N=1000000
export INIT_MODEL="$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext"
export EPOCHS=3
echo "[wait] launching domain-1M on GPU=$GPU $(date -Is)" | tee -a "$OUT/wait.log"
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUT/wait.log"
bash "$PAPER/scripts/run_jobbert_zh_domain_1m.sh"
echo "[wait] handed-off runner exit=$? $(date -Is)" | tee -a "$OUT/wait.log"
