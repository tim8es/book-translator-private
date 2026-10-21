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
