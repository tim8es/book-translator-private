# The Claiming Moon — source identity verification, 2026-10-21

- Uploaded original EPUB SHA-256 matches the intake record:
  `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.
- EPUB ZIP integrity: PASS.
- Source EPUB size: 1,144,636 bytes.
- Reading-order XHTML documents: 48 (preface, summary, 45 numbered chapters, afterword).
- Structural h1-h4/p elements: 18,057 including empty nodes; 17,790 nonempty nodes.
- Metadata-only map: `docs/migrations/the-claiming-moon-source-reference.json`.
- The original EPUB and all extracted original text are **not committed** to this public repository.
- The source map is useful for read-only structural auditing only; it cannot initialize source identity, create current extracted artifacts, produce a sealed corpus, or satisfy canonical `validate` and `corpus verify`.
- This report does not imply completeness, literary Reviewer PASS or release eligibility.

## Safe next execution

```bash
python scripts/migrate_intake.py the-claiming-moon --chapter-offset 2 \
  --source-reference docs/migrations/the-claiming-moon-source-reference.json
```

When moving the working book to a private workspace, initialize and seal from the exact original EPUB. Until then, do not write source XHTML/text or a false canonical progress/review ledger into the public book root.
