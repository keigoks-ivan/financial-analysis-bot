"""
Generator for /backtest/criteria/ — system evaluation framework v3 (2026-06).

v3 redesign rationale:
  * Trigger question (owner, 2026-06): "LT SMH/QQQ's CAGR loses to B&H —
    can we call the strategy bad?"  v2 had no formal layer to answer this:
    absolute thresholds say "investable or not", never "better than the
    lazy alternative or not".
  * v3 reorganizes evaluation as a 5-layer funnel:
      L0 validity (methodology discipline, was v2 §3)
      L1 absolute thresholds (unchanged bands, was v2 §1-2)
      L2 benchmark-relative dual-axis dominance  ← NEW core layer
      L3 portfolio-level marginal contribution   ← NEW (was scattered)
      L4 adoption decision (qualified ≠ adopted, was v2 §5)
  * L2 formalizes: "bad" has exactly one definition — dominated on BOTH
    the return axis and the risk-adjusted axes vs the declared natural
    benchmark.  Everything else is a trade whose value depends on the
    risk budget, judged with four tools (leverage equivalence,
    holdability, terminal-wealth honesty, endpoint sensitivity).
  * Dominance table uses each system page's pinned 20Y B&H numbers.

Update SYSTEMS / DOMINANCE below when a system page changes, then re-run:
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

# Minimum qualification thresholds (unchanged since v1)
TH = {"cagr": 8.0, "mdd": -35.0, "sharpe": 0.5, "calmar": 0.3}

# (name, url, cagr, mdd, sharpe, calmar, years_ok, note)  — 20Y, refreshed 2026-06-12
SYSTEMS_20Y = [
    ("Long Track Only", "/backtest/long_track/", 9.72, -20.08, 0.81, 0.48, True, ""),
    ("LTO QQQ only", "/backtest/long_track_qqq/", 10.80, -25.37, 0.75, 0.43, True, ""),
    ("Ensemble E3", "/backtest/long_track_ensemble/", 11.47, -21.15, 0.89, 0.54, True, "2026-06-11 採用 · OOS"),
    ("LT SMH/QQQ STX50", "/backtest/long_track_smh/", 14.05, -21.87, 0.91, 0.64, True, "2026-06-13 採用 STX50 · OOS"),
    ("W52 斜率濾網", "/backtest/slope_filter/", 10.16, -20.05, 0.92, 0.51, True, "warmup 完整(資料自 2000)"),
    ("GEM 雙動能", "/backtest/gem/", 8.95, -21.54, 0.57, 0.42, True, ""),
    ("六狀態機 v1.1", "/backtest/six_state/", 14.77, -35.80, 0.86, 0.41, True, ""),
    ("六狀態機 v1.0r1 實盤", "/backtest/six_state_v1r1/", 14.58, -49.29, 0.81, 0.30, True, "壓力路徑 -77%"),
    ("雙軌多空", "/backtest/dual_track/", 4.35, -38.72, 0.37, 0.11, True, "已否決 · 2026-06-12 修正重檢"),
    ("盤整 MR (RSI2)", "/backtest/rsi2_mr/", 3.12, -16.46, 0.50, 0.19, True, "實驗 · 未採用 · 組合互補性已否定(被現金壓制)"),
    ("週線 Supertrend (SPY)", "/backtest/supertrend/", 8.11, -17.77, 0.77, 0.46, True, "實驗 · 未採用 · standalone 輸 W52,E4 成員候選"),
    ("🐢 Turtle(多資產)", "/backtest/turtle/", 22.48, -38.12, 0.73, 0.59, True, "CAGR 進可疑帶"),
    ("📈 Clenow(多資產)", "/backtest/clenow/", 13.28, -44.11, 0.69, 0.30, True, ""),
]

# (name, cagr, mdd, sharpe, calmar, verdict)  — 10Y, refreshed 2026-06-12
SYSTEMS_10Y = [
    ("LT SMH/QQQ STX50", 25.60, -20.04, 1.31, 1.28, "warn", "CAGR 進可疑帶(>20%)— H2 半導體 regime"),
    ("六狀態機 v1.1", 22.40, -28.49, 1.12, 0.79, "warn", "CAGR 進可疑帶(>20%)— 無 2008 的視窗"),
    ("LTO QQQ only", 18.81, -25.18, 1.10, 0.75, "good", "進攻型優秀"),
    ("Ensemble E3", 16.29, -21.15, 1.12, 0.77, "good", "優秀(樣本內)"),
    ("Long Track Only", 15.47, -18.75, 1.11, 0.83, "good", "優秀"),
    ("W52 斜率濾網", 11.04, -20.05, 0.82, 0.55, "pass", "合格(穩定)"),
    ("GEM 雙動能", 9.85, -21.54, 0.54, 0.46, "pass", "合格"),
    ("雙軌多空", 9.26, -19.61, 0.73, 0.47, "fail", "10 年窗口仍墊底;全期已否決"),
    ("週線 Supertrend (SPY)", 11.86, -13.48, 1.09, 0.88, "pass", "實驗:10 年窗口合格,但全期輸 W52 · 未採用"),
    ("盤整 MR (RSI2)", 3.29, -16.46, 0.51, 0.20, "fail", "實驗:CAGR 低於門檻 · standalone 暴險僅 13% · 未採用"),
    ("QQQ Buy & Hold", 21.71, -35.12, 0.99, 0.62, "bh", "基準"),
    ("SPY Buy & Hold", 15.35, -33.72, 0.89, 0.46, "bh", "基準"),
]

# ===== L2 dominance data =====
# Pinned 20Y B&H benchmarks (from each system page, same engine/period):
#   SPY 2006-26:        +11.01 / -55.19 / 0.64 / 0.20
#   QQQ 2006-26:        +15.88 / -53.40 / 0.78 / 0.30
#   SPY/QQQ 50/50:      +13.52 / -53.66 / 0.73 / 0.25
#   SMH/QQQ 50/50:      +18.03 / -56.93 / 0.79 / 0.32
#   SPY 2000-26 (W52 頁): +10.94 / -50.78 (Sharpe/Calmar 欄位版式不同,不引用)
#   GEM 同期 SPY:        +10.99 / -50.78 / 0.60 / 0.22
# (name, url, bench_label, sys(cagr,mdd,sharpe,calmar), bench(... or None), kind, note)
DOMINANCE = [
    ("🐢 Turtle(多資產)", "/backtest/turtle/", "等權多資產 B&H",
     (22.48, -38.12, 0.73, 0.59), (10.92, None, None, None), "domc",
     "兩軸皆贏的稀有案例 → 不是慶祝,是觸發過擬合/regime 審查(CAGR 已進可疑帶;資產池不同僅參照)"),
    ("W52 斜率濾網", "/backtest/slope_filter/", "SPY B&H(同期,2000 起)",
     (10.16, -20.05, 0.92, 0.51), (10.94, -50.78, None, None), "neardom",
     "報酬只讓 0.8pp、回撤淺 2.5 倍 — 全站最接近支配的交換;惟 warmup 審計未完成,數字未確認"),
    ("LT SMH/QQQ STX50", "/backtest/long_track_smh/", "SMH/QQQ 50/50 B&H",
     (14.05, -21.87, 0.91, 0.64), (18.03, -56.93, 0.79, 0.32), "trade",
     "★ 本版觸發案例 — 完整判讀見上方範例"),
    ("Ensemble E3", "/backtest/long_track_ensemble/", "SPY/QQQ 50/50 B&H",
     (11.47, -21.15, 0.89, 0.54), (13.52, -53.66, 0.73, 0.25), "trade",
     "讓 2pp 報酬換 Calmar 2.2 倍 — 站內風險效率最佳的核心交換"),
    ("Long Track Only", "/backtest/long_track/", "SPY/QQQ 50/50 B&H",
     (9.72, -20.08, 0.81, 0.48), (13.52, -53.66, 0.73, 0.25), "trade", ""),
    ("六狀態機 v1.1", "/backtest/six_state/", "QQQ B&H",
     (14.77, -35.80, 0.86, 0.41), (15.88, -53.40, 0.78, 0.30), "trade",
     "支配性過關但 L1 門檻不過(MDD -35.8%)— 兩道關卡互相獨立,缺一不可"),
    ("週線 Supertrend (SPY)", "/backtest/supertrend/", "SPY B&H",
     (8.11, -17.77, 0.77, 0.46), (11.01, -55.19, 0.64, 0.20), "trade",
     "對 B&H 是有效交換,但輸給同家族 W52(第二基準)→ 只剩組合互補一條活路(E4 候選)"),
    ("LTO QQQ only", "/backtest/long_track_qqq/", "QQQ B&H",
     (10.80, -25.37, 0.75, 0.43), (15.88, -53.40, 0.78, 0.30), "mixed",
     "Calmar 贏 1.4 倍但 Sharpe 微輸 — 砍掉的是尾部,沒有提升波動效率;讓 5pp 報酬偏貴"),
    ("GEM 雙動能", "/backtest/gem/", "SPY B&H(同期)",
     (8.95, -21.54, 0.57, 0.42), (10.99, -50.78, 0.60, 0.22), "mixed",
     "同為「砍尾部、波動效率打平」型"),
    ("📈 Clenow(多資產)", "/backtest/clenow/", "等權多資產 B&H",
     (13.28, -44.11, 0.69, 0.30), (10.83, None, None, None), "mixed",
     "報酬軸贏 2.5pp 但 MDD -44% 過深(L1 不合格);資產池不同僅參照"),
    ("六狀態機 v1.0r1 實盤", "/backtest/six_state_v1r1/", "QQQ B&H",
     (14.58, -49.29, 0.81, 0.30), (15.88, -53.40, 0.78, 0.30), "weak",
     "讓 1.3pp 報酬,回撤只淺 4pp、Calmar 打平 — 付了趨勢系統的代價,沒拿到趨勢系統的保護"),
    ("雙軌多空", "/backtest/dual_track/", "SPY/QQQ 50/50 B&H",
     (4.35, -38.72, 0.37, 0.11), (13.52, -53.66, 0.73, 0.25), "dominated",
     "報酬、Sharpe、Calmar、MDD 全軸輸 — 正式定義下唯一能說「不好」的判定;已否決"),
    ("盤整 MR (RSI2)", "/backtest/rsi2_mr/", "SPY B&H",
     (3.12, -16.46, 0.50, 0.19), (11.01, -55.19, 0.64, 0.20), "dominated",
     "全軸輸或打平;L3 組合互補性亦被現金支配 — 雙重否決(standalone 暴險僅 13%,曝險調整後仍無解)"),
]

DOM_KINDS = {
    "domc":      ("tag-warn",   "支配候選 ⚠"),
    "neardom":   ("tag-best",   "近支配"),
    "trade":     ("tag-blue",   "有效交換"),
    "mixed":     ("tag-pass",   "混合"),
    "weak":      ("tag-orange", "無效交換"),
    "dominated": ("tag-fail",   "被支配"),
}


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


def _vs(s, b, fmt="{:.2f}", higher_wins=True, eps=0.02):
    """Render 'sys vs bench' with win/loss color; bench may be None."""
    if b is None:
        return f'<td>{fmt.format(s)} <span style="color:var(--muted)">vs —</span></td>'
    if abs(s - b) < eps:
        color = "var(--muted)"
    elif (s > b) == higher_wins:
        color = "var(--green)"
    else:
        color = "var(--red)"
    return (f'<td style="color:{color};font-weight:600">{fmt.format(s)}'
            f' <span style="font-weight:400">vs {fmt.format(b)}</span></td>')


def dominance_rows() -> str:
    rows = ""
    for name, url, bench, s, b, kind, note in DOMINANCE:
        sc, sm, ssh, sca = s
        bc, bm, bsh, bca = b
        tag_cls, tag_txt = DOM_KINDS[kind]
        d = sc - bc
        dcol = "var(--green)" if d >= 0 else "var(--red)"
        ratio = f'<span style="color:var(--muted);font-size:.78rem"> ({sca/bca:.1f}×)</span>' if bca else ""
        note_html = f'<br><span style="font-size:.72rem;color:var(--muted)">{note}</span>' if note else ""
        rows += (
            f'<tr><td><strong><a href="{url}">{name}</a></strong>'
            f'<br><span style="font-size:.72rem;color:var(--muted)">基準:{bench}</span>{note_html}</td>'
            f'<td style="color:{dcol};font-weight:600">{d:+.2f}pp</td>'
            + _vs(ssh, bsh) +
            (_vs(sca, bca)[:-5] + ratio + "</td>" if bca else _vs(sca, bca))
            + _vs(sm, bm, fmt="{:.1f}%", higher_wins=True)  # MDD: less negative = higher = wins
            + f'<td><span class="tag {tag_cls}">{tag_txt}</span></td></tr>\n')
    return rows


def render() -> str:
    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%TOGGLE%": make_toggle("criteria"),
        "%SCOREBOARD%": scoreboard_rows(),
        "%TABLE10%": table10_rows(),
        "%DOMTABLE%": dominance_rows(),
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
<title>系統評估標準 v3 | InvestMQuest Research</title>
<style>
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;
      --text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--red-text:#991b1b;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e;
      --blue-bg:#eff6ff;--blue-border:#bfdbfe;--blue-text:#1e40af;
      --orange-bg:#fff7ed;--orange-border:#fed7aa;--orange-text:#9a3412}
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
.tag-blue{background:var(--blue-bg);color:var(--blue-text);border:1px solid var(--blue-border)}
.tag-orange{background:var(--orange-bg);color:var(--orange-text);border:1px solid var(--orange-border)}
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
.example{border:2px solid var(--brand);border-radius:10px;background:var(--card);padding:1.3rem 1.5rem;margin:1rem 0}
.example h3{font-size:1.02rem;font-weight:700;color:var(--brand);margin-bottom:.7rem}
.example .step{display:flex;gap:.7rem;padding:.5rem 0;border-bottom:1px dashed var(--border);font-size:.88rem}
.example .step:last-of-type{border-bottom:none}
.example .step .n{flex-shrink:0;width:1.5rem;height:1.5rem;border-radius:50%;background:var(--brand);
                  color:#fff;font-size:.78rem;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:.15rem}
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
    <h1>系統評估標準 v3</h1>
    <div class="sub">五層評估漏斗 · 雙軸支配性分析 · 組合邊際貢獻 · 2026-06 修訂</div>
    %TOGGLE%
  </div>
</div>

<div class="container">

<!-- ===== HERO ===== -->
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag">📐 框架 v3 — 2026-06 修訂</span>
    <h2>「績效輸 Buy &amp; Hold,可以說這個策略不好嗎?」— v2 答不了這題,所以有 v3</h2>
    <p>LT SMH/QQQ STX50 的 CAGR(+14.05%)輸給 SMH/QQQ B&amp;H(+18.03%)。這算不算「策略不好」?
       v2 的絕對門檻只能回答「能不能投」,從來沒有正式回答過「比最懶的替代方案好嗎」。
       v3 把評估重組為<strong>五層漏斗</strong>:數字有效性 → 絕對門檻 → <strong>相對基準雙軸支配性(新)</strong> →
       組合邊際貢獻(新成文)→ 採用決策。核心新規則只有一條:
       <strong>「策略不好」有且只有一個正式定義 — 對宣告的自然基準,在報酬軸與風險調整軸上同時落敗(被支配)。</strong>
       其餘一切都是交換,值不值取決於風險預算,用第 2 層的四個工具判讀。
       門檻帶維持 v1/v2 不變(它們剛通過 2026-06 的自我壓力測試);改變的是門檻在整個評估裡的位置。</p>
  </div>
</div>

<!-- ===== 0. FUNNEL OVERVIEW ===== -->
<div class="section">
<h2 class="section-title">0. 評估漏斗總覽</h2>
<div class="section-sub">每一層回答一個不同的問題;任何一層出局就終止。層與層互相獨立 — 支配性過關不豁免門檻,門檻過關不豁免組合檢驗。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th style="width:9rem">層</th><th>回答的問題</th><th>工具</th><th>出局案例(站內)</th></tr></thead>
<tbody>
<tr><td><strong>L0 數字有效性</strong></td><td>這些數字能信嗎?</td>
    <td>分母完整性 · 樣本內紀律 · 現實假設 · 預註冊全揭露 · 統計可證偽性</td>
    <td>Long Track 舊頁 +10.95% 分母缺 4.5 年 → 修正為 +9.59%</td></tr>
<tr><td><strong>L1 絕對門檻</strong></td><td>這能不能投?(下限 + 過擬合警報)</td>
    <td>五指標門檻帶 + 可疑帶</td>
    <td>六狀態機 v1.1 — MDD -35.8% 差 0.8pp 出局</td></tr>
<tr><td><strong>L2 相對支配性</strong></td><td>它比「最懶的可執行替代方案」好嗎?</td>
    <td>雙軸支配性判定 + 四工具(槓桿等價 / 可持有性 / 終值誠實 / 終點敏感性)</td>
    <td>雙軌多空 — 對 50/50 B&amp;H 全軸落敗 → 被支配,否決</td></tr>
<tr><td><strong>L3 組合貢獻</strong></td><td>加進組合後,組合有沒有變好?</td>
    <td>相關性(尤其危機期)· 危機行為 · with/without 組合指標 · 同家族第二基準</td>
    <td>盤整 MR(RSI2)— 互補性被現金支配 → 雙重否決</td></tr>
<tr><td><strong>L4 採用決策</strong></td><td>要不要真的用?(合格 ≠ 採用)</td>
    <td>有記錄的決策 + OOS 重審 / 退場條件</td>
    <td>E3 / STX50 — 數字全過仍先記「未採用」,經審視後才採用並附條件</td></tr>
</tbody>
</table>
</div>
</div>

<!-- ===== 1. L0 METHODOLOGY ===== -->
<div class="section">
<h2 class="section-title">1. 第 0 層 — 數字有效性(方法論紀律)</h2>
<div class="section-sub">下游所有分析的前提。任何一條不過,該系統的數字視為無效,先修數再談評估。前五條來自 2026-06 修正週期,後兩條為 v3 新增(日內研究線的紀律反向移植)。</div>
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
  <li><strong>預註冊與全揭露</strong> — 門檻、網格、子期間在跑數之前申報;敏感度掃描全數揭露,不准沉默擇優。
      日內線(TXF / SSF)已全面實施;權益線回測自 v3 起比照辦理。</li>
  <li><strong>統計可證偽性(v3 新增)</strong> — 樣本太少的優勢與運氣不可區分。交易筆數 &lt; 20 筆/20 年的子軌,
      其 standalone 指標降級為「描述性」,不得作為配置依據(長軌單獨約 8 筆/20 年即屬此類);
      訊號層假設比照日內線標準:雙半期 t ≥ 2 才算存在。</li>
  <li><strong>合格 ≠ 採用,採用 = 決策 + 條件</strong> — 數字全過只代表「值得進入 L4 決策」。
      採用紀錄必須包含日期、保留意見、OOS 重審與退場條件(詳見第 6 節)。</li>
</ol>
</div>
</div>

<!-- ===== 2. L1 THRESHOLDS ===== -->
<div class="section">
<h2 class="section-title">2. 第 1 層 — 絕對門檻(維持 v1 帶)</h2>
<div class="section-sub">業界基準 + 個人判斷框架。「可疑」帶與「不及格」帶同樣重要 — 太好的數字是過擬合警報,不是慶祝理由。</div>

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
<h3>Sharpe Ratio · 波動效率</h3>
<div class="band"><span class="b-label">不及格</span><span class="b-range">&lt; 0.5</span><span class="b-bar" style="width:40px;background:var(--red)"></span><span class="b-desc">不如持有大盤</span></div>
<div class="band"><span class="b-label">及格</span><span class="b-range">0.5 ~ 0.8</span><span class="b-bar" style="width:80px;background:#9ca3af"></span><span class="b-desc">與 B&amp;H 相當</span></div>
<div class="band"><span class="b-label">良好</span><span class="b-range">0.8 ~ 1.2</span><span class="b-bar" style="width:120px;background:var(--brand)"></span><span class="b-desc">明確優於被動</span></div>
<div class="band"><span class="b-label">優秀</span><span class="b-range">1.2 ~ 2.0</span><span class="b-bar" style="width:160px;background:var(--green)"></span><span class="b-desc">機構級</span></div>
<div class="band"><span class="b-label">可疑</span><span class="b-range">&gt; 2.0</span><span class="b-bar" style="width:200px;background:var(--amber)"></span><span class="b-desc">⚠ 過擬合警報</span></div>
</div>

<div class="card">
<h3>Calmar Ratio · 尾部效率(CAGR ÷ |MDD|)<span class="tag tag-best" style="margin-left:.4rem">★ 最重要單一指標</span></h3>
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
<strong>交易次數</strong>:過少(&lt;20 筆/20 年)→ 觸發 L0 可證偽性降級;過多 → 成本與執行負擔。趨勢系統合理區間約 25~100 筆/20 年。</p>
</div>

<div class="two-col">
<div class="crit-box">
<h3>最低門檻(合格)</h3>
<ul>
<li>CAGR ≥ 8%</li>
<li>MDD ≥ -35%</li>
<li>Sharpe ≥ 0.5</li>
<li>Calmar ≥ 0.3</li>
<li>樣本期 ≥ 15 年(含至少 2 個熊市)</li>
<li>子期間穩健:H1 / H2 Calmar 皆 &gt; 0</li>
<li>分母完整:CAGR 自模擬起點起算、MA warmup 補齊</li>
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
<li>L2 判定 ≥ 有效交換(v3:取代舊「Sharpe &gt; B&amp;H」單條)</li>
<li>子期間平衡:H1 / H2 Calmar 差距 &lt; 3 倍</li>
</ul>
</div>
</div>

<div class="card takeaway" style="margin-top:1rem">
<strong>門檻的角色與極限:</strong>絕對門檻回答「能不能投」— 它過濾不可投資的(回撤深到必然棄船、報酬低到不值得執行),
並用可疑帶攔截好到不像話的。它<strong>回答不了「好不好」</strong>:一個 CAGR 14% 的系統可能輸給躺著不動(基準 18%),
一個 CAGR 9% 的系統可能是站內最接近支配基準的交換(W52)。「好不好」是第 2 層的工作。
</div>
</div>

<!-- ===== 3. L2 DOMINANCE ===== -->
<div class="section">
<h2 class="section-title">3. 第 2 層 — 相對基準:雙軸支配性分析(v3 新增核心)</h2>
<div class="section-sub">每個系統必須宣告自然基準 = 同一資產池裡「最懶但可執行」的替代方案(通常是 B&amp;H),再加同家族最強站內系統作第二基準。然後在兩條軸上比:報酬軸(CAGR)與風險調整軸(Sharpe = 波動效率、Calmar = 尾部效率 — 兩者回答不同問題,可能互相矛盾)。</div>

<div class="card">
<h3>五種判定</h3>
<table>
<thead><tr><th style="width:9.5rem">判定</th><th>定義</th><th>處置</th></tr></thead>
<tbody>
<tr><td><span class="tag tag-warn">支配候選 ⚠</span></td><td>報酬軸與風險調整軸<strong>全贏</strong></td>
    <td>不是慶祝 — 先觸發過擬合 / regime 集中審查(全贏太稀有,通常是樣本或方法問題)</td></tr>
<tr><td><span class="tag tag-best">近支配</span></td><td>報酬軸幾乎打平(讓 &lt; 1pp),風險調整軸明確贏</td>
    <td>最理想的真實狀態;確認 L0 有效性後優先配置</td></tr>
<tr><td><span class="tag tag-blue">有效交換</span></td><td>報酬軸讓分,Sharpe <strong>與</strong> Calmar 皆明確贏</td>
    <td>值不值取決於風險預算 — 用下方四工具判讀,<strong>不能</strong>因 CAGR 較低就說「不好」</td></tr>
<tr><td><span class="tag tag-pass">混合</span></td><td>Calmar 贏、Sharpe 輸或打平</td>
    <td>砍掉的是尾部、沒提升波動效率 — 對「以 MDD 定義風險」的人有價值,對「以波動定義風險」的人沒有;讓分越多越貴</td></tr>
<tr><td><span class="tag tag-orange">無效交換</span></td><td>報酬軸讓分,風險調整軸<strong>沒有換到</strong>(≈ 基準)</td>
    <td>付了主動管理的代價、沒拿到保護 — 接近劣勢,除非 L3 有強互補證據,否則否決</td></tr>
<tr><td><span class="tag tag-fail">被支配</span></td><td>報酬軸<strong>與</strong>風險調整軸全輸</td>
    <td><strong>這是「策略不好」唯一的正式定義</strong> — 直接否決,無需 L3/L4</td></tr>
</tbody>
</table>
</div>

<div class="card">
<h3>判讀交換的四個工具</h3>
<ol class="issue-list">
  <li><strong>槓桿等價(等風險比較)</strong> — Sharpe / Calmar 的本義是「每單位風險的報酬」。在可槓桿工具(期貨)上,
      風險效率高的系統可以加曝險到與基準相同的風險預算,屆時報酬軸的「落後」會消失甚至反轉 —
      所以<strong>在固定風險預算下,Calmar 高的那個才是更好的系統</strong>。
      三個必揭露的 caveat:波動拖累使報酬非線性、融資成本吃掉一部分、槓桿下 MDD 放大也非線性。
      本站實際不使用槓桿;此論證的用途是<strong>確立比較的正確座標系</strong>,不是建議開槓桿。</li>
  <li><strong>可持有性</strong> — B&amp;H 的 CAGR 隱含「完美持有紀律」:那 18% 的前提是抱住 -57% 不砍倉、不被贖回、不手滑。
      回測裡的 B&amp;H 沒有情緒,真實資金有。一個 MDD -22% 的系統和一個 -57% 的基準,
      在「真的能執行 20 年」這個維度上不是同一種東西。</li>
  <li><strong>終值誠實</strong> — 反過來也要誠實:複利下報酬軸的讓分極其昂貴,不准只報 ratio 不報終值。
      讓 4pp、20 年 = 終值少一半。如果效用函數就是終值極大化、且風險預算真的吃得下基準的回撤
      (部位小、無槓桿、無贖回壓力),那 B&amp;H 對那個人就是更好的選擇 — 這不是策略不好,是目標函數不同。</li>
  <li><strong>終點敏感性</strong> — 結束在牛市頂點的樣本偏袒 B&amp;H,結束在熊市谷底的樣本偏袒趨勢系統。
      判定前在 2~3 個替代終點(上一次熊市谷底、上一次盤整尾)重看結論是否翻轉;
      會翻轉的判定要標註,不會翻轉的才算穩。統計上同理:20 年樣本中 Sharpe 差距 &lt; ~0.15 通常無法與雜訊區分,
      但 MDD 砍半是<strong>結構性</strong>的(來自空頭期離場),不受小樣本懷疑論影響。</li>
</ol>
</div>

<!-- worked example -->
<div class="example">
<h3>判讀範例:LT SMH/QQQ STX50 vs SMH/QQQ 50/50 B&amp;H — 「CAGR 輸 4pp,這策略不好嗎?」</h3>
<div class="step"><span class="n">1</span><div><strong>兩軸事實。</strong>報酬軸:14.05% vs 18.03%,讓 3.98pp — B&amp;H 贏。
  風險調整軸:Sharpe 0.91 vs 0.79、Calmar 0.64 vs 0.32(2 倍)、MDD -21.9% vs -56.9% — 策略全贏。
  → 不是被支配,是<span class="tag tag-blue">有效交換</span>。「不好」這個詞在定義上就套不上。</div></div>
<div class="step"><span class="n">2</span><div><strong>終值誠實。</strong>$1M、20 年:策略 13.9 倍 vs B&amp;H 27.5 倍 — 終值少一半,這是交換的真實代價,必須明說。</div></div>
<div class="step"><span class="n">3</span><div><strong>槓桿等價。</strong>Calmar 0.64 vs 0.32:每承受 1 單位回撤,策略賺 2 倍。線性粗估 1.5× 曝險(期貨可行):
  CAGR ≈ 18~19%(已扣融資與波動拖累的量級)、MDD ≈ -31% — <strong>報酬追平 B&amp;H,回撤仍只有它的一半</strong>。
  B&amp;H 做不出反向操作(無法把 -57% 降下來而不犧牲更多報酬)→ 等風險座標系下,策略弱支配基準。</div></div>
<div class="step"><span class="n">4</span><div><strong>可持有性。</strong>B&amp;H 的 18% 要求抱住 -57%(樣本內 SMH 段最深 -64%)。半導體單一產業 ETF 腰斬再加碼的路徑,
  對多數資金配置不可執行 — 基準的報酬軸優勢有一部分是紙上的。</div></div>
<div class="step"><span class="n">5</span><div><strong>終點敏感性。</strong>本樣本終點(2026-06)落在 AI/半導體大多頭高點附近,B&amp;H 的 CAGR 被終點加持;
  終點若在 2022-10 或 2009-03,報酬軸差距大幅收斂甚至反轉。同一系統在 10 年窗(2016 起)對 QQQ B&amp;H
  是<strong>兩軸全贏</strong>(25.6%/-20.0% vs 21.7%/-35.1%)— 窗口與基準的選擇就能改寫故事,
  所以判定必須:固定自然基準 + 兩個視窗取交集 + 標註終點位置。</div></div>
<div class="step"><span class="n">6</span><div><strong>結論。</strong>有效交換 — 用 4pp CAGR 買回撤從 -57% 到 -22% 的壓縮。值不值取決於風險預算;
  此外它在組合裡是進攻位 sleeve(L3),最終考題是組合層的貢獻,不是 standalone 對 B&amp;H 的擂台。
  Sharpe 差 0.12 在 20 年樣本接近雜訊邊緣,但 MDD 砍半是結構性的 — 交換的價值主要在尾部,這也與「混合」型系統劃清界線。</div></div>
</div>

<div class="card" style="overflow-x:auto">
<h3>全系統支配性對照(20 年 · 對各自的自然基準)</h3>
<table>
<thead><tr><th>系統 / 基準</th><th>ΔCAGR</th><th>Sharpe</th><th>Calmar</th><th>MDD</th><th>判定</th></tr></thead>
<tbody>
%DOMTABLE%
</tbody>
</table>
<div class="takeaway">
讀法:<strong>13 個系統裡只有 2 個「被支配」</strong>(雙軌多空、RSI2)— 它們也正是已否決的系統,判定與決策史一致。
有效交換是趨勢家族的常態型;「混合」型(LTO QQQ、GEM)提醒 Sharpe 與 Calmar 是兩種風險定義,不可混報;
v1.0r1 的「無效交換」是最危險的象限 — 付了代價沒買到保護,比被支配更難察覺。
Turtle 兩軸全贏反而觸發審查,這是可疑帶哲學在 L2 的延伸。
</div>
</div>
</div>

<!-- ===== 4. L3 PORTFOLIO ===== -->
<div class="section">
<h2 class="section-title">4. 第 3 層 — 組合邊際貢獻(v3 成文)</h2>
<div class="section-sub">sleeve 的最終考題不是 standalone 對 B&amp;H,而是:加進組合後,組合的 Calmar / MDD 有沒有變好。一個 standalone 平庸的系統可能是好 sleeve(低相關),一個 standalone 合格的系統可能是壞 sleeve(與既有部位同漲同跌)。</div>
<div class="card">
<ol class="issue-list">
  <li><strong>危機期相關性優先於全期相關性</strong> — 全期低相關但 2008/2020/2022 同步 -30% 的 sleeve 沒有分散價值;
      相關性必須分段報:全期 / 三次危機窗 / 高利率盤整段。</li>
  <li><strong>with / without 是唯一裁決</strong> — 把候選 sleeve 以擬議權重加入現行組合,
      報組合層 CAGR / MDD / Calmar 的前後對照;邊際 Calmar 沒有改善 → 不論 standalone 多漂亮都不加。
      案例:RSI2 MR standalone 已被支配,組合檢驗再確認「同權重換成現金更好」— 互補性被現金支配,雙重否決。</li>
  <li><strong>第二基準:同家族最強系統</strong> — 新候選除了贏 B&amp;H,還要跟站內同家族最強者比;
      輸了就只剩「與它低相關」一條入場路。案例:週線 Supertrend standalone 輸 W52,
      但與 E3 成員的出場時點互補 → 不作 standalone 採用,保留為 E4 成員候選 / 出場閘門(STX50 即此用法)。</li>
  <li><strong>角色決定評分權重</strong> — 防守位(核心)看 Calmar 與危機行為;進攻位看 CAGR 與 regime 集中度(可疑帶);
      互補位看相關性與危機月份報酬。用同一張表評所有角色 = 類別錯誤。
      站內現行角色:防守主力 = E3(SPY/QQQ)、進攻位 = STX50(SMH/QQQ)、
      互補缺口 = 跨資產趨勢(Turtle 商品腿 / Clenow)— 與美股趨勢家族低相關,是把組合 MDD 再往下壓唯一沒走過的路。</li>
  <li><strong>曝險調整視角</strong> — 平均曝險 13% 的系統(RSI2)與滿倉系統的 headline CAGR 不可直比;
      報「每單位曝險報酬」作輔助欄。但注意:曝險調整能解釋數字,不能豁免 with/without 裁決。</li>
</ol>
</div>
</div>

<!-- ===== 5. SCOREBOARD ===== -->
<div class="section">
<h2 class="section-title">5. 計分板(L1 絕對門檻 · 修正後數據)</h2>
<div class="section-sub">每格 = 是否通過該項最低門檻。多資產系統(Turtle/Clenow)資產池不同,僅供參照。數據截至日期見各系統頁。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>CAGR ≥ 8%</th><th>MDD ≥ -35%</th><th>Sharpe ≥ 0.5</th><th>Calmar ≥ 0.3</th><th>樣本 ≥ 15y</th><th>判定</th></tr></thead>
<tbody>
%SCOREBOARD%
</tbody>
</table>
<div class="takeaway">2026-06 修正後的變動:<strong>Long Track 從「優秀」降為「合格」</strong>(CAGR 9.59% &lt; 12%、Calmar 0.48 &lt; 0.5,各差一步);
<strong>六狀態機 v1.1 以 0.8pp 之差跌出 MDD 門檻</strong>(-35.80% vs -35%)— 它已完成全站最完整的穩健性檢驗,
出局原因單純是回撤太深,角色問題用部位大小解,不是用門檻豁免解;
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
注意 STX50 在此窗對 QQQ B&amp;H 兩軸全贏、在 20 年窗對 SMH/QQQ B&amp;H 是交換 —
這正是 L2 終點敏感性工具存在的理由。用兩個視窗的<strong>交集</strong>做判斷,不是擇優。</div>
</div>
</div>

<!-- ===== 6. L4 ADOPTION ===== -->
<div class="section">
<h2 class="section-title">6. 第 4 層 — 採用決策與現行配置</h2>
<div class="verdict">
  <strong>合格名單(2026-06):</strong>Long Track Only、LTO QQQ、Ensemble E3、LT SMH/QQQ STX50、GEM、W52 斜率(未經 warmup 審計,數字待覆核)。<br>
  <strong>已採用(均附 OOS 重審 / 退場條件):</strong>
  Ensemble E3 = 股票趨勢核心(2026-06-11;Ch12 基準轉為對照組;重審:下一次盤整 + 下一次快崩兩個事件後)、
  LT SMH/QQQ <strong>STX50</strong> = 進攻位(2026-06-13;E3 + 週線 Supertrend 半倉出場閘門;
  重審:滾動 3 年 Calmar 低於 SPY/QQQ 版,或半導體相對 QQQ 連 12 個月落後)。<br>
  <strong>角色配置:</strong>防守主力 = E3;進攻位 = STX50;六狀態機 v1.1 L1 不合格但可用部位大小納入
  (56% 倉位 + 44% T-bill 即等效 -20% MDD 預算,代價是等風險下輸給 Long Track);
  互補缺口 = 跨資產趨勢(Turtle 商品腿 / Clenow)。<br>
  <strong>已否決(L2/L3 判定與決策一致):</strong>雙軌多空(被支配 + 資金配置倒掛)、盤整 MR(被支配 + 互補性被現金支配)、
  做空系統(兩個獨立引擎均證偽)、參數式微調(緩衝/確認週數,實測更糟)。<br>
  <strong>原則:</strong>採用來自有記錄的決策,不來自漂亮的回測數字本身;每筆採用必須同時寫下「什麼情況下退場重審」。
</div>
<div class="note">
  <strong>待辦:</strong>W52 斜率濾網與 GEM 尚未做 2026-06 標準的 warmup / 分母審計(數字截至 2026-04,引擎獨立)。
  在審計完成前,W52 的「近支配」判定應視為未確認 — 它若確認,將是全站第一個近支配系統,值得優先排審。
</div>
</div>

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 系統評估標準 v3 &middot; 門檻參考業界共識與個人經驗 &middot;
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
