# The Claiming Moon — reverse QA staging checkpoint

Generated 2026-10-22; authoritative lifecycle lives in `progress.json`. **This is an unreviewed correction workspace, not a final translation, acceptance, Reviewer PASS or EPUB.**

## Work performed

- Source and accepted Russian text checked in narrative chapters **31–45**.
- Confirmed original opening author instruction `See the end of the chapter for [more] notes` missing from all 15 canonical Russian chapters; a corrected **separate incoming draft** was created for every chapter.
- In chapter **31**, the nonsource-added `## Текст главы` heading was replaced by the omitted author note in the incoming draft.
- In chapter **45**, there are **four source-grounded patch proposals**, including the missing original scene action (Taehyung sitting with legs swinging on kitchen counter), restoring a repeated `It was cold`, and clarifying the Namjoon/Jin reference. The incoming revised draft applies all four as a proposed version.
- The readback for each of the 15 staged drafts was verified against the original accepted text plus exactly the documented edit(s). The drafts were not written into `translated/`.

## Staged files (unreviewed)

| Narrative chapter | Stable unit | Canonical accepted path, unchanged | QA draft path | Canonical status at checkpoint |
|---:|---|---|---|---|
| 31 | chapter-000033 | `translated/033-chapter-31-chapter-31-hollowed.md` | `incoming/033-chapter-31-chapter-31-hollowed-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 32 | chapter-000034 | `translated/034-chapter-32-chapter-32-the-things-that-follow-us.md` | `incoming/034-chapter-32-chapter-32-the-things-that-follow-us-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 33 | chapter-000035 | `translated/035-chapter-33-chapter-33-the-night-before-war.md` | `incoming/035-chapter-33-chapter-33-the-night-before-war-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 34 | chapter-000036 | `translated/036-chapter-34-chapter-34-a-miracle-written-in-blood.md` | `incoming/036-chapter-34-chapter-34-a-miracle-written-in-blood-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 35 | chapter-000037 | `translated/037-chapter-35-chapter-35-a-monster-for-his-mate.md` | `incoming/037-chapter-35-chapter-35-a-monster-for-his-mate-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 36 | chapter-000038 | `translated/038-chapter-36-chapter-36-let-me-know-every-part-of-you.md` | `incoming/038-chapter-36-chapter-36-let-me-know-every-part-of-you-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 37 | chapter-000039 | `translated/039-chapter-37-chapter-37-someone-tell-the-alpha.md` | `incoming/039-chapter-37-chapter-37-someone-tell-the-alpha-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 38 | chapter-000040 | `translated/040-chapter-38-chapter-38-one-pup-a-hundred-blessings.md` | `incoming/040-chapter-38-chapter-38-one-pup-a-hundred-blessings-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 39 | chapter-000041 | `translated/041-chapter-39-chapter-39-the-life-we-get-to-keep.md` | `incoming/041-chapter-39-chapter-39-the-life-we-get-to-keep-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 40 | chapter-000042 | `translated/042-chapter-40-chapter-40-journey-to-the-hefters-pack.md` | `incoming/042-chapter-40-chapter-40-journey-to-the-hefters-pack-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 41 | chapter-000043 | `translated/043-chapter-41-chapter-41-expect-the-unexpected.md` | `incoming/043-chapter-41-chapter-41-expect-the-unexpected-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 42 | chapter-000044 | `translated/044-chapter-42-chapter-42-tortured.md` | `incoming/044-chapter-42-chapter-42-tortured-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 43 | chapter-000045 | `translated/045-chapter-43-chapter-43-youre-my-kid-kook-ah.md` | `incoming/045-chapter-43-chapter-43-youre-my-kid-kook-ah-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 44 | chapter-000046 | `translated/046-chapter-44-chapter-44-the-past-that-didnt-last.md` | `incoming/046-chapter-44-chapter-44-the-past-that-didnt-last-qa-corrected-unreviewed-2026-10-22.md` | translated |
| 45 | chapter-000047 | `translated/047-chapter-45-chapter-45-a-little-less-than-forever.md` | `incoming/047-chapter-45-qa-corrected-unreviewed-2026-10-22.md` | translated |

## Source and workflow identity

- Pinned workflow: `5e0731da8b7ca81ada5316ed536a8a954008b789`.
- Source revision: `source-000001`.
- Source EPUB SHA-256: `611d1717e7997955619576a667073b79b815bf7606c6ea4513c823b01c53c9bb`.
- Progress GitHub blob SHA at checkpoint: `a4eaffe8a5a0f076b95f9afdd232f34fc319ed88`.
- Status summary at checkpoint: reviewed **3**, translated **41**, extracted **4**, total **48**.

## Other QA records

- `incoming/QA_reverse_chapters_31-35_2026-10-22.md`
- `incoming/QA_reverse_chapters_36-45_2026-10-22.md`
- `incoming/QA_reverse_author_notes_correction_queue_2026-10-22.json`
- `incoming/QA_chapter_45_correction_proposals_2026-10-22.json`

## Required next durable transitions

1. Freshly re-read `metadata.json`, `source-revisions.json`, `progress.json`, `review-ledger.json`, claims, glossary, style guide, canonical source, and canonical translation; validate the 48-unit source corpus and active source revision. Do not assume this checkpoint is current when another agent is active.
2. Only a current **Translator claim** for a unit may promote its staged correction into its canonical translation. Use `accept-translation` so the exact source/translation hashes and current progress revision are bound; release the claim.
3. Independently perform full original-vs-Russian comparison as **Reviewer** for the entire unit, from chapter 45 backward, with its own claim and context. Use `review-record` with `PASS` only after actual full literary comparison, otherwise `CORRECTIONS_REQUIRED`; orchestrator must invoke `accept-review` before status `reviewed`.
4. Do not treat structural paragraph alignment or the presence of author notes as proof of full fidelity. The extra chapter-45 narrative sentence was found by targeted comparison, and other omissions might still remain.
5. Keep the other agent's earlier chapter work and shared mutable state untouched unless current claims and CAS allow a transition. No final EPUB until all 48 units have current PASS evidence.

**No canonical translation bytes, original sources, `progress.json`, glossary, style guide or review ledger were mutated by this QA session.**
