#!/usr/bin/env python3
"""測試 `scripts/gen_dd_tables.py::resolve_scenario_meta`（WP7b 第 4 項，
2026-09-05）：v17 per-run 目錄下 `judgment.scenario_ref` 指向 `dd_scenario.py`
的輸入檔 `scenario.json`（無 `bull_5y_price` 結果欄）、旁邊有 `scenario_meta.json`
（六個結果欄）時，`resolve_scenario_meta` 須退回讀 `scenario_meta.json`，讓
`build_dd_meta` 拿到 `bull_5y_price`（AVGO 2026-09-05 真跑查出：漂移檢查誤判
本次=None）。本檔只讀 gen_dd_tables，不改動它；測試資料用 tmp_path 自造最小
JSON，不動 `_src` 與 `.dd_build`。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(SCRIPTS_DIR))
import gen_dd_tables  # noqa: E402


def _write(path: Path, obj: dict):
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def test_resolve_scenario_meta_falls_back_to_sibling_scenario_meta(tmp_path):
    run_dir = tmp_path / "AVGO_20260905"
    run_dir.mkdir()

    scenario_input = {
        # dd_scenario.py 的輸入檔形狀：無結果欄 bull_5y_price
        "base_eps_path": {"FY26": 10.0, "FY27": 11.0},
        "bull_5y_price": None,
    }
    _write(run_dir / "scenario.json", scenario_input)

    scenario_meta = {
        "bull_5y_price": 320.5,
        "bear_5y_price": 180.0,
        "p_bull_pct": 25,
        "p_bear_pct": 20,
        "upside_5y_pct": 60.0,
        "scenario_tree": {"terminal_label": "FY31"},
    }
    _write(run_dir / "scenario_meta.json", scenario_meta)

    judgment_path = run_dir / "judgment.json"
    judgment = {
        "scenario_ref": "scenario.json",
        "meta": {"ticker": "AVGO", "schema": "v16", "date": "20260905"},
        "decision_inputs": {"price_at_dd": 300},
    }
    _write(judgment_path, judgment)

    resolved = gen_dd_tables.resolve_scenario_meta(judgment, judgment_path, None)

    assert resolved is not None
    assert resolved.get("bull_5y_price") == 320.5

    meta = gen_dd_tables.build_dd_meta(judgment, resolved)
    assert meta.get("bull_5y_price") == 320.5
    assert meta.get("bear_5y_price") == 180.0


def test_resolve_scenario_meta_uses_ref_directly_when_it_has_bull_price(tmp_path):
    run_dir = tmp_path / "CIEN_20260905"
    run_dir.mkdir()

    scenario_with_result = {
        "bull_5y_price": 99.0,
        "bear_5y_price": 40.0,
    }
    _write(run_dir / "scenario.json", scenario_with_result)
    # 旁邊也放一份 scenario_meta.json，但因 scenario_ref 本身已有
    # bull_5y_price，不應被改讀去 fallback 檔。
    _write(run_dir / "scenario_meta.json", {"bull_5y_price": 1.0, "bear_5y_price": 1.0})

    judgment_path = run_dir / "judgment.json"
    judgment = {"scenario_ref": "scenario.json"}
    _write(judgment_path, judgment)

    resolved = gen_dd_tables.resolve_scenario_meta(judgment, judgment_path, None)

    assert resolved.get("bull_5y_price") == 99.0


def test_resolve_scenario_meta_no_ref_returns_none(tmp_path):
    judgment_path = tmp_path / "judgment.json"
    judgment = {}
    _write(judgment_path, judgment)

    assert gen_dd_tables.resolve_scenario_meta(judgment, judgment_path, None) is None


def test_resolve_scenario_meta_missing_file_returns_none(tmp_path):
    judgment_path = tmp_path / "judgment.json"
    judgment = {"scenario_ref": "does_not_exist.json"}
    _write(judgment_path, judgment)

    assert gen_dd_tables.resolve_scenario_meta(judgment, judgment_path, None) is None
