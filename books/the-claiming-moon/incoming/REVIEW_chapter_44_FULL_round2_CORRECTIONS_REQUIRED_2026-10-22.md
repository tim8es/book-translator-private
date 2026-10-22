# The Claiming Moon — narrative chapter 44, full sequential Reviewer comparison, round 2

**Outcome: CORRECTIONS_REQUIRED.** Current canonical Russian text has one confirmed source-fidelity mismatch.

- Stable unit: `chapter-000046` (narrative Chapter 44, "The Past That Didn't Last")
- Reviewer session: `cm-20261022-reviewer-ch44-full`
- Pinned workflow: `5e0731da8b7ca81ada5316ed536a8a954008b789`
- Current source SHA-256: `6ffb95dbd4ac53c82c41a31ad227e9ea987e5304420729da93a81d82ca4037d8`
- Reviewed translation SHA-256: `9c5d6714088bb281f8fe5a0a2977c635d9fbd1b2a3a07101ae4c3d568d7db421`

## Coverage

Original and accepted Russian chapter were independently read sequentially, **all 445 aligned nonempty semantic blocks**, indexed 0–444 (extractor title/header skipped). Coverage included opening author notes, flashback, Ha Yung/Tae Won and Ha Rin scenes, arrival at Hefter, omega-suppression plan, present-day disclosures and reconciliation, the closing scene with Jungkook and Taehyung, and all six end-note blocks. Negation, character identity, dialogue, emotional certainty, violence intensity, quantities, repeated phrases, stage transitions, and natural-language readability were checked.

Previous three accepted corrections (opening author note; grief/relief sentence; unnatural `Она в этом позаботится` calque) were confirmed present and source-faithful.

## Blocking finding (source block 145)

- Source: `It was Ra Hee, Hyungwon's mate. She came splashing through the mud and threw herself on his arm, and right after her came Jungwon, eight years old ...`
- Current Russian: `Это была Ра Хи, пара Хёнвона. Она плюхнулась в грязь и вцепилась ему в руку. Следом подбежал Чонвон ...`
- Semantic error: `came splashing through the mud` describes moving **through mud with splashes**, not falling or plopping down **into** it.
- Correct to `Это была Ра Хи, пара Хёнвона. Она прибежала, разбрызгивая грязь, и вцепилась ему в руку. Следом подбежал Чонвон ...`, keeping the eight-year-old description unchanged.

No other blocking discrepancies identified in this complete sequential comparison. The Reviewer must not PASS the current translation while this action remains inaccurate.

## Next role transitions

1. Record `CORRECTIONS_REQUIRED` against this exact accepted SHA-256 in `review-ledger.json`, with current Reviewer claim and CAS.
2. Release Reviewer claim and stage the exact correction.
3. Under a **Translator** claim, update canonical `translated/`, validate bytes and SHA-256 and run `accept-translation` with compare-and-swap, then release.
4. A fresh Reviewer independently re-opens original and updated translation; check the corrected block and verify all previously compared blocks remained unchanged and coherent. Only then may PASS be recorded and `accept-review` promote the unit to `reviewed`.
