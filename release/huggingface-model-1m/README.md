---
language:
  - zh
pretty_name: JobBERT-zh 1M (DAPT contrast)
library_name: transformers
pipeline_tag: token-classification
inference: false
widget:
  - text: "任职要求：熟练掌握Python和SQL，英语CET-6，具备良好的沟通与团队合作能力。"
    example_title: "Chinese job advertisement"
tags:
  - jobbert-zh
  - chinese-skillspan
  - token-classification
  - crf
  - job-advertisements
  - lskt
license: other
base_model: hfl/chinese-roberta-wwm-ext
---

# JobBERT-zh 1M (DAPT contrast)

This repository is a **smaller domain-adaptive pre-training contrast** of JobBERT-zh. It is **not** the paper-main encoder.

| Checkpoint | Hub | Test | Typed exact F1 | Typed relaxed F1 |
|---|---|---|---:|---:|
| **3M + V4 CRF (paper-main)** | [`AlfredJames/jobbert-zh`](https://huggingface.co/AlfredJames/jobbert-zh) | V4 hybrid 2601 + jieba | **0.433118** | 0.587322 |
| **1M + V4 CRF (this repo)** | [`AlfredJames/jobbert-zh-1m`](https://huggingface.co/AlfredJames/jobbert-zh-1m) | V4 hybrid 2601 + jieba | **0.427162** | 0.595170 |

Cells are from `tables/hybrid_cws_simhuman980_all_models.csv`. Do **not** rank 0.4272 against V4 hybrid **0.4331**, human-reference v6a **0.5536±0.0054**, or Gold v2 ChatGPT **0.6365** in one table.

- Paper-main encoder: https://huggingface.co/AlfredJames/jobbert-zh
- Human-reference continuation: https://huggingface.co/AlfredJames/jobbert-zh-v6a
- Code and data: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark
- Archive (`v0.1.3`): https://doi.org/10.5281/zenodo.22698504

This is **not** English [`jjzha/jobbert-base-cased`](https://huggingface.co/jjzha/jobbert-base-cased) and **not** TechWolf [`JobBERT-v3`](https://huggingface.co/TechWolf/JobBERT-v3). There is no `AutoModelForTokenClassification` export and no hosted Inference Provider.

---

## What this repository contains

Same three-file layout as the 3M paper-main repo: MLM encoder (`config.json`, `model.safetensors`, tokenizer) plus a V4 silver CRF head (`crf/best.pt`). The 1M encoder is a **different DAPT run**, not a truncated 3M checkpoint.

Paper-main typed exact **0.4331** uses **`AlfredJames/jobbert-zh`**, not these weights.

---

## Intended uses

- Ablation / contrast against the 3M JobBERT-zh encoder on Chinese-SkillSpan
- Research on domain-adaptive pre-training scale for Chinese job-ad spans

## Out-of-scope uses

- Replacing `AlfredJames/jobbert-zh` as the paper-main encoder
- Applicant screening, hiring automation, or ESCO concept-ID prediction
- Hub Inference Providers / the default token-classification widget
- Treating V4 hybrid scores as fully human gold

---

## Loading

Same `BertCRF` pattern as the 3M card (`scripts/train_cn_roberta_crf.py`). After decoding tags, jieba-snap predictions and run `scorer/score_lskt.py --align-mode official`.

```python
import torch
from torch import nn
from torchcrf import CRF
from huggingface_hub import hf_hub_download
from transformers import AutoModel, AutoTokenizer

REPO = "AlfredJames/jobbert-zh-1m"

class BertCRF(nn.Module):
    def __init__(self, model_dir: str, n_labels: int = 9, dropout: float = 0.1):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_dir)
        self.dropout = nn.Dropout(dropout)
        self.emissions = nn.Linear(self.encoder.config.hidden_size, n_labels)
        self.crf = CRF(n_labels, batch_first=True)

tok = AutoTokenizer.from_pretrained(REPO)
model = BertCRF(REPO)
crf_path = hf_hub_download(REPO, "crf/best.pt")
model.load_state_dict(torch.load(crf_path, map_location="cpu"))
```

---

## Licence

`license: other` until job-advertisement text rights are confirmed. The backbone `hfl/chinese-roberta-wwm-ext` is listed as Apache-2.0 on Hugging Face. Do not treat this checkpoint as Apache-2.0.

Funding: National Social Science Fund of China, Grant No. **21BGL142**. Authors: same as JobBERT-zh (corresponding author Xiangyu Zhao, `xianzhao@cityu.edu.hk`).
