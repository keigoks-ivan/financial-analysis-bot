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
import dd_brief  # noqa: E402


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


def test_scenario_metrics_are_identical_across_four_render_entrypoints():
    """2026-09-07：null judgment 不得讓 full dashboard／revlog 漏掉三欄。"""
    judgment = {
        "meta": {"ticker": "ZTEST", "date": "20260907", "schema": "v17"},
        "decision_inputs": {
            "price_at_dd": 100,
            "ev5y_pct": None,
            "irr_base_pct": None,
            "asym_ratio": None,
        },
        "decision_out": {"verdict": "觀望", "role": "追蹤"},
        "appendix_a": {"val": "🟡"},
    }
    scenario_meta = {"ev5y_pct": 6.8, "irr_base_pct": 0.9, "asym_ratio": 1.7}

    meta = gen_dd_tables.build_dd_meta(judgment, scenario_meta)
    dashboard = gen_dd_tables.render_dashboard_html(judgment, scenario_meta)
    revlog = gen_dd_tables.render_revlog_html(judgment, scenario_meta=scenario_meta)
    tiles = dd_brief.render_tiles(judgment, scenario_meta)

    assert [meta[field] for field in ("ev5y_pct", "irr_base_pct", "asym_ratio")] == [
        6.8, 0.9, 1.7,
    ]
    assert "+6.8%／Base +0.9%/yr" in dashboard
    assert "不對稱比率 1.7" in revlog
    assert "5 年機率加權報酬 +6.8%" in revlog
    assert "+6.8%" in tiles
    assert ">0.9<" in tiles
    assert ">1.7<" in tiles


# ---------------------------------------------------------------------------
# WP-G item 6b（2026-09-11）：judgment-rules.md §0.5(二) 給的條件式展開示例是
# `[{"item","value"}]`，但 E3／E8／E10 各自要自己的專屬逐列形狀——TXN
# 2026-09-10 實例：governance.capital_returns 填成 7 筆 {item,value}，
# render_e10_html 原本讀 year/buyback/…/rd 全空，渲出七列全空表。改法：偵測
# 到退化成示例形狀時改渲染兩欄表。
# ---------------------------------------------------------------------------

def test_render_e10_item_value_shape_renders_two_column_table():
    judgment = {
        "governance": {
            "capital_returns": [
                {"item": "十年回饋", "value": "回饋 130% FCF"},
                {"item": "負債", "value": "總債 140 億"},
            ],
        },
    }
    html = gen_dd_tables.render_e10_html(judgment)
    assert "十年回饋" in html and "回饋 130% FCF" in html
    assert "總債 140 億" in html
    assert "<th>項目</th><th>內容</th>" in html


def test_render_e10_normal_shape_unchanged():
    judgment = {
        "governance": {
            "capital_returns": [
                {"year": "2025", "buyback": "6 億", "dividend": "52 億",
                 "capex": "10 億", "rd": "8 億"},
            ],
        },
    }
    html = gen_dd_tables.render_e10_html(judgment)
    # v19（WP-H2-2，2026-09-11）：七表數值欄新增 class="num"（v19.css 的
    # td.num 靠 class 選右對齊，不靠欄序）；本測試名稱「unchanged」指的是
    # shape（正常陣列 vs item/value fallback 兩者不混淆），不是逐字 HTML
    # 不變——header/cell 文字與欄數本身確實沒變，只多了這個屬性。
    assert ('<th>年度</th><th class="num">回購</th><th class="num">股利</th>'
            '<th class="num">資本支出</th><th class="num">研發</th>') in html
    assert '<td>2025</td><td class="num">6 億</td>' in html


def test_render_e3_item_value_shape_renders_two_column_table():
    judgment = {"industry": {"tam_table": [{"item": "展開理由", "value": "估值依賴低滲透"}]}}
    html = gen_dd_tables.render_e3_html(judgment)
    assert "<th>項目</th><th>內容</th>" in html
    assert "展開理由" in html and "估值依賴低滲透" in html


def test_render_e8_item_value_shape_renders_two_column_table():
    judgment = {"growth": {"segments": [{"item": "分部驅動", "value": "量增為主"}]}}
    html = gen_dd_tables.render_e8_html(judgment)
    assert "<th>項目</th><th>內容</th>" in html
    assert "分部驅動" in html and "量增為主" in html


def test_wdc_ev_uses_scenario_meta_even_inside_historical_tolerance():
    """2026-09-07：重現 WDC 7.0／6.8；發布值必須採 scenario 的 6.8。"""
    src = SCRIPTS_DIR.parent / "notes" / "site-internal" / "dd" / "_src" / "WDC_20260906"
    judgment = json.loads(
        (src / "WDC_20260906.judgment.json").read_text(encoding="utf-8"))
    scenario_meta = json.loads(
        (src / "WDC_20260906.scenario_meta.json").read_text(encoding="utf-8"))

    assert judgment["decision_inputs"]["ev5y_pct"] == 7
    assert scenario_meta["ev5y_pct"] == 6.8
    assert gen_dd_tables.build_dd_meta(judgment, scenario_meta)["ev5y_pct"] == 6.8
