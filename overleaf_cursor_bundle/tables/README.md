# Overleaf table sources (Chinese-SkillSpan)

Copied from the server `Chinese_skill_benchmark_Paper/tables/` on 2026-08-24.
Round to **4 decimals** in tex. Do not invent cells.

| File | Use |
|---|---|
| `table3_paper_strict_sf1.json` | Keep PDF Table 3 paper S-F1 (Gold 2676) |
| `table3_gold_v2_unique_view.csv` | New Gold v2 unique-first typed/collapsed (2601 IDs) |
| `relaxed_f1_gold_v2.csv` | Typed relaxed F1, IoU≥0.5 |
| `per_domain_gold_v2.csv` | Industry-OOD **proxy** (source_domain) |
| `encoder_gold_v2.csv` | JobBERT-zh CRF ranking, seed 42 |

Authoritative rounding and captions: `.cursor/skills/cnss-overleaf/confirmed-results.md`.
