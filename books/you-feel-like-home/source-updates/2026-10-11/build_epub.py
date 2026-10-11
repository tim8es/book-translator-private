from pathlib import Path
from html import escape
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from xml.etree import ElementTree as ET
import re

ROOT=Path(__file__).resolve().parent
BOOK=ROOT.parent.parent
OLD=BOOK/'output/You_Feel_Like_Home_RU_chapters_1-8.epub'
NEW=BOOK/'output/You_Feel_Like_Home_RU_chapters_1-9.epub'
MD=ROOT/'translated/011-chapter-9.md'
SECTION='OEBPS/section-09a.xhtml'
OPF='OEBPS/content.opf'
NAV='OEBPS/nav.xhtml'
NCX='OEBPS/toc.ncx'

def inline(s):
    s=escape(s,quote=False)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)',r'<em>\1</em>',s)

def chapter(md):
    items=[]
    for part in re.split(r'\n\s*\n',md.strip()):
        p=part.strip()
        if p=='++++': items.append('<p class="scene-break">++++</p>')
        elif p.startswith('## '): items.append('<h3>'+inline(p[3:])+'</h3>')
        elif p.startswith('# '): items.append('<h2>'+inline(p[2:])+'</h2>')
        else: items.append('<p>'+inline(p).replace('\n','<br/>')+'</p>')
    s=('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
       '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru">'
       '<head><title>Глава 9</title><link rel="stylesheet" href="styles.css" type="text/css"/></head>'
       '<body>'+'\n'.join(items)+'</body></html>')
    ET.fromstring(s.encode())
    return s.encode()

def update_opf(data):
    ns='http://www.idpf.org/2007/opf'
    tree=ET.fromstring(data)
    m=tree.find('{'+ns+'}manifest')
    s=tree.find('{'+ns+'}spine')
    assert m is not None and s is not None
    assert not any(x.get('href')=='section-09a.xhtml' for x in m)
    m.append(ET.Element('{'+ns+'}item',{'id':'ru9','href':'section-09a.xhtml','media-type':'application/xhtml+xml'}))
    refs=s.findall('{'+ns+'}itemref')
    assert len(refs)>=9
    s.insert(list(s).index(refs[-1]),ET.Element('{'+ns+'}itemref',{'idref':'ru9'}))
    return ET.tostring(tree,encoding='utf-8',xml_declaration=True)

def update_nav(data):
    ns='http://www.w3.org/1999/xhtml'
    root=ET.fromstring(data)
    navs=root.findall('.//{'+ns+'}nav')
    assert navs
    nav=next((n for n in navs if n.get('{http://www.idpf.org/2007/ops}type')=='toc'),navs[0])
    ol=nav.find('{'+ns+'}ol')
    assert ol is not None and len(ol)>=9
    li=ET.Element('{'+ns+'}li')
    ET.SubElement(li,'{'+ns+'}a',{'href':'section-09a.xhtml'}).text='Глава 9'
    ol.insert(len(ol)-1,li)
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)

def update_ncx(data):
    ns='http://www.daisy.org/z3986/2005/ncx/'
    root=ET.fromstring(data)
    nav=root.find('{'+ns+'}navMap')
    assert nav is not None
    points=nav.findall('{'+ns+'}navPoint')
    assert len(points)>=9
    point=ET.Element('{'+ns+'}navPoint',{'id':'ru-chapter-9','playOrder':'1'})
    lab=ET.SubElement(point,'{'+ns+'}navLabel')
    ET.SubElement(lab,'{'+ns+'}text').text='Глава 9'
    ET.SubElement(point,'{'+ns+'}content',{'src':'section-09a.xhtml'})
    nav.insert(list(nav).index(points[-1]),point)
    for i,item in enumerate(root.iter('{'+ns+'}navPoint'),1): item.set('playOrder',str(i))
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)

def main():
    md=MD.read_text('utf-8')
    assert md.startswith('# Глава 9') and md.count('++++')==6 and len(md)>40000
    xhtml=chapter(md)
    with ZipFile(OLD) as z:
        for p in ['mimetype',OPF,NAV,NCX,'OEBPS/section-01.xhtml','OEBPS/section-10.xhtml']:
            assert p in z.namelist(),p
        assert SECTION not in z.namelist()
        modifications={OPF:update_opf(z.read(OPF)),NAV:update_nav(z.read(NAV)),NCX:update_ncx(z.read(NCX))}
        front=z.read('OEBPS/section-01.xhtml')
        modifications['OEBPS/section-01.xhtml']=front.replace('Глав: 8/?'.encode(),'Глав: 9/?'.encode())
        with ZipFile(NEW,'w') as out:
            out.writestr('mimetype',z.read('mimetype'),compress_type=ZIP_STORED)
            for info in z.infolist():
                if info.filename=='mimetype': continue
                if info.filename=='OEBPS/section-10.xhtml':
                    out.writestr(SECTION,xhtml,compress_type=ZIP_DEFLATED)
                out.writestr(info,modifications.get(info.filename,z.read(info)))
    with ZipFile(NEW) as z:
        assert z.testzip() is None
        assert z.read('mimetype')==b'application/epub+zip'
        assert z.read(SECTION).count(b'++++')==6
        opf=ET.fromstring(z.read(OPF))
        refs=[e.get('idref') for e in opf.findall('.//{http://www.idpf.org/2007/opf}spine/{http://www.idpf.org/2007/opf}itemref')]
        assert refs[-2]=='ru9',refs
        ET.fromstring(z.read(NCX))
        ET.fromstring(z.read(NAV))
    print('Validated '+str(NEW)+' ('+str(NEW.stat().st_size)+' bytes)')

if __name__=='__main__': main()
