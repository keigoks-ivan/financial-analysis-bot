"""2026-10-11：共識 EPS 改依 koyfin_families 找快照家族（8 檔台股共識全空案）。

覆蓋：universe 池成分股照舊、只在 smallcap／largecap／台股池的成分股讀得到、台股美元 EPS 依快照日
匯率換新台幣且查不到匯率時不混幣別、dd_facts 的台股單位、dd2 plan 段缺共識就停。
"""
from __future__ import annotations

import json
import sys
import types
from datetime import datetime
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "dd2"))

import dd_facts  # noqa: E402
import dd_numbers_extra as dne  # noqa: E402
import eps_fx_normalize  # noqa: E402
import run  # noqa: E402


class _Snap:
    def __init__(self, date, recs):
        self.snapshot_date, self._recs = date, recs

    def get(self, t):
        return self._recs.get(t)


def _setup(monkeypatch, fx=31.912):
    snaps = {
        "u1": _Snap("2026-09-10", {"AMD": {"fy1": 4.0, "fy2": 6.0, "fy3": 8.0}}),
        "u2": _Snap("2026-10-08", {"AMD": {"fy1": 4.2, "fy2": 6.3, "fy3": 8.4},
                                    "BOTH": {"fy1": 1.0, "fy2": 2.0, "fy3": 3.0}}),
        "l2": _Snap("2026-10-08", {"AMGN": {"fy1": 23.05, "fy2": 24.47, "fy3": 26.0},
                                    "BOTH": {"fy1": 9.0, "fy2": 9.0, "fy3": 9.0}}),
        "t1": _Snap("2026-10-09", {"2395.TW": {"fy1": 0.62, "fy2": 0.74, "fy3": 0.87}}),
    }
    fams = {"DD_universe_EPS_estimates_": [("u1", "20260910"), ("u2", "20261008")],
            "DD_smallcap_EPS_estimates_": [], "DD_largecap_EPS_estimates_": [("l2", "20261008")],
            "DD_tw_EPS_estimates_": [("t1", "20261009")]}
    monkeypatch.setattr(dne, "_family_files", lambda prefix: [(Path(q), d) for q, d in fams[prefix]])
    monkeypatch.setattr(dne, "_load_snap", lambda p: snaps[p.name])
    monkeypatch.setattr(dne, "_fx_cache", {})
    monkeypatch.setattr(eps_fx_normalize, "get_fx_rate", lambda cur, d, cache: fx if cur == "TWD" else None)
    return snaps


def test_universe_member_keeps_universe_family(monkeypatch):
    _setup(monkeypatch)
    assert [d for _, d in dne._eps_snapshot_files("AMD")] == ["20260910", "20261008"]
    assert dne._eps_snapshot_files("BOTH")[-1][0].name == "u2"  # 兩池都有 → universe 優先


def test_other_family_member_found(monkeypatch):
    _setup(monkeypatch)
    assert dne._eps_snapshot_files("AMGN") == [(Path("l2"), "20261008")]
    r = dne.compute_consensus_revision("AMGN", datetime(2026, 10, 11))
    assert r["latest_snapshot"]["fy2"] == 24.47 and r.get("eps_basis") is None


def test_uncovered_ticker_falls_back_to_universe(monkeypatch):
    _setup(monkeypatch)
    r = dne.compute_consensus_revision("ZZZZ", datetime(2026, 10, 11))
    assert r["latest_snapshot"] is None and "不在最新快照" in r["note"]


def test_tw_usd_eps_converted_to_twd(monkeypatch):
    _setup(monkeypatch)
    r = dne.compute_consensus_revision("2395.TW", datetime(2026, 10, 11))
    ls = r["latest_snapshot"]
    assert (ls["fy1"], ls["fy2"], ls["fy3"]) == (19.79, 23.61, 27.76)
    assert r["eps_basis"].startswith("twd (koyfin usd ×31.9120 @ 2026-10-09")


def test_tw_without_fx_rate_is_missing_not_usd(monkeypatch):
    _setup(monkeypatch, fx=None)
    r = dne.compute_consensus_revision("2395.TW", datetime(2026, 10, 11))
    assert r["latest_snapshot"] is None  # 不可把美元值當新台幣用


def test_dd_facts_tw_consensus_unit():
    numbers = {"price_at_dd": 727.0, "consensus_revision": {
        "eps_basis": "twd (koyfin usd ×31.9120 @ 2026-10-09)",
        "latest_snapshot": {"file": "DD_tw_EPS_estimates_20261009.xlsx", "date": "2026-10-09",
                            "fy1": 19.79, "fy2": 23.61}}}
    buckets = {"q5_valuation": {"facts": []}}
    dd_facts._valuation_facts(numbers, buckets, ticker="2395.TW")
    facts = {f["id"]: f for f in buckets["q5_valuation"]["facts"]}
    assert facts["f_price_at_dd"]["unit"] == "TWD"
    assert facts["f_consensus_eps_fy2"]["unit"] == "TWD/share"
    assert "新台幣" in facts["f_consensus_eps_fy2"]["basis"]


def _plan_ctx(tmp_path, latest, allow=False, ticker="2395.TW"):
    (tmp_path / "parts").mkdir(exist_ok=True)
    (tmp_path / "parts" / "numbers_extra.json").write_text(json.dumps(
        {"numbers": {"consensus_revision": {"latest_snapshot": latest, "note": "2395.TW 不在最新快照 X"}}},
        ensure_ascii=False), encoding="utf-8")
    return types.SimpleNamespace(run_dir=tmp_path, ticker=ticker, manifest={"stages": {"plan": {}}},
                                 args=types.SimpleNamespace(allow_no_consensus=allow))


def test_plan_consensus_gate(tmp_path):
    assert "共識 EPS 未載入" in run._consensus_check(_plan_ctx(tmp_path, None))
    assert run._consensus_check(_plan_ctx(tmp_path, {"fy1": 19.79})) is not None  # 缺 FY2 也停
    assert run._consensus_check(_plan_ctx(tmp_path, None, allow=True)) is None
    ctx = _plan_ctx(tmp_path, {"file": "f", "date": "2026-10-09", "fy1": 19.79, "fy2": 23.61})
    assert run._consensus_check(ctx) is None
    assert ctx.manifest["stages"]["plan"]["consensus"]["fy2"] == 23.61


def test_bare_numeric_ticker_stops():
    assert run.main(["3017", "--dry-run"]) == 2


def test_fy2_peg_convention():
    import gen_dd_tables
    # TPR_20261005 判斷者自填 13.27／1.01：FY1→FY3 年化
    assert gen_dd_tables.fy2_peg(13.27, 1.0, 1.117, 1.117 * 1.147) == 1.01
    assert gen_dd_tables.fy2_peg(20.0, 2.0, 2.4) == 1.0  # 缺 FY3 → FY1→FY2
    assert gen_dd_tables.fy2_peg(20.0, 2.0, 1.8, 1.6) == -1
    assert gen_dd_tables.fy2_peg(20.0, None, 2.0) is None


def _fill_ctx(tmp_path, aa, ls):
    (tmp_path / "judgment.json").write_text(json.dumps({"appendix_a": aa}, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "evidence.json").write_text(json.dumps(
        {"numbers": {"price_at_dd": 727.0, "consensus_revision": {"latest_snapshot": ls}}}), encoding="utf-8")
    return types.SimpleNamespace(run_dir=tmp_path, manifest={}, save=lambda: None)


def _aa(tmp_path):
    return json.loads((tmp_path / "judgment.json").read_text(encoding="utf-8"))["appendix_a"]


LS_2395 = {"file": "DD_tw_EPS_estimates_20261009.xlsx", "date": "2026-10-09", "fy1": 19.79, "fy2": 23.61, "fy3": 27.76}


def test_fy2_fill_from_consensus_when_blank(tmp_path):
    ctx = _fill_ctx(tmp_path, {"fpe_fy2": None, "peg_fy2": None}, LS_2395)
    assert run._fy2_valuation_fill(ctx) == 2
    aa = _aa(tmp_path)
    assert aa["fpe_fy2"] == 30.8 and aa["peg_fy2"] == 1.67
    assert aa["fy2_valuation_basis"] == "依 Koyfin 共識（2026-10-09）"
    assert [o["path"] for o in ctx.manifest["mechanical_overrides"]] == ["$.appendix_a.fpe_fy2", "$.appendix_a.peg_fy2"]


def test_fy2_fill_keeps_judge_values(tmp_path):
    ctx = _fill_ctx(tmp_path, {"fpe_fy2": 16.7, "peg_fy2": 0.49}, LS_2395)
    assert run._fy2_valuation_fill(ctx) == 0 and _aa(tmp_path)["fpe_fy2"] == 16.7
    ctx = _fill_ctx(tmp_path, {"fpe_fy2": 31.0, "peg_fy2": None}, LS_2395)
    assert run._fy2_valuation_fill(ctx) == 1
    aa = _aa(tmp_path)
    assert aa["fpe_fy2"] == 31.0 and aa["fy2_valuation_basis"].startswith("PEG 依")


def test_fy2_fill_no_consensus_leaves_blank(tmp_path):
    ctx = _fill_ctx(tmp_path, {"fpe_fy2": None, "peg_fy2": None}, None)
    assert run._fy2_valuation_fill(ctx) == 0 and _aa(tmp_path)["fpe_fy2"] is None


def test_fy2_fill_forced_overwrites(tmp_path):
    ctx = _fill_ctx(tmp_path, {"fpe_fy2": 16.7, "peg_fy2": 0.49}, None)
    cons = dict(LS_2395, price=727.0)
    assert run._fy2_valuation_fill(ctx, consensus=cons, basis_suffix="；10-11 補正") == 2
    aa = _aa(tmp_path)
    assert aa["fpe_fy2"] == 30.8 and aa["fy2_valuation_basis"].endswith("；10-11 補正")
    assert ctx.manifest["mechanical_overrides"][0]["judge"] == 16.7
