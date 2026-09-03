# Codex / Overleaf — Human page-1 200 (edit this pass)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**This file is the edit paste for the 200-sentence human analysis set (2026-09-03).**  
Do **not** re-run `CODEX_PROMPT_ALL.md` from scratch. Patch Methods + a **supplement/appendix table only**. **Do not commit or push.**

Copy `tables/human200_page1_scores.csv` and this prompt into the Overleaf repo if missing. Numbers only from the table below (also in `confirmed-results.md`).

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper for **PeerJ Computer Science**. This is **not** IEEE Access / SRICL.

`git pull --ff-only`. Read `HANDOVER_OVERLEAF.md`, `handbooks/handbook_B_sop_v4.en.md`, `.cursor/skills/cnss-overleaf/confirmed-results.md`, `.cursor/skills/cnss-overleaf/not-for-paper.md`. Then patch tex. Show the full diff. **Do not commit.**

### Hard rules

- Venue remains **PeerJ Computer Science**. No DASFAA.
- **Do not change the abstract SOTA.** JobBERT 3M v4 typed exact stays **0.4331**; ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**.
- **Do not overwrite or relabel** Gold v2. Do **not** replace the V4 hybrid 2601 test gold with these 200 sentences.
- **Do not** rank n=200 F1 against 0.4331 or Gold v2 ChatGPT **0.6365** in one SOTA sentence.
- These 200 are the **first page of the 980 disagreement queue**, all **人工智能招聘**. Mixed annotators (Maple / admin / James1). **Not** dual-blind IAA. Historical Table 2 (n=100, exact 0.532 / κ 0.554) stays Gold-era / Handbook A.
- 57/200 sentences have residual QA flags (mid-word cuts such as 培训其, swallowed list digits, spans >14 characters, ability verbs marked). Write them as a **human analysis set / first release**, not “clean Handbook B Gold”.
- 780 sentences remain. After submission the authors will release **100 more per day** on GitHub. One sentence in Data Availability / Limitations is enough; do not promise a finished 980 Gold.
- Delete Concept Accuracy / Time-OOD / ESCO concept-ID claims if still present.
- Round to 4 decimals. Do not invent F1.

### What to add

1. **Methods (short).** A first tranche of 200 sentences from the 980 three-model disagreement queue was labeled by human annotators (character offsets; L/K/S/T). IDs are a subset of the same 2601 Gold v2 / V4 hybrid IDs. File: `human_gold_page1_200.jsonl`. Scorer `cnss-lskt-1.2.0`. This tranche does **not** replace the V4 hybrid main gold.

2. **Appendix or Supplemental table** (caption must say n=200, 人工智能招聘 only, not the main 2601 table):

| System | n | typed exact P | R | F1 | typed relaxed F1 |
|---|---:|---:|---:|---:|---:|
| ChatGPT (`gpt-4o`, frozen dump) | 200 | 0.2381 | 0.3317 | **0.2772** | **0.4013** |
| Claude (`claude-3-5-haiku-20241022`) | 155/200 | 0.2267 | 0.2553 | 0.2402 | 0.3874 |
| Kimi (`kimi-k2-0711-preview`) | 200 | 0.1652 | 0.1908 | 0.1771 | 0.2280 |
| JobBERT 1M CWS retrain + frozen | 200 | 0.1961 | 0.1247 | 0.1524 | 0.3689 |
| JobBERT 3M v4 frozen | 200 | 0.1586 | 0.1060 | 0.1271 | 0.3498 |
| JobBERT 1M v4 frozen | 200 | 0.1391 | 0.0935 | 0.1119 | 0.3729 |
| DeepSeek (`deepseek-r1`) | 200 | 0.0964 | 0.1060 | 0.1010 | 0.1520 |
| Qwen (`Qwen2.5-14B-Instruct`) | 200 | 0.1854 | 0.0474 | 0.0755 | 0.1271 |

Claude is **matched-only** (45 gold IDs missing in the haiku dump). Do not empty-fill that row into a complete-200 claim.

3. **Agreement rows** (same table footnote or a second mini-table; these are **not** systems):

| Reference on the same 200 IDs | typed exact F1 | typed relaxed F1 |
|---|---:|---:|
| Gold v2 (Handbook A spans) | 0.3960 | 0.5086 |
| V4 hybrid (SOP+jieba / SimHuman) | 0.1617 | 0.4147 |

Allowed claim: the new human tranche disagrees with both existing references (exact 0.3960 vs Gold v2; 0.1617 vs V4 hybrid). This is evidence that **span convention still moves the number**, not that JobBERT “lost” to ChatGPT on the main V4 table.

4. **Data availability.** State that `human_gold_page1_200.jsonl` (200 IDs, sha256 `fcecb522fbdf6571caaaa02c592b6ba4a552c4a9cfa52a0ed1f36b0fe9617490`) will be in the public/Zenodo pack; 780 further 980-queue sentences to be released after submission at ~100/day.

5. If the title/abstract still calls V4 hybrid “human-annotated Gold”, rewrite to **derived SOP+jieba evaluation gold** (980 SimHuman + 1621 SOP-CWS). The 200 human labels are a **partial** human check, not the 2601 main gold.

Do not add XLM-R, GlobalPointer, or Concept Accuracy. Do not start new experiments.
