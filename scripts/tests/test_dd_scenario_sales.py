#!/usr/bin/env python3
"""sales_multiple 模式（2026-10-12，CRWV 案，持有人拍板）：虧損公司情境樹改走「營收路徑 × 終端 EV/S」。

涵蓋：手算對帳、終端權益 ≤ 0 歸零且不拋例外、拆解欄位、validate 排序、觸發判定（FY1 EPS ≤ 0／> 0）、
eps_pe 模式與改前逐位相同（fixtures/dd_scenario_regress 是改前的真實 v20 scenario.json 與當時
腳本輸出）、CRWV 原失敗樣本不再拋例外、check_meta 對 sales 重算、gen_dd_tables 能渲染。

Python 3.9 相容。
"""
from __future__ import annotations

import copy
import json
import re
import sys
import types
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))

import dd_scenario  # noqa: E402
import gen_dd_tables  # noqa: E402
from dd2 import run as dd2_run  # noqa: E402
from dd2 import bundle as dd2_bundle  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "dd_scenario_regress"
PRICE = 82.08


def _sales(**over):
    d = {
        "ticker": "CRWV", "date": "2026-10-12", "price": PRICE,
        "valuation_basis": "sales_multiple",
        "start": {"rev": 12870.0, "ev_s": 7.1, "basis": "FY2026E 共識營收；EV÷FY1 營收"},
        "yield_pct": {"dividend": 0.0, "net_buyback": 0.0},
        "terminal_label": "FY2031E",
        "net_debt_now": 46074.0, "shares_now": 551.5,
        "scenarios": {
            "bull": {"rev_path": [14000, 19000, 26000, 34000, 42000], "terminal_ev_s": 7.0,
                     "net_debt_y5": 30000, "shares_y5": 650, "p": 25, "basis": "bull"},
            "base": {"rev_path": [13000, 17000, 21000, 23500, 25000], "terminal_ev_s": 6.0,
                     "net_debt_y5": 30000, "shares_y5": 600, "p": 45, "basis": "base"},
            "bear": {"rev_path": [12500, 15000, 16000, 16500, 17000], "terminal_ev_s": 3.0,
                     "net_debt_y5": 60000, "shares_y5": 700, "p": 30, "basis": "bear"},
        },
    }
    d.update(over)
    return d


# ---- 手算對帳 --------------------------------------------------------------

def test_sales_terminal_price_hand_calc():
    res = dd_scenario.compute(_sales())
    rows = res["rows"]
    # bull: 42000*7 = 294000；−30000 = 264000；÷650
    assert abs(rows["bull"]["terminal_price"] - 264000 / 650) < 1e-9
    # base: 25000*6 = 150000；−30000 = 120000；÷600 = 200
    assert abs(rows["base"]["terminal_price"] - 200.0) < 1e-9
    # bear: 17000*3 = 51000；−60000 = −9000 → 股權為負，歸零
    assert rows["bear"]["terminal_price"] == 0.0
    # 輸出欄：5Y%、IRR、EV、AR
    base5y = (200.0 / PRICE - 1) * 100
    assert abs(rows["base"]["five_y_pct"] - base5y) < 1e-9
    assert abs(rows["base"]["irr_ex_div"] - ((200.0 / PRICE) ** 0.2 - 1) * 100) < 1e-9
    bull5y = (264000 / 650 / PRICE - 1) * 100
    ev = (25 * bull5y + 45 * base5y + 30 * -100.0) / 100
    assert abs(res["ev5y_pct"] - ev) < 1e-9
    assert abs(res["ar"] - (25 * abs(bull5y)) / (30 * 100)) < 1e-9
    assert res["ten_y"] == {}
    assert res["guardrail_diff_pp"] is None


def test_sales_null_net_debt_and_shares_fall_back_to_current():
    d = _sales()
    d["scenarios"]["base"]["net_debt_y5"] = None
    d["scenarios"]["base"]["shares_y5"] = None
    row = dd_scenario.compute(d)["rows"]["base"]
    assert row["net_debt_y5"] == 46074.0 and row["shares_y5"] == 551.5
    assert abs(row["terminal_price"] - (25000 * 6 - 46074) / 551.5) < 1e-9


def test_sales_null_without_current_value_raises_clear_error():
    d = _sales(net_debt_now=None)
    d["scenarios"]["base"]["net_debt_y5"] = None
    try:
        dd_scenario.compute(d)
    except ValueError as exc:
        assert "f_net_debt_m" in str(exc)
    else:
        raise AssertionError("應丟 ValueError")


# ---- 終端權益 ≤ 0：價格歸零、IRR −100、不拋例外 ------------------------------

def test_sales_negative_equity_zero_price_irr_minus_100_no_exception():
    row = dd_scenario.compute(_sales())["rows"]["bear"]
    assert row["terminal_price"] == 0.0
    assert row["five_y_pct"] == -100.0
    assert row["irr_ex_div"] == -100.0
    assert row["rev_contrib"] is None and row["multiple_contrib"] is None


def test_all_three_scenarios_zero_does_not_raise():
    d = _sales()
    for k in ("bull", "base", "bear"):
        d["scenarios"][k]["terminal_ev_s"] = 0.5
        d["scenarios"][k]["net_debt_y5"] = 1e9
    res = dd_scenario.compute(d)
    assert res["ev5y_pct"] == -100.0 and res["ev_annualized_pct"] == -100.0 and abs(res["ar"] - 25 / 30) < 1e-9


# ---- 拆解欄位 ---------------------------------------------------------------

def test_sales_decomposition_fields():
    rows = dd_scenario.compute(_sales())["rows"]
    base = rows["base"]
    want_rev = (((25000 / 600) / (12870.0 / 551.5)) ** 0.2 - 1) * 100
    want_mult = ((6.0 / 7.1) ** 0.2 - 1) * 100
    assert abs(base["rev_contrib"] - want_rev) < 1e-9
    assert abs(base["multiple_contrib"] - want_mult) < 1e-9
    assert "eps_contrib" not in base and "rerate_contrib" not in base
    assert base["ex_div_total"] == base["irr_ex_div"]  # 槓桿下不做恆等式，直接取實際 IRR


def test_sales_valuation_dependent_looks_at_multiple_contribution():
    # Base 倍數由 7.1 擴到 30：倍數貢獻 33.3%/yr ÷ 不含息 IRR 71%/yr ≈ 0.47 ≥ 0.40
    d = _sales()
    d["scenarios"]["base"]["terminal_ev_s"] = 30.0
    assert dd_scenario.compute(d)["valuation_dependent"] is True
    # 倍數收縮（6 < 7.1）→ 負負得正的舊 bug 不得再出現
    assert dd_scenario.compute(_sales())["valuation_dependent"] is False


# ---- validate ---------------------------------------------------------------

def test_sales_validate_passes_on_sound_input_and_orders_terminal_revenue():
    d = _sales()
    res = dd_scenario.compute(d)
    fails, _warns = dd_scenario.validate(d, res)
    assert fails == []
    d["scenarios"]["bull"]["rev_path"] = [14000, 19000, 22000, 23000, 24000]  # 終端 < Base
    fails, _ = dd_scenario.validate(d, dd_scenario.compute(d))
    assert any("終端營收排序不成立" in f for f in fails)


def test_sales_validate_bull_front_two_years_equal_base_is_degenerate():
    d = _sales()
    d["scenarios"]["bull"]["rev_path"][0:2] = d["scenarios"]["base"]["rev_path"][0:2]
    fails, _ = dd_scenario.validate(d, dd_scenario.compute(d))
    assert any("前兩年營收" in f for f in fails)


def test_sales_validate_spread_warn_and_prob_rules():
    d = _sales()
    d["scenarios"]["bull"]["rev_path"] = [14000, 19000, 21000, 24000, 26000]  # 26000/25000 = +4%
    _fails, warns = dd_scenario.validate(d, dd_scenario.compute(d))
    assert any("Bull 終端營收僅高於 Base" in w for w in warns)
    d["scenarios"]["bear"]["p"], d["scenarios"]["base"]["p"] = 15, 60
    fails, _ = dd_scenario.validate(d, dd_scenario.compute(d))
    assert any("p_bear" in f for f in fails) and any("p_base" in f for f in fails)


# ---- build_meta / check_meta / html -----------------------------------------

def test_sales_build_meta_keeps_output_field_names_and_check_meta_roundtrips():
    d = _sales()
    res = dd_scenario.compute(d)
    meta = dd_scenario.build_meta(d, res)
    for key in ("bull_5y_price", "bear_5y_price", "p_bull_pct", "p_bear_pct", "upside_5y_pct",
                "ev5y_pct", "irr_base_pct", "asym_ratio", "scenario_tree"):
        assert key in meta
    assert meta["bear_5y_price"] == 0.0
    assert meta["scenario_tree"]["valuation_basis"] == "sales_multiple"
    assert "eps" not in meta["scenario_tree"]
    meta["price_at_dd"] = PRICE
    fails, _warns = dd_scenario.check_meta(meta)
    assert fails == []
    meta["bull_5y_price"] = 999.0
    fails, _ = dd_scenario.check_meta(meta)
    assert any("bull_5y_price 對不上" in f for f in fails)


def test_sales_html_and_table_render():
    d = _sales()
    res = dd_scenario.compute(d)
    html = dd_scenario.build_html(d, res)
    assert "終端 EV/S" in html and "起點" in html and "42,000" in html and "—" in html
    assert re.search(r"<td>Bear</td>.*?<td>0\.0</td>", html, re.S)


# ---- 觸發判定 ---------------------------------------------------------------

def _ctx(tmp_path, fy1):
    facts = {"meta": {"ticker": "T", "date": "2026-10-12", "schema": "facts-v1"},
             "questions": {"q5_valuation": {"facts": []}}, "findings_digest": []}
    if fy1 is not None:
        facts["questions"]["q5_valuation"]["facts"].append(
            {"id": "f_consensus_eps_fy1", "value": fy1, "label": "x", "unit": "USD/share"})
    (tmp_path / "facts.json").write_text(json.dumps(facts), encoding="utf-8")
    return types.SimpleNamespace(run_dir=tmp_path, ticker="T", date="20261012", manifest={}, save=lambda: None)


def test_trigger_fy1_eps_nonpositive_is_sales_multiple(tmp_path):
    for v in (-3.94, 0, 0.0):
        ctx = _ctx(tmp_path, v)
        assert dd2_run.decide_valuation_basis(ctx) == "sales_multiple"
        assert ctx.manifest["valuation_basis"] == "sales_multiple"
        assert dd2_bundle.valuation_basis_of(tmp_path) == "sales_multiple"


def test_trigger_fy1_eps_positive_or_missing_is_eps_pe(tmp_path):
    for v in (0.01, 12.79, None):
        ctx = _ctx(tmp_path, v)
        assert dd2_run.decide_valuation_basis(ctx) == "eps_pe"
        assert dd2_bundle.valuation_basis_of(tmp_path) == "eps_pe"


def test_judge_valuation_basis_always_overridden_and_logged(tmp_path):
    ctx = _ctx(tmp_path, -3.94)
    obj = {"scenario_inputs": {"valuation_basis": "eps_pe"}}
    dd2_run._valuation_basis_override(ctx, obj)
    assert obj["scenario_inputs"]["valuation_basis"] == "sales_multiple"
    assert ctx.manifest["mechanical_overrides"] == [
        {"path": "$.scenario_inputs.valuation_basis", "judge": "eps_pe", "program": "sales_multiple"}]
    # eps_pe 且判斷者沒填：不加欄位、不記覆寫（現行判斷檔形狀不變）
    ctx2 = _ctx(tmp_path, 5.0)
    obj2 = {"scenario_inputs": {"eps": {}}}
    dd2_run._valuation_basis_override(ctx2, obj2)
    assert "valuation_basis" not in obj2["scenario_inputs"] and "mechanical_overrides" not in ctx2.manifest
    # eps_pe 但判斷者誤填 sales_multiple → 被改回
    obj3 = {"scenario_inputs": {"valuation_basis": "sales_multiple"}}
    dd2_run._valuation_basis_override(ctx2, obj3)
    assert obj3["scenario_inputs"]["valuation_basis"] == "eps_pe"


def test_judge_tail_shape_switches_with_basis():
    eps_tail = dd2_bundle._judge_tail_section(Path("/x/judgment.json"))
    assert '"pe": {"bull"' in eps_tail and "sales_multiple" not in eps_tail
    sales_tail = dd2_bundle._judge_tail_section(Path("/x/judgment.json"), valuation_basis="sales_multiple")
    assert '"net_debt_y5"' in sales_tail and '"ev_s"' in sales_tail and '"second_stage"' not in sales_tail


# ---- project：scenario_inputs → scenario.json -------------------------------

def _judgment_sales():
    return {
        "meta": {"ticker": "CRWV", "date": "2026-10-12"},
        "scenario_inputs": {
            "valuation_basis": "sales_multiple", "terminal_label": "FY2031E",
            "start": {"rev": 12870.0, "ev_s": 7.1, "basis": "b"},
            "rev": {"bull": [1, 2, 3, 4, 5], "base": [1, 2, 3, 4, 4], "bear": [1, 1, 1, 1, 1]},
            "ev_s": {"bull": 7, "base": 6, "bear": 3},
            "net_debt_y5": {"bull": 1, "base": None, "bear": 3},
            "shares_y5": {"bull": 10, "base": 10, "bear": None},
            "p": {"bull": 25, "base": 45, "bear": 30},
            "basis": {"bull": "a", "base": "b", "bear": "c"},
        },
    }


def test_dd_project_scenario_input_carries_sales_fields():
    import dd_project
    facts = {"questions": {"q5_valuation": {"facts": [
        {"id": "f_price_at_dd", "value": PRICE}, {"id": "f_net_debt_m", "value": 46074.0},
        {"id": "f_shares_diluted_m", "value": 551.5}]}}}
    out = dd_project.scenario_input_from_v19(_judgment_sales(), facts)
    assert out["valuation_basis"] == "sales_multiple" and out["price"] == PRICE
    assert out["net_debt_now"] == 46074.0 and out["shares_now"] == 551.5
    assert out["scenarios"]["bull"] == {"rev_path": [1, 2, 3, 4, 5], "terminal_ev_s": 7, "net_debt_y5": 1,
                                       "shares_y5": 10, "p": 25, "basis": "a"}
    assert out["scenarios"]["base"]["net_debt_y5"] is None
    assert out["start"]["rev"] == 12870.0


# ---- validate_judgment 條件式必填 -------------------------------------------

def test_scenario_basis_checks_conditional_required():
    import validate_judgment as vj
    ok_sales = _judgment_sales()
    assert vj.scenario_basis_checks(ok_sales) == []
    bad = copy.deepcopy(ok_sales)
    del bad["scenario_inputs"]["rev"]
    assert any("缺 rev" in f for f in vj.scenario_basis_checks(bad))
    # eps_pe 模式缺 eps／pe 仍要擋
    eps_missing = {"scenario_inputs": {"terminal_label": "FY2031E", "p": {}, "max_dd": {}}}
    fails = vj.scenario_basis_checks(eps_missing)
    assert any("缺 eps" in f for f in fails) and any("缺 pe" in f for f in fails)


# ---- 回歸：eps_pe 結果與改前逐位相同 ----------------------------------------

def _run_cli(scen_path, tmp_path, name):
    meta, html = tmp_path / (name + ".meta.json"), tmp_path / (name + ".html")
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = dd_scenario.main([str(scen_path), "--meta", str(meta), "--html", str(html)])
    out = "\n".join(l for l in buf.getvalue().splitlines() if not l.startswith("已寫 "))
    return rc, meta.read_text(encoding="utf-8"), html.read_text(encoding="utf-8"), out


def test_eps_pe_outputs_bit_identical_to_pre_change_fixtures(tmp_path):
    names = sorted(p.name[:-len(".scenario.json")] for p in FIX.glob("*_2026*.scenario.json")
                   if "eps_failed" not in p.name)
    assert len(names) >= 4
    for name in names:
        rc, meta, html, out = _run_cli(FIX / (name + ".scenario.json"), tmp_path, name)
        want_out = "\n".join(l for l in (FIX / (name + ".expected_stdout.txt")).read_text(encoding="utf-8").splitlines()
                             if not l.startswith("已寫 "))
        assert rc == 0, name
        assert meta == (FIX / (name + ".expected_meta.json")).read_text(encoding="utf-8"), name
        assert html == (FIX / (name + ".expected.html")).read_text(encoding="utf-8"), name
        assert out == want_out, name


def test_eps_pe_pe_zero_and_negative_eps_no_longer_raise():
    """CRWV 原失敗樣本（eps_pe 欄位）：起點 EPS −3.94、pe=null、Bear 終端 EPS<0 且 pe=0。"""
    data = json.loads((FIX / "CRWV_20261012.eps_failed.scenario.json").read_text(encoding="utf-8"))
    res = dd_scenario.compute(data)
    rows = res["rows"]
    assert abs(rows["bull"]["terminal_price"] - 6.8 * 28) < 1e-9
    assert abs(rows["base"]["terminal_price"] - 4.0 * 22) < 1e-9
    assert rows["bear"]["terminal_price"] == 0.0
    assert rows["bear"]["five_y_pct"] == -100.0 and rows["bear"]["irr_ex_div"] == -100.0
    assert rows["base"]["eps_contrib"] is None  # 起點 EPS 為負，拆解不成立
    assert res["guardrail_diff_pp"] is None
    # 表格與 html 對 None 欄位不拋例外
    dd_scenario.build_html(data, res)
    dd_scenario.build_meta(data, res)


# ---- gen_dd_tables 渲染 -----------------------------------------------------

def test_gen_dd_tables_scenario_tree_renders_sales_mode():
    d = _sales()
    meta = dd_scenario.build_meta(d, dd_scenario.compute(d))
    html = gen_dd_tables.render_v19_scenario_tree_html(meta)
    assert html and 'id="stree"' in html
    assert "起點營收 12,870" in html and "7.1x" in html     # 起點列
    assert "營收 年1" in html and "42,000" in html            # 逐年營收
    assert "終端 EV/S" in html and "終端淨負債" in html and "60,000" in html and "700" in html
    assert "股權價值為負時歸零" in html


def test_gen_dd_tables_scenario_tree_eps_mode_unchanged():
    data = json.loads((FIX / "AMAT_20261012.scenario.json").read_text(encoding="utf-8"))
    meta = dd_scenario.build_meta(data, dd_scenario.compute(data))
    html = gen_dd_tables.render_v19_scenario_tree_html(meta)
    assert "終端倍數" in html and "終端 EV/S" not in html


# ---- QC-48 Bull 區段 ---------------------------------------------------------

def test_qc48_bull_section_sales_uses_price_as_start(tmp_path):
    d = _sales()
    meta = dd_scenario.build_meta(d, dd_scenario.compute(d))
    (tmp_path / "scenario_meta.json").write_text(json.dumps(meta), encoding="utf-8")
    (tmp_path / "scenario.json").write_text(json.dumps(d), encoding="utf-8")
    text = dd2_bundle._qc48_bull_section(tmp_path)
    assert "sales_multiple" in text and "起始價（判斷日股價）：82.1" in text
    irr = ((264000 / 650 / PRICE) ** 0.2 - 1) * 100
    assert "{0:+.1f}%/yr".format(irr) in text


# ---- dd_facts：capital_structure → 事實 id -----------------------------------

def test_dd_facts_emits_capital_structure_facts_with_new_ids():
    import dd_facts
    numbers = {"price_at_dd": 82.08, "price_as_of": "2026-10-09", "capital_structure": {
        "as_of": "2026-10-12", "currency": "USD", "price_currency": "USD", "fx_mismatch": False,
        "net_debt_m": 46074.0, "total_debt_m": 51613.0, "cash_m": 5539.0, "shares_diluted_m": 551.54,
        "shares_basis": "yfinance impliedSharesOutstanding", "market_cap_m": 45270.12, "ev_m": 91344.12,
        "revenue_consensus": {"fy1": {"avg_m": 12869.75, "analysts": 40, "yf_period": "0y"},
                              "fy2": {"avg_m": 26295.93, "analysts": 40, "yf_period": "+1y"}, "fy3": None},
        "note": None}}
    buckets = {k: {"facts": []} for k in dd_facts.QUESTION_KEYS}
    dd_facts._valuation_facts(numbers, buckets, ticker="CRWV")
    by_id = {f["id"]: f for f in buckets["q5_valuation"]["facts"]}
    assert by_id["f_net_debt_m"]["value"] == 46074.0 and by_id["f_net_debt_m"]["unit"] == "USD m"
    assert by_id["f_shares_diluted_m"]["value"] == 551.54
    assert by_id["f_ev_m"]["value"] == 91344.12
    assert by_id["f_rev_consensus_fy1_m"]["value"] == 12869.75
    assert by_id["f_rev_consensus_fy2_m"]["value"] == 26295.93
    assert "f_rev_consensus_fy3_m" not in by_id
    assert by_id["f_ev_s_fwd"]["value"] == round(91344.12 / 12869.75, 2)
    # 不撞既有名字：f_consensus_rev_fy*_pct 是 EPS 修正率，沒被動到
    assert not any(i.startswith("f_consensus_rev_") for i in by_id)


def test_numbers_extra_only_capital_structure_splices_into_existing_file(tmp_path, monkeypatch):
    import dd_numbers_extra
    out = tmp_path / "numbers_extra.json"
    out.write_text(json.dumps({"numbers": {"momentum_26w": {"rsi14": 55}}}), encoding="utf-8")
    monkeypatch.setattr(dd_numbers_extra, "compute_capital_structure",
                        lambda ticker, date_dt: {"net_debt_m": 1.0, "ticker": ticker})
    assert dd_numbers_extra.main(["CRWV", "20261012", "--only", "capital_structure", "--out", str(out)]) == 0
    got = json.loads(out.read_text(encoding="utf-8"))["numbers"]
    assert got["momentum_26w"] == {"rsi14": 55}                       # 既有欄位原樣保留
    assert got["capital_structure"] == {"net_debt_m": 1.0, "ticker": "CRWV"}


def test_dd_facts_fx_mismatch_has_no_ev_facts():
    import dd_facts
    numbers = {"capital_structure": {
        "as_of": "2026-10-12", "currency": "TWD", "price_currency": "USD", "fx_mismatch": True,
        "net_debt_m": -2449451.71, "shares_diluted_m": 5186.47, "ev_m": None,
        "revenue_consensus": {"fy1": {"avg_m": 5460820.47, "analysts": 40, "yf_period": "0y"}},
        "note": "財報幣別 TWD ≠ 報價幣別 USD"}}
    buckets = {k: {"facts": []} for k in dd_facts.QUESTION_KEYS}
    dd_facts._valuation_facts(numbers, buckets, ticker="TSM")
    ids = {f["id"] for f in buckets["q5_valuation"]["facts"]}
    assert "f_ev_m" not in ids and "f_ev_s_fwd" not in ids
    assert {"f_net_debt_m", "f_rev_consensus_fy1_m"} <= ids
