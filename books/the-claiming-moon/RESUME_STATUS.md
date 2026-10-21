# The Claiming Moon — current translation checkpoint

**UNREVIEWED INTAKE STATE.** This is NOT an initialized or sealed Book Translator workflow workspace. Do not claim a final, reviewed or full-book translation.

- **Original EPUB:** `The_Claiming_Moon.epub`, SHA-256 `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.
- **Pinned workflow revision:** `767c446e79eb112cfc236c0b54b5ef48647b7973`.
- **Original source reading order:** 48 EPUB spine units: preface, summary, chapters 1–45, afterword.
- **Staged Russian translation:** complete unreviewed drafts of preface, summary and Chapters **1–14** inclusive. Current book root: `books/the-claiming-moon/` in private GitHub repository. Drafts stored under `incoming/`.
- Chapter 12: `incoming/chapter-012-ru-draft.md` and `incoming/chapter-012-ru-indexed-000-337.json` — source indices 0–337 / 338. Source `The_Claiming_Moon_split_013.xhtml`, SHA-256 `3f7e04991b6d785899cd4722ef99f54206e27f933150e16388fa3831b7e0406e`.
- Chapter 13: `incoming/chapter-013-ru-draft.md` and `incoming/chapter-013-ru-indexed-000-280.json` — source indices 0–280 / 281. Source `The_Claiming_Moon_split_014.xhtml`, SHA-256 `b566f9059ecfd8eefffb71a8265893afecb631afccc6634dccd2790aad084b83`.
- Chapter 14: `incoming/chapter-014-ru-draft.md` and `incoming/chapter-014-ru-indexed-000-259.json` — source indices 0–259 / 260. Source `The_Claiming_Moon_split_015.xhtml`, SHA-256 `bb530d80cbd866589506d66c0239184e8f0986a25c397356c812b52f71952938`. These files have been saved and checked by reading back from private GitHub.
- **EXACT NEXT TRANSLATION POINT (with conversation attachment available):** Chapter **16**, `The_Claiming_Moon_split_017.xhtml`, source block **0** of 329. Chapter 15 blocks 96–362 were translated but are NOT confirmed remotely staged; see the dated note below.
- **Untranslated:** Chapters **16–45**, then final afterword. Chapter 15 full draft available only as the conversation attachment, not remotely staged.
- **Latest temporary preview EPUB:** `The_Claiming_Moon_ru_chapters_01-14_PREVIEW.epub`, frontmatter and chapters 1–14 only. This is **not the final full-book EPUB**.
- **Canonical workflow blocker:** Original EPUB binary is not yet persisted in private GitHub; missing source seal, provenance-rich `metadata.json`, canonical `progress.json`, source-revision ledger, review PASS evidence. Do not mark the book `reviewed` or `complete`.

- Chapter 15 is INCOMPLETE: its opening 96 blocks have been drafted and persisted, but **do not include it as a complete chapter** in the partial EPUB or mark as full.

This checkpoint supersedes stale next-chapter mentions in older audit entries of `INTAKE.md`.

## 2026-10-21 — Chapter 15 completion in conversation artifact (NOT remotely staged)

- Local source `The_Claiming_Moon.epub` SHA-256: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb` verified.
- Chapter 15 source `The_Claiming_Moon_split_016.xhtml` SHA-256: `8f0c380ad84580e26541b64f5abc8653f0dac9abb117166d4a7293c4f1f64edd`, **363 source text blocks**.
- Russian chapter 15 draft **0–362 of 363 blocks complete** in the current conversation's attached file `The_Claiming_Moon_ru_chapter_15_draft.md`; local SHA-256 `74baa921b3086eadcef10001705ba214deabf41b2a8ead2dcd832ae227af4412`.
- Complete indexed mapping in current conversation's `The_Claiming_Moon_ru_chapter_15_indexed.json`, SHA-256 `83054802456b51351556b478eb12210d5bfa4bd17635260df6d88cd871867863`.
- Preview EPUB from frontmatter and chapters 1–15: `The_Claiming_Moon_ru_chapters_01-15_PREVIEW.epub`, local SHA-256 `383db9586b285157f46d4b9cb9bf0332f1dfb87d1dd3dd53190401ec117aa49e` (not canonical, not full book).
- **IMPORTANT:** The attempt to commit the full Russian Chapter 15 text using the GitHub connector was BLOCKED by the tool. **Do not assume any Chapter 15 completion file exists in private GitHub.** The pre-existing partial indices 0–95 in `incoming/` remain staged; the remaining chapter 15 content is available only as a file attached to this conversation unless later independently persisted. On resume, retrieve that attachment by exact SHA-256 before treating this chapter as recoverable; if unavailable, first recover its missing 96–362 blocks before canonical acceptance.
- **Next not-yet-translated section in the original book: Chapter 16**, `The_Claiming_Moon_split_017.xhtml`, source EPUB spine index 17, source index **0** of 329 (first narrative index 4), SHA-256 `5be2b8d16353114319efda513dcd3764924e55e9797fbe7b5dc5b864c0364e6b`.
- Chapters 16–45 and the original afterword remain untranslated on this trajectory. No chapter has independent PASS review; source binary/sealed corpus/canonical progress remain absent in private GitHub.
