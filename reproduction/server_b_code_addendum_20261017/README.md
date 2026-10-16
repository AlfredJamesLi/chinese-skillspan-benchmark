# Server B source addendum: audited integration

This adds the supplied server-B source files to the previously published code materials. Read this audited integration note before the original server README: the latter describes the exporter’s intent, while local inspection found a stale manifest entry and a truncated patch.

## Delivered and remaining items

| Item | Verified contents | Limit |
|---|---|---|
| JobBERT continuation | Five original entry files, general BertCRF implementation, scorer, GPU-selection helper, CRF dependency, seed42 run configuration and Slurm excerpt | Source delivery is complete for these local dependencies. No training rerun, historical runtime lock, full-log verification or complete-input release is claimed. |
| Qwen no-adapter baseline | Frozen prompt, user template, parser and pairing notes | Original generator remains absent. The notes identify DS209213 jobs 50966/50967. Their score line still says pending verification; this release does not revalidate it. |
| Native SkillSpan/Gnehm | B-side configs, launchers and compatibility notes | `machamp_sampler_torch214.patch` is truncated: `git apply --stat` reports corrupt patch at line 41. Do not apply it. Complete native source/revision binding and other task launch/config coverage remain incomplete. |
| Historical environment | 2026-09-21 encoder environment record and JSON-offset Qwen resource record | These are not the JobBERT 2026-09-08 environment or the Qwen shared-guideline baseline environment. |

The five JobBERT files are in [original/jobbert_continuation/scripts](original/jobbert_continuation/scripts): `phase4_v6_jobbert.sbatch`, `run_phase4_v6_jobbert12.sh`, `train_jobbert_phase1.py`, `infer_jobbert_phase1.py`, and `eval_gold150_phase1.py`. The trainer loads an existing CRF checkpoint through `--init_pt`; it is not the fresh-head comparison script. The retained run configuration uses epochs 6, patience 2, batch size 16, max length 256, learning rate 2e-5 and seed 42. The 2,156-record JobBERT training split must not be replaced with the 2,150-record Qwen/encoder split.

## How to use the recovered JobBERT entry points

These are historical files with hard-coded laboratory paths, preserved without rewriting. Review paths before execution. In a separate working copy, map the two historical roots (`/home/guojingli3/SCESC-LLM-skill-extraction` and `/home/guojingli3/Chinese-Skillspan-Benchmark`) to your local project, or explicitly configure imports and pass local input paths. Historical paths inserted by the scripts must not resolve to unrelated older modules.

For direct execution, set `JB` to the absolute path of `original/jobbert_continuation`, and put `$JB/scripts`, `$JB/scorer` and `$JB/pytorch-crf` on `PYTHONPATH`. Use the matching PyTorch, Transformers and NumPy environment; their original JobBERT execution-time versions remain unrecorded. The September encoder pin file is not a JobBERT lockfile.

1. Obtain the matching initialization model and inherited CRF `best.pt`, and authorized train/dev inputs. The project [data-access guide](../../DATA_AVAILABILITY.md) describes current access limits. The release model links do not alone prove the exact initialization file's historical bytes.
2. Run `train_jobbert_phase1.py` with `--model_dir`, `--init_pt`, `--train`, `--dev`, a new `--out_dir`, and the recorded hyperparameters. Check the emitted `missing`/`unexpected` checkpoint-key lists: historical loading uses `strict=False`, so successful loading alone is not proof of a matching checkpoint. Development data select the checkpoint; Gold150 is not read by this continuation trainer.
3. Run `infer_jobbert_phase1.py` with `--model_dir`, `--ckpt <out_dir>/best.pt`, `--input <matching-reference.jsonl>`, `--out <new-prediction.jsonl>`, `--batch_size 16`, `--max_len 256`.
4. Run `eval_gold150_phase1.py` with `--gold`, `--pred` and `--out`; it imports the bundled historical scorer. Existing frozen predictions and the current repository scorer remain unchanged.

The Slurm/wrapper files retain the historical 12-run grid and server GPU/Conda paths. Do not submit them unchanged on another machine. The native launchers additionally require `run_remaining_today.py` from the pinned B-side archive, native upstream trees and datasets. They also call `emit_verified_results.py` for optional post-run aggregation; that helper is absent from this ZIP and the inspected pinned archive, so this part remains unresolved. The call is guarded with `|| true`, but it must not be represented as delivered. The one-epoch SkillSpan launcher is a smoke test, not the full reported run. See the [previous code inventory](../code_release_20261017/README.md) for archive links.

## Integrity, provenance and packaging discrepancy

Input ZIP SHA-256: `590257396882743dd359ca7e57b1ef432c014f946489ced7f7559ea3961db6a6`.

All 40 entries in the incoming `SHA256SUMS` verify. The original `MANIFEST.json` lists 40 other files, but its size/hash for `SHA256SUMS` are stale (4,655 bytes recorded versus 4,737 supplied). The other 39 entries match. There are 41 files including the manifest itself. This is a packaging-metadata discrepancy, not evidence of changed training scripts. Both original metadata files are preserved. [AUDIT.json](AUDIT.json) records freshly computed checksums for all 41 received files.

The exporter reports copying live server originals. Local checks establish identity to the supplied ZIP and agreement with its checksums, not independent access to that server or proof that today's source bytes were those executed in September. Full logs listed in `LOG_CITATIONS.json` were not provided; only the included excerpt/configuration were inspected.

Seven Python files pass AST syntax parsing. This audit did not run models, training, inference, paid APIs or prediction rescoring. Existing experimental outputs are unchanged. See [third-party notices](THIRD_PARTY_NOTICES.md) and the [current release scope](../code_release_20261017_1/README.md).
