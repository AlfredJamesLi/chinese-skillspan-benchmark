# Label first, then train

Internal note only. **Not paper numbers.** Do not copy into `confirmed-results.md` or the PDF. Do not invent F1.

## Order

1. Fix train/dev **labels** to Gold granularity.
2. Inspect span-length and a handful of spans (this note + `goldstyle_v3_meta.json`).
3. Only then 1-seed smoke on the new files. No 3-seed. No train on Gold v2 test IDs. No overwrite of corpus `train.json` / Gold v2.

v1 took whole duty clauses (mean 34.8) → official typed exact 0.0.  
v2 tightened to punct (mean 11.4) → official typed exact 0.0238.  
Encoder dev F1 0.56–0.66 on both, so the head learns whatever it is given. Silver official typed exact ~0.012. Alignment was true. Those smoke F1 stay in `goldstyle_smoke_result.md` only.

## Target granularity

Gold complete NP, not mid-word fragments, **not** whole duty clauses.

| set | n spans | mean | median | p25 | p75 | p90 | share 4–12 | share >14 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Gold v2 | 6627 | 4.90 | 4 | 2 | 6 | 9 | 0.64 | 0.022 |
| silver train | 37911 | 5.16 | 5 | 3 | 6 | 8 | 0.64 | 0.009 |
| human80 lock | 89 | **17.90** | **16** | 10 | 26 | 31 | 0.33 | **0.55** |
| goldstyle v1 | 12588 | 34.76 | 27 | 19 | 39 | 59 | 0.08 | 0.87 |
| goldstyle v2 | 27972 | 11.37 | 11 | 8 | 15 | 16 | 0.58 | 0.29 |
| goldstyle v3 | 25401 | **6.71** | **5** | 3 | 11 | 13 | 0.57 | 0.002 |

Silver is already Gold-length but cut mid-word (`维护和` / `支持服`). v3 expands the fragment to a complete NP, stops at `，。；、` or 熟悉/掌握, splits 英语 / Python / 沟通, hard cap 13. It does **not** take the whole sentence.

## human80 vs Gold

human80 is **systematically longer** than Gold (mean 17.9 vs 4.9; 55% of human80 spans >14 tokens vs 2% of Gold). The 80 were annotated under the old “岗位职责整段可以标成一条 S” rule. **Do not silently rewrite `sample80_final.json`.** A later Gold-length pass on the 80 is optional if we want the lock to match Gold. rule_v3 vs human80 exact = **20/80** (v1 18/80, v2 16/80). Low agreement is expected while the lock stays long-clause.

Example spans (token length in parentheses):

- Gold: `沟通能力`(4 T), `虚拟化经验`(5 S), `英文读写能力`(6 L), `团队合作精神`(6 T), `AWS工作经验`(7 S), `飞控计算机`(5 S)
- Gold tail (rare): `多平台或关键应用程序的维护和支持服务`(18 S)
- human80: `本科及以上学历`(7 K) is Gold-like; `掌握图像滤波、…等各类图像处理理论`(36 K) and `负责事业部内云计算实施项目的管理工作，包括…`(43 S) are duty-clause
- v3 (cleaner rows): `主动性`(3 T), `团队协作能力`(6 T), `德语读写能力良好`(8 L), `普通话表达`(5 L after complete-word grow). First-file gym ads still have leftover junk (`求回当地工作的`); rule-only, not Gold.

Full percentiles and more examples: `goldstyle_v3_meta.json`.

## JobBERT-zh (Zhang et al., SkillSpan NAACL 2022)

**Later — not this round.** Zhang-faithful JobBERT is domain-adaptive MLM on **~3.2M unlabeled job-ad sentences**, then token-level SE. This repo has **no** 3.2M Chinese JD corpus. In-repo text is ~2000 postings / **~22.8k sentences** (train 17460 + dev 2143 + test 3237; `paragraph.jsonl` = 2000). That is two orders of magnitude too small to claim JobBERT-scale DAPT.

- Do **not** MLM on test (or Gold test IDs).
- Existing JobBERT numbers (~0.0045 skill / ~0.0038 knowledge) are **English JobBERT head-transfer onto Chinese BERT**, not Chinese DAPT. Keep that as the weak published baseline.
- After labels work, optional **small DAPT on train+dev text only** can be an ablation, not a JobBERT-zh claim.

## Recommended benchmark table (after labels look Gold-like)

1. Chinese RoBERTa-wwm / MacBERT + CRF (1-seed smoke, then 3-seed only if official typed exact is worth it)
2. Optional small DAPT on train+dev sentences only (ablation; say the size)
3. XLM-R + CRF
4. Span / GlobalPointer later
5. Existing LLM few-shot dumps (official scorer, unique Gold v2)
6. English JobBERT transfer — weak published baseline, not a Chinese DAPT result

Scorer: `cnss-lskt-1.2.0`. Gold: `Chinese_skill_benchmark_Paper/data/gold_canonical_v2.jsonl`. Primary: typed exact micro F1.

## v3 files (new only)

- `Chinese_skill_benchmark_Paper/scripts/rewrite_train_goldstyle_v3.py`
- `Chinese_skill_benchmark_Paper/data/train_goldstyle_v3.jsonl` (17460; 80 human80 + 17380 rule_v3)
- `Chinese_skill_benchmark_Paper/data/dev_goldstyle_v3.jsonl`
- `Chinese_skill_benchmark_Paper/reports/gold_style_relabel/goldstyle_v3_meta.json`

Did **not** start GPU. Mean 6.71 is in the ~5–8 Gold band and closer than v2, so a 1-seed is **ready if you confirm**. Prefer you trigger it.

## Ready 1-seed (only after you confirm)

Pick an empty GPU (`nvidia-smi`). Same protocol as v2 smoke. New out dir only.

```bash
ROOT=/home/guojingli3/SCESC-LLM-skill-extraction
PAPER=$ROOT/Chinese_skill_benchmark_Paper
OUT=$PAPER/output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42
mkdir -p "$OUT"
# set CUDA_VISIBLE_DEVICES to an empty GPU
setsid env CUDA_VISIBLE_DEVICES=0 \
  TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1 \
  PYTHONPATH="$ROOT/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}" \
  python3 "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed 42 \
    --train "$PAPER/data/train_goldstyle_v3.jsonl" \
    --dev "$PAPER/data/dev_goldstyle_v3.jsonl" \
    --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
    --gold "$PAPER/data/gold_canonical_v2.jsonl" \
    --out_dir "$OUT" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
  < /dev/null > "$OUT/nohup.out" 2>&1 &
```

Do not resume an old silver/v1/v2 out dir. Do not start 3-seed from this smoke.

## Next Doubao / Qwen batch (gateway cannot call external LLMs)

`expand_goldstyle_train.py` is for later API/local batches. It still injects the 80 lock and does not overwrite `train.json` / Gold v2. Update its system prompt to Gold-length (no “整段职责一条 S”) before a large batch.

```bash
# API (Doubao/Qwen) when a key+base are available — not on this gateway
GOLDSTYLE_BACKEND=api GOLDSTYLE_MODEL=<model> GOLDSTYLE_API_BASE=<base> \
  python3 Chinese_skill_benchmark_Paper/scripts/expand_goldstyle_train.py \
    --backend api --n 4000 --batch 8

# local Qwen2.5-14B on an empty GPU
GOLDSTYLE_BACKEND=local \
  python3 Chinese_skill_benchmark_Paper/scripts/expand_goldstyle_train.py \
    --backend local --n 4000 --batch 4 --limit 200
```

Human-review a slice before mixing LLM spans into a train file. Rule v3 is the current full-train stand-in.
