"""dd_screener_quality.yf_symbol：站內代號 → yfinance 代號（無網路）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd_screener_quality import yf_symbol  # noqa: E402


def test_eu_and_override():
    assert yf_symbol("LVMH") == "MC.PA"
    assert yf_symbol("RMS") == "RMS.PA"
    assert yf_symbol("AENA") == "AENA.MC"
    assert yf_symbol("BESI") == "BESI.AS"
    assert yf_symbol("ABB") == "ABBNY"


def test_koyfin_dash_suffix_to_dot():
    for src, want in [("5246-KL", "5246.KL"), ("3081-TWO", "3081.TWO"), ("6857-T", "6857.T"),
                      ("LYC-AX", "LYC.AX"), ("VACN-SW", "VACN.SW"), ("2330-TW", "2330.TW")]:
        assert yf_symbol(src) == want


def test_dotted_exchange_kept_and_class_share_dashed():
    for t in ["5246.KL", "6857.T", "LYC.AX", "VACN.SW", "3081.TWO", "NVDA", "BRK-B"]:
        assert yf_symbol(t) == t
    assert yf_symbol("BRK.B") == "BRK-B"
