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
.imq-nav-root{background:linear-gradient(135deg,#081832 0%,#173564 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.imq-nav-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.imq-logo{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}
.imq-logo:hover{color:#fff !important;text-decoration:none !important}
.imq-logo span{color:#d4b576}
.imq-menu{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}
.imq-menu > a,.imq-dd-btn{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}
.imq-menu > a:hover,.imq-dd-btn:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-menu > a.active,.imq-dd.active > .imq-dd-btn{color:#fff !important;background:rgba(184,146,74,.26);font-weight:600}
.imq-dd{position:relative;display:inline-block}
.imq-dd-menu{display:none;position:absolute;top:100%;left:0;background:#0d2244;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{display:block}
.imq-dd-menu a{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}
.imq-dd-menu a:hover{color:#fff !important;background:rgba(184,146,74,.20)}
.imq-dd-menu a.active{color:#fff !important;background:rgba(184,146,74,.26);font-weight:600}
.imq-caret{font-size:.6rem;opacity:.7;margin-top:1px}
.imq-subnav{background:#081832;padding:.45rem 20px;font-family:'Inter','Noto Sans TC',-apple-system,sans-serif}
.imq-subnav-inner{max-width:1140px;margin:0 auto;display:flex;gap:.3rem;flex-wrap:wrap}
.imq-subnav a{color:rgba(255,255,255,.55) !important;font-size:.74rem;font-weight:500;padding:.28rem .6rem;border-radius:5px;text-decoration:none !important}
.imq-subnav a:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-subnav a.active{color:#fff !important;background:rgba(184,146,74,.30);font-weight:600}
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

# (group, item, href, label) — groups: home / pick / research / market / system / mm / howto
# 2026-07-07 整站 IA v2（見 notes/site-internal/root/_proposal_site_ia_20260707.md）：
# 三群 catch-all（研究/市場/工具）改為四群意圖式（選股/研究/市場/系統）——
# 選股系統原散在研究+工具兩選單，收斂為單一「選股」群；跨資產三頁（描述器）
# 自研究移入市場；每日簡報已暫停自 nav 移除（/briefing/ 歸檔頁仍可直達）。
MENU = {
    # 2026-07-10 選股主控台整併（見 notes/site-internal/root/_consolidation_stock_console_20260710.md）：
    # 精選榜／流程板機／席位排序（＋原駕駛艙總覽）四頁已收斂進單一 /cockpit/ 四分頁，
    # 故下拉移除 picks／pipe／eng 三個舊條目，只留單一「選股主控台」入口。
    # 舊 URL 皆為活 redirect stub，外部書籤與外部 3 repo 舊 nav 仍可用。
    # 非四頁條目（DD Screener 主表／Momentum-5／QGM／RS+VCP）保留不動。
    "pick": [
        ("cockpit", "/cockpit/", "選股主控台"),
        ("dds", "/dd-screener/", "DD Screener"),
        ("mom5", "/research/momentum-5/", "Momentum-5"),
        ("qus", "/qgm/", "QGM 美股"),
        ("qtw", "/qgm-tw/", "QGM 台股"),
        ("scr", "/screeners.html", "RS+VCP Screener"),
    ],
    "research": [
        ("thub", "/t/", "個股總覽"),
        ("dd", "/research/", "個股 DD"),
        ("id", "/id/", "產業深度 ID"),
        ("tier", "/id/tier_matrix.html", "Tier Matrix"),
        ("sc", "/supply-chain/", "供應鏈地圖"),
        ("cmp", "/comparisons/", "多股對比"),
        ("syn", "/research/synthesis/", "期望落差綜合研判"),
    ],
    "market": [
        ("mon", "/monitor/", "市場監測"),
        ("det", "/detective/", "偵測警報網"),
        ("radar", "/rotation/radar.html", "資產輪動雷達"),
        ("rot", "/rotation/", "產業輪動"),
        ("crowd", "/crowding/", "擁擠交易監測"),
        ("regime", "/regime/", "大類資產 regime"),
        ("macro", "/macro/", "總經深度報告"),
        ("earn", "/earnings/", "財報分析"),
        ("cat", "/catalyst/", "催化劑日曆"),
        ("markets", "/markets.html", "Markets"),
        ("sectors", "/sectors.html", "Sectors"),
        # 2026-07-11 週報已停更，自頁首移除（/weekly/ 頁面保留可直達；
        # PREFIX_ACTIVE 的 weekly/ 映射保留，使其頁面仍歸市場群 active）
    ],
    "system": [
        ("tr", "/track-record/", "裁決實績"),
        ("ltsmh", "/long-track-smh/", "長線訊號 SMH"),
        ("ltqsvt", "/long-track-qs-vt/", "QQQ+SMH 波動率"),
        ("lttw", "/long-track-tw/", "台股長線"),
        ("sleeve", "/turtle-sleeve/", "商品 Sleeve"),
        ("bt", "/backtest/", "量化回測"),
        ("tools", "/tools/", "期貨部位計算機"),
        ("cache", "/cache/", "Data Cache"),
        ("data", "/data.html", "公開資料"),
    ],
}
GROUP_LABELS = {"pick": "選股", "research": "研究", "market": "市場", "system": "系統"}


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
    search_cls = ' class="active"' if group == "search" else ""
    return f"""<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/"{home_cls}>首頁</a>
{dd("market")}
{dd("pick")}
{dd("research")}
      <a href="/mental-models/"{mm_cls}>心智模型</a>
{dd("system")}
      <a href="/how-to.html"{howto_cls}>使用指南</a>
      <a href="/search.html"{search_cls}>搜尋</a>
    </nav>
  </div>
</header>"""


def full_nav_block(group=None, item=None, subnav=""):
    return NAV_STYLE + "\n" + build_nav(group, item) + subnav + "\n" + NAV_SCRIPT


# ------------------------------------------------------------- section subnav

# 2026-07-07 選股頁面整理：targets / bottom-out / breakout / 盈餘加速 /
# entry-state（含回測）/ alpha-rank / state-machine 已封存（noindex stub），
# 從子選單移除；見 notes/site-internal/root/_proposal_stock_pages_cleanup_20260707.md。
DD_SCREENER_SUBNAV = [
    ("/dd-screener/", "總覽"),
    ("/dd-screener/pipeline.html", "Pipeline"),
    ("/dd-screener/quality-entry.html", "Quality-Entry"),
    ("/dd-screener/cyclical-track.html", "衛星·循環軌"),
    ("/dd-screener/sop-funnel.html", "SOP Funnel"),
    ("/dd-screener/sop-funnel-backtest.html", "SOP 回測"),
]


ENGINE_SUBNAV = [
    ("/engine/", "總覽 · 方法論"),
    ("/engine/radar.html", "全市場雷達"),
    ("/engine/cards.html", "決策卡"),
    ("/engine/arena.html", "席位擂台"),
    ("/engine/scoreboard.html", "形狀記分板"),
]


def build_subnav(links, current):
    items = "".join(
        f'<a href="{href}"{" class=\"active\"" if href == current else ""}>{label}</a>'
        for href, label in links
    )
    return f'\n<div class="imq-subnav"><div class="imq-subnav-inner">{items}</div></div>'


# ----------------------------------------------------------- active mapping

PREFIX_ACTIVE = [
    # 選股群
    ("cockpit/", ("pick", "cockpit")),
    # picks/ · dd-screener/pipeline.html · engine/ 皆為 redirect stub / iframe 片段（全在 SKIP_FILES，
    # 不會被注入 nav）；保留前綴僅為「選股群高亮」的語意錨，不再對應下拉條目（item=None）。
    ("picks/", ("pick", None)),
    ("dd-screener/pipeline.html", ("pick", None)),
    ("dd-screener/", ("pick", "dds")),
    ("engine/", ("pick", None)),
    ("research/momentum-5/", ("pick", "mom5")),
    ("qgm/", ("pick", "qus")),
    ("qgm-tw/", ("pick", "qtw")),
    ("screeners.html", ("pick", "scr")),
    ("screener.html", ("pick", "scr")),
    ("screener-tw.html", ("pick", "scr")),
    ("screener-jp.html", ("pick", "scr")),
    ("screener-my.html", ("pick", "scr")),
    # 研究群
    ("t/", ("research", "thub")),  # 個股總覽（2026-07-11 新增）
    ("research/synthesis/", ("research", "syn")),
    ("research/", ("research", "dd")),
    ("dd/", ("research", "dd")),
    ("dca/", ("research", "dd")),
    ("report/", ("research", "dd")),
    ("id/tier_matrix.html", ("research", "tier")),
    ("id/", ("research", "id")),
    ("ds/", ("research", "id")),
    ("comparisons/", ("research", "cmp")),
    ("supply-chain/", ("research", "sc")),
    # 市場群
    ("earnings/", ("market", "earn")),
    ("catalyst/", ("market", "cat")),
    ("monitor/", ("market", "mon")),  # 全資產市場監測（2026-07-10）
    ("detective/", ("market", "det")),  # 市場偵測器 v2 警報網（2026-07-16；noindex 保留）
    ("markets.html", ("market", "markets")),
    ("sectors.html", ("market", "sectors")),
    ("crowding/", ("market", "crowd")),
    # rotation/radar.html 是「資產輪動雷達」獨立項目；須排在 rotation/ 之前，
    # 否則會被 rotation/ 前綴吃掉。index.html 與 ROTATION_*.html 仍歸「產業輪動」。
    ("rotation/radar.html", ("market", "radar")),  # 資產輪動雷達（2026-07-11 新增）
    ("rotation/", ("market", "rot")),
    ("regime/", ("market", "regime")),
    ("macro/", ("market", "macro")),  # 總經深度報告（2026-07-09），nav 已掛項目
    ("weekly/", ("market", "week")),
    ("briefing/", ("market", None)),  # 已暫停，nav 無項目，僅群高亮
    # 系統群
    ("track-record/", ("system", "tr")),  # 裁決實績（2026-07-11 新增）
    ("long-track-smh/", ("system", "ltsmh")),
    ("long-track-qs-vt/", ("system", "ltqsvt")),
    ("long-track-tw/", ("system", "lttw")),
    ("turtle-sleeve/", ("system", "sleeve")),
    ("backtest/", ("system", "bt")),
    ("tools/", ("system", "tools")),
    ("cache/", ("system", "cache")),
    ("data.html", ("system", "data")),  # 公開資料（2026-07-11 新增）
    # 頂層
    ("mental-models/", ("mm", None)),
    ("how-to.html", ("howto", None)),
    ("search.html", ("search", None)),  # 搜尋（2026-07-11 新增頂層連結）
    ("index.html", ("home", None)),
]

SKIP_DIRS = {"_archived", "private"}
# 外部三 repo（+ 其 cron）擁有的 docs/ 子樹（見 .claude/notes/site-composition.md）：
#   qgm / qgm-tw → minervini-quality-backtest；briefing / weekly → morning-briefing；
#   backtest → v7-backtest。這些頁面的 nav 由各自 repo 內嵌的 canonical literal 重生，
#   本 repo 的 re-inject sweep 必須跳過整棵樹（否則會在工作區改動 400+ 支外部檔，
#   且下次外部 cron push 會覆蓋）。改 nav 時：本 repo re-inject 只動自有頁面，
#   外部樹靠 step「re-sync 三個外部 repo 的 synced literal」重生 byte-identical。
EXTERNAL_TREES = {"qgm", "qgm-tw", "briefing", "weekly", "backtest"}
SKIP_FILES = {
    "jot.html",                                 # 私人餵腦框（noindex 獨立小頁，不掛站 nav）
    "pm/index.html",                            # archived stub, intentionally bare
    "six-state/index.html",                     # redirect stub -> /backtest/six_state/status/
    "backtest/six_state/status/index.html",     # live status sub-page, intentionally headerless
    # 2026-07-10 選股主控台整併：舊 4 頁折進 /cockpit/ 四分頁。
    # 這 3 個 redirect stub 與 3 個 nav-less iframe 片段一律不注入站 nav
    # （片段被灌 nav 會在 iframe 內冒出整條站選單；stub 應保持極簡）。
    "picks/index.html",                         # redirect stub -> /cockpit/#picks
    "dd-screener/pipeline.html",                # redirect stub -> /cockpit/#pipeline
    "engine/index.html",                        # redirect stub -> /cockpit/#seats
    "picks/_embed.html",                        # iframe 片段（精選榜分頁）
    "dd-screener/_pipeline_body.html",          # iframe 片段（流程板機分頁）
    "engine/_index_body.html",                  # iframe 片段（席位排序·席位總表子分頁）
    # 2026-07-10 engine 四子頁收編成 /cockpit/#seats 子分頁：
    # 舊 4 URL → redirect stub；builder 改產 nav-less _*_body 片段（供子分頁 iframe）。
    "engine/radar.html",                        # redirect stub -> /cockpit/#seats-radar
    "engine/arena.html",                        # redirect stub -> /cockpit/#seats-arena
    "engine/cards.html",                        # redirect stub -> /cockpit/#seats-cards
    "engine/scoreboard.html",                   # redirect stub -> /cockpit/#seats-scoreboard
    "engine/_radar_body.html",                  # iframe 片段（雷達子分頁）
    "engine/_arena_body.html",                  # iframe 片段（擂台子分頁·M5 對照組 PREREG 凍結）
    "engine/_cards_body.html",                  # iframe 片段（決策卡子分頁）
    "engine/_scoreboard_body.html",             # iframe 片段（記分板子分頁）
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
    parts = path.relative_to(ROOT).parts
    if any(part in SKIP_DIRS for part in parts):
        return "skip"
    if parts and parts[0] in EXTERNAL_TREES:
        return "skip-external"
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
    elif rel.startswith("engine/"):
        cur = "/engine/" if rel == "engine/index.html" else "/" + rel
        subnav = build_subnav(ENGINE_SUBNAV, cur)
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
