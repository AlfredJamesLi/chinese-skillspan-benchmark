#!/usr/bin/env python3
"""Qwen2.5-14B LoRA SFT on public-API Silver-2500 with silver_public_api_v1.0.

Recipe copied from job 50981 / output/qwen_shared_guidelines_sft_20260910:
r=16 α=32 dropout 0.05 q/k/v/o, lr 1e-4, batch 1×16, bf16, patience 2, max 6
epochs, seeds 42/43/44, assistant-only loss, gradient checkpointing.

Prompt, train file, and test file are new. Not Gold150 0.5403. Not paper-main.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

import torch
from peft import LoraConfig, PeftModel, get_peft_model
from torch.utils.data import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainerCallback, TrainingArguments

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
from qwen_silver2500_sft_lib import (  # noqa: E402
    MAX_NEW,
    MAX_SEQ,
    MODEL_PATH,
    OUT_ROOT,
    PROTOCOL_ID,
    PROMPT_PATH,
    SILVER_DATA,
    convert_split,
    dump_json,
    dump_jsonl,
    gold_row,
    load_jsonl,
    load_system,
    parse_response,
    pred_row,
    render_user,
    sha256_file,
)
from score_lskt import score  # noqa: E402


def encode_pair(tok, system: str, user: str, assistant: str) -> dict:
    full = tok.apply_chat_template(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        tokenize=False,
        add_generation_prompt=False,
    )
    prompt = tok.apply_chat_template(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        tokenize=False,
        add_generation_prompt=True,
    )
    full_ids = tok(full, add_special_tokens=False)["input_ids"]
    pref_ids = tok(prompt, add_special_tokens=False)["input_ids"]
    if full_ids[: len(pref_ids)] != pref_ids:
        raise RuntimeError("chat template prefix not stable")
    if len(full_ids) > MAX_SEQ:
        raise RuntimeError(f"sequence {len(full_ids)} exceeds max_seq_length {MAX_SEQ}")
    labels = [-100] * len(pref_ids) + full_ids[len(pref_ids) :]
    return {
        "input_ids": full_ids,
        "attention_mask": [1] * len(full_ids),
        "labels": labels,
    }


class ChatSFT(Dataset):
    def __init__(self, rows, tok, system):
        self.items = []
        for r in rows:
            user = render_user(r["id"], r["text"])
            self.items.append(encode_pair(tok, system, user, r["assistant"]) | {"id": r["id"]})

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]


def collate(features, pad_id):
    m = max(len(f["input_ids"]) for f in features)
    batch = {"input_ids": [], "attention_mask": [], "labels": []}
    for f in features:
        n = m - len(f["input_ids"])
        batch["input_ids"].append(f["input_ids"] + [pad_id] * n)
        batch["attention_mask"].append(f["attention_mask"] + [0] * n)
        batch["labels"].append(f["labels"] + [-100] * n)
    return {k: torch.tensor(v) for k, v in batch.items()}


def score_pred(gold_rows: list[dict], pred_rows: list[dict], tmp: Path) -> dict:
    tmp.mkdir(parents=True, exist_ok=True)
    gpath = tmp / "dev_gold.jsonl"
    ppath = tmp / "dev_pred.jsonl"
    dump_jsonl(gpath, gold_rows)
    dump_jsonl(ppath, pred_rows)
    sc = score(str(gpath), str(ppath), align_mode="official", n_boot=0)
    return {
        "typed_exact_f1": sc["typed_exact"]["f1"],
        "typed_exact_p": sc["typed_exact"]["precision"],
        "typed_exact_r": sc["typed_exact"]["recall"],
        "typed_relaxed_f1": sc["typed_relaxed"]["f1"],
        "alignment_ok": sc.get("alignment_ok"),
        "scorer_version": sc.get("scorer_version"),
        "n_matched": sc.get("n_matched"),
    }


def generate_split(model, tok, system, rows) -> list[dict]:
    model.eval()
    was_cache = model.config.use_cache
    model.config.use_cache = True
    out = []
    for i, r in enumerate(rows, 1):
        user = render_user(r["id"], r["text"])
        prompt = tok.apply_chat_template(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = tok(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            gen = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW,
                do_sample=False,
                pad_token_id=tok.pad_token_id,
                eos_token_id=tok.eos_token_id,
            )
        new = gen[0, inputs["input_ids"].shape[1] :]
        content = tok.decode(new, skip_special_tokens=True)
        parsed = parse_response(content, r["id"], r["text"])
        rec = pred_row(
            r["id"],
            r["text"],
            parsed,
            {
                "n_new_tokens": int(new.shape[0]),
                "truncated": int(new.shape[0]) >= MAX_NEW,
                "raw": content,
            },
        )
        out.append(rec)
        if i % 20 == 0:
            print(json.dumps({"gen": i, "n": len(rows)}), flush=True)
    model.config.use_cache = was_cache
    return out


def select_best(history: list[dict]) -> dict:
    best = history[0]
    for row in history[1:]:
        if row["typed_exact_f1"] > best["typed_exact_f1"] + 1e-4:
            best = row
    return best


def ensure_converted() -> dict:
    data = OUT_ROOT / "data"
    train_p = data / "train.jsonl"
    dev_p = data / "dev.jsonl"
    if train_p.is_file() and dev_p.is_file():
        return {"train": train_p, "dev": dev_p, "n_train": sum(1 for _ in open(train_p)), "n_dev": sum(1 for _ in open(dev_p))}
    data.mkdir(parents=True, exist_ok=True)
    train_rows = convert_split(SILVER_DATA / "train.jsonl")
    dev_rows = convert_split(SILVER_DATA / "dev.jsonl")
    dump_jsonl(train_p, train_rows)
    dump_jsonl(dev_p, dev_rows)
    dump_json(
        data / "MANIFEST.json",
        {
            "protocol": PROTOCOL_ID,
            "prompt_path": str(PROMPT_PATH),
            "prompt_sha256": sha256_file(PROMPT_PATH),
            "n_train": len(train_rows),
            "n_dev": len(dev_rows),
            "source_train": str(SILVER_DATA / "train.jsonl"),
            "source_dev": str(SILVER_DATA / "dev.jsonl"),
            "not_v6a": True,
            "not_gold150": True,
            "test_is_silver_dev": True,
        },
    )
    return {"train": train_p, "dev": dev_p, "n_train": len(train_rows), "n_dev": len(dev_rows)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True, choices=[42, 43, 44])
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--patience", type=int, default=2)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--batch_size", type=int, default=1)
    ap.add_argument("--grad_accum", type=int, default=16)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    paths = ensure_converted()
    out = OUT_ROOT / "runs" / f"seed{args.seed}"
    out.mkdir(parents=True, exist_ok=True)
    state_path = out / "TRAIN_STATE.json"
    if state_path.is_file() and not args.resume:
        st = json.loads(state_path.read_text(encoding="utf-8"))
        if st.get("status") == "completed" and (out / "selected_checkpoint.json").is_file():
            print(json.dumps({"skip": True, "seed": args.seed, **st}), flush=True)
            return 0
        raise SystemExit(f"{state_path} exists; pass --resume")

    system = load_system()
    train_rows = load_jsonl(paths["train"])
    dev_rows = load_jsonl(paths["dev"])
    gold_dev = [gold_row(r) for r in load_jsonl(SILVER_DATA / "dev.jsonl")]

    tok = AutoTokenizer.from_pretrained(str(MODEL_PATH), local_files_only=True, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        attn_implementation="flash_attention_2",
        device_map={"": 0},
    )
    print(
        json.dumps(
            {
                "attn_implementation": getattr(model.config, "_attn_implementation", None),
                "device": str(next(model.parameters()).device),
            }
        ),
        flush=True,
    )
    history = []
    hist_path = out / "epoch_history.json"
    if hist_path.is_file():
        history = json.loads(hist_path.read_text(encoding="utf-8"))
    last_ep = max((int(h["epoch"]) for h in history), default=0)
    remaining = max(args.epochs - last_ep, 0)
    adapter_dir = out / f"epoch_{last_ep}" if last_ep else None
    if last_ep and not args.resume:
        raise SystemExit(f"{out} has epoch_history through {last_ep}; pass --resume")
    if args.resume and last_ep and not (adapter_dir / "adapter_config.json").is_file():
        raise SystemExit(f"resume missing adapter at {adapter_dir}")
    if remaining == 0 and history:
        selected = select_best(history)
        dst = out / "adapter"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(out / f"epoch_{selected['epoch']}", dst)
        dump_json(
            out / "selected_checkpoint.json",
            {
                "selected_epoch": selected["epoch"],
                "metric": "silver_dev_typed_exact_f1",
                "value": selected["typed_exact_f1"],
                "tie_rule": "earlier_epoch_if_delta_le_1e-4",
                "patience": args.patience,
                "test_set": "public_api_silver2500_dev",
                "n_test": len(dev_rows),
                "gold150_not_used": True,
                "protocol": PROTOCOL_ID,
                "not_shared_prompt_0.5403": True,
                "not_comparable_to_0.4331": True,
                "resumed_finalize_only": True,
                "history": history,
            },
        )
        dump_json(out / "TRAIN_STATE.json", {"status": "completed", "selected_epoch": selected["epoch"], "dev_f1": selected["typed_exact_f1"]})
        print(json.dumps({"done": True, "finalize_only": True, "selected_epoch": selected["epoch"], "silver_dev_f1": selected["typed_exact_f1"]}), flush=True)
        return 0

    lora_cfg = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    if adapter_dir is not None:
        model = PeftModel.from_pretrained(model, str(adapter_dir), is_trainable=True)
        print(json.dumps({"resume_adapter": str(adapter_dir), "last_ep": last_ep, "remaining_epochs": remaining}), flush=True)
    else:
        model = get_peft_model(model, lora_cfg)
    model.config.use_cache = False
    model.enable_input_require_grads()

    class EpochDev(TrainerCallback):
        def on_epoch_end(self, args_t, state, control, **kwargs):
            ep = last_ep + int(round(state.epoch))
            ev = kwargs["model"]
            ep_dir = out / f"epoch_{ep}"
            ev.save_pretrained(ep_dir)
            tok.save_pretrained(ep_dir)
            print(json.dumps({"epoch_eval_start": ep, "n_dev": len(dev_rows)}), flush=True)
            preds = generate_split(ev, tok, system, dev_rows)
            dump_jsonl(ep_dir / "dev_pred.jsonl", preds)
            sc = score_pred(gold_dev, preds, ep_dir)
            outcomes = {}
            for p in preds:
                outcomes[p.get("outcome") or "unknown"] = outcomes.get(p.get("outcome") or "unknown", 0) + 1
            row = {
                "epoch": ep,
                **sc,
                "n_dev": len(preds),
                "outcomes": outcomes,
                "n_truncated": sum(1 for p in preds if p.get("truncated")),
                "n_format_failed": sum(1 for p in preds if p.get("format_failed")),
            }
            history[:] = [h for h in history if int(h["epoch"]) != ep]
            history.append(row)
            history.sort(key=lambda r: int(r["epoch"]))
            (out / "epoch_history.json").write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps(row, ensure_ascii=False), flush=True)
            best = select_best(history)
            if ep - best["epoch"] >= args.patience:
                control.should_training_stop = True
                print(json.dumps({"early_stop": True, "patience": args.patience, "best_epoch": best["epoch"]}), flush=True)
            ev.train()

    targs = TrainingArguments(
        output_dir=str(out / "hf"),
        num_train_epochs=remaining if args.resume and last_ep else args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        warmup_ratio=0.0,
        weight_decay=0.0,
        lr_scheduler_type="linear",
        optim="adamw_torch",
        logging_steps=10,
        save_strategy="no",
        bf16=True,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        report_to=[],
        seed=args.seed,
        remove_unused_columns=False,
        dataloader_num_workers=0,
    )
    trainer = Trainer(
        model=model,
        args=targs,
        train_dataset=ChatSFT(train_rows, tok, system),
        data_collator=lambda fs: collate(fs, tok.pad_token_id),
        callbacks=[EpochDev()],
    )
    t0 = time.time()
    trainer.train()
    selected = select_best(history)
    dst = out / "adapter"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(out / f"epoch_{selected['epoch']}", dst)
    dump_json(
        out / "selected_checkpoint.json",
        {
            "selected_epoch": selected["epoch"],
            "metric": "silver_dev_typed_exact_f1",
            "value": selected["typed_exact_f1"],
            "tie_rule": "earlier_epoch_if_delta_le_1e-4",
            "patience": args.patience,
            "test_set": "public_api_silver2500_dev",
            "n_test": len(dev_rows),
            "gold150_not_used": True,
            "protocol": PROTOCOL_ID,
            "not_shared_prompt_0.5403": True,
            "not_comparable_to_0.4331": True,
            "resumed_from_epoch": last_ep or None,
            "history": history,
        },
    )
    dump_json(
        out / "run_config.json",
        {
            **vars(args),
            "model_path": str(MODEL_PATH),
            "prompt_sha256": sha256_file(PROMPT_PATH),
            "max_seq_length": MAX_SEQ,
            "max_new_tokens": MAX_NEW,
            "gradient_checkpointing": True,
            "seconds": time.time() - t0,
            "hostname": os.uname().nodename,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "protocol": PROTOCOL_ID,
        },
    )
    dump_json(out / "TRAIN_STATE.json", {"status": "completed", "selected_epoch": selected["epoch"], "dev_f1": selected["typed_exact_f1"]})
    print(json.dumps({"done": True, "selected_epoch": selected["epoch"], "silver_dev_f1": selected["typed_exact_f1"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
