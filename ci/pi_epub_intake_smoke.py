#!/usr/bin/env python3
"""Ephemeral source-EPUB + canonical book_runner.run integration.

The only GitHub writes target synthetic book, immutable intake, and its status
on a disposable branch; book_runner checkpoints go to a local bare git remote.
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
import zipfile

BRANCH = "ci/pi-durable-resume-smoke-20261121"
BOOK_SLUG = "pi-epub-intake-smoke-november-2026"
TITLE = "Pi EPUB Intake Smoke November 2026"
JOB_ID = "a71c2f5f4fb6415d98b46e93a4e320a7"
PUBLIC_SHA = "ffcc39c1977cd36107510953ad6c689dabd10ab0"
WORKSPACE = Path(os.environ["GITHUB_WORKSPACE"]).resolve()
PUBLIC = WORKSPACE / ".pi-engine"


def shell(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", check=True)


def expect(cond, message):
    if not cond:
        raise RuntimeError(message)


def build_epub(path):
    content = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<html xmlns="http://www.w3.org/1999/xhtml">'
        '<head><title>Chapter One</title></head>'
        '<body><h1>Chapter One</h1>'
        '<p>The lantern flickered above the quiet pier. Mara looked toward the harbor, '
        'where the fishing boats returned at dawn. She took her brother by the hand '
        'and thanked him for keeping his promise.</p></body></html>'
    )
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
          '<?xml version="1.0" encoding="utf-8"?>'
          '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">'
          '<rootfiles><rootfile full-path="OPS/content.opf" '
          'media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr("OPS/content.opf",
          '<?xml version="1.0" encoding="utf-8"?>'
          '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">'
          '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
          '<dc:identifier id="id">urn:uuid:pi-epub-intake-20261121</dc:identifier>'
          f'<dc:title>{TITLE}</dc:title><dc:creator>Test Fixture</dc:creator>'
          '<dc:language>en</dc:language></metadata>'
          '<manifest><item id="c1" href="chapter.xhtml" media-type="application/xhtml+xml"/>'
          '</manifest><spine><itemref idref="c1"/></spine></package>')
        z.writestr("OPS/chapter.xhtml", content)


def run_smoke():
    expect(os.environ.get("GITHUB_REF") == "refs/heads/" + BRANCH,
           "wrong_branch")
    expect(os.environ.get("BOOK_TRANSLATOR_LLM_BACKEND") == "pi",
           "pi_not_selected")
    expect(shell("git", "-C", str(PUBLIC), "rev-parse", "HEAD").stdout.strip() == PUBLIC_SHA,
           "wrong_public_commit")

    with tempfile.TemporaryDirectory(prefix="pi-auto-intake-") as d:
        t=Path(d)
        remote=t / "remote.git"
        state=t / "state"
        shell("git","init","--bare",str(remote))
        shell("git","push",str(remote),"HEAD:refs/heads/main",cwd=WORKSPACE)
        shell("git","clone","--branch","main",str(remote),str(state))
        shell("git","config","user.name","github-actions[bot]",cwd=state)
        shell("git","config","user.email",
              "41898282+github-actions[bot]@users.noreply.github.com",cwd=state)

        job_dir=state/"intake"/"auto"/JOB_ID
        expect(not job_dir.exists(), "duplicate_synthetic_intake")
        job_dir.mkdir(parents=True)
        epub=job_dir/"source.epub"
        build_epub(epub)
        epub_sha=hashlib.sha256(epub.read_bytes()).hexdigest()
        (job_dir/"request.json").write_text(json.dumps({
            "schema_version":1,"job_id":JOB_ID,"source_sha256":epub_sha,
            "target_language":"ru","workflow_revision":PUBLIC_SHA,
            "title":TITLE,"author":"Test Fixture",
            "source_filename":"synthetic-fixture.epub",
        }) + "\n",encoding="utf-8")

        sys.path.insert(0, str(PUBLIC/"automation"))
        import book_runner as runner
        runner.ROOT=state

        steps=[]
        for i in range(18):
            previous=runner.read_json(state/"automation"/"status"/(JOB_ID+".json")) \
                if (state/"automation"/"status"/(JOB_ID+".json")).exists() else None
            if previous and previous.get("state") == "done":
                break
            try:
                status=runner.run(JOB_ID)
            except Exception as exc:
                raise RuntimeError("canonical_step_failed_" +
                                   type(exc).__name__) from None
            expect(isinstance(status,dict) and status.get("job_id")==JOB_ID,
                   "invalid_checkpoint_state")
            steps.append(status.get("phase"))
            print("AUTO_CHECKPOINT=" + str(i+1) +
                  ",state=" + str(status.get("state")) +
                  ",phase=" + str(status.get("phase")),flush=True)
            expect(status.get("state")=="running" or status.get("state")=="done",
                   "auto_job_blocked")
            expect(status.get("phase")!="provider-backoff",
                   "provider_backoff_is_not_an_epub_success")
        else:
            raise RuntimeError("bounded_steps_exhausted")

        final=runner.read_json(state/"automation"/"status"/(JOB_ID+".json"))
        expect(final["state"]=="done","missing_terminal_done")
        book_dir=state/"books"/BOOK_SLUG
        expect(book_dir.is_dir(),"derived_book_slug_drift")
        meta=runner.read_json(book_dir/"metadata.json")
        expect(meta["workflow"]["resolved_revision"]==PUBLIC_SHA,
               "book_revision_drift")
        progress=runner.read_json(book_dir/"progress.json")
        expect(len(progress["chapters"])==1 and
               progress["chapters"][0]["status"]=="reviewed","unit_not_reviewed")
        ledger=runner.read_json(book_dir/"review-ledger.json")
        expect(any(x.get("outcome")=="PASS" for x in ledger["records"]),
               "independent_review_missing")
        coverage=runner.read_json(book_dir/"source-coverage.json")
        expect(bool(coverage),"source_coverage_missing")
        manifest=runner.read_json(book_dir/"output"/"manifest.json")
        artifact=book_dir/manifest["artifact_path"]
        expect(artifact.is_file(),"epub_missing")
        expect(hashlib.sha256(artifact.read_bytes()).hexdigest()==manifest["artifact_sha256"],
               "epub_hash_mismatch")
        print("EPUB_AUTO_COMPLETED:steps=" + str(len(steps)) +
              ",bytes=" + str(artifact.stat().st_size) +
              ",coverage=true,reviewed=true",flush=True)

        # Snapshot only the newly created synthetic intake/book/job to the
        # isolated GitHub branch; the original private main is untouched.
        for src,target in [
            (book_dir,WORKSPACE/"books"/BOOK_SLUG),
            (job_dir,WORKSPACE/"intake"/"auto"/JOB_ID),
            (state/"automation"/"status"/(JOB_ID+".json"),
             WORKSPACE/"automation"/"status"/(JOB_ID+".json")),
        ]:
            expect(src.exists(),"source_artifact_missing")
            target.parent.mkdir(parents=True,exist_ok=True)
            if src.is_dir():
                shutil.copytree(src,target)
            else:
                shutil.copy2(src,target)
        paths=[f"books/{BOOK_SLUG}",f"intake/auto/{JOB_ID}",
               f"automation/status/{JOB_ID}.json"]
        shell("git","add","-A","--",*paths,cwd=WORKSPACE)
        selected=shell("git","diff","--cached","--name-only",cwd=WORKSPACE).stdout.splitlines()
        expect(bool(selected) and all(
            x.startswith("books/"+BOOK_SLUG+"/") or
            x.startswith("intake/auto/"+JOB_ID+"/") or
            x=="automation/status/"+JOB_ID+".json" for x in selected),
            "unexpected_commit_scope")
        shell("git","-c","user.name=github-actions[bot]",
              "-c","user.email=41898282+github-actions[bot]@users.noreply.github.com",
              "commit","-m","test(pi): durable canonical EPUB Auto intake smoke",
              cwd=WORKSPACE)
        shell("git","push","origin","HEAD:refs/heads/"+BRANCH,cwd=WORKSPACE)
        print("CANONICAL_AUTO_INTAKE_PERSISTED_TO_GITHUB",flush=True)


try:
    run_smoke()
except Exception as exc:
    print("INTAKE_SMOKE_FAILED:" + type(exc).__name__ + ":" +
          str(exc)[:100],file=sys.stderr)
    raise SystemExit(1)
