# HTML import audit — 2026-11-24

Pinned workflow: `20521f143dbd0b06e9c10a60428cf6c0e02d330a`.

Original SHA-256: `9e49f0faac9f7749e0b7bfa8ddca663ecb8b2efb49ae6066def7ec2db473968c` (379167 bytes).

The normal HTML extraction CLI initially rejected local anchors `#endnotes1` through `#endnotes5` because `extract_chapters` calls `split_html_document` without `document_path`. For this initial import only, a local in-memory adapter supplied the original filename as `document_path` to the pinned `split_html_document`, with `skip_navigation=False` unchanged. It ran the same canonical initialization, preserving the original bytes and link markers. No persisted workflow files were modified. Seven reading-order units were extracted. `book.py validate` and `corpus.py verify` succeeded; canonical `corpus.py seal` also succeeded during initialization. A future restore from the original HTML may encounter the same CLI issue until the upstream HTML caller is corrected.

User explicitly instructed proceeding in the existing repository despite its public visibility. No Auto translation job was created.
