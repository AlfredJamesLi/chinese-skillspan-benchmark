---
language:
  - zh
pretty_name: Chinese JobBERT
library_name: transformers
pipeline_tag: token-classification
tags:
  - chinese-jobbert
  - chinese-skillspan
  - token-classification
  - crf
  - job-advertisements
  - lskt
license: other
# [TODO: SPDX licence — must be compatible with hfl/chinese-roberta-wwm-ext AND training-data rights]
base_model: hfl/chinese-roberta-wwm-ext
# [TODO: Hugging Face model repo id]
# [TODO: dataset repo id]
---

# Chinese JobBERT

**Chinese JobBERT** is the domain-adapted encoder baseline for **Chinese-SkillSpan**: competency span extraction from Chinese job advertisements.

This card describes the model as implemented in `scripts/train_cn_roberta_crf.py`. Weights are **not** stored in the paper Git tree. `[TODO: Hugging Face model URL]`.

Do **not** select a final model licence until (1) the base-model licence is verified on Hugging Face and (2) redistribution rights for the job-advertisement training text are confirmed.

---

## Model description

Chinese JobBERT is built in two stages, as recorded in repository scripts and notes:

1. **Continued masked language modelling** on Chinese job-advertisement sentences, initialised from [`hfl/chinese-roberta-wwm-ext`](https://huggingface.co/hfl/chinese-roberta-wwm-ext) (Chinese RoBERTa whole-word-masking, `BertForMaskedLM` in the local snapshot `config.json`).
2. **Token classification with a linear emission layer and a linear-chain CRF** (`BertCRF` in `scripts/train_cn_roberta_crf.py`): `AutoModel` encoder, dropout 0.1, 9 BIO labels by default (`O`, `B-L`, `I-L`, `B-K`, `I-K`, `B-S`, `I-S`, `B-T`, `I-T`).

Laboratory runs referred to 1M- and 3M-sentence MLM corpora and a 3M checkpoint `encoder_ckpt65000`. Those corpora and checkpoints are local; they are not a public revision.

Repository aliases: JobBERT-zh, JobBERT 3M v4. The public name is **Chinese JobBERT**.

This is **not** the English [`jjzha/jobbert-base-cased`](https://huggingface.co/jjzha/jobbert-base-cased) model. English JobBERT skill/knowledge heads scored near zero on the Chinese V4 hybrid (committed CSV typed exact 0.0096 / 0.0088).

---

## Intended uses

- Research on Chinese competency / skill-span extraction
- Fine-tuning or evaluation on Chinese-SkillSpan (LSKT)
- Reproducing the paper-main encoder rows after jieba alignment

---

## Out-of-scope uses

- Applicant screening, hiring automation, or profiling of individuals
- Inferring protected attributes or demographic information
- Claiming ESCO concept-ID prediction (this model emits LSKT spans, not ESCO IDs)
- Nested or overlapping NER
- Treating V4 hybrid scores as human-gold performance
- Production HR systems without a human review policy

---

## Architecture (verified from training code)

| Item | Value in `train_cn_roberta_crf.py` |
|---|---|
| Encoder load | `AutoModel.from_pretrained(model_dir, local_files_only=True)` |
| Head | Linear emissions + `torchcrf.CRF` (`batch_first=True`) |
| Default labels | 9-way joint LSKT BIO |
| Optional STL | `--keep_type L\|K\|S\|T` → 3-tag CRF |
| Max length | 256 (default) |
| Tokenizer | `AutoTokenizer` from the same `model_dir`; `is_split_into_words=True` on character tokens |

Hidden size and layer count follow the base checkpoint; they are not re-stated here beyond what `AutoModel` loads. `[TODO: publish config.json with the public revision]`.

---

## Language

Chinese (`zh`). Job-advertisement register, including mixed English tokens (for example tool names).

---

## Training data

- **Base:** `hfl/chinese-roberta-wwm-ext`.
- **MLM adaptation:** Chinese job-advertisement sentences prepared by `scripts/prepare_jobbert_*.py`. File-level dumps such as `data/jobbert_3m_sents.jsonl` exist locally. **`[TODO: confirm sentence counts, sampling, and redistribution rights before stating that the MLM corpus is public.]`**
- **CRF (paper-main recipe):** `data/train_lskt_v4_silver.jsonl` and `data/dev_lskt_v4_silver.jsonl` (SOP v4 silver, **not** human Gold).

---

## Preprocessing and tokenisation

1. Sentences are stored as **character lists** in `tokens`.
2. The tokenizer is applied with `is_split_into_words=True`, truncation/padding to `max_len`.
3. Word-piece subwords copy the first-piece label; subsequent pieces are masked to `O` (id 0) in the CRF label channel.
4. Paper-main **evaluation** additionally jieba-snaps predicted spans (`scripts/cws_snap.py`). Skipping that step changes the score (frozen 3M dump scored **0.2552** typed exact without snap versus **0.4331** with snap).

---

## Loading and inference

There is **no** `AutoModelForTokenClassification.from_pretrained` export in this repository. Inference uses the custom `BertCRF` module. The following is a schematic of the actual class (edit paths; `local_files_only` is what the trainer uses):

```python
import torch
from torch import nn
from torchcrf import CRF
from transformers import AutoModel, AutoTokenizer

class BertCRF(nn.Module):
    def __init__(self, model_dir: str, n_labels: int = 9, dropout: float = 0.1):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_dir)
        self.dropout = nn.Dropout(dropout)
        self.emissions = nn.Linear(self.encoder.config.hidden_size, n_labels)
        self.crf = CRF(n_labels, batch_first=True)

JOINT = ["O", "B-L", "I-L", "B-K", "I-K", "B-S", "I-S", "B-T", "I-T"]

# [TODO: replace with the public Chinese JobBERT revision]
model_dir = "path/to/chinese-jobbert"
tok = AutoTokenizer.from_pretrained(model_dir)
model = BertCRF(model_dir)
# model.load_state_dict(torch.load("path/to/best.pt"))  # CRF run dump from train_cn_roberta_crf.py

tokens = list("熟悉Python与英语六级")  # character tokens
enc = tok(tokens, is_split_into_words=True, return_tensors="pt", truncation=True, max_length=256)
# Decode with the CRF (see BertCRF.forward / predict_tags in train_cn_roberta_crf.py)
```

Then map CRF tag ids back to characters and, for paper-main scores, run `scripts/cws_snap.py` and `scorer/score_lskt.py --align-mode official`.

`[TODO: add a `from_pretrained` wrapper when the public repository exists.]`

---

## Fine-tuning

Supported by `scripts/train_cn_roberta_crf.py`:

```bash
python3 scripts/train_cn_roberta_crf.py \
  --seed 42 \
  --model_dir path/to/chinese-jobbert-encoder \
  --train data/train_lskt_v4_silver.jsonl \
  --dev data/dev_lskt_v4_silver.jsonl \
  --test data/corpus_splits/test.json \
  --gold data/gold_canonical_v2.jsonl \
  --out_dir path/to/crf_run \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5
```

Hyperparameters above are the verified script defaults / 3M V4 wrapper. Hardware: `[TODO]`.

---

## Evaluation

- **Task:** typed span extraction, labels L / K / S / T.
- **Scorer:** `cnss-lskt-1.2.0`, official alignment, micro-F1 over sentences.
- **Paper-main gold:** `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` (2,601 IDs; derived hybrid, not human Doccano Gold).
- **Verified CSV** (`tables/hybrid_cws_simhuman980_all_models.csv`), jieba-aligned:

| Checkpoint (laboratory name) | Typed exact F1 | Typed relaxed F1 |
|---|---:|---:|
| JobBERT_3M_v4 (Chinese JobBERT 3M) | 0.433118 | 0.587322 |
| JobBERT_1M_v4 | 0.427162 | 0.595170 |

Do not compare these numbers in one sentence with Gold v2 ChatGPT **0.6365**.

---

## Limitations, bias, and domain shift

- Silver CRF labels follow SOP v4, not full human adjudication.
- Boundary errors are common; jieba snap changes exact-match F1 substantially.
- Encoder quality varies by source domain (public-institution ads are hard under Gold v2 notes).
- Training text is job-ad register: tools, degrees, and trait clichés are over-represented; narrative Chinese is under-represented.
- Character tokenisation plus WordPiece can split English tool names awkwardly; Handbook B forbids mid-word cuts in gold.
- `[TODO: document any measured gender, region, or firm-size bias once analysed]`.

---

## Ethical and responsible use

Job ads can contain employer names and workplace locations. Do not re-identify individuals, scrape additional ads to “improve” the model without rights, or deploy scores as the sole hiring signal. Funding: National Social Science Fund of China, Grant No. **21BGL142**.

---

## Authors and citation

Guojing Li, Zichuan Fu, Junyi Li, Wenlin Zhang, Kaifeng Guo, Jinning Yang, Jingtong Gao, Xiangyu Zhao (corresponding).

See the repository [`CITATION.cff`](../../CITATION.cff). `[TODO: affiliations and contact email]`.

---

## Licence

```
license: other
```

`[TODO: choose an SPDX licence only after verifying (a) the licence of hfl/chinese-roberta-wwm-ext and (b) rights in the job-ad MLM and silver data. The public model licence must be compatible with the base model.]`

A local laboratory snapshot of the base model contains `config.json` but **no** `LICENSE` file.

---

## Links

| Resource | URL |
|---|---|
| Code | `[TODO: public GitHub URL]` |
| Dataset | `[TODO: Hugging Face dataset URL]` |
| Paper | `[TODO: this paper's arXiv / PeerJ URL]` |
| Zenodo archive | `[TODO: Zenodo DOI]` |
| Legacy homepage | https://sites.google.com/view/cn-skillspan-resources |
