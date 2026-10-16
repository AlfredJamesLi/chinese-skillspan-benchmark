#!/usr/bin/env bash
# Train v6a (drop44) + v6b (cleandev), two GPUs at a time. Skip finished run_config.json.
set -euo pipefail
WORK=/home/guojingli3/Chinese-Skillspan-Benchmark
export SCESC_ROOT="$WORK"
export PYTHON=/home/guojingli3/miniconda3/envs/adasparse/bin/python3
export PYTHONPATH="$WORK/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
JB="$WORK/Baseline_Models_Collection/jobbert-zh"
TRAINER="$WORK/Chinese_skill_benchmark_Paper/scripts/train_jobbert_phase1.py"
INFER="$WORK/Chinese_skill_benchmark_Paper/scripts/infer_jobbert_phase1.py"
EVAL="$WORK/Chinese_skill_benchmark_Paper/scripts/eval_gold150_phase1.py"
RUNS="$WORK/Chinese_skill_benchmark_Paper/output/silver_plus_phase4_v6_runs"
A="$WORK/Chinese_skill_benchmark_Paper/output/silver_plus_v6a_drop44_train_20260908"
B="$WORK/Chinese_skill_benchmark_Paper/output/silver_plus_v6b_clean_dev_20260908"

IFS=',' read -r G0 G1 <<< "${CUDA_VISIBLE_DEVICES:-2,3}"
G0="${G0:-2}"
G1="${G1:-${G0}}"
echo "[phase4] host=$(hostname) CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-} pair=$G0,$G1 date=$(date -Is)"

jobs=()
for tag_data in "drop44|$A" "cleandev|$B"; do
  tag="${tag_data%%|*}"
  data="${tag_data##*|}"
  for cond in b1 b2; do
    for seed in 42 43 44; do
      jobs+=("$tag|$data|$cond|$seed")
    done
  done
done

run_one() {
  local spec="$1" gpu="$2"
  local tag="${spec%%|*}"
  local rest="${spec#*|}"
  local data="${rest%%|*}"
  rest="${rest#*|}"
  local cond="${rest%%|*}"
  local seed="${rest##*|}"
  local out="$RUNS/$tag/jobbert3m/${cond}/seed${seed}"
  mkdir -p "$out"
  if [[ -f "$out/run_config.json" && -f "$out/best.pt" ]]; then
    echo "SKIP $tag $cond $seed"
    return 0
  fi
  echo "START $tag $cond $seed gpu$gpu"
  CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON" "$TRAINER" \
    --model_dir "$JB" --init_pt "$JB/crf/best.pt" \
    --train "$data/train_${cond}.jsonl" --dev "$data/dev_${cond}.jsonl" \
    --out_dir "$out" --seed "$seed" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    > "$out/train.log" 2>&1
  echo "DONE $tag $cond $seed exit:$?"
}

pending=()
for spec in "${jobs[@]}"; do
  tag="${spec%%|*}"
  rest="${spec#*|}"
  data="${rest%%|*}"
  rest="${rest#*|}"
  cond="${rest%%|*}"
  seed="${rest##*|}"
  out="$RUNS/$tag/jobbert3m/${cond}/seed${seed}"
  if [[ -f "$out/run_config.json" && -f "$out/best.pt" ]]; then
    echo "SKIP $tag $cond $seed"
  else
    pending+=("$spec")
  fi
done

i=0
n=${#pending[@]}
while [[ $i -lt $n ]]; do
  spec0="${pending[$i]}"
  run_one "$spec0" "$G0" &
  pids=($!)
  i=$((i + 1))
  if [[ $i -lt $n ]]; then
    spec1="${pending[$i]}"
    run_one "$spec1" "$G1" &
    pids+=($!)
    i=$((i + 1))
  fi
  for pid in "${pids[@]}"; do
    wait "$pid"
  done
done

echo "[phase4] train done; Gold150 eval"
for spec in "${jobs[@]}"; do
  tag="${spec%%|*}"
  rest="${spec#*|}"
  data="${rest%%|*}"
  rest="${rest#*|}"
  cond="${rest%%|*}"
  seed="${rest##*|}"
  out="$RUNS/$tag/jobbert3m/${cond}/seed${seed}"
  if [[ ! -f "$out/best.pt" ]]; then
    echo "MISSING ckpt $out"
    continue
  fi
  CUDA_VISIBLE_DEVICES="$G0" "$PYTHON" "$INFER" \
    --model_dir "$JB" --ckpt "$out/best.pt" \
    --input "$data/gold150_eval.jsonl" \
    --out "$out/gold150_pred.jsonl" \
    > "$out/infer.log" 2>&1
  "$PYTHON" "$EVAL" \
    --gold "$data/gold150_eval.jsonl" \
    --pred "$out/gold150_pred.jsonl" \
    --out "$out/gold150_score.json"
  echo "SCORED $tag $cond $seed"
done
echo V6_SLURM_ALL_DONE
