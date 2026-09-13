# Evaluation entry for the current manuscript

Use this entry for current Tables 5/6/11 and Figure 5. The [paper index](PAPER_INDEX.md) distinguishes historical tables. Read [paper names](../PAPER_NAMES.md) and [experimental notes](experimental_notes/README.md) before selecting artifacts.

## 1. Select the comparison

| Comparison | Reference and inputs | Output interpretation |
|---|---|---|
| Shared-guideline inference, six configurations | Frozen 150-sentence human reference; shared occurrence protocol | Descriptive configuration comparison, with separate reasoning/output settings |
| Qwen no adapter vs B2 LoRA, seeds 42/43/44 | Same reference, prompts, parser and decoding; 2,150/169 train/dev | Task adaptation under the fixed protocol |
| JobBERT B1 vs B2, seeds 42/43/44 | Same 150-sentence reference; primary 2,156/169 matched texts, changed train/dev labels | Joint supervision and selection comparison |
| Historical JSON-offset/SOP/V4/Gold v2 | Their original label files and protocols | Supplementary results, not replacements for current cells |

## 2. Resolve files and check identities

The current reference is [data/gold150_test.jsonl](../data/gold150_test.jsonl), 150 sentences and 663 spans, SHA-256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`. Its copy under `data/gold150/` has the same Git blob identity. Released Qwen supervision is [data/silver_plus_v6a_nocross/](../data/silver_plus_v6a_nocross/), 2,150/169 records.

[contract.json](evaluation/contract.json) records exact reference/input/system/user/parser hashes from the earlier local verification. [materials_inventory.json](evaluation/materials_inventory.json) lists all 58 earlier evidence items, with repository paths only where byte identity was found against the pre-sync Git tree. Empty repository paths mean local evidence was available during revision but is not supplied by this documentation update. No machine-specific absolute path is needed to read this inventory.

For the shared protocol the recorded files are `PROMPT_gold150_shared_guidelines_v2_rev2_patch1.DRAFT.system.txt`, `USER_TEMPLATE_v2_rev2_patch1.DRAFT.txt` and `parser_occurrence_v1_1.py`. Their original names and hashes remain authoritative. The original run registry identifies scorer version `cnss-lskt-1.2.0`, but not its executable hash. The repository scorer is available; matching a version string alone does not establish historical byte identity.

## 3. Inspect committed results without inference

```bash
python -c "import csv; print(*csv.DictReader(open('reproduction/current_results/inference.csv', encoding='utf-8')), sep='\n')"
python -c "import csv; print(*csv.DictReader(open('reproduction/current_results/qwen_runs.csv', encoding='utf-8')), sep='\n')"
python reproduction/verify_companion.py
```

These commands display archived values or validate companion-file checksums, counts and links. They do not call models, train, or score predictions. Reading a CSV is not independent reproduction of a model result.

## 4. Score compatible predictions if those artifacts have been obtained

The existing [evaluation wrapper](../scripts/eval_gold150_ext.py) accepts `shared_prompt` and `jobbert_v6a` protocol labels and converts the reference in memory when needed. It does not reconstruct model outputs. Supply the correct frozen, scorer-compatible accepted predictions and validate all 150 unique IDs, exact source texts and file hashes first. Preserve empty and malformed-response cases according to the recorded parser contract.

```bash
python scripts/eval_gold150_ext.py --protocol shared_prompt --gold_eval data/gold150_test.jsonl --pred PATH_TO_FROZEN_ACCEPTED_PREDICTIONS --out output/shared_prompt_score.json
python scripts/eval_gold150_ext.py --protocol jobbert_v6a --gold_eval data/gold150_test.jsonl --pred PATH_TO_JOBBERT_PREDICTIONS --out output/jobbert_score.json
```

`PATH_TO_*` denotes an input the reader must provide; it is not a shipped file or runnable placeholder. The wrapper's legacy parse-status summary is not a replacement for the [mutually exclusive outcome table](output_outcomes/README.md). The current task did not execute these scoring commands. Resolve the original scorer binding before claiming exact historical replay, especially for relaxed matching.

Typed exact matching requires equal boundaries and type. Relaxed matching uses same-type one-to-one greedy matching with character IoU >= 0.5. Micro-F1 pools TP/FP/FN; 150 is sentence coverage, not its numerical denominator. Three seeds yield sample SD on the same reference, not a test-set confidence interval. Missing/extra/duplicate IDs require inspection, not silent deletion.

## 5. Read diagnostics and training requirements

- [Qwen counts](qwen_diagnostics/README.md): full-sentence exact matching precedes type/length aggregation; length bins have 346/243/74 gold spans; one sentence can contribute to several bins. No prediction repair.
- [Output outcomes](output_outcomes/README.md): all nine rows sum to 150; partial responses retain accepted spans, wholly rejected/malformed cases count as empty predictions.
- [Agreement](agreement/README.md): character kappa and exact span F1 describe different aspects of coding; machine-prefilled review is a separate design.
- [Selection records](supplementary_tables/table_19.md) and [training details](experimental_notes/README.md): selected epochs and development scores remain separate from reference scores. JobBERT's historical implementation binding and Qwen adapters remain unavailable for complete rerunning.

The current handbook v4.2.14, historical calibration guide, frozen reference metadata and executed prompt have separate roles. [The R23 check](evaluation/version_applicability.json) only establishes the documented example's absence from the current reference by ID/text. Never relabel the reference to match a later handbook and reuse old scores.
