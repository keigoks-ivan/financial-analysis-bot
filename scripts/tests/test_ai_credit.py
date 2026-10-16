"""scripts/ai_credit/ 的離線單元測試（不連網）。

涵蓋：近四季累計相減（含缺零值季）、遲滯規則、12 條越線判斷、狀態改變才通知、首跑不通知、
抓失敗沿用舊值與日期、事件去重與關鍵字、內嵌 XBRL 解析、頁面冒煙測試。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "ai_credit"))

import aic_alerts as AL  # noqa: E402
import aic_events as EV  # noqa: E402
import aic_metrics as M  # noqa: E402
import aic_page as PG  # noqa: E402
import aic_page2 as P2  # noqa: E402
import aic_round2 as R2  # noqa: E402
import build_ai_credit as B  # noqa: E402
import ixparse as IX  # noqa: E402
import sec_facts as S  # noqa: E402
from aic_sources import spread_stats  # noqa: E402


# ---------------------------------------------------------------------------
# 近四季累計相減
# ---------------------------------------------------------------------------
def R(start, end, val, form="10-Q", filed="2026-08-01"):
    return {"start": start, "end": end, "val": val, "form": form, "filed": filed}


def test_ttm_is_annual_minus_prior_ytd_plus_current_ytd():
    rs = [
        R("2025-01-01", "2025-12-31", 100.0, "10-K"),
        R("2025-01-01", "2025-06-30", 40.0),
        R("2026-01-01", "2026-06-30", 50.0),
    ]
    t = S.ttm_flow(rs)
    assert t["value"] == 110.0 and t["end"] == "2026-06-30"
    assert t["parts"] == {"A": 100.0, "P": 40.0, "C": 50.0}


def test_ttm_without_newer_ytd_is_the_annual():
    t = S.ttm_flow([R("2025-01-01", "2025-12-31", 100.0, "10-K")])
    assert t["value"] == 100.0 and t["end"] == "2025-12-31"


def test_ttm_missing_zero_quarter_is_not_filled_by_last_four():
    """零值季常整筆缺漏：發債只在 2025 H2 有事實（20），2026 上半年與 2025 上半年都沒有。
    正確的近四季是 20；若取最後四筆（含更早的別年資料）會錯。"""
    main = [R("2025-01-01", "2025-12-31", 500.0, "10-K"), R("2025-01-01", "2025-06-30", 200.0), R("2026-01-01", "2026-06-30", 260.0)]
    win = S.ttm_window(main)
    issue = [R("2024-01-01", "2024-12-31", 90.0, "10-K"), R("2025-01-01", "2025-12-31", 20.0, "10-K")]
    t = S.ttm_flow(issue, win, zero_ok=True)
    assert t["value"] == 20.0
    assert sorted(t["assumed_zero"]) == ["C", "P"]
    # 不允許補零時，缺漏就是算不出來，而不是默默給一個錯數字
    assert S.ttm_flow(issue, win, zero_ok=False) is None


def test_ttm_second_tag_fills_a_period_but_tags_are_not_summed():
    """Oracle 式換 tag：新 tag 有今年累計，舊 tag 有去年同期（0）。每個元件只取第一個有值的 tag。"""
    main = [R("2025-06-01", "2026-05-31", 900.0, "10-K"), R("2026-06-01", "2026-08-31", 300.0), R("2025-06-01", "2025-08-31", 100.0)]
    win = S.ttm_window(main)
    new_tag = [R("2025-06-01", "2026-05-31", 46.0, "10-K")]
    old_tag = [R("2025-06-01", "2025-08-31", 0.0)]
    t = S.ttm_flow([new_tag, old_tag], win, zero_ok=True)
    assert t["value"] == 46.0 and t["assumed_zero"] == ["C"]


def test_single_quarters_derives_q4_and_missing_quarter():
    rs = [
        R("2025-01-01", "2025-03-31", 10.0),
        R("2025-01-01", "2025-06-30", 25.0),          # Q2 = 15（沒有直接 3 個月事實）
        R("2025-01-01", "2025-09-30", 45.0),          # Q3 = 20
        R("2025-01-01", "2025-12-31", 70.0, "10-K"),  # Q4 = 25
    ]
    q = S.single_quarters(rs)
    assert q == {"2025-03-31": 10.0, "2025-06-30": 15.0, "2025-09-30": 20.0, "2025-12-31": 25.0}


def test_rows_filters_non_periodic_forms_and_dedups_latest_filing():
    facts = {"facts": {"us-gaap": {"X": {"units": {"USD": [
        {"start": "2025-01-01", "end": "2025-12-31", "val": 1, "form": "10-K", "filed": "2026-02-01"},
        {"start": "2025-01-01", "end": "2025-12-31", "val": 2, "form": "10-K", "filed": "2026-03-01"},
        {"start": "2025-01-01", "end": "2025-12-31", "val": 99, "form": "424B2", "filed": "2026-04-01"},
    ]}}}}}
    rs = S.rows(facts, "X")
    assert len(rs) == 1 and rs[0]["val"] == 2


# ---------------------------------------------------------------------------
# 遲滯規則
# ---------------------------------------------------------------------------
def series(vals, start=1):
    return [(f"2026-01-{i + start:02d}", v) for i, v in enumerate(vals)]


def test_hysteresis_enter_exit_and_hold():
    s = series([-5, -15, -20.0, -15, -10.0, -9.9, -15])
    # -20 剛好等於進入線 → 進入；-15、-10 維持；-9.9 > -10 → 解除；-15 維持未越
    state, tr = M.run_hysteresis(s)
    assert [(t["date"], t["to"]) for t in tr] == [("2026-01-03", "in"), ("2026-01-06", "out")]
    assert state is False


def test_hysteresis_middle_zone_keeps_previous_state():
    assert M.run_hysteresis(series([-15, -12, -18]))[0] is False          # 從沒進過 → 維持未越
    assert M.run_hysteresis(series([-25, -15, -12]))[0] is True            # 進過 → 中間帶維持越線
    assert M.run_hysteresis(series([-25, -15, -10.0]))[0] is True          # 恰好 -10 還不算解除
    assert M.run_hysteresis(series([-25, -9.99]))[0] is False


def test_hysteresis_continues_from_stored_state_and_skips_processed_days():
    s = series([-25, -15, -12, -8])
    st, tr = M.run_hysteresis(s, state=True, after="2026-01-03")   # 只處理 01-04 的 -8
    assert st is False and tr[0]["date"] == "2026-01-04"
    st2, tr2 = M.run_hysteresis(s, state=True, after="2026-01-04")
    assert st2 is True and tr2 == []


def test_bootstrap_runs_whole_history_from_unbreached():
    s = series([0, -22, -30, -12, -8, -9, -3])
    state, tr = M.run_hysteresis(s, state=None)
    assert state is False and [t["to"] for t in tr] == ["in", "out"]


def test_rel_series_is_pp_difference_of_63_day_returns():
    dates = [f"d{i:03d}" for i in range(70)]
    stock = [(d, 100.0 * (1.01 ** i)) for i, d in enumerate(dates)]
    bench = [(d, 100.0 * (1.005 ** i)) for i, d in enumerate(dates)]
    out = M.rel_series(stock, bench, 63)
    assert len(out) == 7
    expect = (1.01 ** 63 - 1) * 100 - (1.005 ** 63 - 1) * 100
    assert out[0][1] == pytest.approx(expect)


# ---------------------------------------------------------------------------
# 12 條越線判斷
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("i,v,expected", [
    (1, 1.0, False), (1, 1.0001, True),
    (2, 2, False), (2, 3, True),
    (3, 0.50, False), (3, 0.5001, True),
    (4, 3.5, False), (4, 3.51, True),
    (5, 1.5, False), (5, 1.49, True),
    (6, 1.0, False), (6, 0.99, True),
    (10, 0.85, False), (10, 0.8499, True),
    (11, 9.99, False), (11, 10.0, True),
    (12, 0.25, False), (12, 0.2501, True),
])
def test_breach_thresholds_and_boundaries(i, v, expected):
    assert M.breach(i, v) is expected


def test_breach_none_stays_none():
    assert M.breach(1, None) is None


def base_units():
    """所有 12 條都「未越線」的合成資料。金額單位：美元。"""
    B_ = 1e9
    clouds = {}
    for t in M.CLOUDS:
        clouds[f"cloud:{t}"] = {"data": {"capex": 50 * B_, "ocf": 100 * B_, "issued": 20 * B_, "repaid": 5 * B_,
                                         "end": "2026-06-30", "assumed_zero": []}, "fetched": "2026-10-16", "stale": False}
    mk = {}
    for t in M.REL_NAME:
        mk[t] = {"rel_pp": 0.0, "asof": "2026-10-15", "ret_stock": 5.0, "ret_bench": 5.0, "dd1y_rel": -10.0,
                 "flag": {"breached": False, "asof": "2026-10-15", "since": None}}
    u = dict(clouds)
    u["orcl"] = {"data": {"debt_current": 10 * B_, "debt_lt": 100 * B_, "debt_check": None, "cash": 30 * B_, "afs": 0.0,
                          "fin_lease": 9 * B_, "oi": 20 * B_, "dep": 8 * B_, "amort": 2 * B_, "bs_end": "2026-08-31",
                          "flow_end": "2026-08-31", "notes": []}, "stale": False}
    u["crwv"] = {"data": {"oi": 0.0, "dda": 4 * B_, "interest": 1 * B_, "ocf": 6 * B_, "cash": 5 * B_, "maturities_12m": 6 * B_,
                          "bs_end": "2026-06-30", "flow_end": "2026-06-30"}, "stale": False}
    u["market"] = {"data": mk, "stale": False}
    u["bdc_px"] = {"data": {t: {"price": 9.0, "asof": "2026-10-15"} for t in M.BDCS}, "stale": False}
    for t in M.BDCS:
        u[f"bdc_nav:{t}"] = {"data": {"nav": 10.0, "asof": "2026-06-30"}, "stale": False}
    qs = [{"end": f"2025-{m:02d}-28", "rev": 50 * B_, "ar": 25 * B_, "dso": 45.5, "dio": 100.0} for m in range(1, 9)]
    u["nvda_fin"] = {"data": {"quarters": qs, "rev_ttm": 300 * B_, "rev_end": "2026-07-26", "guarantee": 20 * B_,
                              "guarantee_date": "2026-07-26"}, "stale": False}
    u["nvda_commit"] = {"data": {"ai_cloud": 10 * B_, "equity": 10 * B_, "report_date": "2026-07-26"}, "stale": False}
    return u


def by_id(inds):
    return {x["id"]: x for x in inds}


def test_all_twelve_unbreached_baseline():
    inds = M.compute_indicators(base_units())
    assert len(inds) == 12
    assert [x["breached"] for x in inds] == [False] * 12
    assert M.summarize(inds) == {"n_breached": 0, "n_total": 12, "n_unknown": 0, "breached_ids": []}


def test_each_indicator_can_breach_through_the_full_pipeline():
    u = base_units()
    # 1：資本支出 > 營運現金流
    for t in M.CLOUDS:
        u[f"cloud:{t}"]["data"]["capex"] = 120e9
    inds = by_id(M.compute_indicators(u))
    assert inds[1]["breached"] is True
    assert inds[2]["breached"] is True            # 每家 FCF 都為負（5 家 ≥ 3）
    assert inds[2]["value"] == 5
    # 3：淨發債 / 資本支出 = (5×15) / (5×120) = 12.5% → 另行測
    u = base_units()
    for t in M.CLOUDS:
        u[f"cloud:{t}"]["data"]["issued"] = 60e9
    assert by_id(M.compute_indicators(u))[3]["breached"] is True   # (60-5)/50 = 110%
    # 4
    u = base_units()
    u["orcl"]["data"]["debt_lt"] = 300e9
    x = by_id(M.compute_indicators(u))[4]
    assert x["breached"] is True and x["value"] == pytest.approx((310 - 30) / 30)
    # 5
    u = base_units()
    u["crwv"]["data"]["interest"] = 3e9
    assert by_id(M.compute_indicators(u))[5]["breached"] is True   # 4/3 = 1.33
    # 6
    u = base_units()
    u["crwv"]["data"]["maturities_12m"] = 20e9
    assert by_id(M.compute_indicators(u))[6]["breached"] is True   # 11/20
    # 7–9：由遲滯旗標決定，不由當日值
    u = base_units()
    u["market"]["data"]["CRWV"]["flag"]["breached"] = True
    u["market"]["data"]["CRWV"]["rel_pp"] = -15.0          # 在中間帶，維持越線
    r = by_id(M.compute_indicators(u))
    assert r[8]["breached"] is True and r[7]["breached"] is False and r[9]["breached"] is False
    # 10
    u = base_units()
    u["bdc_px"]["data"]["OBDC"]["price"] = 5.0             # (0.9+0.5+0.9)/3 = 0.767
    assert by_id(M.compute_indicators(u))[10]["breached"] is True
    # 11：最新 56 天、前四季均 45.5 → +10.5
    u = base_units()
    u["nvda_fin"]["data"]["quarters"][-1]["dso"] = 56.0
    x = by_id(M.compute_indicators(u))[11]
    assert x["breached"] is True and x["value"] == pytest.approx(10.5)
    # 12：(20+10+10)/300 = 13.3% → 保證放大到 80B：(80+20)/300 = 33%
    u = base_units()
    u["nvda_fin"]["data"]["guarantee"] = 80e9
    assert by_id(M.compute_indicators(u))[12]["breached"] is True


def test_missing_source_gives_unknown_not_zero():
    u = base_units()
    del u["cloud:ORCL"]
    del u["crwv"]
    inds = by_id(M.compute_indicators(u))
    for i in (1, 2, 3, 5, 6):
        assert inds[i]["breached"] is None and inds[i]["value"] is None
    assert M.summarize(list(inds.values()))["n_unknown"] == 5


# ---------------------------------------------------------------------------
# 抓失敗沿用舊值與日期
# ---------------------------------------------------------------------------
def test_failed_fetch_reuses_previous_value_and_date():
    prev = {"cloud:MSFT": {"data": {"capex": 1}, "fetched": "2026-10-10", "stale": False, "error": None}}
    errors = {}

    def boom():
        raise RuntimeError("SEC 503")

    u = B.run_unit("cloud:MSFT", boom, prev, "2026-10-16", errors)
    assert u["data"] == {"capex": 1} and u["stale"] is True
    assert u["fetched"] == "2026-10-10"                  # 保留原始抓取日期，不改成今天
    assert "SEC 503" in errors["cloud:MSFT"]


def test_failed_fetch_without_previous_gives_nothing_not_zero():
    errors = {}
    u = B.run_unit("orcl", lambda: 1 / 0, {}, "2026-10-16", errors)
    assert u is None and "orcl" in errors


def test_success_resets_stale():
    prev = {"x": {"data": 1, "fetched": "2026-10-01", "stale": True, "error": "old"}}
    u = B.run_unit("x", lambda: 2, prev, "2026-10-16", {})
    assert u == {"data": 2, "fetched": "2026-10-16", "stale": False, "error": None}


def test_stale_flag_reaches_the_indicator():
    u = base_units()
    u["cloud:MSFT"]["stale"] = True
    inds = by_id(M.compute_indicators(u))
    assert inds[1]["stale"] and inds[2]["stale"] and inds[3]["stale"] and not inds[4]["stale"]


# ---------------------------------------------------------------------------
# 通知：狀態改變才發、首跑不發
# ---------------------------------------------------------------------------
def make_inds(breached_by_id):
    inds = M.compute_indicators(base_units())
    for x in inds:
        x["breached"] = breached_by_id.get(x["id"], False)
    return inds


def test_first_run_has_no_alert():
    assert AL.build_alerts(None, make_inds({12: True})) == []


def test_no_change_no_alert():
    prev = {str(i): False for i in range(1, 13)}
    assert AL.build_alerts(prev, make_inds({})) == []
    prev["12"] = True
    assert AL.build_alerts(prev, make_inds({12: True})) == []


def test_unbreached_to_breached_and_back_both_alert():
    prev = {str(i): False for i in range(1, 13)}
    a = AL.build_alerts(prev, make_inds({4: True}))
    assert [(x["id"], x["old"], x["new"]) for x in a] == [(4, False, True)]
    prev["4"] = True
    b = AL.build_alerts(prev, make_inds({}))
    assert [(x["id"], x["old"], x["new"]) for x in b] == [(4, True, False)]


def test_unknown_to_known_does_not_alert():
    prev = {str(i): None for i in range(1, 13)}
    assert AL.build_alerts(prev, make_inds({1: True})) == []


def test_alert_files_content(tmp_path):
    prev = {str(i): False for i in range(1, 13)}
    inds = make_inds({6: True})
    al = AL.build_alerts(prev, inds)
    title = AL.write_alert_files(tmp_path, al, inds)
    assert "第 6 條進入越線" in title and "12 條裡 1 條越線" in title
    body = (tmp_path / "aic_alert.txt").read_text(encoding="utf-8")
    assert "未越線 → 越線" in body and "門檻 < 1.0 倍" in body and "https://research.investmquest.com/ai-credit/" in body
    assert (tmp_path / "aic_mail.html").exists()


def test_test_alert_is_marked():
    inds = make_inds({3: True})
    al = AL.build_alerts(None, inds, test=True)
    title, _ = AL.alert_text(al, inds, test=True)
    assert title.startswith("【測試】")


# ---------------------------------------------------------------------------
# 歷史檔
# ---------------------------------------------------------------------------
def test_history_appends_and_same_day_rerun_overwrites(tmp_path):
    p = tmp_path / "h.jsonl"
    inds = M.compute_indicators(base_units())
    B.write_history(p, B.history_row("2026-10-15", inds))
    B.write_history(p, B.history_row("2026-10-16", inds))
    B.write_history(p, B.history_row("2026-10-16", inds))
    lines = p.read_text().splitlines()
    assert [json.loads(x)["date"] for x in lines] == ["2026-10-15", "2026-10-16"]
    row = json.loads(lines[-1])
    assert set(row["v"]) == {str(i) for i in range(1, 13)} and set(row["b"]) == set(row["v"])


# ---------------------------------------------------------------------------
# 事件：關鍵字與去重
# ---------------------------------------------------------------------------
def test_event_keywords():
    assert EV.match_event("Oracle-Blue Owl project delay ripples through AI financing")
    assert EV.match_event("SoftBank prices record $11bn junk bond to fund OpenAI bet")
    assert EV.match_event("Startup raises GPU-backed credit line")
    assert EV.match_event("Nscale's data center contracts", "lenders arrange a $2B loan")        # 標題有基礎建設詞，摘要有融資詞
    assert not EV.match_event("Apple unveils new iPhone", "")
    assert not EV.match_event("Bank of Japan raises rates", "loans and bonds repriced")           # 沒有 AI 基礎建設或公司名
    assert not EV.match_event("Company is releasing new AI models with OpenAI")                  # releasing 不是 leasing
    assert not EV.match_event("Meta ships new feature", "data center mention only in passing but no finance words")


def test_event_dedup_by_url_and_by_title():
    existing = [{"date": "2026-10-01", "title": "CoreWeave bonds slide", "url": "https://x.com/a/?utm=1", "source": "S"}]
    cands = [
        {"date": "2026-10-02", "title": "Different title", "url": "https://X.com/a", "source": "T", "first_seen": "2026-10-02", "matched": []},       # 同網址
        {"date": "2026-10-02", "title": "CoreWeave Bonds Slide!", "url": "https://y.com/b", "source": "T", "first_seen": "2026-10-02", "matched": []},  # 同標題
        {"date": "2026-10-03", "title": "Oracle debt deal", "url": "https://y.com/c", "source": "T", "first_seen": "2026-10-03", "matched": []},
        {"date": "2026-10-03", "title": "Oracle debt deal", "url": "", "source": "U", "first_seen": "2026-10-03", "matched": []},                   # 本批內同標題
    ]
    allv, added = EV.merge_events(existing, cands)
    assert [a["title"] for a in added] == ["Oracle debt deal"] and len(allv) == 2


def test_extract_candidates_from_ledger_ignores_seed_and_picks_a_link():
    ledger = {"facts": [
        {"origin": "seed", "claim": "Oracle data center financing", "detail": "", "sources": []},
        {"origin": "briefing", "claim": "Oracle data center financing falters", "detail": "", "first_seen": "2026-10-02",
         "sources": [{"source": "Bloomberg", "url": "", "published": "2026-10-01"}, {"source": "Reuters", "url": "https://r.com/x", "published": "2026-10-02"}]},
        {"origin": "briefing", "claim": "Sunny weather", "detail": "", "sources": []},
    ]}
    c = EV.extract_candidates(ledger)
    assert len(c) == 1 and c[0]["url"] == "https://r.com/x" and c[0]["date"] == "2026-10-01"


def test_event_store_roundtrip_and_latest(tmp_path):
    p = tmp_path / "e.jsonl"
    EV.append_events(p, [{"date": f"2026-10-{d:02d}", "title": f"t{d}", "first_seen": "x"} for d in range(1, 6)])
    ev = EV.load_events(p)
    assert [e["title"] for e in EV.latest(ev, 3)] == ["t5", "t4", "t3"]


# ---------------------------------------------------------------------------
# 內嵌 XBRL
# ---------------------------------------------------------------------------
IXH = """
<xbrli:context id="c1"><xbrli:entity/><xbrli:period><xbrli:instant>2026-06-30</xbrli:instant></xbrli:period></xbrli:context>
<xbrli:context id="c2"><xbrli:entity><xbrli:segment><xbrldi:explicitMember dimension="us-gaap:OtherCommitmentsAxis">nvda:AICloudPartnershipCommitmentsMember</xbrldi:explicitMember></xbrli:segment></xbrli:entity><xbrli:period><xbrli:instant>2026-06-30</xbrli:instant></xbrli:period></xbrli:context>
<xbrli:context id="c3"><xbrli:entity/><xbrli:period><xbrli:startDate>2026-04-01</xbrli:startDate><xbrli:endDate>2026-06-30</xbrli:endDate></xbrli:period></xbrli:context>
<ix:nonFraction name="us-gaap:OtherCommitment" contextRef="c2" scale="9" decimals="-8">36</ix:nonFraction>
<ix:nonFraction name="us-gaap:OtherCommitment" contextRef="c1" scale="9">100</ix:nonFraction>
<ix:nonFraction name="x:Neg" contextRef="c1" scale="6" sign="-">1,234</ix:nonFraction>
<ix:nonFraction name="x:Dash" contextRef="c3" scale="6">&#8212;</ix:nonFraction>
<ix:nonFraction name="x:Pct" contextRef="c3" scale="-2">36</ix:nonFraction>
"""


def test_ix_facts_scale_sign_dash_and_dimensions():
    fs = IX.facts(IXH, r"^(us-gaap:OtherCommitment|x:.*)$")
    by = {}
    for f in fs:
        by.setdefault(f["name"], []).append(f)
    assert IX.pick_instant(fs, "us-gaap:OtherCommitment", {"nvda:AICloudPartnershipCommitmentsMember"})["value"] == 36e9
    assert IX.pick_instant(fs, "us-gaap:OtherCommitment", set())["value"] == 100e9           # 無維度
    assert by["x:Neg"][0]["value"] == -1234e6
    assert by["x:Dash"][0]["value"] == 0.0 and by["x:Dash"][0]["start"] == "2026-04-01"
    assert by["x:Pct"][0]["value"] == pytest.approx(0.36)


# ---------------------------------------------------------------------------
# 背景利差與頁面
# ---------------------------------------------------------------------------
def test_spread_stats_position_and_year_ago():
    s = [("2025-10-14", 3.0), ("2026-01-01", 5.0), ("2026-06-01", 1.0), ("2026-10-14", 4.0)]
    st = spread_stats(s)
    assert st["latest"] == 4.0 and st["year_ago"] == 3.0 and st["year_ago_date"] == "2025-10-14"
    assert st["pos"] == pytest.approx(0.75)


def test_page_smoke():
    u = base_units()
    inds = M.compute_indicators(u)
    inds[11]["breached"] = True
    summary = M.summarize(inds)
    state = {"generated_at": "2026-10-16 07:40", "units": u}
    html = PG.build_page(state, inds, summary, [{"date": "2026-10-15", "title": "A <b> title", "source": "Reuters", "url": "https://r.com/x"}], 1)
    assert "12 條裡 <em>1</em> 條越線" in html
    assert 'id="i12"' in html
    for ch in ("一　借錢的人撐不撐得住", "二　市場怎麼定價", "三　錢怎麼繞回來", "四　AI 傷到借款人", "五　投資回不回得了本"):
        assert ch in html
    assert "A &lt;b&gt; title" in html                      # 標題已跳脫
    assert "事前登記" in html and "2026-10-16" in html
    assert 'name="robots"' not in html                       # 公開、可收錄


# ---------------------------------------------------------------------------
# 第二輪：純函式
# ---------------------------------------------------------------------------
def test_pik_series_cf_adds_interest_and_dividend(monkeypatch):
    gross = {"2026-03-31": 100.0, "2026-06-30": 120.0}
    interest = {"2026-03-31": 10.0, "2026-06-30": 12.0}
    div = {"2026-03-31": 2.0, "2026-06-30": 3.0}
    table = {R2.GROSS_TAG: gross, R2.INT_PIK: interest, R2.DIV_PIK: div}
    monkeypatch.setattr(R2.S, "rows", lambda facts, tag: tag)
    monkeypatch.setattr(R2.S, "single_quarters", lambda tag: table.get(tag))
    out = R2.pik_series_cf({}, R2.PIK_SPEC["ARCC"])
    assert [round(x["pct"], 2) for x in out] == [12.0, 12.5]
    out2 = R2.pik_series_cf({}, R2.PIK_SPEC["OBDC"])
    assert [round(x["pct"], 2) for x in out2] == [10.0, 10.0]


def test_pik_series_cf_requires_tags(monkeypatch):
    monkeypatch.setattr(R2.S, "rows", lambda facts, tag: tag)
    monkeypatch.setattr(R2.S, "single_quarters", lambda tag: None)
    with pytest.raises(RuntimeError):
        R2.pik_series_cf({}, R2.PIK_SPEC["ARCC"])


def _conc(member, bench, v, dt="2026-06-30"):
    return {"name": "us-gaap:ConcentrationRiskPercentage1", "value": v, "instant": dt, "end": dt,
            "dims": [("us-gaap:EquitySecuritiesByIndustryAxis", "x:" + member), ("us-gaap:ConcentrationRiskByBenchmarkAxis", "us-gaap:" + bench)]}


def test_software_share_uses_fair_value_and_latest_date():
    facts = [_conc("SoftwareSectorMember", "InvestmentOwnedBalancePrincipalAmountMember", 0.5),
             _conc("SoftwareSectorMember", "FairValueConcentrationRiskMember", 0.2),
             _conc("OtherMember", "FairValueConcentrationRiskMember", 0.8),
             _conc("SoftwareSectorMember", "FairValueConcentrationRiskMember", 0.9, "2026-03-31")]
    r = R2.software_share(facts, ["SoftwareSectorMember"])
    assert r["pct"] == pytest.approx(20.0) and r["asof"] == "2026-06-30" and r["n_industries"] == 2
    assert r["total_pct"] == pytest.approx(100.0)
    with pytest.raises(RuntimeError):
        R2.software_share(facts, ["NoSuchMember"])


@pytest.mark.parametrize("t,text,cost,fv", [
    ("OBDC", "two of our portfolio companies are on non-accrual, which represents 0.8% of our portfolio at fair value", None, 0.8),
    ("FSK", "% of Investments on Non-Accrual (based on fair value) 3.8% 3.1%", None, 3.8),
    ("MAIN", "comprised 1.1% and 4.0% of our total Investment Portfolio at fair value and cost", 4.0, 1.1),
    ("GBDC", "at cost and fair value were 2.9% and 1.9%", 2.9, 1.9),
    ("ARCC", "non-accrual status represented 2.4% of the total investments at amortized cost (or 1.4% at fair value)", 2.4, 1.4),
])
def test_parse_nonaccrual_text(t, text, cost, fv):
    r = R2.parse_nonaccrual(t, text)
    assert r["cost"] == cost and r["fv"] == fv


def test_parse_nonaccrual_arcc_xbrl_and_miss():
    ix = [{"name": R2.ARCC_XBRL[0], "instant": "2026-06-30", "dims": [], "value": 0.024},
          {"name": R2.ARCC_XBRL[1], "instant": "2026-06-30", "dims": [], "value": 0.014}]
    r = R2.parse_nonaccrual("ARCC", "沒有相關文字", ix)
    assert r["via"] == "XBRL" and r["cost"] == pytest.approx(2.4) and r["fv"] == pytest.approx(1.4)
    assert R2.parse_nonaccrual("GBDC", "文字改版了，找不到") is None


def _filing(acc, rd, na):
    return {"accession": acc, "report_date": rd, "filing_date": rd, "url": "https://x/" + acc, "nonaccrual": na}


def test_latest_nonaccrual_statuses():
    ok = R2.latest_nonaccrual([_filing("a2", "2026-06-30", {"cost": 1, "fv": 1}), _filing("a1", "2026-03-31", {"cost": 2, "fv": 2})])
    assert ok["status"] == "ok" and ok["accession"] == "a2"
    miss = R2.latest_nonaccrual([_filing("a2", "2026-06-30", None), _filing("a1", "2026-03-31", {"cost": 2, "fv": 2})])
    assert miss["status"] == "miss" and miss["report_date"] == "2026-03-31" and miss["miss_accession"] == "a2"
    none = R2.latest_nonaccrual([_filing("a2", "2026-06-30", None)])
    assert none["status"] == "none" and none["miss_accession"] == "a2"
    assert R2.latest_nonaccrual([])["status"] == "none"


def test_build_notices_once_per_filing_and_dep_change():
    bdc = {t: [_filing(t + "2", "2026-06-30", {"cost": 1, "fv": 1})] for t in R2.NONACCRUAL_BDCS}
    bdc["FSK"] = [_filing("fsk2", "2026-06-30", None), _filing("fsk1", "2026-03-31", {"cost": None, "fv": 3.0})]
    n1, notified = R2.build_notices(bdc, [], {})
    assert len(n1) == 1 and n1[0]["kind"] == "fetch" and "FSK" in n1[0]["title"] and notified["nonaccrual"] == {"fsk2": "FSK"}
    n2, notified2 = R2.build_notices(bdc, [], notified)
    assert n2 == [] and notified2 == notified                      # 同一份申報不重複通知
    dep = [{"t": "META", "name": "Meta", "old": 5.5, "new": 5.0, "accession": "m1", "report_date": "2026-12-31"}]
    n3, notified3 = R2.build_notices(bdc, dep, notified)
    assert len(n3) == 1 and n3[0]["kind"] == "change" and "5.5" in n3[0]["title"] and notified3["dep"] == {"m1": "META"}
    assert notified == {"nonaccrual": {"fsk2": "FSK"}}              # 不改動傳入的 notified


def test_notice_title_prefixes_and_alert_text():
    fetch = {"kind": "fetch", "title": "A 未抓到", "body": "內文 A"}
    change = {"kind": "change", "title": "B 年限變動", "body": "內文 B"}
    assert AL.notice_title([fetch]).startswith("資料抓取異常：")
    assert AL.notice_title([change]).startswith("資料變動：")
    assert AL.notice_title([fetch, change]).startswith("資料抓取異常／資料變動：")
    inds = M.compute_indicators(base_units())
    title, body = AL.alert_text([], inds, notices=[fetch])
    assert title.startswith("資料抓取異常") and "內文 A" in body


def test_cloud_ratio_table_matches_near_quarter_ends():
    rev = {"2025-09-30": 10.0, "2025-12-31": 12.0, "2026-03-31": 14.0, "2026-06-30": 16.0}
    capex = {"2025-09-29": 20.0, "2025-12-31": 24.0, "2026-03-30": 28.0, "2026-06-30": 32.0}
    t = R2.cloud_ratio_table(rev, capex)
    assert [round(r["ratio"], 2) for r in t["rows"]] == [0.5] * 4
    assert t["ttm"] == pytest.approx(52.0 / 104.0) and t["ttm_rev"] == 52.0 and t["ttm_capex"] == 104.0
    t2 = R2.cloud_ratio_table(rev, {"2026-06-30": 32.0})
    assert t2["ttm"] is None and t2["rows"][0]["ratio"] is None


def test_gpu_stats():
    v = R2.vast_stats([{"dph_total": 8.0, "num_gpus": 4}, {"dph_total": 5.0, "num_gpus": 2}, {"dph_total": 3.0, "num_gpus": 1}],
                      [{"dph_total": 16.0, "num_gpus": 4}])
    assert v["rentable_median"] == pytest.approx(2.5) and v["rentable_n"] == 3 and v["all_n"] == 4 and v["all_median"] == pytest.approx(2.75)
    assert R2.vast_stats([], []) is None
    types = [{"gpu_type": "H100", "num_gpus": 8, "hourly_price": 1600, "availability": [{"available": True}]},
             {"gpu_type": "H100", "num_gpus": 1, "hourly_price": 300, "availability": [{"available": False}]},
             {"gpu_type": "B200", "num_gpus": 8, "hourly_price": 4000, "availability": []}]
    sh = R2.shade_stats(types, ["H100"])
    assert sh["all_n"] == 2 and sh["avail_n"] == 1 and sh["avail_median"] == pytest.approx(2.0) and sh["all_median"] == pytest.approx(2.5)
    assert R2.shade_stats(types, ["A100"]) is None


def test_upsert_gpu_rows_replaces_same_day_and_sorts():
    lines = [json.dumps({"date": "2026-10-16", "vast": 1}), json.dumps({"date": "2026-10-15", "vast": 0})]
    out = R2.upsert_gpu_rows(lines, R2.gpu_row("2026-10-16", {"H100": {}}, None))
    rows = [json.loads(x) for x in out]
    assert [r["date"] for r in rows] == ["2026-10-15", "2026-10-16"] and rows[1]["vast"] == {"H100": {}}


@pytest.mark.parametrize("txt,y", [("P6Y", 6.0), ("P5Y6M", 5.5), ("six years", 6.0), ("5.5", 5.5), ("4 years", 4.0), ("abc", None)])
def test_parse_years(txt, y):
    assert R2.parse_years(txt) == y


def test_server_life_and_dep_changed():
    dims = lambda *ms: [("us-gaap:PropertyPlantAndEquipmentByTypeAxis", "x:" + m) for m in ms]  # noqa: E731
    nn = [{"text": "P6Y", "dims": dims("ServerEquipmentMember"), "instant": "2025-12-31", "end": "2025-12-31"},
          {"text": "P3Y", "dims": dims("ServerEquipmentMember", "MinimumMember"), "instant": "2025-12-31", "end": "2025-12-31"},
          {"text": "P4Y", "dims": dims("ServerEquipmentMember"), "instant": "2024-12-31", "end": "2024-12-31"}]
    assert R2.server_life(nn, ["ServerEquipmentMember"]) == {"years": 6.0, "asof": "2025-12-31"}
    assert R2.server_life(nn, ["OtherMember"]) is None
    table = [{"t": "AAA", "name": "A 公司", "years": 6.0}, {"t": "BBB", "name": "B 公司", "years": 5.5}]
    ch = R2.dep_changed(table, {"AAA": {"years": 6.0, "accession": "a"}, "BBB": {"years": 5.0, "accession": "b", "report_date": "2026-12-31"}})
    assert len(ch) == 1 and ch[0]["t"] == "BBB" and ch[0]["old"] == 5.5 and ch[0]["new"] == 5.0


def test_weekly_index_and_drawdown():
    stock = [(f"2026-01-{i:02d}", 100.0 + i) for i in range(1, 21)]
    bench = [(d, 200.0) for d, _ in stock]
    w = R2.weekly_index(stock, bench, window=20, step=5)
    assert w[0] == ["2026-01-01", 100.0, 100.0] and w[-1][0] == "2026-01-20" and w[-1][2] == 100.0
    assert R2.own_drawdown_1y([("a", 100.0), ("b", 80.0), ("c", 90.0)]) == pytest.approx(-10.0)
    assert R2.own_drawdown_1y([("a", 1.0)]) is None


def test_cn_date_helper():
    assert P2._cn_date("May 31, 2031") == "2031-05-31"
    assert P2._cn_date("October 2030") == "2030 年 10 月"
    assert P2._cn_date("未知") == "未知"


def test_every_threshold_has_type_and_why():
    for i in range(1, 13):
        typ, short, long = PG.THRESH_WHY[i]
        assert typ in ("結構線", "經驗值") and short.strip() and long.strip()
        assert i in PG.METHOD_ROWS
    assert [PG.THRESH_WHY[i][0] for i in (1, 2, 3, 6)] == ["結構線"] * 4
    assert [PG.THRESH_WHY[i][0] for i in (4, 5, 7, 8, 9, 10, 11, 12)] == ["經驗值"] * 8


def test_page_round2_blocks_degrade_without_data():
    """第二輪來源全部沒有資料時，頁面仍能產出，且每個區塊給出「尚無可用值」而不是丟例外。"""
    u = base_units()
    inds = M.compute_indicators(u)
    html = PG.build_page({"generated_at": "2026-10-16 07:40", "units": u}, inds, M.summarize(inds), [], 0)
    for key in ("軟體業股價（IGV）對 QQQ", "BDC 實物付息", "BDC 的軟體業占比", "BDC 不計息貸款", "雲端營收 ÷ 資本支出", "GPU 租價", "伺服器折舊年限", "OpenAI 曝險"):
        assert key in html
    assert "為什麼是這個數字" in html and "結構線" in html and "經驗值" in html
    assert 'href="/market/"' in html


def test_page_from_committed_state_has_links_and_blocks():
    st = B.load_state()
    if not st or "croi:AWS" not in st["units"]:
        pytest.skip("尚無第二輪的 state")
    inds = M.compute_indicators(st["units"])
    html = PG.build_page(st, inds, M.summarize(inds), [], 0, [], [])
    assert html.count("https://www.sec.gov/Archives/edgar/data/") >= 30         # 申報檔連結
    assert "data.sec.gov/api/xbrl/companyfacts/" in html and "fred.stlouisfed.org/series/" in html
    assert "Broadcom" in html and "尚未起租" in html and "CoreWeave 客戶集中度" in html
    assert 'data-chart="igv"' in html and 'data-chart="cloud_roi"' in html


# ---------------------------------------------------------------------------
# 負債公允價值 ÷ 帳面價值（第一區補充，只顯示）
# ---------------------------------------------------------------------------
def dfact(name, v, end, **axes):
    """合成內嵌 XBRL 事實。axes：軸名=成員名（不含前綴）。"""
    return {"name": "us-gaap:" + name, "value": float(v), "start": None, "end": None, "instant": end,
            "dims": [["us-gaap:" + a, "x:" + m] for a, m in axes.items()]}


def dfiling(acc, report, filed, facts, text_base=None, form="10-Q"):
    return {"accession": acc, "form": form, "report_date": report, "filing_date": filed, "url": "https://sec/" + acc, "facts": facts, "text_base": text_base}


def test_meta_principal_two_phrasings():
    a = "As of June 30, 2025, we had outstanding long-term debt in the form of senior unsecured notes for an aggregate principal amount of $29.0 billion, which mature"
    b = "As of June 30, 2026, we had $84.00 billion aggregate principal amount of Notes outstanding, which mature"
    assert R2.meta_principal(a) == 29.0e9 and R2.meta_principal(b) == 84.0e9
    assert R2.meta_principal("沒有這段文字") is None


def test_dfv_keep_drops_unneeded_facts():
    keep = lambda t, f: R2.dfv_keep(t, f)  # noqa: E731
    assert keep("AMZN", dfact("LongTermDebt", 1, "2026-06-30"))
    assert not keep("AMZN", dfact("LongTermDebt", 1, "2026-06-30", LongtermDebtTypeAxis="SeniorNotesMember", DebtInstrumentAxis="A2014"))
    assert keep("META", dfact("LongTermDebtFairValue", 1, "2026-06-30", LongtermDebtTypeAxis="SeniorNotesMember",
                              FairValueByMeasurementBasisAxis="E", FairValueByFairValueHierarchyLevelAxis="L2"))
    assert not keep("CRWV", dfact("DebtInstrumentCarryingAmount", 1, "2026-06-30", LongtermDebtTypeAxis="LineOfCreditMember", DebtInstrumentAxis="DDTL"))
    assert keep("CRWV", dfact("DebtInstrumentCarryingAmount", 1, "2026-06-30", LongtermDebtTypeAxis="SeniorNotesMember", DebtInstrumentAxis="A2030SeniorNotesMember"))
    nf = dfact("LongTermDebt", 1, "2026-06-30")
    nf["instant"] = None
    assert not keep("AMZN", nf)                     # 期間事實不留


def test_dfv_amzn_orcl_meta_googl_formulas():
    sn = dict(LongtermDebtTypeAxis="SeniorNotesMember")
    amzn = [dfiling("a1", "2026-06-30", "2026-07-31", [dfact("LongTermDebtFairValue", 123.8e9, "2026-06-30", **sn), dfact("LongTermDebt", 133.0e9, "2026-06-30"),
                                                       dfact("LongTermDebt", 132.1e9, "2026-06-30", **sn)])]
    r = R2.dfv_lines("AMZN", amzn)["main"][0]
    assert r["ratio"] == pytest.approx(123.8 / 133.0) and r["via"] == "XBRL"            # 分母是無維度的長期債面值合計
    orcl = [dfiling("o1", "2026-08-31", "2026-09-10", [
        dfact("DebtInstrumentFairValue", 105.7e9, "2026-08-31", LongtermDebtTypeAxis="SeniorNotesAndOtherBorrowingsMember", FairValueByFairValueHierarchyLevelAxis="L2"),
        dfact("DebtInstrumentCarryingAmount", 125.0e9, "2026-08-31", LongtermDebtTypeAxis="SeniorNotesAndOtherLongTermBorrowingsMember"),
        dfact("DebtInstrumentCarryingAmount", 5.0e9, "2026-08-31", CreditFacilityAxis="CommercialPaperMember")])]
    assert R2.dfv_lines("ORCL", orcl)["main"][0]["ratio"] == pytest.approx(105.7 / 125.0)
    fvm = dfact("LongTermDebtFairValue", 55.94e9, "2026-03-31", LongtermDebtTypeAxis="SeniorNotesMember")
    meta_x = [dfiling("m1", "2026-06-30", "2026-07-30", [dict(fvm, value=79.75e9, instant="2026-06-30"), dfact("DebtInstrumentCarryingAmount", 84e9, "2026-06-30")])]
    meta_t = [dfiling("m2", "2026-03-31", "2026-04-30", [fvm], text_base=59.0e9)]
    assert R2.dfv_lines("META", meta_x)["main"][0]["ratio"] == pytest.approx(79.75 / 84) and R2.dfv_lines("META", meta_x)["main"][0]["via"] == "XBRL"
    rt = R2.dfv_lines("META", meta_t)["main"][0]
    assert rt["ratio"] == pytest.approx(55.94 / 59.0) and rt["via"] == "XBRL＋文字"       # 沒有標籤的季度用文字補本金
    g_tot = [dfiling("g1", "2026-06-30", "2026-07-23", [dfact("LongTermDebtFairValue", 94.9e9, "2026-06-30"), dfact("DebtInstrumentCarryingAmount", 101.085e9, "2026-06-30"),
                                                        dfact("DebtInstrumentCarryingAmount", 2e9, "2026-06-30", DebtInstrumentAxis="A2016NotesMember")])]
    assert R2.dfv_lines("GOOGL", g_tot)["main"][0]["ratio"] == pytest.approx(94.9 / 101.085)
    g_mem = [dfiling("g0", "2024-09-30", "2024-10-30", [dfact("LongTermDebtFairValue", 9.5e9, "2024-09-30"),
                                                        dfact("DebtInstrumentCarryingAmount", 12e9, "2024-09-30", DebtInstrumentAxis="A20162020NotesMember")])]
    assert R2.dfv_lines("GOOGL", g_mem)["main"][0]["ratio"] == pytest.approx(9.5 / 12)   # 沒有合計標籤時加總各票據


def test_dfv_missing_value_is_none_not_zero_and_never_guessed():
    f = [dfiling("a1", "2026-06-30", "2026-07-31", [dfact("LongTermDebt", 133e9, "2026-06-30")])]      # 只有分母
    r = R2.dfv_lines("AMZN", f)["main"][0]
    assert r["ratio"] is None and r["fv"] is None and r["base"] is None
    conflict = [dfiling("a1", "2026-06-30", "2026-07-31", [dfact("LongTermDebt", 133e9, "2026-06-30"), dfact("LongTermDebt", 134e9, "2026-06-30"),
                                                           dfact("LongTermDebtFairValue", 120e9, "2026-06-30", LongtermDebtTypeAxis="SeniorNotesMember")])]
    assert R2.dfv_lines("AMZN", conflict)["main"][0]["ratio"] is None           # 同一時點兩個不同值，不猜


def test_dfv_prior_year_column_fills_a_missing_part_from_a_single_filing():
    sn = dict(LongtermDebtTypeAxis="SeniorNotesMember")
    k = dfiling("k", "2025-12-31", "2026-03-02", [
        dfact("DebtInstrumentFairValue", 3.5e9, "2025-12-31", **sn),
        dfact("DebtInstrumentFairValue", 2.5e9, "2025-12-31", DebtInstrumentAxis="A2031ConvertibleSeniorNotesMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 2.0e9, "2025-12-31", DebtInstrumentAxis="A2030SeniorNotesMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 1.75e9, "2025-12-31", DebtInstrumentAxis="A2031SeniorNotesMember", **sn)], form="10-K")
    q = dfiling("q", "2026-06-30", "2026-08-12", [          # 上年底欄：2031 票據改了成員名稱，可轉債本金只在這份裡
        dfact("DebtInstrumentCarryingAmount", 1.75e9, "2025-12-31", DebtInstrumentAxis="A20319.00SeniorNotesMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 2.588e9, "2025-12-31", DebtInstrumentAxis="A2031ConvertibleSeniorNotesMember", LongtermDebtTypeAxis="ConvertibleDebtMember"),
        dfact("DebtInstrumentFairValue", 10.0e9, "2026-06-30", DebtInstrumentAxis="A20329.625SeniorNotesMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 2.0e9, "2026-06-30", DebtInstrumentAxis="A2030SeniorNotesMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 1.75e9, "2026-06-30", DebtInstrumentAxis="A20319.00SeniorNotesMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 2.75e9, "2026-06-30", DebtInstrumentAxis="A20319.75SeniorNotesMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 1.25e9, "2026-06-30", DebtInstrumentAxis="A20329.625SeniorNotesMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 2.0e9, "2026-06-30", DebtInstrumentAxis="A2032EURSeniorNotesMember", **sn),            # 歐元面額
        dfact("DebtInstrumentCarryingAmount", 2.279e9, "2026-06-30", DebtInstrumentAxis="A2032EURSeniorNotesMember", RecourseStatusAxis="RecourseMember", **sn),
        dfact("DebtInstrumentCarryingAmount", 0.171e9, "2026-06-30", DebtInstrumentAxis="ConvertiblePromissoryNotesMember", LongtermDebtTypeAxis="ConvertibleDebtMember"),
    ])
    lines = R2.dfv_lines("CRWV", [k, q])
    ks, kc = lines["senior"][0], lines["conv"][0]
    assert ks["ratio"] == pytest.approx(3.5 / 3.75)                    # 2031 票據只算自己那份申報的一次，不被上年底欄的新成員名稱重複計入
    assert kc["ratio"] == pytest.approx(2.5 / 2.588)                   # 分子取自 10-K、分母取自較晚的 10-Q
    qs = lines["senior"][1]
    assert qs["base"] == pytest.approx(2.0e9 + 1.75e9 + 2.75e9 + 1.25e9 + 2.279e9)   # 歐元票據取美元換算值，不取歐元面額
    assert qs["ratio"] == pytest.approx(10.0 / 10.029)
    assert lines["conv"][1]["ratio"] is None                          # 該季沒有可轉債公允價值


def test_dfv_lines_cf_uses_companyfacts_tags():
    def rowsx(vals):
        return {"units": {"USD": [{"end": e, "val": v, "form": "10-Q", "filed": "2026-08-01"} for e, v in vals]}}
    facts = {"facts": {"us-gaap": {"LongTermDebtFairValue": rowsx([("2026-03-31", 36.6e9), ("2026-06-30", 36.5e9)]),
                                   "LongTermDebt": rowsx([("2026-03-31", 40.262e9), ("2026-06-30", 40.294e9)])}}}
    metas = [{"report_date": "2026-06-30", "form": "10-K", "accession": "m2", "url": "u2", "filing_date": "2026-07-29"},
             {"report_date": "2026-03-31", "form": "10-Q", "accession": "m1", "url": "u1", "filing_date": "2026-04-29"},
             {"report_date": "2025-12-31", "form": "10-Q", "accession": "m0", "url": "u0", "filing_date": "2026-01-28"}]
    rows = R2.dfv_lines_cf(facts, metas)["main"]
    assert [r["end"] for r in rows] == ["2025-12-31", "2026-03-31", "2026-06-30"]
    assert rows[2]["ratio"] == pytest.approx(36.5 / 40.294) and rows[0]["ratio"] is None


def _units_with_dfv(newest_missing=False):
    def row(end, r, acc):
        return {"end": end, "form": "10-Q", "accession": acc, "url": "https://sec/" + acc, "fv": None if r is None else r * 100, "base": None if r is None else 100.0,
                "ratio": r, "via": None if r is None else "XBRL"}
    u = {}
    for t, rs in {"MSFT": [0.93, 0.92, 0.91], "GOOGL": [0.90, 0.93, 0.94], "AMZN": [0.89, 0.92, 0.93], "META": [0.97, 0.95, 0.95],
                  "ORCL": [0.90, 0.89, None if newest_missing else 0.846]}.items():
        u[f"dfv:{t}"] = {"data": {"lines": {"main": [row(f"2026-0{3 + 3 * i}-30", r, f"{t}{i}") for i, r in enumerate(rs)]}}, "fetched": "2026-10-16", "stale": False}
    u["dfv:CRWV"] = {"data": {"lines": {"senior": [row("2026-03-31", None, "c0"), row("2026-06-30", 0.997, "c1")],
                                        "conv": [row("2026-03-31", None, "c0"), row("2026-06-30", 1.138, "c1")]}}, "fetched": "2026-10-16", "stale": False}
    return u


def test_dfv_latest_view_carries_last_value_when_newest_missing():
    ok = R2.dfv_latest_view([{"end": "a", "ratio": 0.9}, {"end": "b", "ratio": 0.8}])
    assert ok == {"value": 0.8, "end": "b", "carried": False}
    miss = R2.dfv_latest_view([{"end": "a", "ratio": 0.9}, {"end": "b", "ratio": None}])
    assert miss["value"] == 0.9 and miss["end"] == "a" and miss["carried"] is True and miss["missing_end"] == "b"
    assert R2.dfv_latest_view([{"end": "a", "ratio": None}])["value"] is None and R2.dfv_latest_view([])["value"] is None


def test_dfv_misses_and_notice_once_per_filing():
    assert R2.dfv_misses(_units_with_dfv()) == []                       # CoreWeave 2026-03 那季沒揭露，但最新一份有值，不通知
    u = _units_with_dfv(newest_missing=True)
    miss = R2.dfv_misses(u)
    assert len(miss) == 1 and miss[0]["t"] == "ORCL" and miss[0]["accession"] == "ORCL2" and miss[0]["last"] == "2026-06-30"
    bdc = {t: [_filing(t + "2", "2026-06-30", {"cost": 1, "fv": 1})] for t in R2.NONACCRUAL_BDCS}
    n1, notified = R2.build_notices(bdc, [], {}, miss)
    assert len(n1) == 1 and n1[0]["kind"] == "fetch" and "Oracle" in n1[0]["title"] and "負債公允價值" in n1[0]["title"] and notified["dfv"] == {"ORCL2": "ORCL"}
    assert AL.notice_title(n1).startswith("資料抓取異常：")
    n2, notified2 = R2.build_notices(bdc, [], notified, miss)
    assert n2 == [] and notified2 == notified                           # 同一份申報檔只通知一次
    assert R2.build_notices(bdc, [], {})[0] == []                       # 不傳第四個參數的舊呼叫方式照舊


def test_dfv_sentence_picks_lowest_of_five_and_range_of_rest():
    views = {t: R2.dfv_latest_view(((_units_with_dfv()[f"dfv:{t}"])["data"]["lines"]["main"])) for t in R2.DFV_PEERS}
    s = P2.dfv_sentence(views)
    assert "Oracle" in s and "0.846" in s and "0.91 至 0.95" in s and "4 家" in s
    assert P2.dfv_sentence({"MSFT": views["MSFT"]}) == ""


def test_dfv_block_renders_table_chart_and_carried_badge():
    ch = P2.Charts()
    html = P2.dfv_block(_units_with_dfv(), ch)
    assert "負債公允價值 ÷ 帳面價值（近 8 季）" in html and "只顯示" in html and 'data-chart="dfv"' in html
    assert "CoreWeave 高收益優先票據" in html and "CoreWeave 可轉換優先票據" in html and "該季未揭露" in html
    assert "0.846" in html and "利率上升" in html and "信用要求更高" in html and "日 沿用" not in html and "-30 沿用" not in html
    assert ch.data["dfv"]["ref"] == 1.0 and len(ch.data["dfv"]["series"]) == 6 and ch.data["dfv"]["labels"][-1] == "最新"
    html2 = P2.dfv_block(_units_with_dfv(newest_missing=True), P2.Charts())
    assert "申報檔本期未抓到，顯示上次值（2026-06-30）" in html2 and "2026-06-30 沿用" in html2
    assert "資料尚無可用值" in P2.dfv_block({}, P2.Charts())


def test_page_has_dfv_block_in_chapter_one_and_cds_note_without_numbers():
    u = base_units()
    u.update(_units_with_dfv())
    inds = M.compute_indicators(u)
    html = PG.build_page({"generated_at": "2026-10-16 07:40", "units": u}, inds, M.summarize(inds), [], 0)
    a, b = html.index("負債公允價值 ÷ 帳面價值"), html.index("市場怎麼定價")
    assert html.index("借錢的人撐不撐得住") < a < b                       # 在第一區裡、第二區之前
    assert "為什麼沒有個別公司的 CDS 與債券價格" in html and "FINRA TRACE" in html and "DTCC" in html
    assert "第一區最後的負債公允價值表" in html
    assert "Blue Owl" not in html[a:b]                                 # 不放 Blue Owl
