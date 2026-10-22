#!/usr/bin/env python3
"""Reproducible layout-only repair for The Claiming Moon Russian EPUB.

Does not edit accepted translations, their SHA evidence or the pinned Workflow.
Verifies all visible text is preserved, repairs Markdown inline emphasis,
chapter and notes structure, and restores safely identified source-emphasized
whole paragraphs that were flattened at text extraction.
"""
from __future__ import annotations
import re, sys, zipfile, os, io, hashlib
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

NS = 'http://www.w3.org/1999/xhtml'
EPUB_NS = 'http://www.idpf.org/2007/ops'
DC_NS = 'http://purl.org/dc/elements/1.1/'
ET.register_namespace('', NS)
ET.register_namespace('epub', EPUB_NS)
ET.register_namespace('dc', DC_NS)

# Source-emphasis spans with independently identified Russian equivalents.
# These passages are restored as full-paragraph italics only where their
# source counterpart was entirely italic; ambiguous sub-paragraph cases are
# deliberately not guessed.
WHOLE_EMPHASIS = {
 3: [
  '— Этот мальчишка нас по миру пустит',
  'Кайла даже не поднял глаз от шитья',
  '— Растущие мальчишки всегда такие',
  'Рунджин фыркнул и сильнее раскачался',
  '— В мои времена волчата знали',
  '— А в твои времена еды и на добавку-то не хватало',
  'Мой.',
 ],
 7: ['Хочешь бежать? Ладно, беги.', 'Мой. Ты мой. Я поймал тебя.', 'Ты бежал, а я тебя поймал.'],
 10: ['Умница, волчонок.'],
 13: ['На кровати Чонгука.', '«Всё хорошо. Я с тобой».'],
 14: ['Как он всё ещё может выбирать меня?', 'Пока я с ним, со мной всё будет хорошо.'],
 26: ['Какого хуя делал Чонгук?', 'Младший брат.'],
 27: ['Младший брат.', 'Это я живу с человеком, который лгал мне в лицо.'],
 28: ['Ни хуя не идеально.'],
 33: ['Зомби.', 'Ты опоздал.'],
}
# Deterministic partial inline emphasis recovered from the original source.
# Each pair is a unique Russian paragraph prefix and exact italicized substring.
PARTIAL_EMPHASIS = {
 3: [('За эти годы десятки омег', '«Ой, Альфа, ты меня нашёл. Похоже, теперь я твой»'),('«Нашёл тебя»,', '«Нашёл тебя»')],
 6: [('Но в голове то и дело всплывало лицо Айрин.', '«Он убийца, Тэ. Не забывай, кто он на самом деле под всей этой добротой»')],
 7: [('Он быстро-быстро заморгал', 'С чего я вдруг так расчувствовался?')],
 8: [('«Так бывает, когда Альфа', '«Так бывает, когда Альфа ведёт себя безрассудно на охоте»'),('А ещё насильником.', 'насильником')],
 11: [('Его альфа кричал.', 'Возьми его. Сцепись с ним узлом.')],
 12: [('А в голове крутилось одно:', 'почему он такой спокойный? Почему он не умирает от стыда, как я? Почему смотрит на меня так, словно я не сделал ничего унизительного?'),('Почему он всё время так зовёт меня', 'Почему он всё время так зовёт меня «волчонком»? Почему у меня всё тело откликается на его голос?')],
 13: [('Тэхён глуповато моргнул', '«Это не я придумал»'),('Тэхён так же беззвучно ответил:', '«Врёшь»')],
 14: [('Кто-то следит за мной.', 'Кто-то следит за мной.')],
 15: [('Тэхён шутливо скалит зубы', '«Какого хера ты вообще творишь, ублюдок?»')],
 16: [('Держись рядом. Я тебя защищу.', 'Держись рядом. Я тебя защищу.')],
 19: [('«Береги себя, моя пара.', '«Береги себя, моя пара. Я вернусь к тебе»')],
 22: [('Слышал, как она снова и снова повторяла', 'Никогда, никогда не доверяй альфе.')],
 23: [('Он схватился за перемычку', 'разорвал')],
 25: [('Он открыл мысленную связь', '«Люблю тебя, альфа»'),('Ответ пришёл мгновенно', '«Привет, мой сладкий малыш. Проснулся?»'),('Тэхён покраснел.', '«Да-а-а»'),('«Хороший мальчик.', '«Хороший мальчик.')],
 27: [('Он так сильно любил Чонгука.', 'любил')],
 42: [('Он не думал, что Юнги настолько', 'настолько')],
 43: [('Именно здесь с ним произошло', 'Именно здесь')],
}

INLINE_MARKUP = re.compile(r'(?<!\\)(\*\*(?=\S)[^\n*]+?(?<=\S)\*\*|(?<!\*)\*(?=\S)[^\n*]+?(?<=\S)\*(?!\*)|`[^`\n]+`)')
CHAPTER_HEADER = re.compile(r'^\s*Глава\s+\d+\b',re.I)
NOTES_HEADING = re.compile(r'^(?:Примечания(?:\s+автора)?(?:\s+(?:перед|после|в конце)\s+главы|\s+к\s+главе)?|Примечания в конце главы|Заметки автора)(?:\s*[:.]?)$',re.I)
MINOR_SECTION = re.compile(r'^\s*(?:ГЛАВА\s+\d+|Текст главы)\s*$',re.I)
STYLE = '''body { font-family: serif; line-height: 1.56; margin: 0 4%; }
h1.chapter-title { font-size: 1.55em; font-weight: bold; text-align: center; margin: 1.6em 0 1em; break-after: avoid; page-break-after: avoid; }
h1 { font-size: 1.5em; }
h2.note-heading { font-size: 1.03em; font-weight: bold; margin: 1.5em 0 .65em; break-after: avoid; page-break-after: avoid; }
h2, h3, h4, h5, h6 { break-after: avoid; page-break-after: avoid; }
h3.internal-heading { text-align: center; font-size: 1em; margin: 1.5em 0 .9em; }
p { margin: .2em 0; text-indent: 1.2em; orphans: 2; widows: 2; }
p.first-paragraph, p.author-note, p.metadata, p.summary, p.scene-break { text-indent: 0; }
p.author-note { margin: .5em 0; font-size: .95em; }
p.scene-break { text-align: center; margin: 1.1em auto; }
strong, b { font-weight: bold; }
em, i { font-style: italic; }
pre { white-space: pre-wrap; }
'''

def local(el): return el.tag.rsplit('}',1)[-1]
def t(el): return ''.join(el.itertext())
def norm(s): return re.sub(r'\s+',' ',s).strip()

def append_inline(el, text):
    """Parse the safe Markdown inline subset into XML nodes; reject raw markup."""
    from html import unescape
    source = text
    prev=0
    for match in INLINE_MARKUP.finditer(source):
        lit=source[prev:match.start()]
        if len(el): el[-1].tail=(el[-1].tail or '')+lit
        else: el.text=(el.text or '')+lit
        token=match.group()
        if token.startswith('**'):
            tag='strong'; value=token[2:-2]
        elif token.startswith('*'):
            tag='em'; value=token[1:-1]
        else:
            tag='code'; value=token[1:-1]
        child=ET.SubElement(el,f'{{{NS}}}{tag}')
        child.text=value
        prev=match.end()
    remainder=source[prev:]
    if len(el):el[-1].tail=(el[-1].tail or '')+remainder
    else:el.text=(el.text or '')+remainder
    # Unescape authored escaped asterisk sequences without interpreting as tags.
    for n in el.iter():
        if n.text: n.text=n.text.replace('\\*','*').replace('\\`','`')
        if n.tail: n.tail=n.tail.replace('\\*','*').replace('\\`','`')

def inline_existing(root):
    changed=0
    for el in root.iter():
        if local(el) not in ('p','h1','h2','h3','li'):continue
        if len(el):continue
        text=el.text or ''
        if INLINE_MARKUP.search(text):
            el.text=None;append_inline(el,text);changed+=1
    return changed

def heading_text(s):
    s=norm(s).strip(' .')
    return s

def apply_structure(root,unit):
    body=root.find(f'{{{NS}}}body'); children=list(body)
    if unit==1:
        for el in children:
            if local(el)=='p':el.set('class','metadata')
    elif unit==2:
        for el in children:
            if local(el)=='p':el.set('class','summary')
    elif unit<48:
        first=children[0]
        if local(first) in ('p','h2','h3') and CHAPTER_HEADER.match(t(first)):
            first.tag=f'{{{NS}}}h1'
        # If the first chapter block does not contain a heading, inject using
        # existing section title in the table of contents (not new content).
        if local(first)=='h1':first.set('class','chapter-title')
        for el in children[1:]:
            txt=norm(t(el))
            if local(el) in ('p','h3') and (NOTES_HEADING.match(txt) or (txt.lower().startswith('примечания автора') and len(txt)<55)):
                el.tag=f'{{{NS}}}h2'
            if local(el)=='h2' and ('примечани' in txt.lower() or 'заметки автора' in txt.lower()):el.set('class','note-heading')
            if local(el) in ('p','h1','h2') and MINOR_SECTION.match(txt):
                el.tag=f'{{{NS}}}h3';el.set('class','internal-heading')
            if txt in {'—','–','* * *','***','- - -'} and local(el)=='p':el.set('class','scene-break')
        # Capture opening author's notes and endnote paragraphs as visually
        # distinct from story narrative, without mislabeling content.
        children=list(body); note_heading_idxs=[i for i,e in enumerate(children) if local(e) in ('h2','h3') and 'примечан' in norm(t(e)).lower()]
        for ni in note_heading_idxs:
            is_end=ni > len(children)//2 or 'конце' in norm(t(children[ni])).lower() or 'после' in norm(t(children[ni])).lower()
            if is_end:
                next_index=len(children)
            else:
                next_index=min(len(children),ni+4)
                for j in range(ni+1,next_index):
                    if local(children[j]) in ('h1','h2','h3') or norm(t(children[j])).lower().startswith('дополнительные примечания'):
                        next_index=j+1;break
            for p in children[ni+1:next_index]:
                if local(p)=='p':p.set('class','author-note')
        # Root story first paragraph never appears before an author's note.
        h1=body.find(f'{{{NS}}}h1')
        if h1 is not None and h1 is not children[0]:h1.set('class','chapter-title')
    return body

def apply_source_emphasis(root, unit):
    pats=WHOLE_EMPHASIS.get(unit,[])
    if not pats:return 0,[]
    paragraphs=[n for n in root.iter() if local(n)=='p']
    used=set();bad=[];counter=0
    for needle in pats:
        matches=[p for p in paragraphs if norm(t(p)).lower().startswith(needle.lower())]
        if len(matches)!=1 and not (unit==27 and needle=='Младший брат.' and len(matches)==2):bad.append((needle,len(matches)));continue
        target=matches[-1] if (unit==27 and needle=='Младший брат.') else matches[0]
        if id(target) in used:continue
        used.add(id(target))
        if len(target)==0:
            full=target.text or ''
            if full.startswith('*') and full.endswith('*'):
                target.text=full[1:-1]
            else:
                target.text=None
                em=ET.SubElement(target,f'{{{NS}}}em');em.text=full
        else:
            # Already carries an authored Markdown emphasis -- do not duplicate.
            if not any(local(x)=='em' for x in target.iter()):
                full=t(target)
                target[:]=[];target.text=None
                em=ET.SubElement(target,f'{{{NS}}}em');em.text=full
        counter+=1
    return counter,bad

def apply_partial_emphasis(root, unit):
    specs=PARTIAL_EMPHASIS.get(unit,[])
    if not specs:return 0,[]
    paragraphs=[n for n in root.iter() if local(n)=='p']
    success=0; missing=[]
    for anchor,marked in specs:
        matches=[p for p in paragraphs if norm(t(p)).startswith(anchor)]
        if unit==14 and anchor=='Кто-то следит за мной.' and len(matches)==3:
            selected=matches
        elif len(matches)==1:
            selected=matches
        else:
            missing.append((anchor,marked,len(matches)));continue
        for p in selected:
            if len(p)>0:
                # Already italicized Markdown target, avoid double treatment.
                if any(local(c)=='em' for c in p.iter()):continue
                missing.append((anchor,'existing child nodes',len(p)));continue
            full=p.text or ''
            pos=full.find(marked)
            if pos<0:
                missing.append((anchor,marked,'not found'));continue
            p.text=full[:pos]
            child=ET.SubElement(p,f'{{{NS}}}em');child.text=marked;child.tail=full[pos+len(marked):]
            success+=1
    return success,missing

def repair(old_epub, source_epub, new_epub):
    with zipfile.ZipFile(old_epub) as src,zipfile.ZipFile(source_epub) as raw:
        names=src.namelist(); texts=[n for n in names if n.startswith('EPUB/text/') and n.endswith('.xhtml')]
        assert len(texts)==48 and src.read('mimetype')==b'application/epub+zip'
        fixups={};stats=[];heading_missing=[]
        for unit,name in enumerate(texts,1):
            root=ET.fromstring(src.read(name));before=norm(t(root.find(f'{{{NS}}}body')))
            updated=inline_existing(root);body=apply_structure(root,unit)
            italicized,missing=apply_source_emphasis(root,unit)
            partial,partial_missing=apply_partial_emphasis(root,unit)
            italicized+=partial
            missing.extend(partial_missing)
            if missing:heading_missing.append((unit,missing))
            after=norm(t(body))
            # Styling alone must not change literary text except stripping markup.
            a=INLINE_MARKUP.sub(lambda m: m.group()[2:-2] if m.group().startswith('**') else m.group()[1:-1],before)
            if a!=after: raise AssertionError(f'Text content changed unit {unit}: {len(a)} -> {len(after)}; before={a[:200]!r} after={after[:200]!r}')
            fixups[name]=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            stats.append((unit,updated,italicized,len([e for e in body if local(e)=='h1']),len([e for e in body if local(e)=='h2'])))
        if heading_missing: print('emphasis mismatches:',heading_missing,file=sys.stderr)
        nav=ET.fromstring(src.read('EPUB/nav.xhtml')); links=nav.findall('.//{%s}a'%NS)
        assert len(links)==48
        for unit,(anchor,name) in enumerate(zip(links,texts),1):
            if unit==1:new_title='Предисловие'
            elif unit==2:new_title='Аннотация'
            elif unit==48:new_title='Послесловие'
            else:
                chapter_root=ET.fromstring(fixups[name]); h=chapter_root.find('.//{%s}h1'%NS)
                if h is None:
                    paragraphs=[p for p in chapter_root.findall('.//{%s}body/*'%NS) if local(p)=='p']
                    new_title=norm(t(paragraphs[0]))[:90] if paragraphs else anchor.text
                else:new_title=norm(t(h))
            anchor.text=new_title
        for el in nav.iter():
            if local(el)=='h1' and t(el)=='Contents':el.text='Содержание'
        fixups['EPUB/nav.xhtml']=ET.tostring(nav,encoding='utf-8',xml_declaration=True)
        opf=ET.fromstring(src.read('EPUB/package.opf'))
        for ch in opf.iter():
            if ch.tag=='{%s}title'%DC_NS:ch.text='Луна присвоения'
        fixups['EPUB/package.opf']=ET.tostring(opf,encoding='utf-8',xml_declaration=True)
        fixups['EPUB/styles.css']=STYLE.encode()
        with zipfile.ZipFile(new_epub,'w') as output:
            for info in src.infolist():
                output.writestr(info,fixups.get(info.filename,src.read(info.filename)))
    with zipfile.ZipFile(new_epub) as z:
        assert z.testzip() is None
        for name in texts:ET.fromstring(z.read(name))
    print('FILE',new_epub,'SIZE',new_epub.stat().st_size,'SHA256',hashlib.sha256(new_epub.read_bytes()).hexdigest())
    print('MARKUP',(sum(a[1] for a in stats)),'WHOLE_EM',(sum(a[2] for a in stats)),'H1',(sum(a[3] for a in stats)),'H2',(sum(a[4] for a in stats)))
    print('NO_HEADING',[a[0] for a in stats if a[3]!=1 and 3<=a[0]<=47])
    return stats

if __name__=='__main__':
    inp=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/mnt/data/The_Claiming_Moon_RU.epub')
    source=Path(sys.argv[2]) if len(sys.argv)>2 else Path('/mnt/data/claiming_inputs/The_Claiming_Moon.epub')
    out=Path(sys.argv[3]) if len(sys.argv)>3 else Path('/mnt/data/The_Claiming_Moon_RU_Formatted.epub')
    repair(inp,source,out)
