#!/usr/bin/env bash
# One chain, at most two GPUs. Respect CUDA_VISIBLE_DEVICES. Do not kill other jobs.
set -euo pipefail
WORK=/home/guojingli3/Chinese-Skillspan-Benchmark
PAPER="$WORK/Chinese_skill_benchmark_Paper"
EXT="$PAPER/output/silver_plus_extensions"
DATA="$EXT/data/v6a_nocross_20260908"
QWEN=/home/guojingli3/IEEE_Access_project/models/Qwen2.5-14B-Instruct
JB="$WORK/Baseline_Models_Collection/jobbert-zh"
export SCESC_ROOT="$WORK"
export PYTHON=/home/guojingli3/miniconda3/envs/adasparse/bin/python3
export PYTHONPATH="$WORK/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
mkdir -p "$EXT/logs" "$EXT/qwen14b_b2" "$EXT/hem_jobbert3m"
LOG="$EXT/RESOURCE_LOG.jsonl"
echo "[host] $(hostname) date=$(date -Is) slurm=${SLURM_JOB_ID:-na} CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-unset}" | tee -a "$EXT/run.log"
nvidia-smi --query-gpu=index,uuid,name,memory.total,memory.used,utilization.gpu --format=csv | tee -a "$EXT/run.log"

IFS=',' read -r -a GPUS <<< "${CUDA_VISIBLE_DEVICES:-}"
if [[ ${#GPUS[@]} -lt 1 ]]; then
  echo "CUDA_VISIBLE_DEVICES empty; refusing to pick physical IDs" | tee -a "$EXT/run.log"
  exit 2
fi
G0="${GPUS[0]}"
G1="${GPUS[1]:-${GPUS[0]}}"

log_event() {
  local phase="$1" extra="${2:-}"
  echo "{\"ts\":\"$(date -Is)\",\"job\":\"${SLURM_JOB_ID:-na}\",\"phase\":\"$phase\",\"cuda\":\"${CUDA_VISIBLE_DEVICES:-}\",\"extra\":\"$extra\"}" >> "$LOG"
}

# KNN index leftover from a superseded plan is not built or used this round.

run_qwen_seed() {
  local seed="$1" gpu="$2"
  local out="$EXT/qwen14b_b2/seed${seed}"
  mkdir -p "$out"
  if [[ -f "$out/selected_checkpoint.json" && -f "$out/adapter/adapter_config.json" ]]; then
    echo "SKIP qwen train seed${seed}"
    return 0
  fi
  log_event "qwen_train_start" "seed=${seed} gpu=${gpu}"
  CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON" "$PAPER/scripts/train_qwen_ext_sft.py" \
    --model_dir "$QWEN" \
    --train "$DATA/train_b2.jsonl" \
    --dev "$DATA/dev_b2.jsonl" \
    --out_dir "$out" \
    --seed "$seed" \
    > "$out/train.log" 2>&1
  log_event "qwen_train_end" "seed=${seed} exit=$?"
}

eval_qwen_seed() {
  local seed="$1" gpu="$2"
  local out="$EXT/qwen14b_b2/seed${seed}"
  local gout="$out/gold150"
  mkdir -p "$gout"
  if [[ -f "$gout/score.json" || -f "$gout/score_A.json" ]]; then
    echo "SKIP qwen gold seed${seed}"
    return 0
  fi
  log_event "qwen_gold_start" "seed=${seed}"
  CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON" "$PAPER/scripts/infer_qwen_ext_sft.py" \
    --model_dir "$QWEN" \
    --adapter_dir "$out/adapter" \
    --queries "$DATA/gold150_eval.jsonl" \
    --out_dir "$gout" \
    > "$gout/infer.log" 2>&1
  CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON" "$PAPER/scripts/eval_gold150_ext.py" \
    --gold_eval "$DATA/gold150_eval.jsonl" \
    --pred "$gout/pred.jsonl" \
    --out "$gout/score.json"
  cp -f "$gout/score.json" "$gout/score_A.json"
  log_event "qwen_gold_end" "seed=${seed}"
}

# 42+43 parallel, then 44
run_qwen_seed 42 "$G0" &
p42=$!
if [[ "$G0" != "$G1" ]]; then
  run_qwen_seed 43 "$G1" &
  p43=$!
  wait "$p42"
  wait "$p43"
else
  wait "$p42"
  run_qwen_seed 43 "$G0"
fi
run_qwen_seed 44 "$G0"

eval_qwen_seed 42 "$G0" &
pe42=$!
if [[ "$G0" != "$G1" ]]; then
  eval_qwen_seed 43 "$G1" &
  pe43=$!
  wait "$pe42"
  wait "$pe43"
else
  wait "$pe42"
  eval_qwen_seed 43 "$G0"
fi
eval_qwen_seed 44 "$G0"

# --- HEM ---
HEM_DATA="$EXT/hem_data"
if [[ ! -f "$EXT/HEM_SAMPLING_MANIFEST.json" ]]; then
  "$PYTHON" "$PAPER/scripts/sample_hem_ext.py" \
    --train "$DATA/train_b2.jsonl" \
    --out_dir "$HEM_DATA"
  cp -f "$HEM_DATA/HEM_SAMPLING_MANIFEST.json" "$EXT/HEM_SAMPLING_MANIFEST.json"
  cp -f "$HEM_DATA/HEM_BALANCE_REPORT.md" "$EXT/HEM_BALANCE_REPORT.md"
  cp -f "$HEM_DATA/HEM_CONFIG.json" "$EXT/HEM_CONFIG.json"
fi
N=$(python3 -c "import json; print(json.load(open('$EXT/HEM_CONFIG.json'))['n'])")
A=$(python3 -c "import json; print(json.load(open('$EXT/HEM_CONFIG.json'))['A_base'])")
run_hem() {
  local cond="$1" seed="$2" gpu="$3"
  local name="${cond}"
  local train="$HEM_DATA/train_B2_A${A}_${cond}.jsonl"
  # cond is H_n / E_n / M_n
  local out="$EXT/hem_jobbert3m/${cond}/seed${seed}"
  mkdir -p "$out"
  if [[ -f "$out/best.pt" && -f "$out/score_gold150.json" ]]; then
    echo "SKIP hem ${cond} seed${seed}"
    return 0
  fi
  log_event "hem_start" "${cond} seed=${seed}"
  if [[ ! -f "$out/best.pt" ]]; then
    CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON" "$PAPER/scripts/train_jobbert_ext.py" \
      --model_dir "$JB" \
      --train "$train" \
      --dev "$DATA/dev_b2.jsonl" \
      --out_dir "$out" \
      --seed "$seed" \
      > "$out/train.log" 2>&1
  fi
  CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON" "$PAPER/scripts/infer_jobbert_phase1.py" \
    --model_dir "$JB" \
    --ckpt "$out/best.pt" \
    --input "$DATA/gold150_eval.jsonl" \
    --out "$out/gold150_pred.jsonl"
  CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON" "$PAPER/scripts/eval_gold150_ext.py" \
    --gold_eval "$DATA/gold150_eval.jsonl" \
    --pred "$out/gold150_pred.jsonl" \
    --out "$out/score_gold150.json"
  log_event "hem_end" "${cond} seed=${seed}"
}

CONDS=()
while IFS= read -r line; do
  [[ -n "$line" ]] && CONDS+=("$line")
done < <("$PYTHON" -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1]))["conditions"]))' "$EXT/HEM_CONFIG.json")
if [[ ${#CONDS[@]} -lt 1 ]]; then
  echo "HEM conditions empty" | tee -a "$EXT/run.log"
  exit 2
fi
jobs=()
for cond in "${CONDS[@]}"; do
  for seed in 42 43 44; do
    jobs+=("${cond}:${seed}")
  done
done
i=0
while [[ $i -lt ${#jobs[@]} ]]; do
  c1="${jobs[$i]%%:*}"; s1="${jobs[$i]##*:}"
  run_hem "$c1" "$s1" "$G0" &
  p1=$!
  i=$((i + 1))
  if [[ $i -lt ${#jobs[@]} && "$G0" != "$G1" ]]; then
    c2="${jobs[$i]%%:*}"; s2="${jobs[$i]##*:}"
    run_hem "$c2" "$s2" "$G1" &
    p2=$!
    i=$((i + 1))
    wait "$p1"
    wait "$p2"
  else
    wait "$p1"
  fi
done

"$PYTHON" "$PAPER/scripts/collect_extension_results.py"
echo "[chain_done] $(date -Is)" | tee -a "$EXT/run.log"
