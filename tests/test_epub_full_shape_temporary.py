"""One-off structural EPUB preflight: no book words or rendered XHTML in logs."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET
import zipfile

JOB = "05eed6ea814d3b5eec014c6d05b39e3f"
EPUB = Path(__file__).resolve().parents[1]/"intake"/"auto"/JOB/"source.epub"
ALLOWED = set("html head title meta link style body section div span p h1 h2 h3 h4 h5 h6 a em i b strong big br hr img svg image ul ol li dl dt dd blockquote pre wbr".split())
PROSE = set("p h1 h2 h3 h4 h5 h6 li dt dd blockquote pre".split())

def name(n):
    return n.tag.rsplit("}",1)[-1] if isinstance(n.tag,str) else "comment"

class AllEpubShapes(unittest.TestCase):
    def test_all_spine_xhtml_shapelist(self):
        with zipfile.ZipFile(EPUB) as z:
            files=[p for p in z.namelist() if p.lower().endswith((".xhtml",".html"))]
            counts=Counter()
            per_tag=defaultdict(list)
            anomalies=defaultdict(list)
            all_nodes=0
            for f in files:
                root=ET.fromstring(z.read(f))
                parent={child:n for n in root.iter() for child in n}
                body=next((n for n in root.iter() if name(n)=="body"),None)
                if body is None: continue
                for n in body.iter():
                    t=name(n); counts[t]+=1; all_nodes+=1
                    if t in ALLOWED and t not in {"big"}: continue
                    p=parent.get(n)
                    x = {
                        "file":f.rsplit("/",1)[-1],
                        "tag":t,
                        "parent":name(p) if p is not None else None,
                        "parent_text_len":len((p.text or "").strip()) if p is not None else 0,
                        "preceding_tail_len":len((n.tail or "").strip()),
                        "child_tags":[name(x) for x in list(n)][:12],
                        "attr_keys":sorted(n.attrib),
                        "text_len":len((n.text or "").strip()),
                        "subtree_text_len":len("".join(n.itertext()).strip()),
                        "sibling_count":len(list(p)) if p is not None else 0,
                        "child_position":list(p).index(n) if p is not None else 0,
                        "ancestor_tags":[name(parent.get(p)) if p is not None and parent.get(p) is not None else None],
                    }
                    per_tag[t].append(x)
                # Inspect every image's placement without printing its source or alt.
                for n in body.iter():
                    if name(n) != "img": continue
                    p = parent.get(n)
                    ancestor = p
                    enclosing = None
                    while ancestor is not None:
                        if name(ancestor) in PROSE:
                            enclosing = ancestor
                            break
                        ancestor = parent.get(ancestor)
                    anomalies["image_shapes"].append({
                        "file": f.rsplit("/", 1)[-1],
                        "parent_tag": name(p) if p is not None else None,
                        "parent_direct_text_len": len((p.text or "").strip()) if p is not None else 0,
                        "parent_child_tags": [name(x) for x in p][:12] if p is not None else [],
                        "parent_tail_lengths": [len((x.tail or "").strip()) for x in p][:12] if p is not None else [],
                        "enclosing_prose": name(enclosing) if enclosing is not None else None,
                        "enclosing_prose_text_len": len("".join(enclosing.itertext()).strip()) if enclosing is not None else 0,
                        "attributes": sorted(n.attrib),
                        "has_caption": bool(n.get("alt", "").strip()),
                    })
                # other risks to map proactively: containers with direct text and descendant prose
                for n in body.iter():
                    if name(n) not in {"div","blockquote","li","p"}: continue
                    descendants=[x for x in n.iter() if x is not n]
                    if any(name(x) in PROSE for x in descendants) and (
                        (n.text or "").strip() or any((x.tail or "").strip() for x in n)
                    ):
                        anomalies["nested_direct_text"].append({
                           "file": f.rsplit("/",1)[-1],"tag":name(n),"direct_chars":len((n.text or "").strip()),
                           "tail_children":[name(x) for x in n if (x.tail or "").strip()][:5],
                           "child_tags":[name(x) for x in n][:12]})
            result={
                "xhtml_count":len(files), "node_count":all_nodes,
                "tags":dict(counts.most_common()), "unsupported_summary":{
                   k:{"count":len(v),"examples":v[:18]} for k,v in per_tag.items()
                },
                "anomalies":{k:{"count":len(v),"examples":v[:15]} for k,v in anomalies.items()}
            }
            print("EPUB_INVENTORY_JSON="+json.dumps(result,ensure_ascii=False,separators=(",",":")))
            self.assertGreater(len(files),0)
