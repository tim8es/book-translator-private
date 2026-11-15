"""Ephemeral real-source preserve/extract/audit/build smoke test.

No book text, source bytes or output archive are printed or checked in.
Runs only on the diagnostic PR branch, never merged.
"""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".public-auto-runtime" / "scripts"
sys.path.insert(0, str(ENGINE))
from workflow import epub_preserve

JOB = "05eed6ea814d3b5eec014c6d05b39e3f"
INTAKE = ROOT / "intake" / "auto" / JOB

class RealSourcePreflight(unittest.TestCase):
    def test_original_epub_extract_audit_and_source_build(self):
        source = INTAKE / "source.epub"
        request = json.loads((INTAKE / "request.json").read_text(encoding="utf-8"))
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        self.assertEqual(digest, request["source_sha256"])
        docs, identity = epub_preserve.analyze(source)
        self.assertEqual(identity["source_sha256"], digest)
        chapters = epub_preserve.extract(source, lambda **kwargs: type("Unit", (), kwargs)())
        audit = epub_preserve.audit(source, chapters)
        self.assertEqual(audit["state"], "verified")
        self.assertEqual(audit["source_sha256"], digest)
        self.assertEqual(audit["chapter_count"], len(chapters))
        self.assertGreater(len(chapters), 1)
        assembled = epub_preserve.build(
            source,
            [{"markdown": chapter.content} for chapter in chapters],
            expected_source_sha256=digest,
            language="en",
        )
        self.assertTrue(assembled.startswith(b"PK"))
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
        print("EPUB_END_TO_END_OK " + json.dumps(
            {"source_documents": len(docs), "chapters": len(chapters),
             "covered_documents": len(audit["documents"]),
             "mode": epub_preserve.MODE}, sort_keys=True))

if __name__ == "__main__":
    unittest.main()
