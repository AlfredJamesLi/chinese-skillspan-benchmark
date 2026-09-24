# Table 11 checkpoints on Hugging Face

Account `AlfredJames`. Six public repositories. Hub LFS SHA-256 matches the training-run `best/model.safetensors`.

| Encoder | Seed | Hub | Gold150 typed exact |
|---|---:|---|---:|
| XLM-R-large | 42 | https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s42 | 0.499577 |
| XLM-R-large | 43 | https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s43 | 0.522449 |
| XLM-R-large | 44 | https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s44 | 0.544571 |
| ESCOXLM-R | 42 | https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s42 | 0.516076 |
| ESCOXLM-R | 43 | https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s43 | 0.540146 |
| ESCOXLM-R | 44 | https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s44 | 0.557676 |

Use these Hub URLs for the Table 11 linear-head weights. The base encoders (`FacebookAI/xlm-roberta-large`, `jjzha/esco-xlm-roberta-large`) and `AlfredJames/jobbert-zh` are different models.

The matching Zenodo record is https://zenodo.org/records/22937244 (concept DOI 10.5281/zenodo.22937244). Corpus files stay on the v0.1.x dataset DOIs.

```python
from transformers import AutoModelForTokenClassification, AutoTokenizer
repo = "AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s42"
tok = AutoTokenizer.from_pretrained(repo, use_fast=True)
model = AutoModelForTokenClassification.from_pretrained(repo)
```
