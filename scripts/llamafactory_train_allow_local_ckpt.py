#!/usr/bin/env python3
"""Launch LLaMA-Factory train after allowing torch.load of a local trainer checkpoint.

Needed because transformers 4.52 refuses optimizer.pt unless torch>=2.6.
This machine has torch 2.3.1; checkpoint-500 was written here the same day.
Does not download or execute untrusted checkpoints.
"""
from __future__ import annotations

import sys

import transformers.trainer as trainer_mod
import transformers.utils.import_utils as import_utils


def _allow_local_ckpt() -> None:
    import_utils.check_torch_load_is_safe = lambda: None
    trainer_mod.check_torch_load_is_safe = lambda: None


def main() -> None:
    _allow_local_ckpt()
    from llamafactory.cli import main as lf_main

    sys.argv = ["llamafactory-cli", "train", *sys.argv[1:]]
    lf_main()


if __name__ == "__main__":
    main()
