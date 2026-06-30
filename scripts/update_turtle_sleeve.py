#!/usr/bin/env python3
"""
Commodity Sleeve + Combined System — daily signal dashboard generator
=====================================================================
Renders docs/turtle-sleeve/index.html: the CMDTY2 turtle sleeve (GLD/USO
signals → MGC/MCL micro futures) on the DAILY timeframe, PLUS the adopted
80/20 combined view — 80% STX50 stock core (read from the sibling
long-track-smh state.json) + 20% commodity sleeve.

STATUS: OOS PARALLEL-TRACK (paper).  This is NOT a live-money page — it is
the pre-adoption parallel run the daily_signals replay was built for. It
logs the daily signal so the close→next-open gap and slippage can be
measured before the owner (Ivan) commits real capital. Sleeve adoption is an
open L4 decision; see /backtest/turtle_adopt/.

ENGINE: the turtle block below (true_range / compute_indicators / Position /
run_turtle) is a VERBATIM PORT of the backtest authority
  v7-backtest/src/turtle_backtest/strategy.py  (original System 2, 55/20)
Keep it in sync if the adopted rule ever changes. fab is a standalone repo
(the GitHub Action only checks out fab), so the engine must be inlined here —
same self-contained pattern as update_long_track_smh.py.

The live state is the REPLAY's end-of-run positions: every run re-downloads
GLD/USO and replays the engine from 2005 to the latest close, so the live
track can never drift from the backtest. Today's events are detected by
diffing against a replay that stops one trading day earlier.

EMAIL: this page emails ONLY on sleeve events (entry/exit/stop/add) and the
month-end rebalance reminder. Stock-core (STX50) signal changes are emailed
separately by update_long_track_smh.yml — not duplicated here.

Schedule: daily after US close (sleeve is a daily-timeframe system).
"""
from __future__ import annotations
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf
from pandas.tseries.offsets import BDay

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("market", "sleeve")

OUTPUT = Path(__file__).parent.parent / "docs" / "turtle-sleeve" / "index.html"
STATE_JSON = Path(__file__).parent.parent / "docs" / "turtle-sleeve" / "state.json"
STX50_STATE = Path(__file__).parent.parent / "docs" / "long-track-smh" / "state.json"
ALERT_FILE = Path(__file__).parent.parent / "turtle_sleeve_alert.txt"

# --- adopted combined-system parameters ---
SIGNAL_TICKERS = ["USO", "GLD"]                 # CMDTY2 sleeve signal legs
FUT = {"GLD": ("GC=F", 10, "MGC 微型金 (10oz)"),
       "USO": ("CL=F", 100, "MCL 微型油 (100bbl)")}
SLEEVE_W = 0.20                                 # 20% sleeve / 80% stock core
TOTAL_NAV = 1_000_000.0                         # nominal paper NAV for contract sizing
SLEEVE_NAV = TOTAL_NAV * SLEEVE_W
START = "2005-01-01"


# ===========================================================================
# Turtle engine — VERBATIM PORT of v7-backtest turtle_backtest/strategy.py
# (original System 2: 55-day entry / 20-day exit, 2xATR stop, pyramide to 4u)
# ===========================================================================
DEFAULT_PARAMS = dict(
    entry_channel=55, exit_channel=20, atr_period=20,
    risk_per_trade=0.01, stop_loss_atr_multiple=2.0,
    max_units_per_market=4, add_unit_atr_multiple=0.5,
    volume_filter=False, volume_threshold=1.5, confirmation_days=0,
    long_only=False, max_gross=None, cost_bps=2, initial_capital=1_000_000.0,
)
P = dict(DEFAULT_PARAMS)


@dataclass
class Position:
    direction: int = 0
    units: list = field(default_factory=list)   # (entry_price, shares, atr_at_entry)
    stop: float = 0.0


def true_range(h, l, c):
    prev_close = c.shift(1)
    return pd.concat([(h - l), (h - prev_close).abs(),
                      (l - prev_close).abs()], axis=1).max(axis=1)


def compute_indicators(df, params):
    out = df.copy()
    tr = true_range(out["High"], out["Low"], out["Close"])
    out["ATR"] = tr.ewm(alpha=1 / params["atr_period"], adjust=False).mean()
    out["high_entry"] = out["High"].rolling(params["entry_channel"]).max().shift(1)
    out["low_entry"] = out["Low"].rolling(params["entry_channel"]).min().shift(1)
    out["high_exit"] = out["High"].rolling(params["exit_channel"]).max().shift(1)
    out["low_exit"] = out["Low"].rolling(params["exit_channel"]).min().shift(1)
    out["vol_avg20"] = out["Volume"].rolling(20).mean()
    return out


def run_turtle(data_dict, params, start_date, end_date):
    """Faithful port of strategy.run_turtle. Returns (positions, equity, events):
    positions = end-of-run state (the live state), equity = daily mark-to-market
    NAV Series, events = chronological (date, tk, kind, direction, price, units,
    reason) log of entries/adds/exits. Sizing/pyramiding/stops/exits are
    identical to the backtest engine."""
    p = {**DEFAULT_PARAMS, **(params or {})}
    markets = {tk: compute_indicators(df, p) for tk, df in data_dict.items()}
    common_idx = None
    for df in markets.values():
        common_idx = df.index if common_idx is None else common_idx.intersection(df.index)
    common_idx = common_idx[(common_idx >= start_date) & (common_idx <= end_date)].sort_values()

    capital = p["initial_capital"]
    positions = {tk: Position() for tk in markets}
    cost = p["cost_bps"] / 10_000
    eq_dates, eq_vals, events = [], [], []

    for date in common_idx:
        for tk, df in markets.items():
            if date not in df.index:
                continue
            row = df.loc[date]
            close, atr = row["Close"], row["ATR"]
            high_entry, low_entry = row["high_entry"], row["low_entry"]
            high_exit, low_exit = row["high_exit"], row["low_exit"]
            if pd.isna(atr) or pd.isna(high_entry) or pd.isna(low_entry):
                continue
            pos = positions[tk]

            # 1. stop
            if pos.direction != 0:
                hit = (pos.direction == 1 and close <= pos.stop) or \
                      (pos.direction == -1 and close >= pos.stop)
                if hit:
                    ep = pos.stop * (1 - cost) if pos.direction == 1 else pos.stop * (1 + cost)
                    capital += sum(s * (ep - e) * pos.direction for e, s, _ in pos.units)
                    events.append((date, tk, "exit", pos.direction, ep, 0, "stop"))
                    positions[tk] = Position()
                    continue
            # 2. channel exit
            if pos.direction == 1 and not pd.isna(low_exit) and close < low_exit:
                ep = close * (1 - cost)
                capital += sum(s * (ep - e) for e, s, _ in pos.units)
                events.append((date, tk, "exit", 1, ep, 0, "channel"))
                positions[tk] = Position()
                continue
            elif pos.direction == -1 and not pd.isna(high_exit) and close > high_exit:
                ep = close * (1 + cost)
                capital += sum(s * (e - ep) for e, s, _ in pos.units)
                events.append((date, tk, "exit", -1, ep, 0, "channel"))
                positions[tk] = Position()
                continue
            # 3. pyramide
            if pos.direction != 0 and len(pos.units) < p["max_units_per_market"]:
                last_ep, _, last_atr = pos.units[-1]
                thr = p["add_unit_atr_multiple"] * last_atr
                if (pos.direction == 1 and close >= last_ep + thr) or \
                   (pos.direction == -1 and close <= last_ep - thr):
                    entry_eff = close * (1 + cost) if pos.direction == 1 else close * (1 - cost)
                    risk = p["stop_loss_atr_multiple"] * atr
                    shares = (capital * p["risk_per_trade"]) / risk if risk > 0 else 0
                    if shares > 0:
                        pos.units.append((entry_eff, shares, atr))
                        pos.stop = (entry_eff - p["stop_loss_atr_multiple"] * atr
                                    if pos.direction == 1
                                    else entry_eff + p["stop_loss_atr_multiple"] * atr)
                        events.append((date, tk, "add", pos.direction, entry_eff, len(pos.units), ""))
            # 4. entry (confirmation_days=0 → immediate)
            if pos.direction == 0:
                if not pd.isna(high_entry) and close > high_entry:
                    risk = p["stop_loss_atr_multiple"] * atr
                    shares = (capital * p["risk_per_trade"]) / risk if risk > 0 else 0
                    entry_eff = close * (1 + cost)
                    if shares > 0:
                        positions[tk] = Position(1, [(entry_eff, shares, atr)],
                                                 entry_eff - p["stop_loss_atr_multiple"] * atr)
                        events.append((date, tk, "entry", 1, entry_eff, 1, ""))
                elif (not pd.isna(low_entry) and close < low_entry and not p["long_only"]):
                    risk = p["stop_loss_atr_multiple"] * atr
                    shares = (capital * p["risk_per_trade"]) / risk if risk > 0 else 0
                    entry_eff = close * (1 - cost)
                    if shares > 0:
                        positions[tk] = Position(-1, [(entry_eff, shares, atr)],
                                                 entry_eff + p["stop_loss_atr_multiple"] * atr)
                        events.append((date, tk, "entry", -1, entry_eff, 1, ""))

        # mark-to-market NAV at end of bar
        pv = capital
        for tk, pos in positions.items():
            if pos.direction == 0 or date not in markets[tk].index:
                continue
            c = markets[tk]["Close"].loc[date]
            for e, s, _ in pos.units:
                pv += s * (c - e) * pos.direction
        eq_dates.append(date)
        eq_vals.append(pv)

    equity = pd.Series(eq_vals, index=pd.DatetimeIndex(eq_dates), name="equity")
    return positions, equity, events


# ===========================================================================
# Data
# ===========================================================================
def fetch_ohlc(ticker: str) -> pd.DataFrame:
    end = datetime.now() + timedelta(days=1)
    start = "2003-01-01"  # warmup before 2005 backtest start (ATR/channel)
    df = yf.download(ticker, start=start, end=end.strftime("%Y-%m-%d"),
                     progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df[["Open", "High", "Low", "Close", "Volume"]].dropna()


# ===========================================================================
# STX50 stock core (80% leg) — faithful port of v7-backtest stx50_curve
# (e4_experiment.member_signals + run_pos + combine; E3 {W40·W52·TSMOM} each ⅓
# with a weekly Supertrend(10,3) half-book reduce-only gate, 50/50 SMH/QQQ).
# Lets this page draw the COMBINED 80/20 curve that is actually run, not just
# the 20% sleeve leg in isolation.
# ===========================================================================
STX_TICKERS = ["SMH", "QQQ"]
SIM_START_STX = "2006-01-01"
INIT_CAP = 1_000_000.0
COST_PER_SIDE = 0.0007


def _close_series(df: pd.DataFrame) -> pd.Series:
    c = df["Close"]
    return (c.iloc[:, 0] if isinstance(c, pd.DataFrame) else c).dropna()


def load_cash_close() -> pd.Series:
    """SHY before BIL inception (2007-05), BIL after — same splice as backtest."""
    shy, bil = _close_series(fetch_ohlc("SHY")), _close_series(fetch_ohlc("BIL"))
    if len(bil) == 0:
        return shy
    return pd.concat([shy[shy.index < bil.index[0]], bil]).sort_index()


def _exec_dates(px: pd.Series, freq: str) -> pd.Series:
    return px.resample(freq).apply(lambda x: x.index[-1] if len(x) else pd.NaT).dropna()


def _signal_daily(sig: pd.Series, ex: pd.Series, idx: pd.DatetimeIndex) -> pd.Series:
    s = pd.Series(sig.values, index=ex.reindex(sig.index).values).dropna()
    s = s[~s.index.duplicated(keep="last")]
    return s.reindex(idx).ffill()


def _build_e3(px: pd.Series, cash: pd.Series) -> dict:
    wk = px.resample("W-FRI").last().dropna()
    exw = _exec_dates(px, "W-FRI")
    mo = px.resample("ME").last().dropna()
    exm = _exec_dates(px, "ME")
    cash_m = cash.resample("ME").last()
    w40 = (wk > wk.rolling(40).mean()).astype(float)
    w52 = (wk > wk.rolling(52).mean()).astype(float)
    ts = ((mo / mo.shift(12) - 1) >
          (cash_m / cash_m.shift(12) - 1).reindex(mo.index).fillna(0)).astype(float)
    return {"W40": _signal_daily(w40, exw, px.index),
            "W52": _signal_daily(w52, exw, px.index),
            "TSMOM": _signal_daily(ts, exm, px.index)}


def _weekly_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "High": df["High"].resample("W-FRI").max(),
        "Low": df["Low"].resample("W-FRI").min(),
        "Close": df["Close"].resample("W-FRI").last(),
        "exec_date": df["Close"].resample("W-FRI").apply(
            lambda x: x.index[-1] if len(x) else pd.NaT),
    }).dropna(subset=["Close"])


def _supertrend_dir(wk: pd.DataFrame, period: int = 10, mult: float = 3.0) -> pd.Series:
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
    return pd.Series(direction, index=wk.index)


def _run_pos(px: pd.Series, cash: pd.Series, pos: pd.Series) -> pd.Series:
    sim = px.index[px.index >= SIM_START_STX]
    qr = px.pct_change().reindex(sim).fillna(0)
    cr = cash.pct_change().reindex(sim).fillna(0)
    p = pos.reindex(sim)
    p_prev = p.shift(1)
    pre = pos[pos.index < sim[0]].dropna()
    p_prev.iloc[0] = float(pre.iloc[-1]) if len(pre) else 0.0
    turn = (p - p_prev).abs().fillna(0)
    ret = p_prev * qr + (1 - p_prev) * cr - turn * COST_PER_SIDE
    return INIT_CAP * (1 + ret).cumprod()


def _daily_returns(eq: pd.Series) -> pd.Series:
    dr = eq.pct_change()
    dr.iloc[0] = eq.iloc[0] / INIT_CAP - 1
    return dr


def _combine(eqs: dict, weights: dict) -> pd.Series:
    common = None
    for eq in eqs.values():
        common = eq.index if common is None else common.intersection(eq.index)
    cr = sum(weights[t] * _daily_returns(eq.reindex(common)) for t, eq in eqs.items())
    return INIT_CAP * (1 + cr).cumprod()


def stx50_equity(cash: pd.Series) -> pd.Series:
    eqs = {}
    for t in STX_TICKERS:
        df = fetch_ohlc(t)
        px = _close_series(df)
        sigs = _build_e3(px, cash)
        st_w = (_supertrend_dir(_weekly_ohlc(df)) > 0).astype(float)
        wk = _weekly_ohlc(df)
        st_daily = _signal_daily(st_w, wk["exec_date"], px.index)
        e3 = sum(sigs[m] for m in ("W40", "W52", "TSMOM")) / 3
        pos = 0.5 * e3 + 0.5 * np.minimum(e3, st_daily)
        eqs[t] = _run_pos(px, cash, pos)
    return _combine(eqs, {"SMH": 0.5, "QQQ": 0.5})


def monthly_rebal_mix(base_r: pd.Series, sleeve_r: pd.Series, w: float) -> pd.Series:
    """80/20 portfolio, weights reset to (1-w, w) at each month end."""
    vb, vs = INIT_CAP * (1 - w), INIT_CAP * w
    vals, idx = [], base_r.index
    for i, d in enumerate(idx):
        vb *= 1 + base_r.iloc[i]
        vs *= 1 + sleeve_r.iloc[i]
        tot = vb + vs
        vals.append(tot)
        if i + 1 < len(idx) and idx[i + 1].month != d.month:
            vb, vs = tot * (1 - w), tot * w
    return pd.Series(vals, index=idx)


# ===========================================================================
# Signal / live state
# ===========================================================================
def fmt_pos(pos: Position) -> str:
    if pos.direction == 0:
        return "FLAT"
    side = "LONG" if pos.direction == 1 else "SHORT"
    return f"{side} {len(pos.units)}u"


def build_leg_state(data: dict, fut_px: dict, pos_now: dict, pos_prev: dict) -> list:
    legs = []
    for t in SIGNAL_TICKERS:
        df = data[t]
        px = float(df["Close"].iloc[-1])
        ind = compute_indicators(df, P)
        atr = float(ind["ATR"].iloc[-1])
        hi55 = float(df["High"].rolling(P["entry_channel"]).max().iloc[-1])
        lo55 = float(df["Low"].rolling(P["entry_channel"]).min().iloc[-1])
        hi20 = float(df["High"].rolling(P["exit_channel"]).max().iloc[-1])
        lo20 = float(df["Low"].rolling(P["exit_channel"]).min().iloc[-1])

        pn, pp = pos_now[t], pos_prev[t]
        event, event_kind = "—", None
        if pp.direction != pn.direction:
            if pn.direction == 0:
                event, event_kind = "✂️ 今日收盤觸發出場 → 明日開盤平倉", "exit"
            else:
                side = "做多" if pn.direction == 1 else "做空"
                event, event_kind = f"🚀 今日收盤突破 → 明日開盤{side}", "entry"
        elif len(pn.units) > len(pp.units):
            event, event_kind = f"➕ 今日觸發加碼(第 {len(pn.units)} 單位)", "add"

        fsym, mult, flabel = FUT[t]
        unit_notional = SLEEVE_NAV * P["risk_per_trade"] * px / (P["stop_loss_atr_multiple"] * atr)
        n_contracts = int(unit_notional // (fut_px[t] * mult)) if fut_px[t] > 0 else 0

        triggers = []
        if pn.direction == 0:
            triggers.append(("進場做多", f"明日收盤 > {hi55:.2f}", "long"))
            triggers.append(("進場做空", f"明日收盤 < {lo55:.2f}", "short"))
        else:
            d = pn.direction
            ch_exit = lo20 if d == 1 else hi20
            triggers.append(("停損", f"收盤 {'≤' if d == 1 else '≥'} {pn.stop:.2f} → 全部出場", "stop"))
            triggers.append(("通道出場", f"收盤 {'<' if d == 1 else '>'} {ch_exit:.2f} → 全部出場", "exit"))
            if len(pn.units) < P["max_units_per_market"]:
                last_ep, _, last_atr = pn.units[-1]
                add_lv = last_ep + d * P["add_unit_atr_multiple"] * last_atr
                triggers.append(("加碼", f"收盤 {'≥' if d == 1 else '≤'} {add_lv:.2f} → +1 單位", "add"))

        legs.append({
            "ticker": t, "fut": flabel, "px": px, "atr": atr,
            "pos": fmt_pos(pn), "direction": pn.direction, "units": len(pn.units),
            "stop": pn.stop if pn.direction != 0 else None,
            "event": event, "event_kind": event_kind,
            "unit_notional": unit_notional, "n_contracts": n_contracts,
            "triggers": triggers,
            "hi55": hi55, "lo55": lo55, "hi20": hi20, "lo20": lo20,
        })
    return legs


def read_stx50() -> dict | None:
    if not STX50_STATE.exists():
        return None
    try:
        return json.loads(STX50_STATE.read_text())
    except Exception:
        return None


def is_month_end_session(asof: pd.Timestamp) -> bool:
    """True if the next US trading day falls in a new month (rebalance day-ish).
    Approximated with business days — holidays may shift by 1 day, acceptable
    for a reminder."""
    nxt = (asof + BDay(1)).to_pydatetime()
    return nxt.month != asof.month


# ===========================================================================
# HTML
# ===========================================================================
def fmt_pct(v, dp=1):
    return f"{'+' if v >= 0 else ''}{v:.{dp}f}%"


def dir_badge(direction: int, units: int) -> str:
    if direction == 0:
        return '<span class="pos-badge pos-flat">FLAT</span>'
    if direction == 1:
        return f'<span class="pos-badge pos-long">LONG {units}u</span>'
    return f'<span class="pos-badge pos-short">SHORT {units}u</span>'


def leg_card(leg: dict) -> str:
    trig_rows = ""
    for label, desc, kind in leg["triggers"]:
        col = {"long": "green", "short": "red", "stop": "red",
               "exit": "amber", "add": "blue"}.get(kind, "muted")
        trig_rows += (f'<div class="trig"><span class="trig-l" style="color:var(--{col})">'
                      f'{label}</span><span class="trig-d">{desc}</span></div>')
    ev = ""
    if leg["event_kind"]:
        ev = f'<div class="leg-event">{leg["event"]}</div>'
    stop_txt = f' · 停損 {leg["stop"]:.2f}' if leg["stop"] is not None else ""
    return f"""<div class="tcard">
  <div class="tcard-hdr">
    <span class="tname">{leg['ticker']} <span style="font-size:.72rem;color:var(--muted);font-weight:500">→ {leg['fut']}</span></span>
    {dir_badge(leg['direction'], leg['units'])}
  </div>
  <div class="tcard-sub">收盤 {leg['px']:.2f} · ATR20 {leg['atr']:.2f}{stop_txt} · 1 單位 ≈ ${leg['unit_notional']:,.0f} ≈ <b>{leg['n_contracts']} 口</b></div>
  {ev}
  <div class="trig-box">{trig_rows}</div>
</div>"""


def stx50_card(s: dict | None) -> str:
    if not s:
        return ('<div class="card"><h3>股票核心 STX50 — 狀態未取得</h3>'
                '<div style="font-size:.8rem;color:var(--muted)">尚未讀到 '
                '<code>long-track-smh/state.json</code>。詳見 '
                '<a href="/long-track-smh/">/long-track-smh/</a>。</div></div>')
    exp = s.get("combined_exposure_pct", 0.0)
    rows = ""
    for t, td in s.get("tickers", {}).items():
        rows += (f'<tr><td><b>{t}</b></td><td>{td["position_pct"]:.0f}%</td>'
                 f'<td>W40{"✓" if td["w40"] else "✕"} W52{"✓" if td["w52"] else "✕"} '
                 f'TSMOM{"✓" if td["tsmom"] else "✕"} ST{"✓" if td["st_gate"] else "✕"}</td></tr>')
    return f"""<div class="card">
  <h3>股票核心 — STX50 (50/50 SMH/QQQ) · 組合 80% 權重</h3>
  <div style="font-size:.82rem;color:var(--muted);margin-bottom:.6rem">
    當前股票曝險 <b style="color:var(--text);font-size:1.05rem">{exp:.0f}%</b> ·
    數據截至 {s.get('data_date','—')} · 週/月頻訊號,變化由
    <a href="/long-track-smh/">長線訊號頁</a>另行 email 通知。</div>
  <table><thead><tr><th>標的</th><th>倉位</th><th>訊號</th></tr></thead><tbody>{rows}</tbody></table>
</div>"""


def event_row(ev) -> str:
    date, tk, kind, direction, price, units, reason = ev
    fut = FUT[tk][2]
    if kind == "entry":
        label = "🟢 進場做多" if direction == 1 else "🔴 進場做空"
        col = "green" if direction == 1 else "red"
    elif kind == "add":
        label = f"➕ 加碼 → 第 {units} 單位 ({'多' if direction == 1 else '空'})"
        col = "blue"
    else:  # exit
        rs = {"stop": "停損", "channel": "通道"}.get(reason, "")
        label = f"✂️ 出場 ({'多' if direction == 1 else '空'} · {rs})"
        col = "amber"
    return (f'<tr><td>{date.strftime("%Y-%m-%d")}</td>'
            f'<td><b>{tk}</b> <span style="color:var(--muted);font-size:.72rem">{fut}</span></td>'
            f'<td style="color:var(--{col});font-weight:600">{label}</td>'
            f'<td>{price:.2f}</td></tr>')


def events_section(year_events) -> str:
    if not year_events:
        body = ('<div style="font-size:.82rem;color:var(--muted);padding:.5rem">'
                '近一年無進出場事件(部位持續持有或空手)。</div>')
    else:
        rows = "".join(event_row(e) for e in year_events)
        body = (f'<table><thead><tr><th>日期</th><th>標的</th><th>動作</th><th>成交價</th></tr></thead>'
                f'<tbody>{rows}</tbody></table>')
    return f"""<div class="card">
  <h3>近一年訊號史 — 進場 / 加碼 / 出場({len(year_events)} 筆)</h3>
  <div style="font-size:.78rem;color:var(--muted);margin-bottom:.6rem">
    由 replay 引擎逐日重放產生(回測訊號,非實單成交)。成交價為訊號日收盤含 2bps 成本;
    實單為次日開盤,gap 列入並行比對。多空雙向,加碼每 0.5×ATR 一單位至 4 單位。</div>
  {body}
</div>"""


def perf_section(yr_ret) -> str:
    col = "green" if yr_ret >= 0 else "red"
    return f"""<div class="card">
  <h3>組合 80/20 績效曲線(replay 權益,起點=100)
    <span style="font-size:.8rem;font-weight:600;color:var(--{col})">· 近一年 {yr_ret:+.1f}%</span></h3>
  <div style="font-size:.78rem;color:var(--muted);margin-bottom:.6rem">
    引擎自 2006 重放至最新收盤的模型 NAV(月頻、含成本)。實線 = <b>實際在跑的組合
    80% STX50 + 20% 商品 sleeve(月底再平衡)</b>;虛線為兩條分解腿。
    <b>這是回測/紙上權益,非實倉損益</b> —— OOS 並行追蹤期間沒有真實成交。
    sleeve 單腿波動大(MDD ≈ -33%),但只佔 20%;組合層 MDD 被 STX50 拉到約 -16%。
    細節見 <a href="/backtest/turtle_adopt/">採用回測頁</a>。</div>
  <div class="chart-wrap"><canvas id="chart-perf"></canvas></div>
</div>"""


def perf_script(nav_labels, comb_vals, stx_vals, slv_vals) -> str:
    return ("<script>new Chart(document.getElementById('chart-perf'),{type:'line',"
            "data:{labels:" + json.dumps(nav_labels) + ",datasets:["
            "{label:'組合 80/20',data:" + json.dumps(comb_vals) + ",borderColor:'#0f766e',"
            "borderWidth:2.4,pointRadius:0,pointHoverRadius:4,tension:0.1},"
            "{label:'STX50 (股核 80%)',data:" + json.dumps(stx_vals) + ",borderColor:'#1565c0',"
            "borderWidth:1.3,borderDash:[6,3],pointRadius:0,pointHoverRadius:3,tension:0.1},"
            "{label:'Sleeve (商品 20%)',data:" + json.dumps(slv_vals) + ",borderColor:'#d97706',"
            "borderWidth:1.3,borderDash:[2,3],pointRadius:0,pointHoverRadius:3,tension:0.1}]},"
            "options:{responsive:true,maintainAspectRatio:false,"
            "interaction:{mode:'index',intersect:false},"
            "plugins:{legend:{position:'top',align:'start',labels:{usePointStyle:true,"
            "pointStyle:'line',boxWidth:24,font:{size:10},padding:12}}},"
            "scales:{x:{grid:{color:'rgba(0,0,0,0.04)'},ticks:{maxTicksLimit:14,font:{size:10}}},"
            "y:{type:'logarithmic',grid:{color:'rgba(0,0,0,0.06)'},ticks:{font:{size:10}}}}}});</script>")


def generate_html(legs, stx, combined, asof, changes, last_change_date, rebal_due,
                  year_events, nav_labels, comb_vals, stx_vals, slv_vals, yr_ret):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sleeve_dir = ", ".join(f"{l['ticker']} {l['pos']}" for l in legs)
    cards = "".join(leg_card(l) for l in legs)
    stx_exp = stx.get("combined_exposure_pct", 0.0) if stx else 0.0

    change_html = ""
    if changes:
        change_html = ('<div class="change-box"><b style="color:var(--red-text)">⚡ 今日 sleeve 事件</b><br>'
                       + "<br>".join(changes)
                       + '<br><span style="font-size:.78rem;color:var(--muted)">明日開盤依上列觸發執行。</span></div>')
    elif rebal_due:
        change_html = ('<div class="change-box" style="background:var(--blue-bg);border-color:var(--blue-border)">'
                       '<b style="color:var(--blue-text)">🔁 月底再平衡日</b><br>'
                       'sleeve 與股票核心再平衡回 20 / 80(回測驗證的紀律)。</div>')
    else:
        change_html = ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">'
                       '今日 sleeve 無事件'
                       + (f'(上次:{last_change_date})' if last_change_date else '') + '</div>')

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>商品 Sleeve + 組合系統即時狀態 (OOS) | InvestMQuest Research</title>
  <meta name="description" content="CMDTY2 唐奇安突破 sleeve (GLD/USO→MGC/MCL) 日線訊號 + 80/20 STX50 組合曝險">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
  <style>
:root{{--brand:#1a56db;--bg:#f8f9fa;--card:#fff;--text:#1a1a2e;--muted:#6b7280;--border:#e2e5e9;
  --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
  --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--red-text:#991b1b;
  --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e;
  --blue:#2563eb;--blue-bg:#eff6ff;--blue-border:#93c5fd;--blue-text:#1e40af}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
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
footer{{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1rem 0;font-size:.75rem;margin-top:1rem}}
.banner{{background:var(--amber-bg);border:1px solid var(--amber-border);color:var(--amber-text);
  border-radius:8px;padding:.7rem 1rem;font-size:.8rem;margin:1rem 0}}
.hero{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;padding:1.5rem 0 .5rem}}
.hero-box{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:1.3rem 1.5rem;text-align:center}}
.hero-box .lbl{{font-size:.8rem;color:var(--muted);font-weight:600}}
.hero-box .big{{font-size:2rem;font-weight:800;margin:.25rem 0;letter-spacing:-.02em}}
.hero-box .sub2{{font-size:.76rem;color:var(--muted)}}
.change-box{{background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem}}
.tgrid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}}
.tcard{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:1.1rem;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.tcard-hdr{{display:flex;align-items:center;justify-content:space-between;margin-bottom:.3rem}}
.tname{{font-size:1.2rem;font-weight:800;letter-spacing:-.02em}}
.pos-badge{{font-size:.9rem;font-weight:700;padding:.25rem .7rem;border-radius:8px}}
.pos-long{{background:var(--green-bg);color:var(--green-text)}}
.pos-short{{background:var(--red-bg);color:var(--red-text)}}
.pos-flat{{background:#f1f5f9;color:var(--muted)}}
.tcard-sub{{font-size:.74rem;color:var(--muted);margin-bottom:.6rem;font-variant-numeric:tabular-nums}}
.leg-event{{font-size:.82rem;font-weight:600;padding:.45rem .7rem;border-radius:6px;background:var(--amber-bg);
  border:1px solid var(--amber-border);color:var(--amber-text);margin-bottom:.6rem}}
.trig-box{{display:grid;gap:.35rem}}
.trig{{display:flex;justify-content:space-between;gap:.5rem;font-size:.78rem;padding:.35rem .55rem;
  background:#f8fafc;border-radius:6px;border:1px solid var(--border)}}
.trig-l{{font-weight:700}}
.trig-d{{color:var(--muted);font-variant-numeric:tabular-nums;text-align:right}}
.rule-list{{font-size:.82rem;line-height:1.9}}
.chart-wrap{{position:relative;width:100%;height:340px;margin-top:.4rem}}
@media(max-width:768px){{.hero,.tgrid{{grid-template-columns:1fr}}.big{{font-size:1.6rem}}table{{font-size:.74rem}}th,td{{padding:.4rem .45rem}}.chart-wrap{{height:260px}}}}
</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / 商品 Sleeve + 組合系統</div>
    <h1>商品 Sleeve + 組合系統 — 即時狀態</h1>
    <div class="sub">80% STX50 股票核心 (SMH/QQQ) + 20% CMDTY2 商品 sleeve (GLD/USO 訊號 → MGC/MCL 微型期貨,原始 System 2 · 55/20 日線)</div>
  </div>
</div>
<div class="container">

<div class="banner">
  <b>⚠ OOS 並行追蹤(紙上)· 非實倉。</b>
  這是 sleeve 採用前的並行測試 —— 記錄每日訊號以實測 close→次日開盤 gap 與滑點,
  供擁有者決定何時投真錢。Sleeve 採用為未決的 L4 決策,評估見
  <a href="/backtest/turtle_adopt/">組合回測頁</a>。口數依名目 sleeve NAV ${SLEEVE_NAV:,.0f} 計,按實際資金等比例縮放。
</div>

<div class="hero">
  <div class="hero-box">
    <div class="lbl">股票核心 STX50 · 80% 權重</div>
    <div class="big" style="color:var(--brand)">{stx_exp:.0f}%</div>
    <div class="sub2">曝險 → 組合 {stx_exp*0.8:.0f}% 在股票 · 閒置持 SHY/BIL</div>
  </div>
  <div class="hero-box">
    <div class="lbl">商品 Sleeve · 20% 權重</div>
    <div class="big" style="color:var(--amber-text);font-size:1.3rem;margin-top:.6rem">{sleeve_dir}</div>
    <div class="sub2">GLD/USO 唐奇安突破 · 可多可空</div>
  </div>
</div>

<div style="text-align:center;font-size:.8rem;color:var(--muted);margin:.2rem 0 1rem">
  訊號資料截至 {asof}(收盤)· 頁面更新 {now}</div>

{change_html}

<div class="card">
  <h3>商品 Sleeve — 每日持倉與明日觸發價</h3>
  <div style="font-size:.78rem;color:var(--muted);margin-bottom:.8rem">
    每日收盤後 replay 引擎自 2005 重放到最新收盤 → 持倉即引擎狀態,永不漂移。
    觸發價為次日決策線(突破/停損/通道/加碼),掛 resting order 即可。</div>
  <div class="tgrid">{cards}</div>
</div>

{stx50_card(stx)}

{perf_section(yr_ret)}

{events_section(year_events)}

<div class="card">
  <h3>規則摘要(組合 = 80% STX50 + 20% CMDTY2 sleeve,月底再平衡)</h3>
  <div class="rule-list">
  ① <b>股票核心 STX50</b>(80%):50/50 SMH/QQQ · E3 三訊號各 ⅓ + 週線 ST(10,3) 半倉出場閘門 · 週/月頻 · 見 <a href="/long-track-smh/">長線訊號頁</a><br>
  ② <b>商品 sleeve</b>(20%):GLD/USO 各跑原始海龜 System 2 — 收盤突破 55 日高/低點進場、跌破 20 日反向通道或 2×ATR 停損出場、每 0.5×ATR 加碼至 4 單位<br>
  ③ <b>倉位大小</b>:每單位風險 = sleeve NAV 的 1% ÷ (2×ATR);波動定倉位<br>
  ④ <b>執行</b>:微型期貨 MGC(金)/MCL(油)為主(可空、SPAN 槓桿);或 IBKR margin 放空 ETF(回測拿回約 56% 效益)<br>
  ⑤ <b>再平衡</b>:每月最後交易日,sleeve ⇄ 股票核心回 20/80<br>
  <span style="color:var(--muted);font-size:.78rem">引擎為 v7-backtest turtle_backtest/strategy.py 的 verbatim port(原始 System 2)。
  時間架構刻意維持日線 —— 與週線股票核心錯位是分散來源,週線化會抹掉危機 alpha(見回測頁)。</span>
  </div>
</div>

</div>
<footer>
  &copy; {datetime.now().year} InvestMQuest Research · 商品 Sleeve + 組合系統(OOS 並行追蹤)·
  真實 yfinance 資料 · 引擎同步自 v7-backtest turtle_backtest/strategy.py · 每日美股收盤後自動更新
</footer>
{perf_script(nav_labels, comb_vals, stx_vals, slv_vals)}
</body>
</html>"""


# ===========================================================================
# Change detection + main
# ===========================================================================
def detect_changes(legs: list) -> list[str]:
    out = []
    for l in legs:
        if l["event_kind"]:
            ev = l["event"].split(" → ")[0].lstrip("✂️🚀➕ ").strip()
            out.append(f"<b>{l['ticker']}</b> ({l['fut']}):{l['event']} · 約 {l['n_contracts']} 口")
    return out


def main():
    prev_state = {}
    if STATE_JSON.exists():
        try:
            prev_state = json.loads(STATE_JSON.read_text())
        except Exception:
            prev_state = {}

    print("Fetching GLD/USO + GC=F/CL=F...")
    data = {t: fetch_ohlc(t) for t in SIGNAL_TICKERS}
    fut_px = {}
    for t, (sym, mult, label) in FUT.items():
        try:
            fut_px[t] = float(fetch_ohlc(sym)["Close"].iloc[-1])
        except Exception:
            fut_px[t] = 0.0

    asof = min(df.index[-1] for df in data.values())
    data = {t: df[df.index <= asof] for t, df in data.items()}
    print(f"  data as-of {asof.date()}")

    pos_now, eq, events = run_turtle(data, P, START, str(asof.date()))
    prev_day = eq.index[-2]
    pos_prev, _, _ = run_turtle(data, P, START, str(prev_day.date()))

    legs = build_leg_state(data, fut_px, pos_now, pos_prev)
    for l in legs:
        print(f"  {l['ticker']}: {l['pos']} | event={l['event_kind']} | {l['n_contracts']} contracts")

    # past-year signal history (most recent first)
    one_yr_ago = asof - pd.Timedelta(days=365)
    year_events = sorted([e for e in events if e[0] >= one_yr_ago],
                         key=lambda e: e[0], reverse=True)
    sleeve_yr = round((float(eq.iloc[-1]) /
                       float(eq.loc[eq.index >= one_yr_ago].iloc[0]) - 1) * 100, 1)

    # COMBINED 80/20 curve (what is actually run) + STX50/sleeve decomposition.
    # STX50 stock core built live (faithful v7 port); 80/20 monthly-rebalanced.
    def _mnav(series):
        m = series.resample("ME").last().dropna()
        b = float(m.iloc[0])
        return [str(k.date())[:7] for k in m.index], [round(float(v) / b * 100, 2) for v in m.values]

    try:
        cash = load_cash_close()
        stx_eq = stx50_equity(cash)
        common = stx_eq.index.intersection(eq.index)
        sr = stx_eq.reindex(common).pct_change().fillna(0)
        cr = eq.reindex(common).pct_change().fillna(0)
        combined_eq = monthly_rebal_mix(sr, cr, SLEEVE_W)          # 80% STX50 + 20% sleeve
        nav_labels, comb_vals = _mnav(combined_eq)
        _, stx_vals = _mnav(INIT_CAP * (1 + sr).cumprod())
        _, slv_vals = _mnav(INIT_CAP * (1 + cr).cumprod())
        c1 = combined_eq.loc[combined_eq.index >= one_yr_ago]
        yr_ret = round((float(combined_eq.iloc[-1]) / float(c1.iloc[0]) - 1) * 100, 1)
        print(f"  combined 80/20 replay NAV 1y {yr_ret:+.1f}% | STX50+sleeve decomposition built")
    except Exception as exc:  # network / data hiccup → degrade to sleeve-only line
        print(f"  WARN: STX50/combined build failed ({exc}); sleeve-only curve")
        nav_labels, slv_vals = _mnav(eq)
        comb_vals = stx_vals = slv_vals
        yr_ret = sleeve_yr
    print(f"  {len(year_events)} events in past year | sleeve 1y {sleeve_yr:+.1f}%")

    stx = read_stx50()
    stx_exp = stx.get("combined_exposure_pct", 0.0) if stx else 0.0
    combined = {"stx50_exposure": stx_exp, "stock_weight_in_portfolio": round(stx_exp * 0.8, 1)}

    changes = detect_changes(legs)
    rebal_due = is_month_end_session(asof)
    asof_str = asof.strftime("%Y-%m-%d")

    if changes:
        last_change_date = asof_str
        lines = [f"商品 Sleeve 訊號事件 — 資料截至 {asof_str}", ""]
        for c in changes:
            lines.append("• " + c.replace("<b>", "").replace("</b>", ""))
        lines += ["", "明日開盤依觸發執行。當前 sleeve 持倉:"]
        for l in legs:
            stop_s = f" stop {l['stop']:.2f}" if l['stop'] is not None else ""
            lines.append(f"  {l['ticker']} → {l['fut']}: {l['pos']}{stop_s} · {l['n_contracts']} 口")
        lines += ["", f"股票核心 STX50 曝險:{stx_exp:.0f}%(組合 80% 權重)",
                  "", "詳細: https://research.investmquest.com/turtle-sleeve/"]
        ALERT_FILE.write_text("\n".join(lines), encoding="utf-8")
        print(f"ALERT written: {ALERT_FILE}")
    else:
        last_change_date = prev_state.get("last_change_date")
        if rebal_due:
            ALERT_FILE.write_text(
                f"🔁 月底再平衡提醒 — 資料截至 {asof_str}\n\n"
                f"sleeve 與股票核心再平衡回 20/80。\n"
                f"當前股票核心 STX50 曝險 {stx_exp:.0f}%。\n\n"
                f"詳細: https://research.investmquest.com/turtle-sleeve/",
                encoding="utf-8")
            print(f"REBALANCE reminder written: {ALERT_FILE}")
        elif ALERT_FILE.exists():
            ALERT_FILE.unlink()
        print("No sleeve events.")

    html = generate_html(legs, stx, combined, asof_str, changes, last_change_date,
                         rebal_due, year_events, nav_labels, comb_vals, stx_vals, slv_vals, yr_ret)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": asof_str,
        "last_change_date": last_change_date,
        "status": "oos_paper",
        "sleeve_weight": SLEEVE_W,
        "stx50_exposure_pct": stx_exp,
        "sleeve_1y_replay_ret_pct": sleeve_yr,
        "combined_1y_replay_ret_pct": yr_ret,
        "events_1y": len(year_events),
        "legs": {
            l["ticker"]: {
                "direction": l["direction"], "units": l["units"],
                "stop": round(l["stop"], 2) if l["stop"] is not None else None,
                "n_contracts": l["n_contracts"], "fut": l["fut"],
                "event": l["event_kind"],
            } for l in legs
        },
    }
    STATE_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


if __name__ == "__main__":
    main()
