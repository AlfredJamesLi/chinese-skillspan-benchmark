#!/usr/bin/env bash
# Extract yearly CSVs from 分年份保存数据.rar (skip .dta). Run once before corpus build.
set -euo pipefail
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PRE="$ROOT/Chinese_skill_benchmark_Paper/chineseskillspan-jobert-pretrain"
RAR="$PRE/上市公司招聘大数据2014-2026.3/分年份保存数据.rar"
OUT="$PRE/上市公司招聘大数据2014-2026.3/分年份保存数据"
mkdir -p "$OUT"
if [[ ! -f "$RAR" ]]; then
  echo "Missing $RAR" >&2
  exit 1
fi
for y in 2014 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026; do
  f="上市公司招聘数据${y}.csv"
  if [[ -f "$OUT/$f" ]]; then
    echo "skip $f (exists)"
    continue
  fi
  echo "extract $f ..."
  unrar x -o+ "$RAR" "$f" "$OUT/" >/dev/null
done
echo "done -> $OUT"
ls -lh "$OUT"/*.csv 2>/dev/null | awk '{print $5, $9}'
