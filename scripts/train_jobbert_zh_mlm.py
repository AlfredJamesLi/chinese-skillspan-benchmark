#!/usr/bin/env python3
"""Small-domain MLM on Chinese job-ad sentences. Offline local encoder only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoModelForMaskedLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


class LineDS(Dataset):
    def __init__(self, path: Path, tokenizer, max_len: int):
        self.texts = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            t = rec.get("text") or rec.get("sentence") or ""
            if t:
                self.texts.append(t)
        self.tok = tokenizer
        self.max_len = max_len

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, i: int) -> dict:
        return self.tok(
            self.texts[i],
            truncation=True,
            max_length=self.max_len,
            padding=False,
            return_special_tokens_mask=True,
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--batch_size", type=int, default=32)
    ap.add_argument("--max_len", type=int, default=128)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    model = AutoModelForMaskedLM.from_pretrained(args.model_dir, local_files_only=True)
    # Standard token MLM. HF whole-word mask needs padded offset_mapping tensors;
    # this local BertTokenizer cannot batch those offsets (failed on the first 1M job).
    ds = LineDS(Path(args.corpus), tok, args.max_len)
    print(
        json.dumps(
            {"n_sents": len(ds), "model": args.model_dir, "wwm": False, "n_gpu": torch.cuda.device_count()},
            ensure_ascii=False,
        ),
        flush=True,
    )
    targs = TrainingArguments(
        output_dir=str(out / "hf_trainer"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.lr,
        weight_decay=0.01,
        warmup_ratio=0.06,
        logging_steps=100,
        save_steps=int(__import__("os").environ.get("SAVE_STEPS", "5000")),
        save_total_limit=int(__import__("os").environ.get("SAVE_TOTAL_LIMIT", "1")),
        seed=args.seed,
        fp16=torch.cuda.is_available(),
        dataloader_num_workers=2,
        report_to=[],
        remove_unused_columns=False,
        ddp_find_unused_parameters=False,
    )
    collator = DataCollatorForLanguageModeling(tok, mlm=True, mlm_probability=0.15)
    trainer_kw = dict(model=model, args=targs, train_dataset=ds, data_collator=collator)
    try:
        trainer = Trainer(**trainer_kw, processing_class=tok)
    except TypeError:
        trainer = Trainer(**trainer_kw, tokenizer=tok)
    result = trainer.train()
    trainer.save_model(str(out / "encoder"))
    tok.save_pretrained(str(out / "encoder"))
    (out / "mlm_summary.json").write_text(
        json.dumps({"train": result.metrics, "n_sents": len(ds), "epochs": args.epochs}, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"mlm_done": True, "metrics": result.metrics, "encoder": str(out / "encoder")}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
