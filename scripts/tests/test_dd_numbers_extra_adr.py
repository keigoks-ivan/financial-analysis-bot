"""2026-09-12：ADR 換算表在資料層統一（工作單 _dd_simple_workorder_20260912.md 任務 1）。

覆蓋三件事：ADR ticker 換算正確、非 ADR ticker byte-for-byte 不變、eps_basis 註記
只在換算發生時才出現（不污染其餘 ticker 的輸出形狀）。
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import dd_numbers_extra as dne  # noqa: E402
from load_eps_estimates_xlsx import ExcelSnapshot, apply_adr_ratio, load_adr_ratios  # noqa: E402


# ---------------------------------------------------------------------------
# apply_adr_ratio / load_adr_ratios（共用讀取函式）
# ---------------------------------------------------------------------------

def test_apply_adr_ratio_converts_listed_ticker():
    ratios = {"TSM": {"ratio": 5}}
    rec = {"fy1": 3.41, "fy2": 4.51, "fy3": 5.73, "growth_fy1_fy2_pct": 10.0}
    out = apply_adr_ratio("TSM", rec, ratios=ratios)
    assert out["fy1"] == 17.05
    assert out["fy2"] == 22.55
    assert out["fy3"] == 28.65
    # growth/CAGR 是比率，ADR 換算前後不變
    assert out["growth_fy1_fy2_pct"] == 10.0
    assert out["eps_basis"] == "adr-usd (koyfin ordinary ×5)"
    # 原record 不得被就地改動（呼叫端可能還要用原始值）
    assert "eps_basis" not in rec


def test_apply_adr_ratio_leaves_non_adr_ticker_byte_identical():
    ratios = {"TSM": {"ratio": 5}}
    rec = {"fy1": 3.41, "fy2": 4.51, "fy3": 5.73}
    out = apply_adr_ratio("AAPL", rec, ratios=ratios)
    assert out is rec  # 非表列 ticker：原樣回傳同一個物件，零變化
    assert "eps_basis" not in out


def test_apply_adr_ratio_passthrough_for_none_and_empty():
    assert apply_adr_ratio("TSM", None, ratios={"TSM": {"ratio": 5}}) is None
    assert apply_adr_ratio("TSM", {}, ratios={"TSM": {"ratio": 5}}) == {}


def test_load_adr_ratios_missing_file_returns_empty(tmp_path):
    assert load_adr_ratios(tmp_path / "nope.json") == {}


def test_load_adr_ratios_bad_json_returns_empty(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    assert load_adr_ratios(p) == {}


def test_repo_adr_ratios_table_has_verified_tsm_entry():
    ratios = load_adr_ratios()
    assert ratios["TSM"]["ratio"] == 5
    assert ratios["TSM"].get("source")  # 查證來源不得空白


# ---------------------------------------------------------------------------
# compute_consensus_revision（dd_numbers_extra.py 端到端接線）
# ---------------------------------------------------------------------------

def _write_fake_snapshots(tmp_path, dates):
    for d in dates:
        (tmp_path / "DD_universe_EPS_estimates_{0}.xlsx".format(d)).write_bytes(b"")


def test_compute_consensus_revision_converts_adr_ticker(tmp_path, monkeypatch):
    _write_fake_snapshots(tmp_path, ("20260604", "20260904", "20260909"))
    monkeypatch.setattr(dne, "DEFAULT_DATA_DIR", tmp_path)
    snaps = {
        "20260604": ExcelSnapshot(snapshot_date="2026-06-04", source_file="x",
                                   tickers={"TSM": {"fy1": 3.11, "fy2": 3.89, "fy3": 4.89}}),
        "20260904": ExcelSnapshot(snapshot_date="2026-09-04", source_file="x",
                                   tickers={"TSM": {"fy1": 3.39, "fy2": 4.48, "fy3": 5.69}}),
        "20260909": ExcelSnapshot(snapshot_date="2026-09-09", source_file="x",
                                   tickers={"TSM": {"fy1": 3.41, "fy2": 4.51, "fy3": 5.73}}),
    }

    def fake_load_excel(path):
        d = dne.FILENAME_RE.search(path.name).group(1)
        return snaps[d]

    monkeypatch.setattr(dne, "load_excel", fake_load_excel)
    result = dne.compute_consensus_revision("TSM", datetime(2026, 9, 11))

    assert result["latest_snapshot"]["fy1"] == 17.05
    assert result["latest_snapshot"]["fy2"] == 22.55
    assert result["latest_snapshot"]["fy3"] == 28.65
    assert result["eps_basis"] == "adr-usd (koyfin ordinary ×5)"
    # revision% 是比率，換算不影響（3.41/3.39 - 1 == 17.05/16.95 - 1）
    assert result["fy1"]["revision_pct"] == pytest.approx(0.59, abs=0.01)


def test_compute_consensus_revision_non_adr_ticker_unaffected(tmp_path, monkeypatch):
    _write_fake_snapshots(tmp_path, ("20260904", "20260909"))
    monkeypatch.setattr(dne, "DEFAULT_DATA_DIR", tmp_path)
    snaps = {
        "20260904": ExcelSnapshot(snapshot_date="2026-09-04", source_file="x",
                                   tickers={"AAPL": {"fy1": 7.5, "fy2": 8.2, "fy3": 9.0}}),
        "20260909": ExcelSnapshot(snapshot_date="2026-09-09", source_file="x",
                                   tickers={"AAPL": {"fy1": 7.5, "fy2": 8.2, "fy3": 9.0}}),
    }

    def fake_load_excel(path):
        d = dne.FILENAME_RE.search(path.name).group(1)
        return snaps[d]

    monkeypatch.setattr(dne, "load_excel", fake_load_excel)
    result = dne.compute_consensus_revision("AAPL", datetime(2026, 9, 11))

    assert result["latest_snapshot"]["fy1"] == 7.5
    assert "eps_basis" not in result
