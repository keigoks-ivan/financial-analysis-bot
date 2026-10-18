#!/usr/bin/env python3
"""2026-10-19：docs/intel 日報（data）與抓取檔（pending）的保留規則測試。

規則：pending 留最近 7 份、data 留最近 14 份；只認 YYYY-MM-DD.json；狀態檔、日期頁、壞檔名一律不動；
protect 內的日期不刪；重複執行不再刪。
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR / "intel"))
import data_retention as retention  # noqa: E402

FIRST = date(2026, 8, 1)


def _make_days(directory, count, first=FIRST):
    directory.mkdir(parents=True, exist_ok=True)
    names = []
    for i in range(count):
        name = (first + timedelta(days=i)).isoformat() + ".json"
        (directory / name).write_text("{}", encoding="utf-8")
        names.append(name)
    return names


def _present(directory):
    return sorted(p.name for p in directory.glob("*.json"))


def test_defaults_match_documented_rule():
    assert retention.KEEP_PENDING == 7
    assert retention.KEEP_DAILY == 14


def test_daily_keeps_newest_14_by_date_not_by_write_order(tmp_path):
    data = tmp_path / "data"
    names = _make_days(data, 40)
    removed = retention.prune_dated(data, retention.KEEP_DAILY)
    assert _present(data) == names[-14:]
    assert removed == names[:-14]


def test_pending_keeps_newest_7(tmp_path):
    pending = tmp_path / "pending"
    names = _make_days(pending, 20)
    retention.prune_dated(pending, retention.KEEP_PENDING)
    assert _present(pending) == names[-7:]


def test_fewer_files_than_limit_removes_nothing(tmp_path):
    data = tmp_path / "data"
    names = _make_days(data, 5)
    assert retention.prune_dated(data, 14) == []
    assert _present(data) == names


def test_idempotent(tmp_path):
    data = tmp_path / "data"
    _make_days(data, 30)
    assert retention.prune_dated(data, 14)
    before = _present(data)
    assert retention.prune_dated(data, 14) == []
    assert _present(data) == before


def test_state_files_html_and_bad_names_are_left_alone(tmp_path):
    data = tmp_path / "data"
    names = _make_days(data, 30)
    keepers = ["threads.json", "theme_history.json", "sources_health.json", "sec_ticker_map.json",
               "2026-08-03.classify-debug.json", "2026-13-45.json", "2026-8-3.json", "2026-08-03.json.bak"]
    for name in keepers:
        (data / name).write_text("{}", encoding="utf-8")
    page = tmp_path / "2026-08-03.html"
    page.write_text("<html></html>", encoding="utf-8")
    retention.prune_dated(data, 14)
    for name in keepers:
        assert (data / name).exists(), name
    assert page.exists()
    # 狀態檔與壞檔名不佔名額：合法日期檔仍恰好留最新 14 份
    assert [n for n in _present(data) if n in set(names)] == names[-14:]


def test_protect_keeps_a_backfilled_old_date(tmp_path):
    data = tmp_path / "data"
    names = _make_days(data, 30)
    old = names[0][:-5]  # 補跑最舊那天：剛寫完不能被清掉
    removed = retention.prune_dated(data, 14, protect={old})
    assert names[0] in _present(data)
    assert names[0] not in removed
    assert len(_present(data)) == 14 + 1


def test_missing_directory_is_a_no_op(tmp_path):
    assert retention.prune_dated(tmp_path / "nope", 14) == []
    assert retention.prune_intel(tmp_path / "a", tmp_path / "b") == {"data": [], "pending": []}


def test_prune_intel_applies_each_limit_to_its_own_folder(tmp_path):
    data, pending = tmp_path / "data", tmp_path / "pending"
    d = _make_days(data, 30)
    p = _make_days(pending, 30)
    removed = retention.prune_intel(data, pending, protect={d[-1][:-5]})
    assert _present(data) == d[-14:]
    assert _present(pending) == p[-7:]
    assert len(removed["data"]) == 16 and len(removed["pending"]) == 23
    assert retention.prune_intel(data, pending) == {"data": [], "pending": []}
