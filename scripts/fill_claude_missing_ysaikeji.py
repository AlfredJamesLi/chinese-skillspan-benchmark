#!/usr/bin/env python3
"""Fill the 98 missing Gold-v2 IDs in the Claude dump.

Does not overwrite merged_test_cluade.jsonl or Claude_unique_first_v2.jsonl.
Uses the original @@span##[L|K|S|T] Table-3 prompt. Fill model is
claude-sonnet-4-6 (original dump is claude-3-5-haiku-20241022; haiku is 403 here).
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
from expand_goldstyle_train import apply_text_spans  # noqa: E402
from score_lskt import load_records, rec_id, score  # noqa: E402

GOLD = PAPER / "data/gold_canonical_v2.jsonl"
CLAUDE_VIEW = PAPER / "reports/views/Claude_unique_first_v2.jsonl"
OUT_DIR = PAPER / "output/llm_fill_missing"
KEY_PATH = Path.home() / ".config/ysaikeji/api_key"
BASE = "https://claudeplus.ysaikeji.cn"
MODEL = "claude-sonnet-4-6"
CTX = ssl.create_default_context()
PAT_BRACKET = re.compile(r"@@\s*(.+?)\s*##\s*\[([LKST])\]", re.DOTALL)
PAT_BARE = re.compile(r"@@\s*(.+?)\s*##([LKST])\b", re.DOTALL)

SYSTEM = (
    "你是一名熟悉中文招聘文本的人力资源与技能本体（ESCO）专家。"
    "你的任务是在原句中标注与能力相关的片段，并严格遵循 ESCO-1.20 的 LKST 平面标注政策：\n"
    "• [L] Language：仅限自然语言能力/证书/等级/使用（如英语六级、日语N2、普通话二甲、能用英语沟通）。\n"
    "• [K] Knowledge：学科/领域/规范/标准/法规/框架/工具体系等“拥有/了解”的知识客体（名词本体）。\n"
    "• [S] Skills：可训练/执行/操作的能力或方法（做事动作或过程，如 制定/开发/调试/部署/评审/配置/优化 等；编程语言与工具使用也归此类）。\n"
    "• [T] Transversal：跨岗位通用能力（沟通、协作、学习、时间管理、抗压、领导力、客户导向等）。\n\n"
    "全局规则：平面标注（不重叠、不嵌套）；采用最小充分片段；并列项逐一切分；"
    "剥离“参与/负责/进行/熟悉/掌握/具备/能够/良好/较强”等触发或评价词。\n\n"
    "你将获得一句中文招聘文本。请在原句中用 `@@片段##[L|K|S|T]` 标注所有能力相关片段，遵循：\n"
    "1) 平面标注：不重叠、不嵌套；并列项逐一切分；\n"
    "2) 最小充分片段：去掉轻动词/评价/程度与连接词，仅保留能自解释的核心片段；\n"
    "3) K/S 语境：名词本体处于“知识/了解/熟悉/具备…知识/理解”语境多判 K；"
    "在“制定/设计/评审/配置/开发/调试/部署/维护/优化/调优”等动作语境多判 S；\n"
    "4) 语言 L：仅自然语言/证书/等级/使用；编程语言与工具使用归 S；\n"
    "5) 冲突兜底：先按语境判定 K/S；若仍冲突，则按优先级 L > S > K > T；\n"
    "6) 无能力相关内容时原样返回。\n"
    "输出仅包含一行：标注后的句子。"
)


def load_key() -> str:
    key = (os.environ.get("YSAIKEJI_API_KEY") or "").strip()
    if key.startswith("sk-") and len(key) >= 20:
        return key
    if KEY_PATH.is_file():
        key = KEY_PATH.read_text(encoding="utf-8").strip()
        if key.startswith("sk-") and len(key) >= 20:
            return key
    raise SystemExit("missing YSAIKEJI_API_KEY or ~/.config/ysaikeji/api_key")


def parse_marked(text: str) -> list[dict]:
    raw = (text or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    spans = [{"text": a.strip(), "type": b} for a, b in PAT_BRACKET.findall(raw)]
    if spans:
        return spans
    return [{"text": a.strip(), "type": b} for a, b in PAT_BARE.findall(raw)]


def chat(key: str, sentence: str, timeout: int = 120) -> tuple[int | None, str, str | None]:
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": sentence},
        ],
        "max_tokens": 4096,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            parsed = json.loads(resp.read().decode("utf-8"))
            content = (((parsed.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
            return resp.status, content, None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace") if e.fp else ""
        return e.code, "", raw[:800]
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"


def tokens_of(rec: dict) -> list[str]:
    toks = rec.get("tokens")
    if isinstance(toks, list) and toks:
        return [str(t) for t in toks]
    return list(rec.get("sentence") or "")


def main() -> int:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    key = load_key()
    gold = {rec_id(r): r for r in load_records(str(GOLD))}
    claude = {rec_id(r): r for r in load_records(str(CLAUDE_VIEW))}
    missing = [i for i in gold if i not in claude]
    todo = missing[:limit] if limit else missing
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = OUT_DIR / "Claude_fill_raw.jsonl"
    done: dict[str, dict] = {}
    if raw_path.is_file():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done[str(rec["id"])] = rec
    pending = [i for i in todo if i not in done]
    print(
        json.dumps(
            {"gold": len(gold), "claude": len(claude), "missing": len(missing), "pending": len(pending), "model": MODEL},
            ensure_ascii=False,
        ),
        flush=True,
    )
    with raw_path.open("a", encoding="utf-8") as fout:
        for n, cid in enumerate(pending, 1):
            rec = gold[cid]
            sent = rec.get("sentence") or ""
            status, text, err = chat(key, sent)
            if status != 200 or not text:
                print(json.dumps({"fail": cid, "status": status, "err": err}, ensure_ascii=False), flush=True)
                time.sleep(1.0)
                status, text, err = chat(key, sent)
            if status != 200:
                print(json.dumps({"abort": cid, "status": status, "err": err}, ensure_ascii=False), flush=True)
                return 2
            spans = parse_marked(text)
            tags, miss = apply_text_spans({"tokens": tokens_of(rec), "sentence": sent}, spans)
            row = {
                "id": cid,
                "sentence": sent,
                "tokens": tokens_of(rec),
                "source_domain": rec.get("source_domain") or "",
                "pred_tags": tags,
                "list_of_selection_bio4": tags,
                "list_of_selection": tags,
                "model": MODEL,
                "model_output": text,
                "annotated_sentence": text,
                "checker": {"verdict": "OK", "issues": [], "hints": []},
                "_fill": {
                    "source": "ysaikeji_fill_missing",
                    "reason": "missing",
                    "unaligned": miss,
                    "model": MODEL,
                    "original_dump_model": "claude-3-5-haiku-20241022",
                },
            }
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            fout.flush()
            done[cid] = row
            if n % 10 == 0 or n == len(pending):
                print(json.dumps({"wrote": n, "of": len(pending), "id": cid}), flush=True)
            time.sleep(0.2)
    if any(i not in done for i in missing):
        print(json.dumps({"partial": True, "done": len(done), "want": len(missing), "raw": str(raw_path)}))
        return 0
    merged = []
    seen = set()
    for rec in list(claude.values()) + [done[i] for i in missing]:
        i = rec_id(rec)
        if i in seen:
            continue
        merged.append(done[i] if i in done else rec)
        seen.add(i)
    view_out = PAPER / "reports/views/Claude_filled_v2.jsonl"
    view_out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in merged), encoding="utf-8")
    report = score(str(GOLD), str(view_out), align_mode="official", n_boot=0)
    slim = {
        "alignment_ok": report.get("alignment_ok"),
        "n_missing": report.get("n_missing"),
        "n_matched": report.get("n_matched"),
        "typed_exact_f1": (report.get("typed_exact") or {}).get("f1"),
        "collapsed_exact_f1": (report.get("collapsed_exact") or {}).get("f1"),
        "typed_relaxed_f1": (report.get("typed_relaxed") or {}).get("f1"),
        "filled": len(missing),
        "view": str(view_out),
        "model_used": MODEL,
        "note": "Ysaikeji fill of 98 missing Claude rows; original haiku dump untouched. Mixed haiku+sonnet-4-6. Not PDF Table 3 overwrite.",
    }
    (OUT_DIR / "Claude_fill_summary.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(slim, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
