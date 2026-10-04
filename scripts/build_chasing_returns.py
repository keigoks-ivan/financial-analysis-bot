#!/usr/bin/env python3
"""Publish the 追漲四問 backtest pages to /backtest/chasing_returns/.

Source of truth is the research pipeline in
notes/site-internal/research/chasing_returns_20261004/ (run_all.sh there
rebuilds chasing.html and followups.html from public data). This script only
wraps those two pages in the site shell — site header, /backtest/ pill bar,
breadcrumb, full HTML skeleton — and rewrites the cross-links that point at
the private Artifact copies so they point at the site instead.

    python3 scripts/build_chasing_returns.py

Writes:
    docs/backtest/chasing_returns/index.html      (主報告：四題)
    docs/backtest/chasing_returns/followups.html  (續篇：七個追問)
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "notes/site-internal/research/chasing_returns_20261004"
OUT_DIR = ROOT / "docs/backtest/chasing_returns"
NAV_DIR = ROOT / "docs/backtest"

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(NAV_DIR))
from site_nav import full_nav_block  # noqa: E402
from _nav_common import make_toggle  # noqa: E402

MAIN_URL = "/backtest/chasing_returns/"
FOLLOW_URL = "/backtest/chasing_returns/followups.html"
LINK_MAP = {
    "https://claude.ai/artifact/BB2ajiy5edyV4dHsAHnpQt": MAIN_URL,
    "https://claude.ai/artifact/36p9Uiz9WRhATeypLy2QhN": FOLLOW_URL,
}

PAGES = [
    dict(src="chasing.html", out="index.html", key="chasing_returns",
         title="追漲四問：追逐過去的高報酬有沒有用",
         crumb="追漲四問",
         desc=("用 1871 年起的美股、1926 年起的美國產業組合、18 國長期報酬、標普類股 ETF 與兩套避險基金指數，"
               "回測四個問題：連續高報酬之後大盤表現如何、熱或冷的起點對 5–20 年投資的影響、每年換到最強類股、"
               "追逐最佳避險基金策略。每題 6–9 個面向，並分開比較現代時期與長期平均。")),
    dict(src="followups.html", out="followups.html", key="chasing_returns_f",
         title="追漲四問續篇：七個追問",
         crumb="追漲四問續篇",
         desc=("追漲四問的七個追問：近三年漲幅來自盈餘還是本益比、高 CAPE 有多少是結構性的、漲勢寬度、"
               "長期領先類股何時結束、熱且貴訊號太早的代價、樣本外檢驗，以及台股是否適用。")),
]

# The Artifact pages follow the viewer's dark mode; the rest of /backtest/ is
# light-only, so the site copy drops the dark-theme overrides.
DARK_BLOCKS = [
    re.compile(r'@media \(prefers-color-scheme: dark\)\{:root:not\(\[data-theme="light"\]\)\{[^}]*\}\}'),
    re.compile(r':root\[data-theme="dark"\]\{[^}]*\}'),
]

SHELL_STYLE = """<style id="chasing-shell">
.bt-shell{max-width:1120px;margin:0 auto;padding:1rem 20px 0}
.bt-shell .crumb{font-size:.82rem;color:#6b7280}
.bt-shell .crumb a{color:#6b7280;text-decoration:none}
.bt-shell .crumb a:hover{text-decoration:underline}
</style>"""


def build(page: dict) -> Path:
    src = (SRC / page["src"]).read_text(encoding="utf-8")
    # 1. pull the Artifact page apart: <title>, <link>/<style> head material, body markup
    head_end = src.index('<div class="page">')
    head_part, body_part = src[:head_end], src[head_end:]
    head_part = re.sub(r"<title>.*?</title>\s*", "", head_part, flags=re.S)
    for rx in DARK_BLOCKS:
        head_part = rx.sub("", head_part)
    # the page's own `header{...}` rule would also hit the site's <header class="imq-nav-root">
    head_part = head_part.replace("header{display:grid;gap:14px}", ".page>header{display:grid;gap:14px}")
    if ".page>header{display:grid" not in head_part:
        raise SystemExit(f"{page['src']}: expected header rule not found; check the CSS before publishing")
    for old, new in LINK_MAP.items():
        body_part = body_part.replace(old, new)
    if "claude.ai/artifact" in body_part:
        raise SystemExit(f"{page['src']}: unmapped Artifact link left in page body")

    title = f"{page['title']} | InvestMQuest Research"
    shell = (f'<div class="bt-shell">\n'
             f'  <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / {html.escape(page["crumb"])}</div>\n'
             f'  {make_toggle(page["key"])}\n'
             f'</div>\n')
    out = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(page['desc'])}">
{head_part.strip()}
{SHELL_STYLE}
</head>
<body>
{full_nav_block("system", "bt")}
{shell}
{body_part.strip()}
</body>
</html>
"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / page["out"]
    path.write_text(out, encoding="utf-8")
    return path


def main() -> None:
    for page in PAGES:
        p = build(page)
        print(f"Written {p.relative_to(ROOT)} ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
