# The Claiming Moon — backward QA accepted-corrections checkpoint

Date: 2026-10-22. Scope: narrative chapters 45 and 44, processed from the end of the book. This is a reproducible orchestrator checkpoint, **not** final literary completion.

## Confirmed canonical acceptance

| Narrative chapter | Stable unit | Accepted correction count | Accepted translation UTF-8 SHA-256 | Canonical blob SHA | State after acceptance |
|---:|---|---:|---|---|---|
| 45 | `chapter-000047` | 5 | `fb222210ce7039eb872f61dcef84afd52262973dbf4f3b4a8a4123f8334a9969` | `20523e8e4cc049423ed71c52d1718390a310bc71` | `translated` |
| 44 | `chapter-000046` | 3 | `9c5d6714088bb281f8fe5a0a2977c635d9fbd1b2a3a07101ae4c3d568d7db421` | `e5e6311f915ae2dab9c8c92c4ed5abd4157ecb10` | `translated` |

For **chapter 45**, fixed: omitted opening author note; omitted Taehyung countertop gesture; weather repetition; Namjoon/Jin referent; erroneous `становятся маленькими` for the pups. These five exact textual changes were reconstructed from original and draft, saved into the canonical `translated/` file under a live Translator claim, checked by readback, then accepted by hash-bound `progress.json.translation_acceptance` CAS. The Reviewer recorded `CORRECTIONS_REQUIRED` for the prior accepted SHA under ledger sequence 7. That outcome is now stale relative to corrected artifact; no fresh PASS.

For **chapter 44**, fixed: omitted opening author note; ungrammatical `Ей было так же грустно, как и облегчённо`; broken calque `Она в этом позаботится, чего бы ни стоило`. The three changes were staged in a v2 draft, compared with a mechanical reconstruction against original accepted bytes, written to canonical `translated/`, and accepted under a new live Translator claim with CAS. Its prior Reviewer `CORRECTIONS_REQUIRED` is recorded at ledger sequence 11 for the previous translation hash; no fresh PASS.

## Original sources and audit provenance

Pinned workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789`.
Original EPUB/source revision: `source-000001`, original SHA-256: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.
Canonical source Markdown files remained unchanged, source SHA identities stayed intact.

Chapter 45 acceptance commits: canonical file `f1b8779ba563339bb2a33eb8917404531584e260`, progress `961b830a2eae1c148f882f4f0647b16b721065cc`.
Chapter 44 acceptance commits: canonical file `1f680d26271afba10fc4de89b0270d0a135e7da7`, progress `a652f40fcfc7145d8bbb81c1152c36a642720721`.
All Reviewer and Translator claims for units `chapter-000046` and `chapter-000047` were released with separate `release_requested` and `released` audit events. Claims on other units remained untouched.

The existing review ledger histories refer to **previous** canonical versions and do not establish current literary `PASS`. To advance the workflow, acquire independent Reviewer claims for the newly accepted exact bytes and compare chapter 45, then 44, in full. Chapter 43 (`chapter-000045`) still has an unreviewed author-note correction draft in `incoming/` and was not mutated in this pass.

## Fresh concurrent snapshot after acceptance

Progress GitHub blob `6567409499cff1ea8166a8dc6c7dca886efe934d`: **3 reviewed, 41 translated, 4 extracted**, 48 units total. Other agents are claiming earlier units. A Reviewer claim attempt for chapter 43 collided with book-level concurrent GitHub writes/claim coordination; the claim did not persist, no other claims were taken over.

The canonical full-book build remains blocked by untranslated and unreviewed units. Only build EPUB after validating complete 48-unit coverage with current independent PASS evidence.
