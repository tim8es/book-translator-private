# The Claiming Moon — full source and accepted-artifact byte-integrity audit

Date: 2026-10-22. Pinned workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789`.

## Verified

- **48 of 48** source-derived `extracted/*.md` files: each complete UTF-8 file was freshly retrieved from GitHub, SHA-256 recomputed from the actual bytes, and compared against the exact `source-manifest.json.extracted[].sha256`. **48 matches; zero mismatches or fetch failures.**
- **44 of 44** accepted translation files: each complete UTF-8 file was freshly retrieved from GitHub, SHA-256 recomputed from the actual bytes, and compared against the matching `progress.json.chapters[].translation_acceptance.translation_sha256`. **44 matches; zero mismatches or fetch failures.**
- SHA-256 implementation was checked against the standard test vector `SHA256("abc") = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` in every verification batch.
- Current `progress.json` blob SHA-1: `a4eaffe8a5a0f076b95f9afdd232f34fc319ed88`. Current counts: **reviewed 3**, **translated 41**, **extracted 4**.
- Book source original EPUB digest recorded in `source-manifest.json`: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`. The original binary EPUB was **not independently rehashed** in this pass because the GitHub connector's content retrieval is UTF-8 oriented; only all **48 derived source units** were independently rehashed.
- Review ledger has three historical `CORRECTIONS_REQUIRED` entries for narrative chapter 15; no current narrative `PASS` evidence.

## Meaning and limits of result

These checks establish that the canonical stored source text and accepted Russian text are **byte-identical to their manifests/evidence**. This **does not** prove full semantic coverage, sentence-to-sentence fidelity, correct character voices, or independent literary review. Each narrative chapter must still be compared completely with the original before being marked `reviewed`.

The four `extracted` chapters (19, 26, 27, 29) have partial incoming draft translations, not accepted canonical artifacts. As of this audit, chapter 26 has new text-indexed partial coverage **0–270 of 570**, chapter 27 has repository-confirmed **0–90 of 341**, chapter 29 **0–290 of 456**, and chapter 19 has multiple **conflicting overlapping drafts through block 125 of 324**. See `incoming/coverage-audit-2026-10-22-ch26-250.md` (content updated to block 270) for file-level detail.

## Outstanding gates

1. Reconcile chapter 19 draft variants; finish the four incomplete narrative chapters, preserving every source block including author notes.
2. Accept complete canonical files by live translator claims and hash-bound `progress.json` transitions.
3. Perform full independent source-comparison Reviewer pass on all 45 narrative chapters; record exact-version `PASS` and promote each unit under the orchestration contract.
4. Verify full book final-state invariants and assemble the final Russian EPUB.

No lifecycle promotions and no final EPUB were performed by this audit.
