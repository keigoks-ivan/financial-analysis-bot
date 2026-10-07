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

2026-10-06 第四版：警戒度拆成「有東西在壞」（警戒度，只數壓力面）與「漲太熱」
（熱度，另列、不計分），否證指標移出分數、獨立成「報告要重看」一行並附
「照平常的速度多久碰線」。closest_composite 不再選到已成立的規則；黃燈名單改依底層
序列去重，不再需要「×2＝兩個偵測器」的說法。

本檔鎖住四版的行為。真資料測試只斷言 notify_render 自己產的字，不斷言
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


# ── 紅燈、訊號進出、名詞解釋 ───────────────────────────────────────────
def test_red_sentence_says_so_when_there_is_none():
    assert nr._red_sentence(0) == "今天沒有任何訊號亮紅燈。紅燈是最嚴重的一級。"
    s = nr._red_sentence(2, "某訊號大跌")
    assert s.startswith("有 2 條訊號亮紅燈") and s.endswith("最嚴重的是：某訊號大跌")


def test_red_sentence_says_when_reds_are_not_in_alert_score():
    s = nr._red_sentence(4, None, 0)
    assert "都沒算進警戒度" in s
    s = nr._red_sentence(4, None, 1)
    assert "其中 1 條算進警戒度，另外 3 條不算" in s
    assert "警戒度" not in nr._red_sentence(2, None, 2)


@pytest.mark.parametrize("new,res,tail", [(32, 39, "總數少了 7 條"),
                                          (40, 30, "總數多了 10 條"),
                                          (5, 5, "總數沒變")])
def test_net_change_sentence_gives_direction(new, res, tail):
    s = nr._net_change_sentence(new, res)
    assert f"新增 {new} 條、解除 {res} 條" in s and tail in s


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


def test_composite_sentence_uses_only_plain_words():
    s = nr._composite_gap_sentence(COMPOSITE)
    assert s == ("最接近成立的一組複合規則，要 3 件事同時發生，現在發生了 2 件："
                 "指數在一年高點附近、大多數股票沒跟上指數。"
                 "還沒發生的是：高風險公司債比優質公司債弱。")


def test_composite_k_of_n_wording():
    c = dict(COMPOSITE, min_true=2, met_count=1)
    assert "3 件事裡要有 2 件同時發生" in nr._composite_gap_sentence(c)


def test_near_composites_only_one_short_and_unfired():
    comps = [{"fired": False, "met_count": 2, "min_true": 3},   # 差一件 → 算
             {"fired": False, "met_count": 1, "min_true": 3},   # 差兩件 → 不算
             {"fired": True, "met_count": 3, "min_true": 3},    # 已成立 → 不算
             {"fired": False, "met_count": 0, "min_true": 0}]   # 無門檻 → 不算
    assert nr._near_composites(comps) == [comps[0]]


def test_composite_gap_sentence_none_for_missing_rule():
    assert nr._composite_gap_sentence(None) is None


# ── 否證指標 ───────────────────────────────────────────────────────────
def test_kill_sentence_ties_near_to_the_machine_checked_ones():
    kw = {"coverage": {"mechanical": 12, "total": 1009, "llm_only": 997}, "near": ["a"] * 7}
    assert nr._kill_sentence(kw, []) == (
        "否證指標沒有一條越過警戒線。機器能自動檢查的 12 條裡，有 7 條離警戒線不到兩成。"
        "另外 997 條沒辦法自動檢查，要靠人看。")


def test_kill_sentence_breached_and_quiet():
    kw = {"coverage": {"mechanical": 12, "total": 20}, "near": []}
    assert nr._kill_sentence(kw, ["x", "y"]).startswith("有 2 條否證指標已經越過警戒線。")
    assert "都離警戒線還有兩成以上" in nr._kill_sentence(kw, [])
    assert "另外 8 條沒辦法自動檢查" in nr._kill_sentence(kw, [])


def test_near_wording_matches_the_20pct_rule():
    """build_kill_watch 的 near＝離門檻 20% 以內；字面不能比規則講得更近。"""
    import build_kill_watch as bkw
    assert bkw.NEAR_BAND == 0.20
    # 否證指標已移出警戒度計分，driver 標籤不該再有 kill 兩項
    assert "kill_near" not in bd.ALERT_DRIVER_LABELS
    assert "kill_breached" not in bd.ALERT_DRIVER_LABELS
    one_min = nr._kill_minute_sentence({"breached": [], "near": ["a"], "items": []})
    assert "不到兩成" in one_min and "快碰到" not in one_min


def test_kill_sentence_none_without_table():
    assert nr._kill_sentence(None, []) is None


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


def test_kill_near_lines_name_report_metric_now_and_line():
    kw = {"near": ["a", "b", "c"], "items": [
        {"id": "a", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html",
         "metric_text": "10Y/30Y 殖利率", "current": 5.29, "value": 5.5, "op": ">=", "unit": "%"},
        {"id": "b", "theme": "Demo", "metric_text": "某數", "current": 12.0, "value": 10.0,
         "op": "<", "unit": ""},
        {"id": "c", "metric_text": "缺值"},
    ]}
    lines = nr._kill_near_lines(kw)
    assert lines[0] == "美國財政赤字與利率上限：10Y/30Y 殖利率，現在 5.29%，升到 5.5% 就碰線"
    assert lines[1] == "Demo：某數，現在 12，跌到 10 就碰線"
    assert lines[2] == "缺值。"
    assert nr._kill_near_lines(None) == []


def test_kill_near_lines_never_claim_the_report_was_wrong():
    """證偽表同時收「推翻」與「升級」門檻，碰線不等於看錯。"""
    kw = json.loads((DATA / "kill_watch.json").read_text(encoding="utf-8"))
    text = "".join(nr._kill_near_lines(kw)) + nr.KILL_NEAR_NOTE + "".join(nr._glossary_lines("否證指標"))
    assert "看錯" not in text and "錯了" not in text
    assert "回頭檢查" in nr.KILL_NEAR_NOTE


def test_near_composite_lines():
    assert nr._near_composite_lines([COMPOSITE]) == [
        "已經發生：指數在一年高點附近、大多數股票沒跟上指數。還差：高風險公司債比優質公司債弱。"]
    k_of_n = dict(COMPOSITE, min_true=2, met_count=1,
                  members=[dict(COMPOSITE["members"][0], met=True),
                           dict(COMPOSITE["members"][1], met=False),
                           dict(COMPOSITE["members"][2], met=False)])
    assert "還差其中一件：" in nr._near_composite_lines([k_of_n])[0]


def _sig(label, state="active", sev="yellow", dim="credit", esc_type=None):
    s = {"label": label, "state": state, "sev": sev, "dim": dim}
    if esc_type:
        s["escalations"] = [{"type": esc_type}]
    return s


def test_escalated_note_only_when_all_are_just_sustained():
    sustained = [_sig("A", "escalated", esc_type="sustained"),
                 _sig("B", "escalated", esc_type="sustained"), _sig("C")]
    names, note = nr._escalated_names_and_note(sustained)
    assert names == ["A", "B"]
    assert "沒有一條變成紅燈" in note and f"連續亮 {nr.SUSTAINED_DAYS} 天" in note
    mixed = [_sig("A", "escalated", esc_type="sustained"),
             _sig("B", "escalated", esc_type="sev_jump")]
    assert nr._escalated_names_and_note(mixed)[1] == ""


def test_yellow_by_dim_groups_dedupes_and_skips_red():
    sigs = [_sig("HYG", dim="credit"), _sig("LQD", dim="credit"), _sig("LQD", dim="credit"),
            _sig("VIX", dim="vol_options"), _sig("紅的", sev="red", dim="credit")]
    assert nr._yellow_by_dim(sigs) == [("公司債", 3, ["HYG", "LQD ×2"]), ("波動", 1, ["VIX"])]


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


def test_direction_of():
    assert nr._direction_of(["a:x:up", "b:y:up"]) == "up"
    assert nr._direction_of(["a:x:up", "b:y:down"]) == ""
    assert nr._direction_of(["a:x"]) == ""


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
    first = [l for l in body.splitlines() if l.strip()][1]
    assert first.startswith("警戒度 "), first
    if "複合規則" in body:
        assert "複合規則＝" in body
    if "否證指標" in body:
        assert "否證指標＝" in body


def test_real_digest_names_what_is_behind_each_count(real):
    latest, state = real
    kw = json.loads((DATA / "kill_watch.json").read_text(encoding="utf-8"))
    blocks = nr._which_ones_digest(latest, latest.get("composites"), kw)
    heads = [b[0] for b in blocks]
    n_near = len(kw.get("near") or [])
    if n_near:
        head = f"離警戒線不到兩成的否證指標（{n_near} 條）"
        assert head in heads
        # 同一個數字被兩份報告各列一次會合併成一行，所以行數 ≤ 條數
        assert 1 <= len(blocks[heads.index(head)][1]) <= n_near
    n_b = len(kw.get("breached") or [])
    if n_b:
        assert f"已越線的否證指標（{n_b} 條）" in heads
    n_comp_near = len(nr._near_composites(latest.get("composites")))
    assert any(h.startswith(f"只差一件事就成立的複合規則（{n_comp_near} 組") for h in heads)
    n_yellow = sum(1 for s in nr._dedupe_series(latest["signals"]) if s.get("sev") != "red")
    assert f"{n_yellow} 條黃燈分在哪裡" in heads
    body = nr.render_digest(latest, state, force=True)
    html = nr.render_digest_html(latest, state, force=True)
    assert "這些數字是哪些" in body and "這些數字是哪些" in html


def test_real_weekly_names_sustained_and_near_kill(real):
    latest, state = real
    d = nr._weekly_compute(latest, state)
    assert len(d["sustained_keys"]) == d["sustained_count"]
    body = nr.render_weekly(latest, state)
    if d["sustained_count"]:
        assert f"還沒退的黃燈（{d['sustained_count']} 條）" in body


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
    lines = nr._kill_near_lines(kw)
    assert len(lines) == 3                                # 兩份報告同一條美元線合併成一行
    assert lines[0].startswith("美元週期、全球流動性循環：DXY，")     # 最快的在前、點名兩份報告
    assert "幾天內就可能碰到" in lines[0]
    assert "大約要幾週才會碰到" in lines[1] and "快的" in lines[1]
    assert "要好幾年" not in lines[2] and "大約要一兩年才會碰到" in lines[2]


def test_kill_lines_without_pace_keep_old_wording():
    kw = {"near": ["a"], "items": [
        {"id": "a", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html",
         "metric_text": "10Y/30Y 殖利率", "current": 5.29, "value": 5.5, "op": ">=", "unit": "%"}]}
    assert nr._kill_near_lines(kw) == [
        "美國財政赤字與利率上限：10Y/30Y 殖利率，現在 5.29%，升到 5.5% 就碰線"]


def test_kill_breached_lines_say_already_crossed():
    kw = {"breached": ["a"], "items": [
        {"id": "a", "doc": "docs/macro/MACRO_USFiscalDeficit_20260708.html",
         "metric_text": "10Y/30Y 殖利率", "current": 5.63, "value": 5.5, "op": ">=", "unit": "%"}]}
    assert nr._kill_breached_lines(kw) == [
        "美國財政赤字與利率上限：10Y/30Y 殖利率，現在 5.63%，已經越過 5.5%"]


def test_kill_minute_sentence():
    kw = {"breached": ["a", "b"], "near": ["c", "d"], "items": [
        {"id": "c", "days_to_line": 400.0}, {"id": "d", "days_to_line": 9.0}]}
    s = nr._kill_minute_sentence(kw)
    assert s == ("報告要重看：2 條否證指標已越線。另有 2 條離警戒線不到兩成，"
                 "其中最快的一條，照平常的速度，幾天內就可能碰到。")
    assert nr._kill_minute_sentence({"breached": [], "near": [], "items": []}) == \
        "報告要重看：目前沒有否證指標越線。"
    assert nr._kill_minute_sentence(None) is None


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


def _comp(cid, fired, prox, met=1, need=2):
    return {"id": cid, "name": "規則" + cid, "status": "active", "fired": fired,
            "proximity": prox, "met_count": met, "min_true": need, "members": [], "sev": "yellow"}


def test_closest_composite_excludes_fired_ones():
    latest = {"as_of": "d", "signals": [], "counts": {},
              "composites": [_comp("R6", True, 1.0, 2, 2), _comp("R1", False, 0.67, 2, 3),
                             _comp("R7", False, 0.5)]}
    d = nr._digest_compute(latest, {"transitions_today": [], "keys": {}, "history": []})
    assert d["closest_composite"]["id"] == "R1"
    only_fired = dict(latest, composites=[_comp("R6", True, 1.0, 2, 2)])
    d2 = nr._digest_compute(only_fired, {"transitions_today": [], "keys": {}, "history": []})
    assert d2["closest_composite"] is None


def test_gap_sentence_for_fired_rule_says_already_in_effect():
    s = nr._composite_gap_sentence(_comp("R6", True, 1.0, 2, 2))
    assert s == "複合規則「規則R6」已成立。" and "最接近" not in s


def test_yellow_by_dim_dedupes_same_series_across_detectors():
    def sg(key, label, **kw):
        return dict({"key": key, "label": label, "sev": "yellow", "score": 6, "dim": "equity_structure"}, **kw)
    sigs = [sg("monitor:indices:hsi:down", "香港恆生"), sg("reversal:indices:hsi:down", "香港恆生"),
            sg("crowding:theme:advanced-packaging", "主題擁擠：Advanced Packaging", dim="positioning"),
            sg("crowding:theme:advancedpackaging", "主題擁擠：AdvancedPackaging", dim="positioning")]
    rows = nr._yellow_by_dim(sigs)
    assert sum(r[1] for r in rows) == 2                    # 各只剩一條，不再出現 ×2
    assert all("×" not in "".join(r[2]) for r in rows)


def test_digest_one_minute_order_alert_heat_kill_composite(real, tmp_path, monkeypatch):
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
    i_kill, i_gap = body.index("報告要重看：1 條否證指標已越線"), body.index("最接近成立的一組複合規則")
    assert i_alert < i_heat < i_kill < i_gap
    html = nr.render_digest_html(latest, state, force=True)
    assert html.index("熱度：亮 20 盞") < html.index("報告要重看") < html.index("最接近成立")
