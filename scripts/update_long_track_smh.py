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
from pandas.tseries.offsets import BDay

# Canonical site header (single source: scripts/site_nav.py)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "ltsmh")

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
    dir_s = pd.Series(direction, index=wk.index)
    st_s = pd.Series(st, index=wk.index)
    return bool(direction[-1] > 0), float(st[-1]), dir_s, st_s


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
                    st_on: bool, st_level: float,
                    st_dir_s=None, st_lvl_s=None) -> dict:
    wk = px.resample("W-FRI").last().dropna()
    mo = px.resample("ME").last().dropna()
    # TSMOM timing sync with the backtest authority (ensemble_experiment
    # signal_daily): the monthly signal is DECIDED at each month's last trading
    # session and effective the next day; mid-month the effective signal is the
    # last COMPLETED month's.  resample("ME") makes the trailing bar a partial
    # month, so drop it unless today is the month-end session (BDay approx,
    # same convention as update_turtle_sleeve.is_month_end_session).
    if len(px) and (px.index[-1] + BDay(1)).month == px.index[-1].month:
        mo = mo.iloc[:-1]
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
        wdate = wk.index[i]
        r = {
            "date": wdate.strftime("%Y-%m-%d"),
            "close": float(wk.iloc[i]),
            "ma40": float(ma40.iloc[i]),
            "ma52": float(ma52.iloc[i]),
            "w40": bool(w40.iloc[i]),
            "w52": bool(w52.iloc[i]),
            "pct40": (float(wk.iloc[i]) / float(ma40.iloc[i]) - 1) * 100,
            "pct52": (float(wk.iloc[i]) / float(ma52.iloc[i]) - 1) * 100,
        }
        if st_dir_s is not None and wdate in st_dir_s.index:
            r["st"] = bool(st_dir_s.loc[wdate] > 0)
            r["st_lvl"] = float(st_lvl_s.loc[wdate])
            r["pct_st"] = (r["close"] / r["st_lvl"] - 1) * 100
        recent.append(r)

    return {
        "ticker": None,
        "w40": w40_now, "w52": w52_now, "tsmom": ts_now,
        "st": st_on, "st_level": st_level, "e3": e3,
        "pos": pos,
        "near": {   # within 2% (2pp for TSMOM) of flipping
            "w40": abs(float(wk.iloc[-1]) / float(ma40.iloc[-1]) - 1) < 0.02,
            "w52": abs(float(wk.iloc[-1]) / float(ma52.iloc[-1]) - 1) < 0.02,
            "tsmom": abs(float(mom.iloc[-1]) - float(cash_mom.reindex(mo.index).iloc[-1])) < 0.02,
            "st": abs(float(wk.iloc[-1]) / st_level - 1) < 0.02,
        },
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


def sig_bulb(label, on, detail, near=False):
    cls = "on" if on else "off"
    mark = "✓" if on else "✕"
    warn = ' <span style="color:var(--amber);font-weight:700;font-size:.72rem">⚠ 接近翻轉</span>' if near else ""
    return f"""<div class="sig {cls}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">{label}</span>{warn}<span class="sig-mark">{mark}</span></div>
      <div class="sig-detail">{detail}</div>
    </div>"""


def ticker_card(t: str, d: dict) -> str:
    col = pos_color(d["pos"])
    pos_pct = d["pos"] * 100
    bulbs = "".join([
        sig_bulb("W40", d["w40"],
                 f"週收 {d['wk_close']:.2f} vs 40週均 {d['ma40']:.2f} "
                 f"<b style='color:var(--{'green' if d['w40'] else 'red'})'>{fmt_pct((d['wk_close']/d['ma40']-1)*100)}</b>",
                 near=d["near"]["w40"]),
        sig_bulb("W52", d["w52"],
                 f"週收 {d['wk_close']:.2f} vs 52週均 {d['ma52']:.2f} "
                 f"<b style='color:var(--{'green' if d['w52'] else 'red'})'>{fmt_pct((d['wk_close']/d['ma52']-1)*100)}</b>",
                 near=d["near"]["w52"]),
        sig_bulb("TSMOM", d["tsmom"],
                 f"12m 報酬 <b>{fmt_pct(d['mom12'])}</b> vs 現金 <b>{fmt_pct(d['cash_mom12'])}</b>",
                 near=d["near"]["tsmom"]),
        sig_bulb("ST 閘門 (10,3)", d["st"],
                 f"週收 {d['wk_close']:.2f} vs Supertrend {d['st_level']:.2f} "
                 f"<b style='color:var(--{'green' if d['st'] else 'red'})'>{fmt_pct((d['wk_close']/d['st_level']-1)*100)}</b> — "
                 f"{'開(受閘半倉在場)' if d['st'] else '關(受閘半倉出場)'}",
                 near=d["near"]["st"]),
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
        st_cell = "<td>—</td>"
        if "st" in r:
            cst = "green" if r["st"] else "red"
            st_cell = (f'<td>{r["st_lvl"]:.2f} <span class="tag" '
                       f'style="background:var(--{cst}-bg);color:var(--{cst}-text)">'
                       f'ST {"✓" if r["st"] else "✕"} {fmt_pct(r["pct_st"], 1)}</span></td>')
        rows += f"""<tr>
  <td>{r['date']}</td><td>{r['close']:.2f}</td>
  <td>{r['ma40']:.2f}</td><td style="color:{c40}">{fmt_pct(r['pct40'])}</td>
  <td>{r['ma52']:.2f}</td><td style="color:{c52}">{fmt_pct(r['pct52'])}</td>
  {st_cell}
  <td><span class="tag" style="background:var(--{'green' if r['w40'] else 'red'}-bg);color:var(--{'green' if r['w40'] else 'red'}-text)">W40 {'✓' if r['w40'] else '✕'}</span>
      <span class="tag" style="background:var(--{'green' if r['w52'] else 'red'}-bg);color:var(--{'green' if r['w52'] else 'red'}-text)">W52 {'✓' if r['w52'] else '✕'}</span></td>
</tr>\n"""
    return f"""<div class="card">
<h3>{t} — 近 8 週軌跡(週線)</h3>
<table><thead><tr><th>週五</th><th>收盤</th><th>40週均</th><th>距離</th><th>52週均</th><th>距離</th><th>Supertrend</th><th>週線訊號</th></tr></thead>
<tbody>{rows}</tbody></table>
<div style="font-size:.72rem;color:var(--muted);margin-top:.5rem">TSMOM 為月頻(月底判定),不在此週線表中；見上方卡片當前值。</div>
</div>"""


def generate_html(sigs: dict, changes: list[str] | None = None,
                  last_change_date: str | None = None) -> str:
    changes = changes or []
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
  <title>美股長線訊號 SMH/QQQ(STX50)即時狀態 | InvestMQuest Research</title>
  <meta name="description" content="SystemProtocol v7 長線 STX50 — 50/50 SMH/QQQ 當前訊號與倉位">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/imq-base.css">
  <style>
:root{{--brand:#0d2244;--bg:#f7f3ea;--card:#ffffff;--text:#0c1521;--muted:#9aa7b8;--border:#e5dfd0;
  --green:#15803d;--green-bg:#eafaef;--green-border:var(--line);--green-text:#15803d;
  --red:#b91c1c;--red-bg:#fbeceb;--red-border:var(--line);--red-text:#b91c1c;
  --amber:#a16207;--amber-bg:#fbf3df;--amber-border:var(--line);--amber-text:#a16207;
  --blue:#15803d;--blue-bg:#e8eef5;--blue-border:var(--line);--blue-text:#15803d}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',sans-serif;
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
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th,td{{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}}
th{{background:transparent;font-family:var(--mono);font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}}
td{{font-variant-numeric:tabular-nums}}
tbody tr:hover td{{background:#fbf8f1}}
.tag{{display:inline-block;padding:.12rem .5rem;border-radius:6px;font-size:.7rem;font-weight:600}}
footer{{background:var(--card);border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1rem 0;font-size:.75rem;margin-top:1rem}}
.banner{{background:var(--amber-bg);border:1px solid var(--amber-border);color:var(--amber-text);
  border-radius:var(--r);padding:.7rem 1rem;font-size:.8rem;margin:1rem 0}}
.status-hero{{padding:2rem 0 1rem;text-align:center}}
.status-badge{{display:inline-flex;align-items:center;gap:.75rem;padding:1rem 2.5rem;border-radius:var(--r);
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
.tcard{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem;box-shadow:var(--sh-1)}}
.tcard-hdr{{display:flex;align-items:center;justify-content:space-between;margin-bottom:.2rem}}
.tname{{font-size:1.3rem;font-weight:800;letter-spacing:-.02em}}
.pos-badge{{font-size:.95rem;font-weight:700;padding:.25rem .7rem;border-radius:6px}}
.pos-green{{background:var(--green-bg);color:var(--green-text)}}
.pos-blue{{background:var(--blue-bg);color:var(--blue-text)}}
.pos-amber{{background:var(--amber-bg);color:var(--amber-text)}}
.pos-red{{background:var(--red-bg);color:var(--red-text)}}
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
    <div class="crumb"><a href="/">首頁</a> / 美股長線訊號 SMH/QQQ</div>
    <h1>美股長線訊號 — SMH/QQQ(STX50)即時狀態</h1>
    <div class="sub">SystemProtocol v7 · 50% SMH + 50% QQQ · E3 三訊號各 1/3 + ST(10,3) 半倉出場閘門 · Long only</div>
    <div style="margin-top:.6rem;display:flex;gap:.4rem">
      <a href="/long-track-smh/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;background:var(--text);color:#fff;text-decoration:none">美股</a>
      <a href="/long-track-tw/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">台股</a>
    </div>
  </div>
</div>
<div class="container">

<div style="background:var(--amber-bg);border:2px solid var(--amber-border);color:var(--amber-text);border-radius:10px;padding:.9rem 1.2rem;margin:1rem 0;font-size:.92rem;font-weight:600;text-align:center">2026-07-18 起本頁非實單系統（實單已改為 <a href="/long-track-w52-adaptive/" style="color:var(--amber-text);text-decoration:underline">W52 × 自適應波動率 150%</a>）；本頁保留每日更新作對照。</div>

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>組合當前曝險</span></div>
  <div class="status-exposure">{combined:.0f}%</div>
  <div style="font-size:.8rem;color:var(--muted)">50% SMH + 50% QQQ · 閒置部分持 SHY/BIL</div>
  <div class="status-date">數據截至 {data_date}(週五收盤)· 頁面更新 {now}</div>
</div>

{('<div style="background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem"><b style="color:var(--red-text)">本週訊號變化</b><br>' + "<br>".join(changes) + '<br><span style="font-size:.78rem;color:var(--muted)">下一個交易日將部位調整至上列目標。</span></div>') if changes else ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">本週無訊號變化' + (f"(上次變化：{last_change_date})" if last_change_date else "") + '</div>')}

<div class="banner">
  <b>STX50 長線訊號 · 2026-06-13 採用 · 2026-07-18 起改為對照（實單改用 <a href="/long-track-w52-adaptive/">W52 × 自適應波動率 150%</a>）。</b>
  這是<b>曝險狀態讀數</b>,不是每日交易動作 —— 訊號為週/月頻，每標的年換手約 2.4 邊，
  多數日子不會變化。SMH 為高 β 半導體，集中度高；此結構在半導體寒冬的 whipsaw 從未實測，
  解讀請對照 <a href="/backtest/long_track_smh/">回測頁</a> 的 caveat。
</div>

<div style="text-align:center;font-size:.82rem;margin:.2rem 0 1rem;padding:.6rem;background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px">
  如需在此疊加槓桿，參見 <a href="/long-track-smh/leverage/" style="font-weight:600">vol-target 槓桿層(實驗·紙上讀數)</a>
</div>

<div class="tgrid">{cards}</div>

<div class="card">
<h3>規則(每標的倉位 = 0.5 × E3 + 0.5 × (ST 開 ? E3 : 0))</h3>
<div class="rule-list">
① <b>W40</b>:週線收盤 &gt; 40 週均線<br>
② <b>W52</b>:週線收盤 &gt; 52 週均線<br>
③ <b>TSMOM</b>:過去 12 個月總報酬 &gt; 現金(SHY/BIL)同期 12 個月報酬，<b>月頻、月底判定</b><br>
④ <b>ST 閘門</b>:週線 Supertrend(ATR 10、乘數 3,TradingView final-band 公式)方向 —
翻空時受閘半倉出場、翻多時回來；<b>閘門只減倉、永不加倉</b><br>
<span style="color:var(--muted);font-size:.78rem">E3 = 三訊號平均(0/33%/67%/100% 四檔);ST 關閘時倉位折半(0/17%/33%/50%)。
兩標的各自獨立跑訊號與資金，日報酬 50/50 加權合成。成本單邊 7bps 計於 |倉位變動|。2026-06-13 採用，對照線為 E3。<br>
ST(10,3) 的 3×3 參數格檢驗（2026-07-02）：方向穩健 —— 9 點中 8 點 Calmar 不輸同 CAGR 現金對照；
幅度不穩健 —— (10,3) 的 +0.07 是單點最佳（次佳 +0.04、中位數 +0.02），headline 改善約一半來自恰好選中 (10,3)，
詳見 <a href="/backtest/long_track_smh/">回測頁</a>。</span>
</div>
</div>

{tables}

<div class="card">
<h3>訊號流程說明 — 出場的半倉怎麼買回來？(以 2026 春季 QQQ 為實例)</h3>
<div class="rule-list" style="font-size:.8rem">
兩套訊號<b>完全獨立、各自演</b>:E3 的三個訊號自己進出(每跌破/收復一條線動 1/3),
ST 閘門自己開關(受閘半倉跟著 E3 或歸零)。<b>買回訊號就是 Supertrend 自己翻多的那一週收盤</b>
(週收上穿被棘輪壓低的上軌)— 不需要等均線重新給進場訊號，閘門是「狀態」不是一次性停損。<br>
實務上每週五收盤只算一個數字：<b>目標倉位 = 0.5×E3 + 0.5×(ST開 ? E3 : 0)</b>,
與上週目標的差額就是下一個交易日要下的單。本頁頂部的倉位數字即當前目標。
</div>
<table style="margin-top:.6rem">
<thead><tr><th>決策日(週收盤)</th><th>部位</th><th>發生了什麼</th></tr></thead>
<tbody>
<tr><td>2026-03-20</td><td>100% → 67%</td><td>E3 自己先出了 ⅓(W40 跌破),ST 還在多方。兩個半邊都縮：0.5×⅔ + 0.5×⅔</td></tr>
<tr><td>2026-03-27</td><td>67% → 17%</td><td><b>ST 翻空</b>(對應 TradingView 圖上的 Sell 標籤，週收 562.58)+ E3 再掉到 ⅓。受閘半倉歸零：0.5×⅓ + 0</td></tr>
<tr><td>2026-04-02</td><td>17% → 33%</td><td>E3 回到 ⅔(W52 收復),ST 仍空 → 受閘半倉不跟</td></tr>
<tr><td>2026-04-10</td><td>33% → 50%</td><td>E3 回滿 3/3,ST 仍空。未受閘半倉滿、受閘半倉仍是 0</td></tr>
<tr><td>2026-04-17</td><td>50% → 100%</td><td><b>ST 翻多(對應 TradingView 圖上的 Buy 標籤，週收 648.85)→ 受閘半倉一次買回</b></td></tr>
</tbody>
</table>
<div style="font-size:.74rem;color:var(--amber-text);background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:6px;padding:.5rem .8rem;margin-top:.6rem">
<b>實際結果：</b>這次受閘半倉 562 附近出、648 買回 — V 型反轉裡閘門是付錢的(高 15% 追回)。
ST 閘門賺錢的場景是 2022 型持續陰跌(出場後不必更高買回);全期統計淨賺(MDD -26.9% → -21.9%、Calmar 0.56 → 0.63),
但個別 episode 會像這次一樣難看。OOS 重審追蹤的就是這個比例有沒有走樣 — 對照線為 E3,見
<a href="/backtest/long_track_smh/">回測頁</a>。
</div>
</div>

</div>
<footer class="imq-foot">
  <div>&copy; {datetime.now().year} InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</body>
</html>"""


SIG_LABEL = {"w40": "W40", "w52": "W52", "tsmom": "TSMOM", "st_gate": "ST 閘門"}


def detect_changes(prev: dict, sigs: dict) -> list[str]:
    """Compare last run's state.json against this run; return change strings."""
    if not prev or "tickers" not in prev:
        return []
    out = []
    for t in TICKERS:
        pt = prev["tickers"].get(t)
        if not pt:
            continue
        cur = {"w40": sigs[t]["w40"], "w52": sigs[t]["w52"],
               "tsmom": sigs[t]["tsmom"], "st_gate": sigs[t]["st"]}
        flips = [f"{SIG_LABEL[k]} {'✕→✓' if cur[k] else '✓→✕'}"
                 for k in cur if k in pt and bool(pt[k]) != bool(cur[k])]
        new_pos = round(sigs[t]["pos"] * 100, 1)
        old_pos = pt.get("position_pct")
        if flips or (old_pos is not None and abs(old_pos - new_pos) > 0.5):
            arrow = (f"倉位 {old_pos:.0f}% → {new_pos:.0f}%"
                     if old_pos is not None else f"倉位 {new_pos:.0f}%")
            out.append(f"<b>{t}</b>:{'、'.join(flips) if flips else '訊號未翻轉'} → {arrow}")
    return out


def main():
    sigs = {}
    prev_state = {}
    if STATE_JSON.exists():
        try:
            prev_state = json.loads(STATE_JSON.read_text())
        except Exception:
            prev_state = {}
    print("Fetching cash (SHY/BIL)...")
    cash = load_cash_close()
    for t in TICKERS:
        print(f"Fetching {t}...")
        df = fetch_ohlc(t)
        px = _close(df)
        print(f"  {len(px)} daily bars")
        st_on, st_level, st_dir_s, st_lvl_s = supertrend_state(df)
        d = compute_signals(px, cash, st_on, st_level, st_dir_s, st_lvl_s)
        d["ticker"] = t
        sigs[t] = d
        print(f"  {t}: W40={d['w40']} W52={d['w52']} TSMOM={d['tsmom']} ST={d['st']} -> pos {d['pos']*100:.0f}%")

    combined = sum(WEIGHTS[t] * sigs[t]["pos"] for t in TICKERS) * 100
    print(f"Combined exposure: {combined:.0f}%")

    changes = detect_changes(prev_state, sigs)
    data_date = max(sigs[t]["wk_date"] for t in TICKERS)
    alert_file = Path(__file__).parent.parent / "lt_smh_alert.txt"
    if changes:
        last_change_date = data_date
        last_change_desc = "; ".join(c.replace("<b>", "").replace("</b>", "") for c in changes)
        print(f"CHANGES: {last_change_desc}")
        # plain-text alert consumed by the Action's email step (not committed)
        lines = [f"LT SMH/QQQ (STX50) 訊號變化 — 數據截至 {data_date}", ""]
        for c in changes:
            lines.append("• " + c.replace("<b>", "").replace("</b>", ""))
        lines += ["",
                  "當前目標倉位："]
        for t in TICKERS:
            d_ = sigs[t]
            lines.append(f"  {t}: {d_['pos']*100:.0f}%  "
                         f"(W40{'✓' if d_['w40'] else '✕'} W52{'✓' if d_['w52'] else '✕'} "
                         f"TSMOM{'✓' if d_['tsmom'] else '✕'} ST{'✓' if d_['st'] else '✕'})")
        lines += ["", "下一個交易日將部位調整至上列目標。",
                  "", "詳細： https://research.investmquest.com/long-track-smh/"]
        alert_file.write_text("\n".join(lines), encoding="utf-8")
        print(f"Alert file: {alert_file}")
    else:
        last_change_date = prev_state.get("last_change_date")
        last_change_desc = prev_state.get("last_change_desc")
        if alert_file.exists():
            alert_file.unlink()
        print("No signal changes vs last run.")

    html = generate_html(sigs, changes, last_change_date)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state_json = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": data_date,
        "last_change_date": last_change_date,
        "last_change_desc": last_change_desc,
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
