# Chinese JobBERT CRF head

File `best.pt` is the V4 silver CRF checkpoint trained on top of the Chinese JobBERT encoder (`encoder_ckpt65000`). It is a `BertCRF` `state_dict` from `scripts/train_cn_roberta_crf.py`, not an `AutoModelForTokenClassification` dump.

Load the encoder and tokenizer from the repository root (`config.json`, `model.safetensors`, `tokenizer.json`). Then:

```python
import torch
from scripts.train_cn_roberta_crf import BertCRF  # paper repository

model = BertCRF("path/to/this/repo", n_labels=9)
model.load_state_dict(torch.load("crf/best.pt", map_location="cpu"))
```

Do not upload or redistribute `last.ckpt`. Paper-main scoring still requires jieba alignment (`scripts/cws_snap.py`) and `scorer/score_lskt.py --align-mode official`.
