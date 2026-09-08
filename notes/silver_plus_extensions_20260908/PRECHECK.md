# Silver-plus extensions precheck (server B)

**方案更正（2026-09-08 下午）：** 本轮 Qwen **只做 SFT**。此前含 KNN / 随机示例 A/B/C 的草案已替代，见 `SUPERSEDED_KNN_ABC.md`。作业 7349 未中断；其已启动的 42/43 SFT 继续作为正式三 seed 中的两个。

Host: `DS210039` / 144.214.210.39. Workspace: `/home/guojingli3/Chinese-Skillspan-Benchmark`.  
New output root: `Chinese_skill_benchmark_Paper/output/silver_plus_extensions/`.  
Existing v3–v6a/v6b runs, Gold150, and frozen CRF dirs were not overwritten.

## 1. Slurm and GPU (not guessed)

Checked on 2026-09-08 with `sinfo`, `scontrol show partition LocalQ`, `squeue`, `nvidia-smi`.

| Item | Observation |
|---|---|
| Default partition | `LocalQ*` up, 1 node `localhost`, `gres/gpu=8`, time unlimited |
| TRES | `cpu=512, mem=1547466M, gres/gpu=8` |
| GPU write-up | Past lab jobs on this node omit `--gres=gpu` because LocalQ can pin busy cards |
| Cards | 8× NVIDIA RTX PRO 6000 Blackwell, 97887 MiB each |
| Occupied at check | GPU 0–1: ~17 GB, 99%, Slurm job **7322** `qwen3_14b_lora` user `boluzhan`, `gres/gpu:2` |
| Idle | GPU 2–7 (~0–3 MiB) |
| This chain cap | **2 GPUs at once**; do not kill 7322; do not hard-code physical 2/3 |

Qwen2.5-14B-Instruct BF16 + LoRA r=16 fits one 96 GB card. Two seeds run as two independent 1-GPU processes. Three seeds = two parallel + one leftover. DDP only if a single run needs two cards (not expected here).

Scheduler `CUDA_VISIBLE_DEVICES` is respected. New picker: any two idle cards among 0–7 (`scripts/wait_idle_gpus.sh`), not the old 0+1 / 2+3-only helper.

## 2. Data freeze

v6a on disk matches the reported 2156 / 169.

| Field | Value |
|---|---|
| v6a train / unique NFC / dup extras | 2156 / 1911 / 245 (mean weight 1.1282) |
| v6a cohort records | A100=96, H730=637, E1621=1423 |
| v6a empty-span train | 875 |
| Frozen Gold150 SHA256 | `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` (match) |
| Hold-82 in train | 0 |
| Train/dev exact NFC vs Gold150 | 0 |

Isolation wording for same-document different sentences remains **句级隔离扩展版**. Do not call it 文档隔离.

Pending labels are not converted to empty negatives. The unreleased 82 are not appended.

Gold150 is not used for train, early stop, prompt debug, or parameter choice. Dev is not in the train set. A leftover `knn_index/` was built before the SFT-only correction; it is not used for official Gold.

## 3. Three short cross-split strings

These are **whole-sentence** NFC copies, not extracted fragments. They remain in v6a. Punctuation/template fragments are not automatic leaks, but whole-sentence copies must not cross train/dev/test.

1. `']` — train `1945-s0010`, `1950-s0004`, `1959-s0011`, `1960-s0025` / dev `1954-s0007`
2. `。` — train `1898-s0015` / dev `1843-s0009`
3. NFC `关注公众号马克数据网` (surface has spaces) — train `1873-s0012` / dev `1843-s0010`

**New list (v6a files untouched):** `data/v6a_nocross_20260908/`  
Train 2156→2150 (drop the six train IDs above). Dev 169 unchanged. Unique NFC 1911→1908.  
All new trains use this list.

## 4. JobBERT start point — independence fails

Released 3M CRF `Baseline_Models_Collection/jobbert-zh/crf/best.pt`  
SHA256 `d98814cb954036f885e1247c2c50c66adbc5a280750f0228bfc3df077f2fc98c`.  
README: V4 silver CRF on encoder `encoder_ckpt65000`. **No `history.json` / selection manifest.**  
Encoder SHA256 `ed2130f680d0aa9691d081a516963da252449746ef7e78818050e3039b6ccf3b` is the DAPT file.

New JobBERT claims will **not** inherit that CRF. H/E/M uses the DAPT encoder + **re-initialized** task head/CRF.  
1M encoder hash matches the Hub README (`7fd83053…bed57`), but 1M vs 3M are different DAPT recipes (1M×3 epochs vs 3M `ckpt65000`), and the 1M CRF also lacks selection history. **1M official 6-run block is skipped** (not a pure scale ablation). This does not block Qwen.

## 5. Qwen path — identity passes

`/home/guojingli3/IEEE_Access_project/models/Qwen2.5-14B-Instruct`  
README title: Qwen2.5-14B-Instruct, 14.7B, 48 layers. `config.json`: `qwen2`, `Qwen2ForCausalLM`, hidden 5120. Eight shards, **no adapter in that directory**. Read-only. New adapters stay under `silver_plus_extensions/`. Not 15B. Directory name is not the sole evidence.

## 6. Qwen method boundary

This round does **not** import SpanAnchor / SRICL modules. It reuses this project's JSON-offset LoRA SFT. IEEE Access adapters are not loaded. Directory location in another project does not disqualify the Instruct base weights after config / shard / no-adapter checks.

## 7. Go / no-go

| Branch | Decision |
|---|---|
| Qwen 14B SFT ×3 + Gold ×3 | **Go** (protocol frozen: parser 13/13, LoRA reused, no Gold peek) |
| KNN / random A/B/C | **Not official** (superseded) |
| JobBERT3M H/E/M | **Go**, encoder + reinit CRF only |
| JobBERT1M × B1/B2 × 3 seeds | **Skip** (DAPT stages not comparable; CRF history missing) |
| Old 17460 relabel | **Not run** |
