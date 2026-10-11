# Source update — 2026-10-11

This update stages the new `You_Feel_Like_Home 3.epub`, which adds **Chapter 9** before the Afterword.

- Preserved exact user-provided EPUB: `source/You_Feel_Like_Home 3.epub` (SHA-256: `071b365ece660dce8ed9bf3a51f47eb4f6d1c4c029138c45a3d998f580d0d77d`)
- New English chapter extraction: `extracted/011-chapter-9.md` (SHA-256: `e354317dfbb0467a025b78f0580eeaae0e318712b9428b72001ccca4664cc171`)
- Complete Russian Chapter 9 translation: `translated/011-chapter-9.md` (SHA-256: `84baa3acf5f5da94d2f7fdae098947480af405f5a4c63fa963450b727cbc0329`)
- Russian compilation through Chapter 9: `../../output/You_Feel_Like_Home_RU_chapters_1-9.epub` (SHA-256: `b2703f008c9cda9df6ec1585d34fb9b72291bb3fa2dbde4878e92bed51969a3f`)

The pre-existing Russian Chapters 1–8 are retained from the prior translated edition. The EPUB was checked for ZIP integrity, valid EPUB XML resources, spine/TOC order, and placement of Chapter 9 before the Afterword.

This is a **staged source update**. The original sealed source corpus, canonical `source-manifest.json`, `metadata.json`, `progress.json`, and `review-ledger.json` remain unchanged. A successful EPUB build is not a `PASS` literary review, and no authoritative independent review has been recorded for this new chapter.

Previous translation transport parts remain for historical traceability; `translated/011-chapter-9.md` is now the complete, canonical artifact *within this staged update*.
