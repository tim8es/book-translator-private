# Policy Change — preliminary source/draft reconciliation (NOT canonical review)

Date: 2026-10-30. Original source: `Policy Change - original.epub`, SHA-256 `b27e61a767dd5ba93451cf0b1df5ad8d6c40b11bdead7435e0ca682768378639`.

**Scope:** Local ZIP/OPF/XHTML reading-order inspection against backup drafts 1–7. This is a triage aid only. No machine `source-coverage`, claims, acceptance, or independent review evidence was created.

## Exact structural facts
- EPUB container passes ZIP CRC (`testzip() = None`).
- OPF metadata: `Policy Change`, `josie_ides (josephides)`, en.
- OPF spine has **65** XHTML items. The document's metadata explicitly says **25/25 chapters** (177,819 words), with introductory metadata/summary, split chapter headings/summaries, distinct end notes, and final credits. Do **not** equate 65 spine items with 65 narrative chapters.
- Chapter 3 heading and summary live in `index_split_004.html`; the main prose and opening chapter notes begin in `index_split_005.html`; end notes are in `index_split_006.html`.
- Chapter 6 body and opening note appear in `index_split_010.html`; its **substantive end note** is in `index_split_011.html`.
- Chapter 7 body is in `index_split_012.html` and its end notes are in `index_split_013.html`.
- The original includes **19** same-document relative fragment links (`index_split_NNN.html#page_N`); all 19 target anchors exist. They occur in spine files 005, 008, 010, 012, 014, 019, 022, 025, 028, 031, 038, 041, 044, 047, 050, 053, 056, 059, 062 (zero-based file suffixes).
- Existing draft chapters 1–7 show **zero Markdown links and zero explicit fragment markers**. At least draft chapters 3, 5, 6, 7 therefore do not preserve these source link structures. Reconcile under revised extraction before canonical acceptance.

## Draft-specific triage
| Backup draft | Observations | Status |
|---|---|---|
| 1 | Main body reaches the same narrative ending as source Chapter 1; completeness not machine validated. | UNVERIFIED_DRAFT |
| 2 | Summary and main prose saved, ending aligns in broad terms; completeness not machine validated. | UNVERIFIED_DRAFT |
| 3 | Summary, main prose, and end note represented, but original hyperlink/anchor structure is not represented. | UNVERIFIED_DRAFT |
| 4 | Main prose saved; completeness not machine validated. | UNVERIFIED_DRAFT |
| 5 | Opening/end notes represented; original hyperlink/anchor structure is not represented. | UNVERIFIED_DRAFT |
| 6 | **Confirmed missing source content:** `index_split_011.html` contains a Chapter End Notes section mentioning seeing hockey in Montreal in **2016**, 91k WIP, and the original-character tag. Saved draft `chapter-06-ru.md` ends directly after the narrative with the sashimi scene, contains no `2016` and no translated end-notes section. Also loses source hyperlink/anchor structure. | UNVERIFIED_DRAFT — REQUIRES SOURCE-ALIGNED REPAIR |
| 7 | Backup explicitly marked incomplete; source end notes and remaining narrative not yet established in draft. Also lacks original hyperlink/anchor structure. | INCOMPLETE |

## Mandatory next gate
Before any genuine translation/reviewer claim, place the **exact original EPUB** inside a writable canonical workflow installation at the selected revision, run `book.py extract`, `corpus.py seal`, `book.py validate`, `corpus.py verify`, and independent SHA-bound EPUB `source-coverage` successfully. Then map drafts to extracted stable unit IDs; repair omissions/markup and accept only with live claims, CAS and proper machine checks. Do not convert this report into a PASS.
