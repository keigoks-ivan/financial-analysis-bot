"""
Generator for the system pages that have no dedicated backtest engine generator:
  /backtest/dual_track/  - 雙軌多空
  /backtest/gem/         - GEM 雙動能

DO NOT add these back — they are owned by generators in the v7-backtest repo
(re-running them here would overwrite the corrected hero-layout pages):
  /backtest/long_track/           v7-backtest/src/long_track_backtest/generate_site_page.py
  /backtest/long_track_qqq/       v7-backtest/src/lto_qqq_backtest/generate_site_page.py
  /backtest/long_track_ensemble/  v7-backtest/src/long_track_backtest/generate_ensemble_page.py
  /backtest/six_state/            v7-backtest/six_state_backtest/generate_site_page.py
  /backtest/six_state_v1r1/       v7-backtest/six_state_backtest/generate_v1r1_page.py

Sub-navigation comes from _nav_common.make_toggle (single source).
Run from anywhere; outputs each <slug>/index.html.  Re-run to regenerate.
"""
import sys
from pathlib import Path

OUT = Path(__file__).parent
sys.path.insert(0, str(OUT))
from _nav_common import make_toggle  # noqa: E402

# Canonical site header (single source: scripts/site_nav.py)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block  # noqa: E402

NAV_HEADER = full_nav_block("quant", "bt")

# ===== Common assets =====
CSS = """
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
.toggle-pill{display:inline-flex;gap:0;border:1px solid var(--border);border-radius:6px;overflow:hidden;margin-top:.75rem;flex-wrap:wrap}
.toggle-pill a{padding:.4rem .85rem;font-size:.8rem;font-weight:500;text-decoration:none;border-left:1px solid var(--border)}
.toggle-pill a:first-child{border-left:none}
.toggle-pill a.active{background:var(--brand);color:#fff;font-weight:600}
.toggle-pill a:not(.active){background:#fff;color:var(--brand)}
.section{padding:1.5rem 0}
.section-title{font-size:1.15rem;font-weight:700;margin-bottom:1rem;
               padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.section-sub{font-size:.85rem;color:var(--muted);margin-bottom:1rem;margin-top:-.5rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.card h3{font-size:1rem;font-weight:600;margin-bottom:.85rem;color:var(--text)}
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{text-align:left;padding:.6rem .75rem;border-bottom:1px solid var(--border)}
th{background:#f9fafb;font-weight:600;font-size:.78rem;text-transform:uppercase;
   letter-spacing:.04em;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
tbody tr:hover td{background:#f3f4f6}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.7rem;margin-bottom:1rem}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:.85rem 1rem;text-align:center}
.kpi .label{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:.25rem}
.kpi .value{font-size:1.25rem;font-weight:700}
.kpi .value.pos{color:var(--green)}.kpi .value.neg{color:var(--red)}.kpi .value.neu{color:var(--brand)}
.kpi-pair{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}
.kpi-pair > div{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem 1.2rem}
.kpi-pair h4{font-size:.85rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:.7rem;font-weight:600}
.verdict{background:var(--brand-light);border-left:4px solid var(--brand);
         padding:1rem 1.4rem;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.9rem;line-height:1.7}
.verdict strong{color:var(--brand)}
.note{background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px;
      padding:.85rem 1.1rem;font-size:.82rem;color:var(--amber-text);margin:1rem 0}
.event-card{background:var(--card);border:1px solid var(--border);border-radius:8px;
            padding:.85rem 1.1rem;margin-bottom:.6rem}
.event-card .ev-name{font-weight:600;font-size:.92rem;margin-bottom:.3rem;color:var(--text)}
.event-card .ev-detail{font-size:.83rem;color:#374151;line-height:1.65}
.tag{display:inline-block;padding:.15rem .55rem;border-radius:4px;font-size:.72rem;font-weight:600}
.tag-best{background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)}
.tag-warn{background:var(--amber-bg);color:var(--amber-text);border:1px solid var(--amber-border)}
.tag-fail{background:var(--red-bg);color:var(--red-text);border:1px solid var(--red-border)}
.tag-pass{background:#f3f4f6;color:#374151;border:1px solid #d1d5db}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.chart-card h3{font-size:.95rem;font-weight:600;margin-bottom:.5rem;color:var(--text)}
.chart-wrap{position:relative;width:100%;height:380px}
.chart-wrap-sm{position:relative;width:100%;height:200px}
.hero{margin:1.25rem 0;border:1px solid var(--border);border-radius:12px;overflow:hidden;background:var(--card)}
.hero-top{padding:1.4rem 1.6rem;border-bottom:1px solid var(--border)}
.hero-top .verdict-tag{display:inline-block;color:#fff;font-size:.74rem;font-weight:700;
                       letter-spacing:.05em;padding:.25rem .7rem;border-radius:99px;margin-bottom:.5rem}
.hero-top h2{font-size:1.35rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.35rem}
.hero-top p{font-size:.92rem;color:#374151;max-width:60rem}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);
       text-align:center;padding:1.25rem 0;font-size:.78rem}
@media(max-width:768px){
  .kpi-grid{grid-template-columns:repeat(2,1fr)}
  .kpi-pair{grid-template-columns:1fr}
  table{font-size:.78rem}th,td{padding:.45rem .5rem}
}
"""

# Years used in yearly returns arrays
YEARS = list(range(2006, 2027))

# ===== System data =====
# Each system has: name, slug, color, 20y/10y metrics, yearly returns, etc.

SYSTEMS = {
    "dual": {
        "name": "雙軌多空",
        "subtitle": "50/50 SPY/QQQ · Short Track 70% + Long Track 30%",
        "color": "#7c3aed",
        "hero": {
            "tag": "✗ 原始設計 — 已否決",
            "tag_bg": "#dc2626",
            "bg": "linear-gradient(135deg,#fef2f2 0%,#fff5f5 100%)",
            "border": "var(--red-border)",
            "title": "70% 資金配給獲利因子 1.15 的短線軌 — 結構性錯置",
            "body": """v7 Ch12 原始雙軌設計。短線軌(70% 資金)獲利因子僅 1.15、做空勝率 11-16%,
                貢獻 75.7% 的最大回撤,把長線軌(獲利因子 6.6-8.9)的優勢稀釋殆盡。
                CAGR 4.60% 輸所有基準。後續演化:移除短線軌 →
                <a href="/backtest/long_track/">Long Track Only</a>(2026-06 修正版 +9.59% / -20.08%)。
                「指數做空不可行」由本系統與 <a href="/backtest/turtle/">Turtle 的 SPY 腿</a>(勝率 3.2%)獨立驗證兩次。""",
        },
        "rules": """
            原始 v7 Ch12 系統設計。每個標的內部分為兩條獨立軌道:<br>
            <strong>短線軌 (70% 資金)</strong>: D60/D120/D200 日線均線,N=2 出場確認,可做多可做空。<br>
            <strong>長線軌 (30% 資金)</strong>: W52/W104/W250 週線均線,N=1 出場,可做多可做空。<br>
            兩軌獨立運作,可同時持有相反方向。50/50 配置 SPY 和 QQQ 兩個標的。
        """,
        "m20": {"cagr": 4.60, "mdd": -26.83, "sharpe": 0.42, "sortino": 0.51, "calmar": 0.17, "vol": 12.47, "trades": 210, "final": "$2.00M"},
        "m10": {"cagr": 7.28, "mdd": -19.38, "sharpe": 0.60, "sortino": 0.71, "calmar": 0.38, "vol": 12.50, "trades": 105, "final": "$2.02M"},
        "yearly": [None, None, None, None, 5.69, -19.27, 5.18, 29.62, 7.79, -18.49, -2.28, 25.48, 4.43, 1.62, 9.42, 18.27, -13.13, 12.22, 15.26, 6.23, -2.40],
        "verdict": """
            <strong>原始系統,已被證明是錯誤設計。</strong> 短線軌獲利因子僅 1.15、佔 70% 資金,
            把長線軌的優勢稀釋掉了。CAGR 4.60% 跑輸所有基準,Calmar 0.17 不及格。
            短線軌在所有 4 個子軌中貢獻了 75.7% 的最大回撤。
            <strong>建議改用 Long Track Only 配置</strong> (移除短線軌)。
        """,
        "extra_section": ("短線軌 vs 長線軌貢獻拆解", """
<table>
<thead><tr><th></th><th>SPY Short</th><th>SPY Long</th><th>QQQ Short</th><th>QQQ Long</th></tr></thead>
<tbody>
<tr><td>交易數</td><td>84</td><td>15</td><td>89</td><td>22</td></tr>
<tr><td>勝率</td><td>40.5%</td><td style="color:var(--green);font-weight:600">53.3%</td><td>36.0%</td><td>40.9%</td></tr>
<tr><td>盈虧比</td><td>1.68x</td><td style="color:var(--green);font-weight:600">5.77x</td><td>2.10x</td><td style="color:var(--green);font-weight:600">12.87x</td></tr>
<tr><td>獲利因子</td><td>1.14</td><td style="color:var(--green);font-weight:600">6.60</td><td>1.18</td><td style="color:var(--green);font-weight:600">8.91</td></tr>
<tr><td>做空勝率</td><td style="color:var(--red)">11.8%</td><td>—</td><td style="color:var(--red)">15.8%</td><td>—</td></tr>
<tr><td>總 P&amp;L</td><td>+$131K</td><td style="font-weight:600">+$865K</td><td>+$264K</td><td style="font-weight:600">+$1,464K</td></tr>
<tr><td>佔 MDD %</td><td style="color:var(--red);font-weight:600">46.2%</td><td>11.5%</td><td style="color:var(--red);font-weight:600">29.5%</td><td>10.0%</td></tr>
</tbody>
</table>
<div class="note">
  短線軌做空方向幾乎全軍覆沒 (SPY 11.8%、QQQ 15.8% 勝率)。
  70% 資金配給獲利因子 ~1.15 的策略是 underperform 的根本原因。
</div>
        """),
    },
    "gem": {
        "name": "GEM 雙動能",
        "subtitle": "SPY / ACWX / AGG · 月度切換 · Gary Antonacci",
        "color": "#f57c00",
        "hero": {
            "tag": "✓ 經典防守基準",
            "tag_bg": "#f57c00",
            "bg": "linear-gradient(135deg,#fff7ed 0%,#fffbf5 100%)",
            "border": "#fed7aa",
            "title": "2008 一役定江山 — alpha 集中在單一事件的防守型經典",
            "body": """Gary Antonacci 的雙動能,規則只有兩條、20 年僅 33 次換倉,低過擬合風險。
                2008 GFC 完美避開(-1.30% vs SPY -36.97%)是它全部價值的來源;
                2010 之後的 V 轉環境(2018/2020/2022)避險訊號反而慢半拍。
                定位:組合中的防守對照組,不是報酬引擎。""",
        },
        "rules": """
            Gary Antonacci 的 Global Equities Momentum 雙動能策略。每月底依據 12 個月動能決定下月持倉:<br>
            <strong>1. 相對動能</strong>: 比較 SPY (美國) vs ACWX (國際) 過去 12 個月報酬,選較強者。<br>
            <strong>2. 絕對動能</strong>: 若勝出市場的 12 個月報酬 &gt; T-Bill 12 個月累積報酬,持有股票;否則切換到 AGG 債券避險。<br>
            單邊交易成本 0.1%,初始 $100,000 (規格定義),全期 20 年僅 33 次換倉。
            ACWX 於 2008-03 上市,之前用 EFA 替代,以延續價格序列。
        """,
        "m20": {"cagr": 8.49, "mdd": -21.54, "sharpe": 0.54, "sortino": 0.76, "calmar": 0.39, "vol": 12.55, "trades": 33, "final": "$484K*"},
        "m10": {"cagr": 8.93, "mdd": -21.54, "sharpe": 0.70, "sortino": 0.96, "calmar": 0.41, "vol": 11.73, "trades": 18, "final": "$2.34M"},
        "yearly": [16.48, 9.48, -1.30, 6.35, 6.99, -0.85, 11.26, 28.45, 13.45, -7.52, 6.80, 20.17, -8.01, 18.02, 1.69, 24.11, -16.57, 5.84, 24.97, 13.33, 3.61],
        "verdict": """
            <strong>老牌防守型系統,各項指標都剛好及格,沒一項突出。</strong>
            優點是<strong>邏輯極簡 (只有 2 個規則)</strong>,20Y 和 10Y 表現幾乎一致 (CAGR 8.15% vs 8.93%),
            這個穩定性反而證明它沒過擬合。最大價值是 2008 GFC 完美避險 (-1.30% vs SPY -36.81%)。
            <strong>近 10 年表現乏力</strong> — 後 GFC 低 vol 多頭環境是 GEM 的天敵。
            <span style="font-size:.78rem;color:var(--muted)">* 規格定義初始 $100K,其他系統 $1M。</span>
        """,
        "extra_section": ("關鍵事件 + GEM 的「2010s problem」", """
<div class="event-card">
  <div class="ev-name">2008 GFC <span class="tag tag-best" style="margin-left:.5rem">+34pp vs SPY</span></div>
  <div class="ev-detail">GEM 全年僅 -1.30% vs SPY -36.97%。2008-01 即觸發 INT→AGG 進入避險,直到 2009-09 才重新進場股票,完美避開金融海嘯。</div>
</div>
<div class="event-card">
  <div class="ev-name">2020 COVID <span class="tag tag-fail" style="margin-left:.5rem">-17pp vs SPY</span></div>
  <div class="ev-detail">GEM 全年 +1.69% vs SPY +18.41%。2020-03 觸發 SPY→AGG,2020-05 才重新進場,錯過最猛 V 轉反彈。GEM 對 V 轉反應遲鈍。</div>
</div>
<div class="event-card">
  <div class="ev-name">2022 通膨熊 <span class="tag tag-best" style="margin-left:.5rem">+2pp vs SPY</span></div>
  <div class="ev-detail">GEM -16.57% vs SPY -18.26%。觸發避險但債券同步下跌,優勢有限。</div>
</div>

<h3 class="section-title" style="margin-top:1.25rem">分期間 CAGR 衰退</h3>
<table>
<thead><tr><th>期間</th><th>GEM</th><th>SPY B&amp;H</th><th>差距</th></tr></thead>
<tbody>
<tr><td>全期 21 年</td><td>+8.15%</td><td>+10.64%</td><td style="color:var(--red)">-2.49pp</td></tr>
<tr><td>近 15 年</td><td>+8.54%</td><td>+12.39%</td><td style="color:var(--red)">-3.85pp</td></tr>
<tr><td><strong>近 10 年</strong></td><td><strong>+8.93%</strong></td><td><strong>+14.39%</strong></td><td style="color:var(--red);font-weight:600">-5.46pp</td></tr>
<tr><td><strong>近 5 年</strong></td><td><strong>+5.32%</strong></td><td><strong>+8.70%</strong></td><td style="color:var(--red);font-weight:600">-3.38pp</td></tr>
</tbody>
</table>
<div class="note">
  GEM 的 alpha 主要來自避開 2008 GFC 那次大空頭,2010 之後沒有等量級的長期熊市,
  系統反而因為頻繁的避險訊號吃成本 (2018, 2020, 2022 都觸發但都是 V 轉)。
  這是 GEM 在後 GFC 低 vol 多頭環境的已知弱點 (the "2010s problem")。
</div>
        """),
    },
}


NAV_HEADER = """<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/">首頁</a>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">研究<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/research/">個股 DD</a>
          <a href="/id/">產業深度 ID</a>
          <a href="/id/tier_matrix.html">🎯 Tier Matrix</a>
        </div>
      </div>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">市場<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/briefing/">每日簡報</a>
          <a href="/weekly/">週報</a>
          <a href="/earnings/">財報分析</a>
          <a href="/markets.html">Markets</a>
          <a href="/sectors.html">Sectors</a>
          <a href="/six-state/">六狀態機</a>
        </div>
      </div>
      <div class="imq-dd active">
        <button type="button" class="imq-dd-btn">工具<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/backtest/" class="active">量化回測</a>
          <a href="/qgm/">QGM 美股</a>
          <a href="/qgm-tw/">QGM 台股</a>
          <a href="/screener.html">Screener 美股</a>
          <a href="/screener-tw.html">Screener 台股</a>
        </div>
      </div>
      <a href="/mental-models/">🧠 心智模型</a>
      <a href="/how-to.html">📘 使用說明</a>
    </nav>
  </div>
</header>
<script>(function(){document.querySelectorAll('.imq-dd-btn').forEach(function(btn){btn.addEventListener('click',function(e){e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){if(d!==dd)d.classList.remove('open')});dd.classList.toggle('open')})});document.addEventListener('click',function(e){if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){d.classList.remove('open')})});})();</script>"""


def make_yearly_table(yearly_returns: list, name: str, color: str) -> str:
    """Build the yearly returns table HTML."""
    rows = []
    for i, year in enumerate(YEARS):
        v = yearly_returns[i] if i < len(yearly_returns) else None
        if v is None:
            cell = '<td>—</td>'
        else:
            color_style = "color:var(--red)" if v < 0 else ("color:var(--green);font-weight:600" if v > 25 else "")
            sign = "+" if v >= 0 else ""
            cell = f'<td style="{color_style}">{sign}{v:.2f}%</td>'
        rows.append(f'<tr><td>{year}</td>{cell}</tr>')

    return f"""
<table>
<thead><tr><th>Year</th><th style="color:{color}">{name}</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
"""


def make_kpi_pair(m20: dict, m10: dict) -> str:
    """Build the side-by-side 20Y/10Y KPI cards."""
    def kpi_block(m: dict, label: str) -> str:
        cagr_color = "pos" if m["cagr"] > 0 else "neg"
        return f"""
<div>
<h4>{label}</h4>
<div class="kpi-grid" style="grid-template-columns:repeat(2,1fr);gap:.5rem">
  <div class="kpi"><div class="label">CAGR</div><div class="value {cagr_color}">{'+' if m['cagr']>=0 else ''}{m['cagr']:.2f}%</div></div>
  <div class="kpi"><div class="label">MDD</div><div class="value">{m['mdd']:.2f}%</div></div>
  <div class="kpi"><div class="label">Sharpe</div><div class="value neu">{m['sharpe']:.2f}</div></div>
  <div class="kpi"><div class="label">Sortino</div><div class="value neu">{m['sortino']:.2f}</div></div>
  <div class="kpi"><div class="label">Calmar</div><div class="value">{m['calmar']:.2f}</div></div>
  <div class="kpi"><div class="label">Vol</div><div class="value">{m['vol']:.2f}%</div></div>
  <div class="kpi"><div class="label">交易次數</div><div class="value">{m['trades']}</div></div>
  <div class="kpi"><div class="label">期末資產</div><div class="value">{m['final']}</div></div>
</div>
</div>
"""
    return f'<div class="kpi-pair">{kpi_block(m20, "20 年 (2006-2026)")}{kpi_block(m10, "10 年 (2016-2026)")}</div>'


def build_page(slug: str, system: dict) -> str:
    name = system["name"]
    subtitle = system["subtitle"]
    color = system["color"]
    rules = system["rules"]
    m20 = system["m20"]
    m10 = system["m10"]
    yearly = system["yearly"]
    verdict = system["verdict"]
    extra_title, extra_html = system["extra_section"]

    yearly_table = make_yearly_table(yearly, name, color)
    kpi_pair = make_kpi_pair(m20, m10)
    toggle = make_toggle(slug)
    h = system["hero"]
    hero = f"""<div class="hero" style="border-color:{h['border']}">
  <div class="hero-top" style="background:{h['bg']};border-bottom-color:{h['border']}">
    <span class="verdict-tag" style="background:{h['tag_bg']}">{h['tag']}</span>
    <h2>{h['title']}</h2>
    <p>{h['body']}</p>
  </div>
</div>"""

    # Yearly returns as JS array
    yearly_js = "[" + ",".join("null" if v is None else str(v) for v in yearly) + "]"

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>{CSS}</style>
</head>
<body>
{NAV_HEADER}

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / {name}</div>
    <h1 style="color:{color}">{name}</h1>
    <div class="sub">{subtitle}</div>
    {toggle}
  </div>
</div>

<div class="container">

{hero}

<!-- ===== 1. 策略規則 ===== -->
<div class="section">
<h2 class="section-title">1. 策略規則</h2>
<div class="card">
  <p style="font-size:.92rem;color:#374151;line-height:1.75">{rules}</p>
</div>
</div>

<!-- ===== 2. 績效摘要 ===== -->
<div class="section">
<h2 class="section-title">2. 績效摘要</h2>
{kpi_pair}

<div class="verdict">
  <strong>結論:</strong> {verdict}
</div>
</div>

<!-- ===== 3. 淨值曲線 ===== -->
<div class="section">
<h2 class="section-title">3. 淨值曲線</h2>
<div class="chart-card">
  <div class="chart-wrap"><canvas id="chart-nav"></canvas></div>
</div>
</div>

<!-- ===== 4. 回撤 ===== -->
<div class="section">
<h2 class="section-title">4. 回撤分析</h2>
<div class="chart-card">
  <div class="chart-wrap-sm"><canvas id="chart-dd"></canvas></div>
</div>
</div>

<!-- ===== 5. 逐年報酬 ===== -->
<div class="section">
<h2 class="section-title">5. 逐年報酬</h2>
<div class="chart-card">
  <div class="chart-wrap"><canvas id="chart-yearly"></canvas></div>
</div>
{yearly_table}
</div>

<!-- ===== 6. 系統特有分析 ===== -->
<div class="section">
<h2 class="section-title">6. {extra_title}</h2>
{extra_html}
</div>

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; {name} 詳細回測 &middot; 真實 yfinance 資料 &middot; 僅供研究參考
  </div>
</footer>

<script>
var YEARS={YEARS};
var RET={yearly_js};
var SPY=[13.81,3.69,-36.81,25.94,12.78,0.00,13.47,29.93,11.39,-0.73,9.54,19.42,-6.24,28.88,16.26,26.89,-19.44,24.23,23.31,21.50,1.20];
var QQQ=[6.93,18.67,-41.73,53.47,19.22,2.70,16.82,33.27,19.18,7.09,5.89,31.60,-1.04,37.96,47.58,26.63,-32.58,53.81,28.73,23.88,-3.50];

function toNAV(ret){{
  var nav=[1];var v=1;
  for(var i=0;i<ret.length;i++){{
    if(ret[i]===null){{nav.push(null)}}
    else{{v=v*(1+ret[i]/100);nav.push(v)}}
  }}
  return nav;
}}
function toDD(nav){{
  var dd=[];var peak=0;
  for(var i=0;i<nav.length;i++){{
    if(nav[i]===null){{dd.push(null);continue}}
    if(nav[i]>peak)peak=nav[i];
    dd.push((nav[i]/peak-1)*100);
  }}
  return dd;
}}
var LABELS=['2005'].concat(YEARS.map(String));
var NAV_SYS=toNAV(RET);
var NAV_SPY=toNAV(SPY);
var NAV_QQQ=toNAV(QQQ);
var DD_SYS=toDD(NAV_SYS);
var DD_SPY=toDD(NAV_SPY);
var DD_QQQ=toDD(NAV_QQQ);

Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;

new Chart(document.getElementById('chart-nav'),{{
  type:'line',
  data:{{labels:LABELS,datasets:[
    {{label:'{name}',data:NAV_SYS,borderColor:'{color}',borderWidth:2.6,pointRadius:0,pointHoverRadius:4,tension:0.15,spanGaps:false}},
    {{label:'QQQ B&H',data:NAV_QQQ,borderColor:'#1565c0',borderWidth:1.6,borderDash:[6,3],pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'SPY B&H',data:NAV_SPY,borderColor:'#757575',borderWidth:1.6,borderDash:[6,3],pointRadius:0,pointHoverRadius:3,tension:0.15}}
  ]}},
  options:{{
    responsive:true,maintainAspectRatio:false,
    interaction:{{mode:'index',intersect:false}},
    plugins:{{
      legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:14,font:{{size:11}}}}}},
      tooltip:{{mode:'index',intersect:false,callbacks:{{label:function(ctx){{
        if(ctx.parsed.y===null)return null;
        return ctx.dataset.label+': $'+(ctx.parsed.y*1000000/1e6).toFixed(2)+'M';
      }}}}}}
    }},
    scales:{{
      x:{{grid:{{color:'rgba(0,0,0,0.04)'}},ticks:{{font:{{size:10}}}}}},
      y:{{type:'logarithmic',grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return '$'+v.toFixed(1)+'M'}},font:{{size:10}}}}}}
    }}
  }}
}});

new Chart(document.getElementById('chart-dd'),{{
  type:'line',
  data:{{labels:LABELS,datasets:[
    {{label:'{name}',data:DD_SYS,borderColor:'{color}',backgroundColor:'{color}1f',borderWidth:1.6,fill:'origin',pointRadius:0,pointHoverRadius:3,tension:0.15,spanGaps:false}},
    {{label:'QQQ',data:DD_QQQ,borderColor:'#1565c0',backgroundColor:'rgba(21,101,192,0.10)',borderWidth:1.4,fill:'origin',pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'SPY',data:DD_SPY,borderColor:'#757575',backgroundColor:'rgba(117,117,117,0.10)',borderWidth:1.4,fill:'origin',pointRadius:0,pointHoverRadius:3,tension:0.15}}
  ]}},
  options:{{
    responsive:true,maintainAspectRatio:false,
    interaction:{{mode:'index',intersect:false}},
    plugins:{{
      legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10,font:{{size:10}}}}}},
      tooltip:{{mode:'index',intersect:false,callbacks:{{label:function(ctx){{
        if(ctx.parsed.y===null)return null;
        return ctx.dataset.label+': '+ctx.parsed.y.toFixed(2)+'%';
      }}}}}}
    }},
    scales:{{
      x:{{grid:{{display:false}},ticks:{{font:{{size:10}}}}}},
      y:{{grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}
    }}
  }}
}});

new Chart(document.getElementById('chart-yearly'),{{
  type:'bar',
  data:{{
    labels:YEARS.map(String),
    datasets:[
      {{label:'{name}',data:RET,backgroundColor:RET.map(function(v){{return v===null?'transparent':v>=0?'{color}cc':'{color}55'}}),borderColor:'{color}',borderWidth:1,borderRadius:2}},
      {{label:'SPY B&H',data:SPY,backgroundColor:SPY.map(function(v){{return v>=0?'rgba(117,117,117,0.65)':'rgba(117,117,117,0.30)'}}),borderColor:'#757575',borderWidth:1,borderRadius:2}}
    ]
  }},
  options:{{
    responsive:true,maintainAspectRatio:false,
    interaction:{{mode:'index',intersect:false}},
    plugins:{{
      legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'rect',padding:14,font:{{size:11}}}}}},
      tooltip:{{mode:'index',intersect:false,callbacks:{{label:function(ctx){{
        if(ctx.parsed.y===null)return null;
        return ctx.dataset.label+': '+(ctx.parsed.y>0?'+':'')+ctx.parsed.y.toFixed(2)+'%';
      }}}}}}
    }},
    scales:{{
      x:{{grid:{{display:false}},ticks:{{font:{{size:10}}}}}},
      y:{{grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}
    }}
  }}
}});
</script>
</body>
</html>
"""


SLUG_TO_DIR = {
    "dual": "dual_track",
    "gem": "gem",
}


def main():
    for slug, system in SYSTEMS.items():
        out_dir = OUT / SLUG_TO_DIR.get(slug, slug)
        out_dir.mkdir(exist_ok=True)
        out_file = out_dir / "index.html"
        html = build_page(slug, system)
        out_file.write_text(html, encoding="utf-8")
        print(f"  Wrote {out_file.relative_to(OUT)}  ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
