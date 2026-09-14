#!/usr/bin/env python3
"""Draw the frozen 150 human QA sample from NEW public-API Silver (7936).

Seed/salt are the pre-declared values in human_qa150/STATUS.json.
Domain mix follows the 10k top-up 40/30/30 (60/45/45), then SRS inside
each domain by sha256(salt|seed|id). Do not redraw.

Not independent blind Gold. Not paper-main. If these IDs later become a
test set, drop them from future student train; do not swap the 150.
"""
from __future__ import annotations

import hashlib
import json
import unicodedata
from collections import Counter
from pathlib import Path

from silver_public_api_lib import dump_json, dump_jsonl, load_jsonl, to_student_row

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PREP = PAPER / "data/silver_plus_10k_prep_20260913"
OUT = PREP / "human_qa150"
GOLD150 = PAPER / "data/gold150_test.jsonl"
STUDENT_SPLIT = PAPER / "output/silver_new_merged_student_20260914/data/SPLIT.json"
TRAIN = PAPER / "output/silver_new_merged_student_20260914/data/train.jsonl"
DEV = PAPER / "output/silver_new_merged_student_20260914/data/dev.jsonl"
ZIP_DIR = PREP / "cnss_silver_wave1_wave2_20260914T040731Z"
RUN2500 = PREP / "run2500_public_api_v1/labeled.jsonl"
WAVE3 = PREP / "codex_remaining_5436/waves/wave3/labeled.jsonl"
REMAINING = PREP / "codex_remaining_5436/remaining.jsonl"

SEED = 20260913
SALT = "CNSS_SP_NEW150_QA"
N = 150
QUOTA = {"阿里云公开数据集": 60, "事业单位招聘": 45, "上市公司招聘": 45}


def nfc_key(s: str) -> str:
    t = unicodedata.normalize("NFC", s or "")
    return "".join(t.split())


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rank_key(sid: str) -> str:
    return hashlib.sha256(f"{SALT}|{SEED}|{sid}".encode("utf-8")).hexdigest()


def span_objs(text: str, spans) -> list[dict]:
    out = []
    for item in spans or []:
        if isinstance(item, dict):
            a, b = int(item["start"]), int(item["end"])
            lab = str(item.get("label") or item.get("type") or "")
            tx = item.get("text") if isinstance(item.get("text"), str) else text[a:b]
        else:
            a, b, lab = int(item[0]), int(item[1]), str(item[2])
            tx = text[a:b]
        if text[a:b] != tx:
            raise ValueError(f"slice mismatch {a}:{b}")
        out.append({"start": a, "end": b, "text": tx, "label": lab})
    return out


def triples(objs: list[dict]) -> list[list]:
    return [[o["start"], o["end"], o["label"]] for o in objs]


def from_student(path: Path, wave: str) -> list[dict]:
    rows = []
    for r in load_jsonl(path):
        text = r.get("sentence") or r.get("text") or ""
        objs = span_objs(text, r.get("spans") or [])
        rows.append(
            {
                "id": r["id"],
                "text": text,
                "spans": objs,
                "gpt6_label": triples(objs),
                "status": r.get("status"),
                "note": r.get("note"),
                "issues": r.get("issues") or [],
                "source_domain": r.get("source_domain"),
                "source_file": r.get("source_file"),
                "nfc_sha1": r.get("nfc_sha1"),
                "prompt_id": r.get("prompt_id") or "silver_public_api_v1.0",
                "model": r.get("model") or "gpt-6-astra",
                "wave": wave,
            }
        )
    return rows


def from_zip(remaining: dict[str, dict]) -> list[dict]:
    rows = []
    for r in load_jsonl(ZIP_DIR / "data/all_candidates_3620.jsonl"):
        src = remaining[r["id"]]
        stu = to_student_row(src, r)
        text = stu["sentence"]
        objs = span_objs(text, r.get("spans") or [])
        rows.append(
            {
                "id": r["id"],
                "text": text,
                "spans": objs,
                "gpt6_label": triples(objs),
                "status": r.get("status"),
                "note": r.get("note"),
                "issues": r.get("issues") or [],
                "source_domain": src.get("source_domain"),
                "source_file": src.get("source_file"),
                "nfc_sha1": src.get("nfc_sha1"),
                "prompt_id": "silver_public_api_v1.0",
                "model": "gpt-6-astra",
                "wave": "wave1_wave2_zip",
            }
        )
    return rows


def main() -> int:
    remaining = {r["id"]: r for r in load_jsonl(REMAINING)}
    pool = from_student(RUN2500, "run2500") + from_zip(remaining) + from_student(WAVE3, "wave3")
    ids = [r["id"] for r in pool]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate ids in labeled pool")
    if len(pool) != 7936:
        raise SystemExit(f"expected 7936 labeled new silver, got {len(pool)}")

    human350 = load_jsonl(PREP / "human350/ids.jsonl")
    block_ids = {str(o["id"]) for o in human350 if o.get("id")}
    block_nfc = {str(o["nfc_sha1"]) for o in human350 if o.get("nfc_sha1")}
    gold_nfc = set()
    gold_ids = set()
    for r in load_jsonl(GOLD150):
        gold_ids.add(str(r.get("source_id") or r.get("id") or "").strip())
        gold_nfc.add(nfc_key(r.get("text") or r.get("sentence") or ""))
    frame = []
    dropped = Counter()
    for r in pool:
        if r["id"] in block_ids or r["id"] in gold_ids:
            dropped["human350_or_gold150_id"] += 1
            continue
        if r.get("nfc_sha1") in block_nfc or nfc_key(r["text"]) in gold_nfc:
            dropped["human350_or_gold150_nfc"] += 1
            continue
        frame.append(r)
    by_d: dict[str, list] = {}
    for r in frame:
        by_d.setdefault(r.get("source_domain") or "unk", []).append(r)
    missing_q = [d for d in QUOTA if d not in by_d]
    if missing_q:
        raise SystemExit(f"missing domains in frame: {missing_q}")
    drawn = []
    for d, q in QUOTA.items():
        ranked = sorted(by_d[d], key=lambda r: (rank_key(str(r["id"])), r["id"]))
        if len(ranked) < q:
            raise SystemExit(f"{d}: {len(ranked)} < quota {q}")
        drawn.extend(ranked[:q])
    drawn.sort(key=lambda r: (rank_key(str(r["id"])), r["id"]))
    if len(drawn) != N:
        raise SystemExit(f"drew {len(drawn)} != {N}")

    train_ids = {r["id"] for r in load_jsonl(TRAIN)} if TRAIN.is_file() else set()
    dev_ids = {r["id"] for r in load_jsonl(DEV)} if DEV.is_file() else set()

    tasks, ai_only, id_rows = [], [], []
    for i, r in enumerate(drawn, start=1):
        ai_only.append(
            {
                "id": r["id"],
                "text": r["text"],
                "ai_label": r["gpt6_label"],
                "spans": r["spans"],
                "status": r["status"],
                "note": r.get("note"),
                "issues": r.get("issues") or [],
                "model": r.get("model"),
                "prompt_id": r.get("prompt_id"),
                "source_domain": r.get("source_domain"),
                "wave": r.get("wave"),
            }
        )
        tasks.append(
            {
                "qa_seq": i,
                "id": r["id"],
                "source_domain": r.get("source_domain"),
                "source_file": r.get("source_file"),
                "wave": r.get("wave"),
                "text": r["text"],
                "ai_label": r["gpt6_label"],
                "spans": r["spans"],
                "ai_status": r.get("status"),
                "ai_note": r.get("note"),
                "ai_issues": r.get("issues") or [],
                "ai_model": r.get("model"),
                "prompt_id": r.get("prompt_id"),
                "human_label": None,
                "human_status": "pending",
                "human_notes": "",
                "span_ops": {
                    "added": [],
                    "deleted": [],
                    "type_changed": [],
                    "boundary_changed": [],
                },
                "in_current_student_train": r["id"] in train_ids,
                "in_current_student_dev": r["id"] in dev_ids,
                "not_independent_blind_gold": True,
                "quality_check_of": "new_silver_only",
                "possible_future_test": True,
            }
        )
        id_rows.append({"qa_seq": i, "id": r["id"], "source_domain": r.get("source_domain")})

    OUT.mkdir(parents=True, exist_ok=True)
    dump_jsonl(PREP / "annotation_input/work.labeled.jsonl", pool)
    dump_jsonl(OUT / "qa150_ai_original.jsonl", ai_only)
    dump_jsonl(OUT / "qa150_human_task.jsonl", tasks)
    dump_jsonl(OUT / "qa150_ids.jsonl", id_rows)
    (OUT / "qa150_ids.txt").write_text("".join(t["id"] + "\n" for t in tasks), encoding="utf-8")

    overlap_train = [t["id"] for t in tasks if t["in_current_student_train"]]
    overlap_dev = [t["id"] for t in tasks if t["in_current_student_dev"]]
    manifest = {
        "n": N,
        "seed": SEED,
        "salt": SALT,
        "method": "stratified SRS: quota 阿里云60 / 事业单位45 / 上市公司45 (10k 40/30/30); inside domain sort by sha256(salt|seed|id), take quota. No replacement after this draw.",
        "old_unstratified_script": "scripts/sample_silver_plus_new150_qa.py",
        "executed_script": "scripts/sample_silver_new150_qa_20260914.py",
        "n_labeled_new": len(pool),
        "n_frame": len(frame),
        "dropped": dict(dropped),
        "quota": QUOTA,
        "drawn_domains": dict(Counter(t["source_domain"] for t in tasks)),
        "drawn_status": dict(Counter(t["ai_status"] for t in tasks)),
        "drawn_n_spans": sum(len(t["ai_label"] or []) for t in tasks),
        "drawn_empty": sum(1 for t in tasks if not (t["ai_label"] or [])),
        "gold150_overlap": 0,
        "do_not_replace_after_draw": True,
        "not_independent_blind_gold": True,
        "not_paper_main": True,
        "possible_future_test": True,
        "if_used_as_test_later": "Drop these 150 IDs from student train/dev and retrain. Do not swap the sample. This is still a quality check of new Silver, not a second Gold150.",
        "overlap_current_student_train_n": len(overlap_train),
        "overlap_current_student_dev_n": len(overlap_dev),
        "overlap_current_student_train_ids": overlap_train,
        "overlap_current_student_dev_ids": overlap_dev,
        "sha256_human_task": sha256_file(OUT / "qa150_human_task.jsonl"),
        "sha256_ai_original": sha256_file(OUT / "qa150_ai_original.jsonl"),
        "drawn_ids": [t["id"] for t in tasks],
        "do_not_write_paper_coverage_500_until_human_done": True,
    }
    dump_json(OUT / "SAMPLING_MANIFEST.json", manifest)
    status = {
        "status": "task_ready_human_check_pending",
        "n_requested": N,
        "drawn": N,
        "seed": SEED,
        "salt": SALT,
        "frame": "new AI-labeled silver 7936 only; not old 2451/v6a",
        "exclude": "Gold150 + A100 + QA100 (350) by id and NFC",
        "do_not_replace_after_draw": True,
        "not_independent_blind_gold": True,
        "possible_future_test": True,
        "quality_stats_scope": "new silver portion only, not the full 10,000",
        "script": "scripts/sample_silver_new150_qa_20260914.py",
        "sha256_human_task": manifest["sha256_human_task"],
    }
    dump_json(OUT / "STATUS.json", status)
    (OUT / "README.md").write_text(
        "\n".join(
            [
                "# 新增 Silver 人工质量检查 150",
                "",
                "抽中不换样。不是独立盲标 Gold，也不代表全部 10,000 条质量。",
                "不要把论文人工覆盖量改成 500，直到这 150 条人检完成。",
                "",
                "若这 150 条以后当作 test：从学生 train/dev 去掉这些 ID 后重训；不要另抽一套替换。",
                "当前 JobBERT 合并银标学生已经见过其中一部分（见 SAMPLING_MANIFEST overlap）。",
                "",
                f"- 任务：`qa150_human_task.jsonl`（human_label 现为 null）",
                f"- AI 原标：`qa150_ai_original.jsonl`",
                f"- 域配额：阿里云 60 / 事业单位 45 / 上市公司 45",
                f"- 与当前 student train 重叠：{len(overlap_train)}；dev 重叠：{len(overlap_dev)}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "n": N,
                "domains": manifest["drawn_domains"],
                "status": manifest["drawn_status"],
                "empty": manifest["drawn_empty"],
                "n_spans": manifest["drawn_n_spans"],
                "overlap_train": len(overlap_train),
                "overlap_dev": len(overlap_dev),
                "out": str(OUT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
