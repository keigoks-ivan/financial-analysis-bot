"""
Generator for the /backtest/ overview page (index.html).

Design: the overview is a comparison dashboard ONLY — summary table with
links to every sub-page, comparison charts, multi-window CAGR, yearly table,
and honest key findings.  Per-system deep dives live in the sub-pages; the
old hand-maintained tab sprawl duplicated them and rotted (stale numbers).

Numbers are pinned here with as-of dates, sourced from each system's own
generator output.  When a system page is regenerated with new numbers,
update SYSTEMS below and re-run:

    python3 _build_index.py
"""
from __future__ import annotations
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _nav_common import make_toggle

# Canonical site header (single source: scripts/site_nav.py)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("quant", "bt")

OUT = Path(__file__).parent / "index.html"

YEARS = list(range(2006, 2027))

# Yearly returns (%, within-year), 2006..2026 — drive all charts.
# ch12/ch12q corrected 2026-06 (warmup fix + cash yield); ch8/v1r1 corrected 2026-06.
RET = {
    "ch8":   [0.00, 14.90, -26.41, 33.68, 16.87, -8.11, 11.56, 30.17, 21.50, 4.58, 6.23, 31.52, -2.54, 33.64, 30.16, 31.09, -23.13, 41.41, 30.25, 23.58, 22.64],
    "v1r1":  [6.64, 18.51, -36.57, 45.24, 16.74, -6.96, 13.36, 30.79, 18.21, 6.18, 4.47, 29.96, -0.24, 30.56, 40.06, 26.57, -24.35, 52.35, 25.23, 21.45, 12.28],
    "ch12":  [4.20, 10.71, -5.38, 0.25, 7.89, -9.57, 8.62, 31.28, 17.36, -5.30, 3.47, 26.09, -1.53, 20.81, 26.54, 30.01, -13.53, 10.45, 26.74, 17.59, 5.85],
    "ch12q": [-1.67, 18.81, -9.74, 0.25, 6.73, -14.44, 6.88, 33.49, 20.12, -0.91, -0.43, 31.49, 4.65, 19.92, 39.23, 29.24, -17.22, 20.14, 27.74, 19.06, 8.86],
    "e3":    [5.12, 8.81, -4.68, 19.63, 7.95, -9.89, 10.26, 31.10, 16.53, -2.40, 3.91, 26.09, -1.56, 20.19, 25.20, 30.01, -13.62, 19.54, 26.74, 17.20, 6.84],
    "smh":   [1.16, 9.51, -4.16, 0.25, 3.66, -10.75, 2.55, 31.71, 25.92, -6.65, 9.82, 34.99, 3.79, 26.99, 42.99, 35.93, -19.73, 31.12, 36.33, 25.81, 29.46],
    "dual":  [None, None, None, None, 5.69, -19.27, 5.18, 29.62, 7.79, -18.49, -2.28, 25.48, 4.43, 1.62, 9.42, 18.27, -13.13, 12.22, 15.26, 6.23, -2.40],
    "gem":   [16.48, 9.48, -1.30, 6.35, 6.99, -0.85, 11.26, 28.45, 13.45, -7.52, 6.80, 20.17, -8.01, 18.02, 1.69, 24.11, -16.57, 5.84, 24.97, 13.33, 3.61],
    "w52":   [12.50, 4.96, 7.94, 3.12, 14.81, 0.04, 6.36, 32.53, 13.45, -4.03, 13.96, 21.80, -4.83, 18.02, 1.69, 28.82, -16.57, 19.51, 24.97, 9.70, -4.35],
    "qqq":   [6.93, 18.67, -41.73, 53.47, 19.22, 2.70, 16.82, 33.27, 19.18, 7.09, 5.89, 31.60, -1.04, 37.96, 47.58, 26.63, -32.58, 53.81, 28.73, 23.88, -3.50],
    "spy":   [13.81, 3.69, -36.81, 25.94, 12.78, 0.00, 13.47, 29.93, 11.39, -0.73, 9.54, 19.42, -6.24, 28.88, 16.26, 26.89, -19.44, 24.23, 23.31, 21.50, 1.20],
}

# Summary rows: (name, url, subtitle, cagr, mdd, sharpe, calmar, trades, final, tag_html, asof)
TAG = {
    "atk":  '<span class="tag" style="background:#dcfce7;color:#166534;border:1px solid #86efac">進攻</span>',
    "def":  '<span class="tag tag-best">防守</span>',
    "live": '<span class="tag" style="background:#fffbeb;color:#92400e;border:1px solid #fde68a">實盤 ⚠</span>',
    "exp":  '<span class="tag" style="background:#fffbeb;color:#92400e;border:1px solid #fde68a">🔬 實驗·未採用</span>',
    "adopt": '<span class="tag" style="background:#ecfdf5;color:#065f46;border:1px solid #a7f3d0">✓ 採用 · OOS</span>',
    "fail": '<span class="tag tag-fail">失敗</span>',
    "ma":   '<span class="tag" style="background:#f0fdfa;color:#115e59;border:1px solid #99f6e4">多資產</span>',
    "bh":   '<span class="tag tag-bh">基準</span>',
}

US_SYSTEMS = [
    ("六狀態機 v1.1", "/backtest/six_state/", "QQQ+SMH+BIL · 三狀態 · 無 Grid(2026-06 修正)",
     "+14.53%", "-35.80%", "0.85", "0.41", "85", "$16.00M", TAG["atk"]),
    ("六狀態機 v1.0r1 實盤", "/backtest/six_state_v1r1/", "QQQ+IB01 · 五狀態+Grid · 指數部閘門補做",
     "+14.41%", "-49.29%", "0.80", "0.29", "134", "$15.65M", TAG["live"]),
    ("Long Track Only", "/backtest/long_track/", "50/50 SPY/QQQ · W52/104/250(2026-06 warmup 修正)",
     "+9.59%", "-20.08%", "0.80", "0.48", "47", "$6.50M", TAG["def"]),
    ("LTO QQQ only", "/backtest/long_track_qqq/", "100% QQQ · Long Track 進攻變體(2026-06 修正)",
     "+10.63%", "-25.37%", "0.74", "0.42", "29", "$7.87M", TAG["atk"]),
    ("Ensemble 集成", "/backtest/long_track_ensemble/", "{W40·W52·TSMOM} 各⅓ 倉位 · 2026-06-11 採用",
     "+11.33%", "-21.15%", "0.88", "0.54", "—", "$8.97M", TAG["adopt"]),
    ("LT SMH/QQQ", "/backtest/long_track_smh/", "50/50 SMH/QQQ · 進攻位 · 2026-06-11 採用",
     "+13.88%", "-26.93%", "0.88", "0.52", "45", "$14.24M", TAG["adopt"]),
    ("雙軌多空", "/backtest/dual_track/", "50/50 SPY/QQQ · Short 70% + Long 30%(原始設計)",
     "+4.60%", "-26.83%", "0.42", "0.17", "210", "$2.00M", TAG["fail"]),
    ("GEM 雙動能", "/backtest/gem/", "SPY/ACWX/AGG 月度切換",
     "+8.49%", "-21.54%", "0.54", "0.39", "33", "$4.84M*", TAG["def"]),
    ("W52 斜率濾網", "/backtest/slope_filter/", "SPY/AGG 非對稱進出場",
     "+9.59%", "-20.05%", "0.89", "0.48", "17", "$6.19M", TAG["def"]),
    ("做空系統", "/backtest/short_system/", "指數做空 · 兩個獨立引擎均否決",
     "—", "—", "—", "—", "—", "—", TAG["fail"]),
]

MULTI_SYSTEMS = [
    ("🐢 Turtle System 2", "/backtest/turtle/", "USO/GLD/DBA/FXE/TLT/SPY · 55/20 突破",
     "+21.26%", "-37.16%", "0.71", "0.57", "572", "$38.89M", TAG["ma"]),
    ("📈 Clenow 趨勢", "/backtest/clenow/", "35 ETF × 7 類別 · EMA50/100 + 突破",
     "+13.67%", "-44.06%", "0.71", "0.31", "1118", "$14.73M", TAG["ma"]),
]

BH_ROWS = [
    ("QQQ Buy & Hold", "+14.90%", "-53.40%", "0.74", "0.28"),
    ("SPY Buy & Hold", "+10.50%", "-55.19%", "0.61", "0.19"),
    ("50/50 SPY/QQQ B&H", "+12.78%", "-53.66%", "0.70", "0.24"),
]

# 分期間 CAGR (全期 / 近15y / 近10y / 近5y)
PERIOD_CAGR = [
    ("六狀態機 v1.1", "#d32f2f", "+14.53%", "+17.93%", "+21.79%", "+20.44%"),
    ("v1.0r1 實盤", "#b45309", "+14.41%", "+17.35%", "+20.53%", "+17.55%"),
    ("Long Track", "#2e7d32", "+9.59%", "+12.04%", "+15.08%", "+11.55%"),
    ("LTO QQQ", "#16a34a", "+10.63%", "+13.90%", "+18.30%", "+13.82%"),
    ("Ensemble E3(採用)", "#d97706", "+11.33%", "+12.98%", "+15.90%", "+13.44%"),
    ("LT SMH/QQQ(採用)", "#b45309", "+13.88%", "+18.79%", "+25.90%", "+23.35%"),
    ("GEM", "#f57c00", "+7.81%", "+8.54%", "+7.87%", "+5.32%"),
    ("W52 斜率", "#0891b2", "+9.59%", "+10.21%", "+10.05%", "+6.43%"),
    ("QQQ B&H", "#1565c0", "+14.00%", "+17.53%", "+18.28%", "+9.80%"),
    ("SPY B&H", "#757575", "+9.00%", "+12.39%", "+12.44%", "+8.70%"),
]

SCATTER = [
    ("六狀態機 v1.1", 35.80, 14.53, "#d32f2f"),
    ("v1.0r1 實盤", 49.29, 14.41, "#b45309"),
    ("Long Track", 20.08, 9.59, "#2e7d32"),
    ("LTO QQQ", 25.37, 10.63, "#16a34a"),
    ("Ensemble E3", 21.15, 11.33, "#d97706"),
    ("LT SMH/QQQ", 26.93, 13.88, "#b45309"),
    ("雙軌多空", 26.83, 4.60, "#7c3aed"),
    ("GEM", 21.54, 8.49, "#f57c00"),
    ("W52 斜率", 20.05, 9.59, "#0891b2"),
    ("🐢 Turtle", 37.16, 21.26, "#0f766e"),
    ("📈 Clenow", 44.06, 13.67, "#6366f1"),
    ("QQQ B&H", 53.40, 14.90, "#1565c0"),
    ("SPY B&H", 55.19, 10.50, "#757575"),
]

YEARLY_COLS = [  # (key, header, color)
    ("ch8", "六狀態 v1.1", "#d32f2f"),
    ("v1r1", "v1.0r1", "#b45309"),
    ("ch12", "Long Track", "#2e7d32"),
    ("ch12q", "LTO QQQ", "#16a34a"),
    ("e3", "集成實驗", "#d97706"),
    ("smh", "LT SMH/QQQ", "#b45309"),
    ("dual", "雙軌多空", "#7c3aed"),
    ("gem", "GEM", "#f57c00"),
    ("w52", "W52", "#0891b2"),
    ("qqq", "QQQ B&H", "#1565c0"),
    ("spy", "SPY B&H", "#757575"),
]


def yearly_cell(v) -> str:
    if v is None:
        return "<td>—</td>"
    if v <= -10:
        return f'<td style="color:var(--red)">{v:+.2f}%</td>'
    if v >= 25:
        return f'<td style="color:var(--green);font-weight:600">{v:+.2f}%</td>'
    return f'<td>{v:+.2f}%</td>'


def sys_row(name, url, sub, cagr, mdd, sharpe, calmar, trades, final, tag) -> str:
    cagr_html = (f'<td style="font-weight:700;color:var(--green)">{cagr}</td>'
                 if cagr != "—" else "<td>—</td>")
    mdd_html = f'<td style="color:var(--red)">{mdd}</td>' if mdd != "—" else "<td>—</td>"
    return (f'<tr><td><strong><a href="{url}">{name}</a></strong><br>'
            f'<span style="font-size:.72rem;color:var(--muted)">{sub}</span></td>'
            f'{cagr_html}{mdd_html}<td>{sharpe}</td><td>{calmar}</td>'
            f'<td>{trades}</td><td>{final}</td><td>{tag}</td></tr>')


def render() -> str:
    rows = "".join(sys_row(*r) for r in US_SYSTEMS)
    rows += ('<tr><td colspan="8" style="background:#f0fdfa;font-size:.75rem;font-weight:600;'
             'color:#115e59;text-transform:uppercase;letter-spacing:.04em">多資產系統'
             '(不同資產池,僅供參考對照)</td></tr>')
    rows += "".join(sys_row(*r) for r in MULTI_SYSTEMS)
    rows += "".join(
        f'<tr style="background:#f9fafb"><td>{n}</td><td>{c}</td>'
        f'<td style="color:var(--red)">{m}</td><td>{s}</td><td>{cl}</td>'
        f'<td>—</td><td>—</td><td>{TAG["bh"]}</td></tr>'
        for n, c, m, s, cl in BH_ROWS)

    period_rows = "".join(
        f'<tr><td style="color:{color};font-weight:600">{name}</td>'
        f'<td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>'
        for name, color, a, b, c, d in PERIOD_CAGR)

    yearly_head = "".join(f'<th style="color:{c}">{h}</th>' for _, h, c in YEARLY_COLS)
    yearly_rows = ""
    for i, y in enumerate(YEARS):
        cells = "".join(yearly_cell(RET[k][i]) for k, _, _ in YEARLY_COLS)
        yearly_rows += f"<tr><td>{y}</td>{cells}</tr>\n"

    import json
    js_ret = json.dumps({k: v for k, v in RET.items()})
    js_scatter = json.dumps([dict(label=l, x=x, y=y, color=c) for l, x, y, c in SCATTER])

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%TOGGLE%": make_toggle("20y"),
        "%ROWS%": rows,
        "%PERIOD_ROWS%": period_rows,
        "%YEARLY_HEAD%": yearly_head,
        "%YEARLY_ROWS%": yearly_rows,
        "%JS_RET%": js_ret,
        "%JS_SCATTER%": js_scatter,
        "%JS_YEARS%": json.dumps(YEARS),
        "%NOW%": datetime.now().strftime("%Y-%m-%d"),
    }.items():
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>量化回測系統總覽 | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;
      --text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--red-text:#991b1b;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
     background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.75rem 0 1.25rem;background:linear-gradient(180deg,#f0f4ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.6rem;font-weight:700;letter-spacing:-.03em}
.page-hdr .sub{color:var(--muted);font-size:.9rem;margin-top:.2rem}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}
.crumb a{color:var(--muted)}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.15rem;font-weight:700;margin-bottom:1rem;
               padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.section-sub{font-size:.85rem;color:var(--muted);margin:-.5rem 0 1rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.card h3{font-size:1rem;font-weight:600;margin-bottom:.85rem}
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{text-align:left;padding:.6rem .75rem;border-bottom:1px solid var(--border)}
th{background:#f9fafb;font-weight:600;font-size:.78rem;text-transform:uppercase;
   letter-spacing:.04em;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
tbody tr:hover td{background:#f3f4f6}
.tag{display:inline-block;padding:.15rem .55rem;border-radius:4px;font-size:.72rem;font-weight:600;white-space:nowrap}
.tag-best{background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)}
.tag-fail{background:var(--red-bg);color:var(--red-text);border:1px solid var(--red-border)}
.tag-bh{background:#f3f4f6;color:#374151;border:1px solid #d1d5db}
.verdict{background:var(--brand-light);border-left:4px solid var(--brand);
         padding:1rem 1.4rem;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.9rem;line-height:1.7}
.verdict strong{color:var(--brand)}
.note{background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px;
      padding:.85rem 1.1rem;font-size:.84rem;color:var(--amber-text);margin:1rem 0}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.chart-card h3{font-size:.95rem;font-weight:600;margin-bottom:.5rem}
.chart-sub{font-size:.78rem;color:var(--muted);margin-bottom:.5rem}
.chart-wrap{position:relative;width:100%;height:420px}
.chart-wrap-sm{position:relative;width:100%;height:220px}
details{background:var(--card);border:1px solid var(--border);border-radius:8px;margin-bottom:.75rem}
details summary{padding:.9rem 1.25rem;font-weight:600;font-size:.95rem;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.5rem}
details summary::before{content:'▸';color:var(--brand);transition:transform .15s}
details[open] summary::before{transform:rotate(90deg)}
details .d-body{padding:0 1.25rem 1.25rem;overflow-x:auto}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);
       text-align:center;padding:1.25rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){table{font-size:.74rem}th,td{padding:.4rem .45rem}}
</style>
</head>
<body>
%NAV%

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
    <h1>量化回測系統總覽</h1>
    <div class="sub">20 年實證(2006 ~ 至今) · 真實 yfinance 資料 · 起始資金 $1,000,000 · 詳細分析見各系統頁</div>
    %TOGGLE%
  </div>
</div>

<div class="container">

<div class="section">
<h2 class="section-title">配置對比總表(20 年)</h2>
<div class="section-sub">點系統名稱進入詳頁。各系統數據截至日期見頁尾說明;多資產系統使用不同資產池,不與美股單資產系統直接比較。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar</th><th>交易</th><th>期末資產</th><th></th></tr></thead>
<tbody>
%ROWS%
</tbody>
</table>
</div>

<div class="verdict">
  <strong>定位一覽:</strong>
  <strong>六狀態機 v1.1</strong>是美股最高絕對報酬(+14.53%),代價 -35.8% MDD;
  <strong>Long Track Only</strong>(2026-06 warmup 修正後 +9.59% / -20.08% / Calmar 0.48)與
  <strong>W52 斜率</strong>(Sharpe 0.89)是防守雙雄;
  <strong>Ensemble E3</strong>(股票趨勢核心,Sharpe / Calmar 0.88 / 0.54)與
  <strong>LT SMH/QQQ</strong>(進攻位,+13.88% / -26.93%)於 2026-06-11 經系統擁有者決策採用,OOS 追蹤中(重審條件見各頁);
  <strong>雙軌多空與做空系統</strong>已被否決(指數做空在兩個獨立引擎中均失敗);
  <strong>Turtle / Clenow</strong> 的 alpha 來自商品/匯率/利率,與股票趨勢低相關,是組合層的互補件。
</div>

<div class="note">
  <strong>2026-06 方法論修正:</strong>Long Track 家族(50/50、QQQ only)與六狀態機完成 MA warmup 修正 —
  舊版資料自 2006 載入使 W250/D200 到 2010 年才有值,「20 年」實為 15.5 年且從首筆交易起算。
  修正後 Long Track 真實成績為 +9.59% / Calmar 0.48(舊頁 +10.95% / 0.55 已失效),
  LTO QQQ 為 +10.63% / 0.42(舊 +12.33% / 0.49)。詳見各頁「穩健性檢驗 ①」。
</div>
</div>

<div class="section">
<h2 class="section-title">淨值與風險對比</h2>
<div class="chart-card">
  <h3>Growth of $1,000,000</h3>
  <div class="chart-sub">年頻淨值(對數座標)· 2006–2026 · 點圖例可隱藏線</div>
  <div class="chart-wrap"><canvas id="chart-nav"></canvas></div>
</div>
<div class="chart-card">
  <h3>Underwater Equity(年頻回撤)</h3>
  <div class="chart-sub">年底相對前高;精確 MDD 以總表為準(年頻會低估盤中深度)</div>
  <div class="chart-wrap-sm"><canvas id="chart-dd"></canvas></div>
</div>
<div class="chart-card">
  <h3>Risk vs Return</h3>
  <div class="chart-sub">X = MDD (%) · Y = CAGR (%) · 左上為最佳象限</div>
  <div style="position:relative;width:100%;height:340px"><canvas id="chart-scatter"></canvas></div>
</div>
</div>

<div class="section">
<h2 class="section-title">分期間 CAGR 對比</h2>
<div class="section-sub">近 10 年所有主動系統都跑輸對應 Buy &amp; Hold — 這些系統買的是危機保險,不是牛市超額報酬。</div>
<div class="card">
<table>
<thead><tr><th>系統</th><th>全期</th><th>近 15 年</th><th>近 10 年</th><th>近 5 年</th></tr></thead>
<tbody>
%PERIOD_ROWS%
</tbody>
</table>
</div>
</div>

<div class="section">
<h2 class="section-title">明細</h2>
<details>
<summary>逐年報酬表(全系統)</summary>
<div class="d-body">
<table>
<thead><tr><th>Year</th>%YEARLY_HEAD%</tr></thead>
<tbody>
%YEARLY_ROWS%
</tbody>
</table>
</div>
</details>

<details>
<summary>數據截至日期與方法論說明</summary>
<div class="d-body">
<ul style="font-size:.85rem;color:#374151;line-height:1.9;padding-left:1.2rem">
  <li><strong>六狀態機 v1.1 / v1.0r1 / Long Track 家族(50/50、QQQ only、集成實驗、SMH 變體)</strong>:截至 2026-06-10,MA warmup 已修正(資料自 1999 載入、模擬自 2006-01 起算)、閒置資金計 SHY/BIL 利息。</li>
  <li><strong>雙軌多空 / GEM / W52 斜率 / 做空系統</strong>:截至 2026-04-09,尚未做 warmup 修正(雙軌的回測實際從 2010 起算)。</li>
  <li><strong>Turtle / Clenow</strong>:多資產系統,2005–2025,詳見各頁。</li>
  <li>* GEM 規格定義初始資金 $100,000,實際終值 $484K;表中 $4.84M 為換算 $1M 起始的等效值。</li>
  <li>逐年報酬與圖表使用年頻資料;精確 MDD / Sharpe 以各系統詳頁的日頻計算為準。</li>
</ul>
</div>
</details>
</div>

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 量化回測總覽 &middot; 真實 yfinance 資料 &middot; 頁面生成 %NOW% &middot; 僅供研究參考
  </div>
</footer>

<script>
var YEARS=%JS_YEARS%;
var RET=%JS_RET%;
var SCATTER=%JS_SCATTER%;

function toNAV(ret){
  var nav=[],v=1;
  for(var i=0;i<ret.length;i++){
    if(ret[i]===null){nav.push(null);continue}
    v=v*(1+ret[i]/100);nav.push(v);
  }
  return nav;
}
function toDD(nav){
  var dd=[],peak=0;
  for(var i=0;i<nav.length;i++){
    if(nav[i]===null){dd.push(null);continue}
    if(nav[i]>peak)peak=nav[i];
    dd.push((nav[i]/peak-1)*100);
  }
  return dd;
}
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;

var LINES=[
  ['ch8','六狀態機 v1.1','#d32f2f',2,[]],
  ['v1r1','v1.0r1 實盤','#b45309',1.2,[3,3]],
  ['ch12','Long Track','#2e7d32',2.2,[]],
  ['ch12q','LTO QQQ','#16a34a',1.4,[]],
  ['e3','Ensemble E3(採用)','#d97706',1.4,[3,3]],
  ['smh','LT SMH/QQQ(採用)','#b45309',1.4,[3,3]],
  ['dual','雙軌多空','#7c3aed',1.1,[3,3]],
  ['gem','GEM','#f57c00',1.2,[]],
  ['w52','W52 斜率','#0891b2',1.2,[]],
  ['qqq','QQQ B&H','#1565c0',1.4,[6,3]],
  ['spy','SPY B&H','#757575',1.4,[6,3]]
];

new Chart(document.getElementById('chart-nav'),{
  type:'line',
  data:{labels:YEARS.map(String),datasets:LINES.map(function(s){
    return {label:s[1],data:toNAV(RET[s[0]]),borderColor:s[2],borderWidth:s[3],
            borderDash:s[4],pointRadius:0,pointHoverRadius:4,tension:0.1,spanGaps:false};
  })},
  options:{responsive:true,maintainAspectRatio:false,
    interaction:{mode:'index',intersect:false},
    plugins:{legend:{display:true,position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'line',padding:12}},
      tooltip:{callbacks:{label:function(c){return c.parsed.y===null?null:c.dataset.label+': $'+c.parsed.y.toFixed(2)+'M'}}}},
    scales:{x:{grid:{color:'rgba(0,0,0,0.04)'},ticks:{font:{size:10}}},
      y:{type:'logarithmic',grid:{color:'rgba(0,0,0,0.06)'},ticks:{callback:function(v){return '$'+v+'M'},font:{size:10}}}}
  }
});

new Chart(document.getElementById('chart-dd'),{
  type:'line',
  data:{labels:YEARS.map(String),datasets:[
    {label:'Long Track',data:toDD(toNAV(RET.ch12)),borderColor:'#2e7d32',backgroundColor:'rgba(46,125,50,0.10)',borderWidth:1.5,fill:'origin',pointRadius:0,tension:0.1},
    {label:'六狀態機 v1.1',data:toDD(toNAV(RET.ch8)),borderColor:'#d32f2f',backgroundColor:'rgba(211,47,47,0.06)',borderWidth:1.2,fill:'origin',pointRadius:0,tension:0.1},
    {label:'QQQ B&H',data:toDD(toNAV(RET.qqq)),borderColor:'#1565c0',backgroundColor:'rgba(21,101,192,0.06)',borderWidth:1.2,fill:'origin',pointRadius:0,tension:0.1}
  ]},
  options:{responsive:true,maintainAspectRatio:false,
    interaction:{mode:'index',intersect:false},
    plugins:{legend:{display:true,position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'line',padding:10}},
      tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+c.parsed.y.toFixed(2)+'%'}}}},
    scales:{x:{grid:{display:false},ticks:{font:{size:10}}},
      y:{grid:{color:'rgba(0,0,0,0.06)'},ticks:{callback:function(v){return v+'%'},font:{size:10}}}}
  }
});

new Chart(document.getElementById('chart-scatter'),{
  type:'scatter',
  data:{datasets:SCATTER.map(function(p){
    return {label:p.label,data:[{x:p.x,y:p.y}],backgroundColor:p.color,pointRadius:7,pointHoverRadius:9};
  })},
  options:{responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:true,position:'right',labels:{usePointStyle:true,padding:8,font:{size:10}}},
      tooltip:{callbacks:{label:function(c){return c.dataset.label+': MDD '+c.parsed.x+'% / CAGR '+c.parsed.y+'%'}}}},
    scales:{x:{reverse:false,title:{display:true,text:'Max Drawdown (%)'},grid:{color:'rgba(0,0,0,0.05)'}},
      y:{title:{display:true,text:'CAGR (%)'},grid:{color:'rgba(0,0,0,0.05)'}}}
  }
});
</script>
</body>
</html>
"""


def main():
    html = render()
    OUT.write_text(html, encoding="utf-8")
    print(f"Written {OUT} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
