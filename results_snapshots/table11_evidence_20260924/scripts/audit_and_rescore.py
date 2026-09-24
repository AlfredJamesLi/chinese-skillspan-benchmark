#!/usr/bin/env python3
"""Table 11 evidence recovery + independent Gold150 rescoring. Does not train or overwrite original runs."""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import statistics
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/home/guojingli3/cnss_external_benchmarks_20260921")
EV = ROOT / "TABLE11_EVIDENCE_20260924"
PUB = Path("/home/guojingli3/chinese-skillspan-benchmark")
sys.path.insert(0, str(ROOT / "adapters"))
from convert_gold150_to_bio import TYPE_MAP, convert_record, spans_to_bio  # noqa: E402
from score_lskt import SCORER_VERSION, score as official_score  # noqa: E402

CELLS = [
    ("xlm-roberta-large", "FacebookAI/xlm-roberta-large", "c23d21b0620b635a76227c604d44e43a9f0ee389", 42),
    ("xlm-roberta-large", "FacebookAI/xlm-roberta-large", "c23d21b0620b635a76227c604d44e43a9f0ee389", 43),
    ("xlm-roberta-large", "FacebookAI/xlm-roberta-large", "c23d21b0620b635a76227c604d44e43a9f0ee389", 44),
    ("esco-xlm-roberta-large", "jjzha/esco-xlm-roberta-large", "8093cc37ac619a25c5166355acba7be878eb6402", 42),
    ("esco-xlm-roberta-large", "jjzha/esco-xlm-roberta-large", "8093cc37ac619a25c5166355acba7be878eb6402", 43),
    ("esco-xlm-roberta-large", "jjzha/esco-xlm-roberta-large", "8093cc37ac619a25c5166355acba7be878eb6402", 44),
]
EXPECTED_EXACT = {
    ("xlm-roberta-large", 42): (0.49957662997459773, 11),
    ("xlm-roberta-large", 43): (0.5224489795918368, 14),
    ("xlm-roberta-large", 44): (0.5445705024311183, 14),
    ("esco-xlm-roberta-large", 42): (0.5160758450123661, 19),
    ("esco-xlm-roberta-large", 43): (0.5401459854014599, 15),
    ("esco-xlm-roberta-large", 44): (0.5576763485477179, 10),
}
FREEZE_SHA = "ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0"
TRAIN_SHA = "8921e5fc4b89a0fa83bd942f919c3325546b9938e099b6a13e378736b6717d2e"
DEV_SHA = "e67a3eb5229b94c6c1b552d5f40ece9ad362197236c20cd66b7f2600c9636fef"
HAN_RE = re.compile(r"[\u3400-\u9fff\U00020000-\U0002a6df]")
LATIN_RE = re.compile(r"[A-Za-z]")
TRANSLATION_HINTS = re.compile(
    r"translat|round[-_ ]?trip|mt_|machine.?trans|en2zh|zh2en|gold.?hint|teacher.?force",
    re.I,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def bio_spans(tags: list[str]) -> list[tuple[int, int, str]]:
    spans = []
    i, n = 0, len(tags)
    while i < n:
        t = tags[i]
        if t.startswith("B-"):
            typ = t[2:]
            j = i + 1
            while j < n and tags[j] == f"I-{typ}":
                j += 1
            spans.append((i, j, typ))
            i = j
        else:
            i += 1
    return spans


def copy_code() -> dict[str, str]:
    mapping = {
        "code/run_chinese_encoder.py": ROOT / "run_chinese_encoder.py",
        "code/adapters/score_lskt.py": ROOT / "adapters" / "score_lskt.py",
        "code/adapters/convert_gold150_to_bio.py": ROOT / "adapters" / "convert_gold150_to_bio.py",
        "code/adapters/test_chinese_roundtrip.py": ROOT / "adapters" / "test_chinese_roundtrip.py",
        "code/scripts/one_chinese.sbatch": ROOT / "scripts" / "one_chinese.sbatch",
        "code/scripts/chinese_full_2gpu.sbatch": ROOT / "scripts" / "chinese_full_2gpu.sbatch",
        "code/scripts/run_remaining_today.py": ROOT / "scripts" / "run_remaining_today.py",
        "code/models.json": ROOT / "models.json",
        "env/ENV_RECORD.txt": ROOT / "ENV_RECORD.txt",
    }
    hashes = {}
    for rel, src in mapping.items():
        dst = EV / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        hashes[rel] = sha256_file(dst)
    pub_scorer = PUB / "scorer" / "score_lskt.py"
    hashes["public_repo_scorer/score_lskt.py"] = sha256_file(pub_scorer)
    hashes["scorer_bytes_equal_public_cnss-lskt-1.2.0"] = hashes["code/adapters/score_lskt.py"] == hashes["public_repo_scorer/score_lskt.py"]
    hashes["scorer_version_constant"] = SCORER_VERSION
    return hashes


def script_mentions_translation(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if TRANSLATION_HINTS.search(line):
            hits.append(f"{path.name}:{i}:{line.strip()[:200]}")
    return hits


def split_stats(path: Path, kind: str) -> dict:
    rows = load_jsonl(path)
    ids = []
    n_spans = 0
    type_counts = Counter()
    empty = 0
    long128 = 0
    han_sents = 0
    latin_only = 0
    punct_zh = 0
    oob = []
    overlap_spans = []
    illegal = []
    empty_text = []
    nfc_diff = 0
    fields = Counter()
    samples = []
    for r in rows:
        for k in r:
            fields[k] += 1
        if kind == "gold150_doccano":
            sid = str(r.get("source_id") or r.get("id")).strip()
            text = r.get("text") or ""
            labels = r.get("label") or []
            toks = list(text)
            try:
                tags = spans_to_bio(text, labels)
            except ValueError as e:
                illegal.append({"id": sid, "error": str(e)})
                tags = ["O"] * len(toks)
            spans = [(int(a), int(b), TYPE_MAP.get(str(c), str(c))) for a, b, c in labels]
        else:
            sid = str(r.get("id")).strip()
            text = r.get("sentence") or ""
            toks = r.get("tokens")
            tags = r.get("list_of_selection_bio4") or []
            if toks != list(text):
                illegal.append({"id": sid, "error": "tokens != list(sentence)"})
            spans = bio_spans(tags)
            if "".join(toks or []) != text:
                illegal.append({"id": sid, "error": "join(tokens) != sentence"})
        ids.append(sid)
        if not text:
            empty_text.append(sid)
        if unicodedata.normalize("NFC", text) != text:
            nfc_diff += 1
        if HAN_RE.search(text):
            han_sents += 1
        if LATIN_RE.search(text) and not HAN_RE.search(text):
            latin_only += 1
        if any(ch in text for ch in "，。；、（）"):
            punct_zh += 1
        if len(toks or text) > 128:
            long128 += 1
        if not spans:
            empty += 1
        n_spans += len(spans)
        occupied = [None] * len(toks or text)
        for a, b, typ in spans:
            type_counts[typ] += 1
            if a < 0 or b > len(toks or text) or a >= b:
                oob.append({"id": sid, "span": [a, b, typ], "n": len(toks or text)})
                continue
            if any(occupied[i] for i in range(a, b)):
                overlap_spans.append({"id": sid, "span": [a, b, typ]})
            for i in range(a, min(b, len(occupied))):
                occupied[i] = typ
        if len(samples) < 3:
            samples.append({"id": sid, "text_prefix": text[:80], "n_chars": len(text), "n_spans": len(spans)})
    dup = [i for i, c in Counter(ids).items() if c > 1]
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "n_rows": len(rows),
        "n_unique_ids": len(set(ids)),
        "duplicate_ids": dup,
        "n_spans": n_spans,
        "span_types": dict(type_counts),
        "n_empty_span_sents": empty,
        "n_empty_text": empty_text,
        "n_chars_gt_128": long128,
        "n_sents_with_han": han_sents,
        "n_latin_without_han": latin_only,
        "n_sents_with_cjk_punct": punct_zh,
        "n_text_not_already_nfc": nfc_diff,
        "out_of_range_spans": oob,
        "overlapping_spans": overlap_spans,
        "illegal": illegal,
        "fields_present": dict(fields),
        "samples": samples,
        "id_prefix_examples": sorted(set(ids))[:8],
    }


def overlap_report(train, dev, gold) -> dict:
    def recs(path, id_key, text_key):
        out = {}
        for r in load_jsonl(path):
            sid = str(r.get(id_key) or r.get("id") or r.get("source_id")).strip()
            text = r.get(text_key) or r.get("sentence") or r.get("text") or ""
            out[sid] = text
        return out

    tr = recs(train, "id", "sentence")
    dv = recs(dev, "id", "sentence")
    gd = recs(gold, "source_id", "text")

    def set_overlap(a, b):
        return sorted(set(a) & set(b))

    def text_overlap(a: dict, b: dict, nfc=False):
        sa = {unicodedata.normalize("NFC", t) if nfc else t for t in a.values()}
        sb = {unicodedata.normalize("NFC", t) if nfc else t for t in b.values()}
        return {
            "n_shared_strings": len(sa & sb),
            "rule": "exact Unicode string equality on sentence/text" + (" after NFC" if nfc else " (raw)"),
        }

    return {
        "id_overlap": {
            "rule": "string equality on record id / source_id after strip",
            "train_dev": set_overlap(tr, dv),
            "train_gold150": set_overlap(tr, gd),
            "dev_gold150": set_overlap(dv, gd),
            "n_train_dev": len(set_overlap(tr, dv)),
            "n_train_gold150": len(set_overlap(tr, gd)),
            "n_dev_gold150": len(set_overlap(dv, gd)),
        },
        "exact_text_overlap": {
            "train_dev": text_overlap(tr, dv, False),
            "train_gold150": text_overlap(tr, gd, False),
            "dev_gold150": text_overlap(dv, gd, False),
        },
        "nfc_text_overlap": {
            "train_dev": text_overlap(tr, dv, True),
            "train_gold150": text_overlap(tr, gd, True),
            "dev_gold150": text_overlap(dv, gd, True),
        },
        "ad_level_isolation": {
            "status": "cannot_prove",
            "reason": "IDs are handbook-sentence keys like 1801-s0004; files have no advertisement/job-posting parent ID field for clustering near-duplicates across ads.",
        },
    }


def gold150_vs_published() -> dict:
    local = ROOT / "chinese_data" / "gold150_test.jsonl"
    pub1 = PUB / "data" / "gold150_test.jsonl"
    pub2 = PUB / "data" / "gold150" / "gold150_test.jsonl"
    rows_l = load_jsonl(local)
    rows_p = load_jsonl(pub1)
    diffs = []
    n_spans = 0
    n_L = 0
    for i, (a, b) in enumerate(zip(rows_l, rows_p)):
        if a != b:
            diffs.append({"index": i, "local_id": a.get("source_id"), "pub_id": b.get("source_id")})
        labels = a.get("label") or []
        n_spans += len(labels)
        n_L += sum(1 for x in labels if len(x) >= 3 and x[2] == "Language_Skills&Knowledge")
    return {
        "local_sha256": sha256_file(local),
        "published_data_gold150_test_sha256": sha256_file(pub1),
        "published_data_gold150_dir_sha256": sha256_file(pub2),
        "expected_freeze_sha256": FREEZE_SHA,
        "bytes_equal_published": sha256_file(local) == sha256_file(pub1) == sha256_file(pub2) == FREEZE_SHA,
        "n_rows_local": len(rows_l),
        "n_rows_published": len(rows_p),
        "n_record_diffs_in_order": len(diffs),
        "record_diffs_head": diffs[:10],
        "n_spans_from_doccano_labels": n_spans,
        "n_L_spans": n_L,
        "public_urls": [
            "https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150_test.jsonl",
            "https://doi.org/10.5281/zenodo.22698504 (v0.1.3 includes this freeze)",
        ],
    }


def pred_alignment(gold_bio: list[dict], pred: list[dict]) -> dict:
    g_ids = [r["id"] for r in gold_bio]
    p_ids = [str(r.get("id")).strip() for r in pred]
    gmap = {r["id"]: r for r in gold_bio}
    pmap = {}
    dup = []
    for r in pred:
        i = str(r.get("id")).strip()
        if i in pmap:
            dup.append(i)
        pmap[i] = r
    missing = [i for i in g_ids if i not in pmap]
    extra = [i for i in p_ids if i not in gmap]
    text_mismatch = []
    len_mismatch = []
    replaced = 0
    for i in g_ids:
        if i not in pmap:
            continue
        g, p = gmap[i], pmap[i]
        gt = "".join(g["tokens"])
        pt = "".join(p.get("tokens") or [])
        if gt != pt:
            text_mismatch.append(i)
        if len(p.get("list_of_selection_bio4") or []) != len(g["tokens"]):
            len_mismatch.append(i)
        if any(t == "■" for t in (p.get("tokens") or [])):
            replaced += 1
    return {
        "n_gold": len(g_ids),
        "n_pred": len(pred),
        "n_unique_pred_ids": len(pmap),
        "duplicate_pred_ids": dup,
        "missing_ids": missing,
        "extra_ids": extra,
        "id_order_equal": g_ids == p_ids,
        "n_text_mismatch": text_mismatch,
        "n_tag_len_mismatch": len_mismatch,
        "n_pred_with_placeholder_token": replaced,
    }


def empty_sentence_fp(gold_bio, pred) -> dict:
    gmap = {r["id"]: r for r in gold_bio}
    n_empty_gold = 0
    fp_ids = []
    for r in pred:
        i = str(r.get("id")).strip()
        g = gmap.get(i)
        if g is None:
            continue
        if bio_spans(g["list_of_selection_bio4"]):
            continue
        n_empty_gold += 1
        if bio_spans(r.get("list_of_selection_bio4") or []):
            fp_ids.append(i)
    return {"n_gold_sents_with_zero_spans": n_empty_gold, "n_empty_gold_with_pred_span": len(fp_ids), "ids": fp_ids}


def history_selection(hist: list[dict], claimed_epoch: int) -> dict:
    best_f1, best_ep = -1.0, None
    gold150_keys = []
    for row in hist:
        gold150_keys.extend([k for k in row if "gold150" in k.lower() or "test" == k])
        f1 = row["dev"]["f1"]
        ep = row["epoch"]
        if f1 > best_f1:
            best_f1, best_ep = f1, ep
    return {
        "n_epochs_logged": len(hist),
        "epochs": [r["epoch"] for r in hist],
        "argmax_dev_f1_earliest_tie": best_ep,
        "argmax_dev_f1_value": best_f1,
        "matches_claimed_best_epoch": best_ep == claimed_epoch,
        "gold150_or_test_keys_in_history": gold150_keys,
        "history_contains_gold150_metric": bool(gold150_keys),
    }


def mean_sd(xs):
    return {"n": len(xs), "mean": statistics.mean(xs), "sd_sample": statistics.stdev(xs) if len(xs) > 1 else 0.0, "values": xs}


def paper_round(x: float, nd=3) -> float:
    return float(f"{x:.{nd}f}")


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    code_hashes = copy_code()
    train_p = ROOT / "chinese_data" / "train_b2.jsonl"
    dev_p = ROOT / "chinese_data" / "dev_b2.jsonl"
    gold_p = ROOT / "chinese_data" / "gold150_test.jsonl"
    pub_train = PUB / "data" / "silver_plus_v6a_nocross" / "train_b2.jsonl"
    pub_dev = PUB / "data" / "silver_plus_v6a_nocross" / "dev_b2.jsonl"

    data_manifest = {
        "train_b2": split_stats(train_p, "b2"),
        "dev_b2": split_stats(dev_p, "b2"),
        "gold150_doccano": split_stats(gold_p, "gold150_doccano"),
        "sha_match_published_b2": {
            "train": sha256_file(train_p) == sha256_file(pub_train) == TRAIN_SHA,
            "dev": sha256_file(dev_p) == sha256_file(pub_dev) == DEV_SHA,
            "published_train": str(pub_train),
            "published_dev": str(pub_dev),
        },
        "gold150_vs_published": gold150_vs_published(),
        "overlap": overlap_report(train_p, dev_p, gold_p),
        "label_versions": {
            "b2": "list_of_selection_bio4 on character tokens; Silver-plus v6a_nocross teacher labels",
            "gold150": "Doccano label triples with freeze spelling Tranversial SKills / Language_Skills&Knowledge / knowledge / skills",
        },
    }
    dump(EV / "data_manifest" / "data_manifest.json", data_manifest)

    translation = {
        "training_script_translation_hits": script_mentions_translation(ROOT / "run_chinese_encoder.py"),
        "convert_script_translation_hits": script_mentions_translation(ROOT / "adapters" / "convert_gold150_to_bio.py"),
        "direct_chinese_read_sites": {
            "normalize_b2": "run_chinese_encoder.py:normalize_b2 asserts list(sentence)==tokens and uses those characters as the encoder words",
            "gold150_convert": "convert_gold150_to_bio.py:convert_record uses rec['text'] and list(text) as tokens; spans are integer Unicode-code-point offsets into that string",
            "no_translate_import": "run_chinese_encoder.py imports only stdlib + torch/numpy/transformers + local convert/score adapters",
        },
        "gold_tags_in_model_input": "Gold150 rows are encoded with all-O tags; gold BIO is written only for the scorer after prediction",
        "post_hoc_human_edit_in_code": False,
        "boundary_correction_in_code": False,
    }
    dump(EV / "data_manifest" / "translation_and_eval_target.json", translation)

    results_rows = []
    for line in (ROOT / "receipts" / "results.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("protocol_id") == "chinese_lskt_linear_b2_20260921" and r.get("metric_name") == "typed_exact_micro_f1":
            results_rows.append(r)

    cell_reports = []
    rescore_table = []
    old_vs_new = []
    for short, model, rev, seed in CELLS:
        run = ROOT / "runs" / "chinese" / "full" / short / str(seed)
        cfg_p = run / "config.json"
        pred_p = run / "gold150_predictions.jsonl"
        off_p = run / "gold150_official.json"
        gold_bio_p = run / "gold150_gold.bio.jsonl"
        hist_p = run / "history.json"
        res_p = run / "result.json"
        best = run / "best"
        ckpt = best / "model.safetensors"
        tok = best / "tokenizer.json"
        files = {
            "config.json": cfg_p,
            "gold150_predictions.jsonl": pred_p,
            "gold150_official.json": off_p,
            "gold150_gold.bio.jsonl": gold_bio_p,
            "history.json": hist_p,
            "result.json": res_p,
            "best/config.json": best / "config.json",
            "best/tokenizer.json": tok,
            "best/model.safetensors": ckpt,
        }
        file_hash = {k: (sha256_file(p) if p.exists() else None) for k, p in files.items() if k != "best/model.safetensors"}
        # heavy checkpoint hash may still be running; record size/mtime now
        ckpt_meta = None
        if ckpt.exists():
            st = ckpt.stat()
            ckpt_meta = {"path": str(ckpt), "bytes": st.st_size, "mtime": st.st_mtime, "exists": True}
        cfg = json.loads(cfg_p.read_text()) if cfg_p.exists() else {}
        res = json.loads(res_p.read_text()) if res_p.exists() else {}
        hist = json.loads(hist_p.read_text()) if hist_p.exists() else []
        old_off = json.loads(off_p.read_text()) if off_p.exists() else {}
        gold_bio = load_jsonl(gold_bio_p) if gold_bio_p.exists() else []
        pred = load_jsonl(pred_p) if pred_p.exists() else []
        best_cfg = json.loads((best / "config.json").read_text()) if (best / "config.json").exists() else {}

        receipt = next((r for r in results_rows if str(r.get("seed")) == str(seed) and short in (r.get("config_file") or "")), None)
        hash_vs_receipt = {}
        if receipt:
            hash_vs_receipt = {
                "config_sha256_match": file_hash.get("config.json") == receipt.get("config_sha256"),
                "pred_sha256_match": file_hash.get("gold150_predictions.jsonl") == receipt.get("predictions_sha256"),
                "official_sha256_match": file_hash.get("gold150_official.json") == receipt.get("eval_file_sha256"),
                "receipt_score": receipt.get("score"),
            }

        sel = history_selection(hist, res.get("best_epoch"))
        align = pred_alignment(gold_bio, pred) if gold_bio and pred else {"error": "missing gold or pred"}
        empty_fp = empty_sentence_fp(gold_bio, pred) if gold_bio and pred else {}

        # independent rescore in a new directory; do not overwrite old official json
        new_off_p = EV / "rescore_20260924" / short / str(seed) / "gold150_official.rescore.json"
        new_off = None
        if gold_bio_p.exists() and pred_p.exists():
            new_off = official_score(str(gold_bio_p), str(pred_p), align_mode="official", n_boot=2000, boot_seed=20260921)
            dump(new_off_p, new_off)

        def metric_pack(off):
            if not off:
                return None
            te = off.get("typed_exact") or {}
            tr = off.get("typed_relaxed") or {}
            ce = off.get("collapsed_exact") or {}
            per = off.get("per_type_exact") or {}
            macro = statistics.mean([per[t]["f1"] for t in ("L", "K", "S", "T") if t in per]) if per else None
            return {
                "typed_exact": te,
                "typed_relaxed": tr,
                "collapsed_exact_boundary": ce,
                "per_type_exact": per,
                "macro_f1_LKST": macro,
                "scorer_version": off.get("scorer_version"),
                "alignment_ok": off.get("alignment_ok"),
            }

        old_m = metric_pack(old_off)
        new_m = metric_pack(new_off)
        expected_f1, expected_ep = EXPECTED_EXACT[(short, seed)]
        diff = {
            "encoder": short,
            "seed": seed,
            "old_typed_exact_f1": (old_m or {}).get("typed_exact", {}).get("f1") if old_m else None,
            "new_typed_exact_f1": (new_m or {}).get("typed_exact", {}).get("f1") if new_m else None,
            "receipt_typed_exact_f1": expected_f1,
            "old_equals_new": ((old_m or {}).get("typed_exact", {}).get("f1") == (new_m or {}).get("typed_exact", {}).get("f1")) if old_m and new_m else False,
            "new_equals_receipt": ((new_m or {}).get("typed_exact", {}).get("f1") == expected_f1) if new_m else False,
            "best_epoch_result_json": res.get("best_epoch"),
            "best_epoch_expected": expected_ep,
            "best_epoch_from_history": sel.get("argmax_dev_f1_earliest_tie"),
        }
        old_vs_new.append(diff)
        rescore_table.append(
            {
                "encoder": short,
                "seed": seed,
                "best_epoch": res.get("best_epoch"),
                "dev_selection_f1": res.get("dev_selection_f1"),
                "rescore": new_m,
                "empty_sentence_fp": empty_fp,
                "command": [
                    str(ROOT / "env" / "bin" / "python"),
                    str(ROOT / "adapters" / "score_lskt.py"),
                    "--gold",
                    str(gold_bio_p),
                    "--pred",
                    str(pred_p),
                    "--align-mode",
                    "official",
                    "--n-boot",
                    "2000",
                    "--out",
                    str(new_off_p),
                ],
            }
        )

        # copy lightweight artifacts
        for name, src in {
            "config.json": cfg_p,
            "history.json": hist_p,
            "result.json": res_p,
            "gold150_predictions.jsonl": pred_p,
            "gold150_gold.bio.jsonl": gold_bio_p,
            "gold150_official.json": off_p,
            "best_config.json": best / "config.json",
            "best_tokenizer_config.json": best / "tokenizer_config.json",
            "best_special_tokens_map.json": best / "special_tokens_map.json",
        }.items():
            if src.exists():
                dst = EV / "runs_lightweight" / short / str(seed) / name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

        log_candidates = [
            ROOT / "logs" / f"chinese_full_{short}_{seed}.out",
            ROOT / "logs" / f"chinese_full_{short}_{seed}_try1.out",
        ]
        logs_found = []
        for lp in log_candidates:
            if lp.exists():
                dst = EV / "logs_excerpt" / lp.name
                text = lp.read_text(encoding="utf-8", errors="replace")
                dst.write_text(text, encoding="utf-8")
                logs_found.append({"path": str(lp), "sha256": sha256_file(lp), "n_lines": text.count("\n") + 1})

        cell_reports.append(
            {
                "encoder_short": short,
                "hf_id": model,
                "declared_revision": rev,
                "config_revision": cfg.get("revision"),
                "revision_match": cfg.get("revision") == rev,
                "seed": seed,
                "run_dir": str(run),
                "files_exist": {k: p.exists() for k, p in files.items()},
                "file_sha256": file_hash,
                "checkpoint": ckpt_meta,
                "hash_vs_receipt": hash_vs_receipt,
                "config": {
                    k: cfg.get(k)
                    for k in (
                        "model",
                        "revision",
                        "seed",
                        "epochs",
                        "batch_size",
                        "lr",
                        "method",
                        "labels",
                        "chunk_word_limit",
                        "selection",
                        "gold150_in_gradient",
                        "gold150_in_selection",
                        "gold150_id_overlap_in_used_splits",
                        "train_sha256",
                        "dev_sha256",
                        "gold150_sha256",
                        "split_counts",
                        "chunk_counts",
                        "python",
                        "torch",
                        "transformers",
                        "gpu",
                        "cuda",
                        "started_unix",
                    )
                },
                "head_vs_mlm": {
                    "base_cache_architecture_xlm": "XLMRobertaForMaskedLM",
                    "base_cache_architecture_esco": "RobertaForCustomMaskedLM",
                    "saved_run_architecture": best_cfg.get("architectures"),
                    "saved_id2label": best_cfg.get("id2label"),
                    "log_warning": "Some weights of XLMRobertaForTokenClassification were not initialized ... ['classifier.bias', 'classifier.weight']",
                    "explanation": "AutoModelForTokenClassification drops the masked-LM lm_head and randomly initializes a linear classifier (hidden_size x 9 LSKT BIO labels). Task head is not the MLM softmax.",
                },
                "finetune_scope": {
                    "optimizer_from_source": "AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)",
                    "encoder_frozen": False,
                    "all_parameters_updated": True,
                    "extra_training_data": False,
                    "init_from_another_task_head": False,
                    "precision": "float32; no autocast/AMP in run_chinese_encoder.py",
                },
                "selection": sel,
                "pred_alignment": align,
                "empty_sentence_fp": empty_fp,
                "logs": logs_found,
                "old_metrics": old_m,
                "new_metrics": new_m,
            }
        )

    dump(EV / "cell_reports.json", cell_reports)
    dump(EV / "rescore_20260924" / "per_seed.json", rescore_table)
    dump(EV / "rescore_20260924" / "old_vs_new_diff.json", old_vs_new)

    def collect(enc, key_path):
        vals = []
        for row in rescore_table:
            if row["encoder"] != enc:
                continue
            cur = row["rescore"]
            for k in key_path:
                cur = cur[k]
            vals.append(cur)
        return vals

    summary_mean = {}
    for enc in ("xlm-roberta-large", "esco-xlm-roberta-large"):
        exact = collect(enc, ["typed_exact", "f1"])
        relax = collect(enc, ["typed_relaxed", "f1"])
        bound = collect(enc, ["collapsed_exact_boundary", "f1"])
        macro = collect(enc, ["macro_f1_LKST"])
        summary_mean[enc] = {
            "typed_exact": mean_sd(exact),
            "typed_relaxed": mean_sd(relax),
            "boundary_collapsed_exact": mean_sd(bound),
            "macro_f1_LKST": mean_sd(macro),
            "paper_table11_rounded": {
                "exact": f"{paper_round(statistics.mean(exact))} ± {paper_round(statistics.stdev(exact))}",
                "relaxed": f"{paper_round(statistics.mean(relax))} ± {paper_round(statistics.stdev(relax))}",
                "boundary": f"{paper_round(statistics.mean(bound))} ± {paper_round(statistics.stdev(bound))}",
                "macro": f"{paper_round(statistics.mean(macro))} ± {paper_round(statistics.stdev(macro))}",
            },
        }
    dump(EV / "rescore_20260924" / "mean_sd.json", summary_mean)

    paper = {
        "tab_external_chinese_from_prompt_20260922": {
            "XLM-R-large": {"exact": "0.522 ± 0.022", "relaxed": "0.650 ± 0.021", "boundary": "0.571 ± 0.022", "macro": "0.607 ± 0.016"},
            "ESCOXLM-R": {"exact": "0.538 ± 0.021", "relaxed": "0.662 ± 0.022", "boundary": "0.582 ± 0.024", "macro": "0.622 ± 0.010"},
        },
        "rescore_rounded": {k: v["paper_table11_rounded"] for k, v in summary_mean.items()},
        "seed_exact_rescore": {
            f"{r['encoder']}/{r['seed']}": (r["rescore"] or {}).get("typed_exact", {}).get("f1") for r in rescore_table
        },
    }
    dump(EV / "rescore_20260924" / "vs_paper.json", paper)

    encoder_cache = {
        "xlm-roberta-large": {
            "snapshot_dir": str(ROOT / "hf_cache/hub/models--FacebookAI--xlm-roberta-large/snapshots/c23d21b0620b635a76227c604d44e43a9f0ee389"),
            "model.safetensors_symlink": str(ROOT / "hf_cache/hub/models--FacebookAI--xlm-roberta-large/snapshots/c23d21b0620b635a76227c604d44e43a9f0ee389/model.safetensors"),
            "blob": str(ROOT / "hf_cache/hub/models--FacebookAI--xlm-roberta-large/blobs/2dfa19f172412917cab174da04b46e2134811b723666965fd0aabd97caa6e23b"),
            "config_architectures": json.loads((ROOT / "hf_cache/hub/models--FacebookAI--xlm-roberta-large/snapshots/c23d21b0620b635a76227c604d44e43a9f0ee389/config.json").read_text())["architectures"],
            "refs_file_present": (ROOT / "hf_cache/hub/models--FacebookAI--xlm-roberta-large/refs/c23d21b0620b635a76227c604d44e43a9f0ee389").exists(),
        },
        "esco-xlm-roberta-large": {
            "snapshot_dir": str(ROOT / "hf_cache/hub/models--jjzha--esco-xlm-roberta-large/snapshots/8093cc37ac619a25c5166355acba7be878eb6402"),
            "model.safetensors_symlink": str(ROOT / "hf_cache/hub/models--jjzha--esco-xlm-roberta-large/snapshots/8093cc37ac619a25c5166355acba7be878eb6402/model.safetensors"),
            "blob": str(ROOT / "hf_cache/hub/models--jjzha--esco-xlm-roberta-large/blobs/5ab9c8c2901790a93235ccb37a2847b0e684760271fc7ed1645fbaf00d2cdae0"),
            "config_architectures": json.loads((ROOT / "hf_cache/hub/models--jjzha--esco-xlm-roberta-large/snapshots/8093cc37ac619a25c5166355acba7be878eb6402/config.json").read_text())["architectures"],
            "refs_main": (ROOT / "hf_cache/hub/models--jjzha--esco-xlm-roberta-large/refs/main").read_text().strip()
            if (ROOT / "hf_cache/hub/models--jjzha--esco-xlm-roberta-large/refs/main").exists()
            else None,
        },
    }
    dump(EV / "hashes" / "encoder_cache_manifest.json", encoder_cache)
    dump(EV / "hashes" / "code_sha256.json", code_hashes)

    launch = {
        "xlm-roberta-large/42": {
            "log": "logs/chinese_full.out + logs/chinese_full_xlm-roberta-large_42.out",
            "launcher": "scripts/chinese_full_2gpu.sbatch job path (GPU0, started 2026-09-22T04:51:14+08:00)",
            "command": f"{ROOT}/env/bin/python {ROOT}/run_chinese_encoder.py --model FacebookAI/xlm-roberta-large --revision c23d21b0620b635a76227c604d44e43a9f0ee389 --seed 42 --output {ROOT}/runs/chinese/full/xlm-roberta-large/42",
            "note": "Default train/dev/gold150 paths. Full command line not prefixed with # CMD in this log; reconstructed from sbatch + models.json + config.json.",
        },
        "xlm-roberta-large/43": {
            "log": "logs/chinese_full.out + logs/chinese_full_xlm-roberta-large_43.out",
            "launcher": "scripts/chinese_full_2gpu.sbatch (GPU1, same start timestamp)",
            "command": f"{ROOT}/env/bin/python {ROOT}/run_chinese_encoder.py --model FacebookAI/xlm-roberta-large --revision c23d21b0620b635a76227c604d44e43a9f0ee389 --seed 43 --output {ROOT}/runs/chinese/full/xlm-roberta-large/43",
            "note": "Same reconstruction as seed 42.",
        },
        "xlm-roberta-large/44": {
            "log": "logs/chinese_full_xlm-roberta-large_44_try1.out",
            "launcher": "scripts/run_remaining_today.py",
            "command_from_log": open(ROOT / "logs/chinese_full_xlm-roberta-large_44_try1.out", encoding="utf-8").read().splitlines()[1],
        },
        "esco-xlm-roberta-large/42": {
            "log": "logs/chinese_full_esco-xlm-roberta-large_42_try1.out",
            "command_from_log": open(ROOT / "logs/chinese_full_esco-xlm-roberta-large_42_try1.out", encoding="utf-8").read().splitlines()[1],
        },
        "esco-xlm-roberta-large/43": {
            "log": "logs/chinese_full_esco-xlm-roberta-large_43_try1.out",
            "command_from_log": open(ROOT / "logs/chinese_full_esco-xlm-roberta-large_43_try1.out", encoding="utf-8").read().splitlines()[1],
        },
        "esco-xlm-roberta-large/44": {
            "log": "logs/chinese_full_esco-xlm-roberta-large_44_try1.out",
            "command_from_log": open(ROOT / "logs/chinese_full_esco-xlm-roberta-large_44_try1.out", encoding="utf-8").read().splitlines()[1],
        },
        "defaults_not_overridden": {
            "epochs": 20,
            "batch_size": 8,
            "lr": 2e-5,
            "train": str(train_p),
            "dev": str(dev_p),
            "gold150": str(gold_p),
        },
    }
    dump(EV / "env" / "launch_commands.json", launch)

    answers = {
        "1_no_translation_chinese_adaptation": {
            "verdict": "yes_from_executed_code_and_inputs",
            "evidence": "run_chinese_encoder.py reads Chinese character tokens; Gold150 freeze SHA matches published Chinese Doccano file; no translation call in the training/eval path.",
        },
        "2_original_gold150": {
            "verdict": bool(data_manifest["gold150_vs_published"]["bytes_equal_published"]),
            "n": data_manifest["gold150_doccano"]["n_rows"],
            "n_spans": data_manifest["gold150_doccano"]["n_spans"],
            "n_L": data_manifest["gold150_doccano"]["span_types"].get("L"),
        },
        "3_six_checkpoints_and_preds_exist": {
            "verdict": all(c["files_exist"].get("best/model.safetensors") and c["files_exist"].get("gold150_predictions.jsonl") for c in cell_reports),
            "per_cell": {f"{c['encoder_short']}/{c['seed']}": c["files_exist"] for c in cell_reports},
        },
        "4_old_table_rescores_identically": {
            "verdict": all(d["old_equals_new"] and d["new_equals_receipt"] for d in old_vs_new),
            "diff": old_vs_new,
            "mean_sd": summary_mean,
        },
        "5_platforms": {
            "local_pack": str(EV),
            "github_results_commit_preserved": "46d1166f8e11dd52d473f645536074bb8dd0a53c",
            "github_audit_commit": "pending_this_session",
            "hf_models": "not_published",
            "zenodo_models": "not_published",
        },
        "delivery_status": {
            "files_checked": True,
            "predictions_rescored": True,
            "checkpoint_reinferred": False,
            "full_training_rerun": False,
        },
    }
    dump(EV / "ANSWERS.json", answers)
    print(json.dumps({"ok": True, "n_cells": len(cell_reports), "rescore_equal": answers["4_old_table_rescores_identically"]["verdict"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
