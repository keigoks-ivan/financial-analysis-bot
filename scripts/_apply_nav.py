#!/usr/bin/env python3
"""Apply unified nav to all top-level landing pages.

Strategy:
- Find existing <header>...</header> block (or first dark nav bar for inline-styled pages)
- Replace with unified nav with correct active markers for the page.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs"

NAV_STYLE = """<style>
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
.imq-dd-menu{display:none;position:absolute;top:calc(100% + 6px);left:0;background:#1e293b;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{display:block}
.imq-dd-menu a{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}
.imq-dd-menu a:hover{color:#fff !important;background:rgba(59,130,246,.18)}
.imq-dd-menu a.active{color:#fff !important;background:rgba(59,130,246,.22);font-weight:600}
.imq-caret{font-size:.6rem;opacity:.7;margin-top:1px}
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


def build_nav(active):
    """active is a dict: {group: 'home'|'research'|'market'|'quant'|'howto'|None, item: '...' }"""
    group = active.get("group")
    item = active.get("item")

    def cls(name):
        return ' class="active"' if item == name else ""

    def grp_cls(name):
        return " active" if group == name else ""

    home_cls = ' class="active"' if group == "home" else ""
    howto_cls = ' class="active"' if group == "howto" else ""

    return f"""<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/"{home_cls}>首頁</a>
      <div class="imq-dd{grp_cls("research")}">
        <button type="button" class="imq-dd-btn">研究<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/research/"{cls("dd")}>個股 DD</a>
          <a href="/pm/"{cls("pm")}>PM 複盤</a>
          <a href="/id/"{cls("id")}>產業深度 ID</a>
          <a href="/id/theses.html"{cls("theses")}>⭐ 九大非共識</a>
          <a href="/id/tier_matrix.html"{cls("tier")}>🎯 Tier Matrix</a>
        </div>
      </div>
      <div class="imq-dd{grp_cls("market")}">
        <button type="button" class="imq-dd-btn">市場<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/briefing/"{cls("brief")}>每日簡報</a>
          <a href="/weekly/"{cls("week")}>週報</a>
          <a href="/earnings/"{cls("earn")}>財報分析</a>
          <a href="/markets.html"{cls("markets")}>Markets</a>
          <a href="/sectors.html"{cls("sectors")}>Sectors</a>
          <a href="/six-state/"{cls("six")}>六狀態機</a>
        </div>
      </div>
      <div class="imq-dd{grp_cls("quant")}">
        <button type="button" class="imq-dd-btn">工具<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/backtest/"{cls("bt")}>量化回測</a>
          <a href="/qgm/"{cls("qus")}>QGM 美股</a>
          <a href="/qgm-tw/"{cls("qtw")}>QGM 台股</a>
        </div>
      </div>
      <a href="/how-to.html"{howto_cls}>📘 使用說明</a>
    </nav>
  </div>
</header>"""


def full_nav_block(active):
    return NAV_STYLE + "\n" + build_nav(active) + "\n" + NAV_SCRIPT


# Pages with <header>...</header> CSS-class structure
PAGES_HEADER_STYLE = {
    "id/theses.html": {"group": "research", "item": "theses"},
    "how-to.html": {"group": "howto"},
    "six-state/index.html": {"group": "market", "item": "six"},
    "backtest/index.html": {"group": "quant", "item": "bt"},
    "qgm/latest.html": {"group": "quant", "item": "qus"},
    "qgm-tw/latest.html": {"group": "quant", "item": "qtw"},
    "404.html": {},
}

# Pattern to match <header>...</header> blocks (first one only)
HEADER_RE = re.compile(r"<header>.*?</header>", re.DOTALL)


def apply_to_header_style_page(relpath, active):
    p = ROOT / relpath
    text = p.read_text(encoding="utf-8")
    new_block = full_nav_block(active)
    new_text, n = HEADER_RE.subn(new_block, text, count=1)
    if n == 0:
        print(f"  ❌ no <header> match in {relpath}")
        return False
    p.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {relpath}")
    return True


# Pages with inline-style top dark bar (briefing / weekly and sub-pages)
# Pattern: <div style="background:linear-gradient(135deg,#0f172a,#1e293b)...">...</div>
INLINE_BAR_RE = re.compile(
    r'<div style="background:linear-gradient\(135deg,#0f172a,#1e293b\)[^"]*"[^>]*>.*?</div>',
    re.DOTALL,
)


def apply_to_inline_bar_page(relpath, active):
    p = ROOT / relpath
    text = p.read_text(encoding="utf-8")
    new_block = full_nav_block(active)
    new_text, n = INLINE_BAR_RE.subn(new_block, text, count=1)
    if n == 0:
        print(f"  ❌ no inline bar match in {relpath}")
        return False
    p.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {relpath}")
    return True


def main():
    print("Applying unified nav to CSS-class pages...")
    for relpath, active in PAGES_HEADER_STYLE.items():
        apply_to_header_style_page(relpath, active)

    print("\nApplying to /briefing/ pages (inline-bar style)...")
    briefing_pages = sorted((ROOT / "briefing").glob("*.html"))
    for p in briefing_pages:
        apply_to_inline_bar_page(
            str(p.relative_to(ROOT)), {"group": "market", "item": "brief"}
        )

    print("\nApplying to /weekly/ page(s) (inline-bar style)...")
    for p in sorted((ROOT / "weekly").glob("*.html")):
        apply_to_inline_bar_page(
            str(p.relative_to(ROOT)), {"group": "market", "item": "week"}
        )

    # PM page has NO existing nav — inject after <body>
    print("\nInjecting nav into /pm/index.html (no existing nav)...")
    p = ROOT / "pm/index.html"
    text = p.read_text(encoding="utf-8")
    active = {"group": "research", "item": "pm"}
    new_block = full_nav_block(active)
    # Remove the first h1 "🏛 PM 週度複盤" from inside container since nav duplicates breadcrumb
    if "<body>" in text and ".imq-nav-root" not in text:
        new_text = text.replace("<body>", "<body>\n" + new_block, 1)
        p.write_text(new_text, encoding="utf-8")
        print("  ✅ pm/index.html")
    else:
        print("  ⚠️  pm/index.html already has nav or unexpected structure")


if __name__ == "__main__":
    main()
