# The Claiming Moon — migration preflight (2026-10-21)

This is a **read-only repository tree inventory**, not verified source coverage or literary review.

- Private workspace snapshot: `700eabf5e5fffd6a15ff6635da1632a3d4139454`.
- Installed public workflow revision: `c630e65bfe27c03bfa9a461a77385ca43cf46d93` (dual-index verification).
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

## Original source verification (2026-10-21)

The user supplied the original EPUB in the active ChatGPT conversation. It was
verified locally, **not committed to GitHub**:

- Filename: `The_Claiming_Moon.epub`.
- Bytes: 1,144,636.
- SHA-256: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb` — exact match with intake provenance.
- Valid EPUB mimetype and ZIP integrity; 55 ZIP members, no CRC failures.
- Ordered EPUB XHTML units: 48 (preface, summary, 45 chapters, afterword).
- All XHTML h1-h4/p blocks: 18,057; nonempty h1-h4/p blocks: 17,790.
- Unit identity: chapter 1 corresponds to source spine unit 3, chapter 45 to unit 47, afterword to unit 48.
- Historical indexing conventions differ: chapter 5 has 400 XHTML blocks / 397 nonempty; chapter 20 has 580 / 577; chapter 41 has 363 / 359. Both complete indexing modes must be recognized without guessing.

**Storage warning:** The original is verified in the current ChatGPT runtime
only. It is not a durable source artifact in the repository. Do not mark the
canonical corpus sealed or report permanent source availability until the
source and its verified extracted artifacts are stored in a permitted private
workspace. While the working GitHub repository is public, do not upload the
original EPUB or a full extracted original corpus there.

**Review warning:** Source identity and structural checks do not certify the
Russian literary translations. All imported drafts remain UNREVIEWED pending
actual hash-bound acceptance and independent Reviewer PASS.
