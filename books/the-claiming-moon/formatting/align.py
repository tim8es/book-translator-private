from __future__ import annotations
from pathlib import Path
import re, math, json, collections, time
from analyze import getbl, tag, trans, M, ROOT, p

def clean(s):
    return re.sub('(?m)^\\s*#{1,6}\\s*|\\*\\*|(?<!\\w)\\*(?!\\*)|`|\\s+', ' ', s).strip()

def lens(seq):
    return [max(1, len(clean(s))) for s in seq]

def align(i, *, band=120, trace=False):
    blocks = getbl(M[i])
    rus = trans(i)
    eng = [''.join(x.itertext()).strip() for x in blocks]
    n, m = (len(eng), len(rus))
    e = lens(eng)
    r = lens(rus)
    ratio = sum(r) / max(1, sum(e))
    ee = [0]
    rr = [0]
    for x in e:
        ee.append(ee[-1] + x)
    for x in r:
        rr.append(rr[-1] + x)
    dp = {(0, 0): 0.0}
    prev = {}

    def metric(a, b, c, d):
        x = ee[b] - ee[a] + (b - a - 1) * 1
        y = rr[d] - rr[c] + (d - c - 1) * 1
        diff = abs(math.log((y + 15) / (ratio * x + 15)))
        return min(4.0, diff) ** 2 * 0.93
    for a in range(n + 1):
        center = round(a * m / max(1, n))
        lo = max(0, center - band) if a else 0
        hi = min(m, center + band)
        for c in range(lo, hi + 1):
            key = (a, c)
            if key not in dp:
                continue
            curr = dp[key]

            def upd(b, d, cost):
                key = (b, d)
                potential = curr + cost
                if potential < dp.get(key, 1e+100):
                    dp[key] = potential
                    prev[key] = (a, c)
            if a < n and c < m:
                penalty = 1 if not eng[a] else 0
                upd(a + 1, c + 1, metric(a, a + 1, c, c + 1) + penalty)
            if a < n and c + 1 < m:
                upd(a + 1, c + 2, 0.54 + metric(a, a + 1, c, c + 2))
                if c + 2 < m:
                    upd(a + 1, c + 3, 1.15 + metric(a, a + 1, c, c + 3))
            if a + 1 < n and c < m:
                upd(a + 2, c + 1, 0.66 + metric(a, a + 2, c, c + 1))
            if a < n:
                upd(a + 1, c, 0.03 if not eng[a] else 1.8 + min(3, e[a] / 100.0))
            if c < m:
                upd(a, c + 1, 2.2 + min(2, r[c] / 120.0))
    if (n, m) not in dp:
        return {'error': f'cannot align n={n},m={m}'}
    route = []
    at = (n, m)
    while at != (0, 0):
        start = prev[at]
        route.append((start[0], at[0], start[1], at[1]))
        at = start
    route.reverse()
    counter = collections.Counter(((b - a, d - c) for a, b, c, d in route))
    result = {'i': i + 1, 'n': n, 'm': m, 'cost': round(dp[n, m], 2), 'moves': {str(k): v for k, v in counter.items()}, 'route': route}
    if trace:
        for a, b, c, d in route[:80]:
            print(f'{a:03d}:{b:03d} {c:03d}:{d:03d}', repr(eng[a][:60] if a < n else ''), '|', repr(rus[c][:60] if c < m else ''))
    return result
if __name__ == '__main__':
    out = []
    start = time.time()
    for i in range(48):
        v = align(i)
        out.append(v)
        print('%2d' % (i + 1), 'src', v.get('n'), 'ru', v.get('m'), 'cost', v.get('cost'), v.get('moves', v.get('error')), flush=True)
    Path(__file__).with_name('routes.json').write_text(json.dumps(out, ensure_ascii=False))
    print('elapsed', time.time() - start)
