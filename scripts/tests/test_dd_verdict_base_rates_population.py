"""p_clim 母體只收主池 dd_status=="dd" 的名字 (build_dd_verdict_base_rates), 2026-10-10.

data/weekly_cache 也收小型股模式寫進來的非 DD 名字，它們不在主池 latest.json 裡，
舊的「排除非 DD」名單擋不到。主池的上櫃股記成 .TW、快取檔是 .TWO，白名單要經過
寫檔端同一個代號轉換才對得到。No network.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_verdict_base_rates as br  # noqa: E402


def _setup(tmp_path, monkeypatch):
    latest = tmp_path / "latest.json"
    latest.write_text(json.dumps({"stocks": [
        {"ticker": "AAPL", "dd_status": "dd"},
        {"ticker": "5274.TW", "dd_status": "dd"},   # TPEx name, cache file is 5274.TWO
        {"ticker": "QGM1", "dd_status": "none"},    # --include-non-dd name
    ]}), encoding="utf-8")
    cache = tmp_path / "weekly_cache"
    cache.mkdir()
    for t in ("AAPL", "5274.TWO", "QGM1", "DAVE"):   # DAVE: smallcap mode, not in main pool
        (cache / f"{t}.json").write_text('{"weekly_bars": []}', encoding="utf-8")
    monkeypatch.setattr(br, "DD_SCREENER_LATEST", latest)
    monkeypatch.setattr(br, "CACHE_DIR", cache)


def test_allow_set_maps_tpex_names_to_cache_file_names(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert br._load_dd_allow_set() == {"AAPL", "5274.TWO"}


def test_names_outside_the_main_pool_are_not_scanned(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    _, _, n_files, n_excluded = br.compute_p_clim([], [], "2026-10-10")
    assert (n_files, n_excluded) == (2, 2)   # AAPL + 5274.TWO kept; QGM1 and DAVE dropped


def test_missing_latest_falls_back_to_all_files(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    monkeypatch.setattr(br, "DD_SCREENER_LATEST", tmp_path / "nope.json")
    _, _, n_files, n_excluded = br.compute_p_clim([], [], "2026-10-10")
    assert (n_files, n_excluded) == (4, 0)
