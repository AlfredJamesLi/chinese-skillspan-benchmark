#!/usr/bin/env python3
"""Single-card Qwen2.5-14B-Instruct worker for Gold150 shared-prompt patch1.

Uses SLURM-assigned CUDA devices only. Writes its own shard directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RUN_ROOT = Path(__file__).resolve().parents[1]
INFER = RUN_ROOT / "inference"
sys.path.insert(0, str(INFER))
from parser_occurrence_v1_1 import parse_response  # noqa: E402

MODEL_PATH = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Qwen2.5-14B-Instruct")
SYSTEM_NAME = "qwen25-14b-instruct"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(path)


def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def load_json(path: Path):
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def render_user(template: str, sample_id: str, text: str) -> str:
    payload = json.dumps({"id": sample_id, "text": text}, ensure_ascii=False)
    return template.replace("{payload}", payload)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", type=int, required=True)
    ap.add_argument("--phase", choices=["smoke", "formal", "smoke-then-formal"], default="smoke-then-formal")
    args = ap.parse_args()

    freeze = json.loads((RUN_ROOT / "FREEZE_REGISTRY.json").read_text(encoding="utf-8"))
    system = (INFER / "PROMPT_gold150_shared_guidelines_v2_rev2_patch1.DRAFT.system.txt").read_text(encoding="utf-8")
    user_t = (INFER / "USER_TEMPLATE_v2_rev2_patch1.DRAFT.txt").read_text(encoding="utf-8")
    assert sha_text(system) == freeze["frozen_files"]["system"]["sha256"]
    assert sha_file(INFER / "USER_TEMPLATE_v2_rev2_patch1.DRAFT.txt") == freeze["frozen_files"]["user_template"]["sha256"]
    assert sha_file(INFER / "parser_occurrence_v1_1.py") == freeze["frozen_files"]["parser"]["sha256"]

    fp = {
        "protocol": "gold150_shared_guidelines_v2_rev2_patch1",
        "system_name": SYSTEM_NAME,
        "request_model": str(MODEL_PATH),
        "adapter": None,
        "do_sample": False,
        "max_new_tokens": 2048,
        "torch_dtype": "bfloat16",
        "system_sha256": freeze["frozen_files"]["system"]["sha256"],
        "user_sha256": freeze["frozen_files"]["user_template"]["sha256"],
        "parser_sha256": freeze["frozen_files"]["parser"]["sha256"],
        "gold150_sha256": freeze["gold150"]["sha256"],
        "parser_version": "occurrence_v1.1",
        "worker": args.worker,
    }
    out = RUN_ROOT / "runs" / SYSTEM_NAME / f"worker{args.worker}"
    out.mkdir(parents=True, exist_ok=True)
    atomic_write(out / "CONFIG_FINGERPRINT.json", json.dumps(fp, ensure_ascii=False, indent=2) + "\n")
    alloc = {
        "hostname": os.uname().nodename,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "slurm_job_gpus": os.environ.get("SLURM_JOB_GPUS"),
        "slurm_step_gpus": os.environ.get("SLURM_STEP_GPUS"),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "at": utc_now(),
    }
    atomic_write(out / "ALLOC.json", json.dumps(alloc, indent=2) + "\n")
    print(json.dumps({"worker": args.worker, "alloc": alloc}, ensure_ascii=False), flush=True)

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(str(MODEL_PATH), trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        str(MODEL_PATH),
        torch_dtype=torch.bfloat16,
        device_map={"": 0},
        trust_remote_code=True,
    )
    model.eval()
    print(json.dumps({"worker": args.worker, "loaded": True, "cuda": torch.cuda.get_device_name(0)}, ensure_ascii=False), flush=True)

    phases = ["smoke", "formal"] if args.phase == "smoke-then-formal" else [args.phase]
    for phase in phases:
        if phase == "smoke":
            samples = load_jsonl(RUN_ROOT / "inputs" / "synthetic_smoke.jsonl")
        else:
            shard = RUN_ROOT / "inputs" / f"gold150_shard{args.worker}_75.jsonl"
            samples = load_jsonl(shard)
        print(json.dumps({"worker": args.worker, "phase": phase, "n": len(samples)}, ensure_ascii=False), flush=True)
        for sample in samples:
            sid = sample["id"]
            text = sample["text"]
            text_sha = sample.get("text_sha256") or sha_text(text)
            st_path = out / "states" / f"{sid.replace('/', '_')}.json"
            existing = load_json(st_path)
            rkey = sha_text(json.dumps({"fp": {k: fp[k] for k in fp if k != "worker"}, "id": sid, "text_sha256": text_sha}, ensure_ascii=False, sort_keys=True))
            if existing and existing.get("status") == "got_response":
                if existing.get("resume_key") != rkey:
                    raise SystemExit(f"resume conflict {sid}")
                continue
            user = render_user(user_t, sid, text)
            messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
            prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tok(prompt, return_tensors="pt").to(model.device)
            t0 = time.time()
            with torch.no_grad():
                gen = model.generate(
                    **inputs,
                    max_new_tokens=2048,
                    do_sample=False,
                    pad_token_id=tok.eos_token_id,
                )
            new_tokens = gen[0, inputs["input_ids"].shape[1] :]
            content = tok.decode(new_tokens, skip_special_tokens=True)
            elapsed = round(time.time() - t0, 3)
            finish = "length" if int(new_tokens.shape[0]) >= 2048 else "stop"
            parsed = parse_response(content, sid, text)
            rec = {
                "id": sid,
                "text_sha256": text_sha,
                "resume_key": rkey,
                "phase": phase,
                "system": SYSTEM_NAME,
                "worker": args.worker,
                "status": "got_response",
                "content": content,
                "n_new_tokens": int(new_tokens.shape[0]),
                "finish_reason": finish,
                "truncated": finish == "length",
                "elapsed_s": elapsed,
                "outcome": parsed.get("outcome"),
                "format_failed": parsed.get("format_failed"),
                "parse_error": parsed.get("parse_error"),
                "spans": parsed.get("spans") or [],
                "rejected": parsed.get("rejected") or [],
                "completed_at": utc_now(),
                "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            }
            atomic_write(st_path, json.dumps(rec, ensure_ascii=False, indent=2) + "\n")
            append_jsonl(out / "records.jsonl", rec)
            print(
                json.dumps(
                    {
                        "worker": args.worker,
                        "phase": phase,
                        "id": sid,
                        "outcome": rec["outcome"],
                        "n_new_tokens": rec["n_new_tokens"],
                        "finish_reason": finish,
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
            if phase == "smoke" and rec["truncated"] and not content.strip():
                atomic_write(out / "SMOKE_FAIL.json", json.dumps(rec, ensure_ascii=False, indent=2) + "\n")
                return 4
        if phase == "smoke":
            atomic_write(out / "SMOKE_OK.json", json.dumps({"ok": True, "worker": args.worker}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
