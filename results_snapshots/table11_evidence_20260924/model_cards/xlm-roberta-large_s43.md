---
language:
  - zh
pretty_name: Table 11 LSKT linear head (xlm-roberta-large, seed 43)
library_name: transformers
pipeline_tag: token-classification
inference: false
widget:
  - text: "任职要求：熟练掌握Python和SQL，英语CET-6，具备良好的沟通与团队合作能力。"
    example_title: "Chinese job advertisement"
tags:
  - chinese-skillspan
  - lskt
  - token-classification
  - table11
  - xlm-roberta
license: other
base_model: FacebookAI/xlm-roberta-large
base_model_revision: c23d21b0620b635a76227c604d44e43a9f0ee389
---

# Table 11 Chinese LSKT linear head (`xlm-roberta-large`, seed 43)

Hub: [`AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s43`](https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s43)

`XLMRobertaForTokenClassification` fine-tuned on Silver-plus B2 (2,150 train / 169 development sentences) with `run_chinese_encoder.py`. Separate from the JobBERT-zh CRF models ([`AlfredJames/jobbert-zh`](https://huggingface.co/AlfredJames/jobbert-zh), [`jobbert-zh-v6a`](https://huggingface.co/AlfredJames/jobbert-zh-v6a)) and from the original fill-mask checkpoint [`FacebookAI/xlm-roberta-large`](https://huggingface.co/FacebookAI/xlm-roberta-large).

Paper cell (three-seed mean ± sample SD, this encoder): **0.522 ± 0.022** typed exact micro-F1 on Gold150. This repository is **seed 43 only**.

| Seed | Selected epoch | Gold150 typed exact |
|---:|---:|---:|
| 43 | 14 | 0.522449 |

Gold150 is a 150-sentence **human reference freeze** (663 spans, L=2), not a new blind test. Freeze SHA-256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` ([`data/gold150_test.jsonl`](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150_test.jsonl)).

- Evidence pack: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/audit/table11-evidence-20260924/results_snapshots/table11_evidence_20260924
- Code: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark

## Files

| File | Role | SHA-256 |
|---|---|---|
| `model.safetensors` | Fine-tuned encoder + 9-label linear head | `be3caa3ed3a7ebf5a6ffe3d698440bc15c0b4fb8dd856157e74a47ee45fded49` |
| `config.json` | `XLMRobertaForTokenClassification`, labels B-/I- K,L,S,T and O | |
| tokenizer files | Copied from `FacebookAI/xlm-roberta-large@c23d21b0620b635a76227c604d44e43a9f0ee389` | |

This checkpoint is a token classifier, not a masked language model. The `FacebookAI/xlm-roberta-large` `lm_head` was dropped; `classifier.weight` and `classifier.bias` were randomly initialized. The encoder was then trained together with the head in float32.

## Load

```python
from transformers import AutoModelForTokenClassification, AutoTokenizer
repo = "AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s43"
tok = AutoTokenizer.from_pretrained(repo, use_fast=True)
model = AutoModelForTokenClassification.from_pretrained(repo)
# labels: B-K B-L B-S B-T I-K I-L I-S I-T O
# inputs: list(chinese_text) as words; score the first subword of each character
```

Matching inference: `https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/audit/table11-evidence-20260924/results_snapshots/table11_evidence_20260924/scripts/reinfer_gold150.py` (uses the original on-disk `best/` which is byte-identical to this Hub snapshot).

## Training

- Train: `data/silver_plus_v6a_nocross/train_b2.jsonl` SHA-256 `8921e5fc4b89a0fa83bd942f919c3325546b9938e099b6a13e378736b6717d2e` (2,150)
- Dev (epoch selection only): `dev_b2.jsonl` SHA-256 `e67a3eb5229b94c6c1b552d5f40ece9ad362197236c20cd66b7f2600c9636fef` (169)
- Gold150 never entered the gradient or `history.json`
- AdamW \(2\times10^{-5}\), batch 8, 20 epochs, seed 43, character BIO, first-subword, chunk 128
- Scorer: `cnss-lskt-1.2.0` typed exact micro-F1

## Limitations

- Hub `license: other`. GitHub Apache-2.0 covers repository software, not these weights.
- Gold150 is a frozen human reference, not a new blind test.
- Character-offset LSKT F1 is not a single difficulty ranking against English token-span F1.
