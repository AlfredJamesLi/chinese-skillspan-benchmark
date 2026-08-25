#!/usr/bin/env python3
"""SOP-v4 extract on all 2601 P2 IDs via ysaikeji proxy (resume-safe).

Same prompt as the gpt-5.4 n=100 pilot: id+sentence, no silver, no Gold.

gpt-5.4: seed from the existing 100 records, then the remaining 2501.
claude-sonnet-4-6: start from 0. The human980 sonnet46_round1 job was
silver-correction (silver in the prompt) and MUST NOT be reused here.

Does not overwrite Gold v2, frozen LLM dumps, or confirmed-results.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
import sys

sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
import pilot_gpt4o_sop_extract100 as p  # noqa: E402
from score_lskt import SCORER_VERSION, rec_id, score  # noqa: E402

PROMPT_PATH = PAPER / "reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100/PROMPT_gpt4o_sop_extract.txt"
PILOT_GPT = PAPER / "reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100/records_gpt-5.4.jsonl"
P2 = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
P1 = PAPER / "data/gold_canonical_v2.jsonl"
P980 = PAPER / "data/test_lskt_v4_simhuman980_cws.jsonl"
USERDICT = PAPER / "data/cws_userdict.txt"
ROOT_OUT = PAPER / "reports/sandbox_lskt_v4_silver/sop_extract_p2_2601"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def slim(gold_path: Path, pred_path: Path) -> dict:
    r = score(str(gold_path), str(pred_path), align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    return {
        "alignment_ok": bool(r.get("alignment_ok")),
        "n_gold": r.get("gold_n_unique_ids"),
        "n_matched": r.get("n_matched"),
        "n_missing": r.get("n_missing"),
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "typed_exact_f1": te["f1"],
        "typed_relaxed_f1": tr["f1"],
        "collapsed_exact_f1": r["collapsed_exact"]["f1"],
        "collapsed_relaxed_f1": r["collapsed_relaxed"]["f1"],
    }


def load_done(path: Path) -> dict[str, dict]:
    done: dict[str, dict] = {}
    if not path.is_file():
        return done
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        done[str(rec["id"])] = rec
    return done


def seed_records(dst: Path, src: Path, allowed: set[str]) -> int:
    if dst.is_file() or not src.is_file():
        return 0
    n = 0
    with dst.open("w", encoding="utf-8") as out:
        for line in src.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            if str(rec.get("id") or "") not in allowed:
                continue
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    return n


def freeze_now(out: Path, model: str, slug: str) -> dict:
    freeze = {
        "run": f"sopv4_api_p2_2601_{slug}",
        "model": model,
        "base": p.BASE,
        "prompt_path": str(PROMPT_PATH),
        "prompt_sha256": sha256_file(PROMPT_PATH),
        "p2_sha256": sha256_file(P2),
        "p1_sha256": sha256_file(P1),
        "p980_sha256": sha256_file(P980),
        "p980_note": "SimHuman SOP-v4 overlay, not human-validated Gold",
        "scorer_version": SCORER_VERSION,
        "jieba_userdict_sha256": sha256_file(USERDICT),
        "cws_snap_sha256": sha256_file(PAPER / "scripts/cws_snap.py"),
        "input_fields": ["id", "sentence", "domain"],
        "gold_not_in_prompt": True,
        "silver_not_in_prompt": True,
        "not_sonnet46_human980_silver_correct": True,
        "not_for_confirmed_results_until_coverage": True,
        "do_not_overwrite_frozen_dumps": True,
        "thinking": p.EXTRA_BODY.get("thinking") if p.EXTRA_BODY else None,
        "not_codex_kimi_g2ids_silver_pack": True,
    }
    path = out / "freeze.json"
    path.write_text(json.dumps(freeze, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return freeze


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--base", default="https://claudeed.ysaikeji.cn")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--min-interval", type=float, default=0.4)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--no-temperature", action="store_true")
    ap.add_argument("--chat-path", default="/v1/chat/completions")
    ap.add_argument("--key-path", default="", help="API key file; default is ysaikeji via the pilot loader")
    ap.add_argument("--api-key-env", default="", help="Only this env var is checked before --key-path")
    ap.add_argument("--thinking-disabled", action="store_true", help="Moonshot kimi-k2.6: thinking.type=disabled")
    ap.add_argument("--thinking", action="store_true", help="DeepSeek: thinking.type=enabled")
    ap.add_argument("--reasoning-effort", default="", help="DeepSeek: high|medium|low")
    ap.add_argument("--seed-records", default="", help="Existing SOP-extract records to resume from")
    ap.add_argument("--score-only", action="store_true")
    args = ap.parse_args()

    p.BASE = args.base.rstrip("/")
    p.CHAT_PATH = args.chat_path
    p.CHAT_TIMEOUT = args.timeout
    p.USE_TEMPERATURE = not args.no_temperature
    p.REQUEST_PACE = p.RequestPace(args.min_interval) if args.min_interval > 0 else None
    extra: dict = {}
    if args.thinking_disabled:
        extra["thinking"] = {"type": "disabled"}
    if args.thinking:
        extra["thinking"] = {"type": "enabled"}
        p.USE_TEMPERATURE = False
    if args.reasoning_effort:
        extra["reasoning_effort"] = args.reasoning_effort
        p.USE_TEMPERATURE = False
    p.EXTRA_BODY = extra or None
    if args.api_key_env:
        p.KEY_ENV = args.api_key_env
    if args.key_path:
        p.KEY_PATH = Path(args.key_path)
        if not args.api_key_env:
            p.KEY_ENV = "MOONSHOT_API_KEY"

    model = args.model.strip()
    slug = p.model_slug(model)
    out = ROOT_OUT / slug
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROMPT_PATH, out / "PROMPT_gpt4o_sop_extract.txt")

    hybrid = cws.load_jsonl(P2)
    gold_map = {rec_id(r): r for r in hybrid}
    ids = [rec_id(r) for r in hybrid]
    if len(ids) != 2601 or len(set(ids)) != 2601:
        raise SystemExit(f"P2 ID set invalid: n={len(ids)} unique={len(set(ids))}")
    p1_ids = {rec_id(r) for r in cws.load_jsonl(P1)}
    if set(ids) != p1_ids:
        raise SystemExit("P2 IDs are not identical to Gold v2 IDs")

    freeze = freeze_now(out, model, slug)
    print(json.dumps({"out": str(out), "model": model, "base": p.BASE, "freeze": freeze["prompt_sha256"][:12]}, ensure_ascii=False), flush=True)

    done_path = out / f"records_{slug}.jsonl"
    seed_src = Path(args.seed_records) if args.seed_records else None
    if seed_src and seed_src.is_file() and not done_path.is_file():
        n_seed = seed_records(done_path, seed_src, set(ids))
        print(json.dumps({"seeded": n_seed, "from": str(seed_src)}, ensure_ascii=False), flush=True)

    done = load_done(done_path)
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    n_sim = sum(1 for r in hybrid if r.get("hybrid_source") == "simhuman980_cws")

    if not args.score_only:
        key = p.load_key()
        pending = [gold_map[i] for i in ids if i not in done]
        workers = max(1, int(args.workers))
        print(
            json.dumps(
                {
                    "n": 2601,
                    "n_simhuman": n_sim,
                    "done": len(done),
                    "pending": len(pending),
                    "batch": args.batch,
                    "workers": workers,
                    "prompt": "SOP extract v4 (no silver)",
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        raw_dir = out / f"raw_{slug}"
        raw_dir.mkdir(exist_ok=True)
        write_lock = Lock()
        stop = {"err": None}

        def run_batch(b: int, chunk: list[dict]):
            cids = [rec_id(c) for c in chunk]
            send = [
                {
                    "id": rec_id(c),
                    "sentence": c.get("sentence") or "",
                    "domain": c.get("source_domain") or c.get("hybrid_source") or "",
                }
                for c in chunk
            ]
            parsed = None
            last_err = None
            raw_text = ""
            for attempt in range(8):
                code, raw_text, err, _meta = p.chat(
                    key, prompt, send, model, max_tokens=8192 if (p.EXTRA_BODY and p.EXTRA_BODY.get("thinking")) else 4096
                )
                if code == 429 or (err and "429" in str(err)):
                    last_err = err or f"http_{code}"
                    time.sleep(min(40, 2 ** attempt))
                    continue
                if code != 200 or not (raw_text or "").strip():
                    last_err = err or f"http_{code}"
                    time.sleep(2 + attempt)
                    continue
                try:
                    parsed = p.parse_results(raw_text, cids)
                    if any(r.get("comment") == "missing_in_model_output" for r in parsed):
                        raise ValueError("missing_ids")
                    last_err = None
                    break
                except Exception as e:
                    last_err = f"{type(e).__name__}: {e}"
                    time.sleep(2 + attempt)
            return b, cids, parsed, raw_text, last_err

        def commit(b: int, chunk: list[dict], cids: list[str], parsed: list[dict], raw_text: str) -> None:
            by_id = {r["id"]: r for r in parsed}
            with done_path.open("a", encoding="utf-8") as fout:
                for gold in chunk:
                    cid = rec_id(gold)
                    item = by_id[cid]
                    row, _miss = p.pred_row(gold, item.get("spans") or [], {"comment": item.get("comment") or ""}, model)
                    done[cid] = row
                    fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(
                json.dumps(
                    {
                        "wrote": len(done),
                        "of": 2601,
                        "batch": b,
                        "unaligned": sum(len(done[i].get("unaligned") or []) for i in cids),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

        batches = [(b, pending[b : b + args.batch]) for b in range(0, len(pending), args.batch)]
        if workers == 1:
            for b, chunk in batches:
                _b, cids, parsed, raw_text, last_err = run_batch(b, chunk)
                (raw_dir / f"batch_{b:04d}.txt").write_text(raw_text or (last_err or ""), encoding="utf-8")
                if parsed is None:
                    print(json.dumps({"batch_start": b, "error": last_err, "ids": cids}, ensure_ascii=False), flush=True)
                    return 2
                commit(b, chunk, cids, parsed, raw_text)
        else:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futs = {pool.submit(run_batch, b, chunk): (b, chunk) for b, chunk in batches}
                for fut in as_completed(futs):
                    b, chunk = futs[fut]
                    _b, cids, parsed, raw_text, last_err = fut.result()
                    with write_lock:
                        (raw_dir / f"batch_{b:04d}.txt").write_text(raw_text or (last_err or ""), encoding="utf-8")
                        if parsed is None:
                            stop["err"] = {"batch_start": b, "error": last_err, "ids": cids}
                            print(json.dumps(stop["err"], ensure_ascii=False), flush=True)
                            continue
                        commit(b, chunk, cids, parsed, raw_text)
            if stop["err"]:
                missing = [i for i in ids if i not in done]
                print(json.dumps({"incomplete": True, "missing_n": len(missing)}, ensure_ascii=False), flush=True)
                return 2

    missing = [i for i in ids if i not in done]
    if missing:
        print(json.dumps({"incomplete": True, "missing_n": len(missing), "missing_head": missing[:10]}, ensure_ascii=False))
        return 1

    ordered = [done[i] for i in ids]
    pred_raw = out / f"pred_{slug}_sop_extract.jsonl"
    write_jsonl(pred_raw, ordered)
    pred_cws = [cws.rewrite_record(r, tag_field="pred_tags") for r in ordered]
    pred_cws_path = out / f"pred_{slug}_sop_extract_cws.jsonl"
    write_jsonl(pred_cws_path, pred_cws)
    gold_path = out / "gold_p2_2601.jsonl"
    write_jsonl(gold_path, hybrid)

    ids980 = {rec_id(r) for r in cws.load_jsonl(P980)}
    gold980 = [r for r in hybrid if rec_id(r) in ids980]
    pred980 = [r for r in pred_cws if rec_id(r) in ids980]
    gold980_path = out / "gold_p2_980.jsonl"
    pred980_path = out / f"pred_{slug}_sop_extract_cws_980.jsonl"
    write_jsonl(gold980_path, gold980)
    write_jsonl(pred980_path, pred980)

    summary = {
        "n": 2601,
        "n_simhuman": n_sim,
        "n_sop_cws": 2601 - n_sim,
        "n_unaligned_sents": sum(1 for r in ordered if r.get("unaligned")),
        "n_spans": sum(len(r.get("spans") or []) for r in ordered),
        "n_empty": sum(1 for r in ordered if not (r.get("spans") or [])),
        "model": model,
        "base": p.BASE,
        "prompt": "SOP extract v4 (no silver); not frozen @@span## dump; not sonnet46 silver-correct",
        "gold_v2_untouched": True,
        "frozen_dumps_untouched": True,
        "not_for_confirmed_results": True,
        "hybrid_cws": {
            "p2_2601": slim(gold_path, pred_cws_path),
            "p2_980": slim(gold980_path, pred980_path),
        },
    }
    (out / f"summary_{slug}.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
