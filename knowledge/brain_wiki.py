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
    "entity": "個股", "theme": "主題", "mental-model": "思維模型", "munger": "蒙格腦",
    "buffett": "巴菲特信", "marks": "Marks 備忘錄", "wisdom-card": "判斷卡",
}

CSS = """
:root{--bg:#070a14;--bg2:#0a0f1e;--card:rgba(19,26,46,.72);--cardsolid:#111730;
--ink:#e5eaf3;--sub:#8b98b3;--line:rgba(148,163,184,.14);--line2:rgba(148,163,184,.28);
--accent:#5ea0ff;--accent2:#a78bfa;--cyan:#22d3ee;
--go:#16a34a;--hold:#d97706;--avoid:#dc2626;
--go-t:#4ade80;--hold-t:#fbbf24;--avoid-t:#f87171;
--glow:0 0 24px rgba(94,160,255,.18);--glow-cy:0 0 26px rgba(34,211,238,.22);
--grid:rgba(94,160,255,.04);
--mono:'SF Mono','JetBrains Mono',ui-monospace,Menlo,monospace}
*{box-sizing:border-box}
::selection{background:rgba(34,211,238,.32)}
html{scrollbar-color:#3b5aa0 #070a14;scrollbar-width:thin}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:#070a14}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#1d3a6b,#3b5aa0);
border-radius:5px;border:2px solid #070a14}
::-webkit-scrollbar-thumb:hover{background:#5ea0ff}
body{margin:0;color:var(--ink);font-size:15px;line-height:1.75;
font-family:'Inter','Noto Sans TC',-apple-system,'Segoe UI',sans-serif;
background:var(--bg);
background-image:
radial-gradient(1px 1px at 22% 34%,rgba(226,236,255,.6) 50%,transparent 51%),
radial-gradient(1px 1px at 68% 12%,rgba(165,215,255,.45) 50%,transparent 51%),
radial-gradient(1.4px 1.4px at 44% 78%,rgba(196,181,253,.4) 50%,transparent 51%),
radial-gradient(1px 1px at 84% 56%,rgba(226,236,255,.28) 50%,transparent 51%),
linear-gradient(var(--grid) 1px,transparent 1px),
linear-gradient(90deg,var(--grid) 1px,transparent 1px),
radial-gradient(1200px 600px at 85% -10%,rgba(167,139,250,.14),transparent 60%),
radial-gradient(900px 500px at -10% 0%,rgba(34,211,238,.10),transparent 55%),
radial-gradient(1100px 520px at 60% 45%,rgba(99,72,190,.07),transparent 65%),
radial-gradient(700px 700px at 50% 110%,rgba(94,160,255,.08),transparent 60%);
background-size:190px 190px,290px 290px,410px 410px,530px 530px,
46px 46px,46px 46px,100% 100%,100% 100%,100% 100%,100% 100%;
background-attachment:fixed}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
a.dead{color:#5b6478;pointer-events:none}
.top{background:rgba(7,10,20,.82);backdrop-filter:blur(12px);
border-bottom:1px solid var(--line);color:#fff;
padding:.65rem 20px;font-size:13px;position:sticky;top:0;z-index:10;
display:flex;gap:16px;align-items:center;flex-wrap:wrap;
box-shadow:0 1px 0 rgba(34,211,238,.09)}
.top a{color:rgba(229,234,243,.9)}
.top b{font-weight:700;letter-spacing:.04em}
.top .dim{color:var(--sub)}
main{max-width:1020px;margin:0 auto;padding:24px 20px 70px}
h1{font-size:1.45rem;line-height:1.4;letter-spacing:-.01em;margin:.4em 0}
h2{font-size:1.05rem;margin-top:2.4em;padding-bottom:8px;
border-bottom:1px dashed rgba(148,163,184,.24);letter-spacing:.02em;
display:flex;align-items:baseline;gap:10px}
h2::before{content:"";width:22px;height:3px;border-radius:2px;align-self:center;
background:linear-gradient(90deg,var(--cyan),var(--accent2));
box-shadow:0 0 10px rgba(34,211,238,.5)}
.badge{background:rgba(94,160,255,.12);color:var(--accent);border-radius:5px;
padding:1px 8px;font-weight:600;font-size:12px;border:1px solid rgba(94,160,255,.25)}
.chip{display:inline-block;border:1px solid var(--line2);background:var(--card);
border-radius:6px;padding:2px 9px;font-size:12.5px;margin:2px;color:var(--sub)}
.v-go{color:var(--go-t);font-weight:700}
.v-hold{color:var(--hold-t);font-weight:700}
.v-avoid{color:var(--avoid-t);font-weight:700}
/* ── hero ── */
.hero{position:relative;border:1px solid var(--line);border-radius:18px;
overflow:hidden;margin:18px 0 8px;background-color:#070a14;
background-image:
radial-gradient(1px 1px at 18% 28%,rgba(226,236,255,.7) 50%,transparent 51%),
radial-gradient(1px 1px at 72% 64%,rgba(165,215,255,.55) 50%,transparent 51%),
radial-gradient(1.5px 1.5px at 46% 12%,rgba(196,181,253,.5) 50%,transparent 51%),
repeating-linear-gradient(0deg,rgba(94,160,255,.028) 0 1px,transparent 1px 4px),
radial-gradient(520px 280px at 82% -5%,rgba(167,139,250,.15),transparent 65%),
linear-gradient(160deg,#0e1526,#070a14);
background-size:170px 170px,240px 240px,330px 330px,auto,100% 100%,100% 100%;
box-shadow:0 0 0 1px rgba(34,211,238,.06),0 22px 60px rgba(0,0,0,.42)}
.hero::before,.hero::after{content:"";position:absolute;width:24px;height:24px;
z-index:2;pointer-events:none}
.hero::before{top:12px;left:12px;border-top:2px solid var(--cyan);
border-left:2px solid var(--cyan);opacity:.55}
.hero::after{bottom:12px;right:12px;border-bottom:2px solid var(--accent2);
border-right:2px solid var(--accent2);opacity:.55}
.hero canvas{position:absolute;inset:0;width:100%;height:100%}
.hero .inner{position:relative;padding:22px 28px 18px;z-index:1}
/* 艙窗軌道環＋緩行光點（裝飾層，pointer-events:none） */
.hero .inner::before{content:"";position:absolute;top:-96px;right:-70px;
width:280px;height:280px;border-radius:50%;pointer-events:none;
border:1px dashed rgba(34,211,238,.22);
box-shadow:inset 0 0 40px rgba(34,211,238,.05)}
.hero .inner::after{content:"";position:absolute;top:41px;right:67px;
width:6px;height:6px;border-radius:50%;pointer-events:none;
background:#7dd3fc;box-shadow:0 0 8px 2px rgba(125,211,252,.6);
transform:rotate(35deg) translateX(140px);
animation:orbit 26s linear infinite}
@keyframes orbit{from{transform:rotate(0deg) translateX(140px)}
to{transform:rotate(360deg) translateX(140px)}}
.hero h1{font-size:1.8rem;margin:0;font-weight:800;letter-spacing:-.02em;
background:linear-gradient(92deg,#7dd3fc 0%,#5ea0ff 40%,#a78bfa 80%);
-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(0 0 18px rgba(94,160,255,.25))}
.hero .sub{color:var(--sub);font-size:13px;margin-top:6px;font-family:var(--mono);
letter-spacing:.05em}
/* stat tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
gap:10px;margin:16px 0 4px}
.tile{background:var(--card);backdrop-filter:blur(8px);border:1px solid var(--line);
border-radius:14px;padding:10px 16px;position:relative;overflow:hidden;
transition:transform .18s,border-color .18s,box-shadow .18s}
.tile::before{content:"";position:absolute;top:0;left:0;right:0;height:1px;
background:linear-gradient(90deg,transparent,var(--cyan),transparent);opacity:.45}
.tile::after{content:"";position:absolute;top:8px;right:8px;width:9px;height:9px;
pointer-events:none;opacity:.4;
background:
linear-gradient(var(--cyan),var(--cyan)) center/1px 9px no-repeat,
linear-gradient(var(--cyan),var(--cyan)) center/9px 1px no-repeat}
.tile:hover{transform:translateY(-3px);border-color:var(--line2);
box-shadow:var(--glow),0 14px 34px rgba(2,5,16,.55)}
.tile .n{font-size:1.75rem;font-weight:800;font-family:var(--mono);letter-spacing:-.02em;
background:linear-gradient(120deg,#7dd3fc,#5ea0ff 55%,#a78bfa);
-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(0 0 12px rgba(94,160,255,.28))}
.tile .l{font-size:12px;color:var(--sub);margin-top:2px;letter-spacing:.12em;
text-transform:uppercase}
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
border-radius:16px;padding:20px 24px;margin:16px 0;position:relative;overflow:hidden}
.filecard::before{content:"";position:absolute;top:0;left:0;width:100%;height:2px;
background:linear-gradient(90deg,var(--cyan),var(--accent),var(--accent2));opacity:.7}
.filecard .meta{display:flex;gap:10px;flex-wrap:wrap;align-items:center;
font-size:13px;color:var(--sub);margin:8px 0}
.filecard .one{font-size:14.5px;color:#c6d0e2;background:rgba(94,160,255,.07);
border-left:3px solid var(--accent);padding:10px 14px;border-radius:0 8px 8px 0;
margin:12px 0}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 4px}
.btn{display:inline-block;border-radius:9px;padding:8px 18px;font-weight:600;
font-size:14px;color:#fff!important;position:relative;overflow:hidden;
background:linear-gradient(92deg,#2f66c4,#5ea0ff);
box-shadow:0 2px 14px rgba(94,160,255,.3)}
.btn::after{content:"";position:absolute;inset:0;
background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.28) 50%,transparent 65%);
transform:translateX(-130%);transition:transform .55s ease}
.btn:hover::after{transform:translateX(130%)}
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
.search:focus{border-color:var(--cyan);
box-shadow:0 0 0 3px rgba(34,211,238,.16),0 0 20px rgba(34,211,238,.12)}
.search::placeholder{color:#556180}
.secnav{display:flex;gap:8px;flex-wrap:wrap;font-size:13px;
position:sticky;top:40px;z-index:9;margin:10px -8px 4px;padding:8px;
background:rgba(10,14,26,.85);backdrop-filter:blur(10px);border-radius:12px}
.secnav a{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:4px 14px;color:var(--sub);transition:all .15s}
.secnav a:hover{color:var(--ink);border-color:var(--cyan);text-decoration:none;
box-shadow:var(--glow-cy)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:10px 16px;margin:8px 0;transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-2px);border-color:var(--line2);
box-shadow:var(--glow),0 12px 30px rgba(2,5,16,.5)}
.card .t{font-weight:600}
.card .m{font-size:12.5px;color:var(--sub);margin-top:2px}
.card .o{font-size:13px;color:#aeb9cf;margin-top:4px}
.cnt{color:var(--sub);font-size:13px;margin:8px 0}
.tickgrid{line-height:2.1}
.tickgrid a{display:inline-block;border:1px solid var(--line);background:var(--card);
border-radius:7px;padding:1px 10px;font-size:13px;margin:2px;font-weight:600;
font-family:var(--mono);transition:all .12s}
.tickgrid a:hover{text-decoration:none;transform:translateY(-1px);
border-color:var(--cyan);box-shadow:var(--glow-cy)}
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
.subh{font-size:12px;color:var(--sub);font-weight:700;margin:16px 0 6px;
letter-spacing:.14em;text-transform:uppercase;font-family:var(--mono)}
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
overflow:hidden;background-color:#070a14;
background-image:
radial-gradient(1px 1px at 24% 42%,rgba(226,236,255,.55) 50%,transparent 51%),
radial-gradient(1px 1px at 76% 18%,rgba(165,215,255,.45) 50%,transparent 51%),
radial-gradient(1.4px 1.4px at 52% 72%,rgba(196,181,253,.4) 50%,transparent 51%),
radial-gradient(600px 300px at 70% 20%,rgba(167,139,250,.09),transparent 60%),
repeating-linear-gradient(0deg,rgba(94,160,255,.022) 0 1px,transparent 1px 5px),
linear-gradient(160deg,#0e1526,#070a14);
background-size:180px 180px,260px 260px,360px 360px,100% 100%,auto,100% 100%}
.graphwrap::before,.graphwrap::after{content:"";position:absolute;width:22px;height:22px;
z-index:2;pointer-events:none}
.graphwrap::before{top:12px;left:12px;border-top:2px solid var(--cyan);
border-left:2px solid var(--cyan);opacity:.5}
.graphwrap::after{bottom:12px;right:12px;border-bottom:2px solid var(--accent2);
border-right:2px solid var(--accent2);opacity:.5}
.graphwrap canvas{display:block;width:100%;height:560px;position:relative;z-index:1}
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

<div style="display:flex;gap:8px;align-items:center;margin:16px 0 4px">
<input class="search" id="feedin" style="flex:1;margin:0" placeholder="📥 餵大腦：一句話 → 收件匣（Enter 送出，免終端機）…">
<button id="feedgo" style="padding:13px 20px;border:1px solid var(--line2);border-radius:12px;background:var(--accent);color:#0b1020;font-weight:700;font-size:15px;cursor:pointer;white-space:nowrap">送出</button></div>
<div id="feedmsg" class="cnt" style="margin:0 0 8px;min-height:1.3em"></div>
<script>
(function(){
  var inp=document.getElementById('feedin'),btn=document.getElementById('feedgo'),
      msg=document.getElementById('feedmsg'),
      // file:// 開的頁 origin=null，只能打絕對本機位址；經 server（bw http／Tailscale https）開則同源 /jot
      API=(location.protocol==='file:')?'http://127.0.0.1:8873/jot':'/jot';
  function send(){
    var t=(inp.value||'').trim();
    if(!t){inp.focus();return;}
    btn.disabled=true;msg.style.color='';msg.textContent='入腦中…';
    fetch(API,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:t})
      .then(function(r){if(!r.ok)throw 0;return r.json();})
      .then(function(){msg.style.color='var(--accent)';msg.textContent='✅ 已入腦（'+t.slice(0,40)+(t.length>40?'…':'')+'）';inp.value='';})
      .catch(function(){msg.style.color='#f0a35e';msg.textContent='⚠ server 未啟動——用 bj 或丟 BrainInbox 資料夾';})
      .finally(function(){btn.disabled=false;inp.focus();});
  }
  btn.addEventListener('click',send);
  inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();send();}});
})();
</script>
<input class="search" id="q" placeholder="全庫搜：ticker / 主題 / 標題 / oneliner…（深度全文用 q.py --search）">
<div class="secnav"><a href="#recent">🕐 最近更新</a><a href="#stocks">📈 個股導航</a>
<a href="#themes">🗺 主題地圖</a><a href="#shelf">📚 閒讀書架</a><a href="#all">全部</a>
<a href="munger.html" style="border-color:rgba(167,139,250,.5);color:#c4b5fd">🧭 蒙格清單</a>
<a href="dojo.html" style="border-color:rgba(34,211,238,.5);color:#67e8f9">🥋 道場</a>
<a href="gym.html" style="border-color:rgba(74,222,128,.5);color:#86efac">🏋️ 訓練場</a></div>
<div id="qresults"></div>

<h2>📬 今日重訪 <span class="cnt">大腦來找你——每天輪三樣</span></h2>
<div id="revisit" class="shelf"></div>

<h2 id="recent">🕐 最近更新</h2>
<div id="recentlist"></div>
<details id="recentmore"><summary class="cnt">更多近期報告…</summary>
<div id="recentrest"></div></details>

<h2 id="graph">🕸 知識星圖 <span class="cnt">現行裁決個股 × 產業主題 · hover 看連線 · 點節點跳 hub</span></h2>
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
<script id="fals-data" type="application/json">%%FALS%%</script>
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

/* 📬 今日重訪：日期種子輪三樣（未對帳假設 / 思維模型 / 30 天前舊筆記） */
(function(){
  const FALS=JSON.parse(document.getElementById('fals-data').textContent);
  function hsh(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
  const seed=hsh(new Date().toISOString().slice(0,10));
  const cards=[];
  if(FALS.length){
    const f=FALS[seed%FALS.length];
    const age=f.date?Math.round((Date.now()-new Date(f.date))/864e5):null;
    cards.push('<div class="card"><div class="m"><span class="badge">未對帳假設</span> '+
      e_(f.ticker||'')+(age!=null?' · '+age+' 天前寫下':'')+'</div>'+
      '<div class="o">'+e_(f.text)+'</div>'+
      '<div class="m">觸發了嗎？→ <a href="gym.html">獵場判定</a></div></div>');
  }
  const mms=DATA.filter(n=>n.t==='mental-model');
  if(mms.length){
    const m=mms[seed%mms.length];
    cards.push('<div class="card"><div class="m"><span class="badge">今日模型</span></div>'+
      '<div class="t"><a href="'+m.p+'">'+e_(m.title)+'</a></div>'+
      (m.one?'<div class="o">'+e_(m.one)+'</div>':'')+
      '<div class="m">今天在哪裡看到它？（bj 記一筆）</div></div>');
  }
  const old30=DATA.filter(n=>n.t==='usernote'&&n.d&&
    (Date.now()-new Date(n.d))/864e5>=21);
  const pastPool=old30.length?old30:DATA.filter(n=>n.t==='usernote');
  if(pastPool.length){
    const u=pastPool[seed%pastPool.length];
    cards.push('<div class="card"><div class="m"><span class="badge">過去的你</span> '+e_(u.d||'')+'</div>'+
      '<div class="t"><a href="'+u.p+'">'+e_(u.title)+'</a></div>'+
      '<div class="m">現在還同意當時的自己嗎？</div></div>');
  }else{
    cards.push('<div class="card"><div class="m"><span class="badge">過去的你</span></div>'+
      '<div class="o">還沒有你寫的筆記——去蒙格清單或訓練場寫第一則，30 天後它會回來找你。</div></div>');
  }
  document.getElementById('revisit').innerHTML=cards.join('');
})();

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
      /* 十字星芒（裝飾 flare，非資料色） */
      const fl=r+5*DPR;
      ctx.strokeStyle='rgba(226,236,255,'+(lit?0.5:0.16)+')';
      ctx.lineWidth=DPR;
      ctx.beginPath();ctx.moveTo(n.x-fl,n.y);ctx.lineTo(n.x+fl,n.y);
      ctx.moveTo(n.x,n.y-fl);ctx.lineTo(n.x,n.y+fl);ctx.stroke();
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

    fals = []
    fp = KDIR / "falsifiers.json"
    if fp.exists():
        try:
            fals = [{"ticker": i.get("ticker"), "date": i.get("date"),
                     "text": (i.get("text") or "")[:200]}
                    for i in json.loads(fp.read_text(encoding="utf-8")).get("items", [])]
        except (json.JSONDecodeError, OSError):
            pass

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
             .replace("%%KG%%", payload(kg))
             .replace("%%FALS%%", payload(fals)), encoding="utf-8")


MUNGER = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>決策前蒙格清單 · 第二大腦</title>
<link rel="stylesheet" href="assets/wiki.css">
<style>
.qcard{border:1px solid var(--line);border-radius:12px;background:var(--card);
padding:14px 18px;margin:10px 0;position:relative;overflow:hidden}
.qcard::before{content:"";position:absolute;top:0;left:0;right:0;height:1px;
background:linear-gradient(90deg,transparent,var(--cyan),transparent);opacity:.4}
.qcard .why{font-size:12px;color:#c4b5fd;background:rgba(167,139,250,.1);
border-radius:6px;padding:3px 10px;display:inline-block;margin-bottom:6px}
.qcard .ask{font-weight:700;font-size:15.5px;color:var(--ink)}
.qcard .nm{font-size:12px;color:var(--sub);margin:4px 0 8px}
.qcard textarea{width:100%;min-height:64px;background:rgba(10,14,26,.6);
border:1px solid var(--line);border-radius:8px;color:var(--ink);
padding:10px 12px;font-size:14px;font-family:inherit;line-height:1.6;resize:vertical}
.qcard textarea:focus{outline:none;border-color:var(--cyan);
box-shadow:0 0 0 3px rgba(34,211,238,.15)}
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


def _premortems(notes_by, cap=2200):
    """每 entity 取最新 DD 筆記的 §13 pre-mortem 摘錄（munger 對質區 / 道場殺手題共用）。"""
    pm = {}
    for ent_k, lst in notes_by.items():
        dd = next((n for n in lst if n["t"] == "dd"), None)
        if not dd:
            continue
        try:
            body = (VAULT / (dd["p"][:-5] + ".md")).read_text(encoding="utf-8")
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
        if len(seg) > cap:
            seg = seg[:cap] + "\n…（全文開 DD 筆記）"
        if seg:
            pm[ent_k] = seg
    return pm


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

    pm = _premortems(notes_by)

    def payload(o):
        return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

    (WIKI / "munger.html").write_text(
        MUNGER.replace("%%MODELS%%", payload(models))
              .replace("%%ENTS%%", payload(ents))
              .replace("%%ENTTHEMES%%", payload(ent_themes))
              .replace("%%NOTESBY%%", payload(notes_by))
              .replace("%%SETTLE%%", payload(settle))
              .replace("%%PM%%", payload(pm)), encoding="utf-8")


DOJO = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>商業模式道場 · 第二大腦</title>
<link rel="stylesheet" href="assets/wiki.css">
<style>
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
.tab{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:6px 16px;font-size:13.5px;cursor:pointer;color:var(--sub);user-select:none}
.tab.on{background:linear-gradient(92deg,#2f66c4,#5ea0ff);border-color:transparent;
color:#fff;box-shadow:0 2px 14px rgba(34,211,238,.35)}
.mode{display:none}.mode.on{display:block}
.qhead{font-family:var(--mono);font-size:1.5rem;font-weight:800;margin:4px 0}
.guessrow{display:grid;grid-template-columns:170px 1fr 90px;gap:12px;
align-items:center;margin:8px 0;font-size:14px}
.guessrow input[type=range]{width:100%;accent-color:#5ea0ff}
.guessrow input[type=number]{width:84px;background:rgba(10,14,26,.6);color:var(--ink);
border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:14px;
font-family:var(--mono)}
.gv{font-family:var(--mono);color:var(--ink);text-align:right}
table.rvl{width:100%;border-collapse:collapse;margin:10px 0;font-size:13.5px}
table.rvl td,table.rvl th{padding:6px 10px;border-bottom:1px solid var(--line);
text-align:right;font-family:var(--mono)}
table.rvl td:first-child,table.rvl th:first-child{text-align:left;font-family:inherit}
.hit{color:var(--go-t);font-weight:700}.missx{color:var(--avoid-t);font-weight:700}
.duelq{border:1px solid var(--line);border-radius:12px;background:var(--card);
padding:12px 16px;margin:10px 0}
.duelbtns{display:flex;gap:10px;margin-top:8px}
.duelbtns button{flex:1;padding:10px;border-radius:10px;border:1px solid var(--line2);
background:var(--cardsolid);color:var(--ink);font-size:15px;font-weight:700;
font-family:var(--mono);cursor:pointer}
.duelbtns button:hover{border-color:var(--accent)}
.duelbtns button.win{border-color:var(--go);background:rgba(22,163,74,.15)}
.duelbtns button.lose{border-color:var(--avoid);background:rgba(220,38,38,.12)}
.streak{font-family:var(--mono);font-size:14px;color:var(--hold-t)}
.pmbox{border:1px solid rgba(220,38,38,.35);background:rgba(220,38,38,.05);
border-radius:12px;padding:14px 18px;margin:10px 0;font-size:13.5px;line-height:1.8;
max-height:320px;overflow-y:auto;white-space:pre-wrap}
.qcard textarea,textarea.big{width:100%;min-height:80px;background:rgba(10,14,26,.6);
border:1px solid var(--line);border-radius:8px;color:var(--ink);padding:10px 12px;
font-size:14px;font-family:inherit;line-height:1.6;resize:vertical}
.statgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.mapwrap{position:relative;border:1px solid var(--line);border-radius:14px;overflow:hidden;
background-color:#070a14;
background-image:
radial-gradient(1px 1px at 30% 26%,rgba(226,236,255,.5) 50%,transparent 51%),
radial-gradient(1px 1px at 70% 66%,rgba(165,215,255,.4) 50%,transparent 51%),
repeating-linear-gradient(0deg,rgba(94,160,255,.022) 0 1px,transparent 1px 5px),
linear-gradient(160deg,#0e1526,#070a14);
background-size:190px 190px,300px 300px,auto,100% 100%}
.mapwrap::before,.mapwrap::after{content:"";position:absolute;width:20px;height:20px;
z-index:2;pointer-events:none}
.mapwrap::before{top:10px;left:10px;border-top:2px solid var(--cyan);
border-left:2px solid var(--cyan);opacity:.5}
.mapwrap::after{bottom:10px;right:10px;border-bottom:2px solid var(--accent2);
border-right:2px solid var(--accent2);opacity:.5}
.mapwrap canvas{display:block;width:100%;height:460px;cursor:crosshair;
position:relative;z-index:1}
.maptip{position:absolute;pointer-events:none;background:var(--cardsolid);
border:1px solid var(--line2);border-radius:8px;padding:6px 10px;font-size:12.5px;
font-family:var(--mono);display:none;z-index:5}
.ctx{color:var(--sub);font-size:13px;margin:4px 0 12px}
.btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}
</style></head>
<body><div class="top"><a href="index.html">🧠 <b>第二大腦</b></a>
<span class="dim">🥋 商業模式道場</span></div>
<main>
<h1>🥋 商業模式道場</h1>
<p class="cnt">敏銳度＝先猜、再對答案、追蹤誤差。題庫是你自己的 DD（答案卡＝分析時落下的護城河評分與市場倍數）。
先猜完才准看庫內答案——猜錯的痛感就是訓練。</p>
<div class="tabs">
<span class="tab on" data-m="blind">🎯 盲測</span>
<span class="tab" data-m="duel">⚔️ 對決</span>
<span class="tab" data-m="kill">💀 殺手題</span>
<span class="tab" data-m="map">🗺 品質×倍數地圖</span>
<span class="tab" data-m="stats">📊 校準紀錄</span>
</div>

<div class="mode on" id="m-blind"></div>
<div class="mode" id="m-duel"></div>
<div class="mode" id="m-kill"></div>
<div class="mode" id="m-map">
<p class="ctx">每個點＝一份最新 DD。橫軸護城河總分、縱軸市場給的 Fwd P/E（FY2）。
先在腦中畫出「品質應該值幾倍」的線，再看哪些點偏離——偏離處就是市場觀點與你觀點的分歧。hover 看名字、點擊進 hub。</p>
<div class="mapwrap"><canvas id="map"></canvas><div class="maptip" id="maptip"></div></div>
</div>
<div class="mode" id="m-stats"></div>

<script id="d-dojo" type="application/json">%%DOJO%%</script>
<script id="d-pm" type="application/json">%%PM%%</script>
<script>
const POOL=JSON.parse(document.getElementById('d-dojo').textContent);
const PM=JSON.parse(document.getElementById('d-pm').textContent);
function e_(s){const d=document.createElement('span');d.textContent=s==null?'':s;return d.innerHTML}
const VCL={'進場':'v-go','觀望':'v-hold','迴避':'v-avoid'};
function H(tk){return localStorage.getItem('dojo_'+tk)}
function hist(){try{return JSON.parse(localStorage.getItem('dojo_hist')||'{}')}catch(e){return{}}}
function saveHist(h){localStorage.setItem('dojo_hist',JSON.stringify(h))}
function pick(arr){return arr[Math.floor(Math.random()*arr.length)]}

/* tabs */
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
  document.querySelectorAll('.mode').forEach(x=>x.classList.remove('on'));
  t.classList.add('on');document.getElementById('m-'+t.dataset.m).classList.add('on');
  if(t.dataset.m==='stats')renderStats();
  if(t.dataset.m==='map')drawMap();
}));

/* ═══ 🎯 盲測 ═══ */
const METRICS=[
  {id:'moat', name:'護城河總分', min:0,max:10,step:.5, tol:1, get:x=>x.moat},
  {id:'pp',   name:'定價權',     min:0,max:10,step:.5, tol:1, get:x=>x.pp},
  {id:'gd',   name:'成長持久度', min:0,max:10,step:.5, tol:1, get:x=>x.gd},
  {id:'fpe',  name:'Fwd P/E（市場給幾倍）', min:0,max:80,step:.5, tol:'rel20', get:x=>x.fpe},
  {id:'pct5', name:'5Y P/E 分位（現在貴嗎 0-100）', min:0,max:100,step:1, tol:15, get:x=>x.pct5}
];
let bq=null;
function blindPool(){return POOL.filter(x=>x.moat!=null&&x.pp!=null&&x.gd!=null)}
function newBlind(){
  const bp=blindPool();
  if(!bp.length){document.getElementById('m-blind').innerHTML='<p class="cnt">題庫為空——先跑 python knowledge/brain_build.py --full</p>';return}
  bq=pick(bp);
  const ms=METRICS.filter(m=>m.get(bq)!=null);
  let h='<div class="filecard"><div class="qhead">'+e_(bq.k)+'</div>'+
    '<div class="ctx">'+e_(bq.title)+'</div>'+
    (bq.themes.length?'<div class="ctx">掛在：'+bq.themes.slice(0,5).map(e_).join(' · ')+'</div>':'')+
    '<p class="cnt">憑你對這門生意的理解作答（不要先開報告）：</p>'+
    ms.map(m=>'<div class="guessrow"><span>'+m.name+'</span>'+
      '<input type="range" min="'+m.min+'" max="'+m.max+'" step="'+m.step+'" value="'+((m.min+m.max)/2)+'" data-g="'+m.id+'">'+
      '<span class="gv" data-v="'+m.id+'">'+((m.min+m.max)/2)+'</span></div>').join('')+
    '<div class="btnrow"><a class="btn" href="#" id="rvl">揭曉答案卡</a>'+
    '<a class="btn sec" href="#" id="skip">換一題</a></div>'+
    '<div id="rvlout"></div></div>';
  document.getElementById('m-blind').innerHTML=h;
  document.querySelectorAll('#m-blind input[type=range]').forEach(r=>{
    r.addEventListener('input',()=>{
      document.querySelector('.gv[data-v="'+r.dataset.g+'"]').textContent=r.value})});
  document.getElementById('skip').addEventListener('click',e=>{e.preventDefault();newBlind()});
  document.getElementById('rvl').addEventListener('click',e=>{e.preventDefault();reveal(ms)});
}
function reveal(ms){
  const h=hist();h.blind=h.blind||{};
  let rows='',hits=0;
  ms.forEach(m=>{
    const g=parseFloat(document.querySelector('input[data-g="'+m.id+'"]').value);
    const a=m.get(bq);
    const err=Math.abs(g-a);
    const ok=(m.tol==='rel20')?err<=Math.abs(a)*.2:err<=m.tol;
    if(ok)hits++;
    (h.blind[m.id]=h.blind[m.id]||[]).push(+err.toFixed(1));
    if(h.blind[m.id].length>60)h.blind[m.id]=h.blind[m.id].slice(-60);
    rows+='<tr><td>'+m.name+'</td><td>'+g+'</td><td>'+a+'</td>'+
      '<td class="'+(ok?'hit':'missx')+'">'+(ok?'✓':'±'+err.toFixed(1))+'</td></tr>';
  });
  h.blindN=(h.blindN||0)+1;saveHist(h);
  document.getElementById('rvlout').innerHTML=
    '<table class="rvl"><tr><th></th><th>你猜</th><th>DD 答案</th><th>判定</th></tr>'+rows+'</table>'+
    '<p class="cnt">本題 '+hits+'/'+ms.length+' 中。DD 的一句話：</p>'+
    '<div class="filecard" style="margin:8px 0"><div class="ctx">'+e_(bq.one||'—')+'</div>'+
    '<div class="actions"><a class="btn sec" href="'+bq.hub+'">個股 hub</a>'+
    (bq.dd?'<a class="btn sec" href="'+bq.dd+'">DD 筆記</a>':'')+'</div></div>'+
    '<p class="cnt">誤差大的那格，去讀報告找「你沒看到的東西」——那就是敏銳度的缺口。</p>'+
    '<div class="btnrow"><a class="btn" href="#" id="nextb">下一題 →</a></div>';
  document.getElementById('nextb').addEventListener('click',e=>{e.preventDefault();newBlind()});
}

/* ═══ ⚔️ 對決 ═══ */
let duel=null,streak=0;
const DUELQ=[
  {name:'誰的護城河總分更高？',get:x=>x.moat},
  {name:'市場給誰更高的 Fwd P/E？',get:x=>x.fpe},
  {name:'誰的品質分更高？',get:x=>x.qs},
  {name:'誰的成長持久度更高？',get:x=>x.gd}
];
function themePairs(){
  const byTheme={};
  POOL.forEach(x=>x.themes.forEach(t=>{(byTheme[t]=byTheme[t]||[]).push(x)}));
  return Object.entries(byTheme).filter(([t,l])=>l.length>=2);
}
function newDuel(){
  const cand=themePairs();
  if(!cand.length){document.getElementById('m-duel').innerHTML='<p class="cnt">題庫不足。</p>';return}
  for(let tries=0;tries<50;tries++){
    const [theme,list]=pick(cand);
    const a=pick(list);let b=pick(list);
    if(a.k===b.k)continue;
    const qs=DUELQ.filter(q=>q.get(a)!=null&&q.get(b)!=null&&q.get(a)!==q.get(b));
    if(!qs.length)continue;
    duel={theme,a,b,qs,i:0};break;
  }
  renderDuel();
}
function renderDuel(){
  const d=duel,q=d.qs[d.i];
  document.getElementById('m-duel').innerHTML=
    '<p class="ctx">同主題對決：<b>'+e_(d.theme)+'</b> · <span class="streak">連勝 '+streak+'</span></p>'+
    '<div class="duelq"><div class="ask" style="font-weight:700">'+q.name+'</div>'+
    '<div class="duelbtns"><button data-s="a">'+e_(d.a.k)+'</button>'+
    '<button data-s="b">'+e_(d.b.k)+'</button></div><div id="duelout"></div></div>';
  document.querySelectorAll('.duelbtns button').forEach(btn=>btn.addEventListener('click',()=>{
    const va=q.get(d.a),vb=q.get(d.b);
    const win=(va>vb)?'a':'b';
    const okpick=btn.dataset.s===win;
    document.querySelectorAll('.duelbtns button').forEach(x=>{
      x.disabled=true;
      x.classList.add(x.dataset.s===win?'win':'lose');
      x.textContent+=' — '+(x.dataset.s==='a'?va:vb);
    });
    const h=hist();h.duelN=(h.duelN||0)+1;h.duelWin=(h.duelWin||0)+(okpick?1:0);
    streak=okpick?streak+1:0;h.duelBest=Math.max(h.duelBest||0,streak);saveHist(h);
    document.getElementById('duelout').innerHTML=
      '<p class="cnt">'+(okpick?'✓ 對。':'✗ 錯——記住這對比，這就是格柵的一格。')+
      ' <a href="'+d.a.hub+'">'+e_(d.a.k)+' hub</a> · <a href="'+d.b.hub+'">'+e_(d.b.k)+' hub</a></p>'+
      '<div class="btnrow"><a class="btn" href="#" id="nextd">下一局 →</a></div>';
    document.getElementById('nextd').addEventListener('click',e=>{e.preventDefault();
      d.i++;if(d.i<d.qs.length)renderDuel();else newDuel()});
  }));
}

/* ═══ 💀 殺手題 ═══ */
let kq=null;
function newKill(){
  const pool=POOL.filter(x=>PM[x.k]);
  if(!pool.length){document.getElementById('m-kill').innerHTML='<p class="cnt">沒有 pre-mortem 題庫。</p>';return}
  kq=pick(pool);
  document.getElementById('m-kill').innerHTML=
    '<div class="filecard"><div class="qhead">'+e_(kq.k)+'</div>'+
    '<div class="ctx">'+e_(kq.title)+'</div>'+
    (kq.themes.length?'<div class="ctx">掛在：'+kq.themes.slice(0,5).map(e_).join(' · ')+'</div>':'')+
    '<p class="cnt"><b>這門生意 3 年後死掉，訃聞怎麼寫？</b>寫 ≥30 字（具體機制，不是「競爭變激烈」）：</p>'+
    '<textarea class="big" id="killta"></textarea>'+
    '<div class="btnrow"><a class="btn" href="#" id="killrvl">跟 DD 的 pre-mortem 對答案</a>'+
    '<a class="btn sec" href="#" id="killskip">換一題</a></div><div id="killout"></div></div>';
  document.getElementById('killskip').addEventListener('click',e=>{e.preventDefault();newKill()});
  document.getElementById('killrvl').addEventListener('click',e=>{
    e.preventDefault();
    const ta=document.getElementById('killta');
    if(ta.value.trim().length<30){ta.style.borderColor='var(--avoid)';return}
    document.getElementById('killout').innerHTML=
      '<div class="pmbox">'+e_(PM[kq.k])+'</div>'+
      '<p class="cnt">自評：你寫的死法有出現在上面嗎？</p>'+
      '<div class="btnrow"><a class="btn sec" href="#" data-sg="1">✓ 抓到核心死法</a>'+
      '<a class="btn sec" href="#" data-sg="0">✗ 漏了——這是盲點</a></div>';
    document.querySelectorAll('[data-sg]').forEach(b=>b.addEventListener('click',ev=>{
      ev.preventDefault();
      const h=hist();h.killN=(h.killN||0)+1;h.killHit=(h.killHit||0)+(+b.dataset.sg);saveHist(h);
      document.getElementById('killout').insertAdjacentHTML('beforeend',
        '<div class="btnrow"><a class="btn" href="#" id="nextk">下一題 →</a>'+
        (kq.dd?'<a class="btn sec" href="'+kq.dd+'">開完整 DD</a>':'')+'</div>');
      document.getElementById('nextk').addEventListener('click',x=>{x.preventDefault();newKill()});
    }));
  });
}

/* ═══ 📊 校準紀錄 ═══ */
function renderStats(){
  const h=hist();
  let cards='';
  cards+='<div class="tile"><div class="n">'+(h.blindN||0)+'</div><div class="l">盲測題數</div></div>';
  (h.blind?METRICS:[]).forEach(m=>{
    const arr=(h.blind[m.id]||[]);
    if(!arr.length)return;
    const mean=(arr.reduce((a,b)=>a+b,0)/arr.length);
    const half=Math.floor(arr.length/2)||1;
    const early=arr.slice(0,half),late=arr.slice(half);
    const em=early.reduce((a,b)=>a+b,0)/early.length,lm=late.reduce((a,b)=>a+b,0)/(late.length||1);
    const trend=late.length&&lm<em?'↓ 在進步':'→';
    cards+='<div class="tile"><div class="n">±'+mean.toFixed(1)+'</div>'+
      '<div class="l">'+m.name+' 平均誤差 '+trend+'</div></div>';
  });
  cards+='<div class="tile"><div class="n">'+(h.duelWin||0)+'/'+(h.duelN||0)+'</div><div class="l">對決勝率 · 最佳連勝 '+(h.duelBest||0)+'</div></div>';
  cards+='<div class="tile"><div class="n">'+(h.killHit||0)+'/'+(h.killN||0)+'</div><div class="l">殺手題命中（自評）</div></div>';
  document.getElementById('m-stats').innerHTML=
    '<p class="ctx">敏銳度的證據不是感覺，是誤差在收斂。盲測誤差 ↓、對決勝率 ↑、殺手題命中 ↑ ＝格柵在長。</p>'+
    '<div class="statgrid">'+cards+'</div>'+
    '<div class="btnrow"><a class="btn" href="#" id="bkup">⬇ 備份全部訓練紀錄 .md</a>'+
    '<a class="btn sec" href="#" id="wipe">清空盲測紀錄重練</a>'+
    '<span class="cnt">備份含道場/訓練場/蒙格清單全部 localStorage——收進 vault/notes/training/ 後兩台機都找得回</span></div>';
  document.getElementById('bkup').addEventListener('click',e=>{
    e.preventDefault();
    const dump={};
    for(let i=0;i<localStorage.length;i++){
      const k=localStorage.key(i);
      if(/^(dojo_|gym_|munger2_)/.test(k))dump[k]=localStorage.getItem(k);}
    const d=new Date().toISOString().slice(0,10);
    const md=['---','type: usernote','title: "訓練紀錄備份 · '+d+'"','date: '+d,
      'tags: [training-backup]','---','','# 訓練紀錄備份 · '+d,'',
      '還原：開瀏覽器 console，對下面 JSON 逐 key 執行 localStorage.setItem(k, v)。','',
      '```json',JSON.stringify(dump,null,1),'```'].join(String.fromCharCode(10));
    const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([md],{type:'text/markdown'}));
    a.download='TRAINING_BACKUP_'+d.replace(/-/g,'')+'.md';a.click();});
  document.getElementById('wipe').addEventListener('click',e=>{e.preventDefault();
    localStorage.removeItem('dojo_hist');renderStats()});
}

/* ═══ 🗺 品質×倍數地圖 ═══ */
const VC={'進場':'#16a34a','觀望':'#d97706','迴避':'#dc2626'};
let mapPts=[];
function drawMap(){
  const cv=document.getElementById('map'),ctx=cv.getContext('2d'),DPR=devicePixelRatio;
  const W=cv.width=cv.offsetWidth*DPR,Hh=cv.height=cv.offsetHeight*DPR;
  const data=POOL.filter(x=>x.moat!=null&&x.fpe!=null&&x.fpe>0&&x.fpe<=80);
  const padL=46*DPR,padB=34*DPR,padT=16*DPR,padR=16*DPR;
  const X=v=>padL+(v/10)*(W-padL-padR);
  const Y=v=>Hh-padB-(v/80)*(Hh-padT-padB);
  ctx.clearRect(0,0,W,Hh);
  ctx.strokeStyle='rgba(148,163,184,.12)';ctx.fillStyle='rgba(139,152,179,.8)';
  ctx.font=(10.5*DPR)+'px SF Mono,Menlo,monospace';ctx.lineWidth=DPR;
  for(let m=0;m<=10;m+=2){ctx.beginPath();ctx.moveTo(X(m),padT);ctx.lineTo(X(m),Hh-padB);ctx.stroke();
    ctx.fillText(m,X(m)-3*DPR,Hh-padB+16*DPR)}
  for(let p=0;p<=80;p+=20){ctx.beginPath();ctx.moveTo(padL,Y(p));ctx.lineTo(W-padR,Y(p));ctx.stroke();
    ctx.fillText(p+'x',padL-30*DPR,Y(p)+4*DPR)}
  ctx.fillText('護城河總分 →',W/2-40*DPR,Hh-6*DPR);
  ctx.save();ctx.translate(12*DPR,Hh/2+40*DPR);ctx.rotate(-Math.PI/2);
  ctx.fillText('Fwd P/E（FY2）→',0,0);ctx.restore();
  mapPts=[];
  data.forEach(x=>{
    const jx=X(Math.min(10,x.moat+(hash(x.k)%100-50)/250)),jy=Y(x.fpe);
    ctx.save();
    ctx.fillStyle=VC[x.v]||'#3b5aa0';
    ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=6*DPR;
    ctx.globalAlpha=.9;
    ctx.beginPath();ctx.arc(jx,jy,4.5*DPR,0,7);ctx.fill();ctx.restore();
    mapPts.push({x:jx,y:jy,d:x});
  });
  cv.onmousemove=e=>{
    const r=cv.getBoundingClientRect(),mx=(e.clientX-r.left)*DPR,my=(e.clientY-r.top)*DPR;
    const hit=mapPts.find(p=>Math.hypot(p.x-mx,p.y-my)<8*DPR);
    const tip=document.getElementById('maptip');
    if(hit){tip.style.display='block';
      tip.style.left=(e.clientX-r.left+14)+'px';tip.style.top=(e.clientY-r.top-10)+'px';
      tip.innerHTML=e_(hit.d.k)+' · 護城河 '+hit.d.moat+' · '+hit.d.fpe+'x'+
        (hit.d.v?' · '+e_(hit.d.v):'');cv.style.cursor='pointer'}
    else{tip.style.display='none';cv.style.cursor='crosshair'}
  };
  cv.onclick=e=>{
    const r=cv.getBoundingClientRect(),mx=(e.clientX-r.left)*DPR,my=(e.clientY-r.top)*DPR;
    const hit=mapPts.find(p=>Math.hypot(p.x-mx,p.y-my)<8*DPR);
    if(hit)location.href=hit.d.hub;
  };
}
function hash(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}

newBlind();newDuel();newKill();
</script></main></body></html>
"""


def build_dojo(summaries, stems, graph):
    """商業模式道場：盲測/對決/殺手題/品質×倍數地圖（答案卡＝dd-meta）。"""
    latest = {}
    for s in sorted(summaries, key=lambda s: s.get("date") or ""):
        if s["type"] == "dd" and s.get("entity"):
            latest[s["entity"]] = s
    ent_themes = {}
    for e in graph.get("edges", []):
        if e.get("rel") == "belongs_to":
            lst = ent_themes.setdefault(e["from"], [])
            if e["to"] not in lst:
                lst.append(e["to"])
    pool = []
    notes_by = {}
    for k, s in latest.items():
        x = s.get("extra") or {}
        hub = stems.get(k)
        if not hub or x.get("moat_score") is None:
            continue
        ddp = stems.get(Path(s["note"]).stem)

        def num(key):
            try:
                v = float(x.get(key))
                return round(v, 2)
            except (TypeError, ValueError):
                return None

        pool.append({
            "k": k, "title": (s.get("title") or "")[:110],
            "v": s.get("verdict"), "one": (s.get("oneliner") or "")[:220],
            "moat": num("moat_score"), "pp": num("moat_pricing_power"),
            "gd": num("growth_durability"), "qs": num("quality_score"),
            "fpe": num("fpe_fy2"), "pct5": num("pct_5y"),
            "hub": hub, "dd": ddp, "themes": ent_themes.get(k, [])[:8]})
        notes_by[k] = [{"t": "dd", "p": ddp}] if ddp else []
    pm = _premortems(notes_by)

    def payload(o):
        return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

    (WIKI / "dojo.html").write_text(
        DOJO.replace("%%DOJO%%", payload(pool)).replace("%%PM%%", payload(pm)),
        encoding="utf-8")


GYM = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>思考訓練場 · 第二大腦</title>
<link rel="stylesheet" href="assets/wiki.css">
<style>
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
.tab{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:6px 16px;font-size:13.5px;cursor:pointer;color:var(--sub);user-select:none}
.tab.on{background:linear-gradient(92deg,#2f66c4,#5ea0ff);border-color:transparent;
color:#fff;box-shadow:0 2px 14px rgba(34,211,238,.35)}
.mode{display:none}.mode.on{display:block}
.ctx{color:var(--sub);font-size:13px;margin:4px 0 12px}
.btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0;align-items:center}
textarea{width:100%;min-height:70px;background:rgba(10,14,26,.6);
border:1px solid var(--line);border-radius:8px;color:var(--ink);padding:10px 12px;
font-size:14px;font-family:inherit;line-height:1.6;resize:vertical}
textarea:focus{outline:none;border-color:var(--cyan);
box-shadow:0 0 0 3px rgba(34,211,238,.13)}
select,input.pick{background:var(--cardsolid);color:var(--ink);
border:1px solid var(--line2);border-radius:8px;padding:8px 12px;font-size:14px}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:720px){.duo{grid-template-columns:1fr}}
.col{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;
position:relative;overflow:hidden}
.col::before{content:"";position:absolute;top:0;left:0;right:0;height:1px;
background:linear-gradient(90deg,transparent,var(--cyan),transparent);opacity:.4}
.col .tk{font-family:var(--mono);font-size:1.3rem;font-weight:800}
table.mx{width:100%;border-collapse:collapse;font-size:13.5px;margin:8px 0}
table.mx td{padding:5px 8px;border-bottom:1px solid var(--line);font-family:var(--mono);text-align:right}
table.mx td:first-child{text-align:left;font-family:inherit;color:var(--sub)}
.dwin{color:var(--go-t);font-weight:700}
.tl{border-left:2px solid var(--line2);margin:14px 0 14px 8px;padding-left:18px}
.tlrow{position:relative;margin:0 0 16px}
.tlrow::before{content:"";position:absolute;left:-24px;top:6px;width:10px;height:10px;
border-radius:50%;background:#3b5aa0;box-shadow:0 0 8px rgba(94,160,255,.5)}
.tlrow.flip::before{background:#d97706;box-shadow:0 0 10px rgba(217,119,6,.7)}
.flipnote{color:var(--hold-t);font-size:12.5px;font-weight:700}
.pmbox{border:1px solid rgba(220,38,38,.35);background:rgba(220,38,38,.05);
border-radius:12px;padding:14px 18px;margin:10px 0;font-size:13.5px;line-height:1.8;
max-height:320px;overflow-y:auto;white-space:pre-wrap}
.q2x2{display:grid;grid-template-columns:1fr 1fr;gap:8px;max-width:560px}
.q2x2 a{border:1px solid var(--line2);border-radius:10px;padding:10px;text-align:center;
color:var(--ink);font-size:13.5px}
.q2x2 a:hover{border-color:var(--accent);text-decoration:none}
table.hunt{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0}
table.hunt th{color:var(--sub);font-weight:600;text-align:left;padding:6px 8px;
border-bottom:1px solid var(--line2)}
table.hunt td{padding:6px 8px;border-bottom:1px solid var(--line);font-family:var(--mono)}
table.hunt tr:hover{background:rgba(94,160,255,.05)}
.claim{font-size:12px;color:var(--accent);cursor:pointer}
.claimbox{margin:6px 0 12px}
.subtabs{display:flex;gap:8px;margin:8px 0}
.subtabs span{border:1px solid var(--line);border-radius:8px;padding:3px 12px;
font-size:12.5px;color:var(--sub);cursor:pointer}
.subtabs span.on{border-color:var(--accent);color:var(--accent)}
.wc{font-size:11px;color:#556180;text-align:right;font-family:var(--mono)}
.rvlone{background:rgba(94,160,255,.07);border-left:3px solid var(--accent);
padding:10px 14px;border-radius:0 8px 8px 0;margin:10px 0;font-size:14px;color:#c6d0e2}
</style></head>
<body><div class="top"><a href="index.html">🧠 <b>第二大腦</b></a>
<span class="dim">🏋️ 思考訓練場（非問答式）</span></div>
<main>
<h1>🏋️ 思考訓練場</h1>
<p class="cnt">四種非問答式訓練：並排看出模式（對照）、過程與結果分離（時光機）、自己生問題（狩獵）、輸出組織思想（寫作）。用一輪就知道哪個對你最有效。</p>
<div class="tabs">
<span class="tab on" data-m="cmp">🔍 對照室</span>
<span class="tab" data-m="replay">⏪ 時光機</span>
<span class="tab" data-m="hunt">🎯 異常狩獵</span>
<span class="tab" data-m="write">✍️ 寫作間</span>
</div>
<div class="mode on" id="m-cmp"></div>
<div class="mode" id="m-replay"></div>
<div class="mode" id="m-hunt"></div>
<div class="mode" id="m-write"></div>

<script id="g-dd" type="application/json">%%ALLDD%%</script>
<script id="g-ents" type="application/json">%%ENTS%%</script>
<script id="g-eth" type="application/json">%%ETH%%</script>
<script id="g-settle" type="application/json">%%SETTLE%%</script>
<script id="g-pm" type="application/json">%%PM%%</script>
<script id="g-crit" type="application/json">%%CRIT%%</script>
<script>
const DD=JSON.parse(document.getElementById('g-dd').textContent);
const ENTS=JSON.parse(document.getElementById('g-ents').textContent);
const ETH=JSON.parse(document.getElementById('g-eth').textContent);
const ST=JSON.parse(document.getElementById('g-settle').textContent);
const PM=JSON.parse(document.getElementById('g-pm').textContent);
const CRIT=JSON.parse(document.getElementById('g-crit').textContent);
function e_(s){const d=document.createElement('span');d.textContent=s==null?'':s;return d.innerHTML}
const VCL={'進場':'v-go','觀望':'v-hold','迴避':'v-avoid'};
function vb(v){return v?'<b class="'+(VCL[v]||'')+'">'+e_(v)+'</b>':'—'}
function pick(a){return a[Math.floor(Math.random()*a.length)]}
const byEnt={};DD.forEach(d=>{(byEnt[d.k]=byEnt[d.k]||[]).push(d)});
Object.values(byEnt).forEach(l=>l.sort((a,b)=>(a.d||'').localeCompare(b.d||'')));
const latest={};Object.entries(byEnt).forEach(([k,l])=>latest[k]=l[l.length-1]);
const ENTMAP={};ENTS.forEach(t=>ENTMAP[t.k]=t);
function dlOpts(){return Object.keys(byEnt).sort().map(k=>'<option value="'+k+'">').join('')}
function exportMd(fname,lines){
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([lines.join(String.fromCharCode(10))],{type:'text/markdown'}));
  a.download=fname;a.click();}
function today(){return new Date().toISOString().slice(0,10)}
function fmnote(kind,tk,extra){return ['---','type: usernote',
  'title: "'+kind+' · '+tk+' · '+today()+'"','ticker: '+tk,'date: '+today(),
  'tags: [gym]','---','','# '+kind+' · '+tk+' · '+today(),'','所屬：[['+tk+']]',''].concat(extra,
  ['','---','（由 wiki/gym.html 匯出；存 knowledge/vault/notes/gym/ 後 rebuild 入腦）'])}

/* tabs */
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
  document.querySelectorAll('.mode').forEach(x=>x.classList.remove('on'));
  t.classList.add('on');document.getElementById('m-'+t.dataset.m).classList.add('on');
}));

/* ═══ 🔍 對照室 ═══ */
const CMPM=[['moat','護城河總分'],['pp','定價權'],['gd','成長持久度'],['qs','品質分'],
  ['fpe','Fwd P/E'],['pct5','5Y P/E 分位']];
function colHtml(x){
  if(!x)return '<div class="col"><p class="cnt">選一檔</p></div>';
  const ent=ENTMAP[x.k]||{};
  return '<div class="col"><div class="tk">'+e_(x.k)+'</div>'+
    '<div class="ctx">'+e_(x.title)+'</div>'+
    '<div class="ctx">'+vb(x.v)+' · '+e_(x.d||'')+'</div>'+
    (x.one?'<div class="rvlone">'+e_(x.one)+'</div>':'')+
    '<div class="btnrow">'+(ent.p?'<a class="btn sec" href="'+ent.p+'">hub</a>':'')+
    (x.p?'<a class="btn sec" href="'+x.p+'">DD 筆記</a>':'')+'</div></div>';
}
function cmpTable(a,b){
  if(!a||!b)return '';
  let rows='';
  CMPM.forEach(([f,name])=>{
    const va=a[f],vc=b[f];
    if(va==null&&vc==null)return;
    const aw=(va!=null&&vc!=null&&va>vc),bw=(va!=null&&vc!=null&&vc>va);
    rows+='<tr><td>'+name+'</td><td class="'+(aw?'dwin':'')+'">'+(va==null?'—':va)+
      '</td><td class="'+(bw?'dwin':'')+'">'+(vc==null?'—':vc)+'</td></tr>';});
  return '<table class="mx"><tr><td></td><td style="font-family:var(--mono)">'+e_(a.k)+
    '</td><td style="font-family:var(--mono)">'+e_(b.k)+'</td></tr>'+rows+'</table>'+
    '<p class="cnt">自問：分數差最大的那一列，差在生意結構的哪裡？如果你只能持有一檔 10 年，選哪檔、為什麼不是另一檔？</p>';
}
let cmpA=null,cmpB=null,cmpMode='pair';
function renderCmp(){
  const el=document.getElementById('m-cmp');
  let h='<div class="subtabs"><span class="'+(cmpMode==='pair'?'on':'')+'" data-s="pair">同業並排</span>'+
    '<span class="'+(cmpMode==='time'?'on':'')+'" data-s="time">同檔穿時空</span></div>';
  if(cmpMode==='pair'){
    h+='<p class="ctx">並排是建格柵最快的方式：同一條產業鏈，為什麼評分差這麼多？</p>'+
      '<div class="btnrow"><input class="pick" id="ca" list="gdl" placeholder="A 檔" value="'+(cmpA?cmpA.k:'')+'">'+
      '<input class="pick" id="cb" list="gdl" placeholder="B 檔" value="'+(cmpB?cmpB.k:'')+'">'+
      '<a class="btn" href="#" id="rndpair">🎲 隨機同主題一對</a></div>'+
      '<datalist id="gdl">'+dlOpts()+'</datalist>'+
      '<div class="duo">'+colHtml(cmpA)+colHtml(cmpB)+'</div>'+cmpTable(cmpA,cmpB);
  }else{
    const multi=Object.entries(byEnt).filter(([k,l])=>l.length>=2).map(([k])=>k).sort();
    h+='<p class="ctx">同一家公司穿時空：裁決翻面那一刻，是什麼證據進來了？（'+multi.length+' 檔有 ≥2 份 DD）</p>'+
      '<div class="btnrow"><input class="pick" id="ct" list="mdl" placeholder="輸入 ticker">'+
      '<a class="btn" href="#" id="rndt">🎲 隨機</a></div>'+
      '<datalist id="mdl">'+multi.map(k=>'<option value="'+k+'">').join('')+'</datalist>'+
      '<div id="tlout"></div>';
  }
  el.innerHTML=h;
  el.querySelectorAll('.subtabs span').forEach(s=>s.addEventListener('click',()=>{
    cmpMode=s.dataset.s;renderCmp()}));
  if(cmpMode==='pair'){
    ['ca','cb'].forEach((id,i)=>document.getElementById(id).addEventListener('change',e=>{
      const x=latest[e.target.value.toUpperCase()];
      if(i===0)cmpA=x;else cmpB=x;renderCmp()}));
    document.getElementById('rndpair').addEventListener('click',e=>{
      e.preventDefault();
      const themes={};Object.keys(latest).forEach(k=>(ETH[k]||[]).forEach(t=>{
        (themes[t.name]=themes[t.name]||[]).push(k)}));
      const cand=Object.values(themes).filter(l=>l.length>=2);
      if(!cand.length)return;
      const l=pick(cand);cmpA=latest[pick(l)];
      do{cmpB=latest[pick(l)]}while(cmpB.k===cmpA.k);
      renderCmp()});
  }else{
    function tl(tk){
      const l=byEnt[tk];if(!l||l.length<2){document.getElementById('tlout').innerHTML='<p class="cnt">此檔不足 2 份 DD。</p>';return}
      let h2='<div class="tl">',prev=null;
      l.forEach(x=>{
        const flip=prev&&prev.v&&x.v&&prev.v!==x.v;
        h2+='<div class="tlrow'+(flip?' flip':'')+'">'+
          '<b style="font-family:var(--mono)">'+e_(x.d||'')+'</b> '+vb(x.v)+
          (x.g?' · '+e_(x.g):'')+(x.fpe?' · '+x.fpe+'x':'')+
          (flip?' <span class="flipnote">← 翻面！找出是什麼證據</span>':'')+
          (x.p?' · <a href="'+x.p+'">筆記</a>':'')+
          (x.one?'<div class="ctx" style="margin:4px 0 0">'+e_(x.one)+'</div>':'')+'</div>';
        prev=x;});
      document.getElementById('tlout').innerHTML=h2+'</div>'+
        '<p class="cnt">自問：每次翻面，是新事實（財報/產業變化）還是新框架（同一組事實換個看法）？前者是更新，後者要小心是敘事漂移。</p>';
    }
    document.getElementById('ct').addEventListener('change',e=>tl(e.target.value.toUpperCase()));
    document.getElementById('rndt').addEventListener('click',e=>{e.preventDefault();
      const multi=Object.entries(byEnt).filter(([k,l])=>l.length>=3).map(([k])=>k);
      const tk=pick(multi.length?multi:Object.keys(byEnt));
      document.getElementById('ct').value=tk;tl(tk)});
  }
}

/* ═══ ⏪ 時光機 ═══ */
let rq=null;
function gh(){try{return JSON.parse(localStorage.getItem('gym_hist')||'{}')}catch(e){return{}}}
function saveGh(h){localStorage.setItem('gym_hist',JSON.stringify(h))}
function replayPool(){
  const cutoff=new Date(Date.now()-60*864e5).toISOString().slice(0,10);
  return DD.filter(x=>x.d&&x.d<cutoff&&ST[x.k]);
}
function newReplay(){
  const pool=replayPool();
  if(!pool.length){document.getElementById('m-replay').innerHTML='<p class="cnt">題庫不足（需 >60 天前的 DD＋結算）。</p>';return}
  rq=pick(pool);
  document.getElementById('m-replay').innerHTML=
    '<p class="ctx">撲克手牌復盤：回到 <b>'+e_(rq.d)+'</b>，只用當時的資訊做決定。先開 DD 讀（那是當時的牌面），**忽略報告自己的裁決**，寫你的。</p>'+
    '<div class="filecard"><div class="tk" style="font-family:var(--mono);font-size:1.4rem;font-weight:800">'+
    e_(rq.k)+' <span class="cnt">@ '+e_(rq.d)+'</span></div>'+
    '<div class="ctx">'+e_(rq.title)+'</div>'+
    '<div class="btnrow">'+(rq.p?'<a class="btn" href="'+rq.p+'">讀當時的 DD</a>':'')+'</div>'+
    '<div class="btnrow"><b>我的裁決：</b><select id="rv"><option></option><option>進場</option><option>觀望</option><option>迴避</option></select></div>'+
    '<textarea id="rwhy" placeholder="理由 ≥50 字：關鍵變數是什麼？我最怕什麼？"></textarea><div class="wc" id="rwc"></div>'+
    '<div class="btnrow"><a class="btn" href="#" id="rrvl">揭曉之後發生的事</a>'+
    '<a class="btn sec" href="#" id="rskip">換一題</a></div><div id="rout"></div></div>';
  const ta=document.getElementById('rwhy'),wc=document.getElementById('rwc');
  ta.addEventListener('input',()=>wc.textContent=ta.value.length+' 字');
  document.getElementById('rskip').addEventListener('click',e=>{e.preventDefault();newReplay()});
  document.getElementById('rrvl').addEventListener('click',e=>{
    e.preventDefault();
    if(ta.value.trim().length<50){ta.style.borderColor='var(--avoid)';return}
    revealReplay(document.getElementById('rv').value,ta.value);});
}
function revealReplay(myv,why){
  const rows=(ST[rq.k]||[]).filter(r=>r[0]>=rq.d);
  const after=byEnt[rq.k].filter(x=>x.d>rq.d);
  let h='<h2 style="margin-top:1em">之後發生的事</h2>';
  const exact=(ST[rq.k]||[]).find(r=>r[0]===rq.d);
  if(exact)h+='<p>該筆裁決至今：<b style="color:'+(exact[2]>=0?'var(--go-t)':'var(--avoid-t)')+'">'+
    (exact[2]>=0?'+':'')+exact[2]+'%</b>（'+exact[3]+' 天）· 當時系統裁決 '+vb(rq.v)+' vs 你 '+vb(myv||'—')+'</p>';
  if(after.length)h+='<p class="cnt">後續 DD：</p>'+after.map(x=>
    '<div class="card"><b style="font-family:var(--mono)">'+e_(x.d)+'</b> '+vb(x.v)+
    (x.p?' · <a href="'+x.p+'">筆記</a>':'')+
    (x.one?'<div class="o">'+e_(x.one)+'</div>':'')+'</div>').join('');
  h+='<p class="cnt"><b>過程 × 結果 2×2 自評</b>——結果好不代表決策對：</p>'+
    '<div class="q2x2">'+
    ['好決策·好結果','好決策·壞結果','壞決策·好結果','壞決策·壞結果'].map(q=>
    '<a href="#" data-q="'+q+'">'+q+'</a>').join('')+'</div><div id="rq2"></div>';
  document.getElementById('rout').innerHTML=h;
  document.querySelectorAll('#rout [data-q]').forEach(b=>b.addEventListener('click',e=>{
    e.preventDefault();
    const h2=gh();h2.replay=h2.replay||{};h2.replay[b.dataset.q]=(h2.replay[b.dataset.q]||0)+1;saveGh(h2);
    document.getElementById('rq2').innerHTML=
      '<p class="cnt">已記錄：'+e_(b.dataset.q)+' · 累計 '+
      Object.entries(h2.replay).map(([k,v])=>k+' '+v).join(' / ')+'</p>'+
      '<div class="btnrow"><a class="btn sec" href="#" id="rexp">⬇ 匯出復盤 .md</a>'+
      '<a class="btn" href="#" id="rnext">下一題 →</a></div>';
    document.getElementById('rexp').addEventListener('click',ev=>{ev.preventDefault();
      exportMd('REPLAY_'+rq.k.replace(/[^A-Za-z0-9.]/g,'_')+'_'+today().replace(/-/g,'')+'.md',
        fmnote('時光機復盤',rq.k,['## 回到 '+rq.d,'','我的裁決：'+(myv||'—')+'（當時系統：'+(rq.v||'—')+'）','','理由：','',why,'','自評：'+b.dataset.q]))});
    document.getElementById('rnext').addEventListener('click',ev=>{ev.preventDefault();newReplay()});
  }));
}

/* ═══ 🎯 異常狩獵（v2：五鏡頭＋認領快照＋收斂對帳＋記分板） ═══ */
function pctRank(arr,v){const s=arr.filter(x=>x!=null).sort((a,b)=>a-b);
  return s.length?Math.round(100*s.filter(x=>x<=v).length/s.length):null}
function median(a){const s=a.slice().sort((x,y)=>x-y);const m=Math.floor(s.length/2);
  return s.length%2?s[m]:(s[m-1]+s[m])/2}
function hash(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}

/* 五種背離鏡頭；每個異常帶 snap（認領時凍結，回訪對帳用） */
function buildAnomalies(){
  const pool=Object.values(latest).filter(x=>x.moat!=null&&x.fpe!=null&&x.fpe>0);
  const moats=pool.map(x=>x.moat),fpes=pool.map(x=>x.fpe);
  const out=[];
  /* ① 品質×倍數背離 */
  pool.forEach(x=>{
    const mp=pctRank(moats,x.moat),fp=pctRank(fpes,x.fpe),gap=fp-mp;
    if(Math.abs(gap)>=35)out.push({key:'pq_'+x.k,tk:x.k,kind:'品質×倍數',score:Math.abs(gap),
      desc:'護城河 '+x.moat+'（P'+mp+'）vs '+x.fpe+'x（P'+fp+'）→ '+
        (gap>0?'市場給的倍數遠高於品質排名 🔺':'高品質但市場只給低倍數 🔻'),
      snap:{gap,fpe:x.fpe,moat:x.moat}});});
  /* ② 裁決×結算背離 */
  Object.entries(ST).forEach(([k,rows])=>{
    const ent=ENTMAP[k];if(!ent||!rows.length)return;
    const last=rows[rows.length-1],pct=last[2];
    if(ent.v==='進場'&&pct<-15)out.push({key:'vs_'+k,tk:k,kind:'裁決×結算',score:Math.abs(pct),
      desc:'裁決進場但結算 '+pct+'% → thesis 受傷還是市場錯殺？',snap:{pct}});
    if((ent.v==='觀望'||ent.v==='迴避')&&pct>30)out.push({key:'vs_'+k,tk:k,kind:'裁決×結算',
      score:pct,desc:'裁決'+ent.v+'但結算 +'+pct+'% → 錯過還是泡沫？',snap:{pct}});});
  /* ③ 同主題離群 */
  const themeMembers={};
  Object.keys(latest).forEach(k=>(ETH[k]||[]).forEach(t=>{
    (themeMembers[t.name]=themeMembers[t.name]||[]).push(latest[k])}));
  Object.entries(themeMembers).forEach(([tm,ms])=>{
    const withMoat=ms.filter(m=>m.moat!=null);
    if(withMoat.length<3)return;
    const med=median(withMoat.map(m=>m.moat));
    withMoat.forEach(m=>{
      const dev=m.moat-med;
      if(Math.abs(dev)>=2.5)out.push({key:'th_'+m.k+'_'+hash(tm)%1e4,tk:m.k,kind:'主題離群',
        score:Math.abs(dev)*10,
        desc:'在「'+tm+'」中護城河 '+m.moat+' vs 同儕中位 '+med+'（'+(dev>0?'+':'')+dev.toFixed(1)+
          '）→ 真的比同行'+(dev>0?'強':'弱')+'這麼多？',snap:{dev:+dev.toFixed(1),med}});});});
  /* ④ 跨版本評分漂移 */
  Object.entries(byEnt).forEach(([k,l])=>{
    for(let i=1;i<l.length;i++){
      const a=l[i-1],b=l[i];
      if(a.moat!=null&&b.moat!=null&&Math.abs(b.moat-a.moat)>=2)
        out.push({key:'dr_'+k+'_'+(b.d||i),tk:k,kind:'評分漂移',score:Math.abs(b.moat-a.moat)*8,
          desc:a.d+' 護城河 '+a.moat+' → '+b.d+' 變 '+b.moat+' → 是新事實還是評分者換了心情？',
          snap:{from:a.moat,to:b.moat}});}});
  /* ⑤ 評分內部張力 */
  pool.forEach(x=>{
    if(x.pp!=null&&Math.abs(x.moat-x.pp)>=3)
      out.push({key:'tn_'+x.k,tk:x.k,kind:'內部張力',score:Math.abs(x.moat-x.pp)*7,
        desc:'護城河總分 '+x.moat+' 但定價權只有 '+x.pp+' → 沒有定價權的護城河是什麼做的？',
        snap:{moat:x.moat,pp:x.pp}});});
  /* 去重（同 ticker 多鏡頭保留，同 key 去重）＋排序 */
  const seen=new Set();
  return out.filter(a=>!seen.has(a.key)&&seen.add(a.key)).sort((a,b)=>b.score-a.score);
}

function huntClaims(){try{return JSON.parse(localStorage.getItem('gym_hunt2')||'{}')}catch(e){return{}}}
function saveHuntClaims(c){localStorage.setItem('gym_hunt2',JSON.stringify(c))}

/* 回訪對帳：認領時 snap vs 現在的同指標 → 收斂 / 擴大 */
function drift(a,claim){
  const s=claim.snap||{};
  if(a==null)return '（此異常已從榜上消失——很可能已收斂）';
  const n=a.snap;
  if(s.gap!=null&&n.gap!=null)return 'P 差 '+s.gap+' → '+n.gap+(Math.abs(n.gap)<Math.abs(s.gap)?'（收斂中）':'（還在擴大）');
  if(s.pct!=null&&n.pct!=null)return '結算 '+s.pct+'% → '+n.pct+'%';
  if(s.dev!=null&&n.dev!=null)return '離群 '+s.dev+' → '+n.dev;
  if(s.pp!=null&&n.pp!=null)return '張力 '+(s.moat-s.pp)+' → '+(n.moat-n.pp);
  return '';
}

function renderHunt(){
  const anomalies=buildAnomalies();
  const byKey={};anomalies.forEach(a=>byKey[a.key]=a);
  const claims=huntClaims();
  const kinds=['品質×倍數','裁決×結算','主題離群','評分漂移','內部張力'];
  const kindOn=window._huntKind||'*';

  /* 今日獵物：日期種子確定性選一隻未認領的 */
  const openA=anomalies.filter(a=>!claims[a.key]);
  const daily=openA.length?openA[hash(today())%openA.length]:null;

  /* 記分板 */
  const cl=Object.values(claims);
  const resolved=cl.filter(c=>c.judge);
  const right=resolved.filter(c=>c.judge==='right').length;

  let h='<p class="ctx">敏銳度的高階形式是「會自己生問題」。五種鏡頭掃出的背離——認領、寫解釋、'+
    '<b>之後回來對帳</b>：背離收斂了嗎？你的解釋對了嗎？獵人跟評論家的差別就在有沒有對帳。</p>';
  h+='<div class="tiles" style="margin:10px 0">'+
    '<div class="tile"><div class="n">'+anomalies.length+'</div><div class="l">在榜異常</div></div>'+
    '<div class="tile"><div class="n">'+cl.length+'</div><div class="l">已認領</div></div>'+
    '<div class="tile"><div class="n">'+right+'/'+resolved.length+'</div><div class="l">對帳命中</div></div></div>';

  if(daily){
    h+='<div class="filecard" style="border-color:rgba(74,222,128,.4)"><b>🏹 今日獵物</b>'+
      '<div style="margin:6px 0"><a href="'+(ENTMAP[daily.tk]?ENTMAP[daily.tk].p:'#')+
      '" style="font-family:var(--mono);font-weight:700">'+e_(daily.tk)+'</a> '+
      '<span class="badge">'+e_(daily.kind)+'</span></div>'+
      '<div class="ctx">'+e_(daily.desc)+'</div>'+
      '<div class="btnrow"><a class="btn" href="#" class="claim" id="dailyclaim" data-k="'+daily.key+'">認領這隻</a></div></div>';
  }

  /* 獵場日誌 */
  if(cl.length){
    h+='<h2>📓 獵場日誌（回訪對帳）</h2>';
    Object.entries(claims).sort((a,b)=>(b[1].date||'').localeCompare(a[1].date||'')).forEach(([key,c])=>{
      const cur=byKey[key];
      h+='<div class="card"><div class="t"><a href="'+(ENTMAP[c.tk]?ENTMAP[c.tk].p:'#')+'">'+e_(c.tk)+'</a> '+
        '<span class="badge">'+e_(c.kind||'')+'</span> <span class="cnt">'+e_(c.date)+' 認領</span>'+
        (c.judge?' <b class="'+(c.judge==='right'?'v-go':c.judge==='wrong'?'v-avoid':'v-hold')+'">'+
          (c.judge==='right'?'✓ 我對了':c.judge==='wrong'?'✗ 我錯了':'…觀察中')+'</b>':'')+'</div>'+
        '<div class="o">'+e_(c.t)+'</div>'+
        '<div class="m">'+e_(drift(cur,c))+'</div>'+
        (!c.judge?'<div class="btnrow" style="margin:6px 0 0">'+
          '<a href="#" class="claim" data-j="right" data-k="'+key+'">判定：我對了</a> · '+
          '<a href="#" class="claim" data-j="wrong" data-k="'+key+'">我錯了</a> · '+
          '<a href="#" class="claim" data-j="open" data-k="'+key+'">再觀察</a></div>':'')+
        '</div>';});
  }

  /* 異常榜（鏡頭過濾） */
  h+='<h2>背離榜</h2><div class="subtabs"><span class="'+(kindOn==='*'?'on':'')+'" data-kd="*">全部</span>'+
    kinds.map(k=>'<span class="'+(kindOn===k?'on':'')+'" data-kd="'+k+'">'+k+'</span>').join('')+'</div>';
  const rows=anomalies.filter(a=>kindOn==='*'||a.kind===kindOn).slice(0,30);
  h+='<table class="hunt"><tr><th>異常</th><th></th></tr>'+rows.map(a=>{
    const claimed=claims[a.key];
    return '<tr><td><a href="'+(ENTMAP[a.tk]?ENTMAP[a.tk].p:'#')+'">'+e_(a.tk)+'</a> '+
      '<span class="badge">'+e_(a.kind)+'</span> '+e_(a.desc)+'</td><td>'+
      (claimed?'<span class="cnt">已認領</span>':'<span class="claim" data-k="'+a.key+'">認領</span>')+'</td></tr>';
  }).join('')+'</table>';
  h+='<div id="claimarea"></div><div class="btnrow"><a class="btn sec" href="#" id="hexp">⬇ 匯出獵場日誌 .md</a></div>';

  document.getElementById('m-hunt').innerHTML=h;

  document.querySelectorAll('#m-hunt .subtabs span').forEach(s=>s.addEventListener('click',()=>{
    window._huntKind=s.dataset.kd;renderHunt()}));

  document.querySelectorAll('#m-hunt .claim, #dailyclaim').forEach(c=>c.addEventListener('click',ev=>{
    ev.preventDefault();
    const key=c.dataset.k;
    if(c.dataset.j){ /* 對帳判定 */
      const cs=huntClaims();
      if(c.dataset.j!=='open')cs[key].judge=c.dataset.j;
      saveHuntClaims(cs);renderHunt();return;
    }
    const a=byKey[key];if(!a)return;
    document.getElementById('claimarea').innerHTML=
      '<div class="claimbox"><h2>認領：'+e_(a.tk)+'（'+e_(a.kind)+'）</h2>'+
      '<p class="ctx">'+e_(a.desc)+'</p>'+
      '<p class="ctx">三種解法：①市場錯（背離會收斂）②評分錯（DD 該重跑）③<b>第三變數</b>——'+
      '評分表沒有格子、但市場有在 price in 的東西。常見第三變數：'+
      '<span class="chip">治理／關鍵人（一人決策）</span><span class="chip">股權結構（雙層股權）</span>'+
      '<span class="chip">資本配置紀律（亂投資）</span><span class="chip">監管懸而未決</span>'+
      '<span class="chip">週期位置（高點利潤）</span><span class="chip">會計品質</span>'+
      '<span class="chip">地緣／制裁</span><span class="chip">客戶集中</span></p>'+
      '<textarea id="cta" placeholder="≥40 字，寫成可證偽的判斷。範例：META 護城河 9 但倍數被壓——不是市場錯，是市場在 price in 執行長一人決策的治理折價；若 metaverse 資本開支紀律連兩季改善而倍數不修復，則我錯。"></textarea>'+
      '<div class="btnrow"><a class="btn" href="#" id="csave">存進獵場日誌</a></div></div>';
    document.getElementById('claimarea').scrollIntoView({behavior:'smooth'});
    document.getElementById('csave').addEventListener('click',e2=>{
      e2.preventDefault();
      const t=document.getElementById('cta').value.trim();
      if(t.length<40){document.getElementById('cta').style.borderColor='var(--avoid)';return}
      const cs=huntClaims();
      cs[key]={tk:a.tk,kind:a.kind,t,date:today(),snap:a.snap};
      saveHuntClaims(cs);renderHunt();});
  }));

  document.getElementById('hexp').addEventListener('click',e=>{
    e.preventDefault();
    const cs=huntClaims();
    const lines=['---','type: usernote','title: "獵場日誌 · '+today()+'"','date: '+today(),
      'tags: [gym, hunt]','---','','# 獵場日誌 · '+today(),''];
    Object.entries(cs).forEach(([k,c])=>{
      const cur=byKey[k];
      lines.push('## [['+c.tk+']]（'+(c.kind||'')+'，'+c.date+' 認領'+
        (c.judge?'，判定：'+(c.judge==='right'?'我對了':'我錯了'):'')+'）','',c.t,'',
        '對帳：'+drift(cur,c),'')});
    exportMd('HUNT_'+today().replace(/-/g,'')+'.md',lines)});
}

/* ═══ ✍️ 寫作間 ═══ */
let wMode='feyn',wq=null;
function renderWrite(){
  const el=document.getElementById('m-write');
  let h='<div class="subtabs"><span class="'+(wMode==='feyn'?'on':'')+'" data-s="feyn">費曼三句</span>'+
    '<span class="'+(wMode==='red'?'on':'')+'" data-s="red">紅隊做空報告</span></div>';
  if(wMode==='feyn'){
    if(!wq||!wq.feyn)wq={feyn:pick(Object.values(latest))};
    const x=wq.feyn;
    h+='<p class="ctx">費曼法：不能解釋給外行聽＝你其實不懂。三句話，每句 ≥15 字，禁術語。</p>'+
      '<div class="filecard"><div class="tk" style="font-family:var(--mono);font-size:1.4rem;font-weight:800">'+e_(x.k)+'</div>'+
      '<div class="ctx">'+e_(x.title)+'</div>'+
      '<p class="cnt">① 這門生意怎麼賺錢？</p><textarea id="f1" style="min-height:52px"></textarea>'+
      '<p class="cnt">② 為什麼別人搶不走？</p><textarea id="f2" style="min-height:52px"></textarea>'+
      '<p class="cnt">③ 什麼會殺死它？</p><textarea id="f3" style="min-height:52px"></textarea>'+
      '<div class="btnrow"><a class="btn" href="#" id="frvl">寫完了，對照庫內</a>'+
      '<a class="btn sec" href="#" id="fskip">換一檔</a></div><div id="fout"></div></div>';
  }else{
    const pool=Object.values(latest).filter(x=>x.v==='進場'&&PM[x.k]);
    if(!wq||!wq.red)wq={red:pool.length?pick(pool):null};
    const x=wq.red;
    if(!x){h+='<p class="cnt">沒有「進場＋pre-mortem」的題庫。</p>';}
    else h+='<p class="ctx">紅隊：這檔的現行裁決是<b class="v-go">進場</b>。你是做空基金分析師，寫一段 ≥120 字的做空 pitch——寫到多頭會不舒服的程度。</p>'+
      '<div class="filecard"><div class="tk" style="font-family:var(--mono);font-size:1.4rem;font-weight:800">'+e_(x.k)+'</div>'+
      '<div class="ctx">'+e_(x.title)+'</div>'+
      (x.one?'<div class="rvlone">多頭論點：'+e_(x.one)+'</div>':'')+
      '<textarea id="rd" style="min-height:120px" placeholder="做空 pitch：結構性問題／估值鏡頭／催化劑與時點…"></textarea><div class="wc" id="rdwc"></div>'+
      '<div class="btnrow"><a class="btn" href="#" id="rdrvl">對照 pre-mortem 與 critic</a>'+
      '<a class="btn sec" href="#" id="rdskip">換一檔</a></div><div id="rdout"></div></div>';
  }
  el.innerHTML=h;
  el.querySelectorAll('.subtabs span').forEach(s=>s.addEventListener('click',()=>{
    wMode=s.dataset.s;wq=null;renderWrite()}));
  if(wMode==='feyn'){
    document.getElementById('fskip').addEventListener('click',e=>{e.preventDefault();wq=null;renderWrite()});
    document.getElementById('frvl').addEventListener('click',e=>{
      e.preventDefault();
      const v=[1,2,3].map(i=>document.getElementById('f'+i).value.trim());
      if(v.some(t=>t.length<15)){[1,2,3].forEach(i=>{const t=document.getElementById('f'+i);
        if(t.value.trim().length<15)t.style.borderColor='var(--avoid)'});return}
      const x=wq.feyn,ent=ENTMAP[x.k]||{};
      document.getElementById('fout').innerHTML=
        (x.one?'<div class="rvlone">DD 的一句話：'+e_(x.one)+'</div>':'')+
        '<p class="cnt">對照後自問：你的版本跟 DD 的版本，哪個更接近本質？差在哪個維度（客戶/成本/轉換/網路效應）？</p>'+
        '<div class="btnrow">'+(x.p?'<a class="btn sec" href="'+x.p+'">開 DD 筆記驗證</a>':'')+
        '<a class="btn sec" href="#" id="fexp">⬇ 匯出 .md</a>'+
        '<a class="btn" href="#" id="fnext">下一檔 →</a></div>';
      document.getElementById('fexp').addEventListener('click',ev=>{ev.preventDefault();
        exportMd('FEYNMAN_'+x.k.replace(/[^A-Za-z0-9.]/g,'_')+'_'+today().replace(/-/g,'')+'.md',
          fmnote('費曼三句',x.k,['## ① 怎麼賺錢','',v[0],'','## ② 為什麼搶不走','',v[1],'','## ③ 什麼殺死它','',v[2]]))});
      document.getElementById('fnext').addEventListener('click',ev=>{ev.preventDefault();wq=null;renderWrite()});
    });
  }else if(wq&&wq.red){
    const ta=document.getElementById('rd'),wc=document.getElementById('rdwc');
    ta.addEventListener('input',()=>wc.textContent=ta.value.length+' 字');
    document.getElementById('rdskip').addEventListener('click',e=>{e.preventDefault();wq=null;renderWrite()});
    document.getElementById('rdrvl').addEventListener('click',e=>{
      e.preventDefault();
      if(ta.value.trim().length<120){ta.style.borderColor='var(--avoid)';return}
      const x=wq.red;
      document.getElementById('rdout').innerHTML=
        '<p class="cnt">DD 的 pre-mortem：</p><div class="pmbox">'+e_(PM[x.k])+'</div>'+
        ((CRIT[x.k]||[]).length?'<p class="cnt">critic 冷讀：'+CRIT[x.k].map(p=>'<a href="'+p+'">報告</a>').join(' · ')+'</p>':'')+
        '<p class="cnt">自問：你的做空 pitch 有沒有超出 pre-mortem 的新死法？有＝你看到了系統沒看到的。</p>'+
        '<div class="btnrow"><a class="btn sec" href="#" id="rdexp">⬇ 匯出 .md</a>'+
        '<a class="btn" href="#" id="rdnext">下一檔 →</a></div>';
      document.getElementById('rdexp').addEventListener('click',ev=>{ev.preventDefault();
        exportMd('REDTEAM_'+x.k.replace(/[^A-Za-z0-9.]/g,'_')+'_'+today().replace(/-/g,'')+'.md',
          fmnote('紅隊做空',x.k,['## 做空 pitch','',ta.value]))});
      document.getElementById('rdnext').addEventListener('click',ev=>{ev.preventDefault();wq=null;renderWrite()});
    });
  }
}

renderCmp();newReplay();renderHunt();renderWrite();
</script></main></body></html>
"""


def build_gym(summaries, stems, graph):
    """思考訓練場：對照/時光機/異常狩獵/寫作（非問答式四模式）。"""
    def num(x, key):
        try:
            return round(float(x.get(key)), 2)
        except (TypeError, ValueError):
            return None

    alldd = []
    for s in summaries:
        if s["type"] != "dd" or not s.get("entity"):
            continue
        p = stems.get(Path(s["note"]).stem)
        if not p:
            continue
        x = s.get("extra") or {}
        alldd.append({"k": s["entity"], "d": s.get("date"), "v": s.get("verdict"),
                      "g": s.get("grade"), "one": (s.get("oneliner") or "")[:220],
                      "title": (s.get("title") or "")[:110], "p": p,
                      "moat": num(x, "moat_score"), "pp": num(x, "moat_pricing_power"),
                      "gd": num(x, "growth_durability"), "qs": num(x, "quality_score"),
                      "fpe": num(x, "fpe_fy2"), "pct5": num(x, "pct_5y")})

    ents, ent_themes = [], {}
    theme_page = {}
    for n in graph.get("nodes", []):
        if n.get("type") == "company":
            page = stems.get(n["id"])
            if page:
                c = n.get("canonical") or {}
                ents.append({"k": n["id"], "v": c.get("verdict") or "",
                             "g": c.get("fundamental_grade") or "", "p": page})
        elif n.get("type") in ("industry", "supplychain"):
            theme_page[n["id"]] = stems.get(f"Theme_{_safe_name(n['id'])}")
    for e in graph.get("edges", []):
        tp = theme_page.get(e["to"])
        if tp:
            lst = ent_themes.setdefault(e["from"], [])
            if not any(t["name"] == e["to"] for t in lst):
                lst.append({"name": e["to"], "p": tp})

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

    latest_by = {}
    for d in sorted(alldd, key=lambda d: d.get("d") or ""):
        latest_by[d["k"]] = d
    pm = _premortems({k: [{"t": "dd", "p": d["p"]}] for k, d in latest_by.items()})

    crit = {}
    crit_re = re.compile(r"_?critic(?:_v[\d_]+)?_([A-Z][A-Z0-9.]{0,7})_\d{8}")
    for s in summaries:
        if s["type"] != "internal-note":
            continue
        stem = Path(s["note"]).stem
        m = crit_re.search(stem)
        if not m:
            continue
        p = stems.get(stem)
        if p:
            crit.setdefault(m.group(1), []).append(p)

    def payload(o):
        return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

    (WIKI / "gym.html").write_text(
        GYM.replace("%%ALLDD%%", payload(alldd)).replace("%%ENTS%%", payload(ents))
           .replace("%%ETH%%", payload(ent_themes)).replace("%%SETTLE%%", payload(settle))
           .replace("%%PM%%", payload(pm)).replace("%%CRIT%%", payload(crit)),
        encoding="utf-8")


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
        if rel in ("index.html", "munger.html", "dojo.html", "gym.html"):
            continue
        if rel[:-5] + ".md" not in md_files:
            hp.unlink()
            n_pruned += 1

    graph = json.loads(GRAPH.read_text(encoding="utf-8")) if GRAPH.exists() else {}
    build_index(summaries, stems)
    build_munger(summaries, stems, graph)
    build_dojo(summaries, stems, graph)
    build_gym(summaries, stems, graph)
    print(f"📖 wiki: {n_render} rendered, {n_skip} cached, {n_pruned} pruned "
          f"→ open {WIKI / 'index.html'}")


if __name__ == "__main__":
    main()
