# Integrity finding — chapter-000027 (source hash evidence)

Date: 2026-10-22 UTC
Book: *The Claiming Moon*; workflow pinned to `5e0731da8b7ca81ada5316ed536a8a954008b789`.

## Verified hashes

- Unit: `chapter-000027`, reading order 27, narrative Chapter 25 — *No More Secrets*.
- Actual extracted source SHA-256 (computed from current bytes): `89b1908440458a564fa55227f3f6c3f2b8648e9f2baf5e883535d18d21d29b8b`.
- Sealed `source-manifest.json` SHA-256: **same 64-character value**. The immutable source and manifest agree.
- `progress.json.translation_acceptance.source_sha256`: `89b1908440458a564fa55227f3f6c3f2b8648e9f2af5e883535d18d21d29b8b` (**invalid 63-character value**, missing the `b` after `...e9f2`).
- Current translated artifact SHA-256: `87cb5d988febfc3313dd028eb3271fb8315af431127a78af524da7dd3b428dc1`; it matches the stored `translation_acceptance.translation_sha256`.
- Historical review-ledger PASS for the unit at sequence 92 repeats the malformed source hash and therefore is **not a valid current source-byte-bound PASS**, notwithstanding `progress.json` status `reviewed`.

## Impact and safe recovery

The book currently shows 48/48 `reviewed` lifecycle entries, but only 47 have PASS/source-identity evidence that matches the sealed corpus. Do **not** declare final quality gates passed or build a final EPUB from this state. Do not change the immutable source or regenerate the manifest.

Correct via an auditable recovery of the invalid acceptance under the book-pinned workflow: preserve historical ledger records, re-establish a valid Translator acceptance bound to the unchanged canonical source and translation bytes with a live claim, then create a fresh current hash-bound Reviewer PASS and promote via normal lifecycle semantics. Do not hand-edit old PASS history, silently bless the typo, or fabricate a comparison that was not performed. If the existing reviewed-state API refuses re-acceptance, handle the recovery as an explicit orchestration/state-repair transition rather than disguising it as a routine review.

Chapter 21 (`chapter-000023`) was independently completed and promoted to `reviewed`, PASS ledger sequence 111, source/translation hashes verified. Its claim was released with audit events.
