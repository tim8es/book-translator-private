from pathlib import Path
from html import escape
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from xml.etree import ElementTree as ET
import re
import hashlib

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent.parent
OLD = BOOK / "output/You_Feel_Like_Home_RU_chapters_1-9.epub"
NEW = BOOK / "output/You_Feel_Like_Home_RU_chapters_1-10.epub"
SECTION = "OEBPS/section-09b.xhtml"
OPF = "OEBPS/content.opf"
NAV = "OEBPS/nav.xhtml"
NCX = "OEBPS/toc.ncx"
PARTS = [
    "012-chapter-10-part-01.md",
    "012-chapter-10-part-02.md",
    "012-chapter-10-part-03.md",
    "012-chapter-10-part-04a.md",
    "012-chapter-10-part-04b1.md",
    "012-chapter-10-part-04b2a.md",
    "012-chapter-10-part-04b2b.md",
    "012-chapter-10-part-05.md",
    "012-chapter-10-part-06.md",
    "012-chapter-10-part-07.md",
]

def inline(s):
    s = escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", s)

def chapter(md):
    items = []
    for block in re.split(r"\n\s*\n", md.strip()):
        p = block.strip()
        if p == "++++":
            items.append('<p class="scene-break">++++</p>')
        elif p.startswith("## "):
            items.append("<h3>" + inline(p[3:]) + "</h3>")
        elif p.startswith("# "):
            items.append("<h2>" + inline(p[2:]) + "</h2>")
        else:
            items.append("<p>" + inline(p).replace("\n", "<br/>") + "</p>")
    s = (
        '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru">'
        '<head><title>Глава 10</title><link rel="stylesheet" href="styles.css" type="text/css"/></head>'
        '<body>' + "\n".join(items) + "</body></html>"
    )
    ET.fromstring(s.encode("utf-8"))
    return s.encode("utf-8")

def update_opf(data):
    ns = "http://www.idpf.org/2007/opf"
    root = ET.fromstring(data)
    manifest = root.find("{" + ns + "}manifest")
    spine = root.find("{" + ns + "}spine")
    assert manifest is not None and spine is not None
    assert not any(x.get("href") == "section-09b.xhtml" for x in manifest)
    manifest.append(ET.Element("{" + ns + "}item", {
        "id": "ru10", "href": "section-09b.xhtml", "media-type": "application/xhtml+xml"
    }))
    refs = spine.findall("{" + ns + "}itemref")
    assert refs[-2].get("idref") == "ru9", [x.get("idref") for x in refs]
    spine.insert(list(spine).index(refs[-1]), ET.Element("{" + ns + "}itemref", {"idref": "ru10"}))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def update_nav(data):
    ns = "http://www.w3.org/1999/xhtml"
    root = ET.fromstring(data)
    navs = root.findall(".//{" + ns + "}nav")
    assert navs
    nav = next((n for n in navs if n.get("{http://www.idpf.org/2007/ops}type") == "toc"), navs[0])
    ol = nav.find("{" + ns + "}ol")
    assert ol is not None and len(ol) >= 10
    li = ET.Element("{" + ns + "}li")
    ET.SubElement(li, "{" + ns + "}a", {"href": "section-09b.xhtml"}).text = "Глава 10"
    ol.insert(len(ol) - 1, li)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def update_ncx(data):
    ns = "http://www.daisy.org/z3986/2005/ncx/"
    root = ET.fromstring(data)
    nav = root.find("{" + ns + "}navMap")
    assert nav is not None
    points = nav.findall("{" + ns + "}navPoint")
    assert len(points) >= 10
    point = ET.Element("{" + ns + "}navPoint", {"id": "ru-chapter-10", "playOrder": "1"})
    label = ET.SubElement(point, "{" + ns + "}navLabel")
    ET.SubElement(label, "{" + ns + "}text").text = "Глава 10"
    ET.SubElement(point, "{" + ns + "}content", {"src": "section-09b.xhtml"})
    nav.insert(list(nav).index(points[-1]), point)
    for i, item in enumerate(root.iter("{" + ns + "}navPoint"), 1):
        item.set("playOrder", str(i))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def main():
    texts = [(ROOT / "translated" / name).read_text("utf-8").strip() for name in PARTS]
    md = "\n\n".join(texts) + "\n"
    assert md.startswith("## Глава 10")
    assert md.count("++++") == 2
    assert "Примечания автора к главе" in md and md.rstrip().endswith("❤️")
    assert len(md) > 33000, len(md)
    xhtml = chapter(md)
    assert len(xhtml) > 40000, len(xhtml)
    with ZipFile(OLD) as old:
        assert old.testzip() is None
        for name in ["mimetype", OPF, NAV, NCX, "OEBPS/section-09a.xhtml", "OEBPS/section-10.xhtml"]:
            assert name in old.namelist(), name
        assert SECTION not in old.namelist()
        mods = {
            OPF: update_opf(old.read(OPF)),
            NAV: update_nav(old.read(NAV)),
            NCX: update_ncx(old.read(NCX)),
        }
        front = old.read("OEBPS/section-01.xhtml")
        mods["OEBPS/section-01.xhtml"] = front.replace("Глав: 9/?".encode(), "Глав: 10/?".encode())
        NEW.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(NEW, "w") as output:
            output.writestr("mimetype", old.read("mimetype"), compress_type=ZIP_STORED)
            for info in old.infolist():
                if info.filename == "mimetype":
                    continue
                if info.filename == "OEBPS/section-10.xhtml":
                    output.writestr(SECTION, xhtml, compress_type=ZIP_DEFLATED)
                output.writestr(info, mods.get(info.filename, old.read(info.filename)))
    with ZipFile(NEW) as z:
        assert z.testzip() is None
        assert z.infolist()[0].filename == "mimetype"
        assert z.infolist()[0].compress_type == ZIP_STORED
        assert z.read("mimetype") == b"application/epub+zip"
        assert z.read(SECTION) == xhtml
        for n in [OPF, NAV, NCX, SECTION]:
            ET.fromstring(z.read(n))
        opf = ET.fromstring(z.read(OPF))
        ns = "http://www.idpf.org/2007/opf"
        manifest = {x.get("id"): x.get("href") for x in opf.findall("./{" + ns + "}manifest/{" + ns + "}item")}
        spine = [x.get("idref") for x in opf.findall("./{" + ns + "}spine/{" + ns + "}itemref")]
        assert spine[-3:] == ["ru9", "ru10", spine[-1]], spine
        assert manifest["ru10"] == "section-09b.xhtml"
        assert z.read("OEBPS/section-09a.xhtml") == old_ch9
    print("EPUB:", NEW)
    print("SIZE:", NEW.stat().st_size)
    print("SHA256:", hashlib.sha256(NEW.read_bytes()).hexdigest())
    print("CH10_TRANSLATION_CHARS:", len(md))
    print("CH10_PARTS:", len(PARTS))

if __name__ == "__main__":
    with ZipFile(OLD) as z:
        old_ch9 = z.read("OEBPS/section-09a.xhtml")
    main()
