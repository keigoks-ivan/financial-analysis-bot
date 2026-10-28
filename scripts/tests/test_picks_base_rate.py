"""picks_base_rate.py：「本站挑選」攻方理由的歷史基率（合成小樣本，不抓網路）。

也測 check_picks_text.py 的基率引用檢查、picks_register.py 的 frozen.base_rates。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "etf_dash"))
import check_picks_text as cpt  # noqa: E402
import picks_base_rate as br  # noqa: E402
import picks_register as preg  # noqa: E402

REG_ON = "2012-12-31"


def _daily(start="2000-01-03", end=REG_ON):
    return pd.bdate_range(start, end)


def _prices(seed=0, fund_alpha=None):
    """SPY、FUND（美元）、SMH、^SOX、^GSPC 的日線寬表。fund_alpha：每日超額漂移序列。"""
    rng = np.random.default_rng(seed)
    idx = _daily()
    n = len(idx)
    spy = 100 * np.exp(np.cumsum(rng.normal(0.0003, 0.01, n)))
    a = np.zeros(n) if fund_alpha is None else fund_alpha
    fund = spy * np.exp(np.cumsum(rng.normal(0.0, 0.01, n) + a))
    adj = pd.DataFrame({"SPY": spy, "FUND": fund, "SMH": fund}, index=idx)
    close = pd.DataFrame({"^SOX": fund, "^GSPC": spy}, index=idx)
    return adj, close


def _long_pe(tmp_path: Path, close: pd.DataFrame, sox_pe: np.ndarray | None = None) -> Path:
    """週頻 sox.csv 與 sp500.csv；預設本益比固定（隱含 EPS 與價格同步）。"""
    d = tmp_path / "long_pe"
    d.mkdir()
    wk = close.groupby(close.index.to_period("W-FRI")).tail(1)
    n = len(wk)
    pe_sox = np.full(n, 20.0) if sox_pe is None else sox_pe
    pd.DataFrame({"date": wk.index.strftime("%Y-%m-%d"), "pe": pe_sox, "src": "terminal"}).to_csv(d / "sox.csv", index=False)
    pd.DataFrame({"date": wk.index.strftime("%Y-%m-%d"), "pe": 15.0, "src": "terminal"}).to_csv(d / "sp500.csv", index=False)
    return d


# ── 統計零件 ──────────────────────────────────────────────────────────────
def test_episodes_gap():
    d = pd.to_datetime(["2020-01-03", "2020-01-10", "2020-06-05", "2020-06-12", "2021-01-01"])
    assert br.episodes(d, 91) == 3


def test_summarize_and_verdict_yes():
    dates = pd.date_range("2000-01-07", periods=600, freq="W-FRI")
    m = np.zeros(600, bool)
    for s in range(0, 600, 60):  # 10 段，每段 20 週
        m[s:s + 20] = True
    rng = np.random.default_rng(1)
    x = rng.normal(0.0, 0.02, 600) + np.where(m, 0.10, 0.0)
    st = br.summarize(dates, x, m, 52)
    assert st["n_cond_weeks"] == 200 and st["episodes"] == 10
    assert st["diff_pct"] >= 3 and st["nw_t"] >= 2
    assert br.verdict(st)[0] == br.VERDICT_YES


def test_verdict_insufficient_and_no():
    dates = pd.date_range("2000-01-07", periods=300, freq="W-FRI")
    rng = np.random.default_rng(2)
    x = rng.normal(0.0, 0.05, 300)
    m = np.zeros(300, bool)
    m[10:40] = True  # 30 週、1 次 → 樣本不足
    assert br.verdict(br.summarize(dates, x, m, 52))[0] == br.VERDICT_NA
    m2 = np.zeros(300, bool)
    for s in range(0, 300, 30):
        m2[s:s + 10] = True  # 100 週、10 次，沒有加超額
    v, _ = br.verdict(br.summarize(dates, x, m2, 52))
    assert v == br.VERDICT_NO


def test_minus_zero_normalized():
    assert str(br._r(-0.04)) == "0.0"


# ── 三條規則 ──────────────────────────────────────────────────────────────
def test_compute_smh_three_rules(tmp_path):
    adj, close = _prices(seed=3)
    lp = _long_pe(tmp_path, close)
    out = br.compute("SMH", REG_ON, adj, close, long_pe_dir=lp)
    assert out["schema"] == "picks-base-rate-v1" and out["attack"] == "SMH"
    ids = [r["id"] for r in out["rules"]]
    assert ids == ["a", "b", "c"]
    for r in out["rules"]:
        assert r["verdict"] in (br.VERDICT_YES, br.VERDICT_NO, br.VERDICT_NA)
        if r.get("excess_cond_pct") is not None:
            assert r["sample_end"] <= REG_ON
            assert r["n_cond_weeks"] <= r["n_weeks"]
    assert "門檻不是結論" in out["brief"]
    # 本益比固定 → 十年分位永遠 100，(c) 條件從不成立 → 無基率
    c = out["rules"][2]
    assert c["verdict"] == br.VERDICT_NA


def test_no_lookahead(tmp_path):
    """登記日之後的價格不能影響結果。"""
    adj, close = _prices(seed=4)
    lp = _long_pe(tmp_path, close)
    a = br.compute("SMH", "2010-06-30", adj, close, long_pe_dir=lp)
    adj2, close2 = adj.copy(), close.copy()
    late = adj2.index > "2010-06-30"
    adj2.loc[late, "SMH"] *= 5
    close2.loc[late, "^SOX"] *= 5
    b = br.compute("SMH", "2010-06-30", adj2, close2, long_pe_dir=lp)
    strip = lambda d: [{k: v for k, v in r.items() if k != "now"} for r in d["rules"]]  # noqa: E731
    assert strip(a) == strip(b)


def test_rule_a_detects_momentum(tmp_path):
    """過去一年贏 SPY 的時候之後一年也贏（合成動能），(a) 要判「有預測力」。"""
    idx = _daily()
    n = len(idx)
    regime = (np.arange(n) // 1300) % 2 == 0  # 約五年一段，交替贏輸
    alpha = np.where(regime, 0.0012, -0.0012)
    adj, close = _prices(seed=5, fund_alpha=alpha)
    lp = _long_pe(tmp_path, close)
    out = br.compute("SMH", REG_ON, adj, close, long_pe_dir=lp)
    a = out["rules"][0]
    assert a["diff_pct"] > 3 and a["verdict"] in (br.VERDICT_YES, br.VERDICT_NA)


def test_fund_without_proxy_only_rule_a(tmp_path):
    adj, close = _prices(seed=6)
    adj = adj.rename(columns={"FUND": "XLV"})
    out = br.compute("XLV", REG_ON, adj, close, long_pe_dir=tmp_path)
    assert out["rules"][0]["excess_all_pct"] is not None
    assert [r["verdict"] for r in out["rules"][1:]] == [br.VERDICT_NA, br.VERDICT_NA]
    assert "無基率" in out["brief"]


def test_rsp_rule_b_is_na(tmp_path):
    adj, close = _prices(seed=7)
    adj = adj.rename(columns={"FUND": "RSP"})
    lp = _long_pe(tmp_path, close)
    out = br.compute("RSP", REG_ON, adj, close, long_pe_dir=lp)
    assert out["rules"][1]["verdict"] == br.VERDICT_NA
    assert "基準" in out["rules"][1]["reason"]


def test_spy_rejected(tmp_path):
    adj, close = _prices(seed=8)
    with pytest.raises(br.BaseRateError):
        br.compute("SPY", REG_ON, adj, close, long_pe_dir=tmp_path)


def test_currency_conversion(tmp_path):
    adj, close = _prices(seed=9)
    adj["0050.TW"] = adj["FUND"] * 30.0
    adj["TWD=X"] = 30.0
    out_twd = br.compute("0050", REG_ON, adj, close, currency="TWD", yf_ticker="0050.TW", long_pe_dir=tmp_path)
    adj2 = adj.rename(columns={"FUND": "X"})
    out_usd = br.compute("X", REG_ON, adj2, close, long_pe_dir=tmp_path)
    assert out_twd["rules"][0]["excess_cond_pct"] == out_usd["rules"][0]["excess_cond_pct"]


# ── 文字檢查：第二段引用 ──────────────────────────────────────────────────
BASE = {"schema": "picks-base-rate-v1", "attack": "SMH", "registered_on": "2027-01-01", "rules": [
    {"id": "a", "verdict": "沒有", "hit_cond_pct": 54.5, "excess_cond_pct": 6.7},
    {"id": "b", "verdict": "沒有", "hit_cond_pct": 61.9, "excess_cond_pct": 9.7},
    {"id": "c", "verdict": "沒有", "hit_cond_pct": 57.0, "excess_cond_pct": 4.7}],
    "brief": "(a) 勝率 54.5%，超額 +6.7%。(b) 勝率 61.9%，超額 +9.7%。(c) 勝率 57.0%，超額 +4.7%。"}
EV = "SMH 近一年 +54.9%｜SPY +13.7%｜上修 +13.6%｜寬度 84.9%｜PEG 0.40"


def _reg(p2: str) -> dict:
    return {"paragraphs": [{"lead": "", "text": "SMH 近一年 +54.9%，SPY 為 +13.7%。"},
                           {"lead": "SMH 攻。", "text": p2},
                           {"lead": "守的那一半放 SPY。", "text": "上修寬度 84.9%。"},
                           {"lead": "", "text": "會錯在哪：上修轉負。"}],
            "frozen_note": "守方是 SPY 本身。"}


def test_citation_pass():
    errs = cpt.check("etf-dash", _reg("上修 +13.6%。近一年贏 SPY 的週，之後 52 週勝率 54.5%。"), EV, "register", BASE)
    assert errs == []


def test_citation_excess_pass():
    assert cpt.check("etf-dash", _reg("上修高於 SPY 的週，之後 52 週平均超額 +9.7%。"), EV, "register", BASE) == []


def test_citation_missing_fails():
    errs = cpt.check("etf-dash", _reg("上修 +13.6%，PEG 0.40。"), EV, "register", BASE)
    assert any("第二段沒有引用" in e for e in errs)


def test_citation_wrong_sign_fails():
    errs = cpt.check("etf-dash", _reg("之後 52 週平均超額 −9.7%。"), EV, "register", BASE)
    assert any("第二段沒有引用" in e for e in errs)


def test_citation_all_na_requires_word():
    na = {**BASE, "rules": [{"id": i, "verdict": "無基率", "hit_cond_pct": None, "excess_cond_pct": None}
                            for i in "abc"], "brief": ""}
    assert any("無基率" in e for e in cpt.check("etf-dash", _reg("上修 +13.6%。"), EV, "register", na))
    assert cpt.check("etf-dash", _reg("三條理由都無基率。上修 +13.6%。"), EV, "register", na) == []


def test_citation_ignores_na_rule_numbers():
    """樣本不足判「無基率」的規則就算有數字，也不算引用。"""
    b = {**BASE, "rules": [dict(BASE["rules"][0], verdict="無基率")] + BASE["rules"][1:]}
    errs = cpt.check("etf-dash", _reg("之後 52 週勝率 54.5%。"), EV, "register", b)
    assert any("第二段沒有引用" in e for e in errs)


def test_no_base_rate_unchanged():
    """沒給基率檔：跟舊行為一樣，不查引用。"""
    assert cpt.check("etf-dash", _reg("上修 +13.6%，PEG 0.40。"), EV, "register") == []


# ── 登記程式：凍結 ───────────────────────────────────────────────────────
def test_validate_base_rate():
    fz = preg.validate_base_rate(BASE, "SMH", "2027-01-01")
    assert "brief" not in fz and [r["id"] for r in fz["rules"]] == ["a", "b", "c"]
    with pytest.raises(preg.RegisterError):
        preg.validate_base_rate(BASE, "QQQ", "2027-01-01")
    with pytest.raises(preg.RegisterError):
        preg.validate_base_rate(BASE, "SMH", "2027-04-01")
    with pytest.raises(preg.RegisterError):
        preg.validate_base_rate({**BASE, "schema": "x"}, "SMH", "2027-01-01")
