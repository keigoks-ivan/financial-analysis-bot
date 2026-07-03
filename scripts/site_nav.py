#!/usr/bin/env python3
"""Canonical site header (imq-nav) — single source of truth + idempotent injector.

The canonical nav is defined here once. Running this script over docs/ will:
  1. strip every known legacy/variant site header (imq-nav-root header blocks,
     dedicated nav <style> blocks, imq-dd toggle <script>s, legacy
     <nav class="imq-nav">, supply-chain <header class="site">, the old
     six-state plain header, the tools/ wordpress header)
  2. re-insert the canonical unit (style + header + script) right after <body>,
     with the active group/item derived from the file's path
  3. for /dd-screener/ pages, append the section sub-nav strip (sibling pages)
     below the site header — mirroring the /backtest/ pill-bar pattern

Idempotent: re-running produces identical output. New pages from any skill or
generator are picked up on the next run (update_dd_index.py calls this).

External generators (v7-backtest, morning-briefing, minervini-quality-backtest)
embed a copy of NAV_STYLE / NAV_HTML / NAV_SCRIPT — when changing the nav here,
re-sync those templates too (see .claude/notes/site-composition.md).

Usage:
    python3 scripts/site_nav.py            # apply to docs/
    python3 scripts/site_nav.py --check    # report variants, change nothing
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs"

# ---------------------------------------------------------------- canonical

NAV_STYLE = """<style id="imq-nav-style">
.imq-nav-root{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.imq-nav-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.imq-logo{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}
.imq-logo:hover{color:#fff !important;text-decoration:none !important}
.imq-logo span{color:#3b82f6}
.imq-menu{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}
.imq-menu > a,.imq-dd-btn{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}
.imq-menu > a:hover,.imq-dd-btn:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-menu > a.active,.imq-dd.active > .imq-dd-btn{color:#fff !important;background:rgba(59,130,246,.22);font-weight:600}
.imq-dd{position:relative;display:inline-block}
.imq-dd-menu{display:none;position:absolute;top:100%;left:0;background:#1e293b;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{display:block}
.imq-dd-menu a{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}
.imq-dd-menu a:hover{color:#fff !important;background:rgba(59,130,246,.18)}
.imq-dd-menu a.active{color:#fff !important;background:rgba(59,130,246,.22);font-weight:600}
.imq-caret{font-size:.6rem;opacity:.7;margin-top:1px}
.imq-subnav{background:#0f172a;padding:.45rem 20px;font-family:'Inter','Noto Sans TC',-apple-system,sans-serif}
.imq-subnav-inner{max-width:1140px;margin:0 auto;display:flex;gap:.3rem;flex-wrap:wrap}
.imq-subnav a{color:rgba(255,255,255,.55) !important;font-size:.74rem;font-weight:500;padding:.28rem .6rem;border-radius:5px;text-decoration:none !important}
.imq-subnav a:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-subnav a.active{color:#fff !important;background:rgba(59,130,246,.28);font-weight:600}
@media(max-width:768px){
  .imq-nav-root{padding:.55rem 12px}
  .imq-nav-inner{gap:.4rem}
  .imq-menu{width:100%;justify-content:flex-start;gap:.1rem}
  .imq-menu > a,.imq-dd-btn{font-size:.74rem;padding:.32rem .5rem}
  .imq-dd-menu{position:static;display:none;min-width:auto;box-shadow:none;background:rgba(255,255,255,.04);border:none;padding:.1rem 0 .3rem 1rem;margin:.1rem 0}
  .imq-dd.open .imq-dd-menu{display:block}
}
</style>"""

NAV_SCRIPT = """<script>(function(){document.querySelectorAll('.imq-dd-btn').forEach(function(btn){btn.addEventListener('click',function(e){e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){if(d!==dd)d.classList.remove('open')});dd.classList.toggle('open')})});document.addEventListener('click',function(e){if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){d.classList.remove('open')})});})();</script>"""

# (group, item, href, label) — groups: home / research / market / quant / mm / howto
MENU = {
    "research": [
        ("dd", "/research/", "個股 DD"),
        ("syn", "/research/synthesis/", "期望落差綜合研判"),
        ("id", "/id/", "產業深度 ID"),
        # ("ds", "/ds/", "產業敘述 DS"),  # 2026-06-25 封存 /ds/（已併入 ID）— 自 nav 移除
        ("cmp", "/comparisons/", "多股對比"),
        ("sc", "/supply-chain/", "供應鏈地圖"),
        ("tier", "/id/tier_matrix.html", "🎯 Tier Matrix"),
    ],
    "market": [
        ("brief", "/briefing/", "每日簡報"),
        ("week", "/weekly/", "週報"),
        ("earn", "/earnings/", "財報分析"),
        ("markets", "/markets.html", "Markets"),
        ("sectors", "/sectors.html", "Sectors"),
        ("ltsmh", "/long-track-smh/", "長線訊號"),
        ("lttw", "/long-track-tw/", "台股長線"),
        ("sleeve", "/turtle-sleeve/", "商品 Sleeve"),
    ],
    "quant": [
        ("bt", "/backtest/", "量化回測"),
        ("dds", "/dd-screener/", "DD Screener"),
        ("qus", "/qgm/", "QGM 美股"),
        ("qtw", "/qgm-tw/", "QGM 台股"),
        ("scr_us", "/screener.html", "Screener 美股"),
        ("scr_tw", "/screener-tw.html", "Screener 台股"),
        ("scr_jp", "/screener-jp.html", "Screener 日股"),
        ("scr_my", "/screener-my.html", "Screener 馬股"),
        ("cache", "/cache/", "🗄 Data Cache"),
        ("tools", "/tools/", "期貨部位計算機"),
    ],
}
GROUP_LABELS = {"research": "研究", "market": "市場", "quant": "工具"}


def build_nav(group=None, item=None):
    def dd(name):
        links = "\n".join(
            f'          <a href="{href}"{" class=\"active\"" if group == name and item == key else ""}>{label}</a>'
            for key, href, label in MENU[name]
        )
        act = " active" if group == name else ""
        return (
            f'      <div class="imq-dd{act}">\n'
            f'        <button type="button" class="imq-dd-btn">{GROUP_LABELS[name]}<span class="imq-caret">▾</span></button>\n'
            f'        <div class="imq-dd-menu">\n{links}\n        </div>\n'
            f"      </div>"
        )

    home_cls = ' class="active"' if group == "home" else ""
    mm_cls = ' class="active"' if group == "mm" else ""
    howto_cls = ' class="active"' if group == "howto" else ""
    return f"""<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/"{home_cls}>首頁</a>
{dd("research")}
{dd("market")}
{dd("quant")}
      <a href="/mental-models/"{mm_cls}>🧠 心智模型</a>
      <a href="/how-to.html"{howto_cls}>📘 使用說明</a>
    </nav>
  </div>
</header>"""


def full_nav_block(group=None, item=None, subnav=""):
    return NAV_STYLE + "\n" + build_nav(group, item) + subnav + "\n" + NAV_SCRIPT


# ------------------------------------------------------------- section subnav

DD_SCREENER_SUBNAV = [
    ("/dd-screener/", "總覽"),
    ("/dd-screener/pipeline.html", "🧭 Pipeline"),
    ("/dd-screener/targets.html", "🎯 標的清單"),
    ("/dd-screener/quality-entry.html", "Quality-Entry"),
    ("/dd-screener/cyclical-track.html", "衛星·循環軌"),
    ("/dd-screener/bottom-out.html", "Bottom-Out"),
    ("/dd-screener/breakout.html", "Breakout"),
    ("/dd-screener/earnings-acceleration.html", "盈餘加速"),
    ("/dd-screener/entry-state.html", "Entry-State"),
    ("/dd-screener/entry-state-backtest.html", "Entry 回測"),
    ("/dd-screener/sop-funnel.html", "SOP Funnel"),
    ("/dd-screener/sop-funnel-backtest.html", "SOP 回測"),
    ("/dd-screener/alpha-rank.html", "Alpha Rank"),
]


def build_subnav(links, current):
    items = "".join(
        f'<a href="{href}"{" class=\"active\"" if href == current else ""}>{label}</a>'
        for href, label in links
    )
    return f'\n<div class="imq-subnav"><div class="imq-subnav-inner">{items}</div></div>'


# ----------------------------------------------------------- active mapping

PREFIX_ACTIVE = [
    ("research/synthesis/", ("research", "syn")),
    ("research/", ("research", "dd")),
    ("dd/", ("research", "dd")),
    ("dca/", ("research", "dd")),
    ("report/", ("research", "dd")),
    ("id/tier_matrix.html", ("research", "tier")),
    ("id/", ("research", "id")),
    ("ds/", ("research", "ds")),
    ("comparisons/", ("research", "cmp")),
    ("supply-chain/", ("research", "sc")),
    ("briefing/", ("market", "brief")),
    ("weekly/", ("market", "week")),
    ("earnings/", ("market", "earn")),
    ("markets.html", ("market", "markets")),
    ("sectors.html", ("market", "sectors")),
    ("long-track-smh/", ("market", "ltsmh")),
    ("long-track-tw/", ("market", "lttw")),
    ("turtle-sleeve/", ("market", "sleeve")),
    ("backtest/", ("quant", "bt")),
    ("dd-screener/", ("quant", "dds")),
    ("qgm/", ("quant", "qus")),
    ("qgm-tw/", ("quant", "qtw")),
    ("screener.html", ("quant", "scr_us")),
    ("screener-tw.html", ("quant", "scr_tw")),
    ("screener-jp.html", ("quant", "scr_jp")),
    ("screener-my.html", ("quant", "scr_my")),
    ("cache/", ("quant", "cache")),
    ("tools/", ("quant", "tools")),
    ("mental-models/", ("mm", None)),
    ("how-to.html", ("howto", None)),
    ("index.html", ("home", None)),
]

SKIP_DIRS = {"_archived", "private"}
SKIP_FILES = {
    "pm/index.html",                            # archived stub, intentionally bare
    "six-state/index.html",                     # redirect stub -> /backtest/six_state/status/
    "backtest/six_state/status/index.html",     # live status sub-page, intentionally headerless
}


def active_for(rel: str):
    for prefix, ga in PREFIX_ACTIVE:
        if rel == prefix or rel.startswith(prefix):
            return ga
    return (None, None)


# ------------------------------------------------------------ legacy removal

STRIP_PATTERNS = [
    # canonical + all imq-nav-root header variants
    re.compile(r'[ \t]*<header class="imq-nav-root"[^>]*>.*?</header>\n?', re.S),
    # dedicated nav style blocks (canonical id= form and bare legacy form)
    re.compile(r'[ \t]*<style id="imq-nav-style">.*?</style>\n?', re.S),
    re.compile(r"[ \t]*<style>\s*\.imq-nav-root\{.*?</style>\n?", re.S),
    # dropdown toggle scripts
    re.compile(r"[ \t]*<script>\(function\(\)\{document\.querySelectorAll\('\.imq-dd-btn'\).*?</script>\n?", re.S),
    # legacy hover-nav used by earnings dailies
    re.compile(r'[ \t]*<nav class="imq-nav">.*?</nav>\n?', re.S),
    # supply-chain hub/topic header
    re.compile(r'[ \t]*<header class="site">.*?</header>\n?', re.S),
    # old six-state plain header
    re.compile(r'[ \t]*<header>\s*<div class="container hdr-inner">.*?</header>\n?', re.S),
    # tools/ wordpress-site header
    re.compile(r'[ \t]*<header class="site-header">.*?</header>\n?', re.S),
    # injected sub-nav strip (re-runs)
    re.compile(r'[ \t]*<div class="imq-subnav">.*?</div></div>\n?', re.S),
]

BODY_RE = re.compile(r"<body[^>]*>")


def process(path: Path, check=False):
    rel = str(path.relative_to(ROOT))
    if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
        return "skip"
    if rel in SKIP_FILES:
        return "skip"
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "non-utf8"
    m = BODY_RE.search(text)
    if not m:
        return "no-body"

    stripped = text
    for pat in STRIP_PATTERNS:
        stripped = pat.sub("", stripped)

    group, item = active_for(rel)
    subnav = ""
    if rel.startswith("dd-screener/"):
        subnav = build_subnav(DD_SCREENER_SUBNAV, "/" + rel)
    block = full_nav_block(group, item, subnav)

    m = BODY_RE.search(stripped)
    new = stripped[: m.end()] + "\n" + block + stripped[m.end():]
    if new == text:
        return "unchanged"
    if not check:
        path.write_text(new, encoding="utf-8")
    return "updated"


def main():
    check = "--check" in sys.argv
    counts = {}
    issues = []
    for path in sorted(ROOT.rglob("*.html")):
        status = process(path, check=check)
        counts[status] = counts.get(status, 0) + 1
        if status in ("no-body", "non-utf8"):
            issues.append((status, str(path.relative_to(ROOT))))
    for k, v in sorted(counts.items()):
        print(f"{k:10s} {v}")
    for status, rel in issues:
        print(f"  ⚠️  {status}: {rel}")


if __name__ == "__main__":
    main()
