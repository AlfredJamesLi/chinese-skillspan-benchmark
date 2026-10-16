#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scripts"))
from train_cn_roberta_crf import BertCRF, label_maps, load_split, predict_tags, write_pred_jsonl  # noqa: E402
from transformers import AutoTokenizer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--batch_size", type=int, default=16)
    ap.add_argument("--max_len", type=int, default=256)
    args = ap.parse_args()
    _, label2id, id2label = label_maps(None)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    model = BertCRF(args.model_dir, n_labels=len(label2id))
    model.load_state_dict(torch.load(args.ckpt, map_location="cpu", weights_only=True), strict=False)
    model.to(device)
    rows = load_split(Path(args.input))
    tags = predict_tags(model, tok, rows, args.max_len, device, args.batch_size, label2id, id2label, None)
    write_pred_jsonl(rows, tags, Path(args.out))
    print(json.dumps({"n": len(rows), "out": args.out}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
