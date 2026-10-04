"""Checks for the merged page. Report to stdout, exit 1 on hard failures.

    python3 check_merged.py [--templates DIR]

Hard failures:  (a) numbers in the new prose that appear nowhere in the originals,
                (b) forbidden strings in visible prose,
                (e) duplicate / missing details.angle ids, unresolved href="#...".
Listed only:    (a') numbers in the originals' prose missing from merged.html,
                (c) CJK followed by a half-width , . : ; (,
                (d) metaphor words (zh-analyst-prose rule 13).
"Prose" = template text with the {{key}} placeholders (the data fragments) removed.
"""
import argparse, html, json, re, sys
from pathlib import Path
import page_merged

HERE = Path(__file__).resolve().parent
NUM = re.compile(r'\d+(?:\.\d+)?')
FORBIDDEN = ['追問', '續篇', '第一版', '第二版', '本頁', '本報告']
METAPHOR = ['吹出', '煞車', '天花板', '柱子', '震央', '癒合', '扛著', '甩開', '雪崩', '閘門', '藥方', '天平', '聽話', '鏡像', '同一張牌', '拆柱子']


def text(s):
    s = re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)


def nums(s):
    return set(NUM.findall(s))


def numpat(n):
    return r'(?<![\d.])' + re.escape(n) + r'(?!\d)'


def snippet(s, pat, w=18):
    out = []
    for m in re.finditer(pat, s):
        out.append(re.sub(r'\s+', ' ', s[max(0, m.start() - w):m.end() + w]))
        if len(out) >= 3:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--templates', default=str(HERE / 'merged'))
    a = ap.parse_args()
    frags = json.load(open(HERE / 'frags_merged.json', encoding='utf-8'))
    hard = []

    # --- new prose (templates without placeholders) and the assembled page
    raw = '\n'.join((Path(a.templates) / f'{n}.html').read_text(encoding='utf-8') for n in page_merged.NAMES)
    prose_html = re.sub(r'\{\{\s*\w+\s*\}\}', ' ', raw)
    prose = text(prose_html)
    full_html, errs = page_merged.assemble(a.templates, frags)
    hard += errs
    full_text = text(full_html)

    # --- originals
    src_all = set()
    for f in ['chasing.html', 'followups.html', 'page_v2.py', 'page_f.py', 'frags_tw.py']:
        src_all |= nums(text((HERE / f).read_text(encoding='utf-8')) if f.endswith('.html') else re.sub(r'<[^>]+>', ' ', html.unescape((HERE / f).read_text(encoding='utf-8'))))
    orig_prose = ''
    for f in ['chasing.html', 'followups.html']:
        h = (HERE / f).read_text(encoding='utf-8')
        h = h[h.index('<div class="page">'):]
        for v in sorted(frags.values(), key=len, reverse=True):
            h = h.replace(v, ' ')
        orig_prose += text(h) + '\n'

    # (a) numbers
    new_only = sorted(nums(prose) - src_all, key=float)
    print(f'(a) numbers in new prose not found in the originals: {len(new_only)}')
    for n in new_only:
        print(f'    {n}: ...{" | ".join(snippet(prose, numpat(n)))}...')
        hard.append(f'new number {n}')
    missing = sorted(nums(orig_prose) - nums(full_text), key=float)
    print(f"(a') numbers in the originals' prose absent from merged.html: {len(missing)}")
    for n in missing:
        print(f'    {n}: ...{" | ".join(snippet(orig_prose, numpat(n)))}...')

    # (b) forbidden
    pat = '|'.join(FORBIDDEN + [r'Q[1-4]'])
    hits = snippet(prose, pat, 12)
    allhits = [m.group(0) for m in re.finditer(pat, prose)]
    print(f'(b) forbidden strings in visible prose: {len(allhits)}')
    for s in hits:
        print('    ...' + s + '...')
    if allhits:
        hard.append('forbidden strings')

    # (c) half-width punctuation after CJK
    c = [re.sub(r'\s+', ' ', prose[max(0, m.start() - 10):m.end() + 10]) for m in re.finditer(r'[一-鿿][,.:;(]', prose)]
    print(f'(c) CJK followed by half-width , . : ; ( : {len(c)}')
    for s in c[:20]:
        print('    ...' + s + '...')

    # (d) metaphors
    d = [(w, prose.count(w)) for w in METAPHOR if w in prose]
    print(f'(d) metaphor words: {d if d else 0}')

    # (e) ids and anchors
    ids = re.findall(r'<details[^>]*class="[^"]*\bangle\b[^"]*"[^>]*>', full_html)
    angle_ids = [m.group(1) if (m := re.search(r'\bid="([^"]+)"', t)) else None for t in ids]
    noid = angle_ids.count(None)
    dup = sorted({i for i in angle_ids if i and angle_ids.count(i) > 1})
    allids = set(re.findall(r'\bid="([^"]+)"', full_html))
    bad = sorted({h for h in re.findall(r'href="#([^"]*)"', full_html) if h and h not in allids})
    print(f'(e) details.angle: {len(angle_ids)}, without id: {noid}, duplicate ids: {dup}, unresolved #hrefs: {bad}')
    if noid or dup or bad:
        hard.append('ids/anchors')
    # ids the old URLs and the toc rely on
    need = ['now', 'q1', 'q2', 'q3', 'q4', 'oos', 'tw', 'method', 'q1-h', 'q1-i', 'q1-j', 'q2-i', 'q3-j']
    miss = [i for i in need if i not in allids]
    print(f'(e) anchor ids needed by redirects/toc but absent: {miss}')
    if miss:
        hard.append('missing redirect targets')

    print('\nHARD FAILURES:' if hard else '\nno hard failures', *hard, sep='\n  ')
    sys.exit(1 if hard else 0)


if __name__ == '__main__':
    main()
