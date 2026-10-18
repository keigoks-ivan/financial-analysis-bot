"""docs/ideas/data/bond-outlook/data.py --gauges 的測試：BEY 換算、分界（整數空間）、相關係數、
HTML 標記重寫冪等、抓不到時沿用上次。全程離線，不連 FRED／yfinance。

python3.12 -m pytest scripts/tests/test_bond_gauges.py -q
"""
from __future__ import annotations

import importlib.util
import json
import sys
from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO / "scripts"
DATA_PY = REPO / "docs" / "ideas" / "data" / "bond-outlook" / "data.py"

_spec = importlib.util.spec_from_file_location("bond_outlook_data", DATA_PY)
bo = importlib.util.module_from_spec(_spec)
_dwb, sys.dont_write_bytecode = sys.dont_write_bytecode, True      # 不在 docs/ 底下留 __pycache__
_spec.loader.exec_module(bo)
sys.dont_write_bytecode = _dwb


# ───────────────────────── BEY 與利差 ─────────────────────────
def test_bey_from_discount_rate():
    # 4.10% 貼現率 → 365·0.041 / (360 − 0.041·91) = 4.2005%
    assert round(bo.bey_pct(4.10), 4) == Decimal("4.2005")
    assert bo.bey_pct(0) == 0


def test_bey_matches_backtest_library_formula():
    """與回測庫 reconstruct.bey_from_discount 同公式（BILL_YEAR=365、BILL_DAYS=91）。"""
    for d in (0.05, 1.0, 2.37, 4.10, 5.25):
        want = 100.0 * 365.0 * (d / 100) / (360.0 - (d / 100) * 91)
        assert abs(float(bo.bey_pct(d)) - want) < 1e-9


def test_spread_bps_uses_bey_not_discount_rate():
    # 舊的錯誤口徑 5.10 − 4.10 = 1.00 個百分點；正確口徑 5.10 − 4.2005 = 0.8995 → 90 基點
    assert bo.spread_bps(5.10, 4.10) == 90
    assert bo.spread_zone(bo.spread_bps(5.10, 4.10)) == "red"


def test_spread_zone_integer_boundaries():
    assert bo.spread_zone(100) == "yellow"    # 恰好 1 個百分點：中性
    assert bo.spread_zone(99) == "red"        # 差 1 個基點：不利
    assert bo.spread_zone(199) == "yellow"
    assert bo.spread_zone(200) == "green"     # 恰好 2 個百分點：有利
    assert bo.spread_zone(201) == "green"
    assert bo.spread_zone(0) == "red"
    assert bo.spread_zone(-35) == "red"


def test_spread_boundaries_end_to_end_with_zero_bill_rate():
    # 3 個月利率 0 時 BEY 也是 0，利差就是 10 年殖利率本身，檢查浮點不會把 1.00 算成 0.9999…
    assert bo.spread_bps(1.00, 0.0) == 100 and bo.spread_zone(bo.spread_bps(1.00, 0.0)) == "yellow"
    assert bo.spread_bps(0.99, 0.0) == 99 and bo.spread_zone(bo.spread_bps(0.99, 0.0)) == "red"
    assert bo.spread_bps(2.00, 0.0) == 200 and bo.spread_zone(bo.spread_bps(2.00, 0.0)) == "green"
    assert bo.spread_bps(1.99, 0.0) == 199 and bo.spread_zone(bo.spread_bps(1.99, 0.0)) == "yellow"


def test_spread_rounds_to_whole_bps_before_comparing():
    # 5.20 − 4.2005 = 0.9995 個百分點（99.95 基點）四捨五入成 100 基點 → 中性
    assert bo.spread_bps(5.20, 4.10) == 100
    assert bo.spread_zone(bo.spread_bps(5.20, 4.10)) == "yellow"
    # 5.19 − 4.2005 = 98.95 基點 → 99 → 不利
    assert bo.spread_bps(5.19, 4.10) == 99
    assert bo.spread_zone(bo.spread_bps(5.19, 4.10)) == "red"


def test_spread_row_fields():
    r = bo.spread_row("2026-10-15", 5.10, 4.10)
    assert r["bps"] == 90 and r["value"] == 0.9
    assert r["value_text"] == "0.90 個百分點"
    assert r["zone"] == "red" and r["zone_label"] == "不利"
    assert r["zones"]["red"] == "低於 1 個百分點"
    assert "4.20%" in r["note"] and "5.10%" in r["note"]


def test_negative_spread_text_uses_true_minus():
    r = bo.spread_row("2026-10-15", 3.0, 4.10)
    assert r["bps"] < 0 and r["value_text"].startswith("−") and r["zone"] == "red"


# ───────────────────────── 相關係數 ─────────────────────────
def test_corr_zone_boundaries():
    assert bo.corr_zone(-30) == "yellow"      # −0.30 中性
    assert bo.corr_zone(-31) == "green"       # −0.31 有利
    assert bo.corr_zone(30) == "yellow"       # +0.30 中性
    assert bo.corr_zone(31) == "red"          # +0.31 不利
    assert bo.corr_zone(0) == "yellow"


def test_corr_rounds_to_two_decimals_before_zone():
    assert bo.corr_c100(0.304) == 30 and bo.corr_zone(bo.corr_c100(0.304)) == "yellow"
    assert bo.corr_c100(0.305) == 31 and bo.corr_zone(bo.corr_c100(0.305)) == "red"
    assert bo.corr_c100(-0.304) == -30 and bo.corr_zone(bo.corr_c100(-0.304)) == "yellow"
    assert bo.corr_c100(-0.306) == -31 and bo.corr_zone(bo.corr_c100(-0.306)) == "green"
    assert bo.corr_c100(np.float64(0.5481)) == 55


def _prices(rets, start="2025-01-02"):
    idx = pd.bdate_range(start, periods=len(rets) + 1)
    return pd.Series(100 * np.concatenate([[1.0], np.cumprod(1 + np.asarray(rets))]), index=idx)


def test_corr_series_window_is_60_returns_from_61_closes():
    rng = np.random.default_rng(7)
    a = rng.normal(0, 0.01, 200)
    b = 0.5 * a + rng.normal(0, 0.01, 200)
    spy, ief = _prices(a), _prices(b)
    rc = bo.corr_series(spy, ief)
    want = np.corrcoef(a[-60:], b[-60:])[0, 1]
    assert abs(rc.iloc[-1] - want) < 1e-12
    # 61 個收盤剛好只有 1 個值
    assert len(bo.corr_series(spy.iloc[:61], ief.iloc[:61])) == 1


def test_corr_series_uses_common_trading_days_only():
    rng = np.random.default_rng(3)
    a = rng.normal(0, 0.01, 120)
    spy = _prices(a)
    ief = _prices(a)
    ief = ief.drop(ief.index[-1])             # IEF 少最後一天
    rc = bo.corr_series(spy, ief)
    assert rc.index[-1] == ief.index[-1]
    assert abs(rc.iloc[-1] - 1.0) < 1e-9


def test_corr_row_year_to_date_extremes_and_note():
    idx = pd.to_datetime(["2025-12-30", "2026-01-02", "2026-03-10", "2026-06-05", "2026-10-16"])
    rc = pd.Series([0.99, -0.113, 0.20, 0.667, 0.445], index=idx)
    r = bo.corr_row(rc)
    assert r["asof"] == "2026-10-16" and r["value_text"] == "+0.45" and r["zone"] == "red"
    # 去年的 0.99 不算進今年
    assert r["note"] == "還原日價自算；2026 年最高 +0.67（6 月 5 日），最低 −0.11（1 月 2 日）"


# ───────────────────────── FRED ─────────────────────────
def test_parse_fred_csv_skips_blank_and_dot():
    text = "observation_date,DGS10\n2026-10-09,5.24\n2026-10-12,\n2026-10-13,.\n2026-10-15,5.10\n"
    assert bo.parse_fred_csv(text) == {"2026-10-09": 5.24, "2026-10-15": 5.10}
    assert bo.parse_fred_csv("DATE,DTB3\n2026-10-15,4.10\n") == {"2026-10-15": 4.10}


def test_parse_fred_csv_rejects_html():
    with pytest.raises(ValueError):
        bo.parse_fred_csv("<html><body>blocked</body></html>")


def test_latest_common_date_when_one_series_lags():
    a = {"2026-10-14": 5.19, "2026-10-15": 5.10, "2026-10-16": 5.05}
    b = {"2026-10-14": 4.10, "2026-10-15": 4.10}
    assert bo.latest_common(a, b) == ("2026-10-15", 5.10, 4.10)
    with pytest.raises(ValueError):
        bo.latest_common({"2026-10-16": 5.0}, {"2026-10-15": 4.0})


# ───────────────────────── 連續週數 ─────────────────────────
def test_streak_of_and_text():
    dates = ["2026-08-28", "2026-09-04", "2026-09-11", "2026-09-18"]
    st = bo.streak_of([1, 0, 0, 0], dates)
    assert st == {"n": 0, "start": "2026-09-04", "weeks": 3, "prev_n": 1}
    assert bo.streak_text(st) == "9/4 起連續 3 週"
    st1 = bo.streak_of([1, 1, 1, 0], dates)
    assert st1["weeks"] == 1 and st1["prev_n"] == 1
    assert bo.streak_text(st1) == "9/18 由 1/3 降為 0/3"
    st2 = bo.streak_of([0, 0, 0, 2], dates)
    assert bo.streak_text(st2) == "9/18 由 0/3 升為 2/3"
    assert bo.streak_text(bo.streak_of([0, 0], dates[:2])) == "8/28 起 0/3"


def _ov(n=0, week="2026-10-16"):
    return {"week_date": week, "n": n, "c_ma40": n >= 1, "c_ma52": n >= 2, "c_px52": n >= 3}


def test_leg_row_shape_and_no_account_strings():
    st = bo.streak_of([1, 0, 0], ["2026-10-02", "2026-10-09", "2026-10-16"])
    r = bo.leg_row("ief", _ov(0), st)
    assert r["id"] == "ief_3cond" and r["kind"] == "leg" and r["value_text"] == "0/3"
    assert r["zone"] == "off" and r["zone_label"] == "不持有"
    on = bo.leg_row("gld", _ov(2), bo.streak_of([0, 2], ["2026-10-09", "2026-10-16"]))
    assert on["zone"] == "on" and on["zone_label"] == "持有 2/3"
    blob = json.dumps([r, on], ensure_ascii=False)
    for bad in ("MNQ", "XNAS", "CBU0", "IGLN", "UCITS", "帳戶"):
        assert bad not in blob


# ───────────────────────── fetch_legs（真的實單程式，價格用合成資料）─────────────────────────
def test_fetch_legs_uses_live_compute_overlay_and_isolates_failures(monkeypatch):
    sys.path.insert(0, str(SCRIPTS_DIR))
    import update_long_track_w52_adaptive as w52
    import update_long_track_w52_adaptive_c1 as c1

    today = pd.Timestamp.now(tz="UTC").tz_localize(None).normalize()
    idx = pd.bdate_range(end=today, periods=900)
    up = pd.Series(np.linspace(50, 150, len(idx)), index=idx)

    def fake_fetch(sym):
        if sym == "GLD":
            raise RuntimeError("yahoo down")
        return up

    monkeypatch.setattr(c1, "fetch_adj", fake_fetch)
    legs_before = w52.OVERLAY_LEGS
    out = bo.fetch_legs()
    assert w52.OVERLAY_LEGS == legs_before and c1.fetch_adj is fake_fetch
    assert isinstance(out["gld"], Exception)
    ief = out["ief"]
    assert ief["id"] == "ief_3cond" and ief["value"] == 3 and ief["zone"] == "on"
    # 和實單程式同一個答案（GLD 會丟例外，所以單腿比對）
    monkeypatch.setattr(w52, "OVERLAY_LEGS", ("ief",))
    live = w52.compute_overlay(today)["ief"]
    assert live["n"] == ief["value"] and live["week_date"] == ief["asof"]


# ───────────────────────── HTML 重寫 ─────────────────────────
HTML = """<p><!-- gauges-lead:start --><b>舊標題</b><!-- gauges-lead:end -->後文</p>
<table><tbody>
<!-- gauges:start -->
<tr><td>舊列</td></tr>
<!-- gauges:end -->
</tbody></table>
<script>{"data_asof": "2020-01-01", "data_last_trading_day": "2020-01-01", "x": 1}</script>
"""


def _rows(corr_c100=45, bps_y10=5.10, ief_n=0):
    rc = pd.Series([corr_c100 / 100], index=pd.to_datetime(["2026-10-16"]))
    st = bo.streak_of([1, 0, 0], ["2026-10-02", "2026-10-09", "2026-10-16"])
    return [bo.corr_row(rc), bo.spread_row("2026-10-15", bps_y10, 4.10),
            bo.leg_row("ief", _ov(ief_n), st), bo.leg_row("gld", _ov(0), st)]


def test_apply_gauges_rewrites_between_markers_and_is_idempotent():
    rows = _rows()
    once = bo.apply_gauges(HTML, rows)
    assert "舊列" not in once and "舊標題" not in once
    assert "<td>+0.45</td><td>2026-10-16</td>" in once
    assert '<span class="badge b-ref">不利</span>' in once
    assert 'colspan="3">9/4' not in once  # 連續週數用本次資料的日期
    assert 'colspan="3">10/9 起連續 2 週 0/3' in once
    assert '"data_asof": "2026-10-16"' in once and '"data_last_trading_day": "2026-10-16"' in once
    assert once.count("<!-- gauges:start -->") == 1 and once.count("<!-- gauges:end -->") == 1
    assert bo.apply_gauges(once, rows) == once            # 同資料再套一次不變
    twice_other = bo.apply_gauges(once, _rows(corr_c100=-40))
    assert "<td>−0.40</td>" in twice_other and twice_other != once


def test_apply_gauges_requires_markers():
    with pytest.raises(ValueError):
        bo.apply_gauges("<table><tbody></tbody></table>", _rows())


def test_render_lead_variants():
    rows = _rows()
    assert "目前都不在有利區" in bo.render_lead(rows)
    rows[0] = {**rows[0], "zone": "green"}
    assert "目前只有相關係數在有利區" in bo.render_lead(rows)
    rows[1] = {**rows[1], "zone": "green"}
    assert "目前都在有利區" in bo.render_lead(rows)
    rows[0] = {**rows[0], "zone": "red"}
    assert "目前只有利差在有利區" in bo.render_lead(rows)


def test_committed_page_matches_committed_gauges_json():
    """repo 裡的頁面表格要等於 gauges.json 套進模板的結果（兩者永遠一起寫）。"""
    g = json.loads(bo.GAUGES_JSON.read_text(encoding="utf-8"))
    html = bo.PAGE.read_text(encoding="utf-8")
    assert [r["id"] for r in g["gauges"]] == list(bo.GAUGE_ORDER)
    assert bo.apply_gauges(html, g["gauges"]) == html


# ───────────────────────── refresh_gauges：冪等、抓不到沿用 ─────────────────────────
@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    page = tmp_path / "bond-outlook.html"
    page.write_text(HTML, encoding="utf-8")
    monkeypatch.setattr(bo, "PAGE", page)
    monkeypatch.setattr(bo, "GAUGES_JSON", tmp_path / "gauges.json")
    monkeypatch.setattr(bo, "STATE_JSON", tmp_path / "no_state.json")
    monkeypatch.setattr(bo, "OUT", tmp_path / "data.json")
    monkeypatch.setattr(bo, "EXTRACT", tmp_path / "history_extract.json")
    (tmp_path / "history_extract.json").write_text('{"events": []}', encoding="utf-8")
    return tmp_path


def _fetchers(rows):
    return {"corr": lambda: rows[0], "spread": lambda: rows[1],
            "legs": lambda: {"ief": rows[2], "gld": rows[3]}}


def _boom():
    raise RuntimeError("network down")


def test_refresh_is_idempotent(sandbox):
    rows = _rows()
    bo.refresh_gauges(_fetchers(rows))
    first = {p.name: p.read_bytes() for p in sandbox.iterdir()}
    bo.refresh_gauges(_fetchers(rows))
    second = {p.name: p.read_bytes() for p in sandbox.iterdir()}
    assert first == second                                  # generated 時間也不變
    bo.build()
    built = (sandbox / "data.json").read_bytes()
    bo.refresh_gauges(_fetchers(rows))
    bo.build()
    assert (sandbox / "data.json").read_bytes() == built


def test_refresh_keeps_previous_row_when_one_source_fails(sandbox):
    old = _rows()
    bo.refresh_gauges(_fetchers(old))
    new = _rows(corr_c100=-40, bps_y10=7.0)
    fetchers = _fetchers(new)
    fetchers["spread"] = _boom                              # 利差抓不到
    doc = bo.refresh_gauges(fetchers)
    by = {g["id"]: g for g in doc["gauges"]}
    assert by["spy_ief_corr60"]["value_text"] == "−0.40"      # 其他列照常更新
    assert by["t10y3m"]["value_text"] == old[1]["value_text"]       # 這列沿用上次的值與資料日
    assert by["t10y3m"]["asof"] == old[1]["asof"] and by["t10y3m"]["stale"] is True
    page = bo.PAGE.read_text(encoding="utf-8")
    assert "<td>−0.40</td>" in page and "<td>0.90 個百分點</td>" in page
    # 恢復後 stale 旗標消失
    doc2 = bo.refresh_gauges(_fetchers(new))
    assert all("stale" not in g for g in doc2["gauges"])


def test_refresh_leg_failure_is_per_leg(sandbox):
    old = _rows()
    bo.refresh_gauges(_fetchers(old))
    st = bo.streak_of([0, 2], ["2026-10-09", "2026-10-16"])
    new_ief = bo.leg_row("ief", _ov(2), st)
    f = _fetchers(old)
    f["legs"] = lambda: {"ief": new_ief, "gld": RuntimeError("gld down")}
    doc = bo.refresh_gauges(f)
    by = {g["id"]: g for g in doc["gauges"]}
    assert by["ief_3cond"]["value"] == 2 and "stale" not in by["ief_3cond"]
    assert by["gld_3cond"]["stale"] is True and by["gld_3cond"]["value"] == 0
    # 整個 legs 抓取炸掉：兩條腿都沿用
    f["legs"] = _boom
    doc = bo.refresh_gauges(f)
    by = {g["id"]: g for g in doc["gauges"]}
    assert by["ief_3cond"]["stale"] and by["gld_3cond"]["stale"] and by["ief_3cond"]["value"] == 2


def test_refresh_all_fail_without_previous_does_not_touch_page(sandbox):
    f = {"corr": _boom, "spread": _boom, "legs": _boom}
    doc = bo.refresh_gauges(f)
    assert doc["gauges"] == []
    assert bo.PAGE.read_text(encoding="utf-8") == HTML      # 四列不齊，頁面不動


def test_build_reads_gauges_json_and_splits_legs(sandbox):
    bo.refresh_gauges(_fetchers(_rows()))
    bo.build()
    d = json.loads((sandbox / "data.json").read_text(encoding="utf-8"))
    assert [g["id"] for g in d["gauges"]] == ["spy_ief_corr60", "t10y3m"]
    assert d["legs_status"]["ief"] == "0/3（10/9 起連續 2 週）"
    assert d["legs_status"]["gold"] == "0/3（10/9 起連續 2 週）"
    assert d["legs_status"]["live_page"] == "/long-track-w52-adaptive/"
    assert d["history"] == {"events": []}
