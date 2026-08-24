#!/usr/bin/env bash
# CPU-only: extract listed yearly CSVs + build listed-mix 1M corpus.
# Safe to run while another Slurm job holds the GPU slot.
set -euo pipefail
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="${OUT_DIR:-$PAPER/output/jobbert_zh_listed_1m}"
CORPUS="${CORPUS:-$PAPER/data/jobbert_listed_mix_1m_sents.jsonl}"
N="${CORPUS_N:-1000000}"
YEARLY="$PAPER/chineseskillspan-jobert-pretrain/上市公司招聘大数据2014-2026.3/分年份保存数据"
mkdir -p "$OUT"
echo $$ > "$OUT/corpus_prep.pid"
cleanup() { rm -f "$OUT/corpus_prep.pid"; }
trap cleanup EXIT
echo "[corpus-prep] start $(date -Is) pid=$$" | tee -a "$OUT/corpus_prep.log"

if [[ ! -f "$YEARLY/上市公司招聘数据2026.csv" ]]; then
  echo "[corpus-prep] extracting yearly CSVs" | tee -a "$OUT/corpus_prep.log"
  bash "$PAPER/scripts/extract_listed_yearly_csvs.sh" 2>&1 | tee -a "$OUT/corpus_prep.log"
fi

if [[ ! -f "$CORPUS" ]]; then
  echo "[corpus-prep] building $CORPUS n=$N" | tee -a "$OUT/corpus_prep.log"
  "$PY" "$PAPER/scripts/prepare_jobbert_listed_mix_corpus.py" \
    --n "$N" \
    --out "$CORPUS" \
    --seed 20260824 \
    2>&1 | tee -a "$OUT/corpus_prep.log"
fi

echo "[corpus-prep] done $(date -Is) corpus=$CORPUS" | tee -a "$OUT/corpus_prep.log"
