# Reproducibility guide — current paper

The current manuscript has 22 pages, 11 tables and 5 figures. Its primary student results use the 150-sentence human reference. Start with the following entries; historical commands remain available with their original experimental scope.

1. [Current evaluation entry](reproduction/EVALUATION_ENTRY.md): comparison, files, hashes, scoring directions and missing rerun requirements.
2. [Paper/table/figure map](reproduction/PAPER_INDEX.md): exact destinations for removed tables and current body results.
3. [Companion notes](reproduction/README.md): archived tables, failed outputs, detailed implementation reminders and naming map.
4. [58-item material inventory](reproduction/evaluation/materials_inventory.json) and [frozen contract](reproduction/evaluation/contract.json): repository matches versus local-only evidence.
5. [Full historical reproduction guide](docs/archive/REPRODUCIBILITY_0911.md): original environment pins, checksums and commands for historical V4/Gold v2/JSON-offset studies.

```bash
python reproduction/verify_companion.py
```

This standard-library check validates transferred-file hashes, output row totals, documented aggregate counts, numeric display consistency and local link paths. It makes no model call and does not rescore predictions.

Current Qwen no adapter is 0.3612; matched B2 LoRA is 0.5403 ± 0.0354. JobBERT B1/B2 are 0.1422 ± 0.0138 and 0.5536 ± 0.0054. Sample SD uses seeds 42/43/44, not independent test replications. These are different studies from the historical V4 2,601-row and JSON-offset results.

The repository scorer and evaluation wrapper exist. Complete historical run replay additionally requires correctly bound predictions, prompts, parser/scorer bytes and model artifacts. Do not treat a documentation synchronization, stored aggregate CSV or a matching version string as proof of complete retraining or provider-model identity. See [open evidence items](reproduction/ROUND2_CHANGES.md).
