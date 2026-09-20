#!/usr/bin/env python3
"""scripts/dd2/decide.py — DD 閘機械化第一批（A／B／C／H 四類）。

設計稿：`notes/site-internal/dd/_dd_gate_decide_design_20260920.md`（2026-09-20
持有人拍板：信心門檻 0.95／0.70；第一批只做 A、B、C、H 四類；低信心清單不停
run）。契約見 `scripts/dd2/README.md` §8k（實作者填的實測紀錄）。

概念：閘從「叫 opus 讀一遍找矛盾」改成「程式列題、模型只答選項、程式依信心
分流」。四類題目全部由程式從 `judgment.json`／`facts.json` 展開（`expand_A`／
`expand_B`／`expand_C`／`expand_H`，純程式、離線可跑），送進 `decide_batch`
用 `claude -p --json-schema` 問模型，回來後 `apply_decisions` 依信心分流：

- 信心 ≥ 0.95：程式直接處置（標記 judgment 欄位、必要時改 scenario.json 機率），
  同時記一筆 🔴（`mechanical_items`），供 `run.py::do_gated` 併進當輪 gate 結果。
- 0.70 ≤ 信心 < 0.95：轉交 opus 閘複審（`mid_items`，🟡）。
- 信心 < 0.70 或答案不在選項內（`valid=False`）：寫進 `owner_queue.md`，run
  不因此停下，交 finish 檢查未清項目。

不動判斷者的 prompt 與契約，不動散文；不接真的決策模型 API，後端只有
`claude -p` 一種（`decide_batch` 內部呼叫），介面（`decide_batch`／
`apply_decisions`）與後端脫鉤，換後端不用動題庫與分流規則。

只 import `scripts/dd2/spawn.py`（`oneshot_stream`／`strip_json`），不 import
`scripts/ddreport.py`——與 `bundle.py`／`facts_store.py` 同一個理由：避免拖進
整條舊鏈的重依賴，本檔只需要一個會呼叫 `claude -p` 的函式與一組小工具，見
`spawn.py` 模組 docstring。`_load_json`／`_atomic_write_json` 因此在本檔重寫
一份（與 `ddreport.py` 同語意），不是重複發明。

Python 3.9 相容（`from __future__ import annotations`）。

CLI：
    python3 scripts/dd2/decide.py MU_20260917            # 真跑機械閘，印結果
    python3 scripts/dd2/decide.py MU_20260917 --offline  # 只展開題目印出來
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS_DIR = HERE.parent
REPO_ROOT = SCRIPTS_DIR.parent
for _p in (str(SCRIPTS_DIR), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import spawn as sp  # noqa: E402

# ---------------------------------------------------------------------------
# 小工具（與 ddreport.py 同語意，原樣重寫一份，理由見模組 docstring）
# ---------------------------------------------------------------------------

def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _atomic_write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    import os
    os.replace(str(tmp), str(path))


def _usage_record(label, r):
    """比照 `run.py::_usage_record`（同一組欄位），這裡不 import run.py（會與
    它未來 import 本檔形成循環），原樣重寫一份。"""
    return {"id": label, "ok": r.get("ok"), "num_turns": r.get("num_turns"),
            "output_tokens": r.get("output_tokens"), "cache_read": r.get("cache_read"),
            "cache_creation": r.get("cache_creation"), "cost_usd": r.get("cost_usd"),
            "duration_ms": r.get("duration_ms"), "over_budget": r.get("over_budget"),
            "thinking_tokens": r.get("thinking_tokens"), "haiku_input_tokens": r.get("haiku_input_tokens")}


# ---------------------------------------------------------------------------
# decide_batch：固定前綴＋題目列表，claude -p --json-schema
#
# 2026-09-20 實測（3 題、opus、effort low，見 README §8k）：`--json-schema`
# 頂層必須是 `"type":"object"`——傳裸陣列 schema 會被 API 拒絕
# （`tools.0.custom.input_schema.type: Input should be 'object'`），因為
# CLI 把 `--json-schema` 包成一個叫 `StructuredOutput` 的工具，工具輸入本來就
# 只能是 object。故本檔的 schema 是 `{"answers": [...]}`，答案陣列包一層。
# 模型走工具呼叫回答，不产生 assistant text 區塊；結構化結果落在最終
# `result` 事件的 `structured_output`（已解析 dict）與 `result`（同內容的
# JSON 字串）兩個欄位，`oneshot_stream` 原本只收集 text 內容塊、不認得
# `tool_use`，故補一段解析（`_augment_stream_result_with_structured_output`
# 沒有另開函式，直接在 `oneshot_stream` 內加，見該函式改動）——不動它既有
# 「回傳 text 內容」那條路徑，只是在 `stitched` 為空又有 `structured_output`
# 時補上等效內容，讓既有呼叫端（run.py 的 judged／gated，走 `strip_json`
# 消費 `result_text`）完全不受影響。
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "opus"
DEFAULT_EFFORT = "low"
DEFAULT_BATCH_SIZE = 20
THRESHOLDS = (0.95, 0.70)  # (高信心, 中信心下界)，2026-09-20 持有人拍板


def _answer_schema():
    return {
        "type": "object",
        "properties": {
            "answers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "answer": {"type": "string"},
                        "confidence": {"type": "number"},
                        "note": {"type": "string"},
                    },
                    "required": ["id", "answer", "confidence", "note"],
                },
            }
        },
        "required": ["answers"],
    }


def _compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


_PREFIX_HEADER = (
    "# DD 機械閘題庫（decide.py）\n\n"
    "以下依序是判斷物（judgment.json）、findings 摘要（facts.json 的 "
    "findings_digest）、情境輸入（scenario.json），皆為緊湊 JSON，內容跨包"
    "固定不變。讀完後只依本訊息最後的題目列表作答，不得引用檔案以外的資訊，"
    "也不必檢查與題目無關的內容。\n"
)


def _build_prefix(run_dir):
    """固定前綴：judgment.json（緊湊 JSON）＋ facts.json 的 findings_digest
    （緊湊 JSON）＋ scenario.json（緊湊 JSON），三段依序放最前面。同一
    `run_dir` 重複呼叫必須逐位元組相同（跨包快取靠這個）——只要 judgment.json／
    facts.json／scenario.json 這三個檔在呼叫之間沒被改動，重讀檔案本身就
    保證位元組相同，`decide_batch` 因此不快取這段文字、每次呼叫都重讀，
    呼叫端（`run_mechanical_gate`）必須確保四類 `decide_batch` 呼叫之間不去
    動這三個檔（覆寫動作全部留到 `apply_decisions` 最後一次寫回）。"""
    run_dir = Path(run_dir)
    judgment = _load_json(run_dir / "judgment.json")
    facts = _load_json(run_dir / "facts.json")
    digest = facts.get("findings_digest") or []
    scenario_path = run_dir / "scenario.json"
    scenario = _load_json(scenario_path) if scenario_path.exists() else {}
    parts = [
        _PREFIX_HEADER,
        "\n## judgment.json（緊湊 JSON）\n\n```json\n" + _compact(judgment) + "\n```\n",
        "\n## facts.json findings_digest（緊湊 JSON）\n\n```json\n" + _compact(digest) + "\n```\n",
        "\n## scenario.json（緊湊 JSON）\n\n```json\n" + _compact(scenario) + "\n```\n",
    ]
    return "".join(parts)


def _question_tail(batch):
    lines = [
        "\n## 本包題目（共 {0} 題，依序作答）\n\n".format(len(batch)),
        "每題依 kind 用對應規則作答：noul（是／否二選一）、choice（從 options "
        "選一個最貼切的）、score（有序等級，從 options 選一個）。confidence 是"
        "你對這個答案自報的把握（0 到 1 之間的小數，不必是校準過的機率）；"
        "note 是一句話理由，40 字以內。只用結構化輸出作答，不要多寫文字。\n",
    ]
    for q in batch:
        lines.append("\n### {0}（{1}）\n\n".format(q["id"], q["kind"]))
        lines.append("問題：{0}\n\n".format(q["question"]))
        lines.append("options：{0}\n\n".format(json.dumps(q.get("options") or [], ensure_ascii=False)))
        lines.append("context：{0}\n".format(q.get("context") or ""))
    return "".join(lines)


def _extract_answers(r):
    """從 `oneshot_stream` 的回傳值取出答案陣列。優先看 `structured_output`
    （`--json-schema` 呼叫時 CLI 把答案放這裡，見上方模組註解的實測紀錄）；
    沒有就退回對 `result_text` 跑 `strip_json`（沿用既有 JSON 剝殼邏輯）。兩種
    來源都可能是「裸陣列」或「{"answers": [...]}」（schema 頂層是 object，
    答案包在 `answers` 欄位下），兩種形狀都收。"""
    so = r.get("structured_output")
    if isinstance(so, dict) and isinstance(so.get("answers"), list):
        return so["answers"]
    if isinstance(so, list):
        return so
    text = r.get("result_text")
    obj = None
    if text:
        obj, _err = sp.strip_json(text)
    if isinstance(obj, dict) and isinstance(obj.get("answers"), list):
        return obj["answers"]
    if isinstance(obj, list):
        return obj
    return []


def decide_batch(run_dir, questions, *, model, effort="low", batch_size=20, agents_dir,
                  label_prefix, usage_sink=None):
    """一批題目送 `claude -p --json-schema` 問一輪，超過 `batch_size` 自動
    分包（固定前綴＋本包題目）。回 list of
    `{"id","answer","confidence","note","valid"}`（`answer` 不在該題
    `options` 內視為 `valid=False`、`confidence` 強制歸零）。

    `usage_sink`：可選，給一個 list 就把每包的 usage（比照
    `run.py::_usage_record`，label 形如 `decide_A_1`）append 進去，供呼叫端
    記進 manifest；不給就不記（本函式的回傳值本身只有答案，usage 走這個
    旁路——設計稿只講回傳答案陣列，沒有另開一個回傳值，這是最小侵入的做法，
    細節見 README §8k「假設」）。"""
    run_dir = Path(run_dir)
    agents_dir = Path(agents_dir)
    agents_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir = run_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    prefix = _build_prefix(run_dir)
    schema_str = json.dumps(_answer_schema(), ensure_ascii=False)
    by_id = {q["id"]: q for q in questions}
    results = []
    batches = [questions[i:i + batch_size] for i in range(0, len(questions), batch_size)]
    for bi, batch in enumerate(batches, start=1):
        prompt_text = prefix + _question_tail(batch)
        label = "{0}_{1}".format(label_prefix, bi)
        prompt_path = prompts_dir / (label + ".md")
        prompt_path.write_text(prompt_text, encoding="utf-8")
        out_json = agents_dir / (label + ".json")
        extra_args = ["--effort", effort, "--json-schema", schema_str]
        r = sp.oneshot_stream(prompt_path, model, out_json, run_dir, extra_args=extra_args)
        if usage_sink is not None:
            usage_sink.append(_usage_record(label, r))
        answers = _extract_answers(r) if r.get("ok") else []
        got = set()
        for a in answers:
            if not isinstance(a, dict):
                continue
            qid = str(a.get("id") or "")
            q = by_id.get(qid)
            if q is None or qid in got:
                continue
            got.add(qid)
            answer = a.get("answer")
            answer = "" if answer is None else str(answer)
            options = q.get("options") or []
            valid = answer in options
            try:
                conf = float(a.get("confidence"))
            except (TypeError, ValueError):
                conf = 0.0
            if not valid:
                conf = 0.0
            conf = max(0.0, min(1.0, conf))
            results.append({"id": qid, "answer": answer, "confidence": conf,
                            "note": str(a.get("note") or ""), "valid": valid})
        for q in batch:
            if q["id"] not in got:
                results.append({"id": q["id"], "answer": "", "confidence": 0.0,
                                "note": "模型未作答（呼叫失敗或漏答）", "valid": False})
    return results


# ---------------------------------------------------------------------------
# 題庫展開：純程式、離線可跑
# ---------------------------------------------------------------------------

_A_QUESTION = "照這些證據，門檻寫的條件現在已經成立了嗎？"
_A_OPTIONS = ["是", "否"]


def expand_A(judgment, facts):
    """A 類（門檻是否已被自引證據觸發）。對 `thesis.R[]` 每一條有 `threshold`
    的，取 `evidence_refs` 指到的 finding 原文（`facts.json` 的
    `findings_digest` 裡對應 id 的那條全文：claim／direction／source／
    as_of）當 context，一題 noul。`evidence_refs` 沒有任何一條在
    `findings_digest` 找得到的 R 不出題（沒有證據原文可給，出了模型也無所
    本回答）。"""
    digest_by_id = {e.get("id"): e for e in (facts.get("findings_digest") or []) if isinstance(e, dict)}
    r_list = ((judgment.get("thesis") or {}).get("R")) or []
    out = []
    n = 0
    for idx, r in enumerate(r_list):
        if not isinstance(r, dict):
            continue
        threshold = r.get("threshold")
        if not threshold:
            continue
        refs = r.get("evidence_refs") or []
        findings = [digest_by_id[ref] for ref in refs if ref in digest_by_id]
        if not findings:
            continue
        n += 1
        ctx_obj = {
            "r_id": r.get("id"), "threshold": threshold,
            "findings": [{"id": f.get("id"), "claim": f.get("claim"), "direction": f.get("direction"),
                         "source": f.get("source"), "as_of": f.get("as_of")} for f in findings],
        }
        out.append({
            "id": "A{0}".format(n), "kind": "noul", "question": _A_QUESTION, "options": list(_A_OPTIONS),
            "context": json.dumps(ctx_obj, ensure_ascii=False),
            "_r_index": idx, "_r_id": r.get("id"), "_threshold": threshold,
        })
    return out


_B_QUESTION = "這條進場路徑是否在約束全部解除後才進場？"
_B_OPTIONS = ["是", "否"]
_B_SPLIT_RE = re.compile(r"[；。]|或")
_B_CONSTRAINT_RE = re.compile(r"約束|解除|才進場")


def _split_paths(text):
    if not text:
        return []
    return [p.strip() for p in _B_SPLIT_RE.split(text) if p and p.strip()]


def expand_B(judgment):
    """B 類（進場路徑是否符合自身約束）。把
    `counter_evidence.action_conditions` 的 `exec_line` 與 `rearm_trigger`
    依「；」「。」「或」拆成路徑；約束句＝`exec_line` 拆出的路徑裡含「約束」
    「解除」「才進場」字樣的那一條（找不到就整段 `exec_line` 當約束）。

    設計稿沒講清楚約束句本身算不算一條「路徑」——它是判準本身，不是一條
    進場動作，問「這條路徑是否在約束解除後才進場」對它自己是範疇錯誤，故本
    實作把約束句排除在出題之外，只對其餘路徑（`exec_line` 與
    `rearm_trigger` 拆出來的，各自）逐條出題。這是保守假設，見 README §8k。"""
    ac = (judgment.get("counter_evidence") or {}).get("action_conditions") or {}
    exec_line = ac.get("exec_line") or ""
    rearm = ac.get("rearm_trigger") or ""
    exec_paths = _split_paths(exec_line)
    constraint = next((p for p in exec_paths if _B_CONSTRAINT_RE.search(p)), None)
    if constraint is None:
        constraint = exec_line.strip() if exec_line else ""
    rearm_paths = _split_paths(rearm)
    out = []
    n = 0
    for source, paths in (("exec_line", exec_paths), ("rearm_trigger", rearm_paths)):
        for p in paths:
            if p == constraint:
                continue
            n += 1
            ctx_obj = {"path": p, "source": source, "constraint": constraint}
            out.append({
                "id": "B{0}".format(n), "kind": "noul", "question": _B_QUESTION, "options": list(_B_OPTIONS),
                "context": json.dumps(ctx_obj, ensure_ascii=False),
                "_source": source, "_path_text": p, "_constraint": constraint,
            })
    return out


_C_QUESTION = "判斷物的內容有沒有實質處理這條？"
_C_OPTIONS = ["有", "沒有"]
# fallback（digest 沒有 direction 欄位時才用）：風險軸與負向詞表，見 expand_C docstring。
_RISK_AXES = (
    "competitive_share_entrants", "customer_second_source", "customer_concentration_credit",
    "supply_demand_durability", "regulatory_antitrust", "reg_tariff_export", "geo_supply_chain",
    "substitute_technology", "channel_business_model_shift", "cyclical_prior_downcycle_behavior",
)
_NEGATIVE_WORDS = ("下滑", "流失", "轉弱", "訴訟", "關稅", "違約", "下修", "收縮", "惡化", "侵蝕",
                   "過剩", "反轉", "裁罰", "罷工", "制裁", "斷鏈", "示警", "警告")


def expand_C(judgment, facts):
    """C 類（負向 finding 有沒有被接住）。`findings_digest` 裡負向的
    finding，且 id 沒出現在 judgment 全文任何地方的，一題 noul。

    負向判準：三檔實測（MU／TSM／TXN）`findings_digest` 每條都帶 `direction`
    欄位（值 `"+"`／`"0"`／`"-"`／`null`），故直接取 `direction == "-"`。
    若日後 digest 換了欄位名（polarity／sentiment 之類），這裡要跟著改名，
    不強求同名不改邏輯；`findings_digest` 完全沒有這類欄位時才退回較粗的
    fallback——軸名屬於 `_RISK_AXES`（競爭／客戶集中／供需／法規／關稅／
    地緣／替代技術／通路轉型／上一輪下行行為）且 `claim` 文字含
    `_NEGATIVE_WORDS` 任一負向詞。這是保守 fallback，寧可漏抓也不要對已經
    標好極性的資料另猜一套規則。

    「id 沒出現在 judgment 全文任何地方」：把整份 `judgment` 序列化成緊湊
    JSON 字串做子字串比對，不是只挑 `thesis.R`／`counter_evidence.
    contradictions`／`counter_evidence.triggers`／
    `counter_evidence.evidence_dismissed` 幾個路徑逐一核對——不同 archetype
    的判斷物欄位形狀不同（例如本批三檔都沒有 `moat.threats` 這個路徑，
    `moat` 相關內容在 `answers.q2_moat` 底下），挑固定路徑容易因為挑錯路徑
    漏放過一條該問的；全文比對更保守，純比對抓得到就不出題，抓不到才問
    模型。"""
    digest = facts.get("findings_digest") or []
    jtext = json.dumps(judgment, ensure_ascii=False)
    has_direction = any(isinstance(e, dict) and "direction" in e for e in digest)
    out = []
    n = 0
    for e in digest:
        if not isinstance(e, dict):
            continue
        fid = e.get("id")
        if not fid:
            continue
        if has_direction:
            negative = e.get("direction") == "-"
        else:
            axis = str(e.get("axis") or "")
            claim = str(e.get("claim") or "")
            negative = (axis in _RISK_AXES) and any(w in claim for w in _NEGATIVE_WORDS)
        if not negative:
            continue
        if fid in jtext:
            continue  # 純比對找得到，不出題
        n += 1
        ctx_obj = {"id": fid, "axis": e.get("axis"), "claim": e.get("claim"),
                   "source": e.get("source"), "as_of": e.get("as_of")}
        out.append({
            "id": "C{0}".format(n), "kind": "noul", "question": _C_QUESTION, "options": list(_C_OPTIONS),
            "context": json.dumps(ctx_obj, ensure_ascii=False),
            "_finding_id": fid,
        })
    return out


_H_QUESTION = "oneliner 的方向是哪個？"
_H_OPTIONS = ["進場", "觀望", "迴避", "看不出"]


def expand_H(judgment):
    """H 類（裁決與一句話方向一致）。一題 choice，context 是 `oneliner` 全文。"""
    oneliner = judgment.get("oneliner") or ""
    return [{
        "id": "H1", "kind": "choice", "question": _H_QUESTION, "options": list(_H_OPTIONS),
        "context": oneliner,
    }]


# ---------------------------------------------------------------------------
# apply_decisions：信心分流＋高信心機械處置
# ---------------------------------------------------------------------------

_BULL_PCT_RE = re.compile(r"bull[^0-9]{0,12}(\d{1,2})%", re.IGNORECASE)


def _judgment_path_for(cat, q):
    if cat == "A":
        idx = q.get("_r_index")
        return "$.thesis.R[{0}].threshold".format(idx) if idx is not None else "$.thesis.R"
    if cat == "B":
        return "$.counter_evidence.action_conditions.{0}".format(q.get("_source") or "exec_line")
    if cat == "C":
        return "$.counter_evidence.contradictions"
    if cat == "H":
        return "$.oneliner"
    return "$"


def _mid_reason(cat, q, d):
    conf = float(d.get("confidence") or 0.0)
    return "{0}（模型答「{1}」，信心 {2:.2f}，未達 0.95 機械處置門檻，轉交閘複審）".format(
        q.get("question"), d.get("answer"), conf)


def _apply_A_hit(q, d, judgment, scenario_state, overrides):
    idx = q.get("_r_index")
    r_id = q.get("_r_id")
    threshold = q.get("_threshold") or ""
    conf = float(d.get("confidence") or 0.0)
    r_list = ((judgment.get("thesis") or {}).get("R")) or []
    if idx is not None and 0 <= idx < len(r_list) and isinstance(r_list[idx], dict):
        r_list[idx]["triggered_by_evidence"] = True
        overrides.append({"judgment_path": "$.thesis.R[{0}].triggered_by_evidence".format(idx),
                          "change": "→ true", "r_id": r_id})
    path = "$.thesis.R[{0}].threshold".format(idx) if idx is not None else "$.thesis.R"
    m = _BULL_PCT_RE.search(threshold)
    if not m:
        reason = "{0} 門檻文字經自引證據判定已觸發（模型信心 {1:.2f}），機率待補丁輪處理".format(r_id, conf)
        return {"item": "M-{0}".format(q["id"]), "light": "🔴", "judgment_path": path, "reason": reason}
    new_bull = int(m.group(1))
    scenario = scenario_state["load"]()
    sc = (scenario or {}).get("scenarios") or {}
    bull_node, base_node = sc.get("bull"), sc.get("base")
    if not (isinstance(bull_node, dict) and isinstance(base_node, dict)
            and isinstance(bull_node.get("p"), (int, float)) and isinstance(base_node.get("p"), (int, float))):
        reason = ("{0} 門檻文字經自引證據判定已觸發（模型信心 {1:.2f}），"
                  "scenario.json 機率欄形狀不符，機率待補丁輪處理").format(r_id, conf)
        return {"item": "M-{0}".format(q["id"]), "light": "🔴", "judgment_path": path, "reason": reason}
    old_bull, old_base = bull_node["p"], base_node["p"]
    new_base = old_base + (old_bull - new_bull)
    bull_node["p"] = new_bull
    base_node["p"] = new_base
    scenario_state["mark_dirty"]()
    overrides.append({"file": "scenario.json", "path": "scenarios.bull.p", "old": old_bull, "new": new_bull, "r_id": r_id})
    overrides.append({"file": "scenario.json", "path": "scenarios.base.p", "old": old_base, "new": new_base, "r_id": r_id})
    reason = ("{0} 門檻文字經自引證據判定已觸發（模型信心 {1:.2f}）；"
             "bull 機率依門檻文字由 {2}% 改為 {3}%，base 吸收差額至 {4}%").format(
        r_id, conf, old_bull, new_bull, new_base)
    return {"item": "M-{0}".format(q["id"]), "light": "🔴", "judgment_path": path, "reason": reason}


def _apply_B_hit(q, d):
    conf = float(d.get("confidence") or 0.0)
    path = _judgment_path_for("B", q)
    reason = "進場路徑「{0}」未確認在約束（{1}）全部解除後才進場（模型信心 {2:.2f}）".format(
        q.get("_path_text"), q.get("_constraint"), conf)
    return {"item": "M-{0}".format(q["id"]), "light": "🔴", "judgment_path": path, "reason": reason}


def _apply_C_hit(q, d):
    conf = float(d.get("confidence") or 0.0)
    fid = q.get("_finding_id")
    try:
        ctx = json.loads(q.get("context") or "{}")
    except (TypeError, ValueError):
        ctx = {}
    claim = str(ctx.get("claim") or "")
    snippet = claim[:60] + ("…" if len(claim) > 60 else "")
    reason = "finding {0}（{1}）未見於判斷物任何段落，可能未被實質處理（模型信心 {2:.2f}）".format(fid, snippet, conf)
    return {"item": "M-{0}".format(q["id"]), "light": "🔴", "judgment_path": _judgment_path_for("C", q), "reason": reason}


def _apply_H_hit(q, d, judgment):
    conf = float(d.get("confidence") or 0.0)
    verdict = ((judgment.get("decision_out") or {}).get("verdict")) or "（無 decision_out.verdict）"
    reason = "oneliner 方向判定為「{0}」，與 decision_out.verdict「{1}」不同（模型信心 {2:.2f}）".format(
        d.get("answer"), verdict, conf)
    return {"item": "M-{0}".format(q["id"]), "light": "🔴", "judgment_path": "$.oneliner", "reason": reason}


def apply_decisions(run_dir, judgment, decisions, questions, thresholds=THRESHOLDS):
    """依信心分流：`decisions` 是 `decide_batch` 回傳的答案陣列（或形狀相同的
    假答案，供測試用），`questions` 是產生這些答案的題目（`expand_*` 的輸出，
    含 `_` 開頭的內部欄位）。回 dict：

        {"mechanical_items": [...], "mid_items": [...], "owner_queue": [...], "overrides": [...]}

    高信心（≥ thresholds[0]）且答案落在該類「異常」方向的，就地修改傳入的
    `judgment`（呼叫端負責寫回 `judgment.json`）與 `run_dir/scenario.json`
    （本函式直接寫回，因為只有這裡拿得到 `run_dir`），改動記進 `overrides`。
    高信心但答案是「正常」方向的（沒有異常）不進任何清單——沒有需要處置或
    複審的疑點。0.70–0.95 進 `mid_items`（🟡，附 `confidence`）；
    < 0.70 或 `valid=False` 進 `owner_queue`，不分答案方向（信心不足時，
    連「正常」的答案都不可信，一律轉交複審／裁示）。"""
    high, mid = thresholds
    run_dir = Path(run_dir)
    by_id = {q["id"]: q for q in questions}
    mechanical_items, mid_items, owner_queue, overrides = [], [], [], []
    verdict = (judgment.get("decision_out") or {}).get("verdict")

    scenario_path = run_dir / "scenario.json"
    _state = {"obj": None, "dirty": False}

    def _load_scenario():
        if _state["obj"] is None:
            _state["obj"] = _load_json(scenario_path) if scenario_path.exists() else {}
        return _state["obj"]

    def _mark_dirty():
        _state["dirty"] = True

    scenario_state = {"load": _load_scenario, "mark_dirty": _mark_dirty}

    for d in decisions:
        qid = d.get("id")
        q = by_id.get(qid)
        if q is None:
            continue
        cat = qid[:1] if qid else ""
        conf = float(d.get("confidence") or 0.0)
        valid = bool(d.get("valid"))
        answer = d.get("answer")

        if (not valid) or conf < mid:
            owner_queue.append({"id": qid, "question": q.get("question"), "answer": answer,
                                "confidence": conf, "note": d.get("note")})
            continue

        if cat == "A":
            hit = answer == "是"
        elif cat == "B":
            hit = answer == "否"
        elif cat == "C":
            hit = answer == "沒有"
        elif cat == "H":
            hit = (answer != "看不出") and (verdict is not None) and (answer != verdict)
        else:
            hit = False

        if conf >= high:
            if not hit:
                continue
            if cat == "A":
                item = _apply_A_hit(q, d, judgment, scenario_state, overrides)
            elif cat == "B":
                item = _apply_B_hit(q, d)
            elif cat == "C":
                item = _apply_C_hit(q, d)
            elif cat == "H":
                item = _apply_H_hit(q, d, judgment)
            else:
                continue
            mechanical_items.append(item)
        else:
            mid_items.append({"item": qid, "light": "🟡", "judgment_path": _judgment_path_for(cat, q),
                              "reason": _mid_reason(cat, q, d), "confidence": conf})

    if _state["dirty"]:
        _atomic_write_json(scenario_path, _state["obj"])

    return {"mechanical_items": mechanical_items, "mid_items": mid_items,
            "owner_queue": owner_queue, "overrides": overrides}


# ---------------------------------------------------------------------------
# run_mechanical_gate：串起來，落檔
# ---------------------------------------------------------------------------

def _write_owner_queue(run_dir, owner_queue):
    path = Path(run_dir) / "owner_queue.md"
    if not owner_queue:
        if path.exists():
            path.unlink()
        return
    lines = ["# owner queue（decide.py 機械閘，低信心待裁示）", ""]
    for item in owner_queue:
        lines.append("- [ ] {0} {1} → 模型答 {2}（信心 {3:.2f}）".format(
            item.get("id"), item.get("question"), item.get("answer"), float(item.get("confidence") or 0.0)))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_mechanical_gate(ctx, st, *, model=DEFAULT_MODEL, effort=DEFAULT_EFFORT, batch_size=DEFAULT_BATCH_SIZE):
    """串 `expand_*` → `decide_batch` → `apply_decisions`，落檔
    `run_dir/mechanical_gate.json`（題目、答案、分流結果、usage）與
    `run_dir/owner_queue.md`（空清單就刪除既有檔，不寫新檔）。

    `ctx` 只用到 `run_dir`；若 `ctx` 帶 `manifest`（dict，`run.py::Ctx` 的
    慣例），高信心覆寫會比照 `run.py::_write_judgment` 的作法記進
    `manifest["mechanical_overrides"]`——找不到這個屬性就跳過，本函式不因此
    耦合 `run.py::Ctx` 這個類別本身（duck typing，供 CLI 直接用一個最小假
    ctx 呼叫，見 `main()`）。`st` 是呼叫端的 stage dict（例如
    `ctx.manifest["stages"]["gated"]`），這裡只加一個 `st["mechanical_gate"]`
    摘要鍵，不動 `st` 其他既有欄位。

    回傳 dict：`{"questions","decisions","mechanical_items","mid_items",
    "owner_queue","overrides","usage"}`（`questions` 已濾掉 `_` 開頭的內部
    欄位，是落進 `mechanical_gate.json` 的同一份）。"""
    run_dir = Path(ctx.run_dir)
    judgment_path = run_dir / "judgment.json"
    facts_path = run_dir / "facts.json"
    judgment = _load_json(judgment_path)
    facts = _load_json(facts_path)

    questions = []
    questions += expand_A(judgment, facts)
    questions += expand_B(judgment)
    questions += expand_C(judgment, facts)
    questions += expand_H(judgment)

    usage = []
    decisions = []
    agents_dir = run_dir / "agents"
    for cat in ("A", "B", "C", "H"):
        qs = [q for q in questions if q["id"][:1] == cat]
        if not qs:
            continue
        decisions.extend(decide_batch(run_dir, qs, model=model, effort=effort, batch_size=batch_size,
                                      agents_dir=agents_dir, label_prefix="decide_{0}".format(cat),
                                      usage_sink=usage))

    result = apply_decisions(run_dir, judgment, decisions, questions, thresholds=THRESHOLDS)

    if result.get("overrides"):
        _atomic_write_json(judgment_path, judgment)

    manifest = getattr(ctx, "manifest", None)
    if isinstance(manifest, dict) and result.get("overrides"):
        manifest.setdefault("mechanical_overrides", []).extend(result["overrides"])

    public_questions = [{k: v for k, v in q.items() if not k.startswith("_")} for q in questions]
    payload = {"questions": public_questions, "decisions": decisions,
               "mechanical_items": result["mechanical_items"], "mid_items": result["mid_items"],
               "owner_queue": result["owner_queue"], "overrides": result["overrides"], "usage": usage}
    _atomic_write_json(run_dir / "mechanical_gate.json", payload)
    _write_owner_queue(run_dir, result["owner_queue"])

    if isinstance(st, dict):
        st["mechanical_gate"] = {"n_questions": len(questions), "n_red": len(result["mechanical_items"]),
                                 "n_mid": len(result["mid_items"]), "n_owner_queue": len(result["owner_queue"]),
                                 "usage_n": len(usage)}
    return payload


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class _SimpleCtx:
    """`run_mechanical_gate` 只用到 `run_dir`／`manifest` 兩個屬性，CLI 獨立
    跑不需要完整的 `run.py::Ctx`。"""

    def __init__(self, run_dir):
        self.run_dir = run_dir
        self.manifest = {}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir_name", help="如 MU_20260917（對應 .dd_build/runs/<run_dir_name>/）")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--effort", default=DEFAULT_EFFORT)
    ap.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    ap.add_argument("--offline", action="store_true", help="只展開題目印出來，不呼叫模型")
    args = ap.parse_args(argv)

    run_dir = REPO_ROOT / ".dd_build" / "runs" / args.run_dir_name
    if not (run_dir / "judgment.json").exists():
        print("[error] 找不到 judgment.json：{0}".format(run_dir), file=sys.stderr)
        return 1
    judgment = _load_json(run_dir / "judgment.json")
    facts = _load_json(run_dir / "facts.json")

    if args.offline:
        questions = expand_A(judgment, facts) + expand_B(judgment) + expand_C(judgment, facts) + expand_H(judgment)
        for q in questions:
            print("{0}\t{1}\t{2}".format(q["id"], q["kind"], q["question"]))
            print("  options: {0}".format(q["options"]))
            print("  context: {0}".format((q.get("context") or "")[:200]))
        print("共 {0} 題（A {1}／B {2}／C {3}／H {4}）".format(
            len(questions), sum(1 for q in questions if q["id"][0] == "A"),
            sum(1 for q in questions if q["id"][0] == "B"), sum(1 for q in questions if q["id"][0] == "C"),
            sum(1 for q in questions if q["id"][0] == "H")))
        return 0

    ctx = _SimpleCtx(run_dir)
    st = {}
    payload = run_mechanical_gate(ctx, st, model=args.model, effort=args.effort, batch_size=args.batch_size)
    cost = sum(u.get("cost_usd") or 0.0 for u in payload["usage"])
    print(json.dumps({"summary": st.get("mechanical_gate"), "cost_usd": round(cost, 4),
                      "mechanical_items": payload["mechanical_items"], "mid_items": payload["mid_items"],
                      "owner_queue_n": len(payload["owner_queue"])}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
