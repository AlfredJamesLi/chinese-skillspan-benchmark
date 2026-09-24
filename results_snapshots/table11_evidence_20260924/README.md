# Table 11 evidence pack (2026-09-24)

Supporting files for the Chinese LSKT linear-head runs reported in Table 11 (protocol `chinese_lskt_linear_b2_20260921`). The original training outputs were left in place; the six runs were not retrained.

Predictions were rescored with `cnss-lskt-1.2.0` (typed exact F1 unchanged). Re-inference from the stored checkpoints on the frozen Gold150 file produced 0 tag differences.

Weights are on Hugging Face (`HF_RELEASE.md`). This pack and the matching Zenodo record keep scores, predictions, tokenizer/config sidecars, and checksums. The 2.1 GiB `model.safetensors` files are not included. Corpus snapshots remain on the v0.1.x dataset records. GitHub results snapshot `46d1166` is unchanged.

## Findings

Training used Chinese character tokens from the source sentences. The trainer has no translation, transcription, or gold-hint path. Gold150 freeze SHA-256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` (150 sentences, 663 spans, L=2) matches the public file. All six checkpoints and `gold150_predictions.jsonl` files are present. Typed exact F1 matches the earlier receipt and snapshot `46d1166`: XLM-R **0.522 ± 0.022**, ESCO **0.538 ± 0.021**.

See `CHECK_REPORT.md` for the execution record, hashes, and per-seed tables.
