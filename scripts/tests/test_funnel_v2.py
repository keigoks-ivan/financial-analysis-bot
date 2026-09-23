"""Unit tests for scripts/build_dd_screener.py's FunnelRank v2 (2026-09-22
逐層法) — compute_funnel_v2() and its helpers.

Design doc: notes/site-internal/root/_funnel_v2_design_20260922.md
v1 (compute_funnel_rank) is untouched and has its own test file
(test_funnel_caps.py) — this file only covers the new v2 code path.

護城河不進排序；護城河三題制已於 2026-09-22 同日放棄，不再有任何護城河
顯示欄位——`moat_questions_url`/`moat_review_due` 已從 `compute_funnel_v2()`
整個移除，不是留空。排序只剩四層：事業品質→再投資引擎→期望落差→價格。本
檔早先幾版護城河相關測試（三來源鏈／覆蓋率守門／絕對分層＋過渡開關／純顯
示連結）皆已移除，只留「moat 從不進 `FUNNEL_V2_LAYER_ORDER`」與「summary
無 moat 欄位」兩類驗證。

Hand-made synthetic populations only — no network, no cache files. Same style
as test_funnel_caps.py / test_fundamental_gates.py.

2026-09-23 additions (see knowledge/rule_ledger.md FunnelRank v2 row, same-day
follow-up entry): sort method fixed to leximin (weakest layer first — the
design doc always said this, the original implementation was fixed-order
quality→engine→gap→price); `pct_5y` dropped from the price layer; quality
layer's `fcf_ni_ratio` input capped at `FUNNEL_V2_FCF_NI_CAP`; and a new
`_target_upside_yfinance_fallback()` helper (network-free here — monkeypatched
`yf.Ticker`) for rows where Koyfin's own target_avg/last_price_local pair is
split across the ADR/local listing.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402


# ---------------------------------------------------------------------------
# _percentile_rank
# ---------------------------------------------------------------------------

def test_percentile_rank_basic_spread():
    out = bds._percentile_rank({"A": 10, "B": 20, "C": 30, "D": 40, "E": 50})
    assert out["A"] == pytest.approx(0.0)
    assert out["E"] == pytest.approx(100.0)
    assert out["C"] == pytest.approx(50.0)
    # monotonic
    assert out["A"] < out["B"] < out["C"] < out["D"] < out["E"]


def test_percentile_rank_ties_get_same_value():
    out = bds._percentile_rank({"A": 10, "B": 10, "C": 30})
    assert out["A"] == out["B"]
    assert out["A"] < out["C"]


def test_percentile_rank_invert_flips_direction():
    normal = bds._percentile_rank({"A": 10, "B": 20, "C": 30})
    inverted = bds._percentile_rank({"A": 10, "B": 20, "C": 30}, invert=True)
    assert inverted["A"] == pytest.approx(100.0 - normal["A"])
    assert inverted["A"] > inverted["C"]  # lower raw -> higher pct when inverted


def test_percentile_rank_drops_none_values():
    out = bds._percentile_rank({"A": 10, "B": None, "C": 30})
    assert "B" not in out
    assert set(out) == {"A", "C"}


def test_percentile_rank_single_value_is_neutral():
    out = bds._percentile_rank({"A": 42})
    assert out == {"A": 50.0}


def test_percentile_rank_empty():
    assert bds._percentile_rank({}) == {}


# ---------------------------------------------------------------------------
# Field-exclusion helpers
# ---------------------------------------------------------------------------

def test_incremental_roic_excluded_when_clamped():
    row = {"incremental_roic_pct": 500.0, "incremental_roic_clamped": True}
    assert bds._funnel_v2_incremental_roic(row) is None


def test_incremental_roic_excluded_on_capital_shrink_note():
    row = {"incremental_roic_pct": None, "incremental_roic_note": "資本縮減"}
    assert bds._funnel_v2_incremental_roic(row) is None


def test_incremental_roic_passes_through_when_clean():
    row = {"incremental_roic_pct": 25.5, "incremental_roic_clamped": False}
    assert bds._funnel_v2_incremental_roic(row) == 25.5


def test_growth_gap_none_when_either_missing():
    assert bds._funnel_v2_growth_gap({"implied_growth_pct": 10.0, "fund": {}}) is None
    assert bds._funnel_v2_growth_gap({"implied_growth_pct": None, "fund": {"est_eps_cagr_3y_pct": 5.0}}) is None


def test_growth_gap_computed_when_both_present():
    row = {"implied_growth_pct": 12.0, "fund": {"est_eps_cagr_3y_pct": 7.0}}
    assert bds._funnel_v2_growth_gap(row) == pytest.approx(5.0)


# ---------------------------------------------------------------------------
# compute_funnel_v2 — fixtures
# ---------------------------------------------------------------------------

def _base_row(ticker: str, **overrides) -> dict:
    """A row with every FunnelRank v2 field populated with a distinct,
    ticker-specific value so it participates in the 4 percentile layers by
    default. Tests override only the fields they care about."""
    n = overrides.pop("_n", 1)
    row = {
        "ticker": ticker,
        "roic_5y_avg_pct": 10.0 * n, "roic": 10.0 * n,
        "fcf": 10.0 * n, "fcf_ni_ratio": 1.0 + 0.1 * n,
        "fund": {"ni_margin_ltm_pct": 10.0 * n, "est_eps_cagr_3y_pct": 5.0},
        "implied_growth_pct": 5.0 * n, "incremental_roic_pct": 20.0 * n,
        "incremental_roic_clamped": False, "incremental_roic_note": None,
        "eps_fy1_fy3_cagr_pct": 10.0 * n,
        "eps_rev_3m_pct": 1.0 * n, "eps_rev_since_earnings_pct": 1.0 * n,
        "pe_vs_5y_x": 2.0 - 0.1 * n, "live_peg": 2.0 - 0.1 * n,
        "target_upside_pct": 5.0 * n, "pct_5y": 100.0 - 10.0 * n,
        "quality_veto_level": "維持", "decline_signal_light": "🟢",
        "veto_all_downgrade": False,
    }
    row.update(overrides)
    return row


# ---------------------------------------------------------------------------
# compute_funnel_v2 — moat is fully removed, never enters ranking or output
# ---------------------------------------------------------------------------

def test_moat_never_in_layer_order():
    assert "moat" not in bds.FUNNEL_V2_LAYER_ORDER
    assert list(bds.FUNNEL_V2_LAYER_ORDER) == ["quality", "engine", "gap", "price"]


def test_profile_and_tiers_are_four_elements():
    rows = [_base_row("AAA", _n=1), _base_row("BBB", _n=2)]
    bds.compute_funnel_v2(rows)
    aaa = next(r for r in rows if r["ticker"] == "AAA")
    assert len(aaa["funnel_v2_profile"]) == 4
    assert len(aaa["funnel_v2_tiers"]) == 4


def test_rows_have_no_moat_display_fields():
    """護城河三題制已於 2026-09-22 放棄——compute_funnel_v2() 不應該再替每
    一列寫入 `moat_questions_url`／`moat_review_due` 這兩個舊的純顯示欄位，
    連 key 都不該出現（不是寫成 None）。"""
    rows = [_base_row("AAA", _n=1), _base_row("BBB", _n=2)]
    bds.compute_funnel_v2(rows)
    for r in rows:
        assert "moat_questions_url" not in r
        assert "moat_review_due" not in r


def test_summary_has_no_moat_fields():
    """summary／layer_config 不再有任何 moat_* 鍵——徹底刪除，不是留空。"""
    rows = [_base_row("AAA", _n=1), _base_row("BBB", _n=2)]
    summary = bds.compute_funnel_v2(rows)
    assert not any(k.startswith("moat") for k in summary)
    assert not any(k.startswith("moat") for k in summary["layer_config"])


# ---------------------------------------------------------------------------
# compute_funnel_v2 — veto / insufficient-data / ranking
# ---------------------------------------------------------------------------

def test_hard_veto_quality_reject_sinks_and_records_reason():
    rows = [_base_row("AAA", _n=5, quality_veto_level="拒絕"), _base_row("BBB", _n=1)]
    bds.compute_funnel_v2(rows)
    aaa = next(r for r in rows if r["ticker"] == "AAA")
    assert aaa["funnel_v2_rank"] is None
    assert "quality_veto_level=拒絕" in aaa["funnel_v2_veto"]
    assert aaa["funnel_v2_note"] is None  # veto takes priority over the data-sufficiency note


def test_hard_veto_decline_signal_black():
    rows = [_base_row("AAA", _n=5, decline_signal_light="⛔"), _base_row("BBB", _n=1)]
    bds.compute_funnel_v2(rows)
    aaa = next(r for r in rows if r["ticker"] == "AAA")
    assert aaa["funnel_v2_rank"] is None
    assert "decline_signal_light=⛔" in aaa["funnel_v2_veto"]


def test_hard_veto_all_downgrade():
    rows = [_base_row("AAA", _n=5, veto_all_downgrade=True), _base_row("BBB", _n=1)]
    bds.compute_funnel_v2(rows)
    aaa = next(r for r in rows if r["ticker"] == "AAA")
    assert aaa["funnel_v2_rank"] is None
    assert "veto_all_downgrade" in aaa["funnel_v2_veto"]


def test_insufficient_data_below_min_layers():
    # Only the quality layer has data; the other three layers are nulled.
    sparse = _base_row(
        "AAA", _n=1,
        implied_growth_pct=None, incremental_roic_pct=None, eps_fy1_fy3_cagr_pct=None,
        eps_rev_3m_pct=None, eps_rev_since_earnings_pct=None,
        fund={"ni_margin_ltm_pct": 10.0, "est_eps_cagr_3y_pct": None},
        pe_vs_5y_x=None, live_peg=None, target_upside_pct=None, pct_5y=None,
    )
    rows = [sparse, _base_row("BBB", _n=2)]
    bds.compute_funnel_v2(rows)
    aaa = next(r for r in rows if r["ticker"] == "AAA")
    assert aaa["funnel_v2_rank"] is None
    assert aaa["funnel_v2_veto"] == []
    assert aaa["funnel_v2_note"] == "資料不足（1/4 層）"


def test_ranks_are_1_indexed_and_contiguous_over_eligible_rows():
    rows = [_base_row(f"T{i}", _n=i) for i in range(1, 6)]
    bds.compute_funnel_v2(rows)
    ranks = sorted(r["funnel_v2_rank"] for r in rows)
    assert ranks == [1, 2, 3, 4, 5]
    # Higher _n -> better on every field above -> rank 1
    best = next(r for r in rows if r["ticker"] == "T5")
    worst = next(r for r in rows if r["ticker"] == "T1")
    assert best["funnel_v2_rank"] == 1
    assert worst["funnel_v2_rank"] == 5


def test_summary_counts_veto_and_insufficient_separately():
    ok = _base_row("OK", _n=1)
    vetoed = _base_row("VET", _n=2, quality_veto_level="拒絕")
    sparse = _base_row(
        "SPARSE", _n=3,
        implied_growth_pct=None, incremental_roic_pct=None, eps_fy1_fy3_cagr_pct=None,
        eps_rev_3m_pct=None, eps_rev_since_earnings_pct=None,
        fund={"ni_margin_ltm_pct": 10.0, "est_eps_cagr_3y_pct": None},
        pe_vs_5y_x=None, live_peg=None, target_upside_pct=None, pct_5y=None,
    )
    rows = [ok, vetoed, sparse]
    summary = bds.compute_funnel_v2(rows)
    assert summary["universe_size"] == 3
    assert summary["veto_count"] == 1
    assert summary["insufficient_count"] == 1
    assert summary["ranked_count"] == 1
    assert summary["layer_config"]["min_layers"] == bds.FUNNEL_V2_MIN_LAYERS
    assert list(summary["layer_config"]["layer_order"]) == list(bds.FUNNEL_V2_LAYER_ORDER)


# ---------------------------------------------------------------------------
# 2026-09-23 修正 — price layer 拿掉 pct_5y
# ---------------------------------------------------------------------------

def test_price_layer_field_list_drops_pct_5y():
    """pct_5y 仍是輸出欄位（見 compute_fundamental_gates），但不再進價格層的
    百分位平均——它是寫 DD 當下抄來的欄位，寫完就凍結，且非 DD 股票整批缺值。"""
    price_fields = [f[0] for f in bds.FUNNEL_V2_LAYER_FIELDS["price"]]
    assert "pct_5y" not in price_fields
    assert price_fields == ["pe_vs_5y_x", "live_peg", "target_upside_pct"]


def test_pct_5y_present_in_row_does_not_affect_price_layer():
    """一列的 pct_5y 不管填什麼，只要 pe_vs_5y_x/live_peg/target_upside_pct 三
    個欄位相同，價格層（profile 第 4 個值）就該相同——證明 pct_5y 真的被排除
    在外，不是只改了 docstring。"""
    a = _base_row("AAA", _n=1, pct_5y=5.0)
    b = _base_row("BBB", _n=1, pct_5y=95.0)
    # 讓其餘三層也相同，只留價格層的三個真正欄位一致、pct_5y 不同。
    b["roic_5y_avg_pct"] = a["roic_5y_avg_pct"]
    b["fcf"] = a["fcf"]
    b["fcf_ni_ratio"] = a["fcf_ni_ratio"]
    b["fund"] = dict(a["fund"])
    b["implied_growth_pct"] = a["implied_growth_pct"]
    b["incremental_roic_pct"] = a["incremental_roic_pct"]
    b["eps_fy1_fy3_cagr_pct"] = a["eps_fy1_fy3_cagr_pct"]
    b["eps_rev_3m_pct"] = a["eps_rev_3m_pct"]
    b["eps_rev_since_earnings_pct"] = a["eps_rev_since_earnings_pct"]
    b["pe_vs_5y_x"] = a["pe_vs_5y_x"]
    b["live_peg"] = a["live_peg"]
    b["target_upside_pct"] = a["target_upside_pct"]
    rows = [a, b]
    bds.compute_funnel_v2(rows)
    assert a["funnel_v2_profile"][3] == pytest.approx(b["funnel_v2_profile"][3])
    assert a["funnel_v2_tiers"] == b["funnel_v2_tiers"]


# ---------------------------------------------------------------------------
# 2026-09-23 修正 — fcf_ni_ratio 封頂（「懲罰過低，不獎勵過高」）
# ---------------------------------------------------------------------------

def test_fcf_ni_capped_helper():
    assert bds._funnel_v2_fcf_ni_capped({"fcf_ni_ratio": 0.5}) == pytest.approx(0.5)
    assert bds._funnel_v2_fcf_ni_capped({"fcf_ni_ratio": bds.FUNNEL_V2_FCF_NI_CAP}) == pytest.approx(
        bds.FUNNEL_V2_FCF_NI_CAP)
    assert bds._funnel_v2_fcf_ni_capped({"fcf_ni_ratio": 35.9}) == pytest.approx(bds.FUNNEL_V2_FCF_NI_CAP)
    assert bds._funnel_v2_fcf_ni_capped({"fcf_ni_ratio": None}) is None


def test_fcf_ni_ratio_ties_above_cap_in_quality_layer():
    """CRWD (35.9) / PANW (13.4) / MDB (11.2)-style names must NOT out-rank a
    name sitting right at the cap — above FUNNEL_V2_FCF_NI_CAP they tie in the
    quality layer's fcf_ni_ratio input. Isolate to just this one field so the
    quality-layer percentile is a pure read of the capped value."""
    def _quality_only_row(ticker, fcf_ni_ratio):
        return {
            "ticker": ticker,
            "roic_5y_avg_pct": None, "fcf": None, "fcf_ni_ratio": fcf_ni_ratio,
            "fund": {"ni_margin_ltm_pct": None, "est_eps_cagr_3y_pct": None},
            "implied_growth_pct": None, "incremental_roic_pct": None,
            "incremental_roic_clamped": False, "incremental_roic_note": None,
            "eps_fy1_fy3_cagr_pct": None,
            "eps_rev_3m_pct": None, "eps_rev_since_earnings_pct": None,
            "pe_vs_5y_x": None, "live_peg": None, "target_upside_pct": None,
            "quality_veto_level": "維持", "decline_signal_light": "🟢",
            "veto_all_downgrade": False,
        }
    at_cap = _quality_only_row("ATCAP", 0.8)
    far_above = _quality_only_row("FARABOVE", 35.9)
    below_cap = _quality_only_row("BELOW", 0.3)
    rows = [at_cap, far_above, below_cap]
    bds.compute_funnel_v2(rows)
    # at_cap and far_above both capped to 0.8 -> tie in the quality layer.
    assert at_cap["funnel_v2_profile"][0] == pytest.approx(far_above["funnel_v2_profile"][0])
    # below_cap is strictly worse (uncapped, below the threshold).
    assert below_cap["funnel_v2_profile"][0] < at_cap["funnel_v2_profile"][0]


# ---------------------------------------------------------------------------
# 2026-09-23 修正 — 排序改 leximin（最弱層先比），缺層視為中性值 2
# ---------------------------------------------------------------------------

def test_leximin_weak_layer_outranked_by_uniform_mediocre():
    """[4,0,x,0]（有一層頂尖但另兩層墊底）排名要輸給 [3,3,3,3]（四層都普通）
    ——先比最弱的那一層，AAA 的最弱層（0）比 BBB 的最弱層（3）差，AAA 排名
    數字較大（較差），不因為 AAA 有一層 tier=4 就贏。population 特意設計成
    n=5、四層各自的代表欄位都是 {1,2,3,4,5} 的一個排列，讓百分位／tier 的對
    應完全可預測：值 v → tier (v-1)。"""
    def _row(ticker, quality, engine, gap, price):
        return {
            "ticker": ticker,
            "roic_5y_avg_pct": quality, "fcf": None, "fcf_ni_ratio": None,
            "fund": {"ni_margin_ltm_pct": None, "est_eps_cagr_3y_pct": None},
            "implied_growth_pct": engine, "incremental_roic_pct": None,
            "incremental_roic_clamped": False, "incremental_roic_note": None,
            "eps_fy1_fy3_cagr_pct": None,
            "eps_rev_3m_pct": gap, "eps_rev_since_earnings_pct": None,
            "pe_vs_5y_x": None, "live_peg": None, "target_upside_pct": price,
            "quality_veto_level": "維持", "decline_signal_light": "🟢",
            "veto_all_downgrade": False,
        }
    aaa = _row("AAA", quality=5, engine=1, gap=3, price=1)   # tiers [4,0,2,0]
    bbb = _row("BBB", quality=4, engine=4, gap=4, price=4)   # tiers [3,3,3,3]
    ccc = _row("CCC", quality=1, engine=2, gap=1, price=2)   # tiers [0,1,0,1]
    ddd = _row("DDD", quality=2, engine=3, gap=2, price=3)   # tiers [1,2,1,2]
    eee = _row("EEE", quality=3, engine=5, gap=5, price=5)   # tiers [2,4,4,4]
    rows = [aaa, bbb, ccc, ddd, eee]
    bds.compute_funnel_v2(rows)
    assert aaa["funnel_v2_tiers"] == [4, 0, 2, 0]
    assert bbb["funnel_v2_tiers"] == [3, 3, 3, 3]
    # AAA has a top-tier layer but its weakest layer (0) is worse than BBB's
    # weakest (3) -> AAA must rank below (worse than) BBB.
    assert aaa["funnel_v2_rank"] > bbb["funnel_v2_rank"]
    order = sorted(rows, key=lambda r: r["funnel_v2_rank"])
    assert [r["ticker"] for r in order] == ["BBB", "EEE", "DDD", "AAA", "CCC"]


def test_missing_layer_treated_as_neutral_not_worst():
    """缺層（tier -1）排序時當作 FUNNEL_V2_MISSING_TIER_AS（中性值 2）——不是
    最差也不是最好。AAA 缺再投資引擎層；BBB 該層是真正的頂尖 tier 4；CCC 該
    層是真正的最差 tier 0。事業品質／期望落差／價格三層對三檔給相同原始值
    （必打平）。預期名次：BBB（真頂尖）＞AAA（缺層，中性）＞CCC（真最差）。"""
    common = dict(
        roic_5y_avg_pct=5.0, fcf=None, fcf_ni_ratio=None,
        fund={"ni_margin_ltm_pct": None, "est_eps_cagr_3y_pct": None},
        incremental_roic_pct=None, incremental_roic_clamped=False, incremental_roic_note=None,
        eps_fy1_fy3_cagr_pct=None,
        eps_rev_3m_pct=5.0, eps_rev_since_earnings_pct=None,
        pe_vs_5y_x=None, live_peg=None, target_upside_pct=5.0,
        quality_veto_level="維持", decline_signal_light="🟢", veto_all_downgrade=False,
    )
    aaa = {"ticker": "AAA", "implied_growth_pct": None, **common}   # engine missing
    bbb = {"ticker": "BBB", "implied_growth_pct": 10.0, **common}   # engine real, top
    ccc = {"ticker": "CCC", "implied_growth_pct": 1.0, **common}    # engine real, bottom
    rows = [aaa, bbb, ccc]
    bds.compute_funnel_v2(rows)
    assert aaa["funnel_v2_tiers"][1] == -1
    assert bbb["funnel_v2_tiers"][1] == 4
    assert ccc["funnel_v2_tiers"][1] == 0
    # quality/gap/price tie identically across all three (same raw inputs).
    assert aaa["funnel_v2_tiers"][0] == bbb["funnel_v2_tiers"][0] == ccc["funnel_v2_tiers"][0]
    assert aaa["funnel_v2_tiers"][2] == bbb["funnel_v2_tiers"][2] == ccc["funnel_v2_tiers"][2]
    assert aaa["funnel_v2_tiers"][3] == bbb["funnel_v2_tiers"][3] == ccc["funnel_v2_tiers"][3]
    order = sorted(rows, key=lambda r: r["funnel_v2_rank"])
    assert [r["ticker"] for r in order] == ["BBB", "AAA", "CCC"]


# ---------------------------------------------------------------------------
# 2026-09-23 新增 — target_upside_pct 的 yfinance 備援
# ---------------------------------------------------------------------------

class _FakeYfTicker:
    def __init__(self, info):
        self.info = info


def test_target_upside_yfinance_fallback_uses_current_price(monkeypatch):
    monkeypatch.setattr(
        bds.yf, "Ticker",
        lambda t: _FakeYfTicker({"targetMeanPrice": 250.0, "currentPrice": 200.0}),
    )
    assert bds._target_upside_yfinance_fallback("TSM") == pytest.approx(25.0)


def test_target_upside_yfinance_fallback_falls_back_to_regular_market_price(monkeypatch):
    monkeypatch.setattr(
        bds.yf, "Ticker",
        lambda t: _FakeYfTicker({"targetMeanPrice": 100.0, "regularMarketPrice": 80.0}),
    )
    assert bds._target_upside_yfinance_fallback("2330.TW") == pytest.approx(25.0)


def test_target_upside_yfinance_fallback_none_when_fields_missing(monkeypatch):
    monkeypatch.setattr(bds.yf, "Ticker", lambda t: _FakeYfTicker({}))
    assert bds._target_upside_yfinance_fallback("ASML") is None


def test_target_upside_yfinance_fallback_none_on_exception(monkeypatch):
    def _boom(t):
        raise RuntimeError("network down")
    monkeypatch.setattr(bds.yf, "Ticker", _boom)
    assert bds._target_upside_yfinance_fallback("XXX") is None


def test_target_upside_source_field_set_by_compute_fundamental_gates():
    """compute_fundamental_gates() 本身不打網路（docstring 明訂），只在算出
    Koyfin 版 target_upside_pct 時記 source="koyfin"；算不出來時是 None，等
    呼叫端（enrich_ticker）決定要不要打 yfinance 備援。"""
    ok = bds.compute_fundamental_gates(
        {"target_avg": 250.0, "last_price_local": 200.0}, None, None, None)
    assert ok["target_upside_source"] == "koyfin"
    missing = bds.compute_fundamental_gates(
        {"target_avg": None, "last_price_local": 200.0}, None, None, None)
    assert missing["target_upside_pct"] is None
    assert missing["target_upside_source"] is None
