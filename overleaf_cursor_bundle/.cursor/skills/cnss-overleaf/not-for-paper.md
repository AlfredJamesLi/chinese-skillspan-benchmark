# Do not write into the Chinese-SkillSpan paper

## Other paper (keep out)

- IEEE Access / SRICL method paper (arXiv `2604.21525`)
- Writing DASFAA 2026 as this paper’s submission venue (target is **PeerJ Computer Science**)
- English SkillSpan / Green / FIJO / Sayfullina / Gnehm / Kompetencer main tables
- Access experiment ids `B8`, `A1`–`A4` as if they were this paper’s method
- Claiming RAG-2 outputs ESCO skill IDs
- Agent / tool-calling as the reported method of *this* benchmark paper (unless the uploaded PDF already does)

## Unverified

- Any F1 not in `confirmed-results.md` and not on the user-uploaded PDF
- Internal encoder summaries that were not scored with this paper’s official script
- Numbers from the *other* processed copy of `chinese_skillspan` if the two trees differ
- RoBERTa-wwm v3 3-seed **mean is 0.1199** (0.1156 / 0.1187 / 0.1254); do not leave `---`
- Replacing the 4-encoder **3-seed** ranking (JobBERT 1M **0.1288**) with the JobBERT 1M **5-seed** mean **0.1257**; 5-seed is 1M-only and slightly lower because seed 13 is 0.1192
- Claiming domain-mix 1M beats JobBERT 1M on the 3-seed mean (0.1269 < 0.1288)
- Claiming domain-mix fixes 事业单位 (seed 42 typed F1 0.0287 vs ChatGPT 0.7032)
- Presenting the original Claude unique-first dump (missing 98) as a complete Gold v2 row; use `Claude_filled_v2.jsonl` (haiku+sonnet-4-6 mix)
- Presenting the original Kimi unique-first dump (missing 293) as complete; use `Kimi_filled_v2.jsonl`
- listed-company mix **3M** DAPT (1M already lost: 0.1201 < 0.1224)
- Concept Accuracy / ESCO concept-ID eval (no concept IDs in Gold)
- Time-OOD (no `year` field)
- English JobBERT ~0.46 or `*.eval_ner.json`
- Claiming JobBERT-zh CRF (~0.12, or SOP-silver 0.3170, or CWS post-hoc 0.1454) beats ChatGPT **on Gold v2**
- Putting SOP-silver 0.3170 / 0.5663, both-sides CWS ~0.43, or jieba post-hoc 0.1454/0.1479 into PDF Table 3, the Gold v2 unique-first LLM table, or the abstract SOTA sentence (those rows belong only in the labeled diagnostic tables in `confirmed-results.md`)
- Claiming JobBERT-zh 0.4272/0.4331 on SOP-CWS+SimHuman980 jieba bilateral beats ChatGPT 0.6365 on Gold v2 (different span conventions; V4 is paper main, Gold v2 is appendix)
- Calling the V4 hybrid “human Doccano Gold”, overwriting `gold_canonical_v2.jsonl`, treating the 980 SimHuman overlay as a full human SOP pass, or claiming Table 2 IAA measures V4 spans
- Merging Handbook A and Handbook B into one guideline, or claiming Handbook A reprints the original `prompt_template_rag.py` silver API (that API used minimal sufficient span and put language certificates in L)
- Putting gpt-5.4 SOP-extract 0.2338 (n=100) or 0.2132 (n=2601), kimi-k2.6 0.1979, claude-sonnet-4-5 0.1972, Qwen Instruct SOP 0.1724, or deepseek-v4-pro n=46 0.2353 into PDF Table 3, Gold v2 unique-first, or the matched-protocol **main** 2601 frozen-dump table
- Mixing n=100 gpt-5.4 0.2338 with n=2601 0.2132, or claiming Qwen SOP Gold-v2 diagnostic 0.2134 reproduces paper Qwen S-F1 0.2130
- Replacing Table 3 / Gold v2 dump ids (`gpt-4o`, `claude-3-5-haiku-20241022`, `kimi-k2-0711-preview`) with gpt-5.4 / sonnet-4-5 / kimi-k2.6
- Incomplete SOP runs (Llama 98/2601, sonnet-4-6 128/2601, deepseek-v4-pro 700/2601) or un-scored Qwen SOP LoRA as paper F1
- Putting STL combined **0.4100** into the abstract / main V4 table (it does not beat JobBERT 1M v4 **0.4272**); mixing STL with SkillSpan nested SKILL/KNOWLEDGE STL/MTL F1; using an STL head’s Gold-v2 trainer micro as if it were joint 0.1224
- Promoting **repartition_v1** silver-draft F1 (RoBERTa-wwm 3-seed mean **0.3070**, best seed **0.3115**, Qwen SOP **0.1473**, STL combined **0.2905**) into the abstract or as a replacement for V4 hybrid JobBERT 3M **0.4331**. New test gold is LSKT v4 character silver, not human Doccano Gold. Do not rank 0.3115 against 0.4331 or 0.6365.
- Putting server-B vanilla WWM v4 seed-42 exact **0.4341** (base) / **0.4289** (large) into the abstract or as a replacement for JobBERT 3M **0.4331**, or claiming vanilla “beats JobBERT” (Δ ~0.001, 待验证). Factory large did not help (B−A = −0.0052). Do not start large 3-seed or large DAPT from the auto-appended “discuss 1M DAPT” clause.
- Putting human page-1 **n=200** F1 (ChatGPT exact **0.2772**, JobBERT 3M v4 **0.1271**, Gold v2 agreement **0.3960**, V4 hybrid agreement **0.1617**) into the abstract or as a replacement for V4 hybrid 2601 JobBERT 3M **0.4331**. Do not rank 0.1271 against 0.4331 or 0.6365. Do not call the 200 “clean Handbook B Gold” or V4 dual-blind IAA (57/200 QA-flagged; mixed annotators). Claude **0.2402** is matched-only (n=155). Do not overwrite `gold_canonical_v2.jsonl` or the V4 hybrid 2601 file with this tranche.

## Abandoned / mix-ups

- Access “do not use Chinese data in Table II” notes (those constrain the *other* paper only)
- Treating `prompt_template_zh.py` as the reported prompt (unused by current silver scripts; reported prompt is `prompt_template_rag.py` → `chinese_skillspan` unless PDF says otherwise)
