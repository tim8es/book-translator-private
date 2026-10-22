# The Claiming Moon — Chapter 42 corrected-artifact regression review

- Unit: `chapter-000044` (narrative chapter 42, *Tortured*)
- Reviewer session: `cm-chatgpt-u044-final-independent-review-20261022-1539`
- Workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789`
- Original source SHA-256: `4fa3970dab5f0037c758d3b4eb57f7602071e25b27793fa2ccc842f65442a182`
- Previously compared translation SHA-256: `c2bcad2b92ae5cd1b9247fd05282c77e867202d55ac59ef85256cb85c18f831a`
- Updated translation SHA-256: `7a57c127981a54de74824f40afad95b7db48d8bfd083bae3e47df6aae319c8f1`

## Provenance and coverage

The independent original-to-Russian 295-of-295 semantic block review is documented in `incoming/QA_ch42_checked_295_blocks.md`, with source-bound machine record `5ec1b7f2bc4b41b6a927625bc6b43717`. It found exactly three blocking discrepancies. The corrected canonical artifact has been independently re-opened beside the original source and compared against the exact previously reviewed canonical translation.

The entire updated Russian artifact is **byte-for-byte identical to that already-reviewed baseline except for the three specified review corrections and one further narrowly scoped grammar correction**. This is verified by applying those exact four replacements to the prior canonical blob `7c91f04955481f1dc492854c097900cfa7c14146` and comparing the resulting entire text to current canonical blob `c65a97b495df496863fcdc546d52e3da14eb6e8f`. No other sections, scene breaks, author notes or ending text were changed.

## Independently checked modifications

1. Restored opening source author note directing readers to the chapter end notes in its own paragraph.
2. Jin's hand remains **on** Taehyung's belly; the translation no longer falsely describes Jin leaning against it.
3. Yoongi's eyes turn green on seeing Jungkook tortured; text no longer incorrectly states that he consciously felt their color change.
4. Corrected a Russian dangling participial phrase caused by edit 3. Current wording: «Как только Юнги увидел Чонгука, лежащего на полу, и мужчину, который хлестал его плетью, глаза Юнги полностью позеленели.» The source specifies the observation and change of eye color without an invented perception.

The original beginning, closing narrative, and full end notes were re-opened as part of regression verification, and previously compared unchanged body text was verified by exact canonical-text identity.

## Outcome

**PASS** for the exact corrected translation SHA-256 above, based on prior complete independent source comparison plus fresh source-grounded regression review and proof of unchanged coverage. This note alone does not promote lifecycle status. Only a current machine `PASS` record plus orchestrator `accept-review` may set `reviewed`.
