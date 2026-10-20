#!/usr/bin/env python3
"""測試 `scripts/dd2/primary_docs.py` 與 primary_common／primary_tw／primary_us（一手文件抓取，零 LLM）。

全程離線：fixture 放 scripts/tests/fixtures/primary_docs/（取自 2026-10-20 實測回應，已去掉個人聯絡欄位），
網路來源一律 monkeypatch。實網測試要設環境變數 DD_PRIMARY_LIVE=1 才會跑（TW 約 17 次、US 約 4 次請求）。

涵蓋：文字計量與預算、台股標題關鍵字與重大訊息 item、doc.twse 清單挑年報、主要客戶表定位與解析
（四檔版型）、公平會結果解析、ESG 反競爭、美股 10-K 分節與挑段、8-K 清單、collect 快取與失敗略過、
共用資料庫 CSV 累加、模板注入（無摘錄時 prompt 與舊版逐字相同）。

Python 3.9 相容。
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
import types
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))

import ddreport  # noqa: E402
import primary_common as pc  # noqa: E402
import primary_docs  # noqa: E402
import primary_tw as tw  # noqa: E402
import primary_us as us  # noqa: E402

FX = Path(__file__).resolve().parent / "fixtures" / "primary_docs"
TMPL = SCRIPTS_DIR / "dd2" / "prompts" / "coverage.md.tmpl"


def _json(name):
    return json.loads((FX / name).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 文字計量與預算
# ---------------------------------------------------------------------------

def test_weight_counts_cjk_chars_and_latin_words():
    assert pc.weight("聯電甲客戶占12%") == 7  # 6 個中文字＋1 個數字詞
    assert pc.weight("largest customer accounted for 12% of revenue") == 7


def test_clip_to_weight_snaps_to_sentence():
    text = "第一句。第二句。第三句。第四句。"
    out = pc.clip_to_weight(text, 8)
    assert out.endswith("…") and "第三句" not in out
    assert pc.clip_to_weight("短文", 100) == "短文"


def test_enforce_budget_truncates_last_item_and_drops_rest():
    items = [pc.mk_item("s", "d", "u", "2026-01-01", "x", "字" * 100) for _ in range(5)]
    out = pc.enforce_budget(items, 280)
    assert len(out) == 3
    assert pc.weight(out[2]["text"]) <= 81
    assert len(pc.enforce_budget(items, 250)) == 2  # 剩不到 60 單位就不收半段
    assert pc.enforce_budget(items[:1], 500) == items[:1]


def test_pick_paragraphs_filters_and_orders():
    rules = [(re.compile("antitrust", re.I), 3)]
    paras = [(1, "a", "x antitrust antitrust y. " * 5), (2, "b", "nothing here. " * 5), (3, "a", "antitrust once. " * 3)]
    got = pc.pick_paragraphs(paras, rules, 1000, min_score=3.0)
    assert [sec for sec, _ in got] == ["a", "a"]
    got = pc.pick_paragraphs(paras, rules, 1000, min_score=3.0, section_bonus={"b": 1.0})
    assert got == []
    # 平均每句詞數過長（清單串接）略過
    long_para = [(1, "a", ("antitrust word " * 200).strip())]
    assert pc.pick_paragraphs(long_para, rules, 5000, min_score=1.0, max_sentence_words=90) == []


# ---------------------------------------------------------------------------
# 台股：關鍵字與重大訊息
# ---------------------------------------------------------------------------

def test_tag_keywords_ignores_routine_consolidated_report():
    assert tw.tag_keywords("公告本公司董事會決議通過民國114年度合併財務報告") == []
    assert tw.tag_keywords("本公司針對115/10/13工安意外之說明") == ["工安"]
    assert tw.tag_keywords("公告擬處分聯能科技全部股權 (更正公告)") == ["處分", "更正"]
    assert tw.tag_keywords("與A公司合併案") == ["合併"]


def _rows_from_sample():
    res = _json("mops_t05st01_sample.json")["result"]["data"]
    rows = []
    for r in res:
        rows.append({"date": tw.roc_to_iso(r[2]), "time": r[3], "title": pc.one_line(r[4]), "params": r[5]["parameters"]})
    rows.sort(key=lambda x: x["date"], reverse=True)
    return rows


def test_build_mops_items_stats_hits_and_details():
    rows = _rows_from_sample()
    detail = _json("mops_detail_sample.json")["result"]["data"][0]
    details = {("2026-10-13", rows[0]["title"]): {"subject": detail[6].strip(), "clause": detail[7], "body": detail[9]}}
    items = tw.build_mops_items("3037", rows, details, dt.date(2026, 10, 20), [("2026-10-13", rows[0]["title"])])
    head = items[0]["text"]
    assert "共 6 則" in head and "含關鍵字" in head
    assert "2026-10-13［工安］" in head
    assert "合併財務報告" not in head.split("標題含關鍵字者")[1]  # 例行合併財報不算命中
    assert items[1]["as_of"] == "2026-10-13" and "勞檢處" in items[1]["text"]
    assert items[-1]["section"] == "重大訊息標題清單" and "合併財務報告" in items[-1]["text"]


def test_build_mops_items_no_hit_says_none():
    rows = [r for r in _rows_from_sample() if not tw.tag_keywords(r["title"])]
    items = tw.build_mops_items("3037", rows, {}, dt.date(2026, 10, 20))
    assert "沒有任何標題含上述關鍵字" in items[0]["text"] and "含關鍵字（併購" in items[0]["text"]
    assert "0 則，未含者 2 則" in items[0]["text"]


def test_fetch_mops_rows_window_and_errors(monkeypatch):
    sample = _json("mops_t05st01_sample.json")["result"]

    def fake_post(http, name, body):
        if body["year"] == "115":
            return sample
        raise pc.FetchError("MOPS code=500")
    monkeypatch.setattr(tw, "_mops_post", fake_post)
    rows, errs = tw.fetch_mops_rows(None, "3037", dt.date(2026, 10, 20))
    assert len(rows) == 6 and rows[0]["date"] == "2026-10-13"
    assert errs and "500" in errs[0]  # 去年那年失敗只記錯誤，不丟例外
    # 兩年都失敗才丟例外
    monkeypatch.setattr(tw, "_mops_post", lambda *a: (_ for _ in ()).throw(pc.FetchError("x")))
    with pytest.raises(pc.FetchError):
        tw.fetch_mops_rows(None, "3037", dt.date(2026, 10, 20))


# ---------------------------------------------------------------------------
# 台股：doc.twse 年報／主要客戶表
# ---------------------------------------------------------------------------

def test_parse_doc_listing_and_pick_annual_report():
    rows = tw.parse_doc_listing((FX / "doc_listing_sample.html").read_bytes())
    assert len(rows) == 6 and rows[1]["filename"] == "2025_3037_20260529F04.pdf" and rows[1]["upload"] == "2026-05-08"
    pick = tw.pick_annual_report(rows, dt.date(2026, 10, 20))
    assert pick["filename"] == "2025_3037_20260529F11.pdf"  # 中文、最新資料年度、優先股東會後修訂本
    early = tw.pick_annual_report(rows, dt.date(2026, 6, 1))  # 修訂本還沒上傳：用原本
    assert early["filename"] == "2025_3037_20260529F04.pdf"
    assert tw.pick_annual_report(rows, dt.date(2025, 1, 1)) is None


def test_find_table_anchor_skips_toc_page():
    lay = _json("customer_layouts.json")
    pages = [lay["toc_page"], "無關頁面", lay["ar_2383"]]
    hit = tw.find_table_anchor(pages, tw.AR_ANCHORS)
    assert hit and hit[0] == 3  # 目錄頁只有頁碼，不算
    assert tw.find_table_anchor([lay["toc_page"]], tw.AR_ANCHORS) is None


@pytest.mark.parametrize("key,roc,expect", [
    ("ar_2303_cropped", 114, [("甲", 28005843, 12.0, 2025), ("甲", 24180535, 10.0, 2024)]),
    ("ar_3037", 114, [("辛", 18475388, 16.0, 2024), ("辛", 37232882, 28.0, 2025)]),
    ("ar_2317", 114, [("戊客戶", 3706464, 54.03, 2024), ("戊客戶", 3574256, 44.11, 2025)]),
    ("fs_2303", 114, [("甲客戶", 28005843, None, 2025), ("甲客戶", 24180535, None, 2024)]),
    ("fs_2383", 114, [("甲", 13288019, 14.0, 2025), ("甲", 8987063, 13.0, 2024)]),
])
def test_parse_customer_rows_layouts(key, roc, expect):
    text = tw.trim_table(tw._tidy_layout(_json("customer_layouts.json")[key]))
    got = [(r["customer_label"], r["amount"], r["pct"], r["fiscal_year"]) for r in tw.parse_customer_rows(text, roc)]
    assert got == expect


def test_parse_customer_rows_unit_variants():
    for key, unit in (("ar_2317", "新台幣佰萬元"), ("ar_3037", "新台幣仟元"), ("ar_2303_cropped", "新臺幣千元")):
        text = tw.trim_table(tw._tidy_layout(_json("customer_layouts.json")[key]))
        assert {r["unit"] for r in tw.parse_customer_rows(text, 114)} == {unit}


def test_parse_customer_rows_three_year_columns_keeps_first_two():
    text = tw.trim_table(tw._tidy_layout(_json("customer_layouts.json")["ar_2383"]))
    rows = tw.parse_customer_rows(text, 114)
    labels = [(r["customer_label"], r["fiscal_year"]) for r in rows]
    assert ("甲", 2024) in labels and ("甲", 2025) in labels
    assert all(r["fiscal_year"] in (2024, 2025) for r in rows)  # 第三欄「截至第一季」不收
    assert not any("其他" in r["customer_label"] or "銷貨" in r["customer_label"] for r in rows)


def test_trim_table_drops_following_sections():
    text = tw._tidy_layout(_json("customer_layouts.json")["ar_3037"])
    out = tw.trim_table(text)
    assert "註 3：銷貨客戶係指終端客戶" in out
    assert "員工資料" not in out and "工程師" not in out


def test_extract_customer_table_prefers_crop_then_falls_back(monkeypatch):
    lay = _json("customer_layouts.json")
    pages = ["x", lay["ar_3037"]]
    monkeypatch.setattr(tw, "_pdftotext", lambda pdf, *a: "\f".join(pages))
    monkeypatch.setattr(tw, "_crop_below_anchor", lambda *a, **k: None)  # 裁切失敗
    got = tw.extract_customer_table("x.pdf", tw.AR_ANCHORS)
    assert got and got[0] == 2 and "辛" in got[1] and "非關係人" in got[1]
    monkeypatch.setattr(tw, "_crop_below_anchor", lambda *a, **k: lay["ar_2303_cropped"])
    got = tw.extract_customer_table("x.pdf", tw.AR_ANCHORS)
    assert "28,005,843" in got[1]  # 雙欄排版靠裁切取得右欄表格


# ---------------------------------------------------------------------------
# 台股：公平會、ESG
# ---------------------------------------------------------------------------

def test_parse_ftc_results_and_items():
    total, rows = tw.parse_ftc_results((FX / "ftc_result_sample.html").read_text(encoding="utf-8"))
    assert total == 12 and len(rows) == 2
    assert rows[0][0] == "2015/12/16" and rows[0][1] == "處分書及不處分決議書" and rows[0][4].startswith("https://www.ftc.gov.tw/uploadDecision/")
    items = tw.build_ftc_items("鴻海精密", total, rows, dt.date(2026, 10, 20))
    assert "共 12 筆" in items[0]["text"] and "命中只代表" in items[0]["text"]
    assert items[1]["section"].endswith("（僅文內提及）") and items[1]["as_of"] == "2015-12-16"
    empty = tw.build_ftc_items("環球晶圓", 0, [], dt.date(2026, 10, 20))
    assert len(empty) == 1 and "沒有任何命中" in empty[0]["text"]
    named = tw.build_ftc_items("SANYO", 1, [rows[0]], dt.date(2026, 10, 20))
    assert "案名含公司名" in named[1]["section"]


def test_parse_anti_loss():
    rows = _json("esg_anti_sample.json")
    yr, iso, amt = tw.parse_anti_loss(rows, "2303")
    assert (yr, iso, amt) == ("114", "2026-10-20", "0.000")
    assert tw.parse_anti_loss(rows, "9999") is None


def test_roc_to_iso_and_name_norm():
    assert tw.roc_to_iso("115/05/08 15:40:55") == "2026-05-08" and tw.roc_to_iso("1150114") == "2026-01-14"
    assert tw.roc_to_iso("abc") is None
    assert tw._norm_name("聯華電子股份有限公司") == "聯華電子"


# ---------------------------------------------------------------------------
# 美股
# ---------------------------------------------------------------------------

def _tenk_axes():
    text = pc.html_to_text((FX / "tenk_sample.html").read_text())
    lines, spans = us.split_sections(text, "10-K")
    return text, lines, spans, us.build_axis_items(lines, spans, "10-K", "10-K（FY2025）", "http://x", "2026-02-06")


def test_split_sections_picks_body_not_toc():
    _text, lines, spans, _ = _tenk_axes()
    for iid in ("1", "1A", "3", "7", "8"):
        assert iid in spans
    a, b = spans["1A"]
    assert "Entity List" in "\n".join(lines[a:b])  # 取正文（不是目錄那行）
    assert (spans["1A"][1] - spans["1A"][0]) > 2


def test_build_axis_items_routes_by_keywords():
    _text, _lines, _spans, out = _tenk_axes()
    cust = " ".join(i["text"] for i in out["customer_concentration_credit"])
    assert "end customers accounted for 12% of revenue" in cust
    assert "Free cash flow represented 16.6% of revenue" not in cust  # 沒提到 customer 的獲利段不收
    assert any("Item 8" in i["section"] for i in out["customer_concentration_credit"])
    anti = out["regulatory_antitrust"]
    assert anti[0]["section"].startswith("Item 3") and "ordinary course" in anti[0]["text"]  # Item 3 本文前置
    assert any("European Commission" in i["text"] for i in anti)
    assert "tariffs" in out["reg_tariff_export"][0]["text"]
    assert "in-house" in out["customer_second_source"][0]["text"]
    assert any("market share" in i["text"] for i in out["competitive_share_entrants"])
    assert "distributors" in out["channel_business_model_shift"][0]["text"]
    me = " ".join(i["text"] for i in out["major_events"])
    assert "ordinary course" in me and "class action" in me  # Item 3 ＋ 訴訟段落
    assert all(i["as_of"] == "2026-02-06" and i["url"] == "http://x" for items in out.values() for i in items)


def test_pick_annual_filing_and_8k_list():
    sub = _json("submissions_sample.json")
    row = us.pick_annual_filing(sub, "2026-10-20")
    assert row["form"] == "10-K" and row["filingDate"] == "2026-02-06"
    assert us.pick_annual_filing(sub, "2026-01-01") is None
    assert us.filing_url("0000097476", row).endswith("/97476/000009747626000059/txn-20251231.htm")
    rows = list(us._recent_rows(sub))
    sel = us.build_8k_list(rows, dt.date(2026, 10, 20), foreign=False)
    assert [r["filingDate"] for r in sel] == ["2026-09-17", "2026-07-22", "2026-03-25", "2026-01-27"]  # 含 8-K/A、不含 2025-09-01
    codes, label = us._fmt_items("5.02,1.01")
    assert codes == ["5.02", "1.01"] and "Material Definitive Agreement" in label


def test_src_us_8k_builds_list_and_fetches_notable_detail(monkeypatch):
    sub = _json("submissions_sample.json")

    class FakeHttp:
        def __init__(self):
            self.urls = []

        def get(self, url, **kw):
            self.urls.append(url)
            return types.SimpleNamespace(status_code=200, text="<p>Item 1.01 Entry into a Material Definitive Agreement</p><p>On March 20, 2026 the company entered into an agreement.</p><p>SIGNATURE</p>")

    ctx = types.SimpleNamespace(ticker="TXN", date=dt.date(2026, 10, 20), http_sec=FakeHttp(), global_cache=Path("."), _sub=("0000097476", sub))
    res = us.src_us_8k(ctx)
    items = res["axes"]["major_events"]
    assert "共 4 份 8-K" in items[0]["text"] and "含重大項目" in items[0]["text"]
    assert len(items) == 2 and items[1]["as_of"] == "2026-03-25" and "entered into an agreement" in items[1]["text"]
    assert len(ctx.http_sec.urls) == 1


# ---------------------------------------------------------------------------
# collect：快取、失敗略過、共用資料庫
# ---------------------------------------------------------------------------

def _fake_sources(calls, fail=()):
    def mk(name, axes, extra=None):
        def fn(ctx):
            calls.append(name)
            if name in fail:
                raise pc.FetchError("測試失敗")
            res = {"axes": axes, "note": ""}
            res.update(extra or {})
            return res
        return fn
    it = lambda t, sec="s": pc.mk_item("src", "doc", "https://x", "2026-05-01", sec, t)
    return [
        ("tw_company", mk("tw_company", {}, {"meta": {"full_name": "測試股份有限公司", "abbr": "測試", "market": "sii"}})),
        ("tw_mops", mk("tw_mops", {"major_events": [it("標題清單")]},
                       {"csv_news": [{"date": "2026-05-01", "ticker": "9999.TW", "title": "T", "keyword_tags": "", "url": "u"}]})),
        ("tw_customers", mk("tw_customers", {"customer_concentration_credit": [it("甲 12%")]},
                            {"csv_customers": [{"date": "2026-05-01", "ticker": "9999.TW", "fiscal_year": 2025, "customer_label": "甲",
                                                "amount": 1, "unit": "千元", "pct": 12.0, "source_url": "u"}]})),
        ("tw_ftc", mk("tw_ftc", {"regulatory_antitrust": [it("0 筆")]})),
    ]


def test_collect_caches_same_day_and_retries_failed_sources(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(primary_docs, "_sources", lambda market: _fake_sources(calls, fail=("tw_ftc",)))
    monkeypatch.setattr(primary_docs, "_make_ctx", lambda *a, **k: types.SimpleNamespace(meta=None))
    run = tmp_path / "run"
    shared = tmp_path / "shared"
    shared.parent.mkdir(exist_ok=True)
    axes = primary_docs.collect("9999.TW", "20261020", run, shared_dir=shared)
    assert sorted(axes) == ["customer_concentration_credit", "major_events"]  # 公平會失敗：略過、不擋
    man = primary_docs.load_manifest(run)
    st = {s["name"]: s for s in man["sources"]}
    assert st["tw_ftc"]["status"] == "failed" and "測試失敗" in st["tw_ftc"]["note"]
    assert st["tw_mops"]["status"] == "ok"
    assert json.loads((run / "primary_docs.json").read_text(encoding="utf-8")) == axes
    # 同日重跑：成功的來源讀快取、失敗的重抓
    calls.clear()
    monkeypatch.setattr(primary_docs, "_sources", lambda market: _fake_sources(calls, fail=()))
    axes2 = primary_docs.collect("9999.TW", "20261020", run, shared_dir=shared)
    assert calls == ["tw_ftc"]
    assert "regulatory_antitrust" in axes2
    assert {s["name"]: s["status"] for s in primary_docs.load_manifest(run)["sources"]} == {
        "tw_company": "cached", "tw_mops": "cached", "tw_customers": "cached", "tw_ftc": "ok"}
    # --force 全部重抓
    calls.clear()
    primary_docs.collect("9999.TW", "20261020", run, force=True, shared_dir=shared)
    assert len(calls) == 4


def test_collect_writes_shared_csv_with_upsert(tmp_path, monkeypatch):
    monkeypatch.setattr(primary_docs, "_sources", lambda market: _fake_sources([]))
    monkeypatch.setattr(primary_docs, "_make_ctx", lambda *a, **k: types.SimpleNamespace(meta=None))
    shared = tmp_path / "data" / "primary_docs"
    shared.parent.mkdir()
    primary_docs.collect("9999.TW", "20261020", tmp_path / "r1", shared_dir=shared)
    primary_docs.collect("9999.TW", "20261021", tmp_path / "r2", shared_dir=shared)  # 同主鍵再寫一次不重複
    with (shared / "tw_major_customers.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert list(rows[0].keys()) == primary_docs.CUSTOMER_FIELDS and rows[0]["date"] == "2026-05-01"
    assert len(rows) == 1 and rows[0]["pct"] == "12.0"
    with (shared / "tw_material_news.csv").open(encoding="utf-8", newline="") as f:
        assert len(list(csv.DictReader(f))) == 1
    # 共用資料庫資料夾的上層不存在（雲端）→ 只略過 CSV，不報錯
    note = primary_docs._save_shared({"x": {"csv_news": [{"date": "d", "ticker": "t", "title": "t"}]}}, tmp_path / "nope" / "primary_docs")
    assert "略過" in note


def test_collect_unknown_market_returns_empty(tmp_path):
    assert primary_docs.collect("7203.T", "20261020", tmp_path / "r") == {}
    assert primary_docs.load_manifest(tmp_path / "r")["market"] is None


def test_detect_market():
    assert primary_docs.detect_market("2303.TW") == ("tw", "2303", "TW")
    assert primary_docs.detect_market("6488.TWO") == ("tw", "6488", "TWO")
    assert primary_docs.detect_market("00878.TW")[0] == "tw"
    assert primary_docs.detect_market("TXN") == ("us", "TXN", "")
    assert primary_docs.detect_market("BRK-B")[0] == "us"
    assert primary_docs.detect_market("7203.T")[0] is None and primary_docs.detect_market("0700.HK")[0] is None


# ---------------------------------------------------------------------------
# 模板注入
# ---------------------------------------------------------------------------

def _render(block, major=False):
    mapping = {"TICKER": "2303.TW", "N_AXES": "1", "MAX_SEARCH": "3", "AXES_BLOCK": "[x] 軸\n", "PART_PATH": "/p.json",
               "EVENTS_BLOCK": "## 事件\n" if major else "", "EVENTS_JSON_KEY": "", "PRIMARY_DOCS_BLOCK": block}
    return ddreport._render_template(TMPL, mapping)


def test_render_axis_block_empty_axis_leaves_prompt_unchanged():
    docs = {"major_events": [pc.mk_item("s", "d", "https://u", "2026-10-20", "sec", "本文")]}
    assert primary_docs.render_axis_block(docs, "geo_supply_chain") == ""
    assert primary_docs.render_axis_block({}, "major_events") == ""
    text = _render("")
    assert "{{" not in text and "程式已抓好的一手文件摘錄" not in text
    # 無摘錄的軸：與加區塊之前的模板逐字相同（把 placeholder 行還原後比對）
    legacy = TMPL.read_text(encoding="utf-8").replace("{{PRIMARY_DOCS_BLOCK}}{{EVENTS_BLOCK}}", "{{EVENTS_BLOCK}}")
    for k, v in {"TICKER": "2303.TW", "N_AXES": "1", "MAX_SEARCH": "3", "AXES_BLOCK": "[x] 軸\n", "PART_PATH": "/p.json",
                 "EVENTS_BLOCK": "", "EVENTS_JSON_KEY": ""}.items():
        legacy = legacy.replace("{{" + k + "}}", v)
    assert legacy == text


def test_render_axis_block_contains_url_asof_excerpt_rules():
    docs = {"major_events": [pc.mk_item("公開資訊觀測站", "歷史重大訊息清單", "https://mops/x", "2026-10-20", "標題清單", "命中 0 則")]}
    blk = primary_docs.render_axis_block(docs, "major_events")
    for needle in ("url：https://mops/x", "as_of：2026-10-20", "<<<\n命中 0 則\n>>>", "逐字複製", "經查一手紀錄無此類事件", "queries_run", "events"):
        assert needle in blk
    text = _render(blk, major=True)
    assert text.index("程式已抓好的一手文件摘錄") < text.index("## 事件") < text.index("## 回傳格式")
    assert "{{" not in text
    other = primary_docs.render_axis_block({"customer_concentration_credit": docs["major_events"]}, "customer_concentration_credit")
    assert "頂層 `events`" not in other  # 只有 major_events 軸加 events 提醒


def test_stage0_wiring_in_run_py():
    src = (SCRIPTS_DIR / "dd2" / "run.py").read_text(encoding="utf-8")
    assert "import primary_docs" in src and "primary_docs.collect(" in src
    assert '"PRIMARY_DOCS_BLOCK": primary_docs.render_axis_block(pdocs, axis_id)' in src
    assert src.count("PRIMARY_DOCS_BLOCK") == 1


# ---------------------------------------------------------------------------
# 實網（DD_PRIMARY_LIVE=1 才跑）
# ---------------------------------------------------------------------------

@pytest.mark.skipif(os.environ.get("DD_PRIMARY_LIVE") != "1", reason="實網測試：設 DD_PRIMARY_LIVE=1 才跑")
def test_live_collect_tw_and_us(tmp_path):
    shared = tmp_path / "shared"
    tw_axes = primary_docs.collect("2303.TW", dt.date.today().strftime("%Y%m%d"), tmp_path / "tw", shared_dir=shared)
    assert "major_events" in tw_axes and "customer_concentration_credit" in tw_axes
    us_axes = primary_docs.collect("TXN", dt.date.today().strftime("%Y%m%d"), tmp_path / "us")
    assert "customer_concentration_credit" in us_axes and "major_events" in us_axes


def test_ar_anchor_matches_two_year_arabic_ten_percent_heading():
    # 6223.TWO 114 年報：「最近兩年度佔銷貨總額 10%之客戶名單」（「兩」＋阿拉伯數字 10%）
    line = "  (2) 最近兩年度佔銷貨總額 10%之客戶名單"
    assert any(rx.search(line) for rx in tw.AR_ANCHORS)
    assert not any(rx.search("本公司 113 年度及 114 年度無佔進貨淨額 10%以上之廠商。") for rx in tw.AR_ANCHORS)
