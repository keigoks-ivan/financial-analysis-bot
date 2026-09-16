#!/usr/bin/env python3
"""scripts/dd2/bundle.py — DD 管線 v20 prompt bundle 組裝器。

契約見 `scripts/dd2/README.md` §4。三個 builder（`build_judge`／`build_gate`／
`build_prose`）各自把 `scripts/dd2/cards/*.md`（七張卡）與 `scripts/dd_bundle.py`
既有的零 LLM 段落函式，依 README §4 講定的順序組成一份 bundle，寫到
`run_dir/bundles/{judge,gate,prose}.md`；再把對應 `prompts/{judge,gate,prose}.md.tmpl`
任務頭接在 bundle 之前（分隔行沿用舊鏈 `ddreport.py` 的
`"\\n\\n===== BUNDLE =====\\n\\n"` 慣例），寫到 `run_dir/prompts/{judge,gate,prose}.md`
——這份合併檔才是真正餵給 `dd_headless.spawn` 的 prompt。

刻意不沿用（見 README §4「不放」清單）：`dd_bundle._evidence_compact`、
`_digest_section`、`_judgment_rules_section`、`_archetype_refs_section`、
`_gate_view_section`——這些屬於 v17／v19 舊鏈的胖段落或已被 v20 卡片取代。

只 import `dd_bundle.py`／`dd_project.py` 既有函式與常數，不改動這兩個檔案
一個字；不 import `ddreport.py`（避免拖進整條舊鏈的重依賴，本檔只需要它
「任務頭 + 分隔行 + bundle」這個慣例本身，另在本檔重寫一份同語意的小函式）。

Python 3.9 相容（`from __future__ import annotations`，不用 3.10+ 語法）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import dd_bundle  # noqa: E402 — 沿用其零 LLM 段落函式，見模組 docstring
import dd_project  # noqa: E402 — view_for／is_v19：v19 判斷檔 → 投影視圖

DD2_DIR = Path(__file__).resolve().parent
CARDS_DIR = DD2_DIR / "cards"
PROMPTS_DIR = DD2_DIR / "prompts"

# 舊鏈 `scripts/ddreport.py` 的 `BUNDLE_SEPARATOR`／`_write_inline_prompt` 同一慣例
# （任務頭 + 這行分隔 + bundle 全文＝真正餵給 LLM 的內容）；不 import ddreport.py，
# 原樣重寫這一行常數，語意不變。
BUNDLE_SEPARATOR = "\n\n===== BUNDLE =====\n\n"

# 前份判斷摘要硬上限（README §4）：超過就砍 H/R 的長文字欄。
PRIOR_SUMMARY_MAX_BYTES = 5000

# archetype → 附卡檔名。單一權威沿用 `dd_bundle.ARCHETYPE_REFS`（v18 舊鏈已有的
# archetype 分類表，不重複定義一次判準），只是把它原本指向的舊 reference 檔名
# （cyclical-lens.md／archetype-gatesets.md）換算成 v20 的對應附卡檔名。
_LEGACY_REF_TO_ADDENDUM = {
    "cyclical-lens.md": "judge_addendum_cyclical.md",
    "archetype-gatesets.md": "judge_addendum_archetype.md",
}


def _render_template(tmpl_path, mapping: dict) -> str:
    """`{{key}}` 字面取代，沿用 `scripts/ddreport.py::_render_template` 同一慣例
    （原樣重寫，不 import ddreport.py——見模組 docstring）。"""
    text = Path(tmpl_path).read_text(encoding="utf-8")
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def _card_section(label: str, card_path: Path) -> str:
    if not card_path.exists():
        return "## {0}\n\n[找不到卡片：{1}]".format(label, card_path)
    return "## {0}\n\n{1}".format(label, card_path.read_text(encoding="utf-8"))


def select_addenda(archetype_hint, cards_dir: Path = CARDS_DIR) -> list:
    """依 archetype_hint（evidence.archetype_hint，或 judgment.archetype 的
    primary 字串）對照各附卡檔頭 `load-when`，回傳要條件載入的附卡路徑清單。

    判準沿用 `dd_bundle.ARCHETYPE_REFS`（單一權威，不重複定義 archetype 分類），
    只是把它原本指向的 v18 reference 檔名換算成 v20 附卡檔名——`archetype_hint`
    本身只有一個值，同時拿來對 `judge_addendum_cyclical.md`（load-when 寫
    primary 或 secondary）與 `judge_addendum_archetype.md`（load-when 只寫
    primary）兩張卡的判準，命中就都算數。"""
    cards_dir = Path(cards_dir)
    refs = dd_bundle.ARCHETYPE_REFS.get(archetype_hint, [])
    seen = []
    for ref in refs:
        name = _LEGACY_REF_TO_ADDENDUM.get(ref)
        if name and name not in seen:
            seen.append(name)
    return [cards_dir / name for name in seen]


def _trim_prior_rows(node):
    """H／R 是 `{"status","format","rows":[{"id","text","columns":{...}}]}`；
    `columns` 是逐欄長文字（監測指標／警戒閾值），超字數時先丟這個，保留
    `id`／`text`（前份摘要仍看得出主張，只是不帶展開的逐欄細節）。"""
    if not isinstance(node, dict):
        return node
    rows = node.get("rows")
    if not isinstance(rows, list):
        return node
    trimmed = dict(node)
    trimmed["rows"] = [
        {"id": r.get("id"), "text": r.get("text")} if isinstance(r, dict) else r
        for r in rows
    ]
    return trimmed


def prior_summary(prior_json: dict) -> str:
    """從 `parts/prior.json` 的 `prior_dd` 取判斷摘要，回傳緊湊 JSON 字串
    （≤ `PRIOR_SUMMARY_MAX_BYTES`；超過就砍 H/R 的長文字欄，見
    `_trim_prior_rows`）。取 verdict／role／date／H／R／Single Thing／
    kill_metrics／rearm_trigger／irr／ev5y——欄位名依 schema 沿革不同代而異
    （legacy `prior_meta.verdict` vs v19 的 `dca_verdict`／`irr_base_pct` 等），
    `dca_*`／頂層值缺席時退回 `prior_meta` 對應欄；兩邊都沒有就是 `None`，
    不臆造。"""
    prior_dd = (prior_json or {}).get("prior_dd") or {}
    if prior_dd.get("status") != "ok":
        return json.dumps(
            {"status": prior_dd.get("status") or "none"},
            ensure_ascii=False, separators=(",", ":"),
        )
    prior_meta = prior_dd.get("prior_meta") or {}

    def pick(*paths):
        for container, key in paths:
            if isinstance(container, dict) and container.get(key) is not None:
                return container.get(key)
        return None

    summary = {
        "date": pick((prior_dd, "date"), (prior_meta, "date")),
        "verdict": pick((prior_dd, "dca_verdict"), (prior_meta, "verdict")),
        "role": pick((prior_dd, "dca_role"), (prior_meta, "dca_role")),
        "H": prior_dd.get("H"),
        "R": prior_dd.get("R"),
        "single_thing": pick((prior_dd, "single_thing"), (prior_dd, "Single Thing")),
        "kill_metrics": prior_dd.get("kill_metrics"),
        "rearm_trigger": pick((prior_dd, "rearm_trigger"), (prior_meta, "rearm_trigger")),
        "irr_base_pct": pick((prior_dd, "irr_base_pct"), (prior_meta, "irr_base_pct")),
        "ev5y_pct": pick((prior_dd, "ev5y_pct"), (prior_meta, "ev5y_pct")),
    }
    # 20 欄漂移對帳表：欄名清單在 prior_dd.drift_watch，前份值散在 prior_meta／prior_dd。
    # 判斷者看不到 evidence 原文（v20 拿掉），沒有這張表就無法逐欄歸因（TXN 2026-09-16 首跑 14 欄未歸因）。
    dw = prior_dd.get("drift_watch")
    if isinstance(dw, list) and dw:
        summary["drift_watch_prior"] = {
            str(k): pick((prior_meta, str(k)), (prior_dd, str(k))) for k in dw
        }
    text = json.dumps(summary, ensure_ascii=False, separators=(",", ":"))
    if len(text.encode("utf-8")) > PRIOR_SUMMARY_MAX_BYTES:
        summary["H"] = _trim_prior_rows(summary.get("H"))
        summary["R"] = _trim_prior_rows(summary.get("R"))
        text = json.dumps(summary, ensure_ascii=False, separators=(",", ":"))
    return text




# ---------------------------------------------------------------------------
# enum 表：從 judgment.schema.json 機械抽出所有 enum 欄（v19_contract ＋ 舊形狀頂層
# 的 archetype／decision_inputs.cycle_*／triggers／catalysts／thesis.R.clock 等，
# validate_judgment 會對投影後的視圖驗這些）。TXN 2026-09-16 首跑：判斷者把
# archetype.primary／confidence／cycle_position／cycle_verdict 寫成自由文字，因為
# v19 速查裡沒列這幾個 enum。此表補上，且永遠跟 schema 同步。
# ---------------------------------------------------------------------------

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "dd_schema" / "judgment.schema.json"
_LEGACY_ENUM_PATHS = ("archetype", "decision_inputs", "triggers", "catalysts", "thesis", "appendix_a")


def _walk_enums(node, path, out):
    if not isinstance(node, dict):
        return
    if "enum" in node and path:
        vals = [v for v in node["enum"] if v is not None]
        if vals:
            out.append((path, vals))
    for k, v in (node.get("properties") or {}).items():
        _walk_enums(v, (path + "." + k) if path else k, out)
    if isinstance(node.get("items"), dict):
        _walk_enums(node["items"], path + "[]", out)
    for alt in (node.get("anyOf") or node.get("oneOf") or []):
        _walk_enums(alt, path, out)


def enum_sheet(schema_path=None) -> str:
    schema = json.loads(Path(schema_path or _SCHEMA_PATH).read_text(encoding="utf-8"))
    rows = []
    _walk_enums(schema.get("v19_contract") or {}, "", rows)
    legacy = []
    for top in _LEGACY_ENUM_PATHS:
        node = (schema.get("properties") or {}).get(top)
        if node is not None:
            _walk_enums(node, top, legacy)
    seen = set(p for p, _ in rows)
    for pth, vals in legacy:
        leaf = pth.split(".")[-1]
        if pth in seen or any(r.endswith("." + leaf) or r == leaf for r in seen):
            continue
        rows.append((pth + "（投影後驗）", vals))
        seen.add(pth)
    lines = ["## ②b enum 表（機械抽自 judgment.schema.json；這些欄只准填表列值，填自由文字＝FAIL）", ""]
    for pth, vals in rows:
        if pth.startswith("meta.contract"):
            continue
        lines.append("- `{0}`：{1}".format(pth, "｜".join(str(v) for v in vals)))
    return "\n".join(lines)


def leak_words_section() -> str:
    """QC-40 機器語言詞表，機械抽自 scripts/dd_sections.py 的 LEAK_PATTERNS（單一權威，不複製）。
    TXN 2026-09-16 第二跑：判斷者在 ruling 寫「估值燈色」被擋。判斷者看得到詞表就能避開。"""
    import dd_sections  # noqa: E402
    pats = [p for p in dd_sections.LEAK_PATTERNS]
    lines = ["## ②c 理由文字禁用詞表（QC-40 機器語言，命中任一＝FAIL；這些是給程式看的代號，不是給讀者的話）", "",
             "以下為 regex 原文，逐條避開（含變體）：", ""]
    lines.append("`" + "`　`".join(pats) + "`")
    lines.append("")
    lines.append("改寫原則：說結論本身，不說「燈號／閘／row／QC／驗算」這類流程代號。例：「估值燈色不變」→「估值結論不變」；「row 8a」→ 直接寫進場條件本身，不用路徑代號。")
    return "\n".join(lines)


def drift_rule_section(prior_summary_text: str) -> str:
    return (
        "## ⑦b 前份漂移歸因（機械閘逐欄對帳）\n\n"
        "上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 "
        "`prior_field` 陣列**合起來涵蓋這 20 個欄名的每一個**（含程式稍後才會算的 asym_ratio／bull_5y_price／"
        "bear_5y_price／p_bull_pct／p_bear_pct／ev5y_pct／irr_base_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 "
        "`方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。"
        "`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、"
        "`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。"
        "\n\n`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。"
        "\n\n**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、"
        "`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，"
        "一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 "
        "`competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 "
        "`fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。"
    )


# ---------------------------------------------------------------------------
# judge
# ---------------------------------------------------------------------------

# `scenario_inputs` 形狀範本：照抄 `scripts/dd_prompts/judge_oneshot_tail.md.tmpl`
# 那段（鍵名與結構一字不改），該檔用 `.format_map` 渲染故字面 `{{`/`}}` 逃脫
# 大括號；本檔用純文字組裝（不經 `.format`），故直接寫單層大括號即可。
_SCENARIO_INPUTS_SHAPE = """{
  "terminal_label": "FY20XXE",
  "start": {"eps": <起點 EPS>, "pe": <起點 P/E＝price÷eps>, "basis": "<起點口徑一句話，TTM 或 FY1 須與終端倍數分母同口徑>"},
  "eps": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "pe": {"bull": <終端倍數>, "base": <倍數>, "bear": <倍數>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "second_stage": {"bull_cagr_pct": <Y6–Y10 EPS CAGR %>, "base_cagr_pct": <%>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>,
  "peer_max_fpe": <同業最高 Fwd P/E，可省略>
}"""


def _judge_tail_section(judgment_path: Path, thinking_note=None) -> str:
    lines = [
        "## 尾段：scenario_inputs 形狀與回覆格式",
        "",
        "`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此"
        "產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：",
        "",
        "```json",
        _SCENARIO_INPUTS_SHAPE,
        "```",
        "",
        "（共識三年 EPS 寫在 `eps_meta`，不要在這裡再寫一份；現價與共識由程式從"
        "事實表帶進 `scenario.json`。）",
        "",
        "`dd_scenario.py` 會擋：`eps` 各路徑長度 ≠ 5、終端 EPS 非 Bear＜Base＜Bull、"
        "Bear 終端 EPS ＞ `consensus.fy2`、三機率加總 ≠ 100、`p.bear` ＜ 20、"
        "`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘："
        "Bull 前兩年 EPS 不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一"
        "情境終點跌幅。機率與路徑是你的判斷，算術（IRR／三分量／AR／10Y）全由腳本"
        "算，不要自己填結果欄。",
        "",
        "**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, "
        "separators=(\",\", \":\"))` 等效格式），陣列外不得有任何文字（不加前言、"
        "不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 "
        "`scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、"
        "`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、"
        "`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。"
        "`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，"
        "由腳本從 scenario 機械算回。",
        "",
        "此回覆內容之後由程式存為 `{0}`（你不用、也不能動筆存檔，只需回覆內容"
        "本身）。".format(judgment_path),
    ]
    if thinking_note:
        lines += ["", thinking_note]
    return "\n".join(lines)


def build_judge(run_dir, *, cards_dir, judgment_path=None, thinking_note=None) -> dict:
    run_dir = Path(run_dir)
    cards_dir = Path(cards_dir)
    evidence_path = run_dir / "evidence.json"
    facts_path = run_dir / "facts.json"
    prior_path = run_dir / "parts" / "prior.json"
    out_judgment_path = Path(judgment_path) if judgment_path else (run_dir / "judgment.json")

    evidence = dd_bundle._load_json(evidence_path)
    ticker, date = evidence.get("ticker"), evidence.get("date")
    archetype_hint = evidence.get("archetype_hint")

    named_parts = [
        ("schema_cheatsheet", dd_bundle._schema_cheatsheet("v19")),
        ("enum_sheet", enum_sheet()),
        ("leak_words", leak_words_section()),
        ("facts", dd_bundle._facts_section(facts_path)),
        ("transcript", dd_bundle._transcript_section(evidence, None)),
        ("judge_card", _card_section("④ 判斷卡（judge_card.md）", cards_dir / "judge_card.md")),
        ("addendum_roic", _card_section(
            "⑤a 常載附卡：§5.R 報酬持續期檢核", cards_dir / "judge_addendum_roic.md")),
        ("addendum_playbook", _card_section(
            "⑤b 常載附卡：情境判斷問題字典", cards_dir / "judge_addendum_playbook.md")),
    ]
    for addendum_path in select_addenda(archetype_hint, cards_dir):
        key = "addendum_" + addendum_path.stem.replace("judge_addendum_", "")
        named_parts.append((key, _card_section(
            "⑥ 條件附卡（archetype_hint={0!r} 命中）：{1}".format(
                archetype_hint, addendum_path.name), addendum_path)))

    prior_json = dd_bundle._load_json(prior_path) if prior_path.exists() else {}
    prior_text = prior_summary(prior_json)
    named_parts.append(("prior_summary",
        "## ⑦ 前份判斷摘要（緊湊 JSON，≤ {0} bytes）\n\n```json\n{1}\n```".format(
            PRIOR_SUMMARY_MAX_BYTES, prior_text)))
    named_parts.append(("drift_rule", drift_rule_section(prior_text)))
    named_parts.append(("tail", _judge_tail_section(out_judgment_path, thinking_note)))

    return _assemble(run_dir, "judge", ticker, date, named_parts)


# ---------------------------------------------------------------------------
# gate
# ---------------------------------------------------------------------------

def _gate_tail_section() -> str:
    return (
        "## 尾段：回覆格式\n\n"
        "只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，"
        "陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：\n\n"
        "```json\n"
        "[{\"item\": \"①\", \"light\": \"🔴|🟡|🟢\", \"judgment_path\": \"$.路徑\", "
        "\"reason\": \"一句話\"}]\n"
        "```"
    )


def build_gate(run_dir, *, cards_dir) -> dict:
    run_dir = Path(run_dir)
    cards_dir = Path(cards_dir)
    evidence_path = run_dir / "evidence.json"
    facts_path = run_dir / "facts.json"
    judgment_path = run_dir / "judgment.json"

    evidence = dd_bundle._load_json(evidence_path)
    ticker, date = evidence.get("ticker"), evidence.get("date")
    raw_judgment = dd_bundle._load_json(judgment_path)
    facts = dd_bundle._load_json(facts_path) if facts_path.exists() else None

    judgment_compact = json.dumps(raw_judgment, ensure_ascii=False, separators=(",", ":"))
    named_parts = [
        ("gate_card", _card_section("① gate_card.md（判斷層閘卡）", cards_dir / "gate_card.md")),
        ("referenced_facts", dd_bundle._gate_referenced_facts_section(raw_judgment, facts)),
        ("scenario_meta", dd_bundle._gate_scenario_meta_section(judgment_path)),
        # 2026-09-16 TXN 首次過閘：閘回報「bundle 沒附軸覆蓋總覽」，覆蓋面掃描 (a) 沒得看；補上舊鏈同一段（機械）。
        ("coverage_summary", dd_bundle._gate_coverage_summary(evidence.get("coverage") or {})),
        ("prior_summary", "## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）\n\n```json\n"
            + prior_summary(dd_bundle._load_json(run_dir / "parts" / "prior.json")
                            if (run_dir / "parts" / "prior.json").exists() else {}) + "\n```"),
        ("judgment_full", "## judgment.json 全文（被審對象，緊湊格式）\n\n"
            + dd_bundle._JSON_NOTE + "\n\n```json\n" + judgment_compact + "\n```"),
        ("tail", _gate_tail_section()),
    ]
    return _assemble(run_dir, "gate", ticker, date, named_parts)


# ---------------------------------------------------------------------------
# prose
# ---------------------------------------------------------------------------

_PROSE_SIDS_A = "s1、s2、s3、s4、s5、s6、s7"
_PROSE_SIDS_B = "s8、s9、s10、s11、s12、decision（s85 若觸發併入）"


def _prose_write_instruction(part, prose_a_path, prose_b_path):
    common = ("每段前面獨立一行標記 `<!-- SID:sX -->`（`decision` 段寫 `<!-- SID:decision -->`），緊接該段完整外層元素，"
              "格式與每段固定三塊（`<h2>`／`<p class=\"lead\">`／`<ul class=\"pts\">`）見散文卡 §6。表格注入標記依散文卡 §3 放在對應位置。\n\n"
              "動筆前只列大綱（每章一句主張＋要用的白名單數字），列完就寫，不在腦中預演全文；每章寫完不回頭改。"
              "寫壞即交卷不補——這一輪沒有機械閘回饋、沒有第二次機會。")
    if part == "A":
        return ("## 寫（只有 Write 工具，最多 4 輪）\n\n本通只負責**前半**：輸出一個檔 `{0}`，依序含 {1} 七段。後半由另一通同時在寫，你不要碰。\n\n"
                "**s3 到 s7 是整份報告的重心**（商業本質五章）：每章 4–6 條，每條 120–200 字，把 judgment 投影視圖裡對應問題的 reasoning、數字、反方依據全部鋪開，"
                "不要一句話帶過；s5 至少 3,000 bytes、s3／s4／s6 至少 1,500 bytes，低於直接 FAIL。\n\n"
                .format(prose_a_path, _PROSE_SIDS_A) + common)
    if part == "B":
        return ("## 寫（只有 Write 工具，最多 4 輪）\n\n本通只負責**後半**：輸出一個檔 `{0}`，依序含 {1}。前半（s1–s7）由另一通同時在寫，你不要碰；"
                "s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。\n\n"
                "每章 3–6 條，每條 100–200 字；s10（估值與三種未來）與 s12（最可能怎麼賠）至少 1,500 bytes，把情境輸入、終端倍數、反證三視角的裁定鋪開。\n\n"
                .format(prose_b_path, _PROSE_SIDS_B) + common)
    return ("## 寫（只有 Write 工具，最多 6 輪）\n\n輸出兩個檔：\n\n1. `{0}`：依序含 {1} 七段。\n2. `{2}`：依序含 {3}。\n\n"
            .format(prose_a_path, _PROSE_SIDS_A, prose_b_path, _PROSE_SIDS_B) + common)


def build_prose(run_dir, *, cards_dir, part=None) -> dict:
    run_dir = Path(run_dir)
    cards_dir = Path(cards_dir)
    judgment_path = run_dir / "judgment.json"
    evidence_path = run_dir / "evidence.json"
    tables_dir = run_dir / "tables"
    prose_dir = run_dir / "prose"

    judgment = dd_bundle._load_json(judgment_path)
    evidence = dd_bundle._load_json(evidence_path) if evidence_path.exists() else None
    meta = judgment.get("meta") or {}
    ticker, date = meta.get("ticker"), meta.get("date")

    view = dd_project.view_for(judgment, judgment_path)
    view_compact = json.dumps(view, ensure_ascii=False, separators=(",", ":"))

    named_parts = [
        ("task_header", dd_bundle._prose_task_header(judgment, evidence)),
        ("table_listing", dd_bundle._table_listing_section(tables_dir)),
        ("budget", dd_bundle._prose_budget_section(judgment_path, tables_dir)),
        ("numbers_whitelist", dd_bundle._numbers_whitelist_section(judgment)),
        ("mechanical_sids", dd_bundle._mechanical_sids_section(prose_dir)),
        ("prose_card", _card_section("prose_card.md（散文卡）", cards_dir / "prose_card.md")),
        ("leak_words", leak_words_section()),
        ("judgment_view", "## judgment 投影視圖（dd_project.view_for，緊湊 JSON）\n\n"
            + dd_bundle._JSON_NOTE + "\n\n```json\n" + view_compact + "\n```"),
    ]

    prose_a_path = run_dir / "prose_A.html"
    prose_b_path = run_dir / "prose_B.html"
    header_mapping = {
        "ticker": ticker or "", "date": date or "",
        "prose_a_path": str(prose_a_path), "prose_b_path": str(prose_b_path),
        "write_instruction": _prose_write_instruction(part, prose_a_path, prose_b_path),
    }
    name = "prose" if part is None else "prose_{0}".format(part)
    return _assemble(run_dir, name, ticker, date, named_parts, header_mapping=header_mapping, template="prose")


# ---------------------------------------------------------------------------
# 共用組裝：寫 bundle、接任務頭寫 prompt、算各段 bytes
# ---------------------------------------------------------------------------

def _assemble(run_dir: Path, name: str, ticker, date, named_parts, header_mapping=None, template=None) -> dict:
    bundle_parts = [text for _, text in named_parts]
    bundle_path = run_dir / "bundles" / "{0}.md".format(name)
    dd_bundle._write_bundle(bundle_parts, bundle_path)
    bundle_text = bundle_path.read_text(encoding="utf-8")

    mapping = {"ticker": ticker or "", "date": date or ""}
    if header_mapping:
        mapping.update(header_mapping)
    header_text = _render_template(PROMPTS_DIR / "{0}.md.tmpl".format(template or name), mapping)

    prompt_text = header_text + BUNDLE_SEPARATOR + bundle_text
    prompt_path = run_dir / "prompts" / "{0}.md".format(name)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt_text, encoding="utf-8")

    section_bytes = {key: len(text.encode("utf-8")) for key, text in named_parts}
    section_bytes["header"] = len(header_text.encode("utf-8"))
    section_bytes["bundle_total"] = len(bundle_text.encode("utf-8"))
    section_bytes["prompt_total"] = len(prompt_text.encode("utf-8"))

    return {"prompt_path": prompt_path, "bundle_path": bundle_path, "bytes": section_bytes}
