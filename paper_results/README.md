# Paper results index

Consolidated results for **Chinese-SkillSpan / DASFAA 2026**. Numbers in `paper/` come from the uploaded PDF (plus 2026-08-22 legacy rescore notes). Numbers in `repo/` use **Gold v2** (`gold_canonical_v2.jsonl`) and scorer `cnss-lskt-1.2.0`.

## Layout

| Path | Contents |
|---|---|
| `manifest.json` | Master index and file pointers |
| `paper/` | PDF Table 1–3 (confirmed paper numbers) |
| `repo/` | Repo rescores on canonical Gold v2 + encoder runs |
| `pending/placeholders.json` | Reserved slots for incomplete / future experiments (`metrics: null`) |
| `../results_snapshots/` | Per-run `run_summary` JSON copies |
| `../reports/` | Full audit CSVs, score dumps, IAA worksheets |

## Encoder leaderboard (Gold v2 test typed F1)

| Run | F1 |
|---|---:|
| `jobbert_zh_3m/crf_ckpt65000_ep1` | 0.1233 |
| `jobbert_zh_3m_ckpt_sweep/crf_ckpt65000` | 0.1233 |
| `jobbert_zh_1m/crf_v3_seed42` | 0.1224 |
| `jobbert_1m_human380_v3merge_seed42` | 0.1207 |
| `jobbert_zh_listed_1m/crf_v3_seed42` | 0.1201 |
| `jobbert_zh_3m/crf_v3_seed42` | 0.1170 |
| `jobbert_zh_3m_ckpt_sweep/crf_ckpt100000` | 0.1167 |
| `cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42` | 0.1156 |
| `jobbert_zh_demo/crf_v3_seed42` | 0.1152 |
| `cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42` | 0.0238 |
| `cn_roberta_wwm_crf/smoke_seed42_gpu1` | 0.0120 |
| `cn_roberta_wwm_crf/smoke_goldstyle_seed42` | 0.0000 |

## Pending (empty until filled)

See `pending/placeholders.json` — includes relaxed F1, concept accuracy, OOD splits, Claude/Kimi fill, human IAA-300, listed-3M (skipped), hybrid LLM ablations.

Do **not** copy internal encoder numbers into the PDF Table 3 without protocol sign-off (`notes/DATA_PROTOCOL_FREEZE.md`).
