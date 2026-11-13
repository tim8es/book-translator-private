"""Durable provider outages, safe unit isolation and optional failover."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "automation"))
import book_runner as worker
from omniroute import (
    ModelError, TransientModelError, complete, config,
)


class ProviderRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.chapter = {"number": 1, "unit_id": "chapter-000001",
                        "status": "extracted"}
        self.status = {"state": "running", "failures": 1,
                       "active": {"role": "translator", "chapter": 1,
                                  "session_id": "test"}}
        self.env = {
            "OMNIROUTE_BASE_URL": "https://model.example/v1",
            "OMNIROUTE_API_KEY": "test-token",
            "OMNIROUTE_TRANSLATOR_MODEL": "test-primary",
            "OMNIROUTE_TRANSLATOR_FALLBACK_MODEL": "test-backup",
        }

    def test_http_429_is_one_classified_request_with_retry_after(self):
        error = HTTPError("https://model.example/v1/chat/completions",
                          429, "Too Many Requests",
                          {"Retry-After": "150"}, None)
        with patch.dict(os.environ, self.env), \
             patch("omniroute.urlopen", side_effect=error) as post:
            with self.assertRaises(TransientModelError) as ctx:
                complete("TRANSLATOR", "system", "source")
        post.assert_called_once()
        self.assertEqual(ctx.exception.code, "http_429")
        self.assertEqual(ctx.exception.retry_after_seconds, 150)
        self.assertNotIn("test-token", str(ctx.exception))

    def test_nontransient_http_error_cannot_be_scheduled(self):
        error = HTTPError("https://model.example/v1/chat/completions",
                          404, "Not Found", {}, None)
        with patch.dict(os.environ, self.env), \
             patch("omniroute.urlopen", side_effect=error) as post:
            with self.assertRaisesRegex(ModelError, "404") as ctx:
                complete("TRANSLATOR", "system", "source")
        self.assertNotIsInstance(ctx.exception, TransientModelError)
        post.assert_called_once()

    def test_network_failure_is_transient_but_bad_payload_is_not(self):
        with patch.dict(os.environ, self.env), \
             patch("omniroute.urlopen", side_effect=URLError("timeout")) as post:
            with self.assertRaises(TransientModelError) as ctx:
                complete("TRANSLATOR", "system", "source")
        post.assert_called_once()
        self.assertEqual(ctx.exception.code, "transport")
        self.assertIsNone(worker.translator_model_output_code(ctx.exception))

    def test_retry_deadline_is_persisted_and_exponentially_bounded(self):
        first = TransientModelError("model HTTP status 429", code="http_429",
                                    retry_after_seconds=300)
        worker.schedule_provider_retry(self.status, self.chapter, "translator", first)
        one = self.status["provider_retry"]
        self.assertEqual(one["attempts"], 1)
        self.assertEqual(one["code"], "http_429")
        self.assertFalse(worker.provider_retry_due(self.status))
        self.assertGreaterEqual(
            (datetime.fromisoformat(one["not_before"]) -
             datetime.now(timezone.utc)).total_seconds(), 290)
        second = TransientModelError("model HTTP status 503", code="http_503")
        worker.schedule_provider_retry(self.status, self.chapter, "translator", second)
        self.assertEqual(self.status["provider_retry"]["attempts"], 2)
        self.assertEqual(self.status["phase"], "provider-backoff")
        self.assertEqual(self.status["state"], "running")
        self.assertEqual(self.status["failures"], 1)
        self.assertTrue(worker.provider_retry_due({
            "provider_retry": {**self.status["provider_retry"],
                               "not_before": (datetime.now(timezone.utc)
                               - timedelta(minutes=1)).isoformat()}
        }))
        for _ in range(15):
            worker.schedule_provider_retry(
                self.status, self.chapter, "translator", second)
        deadline = datetime.fromisoformat(self.status["provider_retry"]["not_before"])
        self.assertLessEqual(
            (deadline - datetime.now(timezone.utc)).total_seconds(),
            worker.MAX_BACKOFF_SECONDS + 2)

    def test_corrupted_checkpoint_blocks_no_external_requests(self):
        self.status["provider_retry"] = {"not_before": "invalid"}
        with self.assertRaisesRegex(worker.JobError, "invalid provider retry checkpoint"):
            worker.provider_retry_due(self.status)

    def test_fallback_uses_only_configured_variable_and_current_unit(self):
        worker.schedule_provider_retry(
            self.status, self.chapter, "translator",
            TransientModelError("timeout", code="transport"))
        worker.schedule_provider_retry(
            self.status, self.chapter, "translator",
            TransientModelError("timeout", code="transport"))
        with patch.dict(os.environ, self.env), \
             patch.object(worker, "complete", return_value="{}") as post:
            self.assertEqual(worker.complete_for_job(
                self.status, "TRANSLATOR", "system", "source"), "{}")
        post.assert_called_once_with("TRANSLATOR_FALLBACK", "system", "source")
        self.assertEqual(self.status["provider_model_route"], "fallback")
        with patch.dict(os.environ, {**self.env,
                                     "OMNIROUTE_TRANSLATOR_FALLBACK_MODEL": ""}), \
             patch.object(worker, "complete", return_value="{}") as post:
            worker.complete_for_job(self.status, "TRANSLATOR", "system", "source")
        post.assert_called_once_with("TRANSLATOR", "system", "source")
        with patch.dict(os.environ, self.env), \
             patch.object(worker, "complete", return_value="{}") as post:
            self.status["active"]["chapter"] = 2
            worker.complete_for_job(self.status, "TRANSLATOR", "system", "source")
        post.assert_called_once_with("TRANSLATOR", "system", "source")
        with patch.dict(os.environ, self.env):
            self.assertEqual(config("TRANSLATOR_FALLBACK")[2], "test-backup")


    def test_repeated_same_unit_protocol_failures_select_backup(self):
        self.status["active"]["unit_id"] = self.chapter["unit_id"]
        self.status["unit_protocol_failures"] = {self.chapter["unit_id"]: 2}
        with patch.dict(os.environ, self.env), \
             patch.object(worker, "complete", return_value="{}") as post:
            worker.complete_for_job(self.status, "TRANSLATOR", "system", "text")
        post.assert_called_once_with("TRANSLATOR_FALLBACK", "system", "text")
        # Never use another unit's failed attempts to select its model.
        self.status["active"]["unit_id"] = "chapter-000002"
        with patch.dict(os.environ, self.env), \
             patch.object(worker, "complete", return_value="{}") as post:
            worker.complete_for_job(self.status, "TRANSLATOR", "system", "text")
        post.assert_called_once_with("TRANSLATOR", "system", "text")

    def test_translator_output_allowlist_excludes_transport_and_unknown(self):
        for message, expected in (
            ("translator must return a structured JSON response", "invalid_translator_output"),
            ("pre-acceptance coverage gate detected probable missing source text",
             "translation_coverage"),
            ("model transport timeout or connection failure", None),
            ("source changed during structural translation", None),
            ("model HTTP status 404", None),
        ):
            self.assertEqual(worker.translator_model_output_code(
                ModelError(message)), expected)

    def test_translation_deferral_requires_canonical_supported_contract(self):
        self.status["failures"] = worker.MAX_FAILURES
        with patch.object(worker, "canonical_translation_deferral_supported",
                          return_value=True), \
             patch.object(worker, "cli", return_value="ok") as cli:
            self.assertTrue(worker.defer_untranslated_unit(
                "synthetic-book", self.chapter,
                self.status, "translation_coverage"))
        cli.assert_called_once_with(
            "defer-translation", "synthetic-book", "1", "--reason",
            "model-coverage-exhausted")
        self.assertEqual(self.status["state"], "running")
        self.assertEqual(self.status["phase"], "model-unit-deferred")
        self.assertNotIn("PASS", repr(self.status))
        with patch.object(worker, "canonical_translation_deferral_supported",
                          return_value=False), \
             patch.object(worker, "cli") as cli:
            self.assertFalse(worker.defer_untranslated_unit(
                "synthetic-book", self.chapter,
                {**self.status, "failures": 3}, "invalid_translator_output"))
            cli.assert_not_called()

    def test_provider_backoff_has_no_immediate_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            with patch.dict(os.environ, {"GITHUB_OUTPUT": str(output)}):
                worker.publish_outputs(
                    "b" * 32, {"state": "running", "phase": "provider-backoff"})
            self.assertIn("continue_queue=true", output.read_text("utf-8"))
            self.assertNotIn("continue=true", output.read_text("utf-8"))


if __name__ == "__main__":
    unittest.main()
