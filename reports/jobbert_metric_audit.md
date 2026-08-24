# JobBERT metric audit

Scorer: `cnss-lskt-1.2.0` (sentence-level micro F1).
Canonical Gold: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/data/gold_canonical_v1.jsonl` (2583 unique IDs, SHA256 `458c91478079c7702a82befc15c58f4be7cc77b2cf820b0ed33efb791657e5df`).
Original dump (not overwritten): `/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/out_jobbert_skill_chinese_encoder_aligned.jsonl`.
Derived unique-first view: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/reports/views/jobbert_skill_unique_first_canonical_v1.jsonl` (n_out=2583).

## Verdict: do not adopt ~0.46

**Adopt 0.46? `False`.** The ~0.46 figure is an artifact of scorer `cnss-lskt-1.0/1.1`,
which put `(start, end, type)` into a **global set**. Identical token offsets in different
sentences collapsed, so thousands of illegal `I-SKILL` fragments became ~950 unique offset
patterns and spuriously matched Gold.

**Keep the paper ballpark ~0.0045? `True`** (as an order-of-magnitude / published S-F1).
Official unique-view collapsed exact F1 = **0.004480651731160896**
(P=0.0033788972508063276, R=0.006648534300392868, TP=44, FP=12978, FN=6574).
Paper Table 3 JobBERT-skill **0.0045** / knowledge **0.0038** are in this range.
They are **not** a 100× scoring error relative to BIO-legal micro F1.
Do **not** replace them with 0.46. Do **not** put 0.46 in any paper table.

Unique-view official alignment_ok: **True** — None
Raw dump official alignment_ok: **False** — duplicate predictions for 56 gold IDs

## Illegal BIO transfers (unique-first rows vs canonical Gold)

- I-after-O: 14094

Total illegal I transfers: **14094**.
Dominant pattern: `I-SKILL` immediately after `O` (model emits I without B).
BIO-legal decode **drops** those I tokens (they do not start a span).
`repair-I-to-B` turns them into `B-SKILL` and creates many extra predicted spans.

## Alignment (character / token / offset)

- `''.join(tokens) == sentence`: ok=2583, fail=0
- reconstructed token offsets cover the sentence: ok=2583, fail=0
- no_token_char_spans: 2583

JobBERT `pred_tags` length is aligned to Gold `tokens`. Scoring is **token-index** spans,
not character offsets. Leading spaces in `sentence` are separate tokens when present.

## Scheme comparison (collapsed exact unless noted)

- BIO-legal (scorer): F1=0.004481 TP=44 FP=12978 FN=6574
- repair-I-to-B: F1=0.006462 TP=109 FP=27007 FN=6509
- seqeval-default (I starts entity): F1=0.006462 TP=109 FP=27007 FN=6509
- seqeval-strict / IOB2-like: F1=0.004481 TP=44 FP=12978 FN=6574
- typed exact (LSKT vs SKILL): F1=0.000000
- collapsed relaxed IoU≥0.5: F1=0.072505
- seqeval package: default F1=0.006462 (matches in-repo I-starts-entity / repair-I-to-B); strict IOB2 F1=0.004481 (matches BIO-legal). Independent confirmation of the in-repo decoders.
- JobBERT-knowledge unique-view collapsed F1: 0.003734733017058645

## Fixtures

12/12 fixtures passed (see `reports/jobbert_fixtures.csv`).
These check exact match, miss, false span, boundary, type mismatch, illegal I-after-O,
long span, merge error, empty, length pad, and leading illegal I.

## Manual span samples

Random TP / FP / FN (seed 20260822): `reports/jobbert_span_samples.json`.
Token slices are `''.join(tokens[start:end])`. BIO-legal JobBERT predicts few true spans;
most mass is FP from leftover `B-SKILL` fragments after dropping illegal I.

## Why v1.1 reported ~0.46

```python
# buggy
all_spans.extend(sentence_spans)  # (start, end, type) only
tp = len(set(gold_spans) & set(pred_spans))
```
Correct: count TP/FP/FN **inside each sentence**, then sum (micro).
A regression test (`test_micro_does_not_collapse_cross_sentence_offsets`) now requires
two sentences with the same offsets to contribute 2 TP.
