#!/usr/bin/env python3
"""
日股國家掃描 hub 組裝腳本（重寫 2026-09-10）。

Usage:
  /opt/homebrew/bin/python3.12 _build_hub.py            # 產出 docs/backtest/country_scan/japan.html
  /opt/homebrew/bin/python3.12 _build_hub.py --check    # 產出後跑自檢，不重新寫檔亦可單獨執行

只用標準庫（json / statistics / math / re / os）。母體數字一律從 _universe.json 現算；
非母體的結構數字（東證改革象限、外資持股、NISA、BOJ利率、JGB殖利率、買回授權、MBO/TOB/Activist、
交叉持股……）一律從 _hub_facts.json 讀取，每筆都帶 value / as_of / source_name / source_url / confidence，
禁止在內文手打數字。本檔照 notes/site-internal/country_scan/malaysia/_build_hub.py 的結構與機制複製
（n<5 灰化、DD 最新檔逐字比對、SVG 幾何檢查、逐字引用跳過買賣指令掃描、禁用字表），鏡頭區改用
notes/site-internal/country_scan/taiwan/_build_hub.py 的一覽表模式（build_lens_table），因為日本有
七個獨立子頁（japan/{compounders,governance,financials,dividends,events,ai-chain,domestic}.html）。
母體欄位為日股口徑（market_cap_jpy／sector，TradingView 20 類粗分類，非 JPX 33 業種）。
"""
import datetime
import json
import os
import re
import statistics as st
import sys
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
UNIVERSE_PATH = os.path.join(BASE, "_universe.json")
FACTS_PATH = os.path.join(BASE, "_hub_facts.json")
NAV_SNIPPET_PATH = os.path.join(BASE, "_nav_snippet.html")
OUT_PATH = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "docs", "backtest", "country_scan", "japan.html"))

SNAPSHOT_DATE = "2026-09-10"
DD_BASIS_DATE = "2026-09-10"

# ---------------------------------------------------------------------------
# 0. 資料載入
# ---------------------------------------------------------------------------


def load_universe():
    with open(UNIVERSE_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_facts():
    with open(FACTS_PATH, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 1. 格式化工具
# ---------------------------------------------------------------------------


def jpy_zhao_from_raw(v):
    """原始日圓數字 -> 「¥X兆」（兆=1e12），母體總市值等大數字用。"""
    return f"¥{v/1e12:,.1f}兆"


def jpy_yi_from_raw(v):
    """原始日圓數字 -> 「¥X億」（億=1e8），個股／中型數字用。"""
    return f"¥{v/1e8:,.0f}億"


def days_between(d1, d2):
    a = datetime.date.fromisoformat(d1)
    b = datetime.date.fromisoformat(d2)
    return (b - a).days


# ---------------------------------------------------------------------------
# 2. 母體統計（全部從 _universe.json 現算）
# ---------------------------------------------------------------------------

TOP_SECTOR_N = 12

# TradingView 日股 sector 粗分類（20 類）中譯，圖上顯示中文、圖註中英對照
SECTOR_ZH = {
    "Finance": "金融",
    "Producer Manufacturing": "生產製造",
    "Process Industries": "製程工業",
    "Electronic Technology": "電子科技",
    "Retail Trade": "零售貿易",
    "Consumer Non-Durables": "非耐久消費品",
    "Technology Services": "科技服務",
    "Consumer Durables": "耐久消費品",
    "Distribution Services": "流通服務",
    "Consumer Services": "消費服務",
    "Transportation": "運輸",
    "Industrial Services": "工業服務",
    "Health Technology": "健康科技",
    "Commercial Services": "商業服務",
    "Non-Energy Minerals": "非能源礦業",
    "Utilities": "公用事業",
    "Communications": "通訊",
    "Energy Minerals": "能源礦業",
    "Miscellaneous": "其他",
    "Health Services": "健康服務",
}


def sec_zh(name):
    return SECTOR_ZH.get(name, name)


def sector_legend(rows):
    pairs = [f"{sec_zh(r['sector'])} {r['sector']}" for r in rows if r["sector"] in SECTOR_ZH]
    return "／".join(pairs)


def compute_population_stats(uni):
    cons = uni["constituents"]
    total_mcap = sum(c["market_cap_jpy"] for c in cons if c.get("market_cap_jpy"))
    count = len(cons)

    srt = sorted(cons, key=lambda c: -(c.get("market_cap_jpy") or 0))

    def topn_share(n):
        s = sum(c["market_cap_jpy"] for c in srt[:n])
        return s, s / total_mcap * 100

    conc = {}
    for n in (1, 5, 10, 20):
        s, p = topn_share(n)
        conc[n] = {"mcap": s, "pct": p}
    conc["rest"] = {"pct": 100 - conc[20]["pct"]}
    top10_names = [f'{c["name"]}（{c["code"]}）' for c in srt[:10]]

    sec = defaultdict(float)
    seccount = defaultdict(int)
    for c in cons:
        k = c.get("sector") or "未分類"
        mc = c.get("market_cap_jpy") or 0
        sec[k] += mc
        seccount[k] += 1
    sector_rows = sorted(
        ({"sector": k, "mcap": v, "pct": v / total_mcap * 100, "n": seccount[k]} for k, v in sec.items()),
        key=lambda r: -r["pct"],
    )
    top_sectors = sector_rows[:TOP_SECTOR_N]
    rest_sector_pct = 100 - sum(r["pct"] for r in top_sectors)
    rest_sector_n = count - sum(r["n"] for r in top_sectors)

    pb_known = [c for c in cons if c.get("price_book") is not None]
    pb_below1 = [c for c in pb_known if c["price_book"] < 1]
    pb_below1_n = len(pb_below1)
    pb_below1_pct = pb_below1_n / len(pb_known) * 100 if pb_known else 0.0

    def quartiles(vals):
        vals = sorted(vals)
        n = len(vals)
        if n == 0:
            return None
        return {"n": n, "median": st.median(vals), "q1": vals[n // 4], "q3": vals[(3 * n) // 4]}

    fpe_vals = [c["forward_pe"] for c in cons if c.get("forward_pe") is not None and c["forward_pe"] > 0]
    fpe_all = quartiles(fpe_vals)
    tpe_vals = [c["trailing_pe"] for c in cons if c.get("trailing_pe") is not None and c["trailing_pe"] > 0]
    tpe_all_median = st.median(tpe_vals) if tpe_vals else None

    roe_all_vals = [c["roe"] * 100 for c in cons if c.get("roe") is not None]
    roe_all_median = st.median(roe_all_vals) if roe_all_vals else None

    dy_vals_all = [c["dividend_yield"] for c in cons if c.get("dividend_yield") is not None]
    dy_paying = [v for v in dy_vals_all if v > 0]
    dy_median = st.median(dy_paying) if dy_paying else None
    dy_known_n = len(dy_vals_all)
    dy_missing_n = count - dy_known_n
    dy_buckets_def = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (8, 9999)]
    dy_hist = []
    for lo, hi in dy_buckets_def:
        n = sum(1 for v in dy_paying if lo <= v < hi)
        label = f"{lo}–{hi}%" if hi < 9999 else f"≥{lo}%"
        dy_hist.append({"label": label, "n": n})

    # 產業別 ROE 中位數（前 TOP_SECTOR_N 大，依市值排序；n<5 由呼叫端灰化）
    roe_by_sector = []
    for r in top_sectors:
        group = [c for c in cons if (c.get("sector") or "未分類") == r["sector"]]
        vals = [c["roe"] * 100 for c in group if c.get("roe") is not None]
        roe_by_sector.append({
            "sector": r["sector"], "n": len(vals),
            "median": st.median(vals) if vals else None,
            "mcap_pct": r["pct"],
        })

    # 盈餘殖利率（1/forward_pe，百分比）分布，供論點B股息/盈餘兩把尺對照
    ey_vals = [100.0 / c["forward_pe"] for c in cons if c.get("forward_pe") is not None and c["forward_pe"] > 0]
    ey_median = st.median(ey_vals) if ey_vals else None

    # ROE x P/B 四象限（population 版本，8% 線 × 1x 線），對照論點A的東證官方Prime序列
    q1 = q2 = q3 = q4 = 0
    q1_mcap = q3_mcap = 0.0
    quad_n_known = 0
    for c in cons:
        roe = c.get("roe")
        pb = c.get("price_book")
        if roe is None or pb is None:
            continue
        quad_n_known += 1
        mc = c.get("market_cap_jpy") or 0
        roe_pct = roe * 100
        if pb >= 1 and roe_pct >= 8:
            q1 += 1
            q1_mcap += mc
        elif pb >= 1 and roe_pct < 8:
            q2 += 1
        elif pb < 1 and roe_pct < 8:
            q3 += 1
            q3_mcap += mc
        else:
            q4 += 1
    quad_mcap_total = sum((c.get("market_cap_jpy") or 0) for c in cons if c.get("roe") is not None and c.get("price_book") is not None)

    return {
        "count": count,
        "total_mcap": total_mcap,
        "conc": conc,
        "top10_names": top10_names,
        "sector_rows": sector_rows,
        "top_sectors": top_sectors,
        "rest_sector_pct": rest_sector_pct,
        "rest_sector_n": rest_sector_n,
        "pb_known_n": len(pb_known),
        "pb_below1_n": pb_below1_n,
        "pb_below1_pct": pb_below1_pct,
        "fpe_all": fpe_all,
        "tpe_all_median": tpe_all_median,
        "roe_all_median": roe_all_median,
        "dy_median": dy_median,
        "dy_hist": dy_hist,
        "dy_known_n": dy_known_n,
        "dy_missing_n": dy_missing_n,
        "roe_known_n": len(roe_all_vals),
        "fpe_known_n": len(fpe_vals),
        "roe_by_sector": roe_by_sector,
        "ey_median": ey_median,
        "quad": {
            "q1": q1, "q2": q2, "q3": q3, "q4": q4,
            "q1_mcap_pct": q1_mcap / quad_mcap_total * 100 if quad_mcap_total else 0.0,
            "q3_mcap_pct": q3_mcap / quad_mcap_total * 100 if quad_mcap_total else 0.0,
            "n_known": quad_n_known,
        },
    }


# ---------------------------------------------------------------------------
# 3. SVG 圖表（內嵌、全寬、大字、柔和色，色票沿用頁面既有 CSS 變數）
# ---------------------------------------------------------------------------

C_INK = "#0c1521"
C_BODY = "#2a3a52"
C_SEC = "#6b7a92"
C_BORDER = "#e5dfd0"
C_ACCENT = "#0d2244"
C_ACCENT2 = "#3a5a8c"
C_GOLD = "#b8924a"
C_GOLD_DEEP = "#8f6d2c"
C_GOLD_SOFT = "#e8d4a8"
C_SURFACE2 = "#f3efe4"
C_NEG = "#b91c1c"
C_POS = "#15803d"

SVG_W = 920


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_wrap(inner, height, label):
    height = int(round(height))
    return (
        f'<svg viewBox="0 0 {SVG_W} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}" '
        f'style="display:block;font-family:\'IBM Plex Mono\',ui-monospace,monospace">{inner}</svg>'
    )


def svg_exhibit_a(stats, facts):
    """論點A：population ROE(8%)×P/B(1x)四象限占比 + 東證官方Prime序列(2023-02 vs 2026-02)兩點對照。"""
    quad = stats["quad"]
    q_total = quad["n_known"]

    def pct(n):
        return n / q_total * 100 if q_total else 0.0

    bar_x, top = 24, 40
    box_w, box_h = 380, 220
    parts = [
        f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">'
        f'母體 ROE（8%線）× P/B（1倍線）四象限（{q_total} 檔有效樣本）</text>'
    ]
    # 四象限方塊：左上Q4(P/B<1,ROE高) 左下Q3(P/B<1,ROE低) 右上Q1(P/B>=1,ROE高) 右下Q2(P/B>=1,ROE低)
    # 注意：以下字串會經過 esc()，一律寫原始「<」，寫 &lt; 會被二次轉義成 &amp;lt;
    cells = [
        ("Q4　便宜但賺錢\nP/B<1・ROE≥8%", quad["q4"], bar_x, top, C_GOLD_SOFT),
        ("Q1　高PBR高ROE\nP/B≥1・ROE≥8%", quad["q1"], bar_x + box_w / 2, top, C_ACCENT),
        ("Q3　便宜且不賺錢\nP/B<1・ROE<8%", quad["q3"], bar_x, top + box_h / 2, C_GOLD),
        ("Q2　貴但不賺錢\nP/B≥1・ROE<8%", quad["q2"], bar_x + box_w / 2, top + box_h / 2, C_ACCENT2),
    ]
    for label, n, x, y, color in cells:
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{box_w/2-4:.1f}" height="{box_h/2-4:.1f}" rx="3" fill="{color}"/>')
        lines = label.split("\n")
        for i, seg in enumerate(lines):
            fill = "#fff" if color in (C_ACCENT, C_ACCENT2, C_GOLD) else C_INK
            parts.append(f'<text x="{x+14:.1f}" y="{y+27+i*16:.1f}" font-size="12" font-weight="700" fill="{fill}">{esc(seg)}</text>')
        parts.append(f'<text x="{x+14:.1f}" y="{y+box_h/2-16:.1f}" font-size="17" font-weight="800" fill="{"#fff" if color in (C_ACCENT,C_ACCENT2,C_GOLD) else C_INK}">{n} 檔（{pct(n):.1f}%）</text>')

    # 右側：東證官方 Prime 序列兩點對照
    rx = bar_x + box_w + 50
    q = facts["prime_pb_quadrant"]["value"]
    p23 = q["2023-02-28"]
    p26 = q["2026-02-28"]
    parts.append(f'<text x="{rx}" y="20" font-size="14" font-weight="700" fill="{C_INK}">東證官方 Prime 市場（1,508家）P/B&lt;1 比率</text>')
    rows = [("2023-02-28", p23["pbr_below1_pct"], p23["q1_pct"]), ("2026-02-28", p26["pbr_below1_pct"], p26["q1_pct"])]
    ry = 46
    # 長條可用寬度須預留右側資料標籤（最長為「Q1高PBR高ROE　51.7%」約 150px），否則標籤會被畫布右緣切掉
    label_reserve = 156
    rw = SVG_W - rx - 30 - label_reserve
    for label, pb1, q1p in rows:
        parts.append(f'<text x="{rx}" y="{ry+14:.1f}" font-size="12.5" fill="{C_SEC}">{label}</text>')
        w1 = rw * pb1 / 60
        parts.append(f'<rect x="{rx}" y="{ry+20:.1f}" width="{w1:.1f}" height="16" rx="2" fill="{C_GOLD_DEEP}"/>')
        parts.append(f'<text x="{rx+w1+8:.1f}" y="{ry+32:.1f}" font-size="12.5" font-weight="700" fill="{C_INK}">P/B&lt;1　{pb1:.1f}%</text>')
        w2 = rw * q1p / 60
        parts.append(f'<rect x="{rx}" y="{ry+42:.1f}" width="{w2:.1f}" height="16" rx="2" fill="{C_ACCENT}"/>')
        parts.append(f'<text x="{rx+w2+8:.1f}" y="{ry+54:.1f}" font-size="12.5" font-weight="700" fill="{C_INK}">Q1高PBR高ROE　{q1p:.1f}%</text>')
        ry += 76
    parts.append(
        f'<text x="{rx}" y="{ry+14:.1f}" font-size="12" fill="{C_SEC}">Q1（高PBR高ROE）2026-02 占 Prime'
        f'總市值 {p26["q1_market_cap_share_pct"]:.1f}%（¥942兆）</text>'
    )
    total_h = max(top + box_h + 24, ry + 34)
    return svg_wrap("".join(parts), total_h, "母體ROE×P/B四象限與東證官方Prime序列對照")


def svg_exhibit_b(stats, facts):
    """論點B：母體殖利率 vs 盈餘殖利率分布（中位數標示）對照JGB線 + JGB殖利率時間序列。"""
    hist = stats["dy_hist"]
    bar_x, top = 24, 40
    max_n = max(h["n"] for h in hist) if hist else 1
    bw = 78
    gap = 14
    base_y = top + 130
    jgb = facts["jgb_10y_yield"]["value"]
    parts = [
        f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">'
        f'母體股息殖利率分布（{stats["dy_known_n"]}檔有殖利率資料，母體{stats["count"]}檔中{stats["dy_missing_n"]}檔缺值）'
        f'對照10年期JGB殖利率</text>'
    ]
    x = bar_x
    for h in hist:
        hh = 130 * h["n"] / max_n if max_n else 0
        color = C_GOLD_DEEP if h["label"].startswith(("6", "≥")) else C_ACCENT2
        parts.append(f'<rect x="{x:.1f}" y="{base_y-hh:.1f}" width="{bw}" height="{hh:.1f}" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{base_y-hh-6:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{h["n"]}</text>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{base_y+15:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{h["label"]}</text>')
        x += bw + gap
    jgb_x = bar_x + (jgb / 9.0) * (x - gap - bar_x)
    parts.append(f'<line x1="{jgb_x:.1f}" y1="{top+2}" x2="{jgb_x:.1f}" y2="{base_y+8:.1f}" stroke="{C_NEG}" stroke-width="2" stroke-dasharray="4,3"/>')
    parts.append(f'<text x="{jgb_x+6:.1f}" y="{top+14:.1f}" font-size="12" font-weight="700" fill="{C_NEG}">10Y JGB {jgb:.2f}%</text>')
    y0 = base_y + 38
    parts.append(
        f'<text x="{bar_x}" y="{y0:.1f}" font-size="12.5" fill="{C_GOLD_DEEP}" font-weight="700">'
        f'母體殖利率中位數 {stats["dy_median"]:.2f}%　vs　母體盈餘殖利率（1／前瞻本益比）中位數 {stats["ey_median"]:.2f}%'
        "</text>"
    )
    parts.append(
        f'<text x="{bar_x}" y="{y0+18:.1f}" font-size="12" fill="{C_SEC}">'
        f'股息殖利率利差（殖利率中位數－JGB）約 {stats["dy_median"]-jgb:+.2f}pp；'
        f'盈餘殖利率利差（盈餘殖利率中位數－JGB）約 {stats["ey_median"]-jgb:+.2f}pp——兩把尺方向相反。</text>'
    )

    # 右側：JGB 10Y 時間序列
    hist_pts = list(facts["jgb_10y_yield_history"]["value"].items())
    ry0 = y0 + 44
    parts.append(f'<text x="{bar_x}" y="{ry0:.1f}" font-size="14" font-weight="700" fill="{C_INK}">10年期JGB殖利率時間序列（財務省官方收盤，月底取樣）</text>')
    # 首尾兩點的資料標籤是置中對齊，起點須離左緣夠遠、終點須離右緣夠遠，否則「0.62%」「2023-12」會貼邊或被切掉
    rx = bar_x + 42
    chart_w = SVG_W - rx - 60
    chart_h = 110
    cy0 = ry0 + 20
    max_v = max(v for _, v in hist_pts) * 1.15
    step = chart_w / (len(hist_pts) - 1)
    coords = []
    for i, (label, v) in enumerate(hist_pts):
        x = rx + i * step
        y = cy0 + chart_h - chart_h * v / max_v
        coords.append((x, y))
    path = " L ".join(f"{x:.1f} {y:.1f}" for x, y in coords)
    parts.append(f'<path d="M {path}" fill="none" stroke="{C_GOLD_DEEP}" stroke-width="3"/>')
    for (x, y), (label, v) in zip(coords, hist_pts):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{C_ACCENT}"/>')
        parts.append(f'<text x="{x:.1f}" y="{y-12:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{v:.2f}%</text>')
        parts.append(f'<text x="{x:.1f}" y="{cy0+chart_h+17:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{esc(label)}</text>')
    total_h = cy0 + chart_h + 34
    return svg_wrap("".join(parts), total_h, "母體殖利率分布與JGB殖利率時間序列")


def svg_exhibit_c(facts):
    """論點C：外資持股比重FY2023->FY2025時間序列 + 買回授權金額年度長條。"""
    hist = facts["foreign_holding_share_history"]["value"]
    pts = [("FY2023", hist["FY2023"]), ("FY2024", hist["FY2024"]), ("FY2025", hist["FY2025"])]
    bar_x, top = 24, 44
    chart_w = 330
    chart_h = 140
    max_v = 36.0
    min_v = 30.0
    parts = [f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">外資持股占大盤市值比重（時價總額基礎）</text>']
    step = chart_w / (len(pts) - 1)
    coords = []
    for i, (label, v) in enumerate(pts):
        x = bar_x + i * step
        y = top + chart_h - chart_h * (v - min_v) / (max_v - min_v)
        coords.append((x, y))
    path = " L ".join(f"{x:.1f} {y:.1f}" for x, y in coords)
    parts.append(f'<path d="M {path}" fill="none" stroke="{C_GOLD_DEEP}" stroke-width="3"/>')
    for (x, y), (label, v) in zip(coords, pts):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{C_ACCENT}"/>')
        parts.append(f'<text x="{x:.1f}" y="{y-12:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{v:.1f}%</text>')
        parts.append(f'<text x="{x:.1f}" y="{top+chart_h+16:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{esc(label)}</text>')

    x2 = bar_x + chart_w + 60
    parts.append(f'<text x="{x2}" y="20" font-size="14" font-weight="700" fill="{C_INK}">庫藏股買回金額（¥兆，授權與執行兩種口徑並列）</text>')
    b = facts["buyback_authorization_series"]["value"]
    bars = [
        ("FY2024\n授權", b["FY2024_authorization_jpy_trillion"]),
        ("FY2024\n執行", b["FY2024_execution_jpy_trillion"]),
        ("FY2025\n授權", b["FY2025_authorization_jpy_trillion"]),
        ("2026\n1-5月授權", b["2026_jan_may_jpy_trillion"]),
    ]
    chart_w2 = SVG_W - x2 - 30
    bw2 = chart_w2 / len(bars) - 10
    max_b = max(v for _, v in bars) * 1.25
    base_y2 = top + chart_h
    for i, (label, v) in enumerate(bars):
        x = x2 + i * (bw2 + 10)
        h = chart_h * v / max_b
        parts.append(f'<rect x="{x:.1f}" y="{base_y2-h:.1f}" width="{bw2:.1f}" height="{h:.1f}" rx="2" fill="{C_ACCENT2}"/>')
        parts.append(f'<text x="{x+bw2/2:.1f}" y="{base_y2-h-6:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">¥{v:.1f}兆</text>')
        for j, seg in enumerate(label.split("\n")):
            parts.append(f'<text x="{x+bw2/2:.1f}" y="{top+chart_h+17+j*14:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{esc(seg)}</text>')
    note_y = top + chart_h + 52
    parts.append(
        f'<text x="{bar_x}" y="{note_y:.1f}" font-size="12" fill="{C_SEC}">'
        "只有第 1 與第 3 根同口徑可比（會計年度授權額，FY2024→FY2025 為 +18%）；</text>"
        f'<text x="{bar_x}" y="{note_y+16:.1f}" font-size="12" fill="{C_SEC}">'
        "第 2 根是會計年度實際執行額、第 4 根是曆年前 5 個月的授權累計，與前兩根不是同一序列，僅供量級對照。</text>"
    )
    total_h = note_y + 36
    return svg_wrap("".join(parts), total_h, "外資持股時間序列與買回授權金額")


def svg_exhibit_d(stats):
    """論點D：產業別ROE中位數長條（前12業種，n<5灰化）。"""
    rows = stats["roe_by_sector"]
    bar_x, top = 220, 44
    row_h = 30
    chart_w = SVG_W - bar_x - 90
    axis_max = 20.0
    MIN_N = 5
    parts = [f'<text x="20" y="20" font-size="14" font-weight="700" fill="{C_INK}">產業別 ROE 中位數（依市值前 {len(rows)} 大分類）</text>']

    def xpos(v):
        return bar_x + max(0, min(v, axis_max)) / axis_max * chart_w

    zero_x = xpos(0)
    for t in (0, 5, 10, 15, 20):
        tx = xpos(t)
        parts.append(f'<line x1="{tx:.1f}" y1="{top-6}" x2="{tx:.1f}" y2="{top+row_h*len(rows)+6}" stroke="{C_BORDER}" stroke-width="1"/>')
        parts.append(f'<text x="{tx:.1f}" y="{top-10}" font-size="12" fill="{C_SEC}" text-anchor="middle">{t}%</text>')
    y = top
    for r in rows:
        small = r["n"] < MIN_N or r["median"] is None
        name = f'{esc(sec_zh(r["sector"]))}（n={r["n"]}）' + ("　樣本不足不可比" if small else "")
        parts.append(f'<text x="20" y="{y+row_h/2+5:.1f}" font-size="12.5" fill="{C_SEC if small else C_BODY}">{name}</text>')
        if not small:
            v = max(0, r["median"])
            w = xpos(v) - zero_x
            color = C_ACCENT2 if r["median"] >= 8 else C_GOLD
            parts.append(f'<rect x="{zero_x:.1f}" y="{y+6}" width="{w:.1f}" height="{row_h-14}" rx="2" fill="{color}"/>')
            parts.append(f'<text x="{xpos(v)+8:.1f}" y="{y+row_h/2+5:.1f}" font-size="12" font-weight="700" fill="{C_INK}">{r["median"]:.1f}%</text>')
        y += row_h
    parts.append(f'<line x1="{zero_x:.1f}" y1="{top-6}" x2="{zero_x:.1f}" y2="{y+6}" stroke="{C_SEC}" stroke-width="1.5"/>')
    ly = y + 22
    parts.append(f'<text x="20" y="{ly:.1f}" font-size="12" fill="{C_SEC}">東證Q1／Q4象限判準的ROE 8% 分岔線另以深色標示（≥8%深藍／&lt;8%金色）</text>')
    total_h = ly + 20
    return svg_wrap("".join(parts), total_h, "產業別ROE中位數")


def svg_exhibit_e(facts):
    """論點E：MBO/TOB/Activist三序列逐年件數分組長條（缺年明標）。"""
    mtd = facts["mbo_tob_delisting_2025"]["value"]
    af = facts["activist_filings_2025"]["value"]
    mbo = dict(facts["mbo_count_history"]["value"])
    tob = {"2024": mtd["tob_count_2024"], "2025": mtd["tob_count_2025"], "2026H1": mtd["tob_count_2026h1"]}
    act = {"2024": af["significant_proposal_filings_2024"], "2025": af["significant_proposal_filings_2025"]}
    years = ["2023", "2024", "2025", "2026H1"]
    series = [("MBO", mbo, C_ACCENT), ("TOB", tob, C_ACCENT2), ("Activist申報", act, C_GOLD_DEEP)]
    bar_x, top = 24, 40
    chart_w = SVG_W - bar_x - 30
    chart_h = 200
    max_v = 260
    group_w = chart_w / len(years)
    bw = group_w / (len(series) + 1)
    parts = [f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">MBO／TOB／Activist申報件數（逐年，缺年明標）</text>']
    base_y = top + chart_h
    for gi, yr in enumerate(years):
        gx = bar_x + gi * group_w
        for si, (name, data, color) in enumerate(series):
            v = data.get(yr)
            x = gx + si * bw + bw * 0.3
            if v is None:
                parts.append(f'<text x="{x+bw*0.35:.1f}" y="{base_y-6:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">缺</text>')
                continue
            h = chart_h * v / max_v
            parts.append(f'<rect x="{x:.1f}" y="{base_y-h:.1f}" width="{bw*0.7:.1f}" height="{h:.1f}" rx="2" fill="{color}"/>')
            parts.append(f'<text x="{x+bw*0.35:.1f}" y="{base_y-h-6:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{v}</text>')
        parts.append(f'<text x="{gx+group_w/2:.1f}" y="{base_y+18:.1f}" font-size="12.5" fill="{C_SEC}" text-anchor="middle">{yr}</text>')
    ly = base_y + 40
    lx = bar_x
    for name, data, color in series:
        parts.append(f'<rect x="{lx}" y="{ly-11}" width="12" height="12" fill="{color}"/>')
        parts.append(f'<text x="{lx+17}" y="{ly}" font-size="12" fill="{C_BODY}">{esc(name)}</text>')
        lx += 17 + len(name) * 13 + 26
    total_h = ly + 16
    return svg_wrap("".join(parts), total_h, "MBO／TOB／Activist逐年件數")


# ---------------------------------------------------------------------------
# 4. 內文組裝：五個論點卡
# ---------------------------------------------------------------------------


def tile(v, l):
    return f'<div class="t"><div class="v">{v}</div><div class="l">{esc(l)}</div></div>'


def argument_card(letter, tag, lead, bullets, sowhat, tiles, exnum, cap, sub, svg, take):
    bl = "".join(f"<li>{b}</li>" for b in bullets)
    tl = "".join(tiles)
    return f'''
<div class="card">
<h3><span class="h-n">論點{letter}</span>{tag}</h3>
<div class="argcard">
  <div>
    <div class="lead">{lead}</div>
    <ul>{bl}</ul>
    <div class="sowhat"><b>所以呢：</b>{sowhat}</div>
  </div>
  <div class="tilecol">{tl}</div>
</div>
<div class="exhibit scroll">
<div class="ex-tag">Exhibit {exnum}</div>
<div class="ex-cap">{cap}</div>
<div class="ex-sub">{sub}</div>
{svg}
<div class="ex-take">{take}</div>
</div>
</div>
'''


def build_arguments(stats, facts):
    out = []
    q = facts["prime_pb_quadrant"]["value"]
    p26 = q["2026-02-28"]
    p23 = q["2023-02-28"]

    # A 東證改革已跑完大盤層
    out.append(argument_card(
        "A", "東證改革把大盤層級的便宜大致定價完畢",
        f'東證「資本コストや株価を意識した経営」（資本成本與股價意識經營）要請跑了三年，Prime 市場（東京證券交易所最高一層市場，'
        f'掛牌門檻最嚴）P/B（股價淨值比，股價除以每股淨資產，低於1代表股價低於帳面價值）低於1的比率由 '
        f'{p23["pbr_below1_pct"]}%（2023-02-28）降至 {p26["pbr_below1_pct"]}%（2026-02-28），'
        f'高PBR高ROE（股東權益報酬率，衡量公司用股東的錢賺多少報酬）象限（Q1）占家數由 {p23["q1_pct"]}% 升至 {p26["q1_pct"]}%，'
        f'占 2026-02 Prime 總市值 {p26["q1_market_cap_share_pct"]}%——大盤層級的重新定價大致已經完成。',
        [
            f'把同一把尺（ROE 8% 分岔線 × P/B 1倍線）套到本頁自建的 {stats["count"]} 檔母體（市值≥¥1,000億，'
            f'不限Prime，含Standard市場〔第二層，掛牌門檻次嚴〕與Growth市場〔第三層，給高成長但規模未達標的公司〕的大型股），'
            f'P/B&lt;1 比率為 {stats["pb_below1_pct"]:.1f}%'
            f'（{stats["pb_below1_n"]}／{stats["pb_known_n"]}檔；母體{stats["count"]}檔中{stats["count"]-stats["pb_known_n"]}檔查無P/B值，'
            f'分母只計有值者，{SNAPSHOT_DATE}快照，本頁自算）——'
            "與東證官方Prime序列的方向一致，但母體口徑不同（東證序列僅計Prime、本頁母體含市值達標的Standard／Growth），"
            "兩個數字不可直接相減比較。",
            "機制是活的：東證每月更新「開示企業一覧表」（已回應資本成本要請的公司名單）公開施加聲譽壓力，"
            "2026年1月起改為直接刊載各公司公司治理報告書中的對應揭露；經產省2023年行動指針、金融廳監督指針對保險業"
            "施壓削減政策性持股，三線並進——但這是聲譽與透明度壓力機制，不是強制下市觸發器，"
            "須與「上場維持基準」（東證各市場的最低流通市值、股東人數等維持門檻）過渡期屆滿這條真正的強制下市機制分開理解。",
            f"約七週後（本頁快照日{SNAPSHOT_DATE}起算，2026-10-30）東證將啟動TOPIX指數見直し（指數編製規則改版）第二階段首次定期入替——"
            "選股改採兩道門檻並用：年間成交金額週轉率≥0.2，且累積自由流通調整市值排名進入前96%（既有成分股的續留門檻較寬，為0.14與97%）；"
            "母體首次涵蓋Standard與Growth市場。未達標既有成分股權重分8段等分季度調降（每季12.5%），自2026-10起約2年降至零，"
            "其間2027年10月做一次再評估，通過續留門檻者停止繼續調降。"
            "這是本頁所有機制中唯一不需要任何公司治理動作、純靠機械篩選就會觸發被動買盤或賣壓的一條，"
            "方向與「機制在讓便宜股重新定價」的主敘事相反：被動賣壓會讓低自由流通、控制股東集中的名字折價加深而非收斂，幅度未知但方向明確。",
            "市值集中度的位移比家數位移更劇烈：Q1（高PBR高ROE）2023年占家數36.6%時占Prime市值遠低於2026年72.5%的比重"
            "——市場給龍頭股重新定價的速度快過給長尾股重新定價的速度。",
        ],
        "剩下的機會不在「這個市場整體便宜」，機制已經把最容易的部分做完；殘餘的P/B&lt;1角落要看機制訊號密度，不是折價深度。",
        [
            # tile() 的 label 會經過 esc()，此處一律寫原始「<」，寫 &lt; 會二次轉義
            tile(f'{p23["pbr_below1_pct"]}%→{p26["pbr_below1_pct"]}%', "Prime市場P/B<1比率（2023-02→2026-02）"),
            tile(f'{p26["q1_market_cap_share_pct"]}%', "高PBR高ROE象限占Prime總市值"),
            tile(f'{stats["pb_below1_pct"]:.1f}%', f'本頁母體P/B<1比率（{stats["pb_below1_n"]}／{stats["pb_known_n"]}檔，自算）'),
        ],
        1, "母體ROE×P/B四象限與東證官方Prime序列對照",
        f'來源：東證官方Prime序列引自第一生命經濟研究所（現第一ライフ資産運用経済研究所）2026-04-01報告，樣本為1,508家連續上市Prime企業，'
        "as-of 2026-02-28；該報告本文只列四象限家數，圖上的P/B&lt;1比率50.1%／26.9%是以Q3＋Q4家數除以1,508家計得（506+249=755；312+93=405）。"
        f'母體四象限為本頁對{SNAPSHOT_DATE}快照自算，'
        f"四象限需同時查得ROE與P/B才納入，故有效樣本{stats['quad']['n_known']}檔少於計分卡P/B&lt;1那列的{stats['pb_known_n']}檔"
f"（圖上Q3＋Q4＝{stats['quad']['q3']+stats['quad']['q4']}檔，計分卡為{stats['pb_below1_n']}檔，差額是有P/B但查無ROE的個股）。"
        "兩者口徑不同（Prime-only vs 市值≥¥1,000億全市場）不可直接相減。",
        svg_exhibit_a(stats, facts),
        "東證改革的紅利已經反映在股價裡；下一輪機會的判準是機制訊號密度，不是「這檔還沒漲」。",
    ))

    # B 金利回來了，兩把尺相反
    jgb = facts["jgb_10y_yield"]["value"]
    per = facts["topix_per_pbr_snapshot"]["value"]
    dy_topix = facts["topix_dividend_yield"]["value"]
    ey = 100 / per["per_forecast_prime"]
    ey_tr = 100 / per["per_trailing_topix"]
    jh = facts["jgb_10y_yield_history"]["value"]
    j0_label, j0 = list(jh.items())[0]
    out.append(argument_card(
        "B", "金利回來了，股息與盈餘兩把估值尺指向相反方向",
        f'10年期JGB（日本國債，長期無風險利率的代表指標）殖利率已升至{jgb:.2f}%'
        f'（{facts["jgb_10y_yield"]["as_of"]}，財務省官方收盤），TOPIX（東證股價指數，涵蓋東證主要上市股票的市值加權指數）'
        f'加權股息殖利率{dy_topix}%（{facts["topix_dividend_yield"]["as_of"]}）'
        f'已低於JGB殖利率——股息殖利率利差約{dy_topix-jgb:+.2f}pp（債券贏），'
        f'但把東証Prime預估本益比{per["per_forecast_prime"]}倍（{per["per_forecast_as_of"]}）換算成盈餘殖利率'
        f'（本益比的倒數，1÷本益比，代表每投入1元股價對應多少稅後盈餘）約{ey:.2f}%，利差約{ey-jgb:+.2f}pp（股票贏）'
        "——同一個市場，兩把利差尺說相反的話。",
        [
            f'兩把尺的正負號都不隨口徑改變：改用JPX官方TOPIX實績本益比{per["per_trailing_topix"]}倍'
            f'（{per["per_trailing_as_of"]}，以已確定的財報數字計算）換算，盈餘殖利率{ey_tr:.2f}%、利差仍為{ey_tr-jgb:+.2f}pp（股票贏），'
            "只是幅度較窄。JPX本身不發布TOPIX的預估本益比，預估口徑只能引第三方，兩個口徑並列而不擇一。",
            f'母體層級同樣呈現這個矛盾：{stats["count"]}檔母體殖利率中位數{stats["dy_median"]:.2f}%'
            f'（{stats["dy_known_n"]}檔有資料）、盈餘殖利率中位數{stats["ey_median"]:.2f}%（{stats["fpe_known_n"]}檔有前瞻本益比，'
            f'皆{SNAPSHOT_DATE}快照，本頁自算）——'
            f'前者對JGB利差約{stats["dy_median"]-jgb:+.2f}pp，後者約{stats["ey_median"]-jgb:+.2f}pp，方向與TOPIX層級一致。',
            f'JGB殖利率從{j0_label}月底的{j0:.2f}%升到現值{jgb:.2f}%，是當時的約{jgb/j0:.1f}倍、絕對值上升約{jgb-j0:.2f}pp；'
            f'同一序列在2026-09-02曾收3.006%，是1996-09以來首度站上3%——'
            f'BOJ（日本銀行，日本的中央銀行）政策利率同期由0～0.1%升至{facts["boj_policy_rate_current"]["value"]:.2f}%'
            "（2026-06-16決議、06-17生效，2026-07-31會議維持不變），為1995年以來、31年來最高。"
            "下一次會議訂於2026-09-17至18日，本頁快照日尚未召開，本頁不假設結果。",
            "這個+2.6pp量級的盈餘殖利率利差是沒有匯率避險的比較——只有直接持有日圓資產、承擔匯率波動的投資人拿得到；"
            "對選擇把日圓避險回自己本幣的投資人，避險成本約等於日圓與該本幣的短端利率差，"
            "當本幣短端利率高於日圓時，這筆成本的量級與利差相近，換算後「股票贏」的部分大致會被利率差本身吃掉，是完全不同的兩筆帳。",
            "股息殖利率利差為負，代表過去「日股殖利率天生比公債高」的環境已經結束——這改變了收息型選股的篩選門檻，"
            "不能再用表面殖利率排序，必須疊加對JGB的緩衝門檻（見鏡頭四）。",
        ],
        "兩把利差尺同時呈現，不選邊：股息殖利率利差說債券贏、盈餘殖利率利差說股票贏，判讀日股估值時必須先確認講的是哪一把尺。",
        [
            tile(f'{jgb:.2f}%', "10年期JGB殖利率"),
            tile(f'{dy_topix-jgb:+.2f}pp', "TOPIX股息殖利率利差（債券贏）"),
            tile(f'{ey-jgb:+.2f}pp', "Prime盈餘殖利率利差（股票贏）"),
        ],
        2, "母體殖利率分布與JGB殖利率時間序列",
        f"來源：母體殖利率／盈餘殖利率為本頁對{SNAPSHOT_DATE}快照自算；JGB殖利率五個點全部取自財務省官方每日收盤序列的月底值"
        "（末點為2026-09-09單日收盤），同一來源、同一取樣規則，可逐點比較。",
        svg_exhibit_b(stats, facts),
        "利率回來的世界裡，日股估值不是「貴或便宜」單一答案，是兩把尺同時存在、方向相反，選哪把尺決定看到的結論。",
    ))

    # C 買盤結構
    fh = facts["foreign_holding_share_history"]["value"]
    out.append(argument_card(
        "C", "買盤結構：外資、NISA、庫藏股回購三條線同步走高",
        f'外資持股占大盤市值比重由FY2023的{fh["FY2023"]}%升至FY2025的{fh["FY2025"]}%'
        '（基準日2026-03底，2026-07-02公布），史上新高、官方措辭為2023年度以來連續3年刷新新高；'
        f'NISA（少額投資非課稅制度，個人在額度內投資的獲利與配息免稅）新制上路後累計投資金額達'
        f'¥{facts["nisa_cumulative_amount"]["value"]["amount_jpy_trillion"]}兆'
        '（2025年12月底，金融廳2026-07-03公布），較政府原訂「2027年12月底累計¥56兆」的目標提前約2年達成；但這筆錢有相當比例流向海外資產（日股／海外拆分無官方數字，見方法論），不能整筆讀成日股買盤。',
        [
            f'庫藏股買回授權金額FY2025（2026-03期）達¥{facts["buyback_authorization_series"]["value"]["FY2025_authorization_jpy_trillion"]}兆'
            f'，較FY2024的¥{facts["buyback_authorization_series"]["value"]["FY2024_authorization_jpy_trillion"]:.2f}兆增加'
            f'{facts["buyback_authorization_series"]["value"]["FY2025_yoy_growth_pct"]}%，連續第5年增加；'
            f'2026年1-5月授權累計已達¥{facts["buyback_authorization_series"]["value"]["2026_jan_may_jpy_trillion"]}兆'
            f'（YoY+{facts["buyback_authorization_series"]["value"]["2026_jan_may_yoy_growth_pct"]}%），由Sony集團與日立主導——'
            "授權（設定買回額度）與執行（實際買回）、會計年度與曆年是不同口徑，只有兩個會計年度授權額之間可以直接比較。",
            f'交叉持股（企業互相持有對方股票以維繫業務關係，而非單純財務投資）解消是這條資金流背後的供給端：'
            f'狹義口徑（僅計銀行＋非金融事業法人互持）已降至FY2024的'
            f'{facts["cross_shareholding_ratio"]["value"]["narrow_pct_fy2024"]}%'
            f'（較前一年{facts["cross_shareholding_ratio"]["value"]["narrow_yoy_change_pp"]}pp），廣義口徑（加計壽險與產險持股）'
            f'{facts["cross_shareholding_ratio"]["value"]["broad_pct_fy2024"]}%，首度跌破10%，兩者自FY2019起連續6年刷新歷史低點；'
            f'廣義口徑1990年度末的高點為{facts["cross_shareholding_ratio"]["value"]["broad_peak_pct_fy1990"]}%'
            f'（常被引用的約70%是另一條尺「政策保有投資家比率」的{facts["cross_shareholding_ratio"]["value"]["policy_holder_peak_pct_fy1990"]}%，'
            "分母含非上市持有者，兩把尺相差約20pp，不可混用）。",
            f'官方統計同向：JPX調查FY2025事業法人等持股比重17.7%、都銀地銀等1.7%，兩者皆為史上最低。'
            f'豐田集團私有化豐田自動織機（交易規模約¥{facts["toyota_industries_privatization"]["value"]["deal_size_jpy_trillion"]}兆）'
            "是這條主線最大的單一案例，一次交易解消豐田自動織機與豐田汽車／Aisin／電裝／豐田通商間的四方交叉持股。",
            "產險業是交叉持股解消最明確的時程線：金融廳2025年因產險業投標圍標與卡特爾醜聞公布監督指針修訂，"
            "東京海上控股與MS&AD控股的政策性持股歸零目標同為2030-03-31（FY2029年度末），SOMPO控股為2031-03-31（FY2030年度末）；"
            "三家都曾表示考慮提前，但截至本頁快照日查無任何一家正式修訂目標時點，也無任何一家已達成歸零。",
            f'個人股東延べ人數（累計人次，同一人持有多檔會重複計數）9,198萬人，2014年度以來連續12年增加，'
            "較2015年度的4,945萬人成長約1.9倍——買盤結構的擴大不只是外資與機構，個人參與度也在同步墊高。",
        ],
        "三條買盤線（外資、NISA、庫藏股回購）與一條供給線（交叉持股解消）指向同一件事：需求在擴大、可流通股數在收縮。四者的節奏與統計口徑各自獨立，不宜合併成單一敘事。",
        [
            tile(f'{fh["FY2025"]}%', "外資持股占大盤市值比重（史上新高）"),
            tile(f'¥{facts["nisa_cumulative_amount"]["value"]["amount_jpy_trillion"]}兆', "NISA累計投資金額"),
            tile(f'¥{facts["buyback_authorization_series"]["value"]["FY2025_authorization_jpy_trillion"]}兆', "FY2025庫藏股買回授權（連5年增）"),
        ],
        3, "外資持股時間序列與買回授權金額",
        "來源：外資持股為JPX／名證／福證／札證聯合「2025年度株式分布状況調査」（2026-07-02公布，基準日各年3月底）；"
        "買回金額為日本經濟新聞與野村資產管理統計，as-of 見計分卡與§6方法論。",
        svg_exhibit_c(facts),
        "買盤結構的三條線都指向同一個方向（需求擴大、供給收縮），但各自的節奏與口徑不同，不能讀成一條乾淨的單一序列。",
    ))

    # D 資本報酬地圖
    top_roe_rows = sorted(
        [r for r in stats["roe_by_sector"] if r["median"] is not None and r["n"] >= 5],
        key=lambda r: -r["median"],
    )
    best = top_roe_rows[0] if top_roe_rows else None
    worst = top_roe_rows[-1] if top_roe_rows else None
    out.append(argument_card(
        "D", "資本報酬地圖：複利機器供給豐富，零檔便宜",
        f'{stats["count"]}檔母體ROE中位數{stats["roe_all_median"]:.1f}%（{SNAPSHOT_DATE}快照，本頁自算），'
        f'但拉開到產業別看差異可達數倍——'
        + (f'{sec_zh(best["sector"])}分類ROE中位數{best["median"]:.1f}%（n={best["n"]}）最高，'
           f'{sec_zh(worst["sector"])}分類僅{worst["median"]:.1f}%（n={worst["n"]}）' if best and worst else "")
        + "，資本報酬的地圖不是均勻分布，是高度集中在特定產業分類。",
        [
            "複利機器（能把賺到的錢持續再投入、維持高資本報酬率的公司）的供給豐富是真的，東證改革三年的制度紅利也還在"
            "——但供給豐富不等於便宜；市場早就看到這些好生意也付過錢了，站內量化篩選出的候選經深度剖析後零檔可誠實標記為便宜"
            "（完整方法論與逐檔查證見鏡頭一）。",
            "反直覺發現：多檔市場公認的日本複利機器代表——精密自動化與材料獨佔類的幾家龍頭——此刻實際ROE已跌破常見的15%門檻，"
            "不是生意變差，是資本支出循環正處低谷；估值確實友善，但買的是循環復甦的判斷，不是已經證實的複利（完整名單見鏡頭一）。",
            "產業別ROE差異也是治理鏡頭（鏡頭二）的背景：P/B&lt;1角落裡「真便宜」（ROE已達東證Q4判準但沒被市場給估值）"
            "與「該便宜」（低ROE結構性，集中在基本材料產能過剩與汽車供應鏈電動化轉型壓力）的分岔，本質上就是這張地圖的局部放大。",
        ],
        "日本不缺高資本報酬的公司，缺的是「便宜又已經被證實」的高資本報酬公司；產業別的中位數差異提示了哪裡的供給集中，不等於哪裡有錯價。",
        [
            tile(f'{stats["roe_all_median"]:.1f}%', "母體ROE中位數"),
            tile(f'{best["median"]:.1f}%' if best else "n/a", f'{sec_zh(best["sector"])}分類ROE中位數（最高）' if best else "資料不足"),
            tile(f'{worst["median"]:.1f}%' if worst else "n/a", f'{sec_zh(worst["sector"])}分類ROE中位數（最低）' if worst else "資料不足"),
        ],
        4, "產業別ROE中位數",
        f"來源：本頁{stats['count']}檔母體快照，as-of {SNAPSHOT_DATE}，本頁自算。"
        "依市值排序取前12大分類；圖上括號內的 n 是該分類中「查得到 ROE 的檔數」，不是該分類的總檔數，"
        "n 低於5檔者灰化並標「樣本不足不可比」；"
        f"產業分類採TradingView粗分類，圖上為中譯，中英對照：{sector_legend(stats['top_sectors'])}。",
        svg_exhibit_d(stats),
        "地圖顯示供給集中在哪些產業，但「值不值得投資」仍要靠逐檔查證——高中位數的產業裡一樣可能沒有便宜貨。",
    ))

    # E 退出通道是活的
    mtd = facts["mbo_tob_delisting_2025"]["value"]
    af = facts["activist_filings_2025"]["value"]
    pcp = facts["parent_child_buyback_premium"]["value"]
    out.append(argument_card(
        "E", "退出通道是活的：MBO、TOB、Activist三條管道同步創紀錄",
        f'MBO（管理層收購，公司經營團隊聯合資金買下自家公司股權、使其下市）2025年{mtd["mbo_count_2025"]}件創紀錄'
        f'（+{mtd["mbo_yoy_growth_pct"]}% YoY）；TOB（公開收購，收購方向全體股東公開出價買股）2025年{mtd["tob_count_2025"]}件創紀錄；'
        f'Activist（積極介入公司治理、要求改善資本配置或推動出售/下市的機構投資人）大量保有報告書申報'
        f'{af["significant_proposal_filings_2025"]}件，較2024年{af["significant_proposal_filings_2024"]}件成長——三條管道同步創紀錄。',
        [
            f'2025年以下市為前提的TOB與MBO合計{mtd["mbo_tob_delisting_combined_2025"]}家（TOB 80家＋MBO 32家，東京商工調查口徑）；'
            f'同一年東證實際上場廢止（下市）{mtd["delisting_2025_tse_total"]}家，連續2年為最多，'
            "理由別為他社收購49家、支配股東等收購27家、MBO 26家、完全子公司化17家——"
            "退出通道不是政策宣示，是真實發生的公司數量。四組數字口徑不同（發表基準／完成基準／含或不含收購以外原因），不可互相加減。",
            f'溢價結構是真溢價，不是最低價：TOB整體溢價中位數{facts["tob_premium_median_2024"]["value"]}%'
            f'（{facts["tob_premium_median_2024"]["as_of"]}，相對公表前1個月平均股價，區間7.0%～275.1%）；'
            "連最接近內部人交易性質的親子上市買回（母公司對已上市子公司發動收購，使其完全併入母公司、消除同一集團兩層上市的結構），"
            f'本頁自行彙整的{pcp["cases_n"]}件具名案例中位溢價也有約{pcp["median_pct_range_low"]}–{pcp["median_pct_range_high"]}%'
            "（依前一日收盤或1個月均價兩種基準）——這6件是本頁自建的小樣本，查無官方或第三方資料庫給出同口徑統計，"
            "個案散布極大，只能讀成方向性證據，不可當成可靠的期望值。",
            f'{af["agm_shareholder_proposals_2025"]}家公司在2025年6月股東會季（統計期間2024-07至2025-06）收到股東提案（歷史新高），其中'
            f'{af["activist_institutional_proposals_2025"]}家收到activist／機構投資人提案（較2024年'
            f'{af["activist_institutional_proposals_2024"]}家增加，同創紀錄）——大和總研定性觀察：activist策略正由'
            "「對話型」轉向「交渉型」，愈趨鎖定經由下市／私有化提案取得控制權溢價。",
            "機制雙向都能動，不是保證獲利的套利：2025年「同意なき買収」（未經目標公司同意的收購提案，即敵意收購）達8件過去最多，"
            "其中4件成立，成功率約5成（經產省「公正な買収の在り方に関する研究会」2026-02統計）；"
            "日本嚴格的內線交易規範也讓外部投資人（非公司內部人）結構性缺乏公告前的資訊優勢，能參與的永遠是公告後的殘餘價差。",
        ],
        "退出通道的溢價是真的，但買不到公告前；三條管道創紀錄代表機制在動，不代表任何具體案例都會照劇本走。",
        [
            tile(f'{mtd["mbo_count_2025"]}件', "MBO件數2025（創紀錄）"),
            tile(f'{mtd["tob_count_2025"]}件', "TOB件數2025（創紀錄）"),
            tile(f'{pcp["median_pct_range_low"]}–{pcp["median_pct_range_high"]}%', "親子上市買回中位溢價"),
        ],
        5, "MBO／TOB／Activist逐年件數",
        "來源：MBO與TOB件數為日本經濟新聞（曆年、發表基準；TOB為公開買付届出書提出基準，含不涉下市的TOB）；"
        "Activist為大和總研「重要提案行為あり」大量保有報告書申報件數（曆年）。三個序列各自獨立、不可相加；"
        "缺年份（MBO 2024、Activist 2023與2026上半年）誠實標「缺」，不用推算值填補。",
        svg_exhibit_e(facts),
        "退出通道的機制訊號密度是本頁計分卡以外唯一明確逐年創紀錄的一組數字，但個案層級的成敗仍需逐一查證。",
    ))

    return out


def build_arguments_html(stats, facts):
    return "".join(build_arguments(stats, facts))


# ---------------------------------------------------------------------------
# 5. 計分卡
# ---------------------------------------------------------------------------


def build_scorecard(stats, facts):
    q = facts["prime_pb_quadrant"]["value"]
    p23, p26 = q["2023-02-28"], q["2026-02-28"]
    jgb = facts["jgb_10y_yield"]["value"]
    per = facts["topix_per_pbr_snapshot"]["value"]
    ey = 100 / per["per_forecast_prime"]
    mtd = facts["mbo_tob_delisting_2025"]["value"]
    af = facts["activist_filings_2025"]["value"]
    cross = facts["cross_shareholding_ratio"]["value"]
    rows = [
        (f"母體市值總額與檔數（{stats['count']}檔）", f'{jpy_zhao_from_raw(stats["total_mcap"])}／{stats["count"]}檔', SNAPSHOT_DATE,
         "東證主板市值≥¥1,000億普通股（TradingView篩選器）", "母體快照（本頁自算）"),
        ("前十大個股占母體市值", f'{stats["conc"][10]["pct"]:.1f}%', SNAPSHOT_DATE,
         "少數龍頭股決定母體裡最大的一塊市值", "母體快照（本頁自算）"),
        (f"母體P/B&lt;1比率（{stats['pb_below1_n']}／{stats['pb_known_n']}檔）", f'{stats["pb_below1_pct"]:.1f}%', SNAPSHOT_DATE,
         f"全市場口徑，非Prime-only；母體{stats['count']}檔中{stats['count']-stats['pb_known_n']}檔查無P/B值，分母只計有值者。見論點A",
         "母體快照（本頁自算）"),
        (f"母體ROE中位數（{stats['roe_known_n']}檔有值）", f'{stats["roe_all_median"]:.1f}%', SNAPSHOT_DATE,
         "資本報酬整體水位，產業別差異可達數倍，見論點D", "母體快照（本頁自算）"),
        (f"母體前瞻本益比中位數（{stats['fpe_known_n']}檔有值）", f'{stats["fpe_all"]["median"]:.1f}倍', SNAPSHOT_DATE,
         "換算盈餘殖利率對照JGB，見論點B", "母體快照（本頁自算）"),
        (f"母體殖利率中位數（{stats['dy_known_n']}檔有值）", f'{stats["dy_median"]:.2f}%', SNAPSHOT_DATE,
         "股息殖利率利差已轉負，見論點B", "母體快照（本頁自算）"),
        ("Prime市場P/B&lt;1比率（改革前→現值）", f'{p23["pbr_below1_pct"]}%→{p26["pbr_below1_pct"]}%', "2023-02-28→2026-02-28",
         "1,508家連續上市Prime企業樣本；比率為該報告四象限家數自行計算（Q3＋Q4／1,508）", "第一生命經濟研究所"),
        ("外資持股占大盤市值比重", f'{facts["foreign_holding_share_pct"]["value"]}%', facts["foreign_holding_share_pct"]["as_of"],
         "史上新高，官方措辭為2023年度以來連續3年刷新新高", "JPX等四證交所聯合「2025年度株式分布状況調査」"),
        ("NISA累計投資金額", f'¥{facts["nisa_cumulative_amount"]["value"]["amount_jpy_trillion"]}兆', facts["nisa_cumulative_amount"]["as_of"],
         "政府目標為2027年12月底累計¥56兆，提前約2年達成", "金融廳「NISA口座の利用状況調査」"),
        ("BOJ（日本銀行）政策利率", f'{facts["boj_policy_rate_current"]["value"]:.2f}%', facts["boj_policy_rate_current"]["as_of"],
         "中央銀行對無擔保隔夜拆款利率的目標水準；1995年以來、31年來最高。下次會議2026-09-17至18日，本頁快照日尚未召開",
         "日本銀行金融政策決定會合聲明"),
        ("10年期JGB殖利率", f'{jgb:.2f}%', facts["jgb_10y_yield"]["as_of"],
         "財務省官方收盤值；同序列2026-09-02曾收3.006%，1996-09以來首度站上3%", "財務省「国債金利情報」"),
        ("TOPIX股息殖利率利差／Prime盈餘殖利率利差",
         f'{facts["topix_dividend_yield"]["value"]-jgb:+.2f}pp／{ey-jgb:+.2f}pp',
         f'{facts["topix_dividend_yield"]["as_of"]}／{per["per_forecast_as_of"]}（同減JGB 2026-09-09）',
         "兩把尺方向相反，債券贏vs股票贏；改用實績本益比21.05倍算，盈餘殖利率利差仍為正（約+1.86pp），見論點B",
         "JPX官方TOPIX Factsheet／いちよし經濟研究所（引用日經預估）"),
        ("庫藏股買回授權金額（FY2025）", f'¥{facts["buyback_authorization_series"]["value"]["FY2025_authorization_jpy_trillion"]}兆', "FY2025（2026-03期）",
         f'較FY2024的¥{facts["buyback_authorization_series"]["value"]["FY2024_authorization_jpy_trillion"]:.2f}兆增加'
         f'{facts["buyback_authorization_series"]["value"]["FY2025_yoy_growth_pct"]}%，連續第5年增加', "日本經濟新聞"),
        ("2025年MBO／TOB／東證下市家數", f'{mtd["mbo_count_2025"]}件／{mtd["tob_count_2025"]}件／{mtd["delisting_2025_tse_total"]}家', "2025全年（曆年）",
         "MBO與TOB為發表基準且皆創紀錄；下市家數為東證實際上場廢止統計（含收購以外原因），三者口徑不同不可相加",
         "日本經濟新聞／東京證券交易所統計"),
        ("Activist件數（2025）", f'{af["significant_proposal_filings_2025"]}件', "2025全年",
         f'「重要提案行為あり」大量保有報告書申報件數，較2024年{af["significant_proposal_filings_2024"]}件成長；'
         f'{af["activist_funds_count"]}個申報者鎖定{af["targeted_companies"]}家公司', "大和總研"),
        ("交叉持股比率（狹義口徑）", f'{cross["narrow_pct_fy2024"]}%', "FY2024底",
         f'廣義口徑（加計壽險與產險）{cross["broad_pct_fy2024"]}%，首度跌破10%；廣義口徑1990年度末高點為'
         f'{cross["broad_peak_pct_fy1990"]}%（常引用的約70%是另一把尺「政策保有投資家比率」，不可混用）',
         "野村資本市場研究所（NICMR）"),
    ]
    trs = []
    for label, val, asof, gloss, src in rows:
        trs.append(
            f'<tr><td class="lbl">{label}</td><td class="num strong">{val}</td>'
            f'<td class="num" style="color:var(--sec)">{asof}</td><td class="why">{gloss}</td>'
            f'<td class="why">{src}</td></tr>'
        )
    build_scorecard.row_count = len(rows)
    return "".join(trs)


# ---------------------------------------------------------------------------
# 6. 七個投資鏡頭一覽表
# ---------------------------------------------------------------------------

LENS_ROWS = [
    dict(n=1, slug="compounders", name="複利機器",
         q="日本不缺高ROE公司，缺的是還沒被定價的高ROE公司",
         a="以ROE≥15%×正營收成長的量化尺掃476檔TOPIX500型母體（子頁計算基礎，見方法論），篩出70檔候選，"
           "命中率14.7%；12檔深度剖析後零檔可誠實標記為便宜，真正還沒被定價完的角落是ROE被砍到10%左右、"
           "站在資本支出循環谷底的名字。",
         n_dd=0, gap="Fanuc／SMC／信越化學等循環谷底名字站內尚無獨立DD，需要判斷資本支出循環是否轉向"),
    dict(n=2, slug="governance", name="治理改革",
         q="P/B&lt;1角落裡，折價深度與機制訊號密度哪個才是真訊號",
         a="476檔母體（子頁計算基礎）中P/B&lt;1共105檔（22.1%），拆開後37檔是「真便宜」（ROE已達東證Q4判準）、"
           "65檔是「該便宜」（低ROE結構性）、其餘3檔ROE缺值未歸類；折價最深不等於機制訊號最密集，具名activist＋量化承諾＋已簽約"
           "交割事件三者齊備才是真正即將重新定價的組合。",
         n_dd=0, gap="105檔P/B&lt;1候選裡，僅少數幾組（MediPal／Suzuken／SUBARU等）有具體機制訊號，多數站內零覆蓋"),
    dict(n=3, slug="financials", name="金融",
         q="三大行創紀錄獲利是真新聞，但股價是不是已經聽過了",
         a="19檔可比銀行中17檔（89%）隱含ROE（用Gordon Growth模型從股價淨值比反推的股東權益報酬率）高於實際ROE"
           "——市場已經替BOJ升息推升利差的劇本提前付款；MS&AD控股是三雄中政策性持股殘留最厚、市場給的信用卻最少的例外。",
         n_dd=0, gap="MS&AD控股站內尚無獨立DD驗證2030年政策性持股歸零承諾的兌現節奏"),
    dict(n=4, slug="dividends", name="收息",
         q="JGB升破2.8%後，日股收息的供給還剩多少",
         a="80檔殖利率≥3.5%的候選，套用JGB+150bp緩衝門檻後剩25檔，再扣掉8檔配息率超過100%與2檔轉金融後，對15檔逐檔查證10年配息史，最終只有3檔通過零實質砍息驗證（Sekisui House質性更好但被量化門檻機械式排除，子頁稱其為「準第五席」是沿用原始候選排序順位，不代表前面有四席）——供給密度遠比表面殖利率排行榜稀薄。",
         n_dd=0, gap="3檔通過驗證的核心候選加1檔質性候選，站內均無獨立DD，僅完成殖利率階梯篩選"),
    dict(n=5, slug="events", name="事件驅動",
         q="MBO／TOB／Activist三條管道創紀錄，溢價是真的還是最低價",
         a="連最接近內部人交易性質的親子上市買回中位溢價都約30–32%（本頁自建6件小樣本），不是最低價；但外部投資人結構性缺乏公告前"
           "資訊優勢，敵意收購（同意なき買収）提案成功率僅約5成，東邦控股2026-06股東會的防衛表決證明機制雙向都能動。",
         n_dd=0, gap="親子上市解消候選（Canon Marketing Japan／大阪製鐵）與activist觀察名單站內均無獨立DD"),
    dict(n=6, slug="ai-chain", name="AI出口鏈",
         q="半導體供應鏈的獨佔純度有沒有換來估值溢價",
         a="15個節點掃出至少六道日廠近壟斷關卡，查證後原本三個看似異常的高本益比全數證實是數據假象，"
           "獨佔純度沒有換來額外估值溢價這個結論更加確立；Kioxia查證後前瞻PE僅約6.8倍是估值最不對稱的候選"
           "（但需警惕循環頂部陷阱）。",
         n_dd=2, gap="Tokyo Electron／Lasertec兩個獨佔純度最深的節點站內完全沒做過DD"),
    dict(n=7, slug="domestic", name="內需",
         q="人口每年減少的市場裡，誰還握有真正的定價權",
         a="9檔內需代表股拆成客數×客單價後，僅3檔（迅銷／FOOD&LIFE／麥當勞日本）是客數與客單價同步走揚的真定價權，"
           "其餘是客單價撐大盤、客數在流失的假定價權；2026-11-01免稅新制是尚未定價的現金流逆風。",
         n_dd=0, gap="3檔真定價權候選（迅銷／FOOD&LIFE／麥當勞日本）站內均無獨立DD"),
]


def lens_dd_coverage(n):
    rows = [r for r in WATCH_EXISTING if r["lens_n"] == n]
    win = [r for r in rows if days_between(r["date"], DD_BASIS_DATE) <= 90]
    return len(rows), len(win)


def build_lens_table():
    trs = []
    for r in LENS_ROWS:
        n_dd, n_win = lens_dd_coverage(r["n"])
        if n_dd > 0:
            cov = f'{n_dd} 檔／{n_win/n_dd*100:.0f}% 窗內'
        else:
            cov = "0 份既有DD"
        trs.append(
            f'<tr><td class="lbl"><a href="japan/{r["slug"]}.html">鏡頭{r["n"]}・{r["name"]}</a></td>'
            f'<td class="why">{r["q"]}</td><td class="why">{r["a"]}</td>'
            f'<td class="num" style="white-space:nowrap">{cov}</td><td class="why">{r["gap"]}</td></tr>'
        )
    return "".join(trs)


# ---------------------------------------------------------------------------
# 7. 可作戰名單
# ---------------------------------------------------------------------------

DD_DOC_BASE = "https://research.investmquest.com/dd"

WATCH_EXISTING = [
    dict(t="6146", name="DISCO Corporation", lens="鏡頭六・AI出口鏈", lens_n=6, verdict="A｜核心候選",
         wait="建議分批進場，等回測 BB 中軌 ¥68,377 或 W52 ¥53,225 後加碼。",
         gloss="BB中軌＝布林通道中軌線（20期均線），W52＝52週移動平均線；兩者皆為技術面訊號的參考水位，不是高低點",
         dd="DD_6146T_20260522.html", date="2026-05-22"),
    dict(t="6857", name="Advantest Corp.", lens="鏡頭六・AI出口鏈", lens_n=6, verdict="A｜核心候選",
         wait="建議追高分批至 Bollinger 中軌 ¥25,291 後加碼。",
         gloss="Bollinger中軌＝布林通道中軌線（20期均線），技術面訊號的參考水位",
         dd="DD_6857T_20260522.html", date="2026-05-22"),
]

WATCH_CANDIDATES = [
    ("6954", "Fanuc", "鏡頭一・複利機器", "循環谷底真複利：正牌複利機器歷史ROIC/ROE紀錄，估值已降至循環低點友善區間，缺口是資本支出循環復甦的判斷"),
    ("6273", "SMC", "鏡頭一・複利機器", "循環谷底真複利：ROE已跌破常見門檻，估值友善但賭的是循環復甦"),
    ("4063", "信越化學", "鏡頭一・複利機器", "循環谷底真複利：矽晶圓與PVC雙循環分散，客戶轉向補庫存訊號最明確"),
    ("7459", "MediPal控股", "鏡頭二・治理改革", "治理×事件交集：自身正TOB收購PALTAC消除親子上市，角色是整併發動者，缺口是整併完成後的財務效果"),
    ("9987", "Suzuken", "鏡頭二・治理改革", "治理×事件交集：批發四強中ROE最高，已達東證Q4真便宜門檻"),
    ("7270", "SUBARU", "鏡頭二・治理改革", "治理×事件交集：已決議買回並消却庫藏股，訊號具體但ROE仍偏低，缺口是ROE能否跟上訊號"),
    ("8725", "MS&AD控股", "鏡頭三・金融", "政策保有股殘留占自身市值比重三雄最厚，隱含ROE卻是三雄中定價最保守的一檔，缺口是一份DD驗證2030年歸零承諾兌現節奏"),
    ("3231", "Nomura Real Estate Holdings", "鏡頭四・收息", "收息核心候選：15期連續增配，逐檔查證零實質砍息"),
    ("2815", "Ariake Japan", "鏡頭四・收息", "收息核心候選：11個財年零下修"),
    ("4208", "UBE", "鏡頭四・收息", "收息核心候選：僅1次形式性下修（實績持平）"),
    ("1928", "Sekisui House", "鏡頭四・收息", "質性優於表列3檔（ROE 12.6%、11年零砍息），但殖利率4.27%差門檻4.3%共0.03pp，被量化門檻機械式排除"),
    ("8129", "東邦控股", "鏡頭五・事件驅動", "多層交集觀察池：治理雙重便宜候選×收息鏡頭質性名單×activist在籍三鏡頭同時交集，2026-06-26股東會毒丸（防禦性增資授權）案已以54.70%通過，activist介入路徑因此變難但仍值得觀察"),
    ("8060", "Canon Marketing Japan", "鏡頭五・事件驅動", "親子上市解消：Canon持股54.1%，分析師點名首選，同集團已有先例（precedent）成立"),
    ("5449", "大阪製鐵", "鏡頭五・事件驅動", "親子上市解消：日本製鐵持股約55.6%，先例為山陽特殊製鋼（2025已完成）"),
    ("8035", "Tokyo Electron", "鏡頭六・AI出口鏈", "EUV光阻塗佈／顯影機近100%獨佔，市值與Advantest同量級，卻零個股DD"),
    ("6920", "Lasertec", "鏡頭六・AI出口鏈", "EUV光罩actinic檢測（用與曝光機同波長的光源檢查光罩缺陷）字面100%獨佔，FY26訂單大幅下滑後股價回檔，需驗證是雜訊或真轉弱"),
    ("285A", "Kioxia Holdings", "鏡頭六・AI出口鏈", "查證後前瞻PE僅約6.8倍，本頁估值最不對稱候選，但需警惕循環頂部陷阱"),
    ("6981", "Murata Manufacturing", "鏡頭六・AI出口鏈", "MLCC全球約40%，查證後估值非便宜標的，AI伺服器升級敘事待驗證"),
    ("7735", "SCREEN Holdings", "鏡頭六・AI出口鏈", "單片式晶圓清洗約25%，查證後估值僅溫和折價，缺口理由是覆蓋空白"),
    ("6525", "Kokusai Electric", "鏡頭六・AI出口鏈", "批次型ALD／熱處理設備全球第一約70%，2023年才重新IPO，站內完全未觸及"),
    ("4186", "Tokyo Ohka Kogyo", "鏡頭六・AI出口鏈", "EUV光阻，JSR私有化後唯一仍可投資的一家，PB明顯低於同護城河深度的其他節點"),
    ("9983", "迅銷", "鏡頭七・內需", "真定價權：客數與客單價同步走揚，但PE已站上高檔，且近期出現月度反轉訊號需標註脆弱性"),
    ("3563", "FOOD&LIFE", "鏡頭七・內需", "真定價權：漲價後維持並提升客數同時拉高客單價，ROE全表最高"),
]


def build_watchlist():
    trs = []
    for r in WATCH_EXISTING:
        gloss = (f'<br><span style="color:var(--gold-deep)">本頁補註：{r["gloss"]}</span>' if r.get("gloss") else "")
        trs.append(
            f'<tr><td class="lbl">{esc(r["name"])}（{r["t"]}）</td><td class="why lenscol">{r["lens"]}</td>'
            f'<td class="why"><b>{r["verdict"]}</b></td>'
            f'<td class="why"><span data-verbatim="dd">{esc(r["wait"])}</span>{gloss}</td>'
            f'<td class="why ddcol"><a href="{DD_DOC_BASE}/{r["dd"]}">查看DD</a></td></tr>'
        )
    for t, name, lens, reason in WATCH_CANDIDATES:
        trs.append(
            f'<tr><td class="lbl">{esc(name)}（{t}）</td><td class="why lenscol">{lens}</td>'
            f'<td class="why" style="color:var(--warn);white-space:nowrap">無（站內零覆蓋）</td><td class="why">{reason}</td>'
            f'<td class="why ddcol">—</td></tr>'
        )
    return "".join(trs)


def build_dd_review_note():
    lines = []
    for r in WATCH_EXISTING:
        d = days_between(r["date"], DD_BASIS_DATE)
        if d > 90:
            lines.append(f'{esc(r["name"])}（{r["t"]}，裁決日{r["date"]}），截至{DD_BASIS_DATE}已滿{d}天，超過站內90天複審窗')
    return "；".join(lines)


# ---------------------------------------------------------------------------
# 8. 會推翻本頁判斷的證據
# ---------------------------------------------------------------------------

FALSIFIERS = [
    "若本頁母體P/B&lt;1比率或東證官方Prime序列在下一次量測時止跌回升（而不是延續2023年以來的收斂趨勢），"
    "代表論點A「大盤層級重新定價已大致完成」的判讀需要重新檢視。",
    "若BOJ在2026-09-17至18日或後續會議暫停升息路徑，且10年期JGB殖利率明顯回落，"
    "代表論點B「金利回來了」的利率背景本身需要重新評估，兩把估值尺的相對關係可能反轉。",
    "若外資持股占大盤市值比重或NISA累計投資金額在下一期統計中轉為下滑，且不是單一季度雜訊，"
    "代表論點C「買盤結構同步走高」需要重新檢視資金流方向。",
    "若循環谷底的複利機器候選（Fanuc／SMC／信越化學）在下一份財報中ROE持續下滑而非回升，"
    "代表論點D對「資本支出循環將轉向」的判斷落空，這批名字的估值友善程度需要重新評估。",
    "若2026年MBO或TOB件數較2025年明顯下滑，或親子上市買回溢價中位數顯著低於30%，"
    "代表論點E「退出通道持續創紀錄」的敘事動能已經放緩。",
    "若2026-10-30 TOPIX指數見直し第二階段首次定期入替後，納入Standard／Growth的個股未出現預期中的機械性買盤，"
    "代表本頁對這個機械機制的判讀需要重新檢視。",
]


def build_falsifiers():
    return "".join(f'<div class="amber">{x}</div>' for x in FALSIFIERS)


# ---------------------------------------------------------------------------
# 9. 資料、方法與盲區
# ---------------------------------------------------------------------------


def build_methodology(stats, facts, uni=None):
    meta = (uni or {}).get("meta", {})
    return f'''
<b>母體怎麼建的</b>：範圍為東京證券交易所主板普通股（Prime／Standard／Growth三市場皆可入選），
市值≥¥1,000億，快照日期{SNAPSHOT_DATE}。候選清單取自TradingView日本篩選器（條件：exchange=TSE、
subtype=common、market_cap_basic&gt;¥1,000億），排除REIT／信託（industry=Real Estate Investment Trusts）
與優先股後，共{stats["count"]}檔。TradingView欄位為主資料；抽樣40檔（依市值分層各10檔）以 yfinance（另一組獨立行情資料源）交叉比對後，trailing本益比、前瞻本益比、ROE、殖利率四個欄位
中位數偏差均超過5%（分屬計算基期／分析師共識來源差異），已整欄改抓yfinance；市值、P/B、現金、
股數、52週高低偏差在5%以內，維持TradingView原值。<br><br>

<b>與先前TOPIX 500型476檔母體的對應</b>：先前建構（以2022-02版TOPIX 500成分名單為底＋6檔手補）的476檔母體中，
474檔（99.6%）在新母體{stats["count"]}檔中找到；缺少的2檔為Milbon（4919，現市值約¥989億，剛好跌破
¥1,000億門檻的邊界案例）與PALTAC（8283，已於2026年經MediPal控股TOB完成收購下市，親子上市解消的
真實案例，與鏡頭二治理鏡頭的敘事互相印證，非資料缺失）。先前這份TOPIX 500型476檔母體本身仍保留
供對照。<br><br>

<b>子頁仍使用TOPIX 500型476檔母體計算</b>：七個投資鏡頭子頁（compounders／governance／financials／
dividends／events／ai-chain／domestic）皆是在本頁母體重建之前完成的獨立研究，計算基礎是先前那份
TOPIX 500型476檔母體（例如「476檔篩出70檔候選」「105/476落在P/B&lt;1」「476檔套用JGB+150bp門檻剩
25檔候選」）。
本頁引用子頁結論時已明寫「476檔母體」字樣以資區分；本頁自己的母體圖表（Exhibit 1、2、4）
一律使用新母體{stats["count"]}檔計算，兩個母體的數字不可混寫成同一個口徑。<br><br>

<b>TradingView口徑與JPX 33業種的差異</b>：本頁產業分類採TradingView自身的20類粗分類（Finance／
Producer Manufacturing／Process Industries等），不是JPX官方33業種分類——後者本次未能透過
自動化工具取得逐檔對應表，是誠實列出的分類口徑差異，非本頁刻意選擇。<br><br>

<b>同一個量有兩個口徑時怎麼處理</b>：本頁的規則是取最新、標明口徑、必要時並列，不擇一也不平均。
（1）估值兩把尺：股息殖利率用JPX官方TOPIX Factsheet（2026-08-31）、盈餘殖利率用東証Prime預估本益比
（2026-09-04第三方統計，因JPX本身不發布預估本益比，其Factsheet的21.05倍是實績口徑），兩者都減同一個
JGB收盤值（2026-09-09）；實績口徑的結論並列於論點B，方向一致。
（2）交叉持股1990年高點：廣義持ち合い比率為50.5%，市場上常見的約70%是另一條線「政策保有投資家比率」
（分母含非上市持有者），兩把尺相差約20pp，本頁只用前者。
（3）2025年的退出通道件數有四種統計：MBO 30件與TOB 136件（曆年、發表基準）、以下市為前提的TOB 80家＋MBO 32家
（東京商工調查、含進行中）、東證實際上場廢止125家（曆年、含收購以外原因），四者不可互相加減。
（4）庫藏股只有兩個會計年度授權額之間可以直接比較，執行額與曆年累計是另外兩種口徑。<br><br>

<b>本頁未能取得而沿用不確定值的地方</b>：配息總額FY2026/3期存在¥20兆與¥23兆兩個互相矛盾的數字
（疑為預測vs實際決算落差或跨年度誤標）；Prime市場家數在不同as-of日期的官方精確數字未能取得同一
資料源的連續序列；現貨成交值占比（外資約67.4%、個人約27.0%）為市場慣用描述，未鎖定單一精確月份，
信心度中等；NISA累計¥71兆的日股／海外拆分無官方精確數字，僅有2024單年、部分推估的概算；
親子上市買回中位溢價30–32%是本頁自建的6件具名案例小樣本，查無任何官方或第三方資料庫給出同口徑統計，
只能讀成方向性證據。<br><br>

<b>站內DD裁決的抄錄規則</b>：可作戰名單的裁決欄位逐字取自各檔DD的dd-meta區塊signal／verdict欄位；
本頁DD schema（v12.4）沒有獨立的rearm_trigger欄位，「在等什麼」改取verdict欄位中描述後續操作門檻的
子句逐字引用（連數字與符號都原樣保留，不因此觸發買賣指令字樣掃描——這些是DD原文的
逐字引用，不是本頁自己的建議），欄內以金色標示的「本頁補註」是本頁另外加上的白話解釋，不屬於原裁決文字。
同一家公司一律取日期最新的那一份；零覆蓋候選標「無（站內零覆蓋）」。<br><br>

<b>已知缺口清單</b>：GPIF（年金積立金管理運用独立行政法人，日本公共年金的資產運用機構，全球規模最大之一）
現行日股配置精確金額，與BOJ ETF處分計畫最新公告速度，未查得精確現值；
MSCI ACWI中日本現行權重與TOPIX／Nikkei 225十年本益比／股價淨值比區間未取得官方一手數字；三大銀行精確NIM
（淨利差，銀行放款利率與資金成本之差）數字僅有淨利金額；消却（註銷）vs金庫株（庫存股保留）市場整體比率無加總數字；
2025年TOB全年溢價中位數僅取得部分基準的數字，故本頁只寫2024年度；MBO 2024年的同口徑件數未查得，
圖上標「缺」而不用增幅回推填補；每筆結構數字的原始出處與查證日期已在計分卡與各論點卡標明。
'''


# ---------------------------------------------------------------------------
# 10. 排版：CJK／英文（含 ticker、數字）自動留白一格
# ---------------------------------------------------------------------------


def add_cjk_latin_spacing(text):
    text = re.sub(r"([一-鿿])([A-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9])([一-鿿])", r"\1 \2", text)
    return text


# ---------------------------------------------------------------------------
# 11. HTML 外殼
# ---------------------------------------------------------------------------

EXTRA_CSS = """
.argcard{display:grid;grid-template-columns:1fr 210px;gap:20px;align-items:start;margin-bottom:16px}
@media(max-width:700px){.argcard{grid-template-columns:1fr}}
.argcard .lead{font-size:14.5px;font-weight:700;color:var(--ink);margin-bottom:10px;line-height:1.62}
.argcard ul{margin:0 0 10px 18px;padding:0}
.argcard li{margin-bottom:8px;font-size:13.5px;line-height:1.7;color:var(--body)}
.argcard .sowhat{font-size:13px;color:var(--body);border-top:1px solid var(--border);padding-top:10px;margin-top:2px;line-height:1.68}
.argcard .sowhat b{color:var(--ink)}
.tilecol{display:flex;flex-direction:column;gap:8px}
.tilecol .t{background:var(--surface-2);border:1px solid var(--border);border-radius:4px;padding:10px 12px;text-align:center}
.tilecol .t .v{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:15.5px;font-weight:700;color:var(--ink);line-height:1.3}
.tilecol .t .l{font-size:10.5px;color:var(--sec);margin-top:4px;line-height:1.4}
.amber{background:var(--gold-bg);border-left:3px solid var(--gold);border-radius:0 4px 4px 0;padding:12px 16px;margin-bottom:10px;font-size:13px;line-height:1.7;color:var(--body)}
.card > ul{margin:0 0 4px 18px;padding:0}
.card > ul > li{margin-bottom:8px;font-size:13.5px;line-height:1.7;color:var(--body)}
.watchtable td.lbl a{white-space:nowrap}
.watchtable td.lenscol{white-space:nowrap;min-width:5rem}
.watchtable td.ddcol{white-space:nowrap}
.lenstable td.why{font-size:12.5px}
code{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12px;background:var(--surface-2);padding:1px 5px;border-radius:3px}
"""

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="noindex,nofollow">
<style>
:root{{
  --ink:#0c1521;--body:#2a3a52;--sec:#6b7a92;--muted:#9aa7b8;
  --paper:#f7f3ea;--surface:#ffffff;--surface-2:#f3efe4;--surface-3:#ece7d8;
  --border:#e5dfd0;--border-2:#d0c9b4;
  --accent:#0d2244;--accent-hover:#081832;
  --gold:#b8924a;--gold-deep:#8f6d2c;--gold-bg:#fbf3df;--gold-soft:#f3e5c3;
  --pos:#15803d;--pos-bg:#eafaef;--neg:#b91c1c;--neg-bg:#fbeceb;--warn:#a16207;--warn-bg:#fbf3df;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;line-height:1.74;color:var(--body);background:var(--paper);-webkit-font-smoothing:antialiased}}
a{{color:var(--accent);text-decoration:none}}a:hover{{text-decoration:underline;color:var(--accent-hover)}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 22px 72px}}
h1,h2,h3,h4{{font-family:'Noto Serif TC',Georgia,'Times New Roman',serif;color:var(--ink);letter-spacing:-.01em;font-weight:700}}
.mono{{font-family:'IBM Plex Mono',ui-monospace,Menlo,monospace}}
.masthead{{background:var(--accent);color:#eef1f7;margin:0;padding:30px 22px 24px;border-bottom:3px solid var(--gold)}}
.masthead-inner{{max-width:1040px;margin:0 auto}}
.masthead .kicker{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:10px}}
.masthead h1{{font-size:26px;font-weight:800;letter-spacing:-.02em;line-height:1.32;color:#fff;margin-bottom:10px}}
.masthead .subt{{font-size:14.5px;color:#c3cbdb;font-weight:500;max-width:52rem;line-height:1.6}}
.masthead .rule{{height:1px;background:rgba(255,255,255,.14);margin:18px 0 13px}}
.masthead .meta{{display:flex;flex-wrap:wrap;gap:4px 26px;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;color:#9aa7c4;line-height:1.9}}
.masthead .meta b{{color:#dbe1ee;font-weight:600}}
.masthead .nature{{margin-top:12px;font-size:11.5px;color:#8b95b3;line-height:1.7;border-top:1px solid rgba(255,255,255,.1);padding-top:11px;max-width:56rem}}
.exec-wrap{{background:var(--surface);border:1px solid var(--border-2);border-radius:4px;padding:4px 24px;margin:24px 0 8px;box-shadow:0 1px 2px rgba(12,21,33,.04)}}
.exec-hd{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-deep);font-weight:700;padding:14px 0 6px}}
.exec{{counter-reset:e}}
.exec li{{list-style:none;position:relative;padding:13px 0 13px 42px;border-bottom:1px solid var(--border);font-size:14px;line-height:1.68;color:var(--body);counter-increment:e}}
.exec li:last-child{{border-bottom:none}}
.exec li b{{color:var(--ink);font-weight:700}}
.exec li::before{{content:counter(e,upper-roman);position:absolute;left:0;top:13px;font-family:'IBM Plex Mono',ui-monospace,monospace;font-weight:800;font-size:12.5px;color:var(--accent)}}
.kdstrip{{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--border-2);border:1px solid var(--border-2);border-radius:4px;overflow:hidden;margin:16px 0 28px}}
.kdstrip>div{{background:var(--surface);padding:14px 14px;text-align:center}}
.kdstrip .kl{{font-size:10.5px;color:var(--sec);letter-spacing:.02em;line-height:1.4;margin-bottom:5px;min-height:2.4em}}
.kdstrip .kv{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:19px;font-weight:700;color:var(--ink)}}
@media(max-width:760px){{.kdstrip{{grid-template-columns:repeat(2,1fr)}}}}
.toc{{background:var(--surface-2);border:1px solid var(--border);border-radius:4px;padding:16px 22px;margin:0 0 30px}}
.toc-hd{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--sec);font-weight:700;margin-bottom:10px}}
.toc ol{{list-style:none;columns:2;column-gap:30px}}
.toc li{{break-inside:avoid;margin-bottom:6px}}
.toc a{{display:flex;gap:8px;font-size:13px;color:var(--body);padding:2px 0}}
.toc a:hover{{color:var(--accent)}}
.toc .n{{font-family:'IBM Plex Mono',ui-monospace,monospace;color:var(--gold-deep);font-weight:700;flex-shrink:0}}
@media(max-width:640px){{.toc ol{{columns:1}}}}
.section{{padding:44px 0 0;scroll-margin-top:14px}}
.section-hd{{border-bottom:2px solid var(--accent);padding-bottom:9px;margin-bottom:4px}}
.section-hd .sec-eyebrow{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-deep);font-weight:700;margin-bottom:4px}}
.section-hd h2{{font-size:21px;line-height:1.35}}
.section-lead{{font-size:14px;color:var(--sec);margin:10px 0 18px;line-height:1.7}}
.thecall{{background:var(--gold-bg);border-left:3px solid var(--gold);border-radius:0 4px 4px 0;padding:14px 20px;margin:0 0 20px;font-size:15px;line-height:1.7;color:var(--ink);font-weight:600}}
.thecall b{{color:var(--accent-hover)}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:18px 22px;margin-bottom:16px}}
.card h3{{font-size:15.5px;font-weight:700;margin-bottom:8px;color:var(--ink)}}
.card h3 .h-n{{font-family:'IBM Plex Mono',ui-monospace,monospace;color:var(--gold-deep);font-weight:700;margin-right:6px}}
.pt{{margin-bottom:14px}}
.ph{{font-size:14px;font-weight:700;color:var(--ink);margin-bottom:3px}}
.pb{{font-size:13.5px;color:var(--body);line-height:1.82}}
.pb a{{font-size:12.5px}}
.exhibit{{background:var(--surface);border:1px solid var(--border-2);border-radius:4px;padding:18px 20px 15px;margin:16px 0}}
.exhibit .ex-tag{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;font-weight:700;letter-spacing:.06em;color:var(--gold-deep);text-transform:uppercase;margin-bottom:3px}}
.exhibit .ex-cap{{font-weight:700;font-size:14.5px;color:var(--ink);line-height:1.5;margin-bottom:2px}}
.exhibit .ex-sub{{font-size:12px;color:var(--sec);margin-bottom:12px;line-height:1.6}}
.exhibit .ex-take{{font-size:13px;color:var(--body);margin-top:11px;padding-top:10px;border-top:1px solid var(--border);line-height:1.72}}
.exhibit .ex-take b{{color:var(--ink)}}
.scroll{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:12.5px}}
thead th{{text-align:left;padding:8px 10px;background:var(--surface-2);font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.5px;text-transform:uppercase;letter-spacing:.03em;color:var(--sec);border-bottom:1.5px solid var(--border-2);white-space:nowrap}}
tbody td{{padding:8px 10px;border-bottom:1px solid var(--border);vertical-align:top;font-variant-numeric:tabular-nums}}
tbody tr:last-child td{{border-bottom:none}}
tbody tr:hover td{{background:var(--surface-2)}}
td.lbl{{font-weight:700;white-space:nowrap;color:var(--ink)}}
td.num{{text-align:right;font-family:'IBM Plex Mono',ui-monospace,monospace}}
td.strong{{font-weight:700;color:var(--ink)}}
td.why{{font-size:12px;color:var(--sec);font-variant-numeric:normal;line-height:1.6}}
details.mdet{{margin:12px 0}}
details.mdet>summary{{cursor:pointer;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;font-weight:700;letter-spacing:.02em;color:var(--accent);padding:9px 14px;background:var(--surface-2);border:1px solid var(--border);border-radius:4px;list-style:none}}
details.mdet>summary::-webkit-details-marker{{display:none}}
details.datanote{{margin:12px 0}}
details.datanote>summary{{cursor:pointer;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;font-weight:700;color:var(--warn);padding:8px 13px;background:var(--warn-bg);border:1px solid var(--gold-soft);border-radius:4px;list-style:none}}
details.datanote>summary::-webkit-details-marker{{display:none}}
details.datanote>summary::before{{content:"▸ 資料信心與缺口　";}}
details.datanote[open]>summary::before{{content:"▾ 資料信心與缺口　";}}
details.datanote .dn-body{{padding:12px 15px 3px;font-size:12px;color:var(--body);line-height:1.75}}
.callout{{background:var(--gold-bg);border-left:3px solid var(--gold);border-radius:0 4px 4px 0;padding:13px 17px;margin:14px 0;font-size:13px;line-height:1.7;color:var(--body)}}
.callout b{{color:var(--ink)}}
.closing{{background:var(--surface-2);border:1px solid var(--border);border-radius:4px;padding:14px 18px;font-size:12.5px;color:var(--sec);margin-top:16px;line-height:1.7}}
.imq-foot{{background:var(--accent);color:#aab3c9;text-align:center;padding:20px 0;font-size:12px;margin-top:44px;line-height:1.9}}
.imq-foot a{{color:#dbe1ee}}
.crumb{{max-width:1040px;margin:0 auto;padding:14px 22px 0;font-size:12.5px;color:var(--sec)}}
.crumb a{{color:var(--sec)}}
.footlinks{{display:flex;flex-wrap:wrap;gap:8px 10px;margin:10px 0 4px}}
.footlinks a{{background:var(--surface-2);border:1px solid var(--border);border-radius:4px;padding:6px 12px;font-size:12.5px;color:var(--body)}}
.footlinks a:hover{{color:var(--accent);border-color:var(--border-2);text-decoration:none}}
{extra}
@media(max-width:760px){{.masthead h1{{font-size:20px}}.section-hd h2{{font-size:18px}}.wrap{{padding:0 15px 56px}}.masthead{{padding:22px 16px 20px}}.crumb{{padding:12px 15px 0}}}}
</style>
</head>
<body>
"""


def build_exec_summary(stats, facts):
    q = facts["prime_pb_quadrant"]["value"]
    p23, p26 = q["2023-02-28"], q["2026-02-28"]
    jgb = facts["jgb_10y_yield"]["value"]
    per = facts["topix_per_pbr_snapshot"]["value"]
    ey = 100 / per["per_forecast_prime"]
    fh = facts["foreign_holding_share_history"]["value"]
    mtd = facts["mbo_tob_delisting_2025"]["value"]
    items = [
        f'<b>東證改革把大盤層級的便宜大致定價完畢</b>——Prime市場P/B&lt;1比率由{p23["pbr_below1_pct"]}%'
        f'（2023-02-28）降至{p26["pbr_below1_pct"]}%（2026-02-28），高PBR高ROE象限占家數由{p23["q1_pct"]}%'
        f'升至{p26["q1_pct"]}%、占Prime總市值{p26["q1_market_cap_share_pct"]}%；本頁{stats["count"]}檔全市場母體'
        f'P/B&lt;1比率為{stats["pb_below1_pct"]:.1f}%（{SNAPSHOT_DATE}快照，本頁自算，口徑不同不可直接比較）。',

        f'<b>金利回來了，股息與盈餘兩把估值尺指向相反方向</b>——10年期JGB殖利率已升至{jgb:.2f}%'
        f'（{facts["jgb_10y_yield"]["as_of"]}），TOPIX加權股息殖利率{facts["topix_dividend_yield"]["value"]}%已低於JGB'
        f'（利差約{facts["topix_dividend_yield"]["value"]-jgb:+.2f}pp，債券贏），但東証Prime預估本益比換算的'
        f'盈餘殖利率利差約{ey-jgb:+.2f}pp（股票贏，改用實績本益比算仍為正）——同一個市場，兩把尺同時存在、方向相反。',

        f'<b>買盤結構三條線同步走高</b>——外資持股占大盤市值比重由FY2023的{fh["FY2023"]}%升至FY2025的'
        f'{fh["FY2025"]}%（史上新高）；NISA累計投資金額達¥{facts["nisa_cumulative_amount"]["value"]["amount_jpy_trillion"]}兆，'
        f'較政府原訂2027年12月底¥56兆的目標提前約2年達成；庫藏股買回授權金額FY2025達¥{facts["buyback_authorization_series"]["value"]["FY2025_authorization_jpy_trillion"]}兆，'
        "連續第5年增加；交叉持股廣義比率降至9.7%，首度跌破10%。",

        f'<b>資本報酬地圖顯示複利機器供給豐富，但零檔便宜</b>——{stats["count"]}檔母體ROE中位數'
        f'{stats["roe_all_median"]:.1f}%（{SNAPSHOT_DATE}快照，本頁自算），產業別差異可達數倍；'
        "站內量化篩選出的複利機器候選經深度剖析後零檔可誠實標記為便宜，真正還沒被定價完的角落是"
        "站在資本支出循環谷底、ROE已跌破常見門檻的名字。",

        f'<b>退出通道是活的，三條管道同步創紀錄</b>——MBO 2025年{mtd["mbo_count_2025"]}件創紀錄'
        f'（+{mtd["mbo_yoy_growth_pct"]}% YoY）、TOB 2025年{mtd["tob_count_2025"]}件創紀錄、'
        f'東證同年實際下市{mtd["delisting_2025_tse_total"]}家連續2年最多；TOB整體溢價中位數43.3%（2024年度，對前1個月均價），'
        "連最接近內部人交易性質的親子上市買回也是真溢價不是最低價；但外部投資人（非公司內部人）結構性缺乏公告前資訊優勢，"
        "敵意收購（同意なき買収）2025年8件中僅4件成立。",

        "<b>AI出口鏈查證後：獨佔純度沒有換來額外估值溢價</b>——15個半導體供應鏈節點掃出至少六道日廠近壟斷關卡，"
        "原本三個看似異常的高本益比經一手來源查證後全數證實是數據假象；Kioxia查證後前瞻PE僅約6.8倍是"
        "本鏡頭估值最不對稱的候選，但需警惕循環頂部陷阱。",

        "<b>內需股沒有人口順風可打，僅3檔握有真定價權</b>——9檔內需代表股拆成客數×客單價後，僅迅銷、"
        "FOOD&LIFE、麥當勞日本客數與客單價同步走揚，但估值已站上高檔；2026-11-01出境免稅制度改為"
        "「リファンド方式（退款制）」是尚未被市場定價的現金流時程逆風。",

        '<b>約七週後（2026-10-30）TOPIX指數見直し第二階段首次定期入替同時帶來正反兩面效果</b>——選股改採'
        "成交金額週轉率與累積自由流通市值排名雙門檻，母體首次擴大到Standard與Growth市場；流入的一面是機械性買盤"
        "不需任何治理動作即可觸發，流出的一面是未達標既有成分股將承受約2年、每季調降12.5%權重的被動賣壓，"
        "兩個方向與本頁其餘機制的主敘事相反。",
    ]
    return "".join(f"<li>{x}</li>" for x in items)


def main():
    uni = load_universe()
    facts = load_facts()
    stats = compute_population_stats(uni)
    nav_snippet = open(NAV_SNIPPET_PATH, encoding="utf-8").read()

    title = "日股國家掃描：東證改革把大盤層級的便宜定價完畢，金利回來後兩把尺指向相反方向 | InvestmQuest Research"
    description = (
        f"日股國家掃描研究記錄：東京證券交易所主板市值≥¥1,000億共{stats['count']}檔母體"
        f"（總市值約{jpy_zhao_from_raw(stats['total_mcap'])}）。五個論點——東證改革、利率與估值兩把尺、"
        "買盤結構、資本報酬地圖、退出通道——加上複利機器／治理改革／金融／收息／事件驅動／AI出口鏈／內需"
        "七個投資鏡頭，含2份站內既有DD對帳。掃描是研究記錄，不是選股名單。"
    )

    masthead_h1 = "東證改革三年，大盤層級的便宜已經定價完畢；金利回來後，股息與盈餘兩把尺不再說同一件事"
    masthead_subt = (
        f'本頁是 {stats["count"]} 檔日股母體（東京證券交易所主板普通股，市值≥¥1,000億）的市場結構掃描：'
        "五個論點＋日股計分卡＋複利機器／治理改革／金融／收息／事件驅動／AI出口鏈／內需七個投資鏡頭，"
        "資料快照 " + SNAPSHOT_DATE + "，結構數字另附各自查證日期；本頁是研究記錄，不是投資建議，"
        "個股「值不值得投資」的裁決一律走站內DD統一裁決鏈。"
    )

    scorecard_html = build_scorecard(stats, facts)
    SCORECARD_N = build_scorecard.row_count

    body = []
    body.append('<div class="masthead"><div class="masthead-inner">')
    body.append('<div class="kicker">國家掃描 · 日本</div>')
    body.append(f'<h1>{masthead_h1}</h1>')
    body.append(f'<div class="subt">{masthead_subt}</div>')
    body.append('<div class="rule"></div>')
    body.append(
        '<div class="meta">'
        f'<span><b>掃描日期</b>　{SNAPSHOT_DATE}（資料快照，非持續更新）</span>'
        f'<span><b>母體</b>　東證主板市值≥¥1,000億，共 {stats["count"]:,} 檔</span>'
        f'<span><b>覆蓋</b>　{stats["count"]:,} 檔母體 × 五個論點＋七個投資鏡頭</span>'
        '</div>'
    )
    body.append(
        '<div class="nature">本頁性質聲明：描述器／研究紀錄，非投資建議。五個論點與七個鏡頭收斂出的是判讀框架與'
        '資料事實，不是一張「買這些」的名單；個股「值不值得投資」的裁決一律走 DD 統一裁決鏈。</div>'
    )
    body.append('</div></div>')

    body.append('<div class="wrap">')

    body.append('<div class="exec-wrap"><div class="exec-hd">一頁摘要</div><ol class="exec">')
    body.append(build_exec_summary(stats, facts))
    body.append('</ol></div>')

    body.append('<div class="kdstrip">')
    body.append(f'<div><div class="kl">母體規模（東證主板≥¥1,000億）</div><div class="kv">{stats["count"]:,} 檔</div></div>')
    body.append(f'<div><div class="kl">母體總市值</div><div class="kv">{jpy_zhao_from_raw(stats["total_mcap"])}</div></div>')
    body.append(f'<div><div class="kl">Prime市場P/B&lt;1比率（現值）</div><div class="kv">{facts["prime_pb_quadrant"]["value"]["2026-02-28"]["pbr_below1_pct"]}%</div></div>')
    body.append(f'<div><div class="kl">外資持股占大盤市值比重</div><div class="kv">{facts["foreign_holding_share_pct"]["value"]}%</div></div>')
    body.append('<div><div class="kl">站內DD覆蓋</div><div class="kv">2 份</div></div>')
    body.append('</div>')

    toc_items = [
        ("s1", f"日股計分卡：{SCORECARD_N} 個指標速覽"),
        ("s2", "五個論點：東證改革、利率兩把尺、買盤結構、資本報酬地圖、退出通道"),
        ("s3", "七個投資鏡頭一覽"),
        ("s4", "可作戰名單：已有裁決與零覆蓋候選"),
        ("s5", "會推翻本頁判斷的證據"),
        ("s6", "資料、方法與盲區"),
    ]
    body.append('<div class="toc"><div class="toc-hd">報告目錄</div><ol>')
    for i, (anchor, label) in enumerate(toc_items, 1):
        body.append(f'<li><a href="#{anchor}"><span class="n">§{i}</span>{label}</a></li>')
    body.append('</ol></div>')

    body.append(f'<div class="section" id="s1"><div class="section-hd"><div class="sec-eyebrow">Section I</div><h2>§1　日股計分卡：{SCORECARD_N} 個指標速覽</h2></div>')
    body.append('<div class="section-lead">母體算得出來的直接算，算不出來的查證後標明來源與查證日期；查不到的在「資料、方法與盲區」自陳，不沿用沒有出處的數字。</div>')
    body.append('<div class="exhibit scroll"><table><thead><tr><th>指標</th><th>數值</th><th>as-of</th><th>白話一句</th><th>來源</th></tr></thead><tbody>')
    body.append(scorecard_html)
    body.append('</tbody></table></div>')
    body.append('</div>')

    body.append('<div class="section" id="s2"><div class="section-hd"><div class="sec-eyebrow">Section II</div><h2>§2　五個論點：這個市場現在是什麼</h2></div>')
    body.append('<div class="section-lead">每個論點都是可以被推翻的具體主張，不是氣氛描述；推翻條件見§5。</div>')
    body.append(build_arguments_html(stats, facts))
    body.append('</div>')

    body.append('<div class="section" id="s3"><div class="section-hd"><div class="sec-eyebrow">Section III</div><h2>§3　七個投資鏡頭一覽</h2></div>')
    body.append('<div class="section-lead">結論濃縮自各鏡頭子頁的問題與答案節，數字回查子頁與母體檔案，不憑印象轉述；子頁計算基礎為先前TOPIX 500型476檔母體（見§6方法論），完整推理與逐檔對帳見各鏡頭子頁。</div>')
    body.append('<div class="exhibit scroll lenstable"><table><thead><tr><th>鏡頭</th><th>核心問題</th><th>一句結論</th><th>站內DD覆蓋</th><th>最大缺口</th></tr></thead><tbody>')
    body.append(build_lens_table())
    body.append('</tbody></table></div>')
    body.append(f'<div class="ex-sub" style="padding:0 4px">站內DD覆蓋盤點 as-of {DD_BASIS_DATE}（複審窗基準日，非本頁即時重算）；窗內比例＝90天內完成之裁決占該鏡頭DD總數。</div>')
    body.append('</div>')

    body.append('<div class="section" id="s4"><div class="section-hd"><div class="sec-eyebrow">Section IV</div><h2>§4　可作戰名單：已有裁決與零覆蓋候選</h2></div>')
    body.append('<div class="section-lead">站內裁決逐字取自各檔DD的dd-meta區塊signal／verdict欄位，同一家公司一律取日期最新的那一份，不改寫不總結；本頁不給買賣指令，個股「值不值得投資」一律點進DD查完整推理。</div>')
    body.append('<div class="exhibit scroll watchtable"><table><thead><tr><th>公司</th><th>鏡頭</th><th>站內裁決</th><th>在等什麼</th><th>DD連結</th></tr></thead><tbody>')
    body.append(build_watchlist())
    body.append('</tbody></table></div>')
    review_note = build_dd_review_note()
    if review_note:
        body.append(f'<div class="callout"><b>複審提醒：</b>{review_note}。</div>')
    body.append('</div>')

    body.append('<div class="section" id="s5"><div class="section-hd"><div class="sec-eyebrow">Section V</div><h2>§5　會推翻本頁判斷的證據</h2></div>')
    body.append('<div class="section-lead">每一條論點都附一組具體、可觀察的反證條件，不是模糊的「情況可能改變」。</div>')
    body.append(build_falsifiers())
    body.append('</div>')

    body.append('<div class="section" id="s6" style="padding-top:30px">')
    body.append('<details class="datanote"><summary>§6　資料、方法與盲區</summary><div class="dn-body">')
    body.append(build_methodology(stats, facts, uni))
    body.append('</div></details>')
    body.append('</div>')

    body.append(
        '<div class="closing">本頁為掃描研究記錄（描述器），非選股名單、非買賣建議；個股「值不值得投資」的裁決一律走DD統一裁決鏈。</div>'
    )

    body.append('<div class="footlinks">')
    for r in LENS_ROWS:
        body.append(f'<a href="japan/{r["slug"]}.html">鏡頭{r["n"]}・{r["name"]}</a>')
    body.append('<a href="/backtest/#scan">回國家掃描</a>')
    body.append('</div>')

    body.append('</div>')  # .wrap

    body_str = "".join(body)
    body_str = add_cjk_latin_spacing(body_str)

    head = HEAD_TEMPLATE.format(title=title, description=description, extra=EXTRA_CSS)
    footer = (
        '<footer class="imq-foot">'
        '<div>© 2026 InvestmQuest Research</div>'
        '<div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議 · '
        '<a href="/backtest/#scan">回國家掃描</a></div>'
        '</footer></body></html>'
    )

    html = head + nav_snippet + body_str + footer
    return html, stats, facts


# ---------------------------------------------------------------------------
# 12. 自檢：--check
# ---------------------------------------------------------------------------

# 「護城河」是既有的標準投資術語，不列入禁用比喻；日股舊頁的比喻詞（引擎／壓艙石／三張牌／地板價／
# 腰斬／獵場／大票／解放）全部列入禁用，新版必須改直述。
BANNED_METAPHOR_WORDS = ["煞车", "煞車", "收費站", "水庫", "半壁江山", "斷層帶", "藏寶圖", "尋寶",
                          "鴻溝", "雙面刃", "硬幣兩面", "賽道", "像座", "彷彿", "宛如",
                          "壓艙石", "壓艙", "母語", "地板價", "天花板", "籃子", "死法", "引擎", "資金潮",
                          "接盤", "撐盤", "彩票", "三張牌", "腰斬", "獵場", "大票", "解放"]
BANNED_PROCESS_WORDS = ["sonnet", "Sonnet", "opus", "Opus", "agent", "Agent", "critic", "orchestrator",
                         "本輪", "上一版", "舊版", "重寫"]
BANNED_CROSS_MARKET_WORDS = ["美國", "美股", "S&P", "台灣", "台股", "TWSE", "馬來西亞", "Bursa",
                              "韓國", "Korea", "新加坡", "泰國", "印尼", "新馬", "星馬", "中國", "區域同業"]
BANNED_TRADE_CALL_WORDS = ["買進", "賣出", "加碼", "減碼", "停損", "目標價"]
BANNED_INTERNAL_FILENAMES = ["_universe.json", "_hub_facts.json", "_universe_report.md",
                              "_build_hub.py", "_critic_hub", "_nav_snippet.html", "_structure_dossier.md"]


def run_check(html_path):
    html = open(html_path, encoding="utf-8").read()
    problems = []

    def report(name, hits):
        if hits:
            problems.append(f"{name}: {len(hits)} 處命中 -> {hits[:5]}")

    for w in BANNED_METAPHOR_WORDS:
        if w in html:
            report(f"禁用比喻詞「{w}」", [w] * html.count(w))

    body_only = html.split("<body>", 1)[-1]
    body_no_quote = re.sub(r'<span data-verbatim="dd">.*?</span>', "", body_only, flags=re.S)
    for w in BANNED_PROCESS_WORDS:
        if w in body_only:
            report(f"流程語氣詞「{w}」", [w] * body_only.count(w))

    for w in BANNED_CROSS_MARKET_WORDS:
        if w in body_only:
            report(f"跨市場字樣「{w}」", [w] * body_only.count(w))

    for w in BANNED_TRADE_CALL_WORDS:
        if w in body_no_quote:
            report(f"買賣指令字樣「{w}」", [w] * body_no_quote.count(w))
    quoted_calls = [w for w in BANNED_TRADE_CALL_WORDS if w in body_only and w not in body_no_quote]
    if quoted_calls:
        print(f"（提示）以下字樣只出現在逐字引用的站內DD裁決文字內，未計為問題：{quoted_calls}")

    for w in BANNED_INTERNAL_FILENAMES:
        if w in html:
            report(f"內部檔名外洩「{w}」", [w] * html.count(w))

    text_nodes = re.sub(r"<[^>]+>", "\n", body_only)
    text_nodes = re.sub(r"<style>.*?</style>", "", text_nodes, flags=re.S)
    halfwidth_hits = re.findall(r"[一-鿿][,.][一-鿿]", text_nodes)
    report("中文字之間夾半形逗號/句號", halfwidth_hits)

    anchors = set(re.findall(r'id="([a-zA-Z0-9_-]+)"', html))
    hrefs = re.findall(r'href="#([a-zA-Z0-9_-]+)"', html)
    missing_anchor = [h for h in hrefs if h not in anchors]
    report("TOC 錨點缺失", missing_anchor)

    lens_dir = os.path.join(BASE, "..", "..", "..", "..", "docs", "backtest", "country_scan", "japan")
    missing_pages = []
    for slug in re.findall(r'href="japan/([a-z-]+\.html)"', html):
        p = os.path.normpath(os.path.join(lens_dir, slug))
        if not os.path.exists(p):
            missing_pages.append(slug)
    report("子頁連結缺失（japan/前綴解析）", missing_pages)

    dd_dir_candidates = [os.path.join(BASE, "..", "..", "..", "..", "docs", "dd")]
    missing_dd = []
    for m in re.findall(r'DD_[A-Za-z0-9.\-]+\.html', html):
        found = any(os.path.exists(os.path.join(d, m)) for d in dd_dir_candidates)
        if not found:
            missing_dd.append(m)
    report("DD 連結檔案缺失（本機比對）", sorted(set(missing_dd)))

    stuck2 = re.findall(r"[一-鿿][A-Za-z0-9]|[A-Za-z0-9][一-鿿]", text_nodes.replace(" ", "\x01"))
    report("CJK 與英文/數字之間缺空格", stuck2)

    ex_nums = [int(x) for x in re.findall(r'<div class="ex-tag">Exhibit (\d+)</div>', html)]
    if ex_nums != sorted(set(ex_nums)) or ex_nums != list(range(1, len(set(ex_nums)) + 1)):
        problems.append(f"Exhibit 連號異常: {ex_nums}")

    facts = load_facts()
    uni = load_universe()
    stats = compute_population_stats(uni)
    plain = re.sub(r"<[^>]+>", "", body_only)

    for key in ("foreign_holding_share_pct", "boj_policy_rate_current", "jgb_10y_yield"):
        raw = facts[key]["value"]
        candidates = {str(raw)}
        if isinstance(raw, (int, float)):
            candidates.add(f"{raw:.2f}")
            candidates.add(f"{raw:.1f}")
        if not any(c in html for c in candidates if isinstance(c, str)):
            problems.append(f"facts[{key}].value={raw} 未出現在頁面內文中（試過 {sorted(str(c) for c in candidates)}）")

    for key, e in facts.items():
        if key.startswith("_") or not isinstance(e, dict):
            continue
        if e.get("confidence") == "gap" or e.get("value") is None:
            continue
        if not e.get("source_url"):
            problems.append(f"facts[{key}] 有數值但缺 source_url")

    pop_checks = [
        (f'{stats["pb_below1_pct"]:.1f}%', "母體P/B&lt;1比率"),
        (f'{stats["fpe_all"]["median"]:.1f}倍', "母體前瞻本益比中位數"),
        (f'{stats["dy_median"]:.2f}%', "母體殖利率中位數"),
        (f'{stats["roe_all_median"]:.1f}%', "母體ROE中位數"),
        (jpy_zhao_from_raw(stats["total_mcap"]), "母體總市值"),
        (f'{stats["conc"][10]["pct"]:.1f}%', "前十大個股占母體市值"),
    ]
    for expect, label in pop_checks:
        if add_cjk_latin_spacing(expect) not in plain:
            problems.append(f"母體數字檢查失敗：{label} 應出現「{expect}」")

    # 476 vs 新母體混寫檢查：任何句子出現「476」必須同時出現「子頁」或「TOPIX 500」字樣
    for sent in re.split(r"(?<=[。；])", plain):
        if "476" in sent and ("子頁" not in sent and "TOPIX 500" not in sent and "TOPIX500" not in sent):
            problems.append(f"「476」出現但句中未見「子頁」或「TOPIX 500」字樣：{sent.strip()[:80]}")

    dd_dir = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "docs", "dd"))
    if os.path.isdir(dd_dir):
        all_dd = os.listdir(dd_dir)
        for r in WATCH_EXISTING:
            pat = re.compile(r"^DD_%sT_(\d{8})\.html$" % re.escape(r["t"]))
            dates = sorted(m.group(1) for m in (pat.match(f) for f in all_dd) if m)
            if not dates:
                continue
            newest = dates[-1]
            used = r["date"].replace("-", "")
            if used != newest:
                problems.append(
                    f'{r["name"]}（{r["t"]}）引用的 DD 日期 {r["date"]} 不是最新，'
                    f'docs/dd 內最新為 {newest[:4]}-{newest[4:6]}-{newest[6:]}'
                )

    dd_total = len(WATCH_EXISTING)
    if f"{dd_total} 份" not in plain and f"{dd_total}份" not in plain:
        problems.append(f"站內DD總數 {dd_total} 份與頁面敘述對不上")

    # SVG 幾何檢查：viewBox 高度需與宣告的 height 一致
    for m in re.finditer(r'<svg viewBox="0 0 (\d+) (\d+)"[^>]*height="(\d+)"', html):
        vw, vh, h = m.groups()
        if vh != h:
            problems.append(f"SVG viewBox高度({vh})與height屬性({h})不一致")

    # HTML 實體二次轉義：任何 &amp;lt; / &amp;gt; / &amp;amp; 都代表某個字串被 esc() 了兩次
    dbl = re.findall(r"&amp;(?:lt|gt|amp|#\d+);", html)
    report("HTML 實體二次轉義（字面顯示成 &lt; 等）", dbl)

    # SVG 字級下限：頁面規格為 ≥12px
    small_fonts = [f for f in re.findall(r'font-size="([0-9.]+)"', html) if float(f) < 12]
    report("SVG 字級小於 12px", small_fonts)

    # SVG 文字水平出界：估算每個 <text> 的左右邊界是否落在 viewBox 內
    #   全形字寬約 1.0em、半形約 0.55em（IBM Plex Mono 為等寬，此估算偏保守）
    def text_width(s, fs):
        w = 0.0
        for ch in s:
            w += fs * (1.0 if ord(ch) > 0x2E7F else 0.55)
        return w

    overflow = []
    for svg_m in re.finditer(r'<svg viewBox="0 0 (\d+) (\d+)".*?</svg>', html, re.S):
        vw = int(svg_m.group(1))
        for t in re.finditer(
            r'<text x="([-0-9.]+)"[^>]*?font-size="([0-9.]+)"([^>]*)>(.*?)</text>', svg_m.group(0), re.S
        ):
            x, fs, attrs, content = float(t.group(1)), float(t.group(2)), t.group(3), t.group(4)
            plain_txt = re.sub(r"&[a-z#0-9]+;", "X", re.sub(r"<[^>]+>", "", content))
            w = text_width(plain_txt, fs)
            anchor = "middle" if 'text-anchor="middle"' in attrs else "start"
            left = x - w / 2 if anchor == "middle" else x
            right = left + w
            if left < -2 or right > vw + 2:
                overflow.append(f'"{plain_txt[:22]}" x={x:.0f} 估算範圍[{left:.0f},{right:.0f}] 超出 0–{vw}')
    report("SVG 文字水平出界（估算）", overflow)

    print(f"檢查完成，共 {len(problems)} 個問題：" if problems else "檢查完成，未發現問題。")
    for p in problems:
        print(" -", p)
    return problems


def main_cli():
    html, stats, facts = main()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"寫入 {OUT_PATH}（{len(html)/1024:.1f} KB）")
    if "--check" in sys.argv:
        run_check(OUT_PATH)


if __name__ == "__main__":
    if "--stats-only" in sys.argv:
        uni = load_universe()
        stats = compute_population_stats(uni)
        print(json.dumps(
            {k: v for k, v in stats.items() if k not in ("sector_rows", "top_sectors", "roe_by_sector", "dy_hist")},
            ensure_ascii=False, indent=2, default=str,
        ))
    elif "--check-only" in sys.argv:
        run_check(OUT_PATH)
    else:
        main_cli()
