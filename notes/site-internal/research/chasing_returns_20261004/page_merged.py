"""Assemble the merged page: R/merged/00_top.html ... 08_method.html + frags_merged.json -> merged.html.

    python3 page_merged.py [--templates DIR] [--out FILE]

Hard errors: unknown {{key}}, a key used twice, any of the frags_merged.json keys unused,
or a missing template file. merged.html is a complete standalone page; the site wrapper
(scripts/build_chasing_returns.py) takes the <style>, <script> and the part between the
BODY START / BODY END comments.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = ['00_top', '01_now', '02_q1', '03_q2', '04_q3', '05_q4', '06_oos', '07_tw', '08_method']
TITLE = '漲多了還能追嗎 | InvestMQuest Research'

HASH_SCRIPT = r'''<script>
(function(){
  // old anchors that no longer have a section of their own go to the top of the page
  var LEGACY={synth:1,update:1,pos:'now'};
  function go(){
    var h=decodeURIComponent((location.hash||'').slice(1));
    if(!h)return;
    var el=document.getElementById(h);
    if(!el&&LEGACY[h]===1){setTimeout(function(){window.scrollTo(0,0);},0);return;}
    if(!el&&LEGACY[h])el=document.getElementById(LEGACY[h]);
    if(!el)return;
    for(var n=el;n;n=n.parentElement){if(n.tagName==='DETAILS')n.open=true;}
    setTimeout(function(){el.scrollIntoView();},0);
  }
  window.addEventListener('hashchange',go);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
</script>'''


def assemble(tdir, frags):
    texts = []
    for n in NAMES:
        p = Path(tdir) / f'{n}.html'
        if not p.exists():
            sys.exit(f'missing template: {p}')
        texts.append(p.read_text(encoding='utf-8'))
    body = '\n'.join(texts)
    used = {}
    errors = []

    def sub(m):
        k = m.group(1)
        if k not in frags:
            errors.append(f'unknown key {{{{{k}}}}}')
            return m.group(0)
        used[k] = used.get(k, 0) + 1
        return frags[k]
    # fragments are inserted verbatim; scan only the template text (single pass, no re-scan)
    body = re.sub(r'\{\{\s*(\w+)\s*\}\}', sub, body)
    errors += [f'key used {c} times: {k}' for k, c in used.items() if c > 1]
    errors += [f'key never used: {k}' for k in frags if k not in used]
    return body, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--templates', default=str(HERE / 'merged'))
    ap.add_argument('--out', default=str(HERE / 'merged.html'))
    a = ap.parse_args()
    frags = json.load(open(HERE / 'frags_merged.json', encoding='utf-8'))
    body, errors = assemble(a.templates, frags)
    if errors:
        print('\n'.join('ERROR ' + e for e in errors), file=sys.stderr)
        sys.exit(1)
    css = (HERE / 'merged_css.txt').read_text(encoding='utf-8')
    tip = (HERE / 'v2_script.txt').read_text(encoding='utf-8')
    html = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<style id="chasing-merged-css">
{css}</style>
</head>
<body>
<h1 class="standalone-title">漲多了還能追嗎</h1>
<!-- BODY START -->
{body}
<!-- BODY END -->
{tip}
{HASH_SCRIPT}
</body>
</html>
'''
    Path(a.out).write_text(html, encoding='utf-8')
    print(f'merged.html: {len(html):,} bytes, {len(frags)} fragments filled -> {a.out}')


if __name__ == '__main__':
    main()
