#!/usr/bin/env python3
"""Source-stratified post-level split (repartition_v1).

Does not overwrite Gold v2, v4 silver, hybrid gold, old splits, or checkpoints.
Does not use model F1. Official seeds only: 42, 123, 2026, 7, 13.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
CORPUS = ROOT / "data/annotated/processed/chinese_skillspan"
OUT = PAPER / "reports/repartition_v1"
MAN = PAPER / "manifests/repartition_v1"
DATA_OUT = PAPER / "data/repartition_v1"

SOURCE_MAP = {
    "人工智能招聘": "AI",
    "应届生招聘": "Grad",
    "阿里云公开数据集": "Cloud",
    "事业单位招聘": "Public",
}
SEEDS = [42, 123, 2026, 7, 13]
WEIGHTS = {
    "js_label_train_test": 2.0,
    "js_label_train_dev": 1.0,
    "abs_empty_train_test": 1.0,
    "abs_len_train_test": 0.5,
    "missing_L_in_split": 3.0,
    "missing_source_in_split": 100.0,
    "post_quota_l1": 1.0,
}
FIXED_QUOTA = {
    "Public": {"train": 12, "dev": 4, "test": 4},
    "Cloud": {"train": 28, "dev": 4, "test": 8},
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rec_id(rec: dict) -> str:
    return str(rec.get("id") or "").strip()


def post_id(rec: dict) -> str:
    g = rec.get("global_id")
    if g is None or str(g).strip() == "":
        rid = rec_id(rec)
        return rid.split("-s")[0] if "-s" in rid else rid
    return str(g).strip()


def load_json_or_jsonl(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(l) for l in raw.splitlines() if l.strip()]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def bio_spans(tags: list[str]) -> list[tuple[int, int, str]]:
    out = []
    i, n = 0, len(tags)
    while i < n:
        t = str(tags[i] or "O")
        if t.startswith("B-"):
            typ = t[2:]
            j = i + 1
            while j < n and str(tags[j] or "O") == f"I-{typ}":
                j += 1
            out.append((i, j, typ))
            i = j
        else:
            i += 1
    return out


def count_types(tags: list[str]) -> dict[str, int]:
    c = {"L": 0, "K": 0, "S": 0, "T": 0}
    for _, _, typ in bio_spans(tags):
        if typ in c:
            c[typ] += 1
    return c


def tags_of(rec: dict) -> list[str]:
    return [str(t or "O") for t in (rec.get("list_of_selection_bio4") or [])]


def norm_text(s: str) -> str:
    s = (s or "").replace("\u3000", " ")
    s = re.sub(r"\s+", "", s)
    return s.casefold()


def src_code(rec: dict) -> str:
    return SOURCE_MAP.get(str(rec.get("source_domain") or "").strip(), "UNK")


class UF:
    def __init__(self):
        self.p: dict[str, str] = {}

    def add(self, x: str) -> None:
        self.p.setdefault(x, x)

    def find(self, x: str) -> str:
        self.add(x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def js_div(p: dict[str, float], q: dict[str, float]) -> float:
    keys = set(p) | set(q)
    def _h(d):
        s = 0.0
        for k in keys:
            v = d.get(k, 0.0)
            if v > 0:
                s -= v * math.log(v, 2)
        return s
    m = {k: 0.5 * (p.get(k, 0.0) + q.get(k, 0.0)) for k in keys}
    return _h(m) - 0.5 * _h(p) - 0.5 * _h(q)


def label_dist(rows: list[dict]) -> dict[str, float]:
    c = Counter()
    for r in rows:
        for k, n in r["type_counts"].items():
            c[k] += n
    tot = sum(c.values()) or 1
    return {k: c[k] / tot for k in "LKST"}


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    MAN.mkdir(parents=True, exist_ok=True)
    DATA_OUT.mkdir(parents=True, exist_ok=True)

    train_s = load_jsonl(PAPER / "data/train_lskt_v4_silver.jsonl")
    dev_s = load_jsonl(PAPER / "data/dev_lskt_v4_silver.jsonl")
    test_s = load_jsonl(PAPER / "data/test_lskt_v4_silver.jsonl")
    gold_v2 = load_jsonl(PAPER / "data/gold_canonical_v2.jsonl")
    hybrid = load_jsonl(PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl")
    sim980 = load_jsonl(PAPER / "data/test_lskt_v4_simhuman980_cws.jsonl")
    corpus_test = load_json_or_jsonl(CORPUS / "test.json")
    try:
        pilot300 = load_jsonl(PAPER / "data/gold_eval_v3_pilot300.jsonl")
    except Exception:
        pilot300 = []

    by_split = {"train": train_s, "dev": dev_s, "test": test_s}
    pool: dict[str, dict] = {}
    for sp, rows in by_split.items():
        for rec in rows:
            rid = rec_id(rec)
            pool[rid] = rec
            rec["_current_split"] = sp

    gold_ids = {rec_id(r) for r in gold_v2}
    hybrid_ids = {rec_id(r) for r in hybrid}
    sim_ids = {rec_id(r) for r in sim980}
    hybrid_src = {rec_id(r): r.get("hybrid_source") for r in hybrid}
    corpus_test_ids = {rec_id(r) for r in corpus_test}
    corpus_test_map = {rec_id(r): r for r in corpus_test}
    pilot_ids = {rec_id(r) for r in pilot300}

    test_ids = {rec_id(r) for r in test_s}
    missing_636_ids = sorted(test_ids - gold_ids)

    inv_fields = [
        "sentence_id", "post_id", "near_duplicate_group_id", "source", "current_split",
        "text_hash", "normalized_text_hash", "sentence_length_chars", "sentence_length_tokens",
        "n_L", "n_K", "n_S", "n_T", "n_total_spans", "is_empty", "annotation_protocol",
        "annotation_provenance", "human_verification_status", "eligible_for_repartition",
        "exclusion_reason", "offset_ok", "substring_ok",
    ]
    inventory = []
    conflicts = []
    id_seen: dict[str, str] = {}
    missing_rows = []

    for rec in [*train_s, *dev_s, *test_s]:
        rid = rec_id(rec)
        pid = post_id(rec)
        toks = [str(t) for t in (rec.get("tokens") or list(rec.get("sentence") or ""))]
        tags = tags_of(rec)
        if len(tags) < len(toks):
            tags = tags + ["O"] * (len(toks) - len(tags))
        tags = tags[: len(toks)]
        tc = count_types(tags)
        sent = rec.get("sentence") or ""
        nth = hashlib.sha256(norm_text(sent).encode()).hexdigest()
        th = hashlib.sha256(sent.encode("utf-8")).hexdigest()
        offset_ok = len(tags) == len(toks)
        sub_ok = True
        if offset_ok:
            for a, b, _ in bio_spans(tags):
                frag = "".join(toks[a:b])
                if frag not in sent and frag != "".join(list(sent)[a:b] if False else toks[a:b]):
                    # token concat must match a contiguous source substring when tokens are chars
                    if frag not in sent:
                        sub_ok = False
                        break
        src = src_code(rec)
        protocol = str(rec.get("v4_source") or "lskt_v4_silver")
        in_gold = rid in gold_ids
        in_hyb = rid in hybrid_ids
        hs = hybrid_src.get(rid)
        if rid in sim_ids or hs in {"simhuman980_cws", "simhuman980"}:
            human_st = "simhuman_rule_v4_overlay_not_dual_blind"
        elif rid in pilot_ids:
            human_st = "eval_v3_pilot300_not_v4_iaa"
        elif in_gold:
            human_st = "gold_v2_doccano_not_v4_audit"
        else:
            human_st = "not_human_reviewed"
        if in_hyb and hs:
            prov = f"v4_silver+hybrid:{hs}"
        elif rec["_current_split"] in {"train", "dev"}:
            prov = "v4_silver_draft"
        else:
            prov = "v4_silver_test_draft"
        excl = ""
        eligible = True
        if not rid:
            eligible, excl = False, "missing_sentence_id"
        elif not pid:
            eligible, excl = False, "missing_post_id"
        elif src == "UNK":
            eligible, excl = False, "unknown_source"
        elif not offset_ok:
            eligible, excl = False, "tag_token_length_mismatch"
        if rid in id_seen:
            conflicts.append({"kind": "duplicate_sentence_id", "id": rid, "a": id_seen[rid], "b": rec["_current_split"]})
        else:
            id_seen[rid] = rec["_current_split"]
        row = {
            "sentence_id": rid,
            "post_id": pid,
            "source": src,
            "current_split": rec["_current_split"],
            "text_hash": th,
            "normalized_text_hash": nth,
            "sentence_length_chars": len(sent),
            "sentence_length_tokens": len(toks),
            "n_L": tc["L"], "n_K": tc["K"], "n_S": tc["S"], "n_T": tc["T"],
            "n_total_spans": sum(tc.values()),
            "is_empty": int(sum(tc.values()) == 0),
            "annotation_protocol": protocol,
            "annotation_provenance": prov,
            "human_verification_status": human_st,
            "eligible_for_repartition": int(eligible),
            "exclusion_reason": excl,
            "offset_ok": int(offset_ok),
            "substring_ok": int(sub_ok),
            "type_counts": tc,
            "sentence": sent,
            "tokens": toks,
            "tags": tags,
            "title": rec.get("title") or "",
            "source_domain": rec.get("source_domain"),
            "rec": rec,
        }
        inventory.append(row)
        if rid in missing_636_ids:
            ct = corpus_test_map.get(rid, {})
            ct_tags = tags_of(ct) if ct else []
            missing_rows.append({
                "sentence_id": rid,
                "post_id": pid,
                "source": src,
                "in_processed_test_3237": int(rid in corpus_test_ids),
                "in_test_v4_silver": 1,
                "in_gold_v2": 0,
                "in_v4_hybrid_2601": int(rid in hybrid_ids),
                "in_simhuman980": int(rid in sim_ids),
                "has_v4_labels": int(sum(tc.values()) >= 0),
                "n_spans": sum(tc.values()),
                "annotation_protocol": protocol,
                "human_verification_status": human_st,
                "processed_test_has_bio4": int(any(str(t).upper().startswith("B") for t in ct_tags)),
                "eligible_for_repartition": int(eligible),
                "exclusion_reason": excl or ("ok_v4_silver_not_in_unique_gold_v2"),
                "title": rec.get("title") or "",
            })

    write_csv(OUT / "candidate_pool_inventory.csv", inventory, inv_fields)
    m636_fields = [
        "sentence_id", "post_id", "source", "in_processed_test_3237", "in_test_v4_silver",
        "in_gold_v2", "in_v4_hybrid_2601", "in_simhuman980", "has_v4_labels", "n_spans",
        "annotation_protocol", "human_verification_status", "processed_test_has_bio4",
        "eligible_for_repartition", "exclusion_reason", "title",
    ]
    write_csv(OUT / "missing_636_audit.csv", missing_rows, m636_fields)

    n_pool = len(inventory)
    n_el = sum(r["eligible_for_repartition"] for r in inventory)
    src_636 = Counter(r["source"] for r in missing_rows)
    (OUT / "missing_636_summary.md").write_text(
        "\n".join([
            "# 636-record audit (processed test 3237 − Gold v2 / V4 hybrid 2601)",
            "",
            f"Processed test.json: {len(corpus_test_ids)}",
            f"test_lskt_v4_silver.jsonl: {len(test_s)}",
            f"gold_canonical_v2.jsonl unique IDs: {len(gold_ids)}",
            f"V4 hybrid 2601: {len(hybrid_ids)}",
            f"IDs in test silver not in Gold v2: {len(missing_636_ids)}",
            f"IDs in that set also in processed test: {sum(r['in_processed_test_3237'] for r in missing_rows)}",
            f"IDs in that set also in V4 hybrid: {sum(r['in_v4_hybrid_2601'] for r in missing_rows)}",
            "",
            "Arithmetic: 17460 train + 2143 dev + 2601 eval = 22204; claimed 22840; 22840−22204=636.",
            "22840 = 17460+2143+3237 (full processed corpus). 3237−2601=636.",
            "These 636 are processed-test sentences excluded from unique-first Gold v2 / V4 hybrid.",
            "They still have LSKT v4 silver (rule_v4) labels. They are **not** human Gold.",
            "Do not auto-generate Gold to fill them.",
            "",
            "By source: " + ", ".join(f"{k}={v}" for k, v in sorted(src_636.items())),
            f"Empty (0 spans): {sum(r['n_spans']==0 for r in missing_rows)}",
            f"Eligible for new stratified pool: {sum(r['eligible_for_repartition'] for r in missing_rows)}",
            "",
            "980 SimHuman: overlay rule_v4, not dual-blind IAA. File "
            f"`test_lskt_v4_simhuman980_cws.jsonl` n={len(sim_ids)}. "
            f"eval_v3 pilot300 n={len(pilot_ids)} is a separate Gold-era pilot, not V4 IAA.",
            "",
        ]),
        encoding="utf-8",
    )

    # Near-dup groups: exact normalized sentence shared across posts; same title+source.
    uf = UF()
    posts_meta: dict[str, dict] = {}
    hash_posts: dict[str, set[str]] = defaultdict(set)
    title_posts: dict[tuple[str, str], set[str]] = defaultdict(set)
    for r in inventory:
        pid = r["post_id"]
        uf.add(pid)
        posts_meta.setdefault(pid, {"source": r["source"], "title": r["title"], "sents": []})
        posts_meta[pid]["sents"].append(r["sentence_id"])
        if len(norm_text(r["sentence"])) >= 12:
            hash_posts[r["normalized_text_hash"]].add(pid)
        if r["title"]:
            title_posts[(r["source"], r["title"])].add(pid)
    for ps in hash_posts.values():
        ps = list(ps)
        for x in ps[1:]:
            uf.union(ps[0], x)
    for ps in title_posts.values():
        if len(ps) > 1:
            ps = list(ps)
            for x in ps[1:]:
                uf.union(ps[0], x)
    for r in inventory:
        r["near_duplicate_group_id"] = uf.find(r["post_id"])

    write_csv(OUT / "candidate_pool_inventory.csv", inventory, inv_fields)

    # Leakage on OLD split
    old_post_split: dict[str, set[str]] = defaultdict(set)
    old_hash_split: dict[str, set[str]] = defaultdict(set)
    for r in inventory:
        old_post_split[r["post_id"]].add(r["current_split"])
        old_hash_split[r["normalized_text_hash"]].add(r["current_split"])
    leak_posts = {p: s for p, s in old_post_split.items() if len(s) > 1}
    leak_text = {h: s for h, s in old_hash_split.items() if len(s) > 1}
    miss_pid = [r for r in inventory if not r["post_id"]]
    if miss_pid:
        (OUT / "STOP.txt").write_text("Cannot recover post_id; split aborted.\n", encoding="utf-8")
        return 2

    leak_md = [
        "# Pre-split leakage and quality (current source-disjoint split)",
        "",
        f"Pool sentences: {n_pool} (train {len(train_s)} + dev {len(dev_s)} + test silver {len(test_s)})",
        f"Eligible: {n_el}",
        f"Unique posts: {len(posts_meta)}",
        f"Near-dup groups after union: {len({uf.find(p) for p in posts_meta})}",
        f"Duplicate sentence IDs: {len(conflicts)}",
        f"Posts spanning multiple current splits: {len(leak_posts)}",
        f"Normalized-text hashes spanning multiple current splits: {len(leak_text)}",
        f"Offset mismatches: {sum(r['offset_ok']==0 for r in inventory)}",
        f"Substring failures: {sum(r['substring_ok']==0 for r in inventory)}",
        f"Empty-sentence rate: {sum(r['is_empty'] for r in inventory)/max(n_pool,1):.4f}",
        "",
        "## Human vs draft (not assumed from chat)",
        f"- SimHuman 980 file n={len(sim_ids)}; hybrid_source counts: "
        + json.dumps(dict(Counter(hybrid_src.values())), ensure_ascii=False),
        f"- Gold v2 n={len(gold_ids)} (Doccano; not V4 IAA)",
        f"- eval_v3 pilot300 n={len(pilot_ids)} (Gold-era; not V4 dual-blind)",
        "- 980 is **not** a completed dual-blind V4 human audit.",
        "",
        "## Current source × split (sentences)",
    ]
    grid = Counter((r["source"], r["current_split"]) for r in inventory)
    for src in ("AI", "Grad", "Cloud", "Public"):
        leak_md.append(
            f"- {src}: train={grid[(src,'train')]} dev={grid[(src,'dev')]} test={grid[(src,'test')]}"
        )
    (OUT / "pre_split_leakage_audit.md").write_text("\n".join(leak_md) + "\n", encoding="utf-8")
    leak_rows = (
        [{"kind": "old_post_cross_split", "key": p, "splits": "|".join(sorted(s))} for p, s in leak_posts.items()]
        + [{"kind": "old_normtext_cross_split", "key": h[:16], "splits": "|".join(sorted(s))} for h, s in list(leak_text.items())[:500]]
        + conflicts
    )
    write_csv(OUT / "pre_split_conflicts.csv", leak_rows, ["kind", "key", "splits", "id", "a", "b"])

    # --- Phase B ---
    by_id = {r["sentence_id"]: r for r in inventory}
    groups: dict[str, list[str]] = defaultdict(list)
    for pid in posts_meta:
        groups[uf.find(pid)].append(pid)
    group_src = {g: posts_meta[ps[0]]["source"] for g, ps in groups.items()}
    # If a group mixes sources, mark conflict
    mixed = []
    for g, ps in groups.items():
        ss = {posts_meta[p]["source"] for p in ps}
        if len(ss) > 1:
            mixed.append((g, ss))
            group_src[g] = sorted(ss)[0]
    src_groups: dict[str, list[str]] = defaultdict(list)
    for g, src in group_src.items():
        src_groups[src].append(g)

    def n_posts_src(src: str) -> int:
        return sum(1 for p, m in posts_meta.items() if m["source"] == src)

    def quota_for(src: str) -> dict[str, int]:
        if src in FIXED_QUOTA:
            return dict(FIXED_QUOTA[src])
        n = n_posts_src(src)
        n_test = int(round(0.20 * n))
        n_dev = int(round(0.10 * n))
        n_train = n - n_dev - n_test
        return {"train": n_train, "dev": n_dev, "test": n_test}

    def assign(seed: int) -> dict[str, str]:
        rng = random.Random(seed)
        post_to_split: dict[str, str] = {}
        for src, gl in src_groups.items():
            q = quota_for(src)
            order = list(gl)
            rng.shuffle(order)
            counts = {"train": 0, "dev": 0, "test": 0}
            # Fill test, then dev, then train (group-atomic).
            buckets = ["test", "dev", "train"]
            for g in order:
                ps = groups[g]
                need = None
                for b in buckets:
                    if counts[b] < q[b]:
                        need = b
                        break
                if need is None:
                    need = "train"
                for p in ps:
                    post_to_split[p] = need
                counts[need] += len(ps)
        return post_to_split

    def repair_text_leak(post_to_split: dict[str, str]) -> dict[str, str]:
        """Move whole near-dup groups so normalized sentences (len>=12) stay in one split.
        Tie-break: train. Never uses model F1."""
        by_pid_sents: dict[str, list[dict]] = defaultdict(list)
        for r in inventory:
            by_pid_sents[r["post_id"]].append(r)
        changed = True
        guard = 0
        while changed and guard < 20:
            guard += 1
            changed = False
            hsp: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
            for pid, sp in post_to_split.items():
                for r in by_pid_sents[pid]:
                    if r["sentence_length_chars"] >= 12:
                        hsp[r["normalized_text_hash"]][sp].add(pid)
            for _h, spmap in hsp.items():
                if len(spmap) <= 1:
                    continue
                # majority split, tie -> train
                majority = max(spmap.items(), key=lambda kv: (len(kv[1]), kv[0] == "train"))[0]
                if len(spmap[majority]) == max(len(v) for v in spmap.values()):
                    # if several max, prefer train
                    cands = [s for s, v in spmap.items() if len(v) == max(len(x) for x in spmap.values())]
                    majority = "train" if "train" in cands else sorted(cands)[0]
                pids = set().union(*spmap.values())
                for pid in pids:
                    g = uf.find(pid)
                    for p in groups[g]:
                        if post_to_split.get(p) != majority:
                            post_to_split[p] = majority
                            changed = True
        return post_to_split

    def split_rows(post_to_split: dict[str, str]) -> dict[str, list[dict]]:
        out = {"train": [], "dev": [], "test": []}
        for r in inventory:
            if not r["eligible_for_repartition"]:
                continue
            out[post_to_split[r["post_id"]]].append(r)
        return out

    def hard_ok(post_to_split: dict[str, str], parts: dict[str, list[dict]]) -> tuple[bool, list[str]]:
        fails = []
        # post across splits
        inv = defaultdict(set)
        for p, sp in post_to_split.items():
            inv[p].add(sp)
        if any(len(s) > 1 for s in inv.values()):
            fails.append("post_id_cross_split")
        # group
        gsp = defaultdict(set)
        for p, sp in post_to_split.items():
            gsp[uf.find(p)].add(sp)
        if any(len(s) > 1 for s in gsp.values()):
            fails.append("near_dup_group_cross_split")
        # sentence id
        ids = [r["sentence_id"] for sp in parts.values() for r in sp]
        if len(ids) != len(set(ids)):
            fails.append("duplicate_sentence_id")
        # norm text leakage across splits
        hsp = defaultdict(set)
        for sp, rows in parts.items():
            for r in rows:
                if r["sentence_length_chars"] >= 12:
                    hsp[r["normalized_text_hash"]].add(sp)
        if any(len(s) > 1 for s in hsp.values()):
            fails.append("normalized_text_leakage")
        for src in ("AI", "Grad", "Cloud", "Public"):
            for sp in ("train", "dev", "test"):
                if not any(r["source"] == src for r in parts[sp]):
                    fails.append(f"missing_{src}_in_{sp}")
        if any(r["offset_ok"] == 0 for rows in parts.values() for r in rows):
            fails.append("invalid_offsets")
        return (len(fails) == 0, fails)

    def cost(parts: dict[str, list[dict]], post_to_split: dict[str, str]) -> tuple[float, dict]:
        det = {}
        dtr, dte, ddv = label_dist(parts["train"]), label_dist(parts["test"]), label_dist(parts["dev"])
        det["js_label_train_test"] = js_div(dtr, dte)
        det["js_label_train_dev"] = js_div(dtr, ddv)
        e_tr = sum(r["is_empty"] for r in parts["train"]) / max(len(parts["train"]), 1)
        e_te = sum(r["is_empty"] for r in parts["test"]) / max(len(parts["test"]), 1)
        det["abs_empty_train_test"] = abs(e_tr - e_te)
        l_tr = sum(r["sentence_length_tokens"] for r in parts["train"]) / max(len(parts["train"]), 1)
        l_te = sum(r["sentence_length_tokens"] for r in parts["test"]) / max(len(parts["test"]), 1)
        det["abs_len_train_test"] = abs(l_tr - l_te) / 50.0
        miss_l = 0
        for sp, rows in parts.items():
            if sum(r["n_L"] for r in rows) == 0:
                miss_l += 1
        det["missing_L_in_split"] = miss_l
        miss_src = 0
        for src in ("AI", "Grad", "Cloud", "Public"):
            for sp in ("train", "dev", "test"):
                if not any(r["source"] == src for r in parts[sp]):
                    miss_src += 1
        det["missing_source_in_split"] = miss_src
        l1 = 0
        for src in ("AI", "Grad", "Cloud", "Public"):
            q = quota_for(src)
            got = Counter()
            for p, sp in post_to_split.items():
                if posts_meta[p]["source"] == src:
                    got[sp] += 1
            for sp in ("train", "dev", "test"):
                l1 += abs(got[sp] - q[sp])
        det["post_quota_l1"] = l1 / 100.0
        total = sum(WEIGHTS[k] * det[k] for k in WEIGHTS)
        return total, det

    ranking = []
    best = None
    for seed in SEEDS:
        pmap = assign(seed)
        pmap = repair_text_leak(pmap)
        parts = split_rows(pmap)
        ok, fails = hard_ok(pmap, parts)
        sc, det = cost(parts, pmap)
        row = {
            "seed": seed,
            "hard_ok": int(ok),
            "hard_fails": ";".join(fails),
            "cost": round(sc, 6),
            **{k: round(v, 6) for k, v in det.items()},
            "n_train": len(parts["train"]),
            "n_dev": len(parts["dev"]),
            "n_test": len(parts["test"]),
        }
        for src in ("AI", "Grad", "Cloud", "Public"):
            for sp in ("train", "dev", "test"):
                row[f"posts_{src}_{sp}"] = sum(
                    1 for p, s in pmap.items() if posts_meta[p]["source"] == src and s == sp
                )
                row[f"sents_{src}_{sp}"] = sum(1 for r in parts[sp] if r["source"] == src)
        ranking.append(row)
        if ok and (best is None or sc < best[0]):
            best = (sc, seed, pmap, parts, det, fails)

    write_csv(
        OUT / "candidate_split_ranking.csv",
        ranking,
        list(ranking[0].keys()) if ranking else ["seed"],
    )
    cmp_lines = [
        "# Candidate split ranking",
        "",
        "Seeds are the project encoder set (42, 123, 2026, 7, 13). Cost uses only distributional stats.",
        "**No model F1 entered the objective.**",
        "",
        "| seed | hard_ok | cost | n_train | n_dev | n_test | fails |",
        "|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in ranking:
        cmp_lines.append(
            f"| {r['seed']} | {r['hard_ok']} | {r['cost']} | {r['n_train']} | {r['n_dev']} | {r['n_test']} | {r['hard_fails']} |"
        )
    (OUT / "candidate_split_comparison.md").write_text("\n".join(cmp_lines) + "\n", encoding="utf-8")

    if best is None:
        (OUT / "frozen_split_decision.md").write_text(
            "No candidate satisfied hard constraints. Training is blocked.\n" + json.dumps(ranking, indent=2),
            encoding="utf-8",
        )
        return 3

    _, seed, pmap, parts, det, _fails = best

    # Write manifests (new files only)
    def dump_split(name: str, rows: list[dict]) -> Path:
        path = DATA_OUT / f"{name}.jsonl"
        man = MAN / f"{name}_manifest.jsonl"
        with path.open("w", encoding="utf-8") as f, man.open("w", encoding="utf-8") as m:
            for r in rows:
                rec = {
                    "id": r["sentence_id"],
                    "global_id": r["post_id"],
                    "sentence": r["sentence"],
                    "tokens": r["tokens"],
                    "list_of_selection_bio4": r["tags"],
                    "source_domain": r["source_domain"],
                    "title": r["title"],
                    "near_duplicate_group_id": r["near_duplicate_group_id"],
                    "repartition_split": name,
                    "annotation_protocol": "lskt_v4_character",
                    "annotation_provenance": r["annotation_provenance"],
                    "human_verification_status": r["human_verification_status"],
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                m.write(json.dumps({
                    "sentence_id": r["sentence_id"],
                    "post_id": r["post_id"],
                    "near_duplicate_group_id": r["near_duplicate_group_id"],
                    "source": r["source"],
                    "split": name,
                }, ensure_ascii=False) + "\n")
        return path

    paths = {sp: dump_split(sp, parts[sp]) for sp in ("train", "dev", "test")}
    all_man = MAN / "split_manifest_all.jsonl"
    with all_man.open("w", encoding="utf-8") as f:
        for sp, rows in parts.items():
            for r in rows:
                f.write(json.dumps({
                    "sentence_id": r["sentence_id"],
                    "post_id": r["post_id"],
                    "near_duplicate_group_id": r["near_duplicate_group_id"],
                    "source": r["source"],
                    "split": sp,
                    "old_split": r["current_split"],
                }, ensure_ascii=False) + "\n")

    sums = MAN / "SHA256SUMS"
    with sums.open("w", encoding="utf-8") as f:
        for p in [
            paths["train"], paths["dev"], paths["test"],
            MAN / "train_manifest.jsonl", MAN / "dev_manifest.jsonl", MAN / "test_manifest.jsonl",
            all_man,
            PAPER / "configs/repartition_v1.yaml",
        ]:
            f.write(f"{sha256_file(p)}  {p.name}\n")

    stat_rows = []
    for sp, rows in parts.items():
        tc = Counter()
        for r in rows:
            for k, n in r["type_counts"].items():
                tc[k] += n
        rec = {
            "split": sp,
            "n_sentences": len(rows),
            "n_posts": len({r["post_id"] for r in rows}),
            "n_L": tc["L"], "n_K": tc["K"], "n_S": tc["S"], "n_T": tc["T"],
            "empty_rate": round(sum(r["is_empty"] for r in rows) / max(len(rows), 1), 4),
            "mean_tokens": round(sum(r["sentence_length_tokens"] for r in rows) / max(len(rows), 1), 2),
        }
        for src in ("AI", "Grad", "Cloud", "Public"):
            rec[f"sents_{src}"] = sum(1 for r in rows if r["source"] == src)
            rec[f"posts_{src}"] = len({r["post_id"] for r in rows if r["source"] == src})
        stat_rows.append(rec)
    write_csv(OUT / "frozen_split_statistics.csv", stat_rows, list(stat_rows[0].keys()))

    n636_in = Counter()
    miss_set = set(missing_636_ids)
    for sp, rows in parts.items():
        n636_in[sp] += sum(1 for r in rows if r["sentence_id"] in miss_set)

    decision = f"""# Frozen split decision (repartition_v1)

Chosen candidate seed: **{seed}** (official encoder seed set; not invented).
Objective cost: {best[0]:.6f}. Details: {json.dumps(det)}.

## Why this split
Among seeds {SEEDS}, this is the lowest-cost candidate that passed every hard constraint.
Ranking used only source/post quotas, L/K/S/T mix, empty rate, and length. **No JobBERT, RoBERTa, Qwen, or LLM F1 was computed or used.**

## Remaining imbalance
Public has 20 posts (quota 12/4/4) and very few L spans historically (33 on old V4 test, 1 in Public). Some splits may still have sparse L.
Cloud has 40 posts (quota 28/4/8). Near-duplicate grouping can move extra posts with a group.

## Label provenance (not human Gold)
Train/dev/test all use **LSKT v4 character BIO** from `train/dev/test_lskt_v4_silver.jsonl` (rule_v4 / Codex sample drafts).
- SimHuman 980 overlay is **not** treated as completed dual-blind human SOP.
- Gold v2 remains frozen appendix provenance; it is **not** overwritten and is **not** the new test gold.
- New test is mixed-provenance v4 silver, including Grad (previously train-only drafts).

## 636 records
They are the processed-test sentences absent from unique-first Gold v2 / V4 hybrid (3237−2601).
They retain v4 silver labels and **were eligible**. Placement after freeze: train={n636_in['train']} dev={n636_in['dev']} test={n636_in['test']}.

## Old source-disjoint benchmark
Unchanged: `gold_canonical_v2.jsonl`, `test_lskt_v4_cws_simhuman980_hybrid.jsonl`, old train/dev silver, encoder dirs, dumps.
Future paper role: **appendix cross-source transfer diagnostic**.

## SHA256
See `manifests/repartition_v1/SHA256SUMS`.
"""
    (OUT / "frozen_split_decision.md").write_text(decision, encoding="utf-8")

    artifact = [
        "# Artifact path list (repartition_v1)",
        "",
        "| artifact | path | rows | unique IDs | source coverage | annotation provenance | current role | proposed role | action |",
        "|---|---|---:|---:|---|---|---|---|---|",
        f"| corpus train | `{CORPUS}/train.json` | {len(train_s)} | {len(train_s)} | AI+Grad | v4 silver | old train | keep | do not overwrite |",
        f"| corpus dev | `{CORPUS}/dev.json` | {len(dev_s)} | {len(dev_s)} | AI | v4 silver | old dev | keep | do not overwrite |",
        f"| corpus test | `{CORPUS}/test.json` | {len(corpus_test)} | {len(corpus_test)} | AI+Cloud+Public | mixed | processed test 3237 | keep | do not overwrite |",
        f"| Gold v2 | `data/gold_canonical_v2.jsonl` | {len(gold_v2)} | {len(gold_ids)} | AI+Cloud+Public | Doccano | appendix | appendix | do not overwrite |",
        f"| V4 hybrid | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | {len(hybrid)} | {len(hybrid_ids)} | AI+Cloud+Public | 980 simhuman+1621 sop_cws | old main eval | appendix transfer | do not overwrite |",
        f"| v4 silver train/dev/test | `data/*_lskt_v4_silver.jsonl` | {len(train_s)}/{len(dev_s)}/{len(test_s)} | same | see Table 1 | rule_v4 drafts | old labels | source for new BIO | copy into new files only |",
        f"| new train | `data/repartition_v1/train.jsonl` | {len(parts['train'])} | {len(parts['train'])} | all four | v4 character | new | main train | created |",
        f"| new dev | `data/repartition_v1/dev.jsonl` | {len(parts['dev'])} | {len(parts['dev'])} | all four | v4 character | new | main dev | created |",
        f"| new test | `data/repartition_v1/test.jsonl` | {len(parts['test'])} | {len(parts['test'])} | all four | v4 character | new | main test | created |",
        "| encoder train | `scripts/train_cn_roberta_crf.py` | — | — | — | — | CRF trainer | reuse | new out_dir |",
        "| scorer | `scorer/score_lskt.py` cnss-lskt-1.2.0 | — | — | — | — | official | reuse | — |",
        "| 1M encoder | `output/jobbert_zh_1m/mlm/encoder` | — | — | — | — | frozen DAPT | reuse | do not overwrite |",
    ]
    (OUT / "artifact_inventory.md").write_text("\n".join(artifact) + "\n", encoding="utf-8")
    print(json.dumps({
        "chosen_seed": seed,
        "cost": best[0],
        "n": {k: len(v) for k, v in parts.items()},
        "hard_ok": True,
        "test_sha256": sha256_file(paths["test"]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
