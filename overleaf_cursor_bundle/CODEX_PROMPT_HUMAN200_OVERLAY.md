# Codex / Overleaf — Human-200 overlay on V4 hybrid (edit)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
Paste **this file**. Do not replace the main V4 table. **Do not commit.**

Copy `tables/hybrid_human200_overlay_scores.csv` if needed. Numbers only from the table below.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan** Overleaf paper for **PeerJ Computer Science**. `git pull --ff-only`. Patch an **appendix / diagnostic table only**. Show the diff. **Do not commit.**

### Hard rules

- Abstract / main table stay V4 hybrid 2601: JobBERT 3M typed exact **0.4331**, ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**.
- **Do not** write overlay JobBERT **0.3884** into the abstract.
- **Do not** overwrite or rename the main gold file. The overlay is 200 human + 780 SimHuman + 1621 SOP-CWS.
- Do not rank 0.3884 against Gold v2 ChatGPT **0.6365**.
- Claude/Kimi rows remain incomplete (98 / 293 empty-fill).
- Round to 4 decimals. Do not invent F1.

### What happened

Authors labeled the first 200 of the 980 disagreement-queue sentences and **put those labels back onto the same 200 IDs** inside the V4 hybrid test gold, then jieba-snapped those 200 (same scorer `cnss-lskt-1.2.0`). Original hybrid file unchanged.

### Table to add (appendix)

Caption must say: diagnostic overlay, n=2601, 200 IDs human / 780 still SimHuman; not the reported main gold.

| System | orig exact | overlay exact | overlay relaxed |
|---|---:|---:|---:|
| JobBERT 3M v4 | 0.4331 | 0.3884 | 0.5469 |
| JobBERT 1M v4 | 0.4272 | 0.3811 | 0.5560 |
| JobBERT 1M CWS retrain | 0.4049 | 0.3688 | 0.5501 |
| ChatGPT (`gpt-4o`) | 0.2854 | 0.2929 | 0.5902 |
| Claude (98 empty) | 0.1483 | 0.1586 | 0.3346 |
| Kimi (293 empty) | 0.0964 | 0.1094 | 0.1984 |
| DeepSeek | 0.0802 | 0.0860 | 0.1594 |
| Qwen | 0.0501 | 0.0546 | 0.1385 |

Allowed one-sentence: replacing 200/2601 SimHuman IDs with this human tranche lowers JobBERT-zh exact by about 0.045 and slightly raises frozen ChatGPT exact; JobBERT still leads exact, ChatGPT still leads relaxed. When the remaining 780 are labeled, the 2601 table will be **rescored**; encoder **re-finetuning is not required** unless training silver is also changed (the 980 IDs are test-only).

Also keep the n=200-only analysis table from `CODEX_PROMPT_HUMAN200.md` if it is not already in the appendix.
