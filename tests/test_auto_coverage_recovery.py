"""Regression checks for source-bound translation completeness and safe partial patches."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "automation"))
import book_runner as runner


class _PlainHelper:
    def plan(self, source):
        return None

    def spans(self, plan):
        result = [p for p in plan["parts"] if p["kind"] == "text"]
        ids = [p["id"] for p in result]
        assert len(set(ids)) == len(ids)
        return [{"id": p["id"], "source": p["original"]} for p in result]


class CoverageRecoveryTests(unittest.TestCase):
    def test_source_plan_is_bounded_and_preserves_every_source_byte(self):
        source = "\n".join(["Title", ""]) + "\n\n".join(
            f"Paragraph {i}. " + ("This sentence carries meaning. " * 17)
            for i in range(14)
        ) + "\n"
        result = runner.bounded_source_plan(source, _PlainHelper(), limit=1100)
        chunks = _PlainHelper().spans(result)
        self.assertGreater(len(chunks), 4)
        self.assertTrue(all(len(p["source"]) <= 1100 for p in chunks))
        self.assertEqual(result["source_sha256"], hashlib.sha256(source.encode()).hexdigest())
        restored = "".join(
            p["before"] + p["original"] + p["after"]
            if p["kind"] == "text" else p["value"] for p in result["parts"])
        self.assertEqual(restored, source)
        self.assertEqual([p["id"] for p in chunks],
                         [f"s{i:05d}" for i in range(1, len(chunks) + 1)])

    def test_detects_large_missing_chapter_and_short_segment(self):
        source = ("A source paragraph has several sentences.\n\n" * 95)
        self.assertTrue(runner.suspicious_translation_coverage(source, "Краткий текст.\n"))
        self.assertFalse(runner.suspicious_translation_coverage(source, source))
        self.assertEqual(
            runner.incomplete_structural_batch(
                [{"id": "s00001", "source": source}],
                {"s00001": "Недостаточный перевод."}), ["s00001"])
        self.assertEqual(
            runner.incomplete_structural_batch(
                [{"id": "s00001", "source": source}],
                {"s00001": source}), [])

    def test_overlapping_finding_patches_accept_only_safe_partial_for_new_review(self):
        src = "An important source phrase.\n"
        translation = "An incorrect target phrase.\n"
        digest_src = hashlib.sha256(src.encode()).hexdigest()
        digest_dst = hashlib.sha256(translation.encode()).hexdigest()
        record = {"record_id": "review-123", "source_sha256": digest_src,
                  "translation_sha256": digest_dst, "outcome": "CORRECTIONS_REQUIRED",
                  "quality_report": {"evidence_version": 2, "findings": [
                      {"id": "finding-a", "resolved": False},
                      {"id": "finding-b", "resolved": False},
                  ]}}
        patches = [
            {"finding_id": "finding-a", "operation": "replace",
             "target_anchor": {"quote": "incorrect target", "occurrence": 0},
             "replacement": "correct target"},
            {"finding_id": "finding-b", "operation": "replace",
             "target_anchor": {"quote": "incorrect target", "occurrence": 0},
             "replacement": "alternative target"},
        ]
        chapter = {"unit_id": "chapter-000001", "number": 1,
                   "source_path": "extracted/one.md",
                   "translation_path": "translated/one.md",
                   "translation_acceptance": {
                       "source_sha256": digest_src, "translation_sha256": digest_dst}}
        status = {"workflow_revision": "a" * 40, "model_calls_started": 0,
                  "active": {"role": "corrector", "session_id": "owner", "chapter": 1}}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            book = root / "books" / "example"
            (book / "extracted").mkdir(parents=True)
            (book / "translated").mkdir()
            (book / "glossary.md").write_text("glossary", encoding="utf-8")
            (book / "style-guide.md").write_text("style", encoding="utf-8")
            (book / chapter["source_path"]).write_text(src, encoding="utf-8")
            (book / chapter["translation_path"]).write_text(translation, encoding="utf-8")
            with patch.object(runner, "ROOT", root), \
                 patch.object(runner, "context", return_value=("sys", "user", src)), \
                 patch.object(runner, "role_contracts", return_value=("contract", [])), \
                 patch.object(runner, "complete", return_value="model json") as complete, \
                 patch.object(runner, "parse_correction_patches",
                              return_value=(patches, [], [])), \
                 patch.object(runner, "checkpoint") as checkpoint:
                result = runner.process_correction_batches(
                    "b" * 32, "example", status, root, chapter, record)
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "An correct target phrase.\n")
            self.assertEqual(status["correction_batch_progress"]["completed"], 1)
            self.assertEqual(status["correction_batch_progress"]["total"], 2)
            self.assertEqual(
                status["correction_overlap_deferred"]["unapplied_finding_ids"],
                ["finding-b"])
            self.assertEqual(checkpoint.call_count, 2)
            complete.assert_called_once()
            # The canonical source/translation were NOT modified in this helper.
            self.assertEqual((book / chapter["translation_path"]).read_text("utf-8"),
                             translation)


    def test_operator_retry_budget_is_book_scoped_bounded_and_does_not_waive_review(self):
        unit = "chapter-000025"
        chapter = {"unit_id": unit, "status": "translated"}
        ledger = {"records": []}
        status = {"correction_rounds": {unit: 4},
                  "correction_extensions": {unit: 1}}
        self.assertFalse(runner.correction_allowed(status, ledger, chapter))
        status["operator_correction_limits"] = {unit: 9}
        status["operator_review_limits"] = {unit: 12}
        self.assertTrue(runner.correction_allowed(status, ledger, chapter))
        self.assertEqual(runner.operator_unit_limit(
            status, "review", unit, runner.MAX_ACCEPTED_REVIEWS_PER_UNIT), 12)
        self.assertEqual(runner.operator_unit_limit(
            status, "review", "chapter-000022",
            runner.MAX_ACCEPTED_REVIEWS_PER_UNIT), runner.MAX_ACCEPTED_REVIEWS_PER_UNIT)
        status["correction_rounds"][unit] = 9
        self.assertFalse(runner.correction_allowed(status, ledger, chapter))
        status["operator_review_limits"][unit] = 0
        with self.assertRaises(runner.JobError):
            runner.operator_unit_limit(
                status, "review", unit, runner.MAX_ACCEPTED_REVIEWS_PER_UNIT)


if __name__ == "__main__":
    unittest.main()
