#!/usr/bin/env python3
"""Simple random sample of 150 human-check items from NEW Silver only.

Run only after AI labels exist on
  data/silver_plus_10k_prep_20260913/annotation_input/work.labeled.jsonl
or pass --labeled.

Does not resample if the draw looks hard or error-prone.
Not an independent blind Gold / IAA set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PREP = PAPER / "data/silver_plus_10k_prep_20260913"
SEED = 20260913
SALT = "CNSS_SP_NEW150_QA"
N = 150


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def rank_key(sid: str) -> str:
    return hashlib.sha256(f"{SALT}|{SEED}|{sid}".encode("utf-8")).hexdigest()


def parse_ai_spans(row: dict) -> list:
    lab = row.get("gpt6_label")
    if lab is None:
        lab = row.get("ai_label")
    return lab if isinstance(lab, list) else []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--labeled",
        type=Path,
        default=PREP / "annotation_input/work.labeled.jsonl",
    )
    ap.add_argument("--out-dir", type=Path, default=PREP / "human_qa150")
    args = ap.parse_args()
    if not args.labeled.is_file():
        raise SystemExit(
            f"AI labels not ready: {args.labeled}\n"
            "Do not draw the 150 until new Silver has AI spans. "
            "STATUS remains pending_ai_labels."
        )
    rows = load_jsonl(args.labeled)
    missing = [r.get("id") for r in rows if parse_ai_spans(r) is None and r.get("gpt6_label") is None]
    unlabeled = [r for r in rows if r.get("gpt6_label") is None and r.get("ai_label") is None]
    if unlabeled:
        raise SystemExit(f"{len(unlabeled)} rows still have no AI label; refuse to sample.")
    human350 = {o["id"] for o in load_jsonl(PREP / "human350/ids.jsonl") if o.get("id")}
    frame = [r for r in rows if r.get("id") not in human350]
    if len(frame) < N:
        raise SystemExit(f"frame {len(frame)} < {N}")
    ranked = sorted(frame, key=lambda r: rank_key(str(r["id"])))
    drawn = ranked[:N]
    tasks = []
    ai_only = []
    for i, r in enumerate(drawn, start=1):
        ai = parse_ai_spans(r)
        ai_only.append({
            "id": r["id"],
            "text": r["text"],
            "ai_label": ai,
            "model": r.get("model"),
            "prompt_id": r.get("prompt_id"),
            "annotation_version": r.get("annotation_version"),
        })
        tasks.append({
            "qa_seq": i,
            "id": r["id"],
            "source_domain": r.get("source_domain"),
            "source_file": r.get("source_file"),
            "text": r["text"],
            "ai_label": ai,
            "ai_model": r.get("model"),
            "human_label": None,
            "human_status": "pending",  # pending / confirmed / revised
            "human_notes": "",
            "span_ops": {
                "added": [],
                "deleted": [],
                "type_changed": [],
                "boundary_changed": [],
            },
            "not_independent_blind_gold": True,
            "quality_check_of": "new_silver_only",
        })
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "qa150_ai_original.jsonl", ai_only)
    write_jsonl(args.out_dir / "qa150_human_task.jsonl", tasks)
    write_jsonl(
        args.out_dir / "qa150_ids.txt.jsonl",
        [{"qa_seq": t["qa_seq"], "id": t["id"]} for t in tasks],
    )
    (args.out_dir / "SAMPLING_MANIFEST.json").write_text(
        json.dumps(
            {
                "n": N,
                "seed": SEED,
                "salt": SALT,
                "method": "SRS: sort new-silver ids by sha256(salt|seed|id), take first 150. No replacement.",
                "labeled_path": str(args.labeled),
                "n_frame": len(frame),
                "excluded_human350_from_frame": len(rows) - len(frame),
                "drawn_ids": [t["id"] for t in tasks],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    status = json.loads((args.out_dir / "STATUS.json").read_text(encoding="utf-8"))
    status["status"] = "task_ready_human_check_pending"
    status["drawn"] = N
    (args.out_dir / "STATUS.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {N} tasks to {args.out_dir}")


if __name__ == "__main__":
    main()
