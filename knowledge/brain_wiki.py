#!/usr/bin/env python3
"""
brain_wiki.py — 把 vault 渲染成本機 wiki（knowledge/wiki/，gitignore，零網路）。

  wiki/index.html            入口兼 dashboard（內嵌 JSON，vanilla JS 過濾/搜尋）
  wiki/<family>/<name>.html  每則筆記一頁，[[wiki-link]] → 可點相對連結
  wiki/entities/*.html       entity hub（導覽骨幹）
  wiki/themes/*.html         theme hub
  wiki/assets/wiki.css       共用樣式

用法：python knowledge/brain_wiki.py [--full]
增量：.md mtime 比對應 .html 新才重渲染（--full 全量）。
通常由 brain_build.py 自動呼叫，不需手動跑。
"""
import html as html_mod
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import markdown

KDIR = Path(__file__).resolve().parent
REPO = KDIR.parent
VAULT = KDIR / "vault"
WIKI = KDIR / "wiki"
CACHE = KDIR / "brain_cache.json"

CSS = """
:root{--bg:#f8fafc;--card:#fff;--ink:#1e293b;--sub:#64748b;--line:#e2e8f0;
--accent:#2563eb;--badge:#eff6ff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font-family:'Inter','Noto Sans TC',-apple-system,'Segoe UI',sans-serif;
font-size:15px;line-height:1.75}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
a.dead{color:#94a3b8;pointer-events:none}
.top{background:linear-gradient(135deg,#0f172a,#1e293b);color:#fff;
padding:.65rem 20px;font-size:13px;position:sticky;top:0;z-index:10}
.top a{color:rgba(255,255,255,.85)}
.top b{font-weight:700}
main{max-width:900px;margin:0 auto;padding:24px 20px 60px}
.info{background:var(--card);border:1px solid var(--line);border-radius:8px;
padding:10px 16px;font-size:13px;color:var(--sub);margin:14px 0 22px;
display:flex;gap:14px;flex-wrap:wrap}
.info b{color:var(--ink)}
.badge{background:var(--badge);color:var(--accent);border-radius:4px;
padding:1px 8px;font-weight:600}
h1{font-size:1.45rem;line-height:1.4;letter-spacing:-.01em}
h2{font-size:1.12rem;border-bottom:2px solid var(--line);padding-bottom:6px;
margin-top:2em}
article{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:8px 30px 26px}
/* index */
.controls{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0;align-items:center}
.controls input{flex:1;min-width:240px;padding:9px 14px;border:1px solid var(--line);
border-radius:8px;font-size:14px;background:var(--card)}
.pill{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:4px 13px;font-size:12.5px;cursor:pointer;color:var(--sub);user-select:none}
.pill.on{background:var(--accent);border-color:var(--accent);color:#fff}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;
padding:10px 16px;margin:8px 0}
.card .t{font-weight:600}
.card .m{font-size:12.5px;color:var(--sub);margin-top:2px}
.card .o{font-size:13px;color:#334155;margin-top:4px}
.cnt{color:var(--sub);font-size:13px;margin:8px 0}
@media(prefers-color-scheme:dark){
:root{--bg:#0f172a;--card:#1e293b;--ink:#e2e8f0;--sub:#94a3b8;--line:#334155;
--badge:#1e3a5f}
.card .o{color:#cbd5e1}}
"""

PAGE = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · 第二大腦</title>
<link rel="stylesheet" href="{root}assets/wiki.css"></head>
<body><div class="top"><a href="{root}index.html">🧠 <b>第二大腦</b></a> · 本機 wiki（未發布）</div>
<main><div class="info">{info}</div><article>{body}</article></main></body></html>"""

WIKILINK = re.compile(r"\[\[([^\[\]|]+)(?:\|([^\[\]]+))?\]\]")


def load_summaries():
    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    return [n for ent in cache["files"].values() for n in ent.get("notes", [])]


def collect_md():
    """vault/auto + vault/notes 的全部 .md → {vault 相對路徑: Path}"""
    out = {}
    for sub in ("auto", "notes"):
        base = VAULT / sub
        if base.is_dir():
            for p in base.rglob("*.md"):
                out[str(p.relative_to(VAULT))] = p
    return out


def stem_map(md_files):
    """[[link]] 解析：檔名 stem → wiki 相對 html 路徑（同 Obsidian 檔名解析）。"""
    m = {}
    for rel in md_files:
        m.setdefault(Path(rel).stem, rel[:-3] + ".html")
    return m


def parse_note(text):
    fm = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].splitlines():
                mm = re.match(r"(\w[\w-]*):\s*(.*)", line)
                if mm:
                    v = mm.group(2).strip()
                    if v.startswith('"') and v.endswith('"'):
                        try:
                            v = json.loads(v)
                        except json.JSONDecodeError:
                            v = v.strip('"')
                    fm[mm.group(1)] = v
            body = parts[2]
    return fm, body.strip()


def render_page(rel_md, path, stems):
    fm, body = parse_note(path.read_text(encoding="utf-8"))
    depth = rel_md.count("/")
    root = "../" * depth

    def linkify(m):
        target, label = m.group(1).strip(), m.group(2) or m.group(1)
        hit = stems.get(target) or stems.get(Path(target).name)
        if hit:
            return f'<a href="{root}{hit}">{html_mod.escape(label)}</a>'
        return f'<span class="dead">{html_mod.escape(label)}</span>'

    # 先把 [[link]] 換成 HTML anchor 再走 markdown（md 不會動已存在的 tag）
    body = WIKILINK.sub(linkify, body)
    body_html = markdown.markdown(body, extensions=["nl2br"])

    info = [f'<span class="badge">{html_mod.escape(fm.get("type", "note"))}</span>']
    for k, label in (("date", ""), ("verdict", "裁決 "), ("grade", "評級 "),
                     ("entity", ""), ("theme", "")):
        if fm.get(k):
            info.append(f"<span>{label}<b>{html_mod.escape(str(fm[k]))}</b></span>")
    src = fm.get("source", "")
    if src:
        if src.startswith("docs/"):
            href = os.path.relpath(REPO / src, (WIKI / rel_md).parent)
            info.append(f'<a href="{href}">原始報告</a>')
        else:
            info.append(f"<span>來源 {html_mod.escape(src)}</span>")
    if fm.get("url"):
        info.append(f'<a href="{html_mod.escape(fm["url"])}">線上版</a>')

    out = WIKI / (rel_md[:-3] + ".html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PAGE.format(
        title=html_mod.escape(fm.get("title", Path(rel_md).stem)),
        root=root, info=" · ".join(info), body=body_html), encoding="utf-8")


INDEX = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>第二大腦 · 本機 wiki</title>
<link rel="stylesheet" href="assets/wiki.css"></head>
<body><div class="top">🧠 <b>第二大腦</b> · 本機 wiki（未發布） · as of %%ASOF%%</div>
<main>
<h1>第二大腦</h1>
<p style="color:var(--sub);font-size:13.5px">%%COUNTS%%；深度全文搜尋用
<code>python knowledge/q.py --search "…"</code></p>
<div class="controls"><input id="q" placeholder="搜 title / ticker / 主題 / oneliner / tags…">
<span class="pill on" data-t="*">全部</span>%%PILLS%%</div>
<div class="cnt" id="cnt"></div>
<div id="list"></div>
<script id="brain-data" type="application/json">%%DATA%%</script>
<script>
const DATA = JSON.parse(document.getElementById('brain-data').textContent);
DATA.sort((a,b)=>(b.d||'').localeCompare(a.d||''));
let type='*', q='';
const list=document.getElementById('list'), cnt=document.getElementById('cnt');
function esc(s){const d=document.createElement('span');d.textContent=s||'';return d.innerHTML}
function render(){
  const ql=q.toLowerCase();
  const rows=DATA.filter(n=>(type==='*'||n.t===type)&&(!ql||n.s.indexOf(ql)>=0));
  cnt.textContent=rows.length+' / '+DATA.length+' 筆';
  list.innerHTML=rows.slice(0,400).map(n=>
    '<div class="card"><div class="t"><a href="'+n.p+'">'+esc(n.title)+'</a></div>'+
    '<div class="m"><span class="badge">'+esc(n.t)+'</span> '+esc(n.d||'')+
    (n.v?' · <b>'+esc(n.v)+'</b>':'')+(n.k?' · '+esc(n.k):'')+'</div>'+
    (n.one?'<div class="o">'+esc(n.one)+'</div>':'')+'</div>').join('')+
    (rows.length>400?'<div class="cnt">…僅顯示前 400 筆，請縮小條件</div>':'');
}
document.getElementById('q').addEventListener('input',e=>{q=e.target.value;render()});
document.querySelectorAll('.pill').forEach(p=>p.addEventListener('click',()=>{
  document.querySelectorAll('.pill').forEach(x=>x.classList.remove('on'));
  p.classList.add('on');type=p.dataset.t;render()}));
render();
</script></main></body></html>"""


def build_index(summaries, stems):
    data = []
    for s in summaries:
        stem = Path(s["note"]).stem
        p = stems.get(stem)
        if not p:
            continue
        hay = " ".join(str(x) for x in (
            s.get("title"), s.get("entity"), s.get("theme"), s.get("oneliner"),
            " ".join(s.get("tags") or []), s.get("verdict"), s.get("id"))).lower()
        data.append({"title": s.get("title") or stem, "t": s["type"],
                     "d": s.get("date"), "v": s.get("verdict") or s.get("grade"),
                     "k": s.get("entity") or s.get("theme"),
                     "one": (s.get("oneliner") or "")[:160], "p": p, "s": hay})
    types = sorted({n["t"] for n in data})
    pills = "".join(f'<span class="pill" data-t="{t}">{t}</span>' for t in types)
    counts = f"{len(data)} 則筆記 · {len(types)} 類 · vault: knowledge/vault/ · 全部本地"
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (WIKI / "index.html").write_text(
        INDEX.replace("%%ASOF%%", date.today().isoformat())
             .replace("%%COUNTS%%", counts).replace("%%PILLS%%", pills)
             .replace("%%DATA%%", payload), encoding="utf-8")


def main():
    full = "--full" in sys.argv[1:]
    if not CACHE.exists():
        print("brain_cache.json 不存在，先跑 brain_build.py")
        sys.exit(1)
    summaries = load_summaries()
    md_files = collect_md()
    stems = stem_map(md_files)

    (WIKI / "assets").mkdir(parents=True, exist_ok=True)
    css = WIKI / "assets" / "wiki.css"
    if full or not css.exists() or css.read_text(encoding="utf-8") != CSS:
        css.write_text(CSS, encoding="utf-8")

    n_render, n_skip = 0, 0
    for rel_md, p in sorted(md_files.items()):
        out = WIKI / (rel_md[:-3] + ".html")
        if not full and out.exists() and out.stat().st_mtime >= p.stat().st_mtime:
            n_skip += 1
            continue
        try:
            render_page(rel_md, p, stems)
            n_render += 1
        except Exception as e:
            print(f"  WARN wiki render {rel_md}: {e}")

    # 孤兒 wiki 頁清理（來源 md 已刪）
    n_pruned = 0
    for hp in WIKI.rglob("*.html"):
        rel = str(hp.relative_to(WIKI))
        if rel == "index.html":
            continue
        if rel[:-5] + ".md" not in md_files:
            hp.unlink()
            n_pruned += 1

    build_index(summaries, stems)
    print(f"📖 wiki: {n_render} rendered, {n_skip} cached, {n_pruned} pruned "
          f"→ open {WIKI / 'index.html'}")


if __name__ == "__main__":
    main()
