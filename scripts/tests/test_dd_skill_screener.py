"""2026-09-11：新 DD skill 的直出頁面必須保持既有篩選器資料介面。"""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ddreport
import render_dd
from dd_meta_reader import read_dd_meta
from dd_screener_dd_loader import load_dd_universe

FIX = Path(__file__).parent / "fixtures"


def test_direct_research_page_preserves_screener_inputs(tmp_path, monkeypatch):
    raw = json.loads((FIX / "judgment_v19_FIX.json").read_text())
    raw["facts_ref"] = str(FIX / "facts_FIX_20260911.json")
    raw["scenario_ref"] = str(tmp_path / "scenario.json")
    # 2026-09-11：fixture 只驗證資料接線，不冒充真實公司的新研究正文。
    quality = raw["answers"]["q4_capital"]["verdict_values"]["quality"]
    quality["financial_note"] = raw["answers"]["q4_capital"]["reasoning"]
    quality["latest_quarter_note"] = raw["answers"]["q3_growth"]["reasoning"]
    for name in ("evidence", "scenario", "scenario_meta"):
        (tmp_path / (name + ".json")).write_bytes((FIX / (name + "_FIX_20260911.json")).read_bytes())
    judgment_path = tmp_path / "judgment.json"
    judgment_path.write_text(json.dumps(raw, ensure_ascii=False))
    monkeypatch.setattr(ddreport, "_run_dir", lambda *a: tmp_path)
    monkeypatch.setattr(ddreport, "_pick_python", lambda: sys.executable)
    assert ddreport._do_prose_prepare("FIX", "20260911") == 0
    page = render_dd.assemble_from_parts_v19(
        tmp_path / "prose", tmp_path / "tables", judgment_path=judgment_path)
    dd_dir = tmp_path / "dd"
    dd_dir.mkdir()
    html_path = dd_dir / "DD_FIX_20260911.html"
    html_path.write_text(page)
    meta = read_dd_meta(html_path)
    rows = load_dd_universe(dd_dir, tmp_path / "dca")
    assert len(rows) == 1, "新報告不得被篩選器略過"
    row = rows[0]
    assert row["ticker"] == raw["meta"]["ticker"] == "FIX"
    assert row["dd_status"] == "dd" and row["brief"] is False
    assert row["dd_date"] == "2026-09-11"
    assert row["dd_path"] == "/dd/DD_FIX_20260911.html"
    assert row["dca_path"] == row["dd_path"] + "#decision"
    assert 'id="decision"' in page
    for key in (
        "moat_score", "moat_trend", "moat_execution", "moat_pricing_power",
        "signal", "trap", "val", "fpe_fy2", "pct_5y", "growth_durability",
        "quality_score", "ai_risk", "price_at_dd", "runway_post_y5",
        "bull_5y_price", "bear_5y_price", "p_bull_pct", "p_bear_pct",
        "upside_mid_pct", "upside_5y_pct", "dca_verdict", "dca_role",
    ):
        assert meta.get(key) is not None, "fixture 須實際覆蓋欄位：" + key
        assert row[key] == meta[key], "篩選器不可遺失或另算 DD 欄位：" + key
    assert row["moat_grade"] == meta["moat"]
    assert row["dca_verdict"] == "觀望" and row["dca_role"] == "追蹤"
    scenario = json.loads((tmp_path / "scenario_meta.json").read_text())
    for key in ("bull_5y_price", "bear_5y_price", "p_bull_pct", "p_bear_pct"):
        assert row[key] == scenario[key]
    assert not (tmp_path / "prompts" / "b2_prose.md").exists()
