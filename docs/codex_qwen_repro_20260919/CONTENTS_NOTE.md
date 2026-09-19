# What is and is not advertisement text

Codex asked: the pack contains Gold150, so one cannot claim it has *no* job-ad sentences.

**Present (already public freeze, not a new dump):**

- `protocol/gold150_test.jsonl` and `eval_runtime/data/gold150_test.jsonl`
  SHA256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`
  Same 150-sentence human-reference freeze as Zenodo v0.1.3.
- Frozen Gold150 *predictions* (`pred_for_score.jsonl`, `records.jsonl`, `gold_for_score.jsonl`).
  Predictions include tokens / extracted spans from those 150 sentences.

**Absent (do not add):**

- Expanded-silver `train_occurrence.jsonl` / `dev_occurrence.jsonl` / `test_occurrence.jsonl`
- B2 `train_b2.jsonl` / `dev_b2.jsonl` (hashes only, in `DATA_MANIFEST.json`)
- WAVE3 / Run2500 labelled dumps
- Vendor CSV / XLSX advertisement corpora

Zenodo description must say: Gold150 freeze sentences are included for scoring and are the v0.1.3 overlay; expanded-silver training sentences and a full advertisement dump are not included. Do **not** write an unqualified “contains no job-advertisement wording.”

# Licence (do not pick a nearby Creative Commons item)

Read `LICENSE_NOTICE.md`. Governing notice is that file, not Zenodo’s CC-BY-4.0 hook default.

- Software / scorer in the pack: Apache-2.0
- Qwen2.5-14B-Instruct base (not in the zip): Apache-2.0 on the local snapshot
- LoRA adapters: not a CC-BY grant
- Job-ad wording: not CC-BY
