"""One-book, no-push live Pi integration smoke. Only synthetic copyrighted-safe prose."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

PUBLIC = Path(os.environ["PUBLIC_ENGINE_PATH"]).resolve()
sys.path.insert(0, str(PUBLIC / "automation"))
import book_runner as runner

def main():
    if os.environ.get("BOOK_TRANSLATOR_LLM_BACKEND") != "pi":
        raise RuntimeError("pi_backend_not_selected")
    if not os.environ.get("OMNIROUTE_API_KEY"):
        raise RuntimeError("omniroute_key_unavailable")
    with tempfile.TemporaryDirectory(prefix="bt-pi-live-e2e-") as temp:
        repo = Path(temp) / "book-state"
        scripts = repo / "scripts"
        scripts.mkdir(parents=True)
        shutil.copy2(PUBLIC / "scripts" / "book.py", scripts / "book.py")
        shutil.copy2(PUBLIC / "scripts" / "corpus.py", scripts / "corpus.py")
        shutil.copytree(PUBLIC / "scripts" / "workflow", scripts / "workflow")
        shutil.copy2(PUBLIC / "agent-manifest.json", repo / "agent-manifest.json")
        fake_revision = "a" * 40
        (repo / ".book-translator-install.json").write_text(json.dumps({
            "schema_version": 1,
            "canonical_repository": "https://github.com/tim8es/book-translator",
            "requested_ref": fake_revision,
            "resolved_revision": fake_revision,
            "install_root": ".",
        }) + "\n", encoding="utf-8")
        source = repo / "synthetic-source.md"
        source.write_text(
            "# Chapter One\n\n"
            "Mara waited beside the window while rain tapped the roof. "
            "At dawn she opened the door and saw the lighthouse beyond the harbor.\n",
            encoding="utf-8")
        job_id = "d" * 32
        status = {
            "state": "running",
            "workflow_revision": fake_revision,
            "correction_rounds": {},
            "failures": 0,
        }
        with patch.object(runner, "ROOT", repo), \
             patch.object(runner, "git", return_value="b" * 40), \
             patch.object(runner, "checkpoint"):
            runner.cli("extract", str(source), "--slug", "pi-live-epub-smoke",
                       "--target-language", "ru")
            sealed = subprocess.run(
                [sys.executable, str(scripts / "corpus.py"), "seal", "pi-live-epub-smoke"],
                cwd=repo, capture_output=True, text=True, check=False)
            if sealed.returncode:
                raise RuntimeError("corpus_seal_failed")
            runner.verify("pi-live-epub-smoke")
            chapters = runner.chapter_data("pi-live-epub-smoke")[2]
            if len(chapters) != 1:
                raise RuntimeError("unexpected_source_unit_count")
            chapter = chapters[0]
            print("SYNTHETIC_SOURCE_SEALED, unit=" + str(chapter["unit_id"]), flush=True)
            for role in ("translator", "reviewer"):
                print("ROLE_STARTED=" + role, flush=True)
                runner.claim(job_id, "pi-live-epub-smoke", status, role, chapter)
                runner.process_claim(job_id, "pi-live-epub-smoke", status, PUBLIC)
                if status.get("active"):
                    raise RuntimeError("claim_not_released_" + role)
                print("ROLE_COMPLETED=" + role, flush=True)
            refreshed = runner.chapter_data("pi-live-epub-smoke")[2][0]
            print("CANONICAL_UNIT_STATUS=" + str(refreshed["status"]), flush=True)
            if refreshed["status"] != "reviewed":
                raise RuntimeError("chapter_not_reviewed")
            runner.finalize(job_id, "pi-live-epub-smoke", status)
            epub = repo / status.get("artifact_path", "")
            if status["state"] != "done" or not epub.is_file() or epub.stat().st_size < 100:
                raise RuntimeError("epub_not_finalized")
            print("CANONICAL_EPUB_VALIDATED, bytes=" + str(epub.stat().st_size), flush=True)

try:
    main()
except BaseException as exc:
    print("LIVE_CANONICAL_TEST_FAILED, category=" + type(exc).__name__, file=sys.stderr)
    sys.exit(1)
