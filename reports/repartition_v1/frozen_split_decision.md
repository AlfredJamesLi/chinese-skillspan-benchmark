# Frozen split decision (repartition_v1)

Chosen candidate seed: **7** (official encoder seed set; not invented).
Objective cost: 0.614334. Details: {"js_label_train_test": 0.00023443626416153052, "js_label_train_dev": 0.0006342854273535536, "abs_empty_train_test": 0.006120495960434402, "abs_len_train_test": 0.014221343566609762, "missing_L_in_split": 0, "missing_source_in_split": 0, "post_quota_l1": 0.6}.

## Why this split
Among seeds [42, 123, 2026, 7, 13], this is the lowest-cost candidate that passed every hard constraint.
Ranking used only source/post quotas, L/K/S/T mix, empty rate, and length. **No JobBERT, RoBERTa, Qwen, or LLM F1 was computed or used.**

## Remaining imbalance
Public has 20 posts (quota 12/4/4) and very few L spans historically (33 on old V4 test, 1 in Public). Some splits may still have sparse L.
Cloud has 40 posts (quota 28/4/8). Near-duplicate grouping can move extra posts with a group.

## Label provenance (not human Gold)
Train/dev/test all use **LSKT v4 character BIO** from `train/dev/test_lskt_v4_silver.jsonl` (rule_v4 / Codex sample drafts).
- SimHuman 980 overlay is **not** treated as completed dual-blind human SOP.
- Gold v2 remains frozen appendix provenance; it is **not** overwritten and is **not** the new test gold.
- New test is mixed-provenance v4 silver, including Grad (previously train-only drafts).

## 636 records
They are the processed-test sentences absent from unique-first Gold v2 / V4 hybrid (3237−2601).
They retain v4 silver labels and **were eligible**. Placement after freeze: train=460 dev=91 test=85.

## Old source-disjoint benchmark
Unchanged: `gold_canonical_v2.jsonl`, `test_lskt_v4_cws_simhuman980_hybrid.jsonl`, old train/dev silver, encoder dirs, dumps.
Future paper role: **appendix cross-source transfer diagnostic**.

## SHA256
See `manifests/repartition_v1/SHA256SUMS`.
