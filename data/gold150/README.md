**Current 13 September mapping:** [paper names](../../PAPER_NAMES.md), [evaluation entry](../../reproduction/EVALUATION_ENTRY.md), and [current paper index](../../reproduction/PAPER_INDEX.md). The command below illustrates the historical JSON-offset path; the current shared-prompt and JobBERT paths are distinguished in the evaluation entry. Canonical files are unchanged.

# Human reference set (artifact Gold150)

Manuscript name (PeerJ CS under review, after Related Work): **human reference set** — 150 frozen evaluation sentences (challenge cohort + calibration cohort).

Repository identifier **Gold150** and filename `gold150_test.jsonl` are unchanged. Do not rename these files. Appendix D of the manuscript maps the two vocabularies.

Canonical scoring path: [`../gold150_test.jsonl`](../gold150_test.jsonl) (same bytes as `gold150_test.jsonl` in this folder).

| Paper name | n | File | SHA-256 | Laboratory alias |
|---|---:|---|---|---|
| Human reference set | 150 | `gold150_test.jsonl` | `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` | Gold150 |
| Challenge cohort | 100 | `gold100_locked.jsonl` | `a9fe43b79f58631876f00515f6a60649d8d2ceb57ebee111fe471cc70766864c` | Challenge-100 (`split=gold100_page1`) |
| Calibration cohort | 50 | `iaa50_gold_locked.copied.jsonl` | `68b47bdbad1622ca39d89a2dceaf8117ee44a2227272e901a7673bc676531686` | Audit-50 / IAA-50 (`split=iaa50`) |

Fields use `source_id` and Doccano `label` triples. This freeze is the **current manuscript evaluation**. It is **not** V4 hybrid 2,601 and **not** Gold v2. It is also **not** the historical 200-sentence analysis (`data/human_gold_page1_200.jsonl`). Do not overwrite `gold_canonical_v2.jsonl` or `test_lskt_v4_cws_simhuman980_hybrid.jsonl`.

Convert Doccano types to scorer BIO without rewriting the freeze:

```bash
python3 scripts/convert_gold150_to_bio.py
python3 scripts/eval_gold150_ext.py \
  --protocol json_offset \
  --pred path/to/predictions.jsonl \
  --out output/human_reference_score.json
```

JSON from `eval_gold150_ext.py` keeps the old keys (`gold150`, `challenge100`, `audit50`) and adds paper-name aliases (`human_reference`, `challenge_cohort`, `calibration_cohort`).

These files are the **current manuscript evaluation freeze** (0911 PeerJ draft). They are in GitHub Release / Zenodo **`v0.1.3`** (DOI `10.5281/zenodo.22698504`). They are **not** in Zenodo `v0.1.1` or `v0.1.2`. Teacher Silver-plus B2: [`../silver_plus_v6a_nocross/`](../silver_plus_v6a_nocross/). JobBERT-zh v6a B2 typed exact on this freeze is **0.5536±0.0054**. Do not rank that cell against V4 hybrid 2,601 JobBERT **0.4331**.

Appendix shared-guidelines LLM scores on this freeze (not the JobBERT current-eval cell): [`../../tables/gold150_shared_guidelines_rev2_patch1.csv`](../../tables/gold150_shared_guidelines_rev2_patch1.csv) and Qwen B2 LoRA [`../../tables/gold150_shared_guidelines_qwen_sft.csv`](../../tables/gold150_shared_guidelines_qwen_sft.csv). **gpt-5.6-terra** typed exact **0.6667** (n=150). Do not rank those cells against **0.5536** or **0.4331**. Do not rename SOP extract 0.2132.

