#!/usr/bin/env bash
# Pack only what the vanilla base vs large V4 CRF seed-42 test needs.
# Default: code + gold/silver (small). Pass --with-weights to include ~2.5G encoders.
# Does not pack Access, DAPT, output/, LoRA, or Gold-overwriting dumps.
set -euo pipefail
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
STAMP=$(date +%Y%m%d)
OUT="${PACK_OUT:-$PAPER/output/vanilla_wwm_v4/vanilla_wwm_v4_pack_${STAMP}.tgz}"
WITH_WEIGHTS=0
if [[ "${1:-}" == "--with-weights" ]]; then
  WITH_WEIGHTS=1
fi
mkdir -p "$(dirname "$OUT")"
LIST=$(mktemp)
trap 'rm -f "$LIST"' EXIT
{
  echo "Chinese_skill_benchmark_Paper/scripts/train_cn_roberta_crf.py"
  echo "Chinese_skill_benchmark_Paper/scripts/eval_one_hybrid_cws.py"
  echo "Chinese_skill_benchmark_Paper/scripts/cws_snap.py"
  echo "Chinese_skill_benchmark_Paper/scripts/rewrite_train_goldstyle_v3.py"
  echo "Chinese_skill_benchmark_Paper/scripts/diag_span_charlen.py"
  echo "Chinese_skill_benchmark_Paper/scripts/run_vanilla_wwm_v4_crf.sh"
  echo "Chinese_skill_benchmark_Paper/scripts/vanilla_wwm_v4.sbatch"
  echo "Chinese_skill_benchmark_Paper/scripts/download_cn_roberta_wwm_ext_large.py"
  echo "Chinese_skill_benchmark_Paper/scripts/wait_idle_gpu_pair.sh"
  echo "Chinese_skill_benchmark_Paper/scripts/pack_vanilla_wwm_v4_for_new_host.sh"
  echo "Chinese_skill_benchmark_Paper/scorer/score_lskt.py"
  echo "Chinese_skill_benchmark_Paper/notes/vanilla_large_v4.md"
  echo "Chinese_skill_benchmark_Paper/notes/PROMPT_NEW_WINDOW.md"
  echo "Chinese_skill_benchmark_Paper/notes/confirmed-results.md"
  echo "Chinese_skill_benchmark_Paper/notes/not-for-paper.md"
  echo "Chinese_skill_benchmark_Paper/data/train_lskt_v4_silver.jsonl"
  echo "Chinese_skill_benchmark_Paper/data/dev_lskt_v4_silver.jsonl"
  echo "Chinese_skill_benchmark_Paper/data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
  echo "Chinese_skill_benchmark_Paper/data/gold_canonical_v2.jsonl"
  echo "Chinese_skill_benchmark_Paper/data/cws_userdict.txt"
  echo "Chinese_skill_benchmark_Paper/data/cws_userdict_words.txt"
  echo "data/annotated/processed/chinese_skillspan/test.json"
  echo "Baseline_Models_Collection/pytorch-crf/torchcrf/__init__.py"
  echo "Baseline_Models_Collection/pytorch-crf/setup.py"
  if [[ "$WITH_WEIGHTS" -eq 1 ]]; then
    echo "Baseline_Models_Collection/chinese-roberta-wwm-ext/"
    echo "Baseline_Models_Collection/chinese-roberta-wwm-ext-large/"
  fi
} > "$LIST"
tar -C "$ROOT" -czf "$OUT" --files-from="$LIST"
echo "$OUT"
du -h "$OUT"
