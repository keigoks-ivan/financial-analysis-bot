#!/usr/bin/env python3
"""NFCI 紅燈減半往前測影子線（scripts/update_nfci_forward.py）的單元測試。

對應事前登記（v7-backtest docs/NFCI_Forward_Prereg.md）第十節：
  顏色判定（含相等算綠）、週三公布到週五生效、台股週四休市順延、股災切分與區間最大跌幅、
  判準第 1 條的無條件進位；加上結構檢查（強制永遠綠＝與實單逐日一致，強制永遠紅＝每腿目標
  為實單目標 × 0.5）。全部不打網路：價格、現金利率、NFCI 版本都用合成資料。
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import update_nfci_forward as nf  # noqa: E402
import update_long_track_w52_adaptive as w52  # noqa: E402
import build_live_scoreboard as lsb  # noqa: E402
import build_long_track_index as bli  # noqa: E402


# ── 顏色判定 ────────────────────────────────────────────────────────────
def test_color_higher_is_red_equal_is_green():
    assert nf.nfci_color("-0.49", "-0.55") == "red"
    assert nf.nfci_color("-0.55", "-0.49") == "green"
    assert nf.nfci_color("-0.50", "-0.50") == "green"       # 相等算綠


def test_color_compares_after_rounding_to_two_decimals():
    # 三位小數原值不同，取兩位小數後相等 → 綠
    assert nf.nfci_color("-0.494", "-0.486") == "green"
    # 登記文件的例子：10-14 版最後一筆 10-02 為 -0.494、四週前 09-04 為 -0.545 → -0.49 對 -0.55，紅
    assert nf.hundredths("-0.494") == -49
    assert nf.hundredths("-0.545") == -55                    # 與 10-17 回測相同的 round(float, 2)
    assert nf.nfci_color("-0.494", "-0.545") == "red"


VINTAGE_1014 = (
    "observation_date,NFCI_20261014\n"
    "2026-08-28,-0.549\n2026-09-04,-0.545\n2026-09-11,-0.536\n"
    "2026-09-18,-0.524\n2026-09-25,-0.510\n2026-10-02,-0.494\n"
)


def test_release_from_real_1014_vintage():
    obs = nf.parse_vintage(VINTAGE_1014)
    r = nf.release_from_vintage("2026-10-14", obs, "2026-10-18", "起始版本")
    assert (r["last_obs_date"], r["value_2dp"]) == ("2026-10-02", "-0.49")
    assert (r["value_4w_ago_date"], r["value_4w_ago_2dp"]) == ("2026-09-04", "-0.55")
    assert r["color"] == "red"


def test_four_weeks_ago_is_inclusive_and_falls_back_to_earlier_obs():
    # 最後一筆 10-02，往前 28 天＝09-04，剛好有值（含）→ 用 09-04
    obs = nf.parse_vintage(VINTAGE_1014)
    assert nf.release_from_vintage("2026-10-14", obs, "x", "s")["value_4w_ago_date"] == "2026-09-04"
    # 09-04 沒有值 → 取它之前最後一筆（08-28）
    obs2 = [o for o in obs if o[0] != "2026-09-04"]
    assert nf.release_from_vintage("2026-10-14", obs2, "x", "s")["value_4w_ago_date"] == "2026-08-28"


def test_parse_vintage_skips_missing_values():
    txt = "observation_date,NFCI_X\n2026-01-02,-0.1\n2026-01-09,.\n2026-01-16,\n2026-01-23,-0.2\n"
    assert nf.parse_vintage(txt) == [("2026-01-02", "-0.1"), ("2026-01-23", "-0.2")]
    with pytest.raises(ValueError):
        nf.parse_vintage("date,value\n2026-01-02,1\n")


# ── 週三公布 → 週四收盤調整 → 週五起生效；週四休市順延 ─────────────────────────────
REL = [{"release_date": "2026-10-14", "color": "red"}, {"release_date": "2026-10-21", "color": "green"}]


def test_release_applies_from_thursday_not_wednesday():
    f = lambda d: (nf.release_for_day(REL, d) or {}).get("color")   # noqa: E731
    assert f("2026-10-14") is None                # 公布當天（還在用上一版，這裡沒有）
    assert f("2026-10-15") == "red"               # 10-14 版週四起適用
    assert f("2026-10-21") == "red"               # 新一版公布當天仍用舊版
    assert f("2026-10-22") == "green"             # 10-21 版：週四收盤調整
    assert f("2026-10-23") == "green"


def test_adjust_thursday_effective_friday_us_calendar():
    days = ["2026-10-19", "2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-26"]
    assert nf.adjust_date("2026-10-21", days) == "2026-10-22"       # 週四收盤調整
    assert nf.effective_date("2026-10-21", days) == "2026-10-23"    # 週五起生效


def test_thursday_closed_defers_to_next_trading_day():
    # 台股 2026-10-22（週四）休市：調整順延到週五，週一起生效
    days_tw = ["2026-10-19", "2026-10-20", "2026-10-21", "2026-10-23", "2026-10-26"]
    assert nf.adjust_date("2026-10-21", days_tw) == "2026-10-23"
    assert nf.effective_date("2026-10-21", days_tw) == "2026-10-26"
    # 同一條「公布日 + 1 天 <= 交易日」的式子：週四不在日曆裡，週五拿到新顏色
    assert nf.release_for_day(REL, "2026-10-23")["color"] == "green"


def test_due_wednesdays_wait_until_thursday():
    assert nf.due_wednesdays("2026-10-14", date(2026, 10, 14)) == []
    assert nf.due_wednesdays("2026-10-14", date(2026, 10, 15)) == ["2026-10-14"]
    assert nf.due_wednesdays("2026-10-14", date(2026, 10, 22)) == ["2026-10-14", "2026-10-21"]


# ── 股災切分與區間最大跌幅 ──────────────────────────────────────────────────
def test_drop_threshold_is_integer_bp_strictly_over_1000():
    assert nf.drop_bp(100.0, 90.0) == 1000
    assert nf.find_crashes([100.0, 90.0]) == []               # 剛好 10%：不算
    assert len(nf.find_crashes([100.0, 89.99])) == 1          # 10.01%：算
    assert nf.find_crashes([100.0, 90.004]) == []             # 9.996% 四捨五入成 1000：不算


def test_crash_episode_split_recovery_and_open_episode():
    closes = [100, 105, 110, 99, 98, 105, 111, 120, 100, 90]
    eps = nf.find_crashes(closes)
    assert len(eps) == 2
    first, second = eps
    assert (first["peak_i"], first["end_i"], first["recovered"]) == (2, 6, True)
    assert first["trough_bp"] == nf.drop_bp(110, 98)
    # 111 回到高點後，新高點是 111，接著創新高 120；從 120 起第二次股災還沒回到高點，算到最後一天
    assert (second["peak_i"], second["end_i"], second["recovered"]) == (7, 9, False)
    assert second["trough_bp"] == 2500


def test_small_dip_below_threshold_resets_nothing():
    closes = [100, 95, 99, 104, 100, 94, 98, 110]
    assert nf.find_crashes(closes) == []                      # 最深只有約 9.6%（104 → 94）


def test_recovery_at_exactly_the_old_high_closes_the_episode():
    eps = nf.find_crashes([100, 88, 95, 100, 120, 100])
    assert [(e["peak_i"], e["end_i"], e["recovered"]) for e in eps] == [(0, 3, True), (4, 5, False)]


def test_interval_max_drawdown_runs_from_peak_day_nav():
    nav = [100, 101, 102, 95, 93, 99, 103]
    # 區間 [2, 4]：從第 2 天的淨值 102 起算，最低 93 → 882 bp
    assert nf.interval_depth_bp(nav, 2, 4) == int(round((102 - 93) / 102 * 10000))
    # 區間內淨值先創高（104），再下跌：滾動高點抬高，從 104 算
    nav2 = [100, 101, 104, 98]
    assert nf.interval_depth_bp(nav2, 0, 3) == int(round((104 - 98) / 104 * 10000))
    # 區間只有一天：沒有跌幅
    assert nf.interval_depth_bp(nav, 3, 3) == 0


def test_crash_report_benefit_is_live_depth_minus_shadow_depth():
    dates = [f"2026-11-{d:02d}" for d in range(2, 12)]
    closes = [100, 100, 95, 85, 90, 100, 101, 101, 101, 101]
    nav_live = [100, 100, 95, 85, 90, 100, 101, 101, 101, 101]
    nav_shadow = [100, 100, 97.5, 92.5, 95, 100, 100.5, 100.5, 100.5, 100.5]
    rep = nf.crash_report(dates, closes, nav_live, nav_shadow)
    assert len(rep) == 1
    e = rep[0]
    assert (e["peak_date"], e["end_date"], e["recovered"]) == ("2026-11-02", "2026-11-07", True)
    assert e["live_depth_bp"] == 1500 and e["shadow_depth_bp"] == 750 and e["benefit_bp"] == 750
    assert isinstance(e["benefit_bp"], int)


# ── 判準 ────────────────────────────────────────────────────────────────
def test_required_crashes_is_ceiling_of_two_thirds():
    assert [nf.required_crashes(n) for n in range(0, 11)] == [0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7]
    assert all(nf.required_crashes(n) == math.ceil(2 * n / 3) for n in range(0, 400))


def test_crash_rule_threshold_300bp_inclusive_and_count():
    assert nf.crash_pass([300, 300, 0]) is True               # 3 次要 2 次，300 含
    assert nf.crash_pass([299, 300, 0]) is False
    assert nf.crash_pass([350, 340, 330, 0]) is True          # 4 次要 3 次
    assert nf.crash_pass([350, 340, 0, 0]) is False
    assert nf.crash_pass([]) is False


def test_calmar_rule_uses_integer_cross_multiplication():
    # 影子 950/1000 = 0.95，實單 1000/1000 = 1.0：剛好 0.95 倍 → 過（邊界含）
    assert nf.calmar_pass(950, 1000, 1000, 1000) is True
    assert nf.calmar_pass(949, 1000, 1000, 1000) is False
    # 影子回撤較淺：同樣報酬、回撤 900 vs 1000 → Calmar 較高
    assert nf.calmar_pass(1000, 900, 1000, 1000) is True
    assert nf.calmar_pass(1000, 0, 1000, 1000) is None


def test_trade_rule_two_point_five_times():
    assert nf.adj_pass(25, 10) is True
    assert nf.adj_pass(26, 10) is False
    assert nf.adj_pass(0, 0) is True
    assert nf.adj_pass(3, 0) is None


def test_decision_status():
    both3 = {"us": 3, "tw": 4}
    assert nf.decision_status("2029-10-18", both3) == "累積中"
    assert nf.decision_status("2029-10-19", both3) == "可判定"
    assert nf.decision_status("2029-10-19", {"us": 3, "tw": 2}).startswith("股災次數不足")
    assert nf.decision_status("2031-10-19", {"us": 3, "tw": 2}) == "已到最晚判定日"
    assert nf.decision_status("2029-10-19", {"us": 5}).startswith("股災次數不足")   # 台股還沒有資料


# ── 執行層：實單函式與整數空間的獨立算法一致 ─────────────────────────────────────
def _ref_next_exec_bp(held_bp: int, target_bp: int, clamp_bp: int) -> int:
    """整數基點空間的獨立寫法：20pp 門檻、10pp 格（五五入取偶，與 Python round 同）、clamp。"""
    cur = min(held_bp, clamp_bp)
    if abs(target_bp - cur) >= 2000:
        q, r = divmod(target_bp, 1000)
        if r > 500 or (r == 500 and q % 2 == 1):
            q += 1
        cur = min(q * 1000, clamp_bp)
    return cur


@pytest.mark.parametrize("clamp_pp", [50.0, 75.0])
def test_live_next_exec_matches_integer_space_reference(clamp_pp):
    clamp_bp = int(clamp_pp * 100)
    for held_pp in range(0, int(clamp_pp) + 1, 10):
        for target_bp in range(0, 7501, 5):                    # 實單目標 0.1pp 解析，減半後是 5bp 的倍數
            got = w52.next_exec(float(held_pp), target_bp / 100.0, clamp_pp)
            assert int(round(got * 100)) == _ref_next_exec_bp(held_pp * 100, target_bp, clamp_bp), (held_pp, target_bp)


# ── 結構檢查（合成資料；實單函式原樣使用）─────────────────────────────────────────
def _synthetic(n_days=60, start_idx=5, rule=None):
    """兩腿（台股式現金 1%）合成實單紀錄與價格。目標在 0..50 之間擺動，含閘門關閉的一段。"""
    legs = ["0050", "2330"]
    d0 = date(2026, 10, 12)
    dates, d = [], d0
    while len(dates) < n_days:
        if d.weekday() < 5:
            dates.append(d.isoformat())
        d += timedelta(days=1)
    hist, px = [], {t: {} for t in legs}
    for i, ds in enumerate(dates):
        rec = {"date": ds, "source": "live", "tickers": {}}
        for k, t in enumerate(legs):
            gate = not (20 <= i <= 28)
            raw = 0.55 + 0.45 * abs(math.sin(i / 5.0 + k))
            final = round((50.0 if gate else 0.0) * min(1.0, raw), 1)
            rec["tickers"][t] = {"gate": gate, "raw_ratio": raw, "final_pct": final,
                                 **({"rule": rule} if rule else {})}
            px[t][ds] = 100.0 * (1.0 + 0.004 * math.sin(i / 3.0 + k) + 0.0015 * i) * (0.88 if 30 <= i < 34 else 1.0)
        hist.append(rec)
    return legs, dates, hist, px


def _sim(force=None, release_fn=None, start_idx=5, **kw):
    legs, dates, hist, px = _synthetic(**kw)
    mkt = next(m for m in lsb.MARKETS if m["key"] == "tw")
    px_dates = {t: sorted(px[t]) for t in legs}
    rf = release_fn or (lambda d: None)
    return nf.simulate_market(mkt, hist, dates[start_idx], rf, px, px_dates, None, None, force_color=force), dates, hist


def test_force_green_is_identical_to_live_every_day():
    sim, dates, hist = _sim(force="green")
    assert sim["ex_shadow"] == sim["ex_live"]
    assert sim["nav_shadow"] == sim["nav_live"]
    assert not sim["gaps"]
    for t in sim["legs"]:
        assert sim["target_shadow"][t][1:] == sim["target_live"][t][1:]


def test_force_red_halves_every_leg_target():
    sim, dates, hist = _sim(force="red")
    for t in sim["legs"]:
        for a, b in zip(sim["target_live"][t][1:], sim["target_shadow"][t][1:]):
            assert 2 * int(round(b * 100)) == int(round(a * 100))
    # 起始日當天現持＝實單現持；之後兩條線開始分開
    assert all(sim["ex_shadow"][t][0] == sim["ex_live"][t][0] for t in sim["legs"])
    assert sim["ex_shadow"] != sim["ex_live"]


def test_start_day_holdings_equal_live_and_nav_base_is_100():
    sim, *_ = _sim(force="red")
    assert sim["nav_live"][0] == 100.0 and sim["nav_shadow"][0] == 100.0


def test_color_change_adjusts_on_thursday_and_earns_from_friday():
    """週三公布紅燈 → 週四收盤調整（現持改變、當天報酬仍用週三現持，只多一筆換手成本）→ 週五起新現持。"""
    legs, dates, hist, px = _synthetic()
    # 讓價格每天固定漲 1%、目標固定 50：綠燈時現持 50，紅燈時目標 25 → 現持 20（五五入取偶）
    for i, ds in enumerate(dates):
        for t in legs:
            hist[i]["tickers"][t].update({"gate": True, "final_pct": 50.0})
            px[t][ds] = 100.0 * (1.01 ** i)
    mkt = next(m for m in lsb.MARKETS if m["key"] == "tw")
    px_dates = {t: sorted(px[t]) for t in legs}
    wed = next(d for d in dates[8:] if date.fromisoformat(d).weekday() == 2)
    rel = [{"release_date": "2026-10-07", "color": "green"}, {"release_date": wed, "color": "red"}]
    sim = nf.simulate_market(mkt, hist, dates[5], lambda d: nf.release_for_day(rel, d), px, px_dates, None, None)
    ds_ = sim["dates"]
    i_wed = ds_.index(wed)
    i_thu = i_wed + 1
    assert ds_[i_thu] == (date.fromisoformat(wed) + timedelta(days=1)).isoformat()
    # 週三仍是綠燈：影子線與實單一樣
    assert all(sim["ex_shadow"][t][i_wed] == sim["ex_live"][t][i_wed] for t in legs)
    # 週四收盤調整
    assert all(sim["ex_shadow"][t][i_thu] != sim["ex_live"][t][i_thu] for t in legs)
    assert [sim["ex_shadow"][t][i_thu] for t in legs] == [20.0, 20.0]
    # 週四當天的報酬還是用週三現持：兩條線的差只有換手成本（兩腿各 30pp，共 0.6 × 7 bps）
    gap_thu = sim["nav_live"][i_thu] / sim["nav_live"][i_thu - 1] - sim["nav_shadow"][i_thu] / sim["nav_shadow"][i_thu - 1]
    assert gap_thu == pytest.approx(0.6 * 0.0007, abs=5e-6)
    # 週五起新現持承擔報酬：影子線漲得比實單少
    r_live = sim["nav_live"][i_thu + 1] / sim["nav_live"][i_thu] - 1
    r_sh = sim["nav_shadow"][i_thu + 1] / sim["nav_shadow"][i_thu] - 1
    assert r_sh < r_live


def test_tw_thursday_holiday_defers_adjustment_to_friday():
    legs, dates, hist, px = _synthetic()
    wed = next(d for d in dates[8:] if date.fromisoformat(d).weekday() == 2)
    thu = (date.fromisoformat(wed) + timedelta(days=1)).isoformat()
    keep = [i for i, d in enumerate(dates) if d != thu]          # 台股週四休市
    hist2 = [hist[i] for i in keep]
    dates2 = [dates[i] for i in keep]
    for i, ds in enumerate(dates2):
        for t in legs:
            hist2[i]["tickers"][t].update({"gate": True, "final_pct": 50.0})
            px[t][ds] = 100.0 * (1.01 ** i)
    mkt = next(m for m in lsb.MARKETS if m["key"] == "tw")
    px_dates = {t: sorted(px[t]) for t in legs}
    rel = [{"release_date": "2026-10-07", "color": "green"}, {"release_date": wed, "color": "red"}]
    sim = nf.simulate_market(mkt, hist2, dates2[5], lambda d: nf.release_for_day(rel, d), px,
                             {t: sorted(px[t]) for t in legs}, None, None)
    fri = (date.fromisoformat(wed) + timedelta(days=2)).isoformat()
    ds_ = sim["dates"]
    assert thu not in ds_
    assert sim["ex_shadow"]["0050"][ds_.index(wed)] == sim["ex_live"]["0050"][ds_.index(wed)]
    assert sim["ex_shadow"]["0050"][ds_.index(fri)] == 20.0 and sim["ex_live"]["0050"][ds_.index(fri)] == 50.0


def test_rule_switch_clamp_comes_from_record_tag():
    """新規則紀錄（rule 標籤 w52a_c1_live）clamp 50pp；影子線沿用實單的 exec_clamp_for。"""
    sim, *_ = _sim(force="green", rule=w52.NEW_RULE_TAG)
    assert all(v <= 50.0 for t in sim["legs"] for v in sim["ex_shadow"][t])


# ── 存檔：只增不改、補抓註明、顏色一致性 ───────────────────────────────────────
def _fake_fetch_factory(table):
    def fetch(w):
        return table.get(w)
    return fetch


def _vintage_text(last_obs, last_v, prev_obs, prev_v):
    return f"observation_date,NFCI_X\n{prev_obs},{prev_v}\n{last_obs},{last_v}\n"


def test_releases_append_only_and_backfill_is_labelled(tmp_path):
    p = tmp_path / "rel.csv"
    t14 = _vintage_text("2026-10-02", "-0.494", "2026-09-04", "-0.545")
    t21 = _vintage_text("2026-10-16", "-0.470", "2026-09-18", "-0.524")
    t28 = _vintage_text("2026-10-23", "-0.520", "2026-09-25", "-0.510")
    # 10-14 當天以後第一次執行（起始版本）
    cap = nf.capture_missing(p, "2026-10-14", date(2026, 10, 15), fetch=_fake_fetch_factory({"2026-10-14": t14}))
    assert cap == {"added": ["2026-10-14"], "missing": []}
    before = p.read_bytes()
    # 10-22（週四）：10-21 版當週存檔
    cap = nf.capture_missing(p, "2026-10-14", date(2026, 10, 22), fetch=_fake_fetch_factory({"2026-10-21": t21}))
    assert cap["added"] == ["2026-10-21"]
    assert p.read_bytes().startswith(before)                    # 既有列一個位元組都沒動
    # 10-28 版漏抓，11-03 才補：標「事後補抓」並寫備註
    cap = nf.capture_missing(p, "2026-10-14", date(2026, 11, 3), fetch=_fake_fetch_factory({"2026-10-28": t28}))
    assert cap["added"] == ["2026-10-28"]
    rows = nf.load_releases(p)
    assert [r["release_date"] for r in rows] == ["2026-10-14", "2026-10-21", "2026-10-28"]
    assert [r["source"] for r in rows] == ["起始版本", "當週存檔", "事後補抓（ALFRED）"]
    assert "ALFRED" in rows[2]["note"] and "2026-11-03" in rows[2]["note"]
    assert [r["color"] for r in rows] == ["red", "red", "green"]
    # 已存的不重抓、不覆蓋
    cap = nf.capture_missing(p, "2026-10-14", date(2026, 11, 3), fetch=lambda w: pytest.fail("不該重抓"))
    assert cap == {"added": [], "missing": []}


def test_capture_rejects_stale_vintage_and_reports_missing(tmp_path):
    p = tmp_path / "rel.csv"
    stale = _vintage_text("2026-08-28", "-0.5", "2026-07-31", "-0.5")       # 離公布日 48 天
    cap = nf.capture_missing(p, "2026-10-14", date(2026, 10, 15), fetch=_fake_fetch_factory({"2026-10-14": stale}))
    assert cap["added"] == [] and cap["missing"] == ["2026-10-14"]
    assert not p.exists()
    cap = nf.capture_missing(p, "2026-10-14", date(2026, 10, 15), fetch=lambda w: None)
    assert cap["missing"] == ["2026-10-14"]


def test_load_releases_detects_color_tampering(tmp_path):
    p = tmp_path / "rel.csv"
    nf.append_release(p, nf.release_from_vintage("2026-10-14", nf.parse_vintage(VINTAGE_1014), "d", "s"))
    p.write_text(p.read_text(encoding="utf-8").replace(",red,", ",green,"), encoding="utf-8")
    with pytest.raises(nf.Abort):
        nf.load_releases(p)


def test_committed_release_file_matches_registration_start_version():
    rows = nf.load_releases(nf.RELEASES_CSV)
    first = rows[0]
    assert first["release_date"] == nf.SEED_VINTAGE
    assert (first["last_obs_date"], first["value_2dp"], first["value_4w_ago_2dp"], first["color"]) == \
        ("2026-10-02", "-0.49", "-0.55", "red")


# ── 狀態檔：公開檔不放帳戶結構或金額 ───────────────────────────────────────────
FORBIDDEN = ["帳戶", "MNQ", "XNAS", "CBU0", "IGLN", "UCITS", "券商", "股數", "金額"]


def test_public_files_have_no_account_structure_or_amounts():
    files = [nf.RELEASES_CSV, nf.STATE_OUT, SCRIPTS_DIR.parent / ".github" / "workflows" / "nfci-forward-shadow.yml"]
    for f in files:
        text = f.read_text(encoding="utf-8")
        for tok in FORBIDDEN:
            assert tok not in text, f"{f.name} 含有 {tok}"


def test_generated_state_text_has_no_forbidden_tokens_and_is_deterministic():
    sim, dates, hist = _sim(force="red")
    mk = sim["mkt"]
    closes = [1000.0 + i for i in range(len(sim["dates"]))]
    sims = {"tw": sim}
    rel = [{"release_date": "2026-10-14", "last_obs_date": "2026-10-02", "color": "red",
            "value_2dp": "-0.49", "value_4w_ago_2dp": "-0.55"}]
    st1 = nf.build_state("2026-10-19", rel, {"missing": []}, sims, {"tw": closes}, None)
    st2 = nf.build_state("2026-10-19", rel, {"missing": []}, sims, {"tw": closes}, None)
    t1, t2 = nf.dump_json(st1), nf.dump_json(st2)
    assert t1 == t2
    for tok in FORBIDDEN:
        assert tok not in t1
    json.loads(t1)
    assert st1["status"] == "累積中"                              # 判定日之前不提前判
    assert "criteria" not in st1


def test_state_without_data_says_no_shadow_data_yet():
    st = nf.build_state("2026-10-19", [{"release_date": "2026-10-14", "last_obs_date": "2026-10-02",
                                        "color": "red", "value_2dp": "-0.49", "value_4w_ago_2dp": "-0.55"}],
                        {"missing": []}, {"us": None, "tw": None}, {}, None)
    assert st["status"] == "尚無資料" and st["markets"] == {}


def test_committed_state_is_the_real_start_with_no_shadow_data_yet():
    st = json.loads(nf.STATE_OUT.read_text(encoding="utf-8"))
    assert st["start_date"] == "2026-10-19"
    assert st["earliest_decision_date"] == "2029-10-19"
    live = json.loads(nf.LIVE_STATE.read_text(encoding="utf-8"))
    if max(r["date"] for r in live["history_us"]) < "2026-10-19" and max(r["date"] for r in live["history_tw"]) < "2026-10-19":
        assert st["status"] == "尚無資料" and st["markets"] == {}


def test_adjustment_count_ignores_start_day_and_counts_each_leg_change():
    ex = {"a": [50.0, 50.0, 20.0, 20.0, 50.0], "b": [0.0, 0.0, 0.0, 10.0, 10.0]}
    assert nf.count_adjustments(ex) == 3 and nf.count_adjustments({"a": [50.0]}) == 0


# ── 主控台那一列 ──────────────────────────────────────────────────────────
def test_console_row_shows_pending_until_data_exists():
    assert bli.nfci_forward_now_html(None) == "2026-10-19 起累積中"
    assert bli.nfci_forward_now_html({"status": "尚無資料", "markets": {}}) == "2026-10-19 起累積中"


def test_console_row_shows_color_crashes_calmar_and_trade_ratio():
    st = {
        "status": "累積中",
        "nfci": {"current": {"color": "red", "release_date": "2026-10-14"}},
        "markets": {
            "us": {"crashes": {"count": 2, "episodes": [{"benefit_bp": 340, "recovered": True},
                                                       {"benefit_bp": -110, "recovered": False}]},
                   "calmar": {"live": 0.61, "shadow": 0.59}, "adjustments": {"live": 10, "shadow": 21, "ratio": 2.1}},
            "tw": {"crashes": {"count": 0, "episodes": []}, "calmar": {"live": None, "shadow": None},
                   "adjustments": {"live": 0, "shadow": 2, "ratio": None}},
        },
    }
    html = bli.nfci_forward_now_html(st)
    assert "紅燈" in html and "2026-10-14" in html
    assert "股災 2 次" in html and "+3.4" in html and "-1.1（進行中）" in html
    assert "影子線 0.59／實單 0.61" in html and "2.10 倍" in html
    assert "股災 0 次" in html and "滿一年後才算" in html
    assert "判定日" not in html                                   # 判定日之前不提前判


def test_console_testing_table_second_row_is_registered_start_and_decision_dates():
    row = next(r for r in bli.TESTING if r.get("key") == "nfci")
    assert row["start"] == "2026-10-19" and row["due"].startswith("2029-10-19")
    html = bli.render_testing_table(bli.TESTING)
    assert "登記中" not in html


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
