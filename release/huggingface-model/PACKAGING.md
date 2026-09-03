# Packaging Chinese JobBERT for Hugging Face

Local-only guide. This file does **not** create a Hugging Face repository and does **not** upload weights.

Public name: **Chinese JobBERT**. Laboratory aliases: JobBERT-zh / 3M v4 (`encoder_ckpt65000` + V4 CRF).

Do not upload until:

1. A Hugging Face repository id is chosen (`[TODO: HF_REPO_ID]`, for example `<user-or-org>/chinese-jobbert`).
2. `huggingface-cli` / `hf auth whoami` reports a logged-in account.
3. The base-model licence (`hfl/chinese-roberta-wwm-ext`) and job-advertisement training-text rights are confirmed.
4. The Model Card licence field is no longer an unverified guess. The card currently uses `license: other`.

This workspace check (2026-09-04): `huggingface-cli whoami` → **Not logged in**. Upload cannot run from this machine until you `huggingface-cli login` (or `hf auth login`).

---

## 1. Source files (verified on this host)

Run these commands from the paper repository root:

`Chinese_skill_benchmark_Paper/`

| Role | Source | Bytes | SHA-256 |
|---|---|---:|---|
| Encoder config | `output/jobbert_zh_3m/mlm/encoder_ckpt65000/config.json` | 884 | `34a08e0f1ad5d44d696b3a42535f735667148fe5950fcea6cb90d9213e8645bc` |
| Encoder weights | `output/jobbert_zh_3m/mlm/encoder_ckpt65000/model.safetensors` | 406,730,376 | `ed2130f680d0aa9691d081a516963da252449746ef7e78818050e3039b6ccf3b` |
| Tokenizer | `output/jobbert_zh_3m/mlm/encoder_ckpt65000/tokenizer.json` | 439,125 | `48cea5d44424912a6fd1ea647bf4fe50b55ab8b1e5879c3275f80e339e8fae26` |
| Tokenizer config | `output/jobbert_zh_3m/mlm/encoder_ckpt65000/tokenizer_config.json` | 350 | `a690ace137dc901c4c2025eddc805e5587d0ec8ee52dce5c3436ec88cb40c84f` |
| CRF head | `output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/best.pt` | 409,169,002 | `d98814cb954036f885e1247c2c50c66adbc5a280750f0228bfc3df077f2fc98c` |
| Model card | `release/huggingface-model/README.md` | — | see `release/zenodo/RELEASE_MANIFEST.md` |
| CRF note | `release/huggingface-model/crf/README.md` | — | shipped with this pack |

`config.json` reports `architectures: ["BertModel"]`, `hidden_size` 768, `num_hidden_layers` 12, `vocab_size` 21128, `transformers_version` 5.2.0. There is no `vocab.txt` in the encoder export; `tokenizer.json` is the tokenizer file.

`export_meta.json` only records a laboratory path and **must not** be uploaded.

---

## 2. Files that must not be copied

| Path | Reason |
|---|---|
| `encoder_ckpt65000/export_meta.json` | Absolute laboratory path |
| `crf_lskt_v4_silver_seed42/last.ckpt` | ~1.2 GB optimiser state |
| `run.log`, `run.pid`, `launch.out` | Logs / PID |
| `test_pred.jsonl`, `test_pred_cws.jsonl` | Contain job-advertisement sentences |
| `score_official.json`, `sop_eval.json`, `history.json` | Local eval dumps; scores live in `tables/` |

---

## 3. Exact copy commands

```bash
# From Chinese_skill_benchmark_Paper/
set -euo pipefail
ROOT="$(pwd)"
ENC="$ROOT/output/jobbert_zh_3m/mlm/encoder_ckpt65000"
CRF="$ROOT/output/jobbert_zh_3m/crf_lskt_v4_silver_seed42"
STAGING="$ROOT/release/huggingface-model/staging"

test -f "$ENC/config.json"
test -f "$ENC/model.safetensors"
test -f "$ENC/tokenizer.json"
test -f "$ENC/tokenizer_config.json"
test -f "$CRF/best.pt"

rm -rf "$STAGING"
mkdir -p "$STAGING/crf"

cp -v "$ROOT/release/huggingface-model/README.md" "$STAGING/README.md"
cp -v "$ENC/config.json" "$STAGING/config.json"
cp -v "$ENC/model.safetensors" "$STAGING/model.safetensors"
cp -v "$ENC/tokenizer.json" "$STAGING/tokenizer.json"
cp -v "$ENC/tokenizer_config.json" "$STAGING/tokenizer_config.json"
cp -v "$CRF/best.pt" "$STAGING/crf/best.pt"
cp -v "$ROOT/release/huggingface-model/crf/README.md" "$STAGING/crf/README.md"

# Refuse laboratory metadata
test ! -e "$STAGING/export_meta.json"

sha256sum \
  "$STAGING/config.json" \
  "$STAGING/model.safetensors" \
  "$STAGING/tokenizer.json" \
  "$STAGING/tokenizer_config.json" \
  "$STAGING/crf/best.pt"
```

Expected SHA-256 values are the five hashes in Section 1.

`release/huggingface-model/staging/` is listed in `.gitignore`. Do not `git add` the weights.

---

## 4. Staging layout after a successful copy

```text
release/huggingface-model/staging/
  README.md
  config.json
  model.safetensors
  tokenizer.json
  tokenizer_config.json
  crf/best.pt
  crf/README.md
```

---

## 5. Hugging Face upload (ready, not executed here)

Set the repository id yourself. Do not invent one.

```bash
# Still from Chinese_skill_benchmark_Paper/
export HF_REPO_ID='[TODO: user-or-org/chinese-jobbert]'

huggingface-cli whoami
# must print a username; if "Not logged in":
#   huggingface-cli login
# or: hf auth login

# Create an empty model repo once (skip if it already exists)
huggingface-cli repo create "$HF_REPO_ID" --type model --yes

# Upload the staging tree as the repository root
huggingface-cli upload "$HF_REPO_ID" \
  release/huggingface-model/staging \
  . \
  --repo-type model \
  --commit-message "Add Chinese JobBERT encoder ckpt65000, V4 CRF best.pt, and model card."
```

Equivalent newer CLI:

```bash
hf repo create "$HF_REPO_ID" --type model
hf upload "$HF_REPO_ID" release/huggingface-model/staging . --repo-type model
```

After a successful upload:

1. Confirm the repository is **public** (PeerJ reviewers must download without requesting access).
2. Replace `[TODO: Hugging Face model URL]` in `README.md`, `CITATION.cff`, `DATA_AVAILABILITY.md`, both cards, and `release/zenodo/.zenodo.json`.
3. Do not treat the Hugging Face URL as the PeerJ archival DOI; archive the GitHub release on Zenodo as well.

---

## 6. How reviewers should load the files

The encoder loads with `AutoModel` / `AutoTokenizer`. The CRF head does **not** load with `AutoModelForTokenClassification`. Use `BertCRF` in `scripts/train_cn_roberta_crf.py` and `torch.load("crf/best.pt")`. Paper-main typed exact F1 **0.4331** additionally requires jieba snap via `scripts/eval_hybrid_cws_simhuman.py` (or `scripts/cws_snap.py`) against `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`.
