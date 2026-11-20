# Source candidate and Chapter 12 — 2026-11-21

This folder is **preserved input and a provisional ChatOps literary artifact**, not an active canonical source revision, not Translator acceptance, and not Reviewer PASS.

## Preserved artifacts

- `source/You_Feel_Like_Home.html` — exact uploaded HTML (554,021 bytes, SHA-256 `c602be8c25de25d5f943f4c8de80e5a3df801b6c7fb2eb833204a1df38f92b9c`).
- `translated/chapter-12-ru-after-review.md` — corrected full Chapter 12 Russian draft (390 narrative paragraphs; 91,502 bytes, SHA-256 `84ffe904e8e96995f9df46825217f36370684072bef1ff585cf52ed8ab573586`).
- `review/chapter-12-local-review.md` — source-comparison findings from the **same chat context** (`bounded_context`), **not** an independent reviewer record.
- `source-info.json` — machine-readable provenance and staging status.

## Safe canonical handoff

The active book revision is `source-000002`, with 14 reading-order units; the supplied HTML contains 12 numbered chapters plus front/back matter. Source revisions and unit identity must be reconciled by the book-pinned engine `db253095d36f245f9531da654b93ab72193d3b97`.

With that exact engine and a valid checkout of this book-state repository, run:

```bash
python scripts/book.py validate you-feel-like-home
python scripts/corpus.py verify you-feel-like-home
python scripts/book.py update-source you-feel-like-home \
  books/you-feel-like-home/source-updates/2026-11-21/source/You_Feel_Like_Home.html \
  --stage-only --json
```

Inspect the complete staged delta. Do not approve deletions without an explicit decision; do not overwrite historical accepted artifacts. Promote only after the workflow gates pass, and then adapt the Chapter 12 draft to its newly allocated canonical unit path, acquire a Translator claim, accept the exact translated artifact, run an independent source-to-translation review, and record/pass review before marking `reviewed`. Re-review unchanged historical chapters separately according to the current ledger.

The file snapshots in this folder are deliberately kept outside `source-revisions/`, `progress.json`, and `review-ledger.json`. A commit of these staged files **does not** make Chapter 12 part of the built EPUB.
