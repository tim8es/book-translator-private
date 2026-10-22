# The Claiming Moon — reverse QA checkpoint: three accepted chapter corrections

Date: 2026-10-22. Book state restored from `tim8es/book-translator-private/books/the-claiming-moon/`. Pinned workflow: `5e0731da8b7ca81ada5316ed536a8a954008b789`. Source edition `source-000001`, original EPUB SHA-256 `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.

## Accepted canonical Russian translation corrections

| Narrative chapter | Stable unit | Accepted patch count | Current accepted translation SHA-256 | Canonical status |
|---:|---|---:|---|---|
| 45 | `chapter-000047` | 5 | `fb222210ce7039eb872f61dcef84afd52262973dbf4f3b4a8a4123f8334a9969` | translated |
| 44 | `chapter-000046` | 3 | `9c5d6714088bb281f8fe5a0a2977c635d9fbd1b2a3a07101ae4c3d568d7db421` | translated |
| 43 | `chapter-000045` | 2 | `950a24fe6c0f3c0d024c4d1d7513592066fa63fe4c809ccab07b5e9f4615fcac` | translated |

Chapter 45: restored source-authored author-note navigation; a missing kitchen scene gesture; source repetition in weather; clarified an ambiguous male reference; corrected inaccurate description of pups' size when held against Yoongi's chest.

Chapter 44: restored opening author note; fixed awkward portrayal of coexisting relief and sadness; replaced ungrammatical calque about resolve to suppress an omega nature.

Chapter 43: restored omitted opening author-note navigation; preserved rough `so fucking hard` narrative emphasis in the chains-rattling scene.

All corrections were staged as separate exact-patch proposals; the newly accepted canonical `translated/` file was verified by GitHub readback under a live role claim; current `progress.json.translation_acceptance` was updated through GitHub compare-and-swap, binding the exact source/translation SHA-256 to each new Translator claim. Original `extracted/` and `source/` bytes were not overwritten. All three Translator claims were released with auditable request/completion events. One Chapter 43 release hit a concurrent GitHub branch conflict, was re-read, then completed under the original release request; the final completion event was verified.

## Literary Reviewer status

Previous canonical translations of these three chapters were given `CORRECTIONS_REQUIRED` by Reviewer and recorded in `review-ledger.json`:

- `chapter-000047`: review ledger sequence 7.
- `chapter-000046`: review ledger sequence 11.
- `chapter-000045`: review ledger sequence 15.

These records refer to **the previous translation hashes**, not the newly accepted Russian files. The current translated artifacts have **no current Reviewer PASS**. Independent source-vs-target literary review remains necessary. **No lifecycle status was promoted to `reviewed`.**

## Concurrency and source preflight

At final verified snapshot, progress GitHub blob `87a2c372a5c73d61134391539b454036945c39ad`: 48 source units, **3 reviewed, 41 translated, 4 extracted**. Other agents held claim files `chapter-000021.json`, `chapter-000026.json`, and `chapter-000035.json`. No claim for our completed units remained, and no coordination lock remained.

A previous scoped verification recomputed SHA-256 on every original and accepted translation in narrative chapters 31–45 against durable acceptance and sealed source-manifest; all passed before these corrections. Full-book local `book.py validate` and `corpus.py verify` have not been run in this GitHub-plugin-only environment.

## Next backward scope

Narrative chapter 42 (`chapter-000044`) has an existing separate corrected author-note draft in `incoming/`. Re-read claims and status before continuing. Do not overwrite work of parallel agents. Do not claim a final EPUB or a completed full literary review until all 48 units are covered and have current independent PASS records.
