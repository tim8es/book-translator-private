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

## 2026-11-14 continuation: source-faithful editorial correction pass

This follow-up is limited to **candidate translations in the PR branch**.
It did not change the original EPUB, extracted English, workflow pin, canonical
`main` progress/review ledger, or shipped EPUB. The user's latest instruction
is to preserve the meaning of the English original, not silently re-age the
characters or invent altered events.

**48 targeted text replacements were persisted in 13 units** (each commit read
back from GitHub and content verified). They correct confirmed Russian case
errors, chronology and tense in the prologue, dialogue-tag punctuation, speaker
attribution and source-consistent literary wording. No blanket replacement
can be considered literary review.

| Unit | Changes | Verified commit(s) |
| --- | ---: | --- |
| 008 trigger warnings | 2 | `bc98b483614fa5e3c02b7c13eed6873dcc6a083a` |
| 009 prologue | 5 | `ded29c23e5760a8176c0786140f068bacbb343f6` |
| 011 opening narrative | 18 | `60022ff1c68387c44e521d9cbc4bae69c45bbb72` |
| 012 Cade | 5 | `b9e98b35e7c3240751126ffd0dcee0eeb35b0237` |
| 013 Cade | 1 | `427e80ade4ce4504d43a82ac296c3de1818c5d33` |
| 016 Cade | 3 | `7a31ad5ff22beb5c5ef7b474f7975abdd36d370a` |
| 019 Dillon | 5 | `b7dd8296d4335ac28999f07e2fa205b774961929`, `8f9a4fa5fa3e37e5d9bd60f699d843a693e37d25` |
| 023 Cade | 2 | `9846beedd752f20a04674cf1b465b45237cff69b` |
| 037 Dillon | 1 | `0242209f47dbe637462e9ad6a8946d29de765d1d` |
| 040 Cade | 1 | `a31d0e8d3e746b1c40e7cf5ee4121b3810b3fbf7` |
| 045 Cade | 1 | `f4e63f7deb9978ee3bb51851d59ddb72ebc82982` |
| 047 Dillon | 3 | `952149fab2afd6622c593a9d128f63ad4fc91f33` |
| 048 Dillon | 1 | `f51b589aadd81a6eabb32e621f899f1afa6fed1d` |

### Integrity checks and limits

- Source and candidate translations were compared for all **13 edited units**
  with respect to ordered `bt-*` markers, Markdown link destinations and
  heading counts; all compared structures matched.
- A focused, Unicode-aware language-pattern scan found further nominative
  names in indirect grammatical roles. Candidate-only corrections were made
  when the English reference supported them; apparent matches involving
  correctly inflected names or the indeclinable name `Марко` were not blindly
  replaced.
- Pattern scans are incomplete by design. They cannot find all fidelity,
  grammar, dialogue, continuity, or inflection defects. The previous editorial
  report already demonstrated that the former automated PASS was insufficient.
- **Some units still have unresolved literary issues**, including material
  outside this bounded pass. No fresh independent full-chapter PASS has been
  recorded; no reviewed status has been reopened; no accepted replacement EPUB
  has been built.

**Gate: DO NOT MERGE PR #108 or deliver it as final quality-assured EPUB** until
there is an authorized, canonical, provenance-preserving reopen path compatible
with this book's pinned workflow, exact-artifact translation acceptance,
independent full-source review of each affected unit, and a verified rebuild.
