#!/usr/bin/env python3
"""dd_scenario 估值依賴型判定（re-rate 貢獻 ≥ Base 不含息合計 40%）。
2026-09-23 STX：re-rate 與合計都是負的，比值負負得正被誤標；兩者都要 > 0 才算。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dd_scenario  # noqa: E402


def _data(base_eps, base_pe):
    s = lambda eps, pe: {"eps_path": [eps], "terminal_pe": pe, "p": 1 / 3}
    return {"price": 100.0, "start": {"eps": 5.0, "pe": 20.0},
            "scenarios": {"bull": s(10, 25), "base": s(base_eps, base_pe), "bear": s(3, 10)}}


def test_negative_rerate_and_negative_total_not_dependent():
    # EPS 5→6（+3.7%/yr）、PE 20→10（−12.9%/yr）→ 合計負
    assert dd_scenario.compute(_data(6.0, 10.0))["valuation_dependent"] is False


def test_positive_rerate_majority_is_dependent():
    # EPS 5→5.5、PE 20→30：報酬大半靠倍數擴張
    assert dd_scenario.compute(_data(5.5, 30.0))["valuation_dependent"] is True


def test_eps_driven_not_dependent():
    # EPS 5→10、PE 20→21：倍數貢獻小
    assert dd_scenario.compute(_data(10.0, 21.0))["valuation_dependent"] is False


def test_negative_rerate_positive_total_not_dependent():
    assert dd_scenario.compute(_data(12.0, 15.0))["valuation_dependent"] is False


def test_appb_cjk_halfwidth_punct_converted():
    import gen_dd_tables
    facts = {"findings_digest": [{"direction": "+", "claim": "需求強勁.", "source": "Gartner 新聞稿, https://x.com/a.b",
                                  "as_of": "2026-09-01"}]}
    out = gen_dd_tables.render_v19_appB_html(facts)
    assert "新聞稿， https://x.com/a.b" in out and "強勁。" in out
