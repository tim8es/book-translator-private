"""Fast read-only checks for files changed under books/ in GitHub Actions.

Literary correctness is NOT assessed here; canonical Translator/Reviewer
acceptance and hash-bound PASS evidence remain separate quality gates.
"""
import json
import re
import tempfile
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".md", ".txt", ".json", ".html", ".xhtml", ".xml", ".css", ".yml", ".yaml"}
MAX_EPUB_EXPANDED_BYTES = 256 * 1024 * 1024


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _canonical_check_target(root, book, slug):
    """Validate an adopted book with its exact PUBLIC pinned runtime, not the private mirror.

    This happens only in an ephemeral checkout; the original book tree and its
    accepted evidence are not copied, rewritten, or pushed.
    """
    bridge_file = book / ".workflow/workflow-upgrade-evidence.json"
    if not bridge_file.is_file():
        return root, None
    try:
        metadata = json.loads((book / "metadata.json").read_text("utf-8"))
        bridge = json.loads(bridge_file.read_text("utf-8"))
        revision = metadata["workflow"]["resolved_revision"]
        if (not isinstance(revision, str)
                or re.fullmatch(r"[0-9a-f]{40}", revision) is None
                or bridge["target_workflow_revision"] != revision):
            raise ValueError("upgrade bridge target does not match pinned book revision")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"unverifiable pinned workflow upgrade: {exc}") from exc

    folder = tempfile.TemporaryDirectory(prefix="book-pinned-validate-")
    temp = Path(folder.name)
    clone = subprocess.run(
        ["git", "clone", "--quiet", "https://github.com/tim8es/book-translator.git",
         str(temp / "engine")],
        capture_output=True, text=True, timeout=180,
    )
    if clone.returncode:
        folder.cleanup()
        raise RuntimeError("cannot fetch public canonical workflow for pinned validation")
    engine = temp / "engine"
    checkout = subprocess.run(
        ["git", "-C", str(engine), "checkout", "--quiet", "--detach", revision],
        capture_output=True, text=True, timeout=45,
    )
    if checkout.returncode:
        folder.cleanup()
        raise RuntimeError("book's pinned public workflow revision is unavailable")
    (engine / "books").mkdir(exist_ok=True)
    (engine / "books" / slug).symlink_to(book.resolve(), target_is_directory=True)
    (engine / ".book-translator-install.json").write_text(json.dumps({
        "schema_version": 1,
        "canonical_repository": "https://github.com/tim8es/book-translator",
        "requested_ref": revision, "resolved_revision": revision, "install_root": ".",
    }), encoding="utf-8")
    return engine, folder


def verify_changed_books(paths, root=ROOT, run_canonical=True):
    """Return a list of errors; never write into books/."""
    root = Path(root)
    errors = []
    affected = set()
    for raw in paths:
        p = Path(raw)
        if p.is_absolute() or ".." in p.parts or not p.parts or p.parts[0] != "books":
            errors.append(f"Unsafe changed path: {raw}")
            continue
        if len(p.parts) < 3 or p.parts[1].startswith("."):
            continue
        affected.add(p.parts[1])
        path = root / p
        if not path.exists():
            continue  # Deletions are checked through canonical book validation.
        if not path.is_file() or path.is_symlink():
            errors.append(f"Expected a regular book file: {raw}")
            continue
        try:
            if path.suffix.lower() in TEXT_SUFFIXES:
                data = path.read_text(encoding="utf-8")
                if path.suffix.lower() == ".json":
                    json.loads(
                        data, object_pairs_hook=_unique_keys,
                        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"Invalid JSON constant: {x}")),
                    )
            elif path.suffix.lower() == ".epub":
                with zipfile.ZipFile(path) as archive:
                    total = sum(item.file_size for item in archive.infolist())
                    if total > MAX_EPUB_EXPANDED_BYTES:
                        raise ValueError("EPUB expands beyond the safety limit")
                    bad = archive.testzip()
                    if bad:
                        raise ValueError(f"Corrupt EPUB member: {bad}")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, zipfile.BadZipFile,
                RuntimeError) as exc:
            errors.append(f"{raw}: {exc}")

    if run_canonical:
        for slug in sorted(affected):
            book = root / "books" / slug
            if not book.is_dir():
                continue
            if not (book / "source-revisions.json").is_file():
                print(f"NOTICE: books/{slug} is legacy or incomplete; file checks only. "
                      "Literary quality and machine PASS evidence were not verified.")
                continue
            try:
                engine, lease = _canonical_check_target(root, book, slug)
            except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
                errors.append(f"books/{slug}: {exc}")
                continue
            try:
                for command in (
                    [sys.executable, "scripts/book.py", "validate", slug],
                    [sys.executable, "scripts/corpus.py", "verify", slug],
                ):
                    result = subprocess.run(
                        command, cwd=engine, capture_output=True, text=True, timeout=180,
                    )
                    if result.returncode:
                        errors.append(
                            f"books/{slug}: {' '.join(command[1:])} failed: "
                            f"{(result.stdout + result.stderr)[-2000:]}"
                        )
                    else:
                        print(f"PASS: books/{slug} {' '.join(command[1:])}")
            finally:
                if lease is not None:
                    lease.cleanup()
    return errors


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_changed_books.py <changed-book-paths.json>")
    changed = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if not isinstance(changed, list) or any(not isinstance(item, str) for item in changed):
        raise SystemExit("Expected a JSON list of changed file paths")
    issues = verify_changed_books(changed)
    if issues:
        for issue in issues:
            print("ERROR:", issue, file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated changed book files: {len(changed)}")


if __name__ == "__main__":
    main()
