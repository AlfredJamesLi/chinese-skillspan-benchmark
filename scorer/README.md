# Unified LSKT scorer (`cnss-lskt-1.2.0`)

**Historical V4 hybrid reference (2026-08-27; not the current human-reference evaluation):** `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` (V4 SOP+jieba; 2601 IDs derived from Gold v2). Same `--align-mode official`. Do **not** call this human Doccano Gold.

**Provenance file (do not overwrite):** `data/gold_canonical_v2.jsonl` (2601 unique IDs, sha256 `7a26e32b…504ff6`). Use for appendix / construction-history scores only. Do not substitute `gold_canonical_v1.jsonl`.

```bash
# historical V4 hybrid reference
python score_lskt.py \
  --gold ../data/test_lskt_v4_cws_simhuman980_hybrid.jsonl \
  --pred PRED_jieba_snapped.jsonl \
  --align-mode official \
  --out report.json

# appendix (Gold v2)
python score_lskt.py \
  --gold ../data/gold_canonical_v2.jsonl \
  --pred PRED.jsonl \
  --align-mode official \
  --out report_g2.json

python test_regression.py
```

`test_regression.py` uses the paper tree next to `scorer/` (or `$CNSS_PAPER_ROOT`). Parent-repo ChatGPT / JobBERT dumps are skipped when those files are absent.

`--require-exact-id-set` only when the dump is supposed to contain Gold IDs and nothing else.

For the current 150-sentence human-reference evaluation, use [the evaluation guide](../reproduction/EVALUATION_ENTRY.md) and `scripts/eval_gold150_ext.py`. The wrapper converts frozen Unicode-character labels in memory. Historical token-index and current character-index protocols must retain their matching input representation.

## Official alignment

- Gold IDs must be unique.
- Each Gold ID must have exactly one prediction. Missing Gold IDs or duplicate predictions for a Gold ID **fail** (exit 2) unless the caller empty-fills first (hybrid eval scripts do this).
- Predictions whose IDs are **outside** Gold (e.g. the rest of the 3237 test set) are counted as `n_extra`, **not scored**, and do not fail unless `--require-exact-id-set`.

## Metrics

Primary: **typed exact-span micro F1** (sum TP/FP/FN over sentences).

Also reported: collapsed exact; typed/collapsed relaxed (token IoU ≥ 0.5); L/K/S/T; Gold/pred row and unique-ID counts; matched/missing/extra/duplicate; Gold hash, pred hash, git commit, full config.

`v1.0–v1.1` put `(start,end,type)` into a **global set**, so identical offsets in different sentences collapsed. That bug produced JobBERT collapsed F1 ≈ 0.46. `1.2.0` uses sentence-level micro F1.

Pred fields tried in order: `pred_tags`, `list_of_selection_bio4`, `list_of_selection`, `pred`.
An all-O list is treated as empty if a later field contains B/I (LLM dumps often have empty bio4 beside filled untyped tags).
