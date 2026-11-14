#!/usr/bin/env python3
"""Book-local, read-only, source-aware review terminology preflight.

Does not generate PASS evidence or mutate translated/, progress, the ledger
or the pinned literary workflow. A clean result is necessary but not sufficient
for quality: case inflections and semantic fidelity still require a Reviewer.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SOURCE_NAME_TYPES = {"character", "nickname", "person", "place", "form of address"}
INTENTIONALLY_RETAINED = {
    # Named organizations, game titles and URLs remain Latin by glossary policy.
    "A Home in You", "Xbox", "Skyrim", "OceanofPDF.com",
    "Jumpin’ Java Bean", "UVA",
}


def _book_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _glossary_terms(glossary: str) -> list[tuple[str, str]]:
    terms: dict[str, str] = {}
    for line in glossary.splitlines():
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0] == "Original":
            continue
        original, translated, kind = cells[:3]
        if (kind not in SOURCE_NAME_TYPES or original in INTENTIONALLY_RETAINED
                or not re.search(r"[A-Za-z]", original)
                or not re.search(r"[А-Яа-яЁё]", translated)):
            continue
        # A transliterated single name may appear with Russian case endings.
        # Never demand nominative exact-string substitution.
        if original in terms and terms[original] != translated:
            raise ValueError(f"conflicting glossary values for {original}")
        terms[original] = translated
    return sorted(terms.items(), key=lambda pair: (-len(pair[0]), pair[0]))


def _matches(text: str, source_term: str) -> list[dict]:
    # Only a stand-alone Latin word/phrase. Never flag it inside a longer word.
    regex = re.compile(r"(?<![A-Za-z])" + re.escape(source_term) + r"(?![A-Za-z])")
    lines = text.splitlines()
    result = []
    for number, line in enumerate(lines, 1):
        if "](http" in line or "](#" in line:
            # Do not silently skip link LABELS. Only strip raw link destinations.
            line = re.sub(r"\]\((?:https?://|#)[^)]*\)", "]()", line)
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        for match in regex.finditer(line):
            result.append({"line": number, "column": match.start() + 1})
    return result


def _required_case_warnings(text: str) -> list[dict]:
    # Minimal high-confidence grammar sanity check; not a syntactic parser.
    warnings = []
    stems = r"(?:Диллон|Кейд|Даррен|Кристиан|Аарон|Дариус)"
    patterns = [
        ("instrumental", re.compile(r"\b(?:с|со|перед|между|над)\s+" + stems + r"\b")),
        ("dative", re.compile(r"\b(?:к|ко)\s+" + stems + r"\b")),
        ("genitive", re.compile(r"\b(?:у|от|для|без|ради|около)\s+" + stems + r"\b")),
    ]
    for n, line in enumerate(text.splitlines(), 1):
        for rule, regex in patterns:
            if regex.search(line):
                warnings.append({"line": n, "rule": rule})
    return warnings


def check(book: Path) -> dict:
    glossary = (book / "glossary.md").read_text(encoding="utf-8")
    progress = json.loads((book / "progress.json").read_text(encoding="utf-8"))
    terms = _glossary_terms(glossary)
    results = []
    scanned = 0
    for chapter in progress["chapters"]:
        source_path = book / chapter["source_path"]
        translated_path = book / chapter["translation_path"]
        source = source_path.read_text(encoding="utf-8")
        translated = translated_path.read_text(encoding="utf-8")
        scanned += 1
        findings = []
        for original, expected in terms:
            # A name not present in this source unit should not be required
            # in its Russian translation, but stray literal English is
            # flagged irrespective of source presence.
            hits = _matches(translated, original)
            if hits:
                findings.append({
                    "original": original, "expected_base": expected,
                    "count": len(hits), "locations": hits[:20],
                    "source_mentions": len(_matches(source, original)),
                })
        case_warnings = _required_case_warnings(translated)
        if findings or case_warnings:
            results.append({
                "unit_id": chapter["unit_id"],
                "chapter": chapter["number"],
                "untranslated_names": findings,
                "obvious_case_warnings": case_warnings,
            })
    return {
        "units_scanned": scanned,
        "glossary_terms_checked": len(terms),
        "affected_units": len(results),
        "literal_name_occurrences": sum(
            f["count"] for c in results for f in c["untranslated_names"]
        ),
        "case_warnings": sum(len(c["obvious_case_warnings"]) for c in results),
        "results": results,
        "notice": "Not a literary PASS; independent source-linked review remains mandatory.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", type=Path, default=_book_root())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = check(args.book.resolve())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("units:", report["units_scanned"],
              "untranslated names:", report["literal_name_occurrences"],
              "obvious case warnings:", report["case_warnings"])
        for row in report["results"]:
            print("unit", row["chapter"], "issues",
                  sum(x["count"] for x in row["untranslated_names"]),
                  "case warnings", len(row["obvious_case_warnings"]))
    return 1 if report["affected_units"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
