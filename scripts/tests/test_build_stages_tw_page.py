"""個股階段雷達（台股）page (scripts/build_stages_tw_page.py), 2026-10-10.

Runs the derivation against the real US page so a moved anchor fails here
before the workflow does. No network.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_stages_tw_page as page  # noqa: E402

FACTS = {"n": 230, "radar": 200, "pool": 78, "floor_usd_wan": 500.0,
         "floor_twd_yi": 1.53, "fx": 30.6, "low": ["收縮完成"], "win": 233}


def _render():
    html, problems = page.render(page.US_PAGE.read_text(encoding="utf-8"), FACTS)
    assert problems == [] and html is not None
    return html


def test_every_us_anchor_is_found():
    _render()


def test_tw_page_reads_tw_files_and_drops_us_parts():
    html = _render()
    assert 'fetchJSON("../data/latest_tw.json"), fetchJSON("../data/history_tw.json")' in html
    assert "imq-badge" not in html and "qt-matrix-mount" not in html
    assert "<title>個股階段雷達（台股）" in html and '<a href="/stages/">美股</a><span class="on">台股</span>' in html
    assert "0050（右軸）" in html and "相對大盤（0050 還原權息）" in html
    assert "低於 500 萬美元、約新台幣 1.5 億元" in html
    assert "fmtTwd(r.adv20_twd)" in html and "r.name" in html


def test_missing_anchor_leaves_page_unwritten():
    us = page.US_PAGE.read_text(encoding="utf-8").replace("QQQ（右軸）", "QQQ")
    html, problems = page.render(us, FACTS)
    assert html is None and problems


def test_low_sample_stages_are_named_from_the_data():
    assert "少見的段一年內的進場事件不到 20 筆（目前是收縮完成）" in _render()
    html, _ = page.render(page.US_PAGE.read_text(encoding="utf-8"), {**FACTS, "low": []})
    assert "少見的段一年內的進場事件不到 20 筆，轉場基率表上" in html


def test_stage_names_match_the_us_build():
    import build_stages
    assert page.STAGE_ZH == {k: v for k, v in build_stages.STAGE_NAMES.items() if k != "S9"}


def test_window_days_come_from_the_data():
    html = _render()
    assert "過去 250 個交易日" not in html
    assert "<h2>轉場基率：過去 233 個交易日" in html and "所以轉場基率只回算 233 個交易日" in html


def test_us_page_switch_is_replaced_not_duplicated():
    us = page.US_PAGE.read_text(encoding="utf-8")
    assert '<span class="on">美股</span><a href="/stages/tw/">台股</a>' in us
    html = _render()
    assert html.count('class="mkt-switch"') == 1 and html.count(".mkt-switch{") == 1
    assert '<a href="/stages/tw/">台股</a>' not in html
    html, problems = page.render(us.replace('<div class="mkt-switch"', '<div class="mkt-x"'), FACTS)
    assert html is None and problems
