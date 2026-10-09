"""DD ticker → Koyfin row lookup (load_eps_estimates_xlsx._alias_keys / SKIP_TICKERS).

2026-10-09: Koyfin's "ABB" row in the dd_screener watchlist was Volatus Aerospace,
not ABB Ltd. The watchlist now holds ABBN (SIX); DD ticker "ABB" must read that row
and must never read a row keyed "ABB".

No network, no xlsx.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import load_eps_estimates_xlsx as leex  # noqa: E402


def _snap(tickers: dict) -> leex.ExcelSnapshot:
    return leex.ExcelSnapshot(snapshot_date="2026-10-09", source_file="test.xlsx", tickers=tickers)


def test_abb_reads_abbn_row():
    snap = _snap({"ABBN": {"fy1": 2.9}})
    assert snap.has("ABB")
    assert snap.get("ABB") == {"fy1": 2.9}


def test_abb_koyfin_key_is_dropped_at_load():
    # The loader skips any row keyed "ABB", so an old xlsx with the Volatus row
    # leaves DD ticker ABB uncovered instead of feeding it Volatus numbers.
    assert "ABB" in leex.SKIP_TICKERS
    assert not _snap({}).has("ABB")


def test_existing_aliases_unchanged():
    snap = _snap({"MC": {"fy1": 24.92}, "SU": {"fy1": 11.65}, "AAO": {"fy1": 2.36}})
    assert snap.get("LVMH") == {"fy1": 24.92}
    assert snap.get("SU") == {"fy1": 11.65}
    assert snap.get("AAON") == {"fy1": 2.36}
