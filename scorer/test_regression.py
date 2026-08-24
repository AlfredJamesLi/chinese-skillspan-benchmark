#!/usr/bin/env python3
"""Scorer unit tests + canonical Gold checks. Does not overwrite dumps."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_lskt import (  # noqa: E402
    SCORER_VERSION,
    load_records,
    main as score_main,
    match_exact,
    rec_id,
    score,
    tags_to_spans,
)

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
CANON = PAPER / "data/gold_canonical_v2.jsonl"
RAW = ROOT / "chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl"
CHATGPT = ROOT / "chinese_skillspan_preprocessing/output/dir/test-gpt/silver_gpt4o_sent_ner_test_1005_last_test.jsonl"
JOBBERT = ROOT / "Baseline_Models_Collection/out_jobbert_skill_chinese_encoder_aligned.jsonl"


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def test_micro_does_not_collapse_cross_sentence_offsets() -> None:
    """Two sentences with the same (0,2,S) must count as 2 TP, not 1."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        gold = [
            {"id": "a", "tokens": ["x", "y", "z"], "list_of_selection_bio4": ["B-S", "I-S", "O"]},
            {"id": "b", "tokens": ["x", "y", "z"], "list_of_selection_bio4": ["B-S", "I-S", "O"]},
        ]
        pred = [
            {"id": "a", "tokens": ["x", "y", "z"], "pred_tags": ["B-S", "I-S", "O"]},
            {"id": "b", "tokens": ["x", "y", "z"], "pred_tags": ["B-S", "I-S", "O"]},
            {"id": "extra-test", "tokens": ["q"], "pred_tags": ["O"]},
        ]
        gp, pp = td / "g.jsonl", td / "p.jsonl"
        _write_jsonl(gp, gold)
        _write_jsonl(pp, pred)
        r = score(str(gp), str(pp), align_mode="official", n_boot=0)
        assert r["alignment_ok"], r.get("error")
        assert r["n_extra"] == 1
        assert r["n_missing"] == 0
        assert r["n_duplicate_gold_preds"] == 0
        assert r["typed_exact"]["tp"] == 2, r["typed_exact"]
        assert abs(r["typed_exact"]["f1"] - 1.0) < 1e-9
        assert r["primary_metric"] == "typed_exact_micro_f1"


def test_official_missing_and_dup_fail_extras_ok() -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        gold = [
            {"id": "a", "tokens": ["x"], "list_of_selection_bio4": ["O"]},
            {"id": "b", "tokens": ["y"], "list_of_selection_bio4": ["O"]},
        ]
        pred_ok_extra = [
            {"id": "a", "tokens": ["x"], "pred_tags": ["O"]},
            {"id": "b", "tokens": ["y"], "pred_tags": ["O"]},
            {"id": "c", "tokens": ["z"], "pred_tags": ["O"]},
        ]
        gp, pp = td / "g.jsonl", td / "p.jsonl"
        _write_jsonl(gp, gold)
        _write_jsonl(pp, pred_ok_extra)
        ok = score(str(gp), str(pp), align_mode="official", n_boot=0)
        assert ok["alignment_ok"]
        exact = score(str(gp), str(pp), align_mode="official", n_boot=0, require_exact_id_set=True)
        assert not exact["alignment_ok"]
        pred_miss = [{"id": "a", "tokens": ["x"], "pred_tags": ["O"]}]
        _write_jsonl(pp, pred_miss)
        miss = score(str(gp), str(pp), align_mode="official", n_boot=0)
        assert not miss["alignment_ok"]
        assert miss["n_missing"] == 1
        pred_dup = [
            {"id": "a", "tokens": ["x"], "pred_tags": ["O"]},
            {"id": "a", "tokens": ["x"], "pred_tags": ["B-S"]},
            {"id": "b", "tokens": ["y"], "pred_tags": ["O"]},
        ]
        _write_jsonl(pp, pred_dup)
        dup = score(str(gp), str(pp), align_mode="official", n_boot=0)
        assert not dup["alignment_ok"]
        assert dup["n_duplicate_gold_preds"] == 1
        rc = score_main(["--gold", str(gp), "--pred", str(pp), "--align-mode", "official", "--n-boot", "0"])
        assert rc == 2


def test_canonical_gold_ids_unique() -> None:
    rows = load_records(str(CANON))
    ids = [rec_id(r) for r in rows]
    assert len(ids) == len(set(ids)) == 2601
    raw = load_records(str(RAW))
    assert len(raw) == 2676
    assert len({rec_id(r) for r in raw}) == 2601


def test_all_o_bio4_falls_through_to_untyped() -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        gold = [{"id": "a", "tokens": ["x", "y"], "list_of_selection_bio4": ["B-S", "I-S"]}]
        pred = [{
            "id": "a",
            "tokens": ["x", "y"],
            "list_of_selection_bio4": ["O", "O"],
            "list_of_selection": ["B", "I"],
        }]
        gp, pp = td / "g.jsonl", td / "p.jsonl"
        _write_jsonl(gp, gold)
        _write_jsonl(pp, pred)
        r = score(str(gp), str(pp), align_mode="official", n_boot=0)
        assert r["collapsed_exact"]["tp"] == 1, r["collapsed_exact"]
        assert r["typed_exact"]["tp"] == 0


def test_bio_legal_drops_i_after_o() -> None:
    assert tags_to_spans(["O", "I-SKILL", "I-SKILL"]) == []
    assert tags_to_spans(["B-SKILL", "I-SKILL"]) == [(0, 2, "SKILL")]
    m = match_exact([(0, 2, "SKILL")], [(0, 2, "SKILL")])
    assert m["tp"] == 1


def test_chatgpt_not_labeled_as_paper_reproduction() -> None:
    """Report exact delta vs 0.6700; do not treat 0.665 as a match."""
    r = score(str(CANON), str(CHATGPT), align_mode="official", n_boot=0)
    assert not r["alignment_ok"], "ChatGPT dump still has duplicate Gold IDs"
    f1 = r["typed_exact"]["f1"]
    collapsed = r["collapsed_exact"]["f1"]
    print(
        f"ChatGPT canonical typed_exact={f1:.6f} collapsed={collapsed:.6f} "
        f"vs paper 0.6700; official fail: {r.get('error')}"
    )
    assert abs(collapsed - 0.6700) > 0.001 or abs(f1 - 0.6700) > 0.001


def test_jobbert_micro_is_not_0_46() -> None:
    r = score(str(CANON), str(JOBBERT), align_mode="official", pred_fields=("pred_tags",), n_boot=0)
    f1 = r["collapsed_exact"]["f1"]
    print(f"JobBERT-skill canonical collapsed_exact={f1:.6f} official_ok={r['alignment_ok']}")
    assert f1 < 0.05, f1
    assert f1 > 0.001, f1


def main() -> int:
    tests = [
        test_micro_does_not_collapse_cross_sentence_offsets,
        test_official_missing_and_dup_fail_extras_ok,
        test_canonical_gold_ids_unique,
        test_bio_legal_drops_i_after_o,
        test_all_o_bio4_falls_through_to_untyped,
        test_chatgpt_not_labeled_as_paper_reproduction,
        test_jobbert_micro_is_not_0_46,
    ]
    failed = 0
    print(f"scorer {SCORER_VERSION}")
    for fn in tests:
        try:
            fn()
            print(f"OK   {fn.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {type(e).__name__}: {e}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
