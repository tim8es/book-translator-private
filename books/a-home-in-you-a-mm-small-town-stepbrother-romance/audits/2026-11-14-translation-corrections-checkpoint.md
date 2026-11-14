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

**22 more individual fixes across 12 translation-unit files** were
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

## Additional critical fidelity finding — unit 024, not resolved

Source: `extracted/024-14-dillon.md` (immutable original);
candidate: `translated/024-14-dillon.md` in draft PR #108.

- Source dialogue opening `Nervous?` occurs once at **source line 109**.
  The Russian candidate's `— Нервничаешь?` occurs twice,
  **candidate lines 127 and 131**.
- Sequential manual comparison showed that beyond this duplicate the
  candidate diverges substantially from the source in the later
  passage and includes material not supported by the English source.
- The affected scene is about **characters explicitly aged fifteen
  and a half in the source** and contains sexual content. The
  assistant did not generate, reconstruct, or modify that content
  in the candidate file. This is a **blocking unresolved fidelity
  finding**; do not treat the current target as faithful, reviewed
  or suitable for release.
- Earlier **structural marker/link/heading comparisons** did not
  catch this, reinforcing that such checks cannot replace a full
  source-linked literary review.

A prior non-explicit omission in the **same unit** was repaired
directly against the original in
`4ab58ec27a1eb00a98f1fc20c113fd759a6b1e57`:
the narrator's missing remarks about uncertainty and not wanting
to date someone purely to prove a point. No further sensitive scene
text was produced.

**Result: CORRECTIONS REQUIRED; final EPUB blocked for substantive
fidelity and existing canonical hash/review reasons.**


## 2026-11-14 — unit 024 duplication and non-source insertion removed

The user explicitly requested fixing the duplicate line and material not
supported by the original.

- Candidate unit: `translated/024-14-dillon.md`.
- Source: immutable `extracted/024-14-dillon.md` from source revision
  `source-000001`.
- Commit: `13177a27116600734b3b4ef60a2e57b957e6c9a3`.
- Deleted the **second copy** of a repeated Russian question and its
  repeated response, along with subsequent invented, unsupported dialogue
  and prose in the same non-source block: **nine lines in total**.
- Checked the written candidate from GitHub: exactly **one** occurrence
  of that short Russian question remains. The invented block's checked
  prose and dialogue anchors are absent.
- **Critical open issue:** the English source contains a materially
  longer scene not faithfully represented in the current candidate. The
  affected original depicts sexual material involving explicitly
  underage characters. The correction deliberately **did not generate,
  reconstruct or rewrite** explicit content involving minors.
  Consequently the target now has a **translation coverage gap** in
  this chapter. This cannot be treated as an editorial PASS.
- The previously restored, non-explicit discussion earlier in this unit
  remains intact. Other units, original source, pinned workflow, review
  ledger, canonical `progress.json`, and EPUB remain untouched.

**Unit 024 verdict: CORRECTIONS_REQUIRED — duplicated/invented material
removed; original-content coverage is incomplete. Do not merge PR #108,
claim full review or build a corrected final EPUB from this draft.**


## 2026-11-14 additional manual source-paired chapter correction pass

**Operator route:** ChatOps, manual source/target examination and narrowly
targeted GitHub writes. **No Auto translation workflow was invoked.**
This pass preserves the existing book workflow revision
`ea9963ca546b7cc7f6aba4dc5350fa19ea7da862`, original source EPUB,
original extracted English units and unchanged canonical `main` ledger.

The earlier narrow Latin-name check had found no remaining romanized
character names but missed many **Cyrillic nominatives used incorrectly in
indirect cases**. Full-page source-paired examination of successive sections
and an expanded Unicode-aware grammar-candidate scan exposed these errors.

| Unit | New fixes | Verified GitHub commit(s) |
| --- | ---: | --- |
| 014 — wedding | 1 | `bbbb7c831dc78ce095da043fa245e30f170fc442` |
| 015 — home/running | 6 | `3f1e8e17c41aa5efb76c78af5f973e38212c3c8c`, `55830c1d330f5ed98316e4c2fb9c290ae2bfdf9a` |
| 016 — country store | 1 | `5bfde5e4f78bd526e769b7ba2a263ceff9d21aec` |
| 017 — horses / family | 6 | `42f7860963ae655d499264e1ce0e8cf8ee8b14cb` |
| 018 — pond / confidences | 4 | `de04afb92944893656fe919b851882a00711829b` |
| 019 — fair | 10 | `c9ec464f09be3ce46a3a52aed181de980677342b` |
| 021 — school | 1 | `7090d47e17df8d88560538062a4fa1d270f272d9` |
| 022 — football / secrecy | 8 | `076940dd60731545e8bb92134629f5dd97023bdf` |
| 023 — costume party | 7 | `a52a06064d244bf1d6161d5d08ac24c71ea8927d` |
| 025 — school athletics | 1 | `99694dce226931c50204d7187db084d91dc6c130` |
| 026 — family celebration | 1 | `dc76b46cbac825266dbfb182d684cd7fc75b4159` |
| 030 — family separation | 13 | `2c6af5c6b22aecb3bf068df58f30dfaf87d7b395` |
| 048 — college graduation | 1 | `79c5c547c48b057f6103246a56a4b8b4dab60260` |
| **Total** | **60** | **13 distinct units** |

Every modified file was fetched again from GitHub after writing and its
exact intended candidate content was verified. A subsequent **13/13
source-versus-candidate structural comparison** passed for ordered bt
markers, Markdown link destinations, and counts of Markdown headings.

The scope was editorial repair of specific non-explicit wording and name
cases (e.g. `вслед за Кейда` → `вслед за Кейдом`) and one explicit
source-supported speaking attribution. It did **not** alter original
material, invent missing paragraphs, generate sexual content involving
underage characters, or claim a fresh independently reviewed PASS.

### Remaining quality/release gates

1. The previous candidate still has an unresolved original-content gap
   in unit 024, and other chapters may contain omissions or semantic
   departures that these targeted case repairs cannot detect. Full
   sequential independent source-linked literary review is incomplete.
2. PR #108 contains modified text for records still marked `reviewed`
   against the **old accepted SHA-256**. Normal pinned workflow
   validation fails. There is no proven revision-compatible canonical
   reopen/translation-accept/review transition currently active.
3. Do not merge the draft, re-label historical PASS as current, or
   build/deliver a replacement *final* EPUB before these gates pass.

**State: source-grounded candidate corrections committed; not an
approved full revised edition.**


## 2026-11-14 all-51 structural coverage triage (read-only)

Retrieved exact extracted English and candidate Russian Markdown bytes
from GitHub for **all 51 ordered units** and compared:
- total UTF-8 character lengths as an **advisory** ratio (Russian
  target character count divided by English source character count);
- number of nonblank Markdown lines, which approximate paragraph
  structure but may also differ because of dialogue formatting;
- chapter presence (all 51 pairs were readable).

Findings:
- All 51 source/target unit pairs exist on the examined refs.
- Ordinary substantial chapters other than unit 024 have **near-unity
  character-length ratios**, approximately 0.97 to 1.09
  (not a completeness proof and not an independent literary PASS).
- **Unit 024** is the prominent outlier:
  source `10,522` characters / 73 nonblank lines,
  candidate `8,452` characters / 67 nonblank lines,
  ratio approximately **0.80**. This corroborates the already-known
  substantial missing passage involving underage explicit material.
- Other nonblank-line differences appear in units 013, 014, 026,
  027, 028, 032, 038, 039, 040, 041, 044, 048; their character ratios
  are not comparably low. These are **advisory** and may reflect split
  dialogue or formatting, but they have not been semantically adjudicated.
- The check does not establish the absence of lost sentences,
  invented sentences, wrong speakers, contradictions, or grammatical
  errors. Numerous such case errors were found by manual reading despite
  close source/target character-length ratios.

**No lifecycle mutation, independent PASS, or final build occurred.**
The outstanding unit-024 substantive gap, remaining literary review,
and canonical SHA-bound reviewed-artifact reopening are still blockers.


## Manual ChatOps continuation after full-51 triage

No Auto translation workflow was started. Maintained pinned book workflow
revision `ea9963ca546b7cc7f6aba4dc5350fa19ea7da862` and kept
original English extraction, canonical main progress/review evidence and
old EPUB unmodified.

Source-paired, small-extent corrections made in **four files**:

| Unit | Fixes | Commit | Evidence |
| --- | ---: | --- | --- |
| 025 — school lunch and football game | 5 | `3a13e2abe31d2694d19c958fe67996bc1f1c7a71` | English source shows Dillon as addressee, person missed, lifted, or subject of comment; Russian grammatical cases corrected in safe/non-explicit paragraphs |
| 026 — running, gifts and family conversation | 7 | `aa87dfc5fbc451559ca27d7c73ad3d9c91876dbe` | English source establishes Cade as patient/addressee and Dillon as beneficiary or referent |
| 029 — argument with father | 4 | `be39f695f17f7399bd9be17bec9da6c16e7ca512` | Source explicitly describes an attempted attack on Dillon, taking Cade away and references to Dillon's responsibility |
| 048 — adult college epilogue | 3 | `24419a18934aa647e833c1ad19fd0e8d0028c890`, `a9b959facb92e5ff66092f8d5ea524d8ece161f2` | Two nominatives erroneously used as objects and an unnatural case/family-intent sentence restored |
| **Total** | **19** | | **Four distinct units** |

All five commit outcomes were checked by a fresh GitHub content read.
A subsequent source-versus-current-candidate check found identical
ordered Markdown link destinations, ordered bt markers and heading
counts for all **four** modified files. This is not full literary review.

**Concurrent editing observation:** after the unit 029 fix, the branch
advanced through `9b0a9d999fbfd606a29f7da2629eb9e536942386`
(unit 031) and `45fe7830f56d3998b390467214d997f6036e1cc5`
(unit 033), generated outside this specific sequence of file edits.
Upon seeing that unit 031's same grammar problems had already been
corrected, no duplicate write or overwrite was attempted. Do not
attribute those two commits to this audit pass without inspection of
their independent source/review evidence.

**Outstanding release barriers unchanged:**
- Unit 024 still has an untranslated source gap involving explicit
  content with minors; no repair of that passage has been generated.
- Current text of many previously reviewed units differs from
  translation_acceptance's historical SHA-256 in canonical
  `progress.json`; validation rejects it.
- There is no fresh, independent full source/target literary PASS and no
  verified new EPUB. PR #108 must remain **draft**.

This section is an operator correction checkpoint, **not an approval or
reacceptance**.
