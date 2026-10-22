"""Read-only real-chapter probe of current Book Translator wave runtime.

Runs exclusively in a temporary filesystem directory. Uses the privately
stored Chapter 11 of Blood and Honey as its real EN/RU fixture. It does not
retranslate or update any book in the repository.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

RUNTIME = Path(os.environ["BOOK_TRANSLATOR_RUNTIME"]).resolve()
sys.path.insert(0, str(RUNTIME / "scripts"))
from workflow.filesystem import FilesystemStorage
from workflow.repository import WorkflowStateRepository
from workflow.reviews import ReviewLedgerManager
from workflow.schemas import SchemaKind
from workflow.session_planner import plan_sessions
from workflow.session_runtime import next_action, save_dispatch, load_dispatch
from workflow.wave_cli import _wave_load_plan, _read_role_routing
from workflow.waves import WaveManager, WaveError
from workflow.literary_memory import context_pack, canonical

PRIVATE_BOOK = Path("books/blood-and-honey-rbmk-caleb-pov").resolve()
UNIT = "chapter-000013"
WAVE_ID = "b" * 32
DISPATCH_ID = "d" * 32
SOURCE_PATH = "extracted/013-chapter-11.md"
TRANSLATION_PATH = "translated/013-chapter-11.md"
SOURCE_REV = "isolated-source-000001"  # synthetic, never written to the real book
ENGINE_REV = os.environ.get("EXPECTED_ENGINE_REVISION", "98a382cdc644ab1a8773f82748e9e4c22d40a871")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class Chapter11WaveProbe(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="book-translator-real-ch11-")
        self.root = Path(self.directory.name)
        for group in ("extracted", "translated"):
            shutil.copytree(PRIVATE_BOOK / group, self.root / group)
        for name in ("metadata.json", "progress.json", "review-ledger.json",
                     "glossary.md", "style-guide.md"):
            shutil.copy2(PRIVATE_BOOK / name, self.root / name)
        self.storage = FilesystemStorage(self.root)
        self.manager = WaveManager(self.storage)
        self.original_source = self.read(SOURCE_PATH)
        self.original_translation = self.read(TRANSLATION_PATH)
        self.legacy_metadata = json.loads(self.read("metadata.json"))
        self.legacy_progress = json.loads(self.read("progress.json"))
        self.legacy_ledger = json.loads(self.read("review-ledger.json"))
        self.unit_progress = next(ch for ch in self.legacy_progress["chapters"]
                                  if ch["number"] == 13)
        self.old_review = next(r for r in self.legacy_ledger["records"]
                               if r["unit_id"] == UNIT and r["outcome"] == "PASS")
        self.source_fingerprint = self.legacy_metadata["source"]["sha256"]
        self.status = {
            "valid": True, "book_slug": self.legacy_progress["book_slug"],
            "workflow_revision": ENGINE_REV, "claims": [],
            "finalization": {"active": False},
            "corpus": {"state": "verified", "source_sha256": self.source_fingerprint},
            "units": [{
                "unit_id": UNIT, "chapter_number": 13,
                "lifecycle": "extracted", "review": "untranslated",
                "source_path": SOURCE_PATH, "translation_path": TRANSLATION_PATH,
            }],
            "state_revisions": {
                key: self.storage.read(path).version for key, path in (
                    ("metadata", "metadata.json"), ("progress", "progress.json"),
                    ("review_ledger", "review-ledger.json"),
                    ("glossary", "glossary.md"), ("style_guide", "style-guide.md"),
                )
            },
        }
        self.fake_wave_metadata = {
            "source": {"revision_id": SOURCE_REV, "sha256": self.source_fingerprint}
        }

    def tearDown(self):
        self.directory.cleanup()

    def read(self, path):
        return (self.root / path).read_bytes()

    def accepted(self):
        self.status["units"][0]["lifecycle"] = "reviewed"
        self.status["units"][0]["review"] = "pass"

    def start(self):
        return self.manager.start(
            self.status, self.fake_wave_metadata, count=1, wave_id=WAVE_ID
        )

    def prepare(self, decisions):
        return self.manager.prepare_close(
            self.status, decisions=decisions,
            read_source=self.read, read_translation=self.read,
            fresh_status=lambda: self.status,
        )

    def close(self):
        return self.manager.close(
            expected_wave=WAVE_ID, fresh_status=lambda: self.status,
            read_source=self.read, read_translation=self.read,
        )

    def test_existing_chapter_and_hash_bound_pass_are_real(self):
        self.assertTrue(self.original_source.startswith(b"## Chapter 11"))
        self.assertTrue(self.original_translation.startswith("## Глава 11".encode()))
        self.assertTrue(len(self.original_source) > 7000)
        self.assertTrue(len(self.original_translation) > 10000)
        self.assertEqual(sha(self.original_source), self.unit_progress["translation_acceptance"]["source_sha256"])
        self.assertEqual(sha(self.original_translation), self.unit_progress["translation_acceptance"]["translation_sha256"])
        self.assertEqual(sha(self.original_source), self.old_review["source_sha256"])
        self.assertEqual(sha(self.original_translation), self.old_review["translation_sha256"])
        self.assertEqual(self.unit_progress["status"], "reviewed")
        resolved = ReviewLedgerManager(
            WorkflowStateRepository(self.storage),
            artifact_reader=self.read,
        ).resolve_unit(self.legacy_progress, self.legacy_metadata, 13)
        self.assertEqual(resolved.state, "pass")
        self.assertEqual(resolved.current_record["record_id"], self.old_review["record_id"])
        print("PASS real chapter 11 source+translation SHA and historical independent PASS")

    def test_wave_dispatch_context_and_real_chapter_publication_guard(self):
        manifest = self.start()
        self.assertEqual(manifest["unit_ids"], [UNIT])
        memory = self.manager.memory()
        self.assertEqual(memory["revision"], manifest["memory_revision"])
        context = context_pack(memory, unit_id=UNIT, source=self.original_source)
        self.assertEqual(context["memory_revision"], manifest["memory_revision"])

        # The fresh worker gets an instruction/asset route, not chapter bytes.
        plan = plan_sessions(
            self.status, sessions=1, source_sizes={UNIT: len(self.original_source)},
            base_commit=ENGINE_REV, dispatch_id=DISPATCH_ID,
        )
        for session in plan["sessions"]:
            session["context"].update({
                "wave_id": WAVE_ID,
                "memory_revision": manifest["memory_revision"],
            })
        save_dispatch(self.storage, plan)
        persisted = load_dispatch(self.storage, DISPATCH_ID)
        sid = persisted["sessions"][0]["session_id"]
        action = next_action(persisted, self.status, sid)
        self.assertEqual(action["action"], "claim")
        route = _wave_load_plan(action, self.status, manifest, _read_role_routing(RUNTIME))
        self.assertEqual(route["role"], "translator")
        self.assertEqual(route["inputs"][0]["path"],
                         f"books/{self.status['book_slug']}/{SOURCE_PATH}")
        self.assertFalse(route["source_content_included"])
        self.assertNotIn(self.original_source[:100].decode(), json.dumps(route))
        self.assertEqual(route["memory"]["revision"], manifest["memory_revision"])

        # Existing accepted translation/independent PASS as baseline, never retranslate.
        self.accepted()
        proposal = {
            "memory_id": "character-caleb-ch11", "kind": "character",
            "subject": "Caleb", "statement": "Caleb is named in this chapter.",
            "translation_decision": None,
            "evidence": {"unit_id": UNIT, "quote": "Caleb"},
            "source_revision_id": SOURCE_REV,
            "status": "accepted", "supersedes": None,
        }
        claim_path = f".workflow/claims/{UNIT}.json"
        self.storage.create_if_absent(claim_path, canonical({
            "unit_id": UNIT, "role": "translator", "session_id": sid,
            "expires_at": (datetime.now(timezone.utc)+timedelta(minutes=30)).isoformat(),
        }))
        self.manager.submit(WAVE_ID, sid, proposal,
                            source=self.original_source, source_revision=SOURCE_REV)
        claim = self.storage.read(claim_path)
        self.storage.delete_if_version(claim_path, claim.version)

        frozen = self.prepare({"character-caleb-ch11": "accepted"})
        self.assertIn("publication_seal", frozen)
        self.assertEqual(frozen["publication_seal"]["reviewed_artifacts"][0]["source_sha256"],
                         sha(self.original_source))
        self.assertEqual(frozen["publication_seal"]["reviewed_artifacts"][0]["translation_sha256"],
                         sha(self.original_translation))

        # P0: mutate a *temporary* translation after prepare; closing must refuse.
        changed = self.original_translation + "\n\n<!-- isolated test only -->\n".encode()
        current = self.storage.read(TRANSLATION_PATH)
        self.storage.write_if_version(TRANSLATION_PATH, changed, current.version)
        with self.assertRaisesRegex(WaveError, "changed since reconciliation"):
            self.close()
        self.assertEqual(self.manager.status(self.status)["state"]["phase"], "RECONCILING")
        self.assertEqual(self.manager.memory()["revision"], manifest["memory_revision"])

        current = self.storage.read(TRANSLATION_PATH)
        self.storage.write_if_version(
            TRANSLATION_PATH, self.original_translation, current.version
        )
        result = self.manager.recover(
            wave_id=WAVE_ID, fresh_status=lambda: self.status,
            read_source=self.read, read_translation=self.read,
        )
        self.assertEqual(result["state"], "CLOSED")
        self.assertIsNone(self.manager.active())
        self.assertEqual(self.manager.memory()["entries"][0]["memory_id"], "character-caleb-ch11")
        self.assertEqual(self.read(TRANSLATION_PATH), self.original_translation)
        print("PASS real chapter 11 wave start/dispatch/context/reconciliation/mutation block/recovery")

    def test_closed_impact_resolution_reopens_after_real_translation_change(self):
        # Historical reviewer resolution is v1. Test the new invalidation rule
        # without creating fabricated v2 review evidence in the real book.
        revision = "f" * 64
        wave = "c" * 32
        impact_path = f".workflow/literary-memory/impacts/{wave}.json"
        memory_id = "character-caleb-ch11"
        self.storage.create_if_absent(impact_path, canonical({
            "schema_version": 1, "wave_id": wave, "memory_revision": revision,
            "candidates": [{"memory_id": memory_id, "unit_id": UNIT,
                            "reason": "candidate_text_match", "matched_terms": ["Caleb"],
                            "state": "pending"}],
        }))
        resolution_path = (
            f".workflow/literary-memory/resolutions/{wave}/{memory_id}-{UNIT}.json"
        )
        self.storage.create_if_absent(resolution_path, canonical({
            "schema_version": 1, "wave_id": wave, "unit_id": UNIT,
            "memory_id": memory_id, "reviewed": True,
            "review_record_id": self.old_review["record_id"],
            "translation_sha256": sha(self.original_translation),
            "memory_revision": revision,
        }))
        self.assertEqual(self.manager.impact_queue(), [])
        current = self.storage.read(TRANSLATION_PATH)
        changed = self.original_translation + b"\nchanged\n"
        self.storage.write_if_version(
            TRANSLATION_PATH, changed, current.version
        )
        # Tampering with the artifact without an authorized acceptance is
        # corrupted state: the repository must fail closed, not return pending.
        with self.assertRaisesRegex(WaveError, "translation_acceptance sha256 mismatch"):
            self.manager.impact_queue()

        # A newly accepted translation invalidates the old PASS/review record.
        # Simulate that transition only in the isolated copy of progress.json.
        original_progress = self.read("progress.json")
        updated_progress = json.loads(original_progress)
        chapter = next(ch for ch in updated_progress["chapters"] if ch["number"] == 13)
        chapter["translation_acceptance"]["translation_sha256"] = sha(changed)
        progress_value = self.storage.read("progress.json")
        self.storage.write_if_version("progress.json", canonical(updated_progress),
                                      progress_value.version)
        pending = self.manager.impact_queue()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["reason"], "previous_resolution_stale")

        restored = self.storage.read(TRANSLATION_PATH)
        self.storage.write_if_version(
            TRANSLATION_PATH, self.original_translation, restored.version
        )
        progress_value = self.storage.read("progress.json")
        self.storage.write_if_version(
            "progress.json", original_progress, progress_value.version
        )
        self.assertEqual(self.manager.impact_queue(), [])
        print("PASS real chapter 11: tampering blocked; accepted change reopens impact")


if __name__ == "__main__":
    unittest.main(verbosity=2)
