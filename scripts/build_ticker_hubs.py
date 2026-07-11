#!/usr/bin/env python3
"""Build TICKER HUB pages — per-ticker aggregation of all on-site research.

Professionals think in tickers, but the site is organized by report type. A
single ticker's coverage is scattered across docs/dd, docs/id, docs/supply-chain,
docs/comparisons, docs/research/synthesis. This script emits:

  docs/t/{TICKER}.html   one aggregation page per ticker (universe = every
                         ticker with >=1 parseable DD report)
  docs/t/index.html      directory index with count stats + filterable grid

Read-only aggregation. Deterministic (sorted iteration everywhere) so re-runs
are zero-churn when nothing changed. Full regenerate of docs/t/ every run.

Chrome (token block / nav / footer) is the site canonical: nav comes from the
authoritative generator scripts/site_nav.py (byte-exact, so a later nav
re-injection is a no-op); token block + footer copied from the current canonical
docs/mental-models/index.html.
"""
from __future__ import annotations

import html
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "t"

sys.path.insert(0, str(ROOT / "scripts"))
from site_nav import full_nav_block  # noqa: E402  (authoritative canonical nav)

# ── canonical chrome fragments (token block + footer) copied verbatim from
#    docs/mental-models/index.html (current canonical, 設計系統 v1.1) ──────────
TOKEN_BLOCK = """:root {
  --imq-bg:           var(--paper);
  --imq-bg-soft:      var(--paper);
  --imq-card:         var(--card);
  --imq-border:       var(--line);
  --imq-border-soft:  var(--line-soft);
  --imq-text:         var(--ink);
  --imq-text-sec:     var(--sec);
  --imq-text-muted:   var(--muted);
  --imq-accent:       var(--accent);
  --imq-accent-hover: var(--accent-ink);
  --imq-indigo-deep:  #534AB7;
  --imq-green:        #0F6E56;
  --imq-brand:        #1a56db;
  --imq-amber:        #B45309;
  --imq-rose:         #C0392B;
  --imq-shadow-sm:    var(--sh-1);
  --imq-shadow-md:    var(--sh-2);
  --imq-shadow-lg:    var(--sh-2);
  --imq-r-sm:   var(--r);
  --imq-r-md:   var(--r);
  --imq-r-lg:   var(--r);
  --imq-r-xl:   var(--r);
  --imq-r-2xl:  var(--r);
  --imq-r-pill: 999px;
  --imq-font-sans: var(--sans);
  --imq-font-mono: var(--mono);
}"""

FOOTER = """<footer class="imq-foot">
  <div>&copy; 2026 InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>"""

FOOTNOTE = "頁面由站內研究自動聚合，裁決以個別報告為準。"

# page-specific CSS (lean; complements /assets/imq-base.css + token block)
PAGE_CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--imq-font-sans);background:var(--paper);color:var(--body);line-height:1.7;font-size:14px;min-height:100vh;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none;transition:color .15s}
a:hover{color:var(--accent-ink)}
.serif{font-family:'Noto Serif TC',Georgia,'Times New Roman',serif}
.mono{font-family:var(--imq-font-mono)}
.wrap{max-width:960px;margin:0 auto;padding:40px 28px 64px}
.overline{font-family:var(--imq-font-mono);font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:12px}
h1.tk{font-family:'Noto Serif TC',Georgia,serif;font-weight:700;letter-spacing:-.01em;color:var(--ink);font-size:34px;line-height:1.15;margin-bottom:8px}
.oneliner{color:var(--sec);font-size:14px;line-height:1.7;margin:10px 0 18px;max-width:760px}
.verdict-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:20px}
.chip{display:inline-flex;align-items:center;gap:.35em;font-size:12px;font-weight:600;padding:.3rem .7rem;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);white-space:nowrap}
.chip.v-in{background:rgba(15,110,86,.10);border-color:rgba(15,110,86,.35);color:var(--imq-green)}
.chip.v-out{background:rgba(192,57,43,.08);border-color:rgba(192,57,43,.32);color:var(--imq-rose)}
.chip.v-hold{background:rgba(180,83,9,.08);border-color:rgba(180,83,9,.30);color:var(--imq-amber)}
.chip.muted{color:var(--muted)}
.snap{display:flex;flex-wrap:wrap;gap:0;border:1px solid var(--line);border-radius:var(--r);background:var(--card);overflow:hidden;margin-bottom:8px}
.snap .cell{flex:1 1 auto;min-width:96px;padding:10px 14px;border-right:1px solid var(--line-soft)}
.snap .cell:last-child{border-right:0}
.snap .lbl{font-family:var(--imq-font-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:3px}
.snap .val{font-size:14px;font-weight:600;color:var(--ink)}
.asof{font-size:11px;color:var(--muted);margin-bottom:30px}
section.blk{margin-top:30px}
section.blk > h2{font-family:'Noto Serif TC',Georgia,serif;font-size:18px;font-weight:700;color:var(--ink);border-bottom:2px solid var(--line);padding-bottom:7px;margin-bottom:4px}
section.blk > .cnt{font-family:var(--imq-font-mono);font-size:11px;color:var(--muted);margin-bottom:12px}
ul.items{list-style:none;display:flex;flex-direction:column;gap:2px}
ul.items li{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;padding:8px 4px;border-bottom:1px solid var(--line-soft)}
ul.items li:last-child{border-bottom:0}
.dt{font-family:var(--imq-font-mono);font-size:12px;color:var(--sec);flex-shrink:0;min-width:82px}
.it-main{flex:1 1 260px}
.it-main a{font-weight:600}
.it-sub{color:var(--sec);font-size:12.5px}
.tag{font-family:var(--imq-font-mono);font-size:10.5px;padding:.12rem .45rem;border-radius:4px;background:var(--paper);border:1px solid var(--line);color:var(--sec);white-space:nowrap}
.foot-note{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);font-size:11.5px;color:var(--muted)}
/* directory */
.dir-stats{display:flex;flex-wrap:wrap;gap:14px;margin:18px 0 22px}
.stat{border:1px solid var(--line);border-radius:var(--r);background:var(--card);padding:12px 18px;min-width:120px}
.stat .n{font-family:'Noto Serif TC',Georgia,serif;font-size:26px;font-weight:700;color:var(--ink);line-height:1}
.stat .k{font-family:var(--imq-font-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-top:5px}
#flt{width:100%;max-width:360px;padding:10px 14px;font-size:14px;font-family:var(--imq-font-sans);border:1px solid var(--line);border-radius:var(--r);background:var(--card);color:var(--ink);margin-bottom:18px}
#flt:focus{outline:none;border-color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:10px}
a.tcard{display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);border-radius:var(--r);background:var(--card);padding:12px 14px;transition:border-color .15s,box-shadow .15s}
a.tcard:hover{border-color:var(--accent);box-shadow:var(--sh-1)}
a.tcard .tk{font-family:var(--imq-font-mono);font-size:15px;font-weight:700;color:var(--ink);letter-spacing:.01em}
a.tcard .meta{display:flex;align-items:center;justify-content:space-between;gap:8px}
a.tcard .rc{font-family:var(--imq-font-mono);font-size:10.5px;color:var(--muted)}
.nores{color:var(--muted);font-size:13px;padding:20px 4px;display:none}
@media(max-width:600px){.wrap{padding:28px 16px 48px}h1.tk{font-size:27px}}"""

VERDICT_CLASS = {"進場": "v-in", "迴避": "v-out", "觀望": "v-hold"}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def read_meta(path: Path, tag: str):
    try:
        h = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = re.search(rf'<script id="{tag}"[^>]*>(.*?)</script>', h, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


# ─────────────────────────────────────────────── gather sources ────────────
def gather_dd():
    """Return (universe_meta, dd_by_ticker, token_map, skipped).

    universe_meta[ticker] = newest dd-meta dict for that ticker.
    dd_by_ticker[ticker]  = list of {date, verdict, era, path} newest-first.
    """
    file_re = re.compile(r"^DD_(.+?)_(?:v\d+_)?(\d{8})(?:_.*)?\.html$")
    token_map = {}          # filename-token -> canonical ticker (from meta files)
    meta_files = []         # (canonical, date, path, meta)
    plain_files = []        # (token, date, path)  (no parseable meta)
    skipped = []
    for p in sorted((DOCS / "dd").glob("DD_*.html")):
        m = file_re.match(p.name)
        if not m:
            skipped.append(p.name)
            continue
        token, ymd = m.group(1), m.group(2)
        date = f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:]}"
        meta = read_meta(p, "dd-meta")
        if meta and meta.get("ticker"):
            canon = str(meta["ticker"]).strip()
            token_map.setdefault(token, canon)
            meta_files.append((canon, date, p.name, meta))
        else:
            plain_files.append((token, date, p.name))

    dd_by_ticker = defaultdict(list)
    for canon, date, name, meta in meta_files:
        if "dca_verdict" in meta:
            verdict, era = str(meta["dca_verdict"]), "裁決"
        else:
            verdict, era = str(meta.get("signal") or meta.get("verdict") or "—"), "訊號〔legacy〕"
        dd_by_ticker[canon].append({"date": date, "verdict": verdict, "era": era,
                                    "path": f"/dd/{name}", "meta": meta})
    # attach no-meta historical files whose token resolves to a known ticker
    for token, date, name in plain_files:
        canon = token_map.get(token)
        if not canon:
            skipped.append(name)
            continue
        dd_by_ticker[canon].append({"date": date, "verdict": "—", "era": "",
                                    "path": f"/dd/{name}", "meta": None})

    for canon in dd_by_ticker:
        dd_by_ticker[canon].sort(key=lambda r: r["date"], reverse=True)

    # newest meta per ticker = current verdict source
    universe_meta = {}
    for canon, rows in dd_by_ticker.items():
        newest_with_meta = next((r for r in rows if r["meta"]), None)
        if newest_with_meta:
            universe_meta[canon] = newest_with_meta
    return universe_meta, dd_by_ticker, token_map, skipped


def gather_ids():
    """ticker -> list of {theme, sd_verdict, clock_phase, date, path}."""
    out = defaultdict(list)
    for p in sorted((DOCS / "id").glob("ID_*.html")):
        meta = read_meta(p, "id-meta")
        if not meta:
            continue
        rel = meta.get("related_tickers") or []
        theme = meta.get("theme") or p.stem
        entry = {
            "theme": theme,
            "sd_verdict": meta.get("sd_verdict"),
            "clock_phase": meta.get("clock_phase"),
            "date": meta.get("publish_date") or "",
            "path": f"/id/{p.name}",
        }
        for rt in rel:
            if isinstance(rt, dict) and rt.get("ticker"):
                out[str(rt["ticker"]).strip()].append(entry)
    for t in out:
        out[t].sort(key=lambda r: (r["date"], r["theme"]), reverse=True)
    return out


def gather_supply_chain():
    """ticker -> list of {topic_title, topic_id, nodes[]}."""
    data_dir = DOCS / "supply-chain" / "data"
    try:
        topics = json.loads((data_dir / "topics.json").read_text())["topics"]
    except (OSError, KeyError, json.JSONDecodeError):
        return {}
    active = [t["id"] for t in topics if t.get("active")]
    out = defaultdict(dict)  # ticker -> {topic_id: {"title":..,"nodes":set}}
    for tid in sorted(active):
        f = data_dir / f"{tid}.json"
        if not (f.exists() and (DOCS / "supply-chain" / f"{tid}.html").exists()):
            continue
        try:
            d = json.loads(f.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        title = d.get("title") or tid
        for node in d.get("nodes", []):
            nname = node.get("name") or node.get("id") or ""
            for co in node.get("companies", []):
                tk = (co.get("ticker") or "").strip()
                if not tk:
                    continue
                slot = out[tk].setdefault(tid, {"title": title, "nodes": []})
                if nname and nname not in slot["nodes"]:
                    slot["nodes"].append(nname)
    # flatten to sorted lists
    flat = {}
    for tk, topicmap in out.items():
        flat[tk] = [
            {"topic_id": tid, "title": topicmap[tid]["title"],
             "nodes": topicmap[tid]["nodes"]}
            for tid in sorted(topicmap)
        ]
    return flat


def gather_comparisons(universe):
    """ticker -> list of {tickers[], date, path}. Parse from filenames."""
    # build compact map (dotless) from universe so 2330TW -> 2330.TW resolves
    compact = {}
    for t in universe:
        compact.setdefault(t.replace(".", ""), t)
        compact.setdefault(t, t)
    out = defaultdict(list)
    file_re = re.compile(r"^MS_(.+)_(\d{8})\.html$")
    for p in sorted((DOCS / "comparisons").glob("MS_*.html")):
        m = file_re.match(p.name)
        if not m:
            continue
        core, ymd = m.group(1), m.group(2)
        date = f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:]}"
        raw = core.split("vs") if "vs" in core else core.split("_")
        resolved = []
        for tok in raw:
            tok = tok.strip()
            resolved.append(compact.get(tok, compact.get(tok.replace(".", ""), tok)))
        entry = {"tickers": resolved, "date": date, "path": f"/comparisons/{p.name}"}
        for tk in resolved:
            if tk in universe:
                out[tk].append(entry)
    for t in out:
        out[t].sort(key=lambda r: r["date"], reverse=True)
    return out


def gather_synthesis():
    """ticker -> list of {date, path}."""
    out = defaultdict(list)
    file_re = re.compile(r"^(.+)_(\d{8})\.html$")
    d = DOCS / "research" / "synthesis"
    for p in sorted(d.glob("*.html")):
        if p.name == "index.html":
            continue
        m = file_re.match(p.name)
        if not m:
            continue
        tk, ymd = m.group(1).strip(), m.group(2)
        date = f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:]}"
        out[tk].append({"date": date, "path": f"/research/synthesis/{p.name}"})
    for t in out:
        out[t].sort(key=lambda r: r["date"], reverse=True)
    return out


def load_screener():
    """ticker -> stock dict, plus as_of string."""
    f = DOCS / "dd-screener" / "latest.json"
    try:
        d = json.loads(f.read_text())
    except (OSError, json.JSONDecodeError):
        return {}, None
    by = {}
    for s in d.get("stocks", []):
        if s.get("ticker"):
            by[str(s["ticker"]).strip()] = s
    return by, d.get("as_of")


# ───────────────────────────────────────────────── render ──────────────────
def page_head(title, desc, active_group="research"):
    nav = full_nav_block(group=active_group)
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/imq-base.css">
  <style>
{TOKEN_BLOCK}
{PAGE_CSS}
  </style>
</head>
<body>
{nav}
"""


def verdict_chip(verdict, era):
    cls = VERDICT_CLASS.get(verdict, "muted")
    label = f"{verdict}" if not era else f"{era}｜{verdict}"
    return f'<span class="chip {cls}">{esc(label)}</span>'


def render_snapshot(stock, as_of):
    if not stock:
        return ""
    def g(k):
        v = stock.get(k)
        return v if v not in (None, "") else "—"
    def pct(k):
        v = stock.get(k)
        return f"{v}%" if isinstance(v, (int, float)) else "—"
    cells = [
        ("訊號", g("signal")),
        ("估值", g("val")),
        ("護城河", g("moat_grade")),
        ("FY+2 fPE", g("fpe_fy2")),
        ("5Y PE 分位", pct("pct_5y")),
        ("PEG", g("peg")),
        ("中期 upside", pct("upside_mid_pct")),
    ]
    inner = "".join(
        f'<div class="cell"><div class="lbl">{esc(l)}</div>'
        f'<div class="val">{esc(v)}</div></div>'
        for l, v in cells
    )
    asof = f'<div class="asof">Screener 快照 as-of {esc(as_of)}（估值欄隨週更管線刷新）。</div>' if as_of else ""
    return f'<div class="snap">{inner}</div>\n{asof}'


_CJK_HALF_PUNCT = re.compile(r'([一-鿿])([,:;!?.])')
_PUNCT_MAP = {",": "，", ":": "：", ";": "；", "!": "！", "?": "？", ".": "。"}


def normalize_punct(text):
    """中文字後的半形標點轉全形（QC gate 鐵律）——來源 dd-meta oneliner
    是 legacy 自由文字，標點不保證乾淨，顯示前正規化。"""
    return _CJK_HALF_PUNCT.sub(lambda m: m.group(1) + _PUNCT_MAP[m.group(2)], text)


def render_ticker_page(ticker, dd_rows, cur, ids, sc, comps, syns, stock, as_of):
    oneliner = ""
    if cur and cur["meta"]:
        oneliner = normalize_punct(cur["meta"].get("oneliner") or "")
    head = page_head(
        f"{ticker} 個股研究總覽 — InvestMQuest Research",
        f"{ticker} 在 InvestMQuest 站內的全部研究聚合：個股 DD、所屬產業 ID、供應鏈位置、對比與期望落差綜合研判。",
    )
    parts = [head, '<main class="wrap">']
    parts.append('<div class="overline">Ticker Hub · 個股研究總覽</div>')
    parts.append(f'<h1 class="tk mono">{esc(ticker)}</h1>')
    if oneliner:
        parts.append(f'<p class="oneliner">{esc(oneliner)}</p>')
    # verdict row
    vr = []
    if cur:
        vr.append(verdict_chip(cur["verdict"], cur["era"]))
        vr.append(f'<span class="chip muted">裁決日期 {esc(cur["date"])}</span>')
    parts.append(f'<div class="verdict-row">{"".join(vr)}</div>')
    parts.append(render_snapshot(stock, as_of))

    def section(title, count, body):
        return (f'<section class="blk"><h2>{esc(title)}</h2>'
                f'<div class="cnt">{count} 筆</div>{body}</section>')

    # 個股研究 (all DDs)
    if dd_rows:
        lis = []
        for r in dd_rows:
            vtag = f'<span class="tag">{esc(r["verdict"])}</span>' if r["verdict"] != "—" else ""
            era = f' <span class="it-sub">{esc(r["era"])}</span>' if r["era"] else ""
            lis.append(
                f'<li><span class="dt">{esc(r["date"])}</span>'
                f'<span class="it-main"><a href="{esc(r["path"])}">DD 報告</a>{era}</span>'
                f'{vtag}</li>'
            )
        parts.append(section("個股研究", len(dd_rows), f'<ul class="items">{"".join(lis)}</ul>'))

    # 所屬產業研究
    if ids:
        lis = []
        for r in ids:
            sub = []
            if r.get("sd_verdict"):
                sub.append(f'供需 {esc(r["sd_verdict"])}')
            if r.get("clock_phase"):
                sub.append(f'時鐘 {esc(r["clock_phase"])}')
            subtxt = f'<span class="it-sub"> · {" · ".join(sub)}</span>' if sub else ""
            dt = f'<span class="dt">{esc(r["date"])}</span>' if r["date"] else '<span class="dt">—</span>'
            lis.append(
                f'<li>{dt}<span class="it-main">'
                f'<a href="{esc(r["path"])}">{esc(r["theme"])}</a>{subtxt}</span></li>'
            )
        parts.append(section("所屬產業研究", len(ids), f'<ul class="items">{"".join(lis)}</ul>'))

    # 供應鏈位置
    if sc:
        lis = []
        for r in sc:
            nodes = "、".join(r["nodes"][:6]) if r["nodes"] else ""
            ntxt = f'<span class="it-sub"> · {esc(nodes)}</span>' if nodes else ""
            lis.append(
                f'<li><span class="it-main">'
                f'<a href="/supply-chain/{esc(r["topic_id"])}.html">{esc(r["title"])}</a>{ntxt}</span></li>'
            )
        parts.append(section("供應鏈位置", len(sc), f'<ul class="items">{"".join(lis)}</ul>'))

    # 對比研究
    if comps:
        lis = []
        for r in comps:
            others = "、".join(t for t in r["tickers"] if t != ticker)
            sub = f'<span class="it-sub"> · vs {esc(others)}</span>' if others else ""
            lis.append(
                f'<li><span class="dt">{esc(r["date"])}</span>'
                f'<span class="it-main"><a href="{esc(r["path"])}">多股對比</a>{sub}</span></li>'
            )
        parts.append(section("對比研究", len(comps), f'<ul class="items">{"".join(lis)}</ul>'))

    # 期望落差綜合
    if syns:
        lis = []
        for r in syns:
            lis.append(
                f'<li><span class="dt">{esc(r["date"])}</span>'
                f'<span class="it-main"><a href="{esc(r["path"])}">期望落差綜合研判</a></span></li>'
            )
        parts.append(section("期望落差綜合", len(syns), f'<ul class="items">{"".join(lis)}</ul>'))

    parts.append(f'<div class="foot-note">{FOOTNOTE}</div>')
    parts.append('</main>')
    parts.append(FOOTER)
    parts.append('</body>\n</html>')
    return "\n".join(parts) + "\n"


def render_index(universe_sorted, dd_by_ticker, cur_by_ticker, cov_counts):
    total_reports = sum(len(dd_by_ticker[t]) for t in universe_sorted)
    n_verdict = sum(1 for t in universe_sorted
                    if cur_by_ticker.get(t) and cur_by_ticker[t]["era"] == "裁決")
    head = page_head(
        "個股總覽 · Ticker Hub — InvestMQuest Research",
        "按 ticker 聚合 InvestMQuest 站內全部研究（個股 DD／產業 ID／供應鏈／對比／期望落差綜合）的目錄索引。",
    )
    parts = [head, '<main class="wrap">']
    parts.append('<div class="overline">Ticker Hub · 個股總覽</div>')
    parts.append('<h1 class="tk serif">個股總覽</h1>')
    parts.append('<p class="oneliner">專業投資人以 ticker 為單位思考，但本站以報告類型分區。'
                 '此頁按 ticker 聚合站內全部研究——每檔一個入口，收攏其個股 DD、所屬產業 ID、'
                 '供應鏈位置、多股對比與期望落差綜合研判。</p>')
    stats = [
        (len(universe_sorted), "檔 ticker"),
        (total_reports, "份 DD 報告"),
        (n_verdict, "檔具現行裁決"),
    ]
    parts.append('<div class="dir-stats">' + "".join(
        f'<div class="stat"><div class="n">{n}</div><div class="k">{esc(k)}</div></div>'
        for n, k in stats
    ) + '</div>')
    parts.append('<input id="flt" type="text" placeholder="輸入 ticker 篩選…（例：NVDA、2330.TW）" '
                 'autocomplete="off" aria-label="篩選 ticker">')
    cards = []
    for t in universe_sorted:
        cur = cur_by_ticker.get(t)
        n = len(dd_by_ticker[t])
        if cur:
            chip = verdict_chip(cur["verdict"], "")
        else:
            chip = '<span class="chip muted">—</span>'
        cards.append(
            f'<a class="tcard" data-tk="{esc(t.upper())}" href="/t/{esc(t)}.html">'
            f'<div class="tk">{esc(t)}</div>'
            f'<div class="meta">{chip}<span class="rc">{n} 份</span></div></a>'
        )
    parts.append(f'<div class="grid" id="grid">{"".join(cards)}</div>')
    parts.append('<div class="nores" id="nores">無符合的 ticker。</div>')
    parts.append(f'<div class="foot-note">{FOOTNOTE}</div>')
    parts.append('</main>')
    parts.append(FOOTER)
    parts.append("""<script>
(function(){
  var flt=document.getElementById('flt'),grid=document.getElementById('grid'),nores=document.getElementById('nores');
  var cards=Array.prototype.slice.call(grid.querySelectorAll('.tcard'));
  flt.addEventListener('input',function(){
    var q=flt.value.trim().toUpperCase(),shown=0;
    cards.forEach(function(c){
      var hit=q===''||c.getAttribute('data-tk').indexOf(q)!==-1;
      c.style.display=hit?'':'none';
      if(hit)shown++;
    });
    nores.style.display=shown===0?'block':'none';
  });
})();
</script>""")
    parts.append('</body>\n</html>')
    return "\n".join(parts) + "\n"


def main():
    universe_meta, dd_by_ticker, token_map, dd_skipped = gather_dd()
    universe = set(universe_meta.keys())
    ids = gather_ids()
    sc = gather_supply_chain()
    comps = gather_comparisons(universe)
    syns = gather_synthesis()
    stocks, as_of = load_screener()

    cur_by_ticker = universe_meta  # newest-with-meta row per ticker
    universe_sorted = sorted(universe, key=lambda s: s.upper())

    # clean regenerate of docs/t/
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    for t in universe_sorted:
        html_str = render_ticker_page(
            t, dd_by_ticker[t], cur_by_ticker.get(t),
            ids.get(t, []), sc.get(t, []), comps.get(t, []), syns.get(t, []),
            stocks.get(t), as_of,
        )
        (OUT / f"{t}.html").write_text(html_str, encoding="utf-8")

    cov_counts = {}
    (OUT / "index.html").write_text(
        render_index(universe_sorted, dd_by_ticker, cur_by_ticker, cov_counts),
        encoding="utf-8",
    )

    total_bytes = sum(f.stat().st_size for f in OUT.glob("*.html"))
    print(f"tickers            : {len(universe_sorted)}")
    print(f"pages (incl index) : {len(universe_sorted) + 1}")
    print(f"docs/t total size  : {total_bytes/1024:.1f} KB")
    print(f"ids covered        : {len(ids)} tickers have >=1 ID theme")
    print(f"supply-chain covered: {len(sc)} tickers appear in a map")
    print(f"comparisons covered: {len(comps)} tickers")
    print(f"synthesis covered  : {len(syns)} tickers")
    if dd_skipped:
        print(f"DD files skipped (no meta + unresolved token): {len(dd_skipped)}")
    # example coverage
    for ex in ("NVDA", "TSM", "2330.TW"):
        if ex in universe:
            print(f"  [{ex}] DD={len(dd_by_ticker[ex])} ID={len(ids.get(ex,[]))} "
                  f"SC={len(sc.get(ex,[]))} CMP={len(comps.get(ex,[]))} SYN={len(syns.get(ex,[]))}")
        else:
            print(f"  [{ex}] not in universe")


if __name__ == "__main__":
    main()
