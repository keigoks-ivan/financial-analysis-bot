#!/usr/bin/env python3
"""測試 P2-1／P2-2 兩項機械層修法（2026-09-07，複審報告
notes/site-internal/dd/_review_v17_pipeline_20260907.md）：

- P2-1（`scripts/validate_judgment.py::same_source_pair_checks`）：
  judgment-to-ddmeta.md 宣告「同源」的欄位 pair（如
  `decision_inputs.signal` ＝ `appendix_a.signal`）若兩側都有值卻不同，
  FAIL；任一側缺值不比；`fpe_fy2`／`peg_fy2` 財年口徑未定義，明確不在
  pair 清單內。

- P2-2（`scripts/dd_delta.py`）：`cmd_generate` 的 `prior_meta_diff.prior_meta`
  改走 `dd_metric_resolver.resolve_scenario_metrics()`，scenario_meta
  sidecar 有值時一律優先於（可能陳舊的）judgment 原值；`cmd_check` 的
  `missing_prior_field` 迴圈不再對 bull_5y_price／bear_5y_price／
  p_bull_pct／p_bear_pct 四個 scenario-only 欄整個略過。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent
NOTES_SRC = ROOT / "notes" / "site-internal" / "dd" / "_src"

sys.path.insert(0, str(SCRIPTS_DIR))
import validate_judgment as vj  # noqa: E402
import dd_delta  # noqa: E402


def _write_json(path: Path, obj: dict) -> Path:
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# P2-1: same_source_pair_checks 單元測試
# ---------------------------------------------------------------------------

def test_pair_mismatch_is_fail():
    data = {"decision_inputs": {"signal": "A"}, "appendix_a": {"signal": "B"}}
    fails = vj.same_source_pair_checks(data)
    assert any("signal" in f for f in fails)


def test_pair_match_is_clean():
    data = {"decision_inputs": {"signal": "A"}, "appendix_a": {"signal": "A"}}
    assert vj.same_source_pair_checks(data) == []


def test_pair_one_side_missing_is_not_checked():
    """schema 允許 null；只有兩側都有值才比，缺值不是「不一致」。"""
    data = {"decision_inputs": {"signal": None}, "appendix_a": {"signal": "A"}}
    assert vj.same_source_pair_checks(data) == []


def test_pair_both_sides_missing_is_not_checked():
    data = {"decision_inputs": {}, "appendix_a": {}}
    assert vj.same_source_pair_checks(data) == []


def test_pair_numeric_mismatch_is_fail():
    data = {"appendix_a": {"pct_5y": 40.0}, "valuation": {"percentile_5y": 55.0}}
    fails = vj.same_source_pair_checks(data)
    assert any("pct_5y" in f for f in fails)


def test_pair_numeric_match_is_clean():
    data = {"appendix_a": {"pct_5y": 40.0}, "valuation": {"percentile_5y": 40.0}}
    assert vj.same_source_pair_checks(data) == []


def test_pair_moat_score_and_capalloc_grade():
    """抽查兩組容易寫錯路徑方向的 pair（moat.score 是權威側、governance 是
    capalloc_grade 的權威側，與 decision_inputs 互為同源）。"""
    ok = {
        "moat": {"score": 8},
        "appendix_a": {"moat_score": 8},
        "governance": {"capalloc_grade": "A"},
        "decision_inputs": {"capalloc_grade": "A"},
    }
    assert vj.same_source_pair_checks(ok) == []

    bad = {
        "moat": {"score": 8},
        "appendix_a": {"moat_score": 7},
        "governance": {"capalloc_grade": "A"},
        "decision_inputs": {"capalloc_grade": "B"},
    }
    fails = vj.same_source_pair_checks(bad)
    assert len(fails) == 2
    assert any("moat_score" in f for f in fails)
    assert any("capalloc_grade" in f for f in fails)


def test_fpe_fy2_and_peg_fy2_not_in_pair_list():
    """明確不加 equality——appendix_a 側與 valuation 側可能是不同財年
    （AVGO 實測 FY26 vs FY27），口徑待定義前不得視為同義。"""
    data = {
        "appendix_a": {"fpe_fy2": 30.77, "peg_fy2": 0.51},
        "valuation": {"fwd_pe": 18.51, "peg": 0.31},
    }
    assert vj.same_source_pair_checks(data) == []
    pair_names = {name for name, _, _ in vj.SAME_SOURCE_PAIRS}
    assert "fpe_fy2" not in pair_names
    assert "peg_fy2" not in pair_names


def test_pair_check_wired_into_validate_file(tmp_path):
    """不是只加了函式沒接線——validate_file() 的總 fails 要含 pair_fails。"""
    source = NOTES_SRC / "BE_20260905" / "BE_20260905.judgment.json"
    if not source.exists():
        pytest.skip(f"fixture 不存在：{source}")
    data = json.loads(source.read_text(encoding="utf-8"))
    original = data.get("decision_inputs", {}).get("signal")
    mismatched = "X" if original != "X" else "A+"
    data.setdefault("decision_inputs", {})["signal"] = mismatched
    path = tmp_path / "judgment.json"
    _write_json(path, data)

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert any("同源欄位不一致" in f and "signal" in f for f in fails)


# ---------------------------------------------------------------------------
# P2-1 迴歸：全部既有存查 judgment 掃過 same_source_pair_checks，0 mismatch
# ---------------------------------------------------------------------------

def _all_src_judgment_files():
    if not NOTES_SRC.is_dir():
        return []
    return sorted(NOTES_SRC.glob("*/*.judgment.json"))


def test_same_source_pairs_zero_mismatch_across_all_src():
    files = _all_src_judgment_files()
    if not files:
        pytest.skip(f"沒有找到任何存查 judgment：{NOTES_SRC}")
    all_mismatches = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        fails = vj.same_source_pair_checks(data)
        if fails:
            all_mismatches.append((path.name, fails))
    assert all_mismatches == [], (
        f"{len(all_mismatches)}/{len(files)} 份存查出現同源欄位不一致：{all_mismatches}"
    )


# ---------------------------------------------------------------------------
# P2-2: _sibling_scenario_meta sidecar 解析
# ---------------------------------------------------------------------------

def test_sibling_scenario_meta_finds_archive_suffix_sidecar(tmp_path):
    jpath = _write_json(tmp_path / "ZZZ_20260101.judgment.json", {})
    sidecar = _write_json(tmp_path / "ZZZ_20260101.scenario_meta.json", {})
    assert dd_delta._sibling_scenario_meta(jpath) == sidecar


def test_sibling_scenario_meta_finds_run_dir_convention(tmp_path):
    jpath = _write_json(tmp_path / "judgment.json", {})
    sidecar = _write_json(tmp_path / "scenario_meta.json", {})
    assert dd_delta._sibling_scenario_meta(jpath) == sidecar


def test_sibling_scenario_meta_returns_none_when_missing(tmp_path):
    jpath = _write_json(tmp_path / "ZZZ_20260101.judgment.json", {})
    assert dd_delta._sibling_scenario_meta(jpath) is None


# ---------------------------------------------------------------------------
# P2-2: cmd_generate 的 prior_meta 改走 resolve_scenario_metrics
# ---------------------------------------------------------------------------

def _make_prior_dir(tmp_path, ticker="ZZZ", date="20260101"):
    d = tmp_path / f"{ticker}_{date}"
    d.mkdir()
    judgment = {
        "meta": {"ticker": ticker, "schema": "v17.0", "date": date},
        "decision_inputs": {
            "ev5y_pct": 999.0, "irr_base_pct": 999.0, "asym_ratio": 999.0,
            "price_at_dd": 10,
        },
        "contradictions": [],
    }
    _write_json(d / f"{ticker}_{date}.judgment.json", judgment)
    _write_json(d / f"{ticker}_{date}.evidence.json", {"numbers": {}, "coverage": {}, "events": {}})
    _write_json(d / f"{ticker}_{date}.scenario_meta.json", {
        "ev5y_pct": 50.0, "irr_base_pct": 10.0, "asym_ratio": 2.0,
        "bull_5y_price": 100, "bear_5y_price": 40, "p_bull_pct": 30, "p_bear_pct": 25,
    })
    return d


def test_cmd_generate_prior_meta_prefers_scenario_over_stale_judgment(tmp_path):
    """WDC 20260906 真實案例的縮影：judgment.decision_inputs 留著舊判斷值
    （此處故意設 999 模擬陳舊值），scenario_meta sidecar 才是發布權威值。"""
    prior_dir = _make_prior_dir(tmp_path)
    new_evidence = _write_json(tmp_path / "new_evidence.json", {"numbers": {}, "coverage": {}, "events": {}})
    out_path = tmp_path / "delta.json"

    rc = dd_delta.cmd_generate([
        "ZZZ", "20260107",
        "--prior", str(prior_dir),
        "--evidence", str(new_evidence),
        "--out", str(out_path),
    ])
    assert rc == 0

    prior_meta = json.loads(out_path.read_text(encoding="utf-8"))["prior_meta_diff"]["prior_meta"]
    assert prior_meta["ev5y_pct"] == 50.0
    assert prior_meta["irr_base_pct"] == 10.0
    assert prior_meta["asym_ratio"] == 2.0
    # 這四欄過去在 dict comprehension 的 `if p` 過濾下整個不存在於 prior_meta。
    assert prior_meta["bull_5y_price"] == 100
    assert prior_meta["bear_5y_price"] == 40
    assert prior_meta["p_bull_pct"] == 30
    assert prior_meta["p_bear_pct"] == 25


def test_cmd_generate_prior_meta_falls_back_to_judgment_without_sidecar(tmp_path):
    """沒有 scenario_meta sidecar 時退回 judgment 原值（已知範圍缺口，非
    新猜測）——不是新迴歸，行為與修法前的『沒有 scenario 就用 judgment』
    一致，只是現在三欄與四欄都走同一條路徑決定要不要 fallback。"""
    d = tmp_path / "ZZZ_20260101"
    d.mkdir()
    judgment = {
        "meta": {"ticker": "ZZZ", "schema": "v17.0", "date": "20260101"},
        "decision_inputs": {"ev5y_pct": 12.3, "irr_base_pct": 4.5, "asym_ratio": 1.1, "price_at_dd": 10},
        "contradictions": [],
    }
    _write_json(d / "ZZZ_20260101.judgment.json", judgment)
    _write_json(d / "ZZZ_20260101.evidence.json", {"numbers": {}, "coverage": {}, "events": {}})
    new_evidence = _write_json(tmp_path / "new_evidence.json", {"numbers": {}, "coverage": {}, "events": {}})
    out_path = tmp_path / "delta.json"

    rc = dd_delta.cmd_generate([
        "ZZZ", "20260107", "--prior", str(d), "--evidence", str(new_evidence), "--out", str(out_path),
    ])
    assert rc == 0
    prior_meta = json.loads(out_path.read_text(encoding="utf-8"))["prior_meta_diff"]["prior_meta"]
    assert prior_meta["ev5y_pct"] == 12.3
    assert prior_meta["irr_base_pct"] == 4.5
    assert prior_meta["asym_ratio"] == 1.1
    assert prior_meta["bull_5y_price"] is None
    assert prior_meta["bear_5y_price"] is None
    assert prior_meta["p_bull_pct"] is None
    assert prior_meta["p_bear_pct"] is None


# ---------------------------------------------------------------------------
# P2-2: cmd_check 不再對 scenario-only 四欄整個略過
# ---------------------------------------------------------------------------

def test_cmd_check_flags_unattributed_scenario_only_drift(tmp_path, capsys):
    prior_jpath = _write_json(tmp_path / "prior.judgment.json", {
        "meta": {"ticker": "ZZZ"}, "decision_inputs": {}, "contradictions": [],
    })
    current_jpath = _write_json(tmp_path / "current.judgment.json", {
        "meta": {"ticker": "ZZZ"}, "decision_inputs": {}, "contradictions": [],
    })
    _write_json(tmp_path / "prior.scenario_meta.json", {"bull_5y_price": 100})
    _write_json(tmp_path / "current.scenario_meta.json", {"bull_5y_price": 150})
    delta_path = _write_json(tmp_path / "delta.json", {"judgment_fields_to_review": []})

    rc = dd_delta.cmd_check([
        str(delta_path), "--judgment", str(current_jpath), "--prior-judgment", str(prior_jpath),
    ])
    out = capsys.readouterr().out

    assert rc == 1
    assert "bull_5y_price" in out


def test_cmd_check_passes_when_scenario_only_drift_attributed(tmp_path):
    prior_jpath = _write_json(tmp_path / "prior.judgment.json", {
        "meta": {"ticker": "ZZZ"}, "decision_inputs": {}, "contradictions": [],
    })
    current_jpath = _write_json(tmp_path / "current.judgment.json", {
        "meta": {"ticker": "ZZZ"}, "decision_inputs": {},
        "contradictions": [{"prior_field": "bull_5y_price", "axis": "Bull 5Y 上修"}],
    })
    scenario_common = {
        "ev5y_pct": 50.0, "irr_base_pct": 10.0, "asym_ratio": 2.0,
        "bear_5y_price": 40, "p_bull_pct": 30, "p_bear_pct": 25,
    }
    _write_json(tmp_path / "prior.scenario_meta.json", dict(scenario_common, bull_5y_price=100))
    _write_json(tmp_path / "current.scenario_meta.json", dict(scenario_common, bull_5y_price=150))
    delta_path = _write_json(tmp_path / "delta.json", {"judgment_fields_to_review": ["contradictions"]})

    rc = dd_delta.cmd_check([
        str(delta_path), "--judgment", str(current_jpath), "--prior-judgment", str(prior_jpath),
    ])
    assert rc == 0


def test_cmd_check_accepts_explicit_scenario_meta_override(tmp_path):
    """--scenario-meta／--prior-scenario-meta 明講路徑時優先於 sidecar 自動
    探索（檔名不必符合任何慣例）。"""
    prior_jpath = _write_json(tmp_path / "p.judgment.json", {
        "meta": {"ticker": "ZZZ"}, "decision_inputs": {}, "contradictions": [],
    })
    current_jpath = _write_json(tmp_path / "c.judgment.json", {
        "meta": {"ticker": "ZZZ"}, "decision_inputs": {},
        "contradictions": [{"prior_field": "bull_5y_price", "axis": "Bull 5Y 上修"}],
    })
    prior_sm = _write_json(tmp_path / "prior_meta_anywhere.json", {"bull_5y_price": 100})
    current_sm = _write_json(tmp_path / "current_meta_anywhere.json", {"bull_5y_price": 150})
    delta_path = _write_json(tmp_path / "delta.json", {"judgment_fields_to_review": ["contradictions"]})

    rc = dd_delta.cmd_check([
        str(delta_path),
        "--judgment", str(current_jpath), "--prior-judgment", str(prior_jpath),
        "--scenario-meta", str(current_sm), "--prior-scenario-meta", str(prior_sm),
    ])
    assert rc == 0
