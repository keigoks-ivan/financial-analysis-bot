#!/usr/bin/env python3
"""
台股國家掃描 hub 組裝腳本（重寫 2026-09-10）。

Usage:
  /opt/homebrew/bin/python3.12 _build_hub.py            # 產出 docs/backtest/country_scan/taiwan.html
  /opt/homebrew/bin/python3.12 _build_hub.py --check    # 產出後跑自檢，不重新寫檔亦可單獨執行

只用標準庫（json / statistics / math / re / os）。母體數字一律從 _universe.json 現算；
非母體的結構數字（台積電佔加權指數權重、MSCI權重、外資持股、ETF規模、當沖占比……）一律從
_hub_facts.json 讀取，每筆都帶 value / as_of / source_name / source_url / confidence，
禁止在內文手打數字。本檔照 notes/site-internal/country_scan/us/_build_hub.py 的結構與機制複製，
母體欄位改為台股口徑（market_cap_twd／twse_industry／board／is_electronics_broad）。
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
OUT_PATH = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "docs", "backtest", "country_scan", "taiwan.html"))

SNAPSHOT_DATE = "2026-08-14"
DD_BASIS_DATE = "2026-08-14"

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


def twd_yi_from_raw(v):
    """原始台幣數字（market_cap_twd）-> 「NT$X兆」（億=1e8，兆=1e12）。"""
    zhao = v / 1e12
    return f"NT${zhao:,.2f}兆"


def days_between(d1, d2):
    a = datetime.date.fromisoformat(d1)
    b = datetime.date.fromisoformat(d2)
    return (b - a).days


# ---------------------------------------------------------------------------
# 2. 母體統計（全部從 _universe.json 現算）
# ---------------------------------------------------------------------------

# AI 硬體代工鏈 29 檔分層（見鏡頭二子頁 Exhibit 9 已查證分類；毛利率數字本檔對
# _universe.json 同批快照現算，不沿用子頁寫死的數字）
AI_HW_STRUCT = ["2059", "3533", "3653", "2308", "2368", "8210", "3665", "2383",
                "6805", "3017", "3324", "3044", "6274", "2301", "4958", "2313",
                "3037", "8046", "6213"]
AI_HW_NETWORK = ["2345", "3596", "5388", "6285"]
AI_HW_ASSEMBLY = ["3706", "6669", "2317", "2382", "3231", "2356"]

# 記憶體與測試鏈（盲區自陳用）：南亞科／華邦電／群聯／鴻勁／旺矽，佔比由母體快照現算
MEMORY_TEST_CHAIN = ["2408", "2344", "8299", "7769", "6223"]

TOP_INDUSTRY_N = 12


def compute_population_stats(uni):
    cons = uni["constituents"]
    total_mcap = sum(c["market_cap_twd"] for c in cons if c.get("market_cap_twd"))
    count = len(cons)
    n_twse = sum(1 for c in cons if c.get("board") == "TWSE")
    n_tpex = sum(1 for c in cons if c.get("board") == "TPEx")

    srt = sorted(cons, key=lambda c: -(c.get("market_cap_twd") or 0))

    def topn_share(n):
        s = sum(c["market_cap_twd"] for c in srt[:n])
        return s, s / total_mcap * 100

    conc = {}
    for n in (1, 10, 50, 100):
        s, p = topn_share(n)
        conc[n] = {"mcap": s, "pct": p}
    conc["rest"] = {"pct": 100 - conc[100]["pct"]}

    tsm = next(c for c in cons if c["code"] == "2330")
    tsm_pop_pct = tsm["market_cap_twd"] / total_mcap * 100

    # 33 類 TWSE 產業別市值分布
    ind = defaultdict(float)
    indcount = defaultdict(int)
    for c in cons:
        k = c.get("twse_industry") or "未分類"
        mc = c.get("market_cap_twd") or 0
        ind[k] += mc
        indcount[k] += 1
    industry_rows = sorted(
        ({"industry": k, "mcap": v, "pct": v / total_mcap * 100, "n": indcount[k]} for k, v in ind.items()),
        key=lambda r: -r["pct"],
    )
    top_industries = industry_rows[:TOP_INDUSTRY_N]
    rest_industry_pct = 100 - sum(r["pct"] for r in top_industries)
    rest_industry_n = count - sum(r["n"] for r in top_industries)

    semis_row = next(r for r in industry_rows if r["industry"] == "半導體業")
    tsm_semis_pct = tsm["market_cap_twd"] / semis_row["mcap"] * 100

    # 電子業廣義 vs 非電子業（is_electronics_broad 欄位）
    elec = [c for c in cons if c.get("is_electronics_broad")]
    nonelec = [c for c in cons if not c.get("is_electronics_broad")]
    elec_mcap = sum(c["market_cap_twd"] for c in elec if c.get("market_cap_twd"))
    elec_pct = elec_mcap / total_mcap * 100

    def pe_quartiles(group, field="forward_pe"):
        vals = sorted(c[field] for c in group if c.get(field) is not None and c[field] > 0)
        n = len(vals)
        if n == 0:
            return None
        return {
            "n": n,
            "median": st.median(vals),
            "q1": vals[n // 4],
            "q3": vals[(3 * n) // 4],
        }

    pe_elec = pe_quartiles(elec)
    pe_nonelec = pe_quartiles(nonelec)

    def revg_median(group):
        vals = [c["revenue_growth"] * 100 for c in group if c.get("revenue_growth") is not None]
        return st.median(vals) if vals else None

    revg_elec = revg_median(elec)
    revg_nonelec = revg_median(nonelec)

    # ROE：全母體中位數
    roe_all = [c["roe"] * 100 for c in cons if c.get("roe") is not None]
    roe_all_median = st.median(roe_all)

    # ROE：前12類產業 x 上市(TWSE)/上櫃(TPEx)
    roe_data = defaultdict(lambda: defaultdict(list))
    for c in cons:
        k = c.get("twse_industry") or "未分類"
        b = c.get("board")
        if c.get("roe") is not None:
            roe_data[k][b].append(c["roe"] * 100)
    roe_rows = []
    for r in top_industries:
        k = r["industry"]
        byboard = roe_data.get(k, {})
        row = {"industry": k}
        for b in ("TWSE", "TPEx"):
            vals = byboard.get(b, [])
            row[b] = {"n": len(vals), "median": (st.median(vals) if vals else None)}
        roe_rows.append(row)

    # 殖利率 >= 6% 篩選（欄位 dividend_yield 已是百分比數值，如 1.15 代表 1.15%）
    dy6 = [c for c in cons if c.get("dividend_yield") is not None and c["dividend_yield"] >= 6]
    dy6_pe_vals = sorted(c["trailing_pe"] for c in dy6 if c.get("trailing_pe") is not None and c["trailing_pe"] > 0)
    dy6_pe_median = st.median(dy6_pe_vals) if dy6_pe_vals else None

    all_pe_vals = sorted(c["trailing_pe"] for c in cons if c.get("trailing_pe") is not None and c["trailing_pe"] > 0)
    all_pe_median = st.median(all_pe_vals)

    # 殖利率分布直方圖（8個桶）
    dy_all = [c["dividend_yield"] for c in cons if c.get("dividend_yield") is not None]
    dy_buckets_def = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (8, 9999)]
    dy_hist = []
    for lo, hi in dy_buckets_def:
        n = sum(1 for v in dy_all if lo <= v < hi)
        label = f"{lo}–{hi}%" if hi < 9999 else f"≥{lo}%"
        dy_hist.append({"label": label, "n": n})
    dy_no_dividend = count - len(dy_all)

    # AI 硬體代工鏈三層毛利率（快照口徑，本檔對 _universe.json 現算）
    def find(code):
        return next((c for c in cons if c["code"] == code), None)

    def gm_list(codes):
        out = []
        for code in codes:
            c = find(code)
            if c and c.get("gross_margins") is not None:
                out.append(c["gross_margins"] * 100)
        return out

    mem_mcap = sum((find(code) or {}).get("market_cap_twd") or 0 for code in MEMORY_TEST_CHAIN)

    ai_struct_gm = gm_list(AI_HW_STRUCT)
    ai_network_gm = gm_list(AI_HW_NETWORK)
    ai_assembly_gm = gm_list(AI_HW_ASSEMBLY)

    return {
        "count": count,
        "n_twse": n_twse,
        "n_tpex": n_tpex,
        "total_mcap": total_mcap,
        "conc": conc,
        "tsm_pop_pct": tsm_pop_pct,
        "industry_rows": industry_rows,
        "top_industries": top_industries,
        "rest_industry_pct": rest_industry_pct,
        "rest_industry_n": rest_industry_n,
        "semis_row": semis_row,
        "tsm_semis_pct": tsm_semis_pct,
        "elec_n": len(elec),
        "nonelec_n": len(nonelec),
        "elec_pct": elec_pct,
        "pe_elec": pe_elec,
        "pe_nonelec": pe_nonelec,
        "revg_elec": revg_elec,
        "revg_nonelec": revg_nonelec,
        "roe_all_median": roe_all_median,
        "roe_rows": roe_rows,
        "dy6_n": len(dy6),
        "dy6_pct": len(dy6) / count * 100,
        "dy6_pe_median": dy6_pe_median,
        "all_pe_median": all_pe_median,
        "dy_hist": dy_hist,
        "dy_no_dividend": dy_no_dividend,
        "ai_struct_gm_median": st.median(ai_struct_gm),
        "ai_struct_n": len(ai_struct_gm),
        "ai_network_gm_min": min(ai_network_gm),
        "ai_network_gm_max": max(ai_network_gm),
        "ai_network_n": len(ai_network_gm),
        "ai_assembly_gm_median": st.median(ai_assembly_gm),
        "ai_assembly_n": len(ai_assembly_gm),
        "mem_chain_semis_pct": mem_mcap / semis_row["mcap"] * 100,
        "mem_chain_pop_pct": mem_mcap / total_mcap * 100,
        "shipping_n": indcount.get("航運業", 0),
        "shipping_pct": ind.get("航運業", 0) / total_mcap * 100,
        "plastics_n": indcount.get("塑膠工業", 0),
        "plastics_pct": ind.get("塑膠工業", 0) / total_mcap * 100,
        "biotech_n": indcount.get("生技醫療業", 0),
        "biotech_pct": ind.get("生技醫療業", 0) / total_mcap * 100,
        "financials_n": indcount.get("金融保險業", 0),
        "financials_pct": ind.get("金融保險業", 0) / total_mcap * 100,
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
    return (
        f'<svg viewBox="0 0 {SVG_W} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}" '
        f'style="display:block;font-family:\'IBM Plex Mono\',ui-monospace,monospace">{inner}</svg>'
    )


def svg_exhibit_a(stats):
    """論點A：母體市值集中度（台積電／第2–10檔／第11–50檔／第51–100檔／其餘）＋前12類產業市值長條。"""
    conc = stats["conc"]
    segs = [
        ("台積電一檔", conc[1]["pct"], C_ACCENT),
        ("第2–10檔", conc[10]["pct"] - conc[1]["pct"], C_ACCENT2),
        ("第11–50檔", conc[50]["pct"] - conc[10]["pct"], C_GOLD),
        ("第51–100檔", conc[100]["pct"] - conc[50]["pct"], C_GOLD_SOFT),
        (f"第101–{stats['count']}檔", conc["rest"]["pct"], "#cfc9b8"),
    ]
    bar_x, bar_y, bar_w, bar_h = 20, 46, SVG_W - 40, 46
    parts = []
    parts.append(
        f'<text x="{bar_x}" y="24" font-size="14" font-weight="700" fill="{C_INK}">'
        f'母體市值累積占比（依市值排序，{stats["count"]}檔＝100%）</text>'
    )
    x = bar_x
    for name, pct, color in segs:
        w = bar_w * pct / 100
        parts.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" fill="{color}"/>')
        if w > 40:
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
        lx += 17 + len(name) * 12 + 24

    sec_y0 = ly + 34
    parts.append(
        f'<text x="{bar_x}" y="{sec_y0}" font-size="14" font-weight="700" fill="{C_INK}">'
        f"母體市值依 TWSE 官方 33 類產業別分布（前 {TOP_INDUSTRY_N} 類）</text>"
    )
    rows = stats["top_industries"]
    row_h = 26
    max_pct = max(r["pct"] for r in rows)
    label_w = 210  # 「電腦及週邊設備業（42 檔）」在 11.5px 下約 150px，留足不被長條蓋住
    chart_x = bar_x + label_w
    chart_w = bar_w - label_w - 70
    y = sec_y0 + 18
    for r in rows:
        w = chart_w * r["pct"] / max_pct
        bar_color = C_ACCENT if r["industry"] == "半導體業" else C_ACCENT2
        parts.append(
            f'<text x="{bar_x}" y="{y+row_h*0.62:.1f}" font-size="12" fill="{C_BODY}">'
            f'{esc(r["industry"])}（{r["n"]}檔）</text>'
        )
        parts.append(f'<rect x="{chart_x}" y="{y+4}" width="{w:.1f}" height="{row_h-12}" rx="2" fill="{bar_color}"/>')
        parts.append(
            f'<text x="{chart_x+w+8:.1f}" y="{y+row_h*0.62:.1f}" font-size="12" font-weight="700" '
            f'fill="{C_INK}">{r["pct"]:.2f}%</text>'
        )
        y += row_h
    parts.append(
        f'<text x="{bar_x}" y="{y+16:.1f}" font-size="12" fill="{C_SEC}">'
        f'其餘 21 類產業（{stats["rest_industry_n"]}檔）合計 {stats["rest_industry_pct"]:.2f}%</text>'
    )
    total_h = y + 34
    return svg_wrap("".join(parts), total_h, "母體市值集中度與TWSE產業分布")


def svg_exhibit_b(stats):
    """論點B：電子業廣義 vs 非電子業前瞻本益比分布（四分位）＋AI硬體代工鏈三層毛利率。"""
    groups = [
        (f'電子業廣義（{stats["elec_n"]}檔）', stats["pe_elec"]),
        (f'非電子業（{stats["nonelec_n"]}檔）', stats["pe_nonelec"]),
    ]
    axis_max = 40.0
    bar_x, chart_w = 160, SVG_W - 160 - 90
    top = 44
    row_h = 56
    parts = [
        f'<text x="20" y="20" font-size="14" font-weight="700" fill="{C_INK}">'
        f"前瞻本益比分布：電子業廣義 vs 非電子業（第一四分位—中位數—第三四分位，超出 {axis_max:.0f} 倍以箭頭標示）</text>"
    ]

    def xpos(v):
        return bar_x + min(v, axis_max) / axis_max * chart_w

    for t in (0, 10, 20, 30, 40):
        tx = xpos(t)
        parts.append(
            f'<line x1="{tx:.1f}" y1="{top-6}" x2="{tx:.1f}" y2="{top + row_h*2+6}" '
            f'stroke="{C_BORDER}" stroke-width="1"/>'
        )
        parts.append(f'<text x="{tx:.1f}" y="{top-10}" font-size="12" fill="{C_SEC}" text-anchor="middle">{t}倍</text>')

    y = top
    for name, g in groups:
        parts.append(f'<text x="20" y="{y+row_h/2+5:.1f}" font-size="12" fill="{C_BODY}">{esc(name)}</text>')
        x1, xm, x3 = xpos(g["q1"]), xpos(g["median"]), xpos(g["q3"])
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y+row_h/2:.1f}" x2="{x3:.1f}" y2="{y+row_h/2:.1f}" '
            f'stroke="{C_ACCENT2}" stroke-width="6" stroke-linecap="round"/>'
        )
        parts.append(f'<circle cx="{xm:.1f}" cy="{y+row_h/2:.1f}" r="7" fill="{C_GOLD_DEEP}"/>')
        parts.append(
            f'<text x="{xm:.1f}" y="{y+row_h/2-14:.1f}" font-size="12" font-weight="700" fill="{C_INK}" '
            f'text-anchor="middle">中位數 {g["median"]:.1f}倍</text>'
        )
        parts.append(f'<text x="{x1:.1f}" y="{y+row_h/2+22:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{g["q1"]:.1f}</text>')
        parts.append(f'<text x="{x3:.1f}" y="{y+row_h/2+22:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{g["q3"]:.1f}</text>')
        y += row_h

    sec_y0 = y + 24
    parts.append(
        f'<text x="20" y="{sec_y0}" font-size="14" font-weight="700" fill="{C_INK}">'
        "AI 硬體代工鏈毛利率三層落差（快照口徑，本頁自算）</text>"
    )
    bars = [
        (f'結構層（{stats["ai_struct_n"]}檔）', stats["ai_struct_gm_median"], stats["ai_struct_gm_median"], C_ACCENT),
        (
            f'網通交換器層（{stats["ai_network_n"]}檔）',
            stats["ai_network_gm_min"],
            stats["ai_network_gm_max"],
            C_GOLD,
        ),
        (f'組裝層（{stats["ai_assembly_n"]}檔）', stats["ai_assembly_gm_median"], stats["ai_assembly_gm_median"], C_ACCENT2),
    ]
    max_v = 32.0
    chart_x2 = bar_x
    chart_w2 = SVG_W - chart_x2 - 100
    yy = sec_y0 + 20
    rh2 = 34
    for name, lo, hi, color in bars:
        w_lo = chart_w2 * min(lo, max_v) / max_v
        w_hi = chart_w2 * min(hi, max_v) / max_v
        parts.append(f'<text x="20" y="{yy+rh2/2+4:.1f}" font-size="12" fill="{C_BODY}">{esc(name)}</text>')
        if abs(hi - lo) < 0.01:
            parts.append(f'<rect x="{chart_x2}" y="{yy+6}" width="{w_lo:.1f}" height="{rh2-16}" rx="2" fill="{color}"/>')
            parts.append(
                f'<text x="{chart_x2+w_lo+8:.1f}" y="{yy+rh2/2+4:.1f}" font-size="12" font-weight="700" '
                f'fill="{C_INK}">中位數 {lo:.1f}%</text>'
            )
        else:
            parts.append(f'<rect x="{chart_x2+w_lo:.1f}" y="{yy+6}" width="{(w_hi-w_lo):.1f}" height="{rh2-16}" rx="2" fill="{color}"/>')
            parts.append(
                f'<text x="{chart_x2+w_hi+8:.1f}" y="{yy+rh2/2+4:.1f}" font-size="12" font-weight="700" '
                f'fill="{C_INK}">{lo:.1f}%–{hi:.1f}%</text>'
            )
        yy += rh2
    total_h = yy + 14
    return svg_wrap("".join(parts), total_h, "電子業與非電子業前瞻本益比分布及AI硬體代工鏈毛利率三層")


def svg_exhibit_c(stats):
    """論點C：ROE中位數，前12類TWSE產業 x 上市(TWSE)/上櫃(TPEx)。"""
    rows = stats["roe_rows"]
    bar_x, label_w = 20, 130
    chart_x = bar_x + label_w
    chart_w = SVG_W - chart_x - 130
    max_v = 30.0
    row_h = 40
    sub_h = 12
    top = 38
    MIN_N = 5  # 樣本數低於此值的組別灰化，並在標籤上寫明不可比
    C_TOOSMALL = "#c9c2b0"
    parts = [
        f'<text x="{bar_x}" y="18" font-size="14" font-weight="700" fill="{C_INK}">'
        f"ROE 中位數：TWSE 官方前 {TOP_INDUSTRY_N} 大產業別 × 上市／上櫃"
        f"（樣本數少於 {MIN_N} 檔的組別以灰色標示，不可與其他組別比較）</text>"
    ]

    def xpos(v):
        return chart_w * min(v, max_v) / max_v

    series = [("TWSE", "上市", C_ACCENT), ("TPEx", "上櫃", C_GOLD)]
    y = top
    for r in rows:
        parts.append(f'<text x="{bar_x}" y="{y+row_h/2+4:.1f}" font-size="12" fill="{C_BODY}">{esc(r["industry"])}</text>')
        sy = y + 3
        for key, _, color in series:
            v = r[key]["median"]
            n = r[key]["n"]
            if v is not None:
                small = n < MIN_N
                w = xpos(v)
                parts.append(
                    f'<rect x="{chart_x}" y="{sy:.1f}" width="{w:.1f}" height="{sub_h}" '
                    f'fill="{C_TOOSMALL if small else color}"/>'
                )
                tail = f"（n={n}，樣本不足不可比）" if small else f"（n={n}）"
                parts.append(
                    f'<text x="{chart_x+w+6:.1f}" y="{sy+sub_h-1.5:.1f}" font-size="12" '
                    f'fill="{C_SEC if small else C_INK}">{v:.1f}%{tail}</text>'
                )
            else:
                parts.append(f'<text x="{chart_x+4}" y="{sy+sub_h-1.5:.1f}" font-size="12" fill="{C_SEC}">無樣本</text>')
            sy += sub_h + 4
        y += row_h
    ly = y + 8
    lx = chart_x
    legend = series + [(None, f"樣本不足 {MIN_N} 檔", C_TOOSMALL)]
    for key, name, color in legend:
        parts.append(f'<rect x="{lx}" y="{ly-11}" width="13" height="13" fill="{color}"/>')
        parts.append(f'<text x="{lx+18}" y="{ly}" font-size="12" fill="{C_BODY}">{esc(name)}</text>')
        lx += 18 + len(name) * 13 + 24
    total_h = ly + 14
    return svg_wrap("".join(parts), total_h, "ROE中位數依TWSE產業與上市上櫃分層對照")


def svg_exhibit_d(stats, facts):
    """論點D：母體殖利率分布直方＋三大高股息ETF規模。"""
    hist = stats["dy_hist"]
    bar_x, top = 24, 40
    chart_w = 420
    max_n = max(h["n"] for h in hist)
    bw = 40
    gap = 12
    base_y = top + 130
    parts = [f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">母體殖利率分布（{stats["count"]}檔）</text>']
    x = bar_x
    for h in hist:
        hh = 130 * h["n"] / max_n
        color = C_GOLD_DEEP if h["label"].startswith(("6", "≥")) else C_ACCENT2
        parts.append(f'<rect x="{x:.1f}" y="{base_y-hh:.1f}" width="{bw}" height="{hh:.1f}" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{base_y-hh-6:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{h["n"]}</text>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{base_y+15:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{h["label"]}</text>')
        x += bw + gap
    parts.append(
        f'<text x="{bar_x}" y="{base_y+36:.1f}" font-size="12" fill="{C_SEC}">'
        f'不配息／無資料 {stats["dy_no_dividend"]} 檔未列入直方；殖利率≥6% 共 {stats["dy6_n"]} 檔'
        f'（{stats["dy6_pct"]:.2f}%）</text>'
    )
    parts.append(
        f'<text x="{bar_x}" y="{base_y+54:.1f}" font-size="12" fill="{C_SEC}">'
        f'這 {stats["dy6_n"]} 檔的中位數本益比 {stats["dy6_pe_median"]:.2f} 倍，'
        f'遠低於母體整體中位數 {stats["all_pe_median"]:.2f} 倍</text>'
    )

    x2 = bar_x + chart_w + 50
    parts.append(f'<text x="{x2}" y="20" font-size="14" font-weight="700" fill="{C_INK}">三大高股息 ETF 資產規模</text>')
    etfs = [
        ("0056", facts["etf_0056_snapshot"]["value"]["size_billion_twd"]),
        ("00878", facts["etf_00878_snapshot"]["value"]["size_billion_twd"]),
        ("00919", facts["etf_00919_snapshot"]["value"]["size_billion_twd"]),
    ]
    max_v2 = max(v for _, v in etfs) * 1.15
    bw2 = 86
    gap2 = 30
    xx = x2
    for name, v in etfs:
        hh = 130 * v / max_v2
        parts.append(f'<rect x="{xx}" y="{base_y-hh:.1f}" width="{bw2}" height="{hh:.1f}" rx="3" fill="{C_ACCENT}"/>')
        parts.append(
            f'<text x="{xx+bw2/2:.1f}" y="{base_y-hh-8:.1f}" font-size="12" font-weight="700" fill="{C_INK}" '
            f'text-anchor="middle">NT${v*10:,.0f}億</text>'
        )
        parts.append(f'<text x="{xx+bw2/2:.1f}" y="{base_y+16:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{name}</text>')
        xx += bw2 + gap2
    total_sum = sum(v for _, v in etfs)
    parts.append(
        f'<text x="{x2}" y="{base_y+36:.1f}" font-size="12" fill="{C_GOLD_DEEP}" font-weight="700">'
        f'三檔合計 NT${total_sum*10:,.0f}億（約 NT${total_sum/1000:.2f}兆）</text>'
    )
    total_h = base_y + 68
    return svg_wrap("".join(parts), total_h, "母體殖利率分布與三大高股息ETF規模")


def svg_exhibit_e(facts):
    """論點E：MSCI台灣權重時間序列＋TWSE官方當沖占比月序列。"""
    pts = [
        ("2025 Q3", facts["msci_tw_weight_2025q3_pct"]["value"]),
        ("2026-08\n調整前", facts["msci_tw_weight_pre_adjust_pct"]["value"]),
        ("2026-08-31\n生效", facts["msci_tw_weight_announced_pct"]["value"]),
    ]
    bar_x, top = 24, 44
    chart_w = 380
    chart_h = 140
    max_v = 30.0
    parts = [f'<text x="{bar_x}" y="20" font-size="14" font-weight="700" fill="{C_INK}">MSCI 新興市場指數台灣權重時間序列</text>']
    step = chart_w / (len(pts) - 1)
    coords = []
    for i, (label, v) in enumerate(pts):
        x = bar_x + i * step
        y = top + chart_h - chart_h * v / max_v
        coords.append((x, y))
    path = " L ".join(f"{x:.1f} {y:.1f}" for x, y in coords)
    parts.append(f'<path d="M {path}" fill="none" stroke="{C_GOLD_DEEP}" stroke-width="3"/>')
    for (x, y), (label, v) in zip(coords, pts):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{C_ACCENT}"/>')
        parts.append(f'<text x="{x:.1f}" y="{y-12:.1f}" font-size="12.5" font-weight="700" fill="{C_INK}" text-anchor="middle">{v:.2f}%</text>')
        for j, seg in enumerate(label.split("\n")):
            parts.append(f'<text x="{x:.1f}" y="{top+chart_h+16+j*13:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{esc(seg)}</text>')
    y0 = top + chart_h + 40

    x2 = bar_x + chart_w + 70
    parts.append(f'<text x="{x2}" y="20" font-size="14" font-weight="700" fill="{C_INK}">TWSE 官方當沖成交值占比（2026 年月序列）</text>')
    months = [
        ("01", facts["daytrade_share_202601_pct"]["value"]),
        ("02", facts["daytrade_share_202602_pct"]["value"]),
        ("03", facts["daytrade_share_202603_pct"]["value"]),
        ("04", facts["daytrade_share_202604_pct"]["value"]),
        ("06", facts["daytrade_share_202606_pct"]["value"]),
        ("07", facts["daytrade_share_202607_pct"]["value"]),
        ("08", facts["daytrade_share_202608_pct"]["value"]),
    ]
    chart_w2 = SVG_W - x2 - 30
    bw2 = chart_w2 / len(months) - 8
    max_v2 = 50.0
    base_y2 = top + chart_h
    for i, (m, v) in enumerate(months):
        x = x2 + i * (bw2 + 8)
        hh = chart_h * v / max_v2
        parts.append(f'<rect x="{x:.1f}" y="{base_y2-hh:.1f}" width="{bw2:.1f}" height="{hh:.1f}" rx="2" fill="{C_ACCENT2}"/>')
        parts.append(f'<text x="{x+bw2/2:.1f}" y="{base_y2-hh-6:.1f}" font-size="12" font-weight="700" fill="{C_INK}" text-anchor="middle">{v:.1f}%</text>')
        parts.append(f'<text x="{x+bw2/2:.1f}" y="{base_y2+16:.1f}" font-size="12" fill="{C_SEC}" text-anchor="middle">{m}月</text>')
    parts.append(f'<line x1="{x2}" y1="{base_y2:.1f}" x2="{SVG_W-30}" y2="{base_y2:.1f}" stroke="{C_BORDER}" stroke-width="1"/>')

    total_h = y0 + 20
    return svg_wrap("".join(parts), total_h, "MSCI台灣權重時間序列與TWSE當沖占比月序列")


# ---------------------------------------------------------------------------
# 4. 內文組裝
# ---------------------------------------------------------------------------

DD_DOC_BASE = "https://research.investmquest.com/dd"


def name_tag(cn, code):
    return f"{esc(cn)}（{code}）"


def tile(v, l):
    return f'<div class="t"><div class="v">{v}</div><div class="l">{esc(l)}</div></div>'


def build_exec_summary(stats, facts):
    conc = stats["conc"]
    tr = facts["sector_total_return_16y"]["value"]
    items = [
        f'<b>台積電（2330）一檔股票，分母不同就有四個不一樣但都成立的占比</b>——佔加權指數權重 '
        f'{facts["taiex_tsm_weight_pct"]["value"]:.2f}%（as-of {facts["taiex_tsm_weight_pct"]["as_of"]}，taifex.com.tw）、'
        f'佔 0050 成分股權重 {facts["etf0050_tsm_weight_pct"]["value"]:.2f}%（as-of {facts["etf0050_tsm_weight_pct"]["as_of"]}）、'
        f'佔本頁 {stats["count"]} 檔母體（TWSE 上市＋TPEx 上櫃，市值≥NT$100億的常規股票集合）市值 '
        f'{stats["tsm_pop_pct"]:.2f}%（{SNAPSHOT_DATE}快照，本頁自算）、'
        f'佔 TWSE 半導體業分類（{stats["semis_row"]["n"]}檔）市值 {stats["tsm_semis_pct"]:.1f}%——'
        f"四個數字分母遞減、口徑各自成立，判讀任何「台積電佔比」前先確認是哪一個分母、哪一個 as-of。",

        f'<b>電子與非電子是市場用價格分開對待的兩種台股</b>——電子業廣義（{stats["elec_n"]}檔）前瞻本益比'
        f'（股價除以分析師預估未來一年每股盈餘，數字越低代表用同樣一塊錢的預期獲利換到的股價越便宜）中位數 '
        f'{stats["pe_elec"]["median"]:.1f} 倍、營收成長率中位數 {stats["revg_elec"]:.1f}%，'
        f'非電子業（{stats["nonelec_n"]}檔）僅 {stats["pe_nonelec"]["median"]:.1f} 倍、{stats["revg_nonelec"]:.1f}%'
        f'（{SNAPSHOT_DATE}快照，本頁自算）。AI 硬體代工鏈內部同樣分裂：結構層（散熱／電源／PCB／連接器／機殼，'
        f'{stats["ai_struct_n"]}檔）毛利率（營收扣掉直接生產成本後的比率，反映產品的定價能力）中位數 '
        f'{stats["ai_struct_gm_median"]:.1f}%，'
        f'組裝層（ODM，代工廠依客戶設計圖生產，{stats["ai_assembly_n"]}檔）僅 {stats["ai_assembly_gm_median"]:.1f}%，'
        f'網通交換器層（{stats["ai_network_n"]}檔）介於 {stats["ai_network_gm_min"]:.1f}%–{stats["ai_network_gm_max"]:.1f}% 之間自成第三層。',

        "<b>671 檔母體篩到真複利股僅剩 8 檔，隱形冠軍地位不等於資本報酬</b>——ROE"
        "（股東權益報酬率，公司用股東出的每一塊錢賺回多少）≥15% 量化篩先篩出 153 檔，"
        "十年歷史查證後僅 8 檔無結構性下滑；16 檔「全球或區域市佔前三」隱形冠軍候選 ROE 中位數僅 9.15%，"
        f"10 檔（62.5%）是個位數，市佔壟斷程度與資本報酬率沒有正相關（完整推理見鏡頭子頁）。母體整體 ROE 中位數 "
        f'{stats["roe_all_median"]:.1f}%（{SNAPSHOT_DATE}快照，本頁自算，中位數天然排除少數極端值）。',

        f'<b>「高息」與「真收息」在台股母體中幾乎是兩批不同的名字</b>——{stats["count"]} 檔母體中殖利率'
        f'（配息除以股價，衡量取得成本能換回多少現金股利的比率）≥6% 者僅 '
        f'{stats["dy6_n"]} 檔（{stats["dy6_pct"]:.2f}%），中位數本益比 {stats["dy6_pe_median"]:.2f} 倍、'
        f'遠低於母體整體中位數 {stats["all_pe_median"]:.2f} 倍。但這只是第一條篩查線；另一條獨立線不限定殖利率，'
        "直接對全母體套用 FCF（自由現金流，公司在支付營運與資本支出後實際留下的現金）覆蓋率×連續配息年資×"
        "本業現金流品質三判準，篩出 7 檔綠燈＋4 檔黃燈，"
        "其中電信三雄、中保科、大台北瓦斯、億豐五檔殖利率均低於 6%——真正禁得起考驗的收息股，多數不在高息排行榜前段。",

        f'<b>台股的買盤結構由外資、被動基金與當沖三股力量共同定價</b>——外資持股占大盤市值約 '
        f'{facts["foreign_holding_share_pct"]["value"]}%（as-of {facts["foreign_holding_share_pct"]["as_of"]}）；'
        "MSCI（摩根士丹利資本國際公司編製的全球指數系列，決定全球被動基金該把多少資金配置到台股的重要依據）"
        f'新興市場指數台灣權重 {facts["msci_tw_weight_announced_pct"]["value"]}%'
        f'（{facts["msci_tw_weight_announced_pct"]["as_of"]}，躍居該指數第一大市場）；'
        f'台股 ETF 受益人數 {facts["tw_etf_holders_202608_count"]["value"]/10000:,.0f} 萬人次'
        f'（as-of {facts["tw_etf_holders_202608_count"]["as_of"]}，94 檔逐檔加總，同一人持多檔會重複計算）；當沖'
        "（當日內買賣同一檔股票、不留倉過夜的交易方式）占大盤成交值比重 2026 年多數月份落在 3–4 成，"
        f'{facts["daytrade_share_202608_pct"]["as_of"]} 已升破四成達 {facts["daytrade_share_202608_pct"]["value"]}%。'
        "被動資金（跟隨指數比例自動配置、不判斷個股貴不貴的資金）與當沖都是規則驅動的買盤；"
        "台股漲跌幅限制±10%，事件驅動股價若真實調整超過此幅度，價格發現會被迫跨多日以連續漲跌停完成。",

        f'<b>站內既有 DD 研究集中在半導體與 AI 硬體兩條鏈，{stats["financials_n"]} 檔金融保險業標的仍是空白</b>'
        f'——{len(WATCH_EXISTING)} 份已完成 DD '
        "全數落在鏡頭一（半導體核心鏈）與鏡頭二（AI硬體與電子代工），複利機器、隱形冠軍、內需通路、金融、"
        f'收息、資產與事件六個鏡頭站內零覆蓋，其中金融保險業標的合計佔母體市值 {stats["financials_pct"]:.1f}%，'
        "是量體不小但研究覆蓋掛零的最明顯板塊。",

        "<b>電子股是拉開台股長期複利報酬差距的最主要來源</b>——2009-01-05 至 2025-10-31（約 16.8 年）的報酬指數"
        "（把配息再投入後計算的指數，衡量含息總報酬）累積漲幅：電子類 "
        f'+{tr["電子類報酬指數"]:,.1f}%、大盤含息 +{tr["加權報酬指數（大盤含息）"]:,.1f}%、'
        f'金融保險類 +{tr["金融保險類報酬指數"]:,.1f}%、水泥類 +{tr["水泥類報酬指數"]:,.1f}%、'
        f'鋼鐵類 +{tr["鋼鐵類報酬指數"]:,.1f}%——電子類漲幅約為大盤含息的 1.6 倍、金融保險類的 3 倍、'
        "水泥／鋼鐵的 8–9 倍（此組回測為基金業者以 TWSE 指數資料庫自算、媒體轉引，非 TWSE 官方直接公布，"
        "本頁列中信心度）；"
        f'2026 年 GDP 成長率預測上修至 {facts["gdp_growth_2026_pct"]["value"]}%'
        f'（{facts["gdp_growth_2026_pct"]["as_of"]}，創近 40 年新高），主因是 AI 供應鏈出口暴增，這股成長高度集中在單一產業鏈，'
        "不是台灣經濟的新常態基準。",
    ]
    return "".join(f"<li>{x}</li>" for x in items)


def build_scorecard(stats, facts):
    rows = [
        (f"母體市值總額（{stats['count']}檔）", twd_yi_from_raw(stats["total_mcap"]), SNAPSHOT_DATE,
         "本頁台股母體（TWSE＋TPEx，市值≥NT$100億）的合計市值", "母體快照（本頁自算）"),
        ("台積電佔母體市值", f'{stats["tsm_pop_pct"]:.2f}%', SNAPSHOT_DATE,
         "四個「台積電佔比」中分母最寬的一個，見§2論點A", "母體快照（本頁自算）"),
        (f'半導體業佔母體市值（{stats["semis_row"]["n"]}檔）', f'{stats["semis_row"]["pct"]:.2f}%', SNAPSHOT_DATE,
         "TWSE 官方33類產業別中最大的單一產業", "母體快照（本頁自算）"),
        ("電子業廣義佔母體市值", f'{stats["elec_pct"]:.2f}%', SNAPSHOT_DATE,
         "半導體＋電子零組件＋電腦週邊＋其他電子＋光電＋通信網路等9類合計", "母體快照（本頁自算）"),
        ("台積電佔加權指數權重", f'{facts["taiex_tsm_weight_pct"]["value"]:.2f}%', facts["taiex_tsm_weight_pct"]["as_of"],
         "分母是全部約1,068檔指數成分股，比母體口徑更集中", "taifex.com.tw官方"),
        ("台積電佔0050成分股權重", f'{facts["etf0050_tsm_weight_pct"]["value"]:.2f}%', facts["etf0050_tsm_weight_pct"]["as_of"],
         "分母僅50檔，是四個口徑中最集中的一個", "元大投信官方持股頁"),
        ("電子業廣義前瞻本益比中位數", f'{stats["pe_elec"]["median"]:.1f} 倍', SNAPSHOT_DATE,
         "與非電子業並列，才能看出估值分裂，見論點B", "母體快照（本頁自算）"),
        ("非電子業前瞻本益比中位數", f'{stats["pe_nonelec"]["median"]:.1f} 倍', SNAPSHOT_DATE,
         "低於電子業廣義中位數，但營收成長率也明顯較低", "母體快照（本頁自算）"),
        ("母體ROE中位數", f'{stats["roe_all_median"]:.1f}%', SNAPSHOT_DATE,
         "資本報酬整體水位，個別產業差異可達一倍以上，見論點C", "母體快照（本頁自算）"),
        ("殖利率≥6%檔數與中位數本益比", f'{stats["dy6_n"]}檔／{stats["dy6_pe_median"]:.2f}倍', SNAPSHOT_DATE,
         f'佔母體{stats["dy6_pct"]:.2f}%，本益比遠低於母體整體中位數{stats["all_pe_median"]:.2f}倍，市場自己在打折', "母體快照（本頁自算）"),
        ("三大高股息ETF合計規模", f'NT${(facts["etf_0056_snapshot"]["value"]["size_billion_twd"]+facts["etf_00878_snapshot"]["value"]["size_billion_twd"]+facts["etf_00919_snapshot"]["value"]["size_billion_twd"])/1000:.2f}兆',
         facts["etf_0056_snapshot"]["as_of"], "0056＋00878＋00919三檔合計，選股邏輯均為未來一年預測殖利率排序", "TWSE ETF e添富（集保結算所）"),
        ("外資持股比重", f'{facts["foreign_holding_share_pct"]["value"]}%', facts["foreign_holding_share_pct"]["as_of"],
         "外資是台股邊際定價的關鍵力量之一", "聯合新聞網轉引TWSE統計"),
        ("MSCI新興市場指數台灣權重", f'{facts["msci_tw_weight_announced_pct"]["value"]}%', facts["msci_tw_weight_announced_pct"]["as_of"],
         "台灣躍居該指數第一大市場，超越印度與中國", "中央社（轉引MSCI審核結果）"),
        ("台股ETF受益人數", f'{facts["tw_etf_holders_202608_count"]["value"]/10000:,.0f}萬人次', facts["tw_etf_holders_202608_count"]["as_of"],
         "94檔台股ETF逐檔加總的人次，同一人持有多檔會重複計算，不等於參與人數", "聯合新聞網轉引集保結算所統計"),
        ("當沖占大盤成交值比重（最新月）", f'{facts["daytrade_share_202608_pct"]["value"]}%', facts["daytrade_share_202608_pct"]["as_of"],
         "TWSE官方月度統計，2026年多數月份落在3–4成，8月已升破四成", "MoneyDJ理財網轉引TWSE官方統計"),
        ("加權指數本益比／股價淨值比", f'{facts["taiex_index_snapshot"]["value"]["pe_x"]:.2f}倍／{facts["taiex_index_snapshot"]["value"]["pb_x"]:.2f}倍',
         facts["taiex_index_snapshot"]["as_of"], "指數層級的加權本益比，與母體中位數屬不同算法，不可直接比較", "財報狗（彙整TWSE／公開資訊觀測站）"),
        ("2026年GDP成長率預測", f'{facts["gdp_growth_2026_pct"]["value"]}%', facts["gdp_growth_2026_pct"]["as_of"],
         "創近40年新高，但成長高度集中在AI供應鏈出口這一條產業鏈", "行政院主計總處官方新聞稿"),
    ]
    build_scorecard.row_count = len(rows)
    trs = []
    for label, val, asof, gloss, src in rows:
        trs.append(
            f'<tr><td class="lbl">{label}</td><td class="num strong">{val}</td>'
            f'<td class="num" style="color:var(--sec)">{asof}</td><td class="why">{gloss}</td>'
            f'<td class="why">{src}</td></tr>'
        )
    return "".join(trs)


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
        "A", "集中度：台積電一檔股票，四個分母都指向同一件事",
        "台積電不是台股裡最大的一檔股票，是台股本身——不管用哪一個分母衡量，它都拿走接近或超過三分之一的權重。",
        f'台積電佔加權指數權重 {facts["taiex_tsm_weight_pct"]["value"]:.2f}%'
        f'（as-of {facts["taiex_tsm_weight_pct"]["as_of"]}，taifex.com.tw 官方逐檔加總）。',
        [
            f'本頁 {stats["count"]} 檔母體依市值排序，台積電一檔即佔母體總市值 {stats["tsm_pop_pct"]:.2f}%；'
            f'前十檔合計 {conc[10]["pct"]:.2f}%；前五十檔合計 {conc[50]["pct"]:.2f}%'
            f'（{SNAPSHOT_DATE}快照，本頁自算——與 taifex 加權指數口徑不同分母，數字不完全相等但量級一致）。',
            f'拉近到 TWSE「半導體業」這個官方產業分類本身（{stats["semis_row"]["n"]}檔，佔母體市值 '
            f'{stats["semis_row"]["pct"]:.2f}%），台積電仍佔該分類市值的 {stats["tsm_semis_pct"]:.1f}%——'
            "中型股極少，半導體核心鏈在龍頭與小型股之間幾乎沒有中間層。",
            f'0050（元大台灣50）成分股僅 50 檔，台積電權重達 {facts["etf0050_tsm_weight_pct"]["value"]:.2f}%'
            f'（as-of {facts["etf0050_tsm_weight_pct"]["as_of"]}），第二名聯發科（2454）'
            f'{facts["etf0050_no2_weight_pct"]["value"]:.2f}%、第三名台達電（2308）'
            f'{facts["etf0050_no3_weight_pct"]["value"]:.2f}%——龍頭對第二名相差約 '
            f'{facts["etf0050_tsm_weight_pct"]["value"]/facts["etf0050_no2_weight_pct"]["value"]:.1f} 倍——'
            "「買0050分散風險」的直覺，在當前結構下相當程度上等同於單押台積電一檔。",
            f'反過來看尾巴：第 101 檔以後的 {stats["count"]-100} 檔股票（佔母體檔數 '
            f'{(stats["count"]-100)/stats["count"]*100:.1f}%）合計只分到 {conc["rest"]["pct"]:.2f}% 的市值。'
            "市值排序的前段與後段，不是同一個市場。",
        ],
        "任何以「加權指數」為名的判讀，若不先拆解台積電這一檔股票，本質上是在看一支個股的走勢圖，"
        f"不是在看 {stats['count']} 檔公司的平均表現。",
        [
            tile(f'{facts["taiex_tsm_weight_pct"]["value"]:.1f}%', "台積電佔加權指數權重"),
            tile(f'{facts["etf0050_tsm_weight_pct"]["value"]:.1f}%', "台積電佔0050成分股權重"),
            tile(f'{stats["tsm_pop_pct"]:.1f}%', "台積電佔母體市值（本頁自算）"),
        ],
        1, "母體市值集中度累積占比與TWSE產業分布",
        f"來源：本頁 {stats['count']} 檔母體快照，{SNAPSHOT_DATE}快照，依市值排序，本頁自算。",
        svg_exhibit_a(stats),
        "集中度不是新現象，是台股結構本身；真正該問的是分母是哪一個、集中在誰身上。",
    ))

    # B 兩種台股
    out.append(argument_card(
        "B", "兩種台股：電子與非電子被市場用價格分開對待",
        "台股不是一個估值水位的市場，而是電子與非電子兩群公司，被市場用完全不同的價格與成長預期看待。",
        f'電子業廣義（{stats["elec_n"]}檔）前瞻本益比中位數 {stats["pe_elec"]["median"]:.1f} 倍，'
        f'非電子業（{stats["nonelec_n"]}檔）僅 {stats["pe_nonelec"]["median"]:.1f} 倍'
        f'（{SNAPSHOT_DATE}快照，本頁自算）。',
        [
            f'成長端同樣分裂：電子業廣義營收成長率中位數 {stats["revg_elec"]:.1f}%，'
            f'非電子業僅 {stats["revg_nonelec"]:.1f}%——電子業的高本益比至少有更快的成長中位數撐著，'
            "不是純粹的敘事溢價。",
            f'AI 硬體代工鏈內部不是「結構 vs 量」兩極分化，而是三層光譜：結構層'
            f'（散熱／電源／PCB CCL／連接器／機殼，{stats["ai_struct_n"]}檔）毛利率中位數 '
            f'{stats["ai_struct_gm_median"]:.1f}%，網通交換器層（{stats["ai_network_n"]}檔）介於 '
            f'{stats["ai_network_gm_min"]:.1f}%–{stats["ai_network_gm_max"]:.1f}% 之間，'
            f'組裝層（ODM，{stats["ai_assembly_n"]}檔）僅 {stats["ai_assembly_gm_median"]:.1f}%——'
            f'結構層對組裝層約 {stats["ai_struct_gm_median"]/stats["ai_assembly_gm_median"]:.1f} 倍'
            "（數字回查鏡頭二子頁，本頁對同一批快照現算）。",
            "但「結構」不是永久標籤：健策（3653）原是 NVIDIA 獨家均熱片（貼在晶片上把熱導出的金屬片）供應商，"
            "2026 年 5 月客戶改掉單片式上蓋規格、單價從約 150 美元砍到約 50 美元後，站內 DD 裁決由「A｜核心候選」"
            "降為「B｜觀望」，護城河趨勢（競爭優勢是在變強還是變弱的方向判定）由升轉平——"
            "技術門檻極高的結構供應商，議價力仍非永久。",
            f'電子業廣義內部的估值分布同樣寬：第一四分位 {stats["pe_elec"]["q1"]:.1f} 倍、'
            f'第三四分位 {stats["pe_elec"]["q3"]:.1f} 倍，貴的一端比便宜一端高 '
            f'{(stats["pe_elec"]["q3"]/stats["pe_elec"]["q1"]-1)*100:.0f}%——把電子業當成單一族群討論，'
            "會蓋掉這個內部分裂。",
        ],
        "「便宜」或「昂貴」不是對台股整體下的單一判斷，電子與非電子是兩個不同的定價世界，"
        "AI硬體代工鏈內部又再分裂成三層——判讀任何個股估值前，先確認它屬於哪一群、哪一層。",
        [
            tile(f'{stats["pe_elec"]["median"]:.1f}倍 / {stats["pe_nonelec"]["median"]:.1f}倍', "電子業 vs 非電子業前瞻本益比中位數"),
            tile(f'{stats["revg_elec"]:.1f}% / {stats["revg_nonelec"]:.1f}%', "電子業 vs 非電子業營收成長率中位數"),
            tile(f'{stats["ai_struct_gm_median"]/stats["ai_assembly_gm_median"]:.1f}倍', "AI硬體結構層對組裝層毛利率倍數"),
        ],
        2, "前瞻本益比分布：電子業廣義 vs 非電子業＋AI硬體代工鏈毛利率三層",
        f"來源：本頁 {stats['count']} 檔母體快照，{SNAPSHOT_DATE}快照，本頁自算；橫線兩端為第一／第三四分位、圓點為中位數，排除缺值與非正值。",
        svg_exhibit_b(stats),
        "分裂的分界線不是「台股貴不貴」，是市場已經用價格把電子與非電子、結構與組裝分開對待——" "判讀任何個股前，先確認它屬於哪一群。",
    ))

    # C 資本報酬分布
    out.append(argument_card(
        "C", "資本報酬分布：671 檔篩到 8 檔複利，市佔地位不等於股東報酬",
        "同一個 TWSE 產業分類裡，上市與上櫃公司的 ROE 中位數落差可達一倍以上（光電業上市 6.6% 對上櫃 2.4%，"
        "兩組樣本各 27 檔與 6 檔）；市佔地位第一，不代表資本報酬也第一。",
        f'671 檔母體先用 ROE≥15%（非金融、市值≥NT$300億）量化篩出 153 檔，十年歷史查證後只剩 8 檔真複利'
        "——完整推理與逐檔查證見鏡頭三子頁。",
        [
            f'母體整體 ROE 中位數 {stats["roe_all_median"]:.1f}%（{SNAPSHOT_DATE}快照，本頁自算，'
            "中位數天然排除少數負股東權益的極端值）；但拆到前12大產業分類 × 上市／上櫃層級看，"
            "落差遠大於這個整體數字暗示的水準——樣本足夠的組別中，光電業上市 6.6% 對上櫃 2.4%、"
            "其他電子業上市 12.8% 對上櫃 22.1%，同一產業標籤底下的資本報酬完全不是同一回事"
            "（Exhibit 3 中樣本數少於 5 檔的組別已灰化標示，不納入比較）。",
            "16 檔「全球或區域市佔前三」隱形冠軍候選 ROE 中位數僅 9.15%，10 檔（62.5%）是個位數，"
            "且 ROE 最高的三檔（華城、新代、高力）恰好是市佔宣稱最弱或查無可溯源來源的一群——"
            "市佔壟斷程度與資本報酬率在這 16 檔裡沒有正相關（完整查證見鏡頭四子頁）。",
            "大立光（3008）是方法論陷阱的具體案例：市場公認的十年級複利股，因單一年度手機鏡頭需求疲弱、"
            "ROE 降至 13.3%，被單期快照量化門檻直接排除在 153 檔候選之外——任何只看一年 ROE 的篩選，"
            "都必須搭配歷史查證，否則會系統性錯過景氣逆風中的真複利股。",
        ],
        "「地位第一」是敘事，ROE 是驗算——同樣講「利基龍頭」的故事，資本報酬轉換率可以差到一倍以上，"
        "逐檔驗算比相信市佔敘事可靠。",
        [
            tile("153→8檔", "複利機器：量化篩通過數→十年查證後留存數"),
            tile("9.15%", "16檔隱形冠軍候選ROE中位數"),
            tile(f'{stats["roe_all_median"]:.1f}%', "母體ROE中位數（本頁自算）"),
        ],
        3, "ROE 中位數：TWSE 官方前12大產業別 × 上市／上櫃對照",
        f"來源：本頁 {stats['count']} 檔母體快照，{SNAPSHOT_DATE}快照，本頁自算；圖中數字為中位數，非平均數，用以天然排除極端值；樣本數少於 5 檔的組別（航運業上櫃 n=1、電子通路業上櫃 n=1、金融保險業上櫃 n=4、電機機械上櫃 n=4）已灰化並標註「樣本不足不可比」，不納入任何跨組比較。",
        svg_exhibit_c(stats),
        "市占地位是敘事，ROE 是驗算——本頁只回答「資本報酬轉換率是多少」，不回答「值不值得投資」，個股裁決一律走站內 DD。",
    ))

    # D 收息
    green_names = "電信三雄（中華電2412／台灣大3045／遠傳4904）、中保科（9917）、大台北瓦斯（9908）、億豐（8464）、亞泥（1102）"
    yellow_names = "遠雄（5522）、晶華（2707）、遠百（2903）、潤泰新（9945）"
    out.append(argument_card(
        "D", "收息：兩兆規模的高股息 ETF 之下，真收息判準是另一條篩查線",
        "高息排行榜和真正禁得起考驗的收息股，多數是兩批不同的名字——把「殖利率高」與「真的配得出來」混成同一條漏斗，會錯過本頁最重要的一批名字。",
        f'高息排行榜和真正禁得起考驗的收息股，多數是兩批不同的名字——本頁 {stats["count"]} 檔母體中殖利率'
        f'≥6% 者僅 {stats["dy6_n"]} 檔'
        f'（{stats["dy6_pct"]:.2f}%），這批高息名單的中位數本益比僅 {stats["dy6_pe_median"]:.2f} 倍，'
        f'遠低於母體整體中位數 {stats["all_pe_median"]:.2f} 倍。',
        [
            "但這只是第一條篩查線；第二條獨立線不限定殖利率，直接對全母體套用 FCF 覆蓋率×連續配息年資×"
            "本業現金流品質三判準，篩出 7 檔綠燈＋4 檔黃燈"
            "（完整篩查方法論見鏡頭七子頁）。",
            f"7 檔綠燈——{green_names}——其中電信三雄、中保科、大台北瓦斯、億豐五檔殖利率均低於 6%，"
            "代表真正禁得起考驗的收息股，多數不在高息排行榜前段。",
            f"4 檔黃燈邊界——{yellow_names}——共同特徵是連續配息年資雖長，但至少一項判準需保留"
            "（獲利波動、業外貢獻度、再投資壓力）。",
            "配息率超過 100% 不是自動警訊：電信三雄配息率已連續超過淨利 100%，但這是折舊攤銷推升 FCF 高於淨利的"
            "正常會計現象；判讀順序應是先看現金流量表覆蓋能力，再看損益表配息率是否合理。",
            f'三大高股息 ETF（0056＋00878＋00919）合計規模已逾 '
            f'NT${(facts["etf_0056_snapshot"]["value"]["size_billion_twd"]+facts["etf_00878_snapshot"]["value"]["size_billion_twd"]+facts["etf_00919_snapshot"]["value"]["size_billion_twd"])/1000:.2f}兆'
            f'（as-of {facts["etf_0056_snapshot"]["as_of"]}），三檔選股邏輯均為「未來一年預測殖利率排序」，'
            "這批資金本身正在扭曲殖利率排序的定價邏輯。",
        ],
        "資金結構層與個股篩選層必須分開判斷：資金結構層看的是這兩兆資金流向哪些股票，個股篩選層看的是現金流覆蓋"
        "能力而非配息率高低；把兩者混成同一條漏斗，會把真正的收息股藏在高息排行榜看不到的位置。",
        [
            tile(f'{stats["dy6_n"]}檔／{stats["dy6_pe_median"]:.1f}倍', "殖利率≥6%檔數／中位數本益比"),
            tile("7綠燈／4黃燈", "真收息三判準深查候選（不限殖利率）"),
            tile(f'NT${(facts["etf_0056_snapshot"]["value"]["size_billion_twd"]+facts["etf_00878_snapshot"]["value"]["size_billion_twd"]+facts["etf_00919_snapshot"]["value"]["size_billion_twd"])/1000:.2f}兆', "三大高股息ETF合計規模"),
        ],
        4, "母體殖利率分布與三大高股息ETF規模",
        f"來源：本頁 {stats['count']} 檔母體快照，{SNAPSHOT_DATE}快照，本頁自算；ETF規模 as-of {facts['etf_0056_snapshot']['as_of']}，來源TWSE ETF e添富。",
        svg_exhibit_d(stats, facts),
        "殖利率排行榜的排序邏輯只看「配了多少」，不看「配得出來嗎」；真收息判準必須反過來，先確認現金流量表的覆蓋能力。",
    ))

    # E 買盤結構
    out.append(argument_card(
        "E", "買盤結構：外資、被動基金與當沖共同定價台股",
        "外資、MSCI被動資金與當沖三股力量都不是「覺得便宜才買」的買盤，而是規則驅動或制度驅動的資金——這是判讀台股定價的結構性背景。",
        f'外資持股占大盤市值約 {facts["foreign_holding_share_pct"]["value"]}%'
        f'（as-of {facts["foreign_holding_share_pct"]["as_of"]}），是台股邊際定價的關鍵力量之一。',
        [
            f'2026 年外資累計賣超台股逾 NT$2.28 兆，但持股比重仍維持約 '
            f'{facts["foreign_holding_share_pct"]["value"]}%——賣超金額主要反映交易行為，而非部位結構性撤出。',
            f'MSCI 新興市場指數台灣權重從 2025 Q3 的 {facts["msci_tw_weight_2025q3_pct"]["value"]:.2f}% '
            f'一路攀升，2026-08-13 官方公布再從調整前的 '
            f'{facts["msci_tw_weight_pre_adjust_pct"]["value"]:.2f}% 調升至 '
            f'{facts["msci_tw_weight_announced_pct"]["value"]}%（2026-08-31收盤後生效），台灣躍居該指數第一大市場，超越印度與中國；'
            f'台積電單一個股佔該指數權重達 {facts["msci_tw_tsm_weight_pct"]["value"]}%——'
            "這是一批外生、非基本面驅動但金額真實可觀的被動資金，且集中在台積電一檔股票身上。",
            f'台股 ETF 受益人數 {facts["tw_etf_holders_202608_count"]["value"]/10000:,.0f} 萬'
            f'（as-of {facts["tw_etf_holders_202608_count"]["as_of"]}，94 檔台股 ETF 逐檔加總）；'
            "這個數字是「人次」不是「人」——同一人持有多檔會被重複計算，不能讀成 1,851 萬個投資人。"
            f'同一 94 檔口徑內，今年以來累計增加約 {facts["tw_etf_holders_2026ytd_add"]["value"]/10000:,.0f} 萬人次'
            f'（{facts["tw_etf_holders_2026ytd_add"]["as_of"]}），仍在擴張；更早期新聞常見的 72 檔口徑統計與此不可比，'
            "本頁不跨口徑換算成長倍數。",
            f'當沖占大盤成交值比重 2026 年多數月份落在 3–4 成之間'
            f'（1月{facts["daytrade_share_202601_pct"]["value"]}%、2月{facts["daytrade_share_202602_pct"]["value"]}%、'
            f'4月{facts["daytrade_share_202604_pct"]["value"]}%），'
            f'{facts["daytrade_share_202607_pct"]["as_of"]}升至{facts["daytrade_share_202607_pct"]["value"]}%、'
            f'{facts["daytrade_share_202608_pct"]["as_of"]}進一步升破四成達 '
            f'{facts["daytrade_share_202608_pct"]["value"]}%——TWSE 官方月度統計，非新聞轉引估計值。',
            "台股漲跌幅限制現行±10%（2015年由7%放寬而來，已維持11年未再調整），重大意外消息若真實價值調整幅度"
            "超過此限，價格發現會被迫跨越多個交易日以連續漲跌停完成，而非單日一次到位。",
        ],
        "外資、被動指數基金與當沖三股力量都不是「覺得便宜才買」的買盤，而是規則驅動或制度驅動的買盤，"
        "是判讀台股為什麼在特定結構下維持高檔、以及事件驅動股價反應時間軸時繞不開的結構性背景。",
        [
            tile(f'{facts["foreign_holding_share_pct"]["value"]}%', "外資持股占大盤市值比重"),
            tile(f'{facts["msci_tw_weight_announced_pct"]["value"]}%', "MSCI新興市場指數台灣權重"),
            tile(f'{facts["daytrade_share_202608_pct"]["value"]}%', "當沖占大盤成交值比重（最新月）"),
        ],
        5, "MSCI台灣權重時間序列與TWSE官方當沖占比月序列",
        "來源：中央社（MSCI權重）；MoneyDJ理財網轉引TWSE官方統計（當沖占比），詳細來源見計分卡與方法論。",
        svg_exhibit_e(facts),
        "被動買盤、外資與當沖都是判讀台股估值韌性與短期波動的結構性背景，但不代表個股不會因為基本面惡化而重估。",
    ))

    return "".join(out)


# ---------------------------------------------------------------------------
# 5. 八個投資鏡頭一覽表
# ---------------------------------------------------------------------------

LENS_ROWS = [
    dict(n=1, slug="semis", name="半導體核心鏈",
         q="龍頭之外，誰握有結構？",
         a="TWSE半導體業分類116檔佔母體市值55.6%，台積電一檔佔該分類70.7%；扣掉龍頭，仍有六個位置握有獨立長期結構"
           "（家登精密／力旺／創意電子／信驊／世芯-KY／日月光投控），但越靠近「結構最硬」估值倍數往往越高。",
         n_dd=4, n_win=3, gap="家登精密（3680）極紫外光（EUV）曝光機專用晶圓傳送盒全球市佔85%，站內完全無研究覆蓋，是本鏡頭最需優先深查的名字"),
    dict(n=2, slug="ai-hardware", name="AI硬體與電子代工",
         q="同一波AI資本支出，誰在賺結構、誰在賺量？",
         a="結構層（19檔）毛利率中位數約29%，組裝層（6檔）僅約6%，網通交換器層（4檔）自成介於兩者之間的第三層；"
           "但健策（3653）因客戶規格改款、單價從約150美元砍到約50美元（少掉三分之二），證明技術門檻極高不等於議價力可長期維持。",
         n_dd=6, n_win=5, gap="欣興（3037）高階IC載板（承載晶片、連接晶片與電路板的高階基板）產能稀缺定價權代表，537億元資本支出競賽是否稀釋自身議價力，站內尚無深查"),
    dict(n=3, slug="compounders", name="複利機器",
         q="誰的高ROE能穿越景氣循環？",
         a="671檔母體先用ROE≥15%量化篩出153檔，十年歷史查證後只剩8檔真複利；大立光因單一年度逆風被單期量化門檻直接排除，"
           "是本鏡頭最重要的方法論教訓。",
         n_dd=0, n_win=0, gap="寶雅（5904）本名單最強複利軌跡，尚無站內DD檢視展店空間還剩多少與同業競爭動態"),
    dict(n=4, slug="hidden-champions", name="隱形冠軍與利基製造",
         q="市佔地位第一，資本報酬也第一嗎？",
         a="16檔「全球或區域市佔前三」候選ROE中位數僅9.15%，10檔（62.5%）是個位數；中國同業侵蝕已從假設變成兌現數字"
           "——自行車、輪胎兩個消費終端的營收與獲利已明顯下滑，精密傳動、半導體耗材則靠技術門檻守住。",
         n_dd=0, n_win=0, gap="華城（1519）估值與當期財報落差本頁最大（股價淨值比約30倍，即股價是每股帳面淨值的30倍，同期營收卻年減10%），訂單能見度待深查"),
    dict(n=5, slug="domestic", name="內需與通路",
         q="展店速度遇上人口衰退，誰還能找到第二條成長來源？",
         a="台灣總人口連續31個月負成長；統一超（2912）靠菲律賓子公司做出雙萬店規模，寶雅（5904）靠店型結構優化"
           "把展店資本支出換成全母體級ROE，差異在「展店」與「展對店」。",
         n_dd=0, n_win=0, gap="晶華（2707）全頁營益率最高，高端內需與商務會展需求可持續性需站內DD深查"),
    dict(n=6, slug="financials", name="金融",
         q="金融股的高ROE是定價權還是槓桿撐出來的？",
         a="34檔金融保險業標的（佔母體市值7.5%）分壽險型／銀行型／證券型三條資本結構軸線，壽險業避險比率"
           "（壽險業用貨幣避險工具鎖定匯率風險的部位，占其外幣資產的比率）自2024年底"
           "66.39%連續下滑至2026年中42.89%（史上新低）；34檔站內目前零DD覆蓋。",
         n_dd=0, n_win=0, gap="富邦金（2881）、國泰金（2882）為母體最大兩檔金融股，站內均零覆蓋"),
    dict(n=7, slug="dividends", name="收息",
         q="高股息ETF吸走兩兆資金之後，哪些才是真收息股？",
         a="殖利率≥6%的高息名單與FCF覆蓋率×連續配息年資×本業現金流品質三判準篩出的7綠燈＋4黃燈，是兩條互不相干"
           "的篩查線；三大高股息ETF的兩兆資金本身正在扭曲殖利率排序的定價邏輯。",
         n_dd=0, n_win=0, gap="11檔深查候選（7綠4黃）站內均無DD報告，全數進入候選隊列"),
    dict(n=8, slug="assets-events", name="資產與事件",
         q="哪些資產股有真正的觸發器，哪些只是帳面便宜？",
         a="公開收購（TOB，收購方公開向全體股東出價買股）的制度門檻透明——取得5%以上須申報公告、50日內預定取得"
           "20%以上須採公開收購——但榮化、精誠、台紙三案顯示溢價高低完全取決於用哪一天股價當基準；"
           "15檔結構訊號候選，0份既有DD覆蓋，是站內研究空白區。",
         n_dd=0, n_win=0, gap="南港輪胎（2101）自身廠區都更已完工入帳，對泰豐輪胎土地標售的推動力仍卡在對方董事會"),
]


LENS_CN = {1: "鏡頭一", 2: "鏡頭二", 3: "鏡頭三", 4: "鏡頭四",
           5: "鏡頭五", 6: "鏡頭六", 7: "鏡頭七", 8: "鏡頭八"}


def lens_dd_coverage(n):
    """從 WATCH_EXISTING 的裁決日現算該鏡頭的 DD 檔數與 90 天複審窗內比例，不寫死。"""
    rows = [r for r in WATCH_EXISTING if r["lens"] == LENS_CN[n]]
    win = [r for r in rows if days_between(r["date"], DD_BASIS_DATE) <= 90]
    return len(rows), len(win)


def build_lens_table():
    trs = []
    for r in LENS_ROWS:
        r["n_dd"], r["n_win"] = lens_dd_coverage(r["n"])
        if r["n_dd"] > 0:
            cov = f'{r["n_dd"]} 檔／{r["n_win"]/r["n_dd"]*100:.1f}% 窗內'
        else:
            cov = "0 份既有DD"
        trs.append(
            f'<tr><td class="lbl"><a href="taiwan/{r["slug"]}.html">鏡頭{r["n"]}・{r["name"]}</a></td>'
            f'<td class="why">{r["q"]}</td><td class="why">{r["a"]}</td>'
            f'<td class="num" style="white-space:nowrap">{cov}</td><td class="why">{r["gap"]}</td></tr>'
        )
    return "".join(trs)


# ---------------------------------------------------------------------------
# 6. 可作戰名單：已有裁決（逐字抄 dd-meta dca_verdict／dca_role 或原始 verdict 欄位）
# ---------------------------------------------------------------------------

WATCH_EXISTING = [
    dict(t="2330", name="台積電", lens="鏡頭一", verdict="觀望｜追蹤", role="追蹤",
         wait="三個條件任一成立就重估為進場：整體組合透過指數部位持有的台積電曝險回落、本地股相對海外存託憑證"
              "（ADR，同一家公司在海外掛牌的憑證）的折價重新擴大到 20% 以上、或股價回到約 1,900 元的 104 週均線帶",
         dd="DD_2330TW_20260719.html", date="2026-07-19",
         extra="裁決寫「觀望」的理由是整體組合已重複押注同一檔，不是估值或基本面轉弱（標的評等仍為 A+）；"
               "同公司 ADR（代碼 TSM，2026-08-08）的裁決為「進場｜核心」，兩份檔案在決策層並不一致，"
               "引用時要標明看的是哪一份"),
    dict(t="2454", name="聯發科", lens="鏡頭一", verdict="觀望｜追蹤", role="追蹤",
         wait="等護城河趨勢從持平轉為加深",
         dd="DD_2454_20260711.html", date="2026-07-11", extra=""),
    dict(t="2317", name="鴻海", lens="鏡頭二", verdict="B｜觀望偏進場", role="觀望偏進場",
         wait="前瞻本益比落在過去五年區間的第 84 百分位（比過去五年裡 84% 的時間都貴），"
              "等股價回測約 213 元的季線再分批進場",
         dd="DD_2317_20260601.html", date="2026-06-01", extra=""),
    dict(t="2308", name="台達電", lens="鏡頭二", verdict="B｜觀望偏進場", role="觀望偏進場",
         wait="毛利率與獲利雖已上修，短中期報酬對風險比仍不划算，等股價回到布林通道中軌約 1,500 元，"
              "或法說會連兩季驗證 AI 相關營收佔比",
         dd="DD_2308TW_20260514.html", date="2026-05-14", extra="無同公司更新裁決佐證，複審優先順位較高"),
    dict(t="2327", name="國巨", lens="鏡頭二", verdict="B｜觀望", role="觀望",
         wait="四週漲逾一倍、動能極端過熱，等股價回測約 328 元或 235 元的均線帶，"
              "再加上第三季 AI 相關營收佔比達 16% 以上，才重新評估",
         dd="DD_2327_20260526.html", date="2026-05-26", extra=""),
    dict(t="3017", name="奇鋐", lens="鏡頭二", verdict="進場｜衛星", role="衛星",
         wait="等護城河趨勢從持平轉為加深", dd="DD_3017_20260711.html", date="2026-07-11", extra=""),
    dict(t="3231", name="緯創", lens="鏡頭二", verdict="B｜觀望偏進場", role="觀望偏進場",
         wait="等毛利率從 5.21% 回升、自由現金流由負轉正，並等股價回檔",
         dd="DD_3231_20260601.html", date="2026-06-01", extra=""),
    dict(t="3653", name="健策", lens="鏡頭二", verdict="觀望｜條件式衛星持倉", role="條件式衛星持倉",
         wait="等客戶新一代晶片的上蓋（覆蓋晶片、負責導熱的金屬蓋板）是否延續單片式設計，"
              "這決定單價腰斬是一次性還是常態",
         dd="DD_3653_20260703.html", date="2026-07-03", extra=""),
    dict(t="5274", name="信驊", lens="鏡頭一", verdict="觀望｜條件式核心持倉", role="條件式核心持倉",
         wait="前瞻本益比 87 倍、落在過去五年區間的第 88 百分位，估值極貴，等股價回檔或成長真正兌現",
         dd="DD_5274.TW_20260703.html", date="2026-07-03", extra=""),
    dict(t="8299", name="群聯", lens="鏡頭一", verdict="B｜觀察期", role="觀察期",
         wait="等記憶體超級循環是否已到頂，以及市場共識對 2027 年每股盈餘衰退 42% 的預估是否上修",
         dd="DD_8299.TW_20260601.html", date="2026-06-01", extra=""),
]

WATCH_CANDIDATES = [
    ("3680", "家登精密", "鏡頭一", "EUV曝光機專用晶圓傳送盒全球市佔85%，站內完全無研究覆蓋，本頁最需優先深查的名字"),
    ("3443", "創意電子", "鏡頭一", "台積電持股35%的唯一客製化晶片（ASIC，為單一客戶量身設計的專用晶片）戰略夥伴，商業模式與客戶集中度需專門查證"),
    ("3529", "力旺", "鏡頭一", "只賣設計專利授權、不自己生產的商業模式，定價權能撐多久、與先進製程微縮的連動需量化驗證"),
    ("6669", "緯穎", "鏡頭二", "AI硬體組裝層唯一無DD的高ROE（51.1%）個股，靠資產快速週轉撐出的高報酬能否持續待驗"),
    ("2383", "台光電", "鏡頭二", "電路板銅箔基板層毛利率最高個股之一，材料等級躍遷帶來的定價權待深查"),
    ("3037", "欣興", "鏡頭二", "高階IC載板產能稀缺性定價權代表，537億元資本支出競賽是否稀釋自身議價力"),
    ("5904", "寶雅", "鏡頭三", "本名單最強複利軌跡，尚無DD檢視展店空間還剩多少與同業競爭動態"),
    ("2395", "研華", "鏡頭三", "靠生態系品牌收溢價的複利型公司，站內尚無DD覆蓋工業電腦龍頭估值與物聯網的成長空間判斷"),
    ("8069", "元太", "鏡頭三", "真壟斷但需求上限未定的複雜案例，最需DD層級查證電子貨架標籤的普及速度與終端需求"),
    ("1519", "華城", "鏡頭四", "估值與當期財報落差本頁最大（股價淨值比約30倍，同期營收卻年減10%），訂單能見度待深查"),
    ("8255", "朋程", "鏡頭四", "教科書級隱形冠軍面臨電動車轉型的產品週期風險，高壓直流電源與AI伺服器電源的轉型進度待查"),
    ("1590", "亞德客-KY", "鏡頭四", "常見市佔敘事需訂正（全球前三→中國前二），基本面扎實適合完整DD釐清定位"),
    ("2912", "統一超", "鏡頭五", "雙萬店規模＋菲律賓第二成長曲線，海外子公司獨立財報貢獻比重未拆分"),
    ("2707", "晶華", "鏡頭五", "全頁營益率最高，高端內需與商務會展需求可持續性需DD深查"),
    ("2881", "富邦金", "鏡頭六", "站內零覆蓋；三線本業+資本利得混合案例，ROE品質拆解代表標的"),
    ("2882", "國泰金", "鏡頭六", "站內零覆蓋；保險業新會計準則（IFRS 17）上路時淨值衝擊最大，未來獲利能否平滑要看合約服務邊際餘額"),
    ("2412", "中華電", "鏡頭七", "配息率連兩年超過當年淨利100%，要驗證自由現金流是否覆蓋得住；5G資本支出周期對再投資空間的擠壓程度"),
    ("9917", "中保科", "鏡頭七", "智慧城市與AI防災轉型的資本支出擴大，是否擠壓現有高配息政策"),
    ("2101", "南港輪胎", "鏡頭八", "自身廠區都更已完工入帳＋對泰豐影響力，事件驅動＋資產雙重敘事"),
    ("1722", "台肥", "鏡頭八", "資產股，新竹D7-B已動工、高雄園區擱置無開發時程，觸發器判讀需要深查"),
]


def build_watchlist():
    trs = []
    for r in WATCH_EXISTING:
        extra = f'；{r["extra"]}' if r.get("extra") else ""
        trs.append(
            f'<tr><td class="lbl">{name_tag(r["name"], r["t"])}</td><td class="why lenscol">{r["lens"]}</td>'
            f'<td class="why"><b>{r["verdict"]}</b></td><td class="why">{r["wait"]}{extra}</td>'
            f'<td class="why ddcol"><a href="{DD_DOC_BASE}/{r["dd"]}">查看 DD</a></td></tr>'
        )
    for t, name, lens, reason in WATCH_CANDIDATES:
        trs.append(
            f'<tr><td class="lbl">{name_tag(name, t)}</td><td class="why lenscol">{lens}</td>'
            f'<td class="why" style="color:var(--warn);white-space:nowrap">無（站內零覆蓋）</td><td class="why">{reason}</td>'
            f'<td class="why ddcol">—</td></tr>'
        )
    return "".join(trs)


def build_dd_review_note():
    entries = []
    for r in WATCH_EXISTING:
        d = days_between(r["date"], DD_BASIS_DATE)
        entries.append((r, d))
    over = [(r, d) for r, d in entries if d > 90]
    lines = []
    for r, d in over:
        lines.append(f'{name_tag(r["name"], r["t"])}（裁決日{r["date"]}），截至{DD_BASIS_DATE}已滿{d}天，超過站內90天複審窗')
    return "；".join(lines)


# ---------------------------------------------------------------------------
# 7. 會推翻本頁判斷的證據
# ---------------------------------------------------------------------------

FALSIFIERS = [
    "若台積電佔加權指數權重從目前約41%降到30%以下，且不是因為指數大幅剔除其他大型電子股，代表指數集中度正在真正"
    "分散，論點A「台積電一檔股票決定台股」的框架就不再成立。",
    "若電子業廣義與非電子業的前瞻本益比中位數差距（目前為19.4倍對13.5倍，相差5.9個本益比單位）收斂到2個本益比"
    "單位以內，且營收成長率中位數也同步收斂，代表市場已經不再用電子／非電子這條線分開定價，論點B的框架需要重新檢視。",
    "若隱形冠軍候選的ROE中位數從9.15%回升到15%以上，且市佔地位與ROE排序轉為正相關，代表「地位不等於報酬」"
    "這個判讀已不再成立，論點C就需要換掉支撐案例。",
    "若真收息判準（FCF覆蓋率×連續配息年資×本業現金流品質）篩出的綠燈名單與殖利率≥6%的高息名單高度重疊"
    "（例如7成以上重複），代表「高息」與「真收息」已不再是兩批不同的名字，論點D的核心主張就會鬆動。",
    "若外資持股比重、MSCI台灣權重與台股ETF受益人數同時連續下滑，代表不看價格的結構性買盤正在系統性收縮，"
    "論點E就會鬆動。",
    "若116年（2027年）成長率的後續預測不降反升、明顯高於目前的6.04%，且上修來源不是AI供應鏈出口，"
    "代表台灣經濟成長已從單一產業鏈轉為多來源，本頁對「成長集中在AI這一條產業鏈」的判讀需要重新檢視。",
]


def build_falsifiers():
    return "".join(f'<div class="amber">{x}</div>' for x in FALSIFIERS)


# ---------------------------------------------------------------------------
# 8. 資料、方法與盲區
# ---------------------------------------------------------------------------


def build_methodology(stats, facts):
    return f'''
<b>母體怎麼建的</b>：範圍為臺灣證券交易所（TWSE，.TW）＋證券櫃檯買賣中心（TPEx／上櫃，.TWO）普通股，市值≥NT$100億。
股票清單來源TWSE ISIN一覽表，以ISIN CFI分類碼過濾（CFI=ESVUFR一般普通股），排除ETF/ETN、認購售權證、特別股、
存託憑證、債券；過濾後候選母體1,974檔（上市1,084／上櫃890），通過市值篩選最終 {stats["count"]} 檔
（上市{stats["n_twse"]}／上櫃{stats["n_tpex"]}），總市值約{twd_yi_from_raw(stats["total_mcap"])}，快照日期
{SNAPSHOT_DATE}。完整建構方法見本頁母體快照建構報告。<br><br>

<b>本頁範圍未涵蓋的軸線（誠實揭露，非查無資料，是規劃範圍未觸及）</b>：①興櫃股完全未涵蓋——TWSE ISIN頁的
上櫃分類不含興櫃（Emerging Stock Market）；②記憶體與測試鏈（南亞科／華邦電／群聯／鴻勁／旺矽，合計佔半導體
分類市值{stats["mem_chain_semis_pct"]:.2f}%、佔母體{stats["mem_chain_pop_pct"]:.2f}%）未獨立成鏡頭，其報酬來源是商品週期而非結構性定價權，與鏡頭一的問題設定不同軸；
③航運業（{stats["shipping_n"]}檔，佔母體{stats["shipping_pct"]:.2f}%）與塑膠工業（{stats["plastics_n"]}檔，佔母體{stats["plastics_pct"]:.2f}%，南亞（1303）市值NT$16,456億為母體第9大公司）
兩軸未設鏡頭，報酬來源分別為運價循環與油／乙烯價差循環，與八鏡頭的結構性提問不同軸，是刻意取捨不是遺漏；
④生技醫療業（{stats["biotech_n"]}檔，佔母體{stats["biotech_pct"]:.2f}%）市值佔比小，判為合理取捨；⑤軍工／無人機新板塊（漢翔／長榮航太／雷虎）屬
2026年政策驅動再定價題材，尚未查證，列為後續研究方向；⑥母體定義僅含台灣證交所與櫃買中心掛牌（代號後綴 .TW／.TWO），純海外掛牌台廠（如慧榮
SIMO、奇景HIMX，站內皆已有DD覆蓋）依定義不在母體之中。<br><br>

<b>數字的時效不一致，讀者要分開看</b>：母體數字統一為{SNAPSHOT_DATE}快照；台積電佔加權指數權重與0050權重分別
as-of {facts["taiex_tsm_weight_pct"]["as_of"]}與{facts["etf0050_tsm_weight_pct"]["as_of"]}；外資持股as-of
{facts["foreign_holding_share_pct"]["as_of"]}；MSCI權重{facts["msci_tw_weight_announced_pct"]["as_of"]}；
三大高股息ETF規模as-of {facts["etf_0056_snapshot"]["as_of"]}；當沖占比最新月為
{facts["daytrade_share_202608_pct"]["as_of"]}；壽險避險比率最新值as-of
{facts["life_insurer_hedge_ratio_202606_pct"]["as_of"]}；GDP成長率預測as-of
{facts["gdp_growth_2026_pct"]["as_of"]}。整頁不是同一個時間切面，引用時應標明各自的as-of。<br><br>

<b>台積電佔比的四個分母不可互換</b>：本頁論點A已並陳四個分母各異的「台積電佔比」——佔加權指數權重
{facts["taiex_tsm_weight_pct"]["value"]:.2f}%（分母為全部約1,068檔指數成分股）、佔0050成分股權重
{facts["etf0050_tsm_weight_pct"]["value"]:.2f}%（分母僅50檔）、佔本頁母體市值{stats["tsm_pop_pct"]:.2f}%
（分母為{stats["count"]}檔）、佔TWSE半導體業分類市值{stats["tsm_semis_pct"]:.1f}%（分母為
{stats["semis_row"]["n"]}檔）。四個數字分母遞減、口徑各自成立，並非矛盾，下游引用時務必標明是哪一個分母、
哪一個as-of日期，不要跨口徑直接比較。<br><br>

<b>殖利率≥6%的58檔與真收息7綠燈4黃燈是兩條獨立篩查線</b>：前者是對母體套用單一殖利率門檻的結果，後者是對
全母體套用FCF覆蓋率×連續配息年資×本業現金流品質三判準的結果，兩者的候選名單高度不重疊（見論點D）——引用
「台股收息股」時務必先確認是哪一條篩查線的產物。<br><br>

<b>台股ETF受益人數是人次、且口徑隨時間變動</b>：本頁引用的{facts["tw_etf_holders_202608_count"]["value"]/10000:,.0f}萬
（{facts["tw_etf_holders_202608_count"]["as_of"]}）為94檔台股ETF逐檔加總的受益人「人次」，同一人持有多檔會被重複計算，
不等於1,851萬個投資人；此口徑與較早期新聞引用的72檔或更窄口徑統計不完全可比，本頁不換算跨口徑的成長倍數，
只引用同一94檔口徑內的年初至今增量（約{facts["tw_etf_holders_2026ytd_add"]["value"]/10000:,.0f}萬人次）。<br><br>

<b>站內DD裁決的抄錄規則</b>：可作戰名單的裁決欄位逐字取自各檔DD的<code>dca_verdict</code>／<code>dca_role</code>
兩個欄位，同一家公司一律取日期最新的那一份；鴻海（2317）、台達電（2308）、國巨（2327）、緯創（3231）、
群聯（8299）五檔的最新DD仍是較早期的格式，沒有這兩個決策欄位，故其裁決欄改用該份DD的verdict／signal欄位
改寫為對等的裁決字樣，不改寫方向與強度。<b>台積電有兩份決策層並存且結論不同</b>：本地股最新DD（2026-07-19）為
「觀望｜追蹤」，理由是整體組合已透過指數部位重複持有同一檔，非估值或基本面轉弱；同公司海外存託憑證
（ADR，代碼TSM，2026-08-08）最新DD則為「進場｜核心」。本頁可作戰名單依代號取本地股那一份，兩份的差異已在該列
標明，下游引用務必說明看的是哪一份。台達電無同公司更新裁決佐證，複審優先順位較高。<br><br>

<b>已知缺口清單</b>：MSCI各季權重數字在不同轉引來源間可能存在小幅版本差異，本頁未逐一交叉核對所有歷史時點；
壽險業海外投資占比精確單一月份數字未能進一步查證，列中信心度；當沖占比部分月份（如5月）本次查證未查得
可溯源官方數字，圖表中略過該月份而非以插值填補。每筆結構數字的原始出處與查證日期已在計分卡與各論點卡標明。
'''


# ---------------------------------------------------------------------------
# 9. 排版：CJK／英文（含 ticker、數字）自動留白一格
# ---------------------------------------------------------------------------


def add_cjk_latin_spacing(text):
    text = re.sub(r"([一-鿿])([A-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9])([一-鿿])", r"\1 \2", text)
    return text


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

    title = "台股國家掃描：台積電一檔股票，其餘六百七十檔被拆成兩種定價 | InvestmQuest Research"
    description = (
        f"台股國家掃描研究記錄：TWSE＋TPEx市值≥NT$100億共{stats['count']}檔宇宙"
        f"（母體市值約{twd_yi_from_raw(stats['total_mcap'])}）。五個論點——集中度、兩種台股、資本報酬分布、"
        "收息兩條篩查線、買盤結構——加上八個投資鏡頭全景掃描與10份站內既有DD對帳。掃描是研究記錄，不是選股名單。"
    )

    conc = stats["conc"]
    masthead_h1 = "台積電一檔股票決定台股將近四成市值，其餘標的被市場拆成兩種定價"
    masthead_subt = (
        f'本頁是 {stats["count"]} 檔台股母體（TWSE 上市＋TPEx 上櫃〔掛牌門檻低於上市的第二板〕，'
        "市值≥NT$100億）的市場結構掃描：五個論點＋台股計分卡＋"
        "八個投資鏡頭全景結論，資料快照 " + SNAPSHOT_DATE + "，結構數字另附各自查證日期；本頁是研究記錄，不是投資建議，"
        "個股「值不值得投資」的裁決一律走站內 DD 統一裁決鏈。"
    )

    scorecard_html = build_scorecard(stats, facts)
    SCORECARD_N = build_scorecard.row_count

    body = []
    body.append('<div class="masthead"><div class="masthead-inner">')
    body.append('<div class="kicker">國家掃描 · 台灣</div>')
    body.append(f'<h1>{masthead_h1}</h1>')
    body.append(f'<div class="subt">{masthead_subt}</div>')
    body.append('<div class="rule"></div>')
    body.append(
        '<div class="meta">'
        f'<span><b>掃描日期</b>　{SNAPSHOT_DATE}（資料快照，非持續更新）</span>'
        f'<span><b>母體</b>　TWSE＋TPEx市值≥NT$100億，共 {stats["count"]:,} 檔（上市{stats["n_twse"]}／上櫃{stats["n_tpex"]}）</span>'
        f'<span><b>覆蓋</b>　{stats["count"]:,} 檔母體 × 五個論點＋八個投資鏡頭</span>'
        '</div>'
    )
    body.append(
        '<div class="nature">本頁性質聲明：描述器／研究紀錄，非投資建議。五個論點與八個鏡頭收斂出的是判讀框架與'
        '資料事實，不是一張「買這些」的名單；個股「值不值得投資」的裁決一律走 DD 統一裁決鏈。</div>'
    )
    body.append('</div></div>')

    body.append('<div class="wrap">')

    body.append('<div class="exec-wrap"><div class="exec-hd">一頁摘要</div><ol class="exec">')
    body.append(build_exec_summary(stats, facts))
    body.append('</ol></div>')

    body.append('<div class="kdstrip">')
    body.append(f'<div><div class="kl">母體規模（TWSE＋TPEx）</div><div class="kv">{stats["count"]:,} 檔</div></div>')
    body.append(f'<div><div class="kl">台積電佔加權指數權重</div><div class="kv">{facts["taiex_tsm_weight_pct"]["value"]:.1f}%</div></div>')
    body.append(f'<div><div class="kl">母體總市值</div><div class="kv">{twd_yi_from_raw(stats["total_mcap"])}</div></div>')
    body.append(f'<div><div class="kl">站內DD覆蓋（集中於鏡頭一、二）</div><div class="kv">10 份</div></div>')
    body.append(f'<div><div class="kl">外資持股／MSCI台灣權重</div><div class="kv">{facts["foreign_holding_share_pct"]["value"]}%／{facts["msci_tw_weight_announced_pct"]["value"]}%</div></div>')
    body.append('</div>')

    toc_items = [
        ("s1", f"台股計分卡：{SCORECARD_N} 個指標速覽"),
        ("s2", "五個論點：集中度、兩種台股、資本報酬分布、收息、買盤結構"),
        ("s3", "八個投資鏡頭一覽"),
        ("s4", "可作戰名單：已有裁決與零覆蓋候選"),
        ("s5", "會推翻本頁判斷的證據"),
        ("s6", "資料、方法與盲區"),
    ]
    body.append('<div class="toc"><div class="toc-hd">報告目錄</div><ol>')
    for i, (anchor, label) in enumerate(toc_items, 1):
        body.append(f'<li><a href="#{anchor}"><span class="n">§{i}</span>{label}</a></li>')
    body.append('</ol></div>')

    body.append(f'<div class="section" id="s1"><div class="section-hd"><div class="sec-eyebrow">Section I</div><h2>§1　台股計分卡：{SCORECARD_N} 個指標速覽</h2></div>')
    body.append('<div class="section-lead">母體算得出來的直接算，算不出來的查證後標明來源與查證日期；查不到的在「資料、方法與盲區」自陳，不沿用沒有出處的數字。</div>')
    body.append('<div class="exhibit scroll"><table><thead><tr><th>指標</th><th>數值</th><th>as-of</th><th>白話一句</th><th>來源</th></tr></thead><tbody>')
    body.append(scorecard_html)
    body.append('</tbody></table></div>')
    body.append('</div>')

    body.append('<div class="section" id="s2"><div class="section-hd"><div class="sec-eyebrow">Section II</div><h2>§2　五個論點：這個市場現在是什麼</h2></div>')
    body.append('<div class="section-lead">每個論點都是可以被推翻的具體主張，不是氣氛描述；推翻條件見§5。</div>')
    body.append(build_arguments(stats, facts))
    body.append('</div>')

    body.append('<div class="section" id="s3"><div class="section-hd"><div class="sec-eyebrow">Section III</div><h2>§3　八個投資鏡頭一覽</h2></div>')
    body.append('<div class="section-lead">結論濃縮自各鏡頭子頁的問題與答案節，數字回查子頁與母體檔案，不憑印象轉述；完整推理與逐檔對帳見各鏡頭子頁。</div>')
    body.append('<div class="exhibit scroll lenstable"><table><thead><tr><th>鏡頭</th><th>核心問題</th><th>一句結論</th><th>站內DD覆蓋</th><th>最大缺口</th></tr></thead><tbody>')
    body.append(build_lens_table())
    body.append('</tbody></table></div>')
    body.append(f'<div class="ex-sub" style="padding:0 4px">站內DD覆蓋盤點 as-of {DD_BASIS_DATE}（複審窗基準日，非本頁即時重算）；窗內比例＝90天內完成之裁決占該鏡頭DD總數。</div>')
    body.append('</div>')

    body.append('<div class="section" id="s4"><div class="section-hd"><div class="sec-eyebrow">Section IV</div><h2>§4　可作戰名單：已有裁決與零覆蓋候選</h2></div>')
    body.append('<div class="section-lead">站內裁決逐字取自各檔案的決策層欄位（dca_verdict／dca_role；早期格式的檔案沒有這兩欄，改用其 verdict／signal 欄位寫成對等的裁決字樣），同一家公司一律取日期最新的那一份，不改寫不總結；本頁不給買賣指令，個股「值不值得投資」一律點進DD查完整推理。</div>')
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
    body.append(build_methodology(stats, facts))
    body.append('</div></details>')
    body.append('</div>')

    body.append(
        '<div class="closing">本頁為掃描研究記錄（描述器），非選股名單、非買賣建議；個股「值不值得投資」的裁決一律走DD統一裁決鏈。</div>'
    )

    body.append('<div class="footlinks">')
    for r in LENS_ROWS:
        body.append(f'<a href="taiwan/{r["slug"]}.html">鏡頭{r["n"]}・{r["name"]}</a>')
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
# 11. 自檢：--check
# ---------------------------------------------------------------------------

# 「護城河」是既有的標準投資術語（DD 檔案的 moat 欄位即用此字），不列入禁用比喻。
BANNED_METAPHOR_WORDS = ["煞车", "煞車", "收費站", "水庫", "半壁江山", "斷層帶", "藏寶圖", "尋寶",
                          "鴻溝", "雙面刃", "硬幣兩面", "賽道", "像座", "彷彿", "宛如"]
BANNED_PROCESS_WORDS = ["sonnet", "Sonnet", "opus", "Opus", "agent", "Agent", "critic", "orchestrator",
                         "本輪", "上一版", "舊版", "重寫"]
BANNED_CROSS_MARKET_WORDS = ["美國", "美股", "S&P", "日本", "東證", "TOPIX", "馬來西亞", "Bursa", "KLCI",
                              "韓國", "Korea"]
BANNED_TRADE_CALL_WORDS = ["買進", "賣出", "加碼", "減碼", "停損", "目標價"]
BANNED_INTERNAL_FILENAMES = ["_universe.json", "_hub_facts.json", "_universe_report.md", "_structure_dossier.md",
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
    for w in BANNED_PROCESS_WORDS:
        if w in body_only:
            report(f"流程語氣詞「{w}」", [w] * body_only.count(w))

    for w in BANNED_CROSS_MARKET_WORDS:
        if w in body_only:
            report(f"跨市場字樣「{w}」", [w] * body_only.count(w))

    for w in BANNED_TRADE_CALL_WORDS:
        if w in body_only:
            report(f"買賣指令字樣「{w}」", [w] * body_only.count(w))

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

    lens_dir = os.path.join(BASE, "..", "..", "..", "..", "docs", "backtest", "country_scan", "taiwan")
    missing_pages = []
    for slug in re.findall(r'href="taiwan/([a-z-]+\.html)"', html):
        p = os.path.normpath(os.path.join(lens_dir, slug))
        if not os.path.exists(p):
            missing_pages.append(slug)
    report("子頁連結缺失（taiwan/前綴解析）", missing_pages)

    dd_dir_candidates = [os.path.join(BASE, "..", "..", "..", "..", "docs", "dd")]
    missing_dd = []
    for m in re.findall(r'DD_[A-Za-z0-9.\-]+\.html', html):
        found = any(os.path.exists(os.path.join(d, m)) for d in dd_dir_candidates)
        if not found:
            missing_dd.append(m)
    report("DD 連結檔案缺失（本機比對）", sorted(set(missing_dd)))

    stuck2 = re.findall(r"[一-鿿][A-Za-z0-9]|[A-Za-z0-9][一-鿿]", text_nodes.replace(" ", "\x01"))
    report("CJK 與英文/數字之間缺空格", stuck2)

    # 只數 Exhibit 標籤本身，內文提及「見 Exhibit 3」不計入連號檢查
    ex_nums = [int(x) for x in re.findall(r'<div class="ex-tag">Exhibit (\d+)</div>', html)]
    if ex_nums != sorted(set(ex_nums)) or ex_nums != list(range(1, len(set(ex_nums)) + 1)):
        problems.append(f"Exhibit 連號異常: {ex_nums}")

    facts = load_facts()
    uni = load_universe()
    stats = compute_population_stats(uni)
    plain = re.sub(r"<[^>]+>", "", body_only)

    for key in ("taiex_tsm_weight_pct", "etf0050_tsm_weight_pct", "foreign_holding_share_pct",
                "msci_tw_weight_announced_pct", "gdp_growth_2026_pct"):
        raw = facts[key]["value"]
        candidates = {str(raw)}
        if isinstance(raw, (int, float)):
            candidates.add(f"{raw:.2f}")
            candidates.add(f"{raw:.1f}")
        if not any(c in html for c in candidates):
            problems.append(f"facts[{key}].value={raw} 未出現在頁面內文中（試過 {sorted(candidates)}）")

    for key, e in facts.items():
        if key.startswith("_") or not isinstance(e, dict):
            continue
        if e.get("confidence") == "gap" or e.get("value") is None:
            continue
        if not e.get("source_url"):
            problems.append(f"facts[{key}] 有數值但缺 source_url")

    pop_checks = [
        (f'{stats["tsm_pop_pct"]:.2f}%', "台積電佔母體市值"),
        (f'{stats["semis_row"]["pct"]:.2f}%', "半導體業佔母體市值"),
        (f'{stats["elec_pct"]:.2f}%', "電子業廣義佔母體市值"),
        (f'{stats["pe_elec"]["median"]:.1f} 倍', "電子業前瞻本益比中位數"),
        (f'{stats["pe_nonelec"]["median"]:.1f} 倍', "非電子業前瞻本益比中位數"),
        (f'{stats["roe_all_median"]:.1f}%', "母體ROE中位數"),
        (f'{stats["dy6_n"]}檔', "殖利率≥6%檔數"),
        (twd_yi_from_raw(stats["total_mcap"]), "母體總市值"),
    ]
    for expect, label in pop_checks:
        if add_cjk_latin_spacing(expect) not in plain:
            problems.append(f"母體數字檢查失敗：{label} 應出現「{expect}」")

    # 同一家公司必須引用日期最新的 DD 檔（舊審稿 R9：漏掉更新裁決）
    dd_dir = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "docs", "dd"))
    if os.path.isdir(dd_dir):
        all_dd = os.listdir(dd_dir)
        for r in WATCH_EXISTING:
            pat = re.compile(r"^DD_%s(?:TW|\.TW)?_(\d{8})\.html$" % re.escape(r["t"]))
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

    dd_dd_total = len(WATCH_EXISTING)
    if f"{dd_dd_total} 份" not in plain and f"{dd_dd_total}份" not in plain:
        problems.append(f"站內DD總數 {dd_dd_total} 份與頁面敘述對不上")

    lens_candidate_total = sum(1 for _ in WATCH_CANDIDATES)
    if lens_candidate_total != 20:
        problems.append(f"候選隊列檔數應為20檔，實際{lens_candidate_total}檔")

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
            {k: v for k, v in stats.items() if k not in ("roe_rows", "industry_rows", "top_industries", "dy_hist")},
            ensure_ascii=False, indent=2, default=str,
        ))
    elif "--check-only" in sys.argv:
        run_check(OUT_PATH)
    else:
        main_cli()
