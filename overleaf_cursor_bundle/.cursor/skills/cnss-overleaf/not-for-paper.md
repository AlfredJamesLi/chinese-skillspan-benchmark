# Do not write into the Chinese-SkillSpan Overleaf paper

- IEEE Access / SRICL (arXiv `2604.21525`) method, tables, or `B8`/`A1`–`A4` as this paper’s system
- English six-dataset main table (SkillSpan / Kompetencer / Green / FIJO / Sayfullina / Gnehm)
- Any F1 not on the uploaded PDF and not in `confirmed-results.md`
- RAG-2 as ESCO ID linking
- Guessed sample sizes when the two processed `chinese_skillspan` trees disagree
- Concept Accuracy / ESCO concept-ID eval (no concept IDs in Gold)
- Time-OOD (no `year` field)
- listed-company mix **3M** DAPT (1M already lost: 0.1201 &lt; 0.1224)
- Claiming domain-mix 1M beats JobBERT 1M on the 3-seed mean (0.1269 &lt; 0.1288)
- RoBERTa-wwm v3 3-seed **mean** (seed 123 running; seed 2026 not started)
- Claiming domain-mix fixes 事业单位 (0.0287 vs ChatGPT 0.7032)
- Claude/Kimi Gold v2 rows as complete (missing 98 / 293 IDs)
- English JobBERT ~0.46 or `*.eval_ner.json`
- Claiming JobBERT-zh CRF (~0.12, SOP-silver 0.3170, or CWS post-hoc 0.1454) beats ChatGPT
- Putting SOP-silver 0.3170 / 0.5663, both-sides CWS ~0.43, or jieba post-hoc 0.1454/0.1479 into PDF Table 3, the Gold v2 unique-first LLM table, or the abstract SOTA sentence (diagnostic table only; see confirmed-results.md)
- Putting gpt-5.4 SOP-extract 0.2338 or deepseek-v4-pro n=46 0.2353 into Table 3, Gold v2 unique-first, or the matched-protocol 2601 LLM column
- Claiming JobBERT-zh 0.4272/0.4331 on matched-protocol gold beats ChatGPT 0.6365 on Gold v2
