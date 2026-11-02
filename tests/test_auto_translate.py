"""Safety and contract checks for the optional private-only automated runtime."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "automation"))
import book_runner as worker
from omniroute import ModelError, config, parse_review


class AutomatedBookTests(unittest.TestCase):
    def test_checkpoint_keeps_pinned_engine_and_stages_only_job_and_book(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'automation' / 'status').mkdir(parents=True)
            (root / 'scripts').mkdir()
            marker = root / '.book-translator-install.json'
            marker.write_text('pinned', encoding='utf-8')
            calls = []
            def fake_git(*args):
                calls.append(args)
                if args[0] == 'restore':
                    marker.write_text('default', encoding='utf-8')
                return ''
            with patch.object(worker, 'ROOT', root), patch.object(worker, 'git', side_effect=fake_git):
                worker.checkpoint('a' * 32, {'phase': 'matched'}, 'book')
            self.assertEqual(marker.read_text(encoding='utf-8'), 'pinned')
            self.assertIn(('add', '-A', '--', 'books/book', 'automation/status/' + 'a' * 32 + '.json'), calls)

    def test_disjoint_checkpoint_replays_without_touching_active_checkout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def cmd(*args):
                return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
            cmd("init", "-q", "-b", "main")
            cmd("config", "user.name", "Test Agent")
            cmd("config", "user.email", "test-agent@example.test")
            (root / "books" / "our-book").mkdir(parents=True)
            (root / "books" / "our-book" / "chapter.md").write_text(
                "base", encoding="utf-8")
            cmd("add", "-A")
            cmd("commit", "-qm", "base")
            base = cmd("rev-parse", "HEAD")
            (root / "books" / "our-book" / "chapter.md").write_text(
                "our approved translation", encoding="utf-8")
            cmd("add", "-A")
            cmd("commit", "-qm", "our checkpoint")
            local = cmd("rev-parse", "HEAD")
            # A pinned engine in a real runner can leave unstaged local scripts.
            (root / "ephemeral-engine.py").write_text(
                "pinned version", encoding="utf-8")
            cmd("checkout", "-qb", "other-agent", base)
            (root / "books" / "another-book").mkdir(parents=True)
            (root / "books" / "another-book" / "chapter.md").write_text(
                "their unrelated translation", encoding="utf-8")
            cmd("add", "-A")
            cmd("commit", "-qm", "another book")
            remote = cmd("rev-parse", "HEAD")
            cmd("checkout", "-q", "main")
            with patch.object(worker, "ROOT", root):
                merged = worker.replay_disjoint_checkpoint(
                    base, local, remote, ["books/our-book"])
            self.assertEqual(cmd("rev-parse", merged + "^"), remote)
            self.assertEqual(cmd("show", merged + ":books/our-book/chapter.md"),
                             "our approved translation")
            self.assertEqual(cmd("show", merged + ":books/another-book/chapter.md"),
                             "their unrelated translation")
            self.assertEqual(cmd("rev-parse", "HEAD"), local)
            self.assertEqual((root / "ephemeral-engine.py").read_text("utf-8"),
                             "pinned version")
            # A concurrent edit to the SAME book must never be replayed.
            cmd("checkout", "-qb", "conflicting-agent", base)
            (root / "books" / "our-book" / "chapter.md").write_text(
                "conflicting agent edit", encoding="utf-8")
            cmd("add", "-A")
            cmd("commit", "-qm", "conflicting work")
            conflicting = cmd("rev-parse", "HEAD")
            with patch.object(worker, "ROOT", root):
                with self.assertRaisesRegex(worker.JobError, "remote changed this job"):
                    worker.replay_disjoint_checkpoint(
                        base, local, conflicting, ["books/our-book"])

    def test_disjoint_checkpoint_rejects_rewritten_history(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def cmd(*args):
                return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
            cmd("init", "-q", "-b", "main")
            cmd("config", "user.name", "Test Agent")
            cmd("config", "user.email", "test-agent@example.test")
            (root / "base.txt").write_text("base", encoding="utf-8")
            cmd("add", "-A")
            cmd("commit", "-qm", "base")
            base = cmd("rev-parse", "HEAD")
            (root / "other.txt").write_text("local", encoding="utf-8")
            cmd("add", "-A")
            cmd("commit", "-qm", "local")
            local = cmd("rev-parse", "HEAD")
            # An unrelated root commit is not a safe fast-forward upstream.
            cmd("checkout", "--orphan", "rewritten")
            cmd("rm", "-q", "-rf", ".")
            (root / "replacement.txt").write_text("unrelated", encoding="utf-8")
            cmd("add", "-A")
            cmd("commit", "-qm", "replaced history")
            rewritten = cmd("rev-parse", "HEAD")
            with patch.object(worker, "ROOT", root):
                with self.assertRaisesRegex(worker.JobError, "upstream history diverged"):
                    worker.replay_disjoint_checkpoint(
                        base, local, rewritten, ["other.txt"])

    def test_user_approved_exact_artifacts_skip_repeat_review_but_new_unit_does_not(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            book = root / "books" / "approved-book"
            (book / "extracted").mkdir(parents=True)
            (book / "translated").mkdir()
            source, translated = b"original text", "перевод".encode()
            (book / "extracted" / "one.md").write_bytes(source)
            (book / "translated" / "one.md").write_bytes(translated)
            item = {"unit_id": "chapter-000001", "number": 1, "status": "translated",
                    "source_path": "extracted/one.md", "translation_path": "translated/one.md",
                    "translation_acceptance": {"source_sha256": hashlib.sha256(source).hexdigest(),
                                               "translation_sha256": hashlib.sha256(translated).hexdigest()}}
            worker.store_json(book / "progress.json", {"chapters": [item]})
            worker.store_json(book / "review-ledger.json", {"records": []})
            approvals = root / "automation" / "user-approvals" / "approved-book.json"
            approvals.parent.mkdir(parents=True)
            worker.store_json(approvals, {"schema_version": 1, "book_slug": "approved-book",
                "approved_by": "user", "approved_at": "2026-11-02T10:53:13Z",
                "workflow_revision": "a" * 40, "units": [{"unit_id": item["unit_id"],
                **item["translation_acceptance"]}]})
            with patch.object(worker, "ROOT", root):
                self.assertEqual(worker.next_operation("approved-book", {"correction_rounds": {}})[0], "finalize")
                new = {"unit_id": "chapter-000002", "number": 2, "status": "extracted"}
                worker.store_json(book / "progress.json", {"chapters": [item, new]})
                self.assertEqual(worker.next_operation("approved-book", {"correction_rounds": {}}), ("translator", new))
                (book / "translated" / "one.md").write_text("changed", encoding="utf-8")
                worker.store_json(book / "progress.json", {"chapters": [item]})
                self.assertEqual(worker.next_operation("approved-book", {"correction_rounds": {}})[0], "reviewer")
                (book / "translated" / "one.md").write_bytes(translated)
                (book / "extracted" / "one.md").write_bytes(b"changed source")
                self.assertEqual(worker.next_operation("approved-book", {"correction_rounds": {}})[0], "reviewer")

    def test_user_approved_output_remains_labelled_as_not_independently_reviewed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            book = root / "books" / "approved-book"
            book.mkdir(parents=True)
            output = book / "output"
            output.mkdir()
            artifact = output / "approved-book.epub"
            artifact.write_bytes(b"PK\x03\x04approved")
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            worker.store_json(output / "manifest.json", {"preview": True, "format": "epub",
                "artifact_path": "output/approved-book.epub", "artifact_sha256": digest})
            status = {"state": "running", "correction_rounds": {}}
            chapters = [{"unit_id": "chapter-000001", "status": "translated"}]
            with patch.object(worker, "ROOT", root), patch.object(worker, "verify"), \
                 patch.object(worker, "chapter_data", return_value=({}, {"records": []}, chapters)), \
                 patch.object(worker, "approved_unit_ids", return_value={"chapter-000001"}), \
                 patch.object(worker, "cli", side_effect=[json.dumps({"errors": [], "claims": [], "finalization": {"active": False}}),
                                                           json.dumps({"pending": []}), ""]) as cli, \
                 patch.object(worker, "checkpoint"):
                worker.finalize("a" * 32, "approved-book", status)
            self.assertEqual(cli.call_args.args, ("build", "approved-book", "--format", "epub", "--allow-unreviewed"))
            self.assertEqual(status["state"], "done")
            self.assertEqual(status["review_provenance"], "user-approved-unreviewed")

    def test_unapproved_translated_unit_cannot_use_user_approved_preview(self):
        with tempfile.TemporaryDirectory() as folder:
            chapters = [{"unit_id": "chapter-000001", "status": "translated"},
                        {"unit_id": "chapter-000002", "status": "translated"}]
            with patch.object(worker, "ROOT", Path(folder)), patch.object(worker, "verify"), \
                 patch.object(worker, "chapter_data", return_value=({}, {"records": []}, chapters)), \
                 patch.object(worker, "approved_unit_ids", return_value={"chapter-000001"}), \
                 patch.object(worker, "cli") as cli:
                with self.assertRaisesRegex(worker.JobError, "lack current user approval"):
                    worker.finalize("a" * 32, "approved-book", {"state": "running"})
                cli.assert_not_called()

    def test_user_approval_never_overrides_recorded_reviewer_findings(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            book = root / "books" / "approved-book"
            book.mkdir(parents=True)
            chapter = {"unit_id": "chapter-000001", "number": 1, "status": "translated",
                       "translation_acceptance": {"translation_sha256": "a" * 64}}
            worker.store_json(book / "progress.json", {"chapters": [chapter]})
            worker.store_json(book / "review-ledger.json", {"records": [{"unit_id": chapter["unit_id"],
                "sequence": 1, "outcome": "CORRECTIONS_REQUIRED", "translation_sha256": "a" * 64}]})
            with patch.object(worker, "ROOT", root), patch.object(worker, "approved_unit_ids", return_value={chapter["unit_id"]}):
                self.assertEqual(worker.next_operation("approved-book", {"correction_rounds": {}})[0], "corrector")
    def test_reconciled_history_guard_detects_changes_and_lost_progress(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            book = root / "books" / "stable-title"
            history = book / "source-updates" / "2026-10-11"
            history.mkdir(parents=True)
            (history / "translation.md").write_bytes(b"historical translation\n")
            rev = "a" * 40
            unit = {"unit_id": "chapter-000001", "status": "translated",
                    "translation_acceptance": {"translation_sha256": "b" * 64}}
            worker.store_json(book / "progress.json", {"chapters": [unit]})
            worker.store_json(book / "source-manifest.json", {
                "extracted": [{"unit_id": unit["unit_id"], "sha256": "c" * 64}]})
            snapshot = book / "source-revisions" / "source-000002" / "revision.json"
            worker.store_json(snapshot, {
                "revision_id": "source-000002", "metadata": {"source": {"sha256": "d" * 64}},
                "source_manifest": {"extracted": [{"unit_id": unit["unit_id"], "sha256": "c" * 64}]}})
            worker.store_json(book / "source-revisions.json", {"revisions": [{
                "revision_id": "source-000002", "source_sha256": "d" * 64,
                "snapshot_path": "source-revisions/source-000002/revision.json"}]})
            metadata = {"workflow": {"resolved_revision": rev}}
            worker.store_json(book / "automation-reconciliation.json", {
                "schema_version": 1, "workflow_revision": rev, "revision_id": "source-000002",
                "source_sha256": "d" * 64, "history_sha256": worker.history_digest(book / "source-updates"),
            })
            worker.verify_legacy_reconciliation(book, metadata)
            (history / "translation.md").write_bytes(b"changed history\n")
            with self.assertRaisesRegex(worker.BookIdentityError, "staged source updates"):
                worker.verify_legacy_reconciliation(book, metadata)
            (history / "translation.md").write_bytes(b"historical translation\n")
            unit["status"] = "extracted"
            worker.store_json(book / "progress.json", {"chapters": [unit]})
            with self.assertRaisesRegex(worker.BookIdentityError, "staged source updates"):
                worker.verify_legacy_reconciliation(book, metadata)
            worker.store_json(book / "source-manifest.json", {
                "extracted": [{"unit_id": unit["unit_id"], "sha256": "e" * 64}]})
            worker.verify_legacy_reconciliation(book, metadata)
    @staticmethod
    def make_epub(path: Path, title: str, author: str = "Author", chapter: str = "<p>Chapter</p>") -> None:
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
            archive.writestr("META-INF/container.xml", '<container><rootfiles><rootfile full-path="EPUB/package.opf"/></rootfiles></container>')
            archive.writestr("EPUB/package.opf", f'<package xmlns:dc="http://purl.org/dc/elements/1.1/"><metadata><dc:title>{title}</dc:title><dc:creator>{author}</dc:creator></metadata></package>')
            archive.writestr("EPUB/chapter.xhtml", chapter)

    def test_book_identity_reuses_workspace_by_title_and_filename(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            book = root / "books" / "the-same-book"
            book.mkdir(parents=True)
            worker.store_json(book / "metadata.json", {
                "title": "The Same Book", "author": "Writer",
                "source_file": "edition.epub", "target_language": "ru",
            })
            with patch.object(worker, "ROOT", root):
                self.assertEqual(worker.locate_book("the same book", "Writer", "new.epub", "ru")[0], "the-same-book")
                self.assertEqual(worker.locate_book("Different title", "Writer", "edition.epub", "ru")[0], "the-same-book")

    def test_book_identity_blocks_ambiguous_titles_and_language_mismatch(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for slug, language in (("same-a", "ru"), ("same-b", "ru")):
                book = root / "books" / slug
                book.mkdir(parents=True)
                worker.store_json(book / "metadata.json", {
                    "title": "Same Title", "author": "Writer", "target_language": language,
                })
            with patch.object(worker, "ROOT", root):
                with self.assertRaisesRegex(worker.BookIdentityError, "multiple distinct editions"):
                    worker.locate_book("Same Title", "Writer", "new.epub", "ru")
            shutil.rmtree(root / "books" / "same-b")
            with patch.object(worker, "ROOT", root):
                with self.assertRaisesRegex(worker.BookIdentityError, "different target language"):
                    worker.locate_book("Same Title", "Writer", "new.epub", "en")

    def test_duplicate_workspaces_for_same_edition_resolve_to_latest_book(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for slug, imported in (("auto-old", "2026-01-01T00:00:00Z"), ("auto-new", "2026-02-01T00:00:00Z")):
                book = root / "books" / slug
                book.mkdir(parents=True)
                worker.store_json(book / "metadata.json", {
                    "title": "Same Title", "author": "Writer", "target_language": "ru",
                    "imported_at": imported, "source": {"sha256": "a" * 64},
                    "workflow": {"resolved_revision": "b" * 40},
                })
            with patch.object(worker, "ROOT", root):
                self.assertEqual(worker.locate_book("Same Title", "Writer", "same.epub", "ru")[0], "auto-new")
                newer = root / "books" / "auto-new" / "metadata.json"
                value = worker.read_json(newer)
                value["source"]["sha256"] = "c" * 64
                worker.store_json(newer, value)
                with self.assertRaisesRegex(worker.BookIdentityError, "multiple distinct editions"):
                    worker.locate_book("Same Title", "Writer", "same.epub", "ru")

    def test_epub_identity_reads_package_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.epub"
            self.make_epub(path, "A New Book", "A Writer")
            self.assertEqual(worker.epub_identity(path), ("A New Book", "A Writer"))

    def test_same_edition_resumes_existing_book_without_translation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            job = "b" * 32
            source_dir = root / "intake" / "auto" / job
            source_dir.mkdir(parents=True)
            source = source_dir / "source.epub"
            self.make_epub(source, "Stable Title", "Writer")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            worker.store_json(source_dir / "request.json", {
                "schema_version": 1, "job_id": job, "source_sha256": digest,
                "target_language": "ru", "source_filename": "stable-title.epub",
            })
            book = root / "books" / "stable-title"
            book.mkdir(parents=True)
            worker.store_json(book / "metadata.json", {
                "title": "Stable Title", "author": "Writer", "target_language": "ru",
                "source": {"sha256": digest},
                "workflow": {"resolved_revision": "a" * 40},
            })
            engine = root / "engine"
            engine.mkdir()
            with patch.object(worker, "ROOT", root), \
                 patch.object(worker, "install_engine", return_value=(engine, "a" * 40)), \
                 patch.object(worker, "verify"), \
                 patch.object(worker, "checkpoint"), \
                 patch.object(worker, "canonical_dispatch", return_value=("finalize", None)), \
                 patch.object(worker, "finalize", side_effect=lambda _job, _slug, status: status.update({"state": "done", "phase": "delivered"})) as finalize, \
                 patch.object(worker, "claim") as claim:
                status = worker.run(job)
            self.assertEqual(finalize.call_args.args[1], "stable-title")
            claim.assert_not_called()
            self.assertEqual(status["book_slug"], "stable-title")

    def test_new_edition_uses_canonical_source_update_in_same_workspace(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            job = "c" * 32
            source_dir = root / "intake" / "auto" / job
            source_dir.mkdir(parents=True)
            source = source_dir / "source.epub"
            self.make_epub(source, "Stable Title", "Writer", "<p>Changed chapter</p>")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            worker.store_json(source_dir / "request.json", {
                "schema_version": 1, "job_id": job, "source_sha256": digest,
                "target_language": "ru", "source_filename": "stable-title.epub",
            })
            book = root / "books" / "stable-title"
            book.mkdir(parents=True)
            worker.store_json(book / "metadata.json", {
                "title": "Stable Title", "author": "Writer", "target_language": "ru",
                "source": {"sha256": "0" * 64},
                "workflow": {"resolved_revision": "a" * 40},
            })
            engine = root / "engine"
            engine.mkdir()
            with patch.object(worker, "ROOT", root), \
                 patch.object(worker, "install_engine", return_value=(engine, "a" * 40)), \
                 patch.object(worker, "verify"), \
                 patch.object(worker, "checkpoint"), \
                 patch.object(worker, "cli", return_value=json.dumps({"state": "promoted"})) as cli, \
                 patch.object(worker, "canonical_dispatch", return_value=("translator", {"number": 6})), \
                 patch.object(worker, "claim") as claim:
                status = worker.run(job)
            self.assertEqual(status["book_slug"], "stable-title")
            self.assertEqual(cli.call_args_list[0].args[:2], ("update-source", "stable-title"))
            self.assertEqual(cli.call_args_list[1].args,
                             ("source-coverage", "stable-title", "--source", str(source),
                              "--record", "--replace-stale", "--json"))
            self.assertEqual(claim.call_args.args[1], "stable-title")

    def test_staged_legacy_translation_blocks_before_dispatch(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            job = "d" * 32
            intake = root / "intake" / "auto" / job
            intake.mkdir(parents=True)
            source = intake / "source.epub"
            self.make_epub(source, "Stable Title", "Writer")
            worker.store_json(intake / "request.json", {
                "schema_version": 1, "job_id": job,
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "target_language": "ru", "source_filename": "book.epub",
            })
            book = root / "books" / "stable-title"
            (book / "source-updates" / "2026-10-11").mkdir(parents=True)
            (book / "source-updates" / "2026-10-11" / "README.md").write_text("staged translation")
            worker.store_json(book / "metadata.json", {
                "title": "Stable Title", "author": "Writer", "target_language": "ru",
                "workflow": {"resolved_revision": "a" * 40},
            })
            with patch.object(worker, "ROOT", root), patch.object(worker, "install_engine") as install:
                with self.assertRaisesRegex(worker.BookIdentityError, "staged source updates"):
                    worker.run(job)
                install.assert_not_called()

    def test_failed_coverage_blocks_claim_after_source_update(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            job = "e" * 32
            intake = root / "intake" / "auto" / job
            intake.mkdir(parents=True)
            source = intake / "source.epub"
            self.make_epub(source, "Stable Title", "Writer")
            worker.store_json(intake / "request.json", {
                "schema_version": 1, "job_id": job,
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "target_language": "ru", "source_filename": "book.epub",
            })
            book = root / "books" / "stable-title"
            book.mkdir(parents=True)
            worker.store_json(book / "metadata.json", {
                "title": "Stable Title", "author": "Writer", "target_language": "ru",
                "source": {"sha256": "0" * 64},
                "workflow": {"resolved_revision": "a" * 40},
            })
            engine = root / "engine"
            engine.mkdir()
            with patch.object(worker, "ROOT", root), \
                 patch.object(worker, "install_engine", return_value=(engine, "a" * 40)), \
                 patch.object(worker, "verify"), patch.object(worker, "checkpoint"), \
                 patch.object(worker, "cli", side_effect=[json.dumps({"state": "promoted"}), worker.JobError("coverage failed")]), \
                 patch.object(worker, "claim") as claim:
                with self.assertRaisesRegex(worker.JobError, "coverage failed"):
                    worker.run(job)
                claim.assert_not_called()

    def test_strict_review_blocks_unresolved_findings(self):
        payload = {
            "outcome": "PASS",
            "checks": dict.fromkeys(("coverage", "meaning", "terminology", "style", "structure"), True),
            "findings": [{"severity": "major", "detail": "Omission", "resolved": False}],
        }
        with self.assertRaises(ModelError):
            parse_review(json.dumps(payload))
        payload["outcome"] = "CORRECTIONS_REQUIRED"
        outcome, report = parse_review(json.dumps(payload))
        self.assertEqual(outcome, "CORRECTIONS_REQUIRED")
        self.assertEqual(report["context"], "independent_session")

    def test_reviewer_must_complete_all_checks(self):
        payload = {
            "outcome": "PASS",
            "checks": dict.fromkeys(("coverage", "meaning", "terminology", "style", "structure"), True),
            "findings": [],
        }
        payload["checks"]["coverage"] = False
        with self.assertRaises(ModelError):
            parse_review(json.dumps(payload))
        payload["checks"]["coverage"] = True
        self.assertEqual(parse_review(json.dumps(payload))[0], "PASS")

    def test_model_endpoint_requires_https_and_configured_role(self):
        with patch.dict(os.environ, {
            "OMNIROUTE_BASE_URL": "http://example.com/v1",
            "OMNIROUTE_API_KEY": "test-placeholder",
            "OMNIROUTE_TRANSLATOR_MODEL": "test-model",
        }):
            with self.assertRaises(ModelError):
                config("TRANSLATOR")
        with self.assertRaises(ModelError):
            config("UNKNOWN")

    def test_markers_are_order_and_identity_bound(self):
        source = "<!-- bt-block:000001 -->\nFirst [link](#x)\n<!-- bt-block:000002 -->\n"
        worker.check_markers(source, "<!-- bt-block:000001 -->\nПервый [ссылка](#x)\n<!-- bt-block:000002 -->\n")
        with self.assertRaises(worker.JobError):
            worker.check_markers(source, "<!-- bt-block:000002 -->\nПервый [ссылка](#x)\n<!-- bt-block:000001 -->\n")
        with self.assertRaises(worker.JobError):
            worker.check_markers(source, "<!-- bt-block:000001 -->\nПервый [ссылка](#y)\n<!-- bt-block:000002 -->\n")

    def test_scheduler_skips_blocked_and_unreadable_statuses(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            ids = ["0" * 32, "1" * 32, "2" * 32, "3" * 32]
            for job_id in ids:
                request = root / "intake" / "auto" / job_id / "request.json"
                request.parent.mkdir(parents=True)
                request.write_text("{}", encoding="utf-8")
            worker.store_json(root / "automation" / "status" / (ids[0] + ".json"),
                              {"state": "blocked"})
            bad = root / "automation" / "status" / (ids[1] + ".json")
            bad.write_text("{invalid", encoding="utf-8")
            worker.store_json(root / "automation" / "status" / (ids[2] + ".json"),
                              {"state": "done"})
            with patch.object(worker, "ROOT", root):
                self.assertEqual(worker.select(None), ids[3])
                # Explicit attempts remain operator-controlled and are never
                # silently redirected to another request.
                self.assertEqual(worker.select(ids[0]), ids[0])
            worker.store_json(root / "automation" / "status" / (ids[3] + ".json"),
                              {"state": "blocked"})
            with patch.object(worker, "ROOT", root):
                self.assertEqual(worker.select(None), "")

    def test_quarantine_failure_preserves_claim_without_staging_book(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            job_id = "f" * 32
            slug = "existing-book"
            book = root / "books" / slug
            book.mkdir(parents=True)
            (book / "translated.md").write_text("uncommitted mutation", encoding="utf-8")
            worker.store_json(root / "automation" / "status" / (job_id + ".json"),
                              {"job_id": job_id, "book_slug": slug, "state": "running",
                               "phase": "claimed", "model_calls_started": 3,
                               "active": {"role": "reviewer", "session_id": "owner"}})
            calls = []
            def fake_git(*args):
                calls.append(args)
                if args[:2] in (("rev-parse", "HEAD"), ("rev-parse", "origin/main")):
                    return "a" * 40
                if args[:2] == ("diff", "--cached"):
                    # No staged changes prior to status quarantine; the newly
                    # staged status is the only staged path after git add.
                    if sum(call[:2] == ("diff", "--cached") for call in calls) == 1:
                        return ""
                    return "automation/status/" + job_id + ".json"
                return ""
            with patch.object(worker, "ROOT", root), \
                 patch.object(worker, "git", side_effect=fake_git):
                status = worker.block_on_unexpected_failure(
                    job_id, worker.JobError("source coverage blocked"))
            self.assertEqual(status["state"], "blocked")
            self.assertEqual(status["phase"], "operator-intervention-required")
            self.assertEqual(status["model_calls_started"], 3)
            self.assertEqual(status["active"]["session_id"], "owner")
            self.assertIn("claim", status["recovery_note"])
            self.assertEqual(worker.read_json(root / "automation" / "status" / (job_id + ".json"))["state"],
                             "blocked")
            self.assertIn(("add", "-A", "--", "automation/status/" + job_id + ".json"), calls)
            self.assertFalse(any(any("books/" in part for part in call) for call in calls))
            self.assertEqual((book / "translated.md").read_text("utf-8"), "uncommitted mutation")

    def test_status_quarantine_refuses_existing_staged_literary_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            job_id = "c" * 32
            with patch.object(worker, "ROOT", root), \
                 patch.object(worker, "git", return_value="books/other/chapter.md") as git:
                with self.assertRaisesRegex(worker.JobError, "staged changes"):
                    worker.block_on_unexpected_failure(job_id, worker.JobError("bad CLI"))
            self.assertFalse((root / "automation" / "status" / (job_id + ".json")).exists())
            self.assertEqual(git.call_args_list[0].args, ("diff", "--cached", "--name-only"))

    def test_main_records_preflight_failure_and_advances_queue(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            job_id = "e" * 32
            outputs = root / "github_outputs"
            with patch.object(worker, "ROOT", root), \
                 patch.object(worker, "run", side_effect=worker.JobError(
                     "EPUB source coverage blocked: unsupported semantic element <ol>")), \
                 patch.object(worker, "checkpoint") as checkpoint, \
                 patch.object(sys, "argv", ["book_runner.py", "--job-id", job_id]), \
                 patch.dict(os.environ, {"GITHUB_OUTPUT": str(outputs)}):
                self.assertEqual(worker.main(), 0)
            stored = checkpoint.call_args.args[1]
            self.assertEqual(stored["state"], "blocked")
            self.assertIn("unsupported semantic element <ol>", stored["last_error"])
            self.assertEqual(checkpoint.call_args.args[2], None)
            self.assertIn("continue_queue=true", outputs.read_text("utf-8"))
            self.assertNotIn("continue=true", outputs.read_text("utf-8"))

    def test_quarantine_failure_is_not_claimed_success_if_checkpoint_fails(self):
        with patch.object(worker, "run", side_effect=worker.JobError("failed")), \
             patch.object(worker, "block_on_unexpected_failure",
                          side_effect=worker.JobError("stale git head")), \
             patch.object(sys, "argv", ["book_runner.py", "--job-id", "d" * 32]):
            self.assertEqual(worker.main(), 1)

    def test_intake_hash_bound_and_source_filename_fixed(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(worker, "ROOT", Path(folder)):
                job_id = "a" * 32
                source_dir = worker.job_path(job_id)
                source_dir.mkdir(parents=True)
                source = b"PK\x03\x04test epub bytes"
                (source_dir / "source.epub").write_bytes(source)
                request = {"schema_version": 1, "job_id": job_id,
                           "target_language": "ru",
                           "source_sha256": hashlib.sha256(source).hexdigest()}
                worker.store_json(source_dir / "request.json", request)
                self.assertEqual(worker.request_for(job_id)["job_id"], job_id)
                self.assertEqual(worker.select(None), job_id)
                request["source_sha256"] = "0" * 64
                worker.store_json(source_dir / "request.json", request)
                with self.assertRaises(worker.JobError):
                    worker.request_for(job_id)

    def test_unexpected_intake_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(worker, "ROOT", Path(folder)):
                job_id = "a" * 32
                source_dir = worker.job_path(job_id)
                source_dir.mkdir(parents=True)
                source = b"PK\x03\x04test"
                (source_dir / "source.epub").write_bytes(source)
                request = {"schema_version": 1, "job_id": job_id,
                           "target_language": "ru",
                           "source_sha256": hashlib.sha256(source).hexdigest(),
                           "unexpected": True}
                worker.store_json(source_dir / "request.json", request)
                with self.assertRaisesRegex(worker.JobError, "invalid"):
                    worker.request_for(job_id)

    def test_next_step_requires_independent_review(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(worker, "ROOT", Path(folder)):
                slug = "auto-" + "a" * 32
                book = worker.ROOT / "books" / slug
                book.mkdir(parents=True)
                chapter = {
                    "unit_id": "chapter-000001", "number": 1, "status": "translated",
                    "translation_acceptance": {"translation_sha256": "a" * 64}
                }
                worker.store_json(book / "progress.json", {"chapters": [chapter]})
                worker.store_json(book / "review-ledger.json", {"records": []})
                status = {"correction_rounds": {}}
                self.assertEqual(worker.next_operation(slug, status)[0], "reviewer")
                worker.store_json(book / "review-ledger.json", {"records": [{
                    "unit_id": chapter["unit_id"], "sequence": 1, "outcome": "CORRECTIONS_REQUIRED",
                    "translation_sha256": "a" * 64}]})
                self.assertEqual(worker.next_operation(slug, status)[0], "corrector")
                status["correction_rounds"]["chapter-000001"] = worker.MAX_CORRECTIONS
                self.assertEqual(worker.next_operation(slug, status)[0], "blocked")


if __name__ == "__main__":
    unittest.main()
