#!/usr/bin/env python3
"""dd_bundle.py — WP2 判斷層 prompt bundle 組裝器（2026-09-05）。

依母稿 §3.3 順序，把 Stage 0 evidence 包＋逐字稿＋digest＋規則檔組成單一
Markdown，供判斷 agent（judge）或判斷層 critic（gate）一次讀取（無頭執行
時取代人工手貼）。

`judge` 段落順序：①任務頭 → ②schema 速查（機械生成自
judgment.schema.json）→ ③evidence 緊湊版 → ④最新一季逐字稿全文 →
⑤digest → ⑥`references/v16/judgment-rules.md` 全文 → ⑦archetype 條件載入
reference（依 judgment-rules §1 表）。`--contract v19`（預設）改成 ①任務頭 →
②v19 schema 速查 → ③`facts.json` 引用索引 → ③c 原始證據全文 → ③b 前三季摘要壓縮全表 →
④最新一季逐字稿全文 → ⑥規則檔 v19 產物 → ⑦archetype 條件載入。

`gate` 段落順序：①任務頭 → ②`gate_view`（機械抽出，見下）→ judgment.json
全文 → `gate_contract.md` 全文。2026-09-10（WP-A）：閘不再附 evidence／digest
全文與 v15 `references/critic-gates.md`（後者要求讀 HTML／WebSearch 10-14
輪／另一套輸出格式，與 v17 閘「禁搜尋、只審 judgment」互相矛盾，見
`scripts/dd_prompts/gate_contract.md` 開頭對照表）。`gate_view` 改機械抽出
①全部負向 finding、②judgment 有引用／affects 命中但未列
`evidence_dismissed` 的 finding、③coverage 逐軸 status/計數表、④numbers
最新 KPI／估值現值／segments 名單（非整包 numbers）、⑤`scenario_meta.json`
sidecar、⑥`prior_dd`（含 drift_watch，原樣）、⑦digest 的 risk 子集＋全部
qa_flags（digest.json 無 direction 欄位，topic="risk" 是既有分類裡最接近
的替代，理由見 `gate_contract.md`）。2026-09-06 舊註記：閘不再重帶逐字稿
全文；逐字證據已在 evidence／digest，避免跨模型冷讀重付整份逐字稿上下文。

用法：
  python3 scripts/dd_bundle.py judge --run-dir DIR [--out DIR/bundles/judge.md]
  python3 scripts/dd_bundle.py judge --evidence FILE [--digest FILE]
      [--transcript FILE] [--judgment-rules FILE] --out FILE
  python3 scripts/dd_bundle.py gate --run-dir DIR [--out DIR/bundles/gate.md]
  python3 scripts/dd_bundle.py gate --evidence FILE --judgment FILE
      [--digest FILE] [--transcript FILE] [--gate-contract FILE] --out FILE

印 bundle 位元組數與 chars/3 估 token。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_delta  # noqa: E402 — _sibling_scenario_meta（scenario_meta sidecar 尋檔規則），單一權威不複製
import dd_project  # noqa: E402 — v19 判斷檔 → 舊形狀視圖（WP-H1）；舊形狀是 identity
import dd_rules  # noqa: E402 — 規則單一來源與 v19 產物版本戳（WP-H2-3）
import dd_sections  # noqa: E402 — LEAK_PATTERNS（QC-40 詞表），單一權威不複製
import qc  # noqa: E402 — CJK_PUNCT_RE（半形標點規則），單一權威不複製
import validate_judgment  # noqa: E402 — ROIC_CHECKPOINT_NAMES（WP-H2-5），單一權威不複製
import validate_prose  # noqa: E402  （2026-09-06 WP4b：dump_number_whitelist 單一權威不複製）

SCHEMA_PATH = ROOT / "scripts" / "dd_schema" / "judgment.schema.json"
SKILL_REFS_DIR = ROOT / ".claude" / "skills" / "stock-analyst" / "references"
JUDGMENT_RULES_PATH = SKILL_REFS_DIR / "v16" / "judgment-rules.md"
# 2026-09-11 WP-H2-1：v19 判斷包的規則精簡版（只留五出手點判準與反證處置）。
# 完整規則檔留給 v18 路徑與人工查閱，不動——見該檔開頭的分工說明。
JUDGMENT_RULES_V19_PATH = SKILL_REFS_DIR / "v16" / "judgment-rules-v19.md"
PROMPTS_DIR = ROOT / "scripts" / "dd_prompts"
GATE_CONTRACT_PATH = PROMPTS_DIR / "gate_contract.md"  # 2026-09-10 WP-A：取代 critic-gates.md（v15 協議，與 v17 閘矛盾）
RENDER_RULES_PATH = SKILL_REFS_DIR / "v16" / "render-rules.md"  # 2026-09-06 WP4b（散文 agent 唯一讀本）

# archetype → 條件載入 reference（judgment-rules.md §1 表；ALWAYS_REFS 為該表
# 「任一(寫§5.R前)／任一(Part II前)／填appendix_a四欄前」三列，與 archetype 無關）
ARCHETYPE_REFS = {
    "循環/商品": ["cyclical-lens.md"],
    "EMS/ODM": ["cyclical-lens.md"],
    "金融": ["archetype-gatesets.md"],
    "未獲利高成長": ["archetype-gatesets.md"],
    "轉機/特殊情境": ["archetype-gatesets.md"],
    "受監管公用/穩定內需": ["archetype-gatesets.md"],
}
ALWAYS_REFS = ["roic-durability.md", "judgment-playbook.md", "timing-appendix.md"]


def _load_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _task_header(ticker, date, mode: str) -> str:
    role = "判斷（judge）" if mode == "judge" else "判斷層 critic（gate）"
    goal = (
        "輸出 `judgment.json`（形狀見下方 schema 速查），不得臆測未在證據包內出現的數字或事件；"
        "負向 finding 未處置一律列 `evidence_refs` 或 `evidence_dismissed[]`（見 schema 速查 evidence_refs 用法）。"
        if mode == "judge" else
        "輸出 critic gate 判定（PASS／PASS-with-fixes／FAIL）與逐條 finding，依本訊息內建的 ①–⑧ checklist（見下）逐項作答，"
        "checklist 條文權威與欄位對照表見 `gate_contract.md`。"
    )
    return (
        f"## ① 任務頭\n\n"
        f"標的：{ticker}　日期：{date}　角色：stock-analyst v16.2 三步制的{role} agent。\n\n"
        f"{goal}"
    )


def _task_header_v19(ticker, date) -> str:
    """v19 判斷 agent 的任務頭（WP-H2-1，2026-09-11）。

    v19 只在**五個關鍵點**要判斷，其餘由程式投影與算術產生——任務頭先把這五點
    講死，避免判斷 agent 沿用 v18 習慣去填已經不歸它的欄。"""
    return (
        "## ① 任務頭\n\n"
        f"標的：{ticker}　日期：{date}　角色：stock-analyst **v19 判斷 agent**。\n\n"
        "你只在五個地方出手，一回合交卷：\n\n"
        "1. **論點與唯一致命數字**（`thesis`／`answers.q1_business`）\n"
        "2. **護城河方向與再投資報酬**（`answers.q2_moat`／`answers.q3_growth`）\n"
        "3. **情境樹假設**（`scenario_inputs`：三支 EPS 路徑、終端倍數、機率、Max DD 範圍與依據）\n"
        "4. **反證裁定**（`counter_evidence`：三視角反證、矛盾裁定、觸發器與行動條件）\n"
        "5. **決策輸入**（`decision_inputs` 九欄＋`appendix_a` 七欄＋`eps_meta`）\n\n"
        "其餘欄位（評分、燈號、白話段、reasoning 摘要、`scenario.json`、`decision_out` 矩陣欄、"
        "同業對照表的數字）**由程式從你寫的這幾塊投影出來**——你不要填，填了機械閘會擋。"
        "事實表是引用索引，不是唯一數字來源。已有事實用 `fact_refs` 引 id；漏收的資料可直接引用本包原始證據，寫明欄位路徑、來源與期間，不得捏造 fact id。不得從記憶補數字。"
    )


# 2026-09-06：schema 速查瘦身用型別簡寫表（語意不變，只縮寫 type 字面值）。
_TYPE_ABBR = {
    "string": "str", "object": "obj", "array": "arr",
    "integer": "int", "number": "num", "boolean": "bool", "null": "null",
}


def _schema_cheatsheet(contract: str = "v18") -> str:
    """機械生成 schema 速查。

    2026-09-11（WP-H2-1）：`contract="v19"` 時改走 schema 的 `v19_contract`
    區塊——H1 的已知缺口是速查仍印舊形狀，判斷 agent 因此會照舊形狀寫。

    2026-09-06：改成縮排巢狀格式（不重複完整路徑，只在陣列/物件邊界縮排一格），
    type/enum/pattern/maxLength/minItems 壓成一行緊湊記法；required 標記從
    「（必填）」全字改成行首 `*`。語意（哪些欄位/型別/enum/pattern/必填與否）
    一個不少，只是省掉逐行重複的路徑前綴與中文標籤字。
    """
    schema = _load_json(SCHEMA_PATH)
    if contract == "v19":
        schema = schema.get("v19_contract") or {}
        lines = ["## ② Schema 速查（judge-owned 形狀；機械生成自 judgment.schema.json "
                 "的 v19_contract 區塊）", ""]
    else:
        lines = ["## ② Schema 速查（機械生成自 judgment.schema.json，緊湊版）", ""]
    lines.append(
        "格式：縮排＝巢狀層級（不重複完整路徑）；行首 `*`＝必填；"
        "型別簡寫 str/obj/arr/int/num/bool，`a|b`＝可為多型別（含 null）；"
        "`enum[...]`＝允許值；`pat=`＝正則；`≤N`＝maxLength；`≥N`＝minItems；"
        "陣列欄位以 `key[]` 表示，其元素（items）型別接在同一行，物件元素的欄位在下一層縮排列出。"
    )
    lines.append("")

    def type_str(t) -> str:
        if isinstance(t, list):
            return "|".join(_TYPE_ABBR.get(x, x) for x in t)
        return _TYPE_ABBR.get(t, t)

    def scalar_bits(node: dict) -> list:
        bits = []
        if "type" in node and node["type"] != "object" and node["type"] != "array":
            bits.append(type_str(node["type"]))
        if "enum" in node:
            bits.append("enum[" + ",".join(str(x) for x in node["enum"]) + "]")
        if "pattern" in node:
            bits.append(f"pat={node['pattern']}")
        if "maxLength" in node:
            bits.append(f"≤{node['maxLength']}")
        return bits

    def walk(node, key, required_flag, depth):
        if not isinstance(node, dict):
            return
        indent = "  " * depth
        is_array = node.get("type") == "array"
        items = node.get("items") if is_array else None
        display_key = f"{key}[]" if is_array else key
        marker = "*" if required_flag else ""

        bits = []
        if is_array:
            bits.append("arr")
            if "minItems" in node:
                bits.append(f"≥{node['minItems']}")
            if isinstance(items, dict) and items.get("type") not in (None, "object"):
                bits.extend(scalar_bits(items))
        else:
            bits.extend(scalar_bits(node))
        suffix = f": {' '.join(bits)}" if bits else ""
        lines.append(f"{indent}{marker}{display_key}{suffix}")

        target = items if is_array and isinstance(items, dict) else node
        props = target.get("properties") if isinstance(target, dict) else None
        if isinstance(props, dict):
            req = set(target.get("required") or [])
            for k, v in props.items():
                walk(v, k, k in req, depth + 1)

    top_props = schema.get("properties") or {}
    top_req = set(schema.get("required") or [])
    for k, v in top_props.items():
        walk(v, k, k in top_req, 0)

    lines.append("")
    if contract == "v19":
        lines.append("### evidence_refs 用法（v19）")
        lines.append(
            "`counter_evidence.contradictions[]`／`counter_evidence.blind_spots[]`／"
            "`counter_evidence.triggers[]`／`answers.q2_moat.verdict_values.moat.threats[]`／"
            "`thesis.R[]` 可各自加選填 `evidence_refs: [string]`，格式 `axis_id#index`"
            "（對應事實表 `findings_digest[]` 的 `id`）。無法對應到既有證據、但仍要捨棄的"
            "負向 finding，記到 `counter_evidence.evidence_dismissed: [{ref, reason}]`"
            "（理由要指得出證據本身的問題，不得寫「影響不大」）。`validate_judgment.py "
            "--evidence`（J1）會檢查每條 `direction==\"-\"` 的 finding 是否被上述任一處"
            "引用，未引用＝FAIL。"
        )
        lines.append("")
        lines.append("### fact_refs 用法（v19）")
        lines.append(
            "`answers.qX.fact_refs[]` 只准填事實表裡真的存在的 `f_*` id（引不到＝FAIL）。"
            "索引漏收時可引用本包原始證據，寫明欄位路徑、來源與期間；"
            "不要捏造 fact id，也不要從記憶補數字。"
        )
        lines.append("")
        lines.append("### 不要填的欄（填了即 FAIL）")
        lines.append(
            "`decision_inputs` 的 " + "、".join(f"`{k}`" for k in dd_project.PROJECTED_DECISION_INPUT_KEYS)
            + " 一律留 `null` 或整個不寫——由程式從六問答案與事實表投影。"
            "同理不要寫 `moat.spread_table`／`moat.competitors`（同業數字在事實表的 "
            "`peer_comparison`，你只寫 `moat.competitor_notes` 每家一句判讀）、"
            "`reasoning`／`plain`／`contradictions` 等舊形狀頂層欄、以及整份 `scenario.json`。"
        )
        lines.append("")
        lines.append("### §5.R 四檢查點形狀（checkpoints[] 未在上方展開，這裡手動點名）")
        lines.append(
            "`answers.q2_moat.verdict_values.moat.roic_durability.checkpoints[]` 四項"
            "（" + "／".join(validate_judgment.ROIC_CHECKPOINT_NAMES) + "）**每項各一筆物件**，"
            "鍵名固定 `item`（四項名稱之一，逐字比對，不得改寫或縮寫）／`level`（🟢🟡🔴）／"
            "`text`（判讀句；查無或不適用改填 `not_applicable_reason`）。四項缺一，或某項 "
            "`text` 與 `not_applicable_reason` 皆空＝FAIL（`validate_judgment.v19_required_items_checks`）。"
        )
        lines.append("")
        lines.append("### kill_metrics[] 形狀（counter_evidence.kill_metrics，未在上方展開，這裡手動點名）")
        lines.append(
            "是**陣列**（`[{...}, {...}]`），不是以索引數字（`\"0\"`／`\"1\"`）當鍵的物件；"
            "每條必填 `metric`／`bear_threshold`／`window`，並附 `source`（資料來源）。"
        )
        lines.append("")
        lines.append("### 機器語言／半形標點洩漏詞表（單一權威：`dd_sections.LEAK_PATTERNS` ＋ `qc.CJK_PUNCT_RE`）")
        lines.append("、".join(f"`{p}`" for p in dd_sections.LEAK_PATTERNS))
        lines.append(f"- CJK 字元後接半形 `,` `.` `:`（正則 `{qc.CJK_PUNCT_RE.pattern}`）——一律應為全形 ，。：")
        return "\n".join(lines)
    lines.append("### evidence_refs 用法（v17 新增）")
    lines.append(
        "`contradictions[]`／`moat.threats[]`／`premortem.blind_spots[]`（物件形態時）／"
        "`triggers[]`／`thesis.R[]` 可各自加選填 `evidence_refs: [string]`，格式 "
        "`axis_id#index`（對應 evidence coverage/events 該軸 findings 陣列 0-based 索引，"
        "或 finding 自身既有的 `id`）。無法對應到既有證據、但仍要捨棄的負向 finding，"
        "記到頂層 `evidence_dismissed: [{ref, reason}]`。`validate_judgment.py --evidence`"
        "（J1）會檢查每條 `direction==\"-\"` 的 finding 是否被上述任一處引用，未引用＝FAIL。"
    )
    lines.append("")
    lines.append("### 機器語言／半形標點洩漏詞表（單一權威：`dd_sections.LEAK_PATTERNS` ＋ `qc.CJK_PUNCT_RE`）")
    lines.append("、".join(f"`{p}`" for p in dd_sections.LEAK_PATTERNS))
    lines.append(f"- CJK 字元後接半形 `,` `.` `:`（正則 `{qc.CJK_PUNCT_RE.pattern}`）——一律應為全形 ，。：")
    return "\n".join(lines)


# 2026-09-06：JSON 區塊一律緊湊（無縮排、無多餘空白，separators 去掉逗號/冒號後的
# 空格）——只省格式性空白，內容（鍵值）一字不減。所有呼叫點跟著改，不再傳 indent。
_JSON_NOTE = "（以下 JSON 為緊湊格式（省空白），內容完整）"


def _json_block(obj) -> str:
    return "```json\n" + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n```"


def _coverage_table(cov: dict) -> str:
    # 2026-09-06：曾試改緊湊 JSON 陣列，量測反而 +2%（欄位分隔比 ` | ` 還肥）且位置
    # 欄位對判斷 agent 可讀性較差，故維持 markdown 表格原樣。
    lines = ["| id | dir | as_of | reuse | claim | source | affects |", "|---|---|---|---|---|---|---|"]
    for axis, v in (cov or {}).items():
        if not isinstance(v, dict):
            continue
        findings = v.get("findings") or []
        if not findings:
            reuse = "{0}（{1}d）".format(v.get("reused_from"), v.get("age_days")) if v.get("reused_from") else ""
            lines.append(f"| {axis} | - | - | {reuse} | (status={v.get('status')}；無 findings) |  |  |")
            continue
        for i, f in enumerate(findings):
            rid = f.get("id") or f"{axis}#{i}"
            claim = (f.get("claim") or "").replace("|", "\\|").replace("\n", " ")
            source = (f.get("source") or "").replace("|", "\\|").replace("\n", " ")
            affects = ",".join(f.get("affects") or [])
            reuse = "{0}（{1}d）".format(f.get("reused_from"), f.get("age_days")) if f.get("reused_from") else ""
            lines.append(f"| {rid} | {f.get('direction', '')} | {f.get('as_of', '')} | {reuse} | {claim} | {source} | {affects} |")
    return "\n".join(lines)


def _evidence_compact(evidence: dict) -> str:
    lines = ["## ③ Evidence 緊湊版", ""]
    lines.append(
        f"ticker={evidence.get('ticker')}　date={evidence.get('date')}　"
        f"archetype_hint={evidence.get('archetype_hint')}　"
        f"earnings_recency={evidence.get('earnings_recency')}"
    )
    lines.append("")
    lines.append("### numbers（原樣 JSON）")
    lines.append(_JSON_NOTE)
    lines.append(_json_block(evidence.get("numbers") or {}))
    lines.append("")
    lines.append("### coverage（逐軸表格）")
    lines.append(_coverage_table(evidence.get("coverage") or {}))
    lines.append("")
    for key, label in (("events", "events"), ("prior_dd", "prior_dd"),
                        ("ledger", "ledger"), ("canonical_id", "canonical_id")):
        lines.append(f"### {label}（原樣）")
        lines.append(_JSON_NOTE)
        lines.append(_json_block(evidence.get(key) or {}))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _find_transcript_path(ticker: str, filename: str):
    """2026-09-10：`recent_four_quarters[]` 由 Stage 0 寫入時已是完整路徑
    （koyfin.md.tmpl 規格），先直接用；只有純檔名才回退到 Google Drive glob。
    之前一律把完整路徑再接到 glob 樣板後面，14 份判斷包全部「找不到逐字稿」。"""
    if not filename:
        return None
    direct = Path(filename)
    if direct.is_absolute() and direct.exists():
        return direct
    if not ticker:
        return None
    home = Path.home()
    pattern = f"Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/{ticker}/{direct.name}"
    matches = list(home.glob(pattern))
    return matches[0] if matches else None



def _source_evidence_section(evidence: dict) -> str:
    """2026-09-11：原始證據完整保留，取消事實表漏抽就看不到資料的單一路徑。"""
    return "## ③c 原始證據（evidence.json 全文；事實表未收錄時可直接引用）\n\n" + _json_block(evidence)


def _transcript_section(evidence: dict, explicit_path) -> str:
    lines = ["## ④ 最新一季逐字稿全文", ""]
    if explicit_path:
        p = Path(explicit_path)
        if p.exists():
            lines.append(f"（來源：{p}）\n")
            lines.append(p.read_text(encoding="utf-8", errors="replace"))
            return "\n".join(lines)
        lines.append(f"[找不到逐字稿：--transcript 指定的 {p} 不存在]")
        return "\n".join(lines)

    ticker = evidence.get("ticker")
    rec = ((evidence.get("transcripts") or {}).get("selected") or {}).get("recent_four_quarters") or []
    if not rec:
        lines.append("[找不到逐字稿：evidence.transcripts.selected.recent_four_quarters 為空或缺席]")
        return "\n".join(lines)
    # 2026-09-10：清單依日期由舊到新（koyfin.md.tmpl），最新一季是最後一篇；
    # Stage 0 的 digest 也是拿 recent4[:-1] 給摘要、留最後一篇給判斷 agent。
    # 之前取 [0] 拿到的是最舊那季，且與 digest 重疊。
    filename = rec[-1]
    found = _find_transcript_path(ticker, filename)
    if found:
        lines.append(f"（來源：{found}）\n")
        lines.append(found.read_text(encoding="utf-8", errors="replace"))
    else:
        lines.append(
            f"[找不到逐字稿：{filename}（已試 "
            f"~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/{ticker}/）]"
        )
    return "\n".join(lines)


def _digest_section(digest_path) -> str:
    """2026-09-06：digest.json 落地檔是 pretty-print（indent=2），改讀入後轉緊湊
    JSON 再嵌入 bundle（省縮排空白，鍵值內容不變）；若不是合法 JSON（理論上不會，
    保留防呆）就原樣塞入，不因壓縮功能而讓 bundle 開天窗。"""
    lines = ["## ⑤ Digest", ""]
    if not digest_path or not Path(digest_path).exists():
        lines.append(f"[找不到 digest：{digest_path}]")
        return "\n".join(lines)
    raw = Path(digest_path).read_text(encoding="utf-8")
    try:
        obj = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        lines.append("```json")
        lines.append(raw)
        lines.append("```")
        return "\n".join(lines)
    lines.append(_JSON_NOTE)
    lines.append(_json_block(obj))
    return "\n".join(lines)


def _facts_section(facts_path) -> str:
    """2026-09-11：事實表保留為整理與引用索引，原始證據另附全文。"""
    lines = ["## ③ facts.json 事實表全文（引用索引；含 findings_digest 與同業對照）", ""]
    p = Path(facts_path) if facts_path else None
    if not p or not p.exists():
        lines.append(f"[找不到事實表：{facts_path}]——請先補回引用索引，不得捏造 fact id。")
        return "\n".join(lines)
    raw = p.read_text(encoding="utf-8")
    try:
        obj = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        lines.append("```json")
        lines.append(raw)
        lines.append("```")
        return "\n".join(lines)
    lines.append(_JSON_NOTE)
    lines.append(_json_block(obj))
    return "\n".join(lines)


def _digest_lines_section(digest_path) -> str:
    """v19 判斷 bundle 的 ③b 段：前三季（與其餘非最新一季）逐字稿摘要的**壓縮全表**。

    WP-H2-3（2026-09-11，Codex 裁定 1）：H2-1 原本把 digest 整份拿掉，只留事實表
    ——實測顯示「只出現在摘要裡的反證」不會被機械初稿抬進 facts，而事實檢查對這
    種漏失是 0 FAIL、0 WARN（檢查不到的東西不會響）。在有「逐項來源覆蓋檢查」之
    前，判斷層必須看得到摘要的**全部** items 與 qa_flags；省的是排版不是內容——
    每條壓成一行「引用編號｜季別｜topic｜claim｜方向｜來源檔」，quote／speaker
    等逐字定位欄仍不帶（要逐字原文時回事實表或原始逐字稿查）。

    `引用編號`（WP-H2-4，2026-09-11，Codex 複審缺口 3）：digest item 目前沒有
    `id` 欄，schema 不強制——item 自帶 `id` 就沿用，否則以「檔案代號#序號」現算
    （序號＝該檔案內第幾條，1 起算），讓判斷層能點名「哪一條」而不是只講得出
    「哪一季」。檔案代號＝段首的 `source_files` 對照表（F1／F2…），**不是每條都
    重印一次完整檔名**——88 條 items 逐條複製一次完整逐字稿路徑會讓這段本身胖
    過 v18 省下的量，違背 WP-H2-3 把 v19 包壓瘦的整條設計初衷；對照表只印一次，
    每條的來源定位透過代號回查即可。

    `方向` 欄：`digest.json` 的 item 沒有 direction 欄位（摘要 agent 被明令禁裁
    方向，見 `dd_prompts/digest.md.tmpl` 規則 6）。這裡**不臆造方向**——item 自
    帶 `direction` 就照抄，否則以 `topic == "risk"` 當唯一機械代理標「風險」，其
    餘標「未標」，並在段首把這件事講明白，免得判斷層把「未標」讀成「中性」。"""
    lines = ["## ③b 前三季逐字稿摘要（壓縮全表：全部 items 與 qa_flags，不按方向裁）", ""]
    p = Path(digest_path) if digest_path else None
    if not p or not p.exists():
        lines.append(f"[找不到摘要：{digest_path}]——若這檔本來就只有一季逐字稿，忽略本段；"
                     "否則回報 orchestrator，不要當作「沒有反證」。")
        return "\n".join(lines)
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        lines.append(f"[摘要不是合法 JSON：{digest_path}]——回報 orchestrator。")
        return "\n".join(lines)

    items = [i for i in (obj.get("items") or []) if isinstance(i, dict)]
    flags = [f for f in (obj.get("qa_flags") or []) if isinstance(f, dict)]
    lines.append(
        "摘要 agent 被禁止裁方向，所以「方向」欄只有兩種來源：item 自帶 `direction`，"
        "或以 `topic == \"risk\"` 為機械代理。**「未標」不等於中性**——這些條目要不要"
        "當反證由你判斷。逐字原文與出處在事實表與證據包，需要時引該 finding 的 id。"
    )
    lines.append("")
    # 2026-09-11（WP-H2-4，Codex 複審缺口 3）：檔案代號對照表只印一次，每條 item
    # 用代號＋序號當穩定引用編號＋來源定位——不逐條重印完整逐字稿路徑（見上方
    # docstring 的篇幅理由）。
    source_files = [str(f) for f in (obj.get("source_files") or []) if f]
    file_code = {}
    if source_files:
        lines.append("檔案代號（下方引用編號 F#｜序號 用；序號＝該檔第幾條 item，1 起算）：")
        for i, f in enumerate(source_files, 1):
            code = "F{0}".format(i)
            file_code[f] = code
            lines.append("- {0} = {1}".format(code, Path(f).name))
        lines.append("")
    lines.append("### items（{0} 條）".format(len(items)))
    if not items:
        lines.append("（無）")
    per_code_seq = {}
    for it in items:
        topic = str(it.get("topic") or "—")
        direction = it.get("direction")
        if direction is None:
            direction = "風險" if topic == "risk" else "未標"
        raw_file = it.get("file")
        code = file_code.get(raw_file) if raw_file else None
        if code is None:
            # item.file 不在 source_files 裡（不該發生，但不臆造——保底用檔名本身）。
            code = _one_line(Path(str(raw_file)).name) if raw_file else "—"
        per_code_seq[code] = per_code_seq.get(code, 0) + 1
        # 穩定引用編號：item 自帶 id 就用；否則現算「檔案代號#序號」（見上方 docstring）。
        cite_id = it.get("id") or "{0}#{1}".format(code, per_code_seq[code])
        lines.append("- `{0}`｜{1}｜{2}｜{3}｜{4}".format(
            cite_id, it.get("date") or "期間未標", topic,
            _one_line(it.get("claim")), direction))
    lines.append("")
    lines.append("### qa_flags（{0} 條：管理層迴避／改口／保留）".format(len(flags)))
    if not flags:
        lines.append("（無）")
    for fl in flags:
        lines.append("- {0}｜回應型態：{1}".format(
            _one_line(fl.get("question")), _one_line(fl.get("response_pattern"))))
    return "\n".join(lines)


def _one_line(text) -> str:
    """壓成一行：換行轉空白、連續空白收斂。內容一字不刪（壓的是排版不是資訊）。"""
    if text is None:
        return "—"
    return re.sub(r"\s+", " ", str(text)).strip() or "—"


def _judgment_rules_section(path, contract: str = "v18") -> str:
    """⑥ 段規則檔全文。

    WP-H2-3（2026-09-11，Codex 裁定 2）：規則的唯一人工維護來源是
    `judgment-rules.md`，`judgment-rules-v19.md` 降為 `dd_rules.py build-v19`
    的產物。v18 路徑改**經 `dd_rules.render("v18")` 產視圖**，好處是來源檔裡的
    `<!-- only:v19 -->` 段與標記行不會漏進 v18 的包（內容一字不改，只是把不屬
    於這一版的段落拿掉）。指定 `--judgment-rules` 時照原樣讀那份檔，不做視圖轉
    換——那是給「指到另一份合規文件」用的逃生口。"""
    lines = ["## ⑥ judgment-rules.md 全文", ""]
    p = Path(path)
    if not p.exists():
        lines.append(f"[找不到 {p}]")
        return "\n".join(lines)
    if contract == "v18" and p == JUDGMENT_RULES_PATH:
        lines.append(dd_rules.render("v18", source_path=p))
    else:
        rules = p.read_text(encoding="utf-8")
        if contract == "v19":
            # 2026-09-11：依持有人簡化指示，組包時撤掉舊的事實表獨占條款；技能檔不改。
            rules = "\n".join(line for line in rules.split("\n")
                              if not line.startswith("> **事實一律引 id**："))
            rules = rules.replace("①承重數字一律引事實表的", "①事實表已有的承重數字引其")
            rules = rules.replace("②事實表沒有的數字就是沒有——標「事實表未涵蓋」",
                                  "②事實表漏收時引用本包原始證據的路徑、來源與期間；原始證據也缺才標「資料缺口」")
            rules = rules.replace("前份DD只透過事實表與`findings_digest`帶進來",
                                  "前份DD透過本包原始證據的`prior_dd`帶進來")
        lines.append(rules)
    return "\n".join(lines)


def _archetype_refs_section(evidence: dict) -> str:
    lines = ["## ⑦ archetype 條件載入 reference（依 judgment-rules.md §1 表）", ""]
    archetype = (evidence or {}).get("archetype_hint")
    refs = list(ALWAYS_REFS) + ARCHETYPE_REFS.get(archetype, [])
    lines.append(f"archetype_hint={archetype!r} → 載入：{refs}")
    lines.append("")
    for name in refs:
        p = SKILL_REFS_DIR / name
        lines.append(f"### {name}")
        if p.exists():
            lines.append(p.read_text(encoding="utf-8"))
        else:
            lines.append(f"[找不到 {p}]")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# v17 WP-A（2026-09-10）：gate_view —— 閘不再吃 evidence／digest 全文，改機械
# 抽出「checklist 真正會用到」的子集。設計依據：gate.md.tmpl ①–⑧ 逐條複核
# 清單只問「證據包已有而判斷未接的東西」與「覆蓋面／新鮮度／情境樹對帳」，
# 不需要通篇 claim／source 原文或整包 numbers——機械抽出把 151–236KB 的閘
# bundle 壓到 checklist 真正查得到的子集，同時保留可稽核性（每列附
# axis/id，閘仍能回指具體欄位）。
# ---------------------------------------------------------------------------

_AFFECTS_PREFIXES = ("decision_inputs", "thesis", "moat_trend")


def _finding_stable_id(axis: str, i: int, f: dict) -> str:
    """與 `_coverage_table` 同一套 fallback：finding 自身無 `id` 時用
    `{axis}#{i}`（實測 14 份既有 evidence.json 每條 finding 皆已帶 `id`，
    這裡只是防呆，不是常態路徑）。"""
    return f.get("id") or f"{axis}#{i}"


def _iter_findings(coverage: dict):
    """逐軸、逐 finding yield `(axis, stable_id, finding_dict)`。"""
    for axis, v in (coverage or {}).items():
        if not isinstance(v, dict):
            continue
        for i, f in enumerate(v.get("findings") or []):
            yield axis, _finding_stable_id(axis, i, f), f


def _dismissed_refs(judgment: dict) -> list:
    return [str(d.get("ref", "")) for d in (judgment.get("evidence_dismissed") or []) if isinstance(d, dict)]


def _is_dismissed(fid: str, dismissed_refs: list) -> bool:
    """`evidence_dismissed[].ref` 是自由文字（如 "gate_audit#6
    decision_inputs.irr_base_pct"），不保證與 finding id 完全相等，故用
    雙向子字串包含判定，不用精確比對。"""
    if not fid:
        return False
    return any(ref and (fid in ref or ref in fid) for ref in dismissed_refs)


def _affects_hits(affects) -> list:
    return [a for a in (affects or []) if isinstance(a, str) and a.startswith(_AFFECTS_PREFIXES)]


def _judgment_reference_blob(judgment: dict) -> str:
    """整份 judgment 序列化後的文字，供「finding id 是否被引用」的子字串
    掃描——涵蓋 `reasoning`、`contradictions[].evidence_refs`、
    `moat.threats[].evidence_refs`、`premortem.blind_spots[].evidence_refs`、
    `triggers[].evidence_refs`、`thesis.R[].evidence_refs` 等所有位置（比逐
    欄位分別掃更穩，schema 新增 evidence_refs 掛點時不必跟著改本函式）。
    排除 `evidence_dismissed` 本身，避免「finding 只出現在自己的 dismiss
    ref 裡」被誤判成「被引用」。"""
    j = dict(judgment)
    j.pop("evidence_dismissed", None)
    return json.dumps(j, ensure_ascii=False)


def _gate_findings_table(evidence: dict, judgment: dict) -> str:
    """checklist ①（負向 finding 是否被判斷接住）＋ ⑤/⑥ 交叉引用的機械
    子集：收 (a) 全部 direction="-" 的 finding；(b) 未列在
    `evidence_dismissed` 且被判斷引用（id 出現在 judgment 文字裡）或
    `affects` 命中 decision_inputs／thesis／moat_trend 的 finding（可能是
    正向）。純正向且未被引用、affects 也不命中的 finding 不上表——那些對
    checklist 無用，硬塞只會佔位。"""
    cov = evidence.get("coverage") or {}
    dismissed_refs = _dismissed_refs(judgment)
    blob = _judgment_reference_blob(judgment)
    dismiss_reason = {
        str(d.get("ref", "")): d.get("reason", "")
        for d in (judgment.get("evidence_dismissed") or []) if isinstance(d, dict)
    }

    rows = []
    for axis, fid, f in _iter_findings(cov):
        direction = f.get("direction", "")
        dismissed = _is_dismissed(fid, dismissed_refs)
        referenced = (not dismissed) and bool(fid) and (fid in blob)
        hits = [] if dismissed else _affects_hits(f.get("affects"))
        if not (direction == "-" or referenced or hits):
            continue
        claim = (f.get("claim") or "").replace("|", "\\|").replace("\n", " ")
        source = (f.get("source") or "").replace("|", "\\|").replace("\n", " ")
        affects = ",".join(f.get("affects") or [])
        if dismissed:
            ref_hit = next((r for r in dismissed_refs if r and (fid in r or r in fid)), "")
            note = (dismiss_reason.get(ref_hit, "") or "").replace("|", "\\|").replace("\n", " ")
            dismissed_col = f"Y：{note}"
        else:
            dismissed_col = "N"
        rows.append(
            f"| {axis} | {fid} | {direction} | {f.get('as_of', '')} | {claim} | {source} | "
            f"{affects} | {'Y' if referenced else 'N'} | {dismissed_col} |"
        )

    header = [
        "| axis | id | dir | as_of | claim | source | affects | 被引用 | evidence_dismissed |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    if not rows:
        return "\n".join(header) + "\n\n（本檔無符合條件的 finding：無負向、無被引用、affects 也未命中）"
    return "\n".join(header + rows)


def _gate_coverage_summary(coverage: dict) -> str:
    """checklist ⑤ 覆蓋面掃描：逐軸 status／findings 數／queries 數；
    status 為 none／not_applicable 的軸額外列出查詢詞原文，供閘判斷
    「queries_run 是否 <2 條或不相關」（其餘軸已 found，計數已足夠）。"""
    lines = ["| axis | status | n_findings | n_queries |", "|---|---|---|---|"]
    detail = []
    for axis, v in (coverage or {}).items():
        if not isinstance(v, dict):
            continue
        status = v.get("status")
        findings = v.get("findings") or []
        queries = v.get("queries_run") or []
        lines.append(f"| {axis} | {status} | {len(findings)} | {len(queries)} |")
        if status in ("none", "not_applicable"):
            reuse = ""
            if v.get("reused_from"):
                reuse = "（沿用 {0}，{1}d）".format(v.get("reused_from"), v.get("age_days"))
            qtext = "；".join(queries) if queries else "（無查詢記錄）"
            detail.append(f"- **{axis}**（{status}）{reuse}：{qtext}")
    out = "\n".join(lines)
    if detail:
        out += "\n\n未涵蓋／不適用軸的查詢詞原文（供判相關性）：\n" + "\n".join(detail)
    return out


_SEGMENT_MEMBER_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*Segment[A-Za-z0-9]*Member")


def _extract_segment_names(edgar_concentrations: dict) -> list:
    """`numbers.edgar_concentrations.excerpt` 是原始 XBRL tag 文字（常
    >1000 字、對閘無實質資訊），只抽其中的 `XxxSegmentMember` 名稱當「segments
    名單」，不帶整段 excerpt。"""
    excerpt = (edgar_concentrations or {}).get("excerpt") or ""
    return sorted(set(_SEGMENT_MEMBER_RE.findall(excerpt)))


def _gate_numbers_summary(evidence: dict) -> str:
    """checklist ⑦ 數字新鮮度：只帶 `numbers.latest_quarter_kpis`（逐項
    metric/value/as_of，checklist ⑦ 逐字點名的欄位）＋ price_at_dd／
    earnings_recency／估值現值（非五年歷史）／segments 名單，不帶整包
    `numbers`（peer_financials／edgar excerpt 原文／momentum 等對 checklist
    無直接用途）。"""
    numbers = evidence.get("numbers") or {}
    out = {
        "price_at_dd": numbers.get("price_at_dd"),
        "price_as_of": numbers.get("price_as_of"),
        "earnings_recency": numbers.get("earnings_recency"),
    }
    trailing = ((numbers.get("valuation_history") or {}).get("trailing")) or {}
    val_current = {}
    for k in ("pe", "ps", "ev_s"):
        node = trailing.get(k) or {}
        if node:
            val_current[k] = {
                "current": node.get("current"),
                "percentile_within_annual_points": node.get("current_percentile_within_annual_points"),
            }
    fwd_points = ((numbers.get("valuation_history") or {}).get("fwd_recent_window") or {}).get("points") or []
    if fwd_points:
        val_current["fwd_pe_latest_snapshot"] = fwd_points[-1]
    out["valuation_current"] = val_current
    if numbers.get("latest_quarter_kpis"):
        out["latest_quarter_kpis"] = numbers.get("latest_quarter_kpis")
    out["segments"] = _extract_segment_names(numbers.get("edgar_concentrations") or {})

    lines = ["numbers 摘要（僅最新 KPI／估值現值／segments 名單，非整包 numbers）", ""]
    lines.append(_JSON_NOTE)
    lines.append(_json_block(out))
    return "\n".join(lines)


def _gate_scenario_meta_section(judgment_path: Path) -> str:
    """checklist ⑥(iii) `decision_inputs.irr_base_pct`／`ev5y_pct` 與
    `scenario_meta` 對帳，需要這份 sidecar 的權威值——找法沿用
    `dd_delta._sibling_scenario_meta`（archive 命名慣例／in-flight run 目錄
    慣例二擇一，見該函式註解），不在本檔重造一套找檔邏輯。"""
    lines = ["scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）", ""]
    p = dd_delta._sibling_scenario_meta(Path(judgment_path))
    if not p:
        lines.append("[找不到 scenario_meta.json sidecar（archive 命名慣例與 in-flight run 目錄慣例皆未命中）]")
        return "\n".join(lines)
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError):
        lines.append(f"[scenario_meta {p} 讀取失敗或非合法 JSON]")
        return "\n".join(lines)
    lines.append(f"（來源：{p}）")
    lines.append(_JSON_NOTE)
    lines.append(_json_block(obj))
    return "\n".join(lines)


def _gate_prior_dd_section(evidence: dict) -> str:
    """checklist ⑧ QC-49 前份漂移歸因：`evidence.prior_dd` 已含
    `drift_watch`／`prior_meta`／`H`／`R`／`triggers` 等，原樣附上（不是
    大檔，且欄位彼此耦合不易再拆）。"""
    lines = ["prior_dd（前份裁決＋drift_watch，原樣；checklist ⑧ 對帳用）", ""]
    lines.append(_JSON_NOTE)
    lines.append(_json_block(evidence.get("prior_dd") or {}))
    return "\n".join(lines)


def _gate_digest_risk_section(digest_path) -> str:
    """digest.json 的 `items[]` 實測（14 份既有 run 全查）沒有 `direction`
    欄位，只有 `topic`（白名單見 validate_digest.py：guidance/margin/
    competition/capital_allocation/product/risk/customer/commitment）——
    `topic=="risk"` 是既有分類裡與「負向」語意最接近的替代，`qa_flags`
    （管理層迴避／未正面回答的問答，本來就是已篩過的可疑清單）全數保留。
    非 risk 的 items（guidance/margin/product 等中性或正向摘要）對閘的
    checklist 無直接用途，不上 bundle。"""
    lines = [
        "digest 風險子集（topic=\"risk\" 的 items ＋ 全部 qa_flags；"
        "digest.json 無 direction 欄位，理由見本函式 docstring／gate_contract.md）",
        "",
    ]
    if not digest_path or not Path(digest_path).exists():
        lines.append(f"[找不到 digest：{digest_path}]")
        return "\n".join(lines)
    raw = Path(digest_path).read_text(encoding="utf-8")
    try:
        obj = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        lines.append("[digest 非合法 JSON，略過風險子集抽取]")
        return "\n".join(lines)
    items = obj.get("items") or []
    risk_items = [it for it in items if it.get("topic") == "risk"]
    view = {"risk_items": risk_items, "qa_flags": obj.get("qa_flags") or []}
    lines.append(_JSON_NOTE)
    lines.append(_json_block(view))
    return "\n".join(lines)


def _iter_facts(facts: dict):
    """逐條走事實表的 facts（六問各一組），回傳 (qkey, fact dict)。"""
    for qkey, q in ((facts or {}).get("questions") or {}).items():
        for f in (q or {}).get("facts") or []:
            if isinstance(f, dict) and f.get("id"):
                yield qkey, f


def _collect_fact_refs(raw_judgment: dict) -> list:
    """判斷檔內所有 `fact_refs`（六問答案、也可能出現在別處）的 id，去重保序。

    走的是**原始 v19 判斷檔**不是投影視圖：`fact_refs` 是 v19 自有欄位，投影
    視圖為了相容舊形狀不保證保留它。"""
    seen, out = set(), []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "fact_refs" and isinstance(v, list):
                    for r in v:
                        r = str(r)
                        if r and r not in seen:
                            seen.add(r)
                            out.append(r)
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(raw_judgment or {})
    return out


def _gate_referenced_facts_section(raw_judgment: dict, facts: dict) -> str:
    """v19 閘的「被引用事實」段（WP-H2-3，Codex 接線缺口 2）。

    H2-1 的閘 bundle 只有 `fact_refs` 的 **id**，沒有值也沒有原文——閘要查
    「這個數字是不是這個意思」時得靠猜，等於沒查。這裡把被引用到的事實逐條
    帶入（id／值＋單位／期間與口徑／來源與原文片段），另附 `findings_digest`
    中**方向為負或來源有衝突**的條目（閘的職責之一就是問「這些負向的東西，
    判斷者處理了沒有」）。

    刻意**不帶整份事實表**：閘要看的是「判斷者引了什麼、漏了什麼負向的」，
    不是把 Stage 0 的收集成果再付一次上下文。"""
    lines = ["## ②b 被引用的事實與負向條目（v19；閘要查數字時不必猜）", ""]
    if not facts:
        lines.append("[本 run 沒有 facts.json——不是 v19 run，或事實表未產出。]")
        return "\n".join(lines)

    index = {f["id"]: (qkey, f) for qkey, f in _iter_facts(facts)}
    refs = _collect_fact_refs(raw_judgment)
    lines.append("### 判斷檔 `fact_refs` 引到的事實（{0} 條）".format(len(refs)))
    if not refs:
        lines.append("（判斷檔沒有任何 `fact_refs`——這本身就是要問的事：承重數字沒有可追溯來源。）")
    for ref in refs:
        hit = index.get(ref)
        if hit is None:
            lines.append("- `{0}`：**事實表查無此 id**（斷鏈——承重數字追不回來源）".format(ref))
            continue
        qkey, f = hit
        src = f.get("source") or {}
        lines.append("- `{0}`（{1}）｜{2}＝{3}{4}｜期間與口徑：{5}／{6}｜kind：{7}".format(
            ref, qkey, _one_line(f.get("label")), _one_line(f.get("value")),
            (" " + str(f.get("unit"))) if f.get("unit") else "",
            _one_line(f.get("period")), _one_line(f.get("basis")), _one_line(f.get("kind"))))
        lines.append("  - 來源：{0}（{1}，as_of {2}）".format(
            _one_line(src.get("citation")), _one_line(src.get("ref")), _one_line(src.get("as_of"))))
        # 2026-09-11（WP-H2-4，Codex 複審缺口 3）：有 quote／locator 就帶——閘要
        # 核對「這個數字是不是這個意思」，光有 citation 名稱查不到原文段落。
        if src.get("locator"):
            lines.append("  - 定位：{0}".format(_one_line(src.get("locator"))))
        if f.get("quote"):
            lines.append("  - 原文：「{0}」".format(_one_line(f.get("quote"))))
        if f.get("note"):
            lines.append("  - 註記：{0}".format(_one_line(f.get("note"))))

    neg = []
    for d in (facts.get("findings_digest") or []):
        if not isinstance(d, dict):
            continue
        direction = str(d.get("direction") or "")
        status = str(d.get("status") or "")
        if direction == "-" or "conflict" in status or "衝突" in status:
            neg.append(d)
    lines.append("")
    lines.append("### findings_digest 中方向為負或來源衝突的條目（{0} 條）".format(len(neg)))
    if not neg:
        lines.append("（無。若判斷檔通篇沒有反證，這件事本身值得問。）")
    for d in neg:
        lines.append("- `{0}`（{1}｜方向 {2}｜狀態 {3}）：{4}".format(
            _one_line(d.get("id")), _one_line(d.get("axis")),
            _one_line(d.get("direction")), _one_line(d.get("status")), _one_line(d.get("claim"))))
        lines.append("  - 來源：{0}（as_of {1}）｜affects：{2}".format(
            _one_line(d.get("source")), _one_line(d.get("as_of")),
            _one_line("、".join(str(a) for a in (d.get("affects") or [])) or "—")))
    gaps = facts.get("gaps") or []
    if gaps:
        lines.append("")
        lines.append("### 事實表自陳的缺口（{0} 條）".format(len(gaps)))
        for g in gaps:
            if isinstance(g, dict):
                lines.append("- {0}：{1}".format(_one_line(g.get("id") or g.get("question")),
                                                 _one_line(g.get("why"))))
            else:
                lines.append("- {0}".format(_one_line(g)))
    return "\n".join(lines)


def _gate_view_section(evidence: dict, judgment: dict, judgment_path: Path, digest_path) -> str:
    lines = [
        "## ② gate_view（機械抽出，非 evidence／digest 全文；抽取規則與 checklist 對照表見 "
        "`scripts/dd_prompts/gate_contract.md`）",
        "",
        "ticker={0}　date={1}　archetype_hint={2}".format(
            evidence.get("ticker"), evidence.get("date"), evidence.get("archetype_hint")),
        "",
        "### (a)+(b) 負向 finding／被引用或 affects 命中且未列 evidence_dismissed 的 finding",
        _gate_findings_table(evidence, judgment),
        "",
        "### (c) coverage 逐軸總覽",
        _gate_coverage_summary(evidence.get("coverage") or {}),
        "",
        "### (d) " + _gate_numbers_summary(evidence),
        "",
        "### (e) " + _gate_scenario_meta_section(judgment_path),
        "",
        "### (f) " + _gate_prior_dd_section(evidence),
        "",
        "### (g) " + _gate_digest_risk_section(digest_path),
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# v17 WP4b（2026-09-06）：散文（prose）bundle —— `ddreport.py prose prepare`
# 呼叫，組 bundles/prose.md 給散文 agent 一次讀取。段落順序見任務指示：
# ①任務頭 → ②render-rules.md 全文 → ③judgment.json 全文（含 reasoning）→
# ④已生成的機械表格清單（含注入標記）→ ⑤各段散文目標 bytes 表
# （dd_prose_budget.py）→ ⑥數字白名單（validate_prose.py --dump-numbers）→
# ⑦C-1 機械段（revlog/s14/appA）清單，散文 agent 不寫這幾段。
# ---------------------------------------------------------------------------

_PROSE_MECHANICAL_SIDS = ("revlog", "s14", "appA")

# 表格檔名 -> (注入段, 標記, 一句說明)，對照 render-rules.md §2 表格注入標記契約。
_PROSE_TABLE_MARKERS = [
    ("e2.html", "s2", "<!-- E2 -->", "§2.B 三假設 H1-H3 表"),
    ("e3.html", "s3", "<!-- E3 -->", "§3.F 逐段 TAM/SAM + 利潤池"),
    ("e5.html", "s5", "<!-- E5 -->", "§5 二維評分 + Moat-to-Numbers"),
    ("e6.html", "s5", "<!-- E6 -->", "§5.F 對手 P&L 對照"),
    ("e7.html", "s5", "<!-- E7 -->", "§5.R 四檢查點"),
    ("e8.html", "s6", "<!-- E8 -->", "§6.I 分部前瞻 build"),
    ("e9.html", "s7", "<!-- E9 -->", "§7.E DuPont + CCC"),
    ("e10.html", "s9", "<!-- E10 -->", "§9.D 資本配置 track"),
    ("e11.html", "s10", "<!-- E11 -->", "情境樹 Bull/Base/Bear 合一表"),
    ("audit.html", "decision", "<!-- AUDIT -->", "決策矩陣稽核表（audit_rows 非空才有）"),
    ("e12.html", "decision", "<!-- E12 -->", "監測與觸發器表"),
    ("appA-table.html", "appA", "<!-- APPA_TABLE -->", "附錄 A 一列式機械評等表"),
]


def _archetype_label(judgment: dict):
    """`archetype` 在 judgment.json 是物件（{primary,secondary,confidence,
    fingerprint}），任務頭只需要 primary 一句話，不塞整包 fingerprint 長文。"""
    arch = judgment.get("archetype")
    if isinstance(arch, dict):
        return arch.get("primary")
    return arch


def _prose_task_header(judgment: dict, evidence: dict | None) -> str:
    meta = judgment.get("meta") or {}
    prior_line = ""
    if evidence:
        prior = evidence.get("prior_dd") or {}
        if prior.get("status") == "ok":
            pm = prior.get("prior_meta") or {}
            prior_line = "　前份裁決：{0}　{1}｜{2}".format(
                pm.get("date"), pm.get("dca_verdict") or pm.get("verdict"), pm.get("dca_role") or "",
            )
    return (
        "## ① 任務頭\n\n"
        "標的：{ticker}　日期：{date}　archetype：{archetype}{prior_line}　"
        "角色：stock-analyst v17 散文（prose）agent。\n\n"
        "判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`"
        "（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），"
        "每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；"
        "`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。"
    ).format(
        ticker=meta.get("ticker"), date=meta.get("date"),
        archetype=_archetype_label(judgment), prior_line=prior_line,
    )


def _table_listing_section(tables_dir: Path) -> str:
    lines = [
        "## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，"
        "不重寫表格內容）",
        "",
    ]
    for fname, sid, marker, desc in _PROSE_TABLE_MARKERS:
        f = tables_dir / fname
        status = "{0}B".format(len(f.read_bytes())) if f.exists() else "未生成"
        lines.append("- `{0}`（{1}）→ `{2}` 段 `{3}`：{4}".format(fname, status, sid, marker, desc))
    return "\n".join(lines)


def _prose_budget_section(judgment_path: Path, tables_dir: Path) -> str:
    lines = ["## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）", ""]
    r = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "dd_prose_budget.py"),
         str(judgment_path), "--tables", str(tables_dir)],
        capture_output=True, text=True,
    )
    lines.append("```")
    lines.append((r.stdout or r.stderr).strip())
    lines.append("```")
    return "\n".join(lines)


def _numbers_whitelist_section(judgment: dict) -> str:
    """2026-09-10（WP-A 任務 2）：只收 judgment 數字，不再併 evidence。

    依據：① prose.md.tmpl 本身明講「**不讀** evidence.json 全文——承重數字
    一律來自 judgment.json（含其 reasoning）」，白名單併入 evidence 數字與
    這條指示矛盾（等於明著告訴 agent 可以抄 evidence 裡判斷沒引用過的數
    字）。② 實際擋盤的機械閘（`ddreport.py::_run_gates` → `validate_prose.py
    PROSE_DIR --judgment ... --evidence ...`）是直接讀 judgment.json／
    evidence.json 兩個檔案重算 ref_numbers，不消費本函式或本 bundle 的輸
    出——拿掉 evidence 不會讓任何原本會過的 prose 變成 FAIL，只是不再主
    動展示 evidence 裡的數字誘使 agent 去抄。③ `gen_dd_tables.py` 的機械表
    格（e2–e12）以 judgment 欄位為主，唯一吃 evidence 的是 revlog（前份
    比對，機械生成、agent 不寫），不影響散文白名單的需求範圍。

    註記（surface conflict，未動）：references/v16/render-rules.md §0.2 一行
    寫「承重數字必須已存在於 judgment.json(或 evidence.json)」，字面上仍
    允許 evidence 來源——與 prose.md.tmpl 的「不讀 evidence」說法不完全一
    致。render-rules.md 不在本次任務可改檔案清單內，這裡選擇對齊
    prose.md.tmpl 較嚴的那條（agent 動筆前只看得到 judgment 數字），機械
    閘本身仍保留 evidence 當寬鬆備援，兩邊互不衝突、只是本函式不再把
    evidence 數字主動攤在 agent 眼前。"""
    numbers = validate_prose.dump_number_whitelist(judgment)
    lines = [
        "## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）",
        "",
        "```",
    ]
    lines.extend(numbers)
    lines.append("```")
    return "\n".join(lines)


def _mechanical_sids_section(prose_dir: Path) -> str:
    present = [sid for sid in _PROSE_MECHANICAL_SIDS if (prose_dir / f"{sid}.html").exists()]
    lines = [
        "## ⑦ C-1 機械段（已由腳本生成，禁止散文 agent 撰寫或覆寫）",
        "",
        "已生成：{0}".format(", ".join(present) if present else "（無，prepare 步驟可能未跑機械段）"),
        "`decision` 段仍由你撰寫，但段落內 `<!-- E12 -->` 標記之後會由系統自動接一句機械說明"
        "（觸發器見上表、重啟條件），你不需要、也不應該自己寫這句話。",
    ]
    return "\n".join(lines)


def cmd_prose(args) -> int:
    if args.run_dir:
        run_dir = Path(args.run_dir)
        judgment_path = Path(args.judgment) if args.judgment else run_dir / "judgment.json"
        evidence_path = Path(args.evidence) if args.evidence else run_dir / "evidence.json"
        tables_dir = Path(args.tables) if args.tables else run_dir / "tables"
        prose_dir = Path(args.prose_dir) if args.prose_dir else run_dir / "prose"
        out_path = Path(args.out) if args.out else run_dir / "bundles" / "prose.md"
    else:
        if not (args.judgment and args.tables and args.prose_dir and args.out):
            print("prose：需要 --run-dir，或至少 --judgment／--tables／--prose-dir／--out", file=sys.stderr)
            return 2
        judgment_path = Path(args.judgment)
        evidence_path = Path(args.evidence) if args.evidence else None
        tables_dir = Path(args.tables)
        prose_dir = Path(args.prose_dir)
        out_path = Path(args.out)

    if not judgment_path.exists():
        print(f"✗ judgment 檔不存在：{judgment_path}", file=sys.stderr)
        return 1
    judgment = _load_json(judgment_path)
    evidence = _load_json(evidence_path) if evidence_path and evidence_path.exists() else None

    judgment_compact = json.dumps(judgment, ensure_ascii=False, separators=(",", ":"))
    render_rules_text = (
        RENDER_RULES_PATH.read_text(encoding="utf-8") if RENDER_RULES_PATH.exists()
        else f"[找不到 {RENDER_RULES_PATH}]"
    )

    parts = [
        _prose_task_header(judgment, evidence),
        "## ② render-rules.md 全文（呈現規則唯一 always-on 檔）\n\n" + render_rules_text,
        "## ③ judgment.json 全文（含 reasoning，緊湊格式）\n\n" + _JSON_NOTE
        + "\n\n```json\n" + judgment_compact + "\n```",
        _table_listing_section(tables_dir),
        _prose_budget_section(judgment_path, tables_dir),
        _numbers_whitelist_section(judgment),
        _mechanical_sids_section(prose_dir),
    ]
    _write_bundle(parts, out_path)
    return 0


def _write_bundle(parts, out_path: Path):
    bundle = "\n\n---\n\n".join(parts) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(bundle, encoding="utf-8")
    n_bytes = len(bundle.encode("utf-8"))
    print(f"bundle 已寫 {out_path}：{n_bytes} bytes（≈{len(bundle) // 3} tokens）")


def cmd_judge(args) -> int:
    if args.run_dir:
        run_dir = Path(args.run_dir)
        evidence_path = run_dir / "evidence.json"
        digest_path = Path(args.digest) if args.digest else run_dir / "digest.json"
        out_path = Path(args.out) if args.out else run_dir / "bundles" / "judge.md"
    else:
        if not (args.evidence and args.out):
            print("judge：需要 --run-dir，或至少 --evidence 與 --out", file=sys.stderr)
            return 2
        evidence_path = Path(args.evidence)
        digest_path = Path(args.digest) if args.digest else None
        out_path = Path(args.out)

    if not evidence_path.exists():
        print(f"✗ evidence 檔不存在：{evidence_path}", file=sys.stderr)
        return 1
    evidence = _load_json(evidence_path)

    # 2026-09-11：保留原始證據，不再以輸入包較小作為完整性的替代驗收。
    if getattr(args, "contract", "v19") == "v19":
        facts_arg = getattr(args, "facts", None)
        facts_path = Path(facts_arg) if facts_arg else (
            (run_dir / "facts.json") if args.run_dir else None)
        rules_path = Path(args.judgment_rules) if args.judgment_rules else JUDGMENT_RULES_V19_PATH
        # WP-H2-3（Codex 裁定 2）：v19 規則檔是產物不是人工檔——組包前先核對它與
        # 來源 `judgment-rules.md` 的版本戳。不一致就**擋下**（不是警告後照跑）：
        # 拿一份過期的規則去判斷，錯在哪不會有人發現。`--judgment-rules` 指到別份
        # 檔時跳過此檢查（逃生口，責任在呼叫端）。
        if not args.judgment_rules:
            ok_rules, msg_rules = dd_rules.check(rules_path)
            if not ok_rules:
                print("✗ " + msg_rules, file=sys.stderr)
                return 1
        parts = [
            _task_header_v19(evidence.get("ticker"), evidence.get("date")),
            _schema_cheatsheet("v19"),
            _facts_section(facts_path),
            _source_evidence_section(evidence),
            _digest_lines_section(digest_path),
            _transcript_section(evidence, args.transcript),
            _judgment_rules_section(rules_path, "v19"),
            _archetype_refs_section(evidence),
        ]
        _write_bundle(parts, out_path)
        return 0

    judgment_rules_path = Path(args.judgment_rules) if args.judgment_rules else JUDGMENT_RULES_PATH

    parts = [
        _task_header(evidence.get("ticker"), evidence.get("date"), "judge"),
        _schema_cheatsheet(),
        _evidence_compact(evidence),
        _transcript_section(evidence, args.transcript),
        _digest_section(digest_path),
        _judgment_rules_section(judgment_rules_path),
        _archetype_refs_section(evidence),
    ]
    _write_bundle(parts, out_path)
    return 0


def cmd_gate(args) -> int:
    if args.run_dir:
        run_dir = Path(args.run_dir)
        evidence_path = run_dir / "evidence.json"
        digest_path = Path(args.digest) if args.digest else run_dir / "digest.json"
        judgment_path = Path(args.judgment) if args.judgment else run_dir / "judgment.json"
        out_path = Path(args.out) if args.out else run_dir / "bundles" / "gate.md"
    else:
        if not (args.evidence and args.judgment and args.out):
            print("gate：需要 --run-dir，或至少 --evidence／--judgment／--out", file=sys.stderr)
            return 2
        evidence_path = Path(args.evidence)
        digest_path = Path(args.digest) if args.digest else None
        judgment_path = Path(args.judgment)
        out_path = Path(args.out)

    if not evidence_path.exists():
        print(f"✗ evidence 檔不存在：{evidence_path}", file=sys.stderr)
        return 1
    evidence = _load_json(evidence_path)
    # 2026-09-06：judgment.json 落地檔是 pretty-print，嵌入 gate bundle 前轉緊湊
    # JSON（省縮排空白）；找不到檔／非合法 JSON 時原樣保留既有錯誤訊息或原始文字。
    # 2026-09-10（WP-A）：同時需要 judgment 的 dict 形態餵 gate_view（找
    # evidence_dismissed／被引用 finding），故此處改保留 parsed dict；找不到
    # 檔或非合法 JSON 時 judgment_obj 退回空 dict（gate_view 的各函式對空
    # dict 皆有防呆，不會炸）。
    # 2026-09-11（WP-H1）：③ 段的 judgment 全文維持**原樣**（被審對象就是判斷者
    # 實際寫的那份，v19 不例外）；gate_view 的機械抽取則讀 dd_project 投影視圖，
    # 才找得到反證、evidence_dismissed 與被引用的 finding。舊形狀兩者同一物件。
    judgment_obj: dict = {}
    judgment_raw_obj: dict = {}
    if judgment_path.exists():
        judgment_raw = judgment_path.read_text(encoding="utf-8")
        try:
            judgment_raw_obj = json.loads(judgment_raw)
            judgment_obj = dd_project.view_for(judgment_raw_obj, judgment_path)
            judgment_text = json.dumps(judgment_raw_obj, ensure_ascii=False, separators=(",", ":"))
            judgment_note = _JSON_NOTE + "\n\n"
        except (json.JSONDecodeError, ValueError):
            judgment_text = judgment_raw
            judgment_note = ""
    else:
        judgment_text = f"[找不到 judgment：{judgment_path}]"
        judgment_note = ""

    # WP-H2-3（Codex 接線缺口 2）：v19 run 的閘要看得到被引用事實的**值與原文**，
    # 不能只有 id。非 v19（舊形狀）不加這一段，閘 bundle 一位元組不變。
    facts_obj = None
    if judgment_raw_obj and dd_project.is_v19(judgment_raw_obj):
        facts_arg = getattr(args, "facts", None)
        facts_file = Path(facts_arg) if facts_arg else (
            (Path(args.run_dir) / "facts.json") if args.run_dir else None)
        if facts_file and facts_file.exists():
            try:
                facts_obj = json.loads(facts_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                facts_obj = None
        if facts_obj is None:
            facts_obj = dd_project.load_facts(judgment_raw_obj, judgment_path)
    gate_contract_path = Path(args.gate_contract) if args.gate_contract else GATE_CONTRACT_PATH
    gate_contract_text = (
        gate_contract_path.read_text(encoding="utf-8") if gate_contract_path.exists()
        else f"[找不到 {gate_contract_path}]"
    )

    # 2026-09-11：v19 審核與判斷讀同份原始證據，取消另一套欄位與方向篩選。
    parts = [_task_header(evidence.get("ticker"), evidence.get("date"), "gate")]
    if dd_project.is_v19(judgment_raw_obj):
        parts += [_source_evidence_section(evidence),
                  _gate_scenario_meta_section(judgment_path),
                  _digest_lines_section(digest_path)]
    else:
        parts.append(_gate_view_section(evidence, judgment_obj, judgment_path, digest_path))
    if facts_obj is not None:
        parts.append(_gate_referenced_facts_section(judgment_raw_obj, facts_obj))
    parts += [
        "## ③ judgment.json 全文（被審對象，原樣保留）\n\n" + judgment_note + "```json\n" + judgment_text + "\n```",
        "## ④ gate_contract.md 全文（v17 checklist 條文權威，取代 v15 references/critic-gates.md）\n\n"
        + gate_contract_text,
    ]
    _write_bundle(parts, out_path)
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_judge = sub.add_parser("judge", help="組判斷 agent 的輸入 bundle")
    p_judge.add_argument("--run-dir", help=".dd_build/runs/{T}_{D}/ 目錄（讀 evidence.json／digest.json，寫 bundles/judge.md）")
    p_judge.add_argument("--evidence", help="evidence.json 路徑（無 --run-dir 時必填）")
    p_judge.add_argument("--digest", help="digest.json 路徑")
    p_judge.add_argument("--transcript", help="逐字稿檔路徑；未給則由 evidence.transcripts 自動找")
    p_judge.add_argument("--judgment-rules",
                         help="規則檔路徑（v19 預設 references/v16/judgment-rules-v19.md；"
                              "--contract v18 預設 references/v16/judgment-rules.md）")
    p_judge.add_argument("--facts", help="facts.json 路徑（v19 專用；預設 run_dir/facts.json）")
    p_judge.add_argument("--contract", default="v19", choices=["v19", "v18"],
                         help="判斷契約：v19（預設，瘦身包＋五出手點）／v18（舊包，A/B 或回退用）")
    p_judge.add_argument("--out", help="輸出 bundle 路徑（無 --run-dir 時必填）")
    p_judge.set_defaults(func=cmd_judge)

    p_gate = sub.add_parser("gate", help="組判斷層 critic 的輸入 bundle")
    p_gate.add_argument("--run-dir", help=".dd_build/runs/{T}_{D}/ 目錄（讀 evidence.json／digest.json／judgment.json）")
    p_gate.add_argument("--evidence", help="evidence.json 路徑（無 --run-dir 時必填）")
    p_gate.add_argument("--digest", help="digest.json 路徑")
    p_gate.add_argument("--judgment", help="judgment.json 路徑（無 --run-dir 時必填）")
    p_gate.add_argument("--facts", help="facts.json 路徑（v19：閘要看被引用事實的值與原文；預設 run_dir/facts.json）")
    p_gate.add_argument("--transcript", help="逐字稿檔路徑；未給則由 evidence.transcripts 自動找")
    p_gate.add_argument("--gate-contract", help="gate_contract.md 路徑（預設 scripts/dd_prompts/gate_contract.md）")
    p_gate.add_argument("--out", help="輸出 bundle 路徑（無 --run-dir 時必填）")
    p_gate.set_defaults(func=cmd_gate)

    p_prose = sub.add_parser("prose", help="組散文（prose）agent 的輸入 bundle（v17 WP4b）")
    p_prose.add_argument("--run-dir", help=".dd_build/runs/{T}_{D}/ 目錄（讀 judgment.json／evidence.json／tables／prose，寫 bundles/prose.md）")
    p_prose.add_argument("--judgment", help="judgment.json 路徑（無 --run-dir 時必填）")
    p_prose.add_argument("--evidence", help="evidence.json 路徑（選填，用於前份裁決一行與數字白名單）")
    p_prose.add_argument("--tables", help="gen_dd_tables.py 產出目錄（無 --run-dir 時必填）")
    p_prose.add_argument("--prose-dir", help="prose/ 輸出目錄（列 C-1 機械段是否已生成；無 --run-dir 時必填）")
    p_prose.add_argument("--out", help="輸出 bundle 路徑（無 --run-dir 時必填）")
    p_prose.set_defaults(func=cmd_prose)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
