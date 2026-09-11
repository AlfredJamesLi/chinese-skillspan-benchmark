#!/usr/bin/env python3
"""Official this-round Qwen Gold inference: JSON-offset SFT only (0.1215±0.0092).

Not shared-prompt 0.5403. Not V4 hybrid 0.4331. Adapters are not published.
Requires `--protocol json_offset`. No IEEE Access default weights.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

import sys

from cnss_paths import paper_root

PAPER = paper_root()
sys.path.insert(0, str(PAPER / "scripts"))
from qwen_ext_protocol import MAX_NEW_TOKENS, PROTOCOL_ID, build_user_prompt, parse_model_output, pred_row  # noqa: E402


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump_jsonl(p: Path, rows: list[dict]) -> None:
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def generate_one(model, tok, sentence, max_new_tokens):
    user = build_user_prompt(sentence, demos=None)
    ids = tok.apply_chat_template(
        [{"role": "user", "content": user}], add_generation_prompt=True, return_tensors="pt"
    )
    if hasattr(ids, "input_ids"):
        ids = ids.input_ids
    ids = ids.to(model.device)
    t0 = time.time()
    with torch.no_grad():
        gen = model.generate(
            ids,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tok.eos_token_id,
            eos_token_id=tok.eos_token_id,
        )
    dt = time.time() - t0
    text = tok.decode(gen[0, ids.shape[-1] :], skip_special_tokens=True)
    n_in = int(ids.shape[-1])
    n_out = int(gen.shape[-1] - ids.shape[-1])
    parsed = parse_model_output(text, sentence)
    truncated = n_out >= max_new_tokens
    if truncated and parsed["status"] in {"ok", "partial"}:
        parsed["failures"] = list(parsed["failures"]) + [{"reason": "max_new_tokens_reached"}]
        if parsed["status"] == "ok":
            parsed["status"] = "partial"
    cost = {"n_input_tokens": n_in, "n_output_tokens": n_out, "seconds": dt, "truncated": truncated}
    return parsed, cost


def run_sft_infer(
    model_dir: str,
    adapter_dir: str,
    queries_path: str,
    out_dir: str,
    max_new_tokens: int = MAX_NEW_TOKENS,
    local_files_only: bool = True,
) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    queries = load_jsonl(Path(queries_path))
    tok = AutoTokenizer.from_pretrained(model_dir, local_files_only=local_files_only, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_dir, local_files_only=local_files_only, torch_dtype=torch.bfloat16)
    model = PeftModel.from_pretrained(model, adapter_dir)
    model.cuda()
    model.eval()
    preds = []
    for r in queries:
        qid = r.get("id") or r.get("source_id")
        sent = r.get("sentence") or r.get("text")
        parsed, cost = generate_one(model, tok, sent, max_new_tokens)
        extra = {"condition": "SFT", "demo_ids": [], **cost}
        preds.append(pred_row(qid, sent, parsed, extra))
    dump_jsonl(out / "pred.jsonl", preds)
    dump_jsonl(out / "pred_A.jsonl", preds)
    fail_rows = [p for p in preds if p.get("parse_status") not in {"ok"}]
    dump_jsonl(out / "failures.jsonl", fail_rows)
    dump_jsonl(out / "failures_A.jsonl", fail_rows)
    peak = float(torch.cuda.max_memory_allocated()) / (1024**3) if torch.cuda.is_available() else 0.0
    resource = {
        "job_id": os.environ.get("SLURM_JOB_ID", "na"),
        "hostname": os.uname().nodename,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "start_iso": None,
        "end_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "seconds": time.time() - t0,
        "peak_allocated_gib": peak,
        "gpu_hours": (time.time() - t0) / 3600.0,
        "n_pred": len(preds),
        "condition": "SFT",
        "retrieval_used": False,
    }
    (out / "RESOURCE.json").write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")
    (out / "infer_config.json").write_text(
        json.dumps(
            {
                "model_dir": model_dir,
                "adapter_dir": adapter_dir,
                "queries": queries_path,
                "max_new_tokens": max_new_tokens,
                "do_sample": False,
                "demos": False,
                "official_condition": "SFT",
                "protocol": "json_offset",
                "protocol_id": PROTOCOL_ID,
                "not_shared_prompt_0.5403": True,
                "not_comparable_to_0.4331": True,
                "knn_random_not_run": True,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"n": len(preds), "seconds": resource["seconds"], "out": str(out / "pred.jsonl")}, ensure_ascii=False), flush=True)
    return out / "pred.jsonl"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--adapter_dir", required=True)
    ap.add_argument("--queries", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--max_new_tokens", type=int, default=MAX_NEW_TOKENS)
    ap.add_argument(
        "--protocol",
        required=True,
        choices=["json_offset"],
        help="Must be json_offset. This inferencer is not shared-prompt 0.5403.",
    )
    ap.add_argument("--local_files_only", action="store_true", default=True)
    args = ap.parse_args()
    run_sft_infer(
        args.model_dir,
        args.adapter_dir,
        args.queries,
        args.out_dir,
        args.max_new_tokens,
        local_files_only=args.local_files_only,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
