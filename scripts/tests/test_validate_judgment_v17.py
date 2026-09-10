#!/usr/bin/env python3
"""測試 `scripts/validate_judgment.py` WP7b 三項修法（2026-09-05，AVGO 真跑
暴露）：

- J3 `--fix`：`contradictions[].axis` 內「（QC-\\d+）」／「(QC-\\d+)」括注整段
  刪除並去尾空白（純代號去除，不改語意）——判斷 agent 常把 judgment-rules
  段名（含 QC 代號）直接抄進讀者面 axis 欄，被 leak scan 擋下。
- 漂移歸因對「前份無此欄」降為 WARN：前份 dd-meta 缺欄／值為 None 而本次有
  值（如 v16 才新增的 `rearm_trigger`）不算未歸因漂移，只 WARN 提醒可不
  歸因；前份確有值才維持 FAIL。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent
NOTES_SRC = ROOT / "notes" / "site-internal" / "dd" / "_src"

sys.path.insert(0, str(SCRIPTS_DIR))
import validate_judgment as vj  # noqa: E402


# ---------------------------------------------------------------------------
# J3 --fix: contradictions[].axis QC-代號括注刪除
# ---------------------------------------------------------------------------

def test_fix_strips_fullwidth_qc_annotation_from_axis(tmp_path):
    data = {
        "contradictions": [
            {"axis": "產業判斷（QC-52）", "ruling": "x"},
        ]
    }
    jpath = tmp_path / "judgment.json"
    applied = vj.apply_fixes(data, jpath)
    assert data["contradictions"][0]["axis"] == "產業判斷"
    assert any("QC" in a for a in applied)


def test_fix_strips_halfwidth_qc_annotation_from_axis(tmp_path):
    data = {
        "contradictions": [
            {"axis": "同形狀 peer 對帳(QC-51)", "ruling": "x"},
        ]
    }
    jpath = tmp_path / "judgment.json"
    vj.apply_fixes(data, jpath)
    assert data["contradictions"][0]["axis"] == "同形狀 peer 對帳"


def test_fix_leaves_axis_without_qc_untouched(tmp_path):
    data = {
        "contradictions": [
            {"axis": "前份漂移：rearm_trigger", "ruling": "x"},
        ]
    }
    jpath = tmp_path / "judgment.json"
    applied = vj.apply_fixes(data, jpath)
    assert data["contradictions"][0]["axis"] == "前份漂移：rearm_trigger"
    assert not any("QC" in a for a in applied)


def test_fix_qc_annotation_removal_unblocks_leak_scan(tmp_path):
    data_before = {"contradictions": [{"axis": "產業判斷（QC-52）", "ruling": "x"}]}
    fails_before = vj.leak_and_punct_checks(data_before)
    assert any("contradictions[0].axis" in f for f in fails_before)

    data_after = json.loads(json.dumps(data_before))
    vj.apply_fixes(data_after, tmp_path / "judgment.json")
    fails_after = vj.leak_and_punct_checks(data_after)
    assert not any("contradictions[0].axis" in f for f in fails_after)


def test_fix_non_dict_or_missing_axis_does_not_crash(tmp_path):
    data = {"contradictions": [{"ruling": "no axis key"}, "not-a-dict", {"axis": None}]}
    jpath = tmp_path / "judgment.json"
    applied = vj.apply_fixes(data, jpath)  # 不應丟例外
    assert isinstance(applied, list)


# ---------------------------------------------------------------------------
# 漂移歸因：前份無此欄 → WARN；前份有值仍 FAIL
# ---------------------------------------------------------------------------

def _minimal_judgment(rearm_trigger="加碼至衛星上限"):
    return {
        "meta": {"ticker": "TEST", "schema": "v16", "date": "20260905"},
        "decision_inputs": {"price_at_dd": 100},
        "appendix_a": {},
        "decision_out": {"rearm_trigger": rearm_trigger},
        "contradictions": [],
    }


def _write_evidence(tmp_path, prior_meta, drift_watch):
    evidence = {
        "prior_dd": {
            "status": "ok",
            "prior_meta": prior_meta,
            "drift_watch": drift_watch,
        }
    }
    p = tmp_path / "evidence.json"
    p.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")
    return p


def test_drift_missing_prior_field_is_warn_not_fail(tmp_path):
    jpath = tmp_path / "judgment.json"
    data = _minimal_judgment()
    # prior_meta 非空（否則 drift_checks 整段因「無 prior_meta」提早 return），
    # 但確實缺 rearm_trigger 這個鍵——對應 v16 才新增此欄的真實情況。
    ev_path = _write_evidence(
        tmp_path, prior_meta={"signal": "🟢"}, drift_watch=["rearm_trigger"]
    )

    fails, warns = vj.drift_checks(data, jpath, ev_path)

    assert not any("rearm_trigger" in f for f in fails)
    assert any("rearm_trigger" in w and "前份格式無此欄，可不歸因" in w for w in warns)


def test_drift_prior_has_value_still_fails_when_unattributed(tmp_path):
    jpath = tmp_path / "judgment.json"
    data = _minimal_judgment()
    data["appendix_a"]["signal"] = "🟢"
    ev_path = _write_evidence(
        tmp_path, prior_meta={"signal": "🔴"}, drift_watch=["signal"]
    )

    fails, warns = vj.drift_checks(data, jpath, ev_path)

    assert any("signal" in f and "漂移未歸因" in f for f in fails)
    assert not any("前份格式無此欄" in f for f in fails)


def test_drift_missing_prior_field_but_attributed_yields_neither(tmp_path):
    jpath = tmp_path / "judgment.json"
    data = _minimal_judgment()
    data["contradictions"] = [{"prior_field": "rearm_trigger", "axis": "前份漂移：rearm_trigger"}]
    ev_path = _write_evidence(
        tmp_path, prior_meta={"signal": "🟢"}, drift_watch=["rearm_trigger"]
    )

    fails, warns = vj.drift_checks(data, jpath, ev_path)

    assert not any("rearm_trigger" in f for f in fails)
    assert not any("rearm_trigger" in w for w in warns)


# ---------------------------------------------------------------------------
# 迴歸：四份 _src judgment（無 --evidence）仍 0 FAIL
# ---------------------------------------------------------------------------

_SRC_CASES = [
    ("BE_20260905", "BE_20260905.judgment.json"),
    ("CIEN_20260905", "CIEN_20260905.judgment.json"),
    ("CRDO_20260904", "CRDO_20260904.judgment.json"),
    ("PANW_20260904", "PANW_20260904.judgment.json"),
]


@pytest.mark.parametrize("subdir,fname", _SRC_CASES)
def test_src_judgment_zero_fail(subdir, fname):
    path = NOTES_SRC / subdir / fname
    if not path.exists():
        pytest.skip(f"fixture 不存在：{path}")
    fails, _warns = vj.validate_file(path, None, j1_warn=False)
    assert fails == [], f"{fname} 出現非預期 FAIL：{fails}"


def test_derived_decision_inputs_null_remain_valid(tmp_path):
    """2026-09-07：三個 scenario 衍生 key 留 null 不得被 validator 判 FAIL。"""
    source = NOTES_SRC / "BE_20260905" / "BE_20260905.judgment.json"
    if not source.exists():
        pytest.skip(f"fixture 不存在：{source}")
    data = json.loads(source.read_text(encoding="utf-8"))
    for field in ("asym_ratio", "irr_base_pct", "ev5y_pct"):
        data["decision_inputs"][field] = None
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert fails == []


# ---------------------------------------------------------------------------
# WP-D（2026-09-10 規則精簡）：A4 原因分組歸因、B 類條件式展開、A1 反證紀錄
# ---------------------------------------------------------------------------

def test_drift_prior_field_array_attributes_multiple_fields(tmp_path):
    """A4：一條 `cause` 條目用 prior_field 陣列同時歸因多個漂移欄。"""
    jpath = tmp_path / "judgment.json"
    data = _minimal_judgment()
    data["appendix_a"]["signal"] = "🟢"
    data["appendix_a"]["val"] = "🟠"
    data["contradictions"] = [{
        "cause": "價格變動",
        "prior_field": ["signal", "val"],
        "axis": "前份漂移：現價一次變動連帶改訊號與估值燈",
        "ruling": "signal 🔴→🟢／val 🔴→🟠，主因＝股價",
    }]
    ev_path = _write_evidence(
        tmp_path, prior_meta={"signal": "🔴", "val": "🔴"}, drift_watch=["signal", "val"]
    )

    fails, _warns = vj.drift_checks(data, jpath, ev_path)

    assert not any("漂移未歸因" in f for f in fails), fails


def test_drift_prior_field_array_still_fails_for_uncovered_field(tmp_path):
    """A4 的放寬有底線：陣列沒涵蓋到的漂移欄仍 FAIL（不是叫 writer 少寫）。"""
    jpath = tmp_path / "judgment.json"
    data = _minimal_judgment()
    data["appendix_a"]["signal"] = "🟢"
    data["appendix_a"]["val"] = "🟠"
    data["contradictions"] = [{"cause": "價格變動", "prior_field": ["signal"], "axis": "只歸因訊號"}]
    ev_path = _write_evidence(
        tmp_path, prior_meta={"signal": "🔴", "val": "🔴"}, drift_watch=["signal", "val"]
    )

    fails, _warns = vj.drift_checks(data, jpath, ev_path)

    assert any("漂移未歸因" in f and "val" in f for f in fails), fails
    assert not any("漂移未歸因" in f and "signal" in f for f in fails), fails


_UNEXPANDED = {"expanded": False, "reason": "本案估值不靠低滲透；份額或新品類成為承重假設時重新展開"}


def _src_judgment(name="BE_20260905"):
    path = NOTES_SRC / name / f"{name}.judgment.json"
    if not path.exists():
        pytest.skip(f"fixture 不存在：{path}")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("top,key", [
    ("industry", "tam_table"),
    ("growth", "segments"),
    ("governance", "capital_returns"),
    ("valuation", "peers"),
])
def test_conditional_block_unexpanded_marker_validates(tmp_path, top, key):
    """B1–B4：條件式區塊填 {"expanded": false, "reason": …} 仍是合法判斷物。"""
    data = _src_judgment()
    data[top][key] = dict(_UNEXPANDED)
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert fails == [], f"{top}.{key} 未展開標記被判 FAIL：{fails}"


def test_counter_evidence_record_shape_validates(tmp_path):
    """A1：反證紀錄的 canonical 形狀合法，且 failure_story／second_failure 可缺。
    2026-09-10（WP-E 修 #3）：新格式三視角均須至少一條非空 evidence／assumption
    ——這裡三視角都給齊，同時驗證形狀合法與覆蓋完整（單視角版另見
    test_premortem_new_format_cannot_be_fully_empty 對面的反例）。"""
    data = _src_judgment()
    data["premortem"]["blind_spots"] = [
        {
            "view": "論點成功但股東經濟變差",
            "evidence": "產能擴張三年吃掉 FCF",
            "assumption": "H2 營運槓桿",
            "consequence": "FCF Margin 由 18% 降至 9%，估值框架由 P/FCF 切到 EV/S",
            "ruling": "採納——已反映進 Bull 終端倍數",
            "watch": "季度 maintenance capex 占 FCF 比重",
            "evidence_refs": [],
        },
        {"view": "論點失敗", "evidence": "共識成長假設未兌現，訂單能見度回落"},
        {"view": "價格已反映太多", "assumption": "現價已隱含樂觀情境的多數上行"},
    ]
    data["premortem"].pop("failure_story", None)
    data["premortem"].pop("second_failure", None)
    data["premortem"]["max_dd"].pop("trigger_time", None)
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert fails == [], f"反證紀錄形狀被判 FAIL：{fails}"


def test_counter_evidence_view_enum_is_enforced(tmp_path):
    """放寬不等於放任：view 只能是三視角之一。"""
    data = _src_judgment()
    data["premortem"]["blind_spots"] = [{"view": "隨便寫", "evidence": "x"}]
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert any("view" in f for f in fails), fails


def test_thesis_h_periods_may_be_omitted(tmp_path):
    """B6：2y／5y／10y 依可觀測時間窗給 1–3 段，缺欄不再 FAIL。"""
    data = _src_judgment()
    for h in data["thesis"]["H"]:
        h.pop("5y", None)
        h.pop("10y", None)
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert fails == [], f"H 期限缺欄被判 FAIL：{fails}"


# ---------------------------------------------------------------------------
# WP-E（2026-09-10）：修 WP-D 五個契約接線洞（Codex 複審
# notes/site-internal/dd/_codex_wpd_review_20260910.md 發現點 1–3；點 4 在
# test_dd_brief.py、點 5 是 prompt 文案同步不落測試）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("field", ["runway_post_y5", "archetype"])
def test_leak_scan_prior_field_array_is_not_a_prose_leak(field):
    """修 #1：A4 開放 prior_field 為欄名陣列後，_walk_strings 對陣列元素產生的
    路徑是 `prior_field[0]`，QC-49 機器欄名豁免原本只匹配字串形狀的
    `prior_field` 這個路徑，漏接陣列形狀、把合法欄名誤判成讀者面文字外洩。"""
    assert vj.leak_and_punct_checks({"contradictions": [{"prior_field": field}]}) == []
    assert vj.leak_and_punct_checks({"contradictions": [{"prior_field": [field]}]}) == []


@pytest.mark.parametrize("top,key", [
    ("industry", "tam_table"), ("growth", "segments"),
    ("governance", "capital_returns"), ("valuation", "peers"),
])
@pytest.mark.parametrize("marker", [
    {},
    {"expanded": False},
    {"expanded": True},
    {"expanded": False, "reason": "   "},
])
def test_expandable_block_illegal_marker_fails(tmp_path, top, key, marker):
    """修 #2：generic schema_validate 不支援 oneOf，B1–B4 條件式展開區塊的
    object 形態原本沒有 required/properties 可管——空物件、缺 reason、
    expanded 不是明確 false、reason 全空白，四種都必須 FAIL；合法標記
    （test_conditional_block_unexpanded_marker_validates）與陣列／原展開形狀
    （test_src_judgment_zero_fail）仍維持 PASS，不受此檢查影響。"""
    data = _src_judgment()
    data[top][key] = dict(marker)
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert fails, f"{top}.{key} 不合法未展開標記未被擋：{marker}"


def test_premortem_new_format_cannot_be_fully_empty(tmp_path):
    """修 #3：A1 撤掉 premortem.failure_story／second_failure 必填後，新格式的
    反證唯一來源（blind_spots[] 依 view 分組）沒有機械契約接住「三視角全空」
    ——用原本驗證通過的 BE 存查複本，清空 blind_spots、拿掉 failure_story／
    second_failure、trap_analysis 只留 verdict，必須 FAIL。"""
    data = _src_judgment()
    data["premortem"]["blind_spots"] = []
    data["premortem"].pop("failure_story", None)
    data["premortem"].pop("second_failure", None)
    data["trap_analysis"] = {"verdict": data["trap_analysis"]["verdict"]}
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert any("視角" in f for f in fails), f"新格式反證三視角全空未被擋：{fails}"


def test_premortem_new_format_with_all_three_views_passes(tmp_path):
    """三視角齊（各至少一條非空 evidence）：PASS。"""
    data = _src_judgment()
    data["premortem"]["blind_spots"] = [
        {"view": v, "evidence": f"視角{i}的具體證據"} for i, v in enumerate(vj._COUNTER_VIEWS)
    ]
    data["premortem"].pop("failure_story", None)
    data["premortem"].pop("second_failure", None)
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert fails == [], fails


def test_premortem_new_format_not_applicable_reason_is_legal_escape(tmp_path):
    """三視角之一沒有 evidence／assumption，但有非空 not_applicable_reason——
    合法的「此視角不適用」出口，不強逼硬湊散文。"""
    data = _src_judgment()
    data["premortem"]["blind_spots"] = [
        {"view": "論點失敗", "evidence": "共識成長假設未兌現，訂單能見度回落"},
        {"view": "論點成功但股東經濟變差", "assumption": "H2 營運槓桿吃掉 FCF"},
        {"view": "價格已反映太多", "not_applicable_reason": "現價仍低於三年均值，無 priced-in 疑慮"},
    ]
    data["premortem"].pop("failure_story", None)
    data["premortem"].pop("second_failure", None)
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert fails == [], fails


def test_premortem_old_format_untouched_by_new_completeness_check(tmp_path):
    """舊格式（有 failure_story 且 blind_spots 為純字串，BE 存查原樣）不受
    修 #3 的新檢查影響，維持原本沒有此檢查的路。"""
    data = _src_judgment()
    assert data["premortem"].get("failure_story"), "fixture 前提：BE 應為舊格式"
    assert all(isinstance(b, str) for b in data["premortem"]["blind_spots"])
    path = tmp_path / "judgment.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    fails, _warns = vj.validate_file(path, None, j1_warn=False)

    assert fails == [], fails


def test_j4_no_longer_warns_on_derivable_plain_fields():
    """A3：有機械 fallback 的 plain 子欄位缺了不再逐欄催稿。"""
    plain = {
        "five": {k: "x" for k in vj._PLAIN_FIVE_KEYS},
        "business": {k: "x" for k in vj._PLAIN_BUSINESS_KEYS},
        "stories": {k: "x" for k in vj._PLAIN_STORIES_KEYS},
        "growth_funding": "x", "prior_compare_reason": "x", "evidence_quality": "x",
    }
    warns = vj.j4_plain_checks({"plain": plain})
    assert warns == [], warns


def test_j5_plain_role_mismatch_is_fail():
    import validate_judgment as vj
    data = {"decision_out": {"role": "衛星"}, "plain": {"verdict_line": "進場，當核心持股，但先買三分之一。", "five": {"how_to_act": "首階三分之一"}}}
    fails, warns = vj.j5_plain_role_checks(data)
    assert any("J5" in f and "核心" in f for f in fails)


def test_j5_plain_role_match_is_clean():
    import validate_judgment as vj
    data = {"decision_out": {"role": "衛星"}, "plain": {"verdict_line": "進場，當衛星持股。", "five": {"why_this_size": "矩陣給衛星"}}}
    fails, warns = vj.j5_plain_role_checks(data)
    assert not fails and not warns


def test_j5_negated_role_is_not_a_conflict():
    import validate_judgment as vj
    data = {"decision_out": {"role": "衛星"}, "plain": {"five": {"why_this_size": "所以只能當衛星，不當核心。"}}}
    fails, warns = vj.j5_plain_role_checks(data)
    assert not fails
