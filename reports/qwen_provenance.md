# Qwen 0.2130 provenance

**Status: 0.2130 is not reproducible from current artifacts.**  
Do not tune toward 0.2130. Do not overwrite existing dumps.

## Paper claim

Table 3: Qwen S-F1 = **0.2130** (strict). Text says “instruction-tuned LLMs under the same prompting,” listing ChatGPT-4o, Claude, Kimi, DeepSeek, Qwen.

## What exists

| Artifact | Finding |
|---|---|
| `chinese_skillspan_preprocessing/Dataset_Silver_Qwen2-5-14B.sh` | **14B only**. Commented run: base `Qwen2.5-14B-Instruct`. Active run: LoRA `sft_CN_skillspan_ner_latest`. Prompt: `prompt_template_rag`, `ner`, RAG on, shots 0. |
| `output/chinese_skillspan_qwen25-14b_test_all.jsonl` | 3237 rows, 2025-10-07. Unified **legacy** scorer vs Gold: typed ≈ 0.34, collapsed ≈ 0.39 (see `table3_reproduction.csv`). **Not 0.2130.** |
| `output/chinese_skillspan_qwen25-14b_test_all_1.jsonl` | **163 rows only**. Incomplete LoRA run (2025-10-28). Ignore. |
| `qwen2p5_S_predictions.metrics.json` | S-dimension only, LoRA `sft_CN_skillspan_ner_skills_2000`, gold `test_lkst_S.json` (2676). Strict F1 **0.0781**. Not 0.2130. |
| `LLaMA-Factory/data/train_lkst_S.json` | **2142 rows** (= dev size). Must not claim 17460-train SFT. |
| 7B checkpoint / 7B dump | **Not found.** |
| Log that prints 0.2130 | **Not found.** |

## Checklist vs 0.2130

| Question | Answer |
|---|---|
| 7B or 14B? | Only 14B scripts/dumps. 7B not evidenced. |
| zero/few-shot or SFT? | Script contains both a commented base-14B command and an active LoRA command. `test_all.jsonl` is not labeled; F1 0.34–0.39 ≠ 0.2130 either way. |
| full LSKT or S-only? | Dump has BIO4 fields (full LSKT). S-only eval is 0.078. |
| typed or collapsed? | Neither current dump metric equals 0.2130. |
| which gold? | Rescore used `admin_Baseline_test.jsonl`. Wrong-gold `*.eval_ner.json` is banned (~0 F1). |

## Is 0.34–0.39 just a scoring-protocol difference?

**No.** Typed vs collapsed on the same dump moves F1 between ~0.34 and ~0.39, not down to 0.2130. S-only is 0.078. Alignment/legacy vs official changes coverage, not enough to invent 0.2130.

## Decision

Mark paper Qwen **0.2130 as unreproducible**. Next (later phase, not this freeze): run one declared, logged config (14B, prompt hash, SFT or base stated, Gold 2601 unique IDs, `cnss-lskt-1.0.0`) and replace the cell with that number. Do not search for a lost dump that happens to hit 0.2130.
