#!/usr/bin/env python3
"""SOP-v4 extract baseline: local Qwen2.5-14B-Instruct on all 2601 P2 IDs.

Does not overwrite Qwen_unique_first_v2.jsonl, Gold v2, or the paper.
Run: CUDA_VISIBLE_DEVICES=2 python -u scripts/run_qwen25_sopv4_p2_2601.py
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from expand_goldstyle_train import apply_text_spans, load_local  # noqa: E402
from score_lskt import SCORER_VERSION, rec_id, score  # noqa: E402

RUN = "qwen25_14b_instruct_sopv4_p2_2601"
MODEL_PATH = ROOT / "LLaMA-Factory/Qwen2.5-14B-Instruct"
ALT_MODEL = ROOT / "Qwen2.5-14B-Instruct"
PROMPT_PATH = PAPER / "reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100/PROMPT_gpt4o_sop_extract.txt"
SMOKE_IDS = PAPER / "reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100/sample_ids.txt"
P2 = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
P980 = PAPER / "data/test_lskt_v4_simhuman980_cws.jsonl"
P1 = PAPER / "data/gold_canonical_v2.jsonl"
USERDICT = PAPER / "data/cws_userdict.txt"
PRED_DIR = PAPER / "predictions"
REPORT_DIR = PAPER / "reports"
RAW_PATH = PRED_DIR / f"{RUN}.raw.jsonl"
PARSED_PATH = PRED_DIR / f"{RUN}.parsed.jsonl"
JIEBA_PATH = PRED_DIR / f"{RUN}.jieba.jsonl"
INPUT_PATH = PRED_DIR / f"{RUN}.input.jsonl"
FAIL_CSV = REPORT_DIR / f"{RUN}_failures.csv"
FREEZE = REPORT_DIR / f"{RUN}_freeze.json"
SMOKE_REP = REPORT_DIR / f"{RUN}_smoke_format.json"
ADAPTER_PATH: str | None = None
TYPES = {"L", "K", "S", "T"}
PARSER_VERSION = "sop_extract_json_array_v1"


def apply_run_name(name: str) -> None:
    global RUN, RAW_PATH, PARSED_PATH, JIEBA_PATH, INPUT_PATH, FAIL_CSV, FREEZE, SMOKE_REP
    RUN = name
    RAW_PATH = PRED_DIR / f"{RUN}.raw.jsonl"
    PARSED_PATH = PRED_DIR / f"{RUN}.parsed.jsonl"
    JIEBA_PATH = PRED_DIR / f"{RUN}.jieba.jsonl"
    INPUT_PATH = PRED_DIR / f"{RUN}.input.jsonl"
    FAIL_CSV = REPORT_DIR / f"{RUN}_failures.csv"
    FREEZE = REPORT_DIR / f"{RUN}_freeze.json"
    SMOKE_REP = REPORT_DIR / f"{RUN}_smoke_format.json"


USER_PREFIX = (
    "请从下面这一批句子抽出 LSKT 跨度。只输出 JSON 数组，不要 markdown。"
    "id 必须与输入完全一致、顺序一致、不增不删。"
    "text 必须是 sentence 的连续原文子串。不要参考银标或 Gold。\n"
)
GEN = {
    "do_sample": False,
    "max_new_tokens": 2048,
    "torch_dtype": "bfloat16",
    "quantization": "none",
    "device_map": "auto",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def extract_json_array(raw: str) -> list:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\[.*\]", text, re.S)
        if not m:
            raise
        blob = m.group(0)
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            blob2 = re.sub(
                r'("comment"\s*:\s*")(.*?)("\s*})',
                lambda mm: mm.group(1) + mm.group(2).replace('"', "「") + mm.group(3),
                blob,
                flags=re.S,
            )
            data = json.loads(blob2)
    if isinstance(data, dict):
        for k in ("results", "items", "data", "annotations"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
        else:
            if "id" in data:
                data = [data]
            else:
                raise ValueError("json_object_without_array")
    if not isinstance(data, list):
        raise ValueError("not_a_list")
    return data


def parse_results(raw: str, expected_ids: list[str]) -> list[dict]:
    data = extract_json_array(raw)
    rows = []
    for item in data:
        if not isinstance(item, dict):
            continue
        spans = []
        for sp in item.get("spans") or []:
            if not isinstance(sp, dict):
                continue
            typ = str(sp.get("type") or "").strip().upper()[:1]
            txt = str(sp.get("text") or "").strip()
            if txt and typ in TYPES:
                spans.append({"text": txt, "type": typ})
        rows.append({"id": str(item.get("id") or "").strip(), "spans": spans, "comment": str(item.get("comment") or "")})
    if len(rows) == len(expected_ids):
        for rec, cid in zip(rows, expected_ids):
            rec["id"] = cid
        return rows
    by_id = {r["id"]: r for r in rows if r["id"]}
    return [by_id.get(cid) or {"id": cid, "spans": [], "comment": "missing_in_model_output"} for cid in expected_ids]


def tokens_of(rec: dict) -> list[str]:
    toks = rec.get("tokens")
    if isinstance(toks, list) and toks:
        return [str(t) for t in toks]
    return list(rec.get("sentence") or "")


def spans_recoverable(sentence: str, spans: list[dict]) -> tuple[bool, list[str]]:
    bad = []
    for sp in spans:
        t = sp.get("text") or ""
        if t and t not in sentence:
            bad.append(t)
    return (not bad), bad


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


def chat_one(tok, model, prompt: str, payload: list[dict], max_new: int) -> str:
    import torch

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": USER_PREFIX + json.dumps(payload, ensure_ascii=False)},
    ]
    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok(text, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=max_new, do_sample=False)
    gen = out[0, inputs["input_ids"].shape[1] :]
    return tok.decode(gen, skip_special_tokens=True)


def write_input(p2_rows: list[dict]) -> None:
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    with INPUT_PATH.open("w", encoding="utf-8") as f:
        for rec in p2_rows:
            row = {"id": rec_id(rec), "sentence": rec.get("sentence") or ""}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def freeze_now(p2_rows: list[dict]) -> dict:
    write_input(p2_rows)
    tok_json = MODEL_PATH / "tokenizer.json"
    freeze = {
        "run": RUN,
        "model_path": str(MODEL_PATH),
        "alt_model_path_same_weights": str(ALT_MODEL),
        "hf_repo": "Qwen/Qwen2.5-14B-Instruct",
        "torch_dtype": "bfloat16",
        "quantization": "none",
        "lora": ADAPTER_PATH or "none (base Instruct, not sft_CN_skillspan_*)",
        "tokenizer_json_sha256": sha256_file(tok_json) if tok_json.is_file() else None,
        "safetensors_index_sha256": sha256_file(MODEL_PATH / "model.safetensors.index.json"),
        "prompt_path": str(PROMPT_PATH),
        "prompt_sha256": sha256_file(PROMPT_PATH),
        "input_path": str(INPUT_PATH),
        "input_sha256": sha256_file(INPUT_PATH),
        "p2_sha256": sha256_file(P2),
        "p1_sha256": sha256_file(P1),
        "p980_sha256": sha256_file(P980),
        "p980_note": "SimHuman SOP-v4 overlay, not human-validated Gold",
        "scorer_version": SCORER_VERSION,
        "parser_version": PARSER_VERSION,
        "jieba_userdict_sha256": sha256_file(USERDICT),
        "cws_snap_sha256": sha256_file(PAPER / "scripts/cws_snap.py"),
        "generation": GEN,
        "git_head": "70bec064097edd29007c32ecbf8a64d8a57a8ca7",
        "input_fields": ["id", "sentence"],
        "gold_not_in_prompt": True,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FREEZE.write_text(json.dumps(freeze, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return freeze


def infer_ids(ids: list[str], gold_map: dict, tok, model, prompt: str, fail_rows: list) -> None:
    done = load_done(RAW_PATH)
    pending = [i for i in ids if i not in done]
    print(json.dumps({"done": len(done), "pending": len(pending)}, ensure_ascii=False), flush=True)
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RAW_PATH.open("a", encoding="utf-8") as fout:
        for n, cid in enumerate(pending, 1):
            rec = gold_map[cid]
            sent = rec.get("sentence") or ""
            payload = [{"id": cid, "sentence": sent}]
            err = None
            text = ""
            parsed = None
            t0 = time.time()
            for max_new in (GEN["max_new_tokens"], 4096):
                for attempt in range(3):
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
            row = {
                "id": cid,
                "sentence": sent,
                "raw": text,
                "parsed": parsed[0] if parsed else {"id": cid, "spans": [], "comment": "parse_fail"},
                "error": err,
                "elapsed_s": round(time.time() - t0, 3),
                "model": RUN,
            }
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            fout.flush()
            if err:
                fail_rows.append({"id": cid, "stage": "parse", "reason": err})
            if n % 10 == 0 or n == len(pending):
                print(json.dumps({"wrote": n, "of": len(pending), "id": cid, "err": bool(err)}), flush=True)


def materialize(gold_map: dict[str, dict], ids: list[str]) -> tuple[list[dict], list[dict], list[dict]]:
    raw_by = load_done(RAW_PATH)
    parsed_rows = []
    jieba_rows = []
    fails = []
    for cid in ids:
        rec = gold_map[cid]
        sent = rec.get("sentence") or ""
        raw = raw_by.get(cid) or {}
        parsed = (raw.get("parsed") or {"id": cid, "spans": [], "comment": "missing_raw"})
        spans = parsed.get("spans") or []
        tags, miss = apply_text_spans({"tokens": tokens_of(rec), "sentence": sent}, spans)
        prow = {
            "id": cid,
            "sentence": sent,
            "tokens": tokens_of(rec),
            "pred_tags": tags,
            "list_of_selection_bio4": tags,
            "list_of_selection": tags,
            "model": RUN,
            "unaligned": miss,
            "comment": parsed.get("comment") or "",
        }
        parsed_rows.append(prow)
        jieba_rows.append(cws.rewrite_record(prow, tag_field="pred_tags"))
        if raw.get("error"):
            fails.append({"id": cid, "stage": "parse", "reason": raw["error"]})
        if miss:
            fails.append({"id": cid, "stage": "align_span", "reason": ";".join(miss)[:500]})
    return parsed_rows, jieba_rows, fails


def coverage_gate(ids: list[str], jieba_rows: list[dict], gold_map: dict) -> dict:
    got = [rec_id(r) for r in jieba_rows]
    sgot, sids = set(got), set(ids)
    bad_label = 0
    bad_span = 0
    for rec, cid in zip(jieba_rows, ids):
        sent = gold_map[cid].get("sentence") or ""
        for a, b, t in rec.get("cws_spans") or []:
            if str(t) not in TYPES:
                bad_label += 1
            frag = sent[int(a) : int(b)]
            if frag and frag not in sent:
                bad_span += 1
    report = {
        "n_rows": len(jieba_rows),
        "n_unique": len(sgot),
        "n_missing": len(sids - sgot),
        "n_extra": len(sgot - sids),
        "n_duplicate": len(got) - len(sgot),
        "bad_label": bad_label,
        "bad_span_not_in_sentence": bad_span,
        "pass": (
            len(jieba_rows) == 2601
            and len(sgot) == 2601
            and not (sids - sgot)
            and not (sgot - sids)
            and len(got) == len(sgot)
            and bad_label == 0
        ),
    }
    return report


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def error_summary(gold_rows: list[dict], jieba_rows: list[dict]) -> dict:
    from collections import Counter

    gmap = {rec_id(r): r for r in gold_rows}
    counts = Counter()
    for rec in jieba_rows:
        cid = rec_id(rec)
        gold = gmap[cid]
        gspans = cws.spans_of(gold) if gold.get("cws_spans") is not None else cws.g.bio_spans(
            gold.get("list_of_selection_bio4") or []
        )
        pspans = rec.get("cws_spans") or []
        gset = {(int(a), int(b), str(t)) for a, b, t in gspans}
        pset = {(int(a), int(b), str(t)) for a, b, t in pspans}
        sent = gold.get("sentence") or ""
        if not gset and pset:
            counts["empty_sentence_false_positives"] += 1
        for a, b, t in pset:
            if (a, b, t) in gset:
                continue
            types_at = {tt for aa, bb, tt in gset if aa == a and bb == b}
            if types_at:
                counts["type_errors"] += 1
                continue
            overlap = False
            for aa, bb, tt in gset:
                if max(a, aa) < min(b, bb):
                    overlap = True
                    ia, ib = max(a, aa), min(b, bb)
                    ua, ub = min(a, aa), max(b, bb)
                    iou = (ib - ia) / max(1, ub - ua)
                    if iou >= 0.5 and t == tt:
                        counts["boundary_only_errors"] += 1
                    elif t != tt:
                        counts["type_errors"] += 1
                    else:
                        counts["boundary_only_errors"] += 1
                    break
            if not overlap:
                frag = sent[a:b]
                if cws.is_incomplete_text(frag):
                    counts["invalid_or_truncated_word_fragments"] += 1
                elif (b - a) > 8:
                    counts["overlong_spans"] += 1
                else:
                    counts["false_positives_other"] += 1
        for a, b, t in gset:
            if (a, b, t) in pset:
                continue
            if not any(max(a, aa) < min(b, bb) for aa, bb, tt in pset):
                counts["missed_entities"] += 1
    return dict(counts)


def score_all(jieba_rows: list[dict]) -> dict:
    cws.write_jsonl(JIEBA_PATH, jieba_rows)
    p2_score = score(str(P2), str(JIEBA_PATH), align_mode="official", n_boot=0)
    gold980 = {rec_id(r) for r in cws.load_jsonl(P980)}
    sub = [r for r in jieba_rows if rec_id(r) in gold980]
    p980_path = PRED_DIR / f"{RUN}.jieba_980.jsonl"
    cws.write_jsonl(p980_path, sub)
    s980 = score(str(P980), str(p980_path), align_mode="official", n_boot=0)
    s1 = score(str(P1), str(JIEBA_PATH), align_mode="official", n_boot=0)

    def row(split, n, r, note):
        te, tr = r["typed_exact"], r["typed_relaxed"]
        return {
            "run": RUN,
            "split": split,
            "n": n,
            "alignment_ok": bool(r.get("alignment_ok")),
            "n_missing": r.get("n_missing"),
            "typed_exact_p": te["precision"],
            "typed_exact_r": te["recall"],
            "typed_exact_f1": te["f1"],
            "collapsed_exact_f1": r["collapsed_exact"]["f1"],
            "typed_relaxed_f1": tr["f1"],
            "note": note,
        }

    r2601 = row("P2_hybrid_2601", 2601, p2_score, "main P2 result; not comparable to ChatGPT 0.6365 on Gold v2")
    r980 = row("P2_simhuman980", 980, s980, "SimHuman SOP overlay, not human-validated Gold")
    r1 = row("P1_gold_v2_diagnostic", 2601, s1, "span-convention diagnostic only")
    write_csv(REPORT_DIR / f"{RUN}_scores.csv", [r2601])
    write_csv(REPORT_DIR / f"{RUN}_980_scores.csv", [r980])
    write_csv(REPORT_DIR / "qwen25_14b_instruct_sopv4_on_gold_v2_diagnostic.csv", [r1])
    return {"p2_2601": r2601, "p2_980": r980, "p1_diag": r1}


def smoke_format(ids: list[str], gold_map: dict) -> dict:
    raw = load_done(RAW_PATH)
    missing = [i for i in ids if i not in raw]
    dups = []
    seen = set()
    labels_ok = True
    substr_ok = True
    json_ok = True
    for cid in ids:
        rec = raw.get(cid)
        if not rec:
            json_ok = False
            continue
        if cid in seen:
            dups.append(cid)
        seen.add(cid)
        parsed = rec.get("parsed") or {}
        sent = gold_map[cid].get("sentence") or ""
        for sp in parsed.get("spans") or []:
            if sp.get("type") not in TYPES:
                labels_ok = False
            if sp.get("text") and sp["text"] not in sent:
                substr_ok = False
        if rec.get("error"):
            json_ok = False
    return {
        "n": len(ids),
        "n_present": len(ids) - len(missing),
        "missing": missing[:20],
        "n_missing": len(missing),
        "duplicates": dups,
        "json_ok": json_ok and not missing,
        "labels_lkst_only": labels_ok,
        "spans_substrings": substr_ok,
        "resume_ok": RAW_PATH.is_file(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-only", action="store_true")
    ap.add_argument("--score-only", action="store_true")
    ap.add_argument("--skip-smoke-continue", action="store_true", help="skip 100-id smoke and run 2601")
    ap.add_argument("--adapter", default=None, help="optional PEFT adapter dir; writes a separate RUN")
    ap.add_argument("--run-name", default=None, help="override RUN so LoRA preds do not overwrite Instruct")
    args = ap.parse_args()
    global ADAPTER_PATH
    if args.run_name:
        apply_run_name(args.run_name)
    if args.adapter:
        ADAPTER_PATH = args.adapter

    p2_rows = cws.load_jsonl(P2)
    gold_map = {rec_id(r): r for r in p2_rows}
    ids = [rec_id(r) for r in p2_rows]
    if len(ids) != 2601 or len(set(ids)) != 2601:
        raise SystemExit(f"P2 ID set invalid: n={len(ids)} unique={len(set(ids))}")
    p1_ids = {rec_id(r) for r in cws.load_jsonl(P1)}
    if set(ids) != p1_ids:
        raise SystemExit("P2 IDs are not identical to Gold v2 IDs")

    freeze = freeze_now(p2_rows)
    print(json.dumps({"freeze": str(FREEZE), "input_sha256": freeze["input_sha256"]}, ensure_ascii=False), flush=True)

    smoke_ids = [ln.strip() for ln in SMOKE_IDS.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(smoke_ids) != 100:
        raise SystemExit(f"expected 100 smoke ids, got {len(smoke_ids)}")
    if any(i not in gold_map for i in smoke_ids):
        raise SystemExit("smoke id not in P2")

    fail_rows: list[dict] = []
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    tok = model = None
    if not args.score_only:
        print(json.dumps({"load_model": str(MODEL_PATH), "adapter": ADAPTER_PATH}, ensure_ascii=False), flush=True)
        tok, model = load_local(str(MODEL_PATH))
        if ADAPTER_PATH:
            from peft import PeftModel

            model = PeftModel.from_pretrained(model, ADAPTER_PATH)
            model.eval()
        if not args.skip_smoke_continue:
            infer_ids(smoke_ids, gold_map, tok, model, prompt, fail_rows)
            smoke = smoke_format(smoke_ids, gold_map)
            SMOKE_REP.write_text(json.dumps(smoke, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(json.dumps({"smoke_format": smoke}, ensure_ascii=False), flush=True)
            if not smoke["json_ok"] or not smoke["labels_lkst_only"]:
                print(json.dumps({"warn": "smoke format issues; continuing to 2601 per protocol"}, ensure_ascii=False), flush=True)
            if args.smoke_only:
                return 0
        infer_ids(ids, gold_map, tok, model, prompt, fail_rows)

    parsed_rows, jieba_rows, fails2 = materialize(gold_map, ids)
    fail_rows.extend(fails2)
    cws.write_jsonl(PARSED_PATH, parsed_rows)
    cws.write_jsonl(JIEBA_PATH, jieba_rows)
    write_csv(FAIL_CSV, fail_rows or [{"id": "", "stage": "none", "reason": "no_failures"}])
    cov = coverage_gate(ids, jieba_rows, gold_map)
    (REPORT_DIR / f"{RUN}_coverage.json").write_text(json.dumps(cov, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"coverage": cov}, ensure_ascii=False), flush=True)
    if not cov["pass"]:
        print(json.dumps({"abort_score": "coverage gate failed"}, ensure_ascii=False), flush=True)
        return 2
    scores = score_all(jieba_rows)
    err = error_summary(p2_rows, jieba_rows)
    err["parser_failures"] = sum(1 for r in fail_rows if r.get("stage") == "parse")
    md = REPORT_DIR / f"{RUN}_error_summary.md"
    lines = ["# Qwen2.5-14B-Instruct SOP-v4 P2 error summary", "", f"Run `{RUN}`.", "", "| Kind | Count |", "|---|---:|"]
    for k, v in sorted(err.items()):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "P2-980 is SimHuman SOP overlay, **not** human-validated Gold.",
        "Do not compare P2 F1 with ChatGPT 0.6365 on Gold v2.",
        "confirmed-results.md not updated in this run.",
    ]
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    man = {
        "run": RUN,
        "files": {
            str(p): sha256_file(p)
            for p in (INPUT_PATH, RAW_PATH, PARSED_PATH, JIEBA_PATH, FREEZE, JIEBA_PATH)
            if p.is_file()
        },
        "coverage": cov,
        "scores": scores,
        "errors": err,
    }
    (REPORT_DIR / f"{RUN}_manifest.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"scores": scores, "manifest": str(REPORT_DIR / f"{RUN}_manifest.json")}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
