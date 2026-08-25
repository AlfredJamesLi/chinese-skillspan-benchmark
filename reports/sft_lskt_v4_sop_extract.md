# Qwen SOP extract: Instruct baseline vs v4-silver LoRA

Zero-shot Instruct P2-2601 (already scored): typed exact **0.1724**, relaxed **0.3279**. This is the LLM baseline for the SOP extract prompt.

Paired SFT (in progress): LoRA on `train_lskt_v4_silver.jsonl` (17460; **0 overlap** with P2 2601), same SOP extract prompt. Not Gold v2. Not the old `sft_CN_skillspan_ner_*` (those used `@@span##` / RAG NER).

Train log: `reports/sft_lskt_v4_sop_extract.train.log`  
Adapter out: `LLaMA-Factory/saves/qwen2_5_14b/lora/sft_lskt_v4_sop_extract`

Paired Llama-3-8B-Instruct **zero-shot** (same SOP extract prompt, no LoRA): started on idle GPU 1 while Qwen LoRA occupies GPU 2. Script `scripts/run_llama3_8b_sopv4_p2_2601.py`. Full P2 **2601** (user “260” treated as truncated 2601). Log: `reports/llama3_8b_instruct_sopv4_p2_2601.run.log`.

Do not write scores into `confirmed-results.md` until P2 coverage gate passes. Do not compare P2 exact F1 to ChatGPT 0.6365 on Gold v2.
