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
    "entity": "個股", "theme": "主題", "mental-model": "思維模型",
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
.hero .inner{position:relative;padding:22px 28px 18px;z-index:1}
.hero h1{font-size:1.8rem;margin:0;font-weight:800;letter-spacing:-.02em;
background:linear-gradient(92deg,#7dd3fc 0%,#5ea0ff 40%,#a78bfa 80%);
-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(0 0 18px rgba(94,160,255,.25))}
.hero .sub{color:var(--sub);font-size:13px;margin-top:6px;font-family:var(--mono)}
/* stat tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
gap:10px;margin:16px 0 4px}
.tile{background:var(--card);backdrop-filter:blur(8px);border:1px solid var(--line);
border-radius:14px;padding:10px 16px;transition:transform .18s,border-color .18s}
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
.secnav{display:flex;gap:8px;flex-wrap:wrap;font-size:13px;
position:sticky;top:40px;z-index:9;margin:10px -8px 4px;padding:8px;
background:rgba(10,14,26,.85);backdrop-filter:blur(10px);border-radius:12px}
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
.mono{font-family:var(--mono)}
/* 裁決跑馬燈 */
.tape{overflow:hidden;border-bottom:1px solid var(--line);
background:rgba(13,18,32,.7);backdrop-filter:blur(8px);white-space:nowrap}
.tape-in{display:inline-block;padding:5px 0;font-size:12.5px;
font-family:var(--mono);animation:tape 70s linear infinite}
.tape-in a{color:var(--sub);margin:0 4px}
.tape-in a span{color:#556180}
.tape-in i{color:#39425c;font-style:normal;margin:0 8px}
.tape:hover .tape-in{animation-play-state:paused}
@keyframes tape{from{transform:translateX(0)}to{transform:translateX(-50%)}}
/* 知識圖譜 */
.graphwrap{position:relative;border:1px solid var(--line);border-radius:16px;
overflow:hidden;background:
radial-gradient(600px 300px at 70% 20%,rgba(167,139,250,.07),transparent 60%),
linear-gradient(160deg,#0e1526,#0a0e1a)}
.graphwrap canvas{display:block;width:100%;height:560px}
/* ⌘K 指令面板 */
#pal{position:fixed;inset:0;background:rgba(6,9,18,.66);backdrop-filter:blur(6px);
z-index:100;display:flex;align-items:flex-start;justify-content:center;
padding-top:14vh}
#pal[hidden]{display:none!important}
.palbox{width:min(640px,92vw);background:var(--cardsolid);
border:1px solid var(--line2);border-radius:16px;overflow:hidden;
box-shadow:0 24px 80px rgba(0,0,0,.6),0 0 40px rgba(94,160,255,.12)}
.palbox input{width:100%;padding:16px 20px;font-size:16px;border:none;
outline:none;background:transparent;color:var(--ink);
border-bottom:1px solid var(--line)}
#palres{max-height:46vh;overflow-y:auto}
.palrow{display:block;padding:10px 18px;color:var(--ink);font-size:14px;
border-bottom:1px solid rgba(148,163,184,.07)}
.palrow:hover,.palrow.first{background:rgba(94,160,255,.1);text-decoration:none}
.palrow.first{border-left:3px solid var(--accent)}
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
as of %%ASOF%%</span><span class="dim" style="margin-left:auto">⌘K 快速跳轉</span></div>
<div class="tape"><div class="tape-in" id="tape"></div></div>
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
<a href="#themes">🗺 主題地圖</a><a href="#shelf">📚 閒讀書架</a><a href="#all">全部</a>
<a href="munger.html" style="border-color:rgba(167,139,250,.5);color:#c4b5fd">🧭 蒙格清單</a></div>
<div id="qresults"></div>

<h2 id="recent">🕐 最近更新</h2>
<div id="recentlist"></div>
<details id="recentmore"><summary class="cnt">更多近期報告…</summary>
<div id="recentrest"></div></details>

<h2 id="graph">🕸 知識圖譜 <span class="cnt">現行裁決個股 × 產業主題 · hover 看連線 · 點節點跳 hub</span></h2>
<div class="graphwrap"><canvas id="kg"></canvas></div>

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

<div id="pal" hidden><div class="palbox">
<input id="palq" placeholder="跳轉：ticker / 主題 / 報告標題…（Enter 開第一筆，Esc 關閉）">
<div id="palres"></div></div></div>

<script id="brain-data" type="application/json">%%DATA%%</script>
<script id="ent-data" type="application/json">%%ENT%%</script>
<script id="theme-data" type="application/json">%%THEMES%%</script>
<script id="kg-data" type="application/json">%%KG%%</script>
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

/* 最近更新：決策相關類型，首屏 10 筆 + 折疊 20 筆 */
const REC_T=new Set(['dd','id','earnings','comparison','synthesis','monitor','supplychain','internal-note']);
const recent=DATA.filter(n=>REC_T.has(n.t)&&n.d);
document.getElementById('recentlist').innerHTML=recent.slice(0,10).map(card).join('');
document.getElementById('recentrest').innerHTML=recent.slice(10,40).map(card).join('');

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

/* 裁決跑馬燈：最新 DD 裁決 */
(function(){
  const rows=DATA.filter(n=>n.t==='dd'&&n.v&&n.d).slice(0,40);
  const seg=rows.map(n=>'<a href="'+n.p+'"><b class="'+(n.vc||'')+'">'+e_(n.v)+'</b> '+
    e_(n.k||'')+' <span>'+e_(n.d.slice(5))+'</span></a>').join('<i>·</i>');
  const el=document.getElementById('tape');
  el.innerHTML=seg+'<i>·</i>'+seg;  /* 複製一份做無縫循環 */
  if(reduce)el.style.animation='none';
})();

/* hero：synapse 粒子網絡（滑鼠會吸引連線） */
(function(){
  if(reduce)return;
  const cv=document.getElementById('syn'),ctx=cv.getContext('2d');
  let W,H,pts=[],mouse=null;
  const DPR=devicePixelRatio;
  function size(){W=cv.width=cv.offsetWidth*DPR;H=cv.height=cv.offsetHeight*DPR;
    const n=Math.min(70,Math.floor(cv.offsetWidth/14));
    pts=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,
      vx:(Math.random()-.5)*.25*DPR,vy:(Math.random()-.5)*.25*DPR}));}
  size();addEventListener('resize',size);
  cv.parentElement.addEventListener('mousemove',e=>{
    const r=cv.getBoundingClientRect();
    mouse={x:(e.clientX-r.left)*DPR,y:(e.clientY-r.top)*DPR}});
  cv.parentElement.addEventListener('mouseleave',()=>mouse=null);
  (function draw(){
    ctx.clearRect(0,0,W,H);
    const R=120*DPR;
    for(let i=0;i<pts.length;i++){
      const p=pts[i];
      if(mouse){const dx=mouse.x-p.x,dy=mouse.y-p.y,d=Math.hypot(dx,dy);
        if(d<200*DPR&&d>1){p.vx+=dx/d*.012*DPR;p.vy+=dy/d*.012*DPR}}
      p.vx*=.995;p.vy*=.995;
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
      for(let j=i+1;j<pts.length;j++){
        const q=pts[j],dx=p.x-q.x,dy=p.y-q.y,d=Math.hypot(dx,dy);
        if(d<R){ctx.strokeStyle='rgba(94,160,255,'+(0.14*(1-d/R))+')';
          ctx.lineWidth=DPR;
          ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();}
      }
      if(mouse){const d=Math.hypot(mouse.x-p.x,mouse.y-p.y);
        if(d<160*DPR){ctx.strokeStyle='rgba(34,211,238,'+(0.25*(1-d/(160*DPR)))+')';
          ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(mouse.x,mouse.y);ctx.stroke();}}
      ctx.fillStyle='rgba(125,211,252,.5)';
      ctx.beginPath();ctx.arc(p.x,p.y,1.4*DPR,0,7);ctx.fill();
    }
    requestAnimationFrame(draw);
  })();
})();

/* 統計磚 3D 傾斜 */
if(!reduce)document.querySelectorAll('.tile').forEach(t=>{
  t.addEventListener('mousemove',e=>{
    const r=t.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,
      y=(e.clientY-r.top)/r.height-.5;
    t.style.transform='perspective(500px) rotateY('+(x*8)+'deg) rotateX('+(-y*8)+'deg) translateY(-3px)'});
  t.addEventListener('mouseleave',()=>t.style.transform='');
});

/* ⌘K 指令面板 */
(function(){
  const pal=document.getElementById('pal'),pq=document.getElementById('palq'),
    pr=document.getElementById('palres');
  let items=[];
  function open(){pal.hidden=false;pq.value='';pr.innerHTML='';pq.focus()}
  function close(){pal.hidden=true}
  addEventListener('keydown',e=>{
    if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();open()}
    else if(e.key==='/'&&document.activeElement.tagName!=='INPUT'){e.preventDefault();open()}
    else if(e.key==='Escape')close();
    else if(e.key==='Enter'&&!pal.hidden&&items.length)location.href=items[0].p;
  });
  pal.addEventListener('click',e=>{if(e.target===pal)close()});
  pq.addEventListener('input',()=>{
    const q=pq.value.trim().toLowerCase();
    if(!q){pr.innerHTML='';items=[];return}
    const ents=ENT.filter(t=>t.k.toLowerCase().indexOf(q)>=0).slice(0,5)
      .map(t=>({p:t.p,h:'<b class="mono">'+e_(t.k)+'</b> <span class="'+
        ({'進場':'v-go','觀望':'v-hold','迴避':'v-avoid'}[t.v]||'')+'">'+e_(t.v||'')+'</span>',tag:'個股'}));
    const ths=THEMES.filter(t=>t.name.toLowerCase().indexOf(q)>=0).slice(0,4)
      .map(t=>({p:t.p,h:e_(t.name),tag:'主題'}));
    const nts=DATA.filter(n=>n.s.indexOf(q)>=0).slice(0,8)
      .map(n=>({p:n.p,h:e_(n.title),tag:n.tl}));
    items=ents.concat(ths,nts);
    pr.innerHTML=items.map((it,i)=>'<a class="palrow'+(i===0?' first':'')+
      '" href="'+it.p+'"><span class="badge">'+e_(it.tag)+'</span> '+it.h+'</a>').join('')||
      '<div class="cnt" style="padding:10px 16px">無命中</div>';
  });
})();

/* 🕸 力導向知識圖譜 */
(function(){
  const KG=JSON.parse(document.getElementById('kg-data').textContent);
  const cv=document.getElementById('kg');if(!cv||!KG.nodes.length)return;
  const ctx=cv.getContext('2d'),DPR=devicePixelRatio;
  const VC={'進場':'#16a34a','觀望':'#d97706','迴避':'#dc2626'};
  const VT={'進場':'#4ade80','觀望':'#fbbf24','迴避':'#f87171'};
  let W,H;
  const idx={};KG.nodes.forEach((n,i)=>idx[n.id]=i);
  const deg={};KG.links.forEach(l=>{deg[l.s]=(deg[l.s]||0)+1;deg[l.t]=(deg[l.t]||0)+1});
  const N=KG.nodes.map(n=>({...n,deg:deg[n.id]||1,x:0,y:0,vx:0,vy:0}));
  const L=KG.links.map(l=>({a:idx[l.s],b:idx[l.t]}));
  const nb={};L.forEach(l=>{(nb[l.a]=nb[l.a]||new Set()).add(l.b);
    (nb[l.b]=nb[l.b]||new Set()).add(l.a)});
  function size(){W=cv.width=cv.offsetWidth*DPR;H=cv.height=cv.offsetHeight*DPR;
    N.forEach(n=>{if(!n.x){n.x=W/2+(Math.random()-.5)*W*.8;
      n.y=H/2+(Math.random()-.5)*H*.8}})}
  size();addEventListener('resize',size);
  let hover=-1,alpha=1;
  function r_(n){return (n.kind==='theme'?5+Math.min(9,n.deg*.9):4+Math.min(5,n.deg))*DPR}
  function tickPhys(){
    const k=alpha;
    if(k<.005)return;
    for(let i=0;i<N.length;i++)for(let j=i+1;j<N.length;j++){
      const a=N[i],b=N[j];let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+40;
      const f=1400*DPR*DPR/d2*k;const d=Math.sqrt(d2);
      dx/=d;dy/=d;a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f;}
    L.forEach(l=>{const a=N[l.a],b=N[l.b];
      const dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1;
      const f=(d-90*DPR)*.004*k;
      a.vx+=dx/d*f*d;a.vy+=dy/d*f*d;b.vx-=dx/d*f*d;b.vy-=dy/d*f*d;});
    N.forEach(n=>{
      n.vx+=(W/2-n.x)*.0012*k;n.vy+=(H/2-n.y)*.0012*k;
      n.vx*=.86;n.vy*=.86;n.x+=n.vx;n.y+=n.vy;
      const m=14*DPR;
      n.x=Math.max(m,Math.min(W-m,n.x));n.y=Math.max(m,Math.min(H-m,n.y));});
    alpha*=.999;
  }
  function draw(){
    tickPhys();
    ctx.clearRect(0,0,W,H);
    const hn=hover>=0?nb[hover]||new Set():null;
    L.forEach(l=>{
      const lit=hover>=0&&(l.a===hover||l.b===hover);
      const dim=hover>=0&&!lit;
      ctx.strokeStyle=lit?'rgba(34,211,238,.55)':'rgba(94,160,255,'+(dim?.05:.16)+')';
      ctx.lineWidth=(lit?1.6:1)*DPR;
      ctx.beginPath();ctx.moveTo(N[l.a].x,N[l.a].y);ctx.lineTo(N[l.b].x,N[l.b].y);ctx.stroke();});
    N.forEach((n,i)=>{
      const lit=i===hover||(hn&&hn.has(i));
      const dim=hover>=0&&!lit;
      const r=r_(n);
      ctx.save();
      ctx.globalAlpha=dim?.25:1;
      ctx.shadowColor=n.kind==='theme'?'#5ea0ff':(VC[n.v]||'#5ea0ff');
      ctx.shadowBlur=(lit?22:10)*DPR;
      ctx.fillStyle=n.kind==='theme'?'#3b5aa0':(VC[n.v]||'#334155');
      ctx.beginPath();ctx.arc(n.x,n.y,r,0,7);ctx.fill();
      ctx.shadowBlur=0;
      ctx.strokeStyle=n.kind==='theme'?'#7dd3fc':(VT[n.v]||'#94a3b8');
      ctx.lineWidth=1.2*DPR;ctx.stroke();
      if(lit||n.kind==='ticker'||n.deg>=6){
        ctx.font=(lit?600:400)+' '+(11*DPR)+'px SF Mono,Menlo,monospace';
        ctx.fillStyle=lit?'#e5eaf3':'rgba(139,152,179,'+(dim?.3:.85)+')';
        const lb=n.label.length>16&&!lit?n.label.slice(0,15)+'…':n.label;
        ctx.fillText(lb,n.x+r+4*DPR,n.y+4*DPR);}
      ctx.restore();});
    requestAnimationFrame(draw);
  }
  function hit(e){
    const r=cv.getBoundingClientRect();
    const x=(e.clientX-r.left)*DPR,y=(e.clientY-r.top)*DPR;
    for(let i=0;i<N.length;i++)
      if(Math.hypot(N[i].x-x,N[i].y-y)<r_(N[i])+7*DPR)return i;
    return -1;}
  cv.addEventListener('mousemove',e=>{hover=hit(e);
    cv.style.cursor=hover>=0?'pointer':'default';if(hover>=0)alpha=Math.max(alpha,.05)});
  cv.addEventListener('mouseleave',()=>hover=-1);
  cv.addEventListener('click',e=>{const i=hit(e);if(i>=0&&N[i].p)location.href=N[i].p});
  if(reduce){for(let i=0;i<300;i++)tickPhys();alpha=0}  /* 減少動態：先靜態排好 */
  draw();
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

    # 知識圖譜資料：有現行裁決的 ticker + 它們所屬的主題/供應鏈 + 邊
    v_tickers = {t["k"]: t for t in ents if t["v"]}
    kg_theme_ids = set()
    kg_links = []
    theme_page = {}
    for n in graph.get("nodes", []):
        if n.get("type") in ("industry", "supplychain"):
            theme_page[n["id"]] = stems.get(f"Theme_{_safe_name(n['id'])}")
    for e in graph.get("edges", []):
        if e["from"] in v_tickers and e["to"] in theme_page and theme_page[e["to"]]:
            kg_links.append({"s": e["from"], "t": e["to"]})
            kg_theme_ids.add(e["to"])
    kg_nodes = [{"id": k, "label": k, "kind": "ticker", "v": t["v"], "p": t["p"]}
                for k, t in v_tickers.items()]
    kg_nodes += [{"id": tid, "label": tid, "kind": "theme", "p": theme_page[tid]}
                 for tid in sorted(kg_theme_ids)]
    # 去重邊（同 pair 多來源）
    seen_l = set()
    kg_links = [l for l in kg_links
                if (l["s"], l["t"]) not in seen_l and not seen_l.add((l["s"], l["t"]))]
    kg = {"nodes": kg_nodes, "links": kg_links}

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
             .replace("%%THEMES%%", payload(themes))
             .replace("%%KG%%", payload(kg)), encoding="utf-8")


MUNGER = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>決策前蒙格清單 · 第二大腦</title>
<link rel="stylesheet" href="assets/wiki.css">
<style>
.qcard{border:1px solid var(--line);border-radius:12px;background:var(--card);
padding:14px 18px;margin:10px 0}
.qcard .why{font-size:12px;color:#c4b5fd;background:rgba(167,139,250,.1);
border-radius:6px;padding:3px 10px;display:inline-block;margin-bottom:6px}
.qcard .ask{font-weight:700;font-size:15.5px;color:var(--ink)}
.qcard .nm{font-size:12px;color:var(--sub);margin:4px 0 8px}
.qcard textarea{width:100%;min-height:64px;background:rgba(10,14,26,.6);
border:1px solid var(--line);border-radius:8px;color:var(--ink);
padding:10px 12px;font-size:14px;font-family:inherit;line-height:1.6;resize:vertical}
.qcard textarea:focus{outline:none;border-color:var(--accent);
box-shadow:0 0 0 3px rgba(94,160,255,.15)}
.qcard.ok{border-color:rgba(22,163,74,.45)}
.qcard.ok .ask::after{content:" ✓";color:var(--go-t)}
.wc{font-size:11px;color:#556180;text-align:right;font-family:var(--mono)}
.prog{font-family:var(--mono);font-size:13px;color:var(--sub)}
.hist td{padding:4px 12px 4px 0;font-size:13.5px;font-family:var(--mono)}
.missflag{border:1px solid rgba(220,38,38,.5);background:rgba(220,38,38,.08);
border-radius:10px;padding:10px 16px;margin:10px 0;font-size:13.5px}
.pastbox{border:1px solid rgba(167,139,250,.4);background:rgba(167,139,250,.07);
border-radius:12px;padding:12px 18px;margin:12px 0;font-size:13.5px}
.pmbox{border:1px solid rgba(220,38,38,.35);background:rgba(220,38,38,.05);
border-radius:12px;padding:14px 18px;margin:10px 0;font-size:13.5px;
line-height:1.8;max-height:340px;overflow-y:auto;white-space:pre-wrap}
.verdict-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:10px 0}
.verdict-row select{background:var(--cardsolid);color:var(--ink);
border:1px solid var(--line2);border-radius:8px;padding:8px 12px;font-size:14px}
</style></head>
<body><div class="top"><a href="index.html">🧠 <b>第二大腦</b></a>
<span class="dim">🧭 決策前蒙格清單</span></div>
<main>
<h1>🧭 決策前蒙格清單</h1>
<p class="cnt">勾選不會讓你變聰明——<b>寫下來</b>才會。這頁按這檔股票的實際狀態出題（不是 30 題全灌），
每題要寫 ≥20 字才算過；寫完跟 pre-mortem 對質，最後留下裁決與殺手假設，匯出進第二大腦讓未來的你打臉。</p>
<input class="search" id="tk" list="tkl" placeholder="輸入 ticker（如 NVDA、2330.TW）…" autocomplete="off">
<datalist id="tkl"></datalist>
<div id="out"></div>

<script id="d-models" type="application/json">%%MODELS%%</script>
<script id="d-ents" type="application/json">%%ENTS%%</script>
<script id="d-themes" type="application/json">%%ENTTHEMES%%</script>
<script id="d-notes" type="application/json">%%NOTESBY%%</script>
<script id="d-settle" type="application/json">%%SETTLE%%</script>
<script id="d-pm" type="application/json">%%PM%%</script>
<script>
const MODELS=JSON.parse(document.getElementById('d-models').textContent);
const ENTS=JSON.parse(document.getElementById('d-ents').textContent);
const ETH=JSON.parse(document.getElementById('d-themes').textContent);
const NB=JSON.parse(document.getElementById('d-notes').textContent);
const ST=JSON.parse(document.getElementById('d-settle').textContent);
const PM=JSON.parse(document.getElementById('d-pm').textContent);
const M={};MODELS.forEach(m=>M[m.id]=m);
const ENTMAP={};ENTS.forEach(t=>ENTMAP[t.k]=t);
document.getElementById('tkl').innerHTML=ENTS.map(t=>'<option value="'+t.k+'">').join('');
function e_(s){const d=document.createElement('span');d.textContent=s==null?'':s;return d.innerHTML}
const VCL={'進場':'v-go','觀望':'v-hold','迴避':'v-avoid'};
const MIN=20;

/* ── 對症出題引擎：依這檔的實際狀態選 6-9 題，每題帶「為什麼問你這題」 ── */
function route(tk,ent,rows,ths,notes){
  const picks=[],seen=new Set();
  function add(ids,why){ids.forEach(id=>{if(!seen.has(id)&&M[id]){seen.add(id);
    picks.push({m:M[id],why})}})}
  add(['m6'],'核心題：反方論點是入場費，不是選配');
  add(['m26','m24'],'核心題：沒有期望值與機會成本，其他都是敘事');
  const missed=rows.filter(r=>(r[1]==='觀望'||r[1]==='迴避')&&r[2]>30);
  if(missed.length)add(['m22','m16'],'你曾對這檔說「'+missed[0][1]+'」，之後 +'+missed[0][2]+
    '%——先檢查你是在更新信念，還是在防衛舊立場');
  const last=rows.length?rows[rows.length-1]:null;
  if(last&&last[2]>50)add(['m9','m17'],'結算 +'+last[2]+'%——你的「還會漲」是絕對價值還是對比效應？');
  if(last&&last[2]<-20)add(['m7','m22'],'結算 '+last[2]+'%——套牢時最容易凹單，檢查損失厭惡');
  if(ent.v==='進場')add(['m2','m21','m18'],'現裁決是進場——樂觀時最該檢查從眾、過度自信與安全邊際');
  if(ent.v==='觀望'||ent.v==='迴避')add(['m7','m23'],'現裁決偏空——檢查你是理性保守還是心理防衛');
  if(ths.length>=4)add(['m10'],'這檔掛 '+ths.length+' 條 thesis——多重利多共振正是 lollapalooza 高發區');
  if(ths.length<=1)add(['m30','m19'],'只掛 '+ths.length+' 條 thesis——單腳桌，檢查生態位與單點失敗');
  if(notes.length<2)add(['m25','m3'],'這檔功課只有 '+notes.length+' 份——你的資訊優勢從哪來？');
  if(ent.g==='A+'||ent.g==='A')add(['m12','m13'],'評級 '+ent.g+'——愈是好公司愈要問護城河能撐幾年、誰來毀滅它');
  return picks.slice(0,9);
}

function store(tk){try{return JSON.parse(localStorage.getItem('munger2_'+tk)||'{}')}catch(e){return{}}}
function save(tk,s){s.date=new Date().toISOString().slice(0,10);
  localStorage.setItem('munger2_'+tk,JSON.stringify(s))}

let CUR=null;
function render(tk){
  tk=tk.toUpperCase();
  const ent=ENTMAP[tk],out=document.getElementById('out');
  if(!ent){out.innerHTML=tk?'<p class="cnt">庫裡沒有 '+e_(tk)+
    ' —— 這就是能力圈的邊界：沒做過功課的名字，蒙格會放進「太難」籃子。</p>':'';return}
  const rows=ST[tk]||[],ths=ETH[tk]||[],notes=NB[tk]||[];
  const dd=notes.find(n=>n.t==='dd');
  const S=store(tk);S.answers=S.answers||{};
  const picks=route(tk,ent,rows,ths,notes);
  CUR={tk,ent,picks,S};
  let h='';

  /* 檔案 + 上次的你 */
  h+='<div class="filecard"><h1 style="font-family:var(--mono)">'+e_(tk)+'</h1>'+
    '<div class="meta">'+(ent.v?'<span class="'+(VCL[ent.v]||'')+'">庫內現裁決：'+e_(ent.v)+'</span>'
    :'<span>無現行裁決</span>')+(ent.g?'<span>評級 <b>'+e_(ent.g)+'</b></span>':'')+
    '</div><div class="actions"><a class="btn sec" href="'+ent.p+'">個股 hub</a>'+
    (dd?'<a class="btn sec" href="'+dd.p+'">最新 DD 筆記</a>':'')+'</div></div>';
  if(S.verdict&&S.savedDate){
    const cur=rows.length?rows[rows.length-1]:null;
    h+='<div class="pastbox">🪞 <b>'+e_(S.savedDate)+' 的你</b>裁決「<b class="'+
      (VCL[S.verdict]||'')+'">'+e_(S.verdict)+'</b>」，殺手假設：「'+e_(S.falsifier||'（沒寫）')+'」'+
      (cur?' — 目前結算 '+(cur[2]>=0?'+':'')+cur[2]+'%。':'')+
      '<br>先回答：殺手假設觸發了嗎？沒觸發的話，這次是新資訊還是舊情緒？</div>';
  }

  /* ① 對質資料 */
  h+='<h2>① 先跟紀錄對質</h2>';
  if(rows.length){
    h+='<table class="hist">'+rows.map(r=>{
      const miss=(r[1]==='觀望'||r[1]==='迴避')&&r[2]>30;
      return '<tr><td>'+e_(r[0])+'</td><td class="'+(VCL[r[1]]||'')+'">'+e_(r[1]||'—')+
      '</td><td style="color:'+(r[2]>=0?'var(--go-t)':'var(--avoid-t)')+'">'+
      (r[2]>=0?'+':'')+r[2]+'%</td><td class="cnt">'+r[3]+'d'+(miss?' ⚠':'')+'</td></tr>'}).join('')+
      '</table>';
  }else h+='<p class="cnt">尚無機械結算紀錄。</p>';
  h+=ths.length?'<div class="tickgrid">'+ths.map(t=>'<a href="'+t.p+'">'+e_(t.name)+'</a>').join('')+'</div>':'';

  /* ② 對症題目（寫，不是勾） */
  h+='<h2>② 這檔的題目 <span class="prog" id="prog"></span></h2>'+
    '<p class="cnt">題目由這檔的裁決/結算/thesis 數/功課量路由出來，每題 ≥'+MIN+
    ' 字。寫不出來＝你還沒想過。 <a href="#" id="more">＋隨機加 3 題</a></p>'+
    '<div id="qs"></div>';

  /* ③ pre-mortem 對質 */
  h+='<h2>③ 跟反方對質</h2>';
  if(PM[tk]){
    h+='<p class="cnt">下面是這檔 DD 的 pre-mortem（失敗劇本），讀完再答：</p>'+
      '<div class="pmbox">'+e_(PM[tk])+'</div>';
  }else h+='<p class="cnt">這檔沒有 v13+ pre-mortem'+(dd?'（開 DD 筆記找 §13）':'')+
    '——那你自己先寫一個。</p>';
  h+='<div class="qcard" id="duelcard"><div class="ask">反方最強的一擊是什麼？你怎麼接？</div>'+
    '<div class="nm">規則：先把反方論點寫到「反方會點頭」的程度，才輪到你反駁。寫不出反方＝你不配有觀點。</div>'+
    '<textarea id="duel" placeholder="反方最強一擊：… ／ 我的回應：…">'+e_(S.duel||'')+'</textarea>'+
    '<div class="wc" id="duelwc"></div></div>';

  /* ④ 裁決承諾 */
  h+='<h2>④ 落裁決 — 給未來的你打臉用</h2>'+
    '<div class="verdict-row"><b>我的裁決：</b><select id="vd">'+
    ['','進場','觀望','迴避'].map(v=>'<option'+(S.verdict===v?' selected':'')+'>'+v+'</option>').join('')+
    '</select></div>'+
    '<div class="qcard"><div class="ask">殺手假設（falsifier）：出現什麼具體訊號，我承認這個裁決錯了？</div>'+
    '<div class="nm">要可觀察、可證偽（「HOKA 連兩季 cc growth <10%」，不是「基本面變差」）。</div>'+
    '<textarea id="fals" placeholder="若…，則我錯了，應…">'+e_(S.falsifier||'')+'</textarea></div>'+
    '<div class="actions"><a class="btn" href="#" id="export">⬇ 匯出思考紀錄 .md</a>'+
    '<span class="cnt">存到 knowledge/vault/notes/munger/ → 下次 rebuild 自動入腦（可搜尋、掛在 '+e_(tk)+' hub 下）</span></div>';

  out.innerHTML=h;
  renderQs();
  bind(tk);
}

function qcard(p,S){
  const val=S.answers[p.m.id]||'';
  return '<div class="qcard'+(val.length>=MIN?' ok':'')+'" data-m="'+p.m.id+'">'+
    '<div class="why">'+e_(p.why)+'</div>'+
    '<div class="ask">'+e_(p.m.ask)+'</div>'+
    '<div class="nm">'+e_(p.m.zh)+' · '+e_(p.m.tag)+(p.m.p?' · <a href="'+p.m.p+'">模型筆記＋案例</a>':'')+'</div>'+
    '<textarea placeholder="寫下你的答案（'+MIN+' 字起跳）…">'+e_(val)+'</textarea>'+
    '<div class="wc"></div></div>';
}
function renderQs(){
  document.getElementById('qs').innerHTML=CUR.picks.map(p=>qcard(p,CUR.S)).join('');
  wire();
  prog();
}
function prog(){
  const done=CUR.picks.filter(p=>(CUR.S.answers[p.m.id]||'').length>=MIN).length;
  const el=document.getElementById('prog');
  if(el)el.textContent=done+' / '+CUR.picks.length+' 已寫';
}
function wire(){
  document.querySelectorAll('#qs .qcard').forEach(c=>{
    const ta=c.querySelector('textarea'),wc=c.querySelector('.wc'),id=c.dataset.m;
    function upd(){wc.textContent=ta.value.length+' 字';
      c.classList.toggle('ok',ta.value.length>=MIN);
      CUR.S.answers[id]=ta.value;save(CUR.tk,CUR.S);prog();}
    ta.addEventListener('input',upd);upd();
  });
}
function bind(tk){
  const duel=document.getElementById('duel'),dwc=document.getElementById('duelwc');
  function dupd(){dwc.textContent=duel.value.length+' 字';
    document.getElementById('duelcard').classList.toggle('ok',duel.value.length>=MIN);
    CUR.S.duel=duel.value;save(tk,CUR.S);}
  duel.addEventListener('input',dupd);dupd();
  document.getElementById('vd').addEventListener('change',e=>{
    CUR.S.verdict=e.target.value;CUR.S.savedDate=new Date().toISOString().slice(0,10);
    save(tk,CUR.S)});
  document.getElementById('fals').addEventListener('input',e=>{
    CUR.S.falsifier=e.target.value;CUR.S.savedDate=new Date().toISOString().slice(0,10);
    save(tk,CUR.S)});
  document.getElementById('more').addEventListener('click',e=>{
    e.preventDefault();
    const have=new Set(CUR.picks.map(p=>p.m.id));
    const rest=MODELS.filter(m=>!have.has(m.id));
    for(let i=0;i<3&&rest.length;i++){
      const j=Math.floor(Math.random()*rest.length);
      CUR.picks.push({m:rest.splice(j,1)[0],why:'隨機抽題：格柵要跨學科，不能只答舒服的'});}
    renderQs();
  });
  document.getElementById('export').addEventListener('click',e=>{
    e.preventDefault();exportMd(tk);});
}

function exportMd(tk){
  const S=CUR.S,today=new Date().toISOString().slice(0,10);
  const lines=['---','type: usernote','title: "蒙格清單 · '+tk+' · '+today+'"',
    'ticker: '+tk,'date: '+today,
    (S.verdict?'verdict: '+S.verdict:''),'tags: [munger]','---','',
    '# 蒙格清單 · '+tk+' · '+today,'','所屬：[['+tk+']]',''];
  if(S.verdict)lines.push('## 我的裁決','',S.verdict+(S.falsifier?'\\\\n\\\\n殺手假設：'+S.falsifier:''),'');
  lines.push('## 對症問答','');
  CUR.picks.forEach(p=>{const a=S.answers[p.m.id];if(!a)return;
    lines.push('### '+p.m.zh+' — '+p.m.ask,'',
      '（出題理由：'+p.why+'）','',a,'');});
  if(S.duel)lines.push('## 反方對質','',S.duel,'');
  lines.push('---','（由 wiki/munger.html 匯出；存放 knowledge/vault/notes/munger/ 後 rebuild 入腦）');
  const md=lines.filter(l=>l!==undefined&&l!=='undefined').join('\\\\n');
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([md],{type:'text/markdown'}));
  a.download='MUNGER_'+tk.replace(/[^A-Za-z0-9.]/g,'_')+'_'+today.replace(/-/g,'')+'.md';
  a.click();
}

document.getElementById('tk').addEventListener('change',e=>render(e.target.value.trim()));
document.getElementById('tk').addEventListener('keydown',e=>{
  if(e.key==='Enter')render(e.target.value.trim())});
const h0=decodeURIComponent(location.hash.slice(1));
if(h0){document.getElementById('tk').value=h0;render(h0)}
</script></main></body></html>
"""


def build_munger(summaries, stems, graph):
    import runpy
    mm_path = REPO / "mental_models_data.py"
    if not mm_path.exists():
        return
    data = runpy.run_path(str(mm_path))
    disciplines = data.get("DISCIPLINES", {})
    models = []
    for m in data.get("MODELS", []):
        stem = f"MM_{m['id']}_{_safe_name(m['zh'])}"
        models.append({"id": m["id"], "zh": m["zh"], "tag": m.get("tag", ""),
                       "ask": m.get("ask", ""),
                       "disc": disciplines.get(m.get("d"), {}).get("zh", m.get("d", "")),
                       "p": stems.get(stem)})

    ents, ent_themes = [], {}
    for n in graph.get("nodes", []):
        if n.get("type") != "company":
            continue
        page = stems.get(n["id"])
        if not page:
            continue
        c = n.get("canonical") or {}
        ents.append({"k": n["id"], "v": c.get("verdict") or "",
                     "g": c.get("fundamental_grade") or "", "p": page})
    theme_page = {}
    for n in graph.get("nodes", []):
        if n.get("type") in ("industry", "supplychain"):
            theme_page[n["id"]] = stems.get(f"Theme_{_safe_name(n['id'])}")
    for e in graph.get("edges", []):
        tp = theme_page.get(e["to"])
        if tp:
            lst = ent_themes.setdefault(e["from"], [])
            if not any(x["name"] == e["to"] for x in lst):
                lst.append({"name": e["to"], "p": tp})

    notes_by = {}
    for s in sorted(summaries, key=lambda s: s.get("date") or "", reverse=True):
        if s["type"] in ("dd", "synthesis", "comparison") and s.get("entity"):
            p = stems.get(Path(s["note"]).stem)
            if p:
                notes_by.setdefault(s["entity"], []).append(
                    {"t": s["type"], "d": s.get("date"), "v": s.get("verdict"),
                     "title": s.get("title"), "one": (s.get("oneliner") or "")[:150],
                     "p": p})

    settle = {}
    sp = KDIR / "settlement.json"
    if sp.exists():
        try:
            for r in json.loads(sp.read_text(encoding="utf-8")).get("rows", []):
                settle.setdefault(r.get("entity"), []).append(
                    [r.get("date"), r.get("verdict"),
                     round(r.get("to_date_pct", 0)), r.get("days", 0)])
        except (json.JSONDecodeError, OSError):
            pass
    for rows in settle.values():
        rows.sort(key=lambda r: r[0] or "")

    # pre-mortem 摘錄：每 entity 取最新 DD 筆記的 §13（對質區內嵌用，cap 2200 字）
    pm = {}
    for ent_k, lst in notes_by.items():
        dd = next((n for n in lst if n["t"] == "dd"), None)
        if not dd:
            continue
        md_rel = dd["p"][:-5] + ".md"
        try:
            body = (VAULT / md_rel).read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(r"^##\s+(§?13[^\n]*[Pp]re-mortem[^\n]*|[^\n]*[Pp]re-mortem[^\n]*)$",
                      body, re.M)
        if not m:
            continue
        seg = body[m.end():]
        nxt = re.search(r"^##\s+", seg, re.M)
        if nxt:
            seg = seg[:nxt.start()]
        seg = seg.strip()
        if len(seg) > 2200:
            seg = seg[:2200] + "\n…（全文開 DD 筆記）"
        if seg:
            pm[ent_k] = seg

    def payload(o):
        return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

    (WIKI / "munger.html").write_text(
        MUNGER.replace("%%MODELS%%", payload(models))
              .replace("%%ENTS%%", payload(ents))
              .replace("%%ENTTHEMES%%", payload(ent_themes))
              .replace("%%NOTESBY%%", payload(notes_by))
              .replace("%%SETTLE%%", payload(settle))
              .replace("%%PM%%", payload(pm)), encoding="utf-8")


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
        if rel in ("index.html", "munger.html"):
            continue
        if rel[:-5] + ".md" not in md_files:
            hp.unlink()
            n_pruned += 1

    graph = json.loads(GRAPH.read_text(encoding="utf-8")) if GRAPH.exists() else {}
    build_index(summaries, stems)
    build_munger(summaries, stems, graph)
    print(f"📖 wiki: {n_render} rendered, {n_skip} cached, {n_pruned} pruned "
          f"→ open {WIKI / 'index.html'}")


if __name__ == "__main__":
    main()
