"""2026-10-31 LLY 品質閘誤判事故的兩道修正：
  A. Koyfin 當天 roic／fcf 空白時沿用 10 天內的前值（load_eps_estimates_xlsx.KoyfinCarry、
     resolve_koyfin_roic_fcf）。
  B. fundamentals_us._row：先找完全同名的列，避免「Operating Income」抓到排在前面的
     「Other Non Operating Income Expenses」。
純假資料，不讀磁碟 xlsx、不連網。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import fundamentals_us as fu  # noqa: E402
from load_eps_estimates_xlsx import (  # noqa: E402
    ExcelSnapshot,
    KoyfinCarry,
    resolve_koyfin_roic_fcf,
)

FAM = "DD_universe_EPS_estimates_"


def _make_dir(tmp_path, dates):
    for d in dates:
        (tmp_path / f"{FAM}{d}.xlsx").write_bytes(b"")
    return tmp_path


def _carry(tmp_path, snaps: dict, today="2026-10-31"):
    """snaps: {'YYYYMMDD': {ticker: record}}；用假 loader 取代讀 xlsx。"""
    _make_dir(tmp_path, snaps.keys())

    def loader(path):
        d = path.stem[-8:]
        return ExcelSnapshot(snapshot_date=f"{d[:4]}-{d[4:6]}-{d[6:]}",
                             source_file=path.name, tickers=snaps[d])
    return KoyfinCarry([FAM], today, data_dir=tmp_path, loader=loader)


LLY_TODAY = {"roic_pct": None, "fcf_margin_pct": None, "roic_5y_avg_pct": 33.91}


def test_carry_hit_within_10_days(tmp_path):
    c = _carry(tmp_path, {"20261030": {"LLY": {"roic_pct": 40.06, "fcf_margin_pct": 22.83}}})
    roic, fcf, carried, stamp = resolve_koyfin_roic_fcf(LLY_TODAY, c, "LLY")
    assert (roic, fcf) == (40.06, 22.83)
    assert carried == ["roic", "fcf"]
    assert stamp == "2026-10-30"


def test_carry_boundary_10_days_in_11_days_out(tmp_path):
    c = _carry(tmp_path, {"20261021": {"LLY": {"roic_pct": 40.0, "fcf_margin_pct": 20.0}}})
    assert resolve_koyfin_roic_fcf(LLY_TODAY, c, "LLY")[0] == 40.0  # 恰好 10 天
    sub = tmp_path / "b"
    sub.mkdir()
    c2 = _carry(sub, {"20261020": {"LLY": {"roic_pct": 40.0, "fcf_margin_pct": 20.0}}})
    roic, fcf, carried, stamp = resolve_koyfin_roic_fcf(LLY_TODAY, c2, "LLY")  # 11 天
    assert (roic, fcf, carried, stamp) == (None, None, [], None)


def test_no_carry_when_today_row_missing(tmp_path):
    c = _carry(tmp_path, {"20261030": {"LLY": {"roic_pct": 40.06, "fcf_margin_pct": 22.83}}})
    assert resolve_koyfin_roic_fcf(None, c, "LLY") == (None, None, [], None)


def test_only_one_field_missing_other_uses_today(tmp_path):
    c = _carry(tmp_path, {"20261030": {"LLY": {"roic_pct": 40.06, "fcf_margin_pct": 22.83}}})
    today = {"roic_pct": 35.0, "fcf_margin_pct": None}
    roic, fcf, carried, stamp = resolve_koyfin_roic_fcf(today, c, "LLY")
    assert roic == 35.0            # 今天值，不被前值蓋掉
    assert fcf == 22.83
    assert carried == ["fcf"]
    assert stamp == "2026-10-30"


def test_carry_takes_most_recent_nonblank_per_field(tmp_path):
    c = _carry(tmp_path, {
        "20261030": {"LLY": {"roic_pct": None, "fcf_margin_pct": 22.0}},
        "20261029": {"LLY": {"roic_pct": 41.0, "fcf_margin_pct": 21.0}},
    })
    roic, fcf, carried, stamp = resolve_koyfin_roic_fcf(LLY_TODAY, c, "LLY")
    assert (roic, fcf) == (41.0, 22.0)
    assert stamp == "2026-10-29"   # 兩欄來自不同天時標較舊那天


def test_other_family_and_today_file_ignored(tmp_path):
    (tmp_path / "DD_universe_EPS_supplement_20261030.xlsx").write_bytes(b"")
    c = _carry(tmp_path, {"20261031": {"LLY": {"roic_pct": 99.0, "fcf_margin_pct": 99.0}}})
    # 當天（20261031）檔不算前值；supplement 檔名不符族別
    assert resolve_koyfin_roic_fcf(LLY_TODAY, c, "LLY")[2] == []


def test_previous_files_loaded_once(tmp_path):
    _make_dir(tmp_path, ["20261030", "20261029"])
    calls = []

    def loader(path):
        calls.append(path.name)
        return ExcelSnapshot("2026-10-30", path.name, {"A": {"roic_pct": None}})
    c = KoyfinCarry([FAM], "2026-10-31", data_dir=tmp_path, loader=loader)
    for t in ("A", "B", "C"):
        c.lookup(t, "roic_pct")
        c.lookup(t, "fcf_margin_pct")
    assert len(calls) == 2


# ── B. _row 完全同名優先 ─────────────────────────────────────────────────────
class _FakeTicker:
    def __init__(self, rows, ic=100.0):
        self.balance_sheet = pd.DataFrame({"2025": [ic]}, index=["Invested Capital"])
        self.income_stmt = pd.DataFrame({"2025": list(rows.values())}, index=list(rows.keys()))


def test_row_prefers_exact_over_substring():
    # MRK 2025 實際排列：營業外收支排在營業利益前面
    t = _FakeTicker({"Other Non Operating Income Expenses": 8.18, "Pretax Income": 210.67,
                     "Tax Provision": 28.04, "Operating Income": 221.07})
    assert fu._row(t.income_stmt, "Operating Income") == 221.07


def test_row_substring_fallback_when_no_exact():
    t = _FakeTicker({"Total Operating Income As Reported": 5.0})
    assert fu._row(t.income_stmt, "Operating Income") == 5.0


def test_calc_roic_uses_real_operating_income():
    t = _FakeTicker({"Other Non Operating Income Expenses": -5.71, "Pretax Income": 257.31,
                     "Tax Provision": 50.91, "Operating Income": 300.0}, ic=690.38)
    eff = 50.91 / 257.31
    assert abs(fu.calc_roic(t, {}) - 300.0 * (1 - eff) / 690.38) < 1e-9


def test_calc_roic_real_loss_still_negative():
    t = _FakeTicker({"Operating Income": -20.0, "Pretax Income": -25.0, "Tax Provision": 0.0})
    r = fu.calc_roic(t, {"operatingMargins": -0.2, "totalRevenue": 100.0})
    assert r is not None and r < 0
