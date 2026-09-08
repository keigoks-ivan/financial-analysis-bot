#!/usr/bin/env python3
"""測試 `scripts/build_live_scoreboard.py` 的 `build_combined_twd`（F3 修法）。

LIVE_LONGTRACK.md 致命 #6：美台合併 NAV 的聯集日曆會漏掉「休市後恢復交易」那個
市場的整段報酬——原本 `prev_d` 每個聯集日期都往前推進，若某市場當天沒有紀錄
（例如台股開市、美股休市），下一個該市場真正交易日回頭查 `us_by_date[prev_d]`
會落空，從上一個真正交易日到恢復日的報酬整段被計為 0。修法：改成各市場各自
保存「上一個有新資料的 NAV」，只在該市場有新資料時才更新報酬與該值。

本測試建構一組合成資料（不打網路，monkeypatch `fetch_usdtwd_series`／
`px_at_or_before` 用固定匯率，隔絕匯率變動干擾）：
- 2026-01-05：美台皆交易（inception，兩腿 nav=100）
- 2026-01-06：台股交易（100→102）、美股休市（無紀錄）
- 2026-01-07：美台皆交易（美股 100→105＝從 01-05 起 +5%，台股 102→103）

若沒有修 F3，美股在 01-07 的「上一日」查的是 01-06（美股當天沒紀錄），
`us_by_date.get(prev_d)` 為 None，整段 +5% 報酬會被吃成 0；修法後美股的
"上一個有效值" 仍是 01-05 的 100，01-07 能正確算出 +5%。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import build_live_scoreboard as m  # noqa: E402


FX_FLAT = {"2026-01-05": 32.0, "2026-01-06": 32.0, "2026-01-07": 32.0}


def _mkt(inception, nav_rows):
    return {"inception": inception, "nav_sys": nav_rows}


def test_combined_twd_carries_return_across_one_sided_holiday(monkeypatch):
    monkeypatch.setattr(m, "fetch_usdtwd_series", lambda: dict(FX_FLAT))

    mkt_us = _mkt("2026-01-05", [
        {"date": "2026-01-05", "nav": 100.0},
        # 2026-01-06：美股休市，state.json 的 history_us 當天沒有 live 紀錄，
        # 所以 nav_sys 也沒有這一天——這正是聯集日曆會出現「一側缺當日」的成因。
        {"date": "2026-01-07", "nav": 105.0},   # 對 2026-01-05 是 +5%
    ])
    mkt_tw = _mkt("2026-01-05", [
        {"date": "2026-01-05", "nav": 100.0},
        {"date": "2026-01-06", "nav": 102.0},   # 對 2026-01-05 是 +2%
        {"date": "2026-01-07", "nav": 103.0},   # 對 01-06 是 +0.9804%
    ])

    gaps, judgment_calls = [], []
    result = m.build_combined_twd(mkt_us, mkt_tw, gaps, judgment_calls)
    assert result is not None
    series = {r["date"]: r["nav"] for r in result["nav_series"]}

    assert series["2026-01-05"] == 100.0

    # 01-06：只有台股動、美股 0（正確——美股當天本來就沒交易，不是缺口）。
    # 50*1 + 50*1.02 = 101。
    assert series["2026-01-06"] == pytest.approx(101.0, abs=1e-6)

    # 01-07：美股從「上一個真正有效值」(01-05 的 100) 算到 105 → +5%，
    # 不是從查無資料的 01-06 算（那樣會變成 0%）。
    # us_val = 50*1.05 = 52.5；tw_val = 51*(103/102) = 51.5；nav_pre = 104.0
    # （01-07 是最後一天＝月末再平衡，7bps 換手成本 <0.001，可忽略）。
    assert series["2026-01-07"] == pytest.approx(104.0, abs=0.01)
    # 修法前的錯誤行為會把 01-07 美股報酬記為 0（因為 us_by_date 查無
    # prev_d='2026-01-06'），nav 會停在 ~101 附近；用一個寬鬆下界防止回歸。
    assert series["2026-01-07"] > 103.5


def test_combined_twd_carries_return_across_reverse_holiday(monkeypatch):
    """反向：美股開市、台股休市那天，恢復交易後台股報酬也不能消失。"""
    monkeypatch.setattr(m, "fetch_usdtwd_series", lambda: dict(FX_FLAT))

    mkt_us = _mkt("2026-01-05", [
        {"date": "2026-01-05", "nav": 100.0},
        {"date": "2026-01-06", "nav": 101.0},
        {"date": "2026-01-07", "nav": 102.0},
    ])
    mkt_tw = _mkt("2026-01-05", [
        {"date": "2026-01-05", "nav": 100.0},
        # 2026-01-06：台股休市，無紀錄。
        {"date": "2026-01-07", "nav": 110.0},   # 對 2026-01-05 是 +10%
    ])

    gaps, judgment_calls = [], []
    result = m.build_combined_twd(mkt_us, mkt_tw, gaps, judgment_calls)
    series = {r["date"]: r["nav"] for r in result["nav_series"]}

    # 01-07：台股從 01-05 的 100 算到 110 → +10%，不是從查無資料的 01-06 算。
    # us_val = 50*(102/100)=51；tw_val=50*1.10=55；nav_pre=106。
    assert series["2026-01-07"] == pytest.approx(106.0, abs=0.01)
    assert series["2026-01-07"] > 104.0
