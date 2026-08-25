#!/usr/bin/env python3
"""Fill missing Gold-v2 IDs in the Table-3 Kimi dump via Moonshot.

Does not overwrite merged_test_kimi.jsonl or Kimi_unique_first_v2.jsonl.
Uses the same @@span##[L|K|S|T] prompt as the original dump.
"""
from __future__ import annotations

import json
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
KIMI_VIEW = PAPER / "reports/views/Kimi_unique_first_v2.jsonl"
OUT_DIR = PAPER / "output/llm_fill_missing"
KEY_PATH = Path.home() / ".config/moonshot/api_key"
BASE = "https://api.moonshot.cn/v1"
MODELS = ("kimi-k2.6",)  # kimi-k2-0711-preview is no longer served
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
    key = KEY_PATH.read_text(encoding="utf-8").strip()
    if not key.startswith("sk-") or len(key) < 20:
        raise SystemExit(f"bad key file: {KEY_PATH}")
    return key


def parse_marked(text: str) -> list[dict]:
    raw = (text or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    spans = [{"text": a.strip(), "type": b} for a, b in PAT_BRACKET.findall(raw)]
    if spans:
        return spans
    return [{"text": a.strip(), "type": b} for a, b in PAT_BARE.findall(raw)]


def chat(
    key: str,
    model: str,
    sentence: str,
    timeout: int = 120,
    *,
    with_thinking: bool = True,
) -> tuple[int | None, str, str | None]:
    body: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": sentence},
        ],
        "max_tokens": 4096,
    }
    if with_thinking:
        body["thinking"] = {"type": "disabled"}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE + "/chat/completions", data=data, method="POST")
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


def is_quota_fail(rec: dict) -> bool:
    chk = rec.get("checker") or {}
    issues = chk.get("issues") or []
    if any("quota" in str(x).lower() for x in issues):
        return True
    return not str(rec.get("model_output") or "").strip()


def main() -> int:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    key = load_key()
    gold = {rec_id(r): r for r in load_records(str(GOLD))}
    kimi = {rec_id(r): r for r in load_records(str(KIMI_VIEW))}
    missing = [i for i in gold if i not in kimi]
    quota = [i for i, r in kimi.items() if i in gold and is_quota_fail(r)]
    todo = missing + [i for i in quota if i not in missing]
    if limit:
        todo = todo[:limit]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = OUT_DIR / "Kimi_fill_raw.jsonl"
    done: dict[str, dict] = {}
    if raw_path.is_file():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done[str(rec["id"])] = rec
    pending = [i for i in todo if i not in done]
    print(
        json.dumps(
            {
                "gold": len(gold),
                "kimi": len(kimi),
                "missing": len(missing),
                "quota_in_dump": len(quota),
                "todo": len(todo),
                "pending": len(pending),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    model_used = MODELS[0]
    with raw_path.open("a", encoding="utf-8") as fout:
        for n, cid in enumerate(pending, 1):
            rec = gold[cid]
            sent = rec.get("sentence") or ""
            text = err = None
            code = None
            for model in MODELS:
                for attempt in range(6):
                    code, text, err = chat(key, model, sent, with_thinking=True)
                    if code == 200 and (text or "").strip():
                        model_used = model
                        err = None
                        break
                    if code == 200:
                        err = "empty_output"
                    time.sleep(1 + attempt)
                else:
                    continue
                break
            if err is not None or code != 200 or not (text or "").strip():
                print(json.dumps({"id": cid, "error": err or f"http_{code}"}), flush=True)
                continue
            spans = parse_marked(text)
            tags, miss = apply_text_spans(rec, spans)
            src = dict(kimi.get(cid) or rec)
            row = src
            row["id"] = cid
            row["sentence"] = sent
            row["tokens"] = tokens_of(src) or tokens_of(rec)
            row["pred_tags"] = tags
            row["list_of_selection_bio4"] = tags
            row["list_of_selection"] = tags
            row["model"] = model_used
            row["model_output"] = text
            row["annotated_sentence"] = text
            row["checker"] = {"verdict": "OK", "issues": [], "hints": []}
            row["_fill"] = {
                "source": "moonshot_fill_missing",
                "reason": "missing" if cid not in kimi else "quota_fail",
                "unaligned": miss,
                "model": model_used,
            }
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            fout.flush()
            done[cid] = row
            if n % 10 == 0 or n == len(pending):
                print(json.dumps({"wrote": n, "of": len(pending), "id": cid}), flush=True)
            time.sleep(0.25)
    filled_ids = [i for i in (missing + quota) if i in done]
    want = missing + [i for i in quota if i not in missing]
    if limit or any(i not in done for i in want):
        print(
            json.dumps(
                {"partial": True, "done": len(filled_ids), "want": len(want), "raw": str(raw_path)},
                ensure_ascii=False,
            )
        )
        return 0
    merged = []
    seen = set()
    for rec in list(kimi.values()) + [done[i] for i in done]:
        i = rec_id(rec)
        if i in seen:
            continue
        if i in done:
            merged.append(done[i])
        else:
            merged.append(rec)
        seen.add(i)
    for i in missing:
        if i in done and i not in seen:
            merged.append(done[i])
            seen.add(i)
    view_out = PAPER / "reports/views/Kimi_filled_v2.jsonl"
    view_out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in merged), encoding="utf-8")
    report = score(str(GOLD), str(view_out), align_mode="official", n_boot=0)
    slim = {
        "alignment_ok": report.get("alignment_ok"),
        "n_missing": report.get("n_missing"),
        "n_matched": report.get("n_matched"),
        "typed_exact_f1": (report.get("typed_exact") or {}).get("f1"),
        "collapsed_exact_f1": (report.get("collapsed_exact") or {}).get("f1"),
        "typed_relaxed_f1": (report.get("typed_relaxed") or {}).get("f1"),
        "filled": len(filled_ids),
        "view": str(view_out),
        "model_used": model_used,
        "note": "Moonshot fill of missing/quota Kimi rows; original dump untouched. Not PDF Table 3 overwrite.",
    }
    (OUT_DIR / "Kimi_fill_summary.json").write_text(
        json.dumps(slim, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(slim, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
