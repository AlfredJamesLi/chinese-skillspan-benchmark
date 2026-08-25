# Codex / local Cursor prompt — matched-protocol hybrid table

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
Paste **after** Gold v2 tables (`CODEX_PROMPT.md`), SOP methods (`CODEX_PROMPT_SOP_V4.md`), and the diagnostic encoder table (`CODEX_PROMPT_DIAGNOSTIC_SOP.md`). Server cannot log into Overleaf.

Copy into the Overleaf repo: this file, `.cursor/skills/cnss-overleaf/confirmed-results.md`, `.cursor/skills/cnss-overleaf/not-for-paper.md`, and `tables/hybrid_cws_simhuman980_all_models.csv`.

GitHub: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark  
Gold file: `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` (2601 = 980 SimHuman + 1621 SOP-CWS). Official human Gold remains `gold_canonical_v2.jsonl`.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper. This is **not** IEEE Access / SRICL (arXiv 2604.21525). Do not import English six-dataset tables or SRICL claims.

### Start
1. `git status`; `git pull --ff-only`; confirm this is the Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md`, `.cursor/skills/cnss-overleaf/confirmed-results.md`, `.cursor/skills/cnss-overleaf/not-for-paper.md` in full.
3. Add **one matched-protocol results table** (results section or appendix). Show the full `git diff`. **Do not commit or push.**

### Hard rules
- Write **only** numbers in `confirmed-results.md`. Round to 4 decimals. Do not invent F1.
- **Keep PDF Table 3 paper S-F1 cells unchanged** (ChatGPT 0.6700, Claude 0.6300, Kimi 0.5700, DeepSeek 0.5130, Qwen 0.2130, JobBERT-skill 0.0045, JobBERT-knowledge 0.0038).
- **Do not change Gold v2 unique-first cells** (ChatGPT typed exact **0.6365**, relaxed **0.7221**).
- **Do not** claim JobBERT-zh 0.4272 / 0.4331 beats ChatGPT 0.6365 — different test golds.
- **Do not** add gpt-5.4 (0.2338) or deepseek-v4-pro n=46 (0.2353) to this 2601 table, Table 3, Gold v2, or the abstract. Those are SOP-extract pilots only. Optional one-sentence footnote: new SOP extract re-calls of gpt-5.4 (n=100) and DeepSeek V4 Pro (n=46) did not raise hybrid exact vs the frozen ChatGPT dump on the same IDs.
- Caption must name: LSKT v4 SOP + jieba CWS on **both** pred and gold; 980 SimHuman rule_v4 overlay; 1621 SOP-CWS; scorer `cnss-lskt-1.2.0`; official human Gold remains Gold v2.
- LLM rows in this table are **frozen dumps jieba-snapped**, not a new GPT-4o API call. ChatGPT 0.2854 exact is span-convention drop, not a new model.

### Table to add (n=2601 primary; 980 is a robustness check)

Caption meaning (English matching the paper):  
Matched-protocol test gold: SOP-CWS with 980 SimHuman rule_v4 labels, jieba word-boundary snap on gold and predictions. Not human Doccano Gold v2. Typed exact / typed relaxed (IoU≥0.5) micro F1.

| Model | n=2601 exact | n=2601 relaxed | n=980 exact | n=980 relaxed |
|---|---:|---:|---:|---:|
| JobBERT 3M v4 + jieba | 0.4331 | 0.5873 | 0.4401 | 0.6032 |
| JobBERT 1M v4 + jieba | 0.4272 | 0.5952 | 0.4333 | 0.6110 |
| JobBERT 1M CWS retrain + jieba | 0.4049 | 0.5904 | 0.4020 | 0.6084 |
| domain-mix 1M (3-seed mean) | 0.3037 | 0.5278 | — | — |
| JobBERT 1M goldstyle v3 (3-seed mean) | 0.3032 | 0.5332 | — | — |
| listed-mix 1M | 0.2964 | 0.5267 | — | — |
| JobBERT 3M ckpt65000 (3-seed mean) | 0.2961 | 0.5278 | — | — |
| JobBERT demo 80k | 0.2931 | 0.5321 | — | — |
| RoBERTa-wwm v3 (3-seed mean) | 0.2875 | 0.5206 | — | — |
| ChatGPT (frozen dump + jieba) | 0.2854 | 0.6249 | 0.2836 | 0.6447 |
| Claude filled (haiku + sonnet-4-6) | 0.1519 | 0.3416 | 0.1778 | 0.4101 |
| Kimi filled | 0.1093 | 0.2321 | 0.1116 | 0.2514 |
| DeepSeek (frozen dump + jieba) | 0.0802 | 0.1577 | 0.0738 | 0.1573 |
| Qwen (frozen dump + jieba) | 0.0501 | 0.1409 | 0.0483 | 0.1361 |
| JobBERT-skill EN head | 0.0096 | 0.0676 | 0.0124 | 0.0919 |
| JobBERT-knowledge EN head | 0.0088 | 0.0644 | 0.0122 | 0.0862 |

Allowed discussion sentence: under this matched SOP+jieba gold, JobBERT-zh 1M/3M v4 lead typed exact (0.4272 / 0.4331); ChatGPT leads typed relaxed (0.6249). The 980 subset agrees with 2601 for 1M/3M (Δ exact < 0.01).

Optional short footnote (no extra F1 columns): SOP extract re-calls gpt-5.4 n=100 hybrid exact 0.2338 vs old dump 0.3356 on the same IDs; DeepSeek V4 Pro n=46 hybrid exact 0.2353 vs old dump 0.3648. Not expanded to 2601.

### After edits
List files touched, confirm Table 3 and Gold v2 ChatGPT 0.6365 were not changed, full diff. No commit.

## End prompt
