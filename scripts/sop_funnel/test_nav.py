#!/usr/bin/env python3
"""NAV 組合模擬層合成測試 — 單筆對帳 / 額度爭奪 / 斷路器觸發與解除 / 賣腿現金回流。

跑法：python3 scripts/sop_funnel/test_nav.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sop_funnel.backtest_full import nav_simulation  # noqa: E402

N_PASS = 0


def ok(cond, msg):
    global N_PASS
    if not cond:
        raise AssertionError(f"FAIL: {msg}")
    N_PASS += 1
    print(f"  ✓ {msg}")


def make_closes(series_map: dict[str, list[float]], start="2024-01-01") -> pd.DataFrame:
    n = max(len(v) for v in series_map.values())
    idx = pd.bdate_range(start, periods=n)
    return pd.DataFrame({t: pd.Series(v, index=idx[:len(v)])
                         for t, v in series_map.items()}, index=idx)


def trade(ticker, entry_date, entry_close, w=10.0, legs=None,
          etype="A1", base_age=30):
    return {"ticker": ticker, "entry_type": etype, "base_age_weeks": base_age,
            "signal_date": entry_date,
            "sim": {"entry_date": entry_date, "entry_close": entry_close,
                    "suggested_position_pct": w, "legs": legs or [],
                    "exit_date": None, "exit_reason": None}}


def test_single_trade_accounting():
    print("[N1] 單筆對帳：10% 部位、標的 +10% → NAV 101")
    closes = make_closes({"AAA": [100.0] * 5 + list(np.linspace(100, 110, 15))})
    idx = closes.index
    tr = trade("AAA", str(idx[2].date()), 100.0, w=10.0)
    r = nav_simulation([tr], closes, idx[0], idx[-1])
    ok(abs(r["final_nav"] - 101.0) < 0.01, f"終值 {r['final_nav']} ≈ 101")
    ok(r["blocked_entries"] == 0 and not r["breaker_episodes"], "無誤觸額度/斷路器")


def test_exposure_cap():
    print("[N2] 總曝險 ≤100%：12 筆同日 10% → 10 筆全額 + 縮量 + 額度不足")
    tick = {f"T{i:02d}": [100.0] * 20 for i in range(12)}
    closes = make_closes(tick)
    idx = closes.index
    trs = [trade(f"T{i:02d}", str(idx[3].date()), 100.0, w=10.0) for i in range(12)]
    r = nav_simulation(trs, closes, idx[0], idx[-1])
    ok(r["blocked_entries"] + r["scaled_entries"] >= 1,
       f"超額需求被攔（blocked={r['blocked_entries']}, scaled={r['scaled_entries']}）")
    last_expo = r["nav_series"][-1][2]
    ok(last_expo <= 100.01, f"曝險 {last_expo}% ≤ 100%（純現股無槓桿）")


def test_breaker_trigger_block_release():
    print("[N3] 斷路器：-15% 觸發 → 擋新倉 → 收復至 -5% 內 +5 日解除 → 放行")
    n = 60
    crash = [100.0] * 6 + list(np.linspace(100, 70, 14)) + list(np.linspace(70, 100, 20)) + [100.0] * (n - 40)
    flat = [100.0] * n
    closes = make_closes({"C1": crash, "C2": crash, "C3": crash, "C4": crash,
                          "C5": crash, "NEW": flat, "NEW2": flat})
    idx = closes.index
    trs = [trade(f"C{i}", str(idx[2].date()), 100.0, w=10.0) for i in range(1, 6)]
    # 崩跌中（斷路器應已開）嘗試進場 → 擋
    mid = str(idx[16].date())
    trs.append(trade("NEW", mid, 100.0, w=10.0))
    # 收復後再進場 → 放行
    late = str(idx[50].date())
    trs.append(trade("NEW2", late, 100.0, w=10.0))
    r = nav_simulation(trs, closes, idx[0], idx[-1])
    ok(len(r["breaker_episodes"]) >= 1, f"斷路器觸發 {r['breaker_episodes']}")
    ep = r["breaker_episodes"][0]
    ok(ep["release"] is not None, "斷路器有解除")
    blocked = [t for t in trs if t.get("nav_blocked") == "斷路器"]
    ok(any(t["ticker"] == "NEW" for t in blocked), "崩跌中的新倉被斷路器擋下")
    ok(not any(t["ticker"] == "NEW2" for t in blocked), "解除後的新倉放行")


def test_sell_leg_cash_flow():
    print("[N4] 賣腿現金回流：態④減半 → 現金增加、曝險下降")
    closes = make_closes({"AAA": [100.0] * 30})
    idx = closes.index
    legs = [{"date": str(idx[10].date()), "fraction": 0.5, "price": 100.0,
             "reason": "態④減碼"}]
    tr = trade("AAA", str(idx[2].date()), 100.0, w=10.0, legs=legs)
    r = nav_simulation([tr], closes, idx[0], idx[-1])
    expo_before = r["nav_series"][8][2]
    expo_after = r["nav_series"][12][2]
    ok(abs(expo_before - 10.0) < 0.1, f"減碼前曝險 ≈10%（{expo_before}）")
    ok(abs(expo_after - 5.0) < 0.1, f"減碼後曝險 ≈5%（{expo_after}）")
    ok(abs(r["final_nav"] - 100.0) < 0.01, "價格未動 → NAV 不變（無摩擦記帳一致）")


if __name__ == "__main__":
    for fn in [test_single_trade_accounting, test_exposure_cap,
               test_breaker_trigger_block_release, test_sell_leg_cash_flow]:
        fn()
    print(f"\nALL PASS — {N_PASS} 斷言")
