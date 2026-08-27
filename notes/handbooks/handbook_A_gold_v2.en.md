# Handbook A — Official human Gold v2 (P1), one page

**Use:** span convention for Doccano Gold v2. File: `gold_canonical_v2.jsonl` (2601 IDs; scorer `cnss-lskt-1.2.0`).  
**Do not use** for the matched SOP+jieba protocol (Handbook B).

**How Gold was made:** LLM silver from `prompt_template_rag.py` (`chinese_skillspan`; in-sentence `@@span##[L|K|S|T]`; *minimal sufficient span*) → light human check in Doccano. Do not rewrite this history or overwrite the Gold file.

## Labels (flat, non-overlapping)

| Tag | Meaning on Gold / goldstyle | Examples |
|---|---|---|
| L | language name | 英语, 普通话 |
| K | degree, major, **certificate**, domain knowledge | 计算机专业, **大学英语六级 / CET-6** |
| S | actionable skill, method, tool, experience | Python, 网络管理 |
| T | soft skill / trait | 沟通能力, 责任心 |

*Footnote:* the original silver API put language **certificates** in **L**. Gold-style and current Gold practice put them in **K**. Do not relabel Gold v2.

## Spans (Gold-length NPs)

Mark a **complete noun phrase**, typically 4–12 tokens (Gold median 4, mean ≈4.9). No mid-word cuts (`支持服`). Do not tag a whole duty clause as one S. Spans must be contiguous original text. Process / welfare / exam-admin sentences are **empty**. Encoder train silver `train_goldstyle_v3.jsonl` follows this boundary; it does **not** change Gold v2.

**Headline numbers (P1 only):** ChatGPT (`gpt-4o`) typed exact **0.6365**; JobBERT-zh 1M 3-seed **0.1288** (weak baseline).
