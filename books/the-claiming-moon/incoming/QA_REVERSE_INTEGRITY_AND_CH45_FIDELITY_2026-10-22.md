# The Claiming Moon — reverse integrity verification and chapter 45 literary QA

Date: 2026-10-22. Scope: canonical book narrative chapters 31–45 (unit IDs chapter-000033 through chapter-000047). Book: `books/the-claiming-moon/`.

## Authority and concurrency

- Pinned workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789`.
- Original source revision: `source-000001`; full original EPUB identity in `metadata.json`.
- Progress document checked at GitHub blob `a4eaffe8a5a0f076b95f9afdd232f34fc319ed88`.
- Latest status snapshot on this report: 3 reviewed / 41 translated / 4 extracted.
- `.workflow/claims/` contained only a Translator claim for `chapter-000021` (narrative Chapter 19). No new claims or lifecycle transitions were made by this technical QA.
- Scope remains deliberately separate from the agent working earlier chapters.

## Complete SHA-256 integrity verification of the scoped 15 chapters

The full canonical source and translation Markdown files for all narrative chapters **31 through 45** were freshly read from GitHub. Independently computed UTF-8 SHA-256 was checked against the accepted durable state for **every** chapter.

| Narrative chapter | Source digest matches sealed source-manifest | Source digest matches translation acceptance | Translation digest matches translation acceptance |
|---:|:---:|:---:|:---:|
| 31 | YES | YES | YES |
| 32 | YES | YES | YES |
| 33 | YES | YES | YES |
| 34 | YES | YES | YES |
| 35 | YES | YES | YES |
| 36 | YES | YES | YES |
| 37 | YES | YES | YES |
| 38 | YES | YES | YES |
| 39 | YES | YES | YES |
| 40 | YES | YES | YES |
| 41 | YES | YES | YES |
| 42 | YES | YES | YES |
| 43 | YES | YES | YES |
| 44 | YES | YES | YES |
| 45 | YES | YES | YES |

Result: **15/15 source artifacts** match both the sealed source manifest and each chapter's current translation acceptance. **15/15 translation artifacts** match their accepted translation SHA-256. This confirms storage integrity and proven accepted artifact identity only, **not** full original-to-Russian semantic coverage or Reviewer PASS.

This is a scoped verification. Full-book `book.py validate` and `corpus.py verify` were **not** executed against all 48 units, as a connected local checkout capable of running the canonical scripts was not available.

## Chapter 45 — further source-comparison finding

A new spot-check at the return-journey scene found a concrete semantic error:

- Source: `He needed to hold them and needed to feel how small they were against his chest` (Yoongi missing his pups).
- Accepted Russian: `Нужно было подержать их, ощутить, какими маленькими они становятся у него на груди`.
- Issue: source describes their small size *while held against his chest*; Russian `становятся` adds a false change-in-size meaning.
- Proposed correction: `Ему нужно было подержать их на руках, почувствовать, какие они ещё маленькие, прижав к груди`, maintaining the rest of the scene.
- This is an actionable literary QA finding. Chapter 45 remains **unreviewed**: a sampled source-to-target comparison is not sufficient for PASS.

## Staged corrected Chapter 45 draft

- Previously corrected draft (four edits): `incoming/047-chapter-45-qa-corrected-unreviewed-2026-10-22.md`.
- New corrected draft (**five** total targeted edits): `incoming/047-chapter-45-qa-corrected-unreviewed-v2-2026-10-22.md`.
- New draft fetched after writing; confirmed it equals the previous version plus exactly the new pups-paragraph correction.
- Previous corrections preserve an omitted author note; restore Taehyung's kitchen countertop gesture; preserve a purposeful weather repetition; and clarify the male referent in Namjoon/Jin dialogue.
- All chapter 31–44 unreviewed correction drafts remain in `incoming/`; see `incoming/QA_REVERSE_STAGING_CHECKPOINT_2026-10-22.md` for links.
- **No** files under `translated/`, `extracted/`, `source/` and no `progress.json` or `review-ledger.json` changes were made here.

## Required next actions

1. Refresh repository state and verify live claims; avoid mutating another agent's work.
2. When capable of enforcing the pinned workflow's durable Translator claim and acceptance rules, promote verified corrections unit-by-unit from incoming drafts, with SHA-bound compare-and-swap; do not directly overwrite accepted translation files.
3. Run an independent full-source literary Reviewer pass for each chapter from 45 backward; record PASS only after exhaustive comparison; otherwise persist specific CORRECTIONS_REQUIRED findings through the claimed review workflow.
4. Build final EPUB only after all 48 units are reviewed with current accepted PASS evidence, and canonical validation and source verification pass.

This report is **technical and targeted literary QA**, not full-book completion or final literary certification.
