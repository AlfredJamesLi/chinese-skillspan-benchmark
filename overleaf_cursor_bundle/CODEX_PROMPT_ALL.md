# Codex / Overleaf — ONE prompt (merged)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**Git:** `https://git.overleaf.com/68fe17a53e53a7f800e4f2b4`  
**GitHub numbers:** https://github.com/AlfredJamesLi/chinese-skillspan-benchmark  

Do **not** paste the four older files (`CODEX_PROMPT.md`, `CODEX_PROMPT_SOP_V4.md`, `CODEX_PROMPT_DIAGNOSTIC_SOP.md`, `CODEX_PROMPT_MATCHED_PROTOCOL.md`). Those were split only to keep early chats short. This file is the single paste.

First copy `overleaf_cursor_bundle/` into the Overleaf repo **root** (`HANDOVER_OVERLEAF.md`, `AGENTS.md`, `.cursor/`, `tables/`, this prompt).

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper for **PeerJ Computer Science** (dataset paper; LSKT span extraction on Chinese job ads). This is **not** the IEEE Access / SRICL method paper (arXiv 2604.21525). Do not import SkillSpan/Kompetencer/Green/FIJO/Sayfullina/Gnehm tables, SRICL, B8, or A1–A4.

**Venue (hard rule):** submission target is **PeerJ Computer Science**. Do **not** write DASFAA 2026 (or any DASFAA track) as the target venue in title, running header, footnotes, acknowledgements, or cover letter text. An older draft PDF filename still contains “DASFAA”; that is a file name only — retitle the tex to PeerJ CS. If the current document class is a conference template, report it and switch only if a PeerJ template is already in this Overleaf project; otherwise keep the class and change venue wording.

Overleaf: https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4

### Start
1. `git status`; `git pull --ff-only`; confirm this is the Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md`, `.cursor/skills/cnss-overleaf/confirmed-results.md`, `.cursor/skills/cnss-overleaf/not-for-paper.md` in full.
3. Locate `main.tex` (or equivalent) and current Tables 1/2/3.
4. Produce a **conflict table** first: file / current tex / confirmed value / action (`keep` / `add` / `patch wording` / `delete claim`).
5. Then patch methods + tables in **one pass**. Show the full `git diff`. **Do not commit or push.**

### Hard rules
- **Venue: PeerJ Computer Science.** Do not write DASFAA 2026 as the submission target.
- **LLM row labels must include dump model ids** (`tables/model_ids.csv`): ChatGPT=`gpt-4o`, Claude=`claude-3-5-haiku-20241022`, Kimi=`kimi-k2-0711-preview`, DeepSeek=`deepseek-r1`, Qwen=`Qwen2.5-14B-Instruct`. Do not use brand-only names in results tables.
- Write **only** numbers in `confirmed-results.md`. Round to 4 decimals. Do not invent F1.
- **Two test golds, never mixed in one SOTA sentence:**
  - **Official human Gold v2:** `gold_canonical_v2.jsonl`, 2601 IDs, scorer `cnss-lskt-1.2.0`, primary metric typed exact micro F1. ChatGPT **0.6365** typed / **0.7221** relaxed.
  - **Matched-protocol test gold (new benchmark for the SOP+jieba encoder story):** `test_lskt_v4_cws_simhuman980_hybrid.jsonl`, 2601 = 980 SimHuman rule_v4 jieba-snapped + 1621 SOP-CWS. Predictions jieba-snapped with the same snapper. JobBERT 1M/3M v4 **0.4272 / 0.4331** exact. **Not** comparable to ChatGPT 0.6365 on Gold v2.
- **Keep PDF Table 3 paper S-F1 cells unchanged** (ChatGPT 0.6700, Claude 0.6300, Kimi 0.5700, DeepSeek 0.5130, Qwen 0.2130, JobBERT-skill 0.0045, JobBERT-knowledge 0.0038). That table is the old published protocol (Gold 2676).
- Do **not** put diagnostic SOP-silver 0.3170 / both-sides ~0.43 / jieba-on-Gold-v2 0.1454 into Table 3, Gold v2 unique-first, or the abstract SOTA sentence.
- Do **not** add gpt-5.4 0.2338 or deepseek-v4-pro n=46 0.2353 to any 2601 table. Optional footnote only.
- Do **not** claim JobBERT-zh beats ChatGPT on Gold v2. Encoder on Gold v2 is a **weak baseline** (~0.13 typed).
- Delete or rewrite Concept Accuracy, Time-OOD, ESCO concept-ID linking. Allowed: “ESCO-derived LSKT span extraction”. Per-domain table is an Industry-OOD **proxy**.
- Qwen paper 0.2130 is unreproducible as Gold v2 typed 0.0791. Do not defend 0.2130 as Gold v2.
- listed-mix 1M lost (0.1201 vs 0.1224). Domain-mix 3-seed mean 0.1269 is **below** JobBERT 1M 0.1288. No listed-3M. No RoBERTa 3-seed mean (leave `---`).
- If tex, confirmed-results, and PDF disagree, stop and report. Do not average.

---

### Pipeline to write in Methods (this is the missing story — write it)

Add a short subsection (English, same register as the paper) that distinguishes **official Gold v2** from the **matched SOP+jieba protocol**. Do not replace Gold v2 as the official human gold.

**A. Operational SOP (LSKT v4), used for silver rewrite and for the new test gold**
- Labels stay L / K / S / T (flat, non-overlapping). Optional eval projection L+K→KNOWLEDGE, S+T→SKILL.
- Span = contiguous original substring; complete mention (no 半词 such as 支持服); prefer 2–8 tokens; do not tag a whole 岗位职责 clause as one S.
- 熟悉 / 掌握 / 精通 / 了解 mark **the object only**.
- 报名 / 体检 / 公示 / 福利 / 鸡汤 → empty sentence.
- English certificates such as 大学英语6级 → **K**; bare 英语/英文 → **L**. Programming languages and tools → **S**.

**B. New training (encoder fine-tune, not LLM SFT)**
1. Start from existing Chinese JobBERT-zh (RoBERTa-wwm-ext + JD MLM) + CRF.
2. **Official encoder track (already in the Gold v2 encoder table):** train silver = goldstyle v3 (rewrite toward Gold-length NPs). Best 3-seed typed exact on Gold v2: JobBERT 1M **0.1288**.
3. **New SOP track:** rewrite train silver with LSKT v4 SOP → `train_lskt_v4_silver`; fine-tune the same CRF on that silver (1M and 3M DAPT checkpoints). This is a **training-label change**, not a new architecture.
4. **Decode:** optional jieba word-boundary snap (`cws_snap.rewrite_record`, userdict, cap=8) at test time. A separate **CWS-retrain** run trains CRF on already-snapped silver; finished F1 is in the matched-protocol table (1M CWS retrain 0.4049 exact), **below** post-hoc jieba on v4 preds (0.4272).

**C. New testing (matched protocol)**
1. Do **not** overwrite Gold v2.
2. Build test gold on the same 2601 Gold v2 IDs: apply SOP/rule_v4 then jieba snap. Overlay **980** sentences with SimHuman rule_v4 labels (then the same jieba snap); the other **1621** stay SOP-CWS.
3. Snap **predictions** with the same jieba snapper so gold and pred share word boundaries (禁半词).
4. Score with `cnss-lskt-1.2.0`, official align, typed exact and typed relaxed (IoU≥0.5).
5. Frozen LLM dumps (ChatGPT/Claude/Kimi/DeepSeek/Qwen) are **not re-called** for this table; they are jieba-snapped after the fact. ChatGPT / DeepSeek / Qwen are complete. Claude misses 98 IDs and Kimi misses 293; those IDs are empty-filled until later. ChatGPT hybrid exact 0.2854 is a **span-convention** drop vs Gold v2 0.6365, not a new GPT-4o run.

**D. What stays official**
- Human Doccano Gold v2 remains the official gold. Matched-protocol numbers are a **separate** table / appendix.
- LLM SOP-extract **pilots** (gpt-5.4 n=100 hybrid exact 0.2338; DeepSeek V4 Pro n=46 hybrid exact 0.2353) stay a footnote only. Full-n SOP extract scores exist as **Table J** (diagnostic). They did **not** beat frozen ChatGPT P2 exact 0.2854 or JobBERT 3M v4 exact 0.4331. Official `gpt-4o` + the same SOP prompt is still missing.

---

### Tables

**A. Keep Table 1** — train 17460 / dev 2143 / test 3237. Footnote optional: raw Gold 2676 rows vs canonical unique Gold 2601.

**B. Keep Table 2 IAA** (n=100): strict F1 0.532; relaxed 0.624; κ 0.554.

**C. Keep PDF Table 3 paper S-F1** unchanged (old protocol Gold 2676). Relabel rows with dump ids; do not change paper S-F1 cells.

| Model | Paper S-F1 |
|---|---:|
| ChatGPT (`gpt-4o`) | 0.6700 |
| Claude (`claude-3-5-haiku-20241022`) | 0.6300 |
| Kimi (`kimi-k2-0711-preview`) | 0.5700 |
| DeepSeek (`deepseek-r1`) | 0.5130 |
| Qwen (`Qwen2.5-14B-Instruct`) | 0.2130 |
| JobBERT-skill | 0.0045 |
| JobBERT-knowledge | 0.0038 |

**D. Add Gold v2 unique-first** (official human gold; caption: Gold v2, unique-first, typed exact micro F1, `cnss-lskt-1.2.0`)

| Model | typed exact | collapsed exact | typed relaxed | note |
|---|---:|---:|---:|---|
| ChatGPT (`gpt-4o`) | 0.6365 | 0.6403 | 0.7221 | complete |
| Claude (`claude-3-5-haiku-20241022` + 98× `claude-sonnet-4-6`) | 0.2583 | 0.2970 | 0.3861 | haiku dump + 98 sonnet fills; original dump untouched |
| Kimi (`kimi-k2-0711-preview`) | 0.1651 | 0.3349 | 0.2130 | original dump missing 293 IDs |
| DeepSeek (`deepseek-r1`) | 0.1327 | 0.3569 | 0.1798 | complete |
| Qwen (`Qwen2.5-14B-Instruct`) | 0.0791 | 0.1075 | 0.1272 | complete; gap vs paper 0.2130 |
| JobBERT-skill | 0.0000 | 0.0045 | 0.0000 | EN head |
| JobBERT-knowledge | 0.0000 | 0.0037 | 0.0000 | EN head |

Keep ChatGPT as the strongest **complete** LLM under Gold v2. Encoder ~0.13 is a weak baseline on this gold.

**E. Add per-domain typed exact** (Gold v2; n=1407 / 457 / 737). Industry-OOD proxy, not Time-OOD.

| System | 人工智能招聘 | 阿里云 | 事业单位招聘 |
|---|---:|---:|---:|
| ChatGPT (`gpt-4o`) | 0.6489 | 0.5650 | 0.7032 |
| DeepSeek (`deepseek-r1`) | 0.1392 | 0.1293 | 0.0805 |
| Qwen (`Qwen2.5-14B-Instruct`) | 0.0887 | 0.0646 | 0.0207 |
| JobBERT 3M ckpt65000 | 0.1323 | 0.1259 | 0.0150 |
| JobBERT 1M | 0.1287 | 0.1332 | 0.0181 |
| listed mix 1M | 0.1282 | 0.1240 | 0.0153 |
| domain-mix 1M (seed 42) | 0.1276 | 0.1372 | 0.0287 |
| RoBERTa-wwm v3 | 0.1242 | 0.1191 | 0.0115 |

One sentence: encoder collapse on 事业单位 (~0.015–0.029) vs ChatGPT 0.7032.

**F. Add encoder ranking (Gold v2 typed exact, seed 42)**  
Best: domain-mix 1M **0.1234**; JobBERT 3M ckpt65000 **0.1233**; JobBERT 1M goldstyle **0.1224**; listed mix **0.1201**; RoBERTa-wwm v3 **0.1156**.

**G. Add encoder 3-seed (Gold v2 typed exact)**

| Run | 42 | 123 | 2026 | mean | std |
|---|---:|---:|---:|---:|---:|
| JobBERT 1M | 0.1224 | 0.1292 | 0.1348 | **0.1288** | 0.0062 |
| domain-mix 1M | 0.1234 | 0.1280 | 0.1294 | 0.1269 | 0.0031 |
| JobBERT 3M ckpt65000 | 0.1233 | 0.1295 | 0.1246 | 0.1258 | 0.0033 |
| RoBERTa-wwm v3 | 0.1156 | — | — | — | — |

**H. Add diagnostic SOP/jieba table** (appendix). Caption must name train silver, decode, and test gold. Official gold remains Gold v2.

| Pred | Train silver | Decode | Test gold | typed exact | IoU≥0.5 |
|---|---|---|---|---:|---:|
| JobBERT 1M | goldstyle v3 | raw | Gold v2 | 0.1224 | — |
| JobBERT 1M | SOP v4 | raw | Gold v2 | 0.1079 | 0.3320 |
| JobBERT 3M | SOP v4 | raw | Gold v2 | 0.1104 | 0.3404 |
| JobBERT 1M | SOP v4 | jieba post-hoc | Gold v2 | 0.1454 | 0.3411 |
| JobBERT 3M | SOP v4 | jieba post-hoc | Gold v2 | 0.1479 | 0.3470 |
| JobBERT 1M | SOP v4 | raw | SOP rule silver | 0.3170 | 0.5663 |
| JobBERT 3M | SOP v4 | raw | SOP rule silver | 0.3229 | 0.5624 |
| JobBERT 1M | SOP v4 | jieba post-hoc | SOP rule silver | 0.2609 | 0.5835 |
| JobBERT 1M | SOP v4 | jieba post-hoc | SOP-CWS silver | 0.4278 | 0.5960 |
| JobBERT 3M | SOP v4 | jieba post-hoc | SOP-CWS silver | 0.4341 | 0.5884 |

Discussion (two sentences): SOP v4 training **lowers** Gold v2 exact vs goldstyle (0.1079/0.1104 vs 0.1224). 0.3170 and ~0.43 are same-rule consistency, not official gold.

**I. Add matched-protocol table** (new benchmark results; results or appendix). Caption: SOP-CWS + 980 SimHuman, jieba on gold **and** pred, `cnss-lskt-1.2.0`. Not Doccano Gold v2. LLM rows = frozen dumps + jieba.

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
| ChatGPT (`gpt-4o`, frozen dump + jieba, complete) | 0.2854 | 0.6249 | 0.2836 | 0.6447 |
| Claude (`claude-3-5-haiku-20241022`, frozen dump + jieba, 98 empty) | 0.1483 | 0.3349 | 0.1757 | 0.4062 |
| Kimi (`kimi-k2-0711-preview`, frozen dump + jieba, 293 empty) | 0.0964 | 0.1997 | 0.1011 | 0.2183 |
| DeepSeek (`deepseek-r1`, frozen dump + jieba, complete) | 0.0802 | 0.1577 | 0.0738 | 0.1573 |
| Qwen (`Qwen2.5-14B-Instruct`, frozen dump + jieba, complete) | 0.0501 | 0.1409 | 0.0483 | 0.1361 |
| JobBERT-skill EN head | 0.0096 | 0.0676 | 0.0124 | 0.0919 |
| JobBERT-knowledge EN head | 0.0088 | 0.0644 | 0.0122 | 0.0862 |

Allowed sentence: under this matched gold, JobBERT-zh 1M/3M v4 lead typed exact (0.4272 / 0.4331); ChatGPT leads relaxed (0.6249). 980 vs 2601 Δ exact < 0.01 for 1M/3M v4. **Forbidden:** “beats ChatGPT 0.6365”.

Optional footnote: SOP extract **pilot** gpt-5.4 n=100 hybrid exact 0.2338 vs old dump 0.3356 on the same IDs; DeepSeek V4 Pro n=46 hybrid exact 0.2353 vs old dump 0.3648. The n=100 cell **0.2338 is not** the full-n number (full-n gpt-5.4 is **0.2132** in Table J).

**J. Add SOP extract diagnostic table** (appendix; **not** P2 main, **not** Table 3, **not** Gold v2 unique-first). Caption: same SOP extract v4 prompt, jieba snap, gold = matched-protocol hybrid 2601, scorer `cnss-lskt-1.2.0`. New models / new prompt. Do **not** replace `gpt-4o` / `deepseek-r1` dump rows.

| System | n=2601 exact | n=2601 relaxed | n=980 exact | n=980 relaxed |
|---|---:|---:|---:|---:|
| gpt-5.4 SOP extract | 0.2132 | 0.4199 | 0.2063 | 0.4207 |
| kimi-k2.6 SOP extract | 0.1979 | 0.4032 | 0.1912 | 0.4108 |
| deepseek-v4-pro SOP extract | 0.1980 | 0.3931 | 0.1847 | 0.3973 |
| claude-sonnet-4-5 SOP extract | 0.1972 | 0.3987 | 0.1861 | 0.3945 |
| Qwen2.5-14B-Instruct SOP extract (local, no LoRA) | 0.1724 | 0.3279 | 0.1711 | 0.3390 |
| Llama-3-8B-Instruct SOP extract (local, no LoRA) | 0.0582 | 0.1178 | 0.0544 | 0.1140 |
| ChatGPT (`gpt-4o`, frozen dump + jieba) | 0.2854 | 0.6249 | 0.2836 | 0.6447 |
| JobBERT 3M v4 + jieba | 0.4331 | 0.5873 | 0.4401 | 0.6032 |

Allowed sentence: SOP extract re-calls did not beat frozen ChatGPT P2 exact 0.2854 / relaxed 0.6249, and did not beat JobBERT 3M v4 exact 0.4331. Qwen SOP 0.1724 vs frozen Qwen dump 0.0501 is a **prompt** lift, not SFT. Do not write Qwen SOP-on-Gold-v2 0.2134 as paper Qwen 0.2130. Do not add Qwen LoRA (no test F1) or Claude Sonnet 4.6 (paused 460/2601).

CSV copies: `tables/model_ids.csv`, `tables/table3_gold_v2_unique_view.csv`, `tables/per_domain_gold_v2.csv`, `tables/encoder_gold_v2.csv`, `tables/encoder_3seed_gold_v2.csv`, `tables/sop_v4_cws_diagnostic.csv`, `tables/hybrid_cws_simhuman980_all_models.csv`, `tables/hybrid_cws_llm_old_dumps.csv`, `tables/sop_extract_p2_2601.csv`.

Mark Claude / Kimi as incomplete (empty-fill). Do not treat 0.1483 / 0.0964 as complete LLM rows. Do not use the later haiku+sonnet / Kimi_filled numbers in this table.

### Abstract / intro / conclusion
Patch only if they claim Concept Accuracy, Time-OOD, encoder SOTA on Gold v2, or ESCO ID linking. If you mention the new protocol, say it is a **matched SOP+jieba test gold**, not a replacement of human Gold v2.

### After edits
List files touched, conflict table, full diff. Confirm Table 3 paper S-F1 and Gold v2 ChatGPT 0.6365 were not changed. No commit.

## End prompt
