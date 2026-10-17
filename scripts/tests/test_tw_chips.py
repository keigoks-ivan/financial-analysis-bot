"""台股籌碼（/tw-chips/）fetch / build 單元測試：解析器、單位換算、休市處理、整數門檻。

不連網；fixture 取自 TWSE／TAIFEX 官方回應的實際欄位格式。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tw_chips"))

import build  # noqa: E402
import fetch  # noqa: E402


# ---------------------------------------------------------------- fetch：基本轉換

def test_roc_and_slash_dates():
    assert fetch.roc_to_iso("105/10/03") == "2016-10-03"
    assert fetch.roc_to_iso("115/10/16") == "2026-10-16"
    assert fetch.roc_to_iso("總計") is None
    assert fetch.slash_to_iso("2023/10/16") == "2023-10-16"
    assert fetch.slash_to_iso("") is None


def test_to_num():
    assert fetch.to_num("9,219.52") == 9219.52
    assert fetch.to_num("-83,006,510") == -83006510 and isinstance(fetch.to_num("-83,006,510"), int)
    assert fetch.to_num("--") is None and fetch.to_num("") is None and fetch.to_num(None) is None


# ---------------------------------------------------------------- fetch：TWSE 解析

def test_parse_taiex_month():
    payload = {"stat": "OK", "data": [["105/10/03", "9,219.52", "9,256.58", "9,212.38", "9,234.20"],
                                      ["105/10/04", "9,228.66", "9,287.77", "9,224.45", "9,287.77"]]}
    rows = fetch.parse_taiex_month(payload)
    assert rows[0] == {"d": "2016-10-03", "o": 9219.52, "h": 9256.58, "l": 9212.38, "c": 9234.20}
    assert len(rows) == 2


def test_parse_turnover_month_unit_is_yuan():
    payload = {"stat": "OK", "fields": ["日期", "成交股數", "成交金額", "成交筆數", "發行量加權股價指數", "漲跌點數"],
               "data": [["105/10/03", "3,002,161,742", "55,597,456,402", "571,417", "9,234.20", "67.35"]]}
    rows = fetch.parse_turnover_month(payload)
    assert rows == [{"d": "2016-10-03", "amt": 55597456402, "sh": 3002161742}]
    assert build.yuan_to_yi(rows[0]["amt"]) == 555.97   # 約 556 億元


def test_closed_day_payloads_return_empty():
    """休市日：stat 非 OK（『很抱歉，沒有符合條件的資料』）→ 解析器回空/None，不會誤寫入。"""
    closed = {"stat": "很抱歉，沒有符合條件的資料!"}
    assert fetch.parse_taiex_month(closed) == []
    assert fetch.parse_turnover_month(closed) == []
    assert fetch.parse_bfi82u(closed, "2016-10-01") is None
    assert fetch.parse_margn(closed, "2016-10-01") is None


def test_parse_bfi82u_old_format_single_foreign_row():
    payload = {"stat": "OK", "data": [
        ["自營商(自行買賣)", "625,925,680", "708,932,190", "-83,006,510"],
        ["自營商(避險)", "3,393,521,889", "3,585,184,972", "-191,663,083"],
        ["投信", "404,300,250", "458,232,436", "-53,932,186"],
        ["外資及陸資", "19,761,488,595", "22,523,276,715", "-2,761,788,120"],
        ["合計", "24,185,236,414", "27,275,626,313", "-3,090,389,899"]]}
    r = fetch.parse_bfi82u(payload, "2016-10-31")
    assert r["f"] == [19761488595, 22523276715]
    assert r["t"] == [404300250, 458232436]
    assert r["dl"] == [625925680 + 3393521889, 708932190 + 3585184972]
    assert build.yuan_to_yi(r["f"][0] - r["f"][1]) == -27.62      # 外資賣超約 27.6 億


def test_parse_bfi82u_new_format_foreign_two_rows_are_summed():
    payload = {"stat": "OK", "data": [
        ["自營商(自行買賣)", "8,381,436,969", "18,560,032,105", "-10,178,595,136"],
        ["自營商(避險)", "28,653,271,647", "51,888,684,916", "-23,235,413,269"],
        ["投信", "43,848,499,145", "32,800,992,175", "11,047,506,970"],
        ["外資及陸資(不含外資自營商)", "356,324,360,692", "402,471,523,529", "-46,147,162,837"],
        ["外資自營商", "100", "40", "60"],
        ["合計", "437,207,568,453", "505,721,232,725", "-68,513,664,272"]]}
    r = fetch.parse_bfi82u(payload, "2026-10-16")
    assert r["f"] == [356324360692 + 100, 402471523529 + 40]
    assert r["dl"] == [8381436969 + 28653271647, 18560032105 + 51888684916]


def test_parse_bfi82u_incomplete_rows_rejected():
    payload = {"stat": "OK", "data": [["投信", "1", "2", "-1"]]}
    assert fetch.parse_bfi82u(payload, "2026-10-16") is None


def _margn_payload():
    return {"stat": "OK", "tables": [{"data": [
        ["融資(交易單位)", "343,600", "318,542", "7,624", "9,521,230", "9,538,664"],
        ["融券(交易單位)", "20,982", "30,004", "4,570", "229,150", "233,602"],
        ["融資金額(仟元)", "28,656,955", "28,942,556", "536,222", "646,415,871", "645,594,048"]]}]}


def test_parse_margn_and_unit_conversion():
    r = fetch.parse_margn(_margn_payload(), "2026-10-16")
    assert r == {"d": "2026-10-16", "mg": 9538664, "mg_p": 9521230, "sh": 233602, "sh_p": 229150,
                 "mga": 645594048, "mga_p": 646415871}
    # 仟元 → 億元：645,594,048 仟元 = 6,455.94 億元（幾千億量級，不是幾億）
    assert build.qianyuan_to_yi(r["mga"]) == 6455.94
    assert 1000 < build.qianyuan_to_yi(r["mga"]) < 20000


# ---------------------------------------------------------------- fetch：TAIFEX CSV

FUT_CSV = (
    "日期,商品名稱,身份別,多方交易口數,多方交易契約金額(千元),空方交易口數,空方交易契約金額(千元),"
    "多空交易口數淨額,多空交易契約金額淨額(千元),多方未平倉口數,多方未平倉契約金額(千元),"
    "空方未平倉口數,空方未平倉契約金額(千元),多空未平倉口數淨額,多空未平倉契約金額淨額(千元)\n"
    "2023/10/16,臺股期貨,自營商,15488,51629254,15700,52323916,-212,-694662,8056,26830225,7533,25088834,523,1741391\n"
    "2023/10/16,臺股期貨,投信,13111,43646208,13611,45309907,-500,-1663698,14137,47091823,10919,36377233,3218,10714590\n"
    "2023/10/16,臺股期貨,外資及陸資,92748,309121931,93714,312381778,-966,-3259847,31454,104783640,32874,109506622,-1420,-4722982\n"
)


def test_parse_fut_inst_csv():
    rows = fetch.parse_fut_inst_csv(FUT_CSV)
    assert rows == [{"d": "2023-10-16", "dl": [8056, 7533], "t": [14137, 10919], "f": [31454, 32874]}]
    assert rows[0]["f"][0] - rows[0]["f"][1] == -1420      # 與官方『多空未平倉口數淨額』一致


def test_parse_fut_inst_csv_ignores_other_contracts_and_error_page():
    other = FUT_CSV.replace("臺股期貨", "電子期貨")
    assert fetch.parse_fut_inst_csv(other) == []
    assert fetch.parse_fut_inst_csv("<html>alert('DateTime error')</html>") == []


OPT_CSV = (
    "日期,商品名稱,買賣權別,身份別,買方交易口數,買方交易契約金額(千元),賣方交易口數,賣方交易契約金額(千元),"
    "交易口數買賣淨額,交易契約金額買賣淨額(千元),買方未平倉口數,買方未平倉契約金額(千元),"
    "賣方未平倉口數,賣方未平倉契約金額(千元),未平倉口數買賣淨額,未平倉契約金額買賣淨額(千元)\n"
    "2026/10/14,臺指選擇權,CALL,自營商,74050,575782,71213,374574,2837,201208,31507,934463,17627,929293,13880,5170\n"
    "2026/10/14,臺指選擇權,CALL,投信,0,0,2540,168633,-2540,-168633,0,0,4109,245318,-4109,-245318\n"
    "2026/10/14,臺指選擇權,CALL,外資及陸資,100608,493949,105616,495814,-5008,-1864,14620,831951,14975,999830,-355,-167879\n"
    "2026/10/14,臺指選擇權,PUT,自營商,79476,408924,86989,391947,-7513,16977,18453,314549,15340,182193,3113,132356\n"
    "2026/10/14,臺指選擇權,PUT,投信,0,0,0,0,0,0,165,1034,0,0,165,1034\n"
    "2026/10/14,臺指選擇權,PUT,外資及陸資,103663,441864,105113,479830,-1450,-37965,9603,538018,7952,481532,1651,56486\n"
)


def test_parse_opt_inst_csv_net_matches_official():
    rows = fetch.parse_opt_inst_csv(OPT_CSV)
    assert len(rows) == 1
    f_call = rows[0]["c"]["f"]
    assert f_call == [14620, 14975, 831951, 999830]
    assert f_call[0] - f_call[1] == -355                       # 官方『未平倉口數買賣淨額』
    assert f_call[2] - f_call[3] == -167879                    # 官方『未平倉契約金額買賣淨額(千元)』
    assert build.qianyuan_to_yi(f_call[2] - f_call[3]) == -1.68    # 千元 → 億元


def test_parse_pcr_csv():
    text = ("日期,賣權成交量,買權成交量,買賣權成交量比率%,賣權未平倉量,買權未平倉量,買賣權未平倉量比率%\n"
            "2016/10/14,253236,250703,101.01,560341,435933,128.54,\n"
            "2016/10/13,335618,286315,117.22,539814,408449,132.16,\n")
    rows = fetch.parse_pcr_csv(text)
    assert [r["d"] for r in rows] == ["2016-10-13", "2016-10-14"]      # 官方由新到舊，輸出依日期排序
    assert rows[1]["vr"] == 101.01 and rows[1]["or"] == 128.54
    assert rows[1]["pv"] == 253236 and rows[1]["co"] == 435933


def test_parse_large_csv_only_tx_all_months():
    text = ("日期,商品(契約),商品名稱(契約名稱),到期月份(週別),交易人類別,前五大交易人買方,前五大交易人賣方,"
            "前十大交易人買方,前十大交易人賣方,全市場未沖銷部位數\n"
            "2026/10/16,TX     ,臺股期貨(TX+MTX/4+TMF/20)           ,202610  ,0,68157,53675,75382,72888,106162\n"
            "2026/10/16,TX     ,臺股期貨(TX+MTX/4+TMF/20)           ,999999  ,0,78348,60553,87910,87591,132820\n"
            "2026/10/16,TX     ,臺股期貨(TX+MTX/4+TMF/20)           ,999999  ,1,78348,60553,84135,87591,132820\n"
            "2026/10/16,CA     ,南亞期貨                            ,999999  ,0,1,1,1,1,1\n")
    rows = fetch.parse_large_csv(text)
    assert rows == [{"d": "2026-10-16", "a": [78348, 60553, 87910, 87591], "s": [78348, 60553, 84135, 87591],
                     "oi": 132820}]


def test_parse_fred_csv_skips_missing_dot():
    text = "observation_date,DEXTAUS\n2026-10-08,31.9400\n2026-10-09,.\n2026-10-12,31.9\n"
    assert fetch.parse_fred_csv(text) == [{"d": "2026-10-08", "v": 31.94}, {"d": "2026-10-12", "v": 31.9}]


def test_finmind_conversion_matches_taifex_shape():
    data = [{"futures_id": "TX", "date": "2023-10-16", "institutional_investors": n,
             "long_open_interest_balance_volume": lo, "short_open_interest_balance_volume": so}
            for n, lo, so in (("自營商", 8056, 7533), ("投信", 14137, 10919), ("外資", 31454, 32874))]
    assert fetch.finmind_fut_rows(data) == fetch.parse_fut_inst_csv(FUT_CSV)


# ---------------------------------------------------------------- fetch：存檔、休市記錄、缺漏判斷

def test_store_is_incremental_and_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "DATA", tmp_path)
    s = fetch.Store("inst")
    assert s.add({"d": "2026-10-15", "f": [1, 2]}) is True
    assert s.add({"d": "2026-10-15", "f": [1, 2]}) is False        # 同日同內容不重寫
    assert s.add({"d": "2026-10-16", "f": [3, 4]}) is True
    assert len((tmp_path / "inst.jsonl").read_text().splitlines()) == 2
    s2 = fetch.Store("inst")                                        # 重新載入 = 可續跑
    assert s2.has("2026-10-15") and s2.last() == "2026-10-16"


def test_missing_trading_days_skips_known_holes(tmp_path, monkeypatch):
    """休市日不在日曆（taiex）裡 → 不會被當缺口；查無資料 ≥3 次且非近期 → 不再重抓。"""
    import datetime as dt
    monkeypatch.setattr(fetch, "DATA", tmp_path)
    cal = fetch.Store("taiex")
    for d in ("2026-09-01", "2026-09-02", "2026-09-04", "2026-10-15"):     # 09-03 是休市日，不在日曆
        cal.add({"d": d, "o": 1, "h": 1, "l": 1, "c": 1})
    inst = fetch.Store("inst")
    inst.add({"d": "2026-09-02", "f": [0, 0], "t": [0, 0], "dl": [0, 0]})
    st = fetch.State()
    for _ in range(3):
        st.bump_gap("inst", "2026-09-04")
    today = dt.date(2026, 10, 16)
    todo = fetch.missing_trading_days(inst, "inst", st, dt.date(2016, 10, 1), today, None)
    assert todo == ["2026-09-01", "2026-10-15"]    # 09-03 不是交易日；09-04 已重試 3 次放棄；09-02 已有
    # 近期（5 天內）即使有失敗紀錄也要再試（當天資料可能還沒公布）
    for _ in range(3):
        st.bump_gap("inst", "2026-10-15")
    assert "2026-10-15" in fetch.missing_trading_days(inst, "inst", st, dt.date(2016, 10, 1), today, None)


def test_state_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "DATA", tmp_path)
    st = fetch.State()
    st.mark_month("taiex", "2016-10")
    st.bump_gap("margin", "2026-10-15")
    st.save()
    st2 = fetch.State()
    assert st2.month_done("taiex", "2016-10") and not st2.month_done("taiex", "2016-11")
    assert st2.gap_attempts("margin", "2026-10-15") == 1


def test_taifex_window_is_three_years_plus_one_day():
    import datetime as dt
    assert fetch._taifex_window(dt.date(2026, 10, 16)) == dt.date(2023, 10, 17)
    assert fetch._taifex_window(dt.date(2028, 2, 29)) == dt.date(2025, 3, 1)


# ---------------------------------------------------------------- build

def test_rolling_and_cumulate():
    xs = [1.0, 2.0, 3.0, None, 5.0, 6.0]
    assert build.rolling_sum(xs, 2) == [None, 3.0, 5.0, None, None, 11.0]
    assert build.rolling_mean([1, 2, 3, 4], 3) == [None, None, 2.0, 3.0]
    assert build.cumulate([1.0, None, 2.5]) == [1.0, None, 3.5]


def test_ffill_limited():
    assert build.ffill([1.0, None, None, 2.0, None], max_gap=1) == [1.0, 1.0, None, 2.0, None]   # 最後真實值之後不補


def test_margin_final_uses_next_day_prior_balance():
    cal = ["2026-10-14", "2026-10-15", "2026-10-16"]
    rows = {
        "2026-10-14": {"d": "2026-10-14", "mg": 100, "mg_p": 90, "sh": 10, "sh_p": 9, "mga": 1000, "mga_p": 900},
        "2026-10-15": {"d": "2026-10-15", "mg": 110, "mg_p": 101, "sh": 11, "sh_p": 10, "mga": 1100, "mga_p": 1010},
    }
    out = build.margin_final(cal, rows)
    assert out["2026-10-14"]["mg"] == 101 and out["2026-10-14"]["final"] is True      # 以 10-15 的前日餘額為準
    assert out["2026-10-15"]["mg"] == 110 and out["2026-10-15"]["final"] is False     # 尚無下一日 → 用今日餘額
    assert "2026-10-16" not in out                                                     # 沒資料的日子留空


def test_ratio_pct_integer_inputs():
    assert build.ratio_pct(233602, 9538664) == 2.45      # 券資比 = 融券張 ÷ 融資張
    assert build.ratio_pct(5, 0) is None and build.ratio_pct(None, 10) is None


def test_align_leaves_missing_days_null():
    cal = ["2026-10-14", "2026-10-15"]
    assert build.align(cal, {"2026-10-15": {"v": 3}}, lambda r: r["v"]) == [None, 3]


def test_unit_conversions():
    assert build.yuan_to_yi(-46147162837) == -461.47
    assert build.qianyuan_to_yi(646415871) == 6464.16
    assert build.yuan_to_yi(None) is None


def test_build_end_to_end_small(tmp_path, monkeypatch):
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    monkeypatch.setattr(build, "SRC", src)
    monkeypatch.setattr(build, "OUT", out)
    monkeypatch.setattr(build, "DISPLAY_START", "2026-10-14")
    days = ["2026-10-14", "2026-10-15", "2026-10-16"]
    (src / "taiex.jsonl").write_text("\n".join(
        json.dumps({"d": d, "o": 1, "h": 2, "l": 0.5, "c": 1.5 + i}) for i, d in enumerate(days)) + "\n")
    (src / "inst.jsonl").write_text(json.dumps(
        {"d": "2026-10-16", "f": [200_000_000_000, 100_000_000_000], "t": [1, 1], "dl": [1, 1]}) + "\n")
    assert build.main() == 0
    inst = json.loads((out / "inst.json").read_text())
    assert inst["f"] == [None, None, 1000.0]                 # 外資買賣超 1000 億元
    cal = json.loads((out / "cal.json").read_text())["t"]
    assert cal == days
    meta = json.loads((out / "meta.json").read_text())
    assert {s["key"]: s["n"] for s in meta["series"]}["inst"] == 1


def test_no_negative_zero_after_unit_conversion():
    assert str(build.qianyuan_to_yi(-3)) == "0.0"
    assert str(build.yuan_to_yi(-3)) == "0.0"


def test_export_csv_flat_english_columns(tmp_path, monkeypatch):
    src = tmp_path / "src"
    src.mkdir()
    monkeypatch.setattr(build, "SRC", src)
    monkeypatch.setattr(build, "CSV_OUT", tmp_path / "csv")
    (src / "inst.jsonl").write_text(json.dumps(
        {"d": "2026-10-16", "f": [356324360692, 402471523529], "t": [43848499145, 32800992175],
         "dl": [37034708616, 70448717021]}) + "\n")
    (src / "margin.jsonl").write_text("\n".join(json.dumps(r) for r in (
        {"d": "2026-10-15", "mg": 9521231, "mg_p": 9467239, "sh": 229150, "sh_p": 228653, "mga": 646415015, "mga_p": 651556359},
        {"d": "2026-10-16", "mg": 9538664, "mg_p": 9521230, "sh": 233602, "sh_p": 229150, "mga": 645594048, "mga_p": 646415871},
    )) + "\n")
    counts = build.export_csv()
    assert counts["inst"] == 1 and counts["margin"] == 2 and counts["fut_inst"] == 0
    import csv as _csv
    inst = list(_csv.DictReader(open(tmp_path / "csv" / "inst.csv", encoding="utf-8")))
    assert list(inst[0])[0] == "date"
    assert inst[0]["foreign_net_twd"] == str(356324360692 - 402471523529)
    assert inst[0]["foreign_net_yi"] == "-461.47"
    mg = list(_csv.DictReader(open(tmp_path / "csv" / "margin.csv", encoding="utf-8")))
    assert mg[0]["margin_balance_lots_final"] == "9521230" and mg[0]["is_final"] == "1"   # 10-15 以 10-16 的前日餘額定稿
    assert mg[1]["margin_balance_lots_final"] == "9538664" and mg[1]["is_final"] == "0"
    assert mg[1]["margin_balance_yi"] == "6455.94"
