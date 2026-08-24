# Gold duplicate audit

Raw file: `/home/guojingli3/SCESC-LLM-skill-extraction/chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl`  
SHA256: `103e400c79eb3954d0857e7000b4388773622fda6a333e72be7720bf27f5e172`

Raw Gold was **not** modified. This file does not uniqueify or drop rows.

## Arithmetic (2676 rows vs 2601 unique IDs vs 74 duplicate IDs)

| Quantity | Value |
|---|---:|
| Raw rows | 2676 |
| Unique IDs | 2601 |
| Extra rows (`rows − unique IDs`) | **75** |
| IDs with count ≥ 2 | **74** |
| IDs with count = 1 | 2527 |
| IDs with count = 2 | 73 |
| IDs with count = 3 | **1** |
| IDs with count ≥ 4 | 0 |

If every duplicated ID appeared exactly twice, extra rows would equal 74.  
Extra rows are 75, so one ID contributes one additional copy:

`73 × (2−1) + 1 × (3−1) = 73 + 2 = 75`.

The triple ID is **`1989-s0001`**, raw lines `2293|2299|2300`. Same text, same posting (`global_id=1989`), **two distinct LSKT label sets** → classified as `annotation_conflict`, not an exact duplicate.

## Classification of the 74 duplicated IDs

| Class | n | Rule |
|---|---:|---|
| exact_duplicate | 56 | same ID, same text, same L/K/S/T spans |
| annotation_conflict | 18 | same ID, same text, **different** labels |
| id_collision | 0 | same ID, different text |
| other | 0 | |

All 74 duplicated IDs are the same recruitment posting as their copies (`same_posting=1`). No ID collisions.

Full per-ID table: `reports/gold_duplicate_audit.csv` (ID, occurrence count, raw line numbers, text/label/posting identity, class, suggested action).

### Annotation-conflict IDs (held out of canonical Gold)

`1987-s0045`, `1987-s0059`, `1988-s0026`, `1988-s0027`, `1988-s0063`, `1988-s0085`, `1988-s0107`, `1988-s0113`, `1988-s0154`, `1988-s0161`, `1989-s0001` (triple), `1989-s0023`, `1991-s0006`, `1991-s0033`, `1991-s0042`, `1995-s0036`, `1995-s0037`, `1999-s0072`.

These 18 IDs are **37 raw rows** (17×2 + 1×3). They are not auto-merged.
