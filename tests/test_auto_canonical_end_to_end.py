"""Two-chapter dry integration: canonical engine + mocked model, no API charges."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "automation"))
import book_runner as runner


class CanonicalAutoEndToEndTests(unittest.TestCase):
    def test_two_chapters_keep_glossary_and_produce_reviewed_epub(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            scripts = repo / "scripts"
            scripts.mkdir(parents=True)
            shutil.copy2(ROOT / "scripts" / "book.py", scripts / "book.py")
            shutil.copy2(ROOT / "scripts" / "corpus.py", scripts / "corpus.py")
            shutil.copytree(ROOT / "scripts" / "workflow", scripts / "workflow")
            shutil.copy2(ROOT / "agent-manifest.json", repo / "agent-manifest.json")
            revision = "a" * 40
            (repo / ".book-translator-install.json").write_text(json.dumps({
                "schema_version": 1,
                "canonical_repository": "https://github.com/tim8es/book-translator",
                "requested_ref": revision, "resolved_revision": revision,
                "install_root": ".",
            }) + "\n", encoding="utf-8")
            source = repo / "source.md"
            source.write_text(
                "# Chapter One\n\nMara visited Northbridge.\n"
                "\n# Chapter Two\n\nTheo met Mara in Northbridge.\n", encoding="utf-8")
            job_id = "d" * 32
            status = {"state": "running", "workflow_revision": revision,
                      "correction_rounds": {}, "failures": 0}
            observed = []
            glossary_entries = {
                1: [{"original": "Mara", "translation": "Мара", "type": "person",
                     "notes": "Protagonist"},
                    {"original": "Northbridge", "translation": "Нортбридж",
                     "type": "place", "notes": "Town"}],
                2: [{"original": "Theo", "translation": "Тео",
                     "type": "person", "notes": "Mara's friend"}],
            }
            translated = {
                1: "# Глава первая\n\nМара приехала в Нортбридж.\n",
                2: "# Глава вторая\n\nТео встретил Мару в Нортбридже.\n",
            }
            state = {"chapter": 0}

            def model(role, system, user):
                chapter = state["chapter"]
                self.assertIn("AGENTS", system.upper())
                observed.append((chapter, role, user))
                if role == "TRANSLATOR":
                    if chapter == 2:
                        self.assertIn("Northbridge | Нортбридж", user)
                        self.assertIn("PRIOR APPROVED CONTEXT", user)
                    return json.dumps({
                        "translation": translated[chapter],
                        "glossary": glossary_entries[chapter],
                        "style_guide": [],
                    }, ensure_ascii=False)
                if role == "REVIEWER":
                    return json.dumps({
                        "outcome": "PASS",
                        "checks": {"coverage": True, "meaning": True,
                                   "terminology": True, "style": True,
                                   "structure": True},
                        "findings": [], "style_guide": [],
                    })
                raise AssertionError("unexpected model role: " + role)

            with patch.object(runner, "ROOT", repo), \
                 patch.object(runner, "git", return_value="b" * 40), \
                 patch.object(runner, "checkpoint"), \
                 patch.object(runner, "complete", side_effect=model):
                runner.cli("extract", str(source), "--slug", "sample",
                           "--target-language", "ru")
                runner.cli("source-coverage", "sample", "--source",
                           str(source), "--record", "--json")
                # Canonical sealed-source admission is required before work.
                import subprocess
                sealed = subprocess.run(
                    [sys.executable, str(scripts / "corpus.py"), "seal", "sample"],
                    cwd=repo, capture_output=True, text=True)
                self.assertEqual(sealed.returncode, 0, msg=sealed.stderr)
                runner.verify("sample")
                _, _, chapters = runner.chapter_data("sample")
                self.assertEqual(len(chapters), 2)
                for index, chapter in enumerate(chapters, 1):
                    state["chapter"] = index
                    for role in ("translator", "reviewer"):
                        runner.claim(job_id, "sample", status, role, chapter)
                        runner.process_claim(job_id, "sample", status, ROOT)
                        self.assertIsNone(status.get("active"))
                    refreshed = runner.chapter_data("sample")[2][index - 1]
                    self.assertEqual(refreshed["status"], "reviewed")
                runner.finalize(job_id, "sample", status)
                self.assertEqual(status["state"], "done")
                epub = repo / status["artifact_path"]
                self.assertTrue(epub.is_file())
                self.assertGreater(epub.stat().st_size, 100)
                glossary = (repo / "books" / "sample" / "glossary.md").read_text("utf-8")
                self.assertIn("| Mara | Мара |", glossary)
                self.assertIn("| Northbridge | Нортбридж |", glossary)
                self.assertIn("| Theo | Тео |", glossary)
                self.assertEqual(len(observed), 4)


if __name__ == "__main__":
    unittest.main()
