"""下軌接回（supertrend_core.takeback_table／takeback_asof／takeback_daily）的合成價格單元測試。

不依賴 Supertrend 的計算：週線、月線的方向（dir 欄）直接手設，只測接回的觸發與結束規則。
規則：週收盤 z ≤ −2.5 且趨勢水位剛好 30 → 50；週收盤 z ≥ 0 或趨勢水位離開 30 就結束；結束後 z 要先回到 −1 以上才能再觸發；
訊號日 >= BB_TAKEBACK_CUTOVER_DATE 才套用。
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import supertrend_core as stc  # noqa: E402

WEEKS = pd.date_range("2026-01-02", periods=52, freq="W-FRI")      # 週五標籤，2026-01-02 ～ 2026-12-25
MONTHS = pd.date_range("2026-01-31", periods=12, freq="ME")        # 月底標籤


def base_closes(n=52):
    """前 25 週在 100 附近小幅來回，之後由各測試覆寫。"""
    return [100.0 + (0.5 if i % 2 else 0.0) for i in range(n)]


def make_frames(closes, w_dirs, m_dirs):
    """closes／w_dirs 對 WEEKS（長度 52）；m_dirs 對 MONTHS（長度 12）。回傳 make_frames 同格式的 frames。"""
    wb = pd.DataFrame({"close": closes}, index=WEEKS)
    ws = pd.DataFrame({"dir": w_dirs}, index=WEEKS, dtype=float)
    mb = pd.DataFrame({"close": [100.0] * 12}, index=MONTHS)
    ms = pd.DataFrame({"dir": m_dirs}, index=MONTHS, dtype=float)
    return {"week": (wb, ws), "month": (mb, ms)}


@pytest.fixture(autouse=True)
def cutover_open(monkeypatch):
    monkeypatch.setattr(stc, "BB_TAKEBACK_CUTOVER_DATE", "2000-01-01")


def wk(i):
    return WEEKS[i]


def crash_series(crash_at=26, recover_at=None, low=70.0):
    c = base_closes()
    for i in range(crash_at, 52):
        c[i] = low
    if recover_at is not None:
        for i in range(recover_at, 52):
            c[i] = 100.0
    return c


def test_crash_week_has_z_below_trigger():
    z = stc.weekly_z(pd.Series(crash_series(), index=WEEKS))
    assert z["z"].iloc[26] <= -stc.BB_K


@pytest.mark.parametrize("w,m,trend", [(0, 1, 30), (1, 1, 100), (1, 0, 70), (0, 0, 0)])
def test_trigger_only_when_trend_is_30(w, m, trend):
    f = make_frames(crash_series(), [w] * 52, [m] * 12)
    tb = stc.takeback_asof(f, wk(26))
    assert tb["trend"] == trend
    assert tb["active"] is (trend == 30)
    assert tb["level"] == (50 if trend == 30 else trend)


def test_active_from_trigger_week_and_stays_until_recovery():
    f = make_frames(crash_series(recover_at=40), [0] * 52, [1] * 12)
    assert stc.takeback_asof(f, wk(25))["active"] is False
    a = stc.takeback_asof(f, wk(26))
    assert a["active"] and a["level"] == 50 and a["start"] == str(wk(26).date()) and a["trigger_z"] <= -2.5
    # 沒有時間上限、沒有價格停損：一路抱到價格回到均線
    assert stc.takeback_asof(f, wk(39))["active"] is True


def test_ends_when_weekly_z_back_to_zero():
    f = make_frames(crash_series(recover_at=40), [0] * 52, [1] * 12)
    t = stc.takeback_table(f)
    assert stc.weekly_z(f["week"][0]["close"])["z"].iloc[40] >= 0
    end = stc.takeback_asof(f, wk(40))
    assert end["active"] is False and end["level"] == 30           # 回到趨勢水位 30
    assert t.loc[stc.last_weekday(wk(40)), "ended"] == "回到 20 週均線"


def test_ends_when_weekly_flips_bull():
    w = [0] * 52
    for i in range(30, 52):
        w[i] = 1
    f = make_frames(crash_series(), w, [1] * 12)       # 價格一直沒回均線，但週線翻多
    assert stc.takeback_asof(f, wk(29))["active"] is True
    r = stc.takeback_asof(f, wk(30))
    assert r["trend"] == 100 and r["active"] is False and r["level"] == 100


def test_ends_when_monthly_flips_bear():
    m = [1] * 12
    for i in range(7, 12):       # 8 月底（2026-08-31）起月線翻空；crash 在 2026-07-03 之後
        m[i] = 0
    f = make_frames(crash_series(), [0] * 52, m)
    assert stc.takeback_asof(f, pd.Timestamp("2026-08-28"))["active"] is True
    r = stc.takeback_asof(f, pd.Timestamp("2026-08-31"))
    assert r["trend"] == 0 and r["active"] is False and r["level"] == 0


def test_no_retrigger_until_z_above_minus_one():
    # 26 週崩跌觸發；28 週週線翻多（結束，價格仍低）；30 週又翻空，價格仍低（z 還沒回到 −1 以上）→ 不再觸發
    w = [0] * 52
    for i in (28, 29):
        w[i] = 1
    f = make_frames(crash_series(low=70.0), w, [1] * 12)
    assert stc.takeback_asof(f, wk(27))["active"] is True
    assert stc.takeback_asof(f, wk(28))["active"] is False
    r = stc.takeback_asof(f, wk(30))
    assert r["trend"] == 30 and r["active"] is False and r["level"] == 30 and r["z"] <= -1.0
    assert stc.takeback_asof(f, wk(45))["active"] is False


def test_retrigger_after_z_recovers_above_minus_one():
    c = base_closes()
    for i in range(26, 30):
        c[i] = 70.0
    for i in range(30, 38):
        c[i] = 100.0              # 回到均線：結束，且 z > −1 重新武裝
    for i in range(38, 52):
        c[i] = 30.0               # 第二次崩跌
    f = make_frames(c, [0] * 52, [1] * 12)
    z = stc.weekly_z(pd.Series(c, index=WEEKS))["z"]
    assert z.iloc[30] >= 0 and z.iloc[38] <= -2.5
    assert stc.takeback_asof(f, wk(30))["active"] is False
    r = stc.takeback_asof(f, wk(38))
    assert r["active"] is True and r["start"] == str(wk(38).date())


def test_cutover_gating_before_equals_trend(monkeypatch):
    monkeypatch.setattr(stc, "BB_TAKEBACK_CUTOVER_DATE", str(stc.last_weekday(wk(30)).date()))
    f = make_frames(crash_series(), [0] * 52, [1] * 12)
    before = stc.takeback_asof(f, wk(29))
    assert before["applied"] is False and before["active"] is False and before["level"] == 30
    after = stc.takeback_asof(f, wk(30))
    assert after["applied"] is True and after["active"] is True and after["level"] == 50
    idx = pd.DatetimeIndex([wk(28), wk(29), wk(30), wk(31)])
    s = stc.takeback_daily(f, idx)
    assert list(s.values) == [30, 30, 50, 50]


def test_daily_fills_between_weekly_completions():
    f = make_frames(crash_series(recover_at=40), [0] * 52, [1] * 12)
    idx = pd.bdate_range(wk(25) + pd.Timedelta(days=1), wk(41))       # 逐個交易日
    s = stc.takeback_daily(f, idx)
    assert s[wk(26) - pd.Timedelta(days=1)] == 30                      # 崩跌那週週五收盤前還是 30
    assert s[wk(26)] == 50 and s[wk(26) + pd.Timedelta(days=3)] == 50
    assert s[wk(39)] == 50 and s[wk(40)] == 30
