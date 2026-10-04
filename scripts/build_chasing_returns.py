#!/usr/bin/env python3
"""Publish 漲多了還能追嗎 to /backtest/chasing_returns/.

Source of truth is the research pipeline in
notes/site-internal/research/chasing_returns_20261004/ (run_all.sh there rebuilds
every result, then page_merged.py assembles merged.html from the section templates in
merged/ and the data fragments). This script only wraps merged.html in the site shell
(site nav, .page-hdr with crumb, /backtest/ pill bar, footer) -- same skeleton as
scripts/build_first_cut.py -- and writes a redirect stub for the retired
followups.html (old 七個追問 page).

    python3 scripts/build_chasing_returns.py [--merged FILE] [--out-dir DIR]

Writes:
    docs/backtest/chasing_returns/index.html
    docs/backtest/chasing_returns/followups.html   (redirect stub)
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "notes/site-internal/research/chasing_returns_20261004"
NAV_DIR = ROOT / "docs/backtest"

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(NAV_DIR))
from site_nav import full_nav_block  # noqa: E402
from _nav_common import make_toggle  # noqa: E402

KEY = "chasing_returns"
URL = "https://research.investmquest.com/backtest/chasing_returns/"
TITLE = "漲多了還能追嗎"
CRUMB = "漲多了還能追嗎"
SUB = "美股、產業、避險基金與台股的追高回測，資料截至 2026 年 9 月"
DESC = ("用 1871 年起的美股、1926 年起的美國產業組合、18 國長期報酬、標普類股 ETF、兩套避險基金指數與台股，"
        "回測漲多了還能不能追：連續高報酬之後的表現、熱或冷的起點對 5–20 年投資的影響、"
        "每年換到最強類股、追逐最佳避險基金策略，並用沒參與設計的後半段資料再驗證一次。")

# old followups.html anchors -> new page anchors ('' = top of page)
FOLLOWUPS_MAP = {
    "f1": "q1-h", "f2": "q2-i", "f3": "q1-i", "f4": "q3-j", "f5": "q1-j",
    "f6": "oos", "f7": "tw", "pos": "now", "update": "", "method": "method",
}


def parts(merged: str) -> tuple[str, str, str]:
    """(css, body, scripts) out of merged.html."""
    css = re.search(r'<style id="chasing-merged-css">.*?</style>', merged, re.S)
    body = re.search(r"<!-- BODY START -->(.*?)<!-- BODY END -->", merged, re.S)
    if not css or not body:
        raise SystemExit("merged.html: style block or BODY START/END markers missing; rebuild with page_merged.py")
    scripts = merged[body.end():]
    scripts = "".join(re.findall(r"<script>.*?</script>", scripts, re.S))
    return css.group(0), body.group(1).strip(), scripts


def build_index(merged_path: Path, out_dir: Path) -> Path:
    css, body, scripts = parts(merged_path.read_text(encoding="utf-8"))
    built = datetime.now().strftime("%Y-%m-%d")
    title = f"{TITLE} | InvestMQuest Research"
    out = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(DESC)}">
<link rel="canonical" href="{URL}">
{css}
</head>
<body>
{full_nav_block("system", "bt")}

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / {html.escape(CRUMB)}</div>
    <h1>{html.escape(TITLE)}</h1>
    <div class="sub">{html.escape(SUB)}・生成 {built}</div>
    {make_toggle(KEY)}
  </div>
</div>

<div class="container">

{body}

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; {html.escape(TITLE)}（研究頁，不構成投資建議）
    &middot; 頁面生成 {built} &middot; 僅供研究參考，不構成投資建議
  </div>
</footer>
{scripts}
</body>
</html>
"""
    if re.search(r"claude\.ai/artifact", out):
        raise SystemExit("unmapped Artifact link left in page")
    dest = out_dir / "index.html"
    dest.write_text(out, encoding="utf-8")
    return dest


def build_stub(out_dir: Path) -> Path:
    mapping = ",".join(f'"{k}":"{v}"' for k, v in FOLLOWUPS_MAP.items())
    out = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}（已併入新頁） | InvestMQuest Research</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{URL}">
<noscript><meta http-equiv="refresh" content="0; url=/backtest/chasing_returns/"></noscript>
<script>
(function(){{
  var m={{{mapping}}};
  var h=(location.hash||'').slice(1);
  var to='/backtest/chasing_returns/'+(h in m?(m[h]?'#'+m[h]:''):'');
  location.replace(to);
}})();
</script>
</head>
<body>
<p>這一頁已併入 <a href="/backtest/chasing_returns/">{TITLE}</a>。</p>
</body>
</html>
"""
    dest = out_dir / "followups.html"
    dest.write_text(out, encoding="utf-8")
    return dest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged", default=str(SRC / "merged.html"))
    ap.add_argument("--out-dir", default=str(ROOT / "docs/backtest/chasing_returns"))
    a = ap.parse_args()
    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in (build_index(Path(a.merged), out_dir), build_stub(out_dir)):
        print(f"wrote {p} ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
