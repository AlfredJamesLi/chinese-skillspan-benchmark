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
- Claiming JobBERT-zh CRF (~0.12) beats ChatGPT
- LSKT v4 SOP sandbox encoder F1 (~0.3170 exact / ~0.5663 IoU≥0.5 on rule silver). Not Gold v2. Not Table 3.
