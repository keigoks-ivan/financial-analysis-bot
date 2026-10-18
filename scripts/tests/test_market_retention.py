#!/usr/bin/env python3
"""2026-10-19：市況 releases／snapshots 的保留規則測試。

規則：releases 只留最近 30 份；snapshots 留最近 30 份、被引用的版本，加上稀疏錨點，
讓 7／30／90／365 天期間比較仍找得到起點。
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
import market_refresh as refresh  # noqa: E402

START = datetime(2026, 1, 1, 8, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def isolated_source_history(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh, "SOURCE_DIR", tmp_path / "sources" / "series")


def _hash_name(prefix, index):
    # 檔名是內容雜湊，與時間順序無關；刻意讓檔名順序和時間順序相反，確認排序看內容裡的時間。
    return (prefix + "{:04d}".format(9999 - index)).ljust(64, "a")


def _put_release(data_dir, index, generated_at):
    name = _hash_name("r", index)
    refresh.atomic_json(Path(data_dir) / "releases" / (name + ".json"),
                        {"snapshot_id": name, "refresh": {"generated_at": generated_at.isoformat()}})
    return name


def _put_snapshot(data_dir, index, as_of, captured_at):
    name = _hash_name("s", index)
    refresh.atomic_json(Path(data_dir) / "snapshots" / (name + ".json"), {
        "snapshot_id": name, "captured_at": captured_at.isoformat(),
        "state": {"as_of": as_of.isoformat(), "evidence": {"quotes": {}}}, "intel": {}})
    return name


def _names(data_dir, kind):
    return {p.stem for p in Path(data_dir, kind).glob("*.json")}


def test_releases_keep_newest_30_by_generated_time_not_by_filename(tmp_path):
    data_dir = tmp_path / "data"
    made = [_put_release(data_dir, i, START + timedelta(hours=i)) for i in range(45)]
    removed = refresh.prune_history(data_dir)
    assert _names(data_dir, "releases") == set(made[-30:])
    assert len(removed["releases"]) == 15
    assert refresh.prune_history(data_dir) == {"releases": [], "snapshots": []}


def test_current_release_bundle_is_never_removed_even_when_old(tmp_path):
    data_dir = tmp_path / "data"
    made = [_put_release(data_dir, i, START + timedelta(hours=i)) for i in range(40)]
    refresh.atomic_json(data_dir / "refresh.json", {"bundle": "releases/" + made[0] + ".json"})
    refresh.prune_history(data_dir)
    assert made[0] in _names(data_dir, "releases")
    assert len(_names(data_dir, "releases")) == 31


def test_unreadable_files_and_other_files_are_left_alone(tmp_path):
    data_dir = tmp_path / "data"
    for i in range(35):
        _put_release(data_dir, i, START + timedelta(hours=i))
        _put_snapshot(data_dir, i, date(2026, 1, 1) + timedelta(days=i), START + timedelta(hours=i))
    (data_dir / "releases" / "broken.json").write_text("{not json", encoding="utf-8")
    (data_dir / "snapshots" / "no_date.json").write_text(json.dumps({"snapshot_id": "x"}), encoding="utf-8")
    (data_dir / "releases" / "notes.txt").write_text("keep", encoding="utf-8")
    refresh.prune_history(data_dir)
    assert (data_dir / "releases" / "broken.json").exists()
    assert (data_dir / "snapshots" / "no_date.json").exists()
    assert (data_dir / "releases" / "notes.txt").exists()


def test_snapshots_keep_recent_30_and_pinned_references(tmp_path):
    data_dir = tmp_path / "data"
    made = [_put_snapshot(data_dir, i, date(2026, 6, 1), START + timedelta(hours=i)) for i in range(50)]
    # 三個引用來源各指一份很舊的版本：目前發布包、上次判讀、問題板錨點
    refresh.atomic_json(data_dir / "refresh.json", {"snapshot_id": made[0]})
    refresh.atomic_json(data_dir / "read.json", {"snapshot_id": made[1]})
    refresh.atomic_json(data_dir / "questions.json", {"snapshot_id": made[2]})
    refresh.prune_history(data_dir, anchor_max_days=-1)  # 關掉錨點，只看最近份數與引用
    assert _names(data_dir, "snapshots") == set(made[-30:]) | set(made[:3])


def test_old_snapshots_are_thinned_but_every_lookback_still_has_a_baseline(tmp_path):
    data_dir = tmp_path / "data"
    first = date(2025, 9, 1)
    days = [first + timedelta(days=i) for i in range(420) if (first + timedelta(days=i)).weekday() != 6]
    index = 0
    for day in days:
        for slot in range(4):  # 每天多份，和正式資料一樣
            _put_snapshot(data_dir, index, day, datetime.combine(day, datetime.min.time(), timezone.utc) + timedelta(hours=slot))
            index += 1
    assert index > 1000
    refresh.prune_history(data_dir)

    kept = sorted(data_dir.joinpath("snapshots").glob("*.json"))
    assert len(kept) < 100  # 稀疏錨點約 53 份加最近 30 份
    history = [json.loads(p.read_text(encoding="utf-8")) for p in kept]
    current = max(history, key=lambda r: (r["state"]["as_of"], r["captured_at"]))
    periods = refresh.period_comparisons(current, history)
    assert [(p["days"], p["status"]) for p in periods] == [(7, "ok"), (30, "ok"), (90, "ok"), (365, "ok")]
    # 回看範圍之外的版本全部清掉
    oldest = min(date.fromisoformat(r["state"]["as_of"]) for r in history)
    assert (max(days) - oldest).days <= refresh.SNAPSHOT_ANCHOR_MAX_DAYS
    # 冪等：再跑一次不再刪
    assert refresh.prune_history(data_dir)["snapshots"] == []


def test_anchor_picks_latest_capture_of_the_day_and_respects_gap(tmp_path):
    data_dir = tmp_path / "data"
    names = {}
    for offset in range(0, 20):
        day = date(2026, 3, 1) + timedelta(days=offset)
        for slot in range(2):
            names[(offset, slot)] = _put_snapshot(
                data_dir, offset * 2 + slot, day, datetime.combine(day, datetime.min.time(), timezone.utc) + timedelta(hours=slot))
    # 最近 2 份留下，其餘（offset 0..18）依錨點間距 6 天由舊到新挑：第 0、6、12、18 天，每天取較晚的一份
    refresh.prune_history(data_dir, keep_snapshots=2)
    expected = {names[(0, 1)], names[(6, 1)], names[(12, 1)], names[(18, 1)], names[(19, 0)], names[(19, 1)]}
    assert _names(data_dir, "snapshots") == expected


def _real_snapshot(as_of, value):
    state = {"schema": "market-state-v1", "as_of": as_of, "evidence": {"quotes": {"monitor:sp500": {
        "label": "S&P 500", "num": value, "as_of": as_of}}}}
    return refresh.make_snapshot(state, {})


def test_locked_publish_prunes_after_publishing(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh, "KEEP_RELEASES", 2)
    monkeypatch.setattr(refresh, "KEEP_SNAPSHOTS", 2)
    data_dir = tmp_path / "data"
    for i in range(5):
        _put_release(data_dir, i, START + timedelta(hours=i))
        old = _real_snapshot("2026-01-01", 100.0 + i)  # 內容雜湊要真實，history_rows 會驗證
        refresh.atomic_json(data_dir / "snapshots" / (old["snapshot_id"] + ".json"),
                            {**old, "captured_at": (START + timedelta(hours=i)).isoformat()})
    snapshot = _real_snapshot("2026-01-02", 200.0)
    refresh.locked_publish(data_dir, snapshot, {}, [], (START + timedelta(days=1)).isoformat(),
                           [], [], False, refresh.digest({}))
    # 新發布的一份必在；其餘依 KEEP_* 清掉
    assert len(_names(data_dir, "releases")) == 2
    refreshed = json.loads((data_dir / "refresh.json").read_text(encoding="utf-8"))
    assert Path(refreshed["bundle"]).stem in _names(data_dir, "releases")
    assert snapshot["snapshot_id"] in _names(data_dir, "snapshots")
    # 最近 2 份（含新的一份）加 2026-01-01 當天最晚保存的一份當錨點
    assert len(_names(data_dir, "snapshots")) == 3
