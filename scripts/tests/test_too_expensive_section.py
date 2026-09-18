"""v5.1（2026-09-18）「③b 太貴不入池」——其他資格全過、只有估值紅的名字要列出來給持有者看。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))

from engine import grp  # noqa: E402
from test_grp_v5 import _v5_stock  # noqa: E402


def test_pass_ex_valuation_true_when_only_valuation_red():
    s = _v5_stock()
    s["live_peg"] = 3.0
    g = grp.grp_score(s)
    assert g["pass"] is False
    assert g["veto_valuation"] is True
    assert g["pass_ex_valuation"] is True


def test_pass_ex_valuation_false_when_another_gate_fails():
    s = _v5_stock()
    s["live_peg"] = 3.0
    s["short_interest_pct_float"] = 15.0
    g = grp.grp_score(s)
    assert g["pass"] is False
    assert g["pass_ex_valuation"] is False


def test_too_expensive_rows_lists_only_valuation_rejects_sorted_by_revision():
    import build_arena as ba
    def row(t, rev, pass_, pass_ex):
        return {"ticker": t, "implied_growth_pct": None,
                "grp": {"pass": pass_, "pass_ex_valuation": pass_ex, "rev_used_pct": rev, "own": {"raw": {"ey": None}}}}
    rows = [row("A", 5.0, True, True),      # 合格，不列
            row("B", 8.0, False, True),     # 只差估值
            row("C", 20.0, False, True),    # 只差估值，上修更高，排前
            row("D", 30.0, False, False)]   # 別的閘也沒過，不列
    assert [r["ticker"] for r in ba.too_expensive_rows(rows)] == ["C", "B"]
