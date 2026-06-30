"""Leverage-overlay /backtest/leverage/ overview — dashboard (muted palette).

Sibling of 美股 (_index_layout.py) / 台股 (_build_tw.py) / 多資產 (_build_multi.py):
same layout family + palette, 5-tab market switch. This page documents the
FUTURES-LEVERAGE research on the adopted STX50 stock core — whether MNQ futures
can lever it toward 1.8x and improve RISK-ADJUSTED return. Because the adopted
method (adaptive vol-target) is new to the owner, the page leads with a detailed
METHOD section (formula + worked examples + why it works), then the evidence.

Numbers PINNED from v7-backtest src/long_track_backtest/stx50_mnq_overlay.py
(commit a6cdbc7). Re-run: python3 _build_leverage.py
"""
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("quant", "bt")
OUT = Path(__file__).parent / "leverage" / "index.html"
CURVES = json.loads((OUT.parent / "_curves.json").read_text())  # monthly NAV+DD, pinned from v7 backtest

ADOPT, GREY, RED = "#b45309", "#9ca3af", "#dc2626"

# (name, sub, cagr, mdd, sharpe, calmar full/06-15/15-now, tag) — PINNED
ROWS = [
    ("✓ 唯一過關", ADOPT, [
        ("vol-target 疊加（MNQ 槓 QQQ 半邊，+0.4x）", "/backtest/leverage/",
         "依最近波動連續縮放槓桿 · 三個年代 Calmar 都小贏底倉、Sharpe 升、尾部不放大",
         "+15.4%", "-23.3%", "0.92", "0.66 / 0.33 / 0.96", "候選 · 小 edge"),
    ]),
    ("參照（放大整條 STX50，需 SMH 用 SOXL/保證金）", GREY, [
        ("vol-target 放大整條 STX50（→1.8x）", "/backtest/leverage/",
         "同規則但槓滿兩邊 · edge 略大但 SMH 半邊無期貨、要槓桿 ETF/保證金",
         "+16.7%", "-24.3%", "0.91", "0.69 / 0.32 / 1.00", "參照"),
        ("常態 1.8x STX50（不挑時段、純放大）", "/backtest/leverage/",
         "固定槓桿只是同比例放大報酬與回撤 · Calmar ≈ 不變(基準對照)",
         "+22.5%", "-36.4%", "0.85", "0.62 / 0.20 / 0.96", "基準對照"),
    ]),
    ("✗ 否決（輸底倉風險調整 — 挑錯時段 / 放大尾部）", RED, [
        ("趨勢閘門 Sys1 / fast-out / 低波動二元 MNQ 腿", "/backtest/leverage/",
         "「趨勢還在」就加槓桿 → 被抱進頭部;低波動二元腿 2008 槓進去 −22%",
         "+17.2%", "-33.4%", "0.78", "0.52 / 0.10 / 0.92", "否決"),
        ("權益曲線 >MA200 / 指數 >200日線體制", "/backtest/leverage/",
         "近常態槓桿 + 太慢的關閉開關 · 2022 一樣被放大到 −24%",
         "+21.0%", "-34.3%", "0.83", "0.61 / 0.15 / 0.98", "否決"),
        ("固定波動目標 / 選擇權凸性", "/backtest/leverage/",
         "固定目標比底倉還差;選擇權(模型)只小贏線性、救不到 MDD、成本一升就沒了",
         "—", "—", "—", "0.56 / 0.25 / 0.83", "否決"),
    ]),
]
BASE = ("1.0x STX50 底倉（不加槓桿）", "+13.8%", "-21.9%", "0.90", "0.63 / 0.24 / 0.95")

# cross-ASSET generalization: same vol-target rule on genuinely low-correlation
# asset classes (corr −0.31~+0.37, not the 0.79–0.92 of SPY/QQQ/SMH). Only equity
# improves → the edge is EQUITY-SPECIFIC, not a universal vol-targeting principle.
# (BH Calmar, VT Calmar, BH Sharpe, VT Sharpe, improved?)
XASSET = [
    ("SPY 美股", "0.22", "0.24", "0.64", "0.67", True),
    ("GLD 黃金", "0.19", "0.16", "0.55", "0.53", False),
    ("USO 原油", "−0.08", "−0.10", "−0.04", "−0.03", False),
    ("DBA 農業", "−0.01", "−0.02", "0.06", "−0.01", False),
    ("FXE 歐元", "−0.03", "−0.04", "−0.09", "−0.13", False),
    ("TLT 長債", "0.05", "0.04", "0.24", "0.20", False),
]


def sys_rows():
    out = ""
    for title, lc, items in ROWS:
        out += (f'<tr><td colspan="6" style="background:#f8fafc;border-left:3px solid {lc};'
                f'font-size:.74rem;font-weight:700;color:#475569;text-transform:uppercase;'
                f'letter-spacing:.04em">{title}</td></tr>')
        for name, url, sub, cagr, mdd, shp, cal, tag in items:
            out += (f'<tr style="border-left:3px solid {lc}"><td><a href="{url}" style="font-weight:600">{name}</a>'
                    f'<div style="font-size:.72rem;color:var(--muted);margin-top:.15rem">{sub}</div></td>'
                    f'<td style="font-weight:700;color:var(--green)">{cagr}</td>'
                    f'<td style="color:var(--muted)">{mdd}</td><td>{shp}</td>'
                    f'<td style="font-variant-numeric:tabular-nums">{cal}</td>'
                    f'<td><span class="tag">{tag}</span></td></tr>')
    n, c, m, s, cal = BASE
    out += (f'<tr style="background:#fafbfc;border-left:3px solid {GREY}"><td><b>{n}</b></td>'
            f'<td>{c}</td><td style="color:var(--muted)">{m}</td><td>{s}</td>'
            f'<td style="font-variant-numeric:tabular-nums">{cal}</td><td><span class="tag tag-bh">基準</span></td></tr>')
    return out


def xmkt_rows():
    out = ""
    for t, a, b, c, d, ok in XASSET:
        col = "#16a34a" if ok else "var(--muted)"
        tag = ('<span class="tag tag-best">✓ 改善</span>' if ok
               else '<span class="tag" style="color:#dc2626">✗ 無改善</span>')
        out += (f'<tr><td><b>{t}</b></td><td>{a}</td>'
                f'<td style="color:{col};font-weight:600">{b}</td>'
                f'<td>{c}</td><td style="color:{col};font-weight:600">{d}</td>'
                f'<td>{tag}</td></tr>')
    return out


CRISIS_YEARS = {2008, 2011, 2018, 2020, 2022}


def _c(v):
    return "#16a34a" if v >= 0 else "#dc2626"


def yearly_rows():
    y = CURVES["yearly"]
    out = ""
    for yr in sorted(CURVES["decomp"], key=int):
        hl = ' style="background:#fffbeb"' if int(yr) in CRISIS_YEARS else ""
        vt = y["voltarget"].get(yr, 0.0); bs = y["base"].get(yr, 0.0)
        c18 = y["const18"].get(yr, 0.0); bh = y["bh"].get(yr, 0.0)
        out += (f'<tr{hl}><td>{yr}</td>'
                f'<td style="color:{_c(vt)};font-weight:600">{vt:+.1f}%</td>'
                f'<td style="color:{_c(bs)}">{bs:+.1f}%</td>'
                f'<td style="color:{_c(c18)}">{c18:+.1f}%</td>'
                f'<td style="color:{_c(bh)}">{bh:+.1f}%</td></tr>')
    return out


def decomp_rows():
    out = ""
    for yr in sorted(CURVES["decomp"], key=int):
        d = CURVES["decomp"][yr]
        hl = ' style="background:#fffbeb"' if int(yr) in CRISIS_YEARS else ""
        out += (f'<tr{hl}><td>{yr}</td>'
                f'<td style="color:{_c(d["base"])}">{d["base"]:+.1f}%</td>'
                f'<td style="color:{_c(d["overlay"])};font-weight:600">{d["overlay"]:+.1f}%</td>'
                f'<td style="color:{_c(d["total"])};font-weight:600">{d["total"]:+.1f}%</td></tr>')
    return out


def render():
    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK, "%SYS_ROWS%": sys_rows(), "%XMKT_ROWS%": xmkt_rows(),
        "%YEARLY_ROWS%": yearly_rows(), "%DECOMP_ROWS%": decomp_rows(),
        "%JS_CURVES%": json.dumps(CURVES),
        "%NOW%": datetime.now().strftime("%Y-%m-%d"),
    }.items():
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>槓桿疊加量化回測總覽 | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--ink:#1f2937;--text:#374151;--muted:#6b7280;--border:#e5e7eb;--bg:#f7f8fa;--card:#fff;
      --green:#b45309;--green-bg:#fffbeb;--green-border:#fde68a;--red:#dc2626;--grey:#9ca3af;--blue:#1a56db}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1080px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.5rem 0 1rem;background:#fff;border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.45rem;font-weight:800;letter-spacing:-.03em;color:var(--ink)}
.page-hdr .sub{color:var(--muted);font-size:.85rem;margin-top:.15rem}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}.crumb a{color:var(--muted)}
.tabs{display:flex;gap:.4rem;margin-top:.9rem;flex-wrap:wrap}
.tabs a{font-size:.86rem;font-weight:600;padding:.4rem .9rem;border:1px solid var(--border);border-radius:7px;color:var(--muted);background:#fff}
.tabs a.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.05rem;font-weight:700;color:var(--ink);margin-bottom:.85rem;padding-bottom:.4rem;border-bottom:1px solid var(--border)}
.section-sub{font-size:.82rem;color:var(--muted);margin:-.45rem 0 .9rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.5rem;margin-bottom:1rem;overflow-x:auto}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem;margin-bottom:1rem}
.chart-wrap{position:relative;width:100%;height:300px}
.chart-wrap-sm{position:relative;width:100%;height:260px}
.prose{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem 1.4rem;margin-bottom:1rem;font-size:.9rem;line-height:1.85}
.prose h3{font-size:.95rem;font-weight:700;color:var(--ink);margin:1rem 0 .4rem}
.prose h3:first-child{margin-top:0}
.prose b{color:var(--ink)}
.formula{background:#fffbeb;border:1px solid var(--green-border);border-radius:8px;padding:.7rem 1rem;margin:.6rem 0;font-size:.86rem;font-variant-numeric:tabular-nums}
.steps{counter-reset:s;list-style:none;margin:.4rem 0}
.steps li{position:relative;padding-left:2rem;margin-bottom:.55rem}
.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:.05rem;width:1.4rem;height:1.4rem;
  background:var(--green);color:#fff;border-radius:50%;font-size:.74rem;font-weight:700;display:flex;align-items:center;justify-content:center}
.eg{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;margin:.7rem 0}
.eg-box{border:1px solid var(--border);border-radius:8px;padding:.8rem .9rem;font-size:.82rem;background:#fafbfc}
.eg-box .h{font-weight:700;color:var(--ink);font-size:.84rem;margin-bottom:.3rem}
.eg-box .big{font-size:1.3rem;font-weight:800;margin:.2rem 0}
.acard{background:var(--card);border:1px solid var(--green);border-radius:12px;padding:1.2rem 1.3rem;box-shadow:0 0 0 1px var(--green) inset;margin-bottom:1rem}
.ac-tag{display:inline-block;font-size:.72rem;font-weight:700;padding:.2rem .6rem;border-radius:99px;margin-bottom:.5rem;background:var(--green);color:#fff}
.ac-name{font-size:1.25rem;font-weight:800;letter-spacing:-.02em;color:var(--ink)}
.ac-sub{font-size:.82rem;color:var(--muted);margin:.25rem 0 .9rem}
.ac-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem}
.ac-metrics > div{text-align:center;background:#fafbfc;border:1px solid var(--border);border-radius:8px;padding:.5rem .3rem}
.ac-metrics span{display:block;font-size:.64rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.ac-metrics b{font-size:1.05rem;font-weight:800;color:var(--ink)}
table{width:100%;border-collapse:collapse;font-size:.84rem}
th,td{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}
th{background:#fafbfc;font-weight:600;font-size:.72rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
.tag{display:inline-block;padding:.13rem .5rem;border-radius:4px;font-size:.7rem;font-weight:600;white-space:nowrap;background:#f3f4f6;color:#475569;border:1px solid var(--border)}
.tag-best{background:var(--green-bg);color:#92400e;border:1px solid var(--green-border)}
.tag-bh{background:#f3f4f6;color:#6b7280;border:1px solid var(--border)}
.note{background:#fafbfc;border:1px solid var(--border);border-left:3px solid var(--grey);border-radius:0 8px 8px 0;padding:.85rem 1.1rem;font-size:.84rem;color:var(--text);margin:1rem 0}
.warn{background:#fffbeb;border:1px solid var(--green-border);border-left:3px solid var(--green);border-radius:0 8px 8px 0;padding:.85rem 1.1rem;font-size:.84rem;margin:1rem 0}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:820px){.eg{grid-template-columns:1fr}.ac-metrics{grid-template-columns:repeat(2,1fr)}table{font-size:.76rem}th,td{padding:.4rem .45rem}}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>槓桿疊加量化回測總覽</h1>
  <div class="sub">用期貨把已採用的 STX50 股核槓到 1.8x · 目標是改善<b>風險調整後</b>報酬,不是衝 CAGR · <a href="/backtest/criteria/">評估標準</a></div>
  <div class="tabs"><a href="/backtest/">🇺🇸 美股</a><a href="/backtest/tw/">🇹🇼 台股</a><a href="/backtest/multi/">🧩 多資產</a><a class="on" href="/backtest/leverage/">🔧 槓桿疊加</a></div>
</div></div>

<div class="container">

<!-- SPOTLIGHT -->
<div class="section">
<h2 class="section-title">唯一過關的方法 · 自適應 vol-target 疊加</h2>
<div class="section-sub">一連串槓桿設計裡,只有這個三個年代都小贏底倉、且不放大尾部。先講它怎麼運作(對你是新方法),再給證據。</div>
<div class="acard">
  <div class="ac-tag">候選 · 小 edge · OOS 中</div>
  <div class="ac-name">vol-target 疊加（MNQ 只槓 QQQ 半邊,+0.4x）</div>
  <div class="ac-sub">依「最近波動 vs 平常波動」連續縮放槓桿:平靜才加、一亂就收。底倉 STX50 不動。</div>
  <div class="ac-metrics">
    <div><span>CAGR</span><b style="color:var(--green)">+15.4%</b></div>
    <div><span>MDD</span><b>-23.3%</b></div>
    <div><span>Sharpe</span><b>0.92</b></div>
    <div><span>Calmar 全/06–15/15–now</span><b style="font-size:.82rem">0.66/0.33/0.96</b></div>
  </div>
</div>
</div>

<!-- PERF CURVES -->
<div class="section">
<h2 class="section-title">績效曲線 · 權益與回撤</h2>
<div class="section-sub">月頻 · 起點=100 · 2006–今。<b>重點是風險調整,不是終值</b>:常態 1.8x／B&amp;H 終值更高,但回撤深得多(見下圖);vol-target(琥珀)用最小的額外回撤把底倉小幅往上推。</div>
<div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem;margin-bottom:1rem">
  <div style="font-size:.86rem;font-weight:600;color:var(--ink);margin-bottom:.3rem">權益曲線(NAV,起點=100,對數軸)</div>
  <div style="position:relative;width:100%;height:340px"><canvas id="chart-nav"></canvas></div>
</div>
<div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem;margin-bottom:1rem">
  <div style="font-size:.86rem;font-weight:600;color:var(--ink);margin-bottom:.3rem">回撤(月頻)</div>
  <div style="position:relative;width:100%;height:240px"><canvas id="chart-dd"></canvas></div>
</div>
<div class="note"><b>讀法:</b>權益圖上「常態 1.8x」(灰虛線)終值最高,但回撤圖它的谷比 vol-target／底倉深得多、B&amp;H(點線)更是 −50% 級。
<b>vol-target(琥珀)的回撤幾乎貼著底倉(藍)</b> —— 這就是「小 edge」的長相:多賺一點、痛幾乎沒多。(月頻略低估盤中回撤,精確值見下方表格。)</div>
</div>

<!-- YEARLY -->
<div class="section">
<h2 class="section-title">逐年績效</h2>
<div class="section-sub">日曆年報酬。黃底為股票危機年(2008/2011/2018/2020/2022)。末年 2026 為年初至今。常態 1.8x／B&amp;H 多數年更高,但崩盤年(2008/2022)被放大得多 —— 對照下方拆解看 vol-target 的槓桿在危機年幾乎關掉。</div>
<div class="chart-card"><div class="chart-wrap"><canvas id="chart-yearly"></canvas></div></div>
<div class="card">
<table><thead><tr><th>年度</th><th>vol-target(採用)</th><th>1.0x STX50 底倉</th><th>常態 1.8x</th><th>B&amp;H 50/50</th></tr></thead>
<tbody>%YEARLY_ROWS%</tbody></table>
</div>
</div>

<!-- DECOMPOSE SOURCE -->
<div class="section">
<h2 class="section-title">來源拆解 · 底倉 vs MNQ 槓桿腿</h2>
<div class="section-sub">把 vol-target 每年的報酬<strong>加法拆成兩塊</strong>:底倉 STX50 的貢獻 ＋ MNQ 槓桿腿的貢獻(以年初 NAV 標準化,兩者相加 = vol-target 合計)。看槓桿腿到底在哪些年加了多少。</div>
<div class="chart-card"><div class="chart-wrap-sm"><canvas id="chart-decomp"></canvas></div></div>
<div class="card">
<table><thead><tr><th>年度</th><th>底倉 STX50 貢獻</th><th>MNQ 槓桿腿貢獻</th><th>vol-target 合計</th></tr></thead>
<tbody>%DECOMP_ROWS%</tbody></table>
</div>
<div class="note"><b>讀法:</b>槓桿腿(琥珀)逐年貢獻其實很小 —— 最大幾年是 <b>2023 +9.3pp、2009 +7.9pp</b>(乾淨大多頭);
而 <b>2008 只 −1.6pp、2022 只 −0.8pp</b>:危機年波動一升,vol-target 把槓桿關到接近 0,所以崩盤年的拖累極小。全期它<b>平均一年只加個位數 pp、且常常是 0</b> —— 這正是「危機自動關、平時小幅加速」的數字證據。</div>
</div>

<!-- METHOD (detailed) -->
<div class="section">
<h2 class="section-title">① 邏輯與做法（詳述）</h2>
<div class="prose">
<h3>核心概念:槓桿與波動成反比</h3>
<p>傳統做法是「趨勢還在就加槓桿」——問題是趨勢訊號在<b>頭部、崩盤前的平靜</b>也常常還亮著,結果槓桿被抱進反轉。
本方法換一個訊號:<b>波動本身</b>。市場<b>比平常平靜</b>時把槓桿放出來、<b>比平常亂</b>時收回。
因為大跌幾乎都伴隨波動飆升,「波動一升就減槓桿」等於<b>崩盤啟動時人已經在減碼</b>——這是它和趨勢閘門最根本的差別。</p>

<h3>精確規則(四步)</h3>
<ol class="steps">
  <li><b>量最近波動</b>:σ = QQQ 過去 <b>20 日</b>報酬的年化標準差。</li>
  <li><b>比平常波動</b>:基準 = σ 的<b>過去 252 日中位數</b>(自適應,不是釘死一個數字——這點很關鍵,固定數字會失敗)。</li>
  <li><b>算槓桿倍數</b>:<span style="white-space:nowrap">L = clip( 中位數 ÷ σ , 1.0 , 1.8 )</span>。比平常平靜 → L&gt;1(加);比平常亂 → L=1(完全不加)。</li>
  <li><b>換成 MNQ 口數</b>:用 MNQ 期貨<b>只槓 QQQ 半邊</b> → 實際加掛 f = (L−1)×0.5 的 MNQ,最多 +0.4x。每月(或每日)依 L 調口數。</li>
</ol>
<div class="formula">L = clip( median₂₅₂(σ) ÷ σ₂₀ , 1.0 , 1.8 )　·　MNQ 疊加 f = (L − 1) × 0.5　·　總曝險 = 底倉(0–100%) + f</div>

<h3>三個真實例子(QQQ 月底)</h3>
<div class="eg">
  <div class="eg-box"><div class="h">😌 平靜月 · 2025-07</div>σ20 = <b>7%</b> ≪ 中位數 20%<div class="big" style="color:var(--green)">L = 1.80</div>加 <b>+0.40x</b> MNQ(封頂)</div>
  <div class="eg-box"><div class="h">🙂 中度平靜 · 2024-06</div>σ20 = <b>12%</b> &lt; 中位數 16%<div class="big" style="color:var(--green)">L = 1.31</div>加 <b>+0.16x</b> MNQ</div>
  <div class="eg-box"><div class="h">🌪️ 危機月 · 2008-03</div>σ20 = <b>32%</b> &gt; 中位數 20%<div class="big" style="color:var(--red)">L = 1.00</div><b>完全不加槓桿</b>(GFC 自動空手)</div>
</div>

<h3>它有多「省」</h3>
<p>全期(2006–今)<b>平均槓桿只 +0.09x</b>、<b>51% 的交易日根本沒槓桿</b>、只有 <b>7% 的日子</b>放到 +0.4x 上限。
槓桿是稀缺資源,只在最平靜時少量放出——這正是它不放大尾部的原因(2008 全年 −6.0% vs 底倉 −5.2%、<b>2022 −15.4% 跟底倉一模一樣</b>)。</p>

<h3>怎麼執行</h3>
<p>持有 STX50 的 SMH/QQQ ETF(底倉照舊),依 L 在 QQQ 半邊加掛 MNQ 微型那指期貨。財務成本 ≈ 現金利率(你閒置資金本來就收 SHY/BIL,對沖掉)+ 幾 bps 滾倉/價差。
<b>注意:SMH(半導體)沒有流動期貨</b>,純 MNQ 只能槓那指(QQQ)半邊——這就是 +0.4x 上限的由來。要槓滿整條(→1.8x)得用 SOXL/保證金處理 SMH 半邊;本研究採用<b>誠實的半邊版</b>。</p>
</div>
</div>

<!-- EVIDENCE: ranking -->
<div class="section">
<h2 class="section-title">② 證據 · 全部試過的版本對打</h2>
<div class="section-sub">過關門檻 = 兩個年代 Calmar 都贏底倉(0.65 全 / 0.27 在 2006–15 / 0.95 在 2015–now),且 2008/2022 尾部不被放大。色帶:<span style="color:#b45309">琥珀=過關</span> · 灰=參照 · <span style="color:var(--red)">紅=否決</span>。</div>
<div class="card">
<table><thead><tr><th>版本</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar 全/06–15/15–now</th><th>狀態</th></tr></thead>
<tbody>%SYS_ROWS%</tbody></table>
</div>
<div class="note"><b>為什麼別的都輸:</b>固定槓桿只是「同比例放大報酬與回撤」,Calmar 幾乎不變;而所有<b>挑時段</b>的趨勢閘門挑到的反而是比平均差的時段(趨勢尾端/崩盤前平靜),把 Calmar 挑低了。要靠槓桿加值,只能把它<b>集中在真正高 Sharpe 的時段</b>——「比平常平靜＋上升、連續縮放」是少數做得到的。</div>
</div>

<!-- EVIDENCE: cross-asset generalization (corrected) -->
<div class="section">
<h2 class="section-title">③ 普遍性檢驗 · 這是「股票特有」的小 edge,不是萬用原理</h2>
<div class="section-sub"><b style="color:#dc2626">2026-06 review 修正:</b>之前宣稱「SPY/QQQ/SMH 9/9 → 普遍原理」<b>是錯的</b> —— 那三個都是高度相關的美股(日報酬相關 0.79–0.92),等於同一賭注測三次。放到<b>真正低相關</b>的資產類別(彼此相關 −0.31~+0.37)才見真章:</div>
<div class="card">
<table><thead><tr><th>資產類別</th><th>B&amp;H Calmar</th><th>vol-target Calmar</th><th>B&amp;H Sharpe</th><th>vol-target Sharpe</th><th></th></tr></thead>
<tbody>%XMKT_ROWS%</tbody></table>
</div>
<div class="note"><b>只有 1/6 改善,而且就是股票。</b>機制:vol-target 加值需要同時有「正的長期漂移」＋「低波動→續漲、高波動→崩的不對稱」——
<b>股票兩個都有;黃金只有漂移,原油/匯/農兩個都弱,長債也不行。</b>所以它是<b>股票特有現象、不跨資產類別</b>,不是普遍的波動目標原理。窗口仍是 15–40 日一片高原(只有 10 日太雜訊破功)。</div>
</div>

<!-- HONEST CAVEATS -->
<div class="section">
<h2 class="section-title">④ 誠實警語</h2>
<div class="warn">
  <b>這是小 edge、股票特有、不是翻倍級的東西。</b>Sharpe 只 +0.02–0.05、Calmar +0.02–0.06,且只對股票(見 ③)。
  最大實質價值是<b>危機年自動收槓桿(不放大尾部)＋ 平靜年小幅加速</b>。<br>
  · <b>已用真實期貨驗證(2026-06)</b>:之前 MNQ 是用 QQQ 還原報酬−現金「代理」;改用<b>真實 NQ 期貨</b>重跑,結果 Calmar 略勝代理(0.66/0.33/0.96)→ 代理沒美化。<br>
  · <b>工具/可執行性折扣</b>:純期貨只能槓 QQQ 半邊(+0.4x);且 <b>MNQ 微型 2019 才上市</b>,回測 65% 期間只能用全尺寸 NQ,小帳戶切不出這麼細的曝險(平均才 +0.09x)。要更大 edge 需 SOXL/保證金槓 SMH 半邊。<br>
  · <b>尚未做 walk-forward</b>:兩個年代是同一份資料的子區間,參數雖落在敏感度高原(15–40d,非針),但「沒過擬合」目前是論證、還沒用擴張窗 OOS 證明。<br>
  · <b>選擇權凸性試過</b>:模型上只小贏線性、且救不到 MDD,不值得。<b>期貨作空也試過(A/B/C)全否決</b>——救持續空頭但 V 轉/軋空賠更多。<br>
  程式與全部數字:<code>v7-backtest/src/long_track_backtest/stx50_mnq_overlay.py</code>。
</div>
</div>

</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 槓桿疊加量化回測總覽 · 真實 yfinance · 生成 %NOW%</div></footer>
<script>
var C=%JS_CURVES%, L=C.labels;
function mk(id,field,logy){
  return new Chart(document.getElementById(id),{type:'line',
   data:{labels:L,datasets:[
     {label:'vol-target 疊加(採用)',data:C.voltarget[field],borderColor:'#b45309',borderWidth:2.6,pointRadius:0,pointHoverRadius:3,tension:0.1},
     {label:'1.0x STX50 底倉',data:C.base[field],borderColor:'#1565c0',borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.1},
     {label:'常態 1.8x STX50',data:C.const18[field],borderColor:'#9ca3af',borderWidth:1.2,borderDash:[6,3],pointRadius:0,pointHoverRadius:3,tension:0.1},
     {label:'1.0x B&H 50/50',data:C.bh[field],borderColor:'#cbd5e1',borderWidth:1.1,borderDash:[2,3],pointRadius:0,pointHoverRadius:3,tension:0.1}
   ]},
   options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
     plugins:{legend:{display:field==='nav',position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'line',boxWidth:24,font:{size:10},padding:10}}},
     scales:{x:{grid:{color:'rgba(0,0,0,0.04)'},ticks:{maxTicksLimit:14,font:{size:10}}},
       y:logy?{type:'logarithmic',grid:{color:'rgba(0,0,0,0.06)'},ticks:{font:{size:10}}}
            :{grid:{color:'rgba(0,0,0,0.06)'},ticks:{callback:function(v){return v+'%'},font:{size:10}}}}}});
}
mk('chart-nav','nav',true); mk('chart-dd','dd',false);

var Y=Object.keys(C.decomp).sort(function(a,b){return a-b});
function ya(k){return Y.map(function(y){return C.yearly[k][y]})}
new Chart(document.getElementById('chart-yearly'),{type:'bar',
 data:{labels:Y,datasets:[
   {label:'vol-target(採用)',data:ya('voltarget'),backgroundColor:'#b45309'},
   {label:'1.0x STX50 底倉',data:ya('base'),backgroundColor:'rgba(21,101,192,0.55)'},
   {label:'常態 1.8x',data:ya('const18'),backgroundColor:'rgba(156,163,175,0.6)'},
   {label:'B&H 50/50',data:ya('bh'),backgroundColor:'rgba(203,213,225,0.7)'}
 ]},
 options:{responsive:true,maintainAspectRatio:false,
   plugins:{legend:{position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'rect',font:{size:10},padding:10}},
     tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+(c.parsed.y>=0?'+':'')+c.parsed.y+'%'}}}},
   scales:{x:{grid:{display:false},ticks:{font:{size:9}}},
     y:{grid:{color:'rgba(0,0,0,0.06)'},ticks:{callback:function(v){return v+'%'},font:{size:10}}}}}});

new Chart(document.getElementById('chart-decomp'),{type:'bar',
 data:{labels:Y,datasets:[
   {label:'底倉 STX50',data:Y.map(function(y){return C.decomp[y].base}),backgroundColor:'rgba(21,101,192,0.6)',stack:'s'},
   {label:'MNQ 槓桿腿',data:Y.map(function(y){return C.decomp[y].overlay}),backgroundColor:'#b45309',stack:'s'}
 ]},
 options:{responsive:true,maintainAspectRatio:false,
   plugins:{legend:{position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'rect',font:{size:10},padding:10}},
     tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+(c.parsed.y>=0?'+':'')+c.parsed.y+'pp'}}}},
   scales:{x:{stacked:true,grid:{display:false},ticks:{font:{size:9}}},
     y:{stacked:true,grid:{color:'rgba(0,0,0,0.06)'},ticks:{callback:function(v){return v+'%'},font:{size:10}}}}}});
</script>
</body></html>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
