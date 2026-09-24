---
language: zh
license: other
base_model: jjzha/esco-xlm-roberta-large
base_model_revision: 8093cc37ac619a25c5166355acba7be878eb6402
library_name: transformers
pipeline_tag: token-classification
tags:
  - named-entity-recognition
  - skill-extraction
  - chinese-skillspan
  - lskt
  - table11
---

# Table 11 Chinese LSKT linear head (esco-xlm-roberta-large, seed 43)

This is **not** JobBERT-zh CRF and **not** the masked-LM checkpoint `jjzha/esco-xlm-roberta-large`.
It is a new token-classification head trained on Silver-plus B2 (2,150 train / 169 dev) with `run_chinese_encoder.py`.

## Load

```python
from transformers import AutoModelForTokenClassification, AutoTokenizer
tok = AutoTokenizer.from_pretrained(LOCAL_BEST_DIR, use_fast=True)
model = AutoModelForTokenClassification.from_pretrained(LOCAL_BEST_DIR)
# labels: B-K B-L B-S B-T I-K I-L I-S I-T O
# inputs: list(chinese_text) as words; score first subword of each character
```

Local checkpoint (not a public URL until upload is approved):

`/home/guojingli3/cnss_external_benchmarks_20260921/runs/chinese/full/esco-xlm-roberta-large/43/best`

SHA-256 of `model.safetensors`: `2efb6f69def4211a07a9ad30ee4563fe0dd83569d7e3687676b9077be6acc3aa`

Inference that matches the paper cell: `TABLE11_EVIDENCE_20260924/scripts/reinfer_gold150.py`.

## Training data

- Train: `data/silver_plus_v6a_nocross/train_b2.jsonl` SHA-256 `8921e5fc4b89a0fa83bd942f919c3325546b9938e099b6a13e378736b6717d2e` (2,150)
- Dev (model selection): `dev_b2.jsonl` SHA-256 `e67a3eb5229b94c6c1b552d5f40ece9ad362197236c20cd66b7f2600c9636fef` (169)
- Gold150 is **eval-only**. It was not in the gradient and not in epoch selection.

## Metrics (Gold150, official cnss-lskt-1.2.0 typed exact micro-F1)

- seed 43, selected epoch 15: **0.540146**
- Gold150 is a 150-sentence human reference freeze (663 spans, L=2), not a new blind test.

## Head vs MLM

`jjzha/esco-xlm-roberta-large@8093cc37ac619a25c5166355acba7be878eb6402` is fill-mask (`XLMRobertaForMaskedLM` or `RobertaForCustomMaskedLM`).
Loading `AutoModelForTokenClassification` discards `lm_head` and randomly initializes `classifier.weight/bias` (1024×9). All encoder + classifier parameters were then fine-tuned in float32 (AdamW 2e-5, 20 epochs, batch 8).

## Limitations

- Do not mix with JobBERT-zh CRF ~0.55.
- Do not treat Gold150 as independent blind test.
- Character-offset LSKT F1 is not comparable as absolute difficulty against English token-span F1.
