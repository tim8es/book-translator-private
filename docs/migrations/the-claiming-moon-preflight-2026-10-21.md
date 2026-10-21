# The Claiming Moon — migration preflight (2026-10-21)

This is a **read-only repository tree inventory**, not verified source coverage or literary review.

- Private workspace snapshot: `700eabf5e5fffd6a15ff6635da1632a3d4139454`.
- Current public workflow revision: `777e0809af5c523c8224405f40d36e578e57a2a8`.
- Intake files: 285.
- Numbered chapters with some saved translation fragment: 44/45.
- Missing numbered chapter in this snapshot: 19.
- Chapter 15 is known from `RESUME_STATUS.md` to have only a remotely staged partial draft; a complete attachment is not in this workspace.
- Directly named single-file draft candidates: 31 (not evidence of semantic completeness).
- There is no trusted original EPUB binary in the workspace, and no canonical `metadata.json`, `progress.json`, `source-manifest.json`, `source-revisions.json`, or `review-ledger.json`.
- Expected original EPUB SHA-256 from `INTAKE.md`: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.

## Safe execution sequence

1. Obtain the exact original EPUB from an authorized private source; do not commit it into a public repository.
2. Run read-only inventory: `python scripts/migrate_intake.py the-claiming-moon --chapter-offset 2`.
3. Run the same command with `--source /private/The_Claiming_Moon.epub` and verify SHA and EPUB spine.
4. Create an isolated private migration branch/worktree, initialize and seal current-schema canonical state, then run `validate` and `corpus verify`.
5. Stage matching UNREVIEWED chapter candidates. Resolve indexed conflicts and genuinely incomplete units, including chapter 15 and chapter 19.
6. Only the Orchestrator may accept chapter artifacts and run independent Reviewer PASS before promoting the chapter.
7. Verify canonical `resume`, complete the book, and build final EPUB from accepted durable state.

Do not treat this document or any historical checkpoint as source-of-truth progress. Preserve `incoming/` unchanged throughout migration.

## Verified original EPUB (uploaded October 21, 2026)

Original EPUB was inspected locally, **not committed into this public repository**.
- SHA-256 matches: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`
- EPUB spine: **48** documents, preface (1), summary (2), chapters 1–45 (units 3–47), afterword (48).
- Source XHTML file identity matches existing checkpoint SHA-256 for chapters 20, 30 and 40.
- Historical draft index conventions vary: e.g. chapter 20 uses **577 nonempty** text elements out of **580 total**; chapter 41 has **363 total**, **359 nonempty**. The current public importer detects both schemes.
- Repositories remain public during technical development. Do **not** commit this original EPUB or extracted copyrighted source text during this phase.

### Verified partial draft coverage (GitHub blob markers vs EPUB)

| Chapter | GitHub source-indexed draft | Nonempty original source blocks | Missing from end |
|---|---:|---:|---:|
| 15 | 96 | 363 | 267 (full attachment not yet recovered) |
| 19 | 0 | 324 | 324 |
| 26 | 161 | 570 | 409 |
| 27 | 91 | 341 | 250 |
| 29 | 291 | 456 | 165 |

Chapters 26, 27 and 29 have contiguous marker coverage from index 0 and no duplicate source indexes among their currently saved Markdown fragments. This is structural only; it does **not** certify translation accuracy or Reviewer PASS.

Canonical `progress.json` still cannot be created honestly in the public workspace without a durable source corpus. Continue preparing tooling in the public repository, preserve `incoming/`, and initialize/seal the book in an isolated private workspace when source storage has been chosen.
