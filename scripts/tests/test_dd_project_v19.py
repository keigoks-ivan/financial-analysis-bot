#!/usr/bin/env python3
"""測試 v19 契約與一處程式轉接（WP-H1，2026-09-11）。

兩件事同時要成立：

1. **舊形狀零改動**——`notes/site-internal/dd/_src/*/*.judgment.json` 與既有
   fixture 經 `dd_project.view_for()` 回傳的必須是**同一個物件**（identity），
   驗證與渲染路徑一個分支都沒改。
2. **v19 形狀走得完整條鏈**——fixture（`judgment_v19_FIX.json` ＋
   `facts_FIX_20260911.json` ＋ scenario／evidence 複本）組成臨時 run 目錄後：
   投影視圖過 `validate_judgment`（J1 真的可達、J2 真的跑、J6 讀得到前份）、
   dd-meta 欄位與判斷值對得上、監測器拿得到致命指標、快速版渲染得出六問與
   三視角、`dd_bundle judge／gate` 組得起來、`dd_project scenario` 能還原
   `dd_scenario.py` 的輸入檔。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SRC_DIR = ROOT / "notes" / "site-internal" / "dd" / "_src"

sys.path.insert(0, str(SCRIPTS_DIR))
import dd_facts  # noqa: E402
import dd_project  # noqa: E402
import gen_dd_tables as gdt  # noqa: E402
import validate_judgment as vj  # noqa: E402

V19_JUDGMENT = FIXTURES / "judgment_v19_FIX.json"
V19_FACTS = FIXTURES / "facts_FIX_20260911.json"
V19_SCENARIO = FIXTURES / "scenario_FIX_20260911.json"
V19_SCENARIO_META = FIXTURES / "scenario_meta_FIX_20260911.json"
V19_EVIDENCE = FIXTURES / "evidence_FIX_20260911.json"

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.S
)


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def run_dir(tmp_path_factory):
    """把 fixture 組成 production 慣例的 run 目錄（judgment.json／
    scenario_meta.json／scenario.json／evidence.json 同層），讓 J2 的 sidecar
    尋檔、`--run-dir` 旗標與 bundle 組裝都走真實路徑。"""
    d = tmp_path_factory.mktemp("v19_run")
    shutil.copyfile(V19_JUDGMENT, d / "judgment.json")
    shutil.copyfile(V19_SCENARIO_META, d / "scenario_meta.json")
    shutil.copyfile(V19_SCENARIO, d / "scenario.json")
    shutil.copyfile(V19_EVIDENCE, d / "evidence.json")
    return d


@pytest.fixture(scope="module")
def v19_view(run_dir):
    raw, view = dd_project.load_view(run_dir / "judgment.json")
    return raw, view


# ---------------------------------------------------------------------------
# 1. 舊形狀零改動
# ---------------------------------------------------------------------------

def _old_shape_judgments():
    paths = sorted(SRC_DIR.glob("*/*.judgment.json"))
    paths.append(FIXTURES / "judgment_v18_TXN.json")
    return [p for p in paths if p.exists()]


def test_old_shape_projection_is_identity():
    """舊形狀（無 meta.contract）→ view_for 回傳同一個物件，不是複本、不是轉換。"""
    checked = 0
    for path in _old_shape_judgments():
        raw = _load(path)
        assert not dd_project.is_v19(raw), f"{path.name} 不該被判成 v19"
        assert dd_project.view_for(raw, path) is raw, f"{path.name} 的投影不是 identity"
        checked += 1
    assert checked >= 19, f"只檢到 {checked} 份舊形狀判斷檔，樣本不足"


def test_old_shape_validate_unchanged_shape():
    """抽一份舊形狀判斷檔實跑 validate_file，確認不會踩到 v19 分支。"""
    path = FIXTURES / "judgment_v18_TXN.json"
    fails, warns = vj.validate_file(path)
    assert not any("v19｜" in f for f in fails)
    assert not any("v19｜" in w for w in warns)


# ---------------------------------------------------------------------------
# 2. v19 契約本身
# ---------------------------------------------------------------------------

def test_v19_fixture_validates(run_dir):
    fails, warns = vj.validate_file(run_dir / "judgment.json",
                                    evidence_path=run_dir / "evidence.json")
    assert fails == [], "v19 fixture 應 0 FAIL：\n" + "\n".join(fails)


def test_v19_rejects_double_filled_decision_input(run_dir, tmp_path):
    """同一件事不准兩邊都填：判斷者手填投影欄 → FAIL。"""
    raw = _load(run_dir / "judgment.json")
    raw["decision_inputs"]["moat"] = "A"
    p = tmp_path / "judgment.json"
    p.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    shutil.copyfile(run_dir / "scenario_meta.json", tmp_path / "scenario_meta.json")
    fails, _warns = vj.validate_file(p)
    assert any("由程式投影的欄" in f for f in fails), fails


def test_v19_rejects_unknown_fact_ref(run_dir, tmp_path):
    raw = _load(run_dir / "judgment.json")
    raw["answers"]["q1_business"]["fact_refs"].append("f_does_not_exist")
    p = tmp_path / "judgment.json"
    p.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    shutil.copyfile(run_dir / "scenario_meta.json", tmp_path / "scenario_meta.json")
    fails, _warns = vj.validate_file(p)
    assert any("f_does_not_exist" in f for f in fails), fails


def test_v19_missing_judgment_value_is_not_backfilled(run_dir):
    """程式不得補判斷：拿掉護城河等級後，投影結果留空並讓既有檢查報缺。"""
    raw = copy.deepcopy(_load(run_dir / "judgment.json"))
    raw["answers"]["q2_moat"]["verdict_values"]["moat"].pop("grade")
    view = dd_project.project(raw, _load(V19_FACTS))
    assert view["moat"].get("grade") is None
    assert view["decision_inputs"]["moat"] is None
    errs = vj.schema_validate(view, _load(SCRIPTS_DIR / "dd_schema" / "judgment.schema.json"), "$")
    assert any("grade" in e for e in errs), errs


# ---------------------------------------------------------------------------
# 3. J1／J2／J6 三道檢查在 v19 形狀下真的跑得到
# ---------------------------------------------------------------------------

def _negative_finding_ids(evidence):
    out = []
    for section in ("coverage", "events"):
        for axis, v in (evidence.get(section) or {}).items():
            if not isinstance(v, dict):
                continue
            for i, f in enumerate(v.get("findings") or []):
                if isinstance(f, dict) and f.get("direction") == "-":
                    out.append(f.get("id") or "{0}#{1}".format(axis, i))
    return out


def test_j1_reachable_and_complete(run_dir, v19_view):
    """J1 可達：14 條負向 finding（coverage 13＋events 1）逐條在投影視圖裡找得到
    處置；把 counter_evidence 的引用拔掉當對照組，J1 必須逐條報回來——證明它
    真的在檢查，不是靜默通過。"""
    _raw, view = v19_view
    evidence = _load(run_dir / "evidence.json")
    negatives = _negative_finding_ids(evidence)
    assert len(negatives) == 14, negatives

    fails, warns = vj.j1_traceability_checks(view, run_dir / "evidence.json")
    assert fails == [], fails
    assert warns == []

    stripped = copy.deepcopy(view)
    for bucket in ("contradictions", "triggers"):
        for item in stripped.get(bucket) or []:
            if isinstance(item, dict):
                item.pop("evidence_refs", None)
    for item in (stripped.get("premortem") or {}).get("blind_spots") or []:
        if isinstance(item, dict):
            item.pop("evidence_refs", None)
    for item in (stripped.get("moat") or {}).get("threats") or []:
        if isinstance(item, dict):
            item.pop("evidence_refs", None)
    for item in ((stripped.get("thesis") or {}).get("R") or []):
        if isinstance(item, dict):
            item.pop("evidence_refs", None)
    stripped["evidence_dismissed"] = []
    control_fails, _ = vj.j1_traceability_checks(stripped, run_dir / "evidence.json")
    assert len(control_fails) == len(negatives), control_fails


def test_j2_actually_runs(run_dir, v19_view):
    """J2 真跑：sidecar 找得到（沒有「略過」警告），且 Max DD 恆等式對得上。"""
    _raw, view = v19_view
    fails, warns = vj.j2_math_checks(view, run_dir / "judgment.json", strict_terminal_year=True)
    assert fails == [], fails
    assert not any("略過" in w for w in warns), warns


def test_j2_terminal_year_is_fail_for_v19(run_dir, tmp_path):
    """終端年契約：v19 形狀差 >1 年直接 FAIL（舊形狀維持 WARN）。"""
    meta = _load(run_dir / "scenario_meta.json")
    meta["scenario_tree"]["terminal_label"] = "FY2034E"
    (tmp_path / "scenario_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    shutil.copyfile(run_dir / "judgment.json", tmp_path / "judgment.json")
    view = dd_project.view_for(_load(tmp_path / "judgment.json"), tmp_path / "judgment.json")

    fails, _warns = vj.j2_math_checks(view, tmp_path / "judgment.json", strict_terminal_year=True)
    assert any("終端年" in f for f in fails), fails

    old_fails, old_warns = vj.j2_math_checks(view, tmp_path / "judgment.json")
    assert not any("終端年" in f for f in old_fails)
    assert any("終端年" in w for w in old_warns)


def test_j6_sees_prior(run_dir, v19_view):
    """J6 可比：前份裁決讀得到（沒有 prior 就整條略過，那樣等於沒接線）。"""
    _raw, view = v19_view
    evidence = _load(run_dir / "evidence.json")
    assert (evidence.get("prior_dd") or {}).get("status") == "ok"
    fails, warns = vj.threshold_drift_checks(view, run_dir / "evidence.json")
    assert fails == [], fails
    assert warns, "J6 應至少回報比對結果（1:1 才擋，非 1:1 只 WARN）"


# ---------------------------------------------------------------------------
# 4. dd-meta 與監測器路徑
# ---------------------------------------------------------------------------

EXPECTED_DD_META = {
    "ticker": "FIX",
    "date": "2026-09-11",
    "price_at_dd": 1610.34,
    "signal": "B",
    "trap": "🟢",
    "moat": "B",
    "moat_score": 8,
    "val": "🔴",
    "pct_5y": 100,
    "dca_verdict": "觀望",
    "dca_role": "追蹤",
    "moat_trend": "→",
    "runway_post_y5": "🟡",
    "capalloc_grade": "B",
    "max_dd_pct": -56,
    "archetype": "品質複利成長",
    "endo_growth_ceiling": 15,
}


def test_dd_meta_from_projection(v19_view):
    _raw, view = v19_view
    meta = gdt.build_dd_meta(view, _load(V19_SCENARIO_META))
    for key, expected in EXPECTED_DD_META.items():
        assert meta.get(key) == expected, f"{key}: {meta.get(key)!r} != {expected!r}"
    # 三個衍生欄由 scenario 權威提供，不是判斷檔抄來的
    assert meta["ev5y_pct"] == 13.3
    assert meta["irr_base_pct"] == 3.8
    assert meta["asym_ratio"] == 1.3


def test_decision_inputs_projected_from_facts(v19_view):
    """三個純事實欄由 facts 投影，判斷者一個字都不用抄。"""
    _raw, view = v19_view
    di = view["decision_inputs"]
    assert di["price_at_dd"] == 1610.34
    assert di["week26_return_pct"] == 26.01
    assert di["consensus_rev_3m_pct"] == 13.58
    assert di["asym_ratio"] is None and di["irr_base_pct"] is None and di["ev5y_pct"] is None


def test_monitor_path_gets_kill_metrics(v19_view):
    """監測器路徑：dd-meta 的 kill_metrics 與 E12 表都要拿得到唯一致命指標。"""
    _raw, view = v19_view
    meta = gdt.build_dd_meta(view, _load(V19_SCENARIO_META))
    kms = meta.get("kill_metrics") or []
    assert len(kms) >= 3
    assert all(k.get("metric") and k.get("bear_threshold") for k in kms)

    e12 = gdt.render_e12_html(view)
    single = [t for t in view["triggers"] if t.get("type") == "Single Thing"]
    assert len(single) == 1, single
    # E12 的「指標與門檻」欄渲染 threshold，白話欄渲染 text——兩者都要進表，
    # 監測器才知道要看哪個數字、跨過哪條線。
    assert single[0]["text"] in e12
    assert single[0]["threshold"] in e12
    assert single[0]["action"] in e12


def test_path_risk_and_capalloc_are_computed_not_guessed():
    assert dd_project.path_risk_from_lo(-56) == "🔴"
    assert dd_project.path_risk_from_lo(-40) == "🟡"
    assert dd_project.path_risk_from_lo(-20) == "🟢"
    assert dd_project.path_risk_from_lo(None) is None

    items = [
        {"name": "ma_roiic", "applicable": True, "passed": None, "input": "x"},
        {"name": "buyback_yield", "applicable": True, "passed": None, "input": "x"},
        {"name": "sbc_dilution", "applicable": True, "passed": True, "input": "x"},
    ]
    assert dd_project.capalloc_grade_from_items({"items": items})[0] == "B"
    two_pass = copy.deepcopy(items)
    two_pass[0]["passed"] = True
    assert dd_project.capalloc_grade_from_items({"items": two_pass})[0] == "A"
    none_pass = copy.deepcopy(items)
    none_pass[2]["passed"] = False
    assert dd_project.capalloc_grade_from_items({"items": none_pass})[0] == "C"
    # 一項都不適用 → 留空，不猜
    na = [dict(i, applicable=False) for i in items]
    assert dd_project.capalloc_grade_from_items({"items": na})[0] is None


# ---------------------------------------------------------------------------
# 5. 渲染與 bundle
# ---------------------------------------------------------------------------

def test_brief_renders_v19(run_dir, tmp_path):
    out = tmp_path / "brief.html"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "dd_brief.py"), "--run-dir", str(run_dir),
         "--out", str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    html = out.read_text(encoding="utf-8")
    # 六問
    assert "六個問題" in html
    for label in ("怎麼賺錢", "競爭優勢", "現金與資本配置", "可能看錯在哪"):
        assert label in html
    # 三視角反證
    for view_name in ("論點失敗", "論點成功但股東經濟變差", "價格已反映太多"):
        assert view_name in html
    # 數字與觸發器
    assert "1610.34" in html or "1610.3" in html
    assert "-56%" in html
    assert "<table" in html
    meta = json.loads(DD_META_RE.search(html).group(1))
    assert meta["dca_verdict"] == "觀望"
    assert meta["brief"] is True


def test_bundles_build_for_v19(run_dir, tmp_path):
    for mode in ("judge", "gate"):
        out = tmp_path / f"{mode}.md"
        r = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "dd_bundle.py"), mode,
             "--run-dir", str(run_dir), "--out", str(out)],
            capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        assert out.stat().st_size > 10000
    gate_text = (tmp_path / "gate.md").read_text(encoding="utf-8")
    # 閘要看得到原檔（v19 形狀）與機械抽出的負向 finding 表
    assert '"contract":"v19"' in gate_text.replace(" ", "")
    assert "負向 finding" in gate_text


def test_prose_stub_and_full_assembly(run_dir, tmp_path):
    tables = tmp_path / "tables"
    prose = tmp_path / "prose"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "gen_dd_tables.py"), str(run_dir / "judgment.json"),
         "--out", str(tables), "--scenario-meta", str(run_dir / "scenario_meta.json")],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "dd_scenario.py"), str(run_dir / "scenario.json"),
         "--html", str(tables / "e11.html"), "--meta", str(tmp_path / "sm.json")],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "dd_project.py"), "prose-stub",
         str(run_dir / "judgment.json"), "--out", str(prose)],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

    raw, view = dd_project.load_view(run_dir / "judgment.json")
    gdt.write_mechanical_prose(view, _load(run_dir / "evidence.json").get("prior_dd"),
                               prose, _load(run_dir / "scenario_meta.json"))
    out = tmp_path / "full.html"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "render_dd.py"), "--assemble", str(prose),
         "--tables", str(tables), "--judgment", str(run_dir / "judgment.json"),
         "-o", str(out), "--no-postprocess"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    html = out.read_text(encoding="utf-8")
    for sid in ("s1", "s5", "s10", "decision", "revlog", "s14", "appA"):
        assert f'id="{sid}"' in html
    for table_id in ("e3", "e5", "e6", "e7", "e8", "e9", "e10"):
        assert f'id="{table_id}"' in html
    # E12 的表格 id 是 `triggers`（gen_dd_tables.render_e12_html 既有命名）
    assert 'id="triggers"' in html


def test_scenario_emitter_round_trips():
    """P-25：scenario_inputs 產出的 dd_scenario 輸入檔，與既有 scenario.json 等值
    ——同一組 EPS 路徑／倍數／機率只寫一次。"""
    raw = _load(V19_JUDGMENT)
    emitted = dd_project.scenario_input_from_v19(raw, _load(V19_FACTS))
    original = _load(V19_SCENARIO)
    assert json.dumps(emitted, ensure_ascii=False, sort_keys=True) == \
        json.dumps(original, ensure_ascii=False, sort_keys=True)


# ---------------------------------------------------------------------------
# 6. facts.json
# ---------------------------------------------------------------------------

def test_facts_fixture_valid():
    fails, warns = dd_facts.check(_load(V19_FACTS))
    assert fails == [], fails
    assert warns == [], warns


def test_findings_digest_is_not_direction_filtered():
    facts = _load(V19_FACTS)
    evidence = _load(V19_EVIDENCE)
    digest_ids = {d["id"] for d in facts["findings_digest"]}
    directions = {d.get("direction") for d in facts["findings_digest"]}
    assert {"+", "0", "-"} <= directions, directions
    missing = []
    for section in ("coverage", "events"):
        for axis, v in (evidence.get(section) or {}).items():
            if not isinstance(v, dict):
                continue
            findings = v.get("findings") or []
            if not findings:
                assert "{0}#none".format(axis) in digest_ids, axis
                continue
            for i, f in enumerate(findings):
                fid = f.get("id") or "{0}#{1}".format(axis, i)
                if fid not in digest_ids:
                    missing.append(fid)
    assert missing == [], missing


def test_facts_extract_is_deterministic(tmp_path):
    """零 LLM 抽取：同一份 evidence 兩次產出一致，且抽不到的題目標 needs_sonnet。"""
    evidence = _load(V19_EVIDENCE)
    a = dd_facts.extract(evidence, None, date="2026-09-11")
    b = dd_facts.extract(evidence, None, date="2026-09-11")
    assert json.dumps(a, ensure_ascii=False, sort_keys=True) == \
        json.dumps(b, ensure_ascii=False, sort_keys=True)
    assert a["questions"]["q3_growth"]["facts"] == []
    assert a["questions"]["q3_growth"]["needs_sonnet"] is True
    ids = {f["id"] for q in a["questions"].values() for f in q["facts"]}
    assert "f_price_at_dd" in ids
    assert "f_consensus_rev_3m_fy1_pct" in ids
    guidance = [f for q in a["questions"].values() for f in q["facts"]
                if f["kind"] == "guidance"]
    assert guidance, "管理層展望必須記成 guidance 而非 realized"


# ---------------------------------------------------------------------------
# 7. WP-H2-1（2026-09-11）：擋門、護城河表搬移、格式正規化
# ---------------------------------------------------------------------------

def _v19_run(tmp_path, facts=True, scenario_meta=True, mutate=None):
    """組一份 v19 run 目錄；`facts=False` 拔掉事實檔、`scenario_meta=False`
    拔掉 sidecar，用來重現 Codex 點名的兩個漏擋。"""
    d = tmp_path
    raw = _load(V19_JUDGMENT)
    raw["facts_ref"] = str(d / "facts.json") if facts else str(d / "__missing__.json")
    raw["scenario_ref"] = str(d / "scenario.json")
    if mutate:
        mutate(raw)
    (d / "judgment.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    if facts:
        shutil.copyfile(V19_FACTS, d / "facts.json")
    shutil.copyfile(V19_SCENARIO, d / "scenario.json")
    shutil.copyfile(V19_EVIDENCE, d / "evidence.json")
    if scenario_meta:
        shutil.copyfile(V19_SCENARIO_META, d / "scenario_meta.json")
    return d / "judgment.json"


def test_v19_baseline_run_passes(tmp_path):
    """先釘住基準：兩樣都在時 0 FAIL——否則下面兩個負向測試證明不了任何事。"""
    path = _v19_run(tmp_path)
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert fails == [], fails


def test_v19_missing_facts_file_is_fail(tmp_path):
    """Codex 漏擋①：事實檔不存在時，H1 仍 0 FAIL（引用核對與部分投影靜默跳過）。
    v19 正式流程必須擋——沒有事實表就沒有可追溯性。"""
    path = _v19_run(tmp_path, facts=False)
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("事實檔" in f for f in fails), fails


def test_v19_unparseable_facts_file_is_fail(tmp_path):
    """事實檔在、但不是合法 JSON——同樣不得放行。"""
    path = _v19_run(tmp_path)
    (tmp_path / "facts.json").write_text("{ 這不是 JSON", encoding="utf-8")
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("事實檔" in f for f in fails), fails


def test_v19_facts_failing_its_own_check_is_fail(tmp_path):
    """事實檔可解析但過不了 `dd_facts.check`（這裡：value 為 null 卻沒標
    needs_sonnet）——判斷檔一樣不得放行。"""
    path = _v19_run(tmp_path)
    facts = _load(tmp_path / "facts.json")
    facts["questions"]["q1_business"]["facts"][0]["value"] = None
    facts["questions"]["q1_business"]["facts"][0].pop("needs_sonnet", None)
    (tmp_path / "facts.json").write_text(json.dumps(facts, ensure_ascii=False), encoding="utf-8")
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("dd_facts check" in f for f in fails), fails


def test_v19_missing_scenario_meta_is_fail(tmp_path):
    """Codex 漏擋②：scenario_meta 不存在時 J2 靜默略過、仍 0 FAIL。
    v19 要求情境結果完整且 J2 確實執行。"""
    path = _v19_run(tmp_path, scenario_meta=False)
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("J2" in f and "確實執行" in f for f in fails), fails


def test_v19_j2_not_actually_executed_is_fail(tmp_path):
    """「沒算」與「算過通過」不可同樣算過關：scenario_meta 在、但缺
    `bear_5y_price`，Max DD 恆等式根本沒跑 → FAIL（舊形狀只 WARN）。"""
    path = _v19_run(tmp_path)
    meta = _load(tmp_path / "scenario_meta.json")
    meta.pop("bear_5y_price", None)
    (tmp_path / "scenario_meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("Max DD 恆等式略過" in f for f in fails), fails


def test_v19_dangling_fact_ref_is_fail(tmp_path):
    """`fact_refs` 指到事實表沒有的 id ＝ 斷鏈，FAIL。"""
    def mutate(raw):
        raw["answers"]["q1_business"]["fact_refs"].append("f_does_not_exist")
    path = _v19_run(tmp_path, mutate=mutate)
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("f_does_not_exist" in f for f in fails), fails


# --- 護城河表部分搬移（Codex 裁定 3） ------------------------------------

def test_peer_tables_are_projected_from_facts(v19_view):
    """同業數字來自 facts.peer_comparison，判斷者只寫 strategy_note。"""
    raw, view = v19_view
    moat_raw = raw["answers"]["q2_moat"]["verdict_values"]["moat"]
    assert "spread_table" not in moat_raw and "competitors" not in moat_raw, \
        "v19 判斷檔不該再帶同業數字表"
    facts = _load(V19_FACTS)
    pc = facts["peer_comparison"]
    peers = [r for r in pc["rows"] if r["name"] != pc.get("subject")]
    assert len(view["moat"]["competitors"]) == len(peers)
    eme_row = next(r for r in pc["rows"] if r["name"] == "EME")
    eme_view = next(c for c in view["moat"]["competitors"] if c["name"].startswith("EME"))
    assert eme_view["om"] == eme_row["values"]["operating_margin_pct"]
    assert eme_view["gm"] == eme_row["values"]["gross_margin_pct"]
    assert "無力發動價格戰" in json.dumps(view["moat"]["competitors"], ensure_ascii=False)
    assert len(view["moat"]["spread_table"]) == len(pc["metrics"])


def test_peer_tables_absent_when_facts_have_no_peers(tmp_path):
    """事實表沒有同業資料 → 兩張表都不生（不放空表假裝比過）。"""
    path = _v19_run(tmp_path)
    facts = _load(tmp_path / "facts.json")
    facts.pop("peer_comparison", None)
    (tmp_path / "facts.json").write_text(json.dumps(facts, ensure_ascii=False), encoding="utf-8")
    _raw, view = dd_project.load_view(path)
    assert "spread_table" not in view["moat"]
    assert "competitors" not in view["moat"]


def test_peer_comparison_extract_matches_evidence():
    """`dd_facts.build_peer_comparison` 只搬數字、期間、口徑、來源，不加判讀。"""
    evidence = _load(V19_EVIDENCE)
    pc = dd_facts.build_peer_comparison(evidence["numbers"], subject=evidence.get("ticker"))
    peers = (evidence["numbers"] or {}).get("peer_financials") or {}
    assert len(pc["rows"]) == len(peers)
    for row in pc["rows"]:
        src = peers[row["name"]]
        assert row["period"] == src.get("fiscal_period_as_of")
        assert row["source"]["type"] == "evidence_numbers"
        for m in pc["metrics"]:
            assert row["values"][m["key"]] == src.get(m["key"])
    # 整欄皆 null 的度量不列（研發密度四家皆未揭露）
    assert "rd_intensity_pct" not in {m["key"] for m in pc["metrics"]}


# --- 必要項目是否有回答（取代 minItems） ---------------------------------

def test_checkpoints_require_an_answer_not_four_empty_objects(tmp_path):
    """四個空物件過得了 minItems，過不了「四項各有沒有回答」。"""
    def mutate(raw):
        rd = raw["answers"]["q2_moat"]["verdict_values"]["moat"]["roic_durability"]
        rd["checkpoints"] = [{}, {}, {}, {}]
    path = _v19_run(tmp_path, mutate=mutate)
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    for name in vj.ROIC_CHECKPOINT_NAMES:
        assert any(name in f for f in fails), (name, fails)


def test_checkpoint_listed_but_unanswered_is_fail(tmp_path):
    """某一項列了但 text 空、也沒寫不適用理由 → FAIL。"""
    def mutate(raw):
        rd = raw["answers"]["q2_moat"]["verdict_values"]["moat"]["roic_durability"]
        rd["checkpoints"][3] = {"item": "社會容忍度", "level": "🟡", "text": "  "}
    path = _v19_run(tmp_path, mutate=mutate)
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("社會容忍度" in f and "沒有回答" in f for f in fails), fails


def test_checkpoint_not_applicable_with_reason_passes(tmp_path):
    """不適用但寫了理由 ＝ 有回答。"""
    def mutate(raw):
        rd = raw["answers"]["q2_moat"]["verdict_values"]["moat"]["roic_durability"]
        rd["checkpoints"][3] = {"item": "社會容忍度",
                                "not_applicable_reason": "受管制費率案決定，本軸不適用"}
    path = _v19_run(tmp_path, mutate=mutate)
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert not any("社會容忍度" in f for f in fails), fails


def test_no_peers_and_no_reason_is_fail(tmp_path):
    """查無同業又不寫理由 → FAIL（空物件與空陣列都不算回答）。"""
    def mutate(raw):
        raw["answers"]["q2_moat"]["verdict_values"]["moat"]["competitor_notes"] = []
    path = _v19_run(tmp_path, mutate=mutate)
    facts = _load(V19_FACTS)
    facts.pop("peer_comparison", None)
    (tmp_path / "facts.json").write_text(json.dumps(facts, ensure_ascii=False), encoding="utf-8")
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("peer_na_reason" in f for f in fails), fails


def test_competitor_note_missing_strategy_note_is_fail(tmp_path):
    def mutate(raw):
        moat = raw["answers"]["q2_moat"]["verdict_values"]["moat"]
        moat["competitor_notes"].append({"name": "XYZ", "strategy_note": ""})
    path = _v19_run(tmp_path, mutate=mutate)
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert any("competitor_notes" in f for f in fails), fails


# --- 格式正規化只修形狀 --------------------------------------------------

def test_normalize_is_noop_for_old_shape():
    raw = _load(FIXTURES / "judgment_v18_TXN.json")
    out, changes = dd_project.normalize(raw, FIXTURES / "judgment_v18_TXN.json")
    assert out is raw and changes == []


def test_normalize_fixes_shape_only(tmp_path):
    """三類會修：路徑、確定的欄名映射、單物件包陣列。"""
    raw = _load(V19_JUDGMENT)
    raw["answers"]["q1"] = raw["answers"].pop("q1_business")
    raw["answers"]["q1"]["facts"] = raw["answers"]["q1"].pop("fact_refs")
    raw["triggers"] = raw["counter_evidence"].pop("triggers")
    raw["counter_evidence"]["blind_spots"] = raw["counter_evidence"]["blind_spots"][0]
    raw["facts_ref"] = "scripts/tests/fixtures/facts_FIX_20260911.json"
    p = tmp_path / "judgment.json"
    p.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    out, changes = dd_project.normalize(raw, p)
    assert "q1_business" in out["answers"] and "q1" not in out["answers"]
    assert "fact_refs" in out["answers"]["q1_business"]
    assert "triggers" in out["counter_evidence"] and "triggers" not in out
    assert isinstance(out["counter_evidence"]["blind_spots"], list)
    assert Path(out["facts_ref"]).is_absolute()
    assert len(changes) >= 5


def test_normalize_does_not_backfill_missing_judgment_values(tmp_path):
    """**界線測試**：缺理由／缺評級／缺機率，正規化一個都不補，validate 仍 FAIL。"""
    def mutate(raw):
        moat = raw["answers"]["q2_moat"]["verdict_values"]["moat"]
        moat["grade"] = None                                    # 缺評級
        moat["roic_durability"]["checkpoints"][0].pop("text")    # 缺理由
        raw["scenario_inputs"]["p"].pop("bear")                  # 缺機率
    path = _v19_run(tmp_path, mutate=mutate)
    before = _load(path)
    out, _changes = dd_project.normalize(before, path)
    assert out["answers"]["q2_moat"]["verdict_values"]["moat"]["grade"] is None
    assert "text" not in out["answers"]["q2_moat"]["verdict_values"]["moat"][
        "roic_durability"]["checkpoints"][0]
    assert "bear" not in out["scenario_inputs"]["p"]
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    fails, _warns = vj.validate_file(path, evidence_path=path.parent / "evidence.json",
                                     j1_warn=True)
    assert fails, "缺判斷值的檔經正規化後仍必須 FAIL"
    assert any("需求基礎值" in f for f in fails), fails
