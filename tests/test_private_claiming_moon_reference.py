"""A metadata-only source reference must never authorize draft staging.

These tests use disposable fixtures rather than assuming that the real
The Claiming Moon workspace will remain uninitialized forever.
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "migrate_intake.py"
spec = importlib.util.spec_from_file_location("migrate_intake_reference", SCRIPT)
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)
REFERENCE = ROOT / "docs" / "migrations" / "the-claiming-moon-source-reference.json"
ORIGINAL_SHA = "611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb"


class ClaimingMoonSourceReferenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.book = Path(self.tmp.name) / "books" / "the-claiming-moon"
        (self.book / "incoming").mkdir(parents=True)
        (self.book / "INTAKE.md").write_text(
            "Original EPUB SHA-256: " + ORIGINAL_SHA + "\n", encoding="utf-8"
        )
        (self.book / "incoming" / "chapter-001-ru-draft.md").write_text(
            "# Draft only\n", encoding="utf-8"
        )

    def test_metadata_only_reference_never_verifies_original(self):
        source = json.loads(REFERENCE.read_text(encoding="utf-8"))
        self.assertEqual(source["source_units"], 48)
        self.assertEqual(len(source["spine"]), 48)
        self.assertEqual(source["source_sha256"], ORIGINAL_SHA)
        report = migration.audit(self.book, offset=2, source_reference=REFERENCE)
        self.assertTrue(report["source_map_loaded"])
        self.assertFalse(report["source_verified"])
        self.assertEqual(report["source_units"], 48)
        self.assertEqual(report["reviewed_promotions"], 0)
        self.assertTrue(report["blockers"])
        self.assertIn("metadata.json", report["missing_canonical_files"])
        self.assertEqual([chapter["chapter"] for chapter in report["chapters"]], [1])

    def test_reference_only_cannot_stage_without_verified_binary(self):
        report = migration.audit(self.book, offset=2, source_reference=REFERENCE)
        before = (self.book / "incoming/chapter-001-ru-draft.md").read_bytes()
        with self.assertRaises(migration.MigrationError):
            migration.stage(self.book, report, offset=2)
        self.assertFalse((self.book / "migration-staging").exists())
        self.assertEqual(
            (self.book / "incoming/chapter-001-ru-draft.md").read_bytes(), before
        )


if __name__ == "__main__":
    unittest.main()
