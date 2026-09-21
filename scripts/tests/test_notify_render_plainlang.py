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

本檔鎖住三版的行為。真資料測試只斷言 notify_render 自己產的字，不斷言
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
                                      {"label": "7 條否證指標離警戒線不到兩成", "points": 15}]}}


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
        "分數主要來自：62 條訊號亮黃燈、7 條否證指標離警戒線不到兩成。")


# ── 紅燈、訊號進出、名詞解釋 ───────────────────────────────────────────
def test_red_sentence_says_so_when_there_is_none():
    assert nr._red_sentence(0) == "今天沒有任何訊號亮紅燈。紅燈是最嚴重的一級。"
    s = nr._red_sentence(2, "某訊號大跌")
    assert s.startswith("有 2 條訊號亮紅燈") and s.endswith("最嚴重的是：某訊號大跌")


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
    assert "不到兩成" in bd.ALERT_DRIVER_LABELS["kill_near"](7)
    assert "快碰到" not in bd.ALERT_DRIVER_LABELS["kill_near"](7)


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
        assert f"離警戒線不到兩成的否證指標（{n_near} 條）" in heads
        assert len(blocks[heads.index(f"離警戒線不到兩成的否證指標（{n_near} 條）")][1]) == n_near
    n_comp_near = len(nr._near_composites(latest.get("composites")))
    assert any(h.startswith(f"只差一件事就成立的複合規則（{n_comp_near} 組") for h in heads)
    n_yellow = sum(1 for s in latest["signals"] if s.get("sev") != "red")
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
