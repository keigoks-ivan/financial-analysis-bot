"""2026-09-29 MRK：情境樹 yield_pct.dividend 若判斷者查無資料留 null，
dd_scenario.py 把 null 當 0 算（見 aeb3cdb8c），配息股含息報酬因此被低估。

比照 price_at_dd／decision_inputs.ma 的「程式擁有的欄」慣例修復，三段接線：
1. dd_numbers_extra.py::compute_dividend_yield_ttm 機械算出 trailing 12 個月
   殖利率（近 365 天股息加總 ÷ price_at_dd × 100）。
2. dd_facts.py::_valuation_facts 把它落成 f_dividend_yield_ttm 事實（有值才落）。
3. dd_project.py::scenario_input_from_v19 用這個事實覆寫判斷者填的
   scenario_inputs.yield_pct.dividend（net_buyback 仍交判斷者，不動）。

本檔覆蓋：配息股（真算出殖利率）、非配息股（0.0，非 null）、查不到資料的 null
案例、以及覆寫本身（有 fact 就覆寫／無 fact 沿用判斷者原答案）。全程無網路：
yfinance 一律經 monkeypatch `dd_numbers_extra._lazy_imports` 假冒。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

import pandas as pd
import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import dd_facts  # noqa: E402
import dd_numbers_extra as dne  # noqa: E402
import dd_project  # noqa: E402


# ---------------------------------------------------------------------------
# compute_dividend_yield_ttm（dd_numbers_extra.py）
# ---------------------------------------------------------------------------

class _FakeTicker:
    def __init__(self, dividends=None, raise_on_dividends=False):
        self._dividends = dividends
        self._raise = raise_on_dividends

    @property
    def dividends(self):
        if self._raise:
            raise RuntimeError("simulated yfinance failure")
        return self._dividends


class _FakeYF:
    def __init__(self, ticker_map):
        self._map = ticker_map

    def Ticker(self, ticker):
        return self._map[ticker]


def _patch_yf(monkeypatch, ticker_map):
    import numpy as np
    monkeypatch.setattr(dne, "_lazy_imports", lambda: (np, pd, _FakeYF(ticker_map)))


def test_dividend_yield_payer_computes_trailing_pct(monkeypatch):
    """配息股：近 365 天四筆股息加總 ÷ price_at_dd。"""
    idx = pd.to_datetime(["2026-01-15", "2026-04-15", "2026-07-15", "2026-09-15"])
    divs = pd.Series([0.5, 0.5, 0.5, 0.5], index=idx)
    _patch_yf(monkeypatch, {"MRK": _FakeTicker(divs)})
    out = dne.compute_dividend_yield_ttm("MRK", datetime(2026, 9, 29), 100.0)
    assert out["value_pct"] == pytest.approx(2.0)
    assert out["n_payments"] == 4
    assert out["note"] is None


def test_dividend_yield_non_payer_is_zero_not_null(monkeypatch):
    """非配息股：0.0（真實的『沒有』），不是 null——與『查不到資料』的 null
    案例分開，才不會被下游誤判成缺資料。"""
    empty = pd.Series([], dtype=float)
    _patch_yf(monkeypatch, {"GOOG": _FakeTicker(empty)})
    out = dne.compute_dividend_yield_ttm("GOOG", datetime(2026, 9, 29), 200.0)
    assert out["value_pct"] == 0.0
    assert out["note"]


def test_dividend_yield_missing_price_is_null():
    """缺 price_at_dd：null＋note，不猜、不觸網（函式應在算之前就回傳）。"""
    out = dne.compute_dividend_yield_ttm("MRK", datetime(2026, 9, 29), None)
    assert out["value_pct"] is None
    assert out["note"]


def test_dividend_yield_fetch_failure_is_null_not_fabricated(monkeypatch):
    """yfinance 查詢失敗：null＋note，不得捏造一個值頂替。"""
    _patch_yf(monkeypatch, {"MRK": _FakeTicker(raise_on_dividends=True)})
    out = dne.compute_dividend_yield_ttm("MRK", datetime(2026, 9, 29), 148.69)
    assert out["value_pct"] is None
    assert out["note"]


# ---------------------------------------------------------------------------
# dd_facts.py：numbers.dividend_yield_ttm → f_dividend_yield_ttm
# ---------------------------------------------------------------------------

def test_facts_emit_dividend_yield_fact_when_value_present():
    numbers = {"dividend_yield_ttm": {"value_pct": 2.287, "as_of": "2026-09-29",
                                       "method": "m", "note": None}}
    buckets = {k: {"facts": []} for k in dd_facts.QUESTION_KEYS}
    dd_facts._valuation_facts(numbers, buckets)
    ids = {f["id"]: f for f in buckets["q5_valuation"]["facts"]}
    assert "f_dividend_yield_ttm" in ids
    assert ids["f_dividend_yield_ttm"]["value"] == 2.287


def test_facts_skip_dividend_yield_fact_when_value_null():
    """查不到資料時 value_pct=None——不落沒有值的事實，也不假裝有資料。"""
    numbers = {"dividend_yield_ttm": {"value_pct": None, "as_of": "2026-09-29",
                                       "note": "股息資料擷取失敗：x"}}
    buckets = {k: {"facts": []} for k in dd_facts.QUESTION_KEYS}
    dd_facts._valuation_facts(numbers, buckets)
    ids = {f["id"] for f in buckets["q5_valuation"]["facts"]}
    assert "f_dividend_yield_ttm" not in ids


# ---------------------------------------------------------------------------
# dd_project.py：scenario_input_from_v19 覆寫 yield_pct.dividend
# ---------------------------------------------------------------------------

def _minimal_raw(dividend_from_judge):
    return {
        "meta": {"ticker": "MRK", "date": "2026-09-29"},
        "scenario_inputs": {
            "start": {"eps": 1.0, "pe": 10.0},
            "yield_pct": {"dividend": dividend_from_judge, "net_buyback": 0.5},
            "terminal_label": "FY2031E",
        },
        "eps_meta": {"base_eps_path": {}},
    }


def _facts_with_dividend(value):
    return {"questions": {"q5_valuation": {"facts": [
        {"id": "f_dividend_yield_ttm", "label": "trailing 股息殖利率", "value": value,
         "period": "2026-09-29", "unit": "%", "basis": "b", "kind": "realized",
         "source": {"type": "evidence_numbers", "ref": "x"}},
    ]}}}


def test_scenario_input_overwrites_judge_null_dividend_with_program_fact():
    """MRK 教訓的直接回歸：判斷者留 null、程式算得出來 → 用程式值，
    net_buyback 仍是判斷者填的，不被動到。"""
    raw = _minimal_raw(dividend_from_judge=None)
    facts = _facts_with_dividend(2.287)
    out = dd_project.scenario_input_from_v19(raw, facts)
    assert out["yield_pct"]["dividend"] == 2.287
    assert out["yield_pct"]["net_buyback"] == 0.5


def test_scenario_input_overwrites_judge_filled_dividend_with_program_fact():
    """就算判斷者填了值，有程式事實就覆寫——比照 decision_inputs.ma 的覆寫慣例，
    不是『judge 沒填才補』。"""
    raw = _minimal_raw(dividend_from_judge=99.0)
    facts = _facts_with_dividend(2.287)
    out = dd_project.scenario_input_from_v19(raw, facts)
    assert out["yield_pct"]["dividend"] == 2.287


def test_scenario_input_leaves_judge_dividend_when_fact_missing():
    """fact 缺（程式沒算出來）：沿用判斷者原答案，不補 0、不覆寫成 null。"""
    facts_empty = {"questions": {}}

    raw_null = _minimal_raw(dividend_from_judge=None)
    out_null = dd_project.scenario_input_from_v19(raw_null, facts_empty)
    assert out_null["yield_pct"]["dividend"] is None

    raw_filled = _minimal_raw(dividend_from_judge=1.5)
    out_filled = dd_project.scenario_input_from_v19(raw_filled, facts_empty)
    assert out_filled["yield_pct"]["dividend"] == 1.5
