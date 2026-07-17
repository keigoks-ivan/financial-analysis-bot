#!/usr/bin/env python3
"""
QQQ + SMH 長線 × 波動率目標 — 前瞻 OOS 追蹤（paper tracking）訊號頁產生器
========================================================================
每交易日抓 QQQ、SMH 日線（auto-adjust），逐標的算：
  1. 週線長軌閘門（W-FRI；進場 score5＝週收 > W52/W104/W250 且 W104/W250 四週
     斜率 > 0；出場一根週收 < W52；長多 only）→ 0/1。
  2. 波動率套袖 w = min(1, σ目標／RV20)，RV20＝20 日對數報酬年化波動。
  3. 最終目標權重 = 0.5 × 閘門 × 套袖（兩標的各自計算，合成即等權每日再平衡）。

凍結規則（永久，2026-07-17）：σ目標 QQQ 20%、SMH 25%；成本 7 bps／邊；
t 收盤訊號、t+1 收盤生效。定位＝前瞻 OOS 追蹤，非實盤採用。

閘門定義逐位元對齊回測授權（v7-backtest
src/vol_target_backtest/run_ext_ltrack_smh.longtrack_weight 與 run_vol_target.
vt_weight）；規則若變更，兩處一起改。回測數字見 BACKTEST 常數（由
results/vol_targeting/combo_qs.json 轉錄）。

CANONICAL COPY：本檔在 v7-backtest（src/vol_target_backtest/）與
financial-analysis-bot（scripts/）兩處逐位元相同——nav 匯入以 try/except 兼容
兩 repo，輸出路徑自動解析為 <repo_root>/docs/long-track-qs-vt/。CI 由 fab 執行。

排程：每交易日美股收盤後（套袖 RV20 為日頻量，閘門為週頻，故日更）。
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

# ---- nav import (byte-identical file across two repos) ---------------------
HERE = Path(__file__).resolve().parent
for _p in (HERE, HERE.parents[2] if len(HERE.parents) >= 3 else HERE):
    sys.path.insert(0, str(_p))
try:                                       # fab: scripts/site_nav.py
    from site_nav import full_nav_block
except ImportError:                        # v7-backtest: repo-root snippet
    from site_nav_snippet import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "ltqsvt")

# ---- output dir: <repo_root>/docs/long-track-qs-vt/ ------------------------
_cand = [HERE.parent / "docs", HERE.parents[2] / "docs" if len(HERE.parents) >= 3 else HERE / "docs"]
DOCS = next((c for c in _cand if c.exists()), _cand[0])
OUTPUT = DOCS / "long-track-qs-vt" / "index.html"
STATE_JSON = DOCS / "long-track-qs-vt" / "state.json"
ALERT_FILE = DOCS.parent / "lt_qs_vt_alert.txt"

TICKERS = ["QQQ", "SMH"]
WEIGHTS = {"QQQ": 0.5, "SMH": 0.5}
SIGMA = {"QQQ": 0.20, "SMH": 0.25}         # 凍結 2026-07-17
FREEZE_DATE = "2026-07-17"

# 回測（results/vol_targeting/combo_qs.json，window 2005-01-03 起）— 轉錄
BACKTEST = {
    "window": "2005-01 – 2026-07",
    "rows": [                              # (label, cagr, mdd, calmar, ui, martin)
        ("凍結 σ Q20/S25（本頁追蹤）", 11.90, -21.8, 0.547, 8.21, 1.45),
        ("50/50 買進持有", 17.65, -56.9, 0.310, 13.99, 1.26),
        ("純長軌（無套袖）", 12.36, -34.0, 0.363, 9.77, 1.27),
        ("掃描最佳 σ Q15/S30", 12.13, -21.3, 0.569, 7.78, 1.56),
    ],
    "grid": [                              # (qσ, sσ, calmar, cagr, mdd, martin)
        (15, 25, 0.549, 11.66, -21.3, 1.54), (15, 30, 0.569, 12.13, -21.3, 1.56),
        (15, 35, 0.582, 12.41, -21.3, 1.57), (20, 25, 0.547, 11.90, -21.8, 1.45),
        (20, 30, 0.566, 12.36, -21.8, 1.46), (20, 35, 0.552, 12.64, -22.9, 1.47),
        (25, 25, 0.542, 11.96, -22.1, 1.38), (25, 30, 0.551, 12.42, -22.5, 1.40),
        (25, 35, 0.529, 12.70, -24.0, 1.40),
    ],
    "eras": [                              # (label, ΔCAGR vs 純長軌, ΔMDD pp)
        ("2005-08 GFC", -0.1, +0.0), ("2009-13 QE", +0.8, +2.0),
        ("2014-18 低波", -1.0, +0.5), ("2019-23 COVID", +1.3, +14.5),
        ("2024- AI 牛", -7.1, +4.8),
    ],
}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def fetch_close(ticker: str) -> pd.Series:
    end = datetime.now() + timedelta(days=1)
    start = end - timedelta(days=365 * 13)   # 13y: W250 (~4.8y) warmup + state history
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:, 0]
    return c.dropna()


# ---------------------------------------------------------------------------
# Gate — verbatim port of run_ext_ltrack_smh.longtrack_weight (weekly, long-only)
# ---------------------------------------------------------------------------
def gate_state(px: pd.Series) -> dict:
    wk = px.resample("W-FRI").last().dropna()
    w52 = wk.rolling(52).mean()
    w104 = wk.rolling(104).mean()
    w250 = wk.rolling(250).mean()
    s104 = w104 - w104.shift(4)
    s250 = w250 - w250.shift(4)
    pos, state = [], 0
    for i in range(len(wk)):
        if pd.isna(w250.iloc[i]) or pd.isna(s250.iloc[i]):
            pos.append(0)
            continue
        c = wk.iloc[i]
        if (state == 0 and c > w52.iloc[i] and c > w104.iloc[i] and c > w250.iloc[i]
                and s104.iloc[i] > 0 and s250.iloc[i] > 0):
            state = 1
        elif state == 1 and c < w52.iloc[i]:
            state = 0
        pos.append(state)
    pos = pd.Series(pos, index=wk.index, dtype=int)

    recent = []
    for i in range(-8, 0):
        recent.append({
            "date": wk.index[i].strftime("%Y-%m-%d"),
            "close": float(wk.iloc[i]),
            "w52": float(w52.iloc[i]) if not pd.isna(w52.iloc[i]) else None,
            "w104": float(w104.iloc[i]) if not pd.isna(w104.iloc[i]) else None,
            "w250": float(w250.iloc[i]) if not pd.isna(w250.iloc[i]) else None,
            "s104_pos": bool(s104.iloc[i] > 0) if not pd.isna(s104.iloc[i]) else None,
            "s250_pos": bool(s250.iloc[i] > 0) if not pd.isna(s250.iloc[i]) else None,
            "in": bool(pos.iloc[i]),
        })
    return {
        "gate": bool(pos.iloc[-1]),
        "wk_date": wk.index[-1].strftime("%Y-%m-%d"),
        "wk_close": float(wk.iloc[-1]),
        "w52": float(w52.iloc[-1]), "w104": float(w104.iloc[-1]), "w250": float(w250.iloc[-1]),
        "s104_pos": bool(s104.iloc[-1] > 0), "s250_pos": bool(s250.iloc[-1] > 0),
        "recent": recent,
    }


# ---------------------------------------------------------------------------
# Sleeve — verbatim port of run_vol_target.vt_weight
# ---------------------------------------------------------------------------
def sleeve_state(px: pd.Series, sigma: float, win: int = 20) -> dict:
    lr = np.log(px / px.shift(1))
    rv = lr.rolling(win).std() * np.sqrt(252)
    rv_now = float(rv.iloc[-1])
    w = min(1.0, sigma / rv_now) if rv_now > 0 else 1.0
    return {"rv20": rv_now, "sleeve": w}


def compute_ticker(t: str) -> dict:
    px = fetch_close(t)
    g = gate_state(px)
    s = sleeve_state(px, SIGMA[t])
    fill = (1 if g["gate"] else 0) * s["sleeve"]        # 0..1 fill of the 0.5 slot
    final = WEIGHTS[t] * fill
    return {**g, **s, "sigma": SIGMA[t], "fill": fill, "final": final}


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
def fmt_pct(v, dp=2):
    return f"{'+' if v >= 0 else ''}{v:.{dp}f}%"


def fill_color(fill):
    if fill >= 0.99:
        return "green"
    if fill >= 0.66:
        return "blue"
    if fill >= 0.33:
        return "amber"
    return "red"


def ticker_card(t: str, d: dict) -> str:
    col = fill_color(d["fill"])
    gate_on = d["gate"]
    d52 = (d["wk_close"] / d["w52"] - 1) * 100
    d104 = (d["wk_close"] / d["w104"] - 1) * 100
    d250 = (d["wk_close"] / d["w250"] - 1) * 100
    near_exit = gate_on and abs(d52) < 2.0
    warn = (' <span style="color:var(--amber);font-weight:700;font-size:.72rem">'
            '⚠ 接近出場（近 W52）</span>') if near_exit else ""
    return f"""<div class="tcard">
  <div class="tcard-hdr">
    <span class="tname">{t}</span>
    <span class="pos-badge pos-{col}">最終權重 {d['final']*100:.0f}%</span>
  </div>
  <div class="tcard-sub">閘門 {'在場' if gate_on else '出場'} × 套袖 {d['sleeve']*100:.0f}%
    → 佔本標的 50% 額度的 {d['fill']*100:.0f}% · 目標權重 0.5 × {1 if gate_on else 0} × {d['sleeve']:.2f} = {d['final']*100:.0f}%{warn}</div>
  <div class="sig-row">
    <div class="sig {'on' if gate_on else 'off'}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">週線長軌閘門</span><span class="sig-mark">{'✓ 在場' if gate_on else '✕ 出場'}</span></div>
      <div class="sig-detail">週收 {d['wk_close']:.2f}｜W52 {d['w52']:.2f} <b style="color:var(--{'green' if d52>=0 else 'red'})">{fmt_pct(d52,1)}</b>
        ｜W104 {d['w104']:.2f} <b style="color:var(--{'green' if d104>=0 else 'red'})">{fmt_pct(d104,1)}</b>
        ｜W250 {d['w250']:.2f} <b style="color:var(--{'green' if d250>=0 else 'red'})">{fmt_pct(d250,1)}</b>
        ｜W104斜率 {'↑' if d['s104_pos'] else '↓'}｜W250斜率 {'↑' if d['s250_pos'] else '↓'}
        <br><span style="font-size:.72rem">進場 score5＝週收在三線上且 W104/W250 四週斜率為正；出場＝一根週收 &lt; W52。</span></div>
    </div>
    <div class="sig {'on' if d['sleeve']>=0.999 else 'off'}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">波動率套袖 σ目標 {d['sigma']*100:.0f}%</span><span class="sig-mark">{d['sleeve']*100:.0f}%</span></div>
      <div class="sig-detail">RV20（20日年化波動）<b>{d['rv20']*100:.1f}%</b> vs σ目標 {d['sigma']*100:.0f}%
        → w = min(1, {d['sigma']*100:.0f}%／{d['rv20']*100:.1f}%) = <b>{d['sleeve']:.2f}</b>
        <br><span style="font-size:.72rem">{'波動 ≤ σ目標，滿載。' if d['sleeve']>=0.999 else '波動高於 σ目標，按比例減碼（只降不加）。'}</span></div>
    </div>
  </div>
</div>"""


def recent_table(t: str, d: dict) -> str:
    rows = ""
    for r in d["recent"]:
        if r["w52"] is None:
            continue
        d52 = (r["close"] / r["w52"] - 1) * 100
        c52 = "var(--green)" if d52 >= 0 else "var(--red)"
        incell = (f'<span class="tag" style="background:var(--green-bg);color:var(--green-text)">在場</span>'
                  if r["in"] else
                  f'<span class="tag" style="background:var(--red-bg);color:var(--red-text)">出場</span>')
        rows += f"""<tr>
  <td>{r['date']}</td><td>{r['close']:.2f}</td>
  <td>{r['w52']:.2f}</td><td style="color:{c52}">{fmt_pct(d52,1)}</td>
  <td>{r['w104']:.2f}</td><td>{r['w250']:.2f}</td>
  <td>{'↑' if r['s104_pos'] else '↓'} / {'↑' if r['s250_pos'] else '↓'}</td>
  <td>{incell}</td>
</tr>\n"""
    return f"""<div class="card">
<h3>{t} — 近 8 週閘門軌跡（週線 W-FRI）</h3>
<table><thead><tr><th>週五</th><th>週收</th><th>W52</th><th>距 W52</th><th>W104</th><th>W250</th><th>W104/W250 斜率</th><th>閘門</th></tr></thead>
<tbody>{rows}</tbody></table>
</div>"""


def backtest_section() -> str:
    rows = ""
    for lab, cagr, mdd, calmar, ui, martin in BACKTEST["rows"]:
        hl = "rowhl" if "凍結" in lab else ("rowbh" if "買進持有" in lab else "")
        rows += (f'<tr class="{hl}"><td>{lab}</td><td class="num">{cagr:.2f}%</td>'
                 f'<td class="num">{mdd:.1f}%</td><td class="num">{calmar:.3f}</td>'
                 f'<td class="num">{ui:.2f}</td><td class="num">{martin:.2f}</td></tr>\n')
    grid = ""
    for qs, ss, calmar, cagr, mdd, martin in BACKTEST["grid"]:
        hl = ' class="rowhl"' if (qs == 20 and ss == 25) else ""
        grid += (f'<tr{hl}><td>Q{qs}% / S{ss}%</td><td class="num">{calmar:.3f}</td>'
                 f'<td class="num">{cagr:.2f}%</td><td class="num">{mdd:.1f}%</td>'
                 f'<td class="num">{martin:.2f}</td></tr>\n')
    eras = ""
    for lab, dc, dm in BACKTEST["eras"]:
        cc = "pos" if dc >= 0 else "neg"
        cm = "pos" if dm >= 0 else "neg"
        eras += (f'<tr><td>{lab}</td><td class="num {cc}">{dc:+.1f}pp</td>'
                 f'<td class="num {cm}">{dm:+.1f}pp</td></tr>\n')
    return f"""<div class="card">
<h3>回測摘要（凍結版 vs 三基準・共同窗 {BACKTEST['window']}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
兩標的日報酬 50/50 加權合成（等效每日再平衡，如實揭露）。判準基準＝<b>純長軌組合</b>（非買進持有）。</p>
<table><thead><tr><th>配置</th><th class="num">CAGR</th><th class="num">MDD</th><th class="num">Calmar</th><th class="num">Ulcer</th><th class="num">Martin</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="takeaway">套袖把純長軌的 Calmar 0.363 → <b>0.547</b>、MDD −34.0% → <b>−21.8%</b>，CAGR 只付 0.46pp；
對 50/50 買進持有則是「風險調整支配、CAGR 讓步」（B&amp;H 17.65%／−56.9%）。凍結 σ（0.547）貼近掃描最佳（Q15/S30 0.569），
不靠選中特定 σ 才成立。<b>唯一系統性代價集中在 AI 牛（單期 CAGR −7.1pp，高波急彈仍減碼、漏接反彈）。</b></div>
</div>

<div class="card">
<h3>σ 目標敏感度對照（僅回測參考，不追蹤）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
QQQ σ × SMH σ 網格的組合 Calmar。凍結格 Q20/S25 高亮；最佳 Q15/S35（0.582）與凍結差距小，故採原則法 σ（各自長期 RV 中位取整）。</p>
<table><thead><tr><th>σ 組合</th><th class="num">Calmar</th><th class="num">CAGR</th><th class="num">MDD</th><th class="num">Martin</th></tr></thead>
<tbody>{grid}</tbody></table>
</div>

<div class="card">
<h3>分期（凍結 vs 純長軌；ΔCAGR／ΔMDD，正＝套袖較優）</h3>
<table><thead><tr><th>期間</th><th class="num">Δ CAGR</th><th class="num">Δ MDD</th></tr></thead>
<tbody>{eras}</tbody></table>
<div style="font-size:.75rem;color:var(--muted);margin-top:.5rem">五期 MDD 全數改善（+0.0～+14.5pp）；CAGR 代價集中在 AI 牛（−7.1pp）。</div>
</div>"""


def generate_html(sigs: dict, changes: list | None, last_change_date: str | None) -> str:
    changes = changes or []
    combined = sum(sigs[t]["final"] for t in TICKERS) * 100
    ccol = fill_color(combined / 100)
    data_date = max(sigs[t]["wk_date"] for t in TICKERS)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cards = "".join(ticker_card(t, sigs[t]) for t in TICKERS)
    tables = "".join(recent_table(t, sigs[t]) for t in TICKERS)

    change_html = (
        ('<div style="background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;'
         'padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem"><b style="color:var(--red-text)">'
         '可行動變化</b><br>' + "<br>".join(changes) +
         '<br><span style="font-size:.78rem;color:var(--muted)">下一個交易日將部位調整至上列目標。</span></div>')
        if changes else
        ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">'
         '無可行動變化（閘門未翻轉、且無標的最終權重變動 ≥ 10pp）' +
         (f'（上次變化：{last_change_date}）' if last_change_date else '') + '</div>'))

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>QQQ + SMH 長線 × 波動率目標｜前瞻 OOS 追蹤 | InvestMQuest Research</title>
  <meta name="description" content="QQQ 50% + SMH 50% · 週線長軌閘門 × 波動率目標套袖 · 前瞻 OOS 紙上追蹤（未採用）">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/imq-base.css">
  <style>
:root{{--brand:#0d2244;--bg:#f7f3ea;--card:#ffffff;--text:#0c1521;--muted:#9aa7b8;--border:#e5dfd0;
  --green:#15803d;--green-bg:#eafaef;--green-border:var(--line);--green-text:#15803d;
  --red:#b91c1c;--red-bg:#fbeceb;--red-border:var(--line);--red-text:#b91c1c;
  --amber:#a16207;--amber-bg:#fbf3df;--amber-border:var(--line);--amber-text:#a16207;
  --blue:#1d4ed8;--blue-bg:#e8eef5;--blue-border:var(--line);--blue-text:#1d4ed8}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.65;font-size:14px}}
a{{color:var(--brand);text-decoration:none}}a:hover{{text-decoration:underline}}
.container{{max-width:1140px;margin:0 auto;padding:0 1.5rem}}
.page-hdr{{padding:1.5rem 0 1.2rem;background:var(--card);border-bottom:1px solid var(--border)}}
.page-hdr h1{{font-family:var(--serif);font-size:1.5rem;font-weight:700;letter-spacing:-.01em}}
.page-hdr .sub{{color:var(--muted);font-size:.85rem;margin-top:.2rem}}
.crumb{{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}}
.crumb a{{color:var(--muted)}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;margin-bottom:1rem;box-shadow:var(--sh-1)}}
.card h3{{font-size:.95rem;font-weight:600;margin-bottom:.75rem}}
.card .takeaway{{font-size:.82rem;margin-top:.75rem;padding:.6rem .9rem;border-radius:8px;background:#f6f8fb;border-left:3px solid var(--brand)}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th,td{{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}}
th{{background:transparent;font-family:var(--mono);font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}}
td{{font-variant-numeric:tabular-nums}}
td.num,th.num{{text-align:right}}
.pos{{color:var(--green);font-weight:600}}.neg{{color:var(--red);font-weight:600}}
.rowhl td{{background:#eef3fb!important}}.rowbh td{{background:#faf7f0;color:var(--muted)}}
tbody tr:hover td{{background:#fbf8f1}}
.tag{{display:inline-block;padding:.12rem .5rem;border-radius:6px;font-size:.7rem;font-weight:600}}
footer{{background:var(--card);border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1rem 0;font-size:.75rem;margin-top:1rem}}
.status-hero{{padding:2rem 0 1rem;text-align:center}}
.status-badge{{display:inline-flex;align-items:center;gap:.75rem;padding:1rem 2.5rem;border-radius:var(--r);font-size:1.4rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.5rem}}
.status-badge .dot{{width:14px;height:14px;border-radius:50%;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.status-exposure{{font-size:2.6rem;font-weight:800;margin:.3rem 0}}
.status-date{{font-size:.8rem;color:var(--muted)}}
.hero-green .status-badge{{background:var(--green-bg);color:var(--green-text);border:2px solid var(--green-border)}}
.hero-green .dot{{background:var(--green)}}.hero-green .status-exposure{{color:var(--green)}}
.hero-blue .status-badge{{background:var(--blue-bg);color:var(--blue-text);border:2px solid var(--blue-border)}}
.hero-blue .dot{{background:var(--blue)}}.hero-blue .status-exposure{{color:var(--blue)}}
.hero-amber .status-badge{{background:var(--amber-bg);color:var(--amber-text);border:2px solid var(--amber-border)}}
.hero-amber .dot{{background:var(--amber)}}.hero-amber .status-exposure{{color:var(--amber)}}
.hero-red .status-badge{{background:var(--red-bg);color:var(--red-text);border:2px solid var(--red-border)}}
.hero-red .dot{{background:var(--red)}}.hero-red .status-exposure{{color:var(--red)}}
.tgrid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}}
.tcard{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem;box-shadow:var(--sh-1)}}
.tcard-hdr{{display:flex;align-items:center;justify-content:space-between;margin-bottom:.2rem}}
.tname{{font-size:1.3rem;font-weight:800;letter-spacing:-.02em}}
.pos-badge{{font-size:.95rem;font-weight:700;padding:.25rem .7rem;border-radius:6px}}
.pos-green{{background:var(--green-bg);color:var(--green-text)}}.pos-blue{{background:var(--blue-bg);color:var(--blue-text)}}
.pos-amber{{background:var(--amber-bg);color:var(--amber-text)}}.pos-red{{background:var(--red-bg);color:var(--red-text)}}
.tcard-sub{{font-size:.75rem;color:var(--muted);margin-bottom:.75rem}}
.sig-row{{display:grid;grid-template-columns:1fr;gap:.5rem}}
.sig{{border:1px solid var(--border);border-radius:var(--r);padding:.55rem .7rem;background:var(--card)}}
.sig.on{{border-color:var(--green-border);background:var(--green-bg)}}
.sig.off{{border-color:var(--red-border);background:var(--red-bg)}}
.sig-top{{display:flex;align-items:center;gap:.5rem}}
.sig-dot{{width:11px;height:11px;border-radius:50%}}
.sig.on .sig-dot{{background:var(--green)}}.sig.off .sig-dot{{background:var(--red)}}
.sig-name{{font-weight:700;font-size:.85rem}}
.sig-mark{{margin-left:auto;font-weight:800}}
.sig.on .sig-mark{{color:var(--green)}}.sig.off .sig-mark{{color:var(--red)}}
.sig-detail{{font-size:.74rem;color:var(--muted);margin-top:.2rem;font-variant-numeric:tabular-nums}}
.oos-banner{{background:linear-gradient(135deg,#fdf6e3 0%,#faf0d7 100%);border:2px solid var(--amber);border-radius:12px;padding:1rem 1.3rem;margin:1rem 0}}
.oos-banner .tag-loud{{display:inline-block;background:var(--amber);color:#fff;font-size:.72rem;font-weight:800;letter-spacing:.06em;padding:.22rem .7rem;border-radius:99px;margin-bottom:.45rem}}
.oos-banner b{{color:var(--amber-text)}}
.rule-list{{font-size:.82rem;line-height:1.9}}.rule-list b{{color:var(--text)}}
@media(max-width:768px){{.tgrid{{grid-template-columns:1fr}}.status-exposure{{font-size:2rem}}table{{font-size:.74rem}}th,td{{padding:.4rem .45rem}}}}
</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / QQQ + SMH 長線 × 波動率目標</div>
    <h1>QQQ + SMH 長線 × 波動率目標 — 前瞻 OOS 追蹤</h1>
    <div class="sub">50% QQQ + 50% SMH · 週線長軌閘門 × 波動率目標套袖（σ QQQ 20%／SMH 25%）· Long only · 紙上追蹤（未採用）</div>
    <div style="margin-top:.6rem;display:flex;gap:.4rem;flex-wrap:wrap">
      <a href="/long-track-qs-vt/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;background:var(--text);color:#fff;text-decoration:none">QQQ+SMH 波動率</a>
      <a href="/long-track-smh/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">SMH/QQQ STX50（實倉）</a>
      <a href="/backtest/vol_targeting/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">波動率目標回測</a>
    </div>
  </div>
</div>
<div class="container">

<div class="oos-banner">
  <span class="tag-loud">前瞻 OOS 追蹤中・未採用（PAPER TRACKING）</span>
  <div style="font-size:.86rem">這<b>不是實盤系統</b>，是把一組<b>凍結規則（{FREEZE_DATE}）</b>往前逐日記錄，看真實 OOS 表現是否與回測分布一致的紙上追蹤頁。
  規則永久凍結、不再調參。<b>複審條件：2027-01 或滿 120 個追蹤交易日</b>後，比對 OOS 與回測分布。
  實倉的長線攻擊位請見 <a href="/long-track-smh/">SMH/QQQ STX50 頁</a>；本頁的回測邏輯見 <a href="/backtest/vol_targeting/">波動率目標回測</a>。</div>
</div>

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>組合當前目標曝險</span></div>
  <div class="status-exposure">{combined:.0f}%</div>
  <div style="font-size:.8rem;color:var(--muted)">0.5 × 閘門 × 套袖，兩標的相加 · 閒置部分持現金</div>
  <div class="status-date">數據截至 {data_date}（週五收盤）· 頁面更新 {now}</div>
</div>

{change_html}

<div class="tgrid">{cards}</div>

<div class="card">
<h3>凍結規則（永久，{FREEZE_DATE}）</h3>
<div class="rule-list">
① <b>兩標的各 50%</b>，日報酬加權合成（<b>絕不直接相加 equity curve</b>；50/50 日報酬加權＝等效每日再平衡，如實揭露此假設）。<br>
② <b>週線長軌閘門</b>（W-FRI）：進場＝週收盤 &gt; W52／W104／W250 且 W104／W250 四週斜率 &gt; 0（score5）；出場＝一根週收盤 &lt; W52；<b>長多 only</b>，閘門輸出 0／1。<br>
③ <b>波動率套袖</b>：w = min(1, σ目標／RV20)，RV20＝20 日對數報酬年化波動；<b>只降不加</b>（上限 1.0）。<br>
④ <b>σ 凍結（原則法）</b>：QQQ 20%、SMH 25%（各自長期 RV 中位數取整到 5%）。掃描最佳版 Q15/S30 只放回測敏感度對照，<b>不追蹤</b>。<br>
⑤ <b>執行</b>：t 收盤訊號、t+1 收盤生效；成本 7 bps／邊。<br>
⑥ <b>最終權重</b> = 0.5 × 閘門(0/1) × 套袖權重，兩標的各自計算。<br>
<span style="color:var(--muted);font-size:.78rem">閘門為週頻（僅週五可能翻轉），套袖 RV20 為日頻（每日可能微調），故本頁每交易日更新。「可行動變化」＝閘門翻轉或任一標的最終權重變動 ≥ 10pp，觸發 email 通知。</span>
</div>
</div>

{tables}

{backtest_section()}

<div class="card">
<h3>複審條件</h3>
<div class="rule-list" style="font-size:.82rem">
於 <b>2027-01</b> 或滿 <b>120 個追蹤交易日</b>後，檢視前瞻 OOS 的 CAGR／MDD／Calmar 是否落在回測分布內。
若 OOS 顯著劣於回測（例如 Calmar 掉出回測分期區間、或 AI 牛型漏接反彈的代價超出回測所示），則記錄為「規則不穩健」；
若一致，才進入 charter 採用決策流程。<b>在此之前本頁純為研究追蹤，不構成任何倉位建議。</b>
</div>
</div>

</div>
<footer class="imq-foot">
  <div>&copy; {datetime.now().year} InvestMQuest Research · QQQ+SMH 長線 × 波動率目標（前瞻 OOS 追蹤・未採用）</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</body>
</html>"""


# ---------------------------------------------------------------------------
# change detection
# ---------------------------------------------------------------------------
def detect_changes(prev: dict, sigs: dict) -> list:
    """可行動變化＝閘門翻轉，或任一標的最終權重變動 ≥ 10pp（vs 前一日 state）。"""
    if not prev or "tickers" not in prev:
        return []
    out = []
    for t in TICKERS:
        pt = prev["tickers"].get(t)
        if not pt:
            continue
        gate_flip = bool(pt.get("gate")) != bool(sigs[t]["gate"])
        new_final = round(sigs[t]["final"] * 100, 1)
        old_final = pt.get("final_weight_pct")
        big_move = old_final is not None and abs(old_final - new_final) >= 10.0
        if gate_flip or big_move:
            parts = []
            if gate_flip:
                parts.append("閘門 " + ("出場→在場" if sigs[t]["gate"] else "在場→出場"))
            arrow = (f"最終權重 {old_final:.0f}% → {new_final:.0f}%"
                     if old_final is not None else f"最終權重 {new_final:.0f}%")
            out.append(f"<b>{t}</b>：{'、'.join(parts) + ' → ' if parts else ''}{arrow}")
    return out


def main():
    prev_state = {}
    if STATE_JSON.exists():
        try:
            prev_state = json.loads(STATE_JSON.read_text())
        except Exception:
            prev_state = {}

    sigs = {}
    for t in TICKERS:
        print(f"Fetching {t}...")
        d = compute_ticker(t)
        sigs[t] = d
        print(f"  {t}: gate={'IN' if d['gate'] else 'OUT'} RV20={d['rv20']*100:.1f}% "
              f"sleeve={d['sleeve']:.2f} -> final {d['final']*100:.0f}%")

    combined = sum(sigs[t]["final"] for t in TICKERS) * 100
    print(f"Combined target exposure: {combined:.0f}%")

    changes = detect_changes(prev_state, sigs)
    data_date = max(sigs[t]["wk_date"] for t in TICKERS)

    if changes:
        last_change_date = data_date
        last_change_desc = "; ".join(c.replace("<b>", "").replace("</b>", "") for c in changes)
        print(f"CHANGES: {last_change_desc}")
        lines = [f"QQQ+SMH 長線 × 波動率目標 — 可行動變化（數據截至 {data_date}）", ""]
        for c in changes:
            lines.append("• " + c.replace("<b>", "").replace("</b>", ""))
        lines += ["", "當前目標權重："]
        for t in TICKERS:
            d = sigs[t]
            lines.append(f"  {t}: {d['final']*100:.0f}%  "
                         f"(閘門{'在場' if d['gate'] else '出場'}, RV20 {d['rv20']*100:.1f}%, 套袖 {d['sleeve']:.2f})")
        lines += ["", f"組合目標曝險 {combined:.0f}% · 下一個交易日調整至上列目標。", "",
                  "前瞻 OOS 追蹤（未採用）。詳細： https://research.investmquest.com/long-track-qs-vt/"]
        ALERT_FILE.write_text("\n".join(lines), encoding="utf-8")
        print(f"Alert file: {ALERT_FILE}")
    else:
        last_change_date = prev_state.get("last_change_date")
        last_change_desc = prev_state.get("last_change_desc")
        if ALERT_FILE.exists():
            ALERT_FILE.unlink()
        print("No actionable change vs last run.")

    html = generate_html(sigs, changes, last_change_date)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state_json = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": data_date,
        "freeze_date": FREEZE_DATE,
        "status": "forward OOS paper tracking, not adopted",
        "last_change_date": last_change_date,
        "last_change_desc": last_change_desc,
        "weights": WEIGHTS,
        "combined_exposure_pct": round(combined, 1),
        "tickers": {
            t: {
                "gate": sigs[t]["gate"],
                "sigma_target_pct": round(SIGMA[t] * 100, 1),
                "rv20_pct": round(sigs[t]["rv20"] * 100, 2),
                "sleeve_weight": round(sigs[t]["sleeve"], 4),
                "final_weight_pct": round(sigs[t]["final"] * 100, 1),
                "wk_date": sigs[t]["wk_date"],
                "wk_close": round(sigs[t]["wk_close"], 2),
                "w52": round(sigs[t]["w52"], 2),
                "w104": round(sigs[t]["w104"], 2),
                "w250": round(sigs[t]["w250"], 2),
                "s104_pos": sigs[t]["s104_pos"],
                "s250_pos": sigs[t]["s250_pos"],
            } for t in TICKERS
        },
    }
    STATE_JSON.write_text(json.dumps(state_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


if __name__ == "__main__":
    main()
