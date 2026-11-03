"""Diagnostic-only regression probe: report EPUB markup shape, NEVER prose."""
from __future__ import annotations

import posixpath
import unittest
import zipfile
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree as ET


def local(tag):
    return str(tag).rsplit("}", 1)[-1]


class SourceNavShapeProbe(unittest.TestCase):
    def test_lantern_epub_navigation_markup_shape_only(self):
        source = Path("intake/auto/b125af5f128e151b1d9b5c39fddb2a35/source.epub")
        self.assertTrue(source.is_file())
        with zipfile.ZipFile(source) as z:
            container = ET.fromstring(z.read("META-INF/container.xml"))
            rf = next(x for x in container.iter() if local(x.tag) == "rootfile")
            opf_name = rf.get("full-path")
            package = ET.fromstring(z.read(opf_name))
            opf_dir = posixpath.dirname(opf_name)
            items = {
                x.get("id"): (posixpath.normpath(posixpath.join(
                    opf_dir, unquote(x.get("href", "")))), x.get("properties", ""),
                    x.get("media-type", ""))
                for x in package.iter() if local(x.tag) == "item"}
            spine = [x.get("idref") for x in package.iter() if local(x.tag) == "itemref"]
            print("SOURCE_NAV_PROBE: spine_count=",len(spine),"manifest_items=",len(items), flush=True)
            navs = 0
            for item_id, (path, props, media) in items.items():
                if media != "application/xhtml+xml" or path not in z.namelist():
                    continue
                root = ET.fromstring(z.read(path))
                body = next((x for x in root.iter() if local(x.tag) == "body"), None)
                if body is None:
                    continue
                for nav in (x for x in body.iter() if local(x.tag) == "nav"):
                    navs += 1
                    nodes = list(nav.iter())
                    links = [x for x in nodes if local(x.tag) == "a"]
                    # No prose, navigation labels, href contents, source text, or filenames.
                    parents = []
                    def walk(n, path_parts):
                        if n is nav:
                            parents.append(tuple(path_parts))
                            return
                        for ch in n:
                            walk(ch, path_parts+[local(ch.tag)])
                    walk(body, ["body"])
                    kinds = {local(x.tag): sum(local(y.tag) == local(x.tag) for y in nodes) for x in nodes}
                    nav_type = [v for k,v in nav.attrib.items() if local(k) == "type"]
                    text_metrics = {
                       "direct_text_chars": len((nav.text or "").strip()),
                       "direct_tails_chars": sum(len((x.tail or "").strip()) for x in nodes),
                       "text_chars_total": len("".join(nav.itertext()).strip())
                    }
                    print("SOURCE_NAV_PROBE:", {
                        "spine_item": item_id in spine,
                        "opf_nav_property": "nav" in props.split(),
                        "ancestor_tags": parents,
                        "nav_type": nav_type,
                        "tag_counts": kinds,
                        "link_count":len(links),
                        "external_links":sum((x.get("href") or "").startswith(("https:","http:","mailto:")) for x in links),
                        "local_links":sum(bool(x.get("href")) and not (x.get("href") or "").startswith(("https:","http:","mailto:")) for x in links),
                        "metrics": text_metrics,
                    },flush=True)
            print("SOURCE_NAV_PROBE: total_nav_elements=",navs,flush=True)
            self.assertGreater(navs,0)


if __name__ == "__main__":
    unittest.main()
