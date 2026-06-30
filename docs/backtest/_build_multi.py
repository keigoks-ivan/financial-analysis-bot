"""Multi-asset /backtest/multi/ overview — dashboard (muted palette).

Sibling of the US /backtest/ (_index_layout.py) and TW /backtest/tw/
(_build_tw.py): same layout family + palette, 美股/台股/多資產 tab switch.
These systems trade DIFFERENT asset pools (commodity / bond / FX / global
ETF) — complementary to the single-asset US stock systems, NOT on the same
return scale. The page is about diversification + portfolio contribution.

Numbers PINNED, sourced from each system's detail page (mirrors the rows that
used to live in the US overview's 多資產 group). When a system page changes,
update below and re-run:  python3 _build_multi.py

Run: python3 _build_multi.py
"""
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("quant", "bt")
OUT = Path(__file__).parent / "multi" / "index.html"

TEAL, GREEN, RED, GREY = "#0f766e", "#16a34a", "#dc2626", "#9ca3af"

# Adoption candidate spotlight: the 80/20 combined system (sleeve = L4-pending).
LIVE_CARD = {
    "name": "組合系統 · STX50 + 商品 Sleeve（80/20）", "tag": "L4 候選 · OOS 並行追蹤",
    "sub": "80% STX50(SMH/QQQ)＋ 20% CMDTY2 sleeve(GLD/USO→MGC/MCL)· 月底再平衡 · sleeve 採用為未決 L4 決策",
    "cagr": "+13.79%", "mdd": "-16.31%", "sharpe": "1.04", "calmar": "0.85",
    "url": "/backtest/turtle_adopt/",
}

# (name, url, sub, cagr, mdd, sharpe, calmar, dom, status_tag)
def tag_cand():
    return '<span class="tag tag-best">候選 · 未採用</span>'
def tag_ref():
    return '<span class="tag">參照 · 不同資產池</span>'
def tag_bh():
    return '<span class="tag tag-bh">基準</span>'

SYSTEMS = [
    ("L4 採用候選", TEAL, [
        ("🧩 組合系統:STX50 + 商品 Sleeve（80/20）", "/backtest/turtle_adopt/",
         "商品 sleeve 疊上股票核心 · Calmar 0.65→0.85、MDD -21.9%→-16.3%(sleeve 視窗)· 削回撤、不增報酬 · "
         "sleeve 採用待 L4 · 即時頁 <a href='/turtle-sleeve/'>/turtle-sleeve/</a>",
         "+13.79%", "-16.31%", "1.04", "0.85", "有效交換", tag_cand()),
        ("🐢 商品/債/匯/股 唐奇安突破（55/20）", "/backtest/turtle/",
         "USO/GLD/DBA/FXE/TLT/SPY · 55/20 突破(2007 起)· 2026-06 修正:原 22.5% CAGR 是停損成交假象,"
         "修正後全系統平庸(CAGR 7.61% / Calmar 0.15);殘餘價值僅 GLD/USO 低相關 sleeve(+20% → 組合 0.63→0.85),sleeve 即取自此",
         "+7.61%", "-52.28%", "0.39", "0.15", "被支配", tag_ref()),
    ]),
    ("分散參照(資產池不同,僅供對照)", GREY, [
        ("🛡️ 跨資產防守趨勢（SPY/TLT/GLD/DBC）", "/backtest/crossasset_defense/",
         "股/債/金/商品 各一條 · E3 趨勢 + Chandelier 回吐閘門 · 等權 · 防守端:CAGR 最低但 "
         "Calmar 0.64/Sharpe 0.94 全勝 GEM/Clenow、對 QQQ 月相關僅 0.28 → 真分散補位",
         "+6.04%", "-9.39%", "0.94", "0.64", "有效交換", tag_ref()),
        ("📈 35 檔 ETF 跨資產趨勢（EMA＋突破）", "/backtest/clenow/",
         "35 ETF × 7 類別 · EMA50/100 + 突破 · 經典 Clenow 趨勢配置(2026-06 補 vol-cap)",
         "+12.68%", "-45.05%", "0.66", "0.28", "混合", tag_ref()),
    ]),
]

# benchmarks (single-asset US B&H) — shown for SCALE reference only
BH = [
    ("50/50 SPY/QQQ B&H", "+13.55%", "-53.66%", "0.25"),
    ("QQQ Buy & Hold", "+15.91%", "-53.40%", "0.30"),
    ("SPY Buy & Hold", "+11.04%", "-55.19%", "0.20"),
]

SCATTER = [
    ("🧩 組合 80/20(候選)", 16.31, 13.79, TEAL),
    ("🐢 唐奇安突破", 52.28, 7.61, "#0f766e"),
    ("🛡️ 跨資產防守", 9.39, 6.04, "#16a34a"),
    ("📈 跨資產趨勢", 45.05, 12.68, "#6366f1"),
    ("B&H 50/50 SPY/QQQ", 53.66, 13.55, "#94a3b8"),
    ("B&H QQQ", 53.40, 15.91, "#1565c0"),
    ("B&H SPY", 55.19, 11.04, "#757575"),
]


def sys_rows():
    out = ""
    for title, lc, items in SYSTEMS:
        out += (f'<tr><td colspan="6" style="background:#f8fafc;border-left:3px solid {lc};'
                f'font-size:.74rem;font-weight:700;color:#475569;text-transform:uppercase;'
                f'letter-spacing:.04em">{title}</td></tr>')
        for name, url, sub, cagr, mdd, shp, cal, dom, tag in items:
            out += (f'<tr style="border-left:3px solid {lc}"><td><a href="{url}" style="font-weight:600">{name}</a>'
                    f'<div style="font-size:.72rem;color:var(--muted);margin-top:.15rem">{sub}</div></td>'
                    f'<td style="font-weight:700;color:var(--green)">{cagr}</td>'
                    f'<td style="color:var(--muted)">{mdd}</td><td>{shp}</td><td>{cal}</td><td>{tag}</td></tr>')
    out += (f'<tr><td colspan="6" style="background:#f8fafc;border-left:3px solid {GREY};'
            f'font-size:.74rem;font-weight:700;color:#475569;text-transform:uppercase">基準(單一股票池 B&amp;H · 不同尺)</td></tr>')
    for n, c, m, cl in BH:
        out += (f'<tr style="background:#fafbfc;border-left:3px solid {GREY}"><td>{n}</td>'
                f'<td>{c}</td><td style="color:var(--muted)">{m}</td><td>—</td><td>{cl}</td><td>{tag_bh()}</td></tr>')
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
  <a class="ac-link" href="{c['url']}">採用評估頁 →</a> &nbsp;·&nbsp; <a href="/turtle-sleeve/" style="font-size:.82rem">即時 sleeve 狀態 →</a>
</div>
<div class="acard-note">
  <div class="acn-title">為什麼獨立分頁</div>
  <ul>
    <li>這些系統交易<b>不同資產池</b>(商品/債/匯/全球 ETF),報酬軸<b>不與單一股票池系統同尺</b> — 看的是分散與組合貢獻,不是 CAGR 對打。</li>
    <li>商品 sleeve 對 STX50 月相關 ≈ -0.03、三次危機窗全正,<b>+20% 權重把組合 Calmar 0.63→0.85</b> — 採用與工具(需期貨)待 L4。</li>
    <li>跨資產防守腿對 QQQ 月相關僅 0.28,是真正的分散補位(非報酬來源)。</li>
  </ul>
</div>"""

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%CARD%": card, "%SYS_ROWS%": sys_rows(),
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
<title>多資產量化回測總覽 | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--ink:#1f2937;--text:#374151;--muted:#6b7280;--border:#e5e7eb;--bg:#f7f8fa;--card:#fff;
      --green:#0f766e;--green-bg:#f0fdfa;--green-border:#99f6e4;--red:#dc2626;--grey:#9ca3af}
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
.tag-best{background:var(--green-bg);color:#115e59;border:1px solid var(--green-border)}
.tag-bh{background:#f3f4f6;color:#6b7280;border:1px solid var(--border)}
.note{background:#fafbfc;border:1px solid var(--border);border-left:3px solid var(--grey);border-radius:0 8px 8px 0;padding:.85rem 1.1rem;font-size:.84rem;color:var(--text);margin:1rem 0}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem;margin-bottom:1rem}
.chart-card h3{font-size:.92rem;font-weight:600;color:var(--ink);margin-bottom:.4rem}
.chart-sub{font-size:.76rem;color:var(--muted);margin-bottom:.5rem}
.chart-wrap{position:relative;width:100%;height:340px}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:820px){.live-wrap{grid-template-columns:1fr}table{font-size:.76rem}th,td{padding:.4rem .45rem}}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>多資產量化回測總覽</h1>
  <div class="sub">商品 / 債 / 匯 / 全球 ETF · 與美股單一股票池<b>互補</b>,報酬軸不同尺 · 起始 $1M · <a href="/backtest/criteria/">評估標準</a></div>
  <div class="tabs"><a href="/backtest/">🇺🇸 美股</a><a href="/backtest/tw/">🇹🇼 台股</a><a class="on" href="/backtest/multi/">🧩 多資產</a><a href="/backtest/leverage/">🔧 槓桿疊加</a></div>
</div></div>

<div class="container">

<!-- SPOTLIGHT -->
<div class="section">
<h2 class="section-title">採用候選 · 組合系統(80/20)</h2>
<div class="section-sub">多資產的價值在<b>組合貢獻</b>:商品 sleeve 疊上美股股票核心(STX50)後的 80/20 系統,是目前唯一進到 L4 決策的多資產拼圖。</div>
<div class="live-wrap">%CARD%</div>
</div>

<!-- RANKING -->
<div class="section">
<h2 class="section-title">多資產系統 · 風險調整排名</h2>
<div class="section-sub">左色帶:<span style="color:#0f766e">藍綠=L4 候選</span> · 灰=分散參照。皆 2006/2007–2026 · 真實 yfinance · 報酬軸不與單一股票池同尺(資產池不同)。</div>
<div class="card">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar</th><th>狀態</th></tr></thead>
<tbody>%SYS_ROWS%</tbody></table>
</div>
<div class="note"><b>誠實歸因:</b>唐奇安突破舊報 CAGR +22.5% 是<b>停損成交假象</b>(收盤觸發、停損價成交);2026-06 修正後僅 +7.61% / Calmar 0.15,全系統平庸、MDD -52%。
真正可用的只剩它的<b>GLD/USO 商品腿與股票核心低相關</b> — 取 20% 疊進 STX50 → 組合 Calmar 0.63→0.85(削回撤、不增報酬)。跨資產防守腿則用低相關換分散,CAGR 最低但 Calmar/Sharpe 全勝 GEM/Clenow。</div>
</div>

<!-- CHART -->
<div class="section">
<h2 class="section-title">風險 vs 報酬</h2>
<div class="chart-card"><h3>MDD × CAGR</h3><div class="chart-sub">左上最佳 · 藍綠=候選 · 灰=單一股票池 B&amp;H(不同尺,僅供位置對照)</div><div class="chart-wrap"><canvas id="chart-scatter"></canvas></div></div>
</div>

<!-- RESEARCH NOTES -->
<div class="section">
<h2 class="section-title">研究筆記</h2>
<a href="/backtest/slope_filter_global/" style="display:flex;gap:.75rem;align-items:center;background:var(--card);border:1px solid var(--border);border-left:3px solid #0f766e;border-radius:8px;padding:1rem 1.25rem;text-decoration:none;color:inherit">
  <span style="font-size:1.3rem">🌍</span>
  <span style="flex:1"><span style="font-weight:600;color:#0f766e">全球斜率穩健性 — W52 斜率規則跨市場移植</span><br><span style="font-size:.82rem;color:var(--muted)">把 SPY/AGG 斜率擇時搬到多個全球市場,測規則優勢是結構性還是 SPY 特定</span></span>
  <span style="color:#0f766e">→</span>
</a>
<a href="/turtle-sleeve/" style="display:flex;gap:.75rem;align-items:center;background:var(--card);border:1px solid var(--border);border-left:3px solid #d97706;border-radius:8px;padding:1rem 1.25rem;text-decoration:none;color:inherit;margin-top:.75rem">
  <span style="font-size:1.3rem">🐢</span>
  <span style="flex:1"><span style="font-weight:600;color:#b45309">商品 Sleeve + 組合系統 — 即時狀態(OOS 並行追蹤)</span><br><span style="font-size:.82rem;color:var(--muted)">GLD/USO→MGC/MCL 日線訊號 + 80/20 STX50 組合曝險 · 每日美股收盤後更新 · 紙上權益,非實倉</span></span>
  <span style="color:#b45309">→</span>
</a>
</div>

</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 多資產量化回測總覽 · 真實 yfinance · 生成 %NOW%</div></footer>

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
