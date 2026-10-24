"""QGM 重建列改用 dd-screener 數值（2026-10-24，build_arena._overlay_latest_none）：
latest.json 有對應 dd_status="none" 列時，數值與 ma／timing／fund 取該列；
該列缺值才退回 QGM；dist_ath_pct 也缺時時機燈維持「🟡 資料缺」。無網路。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from engine import build_arena as ba  # noqa: E402
from engine.grp import timing_lamp  # noqa: E402


def _qgm_file(tmp_path):
    p = tmp_path / "qgm_us.json"
    p.write_text(json.dumps({"candidates": [{
        "ticker": "ZZZ", "fy1_eps": 2.0, "fy2_eps": 2.4, "fy1_per": 20.0, "price": 50.0,
        "market_cap_b": 30.0,
        "hard_filter_details": {"roic": {"value": 0.20}, "fcf_margin": {"value": 0.18},
                                "debt_to_equity": {"value": 0.5}},
        "quality_breakdown": {"roic_5y_stability": {"pct_above": 0.8}},
    }]}), encoding="utf-8")
    return p


def _load(tmp_path, monkeypatch, latest_none):
    monkeypatch.setattr(ba, "QGM_US", _qgm_file(tmp_path))
    monkeypatch.setattr(ba, "QGM_TW", tmp_path / "missing.json")
    monkeypatch.setattr(ba, "weekly_structure", lambda tk: {"px": 50.0, "r26": 10.0, "r52": 20.0,
                                                             "above_w52": True, "dist_hi52": -5.0})
    monkeypatch.setattr(ba, "compute_peg_unified", lambda *a, **k: {"fpe_next": 21.0, "live_peg": 1.4})
    rows = ba.load_qgm_rows({}, latest_none=latest_none)
    assert len(rows) == 1
    return rows[0]


def test_dd_screener_values_win(tmp_path, monkeypatch):
    ln = {"ZZZ": {"ticker": "ZZZ", "dd_status": "none", "universe_source": "qgm-us",
                  "roic": 31.8, "fcf": None, "eps_fy3": 3.1, "live_peg": 0.9,
                  "incremental_roic_pct": 40.0, "implied_growth_pct": 12.0,
                  "ol_divergence_pp": -5.0, "ol_divergence_label": "利潤率擴張",
                  "fund": {"est_rev_cagr_3y_pct": 8.0},
                  "ma": {"price": 51.0, "above_w52": True, "dist_ath_pct": -14.7, "ath_source": "full"},
                  "timing": {"vs_200ma_pct": 4.0, "dist_52w_high_pct": None}}}
    r = _load(tmp_path, monkeypatch, ln)
    assert r["roic"] == 31.8                       # dd-screener 值優先
    assert abs(r["fcf"] - 18.0) < 1e-9             # dd-screener 缺 → 退回 QGM
    assert r["live_peg"] == 0.9 and r["fpe_next"] == 21.0
    assert r["eps_fy3"] == 3.1 and r["incremental_roic_pct"] == 40.0
    assert r["fund"]["est_rev_cagr_3y_pct"] == 8.0
    assert r["ma"]["dist_ath_pct"] == -14.7 and r["ma"]["price"] == 51.0
    assert r["timing"]["vs_200ma_pct"] == 4.0
    assert r["timing"]["dist_52w_high_pct"] == -5.0  # 巢狀欄 dd-screener 為 None → 保留 QGM
    assert r["_src"] == "qgm" and r["_durable_5y"] == 0.8 and r["_mktcap"] == 30e9
    lamp = timing_lamp(r, yellow_full=True)
    assert lamp["code"] == "red"
    dn = ba.dd_numbers(r)
    assert dn["inc_roic"] == 40.0 and dn["implied"] == 12.0 and dn["rev3"] == 8.0 and dn["ol_pp"] == -5.0


def test_missing_dist_ath_keeps_data_missing_lamp(tmp_path, monkeypatch):
    ln = {"ZZZ": {"ticker": "ZZZ", "dd_status": "none", "roic": 25.0,
                  "ma": {"price": 51.0, "above_w52": True, "dist_ath_pct": None}}}
    r = _load(tmp_path, monkeypatch, ln)
    assert r["ma"].get("dist_ath_pct") is None
    assert timing_lamp(r, yellow_full=True)["label"] == "🟡 資料缺"


def test_no_latest_none_row_unchanged(tmp_path, monkeypatch):
    r = _load(tmp_path, monkeypatch, {})
    assert abs(r["roic"] - 20.0) < 1e-9 and r["live_peg"] == 1.4
    assert r["ma"] == {"above_w52": True, "price": 50.0}
