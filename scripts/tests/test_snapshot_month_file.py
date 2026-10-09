"""Monthly EPS snapshot never overwrites a month file holding another date (2026-10-10).

The month file {YYYY-MM}.json is the only baseline the earnings-anchored
revision reads; a later export in the same month goes to {YYYY-MM-DD}.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import snapshot_eps_estimates as snap  # noqa: E402


@pytest.fixture
def out(tmp_path, monkeypatch):
    monkeypatch.setattr(snap, 'OUTPUT_DIR', tmp_path)
    return tmp_path


def _month_file(out, snapshot_date):
    (out / '2026-10.json').write_text(json.dumps({'snapshot_date': snapshot_date}), encoding='utf-8')


def test_first_export_of_the_month_takes_the_month_file(out):
    assert snap._output_path('2026-10', '2026-10-09') == out / '2026-10.json'


def test_rerun_of_the_same_export_overwrites(out):
    _month_file(out, '2026-10-09')
    assert snap._output_path('2026-10', '2026-10-09') == out / '2026-10.json'


def test_later_export_keeps_the_month_file_and_writes_a_dated_one(out):
    _month_file(out, '2026-10-09')
    assert snap._output_path('2026-10', '2026-10-28') == out / '2026-10-28.json'


def test_earlier_export_never_replaces_the_month_file_either(out):
    _month_file(out, '2026-10-28')
    assert snap._output_path('2026-10', '2026-10-09') == out / '2026-10-09.json'


def test_annotated_snapshot_date_compares_on_the_date_only(out):
    _month_file(out, '2026-05-26 (incremental updates over 2026-05-25 base)')
    assert snap._output_path('2026-10', '2026-05-26') == out / '2026-10.json'


def test_unreadable_month_file_is_overwritten(out):
    (out / '2026-10.json').write_text('{not json', encoding='utf-8')
    assert snap._output_path('2026-10', '2026-10-28') == out / '2026-10.json'
