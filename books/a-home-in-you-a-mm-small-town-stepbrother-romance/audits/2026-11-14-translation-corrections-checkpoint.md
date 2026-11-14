# A Home in You — source-faithful Russian correction checkpoint

Date: 2026-11-14. Candidate branch: `fix/a-home-in-you-names-review-20261114`
(PR #108). Pinned workflow: `ea9963ca546b7cc7f6aba4dc5350fa19ea7da862`.
Preserved source: `source-000001` (original EPUB and extracted English files unchanged).

## Editorial rule for this correction pass

The **English original is authoritative** for age, chronology, actions, speakers,
family relationships, emotional tone and narrative meaning. Correct Russian
grammar and punctuation without inventing plot changes. Previously requested
age alterations are not a substitute for a faithful translation of the
source; never silently relabel an adaptation as a source-faithful edition.

## Corrections persisted on the PR branch

| Unit | Verified commits | Change |
| --- | --- | --- |
| 007 author message | `2de9805e37da0a6edd841d9d3b6d2a507d151396` | Two proper-name declensions and a natural, source-consistent opening sentence. |
| 011 beginning narrative | `cf9e5209c8fe9f005aff0cbdeb9223a127cbbc0a`; `502542894f7dfd0086056b45f6692e63f5cabab9` | Fixed a source-contradicting age sentence; fixed eleven Russian dialogue-tag punctuation instances. |
| 012 Cade | `c02005ddec31f48b03e3686b9826840a0be09d6b` | Fixed eight Russian dialogue-tag punctuation instances. |
| 013 Cade | `f64862df4ed4d74a6a6a4bf3856e350e5deb7086`; `f18b2dd5f2008c4d2851722c1597e7fc5cc03d02` | Corrected name cases and speaker attribution, then two additional case/voice/fidelity sentences and four dialogue-tag punctuation instances. |
| 026 Dillon | `674b1a50bcae8e8d1cc481e50c4e21e861bb48c5` | Corrected `для меня и Кейда`, restored the proper subject of Cade's race win, and repaired two literal `\\u2014` artifacts. |

All five modified files were read back after GitHub writes and matched the
intended candidate content. Their source/target counts and ordered values
of `bt-scene-break`, `bt-anchor`, `bt-block` markers and Markdown link
destinations matched in a read-only structural spot check (zero relevant
markers in the examined source units). No Unicode em-dash escape or the
checked Russian guillemet+dialogue-tag omission remained in these five files.

A narrow pattern scan was also performed across the 39 existing PR candidate
units for common bare-case name errors, missing Russian dialogue punctuation
in guillemet/tag combinations, and literal Unicode punctuation escapes.
This **is not** a complete literary review and may have false positives and
false negatives. Do not claim that it proves grammatical or semantic coverage.

## Still required before a corrected EPUB exists

1. A source-linked literary correction/review pass on all affected units.
   Earlier accepted `reviewed` records still bind original bytes, not PR text.
2. An explicitly authorized, provenance-preserving canonical reopen/accept
   transition. The pinned `TranslationAcceptanceManager.accept()` returns
   verification for `reviewed` units and cannot re-accept changed bytes.
   Do not merge PR #108 as-is or forge fresh PASS evidence.
3. A proper independent Reviewer PASS on each changed exact translation
   artifact; correct further findings where safe and appropriate.
4. Rebuild EPUB through the exact pinned workflow, then verify artifact
   SHA-256, source identity, all units, all links and accepted review state.
5. Retain the old EPUB as the traceable previous revision.

**Status: editorial corrections staged; new final EPUB NOT BUILT;
PR #108 remains draft; canonical translation and review state on `main`
left unchanged.**
