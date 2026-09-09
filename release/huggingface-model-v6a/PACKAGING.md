# Packaging JobBERT-zh v6a (Gold150) for Hugging Face

Local-only guide. Weights must **not** be committed to Git.

Public name: **JobBERT-zh v6a**. Hub id: `AlfredJames/jobbert-zh-v6a`.  
This is an **additional** checkpoint. Do **not** overwrite `AlfredJames/jobbert-zh` (V4, 0.4331).

Paper cell: Gold150 B2 typed exact **0.5536±0.0054** (seeds 42/43/44 sample SD).

---

## 1. Source files (verified 2026-09-09, machine B)

Encoder (byte-identical to `AlfredJames/jobbert-zh`):

`Baseline_Models_Collection/jobbert-zh/`

| File | SHA-256 |
|---|---|
| `model.safetensors` | `ed2130f680d0aa9691d081a516963da252449746ef7e78818050e3039b6ccf3b` |

CRF heads (v6a B2 drop44):

`Chinese_skill_benchmark_Paper/output/silver_plus_phase4_v6_runs/drop44/jobbert3m/b2/`

| Seed | Gold150 exact | SHA-256 of `best.pt` |
|---:|---:|---|
| 42 | 0.5544 | `7bea1f284b666570fd542c1fc7c9f1101840a11be16b4c04cb303047a8df7b7d` |
| 43 | 0.5479 | `275b97da7a94d2d42c3ae0fe8e88c4fe2dec857831e0dc958578cb593abc06d8` |
| 44 | 0.5587 | `3d6d708b8633264aed47911eaeaa317dc052dff1bea34c814165ae42e68cc626` |

`crf/best.pt` on the Hub is a copy of **seed 42** (closest to the mean). Do not upload `last.ckpt`, `test_pred.jsonl`, or `run.log`.

---

## 2. Staging copy

From `/home/guojingli3/chinese-skillspan-benchmark` after the files exist on this host:

```bash
set -euo pipefail
WORK=/home/guojingli3/Chinese-Skillspan-Benchmark
ENC="$WORK/Baseline_Models_Collection/jobbert-zh"
CRF="$WORK/Chinese_skill_benchmark_Paper/output/silver_plus_phase4_v6_runs/drop44/jobbert3m/b2"
STAGING="$(pwd)/release/huggingface-model-v6a/staging"

rm -rf "$STAGING"
mkdir -p "$STAGING/crf/seed42" "$STAGING/crf/seed43" "$STAGING/crf/seed44"

cp README.md "$STAGING/README.md" 2>/dev/null || cp release/huggingface-model-v6a/README.md "$STAGING/README.md"
cp "$ENC/config.json" "$STAGING/config.json"
cp "$ENC/model.safetensors" "$STAGING/model.safetensors"
cp "$ENC/tokenizer.json" "$STAGING/tokenizer.json"
cp "$ENC/tokenizer_config.json" "$STAGING/tokenizer_config.json"
cp "$CRF/seed42/best.pt" "$STAGING/crf/seed42/best.pt"
cp "$CRF/seed43/best.pt" "$STAGING/crf/seed43/best.pt"
cp "$CRF/seed44/best.pt" "$STAGING/crf/seed44/best.pt"
cp "$CRF/seed42/best.pt" "$STAGING/crf/best.pt"
cp release/huggingface-model-v6a/crf/README.md "$STAGING/crf/README.md"
```

---

## 3. Upload (must be logged in as a user who can write `AlfredJames/*`)

```bash
hf auth whoami
hf repo create AlfredJames/jobbert-zh-v6a --repo-type model --exist-ok
hf upload AlfredJames/jobbert-zh-v6a \
  release/huggingface-model-v6a/staging \
  . \
  --repo-type model \
  --commit-message "Add JobBERT-zh v6a Gold150 B2 CRF heads (0.5536±0.0054)."
```

Then confirm the repo is **public**. Do not replace files under `AlfredJames/jobbert-zh`.
