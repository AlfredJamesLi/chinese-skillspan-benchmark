# Hugging Face live model-card upload

**Upload README only. Do not re-upload weights.** Hub user `AlfredJames` is not GitHub `AlfredJamesLi`.

Local templates (source of truth after 2026-09-11 naming/DOI sync):

| Hub repo | Local card | Role |
|---|---|---|
| `AlfredJames/jobbert-zh` | `release/huggingface-model/README.md` | Paper-main V4 encoder (**0.4331**) |
| `AlfredJames/jobbert-zh-v6a` | `release/huggingface-model-v6a/README.md` | Human-reference B2 continuation (**0.5536±0.0054**) |
| `AlfredJames/jobbert-zh-1m` | `release/huggingface-model-1m/README.md` | 1M DAPT contrast (**0.427162**); no previous local tree |

Keep YAML `license: other` on all three cards. GitHub `LICENSE` Apache-2.0 is for repository software, not a claim that Hub weights are Apache-2.0.

Qwen LoRA is **not** a Hub upload.

---

## 1. Auth

```bash
# CLI on this host: /home/guojingli3/.local/bin/hf
hf auth whoami
```

Expected: user **`AlfredJames`**. If not logged in: `hf auth login` (write token with permission to update those three model repos). Do not commit tokens.

---

## 2. Dry-run: README only

From `Chinese_skill_benchmark_Paper/`:

```bash
hf upload AlfredJames/jobbert-zh \
  release/huggingface-model/README.md README.md \
  --repo-type model --dry-run

hf upload AlfredJames/jobbert-zh-v6a \
  release/huggingface-model-v6a/README.md README.md \
  --repo-type model --dry-run

hf upload AlfredJames/jobbert-zh-1m \
  release/huggingface-model-1m/README.md README.md \
  --repo-type model --dry-run
```

`--dry-run` must list **only** `README.md`. Abort if the command would touch `model.safetensors` or `crf/best.pt`.

---

## 3. Live upload (after whoami is AlfredJames)

```bash
hf upload AlfredJames/jobbert-zh \
  release/huggingface-model/README.md README.md \
  --repo-type model \
  --commit-message "Sync model card: Zenodo v0.1.3, paper-main 0.4331, human-reference naming."

hf upload AlfredJames/jobbert-zh-v6a \
  release/huggingface-model-v6a/README.md README.md \
  --repo-type model \
  --commit-message "Sync model card: human reference set, v6a_nocross 2150/169, do not rank vs 0.4331."

hf upload AlfredJames/jobbert-zh-1m \
  release/huggingface-model-1m/README.md README.md \
  --repo-type model \
  --commit-message "Sync model card: 1M DAPT contrast 0.427162; not paper-main."
```

---

## 4. After upload

- [ ] Open each Hub page incognito: card text matches the local template; weights still present.
- [ ] YAML still shows `license: other`.
- [ ] Paper-main repo still states typed exact **0.4331**; v6a still **0.5536±0.0054**; 1M still **0.427162**.
- [ ] No ranking of 0.4331 against 0.5536 in one table on the 3M card (cross-link only).

This document does not create a Hugging Face **dataset** repository (there is none).
