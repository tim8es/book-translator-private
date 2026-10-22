# Chapter 28 — Reviewer findings (2026-10-22)

- Stable unit: `chapter-000030` (narrative Chapter 28, *Where Is My Alpha?*).
- Reviewer session: `cm-middle-reviewer-20261022-unit030`.
- Workflow revision: `5e0731da8b7ca81ada5316ed536a8a954008b789`.
- Review decision: **CORRECTIONS_REQUIRED**.
- This is a bounded review that located blocking fidelity discrepancies. It is **not** full-chapter PASS, nor an exhaustive semantic comparison. The canonical source and Russian translation were read in aligned paragraph order from GitHub. The original English extraction has 245 nonempty paragraphs, Russian translation 243, with an opening two-paragraph offset due to the imported banner / note-navigation text.

## Actionable discrepancies

Paragraph numbers below are **0-based nonempty paragraph positions in the extracted English Markdown**, not EPUB source-block indices.

1. **EN paragraph 60; RU paragraph 58 — omitted dialogue.** Yoongi says an explicit "Thank you" between reassurance and his intention to stay with his mate. The Russian version omits that expression of gratitude. Restore it in its proper position, preserving speaker and register.

2. **EN paragraph 63; RU paragraph 61 — direction of a ritual action changed.** Jungkook is instructed to **receive** the water Namjoon passes to him; the Russian text makes him **hand over** the water on request. Recheck the scene and translate who gives/receives water correctly. The source's object and direction must not be reversed.

3. **EN paragraph 23; RU paragraph 21 — changed parental metaphor.** Namjoon complains that he is everyone's "appa", while nobody is **his** appa. The Russian ending broadens this into his having *nobody at all*. Restore the specific reciprocal parental-role meaning, without implying he has no people around him.

4. **EN paragraph 18; RU paragraph 16 — narrowed medical scope (check in context).** The source requests supplies so anyone injured can treat themselves. The Russian rendering specifies only *treating a wound*; verify whether the broader original should be preserved with an expression such as first aid, while keeping the concrete meaning of the scene.

## Required follow-up

- Translator obtains a separate active durable Translator claim for this exact unit, applies corrections to `translated/030-chapter-28-chapter-28-where-is-my-alpha.md`, and obtains fresh `accept-translation` evidence for changed bytes.
- An independent Reviewer compares corrected source and translation in full, including later paragraphs, chapter notes and dialogue; only then can a new current PASS be recorded and `accept-review` advance the status.
- Do not manually raise the status in `progress.json`. Do not alter source corpus, metadata, glossary or global shared state on the basis of this finding alone.
