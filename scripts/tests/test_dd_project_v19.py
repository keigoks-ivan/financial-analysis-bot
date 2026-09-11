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
