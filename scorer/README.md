# Unified LSKT scorer (`cnss-lskt-1.2.0`)

Gold for official scoring is **canonical** `data/gold_canonical_v1.jsonl` (unique IDs).
Raw Gold is not modified. Canonical Gold is **not frozen** while annotation conflicts remain.

```bash
python score_lskt.py \
  --gold ../data/gold_canonical_v1.jsonl \
  --pred PRED.jsonl \
  --align-mode official \
  --out report.json

# Only when the dump is supposed to contain Gold IDs and nothing else:
python score_lskt.py --gold GOLD --pred PRED --align-mode official --require-exact-id-set
python test_regression.py
```

## Official alignment

- Gold IDs must be unique.
- Each Gold ID must have exactly one prediction. Missing Gold IDs or duplicate predictions for a Gold ID **fail** (exit 2).
- Predictions whose IDs are **outside** Gold (e.g. the rest of the 3237 test set) are counted as `n_extra`, **not scored**, and do not fail unless `--require-exact-id-set`.

## Metrics

Primary: **typed exact-span micro F1** (sum TP/FP/FN over sentences).

Also reported: collapsed exact; typed/collapsed relaxed (token IoU ≥ 0.5); L/K/S/T; Gold/pred row and unique-ID counts; matched/missing/extra/duplicate; Gold hash, pred hash, git commit, full config.

`v1.0–v1.1` put `(start,end,type)` into a **global set**, so identical offsets in different sentences collapsed. That bug produced JobBERT collapsed F1 ≈ 0.46. `1.2.0` uses sentence-level micro F1.

Pred fields tried in order: `pred_tags`, `list_of_selection_bio4`, `list_of_selection`, `pred`.
An all-O list is treated as empty if a later field contains B/I (LLM dumps often have empty bio4 beside filled untyped tags).
