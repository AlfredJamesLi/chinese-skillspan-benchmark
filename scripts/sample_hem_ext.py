#!/usr/bin/env python3
"""Freeze H/E/M equal-n unique-text samples. Train labels only. Seed 20260908."""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/home/guojingli3/Chinese-Skillspan-Benchmark")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump(p: Path, rows: list[dict]) -> None:
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def length_bin(n: int) -> str:
    if n < 20:
        return "L0_20"
    if n < 50:
        return "L20_50"
    if n < 100:
        return "L50_100"
    if n < 200:
        return "L100_200"
    return "L200p"


def stratum(r: dict) -> tuple:
    empty = "empty" if not (r.get("spans") or []) else "span"
    return (r.get("cohort") or "NA", length_bin(len(r["sentence"])), empty)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--unique", default="", help="Optional slim unique file; prefer --train full records")
    ap.add_argument("--train", default="", help="Full B2 train jsonl; unique NFC keep first full record")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--sample_seed", type=int, default=20260908)
    args = ap.parse_args()
    if args.train:
        raw = load(Path(args.train))
        seen = set()
        rows = []
        for r in raw:
            import re, unicodedata

            k = re.sub(r"\s+", "", unicodedata.normalize("NFC", r.get("sentence") or ""))
            if k in seen:
                continue
            seen.add(k)
            if "tokens" not in r:
                r["tokens"] = list(r.get("sentence") or "")
            if "list_of_selection_bio4" not in r:
                n = len(r["tokens"])
                tags = ["O"] * n
                for a, b, t in r.get("spans") or []:
                    if 0 <= a < b <= n:
                        tags[a] = f"B-{t}"
                        for i in range(a + 1, b):
                            tags[i] = f"I-{t}"
                r["list_of_selection_bio4"] = tags
            rows.append(r)
    else:
        rows = load(Path(args.unique))
        for r in rows:
            if "tokens" not in r:
                r["tokens"] = list(r.get("sentence") or "")
            if "list_of_selection_bio4" not in r:
                n = len(r["tokens"])
                tags = ["O"] * n
                for a, b, t in r.get("spans") or []:
                    if 0 <= a < b <= n:
                        tags[a] = f"B-{t}"
                        for i in range(a + 1, b):
                            tags[i] = f"I-{t}"
                r["list_of_selection_bio4"] = tags
    by_id = {r["id"]: r for r in rows}
    a = [r for r in rows if r.get("cohort") == "A100"]
    h = [r for r in rows if r.get("cohort") == "H730"]
    e = [r for r in rows if r.get("cohort") == "E1621"]
    # A is a fixed base, never mixed as ordinary H/E
    a_ids = {r["id"] for r in a}
    h = [r for r in h if r["id"] not in a_ids]
    e = [r for r in e if r["id"] not in a_ids]

    def key_he(r):
        return (length_bin(len(r["sentence"])), "empty" if not r.get("spans") else "span")

    h_by = defaultdict(list)
    e_by = defaultdict(list)
    for r in h:
        h_by[key_he(r)].append(r["id"])
    for r in e:
        e_by[key_he(r)].append(r["id"])
    keys = sorted(set(h_by) | set(e_by))
    supported = []
    unmatched = []
    for k in keys:
        nh, ne = len(h_by[k]), len(e_by[k])
        cap = min(nh, ne)
        if cap <= 0:
            unmatched.append({"stratum": list(k), "n_H": nh, "n_E": ne, "reason": "no_common_support"})
        else:
            supported.append({"stratum": list(k), "n_H": nh, "n_E": ne, "cap": cap})
    n_cap = sum(s["cap"] for s in supported)
    n = n_cap - (n_cap % 2)
    if n <= 0:
        raise SystemExit("no even n supported")

    rng = random.Random(args.sample_seed)
    h_pick, e_pick = [], []
    remain = n
    # allocate floor per stratum proportional to cap, then fill leftover by remaining cap
    caps = [s["cap"] for s in supported]
    raw = [remain * c / n_cap for c in caps]
    take = [int(x) for x in raw]
    leftover = remain - sum(take)
    order = sorted(range(len(supported)), key=lambda i: -(caps[i] - take[i]))
    for i in order:
        if leftover <= 0:
            break
        room = caps[i] - take[i]
        add = min(room, leftover)
        take[i] += add
        leftover -= add
    # if still odd per condition after integer, already even n
    for s, t in zip(supported, take):
        k = tuple(s["stratum"])
        hid = h_by[k][:]
        eid = e_by[k][:]
        rng.shuffle(hid)
        rng.shuffle(eid)
        h_pick.extend(hid[:t])
        e_pick.extend(eid[:t])
        s["sampled"] = t
    assert len(h_pick) == n and len(e_pick) == n
    half = n // 2
    # M: n/2 H + n/2 E from the already frozen H/E pools (same IDs, subset)
    rng_m = random.Random(args.sample_seed + 1)
    h_m = h_pick[:]
    e_m = e_pick[:]
    rng_m.shuffle(h_m)
    rng_m.shuffle(e_m)
    m_h, m_e = h_m[:half], e_m[:half]

    def pack(ids):
        return [by_id[i] for i in ids]

    a_rows = pack(sorted(a_ids))
    h_rows = a_rows + pack(h_pick)
    e_rows = a_rows + pack(e_pick)
    m_rows = a_rows + pack(m_h + m_e)
    assert len(h_rows) == len(e_rows) == len(m_rows) == len(a_rows) + n

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    dump(out / f"train_B2_A{len(a_rows)}_H_{n}.jsonl", h_rows)
    dump(out / f"train_B2_A{len(a_rows)}_E_{n}.jsonl", e_rows)
    dump(out / f"train_B2_A{len(a_rows)}_M_{n}.jsonl", m_rows)
    names = {"H": f"H_{n}", "E": f"E_{n}", "M": f"M_{n}", "A_base": f"A_{len(a_rows)}"}
    manifest = {
        "sample_seed": args.sample_seed,
        "unique_pool": args.train or args.unique,
        "n_unique_pool": len(rows),
        "n_A_unique": len(a_rows),
        "n_H_available": len(h),
        "n_E_available": len(e),
        "n": n,
        "names": names,
        "A_ids": sorted(a_ids),
        "H_ids": h_pick,
        "E_ids": e_pick,
        "M_H_ids": m_h,
        "M_E_ids": m_e,
        "train_sizes": {"H": len(h_rows), "E": len(e_rows), "M": len(m_rows)},
        "supported_strata": supported,
        "unmatched_strata": unmatched,
        "conclusion_scope": "equal-n historical-conflict vs non-conflict source; H/E are not objective difficulty truth",
        "sampling_uncertainty_not_estimated": True,
        "gold_not_used": True,
        "dev_not_used": True,
    }
    (out / "HEM_SAMPLING_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "HEM_CONFIG.json").write_text(
        json.dumps(
            {
                "student": "jobbert3m_dapt_encoder_reinit_crf",
                "labels": "B2",
                "n": n,
                "A_base": len(a_rows),
                "conditions": [names["H"], names["E"], names["M"]],
                "model_seeds": [42, 43, 44],
                "sample_seed": args.sample_seed,
                "shared_dev": "v6a_nocross dev_b2 169",
                "init": "random_task_head_crf",
                "n_trains": 9,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    md = [
        "# HEM 等量抽样报告",
        "",
        f"- 独特文本池：{len(rows)}（仅最终训练池，无开发/Gold）",
        f"- A100 固定底座：{len(a_rows)} 条独特文本（不混作普通 H/E）",
        f"- 可支持 H/E：{len(h)} / {len(e)}",
        f"- 共同分层可支持容量 {n_cap}，取偶数 **n={n}**",
        f"- 条件：`{names['H']}` = A+{n}H；`{names['E']}` = A+{n}E；`{names['M']}` = A+{n//2}H+{n//2}E",
        f"- 各条件训练条数相同：{len(h_rows)}",
        f"- 无法匹配的层：{len(unmatched)}（不强行凑 n，不从开发补样本）",
        "- 结论范围：历史冲突来源与非冲突来源的等量比较；H/E 不是客观难度真值",
        "- 一次抽样 × 三模型种子不估计抽样不确定性",
        "",
    ]
    if unmatched:
        md.append("## 无共同支持的层")
        for u in unmatched:
            md.append(f"- {u}")
    (out / "HEM_BALANCE_REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"n": n, "A": len(a_rows), "train_size": len(h_rows), "unmatched": len(unmatched)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
