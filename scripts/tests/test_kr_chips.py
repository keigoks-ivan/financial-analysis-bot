"""韓股籌碼（/kr-chips/）fetch / build 單元測試：解析器、單位換算、休市處理、累計與比率。

不連網；fixture 取自 KOFIA FreeSIS 與 Naver 行動版 API 的實際欄位格式（數字取自 2026-10-14／15 的實際回應）。
所有測試一律把輸出路徑指到 tmp_path（autouse fixture），不會寫到真資料目錄。
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "kr_chips"))

import build  # noqa: E402
import fetch  # noqa: E402


@pytest.fixture(autouse=True)
def _isolate_paths(tmp_path, monkeypatch):
    """台股頁出過測試把 CSV 寫進真資料目錄的錯：所有輸出路徑預設就指到 tmp。"""
    monkeypatch.setattr(fetch, "DATA", tmp_path / "fetch_data")
    monkeypatch.setattr(build, "SRC", tmp_path / "src")
    monkeypatch.setattr(build, "OUT", tmp_path / "out")
    monkeypatch.setattr(build, "CSV_OUT", tmp_path / "csv")


# ---------------------------------------------------------------- fetch：基本轉換

def test_ymd_to_iso():
    assert fetch.ymd_to_iso("20261015") == "2026-10-15"
    assert fetch.ymd_to_iso("2026-10-15") is None
    assert fetch.ymd_to_iso(None) is None


def test_num():
    assert fetch.num("5,554.22") == 5554.22
    assert fetch.num("+13,967") == 13967 and isinstance(fetch.num("+13,967"), int)
    assert fetch.num("-37,637") == -37637
    assert fetch.num("") is None and fetch.num(None) is None and fetch.num("-") is None
    assert fetch.num(96912122) == 96912122


# ---------------------------------------------------------------- fetch：KOFIA 解析

def test_parse_kofia_index_fields_and_zero_close_dropped():
    rows = [{"TMPV1": "20261015", "TMPV2": 5554.22, "TMPV3": 385805100, "TMPV4": 28639947,
             "TMPV5": 4581178619, "TMPV6": 1749570741, "TMPV7": 38.19},
            {"TMPV1": "19980101", "TMPV2": 0, "TMPV3": 0, "TMPV4": 0, "TMPV5": 0, "TMPV6": 0, "TMPV7": 0}]
    out = fetch.parse_kofia_index(rows)
    assert out == [{"d": "2026-10-15", "c": 5554.22, "vol": 385805100, "amt": 28639947,
                    "mcap": 4581178619, "fmcap": 1749570741, "fpct": 38.19}]
    # 外國人持股比重 ≈ 外國人持股市值 ÷ 上市總市值（欄位對錯的獨立檢查）
    assert abs(out[0]["fmcap"] / out[0]["mcap"] * 100 - out[0]["fpct"]) < 0.01


def test_parse_kofia_deposit_matches_press_figures():
    """2026-10-14 韓國媒體引用金融投資協會：預託金 97 兆 4280 億、反向交易 893 億。"""
    rows = [{"TMPV1": "20261014", "TMPV2": 97428012, "TMPV3": 36737435, "TMPV4": 107642131,
             "TMPV5": 1357473, "TMPV6": 89336, "TMPV7": 7.2}]
    r = fetch.parse_kofia_deposit(rows)[0]
    assert r["dep"] == 97428012 and build.mil_to_eok(r["dep"]) == 974280.12     # 97 兆 4280 億
    assert build.mil_to_eok(r["forced"]) == 893.36                              # 893 億
    assert r["forced_pct"] == 7.2


def test_parse_kofia_credit_split_adds_up():
    rows = [{"TMPV1": "20261014", "TMPV2": 33705742, "TMPV3": 26268574, "TMPV4": 7437167, "TMPV5": 31485,
             "TMPV6": 26308, "TMPV7": 5177, "TMPV8": 0, "TMPV9": 27054769},
            {"TMPV1": "19980130", "TMPV2": 0, "TMPV3": 0, "TMPV4": 0, "TMPV5": 0, "TMPV6": 0, "TMPV7": 0,
             "TMPV8": 0, "TMPV9": 0}]
    out = fetch.parse_kofia_credit(rows)
    assert len(out) == 1                                   # 融資合計為 0 的早期列丟棄
    r = out[0]
    # 來源各欄各自四捨五入到百萬韓元，加總會差 1 左右
    assert abs(r["tot"] - (r["kospi"] + r["kosdaq"])) <= 2
    assert abs(r["sh_tot"] - (r["sh_kospi"] + r["sh_kosdaq"])) <= 2
    assert build.mil_to_eok(r["tot"]) == 337057.42     # 33 兆 7057 億


def test_parse_kofia_lend_total_picks_total_row_only():
    rows = [{"TMPV1": "삼성전자", "TMPV2": "005930", "TMPV3": 1764189, "TMPV4": 1627242, "TMPV5": 82245732, "TMPV6": 17271604},
            {"TMPV1": "합계", "TMPV2": "-", "TMPV3": 42594706, "TMPV4": 32925006, "TMPV5": 3087613687, "TMPV6": 138991227},
            {"TMPV1": "전체대비", "TMPV2": "-", "TMPV3": 100, "TMPV4": 100, "TMPV5": 100, "TMPV6": 100}]
    r = fetch.parse_kofia_lend_total(rows, "2026-10-15")
    assert r == {"d": "2026-10-15", "new": 42594706, "ret": 32925006, "bal": 3087613687, "bal_amt": 138991227}


def test_parse_kofia_lend_total_holiday_is_none():
    assert fetch.parse_kofia_lend_total([], "2026-10-09") is None
    assert fetch.parse_kofia_lend_total([{"TMPV1": "합계", "TMPV2": "-", "TMPV5": 0}], "2026-10-09") is None


# ---------------------------------------------------------------- fetch：Naver 解析

def test_parse_naver_trend_signs_and_units():
    j = {"bizdate": "20261015", "personalValue": "+13,967", "foreignValue": "-37,637", "institutionalValue": "+17,176"}
    assert fetch.parse_naver_trend(j, "2026-10-15") == {"d": "2026-10-15", "p": 13967, "f": -37637, "i": 17176}


def test_parse_naver_trend_holiday_and_mismatched_date_are_none():
    zero = {"bizdate": "20261010", "personalValue": "0", "foreignValue": "0", "institutionalValue": "0"}
    assert fetch.parse_naver_trend(zero, "2026-10-10") is None
    j = {"bizdate": "20261016", "personalValue": "-5,126", "foreignValue": "+3,637", "institutionalValue": "-6,815"}
    assert fetch.parse_naver_trend(j, "2026-10-15") is None       # 回的不是請求的那一天
    assert fetch.parse_naver_trend({}, "2026-10-15") is None


def test_parse_naver_price():
    rows = [{"localTradedAt": "2026-10-16", "closePrice": "5,668.05", "openPrice": "5,653.99",
             "highPrice": "5,809.94", "lowPrice": "5,590.33"},
            {"localTradedAt": "bad", "closePrice": "1", "openPrice": "1", "highPrice": "1", "lowPrice": "1"}]
    assert fetch.parse_naver_price(rows) == [{"d": "2026-10-16", "o": 5653.99, "h": 5809.94, "l": 5590.33, "c": 5668.05}]


def test_parse_fred_csv_skips_missing_dot():
    text = "observation_date,DEXKOUS\n2026-10-07,1339.12\n2026-10-08,\n2026-10-09,1342.13\n2026-10-12,.\n"
    assert fetch.parse_fred_csv(text) == [{"d": "2026-10-07", "v": 1339.12}, {"d": "2026-10-09", "v": 1342.13}]


# ---------------------------------------------------------------- fetch：存檔與日曆

def test_store_is_incremental_and_idempotent():
    s = fetch.Store("inst_kospi")
    assert s.add({"d": "2026-10-14", "p": 1, "f": 2, "i": 3}) is True
    assert s.add({"d": "2026-10-14", "p": 1, "f": 2, "i": 3}) is False       # 內容沒變不重寫
    assert s.add({"d": "2026-10-14", "p": 1, "f": 9, "i": 3}) is True        # 有修正才 append
    s2 = fetch.Store("inst_kospi")
    assert s2.rows["2026-10-14"]["f"] == 9                                   # 讀入時以最後一行為準
    assert len(s2.path.read_text().splitlines()) == 2
    s2.compact()
    assert len(s2.path.read_text().splitlines()) == 1


def test_calendar_is_union_of_kofia_and_naver_dates():
    k, p = fetch.Store("kospi"), fetch.Store("px_kospi")
    k.add({"d": "2026-10-14", "c": 1})
    p.add({"d": "2026-10-14", "c": 1})
    p.add({"d": "2026-10-15", "c": 2})
    assert fetch.calendar() == ["2026-10-14", "2026-10-15"]    # KOFIA 晚一天，Naver 當天就有


def test_missing_days_skips_known_holes_and_respects_window():
    import datetime as dt
    p = fetch.Store("px_kospi")
    for d in ("2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15"):
        p.add({"d": d})
    st = fetch.State()
    store = fetch.Store("inst_kospi")
    store.add({"d": "2026-10-13", "p": 1, "f": 1, "i": 1})
    for _ in range(3):
        st.bump_gap("inst_kospi", "2026-10-12")
    today = dt.date(2026, 10, 30)
    out = fetch.missing_days(store, "inst_kospi", st, "2005-01-03", today, None)
    assert out == ["2026-10-15", "2026-10-14"]          # 最新日在前；已有的 10-13、查無資料滿 3 次且非近期的 10-12 都略過
    out_recent = fetch.missing_days(store, "inst_kospi", st, "2005-01-03", today, 5)
    assert out_recent == []                              # 只看最近 5 天：10-14、10-15 都在窗外，不抓


def test_state_merge_does_not_clobber_other_series():
    a, b = fetch.State(), fetch.State()
    a.bump_gap("lend", "2026-10-01")
    b.bump_gap("inst_kospi", "2026-10-02")
    a.save()
    b.save()
    c = fetch.State()
    assert c.gap_attempts("lend", "2026-10-01") == 1
    assert c.gap_attempts("inst_kospi", "2026-10-02") == 1


# ---------------------------------------------------------------- build：換算與純函式

def test_unit_conversion_million_to_100m():
    assert build.mil_to_eok(100) == 1.0               # 100 百萬 = 1 億
    assert build.mil_to_eok(97428012) == 974280.12
    assert build.mil_to_eok(None) is None


def test_no_negative_zero_after_conversion():
    assert str(build.mil_to_eok(-0.001)) == "0.0"


def test_rolling_mean_needs_full_window():
    assert build.rolling_mean([1, 2, 3, 4], 2) == [None, 1.5, 2.5, 3.5]
    assert build.rolling_mean([1, None, 3], 2) == [None, None, None]


def test_ratio_pct_and_total_mcap():
    assert build.ratio_pct(139, 5010, 2) == 2.77
    assert build.ratio_pct(1, 0) is None and build.ratio_pct(None, 5) is None
    assert build.total_mcap(10, 5) == 15 and build.total_mcap(None, 5) is None


def test_ffill_limited_and_never_extends_past_last_real():
    assert build.ffill([1, None, None, 4, None]) == [1, 1, 1, 4, None]
    assert build.ffill([1] + [None] * 7 + [9], max_gap=5) == [1, 1, 1, 1, 1, 1, None, None, 9]


def test_ban_window_flags(tmp_path, monkeypatch):
    src = tmp_path / "src"
    src.mkdir()
    days = ["2023-11-03", "2023-11-06", "2025-03-28", "2025-03-31"]
    with (src / "px_kospi.jsonl").open("w") as f:
        for d in days:
            f.write(json.dumps({"d": d, "o": 1, "h": 1, "l": 1, "c": 1}) + "\n")
    monkeypatch.setattr(build, "DISPLAY_START", "2023-01-01")
    assert build.main() == 0
    cal = json.loads((tmp_path / "out" / "cal.json").read_text())
    assert cal["ban"] == [0, 1, 1, 0]                 # 2023-11-06 起、2025-03-30 止（含）


# ---------------------------------------------------------------- build：端到端

def _write(src: Path, name: str, rows: list[dict]):
    src.mkdir(parents=True, exist_ok=True)
    with (src / f"{name}.jsonl").open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def test_build_end_to_end_small(tmp_path, monkeypatch):
    src, out = tmp_path / "src", tmp_path / "out"
    monkeypatch.setattr(build, "DISPLAY_START", "2026-10-14")
    d14, d15, d16 = "2026-10-14", "2026-10-15", "2026-10-16"
    _write(src, "px_kospi", [{"d": d, "o": 10, "h": 12, "l": 9, "c": 11 + i} for i, d in enumerate((d14, d15, d16))])
    _write(src, "px_kosdaq", [{"d": d, "o": 1, "h": 2, "l": 1, "c": 2} for d in (d14, d15, d16)])
    # KOFIA 晚一天：沒有 10-16
    kf = {"vol": 1, "amt": 2864, "mcap": 458_000_000, "fmcap": 174_000_000, "fpct": 38.0}
    _write(src, "kospi", [{"d": d, "c": 5000, **kf} for d in (d14, d15)])
    _write(src, "kosdaq", [{"d": d, "c": 800, "vol": 1, "amt": 100, "mcap": 43_000_000, "fmcap": 5_000_000, "fpct": 11.0}
                           for d in (d14, d15)])
    _write(src, "inst_kospi", [{"d": d14, "p": -3203, "f": -11614, "i": 7876}, {"d": d15, "p": 13967, "f": -37637, "i": 17176},
                               {"d": d16, "p": -5126, "f": 3637, "i": -6815}])
    _write(src, "inst_kosdaq", [{"d": d15, "p": -748, "f": 2228, "i": -1614}])
    _write(src, "deposit", [{"d": d15, "dep": 96912122, "x3": 1, "x4": 2, "unpaid": 1392561, "forced": 80498, "forced_pct": 5.9}])
    _write(src, "credit", [{"d": d15, "tot": 32749897, "kospi": 25532078, "kosdaq": 7217819, "sh_tot": 26124,
                            "sh_kospi": 21544, "sh_kosdaq": 4581, "x8": 0, "x9": 1}])
    _write(src, "lend", [{"d": d15, "new": 1, "ret": 1, "bal": 3087613687, "bal_amt": 138991227}])
    _write(src, "usdkrw", [{"d": d14, "v": 1343.0}])
    assert build.main() == 0

    def load(n):
        return json.loads((out / n).read_text())
    cal = load("cal.json")["t"]
    assert cal == [d14, d15, d16]                                    # KOFIA 與 Naver 日曆聯集
    k = load("kospi.json")
    assert k["c"] == [11, 12, 13] and k["amt"] == [28.64, 28.64, None]     # 最新一天 KOFIA 欄位留空，不補假值
    assert k["mcap"][0] == 4580000.0                                 # 458,000,000 百萬 = 458 萬億
    inst = load("inst.json")
    assert inst["kf"] == [-11614, -37637, 3637] and inst["qf"] == [None, 2228, None]
    dep = load("deposit.json")
    assert dep["dep"] == [None, 969121.22, None] and dep["forced"][1] == 804.98
    cr = load("credit.json")
    assert cr["tot"][1] == 327498.97
    assert cr["r_tot"][1] == round(32749897 / (458_000_000 + 43_000_000) * 100, 3)
    assert cr["r_kospi"][1] == round(25532078 / 458_000_000 * 100, 3)
    ld = load("lend.json")
    assert ld["amt"][1] == 1389912.27
    assert ld["ratio"][1] == round(138991227 / (458_000_000 + 43_000_000) * 100, 3)
    meta = load("meta.json")
    assert meta["cal_first"] == d14 and meta["cal_last"] == d16 and meta["ban"] == ["2023-11-06", "2025-03-30"]
    assert {s["key"] for s in meta["series"]} >= {"px_kospi", "kospi", "inst_kospi", "deposit", "credit", "lend", "usdkrw"}
    # 每個欄式陣列都對齊日曆長度
    for name in ("kospi", "kosdaq", "inst", "deposit", "credit", "lend", "fx"):
        for key, arr in load(f"{name}.json").items():
            assert len(arr) == len(cal), (name, key)


def test_export_csv_flat_english_columns(tmp_path):
    import csv as _csv
    src = tmp_path / "src"
    _write(src, "kospi", [{"d": "2026-10-15", "c": 5554.22, "vol": 385805100, "amt": 28639947, "mcap": 4581178619,
                           "fmcap": 1749570741, "fpct": 38.19}])
    _write(src, "inst_kospi", [{"d": "2026-10-15", "p": 13967, "f": -37637, "i": 17176}])
    counts = build.export_csv()
    assert counts["kospi"] == 1 and counts["inst_kospi"] == 1
    rows = list(_csv.DictReader(open(tmp_path / "csv" / "kospi.csv", encoding="utf-8")))
    assert rows[0]["date"] == "2026-10-15" and float(rows[0]["turnover_100m_krw"]) == 286399.47
    assert float(rows[0]["foreign_holding_pct"]) == 38.19
    inst = list(_csv.DictReader(open(tmp_path / "csv" / "inst_kospi.csv", encoding="utf-8")))
    assert inst[0]["foreign_net_100m_krw"] == "-37637"
    assert not list(Path(build.__file__).resolve().parents[2].glob("data/kr_chips/csv/_test*"))   # 沒寫到真目錄


def test_sync_to_v7_copies_only_changed_files_and_skips_state(tmp_path):
    import sync_to_v7
    src, dest = tmp_path / "s", tmp_path / "d"
    (src / "csv").mkdir(parents=True)
    (src / "kospi.jsonl").write_text('{"d":"2026-10-15"}\n')
    (src / "csv" / "kospi.csv").write_text("date\n2026-10-15\n")
    (src / "README.md").write_text("x")
    (src / "_state.json").write_text("{}")
    assert sync_to_v7.sync(src, dest) == (3, 0)
    assert not (dest / "_state.json").exists()                       # 抓取進度不同步
    assert sync_to_v7.sync(src, dest) == (0, 3)                      # 再跑一次：全部未變動
    (src / "kospi.jsonl").write_text('{"d":"2026-10-15"}\n{"d":"2026-10-16"}\n')
    assert sync_to_v7.sync(src, dest, dry_run=True) == (1, 2)
    assert (dest / "kospi.jsonl").read_text().count("\n") == 1       # dry-run 不寫
    assert sync_to_v7.sync(src, dest) == (1, 2)
    assert (dest / "kospi.jsonl").read_text().count("\n") == 2
