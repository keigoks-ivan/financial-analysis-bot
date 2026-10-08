"""中國第二次擴充的 fetcher 離線測試：cn_nbs_hp70（70 城房價）、cn_safe（外管局）、cn_mof（財政部），以及 cn_pbc nth、cn_nbs offset。"""
from __future__ import annotations

from pathlib import Path

import pytest

from macro_db.sources import cn_common, cn_mof, cn_nbs, cn_nbs_hp70 as hp, cn_pbc, cn_safe

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "cn"


def tload(name):
    return (FIX / name).read_text(encoding="utf-8")


class Resp:
    def __init__(self, content):
        self.content = content if isinstance(content, bytes) else content.encode("utf-8")


class FakeNet:
    """依網址回固定內容；值是例外就丟出。calls 記錄請求過的網址。"""
    def __init__(self, routes):
        self.routes = routes
        self.calls = []

    def __call__(self, s, method, url, **kw):
        self.calls.append(url)
        for key, v in self.routes.items():
            if key in url:
                if isinstance(v, Exception):
                    raise v
                return Resp(v)
        raise AssertionError("沒預期的網址：" + url)


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(cn_common, "session", lambda *a, **k: object())
    monkeypatch.setattr(cn_common.time, "sleep", lambda *_: None)


# ---------- cn_pbc nth ----------
def test_pbc_horiz_nth_picks_second_matching_row():
    hdr = [None] + ["2026.%02d" % m for m in range(1, 13)]
    rows = [hdr,
            ["住户贷款"] + [None] * 12,
            ["短期贷款"] + list(range(1, 13)),
            ["企(事)业单位贷款"] + [None] * 12,
            ["短期贷款"] + list(range(101, 113))]
    assert cn_pbc.parse_horiz(rows, "^短期贷款")[0] == ("2026-01-01", 1.0)
    assert cn_pbc.parse_horiz(rows, "^短期贷款", 2)[0] == ("2026-01-01", 101.0)
    with pytest.raises(ValueError):
        cn_pbc.parse_horiz(rows, "^短期贷款", 3)


def test_pbc_vert_nth_picks_nth_same_named_column():
    rows = [["月份", "发行", "余额", "发行", "余额", "发行", "余额"],
            ["2026.01", 1, 10, 2, 20, 3, 30],
            ["2026.02", 4, 11, 5, 21, 6, 31]]
    assert cn_pbc.parse_vert(rows, "余额") == [("2026-01-01", 10.0), ("2026-02-01", 11.0)]
    assert cn_pbc.parse_vert(rows, "余额", 3) == [("2026-01-01", 30.0), ("2026-02-01", 31.0)]
    with pytest.raises(ValueError):
        cn_pbc.parse_vert(rows, "余额", 4)


# ---------- cn_nbs offset ----------
def test_nbs_offset_turns_mom_index_into_pct(monkeypatch):
    from test_cn_sources import FakeNBS
    fake = FakeNBS()
    monkeypatch.setattr(cn_nbs.C, "http_json", fake.http_json)
    cid = "5c7452825c7c4dcba391db5ca7f335c5"
    sp = [{"sid": "t.cpi", "params": {"cid": cid, "name": "居民消费价格指数 (上年同月=100)", "offset": -100}}]
    obs = cn_nbs.fetch(sp)["t.cpi"]["obs"]
    assert dict(obs)["2026-01-01"] == pytest.approx(0.2)                  # 100.2 -> 0.2


# ---------- cn_nbs_hp70 ----------
def test_hp70_list_dedupes_and_ignores_other_titles():
    got = hp.parse_list(tload("hp70_list.html"))
    assert got == {"2026-08": "https://www.stats.gov.cn/sj/zxfb/202609/t20260915_1965304.html"}   # 3 個重複連結＋能源稿只留 1 筆


def test_hp70_page_parses_both_tables_with_all_cities():
    p = hp.parse_page(tload("hp70_page.html"))
    assert len([k for k in p if k[0] == "new"]) == 70 and len([k for k in p if k[0] == "used"]) == 70
    assert p[("new", "北京")] == (99.8, 97.7)          # 國統局 2026 年 8 月新聞稿表 1
    assert p[("new", "上海")] == (100.4, 103.0)
    assert p[("new", "广州")] == (100.1, 98.1)
    assert p[("new", "深圳")] == (100.2, 97.7)
    assert p[("used", "深圳")] == (100.1, 97.3)


def test_hp70_page_restructure_raises():
    with pytest.raises(hp.Restructured):
        hp.parse_page("<html><table><tr><td>x</td></tr></table></html>")
    bad = tload("hp70_page.html").replace("环比", "月比")
    with pytest.raises(hp.Restructured, match="表頭"):
        hp.parse_page(bad)
    few = "<table><tr><th>城市</th><th>环比</th><th>同比</th></tr><tr><td>北京</td><td>100</td><td>100</td></tr></table>" * 2
    with pytest.raises(hp.Restructured, match="城市"):
        hp.parse_page(few)


def test_hp70_values_city_offset_and_breadth():
    page = hp.parse_page(tload("hp70_page.html"))
    pages = {"2026-08": page}
    assert hp.values_for({"kind": "new", "city": "北京", "metric": "yoy"}, pages) == [("2026-08-01", 97.7)]
    got = hp.values_for({"kind": "new", "city": "北京", "metric": "mom", "offset": -100}, pages)
    assert got[0][0] == "2026-08-01" and got[0][1] == pytest.approx(-0.2)
    up = hp.values_for({"kind": "new", "metric": "mom", "stat": "up"}, pages)[0][1]
    down = hp.values_for({"kind": "new", "metric": "mom", "stat": "down"}, pages)[0][1]
    mom = [v[0] for (k, _), v in page.items() if k == "new"]
    assert up == sum(1 for v in mom if v > 100) and down == sum(1 for v in mom if v < 100) and up + down <= 70
    assert hp.values_for({"kind": "new", "city": "不存在", "metric": "yoy"}, pages) == []


SPECS = [
    {"sid": "t.bj_yoy", "params": {"kind": "new", "city": "北京", "metric": "yoy"}},
    {"sid": "t.up", "params": {"kind": "new", "metric": "mom", "stat": "up"}},
]


def hp_net(listing=None, page=None, **extra):
    routes = {"index.html": listing if listing is not None else tload("hp70_list.html"),
              "t20260915_1965304": page if page is not None else tload("hp70_page.html")}
    routes.update(extra)
    return FakeNet(routes)


def test_hp70_fetch_incremental_fetches_page_then_skips_when_stored(monkeypatch):
    net = hp_net()
    monkeypatch.setattr(cn_common, "http_backoff", net)
    monkeypatch.setattr(hp.store, "read", lambda sid, *a: [])
    res = hp.fetch(SPECS)
    assert res["t.bj_yoy"]["obs"] == [("2026-08-01", 97.7)] and res["t.up"]["obs"][0][0] == "2026-08-01"
    assert len(net.calls) == 2                                           # 列表第 1 頁＋最新一期內頁
    # store 已經有最新一期：只看列表，不抓內頁，回傳 store 現有資料（不是空的）
    net2 = hp_net()
    monkeypatch.setattr(cn_common, "http_backoff", net2)
    monkeypatch.setattr(hp.store, "read", lambda sid, *a: [("2026-08-01", 97.7), ("2026-07-01", 98.0)])
    res = hp.fetch(SPECS)
    assert len(net2.calls) == 1 and res["t.bj_yoy"]["obs"] == [("2026-07-01", 98.0), ("2026-08-01", 97.7)]


def test_hp70_fetch_listing_unparsable_is_error_not_empty(monkeypatch):
    monkeypatch.setattr(cn_common, "http_backoff", hp_net(listing="<html>改版了</html>"))
    monkeypatch.setattr(hp.store, "read", lambda sid, *a: [])
    res = hp.fetch(SPECS)
    assert set(res) == {"t.bj_yoy", "t.up"} and all("error" in v and "改版" in v["error"] for v in res.values())


def test_hp70_fetch_newest_page_failure_is_error_and_restructure_is_error(monkeypatch):
    monkeypatch.setattr(hp.store, "read", lambda sid, *a: [])
    monkeypatch.setattr(cn_common, "http_backoff", hp_net(page=RuntimeError("HTTP 502")))
    res = hp.fetch(SPECS)
    assert all("error" in v and "最新一期" in v["error"] for v in res.values())
    monkeypatch.setattr(cn_common, "http_backoff", hp_net(page="<html>沒有表格</html>"))
    res = hp.fetch(SPECS)
    assert all("error" in v and "兩張價格表" in v["error"] for v in res.values())


def test_hp70_backfill_walks_list_pages_and_uses_cache(monkeypatch, tmp_path):
    monkeypatch.setenv("MACRO_DB_BACKFILL", "1")
    monkeypatch.setenv("MACRO_DB_HP70_CACHE", str(tmp_path))
    monkeypatch.setattr(hp.store, "read", lambda sid, *a: [])
    older = tload("hp70_list.html").replace("1965304", "1965050").replace("2026年8月", "2026年7月").replace("202609", "202608")
    net = FakeNet({"index.html": tload("hp70_list.html"), "index_1.html": older,
                   "index_2.html": RuntimeError("HTTP 404"),
                   "t20260915_1965304": tload("hp70_page.html"), "t20260815_1965050": tload("hp70_page.html")})
    monkeypatch.setattr(cn_common, "http_backoff", net)
    res = hp.fetch(SPECS)
    assert [d for d, _ in res["t.bj_yoy"]["obs"]] == ["2026-07-01", "2026-08-01"]
    assert (tmp_path / "hp70_2026-08.json").exists()
    n_before = len(net.calls)
    net.routes["t20260915_1965304"] = RuntimeError("HTTP 502")      # 有快取就不再抓內頁
    net.routes["t20260815_1965050"] = RuntimeError("HTTP 502")
    hp.fetch(SPECS)
    assert [c for c in net.calls[n_before:] if "t2026" in c] == []


# ---------- cn_safe ----------
def test_safe_picks_time_series_link_not_regional_files():
    links = cn_safe.parse_links(tload("safe_landing_jsh.html"))
    assert len(links) == 3
    url = cn_safe.pick_link(links, "jsh")
    assert url == "https://www.safe.gov.cn/safe/file/file/20260915/5c2551f57e2b4e0d94752901ff1abbd5.xlsx"
    assert cn_safe.pick_link(links, "bop") is None


def rows_of(name, sheet):
    return cn_safe.read_sheet((FIX / name).read_bytes(), name, sheet)


def test_safe_bop_quarterly_takes_first_matching_row():
    rows = rows_of("safe_bop.xlsx", "季度BOP（美元）")
    ca = cn_safe.parse_quarterly(rows, r"^1\.经常账户")
    assert ca[0] == ("2025-01-01", 100.5) and ca[5] == ("2026-04-01", 150.5) and len(ca) == 8
    assert cn_safe.parse_quarterly(rows, r"^贷方")[0][1] == 500.0
    with pytest.raises(cn_safe.LayoutError):
        cn_safe.parse_quarterly(rows, "不存在")


def test_safe_monthly_serial_header_ignores_corrupted_first_cells():
    rows = rows_of("safe_jsh.xlsx", "以美元计价（月度）")
    cols = cn_safe.month_columns(rows[3], 2)
    assert cols[0][1] == "2024-01-01" and cols[-1][1] == "2026-06-01" and len(cols) == 30   # 前三格序號壞掉，仍依月序補位
    settle = cn_safe.parse_monthly_section(rows, 3, 2, "结汇", r"^一、结汇")
    assert settle[0] == ("2024-01-01", 2000.0) and settle[-1] == ("2026-06-01", 2029.0)
    net = cn_safe.parse_monthly_section(rows, 3, 2, "差额", r"^三、差额")
    assert net[0][1] == 200.0
    client = cn_safe.parse_monthly_section(rows, 3, 2, "差额", r"\(二）银行代客")       # 同名列只取指定區段內的
    assert client[0][1] == 160.0 and cn_safe.parse_monthly_section(rows, 3, 2, "结汇", r"\(二）银行代客")[0][1] == 1900.0


def test_safe_monthly_header_mismatch_is_layout_error():
    rows = rows_of("safe_jsh.xlsx", "以美元计价（月度）")
    rows[3][-1] = rows[3][-1] + 100       # 最後一欄的序號月份和前面不連續
    with pytest.raises(cn_safe.LayoutError, match="不連續"):
        cn_safe.month_columns(rows[3], 2)


def test_safe_trade_months_from_position_and_checks_last_label():
    rows = rows_of("safe_trade.xlsx", "按美元计值")
    gs = cn_safe.parse_trade(rows, r"^货物和服务贸易差额")
    assert gs[0] == ("2015-01-01", 400.0) and gs[-1] == ("2017-02-01", 425.0)
    assert cn_safe.parse_trade(rows, r"^1\.货物贸易差额")[0][1] == 600.0
    rows[3][-1] = "2017.05"
    with pytest.raises(cn_safe.LayoutError, match="版面可能改版"):
        cn_safe.parse_trade(rows, r"^货物")


def test_safe_debt_uses_unindented_sector_rows_and_quarter_start_month():
    rows = rows_of("safe_debt.xlsx", "Sheet1")
    gov = cn_safe.parse_debt(rows, "广义政府")
    assert gov[0] == ("2014-10-01", 1133.5)            # 2014 年 12 月末 -> 第 4 季（10 月 1 日）
    assert gov[1][0] == "2015-01-01"                   # 3 月末 -> 第 1 季
    assert cn_safe.parse_debt(rows, "外债总额头寸")[0][1] == 20000.0
    with pytest.raises(cn_safe.LayoutError):
        cn_safe.parse_debt(rows, "短期")               # 縮排的子列不算部門


def safe_specs():
    return [
        {"sid": "t.ca", "params": {"file": "bop", "landing_page": "https://www.safe.gov.cn/safe/2019/0627/13519.html",
                                   "sheet": "季度BOP（美元）", "lab_rx": r"^1\.经常账户"}},
        {"sid": "t.bad_row", "params": {"file": "bop", "landing_page": "https://www.safe.gov.cn/safe/2019/0627/13519.html",
                                        "sheet": "季度BOP（美元）", "lab_rx": "不存在的列"}},
        {"sid": "t.bad_sheet", "params": {"file": "bop", "landing_page": "https://www.safe.gov.cn/safe/2019/0627/13519.html",
                                          "sheet": "沒有這張", "lab_rx": r"^1\."}},
        {"sid": "t.settle", "params": {"file": "jsh", "landing_page": "https://www.safe.gov.cn/safe/2023/0215/22329.html",
                                       "sheet": "以美元计价（月度）", "hdr_row": 3, "col0": 2, "sec_rx": "结汇", "lab_rx": "^一、结汇"}},
    ]


def landing(title, name):
    return '<a href="/safe/file/file/20260929/%s.xlsx" title="%s.xlsx">%s</a>' % (name, title, title)


def test_safe_fetch_resolves_link_per_file_and_isolates_row_errors(monkeypatch):
    net = FakeNet({"13519.html": landing("中国国际收支平衡表时间序列(BPM6)", "aaa"),
                   "22329.html": tload("safe_landing_jsh.html"),
                   "aaa.xlsx": (FIX / "safe_bop.xlsx").read_bytes(),
                   "5c2551f57e2b4e0d94752901ff1abbd5.xlsx": (FIX / "safe_jsh.xlsx").read_bytes()})
    monkeypatch.setattr(cn_common, "http_backoff", net)
    res = cn_safe.fetch(safe_specs())
    assert res["t.ca"]["obs"][0] == ("2025-01-01", 100.5) and res["t.ca"]["obs"][-1] == ("2024-10-01", 95.5)
    assert "找不到列" in res["t.bad_row"]["error"] and "沒有這張" in res["t.bad_sheet"]["error"]
    assert res["t.settle"]["obs"][0] == ("2024-01-01", 2000.0)
    assert sum(1 for c in net.calls if c.endswith(".xlsx")) == 2        # 同一個檔只下載一次


def test_safe_landing_page_redesign_is_error_for_whole_file_not_empty(monkeypatch):
    net = FakeNet({"13519.html": "<html>外管局改版：附件改成動態載入</html>", "22329.html": tload("safe_landing_jsh.html"),
                   "5c2551f57e2b4e0d94752901ff1abbd5.xlsx": (FIX / "safe_jsh.xlsx").read_bytes()})
    monkeypatch.setattr(cn_common, "http_backoff", net)
    res = cn_safe.fetch(safe_specs())
    for sid in ("t.ca", "t.bad_row", "t.bad_sheet"):
        assert "error" in res[sid] and "附件連結" in res[sid]["error"] and "改版" in res[sid]["error"]
    assert "obs" in res["t.settle"]                                     # 別的檔不受影響


def test_safe_download_failure_is_error(monkeypatch):
    net = FakeNet({"13519.html": landing("中国国际收支平衡表时间序列(BPM6)", "aaa"), "aaa.xlsx": RuntimeError("HTTP 503"),
                   "22329.html": RuntimeError("HTTP 502")})
    monkeypatch.setattr(cn_common, "http_backoff", net)
    res = cn_safe.fetch(safe_specs())
    assert len(res) == 4 and all("error" in v for v in res.values())


# ---------- cn_mof ----------
def test_mof_period_of_all_title_forms():
    f = cn_mof.period_of
    assert f("2026年1-8月财政收支情况") == (2026, 8) and f("2024年8月财政收支情况") == (2024, 8)
    assert f("2026年1-2月财政收支情况") == (2026, 2) and f("2026年一季度财政收支情况") == (2026, 3)
    assert f("2026年上半年财政收支情况") == (2026, 6) and f("2025年前三季度财政收支情况") == (2025, 9)
    assert f("2025年财政收支情况") == (2025, 12) and f("2025年全国政府采购简要情况") is None


def test_mof_list_and_article_fixture():
    lst = cn_mof.parse_list(tload("mof_list.html"))
    assert sorted(lst) == ["2026-06", "2026-07", "2026-08"] and cn_mof.page_count(tload("mof_list.html")) >= 1
    got = cn_mof.parse_article(cn_mof.page_text(tload("mof_article.html")))
    assert got["rev"] == (156633.0, 5.7) and got["land"] == (13753.0, -28.6)       # 財政部 2026 年 1-8 月財政收支情況
    assert got["deed"] == (2585.0, -14.2) and got["fund_rev"][1] == -19.0 and len(got) == 13


def test_mof_negative_wording_and_missing_sentence():
    t = "全国一般公共预算收入100亿元，同比下降3.5%。税收收入80亿元，比上年同期减少1.2%。"
    got = cn_mof.parse_article(t)
    assert got == {"rev": (100.0, -3.5), "tax": (80.0, -1.2)}
    assert cn_mof.parse_article("2025年，全国一般公共预算收入216045亿元，比上年下降1.7%。") == {"rev": (216045.0, -1.7)}   # 全年稿的句型
    assert cn_mof.parse_article("扣除留抵退税因素后增长，按自然口径计算下降") == {}


MSPECS = [
    {"sid": "t.rev", "params": {"metric": "rev", "field": "yoy_pct", "since_year": 2020}},
    {"sid": "t.land_amt", "params": {"metric": "land", "field": "ytd_amount", "since_year": 2020}},
]


def mof_net(**over):
    routes = {"index.htm": tload("mof_list.html"), "t20260918_3997709": tload("mof_article.html"),
              "t20260814_3995497": tload("mof_article.html"), "t20260722_3993943": tload("mof_article.html")}
    routes.update(over)
    return FakeNet(routes)


def test_mof_fetch_only_new_periods_and_returns_stored_when_nothing_new(monkeypatch):
    net = mof_net()
    monkeypatch.setattr(cn_common, "http_backoff", net)
    monkeypatch.setattr(cn_mof.store, "read", lambda sid, *a: [])
    res = cn_mof.fetch(MSPECS)
    assert [d for d, _ in res["t.rev"]["obs"]] == ["2026-06-01", "2026-07-01", "2026-08-01"]
    assert res["t.land_amt"]["obs"][-1] == ("2026-08-01", 13753.0)
    monkeypatch.setattr(cn_common, "http_backoff", mof_net())
    net2 = cn_common.http_backoff
    monkeypatch.setattr(cn_mof.store, "read", lambda sid, *a: [("2026-06-01", 1.0), ("2026-07-01", 2.0), ("2026-08-01", 3.0)])
    res = cn_mof.fetch(MSPECS)
    assert res["t.rev"]["obs"] == [("2026-06-01", 1.0), ("2026-07-01", 2.0), ("2026-08-01", 3.0)]
    assert len(net2.calls) == 1                                          # 只看列表頁


def test_mof_fetch_stops_after_two_consecutive_failures_and_caps(monkeypatch):
    net = mof_net(**{"t20260918_3997709": RuntimeError("HTTP 502"), "t20260814_3995497": RuntimeError("HTTP 502")})
    monkeypatch.setattr(cn_common, "http_backoff", net)
    monkeypatch.setattr(cn_mof.store, "read", lambda sid, *a: [])
    res = cn_mof.fetch(MSPECS)
    assert all("error" in v and "全部失敗" in v["error"] for v in res.values())   # 連續兩篇失敗就停，不再往下試
    assert not any("t20260722" in c for c in net.calls)
    assert len([c for c in net.calls if "/tongjishuju/2026" in c]) <= cn_mof.MAX_PER_RUN


def test_mof_fetch_all_articles_failing_is_error(monkeypatch):
    net = mof_net(**{"t20260918_3997709": RuntimeError("HTTP 502"), "t20260814_3995497": RuntimeError("HTTP 502"),
                     "t20260722_3993943": RuntimeError("HTTP 502")})
    monkeypatch.setattr(cn_common, "http_backoff", net)
    monkeypatch.setattr(cn_mof.store, "read", lambda sid, *a: [])
    res = cn_mof.fetch(MSPECS)
    assert all("error" in v and "全部失敗" in v["error"] for v in res.values())


def test_mof_list_failure_and_redesign_are_errors(monkeypatch):
    monkeypatch.setattr(cn_mof.store, "read", lambda sid, *a: [])
    monkeypatch.setattr(cn_common, "http_backoff", mof_net(**{"index.htm": RuntimeError("HTTP 502")}))
    assert all("列表頁失敗" in v["error"] for v in cn_mof.fetch(MSPECS).values())
    monkeypatch.setattr(cn_common, "http_backoff", mof_net(**{"index.htm": "<html>改版</html>"}))
    assert all("error" in v and "改版" in v["error"] for v in cn_mof.fetch(MSPECS).values())


def test_mof_newest_article_unparsable_is_error(monkeypatch):
    monkeypatch.setattr(cn_mof.store, "read", lambda sid, *a: [])
    monkeypatch.setattr(cn_common, "http_backoff", mof_net(**{"t20260918_3997709": "<html><p>句型全改了</p></html>"}))
    res = cn_mof.fetch(MSPECS)
    assert all("error" in v and "句型可能改版" in v["error"] for v in res.values())


def test_mof_2022_style_article_is_skipped_without_error(monkeypatch):
    """2022 年那批稿件句型不同：該月缺值，不影響其他月份。"""
    monkeypatch.setenv("MACRO_DB_BACKFILL", "1")
    monkeypatch.setattr(cn_mof.store, "read", lambda sid, *a: [])
    old = tload("mof_list.html") + '<li><a href="./202206/t20220616_3818568.htm"  title="2022年5月财政收支情况">x</a></li>'
    net = mof_net(**{"index.htm": old, "index_1.htm": "", "index_2.htm": "", "index_3.htm": "",
                     "t20220616_3818568": "<p>扣除留抵退税因素后增长，按自然口径计算下降</p>"})
    monkeypatch.setattr(cn_common, "http_backoff", net)
    res = cn_mof.fetch(MSPECS)
    assert "2022-05-01" not in dict(res["t.rev"]["obs"]) and "2026-08-01" in dict(res["t.rev"]["obs"])
