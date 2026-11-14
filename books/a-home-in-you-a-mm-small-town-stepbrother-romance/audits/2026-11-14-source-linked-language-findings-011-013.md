# A Home in You — manual source-linked QA findings (units 011 and 013)

Date: 2026-11-14. Source: immutable `source-000001`.
Pinned workflow: `ea9963ca546b7cc7f6aba4dc5350fa19ea7da862`.
Candidate: draft PR #108, branch `fix/a-home-in-you-names-review-20261114`.

**Result: CORRECTIONS REQUIRED (editorial audit only).** This file is **not**
a canonical `review-record`, accepted translation, lifecycle transition or PASS.
No chapter, age, original EPUB, progress, ledger, or output manifest was changed
by this audit. The earlier PR-wide name scan must not be treated as proof of
grammatical or literary correctness.

## Verified source-to-candidate discrepancies

| ID | Source / candidate | Finding | Required correction |
| --- | --- | --- | --- |
| S011-AGE-01 | `extracted/011-leesburg-virginia-february-2017.md:81` → `translated/011-leesburg-virginia-february-2017.md:81` | Source explicitly says the speaker will turn fourteen **next month**. Russian candidate says `Мне было всего четырнадцать. Ну, в следующем месяце исполнится`, creating an internal time contradiction. | Decide whether the deliverable is the faithful original or a separately labelled age-adjusted adaptation. For fidelity, the narrator is *not yet* fourteen at this moment. Do not silently alter other age decisions. |
| S013-CASE-01 | `extracted/013-3-cade.md:21` → `translated/013-3-cade.md:23` | `Папа тоже подвинул Диллон подарок`: proper name in the wrong case. | `Папа тоже протянул Диллону подарок` (retain the following clause about Cade choosing it). |
| S013-CASE-02 | `extracted/013-3-cade.md:25` → `translated/013-3-cade.md:31` | `Диллон понравился выбранный мной подарок`: wrong case and inversion of the subject/recipient relationship in Russian. | `Диллону понравился выбранный мной подарок`. |
| S013-CASE-03 | `extracted/013-3-cade.md:27` → `translated/013-3-cade.md:33` | `отвёл меня и Диллон в сторону`: incorrect accusative. | `отвёл меня и Диллона в сторону`. |
| S013-CASE-04 | `extracted/013-3-cade.md:31` → `translated/013-3-cade.md:37` | `Я дал Диллон ответить первым`: incorrect dative. | `Я дал Диллону ответить первым`. |
| S013-SPEAKER-01 | `extracted/013-3-cade.md:53` → `translated/013-3-cade.md:59` | Source has **Dillon** offering to help Cade; Russian candidate reads `«Я могу помочь», сказал Диллону`, which loses the speaking subject and is ungrammatical. | `«Я могу помочь», — сказал Диллон, заметив мои мучения. «Мама меня научила».` |
| S013-PUNCT-01 | Multiple lines of `translated/013-3-cade.md` | Dialogue tags regularly omit the necessary Russian dialogue punctuation: `«…», сказал` rather than `«…», — сказал`. | Apply an editorial, meaning-preserving Russian dialogue punctuation pass, then source-check all affected speakers. |

These are direct discrepancies verified against both original and PR candidate,
not pattern-based guesses. The five name-case/speaker examples demonstrate that
PR #108's automated token replacement and earlier 17 manual repairs **did not
finish grammatical validation**.

## Required follow-up

1. Treat all 39 changed units as **unreviewed candidates** and audit name
   inflections, syntax, speaking subjects, chronology and terminology in context.
2. Resolve the fidelity-versus-age-adaptation conflict as an explicit editorial
   decision, preserving source bytes.
3. Use a canonical, provenance-preserving reopen/translation-acceptance path
   compatible with the pinned workflow, followed by independent source-linked
   review. The currently pinned `TranslationAcceptanceManager.accept()`
   returns an unchanged verification for `reviewed` chapters and **cannot**
   accept modified bytes in place.
4. Keep draft PR #108 unmerged until complete canonical state transition,
   validations and a newly verified EPUB output.

**Do not mark these findings resolved solely because the English name spellings
are absent.**
