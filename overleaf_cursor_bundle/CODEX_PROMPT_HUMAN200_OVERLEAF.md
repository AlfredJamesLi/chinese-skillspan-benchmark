# Codex / Overleaf — paste this file (human-200 + overlay)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**GitHub (numbers + files, commit on `main`):** https://github.com/AlfredJamesLi/chinese-skillspan-benchmark  

Copy into the Overleaf repo root if missing:

- this file
- `tables/human200_page1_scores.csv`
- `tables/hybrid_human200_overlay_scores.csv`
- `tex/human200_page1_supplement.tex`
- `tex/hybrid_human200_overlay.tex`
- `.cursor/skills/cnss-overleaf/confirmed-results.md`
- `.cursor/skills/cnss-overleaf/not-for-paper.md`

Then paste **PROMPT** below. **Do not commit or push** from the Overleaf chat.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper for **PeerJ Computer Science**. This is **not** IEEE Access / SRICL / DASFAA.

1. `git pull --ff-only`. Confirm this is the Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md`, `handbooks/handbook_B_sop_v4.en.md`, `.cursor/skills/cnss-overleaf/confirmed-results.md`, `.cursor/skills/cnss-overleaf/not-for-paper.md`.
3. Patch Methods (short) + **two appendix/supplement tables**. You may `\input` `tex/human200_page1_supplement.tex` and `tex/hybrid_human200_overlay.tex` if those files are in the project.
4. Show the full `git diff`. **Do not commit. Do not push.**

### Hard rules

- Venue: **PeerJ Computer Science**. No DASFAA.
- **Do not change the abstract / main-table SOTA.** JobBERT 3M v4 typed exact stays **0.4331**; ChatGPT (`gpt-4o`) dump+jieba exact **0.2854** / relaxed **0.6249**.
- **Do not** write overlay JobBERT **0.3884** or n=200 JobBERT **0.1271** into the abstract.
- **Do not** overwrite Gold v2 or replace the V4 hybrid 2601 file as the reported main gold.
- **Do not** rank 0.4331, 0.3884, 0.2772, or Gold v2 ChatGPT **0.6365** in one SOTA sentence.
- Round to 4 decimals. Do not invent F1.
- Delete Concept Accuracy / Time-OOD / ESCO concept-ID claims if still present.
- If the title/abstract still calls V4 hybrid “human-annotated Gold”, rewrite to **derived SOP+jieba evaluation gold** (980 SimHuman + 1621 SOP-CWS). The 200 human labels are a **partial** check, not the 2601 main gold.

### What the authors did (do not invent more)

They labeled the **first 200** sentences of the 980 three-model disagreement queue (all 人工智能招聘; mixed annotators Maple / admin / James1; **not** dual-blind IAA). 57/200 sentences still have QA flags (mid-word cuts, swallowed list digits, long spans). Scorer `cnss-lskt-1.2.0`.

They then **put those 200 labels back onto the same IDs** inside the V4 hybrid test gold and jieba-snapped those 200. Resulting diagnostic gold = 200 human + 780 still SimHuman + 1621 SOP-CWS. Original hybrid file unchanged.

When the remaining 780 are labeled, **rescore** 2601. Encoder **re-finetuning is not required** unless training silver is also changed (980 IDs are test-only; do not train on them).

Historical Table 2 IAA (n=100, exact 0.532 / κ 0.554) stays Handbook A / Gold-length.

### Appendix table A — n=200 only (人工智能招聘)

CSV: `tables/human200_page1_scores.csv`. Caption must say n=200, not the main 2601 table. Claude is **matched-only** (45 missing dump IDs).

| System | n | P | R | Exact F1 | Relaxed F1 |
|---|---:|---:|---:|---:|---:|
| ChatGPT (`gpt-4o`) | 200 | 0.2381 | 0.3317 | **0.2772** | **0.4013** |
| Claude (haiku, matched) | 155 | 0.2267 | 0.2553 | 0.2402 | 0.3874 |
| Kimi (`kimi-k2-0711-preview`) | 200 | 0.1652 | 0.1908 | 0.1771 | 0.2280 |
| JobBERT 1M CWS retrain | 200 | 0.1961 | 0.1247 | 0.1524 | 0.3689 |
| JobBERT 3M v4 | 200 | 0.1586 | 0.1060 | 0.1271 | 0.3498 |
| JobBERT 1M v4 | 200 | 0.1391 | 0.0935 | 0.1119 | 0.3729 |
| DeepSeek (`deepseek-r1`) | 200 | 0.0964 | 0.1060 | 0.1010 | 0.1520 |
| Qwen (`Qwen2.5-14B-Instruct`) | 200 | 0.1854 | 0.0474 | 0.0755 | 0.1271 |

Agreement on the **same 200 IDs** (not systems): Gold v2 exact **0.3960** / relaxed 0.5086; V4 hybrid exact **0.1617** / relaxed 0.4147. Allowed: span convention still moves the number.

### Appendix table B — overlay on full test 2601

CSV: `tables/hybrid_human200_overlay_scores.csv`. Caption must say diagnostic overlay; 200 IDs human / 780 SimHuman; **not** the reported main gold.

| System | Orig exact | Overlay exact | Overlay relaxed |
|---|---:|---:|---:|
| JobBERT 3M v4 | **0.4331** | 0.3884 | 0.5469 |
| JobBERT 1M v4 | 0.4272 | 0.3811 | 0.5560 |
| JobBERT 1M CWS retrain | 0.4049 | 0.3688 | 0.5501 |
| ChatGPT (`gpt-4o`) | 0.2854 | 0.2929 | 0.5902 |
| Claude (98 empty-fill) | 0.1483 | 0.1586 | 0.3346 |
| Kimi (293 empty-fill) | 0.0964 | 0.1094 | 0.1984 |
| DeepSeek | 0.0802 | 0.0860 | 0.1594 |
| Qwen | 0.0501 | 0.0546 | 0.1385 |

Allowed one sentence: replacing 200/2601 SimHuman IDs with this human tranche lowers JobBERT-zh exact by about 0.045 and slightly raises frozen ChatGPT exact; JobBERT still leads exact, ChatGPT still leads relaxed.

### Methods + data availability (short)

- File `human_gold_page1_200.jsonl` (sha256 `fcecb522fbdf6571caaaa02c592b6ba4a552c4a9cfa52a0ed1f36b0fe9617490`).
- Overlay diagnostic file `test_lskt_v4_hybrid_human200_cws.jsonl` (sha256 `4d4a9e980760534d9157aa1465a47f1faed85e9b1572e8e7cdec1c59e945ef03`); original hybrid sha256 `2ad6342d…818d99` unchanged.
- 780 further 980-queue sentences to be released after submission at ~100/day. Do not promise a finished 980 Gold.

Do not add XLM-R, GlobalPointer, or Concept Accuracy. Do not start new experiments.
