"""
One-shot generator for 4 individual system pages:
  /backtest/dual_track/  - 雙軌多空
  /backtest/long_track/  - Long Track Only
  /backtest/six_state/   - 六狀態機
  /backtest/gem/         - GEM 雙動能

Run from anywhere; outputs each <slug>/index.html.
Re-run to regenerate.
"""
from pathlib import Path

OUT = Path(__file__).parent

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
header{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.75rem 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.hdr-inner{display:flex;align-items:center;justify-content:space-between}
header .logo{font-size:1.15rem;font-weight:700;color:#fff;letter-spacing:-.02em}
header .logo span{color:#3b82f6}
header nav a{color:rgba(255,255,255,.7);margin-left:1.5rem;font-size:.85rem;font-weight:500;
             padding-bottom:4px;border-bottom:2px solid transparent;transition:all .2s}
header nav a:hover{color:#fff;text-decoration:none;border-bottom-color:rgba(255,255,255,.4)}
header nav a.active{color:#fff;border-bottom-color:#3b82f6}
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
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);
       text-align:center;padding:1.25rem 0;font-size:.78rem}
@media(max-width:768px){
  .kpi-grid{grid-template-columns:repeat(2,1fr)}
  .kpi-pair{grid-template-columns:1fr}
  .hdr-inner{flex-direction:column;gap:.5rem}
  header nav a{margin-left:0;margin-right:1rem}
  table{font-size:.78rem}th,td{padding:.45rem .5rem}
}
"""

# Toggle pill — order: comparison views first, then individual systems
TOGGLE_LINKS = [
    ("/backtest/", "20 年", "20y"),
    ("/backtest/10y/", "10 年", "10y"),
    ("/backtest/criteria/", "評估標準", "criteria"),
    ("/backtest/dual_track/", "雙軌多空", "dual"),
    ("/backtest/long_track/", "Long Track", "long"),
    ("/backtest/six_state/", "六狀態機", "six_state"),
    ("/backtest/gem/", "GEM", "gem"),
    ("/backtest/slope_filter/", "W52 斜率", "slope"),
    ("/backtest/short_system/", "做空 (失敗)", "short"),
    ("/backtest/turtle/", "🐢 Turtle", "turtle"),
]


def make_toggle(active: str) -> str:
    parts = []
    for url, label, key in TOGGLE_LINKS:
        cls = "active" if key == active else ""
        # Special styling
        style = ""
        if cls != "active":
            if key == "short":
                style = ' style="color:#dc2626"'
            elif key == "turtle":
                style = ' style="color:#0f766e"'
        parts.append(f'<a href="{url}" class="{cls}"{style}>{label}</a>')
    return '<div class="toggle-pill">' + "".join(parts) + '</div>'


# Years used in yearly returns arrays
YEARS = list(range(2006, 2027))

# ===== System data =====
# Each system has: name, slug, color, 20y/10y metrics, yearly returns, etc.

SYSTEMS = {
    "dual": {
        "name": "雙軌多空",
        "subtitle": "50/50 SPY/QQQ · Short Track 70% + Long Track 30%",
        "color": "#7c3aed",
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
    "long": {
        "name": "Long Track Only",
        "subtitle": "50/50 SPY/QQQ · 只用週線長線軌 · 推薦配置",
        "color": "#059669",
        "rules": """
            從 v7 Ch12 雙軌系統中<strong>移除短線軌</strong>,只保留長線軌:<br>
            週線均線 W52 / W104 / W250,斜率 lookback N=4 週,出場確認 N=1 (週線收盤跌破 W52 即出場)。<br>
            進場條件: 週線收盤 &gt; W52, W104, W250 且 W104, W250 斜率 &gt; 0 (score == 5)。<br>
            50/50 配置 SPY 和 QQQ。<strong>實際 20 年從未觸發做空訊號</strong>,等同只做多策略。
        """,
        "m20": {"cagr": 10.95, "mdd": -19.99, "sharpe": 0.86, "sortino": 1.02, "calmar": 0.55, "vol": 13.17, "trades": 37, "final": "$5.00M"},
        "m10": {"cagr": 13.06, "mdd": -18.82, "sharpe": 0.97, "sortino": 1.16, "calmar": 0.69, "vol": 12.96, "trades": 21, "final": "$3.42M"},
        "yearly": [None, None, None, None, 4.47, -9.51, 8.64, 31.26, 17.36, -5.19, 3.45, 26.09, -1.78, 20.49, 25.78, 30.01, -14.72, 8.71, 26.74, 17.03, -5.07],
        "verdict": """
            <strong>本站唯一通過所有合格 + 優秀 + 穩健標準的系統。</strong>
            CAGR 10.95%、Sharpe 0.86、Calmar 0.55,且 Walk-forward 與參數敏感度檢驗都通過。
            10 年視窗下 Sharpe 進一步提升到 0.97,Calmar 0.69,證明這個系統在不同時期都穩定。
            年均交易 ~2 筆,平均持有 255 天,交易成本極低。
        """,
        "extra_section": ("穩健性驗證", """
<table>
<thead><tr><th>檢驗</th><th>標準</th><th>結果</th><th>狀態</th></tr></thead>
<tbody>
<tr><td>Walk-Forward</td><td>Sharpe 差距 &lt; 0.3</td><td>0.22 (訓練 0.71 / 驗證 0.94)</td><td><span class="tag tag-best">通過</span></td></tr>
<tr><td>參數敏感度</td><td>CAGR 極差 &lt; 3pp</td><td>0.44pp (W48-W56 / W100-W112 / W240-W260)</td><td><span class="tag tag-best">通過</span></td></tr>
<tr><td>年度穩定性</td><td>無連虧兩年 / 無 +50% 年</td><td>最長連虧 1 年 / 最好年 +31%</td><td><span class="tag tag-best">通過</span></td></tr>
<tr><td>正報酬比</td><td>&gt; 60%</td><td>71% (12 / 17 年)</td><td><span class="tag tag-best">通過</span></td></tr>
</tbody>
</table>
        """),
    },
    "six_state": {
        "name": "六狀態機",
        "subtitle": "QQQ + SMH + BIL · 三狀態 + Grid 加碼層 · v7 Ch8",
        "color": "#d32f2f",
        "rules": """
            v7 Ch8 簡化版 (路徑 B)。三主狀態 + Grid 加碼層:<br>
            <strong>S1 正常巡航</strong>: 95% 股票 (QQQ 75% + SMH 20% + BIL 5%)<br>
            <strong>S2 防守模式</strong>: 47.5% 股票 (QQQ 37.5% + SMH 10% + BIL 52.5%)<br>
            <strong>S5 趨勢重啟</strong>: 每週股票曝險 +15% 直到 95% 回到 S1<br>
            <strong>Grid 加碼</strong>: S2 期間,QQQ 跌破 MA104/200/156 觸發 +10%/+15%/+22.5% 加碼。<br>
            所有 MA 用週線收盤計算,Grid 判斷用上週五已知 MA 值避免 look-ahead。
        """,
        "m20": {"cagr": 15.14, "mdd": -40.35, "sharpe": 0.83, "sortino": 1.10, "calmar": 0.38, "vol": 19.36, "trades": 68, "final": "$17.40M"},
        "m10": {"cagr": 21.24, "mdd": -29.41, "sharpe": 1.03, "sortino": 1.36, "calmar": 0.72, "vol": 19.33, "trades": 36, "final": "$6.88M"},
        "yearly": [1.54, 15.38, -27.86, 43.31, 16.86, -8.14, 11.56, 30.17, 21.50, 4.58, 8.47, 31.57, -2.39, 35.38, 40.25, 31.11, -25.29, 56.96, 30.20, 26.96, -0.99],
        "verdict": """
            <strong>進攻型系統,但 MDD 不合格。</strong> 20Y CAGR 15.14% 漂亮,
            但 -40.35% 回撤超出個人可接受範圍。10Y 視窗下 CAGR 衝到 21.24% (進入「可疑」區),
            Sharpe 1.03 + Calmar 0.72 看似優秀,但 21% CAGR 加上未做 walk-forward 驗證,
            <strong>有過擬合疑慮</strong>。需要外推樣本驗證才能採信。
        """,
        "extra_section": ("狀態轉換 + Grid 統計 (20年)", """
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
<div class="card">
  <h3>狀態轉換次數</h3>
  <table>
  <tbody>
  <tr><td>S1→S2 進入防守</td><td style="font-weight:600">11 次</td></tr>
  <tr><td>S2→S5 趨勢重啟</td><td style="font-weight:600">18 次</td></tr>
  <tr><td>S5→S1 完成恢復</td><td style="font-weight:600;color:var(--green)">11 次</td></tr>
  <tr><td>S5→S2 恢復失敗</td><td style="font-weight:600;color:var(--red)">7 次</td></tr>
  </tbody>
  </table>
</div>
<div class="card">
  <h3>Grid 觸發 + 時間分布</h3>
  <table>
  <tbody>
  <tr><td>Grid #1+#2 (MA104)</td><td style="font-weight:600">8 次</td></tr>
  <tr><td>Grid #3 (MA200)</td><td style="font-weight:600">1 次</td></tr>
  <tr><td>Grid #4 (MA156)</td><td style="font-weight:600">3 次</td></tr>
  <tr style="border-top:2px solid var(--border)"><td>S1 巡航時間</td><td>81.8%</td></tr>
  <tr><td>S2 防守時間</td><td>15.4%</td></tr>
  <tr><td>S5 過渡時間</td><td>2.8%</td></tr>
  </tbody>
  </table>
</div>
</div>

<h3 class="section-title" style="margin-top:1.25rem">關鍵壓力事件</h3>
<div class="event-card">
  <div class="ev-name">2008 GFC <span class="tag tag-best" style="margin-left:.5rem">+16pp vs B&amp;H</span></div>
  <div class="ev-detail">系統 -16.97% vs QQQ B&amp;H -33.18%。S2 + G12 + G4 觸發。2009-06 以 80% 曝險快速恢復。</div>
</div>
<div class="event-card">
  <div class="ev-name">2011 歐債 <span class="tag tag-fail" style="margin-left:.5rem">-6.6pp vs B&amp;H</span></div>
  <div class="ev-detail">系統 -7.89% vs QQQ B&amp;H -1.33%。S2/S5 來回 whipsaw 4 次。</div>
</div>
<div class="event-card">
  <div class="ev-name">2020 COVID <span class="tag tag-fail" style="margin-left:.5rem">-3.7pp vs B&amp;H</span></div>
  <div class="ev-detail">系統 -11.15% vs QQQ B&amp;H -7.43%。S2 進入太晚 (3/20),G12+G4 觸發,但 S5→S1 太快。</div>
</div>
<div class="event-card">
  <div class="ev-name">2022 通膨熊 <span class="tag tag-best" style="margin-left:.5rem">+6.1pp vs B&amp;H</span></div>
  <div class="ev-detail">系統 -24.32% vs QQQ B&amp;H -30.46%。三層 Grid 全觸發。2023-02 以 95% 曝險直接回 S1。</div>
</div>
        """),
    },
    "gem": {
        "name": "GEM 雙動能",
        "subtitle": "SPY / ACWX / AGG · 月度切換 · Gary Antonacci",
        "color": "#f57c00",
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
<header>
  <div class="container hdr-inner">
    <a class="logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav><a href="/">首頁</a> <a href="/briefing/">每日簡報</a> <a href="/weekly/">週報</a> <a href="/backtest/" class="active">回測</a></nav>
  </div>
</header>

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / {name}</div>
    <h1 style="color:{color}">{name}</h1>
    <div class="sub">{subtitle}</div>
    {toggle}
  </div>
</div>

<div class="container">

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


def main():
    for slug, system in SYSTEMS.items():
        out_dir = OUT / slug if slug != "long" else OUT / "long_track"
        # Map slug to output dir
        if slug == "dual":
            out_dir = OUT / "dual_track"
        elif slug == "long":
            out_dir = OUT / "long_track"
        elif slug == "six_state":
            out_dir = OUT / "six_state"
        elif slug == "gem":
            out_dir = OUT / "gem"
        out_dir.mkdir(exist_ok=True)
        out_file = out_dir / "index.html"
        html = build_page(slug, system)
        out_file.write_text(html, encoding="utf-8")
        print(f"  Wrote {out_file.relative_to(OUT)}  ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
