#!/usr/bin/env python3
"""
美股國家掃描 hub 組裝腳本（重寫 2026-09-10）。

Usage:
  /opt/homebrew/bin/python3.12 _build_hub.py            # 產出 docs/backtest/country_scan/us.html
  /opt/homebrew/bin/python3.12 _build_hub.py --check    # 產出後跑自檢，不重新寫檔亦可單獨執行

只用標準庫（json / statistics / math / re / os）。母體數字一律從 _universe.json 現算；
非母體的結構數字（SSGA 權重、回購金額、ERP……）一律從 _hub_facts.json 讀取，每筆都帶
value / as_of / source_name / source_url / confidence，禁止在內文手打數字。
"""
import json
import math
import os
import re
import statistics as st
import sys
from collections import defaultdict, OrderedDict

BASE = os.path.dirname(os.path.abspath(__file__))
UNIVERSE_PATH = os.path.join(BASE, "_universe.json")
FACTS_PATH = os.path.join(BASE, "_hub_facts.json")
NAV_SNIPPET_PATH = os.path.join(BASE, "_nav_snippet.html")
OUT_PATH = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "docs", "backtest", "country_scan", "us.html"))

SNAPSHOT_DATE = "2026-08-15"
DD_BASIS_DATE = "2026-08-15"

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

def fmt_pct(x, nd=1):
    return f"{x:.{nd}f}%"


def fmt_x(x, nd=1):
    return f"{x:.{nd}f}倍"


def usd_bn_to_str(bn):
    """billions(usd_bn) -> 「US$X兆」或「US$Y億」，兩種同時附上避免億/兆手誤。"""
    yi = bn * 10.0
    zhao = bn / 1000.0
    if zhao >= 0.1:
        return f"US${zhao:,.2f}兆（US${yi:,.0f}億）" if zhao < 1 else f"US${zhao:,.2f}兆"
    return f"US${yi:,.0f}億"


def usd_from_raw(v):
    """原始美元數字（如 market_cap 83966129280192）-> 「US$X兆」。"""
    zhao = v / 1e12
    return f"US${zhao:,.2f}兆"


# ---------------------------------------------------------------------------
# 2. 母體統計（全部從 _universe.json 現算）
# ---------------------------------------------------------------------------

def compute_population_stats(uni):
    cons = uni["constituents"]
    total_mcap = sum(c["market_cap"] for c in cons if c.get("market_cap"))
    count = len(cons)

    srt = sorted(cons, key=lambda c: -(c.get("market_cap") or 0))

    def topn_share(n):
        s = sum(c["market_cap"] for c in srt[:n])
        return s, s / total_mcap * 100

    conc = {}
    for n in (10, 50, 100):
        s, p = topn_share(n)
        conc[n] = {"mcap": s, "pct": p}
    conc["rest"] = {"pct": 100 - conc[100]["pct"]}
    conc["top10_tickers"] = [c["ticker"] for c in srt[:10]]

    # GICS 產業市值（含補充名單獨立一類）
    sec = defaultdict(float)
    seccount = defaultdict(int)
    for c in cons:
        g = c.get("gics_sector")
        mc = c.get("market_cap") or 0
        key = g if g else "補充名單（無官方 GICS 分類）"
        sec[key] += mc
        seccount[key] += 1
    sector_rows = sorted(
        ({"sector": k, "mcap": v, "pct": v / total_mcap * 100, "n": seccount[k]} for k, v in sec.items()),
        key=lambda r: -r["pct"],
    )

    # 前瞻本益比：依指數分層（500/400/600），排除缺值與非正值
    def pe_stats(idx):
        vals = sorted(
            c["forward_pe"]
            for c in cons
            if c.get("index_membership") == idx and c.get("forward_pe") is not None and c["forward_pe"] > 0
        )
        n = len(vals)
        return {
            "n": n,
            "median": st.median(vals),
            "q1": vals[n // 4],
            "q3": vals[(3 * n) // 4],
            "min": vals[0],
            "max": vals[-1],
        }

    pe_by_group = {idx: pe_stats(idx) for idx in ("SP500", "SP400", "SP600")}
    all_pe = sorted(c["forward_pe"] for c in cons if c.get("forward_pe") is not None and c["forward_pe"] > 0)
    pe_all_median = st.median(all_pe)

    # ROE 全母體中位數
    all_roe = [c["roe"] for c in cons if c.get("roe") is not None]
    roe_all_median = st.median(all_roe) * 100

    # ROE 中位數：GICS 產業 x 指數分層（500/400/600）
    roe_data = defaultdict(lambda: defaultdict(list))
    for c in cons:
        idx = c.get("index_membership")
        g = c.get("gics_sector")
        if idx in ("SP500", "SP400", "SP600") and g and c.get("roe") is not None:
            roe_data[g][idx].append(c["roe"])
    roe_rows = []
    for g, byidx in roe_data.items():
        row = {"sector": g}
        for idx in ("SP500", "SP400", "SP600"):
            vals = byidx.get(idx, [])
            row[idx] = {"n": len(vals), "median": (st.median(vals) * 100 if vals else None)}
        roe_rows.append(row)
    roe_rows.sort(key=lambda r: r["SP500"]["median"] if r["SP500"]["median"] is not None else -999)

    # 規模遞增/遞減計數（500>400>600 的產業數）給論點 D 用
    inc_count = 0
    checked = 0
    for r in roe_rows:
        m500, m600 = r["SP500"]["median"], r["SP600"]["median"]
        if m500 is not None and m600 is not None:
            checked += 1
            if m500 > m600:
                inc_count += 1

    # 個股層級數字（供 Exhibit 3 極端值標註）
    def find(ticker):
        for c in cons:
            if c["ticker"] == ticker:
                return c
        return None

    net = find("NET")
    adbe = find("ADBE")

    return {
        "sector_pct": {r["sector"]: r["pct"] for r in sector_rows},
        "total_mcap": total_mcap,
        "count": count,
        "counts_by_group": uni["meta"]["counts"],
        "conc": conc,
        "sector_rows": sector_rows,
        "pe_by_group": pe_by_group,
        "pe_all_median": pe_all_median,
        "roe_all_median": roe_all_median,
        "roe_rows": roe_rows,
        "roe_inc_count": inc_count,
        "roe_checked": checked,
        "net_fwd_pe": net["forward_pe"],
        "adbe_fwd_pe": adbe["forward_pe"],
        "net_mcap": net["market_cap"],
        "adbe_mcap": adbe["market_cap"],
    }


# ---------------------------------------------------------------------------
# 3. SVG 圖表（內嵌、全寬、大字、柔和色，色票取自頁面既有 CSS 變數）
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

GICS_SECTOR_ZH = {
    "Information Technology": "資訊科技",
    "Communication Services": "通訊服務",
    "Financials": "金融",
    "Consumer Discretionary": "非必需消費",
    "Industrials": "工業",
    "Health Care": "醫療保健",
    "Consumer Staples": "必需消費",
    "Energy": "能源",
    "Real Estate": "不動產",
    "Utilities": "公用事業",
    "Materials": "原物料",
}


def sector_zh(name):
    return GICS_SECTOR_ZH.get(name, name)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def svg_wrap(inner, height, label):
    return (
        f'<svg viewBox="0 0 {SVG_W} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}" '
        f'style="display:block;font-family:\'IBM Plex Mono\',ui-monospace,monospace">{inner}</svg>'
    )


def svg_exhibit1(stats):
    """論點A：集中度累積曲線（100%堆疊條）＋ GICS產業市值長條。"""
    conc = stats["conc"]
    segs = [
        ("前 10 檔", conc[10]["pct"], C_ACCENT),
        ("第 11–50 檔", conc[50]["pct"] - conc[10]["pct"], C_ACCENT2),
        ("第 51–100 檔", conc[100]["pct"] - conc[50]["pct"], C_GOLD),
        ("第 101–1590 檔", conc["rest"]["pct"], "#cfc9b8"),
    ]
    bar_x, bar_y, bar_w, bar_h = 20, 46, SVG_W - 40, 46
    parts = []
    parts.append(f'<text x="{bar_x}" y="24" font-size="14" font-weight="700" fill="{C_INK}">母體市值累積占比（依市值排序，1,590檔＝100%）</text>')
    x = bar_x
    for name, pct, color in segs:
        w = bar_w * pct / 100
        parts.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" fill="{color}"/>')
        if w > 46:
            tx = x + w / 2
            parts.append(
                f'<text x="{tx:.1f}" y="{bar_y+bar_h/2+5}" font-size="13" font-weight="700" '
                f'fill="#fff" text-anchor="middle">{pct:.1f}%</text>'
            )
        x += w
    # legend below bar
    ly = bar_y + bar_h + 26
    lx = bar_x
    for name, pct, color in segs:
        parts.append(f'<rect x="{lx}" y="{ly-11}" width="12" height="12" fill="{color}"/>')
        parts.append(f'<text x="{lx+17}" y="{ly}" font-size="11.5" fill="{C_BODY}">{esc(name)}</text>')
        lx += 17 + len(name) * 12 + 26

    # 第二區塊：GICS 產業市值長條
    sec_y0 = ly + 34
    parts.append(f'<text x="{bar_x}" y="{sec_y0}" font-size="14" font-weight="700" fill="{C_INK}">母體市值依 GICS 產業分布（含補充名單獨立一類）</text>')
    rows = stats["sector_rows"]
    row_h = 26
    max_pct = max(r["pct"] for r in rows)
    label_w = 200
    chart_x = bar_x + label_w
    chart_w = bar_w - label_w - 70
    y = sec_y0 + 18
    for r in rows:
        w = chart_w * r["pct"] / max_pct
        bar_color = C_GOLD_DEEP if "補充" in r["sector"] else C_ACCENT
        lbl = "補充名單" if "補充" in r["sector"] else sector_zh(r["sector"])
        parts.append(f'<text x="{bar_x}" y="{y+row_h*0.62:.1f}" font-size="11.5" fill="{C_BODY}">{esc(lbl)}（{r["n"]}檔）</text>')
        parts.append(f'<rect x="{chart_x}" y="{y+4}" width="{w:.1f}" height="{row_h-12}" rx="2" fill="{bar_color}"/>')
        parts.append(f'<text x="{chart_x+w+8:.1f}" y="{y+row_h*0.62:.1f}" font-size="11.5" font-weight="700" fill="{C_INK}">{r["pct"]:.2f}%</text>')
        y += row_h
    total_h = y + 14
    return svg_wrap("".join(parts), total_h, "母體市值集中度與GICS產業分布")


def svg_exhibit2(facts):
    """論點B：capex年增率 vs 對應業務營收年增率，五家公司成對長條。"""
    rows = sorted(
        ((t, facts[f"capex_ai_{t.lower()}"]) for t in ("ORCL", "META", "AMZN", "MSFT", "GOOGL")),
        key=lambda r: -(r[1]["capex_yoy_pct"] / r[1]["revenue_yoy_pct"]),
    )
    bar_x, top, bar_w = 24, 40, SVG_W - 48
    label_w0 = 64
    max_v = max(max(r["capex_yoy_pct"], r["revenue_yoy_pct"]) for _, r in rows)
    # 保留最長那根柱後面約 190px 給文字標籤，避免最大值（ORCL）把標籤擠出畫布
    scale = (bar_w - label_w0 - 190) / max_v
    group_h = 58
    parts = [f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">AI 資本支出年增率 vs 對應業務營收年增率（依差距倍數由大到小）</text>']
    y = top
    for name, r in rows:
        cap = r["capex_yoy_pct"]
        rev = r["revenue_yoy_pct"]
        multiple = cap / rev
        label_w = 64
        cx = bar_x + label_w
        parts.append(f'<text x="{bar_x}" y="{y+14}" font-size="12.5" font-weight="700" fill="{C_INK}">{name}</text>')
        # capex bar (gold)
        w1 = cap * scale
        parts.append(f'<rect x="{cx}" y="{y}" width="{w1:.1f}" height="16" rx="2" fill="{C_GOLD}"/>')
        parts.append(f'<text x="{cx+w1+6:.1f}" y="{y+12}" font-size="11" fill="{C_INK}">資本支出 +{cap:.1f}%</text>')
        # revenue bar (navy)
        w2 = rev * scale
        parts.append(f'<rect x="{cx}" y="{y+20}" width="{w2:.1f}" height="16" rx="2" fill="{C_ACCENT}"/>')
        seg = r["revenue_segment"]
        parts.append(f'<text x="{cx+w2+6:.1f}" y="{y+32}" font-size="11" fill="{C_SEC}">{esc(seg)} +{rev:.1f}%</text>')
        parts.append(f'<text x="{bar_x}" y="{y+46}" font-size="11" font-weight="700" fill="{C_GOLD_DEEP}">差距 {multiple:.1f} 倍</text>')
        y += group_h
    # legend
    parts.append(f'<rect x="{bar_x}" y="{y+4}" width="12" height="12" fill="{C_GOLD}"/>')
    parts.append(f'<text x="{bar_x+17}" y="{y+14}" font-size="11" fill="{C_BODY}">資本支出年增率</text>')
    parts.append(f'<rect x="{bar_x+150}" y="{y+4}" width="12" height="12" fill="{C_ACCENT}"/>')
    parts.append(f'<text x="{bar_x+167}" y="{y+14}" font-size="11" fill="{C_BODY}">對應業務營收年增率</text>')
    total_h = y + 30
    return svg_wrap("".join(parts), total_h, "AI資本支出年增率與對應業務營收年增率對照")


def svg_exhibit3(stats):
    """論點C：前瞻本益比分布（Q1-中位數-Q3），三組指數＋NET/ADBE極端值標註。"""
    groups = [
        ("S&P 500（大型股）", stats["pe_by_group"]["SP500"]),
        ("S&P 400（中型股）", stats["pe_by_group"]["SP400"]),
        ("S&P 600（小型股）", stats["pe_by_group"]["SP600"]),
    ]
    axis_max = 45.0  # 超過此值以溢出箭頭標註，避免極端值把座標軸拉爆
    bar_x, chart_w = 170, SVG_W - 170 - 90
    top = 44
    row_h = 54
    parts = [
        f'<text x="20" y="20" font-size="14" font-weight="700" fill="{C_INK}">前瞻本益比分布（第一四分位—中位數—第三四分位，超出 {axis_max:.0f} 倍以外用箭頭標示）</text>'
    ]
    def xpos(v):
        return bar_x + min(v, axis_max) / axis_max * chart_w

    # axis ticks
    for t in (0, 10, 20, 30, 40):
        tx = xpos(t)
        parts.append(f'<line x1="{tx:.1f}" y1="{top-6}" x2="{tx:.1f}" y2="{top + row_h*3+6}" stroke="{C_BORDER}" stroke-width="1"/>')
        parts.append(f'<text x="{tx:.1f}" y="{top-10}" font-size="10" fill="{C_SEC}" text-anchor="middle">{t}倍</text>')

    y = top
    for name, g in groups:
        parts.append(f'<text x="20" y="{y+row_h/2+5:.1f}" font-size="12" fill="{C_BODY}">{esc(name)}</text>')
        x1, xm, x3 = xpos(g["q1"]), xpos(g["median"]), xpos(g["q3"])
        parts.append(f'<line x1="{x1:.1f}" y1="{y+row_h/2:.1f}" x2="{x3:.1f}" y2="{y+row_h/2:.1f}" stroke="{C_ACCENT2}" stroke-width="6" stroke-linecap="round"/>')
        parts.append(f'<circle cx="{xm:.1f}" cy="{y+row_h/2:.1f}" r="7" fill="{C_GOLD_DEEP}"/>')
        parts.append(f'<text x="{xm:.1f}" y="{y+row_h/2-14:.1f}" font-size="11.5" font-weight="700" fill="{C_INK}" text-anchor="middle">中位數 {g["median"]:.1f}倍</text>')
        parts.append(f'<text x="{x1:.1f}" y="{y+row_h/2+22:.1f}" font-size="10" fill="{C_SEC}" text-anchor="middle">{g["q1"]:.1f}</text>')
        parts.append(f'<text x="{x3:.1f}" y="{y+row_h/2+22:.1f}" font-size="10" fill="{C_SEC}" text-anchor="middle">{g["q3"]:.1f}</text>')
        y += row_h

    # NET / ADBE 極端值標註（另起一列）
    y += 6
    parts.append(f'<text x="20" y="{y+row_h/2+5:.1f}" font-size="12" fill="{C_BODY}">個股極端例</text>')
    xa = xpos(stats["adbe_fwd_pe"])
    parts.append(f'<circle cx="{xa:.1f}" cy="{y+row_h/2:.1f}" r="6" fill="{C_ACCENT}"/>')
    parts.append(f'<text x="{xa:.1f}" y="{y+row_h/2+22:.1f}" font-size="11" font-weight="700" fill="{C_ACCENT}" text-anchor="middle">ADBE {stats["adbe_fwd_pe"]:.1f}倍</text>')
    # NET 超出座標軸，畫箭頭
    xn = xpos(axis_max) - 4
    parts.append(f'<circle cx="{xn:.1f}" cy="{y+row_h/2:.1f}" r="6" fill="{C_GOLD_DEEP}"/>')
    parts.append(f'<path d="M {xn+6:.1f} {y+row_h/2:.1f} L {xn+22:.1f} {y+row_h/2-5:.1f} L {xn+22:.1f} {y+row_h/2+5:.1f} Z" fill="{C_GOLD_DEEP}"/>')
    parts.append(f'<text x="{xn-4:.1f}" y="{y+row_h/2+22:.1f}" font-size="11" font-weight="700" fill="{C_GOLD_DEEP}" text-anchor="end">NET {stats["net_fwd_pe"]:.0f}倍 →</text>')
    y += row_h + 6
    return svg_wrap("".join(parts), y, "前瞻本益比分布三組對照與極端值")


def svg_exhibit4(stats):
    """論點D：ROE中位數，11個GICS產業 x 3組指數，橫向分組長條。"""
    rows = stats["roe_rows"]
    bar_x, label_w = 20, 150
    chart_x = bar_x + label_w
    chart_w = SVG_W - chart_x - 60
    max_v = 40.0
    row_h = 48
    sub_h = 12
    top = 38
    parts = [f'<text x="{bar_x}" y="18" font-size="14" font-weight="700" fill="{C_INK}">ROE 中位數：11 個 GICS 產業 × 大型股／中型股／小型股（負股東權益極端值以中位數天然排除）</text>']
    def xpos(v):
        return chart_w * min(v, max_v) / max_v

    series = [("SP500", "大型股 S&P 500", C_ACCENT), ("SP400", "中型股 S&P 400", C_ACCENT2), ("SP600", "小型股 S&P 600", C_GOLD)]
    y = top
    for r in rows:
        parts.append(f'<text x="{bar_x}" y="{y+row_h/2+4:.1f}" font-size="12.5" fill="{C_BODY}">{esc(sector_zh(r["sector"]))}</text>')
        sy = y + 3
        for key, _, color in series:
            v = r[key]["median"]
            if v is not None:
                w = xpos(v)
                parts.append(f'<rect x="{chart_x}" y="{sy:.1f}" width="{w:.1f}" height="{sub_h}" fill="{color}"/>')
                parts.append(f'<text x="{chart_x+w+6:.1f}" y="{sy+sub_h-1.5:.1f}" font-size="12" fill="{C_INK}">{v:.1f}%</text>')
            sy += sub_h + 3
        y += row_h
    # legend
    ly = y + 10
    lx = bar_x + label_w
    for key, name, color in series:
        parts.append(f'<rect x="{lx}" y="{ly-11}" width="13" height="13" fill="{color}"/>')
        parts.append(f'<text x="{lx+18}" y="{ly}" font-size="12" fill="{C_BODY}">{esc(name)}</text>')
        lx += 18 + len(name) * 12 + 26
    total_h = ly + 14
    return svg_wrap("".join(parts), total_h, "ROE中位數依GICS產業與指數分層對照")


def svg_exhibit5(facts):
    """論點E：企業回購季度走勢＋近12個月回購/配息對照。"""
    q = [
        ("2025 Q1", facts["buyback_q1_2025_usd_bn"]["value"]),
        ("2025 Q2", facts["buyback_q2_2025_usd_bn"]["value"]),
        ("2025 Q3", facts["buyback_q3_2025_usd_bn"]["value"]),
    ]
    bar_x, top = 24, 40
    chart_w = 360
    max_v = max(v for _, v in q) * 1.15
    parts = [f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">S&amp;P 500 企業季度庫藏股買回金額</text>']
    bw = 76
    gap = 30
    base_y = top + 150
    x = bar_x
    for name, v in q:
        h = 150 * v / max_v
        parts.append(f'<rect x="{x}" y="{base_y-h:.1f}" width="{bw}" height="{h:.1f}" rx="3" fill="{C_ACCENT}"/>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{base_y-h-8:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">US${v*10:,.0f}億</text>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{base_y+16:.1f}" font-size="11.5" fill="{C_SEC}" text-anchor="middle">{name}</text>')
        x += bw + gap

    # 右側：近12個月回購 vs 配息
    x2 = bar_x + chart_w + 60
    parts.append(f'<text x="{x2}" y="20" font-size="14" font-weight="700" fill="{C_INK}">2024-10～2025-09 合計</text>')
    ttm_buy = facts["buyback_ttm_usd_tn"]["value"] * 10000  # 兆 -> 億
    ttm_div = facts["dividend_ttm_usd_bn"]["value"] * 10  # billions -> 億
    max_v2 = ttm_buy * 1.15
    bw2 = 90
    base_y2 = base_y
    labels2 = [("回購", ttm_buy, C_GOLD_DEEP), ("配息", ttm_div, C_ACCENT2)]
    xx = x2
    for name, v, color in labels2:
        h = 150 * v / max_v2
        parts.append(f'<rect x="{xx}" y="{base_y2-h:.1f}" width="{bw2}" height="{h:.1f}" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{xx+bw2/2:.1f}" y="{base_y2-h-8:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">US${v/10000:,.2f}兆</text>')
        parts.append(f'<text x="{xx+bw2/2:.1f}" y="{base_y2+16:.1f}" font-size="11.5" fill="{C_SEC}" text-anchor="middle">{name}</text>')
        xx += bw2 + 40
    ratio = ttm_buy / ttm_div
    parts.append(f'<text x="{x2}" y="{base_y2+40}" font-size="11" fill="{C_GOLD_DEEP}" font-weight="700">回購／配息 ≈ {ratio:.2f} 倍</text>')

    total_h = base_y + 56
    return svg_wrap("".join(parts), total_h, "S&P500企業回購與配息規模")


# ---------------------------------------------------------------------------
# 4. 內文組裝：一頁摘要／計分卡／五個論點卡／九鏡頭表／可作戰名單／琥珀卡／方法論
# ---------------------------------------------------------------------------

DD_BASE = "https://research.investmquest.com/backtest/country_scan/us"
DD_DOC_BASE = "https://research.investmquest.com/dd"


def name_tag(cn_or_en, ticker):
    return f"{esc(cn_or_en)}（{ticker}）"


def build_exec_summary(stats, facts):
    conc = stats["conc"]
    items = [
        f'<b>前十大股票拿走超過三分之一的指數權重</b>——S&amp;P 500 前十大合計權重 {facts["spy_top10_weight_pct"]["value"]}%'
        f'（as-of {facts["spy_top10_weight_pct"]["as_of"]}；Alphabet 一家公司有 A、C 兩類股票各占一席，所以「前十大」是十檔股票、九家公司），'
        f'Mag 7（NVIDIA、Apple、Microsoft、Amazon、Alphabet 兩類股票、Meta、Tesla 八檔股票的合稱）合計占 '
        f'{facts["mag7_weight_pct"]["value"]}%；資訊科技在 S&amp;P 500 的權重達 {facts["sector_weight_it_pct"]["value"]}%，'
        f'是 11 個 GICS 產業（全球產業分類標準，S&amp;P 與 MSCI 共同制定的產業分類系統）中最大的一個。'
        f'本頁 1,590 檔母體依市值排序，前十檔即占母體總市值 {conc[10]["pct"]:.1f}%'
        f'（{SNAPSHOT_DATE}快照，本頁自算）。',

        f'<b>五家公司投同一個 AI 題材，收入跟上的速度差 8 倍</b>——把資本支出（企業用於建置資料中心、伺服器等長期資產的支出）'
        f'年增率除以對應業務營收年增率，Alphabet 只有 1.2 倍（Google Cloud 營收年增 82.4%，幾乎跟上投資速度），'
        f'Oracle 是 9.3 倍（整體營收僅年增 17.4%）。Oracle FY2026 自由現金流（公司在支付營運與資本支出後實際留下的現金）'
        f'−US$2,370 億，前一年只有 −US$4 億。',

        f'<b>兩檔同樣賣軟體訂閱的公司，市場給的價格差 20 倍</b>——Cloudflare（NET）前瞻本益比'
        f'（股價除以分析師預估未來一年每股獲利，數字越低代表為未來一年同樣一塊錢獲利所付出的價格越便宜）達 {stats["net_fwd_pe"]:.0f} 倍，'
        f'而且它過去一年的股東權益報酬率是負的；Adobe（ADBE）只有 {stats["adbe_fwd_pe"]:.1f} 倍，股東權益報酬率 63.0%。'
        f'規模層級也分層：大型股（S&amp;P 500）前瞻本益比中位數 {stats["pe_by_group"]["SP500"]["median"]:.1f} 倍，'
        f'小型股（S&amp;P 600）僅 {stats["pe_by_group"]["SP600"]["median"]:.1f} 倍（{SNAPSHOT_DATE}快照，本頁自算）。',

        f'<b>同一產業裡，公司規模越大，資本報酬通常越高，但不是簡單的線性關係</b>——11 個 GICS 產業中，S&amp;P 500 成分股的 ROE'
        f'（股東權益報酬率，公司用股東出的每一塊錢賺回多少）中位數全數高於同產業 S&amp;P 600 成分股；但不動產與醫療保健兩個產業，'
        f'中型股（S&amp;P 400）中位數反而略高於大型股，規模與報酬的關係要逐產業檢查（{SNAPSHOT_DATE}快照，本頁自算）。',

        f'<b>企業回購是比配息更大的股東現金回饋管道</b>——S&amp;P 500 企業在 2024-10～2025-09 這 12 個月'
        f'回購（公司買回自己股票，是配息之外另一種還錢給股東的方式）總額 US${facts["buyback_ttm_usd_tn"]["value"]:.2f} 兆，'
        f'同期配息 US${facts["dividend_ttm_usd_bn"]["value"]/1000:.3f} 兆，回購規模是配息的約 '
        f'{facts["buyback_ttm_usd_tn"]["value"]*1000/facts["dividend_ttm_usd_bn"]["value"]:.2f} 倍。'
        f'S&amp;P Dow Jones Indices 公開發布的最新一期庫藏股報告止於 2025 Q3，這不是即期水位。',

        f'<b>持有美股的預期報酬裡，超過一半來自不必承擔股票風險就能拿到的公債利息</b>——十年期公債殖利率 '
        f'{facts["treasury_10y_pct"]["value"]}%（as-of {facts["treasury_10y_pct"]["as_of"]}），隱含股權風險溢酬'
        f'（ERP，投資人因為承擔股票風險而多要求的那一段報酬，把它加上公債殖利率就是市場對股票的預期總報酬）'
        f' {facts["implied_erp_pct"]["value"]}%（as-of {facts["implied_erp_pct"]["as_of"]}，Damodaran），'
        f'兩者相加約 {facts["treasury_10y_pct"]["value"]+facts["implied_erp_pct"]["value"]:.2f}%。'
        f'這個 ERP 對算法高度敏感：同一來源換其他方法可得 3.56%–6.05%，引用時必須標明是哪一種算法。',

        f'<b>投在美國股票的基金錢，近三分之二不做選股判斷</b>——投資美國國內股票的共同基金與 ETF 資產中，'
        f'指數型（被動，按指數成分比例配置、不判斷個股貴不貴）占 {facts["passive_share_us_domestic_equity_pct"]["value"]}%'
        f'（as-of {facts["passive_share_us_domestic_equity_pct"]["as_of"]}，ICI），指數型基金與 ETF 絕對規模 '
        f'US${facts["passive_index_fund_assets_usd_tn"]["value"]:.2f} 兆。同時 SPX（S&amp;P 500 指數選擇權）成交量中 '
        f'{facts["odte_spx_pct"]["value"]}% 屬 0DTE（當日到期，當天開倉、當天就會到期或作廢的合約，as-of 2026-05）。',

        f'<b>站內既有研究覆蓋 229 檔，但市值最大的一批名字仍是空白</b>——229 檔中有 203 檔歸入本頁九個鏡頭'
        f'（另 26 檔是外國公司在美國掛牌的存託憑證，不列入鏡頭母體）；九鏡頭 203 檔裡 191 檔在 90 天複審窗內'
        f'（複審窗＝該檔裁決完成日距基準日 90 天以內，超過就算過期待複審），比例 94.1%。'
        f'JPMorgan Chase（JPM）、Berkshire Hathaway（BRK-B）、McDonald\'s（MCD）等九檔零覆蓋的大型與中大型公司合計市值逾 US$3 兆'
        f'（as-of {DD_BASIS_DATE} 站內 DD 盤點）。',
    ]
    return "".join(f"<li>{x}</li>" for x in items)


def build_scorecard(stats, facts):
    rows = [
        ("S&amp;P 500 前十大合計權重", f'{facts["spy_top10_weight_pct"]["value"]}%', facts["spy_top10_weight_pct"]["as_of"],
         "十家公司決定超過三分之一的指數漲跌", "SSGA 官方持股檔"),
        ("Mag 7 合計權重", f'{facts["mag7_weight_pct"]["value"]}%', facts["mag7_weight_pct"]["as_of"],
         "七家科技巨頭合計占大盤將近三分之一", "SSGA 官方持股檔"),
        ("資訊科技產業權重", f'{facts["sector_weight_it_pct"]["value"]}%', facts["sector_weight_it_pct"]["as_of"],
         "S&amp;P 500 裡影響力最大的單一 GICS 產業", "SSGA 官方持股檔"),
        ("母體市值總額（1,590檔）", usd_from_raw(stats["total_mcap"]), SNAPSHOT_DATE,
         "本頁美股母體（S&amp;P 1500＋市值≥US$100億補充名單）的合計市值", "母體快照（本頁自算）"),
        ("母體前瞻本益比中位數", f'{stats["pe_all_median"]:.1f} 倍', SNAPSHOT_DATE,
         "母體整體的估值水位，但被三個規模層級間的分裂蓋掉，見下方各層級", "母體快照（本頁自算）"),
        ("大型股（S&amp;P 500）前瞻本益比中位數", f'{stats["pe_by_group"]["SP500"]["median"]:.1f} 倍', SNAPSHOT_DATE,
         "同一把尺分三個規模層級看，才不會被單一中位數蓋掉分裂", "母體快照（本頁自算）"),
        ("中型股（S&amp;P 400）前瞻本益比中位數", f'{stats["pe_by_group"]["SP400"]["median"]:.1f} 倍', SNAPSHOT_DATE,
         "介於大型股與小型股之間，非簡單平均值", "母體快照（本頁自算）"),
        ("小型股（S&amp;P 600）前瞻本益比中位數", f'{stats["pe_by_group"]["SP600"]["median"]:.1f} 倍', SNAPSHOT_DATE,
         "母體三層中估值最低的一層", "母體快照（本頁自算）"),
        ("母體 ROE 中位數", f'{stats["roe_all_median"]:.1f}%', SNAPSHOT_DATE,
         "資本報酬的整體水位，個別產業差異可達一倍以上，見論點 D", "母體快照（本頁自算）"),
        ("被動指數基金規模", f'US${facts["passive_index_fund_assets_usd_tn"]["value"]:.2f} 兆', facts["passive_index_fund_assets_usd_tn"]["as_of"],
         "不看價格、按資金流入比例配置的資金池；同期主動型基金 US$18.58 兆", "ICI 月報"),
        ("被動占美國國內股票型基金比重", f'{facts["passive_share_us_domestic_equity_pct"]["value"]}%', facts["passive_share_us_domestic_equity_pct"]["as_of"],
         "投在美國股票的共同基金與 ETF 資產中，近三分之二由不做選股判斷的指數型產品持有", "ICI 月報"),
        ("企業回購總額（滾動 12 個月）", f'US${facts["buyback_ttm_usd_tn"]["value"]:.2f} 兆', facts["buyback_ttm_usd_tn"]["as_of"],
         f'同期配息 US${facts["dividend_ttm_usd_bn"]["value"]/1000:.3f} 兆，回購規模是配息的約'
         f' {facts["buyback_ttm_usd_tn"]["value"]*1000/facts["dividend_ttm_usd_bn"]["value"]:.2f} 倍；S&amp;P DJI 最新一期報告止於 2025 Q3，非即期數字',
         "S&amp;P DJI 官方庫藏股報告"),
        ("海外營收占比（S&amp;P 500）", f'{facts["overseas_revenue_share_pct"]["value"]}%', facts["overseas_revenue_share_pct"]["as_of"],
         "S&amp;P 500 公司近三成營收不是來自美國本土；另有一套只納入有完整地理揭露公司的舊口徑算出 42.9%，兩者不可互換",
         "S&amp;P Global Market Intelligence／Goldman Sachs"),
        ("隱含股權風險溢酬 vs 十年期公債殖利率", f'{facts["implied_erp_pct"]["value"]}% vs {facts["treasury_10y_pct"]["value"]}%',
         f'{facts["implied_erp_pct"]["as_of"]} / {facts["treasury_10y_pct"]["as_of"]}',
         "股票相對公債的額外補償只有 4.14 個百分點；同一來源換算法可得 3.56%–6.05%，這個數字對方法論高度敏感", "Damodaran／美國財政部"),
        ("2026 年迄今 IPO 件數與募資總額",
         f'{facts["ipo_priced_2026ytd"]["value"]} 件／US${facts["ipo_proceeds_2026ytd_usd_bn"]["value"]*10:,.0f} 億',
         facts["ipo_priced_2026ytd"]["as_of"],
         "IPO（首次公開發行，公司第一次把股票賣給一般大眾）件數年減 27.4%、募資總額年增 479.4%，少數超大型案件主導市場；"
         "此件數不含 SPAC（空白支票公司，先掛牌募資、之後再找標的合併），SPAC 另計 148 件",
         "Renaissance Capital"),
        ("SPX 選擇權 0DTE 占比", f'{facts["odte_spx_pct"]["value"]}%', facts["odte_spx_pct"]["as_of"],
         "選擇權市場的當沖化程度已經過半數", "Cboe 2026年Q2法說簡報"),
        ("股東行動主義行動件數與成功率", f'{facts["activist_actions_2026h1"]["value"]} 件／{facts["activist_success_rate_2026h1_pct"]["value"]}%',
         facts["activist_actions_2026h1"]["as_of"],
         "股東行動主義＝投資人取得股份後公開要求公司換人、分拆或改變資本配置；件數創史上最活躍半年紀錄，"
         "但取得董事席次的成功率從約 27% 降至 17%",
         "Lazard《Review of Shareholder Activism》"),
    ]
    trs = []
    build_scorecard.row_count = len(rows)
    for label, val, asof, gloss, src in rows:
        trs.append(
            f'<tr><td class="lbl">{label}</td><td class="num strong">{val}</td>'
            f'<td class="num" style="color:var(--sec)">{asof}</td><td class="why">{gloss}</td>'
            f'<td class="why">{src}</td></tr>'
        )
    return "".join(trs)


def tile(v, l):
    return f'<div class="t"><div class="v">{v}</div><div class="l">{esc(l)}</div></div>'


def argument_card(letter, tag, title, lead, bullets, sowhat, tiles, exnum, cap, sub, svg, take):
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
    conc = stats["conc"]
    out = []
    # A 集中度
    out.append(argument_card(
        "A", "集中度：S&amp;P 500 的漲跌由十檔股票決定",
        "S&amp;P 500 不是 500 家公司平均分攤的指數，前十檔股票就拿走超過三分之一的權重。",
        f'S&amp;P 500 前十大合計權重 {facts["spy_top10_weight_pct"]["value"]}%'
        f'（as-of {facts["spy_top10_weight_pct"]["as_of"]}，SSGA 官方持股檔逐檔加總，流通量調整後的權重）。',
        [
            f'本頁 1,590 檔母體依市值排序（未做流通量調整），前十檔合計占母體總市值 {conc[10]["pct"]:.1f}%；'
            f'前 50 檔占 {conc[50]["pct"]:.1f}%；前 100 檔占 {conc[100]["pct"]:.1f}%（{SNAPSHOT_DATE}快照，本頁自算——'
            f'與 SSGA 流通量調整權重方法不同，兩者不是同一套算法，故數字不完全相等，但量級一致）。',
            f'產業集中同樣明顯，但兩套口徑要分開讀：以 SSGA 的 S&amp;P 500 權重看，資訊科技占 {facts["sector_weight_it_pct"]["value"]}%，'
            f'第二大的金融占 {facts["sector_weight_financials_pct"]["value"]}%、第三大的通訊服務占 {facts["sector_weight_comm_pct"]["value"]}%；'
            f'以本頁 1,590 檔母體市值加總看，資訊科技占 {stats["sector_pct"]["Information Technology"]:.1f}%、'
            f'通訊服務 {stats["sector_pct"]["Communication Services"]:.1f}%、金融 {stats["sector_pct"]["Financials"]:.1f}%。'
            f'兩套排序不同，因為母體多了 S&amp;P 500 以外的 1,087 檔中小型股與補充名單，而中小型股的產業分布本來就跟大型股不一樣。',
            f'反過來看尾巴：第 101 檔以後的 1,490 檔股票（占母體檔數 93.7%）合計只分到 {conc["rest"]["pct"]:.1f}% 的市值，'
            f'平均每檔約占母體萬分之二。市值排序的前段與後段不是同一個市場。',
        ],
        "任何以「大盤」為名的判讀，若不先拆解這十檔股票，本質上是在看少數幾家公司的走勢圖，不是在看 1,590 檔公司的平均表現。",
        [tile(f'{facts["spy_top10_weight_pct"]["value"]}%', "S&P 500 前十大權重（SSGA）"),
         tile(f'{facts["mag7_weight_pct"]["value"]}%', "Mag 7 合計權重（SSGA）"),
         tile(f'{conc[10]["pct"]:.1f}%', "母體前十檔市值占比（本頁自算）")],
        1, "母體市值集中度累積占比與 GICS 產業分布",
        f"來源：本頁 1,590 檔母體快照，{SNAPSHOT_DATE}快照，依市值排序（未做流通量調整），本頁自算；"
        f"「補充名單」為不在 S&amp;P 1500 內、故無官方 GICS 產業分類的 85 檔，單獨列為一類。",
        svg_exhibit1(stats),
        "集中度本身不是新現象，是持續墊高數個週期的結構事實；真正該問的是集中在誰身上、靠什麼維持。"
    ))
    # B AI資本週期
    mult = {k: facts[f"capex_ai_{k}"]["capex_yoy_pct"] / facts[f"capex_ai_{k}"]["revenue_yoy_pct"]
            for k in ("msft", "googl", "amzn", "meta", "orcl")}
    out.append(argument_card(
        "B", "AI 資本週期：五家公司投同一個題材，收入跟上的速度差 8 倍",
        "把資本支出的成長速度除以對應收入的成長速度，五家公司從 1.2 倍到 9.3 倍——這不是同一種賭注。",
        "五家公司最新一期的資本支出年增率全數高於對應業務的營收年增率，但差距倍數相差近 8 倍：Alphabet 的雲端收入幾乎跟上投資速度，"
        "Oracle 的收入連投資速度的九分之一都不到。",
        [
            f'Alphabet（GOOGL）差距最小：資本支出年增 {facts["capex_ai_googl"]["capex_yoy_pct"]:.1f}%，'
            f'Google Cloud 分部營收年增 {facts["capex_ai_googl"]["revenue_yoy_pct"]:.1f}%，差距僅 {mult["googl"]:.1f} 倍'
            f'（{facts["capex_ai_googl"]["as_of"]}）——投進去的錢，收入端幾乎同步跟上。',
            f'Amazon（AMZN）：單季資本支出年增 {facts["capex_ai_amzn"]["capex_yoy_pct"]:.1f}%，'
            f'AWS 分部營收年增 {facts["capex_ai_amzn"]["revenue_yoy_pct"]:.1f}%（18 季以來最快），差距 {mult["amzn"]:.1f} 倍；'
            f'但滾動 12 個月自由現金流（公司在支付營運與資本支出後實際留下的現金）已由去年同期的 +US$1,820 億轉為'
            f' −US${abs(facts["amzn_fcf_ttm_usd_bn"]["value"])*100:,.0f} 億。',
            f'Meta（META）：資本支出年增 {facts["capex_ai_meta"]["capex_yoy_pct"]:.1f}%，整體營收年增'
            f' {facts["capex_ai_meta"]["revenue_yoy_pct"]:.1f}%，差距 {mult["meta"]:.1f} 倍'
            f'（{facts["capex_ai_meta"]["as_of"]}；資本支出含融資租賃本金，分子分母同口徑）。',
            f'Microsoft（MSFT）：資本支出年增 {facts["capex_ai_msft"]["capex_yoy_pct"]:.1f}%，'
            f'Intelligent Cloud 分部營收年增 {facts["capex_ai_msft"]["revenue_yoy_pct"]:.1f}%，差距 {mult["msft"]:.1f} 倍'
            f'（FY2026 Q4，截至 2026-06-30）。',
            f'Oracle（ORCL）差距最大：整個會計年度資本支出年增 {facts["capex_ai_orcl"]["capex_yoy_pct"]:.1f}%，'
            f'整體營收僅年增 {facts["capex_ai_orcl"]["revenue_yoy_pct"]:.1f}%，差距 {mult["orcl"]:.1f} 倍；'
            f'FY2026 自由現金流 −US${abs(facts["orcl_fcf_fy26_usd_bn"]["value"])*100:,.0f} 億，前一年只有 −US$4 億；'
            f'股價較 52 週高點回落 {abs(facts["orcl_drawdown_from_52wk_high_pct"]["value"]):.1f}%'
            f'（{facts["orcl_drawdown_from_52wk_high_pct"]["as_of"]}）。',
        ],
        "「AI 資本支出暴衝」不是一句可以套在五家公司身上的通論。差距倍數只回答「投資跑多快、收入跟多快」，不回答「誰撐得住」——"
        "Alphabet 差距最小但單季自由現金流仍是負的，Oracle 差距最大而且自由現金流連兩年惡化。兩件事要分開看，不能互相取代。",
        [tile(f'{mult["orcl"]:.1f} 倍', "ORCL 資本支出／營收成長差距，五家最大"),
         tile(f'{mult["googl"]:.1f} 倍', "GOOGL 差距，五家最小"),
         tile(f'−US${abs(facts["orcl_fcf_fy26_usd_bn"]["value"])*100:,.0f} 億', "ORCL FY2026 自由現金流")],
        2, "AI 資本支出年增率 vs 對應業務營收年增率對照",
        "來源：各公司最新一期財報新聞稿與 SEC 申報文件（MSFT 為 FY2026 Q4、GOOGL／AMZN／META 為 2026 Q2、"
        "ORCL 為 FY2026 全年，會計年度不同故季別不同；逐筆來源與日期見 §6）。",
        svg_exhibit2(facts),
        "差距倍數的排序不等於風險排序。要判斷誰撐得住，看的是自由現金流的方向與幅度，不是資本支出年增率本身。"
    ))
    # C 估值分裂
    net_pe, adbe_pe = stats["net_fwd_pe"], stats["adbe_fwd_pe"]
    out.append(argument_card(
        "C", "估值分裂：市場已經用價格把同一個產業拆成兩群",
        "市場不是整體變貴，是同一門生意裡最貴與最便宜的公司被拉開到 20 倍價差。",
        f'兩家都賣軟體訂閱：Cloudflare（NET）前瞻本益比 {net_pe:.0f} 倍、過去一年股東權益報酬率為負；'
        f'Adobe（ADBE）只有 {adbe_pe:.1f} 倍、股東權益報酬率 63.0%（{SNAPSHOT_DATE}快照）。',
        [
            f'大型股（S&amp;P 500）前瞻本益比中位數 {stats["pe_by_group"]["SP500"]["median"]:.1f} 倍，'
            f'中型股（S&amp;P 400）{stats["pe_by_group"]["SP400"]["median"]:.1f} 倍，'
            f'小型股（S&amp;P 600）{stats["pe_by_group"]["SP600"]["median"]:.1f} 倍——公司規模越小，市場給的本益比中位數越低。',
            f'分裂不只在規模層級之間，S&amp;P 500 內部就有：第一四分位（500 檔由便宜排到貴，排在四分之一位置的那檔）'
            f'{stats["pe_by_group"]["SP500"]["q1"]:.1f} 倍，第三四分位（排在四分之三位置）{stats["pe_by_group"]["SP500"]["q3"]:.1f} 倍，'
            f'貴的那一端比便宜那一端高 {(stats["pe_by_group"]["SP500"]["q3"]/stats["pe_by_group"]["SP500"]["q1"]-1)*100:.0f}%——'
            f'光是指數中間那一半的公司，估值就拉開這麼多，而這還沒算進兩端的極端值。',
            f'NET 前瞻本益比 {net_pe:.0f} 倍是 S&amp;P 500 中位數的 {net_pe/stats["pe_by_group"]["SP500"]["median"]:.1f} 倍；'
            f'ADBE {adbe_pe:.1f} 倍低於母體三個規模層級的所有中位數。'
            f'差別不在「軟體」這個標籤——NET 目前還沒有正的股東權益報酬率，市場買的是未來；ADBE 現在就在賺錢，市場折價買的是它被 AI 取代的風險。',
        ],
        "「便宜」或「昂貴」不是對整個母體下的單一判斷，而是對特定計價模式與特定規模層級下的判斷；把 1,590 檔當成一個估值水位討論，"
        "會把這個分裂蓋掉。",
        [tile(f'{net_pe:.0f} 倍 / {adbe_pe:.1f} 倍', "NET vs ADBE 前瞻本益比"),
         tile(f'{stats["pe_by_group"]["SP500"]["median"]:.1f} 倍', "S&P 500 前瞻本益比中位數"),
         tile(f'{stats["pe_by_group"]["SP600"]["median"]:.1f} 倍', "S&P 600 前瞻本益比中位數")],
        3, "前瞻本益比分布：三組指數對照與個股極端例",
        f"來源：本頁 1,590 檔母體快照，{SNAPSHOT_DATE}快照，本頁自算；橫線兩端為第一四分位與第三四分位、圓點為中位數，排除缺值與非正值。",
        svg_exhibit3(stats),
        "分裂的分界線不是「大盤貴不貴」，是市場已經用價格把不同計價模式與不同規模層級分開對待——判讀任何個股估值前，先確認它屬於哪一群。"
    ))
    # D 資本報酬
    out.append(argument_card(
        "D", "資本報酬比較：地位不會自動換成報酬",
        "同一個 GICS 產業裡，大型股的 ROE 中位數幾乎全面高於中小型股，但關係不是簡單的線性遞減。",
        f"11 個 GICS 產業中，S&amp;P 500 成分股 ROE 中位數全數（{stats['roe_inc_count']}/{stats['roe_checked']}）高於同產業 S&amp;P 600 成分股。",
        [
            "差距最大的是非必需消費：大型股中位數 37.1%，小型股僅 12.6%，相差近三倍；資訊科技緊接在後，23.2% 對 8.2%。",
            "但「規模越大、ROE 越高」不是單向的線性關係：不動產（大型股 7.7%、中型股 8.2%）與醫療保健（13.7%、14.2%）"
            "兩個產業，中型股中位數反而高於大型股；公用事業則是中型股 8.1% 比小型股 9.5% 還低，三層排序完全不照規模走。",
            f"母體整體 ROE 中位數 {stats['roe_all_median']:.1f}%（{SNAPSHOT_DATE}快照，本頁自算，中位數天然排除少數負股東權益的極端值，不受個別離群值拉扯）。",
        ],
        "大型股在多數產業有較高的資本報酬，但中型股不是簡單的「中間值」——個別產業內部的名次會反轉，逐產業檢查比套用一條"
        "「規模與報酬成正比」的通用規則更可靠，尤其是判讀中小型股時。",
        [tile(f"{stats['roe_inc_count']}/{stats['roe_checked']}", "S&P 500 ROE 中位數高於 S&P 600 的產業數"),
         tile("37.1% / 12.6%", "非必需消費：S&P 500 vs S&P 600"),
         tile("23.2% / 8.2%", "資訊科技：S&P 500 vs S&P 600")],
        4, "ROE 中位數：11 個 GICS 產業 × 大型／中型／小型股對照",
        f"來源：本頁 1,590 檔母體快照，{SNAPSHOT_DATE}快照，本頁自算；圖中數字為中位數，非平均數，用以天然排除負股東權益等極端值。",
        svg_exhibit4(stats),
        "市占地位是敘事，ROE 是驗算——同樣講「利基龍頭」的故事，資本報酬轉換率可以差到一倍以上，逐檔驗算比相信故事可靠。"
    ))
    # E 買盤結構
    ttm_buy_yi = facts["buyback_ttm_usd_tn"]["value"] * 10000  # 兆 -> 億
    ttm_div_yi = facts["dividend_ttm_usd_bn"]["value"] * 10  # billions -> 億
    ratio = ttm_buy_yi / ttm_div_yi
    out.append(argument_card(
        "E", "買盤結構：投進美股的基金錢，近三分之二不做選股判斷",
        "被動基金與企業回購，兩股都不因為股價貴就少買的資金，一個占了股票型基金資產的三分之二，一個一年花掉一兆美元。",
        f'投資美國國內股票的共同基金與 ETF 資產中，{facts["passive_share_us_domestic_equity_pct"]["value"]}% 是指數型'
        f'（as-of {facts["passive_share_us_domestic_equity_pct"]["as_of"]}，ICI）；指數型基金與 ETF 總資產 '
        f'US${facts["passive_index_fund_assets_usd_tn"]["value"]:.2f} 兆，約當 S&amp;P 500 官方口徑市值'
        f' US${facts["sp500_total_mcap_usd_tn"]["value"]} 兆（as-of {facts["sp500_total_mcap_usd_tn"]["as_of"]}）的三成。',
        [
            f'S&amp;P 500 企業在 2024-10～2025-09 這 12 個月回購總額 US${facts["buyback_ttm_usd_tn"]["value"]:.2f} 兆，'
            f'同期配息 US${facts["dividend_ttm_usd_bn"]["value"]/1000:.3f} 兆，回購規模是配息的約 {ratio:.2f} 倍。'
            f'S&amp;P Dow Jones Indices 公開發布的最新一期庫藏股報告是 {facts["buyback_report_latest_quarter"]["value"]}'
            f'（發布日 2025-12-18），2025 Q4 以後尚無公開季度數字，本頁不宣稱這是即期水位。',
            f'單季拆開看：2025 年第一季回購 US${facts["buyback_q1_2025_usd_bn"]["value"]*10:,.0f} 億為當年最高，'
            f'第二季回落至 US${facts["buyback_q2_2025_usd_bn"]["value"]*10:,.0f} 億（季減 20.1%），'
            f'第三季回升至 US${facts["buyback_q3_2025_usd_bn"]["value"]*10:,.0f} 億（季增 6.2%）——季度之間本身有明顯波動，不是穩定線性成長。',
            "2023 年起，美國對企業股票回購課徵 1% 聯邦消費稅（源自降低通膨法案條款），但回購規模在稅制生效後仍創下歷史新高，"
            "代表 1% 稅率不足以改變企業的資本配置選擇。",
            "企業偏好回購勝過配息，其中一個機制是股東的課稅時點：配息在發放當年就被課稅，回購則讓股東自己決定何時出脫持股、"
            "何時實現損益（長期持有逾一年還適用 0／15／20% 的優惠稅率，短期則按最高 37% 的一般所得稅率）。"
            "同樣一塊錢還給股東，走回購這條路股東可以延後繳稅。",
            "被動指數基金按資金流入比例配置部位，不判斷個股貴不貴；企業回購按資本配置政策執行，也不是逢低才進場——"
            "兩者都是規則驅動，不是價值判斷驅動的資金。",
        ],
        "這兩股資金不是「覺得便宜才買」的買盤，而是規則驅動或紀律驅動的買盤，是判讀「美股為什麼跌不深、特定股票估值為什麼能維持高檔」"
        "時繞不開的結構性買家。要注意的是兩者的時效不同：被動占比是 2026-07 的即期數字，回購金額止於 2025 Q3，兩個數字不同步。",
        [tile(f'{facts["passive_share_us_domestic_equity_pct"]["value"]}%', "被動占美國國內股票型基金資產比重"),
         tile(f'US${facts["buyback_ttm_usd_tn"]["value"]:.2f} 兆', "企業回購總額（2024-10～2025-09）"),
         tile(f'{ratio:.2f} 倍', "回購／配息倍數")],
        5, "S&amp;P 500 企業回購季度走勢與 2024-10～2025-09 回購／配息對照",
        "來源：S&P Dow Jones Indices 官方庫藏股報告 2025 Q3 期（發布日 2025-12-18，為公開發布的最新一期）；本圖不是即期水位。",
        svg_exhibit5(facts),
        "被動買盤與企業回購都是「不看價格」的買家，這是判讀美股估值韌性時的結構性背景，但不代表個股不會因為基本面惡化而重估。"
    ))
    return "".join(out)


LENS_ROWS = [
    dict(n=1, slug="platforms", name="巨型平台與 AI 資本週期",
         q="Mag 7 是不是同一種資本賭注？",
         a="八個平台橫跨三個 GICS 產業、資本策略分成兩種：四大雲端服務商的資本支出成長速度全數跑贏對應業務營收，"
           "但差距從 1.2 倍到 3.4 倍（本表採各公司最新一期財報，見論點 B；子頁引用的 2–4 倍出自前一期財報）；"
           "Apple 與 Netflix 完全不參與這場資本競賽。",
         n_dd=8, n_win=8, gap="核心 8 檔覆蓋率 100%，本鏡頭無候選隊列缺口"),
    dict(n=2, slug="semis", name="半導體與 AI 基礎設施",
         q="AI 供給側的錢，最後留在誰手上？",
         a="140 檔母體合計市值約 US$16.3 兆，NVIDIA（NVDA）一檔占 33.4%；三層答案——"
           "定價權機制性成立、結構真實但曝險集中、量在飛漲但定價權未證實。",
         n_dd=56, n_win=52, gap="EDA（晶片設計軟體）雙寡占的另一半 Synopsys（SNPS）站內無 DD"),
    dict(n=3, slug="software", name="軟體與網路平台經濟",
         q="同樣叫軟體股，誰在 AI 時代更貴？",
         a="計價模式決定估值，不是「軟體股」這個標籤——前瞻本益比從 9.6 倍到 189 倍，價差 20 倍；25 檔既有裁決中 7 檔進場，"
           "其中 Salesforce（CRM）是附帶條件的衛星持倉、ServiceNow（NOW）屬工作流授權混合，"
           "沒有一檔是不帶條件的純座位制（按使用人數收費，人數減少收入就減少）核心軟體。",
         n_dd=25, n_win=23, gap="Intuit（INTU）站內無 DD，是本鏡頭最純的座位制核心樣本"),
    dict(n=4, slug="compounders", name="複利機器",
         q="誰的高 ROE 能穿越景氣循環？",
         a="用快照與多年 ROIC（投入資本報酬率，公司每投入一塊錢本金賺回多少）軌跡雙入口重篩，10 檔深查名單中有 5 檔若只看單年 ROE 早就出局；"
           "有機成長型（如 Visa／Mastercard）帳面數字可直接信任，連續併購型（如 Roper／Teledyne）須看新投入資本的增量報酬，"
           "因為併購產生的商譽會把帳面 ROIC 壓低。",
         n_dd=10, n_win=10, gap="Union Pacific（UNP）快照 ROE 39.7% 通過篩選，站內無 DD"),
    dict(n=5, slug="healthcare", name="醫療保健",
         q="藥價政策收緊之後，誰真的接得住？",
         a="三條政策收緊線精準命中大藥廠與持有藥品福利管理業務（PBM，介於藥廠與保險之間、決定哪些藥能被理賠與理賠多少的中間商）的保險公司，"
           "藥品流通商幾乎不受影響；AbbVie（ABBV）已交出接替藥物營收超越前高峰的成績單，Pfizer（PFE）靠併購重建仍待驗證。",
         n_dd=16, n_win=16, gap="PFE／ABT／TMO／CI／SYK 五檔核心名字站內零覆蓋"),
    dict(n=6, slug="financials", name="金融",
         q="金融股的高 ROE 是定價權還是槓桿撐出來的？",
         a="278 檔金融股拆成五種商業模式，資本結構與升息環境的方向並不一致；CME 淨利率 63.1% 最接近可持續的高資本報酬，"
           "Goldman Sachs／Morgan Stanley 的高 ROE 主要是交易槓桿撐出來的。",
         n_dd=13, n_win=13, gap="母體最大兩檔金融股 JPMorgan（JPM）與 Berkshire Hathaway（BRK-B）都站內零覆蓋"),
    dict(n=7, slug="consumer", name="消費特許經營",
         q="定價權是結構性的，還是靠通膨順風？",
         a="Costco 的會員費與 TJX 的庫存周轉（ROE 61.3%）不需要持續漲價也能維持獲利品質；Nike 與 Lululemon 的營收與估值雙雙轉弱，"
           "是提價紅利消退的具體證據。",
         n_dd=31, n_win=29, gap="McDonald's／P&amp;G／PepsiCo／Yum!／O'Reilly／AutoZone 六檔核心名字合計市值逾 US$0.88 兆，站內零覆蓋"),
    dict(n=8, slug="energy-industrials", name="能源電力與再工業化",
         q="用電缺口是真的，還是估值先跑？",
         a="PJM 電網容量拍賣總成本跨兩次拍賣週期（2024 年度→2025 年度）暴增近 8 倍，不是單一年度內的變化；官方歸因資料中心用電年增約 5%。"
           "一級發電與電網標的已站上 52 週區間 80% 以上高檔（股價落在過去一年最高與最低價之間的相對位置），"
           "同題材次級標的仍在 40% 以下，估值分歧本身就是要追蹤的訊號。",
         n_dd=35, n_win=31, gap="國防三巨頭 Lockheed Martin／RTX／Northrop Grumman 全數站內零覆蓋"),
    dict(n=9, slug="hidden-champions", name="中小型隱形冠軍",
         q="市占地位第一，資本報酬也第一嗎？",
         a="七個利基型 GICS 子產業中位數 ROE 從 8.3% 到 18.6% 差一倍以上，AI 供應鏈敘事最熱的半導體設備類，資本報酬轉換率反而是七叢集最低。",
         n_dd=9, n_win=9, gap="9 檔站內既有 DD 沒有一檔評級為進場核心，主要卡在估值過熱（本表把 Vicor（VICR）計入鏡頭二，"
            "該鏡頭子頁則把它收在鏡頭九，故子頁列 10 檔）"),
]


def build_lens_table():
    trs = []
    for r in LENS_ROWS:
        cov = f'{r["n_dd"]} 檔／{r["n_win"]/r["n_dd"]*100:.1f}% 窗內'
        trs.append(
            f'<tr><td class="lbl"><a href="us/{r["slug"]}.html">鏡頭{r["n"]}・{r["name"]}</a></td>'
            f'<td class="why">{r["q"]}</td><td class="why">{r["a"]}</td>'
            f'<td class="num" style="white-space:nowrap">{cov}</td><td class="why">{r["gap"]}</td></tr>'
        )
    return "".join(trs)


# 可作戰名單：已有裁決代表（逐字抄 dd-meta dca_verdict／dca_role）
WATCH_EXISTING = [
    dict(t="GOOGL", name="Alphabet", lens="鏡頭一", verdict="進場", role="核心",
         wait="資本支出／營收成長差距倍數是否持續收斂", dd="DD_GOOGL_20260723.html"),
    dict(t="NVDA", name="NVIDIA", lens="鏡頭二", verdict="進場", role="核心",
         wait="超大規模雲端客戶自研晶片的替代速度", dd="DD_NVDA_20260831.html"),
    dict(t="PLTR", name="Palantir Technologies", lens="鏡頭三", verdict="進場", role="衛星",
         wait="AI 基礎設施合約的續約率是否維持", dd="DD_PLTR_20260805.html"),
    dict(t="MA", name="Mastercard", lens="鏡頭四", verdict="進場", role="核心持倉",
         wait="ROIC（投入資本報酬率，公司每投入一塊錢本金賺回多少）連年上升的軌跡是否延續", dd="DD_MA_20260703.html"),
    dict(t="LLY", name="Eli Lilly", lens="鏡頭五", verdict="進場", role="核心",
         wait="口服 GLP-1 劑型能否追上 Novo Nordisk 的進度", dd="DD_LLY_20260806.html"),
    dict(t="BX", name="Blackstone", lens="鏡頭六", verdict="進場", role="核心",
         wait="五檔另類資產管理型中唯一保持純資產管理模式，能否抵抗保險化的同業競爭", dd="DD_BX_20260724.html"),
    dict(t="DECK", name="Deckers Brands", lens="鏡頭七", verdict="進場", role="衛星持倉",
         wait="該檔裁決附條件（逢回分批），等估值回檔進入 DD 設定的觸發區間", dd="DD_DECK_20260706.html"),
    dict(t="TT", name="Trane Technologies", lens="鏡頭八", verdict="進場", role="核心",
         wait="用電缺口需求是否持續兌現為訂單", dd="DD_TT_20260731.html"),
    dict(t="MWA", name="Mueller Water Products", lens="鏡頭九", verdict="站內評 A 級", role="該檔 DD 尚無進場裁決欄位",
         wait="複審後補上進場／觀望等決策欄位", dd="DD_MWA_20260524.html"),
]

# 零覆蓋候選（延續自站內候選隊列提名，逐字保留缺口理由）
WATCH_CANDIDATES = [
    ("JPM", "JPMorgan Chase", "鏡頭六", "S&amp;P 500 前十大唯一金融股，母體最大金融股，站內零覆蓋"),
    ("BRK-B", "Berkshire Hathaway", "鏡頭六", "母體第二大金融股，五大事業群需獨立框架深查，站內零覆蓋"),
    ("MCD", "McDonald's", "鏡頭七", "全球最經典的特許經營與加盟權利金案例，站內零覆蓋"),
    ("PG", "Procter & Gamble", "鏡頭七", "四籃核心中市值最大的無 DD 名字"),
    ("PEP", "PepsiCo", "鏡頭七", "飲料與零食雙曝險，站內零覆蓋"),
    ("YUM", "Yum! Brands", "鏡頭七", "加盟率光譜的另一端代表，站內零覆蓋"),
    ("ORLY", "O'Reilly Automotive", "鏡頭七", "四籃核心中無 DD 者估值最貴，非自由裁量需求代表"),
    ("AZO", "AutoZone", "鏡頭七", "與 O'Reilly 並列覆蓋缺口，房市低檔仍正成長的專業通路代表"),
    ("INTU", "Intuit", "鏡頭三", "最純座位制核心中小企業軟體樣本，站內零覆蓋"),
    ("TEAM", "Atlassian", "鏡頭三", "開發者工具座位制，對 AI 程式協作工具替代壓力本鏡頭最直接——英國註冊，不在本頁 1,590 檔股票母體內"
     "（與 Credo Technology 的排除標準相同，本表未套用同一排除規則，特此註記）"),
    ("SNPS", "Synopsys", "鏡頭二", "EDA 雙寡占的另一半，站內僅 Cadence（CDNS）有 DD"),
    ("UNP", "Union Pacific", "鏡頭四", "西岸鐵路雙占，報酬機制與 CSX 幾乎相同，站內無 DD"),
    ("PFE", "Pfizer", "鏡頭五", "全鏡頭最低遠期本益比＋最高股息率，大藥廠分層唯一缺口"),
    ("TMO", "Thermo Fisher Scientific", "鏡頭五", "生命科學工具分層龍頭，站內零覆蓋"),
    ("CI", "Cigna", "鏡頭五", "持有藥品福利管理業務，直接受政策改革衝擊，站內零覆蓋"),
    ("CME", "CME Group", "鏡頭六", "本鏡頭淨利率最高，獨占型交易所結構，站內零覆蓋"),
    ("VST", "Vistra", "鏡頭八", "發電／獨立發電商估值仍在 52 週區間 40% 以下，與一級標的估值分歧最具體案例"),
    ("LMT", "Lockheed Martin", "鏡頭八", "國防三巨頭全數站內零覆蓋，資料落差最集中處代表"),
    ("MIR", "Mirion Technologies", "鏡頭九", "核能輻射偵測利基地位清楚但 ROE 僅 1.5%，需深查商譽攤銷或定價權不足"),
    ("KRMN", "Karman Holdings", "鏡頭九", "2025 年 2 月 IPO 後毛利率 41.7% 全鏡頭候選最高，需深查資本結構稀釋是否暫時"),
]


def build_watchlist():
    trs = []
    for r in WATCH_EXISTING:
        trs.append(
            f'<tr><td class="lbl">{name_tag(r["name"], r["t"])}</td><td class="why lenscol">{r["lens"]}</td>'
            f'<td class="why"><b>{r["verdict"]}｜{r["role"]}</b></td><td class="why">{r["wait"]}</td>'
            f'<td class="why ddcol"><a href="{DD_DOC_BASE}/{r["dd"]}">查看 DD</a></td></tr>'
        )
    for t, name, lens, reason in WATCH_CANDIDATES:
        trs.append(
            f'<tr><td class="lbl">{name_tag(name, t)}</td><td class="why lenscol">{lens}</td>'
            f'<td class="why" style="color:var(--warn);white-space:nowrap">無（站內零覆蓋）</td><td class="why">{reason}</td>'
            f'<td class="why ddcol">—</td></tr>'
        )
    return "".join(trs)


FALSIFIERS = [
    "若 S&amp;P 500 前十大合計權重從目前 37.56% 降到 30% 以下，且不是因為指數換進更多同類科技股，代表指數集中度正在真正分散，"
    "論點 A「十檔股票決定漲跌」的框架就不再成立。",
    "若五家公司的資本支出／營收成長差距倍數同時收斂到 1.5 倍以內（目前是 1.2 倍到 9.3 倍），代表這輪 AI 資本週期已經從擴張期轉入收成期，"
    "論點 B「同一個題材、五種兌現速度」的分歧就消失了。",
    "若 Cloudflare（NET）與 Adobe（ADBE）的前瞻本益比價差從目前約 20 倍收斂到 10 倍以內，代表市場已經不再用計價模式區分 AI 曝險方向，"
    "論點 C「估值分裂」的框架需要重新檢視。",
    "若中小型股（S&amp;P 600）的 ROE 中位數在多個 GICS 產業同時追上同產業的 S&amp;P 500 成分股，代表中小型股的資本報酬轉換率正在系統性改善，"
    "論點 D「地位不等於報酬」就需要換掉支撐案例。",
    "若 S&amp;P 500 企業回購總額連續兩季年減達兩位數，或被動占美國國內股票型基金資產的比重從 64.1% 回落到六成以下，"
    "代表不看價格的買盤正在收縮，論點 E 就會鬆動。",
    "若十年期公債殖利率快速回落到 4% 以下，且隱含股權風險溢酬同步回升到 5% 以上，代表本頁多處「估值脆弱性」判讀所依賴的總體背景已經反轉，"
    "需要重新檢視整頁的估值判讀。",
]


def build_falsifiers():
    return "".join(f'<div class="amber">{x}</div>' for x in FALSIFIERS)


def build_methodology(stats, facts):
    counts = stats["counts_by_group"]
    return f'''
<b>母體怎麼建的</b>：主體是 S&amp;P 1500 成分股資格（S&amp;P 500／400／600 三張 Wikipedia 成分表解析，
{counts["sp500"]}＋{counts["sp400"]}＋{counts["sp600"]} 檔，無額外市值篩選——指數委員會的既有納入標準本身就是篩選器）；
補充名單為市值≥US$100 億、不在 S&amp;P 1500 內、美國屬性通過 yfinance 三重驗證（quoteType／exchange／country）的
{counts["supplement"]} 檔。母體最終 {counts["total"]:,} 檔，總市值約 {usd_from_raw(stats["total_mcap"])}，
快照日期 {SNAPSHOT_DATE}。<br><br>

<b>S&amp;P 500 的納入與剔除不是市值到門檻就自動發生</b>：指數委員會有裁量權，一般要求近四季及最近一季依 GAAP（美國公認會計原則，主管機關要求的統一記帳規則）計算的獲利為正、
公眾流通市值與流通量達標，且候選公司需經委員會逐案審查——市值規模只是必要條件之一，不是充分條件。本頁凡提到某檔中小型股
市值已超越現有成分股的地方，均不代表對「即將納入」的預測。<br><br>

<b>本頁範圍未涵蓋的三個結構性軸</b>（誠實揭露，非查無資料，是規劃範圍未觸及）：
①投資人稅制——長短期資本利得稅率差、合格股息稅率、401(k)（美國雇主提供的退休儲蓄帳戶，帳戶內的資本利得與股息可遞延或免稅）
／IRA／HSA 稅盾的完整論證未展開，本頁只在論點 E 陳述回購與配息的課稅時點差異；
②現貨端交易微結構——PFOF（訂單流付費，券商把散戶訂單賣給造市商換取報酬的安排）、批發商內化、暗池與另類交易系統（ATS）占比，
本頁僅查得低信心度的業界估計值（約四成，非交易所或監理機關一手數據），未展開完整論證；
③被動基金的表決權——US$21.76 兆的規模只回答了「買盤有多大」，沒有回答「這筆資金在公司治理上投了誰的票」。<br><br>

<b>數字的時效不一致，讀者要分開看</b>：母體數字統一為 {SNAPSHOT_DATE} 快照；被動基金占比與規模是 2026-07；
十年期公債殖利率是 2026-09-09、隱含股權風險溢酬是 2026-09-01；企業回購與配息止於 2025 Q3
（S&amp;P Dow Jones Indices 尚未公開發布 2025 Q4 以後的季度庫藏股報告，本頁不把它寫成即期水位）；
海外營收占比是 2024 年；雙重股權 IPO 占比停在 2021 上半年。整頁不是同一個時間切面。<br><br>

<b>已知缺口清單</b>：2025–2026 美股下市家數統計、市場整體平均短空部位（放空未回補的股數占比）百分比完全查無；
2026 年現行雙重股權 IPO 占比查無，沿用 2021 上半年快照；LULD（個股層級動態價格帶熔斷機制，
單一股票短時間內漲跌超過一定幅度就暫停撮合）與 10-Q（美國上市公司的季度財報）申報期限分級的官方完整規則
本頁僅查得二手簡化敘述，未能以 SEC／Nasdaq 官方一手文件核實，如實保留不確定性。
每筆結構數字的原始出處與查證日期都已在計分卡與各論點卡標明。<br><br>

<b>兩筆一度被列為缺口、實際查得到出處的數字</b>：①被動占美國國內股票型共同基金與 ETF 資產的比重 64.1%（2026-07），
來自 ICI《Active and Index Investing》月報同一份原始統計；②401(k) 資產規模 US$10.1 兆（2025-12-31，ICI 季度退休市場統計）。<br><br>

<b>SPAC 件數大於 IPO 件數不是資料矛盾</b>：Renaissance Capital 的 IPO 件數（106 件）依其方法學排除 SPAC
（空白支票公司，先掛牌募資、之後再找標的合併）、封閉式基金與 unit offerings，SPAC 以獨立資料集另計 148 件，
兩個數字屬平行母體、可以並存，相加才是全部掛牌案件。<br><br>

<b>本頁與鏡頭子頁的一處數字落差</b>：論點 B 與鏡頭一的資本支出、雲端營收年增率已對齊各公司最新一期財報
（MSFT FY2026 Q4、GOOGL／AMZN／META 2026 Q2、ORCL FY2026 全年）；鏡頭一子頁引用的是前一期財報，
兩處數字因此不同，以本頁為準。<br><br>

<b>站內 DD 裁決的抄錄規則與兩個已知落差</b>：§4 的裁決逐字取自各檔 DD 的 <code>dca_verdict</code>／<code>dca_role</code>
兩個欄位。Mueller Water Products（MWA）那份 DD 使用的是早期檔案格式，當時還沒有這兩個決策欄位，只有一個 A／B／C 分級，
所以該列的裁決欄寫的是分級而非進場／觀望。另外，§3 的 DD 覆蓋盤點以 {DD_BASIS_DATE} 為基準日，而 §4 的裁決連結指向各檔
截至本頁組裝時的最新一份 DD，兩者的時點不必然相同。<br><br>

<b>站內 DD 覆蓋的兩個母體</b>：站內美股掛牌唯一標的共 229 檔，其中 203 檔歸入本頁九個鏡頭，另 26 檔是外國公司在美國掛牌的
存託憑證（ADR），依盤點規則保留在清單中但不入鏡頭母體。§3 表格逐列加總得 203 檔／191 檔窗內（94.1%）；
若以 229 檔為分母則為 216 檔窗內（94.3%）。兩個比例出自不同母體，不可互相取代。<br><br>

<b>股票母體與站內 DD 母體的國籍判準不完全一致</b>：本頁 1,590 檔股票母體排除了 Spotify（SPOT，盧森堡註冊）與
MercadoLibre（MELI）；但站內 DD 覆蓋盤點採用不同判準，將這兩檔計入母體。兩套判準本頁未對帳，讀者交叉比對股票母體與
DD 母體檔數時應留意此差異。<br><br>

<b>跨頁口徑差</b>：S&amp;P 500 總市值本頁引用外部口徑 US${facts["sp500_total_mcap_usd_tn"]["value"]} 兆
（as-of {facts["sp500_total_mcap_usd_tn"]["as_of"]}，{facts["sp500_total_mcap_usd_tn"]["source_name"]}），
與本頁母體對 S&amp;P 500 成分股直接加總得到的市值不同，差距約 7%，兩者可能分屬流通量調整與全市值兩種口徑，本頁並陳不對帳，
下游若需引用應標明是哪一個口徑。
'''


# ---------------------------------------------------------------------------
# 5. 排版：CJK／英文（含 ticker、數字）自動留白一格
# ---------------------------------------------------------------------------

def add_cjk_latin_spacing(text):
    text = re.sub(r"([一-鿿])([A-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9])([一-鿿])", r"\1 \2", text)
    return text


# ---------------------------------------------------------------------------
# 6. HTML 外殼（head／CSS 沿用舊頁變數＋新增少量元件樣式）
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
.lenstable td.why{font-size:12.5px}
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
.basket{{background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:0 4px 4px 0;padding:16px 20px;margin-bottom:14px}}
.basket .tag{{font-family:'IBM Plex Mono',ui-monospace,monospace;display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:6px}}
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

    title = "美股國家掃描：十檔股票的指數，一千五百檔的兩種定價 | InvestmQuest Research"
    description = (
        "美股國家掃描研究記錄：S&P 1500＋市值≥US$100億補充名單共1,590檔宇宙（母體市值約US$83.97兆）。"
        "五個論點——指數集中度、AI資本支出週期、估值分裂、資本報酬地圖、不看價格的買盤結構——"
        "加上九個投資鏡頭全景掃描與229檔站內既有DD對帳。掃描是研究記錄，不是選股名單。"
    )

    conc = stats["conc"]
    masthead_h1 = "十檔股票決定 S&amp;P 500 的漲跌，其餘一千五百檔被市場拆成兩群定價"
    masthead_subt = (
        "本頁是 1,590 檔美股母體（S&amp;P 1500＋市值≥US$100 億非指數補充名單）的市場結構掃描：五個論點＋美股計分卡＋"
        "九個投資鏡頭全景結論，資料快照 " + SNAPSHOT_DATE + "，結構數字另附各自查證日期；本頁是研究記錄，不是投資建議，"
        "個股「值不值得投資」的裁決一律走站內 DD 統一裁決鏈。"
    )

    scorecard_html = build_scorecard(stats, facts)
    SCORECARD_N = build_scorecard.row_count

    body = []
    body.append(f'<div class="masthead"><div class="masthead-inner">')
    body.append('<div class="kicker">國家掃描 · 美國</div>')
    body.append(f'<h1>{masthead_h1}</h1>')
    body.append(f'<div class="subt">{masthead_subt}</div>')
    body.append('<div class="rule"></div>')
    body.append(
        '<div class="meta">'
        f'<span><b>掃描日期</b>　{SNAPSHOT_DATE}（資料快照，非持續更新）</span>'
        f'<span><b>母體</b>　S&amp;P 1500＋市值≥US$100億補充名單，共 {stats["count"]:,} 檔</span>'
        f'<span><b>覆蓋</b>　{stats["count"]:,} 檔母體 × 五個論點＋九個投資鏡頭</span>'
        '</div>'
    )
    body.append(
        '<div class="nature">本頁性質聲明：描述器／研究紀錄，非投資建議。五個論點與九個鏡頭收斂出的是判讀框架與資料事實，'
        '不是一張「買這些」的名單；個股「值不值得投資」的裁決一律走 DD 統一裁決鏈。</div>'
    )
    body.append('</div></div>')

    body.append('<div class="wrap">')

    # 一頁摘要
    body.append('<div class="exec-wrap"><div class="exec-hd">一頁摘要</div><ol class="exec">')
    body.append(build_exec_summary(stats, facts))
    body.append('</ol></div>')

    # key data strip
    body.append('<div class="kdstrip">')
    body.append(f'<div><div class="kl">母體規模（S&amp;P 1500＋補充名單）</div><div class="kv">{stats["count"]:,} 檔</div></div>')
    body.append(f'<div><div class="kl">S&amp;P 500 前十大權重</div><div class="kv">{facts["spy_top10_weight_pct"]["value"]}%</div></div>')
    body.append(f'<div><div class="kl">母體總市值</div><div class="kv">{usd_from_raw(stats["total_mcap"])}</div></div>')
    body.append(f'<div><div class="kl">站內 DD 覆蓋（其中 203 檔入九鏡頭）</div><div class="kv">229 檔</div></div>')
    body.append(f'<div><div class="kl">十年期公債／隱含 ERP</div><div class="kv">{facts["treasury_10y_pct"]["value"]}%／{facts["implied_erp_pct"]["value"]}%</div></div>')
    body.append('</div>')

    # toc
    toc_items = [
        ("s1", f"美股計分卡：{SCORECARD_N} 個指標速覽"),
        ("s2", "五個論點：集中度、AI 資本週期、估值分裂、資本報酬比較、買盤結構"),
        ("s3", "九個投資鏡頭一覽"),
        ("s4", "可作戰名單：已有裁決與零覆蓋候選"),
        ("s5", "會推翻本頁判斷的證據"),
        ("s6", "資料、方法與盲區"),
    ]
    body.append('<div class="toc"><div class="toc-hd">報告目錄</div><ol>')
    for i, (anchor, label) in enumerate(toc_items, 1):
        body.append(f'<li><a href="#{anchor}"><span class="n">§{i}</span>{label}</a></li>')
    body.append('</ol></div>')

    # §1 計分卡
    body.append(f'<div class="section" id="s1"><div class="section-hd"><div class="sec-eyebrow">Section I</div><h2>§1　美股計分卡：{SCORECARD_N} 個指標速覽</h2></div>')
    body.append('<div class="section-lead">母體算得出來的直接算，算不出來的查證後標明來源與查證日期；查不到的在「資料、方法與盲區」自陳，不沿用沒有出處的數字。</div>')
    body.append('<div class="exhibit scroll"><table><thead><tr><th>指標</th><th>數值</th><th>as-of</th><th>白話一句</th><th>來源</th></tr></thead><tbody>')
    body.append(scorecard_html)
    body.append('</tbody></table></div>')
    body.append('</div>')

    # §2 五個論點
    body.append('<div class="section" id="s2"><div class="section-hd"><div class="sec-eyebrow">Section II</div><h2>§2　五個論點：這個市場現在是什麼</h2></div>')
    body.append('<div class="section-lead">每個論點都是可以被推翻的具體主張，不是氣氛描述；推翻條件見 §5。</div>')
    body.append(build_arguments(stats, facts))
    body.append('</div>')

    # §3 九鏡頭
    body.append('<div class="section" id="s3"><div class="section-hd"><div class="sec-eyebrow">Section III</div><h2>§3　九個投資鏡頭一覽</h2></div>')
    body.append('<div class="section-lead">結論濃縮自各鏡頭子頁的第一節與答案節，數字回查子頁與母體檔案，不憑印象轉述；完整推理與逐檔對帳見各鏡頭子頁。</div>')
    body.append('<div class="exhibit scroll lenstable"><table><thead><tr><th>鏡頭</th><th>核心問題</th><th>一句結論</th><th>站內 DD 覆蓋</th><th>最大缺口</th></tr></thead><tbody>')
    body.append(build_lens_table())
    body.append('</tbody></table></div>')
    body.append(f'<div class="ex-sub" style="padding:0 4px">站內 DD 覆蓋盤點 as-of {DD_BASIS_DATE}（複審窗基準日，非本頁即時重算）；窗內比例＝90 天內完成之裁決占該鏡頭 DD 總數。</div>')
    body.append('</div>')

    # §4 可作戰名單
    body.append('<div class="section" id="s4"><div class="section-hd"><div class="sec-eyebrow">Section IV</div><h2>§4　可作戰名單：已有裁決與零覆蓋候選</h2></div>')
    body.append('<div class="section-lead">站內裁決逐字取自各檔案的決策層欄位（dca_verdict／dca_role），不改寫不總結；本頁不給買賣指令，個股「值不值得投資」一律點進 DD 查完整推理。</div>')
    body.append('<div class="exhibit scroll watchtable"><table><thead><tr><th>公司</th><th>鏡頭</th><th>站內裁決</th><th>在等什麼</th><th>DD 連結</th></tr></thead><tbody>')
    body.append(build_watchlist())
    body.append('</tbody></table></div>')
    body.append('</div>')

    # §5 falsifiers
    body.append('<div class="section" id="s5"><div class="section-hd"><div class="sec-eyebrow">Section V</div><h2>§5　會推翻本頁判斷的證據</h2></div>')
    body.append('<div class="section-lead">每一條論點都附一組具體、可觀察的反證條件，不是模糊的「情況可能改變」。</div>')
    body.append(build_falsifiers())
    body.append('</div>')

    # §6 方法論
    body.append('<div class="section" id="s6" style="padding-top:30px">')
    body.append('<details class="datanote"><summary>§6　資料、方法與盲區</summary><div class="dn-body">')
    body.append(build_methodology(stats, facts))
    body.append('</div></details>')
    body.append('</div>')

    body.append(
        '<div class="closing">本頁為掃描研究記錄（描述器），非選股名單、非買賣建議；個股「值不值得投資」的裁決一律走 DD 統一裁決鏈。</div>'
    )

    # 九子頁連結列
    body.append('<div class="footlinks">')
    for r in LENS_ROWS:
        body.append(f'<a href="us/{r["slug"]}.html">鏡頭{r["n"]}・{r["name"]}</a>')
    body.append('<a href="/backtest/#scan">回國家掃描</a>')
    body.append('</div>')

    body.append('</div>')  # .wrap

    body_str = "".join(body)
    body_str = add_cjk_latin_spacing(body_str)

    head = HEAD_TEMPLATE.format(title=title, description=description, extra=EXTRA_CSS)
    footer = (
        '<footer class="imq-foot">'
        '<div>© 2026 InvestMQuest Research</div>'
        '<div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議 · '
        '<a href="/backtest/#scan">回國家掃描</a></div>'
        '</footer></body></html>'
    )

    html = head + nav_snippet + body_str + footer
    return html, stats, facts


# ---------------------------------------------------------------------------
# 7. 自檢：--check
# ---------------------------------------------------------------------------

BANNED_METAPHOR_WORDS = ["煞車", "收費站", "水庫", "護城河", "藏寶圖", "尋寶", "像座", "彷彿", "宛如"]
BANNED_PROCESS_WORDS = ["sonnet", "Sonnet", "opus", "Opus", "agent", "Agent", "critic", "orchestrator",
                          "本輪", "上一版", "舊版"]
BANNED_CROSS_MARKET_WORDS = ["台灣", "台股", "TWSE", "日本", "東證", "TOPIX", "馬來西亞", "Bursa", "KLCI", "韓國", "Korea"]
BANNED_TRADE_CALL_WORDS = ["買進", "賣出", "加碼", "減碼", "停損", "目標價"]


def run_check(html_path):
    html = open(html_path, encoding="utf-8").read()
    problems = []

    def report(name, hits):
        if hits:
            problems.append(f"{name}: {len(hits)} 處命中 -> {hits[:5]}")

    # 1) 禁用比喻詞
    for w in BANNED_METAPHOR_WORDS:
        if w in html:
            report(f"禁用比喻詞「{w}」", [w] * html.count(w))

    # 2) 流程語氣詞（排除 nav 選單裡合法出現的字樣、排除本檔案自身路徑字串）
    body_only = html.split("<body>", 1)[-1]
    for w in BANNED_PROCESS_WORDS:
        if w in body_only:
            report(f"流程語氣詞「{w}」", [w] * body_only.count(w))

    # 3) 跨市場字樣（nav 既有字樣例外：/qgm-tw/ 等連結本身不含中文站名字串，直接檢查中文詞即可）
    for w in BANNED_CROSS_MARKET_WORDS:
        if w in body_only:
            report(f"跨市場字樣「{w}」", [w] * body_only.count(w))

    # 4) 買賣指令字樣
    for w in BANNED_TRADE_CALL_WORDS:
        if w in body_only:
            report(f"買賣指令字樣「{w}」", [w] * body_only.count(w))

    # 5) 半形標點（，,｜。 等常見誤用；允許程式碼／URL/屬性內半形逗號、句號）
    text_nodes = re.sub(r"<[^>]+>", "\n", body_only)
    text_nodes = re.sub(r"<style>.*?</style>", "", text_nodes, flags=re.S)
    halfwidth_hits = re.findall(r"[一-鿿][,.][一-鿿]", text_nodes)
    report("中文字之間夾半形逗號/句號", halfwidth_hits)

    # 6) 內部錨點完整性
    anchors = set(re.findall(r'id="([a-zA-Z0-9_-]+)"', html))
    hrefs = re.findall(r'href="#([a-zA-Z0-9_-]+)"', html)
    missing_anchor = [h for h in hrefs if h not in anchors]
    report("TOC 錨點缺失", missing_anchor)

    # 7) 九子頁連結存在性
    lens_dir = os.path.join(BASE, "..", "..", "..", "..", "docs", "backtest", "country_scan", "us")
    missing_pages = []
    for slug in re.findall(r'href="([a-z-]+\.html)"', html):
        p = os.path.normpath(os.path.join(lens_dir, slug))
        if not os.path.exists(p):
            missing_pages.append(slug)
    report("子頁連結缺失", missing_pages)

    # 8) DD 連結存在性（本頁引用的 docs/dd/*.html 需在來源 repo 存在；本頁只存路徑字串，若跑在本 repo 內可核對本機檔案）
    dd_dir_candidates = [
        os.path.join(BASE, "..", "..", "..", "..", "docs", "dd"),
    ]
    missing_dd = []
    for m in re.findall(r'DD_[A-Za-z0-9\-]+\.html', html):
        found = any(os.path.exists(os.path.join(d, m)) for d in dd_dir_candidates)
        if not found:
            missing_dd.append(m)
    report("DD 連結檔案缺失（本機比對）", sorted(set(missing_dd)))

    # 9) CJK-拉丁字元黏在一起（自動留白後應歸零）
    stuck = re.findall(r"[一-鿿][A-Za-z0-9][A-Za-z0-9]*|[A-Za-z0-9][一-鿿]", text_nodes)
    # 上面第一種 pattern 太寬鬆會誤抓已留白後的情形，改用更精準的「無空格緊鄰」偵測
    stuck2 = re.findall(r"[一-鿿][A-Za-z0-9]|[A-Za-z0-9][一-鿿]", text_nodes.replace(" ", ""))
    report("CJK 與英文/數字之間缺空格", stuck2)

    # 10) Exhibit 連號
    ex_nums = [int(x) for x in re.findall(r'Exhibit (\d+)', html)]
    if ex_nums != sorted(set(ex_nums)) or ex_nums != list(range(1, len(set(ex_nums)) + 1)):
        problems.append(f"Exhibit 連號異常: {ex_nums}")

    # 11) 計分卡／tile 數字必須可回溯到 _hub_facts.json 或母體現算結果
    facts = load_facts()
    uni = load_universe()
    stats = compute_population_stats(uni)
    plain = re.sub(r"<[^>]+>", "", body_only)

    for key in ("spy_top10_weight_pct", "mag7_weight_pct", "treasury_10y_pct", "implied_erp_pct",
                "odte_spx_pct", "passive_share_us_domestic_equity_pct", "overseas_revenue_share_pct",
                "activist_actions_2026h1", "ipo_priced_2026ytd"):
        v = str(facts[key]["value"])
        if v not in html:
            problems.append(f"facts[{key}].value={v} 未出現在頁面內文中")

    # 11a) 帶 source_url 的硬性要求：頁面引用到的結構數字都要有出處
    for key, e in facts.items():
        if key.startswith("_") or not isinstance(e, dict):
            continue
        if e.get("confidence") == "gap" or e.get("value") is None:
            continue
        if not e.get("source_url"):
            problems.append(f"facts[{key}] 有數值但缺 source_url")

    # 11b) 單位換算自檢：billions -> 億 必須 ×10，兆 必須 ÷1000（防億／兆混用）
    unit_checks = [
        (f'US${facts["ipo_proceeds_2026ytd_usd_bn"]["value"]*10:,.0f} 億', "IPO 募資總額"),
        (f'US${facts["buyback_q1_2025_usd_bn"]["value"]*10:,.0f} 億', "2025 Q1 回購"),
        (f'US${facts["buyback_q3_2025_usd_bn"]["value"]*10:,.0f} 億', "2025 Q3 回購"),
        (f'US${facts["buyback_ttm_usd_tn"]["value"]:.2f} 兆', "滾動 12 個月回購"),
    ]
    for expect, label in unit_checks:
        if add_cjk_latin_spacing(expect) not in plain:
            problems.append(f"單位換算檢查失敗：{label} 應出現「{expect}」")

    # 11c) 論點 B 差距倍數必須與 facts 現算一致
    for t in ("msft", "googl", "amzn", "meta", "orcl"):
        e = facts[f"capex_ai_{t}"]
        m = e["capex_yoy_pct"] / e["revenue_yoy_pct"]
        if add_cjk_latin_spacing(f"{m:.1f} 倍") not in plain:
            problems.append(f"capex_ai_{t} 差距倍數 {m:.1f} 倍未出現在頁面中")

    # 11d) 母體數字自檢：頁面印出的母體統計必須等於現算值
    pop_checks = [
        (f'{stats["conc"][10]["pct"]:.1f}%', "母體前十檔市值占比"),
        (f'{stats["pe_by_group"]["SP500"]["median"]:.1f} 倍', "S&P 500 前瞻本益比中位數"),
        (f'{stats["pe_by_group"]["SP600"]["median"]:.1f} 倍', "S&P 600 前瞻本益比中位數"),
        (f'{stats["roe_all_median"]:.1f}%', "母體 ROE 中位數"),
        (usd_from_raw(stats["total_mcap"]), "母體總市值"),
    ]
    for expect, label in pop_checks:
        if add_cjk_latin_spacing(expect) not in plain:
            problems.append(f"母體數字檢查失敗：{label} 應出現「{expect}」")

    # 11e) 九鏡頭 DD 檔數加總必須等於頁面宣稱的鏡頭母體檔數
    lens_dd = sum(r["n_dd"] for r in LENS_ROWS)
    lens_win = sum(r["n_win"] for r in LENS_ROWS)
    if f"{lens_dd} 檔歸入本頁九個鏡頭" not in plain:
        problems.append(f"九鏡頭 DD 加總 {lens_dd} 檔與頁面敘述對不上")
    if f"{lens_win} 檔在 90 天複審窗內" not in plain:
        problems.append(f"九鏡頭窗內加總 {lens_win} 檔與頁面敘述對不上")
    if add_cjk_latin_spacing(f"比例 {lens_win/lens_dd*100:.1f}%") not in plain:
        problems.append(f"九鏡頭窗內比例 {lens_win/lens_dd*100:.1f}% 與頁面敘述對不上")

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
            {k: v for k, v in stats.items() if k not in ("roe_rows", "sector_rows")},
            ensure_ascii=False, indent=2, default=str,
        ))
    elif "--check-only" in sys.argv:
        run_check(OUT_PATH)
    else:
        main_cli()
