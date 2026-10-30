# Policy Change — exact original EPUB intake

This folder is the one remaining source-ingress point for the one-shot, fail-closed canonical initialization workflow.

Upload the **original** `Policy Change.epub` here, using that exact filename, to the **main** branch. The upload must contain the byte-identical original:

- SHA-256: `b27e61a767dd5ba93451cf0b1df5ad8d6c40b11bdead7435e0ca682768378639`
- Size: `488072` bytes.
- Trigger: `.github/workflows/policy-change-source-intake.yml` on a push changing `intake/policy-change/source/Policy Change.epub`.
- Runtime revision pinned for this **new** book: `c76159e4939ed00ac19172228f8972af87cadbb8`.

The pinned engine includes PR #113's source-covered external URL parentheses fix (full CI passed). The action verifies the original SHA before extracting, runs independent EPUB source coverage, seals the corpus, validates and verifies it, and **only after all checks PASS** commits `books/policy-change/`. It never adopts historical draft chapters as accepted translations or reviews. If any check fails, no canonical book is published.

**Privacy warning:** at the time this file was written, `tim8es/book-translator-private` is a **public** GitHub repository, despite its name. Uploading the EPUB to `main` publishes the copyrighted source file and records it in Git history. Make the repository private before uploading if public access is unwanted. The book’s prior chat attachment does not automatically exist in GitHub.

One-shot workflow is infrastructure readiness, **not** evidence of successful source admission. The authority remains `books/policy-change/metadata.json`, `progress.json`, `source-coverage.json` and the current review ledger after the action actually succeeds.
