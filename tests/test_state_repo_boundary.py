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
        self.assertIn("group: automatic-book-", auto)
        self.assertIn("max-parallel: 3", auto)
        self.assertIn("Dispatch next bounded step", auto)
        self.assertNotIn("workflow_call:", auto)
        for filename in ("auto-translate.yml", "book-batch-validation.yml",
                         "book-job-monitor.yml", "omniroute-json-smoke.yml"):
            source = (root / filename).read_text("utf-8")
            self.assertIn("runtime_loader.py", source)
            self.assertIn("repository: tim8es/book-translator", source)
        chat = (root / "chat-operations.yml").read_text("utf-8")
        self.assertIn("engine/scripts/chat_ops_bridge.py", chat)
        epub = (root / "final-epub.yml").read_text("utf-8")
        self.assertIn(".pinned-book-translator", epub)
        self.assertIn("cp -a .pinned-book-translator/docs ./docs", epub)

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

    def test_all_changes_to_books_remain_outside_public_checkout(self):
        self.assertTrue((STATE / "books").is_dir())
        self.assertNotEqual(STATE.resolve(),
                            runtime_loader.RUNTIME_ROOT.resolve())
        self.assertEqual(runtime_loader.STATE_ROOT.resolve(), STATE.resolve())


if __name__ == "__main__":
    unittest.main()
