#!/usr/bin/env python3
"""Book-specific native-layout EPUB projection; does not mutate the literary corpus.

Preserves the exact original OPF/NCX/CSS/fonts/images/fragment IDs where possible.
Only XHTML visible text, TOC labels and target-language metadata are localized.
Fails closed if current translation/review hashes, ordering, links or text drift.
"""
import copy
import hashlib
import json
import math
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

X = "http://www.w3.org/1999/xhtml"
DC = "http://purl.org/dc/elements/1.1/"
XML = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", X)
ET.register_namespace("epub", "http://www.idpf.org/2007/ops")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
ET.register_namespace("svg", "http://www.w3.org/2000/svg")
PREFIX = "{"+X+"}"
BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from workflow.epub_output import render_markdown_xhtml  # exact pinned workflow
SLUG = "obsession-eva-marks"
SHA = lambda data: hashlib.sha256(data).hexdigest()

def need(value, reason):
    if not value:
        raise RuntimeError(reason)

def local(el):
    return el.tag.split("}")[-1].lower()

def inner(el):
    return "".join(el.itertext()).strip()

def markdown_document(text, title):
    root = ET.fromstring(render_markdown_xhtml(title, text, language="ru"))
    body = root.find(PREFIX+"body")
    need(body is not None, "Markdown has no XHTML body")
    return list(body)

def split_src(source, source_p):
    if not source_p:
        return []
    source_lengths = [max(1,len(inner(p))) for p in source_p]
    tr_lengths = [max(1,len(inner(p))) for p in source]
    m,n=len(source_lengths),len(tr_lengths)
    need(n>=m, "Unmapped source paragraphs: translation has fewer paragraphs")
    extra=n-m
    ratio=max(.1,sum(tr_lengths)/max(1,sum(source_lengths)))
    # Match adjacent translation blocks to original styled paragraphs, minimizing
    # relative length drift; extra blocks are inserted after their source anchor.
    dp={(0,0):(0.0,[])}
    for i in range(m):
        nd={}
        for (old_i,j),(cost,groups) in dp.items():
            if old_i!=i:continue
            maxk=min(extra+1, n-j-(m-i-1))
            for k in range(1,maxk+1):
                size=sum(tr_lengths[j:j+k])
                expected=source_lengths[i]*ratio
                delta=math.log((size+4)/(expected+4))
                c=cost+delta*delta+(k-1)*.12
                slot=(i+1,j+k)
                if slot not in nd or c<nd[slot][0]:
                    nd[slot]=(c, groups+[source[j:j+k]])
        dp=nd
    need((m,n) in dp, f"Unable to align paragraph counts {m}/{n}")
    return dp[(m,n)][1]

def transfer_text(target, localized):
    # Keep native block tag, id/class/style and its surrounding layout wrappers.
    old_ids = [x.attrib["id"] for x in target.iter() if x is not target and "id" in x.attrib]
    drop = next((child for child in target.iter()
                 if child is not target and "dropcap" in child.attrib.get("class","").split()), None)
    target.text = localized.text
    for child in list(target):
        target.remove(child)
    for child in list(localized):
        target.append(copy.deepcopy(child))
    if drop is not None and target.text and target.text[0].isalpha():
        first=target.text[0]
        tail=target.text[1:]
        replica=ET.Element(PREFIX+"span", {"class":drop.attrib.get("class","dropcap")})
        replica.text=first
        replica.tail=tail
        target.insert(0,replica)
        target.text=None
    used={e.attrib.get("id") for e in target.iter() if e.attrib.get("id")}
    for id_ in old_ids:
        if id_ not in used:
            span=ET.Element(PREFIX+"span",{"id":id_})
            target.insert(0, span)

def add_linkified_plain_text(elem):
    """Turn raw URL/email text from translated Markdown into working HTML anchors."""
    rx=re.compile(r'(?<![\w/])(?:https?://[^\s<>]+|(?:[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}))')
    def attach(parent, child, text, is_tail):
        matches=list(rx.finditer(text))
        if not matches:return
        pieces=[]
        last=0
        for match in matches:
            url=match.group(0).rstrip('.,;:)')
            end=match.start()+len(url)
            if end<=match.start():continue
            pieces.append((text[last:match.start()],url))
            last=end
        if not pieces:return
        trailing=text[last:]
        pos=list(parent).index(child)+1 if is_tail else 0
        prior=child if is_tail else None
        for plain,url in pieces:
            if prior is None:parent.text=plain
            else:prior.tail=plain
            target=url if url.startswith("http") else "mailto:"+url
            el=ET.Element(PREFIX+"a",{"href":target})
            el.text=url
            parent.insert(pos,el)
            pos+=1
            prior=el
        if prior is not None:prior.tail=trailing
    def recurse(node):
        if local(node)=="a":return
        kids=list(node)
        if node.text:attach(node,None,node.text,False)
        for child in kids:
            recurse(child)
            if child.tail: attach(node,child,child.tail,True)
    recurse(elem)

def canonical_title(markdown_blocks):
    for node in markdown_blocks:
        if local(node).startswith("h"):return inner(node)
    for node in markdown_blocks:
        if local(node)=="p":
            text=inner(node)
            if "OceanofPDF" not in text and len(text)<100:
                return text
    return None

def copy_epub(z, replacements, target):
    with zipfile.ZipFile(target,"w") as out:
        # The original container may be accepted by readers but fail EPUB ZIP
        # rules. Normalize ONLY the mandated first, uncompressed mimetype entry.
        info=zipfile.ZipInfo("mimetype",date_time=(1980,1,1,0,0,0))
        info.compress_type=zipfile.ZIP_STORED
        out.writestr(info,b"application/epub+zip")
        for old in z.infolist():
            if old.filename=="mimetype":continue
            payload = replacements.get(old.filename)
            if payload is None:payload=z.read(old.filename)
            out.writestr(old,payload)

def build():
    meta=json.loads((BASE/"metadata.json").read_text("utf8"))
    progress=json.loads((BASE/"progress.json").read_text("utf8"))
    manifest=json.loads((BASE/"source-manifest.json").read_text("utf8"))
    cov=json.loads((BASE/"source-coverage.json").read_text("utf8"))
    ledger=json.loads((BASE/"review-ledger.json").read_text("utf8"))
    need(meta["workflow"]["resolved_revision"]=="8f70b1c1c108926599c36ce40021860bed581400","Incorrect engine revision")
    need(cov["state"]=="verified" and cov["chapter_count"]==48 and manifest["chapter_count"]==48,"Source coverage is not verified")
    source=BASE/"source/Obsession_Eva_Marks.epub"
    need(SHA(source.read_bytes())==meta["source"]["sha256"]==manifest["source_sha256"]==cov["source_sha256"],"Source edition is not original sealed EPUB")
    chapters=progress["chapters"]
    need(len(chapters)==48 and all(x["status"]=="reviewed" for x in chapters),"Not all units reviewed")
    latest={}
    for record in ledger["records"]:latest[record["unit_id"]]=record
    rendered={}
    texts={}
    for unit in chapters:
        source_data=(BASE/unit["source_path"]).read_bytes()
        translated_data=(BASE/unit["translation_path"]).read_bytes()
        a=unit["translation_acceptance"]
        l=latest.get(unit["unit_id"])
        need(a and l and l["outcome"]=="PASS",f"No current PASS: {unit['number']}")
        need(a["source_sha256"]==SHA(source_data)==l["source_sha256"],f"Source SHA mismatch: {unit['number']}")
        need(a["translation_sha256"]==SHA(translated_data)==l["translation_sha256"],f"Translation SHA mismatch: {unit['number']}")
        txt=translated_data.decode("utf-8")
        texts[unit["number"]]=txt
        rendered[unit["number"]]=markdown_document(txt,unit["title"])
    with zipfile.ZipFile(source) as z:
        package_path=next(el.attrib["full-path"] for el in ET.fromstring(z.read("META-INF/container.xml")).iter() if local(el)=="rootfile")
        pkg=ET.fromstring(z.read(package_path))
        base_dir=posixpath.dirname(package_path)
        media={el.attrib["id"]:el for el in pkg.iter() if local(el)=="item" and "id" in el.attrib}
        spine=[el.attrib["idref"] for el in pkg.iter() if local(el)=="itemref"]
        need(len(spine)==48,"Original reading order is no longer 48 units")
        files=[posixpath.normpath(posixpath.join(base_dir,media[id_].attrib["href"])) for id_ in spine]
        path_to_unit={p:i+1 for i,p in enumerate(files)}
        need(all(f in z.namelist() for f in files),"Original source XHTML absent")
        labels={i:canonical_title(rendered[i]) for i in range(1,49)}
        replacements={}
        report={"format":"native-style-epub-v1","book":SLUG,"chapter_count":48,"modified_xhtml":[],"paragraph_split_units":[],"source_assets_retained":[],"localized_toc_links":0,"localized_ncx_labels":0}
        for num,(file,unit) in enumerate(zip(files,chapters),1):
            old_tree=ET.fromstring(z.read(file))
            old_tree.set("lang","ru")
            old_tree.set("{"+XML+"}lang","ru")
            blocks=rendered[num]
            new_h=[x for x in blocks if local(x) in {"h1","h2","h3","h4","h5","h6"}]
            new_p=[x for x in blocks if local(x)=="p"]
            need(len(new_h)+len(new_p)==len(blocks),f"Unsupported translated markup for unit {num}")
            doc_body=old_tree.find(PREFIX+"body")
            need(doc_body is not None, f"Missing source body {num}")
            title=old_tree.find("./"+PREFIX+"head/"+PREFIX+"title")
            if title is not None and new_h:
                title.text=inner(new_h[0])
            main=doc_body[0] if len(doc_body) else None
            need(main is not None, f"Missing source content root {num}")
            src_h=[x for x in main.iter() if local(x) in {"h1","h2","h3","h4","h5","h6"}]
            src_p=[x for x in main.iter() if local(x)=="p" and inner(x)]
            footers=[p for p in doc_body.iter() if local(p)=="p" and "oceanofpdf.com" in inner(p).lower()]
            need(len(footers)==1 and len(new_p)>=1, f"Publisher footer mismatch unit {num}")
            footer=footers[-1]
            translated_footer=new_p[-1]
            need("oceanofpdf.com" in inner(translated_footer).lower(),f"Translation footer missing unit {num}")
            if num==1:
                # Keep original vector-cover XHTML, image position, and publisher imprint.
                need(not new_h and not src_h,f"Unexpected titlepage heading {num}")
                transfer_text(footer,translated_footer)
            elif num==6:
                need(len(src_h)==1 and len(new_h)==1,f"TOC heading mismatch unit {num}")
                transfer_text(src_h[0],new_h[0])
                links=[x for x in main.iter() if local(x)=="a" and x.attrib.get("href","").startswith("part")]
                need(len(links)==42,f"Expected original 42 TOC links, got {len(links)}")
                for a in links:
                    dst=posixpath.normpath(posixpath.join(posixpath.dirname(file),a.attrib["href"].split("#",1)[0]))
                    idx=path_to_unit.get(dst)
                    need(idx and labels[idx],f"Unmapped TOC target {dst}")
                    spans=[el for el in a.iter() if local(el)=="span"]
                    text_target=spans[-1] if spans else a
                    text_target.text=labels[idx]
                    for ch in list(text_target):text_target.remove(ch)
                    report["localized_toc_links"]+=1
                transfer_text(footer,translated_footer)
            else:
                need(len(src_h)==len(new_h),f"Different chapter heading count: {num}: {len(src_h)} != {len(new_h)}")
                for sh,nh in zip(src_h,new_h):
                    transfer_text(sh,nh)
                native_content=[p for p in src_p if p is not footer]
                translated_content=new_p[:-1]
                groups=split_src(translated_content,native_content)
                for old_p,group in zip(native_content,groups):
                    transfer_text(old_p,group[0])
                    add_linkified_plain_text(old_p)
                    if len(group)>1:
                        report["paragraph_split_units"].append(num)
                    parents={child:parent for parent in main.iter() for child in parent}
                    parent=parents.get(old_p)
                    need(parent is not None,"Cannot find paragraph parent")
                    offset=list(parent).index(old_p)
                    for j,part in enumerate(group[1:],1):
                        added=ET.Element(old_p.tag,{k:v for k,v in old_p.attrib.items() if k!="id"})
                        transfer_text(added,part)
                        add_linkified_plain_text(added)
                        parent.insert(offset+j,added)
                transfer_text(footer,translated_footer)
            add_linkified_plain_text(footer)
            replacements[file]=ET.tostring(old_tree,encoding="utf-8",xml_declaration=True)
            # Ensure translation survived verbatim as rendered text in reading order.
            newtree=ET.fromstring(replacements[file])
            actual_body=newtree.find(PREFIX+"body")
            if num==6:
                need(report["localized_toc_links"]==42,"TOC replacement incomplete")
            elif num!=1:
                body_main=actual_body[0]
                visible=[e for e in body_main.iter() if local(e) in {"p","h1","h2","h3","h4","h5","h6"} and inner(e)]
                # Original has title card and blank spacer nodes; assert all localized
                # paragraphs exist in the right order without author/source words.
                expected=[inner(p) for p in blocks[:-1]]
                got=[inner(e) for e in visible]
                need(got==expected,f"Localized XHTML text/paragraph order drift unit {num}: {len(got)} vs {len(expected)}")
            report["modified_xhtml"].append(file)
        # Localization of OPF metadata and original Adobe/NCX reading navigation.
        languages=[el for el in pkg.iter() if el.tag=="{"+DC+"}language"]
        need(languages,"Original package language metadata missing")
        for el in languages:el.text="ru"
        replacements[package_path]=ET.tostring(pkg,encoding="utf-8",xml_declaration=True)
        for name in z.namelist():
            if not name.lower().endswith(".ncx"):continue
            toc=ET.fromstring(z.read(name))
            for point in toc.iter():
                if local(point)!="navpoint":continue
                content=next((e for e in point.iter() if local(e)=="content"),None)
                navlabel=next((e for e in point.iter() if local(e)=="navlabel"),None)
                if content is None or navlabel is None:continue
                href=content.attrib.get("src","").split("#",1)[0]
                dest=posixpath.normpath(posixpath.join(posixpath.dirname(name),href))
                chapter_number=path_to_unit.get(dest)
                if chapter_number and labels[chapter_number]:
                    text=next((e for e in navlabel.iter() if local(e)=="text"),None)
                    if text is not None:
                        text.text=labels[chapter_number]
                        report["localized_ncx_labels"]+=1
            replacements[name]=ET.tostring(toc,encoding="utf-8",xml_declaration=True)
        output=BASE/"output/obsession-eva-marks-original-style.epub"
        output.parent.mkdir(exist_ok=True)
        copy_epub(z,replacements,output)
        report["source_assets_retained"]=[x for x in z.namelist() if re.search(r'\.(css|ttf|otf|woff2?|jpe?g|png|svg)$',x,re.I)]
        report["source_sha256"]=SHA(source.read_bytes())
        report["artifact_sha256"]=SHA(output.read_bytes())
        report["artifact_bytes"]=output.stat().st_size
        report["status"]="built_unverified"
    # Independent package QA: XML+ZIP integrity; original styling and assets,
    # every internal resource/fragment, no text omission or English resurrection.
    with zipfile.ZipFile(source) as oldz,zipfile.ZipFile(output) as newz:
        need(newz.testzip() is None,"Corrupt EPUB ZIP member")
        need(set(newz.namelist())-{"mimetype"}==set(oldz.namelist())-{"mimetype"},"Original package members changed")
        need(newz.namelist()[0]=="mimetype" and newz.read("mimetype")==b"application/epub+zip","Invalid EPUB mimetype")
        need(newz.getinfo("mimetype").compress_type==zipfile.ZIP_STORED,"EPUB mimetype is compressed")
        for asset in report["source_assets_retained"]:
            need(newz.read(asset)==oldz.read(asset),f"Source CSS/font/image bytes mutated: {asset}")
        allnames=set(newz.namelist())
        xml_files=[x for x in allnames if x.endswith((".html",".xhtml",".opf",".ncx",".xml"))]
        ids={}
        rootmap={}
        for path in xml_files:
            el=ET.fromstring(newz.read(path))
            rootmap[path]=el
            idlist=[node.attrib["id"] for node in el.iter() if "id" in node.attrib]
            need(len(idlist)==len(set(idlist)),f"Duplicate fragment id: {path}")
            ids[path]=set(idlist)
        hrefs=0
        for path in files:
            for el in rootmap[path].iter():
                for attr in ("href","src","{http://www.w3.org/1999/xlink}href"):
                    link=el.attrib.get(attr)
                    if not link or link.startswith(("http://","https://","mailto:","data:")):continue
                    url=urlsplit(link)
                    if not url.path and not url.fragment:continue
                    target=posixpath.normpath(posixpath.join(posixpath.dirname(path),url.path))
                    need(target in allnames,f"Broken internal EPUB resource: {path} -> {link}")
                    if url.fragment and target in ids:
                        need(url.fragment in ids[target],f"Broken fragment ID: {path} -> {link}")
                    hrefs+=1
        report["validated_internal_links"]=hrefs
        report["status"]="verified"
    (BASE/"output/obsession-eva-marks-original-style-report.json").write_text(
        json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n","utf-8")
    print(json.dumps(report,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    build()
