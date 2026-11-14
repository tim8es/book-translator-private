"""The private checkout must never fall back to mutable public main."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "automation"))
import runtime_loader as loader


class PublicRuntimeLockTests(unittest.TestCase):
    def test_lock_is_exactly_pinned_and_public(self):
        sha = loader.pinned_revision()
        self.assertRegex(sha, r"^[0-9a-f]{40}$")
        body = json.loads(loader.LOCK_PATH.read_text("utf-8"))
        self.assertEqual(body["repository"], "tim8es/book-translator")
        self.assertEqual(body["schema_version"], 1)

    def test_checkout_without_lock_or_wrong_revision_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            (root / "automation").mkdir()
            (root / "automation" / "book_runner.py").write_text("x = 1")
            lock = root / "runtime.lock.json"
            sha = "b" * 40
            lock.write_text(json.dumps({
                "schema_version": 1, "repository": "tim8es/book-translator",
                "revision": sha}), encoding="utf-8")
            with patch.object(loader, "LOCK_PATH", lock), \\
                 patch.object(loader, "RUNTIME_ROOT", root):
                with patch.object(loader.subprocess, "run", return_value=(
                        subprocess.CompletedProcess([], 0, "a" * 40 + "\n", ""))):
                    with self.assertRaisesRegex(RuntimeError, "revision differs"):
                        loader.verified_runtime("book_runner.py")
                with patch.object(loader.subprocess, "run", return_value=(
                        subprocess.CompletedProcess([], 0, sha + "\n", ""))):
                    self.assertEqual(loader.verified_runtime("book_runner.py"),
                                     (root / "automation" / "book_runner.py").resolve())
                    with self.assertRaisesRegex(RuntimeError, "unsupported"):
                        loader.verified_runtime("../secrets.json")
            lock.write_text(json.dumps({
                "schema_version": 1, "repository": "other/repo",
                "revision": sha}), encoding="utf-8")
            with patch.object(loader, "LOCK_PATH", lock):
                with self.assertRaisesRegex(RuntimeError, "invalid pinned"):
                    loader.pinned_revision()

    def test_no_duplicate_public_engine_impl_in_private_launcher(self):
        root = Path(__file__).resolve().parents[1]
        for filename in ("book_runner.py", "omniroute.py", "literary_context.py"):
            source = (root / "automation" / filename).read_text("utf-8")
            self.assertLess(len(source), 700)
            self.assertIn("load_shared_module", source)
            self.assertNotIn("def complete(", source)
            self.assertNotIn("def process_claim(", source)


if __name__ == "__main__":
    unittest.main()
