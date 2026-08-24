#!/usr/bin/env python3
"""Gold-style relabel of a 4k train subset. Does not overwrite train.json or Gold v2.

Default backend is local Qwen2.5-14B-Instruct (silver proxy now serves HTML).
The 80 human-final items are injected and not re-queried.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import requests

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
FINAL80 = PAPER / "reports/gold_style_relabel/sample80_final.json"
OUT_DIR = PAPER / "output/goldstyle_train_4k"

SYSTEM = """你是中文招聘广告技能标注员。从句子中抽出岗位对候选人要求的能力跨度，打上 L/K/S/T。
L：语言/语种。K：学历、专业、资格考试、领域理论。S：可执行技能、工具框架、语言使用、岗位职责活动。T：软技能、特质、态度。
规则：
1. 一条要求标成一段完整原文，不要切成2-4字碎片，不要从词中间切断。
2. 只有不同要求才拆开。岗位职责整段可以标成一条S。
3. 熟悉/掌握框架、编程语言、办公软件 → S。学历专业资格考试领域理论 → K。
4. 不标：年限套话、形象外貌、身体健康、挑战高薪、留学优先、非司机岗驾照、报名流程、公示体检、资格审查手续、公司给员工的培训福利班次、宣传口号。
5. 整句无能力要求则 spans 为空数组。跨度必须是句中连续原文。
只输出 JSON 数组，每项：{"id":"...","spans":[{"text":"完整原文","type":"S"}]}
无技能：{"id":"...","spans":[]}"""


def bio_n(tags) -> int:
    n = 0
    for t in tags or []:
        if str(t).startswith("B-"):
            n += 1
    return n


def bucket(rec: dict) -> str:
    n = bio_n(rec.get("list_of_selection_bio4") or [])
    if n == 0:
        return "empty"
    if n <= 2:
        return "low"
    return "high"


def find_span(tokens: list[str], text: str) -> tuple[int, int] | None:
    flat = "".join(tokens)
    needle = (text or "").strip()
    if not needle:
        return None
    pos = flat.find(needle)
    if pos < 0:
        return None
    acc = 0
    start = None
    for i, tok in enumerate(tokens):
        nxt = acc + len(tok)
        if start is None and acc <= pos < nxt:
            start = i
        if start is not None and nxt >= pos + len(needle):
            return start, i + 1
        acc = nxt
    return None


def spans_to_bio(n: int, spans: list[tuple[int, int, str]]) -> list[str]:
    tags = ["O"] * n
    for a, b, t in sorted(spans):
        if a < 0 or b > n or a >= b:
            continue
        if t not in {"L", "K", "S", "T"}:
            t = "S"
        if any(tags[i] != "O" for i in range(a, b)):
            continue
        tags[a] = f"B-{t}"
        for i in range(a + 1, b):
            tags[i] = f"I-{t}"
    return tags


def parse_json_array(text: str) -> list:
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start, end = text.find("["), text.rfind("]")
    if start < 0 or end <= start:
        raise ValueError("no json array")
    return json.loads(text[start : end + 1])


def _first_sk(text: str) -> str:
    for part in (text or "").replace("\n", ",").split(","):
        part = part.strip().strip('"').strip("'")
        if part.startswith("sk-") and " " not in part:
            return part
    return ""


def load_keys() -> list[str]:
    found: list[str] = []
    for env in ("GOLDSTYLE_API_KEY", "OPENAI_API_KEY", "OPENAI_API_KEYS"):
        raw = os.environ.get(env) or ""
        if env == "OPENAI_API_KEYS":
            for part in raw.split(","):
                k = _first_sk(part)
                if k and k not in found:
                    found.append(k)
        else:
            k = _first_sk(raw) or raw.strip()
            if k.startswith("sk-") and k not in found:
                found.append(k)
    sh = os.environ.get("GOLDSTYLE_KEYS_SH", "")
    if sh and Path(sh).is_file():
        for line in Path(sh).read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if "OPENAI_API_KEY" not in s and "GOLDSTYLE" not in s:
                continue
            for m in re.findall(r"sk-[A-Za-z0-9]{20,}", s):
                if m not in found:
                    found.append(m)
    if not found:
        try:
            sys.path.insert(0, str(ROOT))
            from api_key import OPENAI_API_KEY as k2  # type: ignore

            if k2 and k2 not in found:
                found.append(k2)
        except Exception:
            pass
    return found


def load_key() -> str:
    ks = load_keys()
    return ks[0] if ks else ""


def load_local(path: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()
    return tok, model


def chat_local(messages: list[dict], tok, model, max_new: int = 2048) -> str:
    import torch

    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok(text, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.inference_mode():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new,
            do_sample=False,
        )
    gen = out[0, inputs["input_ids"].shape[1] :]
    return tok.decode(gen, skip_special_tokens=True)


def chat(messages: list[dict], model: str, base: str, key: str, timeout: int = 180) -> str:
    # Same URL shape as utils/chat_utils._chat_openai_raw
    host = base.rstrip("/")
    if host.endswith("/v1"):
        host = host[:-3]
    url = host + "/v1/chat/completions"
    r = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 4096,
        },
        timeout=timeout,
    )
    ctype = (r.headers.get("content-type") or "").lower()
    body = r.text or ""
    if "html" in ctype or body.lstrip().startswith("<"):
        raise RuntimeError(f"non-json http={r.status_code} ctype={ctype} body={body[:120]}")
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]


def sample_ids(rows: list[dict], n: int, seed: int, force: set[str]) -> list[str]:
    rng = random.Random(seed)
    cells: dict[tuple[str, str], list[str]] = defaultdict(list)
    by_id = {r["id"]: r for r in rows}
    for rec in rows:
        cells[(rec.get("source_domain") or "NA", bucket(rec))].append(rec["id"])
    quota = {
        ("应届生招聘", "empty"): 600,
        ("应届生招聘", "low"): 600,
        ("应届生招聘", "high"): 800,
        ("人工智能招聘", "empty"): 600,
        ("人工智能招聘", "low"): 600,
        ("人工智能招聘", "high"): 800,
    }
    picked: list[str] = []
    used: set[str] = set()
    for fid in force:
        if fid in by_id and fid not in used:
            picked.append(fid)
            used.add(fid)
    for key, q in quota.items():
        already = sum(
            1
            for i in picked
            if (by_id[i].get("source_domain") or "NA", bucket(by_id[i])) == key
        )
        pool = [i for i in cells.get(key, []) if i not in used]
        rng.shuffle(pool)
        take = pool[: max(0, q - already)]
        picked.extend(take)
        used.update(take)
    if len(picked) < n:
        rest = [r["id"] for r in rows if r["id"] not in used]
        rng.shuffle(rest)
        picked.extend(rest[: n - len(picked)])
    return picked


def apply_text_spans(rec: dict, spans: list[dict]) -> tuple[list[str], list]:
    toks = [str(t) for t in (rec.get("tokens") or list(rec.get("sentence") or ""))]
    aligned = []
    miss = []
    for sp in spans or []:
        text = (sp.get("text") if isinstance(sp, dict) else "") or ""
        typ = str((sp.get("type") if isinstance(sp, dict) else "S") or "S").strip().upper()[:1]
        if typ not in {"L", "K", "S", "T"}:
            typ = "S"
        hit = find_span(toks, text)
        if hit is None:
            miss.append(text)
        else:
            aligned.append((hit[0], hit[1], typ))
    return spans_to_bio(len(toks), aligned), miss


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=20260823)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--sleep", type=float, default=0.4)
    ap.add_argument("--model", default=os.environ.get("GOLDSTYLE_MODEL", "gpt-4o"))
    ap.add_argument("--api_base", default=os.environ.get("GOLDSTYLE_API_BASE", os.environ.get("api_base", "https://api.claude-Plus.top/v1")))
    ap.add_argument("--backend", default=os.environ.get("GOLDSTYLE_BACKEND", "local"), choices=["local", "api"])
    ap.add_argument(
        "--local_model",
        default=os.environ.get(
            "GOLDSTYLE_LOCAL_MODEL",
            str(ROOT / "LLaMA-Factory/Qwen2.5-14B-Instruct"),
        ),
    )
    ap.add_argument("--limit", type=int, default=0, help="Cap pending LLM items; 0 = all")
    ap.add_argument("--out_dir", default=str(OUT_DIR))
    ap.add_argument("--skip_api", action="store_true")
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = json.loads(TRAIN.read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in rows}
    final80 = {x["id"]: x for x in json.loads(FINAL80.read_text(encoding="utf-8"))}
    ids = sample_ids(rows, args.n, args.seed, set(final80))
    (out / "sample_ids.json").write_text(json.dumps(ids, ensure_ascii=False, indent=2), encoding="utf-8")
    raw_path = out / "llm_raw.jsonl"
    done = set()
    if raw_path.is_file():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["id"])
    pending = [i for i in ids if i not in done and i not in final80]
    if args.limit and args.limit > 0:
        pending = pending[: args.limit]
    print(
        json.dumps(
            {
                "n_ids": len(ids),
                "done": len(done),
                "final80": len(final80),
                "pending": len(pending),
                "backend": args.backend,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    if not args.skip_api and pending:
        tok = loc = None
        keys: list[str] = []
        if args.backend == "local":
            tok, loc = load_local(args.local_model)
        else:
            key = load_key()
            if not key:
                raise SystemExit("missing OPENAI_API_KEY / GOLDSTYLE_API_KEY")
            keys = load_keys() or [key]
        for i in range(0, len(pending), args.batch):
            chunk = pending[i : i + args.batch]
            lines = [f"{j+1}. id=`{cid}`  {(by_id[cid].get('sentence') or '')[:800]}" for j, cid in enumerate(chunk)]
            user = "只输出 JSON 数组。\n\n句子：\n" + "\n".join(lines)
            err = None
            for attempt in range(4):
                try:
                    if args.backend == "local":
                        text = chat_local(
                            [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                            tok,
                            loc,
                        )
                    else:
                        text = chat(
                            [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                            args.model,
                            args.api_base,
                            keys[attempt % len(keys)],
                        )
                    parsed = parse_json_array(text)
                    by_ret = {str(x.get("id")): x for x in parsed if isinstance(x, dict)}
                    with raw_path.open("a", encoding="utf-8") as w:
                        for cid in chunk:
                            rec = by_ret.get(cid) or {"id": cid, "spans": [], "comment": "missing_in_batch"}
                            rec["id"] = cid
                            rec["raw_ok"] = cid in by_ret
                            rec["backend"] = args.backend
                            w.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    err = None
                    break
                except Exception as e:
                    err = e
                    time.sleep(1 + attempt)
            if err is not None:
                with raw_path.open("a", encoding="utf-8") as w:
                    for cid in chunk:
                        w.write(json.dumps({"id": cid, "spans": [], "error": str(err)[:300]}, ensure_ascii=False) + "\n")
            print(json.dumps({"batch": i // args.batch, "got": min(i + args.batch, len(pending)), "err": str(err)[:120] if err else None}, ensure_ascii=False), flush=True)
            if args.backend == "api":
                time.sleep(args.sleep)
    llm_map = dict(final80)
    if raw_path.is_file():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec.get("id") not in llm_map:
                llm_map[rec["id"]] = rec
    train_out = []
    n_miss = 0
    n_empty = 0
    for cid in ids:
        src = by_id[cid]
        lab = llm_map.get(cid) or {"spans": []}
        bio, miss = apply_text_spans(src, lab.get("spans") or [])
        n_miss += len(miss)
        if not any(t != "O" for t in bio):
            n_empty += 1
        train_out.append(
            {
                "id": cid,
                "global_id": src.get("global_id"),
                "sentence_order": src.get("sentence_order"),
                "sentence": src.get("sentence"),
                "tokens": src.get("tokens"),
                "list_of_selection_bio4": bio,
                "source_domain": src.get("source_domain"),
                "title": src.get("title"),
                "goldstyle_source": "final80" if cid in final80 else "llm",
                "unaligned": miss,
            }
        )
    rng = random.Random(args.seed)
    order = list(range(len(train_out)))
    rng.shuffle(order)
    n_dev = max(200, len(train_out) // 10)
    dev_idx = set(order[:n_dev])
    train_split = [train_out[i] for i in order if i not in dev_idx]
    dev_split = [train_out[i] for i in order if i in dev_idx]
    (out / "train_goldstyle_4k.json").write_text(json.dumps(train_split, ensure_ascii=False), encoding="utf-8")
    (out / "dev_goldstyle_4k.json").write_text(json.dumps(dev_split, ensure_ascii=False), encoding="utf-8")
    meta = {
        "n_ids": len(ids),
        "n_train": len(train_split),
        "n_dev": len(dev_split),
        "n_empty": n_empty,
        "n_unaligned_spans": n_miss,
        "n_from_final80": sum(1 for r in train_out if r["goldstyle_source"] == "final80"),
        "model": args.local_model if args.backend == "local" else args.model,
        "backend": args.backend,
        "overwrites_corpus_train": False,
        "overwrites_gold_v2": False,
    }
    (out / "build_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
