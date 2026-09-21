"""notify_render 白話層：機械層已算好的結論（alert_level）要真的進到信裡。

2026-09-21：持有人指出「寄過來的東西不知道在表達什麼」。根因是 latest.json 的
alert_level（0-100 分＋band＋drivers）從未被通知層讀取，信只寄狀態機 diff。
本檔鎖住修正後的行為，避免日後改版又把結論漏掉。
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import notify_render as nr  # noqa: E402

DATA = REPO_ROOT / "docs" / "detective" / "data"

POINTS = [["2026-09-16", 61, "tense", 7551.8],
          ["2026-09-17", 56, "warming", 7637.7],
          ["2026-09-18", 64, "tense", 7650.5]]
LATEST = {"alert_level": {"score": 64, "band": "tense", "band_label": "緊張",
                          "drivers": [{"label": "62 條黃燈訊號（封頂計分）", "points": 18},
                                      {"label": "9 條訊號今日升級", "points": 16}]}}


def test_alert_facts_reads_score_prev_and_median():
    f = nr._alert_facts(LATEST, points=POINTS)
    assert f["score"] == 64
    assert f["band_label"] == "緊張"
    assert f["prev_score"] == 56 and f["prev_date"] == "2026-09-17"
    assert f["prev_band"] == "升溫"
    assert f["median"] == 61


def test_alert_facts_none_without_alert_level():
    assert nr._alert_facts({}, points=POINTS) is None
    assert nr._alert_facts({"alert_level": {}}, points=POINTS) is None


def test_alert_sentence_states_level_and_direction():
    s = nr._alert_sentence(nr._alert_facts(LATEST, points=POINTS))
    assert s.startswith("警戒度 64／100，屬「緊張」")
    assert "比前次高" in s and "前次 2026-09-17 為 56" in s
    assert s.endswith("。")


def test_alert_sentence_direction_words_cover_down_and_flat():
    down = dict(LATEST, alert_level=dict(LATEST["alert_level"], score=50))
    assert "比前次低" in nr._alert_sentence(nr._alert_facts(down, points=POINTS))
    flat = dict(LATEST, alert_level=dict(LATEST["alert_level"], score=56))
    assert "與前次持平" in nr._alert_sentence(nr._alert_facts(flat, points=POINTS))


def test_alert_sentence_html_bolds_score_and_escapes():
    h = nr._alert_sentence_html(nr._alert_facts(LATEST, points=POINTS))
    assert "警戒度 <b>64</b>／100" in h
    assert "<b>" in h and h.count("<b>") == 1


def test_alert_history_points_failsoft_on_missing_file():
    assert nr._alert_history_points(path="/nonexistent/alert_history.json") == []


def test_near_fire_count_counts_only_one_short_and_unfired():
    comps = [{"fired": False, "met_count": 2, "min_true": 3},   # 差一個 → 計
             {"fired": False, "met_count": 1, "min_true": 3},   # 差兩個 → 不計
             {"fired": True, "met_count": 3, "min_true": 3},    # 已成立 → 不計
             {"fired": False, "met_count": 0, "min_true": 0}]   # 無門檻 → 不計
    assert nr._near_fire_count(comps) == 1
    assert nr._near_fire_count([]) == 0


COMPOSITE = {
    "name": "股高位×信用背離×廣度走弱", "met_count": 2, "min_true": 3,
    "members": [
        {"met": True, "desc": "S&P 500 一年分位 ≥90（指數高位）"},
        {"met": False, "desc": "高收益／投資級相對比 分位 ≤25（信用相對走弱）",
         "current": "分位 94.0", "distance_label": "差 69.0 分位點"},
        {"met": True, "desc": "等權／市值 S&P 相對比 分位 ≤25（廣度走弱）"},
    ],
}


def test_composite_gap_sentence_names_what_is_missing():
    s = nr._composite_gap_sentence(COMPOSITE)
    assert "3 個條件成立 2 個" in s
    assert "已成立：" in s and "還差：" in s
    assert "分位 94.0" in s and "差 69.0 分位點" in s


def test_composite_gap_sentence_brief_drops_detail():
    s = nr._composite_gap_sentence(COMPOSITE, brief=True)
    assert "還差：高收益／投資級相對比 分位 ≤25" in s
    assert "已成立：" not in s and "差 69.0 分位點" not in s


def test_composite_gap_sentence_none_for_missing_rule():
    assert nr._composite_gap_sentence(None) is None


def test_kill_sentence_reports_near_not_just_breached():
    kw = {"coverage": {"mechanical": 12, "total": 1009}, "near": ["a"] * 7}
    s = nr._kill_sentence(kw, [])
    assert "0 條越線" in s
    assert "7 條已接近閾值" in s, "只報 breached=0 會讓讀者以為沒事"
    assert "12 條能被機器自動核對" in s and "共 1009 條" in s


def test_kill_sentence_none_without_table():
    assert nr._kill_sentence(None, []) is None


# ── 真資料端到端 ────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def real():
    return (json.loads((DATA / "latest.json").read_text(encoding="utf-8")),
            json.loads((DATA / "state.json").read_text(encoding="utf-8")))


LEAKS = ["breached", "Composite 0/", "Sources stale", "LLM",
         "composite fire", "Kill watch", "Composites（fired）"]


def test_real_digest_leads_with_alert_level(real):
    body = nr.render_digest(*real, force=True)
    assert "警戒度" in body and "／100" in body
    assert "分數來自：" in body


def test_real_weekly_leads_with_alert_level(real):
    body = nr.render_weekly(*real)
    assert "警戒度" in body and "否證指標：" in body


@pytest.mark.parametrize("tier", ["digest", "weekly"])
def test_real_bodies_have_no_internal_jargon(real, tier):
    body = (nr.render_digest(*real, force=True) if tier == "digest"
            else nr.render_weekly(*real))
    hits = [w for w in LEAKS if w in body]
    assert not hits, f"{tier} 仍有內部用語外流：{hits}"


@pytest.mark.parametrize("tier", ["digest", "weekly"])
def test_real_html_has_no_internal_jargon(real, tier):
    html = (nr.render_digest_html(*real, force=True) if tier == "digest"
            else nr.render_weekly_html(*real))
    hits = [w for w in LEAKS if w in html]
    assert not hits, f"{tier} HTML 仍有內部用語外流：{hits}"


def test_real_html_digest_shows_alert_tile(real):
    html = nr.render_digest_html(*real, force=True)
    assert "警戒度／100" in html
    assert "訊號總數" not in html, "總數＝紅＋黃，磚位應讓給警戒度"
