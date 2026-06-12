"""
Generator for /backtest/criteria/ — system evaluation framework v2 (2026-06).

Redesign rationale:
  * The threshold bands survived the 2026-06 warmup corrections — systems
    moved across the pass line exactly as they should (Long Track lost its
    "excellent" badge, six_state failed MDD marginally), which validates the
    framework.  Bands are kept as-is.
  * What rotted was the application section: stale numbers and verdicts
    ("six_state未驗證" predates its full robustness audit).  The scoreboard
    is now generated from pinned corrected numbers.
  * New section: methodology discipline rules learned in the 2026-06 cycle
    (denominator integrity, in-sample discipline, H1/H2 sub-period windows,
    realistic cash assumptions, qualified ≠ adopted).

Update SYSTEMS below when a system page changes, then re-run:
    python3 _build_criteria.py
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

OUT = Path(__file__).parent / "criteria" / "index.html"

# Minimum qualification thresholds (unchanged from v1)
TH = {"cagr": 8.0, "mdd": -35.0, "sharpe": 0.5, "calmar": 0.3}

# (name, url, cagr, mdd, sharpe, calmar, years_ok, note)  — 20Y, refreshed 2026-06-12
SYSTEMS_20Y = [
    ("Long Track Only", "/backtest/long_track/", 9.72, -20.08, 0.81, 0.48, True, ""),
    ("LTO QQQ only", "/backtest/long_track_qqq/", 10.80, -25.37, 0.75, 0.43, True, ""),
    ("Ensemble E3", "/backtest/long_track_ensemble/", 11.47, -21.15, 0.89, 0.54, True, "2026-06-11 採用 · OOS"),
    ("LT SMH/QQQ E3", "/backtest/long_track_smh/", 15.30, -26.93, 0.90, 0.57, True, "2026-06-12 採用 · OOS"),
    ("W52 斜率濾網", "/backtest/slope_filter/", 10.16, -20.05, 0.92, 0.51, True, "warmup 完整(資料自 2000)"),
    ("GEM 雙動能", "/backtest/gem/", 8.95, -21.54, 0.57, 0.42, True, ""),
    ("六狀態機 v1.1", "/backtest/six_state/", 14.77, -35.80, 0.86, 0.41, True, ""),
    ("六狀態機 v1.0r1 實盤", "/backtest/six_state_v1r1/", 14.58, -49.29, 0.81, 0.30, True, "壓力路徑 -77%"),
    ("雙軌多空", "/backtest/dual_track/", 4.35, -38.72, 0.37, 0.11, True, "已否決 · 2026-06-12 修正重檢"),
    ("🐢 Turtle(多資產)", "/backtest/turtle/", 22.48, -38.12, 0.73, 0.59, True, "CAGR 進可疑帶"),
    ("📈 Clenow(多資產)", "/backtest/clenow/", 13.28, -44.11, 0.69, 0.30, True, ""),
]

# (name, cagr, mdd, sharpe, calmar, verdict)  — 10Y, refreshed 2026-06-12
SYSTEMS_10Y = [
    ("LT SMH/QQQ E3", 26.55, -26.93, 1.23, 0.99, "warn", "CAGR 進可疑帶(>20%)— H2 半導體 regime"),
    ("六狀態機 v1.1", 22.40, -28.49, 1.12, 0.79, "warn", "CAGR 進可疑帶(>20%)— 無 2008 的視窗"),
    ("LTO QQQ only", 18.81, -25.18, 1.10, 0.75, "good", "進攻型優秀"),
    ("Ensemble E3", 16.29, -21.15, 1.12, 0.77, "good", "優秀(樣本內)"),
    ("Long Track Only", 15.47, -18.75, 1.11, 0.83, "good", "優秀"),
    ("W52 斜率濾網", 11.04, -20.05, 0.82, 0.55, "pass", "合格(穩定)"),
    ("GEM 雙動能", 9.85, -21.54, 0.54, 0.46, "pass", "合格"),
    ("雙軌多空", 9.26, -19.61, 0.73, 0.47, "fail", "10 年窗口仍墊底;全期已否決"),
    ("QQQ Buy & Hold", 21.71, -35.12, 0.99, 0.62, "bh", "基準"),
    ("SPY Buy & Hold", 15.35, -33.72, 0.89, 0.46, "bh", "基準"),
]


def check(v, th, geq=True):
    ok = (v >= th) if geq else (v <= th)
    return ok


def cell(ok, text):
    color = "var(--green)" if ok else "var(--red)"
    mark = "✓" if ok else "✗"
    return f'<td style="color:{color};font-weight:600">{mark} {text}</td>'


def scoreboard_rows() -> str:
    rows = ""
    for name, url, cagr, mdd, sharpe, calmar, yrs, note in SYSTEMS_20Y:
        c1 = check(cagr, TH["cagr"])
        c2 = mdd >= TH["mdd"]
        c3 = check(sharpe, TH["sharpe"])
        c4 = check(calmar, TH["calmar"])
        n_pass = sum([c1, c2, c3, c4, yrs])
        qualified = n_pass == 5
        if qualified and "採用" in note:
            verdict = '<span class="tag tag-best">合格 · 已採用</span>'
        elif qualified:
            verdict = '<span class="tag tag-best">合格</span>'
        else:
            verdict = f'<span class="tag tag-fail">不合格 ({n_pass}/5)</span>'
        note_html = f'<br><span style="font-size:.72rem;color:var(--muted)">{note}</span>' if note else ""
        rows += (f'<tr><td><strong><a href="{url}">{name}</a></strong>{note_html}</td>'
                 + cell(c1, f"{cagr:+.2f}%") + cell(c2, f"{mdd:.2f}%")
                 + cell(c3, f"{sharpe:.2f}") + cell(c4, f"{calmar:.2f}")
                 + cell(yrs, "20y")
                 + f"<td>{verdict}</td></tr>\n")
    return rows


def table10_rows() -> str:
    tagmap = {"good": "tag-best", "pass": "tag-pass", "warn": "tag-warn",
              "fail": "tag-fail", "bh": "tag-pass"}
    rows = ""
    for name, cagr, mdd, sharpe, calmar, kind, verdict in SYSTEMS_10Y:
        style = ' style="background:#f9fafb"' if kind == "bh" else ""
        rows += (f'<tr{style}><td><strong>{name}</strong></td>'
                 f'<td>{cagr:+.2f}%</td><td>{mdd:.2f}%</td>'
                 f'<td>{sharpe:.2f}</td><td>{calmar:.2f}</td>'
                 f'<td><span class="tag {tagmap[kind]}">{verdict}</span></td></tr>\n')
    return rows


def render() -> str:
    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%TOGGLE%": make_toggle("criteria"),
        "%SCOREBOARD%": scoreboard_rows(),
        "%TABLE10%": table10_rows(),
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
<title>系統評估標準 v2 | InvestMQuest Research</title>
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
.tag-warn{background:var(--amber-bg);color:var(--amber-text);border:1px solid var(--amber-border)}
.tag-fail{background:var(--red-bg);color:var(--red-text);border:1px solid var(--red-border)}
.tag-pass{background:#f3f4f6;color:#374151;border:1px solid #d1d5db}
.hero{margin:1.25rem 0;border:1px solid #bfdbfe;border-radius:12px;overflow:hidden;background:var(--card)}
.hero-top{background:linear-gradient(135deg,#eff6ff 0%,#f0f7ff 100%);padding:1.4rem 1.6rem;border-bottom:1px solid #bfdbfe}
.hero-top .verdict-tag{display:inline-block;background:var(--brand);color:#fff;font-size:.74rem;font-weight:700;
                       letter-spacing:.05em;padding:.25rem .7rem;border-radius:99px;margin-bottom:.5rem}
.hero-top h2{font-size:1.35rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.35rem}
.hero-top p{font-size:.92rem;color:#374151;max-width:60rem}
.note{background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px;
      padding:.85rem 1.1rem;font-size:.84rem;color:var(--amber-text);margin:1rem 0}
.band{display:flex;align-items:center;gap:.8rem;padding:.45rem 0;border-bottom:1px dashed var(--border);font-size:.85rem}
.band:last-child{border-bottom:none}
.band .b-label{width:70px;font-weight:600;flex-shrink:0}
.band .b-range{width:120px;color:var(--muted);font-variant-numeric:tabular-nums;flex-shrink:0}
.band .b-bar{height:8px;border-radius:4px;flex-shrink:0}
.band .b-desc{font-size:.8rem;color:#374151}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.crit-box{background:var(--card);border:2px solid var(--brand);border-radius:8px;padding:1.1rem 1.3rem}
.crit-box.elite{border-color:var(--green)}
.crit-box h3{font-size:.95rem;font-weight:700;margin-bottom:.6rem;color:var(--brand)}
.crit-box.elite h3{color:var(--green-text)}
.crit-box ul{list-style:none}
.crit-box li{padding:.3rem 0;font-size:.85rem;color:#374151;border-bottom:1px dashed #e5e7eb}
.crit-box li:last-child{border-bottom:none}
.crit-box li::before{content:'✓ ';color:var(--brand);font-weight:700;margin-right:.3rem}
.crit-box.elite li::before{color:var(--green)}
.issue-list{font-size:.88rem;color:#374151;padding-left:1.2rem;line-height:1.9}
.verdict{background:var(--brand-light);border-left:4px solid var(--brand);
         padding:1rem 1.4rem;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.92rem;line-height:1.7}
.verdict strong{color:var(--brand)}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);
       text-align:center;padding:1.25rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){
  .two-col{grid-template-columns:1fr}
  table{font-size:.76rem}th,td{padding:.4rem .45rem}
  .band{flex-wrap:wrap}
}
</style>
</head>
<body>
%NAV%

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / 系統評估標準</div>
    <h1>系統評估標準 v2</h1>
    <div class="sub">指標門檻 · 方法論紀律 · 全系統合格對照 · 2026-06 修訂</div>
    %TOGGLE%
  </div>
</div>

<div class="container">

<!-- ===== HERO ===== -->
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag">📐 框架 v2 — 2026-06 修訂</span>
    <h2>門檻不變,紀律升級 — 這套標準剛通過了它自己的壓力測試</h2>
    <p>2026-06 的 warmup 修正讓兩個系統的 headline 數字失效(Long Track 10.95% → 9.59%、LTO QQQ 12.33% → 10.63%),
       合格名單隨之變動:Long Track 從「優秀」降為「合格」、六狀態機 v1.1 在 MDD 門檻上以 0.8pp 之差出局。
       <strong>門檻有鑑別力,所以維持不變;這次修訂把修正過程中學到的五條方法論紀律成文化</strong> —
       分母完整性、樣本內紀律、子期間雙視窗、現實假設、合格 ≠ 採用(採用 = 有記錄的決策 + 重審條件,
       Ensemble E3 與 LT SMH/QQQ 即循此流程於 2026-06-11 採用)— 並把套用結果改為對照修正後數據的計分板。</p>
  </div>
</div>

<!-- ===== 1. THRESHOLDS ===== -->
<div class="section">
<h2 class="section-title">1. 五大指標門檻(維持 v1)</h2>
<div class="section-sub">業界基準 + 個人判斷框架。「可疑」帶與「不及格」帶同樣重要 — 太好的數字是過擬合警報。</div>

<div class="two-col">
<div class="card">
<h3>CAGR · 年化報酬</h3>
<div class="band"><span class="b-label">不及格</span><span class="b-range">&lt; 6%</span><span class="b-bar" style="width:40px;background:var(--red)"></span><span class="b-desc">輸給被動 60/40</span></div>
<div class="band"><span class="b-label">及格</span><span class="b-range">8 ~ 12%</span><span class="b-bar" style="width:80px;background:#9ca3af"></span><span class="b-desc">接近大盤、回撤須顯著更淺</span></div>
<div class="band"><span class="b-label">良好</span><span class="b-range">12 ~ 15%</span><span class="b-bar" style="width:120px;background:var(--brand)"></span><span class="b-desc">有明確 alpha</span></div>
<div class="band"><span class="b-label">優秀</span><span class="b-range">15 ~ 20%</span><span class="b-bar" style="width:160px;background:var(--green)"></span><span class="b-desc">頂級主動水準</span></div>
<div class="band"><span class="b-label">可疑</span><span class="b-range">&gt; 20%</span><span class="b-bar" style="width:200px;background:var(--amber)"></span><span class="b-desc">⚠ 過擬合 / regime 集中警報</span></div>
</div>

<div class="card">
<h3>MDD · 最大回撤</h3>
<div class="band"><span class="b-label">優秀</span><span class="b-range">&gt; -15%</span><span class="b-bar" style="width:40px;background:var(--green)"></span><span class="b-desc">心理上幾乎無感</span></div>
<div class="band"><span class="b-label">良好</span><span class="b-range">-15 ~ -25%</span><span class="b-bar" style="width:80px;background:var(--brand)"></span><span class="b-desc">可長期持有</span></div>
<div class="band"><span class="b-label">及格</span><span class="b-range">-25 ~ -35%</span><span class="b-bar" style="width:120px;background:#9ca3af"></span><span class="b-desc">需要強大紀律</span></div>
<div class="band"><span class="b-label">不及格</span><span class="b-range">-35 ~ -50%</span><span class="b-bar" style="width:160px;background:var(--red)"></span><span class="b-desc">多數人會在谷底棄船</span></div>
<div class="band"><span class="b-label">不可接受</span><span class="b-range">&lt; -50%</span><span class="b-bar" style="width:200px;background:#7f1d1d"></span><span class="b-desc">與 B&amp;H 無異</span></div>
</div>

<div class="card">
<h3>Sharpe Ratio · 風險調整報酬</h3>
<div class="band"><span class="b-label">不及格</span><span class="b-range">&lt; 0.5</span><span class="b-bar" style="width:40px;background:var(--red)"></span><span class="b-desc">不如持有大盤</span></div>
<div class="band"><span class="b-label">及格</span><span class="b-range">0.5 ~ 0.8</span><span class="b-bar" style="width:80px;background:#9ca3af"></span><span class="b-desc">與 B&amp;H 相當</span></div>
<div class="band"><span class="b-label">良好</span><span class="b-range">0.8 ~ 1.2</span><span class="b-bar" style="width:120px;background:var(--brand)"></span><span class="b-desc">明確優於被動</span></div>
<div class="band"><span class="b-label">優秀</span><span class="b-range">1.2 ~ 2.0</span><span class="b-bar" style="width:160px;background:var(--green)"></span><span class="b-desc">機構級</span></div>
<div class="band"><span class="b-label">可疑</span><span class="b-range">&gt; 2.0</span><span class="b-bar" style="width:200px;background:var(--amber)"></span><span class="b-desc">⚠ 過擬合警報</span></div>
</div>

<div class="card">
<h3>Calmar Ratio · CAGR ÷ |MDD| <span class="tag tag-best" style="margin-left:.4rem">★ 最重要單一指標</span></h3>
<div class="band"><span class="b-label">不及格</span><span class="b-range">&lt; 0.3</span><span class="b-bar" style="width:40px;background:var(--red)"></span><span class="b-desc">報酬不抵回撤痛苦</span></div>
<div class="band"><span class="b-label">及格</span><span class="b-range">0.3 ~ 0.5</span><span class="b-bar" style="width:80px;background:#9ca3af"></span><span class="b-desc">接近 Buy &amp; Hold</span></div>
<div class="band"><span class="b-label">良好</span><span class="b-range">0.5 ~ 1.0</span><span class="b-bar" style="width:120px;background:var(--brand)"></span><span class="b-desc">風險效率有實質優勢</span></div>
<div class="band"><span class="b-label">優秀</span><span class="b-range">1.0 ~ 2.0</span><span class="b-bar" style="width:160px;background:var(--green)"></span><span class="b-desc">罕見,趨勢跟蹤大師級</span></div>
<div class="band"><span class="b-label">可疑</span><span class="b-range">&gt; 2.0</span><span class="b-bar" style="width:200px;background:var(--amber)"></span><span class="b-desc">⚠ 幾乎必為過擬合</span></div>
</div>
</div>

<div class="card">
<h3>輔助指標</h3>
<p style="font-size:.88rem;color:#374151;line-height:1.8">
<strong>Sortino</strong>:通常為 Sharpe 的 1.2~1.5 倍;顯著高於 Sharpe 代表獲利分布偏正(賺多虧少)。及格 ≥ 0.8、優秀 ≥ 1.2。<br>
<strong>期末資產</strong>:CAGR + 時間的衍生品,不是獨立指標。$1M 起始 20 年:10% → $6.7M(B&amp;H 水準)、12% → $9.6M、15% → $16.4M、20% → $38.3M(進入可疑區)。<br>
<strong>交易次數</strong>:過少(&lt;20 筆/20 年)→ 統計上難以證偽;過多 → 成本與執行負擔。趨勢系統合理區間約 25~100 筆/20 年。</p>
</div>
</div>

<!-- ===== 2. QUALIFICATION ===== -->
<div class="section">
<h2 class="section-title">2. 合格組合標準</h2>
<div class="section-sub">單一指標好不夠 — 必須同時通過全部門檻;任何一條未達標直接出局,無論其他指標多漂亮。</div>
<div class="two-col">
<div class="crit-box">
<h3>最低門檻(合格)</h3>
<ul>
<li>CAGR ≥ 8%</li>
<li>MDD ≥ -35%</li>
<li>Sharpe ≥ 0.5</li>
<li>Calmar ≥ 0.3</li>
<li>樣本期 ≥ 15 年(含至少 2 個熊市)</li>
<li>子期間穩健:H1 / H2 Calmar 皆 &gt; 0(v2 取代 walk-forward)</li>
<li>分母完整:CAGR 自模擬起點起算、MA warmup 補齊(v2 新增)</li>
</ul>
</div>
<div class="crit-box elite">
<h3>優秀標準(有商業價值)</h3>
<ul>
<li>CAGR ≥ 12%</li>
<li>MDD ≥ -25%</li>
<li>Sharpe ≥ 0.8</li>
<li>Calmar ≥ 0.5</li>
<li>Sortino ≥ 1.0</li>
<li>Sharpe &gt; 同期 B&amp;H(證明有 alpha)</li>
<li>子期間平衡:H1 / H2 Calmar 差距 &lt; 3 倍(v2 新增)</li>
</ul>
</div>
</div>
</div>

<!-- ===== 3. METHODOLOGY DISCIPLINE (NEW) ===== -->
<div class="section">
<h2 class="section-title">3. 方法論紀律(v2 新增 — 2026-06 修正週期的教訓)</h2>
<div class="card">
<ol class="issue-list">
  <li><strong>分母完整性</strong> — CAGR 必須從模擬起點起算;MA warmup 用上市起的資料補齊,不准讓指標 NaN 吃掉前幾年。
      教訓:舊 Long Track 頁的「20 年 +10.95%」分母實際只有 15.5 年(首筆交易起算),修正後 +9.59%;
      LTO QQQ 同病,+12.33% → +10.63%。<strong>凡是從首筆交易起算的歷史數字一律視為無效。</strong></li>
  <li><strong>樣本內紀律</strong> — 「優化」只做結構性消融(整個條件移除/加回),不做參數網格;
      消融發現只記錄為證據,不在樣本內改規則;headline 永遠留給忠實基準。
      案例:進場斜率冗餘(n=2 事件,未採用)、出場參數微調(實測更糟,否決)。</li>
  <li><strong>子期間雙視窗(H1 2006-2015 / H2 2016-至今)</strong> — 取代單一 walk-forward。
      任一子期間 Calmar 不到全期一半 → 標記 regime 集中。
      案例:LT SMH/QQQ 全期 Calmar 隨 SMH 權重單調上升,但 H1 在 50% 見頂、100% SMH 時只剩 0.16 —
      「更好的系統」其實是「更大的 regime 賭注」。</li>
  <li><strong>現實假設</strong> — 閒置資金計 SHY/BIL 利息(空倉時間集中在高利率熊市,影響不可忽略);
      單邊成本 7bps;訊號在所屬 bar 收盤確認並執行。</li>
  <li><strong>合格 ≠ 採用,採用 = 決策 + 條件</strong> — 數字全過只代表「值得進入決策」。
      案例:Ensemble E3 與 LT SMH/QQQ 數字皆全過,先以「未採用」記錄保留意見(樣本內證據、regime 集中),
      2026-06-11 經系統擁有者審視證據後決策採用 — 採用紀錄包含日期、保留意見與 OOS 重審/退場條件(見各頁)。
      原則不變:採用來自有記錄的決策,不來自漂亮的回測數字本身。</li>
</ol>
</div>
</div>

<!-- ===== 4. SCOREBOARD ===== -->
<div class="section">
<h2 class="section-title">4. 全系統合格對照(20 年 · 修正後數據)</h2>
<div class="section-sub">每格 = 是否通過該項最低門檻。多資產系統(Turtle/Clenow)資產池不同,僅供參照。數據截至日期見各系統頁。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>CAGR ≥ 8%</th><th>MDD ≥ -35%</th><th>Sharpe ≥ 0.5</th><th>Calmar ≥ 0.3</th><th>樣本 ≥ 15y</th><th>判定</th></tr></thead>
<tbody>
%SCOREBOARD%
</tbody>
</table>
<div class="takeaway">修正後的變動:<strong>Long Track 從「優秀」降為「合格」</strong>(CAGR 9.59% &lt; 12%、Calmar 0.48 &lt; 0.5,各差一步);
<strong>六狀態機 v1.1 以 0.8pp 之差跌出 MDD 門檻</strong>(-35.80% vs -35%)— 它已完成全站最完整的穩健性檢驗,
「未驗證/過擬合疑慮」的舊評語撤銷,出局原因單純是回撤太深,角色問題用部位大小解,不是用門檻豁免解;
<strong>v1.0r1 實盤雙項不合格</strong>且 2000-02 壓力路徑 -77%,升級 v1.1 為待決事項。</div>
</div>

<h3 style="font-size:1rem;font-weight:600;margin:1rem 0 .6rem">10 年視窗對照(2016 ~ 至今 · 修正後)</h3>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar</th><th>評語</th></tr></thead>
<tbody>
%TABLE10%
</tbody>
</table>
<div class="takeaway">10 年窗是「沒有 2008 的科技牛市」— 所有 CAGR &gt; 20% 的格子都該觸發可疑帶警報而不是慶祝;
用兩個視窗的<strong>交集</strong>做判斷,不是擇優。</div>
</div>
</div>

<!-- ===== 5. SELECTION ===== -->
<div class="section">
<h2 class="section-title">5. 選用原則</h2>
<div class="verdict">
  <strong>合格名單(2026-06):</strong>Long Track Only、LTO QQQ、GEM、W52 斜率(未經 warmup 審計,數字待覆核)。<br>
  <strong>角色配置:</strong>防守主力 = Long Track 50/50;進攻位 = LTO QQQ 或六狀態機 v1.1(後者不合格但可用部位大小納入 —
  56% 倉位 + 44% T-bill 即等效 -20% MDD 預算,代價是等風險下輸給 Long Track);
  互補 alpha = 跨資產趨勢(Turtle 商品腿 / Clenow),與美股趨勢家族低相關,是把 MDD 再往下壓唯一沒走過的路。<br>
  <strong>已採用(2026-06-11,OOS 追蹤中):</strong>Ensemble E3 = 股票趨勢核心採用版(Ch12 基準轉為對照組;
  重審:下一次盤整 + 下一次快崩兩個事件後)、LT SMH/QQQ = 進攻位(重審:滾動 3 年 Calmar 低於 SPY/QQQ 版,或半導體相對 QQQ 連 12 個月落後)。<br>
  <strong>已否決:</strong>雙軌多空(資金配置倒掛)、做空系統(兩個獨立引擎均證偽)、參數式微調(緩衝/確認週數,實測更糟)。
</div>
<div class="note">
  <strong>待辦:</strong>W52 斜率濾網與 GEM 尚未做 2026-06 標準的 warmup / 分母審計(數字截至 2026-04,引擎獨立)。
  在審計完成前,W52 的「全站最高 Sharpe 0.89」應視為未確認。
</div>
</div>

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 系統評估標準 v2 &middot; 門檻參考業界共識與個人經驗 &middot;
    頁面生成 %NOW% &middot; 僅供研究參考
  </div>
</footer>
</body>
</html>
"""


def main():
    html = render()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Written {OUT} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
