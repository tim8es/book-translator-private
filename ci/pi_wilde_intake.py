#!/usr/bin/env python3
"""One-time public-domain Oscar Wilde EPUB intake, on a disposable branch.

A successful run commits exactly ONE new immutable intake to main, with Pi
ownership already reserved before any possible scheduled Auto selection.
The downloaded EPUB must pass canonical extraction and coverage preflight
BEFORE any state is published. This script must never be merged to main.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

JOB_ID = "297fd08ee43deb245fd4a033240ded56"
BOOK_REV = "6ed4b4cc777b2e099c08b785aae925b0c5b8296c"
BRANCH = "ci/pi-wilde-first-real-book-20261121"
PAGE = "https://github.com/standardebooks/oscar-wilde_childrens-stories"
SOURCES = [
    "https://www.gutenberg.org/ebooks/902.epub3.noimages",
    "https://www.gutenberg.org/cache/epub/902/pg902.epub",
    "https://www.gutenberg.org/cache/epub/902/pg902-images-3.epub",
    "https://www.gutenberg.org/ebooks/902.epub.noimages",
]
ROOT = Path(os.environ["GITHUB_WORKSPACE"])
STATE = ROOT / "state"
ENGINE = ROOT / "engine"
SLUG = "the-happy-prince-and-other-tales"
MAX_SIZE = 8 * 1024 * 1024


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=STATE, text=True, encoding="utf-8",
                          capture_output=True, check=check)


def download() -> tuple[bytes, str]:
    """Package the five original 1888 tales from a pinned CC0 source edition.

    GitHub Actions checks out the pinned Standard Ebooks source repository.
    XHTML source text is preserved byte-for-byte; images, other books and
    publishing front matter are intentionally not included in this pilot.
    """
    source_sha = "8147cbf79e01eeee9eeefed80148ecb2dfb06d67"
    source_root = ROOT / "standard-source"
    actual_sha = subprocess.check_output(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True).strip()
    require(actual_sha == source_sha, "standard_ebooks_source_revision_drift")
    chapters = [
        "the-happy-prince",
        "the-nightingale-and-the-rose",
        "the-selfish-giant",
        "the-devoted-friend",
        "the-remarkable-rocket",
    ]
    text_root = source_root / "src" / "epub" / "text"
    src_css = source_root / "src" / "epub" / "css"
    content = []
    for name in chapters:
        file = text_root / (name + ".xhtml")
        data = file.read_bytes()
        require(b'xmlns="http://www.w3.org/1999/xhtml"' in data and
                b"<article " in data and len(data) > 3500,
                "source_story_missing_or_incomplete")
        ET.fromstring(data)
        content.append((name, data))
    stem = "OPS/"
    metadata = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
        'unique-identifier="book-id">'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
        '<dc:identifier id="book-id">urn:uuid:2991c9fb-3212-4bb4-9c71-4eef341908a8</dc:identifier>'
        '<dc:title>The Happy Prince and Other Tales</dc:title>'
        '<dc:creator>Oscar Wilde</dc:creator>'
        '<dc:language>en</dc:language>'
        '<dc:rights>Original text public domain; Standard Ebooks CC0 source edition.</dc:rights>'
        '<dc:source>https://github.com/standardebooks/oscar-wilde_childrens-stories'
        '/tree/' + source_sha + '</dc:source>'
        '</metadata><manifest>'
        + "".join('<item id="s' + str(i) + '" href="text/' + name +
                  '.xhtml" media-type="application/xhtml+xml"/>'
                  for i, (name, _) in enumerate(content, 1))
        + '<item id="css-core" href="css/core.css" media-type="text/css"/>'
          '<item id="css-local" href="css/local.css" media-type="text/css"/>'
          '</manifest><spine>'
        + "".join('<itemref idref="s' + str(i) + '"/>'
                  for i in range(1, len(content) + 1))
        + '</spine></package>'
    )
    rootfile = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" '
        'version="1.0"><rootfiles><rootfile full-path="OPS/content.opf" '
        'media-type="application/oebps-package+xml"/></rootfiles></container>'
    )
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("mimetype", "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", rootfile)
        z.writestr(stem + "content.opf", metadata)
        for name, body in content:
            z.writestr(stem + "text/" + name + ".xhtml", body)
        for name in ("core.css", "local.css"):
            z.writestr(stem + "css/" + name, (src_css / name).read_bytes())
    data = buffer.getvalue()
    require(3000 < len(data) <= MAX_SIZE and data[:2] == b"PK",
            "constructed_epub_invalid")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        require(archive.testzip() is None, "constructed_epub_zip_corrupt")
    print("PINNED_CC0_SOURCE_VERIFIED stories=" + str(len(content)), flush=True)
    return data, "https://github.com/standardebooks/oscar-wilde_childrens-stories/tree/" + source_sha


def epub_details(data: bytes) -> tuple[str, str, int]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        container = ET.fromstring(archive.read("META-INF/container.xml"))
        rootfile = next(node.attrib["full-path"] for node in container.iter()
                        if node.tag.rsplit("}", 1)[-1] == "rootfile")
        require(".." not in rootfile and not rootfile.startswith("/"),
                "unsafe_opf_path")
        package = ET.fromstring(archive.read(rootfile))
        metadata = next(node for node in package
                        if node.tag.rsplit("}", 1)[-1] == "metadata")
        title = next((e.text.strip() for e in metadata.iter()
                      if e.tag.rsplit("}", 1)[-1] == "title"
                      and e.text and e.text.strip()), "")
        author = next((e.text.strip() for e in metadata.iter()
                       if e.tag.rsplit("}", 1)[-1] == "creator"
                       and e.text and e.text.strip()), "")
        spine = next(node for node in package
                     if node.tag.rsplit("}", 1)[-1] == "spine")
        count = len([n for n in spine if n.tag.rsplit("}", 1)[-1] == "itemref"])
    require("happy prince" in title.casefold() and "wilde" in author.casefold(),
            "unexpected_epub_bibliography")
    require(count >= 2 and count <= 60, "unexpected_spine_count")
    require(len(title) <= 200 and len(author) <= 200, "bibliography_too_long")
    return title, author, count


def check_full_source(epub: Path) -> int:
    with tempfile.TemporaryDirectory(prefix="wilde-canonical-preflight-") as d:
        temp = Path(d)
        shutil.copytree(ENGINE / "scripts", temp / "scripts")
        shutil.copy2(ENGINE / "agent-manifest.json", temp / "agent-manifest.json")
        (temp / ".book-translator-install.json").write_text(json.dumps({
            "schema_version": 1,
            "canonical_repository": "https://github.com/tim8es/book-translator",
            "requested_ref": BOOK_REV,
            "resolved_revision": BOOK_REV,
            "install_root": ".",
        }) + "\n", encoding="utf-8")
        commands = [
            [sys.executable, "scripts/book.py", "extract", str(epub),
             "--slug", SLUG, "--target-language", "ru"],
            [sys.executable, "scripts/corpus.py", "seal", SLUG],
            [sys.executable, "scripts/book.py", "source-coverage", SLUG,
             "--source", str(epub), "--record", "--json"],
            [sys.executable, "scripts/book.py", "validate", SLUG],
            [sys.executable, "scripts/corpus.py", "verify", SLUG],
        ]
        for command in commands:
            result = subprocess.run(command, cwd=temp, text=True,
                                    capture_output=True, encoding="utf-8",
                                    timeout=90)
            if result.returncode:
                print("CANONICAL_PREFLIGHT_FAILED " + " ".join(command[1:4]),
                      flush=True)
                print("CANONICAL_PREFLIGHT_DIAGNOSTIC " +
                      (result.stderr or result.stdout)[-500:].replace("\n", " "),
                      flush=True)
                raise RuntimeError("canonical_preflight_failed")
        progress = json.loads((temp / "books" / SLUG / "progress.json").read_text())
        coverage = json.loads((temp / "books" / SLUG / "source-coverage.json").read_text())
        require(coverage.get("state") == "verified", "coverage_not_verified")
        chapters = progress.get("chapters", [])
        require(len(chapters) >= 4 and all(ch["status"] == "extracted" for ch in chapters),
                "book_reading_order_incomplete")
        print("CANONICAL_PREFLIGHT_VERIFIED units=" + str(len(chapters)),
              flush=True)
        return len(chapters)


def main() -> None:
    require(os.environ.get("GITHUB_REF") == "refs/heads/" + BRANCH,
            "not_isolated_intake_branch")
    require(git("branch", "--show-current").stdout.strip() == "main",
            "state_checkout_not_main")
    require(not (STATE / "intake/auto" / JOB_ID).exists(), "job_already_exists")
    require(not (STATE / "books" / SLUG).exists(), "book_already_exists")
    require(subprocess.check_output(["git", "-C", str(ENGINE), "rev-parse", "HEAD"],
                                  text=True).strip() == BOOK_REV,
            "source_workflow_not_pinned")
    data, url = download()
    title, author, spine_count = epub_details(data)
    derived_slug = re.sub(r"[^\w\s-]", "", title.strip().lower())
    derived_slug = re.sub(r"[\s_]+", "-", derived_slug).strip("-")[:120].rstrip("-")
    require(derived_slug == SLUG, "unexpected_canonical_book_slug")
    digest = hashlib.sha256(data).hexdigest()
    print("AUTHENTIC_EPUB_CHECKED size=" + str(len(data)) +
          " spine=" + str(spine_count) + " sha256=" + digest +
          " source_page=" + PAGE, flush=True)
    with tempfile.TemporaryDirectory(prefix="wilde-epub-") as d:
        source = Path(d) / "original.epub"
        source.write_bytes(data)
        check_full_source(source)
    # Refetch current head after preflight; main may change concurrently.
    git("fetch", "--quiet", "origin", "main")
    require(not git("status", "--porcelain", "--untracked-files=no").stdout.strip(),
            "dirty_state_checkout")
    git("reset", "--hard", "origin/main")
    require(not (STATE / "intake/auto" / JOB_ID).exists(), "job_created_during_preflight")
    require(not (STATE / "books" / SLUG).exists(), "book_created_during_preflight")
    folder = STATE / "intake" / "auto" / JOB_ID
    folder.mkdir(parents=True)
    (folder / "source.epub").write_bytes(data)
    request = {
        "schema_version": 1,
        "job_id": JOB_ID,
        "source_sha256": digest,
        "target_language": "ru",
        "workflow_revision": BOOK_REV,
        "title": title,
        "author": author,
        "source_filename": "oscar-wilde-happy-prince-standardebooks-source.epub",
    }
    owner = {"schema_version": 1, "job_id": JOB_ID,
             "source_sha256": digest, "executor": "pi"}
    (folder / "request.json").write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "executor.json").write_text(
        json.dumps(owner, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rel = f"intake/auto/{JOB_ID}"
    git("add", "--", rel)
    selected = git("diff", "--cached", "--name-only").stdout.splitlines()
    require(sorted(selected) == sorted([rel + "/source.epub", rel + "/request.json",
                                        rel + "/executor.json"]), "staged_scope_invalid")
    git("-c", "user.name=github-actions[bot]",
        "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
        "commit", "-m", "test(pi): register public-domain Oscar Wilde EPUB")
    for attempt in range(8):
        result = git("push", "origin", "HEAD:refs/heads/main", check=False)
        if result.returncode == 0:
            break
        if "rejected" not in result.stderr.lower() and "fetch first" not in result.stderr.lower():
            raise RuntimeError("intake_push_rejected")
        git("fetch", "--quiet", "origin", "main")
        git("rebase", "origin/main")
    else:
        raise RuntimeError("intake_publish_retry_exhausted")
    print("PI_INTAKE_PUBLISHED job_id=" + JOB_ID + " sha256=" + digest, flush=True)
    dispatch = subprocess.run([
        "gh", "workflow", "run", "pi-book-translation.yml", "--ref", "main",
        "-f", "probe_only=false", "-f", "job_id=" + JOB_ID,
        "-f", "continue_automatically=false",
    ], cwd=STATE, capture_output=True, text=True, timeout=30)
    require(dispatch.returncode == 0, "pi_initial_dispatch_failed")
    print("PI_FIRST_CHECKPOINT_DISPATCHED job_id=" + JOB_ID, flush=True)


try:
    main()
except Exception as exc:
    print("PI_REAL_BOOK_INTAKE_FAILED " + type(exc).__name__ + ":" +
          str(exc)[:170], file=sys.stderr)
    raise SystemExit(1)
