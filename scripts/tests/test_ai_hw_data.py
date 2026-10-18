"""docs/ideas/data/ai-hardware-cycle/data.py 的測試：data.json 必要欄位、圖 7a 十檔、日期格式、
52 週均線與距離算法、抓不到時沿用上一版並標 stale。全程離線，不連 yfinance／History of Market。

python3.12 -m pytest scripts/tests/test_ai_hw_data.py -q
"""
from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[2]
DATA_PY = REPO / "docs" / "ideas" / "data" / "ai-hardware-cycle" / "data.py"
DATA_JSON = DATA_PY.with_name("data.json")

_spec = importlib.util.spec_from_file_location("ai_hw_data", DATA_PY)
ah = importlib.util.module_from_spec(_spec)
_dwb, sys.dont_write_bytecode = sys.dont_write_bytecode, True      # 不在 docs/ 底下留 __pycache__
_spec.loader.exec_module(ah)
sys.dont_write_bytecode = _dwb

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SYMBOLS = [s for s, _ in ah.REL_TICKERS]


def fake_prices(last="2026-10-16", missing=(), nan_last=()):
    """合成價格：2025-06-02 到 last 的交易日，每檔緩慢上升；missing 整欄拿掉，nan_last 最後一天缺值。"""
    idx = pd.bdate_range("2025-06-02", last)
    df = pd.DataFrame({s: 100.0 + np.arange(len(idx)) * (0.1 + 0.01 * i) for i, s in enumerate(SYMBOLS)}, index=idx)
    df = df.drop(columns=list(missing))
    for s in nan_last:
        df.loc[df.index[-1], s] = np.nan
    return df


@pytest.fixture(scope="module")
def data():
    return json.loads(DATA_JSON.read_text(encoding="utf-8"))


# ───────────────────────── data.json 內容 ─────────────────────────
def test_top_level_fields(data):
    for k in ("generated", "stale", "drawdown", "fpe", "nvidia", "ai_revenue", "exposure", "scenarios",
              "rel", "ratio", "latest"):
        assert k in data, k
    assert DATE_RE.match(data["generated"])
    assert isinstance(data["stale"], bool)


def test_rel_has_all_ten_tickers_sorted_desc(data):
    items = data["rel"]["items"]
    assert sorted(i["ticker"] for i in items) == sorted(SYMBOLS)
    assert len(items) == 10
    pcts = [i["pct"] for i in items]
    assert pcts == sorted(pcts, reverse=True)
    assert data["rel"]["base_date"] == "2026-06-22"
    assert DATE_RE.match(data["rel"]["last_date"])
    for i in items:
        assert {"ticker", "label", "pct", "base_close", "last_close"} <= set(i)


def test_ratio_series(data):
    rt = data["ratio"]
    assert len(rt["dates"]) == len(rt["values"]) > 100
    assert all(DATE_RE.match(d) for d in rt["dates"])
    assert rt["dates"] == sorted(rt["dates"])
    assert rt["dates"][0] >= "2026-01-02"
    assert rt["values"][rt["dates"].index("2026-06-22")] == 100.0      # 基準日＝100
    assert DATE_RE.match(rt["event"]["date"])


def test_latest_fields(data):
    L = data["latest"]
    assert DATE_RE.match(L["date"])
    for k in ("smh", "sox", "qqq"):
        assert {"close", "ma52", "drop_pct"} <= set(L[k]), k
        # 距離＝還要跌多少碰到均線，與收盤、均線自洽（四捨五入 0.1）
        want = (1 - L[k]["ma52"] / L[k]["close"]) * 100
        assert abs(want - L[k]["drop_pct"]) < 0.06, k
    assert L["nvda"]["close"] > 0


def test_now_path_reaches_latest_date(data):
    now = [p for p in data["drawdown"]["paths"] if p["group"] == "now"][0]
    assert now["peak"] == "2026-06-22"
    assert now["last_date"] == data["drawdown"]["last_close_date"]
    assert len(now["path"]) == now["days"] + 1


def test_date_columns_are_consistent(data):
    """同一次抓價算出的三塊，資料日一致（沒有 stale 時）。"""
    if data["stale"]:
        pytest.skip("有 stale 區塊")
    assert data["rel"]["last_date"] == data["ratio"]["last_date"] == data["latest"]["date"]


# ───────────────────────── 算法 ─────────────────────────
def test_calc_latest_ma52_and_drop():
    df = fake_prices()
    L = ah.calc_latest(df)
    s = df["SMH"]
    w = s.resample("W-FRI").last().dropna()
    assert L["smh"]["ma52"] == round(float(w.iloc[-52:].mean()), 2)
    assert L["smh"]["close"] == round(float(s.iloc[-1]), 2)
    assert L["date"] == "2026-10-16"


def test_calc_latest_needs_52_weeks():
    with pytest.raises(ValueError):
        ah.calc_latest(fake_prices().loc["2026-03-01":])


def test_calc_rel_matches_manual():
    df = fake_prices()
    rel = ah.calc_rel(df)
    nv = [i for i in rel["items"] if i["ticker"] == "NVDA"][0]
    want = (df["NVDA"].iloc[-1] / df.loc["2026-06-22", "NVDA"] - 1) * 100
    assert nv["pct"] == round(want, 1)


def test_last_day_with_missing_quote_falls_back_one_day():
    """最新一天有一檔沒收盤價：整組退到前一個共同交易日，不用缺資料的半天。"""
    df = fake_prices(nan_last=("CRWV",))
    assert ah.calc_rel(df)["last_date"] == "2026-10-15"
    assert ah.calc_latest(df)["date"] == "2026-10-16"       # latest 只需要 SMH／^SOX／QQQ／NVDA


def test_missing_ticker_raises():
    with pytest.raises(ValueError):
        ah.calc_rel(fake_prices(missing=("CRWV",)))


# ───────────────────────── stale 邏輯 ─────────────────────────
@pytest.fixture()
def old(data):
    return copy.deepcopy(data)


def _no_csv(monkeypatch):
    monkeypatch.setattr(ah, "SOX_CSV", Path("/nonexistent/SOX.csv"))     # 模擬 CI：沒有 v7


def test_fresh_fetch_clears_stale(monkeypatch, old):
    _no_csv(monkeypatch)
    old["rel"]["stale"] = True
    out = ah.build([], old, fetch=lambda syms: fake_prices())
    assert out["rel"]["stale"] is False and out["ratio"]["stale"] is False and out["latest"]["stale"] is False
    assert "stale" not in out["drawdown"]
    assert out["stale"] is False


def test_fetch_failure_keeps_old_and_marks_stale(monkeypatch, old):
    _no_csv(monkeypatch)

    def boom(syms):
        raise RuntimeError("yfinance down")

    out = ah.build([], old, fetch=boom)
    for k in ("rel", "ratio", "latest"):
        assert out[k]["stale"] is True
        assert {x: y for x, y in out[k].items() if x != "stale"} == {x: y for x, y in old[k].items() if x != "stale"}
    assert out["drawdown"]["stale"] is True
    assert out["drawdown"]["paths"] == old["drawdown"]["paths"]
    assert out["stale"] is True
    assert out["fpe"] == old["fpe"]               # 沒帶 --fpe：本益比一律沿用


def test_one_missing_ticker_stales_only_dependent_blocks(monkeypatch, old):
    """少 CRWV：圖 7a 沿用舊值，7b 與 latest 不需要它，照常更新。"""
    _no_csv(monkeypatch)
    out = ah.build([], old, fetch=lambda syms: fake_prices(missing=("CRWV",)))
    assert out["rel"]["stale"] is True
    assert out["ratio"]["stale"] is False
    assert out["latest"]["stale"] is False
    assert out["stale"] is True


def test_date_never_goes_backwards(monkeypatch, old):
    _no_csv(monkeypatch)
    out = ah.build([], old, fetch=lambda syms: fake_prices(last="2026-10-09"))
    assert out["rel"]["stale"] is True and out["rel"]["last_date"] == old["rel"]["last_date"]
    assert out["latest"]["stale"] is True and out["latest"]["date"] == old["latest"]["date"]


def test_first_run_without_old_block_omits_it(monkeypatch, old):
    _no_csv(monkeypatch)
    for k in ("rel", "ratio", "latest"):
        old.pop(k)

    def boom(syms):
        raise RuntimeError("down")

    out = ah.build([], old, fetch=boom)
    assert all(k not in out for k in ("rel", "ratio", "latest"))
    assert out["stale"] is True


def test_fpe_failure_falls_back_to_old_and_marks_stale(monkeypatch, old):
    monkeypatch.setattr(ah, "load_fpe", lambda: (None, "none"))
    monkeypatch.setattr(ah, "OUT", DATA_JSON)
    got = ah.forward_pe()
    assert got["stale"] is True
    assert got["weekly"] == old["fpe"]["weekly"]
