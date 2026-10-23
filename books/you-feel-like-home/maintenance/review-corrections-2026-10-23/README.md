# You Feel Like Home — review corrections (2026-10-23)

## Scope and authority
These are corrected **staging translations**, not canonical `translated/` artifacts and not review-ledger PASS evidence. The immutable source and original historic staged texts have not been overwritten. The book remains pinned to workflow `dca1e7db6974d5c4354e4850ecf82b42cda06f42`.

The corrected Russian reader **PREVIEW** was produced from the user's attached `You_Feel_Like_Home_RU_chapters_1-11.epub` (SHA-256 `6297c4570c776ce6de609926a9c9942bf044b63ebc6e44c0944d7818feeb03d2`). Its SHA-256 is `b747f9d677ba2fc2bc49ec78b4ead286a46f5e6471772a850b9d5434ab3ecdc1`. The binary preview is supplied as a conversation attachment but is **not** stored in GitHub.

## Corrected translation files
- `013-chapter-11-part-05.md` derives from `source-updates/2026-10-22/translated/013-chapter-11-part-05.md` (original Git blob `19beeb991eba5fa9bd1bc7d6f56b8b01a4fb1128`, corrected Git blob `a53952bd81e52d051a511d21d92a8c03baae53d6`). Five contextual phrase edits address profanity softening, a lost corporeal image, the reassurance in `I've got you`, an unnatural `Let go for me` calque, and the `emotional range` comparison.
- `010-chapter-8.md` derives from `source-updates/2026-10-04/translated/010-chapter-8.md` (original Git blob `7f1aefa78c5f81747291f63dda1942955db03646`, corrected Git blob `3de22da846b3101a69520ae318f80acad8c8fb7c`). One edit restores the colloquial severity of `Every time you fucked up`.
- Chapter 9's `pain in the fucking ass` is an idiomatic translation judgment, not a forced 1:1 profanity replacement; leave the historic Russian text unchanged.

## Reader EPUB fixes and checks
- Russian mojibake corrected in `OEBPS/nav.xhtml`, `OEBPS/toc.ncx`, and `OEBPS/content.opf`.
- ZIP CRC, XML parsing, 13 reading-order XHTML documents, 13 navigation entries and their destinations, and mandatory uncompressed first `mimetype` entry all passed.
- Original in-text anchor markup, semantic block quotes and section rules were **not reconstructed**: the preserved exact latest English source is not available for source-structure equivalence verification.

## Workflow blocking conditions
`metadata.json`/`progress.json` still refer to the older nine-unit edition; the current latest-source SHA `8efac63cf78817b821008ee001fb33aea40b29d5c8c9d69cb9f52f14b0bd28a2` cannot be independently recovered from this workspace; the original binary and complete sealed corpus are missing, and `review-ledger.json` contains no PASS. Do not claim canonical review, emit `review-record PASS`, update chapter statuses, or substitute an online edition to bypass source identity.

**Reviewer finding:** `CORRECTIONS_REQUIRED` at the book-workflow level pending full exact-source comparison and accepted transition. These amended staging artifacts and the corrected reader preview are concrete fixes to the identified review findings, not a complete literary-review acceptance.
