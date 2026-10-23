# You Feel Like Home — original-verified formatting correction checkpoint (2026-10-24)

This note describes an actual local EPUB correction artifact, not accepted canonical book state.

- **Source original:** user-uploaded `You_Feel_Like_Home 2.epub`, SHA-256 `8efac63cf78817b821008ee001fb33aea40b29d5c8c9d69cb9f52f14b0bd28a2`, size 191460 bytes, ZIP CRC PASS, 14 XHTML source reading-order units.
- **Input RU preview:** `You_Feel_Like_Home_RU_chapters_1-11_review_corrected_PREVIEW.epub`, SHA-256 `8d60a267ed87045addda160150fe390e45cbb4c0dbd4962cf96256c3ec1fbe7e`.
- **Output RU preview:** `You_Feel_Like_Home_RU_1-11_format_fidelity_corrected_PREVIEW.epub`, SHA-256 `f304fc9d6c7242f7835aa9501a21044e728948c1aea037e85b9edae0f2e5ba1d`. Generated in conversation and supplied to user; this binary is not committed to GitHub.
- **Output checks:** ZIP CRC PASS, all XML documents parse, archive retains 14 spine units and all file members, 38 relative internal links resolve to existing files and IDs.
- **Original XHTML markup parity:** 14 units checked, with exact per-unit counts of semantic `<blockquote>`, `<hr>`, and `<em>` in original EN and corrected RU preview (note formatting only, not a complete paragraph/sentence literary review).
- **Fixes:** 14 author/summary blockquote groups restored; 3 `<hr>` scene switches restored (Ch9 x2, Ch10 x1); Ch9 and Ch11 headings normalized to source `<h2>`; excess invented emphasis removed (Chs 3,4,6 and 11), while the Ch11 two-part note *Didn't want to wake you ... — Arian.* is marked up in italics rather than visible literal asterisks. One duplicated notes heading removed.
- **Russian prose unchanged by this formatting pass**, except removal of the two erroneous literal `*` characters surrounding Ch11's italicized note and the redundant notes heading. Earlier literary fixes to Chs 2, 6, 8, 9, 10 and 11 remain in the preview.
- **Limitations:** The original inline `<br>` spacing is not yet proven equivalent; complete independent paragraph-by-paragraph / sentence-by-sentence literary review of all 11 story chapters is not certified.
- **Canonical book machine state:** `metadata.json.workflow.resolved_revision` remains `dca1e7db6974d5c4354e4850ecf82b42cda06f42`; its old 9-unit source corpus is incomplete and latest 14-unit source edition has not been admitted into canonical state. `progress.json` and `review-ledger.json` remain unchanged, no independent exact PASS recorded.

To resume formally, safely reconcile exact source edition/provenance and complete source corpus in one batch, accept current full-length translations, run the pinned Reviewer protocol over each whole chapter, then generate hash-bound PASS evidence and promote reviewed states only when its guards pass. Do not treat this note or preview as a literary PASS or as the final book.
