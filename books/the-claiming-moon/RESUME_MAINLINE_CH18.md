> **АРХИВНАЯ ЗАПИСЬ — НЕ ТЕКУЩЕЕ СОСТОЯНИЕ (22 октября 2026 г.)**
>
> Дальнейший текст сохранён как исторический журнал прежних чат-сессий. Его утверждения о незаписанном исходном EPUB, отсутствии канонической инициализации, состоянии переводов и «следующей главе» **устарели**. Оригинальный EPUB сохранён и подтверждён по SHA-256, книга инициализирована.
>
> Актуальные источники истины: `metadata.json`, `progress.json`, `source-manifest.json`, `source-revisions.json`, `review-ledger.json` и реальные файлы `translated/`. Перед работой выполняйте `python scripts/book.py validate the-claiming-moon`, `python scripts/corpus.py verify the-claiming-moon` и `python scripts/book.py resume the-claiming-moon --json`. Не повышайте статусы и не восстанавливайте «точку продолжения» по историческим заметкам.

---

# The Claiming Moon — sequential translation checkpoint, 2026-10-21

- Source English EPUB sha256: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.
- Workflow pinned revision: `767c446e79eb112cfc236c0b54b5ef48647b7973`.
- Original source reading order contains preface, summary, narrative chapters 1–45, and afterword (48 units).
- Sequential Russian draft through **Chapter 18**. Chapter 18 source `The_Claiming_Moon_split_019.xhtml`, sha256 `a70bd1a7aa065c02a6ab4ac70291c4a7d62516e2c149b6a5812bee036a7fe769`, has **262/262** indexed Russian draft blocks. `incoming/chapter-018-ru-draft.md` was saved and read back exactly, commit `8b6b69329b8807bee4948107cf54d39bb6701640`.
- Local preview `The_Claiming_Moon_ru_chapters_01-18_PREVIEW.epub` includes frontmatter and Chapters 1–18; ZIP integrity, EPUB mimetype, XML, TOC, spine and chapter count validated. **It is not the complete novel.**
- **EXACT NEXT sequential unit:** Chapter **19**, source `The_Claiming_Moon_split_020.xhtml`, original sha256 `8fdcceaa2cb800fe01b151e8fd818e6a44d634e44db71d6989d948b02cb5385c`. **Start at source text block index 0 of 324**, first narrative block 4. Chapter title: `To Be Loved, and to Be Known`.
- Remaining sequential gap: Chapters **19–45**, then final afterword. Some independently scoped drafts for later chapters are present in `incoming/`, but they require source-identity and full-coverage reconciliation before acceptance.
- **Important durability gap:** Chapter 15 draft indices 96–362 are only in a conversation attachment/local draft; an earlier attempt to persist those blocks in private GitHub was blocked. Indices 0–95 are already saved there. Recover source-verified Chapter 15 indexed draft before claiming fully durable consecutive coverage.
- **Not canonical:** Book workspace is intake-only, original source EPUB has not been preserved or sealed in the private repository; no `metadata.json`, `progress.json`, review ledger or independent reviewer PASS evidence. All existing drafts are unreviewed. Never declare the full translation complete, nor use public workflow repo for book content.

This checkpoint supersedes older next-chapter pointers in `RESUME_STATUS.md` and `INTAKE.md` for this sequential scope.
