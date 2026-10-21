"""Workspace-level source-reference safety checks; no literary promotion."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "migrate_intake.py"
spec = importlib.util.spec_from_file_location("migrate_intake_reference", SCRIPT)
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)
BOOK = ROOT / "books" / "the-claiming-moon"
REFERENCE = ROOT / "docs" / "migrations" / "the-claiming-moon-source-reference.json"


class ClaimingMoonSourceReferenceTests(unittest.TestCase):
    def test_metadata_only_audit_preserves_review_boundary(self):
        source = json.loads(REFERENCE.read_text(encoding="utf-8"))
        self.assertEqual(source["source_units"], 48)
        self.assertEqual(len(source["spine"]), 48)
        self.assertEqual(source["source_sha256"],
                         "611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb")
        report = migration.audit(BOOK, offset=2, source_reference=REFERENCE)
        self.assertTrue(report["source_map_loaded"])
        self.assertFalse(report["source_verified"])
        self.assertEqual(report["source_units"], 48)
        self.assertEqual(report["reviewed_promotions"], 0)
        self.assertTrue(report["blockers"])
        self.assertIn("metadata.json", report["missing_canonical_files"])
        self.assertEqual({item["chapter"] for item in report["chapters"]}.difference(range(1, 46)), set())
        print("THE_CLAIMING_MOON_REFERENCE_AUDIT=" + json.dumps({
            "numbered_chapters_with_any_draft": len(report["chapters"]),
            "reference_candidates": report.get("reference_candidates", 0),
            "needs_reconciliation": sum(x["status"] == "needs_reconciliation" for x in report["chapters"]),
            "not_canonically_reviewed": True
        }, sort_keys=True))

    def test_reference_alone_cannot_stage(self):
        report = migration.audit(BOOK, offset=2, source_reference=REFERENCE)
        with self.assertRaises(migration.MigrationError):
            migration.stage(BOOK, report, offset=2)
        self.assertFalse((BOOK / "migration-staging").exists())


if __name__ == "__main__":
    unittest.main()
