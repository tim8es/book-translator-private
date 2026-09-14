# Migration / recovery note

This workspace was reconstructed on 2026-09-14 from the user-supplied updated EPUB and legacy durable state found in `tim8es/traslates`, branch `book/you-feel-like-home-chapter-5`.

- Legacy source SHA-256: `0194ea47ad51cf84631a8b09696700d607e498d52495527ba913be9803e76a18`.
- Current attached source SHA-256: `cfe3a150553340a1c92d7f823ac0821e2307fbda43dc040f6e11287fae4e2df3`.
- The current source contains Chapter 5 and Chapter 6 in addition to the earlier material.
- Legacy glossary and style decisions were recovered for continuity.
- Legacy commit `3ac364fd9ca0690fddc8f54c5c856c37b6ee3aeb` records Chapter 5 as translated and reviewed under the earlier workflow. That historical review is not promoted into the current v3 review ledger because equivalent machine-verifiable evidence does not exist here.
- Current workflow is pinned to `dca1e7db6974d5c4354e4850ecf82b42cda06f42` of `tim8es/book-translator`.

## Persistence limitation

The current attachment was fully inspected and extracted in the active session, and `source-manifest.json` records the expected SHA-256 identity of the EPUB and all nine extracted artifacts. The available GitHub connector can write inline UTF-8 content but cannot directly transfer the local binary EPUB or large local artifact files by file reference. Therefore this GitHub checkpoint intentionally remains **incomplete** rather than claiming a valid self-contained corpus.

The repository currently contains workflow/book metadata, the expected source manifest, recovered glossary/style memory, auxiliary extracted text that was safely persisted, and a Chapter 6 review checkpoint. Missing source/extracted artifacts must be restored from the exact EPUB whose SHA-256 is `cfe3a150553340a1c92d7f823ac0821e2307fbda43dc040f6e11287fae4e2df3` before any future source-dependent preflight or state transition. Do not regenerate the manifest from a different edition simply to make validation pass.

The completed Chapter 6 translation produced in this session has SHA-256 `51a18bfe9575de5701e4053fea8d236c5d2dafdb689ac535cb0221c567b0e6f9`. Its literary source-comparison review returned PASS in the session, but `progress.json` remains `extracted` because the canonical translation artifact and the workflow's durable claim/acceptance/review-ledger transition were not committed through the current connector.
