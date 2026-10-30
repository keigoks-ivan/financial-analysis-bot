"""etf-dash 登記程式的查核點（2026-10-30 起守方是 SPY 時只留 cp1、cp5）與舊登記凍結。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "etf_dash"))
import picks_register as pr  # noqa: E402


def cands():
    return {"funds": [{"key": "SMH", "fwd_pe": 25.0, "fy1_rev_3m_pct": 3.0, "breadth_90d_up_pct": 70.0,
                       "scale_usd_bn": 30.0}]}


def test_new_bench_registration_only_lag_and_outflow():
    cps = pr.build_checkpoints(cands(), "SMH", "SPY")
    assert [(c["id"], c["kind"]) for c in cps] == [("cp1", "lag"), ("cp5", "outflow")]
    assert cps[1]["code"] == "SMH" and "300" in cps[1]["text"]


def test_bench_checkpoints_no_longer_need_pe_rev_breadth():
    c = cands()
    for k in ("fwd_pe", "fy1_rev_3m_pct", "breadth_90d_up_pct"):
        c["funds"][0][k] = None
    assert len(pr.build_checkpoints(c, "SMH", "SPY")) == 2


def test_legacy_registrations_keep_frozen_checkpoints():
    d = json.loads((ROOT / "data" / "etf_dash" / "picks.json").read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in d["registrations"]}
    for rid in ("2026-10-28", "2026-10-29"):
        kinds = [c["kind"] for c in by_id[rid]["checkpoints"]]
        assert {"rev_3m", "pe_max", "breadth"} <= set(kinds)


def test_track_reads_frozen_checkpoints_not_regenerated():
    src = (ROOT / "scripts" / "etf_dash" / "picks_track.py").read_text(encoding="utf-8")
    assert 'reg["checkpoints"]' in src and "build_checkpoints" not in src


def test_active_etf_register_untouched():
    import subprocess
    out = subprocess.run(["git", "diff", "--stat", "HEAD", "--", "scripts/active_etf"], cwd=ROOT,
                         capture_output=True, text=True).stdout
    assert out.strip() == ""
