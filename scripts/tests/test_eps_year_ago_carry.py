"""eps_year_ago 沿用上次值的判斷（同一財年末日才沿用）單元測試。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_dd_screener as b  # noqa: E402

PREV = {"eps_year_ago": 5.0, "eps_year_ago_0y_avg": 6.0,
        "fiscal_year_end": "2025-12-31", "as_of": "2026-10-01"}


def test_same_fye_carries_legacy_row():
    # legacy row: fye derived from fiscal_year_end + as_of -> 2025-12-31
    cur = b.year_ago_fye("2025-12-31", "2026-10-08")
    assert cur == "2025-12-31"
    out = b.decide_year_ago_carry(PREV, cur)
    assert out["eps_year_ago"] == 5.0 and out["eps_year_ago_0y_avg"] == 6.0


def test_fye_rolled_does_not_carry():
    cur = b.year_ago_fye("2025-12-31", "2027-01-05")  # rolled to 2026-12-31
    assert cur == "2026-12-31"
    assert b.decide_year_ago_carry(PREV, cur) is None


def test_explicit_prev_fye_field_wins():
    prev = {**PREV, "eps_year_ago_fye": "2024-12-31"}
    assert b.decide_year_ago_carry(prev, "2025-12-31") is None
    prev["eps_year_ago_fye"] = "2025-12-31"
    assert b.decide_year_ago_carry(prev, "2025-12-31") is not None


def test_previous_missing_is_missing():
    assert b.decide_year_ago_carry(None, "2025-12-31") is None
    assert b.decide_year_ago_carry({**PREV, "eps_year_ago": None}, "2025-12-31") is None
    assert b.decide_year_ago_carry(PREV, None) is None


def test_legacy_row_rolled_between_builds():
    # prev built 2026-12-20 (FYE 2025-12-31 still current); now 2027-01-05 -> rolled
    prev = {**PREV, "as_of": "2026-12-20"}
    assert b.decide_year_ago_carry(prev, b.year_ago_fye("2025-12-31", "2027-01-05")) is None
