"""
Generator for the Taiwan /backtest/tw/ overview page — TW decision dashboard.

Parallel to _build_index.py (US 20y overview) but for the Taiwan research line:
ranks the TW systems on their own basis (NT$, 2010–2026, no 2008 in the main
sample), headlines the adopted E3 2330/0050, and carries the crash-validation
meta from tw_crash.

Numbers — two sources, both ~2010-07..2026, NT$:
  * E3 family + benchmarks: freshly computed from v7-backtest taiwan_lt.py.
  * 0050 single-instrument systems (Ch12 long / six-state / STX50-port / dual):
    PINNED from each system page (same values as _build_index.py GROUPS).

When taiwan_lt or a system page changes, update below and re-run:
    python3 _build_tw.py
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

TAG = {
    "adopt":    '<span class="tag" style="background:#065f46;color:#fff;border:1px solid #065f46">✓ 採用 · OOS</span>',
    "cand":     '<span class="tag" style="background:#fffbeb;color:#92400e;border:1px solid #fde68a">候補 · 未採用</span>',
    "fail":     '<span class="tag tag-fail">否決</span>',
    "analysis": '<span class="tag" style="background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe">分析</span>',
    "bh":       '<span class="tag tag-bh">基準</span>',
}
DOM = {
    "trade":     '<span class="tag" style="background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe">有效交換</span>',
    "best":      '<span class="tag tag-best">0050 單檔最強</span>',
    "mixed":     '<span class="tag tag-bh">混合</span>',
    "dominated": '<span class="tag tag-fail">被支配</span>',
    "na":        "—",
}

# (name, url, subtitle, cagr, mdd, sharpe, calmar, dom, final, tag)
GROUPS = [
    ("✓ 採用(2026-06-23 · OOS 追蹤中)", [
        ("2330/0050 三訊號趨勢集成（E3）", "/backtest/long_track_tw/",
         "50/50 2330/0050 · {W40·W52·TSMOM} 各⅓ · 過尺:Calmar 0.85 vs 同 CAGR 稀釋 B&H 0.60、MDD 比稀釋線淺 ~10pp · 美股長軌的台股鏡像",
         "+20.22%", "-23.75%", "1.16", "0.85", DOM["trade"], "$19.0M", TAG["adopt"]),
    ]),
    ("0050 單檔趨勢候補(2010–2026 · NT$ · 釘自各系統頁 · 皆未採用)", [
        ("0050 週線長軌趨勢（Ch12 W52/104/250）", "/backtest/tw_0050_lt/",
         "週線 score-5 long only · 0050 單檔最強趨勢變體:贏 STX50/六狀態/雙軌風險調整 · 有 W250 暖身偏誤",
         "+14.39%", "-21.30%", "1.10", "0.68", DOM["best"], "$9.13M", TAG["cand"]),
        ("0050 六狀態機（移植）", "/backtest/tw_0050_six/",
         "S1 95%/S2 47.5%/S5 漸進回補 · MA52 驅動 · 風險調整勝 B&H 但輸純長軌(SMH 攻擊腿缺席)",
         "+14.34%", "-26.68%", "0.97", "0.54", DOM["trade"], "$9.07M", TAG["cand"]),
        ("0050 週線進攻趨勢（STX50 移植）", "/backtest/tw_0050/",
         "STX50 方法原樣移植 · 升級在 0050 不複現:Ch12 binary > E3 > STX50(與美股相反)",
         "+12.56%", "-26.69%", "0.95", "0.47", DOM["mixed"], "$7.00M", TAG["cand"]),
        ("0050 雙軌多空・日短軌＋週長軌（否決）", "/backtest/tw_0050_dual/",
         "兩軌可多可空 ST70/LT30 · 被自己的純長軌支配:做空 0% 勝率、日線軌加劇 whipsaw（同美股 dual 結論）",
         "+12.17%", "-30.83%", "0.92", "0.39", DOM["dominated"], "$6.61M", TAG["fail"]),
    ]),
    ("結論驗證 / 分析(無單一指標)", [
        ("台股含崩盤樣本 · 趨勢 vs B&H（^TWII/EWT/2330）", "/backtest/tw_crash/",
         "把 2000(−66%)＋2008(−58%)放進樣本、5 系統零調參 OOS:趨勢把 MDD −60〜66% 砍到 −28〜44%、Calmar 全勝 B&H → 證實「B&H 難敗」是 2009+ 無崩盤的樣本假象",
         "—", "—", "—", "—", DOM["na"], "—", TAG["analysis"]),
        ("0050 四系統總覽・台股 vs 美股為何有差異", "/backtest/tw_0050_compare/",
         "matched-window 檢驗 + 美股升級在 0050 反向扣分的結構解釋（深掘）",
         "—", "—", "—", "—", DOM["na"], "—", TAG["analysis"]),
    ]),
]

# benchmarks (freshly computed, taiwan_lt, 2010-07..2026, NT$, 含息;0050 已修復分割)
BH_ROWS = [
    ("2330/0050 50/50 Buy & Hold", "+24.32%", "-39.47%", "1.16", "0.62"),
    ("2330 台積電 Buy & Hold", "+30.18%", "-44.80%", "1.17", "0.67"),
    ("0050 Buy & Hold（已修復分割）", "+18.13%", "-33.83%", "1.02", "0.54"),
    ("^TWII 加權指數 Buy & Hold（價格指數,不含息）", "+12.42%", "-31.63%", "0.80", "0.39"),
]

# E3 2330-weight ladder (taiwan_lt sweep) — concentration trade-off
SWEEP = [
    ("0 / 100", "+14.85%", "-25.13%", "1.05", "0.59", "0.23"),
    ("25 / 75", "+17.58%", "-22.11%", "1.13", "0.80", "0.56"),
    ("50 / 50", "+20.22%", "-23.75%", "1.16", "0.85", "0.82"),
    ("75 / 25", "+22.77%", "-25.71%", "1.15", "0.89", "0.91"),
    ("100 / 0", "+25.21%", "-27.63%", "1.13", "0.91", "0.86"),
]

# scatter (label, mdd, cagr, color)
SCATTER = [
    ("2330/0050 E3(採用)", 23.75, 20.22, "#16a34a"),
    ("E3 0050 單檔", 25.13, 14.85, "#15803d"),
    ("0050 Ch12 長軌", 21.30, 14.39, "#2e7d32"),
    ("0050 六狀態", 26.68, 14.34, "#2563eb"),
    ("0050 STX50 移植", 26.69, 12.56, "#d97706"),
    ("0050 雙軌(否決)", 30.83, 12.17, "#dc2626"),
    ("B&H 2330/0050", 39.47, 24.32, "#1565c0"),
    ("B&H 0050", 33.83, 18.13, "#60a5fa"),
    ("B&H 2330", 44.80, 30.18, "#a855f7"),
    ("B&H ^TWII", 31.63, 12.42, "#757575"),
]


def sys_row(name, url, sub, cagr, mdd, sharpe, calmar, dom, final, tag):
    return (
        f'<tr><td><a href="{url}" style="font-weight:600">{name}</a>'
        f'<div style="font-size:.74rem;color:var(--muted);margin-top:.2rem">{sub}</div></td>'
        f'<td>{cagr}</td><td style="color:var(--red)">{mdd}</td><td>{sharpe}</td>'
        f'<td>{calmar}</td><td>{dom}</td><td>{final}</td><td>{tag}</td></tr>'
    )


def group_header(title):
    return ('<tr><td colspan="8" style="background:#ecfdf5;font-size:.75rem;font-weight:600;'
            f'color:#065f46;text-transform:uppercase;letter-spacing:.04em">{title}</td></tr>')


def render():
    rows = ""
    for title, items in GROUPS:
        rows += group_header(title)
        rows += "".join(sys_row(*r) for r in items)
    rows += group_header("基準（Buy &amp; Hold · taiwan_lt 計算 · NT$）")
    rows += "".join(
        f'<tr style="background:#f9fafb"><td>{n}</td><td>{c}</td>'
        f'<td style="color:var(--red)">{m}</td><td>{s}</td><td>{cl}</td>'
        f'<td>—</td><td>—</td><td>{TAG["bh"]}</td></tr>'
        for n, c, m, s, cl in BH_ROWS)

    sweep_rows = "".join(
        f'<tr{" style=background:var(--brand-light)" if w == "50 / 50" else ""}>'
        f'<td>{w}</td><td>{c}</td><td style="color:var(--red)">{m}</td>'
        f'<td>{s}</td><td>{cl}</td><td>{h1}</td></tr>'
        for w, c, m, s, cl, h1 in SWEEP)

    js_scatter = json.dumps([dict(label=l, x=x, y=y, color=c) for l, x, y, c in SCATTER])

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%TOGGLE%": make_toggle("tw20y"),
        "%ROWS%": rows,
        "%SWEEP_ROWS%": sweep_rows,
        "%JS_SCATTER%": js_scatter,
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
<title>台股量化回測系統總覽 | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--brand:#16a34a;--brand-light:#ecfdf5;--bg:#f9fafb;--card:#fff;
      --text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--red-text:#991b1b;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
     background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.75rem 0 1.25rem;background:linear-gradient(180deg,#ecfdf5 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
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
.card .takeaway{font-size:.88rem;margin-top:.75rem;padding:.6rem .9rem;border-radius:6px;
                background:var(--brand-light);border-left:3px solid var(--brand)}
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
.hero{margin:1.25rem 0;border:1px solid var(--green-border);border-radius:12px;overflow:hidden;background:var(--card)}
.hero-top{background:linear-gradient(135deg,#ecfdf5 0%,#f0fdf4 100%);padding:1.4rem 1.6rem}
.hero-top .verdict-tag{display:inline-block;background:var(--brand);color:#fff;font-size:.74rem;font-weight:700;
                       letter-spacing:.05em;padding:.25rem .7rem;border-radius:99px;margin-bottom:.5rem}
.hero-top h2{font-size:1.3rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.35rem}
.hero-top p{font-size:.92rem;color:#374151;max-width:62rem}
.note{background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px;
      padding:.85rem 1.1rem;font-size:.84rem;color:var(--amber-text);margin:1rem 0}
.issue-list{font-size:.88rem;color:#374151;padding-left:1.2rem;line-height:1.9}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.chart-card h3{font-size:.95rem;font-weight:600;margin-bottom:.5rem}
.chart-sub{font-size:.78rem;color:var(--muted);margin-bottom:.5rem}
.chart-wrap{position:relative;width:100%;height:380px}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);
       text-align:center;padding:1.25rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){table{font-size:.74rem}th,td{padding:.4rem .45rem}}
</style>
</head>
<body>
%NAV%

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">量化回測</a> / 🇹🇼 台股總覽</div>
    <h1>🇹🇼 台股量化回測系統總覽</h1>
    <div class="sub">2010–2026 · NT$ 含息 · 起始 $1,000,000 · 與美股不同市場/幣別/窗口,不直接同尺並比 · 判定框架見 <a href="/backtest/criteria/">評估標準 v3</a></div>
    %TOGGLE%
  </div>
</div>

<div class="container">

<!-- ===== HERO ===== -->
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag">台股研究線現狀 — 2026-06</span>
    <h2>採用:2330/0050 E3 趨勢集成 · 趨勢的價值在尾部,被 2009+ 無崩盤樣本藏起來</h2>
    <p>台股長軌是美股 <a href="/backtest/long_track_smh/">SMH/QQQ</a> 的鏡像,標的換 2330/0050、規則不改。
       <strong>採用 E3</strong>(過尺:Calmar 0.85 vs 同 CAGR 稀釋 B&amp;H 0.60,MDD 把大盤 −39.5% 砍到 −23.75%);
       美股 06-13 加掛的 <strong>ST 半倉出場閘門(STX50)在台股否決</strong> —— 過不了同一把尺(0.83 輸稀釋 E3 0.85),
       台股急跌常 V 轉、週線閘門砍低追高。<strong>關鍵 meta(見 <a href="/backtest/tw_crash/">含崩盤頁</a>):</strong>
       台股 2009+ 之所以「B&amp;H 難敗」,是樣本裡沒有崩盤;把 2000(−66%)、2008(−58%)放回去做 OOS,
       趨勢把 −60〜66% 的回撤砍到 −28〜44%、Calmar 全勝 B&amp;H。所以在台股採用趨勢的理由是<strong>抗崩盤</strong>,
       而這個價值被近十幾年的多頭樣本藏起來了。每行的支配性 = 對自然基準的 <a href="/backtest/criteria/">L2 判定</a>。</p>
  </div>
</div>

<div class="section">
<h2 class="section-title">全系統對比(台股 · 2010–2026 · NT$)</h2>
<div class="section-sub">點系統名稱進入詳頁。E3 家族與基準由 v7-backtest taiwan_lt 即時計算;0050 單檔系統釘自各自頁面。皆 ~2010–2026、NT$ 含息。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar</th><th>支配性</th><th>期末資產</th><th>狀態</th></tr></thead>
<tbody>
%ROWS%
</tbody>
</table>
</div>

<div class="note">
  <strong>資料與可比性:</strong>① <strong>窗口</strong> — 0050.TW 在 Yahoo 史自 2009,主樣本自 2010-07(暖身後),
  <strong>2008 GFC 不在主樣本</strong>;尾部保護的真正考驗見 <a href="/backtest/tw_crash/">含崩盤頁</a>(另加 2000/2008)。
  ② <strong>0050 分割修復</strong> — Yahoo 把 2025-06 的 1:4 分割錯套在 2014-01-02 起,本站 ×4 修復(對照 2330/^TWII 驗證)。
  ③ <strong>計價</strong> — 全部 NT$ 含息、現金腿台幣 1%/年,<strong>與美股總覽不同尺,不可直接並比</strong>。
</div>
</div>

<!-- ===== CONCENTRATION LADDER ===== -->
<div class="section">
<h2 class="section-title">E3 的領先從哪來:2330 權重梯</h2>
<div class="section-sub">同 E3 規則,只改 2330/0050 權重。藍底 = 採用的 50/50。</div>
<div class="card">
<table>
<thead><tr><th>2330 / 0050</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar</th><th>H1 Calmar</th></tr></thead>
<tbody>
%SWEEP_ROWS%
</tbody>
</table>
<div class="takeaway"><strong>誠實歸因:E3 在 0050 單檔的 Calmar 只有 0.59,反而輸 0050 Ch12 長軌的 0.68</strong>
(與美股 E3&gt;Ch12 相反 —— 0050 上是 Ch12 binary &gt; E3 &gt; STX50)。
E3 2330/0050 能到 0.85,<strong>領先全來自加入 2330(台積電)</strong>:往 2330 加碼 CAGR 單調升、Calmar 也升,
但這是放大「台積電單一公司賭注」,不是 E3 規則本身更強。50/50 已是兩個子期間證據下較穩的點(0050 本就半個台積電,集中度難免)。</div>
</div>
</div>

<!-- ===== SCATTER ===== -->
<div class="section">
<h2 class="section-title">風險 vs 報酬(MDD × CAGR)</h2>
<div class="chart-card">
  <div class="chart-sub">左上 = 高報酬低回撤(較佳)· 綠 = 趨勢系統 · 藍/紫/灰 = Buy &amp; Hold 基準</div>
  <div class="chart-wrap"><canvas id="chart-scatter"></canvas></div>
</div>
</div>

<!-- ===== FINDINGS ===== -->
<div class="section">
<h2 class="section-title">結構性發現(台股)</h2>
<div class="card">
<ol class="issue-list">
  <li><strong>趨勢在台股的溢酬在尾部,被樣本藏起來。</strong>2009+ 無崩盤 → B&amp;H 帳面難敗;
      <a href="/backtest/tw_crash/">含崩盤 OOS</a> 證實趨勢把 −60〜66% 砍到 −28〜44%、Calmar 全勝。採用趨勢 = 買「下次崩盤不會發生在你身上」。</li>
  <li><strong>美股的「升級」在台股反向。</strong>0050 單檔上 Ch12 binary &gt; E3 &gt; STX50(美股是 E3 &gt; Ch12);
      <strong>ST 半倉出場閘門台股否決</strong> —— 台股急跌常 V 轉,週線閘門砍低追高、傷害集中 H1。
      與美股的教訓對稱:規則優勢 = 規則 × 標的回撤-修復幾何,不可假設可移植。</li>
  <li><strong>採用結構的領先來自標的、不是規則。</strong>E3 2330/0050 的 Calmar 0.85 領先,主要是加了 2330(台積電)集中度;
      E3 規則本身在 0050 單檔輸 Ch12。誠實揭露於上方權重梯。</li>
  <li><strong>六狀態 / 雙軌在 0050 被純長軌支配。</strong>雙軌做空 0% 勝率、日線軌加劇 whipsaw(同美股 dual 結論);
      六狀態缺 SMH 攻擊腿,風險調整勝 B&amp;H 但輸純長軌。</li>
</ol>
</div>
</div>

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 台股量化回測系統總覽 &middot; 真實 yfinance 資料(0050 已修復分割)&middot;
    E3 家族由 taiwan_lt 即時計算、0050 系統釘自各頁 &middot; 頁面生成 %NOW% &middot; 僅供研究參考
  </div>
</footer>

<script>
var SCATTER=%JS_SCATTER%;
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;
new Chart(document.getElementById('chart-scatter'),{
  type:'scatter',
  data:{datasets:SCATTER.map(function(p){return {label:p.label,data:[{x:p.x,y:p.y}],
    backgroundColor:p.color,borderColor:p.color,pointRadius:7,pointHoverRadius:9};})},
  options:{responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:true,position:'right',labels:{usePointStyle:true,pointStyle:'circle',padding:8,font:{size:10}}},
      tooltip:{callbacks:{label:function(c){return c.dataset.label+': MDD -'+c.parsed.x.toFixed(1)+'%, CAGR +'+c.parsed.y.toFixed(1)+'%'}}}},
    scales:{
      x:{title:{display:true,text:'最大回撤 MDD (%)'},reverse:true,grid:{color:'rgba(0,0,0,0.06)'},
         ticks:{callback:function(v){return '-'+v+'%'}}},
      y:{title:{display:true,text:'CAGR (%)'},grid:{color:'rgba(0,0,0,0.06)'},
         ticks:{callback:function(v){return '+'+v+'%'}}}}
  }
});
</script>
</body>
</html>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
