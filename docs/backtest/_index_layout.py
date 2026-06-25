"""DRAFT redesign of /backtest/ (US overview) — v2 preview, muted palette.

Renders docs/backtest/v2/index.html (does NOT touch the live page). Reuses
data from _build_index.py.  Design per owner feedback:
  * US-only page (TW split to /backtest/tw/).  Sections: 波段 + 多資產.
  * One live card only (SMH/QQQ STX50); SPY/QQQ E3 card removed.
  * Restrained palette: green=adopted/live, red=rejected, grey=everything else.
    No per-system rainbow; charts default to live + benchmarks.

Run: ~/.venvs/v7bt/bin/python3 _build_index_v2.py
"""
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _nav_common import make_toggle
import _build_index as idx

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("quant", "bt")
OUT = Path(__file__).parent / "index.html"

GREEN, RED, GREY = "#16a34a", "#dc2626", "#9ca3af"

# the single live card
LIVE_CARD = {
    "name": "SMH/QQQ · STX50", "tag": "✓ 實倉中",
    "sub": "50/50 SMH/QQQ · E3 三訊號 + 週線 ST(10,3) 半倉出場閘門 · 進攻位",
    "cagr": "+14.05%", "mdd": "-21.87%", "sharpe": "0.91", "calmar": "0.64",
    "url": "/backtest/long_track_smh/",
}


def lane(title):
    if "採用" in title:
        return GREEN
    if "否決" in title:
        return RED
    return GREY


def is_position(title):   # US 波段 (exclude multi-asset + TW)
    return "🇹🇼" not in title and "多資產" not in title


def slim_row(name, url, sub, cagr, mdd, sharpe, calmar, dom_key, final, tag, lc):
    cagr_h = (f'<td style="font-weight:700;color:var(--green)">{cagr}</td>' if cagr != "—" else "<td>—</td>")
    mdd_h = f'<td style="color:var(--muted)">{mdd}</td>' if mdd != "—" else "<td>—</td>"
    return (f'<tr style="border-left:3px solid {lc}"><td><a href="{url}" style="font-weight:600">{name}</a>'
            f'<div style="font-size:.72rem;color:var(--muted);margin-top:.15rem">{sub}</div></td>'
            f'{cagr_h}{mdd_h}<td>{calmar}</td><td>{idx.DOM[dom_key]}</td><td>{tag}</td></tr>')


def section_header(title, lc):
    return (f'<tr><td colspan="6" style="background:#f8fafc;border-left:3px solid {lc};'
            f'font-size:.74rem;font-weight:700;color:#475569;text-transform:uppercase;'
            f'letter-spacing:.04em">{title}</td></tr>')


def render():
    c = LIVE_CARD
    card = f"""<div class="acard">
  <div class="ac-tag">{c['tag']}</div>
  <div class="ac-name">{c['name']}</div>
  <div class="ac-sub">{c['sub']}</div>
  <div class="ac-metrics">
    <div><span>CAGR</span><b style="color:var(--green)">{c['cagr']}</b></div>
    <div><span>MDD</span><b>{c['mdd']}</b></div>
    <div><span>Sharpe</span><b>{c['sharpe']}</b></div>
    <div><span>Calmar</span><b>{c['calmar']}</b></div>
  </div>
  <a class="ac-link" href="{c['url']}">詳細頁 →</a>
</div>
<div class="acard-note">
  <div class="acn-title">其餘已採用 / 候補(未上實倉)</div>
  <ul>
    <li><a href="/backtest/long_track_ensemble/">SPY/QQQ E3 集成</a> — 合格候補(原列採用,未上實倉)· 核心防守</li>
    <li><a href="/backtest/slope_filter/">SPY/AGG 斜率</a> — 合格候補 · 全站唯一近支配(SPY 特定)</li>
  </ul>
</div>"""

    # 波段 table (position systems; experimental/rejected collapsed)
    main_rows, tail_rows = "", ""
    for title, items in idx.GROUPS:
        if not is_position(title):
            continue
        lc = lane(title)
        hdr = section_header(title, lc)
        body = "".join(slim_row(*r, lc) for r in items)
        if "實驗" in title or "否決" in title:
            tail_rows += hdr + body
        else:
            main_rows += hdr + body
    bh = "".join(
        f'<tr style="background:#fafbfc;border-left:3px solid {GREY}"><td>{n}</td><td>{c}</td>'
        f'<td style="color:var(--muted)">{m}</td><td>{cl}</td><td>—</td><td>{idx.TAG["bh"]}</td></tr>'
        for n, c, m, s, cl in idx.BH_ROWS)

    # 多資產 rows
    multi_rows = ""
    for title, items in idx.GROUPS:
        if "多資產" in title:
            multi_rows = "".join(slim_row(*r, GREY) for r in items)

    period = "".join(
        f'<tr><td style="font-weight:600">{name}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>'
        for name, _color, a, b, c, d in idx.PERIOD_CAGR)

    full_rows = ""
    for title, items in idx.GROUPS:
        full_rows += idx.group_header(title) + "".join(idx.sys_row(*r) for r in items)
    full_rows += idx.group_header("基準(Buy &amp; Hold)") + "".join(
        f'<tr style="background:#fafbfc"><td>{n}</td><td>{c}</td><td style="color:var(--muted)">{m}</td>'
        f'<td>{s}</td><td>{cl}</td><td>—</td><td>—</td><td>{idx.TAG["bh"]}</td></tr>'
        for n, c, m, s, cl in idx.BH_ROWS)

    yhead = "".join(f'<th>{h}</th>' for _, h, _c in idx.YEARLY_COLS)
    yrows = ""
    for i, y in enumerate(idx.YEARS):
        yrows += f"<tr><td>{y}</td>" + "".join(idx.yearly_cell(idx.RET[k][i]) for k, _, _ in idx.YEARLY_COLS) + "</tr>\n"

    # scatter recoloured by category (green adopted / grey bench&others / red rejected)
    def scat_color(label):
        if "進攻" in label or "集成" in label:
            return GREEN
        if "B&H" in label:
            return "#94a3b8"
        if "雙軌" in label or "做空" in label or "回歸" in label:
            return RED
        return "#64748b"
    scatter = [dict(label=l, x=x, y=y, color=scat_color(l)) for l, x, y, _c in idx.SCATTER]

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK, "%TOGGLE%": make_toggle("20y"),
        "%CARD%": card, "%MAIN_ROWS%": main_rows, "%TAIL_ROWS%": tail_rows, "%BH_ROWS%": bh,
        "%MULTI_ROWS%": multi_rows, "%PERIOD_ROWS%": period,
        "%FULL_ROWS%": full_rows, "%YEARLY_HEAD%": yhead, "%YEARLY_ROWS%": yrows,
        "%JS_RET%": json.dumps(idx.RET), "%JS_SCATTER%": json.dumps(scatter),
        "%JS_YEARS%": json.dumps(idx.YEARS), "%NOW%": datetime.now().strftime("%Y-%m-%d"),
    }.items():
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>美股量化回測總覽 | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--ink:#1f2937;--text:#374151;--muted:#6b7280;--border:#e5e7eb;--bg:#f7f8fa;--card:#fff;
      --green:#16a34a;--green-bg:#f0fdf4;--green-border:#bbf7d0;--red:#dc2626;--grey:#9ca3af}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;font-size:15px}
a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1080px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.5rem 0 1rem;background:#fff;border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.45rem;font-weight:800;letter-spacing:-.03em;color:var(--ink)}
.page-hdr .sub{color:var(--muted);font-size:.85rem;margin-top:.15rem}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}.crumb a{color:var(--muted)}
.draft{display:inline-block;background:#f3f4f6;color:#6b7280;border:1px solid var(--border);font-size:.72rem;font-weight:700;padding:.1rem .5rem;border-radius:4px;margin-left:.5rem}
.tabs{display:flex;gap:.4rem;margin-top:.9rem}
.tabs a{font-size:.86rem;font-weight:600;padding:.4rem .9rem;border:1px solid var(--border);border-radius:7px;color:var(--muted);background:#fff}
.tabs a.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.05rem;font-weight:700;color:var(--ink);margin-bottom:.85rem;padding-bottom:.4rem;border-bottom:1px solid var(--border)}
.section-sub{font-size:.82rem;color:var(--muted);margin:-.45rem 0 .9rem}
.live-wrap{display:grid;grid-template-columns:1.3fr 1fr;gap:1rem;margin-top:1rem}
.acard{background:var(--card);border:1px solid var(--green);border-radius:12px;padding:1.2rem 1.3rem;box-shadow:0 0 0 1px var(--green) inset}
.ac-tag{display:inline-block;font-size:.72rem;font-weight:700;padding:.2rem .6rem;border-radius:99px;margin-bottom:.5rem;background:var(--green);color:#fff}
.ac-name{font-size:1.3rem;font-weight:800;letter-spacing:-.02em;color:var(--ink)}
.ac-sub{font-size:.8rem;color:var(--muted);margin:.25rem 0 .9rem}
.ac-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin-bottom:.8rem}
.ac-metrics > div{text-align:center;background:#fafbfc;border:1px solid var(--border);border-radius:8px;padding:.5rem .3rem}
.ac-metrics span{display:block;font-size:.64rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.ac-metrics b{font-size:1.05rem;font-weight:800;color:var(--ink)}
.ac-link{font-size:.82rem;font-weight:600;color:var(--green)}
.acard-note{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.3rem}
.acn-title{font-size:.78rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:.6rem}
.acard-note ul{list-style:none;font-size:.84rem;line-height:1.9}
.acard-note li{padding-left:.9rem;position:relative}
.acard-note li::before{content:'·';position:absolute;left:0;color:var(--grey);font-weight:700}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.5rem;margin-bottom:1rem;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.86rem}
th,td{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}
th{background:#fafbfc;font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
tbody tr:hover td{background:#f6f8fb}
.tag{display:inline-block;padding:.13rem .5rem;border-radius:4px;font-size:.7rem;font-weight:600;white-space:nowrap;background:#f3f4f6;color:#475569;border:1px solid var(--border)}
.tag-best{background:var(--green-bg);color:#166534;border:1px solid var(--green-border)}
.tag-fail{background:#fef2f2;color:#991b1b;border:1px solid #fecaca}
.tag-bh{background:#f3f4f6;color:#6b7280;border:1px solid var(--border)}
.link-card{display:flex;align-items:center;gap:.75rem;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem;color:var(--ink)}
.link-card:hover{border-color:var(--ink);text-decoration:none}
.link-card .lc-name{font-weight:700;font-size:1rem}.link-card .lc-sub{font-size:.78rem;color:var(--muted)}.link-card .lc-arrow{margin-left:auto;color:var(--ink);font-weight:700}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem;margin-bottom:1rem}
.chart-card h3{font-size:.92rem;font-weight:600;color:var(--ink);margin-bottom:.4rem}
.chart-sub{font-size:.76rem;color:var(--muted);margin-bottom:.5rem}
.chart-wrap{position:relative;width:100%;height:330px}
.grid2{display:grid;grid-template-columns:3fr 2fr;gap:1rem}
details{background:var(--card);border:1px solid var(--border);border-radius:10px;margin-bottom:.75rem}
details summary{padding:.85rem 1.2rem;font-weight:600;font-size:.9rem;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.5rem;color:var(--ink)}
details summary::before{content:'▸';color:var(--grey);transition:transform .15s}
details[open] summary::before{transform:rotate(90deg)}
details .d-body{padding:0 1.2rem 1.2rem;overflow-x:auto}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:820px){.live-wrap{grid-template-columns:1fr}.grid2{grid-template-columns:1fr}table{font-size:.76rem}th,td{padding:.4rem .45rem}}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>美股量化回測總覽</h1>
  <div class="sub">20 年全週期(2006~,含 2008/2020/2022 三熊)· 真實 yfinance · 起始 $1M · <a href="/backtest/criteria/">評估標準</a></div>
  <div class="tabs"><a class="on" href="/backtest/">🇺🇸 美股</a><a href="/backtest/tw/">🇹🇼 台股</a></div>
</div></div>

<div class="container">

<div style="margin:1rem 0;padding:.7rem 1rem;background:#eef2ff;border:1px solid #c7d2fe;border-radius:8px;font-size:.86rem">
📖 看不懂 E3 / Ch12 / STX50 / VCP 這些代號?→ <a href="/backtest/glossary/" style="font-weight:700">術語對照表</a>
</div>

<!-- LIVE -->
<div class="section">
<h2 class="section-title">現役系統</h2>
<div class="section-sub">真正動到資金的只有「實倉中」這一個;其餘採用 / 候補列在右側,未上實倉。</div>
<div class="live-wrap">%CARD%</div>
</div>

<!-- 波段 -->
<div class="section">
<h2 class="section-title">波段系統 · 風險調整排名</h2>
<div class="section-sub">左色帶:<span style="color:var(--green)">綠=採用</span> · 灰=候補/角色可用 · <span style="color:var(--red)">紅=否決</span>。支配性 = 對自然基準的 <a href="/backtest/criteria/">L2 判定</a>。實驗/否決收在下方。</div>
<div class="card">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Calmar</th><th>支配性</th><th>狀態</th></tr></thead>
<tbody>%MAIN_ROWS%%BH_ROWS%</tbody></table>
</div>
<details><summary>實驗 / 已否決系統(收合)</summary><div class="d-body">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Calmar</th><th>支配性</th><th>狀態</th></tr></thead>
<tbody>%TAIL_ROWS%</tbody></table></div></details>
</div>

<!-- 多資產 -->
<div class="section">
<h2 class="section-title">多資產 · 跨資產趨勢</h2>
<div class="section-sub">不同資產池(商品/債/匯/股),與上方單一股票系統不同尺,僅供組合互補參照。</div>
<div class="card">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Calmar</th><th>支配性</th><th>狀態</th></tr></thead>
<tbody>%MULTI_ROWS%</tbody></table>
</div>
</div>

<!-- 研究 / 否決 -->
<div class="section">
<h2 class="section-title">研究筆記</h2>
<div class="section-sub">探索性研究頁(分散結構 / 反例),非實倉候選,刻意不列入上方比較表。</div>
<a class="link-card" href="/backtest/dual_track_study/" style="border-left:3px solid var(--green)">
  <span style="font-size:1.3rem">🧪</span>
  <span><span class="lc-name">雙軌分散研究 · 短MR + 長趨勢 on SMH/QQQ</span><br><span class="lc-sub">過尺 · 真實引擎(E3 長軌 + RSI2 短軌)· Calmar 0.65→0.70、MDD −27%→−18% · 兩條軸(時間架構/驅動)收斂到雙軌 = v7 Ch12 設計</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/minervini/" style="border-left:3px solid var(--red)">
  <span style="font-size:1.3rem">🔬</span>
  <span><span class="lc-name">Minervini RS+VCP 機械回測 ·《超級績效》</span><br><span class="lc-sub">否決 · 存活者偏誤樂觀上界,非忠實回測 · 即使偏誤灌水 CAGR 仍輸大盤;三槓桿(出場/進場/部位)皆推不開報酬↔回撤前緣 → alpha 在裁量、不可機械化</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/slope_filter_global/" style="border-left:3px solid #1a56db">
  <span style="font-size:1.3rem">🌍</span>
  <span><span class="lc-name">W52 斜率濾網 · 全球 15 國 ETF 穩健性</span><br><span class="lc-sub">穩健性地圖 · 同規則套 15 國指數 ETF · MDD 控制 15/15 普世(平均淺 +25.7pp)、CAGR 0/15 全輸 B&amp;H、Sharpe 9/15 只在乾淨週期市 · 換倉↔折損 corr −0.79(澳洲 41 次極端)、慢熊到處有效/急殺月度太慢</span></span>
  <span class="lc-arrow">→</span>
</a>
</div>

<!-- TW link -->
<div class="section">
<a class="link-card" href="/backtest/tw/">
  <span style="font-size:1.3rem">🇹🇼</span>
  <span><span class="lc-name">台股總覽</span><br><span class="lc-sub">2330/0050 E3 已採用 · 0050 四系統 · 台指期/個股期日內 · 含崩盤驗證</span></span>
  <span class="lc-arrow">→</span>
</a>
</div>

<!-- CHARTS -->
<div class="section">
<h2 class="section-title">淨值與風險</h2>
<div class="grid2">
  <div class="chart-card"><h3>Growth of $1M</h3><div class="chart-sub">年頻 · 對數座標 · 實倉系統 + B&amp;H</div><div class="chart-wrap"><canvas id="chart-nav"></canvas></div></div>
  <div class="chart-card"><h3>Risk vs Return</h3><div class="chart-sub">X=MDD · Y=CAGR · 左上最佳</div><div class="chart-wrap"><canvas id="chart-scatter"></canvas></div></div>
</div>
<div class="card" style="padding:1.1rem">
<h3 style="font-size:.92rem;margin-bottom:.6rem;color:var(--ink)">分期間 CAGR</h3>
<table><thead><tr><th>系統</th><th>全期</th><th>近 15 年</th><th>近 10 年</th><th>近 5 年</th></tr></thead><tbody>%PERIOD_ROWS%</tbody></table>
</div>
</div>

<!-- DETAILS -->
<div class="section">
<h2 class="section-title">明細</h2>
<details><summary>完整比較表(全系統 · 8 欄)</summary><div class="d-body">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar</th><th>支配性</th><th>期末</th><th>狀態</th></tr></thead>
<tbody>%FULL_ROWS%</tbody></table></div></details>
<details><summary>逐年報酬表(2006–2026)</summary><div class="d-body">
<table><thead><tr><th>Year</th>%YEARLY_HEAD%</tr></thead><tbody>%YEARLY_ROWS%</tbody></table></div></details>
</div>

</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 美股量化回測總覽 · 真實 yfinance · 生成 %NOW%</div></footer>

<script>
var YEARS=%JS_YEARS%,RET=%JS_RET%,SCATTER=%JS_SCATTER%;
function toNAV(r){var n=[],v=1;for(var i=0;i<r.length;i++){if(r[i]===null){n.push(null);continue}v*=1+r[i]/100;n.push(v)}return n}
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";Chart.defaults.font.size=11;
new Chart(document.getElementById('chart-nav'),{type:'line',
 data:{labels:YEARS.map(String),datasets:[
  {label:'SMH/QQQ STX50(實倉)',data:toNAV(RET.smh),borderColor:'#16a34a',borderWidth:2.4,pointRadius:0,tension:.1},
  {label:'QQQ B&H',data:toNAV(RET.qqq),borderColor:'#94a3b8',borderWidth:1.3,borderDash:[5,3],pointRadius:0,tension:.1},
  {label:'SPY B&H',data:toNAV(RET.spy),borderColor:'#cbd5e1',borderWidth:1.3,borderDash:[5,3],pointRadius:0,tension:.1}
 ]},
 options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
  plugins:{legend:{position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'line',padding:10,font:{size:10}}},
   tooltip:{callbacks:{label:function(c){return c.parsed.y===null?null:c.dataset.label+': $'+c.parsed.y.toFixed(2)+'M'}}}},
  scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}},y:{type:'logarithmic',grid:{color:'rgba(0,0,0,.06)'},ticks:{callback:function(v){return '$'+v+'M'},font:{size:10}}}}}});
new Chart(document.getElementById('chart-scatter'),{type:'scatter',
 data:{datasets:SCATTER.map(function(p){return {label:p.label,data:[{x:p.x,y:p.y}],backgroundColor:p.color,pointRadius:6,pointHoverRadius:8}})},
 options:{responsive:true,maintainAspectRatio:false,
  plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.dataset.label+': MDD '+c.parsed.x+'% / CAGR '+c.parsed.y+'%'}}}},
  scales:{x:{title:{display:true,text:'Max Drawdown (%)'},grid:{color:'rgba(0,0,0,.05)'}},y:{title:{display:true,text:'CAGR (%)'},grid:{color:'rgba(0,0,0,.05)'}}}}});
</script>
</body></html>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
