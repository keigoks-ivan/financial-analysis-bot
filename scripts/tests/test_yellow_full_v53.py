"""v5.3（2026-10-18 持有人拍板）：美股看板黃燈倉位 0.5 → 1.0，台股席位／十倍股頁維持半倉。

依據 v7-backtest docs/SeatSizing_Results.md 與 docs/SeatSizing_Results_v2.md；登記判準形式上
未過，是持有人依兩次回測決定改。本檔驗：
  - grp.timing_lamp(s, yellow_full=True) 黃燈 size 1.0、label「🟡 接近」；橘燈仍 0.5
  - 預設呼叫（不傳參數）與舊版輸出逐位元相同（黃 0.5／「🟡 半倉」）
  - build_arena.row_dict 預設＝半倉（台股 build_seats_tw.tw_row、十倍股 build_tenbagger 走這條）；
    只有傳 yellow_full=True（build_arena.main()）才滿倉
純手工輸入，不讀磁碟資料、不連網。
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from engine import build_arena as ba  # noqa: E402
from engine import grp  # noqa: E402
import build_seats_tw as tw  # noqa: E402


def _lamp_input(above_w52=True, dist_ath=-7.0, vs200=1.0, mom=None):
    return {"ma": {"above_w52": above_w52, "dist_ath_pct": dist_ath, "mom_12_1_pct": mom},
            "timing": {"vs_200ma_pct": vs200}}


# ── timing_lamp 開關 ─────────────────────────────────────────────────────────

def test_yellow_full_makes_yellow_size_one_and_label_neutral():
    lamp = grp.timing_lamp(_lamp_input(dist_ath=-7.0), yellow_full=True)
    assert lamp["code"] == "yellow"
    assert lamp["size"] == 1.0
    assert lamp["label"] == "🟡 接近"
    assert "半倉" not in lamp["label"]


def test_yellow_full_boundaries_still_yellow():
    for d in (-10.0, -3.01):
        lamp = grp.timing_lamp(_lamp_input(dist_ath=d), yellow_full=True)
        assert (lamp["code"], lamp["size"]) == ("yellow", 1.0)


def test_yellow_full_keeps_hot_half():
    lamp = grp.timing_lamp(_lamp_input(dist_ath=-1.0, vs200=1.0, mom=200.0), yellow_full=True)
    assert (lamp["code"], lamp["size"]) == ("hot", 0.5)


def test_yellow_full_does_not_touch_green_red_out():
    g = grp.timing_lamp(_lamp_input(dist_ath=-1.0), yellow_full=True)
    r = grp.timing_lamp(_lamp_input(dist_ath=-15.0), yellow_full=True)
    r2 = grp.timing_lamp(_lamp_input(dist_ath=-1.0, vs200=-2.0), yellow_full=True)
    o = grp.timing_lamp(_lamp_input(above_w52=False), yellow_full=True)
    assert (g["code"], g["size"]) == ("green", 1.0)
    assert (r["code"], r["size"]) == ("red", 0.0)
    assert (r2["code"], r2["size"]) == ("red", 0.0)
    assert (o["code"], o["size"]) == ("out", 0.0)


def test_yellow_missing_data_fallback_stays_half_even_when_full():
    lamp = grp.timing_lamp(_lamp_input(dist_ath=None, vs200=None), yellow_full=True)
    assert (lamp["code"], lamp["size"]) == ("yellow", 0.5)
    assert grp.lamp_action(lamp, True) == "半倉"


def test_default_is_bit_identical_to_old_behaviour():
    """預設（不傳參數）＝舊版：黃 0.5「🟡 半倉」、資料缺 fallback 同。其餘燈號兩種模式一致。"""
    y = grp.timing_lamp(_lamp_input(dist_ath=-7.0))
    assert y == {"code": "yellow", "label": "🟡 半倉", "size": 0.5, "trigger": None,
                 "why": "距歷史新高 -7.0%（接近新高，未到突破帶）、vs 200 日線 +1.0%"}
    assert y == grp.timing_lamp(_lamp_input(dist_ath=-7.0), yellow_full=False)
    fb = grp.timing_lamp(_lamp_input(dist_ath=None, vs200=None))
    assert (fb["label"], fb["size"]) == ("🟡 半倉", 0.5)
    for kw in (dict(dist_ath=-1.0), dict(dist_ath=-15.0), dict(dist_ath=-1.0, vs200=-2.0),
               dict(above_w52=False), dict(dist_ath=-1.0, mom=200.0)):
        assert grp.timing_lamp(_lamp_input(**kw)) == grp.timing_lamp(_lamp_input(**kw), yellow_full=True)


def test_lamp_action_text():
    y_old = grp.timing_lamp(_lamp_input(dist_ath=-7.0))
    y_new = grp.timing_lamp(_lamp_input(dist_ath=-7.0), yellow_full=True)
    assert grp.lamp_action(y_old) == "半倉" == grp.lamp_action(y_old, False)
    assert grp.lamp_action(y_new, True) == "正常倉"
    hot = grp.timing_lamp(_lamp_input(dist_ath=-1.0, mom=200.0), yellow_full=True)
    assert grp.lamp_action(hot, True) == "半倉"
    # 全域 LAMP_ACTION 不動（台股／十倍股沿用）
    assert grp.LAMP_ACTION["yellow"] == "半倉" and grp.LAMP_ACTION["hot"] == "半倉"
    assert grp.LAMP_ACTION_V53["yellow"] == "正常倉"


# ── row_dict：預設半倉（台股／十倍股路徑），美股看板傳 True ───────────────────

def _stock(ticker="AAA", dist_ath=-7.0):
    return {
        "ticker": ticker, "dd_status": "dd", "dca_verdict": None,
        "eps_fy1_fy3_cagr_pct": 25.0,
        "eps_rev_since_earnings_pct": 20.0, "eps_rev_anchor": "earnings",
        "eps_rev_since_earnings_baseline_date": "2026-08-01",
        "roic": 20.0, "fcf": 15.0, "ocf": 20.0, "live_fpe_est": 20.0,
        "durable_5y": True, "durable_source": "koyfin-xlsx",
        "_r26": None, "_r52": None,
        "ma": {"above_w52": True, "price": 100.0, "mom_12_1_pct": 10.0, "dist_ath_pct": dist_ath},
        "timing": {"vs_200ma_pct": 5.0, "dist_52w_high_pct": -2.0},
    }


def test_row_dict_default_is_half_for_tw_and_tenbagger_paths():
    r = ba.row_dict(_stock())
    assert (r["lamp"]["code"], r["lamp"]["size"], r["lamp"]["label"]) == ("yellow", 0.5, "🟡 半倉")
    assert r["action"] == "半倉"


def test_row_dict_yellow_full_is_full_for_us_board():
    r = ba.row_dict(_stock(), yellow_full=True)
    assert (r["lamp"]["code"], r["lamp"]["size"], r["lamp"]["label"]) == ("yellow", 1.0, "🟡 接近")
    assert r["action"] == "正常倉"


def test_row_dict_yellow_full_keeps_orange_half():
    s = _stock(dist_ath=-1.0)
    s["ma"]["mom_12_1_pct"] = 200.0
    r = ba.row_dict(s, yellow_full=True)
    assert (r["lamp"]["code"], r["lamp"]["size"]) == ("hot", 0.5)
    assert r["action"] == "半倉"


def test_tw_row_still_half():
    r = tw.tw_row(_stock())
    assert (r["lamp"]["code"], r["lamp"]["size"], r["lamp"]["label"]) == ("yellow", 0.5, "🟡 半倉")
    assert r["action"] == "半倉"


def test_ascii_action_reads_size():
    assert ba._act_ascii({"code": "yellow", "size": 1.0}) == "FULL"
    assert ba._act_ascii({"code": "yellow", "size": 0.5}) == "HALF"
    assert ba._act_ascii({"code": "hot", "size": 0.5}) == "HALF"
    assert ba._act_ascii({"code": "green", "size": 1.0}) == "FULL"
    assert ba._act_ascii({"code": "red", "size": 0.0}) == "ZERO"
    assert ba._act_ascii({"code": "out", "size": 0.0}) == "-"
