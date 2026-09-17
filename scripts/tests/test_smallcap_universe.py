"""Tests for the v5 smallcap pool's universe isolation (2026-09-17, second
Koyfin universe — dedicated screen `dd_smallcap_v5` + watchlist `dd_smallcap`,
see notes/site-internal/root/_koyfin_smallcap_watchlist_20260917.md and
knowledge/rule_ledger.md「精選榜改版：爆發組退役、十倍組改 v5 小市值池」列).

Covers the task's required test surface:
  1. scripts/load_eps_estimates_xlsx.py — find_latest_excel()/find_excel_for_month()/
     load_latest_excel() `family` kwarg selects the right xlsx family without
     touching default DD_universe_* behaviour (every existing caller omits it).
  2. scripts/build_dd_screener.py — `--universe smallcap` mode: output path /
     xlsx family / snapshot dir isolation (the _output_path()/_excel_family()/
     _snapshot_dir() helpers keyed off UNIVERSE_MODE) and the smallcap universe
     entry shape (no DD pool / QGM assumptions — _smallcap_universe_entries()).
  3. scripts/build_tenbagger.py — smallcap ∪ main dedupe rule: same ticker in
     both files, the main dd-screener latest.json's row wins.
  4. (bonus, directly checked in the task's Verify section) the smallcap-pool
     "upgrade baseline not yet built" page note, and that grp.in_pool() never
     admits a None revision — the v5 smallcap pool's first-snapshot run must
     not silently let the pool look non-empty by construction.

No network, no real xlsx parsing beyond one deliberate round-trip through the
repo's own xlsx builder (scripts/koyfin_xlsx_from_raw.py) to prove the family
kwarg threads all the way to a real read, not just filename globbing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import load_eps_estimates_xlsx as leex  # noqa: E402
import build_dd_screener as bds  # noqa: E402
import build_tenbagger as bt  # noqa: E402
from engine import grp  # noqa: E402


# ---------------------------------------------------------------------------
# 1. load_eps_estimates_xlsx.py — family-scoped filename selection
# ---------------------------------------------------------------------------

def test_find_latest_excel_default_family_ignores_smallcap_family(tmp_path):
    (tmp_path / "DD_universe_EPS_estimates_20260910.xlsx").touch()
    (tmp_path / "DD_universe_EPS_estimates_20260917.xlsx").touch()
    # Later date but wrong family — must NOT be picked by the default call.
    (tmp_path / "DD_smallcap_EPS_estimates_20260918.xlsx").touch()
    found = leex.find_latest_excel(tmp_path)
    assert found is not None
    assert found.name == "DD_universe_EPS_estimates_20260917.xlsx"


def test_find_latest_excel_smallcap_family_ignores_dd_universe_family(tmp_path):
    # Later date but wrong family — must NOT be picked by the smallcap call.
    (tmp_path / "DD_universe_EPS_estimates_20260920.xlsx").touch()
    (tmp_path / "DD_smallcap_EPS_estimates_20260916.xlsx").touch()
    (tmp_path / "DD_smallcap_EPS_estimates_20260917.xlsx").touch()
    found = leex.find_latest_excel(tmp_path, family="DD_smallcap_EPS_estimates_")
    assert found is not None
    assert found.name == "DD_smallcap_EPS_estimates_20260917.xlsx"


def test_find_excel_for_month_is_family_scoped(tmp_path):
    (tmp_path / "DD_universe_EPS_estimates_20260917.xlsx").touch()
    (tmp_path / "DD_smallcap_EPS_estimates_20260917.xlsx").touch()
    found = leex.find_excel_for_month("2026-09", tmp_path, family="DD_smallcap_EPS_estimates_")
    assert found is not None
    assert found.name == "DD_smallcap_EPS_estimates_20260917.xlsx"


def test_load_latest_excel_missing_family_returns_none(tmp_path):
    (tmp_path / "DD_universe_EPS_estimates_20260917.xlsx").touch()
    assert leex.load_latest_excel(tmp_path, family="DD_smallcap_EPS_estimates_") is None


def test_load_latest_excel_smallcap_family_end_to_end(tmp_path):
    """family kwarg threads all the way from find -> load -> parse, not just
    filename globbing — build a real (tiny) xlsx via the repo's own builder
    and confirm load_latest_excel(family=...) reads it back correctly."""
    raw = tmp_path / "raw.txt"
    f = ["TESTCO"] + ["10"] * 53  # ticker + 53 pipe fields (koyfin_xlsx_from_raw's contract)
    raw.write_text("|".join(f) + "\n", encoding="utf-8")
    out_xlsx = tmp_path / "DD_smallcap_EPS_estimates_20260917.xlsx"
    import subprocess
    # koyfin_xlsx_from_raw.py (openpyxl) runs under plain `python3`, not the
    # `python3.12` this test suite itself runs under (repo convention: engine
    # code/tests use python3.12, but build_dd_screener.py's web-scrape/xlsx
    # family uses python3 — see openpyxl's install location).
    subprocess.run(
        ["python3", str(SCRIPTS_DIR / "koyfin_xlsx_from_raw.py"),
         "--raw", str(raw), "--out", str(out_xlsx), "--snapshot-date", "2026-09-17"],
        check=True, capture_output=True,
    )
    snap = leex.load_latest_excel(tmp_path, family="DD_smallcap_EPS_estimates_")
    assert snap is not None
    assert snap.snapshot_date == "2026-09-17"
    assert "TESTCO" in snap.tickers


# ---------------------------------------------------------------------------
# 2. build_dd_screener.py --universe smallcap: path/family isolation + universe shape
# ---------------------------------------------------------------------------

def test_universe_mode_isolates_output_paths(monkeypatch):
    monkeypatch.setattr(bds, "UNIVERSE_MODE", "dd")
    assert bds._output_path() == bds.OUTPUT_PATH
    assert bds._excel_family() == "DD_universe_EPS_estimates_"
    assert bds._snapshot_dir() == bds._DD_SNAPSHOT_DIR

    monkeypatch.setattr(bds, "UNIVERSE_MODE", "smallcap")
    assert bds._output_path() == bds.SMALLCAP_OUTPUT_PATH
    assert bds._output_path() != bds.OUTPUT_PATH
    assert bds._excel_family() == bds.SMALLCAP_XLSX_FAMILY
    assert bds._excel_family() != "DD_universe_EPS_estimates_"
    assert bds._snapshot_dir() == bds.SMALLCAP_SNAPSHOT_DIR
    assert bds._snapshot_dir() != bds._DD_SNAPSHOT_DIR
    # smallcap output must live under its own subtree, not touch the main dir
    assert str(bds.SMALLCAP_OUTPUT_DIR).startswith(str(bds.OUTPUT_DIR))
    assert bds.SMALLCAP_OUTPUT_DIR != bds.OUTPUT_DIR


def test_smallcap_universe_entries_have_no_dd_or_qgm_assumptions():
    class _FakeExcelSnapshot:
        tickers = {"AAA": {}, "BBB": {}, "2330.TW": {}}  # .TW must be market_ok-filtered

    entries = bds._smallcap_universe_entries(_FakeExcelSnapshot())
    tickers_out = sorted(e["ticker"] for e in entries)
    # v2 拍板（美股先行）：.TW 一律排除，見 engine.grp.market_ok()
    assert tickers_out == ["AAA", "BBB"]
    for e in entries:
        assert e["dd_status"] == "none"
        assert e["universe_source"] == "smallcap-koyfin"
        assert e["qgm_seed"] is None
        # every DD-only field must be None — no DD-report / DCA assumption leaks in
        for field in bds._DD_ONLY_FIELDS:
            assert e[field] is None


# ---------------------------------------------------------------------------
# 3. build_tenbagger.py — smallcap ∪ main dedupe (main file wins on overlap)
# ---------------------------------------------------------------------------

def _patch_tenbagger_universe_paths(monkeypatch, tmp_path):
    monkeypatch.setattr(bt, "UNIVERSE_JSON", str(tmp_path / "universe.json"))
    monkeypatch.setattr(bt, "DD_LATEST", str(tmp_path / "latest.json"))
    monkeypatch.setattr(bt, "SMALLCAP_LATEST", str(tmp_path / "smallcap_latest.json"))


def test_tenbagger_dedupe_main_file_wins_on_overlap(tmp_path, monkeypatch):
    _patch_tenbagger_universe_paths(monkeypatch, tmp_path)
    (tmp_path / "universe.json").write_text(json.dumps({"tickers": []}), encoding="utf-8")
    (tmp_path / "latest.json").write_text(json.dumps({
        "as_of": "2026-09-17",
        "eps_estimates_source": {"snapshot_date": "2026-09-10"},
        "stocks": [
            {"ticker": "DUP", "_source": "main"},
            {"ticker": "MAINONLY", "_source": "main"},
        ],
    }), encoding="utf-8")
    (tmp_path / "smallcap_latest.json").write_text(json.dumps({
        "as_of": "2026-09-17",
        "eps_estimates_source": {"snapshot_date": "2026-09-17"},
        "stocks": [
            {"ticker": "DUP", "_source": "smallcap"},
            {"ticker": "SMALLONLY", "_source": "smallcap"},
        ],
    }), encoding="utf-8")

    all_tickers, latest_doc, latest_by_ticker, smallcap_meta, smallcap_tickers = bt.load_universe()

    assert set(all_tickers) >= {"DUP", "MAINONLY", "SMALLONLY"}
    # 主 dd-screener latest.json 的列優先（欄位較完整）——不被 smallcap 池覆蓋
    assert latest_by_ticker["DUP"]["_source"] == "main"
    assert latest_by_ticker["MAINONLY"]["_source"] == "main"
    assert latest_by_ticker["SMALLONLY"]["_source"] == "smallcap"
    # DUP 被主池遮蔽，不算「smallcap 來源」——上修基準提示句判定要用這個集合
    assert smallcap_tickers == {"SMALLONLY"}
    assert smallcap_meta["universe_size"] == 2  # smallcap 檔本身列數（含被遮蔽的 DUP）
    assert smallcap_meta["as_of"] == "2026-09-17"
    assert smallcap_meta["rev_data_as_of"] == "2026-09-17"


def test_tenbagger_missing_smallcap_file_is_a_safe_noop(tmp_path, monkeypatch):
    _patch_tenbagger_universe_paths(monkeypatch, tmp_path)
    (tmp_path / "universe.json").write_text(json.dumps({"tickers": []}), encoding="utf-8")
    (tmp_path / "latest.json").write_text(json.dumps({
        "as_of": "2026-09-17",
        "eps_estimates_source": {"snapshot_date": "2026-09-10"},
        "stocks": [{"ticker": "MAINONLY", "_source": "main"}],
    }), encoding="utf-8")
    # smallcap_latest.json intentionally absent

    all_tickers, latest_doc, latest_by_ticker, smallcap_meta, smallcap_tickers = bt.load_universe()

    assert "MAINONLY" in all_tickers
    assert smallcap_tickers == set()
    assert smallcap_meta == {"as_of": None, "rev_data_as_of": None, "universe_size": 0}


# ---------------------------------------------------------------------------
# 4. Bonus — first-snapshot "revision baseline not built yet" page note, and
#    the pool gate's None-handling this note exists to explain (Verify 段落
#    明列的兩項：rev>=5% 不得放行 None；頁面需顯示「上次快照建立」提示句)。
# ---------------------------------------------------------------------------

def test_in_pool_never_admits_none_revision():
    assert grp.in_pool(None) is False
    assert grp.in_pool(4.9) is False
    assert grp.in_pool(5.0) is True


def test_smallcap_rev_baseline_note_fires_when_all_revisions_none():
    smallcap_meta = {"rev_data_as_of": "2026-09-17"}
    eligible = [
        {"ticker": "A", "grp": {"rev_used_pct": None}},
        {"ticker": "B", "grp": {"rev_used_pct": None}},
    ]
    note = bt._smallcap_rev_baseline_note(smallcap_meta, eligible, {"A", "B"})
    assert note is not None
    assert "2026-10" in note  # 快照月 2026-09 的下一月


def test_smallcap_rev_baseline_note_silent_once_any_revision_exists():
    smallcap_meta = {"rev_data_as_of": "2026-09-17"}
    eligible = [
        {"ticker": "A", "grp": {"rev_used_pct": 6.0}},
        {"ticker": "B", "grp": {"rev_used_pct": None}},
    ]
    assert bt._smallcap_rev_baseline_note(smallcap_meta, eligible, {"A", "B"}) is None


def test_smallcap_rev_baseline_note_silent_for_non_smallcap_universe():
    assert bt._smallcap_rev_baseline_note({"rev_data_as_of": "2026-09-17"}, [], set()) is None
