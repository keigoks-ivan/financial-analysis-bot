"""Tests for the 2026-09-24 EPS currency-mismatch fix in build_stock_dash.py.

Root cause: build_dd_screener.py's v1.8.5 foreign-listing display conversion
(see its own docstring around "foreign-listing native-currency display")
overwrites latest.json's eps_fy_curr/eps_fy_next/eps_fy3 with a LOCAL-currency
value for .TW/.T/.HK/.KS/.KQ/.SS/.SZ tickers (e.g. 2330.TW: 142.85 TWD,
2454.TW: 145.31 TWD), while docs/dd-screener/eps-estimates-snapshots/ and
eps_fx_normalize.compute_fx_normalized_revision() both expect USD-basis
inputs (Koyfin's original export currency). Feeding the already-local-currency
display value straight into compute_fx_normalized_revision() double-applies
the FX rate, producing several-thousand-percent fake revisions and an EPS/
price overlay chart whose points jump from ~USD 4 to ~TWD 143 within the same
series.

Fix (scripts/build_stock_dash.py):
  - `_fy_revision_pct_from_snapshot()`'s callers now pass the USD-basis value
    — latest.json's `{fy_key}_usd_orig` when present (foreign listings that
    went through the v1.8.5 conversion), else the display value itself
    (already USD for ADRs/US stocks) — never the local-currency display value.
  - `build_eps_snapshot_timeseries()` and `build_card_eps_revision()`'s
    `_snap_val()` now convert each historical (USD) snapshot point to the
    ticker's local display currency using that snapshot's own date's FX rate
    (`_fx_rate_on()`, new helper reusing eps_fx_normalize's cached FX lookup),
    so every point in a chart series is the same currency as the current
    value instead of mixing USD and TWD/JPY/etc.

No network access: `_fx_pair` / `_fx_rate_on` are monkeypatched with fixed
rates in every test.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_stock_dash as bsd  # noqa: E402

SNAP_3M = {
    "snapshot_date": "2026-06-23",
    "tickers": {"2330.TW": {"eps_fy_curr": 3.11, "eps_fy_next": 3.89, "eps_fy3": 4.94}},
}


def test_fy_revision_pct_from_snapshot_uses_usd_basis(monkeypatch):
    """Feeding the USD-basis current value (as the fix does) gives a sane,
    single/low-double-digit revision %, matching a hand-computed FX-normalized
    ratio — not a currency-mixing blowup."""
    monkeypatch.setattr(bsd, "_snapshot_eps_adr", lambda ticker, trow: trow)
    monkeypatch.setattr(bsd, "_fx_pair", lambda ticker, cur, base: ("TWD", 31.80, 31.20))
    pct = bsd._fy_revision_pct_from_snapshot(4.49, SNAP_3M, "2330.TW", "eps_fy_next", "2026-09-24")
    expected = (4.49 * 31.80) / (3.89 * 31.20) * 100 - 100
    assert pct == pytest.approx(expected, abs=1e-6)
    assert 0 < pct < 50


def test_fy_revision_pct_from_snapshot_regression_local_currency_input_blows_up(monkeypatch):
    """Documents the bug this fix removes: feeding the LOCAL-currency display
    value (142.85 TWD — what row.get('eps_fy_next') held pre-fix) double-
    applies the FX rate and produces a several-thousand-percent number. Guards
    against the bug being reintroduced at a call site."""
    monkeypatch.setattr(bsd, "_snapshot_eps_adr", lambda ticker, trow: trow)
    monkeypatch.setattr(bsd, "_fx_pair", lambda ticker, cur, base: ("TWD", 31.80, 31.20))
    pct = bsd._fy_revision_pct_from_snapshot(142.85, SNAP_3M, "2330.TW", "eps_fy_next", "2026-09-24")
    assert pct > 1000  # the historical bug shape (2330.TW showed +3577%)


def test_build_card_eps_revision_uses_usd_orig_not_local_display_value(monkeypatch):
    """End-to-end at the card1 (獲利預估修正) call-site level: a foreign-listing
    row whose eps_fy_next is local-currency (TWD) but carries the USD original
    in eps_fy_next_usd_orig must produce a sane vs_3m_ago_pct/
    vs_since_earnings_pct, not the currency-mixing blowup."""
    monkeypatch.setattr(bsd, "_fx_pair", lambda ticker, cur, base: ("TWD", 31.80, 31.20))
    monkeypatch.setattr(bsd, "load_dd_screener", lambda: {"as_of": "2026-09-24"})
    monkeypatch.setattr(bsd, "load_eps_snapshot_by_date", lambda d: SNAP_3M if d == "2026-06-23" else None)
    monkeypatch.setattr(bsd, "_snapshot_eps_adr", lambda ticker, trow: trow)

    row = {
        "eps_fy_curr": 107.85, "eps_fy_next": 142.85, "eps_fy3": 181.66,
        "eps_fy_curr_usd_orig": 3.39, "eps_fy_next_usd_orig": 4.49, "eps_fy3_usd_orig": 5.71,
        "eps_fy_curr_revision_pct": 0.3, "eps_fy_next_revision_pct": 0.6, "eps_fy3_revision_pct": 0.78,
        "eps_revision_baseline_date": "2026-08-28",
        "eps_rev_3m_baseline_date": "2026-06-23",
        "eps_rev_since_earnings_baseline_date": "2026-06-23",
        "eps_display_currency": "TWD",
        "fund": {},
    }
    card1 = bsd.build_card_eps_revision("2330.TW", row, {}, {"status": "no_data", "reason": "x"})
    fy_next_row = card1["table"][1]
    assert fy_next_row["current_estimate"] == 142.85  # display value unchanged
    assert 0 < fy_next_row["vs_3m_ago_pct"] < 50       # sane, not a 3500%+ blowup
    assert fy_next_row["vs_3m_ago_pct"] == fy_next_row["vs_since_earnings_pct"]  # same baseline date here


def test_build_card_eps_revision_usd_ticker_unaffected(monkeypatch):
    """A USD-reporting ticker (ADR/US stock; no `_usd_orig` stash because
    build_dd_screener.py never ran the local-currency conversion for it) must
    behave exactly as before the fix: cur_val_usd falls back to cur_val."""
    monkeypatch.setattr(bsd, "_fx_pair", lambda ticker, cur, base: (None, None, None))
    monkeypatch.setattr(bsd, "load_dd_screener", lambda: {"as_of": "2026-09-24"})
    monkeypatch.setattr(bsd, "load_eps_snapshot_by_date",
                         lambda d: {"snapshot_date": "2026-06-23", "tickers": {"TSM": {"eps_fy_next": 19.45}}}
                         if d == "2026-06-23" else None)
    monkeypatch.setattr(bsd, "_snapshot_eps_adr", lambda ticker, trow: trow)

    row = {
        "eps_fy_curr": 16.95, "eps_fy_next": 22.45, "eps_fy3": 28.55,
        # no *_usd_orig keys — matches a real TSM row in latest.json
        "eps_fy_curr_revision_pct": 0.03, "eps_fy_next_revision_pct": 0.32, "eps_fy3_revision_pct": 0.5,
        "eps_revision_baseline_date": "2026-08-28",
        "eps_rev_3m_baseline_date": "2026-06-23",
        "eps_rev_since_earnings_baseline_date": "2026-06-23",
        "eps_display_currency": "USD",
        "fund": {},
    }
    card1 = bsd.build_card_eps_revision("TSM", row, {}, {"status": "no_data", "reason": "x"})
    fy_next_row = card1["table"][1]
    assert fy_next_row["current_estimate"] == 22.45
    # pure USD ratio: 22.45/19.45 - 1
    assert fy_next_row["vs_3m_ago_pct"] == pytest.approx((22.45 / 19.45 - 1) * 100, abs=0.01)


def test_build_eps_snapshot_timeseries_converts_historical_points_to_local_currency(tmp_path, monkeypatch):
    """The price/EPS overlay chart must not mix a USD historical series with a
    local-currency current point — every point has to be the same currency."""
    snap_dir = tmp_path / "eps-estimates-snapshots"
    snap_dir.mkdir()
    (snap_dir / "2026-06.json").write_text(json.dumps({
        "snapshot_date": "2026-06-23",
        "tickers": {"2330.TW": {"eps_fy_next": 3.89, "eps_fy3": 4.94}},
    }), encoding="utf-8")
    monkeypatch.setattr(bsd, "EPS_SNAPSHOT_DIR", snap_dir)
    monkeypatch.setattr(bsd, "_snapshot_eps_adr", lambda ticker, trow: trow)
    monkeypatch.setattr(bsd, "_fx_rate_on", lambda ccy, date_str: 31.20)

    row = {"eps_display_currency": "TWD", "eps_fy_next": 142.85, "eps_fy3": 181.66}
    dd = {"as_of": "2026-09-24"}
    monkeypatch.setattr(bsd, "find_dd_screener_row", lambda t: (row, dd))

    result = bsd.build_eps_snapshot_timeseries("2330.TW")
    assert result["status"] == "ok"
    pts = {p["snapshot_date"]: p["eps_fy_next"] for p in result["points"]}
    # historical USD point (3.89) converted to TWD via the snapshot date's FX rate
    assert pts["2026-06-23"] == pytest.approx(3.89 * 31.20, abs=0.01)
    # current point is latest.json's own local-currency value, untouched
    assert pts["2026-09-24"] == 142.85
    # no unit-mismatch blowup: both points now the same order of magnitude
    values = list(pts.values())
    assert max(values) / min(values) < 3


def test_build_eps_snapshot_timeseries_usd_ticker_no_conversion(tmp_path, monkeypatch):
    """USD-display ticker (TSM/NVDA/US stocks): historical points are left as
    the raw USD snapshot value, exactly as before the fix."""
    snap_dir = tmp_path / "eps-estimates-snapshots"
    snap_dir.mkdir()
    (snap_dir / "2026-06.json").write_text(json.dumps({
        "snapshot_date": "2026-06-23",
        "tickers": {"TSM": {"eps_fy_next": 19.45, "eps_fy3": 24.7}},
    }), encoding="utf-8")
    monkeypatch.setattr(bsd, "EPS_SNAPSHOT_DIR", snap_dir)
    monkeypatch.setattr(bsd, "_snapshot_eps_adr", lambda ticker, trow: trow)

    def _fail_fx(*a, **k):  # must never be called for a USD ticker
        raise AssertionError("_fx_rate_on should not be called for a USD-display ticker")

    monkeypatch.setattr(bsd, "_fx_rate_on", _fail_fx)

    row = {"eps_display_currency": "USD", "eps_fy_next": 22.45, "eps_fy3": 28.55}
    dd = {"as_of": "2026-09-24"}
    monkeypatch.setattr(bsd, "find_dd_screener_row", lambda t: (row, dd))

    result = bsd.build_eps_snapshot_timeseries("TSM")
    assert result["status"] == "ok"
    pts = {p["snapshot_date"]: p["eps_fy_next"] for p in result["points"]}
    assert pts["2026-06-23"] == 19.45  # unconverted
    assert pts["2026-09-24"] == 22.45
