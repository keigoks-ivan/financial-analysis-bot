"""Tests for scripts/koyfin_refresh_all.py — the Koyfin monthly-refresh
orchestrator (2026-09-18 automation of
.claude/skills/refresh-eps-screener-web/SKILL.md, see
notes/site-internal/root/_koyfin_refresh_automation_20260918.md).

No network, no browser (per task brief — the browser scrape itself cannot be
exercised without a logged-in Koyfin session; see scripts/koyfin_scrape.py's
module docstring for what's untested there). Covers:
  1. djb2 fingerprint recompute matches the known 2026-09-18 largecap raw
     file (rows=160, bytes=66677, djb2=3646933340 — given fact in the task
     brief, independently re-verified by hand before writing this test).
  2. Missing raw file -> a clear, informative error (not a bare KeyError/
     FileNotFoundError with no context).
  3. Family -> URL/xlsx-family/universe-note mapping (scripts/koyfin_families.py).
  4. Step 5 anomaly-gate mechanics on synthetic before/after snapshots — one
     passing case, one tripping case (both a >=35% move and a sign flip).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import koyfin_refresh_all as kra  # noqa: E402
from koyfin_families import FAMILIES, FAMILY_ORDER  # noqa: E402
from load_eps_estimates_xlsx import ExcelSnapshot  # noqa: E402

ROOT = SCRIPTS_DIR.parent
KNOWN_LARGECAP_RAW = ROOT / "data" / "eps-estimates" / "raw" / "koyfin_largecap_raw_20260918.txt"


# ---------------------------------------------------------------------------
# 1. Fingerprint recompute
# ---------------------------------------------------------------------------

def test_fingerprint_matches_known_largecap_run():
    assert KNOWN_LARGECAP_RAW.exists(), f"fixture raw file missing: {KNOWN_LARGECAP_RAW}"
    fp = kra.compute_fingerprint(KNOWN_LARGECAP_RAW)
    assert fp == {"rows": 160, "bytes": 66677, "djb2": 3646933340}


def test_verify_fingerprint_no_sidecar_is_soft(tmp_path):
    # No .fingerprint.json sidecar exists for the pre-automation largecap raw
    # file — verify_fingerprint() must still succeed (recompute-only), not
    # raise, and say so in verified_against.
    data_dir = ROOT / "data" / "eps-estimates"
    fp = kra.verify_fingerprint(KNOWN_LARGECAP_RAW, "largecap", "20260918", data_dir)
    assert fp["djb2"] == 3646933340
    assert fp["verified_against"].startswith("none")


def test_verify_fingerprint_sidecar_mismatch_raises(tmp_path):
    import json

    # verify_fingerprint() expects data_dir/raw/<raw file>.txt and
    # data_dir/raw/<...>.fingerprint.json side by side — build that shape.
    fake_data_dir = tmp_path / "fakeroot"
    (fake_data_dir / "raw").mkdir(parents=True)
    raw2 = fake_data_dir / "raw" / "koyfin_largecap_raw_20990101.txt"
    raw2.write_text("AAPL|1.0|2.0", encoding="utf-8")
    (fake_data_dir / "raw" / "koyfin_largecap_raw_20990101.fingerprint.json").write_text(
        json.dumps({"rows": 999, "bytes": 999, "djb2": 999}), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        kra.verify_fingerprint(raw2, "largecap", "20990101", fake_data_dir)


# ---------------------------------------------------------------------------
# 2. Missing raw -> clear error
# ---------------------------------------------------------------------------

def test_missing_raw_file_raises_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError) as exc_info:
        kra.find_raw_file(tmp_path, "largecap", "20990101")
    msg = str(exc_info.value)
    assert "largecap" in msg
    assert "20990101" in msg
    assert "--scrape" in msg  # tells the operator what to do next


def test_find_raw_file_success():
    p = kra.find_raw_file(ROOT / "data" / "eps-estimates", "largecap", "20260918")
    assert p == KNOWN_LARGECAP_RAW


# ---------------------------------------------------------------------------
# 3. Family -> URL/xlsx-family/note mapping
# ---------------------------------------------------------------------------

def test_family_order_and_keys():
    assert FAMILY_ORDER == ["screener", "smallcap", "largecap"]
    assert set(FAMILIES.keys()) == set(FAMILY_ORDER)


def test_family_mapping_values():
    assert FAMILIES["screener"]["url"] == "https://app.koyfin.com/myw/3f1528f1-c3fb-452d-975a-57dbc269e716"
    assert FAMILIES["screener"]["xlsx_family"] == "DD_universe_EPS_estimates_"
    assert FAMILIES["screener"]["watchlist_tab"] == "dd_screener"
    assert FAMILIES["screener"]["universe_note"] is None

    assert FAMILIES["smallcap"]["url"] == "https://app.koyfin.com/myw/4b480dbd-996d-4c8e-b47f-2d3ebf1b6ae9"
    assert FAMILIES["smallcap"]["xlsx_family"] == "DD_smallcap_EPS_estimates_"
    assert FAMILIES["smallcap"]["watchlist_tab"] == "dd_smallcap"
    assert "dd_smallcap_v5" in FAMILIES["smallcap"]["universe_note"]

    assert FAMILIES["largecap"]["url"] == "https://app.koyfin.com/myw/0270b5a3-a66d-4e38-9b33-78916ca2bc53"
    assert FAMILIES["largecap"]["xlsx_family"] == "DD_largecap_EPS_estimates_"
    assert FAMILIES["largecap"]["watchlist_tab"] == "dd_largecap"
    assert "dd_largecap_v5" in FAMILIES["largecap"]["universe_note"]


def test_raw_txt_name_matches_existing_convention():
    from koyfin_families import raw_txt_name
    assert raw_txt_name("largecap", "20260918") == "koyfin_largecap_raw_20260918.txt"
    assert raw_txt_name("smallcap", "20260917") == "koyfin_smallcap_raw_20260917.txt"


# ---------------------------------------------------------------------------
# 4. Step 5 anomaly gate — synthetic before/after
# ---------------------------------------------------------------------------

def _snap(tickers: dict) -> ExcelSnapshot:
    return ExcelSnapshot(snapshot_date="2026-08-01", source_file="fake.xlsx", tickers=tickers)


def test_anomaly_gate_no_previous_snapshot_skips():
    gate = kra.run_anomaly_gate({"AAPL": 9.0}, None)
    assert gate["skipped_no_prev"] is True
    assert gate["flagged"] == []


def test_anomaly_gate_passing_case():
    prev = _snap({"AAPL": {"fy1": 8.83}, "NVDA": {"fy1": 4.50}, "MSFT": {"fy1": 15.0}})
    # AAPL +5%, NVDA +10%, MSFT missing from new scrape entirely (ignored).
    new_fy1 = {"AAPL": 9.27, "NVDA": 4.95}
    gate = kra.run_anomaly_gate(new_fy1, prev)
    assert gate["skipped_no_prev"] is False
    assert gate["checked"] == 2
    assert gate["flagged"] == []


def test_anomaly_gate_tripping_case_large_move():
    # KLAC-style split-like move: FY1 EPS collapses to 1/10th (>=35% threshold
    # blown well past) — this is exactly the 2026-07-16 KLAC/CRWD scenario the
    # skill's Step 5 docstring warns about (mechanical screen must catch it;
    # the split-vs-bad-data judgment itself stays manual).
    prev = _snap({"KLAC": {"fy1": 45.0}})
    new_fy1 = {"KLAC": 4.5}
    gate = kra.run_anomaly_gate(new_fy1, prev)
    assert gate["checked"] == 1
    assert len(gate["flagged"]) == 1
    row = gate["flagged"][0]
    assert row["ticker"] == "KLAC"
    assert row["sign_flip"] is False
    assert row["pct_move"] == pytest.approx(90.0)


def test_anomaly_gate_tripping_case_sign_flip():
    prev = _snap({"XYZ": {"fy1": 2.00}})
    new_fy1 = {"XYZ": -0.50}  # profitable -> loss-making, Koyfin-bad-data archetype
    gate = kra.run_anomaly_gate(new_fy1, prev)
    assert len(gate["flagged"]) == 1
    assert gate["flagged"][0]["sign_flip"] is True


def test_anomaly_gate_mixed_pass_and_trip():
    prev = _snap({"AAA": {"fy1": 5.0}, "BBB": {"fy1": 3.0}, "CCC": {"fy1": 10.0}})
    new_fy1 = {"AAA": 5.1, "BBB": 3.2, "CCC": -1.0}  # AAA/BBB fine, CCC sign flip
    gate = kra.run_anomaly_gate(new_fy1, prev)
    assert gate["checked"] == 3
    flagged_tickers = {r["ticker"] for r in gate["flagged"]}
    assert flagged_tickers == {"CCC"}


def test_anomaly_gate_ignores_tickers_missing_from_previous():
    # A brand-new ticker (not in the prior xlsx at all) must not be flagged —
    # there's nothing to compare it against.
    prev = _snap({"AAA": {"fy1": 5.0}})
    new_fy1 = {"AAA": 5.05, "NEWCO": 1.0}
    gate = kra.run_anomaly_gate(new_fy1, prev)
    assert gate["checked"] == 1
    assert gate["flagged"] == []


# ---------------------------------------------------------------------------
# find_previous_snapshot: largecap's real 2026-09-18 first-run case
# ---------------------------------------------------------------------------

def test_find_previous_snapshot_none_for_largecap_first_run():
    data_dir = ROOT / "data" / "eps-estimates"
    prev = kra.find_previous_snapshot(data_dir, FAMILIES["largecap"]["xlsx_family"], "20260918")
    assert prev is None  # largecap's only xlsx IS the 20260918 one — excluded, nothing earlier exists


def test_find_previous_snapshot_finds_prior_universe_xlsx():
    data_dir = ROOT / "data" / "eps-estimates"
    prev = kra.find_previous_snapshot(data_dir, FAMILIES["screener"]["xlsx_family"], "20260918")
    assert prev is not None
    assert prev.name != "DD_universe_EPS_estimates_20260918.xlsx"
    assert prev.name.startswith("DD_universe_EPS_estimates_")
