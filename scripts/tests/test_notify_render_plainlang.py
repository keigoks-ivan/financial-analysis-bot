"""市場偵探通知信的白話層。

2026-09-21 第一版：持有人指出「寄過來的東西不知道在表達什麼」。根因是 latest.json
的 alert_level（0-100 分＋等級＋drivers）從未被通知層讀取，信只寄狀態機 diff。
2026-09-21 第二版：持有人問「有辦法更白話嗎」。信裡剩下的偵測器名稱（監測／反轉）、
計分用語（封頂計分、差 1 個成員、閾值）、英文欄名（as-of、sev）全部換成白話；
複合規則的條件改用「技術門檻（白話）」格式，信只取括號裡的白話。

2026-09-21 第三版：持有人說「現在一堆數字，但是我不知道是哪些」。一分鐘版的每個
數量，底下新增「這些數字是哪些」一段列出名字。同時修正兩處講過頭的字：否證指標的
「接近」是離門檻 20% 以內，改寫「離警戒線不到兩成」；報告證偽表同時收「推翻」與
「升級」門檻，改寫「碰線就要回頭檢查那份報告的判斷」，不寫「看錯了」。

2026-10-13 第五版：持有人要「講重點」。每日摘要改成結論／要處理／要盯三段，
黃燈清單與名詞解釋只留在週報；改版前用一個月實際資料回放，補上紅燈解除、黃級
壓力面複合規則成立、類股急跌排序三個缺口。

2026-10-13 第六版：持有人「我都要知道最重要的事情要強調出來」。每日摘要與週報開頭
加一行粗體「最重要：…」（四層由重到輕取第一個有東西的層）；週報改成這週發生的事／
還在持續／下週要盯三段。

2026-10-06 第四版：警戒度拆成「有東西在壞」（警戒度，只數壓力面）與「漲太熱」
（熱度，另列、不計分），否證指標移出分數、獨立成「報告要重看」一行並附
「照平常的速度多久碰線」。closest_composite 不再選到已成立的規則；黃燈名單改依底層
序列去重，不再需要「×2＝兩個偵測器」的說法。

本檔鎖住六版的行為。真資料測試只斷言 notify_render 自己產的字，不斷言
latest.json 裡由 build_detective 產的 driver 字——那些要等每日排程重算才會更新。
"""
import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import build_detective as bd  # noqa: E402
import detective_rules as dr  # noqa: E402
import notify_render as nr  # noqa: E402

DATA = REPO_ROOT / "docs" / "detective" / "data"

POINTS = [["2026-09-16", 61, "tense", 7551.8],
          ["2026-09-17", 56, "warming", 7637.7],
          ["2026-09-18", 64, "tense", 7650.5]]
LATEST = {"alert_level": {"score": 64, "band": "tense", "band_label": "緊張",
                          "drivers": [{"label": "62 條訊號亮黃燈", "points": 18},
                                      {"label": "2 組複合規則只差一個條件就成立", "points": 12}]}}


def _facts(score=64):
    latest = {"alert_level": dict(LATEST["alert_level"], score=score)}
    return nr._alert_facts(latest, points=POINTS)


# ── 警戒度 ─────────────────────────────────────────────────────────────
def test_alert_facts_reads_score_rank_prev_and_median():
    f = _facts()
    assert f["score"] == 64 and f["band_label"] == "緊張"
    assert f["band_rank"] == 4
    assert f["prev_score"] == 56
    assert f["median"] == 61


def test_alert_facts_none_without_alert_level():
    assert nr._alert_facts({}, points=POINTS) is None
    assert nr._alert_facts({"alert_level": {}}, points=POINTS) is None


def test_alert_sentence_is_plain():
    s = nr._alert_sentence(_facts())
    assert s.startswith("警戒度 64 分，滿分 100，算「緊張」，是五級裡的第四級。")
    assert "比上一個交易日的 56 分高。" in s
    assert "平常大約 61 分。" in s
    for jargon in ("／100", "中位數", "前次", "屬「"):
        assert jargon not in s


def test_alert_sentence_direction_words():
    assert "比上一個交易日的 56 分低。" in nr._alert_sentence(_facts(50))
    assert "跟上一個交易日一樣是 56 分。" in nr._alert_sentence(_facts(56))


def test_alert_sentence_html_bolds_only_the_score():
    h = nr._alert_sentence_html(_facts())
    assert "警戒度 <b>64</b> 分" in h
    assert h.count("<b>") == 1


def test_alert_history_points_failsoft_on_missing_file():
    assert nr._alert_history_points(path="/nonexistent/alert_history.json") == []


def test_drivers_sentence():
    assert nr._alert_drivers_sentence(_facts()) == (
        "分數主要來自：62 條訊號亮黃燈、2 組複合規則只差一個條件就成立。")


# ── 名詞解釋 ───────────────────────────────────────────
def test_glossary_only_for_terms_present():
    assert nr._glossary_lines("沒有術語") == []
    both = nr._glossary_lines("3 組複合規則…7 條否證指標…")
    assert len(both) == 2 and both[0].startswith("複合規則＝")


# ── 複合規則 ───────────────────────────────────────────────────────────
COMPOSITE = {
    "name": "股高位×信用背離×廣度走弱", "met_count": 2, "min_true": 3,
    "members": [
        {"met": True, "desc": "S&P 500 一年分位 ≥90（指數在一年高點附近）"},
        {"met": False, "desc": "高收益／投資級相對比 分位 ≤25（高風險公司債比優質公司債弱）",
         "scale": "pctile", "op": "<=", "current_num": 94.0, "threshold_num": 25,
         "current": "分位 94.0", "distance_label": "差 69.0 分位點"},
        {"met": True, "desc": "等權／市值 S&P 相對比 分位 ≤25（大多數股票沒跟上指數）"},
    ],
}


def test_gloss_takes_last_fullwidth_paren():
    assert nr._gloss("SOFR（擔保隔夜利率）對 IORB（準備金利率）利差 >0（短期借錢變貴）") == "短期借錢變貴"
    assert nr._gloss("沒有括號") == "沒有括號"
    assert nr._gloss(None) == ""


def test_near_composites_only_one_short_and_unfired():
    comps = [{"fired": False, "met_count": 2, "min_true": 3},   # 差一件 → 算
             {"fired": False, "met_count": 1, "min_true": 3},   # 差兩件 → 不算
             {"fired": True, "met_count": 3, "min_true": 3},    # 已成立 → 不算
             {"fired": False, "met_count": 0, "min_true": 0}]   # 無門檻 → 不算
    assert nr._near_composites(comps) == [comps[0]]


# ── 否證指標 ───────────────────────────────────────────────────────────
def test_near_wording_matches_the_20pct_rule():
    """build_kill_watch 的 near＝離門檻 20% 以內；字面不能比規則講得更近。"""
    import build_kill_watch as bkw
    assert bkw.NEAR_BAND == 0.20
    # 否證指標已移出警戒度計分，driver 標籤不該再有 kill 兩項
    assert "kill_near" not in bd.ALERT_DRIVER_LABELS
    assert "kill_breached" not in bd.ALERT_DRIVER_LABELS


# ── 這些數字是哪些 ─────────────────────────────────────────────────────
@pytest.mark.parametrize("x,unit,want", [(5.37, "%", "5.37%"), (102.0, "DXY 指數", "102"),
                                         (7.2, "USD/CNY", "7.2"), (0.8892, "%", "0.89%"),
                                         (99.120003, "", "99.12"), (1.0, "%", "1%")])
def test_fmt_level(x, unit, want):
    assert nr._fmt_level(x, unit) == want


def test_dedupe_names_marks_repeats():
    assert nr._dedupe_names(["XLE 能源", "VIX", "XLE 能源", None, ""]) == ["XLE 能源 ×2", "VIX"]


def test_doc_title_takes_first_part_of_real_report_title():
    assert nr._doc_title("docs/macro/MACRO_USFiscalDeficit_20260708.html") == "美國財政赤字與利率上限"
    assert nr._doc_title("docs/macro/MACRO_DollarCycle_20260710.html") == "美元週期"
    assert nr._doc_title("docs/nope.html") == ""
    assert nr._doc_title(None) == ""


def test_kill_lines_name_report_metric_now_and_line():
    kw = {"near": ["a", "b", "c"], "items": [
        {"id": "a", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html",
         "metric_text": "10Y/30Y 殖利率", "current": 5.29, "value": 5.5, "op": ">=", "unit": "%"},
        {"id": "b", "theme": "Demo", "metric_text": "某數", "current": 12.0, "value": 10.0,
         "op": "<", "unit": ""},
        {"id": "c", "metric_text": "缺值"},
    ]}
    lines = nr._kill_group_lines(kw, kw["near"])
    assert lines[0] == "美國財政赤字與利率上限：10Y/30Y 殖利率，現在 5.29%，升到 5.5% 就碰線"
    assert lines[1] == "Demo：某數，現在 12，跌到 10 就碰線"
    assert lines[2] == "缺值。"
    assert nr._kill_group_lines(None, None) == []


def test_kill_phrases_never_claim_the_report_was_wrong():
    """證偽表同時收「推翻」與「升級」門檻，碰線不等於看錯。"""
    kw = json.loads((DATA / "kill_watch.json").read_text(encoding="utf-8"))
    text = ("".join(nr._kill_phrases(kw, kw.get("near"), "最快碰線", breached=False))
            + "".join(nr._kill_phrases(kw, kw.get("breached"), "越線"))
            + "".join(nr._glossary_lines("否證指標")))
    assert "看錯" not in text and "錯了" not in text


# ── 家族標籤（週報新增／解除清單）────────────────────────────────────────
@pytest.mark.parametrize("source,cat,direction,want", [
    ("monitor", "crypto", "up", "加密貨幣走升"),
    ("monitor", "fx", "", "外匯變動很大"),
    ("reversal", "fx", "", "外匯轉向"),
    ("reversal", "vol", "up", "波動指標轉為走升"),
    ("rotation", "quadrant", "down", "資產強弱排名轉弱"),
    ("sector", "diverge", "down", "和大盤分歧的產業轉弱"),
    ("crowding", "cot", "", "期貨部位擠在同一邊"),
    ("variance", "ticker", "", "個股財測和市場預期有落差"),
])
def test_family_label_is_thing_plus_what_happened(source, cat, direction, want):
    assert nr._family_label(source, cat, direction) == want


# ── 上游顯示字（build_detective／detective_rules）──────────────────────
def test_driver_labels_have_no_scoring_jargon():
    labels = [f(3) for f in bd.ALERT_DRIVER_LABELS.values()]
    for jargon in ("封頂", "成員", "閾值", "升級", "觸發", "≥"):
        assert not any(jargon in x for x in labels), jargon


def test_escalated_label_does_not_claim_worse():
    """escalated 含 sustained（黃→黃，只是沒退），不能寫成「變嚴重」。"""
    s = bd.ALERT_DRIVER_LABELS["escalated"](9)
    assert "持續" in s and "變嚴重" not in s


def _all_members():
    for rule in dr.RULES:
        stack = list(rule["members"])
        while stack:
            m = stack.pop()
            yield rule["id"], m
            stack.extend(m.get("conds", []))


TECH = ("分位", "≥", "≤", "|z|", "z ", "RS-M", "COT", "OAS", "TGA", "SOFR",
        "IORB", "VIX", "SKEW", ">", "<", "∈")


def test_every_rule_member_ends_with_plain_gloss():
    """信只取每個條件最後一組括號裡的白話；這個格式壞了信就會露出技術門檻。"""
    for rid, m in _all_members():
        g = re.search(r"（([^（）]*)）$", m["desc"])
        assert g, f"{rid} 條件缺白話結尾：{m['desc']}"
        hit = [t for t in TECH if t in g.group(1)]
        assert not hit, f"{rid} 白話結尾含技術字 {hit}：{m['desc']}"


# ── 真資料端到端 ────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def real():
    return (json.loads((DATA / "latest.json").read_text(encoding="utf-8")),
            json.loads((DATA / "state.json").read_text(encoding="utf-8")))


# 只列 notify_render 自己產的字。latest.json 裡 build_detective 產的 driver 字
# 要等排程重算，不在這裡斷言。
LEAKS = ["breached", "Composite 0/", "Sources stale", "LLM", "composite fire",
         "Kill watch", "Composites（fired）", "sev 真升級", "as-of", "監測",
         "詳頁面", "新觸發", "快照", "峰值", "歷時", "／100，屬",
         "快碰到", "看錯了", "逼近觸發程度", "成員 "]


@pytest.mark.parametrize("tier", ["digest", "weekly"])
def test_real_bodies_have_no_internal_jargon(real, tier):
    body = (nr.render_digest(*real, force=True) if tier == "digest"
            else nr.render_weekly(*real))
    hits = [w for w in LEAKS if w in body]
    assert not hits, f"{tier} 仍有內部用語：{hits}"


@pytest.mark.parametrize("tier", ["digest", "weekly"])
def test_real_html_has_no_internal_jargon(real, tier):
    html = (nr.render_digest_html(*real, force=True) if tier == "digest"
            else nr.render_weekly_html(*real))
    hits = [w for w in LEAKS if w in html]
    assert not hits, f"{tier} HTML 仍有內部用語：{hits}"


@pytest.mark.parametrize("tier", ["digest", "weekly"])
def test_real_emails_lead_with_alert_and_define_terms(real, tier):
    body = (nr.render_digest(*real, force=True) if tier == "digest"
            else nr.render_weekly(*real))
    lines = [l for l in body.splitlines() if l.strip()]
    assert lines[1].startswith("**最重要：") and lines[1].endswith("。**"), lines[1]
    assert lines[2].startswith("警戒度 "), lines[2]
    if tier == "digest":   # 2026-10-13 每日只講重點，名詞解釋留給週報
        return
    if "複合規則" in body:
        assert "複合規則＝" in body
    if "否證指標" in body:
        assert "否證指標＝" in body


def test_real_digest_only_key_points(real):
    """2026-10-13 持有人要「講重點」：越線的否證指標只講一次、不帶內部檔名，
    黃燈不再逐條點名，新增訊號只取最顯著的幾條。"""
    latest, state = real
    kw = json.loads((DATA / "kill_watch.json").read_text(encoding="utf-8"))
    body = nr.render_digest(latest, state, force=True)
    html = nr.render_digest_html(latest, state, force=True)
    for gone in ("這些數字是哪些", "黃燈分在哪裡", "（源 MACRO_", "kill_watch", "thesis"):
        assert gone not in body and gone not in html, gone
    items = {it["id"]: it for it in kw.get("items", [])}
    # 「最重要」那行刻意把最要緊的一條再講一次，其餘內文每條只講一次
    rest = "\n".join(l for l in body.splitlines() if not l.startswith("**最重要："))
    for nid in kw.get("breached") or []:
        metric = items[nid]["metric_text"]
        assert rest.count(metric) <= 1, metric   # 同一數字兩份報告各列一次的，合併成一行
    assert "要處理：" in body and nr.REST_ON_WEB in body
    new_lines = [l for l in body.splitlines() if l.startswith("・今天新增訊號裡最顯著的")]
    assert len(new_lines) <= 1
    # 訊號文字本身可能含「；」，所以直接數條數，不數分隔符
    assert len(nr._top_new_facts(nr._digest_compute(latest, state))) <= nr.TOP_NEW_SIGNALS


def test_composite_watch_line_names_shared_condition():
    def comp(pid, met, unmet, prox):
        return {"id": pid, "fired": False, "min_true": len(met) + len(unmet),
                "met_count": len(met), "proximity": prox,
                "members": [{"desc": f"x（{g}）", "met": True} for g in met]
                + [{"desc": f"x（{g}）", "met": False} for g in unmet]}
    shared = [comp("A", ["甲"], ["乙"], 0.5), comp("B", ["丙"], ["乙"], 0.5)]
    assert nr._composite_watch_line(shared) == "「乙」一旦發生，就有 2 組複合規則同時成立。"
    alone = [comp("A", ["甲"], ["乙"], 0.5), comp("B", ["丙"], ["丁"], 0.9)]
    assert nr._composite_watch_line(alone) == "最接近成立的複合規則，只差「丁」。"
    assert nr._composite_watch_line([comp("A", [], ["乙", "丁"], 0.1)]) is None


def test_new_signals_put_something_breaking_first(monkeypatch):
    """單一類股急跌（壓力面）不能被分數較高的類股象限翻轉擠掉。"""
    monkeypatch.setattr(nr.bd, "_signal_side", lambda s: s["side"])
    sigs = {f"k{i}": {"key": f"k{i}", "state": "new", "sev": "yellow", "score": sc,
                      "side": side, "fact": f"f{i}"}
            for i, (sc, side) in enumerate([(9, "other"), (8, "other"), (7, "other"), (5, "stress")])}
    monkeypatch.setattr(nr, "_dedupe_series", lambda xs: list(xs))
    assert nr._top_new_facts({"sig_by_key": sigs}) == ["f3", "f0", "f1"]


def test_fired_yellow_stress_composite_is_named_heat_ones_left_to_heat_line():
    def c(cid, sev):
        return {"id": cid, "fired": True, "sev": sev, "name": cid,
                "members": [{"desc": "x（甲）", "met": True}, {"desc": "x（乙）", "met": True}]}
    d = {"fired_composites": [c("R2", "yellow"), c("R6", "yellow"), c("R1", "red")]}
    assert nr._fired_stress_composite_lines(d) == ["複合規則已成立（黃燈）：甲、乙，同時發生。"]


def test_resolved_red_is_reported():
    d = {"resolved_red_keys": ["monitor:vol:move:up"], "keys_state": {}, "sig_by_key": {},
         "composite_by_key": {}, "history_by_key": {"monitor:vol:move:up":
                                                    {"peak_sev": "red", "days_active": 3}}}
    line = nr._resolved_red_line(d)
    assert line.startswith("今天解除的紅燈：") and "MOVE" in line
    assert nr._resolved_red_line(dict(d, resolved_red_keys=[])) is None


# ── 最重要的事（2026-10-13）────────────────────────────────────────────
def test_headline_takes_first_non_empty_tier_and_names_all_in_it():
    assert nr._headline([[], ["甲", "乙"], ["丙"]], "沒事。") == (2, "最重要：甲；乙。")
    assert nr._headline([[], [], []], "沒事。") == (4, "最重要：沒事。")
    assert nr._headline_text((1, "最重要：甲。")) == "**最重要：甲。**"
    assert "#b3261e" in nr._headline_html((1, "最重要：甲。"))     # 第一層用紅框


def _hd(active_red=(), fired=(), new_red=()):
    return {"as_of": "2026-10-12", "new_red_keys": list(new_red), "esc_red_keys": [],
            "active_red": list(active_red), "fired_composites": list(fired)}


def test_digest_headline_big_band_jump_comes_first(monkeypatch):
    monkeypatch.setattr(nr, "_alert_history_points",
                        lambda path=None: [["2026-10-09", 30, "watch"], ["2026-10-12", 70, "tense"]])
    latest = {"alert_level": {"score": 70, "band": "tense", "band_label": "緊張", "drivers": []}}
    red = {"key": "monitor:x", "source": "monitor", "sev": "red", "fact": "某指數大跌", "days_active": 1}
    tier, text = nr._digest_headline(latest, _hd([red]), {})
    assert tier == 1 and text == "最重要：警戒度升到「緊張」，70 分；某指數大跌（今天亮紅燈）。"


def test_digest_headline_small_band_jump_is_second_tier(monkeypatch):
    monkeypatch.setattr(nr, "_alert_history_points",
                        lambda path=None: [["2026-10-09", 10, "calm"], ["2026-10-12", 25, "watch"]])
    latest = {"alert_level": {"score": 25, "band": "watch", "band_label": "留意", "drivers": []}}
    assert nr._digest_headline(latest, _hd(), {}) == (2, "最重要：警戒度升到「留意」，25 分。")


def test_digest_headline_names_reports_still_breached(monkeypatch):
    monkeypatch.setattr(nr, "_alert_history_points", lambda path=None: [])
    kw = {"breached": ["macro:A:0"], "items": [
        {"id": "macro:A:0", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html", "metric_text": "M",
         "current": 6, "value": 5, "op": ">=", "unit": "", "data_source": {"type": "monitor", "key": "a"}}]}
    sig = {"key": "kill:A:0", "source": "kill", "sev": "red", "days_active": 6}
    tier, text = nr._digest_headline({}, _hd([sig]), kw)
    assert tier == 3
    assert text == "最重要：美國財政赤字與利率上限的否證指標還在越線（最久第 6 天），要回頭檢查判斷。"
    sig["days_active"] = 1
    tier, text = nr._digest_headline({}, _hd([sig]), kw)
    assert tier == 1 and "的否證指標今天越線：M，現在 6，已經越過 5" in text


def test_kill_phrases_merge_same_report():
    kw = {"items": [
        {"id": "a", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html", "metric_text": "M1",
         "current": 6, "value": 5, "op": ">=", "unit": "", "data_source": {"type": "monitor", "key": "a"}},
        {"id": "b", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html", "metric_text": "M2",
         "current": 3, "value": 2, "op": ">=", "unit": "", "data_source": {"type": "monitor", "key": "b"}}]}
    assert nr._kill_phrases(kw, ["a", "b"], "越線") == [
        "美國財政赤字與利率上限的否證指標越線：M1，現在 6，已經越過 5；M2，現在 3，已經越過 2"]


def test_nearest_kill_line_is_only_the_fastest_one():
    kw = {"near": ["slow", "dxy1", "dxy2", "fast"], "items": [
        _kwi("slow", "docs/macro/MACRO_USEconomy_20260708.html", "慢的", 1, 9, 900, ds="a/x"),
        _kwi("dxy1", "docs/macro/MACRO_DollarCycle_20260710.html", "DXY", 101.9, 102, 3.0),
        _kwi("dxy2", "docs/macro/MACRO_GlobalLiquidity_20260708.html", "DXY 同線", 101.9, 102, 3.0),
        _kwi("fast", "docs/macro/MACRO_USEconomy_20260708.html", "快的", 5, 6, 40, ds="b/y")]}
    line = nr._nearest_kill_line(kw)
    assert line.startswith("美元週期、全球流動性循環的否證指標最快碰線：DXY，現在 101.9")
    assert "慢的" not in line and "快的" not in line
    assert nr._nearest_kill_line({"near": []}) is None


def test_alert_week_sentence():
    pts = [["2026-10-05", 30, "watch"], ["2026-10-06", 20, "watch"], ["2026-10-08", 65, "tense"]]
    assert nr._alert_week_sentence(pts, "2026-10-06", "2026-10-12") == "這週警戒度在 20～65 分之間，10/8 升到「緊張」。"
    assert nr._alert_week_sentence(pts[:2], "2026-10-05", "2026-10-12") == "這週警戒度在 20～30 分之間，都在「留意」。"
    assert nr._alert_week_sentence([], "2026-10-06", "2026-10-12") is None


def test_real_weekly_three_sections_and_headline(real):
    latest, state = real
    body = nr.render_weekly(latest, state)
    html = nr.render_weekly_html(latest, state)
    assert "**最重要：" in body and "最重要：" in html
    assert "這週發生的事：" in body and nr.WEEK_REST_ON_WEB in body
    for gone in ("這些數字是哪些", "本週新增（", "本週解除（", "各資料來源的更新日期", "（無）", "kill_metric"):
        assert gone not in body and gone not in html, gone
    d = nr._weekly_compute(latest, state)
    if d["sustained_keys"]:
        assert f"連續亮 {nr.SUSTAINED_DAYS} 天以上、還沒退的黃燈：" in body


def test_breached_kill_lines_say_new_or_day_count():
    kw = {"items": [
        {"id": "macro:A:0", "doc": "", "theme": "A", "metric_text": "M1", "current": 6, "value": 5,
         "op": ">=", "unit": "", "days_to_line": 0.0, "data_source": {"type": "monitor", "key": "a"}},
        {"id": "macro:B:1", "doc": "", "theme": "B", "metric_text": "M2", "current": 6, "value": 5,
         "op": ">=", "unit": "", "days_to_line": 0.0, "data_source": {"type": "monitor", "key": "b"}}]}
    sigs = [{"key": "kill:A:0", "source": "kill", "days_active": 1},
            {"key": "kill:B:1", "source": "kill", "days_active": 6}]
    days = nr._kill_days_by_id(kw, sigs)
    assert days == {"macro:A:0": 1, "macro:B:1": 6}
    lines = nr._kill_group_lines(kw, ["macro:A:0", "macro:B:1"], breached=True, days_by_id=days)
    assert lines[0].endswith("（今天剛越線）") and lines[1].endswith("（第 6 天）")
    # 週報沿用舊呼叫方式，不帶天數
    assert nr._kill_group_lines(kw, ["macro:A:0"], breached=True)[0].endswith("已經越過 5")


def test_real_html_digest_shows_alert_tile(real):
    html = nr.render_digest_html(*real, force=True)
    assert "警戒度／100" in html
    assert "訊號總數" not in html, "總數＝紅＋黃，磚位應讓給警戒度"


def test_quiet_day_still_leads_with_alert(real, monkeypatch):
    """平靜日走提早收工的路徑，也要先講警戒度。"""
    latest, state = real
    real_compute = nr._digest_compute

    def quiet(latest_, state_):
        d = real_compute(latest_, state_)
        d["trivial"] = True
        return d

    monkeypatch.setattr(nr, "_digest_compute", quiet)
    body = nr.render_digest(latest, state, force=True)
    assert "警戒度 " in body and "今天沒有紅燈，也沒有新訊號" in body
    html = nr.render_digest_html(latest, state, force=True)
    assert "警戒度 <b>" in html


# ── 2026-10-06 拆分：熱度、報告要重看、照平常速度、closest_composite ────────────
def test_heat_facts_median_from_history_column_five():
    latest = {"heat_level": {"count": 20, "composites_fired": ["R6"], "as_of": "d"},
              "composites": [{"id": "R6", "name": "擁擠×動能翻轉"}]}
    pts = [["d%d" % i, 10, "calm", 1.0, h] for i, h in enumerate([10, 12, 14, 16, 18, 20])]
    pts.append(["old", 9, "calm", 1.0])            # 舊點沒有第 5 欄：不算
    f = nr._heat_facts(latest, points=pts)
    assert f["count"] == 20 and f["median"] == 15 and f["fired"] == ["擁擠×動能翻轉"]
    assert nr._heat_sentence(f) == "熱度：亮 20 盞，平常大約 15 盞。已成立的過熱類複合規則：擁擠×動能翻轉。"


def test_heat_sentence_omits_usual_when_history_too_short():
    f = nr._heat_facts({"heat_level": {"count": 7, "composites_fired": []}},
                       points=[["d", 1, "calm", 1.0, 5]])
    assert f["median"] is None
    assert nr._heat_sentence(f) == "熱度：亮 7 盞。"
    assert nr._heat_facts({}, points=[]) is None
    assert nr._heat_sentence(None) is None


@pytest.mark.parametrize("days,want", [
    (0.5, "幾天內就可能碰到"), (14, "幾天內就可能碰到"), (30, "大約要幾週才會碰到"),
    (200, "大約要幾個月才會碰到"), (700, "大約要一兩年才會碰到"),
    (5000, "要好幾年才會碰到")])
def test_pace_phrase(days, want):
    assert nr._pace_phrase(days) == "照平常的速度，" + want


def test_pace_phrase_none_is_empty():
    assert nr._pace_phrase(None) == ""


def _kwi(i, doc, metric, cur, val, days, ds="fx/dxy", op=">="):
    return {"id": i, "doc": doc, "theme": "T" + i, "metric_text": metric, "current": cur,
            "value": val, "op": op, "unit": "", "days_to_line": days,
            "data_source": {"type": "monitor", "key": ds}}


def test_kill_lines_sorted_by_pace_and_same_line_merged():
    kw = {"near": ["slow", "dxy1", "dxy2", "fast"], "breached": [], "items": [
        _kwi("slow", "docs/macro/MACRO_USFiscalDeficit_20260708.html", "慢的", 1, 9, 900, ds="a/x"),
        _kwi("dxy1", "docs/macro/MACRO_DollarCycle_20260710.html", "DXY", 101.9, 102, 3.0),
        _kwi("dxy2", "docs/macro/MACRO_GlobalLiquidity_20260708.html", "DXY 同線", 101.9, 102, 3.0),
        _kwi("fast", "docs/macro/MACRO_USFiscalDeficit_20260708.html", "快的", 5, 6, 40, ds="b/y"),
    ]}
    lines = nr._kill_group_lines(kw, kw["near"])
    assert len(lines) == 3                                # 兩份報告同一條美元線合併成一行
    assert lines[0].startswith("美元週期、全球流動性循環：DXY，")     # 最快的在前、點名兩份報告
    assert "幾天內就可能碰到" in lines[0]
    assert "大約要幾週才會碰到" in lines[1] and "快的" in lines[1]
    assert "要好幾年" not in lines[2] and "大約要一兩年才會碰到" in lines[2]


def test_kill_lines_without_pace_keep_old_wording():
    kw = {"near": ["a"], "items": [
        {"id": "a", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html",
         "metric_text": "10Y/30Y 殖利率", "current": 5.29, "value": 5.5, "op": ">=", "unit": "%"}]}
    assert nr._kill_group_lines(kw, kw["near"]) == [
        "美國財政赤字與利率上限：10Y/30Y 殖利率，現在 5.29%，升到 5.5% 就碰線"]


def test_kill_breached_lines_say_already_crossed():
    kw = {"breached": ["a"], "items": [
        {"id": "a", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html",
         "metric_text": "10Y/30Y 殖利率", "current": 5.63, "value": 5.5, "op": ">=", "unit": "%"}]}
    assert nr._kill_group_lines(kw, kw["breached"], breached=True) == [
        "美國財政赤字與利率上限：10Y/30Y 殖利率，現在 5.63%，已經越過 5.5%"]


def test_estimate_days_to_line_random_walk():
    import build_kill_watch as bkw
    spark = [100 + (i % 2) for i in range(30)]            # 每步 ±1，σ≈1
    d = bkw.estimate_days_to_line(spark, "daily", 100.0, 110.0, "near")
    assert 100 < d * 0.9 and d < 160                       # (10/1)² 步 × 1.4 天
    assert bkw.estimate_days_to_line(spark, "daily", 1, 2, "breached") == 0.0
    assert bkw.estimate_days_to_line([1.0] * 30, "daily", 1, 2, "near") is None   # σ=0
    assert bkw.estimate_days_to_line(spark[:5], "daily", 1, 2, "near") is None    # 點太少
    assert bkw.estimate_days_to_line(spark, "quarterly", 1, 2, "near") is None    # 頻率未知
    assert bkw.estimate_days_to_line(None, "daily", 1, 2, "near") is None


def test_digest_order_conclusion_then_action_then_watch(real, tmp_path, monkeypatch):
    latest, state = real
    latest = dict(latest, heat_level={"count": 20, "composites_fired": [], "as_of": latest["as_of"]})
    kw = {"breached": ["a"], "near": [], "items": [
        {"id": "a", "doc": "", "theme": "T", "metric_text": "M", "current": 6, "value": 5,
         "op": ">=", "unit": "", "days_to_line": 0.0, "data_source": {"type": "monitor", "key": "x/y"}}]}
    kwp = tmp_path / "kw.json"
    kwp.write_text(json.dumps(kw), encoding="utf-8")
    monkeypatch.setattr(nr, "DEFAULT_KILL_WATCH", str(kwp))
    body = nr.render_digest(latest, state, force=True)
    i_alert, i_heat = body.index("警戒度 "), body.index("熱度：亮 20 盞")
    i_act = body.index("要處理：1 份研究報告的否證指標越線")
    i_line = body.index("・T：M，現在 6，已經越過 5")
    assert i_alert < i_heat < i_act < i_line
    if "要盯：" in body:
        assert i_line < body.index("要盯：")
    html = nr.render_digest_html(latest, state, force=True)
    assert html.index("熱度：亮 20 盞") < html.index("要處理") < html.index("T：M，現在 6")
