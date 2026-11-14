# A Home in You — independent post-delivery quality audit

Audit date: 2026-11-14 (UTC+3). Book: `a-home-in-you-a-mm-small-town-stepbrother-romance`.
Book workflow revision: `ea9963ca546b7cc7f6aba4dc5350fa19ea7da862`.

**Editorial QA result: FAIL (critical name-localization and terminology consistency defects).**
This is an external audit record, **not** a canonical review ledger entry, a new
translation acceptance, a source revision, or a workflow migration. The delivered
EPUB and previously saved PASS records are preserved for provenance; they must not
be represented as proof that this post-delivery finding has been resolved.

## Scope and method

Read the actual current `progress.json`, `glossary.md`, `review-ledger.json`
and all 51 `translated/*.md` unit files via the GitHub repository.
Counted whole-word, case-sensitive literal English spellings of five character
names in the accepted Russian unit texts, including headings and the contents page.
This is a **conservative lower bound**, not the count of all translation defects
or all untranslated names. Checked source/translation pairs for selected chapters
11, 13, 19, 23, 27, 28, 32 and 35, and further source-specific evidence in 48.

| Original spelling | Expected Russian spelling | Literal English occurrences |
| --- | --- | ---: |
| Dillon | Диллон (decline by context) | 493 |
| Cade | Кейд (decline by context) | 675 |
| Darren | Даррен | 88 |
| Christian | Кристиан | 23 |
| Evelyn | Эвелин | 12 |
| **TOTAL** | | **1,291** |

**39 of 51 units affected:** 003, 007, 009, 010–026, 029–031, 033–048
(the ranges mean chapter/unit numbers, not chapter titles).
Among the 38 numbered chapter headings, **35** still show an English character
name. The prologue heading does too. The final recent correction wave in units
027, 028, 032 did not leave these five English names behind.

Examples (links point to the exact accepted text):
- [Unit 003, contents lines 9–48](../translated/003-contents.md): all chapter name labels still mix English character names into the translated contents.
- [Unit 011, lines 37, 51, 57](../translated/011-leesburg-virginia-february-2017.md): Russian dialogue and narration contain `Cade` and `Dillon`.
- [Unit 013, lines 3, 5, 7, 11](../translated/013-3-cade.md): untranslated `Dillon` and `Evelyn` coexist with Russian `Эвелин` elsewhere in the same unit.
- [Unit 022, lines 27–41](../translated/022-12-dillon.md): `Darren` and `Cade` remain Latin despite glossary entries.
- [Unit 035, lines 7–15](../translated/035-25-dillon.md): `Darren` is left in ordinary Russian prose.
- [Unit 048, line 141](../translated/048-38-dillon.md): `Darren`, `Christian`, `Aaron`, `Darius`, `Raven` remain Latin. The last three character names have no explicit glossary entries.
- [Unit 048, line 149](../translated/048-38-dillon.md): `Loudoun County High School` remains unlocalized in the Russian passage. The book needs an explicit terminology decision before changing the institution name.

## Separate semantic issue

- [Original unit 011, line 81](../extracted/011-leesburg-virginia-february-2017.md)
  clarifies that the narrator's fourteenth birthday will occur **next month**.
  [Russian translation unit 011, line 81](../translated/011-leesburg-virginia-february-2017.md)
  asserts the narrator is **already fourteen**, then immediately says fourteen
  is only reached next month. This is a real internal contradiction in the
  translation. Correct only in a source-bound review; preserve any separately
  authorized editorial age changes as an explicit decision, not an unnoticed
  deviation from the source.

Editorial age-request follow-up: units 011, 012 and 013 still contain Russian
age references to fourteen. If the previously requested +4-year editorial
adjustment was intended to cover these units, that requirement has **not**
been implemented across this early sequence. This is distinct from source fidelity.

## Why the previous automated PASS is insufficient

The last review records say PASS for all 51 units and mark all five checks
including terminology as true. All review SHA identities match the then-accepted
texts. Nevertheless the actual text contains at least 1,291 glossary-violating
name spellings. Of the 51 most recent review records, 24 have anchored v2
evidence and 27 are v1 quality evidence (not silently equivalent to v2).
The pipeline lacks an effective deterministic gate for explicit character names;
the text shows a **false negative in literary/terminology review**, not a GitHub
artifact integrity failure.

A sampled structure check (8 substantive units) found source/target character
length ratios approximately 0.97–1.09 and no sample-level scene-marker/link
count discrepancy. Those metrics **do not** prove semantic completeness.
This audit does not claim a complete sentence-by-sentence accuracy check.

## Required resolution and quality gate

1. Complete and verify the character/institution glossary against the source,
   including separately checking Aaron, Darius, Raven, Heritage and school names.
2. Reopen the affected, already-reviewed **exact units** only through an explicit
   canonical, provenance-preserving correction path compatible with the book's
   pinned workflow revision. Do not directly overwrite a reviewed artifact
   while claiming its previous review/PASS remains valid.
3. Fix Latin character names in **context**: Russian case endings, headings,
   contents, pronoun references and spacing. A literal global replace is not
   sufficient and can produce ungrammatical nominatives.
4. Independently re-review the changed translation against the exact source and
   glossary, including concrete source-linked findings for any other fidelity
   errors. Preserve original source bytes.
5. Validate **all** known required names and titles with a deterministic
   glossary consistency preflight that excludes intentionally preserved English
   brands, game titles, source/URL attributions and quotations as appropriate.
   A failed name check must not be turned into an automatic PASS.
6. Resolve age-related editorial policy consistently and explicitly, then
   rebuild and independently verify the new EPUB and SHA-256. Keep the previous
   artifact as a traceable superseded edition, not a silently replaced PASS.

**Correction status at audit creation: NOT FIXED.**
No original, translated chapter, progress status, review ledger, pinned workflow
revision or finalized EPUB was edited by this audit.
