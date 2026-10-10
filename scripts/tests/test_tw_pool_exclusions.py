"""台股池不列入金融保險業與興櫃 (build_dd_screener._tw_universe_entries), 2026-10-10.

Owner decision: financials leave the pool because the OCF-margin quality gate
means nothing for banks and insurers; 興櫃 names leave until they list on
TWSE/TPEx, at which point the roster's market changes and they come back.
No network.
"""
from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402
import build_dd_screener_tw_page as page  # noqa: E402

RESOLVED = {
    "2330": {"ticker": "2330.TW", "name": "台積電", "market": "TWSE", "industry": "半導體業"},
    "2891": {"ticker": "2891.TW", "name": "中信金", "market": "TWSE", "industry": "金融保險業"},
    "5274": {"ticker": "5274.TWO", "name": "信驊", "market": "TPEx", "industry": "半導體業"},
    "7924": {"ticker": "7924.TWO", "name": "TLC-KY", "market": "TPEx-emerging",
             "industry": "生技醫療業"},
    "8888": {"ticker": "8888.TWO", "name": "8888.TWO", "market": "probe", "industry": None},
}


def test_financials_and_emerging_are_left_out():
    snap = SimpleNamespace(tickers=list(RESOLVED) + ["9999"])        # 9999 unresolved
    rows = bds._tw_universe_entries(snap, RESOLVED)
    assert [r["ticker"] for r in rows] == ["2330.TW", "5274.TWO", "8888.TWO"]


def test_emerging_name_returns_once_it_lists():
    listed = dict(RESOLVED, **{"7924": dict(RESOLVED["7924"], market="TPEx")})
    rows = bds._tw_universe_entries(SimpleNamespace(tickers=["7924"]), listed)
    assert [r["ticker"] for r in rows] == ["7924.TWO"]


def test_hero_names_what_was_left_out_and_why():
    f = {"n": 78, "tpex": 21, "excluded_financial": 3, "excluded_emerging": 5}
    html = page.hero_html(f)
    assert "目前 78 檔，其中上櫃 21 檔。" in html
    assert "另有金融保險業 3 檔、興櫃 5 檔不列入。" in html
    assert "存放款與保費" in html and "轉上市或上櫃後自動列入" in html
    only_fin = page.hero_html({"n": 83, "tpex": 21, "excluded_financial": 3})
    assert "興櫃" not in only_fin
    none_out = page.hero_html({"n": 86, "tpex": 21})
    assert "不列入" not in none_out


def test_tw_pool_does_not_write_the_us_weekly_cache(monkeypatch):
    # data/weekly_cache is globbed by US readers (pipeline 回看鏡, DD base rates)
    for mode, uses in (("dd", True), ("smallcap", True), ("tw", False)):
        monkeypatch.setattr(bds, "UNIVERSE_MODE", mode)
        assert bds._ma_uses_cache() is uses
    src = Path(bds.__file__).read_text(encoding="utf-8")
    assert "compute_ma_snapshot(_yf_ticker_for_ma(t), use_cache=_ma_uses_cache())" in src
