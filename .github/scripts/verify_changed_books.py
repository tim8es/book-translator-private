"""Fast read-only checks for files changed under books/ in GitHub Actions.

Literary correctness is NOT assessed here; canonical Translator/Reviewer
acceptance and hash-bound PASS evidence remain separate quality gates.
"""
import json
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
            for command in (
                [sys.executable, "scripts/book.py", "validate", slug],
                [sys.executable, "scripts/corpus.py", "verify", slug],
            ):
                result = subprocess.run(command, cwd=root, capture_output=True, text=True)
                if result.returncode:
                    errors.append(
                        f"books/{slug}: {' '.join(command[1:])} failed: "
                        f"{(result.stdout + result.stderr)[-2000:]}"
                    )
                else:
                    print(f"PASS: books/{slug} {' '.join(command[1:])}")
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
