#!/usr/bin/env python3
"""dd2 `normalize_v20` 的 eps_meta.base_eps_path 形狀修正（2026-09-23 AMD opus 判斷）。
只改形狀：基期鍵補 A、陣列改用事實表共識重建；不補判斷值。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dd2"))
import run  # noqa: E402

FACTS = {"questions": {"q3_growth": {"facts": [
    {"id": "f_consensus_eps_fy1", "value": 7.58},
    {"id": "f_consensus_eps_fy2", "value": 15.57},
    {"id": "f_consensus_eps_fy3", "value": 22.27},
]}}}


def _obj(path, fy_end=12):
    return {"eps_meta": {"base_eps_path": path, "fy_end_month": fy_end}}


def test_base_key_null_gets_A():
    o = _obj({"FY2025": None, "FY2026E": 7.58, "FY2027E": 15.57, "FY2028E": 22.27})
    o, ch = run.normalize_v20(o, FACTS, "20260923")
    assert o["eps_meta"]["base_eps_path"] == {"FY2025A": None, "FY2026E": 7.58, "FY2027E": 15.57, "FY2028E": 22.27}
    assert len(ch) == 1


def test_four_keys_no_suffix_earliest_gets_A():
    o = _obj({"FY2025": 3.1, "FY2026": 7.58, "FY2027": 15.57, "FY2028": 22.27})
    o, _ = run.normalize_v20(o, FACTS, "20260923")
    assert list(o["eps_meta"]["base_eps_path"]) == ["FY2025A", "FY2026", "FY2027", "FY2028"]


def test_three_forward_keys_untouched():
    path = {"FY2026": 8.49, "FY2027": 10.4, "FY2028": 12.2}  # TXN 形狀，合法
    o, ch = run.normalize_v20(_obj(dict(path)), FACTS, "20260923")
    assert o["eps_meta"]["base_eps_path"] == path and ch == []


def test_list_rebuilt_from_facts_consensus():
    raw = [7.58, 15.3, 21.5, 26.5, 31.0]
    o, ch = run.normalize_v20(_obj(list(raw)), FACTS, "20260923")
    assert o["eps_meta"]["base_eps_path"] == {"FY2026E": 7.58, "FY2027E": 15.57, "FY2028E": 22.27}
    assert o["eps_meta"]["base_eps_path_judge_raw"] == raw
    assert len(ch) == 1


def test_list_non_december_fiscal_year():
    o, _ = run.normalize_v20(_obj([1, 2, 3], fy_end=6), FACTS, "20260923")
    assert list(o["eps_meta"]["base_eps_path"]) == ["FY2027E", "FY2028E", "FY2029E"]


def test_list_left_alone_without_facts():
    o, ch = run.normalize_v20(_obj([1, 2, 3]), None, "20260923")
    assert o["eps_meta"]["base_eps_path"] == [1, 2, 3] and ch == []


def test_digest_targets_prev_quarter_investor_day_and_post_quarter(tmp_path):
    names = ["X_Q3_2026_Earnings_Call_20260428.md", "X_Q4_2026_Earnings_Call_20260728.md",
             "X_Shareholder_Analyst_Call_X_plc_20250522.md", "X_Citi_20260909.md",
             "X_Goldman_20260910.md", "X_A_20260801.md", "X_B_20260802.md", "X_Old_Conf_20250101.md"]
    for n in names:
        (tmp_path / n).write_text("x")
    p = lambda n: str(tmp_path / n)
    ev = {"transcripts": {"selected": {
        "recent_four_quarters": [p(names[0]), p(names[1])],
        "high_signal_optional": [p(names[2]), p(names[7])]}}}
    got = [x.name for x in run._digest_targets(ev)]
    assert got == ["X_Q3_2026_Earnings_Call_20260428.md", "X_Shareholder_Analyst_Call_X_plc_20250522.md",
                   "X_B_20260802.md", "X_Citi_20260909.md", "X_Goldman_20260910.md"]


class _R:
    def __init__(self, rc, out):
        self.returncode, self.stdout, self.stderr = rc, out, ""


def test_koyfin_prefetch_ok_expired_timeout(monkeypatch):
    import subprocess
    monkeypatch.setattr(run.ddreport, "KOYFIN_DOWNLOADER", Path(__file__))  # 存在即可
    monkeypatch.setattr(run.subprocess, "run", lambda *a, **k: _R(0, "  STX: 3 new transcript(s) downloaded\n"))
    assert run._koyfin_prefetch("STX")["new"] == 3
    monkeypatch.setattr(run.subprocess, "run",
                        lambda *a, **k: _R(1, "Koyfin session appears to be expired (redirected to a login page)"))
    assert run._koyfin_prefetch("STX")["status"] == "session_expired"

    def _boom(*a, **k):
        raise subprocess.TimeoutExpired(cmd="x", timeout=1)
    monkeypatch.setattr(run.subprocess, "run", _boom)
    assert run._koyfin_prefetch("STX")["status"] == "timeout"


def test_program_drift_reserves_decision_fields_when_decision_out_has_no_verdict(tmp_path):
    import json, types
    (tmp_path / "parts").mkdir()
    (tmp_path / "parts" / "prior.json").write_text(json.dumps({"prior_dd": {
        "dca_verdict": "進場", "dca_role": "核心", "price_at_dd": 100, "prior_meta": {"ma": "✅"}}}))
    ctx = types.SimpleNamespace(run_dir=tmp_path, ticker="T", date="20260924")
    run._ma_label = lambda c: "🟡"
    run._current_price = lambda c: 110
    obj = {"decision_out": {"exec_line": "分批"}, "counter_evidence": {"contradictions": []}}
    obj, _ = run.program_drift_entries(ctx, obj, decision_out=None)
    assert {"dca_verdict", "dca_role"} <= set(obj["counter_evidence"]["contradictions"][0]["prior_field"])
