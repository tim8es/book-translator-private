# GitHub-first book state

Migration to durable GitHub-first persistence is complete.

- Canonical book workspace: `books/alex-cole-ten-commandments/` in `tim8es/book-translator-private`.
- Canonical workflow revision: `c72f9848d0a79c9ffb66cf7b1dc35905d21aecd9` from `tim8es/book-translator`.
- Exact preserved source: `source/alex-cole-ten-commandments_414809252.epub`.
- Source EPUB SHA-256: `fcfedf4a253a22df3c0baa767cbe5ccdb30916a5957515f4d68b5b5f0be590dc`.
- All five extracted source artifacts are sealed by `source-manifest.json` and pass corpus verification.
- All five Russian chapter translations are present and reviewed.
- Chapter 5 reviewer PASS is recorded under `review/`.
- User-specific translation rule: Russian spoken direct speech is formatted with an em dash (`—`), not quotation marks.

GitHub durable state is authoritative for future sessions; local session files are not book state.
