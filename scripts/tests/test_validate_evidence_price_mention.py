"""validate_evidence.PRICE_MENTION_RE：只抓股價「現價 $N」，不抓商品實現價與帶單位的價格（2026-11-03 VALE）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_evidence as ve  # noqa: E402


def _hits(text):
    return [m.group(1) for m in ve.PRICE_MENTION_RE.finditer(text)]


def test_share_price_mentions_still_caught():
    assert _hits("現價約 $234，財報後") == ["234"]
    assert _hits("trading at $164.17 today") == ["164.17"]
    assert _hits("現價 $1,296.2") == ["1,296.2"]


def test_commodity_realized_price_and_unit_prices_ignored():
    assert _hits("3Q26 鐵礦砂粉平均實現價 $85/t，年減 10%") == []
    assert _hits("金價現價 $2,400/oz") == []
