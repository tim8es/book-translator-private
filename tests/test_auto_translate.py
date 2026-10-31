"""Safety and contract checks for the optional private-only automated runtime."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "automation"))
import book_runner as worker
from omniroute import ModelError, config, parse_review


class AutomatedBookTests(unittest.TestCase):
    def test_strict_review_blocks_unresolved_findings(self):
        payload = {
            "outcome": "PASS",
            "checks": dict.fromkeys(("coverage", "meaning", "terminology", "style", "structure"), True),
            "findings": [{"severity": "major", "detail": "Omission", "resolved": False}],
        }
        with self.assertRaises(ModelError):
            parse_review(json.dumps(payload))
        payload["outcome"] = "CORRECTIONS_REQUIRED"
        outcome, report = parse_review(json.dumps(payload))
        self.assertEqual(outcome, "CORRECTIONS_REQUIRED")
        self.assertEqual(report["context"], "independent_session")

    def test_reviewer_must_complete_all_checks(self):
        payload = {
            "outcome": "PASS",
            "checks": dict.fromkeys(("coverage", "meaning", "terminology", "style", "structure"), True),
            "findings": [],
        }
        payload["checks"]["coverage"] = False
        with self.assertRaises(ModelError):
            parse_review(json.dumps(payload))
        payload["checks"]["coverage"] = True
        self.assertEqual(parse_review(json.dumps(payload))[0], "PASS")

    def test_model_endpoint_requires_https_and_configured_role(self):
        with patch.dict(os.environ, {
            "OMNIROUTE_BASE_URL": "http://example.com/v1",
            "OMNIROUTE_API_KEY": "test-placeholder",
            "OMNIROUTE_TRANSLATOR_MODEL": "test-model",
        }):
            with self.assertRaises(ModelError):
                config("TRANSLATOR")
        with self.assertRaises(ModelError):
            config("UNKNOWN")

    def test_markers_are_order_and_identity_bound(self):
        source = "<!-- bt-block:000001 -->\nFirst [link](#x)\n<!-- bt-block:000002 -->\n"
        worker.check_markers(source, "<!-- bt-block:000001 -->\nПервый [ссылка](#x)\n<!-- bt-block:000002 -->\n")
        with self.assertRaises(worker.JobError):
            worker.check_markers(source, "<!-- bt-block:000002 -->\nПервый [ссылка](#x)\n<!-- bt-block:000001 -->\n")
        with self.assertRaises(worker.JobError):
            worker.check_markers(source, "<!-- bt-block:000001 -->\nПервый [ссылка](#y)\n<!-- bt-block:000002 -->\n")

    def test_intake_hash_bound_and_source_filename_fixed(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(worker, "ROOT", Path(folder)):
                job_id = "a" * 32
                source_dir = worker.job_path(job_id)
                source_dir.mkdir(parents=True)
                source = b"PK\x03\x04test epub bytes"
                (source_dir / "source.epub").write_bytes(source)
                request = {"schema_version": 1, "job_id": job_id,
                           "target_language": "ru",
                           "source_sha256": hashlib.sha256(source).hexdigest(),
                           "public_release_acknowledged": True}
                worker.store_json(source_dir / "request.json", request)
                self.assertEqual(worker.request_for(job_id)["job_id"], job_id)
                self.assertEqual(worker.select(None), job_id)
                request["source_sha256"] = "0" * 64
                worker.store_json(source_dir / "request.json", request)
                with self.assertRaises(worker.JobError):
                    worker.request_for(job_id)

    def test_public_authorization_required_before_source_admission(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(worker, "ROOT", Path(folder)):
                job_id = "a" * 32
                source_dir = worker.job_path(job_id)
                source_dir.mkdir(parents=True)
                source = b"PK\\x03\\x04test"
                (source_dir / "source.epub").write_bytes(source)
                request = {"schema_version": 1, "job_id": job_id,
                           "target_language": "ru",
                           "source_sha256": hashlib.sha256(source).hexdigest()}
                worker.store_json(source_dir / "request.json", request)
                with self.assertRaisesRegex(worker.JobError, "public_release_acknowledged|invalid"):
                    worker.request_for(job_id)
                request["public_release_acknowledged"] = False
                worker.store_json(source_dir / "request.json", request)
                with self.assertRaisesRegex(worker.JobError, "authorization"):
                    worker.request_for(job_id)

    def test_next_step_requires_independent_review(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(worker, "ROOT", Path(folder)):
                slug = "auto-" + "a" * 32
                book = worker.ROOT / "books" / slug
                book.mkdir(parents=True)
                chapter = {
                    "unit_id": "chapter-000001", "number": 1, "status": "translated",
                    "translation_acceptance": {"translation_sha256": "a" * 64}
                }
                worker.store_json(book / "progress.json", {"chapters": [chapter]})
                worker.store_json(book / "review-ledger.json", {"records": []})
                status = {"correction_rounds": {}}
                self.assertEqual(worker.next_operation(slug, status)[0], "reviewer")
                worker.store_json(book / "review-ledger.json", {"records": [{
                    "unit_id": chapter["unit_id"], "sequence": 1, "outcome": "CORRECTIONS_REQUIRED",
                    "translation_sha256": "a" * 64}]})
                self.assertEqual(worker.next_operation(slug, status)[0], "corrector")
                status["correction_rounds"]["chapter-000001"] = worker.MAX_CORRECTIONS
                self.assertEqual(worker.next_operation(slug, status)[0], "blocked")


if __name__ == "__main__":
    unittest.main()
