"""Workspace-level source-reference safety checks; no literary promotion."""
import hashlib
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
        # This test must work before AND after canonical book initialization.
        # The reference by itself is never equivalent to opening trusted source.
        self.assertEqual(report["missing_canonical_files"],
                         [p for p in migration.CANONICAL if not (BOOK / p).exists()])
        self.assertFalse(any(ch["status"] == "reviewed" for ch in report["chapters"]))
        self.assertEqual({item["chapter"] for item in report["chapters"]}.difference(range(1, 46)), set())
        print("THE_CLAIMING_MOON_REFERENCE_AUDIT=" + json.dumps({
            "numbered_chapters_with_any_draft": len(report["chapters"]),
            "reference_candidates": report.get("reference_candidates", 0),
            "needs_reconciliation": sum(x["status"] == "needs_reconciliation" for x in report["chapters"]),
            "not_canonically_reviewed": True
        }, sort_keys=True))

    def test_reference_alone_cannot_stage(self):
        staging = BOOK / "migration-staging"
        before_staging = {
            str(p.relative_to(staging)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in staging.rglob("*") if p.is_file()
        } if staging.exists() else {}
        protected = [BOOK / "progress.json", BOOK / "review-ledger.json"]
        before_state = {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in protected if p.exists()
        }
        report = migration.audit(BOOK, offset=2, source_reference=REFERENCE)
        with self.assertRaises(migration.MigrationError):
            migration.stage(BOOK, report, offset=2)
        after_staging = {
            str(p.relative_to(staging)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in staging.rglob("*") if p.is_file()
        } if staging.exists() else {}
        after_state = {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in protected if p.exists()
        }
        self.assertEqual(before_staging, after_staging)
        self.assertEqual(before_state, after_state)


if __name__ == "__main__":
    unittest.main()
