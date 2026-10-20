"""2026-10-20：findings_digest 對無 findings 的軸只分 none／gap，業態不適用的軸
（金融的客戶第二來源、客戶集中度，由程式標 not_applicable）因此被標成 gap，
判斷與閘讀 facts.json 時會當成缺口。改成照抄 not_applicable。
"""
from __future__ import annotations

from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import dd_facts  # noqa: E402


def _status_by_axis(coverage):
    digest = dd_facts.build_findings_digest({"coverage": coverage, "events": {}})
    return {d["axis"]: d["status"] for d in digest}


def test_empty_axis_status_keeps_none_and_not_applicable():
    got = _status_by_axis({
        "a_none": {"status": "none", "findings": []},
        "a_missing_status": {"findings": []},
        "a_na": {"status": "not_applicable", "findings": []},
        "a_pending": {"status": "pending", "findings": []},
        "a_found_empty": {"status": "found", "findings": []},
    })
    assert got == {
        "a_none": "none",
        "a_missing_status": "none",
        "a_na": "not_applicable",
        "a_pending": "gap",
        "a_found_empty": "gap",
    }


def test_axis_with_findings_unchanged():
    got = _status_by_axis({
        "a_found": {"status": "found", "findings": [{"claim": "x", "direction": "+"}]},
    })
    assert got == {"a_found": "ok"}
