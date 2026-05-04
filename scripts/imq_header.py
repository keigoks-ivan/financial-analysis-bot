#!/usr/bin/env python3
"""
imq_header.py — Unified IMQ minimal header renderer (Python + vanilla HTML/CSS/JS).

Usage:
    from imq_header import build_imq_header, get_section_from_path, get_regime

    section = get_section_from_path("/dd/DD_QCOM_20260504.html")
    regime  = get_regime()                       # reads from docs/data/regime.json or fallback
    header_html = build_imq_header(
        section=section,
        regime=regime,
        updated_at="2026-05-04 08:00 TST",      # pass file mtime or build time
        breadcrumb=[                              # empty list = hidden
            {"label": "研究", "href": "https://research.investmquest.com/research/"},
            {"label": "DD · 個股深度", "href": "https://research.investmquest.com/research/"},
            {"label": "QCOM 2026Q1"},             # no href = current page
        ],
    )

All design tokens match the handoff README exactly.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants (design tokens — do NOT change without updating README)
# ---------------------------------------------------------------------------

BASE = "https://research.investmquest.com"

SECTION_LABELS: dict[str, str] = {
    "research":      "RESEARCH",
    "market":        "MARKET",
    "mental-models": "MENTAL-MODELS",
    "tools":         "TOOLS",
    "how-to":        "HOW-TO",
    "home":          "RESEARCH",   # homepage falls back to RESEARCH for rule text
}

NAV_LINKS = [
    ("研究",     f"{BASE}/research/",       "research"),
    ("市場",     f"{BASE}/market/",         "market"),
    ("心智模型", f"{BASE}/mental-models/",  "mental-models"),
    ("工具",     f"{BASE}/tools/",          "tools"),
    ("指南",     f"{BASE}/how-to/",         "how-to"),
]

REGIME_JSON_PATH = Path(__file__).parent.parent / "docs" / "data" / "regime.json"
DEFAULT_REGIME = 3   # TODO: replace with live data source once regime API endpoint is wired

TST = timezone(timedelta(hours=8))   # Taiwan Standard Time = UTC+8


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_section_from_path(page_path: str) -> str:
    """
    Map a docs-relative or absolute URL path to one of the 5 nav sections.

    Returns one of: 'research', 'market', 'mental-models', 'tools', 'how-to', 'home', or ''.
    """
    p = page_path.lstrip("/")

    if p in ("index.html", "", "index"):
        return "home"

    # 研究 bucket
    research_prefixes = (
        "research/", "dd/", "id/", "pm/", "earnings/",
        "six-state/", "briefing/",
    )
    for prefix in research_prefixes:
        if p.startswith(prefix):
            return "research"

    # 市場 bucket
    if p in ("markets.html", "sectors.html") or p.startswith("market/"):
        return "market"

    # 心智模型
    if p.startswith("mental-models/"):
        return "mental-models"

    # 工具
    tools_prefixes = ("qgm/", "qgm-tw/", "backtest/", "tools/")
    if p in ("screener.html", "screener-tw.html") or p.startswith("screener"):
        return "tools"
    for prefix in tools_prefixes:
        if p.startswith(prefix):
            return "tools"

    # 指南
    if p in ("how-to.html",) or p.startswith("how-to/"):
        return "how-to"

    return ""


def get_regime() -> int:
    """
    Read current market regime (1-6) from docs/data/regime.json if it exists.
    Falls back to DEFAULT_REGIME (3) with a TODO comment.

    JSON format expected: {"regime": 3, "updated": "2026-05-04"}
    """
    # TODO: wire this to a live regime data source once the market regime API
    #       endpoint is available.  Currently the six-state machine uses S1/S2/
    #       S1.5/S0/S5 labels (not the 1-6 integer scale), so until the mapping
    #       from six-state → regime 1-6 is formalised, we return DEFAULT_REGIME.
    if REGIME_JSON_PATH.exists():
        try:
            data = json.loads(REGIME_JSON_PATH.read_text())
            val = int(data.get("regime", DEFAULT_REGIME))
            if 1 <= val <= 6:
                return val
        except Exception:
            pass
    return DEFAULT_REGIME


def get_updated_at(file_path: Path | None = None) -> str:
    """
    Return a formatted 'YYYY-MM-DD HH:MM TST' string.
    Uses file mtime if file_path is given and exists, else current build time.
    """
    if file_path and file_path.exists():
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
    else:
        mtime = datetime.now(tz=timezone.utc)
    tst_dt = mtime.astimezone(TST)
    return tst_dt.strftime("%Y-%m-%d %H:%M TST")


# ---------------------------------------------------------------------------
# CSS block (verbatim design tokens from handoff README)
# ---------------------------------------------------------------------------

IMQ_H_CSS = """\
<style id="imq-h-style">
/* ── IMQ Unified Header ───────────────────────────────────────────────────── */
.imq-h{
  --imq-sans:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --imq-mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  --imq-line:#e5e7eb; --imq-line-soft:#eef0f3;
  --imq-ink:#0f172a; --imq-mute:#475569; --imq-soft:#94a3b8;
  --imq-blue:#3b82f6; --imq-up:#10b981;

  position:fixed; top:0; left:0; right:0; z-index:1000;
  background:rgba(255,255,255,.88);
  backdrop-filter:blur(14px) saturate(160%);
  -webkit-backdrop-filter:blur(14px) saturate(160%);
  border-bottom:1px solid transparent;
  transition:transform .4s cubic-bezier(.4,0,.2,1), border-color .25s;
  font-family:var(--imq-sans); color:var(--imq-ink);
  will-change:transform;
}
.imq-h *{box-sizing:border-box}
.imq-h[data-hidden="true"]{transform:translateY(-100%)}
.imq-h[data-scrolled="true"]{border-bottom-color:var(--imq-line)}

/* ── Top hairline rule ───────────────────────────────────────────────────── */
.imq-h__rule{
  height:14px; position:relative;
  border-bottom:1px solid var(--imq-line-soft);
  display:flex; align-items:flex-end; justify-content:space-between;
  padding:0 32px;
  font-family:var(--imq-mono); font-size:9px; color:#cbd5e1;
  letter-spacing:.16em; text-transform:uppercase; user-select:none;
}
.imq-h__rule::before{
  content:""; position:absolute; left:0; right:0; bottom:0; height:1px;
  background:repeating-linear-gradient(90deg,#e5e7eb 0,#e5e7eb 1px,transparent 1px,transparent 60px);
}
.imq-h__rule > span{background:rgba(255,255,255,.88); padding:0 6px 0 0; line-height:1}
.imq-h__rule > span:last-child{padding:0 0 0 6px}
.imq-h__rule b{color:var(--imq-ink); font-weight:600}

/* ── Main row ────────────────────────────────────────────────────────────── */
.imq-h__row{
  max-width:1280px; margin:0 auto; padding:18px 32px;
  display:grid; grid-template-columns:auto 1fr auto; align-items:center; gap:24px;
  transition:padding .3s;
}
.imq-h[data-scrolled="true"] .imq-h__row{padding:12px 32px}

/* ── Logo ────────────────────────────────────────────────────────────────── */
.imq-h__logo{
  font-family:var(--imq-sans); font-weight:700; font-size:18px;
  letter-spacing:-.025em; color:var(--imq-ink); text-decoration:none;
  display:inline-flex; align-items:baseline; transition:opacity .15s;
}
.imq-h__logo:hover{opacity:.7}
.imq-h__logo .dot{
  display:inline-block; width:6px; height:6px; border-radius:999px;
  background:var(--imq-blue); margin:0 8px 1px 1px; transform:translateY(-1px);
}
.imq-h__logo .sub{font-weight:300; color:#64748b; letter-spacing:0}

/* ── Search ──────────────────────────────────────────────────────────────── */
.imq-h__searchbox{
  display:flex; align-items:center; gap:10px;
  padding:9px 14px; border-radius:999px;
  border:1px solid var(--imq-line); background:#fafbfc;
  max-width:380px; width:100%; justify-self:center;
  transition:border-color .2s, background .2s;
}
.imq-h__searchbox:focus-within{border-color:var(--imq-ink); background:#fff}
.imq-h__searchbox svg{width:14px; height:14px; opacity:.55; flex:0 0 14px; color:#64748b}
.imq-h__searchbox input{
  flex:1; border:0; outline:none; background:transparent;
  font-family:var(--imq-sans); font-size:12.5px; color:var(--imq-ink); padding:0;
}
.imq-h__searchbox input::placeholder{color:#94a3b8}
.imq-h__searchbox kbd{
  font-family:var(--imq-mono); font-size:9.5px;
  padding:1.5px 5px; border-radius:4px;
  background:#fff; border:1px solid var(--imq-line); color:#94a3b8; line-height:1.2;
}

/* ── Right cluster ───────────────────────────────────────────────────────── */
.imq-h__right{display:flex; align-items:center; gap:14px; justify-self:end}

/* ── Nav pill ────────────────────────────────────────────────────────────── */
.imq-h__nav{
  position:relative; display:flex; align-items:center; flex-wrap:nowrap;
  padding:4px 6px; border-radius:999px;
  border:1px solid var(--imq-line); background:#fff;
}
.imq-h__ind{
  position:absolute; top:4px; bottom:4px;
  background:var(--imq-ink); border-radius:999px; z-index:0;
  transition:left .35s cubic-bezier(.5,.1,.25,1), width .35s cubic-bezier(.5,.1,.25,1), opacity .2s;
}
.imq-h__link{
  position:relative; z-index:1;
  padding:9px 18px; font-size:13px; font-weight:500;
  color:var(--imq-mute); text-decoration:none; cursor:pointer;
  border-radius:999px; transition:color .25s; user-select:none;
  white-space:nowrap;
}
.imq-h__link:hover{color:var(--imq-ink)}
.imq-h__link[data-active]{color:var(--imq-ink); font-weight:600}
/* White text only when sliding indicator is directly underneath */
.imq-h__link[data-lit="true"]{color:#fff}
.imq-h__link[data-lit="true"][data-active]{color:#fff}

/* ── Time ────────────────────────────────────────────────────────────────── */
.imq-h__time{
  font-family:var(--imq-mono); font-size:11px; color:#94a3b8;
  letter-spacing:.08em; text-transform:uppercase;
  display:flex; align-items:center; gap:8px;
}
.imq-h__time::before{
  content:""; width:5px; height:5px; border-radius:999px; background:var(--imq-up);
  box-shadow:0 0 0 3px rgba(16,185,129,.18);
  animation:imq-h-pulse 2.4s ease-in-out infinite;
}
@keyframes imq-h-pulse{
  0%,100%{box-shadow:0 0 0 0 rgba(16,185,129,.4)}
  50%    {box-shadow:0 0 0 6px rgba(16,185,129,0)}
}

/* ── Market Regime LED ───────────────────────────────────────────────────── */
.imq-h__regime{
  display:flex; align-items:center; gap:8px;
  padding:6px 11px 6px 9px; border-radius:999px;
  border:1px solid var(--imq-line); background:#fff;
  font-family:var(--imq-mono); font-size:10.5px;
  color:var(--imq-mute); letter-spacing:.04em; text-transform:uppercase;
  cursor:pointer; user-select:none; text-decoration:none;
  transition:border-color .15s, color .15s;
}
.imq-h__regime:hover{border-color:#cbd5e1; color:var(--imq-ink)}
.imq-h__regime__cells{display:inline-flex; gap:2px}
.imq-h__regime__cells i{
  display:block; width:7px; height:10px; border-radius:1.5px;
  background:var(--imq-line); transition:background .25s;
}
.imq-h__regime[data-state="1"] .imq-h__regime__cells i:nth-child(1){background:#3b82f6}
.imq-h__regime[data-state="2"] .imq-h__regime__cells i:nth-child(-n+2){background:#10b981}
.imq-h__regime[data-state="3"] .imq-h__regime__cells i:nth-child(-n+3){background:#10b981}
.imq-h__regime[data-state="4"] .imq-h__regime__cells i:nth-child(-n+4){background:#f59e0b}
.imq-h__regime[data-state="5"] .imq-h__regime__cells i:nth-child(-n+5){background:#ef4444}
.imq-h__regime[data-state="6"] .imq-h__regime__cells i{background:#ef4444}
.imq-h__regime b{font-weight:600; color:var(--imq-ink); letter-spacing:.02em}

/* ── Breadcrumb ──────────────────────────────────────────────────────────── */
.imq-h__crumb{
  max-width:1280px; margin:0 auto; padding:10px 32px 11px;
  display:flex; align-items:center; gap:8px;
  font-family:var(--imq-mono); font-size:11px; color:#94a3b8;
  letter-spacing:.02em;
  border-top:1px solid var(--imq-line-soft);
  overflow:hidden;
}
.imq-h__crumb:empty{display:none}
.imq-h__crumb a{color:#94a3b8; text-decoration:none; transition:color .15s; white-space:nowrap; flex:0 0 auto}
.imq-h__crumb a:hover{color:var(--imq-ink)}
.imq-h__crumb .sep{color:#cbd5e1; font-weight:400; flex:0 0 auto}
.imq-h__crumb .here{
  color:var(--imq-ink); font-weight:600;
  flex:1 1 auto; min-width:0;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width:1100px){
  .imq-h__regime b{display:none}
}
@media (max-width:920px){
  .imq-h__row{grid-template-columns:auto auto; gap:8px; padding:10px 16px}
  .imq-h[data-scrolled="true"] .imq-h__row{padding:8px 16px}
  .imq-h__searchbox{display:none}
  .imq-h__time{display:none}
  .imq-h__regime{display:none}
  .imq-h__rule{display:none}
  .imq-h__crumb{padding:0 16px 8px; font-size:10.5px}
  /* Nav: allow horizontal scroll on very small screens so all 5 links remain accessible */
  .imq-h__nav{padding:2px 3px; overflow-x:auto; scrollbar-width:none; -ms-overflow-style:none; max-width:calc(100vw - 200px)}
  .imq-h__nav::-webkit-scrollbar{display:none}
  .imq-h__link{padding:7px 11px; font-size:12px; white-space:nowrap}
}
@media (max-width:480px){
  .imq-h__row{gap:6px; padding:9px 12px}
  .imq-h__link{padding:6px 8px; font-size:11px}
  .imq-h__logo{font-size:15px}
  .imq-h__nav{max-width:calc(100vw - 175px)}
}

/* ── Body offset (header is fixed; push page content below) ─────────────── */
body{padding-top:var(--imq-h-height, 71px)}
@media (max-width:920px){body{padding-top:var(--imq-h-height-mobile, 43px)}}
@media (max-width:480px){body{padding-top:41px}}
</style>"""

# ---------------------------------------------------------------------------
# JS block
# ---------------------------------------------------------------------------

IMQ_H_JS = """\
<script id="imq-h-script">
(function(){
  var h   = document.getElementById('imqHeader');
  var nav = document.getElementById('imqHNav');
  var ind = nav.querySelector('.imq-h__ind');
  var lastY = window.scrollY, ticking = false;
  var links = nav.querySelectorAll('.imq-h__link');

  /* ── Sliding indicator ──────────────────────────────────────────────── */
  function placeIndicator(target){
    var el = target || nav.querySelector('.imq-h__link[data-active]');
    links.forEach(function(a){
      a.dataset.lit = (a === el) ? 'true' : 'false';
    });
    if (!el){ ind.style.opacity = '0'; return; }
    var navR  = nav.getBoundingClientRect();
    var linkR = el.getBoundingClientRect();
    ind.style.opacity = '1';
    ind.style.left    = (linkR.left - navR.left) + 'px';
    ind.style.width   = linkR.width + 'px';
  }
  links.forEach(function(a){
    a.addEventListener('mouseenter', function(){ placeIndicator(a); });
  });
  nav.addEventListener('mouseleave', function(){ placeIndicator(); });

  /* Initial position — wait for fonts so widths are accurate */
  if (document.fonts && document.fonts.ready){
    document.fonts.ready.then(function(){ placeIndicator(); });
  }
  setTimeout(placeIndicator, 80);
  window.addEventListener('resize', function(){ placeIndicator(); });

  /* ── Scroll: hide on down-scroll, reveal on up-scroll ──────────────── */
  function onScroll(){
    var y = window.scrollY;
    h.dataset.scrolled = y > 8 ? 'true' : 'false';
    if (y > 80 && y > lastY + 4)   h.dataset.hidden = 'true';
    else if (y < lastY - 4)        h.dataset.hidden = 'false';
    lastY = y;
    ticking = false;
  }
  window.addEventListener('scroll', function(){
    if (!ticking){ requestAnimationFrame(onScroll); ticking = true; }
  }, {passive:true});

  /* ── Live clock (TST = UTC+8) ───────────────────────────────────────── */
  var timeEl = document.getElementById('imqHTime');
  if (timeEl){
    function tick(){
      var d = new Date(new Date().getTime() + 8*3600000);  /* UTC → TST */
      var hh = String(d.getUTCHours()).padStart(2,'0');
      var mm = String(d.getUTCMinutes()).padStart(2,'0');
      timeEl.textContent = hh + ':' + mm + ' TST';
    }
    tick();
    setInterval(tick, 30000);  /* update every 30s */
  }

  /* ── ⌘K / Ctrl+K → focus search ───────────────────────────────────── */
  document.addEventListener('keydown', function(e){
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k'){
      e.preventDefault();
      var s = document.getElementById('imqHSearch');
      if (s) s.focus();
    }
  });
})();
</script>"""


# ---------------------------------------------------------------------------
# HTML builder
# ---------------------------------------------------------------------------

def _nav_links_html(section: str) -> str:
    parts = []
    for label, href, key in NAV_LINKS:
        active_attr = ' data-active' if key == section else ''
        parts.append(
            f'<a href="{href}" class="imq-h__link"{active_attr}>{label}</a>'
        )
    return "\n        ".join(parts)


def _breadcrumb_html(breadcrumb: list[dict] | None) -> str:
    if not breadcrumb:
        return '<nav class="imq-h__crumb" aria-label="Breadcrumb"></nav>'

    parts = []
    for i, item in enumerate(breadcrumb):
        is_last = i == len(breadcrumb) - 1
        if i > 0:
            parts.append('<span class="sep">/</span>')
        label = item.get("label", "")
        href = item.get("href")
        if is_last or not href:
            parts.append(f'<span class="here">{label}</span>')
        else:
            parts.append(f'<a href="{href}">{label}</a>')

    inner = "\n    ".join(parts)
    return f'<nav class="imq-h__crumb" aria-label="Breadcrumb">\n    {inner}\n  </nav>'


def build_imq_header(
    section: str = "",
    regime: int = DEFAULT_REGIME,
    updated_at: str = "",
    breadcrumb: list[dict] | None = None,
    google_fonts: bool = True,
) -> str:
    """
    Return the complete header HTML block: <style> + <header> + <script>.

    Args:
        section:    One of 'research', 'market', 'mental-models', 'tools', 'how-to', 'home', ''.
        regime:     Integer 1-6 for the market regime LED.
        updated_at: 'YYYY-MM-DD HH:MM TST' string for the top rule.
        breadcrumb: List of {label, href?} dicts. Empty/None → breadcrumb hidden.
        google_fonts: Whether to include a <link> for Google Fonts preconnect.
                      Set False if the page already loads fonts.
    """
    regime = max(1, min(6, int(regime)))
    rule_label = SECTION_LABELS.get(section, "RESEARCH")

    if not updated_at:
        updated_at = get_updated_at()

    fonts_html = ""
    if google_fonts:
        fonts_html = (
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800'
            '&family=IBM+Plex+Mono:wght@400;500;600;700'
            '&family=Noto+Sans+TC:wght@300;400;500;600;700&display=swap" rel="stylesheet">\n'
        )

    nav_html = _nav_links_html(section)
    crumb_html = _breadcrumb_html(breadcrumb)

    return f"""{fonts_html}{IMQ_H_CSS}

<!-- ═══════════ IMQ UNIFIED HEADER START ═══════════ -->
<header class="imq-h" id="imqHeader">
  <div class="imq-h__rule">
    <span><b>{rule_label}</b> · INVESTMQUEST</span>
    <span>UPDATED <b>{updated_at}</b></span>
  </div>

  <div class="imq-h__row">
    <a href="/" class="imq-h__logo">
      InvestMQuest<span class="dot"></span><span class="sub">Research</span>
    </a>

    <label class="imq-h__searchbox">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input type="text" placeholder="搜尋個股、報告、主題…" id="imqHSearch" />
      <kbd>⌘K</kbd>
    </label>

    <div class="imq-h__right">
      <nav class="imq-h__nav" id="imqHNav">
        <span class="imq-h__ind"></span>
        {nav_html}
      </nav>
      <a href="{BASE}/market/regime/"
         class="imq-h__regime" data-state="{regime}" id="imqHRegime"
         title="市場狀態機 / Market Regime">
        <span class="imq-h__regime__cells"><i></i><i></i><i></i><i></i><i></i><i></i></span>
        <b>R{regime}</b>
      </a>
      <div class="imq-h__time" id="imqHTime"></div>
    </div>
  </div>

  {crumb_html}
</header>
{IMQ_H_JS}
<!-- ═══════════ IMQ UNIFIED HEADER END ═══════════ -->"""
