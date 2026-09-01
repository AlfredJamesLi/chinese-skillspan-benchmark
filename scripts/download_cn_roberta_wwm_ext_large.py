#!/usr/bin/env python3
"""Download factory hfl/chinese-roberta-wwm-ext-large for the vanilla-large V4 CRF arm.

CPU only. Does not touch chinese-roberta-wwm-ext, Gold v2, or existing CRF dirs.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
DEST = ROOT / "Baseline_Models_Collection/chinese-roberta-wwm-ext-large"
REPO = "hfl/chinese-roberta-wwm-ext-large"
IGNORE = ["*.h5", "tf_model*", "flax*", "*.msgpack"]


def ready(dest: Path) -> bool:
    cfg = dest / "config.json"
    weights = list(dest.glob("pytorch_model.bin")) + list(dest.glob("model.safetensors"))
    vocab = dest / "vocab.txt"
    return cfg.is_file() and vocab.is_file() and bool(weights)


def download(endpoint: str | None) -> None:
    from huggingface_hub import snapshot_download

    DEST.mkdir(parents=True, exist_ok=True)
    kw = dict(
        repo_id=REPO,
        local_dir=str(DEST),
        ignore_patterns=IGNORE,
    )
    if endpoint:
        kw["endpoint"] = endpoint
    snapshot_download(**kw)


def main() -> int:
    if ready(DEST):
        print(f"[skip] already have {DEST}", flush=True)
        return 0
    print(f"[download] {REPO} -> {DEST}", flush=True)
    last_err = None
    for endpoint in (os.environ.get("HF_ENDPOINT"), None, "https://hf-mirror.com"):
        try:
            download(endpoint)
            if ready(DEST):
                print(f"[ok] endpoint={endpoint or 'huggingface.co'} dest={DEST}", flush=True)
                return 0
            last_err = RuntimeError(f"download finished but weights missing under {DEST}")
        except Exception as exc:
            last_err = exc
            print(f"[warn] endpoint={endpoint or 'huggingface.co'} failed: {exc}", flush=True)
    print(f"[fail] {last_err}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
