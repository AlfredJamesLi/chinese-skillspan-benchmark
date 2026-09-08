#!/usr/bin/env python3
"""JobBERT extension: DAPT encoder + freshly initialized CRF. Never load released crf/best.pt."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, get_linear_schedule_with_warmup

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(ROOT / "Baseline_Models_Collection/pytorch-crf"))
from train_cn_roberta_crf import (  # noqa: E402
    BertCRF,
    SentDS,
    label_maps,
    load_split,
    predict_tags,
    set_seed,
    typed_f1,
    write_pred_jsonl,
)

BLOCKED_INIT = {
    Path("/home/guojingli3/Chinese-Skillspan-Benchmark/Baseline_Models_Collection/jobbert-zh/crf/best.pt").resolve(),
    Path("/home/guojingli3/Chinese-Skillspan-Benchmark/Baseline_Models_Collection/jobbert-zh-1m/crf/best.pt").resolve(),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", default=str(ROOT / "Baseline_Models_Collection/jobbert-zh"))
    ap.add_argument("--train", required=True)
    ap.add_argument("--dev", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--patience", type=int, default=2)
    ap.add_argument("--batch_size", type=int, default=16)
    ap.add_argument("--max_len", type=int, default=256)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--init_pt", default="", help="Must stay empty. Released CRF is refused.")
    args = ap.parse_args()
    if args.init_pt:
        raise SystemExit("refusing init_pt: extension JobBERT must reinit the task head/CRF")
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    start_iso = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    set_seed(args.seed)
    _, label2id, id2label = label_maps(None)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    model = BertCRF(args.model_dir, n_labels=len(label2id))
    model.to(device)
    train_rows = load_split(Path(args.train))
    dev_rows = load_split(Path(args.dev))
    ds = SentDS(train_rows, tok, args.max_len, label2id, None)
    loader = DataLoader(ds, batch_size=args.batch_size, shuffle=True)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    total = max(1, len(loader) * args.epochs)
    sched = get_linear_schedule_with_warmup(opt, int(0.1 * total), total)
    best_f1, patience, history, steps = -1.0, 0, [], 0
    stop = False
    for epoch in range(1, args.epochs + 1):
        model.train()
        losses = []
        for batch in loader:
            batch.pop("idx")
            batch.pop("word_ids")
            batch.pop("n_words")
            crf_mask = batch.pop("crf_mask").to(device)
            labels = batch.pop("labels").to(device)
            batch = {k: v.to(device) for k, v in batch.items()}
            _, _, loss = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                token_type_ids=batch.get("token_type_ids"),
                labels=labels,
                crf_mask=crf_mask,
            )
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
            losses.append(float(loss.item()))
            steps += 1
        dev_pred = predict_tags(model, tok, dev_rows, args.max_len, device, args.batch_size, label2id, id2label, None)
        dev_f1 = typed_f1(dev_rows, dev_pred, None)
        row = {"epoch": epoch, "steps": steps, "train_loss": sum(losses) / max(1, len(losses)), "dev_typed_f1": dev_f1}
        history.append(row)
        print(json.dumps(row), flush=True)
        if dev_f1 > best_f1 + 1e-4:
            best_f1 = dev_f1
            patience = 0
            torch.save(model.state_dict(), out / "best.pt")
            write_pred_jsonl(dev_rows, dev_pred, out / "dev_pred.jsonl")
        else:
            patience += 1
        if stop or patience >= args.patience:
            break
    if not (out / "best.pt").is_file():
        torch.save(model.state_dict(), out / "best.pt")
        write_pred_jsonl(
            dev_rows,
            predict_tags(model, tok, dev_rows, args.max_len, device, args.batch_size, label2id, id2label, None),
            out / "dev_pred.jsonl",
        )
    (out / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    elapsed = time.time() - t0
    peak = float(torch.cuda.max_memory_allocated()) / (1024**3) if torch.cuda.is_available() else 0.0
    resource = {
        "job_id": os.environ.get("SLURM_JOB_ID", "na"),
        "hostname": os.uname().nodename,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "start_iso": start_iso,
        "end_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "seconds": elapsed,
        "peak_allocated_gib": peak,
        "gpu_hours": elapsed / 3600.0,
        "init": "reinit_crf",
        "released_crf_not_loaded": True,
    }
    (out / "RESOURCE.json").write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")
    (out / "run_config.json").write_text(
        json.dumps(
            {
                **vars(args),
                "best_dev_typed_f1": best_f1,
                "steps": steps,
                "init": "reinit_crf",
                "released_crf_not_loaded": True,
                "seconds": elapsed,
                "peak_allocated_gib": peak,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"done": True, "best_dev": best_f1, "steps": steps, "init": "reinit_crf"}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
