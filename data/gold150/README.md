# Human reference set

The human reference contains **150 sentences and 663 competency spans**: a 50-sentence calibration cohort and a 100-sentence challenge cohort. Adjudicated annotations are frozen for evaluation.

**[Download the reference](../gold150_test.jsonl) · [Versioned archive](https://doi.org/10.5281/zenodo.22698504) · [Score predictions](../../reproduction/EVALUATION_ENTRY.md)**

| Component | Sentences | File |
|---|---:|---|
| Complete reference | 150 | [gold150_test.jsonl](../gold150_test.jsonl) |
| Challenge cohort | 100 | [gold100_locked.jsonl](gold100_locked.jsonl) |
| Calibration cohort | 50 | [iaa50_gold_locked.copied.jsonl](iaa50_gold_locked.copied.jsonl) |

Records use `source_id` and Doccano `label` triples: start, end, type. Offsets refer to original Unicode code points, start at zero, and exclude the end. The complete reference SHA-256 is `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`.

For saved predictions from the shared-guideline protocol:

```bash
python scripts/eval_gold150_ext.py --protocol shared_prompt --gold_eval data/gold150_test.jsonl --pred path/to/accepted_predictions.jsonl --out output/human_reference_score.json
```

Replace the prediction path with an existing, compatible file. This scores saved predictions; it does not call a model. Other protocols have separate instructions in the [evaluation guide](../../reproduction/EVALUATION_ENTRY.md).

This set is included in **v0.1.3**, not v0.1.1/v0.1.2. It differs from the historical 2,601-record hybrid reference and the 200-sentence analysis set. Its calibration/challenge selection history is described in the manuscript. Human-reviewed Silver records remain supervision or quality checks unless separately designated for evaluation.
