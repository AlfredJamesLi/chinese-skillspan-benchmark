# Do not write into the Chinese-SkillSpan Overleaf paper

- IEEE Access / SRICL (arXiv `2604.21525`) method, tables, or `B8`/`A1`–`A4` as this paper’s system
- English six-dataset main table (SkillSpan / Kompetencer / Green / FIJO / Sayfullina / Gnehm)
- Any F1 not on the uploaded PDF and not in `confirmed-results.md`
- RAG-2 as ESCO ID linking
- Guessed sample sizes when the two processed `chinese_skillspan` trees disagree
- Concept Accuracy / ESCO concept-ID eval (no concept IDs in Gold)
- Time-OOD (no `year` field)
- listed-company mix **3M** DAPT (1M already lost: 0.1201 &lt; 0.1224)
- Domain-mix 1M JobBERT F1 (corpus ready, **not scored**)
- Encoder 3-seed **mean** (seeds 123/2026 still running)
- Claude/Kimi Gold v2 rows as complete (missing 98 / 293 IDs)
- English JobBERT ~0.46 or `*.eval_ner.json`
- Claiming JobBERT-zh CRF (~0.12) beats ChatGPT
