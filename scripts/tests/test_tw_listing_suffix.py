"""TW code -> listing resolution (scripts/tw_listing_suffix.py), no network.

2026-10-10: the 興櫃 roster sits between the TPEx roster and the yfinance
probe, so emerging-board names get their Chinese name and industry instead of
falling through to the probe.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import tw_listing_suffix as tls  # noqa: E402

ROWS = {
    tls.TWSE_LISTED_URL: [{"公司代號": "2330", "公司簡稱": "台積電", "產業別": "24"},
                          {"公司代號": "2891", "公司簡稱": "中信金", "產業別": "17"}],
    tls.TPEX_LISTED_URL: [{"SecuritiesCompanyCode": "5274", "CompanyAbbreviation": "信驊",
                           "SecuritiesIndustryCode": "24"}],
    tls.TPEX_EMERGING_URL: [{"SecuritiesCompanyCode": "7924", "CompanyAbbreviation": "TLC-KY",
                             "SecuritiesIndustryCode": "22"},
                            {"SecuritiesCompanyCode": "9999", "CompanyAbbreviation": "未知業",
                             "SecuritiesIndustryCode": "99"}],
}


class _Resp:
    def __init__(self, rows):
        self._rows = rows

    def json(self):
        return self._rows


@pytest.fixture
def offline(monkeypatch):
    import requests
    probed = []
    monkeypatch.setattr(requests, "get", lambda url, **kw: _Resp(ROWS[url]))
    monkeypatch.setattr(tls, "_probe_yfinance",
                        lambda c: probed.append(c) or (f"{c}.TWO" if c == "8888" else None))
    return probed


def test_each_roster_sets_suffix_market_name_and_industry(offline):
    resolved, unresolved = tls.resolve_tw_codes(["2330", "5274", "7924", "2891"])
    assert resolved["2330"] == {"ticker": "2330.TW", "name": "台積電", "market": "TWSE",
                                "industry": "半導體業"}
    assert resolved["5274"] == {"ticker": "5274.TWO", "name": "信驊", "market": "TPEx",
                                "industry": "半導體業"}
    assert resolved["7924"] == {"ticker": "7924.TWO", "name": "TLC-KY",
                                "market": "TPEx-emerging", "industry": "生技醫療業"}
    assert resolved["2891"]["industry"] == "金融保險業"
    assert unresolved == [] and offline == []          # nothing reached the probe


def test_unknown_industry_code_is_none(offline):
    resolved, _ = tls.resolve_tw_codes(["9999"])
    assert resolved["9999"]["industry"] is None


def test_probe_only_for_codes_on_no_roster(offline):
    resolved, unresolved = tls.resolve_tw_codes(["8888", "7777"])
    assert resolved["8888"] == {"ticker": "8888.TWO", "name": "8888.TWO", "market": "probe",
                                "industry": None}
    assert unresolved == ["7777"] and offline == ["7777", "8888"]
