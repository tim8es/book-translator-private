"""Non-merge, no-prose real EPUB Auto batching and helper migration check."""
from __future__ import annotations
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".public-auto-runtime" / "scripts"))
sys.path.insert(0, str(ROOT / ".public-auto-runtime" / "automation"))
import book_runner
from workflow import structural_translation as helper

BOOK_SLUG = "say-it-in-your-mother-tongue"
BOOK = ROOT / "books" / BOOK_SLUG

class RealEpubBatchingDiagnostics(unittest.TestCase):
    def test_all_units_fit_existing_paid_call_cap(self):
        chapters = json.loads((BOOK / "progress.json").read_text("utf-8"))["chapters"]
        self.assertEqual(len(chapters), 54)
        total_spans = total_calls = max_chars = 0
        for chapter in chapters:
            content = (BOOK / chapter["source_path"]).read_text("utf-8")
            plan = book_runner.bounded_source_plan(content, helper)
            completed = {}
            while True:
                batch = helper.next_spans(
                    plan, completed, limit=book_runner.STRUCTURAL_MODEL_SEGMENTS_PER_CALL)
                if not batch:
                    break
                size = sum(len(x["source"]) for x in batch)
                self.assertLessEqual(size, helper.MAX_SOURCE_CHARS_PER_MODEL_CALL)
                self.assertLessEqual(len(batch), 24)
                max_chars = max(max_chars, size)
                total_calls += 1
                completed.update({part["id"]: part["source"] for part in batch})
            total_spans += len(completed)
            self.assertEqual(helper.render(plan, completed), content.rstrip() + "\n")
        self.assertLessEqual(total_calls + 54, 400)
        print("AUTO_BATCH_REAL_SOURCE_VERIFIED=" + json.dumps({
            "units": len(chapters), "spans": total_spans,
            "translator_batches": total_calls, "review_minimum": 54,
            "max_batch_chars": max_chars,
        }, sort_keys=True))

    def test_real_translation_stage_migrates_without_rewriting_original(self):
        chapters = json.loads((BOOK / "progress.json").read_text("utf-8"))["chapters"]
        chapter = chapters[0]
        original = (BOOK / ".workflow" / "auto-structural-translation" /
                    (chapter["unit_id"] + ".json"))
        self.assertTrue(original.is_file())
        before = json.loads(original.read_text("utf-8"))
        self.assertEqual(before["helper_revision"],
                         "d11a30b306a8bac236b73f25ae2f38e89745aab1")
        content = (BOOK / chapter["source_path"]).read_text("utf-8")
        plan = book_runner.bounded_source_plan(content, helper)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stage = (root / "books" / BOOK_SLUG / ".workflow" /
                     "auto-structural-translation" / original.name)
            stage.parent.mkdir(parents=True)
            shutil.copyfile(original, stage)
            status = {"workflow_revision": before["workflow_revision"]}
            with patch.object(book_runner, "ROOT", root):
                _, migrated = book_runner.load_structural_stage(
                    BOOK_SLUG, {"unit_id": chapter["unit_id"]}, status,
                    helper, plan)
            self.assertEqual(migrated["segments"], before["segments"])
            self.assertEqual(migrated["segment_plan_sha256"],
                             before["segment_plan_sha256"])
            self.assertEqual(migrated["source_sha256"], before["source_sha256"])
            self.assertEqual(migrated["helper_revision"],
                             book_runner.PUBLIC_STRUCTURAL_HELPER_REVISION)
            self.assertEqual(len(status["structural_helper_migrations"]), 1)
            print("AUTO_LIVE_STAGE_MIGRATION_VERIFIED=" + json.dumps({
                "persisted_segments": len(before["segments"]),
                "source_identity_unchanged": True,
            }, sort_keys=True))
