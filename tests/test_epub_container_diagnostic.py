"""Temporary non-content diagnostic for unsupported EPUB container shapes."""
import json
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

SOURCE = (Path(__file__).resolve().parents[1] / "intake" / "auto" /
          "05eed6ea814d3b5eec014c6d05b39e3f" / "source.epub")
PROSE = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "dt", "dd", "blockquote", "pre"}


def tag(node):
    return node.tag.rsplit("}", 1)[-1] if isinstance(node.tag, str) else "#other"


class ShapeDiagnostic(unittest.TestCase):
    def test_container_shape_without_prose(self):
        with zipfile.ZipFile(SOURCE) as zf:
            names = [n for n in zf.namelist()
                     if n.endswith("say_it_in_your_mother_split_001.xhtml")]
            self.assertTrue(names, "target XHTML not found")
            for path in names:
                root = ET.fromstring(zf.read(path))
                parent = {child: node for node in root.iter() for child in node}
                cases = []
                for node in root.iter():
                    if tag(node) != "div":
                        continue
                    direct = len((node.text or "").strip())
                    tails = [(tag(ch), len((ch.tail or "").strip()))
                             for ch in node if (ch.tail or "").strip()]
                    descendant_prose = sum(tag(ch) in PROSE for ch in node.iter() if ch is not node)
                    if not (direct or tails or descendant_prose):
                        continue
                    lineage = []
                    cur = node
                    while cur is not None and len(lineage) < 6:
                        lineage.append(tag(cur))
                        cur = parent.get(cur)
                    cases.append({
                        "ancestry": "/".join(reversed(lineage)),
                        "attribute_keys": sorted(node.attrib),
                        "direct_text_length": direct,
                        "children": [tag(ch) for ch in node][:20],
                        "child_attribute_keys": [sorted(ch.attrib) for ch in node][:20],
                        "tail_lengths": tails[:12],
                        "descendant_prose": descendant_prose,
                    })
                print("EPUB_STRUCTURE_ONLY " + json.dumps(
                    {"source_member": path, "candidate_count": len(cases),
                     "candidates": cases[:25]}, ensure_ascii=False))
