"""Deployment-only tests. Canonical business logic is tested in book-translator."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

STATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STATE / "automation"))
import runtime_loader


class StateOnlyDeploymentTests(unittest.TestCase):
    def test_runtime_sha_and_module_integrity(self):
        runtime_loader.verified_runtime("book_runner.py")
        for name in ("job_monitor.py", "actions_failure_notifier.py",
                     "verify_changed_books.py"):
            runtime_loader.verified_runtime(name)
        self.assertRegex(runtime_loader.pinned_revision(), r"^[0-9a-f]{40}$")

    def test_no_canonical_implementation_is_tracked(self):
        tracked = set(subprocess.check_output(
            ["git", "-C", str(STATE), "ls-files"], text=True).splitlines())
        self.assertFalse([x for x in tracked if x.startswith("scripts/")])
        self.assertFalse([x for x in tracked if x.startswith("docs/")
                          and not x.startswith("docs/migrations/")])
        for forbidden in ("AGENTS.md", "SKILL.md", "agent-manifest.json",
                          ".book-translator-install.json", "LICENSE"):
            self.assertNotIn(forbidden, tracked)
        for filename in ("book_runner.py", "literary_context.py", "omniroute.py",
                         "job_monitor.py", "actions_failure_notifier.py"):
            text = (STATE / "automation" / filename).read_text("utf-8")
            self.assertLess(len(text), 700)
            self.assertIn("load_shared_module", text)

    def test_workflows_are_generic_and_use_public_pins(self):
        root = STATE / ".github/workflows"
        names = {p.name for p in root.glob("*.yml")}
        self.assertEqual(names, {
            "auto-translate.yml", "book-batch-validation.yml",
            "book-job-monitor.yml", "chat-operations.yml", "final-epub.yml",
            "omniroute-json-smoke.yml", "tests.yml",
        })
        auto = (root / "auto-translate.yml").read_text("utf-8")
        self.assertIn("group: book-operation-", auto)
        self.assertIn("max-parallel: 3", auto)
        self.assertIn("Dispatch next bounded step", auto)
        self.assertNotIn("workflow_call:", auto)
        for filename in ("auto-translate.yml", "book-batch-validation.yml",
                         "book-job-monitor.yml", "omniroute-json-smoke.yml"):
            source = (root / filename).read_text("utf-8")
            self.assertIn("runtime_loader.py", source)
            self.assertIn("repository: tim8es/book-translator", source)
        chat = (root / "chat-operations.yml").read_text("utf-8")
        self.assertIn("runtime_loader.py --print-revision", chat)
        self.assertIn("engine_sha:", chat)
        self.assertIn("scripts/chat_ops_discover.py", chat)
        self.assertIn("scripts/chat_ops_bridge.py", chat)
        self.assertIn("group: book-operation-", chat)
        self.assertNotIn("ref: db27cc1a3369cd3e3da82e2dfe222af33a1f74e0", chat)
        epub = (root / "final-epub.yml").read_text("utf-8")
        self.assertIn(".pinned-book-translator", epub)
        self.assertIn("scripts/pinned_cli.py", epub)
        self.assertIn("python automation/runtime_loader.py --verify", epub)
        self.assertIn("group: book-operation-", epub)
        self.assertNotIn("git restore -- scripts", epub)
        self.assertNotIn("rm -rf scripts", epub)
        self.assertNotIn("cp -a .pinned-book-translator/scripts", epub)
        self.assertNotIn("cp -a .pinned-book-translator/docs", epub)
        self.assertNotIn("Path(\".book-translator-install.json\").write_text", epub)
        self.assertNotIn("private-deliver:", epub)
        self.assertIn('git add -A -- "books/$BOOK_SLUG"', epub)

    def test_changed_book_launcher_can_validate_empty_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "changed.json"
            manifest.write_text("[]", encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(STATE / ".github/scripts/verify_changed_books.py"),
                str(manifest),
            ], cwd=STATE, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Validated changed book files: 0", result.stdout)

    def test_final_epub_can_publish_with_ignored_engine_and_tracked_migrations(self):
        """No git restore pathspec and no deletion of durable migration evidence."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            remote, work = root / "remote.git", root / "book-state"

            def git(*args):
                result = subprocess.run(
                    ["git", *args], capture_output=True, text=True, check=True)
                return result.stdout.strip()

            git("init", "--bare", str(remote))
            git("clone", str(remote), str(work))
            git("-C", str(work), "checkout", "-b", "main")
            git("-C", str(work), "config", "user.name", "Test Operator")
            git("-C", str(work), "config", "user.email", "test@example.invalid")
            (work / ".gitignore").write_text(
                (STATE / ".gitignore").read_text("utf-8"), encoding="utf-8")
            archive = work / "docs/migrations/provenance.json"
            archive.parent.mkdir(parents=True)
            archive.write_text('{"book":"synthetic"}', encoding="utf-8")
            book = work / "books/synthetic-book"
            (book / "output").mkdir(parents=True)
            (book / "progress.json").write_text("initial", encoding="utf-8")
            git("-C", str(work), "add", "-A", "--", ".gitignore", "books")
            git("-C", str(work), "add", "-f", "--", "docs/migrations/provenance.json")
            git("-C", str(work), "commit", "-m", "seed state and evidence")
            git("-C", str(work), "push", "-u", "origin", "main")

            # Canonical code is loaded separately; state has no installation.
            engine = root / "public-engine"
            (engine / "scripts").mkdir(parents=True)
            (engine / "scripts/book.py").write_text("pinned", encoding="utf-8")
            (engine / "docs").mkdir()
            (engine / "docs/TRANSLATION.md").write_text(
                "review contract", encoding="utf-8")
            self.assertEqual(git("-C", str(work), "ls-files", "--", "scripts",
                                 ".book-translator-install.json"), "")
            for relative in ("scripts", ".book-translator-install.json",
                             "docs/TRANSLATION.md"):
                self.assertFalse((work / relative).exists(), relative)
            (book / "output/manifest.json").write_text(
                '{"format":"epub","preview":false}', encoding="utf-8")

            # Mirrors the deployment shell's staging and guarded push.
            shell = """
set -euo pipefail
if [[ -n "$(git ls-files -- scripts .book-translator-install.json)" ]]; then
  exit 17
fi
git add -A -- "books/$BOOK_SLUG"
if git diff --cached --quiet; then exit 19; fi
git fetch --quiet origin main
if ! git diff --quiet HEAD origin/main -- "books/$BOOK_SLUG"; then exit 21; fi
git commit -m "finalize($BOOK_SLUG): reviewed EPUB"
git rebase origin/main
git push origin HEAD:main
"""
            subprocess.run(["bash", "-c", shell], cwd=work, check=True,
                           env={**__import__("os").environ,
                                "BOOK_SLUG": "synthetic-book"})
            self.assertEqual(
                git("-C", str(work), "show",
                    "origin/main:docs/migrations/provenance.json"),
                '{"book":"synthetic"}')
            self.assertIn('"preview":false', git(
                "-C", str(work), "show",
                "origin/main:books/synthetic-book/output/manifest.json"))
            paths = git("-C", str(work), "ls-tree", "-r",
                        "--name-only", "origin/main").splitlines()
            self.assertNotIn("scripts/book.py", paths)
            self.assertNotIn("docs/TRANSLATION.md", paths)
            self.assertNotIn(".book-translator-install.json", paths)

    def test_all_changes_to_books_remain_outside_public_checkout(self):
        self.assertTrue((STATE / "books").is_dir())
        self.assertNotEqual(STATE.resolve(),
                            runtime_loader.RUNTIME_ROOT.resolve())
        self.assertEqual(runtime_loader.STATE_ROOT.resolve(), STATE.resolve())


if __name__ == "__main__":
    unittest.main()
