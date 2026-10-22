# Reviewer findings — The Claiming Moon, narrative Chapter 45 (unit chapter-000047)

Outcome: **CORRECTIONS_REQUIRED** for the currently accepted `translated/047-chapter-45-chapter-45-a-little-less-than-forever.md`.

Reviewer session: `cm-reverse-review-47-20261022-1419`.
Pinned workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789`.
Accepted source SHA-256: `6f9d4e8765db722cc0dc7b3e7e5ebdd53f50356caf10605a09f9b4d031a53d3c`.
Accepted translation SHA-256: `98d883627115149a82b4736d4dee4fca9af194f047879e0f5380942e516c6ce1`.
Base progress GitHub blob: `a4eaffe8a5a0f076b95f9afdd232f34fc319ed88`.

## Concrete blocking mismatches compared independently with canonical source

1. **Missing original author-note line.** The original opening notes instruct the reader to see further notes at the end of the chapter. That statement is absent from the canonical Russian artifact. Restore an accurate sentence in the opening notes; this is source-authored auxiliary text.
2. **Missing narrative gesture in the palace kitchen.** Original semantic paragraph 542 begins with Taehyung sitting on a counter with his legs swinging and watching his toes. The canonical translation jumps directly to Jungkook making a mistake; the entire first sentence is missing. Restore the scene gesture in Russian.
3. **Incorrect change-of-size inference.** Original semantic paragraph 158 describes Yoongi yearning to feel how small the pups are as he holds them against his chest. The Russian makes the children "become small" when on his chest; restore a description of their actual size, not change in size.
4. **Original repetition reduced.** Original semantic paragraph 266 repeats `It was cold` before the observation about hail. Canonical translation collapses the two references to the cold into one. Preserve the author's repetition if retaining source rhythm.
5. **Ambiguous/misgendered referent risk.** Original semantic paragraph 425 explicitly says Namjoon embraced Jin from behind, using male-reference pronouns. The accepted Russian version uses `обнял её` because of grammatical noun `пара`, creating referential ambiguity. Reword clearly without changing relationships.

Findings 1–3 are unequivocal fidelity failures. Further reviewer comparison is still required after corrections. The note and selected scene comparisons **do not constitute exhaustive source coverage**, and the current translation cannot pass.

## Proposed correction artifact

`incoming/047-chapter-45-qa-corrected-unreviewed-v2-2026-10-22.md`

Reproducible patch manifest:
`incoming/QA_chapter_45_correction_proposals_v2_2026-10-22.json`

Both are staged drafts; the accepted `translated/` artifact has not been replaced. The manifest was verified by applying all five one-time replacements against the original canonical translation and comparing the resulting draft byte-for-byte.

## Next workflow step

Release this Reviewer claim after the machine-ledger record is successfully appended. Start a fresh Translator claim to correct and `accept-translation` the canonical artifact with a source/translation hash-bound CAS operation. Then construct a new independent Reviewer context, compare all original and Russian text sequentially, and record a new outcome. **No PASS should be entered based on this limited failure review.**
