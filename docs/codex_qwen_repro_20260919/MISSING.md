# Missing / withheld items

## Withheld on purpose

- Full `Qwen2.5-14B-Instruct` weight shards (not copied).
- Access keys, private sessions, unrelated Slurm stdout/stderr logs.
- Expanded-Silver sentence jsonl and advertisement wording (public authorization still pending).
- Adapter `dev_pred.jsonl` / `dev_gold.jsonl` (Silver-dev text).
- A Hugging Face **git commit** for `Qwen/Qwen2.5-14B-Instruct`. Original `MODEL_PROVENANCE.json` recorded **local file SHA256s**, not a Hub revision. Those hashes are in `BASE_MODEL.json`. Do not use today's `main`.

## Not found as a separate adapter tree

- Table H **7117 TVT** Gold150 **0.5732**: the exported 7,117 tree is the full-dev run (Gold150 exact 0.5883306320907618). No second adapter directory for the TVT cell was packed.

## Recorded but incomplete

- Pool **torch / transformers** versions were not written into `run_config.json`. Only `peft_version` `0.20.0` is inside those `adapter_config.json` files. Do not fill gaps from a later environment.
- PEFT `adapter_config.json` `"revision": null` for every packed adapter.

## Verification limits

- Offline `eval_gold150_ext.py --protocol shared_prompt` on frozen 150-row predictions **matched** the paper F1s (`offline_score_receipt.json`).
- This pack did **not** reload the base model or re-generate predictions. Inventory SHA256 pass ≠ re-inference verification.
