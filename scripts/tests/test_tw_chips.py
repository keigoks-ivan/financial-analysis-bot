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
    monkeypatch.setattr(build, "CSV_OUT", tmp_path / "csv")
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


# ---------------------------------------------------------------- 借券（TWT72U／TWT93U／市值週報）

def _twt72u(date="20261016"):
    f = ["證券代號", "證券名稱", "前日借券餘額(1)股", "本日異動股借券(2)", "本日異動股還券(3)",
         "本日借券餘額股(4)=(1)+(2)-(3)", "本日收盤價(5)單位：元", "借券餘額市值單位：元(6)=(4)*(5)", "市場別"]
    return {"stat": "OK", "date": date, "fields": f, "data": [
        ["2330", "台積電", "100", "0", "0", "100", "1,000.00", "100,000", "集中市場"],
        ["2317", "鴻海", "200", "0", "50", "150", "200.50", "30,075", "集中市場"],
        ["6488", "環球晶", "10", "0", "0", "10", "400.00", "4,000", "櫃檯買賣中心"],
        ["合計", "　", "250", "0", "50", "250", "　", "130,075", "集中市場"],
        ["合計", "　", "10", "0", "0", "10", "　", "4,000", "櫃檯買賣中心"],
        ["合計", "　", "260", "0", "50", "260", "　", "134,075", "整體市場"],
    ]}


def _twt93u(date="20261016"):
    f = ["代號", "名稱", "前日餘額", "賣出", "買進", "現券", "今日餘額", "次一營業日限額",
         "前日餘額", "當日賣出", "當日還券", "當日調整", "當日餘額", "次一營業日可限額", "備註"]

    def row(code, bal):
        return [code, "x", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", bal, "0", " "]
    return {"stat": "OK", "date": date, "fields": f, "data": [
        row("2330", "40"), row("2317", "1,000"), row("0050", "0"), row("9999", "5"),
        ["", "合計", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1,045", "0", " "]]}


def test_parse_lending_total_takes_listed_total_row_only():
    r = fetch.parse_lending_total(_twt72u(), "2026-10-16")
    assert r["lend_sh"] == 250 and r["lend_amt"] == 130075          # 集中市場合計，不是整體市場的 260／134,075
    assert r["px"] == {"2330": 1000.0, "2317": 200.5, "6488": 400.0}


def test_parse_lending_total_rejects_wrong_date_and_missing_total():
    assert fetch.parse_lending_total(_twt72u("20261015"), "2026-10-16") is None   # 休市日被導到別天
    p = _twt72u()
    p["data"] = [r for r in p["data"] if not (r[0] == "合計" and r[8] == "集中市場")]
    assert fetch.parse_lending_total(p, "2026-10-16") is None
    assert fetch.parse_lending_total({"stat": "很抱歉，沒有符合條件的資料!"}, "2026-10-16") is None
    p = _twt72u()
    p["fields"][5] = "改版後欄位"
    assert fetch.parse_lending_total(p, "2026-10-16") is None


def test_parse_short_balance_amount_is_shares_times_close_and_tracks_missing_price():
    px = fetch.parse_lending_total(_twt72u(), "2026-10-16")["px"]
    r = fetch.parse_short_balance(_twt93u(), "2026-10-16", px)
    assert r["slb_sh"] == 40 + 1000 + 5
    assert r["slb_amt"] == 40 * 1000.0 + 1000 * 200.5               # 9999 沒有收盤價，不計入金額
    assert r["slb_nopx"] == 5
    assert fetch.parse_short_balance(_twt93u("20261015"), "2026-10-16", px) is None
    bad = _twt93u()
    bad["fields"][12] = "改版"
    assert fetch.parse_short_balance(bad, "2026-10-16", px) is None


def test_parse_mktcap_xls_excel_serial_to_date(monkeypatch):
    import types

    class Sheet:
        nrows = 4

        def row_values(self, r):
            return [["表頭", "", ""], ["日期", "總市值", ""], [46311.0, 1541834.31, ""], [46304.0, "1613576.55", ""]][r]

    class Book:
        def sheet_by_index(self, i):
            return Sheet()
    fake = types.SimpleNamespace(open_workbook=lambda *a, **k: Book())
    monkeypatch.setitem(sys.modules, "xlrd", fake)
    rows = fetch.parse_mktcap_xls("x.xls")
    assert rows == [{"d": "2026-10-16", "cap": 1541834.31}, {"d": "2026-10-09", "cap": 1613576.55}]


def test_weekly_cap_ratio_only_on_week_end_days_and_in_percent():
    cal = ["2026-10-14", "2026-10-15", "2026-10-16"]
    sbl = {d: {"slb_amt": 1.473e12, "lend_amt": 3.2819e12} for d in cal}
    cap = {"2026-10-16": {"d": "2026-10-16", "cap": 1541834.31}}        # 億元
    assert build.weekly_cap_ratio(cal, sbl, cap, "slb_amt") == [None, None, round(1.473e12 / 1541834.31e8 * 100, 3)]
    assert build.weekly_cap_ratio(cal, sbl, cap, "lend_amt")[2] == 2.129
    assert build.weekly_cap_ratio(cal, {}, cap, "slb_amt") == [None, None, None]   # 當天沒借券資料就不算


def test_build_and_csv_with_sbl(tmp_path, monkeypatch):
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    monkeypatch.setattr(build, "SRC", src)
    monkeypatch.setattr(build, "OUT", out)
    monkeypatch.setattr(build, "CSV_OUT", tmp_path / "csv")
    monkeypatch.setattr(build, "DISPLAY_START", "2026-10-14")
    days = ["2026-10-14", "2026-10-15", "2026-10-16"]
    (src / "taiex.jsonl").write_text("\n".join(
        json.dumps({"d": d, "o": 1, "h": 2, "l": 0.5, "c": 1.5}) for d in days) + "\n")
    (src / "sbl.jsonl").write_text("\n".join(json.dumps(
        {"d": d, "lend_sh": 1, "lend_amt": 3281903982590, "slb_sh": 1, "slb_amt": 1473007249973.3, "slb_nopx": 0})
        for d in days) + "\n")
    (src / "mktcap.jsonl").write_text(json.dumps({"d": "2026-10-16", "cap": 1541834.31}) + "\n")
    assert build.main() == 0
    s = json.loads((out / "sbl.json").read_text())
    assert s["lend"] == [32819.04] * 3 and s["slb"] == [14730.07] * 3          # 億元
    assert s["cap"] == [None, None, 1541834.31]
    assert s["lend_r"][:2] == [None, None] and s["lend_r"][2] == 2.129
    import csv as _csv
    rows = list(_csv.DictReader(open(tmp_path / "csv" / "sbl.csv", encoding="utf-8")))
    assert rows[2]["lend_balance_to_market_cap_pct_weekly"] == "2.129" and rows[0]["listed_market_cap_yi_weekly"] == ""
    assert rows[0]["short_sale_balance_yi"] == "14730.07"
    cap = list(_csv.DictReader(open(tmp_path / "csv" / "mktcap.csv", encoding="utf-8")))
    assert cap == [{"date": "2026-10-16", "listed_market_cap_yi": "1541834.31"}]


# ---------------------------------------------------------------- 第二批：小台／微台、正逆價差、VIX、當沖、上櫃

MXF_CSV = (
    "日期,商品名稱,身份別,多方交易口數,多方交易契約金額(千元),空方交易口數,空方交易契約金額(千元),多空交易口數淨額,多空交易契約金額淨額(千元),多方未平倉口數,多方未平倉契約金額(千元),空方未平倉口數,空方未平倉契約金額(千元),多空未平倉口數淨額,多空未平倉契約金額淨額(千元)\n"
    "2026/10/16,小型臺指期貨,自營商,1,1,1,1,0,0,306,1,10658,1,-10352,1\n"
    "2026/10/16,小型臺指期貨,投信,0,0,0,0,0,0,87,1,107,1,-20,1\n"
    "2026/10/16,小型臺指期貨,外資及陸資,1,1,1,1,0,0,3676,1,4427,1,-751,1\n"
    "2026/10/16,臺股期貨,外資及陸資,1,1,1,1,0,0,9,1,9,1,0,1\n")


def test_parse_fut_inst_csv_selects_product_by_name():
    rows = fetch.parse_fut_inst_csv(MXF_CSV, "小型臺指期貨")
    assert rows == [{"d": "2026-10-16", "dl": [306, 10658], "t": [87, 107], "f": [3676, 4427]}]
    assert fetch.parse_fut_inst_csv(MXF_CSV) == []          # 預設只收臺股期貨，且三法人不齊就不收（只有外資一列）
    fm = [{"date": "2018-06-05", "futures_id": "MTX", "institutional_investors": "外資",
           "long_open_interest_balance_volume": 1250, "short_open_interest_balance_volume": 1846},
          {"date": "2018-06-05", "futures_id": "MTX", "institutional_investors": "投信",
           "long_open_interest_balance_volume": 46, "short_open_interest_balance_volume": 0},
          {"date": "2018-06-05", "futures_id": "MTX", "institutional_investors": "自營商",
           "long_open_interest_balance_volume": 20536, "short_open_interest_balance_volume": 8722},
          {"date": "2018-06-05", "futures_id": "TX", "institutional_investors": "外資",
           "long_open_interest_balance_volume": 9, "short_open_interest_balance_volume": 9}]
    assert fetch.finmind_fut_rows(fm, "MTX") == [{"d": "2018-06-05", "f": [1250, 1846], "t": [46, 0], "dl": [20536, 8722]}]


FUT_DAILY_CSV = (
    "交易日期,契約,到期月份(週別),開盤價,最高價,最低價,收盤價,漲跌價,漲跌%,成交量,結算價,未沖銷契約數,最後最佳買價,最後最佳賣價,歷史最高價,歷史最低價,是否因訊息面暫停交易,交易時段,價差對單式委託成交量\n"
    "2026/10/16,MTX,202610W4,1,1,1,47000,0,0%,5,47001,4,1,1,1,1,,一般,,\n"
    "2026/10/16,MTX,202610  ,1,1,1,47242,0,0%,5,47250,29164,1,1,1,1,,一般,,\n"
    "2026/10/16,MTX,202610  ,1,1,1,47100,0,0%,5,-,-,1,1,1,1,,盤後,,\n"
    "2026/10/16,MTX,202611  ,1,1,1,47300,0,0%,5,47310,10808,1,1,1,1,,一般,,\n"
    "2026/10/16,MTX,202612  ,1,1,1,-,0,0%,0,47400,2198,1,1,1,1,,一般,,\n"
    "2026/10/16,MTX,202703  ,1,1,1,47500,0,0%,5,47510,590,1,1,1,1,,一般,,\n"
    "2026/10/16,MTX,202610/202611,1,1,1,1,0,0%,5,-,-,1,1,1,1,,一般,,\n")


def test_parse_fut_daily_csv_sums_all_months_skips_spreads_and_after_hours():
    r = fetch.parse_fut_daily_csv(FUT_DAILY_CSV)
    assert len(r) == 1 and r[0]["d"] == "2026-10-16"
    assert r[0]["oi"] == 4 + 29164 + 10808 + 2198 + 590          # 含週契約，不含盤後列與跨月價差
    assert r[0]["oi_wk"] == 4
    assert r[0]["m"] == [["202610", 47242, 47250], ["202611", 47300, 47310], ["202612", None, 47400]]   # 只留近三個月份，沒成交收盤價＝None


def test_parse_vix_txt():
    text = ("日期\t時間\t臺指選擇權波動率指數\t收盤前1分鐘平均\n--------\t-------------------\t--------------------\t-------------------\n"
            "20261015\t13450000\t\t30.61\t\t30.61\n20261016\t13450000\t\t26.37\t\t26.33\n")
    assert fetch.parse_vix_txt(text) == [{"d": "2026-10-15", "v": 30.61, "v1": 30.61}, {"d": "2026-10-16", "v": 26.37, "v1": 26.33}]
    assert fetch.parse_vix_txt("<HTML><title>404</title>") == []


DTRADE_PAYLOAD = {"stat": "OK", "date": "20261016", "tables": [
    {"title": "115年10月16日 當日沖銷交易統計資訊",
     "fields": ["當日沖銷交易總成交股數", "當日沖銷交易總成交股數占市場比重%", "當日沖銷交易總買進成交金額",
                "當日沖銷交易總買進成交金額占市場比重%", "當日沖銷交易總賣出成交金額", "當日沖銷交易總賣出成交金額占市場比重%"],
     "data": [["2,392,658,000", "20.24", "377,952,391,370", "38.03", "378,930,466,350", "38.12"]]},
    {"title": "標的", "fields": ["證券代號"], "data": [["2330"]]}]}


def test_parse_dtrade_and_its_ratio_matches_turnover():
    row = fetch.parse_dtrade(DTRADE_PAYLOAD, "2026-10-16")
    assert row == {"d": "2026-10-16", "sh": 2392658000, "sh_p": 20.24, "buy": 377952391370, "buy_p": 38.03,
                   "sell": 378930466350, "sell_p": 38.12}
    assert fetch.parse_dtrade(DTRADE_PAYLOAD, "2026-10-15") is None           # 日期不符（休市被導到別天）
    assert fetch.parse_dtrade({"stat": "很抱歉，沒有符合條件的資料!"}, "2026-10-16") is None
    # 官方比重＝當沖買進金額 ÷ FMTQIK 全市場成交金額（993,814,830,090）：整數空間重算到小數 2 位
    assert round(row["buy"] * 10000 / 993814830090) == 3803
    assert round(row["sh"] * 10000 / 11820630612) == 2024


TPEX_INST_NEW = {"stat": "ok", "date": "20261016", "tables": [{"date": "115/10/16", "data": [
    ["外資及陸資合計", "73,677,462,203", "76,961,795,204", "-3,284,333,001"],
    ["　外資及陸資(不含自營商)", "73,677,462,203", "76,961,795,204", "-3,284,333,001"],
    ["　外資自營商", "0", "0", "0"],
    ["投信", "6,056,353,497", "4,682,247,965", "1,374,105,532"],
    ["自營商合計", "5,836,459,951", "9,116,991,593", "-3,280,531,642"],
    ["　自營商(自行買賣)", "1,511,400,251", "4,619,670,128", "-3,108,269,877"],
    ["三大法人合計*", "85,570,275,651", "90,761,034,762", "-5,190,759,111"]]}]}
TPEX_INST_2017 = {"stat": "ok", "date": "20170510", "tables": [{"date": "106/05/10", "data": [
    ["投信", "189,257,359", "517,516,125", "-328,258,766"], ["自營商", "1,199,468,180", "727,009,746", "472,458,434"],
    ["自營商(自行買賣)", "373,788,410", "195,076,050", "178,712,360"], []]}]}


def test_parse_tpex_inst_new_and_2017_formats_and_empty():
    r = fetch.parse_tpex_inst(TPEX_INST_NEW, "2026-10-16")
    assert r == {"d": "2026-10-16", "t": [6056353497, 4682247965], "dl": [5836459951, 9116991593],
                 "f": [73677462203, 76961795204]}
    # 三大法人合計＝外資(不含自營商)＋投信＋自營商合計（官方註明外資自營商已含在自營商內）
    assert sum(r[k][0] for k in ("f", "t", "dl")) == 85570275651
    assert sum(r[k][1] for k in ("f", "t", "dl")) == 90761034762
    old = fetch.parse_tpex_inst(TPEX_INST_2017, "2017-05-10")
    assert old == {"d": "2017-05-10", "t": [189257359, 517516125], "dl": [1199468180, 727009746]}   # 沒有外資列就不寫 f
    assert fetch.parse_tpex_inst({"stat": "ok", "date": "20161007", "tables": [{"data": []}]}, "2016-10-07") is None
    assert fetch.parse_tpex_inst(TPEX_INST_NEW, "2026-10-15") is None


TPEX_MARGIN = {"stat": "ok", "date": "20261016", "tables": [{
    "fields": ["代號", "名稱", "前資餘額(張)", "資買", "資賣", "現償", "資餘額", "資屬證金", "資使用率(%)", "資限額",
               "前券餘額(張)", "券賣", "券買", "券償", "券餘額", "券屬證金", "券使用率(%)", "券限額", "資券相抵(張)", "備註"],
    "data": [["6488", "環球晶", "1", "0", "0", "0", "1", "0", "1", "1", "0", "0", "0", "0", "0", "0", "0", "1", "0", ""]],
    "summary": [["", "合計(張)", "2,368,231", "67,193", "68,817", "1,975", "2,364,632", "", "", "", "33,644", "7,579", "2,873", "104", "38,246", "", "", "", "", ""],
                ["", "融資金(仟元)", "218,961,719", "8,090,791", "8,616,671", "185,720", "218,250,119", "", "", "", "", "", "", "", "", "", "", "", "", ""]]}]}


def test_parse_tpex_margin_takes_footer_totals_not_stock_sum():
    r = fetch.parse_tpex_margin(TPEX_MARGIN, "2026-10-16")
    assert r == {"d": "2026-10-16", "mg": 2364632, "mg_p": 2368231, "sh": 38246, "sh_p": 33644,
                 "mga": 218250119, "mga_p": 218961719}
    assert fetch.parse_tpex_margin(TPEX_MARGIN, "2026-10-15") is None
    bad = {"stat": "ok", "date": "20261016", "tables": [{"fields": ["代號"], "data": [], "summary": []}]}
    assert fetch.parse_tpex_margin(bad, "2026-10-16") is None


def test_chunks_by_calendar_month():
    import datetime as dt
    ch = list(fetch._chunks(dt.date(2017, 1, 31), dt.date(2017, 3, 5), 0))
    assert ch == [(dt.date(2017, 1, 31), dt.date(2017, 1, 31)), (dt.date(2017, 2, 1), dt.date(2017, 2, 28)),
                  (dt.date(2017, 3, 1), dt.date(2017, 3, 5))]
    assert list(fetch._chunks(dt.date(2017, 1, 1), dt.date(2017, 3, 1), 28))[0] == (dt.date(2017, 1, 1), dt.date(2017, 1, 28))


def test_state_save_merges_other_process_progress(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "DATA", tmp_path)
    a, b = fetch.State(), fetch.State()            # 兩個回補程序同時啟動
    a.bump_gap("dtrade", "2026-10-01")
    a.save()
    b.bump_gap("otc_inst", "2018-01-12")
    b.mark_month("taiex", "2016-10")
    b.save()
    c = fetch.State()
    assert c.gap_attempts("dtrade", "2026-10-01") == 1 and c.gap_attempts("otc_inst", "2018-01-12") == 1
    assert c.month_done("taiex", "2016-10")


def test_expiry_rule_third_wednesday_with_holiday_shift():
    import datetime as dt
    assert build.third_wednesday(2026, 10) == dt.date(2026, 10, 21)
    cal = {"2026-09-16", "2026-09-17"}
    assert build.expiry_date("202609", cal, "2026-10-16") == "2026-09-16"
    cal2 = {"2026-09-17", "2026-09-18"}              # 假設第三個星期三（9/16）休市 → 順延到下一個交易日
    assert build.expiry_date("202609", cal2, "2026-10-16") == "2026-09-17"
    assert build.expiry_date("202712", {"2026-10-16"}, "2026-10-16") == "2027-12-15"     # 日曆之後：不調整


def test_near_month_pick_rolls_on_expiry_day():
    cal = {"2026-09-15", "2026-09-16", "2026-09-17"}
    months = [["202609", 100, 100], ["202610", 110, 109], ["202611", 120, 119]]
    assert build.near_month_pick("2026-09-15", months, cal, "2026-09-17") == ("202609", 100)
    assert build.near_month_pick("2026-09-16", months, cal, "2026-09-17") == ("202610", 110)    # 到期日當天改看次月
    assert build.near_month_pick("2026-09-17", months[1:], cal, "2026-09-17") == ("202610", 110)


def test_basis_series_points_and_percent():
    taiex = {"2026-09-15": {"c": 20000.0}, "2026-09-16": {"c": 20100.0}, "2026-09-17": {"c": 20050.0}}
    tx = {"2026-09-15": {"m": [["202609", 20100, 0], ["202610", 20200, 0]]},
          "2026-09-16": {"m": [["202609", 20100, 0], ["202610", 20250, 0]]},
          "2026-09-17": {"m": [["202610", None, 0]]}}
    b = build.basis_series(sorted(taiex), tx, taiex)
    assert b["contract"] == ["202609", "202610", "202610"]
    assert b["pts"] == [100.0, 150.0, None] and b["pct"] == [0.5, 0.746, None]


def test_retail_ratio_integer_space():
    inst = {"d1": {"f": [3676, 4427], "t": [87, 107], "dl": [306, 10658]}}
    mk = {"d1": {"oi": 43256}, "d2": {"oi": 100}}
    r = build.retail_ratio(["d1", "d2"], inst, mk)
    assert r["net"] == [-11123, None] and r["oi"] == [43256, 100]
    assert r["ratio"] == [25.71, None]


def test_build_and_csv_with_batch2_series(tmp_path, monkeypatch):
    import csv as _csv
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    monkeypatch.setattr(build, "SRC", src)
    monkeypatch.setattr(build, "OUT", out)
    monkeypatch.setattr(build, "CSV_OUT", tmp_path / "csv")
    monkeypatch.setattr(build, "DISPLAY_START", "2026-10-14")
    days = ["2026-10-14", "2026-10-15", "2026-10-16"]

    def w(name, rows):
        (src / f"{name}.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    w("taiex", [{"d": d, "o": 1, "h": 2, "l": 0.5, "c": 47000.0 + i * 100} for i, d in enumerate(days)])
    w("mtx_inst", [{"d": "2026-10-16", "dl": [306, 10658], "t": [87, 107], "f": [3676, 4427]}])
    w("mtx_mkt", [{"d": d, "oi": 43256, "oi_wk": 0} for d in days])
    w("tx_daily", [{"d": d, "m": [["202610", 47100.0 + i * 100 + 130, 0], ["202611", 47500.0, 0]]} for i, d in enumerate(days)])
    w("vix", [{"d": "2026-10-16", "v": 26.37, "v1": 26.33}])
    w("dtrade", [{"d": "2026-10-16", "sh": 2392658000, "sh_p": 20.24, "buy": 377952391370, "buy_p": 38.03,
                  "sell": 378930466350, "sell_p": 38.12}])
    w("otc_inst", [{"d": "2026-10-16", "t": [6056353497, 4682247965], "dl": [5836459951, 9116991593]}])      # 沒有外資列
    w("otc_margin", [{"d": d, "mg": 2364632, "mg_p": 2368231, "sh": 38246, "sh_p": 33644, "mga": 218250119, "mga_p": 218961719}
                     for d in days])
    assert build.main() == 0
    m = json.loads((out / "mtx.json").read_text())
    assert m["ratio"] == [None, None, 25.71] and m["net"] == [None, None, -11123] and m["f"][2] == -751
    b = json.loads((out / "basis.json").read_text())
    assert b["pts"] == [230.0, 230.0, 230.0] and b["vix"] == [None, None, 26.37]
    assert json.loads((out / "dtrade.json").read_text())["r_amt"] == [None, None, 38.03]
    o = json.loads((out / "otc.json").read_text())
    assert o["f"][2] is None and o["t"][2] == 13.74 and o["dl"][2] == -32.81       # 億元
    assert o["mga"][0] == 2189.62                                                 # 隔日前日餘額定稿
    rows = list(_csv.DictReader(open(tmp_path / "csv" / "mtx_inst.csv", encoding="utf-8")))
    assert rows[0]["foreign_long_oi"] == "3676" and rows[0]["market_oi_all_contracts"] == "43256"
    assert rows[0]["retail_long_short_ratio_pct"] == "25.71"
    tx = list(_csv.DictReader(open(tmp_path / "csv" / "tx_daily.csv", encoding="utf-8")))
    assert tx[2]["near_month_contract"] == "202610" and tx[2]["basis_points"] == "230.0"
    ot = list(_csv.DictReader(open(tmp_path / "csv" / "otc_inst.csv", encoding="utf-8")))
    assert ot[0]["foreign_net_yi"] == "" and ot[0]["trust_net_yi"] == "13.74"


# ---------------------------------------------------------------- 預測檢定區塊（靜態 forecast.json）

def by_f(f):
    return [x for x in f["indicators"] if x["id"] == "F"][0]


def test_forecast_json_static_result():
    """docs/tw-chips/data/forecast.json 是 v7 檢定結果的靜態轉存：五個指標都不通過，頁面照『不通過』版呈現。"""
    f = json.loads((Path(__file__).resolve().parents[2] / "docs" / "tw-chips" / "data" / "forecast.json").read_text(encoding="utf-8"))
    assert f["page_layer_pass"] is False and f["scoreboard"] is None
    assert [x["id"] for x in f["indicators"]] == ["A", "B", "C", "D", "E", "F"]
    assert by_f(f)["single_test"] is True and round(by_f(f)["p_placebo"], 4) == 0.1584
    assert not any(x["pass"] for x in f["indicators"])
    by = {x["id"]: x for x in f["indicators"]}
    assert by["A"]["insufficient"] is True and by["A"]["n_high"] == 18
    assert round(by["B"]["S_test"] * 100, 1) == 13.1 and round(by["B"]["p_placebo"], 4) == 0.0665
    assert by["B"]["n_low_w52on"] == 21
    assert all(by[k]["S_test"] < 0 for k in "CDE")
    assert f["test_start"] == "2022-01-01" and round(f["n_indep_est"]) == 18
