# Standardized-protocol annotation assets (v4.1)

Handbook version: **B.sop_v4.1**. Status of human Gold: **not frozen**.

| File | Role | Status |
|---|---|---|
| `notes/handbooks/handbook_B_sop_v4.md` | Canonical SOP (one page) | active |
| `notes/handbooks/handbook_B_overlap_adjudication.md` | Overlap / conflict-pair rules | active |
| `notes/handbooks/LSKT_V4_RULE_CHANGELOG.md` | Rule history | active |
| `prompts/LSKT_V4_ANNOTATION_PROMPT.txt` | LLM / annotator prompt (SHA in manifest) | active |
| `reports/human980_doccano/` | 980-queue Doccano pack (Gold v2 full text; SimHuman **draft** prelabel) | `draft` / pre-adjudication queue |
| `reports/annotation_v4/adjudication_log.csv` | Schema + empty log | empty; fill during labeling |
| `reports/annotation_v4/iaa/` | Dual-blind A/B | **missing** — do not invent |
| `data/gold_canonical_v2.jsonl` | Historical Doccano Gold (Handbook A) | `frozen` provenance; do not overwrite |
| `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | Paper main scoring file (SimHuman+SOP-CWS) | provisional standardized reference; **not** human-verified |

Do not put unadjudicated alternative spans into Gold. Do not reuse Table 2 n=100 as v4.1 IAA.
