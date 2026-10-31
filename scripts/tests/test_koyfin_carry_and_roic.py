"""2026-10-31 LLY 品質閘誤判事故的兩道修正：
  A. Koyfin 當天 roic／fcf 空白時沿用 10 天內的前值（load_eps_estimates_xlsx.KoyfinCarry、
     resolve_koyfin_roic_fcf）。
  B. fundamentals_us.calc_roic：年報營業利益 <=0 但稅前淨利 >0 視為 yfinance 錯值，改走
     operatingMargins × totalRevenue 後備路徑；真虧損仍判不過。
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


# ── B. calc_roic ─────────────────────────────────────────────────────────────
class _FakeTicker:
    def __init__(self, op_inc, pretax, tax=5.0, ic=100.0):
        self.balance_sheet = pd.DataFrame({"2025": [ic]}, index=["Invested Capital"])
        self.income_stmt = pd.DataFrame(
            {"2025": [op_inc, tax, pretax]},
            index=["Operating Income", "Tax Provision", "Pretax Income"])


def test_calc_roic_bad_operating_income_uses_fallback():
    # LLY 型：年報營業利益 -5.71（錯值）、稅前淨利 257 → 走 operatingMargins × totalRevenue
    t = _FakeTicker(op_inc=-5.71, pretax=257.0)
    info = {"operatingMargins": 0.5, "totalRevenue": 100.0}
    assert abs(fu.calc_roic(t, info) - 0.5 * 100 * (1 - 0.21) / 100.0) < 1e-9


def test_calc_roic_real_loss_still_fails():
    # 真虧損：營業利益與稅前淨利皆 <=0 → 不走新分支，ROIC 為負
    t = _FakeTicker(op_inc=-20.0, pretax=-25.0)
    info = {"operatingMargins": -0.2, "totalRevenue": 100.0}
    r = fu.calc_roic(t, info)
    assert r is not None and r < 0


def test_calc_roic_bad_op_inc_but_margin_negative_still_fails():
    # 錯值判定後走後備路徑；若 operatingMargins 也是負的，結果仍是負
    t = _FakeTicker(op_inc=-5.0, pretax=50.0)
    info = {"operatingMargins": -0.1, "totalRevenue": 100.0}
    assert fu.calc_roic(t, info) < 0


def test_calc_roic_normal_unchanged():
    t = _FakeTicker(op_inc=60.0, pretax=50.0, tax=10.0)   # 稅率 20%
    assert abs(fu.calc_roic(t, {}) - 60.0 * 0.8 / 100.0) < 1e-9
