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
    ("LT SMH/QQQ E3(採用)", "/backtest/long_track_smh/", "smh",
     "+26.55%", "-26.93%", "1.23", "0.99", "$10.52M", "+15.30%", "-26.93%", TAG["adopt"]),
    ("六狀態機 v1.1", "/backtest/six_state/", "ch8",
     "+22.40%", "-28.49%", "1.12", "0.79", "$7.54M", "+14.77%", "-35.80%", TAG["atk"]),
    ("六狀態機 v1.0r1 實盤", "/backtest/six_state_v1r1/", "v1r1",
     "+21.02%", "-26.55%", "1.09", "0.79", "$6.73M", "+14.58%", "-49.29%", TAG["live"]),
    ("LTO QQQ only", "/backtest/long_track_qqq/", "ch12q",
     "+18.81%", "-25.18%", "1.10", "0.75", "$5.60M", "+10.80%", "-25.37%", TAG["atk"]),
    ("Ensemble 集成(採用)", "/backtest/long_track_ensemble/", "e3",
     "+16.29%", "-21.15%", "1.12", "0.77", "$4.52M", "+11.47%", "-21.15%", TAG["adopt"]),
    ("Long Track Only", "/backtest/long_track/", "ch12",
     "+15.47%", "-18.75%", "1.11", "0.83", "$4.21M", "+9.72%", "-20.08%", TAG["def"]),
    ("W52 斜率濾網", "/backtest/slope_filter/", "w52",
     "+11.04%", "-20.05%", "0.82", "0.55", "$2.87M*", "+10.16%", "-20.05%", TAG["def"]),
    ("GEM 雙動能", "/backtest/gem/", "gem",
     "+9.85%", "-21.54%", "0.54", "0.46", "$2.56M*", "+8.95%", "-21.54%", TAG["def"]),
    ("雙軌多空", "/backtest/dual_track/", "dual",
     "+9.26%", "-19.61%", "0.73", "0.47", "$2.42M", "+4.35%", "-38.72%", TAG["fail"]),
    ("週線 Supertrend (SPY)", "/backtest/supertrend/", None,
     "+11.86%", "-13.48%", "1.09", "0.88", "$3.06M", "+8.11%", "-17.77%", TAG["exp"]),
    ("盤整 MR (RSI2)", "/backtest/rsi2_mr/", None,
     "+3.29%", "-16.46%", "0.51", "0.20", "$1.38M", "+3.12%", "-16.46%", TAG["exp"]),
]

MULTI = [
    ("🐢 Turtle System 2", "/backtest/turtle/", None,
     "+24.13%", "-38.12%", "0.76", "0.63", "$8.67M",
     "+22.48%", "-38.12%", TAG["ma"]),
    ("📈 Clenow 趨勢", "/backtest/clenow/", None,
     "+13.16%", "-40.07%", "0.67", "0.33", "$3.44M", "+13.28%", "-44.11%", TAG["ma"]),
]

BH = [
    ("QQQ Buy & Hold", "qqq", "+21.71%", "-35.12%", "0.99", "0.62", "$7.12M", "+15.88%", "-53.40%"),
    ("SPY Buy & Hold", "spy", "+15.35%", "-33.72%", "0.89", "0.46", "$4.17M", "+11.01%", "-55.19%"),
    ("50/50 SPY/QQQ B&H", None, "+18.60%", "-30.86%", "0.96", "0.60", "$5.50M", "+13.52%", "-53.66%"),
]

SCATTER = [
    ("週線 ST (SPY)", 13.48, 11.86, "#be185d"),
    ("盤整 MR", 16.46, 3.29, "#ca8a04"),
    ("🐢 Turtle", 38.12, 24.13, "#0f766e"),
    ("LT SMH/QQQ E3", 26.93, 26.55, "#b45309"),
    ("六狀態機 v1.1", 28.49, 22.40, "#d32f2f"),
    ("v1.0r1 實盤", 26.55, 21.02, "#b45309"),
    ("LTO QQQ", 25.18, 18.81, "#16a34a"),
    ("Ensemble E3", 21.15, 16.29, "#d97706"),
    ("Long Track", 18.75, 15.47, "#2e7d32"),
    ("W52 斜率", 20.05, 11.04, "#0891b2"),
    ("GEM", 21.54, 9.85, "#f57c00"),
    ("雙軌多空", 19.61, 9.26, "#7c3aed"),
    ("📈 Clenow", 40.07, 13.16, "#6366f1"),
    ("QQQ B&H", 35.12, 21.71, "#1565c0"),
    ("SPY B&H", 33.72, 15.35, "#757575"),
]

YEARLY_COLS = [
    ("ch8", "六狀態 v1.1", "#d32f2f"),
    ("v1r1", "v1.0r1", "#b45309"),
    ("ch12", "Long Track", "#2e7d32"),
    ("ch12q", "LTO QQQ", "#16a34a"),
    ("e3", "Ensemble E3", "#d97706"),
    ("smh", "LT SMH/QQQ", "#b45309"),
    ("dual", "雙軌多空", "#7c3aed"),
    ("gem", "GEM", "#f57c00"),
    ("w52", "W52", "#0891b2"),
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


def sys_row(name, url, _key, c10, m10, sh10, cal10, fin10, c20, m20, tag) -> str:
    return (f'<tr><td><strong><a href="{url}">{name}</a></strong></td>'
            f'<td style="font-weight:700;color:var(--green)">{c10}</td>'
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
    <div class="sub">近 10 年滾動窗口(2016-06 ~ 2026-06)· 去除 2008 GFC 後的系統面貌 · 詳細分析見各系統頁</div>
    %TOGGLE%
  </div>
</div>

<div class="container">

<div class="section">
<h2 class="section-title">配置對比總表(近 10 年)</h2>
<div class="section-sub">窗口 = 各系統最新數據日往回 10 年,起點重設 $1M。多資產系統使用不同資產池,僅供參考對照。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>10Y CAGR</th><th>10Y MDD</th><th>Sharpe</th><th>Calmar</th><th>期末資產</th><th></th></tr></thead>
<tbody>
%ROWS%
</tbody>
</table>
</div>

<div class="verdict">
  <strong>10 年視角的結論(2026-06 刷新):</strong>
  去除 2008 後所有系統數字都變好,但排序也變了 —
  <strong>主動系統重新領先 B&amp;H</strong>:LT SMH/QQQ E3(+26.55%)、六狀態機(+22.40%)都超過 QQQ B&amp;H(+21.71%),
  且 MDD 低 7~8pp;這與前一版「近 10 年 B&amp;H 是最大贏家」的結論不同,主因是 2025-26 的 AI/半導體行情
  由趨勢系統滿倉吃到、而 QQQ B&amp;H 在 2022 的 -35% 拖累了它的 10 年窗口。
  <strong>防守組</strong>(Long Track +15.47% / -18.75%、Calmar 0.83)以一半的回撤拿到 SPY B&amp;H 的報酬。
  <strong>雙軌多空即使在最有利的 10 年窗口</strong>(無 2008 做空腿災難)仍墊底 — 否決不因窗口而改變。
</div>
</div>

<div class="section">
<h2 class="section-title">20 年 vs 10 年對比</h2>
<div class="section-sub">差異欄:CAGR 正值 = 近 10 年更好;MDD 正值 = 近 10 年回撤更淺。</div>
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
  <div class="chart-sub">年底相對前高;精確 MDD 以總表為準(年頻會低估盤中深度)</div>
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
  <li>全部美股系統:截至 2026-06-11,統一修正基準(warmup 自上市起算、閒置資金計 SHY/BIL 利息)。</li>
  <li>10 年窗口 = 最新數據日往回 10 年(約 2016-06 起),起點重設 $1M;與 20 年頁的全期數字計算方式一致。</li>
  <li>* GEM 與 W52 斜率規格定義初始資金 $100,000;表中 $M 值為換算 $1M 起始的等效值。</li>
  <li>逐年報酬與圖表使用年頻資料;精確 MDD / Sharpe 以各系統詳頁計算為準。</li>
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
