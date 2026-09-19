# License notice — do not treat this pack as CC-BY

This directory is a **reproduction export of existing Qwen experiments**. It is not a new public grant on every file. Do not label the whole pack CC-BY-4.0.

## 1. Software copied from the public clone (Apache-2.0)

`eval_runtime/scripts/` (including `eval_gold150_ext.py`, `cnss_paths.py`, `convert_gold150_to_bio.py`) and `eval_runtime/scorer/score_lskt.py` follow the software section of `third_party/chinese-skillspan-benchmark.LICENSE` (Apache License 2.0). That grant **does not** re-license job-advertisement wording, Silver labels, or LoRA adapters.

Original B2 / pool train and infer scripts under `shared_guidelines_b2/scripts/` and `expanded_silver/*/scripts/` are laboratory copies of the code that actually ran. They are provided so loading is not reverse-engineered from a paper table. They are **not** a new CC-BY grant.

## 2. Qwen2.5-14B-Instruct (base model) — Apache-2.0 as recorded on the local snapshot

Hugging Face repo ID recorded in the original provenance: `Qwen/Qwen2.5-14B-Instruct`.

The local snapshot used for training (server A path for B2; server B IEEE path for expanded-silver pools) carries `LICENSE` = Apache License 2.0. A copy is `third_party/Qwen2.5-14B-Instruct.LICENSE`. The README YAML of that snapshot also says `license: apache-2.0`.

**Base weights are not in this pack.** File SHA256s of the snapshot that actually trained the adapters are in `BASE_MODEL.json` / `shared_guidelines_b2/configs/MODEL_PROVENANCE.json`. Do not substitute today's Hugging Face `main`.

Adapters are LoRA residuals trained on that base. Using them requires a matching base under the Qwen/Tongyi terms recorded above, plus whatever rights you have to the adapters themselves.

## 3. LoRA adapters — no blanket public licence in this export

`adapter_model.safetensors` / `adapter_config.json` are author-trained artifacts for paper reproduction. PEFT may have written `license: apache-2.0` into a generated `README.md` beside some adapters; **that generated stub is not an author grant covering the adapter weights or the training data.**

Author authorization for public redistribution of these adapters (Zenodo or otherwise) must be recorded separately. This export does not invent that grant.

## 4. Gold150 freeze and frozen predictions

`protocol/gold150_test.jsonl` is the public human-reference freeze (SHA256 `ca8db0bc…`). Frozen `pred_for_score.jsonl` files are model outputs on that freeze, including empty predictions. They are released here for offline scoring of **already-run** inference, not as a CC-BY grant on advertisement wording.

## 5. B2 Silver (2,150 / 169) — already public; not re-licensed here

Train/dev sentence files are **not copied** into this pack. Hashes are in `shared_guidelines_b2/configs/DATA_MANIFEST.json`. Public bytes live in the clone as `data/silver_plus_v6a_nocross/train_b2.jsonl` and `dev_b2.jsonl` under the dataset terms of the public repository notice (academic research use; **not** CC-BY on original advertisement wording).

## 6. Expanded Silver pools (9,646 / 9,540 and optional Table H subsets)

Full Silver jsonl and advertisement wording are **not copied**. Public authorization of those texts is still pending. This pack only includes split ID lists, file SHA256s, configs, adapters, and Gold150 frozen predictions.

## 7. Secrets and logs

Access keys, private chat transcripts, and unrelated training stdout/stderr logs are omitted on purpose.
