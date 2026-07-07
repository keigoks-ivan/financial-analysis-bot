#!/usr/bin/env python3
"""
brain_wiki.py — 把 vault 渲染成本機 wiki（knowledge/wiki/，gitignore，零網路）。

v2（人本化改版）：
  wiki/index.html            四入口首頁：最近更新 / 個股導航 / 主題地圖 / 閒讀書架 ＋ 全庫搜尋
  wiki/<family>/<name>.html  檔案卡式內頁：重點（裁決/oneliner/關鍵欄）＋大按鈕直連原始報告，
                             抽取全文收進折疊區（人讀原稿、wiki 負責導航與互連）
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
GRAPH = KDIR / "graph.json"

# 有「排版完整原稿」的類型 → 內頁做檔案卡，全文折疊；md 原生類型直接排全文
STYLED_TYPES = {"dd", "dca", "id", "earnings", "comparison", "synthesis",
                "monitor", "supplychain", "briefing", "weekly", "qgm",
                "tools", "property"}

VERDICT_CLS = {"進場": "v-go", "觀望": "v-hold", "迴避": "v-avoid"}

TYPE_LABEL = {
    "dd": "個股 DD", "dca": "DCA（legacy）", "id": "產業 ID", "earnings": "財報",
    "comparison": "多股對比", "synthesis": "期望綜合", "monitor": "跨資產監測",
    "supplychain": "供應鏈", "briefing": "晨報", "weekly": "週報", "qgm": "QGM",
    "strategy": "策略規則", "internal-note": "內部筆記", "whitepaper": "白皮書",
    "repo-doc": "repo 文件", "tools": "置產/史詩", "property": "大馬房產",
    "entity": "個股", "theme": "主題",
}

CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#1e293b;--sub:#64748b;--line:#e2e8f0;
--accent:#2563eb;--badge:#eff6ff;--go:#16a34a;--hold:#d97706;--avoid:#dc2626}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font-family:'Inter','Noto Sans TC',-apple-system,'Segoe UI',sans-serif;
font-size:15px;line-height:1.75}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
a.dead{color:#94a3b8;pointer-events:none}
.top{background:linear-gradient(135deg,#0f172a,#1e293b);color:#fff;
padding:.65rem 20px;font-size:13px;position:sticky;top:0;z-index:10;
display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.top a{color:rgba(255,255,255,.85)}
.top b{font-weight:700}
main{max-width:960px;margin:0 auto;padding:24px 20px 60px}
h1{font-size:1.42rem;line-height:1.4;letter-spacing:-.01em;margin:.4em 0}
h2{font-size:1.1rem;border-bottom:2px solid var(--line);padding-bottom:6px;margin-top:2em}
.badge{background:var(--badge);color:var(--accent);border-radius:4px;
padding:1px 8px;font-weight:600;font-size:12px}
.chip{display:inline-block;border:1px solid var(--line);background:var(--card);
border-radius:6px;padding:2px 9px;font-size:12.5px;margin:2px}
.v-go{color:var(--go);font-weight:700}.v-hold{color:var(--hold);font-weight:700}
.v-avoid{color:var(--avoid);font-weight:700}
/* 檔案卡內頁 */
.filecard{background:var(--card);border:1px solid var(--line);border-radius:12px;
padding:20px 24px;margin:16px 0}
.filecard .meta{display:flex;gap:10px;flex-wrap:wrap;align-items:center;
font-size:13px;color:var(--sub);margin:8px 0}
.filecard .one{font-size:14.5px;color:#334155;background:var(--bg);
border-left:3px solid var(--accent);padding:10px 14px;border-radius:0 8px 8px 0;
margin:12px 0}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 4px}
.btn{display:inline-block;background:var(--accent);color:#fff!important;
border-radius:8px;padding:8px 18px;font-weight:600;font-size:14px}
.btn:hover{text-decoration:none;opacity:.92}
.btn.sec{background:var(--card);color:var(--accent)!important;
border:1px solid var(--accent)}
.linksrow{font-size:13.5px;margin:10px 0;color:var(--sub)}
article{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:8px 28px 24px;margin-top:14px}
details.fulltext{margin-top:14px}
details.fulltext>summary{cursor:pointer;background:var(--card);
border:1px dashed var(--line);border-radius:10px;padding:12px 18px;
color:var(--sub);font-size:13.5px;user-select:none}
details.fulltext[open]>summary{border-bottom-left-radius:0;border-bottom-right-radius:0}
details.fulltext>div{background:var(--card);border:1px dashed var(--line);
border-top:none;border-radius:0 0 10px 10px;padding:4px 28px 22px}
/* 首頁 */
.search{width:100%;padding:11px 16px;border:1px solid var(--line);
border-radius:10px;font-size:15px;background:var(--card);margin:14px 0 6px}
.secnav{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 4px;font-size:13px}
.secnav a{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:4px 14px;color:var(--sub)}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;
padding:10px 16px;margin:8px 0}
.card .t{font-weight:600}
.card .m{font-size:12.5px;color:var(--sub);margin-top:2px}
.card .o{font-size:13px;color:#334155;margin-top:4px}
.cnt{color:var(--sub);font-size:13px;margin:8px 0}
.tickgrid{line-height:2.1}
.tickgrid a{display:inline-block;border:1px solid var(--line);background:var(--card);
border-radius:6px;padding:1px 9px;font-size:13px;margin:2px;font-weight:600}
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px}
.shelf .card{margin:0}
.pill{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:4px 13px;font-size:12.5px;cursor:pointer;color:var(--sub);user-select:none;
display:inline-block;margin:2px}
.pill.on{background:var(--accent);border-color:var(--accent);color:#fff}
.subh{font-size:13px;color:var(--sub);font-weight:600;margin:14px 0 6px}
@media(prefers-color-scheme:dark){
:root{--bg:#0f172a;--card:#1e293b;--ink:#e2e8f0;--sub:#94a3b8;--line:#334155;
--badge:#1e3a5f;--go:#4ade80;--hold:#fbbf24;--avoid:#f87171}
.card .o,.filecard .one{color:#cbd5e1}}
"""

PAGE = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · 第二大腦</title>
<link rel="stylesheet" href="{root}assets/wiki.css"></head>
<body><div class="top"><a href="{root}index.html">🧠 <b>第二大腦</b></a>
<span>本機 wiki（未發布）</span></div>
<main>{content}</main></body></html>"""

WIKILINK = re.compile(r"\[\[([^\[\]|]+)(?:\|([^\[\]]+))?\]\]")


def _safe_name(s):
    """與 brain_build.py 同一條檔名規則（theme hub 檔名對齊用）。"""
    import unicodedata
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r'[\\/:*?"<>|\s]+', "_", s).strip("_") or "untitled"


def esc(s):
    return html_mod.escape(str(s))


def load_summaries():
    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    return [n for ent in cache["files"].values() for n in ent.get("notes", [])]


def collect_md():
    out = {}
    for sub in ("auto", "notes"):
        base = VAULT / sub
        if base.is_dir():
            for p in base.rglob("*.md"):
                out[str(p.relative_to(VAULT))] = p
    return out


def stem_map(md_files):
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
    ntype = fm.get("type", "note")

    def linkify(m):
        target, label = m.group(1).strip(), m.group(2) or m.group(1)
        hit = stems.get(target) or stems.get(Path(target).name)
        if hit:
            return f'<a href="{root}{hit}">{esc(label)}</a>'
        return f'<span class="dead">{esc(label)}</span>'

    body = WIKILINK.sub(linkify, body)
    # 內頁第一個 h1 與檔案卡重複 → 拿掉
    body = re.sub(r"^#\s+.*\n?", "", body, count=1)
    body_html = markdown.markdown(body, extensions=["nl2br"])

    # ── 檔案卡 ──
    v = fm.get("verdict", "")
    vcls = VERDICT_CLS.get(v, "")
    meta = [f'<span class="badge">{esc(TYPE_LABEL.get(ntype, ntype))}</span>']
    if fm.get("date"):
        meta.append(f"<span>{esc(fm['date'])}</span>")
    if v:
        meta.append(f'<span class="{vcls}">裁決：{esc(v)}</span>')
    if fm.get("grade"):
        meta.append(f"<span>評級 <b>{esc(fm['grade'])}</b></span>")
    for k, label in (("entity", ""), ("theme", ""), ("archetype", ""),
                     ("dca_role", ""), ("moat_trend", "護城河 "),
                     ("long_term_confidence", "信心 "), ("schema", "")):
        if fm.get(k):
            meta.append(f'<span class="chip">{label}{esc(fm[k])}</span>')

    one = f'<div class="one">{esc(fm["oneliner"])}</div>' if fm.get("oneliner") else ""

    actions = []
    src = fm.get("source", "")
    if src.startswith("docs/"):
        href = os.path.relpath(REPO / src, (WIKI / rel_md).parent)
        actions.append(f'<a class="btn" href="{href}">📄 開原始報告</a>')
    elif src.startswith("~/"):
        href = "file://" + esc(str(Path(src).expanduser()))
        actions.append(f'<a class="btn" href="{href}">📄 開原始檔</a>')
    if fm.get("url"):
        actions.append(f'<a class="btn sec" href="{esc(fm["url"])}">🌐 線上版</a>')
    ent = fm.get("entity")
    if ent and stems.get(ent):
        actions.append(f'<a class="btn sec" href="{root}{stems[ent]}">個股 hub：{esc(ent)}</a>')
    actions_html = f'<div class="actions">{"".join(actions)}</div>' if actions else ""

    card = (f'<div class="filecard"><h1>{esc(fm.get("title", Path(rel_md).stem))}</h1>'
            f'<div class="meta">{" · ".join(meta)}</div>{one}{actions_html}</div>')

    # ── 正文：有排版原稿的類型 → 全文折疊；md 原生 / hub → 直接排 ──
    if ntype in STYLED_TYPES:
        content = (card +
                   '<details class="fulltext"><summary>展開抽取全文'
                   '（純文字備份，建議直接開原始報告）</summary>'
                   f"<div>{body_html}</div></details>")
    else:
        content = card + f"<article>{body_html}</article>"

    out = WIKI / (rel_md[:-3] + ".html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PAGE.format(title=esc(fm.get("title", Path(rel_md).stem)),
                               root=root, content=content), encoding="utf-8")


# ─────────────────────────── 首頁 ───────────────────────────

INDEX = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>第二大腦 · 本機 wiki</title>
<link rel="stylesheet" href="assets/wiki.css"></head>
<body><div class="top">🧠 <b>第二大腦</b><span>本機 wiki（未發布） · as of %%ASOF%% ·
%%NCOUNT%% 則筆記</span></div>
<main>
<input class="search" id="q" placeholder="全庫搜：ticker / 主題 / 標題 / oneliner…（深度全文用 q.py --search）">
<div class="secnav"><a href="#recent">🕐 最近更新</a><a href="#stocks">📈 個股導航</a>
<a href="#themes">🗺 主題地圖</a><a href="#shelf">📚 閒讀書架</a><a href="#all">全部</a></div>
<div id="qresults"></div>

<h2 id="recent">🕐 最近更新</h2>
<div id="recentlist"></div>

<h2 id="stocks">📈 個股導航 <span class="cnt">點 ticker 進 hub（現裁決＋決策史＋全部報告）</span></h2>
<div class="subh v-go">進場</div><div class="tickgrid" id="tk-go"></div>
<div class="subh v-hold">觀望</div><div class="tickgrid" id="tk-hold"></div>
<div class="subh v-avoid">迴避</div><div class="tickgrid" id="tk-avoid"></div>
<details><summary class="cnt">其他（無 v13+ 裁決 / 僅產業圖引用）</summary>
<div class="tickgrid" id="tk-rest"></div></details>

<h2 id="themes">🗺 主題地圖</h2>
<div class="subh">產業 ID</div><div class="tickgrid" id="th-id"></div>
<div class="subh">供應鏈</div><div class="tickgrid" id="th-sc"></div>

<h2 id="shelf">📚 閒讀書架</h2>
<div class="subh">🏛 城市與國家史詩（%%NEPIC%%）</div><div class="shelf" id="sh-epic"></div>
<details><summary class="cnt">全部史詩…</summary><div class="shelf" id="sh-epic-all"></div></details>
<div class="subh">📖 策略白皮書</div><div class="shelf" id="sh-wp"></div>
<div class="subh">🏠 置產工具（tools）／大馬房產</div><div class="shelf" id="sh-prop"></div>

<h2 id="all">全部筆記</h2>
<div>%%PILLS%%</div>
<div class="cnt" id="cnt"></div>
<div id="list"></div>

<script id="brain-data" type="application/json">%%DATA%%</script>
<script id="ent-data" type="application/json">%%ENT%%</script>
<script id="theme-data" type="application/json">%%THEMES%%</script>
<script>
const DATA=JSON.parse(document.getElementById('brain-data').textContent);
const ENT=JSON.parse(document.getElementById('ent-data').textContent);
const THEMES=JSON.parse(document.getElementById('theme-data').textContent);
DATA.sort((a,b)=>(b.d||'').localeCompare(a.d||''));
function e_(s){const d=document.createElement('span');d.textContent=s||'';return d.innerHTML}
function card(n){return '<div class="card"><div class="t"><a href="'+n.p+'">'+e_(n.title)+
'</a></div><div class="m"><span class="badge">'+e_(n.tl)+'</span> '+e_(n.d||'')+
(n.v?' · <b class="'+(n.vc||'')+'">'+e_(n.v)+'</b>':'')+(n.k?' · '+e_(n.k):'')+'</div>'+
(n.one?'<div class="o">'+e_(n.one)+'</div>':'')+'</div>'}

/* 最近更新：決策相關類型，最新 30 筆 */
const REC_T=new Set(['dd','id','earnings','comparison','synthesis','monitor','supplychain','internal-note']);
document.getElementById('recentlist').innerHTML=
  DATA.filter(n=>REC_T.has(n.t)&&n.d).slice(0,30).map(card).join('');

/* 個股導航 */
function tick(t){return '<a href="'+t.p+'">'+e_(t.k)+(t.g?' <span style="color:var(--sub);font-weight:400">'+e_(t.g)+'</span>':'')+'</a>'}
const grp={'進場':[],'觀望':[],'迴避':[],rest:[]};
ENT.forEach(t=>{(grp[t.v]||grp.rest).push(t)});
document.getElementById('tk-go').innerHTML=grp['進場'].map(tick).join('');
document.getElementById('tk-hold').innerHTML=grp['觀望'].map(tick).join('');
document.getElementById('tk-avoid').innerHTML=grp['迴避'].map(tick).join('');
document.getElementById('tk-rest').innerHTML=grp.rest.map(tick).join('');

/* 主題地圖 */
function theme(t){return '<a href="'+t.p+'">'+e_(t.name)+' <span style="color:var(--sub);font-weight:400">'+t.n+'</span></a>'}
document.getElementById('th-id').innerHTML=THEMES.filter(t=>t.k==='industry').map(theme).join('');
document.getElementById('th-sc').innerHTML=THEMES.filter(t=>t.k==='supplychain').map(theme).join('');

/* 書架 */
const epics=DATA.filter(n=>n.p.indexOf('kb/tools/history/')>=0);
document.getElementById('sh-epic').innerHTML=epics.slice(0,9).map(card).join('');
document.getElementById('sh-epic-all').innerHTML=epics.slice(9).map(card).join('');
document.getElementById('sh-wp').innerHTML=DATA.filter(n=>n.t==='whitepaper').map(card).join('');
document.getElementById('sh-prop').innerHTML=
  DATA.filter(n=>(n.t==='tools'&&n.p.indexOf('history/')<0)||n.t==='property').slice(0,60).map(card).join('');

/* 全部 + pills */
let type='*';
const list=document.getElementById('list'),cnt=document.getElementById('cnt');
function renderAll(){
  const rows=DATA.filter(n=>type==='*'||n.t===type);
  cnt.textContent=rows.length+' / '+DATA.length+' 筆';
  list.innerHTML=rows.slice(0,300).map(card).join('')+
    (rows.length>300?'<div class="cnt">…僅顯示前 300 筆</div>':'');
}
document.querySelectorAll('.pill').forEach(p=>p.addEventListener('click',()=>{
  document.querySelectorAll('.pill').forEach(x=>x.classList.remove('on'));
  p.classList.add('on');type=p.dataset.t;renderAll()}));
renderAll();

/* 全庫即時搜尋（頂欄）：ticker/主題 chips + 筆記卡 */
const qr=document.getElementById('qresults');
document.getElementById('q').addEventListener('input',e=>{
  const q=e.target.value.trim().toLowerCase();
  if(!q){qr.innerHTML='';return}
  const ents=ENT.filter(t=>t.k.toLowerCase().indexOf(q)>=0).slice(0,12);
  const ths=THEMES.filter(t=>t.name.toLowerCase().indexOf(q)>=0).slice(0,8);
  const notes=DATA.filter(n=>n.s.indexOf(q)>=0).slice(0,20);
  qr.innerHTML='<div class="card">'+
    (ents.length?'<div class="tickgrid">'+ents.map(tick).join('')+'</div>':'')+
    (ths.length?'<div class="tickgrid">'+ths.map(theme).join('')+'</div>':'')+
    '</div>'+notes.map(card).join('')+
    (notes.length?'':'<div class="cnt">筆記標題層無命中——內文全文請用 q.py --search</div>');
});
</script></main></body></html>"""


def build_index(summaries, stems):
    graph = json.loads(GRAPH.read_text(encoding="utf-8")) if GRAPH.exists() else {}
    data = []
    for s in summaries:
        stem = Path(s["note"]).stem
        p = stems.get(stem)
        if not p:
            continue
        hay = " ".join(str(x) for x in (
            s.get("title"), s.get("entity"), s.get("theme"), s.get("oneliner"),
            " ".join(s.get("tags") or []), s.get("verdict"), s.get("id"))).lower()
        v = s.get("verdict") or s.get("grade")
        data.append({"title": s.get("title") or stem, "t": s["type"],
                     "tl": TYPE_LABEL.get(s["type"], s["type"]),
                     "d": s.get("date"), "v": v,
                     "vc": VERDICT_CLS.get(v or "", ""),
                     "k": s.get("entity") or s.get("theme"),
                     "one": (s.get("oneliner") or "")[:160], "p": p, "s": hay})

    # 個股：graph company canonical（有 DD 裁決者優先分組）
    ents = []
    for n in graph.get("nodes", []):
        if n.get("type") != "company":
            continue
        page = stems.get(n["id"])
        if not page:
            continue
        c = n.get("canonical") or {}
        ents.append({"k": n["id"], "v": c.get("verdict") or "",
                     "g": c.get("fundamental_grade") or "", "p": page})
    ents.sort(key=lambda t: (t["g"] or "Z", t["k"]))

    # 主題：industry / supplychain 節點 + 成員數
    member_cnt = {}
    for e in graph.get("edges", []):
        member_cnt[e["to"]] = member_cnt.get(e["to"], 0) + 1
    themes = []
    for n in graph.get("nodes", []):
        if n.get("type") not in ("industry", "supplychain"):
            continue
        page = stems.get(f"Theme_{_safe_name(n['id'])}")
        if not page:
            continue
        themes.append({"name": n.get("title") or n["id"], "k": n["type"],
                       "n": member_cnt.get(n["id"], 0), "p": page})
    themes.sort(key=lambda t: -t["n"])

    n_epic = sum(1 for n in data if "kb/tools/history/" in n["p"])
    types = sorted({n["t"] for n in data})
    pills = '<span class="pill on" data-t="*">全部</span>' + "".join(
        f'<span class="pill" data-t="{t}">{TYPE_LABEL.get(t, t)}</span>' for t in types)

    def payload(obj):
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    (WIKI / "index.html").write_text(
        INDEX.replace("%%ASOF%%", date.today().isoformat())
             .replace("%%NCOUNT%%", str(len(data)))
             .replace("%%NEPIC%%", str(n_epic))
             .replace("%%PILLS%%", pills)
             .replace("%%DATA%%", payload(data))
             .replace("%%ENT%%", payload(ents))
             .replace("%%THEMES%%", payload(themes)), encoding="utf-8")


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
    css_changed = not css.exists() or css.read_text(encoding="utf-8") != CSS
    if css_changed:
        css.write_text(CSS, encoding="utf-8")
        full = True  # 樣板/樣式變了 → 全量重渲染

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
