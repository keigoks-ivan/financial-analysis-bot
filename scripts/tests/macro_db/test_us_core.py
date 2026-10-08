"""美國部分：store 合併、年增率按日期對齊、各 fetcher 解析、行事曆解析。"""
import datetime as dt
import json
from pathlib import Path

import pytest

from macro_db import store, transform, calendar as relcal
from macro_db.sources import census_trade, cleveland, fedboard, fred, fiscaldata, nyfed, nyfed_markets, umich

FX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "us"


# ---------- store ----------
def test_merge_overwrites_and_keeps_old():
    old = [("2026-01-01", 1.0), ("2026-02-01", 2.0)]
    new = [("2026-02-01", 2.5), ("2026-03-01", 3.0)]
    assert store.merge(old, new) == [("2026-01-01", 1.0), ("2026-02-01", 2.5), ("2026-03-01", 3.0)]


def test_write_merged_accumulates_and_skips_unchanged(tmp_path):
    m, changed, new = store.write_merged("us.x", [("2026-01-01", 1.0), ("2026-02-01", 2.0)], tmp_path)
    assert changed and new
    # 來源只剩近期：舊日期保留
    m, changed, new = store.write_merged("us.x", [("2026-02-01", 2.0), ("2026-03-01", 3.0)], tmp_path)
    assert [d for d, _ in m] == ["2026-01-01", "2026-02-01", "2026-03-01"] and changed and not new
    p = tmp_path / "series" / "us.x.csv"
    mtime = p.stat().st_mtime_ns
    m, changed, _ = store.write_merged("us.x", [("2026-03-01", 3.0)], tmp_path)
    assert not changed and p.stat().st_mtime_ns == mtime
    assert p.read_text().splitlines()[0] == "date,value"


def test_status_failure_keeps_old_data(tmp_path):
    st = {}
    merged, _, _ = store.write_merged("us.x", [("2026-01-01", 1.0)], tmp_path)
    store.update_status(st, "us.x", merged, None, now="t1")
    store.update_status(st, "us.x", merged, "HTTP 500", now="t2")
    e = st["us.x"]
    assert e["last_ok"] == "t1" and e["last_error"] == "HTTP 500" and e["last_date"] == "2026-01-01" and e["n"] == 1
    store.update_status(st, "us.x", merged + [("2026-02-01", 2.0)], None, now="t3")
    assert st["us.x"]["last_error"] is None and st["us.x"]["advanced"] == "t3"


# ---------- transform ----------
def fake_cpi():
    """2024-09 到 2026-03 每月一筆，但缺 2025-10（政府關門）。指數每月 +1。"""
    out, v = [], 100.0
    y, m = 2024, 9
    while (y, m) <= (2026, 3):
        if (y, m) != (2025, 10):
            out.append(("%04d-%02d-01" % (y, m), v))
        v += 1
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return out


def test_yoy_aligns_by_date_not_by_count():
    obs = fake_cpi()
    res = dict(transform.yoy(obs, "M"))
    # 2025-11 的去年同期是 2024-11（值 102+... 依序計算）
    d = dict(obs)
    assert res["2025-11-01"] == pytest.approx((d["2025-11-01"] / d["2024-11-01"] - 1) * 100)
    # 往回數 12 筆會誤取 2024-10 以外的月份：確認不是那個數
    idx = [k for k, _ in obs].index("2025-11-01")
    wrong = obs[idx - 12][1]
    assert d["2024-11-01"] != wrong
    # 缺月本身不出值；2026-10 的去年同期缺 -> 2026 年尚無該月
    assert "2025-10-01" not in res
    # 去年同期缺的那一點（2026-10）若存在資料也不出值
    obs2 = obs + [("2026-10-01", 130.0)]
    assert "2026-10-01" not in dict(transform.yoy(obs2, "M"))


def test_mom_and_diff_use_previous_calendar_month():
    obs = fake_cpi()
    mm = dict(transform.mom(obs, "M"))
    assert "2025-10-01" not in mm and "2025-11-01" not in mm  # 前一月缺
    assert "2025-12-01" in mm
    df = dict(transform.diff(obs, "M"))
    assert df["2025-12-01"] == pytest.approx(1.0)


def test_daily_yoy_tolerance_and_ratio_and_combine():
    obs = [("2024-01-02", 100.0), ("2025-01-03", 110.0)]
    assert transform.yoy(obs, "D")[0][1] == pytest.approx(10.0)  # 2024-01-03 無，取前一筆（7 天內）
    assert transform.ratio([("2026-04-01", 50000.0)], [("2026-04-01", 25000.0)], 0.001) == [("2026-04-01", pytest.approx(0.2))]
    assert transform.combine("sub", [("a", 3.0), ("b", 1.0)], [("a", 1.0)]) == [("a", 2.0)]


def test_downsample_daily_keeps_recent_daily():
    obs = [("2000-01-03", 1.0), ("2000-01-04", 2.0), ("2000-01-05", 3.0), ("2026-01-02", 4.0), ("2026-01-05", 5.0)]
    out = transform.downsample_daily(obs, today=dt.date(2026, 1, 6))
    assert out[0] == ("2000-01-05", 3.0) and out[-2:] == [("2026-01-02", 4.0), ("2026-01-05", 5.0)]


# ---------- fetchers ----------
def test_fred_parse_csv_skips_missing():
    t = "observation_date,A,B\n2026-01-01,1.5,\n2026-02-01,.,2\n2026-03-01,3,4\n"
    r = fred.parse(t, ["A", "B"])
    assert r["A"] == [("2026-01-01", 1.5), ("2026-03-01", 3.0)] and r["B"] == [("2026-02-01", 2.0), ("2026-03-01", 4.0)]


def test_fred_parse_zip_payload():
    import io
    import zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("README.txt", "x")
        z.writestr("monthly.csv", "observation_date,A\n2026-01-01,1\n")
        z.writestr("daily.csv", "observation_date,B\n2026-01-02,2\n")
    r = fred.parse_payload(buf.getvalue(), ["A", "B"])
    assert r == {"A": [("2026-01-01", 1.0)], "B": [("2026-01-02", 2.0)]}


def test_umich_parse():
    obs = umich.parse((FX / "ics.csv").read_text(), "ICS_ALL")
    assert obs[0] == ("1952-11-01", 86.2) and obs[1] == ("1953-02-01", 90.7)


def test_fedboard_parse_scale_and_month_first():
    obs = fedboard.parse((FX / "ebp.csv").read_text(), "est_prob", 100)
    assert obs[0][0] == "1973-01-01" and obs[0][1] == pytest.approx(18.34564, abs=1e-3)


def test_nyfed_mct_parse():
    obs = nyfed.parse_mct((FX / "mct.csv").read_text())
    assert obs[0] == ("1960-02-01", 1.48)


def test_nyfed_recprob_and_gscpi_parse():
    import pandas as pd
    df = pd.DataFrame({"Date": pd.to_datetime(["2026-08-31", "2027-08-31"]), "Rec_prob": [0.1, float("nan")]})
    assert nyfed.parse_recprob(df) == [("2026-08-01", 10.0)]
    g = pd.DataFrame([[None, None], ["31-Jan-1998", -0.5], ["28-Feb-1998", 0.25]])
    assert nyfed.parse_gscpi(g) == [("1998-01-01", -0.5), ("1998-02-01", 0.25)]


def test_nyfed_hlw_finds_rstar_column():
    import pandas as pd
    rows = [[None] * 6 for _ in range(4)]
    rows += [[None, None, "Trend", None, "Natural Rate (r*)", None], ["Date", None, "US", None, "US", None],
             [pd.Timestamp("2026-04-01"), None, 4.0, None, 1.25, None]]
    assert nyfed.parse_hlw(pd.DataFrame(rows)) == [("2026-04-01", 1.25)]


def test_cleveland_parse_uses_target_month_only():
    obs = cleveland.parse((FX / "cleveland.json").read_text(), "CPI Inflation")
    assert obs and all(d.startswith("2026-10") for d, _ in obs)


def test_census_trade_parse():
    tab = census_trade.parse((FX / "census_c5700.html").read_text())
    assert tab["2026-01-01"] == [8329.1, 21057.9, -12728.8]


def test_effr_parse():
    t = '{"refRates":[{"effectiveDate":"2026-10-06","volumeInBillions":120},{"effectiveDate":"2026-10-05","volumeInBillions":121}]}'
    assert nyfed_markets.parse(t, "volumeInBillions") == [("2026-10-05", 121.0), ("2026-10-06", 120.0)]


def test_fiscaldata_parsers():
    rows = [{"record_date": "2026-08-31", "classification_desc": "Customs Duties", "current_month_gross_rcpt_amt": "23376797000"},
            {"record_date": "2026-08-31", "classification_desc": "Other", "current_month_gross_rcpt_amt": "1"}]
    assert fiscaldata.parse_customs(rows) == [("2026-08-01", 23376.797)]
    assert fiscaldata.parse_debt([{"record_date": "2026-10-06", "tot_pub_debt_out_amt": "40273025000000"}]) == [("2026-10-06", 40273.025)]


# ---------- 行事曆 ----------
def test_bls_ics_parse():
    r = relcal.parse_bls_ics((FX / "bls.ics").read_text())
    assert set(r) == {"cpi", "nfp"} and r["cpi"][0] == "2025-01-15"


def test_calendar_build_keeps_old_on_failure():
    old = {"releases": {"cpi": {"name_zh": "x", "dates": ["2026-11-10"], "source": "BLS ICS"}}}

    def boom():
        raise RuntimeError("down")
    new, failed = relcal.build(old, today=dt.date(2026, 10, 8), sources=[("BLS ICS", boom)])
    assert failed and new["releases"]["cpi"]["dates"] == ["2026-11-10"]
    assert relcal.next_date(new, "claims", dt.date(2026, 10, 8)) == "2026-10-08"  # 週四
    assert relcal.next_date(new, "h8", dt.date(2026, 10, 8)) == "2026-10-09"  # 週五


# ---------- catalog ----------
def test_us_catalog_consistent():
    cat = json.loads((Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "us.json").read_text())
    from macro_db.sources import REGISTRY
    seen = {}
    for c in cat["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                if "fetcher" in s:
                    assert s["fetcher"] in REGISTRY, s["sid"]
                    assert "params" in s
                    seen.setdefault(s["sid"], s["fetcher"])
                    assert seen[s["sid"]] == s["fetcher"]
                if s.get("display") == "ratio":
                    assert s["denominator"]
