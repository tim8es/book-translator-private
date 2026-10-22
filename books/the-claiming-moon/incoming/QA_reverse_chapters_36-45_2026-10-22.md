# The Claiming Moon — reverse technical QA, narrative chapters 36–45

Date: 2026-10-22. Scope: chapter 45 backward toward chapter 36. This is an **orchestrator preflight and preliminary structural/source spot-check**, **not** an independent exhaustive literary Reviewer PASS, and it does not advance any lifecycle states.

## Durable authority
- Book: `books/the-claiming-moon/` in `tim8es/book-translator-private`.
- Workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789`, read from `metadata.json.workflow.resolved_revision`; do not silently upgrade.
- Active source revision: `source-000001`; original source SHA-256: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.
- Progress snapshot at audit start: 48 units; 3 `reviewed`, 41 `translated`, 4 `extracted`. This snapshot may change as other agents work. Read `progress.json` afresh before any state transition.
- Explicitly avoid the other agent's ongoing earlier-chapter work and all shared-state mutations without current claims and compare-and-swap.
- Historical `INTAKE.md`, `RESUME_STATUS.md`, `incoming/` drafts and `outputs/` previews are not authoritative lifecycle state.

## Technical results
- Canonical source and translation files for narrative chapters **36–45** (book units 38–47) were re-opened. Every examined translated file was non-empty, had its narrative ending and author-end-note section available, and had no detected generic draft/service completion placeholders in the sampled headings/endings.
- For chapters **41–45**, and the **Afterword** (units 43–48), computed UTF-8 SHA-256 digests for both retrieved canonical files: all six sources match `source-manifest.json`, and both source and Russian translation hashes match their exact `progress.json.translation_acceptance` identities.
- Chapters **36–40** underwent a limited structural/header/tail review only; their current full-file SHA-256 digests have **not** been independently recomputed in this pass.
- Approximate non-empty Markdown paragraph counts, source → translation: chapter 36 **537→535**; 37 **317→315**; 38 **460→458**; 39 **340→338**; 40 **418→416**; 41 **361→359**; 42 **297→295**; 43 **316→314**; 44 **447→445**; 45 **687→685**. The near-equal counts are **only a structural indicator**. Source metadata/title handling and merged or omitted text can conceal missing content; this is not proof of complete semantic coverage.
- End-of-chapter author notes are present in all ten examined translations, including extensive notes in chapter 38 and chapter 45. Chapter 45 begins with the source's announcement of five future epilogues, but these epilogues are **not** separate units in the current 48-unit source revision. Do not invent them during build.
- The afterword is already `reviewed`; review again only if its accepted artifact changes or there is substantive new evidence of an issue.

## Confirmed omissions needing correction

### Narrative chapter 39 (unit 41, `translated/041-chapter-39-chapter-39-the-life-we-get-to-keep.md`)
Source opening author note after `Chapter Notes`: `See the end of the chapter for notes`.
The Russian file has `Примечания к главе` followed by empty space; the note itself is absent. Proposed faithful one-line correction: `Примечания автора — в конце главы.`

### Narrative chapter 45 (unit 47, `translated/047-chapter-45-chapter-45-a-little-less-than-forever.md`)
Source opening author note: `See the end of the chapter for more notes`.
The opening Russian author's note translates the surrounding announcement but omits that sentence. Proposed faithful one-line correction: `Дополнительные примечания — в конце главы.`

These are concrete source-text omissions, albeit small. Do **not** report `PASS` for affected chapters until corrected and independently re-reviewed. Do **not** edit canonical accepted translations in place; use the documented Translator claim, artifact write, `accept-translation`, Reviewer claim, review ledger evidence, and `accept-review` flow, bound to current revisions.

## Expanded systematic finding — all chapters 36–45

A follow-up opening-note comparison found the **same omitted source-authored line in every narrative chapter 36–45**, not only 39 and 45. In each chapter, the source starts with `Chapter Notes`, sometimes with a content warning or other author note, then a separate `See the end of the chapter for more notes` (chapter 39 uses `for notes`) before narrative prose. The Russian opening skips that separate instruction. The story body still appears afterward; the omission is **the author-note navigation sentence**, not a demonstrated missing narrative scene.

Affected units and narrative chapters: unit 38/chapter 36; 39/37; 40/38; 41/39; 42/40; 43/41; 44/42; 45/43; 46/44; 47/45. The omitted text was confirmed by comparing the opening original and Russian text for every unit. This finding supersedes the earlier implication that chapters 39 and 45 alone were affected.

Correction proposal for each chapter (in its opening author-notes block, following any other opening notes):
- Source `See the end of the chapter for more notes` → `Дополнительные примечания автора — в конце главы.`
- Source `See the end of the chapter for notes` → `Примечания автора — в конце главы.`

The same issue was also found in **chapters 31–35**; see the separate reverse technical QA record for that range. This is a systematic pattern that warrants a source-note check in the chapters handled by the other agent as well, **without independently editing their active scope**.

## Next reverse-work order

1. Refresh source/progress/claims state; run full canonical corpus preflight (`book.py validate`, `corpus.py verify`) in a capable workspace. This connector-only run independently checked selected artifact hashes but did **not** execute those Python commands or the complete 48-unit corpus verification.
2. Preserve this separate backward scope: literary Reviewer comparison of chapter 45, then 44, 43, 42, 41; continue with chapter 40 backward. Acquire durable unit claims before literary work, avoid conflicts with the front-working agent. Each chapter's entire original and Russian translation must be checked paragraph by paragraph before `PASS`.
3. Correct chapter 45 and chapter 39 notes via the canonical Translator boundary and re-review changed artifacts. Track any other source/target fidelity, modality, viewpoint, author-notes, dialogue, or terminology defects found.
4. Do not claim final EPUB readiness until **all 48** units are currently `reviewed` with hash-bound PASS evidence and the canonical builder succeeds.

No canonical source, translation, `progress.json`, or review-ledger file was modified by this audit.
