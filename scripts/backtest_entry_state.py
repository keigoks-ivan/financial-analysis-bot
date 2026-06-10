#!/usr/bin/env python3
"""Entry-State signal backtest — fixed-holding-period return distribution.

One-shot analysis (NOT wired to cron). Validates whether the entry-state page's
"相對有勝率" claim has empirical support, by reconstructing PULLBACK_WATCH and
BREAKOUT signals week-by-week over a 5-year sample and measuring the realised
forward return of "buy at the signal week's close → sell after a fixed holding
period".

Design notes / fidelity:
  - Universe = the entry-state universe (Q≥0.55 ∩ G≥0.5 ∩ archetype=成長型 by
    default; CLI-tunable). NOTE this is a *survivorship-biased* set — it is the
    list of names that pass the gate *today*, so their backtested history is
    upward-biased. This is surfaced prominently in the report; do not read the
    numbers as an unbiased estimate of future edge.
  - Signal reconstruction is point-in-time. For every historical week-end we
    recompute the first-layer MA gate and second-layer state using ONLY data up
    to and including that week (`closes.iloc[:i+1]`), via the *exact same*
    `_compute_derived` / `ma_gate` / `classify_state` code the live page uses —
    so the BREAKOUT / PULLBACK_WATCH thresholds are identical, and there is no
    look-ahead bias.
  - Two reconstruction approximations (both documented in the HTML caveat):
      1. ma50_pct: live page uses a *daily* 50-day SMA from the screener timing
         feed. Here it is proxied by the trailing 10-week SMA (≈50 trading days)
         off the same weekly series. Minor; affects the BREAKOUT ma50≥0 and
         PULLBACK ma50∈[-3,+3] sub-gates only.
      2. rs_score: live page percentile-ranks blended 1w/4w/13w momentum against
         a ~511-stock US universe. Reconstructing that historical population is
         infeasible, so RS is ranked *within the backtest universe* (same blend
         + trend-bonus formula as build_dd_screener.compute_yfinance_timing_
         fallback). Because the reference set is uniformly strong, RS≥80 is a
         *harder* bar here → BREAKOUT counts likely UNDER-state the live page.
         To isolate this, BREAKOUT is also reported WITHOUT the RS gate.

Usage:
  python3 scripts/backtest_entry_state.py
  python3 scripts/backtest_entry_state.py --max-tickers 12       # fast smoke
  python3 scripts/backtest_entry_state.py --quality-min 0.75 --growth-min 0.60
  python3 scripts/backtest_entry_state.py --dry-run              # no file writes
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "pandas", "numpy", "-q"])
    import numpy as np
    import pandas as pd
    import yfinance as yf

# Reuse the *exact* live-page signal logic — single source of truth for thresholds.
from scripts.dd_screener_ma import _compute_derived  # noqa: E402
from scripts.build_dd_screener import _yf_ticker_for_ma  # noqa: E402
from scripts.build_entry_state import (  # noqa: E402
    ma_gate,
    classify_state,
    STATE_BREAKOUT,
    STATE_PULLBACK,
    SUB_WATCH,
)

QE_JSON = ROOT / "docs" / "dd-screener" / "quality-entry.json"
OUTPUT_DIR = ROOT / "docs" / "dd-screener"
HTML_OUT = OUTPUT_DIR / "entry-state-backtest.html"
JSON_OUT = OUTPUT_DIR / "entry-state-backtest.json"

TAIPEI_TZ = timezone(timedelta(hours=8))
SCHEMA_VERSION = "1.0"

BENCHMARK = "SPY"
MIN_SAMPLE_WARN = 20          # statistically-thin warning threshold
MA50_PROXY_WEEKS = 10         # ≈ 50 trading days
MIN_BARS_FOR_SIGNAL = 12      # classify_state needs cycle + 8w drift history

# RS blend weights + trend bonus — mirrors build_dd_screener.compute_yfinance_
# timing_fallback (lines ~556-567). Kept here (not imported) to avoid pulling the
# whole orchestrator at import; logic is intentionally identical.
RS_W1, RS_W4, RS_W13 = 0.2, 0.3, 0.5


# ── helpers ───────────────────────────────────────────────────────────────────
def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def _safe_float(x) -> Optional[float]:
    try:
        f = float(x)
        return None if f != f else f
    except (TypeError, ValueError):
        return None


# ── universe ──────────────────────────────────────────────────────────────────
def load_universe(quality_min: float, growth_min: float,
                  growth_type_only: bool) -> list[dict]:
    """Read quality-entry.json all_scored, apply the entry-state universe filter."""
    if not QE_JSON.exists():
        print(f"  ERR: {QE_JSON} not found — run build_quality_entry.py first",
              file=sys.stderr)
        sys.exit(2)
    qe = json.loads(QE_JSON.read_text(encoding="utf-8"))
    rows = qe.get("all_scored")
    if rows is None:
        rows = (qe.get("tier_a") or []) + (qe.get("tier_b") or [])
        print("  WARN: quality-entry.json missing 'all_scored' — using tier_a+tier_b",
              file=sys.stderr)
    out = []
    for r in rows:
        t = r.get("ticker")
        q = _safe_float(r.get("quality"))
        g = _safe_float(r.get("growth"))
        if not t or q is None or g is None:
            continue
        if q < quality_min or g < growth_min:
            continue
        if growth_type_only and r.get("archetype") != "成長型":
            continue
        out.append({"ticker": t, "quality": q, "growth": g,
                    "name": r.get("name") or t, "yf": _yf_ticker_for_ma(t)})
    return out


# ── data fetch ────────────────────────────────────────────────────────────────
def fetch_weekly_closes(yf_tickers: list[str], chunk_size: int = 40,
                        max_retries: int = 3) -> dict[str, "pd.Series"]:
    """Batch-fetch full-history weekly closes. Returns {yf_ticker: Series}.

    Chunked with backoff to survive yfinance rate-limits. Failed tickers are
    dropped (caller skips them)."""
    out: dict[str, pd.Series] = {}
    uniq = sorted(set(yf_tickers))
    n_chunks = (len(uniq) + chunk_size - 1) // chunk_size
    backoff = (15, 45, 120)
    for ci in range(n_chunks):
        chunk = uniq[ci * chunk_size:(ci + 1) * chunk_size]
        for attempt in range(max_retries):
            try:
                df = yf.download(chunk, period="max", interval="1wk",
                                 group_by="ticker", progress=False,
                                 threads=True, auto_adjust=True)
                if df is None or df.empty:
                    raise RuntimeError("empty frame (likely rate-limited)")
                break
            except Exception as exc:
                if attempt < max_retries - 1:
                    d = backoff[min(attempt, len(backoff) - 1)]
                    print(f"  [fetch] chunk {ci+1}/{n_chunks} attempt {attempt+1} "
                          f"failed ({type(exc).__name__}); sleep {d}s", file=sys.stderr)
                    time.sleep(d)
                else:
                    print(f"  [fetch] chunk {ci+1}/{n_chunks} exhausted retries; "
                          f"dropping {len(chunk)}", file=sys.stderr)
                    df = None
        if df is None:
            continue
        for t in chunk:
            try:
                s = (df["Close"] if len(chunk) == 1 else df[t]["Close"]).dropna()
                if not s.empty:
                    out[t] = s.astype(float)
            except (KeyError, TypeError):
                continue
        if ci < n_chunks - 1:
            time.sleep(2)
    return out


# ── signal reconstruction ─────────────────────────────────────────────────────
def reconstruct(universe: list[dict], closes_by_yf: dict[str, "pd.Series"],
                spy: "pd.Series", years: int) -> tuple[list[dict], dict]:
    """Walk every (ticker, week) in the sample window, recompute the point-in-time
    state, and emit signal rows. Returns (signals, meta).

    Each signal row: {ticker, week (master pos), date, state ∈ {BREAKOUT,
    PULLBACK_WATCH}, breakout_no_rs (bool), rs, ma50, dist_250w, ...}."""
    # Master weekly calendar = SPY's index (the benchmark spans the longest).
    master = spy.index
    # Align everything to master so cross-sectional RS + entry/exit share a clock.
    aligned: dict[str, pd.Series] = {}
    for u in universe:
        s = closes_by_yf.get(u["yf"])
        if s is None:
            continue
        aligned[u["ticker"]] = s.reindex(master)
    if not aligned:
        return [], {"reason": "no tickers fetched"}

    closes_df = pd.DataFrame(aligned)            # index=master, cols=ticker
    spy_master = spy.reindex(master)

    # --- vectorised timing fields (cheap; computed for ALL weeks) -------------
    # ma50 proxy: price vs trailing 10-week SMA.
    ma50_df = (closes_df / closes_df.rolling(MA50_PROXY_WEEKS).mean() - 1.0) * 100.0
    # RS proxy: blended 1/4/13-week momentum percentile-ranked across the universe.
    r1 = closes_df.pct_change(1) * 100.0
    r4 = closes_df.pct_change(4) * 100.0
    r13 = closes_df.pct_change(13) * 100.0
    pr1 = r1.rank(axis=1, pct=True, method="max") * 100.0
    pr4 = r4.rank(axis=1, pct=True, method="max") * 100.0
    pr13 = r13.rank(axis=1, pct=True, method="max") * 100.0
    blended = RS_W1 * pr1 + RS_W4 * pr4 + RS_W13 * pr13
    # Trend bonus (matches build_dd_screener logic): strict up +5, monotone-up +2,
    # strict down -5, else 0.
    bonus = pd.DataFrame(0.0, index=closes_df.index, columns=closes_df.columns)
    bonus = bonus.mask((pr1 > pr4) & (pr4 > pr13), 5.0)
    bonus = bonus.mask((pr1 >= pr4) & (pr4 >= pr13) & ~((pr1 > pr4) & (pr4 > pr13)), 2.0)
    bonus = bonus.mask((pr1 < pr4) & (pr4 < pr13), -5.0)
    rs_df = (blended + bonus).clip(upper=100.0)

    # --- sample window -------------------------------------------------------
    last_date = master[-1]
    start_date = last_date - pd.DateOffset(years=years)
    win_positions = [p for p, d in enumerate(master) if d >= start_date]
    p_first = win_positions[0] if win_positions else 0

    signals: list[dict] = []
    pos_index = {d: p for p, d in enumerate(master)}

    for ticker, s in aligned.items():
        native = s.dropna()
        if native.empty:
            continue
        for p in range(p_first, len(master)):
            price = closes_df.iat[p, closes_df.columns.get_loc(ticker)]
            if price != price:  # NaN — not listed yet / no bar
                continue
            week_date = master[p]
            # Point-in-time slice: native bars up to & including this week only.
            slice_ = native.loc[:week_date]
            if len(slice_) < MIN_BARS_FOR_SIGNAL:
                continue
            ma = _compute_derived(slice_)
            ma_label = ma_gate(ma)
            ma50 = ma50_df.iat[p, ma50_df.columns.get_loc(ticker)]
            rs = rs_df.iat[p, rs_df.columns.get_loc(ticker)]
            timing = {
                "ma50_pct": None if ma50 != ma50 else round(float(ma50), 1),
                "rs_score": None if rs != rs else round(float(rs), 1),
            }
            state, sub = classify_state(ma_label, ma, timing)

            is_pb = (state == STATE_PULLBACK and sub == SUB_WATCH)
            is_bk = (state == STATE_BREAKOUT)
            # BREAKOUT minus the RS gate — re-run with RS forced to pass, to size
            # how much of the BREAKOUT shortfall is the (fragile) RS reconstruction.
            bk_no_rs = False
            if not is_bk:
                t2 = dict(timing, rs_score=100.0)
                st2, _ = classify_state(ma_label, ma, t2)
                bk_no_rs = (st2 == STATE_BREAKOUT)

            if not (is_pb or is_bk or bk_no_rs):
                continue
            signals.append({
                "ticker": ticker,
                "pos": p,
                "date": week_date.strftime("%Y-%m-%d"),
                "entry_price": round(float(price), 4),
                "is_pullback": bool(is_pb),
                "is_breakout": bool(is_bk),
                "is_breakout_no_rs": bool(is_bk or bk_no_rs),
                "rs": timing["rs_score"],
                "ma50_pct": timing["ma50_pct"],
                "dist_250w_high_pct": ma.get("dist_250w_high_pct"),
                "weeks_since_250w_high": ma.get("weeks_since_250w_high"),
                "ma_label": ma_label,
            })

    meta = {
        "n_tickers_fetched": len(aligned),
        "sample_window_start": master[p_first].strftime("%Y-%m-%d"),
        "sample_window_end": last_date.strftime("%Y-%m-%d"),
        "master_weeks": len(master),
    }
    return signals, meta


# ── trade simulation (cooldown dedup + forward return) ────────────────────────
def simulate(signals: list[dict], closes_by_yf: dict[str, "pd.Series"],
             universe: list[dict], spy: "pd.Series", horizon: int,
             sample: str) -> list[dict]:
    """For one (sample, horizon): apply per-ticker per-state cooldown=horizon, then
    compute the realised forward return entry→exit and the matched SPY return.

    sample ∈ {'pullback', 'breakout', 'breakout_no_rs'}."""
    flag = {"pullback": "is_pullback", "breakout": "is_breakout",
            "breakout_no_rs": "is_breakout_no_rs"}[sample]
    master = spy.index
    spy_master = spy.reindex(master).values
    yf_by_ticker = {u["ticker"]: u["yf"] for u in universe}
    aligned: dict[str, np.ndarray] = {}
    for u in universe:
        s = closes_by_yf.get(u["yf"])
        if s is not None:
            aligned[u["ticker"]] = s.reindex(master).values

    # Order signals by (ticker, pos) so cooldown is applied chronologically.
    rel = sorted([s for s in signals if s[flag]], key=lambda s: (s["ticker"], s["pos"]))
    last_entry_pos: dict[str, int] = {}
    trades: list[dict] = []
    n_censored = 0
    for sig in rel:
        t = sig["ticker"]
        p = sig["pos"]
        if t in last_entry_pos and (p - last_entry_pos[t]) < horizon:
            continue  # cooldown: overlapping same-state signal suppressed
        exit_p = p + horizon
        if exit_p >= len(master):
            n_censored += 1
            continue  # holding period would run past available data
        arr = aligned.get(t)
        if arr is None:
            continue
        entry_px, exit_px = arr[p], arr[exit_p]
        spy_entry, spy_exit = spy_master[p], spy_master[exit_p]
        if (entry_px != entry_px or exit_px != exit_px
                or spy_entry != spy_entry or spy_exit != spy_exit
                or entry_px == 0 or spy_entry == 0):
            continue
        ret = (exit_px / entry_px - 1.0) * 100.0
        spy_ret = (spy_exit / spy_entry - 1.0) * 100.0
        last_entry_pos[t] = p
        trades.append({
            "ticker": t,
            "entry_date": sig["date"],
            "exit_date": master[exit_p].strftime("%Y-%m-%d"),
            "ret_pct": round(ret, 2),
            "spy_ret_pct": round(spy_ret, 2),
            "alpha_pct": round(ret - spy_ret, 2),
            "rs": sig["rs"],
        })
    if n_censored:
        print(f"    [{sample} {horizon}w] {n_censored} signal(s) censored "
              f"(holding period past data end)")
    return trades


def metrics(trades: list[dict]) -> dict:
    """Compute the indicator block for one sample×horizon trade list."""
    n = len(trades)
    if n == 0:
        return {"n": 0}
    rets = np.array([t["ret_pct"] for t in trades], dtype=float)
    spy = np.array([t["spy_ret_pct"] for t in trades], dtype=float)
    alpha = np.array([t["alpha_pct"] for t in trades], dtype=float)
    pcts = {f"p{q}": round(float(np.percentile(rets, q)), 2)
            for q in (10, 25, 50, 75, 90)}
    return {
        "n": n,
        "win_rate": round(float((rets > 0).mean()) * 100, 1),
        "win_rate_vs_spy": round(float((alpha > 0).mean()) * 100, 1),
        "mean_ret": round(float(rets.mean()), 2),
        "median_ret": round(float(np.median(rets)), 2),
        "std_ret": round(float(rets.std(ddof=1)) if n > 1 else 0.0, 2),
        "worst_ret": round(float(rets.min()), 2),       # single-trade max drawdown
        "best_ret": round(float(rets.max()), 2),
        "percentiles": pcts,
        "spy_mean_ret": round(float(spy.mean()), 2),
        "mean_alpha": round(float(alpha.mean()), 2),
        "median_alpha": round(float(np.median(alpha)), 2),
        "thin": n < MIN_SAMPLE_WARN,
    }


# ── HTML rendering ────────────────────────────────────────────────────────────
SAMPLE_LABELS = {
    "pullback": "PULLBACK · WATCH",
    "breakout": "BREAKOUT (含 RS≥80 閘)",
    "breakout_no_rs": "BREAKOUT (移除 RS 閘 · 敏感度對照)",
}


def _svg_histogram(trades: list[dict], color: str) -> str:
    """Self-contained SVG histogram of forward returns. 5%-buckets, mean + 0 lines."""
    if not trades:
        return '<div class="no-data">— 無樣本 —</div>'
    rets = [t["ret_pct"] for t in trades]
    lo, hi = -50.0, 100.0
    step = 5.0
    nb = int((hi - lo) / step)
    buckets = [0] * nb
    for r in rets:
        rc = min(hi - 0.01, max(lo, r))
        buckets[min(nb - 1, int((rc - lo) / step))] += 1
    bmax = max(buckets) or 1
    W, H, padb = 520, 150, 18
    bw = W / nb
    bars = []
    for i, c in enumerate(buckets):
        bh = (c / bmax) * (H - padb - 10)
        x = i * bw
        y = H - padb - bh
        bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw-1:.1f}" '
                    f'height="{bh:.1f}" fill="{color}" opacity="0.78"/>')
    # zero line + mean line
    def xpos(v):
        return (min(hi, max(lo, v)) - lo) / (hi - lo) * W
    x0 = xpos(0.0)
    mean = sum(rets) / len(rets)
    xm = xpos(mean)
    axis = (f'<line x1="{x0:.1f}" y1="0" x2="{x0:.1f}" y2="{H-padb:.1f}" '
            f'stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,3"/>'
            f'<line x1="{xm:.1f}" y1="0" x2="{xm:.1f}" y2="{H-padb:.1f}" '
            f'stroke="#dc2626" stroke-width="1.5"/>'
            f'<text x="{xm+3:.1f}" y="12" fill="#dc2626" font-size="10">'
            f'mean {mean:+.1f}%</text>')
    ticks = []
    for v in (-50, -25, 0, 25, 50, 75, 100):
        x = xpos(v)
        ticks.append(f'<text x="{x:.1f}" y="{H-4}" fill="#94a3b8" font-size="9" '
                     f'text-anchor="middle">{v}%</text>')
    return (f'<svg viewBox="0 0 {W} {H}" class="hist" preserveAspectRatio="none">'
            f'{"".join(bars)}{axis}{"".join(ticks)}</svg>')


def _svg_boxplot(samples: list[tuple]) -> str:
    """Shared-axis horizontal box plots (P10–P90 whisker, P25–P75 box, median).
    samples: list of (label, metrics_dict, color)."""
    rows = [(lbl, m, c) for (lbl, m, c) in samples if m.get("n", 0) > 0]
    if not rows:
        return '<div class="no-data">— 無樣本 —</div>'
    lo, hi = -50.0, 100.0
    W = 720
    left, right = 230, 30
    plot_w = W - left - right
    rh = 38
    H = rh * len(rows) + 34

    def xpos(v):
        return left + (min(hi, max(lo, v)) - lo) / (hi - lo) * plot_w

    parts = []
    # gridlines
    for v in (-50, -25, 0, 25, 50, 75, 100):
        x = xpos(v)
        col = "#cbd5e1" if v == 0 else "#eef2f7"
        parts.append(f'<line x1="{x:.1f}" y1="20" x2="{x:.1f}" y2="{H-14:.1f}" '
                     f'stroke="{col}" stroke-width="1"/>')
        parts.append(f'<text x="{x:.1f}" y="14" fill="#94a3b8" font-size="9" '
                     f'text-anchor="middle">{v}%</text>')
    for i, (lbl, m, c) in enumerate(rows):
        cy = 28 + i * rh
        pc = m["percentiles"]
        p10, p25, p50, p75, p90 = (pc["p10"], pc["p25"], pc["p50"],
                                   pc["p75"], pc["p90"])
        x10, x25, x50, x75, x90 = map(xpos, (p10, p25, p50, p75, p90))
        # whisker
        parts.append(f'<line x1="{x10:.1f}" y1="{cy:.1f}" x2="{x90:.1f}" '
                     f'y2="{cy:.1f}" stroke="{c}" stroke-width="1.5"/>')
        parts.append(f'<line x1="{x10:.1f}" y1="{cy-6:.1f}" x2="{x10:.1f}" '
                     f'y2="{cy+6:.1f}" stroke="{c}" stroke-width="1.5"/>')
        parts.append(f'<line x1="{x90:.1f}" y1="{cy-6:.1f}" x2="{x90:.1f}" '
                     f'y2="{cy+6:.1f}" stroke="{c}" stroke-width="1.5"/>')
        # box
        parts.append(f'<rect x="{x25:.1f}" y="{cy-10:.1f}" width="{x75-x25:.1f}" '
                     f'height="20" fill="{c}" opacity="0.22" stroke="{c}"/>')
        # median
        parts.append(f'<line x1="{x50:.1f}" y1="{cy-10:.1f}" x2="{x50:.1f}" '
                     f'y2="{cy+10:.1f}" stroke="{c}" stroke-width="2"/>')
        # mean dot
        xm = xpos(m["mean_ret"])
        parts.append(f'<circle cx="{xm:.1f}" cy="{cy:.1f}" r="3" fill="{c}"/>')
        # label
        parts.append(f'<text x="6" y="{cy+4:.1f}" fill="#1e3a5f" font-size="11" '
                     f'font-weight="600">{lbl} (n={m["n"]})</text>')
    return (f'<svg viewBox="0 0 {W} {H}" class="boxplot" '
            f'preserveAspectRatio="xMidYMid meet">{"".join(parts)}</svg>')


def _fmt(v, suffix="", dash="—"):
    return dash if v is None else f"{v}{suffix}"


def render_html(doc: dict, out_path: Path) -> None:
    meta = doc["meta"]
    params = doc["params"]
    res = doc["results"]
    horizons = params["horizons"]

    # metric matrix table rows
    SAMPLE_COLORS = {"pullback": "#0c4a6e", "breakout": "#166534",
                     "breakout_no_rs": "#64748b"}
    metric_rows = []
    for sample in ("pullback", "breakout", "breakout_no_rs"):
        label = SAMPLE_LABELS[sample]
        for h in horizons:
            m = res[sample][str(h)]["metrics"]
            if m.get("n", 0) == 0:
                metric_rows.append(
                    f'<tr><td class="left">{label}</td><td>{h}w</td>'
                    f'<td colspan="11" class="no-data">無樣本</td></tr>')
                continue
            pc = m["percentiles"]
            thin = m.get("thin")
            n_cell = (f'<span class="thin-warn" title="樣本 &lt; {MIN_SAMPLE_WARN}，'
                      f'統計不顯著">{m["n"]} ⚠</span>') if thin else str(m["n"])
            wr_cls = "pos" if m["win_rate"] >= 50 else "neg"
            al_cls = "pos" if m["mean_alpha"] >= 0 else "neg"
            metric_rows.append(
                f'<tr class="{"thin-row" if thin else ""}">'
                f'<td class="left">{label}</td><td>{h}w</td>'
                f'<td>{n_cell}</td>'
                f'<td class="{wr_cls}">{m["win_rate"]}%</td>'
                f'<td>{m["mean_ret"]:+.1f}%</td>'
                f'<td>{m["median_ret"]:+.1f}%</td>'
                f'<td>{m["std_ret"]:.1f}</td>'
                f'<td class="neg">{m["worst_ret"]:+.1f}%</td>'
                f'<td>{pc["p10"]:+.0f} / {pc["p25"]:+.0f} / {pc["p50"]:+.0f} / '
                f'{pc["p75"]:+.0f} / {pc["p90"]:+.0f}</td>'
                f'<td>{m["spy_mean_ret"]:+.1f}%</td>'
                f'<td class="{al_cls}">{m["mean_alpha"]:+.1f}%</td>'
                f'<td>{m["win_rate_vs_spy"]}%</td>'
                f'</tr>')

    # box-plot panels (one per horizon)
    box_panels = []
    for h in horizons:
        samples = [(SAMPLE_LABELS[s].split(" ")[0] + (" (no RS)" if s == "breakout_no_rs" else ""),
                    res[s][str(h)]["metrics"], SAMPLE_COLORS[s])
                   for s in ("pullback", "breakout", "breakout_no_rs")]
        box_panels.append(
            f'<div class="chart-card"><h3>持有 {h} 週 — 報酬分布 box plot '
            f'<span class="hint">(box=P25–P75 · 中線=中位數 · 鬚=P10–P90 · 點=平均)</span></h3>'
            f'{_svg_boxplot(samples)}</div>')

    # histogram grid
    hist_cards = []
    for sample in ("pullback", "breakout", "breakout_no_rs"):
        for h in horizons:
            m = res[sample][str(h)]
            hist_cards.append(
                f'<div class="hist-card"><div class="hist-title">'
                f'{SAMPLE_LABELS[sample]} · {h}w '
                f'<span class="hint">n={m["metrics"].get("n",0)}</span></div>'
                f'{_svg_histogram(m["trades"], SAMPLE_COLORS[sample])}</div>')

    flt = params["filters"]
    universe_line = (f'Q ≥ {flt["quality_min"]} ∩ G ≥ {flt["growth_min"]}'
                     + (' ∩ archetype=成長型' if flt["growth_type_only"] else '')
                     + f' → <b>{meta["n_tickers_fetched"]}</b> 檔成功取得週線')

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entry-State 訊號回測 — 固定持有期報酬分布 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f0f5fb;color:#1e3a5f;line-height:1.5}}
.imq-nav-root{{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.7rem 20px;font-size:13px;position:sticky;top:0;z-index:1000}}
.imq-nav-inner{{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}}
.imq-logo{{font-weight:700;color:#fff !important;text-decoration:none;font-size:15px}}
.imq-logo span{{color:#3b82f6}}
.imq-menu a{{color:rgba(255,255,255,.72) !important;font-size:.8rem;font-weight:500;padding:.42rem .6rem;border-radius:6px;text-decoration:none}}
.imq-menu a:hover{{color:#fff !important;background:rgba(255,255,255,.08)}}
.hero{{background:#fff;border-bottom:1px solid #dce8f5;padding:24px 32px 18px}}
.hero-inner{{max-width:min(1280px,96vw);margin:0 auto}}
.hero-h1{{font-size:22px;font-weight:600;color:#0f2a45;margin-bottom:6px}}
.hero-sub{{font-size:12px;color:#5a7a9a;line-height:1.6;max-width:920px}}
.hero-stats{{display:flex;gap:14px;margin-top:12px;flex-wrap:wrap}}
.hero-stat{{background:#f0f5fb;border:1px solid #dce8f5;border-radius:6px;padding:7px 11px;font-size:11px;color:#5a7a9a}}
.hero-stat strong{{color:#1e3a5f;font-size:13px;display:block;margin-bottom:1px}}
.section{{max-width:min(1280px,96vw);margin:0 auto;padding:22px 32px}}
.caveat-panel{{background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:14px 18px;margin-bottom:20px;font-size:12.5px;color:#991b1b;line-height:1.7}}
.caveat-panel strong{{color:#7f1d1d;display:block;margin-bottom:6px;font-size:13px}}
.caveat-panel ol{{margin-left:20px}}
.caveat-panel code{{background:#fff;padding:1px 5px;border-radius:3px;font-size:11px;color:#7f1d1d}}
.card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:16px 18px;margin-bottom:20px}}
.card h2{{font-size:16px;font-weight:700;margin-bottom:6px;color:#0f2a45}}
.card .desc{{font-size:12px;color:#5a7a9a;margin-bottom:12px;line-height:1.6}}
table{{width:100%;border-collapse:collapse;font-size:11.5px}}
th{{background:#f0f6ff;color:#5a7a9a;font-weight:700;padding:7px 7px;text-align:right;border-bottom:2px solid #dce8f5;font-size:10px;letter-spacing:.03em;text-transform:uppercase;white-space:nowrap}}
th.left{{text-align:left}}
td{{padding:7px 7px;text-align:right;border-bottom:1px solid #f0f5fb;font-variant-numeric:tabular-nums}}
td.left{{text-align:left;color:#0f2a45;font-weight:600}}
td.pos{{color:#16a34a;font-weight:700}}
td.neg{{color:#dc2626;font-weight:700}}
.thin-row{{background:#fff7ed}}
.thin-warn{{color:#c2410c;font-weight:700}}
.no-data{{color:#94a3b8;font-style:italic;text-align:center}}
.chart-card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:14px 18px;margin-bottom:18px}}
.chart-card h3{{font-size:13px;font-weight:700;color:#0f2a45;margin-bottom:10px}}
.chart-card .hint,.hist .hint,.hint{{font-size:10.5px;color:#94a3b8;font-weight:400}}
svg.boxplot{{width:100%;height:auto}}
.hist-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
.hist-card{{background:#fff;border:1px solid #dce8f5;border-radius:8px;padding:10px 12px}}
.hist-title{{font-size:11.5px;font-weight:700;color:#0f2a45;margin-bottom:6px}}
svg.hist{{width:100%;height:130px;display:block}}
.footer{{padding:26px 32px;font-size:11px;color:#5a7a9a;line-height:1.7;max-width:min(1280px,96vw);margin:0 auto;border-top:1px solid #dce8f5}}
.footer code{{background:#f0f5fb;padding:1px 5px;border-radius:3px;font-size:10px}}
@media(max-width:760px){{.hist-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header class="imq-nav-root"><div class="imq-nav-inner">
  <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
  <nav class="imq-menu">
    <a href="/dd-screener/">DD Screener</a>
    <a href="/dd-screener/entry-state.html">⚙️ Entry State</a>
    <a href="/backtest/">量化回測</a>
  </nav>
</div></header>

<div class="hero"><div class="hero-inner">
  <div class="hero-h1">Entry-State 訊號回測 — 固定持有期報酬分布</div>
  <div class="hero-sub">
    對 <a href="/dd-screener/entry-state.html" style="color:#2563eb">進場狀態機</a>的
    <b>PULLBACK·WATCH</b> 與 <b>BREAKOUT</b> 兩類訊號做點對點歷史重建:在每個歷史週末
    <b>只用當週之前的資料</b>重算當時的第一層 MA 閘 + 第二層狀態(沿用 live 頁
    <code>_compute_derived</code> / <code>ma_gate</code> / <code>classify_state</code>
    完全相同的門檻,無 look-ahead),量測「訊號當週收盤買進 → 固定持有期賣出」的裸報酬分布。
  </div>
  <div class="hero-stats">
    <div class="hero-stat"><strong>{meta["sample_window_start"]} → {meta["sample_window_end"]}</strong>樣本窗({params["years"]}y)</div>
    <div class="hero-stat"><strong>{meta["n_tickers_fetched"]}</strong>母體檔數</div>
    <div class="hero-stat"><strong>{params["horizons"][0]}w / {params["horizons"][-1]}w</strong>持有期</div>
    <div class="hero-stat"><strong>{BENCHMARK}</strong>對照基準</div>
    <div class="hero-stat"><strong>{meta["run_ts"][:16].replace("T"," ")}</strong>生成(台北)</div>
  </div>
</div></div>

<div class="section">

  <div class="caveat-panel">
    <strong>⚠️ 動手前必讀 — 這份回測有四個結構性侷限,數字不是無偏估計</strong>
    <ol>
      <li><b>Survivorship bias(最重要)</b>:母體是<u>今日</u>通過品質閘的 {meta["n_tickers_fetched"]} 檔
        ({universe_line.split(' → ')[0]}),這些是「活下來且現在還夠強」的標的。用它們的歷史報酬回測,
        天然<b>偏高</b> — 當年同樣發出訊號但後來掉出母體 / 下市的標的<b>完全沒被計入</b>。
        請當作「最好情況的上界」,不是期望值。</li>
      <li><b>樣本稀疏</b>:entry-state 頁自述 PULLBACK 命中率約 6%/檔、約 17 週才一次;訊號天生少,
        任一格 <code>n &lt; {MIN_SAMPLE_WARN}</code> 會標紅 ⚠,統計不顯著,勿過度解讀勝率。</li>
      <li><b>無交易成本 / 滑價 / 稅</b>:裸報酬,實盤會被點差、稅與沖銷成本侵蝕。</li>
      <li><b>過去績效 ≠ 未來</b>;且 <b>RS 重建為近似</b>:live 頁 RS 對 ~511 檔美股母體百分位排名,
        歷史母體無法還原,本回測改在<u>回測母體內部</u>排名(同 blend 公式)。母體本身偏強 → RS≥80 是更嚴的門檻,
        BREAKOUT 數量可能<b>低估</b> live 頁;故另列「移除 RS 閘」一行做敏感度對照。<code>ma50_pct</code>
        亦以 10 週均線近似日線 50DMA。</li>
    </ol>
  </div>

  <div class="card">
    <h2>指標矩陣 — 狀態 × 持有期</h2>
    <div class="desc">{universe_line}。進場 = 訊號當週收盤價;出場 = 持有期滿週收盤價(不停損/停利)。
      同檔同狀態以 <b>cooldown = 持有期</b>去重避免樣本重疊。「單筆最差」即最大單筆回撤。
      Alpha = 個股報酬 − 同期 {BENCHMARK} 報酬。</div>
    <table>
      <thead><tr>
        <th class="left">狀態</th><th>持有</th><th>樣本數</th><th>勝率</th>
        <th>平均</th><th>中位</th><th>標準差</th><th>單筆最差</th>
        <th>P10/25/50/75/90</th><th>{BENCHMARK} 平均</th><th>平均 α</th><th>勝 {BENCHMARK} %</th>
      </tr></thead>
      <tbody>
{chr(10).join(metric_rows)}
      </tbody>
    </table>
  </div>

  {"".join(box_panels)}

  <div class="card">
    <h2>報酬分布直方圖</h2>
    <div class="desc">5% 一桶,範圍 −50%~+100%(超出截斷至邊界)。紅線 = 平均,灰虛線 = 0%。</div>
    <div class="hist-grid">
{chr(10).join(hist_cards)}
    </div>
  </div>

</div>

<div class="footer">
  <h4 style="color:#1e3a5f;margin-bottom:6px">方法與資料</h4>
  <p>資料源:yfinance 週線(<code>interval=1wk</code>,與 <code>build_dd_screener.py</code> 同源)。
  訊號重建逐週呼叫 <code>scripts.dd_screener_ma._compute_derived</code> +
  <code>scripts.build_entry_state.ma_gate / classify_state</code>,門檻與 live 頁一致。
  母體取自 <code>docs/dd-screener/quality-entry.json</code> 的 <code>all_scored</code>。</p>
  <p style="margin-top:8px">機器可讀:<a href="/dd-screener/entry-state-backtest.json"><code>/dd-screener/entry-state-backtest.json</code></a>
  (含每筆 trade 明細)。一次性分析,<b>未綁 cron</b>。</p>
  <p style="margin-top:12px;color:#94a3b8">Generated by <code>scripts/backtest_entry_state.py</code> · schema v{SCHEMA_VERSION} · {meta["run_ts"]}</p>
</div>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✓ Wrote {out_path} ({out_path.stat().st_size:,} bytes)")


# ── pipeline ──────────────────────────────────────────────────────────────────
def run(args) -> dict:
    print(f"=== Entry-State backtest · {_now_taipei_iso()} ===\n")
    universe = load_universe(args.quality_min, args.growth_min,
                             not args.no_growth_type)
    if args.max_tickers:
        universe = universe[:args.max_tickers]
    print(f"  Universe: {len(universe)} tickers "
          f"(Q≥{args.quality_min} / G≥{args.growth_min}"
          f"{' / 成長型' if not args.no_growth_type else ''})")
    if not universe:
        print("  ERR: empty universe", file=sys.stderr)
        sys.exit(2)

    yf_tickers = [u["yf"] for u in universe] + [BENCHMARK]
    print(f"  Fetching weekly closes for {len(set(yf_tickers))} symbols "
          f"(incl. {BENCHMARK}) ...")
    closes = fetch_weekly_closes(yf_tickers)
    spy = closes.get(BENCHMARK)
    if spy is None or spy.empty:
        print(f"  ERR: failed to fetch benchmark {BENCHMARK}", file=sys.stderr)
        sys.exit(2)
    got = sum(1 for u in universe if u["yf"] in closes)
    print(f"  Fetched {got}/{len(universe)} universe tickers + {BENCHMARK}")

    print("  Reconstructing point-in-time signals ...")
    signals, meta = reconstruct(universe, closes, spy, args.years)
    n_pb = sum(1 for s in signals if s["is_pullback"])
    n_bk = sum(1 for s in signals if s["is_breakout"])
    n_bk0 = sum(1 for s in signals if s["is_breakout_no_rs"])
    print(f"  Raw signal-weeks: PULLBACK={n_pb}  BREAKOUT={n_bk}  "
          f"BREAKOUT(no-RS)={n_bk0}")

    horizons = [int(h) for h in args.horizons.split(",")]
    results: dict = {}
    for sample in ("pullback", "breakout", "breakout_no_rs"):
        results[sample] = {}
        for h in horizons:
            trades = simulate(signals, closes, universe, spy, h, sample)
            results[sample][str(h)] = {"trades": trades, "metrics": metrics(trades)}
            m = results[sample][str(h)]["metrics"]
            print(f"    {sample:16} {h:>2}w → n={m.get('n',0):>3}  "
                  f"win={m.get('win_rate','—')}%  mean={m.get('mean_ret','—')}%  "
                  f"α={m.get('mean_alpha','—')}%"
                  + ("  ⚠THIN" if m.get('thin') else ""))

    meta["run_ts"] = _now_taipei_iso()
    doc = {
        "schema_version": SCHEMA_VERSION,
        "meta": meta,
        "params": {
            "years": args.years,
            "horizons": horizons,
            "benchmark": BENCHMARK,
            "min_sample_warn": MIN_SAMPLE_WARN,
            "cooldown": "per-ticker per-state, N = holding period",
            "ma50_proxy_weeks": MA50_PROXY_WEEKS,
            "rs_reference": "in-universe percentile (NOT live ~511-stock universe)",
            "filters": {
                "quality_min": args.quality_min,
                "growth_min": args.growth_min,
                "growth_type_only": not args.no_growth_type,
            },
        },
        "universe": [{"ticker": u["ticker"], "quality": u["quality"],
                      "growth": u["growth"]} for u in universe],
        "results": results,
    }
    return doc


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--quality-min", type=float, default=0.55)
    p.add_argument("--growth-min", type=float, default=0.50)
    p.add_argument("--no-growth-type", action="store_true",
                   help="Don't restrict to archetype=成長型")
    p.add_argument("--years", type=int, default=5, help="Sample window (default 5)")
    p.add_argument("--horizons", default="13,26",
                   help="Comma-separated holding periods in weeks (default 13,26)")
    p.add_argument("--max-tickers", type=int, default=0,
                   help="Cap universe for a fast smoke test (0 = no cap)")
    p.add_argument("--dry-run", action="store_true", help="Don't write any files")
    args = p.parse_args()

    doc = run(args)

    if args.dry_run:
        print("\n  (dry-run) skipping writes")
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # Strip per-trade lists out of the *console* path but KEEP them in JSON sidecar.
    JSON_OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(f"\n  ✓ Wrote {JSON_OUT} ({JSON_OUT.stat().st_size:,} bytes)")
    render_html(doc, HTML_OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
