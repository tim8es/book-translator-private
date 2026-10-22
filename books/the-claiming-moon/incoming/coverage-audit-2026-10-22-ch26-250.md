# The Claiming Moon — coverage and conflict audit, 2026-10-22

Workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789` (book-pinned; not upgraded).

This file is a **draft coverage inventory**, not a Reviewer PASS, translation-acceptance certificate, whole-book semantic audit, or an EPUB completion marker. Status authority remains `progress.json`.

## Current durable status (before staging the chapter 26 continuation)

- Total source units: 48 (including 45 narrative chapters).
- `reviewed`: 3 ancillary units; **0 narrative chapters independently passed**.
- `translated`: 41 units; `extracted`: 4 narrative chapters (19, 26, 27, 29).
- Metadata workflow pin and sealed source-manifest contain 48 units; source unit paths and progress identifiers were checked against manifests.
- Chapter 15 latest accepted SHA-256: `8e5d93b8da3f0f8ecc3dada091845e0b520ef8686c26de04d89bcdbf52171717`; its three `CORRECTIONS_REQUIRED` records refer to previous revisions. A complete independent review of this exact latest SHA is still required.

## Four extracted chapters: verified incoming drafts

| Narrative chapter | Source blocks | Available verified contiguous IDs | Next missing | Warnings |
| --- | ---: | --- | ---: | --- |
| 19 | 324 (0–323) | Fragments cover 0–125, **with incompatible overlapping alternatives** | 126 | Do not auto-combine; compare and choose line-by-line, or retranslate disputed blocks |
| 26 | 570 (0–569) | **0–250**, without gaps or duplicates inside the chosen ordered seven Markdown parts | 251 | 251–569 still lack confirmed staged translation |
| 27 | 341 (0–340) | 0–90, two GitHub Markdown parts | 91 | An older note refers to an outside-of-repository draft for 91–340; its bytes have not been recovered/verified in canonical GitHub |
| 29 | 456 (0–455) | 0–290, nine GitHub Markdown parts | 291 | 291–455 remain |

### Chapter 26: immutable source and newly staged material

The newly staged, source-indexed translations are:

- `incoming/chapter-026-ru-draft.part-05.md` — 161–190 (30 blocks);
- `incoming/chapter-026-ru-draft.part-06.md` — 191–224 (34 blocks);
- `incoming/chapter-026-ru-draft.part-07.md` — 225–250 (26 blocks).

Together with the five earlier incoming files (0–160), the technical index inventory is **251/570 blocks**, i.e. `0–250` continuously. New files were verified by GitHub read-back and unique, consecutive `<!-- source-block N -->` markers. Their content has **not** been reviewed end-to-end; it is not a canonical accepted translation. Keep `chapter-000028` at `extracted` until all 570 blocks are rendered, completeness reviewed, and accepted under a live translator claim.

### Chapter 19: conflicting draft streams

The following two families are not text-identical:

- `chapter-019-ru-draft-indexed-000-023.json` plus `...024-050.json`;
- `chapter-019-ru-indexed-000-026.json` plus `...027-050.json` (and `chapter-019-ru-assembled-indexed-000-050.json` based on this family).

**46 out of 51** aligned blocks 0–50 differ by text. A second overlap in draft files `040–059`, `060–079`, `080–099` versus alternate `051–075`, `076–100` contains **45 conflicting indexes**. This is evidence of competing revisions, not evidence that one is approved. Before any acceptance, select/source-compare and consolidate exactly one translation per index, then proceed from the selected tail and review the whole narrative chapter.

### QA limitations and acceptance gates

- Presence, numeric contiguity and file-size checks do **not** demonstrate literary fidelity.
- The 41 `translated` units are not independent literary PASS. Chapter 15 in particular needs a fresh whole-chapter Reviewer pass against its final accepted bytes.
- Review all author notes, section dividers, dialogue attribution, recurring terminology and narration changes before promoting a chapter to `reviewed`.
- No final EPUB yet; do not represent a preview as a completed verified book.

## Next durable actions

1. Continue chapter 26 from source block 251, preserving the active chapter's draft boundaries and the source text.
2. Reconcile chapter 19 conflicting blocks, then finish 126–323.
3. Recover and verify any outside-file material for chapter 27 if possible; otherwise complete from 91.
4. Complete chapter 29 from 291.
5. Require technical acceptance and independent source-comparison evidence for every final canonical unit, then assemble and validate the EPUB.
