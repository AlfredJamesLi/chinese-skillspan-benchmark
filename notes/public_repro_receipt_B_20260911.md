# Independent public-repro receipt — server B

Date: 2026-09-11. Host: **DS210039**. Check ran on a detached Git worktree of https://github.com/AlfredJamesLi/chinese-skillspan-benchmark at **`09897d9`**. No commit, no push, no retag `v0.1.3`. Hybrid gold and `data/gold150_test.jsonl` were not rewritten.

Python: `/home/guojingli3/miniconda3/envs/adasparse/bin/python3` (not A’s `/opt/anaconda3/envs/adasparse`). jieba **0.42.1**.

The laboratory path `$WORK/Chinese_skill_benchmark_Paper` on B is **not** a git checkout. Commands below used `_verify_origin_main` at `09897d9`. Branch `gold150-followups-20260909` on the local clone was left in place.

Paper-main cell remains V4 hybrid JobBERT 3M typed exact **0.4331**. JSON-offset empty-pred F1 **0.0** is not a paper cell and is not shared-prompt SFT (**0.5403±0.0354**).

## P0

| Check | Result |
|---|---|
| `python3 scorer/test_regression.py` | exit 0 (parent-repo dumps SKIP, still OK) |
| Frozen 3M, no jieba | typed exact **0.255237** (`cnss-lskt-1.2.0`, `alignment_ok`) |
| `--paper-main-only --use-frozen` | JobBERT_3M_v4 **0.433118** / relaxed **0.587322**; ChatGPT **0.285361** / relaxed **0.624869** |
| Hybrid SHA-256 | `2ad6342d8b762cf1abb289295315e2521bec0c540f4320113409fceab0818d99` |
| Gold150 freeze SHA-256 | `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` |

## P2

| Check | Result |
|---|---|
| `convert_gold150_to_bio.py` | n=150, n_with_spans=142; freeze SHA unchanged |
| `test_qwen_ext_parser.py` | 13/13 pass; `protocol=json_offset` |
| `eval_gold150_ext.py --protocol json_offset` (all-O pred) | complete_150; typed exact **0.0** (connectivity only) |

## P1 (optional smoke)

Not skipped. GPU 1 idle. torch `2.10.0+cu130` already present. Did **not** install `requirements-train.txt`. Used existing laboratory `pytorch-crf` on `PYTHONPATH`. `--out_dir output/p1_crf_smoke_B` (no `/tmp`).

Hub load `AlfredJames/jobbert-zh`. 16/8/8 rows, 1 epoch, scorer skipped. `dev_typed_f1=0.0`. **Not** a paper F1. Bitwise match to 0.4331 is **not** claimed.

## Not done

No Qwen train, no LoRA publish, no 6-epoch CRF, no `backup_push_github.sh`.
