# Split leakage audit

Corpus: `data/annotated/processed/chinese_skillspan/{train,dev,test}.json`
Silver: `data/annotated/raw/chinese_skillspan/doccano_silver_merged_{train,dev,test}_sorted_enrich.jsonl`
Gold: canonical v1 (test subset, unique IDs).

## Split sizes

- train 17460 sentences / 1600 postings
- dev 2143 / 200 postings
- test 3237 / 200 postings
- canonical Gold 2583 IDs; all Gold IDs ⊆ test? True

## Posting-level (`global_id`)

Cross-split posting groups: **0**.

No `global_id` is shared across train/dev/test.
Posting-level split leakage is **not** present. Sentence-level duplicates still exist.
Encoder 3-seed runs remain **blocked** until Gold conflicts are adjudicated and this audit is accepted;
they are not blocked by a posting rebuild.

## Sentence-level duplicates

- Cross-split exact text groups: 67 (non-boilerplate 31)
- Cross-split normalized (strip space/punct, digit→0) groups: 93
- Cross-split 24-char prefix template groups: 31
- Cross-split job-title groups: 33 (same title string, **different** posting IDs)

Exact-text leakage includes short boilerplate (。, `&nbsp;`, 马克数据 watermark). See CSV `boilerplate=1`.
Non-boilerplate exact matches are real sentence reuse across postings, not the same `global_id`.

## Gold vs Silver source overlap

- Gold IDs ∩ silver_train IDs: 0
- Gold IDs ∩ silver_dev IDs: 0
- Gold IDs ∩ silver_test IDs: 2583 (expected: Gold is a test subset)
- Gold posting ∩ silver_train posting: 0
- Gold text ∩ train text: 28
- silver_train IDs == corpus train IDs: True

Silver train/dev/test are the **same sentences** as the corpus splits with LLM silver labels.
Overlap of Gold with silver_test is by design. Overlap of Gold with silver_train would be leakage;
ID/posting overlap with silver_train is zero if posting split is clean.
Shared **text** between Gold and train is the sentence-level exact-dup issue above.

Pairs: `reports/split_duplicate_pairs.csv`.
