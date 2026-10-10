#!/usr/bin/env python3
"""docs/stages/tw/index.html — 個股階段雷達（台股）(2026-10-10).

Derived from the US page (docs/stages/index.html) on every run, the same way
build_dd_screener_tw_page.py derives the TW pool page, so the chart, tables and
definitions stay in step with the US page. What changes:

  * data: ../data/latest_tw.json and ../data/history_tw.json
    (scripts/build_stages_tw.py) instead of ./data/latest.json / history.json;
  * text that is US-bound: title, hero, benchmark (QQQ/SPY → 0050), the
    liquidity floor (US$20M → US$5M in TWD), the universe paragraph and the
    cross links; a 美股／台股 switch goes above the title;
  * the 品質×時機 matrix and the per-ticker badges are dropped: imq-badge.js
    reads US-only files (arena, universe_board, lamp.json);
  * the list shows the Chinese name next to the code and the 20-day traded
    value in NT$ 億.

Universe size and the TWD floor come from latest_tw.json at generation time,
so the workflow reruns this after build_stages_tw.py. If an anchor in the US
page moves, the script exits 1 and leaves the old tw/index.html in place.

Usage:
  python3 scripts/build_stages_tw_page.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
US_PAGE = ROOT / "docs" / "stages" / "index.html"
LATEST_TW = ROOT / "docs" / "stages" / "data" / "latest_tw.json"
OUT = ROOT / "docs" / "stages" / "tw" / "index.html"

SWITCH_CSS = (".mkt-switch{display:inline-flex;border:1px solid var(--line);border-radius:6px;"
              "overflow:hidden;font-size:.76rem;font-weight:600;margin:0 0 .8rem}\n"
              ".mkt-switch a,.mkt-switch span{padding:.22rem .75rem;text-decoration:none}\n"
              ".mkt-switch a{color:var(--sec)}\n"
              ".mkt-switch .on{background:var(--accent);color:#fff}\n")
# same names as build_stages.STAGE_NAMES (test checks they match)
STAGE_ZH = {"S0": "弱勢", "S1": "轉強", "S2": "築底", "S5": "高檔整理", "S3": "收縮完成", "S4": "領先"}


def facts() -> dict:
    d = json.loads(LATEST_TW.read_text(encoding="utf-8"))
    u = d.get("universe") or {}
    fx = d.get("twd_per_usd")
    floor = d.get("adv_min_usd") or 5_000_000
    low = [STAGE_ZH.get(r.get("from"), r.get("from"))
           for r in (d.get("transitions") or {}).get("rows", []) if r.get("low_sample")]
    return {"n": u.get("total"), "radar": u.get("radar"), "pool": u.get("pool"),
            "floor_usd_wan": floor / 1e4,
            "floor_twd_yi": (floor * fx / 1e8) if fx else None, "fx": fx, "low": low,
            "win": (d.get("params") or {}).get("window_days") or 250}


def hero_html(f: dict) -> str:
    floor_twd = f"，約新台幣 {f['floor_twd_yi']:.1f} 億元" if f["floor_twd_yi"] else ""
    low = f"（目前是{'、'.join(f['low'])}）" if f.get("low") else ""
    return (
        '<div class="mkt-switch" role="navigation" aria-label="市場切換">'
        '<a href="/stages/">美股</a><span class="on">台股</span></div>\n'
        "    <h1>個股階段雷達（台股）</h1>\n"
        f"    <p>階段的定義跟美股版相同：弱勢、轉強、築底、高檔整理、收縮完成、領先。這頁把台股 {f['n']} 檔"
        "每天各放進一段，母體是 0050、0051、006201 的成分股加上台股池。名單只回答「看誰」。</p>\n"
        "    <p style=\"margin-top:.6rem\">跟美股版不同的地方有三個。比較大盤時用 0050 還原權息，不用 QQQ。"
        f"流動性門檻是近 20 日平均成交值 {f['floor_usd_wan']:,.0f} 萬美元{floor_twd}，美股是 2,000 萬美元。"
        f"母體只有 {f['n']} 檔，少見的段一年內的進場事件不到 20 筆{low}，"
        "轉場基率表上標「樣本不足」的列只能看方向。</p>"
    )


def universe_html(f: dict) -> str:
    fx = f" {f['fx']:.2f} " if f["fx"] else ""
    return (
        f"<p><b>母體</b>：0050、0051、006201 的成分股（{f['radar']} 檔），加上台股池（{f['pool']} 檔），"
        f"去重後 {f['n']} 檔。成分股名單在 <code>scripts/screener_tw.py</code>，成分股調整後要手動更新。"
        f"兩年的台股交易日只有約 480 天，前 252 天要用來累積資料，所以轉場基率只回算 {f.get('win', 250)} 個交易日，"
        "美股是 250 個。"
        f"流動性門檻用最新一天的新台幣匯率{fx}換算，過去 {f.get('win', 250)} 個交易日也用同一個匯率，"
        "接近門檻的名字在較早的日期可能被歸到過渡。</p>"
    )


CROSSLINKS = ('<p class="crosslinks">相關頁面：<a href="/cockpit-tw/">台股主控台</a>（核心席與台股池）'
              ' · <a href="/screener-tw.html">台股 RS 雷達</a>（相對強弱與波動收縮掃描）'
              ' · <a href="/stages/">美股版</a></p>')

TW_SAMPLE_NOTE = ('<p class="explain-p">台股母體小，少見的段一年內的進場事件可能不到 20 筆。'
                  '標「樣本不足」的列，百分比差幾個點不代表真的有差。</p>')

FMT_TWD = '''  function fmtTwd(v) {
    if (v === null || v === undefined || typeof v !== "number" || isNaN(v)) return "—";
    return (v / 1e8).toFixed(v >= 1e10 ? 0 : 1) + " 億";
  }

  function statTile(k, v) {'''

TICKER_CELL_US = '''    var tickerCell = (r.hub ? '<a href="' + esc(r.hub) + '">' + esc(r.ticker) + "</a>" : esc(r.ticker)) +
      (window.IMQBadge ? " " + window.IMQBadge.tag(r.ticker) : "");'''
TICKER_CELL_TW = '''    var code = String(r.ticker).split(".")[0];
    var tickerCell = (r.hub ? '<a href="' + esc(r.hub) + '">' + esc(code) + "</a>" : esc(code)) +
      (r.name ? " " + esc(r.name) : "");'''


def patches(f: dict) -> list[tuple[str, str]]:
    floor_twd = f"、約新台幣 {f['floor_twd_yi']:.1f} 億元" if f["floor_twd_yi"] else ""
    win = f.get("win", 250)
    return [
        ("<h2>轉場基率：過去 250 個交易日，", f"<h2>轉場基率：過去 {win} 個交易日，"),
        ("對過去 250 個交易日內每一次「進入某段」事件", f"對過去 {win} 個交易日內每一次「進入某段」事件"),
        ("<title>個股階段雷達（美股） | InvestMQuest Research</title>",
         "<title>個股階段雷達（台股） | InvestMQuest Research</title>"),
        ('<link rel="stylesheet" href="/assets/imq-badge.css">\n<script src="/assets/imq-badge.js"></script>\n', ""),
        (".crosslinks a{color:var(--accent);font-weight:600}\n</style>",
         ".crosslinks a{color:var(--accent);font-weight:600}\n" + SWITCH_CSS + "</style>"),
        ('<i style="background:var(--muted)"></i>QQQ（右軸）', '<i style="background:var(--muted)"></i>0050（右軸）'),
        ('  <div class="sec">\n    <div id="qt-matrix-mount"></div>\n  </div>\n\n', ""),
        ('<p class="explain-p">第 60 個交易日所在的階段，以及期間到過的最高階段；過去 250 個交易日回算，描述現況不預測。</p>',
         f'<p class="explain-p">第 60 個交易日所在的階段，以及期間到過的最高階段；過去 {win} 個交易日回算，描述現況不預測。</p>\n    '
         + TW_SAMPLE_NOTE),
        ("<th>代號</th><th>在此階段天數</th>", "<th>代號／名稱</th><th>在此階段天數</th>"),
        ('<th title="近 20 日日均成交金額（美元）">日均成交金額</th>',
         '<th title="近 20 日日均成交值（新台幣）">日均成交值</th>'),
        ("相對大盤（QQQ）近 63 個交易日", "相對大盤（0050 還原權息）近 63 個交易日"),
        ("（近 20 日均成交金額低於 2,000 萬美元、股價低於 5 美元，或交易天數不足）",
         f"（近 20 日均成交值低於 {f['floor_usd_wan']:,.0f} 萬美元{floor_twd}、股價低於 5 元，或交易天數不足）"),
        ("現價／SPY 這條相對強度線", "現價／0050 這條相對強度線"),
        ('fetchJSON("./data/latest.json"), fetchJSON("./data/history.json")',
         'fetchJSON("../data/latest_tw.json"), fetchJSON("../data/history_tw.json")'),
        ('lines.push("QQQ " + (p.qqq', 'lines.push("0050 " + (p.qqq'),
        (TICKER_CELL_US, TICKER_CELL_TW),
        ("  function statTile(k, v) {", FMT_TWD),
        ("'<td class=\"num\">' + fmtUsd(r.adv20_usd) + \"</td>\" +",
         "'<td class=\"num\">' + fmtTwd(r.adv20_twd) + \"</td>\" +"),
        ("    if (window.IMQBadge) window.IMQBadge.decorateAll(tbody);\n", ""),
        ('    if (window.IMQBadge) window.IMQBadge.mountMatrix("qt-matrix-mount", { universe: "all" });\n', ""),
    ]


DESC_RE = re.compile(r'<meta name="description" content="[^"]*">')
HERO_RE = re.compile(r"<h1>個股階段雷達（美股）</h1>\s*<p>.*?</p>", re.S)
UNIVERSE_RE = re.compile(r"<p><b>母體</b>：.*?</p>", re.S)
CROSSLINKS_RE = re.compile(r'<p class="crosslinks">.*?</p>', re.S)


def render(us_html: str, f: dict) -> tuple[str | None, list[str]]:
    """Returns (page, problems). page is None when any anchor is missing."""
    problems = []
    html = us_html
    desc = (f'<meta name="description" content="台股 {f["n"]} 檔的技術結構生命週期定位：弱勢、轉強、築底、'
            f'高檔整理、收縮完成、領先，附每天各段家數與過去 {f.get("win", 250)} 個交易日轉場基率。比較基準是 0050。">')
    for rx, rep, label in ((DESC_RE, desc, "description"), (HERO_RE, hero_html(f), "hero"),
                           (UNIVERSE_RE, universe_html(f), "universe"), (CROSSLINKS_RE, CROSSLINKS, "crosslinks")):
        html, n = rx.subn(lambda _m, rep=rep: rep, html, count=1)
        if n != 1:
            problems.append(label)
    for old, new in patches(f):
        got = html.count(old)
        if got != 1:
            problems.append(f"{old[:40]!r} x{got}")
            continue
        html = html.replace(old, new)
    rest = html.replace(hero_html(f), "")   # the TW hero names QQQ on purpose
    for leftover in ("QQQ", "SPY", "IMQBadge", "./data/latest.json"):
        if leftover in rest:
            problems.append(f"leftover {leftover}")
    return (None if problems else html), problems


def main() -> int:
    if not LATEST_TW.exists():
        print(f"ERROR: {LATEST_TW} missing — run build_stages_tw.py first", file=sys.stderr)
        return 1
    page, problems = render(US_PAGE.read_text(encoding="utf-8"), facts())
    if page is None:
        print(f"ERROR: US page anchors moved ({'; '.join(problems)}); {OUT} left unchanged",
              file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    sys.path.insert(0, str(ROOT / "scripts"))
    import site_nav  # noqa: E402
    status = site_nav.process(OUT)
    print(f"wrote {OUT} ({len(page):,} bytes, nav {status})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
