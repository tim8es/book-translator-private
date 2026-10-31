from __future__ import annotations
import io, hashlib, json, posixpath, re, shutil, zipfile, copy, unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, unquote
from lxml import etree as ET
from analyze import getbl, tag, trans, M, ROOT, p
from align import align, clean
ROOT_DIR = Path(__file__).resolve().parent
SRC = ROOT / 'source' / 'The_Claiming_Moon.epub'
OUTPUT = ROOT / 'output' / 'The_Claiming_Moon_RU_Structural_Migrated.epub'
REPORT = ROOT_DIR / 'migration_report.json'
NS = 'http://www.w3.org/1999/xhtml'
XML_NS = 'http://www.w3.org/XML/1998/namespace'

def get_leaves(root):
    body = next((n for n in root.iter() if local(n) == 'body'))
    B = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'pre', 'div', 'section', 'article', 'aside', 'blockquote', 'figcaption', 'td', 'th', 'dt', 'dd', 'caption', 'address', 'header', 'footer'}
    C = B | {'body', 'ol', 'ul', 'table', 'tbody', 'thead', 'tfoot', 'tr', 'dl', 'main', 'figure', 'nav'}
    leaves = []

    def walk(n):
        a = local(n)
        blocks = [child for child in n if local(child) in C]
        if a in B and (not blocks):
            if ''.join(n.itertext()).strip() or any((local(x) in ('img', 'br', 'hr') for x in n.iter())):
                leaves.append(n)
            return
        for child in n:
            walk(child)
    walk(body)
    return leaves

def local(n):
    return ET.QName(n).localname

def normalize(s):
    return ''.join((x for x in unicodedata.normalize('NFC', s) if not x.isspace()))

def de_markdown(s):
    s = s.strip()
    s = re.sub('^#{1,6}\\s+', '', s)
    s = s.replace('**', '')
    s = re.sub('(?<!\\w)\\*([^*\\n]+)\\*', '\\1', s)
    s = s.replace('  \n', '\n')
    return s

def locate_cut(s, expected, min_cut=0):
    if expected <= 0:
        return 0
    if expected >= len(s):
        return len(s)
    window = max(9, round(len(s) * 0.08))
    best = (9999, expected)
    for idx in range(max(min_cut + 1, expected - window), min(len(s) - 1, expected + window) + 1):
        if s[idx].isspace():
            score = abs(idx - expected) * 1.0
        elif s[idx - 1] in '.!?…':
            score = abs(idx - expected) * 0.7 + 3
        elif s[idx - 1] in ',;:':
            score = abs(idx - expected) * 0.8 + 5
        else:
            continue
        if score < best[0]:
            best = (score, idx)
    return best[1]

def split_proportionally(text, weights):
    if not weights:
        return []
    if len(weights) == 1:
        return [text]
    cum = 0
    cuts = []
    for w in weights[:-1]:
        cum += w
        want = round(len(text) * cum / max(1, sum(weights)))
        pos = locate_cut(text, want, cuts[-1] if cuts else 0)
        cuts.append(pos)
    return [text[a:b] for a, b in zip([0] + cuts, cuts + [len(text)])]

def slots(node):
    slots = []

    def walk(n):
        slots.append((n, 'text', n.text or ''))
        for ch in n:
            walk(ch)
            slots.append((ch, 'tail', ch.tail or ''))
    walk(node)
    return slots

def find_link_text(target, source, href):
    patterns = []
    if 'archiveofourown.org' in href or 'Archive' in source:
        patterns = ['Archive of Our Own', 'Архив(?:е|а|у|ом)?', 'комментар(?:ий|ии|иях|ий)']
    if 'note' in source.lower() or 'endnotes' in href.lower():
        patterns = ['примечани[а-я]*']
    if source.lower().strip() in ('return', 'back') or 'noteref' in href:
        patterns = ['Назад', 'вернут[ьс]*я', 'к началу']
    if source in target:
        return (target.index(source), target.index(source) + len(source))
    for pat in patterns:
        m = re.search(pat, target, re.I)
        if m:
            return m.span()
    return None

def replace_content(node, russian, stats):
    orig_slots = slots(node)
    positions = [x for x in orig_slots if x[2]]
    active = [x for x in positions if x[2].strip()]
    text = russian
    if not active:
        node.text = text
        return
    weights = [max(1, len(x[2].strip())) for x in active]
    pieces = split_proportionally(text, weights)
    for item in orig_slots:
        n, k, old = item
        setattr(n, k, '')
    for (n, k, _), value in zip(active, pieces):
        setattr(n, k, value)
    for a in node.iter():
        if local(a) == 'a' and a.get('href'):
            stats['links_preserved'] += 1
            href = a.get('href')
            source = ''.join(a.itertext()).strip()
            if not source:
                stats['empty_anchors'] += 1

def add_clone(block, text):
    extra = ET.Element(block.tag, nsmap=None)
    for k, v in block.attrib.items():
        if localattr(k) in ('id', 'name'):
            continue
        extra.attrib[k] = v
    extra.text = text
    block.addnext(extra)
    return extra

def localattr(x):
    return x.rsplit('}', 1)[-1]

def assign_group(src_nodes, ru_segments, stats, unit):
    if not src_nodes:
        if ru_segments:
            raise ValueError(f'{unit}: translated text has no source block')
        return
    if not ru_segments:
        for node in src_nodes:
            old = ''.join(node.itertext()).strip()
            if old:
                stats['unmapped_source_blocks'].append({'unit': unit, 'source': old[:130], 'tag': local(node)})
            replace_content(node, '', stats)
        return
    r = [de_markdown(x) for x in ru_segments]
    if len(src_nodes) == 1:
        replace_content(src_nodes[0], r[0], stats)
        previous = src_nodes[-1]
        for extra in r[1:]:
            previous = add_clone(previous, extra)
            stats['extra_ru_blocks'] += 1
        return
    if len(r) == 1:
        eng = [''.join(n.itertext()).strip() for n in src_nodes]
        if all(eng):
            parts = split_proportionally(r[0], [len(x) for x in eng])
        else:
            first = next((k for k, x in enumerate(eng) if x), 0)
            parts = [''] * len(src_nodes)
            parts[first] = r[0]
        for node, v in zip(src_nodes, parts):
            replace_content(node, v, stats)
        stats['multi_source_groups'] += 1
        return
    for j, node in enumerate(src_nodes):
        replace_content(node, r[min(j, len(r) - 1)] if j < len(r) else '', stats)
    for extra in r[len(src_nodes):]:
        add_clone(src_nodes[-1], extra)
        stats['extra_ru_blocks'] += 1

def repair_link_to_notes(doc, unit, stats):
    original = [a for a in doc.iter() if isinstance(a.tag, str) and local(a) == 'a' and (a.get('href') or '').startswith('#endnotes')]
    if not original:
        return
    leaves = get_leaves(doc)
    chosen = None
    for block in leaves[:18]:
        text = ''.join(block.itertext())
        match = re.search('примечани[а-я]*', text, re.I)
        if match:
            priority = 0 if re.search('дополнительн|в конце', text, re.I) else 1
            if chosen is None or priority < chosen[0]:
                chosen = (priority, block)
    if chosen is None:
        stats.setdefault('link_fallbacks', []).append(unit)
        return
    dest = chosen[1]
    for a in original:
        if a.getparent() is None:
            continue
        href = a.get('href')
        parent = a.getparent()
        if a is not None and any((a is x for x in dest.iter())):
            pass
        pos = parent.index(a)
        last = parent[pos - 1] if pos > 0 else None
        tail = (a.text or '') + ''.join(a.itertext())[:-len(a.text or '')] if False else ''.join(a.itertext())
        tail += a.tail or ''
        if last is None:
            parent.text = (parent.text or '') + tail
        else:
            last.tail = (last.tail or '') + tail
        parent.remove(a)
        placed = False
        for owner, kind, segment in slots(dest):
            match = re.search('примечани[а-я]*', segment, re.I)
            if not match:
                continue
            before, word, after = (segment[:match.start()], segment[match.start():match.end()], segment[match.end():])
            owner_text = before
            setattr(owner, kind, owner_text)
            anchor = ET.Element('{' + NS + '}a', href=href)
            anchor.text = word
            anchor.tail = after
            if kind == 'text':
                owner.insert(0, anchor)
            else:
                owner.addnext(anchor)
            placed = True
            stats['relocated_note_links'] = stats.get('relocated_note_links', 0) + 1
            break
        if not placed:
            raise ValueError(f'unit {unit}: cannot relink note without text loss')

def repair_preface_links(doc):
    leaves = get_leaves(doc)
    source = next((n for n in leaves if local(n) == 'p' and n.get('class') == 'message'), None)
    if source is None:
        return
    sibling = source.getnext()
    next_sibling = sibling.getnext() if sibling is not None else None
    if sibling is None or next_sibling is None:
        return
    links = [a for a in source if local(a) == 'a' and a.get('href')]
    if len(links) != 2:
        return
    hrefs = [a.get('href') for a in links]
    if 'archiveofourown.org' not in ' '.join(hrefs):
        return
    russian_sentence = ''.join(next_sibling.itertext())
    label = 'Archive of Our Own'
    url = 'https://archiveofourown.org/works/70374321'
    if label not in russian_sentence or url not in russian_sentence:
        return
    strong = next((n for n in source if local(n) == 'b'), None)
    br = next((n for n in source if local(n) == 'br'), None)
    for child in list(source):
        if child is strong or child is br:
            continue
        source.remove(child)
    source.text = ''
    if strong is not None:
        strong.text = 'Автор:'
        strong.tail = ' Kooktaexd'
        if br is not None:
            br.tail = ''
    else:
        source.text = 'Автор: Kooktaexd'
    next_sibling.text = russian_sentence.split(label, 1)[0]
    if sibling.text is None:
        sibling.text = 'Предисловие / сведения об оригинале'
    parent = next_sibling
    for child in list(parent):
        parent.remove(child)
    sentence = '«Луна присвоения» первоначально опубликована на ' + label + ': ' + url + '.'
    parent.text = sentence.split(label, 1)[0]
    first = ET.SubElement(parent, '{' + NS + '}a', href=hrefs[0])
    first.text = label
    first.tail = ': '
    second = ET.SubElement(parent, '{' + NS + '}a', href=hrefs[1])
    second.text = url
    second.tail = '.'

def repair_preface_metadata(doc, translated):
    dl = next((node for node in doc.iter() if isinstance(node.tag, str) and local(node) == 'dl'), None)
    if dl is None:
        return
    fields = [x for x in dl if local(x) in ('dt', 'dd')]
    if len(fields) != 18:
        return
    for i in range(7):
        text = de_markdown(translated[4 + i])
        if ':' not in text:
            continue
        label, value = text.split(':', 1)
        dt, dd = fields[2 * i:2 * i + 2]
        replace_content(dt, label.strip() + ':', {'links_preserved': 0, 'empty_anchors': 0})
        replace_content(dd, value.strip(), {'links_preserved': 0, 'empty_anchors': 0})
    dt, dd = fields[14:16]
    replace_content(dt, 'Язык оригинала:', {'links_preserved': 0, 'empty_anchors': 0})
    replace_content(dd, 'английский.', {'links_preserved': 0, 'empty_anchors': 0})
    replace_content(fields[16], de_markdown(translated[12]), {'links_preserved': 0, 'empty_anchors': 0})
    replace_content(fields[17], de_markdown(translated[13]), {'links_preserved': 0, 'empty_anchors': 0})

def migrate():
    original = SRC.read_bytes()
    sha = hashlib.sha256(original).hexdigest()
    metadata = json.loads((ROOT / 'metadata.json').read_text())
    if sha != metadata['source']['sha256']:
        raise ValueError('Original SHA mismatch')
    progress = json.loads((ROOT / 'progress.json').read_text())
    if len(progress['chapters']) != 48 or any((x['status'] != 'reviewed' for x in progress['chapters'])):
        raise ValueError('Reviewed chapters changed')
    report = {'original_sha256': sha, 'unit_count': 48, 'units': [], 'warnings': []}
    replacements = {}
    stats = {'extra_ru_blocks': 0, 'multi_source_groups': 0, 'links_preserved': 0, 'empty_anchors': 0, 'unmapped_source_blocks': []}
    with zipfile.ZipFile(SRC) as origin:
        opf = [n for n in origin.namelist() if n.endswith('.opf')][0]
        root = ET.fromstring(origin.read(opf))
        base = posixpath.dirname(opf)
        hrefs = {item.get('id'): item.get('href') for item in root.iter() if local(item) == 'item'}
        spine = [posixpath.normpath(posixpath.join(base, hrefs[x.get('idref')])) for x in root.iter() if local(x) == 'itemref']
        if len(spine) != 48:
            raise ValueError('Spine count mismatch')
        for i, (path, rec) in enumerate(zip(spine, progress['chapters'])):
            old = origin.read(path)
            doc = ET.fromstring(old)
            leaves = get_leaves(doc)
            aligned = align(i)
            if aligned.get('error'):
                raise ValueError(aligned['error'])
            if len(leaves) != aligned['n']:
                raise ValueError(f'{path}: blocks count drift')
            r = trans(i)
            if hashlib.sha256((ROOT / rec['translation_path']).read_bytes()).hexdigest() != rec['translation_acceptance']['translation_sha256']:
                raise ValueError(f'{path}: translation_sha256 changed')
            used = []
            for a, b, c, d in aligned['route']:
                assign_group(leaves[a:b], r[c:d], stats, i + 1)
                used.extend(range(c, d))
            if i == 0:
                repair_preface_links(doc)
                repair_preface_metadata(doc, r)
            repair_link_to_notes(doc, i + 1, stats)
            if used != list(range(len(r))):
                raise ValueError(f'{path}: duplicated/omitted translation block')
            for title_node in doc.iter():
                if isinstance(title_node.tag, str) and local(title_node) == 'title':
                    title_node.text = 'Луна присвоения — Kooktaexd'
            doc.set('{' + XML_NS + '}lang', 'ru')
            doc.set('lang', 'ru')
            output = ET.tostring(doc, encoding='UTF-8', xml_declaration=True, method='xml')
            replacements[path] = output
            ru_text = ''.join((de_markdown(x) for x in r))
            anew = ET.fromstring(output)
            generated = ''.join((''.join(x.itertext()) for x in get_leaves(anew)))
            if normalize(generated) != normalize(ru_text):
                from difflib import SequenceMatcher
                normgen = normalize(generated)
                normref = normalize(ru_text)
                sm = SequenceMatcher(None, normref, normgen, autojunk=False)
                first = next((op for op in sm.get_opcodes() if op[0] != 'equal'), None)
                raise ValueError(f'unit {i + 1}: rendered text loss/reordering at {first}, ref={len(normref)} generated={len(normgen)}')
            unit = {'number': i + 1, 'filename': path, 'source_blocks': len(leaves), 'translation_blocks': len(r), 'alignment_cost': aligned['cost'], 'moves': aligned['moves'], 'source_sha256': hashlib.sha256(old).hexdigest(), 'translation_sha256': rec['translation_acceptance']['translation_sha256'], 'rendered_sha256': hashlib.sha256(output).hexdigest(), 'coverage': 'exact_nonwhitespace_match'}
            report['units'].append(unit)
        for n in root.iter():
            if local(n) == 'language' and n.text == 'en':
                n.text = 'ru'
            if local(n) == 'title':
                n.text = 'Луна присвоения'
        replacements[opf] = ET.tostring(root, encoding='UTF-8', xml_declaration=True, method='xml')
        for pth in origin.namelist():
            if not pth.endswith('.ncx'):
                continue
            ncx = ET.fromstring(origin.read(pth))
            for n in ncx.iter():
                if local(n) == 'docTitle':
                    for q in n.iter():
                        if local(q) == 'text':
                            q.text = 'Луна присвоения'
            for nav in ncx.iter():
                if local(nav) != 'navPoint':
                    continue
                content = next((q.get('src') for q in nav.iter() if local(q) == 'content'), None)
                if not content:
                    continue
                target = posixpath.normpath(posixpath.join(posixpath.dirname(pth), content.split('#')[0]))
                if target not in spine:
                    continue
                idx = spine.index(target)
                heading = de_markdown(trans(idx)[0])
                for label in nav.iter():
                    if local(label) == 'text':
                        label.text = heading
                        break
            replacements[pth] = ET.tostring(ncx, encoding='UTF-8', xml_declaration=True, method='xml')
        with zipfile.ZipFile(OUTPUT, 'w') as dest:
            for info in origin.infolist():
                dest.writestr(copy.copy(info), replacements.get(info.filename) if info.filename in replacements else origin.read(info.filename))
        report['changed_spine_documents'] = len([x for x in spine if replacements[x] != origin.read(x)])
        report['all_nontext_resources_byte_identical'] = all((origin.read(x) == zipfile.ZipFile(OUTPUT).read(x) for x in origin.namelist() if x not in replacements))
        report['stats'] = stats
        report['rendered_sha256'] = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
        report['output_path'] = OUTPUT.name
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    return report
if __name__ == '__main__':
    r = migrate()
    print('MIGRATED', len(r['units']), 'chapters', r['stats'], 'size', OUTPUT.stat().st_size, 'sha', r['rendered_sha256'])
