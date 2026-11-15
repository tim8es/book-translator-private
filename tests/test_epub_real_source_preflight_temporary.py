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
        # Compare source text independently, logging only counts/tag shapes.
        from collections import Counter
        from xml.etree import ElementTree as ET
        with __import__("zipfile").ZipFile(source) as zf:
            mismatches = []
            for doc, chapter in zip((d for d in docs if d.kind == "text"), chapters):
                parts = epub_preserve.parse_blocks(
                    chapter.content, expected=len(doc.blocks), allow_source_escapes=True)
                if any(epub_preserve._tokens(x) != epub_preserve._tokens(y)
                       for x,y in zip(doc.blocks,parts)):
                    root = ET.fromstring(zf.read(doc.path))
                    nodes = epub_preserve._blocks(root)
                    for idx,(original,extracted) in enumerate(zip(doc.blocks,parts),1):
                        if epub_preserve._tokens(original) == epub_preserve._tokens(extracted):
                            continue
                        node=nodes[idx-1][0]
                        tags=Counter(epub_preserve._local(n.tag) for n in node.iter())
                        mismatches.append({
                            "file":Path(doc.path).name,
                            "block":idx,
                            "source_chars":len(original),
                            "extracted_chars":len(extracted),
                            "source_tokens":len(epub_preserve._tokens(original)),
                            "extracted_tokens":len(epub_preserve._tokens(extracted)),
                            "tag_counts":dict(tags),
                            "has_nested_emphasis":any(
                                epub_preserve._local(x.tag) in {"strong","b"} and
                                any(epub_preserve._local(z.tag) in {"em","i"}
                                    for z in x.iter() if z is not x)
                                for x in node.iter()),
                            "has_nested_bold":any(
                                epub_preserve._local(x.tag) in {"em","i"} and
                                any(epub_preserve._local(z.tag) in {"strong","b"}
                                    for z in x.iter() if z is not x)
                                for x in node.iter()),
                        })
            print("EPUB_AUDIT_MISMATCH_SHAPES="+json.dumps({
                "count":len(mismatches),"sample":mismatches[:25]}, ensure_ascii=False))
        audit = epub_preserve.audit(source, chapters)
        self.assertEqual(audit["state"], "verified")
        self.assertEqual(audit["source_sha256"], digest)
        self.assertEqual(audit["chapter_count"], len(chapters))
        self.assertGreater(len(chapters), 1)
        # Preflight renderer ambiguity without disclosing source words.
        with __import__("zipfile").ZipFile(source) as archive:
            _, drop_classes = epub_preserve._source_style_classes(archive)
            collisions = []
            for doc in docs:
                if doc.kind != "text": continue
                root = ET.fromstring(archive.read(doc.path))
                for index, (node, _) in enumerate(epub_preserve._blocks(root), 1):
                    children = list(node)
                    initial = ("".join(children[0].itertext()) if children
                               and epub_preserve._local(children[0].tag) == "span" else "")
                    drop = bool(children and initial and not list(children[0])
                                and set(children[0].get("class", "").split()) & drop_classes
                                and (len(initial) == 1 and initial.isalpha()
                                     or len(initial) == 2 and initial[1].isalpha()))
                    links = [p for p in node.iter() if epub_preserve._local(p.tag) == "a"]
                    styles, media, _ = epub_preserve._inline_structure(node)
                    if (styles or media) and (links or drop):
                        collisions.append({
                            "file":Path(doc.path).name,
                            "index":index,
                            "link_count":len(links),
                            "styled_count":len(styles),
                            "media_count":len(media),
                            "drop_cap":drop,
                            "tags":[epub_preserve._local(p.tag) for p in node.iter()][:18],
                        })
            print("EPUB_BUILD_COLLISIONS="+json.dumps({
                "count":len(collisions),"sample":collisions[:40]},ensure_ascii=False))
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
