# Qwen LSKT SFT v1 prompt (design candidate)

Status: **trained as an appendix contrast (2026-09-09)**. Official Table C is still P0 **0.1215±0.0092**. Scores: [`paper_body_silver_plus.md`](paper_body_silver_plus.md) §6. Do **not** replace P0 with P1 $k=0$ 0.1455±0.0196.

Full prompt text (Chinese, model-facing): [`PROMPT_QWEN_LSKT_SFT_v1.txt`](qwen_lskt_sft_v1_prompt.txt).  
Optional kNN plan: [`qwen_sft_knn_optional_plan_20260909.md`](qwen_sft_knn_optional_plan_20260909.md).

P1 compresses `silver_plus_v4212_rev2` scope / type / boundary rules. It is not Handbook B, not SOP extract v4, and not a new authority over frozen B2 labels. Audit P1 against frozen train/dev labels before any run. Do not import v4.2.14 rulings or rewrite data to fit the prompt.

Edits versus the submitted draft:

1. Split **USER_K0** (no examples block) from **USER_WITH_EXAMPLES**. An empty `examples_json: []` is not used for official P1-SFT.
2. SYSTEM does not assume examples are always present.
3. Program fills `n = len(sentence)` next to the JSON-encoded sentence.
4. SYSTEM must be the tokenizer `system` role (P0 concatenated the instruction into `user`).
5. Example labels may come only from the named frozen train label version.

Swapping a long prompt onto a P0 adapter is not a new SFT run.
