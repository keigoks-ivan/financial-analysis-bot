"""ETF 儀表板：強弱欄、判讀欄、XLU／XLRE 加入、研究工具母體固定 21 檔（2026-10-29）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "etf_dash"))

import build_etf_dash as m  # noqa: E402
import compare_common as cc  # noqa: E402
import drawdown_episodes as de  # noqa: E402
import picks_candidates as pc  # noqa: E402
import strength as st  # noqa: E402

ORIGINAL_21 = ["SPY", "RSP", "QQQ", "XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLC", "XLB",
               "SMH", "SMH_UCITS", "TAIEX", "0050", "TOPIX", "EWY", "EWM", "IEV", "EWZ"]


def _bdays(n):
    return pd.bdate_range(end="2026-10-27", periods=n)


def _series(vals, n=None):
    idx = _bdays(len(vals))
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


# ── 判讀 ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("x,expected", [
    (5.0, st.ALIGN_PRICE_AHEAD),
    (4.99, st.ALIGN_MATCHED),
    (4.995, st.ALIGN_PRICE_AHEAD),   # 499.5 bps 四捨五入到 500
    (-5.0, st.ALIGN_EPS_AHEAD),
    (-4.99, st.ALIGN_MATCHED),
    (0.0, st.ALIGN_MATCHED),
    (23.4, st.ALIGN_PRICE_AHEAD),
    (-8.6, st.ALIGN_EPS_AHEAD),
    (None, None),
])
def test_align_label_boundaries(x, expected):
    assert st.align_label_zh(x) == expected


def test_align_label_float_noise_at_exact_threshold():
    # 0.1+0.2 類浮點誤差不能讓恰好 5.00 掉到門檻下
    assert st.align_label_zh(4.999999999999) == st.ALIGN_PRICE_AHEAD
    assert st.align_label_zh(-4.999999999999) == st.ALIGN_EPS_AHEAD


# ── 強弱 ──────────────────────────────────────────────────────────────────

def test_window_excess_pp_basic():
    n = 300
    spy = _series(np.linspace(100, 130, n))
    # 基金 63 日前到現在漲 20%，SPY 同期漲 x
    fund = _series(np.linspace(50, 80, n))
    got = st.window_excess_pp(fund, spy, 63)
    f_ret = fund.iloc[-1] / fund.iloc[-64] - 1
    s_ret = spy.iloc[-1] / spy.iloc[-64] - 1
    assert got == pytest.approx(round((f_ret - s_ret) * 100, 2))


def test_window_excess_pp_insufficient_history_is_none():
    spy = _series(np.linspace(100, 130, 300))
    short = _series(np.linspace(50, 80, 200)).copy()   # 起點在 252 日前之後才開始
    assert st.window_excess_pp(short, spy, 252) is None
    assert st.window_excess_pp(short, spy, 63) is not None
    assert st.window_excess_pp(spy.iloc[-100:], spy, 252) is None


def test_window_excess_pp_stale_fund_is_none():
    spy = _series(np.linspace(100, 130, 300))
    stale = spy.iloc[:-10] * 2
    assert st.window_excess_pp(stale, spy, 63) is None


def test_compute_strength_spy_is_none_and_windows_named():
    spy = _series(np.linspace(100, 130, 300))
    out = st.compute_strength({"SPY": spy, "XLE": spy * 1.0})
    assert out["SPY"] == {"rel_spy_3m_pct": None, "rel_spy_12m_pct": None}
    assert out["XLE"]["rel_spy_3m_pct"] == 0.0 and out["XLE"]["rel_spy_12m_pct"] == 0.0


def test_to_usd_converts_with_fx_and_ffill():
    idx = _bdays(5)
    twd_px = pd.Series([3000.0, 3000.0, 3000.0, 3000.0, 3300.0], index=idx)
    fx = pd.Series([30.0, 30.0, 30.0, 30.0, 33.0], index=idx)
    usd = st.to_usd(twd_px, "TWD", fx)
    assert list(usd.round(6)) == [100.0, 100.0, 100.0, 100.0, 100.0]
    # 匯率缺一天：ffill 前值
    fx2 = fx.drop(idx[4])
    usd2 = st.to_usd(twd_px, "TWD", fx2)
    assert usd2.iloc[-1] == pytest.approx(3300.0 / 30.0)
    # 沒有匯率資料 → None
    assert st.to_usd(twd_px, "TWD", None) is None
    assert st.to_usd(twd_px, "USD", None).equals(twd_px)


def test_currency_of():
    assert st.currency_of("0050.TW") == "TWD"
    assert st.currency_of("^TWII") == "TWD"
    assert st.currency_of("1475.T") == "JPY"
    assert st.currency_of("SMH.L") == "USD"
    assert st.currency_of("XLE") == "USD"


def test_strength_with_fx_changes_ranking():
    """台幣基金本地漲 10%、台幣貶 15%，換美元後約 −5.2%；SPY 持平，強弱要用美元算。"""
    n = 300
    spy = _series(np.full(n, 100.0))
    local = _series(np.r_[np.full(n - 64, 100.0), np.linspace(100, 110, 64)])
    fx = _series(np.r_[np.full(n - 64, 30.0), np.linspace(30, 34.5, 64)])
    usd = st.to_usd(local, "TWD", fx)
    got = st.window_excess_pp(usd, spy, 63)
    assert got == pytest.approx(round((110 / 34.5 / (100 / 30) - 1) * 100, 2), abs=0.02)
    assert got < 0


# ── overview.json 欄位 ───────────────────────────────────────────────────

def _write_fund(out_dir: Path, key: str, pe90):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{key}.json").write_text(json.dumps({
        "label_zh": key, "yf_ticker": key, "as_of": "2026-10-28", "mode": "price",
        "periods": [{"key": "30d"}, {"key": "90d", "eps_chg_pct": 1.0, "price_chg_pct": 2.0,
                                      "implied_pe_chg_pct": pe90}],
        "weighted_forward_pe": {"value": 20.0},
    }), encoding="utf-8")


def test_overview_has_xlu_xlre_strength_and_label(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "OUT_DIR", tmp_path)
    _write_fund(tmp_path, "SPY", 1.0)
    _write_fund(tmp_path, "XLU", 6.2)
    _write_fund(tmp_path, "XLRE", -5.0)
    _write_fund(tmp_path, "XLK", None)
    ov = m.build_overview_json({"XLU": {"rel_spy_3m_pct": 3.2, "rel_spy_12m_pct": -7.5}})
    by = {f["etf_key"]: f for f in ov["funds"]}
    assert {"XLU", "XLRE"} <= set(by)
    assert by["XLU"]["rel_spy_3m_pct"] == 3.2 and by["XLU"]["rel_spy_12m_pct"] == -7.5
    assert by["XLU"]["align_label_zh"] == "股價跑在獲利前面"
    assert by["XLRE"]["align_label_zh"] == "獲利跑在股價前面"
    assert by["XLRE"]["rel_spy_3m_pct"] is None
    assert by["SPY"]["align_label_zh"] == "對得上"
    assert by["XLK"]["align_label_zh"] is None


def test_overview_strength_as_of(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "OUT_DIR", tmp_path)
    _write_fund(tmp_path, "XLU", 0.0)
    ov = m.build_overview_json({"XLU": {"rel_spy_3m_pct": 1.0, "rel_spy_12m_pct": 2.0, "as_of": "2026-10-27"}})
    assert ov["strength_as_of"] == "2026-10-27"
    assert m.build_overview_json()["strength_as_of"] is None


def test_overview_sector_flows_include_xlu_xlre(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "OUT_DIR", tmp_path)
    _write_fund(tmp_path, "XLU", 0.0)
    _write_fund(tmp_path, "XLRE", 0.0)
    ov = m.build_overview_json()
    assert {"XLU", "XLRE"} <= {r["etf_key"] for r in ov["sector_flows"]}


def test_registry_has_23_funds_and_overview_page_lists_them():
    assert len(m.FUND_REGISTRY) == 23
    assert {"XLU", "XLRE"} <= set(m.FUND_REGISTRY)
    html = (SCRIPTS_DIR.parent / "docs" / "etf-dash" / "index.html").read_text(encoding="utf-8")
    assert "key:'XLU'" in html and "key:'XLRE'" in html
    assert "rel_spy_3m_pct" in html and "rel_spy_12m_pct" in html and "align_label_zh" in html


def test_workflow_builds_xlu_xlre():
    wf = (SCRIPTS_DIR.parent / ".github" / "workflows" / "etf-dash-daily.yml").read_text(encoding="utf-8")
    assert "--etf XLU" in wf and "--etf XLRE" in wf


# ── 研究工具母體固定 21 檔 ───────────────────────────────────────────────

def test_research_universe_is_exactly_original_21():
    assert list(cc.RESEARCH_UNIVERSE) == ORIGINAL_21
    assert len(set(cc.RESEARCH_UNIVERSE)) == 21


def test_picks_candidates_fund_keys_stay_21_even_when_overview_has_23(tmp_path, monkeypatch):
    keys = ORIGINAL_21 + ["XLU", "XLRE"]
    (tmp_path / "overview.json").write_text(
        json.dumps({"funds": [{"etf_key": k} for k in sorted(keys)]}), encoding="utf-8")
    monkeypatch.setattr(pc, "FUND_DATA_DIR", tmp_path)
    got = pc.fund_keys()
    assert len(got) == 21
    assert "XLU" not in got and "XLRE" not in got
    assert set(got) == set(ORIGINAL_21)


def test_drawdown_fund_list_stays_21(tmp_path, monkeypatch):
    keys = ORIGINAL_21 + ["XLU", "XLRE"]
    (tmp_path / "overview.json").write_text(
        json.dumps({"funds": [{"etf_key": k, "yf_ticker": k} for k in keys]}), encoding="utf-8")
    monkeypatch.setattr(de, "FUND_DATA_DIR", tmp_path)
    got = [f["key"] for f in de.fund_list()]
    assert len(got) == 21 and "XLU" not in got and "XLRE" not in got


def test_lookthrough_funds_list_unchanged():
    import lookthrough as lt
    assert {k for k, _, _ in lt.FUNDS} == set(ORIGINAL_21)
