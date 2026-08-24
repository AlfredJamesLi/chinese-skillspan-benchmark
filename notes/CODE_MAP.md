# Code map (Chinese-SkillSpan) — read-only pointers

These paths are in the parent repo. Edit them only when the user asks for experiment/code work, not when drafting prose.

## Data

- `chinese_skillspan_preprocessing/` — gold, doccano, LKST alpaca, silver sbatch
- `chinese_skillspan_preprocessing/data/annotated/processed/chinese_skillspan/{train,dev,test}.json`
- `data/annotated/processed/chinese_skillspan/` — **second copy, may differ**

## Run / eval (shared with Access; do not change for Access jobs)

- `main.py` — `--dataset_name chinese_skillspan`
- `run.py`, `evaluate_src.py`
- `prompt_template_rag.py` — `chinese_skillspan` block (LKST)
- `prompt_template_zh.py` — unused by current silver scripts
- `prompt_template_ctx.py` — CN context prompt copy

## Training / baselines

- `LLaMA-Factory/data/chinese_skillspan_lkst_*.json`
- `LLaMA-Factory/data_transfer_chinsese_skillspan/`
- `LLaMA-Factory/saves/qwen2_5_14b/lora/sft_CN_skillspan_*`
- `LLaMA-Factory/evaluate_lkst.py`, `infer_S.py`
- `Baseline_Models_Collection/eval_*chinese*.py`, `eval_roberta_wwm_ext_crf.py`

## Outputs

- `chinese_skillspan_preprocessing/output/`
- `output/chinese_skillspan*`
