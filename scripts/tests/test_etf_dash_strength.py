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


def test_registry_has_51_funds_and_overview_page_lists_them():
    assert len(m.FUND_REGISTRY) == 51
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

# ── 總覽股價與判讀算到最新收盤（2026-10-29 EWZ 案例）────────────────────────

def test_extend_period_to_latest_close_ewz_case():
    # EWZ：07-24→10-23 股價 +19.1996%、EPS +6.4378%；10-23→10-28 再跌 21.06%（42.59→33.62）
    p90 = {"price_chg_pct": 19.1996, "eps_chg_pct": 6.4378, "implied_pe_chg_pct": 11.9581}
    px, pe = m.extend_period_to_latest_close(p90, (33.62 / 42.59 - 1) * 100)
    assert px == pytest.approx((33.62 / 35.73 - 1) * 100, abs=0.05)  # 07-24 收 35.73
    assert pe == pytest.approx(((1 + px / 100) / 1.064378 - 1) * 100, abs=1e-3)
    assert st.align_label_zh(pe) == "獲利跑在股價前面"
    assert st.align_label_zh(p90["implied_pe_chg_pct"]) == "股價跑在獲利前面"


def test_extend_period_to_latest_close_full_day_and_missing():
    p = {"price_chg_pct": 4.0, "eps_chg_pct": 2.0, "implied_pe_chg_pct": 1.9608}
    assert m.extend_period_to_latest_close(p, 0.0) == (4.0, pytest.approx(1.9608, abs=1e-4))
    assert m.extend_period_to_latest_close(p, None) == (4.0, 1.9608)
    assert m.extend_period_to_latest_close({"key": "30d"}, 3.0) == (None, None)
    assert m.extend_period_to_latest_close({"price_chg_pct": 4.0}, 1.0) == (pytest.approx(5.04), None)


def test_overview_uses_latest_close_but_fund_periods_untouched(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "OUT_DIR", tmp_path)
    tmp_path.mkdir(parents=True, exist_ok=True)
    periods = [{"key": "30d", "eps_chg_pct": 1.0, "price_chg_pct": 2.0, "implied_pe_chg_pct": 0.9901},
               {"key": "90d", "eps_chg_pct": 6.4378, "price_chg_pct": 19.1996, "implied_pe_chg_pct": 11.9581}]
    (tmp_path / "EWZ.json").write_text(json.dumps({
        "label_zh": "EWZ", "yf_ticker": "EWZ", "as_of": "2026-10-29", "mode": "price",
        "eps_as_of": "2026-10-24", "price_since_eps_as_of_pct": -21.0613,
        "price": {"close": 33.62, "date": "2026-10-28", "currency": "USD"},
        "periods": periods, "weighted_forward_pe": {"value": 7.8},
    }), encoding="utf-8")
    row = next(f for f in m.build_overview_json()["funds"] if f["etf_key"] == "EWZ")
    assert row["price_chg_pct_90d"] == pytest.approx(-5.91, abs=0.05)
    assert row["implied_pe_chg_pct_90d"] < -5
    assert row["align_label_zh"] == "獲利跑在股價前面"
    assert row["price_as_of"] == "2026-10-28"
    on_disk = json.loads((tmp_path / "EWZ.json").read_text(encoding="utf-8"))["periods"]
    assert on_disk == periods


# ── 2026-10-29：EPS 涵蓋不足 ─────────────────────────────────────────────

def _write_fund_cov(out_dir: Path, key: str, pe90, coverage):
    out_dir.mkdir(parents=True, exist_ok=True)
    p90 = {"key": "90d", "eps_chg_pct": 1.0, "price_chg_pct": 2.0, "implied_pe_chg_pct": pe90}
    if coverage is not None:
        p90["coverage_pct"] = coverage
    (out_dir / f"{key}.json").write_text(json.dumps({
        "label_zh": key, "yf_ticker": key, "as_of": "2026-10-28", "mode": "price",
        "periods": [{"key": "30d"}, p90], "weighted_forward_pe": {"value": 20.0},
    }), encoding="utf-8")


def test_eps_coverage_threshold_is_named_constant_70():
    assert m.EPS_COVERAGE_MIN_PCT == 70
    assert m.ALIGN_LOW_COVERAGE_ZH == "涵蓋不足"


@pytest.mark.parametrize("cov,low", [
    (0.0, True), (35.69, True), (69.4, True),
    (69.5, False),    # 四捨五入到 70，不算不足
    (70.0, False), (70.4, False), (99.66, False),
    (None, False),    # 舊格式缺欄位，無從判斷，不標
])
def test_eps_coverage_is_low_boundaries(cov, low):
    assert m.eps_coverage_is_low(cov) is low


def test_overview_low_coverage_overrides_align_label(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "OUT_DIR", tmp_path)
    _write_fund_cov(tmp_path, "XBI", 8.0, 35.69)     # 虧損股多，只有 36% 權重有預估
    _write_fund_cov(tmp_path, "EPHE", None, 0.0)     # Yahoo 沒資料
    _write_fund_cov(tmp_path, "VNM", 8.0, 70.76)     # 剛過門檻
    ov = m.build_overview_json()
    by = {f["etf_key"]: f for f in ov["funds"]}
    assert by["XBI"]["align_label_zh"] == "涵蓋不足" and by["XBI"]["eps_coverage_90d_pct"] == 35.69
    assert by["EPHE"]["align_label_zh"] == "涵蓋不足" and by["EPHE"]["eps_coverage_90d_pct"] == 0.0
    assert by["VNM"]["align_label_zh"] == "股價跑在獲利前面"
    assert by["VNM"]["eps_coverage_90d_pct"] == 70.76


# ── 總覽三個分頁（單一來源 OV_TABS）──────────────────────────────────────

def _page_tabs():
    import re
    html = (SCRIPTS_DIR.parent / "docs" / "etf-dash" / "index.html").read_text(encoding="utf-8")
    block = html[html.index("var OV_TABS = ["):html.index("var OV_TAB_DEFAULT")]
    tabs = {}
    for tm in re.finditer(r"\{key:'(sectors|countries|core)', label:'([^']+)'(.*?)(?=\n  \{key:'(?:sectors|countries|core)'|\Z)", block, re.S):
        groups = []
        for gm in re.finditer(r"\{label:'([^']+)', color:'[^']+', funds:\[(.*?)\]\}", tm.group(3), re.S):
            groups.append((gm.group(1), re.findall(r"\{key:'([^']+)', label:", gm.group(2))))
        tabs[tm.group(1)] = (tm.group(2), groups)
    return html, tabs


def test_overview_tabs_order_and_default():
    html, tabs = _page_tabs()
    assert list(tabs) == ["sectors", "countries", "core"]
    assert [tabs[k][0] for k in tabs] == ["產業", "國家", "大盤與持股"]
    assert "var OV_TAB_DEFAULT = 'sectors';" in html


def test_overview_tab_members_exist_in_registry_and_cover_all_51():
    _, tabs = _page_tabs()
    seen = set()
    for _label, groups in tabs.values():
        for _g, keys in groups:
            assert set(keys) <= set(m.FUND_REGISTRY)
            assert len(keys) == len(set(keys))
            seen |= set(keys)
    assert seen == set(m.FUND_REGISTRY) and len(seen) == 51


def test_overview_tab_groups_match_spec():
    _, tabs = _page_tabs()
    sec = dict(tabs["sectors"][1])
    assert list(sec) == ["美股產業", "美股子產業"]
    assert sec["美股產業"] == ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLC", "XLB", "XLU", "XLRE"]
    assert sec["美股子產業"] == ["SMH", "SOXX", "IGV", "ITA", "XBI", "XOP", "KRE", "XHB", "GDX"]
    assert "SMH_UCITS" not in sum(sec.values(), [])
    cty = dict(tabs["countries"][1])
    assert list(cty) == ["美洲", "歐洲", "東北亞", "南亞與東南亞", "大洋洲與中東"]
    assert set(cty["美洲"]) == {"SPY", "EWC", "EWW", "EWZ"}
    assert set(cty["歐洲"]) == {"IEV", "EWU", "EWG", "EWQ", "EWL", "EWN", "EWI", "EWP"}
    assert set(cty["東北亞"]) == {"TOPIX", "EWY", "0050", "TAIEX", "MCHI", "EWH"}
    assert set(cty["南亞與東南亞"]) == {"INDA", "EWS", "EWM", "THD", "EIDO", "EPHE", "VNM"}
    assert set(cty["大洋洲與中東"]) == {"EWA", "ENZL", "KSA"}
    core = dict(tabs["core"][1])
    assert list(core) == ["大盤與持股"]
    assert set(core["大盤與持股"]) == {"SPY", "RSP", "QQQ", "SMH", "SMH_UCITS", "0050", "TAIEX"}
    # 國家分頁各組顏色要分得出來
    import re
    html = (SCRIPTS_DIR.parent / "docs" / "etf-dash" / "index.html").read_text(encoding="utf-8")
    colors = re.findall(r"\{label:'(?:美洲|歐洲|東北亞|南亞與東南亞|大洋洲與中東)', color:'(#[0-9a-f]{6})'", html)
    assert len(colors) == 5 and len(set(colors)) == 5


def test_overview_page_has_country_note_and_lowcov_note():
    html, _ = _page_tabs()
    assert "這些基金都在美國掛牌，報酬以美元計，含匯率變動。" in html
    assert "有分析師 EPS 預估的成分股不到七成權重" in html


# ── 選單、轉址樁、風險儀表頁 ─────────────────────────────────────────────

def test_site_nav_has_single_etf_dash_entry_and_sectors_is_skipped():
    import site_nav
    nav = site_nav.full_nav_block(group="macrochip", item=None)
    assert nav.count('href="/etf-dash/') == 1   # 只留研究 ▾ ETF 儀表板，分頁在頁內切換
    assert '<a href="/etf-dash/">ETF 儀表板</a>' in nav
    assert "全球市場" not in nav and "產業板塊" not in nav
    assert "/sectors.html" not in nav
    assert nav.count('<a href="/markets.html">風險偏好儀表</a>') == 1   # 市場 ▾
    assert site_nav.full_nav_block(group="market", item="riskg").count('href="/markets.html" class="active"') == 1
    assert "sectors.html" in site_nav.SKIP_FILES


def test_sectors_html_is_redirect_stub():
    html = (SCRIPTS_DIR.parent / "docs" / "sectors.html").read_text(encoding="utf-8")
    assert 'http-equiv="refresh"' in html and "location.replace" in html
    assert html.count("/etf-dash/?view=overview") >= 3 and "tab=sectors" in html
    assert "imq-nav-root" not in html


def test_markets_html_keeps_only_risk_gauge():
    html = (SCRIPTS_DIR.parent / "docs" / "markets.html").read_text(encoding="utf-8")
    assert "<!-- RISK_GAUGE:START -->" in html and "<!-- RISK_GAUGE:END -->" in html
    assert '<section class="hero">' in html   # build_risk_gauge 找不到標記時插在 hero 之後
    assert "marketTable" not in html and "var MARKETS" not in html
    assert "風險偏好儀表" in html and "Risk-On / Risk-Off Gauge" in html
    assert "tab=countries" in html
    assert "全球股市投資知識" in html


# ── RS（2026-10-30，舊 update_markets.py 算法，總覽全部基金一起排名）──────────────

def test_percentile_le_counts_ties_and_self():
    assert st.percentile_le([1, 2, 2, 4], 2) == 75.0
    assert st.percentile_le([1, 2, 2, 4], 4) == 100.0
    assert st.percentile_le([1, 2, 2, 4], 1) == 25.0


@pytest.mark.parametrize("p,expected", [
    ((80, 50, 20), ("accelerating", 5.0)),
    ((50, 50, 20), ("steady", 2.0)),
    ((50, 50, 50), ("steady", 2.0)),
    ((20, 50, 80), ("fading", -5.0)),
    ((50, 80, 20), ("choppy", 0.0)),
])
def test_rs_trend_bonus(p, expected):
    assert st.rs_trend_of(*p) == expected


def test_compute_rs_weights_and_bonus():
    # 兩檔：A 三項都較高，B 三項都較低 → A 百分位 100/100/100，B 50/50/50
    out = st.compute_rs({"A": (3.0, 6.0, 9.0), "B": (1.0, 2.0, 3.0)})
    assert out["A"]["rs_score"] == 100.0           # 100 加穩定 +2，上限 100
    assert out["A"]["rs_trend"] == "steady"
    assert out["B"]["rs_score"] == 52.0            # 50*0.2+50*0.3+50*0.5＝50，穩定 +2
    assert (out["B"]["rs_pct_1w"], out["B"]["rs_pct_4w"], out["B"]["rs_pct_13w"]) == (50.0, 50.0, 50.0)


def test_compute_rs_weighted_sum_and_accelerating_cap_and_floor():
    # 五檔，讓 X 的 1w 最強、13w 最弱：pr1=100 > pr4=60 > pr13=20 → 加速 +5
    rets = {"X": (9, 3, 1), "A": (1, 1, 5), "B": (2, 2, 4), "C": (3, 5, 3), "D": (4, 4, 2)}
    out = st.compute_rs(rets)
    x = out["X"]
    assert (x["rs_pct_1w"], x["rs_pct_4w"], x["rs_pct_13w"]) == (100.0, 60.0, 20.0)
    assert x["rs_trend"] == "accelerating"
    assert x["rs_score"] == round(100 * 0.2 + 60 * 0.3 + 20 * 0.5 + 5, 1) == 53.0
    # 下限 0：單一弱者三項都最低且一路轉弱不會低於 0
    lo = st.compute_rs({"W": (0.0, 0.0, 0.0), "S": (1.0, 1.0, 1.0)})
    assert lo["W"]["rs_score"] >= 0


def test_compute_rs_missing_returns_not_ranked_and_not_in_population():
    out = st.compute_rs({"A": (1, 2, 3), "B": (2, 3, 4), "N": (1, None, 3), "Z": None})
    assert out["N"]["rs_score"] is None and out["N"]["rs_trend"] is None
    assert out["Z"]["rs_score"] is None
    # 母體只有 A、B：B 百分位 100，A 50（N 不佔分母）
    assert out["A"]["rs_pct_1w"] == 50.0 and out["B"]["rs_pct_1w"] == 100.0


def test_compute_rs_all_missing():
    assert st.compute_rs({"A": None})["A"]["rs_score"] is None
    assert st.compute_rs({}) == {}


def test_window_return_pct_uses_bench_calendar_and_insufficient_data():
    bench = _series(np.arange(100.0, 200.0))
    fund = _series(np.arange(100.0, 200.0) * 2)
    r = st.window_return_pct(fund, bench, 5)
    assert r == pytest.approx((199 * 2 / (194 * 2) - 1) * 100)
    short = fund.iloc[-3:]            # 起點日之前沒資料
    assert st.window_return_pct(short, bench, 5) is None
    assert st.window_return_pct(fund, bench.iloc[-4:], 5) is None
    stale = fund.iloc[:-10]           # 最後一根比 SPY 終點早超過 5 天
    assert st.window_return_pct(stale, bench, 5) is None
