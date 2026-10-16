# Compatibility patches (2026-09-21)

## Tokenizer placeholders (`run_common_encoder.py`, `run_chinese_encoder.py`)

XLM-R `is_split_into_words=True` drops some source indices:
- SkillSpan: ASCII SUB `\x1a` (8 training sentences)
- Chinese B2: whitespace characters (spaces), because character-level tokens include `' '`

Protocol forbids dropping source words. Replacement: encode those indices as `■` (U+25A0). Original tokens and gold tags are unchanged in saved predictions. Smoke (first 16 sentences) did not hit these cases, which is why 16/16 smoke passed and full encoding failed.

## MaChAmp `MachampBatchSampler` + torch 2.14

`Sampler.__init__` no longer accepts `data_source`. Patch in
`upstream_full/SkillSpan/machamp/machamp/data/machamp_sampler.py`:
`super().__init__(data_source)` → `super().__init__()`.
Reason: CUDA 13 server cannot install the 2022 torch 1.7/1.8 stack.
- MaChAmp `torch.load(..., weights_only=False)`：训练已跑完 epoch 1，重载时 torch 2.14 默认 weights_only=True。只对自产 checkpoint 关闭。


## ESCOXLM-R model path

See `ESCOXLM-R_MODEL_PATH.md`.
