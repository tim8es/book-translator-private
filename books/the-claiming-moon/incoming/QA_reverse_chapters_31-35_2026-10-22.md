# The Claiming Moon — reverse technical QA, narrative chapters 31–35

Date: 2026-10-22. Preliminary Orchestrator file and source-note check, **not** an independent literary Reviewer PASS.

## Provenance and scope
- Pinned workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789`.
- Book: `tim8es/book-translator-private/books/the-claiming-moon/`.
- Source revision: `source-000001`, with original EPUB identity recorded in book metadata.
- Examined canonical source files `extracted/033` through `extracted/037` and corresponding accepted Russian translations `translated/033` through `translated/037` (narrative chapters 31–35). Each file was read, with openings, endings and author notes examined.
- This pass did not execute full `book.py validate` or `corpus.py verify` and did not perform a complete paragraph-by-paragraph literary review. Current statuses must always be re-read from `progress.json`.

## Results and confirmed defects

| Narrative chapter | Unit | Source nonblank Markdown paragraphs | Russian paragraphs | Confirmed issue |
|---|---:|---:|---:|---|
| 31 — Hollowed | 33 | 416 | 455 | Opening author note omitted; added nonsource `## Текст главы` heading |
| 32 — The Things That Follow Us | 34 | 774 | 780 | Opening author note omitted |
| 33 — The Night Before War | 35 | 276 | 274 | Opening author note omitted |
| 34 — A Miracle Written in Blood | 36 | 334 | 332 | Opening author note omitted |
| 35 — A Monster for His Mate | 37 | 267 | 265 | Opening author note omitted |

For all five chapters, the source's opening `Chapter Notes` section contains **`See the end of the chapter for more notes`** (chapter 33: `See the end of the chapter for notes`), while the corresponding opening Russian section omits it. This is a verified, repeated source-author-note omission. The chapter-ending author-note sections themselves are present in the Russian text.

Proposed exact renderings in the corresponding opening notes:
- `See the end of the chapter for more notes` → `Дополнительные примечания автора — в конце главы.`
- `See the end of the chapter for notes` → `Примечания автора — в конце главы.`

Chapter 31's standalone Russian `## Текст главы` appears after the translated opening note but is not a heading in the corresponding source; remove unless subsequent source inspection identifies authorial support. The **416 vs 455** paragraph counts in this chapter also warrant inspection for unintended restructuring, but paragraph count alone does not establish a narrative omission.

The same omission pattern was independently confirmed in every following narrative chapter **36–45**; see `incoming/QA_reverse_chapters_36-45_2026-10-22.md`.

## Acceptance discipline
- Do not edit accepted canonical translation bytes in place, do not forge hash-bound acceptance, and do not change `reviewed` status without independent comparison.
- Before applying corrections, refresh claims, check existing parallel work, acquire durable Translator claims for the specific unit(s), make targeted changes, run `accept-translation` and release, then use independent Reviewer claims, `review-record`, and `accept-review` if and only if fully reviewed.
- Source completeness and end notes still need chapter-by-chapter semantic verification. This report is not a sign-off.
- The other agent's earlier-chapter work is outside this report's mutation scope.

No canonical translation, source, progress, glossary, style-guide, or review ledger was changed by this report.
