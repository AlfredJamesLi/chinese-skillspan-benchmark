#!/usr/bin/env python3
"""SOP-v4 extract on repartition_v1 test, one ID shard per GPU.

Does not overwrite P2-2601 Qwen preds or Gold v2. No commercial API.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from expand_goldstyle_train import apply_text_spans, load_local  # noqa: E402
from run_qwen25_sopv4_p2_2601 import (  # noqa: E402
    MODEL_PATH,
    ALT_MODEL,
    PROMPT_PATH,
    USER_PREFIX,
    chat_one,
    load_done,
    parse_results,
    spans_recoverable,
    tokens_of,
)
from score_lskt import rec_id  # noqa: E402

GOLD = PAPER / "data/repartition_v1/test.jsonl"


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def infer_shard(ids: list[str], gold_map: dict, tok, model, prompt: str, raw_path: Path) -> None:
    done = load_done(raw_path)
    pending = [i for i in ids if i not in done]
    print(json.dumps({"done": len(done), "pending": len(pending), "raw": str(raw_path)}, ensure_ascii=False), flush=True)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    with raw_path.open("a", encoding="utf-8") as fout:
        for n, cid in enumerate(pending, 1):
            rec = gold_map[cid]
            sent = rec.get("sentence") or ""
            payload = [{"id": cid, "sentence": sent}]
            err = None
            text = ""
            parsed = None
            t0 = time.time()
            for max_new in (2048, 4096):
                for _ in range(3):
                    try:
                        text = chat_one(tok, model, prompt, payload, max_new)
                        parsed = parse_results(text, [cid])
                        if parsed[0].get("comment") == "missing_in_model_output":
                            raise ValueError("missing_in_model_output")
                        ok_spans, bad = spans_recoverable(sent, parsed[0]["spans"])
                        if not ok_spans:
                            parsed[0]["spans"] = [sp for sp in parsed[0]["spans"] if sp["text"] in sent]
                            parsed[0]["dropped_not_in_sentence"] = bad
                        err = None
                        break
                    except Exception as e:
                        err = f"{type(e).__name__}: {e}"
                        time.sleep(0.2)
                if err is None:
                    break
            fout.write(
                json.dumps(
                    {
                        "id": cid,
                        "sentence": sent,
                        "raw": text,
                        "parsed": parsed[0] if parsed else {"id": cid, "spans": [], "comment": "parse_fail"},
                        "error": err,
                        "elapsed_s": round(time.time() - t0, 3),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            fout.flush()
            if n % 10 == 0 or n == len(pending):
                print(json.dumps({"wrote": n, "of": len(pending), "id": cid, "err": bool(err)}), flush=True)


def materialize(gold_map: dict, ids: list[str], raw_path: Path) -> list[dict]:
    raw_by = load_done(raw_path)
    rows = []
    for cid in ids:
        rec = gold_map[cid]
        sent = rec.get("sentence") or ""
        raw = raw_by.get(cid) or {}
        parsed = raw.get("parsed") or {"id": cid, "spans": [], "comment": "missing_raw"}
        tags, miss = apply_text_spans({"tokens": tokens_of(rec), "sentence": sent}, parsed.get("spans") or [])
        rows.append(
            {
                "id": cid,
                "sentence": sent,
                "tokens": tokens_of(rec),
                "pred_tags": tags,
                "list_of_selection_bio4": tags,
                "unaligned": miss,
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", type=int, required=True)
    ap.add_argument("--n-shards", type=int, default=2)
    ap.add_argument("--gold", default=str(GOLD))
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--model-dir", default="")
    ap.add_argument("--merge-only", action="store_true")
    args = ap.parse_args()
    gold_rows = load_jsonl(Path(args.gold))
    gold_map = {rec_id(r): r for r in gold_rows}
    ids = [rec_id(r) for r in gold_rows]
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.merge_only:
        merged_raw = out_dir / "raw.jsonl"
        parts = [load_done(out_dir / f"shard_{i}.raw.jsonl") for i in range(args.n_shards)]
        by_id = {}
        for p in parts:
            by_id.update(p)
        missing = [i for i in ids if i not in by_id]
        if missing:
            print(json.dumps({"status": "incomplete", "missing": len(missing)}), flush=True)
            return 3
        with merged_raw.open("w", encoding="utf-8") as f:
            for cid in ids:
                f.write(json.dumps(by_id[cid], ensure_ascii=False) + "\n")
        rows = materialize(gold_map, ids, merged_raw)
        pred = out_dir / "test_pred.jsonl"
        pred.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
        print(json.dumps({"status": "merged", "n": len(rows), "pred": str(pred)}), flush=True)
        return 0

    shard_ids = [i for n, i in enumerate(ids) if n % args.n_shards == args.shard]
    raw_path = out_dir / f"shard_{args.shard}.raw.jsonl"
    model_dir = args.model_dir or (str(MODEL_PATH) if MODEL_PATH.exists() else str(ALT_MODEL))
    prompt = Path(PROMPT_PATH).read_text(encoding="utf-8")
    tok, model = load_local(model_dir)
    infer_shard(shard_ids, gold_map, tok, model, prompt, raw_path)
    print(json.dumps({"status": "shard_done", "shard": args.shard, "n": len(shard_ids)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
