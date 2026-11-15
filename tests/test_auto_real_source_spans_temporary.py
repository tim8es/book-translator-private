"""Non-merge diagnostic: validate every real-book structural text span.

This logs only counts and hashes; no source prose, translation or EPUB bytes.
"""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".public-auto-runtime" / "scripts"))
sys.path.insert(0, str(ROOT / ".public-auto-runtime" / "automation"))

import book_runner
from workflow import structural_translation as helper


class RealSourceStructuralPreflight(unittest.TestCase):
    def test_all_54_extracted_chapters_reassemble_losslessly(self):
        book = ROOT / "books" / "say-it-in-your-mother-tongue"
        progress = json.loads((book / "progress.json").read_text("utf-8"))
        self.assertEqual(len(progress["chapters"]), 54)
        total = 0
        max_length = 0
        marker_count = 0
        for chapter in progress["chapters"]:
            content = (book / chapter["source_path"]).read_text("utf-8")
            planned = book_runner.bounded_source_plan(content, helper)
            self.assertEqual(planned["source_sha256"],
                             hashlib.sha256(content.encode("utf-8")).hexdigest())
            spans = helper.spans(planned)
            self.assertTrue(spans)
            self.assertTrue(all(
                0 < len(item["source"]) <= book_runner.SOURCE_SPAN_CHAR_LIMIT
                for item in spans))
            self.assertTrue(all("<!-- bt-" not in item["source"] for item in spans))
            rebuilt = helper.render(
                planned, {part["id"]: part["source"] for part in spans})
            self.assertEqual(rebuilt, content.rstrip() + "\n")
            book_runner.check_markers(content, rebuilt)
            total += len(spans)
            max_length = max(max_length, *(len(part["source"]) for part in spans))
            marker_count += sum(p["kind"] == "epub_marker"
                                for p in planned["parts"])
        print("REAL_AUTO_STRUCTURAL_PLAN_OK " + json.dumps({
            "units": len(progress["chapters"]),
            "source_spans": total,
            "max_span_chars": max_length,
            "protected_markers": marker_count,
            "helper_revision": book_runner.PUBLIC_STRUCTURAL_HELPER_REVISION,
        }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
