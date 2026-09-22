#!/usr/bin/env python3
"""Assemble docs/stock-dash/index.html (production, fetch-based) from the
page fragments in this folder. Also writes docs/stock-dash/full.html as a
redirect stub, and a self-contained preview for one ticker.

2026-09-22: fragments moved here from a session scratchpad so they survive.
Preview data now comes from docs/stock-dash/data/ instead of stale copies.

Usage:
  python3 scripts/stock_dash_page/assemble_prod.py [--ticker NVDA] [--preview-out PATH]
"""
import argparse
from pathlib import Path

SCRATCH = Path(__file__).parent          # fragment folder (name kept for the code below)
REPO = SCRATCH.parent.parent


def read(name):
    return (SCRATCH / name).read_text(encoding="utf-8")


root_tokens = read("_idx_root_tokens.txt").replace("本頁 full.html 專用", "本頁 index.html 專用")
idx_css = read("_idx_css.txt")
idx_body = read("_idx_body.txt")
idx_js = read("_idx_js.txt")
shared_js = read("_shared_js2.txt")
chart_builders = read("_chart_builders2.txt")
appendix_js = read("_appendix_js2.txt")
moat_js = read("_idx_moat_js.txt")

HEAD_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/imq-base.css">"""

SCRIPT_TAGS = """<script src="https://cdn.jsdelivr.net/npm/lightweight-charts@4.2.3/dist/lightweight-charts.standalone.production.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>"""


def build_index_html():
    html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>個股儀表板 — InvestMQuest Research</title>
<meta name="description" content="個股儀表板：券商研究報告式版面，投資摘要、獲利預估、估值、財報驚喜、護城河與報酬持續期（DD 基準＋機械追蹤）、價格與技術、風險、大盤，全部機械計算，判斷層只在觸發時改版。">
<meta name="robots" content="noindex">
{HEAD_LINKS}
<style>
{root_tokens}
{idx_css}
</style>
</head>
<body>
{idx_body}
{SCRIPT_TAGS}
<script>
(function(){{
{shared_js}
{chart_builders}
{appendix_js}
{moat_js}
{idx_js}
}})();
</script>
</body>
</html>
"""
    out_path = REPO / "docs" / "stock-dash" / "index.html"
    out_path.write_text(html, encoding="utf-8")
    # site nav: inject into this one file only (scripts/site_nav.py with no args sweeps all of docs/)
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    import site_nav
    site_nav.process(out_path.resolve())
    print("wrote", out_path, len(html), "chars (+ site nav)")
    return html


FULL_REDIRECT = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0; url=index.html">
<link rel="canonical" href="index.html">
<title>個股儀表板 — InvestMQuest Research</title>
<meta name="robots" content="noindex">
<script>
(function(){
  var params = new URLSearchParams(location.search);
  var t = params.get('t');
  location.replace('index.html' + (t ? ('?t=' + encodeURIComponent(t)) : ''));
})();
</script>
</head>
<body>
<p>這一頁已經併入 <a href="index.html">個股儀表板</a>，正在自動跳轉…</p>
</body>
</html>
"""


def build_full_redirect():
    out_path = REPO / "docs" / "stock-dash" / "full.html"
    out_path.write_text(FULL_REDIRECT, encoding="utf-8")
    print("wrote", out_path, len(FULL_REDIRECT), "chars (redirect stub)")


def build_preview(index_html):
    """Self-contained variant: swap fetch() bootstrap for embedded consts."""
    data_json = Path(DATA_PATH or (REPO / "docs" / "stock-dash" / "data" / f"{TICKER}.json")).read_text(encoding="utf-8")
    market_json = (REPO / "docs" / "stock-dash" / "data" / "_market.json").read_text(encoding="utf-8")

    # Remove the <link rel="stylesheet" href="/assets/imq-base.css"> and inline
    # its content instead, since preview must be file://-openable standalone.
    base_css = (REPO / "docs" / "assets" / "imq-base.css").read_text(encoding="utf-8")
    html = index_html.replace(
        '<link rel="stylesheet" href="/assets/imq-base.css">',
        f"<style>\n{base_css}\n</style>",
    )

    # Replace the fetch-based bootstrap block with embedded consts + direct render() call.
    old_bootstrap_marker = "var params = new URLSearchParams(location.search);"
    idx = html.index(old_bootstrap_marker)
    end_idx = html.index("})();", idx)
    new_bootstrap = f"render(DATA, MARKET);\n"
    html = html[:idx] + new_bootstrap + html[end_idx:]

    # Inject DATA/MARKET consts right before the big inline <script> IIFE.
    inject_point = html.index(SCRIPT_TAGS) + len(SCRIPT_TAGS)
    consts = f"\n<script>const DATA = {data_json};</script>\n<script>const MARKET = {market_json};</script>\n"
    html = html[:inject_point] + consts + html[inject_point:]

    html = html.replace(
        "<title>個股儀表板 — InvestMQuest Research</title>",
        f"<title>{TICKER} 個股儀表板（自含預覽）— InvestMQuest Research</title>",
    )
    # Preview doesn't need the ticker switch (fixed to NVDA) but leaving it is harmless
    # since DATA is fixed regardless of what's typed; note this in a comment instead.

    out_path = PREVIEW_OUT
    out_path.write_text(html, encoding="utf-8")
    print("wrote", out_path, len(html), "chars (self-contained preview)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default="NVDA")
    ap.add_argument("--preview-out", default=None, help="default: /tmp/stock_dash_preview_<T>.html")
    ap.add_argument("--data", default=None, help="preview only: use this {T}.json instead of docs/stock-dash/data/<T>.json")
    ap.add_argument("--preview-only", action="store_true", help="write only the preview; leave docs/stock-dash/ untouched")
    a = ap.parse_args()
    DATA_PATH = a.data
    TICKER = a.ticker
    PREVIEW_OUT = Path(a.preview_out or f"/tmp/stock_dash_preview_{TICKER}.html")
    if a.preview_only:
        _real = REPO / "docs" / "stock-dash" / "index.html"
        _keep = _real.read_bytes()
        html = build_index_html()
        _real.write_bytes(_keep)  # restore: preview-only must not change the real page
    else:
        html = build_index_html()
        build_full_redirect()
    build_preview(html)
