# Migration / recovery note

This workspace was reconstructed on 2026-09-14 from the user-supplied updated EPUB and legacy durable state found in `tim8es/traslates`, branch `book/you-feel-like-home-chapter-5`.

- Legacy source SHA-256: `0194ea47ad51cf84631a8b09696700d607e498d52495527ba913be9803e76a18`.
- Current attached source SHA-256: `cfe3a150553340a1c92d7f823ac0821e2307fbda43dc040f6e11287fae4e2df3`.
- The current source contains Chapter 5 and Chapter 6 in addition to the earlier material.
- Legacy glossary and style decisions were recovered for continuity.
- Legacy commit `3ac364fd9ca0690fddc8f54c5c856c37b6ee3aeb` records Chapter 5 as translated and reviewed under the earlier workflow. That historical review is not promoted into the current v3 review ledger because equivalent machine-verifiable evidence does not exist here.
- Current workflow is pinned to `dca1e7db6974d5c4354e4850ecf82b42cda06f42` of `tim8es/book-translator`.

## Source persistence limitation

The active GitHub connector can write UTF-8 text files but cannot upload the binary EPUB byte-for-byte. The complete extracted source corpus and exact source SHA-256 are persisted here, but `source/You_Feel_Like_Home (1).epub` is intentionally absent. Therefore this repository checkpoint is not self-contained for future source-integrity verification. Reattach the exact EPUB with SHA-256 `cfe3a150553340a1c92d7f823ac0821e2307fbda43dc040f6e11287fae4e2df3` before a future source-dependent preflight; do not regenerate the manifest from a different edition.

Chapter 6 translation is stored as `translated/008-chapter-6.md`. Its literary source-comparison review was performed in the current session, but its progress status remains `extracted` until the workflow's durable claim/acceptance/review-ledger transition can be executed in an environment exposing that runtime path.
