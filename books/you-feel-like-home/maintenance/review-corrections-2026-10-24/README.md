# You Feel Like Home — stage-only Chapter 9 review corrections

Date: 2026-10-24. **This is a noncanonical, historical-source correction record, not a Reviewer PASS or a promotion of lifecycle state.**

## Reference artifacts
- Historical English Chapter 9: `books/you-feel-like-home/source-updates/2026-10-11/extracted/011-chapter-9.md`; Git blob `2aeacaf147e47d534d25a7335a4391ba2fdc126e`
- Original Russian Chapter 9: `books/you-feel-like-home/source-updates/2026-10-11/translated/011-chapter-9.md`; Git blob `1ae4e0218172bf9ce1297589b7f2386134866b0e`
- **Corrected staging artifact:** `011-chapter-9.md`; Git blob `2164b8141f5701b8c04ac07b98bf1c8c573492e3`. Verified after commit.
- New Russian *reader PREVIEW* `You_Feel_Like_Home_RU_chapters_1-11_review_ch09_PREVIEW.epub`, SHA-256 `7a692b132a38c1eb758c6984ff2b6317663e8997b876d1e1efa88c22996e4fcd`. Produced as a **conversation attachment**, not persisted as binary in GitHub. Compared to the prior reader preview, only `OEBPS/section-09a.xhtml` changed. EPUB ZIP CRC and 17 XML/OPF/NCX/XHTML parses passed; the other sections were byte-for-byte identical. The six previously corrected chapter 8/11 snippets remain inherited from the prior preview.

## Concrete phrase corrections, Chapter 9
| English historical source | Russian before | Russian after | Finding |
|---|---|---|---|
| `You don't have the permission.` | `— У тебя нет разрешения.` | `— Я тебе не разрешаю.` | Direct speech calque; speaker is withholding consent, better natural Russian |
| `For how long?` | `— На какой срок?` | `— И надолго?` | Bureaucratic register in an intimate exchange |
| `Arian’s jaw tightens` | `Ариан сжимает челюсти, а Винсент тихо посмеивается.` | `Ариан стискивает зубы, а Винсент тихо посмеивается.` | Unnatural Russian collocation replaced with a fitting idiom |

The historical `Chapter 8` and `Chapter 11` review-correction staging artifacts remain under `maintenance/review-corrections-2026-10-23/`; no new source-linked Chapter 8/11 PASS review occurred in this session.

## Canonical workflow gating
- Book metadata remains pinned to `dca1e7db6974d5c4354e4850ecf82b42cda06f42`, **not** the proposed `0fe7fd86356d27dafbb409daa7e5ece23fdf62f4`.
- Canonical `metadata.json`/`progress.json` track 9 units of the old edition; all are `extracted`, while the reader edition has 11 story chapters / 14 spine units.
- `review-ledger.json` contains zero verified current PASS records.
- Latest original EPUB `You_Feel_Like_Home 2.epub` (SHA-256 `8efac63cf78817b821008ee001fb33aea40b29d5c8c9d69cb9f52f14b0bd28a2`) was supplied in another chat, but is not present in the current container or repository. No source-coverage certificate or complete canonical corpus is available for a full review.
- This session did not perform a full current-edition chapter review. The above stage-only edits must not be accepted as complete latest-edition coverage or used to write `review-record PASS`.

No workflow architectural changes were made.
