# Unified LSKT scorer (`cnss-lskt-1.2.0`)

Official human Gold is **canonical** `data/gold_canonical_v2.jsonl` (2601 unique IDs, sha256 `7a26e32b…504ff6`).  
Do not score against `gold_canonical_v1.jsonl` for paper tables. Do not overwrite Gold v2.

Matched SOP+jieba test gold (not human Gold): `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`. Same scorer, same `--align-mode official`.

```bash
python score_lskt.py \
  --gold ../data/gold_canonical_v2.jsonl \
  --pred PRED.jsonl \
  --align-mode official \
  --out report.json

python test_regression.py
```

`--require-exact-id-set` only when the dump is supposed to contain Gold IDs and nothing else.

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
