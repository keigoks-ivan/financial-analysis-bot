"""Tests for the 2026-09-17「精選榜改版」(picks v5 rebuild — see
knowledge/rule_ledger.md「精選榜改版：爆發組退役、十倍組改 v5 小市值池」列 and
notes/site-internal/root/_picks_v5_smallcap_20260917.md):

  1. scripts/build_tenbagger.py — rewritten to reuse the SAME GRP seat v5 rules
     (scripts/engine/grp.py via scripts/engine/build_arena.row_dict()/_flat_view())
     on the $1B-$20B market-cap band instead of the retired S&P 400+600 gate-set.
  2. scripts/build_picks.py — the 爆發（循環拐點型）group is retired the same way
     長熬 was retired on 2026-07-29: candidates.json keeps `official_baofa`/`baofa`
     as empty lists plus a `retired_groups.baofa` marker, rather than dropping the
     keys outright (so existing `.get("official_baofa", [])`-style consumers don't
     need a schema migration for one cycle).

Covers the task's required test surface: cap-band filter, rule reuse (same grp
functions, not forked), veto respected, empty-source fail-safe, retired 爆發
outputs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_tenbagger as bt  # noqa: E402
import build_picks as bp  # noqa: E402
from engine import grp  # noqa: E402


# ---------------------------------------------------------------------------
# Shared fixture helpers
# ---------------------------------------------------------------------------

def _v5_stock(ticker, rev_pct, durable=True, cap_b=None, above_w52=True, **extra):
    """A hand-made dd-screener latest.json row that clears every v5 eligibility
    gate (quality/growth/position/durable) by default — mirrors
    scripts/tests/test_arena_lamp_only.py::_v5_stock so this suite proves
    build_tenbagger.py exercises the exact same grp.py gate, not a reimplementation
    of it. `cap_b` (market cap in USD billions) is folded into `qgm_seed` the same
    way docs/dd-screener/latest.json's QGM-supply rows carry it, letting tests
    control the cap-band filter without touching the mktcap.json cache or network."""
    s = {
        "ticker": ticker, "dd_status": "dd", "dca_verdict": None,
        "eps_fy1_fy3_cagr_pct": 25.0,
        "eps_rev_since_earnings_pct": rev_pct, "eps_rev_anchor": "earnings",
        "eps_rev_since_earnings_baseline_date": "2026-08-01",
        "roic": 20.0, "fcf": 15.0, "live_fpe_est": 20.0,
        "durable_5y": durable, "durable_source": "koyfin-xlsx" if durable else None,
        "ma": {"above_w52": above_w52, "price": 100.0, "mom_12_1_pct": 10.0,
               "dist_ath_pct": -2.0},
        "timing": {"vs_200ma_pct": 5.0, "dist_52w_high_pct": -2.0},
    }
    if cap_b is not None:
        s["qgm_seed"] = {"market_cap_b": cap_b}
    s.update(extra)
    return s


def _patch_tenbagger_paths(monkeypatch, tmp_path):
    universe_json = tmp_path / "universe.json"
    dd_latest = tmp_path / "latest.json"
    picks_json = tmp_path / "picks.json"
    out_json = tmp_path / "tenbagger.json"
    # v5 smallcap pool (2026-09-17): point at a tmp_path file that doesn't exist
    # by default (load_json() fail-safe returns None) so this suite's fixtures
    # stay hermetic — without this, bt.SMALLCAP_LATEST would default to the
    # real repo docs/dd-screener/smallcap/latest.json and leak production
    # tickers into these synthetic-universe tests once that file exists.
    smallcap_latest = tmp_path / "smallcap_latest.json"
    monkeypatch.setattr(bt, "UNIVERSE_JSON", str(universe_json))
    monkeypatch.setattr(bt, "DD_LATEST", str(dd_latest))
    monkeypatch.setattr(bt, "SMALLCAP_LATEST", str(smallcap_latest))
    monkeypatch.setattr(bt, "PICKS", str(picks_json))
    monkeypatch.setattr(bt, "OUT", str(out_json))
    # Cap resolution's network fallback (grp.fetch_caps) must never touch the
    # real internet or the shared data/engine/mktcap.json cache from a test run.
    monkeypatch.setattr(grp, "load_caps", lambda: {})
    monkeypatch.setattr(grp, "fetch_caps", lambda tickers, caps=None: dict(caps or {}))
    monkeypatch.setattr(bt.arena, "qgm_cap_map", lambda: {})
    return {"universe": universe_json, "latest": dd_latest, "picks": picks_json,
            "out": out_json, "smallcap_latest": smallcap_latest}


def _write_universe(path, tickers):
    path.write_text(json.dumps({
        "fetched_at": "2026-09-17T00:00:00Z", "n": len(tickers),
        "tickers": [{"ticker": t, "sector": "Test", "tier": "sp400"} for t in tickers],
    }), encoding="utf-8")


def _write_latest(path, stocks, as_of="2026-09-17"):
    path.write_text(json.dumps({
        "as_of": as_of,
        "eps_estimates_source": {"snapshot_date": "2026-09-10"},
        "stocks": stocks,
    }), encoding="utf-8")


def _write_picks(path, veto=None):
    path.write_text(json.dumps({"veto": list(veto or [])}), encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Cap-band filter ($1B-$20B, same floor as GRP seat's $20B ceiling)
# ---------------------------------------------------------------------------

def test_cap_band_filter_keeps_only_1b_to_20b(tmp_path, monkeypatch):
    paths = _patch_tenbagger_paths(monkeypatch, tmp_path)
    tickers = ["TOOSML", "INBAND", "TOOBIG"]
    _write_universe(paths["universe"], tickers)
    stocks = [
        _v5_stock("TOOSML", rev_pct=20.0, cap_b=0.5),   # below $1B floor
        _v5_stock("INBAND", rev_pct=20.0, cap_b=5.0),   # $5B — squarely in band
        _v5_stock("TOOBIG", rev_pct=20.0, cap_b=25.0),  # above $20B ceiling (GRP's own turf)
    ]
    _write_latest(paths["latest"], stocks)
    _write_picks(paths["picks"])

    rc = bt.main()
    assert rc == 0

    out = json.loads(paths["out"].read_text(encoding="utf-8"))
    all_tickers = {r["ticker"] for r in out["official"]} | {r["ticker"] for r in out["not_in_pool"]}
    assert all_tickers == {"INBAND"}
    assert out["outside_band"] == 2   # TOOSML + TOOBIG: cap known, just not in band
    assert out["data_insufficient"]["合計"] == 0   # neither is a data problem — both have known caps
    funnel = out["gate_funnel"]
    assert funnel["市值落在 $10億–$200億帶"] == 1


# ---------------------------------------------------------------------------
# 2. Rule reuse — same grp.py functions, not a forked reimplementation
# ---------------------------------------------------------------------------

def test_pool_reuses_grp_score_and_timing_lamp_not_forked(tmp_path, monkeypatch):
    paths = _patch_tenbagger_paths(monkeypatch, tmp_path)
    tickers = ["HIREV", "LOREV", "NOTDUR"]
    _write_universe(paths["universe"], tickers)
    stocks = [
        _v5_stock("HIREV", rev_pct=20.0, cap_b=5.0),     # clears eligibility, deep in pool (>= +5%)
        _v5_stock("LOREV", rev_pct=8.0, cap_b=5.0),      # clears eligibility, in pool but lower rev
        _v5_stock("NOTDUR", rev_pct=20.0, cap_b=5.0, durable=False),  # fails v5 durability gate
    ]
    _write_latest(paths["latest"], stocks)
    _write_picks(paths["picks"])

    rc = bt.main()
    assert rc == 0
    out = json.loads(paths["out"].read_text(encoding="utf-8"))

    # NOTDUR never eligible under the SAME grp.grp_score() rule build_arena.py's
    # seat table uses (durable_5y is part of the v5 eligibility gate itself).
    official_tickers = [r["ticker"] for r in out["official"]]
    assert "NOTDUR" not in official_tickers
    assert not any(r["ticker"] == "NOTDUR" for r in out["not_in_pool"])

    # Pool sort key (grp.pool_sort_key: revision descending) — not a bespoke
    # ranking, the same one build_arena.py's seat pool uses.
    assert official_tickers == ["HIREV", "LOREV"]

    # Cross-check the row's own numbers against calling grp.grp_score()/
    # grp.timing_lamp() directly on the identical input — if build_tenbagger.py
    # had forked its own copy of the gate, these would be free to drift.
    hi_stock = stocks[0]
    expect_grp = grp.grp_score(hi_stock)
    expect_lamp = grp.timing_lamp(hi_stock)
    hi_row = out["official"][0]
    assert hi_row["rev_used_pct"] == expect_grp["rev_used_pct"]
    assert hi_row["lamp"]["code"] == expect_lamp["code"]
    assert hi_row["durable_5y"] is True


# ---------------------------------------------------------------------------
# 3. Veto respected (picks.json veto[], same file the seat pool and the
#    (now-retired) baofa pipeline both deferred to)
# ---------------------------------------------------------------------------

def test_veto_excludes_ticker_entirely(tmp_path, monkeypatch):
    paths = _patch_tenbagger_paths(monkeypatch, tmp_path)
    tickers = ["VETOED", "CLEAN"]
    _write_universe(paths["universe"], tickers)
    stocks = [
        _v5_stock("VETOED", rev_pct=20.0, cap_b=5.0),
        _v5_stock("CLEAN", rev_pct=20.0, cap_b=5.0),
    ]
    _write_latest(paths["latest"], stocks)
    _write_picks(paths["picks"], veto=["VETOED"])

    rc = bt.main()
    assert rc == 0
    out = json.loads(paths["out"].read_text(encoding="utf-8"))

    all_tickers = ({r["ticker"] for r in out["official"]}
                   | {r["ticker"] for r in out["not_in_pool"]}
                   | {r["ticker"] for r in out["buyable"]}
                   | {r["ticker"] for r in out["waiting"]["yellow"]}
                   | {r["ticker"] for r in out["waiting"]["red"]})
    assert "VETOED" not in all_tickers
    assert "CLEAN" in all_tickers
    assert out["veto"] == ["VETOED"]


# ---------------------------------------------------------------------------
# 4. Empty-source fail-safe — must never fail the workflow, must not clobber
#    whatever tenbagger.json already existed.
# ---------------------------------------------------------------------------

def test_missing_sources_is_a_safe_noop(tmp_path, monkeypatch):
    paths = _patch_tenbagger_paths(monkeypatch, tmp_path)
    # Neither universe.json nor dd-screener latest.json exist at all.
    stale = json.dumps({"as_of": "2026-09-10", "official": [{"ticker": "STALE"}]})
    paths["out"].write_text(stale, encoding="utf-8")
    _write_picks(paths["picks"])

    rc = bt.main()

    assert rc == 0
    # Existing good data is preserved rather than overwritten with an empty/broken file.
    assert paths["out"].read_text(encoding="utf-8") == stale


# ---------------------------------------------------------------------------
# 5. build_picks.py — 爆發 retirement (mirrors the 長熬 2026-07-29 precedent)
# ---------------------------------------------------------------------------

def test_build_picks_emits_retired_empty_baofa(tmp_path, monkeypatch):
    latest = tmp_path / "latest.json"
    out = tmp_path / "candidates.json"
    latest.write_text(json.dumps({"as_of": "2026-09-17", "stocks": []}), encoding="utf-8")
    monkeypatch.setattr(bp, "LATEST", str(latest))
    monkeypatch.setattr(bp, "OUT", str(out))

    rc = bp.main()
    assert rc == 0

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["official_baofa"] == []
    assert payload["baofa"] == []
    assert payload["counts"] == {"official_baofa": 0, "baofa": 0}
    assert payload["retired_groups"]["baofa"]["retired_on"] == "2026-09-17"
    assert payload["retired_groups"]["changhao"]["retired_on"] == "2026-07-29"
    assert payload["as_of"] == "2026-09-17"
