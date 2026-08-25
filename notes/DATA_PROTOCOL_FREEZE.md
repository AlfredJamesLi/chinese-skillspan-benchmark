# Data and scoring protocol (PeerJ CS) — Gold uniqueified (v2)

Date: 2026-08-22. Gold-v2 file hashes are frozen. **Submission venue: PeerJ Computer Science** (Chinese-SkillSpan dataset paper). Do not write DASFAA 2026 as the target venue. Gold v2 sha and official human gold do **not** change with venue.  
18 Gold conflicts are adjudicated. **Do not change PDF Table 3 paper S-F1 cells.** Do not overwrite original LLM dumps. Claude/Kimi fills live in `reports/views/*_filled_v2.jsonl` only.

Scorer: `cnss-lskt-1.2.0`. Git: `NO_GIT_HEAD`.

---

## Status

| Claim | Status |
|---|---|
| 18 Gold conflicts | **Adjudicated** (Doubao + human; 3 overrides) |
| Canonical Gold unique IDs | **Yes — v2, 2601** SHA256 `7a26e32b…504ff6` |
| PDF Table 3 | **Do not update** until unique-first views are the declared pred policy for all models |
| JobBERT ~0.46 | **Rejected** |
| Qwen 0.2130 | **Unreproducible** |

Distinguish: corpus test **3237**; raw Gold rows **2676**; canonical unique Gold **2601**.

---

## Canonical files (use these; none are a public freeze)

| Role | Path | Rows | Unique IDs | SHA256 |
|---|---|---:|---:|---|
| Corpus train | `data/annotated/processed/chinese_skillspan/train.json` | 17460 | 17460 | `0a24841b97416a0b50e80c5e848bc6b232be91c7bc2f81c05ddb937a2924a44b` |
| Corpus dev | `…/dev.json` | 2143 | 2143 | `ea0dabb8dbf295d4edc046fa2ecf9610d33557216095aa54ac9690a77954b1ac` |
| Corpus test | `…/test.json` | **3237** | 3237 | `263edc8b07db139f078f1023bad7f46dc2c6bf3e7ec1bdfb7cbccded2ded3142` |
| Raw Gold (do not edit) | `chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl` | **2676** | **2601** | `103e400c79eb3954d0857e7000b4388773622fda6a333e72be7720bf27f5e172` |
| Canonical Gold v1 | `Chinese_skill_benchmark_Paper/data/gold_canonical_v1.jsonl` | **2583** | **2583** | `458c91478079c7702a82befc15c58f4be7cc77b2cf820b0ed33efb791657e5df` |
| **Canonical Gold v2** | `Chinese_skill_benchmark_Paper/data/gold_canonical_v2.jsonl` | **2601** | **2601** | `7a26e32b89d4e501175cb96443e35e171cea08d91501d2a32779b96ee8504ff6` |

Official scoring still uses **Gold v2 only**. A future eval Gold (`reports/gold_eval_v3/`, 300-item IAA pilot) must not overwrite this file. Do not put v3-pilot F1 into the PDF or `confirmed-results.md`.

Label field: `list_of_selection_bio4` (L/K/S/T). No ESCO concept IDs.

Banned: preprocessing `test.json` (2639, empty labels); `*.eval_ner.json`.

---

## Official scoring

```bash
python Chinese_skill_benchmark_Paper/scorer/score_lskt.py \
  --gold Chinese_skill_benchmark_Paper/data/gold_canonical_v2.jsonl \
  --pred <dump.jsonl> \
  --align-mode official --out report.json
```

- Gold IDs unique; each Gold ID exactly one prediction.
- Extra pred IDs (rest of test) allowed and counted, not scored.
- `--require-exact-id-set` only when the dump should contain Gold and nothing else.
- Primary metric: **typed exact micro F1** (sum TP/FP/FN over sentences).
- `v1.0–v1.1` global-set span F1 is invalid.

---

## Paper wording later (do not edit the PDF now)

- “ESCO-aligned concept extraction” → “ESCO-derived LSKT span extraction”
- Delete Concept Accuracy
- Delete Industry-OOD, Time-OOD, long-tail improvement claims
- Table 1 Avg 4D from release canonical data after freeze
- Table 3 only after frozen Gold + official-aligned dumps

## Experiment order (not started)

1. Chinese BERT/RoBERTa or MacBERT token/CRF, full train, 3 seeds  
2. XLM-R, 3 seeds  
3. GlobalPointer or other span baseline, 3 seeds  
4. Stratified dual IAA, ~300 items  
5. Claude missing Gold IDs, then Kimi missing Gold IDs  

Posting-level train/dev/test `global_id` overlap is **zero**. Sentence-level exact dups exist. Do not rebuild splits for posting leakage. Do not start the 3-seed runs in this round.
