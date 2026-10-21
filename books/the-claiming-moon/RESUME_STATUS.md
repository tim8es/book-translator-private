# The Claiming Moon — current translation checkpoint

**This is a staged intake, not an initialized Book Translator workflow workspace. Do not mark any book unit reviewed or complete.**

- Original EPUB: `The_Claiming_Moon.epub` (source sha256 `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`).
- Source structure: 48 spine units = preface + summary + 45 narrative chapters + afterword.
- Pinned Book Translator workflow revision: `767c446e79eb112cfc236c0b54b5ef48647b7973`.
- Russian drafts for preface + summary and narrative chapters **1–11** exist in private GitHub `incoming/`. These are **not independently literary-reviewed** and not accepted into canonical workflow state.
- For Chapter 11 (647 source blocks): join `incoming/chapter-011-ru-PARTIAL-indexed-000-359.json` indices 0–359 with `incoming/chapter-011-ru-completion-blocks-360-646.json` indices 360–646; this gives **647/647** Russian draft blocks; readbacks verified.
- Chapter 12 is **partial**: indices **0–140** (141 of 338 blocks) have Russian draft counterparts in `incoming/chapter-012-ru-PARTIAL-indexed-000-140.json`. The Markdown view is `incoming/chapter-012-ru-PARTIAL-blocks-000-140.md`.
- **NEXT ACTION / EXACT RESUME:** Chapter **12**, source `The_Claiming_Moon_split_013.xhtml`, next source block **141**. Continue from block 141, not from the beginning. XHTML SHA-256 `3f7e04991b6d785899cd4722ef99f54206e27f933150e16388fa3831b7e0406e`.
- Once Chapter 12 is complete: translate Chapters **13–45** and the source **afterword** (spine index 47, `The_Claiming_Moon_split_047.xhtml`).
- Most recent **local preview EPUB** includes preface, summary and complete drafts of Chapters **1–11**. Chapter 12 partial is separate. The preview is not the complete book.
- **Known blocker for canonical workflow:** original EPUB binary has not been preserved in this private repository; `metadata.json`, `progress.json`, sealed source manifest, source revision ledger and current literary PASS review evidence have not been created. Do not claim full-book export or verified complete translation.
- Avoid mixing source files or drafts with the public workflow repository. Source bytes must be source-integrity verified and preserved before canonical initialization.

This checkpoint supersedes older historical next-chapter statements in `INTAKE.md`; do not use those older statements as the current resume location.
