"""v5.5（2026-10-18 持有人拍板，不另做回測）：美股看板與十倍股頁的品質閘現金流條件
從「FCF margin ≥10%（ROIC ≥25% 時只要 ≥0）」改成「FCF > 0」，ROIC ≥15% 不變；台股席位頁維持原規則。

grp.quality_gate(s) 預設走新規則；台股列帶 s["_quality_rule"] = "margin10"（build_seats_tw.tw_row
設定）就維持舊規則。本檔驗：
  - 美股（預設）：FCF 0 → 不過、0.1 → 過、−1 → 不過、缺 → 不過；ROIC 14.9 → 不過；
    ROIC 26 ∧ FCF 3 → 過但不是豁免；ROIC／FCF 皆缺 → pass=None（金融另軌）
  - 舊規則（margin10）：利潤率 9.9 ∧ ROIC 20 → 不過；10.0 → 過；ROIC 26 ∧ 3 → 過且標豁免；ROIC 26 ∧ −1 → 不過
  - 台股 tw_row：OCF 9.9 ∧ ROIC 20 → 不過；OCF 3 ∧ ROIC 26 → 過（原豁免）；即使 FCF 欄為正也只看 OCF
  - 美股 row_dict：同一檔 FCF 5 ∧ ROIC 20，美股列過、台股 tw_row 不過
純手工輸入，不讀磁碟資料、不連網。
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from engine import build_arena as ba  # noqa: E402
from engine import grp  # noqa: E402
import build_seats_tw as tw  # noqa: E402


def _us(roic, fcf, **kw):
    s = {"roic": roic, "fcf": fcf}
    s.update(kw)
    return s


def _legacy(roic, fcf):
    return {"roic": roic, "fcf": fcf, grp.QUALITY_RULE_KEY: grp.Q_RULE_MARGIN10}


# ── 美股新規則（預設）────────────────────────────────────────────────────────

def test_us_fcf_exactly_zero_fails():
    q = grp.quality_gate(_us(20.0, 0.0))
    assert q["pass"] is False
    assert any("品質閘 FCF" in w for w in q["why"])


def test_us_fcf_slightly_positive_passes():
    q = grp.quality_gate(_us(20.0, 0.1))
    assert q["pass"] is True and q["exempt"] is False and q["why"] == []


def test_us_fcf_negative_fails():
    assert grp.quality_gate(_us(20.0, -1.0))["pass"] is False


def test_us_fcf_missing_fails_with_reason():
    q = grp.quality_gate(_us(20.0, None))
    assert q["pass"] is False and any("品質閘 FCF 缺" in w for w in q["why"])


def test_us_roic_14_9_fails_even_with_big_fcf():
    q = grp.quality_gate(_us(14.9, 30.0))
    assert q["pass"] is False and any("品質閘 ROIC" in w for w in q["why"])


def test_us_roic_exactly_15_passes():
    assert grp.quality_gate(_us(15.0, 0.1))["pass"] is True


def test_us_low_fcf_margin_now_passes_and_is_not_exempt():
    # 舊規則下 FCF 5 不過；ROIC 26 ∧ FCF 3 是豁免。新規則兩者都是一般通過。
    assert grp.quality_gate(_us(20.0, 5.0))["pass"] is True
    q = grp.quality_gate(_us(26.0, 3.0))
    assert q["pass"] is True and q["exempt"] is False


def test_us_high_roic_negative_fcf_fails_no_exemption():
    assert grp.quality_gate(_us(40.0, -0.5))["pass"] is False


def test_us_both_missing_is_other_track():
    q = grp.quality_gate(_us(None, None))
    assert q["pass"] is None


# ── 舊規則（margin10）行為不變 ───────────────────────────────────────────────

def test_legacy_ocf_9_9_with_roic_20_fails():
    q = grp.quality_gate(_legacy(20.0, 9.9))
    assert q["pass"] is False and any("品質閘 FCF" in w for w in q["why"])


def test_legacy_threshold_10_passes():
    assert grp.quality_gate(_legacy(20.0, 10.0))["pass"] is True


def test_legacy_exemption_roic_26_ocf_3():
    q = grp.quality_gate(_legacy(26.0, 3.0))
    assert q["pass"] is True and q["exempt"] is True


def test_legacy_exemption_needs_nonnegative():
    assert grp.quality_gate(_legacy(26.0, -1.0))["pass"] is False
    assert grp.quality_gate(_legacy(24.9, 3.0))["pass"] is False


# ── 台股 tw_row 走舊規則，美股 row_dict 走新規則 ─────────────────────────────

def _tw_stock(roic, ocf, fcf=-5.0):
    return {"ticker": "1111.TW", "name": "TEST", "roic": roic, "fcf": fcf, "ocf": ocf,
            "eps_fy1_fy3_cagr_pct": 20.0, "eps_fy_curr": 10, "eps_fy_next": 12, "eps_fy3": 14.4,
            "ma": {"above_w52": True, "dist_ath_pct": -1.0, "vs_200ma_pct": 5.0, "price": 100},
            "timing": {"dist_52w_high_pct": -1.0}, "last_earnings_date": "2026-08-10"}


def test_tw_row_ocf_9_9_roic_20_fails():
    r = tw.tw_row(_tw_stock(20.0, 9.9))
    assert r["grp"]["quality"]["pass"] is False
    assert r["grp"]["pass"] is False
    assert any("營業現金流利潤率" in w for w in r["grp"]["why"])


def test_tw_row_ocf_3_roic_26_passes_by_exemption():
    r = tw.tw_row(_tw_stock(26.0, 3.0))
    assert r["grp"]["quality"]["pass"] is True and r["grp"]["quality"]["exempt"] is True
    assert r["grp"]["pass"] is True


def test_tw_row_ignores_fcf_column():
    # FCF 欄為正、OCF 不到 10%：台股只看 OCF，所以不過
    assert tw.tw_row(_tw_stock(20.0, 5.0, fcf=30.0))["grp"]["pass"] is False


def test_tw_row_does_not_mutate_input():
    s0 = _tw_stock(20.0, 20.0)
    tw.tw_row(s0)
    assert grp.QUALITY_RULE_KEY not in s0


def test_same_numbers_us_passes_tw_fails():
    s = _tw_stock(20.0, 5.0, fcf=5.0)
    assert ba.row_dict(dict(s))["grp"]["quality"]["pass"] is True     # 美股新規則：FCF 5 > 0
    assert tw.tw_row(s)["grp"]["quality"]["pass"] is False             # 台股舊規則：OCF 5 < 10


# ── 美股說明文字 ─────────────────────────────────────────────────────────────

def test_us_fail_chip_says_must_exceed_zero():
    chip = ba._match_chip("品質閘 FCF -3.2")
    assert chip is not None and chip[0] == "FCF 率 -3.2%，需大於 0"
