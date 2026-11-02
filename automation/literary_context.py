"""Manifest-routed literary prompts and claim-bound shared-memory reconciliation.

This is an adapter for the *pinned* canonical workflow, not a second state engine.
Translator proposes glossary entries; independent Reviewer approves style observations.
The Orchestrator persists one target per claim through canonical ProposalManager.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from omniroute import ModelError, parse_review

MAX_SHARED_CHARS = 100_000
MAX_ITEMS = 40
_ALLOWED_ROLES = {"translator", "reviewer"}
_NAME_KEYS = {"original", "translation", "type", "notes"}
_STYLE_KEYS = {"source_pattern", "translation_approach", "evidence"}


def _one_line(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 700:
        raise ModelError(f"invalid literary memory field: {field}")
    if "\n" in value or "\r" in value or "<!--" in value:
        raise ModelError(f"unsafe literary memory field: {field}")
    return value.strip()


def _entries(raw: object, keys: set[str], field: str) -> list[dict]:
    if not isinstance(raw, list) or len(raw) > MAX_ITEMS:
        raise ModelError(f"{field} must be a bounded list")
    result = []
    for entry in raw:
        if not isinstance(entry, dict) or set(entry) != keys:
            raise ModelError(f"{field} entry has invalid keys")
        result.append({k: _one_line(entry[k], f"{field}.{k}") for k in sorted(keys)})
    return result


def _json_payload(text: str) -> object:
    value = text.strip()
    if value.startswith("```"):
        lines = value.splitlines()
        if len(lines) < 3 or not lines[-1].strip().startswith("```"):
            raise ModelError("incomplete fenced model response")
        value = "\n".join(lines[1:-1])
    return json.loads(value)


def parse_translation(text: str) -> tuple[str, list[dict], list[dict]]:
    try:
        data = _json_payload(text)
    except ValueError as exc:
        raise ModelError("translator must return a structured JSON response") from exc
    if not isinstance(data, dict) or set(data) != {"translation", "glossary", "style_guide"}:
        raise ModelError("translator response must contain translation, glossary, style_guide")
    translation = data["translation"]
    if not isinstance(translation, str) or not translation.strip():
        raise ModelError("empty chapter translation")
    return (translation.rstrip() + "\n",
            _entries(data["glossary"], _NAME_KEYS, "glossary"),
            _entries(data["style_guide"], _STYLE_KEYS, "style_guide"))


def parse_literary_review(text: str) -> tuple[str, dict, list[dict]]:
    try:
        data = _json_payload(text)
    except ValueError as exc:
        raise ModelError("reviewer must return JSON") from exc
    if not isinstance(data, dict) or set(data) != {"outcome", "checks", "findings", "style_guide"}:
        raise ModelError("reviewer response has invalid literary memory schema")
    style = _entries(data["style_guide"], _STYLE_KEYS, "style_guide")
    core = {key: data[key] for key in ("outcome", "checks", "findings")}
    outcome, report = parse_review(json.dumps(core, ensure_ascii=False))
    return outcome, report, style


def role_contracts(engine: Path, role: str) -> tuple[str, list[str]]:
    """Read selected revision's profile and validate every path before loading."""
    if role not in _ALLOWED_ROLES:
        raise ValueError("unsupported literary role")
    # The version-selected engine defines routing; this adapter must not
    # maintain a shadow copy of manifest path selection or optional overlays.
    scripts = str(engine / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from workflow.context_routing import contract_paths, read_manifest
    manifest = read_manifest(engine)
    files = contract_paths(manifest, role)
    mandatory = {"AGENTS.md", "docs/TRANSLATION.md",
                 "docs/TRANSLATOR.md" if role == "translator" else "docs/REVIEWER.md"}
    if not mandatory.issubset(set(files)):
        raise ValueError(f"missing required {role} role contracts")
    other_role = "docs/REVIEWER.md" if role == "translator" else "docs/TRANSLATOR.md"
    if other_role in files:
        raise ValueError(f"cross-role contract leakage in {role} profile")
    sections = []
    for path in files:
        target = (engine / path).resolve(strict=True)
        if not target.is_relative_to(engine.resolve()):
            raise ValueError("contract escapes pinned engine")
        contents = target.read_text("utf-8")
        if not contents.strip():
            raise ValueError(f"empty required {role} contract: {path}")
        sections.append(contents)
    return "\n\n".join(sections), files


def full_shared_context(book: Path) -> tuple[str, str]:
    glossary = (book / "glossary.md").read_text("utf-8")
    guide = (book / "style-guide.md").read_text("utf-8")
    if max(len(glossary), len(guide)) > MAX_SHARED_CHARS:
        raise ValueError("literary memory exceeds prompt budget; refuse silent truncation")
    return glossary, guide


def _cell(value: str) -> str:
    return value.replace("|", "\\|").strip()


def updated_glossary(current: str, rows: list[dict]) -> str:
    if not rows:
        return current
    if "| Original | Translation | Type | Notes |" not in current:
        raise ValueError("glossary template is not recognized")
    result = current.rstrip("\n")
    for row in rows:
        prefix = "| " + _cell(row["original"]) + " |"
        existing = [line for line in result.splitlines() if line.startswith(prefix)]
        target = f"| {_cell(row['original'])} | {_cell(row['translation'])} | {_cell(row['type'])} | {_cell(row['notes'])} |"
        if existing:
            if any(line.split("|")[2].strip() != _cell(row["translation"]) for line in existing):
                raise ValueError(f"conflicting glossary rendering for {row['original']}")
            continue
        result += "\n" + target
    return result + "\n"


def updated_style(current: str, rows: list[dict]) -> str:
    if not rows:
        return current
    heading = "## Automated reviewed stylistic decisions"
    header = "| Source pattern / context | Target-language approach | Reason / evidence |\n| --- | --- | --- |"
    result = current.rstrip("\n")
    if heading not in result:
        result += "\n\n" + heading + "\n\n" + header
    for row in rows:
        value = f"| {_cell(row['source_pattern'])} | {_cell(row['translation_approach'])} | {_cell(row['evidence'])} |"
        if value not in result.splitlines():
            result += "\n" + value
    return result + "\n"


def save_claim_bound_decisions(book: Path, unit_id: str, session_id: str,
                               target: str, items: list[dict]) -> int:
    """Use pinned Workflow's audited proposal and compare-and-swap reconciliation."""
    if not items:
        return 0
    if target not in {"glossary", "style_guide"}:
        raise ValueError("invalid literary memory target")
    sys.path.insert(0, str(book.parents[1] / "scripts"))
    from workflow.filesystem import FilesystemStorage
    from workflow.repository import WorkflowStateRepository
    from workflow.proposals import ProposalManager
    repository = WorkflowStateRepository(FilesystemStorage(book))
    manager = ProposalManager(repository)
    name = "glossary.md" if target == "glossary" else "style-guide.md"
    current = (book / name).read_text("utf-8")
    replacement = (updated_glossary(current, items) if target == "glossary"
                   else updated_style(current, items))
    if replacement == current:
        return 0
    proposal = manager.submit(
        unit_id, session_id=session_id, target=target,
        suggestion=json.dumps(items, ensure_ascii=False),
        rationale="Source-grounded literary decisions from the active worker.",
    )
    result = manager.reconcile(
        proposal.proposal["proposal_id"], session_id="automated-orchestrator-" + session_id,
        accept=True, replacement=replacement.encode("utf-8"),
    )
    if result.resolution["status"] != "accepted":
        raise ValueError("canonical literary memory proposal was not accepted: "
                         + result.resolution["status"])
    return len(items)


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
