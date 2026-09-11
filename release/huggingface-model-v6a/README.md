---
language:
  - zh
pretty_name: JobBERT-zh v6a (human reference)
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
  - gold150
license: other
base_model: AlfredJames/jobbert-zh
---

# JobBERT-zh v6a (human reference set)

This repository is the **human-reference continuation** of JobBERT-zh (artifact Gold150). It is an **additional version**, not a replacement of the V4 hybrid 2601 encoder row.

| Checkpoint | Hub | Test | Typed exact F1 |
|---|---|---|---|
| V4 (paper-main encoder) | [`AlfredJames/jobbert-zh`](https://huggingface.co/AlfredJames/jobbert-zh) | V4 hybrid 2601 + jieba | **0.4331** |
| **v6a B2 (this repo)** | [`AlfredJames/jobbert-zh-v6a`](https://huggingface.co/AlfredJames/jobbert-zh-v6a) | Human reference set | **0.5536±0.0054** (n=3 sample SD) |

Do **not** rank 0.5536 against 0.4331, official Qwen SOP extract 0.1724, or Gold v2 ChatGPT 0.6365 in one table. SD is a **three-seed sample SD**, not a test-set confidence interval. The human reference freeze is **not** in Zenodo `v0.1.1`.

- Code: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark
- V4 weights (unchanged): https://huggingface.co/AlfredJames/jobbert-zh
- Human-reference notes: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150/README.md

---

## What this repository contains

Same 3M DAPT encoder as `AlfredJames/jobbert-zh`. Only the CRF head is continued from the released V4 `crf/best.pt` on Silver-plus **v6a B2**. The published teacher files are `v6a_nocross` (**2,150** train / **169** frozen dev). A 2,156-row train list is an earlier v6a count before the nocross dedupe; do not treat 2,156 as the released file.

| Path | Role |
|---|---|
| `config.json`, `model.safetensors`, `tokenizer.json`, `tokenizer_config.json` | Encoder (identical SHA to `AlfredJames/jobbert-zh`) |
| `crf/best.pt` | Default load path = **seed 42** (human-reference exact 0.5544; closest to the 3-seed mean) |
| `crf/seed42/best.pt` | Seed 42 — human-reference exact **0.5544** / relaxed 0.6917 |
| `crf/seed43/best.pt` | Seed 43 — human-reference exact **0.5479** / relaxed 0.6794 |
| `crf/seed44/best.pt` | Seed 44 — human-reference exact **0.5587** / relaxed 0.6959 |

Paper cell **0.5536±0.0054** / relaxed **0.6890±0.0085** is the mean ± sample SD of those three seeds. Loading only seed 42 is **not** the published mean.

| File | Bytes | SHA-256 |
|---|---:|---|
| encoder `model.safetensors` | 406,730,376 | `ed2130f680d0aa9691d081a516963da252449746ef7e78818050e3039b6ccf3b` |
| `crf/seed42/best.pt` | 409,169,393 | `7bea1f284b666570fd542c1fc7c9f1101840a11be16b4c04cb303047a8df7b7d` |
| `crf/seed43/best.pt` | 409,169,393 | `275b97da7a94d2d42c3ae0fe8e88c4fe2dec857831e0dc958578cb593abc06d8` |
| `crf/seed44/best.pt` | 409,169,393 | `3d6d708b8633264aed47911eaeaa317dc052dff1bea34c814165ae42e68cc626` |

Init CRF (not in this repo): V4 `AlfredJames/jobbert-zh` `crf/best.pt`, SHA-256 `d98814cb954036f885e1247c2c50c66adbc5a280750f0228bfc3df077f2fc98c`.

---

## Training

- Encoder frozen as the released 3M JobBERT-zh (`ckpt65000`).
- CRF continued with AdamW \(2\times10^{-5}\), weight decay 0.01, batch 16, at most 6 epochs, patience 2, 10% warmup.
- Checkpoint = argmax frozen-dev typed exact.
- Labels: Silver-plus teacher **B2** (not B1). Isolation: sentence-level (extended).
- Scorer: `cnss-lskt-1.2.0`. Human-reference freeze SHA-256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` (`data/gold150_test.jsonl`).
- No jieba snap on this human-reference cell (character CRF vs human overlay).

There is no `AutoModelForTokenClassification` export.

---

## Loading

```python
import torch
from torch import nn
from torchcrf import CRF
from huggingface_hub import hf_hub_download
from transformers import AutoModel, AutoTokenizer

REPO = "AlfredJames/jobbert-zh-v6a"

class BertCRF(nn.Module):
    def __init__(self, model_dir: str, n_labels: int = 9, dropout: float = 0.1):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_dir)
        self.dropout = nn.Dropout(dropout)
        self.emissions = nn.Linear(self.encoder.config.hidden_size, n_labels)
        self.crf = CRF(n_labels, batch_first=True)

tok = AutoTokenizer.from_pretrained(REPO)
model = BertCRF(REPO)
# Default = seed 42. For the paper mean, evaluate seed42/43/44 and average.
crf_path = hf_hub_download(REPO, "crf/best.pt")
model.load_state_dict(torch.load(crf_path, map_location="cpu"))
```

The paper class is `BertCRF` in `scripts/train_cn_roberta_crf.py`.

---

## Out of scope

- Replacing `AlfredJames/jobbert-zh` (0.4331 on V4 hybrid 2601)
- Applicant screening or ESCO concept-ID prediction
- Treating 0.5536 as a test CI, or as an independent re-test of the same systems on 2,601 IDs (human-reference IDs sit inside hybrid 2601)
- Peel-rerun heads (0.5509); those did not beat 0.5536 and are not this dump

---

## Licence

`license: other` until job-advertisement text rights are confirmed. Same authors and funding (NSSFC 21BGL142) as JobBERT-zh.
