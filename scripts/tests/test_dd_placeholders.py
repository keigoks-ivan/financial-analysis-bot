#!/usr/bin/env python3
"""stage0 查詢句佔位符（{COMPANY}/{INDUSTRY}/{CUSTOMERS}/{SEGMENT}）解析與清理。"""
from __future__ import annotations

import sys
import types
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import dd_evidence  # noqa: E402
import ddreport  # noqa: E402

AX = {"id": "x", "name": "n", "question": "{COMPANY} q", "queries": [
    "{TICKER} {COMPANY} share 2026", "{CUSTOMERS} in-house {INDUSTRY} 2026"]}


def _fake_yf(info):
    mod = types.ModuleType("yfinance")
    mod.Ticker = lambda t: types.SimpleNamespace(info=info)
    return mod


def test_values_filled_in_resolve_axes():
    matrix = {"common": [dict(AX)], "by_archetype": {"a": []}}
    ax = dd_evidence.resolve_axes(matrix, "a", None, {
        "TICKER": "CRDO", "COMPANY": "Credo", "INDUSTRY": "Semis", "CUSTOMERS": ""})
    assert ax[0]["queries"][0] == "CRDO Credo share 2026"
    assert ax[0]["queries"][1] == "in-house Semis 2026"


def test_no_leftover_when_no_source():
    matrix = {"common": [dict(AX)], "by_archetype": {"a": []}}
    ax = dd_evidence.resolve_axes(matrix, "a", None, {"TICKER": "ZZ"})
    blob = str(ax)
    assert "{COMPANY}" not in blob and "{INDUSTRY}" not in blob and "{CUSTOMERS}" not in blob


def test_axis_block_scrubs_residual(capsys):
    out = ddreport._axis_block([dict(AX, queries=["ZZ {COMPANY} {SEGMENT}  x"])])
    assert "{" not in out and "ZZ x" in out
    assert "[warn]" in capsys.readouterr().err


def test_fallback_screener_then_yfinance(monkeypatch):
    # prior_meta 無 name → screener 名稱等於 ticker 視為無 → yfinance
    monkeypatch.setitem(sys.modules, "yfinance", _fake_yf(
        {"longName": "Syarikat Takaful Malaysia Keluarga Berhad", "industry": "Insurance"}))
    prior = {"prior_dd": {"prior_meta": {"ticker": "6139.KL"}}}
    v, src = ddreport._resolve_placeholders("6139.KL", prior)
    assert v["COMPANY"] == "Syarikat Takaful Malaysia Keluarga"
    assert v["INDUSTRY"] == "Insurance" and src["COMPANY"] == "yfinance"


def test_prior_meta_name_wins(monkeypatch):
    monkeypatch.setitem(sys.modules, "yfinance", _fake_yf({"longName": "Other Inc."}))
    v, src = ddreport._resolve_placeholders(
        "ZZQ", {"prior_dd": {"prior_meta": {"name": "Acme Corporation"}}})
    assert v["COMPANY"] == "Acme" and src["COMPANY"] == "prior_meta"


def test_yfinance_failure_and_offline_skip(monkeypatch):
    mod = types.ModuleType("yfinance")

    def boom(t):
        raise RuntimeError("net down")
    mod.Ticker = boom
    monkeypatch.setitem(sys.modules, "yfinance", mod)
    v, _ = ddreport._resolve_placeholders("ZZQ9", {})
    assert v["COMPANY"] == ""
    v, _ = ddreport._resolve_placeholders("ZZQ9", {}, offline=True)
    assert v["COMPANY"] == ""
