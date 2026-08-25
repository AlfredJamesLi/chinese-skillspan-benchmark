#!/usr/bin/env python3
"""Pilot: GPT-4 family on SOP extract prompt via ysaikeji proxy, n=100.

Does not overwrite Gold v2, the frozen ChatGPT dump, or train silver.
Repro: python scripts/pilot_gpt4o_sop_extract100.py --probe
       python scripts/pilot_gpt4o_sop_extract100.py --model gpt-4-0125-preview
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from expand_goldstyle_train import apply_text_spans  # noqa: E402
from score_lskt import rec_id, score  # noqa: E402

OUT = PAPER / "reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100"
PROMPT_PATH = OUT / "PROMPT_gpt4o_sop_extract.txt"
GOLD_HYBRID = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
GOLD_V2 = PAPER / "data/gold_canonical_v2.jsonl"
CHATGPT_OLD = PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl"
KEY_PATH = Path.home() / ".config/ysaikeji/api_key"
BASE = os.environ.get("YSAIKEJI_BASE", "https://claudeed.ysaikeji.cn").rstrip("/")
# gpt-5.4 lives on claudeed; older gpt-4 aliases were on claudeplus (Claude-only group).
CANDIDATE_MODELS = ["gpt-5.4", "gpt-4-0125-preview", "gpt-4-0613", "gpt-4"]
CTX = ssl.create_default_context()
CHAT_PATH = "/v1/chat/completions"
EXTRA_BODY: dict | None = None
USE_TEMPERATURE = True
CHAT_TIMEOUT = 180
KEY_ENV = ""
REQUEST_PACE: "RequestPace | None" = None
TYPES = {"L", "K", "S", "T"}


class RequestPace:
    """Serialize request *starts* so concurrent workers still honor a min interval."""

    def __init__(self, interval_s: float):
        self.interval = max(0.0, float(interval_s))
        self.lock = Lock()
        self.next_ok = 0.0

    def wait(self) -> None:
        if self.interval <= 0:
            return
        with self.lock:
            now = time.time()
            delay = self.next_ok - now
            self.next_ok = max(now, self.next_ok) + self.interval
        if delay > 0:
            time.sleep(delay)
USER_PREFIX = (
    "请从下面这一批句子抽出 LSKT 跨度。只输出 JSON 数组，不要 markdown。"
    "id 必须与输入完全一致、顺序一致、不增不删。"
    "text 必须是 sentence 的连续原文子串。不要参考银标或 Gold。\n"
)


def load_key(env_name: str = "") -> str:
    names = [env_name or KEY_ENV] if (env_name or KEY_ENV) else ("YSAIKEJI_API_KEY", "DEEPSEEK_API_KEY")
    for name in names:
        if not name:
            continue
        key = (os.environ.get(name) or "").strip()
        if key.startswith("sk-") and len(key) >= 20:
            return key
    if KEY_PATH.is_file():
        key = KEY_PATH.read_text(encoding="utf-8").strip()
        if key.startswith("sk-") and len(key) >= 20:
            return key
    raise SystemExit("missing YSAIKEJI_API_KEY / DEEPSEEK_API_KEY or ~/.config/ysaikeji/api_key")


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
        rows.append(
            {
                "id": str(item.get("id") or "").strip(),
                "spans": spans,
                "comment": str(item.get("comment") or ""),
            }
        )
    if len(rows) == len(expected_ids):
        for rec, cid in zip(rows, expected_ids):
            rec["id"] = cid
        return rows
    by_id = {r["id"]: r for r in rows if r["id"]}
    return [by_id.get(cid) or {"id": cid, "spans": [], "comment": "missing_in_model_output"} for cid in expected_ids]


def message_text(parsed: dict) -> str:
    msg = ((parsed.get("choices") or [{}])[0].get("message") or {})
    content = msg.get("content") or ""
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict):
                parts.append(str(p.get("text") or p.get("content") or ""))
            else:
                parts.append(str(p))
        content = "".join(parts)
    if not str(content).strip():
        content = msg.get("reasoning_content") or ""
    return str(content)


def chat(
    key: str,
    prompt: str,
    payload: list[dict],
    model: str,
    timeout: int | None = None,
    max_tokens: int = 8192,
    extra_body: dict | None = None,
    chat_path: str | None = None,
    use_temperature: bool | None = None,
) -> tuple[int | None, str, str | None, dict]:
    timeout = CHAT_TIMEOUT if timeout is None else timeout
    chat_path = CHAT_PATH if chat_path is None else chat_path
    use_temperature = USE_TEMPERATURE if use_temperature is None else use_temperature
    extra_body = EXTRA_BODY if extra_body is None else extra_body
    if REQUEST_PACE is not None:
        REQUEST_PACE.wait()
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": USER_PREFIX + json.dumps(payload, ensure_ascii=False)},
    ]
    meta = {"requested_model": model}
    if "deepseek.com" in BASE:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=key, base_url=BASE, timeout=timeout)
            kwargs = {
                "model": model,
                "messages": messages,
                "stream": False,
                "max_tokens": max_tokens,
            }
            extra = dict(extra_body or {})
            if extra.get("reasoning_effort"):
                kwargs["reasoning_effort"] = extra.pop("reasoning_effort")
            extra_sdk = {}
            if extra.get("thinking"):
                extra_sdk["thinking"] = extra.pop("thinking")
            extra_sdk.update(extra)
            if extra_sdk:
                kwargs["extra_body"] = extra_sdk
            if use_temperature:
                kwargs["temperature"] = 0
            resp = client.chat.completions.create(**kwargs)
            msg = resp.choices[0].message
            content = msg.content or ""
            if not str(content).strip():
                content = getattr(msg, "reasoning_content", None) or ""
            meta["upstream_model"] = resp.model
            meta["usage"] = resp.usage.model_dump() if getattr(resp, "usage", None) else None
            meta["via"] = "openai_sdk"
            return 200, str(content), None, meta
        except Exception as e:
            raw = ""
            status = getattr(e, "status_code", None)
            resp_obj = getattr(e, "response", None)
            if resp_obj is not None:
                status = status or getattr(resp_obj, "status_code", None)
                try:
                    raw = resp_obj.text[:1200]
                except Exception:
                    raw = str(e)[:1200]
            else:
                raw = f"{type(e).__name__}: {e}"
            if status is None and "RateLimit" in type(e).__name__:
                status = 429
            return status, "", raw, meta
    body = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": False,
    }
    if use_temperature:
        body["temperature"] = 0
    if extra_body:
        body.update(extra_body)
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE + chat_path, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    meta = {"requested_model": model}
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            parsed = json.loads(resp.read().decode("utf-8"))
            content = message_text(parsed)
            meta["upstream_model"] = parsed.get("model")
            meta["usage"] = parsed.get("usage")
            return resp.status, content, None, meta
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace") if e.fp else ""
        return e.code, "", raw[:1200], meta
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}", meta


def probe_models(key: str) -> dict:
    payload = [{"id": "probe-1", "sentence": "熟悉 Python 和英语六级，沟通能力强。", "domain": "it"}]
    prompt = "只输出 JSON 数组：[{\"id\":\"probe-1\",\"spans\":[{\"text\":\"Python\",\"type\":\"S\"}]}]"
    out = {}
    for model in CANDIDATE_MODELS:
        code, text, err, meta = chat(key, prompt, payload, model, timeout=60, max_tokens=64)
        rec = {
            "status": code,
            "ok": code == 200 and bool((text or "").strip()),
            "preview": (text or "")[:180],
            "err": err,
            **meta,
        }
        out[model] = rec
        print(json.dumps({"probe": rec}, ensure_ascii=False), flush=True)
        time.sleep(0.3)
    return out


def sample_ids(hybrid: list[dict], n: int, seed: str) -> list[str]:
    sim = [rec_id(r) for r in hybrid if r.get("hybrid_source") == "simhuman980_cws"]
    sop = [rec_id(r) for r in hybrid if r.get("hybrid_source") != "simhuman980_cws"]
    n_sim = min(len(sim), round(n * len(sim) / max(1, len(hybrid))))
    n_sop = n - n_sim

    def ranked(ids: list[str]) -> list[str]:
        return sorted(ids, key=lambda i: hashlib.sha256(f"{seed}:{i}".encode()).hexdigest())

    picked = ranked(sim)[:n_sim] + ranked(sop)[:n_sop]
    return sorted(picked, key=lambda i: hashlib.sha256(f"{seed}:order:{i}".encode()).hexdigest())


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


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def pred_row(gold: dict, spans: list[dict], extra: dict, model: str) -> tuple[dict, list]:
    sent = gold.get("sentence") or ""
    toks = [str(t) for t in (gold.get("tokens") or list(sent))]
    tags, miss = apply_text_spans({"tokens": toks, "sentence": sent}, spans)
    row = {
        "id": rec_id(gold),
        "sentence": sent,
        "tokens": toks,
        "pred_tags": tags,
        "list_of_selection_bio4": tags,
        "model": model,
        "spans": spans,
        "unaligned": miss,
        **extra,
    }
    return row, miss


def subset_old_chatgpt(ids: set[str], gold_map: dict[str, dict]) -> list[dict]:
    rows = []
    by_id = {}
    for rec in cws.load_jsonl(CHATGPT_OLD):
        try:
            by_id[rec_id(rec)] = rec
        except Exception:
            continue
    for cid in ids:
        g = gold_map[cid]
        src = by_id.get(cid)
        if src is None:
            toks = [str(t) for t in (g.get("tokens") or list(g.get("sentence") or ""))]
            tags = ["O"] * len(toks)
            rows.append({"id": cid, "sentence": g.get("sentence") or "", "tokens": toks, "pred_tags": tags, "list_of_selection_bio4": tags})
            continue
        toks = [str(t) for t in (g.get("tokens") or src.get("tokens") or list(g.get("sentence") or ""))]
        row = dict(src)
        row["id"] = cid
        row["tokens"] = toks
        row["sentence"] = g.get("sentence") or src.get("sentence") or ""
        rows.append(row)
    return rows


def model_slug(model: str) -> str:
    return model.replace("/", "_")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--workers", type=int, default=1, help="Parallel in-flight batches")
    ap.add_argument("--min-interval", type=float, default=0.0, help="Seconds between request starts (rate limit)")
    ap.add_argument("--seed", default="20260825")
    ap.add_argument("--model", default="", help="Model id, e.g. gpt-5.4 or deepseek-v4-pro")
    ap.add_argument("--base", default="", help="API origin, e.g. https://api.deepseek.com")
    ap.add_argument("--chat-path", default="/v1/chat/completions")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--reasoning-effort", default="")
    ap.add_argument("--thinking", action="store_true")
    ap.add_argument("--no-temperature", action="store_true")
    ap.add_argument("--api-key-env", default="", help="Env var for the API key, e.g. DEEPSEEK_API_KEY")
    ap.add_argument("--probe", action="store_true", help="Probe candidate models and exit")
    ap.add_argument("--smoke", action="store_true", help="Call API on 1 sentence and exit")
    ap.add_argument("--score_only", action="store_true")
    args = ap.parse_args()

    global BASE, CHAT_PATH, EXTRA_BODY, USE_TEMPERATURE, CHAT_TIMEOUT, KEY_ENV, REQUEST_PACE
    if args.base:
        BASE = args.base.rstrip("/")
    CHAT_PATH = args.chat_path
    CHAT_TIMEOUT = args.timeout
    USE_TEMPERATURE = not args.no_temperature
    if args.thinking:
        USE_TEMPERATURE = False
    KEY_ENV = args.api_key_env
    REQUEST_PACE = RequestPace(args.min_interval) if args.min_interval > 0 else None
    extra: dict = {}
    if args.reasoning_effort:
        extra["reasoning_effort"] = args.reasoning_effort
    if args.thinking:
        extra["thinking"] = {"type": "enabled"}
    EXTRA_BODY = extra or None

    OUT.mkdir(parents=True, exist_ok=True)
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    hybrid = cws.load_jsonl(GOLD_HYBRID)
    gold_map = {rec_id(r): r for r in hybrid}
    ids = sample_ids(hybrid, args.n, args.seed)
    gold_sub = [gold_map[i] for i in ids]
    gold_path = OUT / "gold_hybrid_sample100.jsonl"
    write_jsonl(gold_path, gold_sub)
    (OUT / "sample_ids.txt").write_text("\n".join(ids) + "\n", encoding="utf-8")
    n_sim = sum(1 for r in gold_sub if r.get("hybrid_source") == "simhuman980_cws")

    if args.probe:
        key = load_key()
        probes = probe_models(key)
        (OUT / "probe.json").write_text(json.dumps(probes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        working = [m for m, v in probes.items() if v.get("ok")]
        print(json.dumps({"working": working, "base": BASE}, ensure_ascii=False), flush=True)
        return 0 if working else 2

    model = (args.model or "").strip()
    if not model:
        raise SystemExit("pass --model gpt-4-0125-preview | gpt-4-0613 | gpt-4  (or --probe first)")
    slug = model_slug(model)
    print(
        json.dumps(
            {"n": len(ids), "n_simhuman": n_sim, "n_sop_cws": len(ids) - n_sim, "model": model, "base": BASE},
            ensure_ascii=False,
        ),
        flush=True,
    )

    if args.smoke:
        key = load_key()
        rec = gold_sub[0]
        payload = [{"id": rec_id(rec), "sentence": rec.get("sentence") or "", "domain": rec.get("source_domain") or rec.get("hybrid_source") or ""}]
        code, text, err, meta = chat(key, prompt, payload, model)
        smoke_path = OUT / f"smoke_{slug}.txt"
        smoke_path.write_text(text or (err or ""), encoding="utf-8")
        print(
            json.dumps(
                {"smoke_status": code, "err": err, "out_chars": len(text or ""), "id": rec_id(rec), "raw": str(smoke_path), **meta},
                ensure_ascii=False,
            ),
            flush=True,
        )
        if code != 200:
            return 2
        parsed = parse_results(text, [rec_id(rec)])
        print(json.dumps(parsed[0], ensure_ascii=False), flush=True)
        return 0

    raw_dir = OUT / f"raw_{slug}"
    raw_dir.mkdir(exist_ok=True)
    done_path = OUT / f"records_{slug}.jsonl"
    done: dict[str, dict] = {}
    if done_path.is_file():
        for line in done_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done[str(rec["id"])] = rec

    if not args.score_only:
        key = load_key()
        pending = [gold_map[i] for i in ids if i not in done]
        workers = max(1, int(args.workers))
        print(
            json.dumps(
                {"done": len(done), "pending": len(pending), "batch": args.batch, "workers": workers},
                ensure_ascii=False,
            ),
            flush=True,
        )
        write_lock = Lock()
        stop = {"err": None}

        def run_batch(b: int, chunk: list[dict]) -> tuple[int, list[str], list[dict] | None, str, str | None]:
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
            max_tokens = 2048 if model in {"gpt-4", "gpt-4-0613"} else 4096
            for attempt in range(6):
                code, raw_text, err, _meta = chat(key, prompt, send, model, max_tokens=max_tokens)
                if code == 429 or (err and "429" in str(err)):
                    last_err = err or f"http_{code}"
                    time.sleep(min(20, 2 ** attempt))
                    continue
                if code != 200 or not (raw_text or "").strip():
                    last_err = err or f"http_{code}"
                    time.sleep(1 + attempt)
                    continue
                try:
                    parsed = parse_results(raw_text, cids)
                    if any(r.get("comment") == "missing_in_model_output" for r in parsed):
                        raise ValueError("missing_ids")
                    last_err = None
                    break
                except Exception as e:
                    last_err = f"{type(e).__name__}: {e}"
                    time.sleep(1 + attempt)
            return b, cids, parsed, raw_text, last_err

        batches = [(b, pending[b : b + args.batch]) for b in range(0, len(pending), args.batch)]
        with done_path.open("a", encoding="utf-8") as fout:

            def commit(b: int, chunk: list[dict], cids: list[str], parsed: list[dict], raw_text: str) -> None:
                (raw_dir / f"batch_{b:04d}.txt").write_text(raw_text or "", encoding="utf-8")
                for src, hit in zip(chunk, parsed):
                    row, miss = pred_row(
                        src,
                        hit["spans"],
                        {"comment": hit.get("comment") or "", "prompt": "sop_extract_v4"},
                        model,
                    )
                    fout.write(json.dumps(row, ensure_ascii=False) + "\n")
                    fout.flush()
                    done[row["id"]] = row
                print(
                    json.dumps(
                        {
                            "wrote": len(done),
                            "of": len(ids),
                            "batch": b,
                            "unaligned": sum(len(done[i].get("unaligned") or []) for i in cids),
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )

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
                    return 2

    missing = [i for i in ids if i not in done]
    if missing:
        print(json.dumps({"incomplete": True, "missing_n": len(missing), "missing_head": missing[:10]}, ensure_ascii=False))
        return 1

    ordered = [done[i] for i in ids]
    pred_raw = OUT / f"pred_{slug}_sop_extract.jsonl"
    write_jsonl(pred_raw, ordered)
    pred_cws = [cws.rewrite_record(r, tag_field="pred_tags") for r in ordered]
    pred_cws_path = OUT / f"pred_{slug}_sop_extract_cws.jsonl"
    write_jsonl(pred_cws_path, pred_cws)

    old_rows = subset_old_chatgpt(set(ids), gold_map)
    old_cws = [cws.rewrite_record(r, tag_field=None) for r in old_rows]
    old_cws_path = OUT / "pred_chatgpt_olddump_cws.jsonl"
    write_jsonl(old_cws_path, old_cws)

    gold_v2 = {rec_id(r): r for r in cws.load_jsonl(GOLD_V2)}
    gold_v2_sub = [gold_v2[i] for i in ids if i in gold_v2]
    gold_v2_path = OUT / "gold_v2_sample100.jsonl"
    write_jsonl(gold_v2_path, gold_v2_sub)

    summary = {
        "n": len(ids),
        "n_simhuman": n_sim,
        "n_sop_cws": len(ids) - n_sim,
        "n_unaligned_sents": sum(1 for r in ordered if r.get("unaligned")),
        "n_spans": sum(len(r.get("spans") or []) for r in ordered),
        "n_empty": sum(1 for r in ordered if not (r.get("spans") or [])),
        "model": model,
        "base": BASE,
        "prompt": "SOP extract v4 (no silver); not the frozen @@span## dump prompt",
        "gold_v2_untouched": True,
        "chatgpt_dump_untouched": True,
        "not_for_table3": True,
        "hybrid_cws": {
            "sop_extract_jieba": slim(gold_path, pred_cws_path),
            "chatgpt_olddump_jieba": slim(gold_path, old_cws_path),
        },
    }
    old_raw_path = OUT / "pred_chatgpt_olddump_raw.jsonl"
    write_jsonl(old_raw_path, old_rows)
    summary["gold_v2"] = {
        "sop_extract_raw": slim(gold_v2_path, pred_raw),
        "chatgpt_olddump_raw": slim(gold_v2_path, old_raw_path),
    }
    (OUT / f"summary_{slug}.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
