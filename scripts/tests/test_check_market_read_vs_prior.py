"""check_market_read 第 12 項：vs_prior_zh 第一句必須是白話結論。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_market_read as critic  # noqa: E402


def test_plain_lead_passes():
    status, _ = critic.check_vs_prior_lead({"vs_prior_zh": "上期的看法大多被這週的證據撐住：升息已被市場定價，長債壓力都更明顯。證偽表十條有一條觸發。"})
    assert status == critic.PASS


def test_ledger_lead_fails():
    status, detail = critic.check_vs_prior_lead({"vs_prior_zh": "對上期（2026-09-07）負責：八張命題全數未到期。後面是明細。"})
    assert status == critic.FAIL
    assert "記帳語" in detail


def test_long_lead_fails():
    status, detail = critic.check_vs_prior_lead({"vs_prior_zh": "上期" * 40 + "。"})
    assert status == critic.FAIL
    assert "超過" in detail


def test_missing_is_warn():
    assert critic.check_vs_prior_lead({})[0] == critic.WARN


def test_registered_in_checks():
    assert "vs_prior_lead" in [name for name, _, _ in critic.CHECKS]
