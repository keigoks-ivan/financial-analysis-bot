#!/usr/bin/env python3
"""
Long Track SMH/QQQ — STX50 Signal Status Page Generator
========================================================
Fetches SMH, QQQ daily OHLC + SHY/BIL cash, computes the adopted STX50
position per ticker and renders docs/long-track-smh/index.html.

STX50 (adopted 2026-06-13, owner decision):
    pos = 0.5 * E3 + 0.5 * (E3 if ST_up else 0)
    E3 = mean of {W40, W52, 12m TSMOM} 0/1 signals (each 1/3)
    ST = weekly Supertrend(ATR 10, mult 3) direction — exit gate on half
         the book; the gate only ever reduces exposure.

Signal definitions are copied verbatim from the backtest authority
(v7-backtest src/long_track_backtest/ensemble_experiment.py:build_signals
and supertrend_experiment.py:supertrend_direction); keep them in sync if
the adopted rule ever changes.

OOS tracking. This is an EXPOSURE-state readout, not a daily trade
trigger — signals only move ~2x/year per ticker.

Schedule: Fridays after US close (weekly W40/W52 update; TSMOM is month-end).
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

# Canonical site header (single source: scripts/site_nav.py)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("market", "ltsmh")

OUTPUT = Path(__file__).parent.parent / "docs" / "long-track-smh" / "index.html"
STATE_JSON = Path(__file__).parent.parent / "docs" / "long-track-smh" / "state.json"

TICKERS = ["SMH", "QQQ"]
WEIGHTS = {"SMH": 0.5, "QQQ": 0.5}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def _close(df) -> pd.Series:
    c = df["Close"]
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:, 0]
    return c.dropna()


def fetch_close(ticker: str) -> pd.Series:
    return _close(fetch_ohlc(ticker))


def fetch_ohlc(ticker: str) -> pd.DataFrame:
    end = datetime.now() + timedelta(days=1)
    start = end - timedelta(days=365 * 6)  # 6y: covers 52w MA + 12m TSMOM + ATR warmup
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def supertrend_state(df: pd.DataFrame, period: int = 10, mult: float = 3.0):
    """Weekly Supertrend direction — verbatim port of
    v7-backtest supertrend_experiment.supertrend_direction (TradingView
    final-band formula incl. reset).  6y of weekly bars contains several
    flips, so the recursive state matches the full-history computation."""
    wk = pd.DataFrame({
        "High": df["High"].resample("W-FRI").max(),
        "Low": df["Low"].resample("W-FRI").min(),
        "Close": df["Close"].resample("W-FRI").last(),
    }).dropna(subset=["Close"])
    h, l, c = wk["High"].values, wk["Low"].values, wk["Close"].values
    n = len(wk)
    c_prev = np.roll(c, 1)
    c_prev[0] = c[0]
    tr = np.maximum(h - l, np.maximum(np.abs(h - c_prev), np.abs(l - c_prev)))
    atr = pd.Series(tr, index=wk.index).ewm(alpha=1 / period, adjust=False,
                                            min_periods=period).mean().values
    mid = (h + l) / 2
    bub, blb = mid + mult * atr, mid - mult * atr
    fub = np.full(n, np.nan)
    flb = np.full(n, np.nan)
    direction = np.zeros(n)
    st = np.full(n, np.nan)
    started = False
    for i in range(n):
        if np.isnan(atr[i]):
            continue
        if not started:
            fub[i], flb[i] = bub[i], blb[i]
            direction[i] = 1.0 if c[i] > fub[i] else -1.0
            st[i] = flb[i] if direction[i] > 0 else fub[i]
            started = True
            continue
        fub[i] = bub[i] if (bub[i] < fub[i - 1] or c[i - 1] > fub[i - 1]) else fub[i - 1]
        flb[i] = blb[i] if (blb[i] > flb[i - 1] or c[i - 1] < flb[i - 1]) else flb[i - 1]
        if st[i - 1] == fub[i - 1]:
            direction[i] = 1.0 if c[i] > fub[i] else -1.0
        else:
            direction[i] = -1.0 if c[i] < flb[i] else 1.0
        st[i] = flb[i] if direction[i] > 0 else fub[i]
    return bool(direction[-1] > 0), float(st[-1])


def load_cash_close() -> pd.Series:
    """SHY before BIL inception (2007-05), BIL after — same splice as the backtest.
    For a 6-year live window this is effectively all BIL, but keep the splice
    faithful in case the fetch window ever predates BIL."""
    shy, bil = fetch_close("SHY"), fetch_close("BIL")
    if len(bil) == 0:
        return shy
    return pd.concat([shy[shy.index < bil.index[0]], bil]).sort_index()


# ---------------------------------------------------------------------------
# Signal — verbatim from ensemble_experiment.build_signals
# ---------------------------------------------------------------------------
def compute_signals(px: pd.Series, cash: pd.Series,
                    st_on: bool, st_level: float) -> dict:
    wk = px.resample("W-FRI").last().dropna()
    mo = px.resample("ME").last().dropna()
    cash_m = cash.resample("ME").last()

    ma40 = wk.rolling(40).mean()
    ma52 = wk.rolling(52).mean()
    w40 = (wk > ma40)
    w52 = (wk > ma52)

    mom = mo / mo.shift(12) - 1
    cash_mom = (cash_m / cash_m.shift(12) - 1).reindex(mo.index).fillna(0)
    ts = mom > cash_mom

    # current (last completed weekly / monthly bar — Action runs Fri after close)
    w40_now = bool(w40.iloc[-1])
    w52_now = bool(w52.iloc[-1])
    ts_now = bool(ts.iloc[-1])
    e3 = (int(w40_now) + int(w52_now) + int(ts_now)) / 3.0
    # STX50 (adopted 2026-06-13): ST gate on half the book, reduce-only
    pos = 0.5 * e3 + 0.5 * (e3 if st_on else 0.0)

    # recent 8 weekly bars for the trajectory table
    recent = []
    for i in range(-8, 0):
        recent.append({
            "date": wk.index[i].strftime("%Y-%m-%d"),
            "close": float(wk.iloc[i]),
            "ma40": float(ma40.iloc[i]),
            "ma52": float(ma52.iloc[i]),
            "w40": bool(w40.iloc[i]),
            "w52": bool(w52.iloc[i]),
            "pct40": (float(wk.iloc[i]) / float(ma40.iloc[i]) - 1) * 100,
            "pct52": (float(wk.iloc[i]) / float(ma52.iloc[i]) - 1) * 100,
        })

    return {
        "ticker": None,
        "w40": w40_now, "w52": w52_now, "tsmom": ts_now,
        "st": st_on, "st_level": st_level, "e3": e3,
        "pos": pos,
        "wk_close": float(wk.iloc[-1]),
        "wk_date": wk.index[-1].strftime("%Y-%m-%d"),
        "ma40": float(ma40.iloc[-1]),
        "ma52": float(ma52.iloc[-1]),
        "mom12": float(mom.iloc[-1]) * 100,
        "cash_mom12": float(cash_mom.iloc[-1]) * 100,
        "mo_date": mo.index[-1].strftime("%Y-%m-%d"),
        "recent": recent,
    }


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
def fmt_pct(v, dp=2):
    return f"{'+' if v >= 0 else ''}{v:.{dp}f}%"


def pos_color(pos):
    if pos >= 0.99:
        return "green"
    if pos >= 0.66:
        return "blue"
    if pos >= 0.33:
        return "amber"
    return "red"


def sig_bulb(label, on, detail):
    cls = "on" if on else "off"
    mark = "✓" if on else "✕"
    return f"""<div class="sig {cls}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">{label}</span><span class="sig-mark">{mark}</span></div>
      <div class="sig-detail">{detail}</div>
    </div>"""


def ticker_card(t: str, d: dict) -> str:
    col = pos_color(d["pos"])
    pos_pct = d["pos"] * 100
    bulbs = "".join([
        sig_bulb("W40", d["w40"],
                 f"週收 {d['wk_close']:.2f} vs 40週均 {d['ma40']:.2f} "
                 f"<b style='color:var(--{'green' if d['w40'] else 'red'})'>{fmt_pct((d['wk_close']/d['ma40']-1)*100)}</b>"),
        sig_bulb("W52", d["w52"],
                 f"週收 {d['wk_close']:.2f} vs 52週均 {d['ma52']:.2f} "
                 f"<b style='color:var(--{'green' if d['w52'] else 'red'})'>{fmt_pct((d['wk_close']/d['ma52']-1)*100)}</b>"),
        sig_bulb("TSMOM", d["tsmom"],
                 f"12m 報酬 <b>{fmt_pct(d['mom12'])}</b> vs 現金 <b>{fmt_pct(d['cash_mom12'])}</b>"),
        sig_bulb("ST 閘門 (10,3)", d["st"],
                 f"週收 {d['wk_close']:.2f} vs Supertrend {d['st_level']:.2f} — "
                 f"{'開(受閘半倉在場)' if d['st'] else '關(受閘半倉出場)'}"),
    ])
    return f"""<div class="tcard">
  <div class="tcard-hdr">
    <span class="tname">{t}</span>
    <span class="pos-badge pos-{col}">{pos_pct:.0f}% 倉位</span>
  </div>
  <div class="tcard-sub">E3 {int(d['w40'])+int(d['w52'])+int(d['tsmom'])}/3 綠燈 × ST 閘門{'開' if d['st'] else '關'} → 倉位 {d['pos']*100:.0f}% · 閒置部分持 SHY/BIL</div>
  <div class="sig-row">{bulbs}</div>
</div>"""


def recent_table(t: str, d: dict) -> str:
    rows = ""
    for r in d["recent"]:
        c40 = "var(--green)" if r["w40"] else "var(--red)"
        c52 = "var(--green)" if r["w52"] else "var(--red)"
        rows += f"""<tr>
  <td>{r['date']}</td><td>{r['close']:.2f}</td>
  <td>{r['ma40']:.2f}</td><td style="color:{c40}">{fmt_pct(r['pct40'])}</td>
  <td>{r['ma52']:.2f}</td><td style="color:{c52}">{fmt_pct(r['pct52'])}</td>
  <td><span class="tag" style="background:var(--{'green' if r['w40'] else 'red'}-bg);color:var(--{'green' if r['w40'] else 'red'}-text)">W40 {'✓' if r['w40'] else '✕'}</span>
      <span class="tag" style="background:var(--{'green' if r['w52'] else 'red'}-bg);color:var(--{'green' if r['w52'] else 'red'}-text)">W52 {'✓' if r['w52'] else '✕'}</span></td>
</tr>\n"""
    return f"""<div class="card">
<h3>{t} — 近 8 週軌跡(週線)</h3>
<table><thead><tr><th>週五</th><th>收盤</th><th>40週均</th><th>距離</th><th>52週均</th><th>距離</th><th>週線訊號</th></tr></thead>
<tbody>{rows}</tbody></table>
<div style="font-size:.72rem;color:var(--muted);margin-top:.5rem">TSMOM 為月頻(月底判定),不在此週線表中;見上方卡片當前值。</div>
</div>"""


def generate_html(sigs: dict) -> str:
    combined = sum(WEIGHTS[t] * sigs[t]["pos"] for t in TICKERS) * 100
    ccol = pos_color(combined / 100)
    data_date = max(sigs[t]["wk_date"] for t in TICKERS)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    cards = "".join(ticker_card(t, sigs[t]) for t in TICKERS)
    tables = "".join(recent_table(t, sigs[t]) for t in TICKERS)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>長線訊號 SMH/QQQ(STX50)即時狀態 | InvestMQuest Research</title>
  <meta name="description" content="SystemProtocol v7 長線 STX50 — 50/50 SMH/QQQ 當前訊號與倉位">
  <style>
:root{{--brand:#1a56db;--bg:#f8f9fa;--card:#fff;--text:#1a1a2e;--muted:#6b7280;--border:#e2e5e9;
  --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
  --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--red-text:#991b1b;
  --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e;
  --blue:#2563eb;--blue-bg:#eff6ff;--blue-border:#93c5fd;--blue-text:#1e40af}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',sans-serif;
  background:var(--bg);color:var(--text);line-height:1.65;font-size:14px}}
a{{color:var(--brand);text-decoration:none}}a:hover{{text-decoration:underline}}
.container{{max-width:1140px;margin:0 auto;padding:0 1.5rem}}
.page-hdr{{padding:1.5rem 0 1.2rem;background:#fff;border-bottom:1px solid var(--border)}}
.page-hdr h1{{font-size:1.5rem;font-weight:700;letter-spacing:-.03em}}
.page-hdr .sub{{color:var(--muted);font-size:.85rem;margin-top:.2rem}}
.crumb{{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}}
.crumb a{{color:var(--muted)}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.card h3{{font-size:.95rem;font-weight:600;margin-bottom:.75rem}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th,td{{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}}
th{{background:#f8f9fa;font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}}
td{{font-variant-numeric:tabular-nums}}
tbody tr:hover td{{background:#f3f4f6}}
.tag{{display:inline-block;padding:.12rem .5rem;border-radius:4px;font-size:.7rem;font-weight:600}}
footer{{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1rem 0;font-size:.75rem;margin-top:1rem}}
.banner{{background:var(--amber-bg);border:1px solid var(--amber-border);color:var(--amber-text);
  border-radius:8px;padding:.7rem 1rem;font-size:.8rem;margin:1rem 0}}
.status-hero{{padding:2rem 0 1rem;text-align:center}}
.status-badge{{display:inline-flex;align-items:center;gap:.75rem;padding:1rem 2.5rem;border-radius:16px;
  font-size:1.4rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.5rem}}
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
.tcard{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:1.1rem;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.tcard-hdr{{display:flex;align-items:center;justify-content:space-between;margin-bottom:.2rem}}
.tname{{font-size:1.3rem;font-weight:800;letter-spacing:-.02em}}
.pos-badge{{font-size:.95rem;font-weight:700;padding:.25rem .7rem;border-radius:8px}}
.pos-green{{background:var(--green-bg);color:var(--green-text)}}
.pos-blue{{background:var(--blue-bg);color:var(--blue-text)}}
.pos-amber{{background:var(--amber-bg);color:var(--amber-text)}}
.pos-red{{background:var(--red-bg);color:var(--red-text)}}
.tcard-sub{{font-size:.75rem;color:var(--muted);margin-bottom:.75rem}}
.sig-row{{display:grid;grid-template-columns:1fr;gap:.5rem}}
.sig{{border:1px solid var(--border);border-radius:8px;padding:.55rem .7rem;background:#fff}}
.sig.on{{border-color:var(--green-border);background:var(--green-bg)}}
.sig.off{{border-color:var(--red-border);background:var(--red-bg)}}
.sig-top{{display:flex;align-items:center;gap:.5rem}}
.sig-dot{{width:11px;height:11px;border-radius:50%}}
.sig.on .sig-dot{{background:var(--green)}}.sig.off .sig-dot{{background:var(--red)}}
.sig-name{{font-weight:700;font-size:.85rem}}
.sig-mark{{margin-left:auto;font-weight:800}}
.sig.on .sig-mark{{color:var(--green)}}.sig.off .sig-mark{{color:var(--red)}}
.sig-detail{{font-size:.74rem;color:var(--muted);margin-top:.2rem;font-variant-numeric:tabular-nums}}
.rule-list{{font-size:.82rem;line-height:1.9}}
.rule-list b{{color:var(--text)}}
@media(max-width:768px){{
  .tgrid{{grid-template-columns:1fr}}
  .status-exposure{{font-size:2rem}}
  table{{font-size:.74rem}}th,td{{padding:.4rem .45rem}}
}}
</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / 長線訊號 SMH/QQQ</div>
    <h1>長線訊號 — SMH/QQQ(STX50)即時狀態</h1>
    <div class="sub">SystemProtocol v7 · 50% SMH + 50% QQQ · E3 三訊號各 1/3 + ST(10,3) 半倉出場閘門 · Long only</div>
  </div>
</div>
<div class="container">

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>組合當前曝險</span></div>
  <div class="status-exposure">{combined:.0f}%</div>
  <div style="font-size:.8rem;color:var(--muted)">50% SMH + 50% QQQ · 閒置部分持 SHY/BIL</div>
  <div class="status-date">數據截至 {data_date}(週五收盤)· 頁面更新 {now}</div>
</div>

<div class="banner">
  <b>STX50 長線訊號 · 2026-06-13 採用 · OOS 追蹤中。</b>
  這是<b>曝險狀態讀數</b>,不是每日交易動作 —— 訊號為週/月頻,每標的年換手約 2.4 邊,
  多數日子不會變化。SMH 為高 β 半導體,集中度高;此結構在半導體寒冬的 whipsaw 從未實測,
  解讀請對照 <a href="/backtest/long_track_smh/">回測頁</a> 的 caveat。
</div>

<div class="tgrid">{cards}</div>

<div class="card">
<h3>規則(每標的倉位 = 0.5 × E3 + 0.5 × (ST 開 ? E3 : 0))</h3>
<div class="rule-list">
① <b>W40</b>:週線收盤 &gt; 40 週均線<br>
② <b>W52</b>:週線收盤 &gt; 52 週均線<br>
③ <b>TSMOM</b>:過去 12 個月總報酬 &gt; 現金(SHY/BIL)同期 12 個月報酬,<b>月頻、月底判定</b><br>
④ <b>ST 閘門</b>:週線 Supertrend(ATR 10、乘數 3,TradingView final-band 公式)方向 —
翻空時受閘半倉出場、翻多時回來;<b>閘門只減倉、永不加倉</b><br>
<span style="color:var(--muted);font-size:.78rem">E3 = 三訊號平均(0/33%/67%/100% 四檔);ST 關閘時倉位折半(0/17%/33%/50%)。
兩標的各自獨立跑訊號與資金,日報酬 50/50 加權合成。成本單邊 7bps 計於 |倉位變動|。2026-06-13 採用,對照線為 E3。</span>
</div>
</div>

{tables}

</div>
<footer>
  &copy; {datetime.now().year} InvestMQuest Research · 長線訊號 SMH/QQQ(STX50)· 真實 yfinance 資料 ·
  訊號定義同步自 v7-backtest ensemble_experiment.build_signals + supertrend_experiment · 每週五美股收盤後自動更新
</footer>
</body>
</html>"""


def main():
    sigs = {}
    print("Fetching cash (SHY/BIL)...")
    cash = load_cash_close()
    for t in TICKERS:
        print(f"Fetching {t}...")
        df = fetch_ohlc(t)
        px = _close(df)
        print(f"  {len(px)} daily bars")
        st_on, st_level = supertrend_state(df)
        d = compute_signals(px, cash, st_on, st_level)
        d["ticker"] = t
        sigs[t] = d
        print(f"  {t}: W40={d['w40']} W52={d['w52']} TSMOM={d['tsmom']} ST={d['st']} -> pos {d['pos']*100:.0f}%")

    combined = sum(WEIGHTS[t] * sigs[t]["pos"] for t in TICKERS) * 100
    print(f"Combined exposure: {combined:.0f}%")

    html = generate_html(sigs)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state_json = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": max(sigs[t]["wk_date"] for t in TICKERS),
        "weights": WEIGHTS,
        "combined_exposure_pct": round(combined, 1),
        "tickers": {
            t: {
                "position_pct": round(sigs[t]["pos"] * 100, 1),
                "w40": sigs[t]["w40"], "w52": sigs[t]["w52"], "tsmom": sigs[t]["tsmom"],
                "st_gate": sigs[t]["st"], "st_level": round(sigs[t]["st_level"], 2),
                "e3_pct": round(sigs[t]["e3"] * 100, 1),
                "wk_close": round(sigs[t]["wk_close"], 2),
                "ma40": round(sigs[t]["ma40"], 2),
                "ma52": round(sigs[t]["ma52"], 2),
                "mom12_pct": round(sigs[t]["mom12"], 2),
                "cash_mom12_pct": round(sigs[t]["cash_mom12"], 2),
            } for t in TICKERS
        },
    }
    STATE_JSON.write_text(json.dumps(state_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


if __name__ == "__main__":
    main()
