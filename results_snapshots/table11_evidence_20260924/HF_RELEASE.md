# Table 11 Hugging Face release (2026-09-24)

Account: `AlfredJames`. All six repositories are **public**. Hub LFS SHA-256 matches the local `best/model.safetensors`.

| Encoder | Seed | Hub | Gold150 typed exact |
|---|---:|---|---:|
| XLM-R-large | 42 | https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s42 | 0.499577 |
| XLM-R-large | 43 | https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s43 | 0.522449 |
| XLM-R-large | 44 | https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s44 | 0.544571 |
| ESCOXLM-R | 42 | https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s42 | 0.516076 |
| ESCOXLM-R | 43 | https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s43 | 0.540146 |
| ESCOXLM-R | 44 | https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s44 | 0.557676 |

These URLs are the release locations. Do **not** cite `FacebookAI/xlm-roberta-large`, `jjzha/esco-xlm-roberta-large`, or `AlfredJames/jobbert-zh` as these checkpoints.

Zenodo weight deposit was **not** made: this host has no `ZENODO_TOKEN`. Hugging Face satisfies the original “one of HF or Zenodo” rule.

Load example:

```python
from transformers import AutoModelForTokenClassification, AutoTokenizer
repo = "AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s42"
tok = AutoTokenizer.from_pretrained(repo, use_fast=True)
model = AutoModelForTokenClassification.from_pretrained(repo)
```
