# Jieba-bilateral benchmark eval (SOP-CWS + SimHuman 980)

**Protocol (reproducible):** both predictions and test gold are jieba-snapped (`cws_snap.rewrite_record`, userdict, cap=8). Scorer `cnss-lskt-1.2.0`, official, `n_boot=0`. Missing Gold IDs filled as empty preds so every system is scored on all 2601 IDs.

**Test gold (full):** `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`  
n=2601 = **980 SimHuman rule_v4** jieba-snapped + **1621 SOP-CWS**. sha256 `2ad6342d…818d99`.  
**980 subset:** `data/test_lskt_v4_simhuman980_cws.jsonl` sha256 `05765161…adec1580`.

Does **not** overwrite Gold v2. This is a matched SOP/jieba test gold, not human Doccano Gold. Script: `scripts/eval_hybrid_cws_simhuman.py`. CSV: `tables/hybrid_cws_simhuman980_all_models.csv`.

## Full test n=2601 (primary for this protocol)

| Model | typed exact P / R / F1 | typed relaxed F1 |
|---|---|---|
| **JobBERT 3M v4 + jieba** | 0.4730 / 0.3994 / **0.4331** | **0.5873** |
| **JobBERT 1M v4 + jieba** | 0.4685 / 0.3925 / **0.4272** | **0.5952** |
| JobBERT 1M CWS retrain + jieba | 0.4537 / 0.3655 / 0.4049 | 0.5904 |
| JobBERT 1M goldstyle v3 (3-seed mean) | — / — / **0.3032** | **0.5332** |
| domain-mix 1M (3-seed mean) | — / — / 0.3037 | 0.5278 |
| JobBERT 3M ckpt65000 (3-seed mean) | — / — / 0.2961 | 0.5278 |
| listed-mix 1M | — / — / 0.2964 | 0.5267 |
| JobBERT demo 80k | — / — / 0.2931 | 0.5321 |
| RoBERTa-wwm v3 (3-seed mean) | — / — / 0.2875 | 0.5206 |
| ChatGPT (`gpt-4o`, old dump, complete) | 0.2371 / 0.3584 / **0.2854** | **0.6249** |
| Claude (`claude-3-5-haiku-20241022`, old dump, 98 empty) | 0.1149 / 0.2090 / **0.1483** | **0.3349** |
| Kimi (`kimi-k2-0711-preview`, old dump, 293 empty) | 0.0862 / 0.1093 / **0.0964** | **0.1997** |
| DeepSeek (`deepseek-r1`, old dump, complete) | 0.0682 / 0.0974 / 0.0802 | 0.1577 |
| Qwen (`Qwen2.5-14B-Instruct`, old dump, complete) | 0.0999 / 0.0334 / 0.0501 | 0.1409 |
| JobBERT-skill (EN head) | 0.0071 / 0.0150 / 0.0096 | 0.0676 |
| JobBERT-knowledge (EN head) | 0.0064 / 0.0138 / 0.0088 | 0.0644 |

## SimHuman 980 only (same protocol)

| Model | typed exact F1 | typed relaxed F1 |
|---|---|---|
| JobBERT 3M v4 + jieba | **0.4401** | 0.6032 |
| JobBERT 1M v4 + jieba | **0.4333** | **0.6110** |
| JobBERT 1M CWS retrain | 0.4020 | 0.6084 |
| ChatGPT (`gpt-4o`, old dump, complete) | 0.2836 | 0.6447 |
| Claude (`claude-3-5-haiku-20241022`, 45/980 empty) | 0.1757 | 0.4062 |
| Kimi (`kimi-k2-0711-preview`, 160/980 empty) | 0.1011 | 0.2183 |
| DeepSeek (`deepseek-r1`, old dump, complete) | 0.0738 | 0.1573 |
| Qwen (`Qwen2.5-14B-Instruct`, old dump, complete) | 0.0483 | 0.1361 |

980 vs full 2601 for 1M/3M v4 differs by <0.01 exact. The 980 subset is a robustness check, not a second SOTA column.

## LLM old dumps vs missing (this pass: no API)

| Model | dump IDs | miss vs 2601 | miss in 980 | 2601 exact / relaxed |
|---|---:|---:|---:|---|
| ChatGPT (`gpt-4o`) | 2639 | 0 | 0 | 0.2854 / 0.6249 |
| Claude (`claude-3-5-haiku-20241022`) | 2536 | 98 | 45 | 0.1483 / 0.3349 |
| Kimi (`kimi-k2-0711-preview`) | 2341 | 293 | 160 | 0.0964 / 0.1997 |
| DeepSeek (`deepseek-r1`) | 2639 | 0 | 0 | 0.0802 / 0.1577 |
| Qwen (`Qwen2.5-14B-Instruct`) | 3237 | 0 | 0 | 0.0501 / 0.1409 |

Fill later (id + sentence only): `fill_later/missing_queue_Claude.jsonl` (98, all 人工智能招聘), `fill_later/missing_queue_Kimi.jsonl` (293 = 246 人工智能 + 47 阿里云). After fills, re-run `python scripts/eval_hybrid_llm_old_dumps.py` on merged views; do not overwrite original unique-first dumps.

## Caption for the paper

Matched-protocol test: LSKT v4 SOP silver + jieba CWS on both pred and gold. 980 sentences use SimHuman rule_v4 labels (then the same jieba snap); the other 1621 use SOP-CWS. Official human Gold remains `gold_canonical_v2.jsonl`. Do not compare these exact F1 numbers to ChatGPT 0.6365 on Gold v2.
