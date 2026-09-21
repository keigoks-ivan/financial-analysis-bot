"""市場偵探通知信的白話層。

2026-09-21 第一版：持有人指出「寄過來的東西不知道在表達什麼」。根因是 latest.json
的 alert_level（0-100 分＋等級＋drivers）從未被通知層讀取，信只寄狀態機 diff。
2026-09-21 第二版：持有人問「有辦法更白話嗎」。信裡剩下的偵測器名稱（監測／反轉）、
計分用語（封頂計分、差 1 個成員、閾值）、英文欄名（as-of、sev）全部換成白話；
複合規則的條件改用「技術門檻（白話）」格式，信只取括號裡的白話。

本檔鎖住兩版的行為。真資料測試只斷言 notify_render 自己產的字，不斷言
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
                                      {"label": "7 條否證指標快碰到警戒線", "points": 15}]}}


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
        "分數主要來自：62 條訊號亮黃燈、7 條否證指標快碰到警戒線。")


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


def test_composite_brief_uses_only_plain_words():
    s = nr._composite_gap_sentence(COMPOSITE, brief=True)
    assert s == ("最接近成立的一組複合規則，要 3 件事同時發生，現在發生了 2 件："
                 "指數在一年高點附近、大多數股票沒跟上指數。"
                 "還沒發生的是：高風險公司債比優質公司債弱。")


def test_composite_full_explains_percentile():
    s = nr._composite_gap_sentence(COMPOSITE)
    assert "最接近成立的是「股高位×信用背離×廣度走弱」" in s
    assert "這一項現在在第 94 百分位，要掉到 25 以下才算" in s
    assert "100 最高、0 最低" in s


def test_composite_k_of_n_wording():
    c = dict(COMPOSITE, min_true=2, met_count=1)
    assert "3 件事裡要有 2 件同時發生" in nr._composite_gap_sentence(c, brief=True)


def test_composite_head_and_near_count():
    comps = [{"fired": False, "met_count": 2, "min_true": 3},
             {"fired": False, "met_count": 1, "min_true": 3},
             {"fired": True, "met_count": 3, "min_true": 3},
             {"fired": False, "met_count": 0, "min_true": 0}]
    assert nr._near_fire_count(comps) == 1
    assert nr._composite_head(comps) == "4 組複合規則，目前沒有一組成立，有 1 組只差一件事。"


def test_composite_gap_sentence_none_for_missing_rule():
    assert nr._composite_gap_sentence(None) is None


# ── 否證指標 ───────────────────────────────────────────────────────────
def test_kill_sentence_reports_near_not_just_breached():
    kw = {"coverage": {"mechanical": 12, "total": 1009, "llm_only": 997}, "near": ["a"] * 7}
    assert nr._kill_sentence(kw, []) == (
        "否證指標沒有一條越過警戒線，但有 7 條快碰到了。"
        "機器能自動檢查的只有 12 條，另外 997 條要靠人看。")


def test_kill_sentence_breached_and_quiet():
    kw = {"coverage": {"mechanical": 12, "total": 20}, "near": []}
    assert nr._kill_sentence(kw, ["x", "y"]).startswith("有 2 條否證指標已經越過警戒線。")
    assert "也沒有快碰到的" in nr._kill_sentence(kw, [])
    assert "另外 8 條要靠人看" in nr._kill_sentence(kw, [])


def test_kill_sentence_none_without_table():
    assert nr._kill_sentence(None, []) is None


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
         "詳頁面", "新觸發", "快照", "峰值", "歷時", "／100，屬"]


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
