# Standardized-protocol annotation assets (v4.1)

Historical materials for handbook version **B.sop_v4.1**. The statuses below describe that annotation stage. Current handbook editions are listed in the [handbook directory](../../notes/handbooks/README.md). At this stage, the human reference labels had not been frozen.

| File | Role | Status |
|---|---|---|
| `notes/handbooks/handbook_B_sop_v4.md` | Canonical SOP (one page) | active |
| `notes/handbooks/handbook_B_overlap_adjudication.md` | Overlap / conflict-pair rules | active |
| `notes/handbooks/LSKT_V4_RULE_CHANGELOG.md` | Rule history | active |
| `prompts/LSKT_V4_ANNOTATION_PROMPT.txt` | LLM / annotator prompt (SHA in manifest) | active |
| `reports/human980_doccano/` | 980-queue Doccano pack (Gold v2 full text; SimHuman **draft** prelabel) | `draft` / pre-adjudication queue |
| `reports/annotation_v4/adjudication_log.csv` | Schema + empty log | empty; fill during labeling |
| `reports/annotation_v4/iaa/` | Dual-blind A/B | Not available at this stage |
| `data/gold_canonical_v2.jsonl` | Historical Doccano Gold (Handbook A) | `frozen` provenance; do not overwrite |
| `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | Paper main scoring file (SimHuman+SOP-CWS) | provisional standardized reference; **not** human-verified |

Alternative spans required review before inclusion in the reference labels. The earlier Table 2 analysis (n=100) used a different annotation design from v4.1.
