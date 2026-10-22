# Chapter 25 — explicit state-recovery journal

Unit: `chapter-000027` (reading-order 27; Chapter 25: No More Secrets).
Workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789` (unchanged).

- Pre-repair progress blob SHA: `85bab90e74ff66e130f92632e1a90bb5e17740b1`.
- Pre-repair ledger blob SHA: `d26b650c64d344dc46530faa56274e7a27036049`.
- Pre-repair exact JSON bytes preserved as immutable snapshots in this directory.
- The accepted translation hash is valid and will be preserved: `87cb5d988febfc3313dd028eb3271fb8315af431127a78af524da7dd3b428dc1`.
- The source file and sealed source manifest both use: `89b1908440458a564fa55227f3f6c3f2b8648e9f2baf5e883535d18d21d29b8b`.
- Acceptance and ledger PASS sequence 92 have an invalid, 63-character source hash: `89b1908440458a564fa55227f3f6c3f2b8648e9f2af5e883535d18d21d29b8b`.
- Repair plan: CAS-downgrade chapter 27 to `extracted` and remove invalid acceptance; reconcile 63-character field in historical ledger row 92 to the verified source digest solely to restore document-schema validity (original ledger retained unmodified in immutable snapshot); then create fresh Translator acceptance and independent Reviewer PASS with current hashes and promote to `reviewed`. This reconciliation must not be treated as a new literary PASS; a separate new reviewer record is mandatory. Preserve the existing source and translation bytes.
- Recovery is complete only after updated `progress.json`, appended `review-ledger.json` evidence, and entire source/translation corpus are revalidated. Do not build while incomplete.

## Completed recovery — 2026-10-22

- Historical JSON snapshots preserved intact; schema reconciliation performed with compare-and-swap.
- Original source and canonical Russian translation **not rewritten**.
- New `translation_acceptance` saved with source `89b1908440458a564fa55227f3f6c3f2b8648e9f2baf5e883535d18d21d29b8b` and translation `87cb5d988febfc3313dd028eb3271fb8315af431127a78af524da7dd3b428dc1`.
- New Reviewer `PASS` at ledger sequence **112**, independent of the historical repaired sequence 92.
- Chapter 27 returned to `reviewed`; all 48/48 units now `reviewed`.
- Both working claims released with request/completion audit events; no active chapter reservations.
- Verified current source and translation bytes for all 48 units against sealed hashes and PASS evidence. Stored source EPUB binary has expected filename/size, but its original SHA-256 could not be independently rehashed through the current GitHub text-only connector; `corpus.py verify` is required in the execution environment before EPUB creation.
- Current progress Git blob: `9e6f5cf7b3b9e8c13004dafd688ee21d095d6f1e`.
- Current review-ledger Git blob: `9ec0e3c776b73ed8b96892ab4a38360c3f51dd12`.
