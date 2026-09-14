#!/usr/bin/env python3
"""Unit tests for silver_public_api_lib (no network)."""
from __future__ import annotations

import unittest

from silver_public_api_lib import (
    extract_json,
    hamilton,
    repair_span_offsets,
    spans_to_bio,
    to_student_row,
    validate_records,
)


class TestHamilton(unittest.TestCase):
    def test_exact(self):
        q = hamilton({"a": 2, "b": 2}, 4)
        self.assertEqual(sum(q.values()), 4)

    def test_2500(self):
        q = hamilton({"阿里云公开数据集": 3174, "事业单位招聘": 2381, "上市公司招聘": 2381}, 2500)
        self.assertEqual(sum(q.values()), 2500)
        self.assertEqual(q["阿里云公开数据集"], 1000)
        self.assertEqual(q["事业单位招聘"], 750)
        self.assertEqual(q["上市公司招聘"], 750)


class TestExtract(unittest.TestCase):
    def test_plain(self):
        obj, note = extract_json('{"records": []}')
        self.assertIsNone(note)
        self.assertEqual(obj, {"records": []})

    def test_fence(self):
        obj, note = extract_json('```json\n{"records": [1]}\n```')
        self.assertEqual(obj, {"records": [1]})
        self.assertIsNone(note)

    def test_garbage_then_object(self):
        obj, note = extract_json('note\n{"records": []}\n')
        self.assertEqual(obj, {"records": []})
        self.assertTrue(note)


class TestValidate(unittest.TestCase):
    def _ok(self):
        src = [{"id": "a", "text": "熟悉Python"}]
        parsed = {
            "records": [
                {
                    "id": "a",
                    "spans": [{"start": 2, "end": 8, "text": "Python", "label": "S"}],
                    "status": "candidate_complete",
                    "note": "ok",
                    "issues": [],
                }
            ]
        }
        return src, parsed

    def test_ok(self):
        src, parsed = self._ok()
        v = validate_records(src, parsed)
        self.assertTrue(v["ok"], v)

    def test_mismatch_offset(self):
        src, parsed = self._ok()
        parsed["records"][0]["spans"][0]["text"] = "python"
        v = validate_records(src, parsed)
        self.assertFalse(v["ok"])
        self.assertTrue(any(e["kind"] == "offset_mismatch" for e in v["errors"]))

    def test_overlap(self):
        src = [{"id": "a", "text": "abcdef"}]
        parsed = {
            "records": [
                {
                    "id": "a",
                    "spans": [
                        {"start": 0, "end": 3, "text": "abc", "label": "S"},
                        {"start": 2, "end": 5, "text": "cde", "label": "K"},
                    ],
                    "status": "candidate_complete",
                    "note": "x",
                    "issues": [],
                }
            ]
        }
        v = validate_records(src, parsed)
        self.assertFalse(v["ok"])
        self.assertTrue(any(e["kind"] == "overlap" for e in v["errors"]))

    def test_empty_status(self):
        src = [{"id": "a", "text": "福利待遇年终奖"}]
        parsed = {
            "records": [
                {
                    "id": "a",
                    "spans": [],
                    "status": "confirmed_empty",
                    "note": "福利",
                    "issues": [],
                }
            ]
        }
        v = validate_records(src, parsed)
        self.assertTrue(v["ok"], v)


class TestRepair(unittest.TestCase):
    def test_off_by_one(self):
        text = "负责日常的数据库优化和维护工作"
        spans = [{"start": 6, "end": 14, "text": "数据库优化和维护", "label": "S"}]
        out, notes = repair_span_offsets(text, spans)
        self.assertEqual(out[0]["start"], 5)
        self.assertEqual(out[0]["end"], 13)
        self.assertEqual(text[5:13], "数据库优化和维护")
        self.assertTrue(notes)

    def test_already_ok(self):
        text = "熟悉Python"
        spans = [{"start": 2, "end": 8, "text": "Python", "label": "S"}]
        out, notes = repair_span_offsets(text, spans)
        self.assertEqual(out[0]["start"], 2)
        self.assertFalse(notes)


class TestBio(unittest.TestCase):
    def test_roundtrip(self):
        text = "熟悉Python"
        tags, triples = spans_to_bio(text, [{"start": 2, "end": 8, "text": "Python", "label": "S"}])
        self.assertEqual(triples, [[2, 8, "S"]])
        self.assertEqual(tags[2], "B-S")
        self.assertEqual(tags[3], "I-S")
        self.assertEqual(tags[0], "O")
        row = to_student_row({"id": "x", "text": text, "source_domain": "t"}, {
            "spans": [{"start": 2, "end": 8, "text": "Python", "label": "S"}],
            "status": "candidate_complete",
            "note": "n",
            "issues": [],
        })
        self.assertEqual(row["tokens"], list(text))
        self.assertEqual(len(row["list_of_selection_bio4"]), len(text))


if __name__ == "__main__":
    unittest.main()
