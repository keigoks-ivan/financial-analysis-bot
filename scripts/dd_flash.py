#!/usr/bin/env python3
"""scripts/dd_flash.py — 閃判（即時裁決層）。

持有人「我現在想知道這檔」的即時需求：目標 5 到 7 分鐘、約 $2 到 3 出一份
**初判**。輕量證據（零 LLM 數字包＋前份 DD＋沿用或輕量蒐集的事件與逐字稿
摘要）＋Fable 一次判斷（規則與正式版同一份 judgment-rules.md）＋**同一張
決策矩陣**（`dd_decision.py`）算裁決；無跨模型閘、不寫 `docs/`、不進任何
名單；產物頂端固定標「即時版，未經跨模型閘」。

本檔只 import／subprocess 呼叫既有腳本（`ddreport.py`／`dd_headless.py`／
`dd_prior.py`／`dd_numbers_extra.py`／`dd_scenario.py`／`dd_decision.py`／
`dd_bundle.py`／`validate_judgment.py`），不改動它們的行為或語意。

Python 3.9 相容（`from __future__ import annotations`，不用 3.10+ 執行期
語法）。

用法：
    python3 scripts/dd_flash.py TICKER [--date YYYYMMDD] [--peers a,b]
        [--no-web] [--judgment-model fable] [--dry-run]

流程：見 notes/site-internal/dd（本檔各步驟對應函式見下方各區塊註解）。
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ddreport  # noqa: E402 —— 只 import 其函式／常數，不改其行為
import dd_headless  # noqa: E402
import dd_bundle  # noqa: E402 —— 重用 _json_block／_judgment_rules_section／JUDGMENT_RULES_PATH
import validate_judgment  # noqa: E402 —— 重用 leak_and_punct_checks（QC-40 詞表單一權威）

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
PROMPTS_TMPL_DIR = SCRIPTS_DIR / "dd_prompts"
JUDGMENT_SCHEMA_PATH = SCRIPTS_DIR / "dd_schema" / "judgment.schema.json"

# 獨立於正式管線的 `.dd_build/runs/`，避免和三步制彼此互相踩腳。
FLASH_BUILD_DIR = REPO_ROOT / ".dd_build" / "flash"
# 不寫 docs/——輸出只落在站內筆記目錄，供人工複審與後續決定要不要跑正式版。
FLASH_OUTPUT_DIR = REPO_ROOT / "notes" / "site-internal" / "dd" / "_flash"

FLASH_JUDGE_TMPL_PATH = PROMPTS_TMPL_DIR / "flash_judge.md.tmpl"
FLASH_EVENTS_TMPL_PATH = PROMPTS_TMPL_DIR / "flash_events.md.tmpl"

FLASH_JUDGE_MODEL_DEFAULT = "fable"
FLASH_JUDGE_BUDGET_CACHE_READ = 400_000

FLASH_EVENTS_MODEL = "sonnet"
FLASH_EVENTS_MAX_TURNS = 8  # 2026-09-06 WDC 首跑：三次搜尋＋Write 用了 7 輪，6 太緊
FLASH_EVENTS_TOOLS = ["WebSearch", "WebFetch", "Write"]
FLASH_EVENTS_BUDGET_CACHE_READ = 500_000

EVIDENCE_REUSE_MAX_AGE_DAYS = 90

# flash schema 頂層鍵（見 `flash_judge.md.tmpl` 的 flash schema 段；單一權威
# 是模板本身，這裡只列鍵名供機械檢查用，不重複判斷語意）。
FLASH_TOP_KEYS = [
    "meta", "oneliner", "archetype", "decision_inputs", "inputs_basis",
    "expected", "plain", "reasoning", "evidence_gaps", "escalate",
]

# evidence.json 頂層 `events` 物件的五個固定子鍵（QC-19，見 ddreport.py
# EVENTS_ADDENDUM）；沿用既有 _src 證據包時原樣取出。
_EVENTS_SUBKEYS = [
    "ma_merger", "lawsuit_class_action", "clinical_fda",
    "product_recall_warning", "sec_investigation_restatement",
]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def _run_dir(ticker, date):
    return FLASH_BUILD_DIR / "{0}_{1}".format(ticker, date)


def _date_iso(date_yyyymmdd):
    return "{0}-{1}-{2}".format(date_yyyymmdd[:4], date_yyyymmdd[4:6], date_yyyymmdd[6:8])


def _json_section(heading, obj, note=None):
    lines = [heading, ""]
    if note:
        lines.append(note)
        lines.append("")
    lines.append(dd_bundle._json_block(obj or {}))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 步驟 2：零 LLM 準備（dd_prior.py／dd_numbers_extra.py，平行跑）
# ---------------------------------------------------------------------------

def _run_zero_llm_prep(py, ticker, date, parts_dir, peers_str):
    """平行跑 `dd_prior.py`／`dd_numbers_extra.py`；任一失敗只記 gap 不中止。
    回傳 (prior_obj, numbers_obj, gap_messages)。"""
    prior_out = parts_dir / "prior.json"
    numbers_out = parts_dir / "numbers_extra.json"
    gaps = []

    def _run_prior():
        return subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_prior.py"), ticker, "--date", date,
             "--out", str(prior_out)],
            capture_output=True, text=True,
        )

    def _run_numbers():
        cmd = [py, str(SCRIPTS_DIR / "dd_numbers_extra.py"), ticker, date,
               "--out", str(numbers_out)]
        if peers_str:
            cmd += ["--peers", peers_str]
        return subprocess.run(cmd, capture_output=True, text=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f_prior = ex.submit(_run_prior)
        f_numbers = ex.submit(_run_numbers)
        r_prior = f_prior.result()
        r_numbers = f_numbers.result()

    prior_obj = {}
    if r_prior.returncode != 0:
        gaps.append("prior_dd：dd_prior.py 失敗（exit {0}）：{1}".format(
            r_prior.returncode, (r_prior.stderr or "").strip()[-300:]))
    elif prior_out.exists():
        try:
            prior_obj = ddreport._load_json(prior_out)
        except Exception as e:
            gaps.append("prior_dd：prior.json 解析失敗：{0}".format(e))

    numbers_obj = {}
    if r_numbers.returncode != 0:
        gaps.append("numbers：dd_numbers_extra.py 失敗（exit {0}）：{1}".format(
            r_numbers.returncode, (r_numbers.stderr or "").strip()[-300:]))
    elif numbers_out.exists():
        try:
            numbers_obj = ddreport._load_json(numbers_out)
        except Exception as e:
            gaps.append("numbers：numbers_extra.json 解析失敗：{0}".format(e))

    if not peers_str:
        gaps.append("peers：未給 --peers 且找不到歷史 evidence／id-meta 可回退，僅算自身一列")

    return prior_obj, numbers_obj, gaps


# ---------------------------------------------------------------------------
# 步驟 2：證據沿用（90 天內最新一份 _src evidence／transcript_digest）
# ---------------------------------------------------------------------------

_SRC_DIR_DATE_RE_TMPL = r"^{0}_(\d{{8}})$"


def _find_reusable_evidence(ticker, run_date):
    """在 `ddreport.SRC_ARCHIVE_DIR` 找 `{T}_YYYYMMDD/` 資料夾，回傳 90 天內
    最新一份的 (evidence_path_or_None, digest_path_or_None, age_days_or_None)。
    找不到任何符合窗口的資料夾則三者皆 None。"""
    src_dir = ddreport.SRC_ARCHIVE_DIR
    if not src_dir.exists():
        return None, None, None
    run_dt = datetime.strptime(run_date, "%Y%m%d")
    pat = re.compile(_SRC_DIR_DATE_RE_TMPL.format(re.escape(ticker)))
    candidates = []
    for p in src_dir.glob("{0}_*".format(ticker)):
        if not p.is_dir():
            continue
        m = pat.match(p.name)
        if not m:
            continue
        try:
            src_dt = datetime.strptime(m.group(1), "%Y%m%d")
        except ValueError:
            continue
        age = (run_dt - src_dt).days
        if abs(age) > EVIDENCE_REUSE_MAX_AGE_DAYS:
            continue
        candidates.append((src_dt, abs(age), p))
    if not candidates:
        return None, None, None
    candidates.sort(key=lambda t: t[0], reverse=True)
    _, age_days, p = candidates[0]
    ev_path = p / "{0}.evidence.json".format(p.name)
    dig_path = p / "{0}.transcript_digest.json".format(p.name)
    return (
        ev_path if ev_path.exists() else None,
        dig_path if dig_path.exists() else None,
        age_days,
    )


def _extract_events_from_evidence(evidence_obj):
    """取沿用 evidence.json 的 `coverage.major_events` 與頂層 `events` 五組。"""
    coverage = (evidence_obj or {}).get("coverage") or {}
    events_top = (evidence_obj or {}).get("events") or {}
    out = {"major_events": coverage.get("major_events")}
    for k in _EVENTS_SUBKEYS:
        out[k] = events_top.get(k)
    return out


def _extract_latest_quarter_digest(digest_obj):
    """取 `transcript_digest.json` 最新一季（`items[].date` 最大值那組）的
    items，零 LLM、確定性篩選。"""
    digest_obj = digest_obj or {}
    items = digest_obj.get("items") or []
    if not items:
        return {"source_files": digest_obj.get("source_files") or [], "items": [], "qa_flags": []}
    dates = [it.get("date") for it in items if it.get("date")]
    if not dates:
        return {
            "source_files": digest_obj.get("source_files") or [],
            "items": items,
            "qa_flags": digest_obj.get("qa_flags") or [],
        }
    latest = max(dates)
    latest_items = [it for it in items if it.get("date") == latest]
    return {
        "source_files": digest_obj.get("source_files") or [],
        "quarter_date": latest,
        "items": latest_items,
        "qa_flags": digest_obj.get("qa_flags") or [],
    }


# ---------------------------------------------------------------------------
# 步驟 2 缺口回退：events 找不到沿用來源時，派一個 sonnet agent 輕量蒐集
# ---------------------------------------------------------------------------

def _spawn_events_agent(ticker, date_iso, run_dir):
    events_out = run_dir / "parts" / "events.json"
    prompt_path = run_dir / "prompts" / "flash_events.md"
    mapping = {"ticker": ticker, "date": date_iso, "out": str(events_out)}
    prompt_text = ddreport._render_format_template(FLASH_EVENTS_TMPL_PATH, mapping)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt_text, encoding="utf-8")

    r = dd_headless.spawn(
        prompt_path=prompt_path, model=FLASH_EVENTS_MODEL,
        allowed_tools=FLASH_EVENTS_TOOLS, max_turns=FLASH_EVENTS_MAX_TURNS,
        budget_cache_read=FLASH_EVENTS_BUDGET_CACHE_READ,
        out_json=run_dir / "agents" / "events_raw.json", cwd=run_dir,
    )
    r = dict(r)
    r["id"] = "events"

    events_obj = None
    if events_out.exists():
        try:
            events_obj = ddreport._load_json(events_out)
        except Exception:
            events_obj = None
    return events_obj, r


# ---------------------------------------------------------------------------
# 步驟 3：bundle 組裝
# ---------------------------------------------------------------------------

def _bundle_header(ticker, date_iso, price, evidence_age_days, has_digest, has_events):
    return (
        "## 閃判 bundle 標頭\n\n"
        "ticker={0}　date={1}　price={2}　evidence_age_days={3}　digest={4}　events={5}".format(
            ticker, date_iso,
            price if price is not None else "無",
            evidence_age_days if evidence_age_days is not None else "無沿用來源",
            "有" if has_digest else "無", "有" if has_events else "無",
        )
    )


def _build_bundle_sections(ticker, date_iso, price, evidence_age_days,
                            numbers_obj, prior_obj, digest_obj, events_obj,
                            digest_note, events_note):
    numbers_payload = (numbers_obj or {}).get("numbers") or {}
    prior_dd_payload = (prior_obj or {}).get("prior_dd") or {}
    sections = [
        ("header", _bundle_header(
            ticker, date_iso, price, evidence_age_days,
            bool(digest_obj), bool(events_obj))),
        ("judgment_rules", dd_bundle._judgment_rules_section(dd_bundle.JUDGMENT_RULES_PATH)),
        ("numbers", _json_section("## numbers（緊湊 JSON）", numbers_payload)),
        ("prior_dd", _json_section("## prior_dd（緊湊 JSON）", prior_dd_payload)),
        ("digest", _json_section("## digest（緊湊 JSON）", digest_obj, note=digest_note)),
        ("events", _json_section("## events（緊湊 JSON）", events_obj, note=events_note)),
    ]
    return sections


def _write_bundle(sections, bundle_path):
    text = "\n\n---\n\n".join(t for _, t in sections) + "\n"
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path.write_text(text, encoding="utf-8")
    return text


# ---------------------------------------------------------------------------
# 步驟 4：判斷（無工具單輪，接受 json:flash／json:scenario 標籤）
# ---------------------------------------------------------------------------

_FLASH_FENCE_TAGS = ("flash", "scenario")


def _parse_flash_oneshot(text):
    """從一次性呼叫回覆抽 `json:flash`／`json:scenario` 兩個 fenced JSON 區塊。
    任一缺席或解析失敗都回傳 None（由呼叫端決定重試或放棄）。"""
    text = text or ""
    out = {}
    for tag in _FLASH_FENCE_TAGS:
        m = re.search(r"```json:{0}[ \t]*\n(.*?)\n```".format(tag), text, re.S)
        if not m:
            return None
        try:
            obj = json.loads(m.group(1))
        except (json.JSONDecodeError, ValueError):
            return None
        if not isinstance(obj, dict):
            return None
        out[tag] = obj
    return out


def _run_judge(ticker, date_iso, run_dir, model):
    """跑判斷 oneshot；解析失敗重試一次（同 prompt）；仍失敗回傳
    (None, usage_list)。"""
    prompt_path = run_dir / "prompts" / "flash_judge.md"
    bundle_path = run_dir / "bundles" / "flash.md"
    mapping = {"ticker": ticker, "date": date_iso}
    prompt_text = ddreport._render_format_template(FLASH_JUDGE_TMPL_PATH, mapping)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt_text, encoding="utf-8")
    inline_path = ddreport._write_inline_prompt(prompt_path, bundle_path)

    usages = []

    r1 = ddreport._spawn_oneshot(
        inline_path, model, run_dir / "agents" / "judge_raw.json", run_dir,
        FLASH_JUDGE_BUDGET_CACHE_READ,
    )
    r1 = dict(r1)
    r1["id"] = "judge"
    usages.append(r1)
    parsed = _parse_flash_oneshot(r1.get("result_text"))
    if parsed is not None:
        return parsed, usages

    r2 = ddreport._spawn_oneshot(
        inline_path, model, run_dir / "agents" / "judge_retry_raw.json", run_dir,
        FLASH_JUDGE_BUDGET_CACHE_READ,
    )
    r2 = dict(r2)
    r2["id"] = "judge_retry"
    usages.append(r2)
    parsed = _parse_flash_oneshot(r2.get("result_text"))
    return parsed, usages


# ---------------------------------------------------------------------------
# 步驟 5：算術與裁決（dd_scenario.py → decision_inputs 回填 → dd_decision.py run）
# ---------------------------------------------------------------------------

def _run_scenario(py, run_dir):
    """跑 `dd_scenario.py scenario.json --meta scenario_meta.json`。回傳
    (scenario_meta_dict, fail_text_or_None)。FAIL 時若仍寫出 scenario_meta.json
    （只是驗證沒過，非重算崩潰），數字照樣回填、只標記 FAIL 原文；真的崩潰
    （連 meta 都沒寫出）則回傳空 dict。"""
    scenario_path = run_dir / "scenario.json"
    scenario_meta_path = run_dir / "scenario_meta.json"
    r = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_scenario.py"), str(scenario_path),
         "--meta", str(scenario_meta_path),
         "--html", str(run_dir / "tables" / "e11.html")],
        capture_output=True, text=True,
    )
    scenario_meta = {}
    if scenario_meta_path.exists():
        try:
            scenario_meta = ddreport._load_json(scenario_meta_path)
        except Exception:
            scenario_meta = {}
    fail_text = None
    if r.returncode != 0:
        fail_text = ((r.stdout or "") + (r.stderr or "")).strip()
    return scenario_meta, fail_text


def _run_decision_matrix(py, run_dir, flash_path):
    """把 flash.json（已補 `decision_out: {}` 占位鍵，觸發
    `dd_decision.py run` 的「完整 judgment.json」合併路徑，不觸發它「裸
    decision_inputs 覆寫整檔」的舊行為，見 `dd_decision.py::cmd_run`）餵
    `dd_decision.py run --json flash.json`。回傳 (ok, stderr_text)。"""
    r = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_decision.py"), "run", str(flash_path),
         "--json", str(flash_path),
         "--html", str(run_dir / "tables" / "audit.html")],
        capture_output=True, text=True,
    )
    return r.returncode == 0, ((r.stdout or "") + (r.stderr or "")).strip()


# ---------------------------------------------------------------------------
# 步驟 6：零 LLM 檢查（schema 最小檢查／plain 洩漏／expected 對帳）
# ---------------------------------------------------------------------------

def _load_judgment_schema():
    return json.loads(JUDGMENT_SCHEMA_PATH.read_text(encoding="utf-8"))


def _schema_min_check(flash_obj):
    """頂層鍵、`decision_inputs` 全部必填鍵存在、enum 值合法——enum 一律從
    `judgment.schema.json` 讀，不自建一份。回傳錯誤字串清單（空＝通過）。"""
    errors = []
    for k in FLASH_TOP_KEYS:
        if k not in flash_obj:
            errors.append("缺頂層鍵：{0}".format(k))

    schema = _load_judgment_schema()
    di_schema = (schema.get("properties") or {}).get("decision_inputs") or {}
    required = di_schema.get("required") or []
    props = di_schema.get("properties") or {}

    di = flash_obj.get("decision_inputs") or {}
    for k in required:
        if k not in di:
            errors.append("decision_inputs 缺鍵：{0}".format(k))

    for k, v in di.items():
        prop = props.get(k)
        if not prop:
            continue
        enum = prop.get("enum")
        if enum is not None and v not in enum:
            errors.append(
                "decision_inputs.{0} 值 {1!r} 不在合法 enum {2!r}".format(k, v, enum)
            )
    return errors


def _expected_mismatch(flash_obj):
    expected = flash_obj.get("expected") or {}
    do = flash_obj.get("decision_out") or {}
    issues = []
    exp_verdict = expected.get("verdict")
    exp_role = expected.get("role")
    if exp_verdict and do.get("verdict") and exp_verdict != do.get("verdict"):
        issues.append(
            "白話預期與矩陣不一致：expected.verdict={0!r} vs decision_out.verdict={1!r}".format(
                exp_verdict, do.get("verdict"))
        )
    if exp_role and do.get("role") and exp_role != do.get("role"):
        issues.append(
            "白話預期與矩陣不一致：expected.role={0!r} vs decision_out.role={1!r}".format(
                exp_role, do.get("role"))
        )
    return issues


# ---------------------------------------------------------------------------
# 步驟 8：用量彙總
# ---------------------------------------------------------------------------

def _summarize_usage(run_dir, spawn_usages):
    total_cache_read = sum(int(u.get("cache_read") or 0) for u in spawn_usages)
    total_cache_creation = sum(int(u.get("cache_creation") or 0) for u in spawn_usages)
    total_output = sum(int(u.get("output_tokens") or 0) for u in spawn_usages)
    total_cost = sum(float(u.get("cost_usd") or 0.0) for u in spawn_usages)

    print("-- 用量 --")
    for u in spawn_usages:
        print("{0}／turns={1}／cache_read={2}／output={3}／cost=${4}".format(
            u.get("id"), u.get("num_turns"), u.get("cache_read"),
            u.get("output_tokens"), u.get("cost_usd"),
        ))
    print("合計／cache_read={0}／cache_creation={1}／output={2}／cost=${3:.4f}".format(
        total_cache_read, total_cache_creation, total_output, total_cost))

    token_obj = {
        "agents": spawn_usages,
        "totals": {
            "cache_read": total_cache_read,
            "cache_creation": total_cache_creation,
            "output_tokens": total_output,
            "cost_usd": total_cost,
        },
    }
    ddreport._atomic_write_json(run_dir / "token.json", token_obj)
    return total_cache_read, total_cost


# ---------------------------------------------------------------------------
# 步驟 7：一頁 markdown 輸出
# ---------------------------------------------------------------------------

def _fmt_pct(v):
    if v is None:
        return "—"
    try:
        return "{0:.1f}%".format(float(v))
    except (TypeError, ValueError):
        return str(v)


def _render_markdown(ticker, flash_obj, evidence_age_days, elapsed_min,
                      total_cache_read, red_flags, evidence_gaps):
    di = flash_obj.get("decision_inputs") or {}
    do = flash_obj.get("decision_out") or {}
    plain = flash_obj.get("plain") or {}
    reasoning = flash_obj.get("reasoning") or {}
    escalate = flash_obj.get("escalate") or {}
    inputs_basis = flash_obj.get("inputs_basis") or {}
    five = plain.get("five") or {}

    lines = []
    age_txt = "{0}天前".format(evidence_age_days) if evidence_age_days is not None else "無沿用"
    lines.append(
        "⚡ 即時版（閃判）· 未經跨模型閘 · 證據包{0} · 用時{1:.1f}分 · 全帳{2:.1f}M".format(
            age_txt, elapsed_min, total_cache_read / 1_000_000.0
        )
    )
    lines.append("")

    lines.append("## 統一裁決")
    lines.append("")
    lines.append("裁決：**{0}**　角色：**{1}**　命中列：{2}".format(
        do.get("verdict") or "—", do.get("role") or "—", do.get("row_hit") or "—",
    ))
    lines.append("")
    lines.append(plain.get("verdict_line") or "")
    lines.append(plain.get("verdict_sub") or "")
    lines.append("")

    lines.append("## 三個數字")
    lines.append("")
    lines.append("5Y EV：{0}　IRR base：{1}　p_bull／p_bear：{2}／{3}　Max DD：{4}".format(
        _fmt_pct(di.get("ev5y_pct")), _fmt_pct(di.get("irr_base_pct")),
        di.get("p_bull_pct") if di.get("p_bull_pct") is not None else "—",
        di.get("p_bear_pct") if di.get("p_bear_pct") is not None else "—",
        _fmt_pct(di.get("max_dd_pct")),
    ))
    lines.append("")

    lines.append("## 五問")
    lines.append("")
    for k, label in (
        ("how_it_makes_money", "怎麼賺錢"), ("why_now", "為何是現在"),
        ("why_this_size", "為何這個部位大小"), ("biggest_fear", "最怕什麼"),
        ("how_to_act", "怎麼做"),
    ):
        lines.append("- **{0}**：{1}".format(label, five.get(k) or "—"))
    lines.append("")

    lines.append("## 三押注")
    lines.append("")
    for b in (plain.get("bets") or []):
        if not b:
            continue
        lines.append("- {0}（錯了的話：{1}）".format(b.get("claim") or "—", b.get("wrong_when") or "—"))
    lines.append("")

    lines.append("## 三怕")
    lines.append("")
    for f in (plain.get("fears") or []):
        if not f:
            continue
        lines.append("- {0} {1}".format(f.get("clock") or "", f.get("text") or "—"))
    lines.append("")

    lines.append("## 改變心意條件")
    lines.append("")
    for c in (plain.get("change_my_mind") or []):
        if not c:
            continue
        lines.append("- {0}（門檻：{1}；則：{2}；時點：{3}）".format(
            c.get("what") or "—", c.get("threshold") or "—",
            c.get("then") or "—", c.get("when") or "—",
        ))
    lines.append("")

    lines.append("## inputs_basis")
    lines.append("")
    lines.append("| 欄 | 值 | 依據 |")
    lines.append("|---|---|---|")
    for k, basis in inputs_basis.items():
        lines.append("| {0} | {1} | {2} |".format(k, di.get(k), basis))
    lines.append("")

    lines.append("## decision_out 稽核（命中列）")
    lines.append("")
    lines.append("| row | condition | basis |")
    lines.append("|---|---|---|")
    for row in (do.get("audit_rows") or []):
        if not row.get("hit"):
            continue
        lines.append("| {0} | {1} | {2} |".format(
            row.get("row"), row.get("condition"), row.get("basis"),
        ))
    lines.append("")

    if reasoning:
        lines.append("## 判斷理由")
        lines.append("")
        for k, label in (("valuation", "估值"), ("growth", "成長"),
                          ("moat", "護城河"), ("scenario", "情境樹")):
            if reasoning.get(k):
                lines.append("- **{0}**：{1}".format(label, reasoning.get(k)))
        lines.append("")

    if plain.get("evidence_quality"):
        lines.append("證據品質：{0}".format(plain.get("evidence_quality")))
        lines.append("")
    if plain.get("prior_compare_reason"):
        lines.append("與前份比較：{0}".format(plain.get("prior_compare_reason")))
        lines.append("")

    lines.append("## evidence_gaps")
    lines.append("")
    all_gaps = list(evidence_gaps) + list(flash_obj.get("evidence_gaps") or [])
    if all_gaps:
        for g in all_gaps:
            lines.append("- {0}".format(g))
    else:
        lines.append("（無）")
    lines.append("")

    lines.append("## 🔴／⚠ 清單")
    lines.append("")
    if red_flags:
        for f in red_flags:
            lines.append("- 🔴 {0}".format(f))
    else:
        lines.append("（無）")
    lines.append("")

    lines.append("---")
    lines.append("{0}　排正式快速版：python3 scripts/ddreport.py batch {1}".format(
        escalate.get("why") or "", ticker,
    ))

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def build_arg_parser():
    ap = argparse.ArgumentParser(
        prog="dd_flash.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("ticker")
    ap.add_argument("--date", default=None, help="YYYYMMDD；省略則用今天")
    ap.add_argument("--peers", default=None, help="逗號分隔 ticker 清單")
    ap.add_argument("--no-web", action="store_true", help="不派 events 蒐集 agent")
    ap.add_argument("--judgment-model", default=FLASH_JUDGE_MODEL_DEFAULT)
    ap.add_argument("--dry-run", action="store_true", help="只組 bundle／prompt，不 spawn 判斷模型")
    return ap


def cmd_flash(args):
    ticker = args.ticker.strip().upper()
    date = args.date or time.strftime("%Y%m%d")
    date_iso = _date_iso(date)
    run_dir = _run_dir(ticker, date)
    parts_dir = run_dir / "parts"
    bundles_dir = run_dir / "bundles"
    tables_dir = run_dir / "tables"
    for d in (parts_dir, bundles_dir, tables_dir, run_dir / "prompts", run_dir / "agents"):
        d.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    spawn_usages = []
    py = ddreport._pick_python()

    # 步驟 2：零 LLM 準備（並行）＋ peers 解析（--peers → archive → id-meta）
    peers_str, _peers_src = ddreport._resolve_peers(args.peers, ticker)
    prior_obj, numbers_obj, evidence_gaps = _run_zero_llm_prep(
        py, ticker, date, parts_dir, peers_str,
    )

    # 步驟 2：證據沿用（90 天內 _src evidence／transcript_digest）
    ev_path, dig_path, evidence_age_days = _find_reusable_evidence(ticker, date)
    events_obj, digest_obj = None, None
    events_note, digest_note = None, None

    if ev_path is not None:
        events_obj = _extract_events_from_evidence(ddreport._load_json(ev_path))
        events_note = "（沿用 {0} 天前證據包：{1}）".format(evidence_age_days, ev_path)
    if dig_path is not None:
        digest_obj = _extract_latest_quarter_digest(ddreport._load_json(dig_path))
        digest_note = "（沿用 {0} 天前證據包最新一季：{1}）".format(evidence_age_days, dig_path)
    else:
        evidence_gaps.append(
            "digest：90 天內找不到可沿用的逐字稿摘要（{0}/{1}_*/）".format(
                ddreport.SRC_ARCHIVE_DIR, ticker)
        )

    if events_obj is None:
        if args.no_web:
            evidence_gaps.append("events：--no-web，未派 web 蒐集 agent")
            events_note = "（--no-web：未蒐集）"
        else:
            events_obj, usage = _spawn_events_agent(ticker, date_iso, run_dir)
            spawn_usages.append(usage)
            if events_obj is None:
                evidence_gaps.append("events：web 蒐集 agent 未產出（見 token.json 的 events 用量）")
                events_note = "（web 蒐集 agent 未產出）"
            else:
                events_note = "（web 蒐集，見 agents/events_raw.json）"

    # 步驟 3：bundle 組裝
    price = ((numbers_obj or {}).get("numbers") or {}).get("price_at_dd")
    sections = _build_bundle_sections(
        ticker, date_iso, price, evidence_age_days,
        numbers_obj, prior_obj, digest_obj, events_obj, digest_note, events_note,
    )
    bundle_path = bundles_dir / "flash.md"
    _write_bundle(sections, bundle_path)

    if args.dry_run:
        print("[dry-run] bundle 各段 bytes：")
        for label, text in sections:
            print("  {0}：{1} bytes".format(label, len(text.encode("utf-8"))))
        return 0

    # 步驟 4：判斷
    parsed, judge_usages = _run_judge(ticker, date_iso, run_dir, args.judgment_model)
    spawn_usages.extend(judge_usages)
    if parsed is None:
        print("[error] 判斷 agent 兩次都沒回傳合法的 json:flash／json:scenario 區塊", file=sys.stderr)
        _summarize_usage(run_dir, spawn_usages)
        return 1

    flash_obj = parsed["flash"]
    scenario_obj = parsed["scenario"]
    flash_path = run_dir / "flash.json"
    scenario_path = run_dir / "scenario.json"
    ddreport._atomic_write_json(scenario_path, scenario_obj)
    ddreport._atomic_write_json(flash_path, flash_obj)

    # 步驟 5：算術與裁決
    red_flags = []
    scenario_meta, scenario_fail_text = _run_scenario(py, run_dir)
    if scenario_fail_text:
        red_flags.append("情境樹驗證未過：{0}".format(scenario_fail_text))

    # ev5y_pct／irr_base_pct／asym_ratio 是矩陣 schema 本身的三個必填數字欄
    # （回填後才進 dd_decision.py）；p_bull_pct／p_bear_pct 不在矩陣 schema
    # 內，只是 scenario_meta 順手算出、供 markdown「三個數字」那行顯示用的
    # 額外欄位，塞進同一個 dict 純屬方便，不影響下面的矩陣 schema 檢查
    # （schema_min_check 只驗已知鍵，多餘鍵不算違規）。
    di = flash_obj.setdefault("decision_inputs", {})
    for k in ("ev5y_pct", "irr_base_pct", "asym_ratio", "p_bull_pct", "p_bear_pct"):
        if k in scenario_meta:
            di[k] = scenario_meta.get(k)

    flash_obj.setdefault("decision_out", {})
    ddreport._atomic_write_json(flash_path, flash_obj)

    decision_ok, decision_err = _run_decision_matrix(py, run_dir, flash_path)
    if decision_ok:
        flash_obj = ddreport._load_json(flash_path)
    else:
        red_flags.append("dd_decision.py run 失敗：{0}".format(decision_err[-500:]))

    # 步驟 6：零 LLM 檢查
    red_flags.extend("schema 最小檢查：{0}".format(e) for e in _schema_min_check(flash_obj))
    # 2026-09-06 WDC 首跑：洩漏詞表只該管讀者面文字（oneliner／plain）；expected、
    # reasoning、inputs_basis、evidence_gaps 是分析師面內部欄，本來就會寫 signal／
    # Veto／欄名，整份掃會誤報 5 條。
    reader_facing = {"oneliner": flash_obj.get("oneliner"), "plain": flash_obj.get("plain")}
    red_flags.extend(validate_judgment.leak_and_punct_checks(reader_facing))
    red_flags.extend(_expected_mismatch(flash_obj))

    # 步驟 8：用量彙總
    total_cache_read, _total_cost = _summarize_usage(run_dir, spawn_usages)

    # 步驟 7：一頁 markdown
    elapsed_min = (time.time() - start_time) / 60.0
    md = _render_markdown(
        ticker, flash_obj, evidence_age_days, elapsed_min, total_cache_read,
        red_flags, evidence_gaps,
    )
    print(md)

    FLASH_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_md_path = FLASH_OUTPUT_DIR / "{0}_{1}.md".format(ticker, date)
    out_md_path.write_text(md, encoding="utf-8")
    print("已寫 {0}".format(out_md_path), file=sys.stderr)

    return 0


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    return cmd_flash(args)


if __name__ == "__main__":
    sys.exit(main())
