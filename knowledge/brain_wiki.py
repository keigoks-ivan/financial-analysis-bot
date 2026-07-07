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
:root{--bg:#0a0e1a;--bg2:#0d1220;--card:rgba(19,26,46,.72);--cardsolid:#131a2e;
--ink:#e5eaf3;--sub:#8b98b3;--line:rgba(148,163,184,.14);--line2:rgba(148,163,184,.28);
--accent:#5ea0ff;--accent2:#a78bfa;--cyan:#22d3ee;
--go:#16a34a;--hold:#d97706;--avoid:#dc2626;
--go-t:#4ade80;--hold-t:#fbbf24;--avoid-t:#f87171;
--glow:0 0 24px rgba(94,160,255,.18);
--mono:'SF Mono','JetBrains Mono',ui-monospace,Menlo,monospace}
*{box-sizing:border-box}
::selection{background:rgba(94,160,255,.35)}
body{margin:0;color:var(--ink);font-size:15px;line-height:1.75;
font-family:'Inter','Noto Sans TC',-apple-system,'Segoe UI',sans-serif;
background:var(--bg);
background-image:radial-gradient(1200px 600px at 85% -10%,rgba(167,139,250,.10),transparent 60%),
radial-gradient(900px 500px at -10% 0%,rgba(34,211,238,.08),transparent 55%),
radial-gradient(700px 700px at 50% 110%,rgba(94,160,255,.07),transparent 60%);
background-attachment:fixed}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
a.dead{color:#5b6478;pointer-events:none}
.top{background:rgba(10,14,26,.82);backdrop-filter:blur(12px);
border-bottom:1px solid var(--line);color:#fff;
padding:.65rem 20px;font-size:13px;position:sticky;top:0;z-index:10;
display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.top a{color:rgba(229,234,243,.9)}
.top b{font-weight:700}
.top .dim{color:var(--sub)}
main{max-width:1020px;margin:0 auto;padding:24px 20px 70px}
h1{font-size:1.45rem;line-height:1.4;letter-spacing:-.01em;margin:.4em 0}
h2{font-size:1.05rem;margin-top:2.4em;padding-bottom:8px;
border-bottom:1px solid var(--line);letter-spacing:.02em;
display:flex;align-items:baseline;gap:10px}
h2::before{content:"";width:22px;height:3px;border-radius:2px;align-self:center;
background:linear-gradient(90deg,var(--cyan),var(--accent2))}
.badge{background:rgba(94,160,255,.12);color:var(--accent);border-radius:5px;
padding:1px 8px;font-weight:600;font-size:12px;border:1px solid rgba(94,160,255,.25)}
.chip{display:inline-block;border:1px solid var(--line2);background:var(--card);
border-radius:6px;padding:2px 9px;font-size:12.5px;margin:2px;color:var(--sub)}
.v-go{color:var(--go-t);font-weight:700}
.v-hold{color:var(--hold-t);font-weight:700}
.v-avoid{color:var(--avoid-t);font-weight:700}
/* ── hero ── */
.hero{position:relative;border:1px solid var(--line);border-radius:18px;
overflow:hidden;margin:18px 0 8px;background:linear-gradient(160deg,#0e1526,#0a0e1a)}
.hero canvas{position:absolute;inset:0;width:100%;height:100%}
.hero .inner{position:relative;padding:34px 30px 26px;z-index:1}
.hero h1{font-size:2.1rem;margin:0;font-weight:800;letter-spacing:-.02em;
background:linear-gradient(92deg,#7dd3fc 0%,#5ea0ff 40%,#a78bfa 80%);
-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(0 0 18px rgba(94,160,255,.25))}
.hero .sub{color:var(--sub);font-size:13px;margin-top:6px;font-family:var(--mono)}
/* stat tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
gap:12px;margin:22px 0 4px}
.tile{background:var(--card);backdrop-filter:blur(8px);border:1px solid var(--line);
border-radius:14px;padding:14px 18px;transition:transform .18s,border-color .18s}
.tile:hover{transform:translateY(-3px);border-color:var(--line2);box-shadow:var(--glow)}
.tile .n{font-size:1.75rem;font-weight:800;font-family:var(--mono);letter-spacing:-.02em;
background:linear-gradient(180deg,#e5eaf3,#93a6c9);
-webkit-background-clip:text;background-clip:text;color:transparent}
.tile .l{font-size:12px;color:var(--sub);margin-top:2px;letter-spacing:.04em}
/* verdict bar（狀態色 #16a34a/#d97706/#dc2626 已過 dataviz 六檢查；2px 間隔＋直接標籤） */
.vbar{display:flex;height:14px;border-radius:7px;overflow:hidden;gap:2px;
background:var(--bg2);margin:10px 0 6px}
.vbar div{height:100%}
.vlegend{display:flex;gap:18px;font-size:12.5px;color:var(--sub);
font-family:var(--mono);flex-wrap:wrap}
.vlegend i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px}
/* type breakdown（magnitude → 單一色相） */
.tbrk{margin:8px 0}
.tbrk .row{display:grid;grid-template-columns:110px 1fr 48px;gap:10px;
align-items:center;font-size:12.5px;color:var(--sub);margin:5px 0}
.tbrk .bar{height:8px;border-radius:4px;background:linear-gradient(90deg,#2f66c4,#5ea0ff);
box-shadow:0 0 10px rgba(94,160,255,.25);min-width:2px}
.tbrk .num{font-family:var(--mono);text-align:right;color:var(--ink)}
/* ── 檔案卡內頁 ── */
.filecard{background:var(--card);backdrop-filter:blur(8px);border:1px solid var(--line);
border-radius:16px;padding:20px 24px;margin:16px 0}
.filecard .meta{display:flex;gap:10px;flex-wrap:wrap;align-items:center;
font-size:13px;color:var(--sub);margin:8px 0}
.filecard .one{font-size:14.5px;color:#c6d0e2;background:rgba(94,160,255,.07);
border-left:3px solid var(--accent);padding:10px 14px;border-radius:0 8px 8px 0;
margin:12px 0}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 4px}
.btn{display:inline-block;border-radius:9px;padding:8px 18px;font-weight:600;
font-size:14px;color:#fff!important;
background:linear-gradient(92deg,#2f66c4,#5ea0ff);
box-shadow:0 2px 14px rgba(94,160,255,.3)}
.btn:hover{text-decoration:none;filter:brightness(1.1)}
.btn.sec{background:var(--card);color:var(--accent)!important;
border:1px solid rgba(94,160,255,.4);box-shadow:none}
article{background:var(--card);border:1px solid var(--line);border-radius:12px;
padding:8px 28px 24px;margin-top:14px}
details.fulltext{margin-top:14px}
details.fulltext>summary{cursor:pointer;background:var(--card);
border:1px dashed var(--line2);border-radius:12px;padding:12px 18px;
color:var(--sub);font-size:13.5px;user-select:none}
details.fulltext[open]>summary{border-bottom-left-radius:0;border-bottom-right-radius:0}
details.fulltext>div{background:var(--card);border:1px dashed var(--line2);
border-top:none;border-radius:0 0 12px 12px;padding:4px 28px 22px}
/* ── 首頁元件 ── */
.search{width:100%;padding:13px 18px;border:1px solid var(--line2);
border-radius:12px;font-size:15px;background:var(--card);color:var(--ink);
margin:16px 0 6px;outline:none;transition:border-color .18s,box-shadow .18s}
.search:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(94,160,255,.18)}
.search::placeholder{color:#556180}
.secnav{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 4px;font-size:13px}
.secnav a{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:4px 14px;color:var(--sub);transition:all .15s}
.secnav a:hover{color:var(--ink);border-color:var(--accent);text-decoration:none;
box-shadow:var(--glow)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:10px 16px;margin:8px 0;transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-2px);border-color:var(--line2);box-shadow:var(--glow)}
.card .t{font-weight:600}
.card .m{font-size:12.5px;color:var(--sub);margin-top:2px}
.card .o{font-size:13px;color:#aeb9cf;margin-top:4px}
.cnt{color:var(--sub);font-size:13px;margin:8px 0}
.tickgrid{line-height:2.1}
.tickgrid a{display:inline-block;border:1px solid var(--line);background:var(--card);
border-radius:7px;padding:1px 10px;font-size:13px;margin:2px;font-weight:600;
font-family:var(--mono);transition:all .12s}
.tickgrid a:hover{text-decoration:none;transform:translateY(-1px);
border-color:var(--accent);box-shadow:var(--glow)}
.tickgrid.g-go a{border-left:3px solid var(--go)}
.tickgrid.g-hold a{border-left:3px solid var(--hold)}
.tickgrid.g-avoid a{border-left:3px solid var(--avoid)}
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:10px}
.shelf .card{margin:0}
.pill{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:4px 13px;font-size:12.5px;cursor:pointer;color:var(--sub);user-select:none;
display:inline-block;margin:2px;transition:all .12s}
.pill:hover{border-color:var(--accent)}
.pill.on{background:linear-gradient(92deg,#2f66c4,#5ea0ff);border-color:transparent;
color:#fff;box-shadow:0 2px 12px rgba(94,160,255,.3)}
.subh{font-size:13px;color:var(--sub);font-weight:600;margin:16px 0 6px;
letter-spacing:.03em}
summary{cursor:pointer}
@media(prefers-reduced-motion:reduce){
*{transition:none!important;animation:none!important}
.hero canvas{display:none}}
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
<body><div class="top">🧠 <b>第二大腦</b><span class="dim">本機 wiki（未發布） ·
as of %%ASOF%%</span></div>
<main>

<div class="hero"><canvas id="syn"></canvas><div class="inner">
<h1>第二大腦</h1>
<div class="sub">SECOND BRAIN · %%NCOUNT%% notes · local only · rebuilt on every commit / pull / search</div>
<div class="tiles">
<div class="tile"><div class="n" data-cnt="%%NCOUNT%%">0</div><div class="l">筆記</div></div>
<div class="tile"><div class="n" data-cnt="%%NENT%%">0</div><div class="l">個股 HUB</div></div>
<div class="tile"><div class="n" data-cnt="%%NTHEME%%">0</div><div class="l">主題</div></div>
<div class="tile"><div class="n" data-cnt="%%NEPIC%%">0</div><div class="l">城市史詩</div></div>
<div class="tile"><div class="n" data-cnt="%%NREPO%%">0</div><div class="l">REPOS</div></div>
</div>
<div class="vbar" id="vbar"></div><div class="vlegend" id="vlegend"></div>
</div></div>

<input class="search" id="q" placeholder="全庫搜：ticker / 主題 / 標題 / oneliner…（深度全文用 q.py --search）">
<div class="secnav"><a href="#recent">🕐 最近更新</a><a href="#stocks">📈 個股導航</a>
<a href="#themes">🗺 主題地圖</a><a href="#shelf">📚 閒讀書架</a><a href="#all">全部</a></div>
<div id="qresults"></div>

<h2 id="recent">🕐 最近更新</h2>
<div id="recentlist"></div>
<h2>🧩 知識庫組成</h2>
<div class="tbrk" id="tbrk"></div>

<h2 id="stocks">📈 個股導航 <span class="cnt">點 ticker 進 hub（現裁決＋決策史＋全部報告）</span></h2>
<div class="subh v-go">進場</div><div class="tickgrid g-go" id="tk-go"></div>
<div class="subh v-hold">觀望</div><div class="tickgrid g-hold" id="tk-hold"></div>
<div class="subh v-avoid">迴避</div><div class="tickgrid g-avoid" id="tk-avoid"></div>
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

/* hero：count-up 統計磚 */
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
document.querySelectorAll('.tile .n').forEach(el=>{
  const target=+el.dataset.cnt;
  if(reduce){el.textContent=target.toLocaleString();return}
  const t0=performance.now(),dur=900;
  (function step(t){const k=Math.min(1,(t-t0)/dur),ease=1-Math.pow(1-k,3);
    el.textContent=Math.round(target*ease).toLocaleString();
    if(k<1)requestAnimationFrame(step)})(t0);
});

/* hero：裁決分布條（狀態色已過 dataviz 檢查；直接標籤非 color-alone） */
const VC={'進場':'#16a34a','觀望':'#d97706','迴避':'#dc2626'};
const vcnt={'進場':grp['進場'].length,'觀望':grp['觀望'].length,'迴避':grp['迴避'].length};
const vtot=Object.values(vcnt).reduce((a,b)=>a+b,0)||1;
document.getElementById('vbar').innerHTML=Object.entries(vcnt)
  .map(([k,n])=>'<div style="width:'+(n/vtot*100)+'%;background:'+VC[k]+'"></div>').join('');
document.getElementById('vlegend').innerHTML=Object.entries(vcnt)
  .map(([k,n])=>'<span><i style="background:'+VC[k]+'"></i>'+k+' '+n+'</span>').join('')+
  '<span style="margin-left:auto">現行裁決覆蓋 '+vtot+' 檔</span>';

/* 知識庫組成：type 分布橫條（magnitude → 單一色相） */
const tc={};DATA.forEach(n=>{tc[n.tl]=(tc[n.tl]||0)+1});
const rows=Object.entries(tc).sort((a,b)=>b[1]-a[1]).slice(0,10);
const mx=rows[0][1];
document.getElementById('tbrk').innerHTML=rows.map(([k,n])=>
  '<div class="row"><span>'+e_(k)+'</span>'+
  '<div class="bar" style="width:'+Math.max(2,n/mx*100)+'%"></div>'+
  '<span class="num">'+n+'</span></div>').join('');

/* hero：synapse 粒子網絡 */
(function(){
  if(reduce)return;
  const cv=document.getElementById('syn'),ctx=cv.getContext('2d');
  let W,H,pts=[];
  function size(){W=cv.width=cv.offsetWidth*devicePixelRatio;
    H=cv.height=cv.offsetHeight*devicePixelRatio;
    const n=Math.min(70,Math.floor(cv.offsetWidth/14));
    pts=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,
      vx:(Math.random()-.5)*.25*devicePixelRatio,vy:(Math.random()-.5)*.25*devicePixelRatio}));}
  size();addEventListener('resize',size);
  (function draw(){
    ctx.clearRect(0,0,W,H);
    const R=120*devicePixelRatio;
    for(let i=0;i<pts.length;i++){
      const p=pts[i];
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
      for(let j=i+1;j<pts.length;j++){
        const q=pts[j],dx=p.x-q.x,dy=p.y-q.y,d=Math.hypot(dx,dy);
        if(d<R){ctx.strokeStyle='rgba(94,160,255,'+(0.14*(1-d/R))+')';
          ctx.lineWidth=devicePixelRatio;
          ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();}
      }
      ctx.fillStyle='rgba(125,211,252,.5)';
      ctx.beginPath();ctx.arc(p.x,p.y,1.4*devicePixelRatio,0,7);ctx.fill();
    }
    requestAnimationFrame(draw);
  })();
})();

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

    n_repo = 1 + len({s["repo"] for s in summaries if s.get("repo")})
    (WIKI / "index.html").write_text(
        INDEX.replace("%%ASOF%%", date.today().isoformat())
             .replace("%%NCOUNT%%", str(len(data)))
             .replace("%%NEPIC%%", str(n_epic))
             .replace("%%NENT%%", str(len(ents)))
             .replace("%%NTHEME%%", str(len(themes)))
             .replace("%%NREPO%%", str(n_repo))
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
