# You Feel Like Home — verified recovery preflight (2026-10-22)

This report records the full comparison completed using the **exact newly attached** English EPUB and the existing Russian reader EPUB. It does not mark the book as upgraded.

- Original source: `You_Feel_Like_Home 2.epub`, SHA-256 `8efac63cf78817b821008ee001fb33aea40b29d5c8c9d69cb9f52f14b0bd28a2`, 191,460 bytes; all 14 spine XHTML documents read and ZIP CRC passed.
- Existing translated compilation: `You_Feel_Like_Home_RU_chapters_1-11.epub`, SHA-256 `6297c4570c776ce6de609926a9c9942bf044b63ebc6e44c0944d7818feeb03d2`.
- The local corrected **preview** fixes mojibake in OPF/nav/NCX, separates the introduction and summary, brings visible paragraphs closer to source CSS spacing, adds a verified work URL and 10 chapter-note links; validates 14 navigation/spine entries, 10 valid internal links. Text token sequences across all original Russian chapter documents were checked against the corrected preview and are identical.
- The locally generated recovery package includes **14 original XHTML and 14 translation XHTML units**, original English EPUB, preview EPUB and checksum manifest. These files are attached in the conversation and **are not in this repository**. The user's original should be transferred only through a supported, authorized binary upload transport in a private environment.
- Current book's `metadata.json.workflow`, `progress.json`, `review-ledger.json`, `source-manifest.json` remain untouched; no independent PASS reviews exist. The EPUB source-coverage contract in workflow `0fe7fd8` rejects original XHTML link/semantic tags. There is no certified source-coverage file.

## Next safe transition

Once a supported structure-preserving XHTML/EPUB workflow is landed as a new **public workflow revision**, validate the exact original, initialize/protect its 14-unit source revision and durable state via Orchestrator, reconcile translations and perform the independent source comparison for every unit, then assemble a verified final EPUB. Do not rewrite canonical state to claim these events occurred prematurely.

The JSON file is an audit record only, not `source-coverage.json` or `source-revisions.json`.
