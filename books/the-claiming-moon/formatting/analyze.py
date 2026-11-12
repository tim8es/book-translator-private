from xml.etree import ElementTree as ET
from zipfile import ZipFile
from pathlib import Path
import json, re, collections
ROOT = Path(__file__).resolve().parents[1]
p = json.loads((ROOT / 'progress.json').read_text())
z = ZipFile(ROOT / 'source' / 'The_Claiming_Moon.epub')
M = ['The_Claiming_Moon_split_%03d.xhtml' % i for i in range(48)]
B = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'pre', 'div', 'section', 'article', 'aside', 'blockquote', 'figcaption', 'td', 'th', 'dt', 'dd', 'caption', 'address', 'header', 'footer'}
C = B | {'body', 'ol', 'ul', 'table', 'tbody', 'thead', 'tfoot', 'tr', 'dl', 'main', 'figure', 'nav'}

def tag(n):
    return n.tag.rsplit('}', 1)[-1]

def getbl(path):
    root = ET.fromstring(z.read(path))
    body = next((n for n in root.iter() if tag(n) == 'body'))
    out = []

    def go(n):
        a = tag(n)
        c = [x for x in n if tag(x) in C]
        if a in B and (not c):
            if ''.join(n.itertext()).strip() or any((tag(x) in ('img', 'br', 'hr') for x in n.iter())):
                out.append(n)
            return
        for x in n:
            go(x)
    go(body)
    return out

def trans(i):
    s = (ROOT / p['chapters'][i]['translation_path']).read_text()
    return [x.strip() for x in re.split('\\n\\s*\\n', s) if x.strip()]
if __name__ == '__main__':
    for i in range(48):
        b = getbl(M[i])
        t = trans(i)
        print('%2d src %5d ru %5d delta %+4d / lens %7d/%7d' % (i + 1, len(b), len(t), len(t) - len(b), sum((len(''.join(x.itertext())) for x in b)), sum((len(x) for x in t))))
    for i in [0, 1, 2, 16, 27, 32, 47]:
        print('\n=== %d ===' % (i + 1))
        b = getbl(M[i])
        t = trans(i)
        for k in range(min(21, len(b), len(t))):
            print(k, '%-5s' % tag(b[k]), repr(''.join(b[k].itertext()).strip()[:85]), ' / ', repr(t[k][:90]))
