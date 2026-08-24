#!/bin/bash
# Pick idle GPUs for one Slurm job. Lab pairs only: 0+1 or 2+3.
# Do not use --gres=gpu: LocalQ can pin busy cards.
# Idle = memory.used <= USED_MAX_MIB. Never stack on a busy card.
# Wait PAIR_WAIT_SEC for an idle pair; then one idle card if ALLOW_SINGLE=1.
# Last stdout line is the CUDA_VISIBLE_DEVICES value.
set -euo pipefail
USED_MAX_MIB="${USED_MAX_MIB:-4096}"
PAIR_WAIT_SEC="${PAIR_WAIT_SEC:-300}"
ALLOW_SINGLE="${ALLOW_SINGLE:-1}"
POLL_SEC="${POLL_SEC:-15}"

is_idle() {
  local used
  used=$(nvidia-smi -i "$1" --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | tr -d ' ')
  [[ -n "${used:-}" && "$used" -le "$USED_MAX_MIB" ]]
}

log_state() {
  echo "[gpu-wait] $(date -Is) want pair 0+1 or 2+3, used<=${USED_MAX_MIB}MiB" >&2
  nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv,noheader \
    | sed 's/^/[gpu-wait] /' >&2
}

pick_pair() {
  local has0=0 has1=0 has2=0 has3=0 i
  for i in 0 1 2 3; do
    if is_idle "$i"; then
      case "$i" in
        0) has0=1 ;;
        1) has1=1 ;;
        2) has2=1 ;;
        3) has3=1 ;;
      esac
    fi
  done
  if [[ "$has0" -eq 1 && "$has1" -eq 1 ]]; then
    echo "0,1"
    return 0
  fi
  if [[ "$has2" -eq 1 && "$has3" -eq 1 ]]; then
    echo "2,3"
    return 0
  fi
  return 1
}

pick_one() {
  local i
  for i in 0 1 2 3; do
    if is_idle "$i"; then
      echo "$i"
      return 0
    fi
  done
  return 1
}

deadline=$((SECONDS + PAIR_WAIT_SEC))
while true; do
  log_state
  if pair=$(pick_pair); then
    echo "[gpu-wait] idle pair $pair" >&2
    echo "$pair"
    exit 0
  fi
  if [[ "$SECONDS" -ge "$deadline" ]]; then
    break
  fi
  sleep "$POLL_SEC"
done

if [[ "$ALLOW_SINGLE" != "1" ]]; then
  echo "[gpu-wait] no idle pair and ALLOW_SINGLE=0" >&2
  exit 2
fi

echo "[gpu-wait] no idle pair in ${PAIR_WAIT_SEC}s; waiting for one idle card" >&2
while true; do
  log_state
  if one=$(pick_one); then
    echo "[gpu-wait] one idle GPU $one" >&2
    echo "$one"
    exit 0
  fi
  sleep "$POLL_SEC"
done
