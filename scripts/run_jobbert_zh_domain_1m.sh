#!/usr/bin/env bash
# JobBERT-zh domain mix 1M: AI 35% / 应届生 25% / 阿里云 22% / 事业单位 14%.
# MLM 3 epochs then goldstyle v3 CRF seeds 42, 123, 2026.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="${OUT_DIR:-$PAPER/output/jobbert_zh_domain_1m}"
CORPUS="${CORPUS:-$PAPER/data/jobbert_domain_mix_1m_sents.jsonl}"
INIT="${INIT_MODEL:-$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext}"
EPOCHS="${EPOCHS:-3}"
N="${CORPUS_N:-1000000}"
mkdir -p "$OUT"
exec 9>"$OUT/run.lock"
if ! flock -n 9; then
  echo "domain-1M already running (lock $OUT/run.lock); exit" | tee -a "$OUT/run.log"
  exit 0
fi
echo $$ > "$OUT/run.pid"
NGPU=$(echo "${CUDA_VISIBLE_DEVICES:-0}" | awk -F, '{print NF}')
echo "domain-1M start GPU=${CUDA_VISIBLE_DEVICES:-?} nproc=$NGPU corpus=$CORPUS $(date -Is)" | tee -a "$OUT/run.log"

if [[ ! -f "$CORPUS" ]]; then
  echo "[corpus] building $CORPUS n=$N" | tee -a "$OUT/run.log"
  "$PY" "$PAPER/scripts/prepare_jobbert_domain_mix_corpus.py" \
    --n "$N" \
    --out "$CORPUS" \
    --seed 20260824 \
    2>&1 | tee -a "$OUT/run.log"
fi

if [[ ! -f "$OUT/mlm/encoder/config.json" ]]; then
  LAUNCH=("$PY")
  if [[ "$NGPU" -gt 1 ]]; then
    LAUNCH=("$PY" -m torch.distributed.run --standalone --nproc_per_node="$NGPU")
  fi
  "${LAUNCH[@]}" "$PAPER/scripts/train_jobbert_zh_mlm.py" \
    --corpus "$CORPUS" \
    --model_dir "$INIT" \
    --out_dir "$OUT/mlm" \
    --epochs "$EPOCHS" --batch_size 32 --max_len 128 --lr 5e-5 \
    2>&1 | tee -a "$OUT/run.log"
else
  echo "[mlm] encoder already exists, skip MLM $(date -Is)" | tee -a "$OUT/run.log"
fi

run_crf() {
  local seed="$1"
  local dest="$OUT/crf_v3_seed${seed}"
  if [[ -f "$dest/run_summary.json" ]]; then
    echo "[skip] CRF seed=$seed already scored" | tee -a "$OUT/run.log"
    return 0
  fi
  mkdir -p "$dest"
  echo "[crf] seed=$seed $(date -Is)" | tee -a "$OUT/run.log"
  "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed "$seed" \
    --model_dir "$OUT/mlm/encoder" \
    --train "$PAPER/data/train_goldstyle_v3.jsonl" \
    --dev "$PAPER/data/dev_goldstyle_v3.jsonl" \
    --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
    --gold "$PAPER/data/gold_canonical_v2.jsonl" \
    --out_dir "$dest" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    2>&1 | tee -a "$OUT/run.log"
  cp -f "$dest/run_summary.json" "$PAPER/results_snapshots/jobbert_zh_domain_1m__crf_v3_seed${seed}.json"
  if [[ -x "$PAPER/scripts/backup_push_github.sh" ]]; then
    bash "$PAPER/scripts/backup_push_github.sh" "domain-mix 1M CRF snapshot seed ${seed}" || true
  fi
}

run_crf 42
run_crf 123
run_crf 2026

"$PY" "$PAPER/scripts/after_jobbert_domain_1m.py" 2>&1 | tee -a "$OUT/run.log" || true

echo "domain-1M done $(date -Is) exit=$?" | tee -a "$OUT/run.log"
echo "summary: $OUT/crf_v3_seed42/run_summary.json" | tee -a "$OUT/run.log"
