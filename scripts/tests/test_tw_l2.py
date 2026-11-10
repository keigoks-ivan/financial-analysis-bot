"""台股正二（supertrend_core.l2_table／l2_asof／l2_daily）的合成價格單元測試。

週線方向直接手設，只測水位規則：週線多 100、週線空 0；週線空時週收盤 z ≤ −2.5 → 30；週收盤 z ≥ 0 或週線翻多就結束；
結束後 z 要先回到 −1 以上才能再觸發；不看月線；資料日 >= TW_L2_CUTOVER_DATE 才持有，0050／2330 權重同日由各 0.5 改各 0.4。
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import supertrend_core as stc  # noqa: E402

WEEKS = pd.date_range("2026-01-02", periods=52, freq="W-FRI")
MONTHS = pd.date_range("2026-01-31", periods=12, freq="ME")


def base_closes():
    return [100.0 + (0.5 if i % 2 else 0.0) for i in range(52)]


def frames(closes, w_dirs, m_dirs=None):
    wb = pd.DataFrame({"close": closes}, index=WEEKS)
    ws = pd.DataFrame({"dir": w_dirs}, index=WEEKS, dtype=float)
    mb = pd.DataFrame({"close": [100.0] * 12}, index=MONTHS)
    ms = pd.DataFrame({"dir": m_dirs if m_dirs is not None else [1] * 12}, index=MONTHS, dtype=float)
    return {"week": (wb, ws), "month": (mb, ms)}


def levels(fr):
    return stc.l2_table(fr)["level"].tolist()


def test_trend_only_up_100_down_0():
    lv = levels(frames(base_closes(), [1] * 30 + [0] * 22))
    assert lv[29] == 100 and lv[30] == 0


def test_takeback_starts_at_30_and_ends_at_ma():
    c = base_closes()
    c[30], c[31] = 90.0, 90.0
    c[32] = 101.0
    w = [1] * 30 + [0] * 22
    t = stc.l2_table(frames(c, w))
    assert t["z"].iloc[30] <= -2.5
    assert t["level"].tolist()[30:33] == [30, 30, 0]
    assert t["ended"].iloc[32] == "回到 20 週均線"


def test_flip_up_ends_takeback():
    c = base_closes()
    c[30], c[31] = 90.0, 90.0
    w = [1] * 30 + [0, 1] + [1] * 20
    t = stc.l2_table(frames(c, w))
    assert t["level"].iloc[30] == 30 and t["level"].iloc[31] == 100
    assert t["ended"].iloc[31] == "週線翻多"


def test_needs_rearm_above_minus_one():
    c = base_closes()
    c[30], c[31], c[32] = 90.0, 90.0, 90.0      # 第 31 週週線翻多結束時 z 還很低，第 32 週翻空不能馬上再接回
    c[33] = 101.0                               # z 回到 −1 以上，解鎖
    c[34] = 80.0                                # 再跌破就可以接回
    w = [1] * 30 + [0, 1, 0, 0, 0] + [0] * 17
    t = stc.l2_table(frames(c, w))
    assert t["level"].iloc[30] == 30
    assert t["level"].iloc[32] == 0
    assert t["z"].iloc[34] <= -2.5 and t["level"].iloc[34] == 30


def test_monthly_is_ignored():
    c = base_closes()
    c[30] = 90.0
    w = [1] * 30 + [0] * 22
    assert levels(frames(c, w, [1] * 12)) == levels(frames(c, w, [0] * 12))


def test_asof_daily_and_weights_cutover():
    c = base_closes()
    c[30] = 90.0
    fr = frames(c, [1] * 30 + [0] * 22)
    d_trig = WEEKS[30]
    a = stc.l2_asof(fr, d_trig)
    assert a["level"] == 30 and a["active"] and a["applied"] == (str(d_trig.date()) >= stc.TW_L2_CUTOVER_DATE)
    idx = pd.DatetimeIndex([pd.Timestamp("2026-11-09"), pd.Timestamp(stc.TW_L2_CUTOVER_DATE)])
    v = stc.l2_daily(fr, idx)
    assert v.iloc[0] == 0
    before, after = stc.leg_weights("2026-11-09"), stc.leg_weights(stc.TW_L2_CUTOVER_DATE)
    assert before["0050.TW"] == before["2330.TW"] == 0.5
    assert after["0050.TW"] == after["2330.TW"] == 0.4
    assert after["QQQ"] == 0.7 and after["SMH"] == 0.3
