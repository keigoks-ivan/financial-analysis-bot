"""Generator for the /backtest/10y/ overview page.

Same design as _build_index.py (20y overview): numbers are pinned here with
as-of dates, sourced from each system's generator output / overview_refresh.py
in the v7-backtest repo.  Charts reuse the yearly RET arrays from
_build_index.py, sliced to the last ~10 years.

Run: python3 _build_10y.py   (needs python 3.12+, see scripts/site_nav.py)
"""
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _nav_common import make_toggle
from _build_index import RET, TAG, yearly_cell

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("quant", "bt")
OUT = Path(__file__).parent / "10y" / "index.html"

YEARS_10 = list(range(2016, 2027))

# (name, url, key-in-RET-or-None, 10y: cagr, mdd, sharpe, calmar, final, 20y: cagr, mdd, tag)
# Refreshed 2026-06-12, data through 2026-06-11 (windows = trailing 10y from last date).
SYS = [
    ("SMH/QQQ 進攻趨勢(採用)", "/backtest/long_track_smh/", "smh",
     "+25.74%", "-20.04%", "1.31", "1.28", "$9.87M", "+13.84%", "-21.87%", TAG["adopt"]),
    ("QQQ+SMH 六狀態機・三態無 Grid", "/backtest/six_state/", "ch8",
     "+22.16%", "-28.48%", "1.11", "0.78", "$7.40M", "+14.66%", "-37.78%", TAG["atk"]),
    ("QQQ 六狀態機・五態＋Grid・實盤", "/backtest/six_state_v1r1/", "v1r1",
     "+14.51%", "-50.28%", "0.80", "0.29", "$15.94M", "+14.51%", "-50.28%", TAG["live"]),
    ("QQQ 純攻擊週線長軌趨勢", "/backtest/long_track_qqq/", "ch12q",
     "+18.81%", "-25.18%", "1.10", "0.75", "$5.60M", "+10.80%", "-25.37%", TAG["atk"]),
    ("SPY/QQQ 三訊號趨勢集成(合格候補)", "/backtest/long_track_ensemble/", "e3",
     "+16.35%", "-21.15%", "1.13", "0.77", "$4.54M", "+11.36%", "-21.15%", TAG["def"]),
    ("SPY/QQQ 週線長軌趨勢", "/backtest/long_track/", "ch12",
     "+15.53%", "-18.75%", "1.12", "0.83", "$4.23M", "+9.75%", "-20.08%", TAG["def"]),
    ("SPY/AGG 週線斜率擇時（防守）", "/backtest/slope_filter/", "w52",
     "+13.16%", "-20.52%", "1.01", "0.64", "$3.41M*", "+10.62%", "-22.13%", TAG["def"]),
    ("SPY/ACWX/AGG 雙動能月切換", "/backtest/gem/", "gem",
     "+9.88%", "-21.54%", "0.72", "0.46", "$2.60M*", "+8.63%", "-21.54%", TAG["def"]),
    ("SPY/QQQ 雙軌多空（否決）", "/backtest/dual_track/", "dual",
     "+9.26%", "-19.61%", "0.73", "0.47", "$2.42M", "+4.35%", "-38.72%", TAG["fail"]),
    ("SPY 週線 Supertrend（ATR 10×3）", "/backtest/supertrend/", None,
     "+11.86%", "-13.48%", "1.09", "0.88", "$3.06M", "+8.11%", "-17.77%", TAG["exp"]),
    ("SPY/QQQ RSI(2) 均值回歸（盤整）", "/backtest/rsi2_mr/", None,
     "+4.48%", "-14.31%", "0.71", "0.31", "$2.45M", "+4.48%", "-14.31%", TAG["exp"]),
]

MULTI = [
    ("🐢 商品/債/匯/股 唐奇安突破（55/20）", "/backtest/turtle/", None,
     "+6.52%", "-52.28%", "0.36", "0.12", "$1.88M",
     "+7.61%", "-52.28%", TAG["ma"]),
    ("📈 35 檔 ETF 跨資產趨勢（EMA＋突破）", "/backtest/clenow/", None,
     "+12.69%", "-39.25%", "0.65", "0.32", "$3.30M", "+12.32%", "-41.01%", TAG["ma"]),
]

BH = [
    ("QQQ Buy & Hold", "qqq", "+21.71%", "-35.12%", "0.99", "0.62", "$7.12M", "+15.88%", "-53.40%"),
    ("SPY Buy & Hold", "spy", "+15.35%", "-33.72%", "0.89", "0.46", "$4.17M", "+11.01%", "-55.19%"),
    ("50/50 SPY/QQQ B&H", None, "+18.60%", "-30.86%", "0.96", "0.60", "$5.50M", "+13.52%", "-53.66%"),
]

SCATTER = [
    ("SPY 週線 Supertrend", 13.48, 11.86, "#be185d"),
    ("SPY/QQQ 回歸", 14.31, 4.48, "#ca8a04"),
    ("🐢 唐奇安突破", 52.28, 6.52, "#0f766e"),
    ("SMH/QQQ 進攻", 20.04, 25.74, "#b45309"),
    ("QQQ+SMH 六狀態", 28.48, 22.16, "#d32f2f"),
    ("QQQ 六狀態實盤", 50.28, 14.51, "#b45309"),
    ("QQQ 長軌純攻", 25.18, 18.81, "#16a34a"),
    ("SPY/QQQ 集成", 21.15, 16.35, "#d97706"),
    ("SPY/QQQ 長軌", 18.75, 15.53, "#2e7d32"),
    ("SPY/AGG 斜率", 20.52, 13.16, "#0891b2"),
    ("雙動能", 21.54, 9.88, "#f57c00"),
    ("SPY/QQQ 雙軌", 19.61, 9.26, "#7c3aed"),
    ("📈 跨資產趨勢", 39.25, 12.69, "#6366f1"),
    ("QQQ B&H", 35.12, 21.71, "#1565c0"),
    ("SPY B&H", 33.72, 15.35, "#757575"),
]

YEARLY_COLS = [
    ("ch8", "QQQ+SMH 六狀態", "#d32f2f"),
    ("v1r1", "QQQ 六狀態實盤", "#b45309"),
    ("ch12", "SPY/QQQ 長軌", "#2e7d32"),
    ("ch12q", "QQQ 長軌純攻", "#16a34a"),
    ("e3", "SPY/QQQ 集成", "#d97706"),
    ("smh", "SMH/QQQ 進攻", "#b45309"),
    ("dual", "SPY/QQQ 雙軌", "#7c3aed"),
    ("gem", "雙動能", "#f57c00"),
    ("w52", "SPY/AGG 斜率", "#0891b2"),
    ("qqq", "QQQ B&H", "#1565c0"),
    ("spy", "SPY B&H", "#757575"),
]

OFFSET = YEARS_10[0] - 2006  # slice index into the 2006-based RET arrays


def pp(a: str, b: str) -> str:
    """a - b in percentage points with diff styling (positive = improvement)."""
    try:
        v = float(a.replace("%", "").replace("+", "")) - float(b.replace("%", "").replace("+", ""))
    except ValueError:
        return "<td>—</td>"
    cls = "diff-pos" if v >= 0 else "diff-neg"
    return f'<td class="{cls}">{v:+.2f}pp</td>'


WARN_20 = ('<span class="tag" style="background:var(--amber-bg);color:var(--amber-text);'
           'border:1px solid var(--amber-border);margin-left:.35rem">⚠ 可疑帶</span>')


def sys_row(name, url, _key, c10, m10, sh10, cal10, fin10, c20, m20, tag) -> str:
    try:
        warn = WARN_20 if float(c10.replace("%", "").replace("+", "")) > 20 else ""
    except ValueError:
        warn = ""
    return (f'<tr><td><strong><a href="{url}">{name}</a></strong></td>'
            f'<td style="font-weight:700;color:var(--green)">{c10}{warn}</td>'
            f'<td style="color:var(--red)">{m10}</td><td>{sh10}</td><td>{cal10}</td>'
            f'<td>{fin10}</td><td>{tag}</td></tr>')


def cmp_row(name, c20, c10, m20, m10) -> str:
    return (f"<tr><td>{name}</td><td>{c20}</td><td>{c10}</td>{pp(c10, c20)}"
            f"<td>{m20}</td><td>{m10}</td>{pp(m10, m20)}</tr>")


def render() -> str:
    rows = "".join(sys_row(*r) for r in SYS)
    rows += ('<tr><td colspan="7" style="background:#f0fdfa;font-size:.75rem;font-weight:600;'
             'color:#115e59;text-transform:uppercase;letter-spacing:.04em">多資產系統</td></tr>')
    rows += "".join(sys_row(*r) for r in MULTI)
    rows += ('<tr><td colspan="7" style="background:#ecfdf5;font-size:.75rem;font-weight:600;'
             'color:#065f46;text-transform:uppercase;letter-spacing:.04em">'
             '🇹🇼 台股(2330/0050 E3 已採用 · NT$ · 不同市場/幣別，僅參照)</td></tr>'
             '<tr><td><strong><a href="/backtest/long_track_tw/">2330/0050 E3（採用）</a></strong>'
             '<br><span style="font-size:.72rem;color:var(--muted)">50/50 · {W40·W52·TSMOM} 各⅓ · '
             '2026-06-23 實倉 · NT$ · 近 10 年(2016~) · 詳見 '
             '<a href="/backtest/tw/">台股總覽</a></span></td>'
             '<td style="font-weight:700;color:var(--green)">+26.63%</td>'
             '<td style="color:var(--red)">-23.75%</td><td>1.37</td><td>1.12</td><td>$19.0M</td>'
             '<td><span class="tag" style="background:#ecfdf5;color:#065f46;border:1px solid #a7f3d0">'
             '✓ 實倉 · NT$</span></td></tr>')
    rows += "".join(
        f'<tr style="background:#f9fafb"><td>{n}</td><td>{c}</td>'
        f'<td style="color:var(--red)">{m}</td><td>{s}</td><td>{cl}</td>'
        f'<td>{f}</td><td>{TAG["bh"]}</td></tr>'
        for n, _k, c, m, s, cl, f, _c20, _m20 in BH)

    cmp_rows = "".join(cmp_row(r[0], r[8], r[3], r[9], r[4]) for r in SYS + MULTI)
    cmp_rows += "".join(cmp_row(n, c20, c10, m20, m10)
                        for n, _k, c10, m10, _s, _cl, _f, c20, m20 in BH)

    yearly_head = "".join(f'<th style="color:{c}">{h}</th>' for _, h, c in YEARLY_COLS)
    yearly_rows = ""
    for i, y in enumerate(YEARS_10):
        cells = "".join(yearly_cell(RET[k][OFFSET + i]) for k, _, _ in YEARLY_COLS)
        yearly_rows += f"<tr><td>{y}</td>{cells}</tr>\n"

    ret10 = {k: v[OFFSET:] for k, v in RET.items()}
    js_ret = json.dumps(ret10)
    js_scatter = json.dumps([dict(label=l, x=x, y=y, color=c) for l, x, y, c in SCATTER])

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%TOGGLE%": make_toggle("10y"),
        "%ROWS%": rows,
        "%CMP_ROWS%": cmp_rows,
        "%YEARLY_HEAD%": yearly_head,
        "%YEARLY_ROWS%": yearly_rows,
        "%JS_RET%": js_ret,
        "%JS_SCATTER%": js_scatter,
        "%JS_YEARS%": json.dumps(YEARS_10),
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
<title>量化系統回測 — 10 年 | InvestMQuest Research</title>
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
.diff-pos{color:var(--green);font-weight:600}
.diff-neg{color:var(--red);font-weight:600}
.verdict{background:var(--brand-light);border-left:4px solid var(--brand);
         padding:1rem 1.4rem;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.9rem;line-height:1.7}
.verdict strong{color:var(--brand)}
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
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">量化回測</a> / 10 年</div>
    <h1>量化系統回測 — 10 年視角</h1>
    <div class="sub">近 10 年滾動窗口(2016-06 ~ 2026-06)· 「無 2008」的壓力對照窗 — 本頁的工作是偵測 regime 集中，不是排名；判定 = 與 <a href="/backtest/">20 年頁</a>取交集</div>
    %TOGGLE%
  </div>
</div>

<div class="container">

<div class="section">
<h2 class="section-title">配置對比總表(近 10 年)</h2>
<div class="section-sub">窗口 = 各系統最新數據日往回 10 年，起點重設 $1M。多資產系統使用不同資產池，僅供參考對照。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>10Y CAGR</th><th>10Y MDD</th><th>Sharpe</th><th>Calmar</th><th>期末資產</th><th></th></tr></thead>
<tbody>
%ROWS%
</tbody>
</table>
</div>

<div class="verdict">
  <strong>怎麼讀這一頁(2026-06 刷新):</strong>
  這個窗口沒有 2008,終點落在 AI/半導體多頭高點 — 所有數字都被窗口加持，
  <strong>每個 ⚠ 可疑帶(CAGR &gt; 20%)都是 regime 集中警報，不是慶祝理由</strong>。
  讀法上有三件事是訊號：
  (1) <strong>主動系統在此窗反超 B&amp;H</strong>(STX50 +25.74%、六狀態 +22.16% &gt; QQQ B&amp;H +21.71%,MDD 低 7~8pp)—
  與 20 年窗「讓報酬換回撤」的結論不同，正說明窗口與基準的選擇能改寫故事，所以判定取兩窗交集；
  (2) <strong>防守組的數字在兩窗一致</strong>(Long Track Calmar 0.83 / W52 0.64,審計 v2)— 一致性本身就是 regime 不集中的證據；
  (3) <strong>雙軌多空在最有利的窗口仍墊底</strong> — 被支配的判定對窗口穩健，否決不因窗口而改變。
</div>
</div>

<div class="section">
<h2 class="section-title">20 年 vs 10 年對比(regime 集中度檢查)</h2>
<div class="section-sub">差異欄：CAGR 正值 = 近 10 年更好；MDD 正值 = 近 10 年回撤更淺。CAGR 差異越大 = 績效越集中在「無 2008 的科技牛市」這一個 regime — 差異小的系統(W52 +2.5pp、GEM +1.2pp)對 regime 最穩健，差異 8pp+ 的系統(STX50、六狀態)是 regime 賭注，部位大小要按此打折。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>20Y CAGR</th><th>10Y CAGR</th><th>差異</th><th>20Y MDD</th><th>10Y MDD</th><th>差異</th></tr></thead>
<tbody>
%CMP_ROWS%
</tbody>
</table>
</div>
</div>

<div class="section">
<h2 class="section-title">淨值與風險對比(近 10 年)</h2>
<div class="chart-card">
  <h3>Growth of $1,000,000(2016 起)</h3>
  <div class="chart-sub">年頻淨值(對數座標)· 點圖例可隱藏線</div>
  <div class="chart-wrap"><canvas id="chart-nav"></canvas></div>
</div>
<div class="chart-card">
  <h3>Underwater Equity(年頻回撤)</h3>
  <div class="chart-sub">年底相對前高；精確 MDD 以總表為準(年頻會低估盤中深度)</div>
  <div class="chart-wrap-sm"><canvas id="chart-dd"></canvas></div>
</div>
<div class="chart-card">
  <h3>Risk vs Return(10 年)</h3>
  <div class="chart-sub">X = 10Y MDD (%) · Y = 10Y CAGR (%) · 左上為最佳象限</div>
  <div style="position:relative;width:100%;height:340px"><canvas id="chart-scatter"></canvas></div>
</div>
</div>

<div class="section">
<h2 class="section-title">明細</h2>
<details>
<summary>逐年報酬表(2016 ~ 2026)</summary>
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
  <li>全部美股系統：截至 2026-06,統一修正基準(warmup 自上市起算、閒置資金計 SHY/BIL 利息);
      W52 為 2026-06 審計引擎 v2(日線重建修正，10 年窗 CAGR +13.16% / MDD -20.52%)。</li>
  <li>10 年窗口 = 最新數據日往回 10 年(約 2016-06 起),起點重設 $1M;與 20 年頁的全期數字計算方式一致。</li>
  <li>* GEM 與 W52 斜率規格定義初始資金 $100,000;表中 $M 值為換算 $1M 起始的等效值。</li>
  <li>逐年報酬與圖表使用年頻資料；精確 MDD / Sharpe 以各系統詳頁計算為準。</li>
</ul>
</div>
</details>
</div>

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 量化回測 10 年視角 &middot; 真實 yfinance 資料 &middot; 頁面生成 %NOW% &middot; 僅供研究參考
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
  ['ch8','QQQ+SMH 六狀態機','#d32f2f',2,[]],
  ['v1r1','QQQ 六狀態機・實盤','#b45309',1.2,[3,3]],
  ['ch12','SPY/QQQ 長軌趨勢','#2e7d32',2.2,[]],
  ['ch12q','QQQ 長軌純攻','#16a34a',1.4,[]],
  ['e3','SPY/QQQ 集成(候補)','#d97706',1.4,[3,3]],
  ['smh','SMH/QQQ 進攻(採用)','#b45309',1.4,[3,3]],
  ['dual','SPY/QQQ 雙軌多空','#7c3aed',1.1,[3,3]],
  ['gem','雙動能月切換','#f57c00',1.2,[]],
  ['w52','SPY/AGG 斜率','#0891b2',1.2,[]],
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
    {label:'SPY/QQQ 長軌趨勢',data:toDD(toNAV(RET.ch12)),borderColor:'#2e7d32',backgroundColor:'rgba(46,125,50,0.10)',borderWidth:1.5,fill:'origin',pointRadius:0,tension:0.1},
    {label:'QQQ+SMH 六狀態機',data:toDD(toNAV(RET.ch8)),borderColor:'#d32f2f',backgroundColor:'rgba(211,47,47,0.06)',borderWidth:1.2,fill:'origin',pointRadius:0,tension:0.1},
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
    scales:{x:{title:{display:true,text:'10Y Max Drawdown (%)'},grid:{color:'rgba(0,0,0,0.05)'}},
      y:{title:{display:true,text:'10Y CAGR (%)'},grid:{color:'rgba(0,0,0,0.05)'}}}
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
