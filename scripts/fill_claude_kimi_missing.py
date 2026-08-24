#!/usr/bin/env python3
"""Fill missing Gold-v2 IDs in Claude / Kimi dumps. Does not overwrite originals."""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))

from expand_goldstyle_train import (  # noqa: E402
    SYSTEM,
    apply_text_spans,
    chat,
    chat_local,
    load_key,
    load_keys,
    load_local,
    parse_json_array,
)
from score_lskt import load_records, rec_id, score  # noqa: E402

GOLD = PAPER / "data/gold_canonical_v2.jsonl"
OUT_DIR = PAPER / "output/llm_fill_missing"
DUMPS = {
    "Claude": ROOT / "chinese_skillspan_preprocessing/output/dir/test_claude/merged_test_cluade.jsonl",
    "Kimi": ROOT / "chinese_skillspan_preprocessing/output/dir/test-kimi/merged_test_kimi.jsonl",
}


def tokens_of(rec: dict) -> list[str]:
    toks = rec.get("tokens")
    if isinstance(toks, list) and toks:
        return [str(t) for t in toks]
    return list(rec.get("sentence") or "")


def slim_score(report: dict) -> dict:
    keep = (
        "scorer_version",
        "alignment_ok",
        "eligible_for_main_table",
        "error",
        "n_missing",
        "n_matched",
        "typed_exact",
        "collapsed_exact",
        "typed_relaxed",
        "collapsed_relaxed",
        "gold_sha256",
        "pred_sha256",
    )
    return {k: report.get(k) for k in keep}


def main() -> int:
    backend = os.environ.get("GOLDSTYLE_BACKEND", "api")
    model = os.environ.get("GOLDSTYLE_MODEL", "gpt-4o")
    api_base = os.environ.get(
        "GOLDSTYLE_API_BASE", os.environ.get("api_base", "https://api.claude-Plus.top/v1")
    )
    gold = load_records(str(GOLD))
    g_by = {rec_id(r): r for r in gold}
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    tok = loc = None
    keys: list[str] = []
    if backend == "local":
        tok, loc = load_local(
            os.environ.get("GOLDSTYLE_LOCAL_MODEL", str(ROOT / "LLaMA-Factory/Qwen2.5-14B-Instruct"))
        )
    else:
        if not load_key():
            print(json.dumps({"error": "no API key; set GOLDSTYLE_API_KEY or api_key.py"}), flush=True)
            return 2
        keys = load_keys()

    summary: dict = {}
    for name, src_path in DUMPS.items():
        src = load_records(str(src_path))
        have = {rec_id(r) for r in src}
        missing = [iid for iid in g_by if iid not in have]
        raw_path = OUT_DIR / f"{name}_fill_raw.jsonl"
        done: dict[str, dict] = {}
        if raw_path.is_file():
            for line in raw_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rec = json.loads(line)
                    done[str(rec["id"])] = rec
        pending = [i for i in missing if i not in done]
        print(
            json.dumps({"model": name, "missing": len(missing), "pending": len(pending)}, ensure_ascii=False),
            flush=True,
        )
        batch = int(os.environ.get("GOLDSTYLE_BATCH", "6"))
        sleep = float(os.environ.get("GOLDSTYLE_SLEEP", "0.5"))
        with raw_path.open("a", encoding="utf-8") as fout:
            for i in range(0, len(pending), batch):
                chunk = pending[i : i + batch]
                lines = [
                    f"{j+1}. id=`{cid}`  {(g_by[cid].get('sentence') or '')[:800]}"
                    for j, cid in enumerate(chunk)
                ]
                user = "只输出 JSON 数组。\n\n句子：\n" + "\n".join(lines)
                messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
                err = None
                parsed: list = []
                for attempt in range(4):
                    try:
                        if backend == "local":
                            text = chat_local(messages, tok, loc)
                        else:
                            text = chat(messages, model, api_base, keys[attempt % len(keys)])
                        parsed = parse_json_array(text)
                        err = None
                        break
                    except Exception as e:
                        err = e
                        time.sleep(1 + attempt)
                if err is not None:
                    print(json.dumps({"error": str(err), "chunk0": chunk[0]}), flush=True)
                    continue
                by_ret = {str(x.get("id")): x for x in parsed if isinstance(x, dict)}
                for cid in chunk:
                    rec = g_by[cid]
                    item = by_ret.get(cid) or {"id": cid, "spans": []}
                    tags, miss = apply_text_spans(rec, item.get("spans") or [])
                    row = {
                        "id": cid,
                        "sentence": rec.get("sentence"),
                        "tokens": tokens_of(rec),
                        "pred_tags": tags,
                        "list_of_selection_bio4": tags,
                        "goldstyle_spans": item.get("spans") or [],
                        "_fill": {"source": name, "unaligned": miss, "backend": backend},
                    }
                    fout.write(json.dumps(row, ensure_ascii=False) + "\n")
                    done[cid] = row
                fout.flush()
                print(
                    json.dumps(
                        {"model": name, "wrote": min(i + batch, len(pending)), "of": len(pending)},
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                time.sleep(sleep)

        filled = list(src)
        for iid in missing:
            if iid in done:
                filled.append(done[iid])
        seen: set[str] = set()
        uniq = []
        for rec in filled:
            i = rec_id(rec)
            if i in seen:
                continue
            seen.add(i)
            uniq.append(rec)
        view_out = PAPER / "reports/views" / f"{name}_filled_v2.jsonl"
        view_out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in uniq), encoding="utf-8")
        report = score(str(GOLD), str(view_out), align_mode="official", n_boot=0)
        slim = slim_score(report)
        (PAPER / "reports" / f"score_v2_unique_{name}_filled.json").write_text(
            json.dumps(slim, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        row = {
            "model": name,
            "missing_before": len(missing),
            "filled": len([i for i in missing if i in done]),
            "alignment_ok": report.get("alignment_ok"),
            "typed_exact_f1": (report.get("typed_exact") or {}).get("f1"),
            "collapsed_exact_f1": (report.get("collapsed_exact") or {}).get("f1"),
            "typed_relaxed_f1": (report.get("typed_relaxed") or {}).get("f1"),
            "view": str(view_out),
        }
        (OUT_DIR / f"{name}_fill_summary.json").write_text(
            json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        summary[name] = row
    (OUT_DIR / "fill_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
