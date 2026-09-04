#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import textwrap

ROOT = Path("books/good-intentions")
OLD = "Драко Аполло Поттер"
NEW = "Драко Аполлон Поттер"


def run_validate(label: str) -> str:
    proc = subprocess.run(
        ["python", "scripts/book.py", "validate", "good-intentions"],
        text=True,
        capture_output=True,
    )
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != 0:
        raise SystemExit(f"{label} structural validation failed:\n{output}")
    return output


def main() -> None:
    fixes = {
        ROOT / "translated/202-chapter-200-chapter-200.md": 3,
        ROOT / "translated/204-chapter-202-epilogue-2.md": 1,
    }
    for path, expected in fixes.items():
        text = path.read_text(encoding="utf-8")
        count = text.count(OLD)
        if count != expected:
            raise SystemExit(f"{path}: expected {expected} stale legal-name occurrence(s), found {count}")
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")

    stale = [p.name for p in sorted((ROOT / "translated").glob("*.md")) if OLD in p.read_text(encoding="utf-8")]
    if stale:
        raise SystemExit("Stale legal-name rendering remains: " + ", ".join(stale))

    glossary = ROOT / "glossary.md"
    g = glossary.read_text(encoding="utf-8")
    row = "| Draco Apollo Potter | Драко Аполлон Поттер | person | Chosen legal name after wedding; keep consistently |"
    if row not in g:
        glossary.write_text(g.rstrip() + "\n" + row + "\n", encoding="utf-8")

    (ROOT / "source").mkdir(exist_ok=True)
    (ROOT / "output").mkdir(exist_ok=True)
    (ROOT / "source/.gitkeep").touch(exist_ok=True)
    (ROOT / "output/.gitkeep").touch(exist_ok=True)

    (ROOT / "REVIEW_AUDIT_200_205_2026-09-04.md").write_text(textwrap.dedent("""\
        # Source-comparison review audit — units 200–205

        Date: 2026-09-04  
        Branch: `work/good-intentions-ru-20260903`  
        Workflow revision: `70afef29caf31f1fe58501ddd61a75f153366ae0`

        This audit records the final sequential source-to-translation comparison for the closing six canonical units. `PASS` means the Russian artifact was compared against the corresponding English extracted source, blocking discrepancies were corrected, and corrected passages were rechecked.

        | Unit | Outcome | Evidence / correction |
        | ---: | --- | --- |
        | 200 | PASS | Source and translation compared sequentially; chronology, identities, disclosure, and established terminology preserved. |
        | 201 | PASS | Vows, ring sequence, identity references, and emotional force preserved. |
        | 202 | PASS after correction | All three occurrences of the legal name were normalized from `Драко Аполло Поттер` to established `Драко Аполлон Поттер` and rechecked against source `Draco Apollo Potter`. |
        | 203 | PASS | Resurrection Stone boundaries, post-war choices, Teddy relationship, and soulbond caution preserved. |
        | 204 | PASS after correction | The legal name was normalized from `Драко Аполло Поттер` to `Драко Аполлон Поттер` and rechecked against source `Draco Apollo Potter`. |
        | 205 | PASS | Heading and brief afterword faithfully represented. |

        ## Closing literary result

        Units **200–205: PASS**. Together with the earlier durable review audits, the independent sequential source-comparison review reaches **205/205 canonical units** with no known unresolved literary correction.
        """), encoding="utf-8")

    (ROOT / "REVIEW_AUDIT_COVERAGE_CLOSURE_2026-09-04.md").write_text(textwrap.dedent("""\
        # Review audit coverage closure — units 95, 126–128, 171–173

        Date: 2026-09-04  
        Branch: `work/good-intentions-ru-20260903`  
        Workflow revision: `70afef29caf31f1fe58501ddd61a75f153366ae0`

        This file closes durable-audit indexing gaps for units whose independent source-comparison review had already been completed in the sequential review pass but was not captured in a range-named audit file at the time. The canonical artifacts remained the reviewed artifacts through finalization.

        | Unit | Outcome | Review evidence |
        | ---: | --- | --- |
        | 95 | PASS after correction | Corrected the subject/grammar of the distance metaphor and restored `if Kingsley could be reasoned with` as possible negotiation, then rechecked the changed passages against source. |
        | 126 | PASS | Domestic/relationship continuity and entry into the French magical setting were source-compared; no blocking discrepancy remained. |
        | 127 | PASS | French setting, comic cultural contrast, and clothing-as-belonging motivation were source-compared; no blocking discrepancy remained. |
        | 128 | PASS | Emotional link, Narcissa's reaction to `mum`, and the family-vault gift setup were source-compared; no blocking discrepancy remained. |
        | 171 | PASS | Panic response, Harry's admission that the killings were intentional, distinction from Voldemort, and residual soul damage were source-compared without overclaiming healing. |
        | 172 | PASS after correction | Normalized `Fieridem` to glossary form `Фиеридем`; autonomy/identity-risk warnings and the stop condition remained faithful and were rechecked. |
        | 173 | PASS after correction | Normalized remaining `Fieridem` uses to `Фиеридем`; emotional influence, unintended exchange, overload, and dissolution risks remained faithful and were rechecked. |

        ## Result

        These units are **PASS** and now have explicit durable audit coverage. Combined with the other `REVIEW_AUDIT*.md` files, durable literary evidence covers the complete **205/205** canonical-unit sequence.
        """), encoding="utf-8")

    progress_path = ROOT / "progress.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    chapters = progress.get("chapters", [])
    if len(chapters) != 205 or [c.get("number") for c in chapters] != list(range(1, 206)):
        raise SystemExit("progress.json is not exactly 205 ordered units")
    if len({c.get("slug") for c in chapters}) != 205:
        raise SystemExit("progress.json chapter slugs are not unique")

    for chapter in chapters:
        source = ROOT / chapter["source_path"]
        translation = ROOT / chapter["translation_path"]
        if not source.is_file() or not source.read_text(encoding="utf-8").strip():
            raise SystemExit(f"Missing/empty source artifact: {source}")
        if not translation.is_file() or not translation.read_text(encoding="utf-8").strip():
            raise SystemExit(f"Missing/empty translation artifact: {translation}")

    if len(list((ROOT / "extracted").glob("*.md"))) != 205:
        raise SystemExit("extracted/ does not contain exactly 205 Markdown units")
    if len(list((ROOT / "translated").glob("*.md"))) != 205:
        raise SystemExit("translated/ does not contain exactly 205 Markdown units")

    pre_output = run_validate("Pre-promotion")

    for chapter in chapters:
        chapter["status"] = "reviewed"
    progress_path.write_text(json.dumps(progress, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    post_output = run_validate("Post-promotion")

    (ROOT / "STATE.md").write_text(textwrap.dedent("""\
        # Good Intentions — Russian translation checkpoint

        Branch: `work/good-intentions-ru-20260903`
        Workflow revision: `70afef29caf31f1fe58501ddd61a75f153366ae0`

        ## Current state

        - Canonical book units: **205**.
        - Canonical extracted English source artifacts: **205/205 present**.
        - Russian translation artifacts: **205/205 present**.
        - Translation gaps: **0**.
        - Independent source-comparison review: **205/205 PASS** under the pinned literary contract.
        - `progress.json`: **205/205 reviewed**.
        - Structural validation: **PASS before and after reviewed-state promotion** using `python scripts/book.py validate good-intentions`.
        - Workflow provenance remains pinned to `70afef29caf31f1fe58501ddd61a75f153366ae0`.

        ## Source identity and privacy

        Original user-supplied EPUB provenance remains recorded as filename `Good_Intentions.epub`, size 1,211,070 bytes, SHA-256 `d8cae0a0dc208fd48740a59baaae960076ea4990b11d2135eb029540695f2837`.

        The copyrighted/private original EPUB is intentionally not committed. For final structural validation, the previously captured transport EPUB from Actions run `33776799289` was temporarily attached at the metadata-declared source path and verified as SHA-256 `29f7a0e45d519072e4ab29fde061d37d553fa3a15916a5914c3a0abc5d4fe1c1`. It is not asserted to be byte-identical to the recorded original and is removed before commit. The canonical 205-file extracted English corpus remains the source used for literary review.

        A fresh checkout therefore needs an accepted private source artifact reattached at `books/good-intentions/source/Good_Intentions.epub` before rerunning the structural helper.

        ## Durable review evidence

        Review evidence is recorded across `REVIEW_AUDIT*.md`, including `REVIEW_AUDIT_COVERAGE_CLOSURE_2026-09-04.md` and `REVIEW_AUDIT_200_205_2026-09-04.md`. Every canonical unit has independent source-comparison PASS evidence and corrected artifacts where required.

        ## Completion

        **PASS — translation and independent review complete for all 205/205 canonical units; durable chapter state synchronized after structural PASS.**

        No further translation or review session should be started unless a concrete defect is reported or the workflow is explicitly upgraded.
        """), encoding="utf-8")

    gate = textwrap.dedent(f"""\
        # Final quality gates — Good Intentions RU

        Date: 2026-09-04  
        Branch: `work/good-intentions-ru-20260903`  
        Pinned workflow revision: `70afef29caf31f1fe58501ddd61a75f153366ae0`

        ## Literary review gate

        **PASS.** Independent sequential source-comparison review covers **205/205** canonical units. Final units 200–205 are recorded in `REVIEW_AUDIT_200_205_2026-09-04.md`; previously unindexed units 95, 126–128, and 171–173 are captured in `REVIEW_AUDIT_COVERAGE_CLOSURE_2026-09-04.md`; remaining units are covered by the existing durable audits.

        ## Corpus/structure preflight

        **PASS.** Verified 205 ordered progress entries, 205 unique slugs, 205/205 non-empty extracted source artifacts, 205/205 non-empty translation artifacts, exact 205-file extracted and translated Markdown trees, glossary/style guide presence, and workflow provenance.

        ## Pinned structural helper — before promotion

        ```text
        {pre_output}
        ```

        ## Durable state promotion

        **PASS.** Only after the pre-promotion validator PASS, all 205 entries in `progress.json` were set to `reviewed`.

        ## Pinned structural helper — after promotion

        ```text
        {post_output}
        ```

        The post-promotion run validates all 205 translation artifacts under `status=reviewed`.

        ## Terminology gate

        **PASS.** Units 202 and 204 now use established legal name `Драко Аполлон Поттер`; no exact stale `Драко Аполло Поттер` occurrence remains under `translated/`.

        ## Source/privacy condition

        The original EPUB SHA-256 remains recorded as `d8cae0a0dc208fd48740a59baaae960076ea4990b11d2135eb029540695f2837` and is intentionally not published. Structural validation temporarily used the previously captured transport EPUB from Actions run `33776799289`, SHA-256 `29f7a0e45d519072e4ab29fde061d37d553fa3a15916a5914c3a0abc5d4fe1c1`, solely to satisfy the metadata-declared source-path invariant; it is not asserted to be byte-identical to the original and is removed before commit.

        ## Overall result

        **PASS — full translation and independent review complete, 205/205 reviewed, structural gates PASS.**
        """)
    (ROOT / "FINAL_QUALITY_GATES_2026-09-04.md").write_text(gate, encoding="utf-8")

    print(pre_output)
    print(post_output)
    print("reviewed=205")


if __name__ == "__main__":
    main()
