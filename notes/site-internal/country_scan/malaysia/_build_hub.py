#!/usr/bin/env python3
"""
馬股國家掃描 hub 組裝腳本（重寫 2026-09-10）。

Usage:
  /opt/homebrew/bin/python3.12 _build_hub.py            # 產出 docs/backtest/country_scan/malaysia.html
  /opt/homebrew/bin/python3.12 _build_hub.py --check    # 產出後跑自檢，不重新寫檔亦可單獨執行

只用標準庫（json / statistics / math / re / os）。母體數字一律從 _universe.json 現算；
非母體的結構數字（外資持股、OPR、令吉匯率、私有化件數、控股折價……）一律從 _hub_facts.json
讀取，每筆都帶 value / as_of / source_name / source_url / confidence，禁止在內文手打數字。
本檔照 notes/site-internal/country_scan/taiwan/_build_hub.py 的結構與機制複製，母體欄位改為
馬股口徑（market_cap_myr／yahoo_sector）；馬來西亞沒有子頁，四個投資鏡頭改成鏡頭卡直接嵌在
本頁（見 build_lenses()），鏡頭卡內的具名個股事實與出處全部承接自舊版 malaysia.html。
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
OUT_PATH = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "docs", "backtest", "country_scan", "malaysia.html"))

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


def myr_yi_from_raw(v):
    """原始令吉數字 -> 「RMx億」（億=1e8）或「RMx,xxx億」。"""
    yi = v / 1e8
    return f"RM{yi:,.0f}億"


def myr_bn_from_raw(v):
    """原始令吉數字 -> 「RMx.xx十億」（給小數字用，如個股市值）。"""
    return f"RM{v/1e9:,.2f}十億"


def myr_zhao_from_raw(v):
    """原始令吉數字 -> 「RMx.xx兆」（兆=1e12，給母體總市值等大數字用）。"""
    return f"RM{v/1e12:,.2f}兆"


def days_between(d1, d2):
    a = datetime.date.fromisoformat(d1)
    b = datetime.date.fromisoformat(d2)
    return (b - a).days


# ---------------------------------------------------------------------------
# 2. 母體統計（全部從 _universe.json 現算）
# ---------------------------------------------------------------------------

TOP_SECTOR_N = 10


def compute_population_stats(uni):
    cons = uni["constituents"]
    total_mcap = sum(c["market_cap_myr"] for c in cons if c.get("market_cap_myr"))
    count = len(cons)

    srt = sorted(cons, key=lambda c: -(c.get("market_cap_myr") or 0))

    def topn_share(n):
        s = sum(c["market_cap_myr"] for c in srt[:n])
        return s, s / total_mcap * 100

    conc = {}
    for n in (1, 5, 10, 20):
        s, p = topn_share(n)
        conc[n] = {"mcap": s, "pct": p}
    conc["rest"] = {"pct": 100 - conc[20]["pct"]}
    top10_names = [f'{c["name"]}（{c["code"]}）' for c in srt[:10]]

    # yahoo_sector 市值與檔數分布
    sec = defaultdict(float)
    seccount = defaultdict(int)
    for c in cons:
        k = c.get("yahoo_sector") or "未分類"
        mc = c.get("market_cap_myr") or 0
        sec[k] += mc
        seccount[k] += 1
    sector_rows = sorted(
        ({"sector": k, "mcap": v, "pct": v / total_mcap * 100, "n": seccount[k]} for k, v in sec.items()),
        key=lambda r: -r["pct"],
    )
    top_sectors = sector_rows[:TOP_SECTOR_N]
    rest_sector_pct = 100 - sum(r["pct"] for r in top_sectors)
    rest_sector_n = count - sum(r["n"] for r in top_sectors)

    fin_row = next((r for r in sector_rows if r["sector"] in ("Financial Services", "Financials")), None)
    fin_n = fin_row["n"] if fin_row else 0
    fin_pct = fin_row["pct"] if fin_row else 0.0
    fin_count_pct = fin_n / count * 100 if fin_row else 0.0

    def pe_quartiles(group, field="forward_pe"):
        vals = sorted(c[field] for c in group if c.get(field) is not None and c[field] > 0)
        n = len(vals)
        if n == 0:
            return None
        return {"n": n, "median": st.median(vals), "q1": vals[n // 4], "q3": vals[(3 * n) // 4]}

    fpe_all = pe_quartiles(cons)
    tpe_all_vals = sorted(c["trailing_pe"] for c in cons if c.get("trailing_pe") is not None and c["trailing_pe"] > 0)
    tpe_all_median = st.median(tpe_all_vals) if tpe_all_vals else None

    # 前 6 大產業別（依市值）的前瞻本益比四分位＋強制納入 Technology（出口科技群所在分類，
    # 市值占比未進前6大，但論點C具名個股皆屬此分類，強制納入避免估值分裂圖漏掉主角）
    pe_sector_names = [r["sector"] for r in top_sectors[:6]]
    if "Technology" not in pe_sector_names:
        pe_sector_names.append("Technology")
    sector_pe_rows = []
    for name in pe_sector_names:
        group = [c for c in cons if (c.get("yahoo_sector") or "未分類") == name]
        pq = pe_quartiles(group)
        if pq:
            sector_pe_rows.append({"sector": name, "n_pe": pq["n"], **pq})

    roe_all = [c["roe"] * 100 for c in cons if c.get("roe") is not None]
    roe_all_median = st.median(roe_all) if roe_all else None

    dy_all_vals = [c["dividend_yield"] for c in cons if c.get("dividend_yield") is not None]
    dy_median = st.median(dy_all_vals) if dy_all_vals else None
    dy_buckets_def = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (8, 9999)]
    dy_hist = []
    for lo, hi in dy_buckets_def:
        n = sum(1 for v in dy_all_vals if lo <= v < hi)
        label = f"{lo}–{hi}%" if hi < 9999 else f"≥{lo}%"
        dy_hist.append({"label": label, "n": n})
    dy_no_dividend = count - len(dy_all_vals)
    dy6 = [v for v in dy_all_vals if v >= 6]

    return {
        "count": count,
        "total_mcap": total_mcap,
        "conc": conc,
        "top10_names": top10_names,
        "sector_rows": sector_rows,
        "top_sectors": top_sectors,
        "rest_sector_pct": rest_sector_pct,
        "rest_sector_n": rest_sector_n,
        "fin_n": fin_n,
        "fin_pct": fin_pct,
        "fin_count_pct": fin_count_pct,
        "fpe_all": fpe_all,
        "tpe_all_median": tpe_all_median,
        "sector_pe_rows": sector_pe_rows,
        "roe_all_median": roe_all_median,
        "dy_median": dy_median,
        "dy_hist": dy_hist,
        "dy_no_dividend": dy_no_dividend,
        "dy6_n": len(dy6),
        "dy6_pct": len(dy6) / count * 100,
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

# Yahoo 產業分類的中譯（頁面圖表一律顯示中文；英文原名在圖註一次列出對照）
SECTOR_ZH = {
    "Financial Services": "金融服務",
    "Industrials": "工業",
    "Consumer Defensive": "必需消費",
    "Utilities": "公用事業",
    "Basic Materials": "基礎材料",
    "Communication Services": "通訊服務",
    "Real Estate": "不動產",
    "Healthcare": "醫療保健",
    "Consumer Cyclical": "非必需消費",
    "Energy": "能源",
    "Technology": "科技",
    "未分類": "未分類",
}


def sec_zh(name):
    return SECTOR_ZH.get(name, name)


def sector_legend(rows):
    """圖註用的中英對照字串（只列出圖上出現過的分類）。"""
    pairs = [f"{sec_zh(r['sector'])} {r['sector']}" for r in rows if r["sector"] in SECTOR_ZH and r["sector"] != "未分類"]
    return "／".join(pairs)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_wrap(inner, height, label):
    return (
        f'<svg viewBox="0 0 {SVG_W} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}" '
        f'style="display:block;font-family:\'IBM Plex Mono\',ui-monospace,monospace">{inner}</svg>'
    )


def svg_exhibit_a(facts):
    """論點A：KLCI年度價格報酬長條＋累積價格指數線（2015-06-30=100）。"""
    yearly = facts["klci_yearly_close"]["value"]
    years = sorted(int(y) for y in yearly)
    base = facts["klci_10y_price_return_pct"]  # noqa: F841 (保留供之後擴充引用)
    base_val = None
    idx_vals = {}
    # 以2015-06-30收盤（1,706.64）為基期100，逐年12月31日收盤換算指數
    base_close = 1706.64
    for y in years:
        idx_vals[y] = yearly[str(y)] / base_close * 100

    bar_x, top = 24, 40
    chart_w = SVG_W - 48
    row_h = 150
    n = len(years) - 1  # 2016起才有年度報酬
    ret_years = years[1:]
    bw = chart_w / len(ret_years) - 10
    max_abs = max(abs(idx_vals[y] / idx_vals[y - 1] * 100 - 100) for y in ret_years)
    parts = [
        f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">'
        "KLCI 日曆年價格報酬（各年 12/31 收盤對前一年 12/31，不含股息）</text>"
    ]
    zero_y = top + row_h / 2
    parts.append(f'<line x1="{bar_x}" y1="{zero_y:.1f}" x2="{bar_x+chart_w:.1f}" y2="{zero_y:.1f}" stroke="{C_BORDER}" stroke-width="1"/>')
    x = bar_x
    for y in ret_years:
        r = idx_vals[y] / idx_vals[y - 1] * 100 - 100
        h = (row_h / 2 - 10) * abs(r) / max_abs
        color = C_POS if r >= 0 else C_NEG
        if r >= 0:
            ry = zero_y - h
        else:
            ry = zero_y
        parts.append(f'<rect x="{x:.1f}" y="{ry:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2" fill="{color}"/>')
        ty = zero_y - h - 6 if r >= 0 else zero_y + h + 14
        parts.append(f'<text x="{x+bw/2:.1f}" y="{ty:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{r:+.1f}%</text>')
        label = f"{y}" if y < 2026 else "2026\nYTD"
        for j, seg in enumerate(label.split("\n")):
            parts.append(f'<text x="{x+bw/2:.1f}" y="{top+row_h+16+j*13:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{esc(seg)}</text>')
        x += bw + 10
    y0 = top + row_h + 36
    latest = facts["klci_latest_snapshot"]["value"]
    h2_2015 = yearly["2015"] / base_close * 100 - 100
    parts.append(
        f'<text x="{bar_x}" y="{y0+18:.1f}" font-size="12.5" fill="{C_GOLD_DEEP}" font-weight="700">'
        f'累積價格指數（2015-06-30 收盤 {base_close:,.2f} 點＝100）：2025-06-30 為 '
        f'{100+facts["klci_10y_price_return_pct"]["value"]:.1f}'
        f'　最新（{latest["date"]}）收盤 {latest["close"]:,.2f} 點，指數＝{100+latest["price_return_since_2015q2_pct"]:.1f}'
        "</text>"
    )
    parts.append(
        f'<text x="{bar_x}" y="{y0+38:.1f}" font-size="12" fill="{C_SEC}">'
        f'長條為日曆年報酬（各年 12/31 對前一年 12/31），第一根是 2016 年；'
        f'2026 年長條為年初至 {latest["date"]}，非全年。</text>'
    )
    parts.append(
        f'<text x="{bar_x}" y="{y0+56:.1f}" font-size="12" fill="{C_SEC}">'
        f'累積指數的基期日是 2015-06-30；該日到 2015-12-31 的 {h2_2015:+.1f}% 只計入累積指數，不單獨畫長條。</text>'
    )
    total_h = y0 + 72
    return svg_wrap("".join(parts), total_h, "KLCI年度價格報酬與累積價格指數")


def svg_exhibit_b(stats):
    """論點B：母體市值集中度累積占比＋前10大產業別市值長條。"""
    conc = stats["conc"]
    segs = [
        ("第1檔", conc[1]["pct"], C_ACCENT),
        ("第2–5檔", conc[5]["pct"] - conc[1]["pct"], C_ACCENT2),
        ("第6–10檔", conc[10]["pct"] - conc[5]["pct"], C_GOLD),
        ("第11–20檔", conc[20]["pct"] - conc[10]["pct"], C_GOLD_SOFT),
        (f"第21–{stats['count']}檔", conc["rest"]["pct"], "#cfc9b8"),
    ]
    bar_x, bar_y, bar_w, bar_h = 20, 46, SVG_W - 40, 46
    parts = [
        f'<text x="{bar_x}" y="24" font-size="14" font-weight="700" fill="{C_INK}">'
        f'母體市值累積占比（依市值排序，{stats["count"]}檔＝100%）</text>'
    ]
    x = bar_x
    for name, pct, color in segs:
        w = bar_w * pct / 100
        parts.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" fill="{color}"/>')
        if w > 34:
            tx = x + w / 2
            parts.append(
                f'<text x="{tx:.1f}" y="{bar_y+bar_h/2+5}" font-size="12.5" font-weight="700" '
                f'fill="#fff" text-anchor="middle">{pct:.1f}%</text>'
            )
        x += w
    ly = bar_y + bar_h + 26
    lx = bar_x
    for name, pct, color in segs:
        parts.append(f'<rect x="{lx}" y="{ly-11}" width="12" height="12" fill="{color}"/>')
        parts.append(f'<text x="{lx+17}" y="{ly}" font-size="12" fill="{C_BODY}">{esc(name)}</text>')
        lx += 17 + len(name) * 12 + 22

    sec_y0 = ly + 34
    parts.append(
        f'<text x="{bar_x}" y="{sec_y0}" font-size="14" font-weight="700" fill="{C_INK}">'
        f"母體市值依 Yahoo 產業分類分布（前 {TOP_SECTOR_N} 大）</text>"
    )
    rows = stats["top_sectors"]
    row_h = 27
    max_pct = max(r["pct"] for r in rows)
    label_w = 210
    chart_x = bar_x + label_w
    chart_w = bar_w - label_w - 70
    y = sec_y0 + 18
    for r in rows:
        w = chart_w * r["pct"] / max_pct
        bar_color = C_ACCENT if "Financ" in r["sector"] else C_ACCENT2
        parts.append(
            f'<text x="{bar_x}" y="{y+row_h*0.62:.1f}" font-size="12.5" fill="{C_BODY}">'
            f'{esc(sec_zh(r["sector"]))}（{r["n"]} 檔）</text>'
        )
        parts.append(f'<rect x="{chart_x}" y="{y+5}" width="{w:.1f}" height="{row_h-13}" rx="2" fill="{bar_color}"/>')
        parts.append(
            f'<text x="{chart_x+w+8:.1f}" y="{y+row_h*0.62:.1f}" font-size="12" font-weight="700" '
            f'fill="{C_INK}">{r["pct"]:.2f}%</text>'
        )
        y += row_h
    parts.append(
        f'<text x="{bar_x}" y="{y+16:.1f}" font-size="12" fill="{C_SEC}">'
        f'其餘產業分類（{stats["rest_sector_n"]} 檔）合計 {stats["rest_sector_pct"]:.2f}%</text>'
    )
    total_h = y + 34
    return svg_wrap("".join(parts), total_h, "母體市值集中度與產業分布")


def svg_exhibit_c(stats):
    """論點C：母體主要產業分類前瞻本益比分布（四分位，含強制納入的Technology分類），標出出口科技群與銀行的具名極端例。"""
    rows = stats["sector_pe_rows"]
    axis_max = 40.0
    bar_x, chart_w = 210, SVG_W - 210 - 90
    top = 44
    row_h = 42
    MIN_N = 5
    parts = [
        f'<text x="20" y="20" font-size="14" font-weight="700" fill="{C_INK}">'
        "前瞻本益比四分位分布（母體主要產業分類）</text>"
    ]

    def xpos(v):
        return bar_x + min(v, axis_max) / axis_max * chart_w

    for t in (0, 10, 20, 30, 40):
        tx = xpos(t)
        parts.append(
            f'<line x1="{tx:.1f}" y1="{top-6}" x2="{tx:.1f}" y2="{top + row_h*len(rows)+6}" '
            f'stroke="{C_BORDER}" stroke-width="1"/>'
        )
        parts.append(f'<text x="{tx:.1f}" y="{top-10}" font-size="12" fill="{C_SEC}" text-anchor="middle">{t}倍</text>')

    y = top
    for r in rows:
        small = r["n"] < MIN_N
        name = f'{esc(sec_zh(r["sector"]))}（n={r["n"]}）' + ("　樣本不足不可比" if small else "")
        parts.append(f'<text x="20" y="{y+row_h/2+5:.1f}" font-size="12.5" fill="{C_SEC if small else C_BODY}">{name}</text>')
        x1, xm, x3 = xpos(r["q1"]), xpos(r["median"]), xpos(r["q3"])
        line_color = "#c9c2b0" if small else C_ACCENT2
        dot_color = "#c9c2b0" if small else C_GOLD_DEEP
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y+row_h/2:.1f}" x2="{x3:.1f}" y2="{y+row_h/2:.1f}" '
            f'stroke="{line_color}" stroke-width="6" stroke-linecap="round"/>'
        )
        parts.append(f'<circle cx="{xm:.1f}" cy="{y+row_h/2:.1f}" r="7" fill="{dot_color}"/>')
        if not small:
            parts.append(
                f'<text x="{xm:.1f}" y="{y+row_h/2-14:.1f}" font-size="12" font-weight="700" fill="{C_INK}" '
                f'text-anchor="middle">{r["median"]:.1f}倍</text>'
            )
        y += row_h
    ly = y + 20
    parts.append(
        f'<text x="20" y="{ly:.1f}" font-size="12" fill="{C_GOLD_DEEP}" font-weight="700">'
        "具名極端例（母體外個股查證值，見鏡頭一／鏡頭二）：出口科技群十檔 trailing PE 47.8–109.8 倍；"
        "十檔銀行隱含 ROE 缺口多數落在 ±2pp 以內</text>'"
    )
    total_h = ly + 24
    return svg_wrap("".join(parts).replace("</text>'", "</text>"), total_h, "前瞻本益比依產業分類分布")


def svg_exhibit_d(stats, facts):
    """論點D：母體殖利率分布直方＋2%股息稅標註。"""
    hist = stats["dy_hist"]
    bar_x, top = 24, 40
    max_n = max(h["n"] for h in hist)
    bw = 78
    gap = 14
    base_y = top + 140
    parts = [f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">母體殖利率分布（{stats["count"]}檔）</text>']
    x = bar_x
    for h in hist:
        hh = 140 * h["n"] / max_n if max_n else 0
        color = C_GOLD_DEEP if h["label"].startswith(("6", "≥")) else C_ACCENT2
        parts.append(f'<rect x="{x:.1f}" y="{base_y-hh:.1f}" width="{bw}" height="{hh:.1f}" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{base_y-hh-6:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{h["n"]}</text>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{base_y+15:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{h["label"]}</text>')
        x += bw + gap
    parts.append(
        f'<text x="{bar_x}" y="{base_y+38:.1f}" font-size="12" fill="{C_SEC}">'
        f'不配息／無資料 {stats["dy_no_dividend"]} 檔未列入直方；殖利率≥6% 共 {stats["dy6_n"]} 檔'
        f'（{stats["dy6_pct"]:.2f}%）；母體殖利率中位數 {stats["dy_median"]:.2f}%</text>'
    )
    parts.append(
        f'<text x="{bar_x}" y="{base_y+56:.1f}" font-size="12" fill="{C_SEC}">'
        "個人股東全年股息所得超過 RM10 萬部分課徵 2% 股息稅（2025 課稅年度起）；資本利得（價差）仍維持免稅</text>'"
    )
    total_h = base_y + 76
    return svg_wrap("".join(parts).replace("</text>'", "</text>"), total_h, "母體殖利率分布與股息稅制")


def svg_exhibit_e(facts):
    """論點E：外資持股時間序列＋年度淨買賣長條。"""
    hist = facts["foreign_holding_share_history"]["value"]
    pts = sorted(hist.items())
    bar_x, top = 24, 44
    line_x = 44          # 左圖第一個時點的標籤置中後不出界，需比 bar_x 再往右退一點
    chart_w = 400
    chart_h = 140
    max_v = 26.0
    min_v = 16.0
    parts = [f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">外資持股占大盤市值比重時間序列</text>']
    step = chart_w / (len(pts) - 1)
    coords = []
    for i, (label, v) in enumerate(pts):
        x = line_x + i * step
        y = top + chart_h - chart_h * (v - min_v) / (max_v - min_v)
        coords.append((x, y))
    path = " L ".join(f"{x:.1f} {y:.1f}" for x, y in coords)
    parts.append(f'<path d="M {path}" fill="none" stroke="{C_GOLD_DEEP}" stroke-width="3"/>')
    for (x, y), (label, v) in zip(coords, pts):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{C_ACCENT}"/>')
        parts.append(f'<text x="{x:.1f}" y="{y-12:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{v:.1f}%</text>')
        parts.append(f'<text x="{x:.1f}" y="{top+chart_h+16:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{esc(label)}</text>')

    x2 = line_x + chart_w + 60
    parts.append(f'<text x="{x2}" y="20" font-size="14" font-weight="700" fill="{C_INK}">外資年度淨買賣（RM 十億，負值＝淨賣超）</text>')
    flow = facts["foreign_net_flow_annual"]["value"]
    years_order = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026_ytd_0903"]
    labels = {"2026_ytd_0903": "2026\n年初至\n09-03"}
    chart_w2 = SVG_W - x2 - 30
    bw2 = chart_w2 / len(years_order) - 6
    max_abs2 = max(abs(v) for v in flow.values())
    zero_y2 = top + chart_h / 2
    for i, y in enumerate(years_order):
        v = flow[y]
        x = x2 + i * (bw2 + 6)
        h = (chart_h / 2 - 20) * abs(v) / max_abs2
        color = C_NEG if v < 0 else C_POS
        ry = zero_y2 - h if v >= 0 else zero_y2
        parts.append(f'<rect x="{x:.1f}" y="{ry:.1f}" width="{bw2:.1f}" height="{h:.1f}" rx="2" fill="{color}"/>')
        # 數值標籤一律放在基線上方：正值放長條頂端上方、負值放基線上方，避免壓到年份列
        ty = zero_y2 - h - 6 if v >= 0 else zero_y2 - 6
        parts.append(f'<text x="{x+bw2/2:.1f}" y="{ty:.1f}" font-size="12" font-weight="700" fill="{color}" text-anchor="middle">{v:+.1f}</text>')
        label = labels.get(y, y)
        for j, seg in enumerate(label.split("\n")):
            parts.append(f'<text x="{x+bw2/2:.1f}" y="{top+chart_h+16+j*13:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{esc(seg)}</text>')
    parts.append(f'<line x1="{x2}" y1="{zero_y2:.1f}" x2="{SVG_W-30}" y2="{zero_y2:.1f}" stroke="{C_BORDER}" stroke-width="1"/>')
    gap_note_y = top + chart_h + 62
    parts.append(
        f'<text x="{bar_x}" y="{gap_note_y:.1f}" font-size="12" fill="{C_SEC}">'
        "左圖各時點來自不同統計提供者，趨勢可信、小數點層級的跨期比較不可信；"
        "右圖 2022 年為全年淨買超（正值），是本序列唯一的反向年度。</text>"
    )

    total_h = gap_note_y + 20
    return svg_wrap("".join(parts), total_h, "外資持股時間序列與年度淨買賣")


# ---------------------------------------------------------------------------
# 4. 內文組裝：五個論點卡
# ---------------------------------------------------------------------------


def name_tag(cn, code):
    return f"{esc(cn)}（{code}）"


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


def klci_total_return_estimate(stats, facts):
    """含息總報酬估算：純價格報酬 × (1＋母體殖利率中位數)^10 － 1。純屬估算，非實算指數。"""
    pr = facts["klci_10y_price_return_pct"]["value"] / 100
    dy = stats["dy_median"] / 100
    return ((1 + pr) * (1 + dy) ** 10 - 1) * 100


def build_arguments(stats, facts):
    out = []
    conc = stats["conc"]
    tr_est = klci_total_return_estimate(stats, facts)

    # A 報酬寫在股息裡
    out.append(argument_card(
        "A", "報酬寫在股息裡：價差十年為負",
        f'KLCI（富時大馬綜合指數，Bursa Malaysia 市值最大的 30 檔成分股組成）十年純價格報酬 '
        f'{facts["klci_10y_price_return_pct"]["value"]:.2f}%'
        f'（{facts["klci_10y_price_return_pct"]["as_of"]}，不含股息，本頁對 yfinance 日線收盤自算）；'
        f'以母體殖利率中位數 {stats["dy_median"]:.2f}%（{SNAPSHOT_DATE}快照，本頁自算）當作年配息、逐年複利再投入估算，'
        f'含息總報酬約 {tr_est:+.1f}%——馬股報酬幾乎全部來自股息，不是價差。',
        [
            f'含息總報酬是估算不是實算：本頁沒有 KLCI 的官方含息總報酬指數，'
            f'{tr_est:+.1f}% 的算法是「純價格報酬 {facts["klci_10y_price_return_pct"]["value"]:.2f}% '
            f'×（1＋{stats["dy_median"]:.2f}%）的十次方」，等於假設十年間殖利率固定在今天的母體中位數、'
            "股息全額再投入且不計稅費——實際值會因逐年殖利率變動而偏離，只能讀成量級，不能讀成精確報酬率。",
            f'拉到最新收盤（{facts["klci_latest_snapshot"]["value"]["date"]}，'
            f'{facts["klci_latest_snapshot"]["value"]["close"]:,.2f} 點），距 2015-06-30 的純價格報酬已收斂到 '
            f'{facts["klci_latest_snapshot"]["value"]["price_return_since_2015q2_pct"]:+.2f}%，十一年多下來幾乎打平'
            "——但這個數字對計算基準日相當敏感：查證區間往前或往後挪一兩個月，正負號都可能翻動，不宜讀成十年價差已經翻正。",
            f'這個估算量級與市場一份報導引用的「十年含息報酬約24.3%」互相印證——該報導原文口徑本來就是含息總報酬，'
            "不是純價格報酬，兩個數字屬同一件事、不是兩個互相矛盾的版本。",
            "年度價格報酬起伏很大：2024年是十年最強的一年，2018年與2019年連兩年下跌超過5%——十年平均數會掩蓋掉年度之間的大幅波動，"
            "見下方 Exhibit 逐年長條。",
            "這個報酬結構決定了後面四個投資角度該用什麼標準去看：複利角度要問內生成長上限（增量投入資本報酬率×再投資率，"
            "估算一家公司光靠留存獲利、不靠外部融資能撐出的最高成長速度）能否對抗負價差背景；金融與收息角度要問股息品質；"
            "事件驅動角度要問深折價能否被機制消滅。",
        ],
        "判讀任何「馬股長期報酬」的敘述，先確認講的是價格報酬還是含息總報酬——這個市場的價格報酬十年為負，"
        "投資人拿到的正報酬幾乎全部來自股息與複利再投入。",
        [
            tile(f'{facts["klci_10y_price_return_pct"]["value"]:.1f}%', "KLCI十年純價格報酬（不含股息）"),
            tile(f"{tr_est:+.1f}%", "十年含息總報酬估算（母體殖利率中位數複利，非官方指數）"),
            tile(f'{facts["klci_latest_snapshot"]["value"]["price_return_since_2015q2_pct"]:+.2f}%', "拉到最新收盤的純價格報酬"),
        ],
        1, "KLCI 日曆年價格報酬與累積價格指數",
        f"來源：yfinance ^KLSE 日線收盤，本頁自算，as-of {SNAPSHOT_DATE}；累積指數基期2015-06-30＝100，"
        "長條為日曆年報酬（各年12/31對前一年12/31），2026年長條為年初至最新收盤、非全年。",
        svg_exhibit_a(facts),
        "價差十年為負不是短期現象，是這個市場十一年來的價格結構；股息不是加分項，是報酬的主要來源。",
    ))

    # B 集中度與產業結構
    fin_row = next((r for r in stats["sector_rows"] if "Financ" in r["sector"]), None)
    out.append(argument_card(
        "B", "集中度與產業結構：金融業以少數家數拿下最大市值占比",
        f'本頁 {stats["count"]} 檔母體（Bursa Malaysia 主板普通股，市值≥RM20億）中，金融服務業僅占家數 '
        f'{stats["fin_count_pct"]:.1f}%（{stats["fin_n"]} 檔），卻拿下母體市值 {stats["fin_pct"]:.1f}%'
        f'（{SNAPSHOT_DATE}快照，本頁自算）——少數金融股定價了母體裡最大的一塊市值。',
        [
            f'前十大個股合計占母體市值 {conc[10]["pct"]:.1f}%，第一大個股單獨占 {conc[1]["pct"]:.1f}%'
            f'（{SNAPSHOT_DATE}快照，本頁自算）；前十大名單見下方 Exhibit。',
            "政府關聯投資機構（GLIC，Government-Linked Investment Companies——由政府設立、管理國民退休金與主權資金的機構投資人，"
            "如 EPF、PNB、Khazanah）是這個市場買盤結構的另一半，但「七大 GLIC 合計控制 Bursa 市值約42%」這筆數字來源是"
            "2017年一位經濟學者的公開發言，距今已逾9年，必須標記為過時數據，僅供結構性參考，不可當作近值引用。",
            f'EPF（雇員公積金局，馬來西亞的強制性退休儲蓄基金）管理的總資產已達 '
            f'{myr_zhao_from_raw(facts["epf_total_assets"]["value"]["amount_rm_trillion"]*1e12)}'
            f'（{facts["epf_total_assets"]["as_of"]}）——但這是 EPF 全部資產的規模（含股票、債券、房地產，且約四成配置在海外），'
            "不等於 EPF 持有的馬股部位占大盤市值的比重，兩者不可混用；後者本頁未查得，是誠實列出的資料缺口，"
            "所以本頁不對「國家隊持股占比」下任何量化結論。",
            f'拉開到本頁母體依 Yahoo 產業分類看，前 {TOP_SECTOR_N} 大分類合計占母體市值 '
            f'{100-stats["rest_sector_pct"]:.1f}%，其餘 {stats["rest_sector_n"]} 檔分散在長尾產業分類中'
            "——這個市場的市值結構是少數大型金融股與資源／公用股構成，而不是均勻分布。",
        ],
        "任何以「馬股大盤」為名的判讀，若不先拆解金融股與前十大個股的占比，本質上是在看一小群龍頭股的走勢，"
        f"不是在看 {stats['count']} 檔公司的平均表現。",
        [
            tile(f'{stats["fin_count_pct"]:.1f}% / {stats["fin_pct"]:.1f}%', "金融服務業占母體家數／市值"),
            tile(f'{conc[10]["pct"]:.1f}%', "前十大個股占母體市值"),
            tile(f'{conc[1]["pct"]:.1f}%', "第一大個股占母體市值"),
        ],
        2, "母體市值集中度累積占比與產業分布",
        f"來源：本頁 {stats['count']} 檔母體快照，as-of {SNAPSHOT_DATE}，依市值排序，本頁自算。"
        f"產業分類採 Yahoo Finance 口徑，圖上為中譯，中英對照：{sector_legend(stats['top_sectors'])}。",
        svg_exhibit_b(stats),
        "集中度不是新現象，是這個市場的結構本身；真正該問的是集中在誰身上、用哪一個分母。",
    ))

    # C 估值分裂
    out.append(argument_card(
        "C", "估值分裂：出口科技群已充分定價，銀行股定價大體有效率",
        "出口導向科技／半導體供應鏈十檔 trailing 本益比 47.8–109.8 倍（過去一年股價普遍已漲 50%–170%），"
        "十檔銀行的隱含 ROE（用 Gordon Growth 模型從股價淨值比反推的股東權益報酬率）缺口多數落在 ±2pp 以內"
        "——同一個市場，兩種完全不同的定價方式。",
        [
            "出口科技群十檔全數距 52 週高點在 20% 以內，多數僅個位數百分比差距——市場已經看到這批公司的品質，"
            "「品質好」與「現在便宜」在這個族群裡是兩件不同的事（完整逐檔查證見鏡頭一）。",
            "十檔銀行的隱含 ROE 缺口多數落在 ±2pp 以內，顯示市場對銀行股的定價效率相當高；真正的錯價集中在保險股"
            "（Takaful Malaysia，Takaful 指符合伊斯蘭教法、以互助分攤取代利息與不確定性的保險，缺口 -6.5pp）"
            "與控股折讓（Hong Leong Financial Group，缺口 -2.9～-3.2pp）兩個角落（完整逐檔查證見鏡頭二）。",
            "拉開到母體依產業分類看前瞻本益比分布（見下方 Exhibit），出口科技群所在的科技分類"
            "中位數與四分位區間仍明顯高於其餘主要分類——這批科技股的估值不是這個市場的常態，是被明確定價的稀缺標的。",
            "估值分裂的另一面是內需複利股：防禦性消費股的內生成長上限普遍卡在個位數（4–9% 區間），"
            "但部分名字的 trailing 本益比已站上 21–46 倍，好價格的窗口不常開（完整查證見鏡頭一）。",
        ],
        "判讀任何個股估值前，先確認它屬於哪一群——出口科技的高本益比已經反映了市場對品質的認可，"
        "銀行股的低隱含 ROE 缺口代表這裡沒有明顯的定價錯誤空間。",
        [
            tile("47.8–109.8倍", "出口科技群十檔trailing本益比區間"),
            tile("±2pp以內", "十檔銀行隱含ROE缺口（多數）"),
            tile(f'{stats["fpe_all"]["median"]:.1f}倍', "母體前瞻本益比中位數（本頁自算）"),
        ],
        3, "前瞻本益比四分位分布：母體主要產業分類",
        f"來源：本頁 {stats['count']} 檔母體快照，as-of {SNAPSHOT_DATE}，本頁自算。"
        "取市值前 6 大分類，再強制納入科技分類（出口科技群所在分類）；橫線兩端為第一四分位與第三四分位、"
        "圓點為中位數，橫軸上限 40 倍，樣本數低於 5 檔的分類灰化並標「樣本不足不可比」。"
        f"產業分類採 Yahoo Finance 口徑，圖上為中譯，中英對照：{sector_legend(stats['sector_pe_rows'])}。"
        "具名個股數字（出口科技群、十檔銀行）為母體外查證值，as-of 2026-08，出處與逐檔明細見鏡頭一、鏡頭二。",
        svg_exhibit_c(stats),
        "估值分裂的分界線不是「馬股貴不貴」，是市場已經用價格把品質稀缺股與傳統銀行股分開對待。",
    ))

    # D 收息
    out.append(argument_card(
        "D", "收息：高息名單與十年未砍息股是兩批不同的名字",
        f'母體 {stats["count"]} 檔中殖利率≥6% 者 {stats["dy6_n"]} 檔（{stats["dy6_pct"]:.1f}%），'
        f'母體殖利率中位數 {stats["dy_median"]:.2f}%；但 27 檔收息驗證階梯裡，同時滿足三項判準'
        "（近十個完整財年常規股息零減少、自由現金流對股息覆蓋率≥1.2 倍、有明文派息政策地板）的是 0 檔。",
        [
            "0 檔這個結果卡在第一項：27 檔全數在近十年窗內至少出現過一次年減。"
            "所以「0 檔」不是判準訂得太苛，是這個市場沒有一檔十年不砍息的樣本（完整判準與逐檔查證見鏡頭三）。",
            "27 檔收息候選做財年對齊的股息品質驗證後，10 檔的全部砍息紀錄完全落在 2020 年 COVID 窗內——"
            "這不是資料失敗，是 2020 年馬股市場普遍性股息削減的真實歷史事件（完整方法論與逐檔查證見鏡頭三）。",
            "真正站得住的供給是 7 檔成長息，其中四席是銀行股，共同點是明文派息政策仍在上修軌道"
            "（完整名單見鏡頭三）。",
            f'個人股東全年股息所得超過 RM10 萬的部分課徵 2% 股息稅（{facts["dividend_tax_2pct"]["as_of"]}），'
            "資本利得（價差）仍維持免稅——這代表「馬股股息全面免稅」的舊印象已被打破，但整體制度仍是重股息、輕價差的設計。",
            "高殖利率不代表安全：收息驗證階梯裡另有 9 檔「高息但脆」——殖利率不低，但十年窗內有砍息紀錄或現金流覆蓋率不足，"
            "判讀高息名單前必須先看現金流量表的覆蓋能力，不能只看配息率高低（完整名單見鏡頭三）。",
        ],
        "殖利率排行榜的排序邏輯只看「配了多少」，不看「配得出來嗎」；真正的收息判準必須反過來，"
        "先確認現金流量表的覆蓋能力與砍息歷史，高息與真收息在這個市場裡多數不是同一批名字。",
        [
            tile(f'{stats["dy6_n"]}檔／{stats["dy6_pct"]:.1f}%', "殖利率≥6%檔數／占母體比重"),
            tile("0檔", "27檔驗證階梯中三項判準全過者"),
            tile("7檔", "真正站得住的成長息（四席為銀行股）"),
        ],
        4, "母體殖利率分布與股息稅制",
        f"來源：本頁 {stats['count']} 檔母體快照，as-of {SNAPSHOT_DATE}，本頁自算；股息稅細則另見計分卡與方法論。",
        svg_exhibit_d(stats, facts),
        "高殖利率排行榜的排序邏輯只看「配了多少」；真收息判準必須反過來，先看現金流量表覆蓋能力與砍息歷史。",
    ))

    # E 買盤結構與資金流
    flow = facts["foreign_net_flow_annual"]["value"]
    ytd = flow["2026_ytd_0903"]
    ytd_yi = abs(ytd) * 10
    full_years = {k: v for k, v in flow.items() if k.isdigit()}
    sell_years = sum(1 for v in full_years.values() if v < 0)
    n_full = len(full_years)
    out.append(argument_card(
        "E", f"買盤結構與資金流：外資 {n_full} 個完整年度賣了 {sell_years} 年，2026 年繼續賣",
        f'外資持股占大盤市值比重 {facts["foreign_holding_share_pct"]["value"]}%'
        f'（{facts["foreign_holding_share_pct"]["as_of"]}），較 2018 年高點的 24.2% 明顯下滑；'
        f'2018–2025 這 {n_full} 個完整年度中有 {sell_years} 年是全年淨賣超，'
        f'2026 年初至 2026-09-03 累計再淨賣超 RM{ytd_yi:.1f} 億'
        "——這是一條方向清楚的單邊撤退，不是來回震盪。",
        [
            "唯一的反向年度是 2022 年：全年淨買超 RM44.0 億（證券監督委員會《Capital Market Stability Review 2022》），"
            "這一年也是唯一打斷連續賣超的年度；除此之外 2018–2025 年年淨賣超，最重的一年是 2020 年的 RM247.5 億。",
            f'2026 年的路徑是「賣為主、中間有幾週回補」：年初至 2026-07-06 累計淨賣超約 RM34 億，'
            f'至 2026-09-03 擴大到 RM{ytd_yi:.1f} 億；同期本地機構累計淨買超 RM51.1 億，'
            "外資釋出的部位主要由本地法人買下，這是這個市場近年反覆出現的持股移轉結構。",
            "IPO 市場同時是活躍的：2026 上半年 36 家 IPO 募資 RM54 億、新增市值 RM261 億，"
            "官方新聞稿稱家數與募資額同步登上東協第一（此為 Bursa Malaysia 自陳的排名，本頁未獨立查證其他交易所同期數字做交叉比對）；"
            "2026 全年 IPO 市值目標已由 RM280 億上修至 RM340 億。新股募得到錢、同時外資在次級市場持續淨賣超，是兩件同時成立的事。",
            f'柔佛的 JS-SEZ 經濟特區（Johor 跨境合作經濟特區）{facts["js_sez_investment_2025"]["as_of"]}核准投資達 RM77.0 億，'
            "此為特區本身口徑，窄於柔佛州整體 FDI（外人直接投資）口徑，兩者分母不同不可互換引用；"
            f'令吉現貨匯率約 1 美元兌 {facts["myr_usd_rate"]["value"]["spot_approx"]} 令吉'
            f'（{facts["myr_usd_rate"]["as_of"]}），2025 年對美元升值約 9-10%——匯率走強沒有把外資買盤帶回來。',
            f'BNM（Bank Negara Malaysia，馬來西亞央行）的隔夜政策利率（OPR）現值 {facts["opr_current"]["value"]}%，'
            f'{facts["opr_current"]["as_of"]}，是判讀馬股資金成本與銀行股淨利差方向的背景利率。',
        ],
        f"外資持股的下滑是趨勢不是雜訊：{n_full} 個完整年度裡 {sell_years} 年淨賣超，2026 年至今仍在賣。"
        "買下這些部位的是本地機構，所以指數沒有因此崩跌——但這代表邊際定價權正在從外資移向本地法人，"
        "任何預期「外資回頭推升估值」的判讀，都必須先看到年度層級的方向翻轉，而不是幾週的回補。",
        [
            tile(f'{facts["foreign_holding_share_pct"]["value"]}%', "外資持股占大盤市值比重"),
            tile(f"-RM{ytd_yi:.1f}億", "2026年初至09-03外資累計淨買賣"),
            tile(f"{sell_years}／{n_full} 年", "2018–2025完整年度中的淨賣超年數"),
        ],
        5, "外資持股時間序列與年度淨買賣",
        "來源：左圖為多家財經媒體轉引 Bursa Malaysia／MIDF-MBSB Research 外資持股統計（各時點提供者不同，見§6）；"
        "右圖 2018 年為 MIDF 統計、2022 年為 Securities Commission Malaysia《Capital Market Stability Review 2022》、"
        "2024–2025 年為星洲日報 2026-01-05 轉引年度統計、2026 年為東方日報 2026-09-04 轉引 MBSB Research。"
        "as-of 依各年標示，2026 年為年初至 2026-09-03 累計。",
        svg_exhibit_e(facts),
        f"外資賣了 {sell_years} 個年度，指數沒垮，因為本地機構把部位買了下來；判讀馬股買盤結構，"
        "要問的是誰在定邊際價格，不是外資回不回來。",
    ))

    return "".join(out)


def build_scorecard(stats, facts):
    conc = stats["conc"]
    rows = [
        (f"母體市值總額（{stats['count']}檔）", myr_zhao_from_raw(stats["total_mcap"]), SNAPSHOT_DATE,
         "本頁馬股母體（Bursa主板普通股，市值≥RM20億）的合計市值", "母體快照（本頁自算）"),
        (f"母體檔數", f'{stats["count"]}檔', SNAPSHOT_DATE,
         "市值≥RM20億的Bursa主板普通股家數", "母體快照（本頁自算）"),
        ("前十大個股占母體市值", f'{conc[10]["pct"]:.1f}%', SNAPSHOT_DATE,
         "少數龍頭股決定了母體裡最大的一塊市值，見論點B", "母體快照（本頁自算）"),
        (f"金融服務業占母體市值（{stats['fin_n']}檔）", f'{stats["fin_pct"]:.1f}%', SNAPSHOT_DATE,
         f"僅占母體家數{stats['fin_count_pct']:.1f}%，卻拿下最大市值占比", "母體快照（本頁自算）"),
        ("母體前瞻本益比中位數", f'{stats["fpe_all"]["median"]:.1f}倍', SNAPSHOT_DATE,
         "與出口科技群、銀行股的估值分裂對照，見論點C", "母體快照（本頁自算）"),
        ("母體殖利率中位數", f'{stats["dy_median"]:.2f}%', SNAPSHOT_DATE,
         "殖利率≥6%者僅占母體少數，見論點D", "母體快照（本頁自算）"),
        ("母體ROE中位數", f'{stats["roe_all_median"]:.1f}%' if stats["roe_all_median"] is not None else "n/a", SNAPSHOT_DATE,
         "資本報酬整體水位，個別產業差異可達數倍", "母體快照（本頁自算）"),
        ("KLCI十年純價格報酬", f'{facts["klci_10y_price_return_pct"]["value"]:.2f}%', facts["klci_10y_price_return_pct"]["as_of"],
         f'不含股息；含息總報酬估算約{klci_total_return_estimate(stats, facts):+.1f}%（估算非官方指數），見論點A', "yfinance自算"),
        ("外資持股占大盤市值比重", f'{facts["foreign_holding_share_pct"]["value"]}%', facts["foreign_holding_share_pct"]["as_of"],
         "較2018年高點24.2%明顯下滑；各時點提供者不同，趨勢可信、小數點比較不可信", "研究機構月度統計轉引（原始頁未能一手複核）"),
        ("2026年外資累計淨買賣", f'-RM{abs(facts["foreign_net_flow_annual"]["value"]["2026_ytd_0903"])*10:.1f}億',
         "2026年初至2026-09-03",
         "延續2018年以來的淨賣超方向，2022年是唯一的淨買超年度", "東方日報2026-09-04轉引MBSB Research"),
        ("2026上半年IPO家數與募資額", "36家／RM54億", facts["ipo_1h2026_count_and_amount"]["as_of"],
         "另新增市值RM261億；官方新聞稿稱同步登上東協第一（自陳排名，本頁未獨立查證）", "The Star轉引Bursa Malaysia"),
        ("BNM隔夜政策利率", f'{facts["opr_current"]["value"]}%', facts["opr_current"]["as_of"],
         "自2025-07-09降息一碼後未再調整，2026年五次會議全數維持不變", "Bank Negara Malaysia官方"),
        ("個人股息稅", "2%（逾RM10萬部分）", facts["dividend_tax_2pct"]["as_of"],
         "資本利得仍維持免稅，制度仍是重股息、輕價差的設計", "會計師事務所彙整財政法案"),
        ("令吉兌美元", f'約{facts["myr_usd_rate"]["value"]["spot_approx"]}', facts["myr_usd_rate"]["as_of"],
         "2025年對美元升值約9-10%", "Wise／XE匯率轉引"),
        ("私有化件數與成交率（2020–2026）", "14件／已知結果10件中成交9件", "2020–2026",
         "14件中僅6件查得溢價數字，溢價中位數約8.3%，樣本小只讀量級不做統計推論",
         "本頁彙整交易所公告"),
        ("控股折價最深值", "56.3%（Genting Bhd）", "2026-08前後",
         "折價最深不等於結構訊號最集中，見鏡頭四；為未扣母公司負債的粗估", "本頁SOTP估算"),
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
# 5. 計分卡／可作戰名單（頁面實際順序見 main()；本節與下方falsifiers/methodology
#    僅為程式碼組織方便集中放置，非頁面章節順序）
# ---------------------------------------------------------------------------

# wait 欄位逐字取自各檔 DD 的 rearm_trigger（不改寫、不換算單位、不補標點）；
# 白話補註另放 gloss 欄，在頁面上以「本頁補註」標明，與逐字裁決分開呈現。
WATCH_EXISTING = [
    dict(t="5398", name="Gamuda Berhad", lens="鏡頭一", verdict="X｜觀望", role="追蹤",
         wait="訂單簿轉換順利且 Fwd PE 回落至 15x 以下（約 RM3.50-3.70）、或連兩季淨負債/EBITDA 降至 4x 以下，方重新評估進場",
         gloss="Fwd PE＝以未來一年預估獲利算出的本益比，x＝倍；EBITDA＝稅息折舊攤銷前獲利",
         dd="DD_5398KL_20260811.html", date="2026-08-11"),
    dict(t="5246", name="Westports Holdings Berhad", lens="鏡頭一／鏡頭三", verdict="B｜觀望", role="追蹤",
         wait="Fwd PE 回落至 15x 以下（約 RM5.7-6.0）或 WP2 CT10 如期於 2028 前段商運且轉口份額止跌，方重新評估進場",
         gloss="WP2 CT10＝巴生港西港第二期擴建的第 10 號貨櫃碼頭；轉口份額＝經此港轉運再出口的貨量占比",
         dd="DD_5246KL_20260811.html", date="2026-08-11"),
    dict(t="5326", name="99 Speed Mart Retail Holdings Berhad", lens="鏡頭一", verdict="B｜觀望", role="追蹤",
         wait="Fwd PE回落至≈30x（約RM2.9-3.0）或SSSG加速/KK Mart份額佐證出現前，維持觀望",
         gloss="SSSG＝同店銷售成長率，只計開店滿一年以上的門市，用來分辨成長來自開新店還是既有店變強；KK Mart＝同業競爭通路",
         dd="DD_5326KL_20260811.html", date="2026-08-11"),
    dict(t="6139", name="Syarikat Takaful Malaysia Keluarga Berhad", lens="鏡頭二", verdict="B｜觀望", role="追蹤",
         wait="Q2FY26(約2026-08下旬公布)確認CSM單季年增回升至≥5%,或估值回落至Fwd PE≈6x／RM3.00附近增加安全邊際，任一成立即可升級進場並加碼至目標倉位",
         gloss="CSM＝合約服務邊際，指已收保費中尚未認列為獲利、將在未來各期逐步釋放的部分，是這類保險業務的獲利存量",
         dd="DD_6139KL_20260812.html", date="2026-08-12"),
]

WATCH_CANDIDATES = [
    ("1163", "Allianz Malaysia Berhad", "鏡頭二", "全股本口徑下隱含ROE缺口仍約-4pp，唯一還沒做DD的真候選，但流動性差、缺口收斂沒有明確催化劑"),
    ("1082", "Hong Leong Financial Group Berhad", "鏡頭二／鏡頭四", "控股折讓-2.9~-3.2pp×私有化結構訊號5/6的雙重折價，但驅動不是基本面而是大股東哪天想收，外部買家才有真溢價"),
    ("1899", "Batu Kawan Berhad", "鏡頭四", "控股折價30.5%×結構訊號5/6，深折價×控制股東83.1%×自由流通14.4%，但賭的是要約事件本身"),
    ("5606", "IGB Berhad", "鏡頭四", "控股折價27.5%×結構訊號5/6，母層淨負債未扣，實質折價會再收斂"),
    ("0128", "Frontken Corporation Berhad", "鏡頭一", "真複利機器（ROIC四年均逾32.6%），但出口科技群顯著回檔前，現距52週高僅-2.6%、trailing PE 47.8倍"),
    ("0151", "Kelington Group Berhad", "鏡頭一", "淨利連四年成長、標案儲備一季內翻倍，但trailing PE已47.9倍，中國營收占比約三成打折全球化程度"),
]


def build_watchlist():
    trs = []
    for r in WATCH_EXISTING:
        gloss = (f'<br><span style="color:var(--gold-deep)">本頁補註：{r["gloss"]}</span>'
                 if r.get("gloss") else "")
        trs.append(
            f'<tr><td class="lbl">{name_tag(r["name"], r["t"])}</td><td class="why lenscol">{r["lens"]}</td>'
            f'<td class="why"><b>{r["verdict"]}</b></td>'
            f'<td class="why"><span data-verbatim="dd">{esc(r["wait"])}</span>{gloss}</td>'
            f'<td class="why ddcol"><a href="{DD_DOC_BASE}/{r["dd"]}">查看DD</a></td></tr>'
        )
    for t, name, lens, reason in WATCH_CANDIDATES:
        trs.append(
            f'<tr><td class="lbl">{name_tag(name, t)}</td><td class="why lenscol">{lens}</td>'
            f'<td class="why" style="color:var(--warn);white-space:nowrap">無（站內零覆蓋）</td><td class="why">{reason}</td>'
            f'<td class="why ddcol">—</td></tr>'
        )
    return "".join(trs)


def build_dd_review_note():
    lines = []
    for r in WATCH_EXISTING:
        d = days_between(r["date"], DD_BASIS_DATE)
        if d > 90:
            lines.append(f'{name_tag(r["name"], r["t"])}（裁決日{r["date"]}），截至{DD_BASIS_DATE}已滿{d}天，超過站內90天複審窗')
    return "；".join(lines)


# ---------------------------------------------------------------------------
# 7. 會推翻本頁判斷的證據
# ---------------------------------------------------------------------------

FALSIFIERS = [
    "若KLCI以最新收盤重新計算的十年純價格報酬穩定站上正值（而不是像目前這樣在零附近隨基準日擺盪），"
    "且不是單一月份的短暫反彈，代表論點A「報酬寫在股息裡」的框架需要重新檢視。",
    "若金融服務業占母體市值的比重從目前水準明顯下滑，且不是因為母體整體市值結構性擴張稀釋，"
    "代表這個市場的集中度正在真正分散，論點B需要換掉支撐案例。",
    "若出口科技群十檔的trailing本益比中位數從目前的高檔區間顯著收斂到30倍以下，且股價同步大幅回檔，"
    "代表市場對這批公司的定價已經鬆動，論點C的「已充分定價」判讀需要重新檢視。",
    "若27檔收息驗證階梯重新查證後出現至少一檔同時滿足三項判準（十年窗內常規股息零減少、自由現金流對股息覆蓋率"
    "≥1.2倍、有明文派息政策地板）的股票，代表這個市場並非完全沒有可長期依賴的股息供給，論點D的核心主張需要鬆動。",
    "若2026全年外資淨買賣結算為淨買超，或2027年再出現一個全年淨買超年度，使2018年以來的淨賣超年度不再是壓倒性多數，"
    "代表外資的結構性撤退已經轉向，論點E需要重新評估；單月或連續數週的回補不算，年度層級的方向翻轉才算。",
    "若Genting Bhd對Genting Malaysia的持股跨過Bursa上市規則的75%公眾持股界線後，公司仍選擇維持掛牌並補回公眾持股，"
    "或控制股東主動降低持股，代表本頁對「控制股東持股逼近界線＝私有化壓力訊號」的判讀框架需要重新檢視。",
]


def build_falsifiers():
    return "".join(f'<div class="amber">{x}</div>' for x in FALSIFIERS)


# ---------------------------------------------------------------------------
# 8. 資料、方法與盲區
# ---------------------------------------------------------------------------


def build_methodology(stats, facts, uni=None):
    flow = facts["foreign_net_flow_annual"]["value"]
    meta = (uni or {}).get("meta", {})
    border = meta.get("crosscheck_below_threshold_on_yfinance", [])
    border_names = "、".join(f'{b["name"].replace(" Berhad", "").replace(" Bhd.", "")}（{b["code"]}）'
                             for b in border)

    def yi(v):
        return f'{"+" if v > 0 else "-"}RM{abs(v)*10:.1f}億'

    flow_line = "、".join(
        f'{k if k.isdigit() else "2026年初至09-03累計"}（{yi(v)}）'
        for k, v in sorted(flow.items())
    )
    return f'''
<b>母體怎麼建的</b>：範圍為Bursa Malaysia主板（Main Market）普通股，市值≥RM20億，快照日期{SNAPSHOT_DATE}。
第一步的候選名單來源為Wikipedia「馬來西亞交易所上市公司列表」（2017年4月10日版本，807檔）＋人工補充近年掛牌之
大型個股9檔，合計814檔，以yfinance批次抓取市值篩出116檔。第二步做完整性交叉比對：另取一份公開的馬股市值排行
全量名單（TradingView馬來西亞股票篩選器，市值≥RM20億共136檔，2026-09-10查詢），與第一步的116檔逐檔對照，
找出19檔候選名單未涵蓋者（多數是2017年後掛牌或改名的公司），逐檔以yfinance補抓後，14檔市值達標納入母體、
4檔在本頁快照日的yfinance市值低於RM20億門檻不納入、1檔（UMS Integration，境外註冊、主要上市地在另一個交易所、
Bursa僅為第二上市）依「不與主要上市地重複計算市值」的規則排除。最終母體{stats["count"]}檔，
總市值約{myr_zhao_from_raw(stats["total_mcap"])}。<br><br>

<b>候選名單中約92檔查無資料或已下市</b>：抽查後確認多數是2017年後已完成私有化或下市的公司，與鏡頭四查證到的
私有化事件互相印證，包括UMW Holdings（2024下市）、Boustead Holdings（2023下市）、Malaysia Airports Holdings
（2025下市）、Cocoaland（2022下市）、FGV Holdings（2025下市）、Apex Healthcare（2026下市）、UEM Edgenta
（2026年7月下市）——這不是資料缺失，是這個市場私有化管道活躍的直接證據。<br><br>

<b>本頁範圍未涵蓋的軸線（誠實揭露）</b>：①ACE市場與LEAP市場（創業板與有限公開發行市場）完全未涵蓋，
僅涵蓋主板；②完整性交叉比對用的市值排行名單本身也是第三方彙整，若它漏列某檔，本頁同樣會漏——
兩份名單互相補位可以把「舊名冊沒有新公司」這一類遺漏補起來，但無法保證等同Bursa官方即時名冊；
③市值門檻以yfinance快照值判定，落在RM19–21億邊界的公司會因報價時點而進出母體，本次查證有{len(border)}檔
屬此情形，逐檔列名如下：{border_names}——其中Zetrix AI雖不在母體內，仍以127檔量化篩的個股身分出現在鏡頭一，
兩者是不同的名單口徑；④外國公司在Bursa的第二上市本次已逐檔查證並排除1檔具名個案，排除規則從
「未查證」升級為「已查證，1檔排除」。<br><br>

<b>數字的時效不一致，讀者要分開看</b>：母體數字統一為{SNAPSHOT_DATE}快照；KLCI十年報酬區間為
{facts["klci_10y_price_return_pct"]["as_of"]}；外資持股as-of {facts["foreign_holding_share_pct"]["as_of"]}；
外資淨買賣as-of {facts["foreign_net_flow_annual"]["as_of"]}；OPR as-of {facts["opr_current"]["as_of"]}；
IPO統計as-of {facts["ipo_1h2026_count_and_amount"]["as_of"]}；EPF資產as-of {facts["epf_total_assets"]["as_of"]}；
四張鏡頭卡的具名個股數字 as-of 2026-08（鏡頭查證日），與母體快照日不同；估值倍數已隔約一個月（例：Zetrix AI 的 trailing 本益比在 2026-09-10 已由 6.0 倍降至 1.9 倍），判讀前請以最新報價為準。
整頁不是同一個時間切面，引用時應標明各自的as-of。<br><br>

<b>外資年度淨買賣的逐年數字與出處</b>：{flow_line}（負值＝淨賣超，正值＝淨買超）。
逐年出處不同：2018為MIDF統計經媒體引用；2019至2021、2023為MIDF週報年度累計；2022取自Securities Commission
Malaysia《Capital Market Stability Review 2022》，是本序列唯一的全年淨買超年度；2024與2025取自星洲日報
2026-01-05轉引之年度統計（原文：2025年全年淨撤223億令吉，較2024年的42億令吉高出5.3倍）；2026年初至09-03
累計取自東方日報2026-09-04轉引MBSB Research。本頁同時撤下先前引用的「3月淨流入RM5.9億、7月淨流入RM2.7億、
8月單月淨流出RM20億」三筆月度數字——無法一手轉引查證，且與同期「連續7–8週淨賣超」的報導互相矛盾。<br><br>

<b>「馬股IPO募資額東協排名第一」為Bursa Malaysia官方自陳，本頁未獨立驗證</b>：2026上半年官方新聞稿稱
家數與募資額同步登上東協第一，但本次查證未取得東協其他交易所同期IPO統計做交叉比對，僅確認家數（36家）
與募資額（RM54億）本身的數字來源可靠，排名本身的獨立驗證仍是缺口。<br><br>

<b>控股折價SOTP（Sum-of-the-Parts）僅為粗估</b>：本頁引用的控股折價百分比未扣除母公司層負債，也未計入
非上市資產（正向修正項，會使真實折價更深）或母公司層現金（可能是負向修正項），僅供量級參考，不是精確估值。<br><br>

<b>GLIC（政府關聯投資機構）個別持股占比未查得</b>：「七大GLIC合計控制Bursa市值約42%」這筆數字來源是2017年
一位經濟學者的公開發言，距今已逾9年，必須標記為過時數據。連該來源的分母都對不齊：本頁能具名的GLIC只有六家
（EPF／PNB／KWAP／Khazanah／LTH／LTAT），第七家是誰原始發言未載明，本頁也未查得，所以這個42%連
「涵蓋哪些機構」都無法確認，只能當結構性印象、不可當數字引用；
EPF馬股部位占大盤市值的比重本頁未查得，是誠實列出的資料缺口，不可與EPF整體資產規模混用。<br><br>

<b>站內DD裁決的抄錄規則</b>：可作戰名單的裁決欄位逐字取自各檔DD決策層的訊號等級與裁決欄位，「在等什麼」欄位
逐字取自各檔的重評估觸發條件欄位——連英文縮寫、半形標點與單位寫法都原樣保留，不做中文化改寫，這樣讀者比對DD原文時
不會發現兩處措辭不同；欄內以金色標示的「本頁補註」是本頁另外加上的白話解釋，不屬於原裁決文字。同一家公司一律取日期
最新的那一份；零覆蓋候選標「無（站內零覆蓋）」。<br><br>

<b>外資持股比重是跨來源拼接的序列，不是單一機構的連續統計</b>：2024-12（19.7%）與2025-12（19.0%）取自同一篇年度
回顧、同一口徑，是序列中唯一可信的相鄰兩點；其餘時點分別轉引自不同報導與可能不同的統計提供者，因此序列在
2025-08（18.8%）到2025-12（19.0%）之間出現小幅回升的非單調轉折，那是跨來源口徑差異，不是真實的月度反轉。
最新一筆18.1%（2026-08）的原始報導頁在本次查證時受反爬蟲阻擋、未能一手複核，量級可信但確信度僅中上。
結論用法：趨勢方向可以引用，小數點層級的跨期比較不可以。<br><br>

<b>已知缺口清單</b>：JS-SEZ特區本身核准投資（RM77.0億）窄於柔佛州整體FDI口徑，本次未重新查證州整體數字，不在本頁引用；
兩者分母不同不可互換引用；令吉匯率為區間估計非單一精確值；私有化溢價僅6件有數字且基準不一致，雙峰結構只讀方向；
含息總報酬為估算非官方指數；每筆結構數字的原始出處與查證日期已在計分卡與各論點卡標明。
'''


# ---------------------------------------------------------------------------
# 9. 排版：CJK／英文（含 ticker、數字）自動留白一格
# ---------------------------------------------------------------------------


def add_cjk_latin_spacing(text):
    text = re.sub(r"([一-鿿])([A-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9])([一-鿿])", r"\1 \2", text)
    return text


# ---------------------------------------------------------------------------
# 6. 四張鏡頭卡（沒有子頁，事實／名單／出處全部承接自舊版 malaysia.html）
# ---------------------------------------------------------------------------

DD_DOC_BASE = "https://research.investmquest.com/dd"


def lens_card(n, name, question, verdict, bullets, exnum, cap, sub, table_html, take):
    bl = "".join(f"<li>{b}</li>" for b in bullets)
    return f'''
<div class="card">
<h3><span class="h-n">鏡頭{n}</span>{esc(name)}</h3>
<div class="pt"><div class="ph">核心問題</div><div class="pb">{question}</div></div>
<div class="thecall">{verdict}</div>
<ul>{bl}</ul>
<div class="exhibit scroll">
<div class="ex-tag">Exhibit {exnum}</div>
<div class="ex-cap">{cap}</div>
<div class="ex-sub">{sub}</div>
<table>{table_html}</table>
<div class="ex-take">{take}</div>
</div>
</div>
'''


def trow(cells):
    tds = "".join(f"<td class=\"why\">{c}</td>" for c in cells)
    return f"<tr>{tds}</tr>"


def build_lenses():
    out = []

    # 鏡頭一：複利機器
    l1_rows = [
        ["QL Resources（7084）", "增量ROIC 515.62%（不穩定）", "四年間投入資本淨增加額僅RM2,380萬，是小分母把比率放大的假象；真實最新年ROIC僅14.07%，不支持排在主榜前段", "母體快照＋公開財報，本頁自算"],
        ["Frontken（0128）", "ROIC四年均＞32.6%", "族群中財務品質最一致的一檔，穿越2022–2025下行週期仍逐年成長，但trailing PE已47.8倍、距52週高僅-2.6%", "公開財報"],
        ["Kelington Group（0151）", "淨利連四年成長逾170%", "標案儲備一季內從RM50億翻倍到RM90億，但中國貢獻約三成營收，全球化程度打折扣；trailing PE 47.9倍", "公開財報"],
        ["Guan Chong（5102）", "增量ROIC 34.75%", "剔除QL假象後名義上的真榜首，但trailing PE 14.0倍是商品週期峰值快照，非結構性複利證據", "公開財報"],
        ["Westports Holdings（5246）", "窄基準ROIC 25.3%／完整基準16.3%", "特許權租賃負債約RM23億藏在非標準會計科目，被排除在投入資本分母外，人為墊高兩項指標", "公開財報＋DD_5246KL_20260811"],
        ["Zetrix AI（0138）", "trailing PE 6.0倍（族群最低）", "自由現金流（營業現金流扣掉資本支出後可自由運用的現金）對淨利的比值連兩年遠低於1，帳面獲利長期難以穩定轉換成現金，低本益比多半是「便宜有理由」", "公開財報"],
        ["99 Speed Mart（5326）", "ROIC約24%", "FY25營收+14.5%／PAT+30.5%，經營現金流自給擴張，但Fwd PE約42倍偏貴", "DD_5326KL_20260811"],
        ["Dutch Lady／F&N／Mr D.I.Y.／99 Speed Mart／Carlsberg／Heineken Malaysia", "內生成長上限多落在4–9%", "防禦性消費股生意品質沒有爭議，但成長上限普遍卡在個位數，部分名字trailing PE已站上21–46倍", "公開財報"],
    ]
    l1_table = "<thead><tr><th>公司（代號）</th><th>關鍵數字</th><th>判讀</th><th>出處</th></tr></thead><tbody>" + "".join(trow(r) for r in l1_rows) + "</tbody>"
    out.append(lens_card(
        1, "複利機器：少而貴",
        "127檔量化篩選能篩出多少真正站得住的複利機器？",
        "127檔篩出14檔候選，但至少4檔的排名本身是計算假象；扣除假象後真正站得住的複利機器（如Frontken、Kelington）"
        "已被市場充分定價——便宜的多是假的，真的都不便宜。",
        [
            "第一層對127檔可算ROIC（投入資本報酬率＝稅後營業利益／投入資本，稅後營業利益＝營業利益×（1－有效稅率），"
            "投入資本＝股東權益＋計息負債－現金）的馬股，做ROIC完整基準≥12%且增量ROIC≥10%的雙門檻量化篩，產出14檔主榜。"
            "增量ROIC是「四年間新增的稅後營業利益／四年間新增的投入資本」，衡量新投進去的錢賺回多少——分母是差額，"
            "所以公司若幾乎沒有擴充投入資本，分母會小到讓比率失去意義，這正是主榜第一名的問題。"
            "第二層對其中出口導向科技／半導體供應鏈嫌疑最高的十檔，做客戶、競爭、跑道、週期、AI封裝曝險五維深查。",
            "出口科技群十檔（ViTrox、Frontken、Inari Amertron、MPI、Unisem、Greatech、Pentamaster、UWC、Kelington、SAM Engineering）"
            "trailing本益比全數落在47.8–109.8倍區間，十檔全部距52週高在20%以內，過去一年股價普遍已漲50%–170%。",
            "量化篩選器常見的四種陷阱：小分母雜訊（QL Resources）、商品週期峰值（Guan Chong）、獲利不轉現金（Zetrix AI）、"
            "特許權租賃負債藏在非標準會計科目而被誤判（Westports）——任何只看比率排序、不追分母結構與週期位置的篩選器都會被騙。",
            "三個類別的收斂：內需複利（生意品質真，但內生成長上限4–9%或已偏貴）、週期假象（篩選器會被騙的四種表現）、"
            "出口科技（品質真，但已被市場充分定價）。",
        ],
        6, "複利機器精選：計算假象、真複利與內需複利三個類別",
        "來源：公開財報（yfinance）本頁彙整，個股數字 as-of 2026-08（鏡頭查證日，與母體快照日不同；估值倍數已隔約一個月，判讀前請以最新報價為準）；"
        "個股DD連結見站內裁決鏈；完整14檔主榜與十檔出口科技深查詳見各公司財報。",
        l1_table,
        "127檔篩到真正站得住的複利機器只剩個位數，且多數已被市場充分定價；市佔地位與生意品質不等於現在的價格划算。",
    ))

    # 鏡頭二：金融
    l2_rows = [
        ["Maybank（1155）", "ROE 11.2%／隱含ROE缺口+0.7~0.8pp", "東協區域龍頭，收入端疲軟拖累ROE，市場略給溢價；十四檔中流動性最深", "公開財報"],
        ["Public Bank（1295）", "ROE 12.0%／隱含ROE缺口+1.3~1.6pp", "資產品質與成本效率最佳的保守型龍頭，估值溢價最明顯之一", "公開財報"],
        ["CIMB（1023）", "ROE 11.0%／隱含ROE缺口≈0pp", "東協全能行，定價最貼近基本面，量價質三軸同步改善", "公開財報"],
        ["Hong Leong Financial Group（1082）", "ROE 10.5%／隱含ROE缺口-2.9~-3.2pp", "銀行＋保險＋投行控股集團，控股折讓十四檔中最明顯", "公開財報"],
        ["Allianz Malaysia（1163）", "窄基準缺口-7.9pp／全股本口徑約-4pp", "普通股與ICPS雙軌股權，yfinance市值僅計入普通股，窄基準缺口有一半是股數假象", "公開財報"],
        ["Takaful Malaysia（6139）", "ROE 17.2%／隱含ROE缺口-6.5pp", "伊斯蘭保險龍頭，獲利能力全場最高但市場折讓顯著，殖利率＋成長力組合全場最佳", "DD_6139KL_20260812"],
        ["Bursa Malaysia（1818）", "ROE 32.9–35%／隱含ROE +18~20pp（框架失真）", "壟斷型交易所，輕資本高ROE，Gordon Growth估值模型不適用於此類資產，本頁列為缺口", "公開財報"],
    ]
    l2_table = "<thead><tr><th>公司（代號）</th><th>關鍵數字</th><th>判讀</th><th>出處</th></tr></thead><tbody>" + "".join(trow(r) for r in l2_rows) + "</tbody>"
    out.append(lens_card(
        2, "金融：定價大體有效率，錯價在保險與控股折讓角落",
        "馬股金融股（金融服務業占母體家數少但市值占比高，見論點B）的估值，是定價權還是槓桿撐出來的？",
        "10檔銀行的隱含ROE缺口多數落在±2pp以內，市場對銀行股的定價效率相當高；真正的錯價集中在保險股"
        "（Takaful Malaysia -6.5pp）與控股折讓（Hong Leong Financial Group -2.9~-3.2pp）兩個角落。",
        [
            "方法：用Gordon Growth股利模型從股價淨值比反推隱含ROE（股價淨值比＝（ROE－永續成長率）／（股東權益成本－永續成長率）），"
            "股東權益成本統一假設9.5%、永續成長率統一假設3.5%；此框架假設穩態股利貼現，對高成長／輕資產的交易所會系統性失真。",
            "馬股銀行ROE偏低有兩個結構性理由，都不是經營不力：一是非利息收入業務（財富管理、保險交叉銷售）規模偏小，"
            "獲利過度依賴利差；二是稅率——馬來西亞企業所得稅24%，同等稅前ROE下稅後ROE會被結構性拉低約1-2pp。"
            "這兩項都不是管理層短期能改變的，所以隱含ROE缺口小並不代表銀行「便宜」，只代表市場已經把這層結構折價算進去了。",
            "Allianz Malaysia的多重股權類別是常見方法論陷阱：普通股與ICPS（不可贖回可轉換特別股，可1股換1股普通股）分開掛牌，yfinance市值計算只抓普通股，"
            "把P/B系統性低估近一半，隱含ROE缺口因此被放大近一倍——任何多重股權類別的公司，用市值算P/B前必須先確認股本計算是否涵蓋全部已發行類別。",
            "籌碼面與收息判讀常互為鏡像：家族或政府關聯機構的高度持股，對收息角度是正面訊號（派息文化穩定），"
            "對流動性角度卻是負面訊號（自由流通淺、股價發現效率打折）。",
        ],
        7, "馬股金融股精選：10銀行＋3保險＋1交易所",
        "來源：公開財報（yfinance）本頁彙整＋站內DD，個股數字 as-of 2026-08（鏡頭查證日；估值倍數已隔約一個月，判讀前請以最新報價為準）；"
        "隱含ROE缺口為本頁對Gordon Growth模型自算，股東權益成本假設9.5%、永續成長率假設3.5%。",
        l2_table,
        "銀行股沒有明顯的定價錯誤空間，十檔隱含ROE缺口幾乎都在±2pp內；真正值得花時間的角落是兩檔保險股與一檔控股折讓。",
    ))

    # 鏡頭三：收息
    l3_rows = [
        ["Focus Point（0157）", "殖利率5.77%／5年股息年化成長率（5Y CAGR）29.88%", "FCF覆蓋率3年均3.81倍，官方明文≥50%派息政策，2026年起改季配", "公開財報"],
        ["Telekom Malaysia（4863）", "殖利率4.71%／5Y CAGR 24.64%", "2026年起派息政策明文上修至稅後歸屬母公司淨利（PATAMI）的≥75%並改季配", "公開財報"],
        ["Westports（5246）", "殖利率3.09%／5Y CAGR 9.04%", "官方明文75%派息政策目標，現金流品質受惠於特許經營合約結構的可預測性", "DD_5246KL_20260811"],
        ["CIMB（1023）", "殖利率6.01%／5Y CAGR 10.41%", "銀行覆蓋以派息政策明文替代：目標約55%派付率", "公開財報"],
        ["RHB Bank（1066）", "殖利率5.75%／5Y CAGR 8.29%", "2025–2026新制明文上修至50–60%，實際派息率已超越指引上緣", "公開財報"],
        ["Public Bank（1295）", "殖利率4.37%／5Y CAGR 7.47%", "明文2025年目標60%（較2024年57%上修），近年逐步上修中", "公開財報"],
        ["Hong Leong Bank（5819）", "殖利率4.26%／5Y CAGR 11.49%", "27檔中唯一有向上調升時間表的銀行，規劃未來2–3年升至50–60%", "公開財報"],
        ["Heineken／Carlsberg Malaysia", "殖利率8.99%／7.15%，十年窗內各4–5次砍息", "2025-11啤酒稅上調10%為明確前瞻壓力，高殖利率與砍息紀錄並存", "公開財報"],
    ]
    l3_table = "<thead><tr><th>公司（代號）</th><th>關鍵數字</th><th>判讀</th><th>出處</th></tr></thead><tbody>" + "".join(trow(r) for r in l3_rows) + "</tbody>"
    out.append(lens_card(
        3, "收息：高息名單裡，真正禁得起考驗的供給有多窄",
        "殖利率排行榜前段的股票，有多少禁得起十年窗的砍息歷史檢驗？",
        "27檔收息候選做財年對齊的股息品質驗證後，最嚴格那一層是0檔——"
        "10檔的全部砍息紀錄完全落在2020年COVID窗內；真正站得住的供給是7檔成長息，其中四席是銀行股。",
        [
            "最嚴格那一層的判準要三項同時成立，缺一不可：①近十個完整財年窗內常規股息零減少；"
            "②自由現金流（或營運現金流）對股息的覆蓋率≥1.2倍；③有明文的派息政策地板。"
            "27檔全數在①就出局（十年窗內至少出現一次年減），所以0檔這個結果不是被②③卡掉的，"
            "而是砍息紀錄本身普遍存在——但其中10檔的砍息全部集中在同一個外部事件窗，判讀時要把這層區分開。",
            "方法：股息依所屬會計年度歸戶而非除息日的日曆年加總（避免橫跨12月／1月除息日的配息被拆進錯誤財年，產生假性砍息）；"
            "特別股息逐筆人工查證後才剔除，非自動門檻判定。",
            "10檔（CIMB、Maybank、RHB Bank、Public Bank、Hong Leong Bank、Takaful Malaysia、Padini、KLCCP Stapled、"
            "Gas Malaysia、PPB Group）的十年窗內全部砍息紀錄完全落在COVID窗（2020–2021）——這不是資料失敗，"
            "是馬股市場2020年普遍性股息削減的真實歷史事件。",
            "9檔「高息但脆」：殖利率不低，但十年窗內有COVID窗外的砍息紀錄，或現金流覆蓋率不足1倍——高殖利率與砍息紀錄可以並存，"
            "判讀高息名單前必須先看現金流量表覆蓋能力。",
            "3檔不合格（5年期成長率轉負且無正式明文派息政策地板）＋8檔無法歸類（上市史短或覆蓋率邊界案例）；"
            "個人股東全年股息所得超過RM10萬部分課徵2%股息稅（2025課稅年度起），資本利得仍維持免稅。",
        ],
        8, "收息階梯精選：7檔成長息與高息但脆的對照",
        "來源：公開財報（yfinance）本頁彙整＋站內DD，個股數字 as-of 2026-08（鏡頭查證日；估值倍數已隔約一個月，判讀前請以最新報價為準）；"
        "5年複合成長率統一採2019（疫情前常態年度，避開2020年低基期虛增成長率）為基期。",
        l3_table,
        "殖利率排行榜的排序邏輯只看配了多少，不看配得出來嗎；這個市場裡真正站得住的收息供給比表面殖利率排序窄得多。",
    ))

    # 鏡頭四：事件驅動
    l4_rows = [
        ["Genting Bhd（3182）／Genting Malaysia＋Genting Singapore", "控股折價56.3%，結構訊號僅2/6", "折價全表最深，但控制股東持股僅46.4%、流動性高，沒有被逼私有化的結構壓力", "本頁查證，2026-08-11前後SOTP估算"],
        ["Hong Leong Financial Group（1082）", "控股折價28.6%，結構訊號5/6", "控制股東持股80.7%、自由流通僅18.4%，逼近Bursa 25%公眾持股下限，另持有未上市保險資產未計入折價", "本頁查證"],
        ["Batu Kawan（1899）", "控股折價30.5%，結構訊號5/6", "控制股東持股83.1%、自由流通僅14.4%，深折價×控制股東×低流通三項疊加", "本頁查證"],
        ["IGB Berhad（5606）", "控股折價27.5%，結構訊號5/6", "控制股東持股78.1%、自由流通21.7%，母層淨負債未扣，實質折價會再收斂", "本頁查證"],
        ["GuocoLand Malaysia", "私有化溢價約RM1.10／股", "既有控股股東擴股型要約，已於2026-08-07完成私有化並下市", "GuocoLand公告，2026-08-07"],
        ["UEM Edgenta", "私有化每股RM1.10", "既有控股股東（UEM Group）擴股至100%，已於2026年7月完成下市", "UEM Edgenta公告，2026年7月"],
        ["Genting Malaysia", "Genting Bhd持股73.859%，逼近75%公眾持股界線", "Genting Bhd透過公開市場持續買入股份；跨過75%會違反Bursa的25%公眾持股規定（下市關卡），90%才是強制收購剩餘股份的門檻，兩者都尚未跨過，是本表最動態的一列", "本頁查證，2026-08前後"],
    ]
    l4_table = "<thead><tr><th>公司（代號）</th><th>關鍵數字</th><th>判讀</th><th>出處</th></tr></thead><tbody>" + "".join(trow(r) for r in l4_rows) + "</tbody>"
    out.append(lens_card(
        4, "事件驅動：折價深且管道活躍，但大股東出的溢價偏低",
        "深折價與活躍的私有化管道，是不是等於好機會？",
        "私有化管道活躍（2020–2026已知14件個案，已知結果的10件中成交9件），但14件裡只有6件查得溢價數字，"
        "這6件呈雙峰——政府關聯投資機構（GLIC）與既有控股股東給的溢價普遍偏低（0～10%量級），"
        "外部收購方才給較高溢價（17～34%）；控股折價最深達56.3%，但結構訊號最集中的是另一張名單。",
        [
            "私有化基率：2020–2026已知14件個案，收購方類型以GLIC／既有控股股東擴股型合計占約半數；"
            "已知結果的10件中成交9件，唯一未完成的是Genting Malaysia——收購要約結束時Genting Bhd持股73.855%，"
            "既沒有跨過Bursa上市規則的75%公眾持股界線（公眾持股須維持25%以上，是能否申請下市的關卡），"
            "也遠低於強制收購剩餘股份的90%門檻，公司因此仍掛牌。兩個門檻的用途不同，不可互相替換引用。",
            "溢價雙峰的樣本數要先講清楚：14件中僅6件查得溢價數字，且基準不一致（部分以最後交易價、部分以1個月或"
            "6個月成交量加權均價為基準），中位數約8.3%。GLIC／既有大股東的要約溢價偏低——如UEM Edgenta約0～1%、"
            "Malaysia Airports 5.8%；外部收購方明顯較高——如Tong Herr Resources 34.2%。6件的分布只能讀成方向性觀察，"
            "不足以做統計推論。方向本身是清楚的：等大股東要約拿到的多半不是套利溢價，"
            "這條路線的報酬來源是深折價被要約消滅，不是要約溢價本身。",
            "控股折價SOTP（Sum-of-the-Parts，母公司市值與其上市子公司持股市值加總後的差額）七組配對中，"
            "Genting Bhd折價最深達56.3%，但控制股東持股與流動性條件都不符合「易被逼私有化」的結構特徵——折價深不等於有事件在路上。",
            "六項結構訊號交叉篩查（P/B低、控制股東持股高、自由流通低、成交清淡、SOTP折價深、控制股東持股逼近Bursa 25%"
            "公眾持股下限）顯示，Batu Kawan、Hong Leong Financial Group、IGB Berhad三檔並列命中最多項，"
            "共同點是深折價×控制股東78–83%×自由流通14–22%。控制股東持股以yfinance的內部人持股欄位近似，"
            "自由流通量以「1減內部人持股」粗估，與Bursa官方公眾持股口徑不完全相同——訊號計數只讀相對排序，不讀絕對值。",
        ],
        9, "控股折價與私有化事件精選：七組SOTP配對與最新狀態",
        "來源：本頁對公開財報與交易所公告查證彙整；SOTP折價與結構訊號as-of 2026-08-11前後，"
        "GuocoLand／UEM Edgenta下市狀態as-of 2026-09；計數非推薦。",
        l4_table,
        "折價深不等於有事件在路上，結構訊號（控制股東持股高、自由流通低）比折價幅度本身更能預示私有化壓力；"
        "等大股東要約，拿到的多半是偏低的溢價，不是套利機會。",
    ))

    return "".join(out)


# ---------------------------------------------------------------------------
# 10. HTML 外殼
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


def main():
    uni = load_universe()
    facts = load_facts()
    stats = compute_population_stats(uni)
    nav_snippet = open(NAV_SNIPPET_PATH, encoding="utf-8").read()

    title = "馬股國家掃描：報酬寫在股息裡，價差十年為負 | InvestmQuest Research"
    description = (
        f"馬股國家掃描研究記錄：Bursa Malaysia主板市值≥RM20億共{stats['count']}檔母體"
        f"（總市值約{myr_zhao_from_raw(stats['total_mcap'])}）。五個論點——股息報酬、集中度與產業結構、"
        "估值分裂、收息、買盤結構與資金流——加上複利機器／金融／收息／事件驅動四個投資鏡頭，"
        "含4份站內既有DD對帳。掃描是研究記錄，不是選股名單。"
    )

    conc = stats["conc"]
    masthead_h1 = "馬股報酬寫在股息裡：十年價差為負，便宜的多是假象，貴的都已定價"
    masthead_subt = (
        f'本頁是 {stats["count"]} 檔馬股母體（Bursa Malaysia 主板普通股，市值≥RM20億）的市場結構掃描：'
        "五個論點＋馬股計分卡＋複利機器／金融／收息／事件驅動四個投資鏡頭，資料快照 " + SNAPSHOT_DATE +
        "，結構數字另附各自查證日期；本頁是研究記錄，不是投資建議，個股「值不值得投資」的裁決一律走站內DD統一裁決鏈。"
    )

    scorecard_html = build_scorecard(stats, facts)
    SCORECARD_N = build_scorecard.row_count

    body = []
    body.append('<div class="masthead"><div class="masthead-inner">')
    body.append('<div class="kicker">國家掃描 · 馬來西亞</div>')
    body.append(f'<h1>{masthead_h1}</h1>')
    body.append(f'<div class="subt">{masthead_subt}</div>')
    body.append('<div class="rule"></div>')
    body.append(
        '<div class="meta">'
        f'<span><b>掃描日期</b>　{SNAPSHOT_DATE}（資料快照，非持續更新）</span>'
        f'<span><b>母體</b>　Bursa Malaysia主板市值≥RM20億，共 {stats["count"]:,} 檔</span>'
        f'<span><b>覆蓋</b>　{stats["count"]:,} 檔母體 × 五個論點＋四個投資鏡頭</span>'
        '</div>'
    )
    body.append(
        '<div class="nature">本頁性質聲明：描述器／研究紀錄，非投資建議。五個論點與四個鏡頭收斂出的是判讀框架與'
        '資料事實，不是一張「買這些」的名單；個股「值不值得投資」的裁決一律走 DD 統一裁決鏈。</div>'
    )
    body.append('</div></div>')

    body.append('<div class="wrap">')

    body.append('<div class="exec-wrap"><div class="exec-hd">一頁摘要</div><ol class="exec">')
    body.append(build_exec_summary(stats, facts))
    body.append('</ol></div>')

    body.append('<div class="kdstrip">')
    body.append(f'<div><div class="kl">母體規模（Bursa主板≥RM20億）</div><div class="kv">{stats["count"]:,} 檔</div></div>')
    body.append(f'<div><div class="kl">母體總市值</div><div class="kv">{myr_zhao_from_raw(stats["total_mcap"])}</div></div>')
    body.append(f'<div><div class="kl">KLCI十年純價格報酬</div><div class="kv">{facts["klci_10y_price_return_pct"]["value"]:.1f}%</div></div>')
    body.append(f'<div><div class="kl">外資持股占大盤市值比重</div><div class="kv">{facts["foreign_holding_share_pct"]["value"]}%</div></div>')
    body.append(f'<div><div class="kl">站內DD覆蓋</div><div class="kv">4 份</div></div>')
    body.append('</div>')

    toc_items = [
        ("s1", f"馬股計分卡：{SCORECARD_N} 個指標速覽"),
        ("s2", "五個論點：股息報酬、集中度、估值分裂、收息、資金流"),
        ("s3", "四個投資鏡頭：複利機器、金融、收息、事件驅動"),
        ("s4", "可作戰名單：已有裁決與零覆蓋候選"),
        ("s5", "會推翻本頁判斷的證據"),
        ("s6", "資料、方法與盲區"),
    ]
    body.append('<div class="toc"><div class="toc-hd">報告目錄</div><ol>')
    for i, (anchor, label) in enumerate(toc_items, 1):
        body.append(f'<li><a href="#{anchor}"><span class="n">§{i}</span>{label}</a></li>')
    body.append('</ol></div>')

    body.append(f'<div class="section" id="s1"><div class="section-hd"><div class="sec-eyebrow">Section I</div><h2>§1　馬股計分卡：{SCORECARD_N} 個指標速覽</h2></div>')
    body.append('<div class="section-lead">母體算得出來的直接算，算不出來的查證後標明來源與查證日期；查不到的在「資料、方法與盲區」自陳，不沿用沒有出處的數字。</div>')
    body.append('<div class="exhibit scroll"><table><thead><tr><th>指標</th><th>數值</th><th>as-of</th><th>白話一句</th><th>來源</th></tr></thead><tbody>')
    body.append(scorecard_html)
    body.append('</tbody></table></div>')
    body.append('</div>')

    body.append('<div class="section" id="s2"><div class="section-hd"><div class="sec-eyebrow">Section II</div><h2>§2　五個論點：這個市場現在是什麼</h2></div>')
    body.append('<div class="section-lead">每個論點都是可以被推翻的具體主張，不是氣氛描述；推翻條件見§5。</div>')
    body.append(build_arguments(stats, facts))
    body.append('</div>')

    body.append('<div class="section" id="s3"><div class="section-hd"><div class="sec-eyebrow">Section III</div><h2>§3　四個投資鏡頭</h2></div>')
    body.append('<div class="section-lead">每個鏡頭問一個獨立的問題，事實、名單與出處逐檔可查；本頁沒有子頁，鏡頭卡是完整內容而非摘要。</div>')
    body.append(build_lenses())
    body.append('</div>')

    body.append('<div class="section" id="s4"><div class="section-hd"><div class="sec-eyebrow">Section IV</div><h2>§4　可作戰名單：已有裁決與零覆蓋候選</h2></div>')
    body.append('<div class="section-lead">站內裁決逐字取自各檔案的決策層欄位（訊號等級與裁決／角色），「在等什麼」欄位逐字取自'
                 '各檔的重評估觸發條件欄位，連縮寫與標點都照抄、不改寫不總結；同一家公司一律取日期最新的那一份。'
                 '欄內以金色標示的「本頁補註」是本頁為逐字內容補上的白話解釋，不屬於原裁決文字。'
                 '本頁不給買賣指令，個股「值不值得投資」一律點進 DD 查完整推理。</div>')
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


def build_exec_summary(stats, facts):
    conc = stats["conc"]
    items = [
        f'<b>KLCI十年純價格報酬為負，含息才轉正</b>——KLCI（富時大馬綜合指數，Bursa Malaysia市值最大的30檔成分股組成）'
        f'2015-06-30至2025-06-30純價格報酬{facts["klci_10y_price_return_pct"]["value"]:.2f}%'
        f'（不含股息，本頁對yfinance日線收盤自算），含息總報酬估算約{klci_total_return_estimate(stats, facts):+.1f}%'
        f'（以母體殖利率中位數{stats["dy_median"]:.2f}%十年複利估算，非官方含息指數）——馬股報酬幾乎全部來自股息，不是價差。',

        f'<b>金融服務業以少數家數拿下母體最大市值占比</b>——本頁{stats["count"]}檔母體中金融服務業僅占家數'
        f'{stats["fin_count_pct"]:.1f}%（{stats["fin_n"]}檔），卻拿下母體市值{stats["fin_pct"]:.1f}%'
        f'（{SNAPSHOT_DATE}快照，本頁自算）；前十大個股合計占母體市值{conc[10]["pct"]:.1f}%。',

        "<b>127檔量化篩選出14檔複利機器候選，但榜首是計算假象</b>——QL Resources增量投入資本報酬率"
        "（增量ROIC，衡量新投入的每一塊資本賺回多少報酬，分母是四年間投入資本的淨增加額）515.62%"
        "源自小分母雜訊，真實最新年ROIC僅14.07%；扣除假象後真正站得住的複利機器（Frontken、Kelington）"
        "已被市場充分定價，出口科技群十檔trailing本益比47.8–109.8倍，全數距52週高在20%以內。",

        "<b>金融股定價大體有效率，錯價在保險與控股折讓角落</b>——10檔銀行的隱含ROE（用Gordon Growth模型從"
        "股價淨值比反推的股東權益報酬率）缺口（pp＝百分點）多數落在±2pp以內；真正的錯價集中在保險股（Takaful Malaysia "
        "-6.5pp）與控股折讓（Hong Leong Financial Group -2.9～-3.2pp）兩個角落。",

        f'<b>高息名單與真正禁得起考驗的收息股是兩批不同的名字</b>——母體殖利率≥6%者{stats["dy6_n"]}檔'
        f'（{stats["dy6_pct"]:.1f}%），但27檔收息驗證階梯裡，同時滿足三項判準（近十個完整財年常規股息零減少、'
        "自由現金流對股息覆蓋率≥1.2倍、有明文派息政策地板）的是0檔，卡點在第一項——27檔全數在十年窗內至少砍過一次息，"
        "其中10檔的砍息紀錄完全落在2020年COVID窗內；真正站得住的供給是7檔成長息，其中四席是銀行股。",

        f'<b>外資八個完整年度賣了七年，2026年還在賣</b>——外資持股占大盤市值比重'
        f'{facts["foreign_holding_share_pct"]["value"]}%（{facts["foreign_holding_share_pct"]["as_of"]}），'
        "較2018年高點24.2%明顯下滑；2018–2025八個完整年度中七年全年淨賣超（唯一例外是2022年淨買超RM44.0億），"
        f'2026年初至2026-09-03再淨賣超RM{abs(facts["foreign_net_flow_annual"]["value"]["2026_ytd_0903"])*10:.1f}億，'
        "同期本地機構淨買超RM51.1億承接——邊際定價權正在從外資移向本地法人。",

        "<b>私有化管道活躍，但大股東出的溢價偏低</b>——2020–2026已知14件私有化個案，已知結果的10件中成交9件；"
        "14件裡只有6件查得溢價數字（基準不一致，中位數約8.3%），這6件呈雙峰：政府關聯投資機構與既有控股股東的"
        "要約溢價普遍偏低（0～10%量級），外部收購方才給較高溢價（17～34%）——樣本小只讀方向不做統計推論；"
        "控股折價（母公司市值低於其持有的上市子公司股權市值的差額）最深達56.3%（Genting Bhd），"
        "但結構訊號最集中的是Batu Kawan／Hong Leong Financial Group／IGB Berhad三檔（六項結構訊號中5項命中）。",

        f'<b>2026上半年IPO家數與募資額同步登上東協第一</b>——{facts["ipo_1h2026_count_and_amount"]["as_of"]}'
        "共36家IPO募資RM54億、新增市值RM261億，Bursa Malaysia官方新聞稿自陳排名，本頁未獨立查證；"
        f'個人股東全年股息所得超過RM10萬部分課徵2%股息稅（{facts["dividend_tax_2pct"]["as_of"]}），'
        "資本利得仍維持免稅——制度設計仍是重股息、輕價差。",
    ]
    return "".join(f"<li>{x}</li>" for x in items)


# ---------------------------------------------------------------------------
# 11. 自檢：--check
# ---------------------------------------------------------------------------

# 「護城河」是既有的標準投資術語，不列入禁用比喻。
BANNED_METAPHOR_WORDS = ["煞车", "煞車", "收費站", "水庫", "半壁江山", "斷層帶", "藏寶圖", "尋寶",
                          "鴻溝", "雙面刃", "硬幣兩面", "賽道", "像座", "彷彿", "宛如",
                          "壓艙石", "壓艙", "母語", "地板價", "天花板", "籃子", "死法", "引擎", "資金潮",
                          "接盤", "撐盤", "彩票"]
BANNED_PROCESS_WORDS = ["sonnet", "Sonnet", "opus", "Opus", "agent", "Agent", "critic", "orchestrator",
                         "本輪", "上一版", "舊版", "重寫"]
BANNED_CROSS_MARKET_WORDS = ["美國", "美股", "S&P", "台灣", "台股", "TWSE", "日本", "東證", "TOPIX",
                              "韓國", "Korea", "新加坡", "泰國", "印尼", "新馬", "星馬", "區域同業"]
BANNED_TRADE_CALL_WORDS = ["買進", "賣出", "加碼", "減碼", "停損", "目標價"]
BANNED_INTERNAL_FILENAMES = ["_universe.json", "_hub_facts.json", "_universe_report.md",
                              "_build_hub.py", "_critic_hub", "_nav_snippet.html"]


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
    # 逐字引用自站內 DD 的裁決觸發條件不套用「不給買賣指令」檢查：那是引號內的原文，
    # 不是本頁自己的話；其餘檢查（比喻／流程語氣／跨市場／內部檔名）仍照掃。
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
        print(f"（提示）以下字樣只出現在逐字引用的站內 DD 裁決文字內，未計為問題：{quoted_calls}")

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

    for key in ("klci_10y_price_return_pct", "foreign_holding_share_pct", "opr_current"):
        raw = facts[key]["value"]
        candidates = {str(raw)}
        if isinstance(raw, (int, float)):
            candidates.add(f"{raw:.2f}")
            candidates.add(f"{raw:.1f}")
        if isinstance(raw, str):
            candidates.add(raw)
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
        (f'{stats["fin_pct"]:.1f}%', "金融服務業占母體市值"),
        (f'{stats["fpe_all"]["median"]:.1f}倍', "母體前瞻本益比中位數"),
        (f'{stats["dy_median"]:.2f}%', "母體殖利率中位數"),
        (f'{stats["dy6_n"]}檔', "殖利率≥6%檔數"),
        (myr_zhao_from_raw(stats["total_mcap"]), "母體總市值"),
        (f'{stats["conc"][10]["pct"]:.1f}%', "前十大個股占母體市值"),
    ]
    for expect, label in pop_checks:
        if add_cjk_latin_spacing(expect) not in plain:
            problems.append(f"母體數字檢查失敗：{label} 應出現「{expect}」")

    dd_dir = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "docs", "dd"))
    if os.path.isdir(dd_dir):
        all_dd = os.listdir(dd_dir)
        for r in WATCH_EXISTING:
            pat = re.compile(r"^DD_%sKL_(\d{8})\.html$" % re.escape(r["t"]))
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
            {k: v for k, v in stats.items() if k not in ("sector_rows", "top_sectors", "sector_pe_rows", "dy_hist")},
            ensure_ascii=False, indent=2, default=str,
        ))
    elif "--check-only" in sys.argv:
        run_check(OUT_PATH)
    else:
        main_cli()
