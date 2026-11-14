# A Home in You — terminology correction candidates and review plan

Date: 2026-11-14. Workflow pinned at
`ea9963ca546b7cc7f6aba4dc5350fa19ea7da862`.
Current proposal: [draft PR #108](https://github.com/tim8es/book-translator-private/pull/108).
Prior independent audit: [quality audit](2026-11-14-independent-quality-audit.md).

## Changes prepared, but not accepted

- Updated candidate text in **39 existing `translated/*.md` units** on the
  draft branch, not on the protected book `main` state.
- Replaced **1,326 English character-name tokens** with Cyrillic name forms:
  Dillon (493), Cade (675), Darren (88), Christian (23), Evelyn (12),
  plus Aaron (8), Darius (10), Raven (8) and Marco (9).
- Expanded the book glossary by ten source-verified entries, including the
  four newly detected character names and school/institution/place decisions.
- Replaced the surviving Heritage-school and Loudoun County High School
  passages, plus Panorama Farms and Fenway Bowl proper names, with
  contextual Cyrillic decisions.
- Applied a second manual source-context pass to correct **17 clear Russian
  case/agreement errors** that remained after the initial heuristic pass.
- Added `audits/terminology_preflight.py`, a **read-only** literal English-name
  detector and basic case warning checker. It does not generate literary PASS.

## Checks performed on draft

Scanned all **51** candidate/current Russian unit files across four independent
repository read batches against 39 named entity variants from the glossary and
audit. No literal English spelling of those 39 entity variants remains in the
draft text; intentional Latin company, game, URL and university abbreviations
remain according to the glossary.

Normalized diff review of available GitHub patches: **1,048** changed-line
pairs inspected; 1,047 differ only in replacement/inflection of target
names or designated translated institution labels; one additionally repairs
Russian agreement in a clause about a school sports team. GitHub did not
return the oversized diff for unit 048, which was checked by direct source
comparison for the affected name locations instead.

**These checks are not independent literary review.** Russian case agreement
and semantic completeness may still have errors outside the deterministic
preflight. The book must not be marked quality-complete on this evidence alone.

## Critical pinned-lifecycle blocker

The current `progress.json` on `main` has 51 `reviewed` units, with
translation acceptance and review records bound to **old** exact bytes.
The pinned workflow's `TranslationAcceptanceManager.accept()` verifies an
already reviewed artifact without re-accepting a modified one.
A direct merge of candidate texts would therefore create SHA mismatches in
`progress.json`, old PASS ledger evidence and the output manifest.
The draft PR CI currently **fails closed on this exact mismatch**, correctly.

Do not merge corrected translations into `main` until there is a
provenance-preserving, **explicitly authorized** canonical correction/reopen
transition compatible with the book-pinned revision. Do not modify the
original source, rewrite historical review records, manufacture approvals or
silently change the selected workflow revision.

## To complete the book

1. Resolve the workflow-specific reopen admission path before text merges.
   If the pinned revision lacks a safe path, request an explicit upgrade rather
   than silently reinterpret its contracts.
2. Recheck each changed chapter's Russian case forms **and** source-to-target
   semantic fidelity. Treat the draft as proposed Translator text.
3. Acquire a valid canonical claim, accept the changed translation, then have
   an independent Reviewer produce a fresh source-linked PASS or actionable
   `CORRECTIONS_REQUIRED`; do not reuse stale evidence.
4. Run `terminology_preflight.py --json` and the book's canonical preflight
   after legitimate acceptance. A zero residual-name count does not grant PASS.
5. Rebuild the final EPUB via the pinned workflow and independently verify
   its SHA-256, reading order and source/translation revision identities.

The previous final EPUB remains traceable but is **editorially rejected** by
the audit. The active content on `main` is deliberately unchanged.

No references to characters' ages were modified by this name-correction draft.
