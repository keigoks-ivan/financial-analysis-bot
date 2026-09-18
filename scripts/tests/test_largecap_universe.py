"""Tests for the v5.1 largecap pool — third dd-screener ticker source (2026-09-18,
notes/site-internal/root/_seat_engine_v5_1_20260918.md §2, knowledge/rule_ledger.md
「2026-09-18：主母體加 Koyfin 大市值來源（DD 選配落實）」列).

Unlike the smallcap pool (test_smallcap_universe.py — an isolated UNIVERSE_MODE
with its own output dir), the largecap pool is a third ticker source merged
straight into the main dd-universe build (UNIVERSE_MODE == "dd"): names with a
Koyfin `dd_largecap_v5` screen hit (US, mktcap>=$20B, ROIC LTM>=15, FCF Margin
LTM>0) but no DD report and not already in QGM. It reuses
build_dd_screener._smallcap_universe_entries() (generalized with `source`/
`existing_tickers` kwargs, see that function's docstring) rather than a
copy-pasted variant.

Covers the task's required test surface:
  1. Entries shaped correctly (dd_status="none", universe_source=
     "largecap-koyfin", every DD-only field None) — same shape contract as the
     smallcap pool, just a different source tag.
  2. Dedupe against existing DD/QGM tickers via the new `existing_tickers` kwarg
     (the smallcap pool never needs this — its own isolated universe has no
     prior tickers to dedupe against — so this kwarg is largecap-only surface).
  3. Missing xlsx family -> load_latest_excel() returns None (same loader-level
     contract as the smallcap family; build_dd_screener.py's Step 1-2d/Step 0d
     both no-op on this, see that file's comments at the two call sites).
  4. Market filter applied (.TW excluded via engine.grp.market_ok(), same as
     the smallcap pool).
  5. The scripts/engine/build_arena.py main() block this task owns (lines
     ~1809-1829: `latest_none` built, dd_status=="none" rows dropped) must keep
     a universe_source=="largecap-koyfin" row while still dropping a plain
     universe_source=="qgm-us" dd_status="none" row. That block lives inline in
     main() (not a standalone function), and build_arena.py's main() does heavy
     network I/O (yfinance market-cap fetches etc.) plus is being edited
     concurrently elsewhere in the same file by another agent this task must
     not couple to — so per the task's "smallest unit you can extract without
     importing heavy network code" guidance, the exact filter predicate is
     replicated here (not imported) and kept in sync by line-reference comment
     rather than by import.

No network, no real xlsx parsing beyond a fake ExcelSnapshot-shaped stub (same
style as test_smallcap_universe.py's _FakeExcelSnapshot).
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import load_eps_estimates_xlsx as leex  # noqa: E402
import build_dd_screener as bds  # noqa: E402


# ---------------------------------------------------------------------------
# 1. Entries shaped correctly (source="largecap-koyfin")
# ---------------------------------------------------------------------------

class _FakeExcelSnapshot:
    tickers = {"AAA": {}, "BBB": {}, "2330.TW": {}}  # .TW must be market_ok-filtered


def test_largecap_universe_entries_have_no_dd_or_qgm_assumptions():
    entries = bds._smallcap_universe_entries(_FakeExcelSnapshot(), source="largecap-koyfin")
    tickers_out = sorted(e["ticker"] for e in entries)
    # v2 拍板（美股先行）：.TW 一律排除，見 engine.grp.market_ok()
    assert tickers_out == ["AAA", "BBB"]
    for e in entries:
        assert e["dd_status"] == "none"
        assert e["universe_source"] == "largecap-koyfin"
        assert e["qgm_seed"] is None
        # every DD-only field must be None — no DD-report / DCA assumption leaks in
        for field in bds._DD_ONLY_FIELDS:
            assert e[field] is None


def test_smallcap_default_source_unchanged_by_generalization():
    """Regression guard: adding `source`/`existing_tickers` kwargs must not
    change the smallcap pool's existing zero-arg call shape (test_smallcap_
    universe.py calls this positionally with no kwargs)."""
    entries = bds._smallcap_universe_entries(_FakeExcelSnapshot())
    assert {e["universe_source"] for e in entries} == {"smallcap-koyfin"}


# ---------------------------------------------------------------------------
# 2. Dedupe against existing DD/QGM tickers (`existing_tickers` kwarg)
# ---------------------------------------------------------------------------

def test_largecap_universe_entries_dedupe_against_existing_tickers():
    class _Snap:
        tickers = {"AAA": {}, "BBB": {}, "CCC": {}}

    # AAA already a DD ticker, BBB already a QGM-supplied ticker — only CCC is new.
    entries = bds._smallcap_universe_entries(
        _Snap(), source="largecap-koyfin", existing_tickers={"AAA", "BBB"})
    assert [e["ticker"] for e in entries] == ["CCC"]


def test_largecap_universe_entries_no_dedupe_when_existing_tickers_omitted():
    class _Snap:
        tickers = {"AAA": {}}

    entries = bds._smallcap_universe_entries(_Snap(), source="largecap-koyfin")
    assert [e["ticker"] for e in entries] == ["AAA"]


# ---------------------------------------------------------------------------
# 3. Missing xlsx family -> load_latest_excel() returns None
# ---------------------------------------------------------------------------

def test_load_latest_excel_missing_largecap_family_returns_none(tmp_path):
    (tmp_path / "DD_universe_EPS_estimates_20260917.xlsx").touch()
    (tmp_path / "DD_smallcap_EPS_estimates_20260917.xlsx").touch()
    # Later date but wrong family — must NOT be picked by the largecap call.
    assert leex.load_latest_excel(tmp_path, family=bds.LARGECAP_XLSX_FAMILY) is None


def test_find_latest_excel_largecap_family_ignores_other_families(tmp_path):
    (tmp_path / "DD_universe_EPS_estimates_20260920.xlsx").touch()
    (tmp_path / "DD_smallcap_EPS_estimates_20260919.xlsx").touch()
    (tmp_path / "DD_largecap_EPS_estimates_20260916.xlsx").touch()
    (tmp_path / "DD_largecap_EPS_estimates_20260918.xlsx").touch()
    found = leex.find_latest_excel(tmp_path, family=bds.LARGECAP_XLSX_FAMILY)
    assert found is not None
    assert found.name == "DD_largecap_EPS_estimates_20260918.xlsx"


# ---------------------------------------------------------------------------
# 4. Market filter applied (.TW excluded) — already exercised above via the
#    _FakeExcelSnapshot fixture's "2330.TW" ticker in test 1; kept explicit
#    here as its own assertion for clarity of intent.
# ---------------------------------------------------------------------------

def test_largecap_universe_entries_exclude_tw_listings():
    # engine.grp.EXCLUDED_SUFFIXES == (".TW",) only — 2026-09-02 拍板僅排除台股，
    # 其餘掛牌（含 .T 日股）不在本輪排除範圍，故只用 .TW 當排除樣本（同
    # test_smallcap_universe.py 的既有斷言口徑）。
    class _Snap:
        tickers = {"NVDA": {}, "2330.TW": {}}

    entries = bds._smallcap_universe_entries(_Snap(), source="largecap-koyfin")
    assert [e["ticker"] for e in entries] == ["NVDA"]


# ---------------------------------------------------------------------------
# 5. scripts/engine/build_arena.py main() block (lines ~1809-1829, this task's
#    only sanctioned edit surface in that file): keep largecap-koyfin rows,
#    still drop plain qgm-us dd_status="none" rows. Predicate replicated (not
#    imported) — see module docstring point 5 for why.
# ---------------------------------------------------------------------------

def _arena_dd_status_none_filter(stocks: list[dict]) -> list[dict]:
    """Mirrors scripts/engine/build_arena.py main()'s
        stocks = [s for s in stocks if s.get("dd_status") != "none"
                  or s.get("universe_source") == "largecap-koyfin"]
    line (2026-09-18 addition to the pre-existing dd_status=="none" drop) —
    the exact block this task owns in that file. Kept here as a literal copy
    rather than an import so this test doesn't couple to build_arena.py's
    module-level imports (engine.grp / engine.build_scoreboard / yfinance-
    touching main()) or to the concurrent edits another agent is making
    elsewhere in that same file this run."""
    return [s for s in stocks if s.get("dd_status") != "none"
            or s.get("universe_source") == "largecap-koyfin"]


def test_arena_filter_keeps_largecap_koyfin_row():
    stocks = [
        {"ticker": "DD1", "dd_status": "dd"},
        {"ticker": "LCK", "dd_status": "none", "universe_source": "largecap-koyfin"},
    ]
    kept = {s["ticker"] for s in _arena_dd_status_none_filter(stocks)}
    assert kept == {"DD1", "LCK"}


def test_arena_filter_still_drops_qgm_us_dd_status_none_row():
    stocks = [
        {"ticker": "DD1", "dd_status": "dd"},
        {"ticker": "LCK", "dd_status": "none", "universe_source": "largecap-koyfin"},
        {"ticker": "QGM1", "dd_status": "none", "universe_source": "qgm-us"},
    ]
    kept = {s["ticker"] for s in _arena_dd_status_none_filter(stocks)}
    assert kept == {"DD1", "LCK"}
    assert "QGM1" not in kept
