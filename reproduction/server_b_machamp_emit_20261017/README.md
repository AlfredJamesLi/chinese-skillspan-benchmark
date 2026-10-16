# Server B MaChAmp source and aggregation recovery

The 17 October follow-up supplies the previously absent `emit_verified_results.py`, its local `audit_and_lexicon.py` dependency, and three complete modified SkillSpan MaChAmp source files. All seven received files, including the exporter README and checksum list, are preserved byte-for-byte under [original](original). Six incoming checksums and five Python AST checks pass. [AUDIT.json](AUDIT.json) records the ZIP and file hashes.

## What this resolves

- [Result aggregation entry](original/scripts/emit_verified_results.py) and [local dependency](original/audit_and_lexicon.py): source delivery is now complete for these two files. The entry aggregates common, Chinese and native results and also performs bootstrap calculations when run; it was not executed in this audit.
- [Sampler](original/executed_skillspan_machamp/machamp/data/machamp_sampler.py): the complete supplied file uses `super().__init__()`.
- [Trainer](original/executed_skillspan_machamp/machamp/model/trainer.py) and [predictor](original/executed_skillspan_machamp/predict.py): supplied files contain the `weights_only=False` loading edits.

The complete unified diff was **not found**. The earlier 40-line patch remains truncated and must not be applied. These complete source files provide the delivered implementation; they do not establish a complete upstream checkout or its exact revision. Do not manufacture a replacement historical patch or apply the SkillSpan sampler to the ESCOXLM-R tree.

## Layout and prerequisites

The exporter identifies server B (DS210039), rooted at `/home/guojingli3/cnss_external_benchmarks_20260921`; see [original provenance](original/README.md). Local checks establish identity to the supplied package, not independent server access or proof that these current bytes were executed historically.

For aggregation, in a separate working copy of the corresponding B experiment tree, place `scripts/emit_verified_results.py` under `scripts/` and `audit_and_lexicon.py` at the tree root. Configure the script's hard-coded `ROOT` for that working copy. It reads `models.json` and `sources.json` at import time, and expects the matching `data/` and `runs/` layout. Those inputs and outputs are not included here. Do not run it against the published frozen outputs in place: it writes `results.jsonl`, `raw_metrics.csv`, receipts and comparison summaries. Its name does not constitute independent verification of those results.

For the recovered SkillSpan files, the historical target is `upstream_full/SkillSpan/machamp/`: map `predict.py` to its root, and the two `machamp/` files to their corresponding relative paths, only in a separate compatible checkout after checking the diff. The complete MaChAmp modules, model dependencies, datasets, checkpoints and runtime must be supplied separately. No end-to-end reproduction or upstream revision binding is claimed.

MaChAmp upstream: https://github.com/machamp-nlp/machamp ; Apache-2.0 [licence](LICENSE-MaChAmp.txt). The three delivered source files contain laboratory modifications described above; original file bytes and any existing attribution are retained. Project-created scripts retain the repository's component-specific terms. No model weights, paid recruitment corpus or full upstream tree is included.

Other remaining limitations include native Kompetencer/NNOSE launch/configuration coverage, complete upstream bindings, historical JobBERT/runtime records and restricted expanded-pool inputs. The Qwen generator is separately recovered from server A. This audit ran no training, inference, paid API, aggregation or rescoring.
