#!/usr/bin/env python3
"""實單台股腿「最新日晚到／暫時價」修正的測試（scripts/update_long_track_w52_adaptive.py）。

背景：yfinance 的 0050.TW 最新一天常為 Close=NaN（fetch_close 的 dropna 會丟掉），
或給盤後尚未定案的暫時價；腿的最新日因此比另一腿少一天，當日目標權重以舊價計算
（2026-10-15 差 12.3pp）。修法＝用證交所官方收盤補最新一兩根（reconcile_with_official），
官方也補不上時由 tw_leg_delays 偵測並標示資料延遲。本檔不打網路。

三種情境：(a) yfinance 最新日缺 (b) 最新日 Close=NaN (c) 官方也抓不到。
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import update_long_track_w52_adaptive as w  # noqa: E402


def _series(n=30, last_day="2026-10-15", start=100.0):
    idx = pd.bdate_range(end=last_day, periods=n)
    return pd.Series(start + np.arange(n) * 0.1, index=idx, dtype="float64")


def _official_for(c: pd.Series, extra: dict | None = None) -> dict:
    """官方原始收盤：既有日期＝yfinance 值（還原因子 1 的區段），再加晚到的日子。"""
    off = {d: float(v) for d, v in c.items()}
    for k, v in (extra or {}).items():
        off[pd.Timestamp(k)] = v
    return off


# ---- (a) yfinance 最新日缺 --------------------------------------------------
def test_missing_latest_day_is_appended_from_official():
    c = _series()
    off = _official_for(c, {"2026-10-16": 103.2})
    out, notes = w.reconcile_with_official(c, off)
    assert out.index[-1] == pd.Timestamp("2026-10-16")
    assert out.iloc[-1] == 103.2
    assert notes["appended"] == ["2026-10-16"] and notes["refreshed"] == []
    # 歷史逐位元不動
    pd.testing.assert_series_equal(out.iloc[:-1], c, check_freq=False)


# ---- (b) 最新日 NaN：fetch_close 先 dropna 再補，等同 (a)；另測暫時價換官方 ----
def test_nan_latest_row_dropped_then_filled():
    c = _series()
    raw = pd.concat([c, pd.Series([np.nan], index=[pd.Timestamp("2026-10-16")])])
    out, notes = w.reconcile_with_official(raw.dropna(), _official_for(c, {"2026-10-16": 103.2}))
    assert out.index[-1] == pd.Timestamp("2026-10-16") and out.iloc[-1] == 103.2
    assert not out.isna().any()


def test_provisional_last_bar_replaced_by_official_close():
    c = _series()
    off = _official_for(c)
    last = c.index[-1]
    c2 = c.copy()
    c2.iloc[-1] = off[last] + 0.6          # 盤後暫時價，與官方差 > 容忍
    out, notes = w.reconcile_with_official(c2, off)
    assert out.iloc[-1] == off[last]
    assert notes["refreshed"] == [last.strftime("%Y-%m-%d")] and notes["appended"] == []
    pd.testing.assert_series_equal(out.iloc[:-1], c2.iloc[:-1])


def test_no_change_when_complete_and_matching():
    c = _series()
    out, notes = w.reconcile_with_official(c, _official_for(c))
    pd.testing.assert_series_equal(out, c)
    assert notes["appended"] == [] and notes["refreshed"] == []


def test_adjusted_regime_last_bar_is_not_overwritten():
    """前一根與官方不吻合（還原口徑≠原始價，除權息過渡期）→ 不敢換最後一根。"""
    c = _series()
    off = {d: float(v) / 0.99 for d, v in c.items()}   # 全段還原因子 0.99
    out, notes = w.reconcile_with_official(c, off)
    pd.testing.assert_series_equal(out, c)
    assert notes["refreshed"] == []


def test_implausible_or_too_long_gap_not_patched():
    c = _series()
    out, notes = w.reconcile_with_official(c, _official_for(c, {"2026-10-16": 150.0}))
    assert out.index[-1] == c.index[-1] and notes["skipped"]
    many = {f"2026-10-{d}": 103.0 for d in (16, 19, 20, 21)}
    out, notes = w.reconcile_with_official(c, _official_for(c, many))
    assert out.index[-1] == c.index[-1] and "不補" in notes["skipped"]


# ---- (c) 官方也抓不到 --------------------------------------------------------
@pytest.mark.parametrize("off", [None, {}])
def test_official_unavailable_leaves_series_untouched(off):
    c = _series()
    out, notes = w.reconcile_with_official(c, off)
    pd.testing.assert_series_equal(out, c)
    assert notes["official"] is False and notes["official_latest"] is None


def test_fetch_official_closes_never_raises(monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("blocked")
    monkeypatch.setattr(w, "_get_json_retry", boom)
    assert w.fetch_official_closes("0050", pd.Timestamp("2026-10-14")) is None


def test_delay_detected_when_one_leg_behind_and_official_down():
    a = _series(last_day="2026-10-15")                 # 0050 晚一天
    b = _series(last_day="2026-10-16")                 # 2330 已到
    px = {"0050": a, "2330": b}
    notes = {"0050": {"official_latest": None}, "2330": {"official_latest": None}}
    d = w.tw_leg_delays(px, notes, ["0050", "2330"])
    assert list(d) == ["0050"]
    assert d["0050"] == {"last": "2026-10-15", "ref": "2026-10-16"}


def test_delay_detected_from_official_latest_date_when_both_legs_behind():
    px = {"0050": _series(last_day="2026-10-15"), "2330": _series(last_day="2026-10-15")}
    notes = {"0050": {"official_latest": "2026-10-16"}, "2330": {"official_latest": None}}
    assert set(w.tw_leg_delays(px, notes, ["0050", "2330"])) == {"0050", "2330"}


def test_no_delay_after_successful_patch():
    c = _series()
    p, n = w.reconcile_with_official(c, _official_for(c, {"2026-10-16": 103.2}))
    px = {"0050": p, "2330": _series(last_day="2026-10-16")}
    assert w.tw_leg_delays(px, {"0050": n, "2330": {"official_latest": None}}, ["0050", "2330"]) == {}


# ---- 修正的實質效果：目標權重回到完整資料的值 ---------------------------------
def test_target_weight_with_patched_bar_equals_full_data_value():
    rng = np.random.default_rng(7)
    idx = pd.bdate_range(end="2026-10-16", periods=1500)
    full = pd.Series(100 * np.exp(np.cumsum(rng.normal(0.0004, 0.012, len(idx)))), index=idx)
    stale = full.iloc[:-1]                                   # yfinance 缺最新日
    off = {d: float(v) for d, v in full.items()}
    patched, _ = w.reconcile_with_official(stale, off)
    pd.testing.assert_series_equal(patched, full, check_freq=False)
    t = "0050"
    fixed = w._daily_record({t: patched}, [t], patched.index[-1], "live")["tickers"][t]["final_pct"]
    truth = w._daily_record({t: full}, [t], full.index[-1], "live")["tickers"][t]["final_pct"]
    old = w._daily_record({t: stale}, [t], stale.index[-1], "live")["tickers"][t]["final_pct"]
    assert fixed == truth
    assert isinstance(old, float)


# ---- main 路徑的抑制邏輯 ------------------------------------------------------
def test_detect_changes_skips_delayed_legs():
    sigs = {t: {"gate": True, "final": 0.0} for t in w.ALL_TICKERS}
    prev = {"tickers": {t: {"gate": True, "executed_pct": 50.0} for t in w.ALL_TICKERS}}
    assert len(w.detect_changes(prev, sigs)) == len(w.ALL_TICKERS)       # 目標 0 vs 現持 50 → 全觸發
    kept = w.detect_changes(prev, sigs, skip_legs={"0050", "2330"})
    assert all("台股" not in c for c in kept) and len(kept) == 2
