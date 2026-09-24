# Recovery state

Recovered on 2026-09-24 from the user-supplied EPUB and prior translation artifacts.

- The source corpus has been partially restored under `extracted/`; remaining source units can be re-extracted from the preserved source identity.
- A complete Russian EPUB was rebuilt in the active session.
- Chapter 1 was missing from the recovered translation and was restored from the original.
- Chapter 9 was truncated in the recovered translation and its missing ending was restored from the original.
- Workflow revision is pinned in `metadata.json`.
- Current workflow lifecycle evidence was not fabricated. This recovery snapshot is not equivalent to a current-schema reviewed book.
- On resume, do not translate the book from scratch. Recover/import the existing translation artifacts first, then validate them under the pinned workflow.
