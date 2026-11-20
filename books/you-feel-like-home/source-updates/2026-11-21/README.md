# You Feel Like Home — November 2026 source edition

## Durable result

The new source edition **source-000004** has been promoted by the book-pinned workflow `db253095d36f245f9531da654b93ab72193d3b97`. The 15 reading-order units are Preface, description, Chapters 1–12 and Afterword. No units were deleted. Every unit currently has machine Translator acceptance, including Chapter 12; **zero units have independent Reviewer PASS**.

## Preserved inputs and correspondence

- `source/You_Feel_Like_Home.html`: immutable exact user-uploaded original; SHA-256 `c602be8c25de25d5f943f4c8de80e5a3df801b6c7fb2eb833204a1df38f92b9c`.
- `source/You_Feel_Like_Home_workflow_compatible.html`: derived source used for the active edition; SHA-256 `fcc4a94fff8722c9cf1ea891361acca1d15cd4796b56fc7c2e95a38a7b92dac9`. Its only changes are eleven `#endnotes...` hyperlinks made absolute and replacing the description's top-level `h1` by `h2`. The visible English text remains identical.
- `source/You_Feel_Like_Home_derived_anchors.html`: earlier candidate retained for provenance.
- `translated/chapter-12-ru-after-review.md`: earlier local translation review draft, not the accepted canonical bytes.
- `translated/chapter-12-canonical-ru.md`: complete Chapter 12 translator artifact with four source-aligned scene-break markers, author notes and footnote link; SHA-256 `4fcae489d7fbf289daf0e55c8f33b89ce88ba129f035ec8e904205980dd33bf1`.
- `translated/preface-ru-updated.md` and `translated/description-ru-updated.md`: metadata and heading updates carried into canonical acceptance.
- `review/chapter-12-local-review.md`: same-chat source comparison only; **not** an independent review record.
- `source-comparison.json`: content similarity evidence for 11 old narrative chapters.

The attempted candidate `source-000003` was correctly **discarded** because it merged the description into the Preface and would have deleted the old description unit. It is immutable historical provenance. `source-000004` preserved the description separately and promoted with zero deletions.

## EPUB output

`output/You_Feel_Like_Home_RU_12chapters_PREVIEW.epub` is a **preview only**, SHA-256 `0d99c065f3065a8a36e9731b3f4b8b3c947ffcbd16b8cdd22856a7001b623a93`, 908,897 bytes. It contains all 15 translated units; `output/manifest.json` is the canonical build identity.

## Remaining canonical work

A Reviewer must compare all current source and translation units and record current SHA-bound PASS evidence through the pinned workflow; the Orchestrator may then promote each from `translated` to `reviewed`. Only after all 15 are reviewed may the final EPUB be built without `--allow-unreviewed`. Do not promote historical review notes as machine evidence, and do not report the preview as the final reviewed book.

A temporary generic GitHub Actions executor was used to invoke pinned CLI source staging, promotion, translation claims/acceptance and preview assembly. It was **removed** after use to restore the book-state repository's canonical nine-workflow topology. Ongoing work uses the existing standard ChatOps and final EPUB workflows.
