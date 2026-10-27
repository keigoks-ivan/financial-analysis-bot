"""build_home_pulse：象限、資產去重、轉折 confirmed／near、油價（用小型假 radar／monitor）。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_home_pulse as pulse  # noqa: E402


def _trail(points):
    """points＝[(r, m), ...]，最後一點是今天。"""
    return [{"d": f"2026-10-{i + 1:02d}", "r": r, "m": m} for i, (r, m) in enumerate(points)]


def _radar(members):
    return {"as_of": "2026-10-26", "generated_at": "2026-10-26T20:00:00Z", "universes": [
        {"key": "other", "members": []},
        {"key": "cross_asset", "members": [
            {"label": lab, "ticker": tk, "frames": {"120": {"trail": tr}}} for lab, tk, tr in members]},
    ]}


def _members():
    flat_strong = [(101, 101)] * 12                            # 一直領先
    cross_confirmed = [(101, 101)] * 4 + [(101, 99)] * 6        # 領先→轉弱，持穩 6 日
    cross_near = [(99, 99)] * 8 + [(99, 100.25)]                # 落後→改善，只有 1 日
    noise = [(99, 99)] * 8 + [(99, 100.05)]                     # 剛穿越且離中軸 < 0.15：不算
    return pulse.radar_members(_radar([
        ("美元", "UUP", _trail(flat_strong)),
        ("標普500", "SPY", _trail(cross_confirmed)),
        ("大宗商品", "DBC", _trail(cross_near)),
        ("黃金", "GLD", _trail(noise)),
        ("空軌跡", "XXX", []),
    ]))


def test_quadrant_boundaries():
    assert pulse.quad(100, 100) == "領先"
    assert pulse.quad(100, 99.99) == "轉弱"
    assert pulse.quad(99.99, 100) == "改善"
    assert pulse.quad(99, 99) == "落後"


def test_members_skip_empty_trail_and_count_streak():
    members = _members()
    assert [m["ticker"] for m in members] == ["UUP", "SPY", "DBC", "GLD"]
    by = {m["ticker"]: m for m in members}
    assert by["UUP"]["streak"] == 12
    assert by["SPY"]["q"] == "轉弱" and by["SPY"]["streak"] == 6


def test_assets_one_row_per_ticker_with_change_merged():
    members = _members()
    pulse.detect_reversals(members)
    assets = pulse.build_assets(members)
    assert [a["ticker"] for a in assets] == ["UUP", "SPY", "DBC", "GLD"]   # 每檔一次，旗標併進該資產
    by = {a["ticker"]: a for a in assets}

    assert by["UUP"]["cell"] == "strong_up" and by["UUP"]["quadrant"] == "領先"
    assert by["UUP"]["change"] is None
    assert by["UUP"]["streak_capped"] is True   # 12 點全在同象限

    spy = by["SPY"]
    assert spy["cell"] == "strong_down" and spy["quadrant"] == "轉弱"
    assert spy["change"] == {"from": "領先", "to": "轉弱", "status": "confirmed", "held_days": 6}
    assert spy["streak_capped"] is False

    dbc = by["DBC"]
    assert dbc["cell"] == "weak_up" and dbc["quadrant"] == "改善"
    assert dbc["change"] == {"from": "落後", "to": "改善", "status": "near", "held_days": 1}

    assert by["GLD"]["change"] is None          # 雜訊過濾
    assert by["GLD"]["cell"] == "weak_up"


def test_confirmed_rule_three_days_needs_half_point_displacement():
    near = pulse.radar_members(_radar([("A", "AAA", _trail([(99, 99)] * 7 + [(99, 100.3)] * 3))]))
    pulse.detect_reversals(near)
    assert near[0]["_rev"]["confirmed"] is False       # 3 日但只離中軸 0.3
    far = pulse.radar_members(_radar([("A", "AAA", _trail([(99, 99)] * 7 + [(99, 100.6)] * 3))]))
    pulse.detect_reversals(far)
    assert far[0]["_rev"]["confirmed"] is True


def test_old_flags_still_produced_for_existing_readers():
    members = _members()
    flags = pulse.reversal_flags(pulse.detect_reversals(members))
    texts = [f["evidence"] for f in flags]
    assert any("持穩" in t for t in texts)              # intel/render.py 靠「持穩」判 confirmed
    assert any("未站穩、接近" in t for t in texts)      # index.html 靠這串判 near


def _latest(with_oil=True):
    items = [{"key": "real10y", "val": "2.66%", "pctile": 91.3, "p20": 100.0, "p60": 98.8}]
    if with_oil:
        items += [
            {"key": "wti", "val": "$101.76", "pctile": 92.1, "p20": 76.2, "p60": 71.8},
            {"key": "brent", "val": "$115.81", "pctile": 98.8, "p20": 88.5, "p60": 71.4},
        ]
    return {"categories": [{"items": items}], "status": {}, "fear_greed": {}}


def test_monitor_points_include_oil():
    pts = pulse.monitor_points(_latest())
    assert "WTI 原油 $101.76，分位 92.1（71.8→76.2→92.1）；Brent 原油 $115.81，分位 98.8（71.4→88.5→98.8）" in pts


def test_monitor_points_skip_oil_when_missing_or_incomplete():
    assert not any("原油" in p for p in pulse.monitor_points(_latest(with_oil=False)))
    latest = _latest()
    latest["categories"][0]["items"][1]["p20"] = None    # WTI 缺一個分位：整段不寫，不補數字
    pts = pulse.monitor_points(latest)
    oil = [p for p in pts if "原油" in p]
    assert oil == ["Brent 原油 $115.81，分位 98.8（71.4→88.5→98.8）"]
