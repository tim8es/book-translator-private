#!/usr/bin/env python3
"""Disposable, branch-isolated durable Pi test.

No production book or job is modified. Checkpoints use a local main remote,
then only this synthetic book/status are promoted to an isolated GitHub branch.
Separate Actions invocations demonstrate recovery without persisted Pi sessions.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BRANCH = "ci/pi-durable-resume-smoke-20261121"
SLUG = "pi-durable-resume-smoke-20261121"
JOB_ID = "9c33de418ec14b9aaa42c4d952d6f31e"
ENGINE_SHA = "ffcc39c1977cd36107510953ad6c689dabd10ab0"
WORKSPACE = Path(os.environ["GITHUB_WORKSPACE"]).resolve()
PUBLIC = (WORKSPACE / ".pi-engine").resolve()
SOURCE = (
    "# Chapter One\n\n"
    "Mira waited by the old lighthouse as the evening rain crossed the harbor. "
    "She had promised to leave the lamp burning until her brother returned. "
    "At dawn, the fishing boats appeared beyond the breakwater, and she finally smiled.\n"
)


def git(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=cwd, text=True, encoding="utf-8",
        capture_output=True, check=check,
    )


def require(test: bool, message: str) -> None:
    if not test:
        raise RuntimeError(message)


def copy_canonical_tools(state: Path) -> None:
    (state / "scripts").mkdir(exist_ok=True)
    for filename in ("book.py", "corpus.py"):
        shutil.copy2(PUBLIC / "scripts" / filename, state / "scripts" / filename)
    shutil.copytree(PUBLIC / "scripts" / "workflow", state / "scripts" / "workflow")
    shutil.copy2(PUBLIC / "agent-manifest.json", state / "agent-manifest.json")
    (state / ".book-translator-install.json").write_text(
        json.dumps({
            "schema_version": 1,
            "canonical_repository": "https://github.com/tim8es/book-translator",
            "requested_ref": ENGINE_SHA,
            "resolved_revision": ENGINE_SHA,
            "install_root": ".",
        }) + "\n",
        encoding="utf-8",
    )


def publish_synthetic_state(state: Path) -> None:
    pairs = (
        (state / "books" / SLUG, WORKSPACE / "books" / SLUG),
        (state / "automation" / "status" / f"{JOB_ID}.json",
         WORKSPACE / "automation" / "status" / f"{JOB_ID}.json"),
    )
    for src, target in pairs:
        require(src.exists(), "expected_canonical_artifact_missing")
        if src.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(src, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
    paths = [f"books/{SLUG}", f"automation/status/{JOB_ID}.json"]
    git("add", "-A", "--", *paths, cwd=WORKSPACE)
    changed = git("diff", "--cached", "--name-only", cwd=WORKSPACE).stdout.splitlines()
    require(all(x.startswith(f"books/{SLUG}/") or
                x == f"automation/status/{JOB_ID}.json" for x in changed),
            "unexpected_staged_change")
    require(bool(changed), "expected_durable_change_missing")
    git("-c", "user.name=github-actions[bot]",
        "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
        "commit", "-m", "test(pi): durable synthetic checkpoint",
        cwd=WORKSPACE)
    git("push", "origin", "HEAD:refs/heads/" + BRANCH, cwd=WORKSPACE)
    print("PUBLISHED_SYNTHETIC_STATE_TO_GITHUB", flush=True)


def main() -> None:
    require(os.environ.get("GITHUB_REF") == "refs/heads/" + BRANCH,
            "must_run_on_isolated_test_branch")
    require(os.environ.get("GITHUB_EVENT_NAME") == "push",
            "unexpected_trigger")
    require(os.environ.get("BOOK_TRANSLATOR_LLM_BACKEND") == "pi",
            "pi_backend_not_selected")
    require(git("rev-parse", "HEAD", cwd=PUBLIC).stdout.strip() == ENGINE_SHA,
            "public_engine_revision_mismatch")

    signal = json.loads((WORKSPACE / "ci" / "pi-durable-signal.json").read_text("utf-8"))
    require(set(signal) == {"schema_version", "step"} and signal["schema_version"] == 1,
            "invalid_test_signal")
    stage = signal["step"]
    require(stage in ("init", "translator", "reviewer", "finalize"),
            "invalid_test_stage")
    print("DURABLE_STAGE=" + stage, flush=True)

    with tempfile.TemporaryDirectory(prefix="pi-durable-") as tmp:
        temp = Path(tmp)
        bare = temp / "remote.git"
        state = temp / "state"
        git("init", "--bare", str(bare))
        git("push", str(bare), "HEAD:refs/heads/main", cwd=WORKSPACE)
        git("clone", "--branch", "main", str(bare), str(state))
        git("config", "user.name", "github-actions[bot]", cwd=state)
        git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com",
            cwd=state)
        copy_canonical_tools(state)
        sys.path.insert(0, str(PUBLIC / "automation"))
        import book_runner as runner
        runner.ROOT = state
        status_file = state / "automation" / "status" / f"{JOB_ID}.json"

        if stage == "init":
            require(not status_file.exists(), "smoke_job_already_initialized")
            require(not (state / "books" / SLUG).exists(), "smoke_book_already_exists")
            original = temp / "original.md"
            original.write_text(SOURCE, encoding="utf-8")
            runner.cli("extract", str(original), "--slug", SLUG, "--target-language", "ru")
            sealed = subprocess.run(
                runner.canonical_command("corpus", "seal", SLUG),
                cwd=state, capture_output=True, text=True, encoding="utf-8",
            )
            require(sealed.returncode == 0, "source_sealing_failed")
            runner.verify(SLUG)
            metadata = runner.read_json(state / "books" / SLUG / "metadata.json")
            require(metadata["workflow"]["resolved_revision"] == ENGINE_SHA,
                    "synthetic_book_pin_invalid")
            chapters = runner.chapter_data(SLUG)[2]
            require(len(chapters) == 1 and chapters[0]["status"] == "extracted",
                    "synthetic_extraction_invalid")
            for directory in ("translated", "output"):
                (state / "books" / SLUG / directory / ".gitkeep").touch(exist_ok=True)
            status = {
                "schema_version": 1, "job_id": JOB_ID, "book_slug": SLUG,
                "state": "running", "phase": "initialized", "failures": 0,
                "correction_rounds": {}, "workflow_revision": ENGINE_SHA,
            }
            runner.checkpoint(JOB_ID, status, SLUG)
            print("CANONICAL_INIT_CHECKPOINT_COMMITTED", flush=True)
        else:
            require(status_file.exists(), "durable_job_status_missing")
            status = runner.read_json(status_file)
            require(status.get("workflow_revision") == ENGINE_SHA,
                    "durable_workflow_pin_drift")
            runner.verify(SLUG)
            chapter = runner.chapter_data(SLUG)[2][0]
            if stage in ("translator", "reviewer"):
                expected = "extracted" if stage == "translator" else "translated"
                require(chapter["status"] == expected, "incorrect_durable_stage")
                role = stage
                print("PI_ROLE_STARTED=" + role, flush=True)
                runner.claim(JOB_ID, SLUG, status, role, chapter)
                runner.process_claim(JOB_ID, SLUG, status, PUBLIC)
                require(status.get("active") is None, "unreleased_canonical_claim")
                updated = runner.chapter_data(SLUG)[2][0]
                expected_after = "translated" if role == "translator" else "reviewed"
                require(updated["status"] == expected_after,
                        "canonical_role_outcome_is_not_" + expected_after)
                print("PI_ROLE_PERSISTED=" + role + ",state=" + updated["status"],
                      flush=True)
            else:
                require(chapter["status"] == "reviewed", "book_not_fully_reviewed")
                runner.finalize(JOB_ID, SLUG, status)
                manifest = runner.read_json(
                    state / "books" / SLUG / "output" / "manifest.json")
                artifact = state / "books" / SLUG / manifest["artifact_path"]
                require(artifact.is_file(), "epub_not_created")
                digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
                require(digest == manifest["artifact_sha256"],
                        "epub_manifest_hash_mismatch")
                require(status["state"] == "done", "book_not_delivered")
                print("FINAL_EPUB_VERIFIED,bytes=" + str(artifact.stat().st_size) +
                      ",sha256=" + digest, flush=True)
        # This push is performed outside Pi, with only the synthetic book scope.
        publish_synthetic_state(state)


try:
    main()
except Exception as exc:
    # No prompts, sources, translations, credentials or generated text in logs.
    print("DURABLE_SMOKE_FAILED:" + type(exc).__name__ + ":" +
          str(exc)[:130], file=sys.stderr)
    raise SystemExit(1)
