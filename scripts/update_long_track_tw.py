#!/usr/bin/env python3
"""
Taiwan Long Track 2330/0050 — E3 Signal Status Page Generator
=============================================================
Fetches 2330.TW, 0050.TW daily OHLC, computes the adopted E3 position per
ticker and renders docs/long-track-tw/index.html.

E3 (adopted 2026-06-23, owner decision — Taiwan analog of the US long track):
    pos = mean of {W40, W52, 12m TSMOM} 0/1 signals (each 1/3)
    Long only; idle fraction earns ~1%/yr TWD cash.

The US 2026-06-13 STX50 upgrade (a weekly Supertrend half-book exit gate) was
TESTED on Taiwan and REJECTED — it fails the site's matched-CAGR ruler that it
passed in the US (sharp V-reversals make it exit late and re-buy higher).  So
this page is E3 only, no gate.  See /backtest/long_track_tw/.

Signal definitions copied verbatim from the backtest authority
(v7-backtest src/long_track_backtest/ensemble_experiment.py:build_signals).

Data notes:
  - The 6-year fetch window is entirely post-2014, so the 0050 Yahoo split
    bug (a -75% gap at 2014-01-02) is OUT of window; the live data is on one
    consistent scale and signals (MA-relative, return-based) are unaffected.
  - 2008 GFC is out of the backtest sample (0050 history starts 2009).

OOS tracking. This is an EXPOSURE-state readout, not a daily trade trigger —
signals only move ~2x/year per ticker.

Schedule: Fridays after TW close (weekly W40/W52 update; TSMOM is month-end).
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

NAV_BLOCK = full_nav_block("system", "lttw")

OUTPUT = Path(__file__).parent.parent / "docs" / "long-track-tw" / "index.html"
STATE_JSON = Path(__file__).parent.parent / "docs" / "long-track-tw" / "state.json"

TICKERS = ["2330.TW", "0050.TW"]
WEIGHTS = {"2330.TW": 0.5, "0050.TW": 0.5}
DISPLAY = {"2330.TW": "2330 台積電", "0050.TW": "0050 元大台灣50"}
CASH_YIELD = 0.01  # flat 1%/yr TWD proxy (matches the backtest assumption)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def _close(df) -> pd.Series:
    c = df["Close"]
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:, 0]
    return c.dropna()


def fetch_close(ticker: str) -> pd.Series:
    end = datetime.now() + timedelta(days=1)
    start = end - timedelta(days=365 * 6)  # 6y: covers 52w MA + 12m TSMOM warmup
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return _close(df)


def twd_cash(index: pd.DatetimeIndex) -> pd.Series:
    days = (index - index[0]).days
    return pd.Series((1 + CASH_YIELD) ** (np.asarray(days) / 365.25), index=index)


# ---------------------------------------------------------------------------
# Signal — verbatim from ensemble_experiment.build_signals (E3, no ST gate)
# ---------------------------------------------------------------------------
def compute_signals(px: pd.Series, cash: pd.Series) -> dict:
    wk = px.resample("W-FRI").last().dropna()
    mo = px.resample("ME").last().dropna()
    # TSMOM timing sync with the backtest authority (ensemble_experiment
    # signal_daily): the monthly signal is DECIDED at each month's last trading
    # session and effective the next day; mid-month the effective signal is the
    # last COMPLETED month's.  resample("ME") makes the trailing bar a partial
    # month, so drop it unless today is the month-end session (BDay approx).
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

    w40_now = bool(w40.iloc[-1])
    w52_now = bool(w52.iloc[-1])
    ts_now = bool(ts.iloc[-1])
    e3 = (int(w40_now) + int(w52_now) + int(ts_now)) / 3.0

    recent = []
    for i in range(-8, 0):
        recent.append({
            "date": wk.index[i].strftime("%Y-%m-%d"),
            "close": float(wk.iloc[i]),
            "ma40": float(ma40.iloc[i]), "ma52": float(ma52.iloc[i]),
            "w40": bool(w40.iloc[i]), "w52": bool(w52.iloc[i]),
            "pct40": (float(wk.iloc[i]) / float(ma40.iloc[i]) - 1) * 100,
            "pct52": (float(wk.iloc[i]) / float(ma52.iloc[i]) - 1) * 100,
        })

    return {
        "ticker": None,
        "w40": w40_now, "w52": w52_now, "tsmom": ts_now,
        "e3": e3, "pos": e3,
        "near": {
            "w40": abs(float(wk.iloc[-1]) / float(ma40.iloc[-1]) - 1) < 0.02,
            "w52": abs(float(wk.iloc[-1]) / float(ma52.iloc[-1]) - 1) < 0.02,
            "tsmom": abs(float(mom.iloc[-1]) - float(cash_mom.reindex(mo.index).iloc[-1])) < 0.02,
        },
        "wk_close": float(wk.iloc[-1]),
        "wk_date": wk.index[-1].strftime("%Y-%m-%d"),
        "ma40": float(ma40.iloc[-1]), "ma52": float(ma52.iloc[-1]),
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
    ])
    return f"""<div class="tcard">
  <div class="tcard-hdr">
    <span class="tname">{DISPLAY.get(t, t)}</span>
    <span class="pos-badge pos-{col}">{pos_pct:.0f}% 倉位</span>
  </div>
  <div class="tcard-sub">E3 {int(d['w40'])+int(d['w52'])+int(d['tsmom'])}/3 綠燈 → 倉位 {d['pos']*100:.0f}% · 閒置部分持台幣現金</div>
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
<h3>{DISPLAY.get(t, t)} — 近 8 週軌跡(週線)</h3>
<table><thead><tr><th>週五</th><th>收盤</th><th>40週均</th><th>距離</th><th>52週均</th><th>距離</th><th>週線訊號</th></tr></thead>
<tbody>{rows}</tbody></table>
<div style="font-size:.72rem;color:var(--muted);margin-top:.5rem">TSMOM 為月頻(月底判定),不在此週線表中；見上方卡片當前值。</div>
</div>"""


def generate_html(sigs: dict, changes=None, last_change_date=None) -> str:
    changes = changes or []
    combined = sum(WEIGHTS[t] * sigs[t]["pos"] for t in TICKERS) * 100
    ccol = pos_color(combined / 100)
    data_date = max(sigs[t]["wk_date"] for t in TICKERS)
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")

    cards = "".join(ticker_card(t, sigs[t]) for t in TICKERS)
    tables = "".join(recent_table(t, sigs[t]) for t in TICKERS)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>台股長線訊號 2330/0050(E3)即時狀態 | InvestMQuest Research</title>
  <meta name="description" content="SystemProtocol v7 台股長線 E3 — 50/50 2330/0050 當前訊號與倉位">
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
.tname{{font-size:1.15rem;font-weight:800;letter-spacing:-.02em}}
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
    <div class="crumb"><a href="/">首頁</a> / 台股長線訊號 2330/0050</div>
    <h1>台股長線訊號 — 2330/0050(E3)即時狀態</h1>
    <div class="sub">SystemProtocol v7 · 50% 2330 + 50% 0050 · E3 三訊號各 1/3 · Long only</div>
    <div style="margin-top:.6rem;display:flex;gap:.4rem">
      <a href="/long-track-smh/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">美股</a>
      <a href="/long-track-tw/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;background:var(--text);color:#fff;text-decoration:none">台股</a>
    </div>
  </div>
</div>
<div class="container">

<div style="background:var(--amber-bg);border:2px solid var(--amber-border);color:var(--amber-text);border-radius:10px;padding:.9rem 1.2rem;margin:1rem 0;font-size:.92rem;font-weight:600;text-align:center">2026-07-18 起本頁非實單系統（實單已改為 <a href="/long-track-w52-adaptive/" style="color:var(--amber-text);text-decoration:underline">W52 × 自適應波動率 150%</a>）；本頁保留每日更新作對照。</div>

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>組合當前曝險</span></div>
  <div class="status-exposure">{combined:.0f}%</div>
  <div style="font-size:.8rem;color:var(--muted)">50% 2330 + 50% 0050 · 閒置部分持台幣現金</div>
  <div class="status-date">數據截至 {data_date}(週五收盤)· 頁面更新 {now} 台北時間</div>
</div>

{('<div style="background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem"><b style="color:var(--red-text)">本週訊號變化</b><br>' + "<br>".join(changes) + '<br><span style="font-size:.78rem;color:var(--muted)">下一個交易日將部位調整至上列目標。</span></div>') if changes else ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">本週無訊號變化' + (f"(上次變化：{last_change_date})" if last_change_date else "") + '</div>')}

<div class="banner">
  <b>E3 台股長線訊號 · 2026-06-23 採用 · 2026-07-18 起改為對照（實單改用 <a href="/long-track-w52-adaptive/">W52 × 自適應波動率 150%</a>）。</b>
  這是<b>曝險狀態讀數</b>,不是每日交易動作 —— 訊號為週/月頻，多數日子不會變化。
  本系統是美股 <a href="/backtest/long_track_smh/">SMH/QQQ 長軌</a>的台股鏡像；美股加掛的 ST 半倉出場閘門(STX50)
  在台股回測<b>過不了同一把尺、已否決</b>,故本頁為純 E3(無閘門)。
  2330 集中度高、2008 GFC 不在回測樣本內，解讀請對照 <a href="/backtest/long_track_tw/">回測頁</a> 的 caveat。
</div>

<div class="tgrid">{cards}</div>

<div class="card">
<h3>規則(每標的倉位 = E3 三訊號平均，各 1/3)</h3>
<div class="rule-list">
① <b>W40</b>:週線收盤 &gt; 40 週均線<br>
② <b>W52</b>:週線收盤 &gt; 52 週均線<br>
③ <b>TSMOM</b>:過去 12 個月總報酬 &gt; 現金(台幣 1%/年)同期 12 個月報酬，<b>月頻、月底判定</b><br>
<span style="color:var(--muted);font-size:.78rem">E3 = 三訊號平均(0 / 33% / 67% / 100% 四檔);兩標的各自獨立跑訊號與資金，
日報酬 50/50 加權合成。成本單邊 7bps 計於 |倉位變動|,<b>未含台股證交稅（2330 賣方 0.3%、0050 0.1%）與券商手續費</b>——
計入後寫實 CAGR 約低 0.2～0.4pp／年。週線訊號於每週最後交易日收盤決策，次日生效。
無 ST 出場閘門(台股回測否決)。2026-06-23 採用，對照線為大盤 B&amp;H 與美股 E3。<br>
Ch12 binary 組合對照 2026-07-02 首跑：Calmar 0.86 vs E3 0.85（雜訊級、含 Ch12 W250 暖身失真；2330 單腿 E3 明顯領先 0.91 vs 0.81），
採用維持 E3、待擁有者重審 —— 詳見 <a href="/backtest/long_track_tw/">回測頁</a>。</span>
</div>
</div>

{tables}

<div class="card">
<h3>訊號流程說明 — 純 E3、沒有「半倉買回」問題(對照美股 SMH 頁)</h3>
<div class="rule-list" style="font-size:.8rem">
台股版<b>只有一套訊號：E3</b>,沒有美股 SMH/QQQ 頁那層 ST(10,3) 半倉出場閘門，所以<b>不存在「出場的半倉怎麼買回來」這個問題</b> ——
E3 跌破一條線就減 ⅓、收復一條線就加 ⅓,買回訊號就是均線/動能自己收復的那一週收盤，不需要第二層閘門。<br>
每週五收盤只算一個數字：<b>每標的目標倉位 = E3 =(W40 + W52 + TSMOM)÷ 3</b>,四檔 0 / 33% / 67% / 100%;
與上週目標的差額就是下一個交易日要下的單。2330 與 0050 各自獨立跑訊號與資金、日報酬 50/50 合成，本頁頂部的倉位數字即當前目標。<br>
<span style="color:var(--muted);font-size:.78rem">TSMOM 為月頻(月底判定),在週線盤整裡不翻面，所以那 ⅓ 多數時候不動 —— 真正把大盤回撤砍半的，是 W40 / W52 兩條週均線在趨勢轉折時各讓出 ⅓。</span>
</div>
<table style="margin-top:.6rem">
<thead><tr><th>情境(示意機制，非實際歷史)</th><th>每標的倉位</th><th>動到哪個 ⅓</th></tr></thead>
<tbody>
<tr><td>三訊號全多</td><td>100%</td><td>W40 ✓ · W52 ✓ · TSMOM ✓(當前狀態)</td></tr>
<tr><td>週收跌破 40 週均</td><td>100% → 67%</td><td>W40 讓出 ⅓;W52、TSMOM 仍多</td></tr>
<tr><td>跌勢延續、再破 52 週均</td><td>67% → 33%</td><td>W52 再讓 ⅓;只剩 TSMOM 撐 ⅓</td></tr>
<tr><td>月底 TSMOM 翻空</td><td>33% → 0%</td><td>三訊號全空 → 空手、持台幣現金</td></tr>
<tr><td>反彈站回 52 週均</td><td>0% → 33%</td><td>W52 收復、買回 ⅓(不必等其他兩條)</td></tr>
<tr><td>站回 40 週均 + 月底 TSMOM 翻多</td><td>33% → 100%</td><td>三訊號逐一收復、各加 ⅓ 回滿</td></tr>
</tbody>
</table>
<div style="font-size:.74rem;color:var(--amber-text);background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:6px;padding:.5rem .8rem;margin-top:.6rem">
<b>為什麼台股不掛美股那層 ST 閘門：</b>美股 SMH/QQQ 的 ST 半倉閘門搬到台股<b>過不了同一把尺</b> —— 它的 Calmar 0.83 反而輸給「同 CAGR 少持一點 E3」的靜態稀釋線(0.85)、MDD 也沒更淺。
原因是台股急跌後常 V 型反彈(2020、2022 底、2024-08),週線閘門砍在低點、追在高點，傷害集中在上半期(H1 Calmar 0.73 vs E3 0.82)。
跨市場結論：<b>趨勢本體(E3)會搬家、出場閘門這層不會。</b>
E3 本身對大盤 B&amp;H 已是經典趨勢交換 —— 讓出約 4pp CAGR、把 -39.5% 回撤壓到 -23.75%(Calmar 0.62 → 0.85),詳見 <a href="/backtest/long_track_tw/">回測頁</a>。保留意見：2008 GFC 不在樣本、2330 集中度高。
</div>
</div>

</div>
<footer class="imq-foot">
  <div>&copy; {datetime.now().year} InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</body>
</html>"""


SIG_LABEL = {"w40": "W40", "w52": "W52", "tsmom": "TSMOM"}


def detect_changes(prev: dict, sigs: dict) -> list:
    if not prev or "tickers" not in prev:
        return []
    out = []
    for t in TICKERS:
        pt = prev["tickers"].get(t)
        if not pt:
            continue
        cur = {"w40": sigs[t]["w40"], "w52": sigs[t]["w52"], "tsmom": sigs[t]["tsmom"]}
        flips = [f"{SIG_LABEL[k]} {'✕→✓' if cur[k] else '✓→✕'}"
                 for k in cur if k in pt and bool(pt[k]) != bool(cur[k])]
        new_pos = round(sigs[t]["pos"] * 100, 1)
        old_pos = pt.get("position_pct")
        if flips or (old_pos is not None and abs(old_pos - new_pos) > 0.5):
            arrow = (f"倉位 {old_pos:.0f}% → {new_pos:.0f}%"
                     if old_pos is not None else f"倉位 {new_pos:.0f}%")
            out.append(f"<b>{DISPLAY.get(t, t)}</b>:{'、'.join(flips) if flips else '訊號未翻轉'} → {arrow}")
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
        px = fetch_close(t)
        print(f"  {len(px)} daily bars")
        cash = twd_cash(px.index)
        d = compute_signals(px, cash)
        d["ticker"] = t
        sigs[t] = d
        print(f"  {t}: W40={d['w40']} W52={d['w52']} TSMOM={d['tsmom']} -> pos {d['pos']*100:.0f}%")

    combined = sum(WEIGHTS[t] * sigs[t]["pos"] for t in TICKERS) * 100
    print(f"Combined exposure: {combined:.0f}%")

    changes = detect_changes(prev_state, sigs)
    data_date = max(sigs[t]["wk_date"] for t in TICKERS)
    alert_file = Path(__file__).parent.parent / "lt_tw_alert.txt"
    if changes:
        last_change_date = data_date
        last_change_desc = "; ".join(c.replace("<b>", "").replace("</b>", "") for c in changes)
        print(f"CHANGES: {last_change_desc}")
        lines = [f"台股長軌 2330/0050 (E3) 訊號變化 — 數據截至 {data_date}", ""]
        for c in changes:
            lines.append("• " + c.replace("<b>", "").replace("</b>", ""))
        lines += ["", "當前目標倉位："]
        for t in TICKERS:
            d_ = sigs[t]
            lines.append(f"  {DISPLAY.get(t, t)}: {d_['pos']*100:.0f}%  "
                         f"(W40{'✓' if d_['w40'] else '✕'} W52{'✓' if d_['w52'] else '✕'} "
                         f"TSMOM{'✓' if d_['tsmom'] else '✕'})")
        lines += ["", "下一個交易日將部位調整至上列目標。",
                  "", "詳細： https://research.investmquest.com/long-track-tw/"]
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
                "e3_pct": round(sigs[t]["e3"] * 100, 1),
                "wk_close": round(sigs[t]["wk_close"], 2),
                "ma40": round(sigs[t]["ma40"], 2), "ma52": round(sigs[t]["ma52"], 2),
                "mom12_pct": round(sigs[t]["mom12"], 2),
                "cash_mom12_pct": round(sigs[t]["cash_mom12"], 2),
            } for t in TICKERS
        },
    }
    STATE_JSON.write_text(json.dumps(state_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


if __name__ == "__main__":
    main()
