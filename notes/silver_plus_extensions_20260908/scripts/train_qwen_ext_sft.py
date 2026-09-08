#!/usr/bin/env python3
"""Qwen LoRA SFT without demos. Save each epoch. Select on frozen-dev condition A only."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch
from peft import LoraConfig, get_peft_model
from torch.utils.data import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainerCallback, TrainingArguments

ROOT = Path("/home/guojingli3/Chinese-Skillspan-Benchmark")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scripts"))
from qwen_ext_protocol import MAX_NEW_TOKENS, build_user_prompt, format_target, parse_model_output, pred_row  # noqa: E402


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


class SpanSFT(Dataset):
    def __init__(self, rows, tok):
        self.rows = rows
        self.tok = tok

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, i):
        r = self.rows[i]
        user = build_user_prompt(r["sentence"], demos=None)
        assistant = format_target(r.get("spans") or [])
        text = self.tok.apply_chat_template(
            [{"role": "user", "content": user}, {"role": "assistant", "content": assistant}],
            tokenize=False,
            add_generation_prompt=False,
        )
        prompt = self.tok.apply_chat_template(
            [{"role": "user", "content": user}], tokenize=False, add_generation_prompt=True
        )
        full = self.tok(text, add_special_tokens=False)
        pref = self.tok(prompt, add_special_tokens=False)
        input_ids = full["input_ids"]
        labels = [-100] * len(pref["input_ids"]) + input_ids[len(pref["input_ids"]) :]
        if len(labels) < len(input_ids):
            labels += [-100] * (len(input_ids) - len(labels))
        labels = labels[: len(input_ids)]
        return {"input_ids": input_ids, "attention_mask": [1] * len(input_ids), "labels": labels}


def collate(features, pad_id):
    m = max(len(f["input_ids"]) for f in features)
    batch = {"input_ids": [], "attention_mask": [], "labels": []}
    for f in features:
        n = m - len(f["input_ids"])
        batch["input_ids"].append(f["input_ids"] + [pad_id] * n)
        batch["attention_mask"].append(f["attention_mask"] + [0] * n)
        batch["labels"].append(f["labels"] + [-100] * n)
    return {k: torch.tensor(v) for k, v in batch.items()}


def generate_rows(model, tok, rows, max_new_tokens: int) -> list[dict]:
    model.eval()
    preds = []
    for r in rows:
        user = build_user_prompt(r["sentence"], demos=None)
        ids = tok.apply_chat_template(
            [{"role": "user", "content": user}], add_generation_prompt=True, return_tensors="pt"
        )
        if hasattr(ids, "input_ids"):
            ids = ids.input_ids
        ids = ids.to(model.device)
        with torch.no_grad():
            gen = model.generate(
                ids,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tok.eos_token_id,
                eos_token_id=tok.eos_token_id,
            )
        text = tok.decode(gen[0, ids.shape[-1] :], skip_special_tokens=True)
        parsed = parse_model_output(text, r["sentence"])
        rid = r.get("id") or r.get("source_id")
        preds.append(pred_row(rid, r["sentence"], parsed))
    return preds


def score_dev(gold_path: Path, pred_path: Path) -> dict:
    sys.path.insert(0, str(PAPER / "scorer"))
    from score_lskt import score  # noqa: E402

    sc = score(str(gold_path), str(pred_path), align_mode="official", n_boot=0)
    return {
        "typed_exact_f1": sc["typed_exact"]["f1"],
        "typed_relaxed_f1": sc["typed_relaxed"]["f1"],
        "alignment_ok": sc.get("alignment_ok"),
        "scorer_version": sc.get("scorer_version"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--train", required=True)
    ap.add_argument("--dev", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--batch_size", type=int, default=1)
    ap.add_argument("--grad_accum", type=int, default=16)
    ap.add_argument("--max_new_tokens", type=int, default=MAX_NEW_TOKENS)
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "right"
    train_rows = load_jsonl(Path(args.train))
    dev_rows = load_jsonl(Path(args.dev))
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir, local_files_only=True, torch_dtype=torch.bfloat16
    )
    model.cuda()
    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    model = get_peft_model(model, lora)
    history = []

    class EpochDevA(TrainerCallback):
        def on_epoch_end(self, args_t, state, control, **kwargs):
            ep = int(round(state.epoch))
            ev_model = kwargs["model"]
            ep_dir = out / f"epoch_{ep}"
            ev_model.save_pretrained(ep_dir)
            tok.save_pretrained(ep_dir)
            preds = generate_rows(ev_model, tok, dev_rows, args.max_new_tokens)
            pred_path = ep_dir / "dev_A_pred.jsonl"
            pred_path.write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in preds), encoding="utf-8")
            sc = score_dev(Path(args.dev), pred_path)
            parse_ok = sum(1 for p in preds if p["parse_status"] in {"ok", "partial"} or not p["pred_spans"])
            row = {"epoch": ep, **sc, "n_dev": len(preds), "parse_nonempty_or_empty_ok": parse_ok}
            history.append(row)
            ev_model.train()
            print(json.dumps(row, ensure_ascii=False), flush=True)

    targs = TrainingArguments(
        output_dir=str(out / "hf"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        logging_steps=10,
        save_strategy="no",
        bf16=True,
        report_to=[],
        seed=args.seed,
        remove_unused_columns=False,
    )
    trainer = Trainer(
        model=model,
        args=targs,
        train_dataset=SpanSFT(train_rows, tok),
        data_collator=lambda fs: collate(fs, tok.pad_token_id),
        callbacks=[EpochDevA()],
    )
    trainer.train()

    best_i, best = 0, history[0]
    for i, row in enumerate(history):
        if row["typed_exact_f1"] > best["typed_exact_f1"] + 1e-4:
            best_i, best = i, row
    selected = history[best_i]
    src = out / f"epoch_{selected['epoch']}"
    dst = out / "adapter"
    if dst.exists():
        pass
    # copy selected adapter files
    import shutil

    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    (out / "selected_checkpoint.json").write_text(
        json.dumps(
            {
                "selected_epoch": selected["epoch"],
                "metric": "dev_A_typed_exact_f1",
                "value": selected["typed_exact_f1"],
                "tie_rule": "earlier_epoch_if_delta_le_1e-4",
                "gold150_not_used": True,
                "sft_contains_demos": False,
                "history": history,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    elapsed = time.time() - t0
    peak = float(torch.cuda.max_memory_allocated()) / (1024**3) if torch.cuda.is_available() else 0.0
    (out / "RESOURCE.json").write_text(
        json.dumps(
            {
                "job_id": os.environ.get("SLURM_JOB_ID", "na"),
                "hostname": os.uname().nodename,
                "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
                "seconds": elapsed,
                "peak_allocated_gib": peak,
                "gpu_hours": elapsed / 3600.0,
                "end_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (out / "run_config.json").write_text(
        json.dumps({**vars(args), "seconds": elapsed, "peak_allocated_gib": peak, "device": str(torch.cuda.current_device()) if torch.cuda.is_available() else "cpu"}, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"done": True, "selected_epoch": selected["epoch"], "dev_A_f1": selected["typed_exact_f1"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
