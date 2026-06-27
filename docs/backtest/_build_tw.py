"""Taiwan /backtest/tw/ overview — redesigned dashboard (muted palette).

Sibling of the US /backtest/ (rendered by _index_layout.py): same layout family
and palette, US/TW tab switch.  Sections: 波段(position) + 日內(intraday).
All numbers PINNED (NT$, ~2010-2026); E3 family/benchmarks sourced from
v7-backtest taiwan_lt, 0050 single-instrument + intraday systems from each page.

Run: python3 _build_tw.py
"""
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _nav_common import make_toggle

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("quant", "bt")
OUT = Path(__file__).parent / "tw" / "index.html"

GREEN, RED, GREY = "#16a34a", "#dc2626", "#9ca3af"

LIVE_CARD = {
    "name": "2330/0050 · E3", "tag": "✓ 實倉中",
    "sub": "50/50 2330/0050 · {W40·W52·TSMOM} 各⅓ · 美股長軌的台股鏡像 · 純 E3(ST 閘門否決)",
    "cagr": "+20.22%", "mdd": "-23.75%", "sharpe": "1.16", "calmar": "0.85",
    "url": "/backtest/long_track_tw/",
}

# 波段 systems: (name, url, sub, cagr, mdd, calmar, dom, status_tag, lane)
def tag_adopt():
    return '<span class="tag tag-best">✓ 實倉中</span>'
def tag_cand():
    return '<span class="tag">候補 · 未採用</span>'
def tag_fail():
    return '<span class="tag tag-fail">否決</span>'
def tag_bh():
    return '<span class="tag tag-bh">基準</span>'

SWING = [
    ("採用", GREEN, [
        ("2330/0050 三訊號趨勢集成（E3）", "/backtest/long_track_tw/",
         "50/50 2330/0050 · 過尺 Calmar 0.85 vs 稀釋B&H 0.60 · MDD 把大盤 -39.5% 砍到 -23.75%",
         "+20.22%", "-23.75%", "0.85", "有效交換", tag_adopt()),
    ]),
    ("0050 單檔趨勢候補", GREY, [
        ("0050 週線長軌趨勢（Ch12 W52/104/250）", "/backtest/tw_0050_lt/",
         "0050 單檔最強趨勢:贏 STX50/六狀態/雙軌風險調整 · 有 W250 暖身偏誤",
         "+14.39%", "-21.30%", "0.68", "0050 單檔最強", tag_cand()),
        ("0050 六狀態機（移植）", "/backtest/tw_0050_six/",
         "MA52 驅動 · 風險調整勝 B&H 但輸純長軌(SMH 攻擊腿缺席)",
         "+14.34%", "-26.68%", "0.54", "有效交換", tag_cand()),
        ("0050 週線進攻趨勢（STX50 移植）", "/backtest/tw_0050/",
         "升級在 0050 不複現:Ch12 binary > E3 > STX50(與美股相反)",
         "+12.56%", "-26.69%", "0.47", "混合", tag_cand()),
    ]),
    ("否決", RED, [
        ("0050 雙軌多空・日短軌＋週長軌", "/backtest/tw_0050_dual/",
         "被自己的純長軌支配:做空 0% 勝率、日線軌加劇 whipsaw(同美股 dual 結論)",
         "+12.17%", "-30.83%", "0.39", "被支配", tag_fail()),
    ]),
]
BH = [
    ("2330/0050 50/50 B&H", "+24.32%", "-39.47%", "0.62"),
    ("2330 台積電 B&H", "+30.18%", "-44.80%", "0.67"),
    ("0050 B&H(已修復分割)", "+18.13%", "-33.83%", "0.54"),
    ("^TWII 加權指數 B&H(價格指數)", "+12.42%", "-31.63%", "0.39"),
]

# 日內: (name, url, sub, market, status_html)
INTRADAY = [
    ("台指期日內趨勢", "/backtest/txf_intraday/",
     "小段趨勢當沖 · 2 觸發×2 出場+日型過濾 · 18 年 1 分 K", "MTX 小台 · 日盤不留倉",
     '<span class="tag tag-fail">未通過</span>', "毛利優勢僅 ~1 tick,1 tick 滑價全負"),
    ("台指期現基差偏向", "/backtest/txf_basis/",
     "基差極端 → 次日反向 · 18 年驗證", "MTX 小台 · 次日日盤",
     '<span class="tag tag-fail">否決</span>', "量測對齊後現行年代歸零(+0.3 點,t=0.04)"),
    ("台指籌碼日盤偏向", "/backtest/txf_chips/",
     "外資淨部位變化跟單 / 選擇權 PCR", "MTX 小台 · 次日日盤",
     '<span class="tag">Z2 否決 · Z1 觀察</span>', "外資跟單 +11.9 點(t=1.2)單調未達標,forward 確認中"),
    ("個股期橫斷面當沖", "/backtest/ssf_xsec/",
     "329 檔個股期 · 橫斷面選多空 · 14.4 年", "個股期近月 · open→close",
     '<span class="tag tag-fail">Phase 1 未過</span>', "鏡像日反轉 +0.13% 撞 0.15% 成本牆;Phase 1b 待 tick"),
]

SWEEP = [  # 2330 weight ladder (E3)
    ("0 / 100", "+14.85%", "-25.13%", "0.59"),
    ("25 / 75", "+17.58%", "-22.11%", "0.80"),
    ("50 / 50", "+20.22%", "-23.75%", "0.85"),
    ("75 / 25", "+22.77%", "-25.71%", "0.89"),
    ("100 / 0", "+25.21%", "-27.63%", "0.91"),
]

SCATTER = [
    ("2330/0050 E3(採用)", 23.75, 20.22, GREEN),
    ("0050 Ch12 長軌", 21.30, 14.39, "#64748b"),
    ("0050 六狀態", 26.68, 14.34, "#64748b"),
    ("0050 STX50", 26.69, 12.56, "#64748b"),
    ("0050 雙軌(否決)", 30.83, 12.17, RED),
    ("B&H 2330/0050", 39.47, 24.32, "#94a3b8"),
    ("B&H 0050", 33.83, 18.13, "#94a3b8"),
    ("B&H 2330", 44.80, 30.18, "#94a3b8"),
    ("B&H ^TWII", 31.63, 12.42, "#94a3b8"),
]


def swing_rows():
    out = ""
    for title, lc, items in SWING:
        out += (f'<tr><td colspan="6" style="background:#f8fafc;border-left:3px solid {lc};'
                f'font-size:.74rem;font-weight:700;color:#475569;text-transform:uppercase;'
                f'letter-spacing:.04em">{title}</td></tr>')
        for name, url, sub, cagr, mdd, cal, dom, tag in items:
            out += (f'<tr style="border-left:3px solid {lc}"><td><a href="{url}" style="font-weight:600">{name}</a>'
                    f'<div style="font-size:.72rem;color:var(--muted);margin-top:.15rem">{sub}</div></td>'
                    f'<td style="font-weight:700;color:var(--green)">{cagr}</td>'
                    f'<td style="color:var(--muted)">{mdd}</td><td>{cal}</td><td>{dom}</td><td>{tag}</td></tr>')
    out += (f'<tr><td colspan="6" style="background:#f8fafc;border-left:3px solid {GREY};'
            f'font-size:.74rem;font-weight:700;color:#475569;text-transform:uppercase">基準(B&amp;H · NT$)</td></tr>')
    for n, c, m, cl in BH:
        out += (f'<tr style="background:#fafbfc;border-left:3px solid {GREY}"><td>{n}</td>'
                f'<td>{c}</td><td style="color:var(--muted)">{m}</td><td>{cl}</td><td>—</td><td>{tag_bh()}</td></tr>')
    return out


def intraday_rows():
    out = ""
    for name, url, sub, mkt, tag, note in INTRADAY:
        out += (f'<tr><td><a href="{url}" style="font-weight:600">{name}</a>'
                f'<div style="font-size:.72rem;color:var(--muted);margin-top:.15rem">{sub}</div></td>'
                f'<td style="font-size:.78rem">{mkt}</td><td>{tag}</td>'
                f'<td style="font-size:.72rem;color:var(--muted)">{note}</td></tr>')
    return out


def sweep_rows():
    out = ""
    for w, c, m, cl in SWEEP:
        hl = ' style="background:var(--green-bg)"' if w == "50 / 50" else ""
        out += (f'<tr{hl}><td>{w}</td><td>{c}</td><td style="color:var(--muted)">{m}</td><td>{cl}</td></tr>')
    return out


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
  <a class="ac-link" href="{c['url']}">回測詳細頁 →</a> &nbsp;·&nbsp; <a href="/long-track-tw/" style="font-size:.82rem">即時訊號 →</a>
</div>
<div class="acard-note">
  <div class="acn-title">採用備註</div>
  <ul>
    <li>美股 06-13 加掛的 <b>ST 半倉出場閘門(STX50)在台股否決</b>(Calmar 0.83 輸稀釋 E3 0.85)。</li>
    <li>NT$ · 自 2010-07(0050 資料起點)· <b>2008 GFC 不在主樣本</b>。</li>
    <li>趨勢的抗崩盤價值見 <a href="/backtest/tw_crash/">含崩盤頁</a>(2000/2008 OOS)。</li>
  </ul>
</div>"""

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK, "%TOGGLE%": make_toggle("tw20y"),
        "%CARD%": card, "%SWING_ROWS%": swing_rows(), "%INTRADAY_ROWS%": intraday_rows(),
        "%SWEEP_ROWS%": sweep_rows(),
        "%JS_SCATTER%": json.dumps([dict(label=l, x=x, y=y, color=c) for l, x, y, c in SCATTER]),
        "%NOW%": datetime.now().strftime("%Y-%m-%d"),
    }.items():
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>台股量化回測總覽 | InvestMQuest Research</title>
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
.acard-note ul{list-style:none;font-size:.82rem;line-height:1.85}
.acard-note li{padding-left:.9rem;position:relative;margin-bottom:.2rem}
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
.note{background:#fafbfc;border:1px solid var(--border);border-left:3px solid var(--grey);border-radius:0 8px 8px 0;padding:.85rem 1.1rem;font-size:.84rem;color:var(--text);margin:1rem 0}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem;margin-bottom:1rem}
.chart-card h3{font-size:.92rem;font-weight:600;color:var(--ink);margin-bottom:.4rem}
.chart-sub{font-size:.76rem;color:var(--muted);margin-bottom:.5rem}
.chart-wrap{position:relative;width:100%;height:340px}
details{background:var(--card);border:1px solid var(--border);border-radius:10px;margin-bottom:.75rem}
details summary{padding:.85rem 1.2rem;font-weight:600;font-size:.9rem;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.5rem;color:var(--ink)}
details summary::before{content:'▸';color:var(--grey);transition:transform .15s}
details[open] summary::before{transform:rotate(90deg)}
details .d-body{padding:0 1.2rem 1.2rem;overflow-x:auto}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:820px){.live-wrap{grid-template-columns:1fr}table{font-size:.76rem}th,td{padding:.4rem .45rem}}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>台股量化回測總覽</h1>
  <div class="sub">2010–2026 · NT$ 含息 · 起始 $1M · 與美股不同市場/幣別,不直接同尺 · <a href="/backtest/criteria/">評估標準</a></div>
  <div class="tabs"><a href="/backtest/">🇺🇸 美股</a><a class="on" href="/backtest/tw/">🇹🇼 台股</a><a href="/backtest/multi/">🧩 多資產</a><a href="/backtest/leverage/">🔧 槓桿疊加</a></div>
</div></div>

<div class="container">

<!-- LIVE -->
<div class="section">
<h2 class="section-title">現役系統</h2>
<div class="section-sub">台股採用 2330/0050 E3 · <b>實倉中</b>。即時訊號見 <a href="/long-track-tw/">每日狀態頁</a>。</div>
<div class="live-wrap">%CARD%</div>
</div>

<!-- 波段 -->
<div class="section">
<h2 class="section-title">波段系統 · 風險調整排名</h2>
<div class="section-sub">左色帶:<span style="color:var(--green)">綠=採用</span> · 灰=候補 · <span style="color:var(--red)">紅=否決</span>。皆 ~2010–2026 NT$;E3/基準由 taiwan_lt 計算、0050 單檔系統釘自各頁。</div>
<div class="card">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Calmar</th><th>支配性</th><th>狀態</th></tr></thead>
<tbody>%SWING_ROWS%</tbody></table>
</div>
<div class="note"><b>誠實歸因:</b>E3 在 <b>0050 單檔</b>的 Calmar 只有 0.59,反輸 0050 Ch12 長軌的 0.68(與美股 E3&gt;Ch12 相反)。
E3 2330/0050 能到 0.85,<b>領先全來自加入 2330</b>(台積電集中度),不是 E3 規則本身更強 — 見下方 2330 權重梯。</div>
</div>

<!-- 日內 -->
<div class="section">
<h2 class="section-title">日內交易 · 台指期 / 個股期</h2>
<div class="section-sub">不同時間尺度(當沖),不與上方波段系統同尺。台指期五路日內訊號毛利多 &lt; 1 tick 成本;結構性出路在橫斷面。</div>
<div class="card">
<table><thead><tr><th>系統</th><th>標的 / 時段</th><th>狀態</th><th>說明</th></tr></thead>
<tbody>%INTRADAY_ROWS%</tbody></table>
</div>
</div>

<!-- crash meta -->
<div class="section">
<a class="acard-note" style="display:block" href="/backtest/tw_crash/">
  <div class="acn-title">🔬 結論驗證 — 趨勢的尾部保護(含崩盤 OOS)</div>
  <div style="font-size:.86rem;color:var(--text)">台股 2009+「B&amp;H 難敗」是樣本無崩盤的假象。把 2000(−66%)、2008(−58%)放進樣本零調參 OOS,
  趨勢把 MDD −60〜66% 砍到 −28〜44%、Calmar 全勝 B&amp;H → 採用趨勢的理由是<b>抗崩盤</b>。 <span style="color:var(--ink);font-weight:600">詳見 →</span></div>
</a>
</div>

<!-- CHARTS -->
<div class="section">
<h2 class="section-title">風險 vs 報酬</h2>
<div class="chart-card"><h3>MDD × CAGR</h3><div class="chart-sub">左上最佳 · 綠=趨勢系統 · 灰/紅=基準/否決</div><div class="chart-wrap"><canvas id="chart-scatter"></canvas></div></div>
</div>

<!-- 研究筆記 -->
<div class="section">
<h2 class="section-title">研究筆記</h2>
<a href="/backtest/tw_vcrash/" style="display:flex;gap:.75rem;align-items:center;background:var(--card);border:1px solid var(--border);border-left:3px solid #16a34a;border-radius:8px;padding:1rem 1.25rem;text-decoration:none;color:inherit">
  <span style="font-size:1.3rem">🛡️</span>
  <span style="flex:1"><span style="font-weight:600;color:#16a34a">突發 V 崩防禦 — 怎麼減少報酬損失,且過得了尺?</span><br><span style="font-size:.82rem;color:var(--muted)">在 E3(2330/0050)上實測全套防禦法 · 唯一過尺 = 黃金/長債分散腿(15–30%);put/加速出場/vol-target/collar 全失敗或砍上檔;純 USD 現金 Calmar 卡基準 = carry 才是關鍵</span></span>
  <span style="color:#16a34a">→</span>
</a>
<a href="/backtest/daily_vs_weekly_tw/" style="display:flex;gap:.75rem;align-items:center;background:var(--card);border:1px solid var(--border);border-left:3px solid #1a56db;border-radius:8px;padding:1rem 1.25rem;text-decoration:none;color:inherit;margin-top:.75rem">
  <span style="font-size:1.3rem">⏱️</span>
  <span style="flex:1"><span style="font-weight:600;color:#1a56db">日線 vs 週線長軌 · 0050</span><br><span style="font-size:.82rem;color:var(--muted)">長軌規則搬日線 D60/120/200 + 各種濾網/多空,過 matched-CAGR 尺 · 0050 週線 Calmar 0.90、0/24 過尺;台美同結論:週線 long-only 最優、盤整閘門反而有害、空單救不活</span></span>
  <span style="color:#1a56db">→</span>
</a>
</div>

<!-- DETAILS -->
<div class="section">
<h2 class="section-title">明細</h2>
<details><summary>E3 的領先從哪來:2330 權重梯</summary><div class="d-body">
<p style="font-size:.84rem;color:var(--muted);margin-bottom:.5rem">同 E3 規則,只改 2330/0050 權重。綠底 = 採用的 50/50。往 2330 加碼 = 放大台積電單一公司賭注。</p>
<table><thead><tr><th>2330 / 0050</th><th>CAGR</th><th>MDD</th><th>Calmar</th></tr></thead><tbody>%SWEEP_ROWS%</tbody></table>
</div></details>
</div>

</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 台股量化回測總覽 · 真實 yfinance(0050 已修復分割)· 生成 %NOW%</div></footer>

<script>
var SCATTER=%JS_SCATTER%;
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";Chart.defaults.font.size=11;
new Chart(document.getElementById('chart-scatter'),{type:'scatter',
 data:{datasets:SCATTER.map(function(p){return {label:p.label,data:[{x:p.x,y:p.y}],backgroundColor:p.color,pointRadius:6,pointHoverRadius:8}})},
 options:{responsive:true,maintainAspectRatio:false,
  plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.dataset.label+': MDD -'+c.parsed.x.toFixed(1)+'% / CAGR +'+c.parsed.y.toFixed(1)+'%'}}}},
  scales:{x:{title:{display:true,text:'Max Drawdown (%)'},reverse:true,grid:{color:'rgba(0,0,0,.05)'},ticks:{callback:function(v){return '-'+v+'%'}}},
   y:{title:{display:true,text:'CAGR (%)'},grid:{color:'rgba(0,0,0,.05)'},ticks:{callback:function(v){return '+'+v+'%'}}}}}});
</script>
</body></html>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
