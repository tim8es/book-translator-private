# The Claiming Moon — front-of-book preflight, 2026-10-22

## Scope and authority

- Book: `books/the-claiming-moon` in `tim8es/book-translator-private`.
- Pinned workflow: `5e0731da8b7ca81ada5316ed536a8a954008b789` (as recorded in `metadata.json.workflow.resolved_revision`); **no workflow upgrade**.
- Active original revision: `source-000001`, original EPUB expected SHA-256 `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.
- This audit covers **technical state and bounded editorial spot-checks from the beginning**, not a full independent Reviewer examination of any chapter.
- Parallel agent is working from the end; avoid writing to its chapter artifacts and global mutable state. This isolated audit file is informational and does not replace machine evidence.

## Durable progress snapshot

- Total original reading-order units: `48`.
- Lifecycle states from `progress.json`: `reviewed=3`, `translated=41`, `extracted=4`, `pending=0`.
- Earliest narrative chapter lacking Reviewer PASS: reading-order unit 3, `chapter-000003` (Chapter 1: Silver Moons, Crimson Throats).
- Existing `.workflow/claims` paths at the snapshot: `chapter-000021.json`.
- Sections currently marked `extracted`: `chapter-000021` (Chapter 19: Chapter 19 : To Be Loved, and to Be Known); `chapter-000028` (Chapter 26: Chapter 26 : The Chase); `chapter-000029` (Chapter 27: Chapter 27 : Worth More Than Gold); `chapter-000031` (Chapter 29: Chapter 29 : Fuck Me, Alpha).
- The 48 extracted paths are listed in `source-manifest.json` and 48 extracted files are present in the GitHub directory listing. The `translated/` directory listing contains 44 numbered Markdown translation files, corresponding to the 44 translated/reviewed units.
- This does **not** establish that the preserved binary EPUB, every extracted SHA-256, and every accepted translation SHA-256 were all verified in this run.

## Verified exact artifact identity: Chapter 1

- `extracted/003-chapter-1-chapter-1-silver-moons-crimson-throats.md`: computed SHA-256 `f278638e9722b0a67841eafeec79afbf525421a32dce91cac04be6f06c4d98b1`; matches the entry in `source-manifest.json`.
- `translated/003-chapter-1-chapter-1-silver-moons-crimson-throats.md`: computed SHA-256 `a7821571c611a1deac6d48d8bbfe608269118f3d71506f932211d659472ad30c`; matches `progress.json.translation_acceptance.translation_sha256`.
- The same artifacts contain 203 and 200 blank-line-delimited blocks respectively; counts alone **cannot** establish literary completeness.

## Editorial findings / preparatory checklist

1. **Original auxiliary note / navigation marker (Chapter 1, also sampled in Chapters 2–4):** the English chapter includes `See the end of the chapter for more notes`; the canonical Russian translation omits an equivalent. End-of-chapter author notes themselves **are present** in Russian on the sampled chapters. Low-severity structural discrepancy; decide whether to retain a translated direction in the final reading flow. Do not remove source-authored notes.
2. **Kayla reference in Chapter 1:** the original switches pronouns (`his mending` versus `her neighbor`). The Russian text initially uses masculine agreement. The source is internally inconsistent; check the wider local context and later canonical uses before a terminology/character decision. Avoid an unsupported global replacement.
3. **Russian dialogue layout in Chapter 1:** multiple dialogue introductions and replies share a paragraph with prior narration in an awkward layout. Target-language polish should adjust dialogue punctuation/paragraph boundaries **without** changing speaker assignments or source semantics.
4. **Do not take a clean excerpt as a literary PASS.** Chapter 1 source/Russian openings, selected middle sections, and ending were compared; Chapters 2–6 were sampled at the beginning, Chapters 1–4 at the end. Full sequential original-to-Russian checking remains to be done.
5. **Known quality debt:** `style-guide.md` flags service/translator artifacts or earlier header cleanup in several chapters and prior serious source-comparison concerns in Chapter 15/17. Verify current canonical bytes independently before resolving. Existing historical Markdown notes are not review-ledger PASS evidence.

## Execution constraints and next safe operation

- The GitHub connector can read/write durable UTF-8 book files with create-if-absent and SHA-guarded replacement.
- The local shell cannot resolve github.com and therefore cannot run the pinned canonical `scripts/book.py validate`, `scripts/corpus.py verify`, or `scripts/book.py resume` on a trusted checked-out workspace in this run. Partial GitHub directory/identity checks above are not represented as a complete corpus preflight.
- **No live claim was acquired, no canonical translation was modified, and no review ledger or lifecycle state was advanced** by this audit.
- Before literary Reviewer work: complete corpus/source preflight through a supported backend, inspect current claims (especially `chapter-000021`), and acquire a durable Reviewer claim for `chapter-000003`. Only after a full independent original-to-translation comparison may a `PASS` be recorded and promoted. Otherwise provide actionable `CORRECTIONS_REQUIRED` feedback and repeat the Translator/Reviewer cycle.
- Keep these front-of-book operations disjoint from the other agent's end-of-book scope.
