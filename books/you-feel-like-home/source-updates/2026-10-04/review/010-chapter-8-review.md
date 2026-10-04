# Chapter 8 literary review

Outcome: `PASS` as a literary source-comparison result for the staged 2026-10-04 source update.

This is **not** a v3 review-ledger lifecycle transition. The supplied EPUB has SHA-256 `86617f0ea38b3aa7c23000a09f0c467b4ca507df664ffbfbfec9c166e1842226`, while the canonical book source is pinned to `cfe3a150553340a1c92d7f823ac0821e2307fbda43dc040f6e11287fae4e2df3`. The canonical `metadata.json`, `progress.json`, `source-manifest.json`, glossary, and style guide are therefore intentionally left unchanged.

## Artifact identity

- Source: `extracted/010-chapter-8.md`
- Source SHA-256: `de5f1766c7a855d8779b0b3025c68733f33582386636615dbc5957256589f67a`
- Translation: `translated/010-chapter-8.md`
- Translation SHA-256: `90e2c5a71196ce1c00d26750da5b42fb9856c1fcdeb25aaab04f395e944e44c5`
- Workflow revision: `dca1e7db6974d5c4354e4850ecf82b42cda06f42`

## Checks performed

- Sequential source-to-translation comparison across the complete chapter.
- Funeral, Andrew's internal admission, will reading, Matilda confrontation, Palermo/Marco/Stefano sequence, and Caleb's week in Sicily were checked for chronology, agency, causality, and viewpoint.
- Numbers, debts, ownership transfers, time spans, family relations, security details, and the official account of the King's death were checked for semantic drift.
- Caleb, Andrew, Matilda, Arian, Marco, and Stefano retain distinct source-supported voices and emotional intensity.
- Source typos in recurring names were normalized consistently with the existing book glossary and the Chapter 7 review precedent.
- New chapter names were rendered consistently as `Марко Белланди`, `Стефано Греко`, `Джулиан`, `Нероне`, and `Риццо`.
- Italian dialogue is retained where the source switches into Italian.
- Russian spoken dialogue uses em dashes in accordance with the book-specific convention.
- All four `++++` scene separators are preserved.
- The source XHTML was checked directly in addition to extracted Markdown; meaningful emphasis stripped by the structural extractor was restored in the translation, including `CENTRO ESTETICO BELLANDI`, the staff's line about Don Conti, Caleb's remembered line about the King, and his internal reaction about the riding instructor.
- Chapter notes and chapter-end notes are retained.
- The repeated AO3 export work/author/series wrapper header is treated as wrapper metadata, consistent with the existing translated Chapter 7 artifact, and is not repeated in the literary translation.
- Target-language polish changes were rechecked against the corresponding source passages after editing.