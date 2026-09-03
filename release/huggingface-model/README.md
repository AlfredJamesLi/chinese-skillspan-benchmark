---
language:
  - zh
pretty_name: JobBERT-zh
library_name: transformers
pipeline_tag: token-classification
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

# JobBERT-zh

**JobBERT-zh** is a Chinese job-domain encoder and CRF span head for **Chinese-SkillSpan** (competency span extraction from Chinese job advertisements). It follows the JobBERT / DaJobBERT domain-adaptive pre-training setup of Zhang et al., using a Chinese RoBERTa-wwm backbone.

- Repository: [https://huggingface.co/AlfredJames/jobbert-zh](https://huggingface.co/AlfredJames/jobbert-zh) (public)
- This is **not** English [`jjzha/jobbert-base-cased`](https://huggingface.co/jjzha/jobbert-base-cased)
- This is **not** TechWolf [`JobBERT-v3`](https://huggingface.co/TechWolf/JobBERT-v3) (job-title embeddings)

The Hugging Face model tree may show a single “finetuned from `hfl/chinese-roberta-wwm-ext`” hop. Training actually has **two stages** (see below).

There is no `AutoModelForTokenClassification` export and no hosted Inference Provider. Token-classification in the sidebar does not mean one-click NER.

---

## What this repository contains

| Stage | Role | Files in this repo |
|---|---|---|
| 1. Public backbone | Chinese RoBERTa-wwm | not redistributed; load `hfl/chinese-roberta-wwm-ext` if needed |
| 2. Domain-adaptive MLM | **Pretrained JobBERT-zh encoder** (3M job-ad run, step 65000) | `config.json`, `model.safetensors`, `tokenizer.json`, `tokenizer_config.json` |
| 3. Task CRF | **Fine-tuned span head** on V4 silver LSKT | `crf/best.pt` |

Paper-main typed exact F1 **0.4331** uses stage 2 + stage 3 **and** jieba span snap. Loading only `model.safetensors` is not enough to reproduce that number.

`config.json` reports `BertModel`, hidden size 768, 12 layers, vocabulary 21,128.

---

## Intended uses

- Research on Chinese competency / skill-span extraction
- Fine-tuning or evaluation on Chinese-SkillSpan (LSKT)
- Reproducing the paper-main encoder row after jieba alignment

## Out-of-scope uses

- Applicant screening, hiring automation, or profiling of individuals
- Inferring protected attributes
- Claiming ESCO concept-ID prediction (this model emits LSKT spans only)
- Nested or overlapping NER
- Treating V4 hybrid scores as fully human gold
- Production HR systems without human review
- The Hub “Token Classification” widget / Inference Providers

---

## Architecture

Encoder: `AutoModel` from this repository (continued MLM from `hfl/chinese-roberta-wwm-ext`).  
Head: linear emissions + linear-chain CRF (`torchcrf`, `batch_first=True`), 9 BIO labels  
`O`, `B-L`, `I-L`, `B-K`, `I-K`, `B-S`, `I-S`, `B-T`, `I-T`.  
Default fine-tune recipe (`scripts/train_cn_roberta_crf.py`): seed 42, 6 epochs, patience 2, batch size 16, max length 256, learning rate `2e-5`.  
Tokenizer: `AutoTokenizer` with `is_split_into_words=True` on **character** tokens.

Hardware used for the 0.4331 run: `[TODO: GPU / CUDA / wall-clock]`.

---

## Training data

- **Backbone:** [`hfl/chinese-roberta-wwm-ext`](https://huggingface.co/hfl/chinese-roberta-wwm-ext). Hugging Face card metadata lists **Apache-2.0** for that checkpoint.
- **MLM:** Chinese job-advertisement sentences. Sentence dumps are **not** published with this model. `[TODO: confirm sampling counts and redistribution rights]`
- **CRF:** `train_lskt_v4_silver.jsonl` / `dev_lskt_v4_silver.jsonl` (SOP v4 silver, **not** human Doccano Gold)

This repository’s licence remains `other` until job-advertisement text rights are confirmed. Compatibility with Apache-2.0 of the backbone is required before any more permissive SPDX id is chosen.

---

## Loading

```python
import torch
from torch import nn
from torchcrf import CRF
from huggingface_hub import hf_hub_download
from transformers import AutoModel, AutoTokenizer

REPO = "AlfredJames/jobbert-zh"

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

The paper repository class `BertCRF` in `scripts/train_cn_roberta_crf.py` is the implementation used for the published scores. After decoding tags, jieba-snap predictions and run `scorer/score_lskt.py --align-mode official`.

---

## Fine-tuning

```bash
python3 scripts/train_cn_roberta_crf.py \
  --seed 42 \
  --model_dir AlfredJames/jobbert-zh \
  --train data/train_lskt_v4_silver.jsonl \
  --dev data/dev_lskt_v4_silver.jsonl \
  --test data/corpus_splits/test.json \
  --gold data/gold_canonical_v2.jsonl \
  --out_dir path/to/crf_run \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5
```

`train_cn_roberta_crf.py` currently sets `local_files_only=True`; point `--model_dir` at a local snapshot if the script is used unchanged.

---

## Evaluation

- Task: typed LSKT span extraction  
- Scorer: `cnss-lskt-1.2.0`, official alignment  
- Paper-main gold: 2,601 IDs, V4 hybrid (derived; not human Doccano Gold)  
- Verified jieba-aligned scores (`tables/hybrid_cws_simhuman980_all_models.csv`):

| System | Typed exact F1 | Typed relaxed F1 |
|---|---:|---:|
| JobBERT-zh 3M + V4 CRF (this repo) | 0.433118 | 0.587322 |
| JobBERT-zh 1M + V4 CRF (not this weight dump) | 0.427162 | 0.595170 |

Do not rank these figures against Gold v2 ChatGPT **0.6365** in one sentence.

---

## Limitations

Silver CRF labels are not fully human-adjudicated. Jieba snap changes exact-match F1 substantially (0.2552 without snap vs 0.4331 with snap on the frozen 3M dump). Public-institution ads are difficult under Gold v2 notes. `[TODO: measured demographic or firm-size bias, if analysed.]`

---

## Ethics

Job advertisements may contain employer names and workplace locations. Do not re-identify people, scrape extra ads without rights, or use scores as the sole hiring signal.

Funding: National Social Science Fund of China, Grant No. **21BGL142**.

---

## Authors

Guojing Li, Zichuan Fu, Junyi Li, Wenlin Zhang, Kaifeng Guo, Jinning Yang, Jingtong Gao, Xiangyu Zhao (corresponding).  
`[TODO: affiliations and contact email]`

---

## Licence

`license: other`

The backbone `hfl/chinese-roberta-wwm-ext` is listed as **Apache-2.0** on Hugging Face. This checkpoint is trained further on job-advertisement text whose redistribution rights are **not** confirmed in the paper repository. Do not treat JobBERT-zh as Apache-2.0 until that confirmation exists.

---

## Links

| Resource | URL |
|---|---|
| This model | https://huggingface.co/AlfredJames/jobbert-zh |
| Code | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark |
| Dataset (HF) | `[TODO: Hugging Face dataset URL]` |
| Paper | `[TODO: this paper's arXiv / PeerJ URL]` |
| Zenodo DOI | `[TODO: Zenodo DOI]` |
