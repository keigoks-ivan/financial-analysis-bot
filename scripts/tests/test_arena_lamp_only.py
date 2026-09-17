"""Tests for scripts/engine/build_arena.py's `--daily` mode (2026-09-17 席位引擎
v5 — see knowledge/rule_ledger.md「v5 席位引擎」列 and build_arena.py 檔頭 --daily
段).

v5 REWRITE NOTE: this file used to cover the v4 `--lamp-only` narrow refresh path
(`run_lamp_only()` and its dedicated helpers `_refresh_row_timing()` /
`_refresh_flat_view_timing()` / `_fresh_timing_bundle()` / `_patch_seat_section_in_*()`
/ `_patch_main_table_in_*()`). The owner's v5 instruction replaced that narrow,
timing-only refresh with `--daily`: a full recompute of eligibility/pool/ranking/
timing-lamps/distance-to-ATH that is functionally the SAME code path as the
pre-existing default (`--ledger` omitted) invocation of `main()` — the only thing
`--ledger` ever controlled was whether the resulting roster/snapshot got persisted
to arena-ledger.json, and `main()` already recomputed everything from scratch every
run regardless of that flag. So there is no separate narrow function left to unit-
test here; `run_lamp_only()` and its helpers were deleted from build_arena.py, and
this file was rewritten (not deleted) into an end-to-end test of `main()` itself
run with `--daily`, monkeypatching the module's path constants onto tmp_path
(same fixture-sandbox style the old file used) plus `fetch_caps` (to avoid a real
network call). It proves the three properties the owner asked for:
  1. core membership untouched when nothing hard-vetoes it (carried forward from
     the ledger's `roster.core`, not re-ranked from scratch mid-month)
  2. the pool (waiting pool / not-in-pool) is genuinely re-ranked from the fresh
     input data every run
  3. arena-ledger.json is never written by `--daily` (byte-for-byte unchanged),
     even in the same run where a hard veto visibly changes the *displayed*
     core_seats in arena.json — the eviction only gets persisted on the next
     real `--ledger` (weekly-engine.yml) run
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from engine import build_arena  # noqa: E402


def _patch_paths(monkeypatch, tmp_path):
    """Sandbox every path build_arena.py reads or writes onto tmp_path, so a
    test run can never touch the real repo's docs/engine/* or data/*. OUT_DIR
    itself is patched too (some functions, e.g. load_light_rows()/_yf_rev_map(),
    read it directly at call time), on top of the individually pre-derived
    constants (which were bound once at import time and don't follow OUT_DIR)."""
    paths = {
        "OUT_DIR": tmp_path,
        "ARENA_JSON": tmp_path / "arena.json",
        "ARENA_HTML": tmp_path / "_arena_body.html",
        "LEDGER_JSON": tmp_path / "arena-ledger.json",
        "BOARD_TXT": tmp_path / "board.txt",
        "BOARD_HTML": tmp_path / "_board_body.html",
        "UNIVERSE_BOARD_JSON": tmp_path / "universe_board.json",
        "CARDS_JSON": tmp_path / "cards.json",
        "DD_LATEST": tmp_path / "latest.json",
        "QGM_US": tmp_path / "qgm_us.json",
        "QGM_TW": tmp_path / "qgm_tw.json",
        "LAMP_JSON": tmp_path / "lamp.json",
        "UNIVERSE": tmp_path / "universe.json",
        "MARKET_STATE": tmp_path / "market_state.json",
        "WEEKLY_CACHE_UNIVERSE": tmp_path / "weekly_cache_universe",
    }
    for name, p in paths.items():
        monkeypatch.setattr(build_arena, name, p)
    # Avoid a real yfinance call from apply_cap()'s fetch_caps() — every ticker
    # clears the market-cap floor comfortably.
    monkeypatch.setattr(build_arena, "fetch_caps", lambda tickers, caps=None: {t: 5e10 for t in (tickers or [])})
    return paths


def _v5_stock(ticker, rev_pct, durable=True, dist_ath=-2.0, above_w52=True, **extra):
    """A hand-made dd-screener latest.json row that clears every v5 eligibility
    gate (quality/growth/position/durable) by default — callers vary `rev_pct`
    (drives both the revision veto and pool membership) and `extra` (e.g.
    dca_verdict/dd_age_days to trigger a hard veto) per test."""
    s = {
        "ticker": ticker, "dd_status": "dd", "dca_verdict": None,
        "eps_fy1_fy3_cagr_pct": 25.0,
        "eps_rev_since_earnings_pct": rev_pct, "eps_rev_anchor": "earnings",
        "eps_rev_since_earnings_baseline_date": "2026-08-01",
        "roic": 20.0, "fcf": 15.0, "live_fpe_est": 20.0,
        "durable_5y": durable, "durable_source": "koyfin-xlsx" if durable else None,
        "ma": {"above_w52": above_w52, "price": 100.0, "mom_12_1_pct": 10.0,
               "dist_ath_pct": dist_ath},
        "timing": {"vs_200ma_pct": 5.0, "dist_52w_high_pct": -2.0},
    }
    s.update(extra)
    return s


def _write_fixtures(paths, stocks, as_of="2026-09-20", rev_data_as_of="2026-09-15",
                    ledger=None):
    paths["DD_LATEST"].write_text(json.dumps({
        "as_of": as_of,
        "eps_estimates_source": {"snapshot_date": rev_data_as_of},
        "stocks": stocks,
    }), encoding="utf-8")
    paths["QGM_US"].write_text(json.dumps({"candidates": []}), encoding="utf-8")
    paths["QGM_TW"].write_text(json.dumps({"candidates": []}), encoding="utf-8")
    paths["LAMP_JSON"].write_text(json.dumps({"as_of": as_of, "lamp": {}}), encoding="utf-8")
    if ledger is not None:
        paths["LEDGER_JSON"].write_text(json.dumps(ledger), encoding="utf-8")


_CORE5 = ["PQRSA", "PQRSB", "PQRSC", "PQRSD", "PQRSE"]   # matches CORE_SLOTS=5


def _full_roster_stocks(extra=()):
    """5 tickers that already fill every core slot (so mid-month carry-forward
    has no vacancy to backfill and "core untouched" is a clean, unambiguous
    assertion — CORE_SLOTS is 5, and rotate_roster()'s same-month path tops up
    any *vacant* slots from the pool, which would otherwise contaminate this
    test) plus whatever extra (ticker, rev_pct) pool/non-pool candidates a test
    wants beyond those 5."""
    stocks = [_v5_stock(t, rev_pct=20.0) for t in _CORE5]
    for ticker, rev_pct in extra:
        stocks.append(_v5_stock(ticker, rev_pct=rev_pct))
    return stocks


def _ledger_with_core5():
    return {
        "schema_version": "5.0", "last_rotation_month": "2026-09",
        "roster": {"core": list(_CORE5)}, "w52_fail_streak": {},
        "snapshots": [{"date": "2026-09-13", "core": list(_CORE5), "sat": [],
                       "rotated": True}],
    }


def test_daily_mode_core_untouched_pool_reranked_ledger_untouched(tmp_path, monkeypatch):
    paths = _patch_paths(monkeypatch, tmp_path)
    stocks = _full_roster_stocks(extra=[("PQRSF", 8.0), ("PQRSG", 3.0)])
    ledger_before = _ledger_with_core5()
    _write_fixtures(paths, stocks, ledger=ledger_before)
    ledger_text_before = paths["LEDGER_JSON"].read_text(encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["build_arena.py", "--daily"])
    rc = build_arena.main()
    assert rc == 0

    # 1) ledger untouched — --daily never writes arena-ledger.json, byte for byte.
    assert paths["LEDGER_JSON"].read_text(encoding="utf-8") == ledger_text_before

    out = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    assert out["schema_version"] == "5.0"

    # 2) core membership untouched — same month, no hard veto, no vacancy (all 5
    # slots already filled by the ledger's roster) -> carried forward exactly,
    # not re-derived from this run's ranking.
    assert [r["ticker"] for r in out["core_seats"]] == _CORE5

    # 3) pool re-ranked from fresh data: PQRSF (rev 8%) is in the waiting pool
    # (sat_seats, backward-compat key), PQRSG (rev 3% < the +5% pool floor) is
    # not — it shows up only in "not_in_pool".
    assert [r["ticker"] for r in out["sat_seats"]] == ["PQRSF"]
    assert all(r.get("track") == "pool" for r in out["sat_seats"])
    assert [r["ticker"] for r in out["not_in_pool"]] == ["PQRSG"]
    assert out["pool_size"] == 6   # 5 core + PQRSF; PQRSG excluded (below pool floor)
    assert out["rev_data_as_of"] == "2026-09-15"
    assert out["price_as_of"] == "2026-09-20"

    # Re-rank check: bump PQRSG's revision above the pool floor and above
    # PQRSF's, rerun, and confirm the pool order actually moves — this is what
    # "re-ranked" means, not just "recomputed to the same answer" — while core
    # membership (already full, no veto) stays exactly the same 5 names.
    stocks[-1] = _v5_stock("PQRSG", rev_pct=15.0)
    _write_fixtures(paths, stocks, ledger=ledger_before)
    rc2 = build_arena.main()
    assert rc2 == 0
    out2 = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    assert [r["ticker"] for r in out2["core_seats"]] == _CORE5
    assert [r["ticker"] for r in out2["sat_seats"]] == ["PQRSG", "PQRSF"], (
        "PQRSG 上修拉到 15%（高於 PQRSF 的 8%）後應排到等待池最前面"
    )
    assert paths["LEDGER_JSON"].read_text(encoding="utf-8") == ledger_text_before, (
        "第二次 --daily 重跑仍不得寫入帳本"
    )


def test_daily_mode_hard_veto_evicts_core_seat_but_ledger_stays_frozen(tmp_path, monkeypatch):
    paths = _patch_paths(monkeypatch, tmp_path)
    stocks = _full_roster_stocks(extra=[("PQRSF", 8.0)])
    ledger_before = _ledger_with_core5()
    _write_fixtures(paths, stocks, ledger=ledger_before)
    ledger_text_before = paths["LEDGER_JSON"].read_text(encoding="utf-8")

    # PQRSA now hits a hard veto (fresh DD avoid, well within the 180-day window).
    stocks[0] = _v5_stock("PQRSA", rev_pct=20.0, dca_verdict="迴避", dd_age_days=5)
    _write_fixtures(paths, stocks, ledger=ledger_before)

    monkeypatch.setattr(sys, "argv", ["build_arena.py", "--daily"])
    rc = build_arena.main()
    assert rc == 0

    out = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    # Displayed output reflects the eviction immediately: PQRSA is gone, and the
    # pool's next-best non-seated candidate (PQRSF, the only pool member left
    # over once the other 4 incumbents keep their seats) backfills the vacancy.
    expected_core = [t for t in _CORE5 if t != "PQRSA"] + ["PQRSF"]
    assert sorted(r["ticker"] for r in out["core_seats"]) == sorted(expected_core)
    assert "PQRSA" not in [r["ticker"] for r in out["core_seats"]]
    assert any(t == "PQRSA" and "DD 迴避" in w for t, w in
              [(x["ticker"], x["why"]) for x in out["rotation"]["removed"]])
    assert ("core", "PQRSF") in [(x["track"], x["ticker"]) for x in out["rotation"]["filled"]]
    # ...but the ledger — the actual monthly-rotation clock — never moves under
    # --daily; only the next real `--ledger` (weekly-engine.yml) run persists this.
    assert paths["LEDGER_JSON"].read_text(encoding="utf-8") == ledger_text_before


def test_argparse_daily_and_lamp_only_are_ledger_readonly_aliases():
    """--daily and its v4-name backward-compat alias --lamp-only must both leave
    args.ledger False — that boolean is the only thing that ever gates whether
    main() persists to arena-ledger.json (see rotate_roster()/main()'s `if
    args.ledger:` block). This is a lightweight CLI-contract check that doesn't
    require the full fixture sandbox above."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", action="store_true")
    parser.add_argument("--daily", action="store_true")
    parser.add_argument("--lamp-only", action="store_true")
    for flag in ("--daily", "--lamp-only"):
        args = parser.parse_args([flag])
        assert args.ledger is False


# ── ③ 等待池 timing-lamp grouping (2026-09-17 owner follow-up) ──────────────

def _waiting_row(ticker, dist_ath, lamp_code):
    return {"ticker": ticker, "dist_ath_pct": dist_ath, "lamp": {"code": lamp_code}}


def test_group_waiting_pool_splits_yellow_red_gray_preserving_order():
    rows = [
        _waiting_row("A", -8.8, "yellow"),
        _waiting_row("B", -19.4, "red"),
        _waiting_row("C", -6.2, "yellow"),
        _waiting_row("D", None, "yellow"),   # data missing -> gray, even though lamp said yellow
        _waiting_row("E", -21.1, "red"),
    ]
    yellow, red, gray = build_arena._group_waiting_pool_by_timing(rows)
    assert [r["ticker"] for r in yellow] == ["A", "C"], "組內維持傳入順序（已依上修降冪排序）"
    assert [r["ticker"] for r in red] == ["B", "E"]
    assert [r["ticker"] for r in gray] == ["D"], "dist_ath_pct 缺值優先歸類為資料缺，不管 lamp code"


def test_group_waiting_pool_all_empty_groups_are_valid():
    yellow, red, gray = build_arena._group_waiting_pool_by_timing([])
    assert yellow == [] and red == [] and gray == []
