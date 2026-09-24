# TABLE11_EVIDENCE_20260924

Server-B audit of Overleaf Table 11 / `tab:external-chinese` (Chinese LSKT linear head, protocol `chinese_lskt_linear_b2_20260921`).

This pack does **not** retrain and does **not** overwrite original run files. Weights are public on Hugging Face; see `HF_RELEASE.md`.

## Delivery status

| Claim | Status |
|---|---|
| Files checked | **yes** |
| Frozen predictions independently rescored with `cnss-lskt-1.2.0` | **yes** (byte-identical F1) |
| Six original checkpoints re-inferred on frozen Gold150 | **yes** (0 tag diffs vs frozen preds) |
| Full training rerun | **no** (out of scope) |
| Hugging Face / Zenodo weight upload | **HF public** (six repos; canonical weights); additional Zenodo archive https://doi.org/10.5281/zenodo.22937245 (sidecars + audit pack; not a v0.1.x dataset version) |
| GitHub audit materials | branch `audit/table11-evidence-20260924`; original results commit `46d1166` left intact |

Local path: `/home/guojingli3/cnss_external_benchmarks_20260921/TABLE11_EVIDENCE_20260924`

## Answers

1. **No-translation Chinese adaptation:** yes, from executed code and inputs (character tokens of original Chinese text; no translate/transcribe path).
2. **Original Gold150:** yes. SHA-256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`; 150 sentences, 663 spans, L=2; byte-identical to the public freeze.
3. **Six original checkpoints and predictions exist:** yes (`best/model.safetensors` ~2.1 GiB × 6, plus `gold150_predictions.jsonl`).
4. **Old table recomputes:** yes. Typed exact F1 matches the receipt and `46d1166` snapshot for all six cells. Mean±sample SD unchanged: XLM-R **0.522 ± 0.022**, ESCO **0.538 ± 0.021**.
5. **Platforms:** lab disk + this pack. GitHub results snapshot `46d1166` intact. **Canonical weights are on Hugging Face** (`HF_RELEASE.md`). Additional archive: https://doi.org/10.5281/zenodo.22937245. Base-encoder pages and JobBERT-zh are still **not** these models. Dataset DOIs v0.1.x were not modified.

## Do not copy

Checkpoints, `hf_cache`, venv, tokens, and unrelated native/common runs stay on the lab disk. See `proposed_publish_manifest.json`.
