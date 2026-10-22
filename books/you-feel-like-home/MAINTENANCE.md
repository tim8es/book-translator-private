# You Feel Like Home — migration and workspace status (2026-10-22)

## Verified inputs
- Original English EPUB supplied in chat: `You_Feel_Like_Home 2.epub`; SHA-256 `8efac63cf78817b821008ee001fb33aea40b29d5c8c9d69cb9f52f14b0bd28a2`; 191,460 bytes; ZIP CRC passed.
- 14 spine documents: preface, book description, Chapters 1–11, afterword. This is the **latest observed source edition**, not the original nine-unit canonical edition.
- Existing Russian output through Chapter 11: `output/You_Feel_Like_Home_RU_chapters_1-11.epub` (Git blob `49e48608bbbfc2b5dbf67524eeacd01a338e95ad`). A previously staged note incorrectly said it was not assembled.
- Current book's `metadata.json.workflow.resolved_revision`: `dca1e7db6974d5c4354e4850ecf82b42cda06f42`.
- Requested target workflow SHA: `0fe7fd86356d27dafbb409daa7e5ece23fdf62f4`; **not yet promoted into book metadata**.

## Authoritative status and blockers
- `metadata.json`/`progress.json` still represent an older nine-unit book, with all units `extracted`.
- The sealed old extracted corpus is incomplete (3 of 9 files); its exact source EPUB SHA `cfe3a150553340a1c92d7f823ac0821e2307fbda43dc040f6e11287fae4e2df3` is not preserved here.
- Historical chapter translations and newer editions are in `source-updates/`, **not** accepted canonical `translated/` state.
- `review-ledger.json` has no current PASS. Historical reviews and previously exported EPUBs do not imply workflow review promotion.
- Current EPUB source-coverage contract rejects unsupported semantic markup. The latest original contains `a`, `blockquote`, `br`, `hr`, `span`, definition-list markup, etc.; a successful independent `source-coverage.json` has **not** been produced.
- The exact latest English binary is available from the chat attachment, but has **not** been committed to GitHub; no claim of a GitHub-persisted original is made.

## Non-destructive cleanup
1. Historical staging is documented in `source-updates/README.md`, without renumbering, deleting or promoting chapter translations.
2. Source details and fidelity barriers are recorded in `maintenance/source-inventory-2026-10-22.json`.
3. Three disposable upload probes from 2026-10-11 have been removed from this maintenance branch; their content remains recoverable from Git history.
4. All four prior EPUB outputs, literary memory files, dated translation drafts and current machine state are preserved.

## Safe path to finish the upgrade
1. Store the **exact** latest original under an immutable source-revision path in an authorized private workspace. Do not overwrite the old edition.
2. Verify all 14 reading-order units and fix the EPUB extraction/coverage blocker through an approved workflow revision (never fabricate `source-coverage.json`).
3. Run source-aware migration in an isolated workspace, then seal and validate. Restore glossary/style decisions and stage all matching historical translation drafts for admission without manufacturing PASS.
4. Use the actual Translator acceptance and independent Reviewer transitions for each unit; compare hashes and track stable `unit_id`s.
5. Rebuild and test chapter order, typography, spacing and internal links. Promote state and merge only after guards pass.

**Status: maintenance audit + safe cleanup only. Canonical book workflow migration is BLOCKED, not complete.**
