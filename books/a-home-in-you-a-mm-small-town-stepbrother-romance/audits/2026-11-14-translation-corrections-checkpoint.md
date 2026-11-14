# A Home in You — source-faithful Russian correction checkpoint

Date: 2026-11-14. Candidate branch: `fix/a-home-in-you-names-review-20261114`
(PR #108). Pinned workflow: `ea9963ca546b7cc7f6aba4dc5350fa19ea7da862`.
Preserved source: `source-000001` (original EPUB and extracted English files unchanged).

## Editorial rule for this correction pass

The **English original is authoritative** for age, chronology, actions, speakers,
family relationships, emotional tone and narrative meaning. Correct Russian
grammar and punctuation without inventing plot changes. Previously requested
age alterations are not a substitute for a faithful translation of the
source; never silently relabel an adaptation as a source-faithful edition.

## Corrections persisted on the PR branch

| Unit | Verified commits | Change |
| --- | --- | --- |
| 007 author message | `2de9805e37da0a6edd841d9d3b6d2a507d151396` | Two proper-name declensions and a natural, source-consistent opening sentence. |
| 011 beginning narrative | `cf9e5209c8fe9f005aff0cbdeb9223a127cbbc0a`; `502542894f7dfd0086056b45f6692e63f5cabab9` | Fixed a source-contradicting age sentence; fixed eleven Russian dialogue-tag punctuation instances. |
| 012 Cade | `c02005ddec31f48b03e3686b9826840a0be09d6b` | Fixed eight Russian dialogue-tag punctuation instances. |
| 013 Cade | `f64862df4ed4d74a6a6a4bf3856e350e5deb7086`; `f18b2dd5f2008c4d2851722c1597e7fc5cc03d02` | Corrected name cases and speaker attribution, then two additional case/voice/fidelity sentences and four dialogue-tag punctuation instances. |
| 026 Dillon | `674b1a50bcae8e8d1cc481e50c4e21e861bb48c5` | Corrected `для меня и Кейда`, restored the proper subject of Cade's race win, and repaired two literal `\\u2014` artifacts. |

All five modified files were read back after GitHub writes and matched the
intended candidate content. Their source/target counts and ordered values
of `bt-scene-break`, `bt-anchor`, `bt-block` markers and Markdown link
destinations matched in a read-only structural spot check (zero relevant
markers in the examined source units). No Unicode em-dash escape or the
checked Russian guillemet+dialogue-tag omission remained in these five files.

A narrow pattern scan was also performed across the 39 existing PR candidate
units for common bare-case name errors, missing Russian dialogue punctuation
in guillemet/tag combinations, and literal Unicode punctuation escapes.
This **is not** a complete literary review and may have false positives and
false negatives. Do not claim that it proves grammatical or semantic coverage.

## Still required before a corrected EPUB exists

1. A source-linked literary correction/review pass on all affected units.
   Earlier accepted `reviewed` records still bind original bytes, not PR text.
2. An explicitly authorized, provenance-preserving canonical reopen/accept
   transition. The pinned `TranslationAcceptanceManager.accept()` returns
   verification for `reviewed` units and cannot re-accept changed bytes.
   Do not merge PR #108 as-is or forge fresh PASS evidence.
3. A proper independent Reviewer PASS on each changed exact translation
   artifact; correct further findings where safe and appropriate.
4. Rebuild EPUB through the exact pinned workflow, then verify artifact
   SHA-256, source identity, all units, all links and accepted review state.
5. Retain the old EPUB as the traceable previous revision.

**Status: editorial corrections staged; new final EPUB NOT BUILT;
PR #108 remains draft; canonical translation and review state on `main`
left unchanged.**

## 2026-11-14 continuation: source-faithful editorial correction pass

This follow-up is limited to **candidate translations in the PR branch**.
It did not change the original EPUB, extracted English, workflow pin, canonical
`main` progress/review ledger, or shipped EPUB. The user's latest instruction
is to preserve the meaning of the English original, not silently re-age the
characters or invent altered events.

**48 targeted text replacements were persisted in 13 units** (each commit read
back from GitHub and content verified). They correct confirmed Russian case
errors, chronology and tense in the prologue, dialogue-tag punctuation, speaker
attribution and source-consistent literary wording. No blanket replacement
can be considered literary review.

| Unit | Changes | Verified commit(s) |
| --- | ---: | --- |
| 008 trigger warnings | 2 | `bc98b483614fa5e3c02b7c13eed6873dcc6a083a` |
| 009 prologue | 5 | `ded29c23e5760a8176c0786140f068bacbb343f6` |
| 011 opening narrative | 18 | `60022ff1c68387c44e521d9cbc4bae69c45bbb72` |
| 012 Cade | 5 | `b9e98b35e7c3240751126ffd0dcee0eeb35b0237` |
| 013 Cade | 1 | `427e80ade4ce4504d43a82ac296c3de1818c5d33` |
| 016 Cade | 3 | `7a31ad5ff22beb5c5ef7b474f7975abdd36d370a` |
| 019 Dillon | 5 | `b7dd8296d4335ac28999f07e2fa205b774961929`, `8f9a4fa5fa3e37e5d9bd60f699d843a693e37d25` |
| 023 Cade | 2 | `9846beedd752f20a04674cf1b465b45237cff69b` |
| 037 Dillon | 1 | `0242209f47dbe637462e9ad6a8946d29de765d1d` |
| 040 Cade | 1 | `a31d0e8d3e746b1c40e7cf5ee4121b3810b3fbf7` |
| 045 Cade | 1 | `f4e63f7deb9978ee3bb51851d59ddb72ebc82982` |
| 047 Dillon | 3 | `952149fab2afd6622c593a9d128f63ad4fc91f33` |
| 048 Dillon | 1 | `f51b589aadd81a6eabb32e621f899f1afa6fed1d` |

### Integrity checks and limits

- Source and candidate translations were compared for all **13 edited units**
  with respect to ordered `bt-*` markers, Markdown link destinations and
  heading counts; all compared structures matched.
- A focused, Unicode-aware language-pattern scan found further nominative
  names in indirect grammatical roles. Candidate-only corrections were made
  when the English reference supported them; apparent matches involving
  correctly inflected names or the indeclinable name `Марко` were not blindly
  replaced.
- Pattern scans are incomplete by design. They cannot find all fidelity,
  grammar, dialogue, continuity, or inflection defects. The previous editorial
  report already demonstrated that the former automated PASS was insufficient.
- **Some units still have unresolved literary issues**, including material
  outside this bounded pass. No fresh independent full-chapter PASS has been
  recorded; no reviewed status has been reopened; no accepted replacement EPUB
  has been built.

**Gate: DO NOT MERGE PR #108 or deliver it as final quality-assured EPUB** until
there is an authorized, canonical, provenance-preserving reopen path compatible
with this book's pinned workflow, exact-artifact translation acceptance,
independent full-source review of each affected unit, and a verified rebuild.


## 2026-11-14 later continuation — source-verified candidate repairs and CI diagnosis

**Scoped correction work, not a canonical lifecycle advancement.**

After reconstructing metadata and PR #108, five more source-bound grammar corrections
were committed to the candidate branch, with read-back of the exact target text:

| Unit | Original source-grounded correction | Commit |
| --- | --- | --- |
| 016 (6 Cade) | `дедушка Диллон` → `дедушка Диллона` | `ee53e565df2c7d0cea2e7b85e85b457e40d09732` |
| 018 (8 Cade) | `позади Диллон` → `позади Диллона` | `668ee2309d9d49a54fda4b08a3d0ad96d8c103ff` |
| 021 (11 Dillon) | `увёл Кейд` → `увёл Кейда` | `afe45f1c46a4f9c1d0253d28280d305193effeb3` |
| 023 (13 Cade) | `дом Диллон` → `дом Диллона` | `f12f4f2485ad9402ee2cd56203c7ec1a5206a00e` |
| 034 (24 Dillon) | `Забрал Кейд` → `Забрал Кейда` | `eadf11aca9b1aae81afaf60d0d6cdaed903aa00b` |

Read-only pattern scans of all applicable draft literary-unit texts were
performed in bounded batches: prepositions, clear accusative/genitive
contexts, missing dialogue-tag dashes and literal Unicode escapes.
These are **heuristics**, not evidence of complete independent review;
a negative finding is not a PASS, and proper-name `Марко` is indeclinable.

### Reproducible CI blocker

[GitHub Actions run #43605718766](https://github.com/tim8es/book-translator-private/actions/runs/43605718766)
failed at the `Validate changed books with each book's pinned public workflow` step.
The pinned `scripts/book.py validate` and `scripts/corpus.py verify`
both rejected the candidate draft, beginning with **chapter 3**:
`progress.json: chapter 3 translation_acceptance sha256 mismatch`.
Accepted SHA-256 from historical evidence was
`b86c7b68cff1e725e80fff35b3cf11e8cf1b438045d70e29a52da9262191a398`,
but the draft text SHA-256 was
`44ef95b5ac4e15e97e1cde4a740d3e58764dd7ae0c9c947ae282a14ffd8ddf12`.
That sample refers to the earlier commit `f12f4f2`; later candidate edits
may change individual text hashes, but **do not resolve** the underlying
lifecycle mismatch.

A book is not finalized merely because `progress.json` says 51/51
`reviewed`: those accepted bytes belong to the previous edition.
Do not rewrite their old SHA identities, reuse old PASS to validate new bytes,
or merge the draft unchanged. A canonical correction/reopen transition
compatible with the pinned workflow is still required, or an **explicitly
authorized** workflow upgrade introducing one.

No public workflow code, main-branch book state, original text or shipped EPUB
was changed during this continuation.

**Result: candidate edits persisted; quality-assured corrected EPUB NOT READY.**

## Manual ChatOps continuation — source comparison without Auto

This continuation was performed manually through GitHub; no Auto translation
job was started. Source EPUB and English extracted units remain immutable.

| Unit | Edits | Commit | What was source-checked |
| --- | ---: | --- | --- |
| 003 TOC | 2 | `0fa9d500e00c8b3902900531c966f5f2b398226c` | Russian TOC headings align with corresponding section headings |
| 004 copyright/credits | 4 | `fb80d88998ae7810d7399974da46bc09aa2f357c` | Accurate Russian copyright, publisher and typesetting labels |
| 007 author note | 7 | `4b62528f1cc995a6474be0a291a1bccc85c139f0` | Author's facts, voice and Russian grammar |
| 008 warnings | 1 | `e5fe7c8a76eca865ed179e92e14ff373a38e705f` | Source-specific warning preserved precisely |
| 011 opening | 2 | `0e6802823157651010160145a1a43c40bc701c7d` | Narrator's original register and narrative sequence |
| 014 wedding | 4 | `fbba5c675f0aef293e7a4078eea7432fe9b66cfb` | Cade's speaking identity and inflected names |
| 016 country store | 6 | `7ceec59f2398d85be4e86f43591ce2fa6b527ad0` | Dillon's speaking identity and inflected names |
| **TOTAL** | **26** | | **7 files; each GitHub write read back and verified** |

### Read-only integrity diagnostics

- Independently fetched all 51 source-unit Markdown files and 51 candidate
  target-unit Markdown files. In **all 51 pairs**, the ordered Markdown link
  destinations, ordered `<!-- bt-* -->` markers, and Markdown heading counts
  were identical. This does not establish complete textual coverage.
- Searched all 51 candidate target files for literal Latin spellings of
  Dillon, Cade, Darren, Christian, Evelyn, Jared, Aaron, Darius and Raven
  in ordinary text, excluding lines with URLs/attribution. **Zero** matches.
  This is a narrow transliteration check, not a grammar or meaning PASS.
- Source-linked review exposed speaker errors and invalid inflections after
  the Latin names had all disappeared, so the chapter-wide literary review
  remains necessary.

### Blocking gates unchanged

The candidate branch has modified already-reviewed bytes without a current
canonical reacceptance. Earlier GitHub Actions book validation correctly failed
SHA-256 checks. The pinned workflow provides no verified reopening transition.
Do not rewrite old evidence, merge an invalid translation candidate into
`main`, call the candidate independently reviewed, or claim a rebuilt EPUB.
The original source, `main` progress/review ledger and output EPUB are unchanged.

## Manual ChatOps correction addendum — Unicode-aware speaker QA

A subsequent source-grounded read of units 014 and 016 discovered
**additional misattributed dialogue** left by the earlier English-name
replacement. A previous narrow JS diagnostic had used a non-Unicode
word-boundary token and produced misleading false negatives for
Cyrillic speaker names. The expression was repaired to use Unicode
letter/number boundaries, and the affected source sentences were
reopened before every correction. This is an audit correction, not a
claim of full independent review.

**22 more individual fixes across 11 translation-unit files** were
recorded after the 26 fixes in the preceding section:

| Unit | Changes | Commit(s) |
| --- | ---: | --- |
| 014 | 2 | `26526c84c0d4ba2fa90d2bcc8f221d1cc9386f43`, `716f0dc5819a52faa89635997510ad10231cd06e` |
| 016 | 1 | `755794a0c023f77e0456dee998440b104fa58cf0` |
| 017 | 1 | `4452c1a29fd7b524772a57da1725a4675af614ed` |
| 019 | 3 | `94a7032c956c3b2d865102de7206e08ceca43f24` |
| 021 | 1 | `b7546d542ee405b2b28d2cafe8e13fe0c1ae8562` |
| 022 | 7 | `784a6e0a0d477f2caa8483dda77fc7fdbd9e6ae4` |
| 023 | 1 | `92a2e3da6bce5803a8c1858a81657a2db81ee43e` |
| 029 | 2 | `88cbd892cac25d68c5f19e64b7b5c88465f18da2` |
| 034 | 1 | `73cf64af81a075809b416e114174e1023e33c4f4` |
| 035 | 1 | `ee563727da017f863c2c389edb0c4a7af3f91a2d` |
| 045 | 1 | `f068e74fb0e4d3515322efe7f7e1a02e1a9cf4c3` |
| 047 | 1 | `97e628d0e4f054a0026d304442840d02931da852` |
| **Total** | **22** | **12 distinct units** |

A clear example was `сказал Диллону` used for source `Dillon
said`, and `сказал Кейду` used for source `Cade said`. Another
example, `отец ... сказал Диллону`, was verified as a correct
addressee case and left unchanged. No blind dative-to-nominative
replacement was applied.

The narrower all-unit Latin-name and structure checks documented
above are unchanged, but these new findings prove they cannot serve
as proof of complete Russian grammar or fidelity.

**Manual edits in this current ChatOps conversation: 48 across the
book. No Auto translation invoked.** As above, these candidate files
have not been canonically re-accepted or independently re-reviewed;
PR #108 must stay draft.
