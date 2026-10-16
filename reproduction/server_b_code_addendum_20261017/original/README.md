# Server B code addendum (2026-10-17)

Original-byte copies from DS210039 for the items still listed as missing in
`reproduction/code_release_20261017/README.md` after commit
`edb45cdebfdcf2fdeb72341abc6f3155a246d7dd`.

This pack is source and local project dependencies only. It does not contain
weights, MacroData, silver jsonl, or full Slurm logs. Files were copied with
`cp -a`; they were not rewritten. `train_jobbert_ext.py` (fresh-head) is
intentionally absent.

## JobBERT continuation — delivered

| File | Role | SHA-256 |
|---|---|---|
| `jobbert_continuation/scripts/phase4_v6_jobbert.sbatch` | Slurm 7340 launcher | `8cbf25d707cf62b53c0bd4a4214dd6f1295c661e2da90df5b4f7164e83ec4c8b` |
| `jobbert_continuation/scripts/run_phase4_v6_jobbert12.sh` | Train/infer/score wrapper | `d2a5227d8fcb76c60ef8f49d4bb4c4a1c9d087a09e39b197abb1f47b1d47dc13` |
| `jobbert_continuation/scripts/train_jobbert_phase1.py` | Inherited-head CRF continue | `004add6d138c9de87c782f5c58958bc4800c060b3fe3770e1f074b8a737fe6ff` |
| `jobbert_continuation/scripts/infer_jobbert_phase1.py` | Gold150 decode | `899940316ccc47a3adca5114c2851f95aca5b84fae285647dc776563b1ec3b98` |
| `jobbert_continuation/scripts/eval_gold150_phase1.py` | `cnss-lskt-1.2.0` score | `5bf78bac792746a4d2b62d968e270c5d2c5fd20123d6339d0361b13b8340c868` |

Project-owned dependencies copied with them:

- `scripts/train_cn_roberta_crf.py` (`BertCRF`)
- `scripts/wait_idle_gpu_pair.sh` (sbatch GPU bind)
- `scorer/score_lskt.py`
- `pytorch-crf/torchcrf/__init__.py` (`pytorch-crf==0.7.2`)

Run binding (Table B drop44 B2 seed42): `evidence/drop44_b2_seed42_run_config.json`
(2156-row train path; `--init_pt` …/`crf/best.pt`; epochs 6, patience 2, batch 16,
lr 2e-5). Log citations and SHA-256: `evidence/LOG_CITATIONS.json`.
Host in `slurm_7340.head25.txt`: DS210039, Slurm 7340, 2026-09-08, GPUs 2,3.

## Qwen no-adapter paired baseline — 本次未找到

Original generation entry that wrote
`gold150_shared_prompt_rev2_run_20260910` with `adapter: null` was **not**
found on this host. Pairing documents only are in `qwen_no_adapter/`.
See `qwen_no_adapter/NOT_FOUND.md`. Expected on DS209213 (jobs 50966/50967).

## Native SkillSpan / Gnehm configs and patches — delivered

Files under `native_patches/` are the B-side originals that were **not** in
the published table11 `code/` tree (`run_remaining_today.py` stays in that
archive; it is not re-exported here).

Includes `machamp_sampler_torch214.patch`, `COMPATIBILITY.md`, ESCOXLM-R and
Gnehm native configs, and the B launchers `native_skillspan_jobbert_smoke.sbatch`,
`gnehm_esco_2gpu.sbatch`, `finish_today_2gpu.sbatch`.

Upstream MaChAmp / SkillSpan trees and native data are not in this pack.
Byte identity with the server-final executed MaChAmp tree is **not** claimed
beyond these copied patch/config files.

## Historical environment records — partial

| File | What it records |
|---|---|
| `env_records/ENV_RECORD.txt` | DS210039, 2026-09-21, Chinese/common encoder venv (Python 3.10.21, torch 2.14.0+cu130, RTX PRO 6000 Blackwell) |
| `env_records/requirements-common.txt` | Same venv pin file |
| `env_records/qwen_json_offset_seed42_RESOURCE.json` | JSON-offset P0 (Slurm 7349), not shared-handbook |

JobBERT continuation Python/torch/CUDA at execution time: still **本次未找到**
in `train.log`. A present-day query of `adasparse` must not be written as the
2026-09-08 stack. Kompetencer/NNOSE original launch/config coverage remains
incomplete on B.

## Checks run for this pack

- Five named JobBERT files: SHA-256 equal to the live server originals.
- `infer_gold150_sft.py` and `train_jobbert_ext.py` not packed.
- No training, inference, paid API, or rescoring.

Use `SHA256SUMS` after copy. Merge into the public tree at
`reproduction/code_release_20261017/` without substituting rewritten files.
