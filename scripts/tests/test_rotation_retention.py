#!/usr/bin/env python3
"""2026-10-19：輪動雷達每日快照（docs/rotation/data/snapshots）的保留規則測試。

規則：最近 14 份全留；更舊的每 28 天留一份稀疏錨點，只回看 372 天；只認 YYYY-MM-DD.json。
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
import build_rotation_radar as radar  # noqa: E402


def _trading_days(first, count):
    days, d = [], first
    while len(days) < count:
        if d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)
    return days


def _put(directory, days):
    directory.mkdir(parents=True, exist_ok=True)
    for d in days:
        (directory / (d.isoformat() + ".json")).write_text("{}", encoding="utf-8")


def _kept(directory):
    return sorted(date.fromisoformat(p.stem) for p in directory.glob("????-??-??.json"))


def test_defaults_match_documented_rule():
    assert (radar.SNAP_KEEP_RECENT, radar.SNAP_ANCHOR_GAP_DAYS, radar.SNAP_ANCHOR_MAX_DAYS) == (14, 28, 372)


def test_short_history_is_untouched(tmp_path):
    snaps = tmp_path / "snapshots"
    days = _trading_days(date(2026, 9, 1), 14)
    _put(snaps, days)
    assert radar.prune_snapshots(snaps) == []
    assert _kept(snaps) == days


def test_recent_14_all_kept_and_older_thinned_to_anchors(tmp_path):
    snaps = tmp_path / "snapshots"
    days = _trading_days(date(2026, 7, 9), 64)  # 與 2026-10-19 當天網站上的份數相同
    _put(snaps, days)
    removed = radar.prune_snapshots(snaps)
    kept = _kept(snaps)
    assert kept[-14:] == days[-14:]
    older = [d for d in kept if d not in set(days[-14:])]
    assert all((b - a).days >= 28 for a, b in zip(older, older[1:]))
    assert older[0] == days[0]  # 最舊那份作為第一個錨點
    assert len(removed) + len(kept) == 64
    assert len(kept) < 24


def test_lookback_limit_drops_anything_older_than_372_days(tmp_path):
    snaps = tmp_path / "snapshots"
    days = _trading_days(date(2025, 6, 2), 340)
    _put(snaps, days)
    radar.prune_snapshots(snaps)
    kept = _kept(snaps)
    newest = days[-1]
    assert all((newest - d).days <= 372 for d in kept)
    assert kept[-14:] == days[-14:]


def test_idempotent_and_steady_state_is_bounded(tmp_path):
    snaps = tmp_path / "snapshots"
    days = _trading_days(date(2025, 6, 2), 700)
    sizes = []
    for i, d in enumerate(days):  # 每天寫一份再清，模擬每日 CI
        _put(snaps, [d])
        radar.prune_snapshots(snaps)
        if i > 420:
            sizes.append(len(_kept(snaps)))
    assert max(sizes) <= 14 + 14 + 1  # 最近 14 份加約每月一份的錨點，不會隨時間增加
    before = _kept(snaps)
    assert radar.prune_snapshots(snaps) == []
    assert _kept(snaps) == before


def test_other_files_and_bad_names_are_left_alone(tmp_path):
    snaps = tmp_path / "snapshots"
    days = _trading_days(date(2026, 1, 5), 120)
    _put(snaps, days)
    extras = ["notes.txt", "2026-13-40.json", "2026-1-5.json", "latest.json", "2026-01-05.json.bak"]
    for name in extras:
        (snaps / name).write_text("x", encoding="utf-8")
    radar.prune_snapshots(snaps)
    for name in extras:
        assert (snaps / name).exists(), name


def test_missing_or_empty_directory_is_a_no_op(tmp_path):
    assert radar.prune_snapshots(tmp_path / "nope") == []
    (tmp_path / "empty").mkdir()
    assert radar.prune_snapshots(tmp_path / "empty") == []
