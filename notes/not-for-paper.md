# Do not write into the Chinese-SkillSpan paper

## Other paper (keep out)

- IEEE Access / SRICL method paper (arXiv `2604.21525`)
- English SkillSpan / Green / FIJO / Sayfullina / Gnehm / Kompetencer main tables
- Access experiment ids `B8`, `A1`–`A4` as if they were this paper’s method
- Claiming RAG-2 outputs ESCO skill IDs
- Agent / tool-calling as the reported method of *this* benchmark paper (unless the uploaded PDF already does)

## Unverified

- Any F1 not in `confirmed-results.md` and not on the user-uploaded PDF
- Internal encoder summaries that were not scored with this paper’s official script
- Numbers from the *other* processed copy of `chinese_skillspan` if the two trees differ
- RoBERTa-wwm v3 3-seed **mean** (seed 123 running; seed 2026 not started)
- Claiming domain-mix 1M beats JobBERT 1M on the 3-seed mean (0.1269 < 0.1288)
- Claiming domain-mix fixes 事业单位 (seed 42 typed F1 0.0287 vs ChatGPT 0.7032)
- Claude/Kimi Gold v2 rows as complete (missing 98 / 293 IDs)
- listed-company mix **3M** DAPT (1M already lost: 0.1201 < 0.1224)
- Concept Accuracy / ESCO concept-ID eval (no concept IDs in Gold)
- Time-OOD (no `year` field)
- English JobBERT ~0.46 or `*.eval_ner.json`
- Claiming JobBERT-zh CRF (~0.12) beats ChatGPT
- LSKT v4 SOP sandbox F1 (rule-silver typed exact ~0.3170 / IoU≥0.5 ~0.5663; 1M CRF). Not Gold v2. Not Table 3.

## Abandoned / mix-ups

- Access “do not use Chinese data in Table II” notes (those constrain the *other* paper only)
- Treating `prompt_template_zh.py` as the reported prompt (unused by current silver scripts; reported prompt is `prompt_template_rag.py` → `chinese_skillspan` unless PDF says otherwise)
