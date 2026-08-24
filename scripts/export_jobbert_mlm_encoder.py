#!/usr/bin/env python3
"""Export Bert encoder from a HuggingFace MLM checkpoint directory."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from transformers import AutoModelForMaskedLM, AutoTokenizer


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True, help="hf_trainer/checkpoint-NNNNN")
    ap.add_argument("--out_dir", required=True, help="encoder output dir")
    args = ap.parse_args()
    ckpt = Path(args.checkpoint)
    enc = Path(args.out_dir)
    enc.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(str(ckpt), local_files_only=True)
    mlm = AutoModelForMaskedLM.from_pretrained(str(ckpt), local_files_only=True)
    mlm.bert.save_pretrained(str(enc))
    tok.save_pretrained(str(enc))
    state_path = ckpt / "trainer_state.json"
    meta = {"from_checkpoint": str(ckpt)}
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        meta["global_step"] = state.get("global_step")
        meta["epoch"] = state.get("epoch")
    (enc / "export_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
