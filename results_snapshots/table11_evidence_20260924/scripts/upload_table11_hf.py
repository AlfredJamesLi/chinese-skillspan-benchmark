#!/usr/bin/env python3
"""Create public Hugging Face repos and upload the six Table-11 LSKT checkpoints.

Does not overwrite AlfredJames/jobbert-zh*. Does not train. Uses the stored Hub token.
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

ROOT = Path("/home/guojingli3/cnss_external_benchmarks_20260921")
EV = ROOT / "TABLE11_EVIDENCE_20260924"
STAGING = Path("/tmp/cnss_table11_hf_staging")
TOKEN_FILE = Path("/home/guojingli3/.cache/huggingface/token")
GH_AUDIT = "https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/audit/table11-evidence-20260924/results_snapshots/table11_evidence_20260924"
GH_GOLD = "https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150_test.jsonl"

CELLS = [
    {
        "short": "xlm-roberta-large",
        "seed": 42,
        "repo": "AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s42",
        "base": "FacebookAI/xlm-roberta-large",
        "rev": "c23d21b0620b635a76227c604d44e43a9f0ee389",
        "epoch": 11,
        "f1": 0.49957662997459773,
        "wsha": "c894df3762a57fd8c10af65a2745db33d94f8aa4476fb4077a9615b1de6ef1f5",
    },
    {
        "short": "xlm-roberta-large",
        "seed": 43,
        "repo": "AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s43",
        "base": "FacebookAI/xlm-roberta-large",
        "rev": "c23d21b0620b635a76227c604d44e43a9f0ee389",
        "epoch": 14,
        "f1": 0.5224489795918368,
        "wsha": "be3caa3ed3a7ebf5a6ffe3d698440bc15c0b4fb8dd856157e74a47ee45fded49",
    },
    {
        "short": "xlm-roberta-large",
        "seed": 44,
        "repo": "AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s44",
        "base": "FacebookAI/xlm-roberta-large",
        "rev": "c23d21b0620b635a76227c604d44e43a9f0ee389",
        "epoch": 14,
        "f1": 0.5445705024311183,
        "wsha": "8946f8cfe5ed772da6d9d97886f2bd1b86be748dc6209d3c9bd1d98d6121b6e3",
    },
    {
        "short": "esco-xlm-roberta-large",
        "seed": 42,
        "repo": "AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s42",
        "base": "jjzha/esco-xlm-roberta-large",
        "rev": "8093cc37ac619a25c5166355acba7be878eb6402",
        "epoch": 19,
        "f1": 0.5160758450123661,
        "wsha": "8d44b7f25de2cebe33a273a6caaf1aebc3076032d3d0fb0eceadb552bf9bc05f",
    },
    {
        "short": "esco-xlm-roberta-large",
        "seed": 43,
        "repo": "AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s43",
        "base": "jjzha/esco-xlm-roberta-large",
        "rev": "8093cc37ac619a25c5166355acba7be878eb6402",
        "epoch": 15,
        "f1": 0.5401459854014599,
        "wsha": "2efb6f69def4211a07a9ad30ee4563fe0dd83569d7e3687676b9077be6acc3aa",
    },
    {
        "short": "esco-xlm-roberta-large",
        "seed": 44,
        "repo": "AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s44",
        "base": "jjzha/esco-xlm-roberta-large",
        "rev": "8093cc37ac619a25c5166355acba7be878eb6402",
        "epoch": 10,
        "f1": 0.5576763485477179,
        "wsha": "98ce01afc2a13fad9cd7db1458c55332df23651d4ce84f6a4d9c653d5b9c9524",
    },
]


def card(c: dict) -> str:
    mean = "0.522 ± 0.022" if c["short"].startswith("xlm") else "0.538 ± 0.021"
    return f"""---
language:
  - zh
pretty_name: Table 11 LSKT linear head ({c["short"]}, seed {c["seed"]})
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
base_model: {c["base"]}
base_model_revision: {c["rev"]}
---

# Table 11 Chinese LSKT linear head (`{c["short"]}`, seed {c["seed"]})

Hub: [`{c["repo"]}`](https://huggingface.co/{c["repo"]})

This is **not** JobBERT-zh CRF, **not** [`AlfredJames/jobbert-zh`](https://huggingface.co/AlfredJames/jobbert-zh) / [`jobbert-zh-v6a`](https://huggingface.co/AlfredJames/jobbert-zh-v6a), and **not** the fill-mask checkpoint [`{c["base"]}`](https://huggingface.co/{c["base"]}). It is a **new** `XLMRobertaForTokenClassification` linear head trained on Silver-plus B2 (2,150 / 169) with `run_chinese_encoder.py`.

Paper cell (three-seed mean ± sample SD, this encoder): **{mean}** typed exact micro-F1 on Gold150. This repository is **seed {c["seed"]} only**.

| Seed | Selected epoch | Gold150 typed exact |
|---:|---:|---:|
| {c["seed"]} | {c["epoch"]} | {c["f1"]:.6f} |

Gold150 is a 150-sentence **human reference freeze** (663 spans, L=2), not a new blind test. Freeze SHA-256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0` ([`data/gold150_test.jsonl`]({GH_GOLD})).

- Evidence pack: {GH_AUDIT}
- Code: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark

## Files

| File | Role | SHA-256 |
|---|---|---|
| `model.safetensors` | Fine-tuned encoder + 9-label linear head | `{c["wsha"]}` |
| `config.json` | `XLMRobertaForTokenClassification`, labels B-/I- K,L,S,T and O | |
| tokenizer files | Copied from `{c["base"]}@{c["rev"]}` | |

Do not load this URL as a masked-LM. The original `{c["base"]}` `lm_head` was discarded; `classifier.weight/bias` were randomly initialized, then **all parameters** (encoder not frozen) were trained in float32.

## Load

```python
from transformers import AutoModelForTokenClassification, AutoTokenizer
repo = "{c["repo"]}"
tok = AutoTokenizer.from_pretrained(repo, use_fast=True)
model = AutoModelForTokenClassification.from_pretrained(repo)
# labels: B-K B-L B-S B-T I-K I-L I-S I-T O
# inputs: list(chinese_text) as words; score the first subword of each character
```

Matching inference: `{GH_AUDIT}/scripts/reinfer_gold150.py` (uses the original on-disk `best/` which is byte-identical to this Hub snapshot).

## Training

- Train: `data/silver_plus_v6a_nocross/train_b2.jsonl` SHA-256 `8921e5fc4b89a0fa83bd942f919c3325546b9938e099b6a13e378736b6717d2e` (2,150)
- Dev (epoch selection only): `dev_b2.jsonl` SHA-256 `e67a3eb5229b94c6c1b552d5f40ece9ad362197236c20cd66b7f2600c9636fef` (169)
- Gold150 never entered the gradient or `history.json`
- AdamW \\(2\\times10^{{-5}}\\), batch 8, 20 epochs, seed {c["seed"]}, character BIO, first-subword, chunk 128
- Scorer: `cnss-lskt-1.2.0` typed exact micro-F1

## Limitations

- Hub `license: other` (same as other Chinese-SkillSpan model cards). GitHub Apache-2.0 is for repository software, not these weights.
- Do not mix with JobBERT-zh CRF ~0.55.
- Do not treat Gold150 as an independent blind test.
- Character-offset LSKT F1 is not an absolute difficulty ranking against English token-span F1.
"""


def link_or_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def stage(c: dict) -> Path:
    src = ROOT / "runs" / "chinese" / "full" / c["short"] / str(c["seed"]) / "best"
    dest = STAGING / c["short"] / str(c["seed"])
    dest.mkdir(parents=True, exist_ok=True)
    for name in (
        "config.json",
        "model.safetensors",
        "tokenizer.json",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "sentencepiece.bpe.model",
    ):
        link_or_copy(src / name, dest / name)
    (dest / "README.md").write_text(card(c), encoding="utf-8")
    return dest


def main() -> int:
    from huggingface_hub import HfApi, whoami

    tok = TOKEN_FILE.read_text().strip()
    user = whoami(token=tok)
    assert user.get("name") == "AlfredJames", user.get("name")
    api = HfApi(token=tok)
    results = []
    for c in CELLS:
        dest = stage(c)
        print(f"[create] {c['repo']}", flush=True)
        api.create_repo(c["repo"], repo_type="model", exist_ok=True, private=False)
        print(f"[upload] {c['repo']} from {dest}", flush=True)
        info = api.upload_folder(
            folder_path=str(dest),
            repo_id=c["repo"],
            repo_type="model",
            commit_message=f"Add Table 11 LSKT linear head {c['short']} seed {c['seed']} (Gold150 exact {c['f1']:.6f}).",
        )
        rec = {
            "repo": c["repo"],
            "url": f"https://huggingface.co/{c['repo']}",
            "commit": getattr(info, "oid", None) or str(info),
            "private": api.repo_info(c["repo"], repo_type="model").private,
            "seed": c["seed"],
            "encoder": c["short"],
            "weights_sha256": c["wsha"],
        }
        print(json.dumps(rec), flush=True)
        results.append(rec)
    out = EV / "hf_publish_receipt.json"
    out.write_text(json.dumps({"whoami": user.get("name"), "repos": results}, indent=2) + "\n", encoding="utf-8")
    print("[done]", out, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
