"""Contract tests for manifest-routed automatic literary prompts and memory."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "automation"))
import book_runner as runner
from literary_context import (MAX_SHARED_CHARS, full_shared_context,
                              parse_literary_review, parse_translation, role_contracts,
                              save_claim_bound_decisions, updated_glossary, updated_style)
from omniroute import ModelError


class LiteraryContextTests(unittest.TestCase):
    def engine(self, root: Path) -> Path:
        engine = root / "pinned"
        engine.mkdir()
        (engine / "docs").mkdir()
        contracts = {"global": "AGENTS.md", "translation": "docs/TRANSLATION.md",
                     "translator": "docs/TRANSLATOR.md", "reviewer": "docs/REVIEWER.md"}
        for role, path in contracts.items():
            dest = engine / path
            dest.write_text("pinned " + role, encoding="utf-8")
        (engine / "agent-manifest.json").write_text(json.dumps({
            "schema_version": 3, "contracts": contracts,
            "context_profiles": {
                "translator": ["global", "translation", "translator"],
                "reviewer": ["global", "translation", "reviewer"]},
            "context_overlays": {}}), encoding="utf-8")
        return engine

    def test_pinned_manifest_selects_only_role_contracts(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = self.engine(Path(tmp))
            translator, files = role_contracts(engine, "translator")
            self.assertEqual(files, ["AGENTS.md", "docs/TRANSLATION.md", "docs/TRANSLATOR.md"])
            self.assertIn("pinned translator", translator)
            self.assertNotIn("pinned reviewer", translator)
            reviewer, files = role_contracts(engine, "reviewer")
            self.assertIn("pinned reviewer", reviewer)
            self.assertNotIn("pinned translator", reviewer)

    def test_manifest_profile_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = self.engine(Path(tmp))
            manifest_path = engine / "agent-manifest.json"
            data = json.loads(manifest_path.read_text("utf-8"))
            data["context_profiles"]["translator"] = ["global"]
            manifest_path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required"):
                role_contracts(engine, "translator")

    def test_translator_returns_complete_artifact_and_decisions(self):
        obj = {"translation": "# Глава\n\nМара у двери.\n",
               "glossary": [{"original": "Mara", "translation": "Мара",
                             "type": "person", "notes": "Protagonist"}],
               "style_guide": [{"source_pattern": "restrained third-person",
                                "translation_approach": "keep simple narration",
                                "evidence": "first paragraph"}]}
        translation, glossary, style = parse_translation("```json\n" + json.dumps(obj, ensure_ascii=False) + "\n```")
        self.assertIn("Мара", translation)
        self.assertEqual(glossary[0]["original"], "Mara")
        self.assertEqual(style[0]["source_pattern"], "restrained third-person")
        for bad in ("only text", json.dumps({"translation": "Hi"})):
            with self.assertRaises(ModelError):
                parse_translation(bad)

    def test_review_requires_literary_decisions_field_and_actual_checks(self):
        review = {"outcome": "PASS", "checks": {
            "coverage": True, "meaning": True, "terminology": True,
            "style": True, "structure": True}, "findings": [],
            "style_guide": []}
        outcome, report, style = parse_literary_review(json.dumps(review))
        self.assertEqual(outcome, "PASS")
        self.assertEqual(style, [])
        self.assertTrue(report["checks"]["terminology"])
        del review["style_guide"]
        with self.assertRaises(ModelError):
            parse_literary_review(json.dumps(review))

    def test_glossary_append_is_idempotent_and_conflicts_fail(self):
        initial = "# Glossary\n\n| Original | Translation | Type | Notes |\n| --- | --- | --- | --- |\n"
        value = {"original": "Northbridge", "translation": "Нортбридж",
                 "type": "place", "notes": "Town"}
        first = updated_glossary(initial, [value])
        self.assertIn("| Northbridge | Нортбридж |", first)
        self.assertEqual(first, updated_glossary(first, [{**value, "notes": "Town, recurring"}]))
        with self.assertRaisesRegex(ValueError, "conflicting glossary"):
            updated_glossary(first, [{**value, "translation": "Северный мост"}])

    def test_style_is_idempotent(self):
        row = {"source_pattern": "dry dialogue", "translation_approach": "restrained",
               "evidence": "chapter one"}
        first = updated_style("# Style Guide\n", [row])
        self.assertEqual(first, updated_style(first, [row]))
        self.assertIn("Automated reviewed stylistic decisions", first)

    def test_shared_context_is_not_silently_truncated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            long_value = "N" * 25000
            (root / "glossary.md").write_text(long_value, encoding="utf-8")
            (root / "style-guide.md").write_text("style", encoding="utf-8")
            self.assertEqual(full_shared_context(root)[0], long_value)
            (root / "glossary.md").write_text("N" * (MAX_SHARED_CHARS + 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "refuse silent truncation"):
                full_shared_context(root)

    def test_runner_context_includes_pinned_instructions_and_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            engine = self.engine(root)
            book = root / "books" / "test"
            (book / "extracted").mkdir(parents=True)
            (book / "translated").mkdir()
            (book / "extracted" / "one.md").write_text("Mara walked home.", encoding="utf-8")
            (book / "translated" / "one.md").write_text("Мара вернулась домой.", encoding="utf-8")
            (book / "metadata.json").write_text('{"target_language": "ru", "title": "Test"}', encoding="utf-8")
            (book / "glossary.md").write_text("Mara = Мара", encoding="utf-8")
            (book / "style-guide.md").write_text("restrained narration", encoding="utf-8")
            chapter = {"unit_id": "chapter-000001", "source_path": "extracted/one.md",
                       "translation_path": "translated/one.md", "status": "translated"}
            with patch.object(runner, "ROOT", root), patch.object(
                    runner, "chapter_data", return_value=({}, {}, [chapter])):
                system, user, original = runner.context(engine, "test", chapter, "reviewer",
                    pending_style=[{"source_pattern": "short clauses",
                                    "translation_approach": "concise",
                                    "evidence": "chapter one"}])
            self.assertIn("pinned reviewer", system)
            self.assertNotIn("pinned translator", system)
            self.assertIn("Mara = Мара", user)
            self.assertIn("CURRENT ACCEPTED TRANSLATION", user)
            self.assertIn("short clauses", user)
            self.assertEqual(original, "Mara walked home.")

    def test_memory_only_correction_triggers_fresh_reviewer(self):
        chapter = {"unit_id": "chapter-000001", "number": 1, "status": "translated",
                   "translation_acceptance": {"translation_sha256": "a" * 64}}
        record = {"unit_id": "chapter-000001", "sequence": 1, "outcome": "CORRECTIONS_REQUIRED",
                  "translation_sha256": "a" * 64}
        with patch.object(runner, "chapter_data",
                          return_value=({}, {"records": [record]}, [chapter])), patch.object(
                          runner, "approved_unit_ids", return_value=set()):
            self.assertEqual(runner.next_operation("test", {"correction_rounds": {}})[0], "corrector")
            self.assertEqual(runner.next_operation("test", {
                "correction_rounds": {}, "memory_recheck_unit": "chapter-000001"})[0], "reviewer")

    def test_canonical_proposal_manager_persists_real_glossary_decision(self):
        from workflow.filesystem import FilesystemStorage
        from workflow.repository import WorkflowStateRepository
        from workflow.schemas import SchemaKind
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "books" / "test"
            book.mkdir(parents=True)
            (book / "glossary.md").write_text(
                "# Glossary\n\n| Original | Translation | Type | Notes |\n"
                "| --- | --- | --- | --- |\n", encoding="utf-8")
            (book / "style-guide.md").write_text("# Style guide\n", encoding="utf-8")
            storage = FilesystemStorage(book)
            repository = WorkflowStateRepository(storage)
            now = datetime.now(timezone.utc)
            claim = {
                "schema_version": 1, "claim_id": "a" * 32,
                "unit_id": "chapter-000001", "role": "translator",
                "session_id": "canonical-test-worker", "base_revision": "a" * 64,
                "base_commit": "b" * 40, "workflow_revision": "c" * 40,
                "shared_state_revisions": {
                    "glossary": hashlib.sha256((book / "glossary.md").read_bytes()).hexdigest(),
                    "style_guide": hashlib.sha256((book / "style-guide.md").read_bytes()).hexdigest()},
                "claimed_at": (now - timedelta(minutes=5)).isoformat(),
                "expires_at": (now + timedelta(minutes=30)).isoformat(),
            }
            repository.create(".workflow/claims/chapter-000001.json",
                              SchemaKind.CLAIM, claim)
            row = {"original": "Northbridge", "translation": "Нортбридж",
                   "type": "place", "notes": "Town name"}
            saved = save_claim_bound_decisions(book, "chapter-000001",
                                              "canonical-test-worker", "glossary", [row])
            self.assertEqual(saved, 1)
            self.assertIn("| Northbridge | Нортбридж |",
                          (book / "glossary.md").read_text("utf-8"))
            self.assertEqual(save_claim_bound_decisions(
                book, "chapter-000001", "canonical-test-worker", "glossary", [row]), 0)
            proposals = list((book / ".workflow" / "proposals").glob("*.json"))
            self.assertEqual(len(proposals), 2)
            self.assertEqual(sum(path.name.endswith(".resolution.json") for path in proposals), 1)

    def test_dispatch_follows_pinned_canonical_resume(self):
        chapter = {"unit_id": "chapter-000001", "number": 1, "status": "extracted"}
        ledger = {"records": []}
        with patch.object(runner, "chapter_data", return_value=({}, ledger, [chapter])), \
             patch.object(runner, "approved_unit_ids", return_value=set()), \
             patch.object(runner, "cli") as cli:
            for operation, expected in (
                ("translate", "translator"), ("review", "reviewer"),
                ("correct_translation", "corrector"), ("accept_review", "promote")
            ):
                cli.return_value = json.dumps({
                    "operation": operation, "unit_id": "chapter-000001",
                    "chapter_number": 1})
                role, selected = runner.canonical_dispatch("test", {"correction_rounds": {}})
                self.assertEqual(role, expected)
                self.assertEqual(selected, chapter)
            cli.return_value = json.dumps({"operation": "complete"})
            self.assertEqual(runner.canonical_dispatch("test", {})[0], "finalize")
            cli.return_value = json.dumps({"operation": "blocked", "reason": "unit_claimed"})
            with self.assertRaisesRegex(runner.JobError, "unit_claimed"):
                runner.canonical_dispatch("test", {})

    def test_claim_includes_frozen_literary_revisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book = root / "books" / "test"
            book.mkdir(parents=True)
            (book / "glossary.md").write_text("glossary", encoding="utf-8")
            (book / "style-guide.md").write_text("style", encoding="utf-8")
            with patch.object(runner, "ROOT", root), patch.object(
                runner, "git", return_value="a" * 40), patch.object(
                runner, "cli") as cli, patch.object(runner, "checkpoint"):
                runner.claim("f" * 32, "test", {}, "translator", {"number": 1})
            args = cli.call_args.args
            self.assertIn("--base-commit", args)
            self.assertEqual(args[args.index("--glossary-revision") + 1],
                             hashlib.sha256(b"glossary").hexdigest())
            self.assertEqual(args[args.index("--style-guide-revision") + 1],
                             hashlib.sha256(b"style").hexdigest())


if __name__ == "__main__":
    unittest.main()
