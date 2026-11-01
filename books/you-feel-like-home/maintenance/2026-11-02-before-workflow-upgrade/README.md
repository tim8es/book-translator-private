# Workflow and edition migration

The files in this directory preserve the previous machine state and the exact
nine extracted artifacts from its sealed manifest before the authorized upgrade.
The original source EPUB remains unchanged in `source/`.

The active workflow is upgraded from `dca1e7db6974d5c4354e4850ecf82b42cda06f42`
to `db253095d36f245f9531da654b93ab72193d3b97`. Extraction of the original EPUB
was independently audited with the new workflow. Its ordered tokens matched the
prior extracted corpus after excluding the old extractor's repeated document
title. The previously sealed manifest and extracted bytes are preserved here.

The user-provided latest edition, SHA-256
`8efac63cf78817b821008ee001fb33aea40b29d5c8c9d69cb9f52f14b0bd28a2`,
was independently audited and promoted as `source-000002`. Existing historical
translations were imported through translator claims and acceptance; this is
technical acceptance of existing text, not an independent literary review.
Original dated translations and previously delivered EPUBs remain unchanged.
The front matter was updated using the existing Russian metadata translation and
the current source, preserving all 31 links and current statistics. Missing
note links and three scene breaks were restored in derived working copies.
Chapter 11 parts were joined only after matching the previously recorded hash.

All 14 units are `translated`; none is represented as reviewed. The old empty
review ledger is preserved. A synthetic next-edition trial, kept outside the
repository, preserved all 14 translation hashes and identified one new unit.
The automatic legacy-source guard remains enabled pending integration testing.
