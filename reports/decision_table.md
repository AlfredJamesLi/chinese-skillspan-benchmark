# Decision table — round 2 (freeze deferred)

Do not start large reruns. Do not overwrite dumps. Do not edit PDF numbers.  
Gold is **not frozen** (18 annotation conflicts held out).

| Item | Decision | Why |
|---|---|---|
| Protocol freeze | **Deferred** | Canonical Gold exists but 18 IDs need adjudication |
| Raw Gold | **Do not edit** `admin_Baseline_test.jsonl` | 2676 rows / 2601 IDs; extra 75 because one ID is triple |
| Canonical Gold v1 | **Score with this; not public freeze** | 2583 unique IDs; SHA256 `458c9147…e5df` |
| 3237 ∪ 2676 as one test | **Forbidden** | Distinguish 3237 test / 2676 raw Gold rows / 2583 canonical |
| ChatGPT 0.6700 | **Not reproduced** | Official collapsed micro **0.6351** on 2029 uniquely matched IDs (554 duplicate pred IDs); delta −0.0349. Previous 0.665 used v1.1 global-set bug |
| DeepSeek dump | **Rescore only** | Official align **passes** (extras allowed). Typed micro 0.132 / collapsed 0.356 vs paper 0.513. Not for Table 3 until Gold frozen |
| JobBERT 0.46 | **Reject** | v1.1 global-set bug. Unique-view collapsed micro **0.00448** / **0.00373** ≈ paper 0.0045 / 0.0038 |
| JobBERT paper 0.0045/0.0038 | **Keep as ballpark** | Not a 100× error. Do not replace with 0.46 |
| Claude / Kimi | **Do not fill this round** | Missing 98 / 293 Gold IDs; official fails |
| Qwen 0.2130 | **Unreproducible** | Canonical collapsed micro 0.108; do not tune toward 0.2130 |
| Table 3 PDF | **Do not update** | No row `eligible_for_main_table` |
| Posting-level split rebuild | **Not required** | 0 cross-split `global_id`. Sentence-level exact dups exist (67 groups) |
| Encoder 3-seed baselines | **Not this round** | After Gold adjudication; order: MacBERT/BERT → XLM-R → span → IAA 300 → Claude/Kimi fill |
| Concept Accuracy / OOD claims | **Delete from draft later** | No concept IDs; no year field |
