#!/usr/bin/env python3
"""validate_report_v19.py — v19 完整版報告的**結構與內容驗收**（WP-H2-3，2026-09-11）。

取代 v19 產物的 70KB 整檔 floor（Codex 2026-09-11 複審裁定 3）。理由：v19 的散文
是條列白話（lead ≤40 字＋2–6 條短條列），寫得好反而短——用 bytes 當深度閘會逼出
灌水，正是 CLAUDE.md QC-38 明講要避免的事。**深度不是長度，是「六問各有結論與可
追溯的理由、反證三視角都在、行動條件齊、該有的表格不是空的、數字沒有憑空冒出來」。**
70KB floor 仍留給 legacy（v15 舊版面）產物，見 `scripts/hooks/pre-commit`。

## 檢查項（每項 FAIL 都會指到 sid，散文 agent 那一輪修補才知道改哪段）

1. **六問各有 lead ＋ 條列**——`s4`（怎麼賺錢）／`s5`（護城河）／`s6`（成長）／
   `s9`（現金與資本配置）／`s10`（估值）／`s12`（可能看錯在哪）各要有一句
   `<p class="lead">`（≤40 字，中文字數不是 bytes）與 ≥2 條 `<li>`，且其中
   ≥2 條帶 fact id（`f_*`）——條列要能追回事實表，不是感想。
2. **三視角反證各 ≥1 條實質內容**——`s12` 要逐條出現「論點失敗」「論點成功但股東
   經濟變差」「價格已反映太多」三個視角名，且該條非佔位。
3. **行動條件齊**——`decision` 段要有「新資金」「已持有」「清倉」三條各自成 `<li>`。
4. **必要表格非空**——H1–H3 假設表（`s2` 內）／情境樹（`table#stree`）／觸發器
   （`table#triggers`）／版本紀錄（`section#revlog` 內）各要有 ≥1 列資料列
   （只有表頭＝空表，算 FAIL）。
5. **頁面數字 ⊆ 白名單**——散文自己寫的文字（扣掉機械注入的 `table`／`details`／
   `.mach` 小字）裡的數字，必須都能在 judgment（選配加 facts／scenario_meta）
   找得到。共用 `validate_prose.py` 的抽取與白名單實作，不另立一套口徑。
6. **佔位文字不算過**——「（略）」「TODO」「TBD」「待補」「—」整段這類佔位，
   出現在 lead／條列／必要表格的資料格裡一律 FAIL；標題齊全不等於寫完。

## 用法

    python3 scripts/validate_report_v19.py REPORT.html --judgment judgment.json \\
        [--facts facts.json] [--scenario-meta scenario_meta.json] [--json]

`--json` 印 `{"ok": bool, "findings": [{"sid": …, "reason": …}, …]}`，供
`ddreport.py` 的散文閘逐 sid 歸因；不帶時印人讀清單。exit 0＝PASS。

Python 3.9 相容。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))
import validate_prose  # noqa: E402 — 數字抽取與白名單的單一權威，不複製一套

# 六問 → 散文段（依 scripts/dd_schema/section_map.json 的 answers.q1…q6 對映；
# q1 的判斷句落 s4 商模、q4 落 s9 治理與資本配置，不是望文生義的順號）。
SIX_QUESTION_SIDS = {
    "s4": "問一 怎麼賺錢",
    "s5": "問二 競爭優勢",
    "s6": "問三 成長",
    "s9": "問四 現金與資本配置",
    "s10": "問五 估值",
    "s12": "問六 可能看錯在哪",
}

LEAD_MAX_CHARS = 40
MIN_BULLETS = 2
MIN_FACT_REF_BULLETS = 2

# 三視角＝judgment.schema.json 的 blind_spots[].view enum，逐字對齊。
THREE_VIEWS = ("論點失敗", "論點成功但股東經濟變差", "價格已反映太多")
ACTION_CONDITIONS = ("新資金", "已持有", "清倉")

_FACT_ID_RE = re.compile(r"\bf_[0-9a-zA-Z_]+")
# 佔位：整段就只有這些字（或空白）才算佔位；句子裡出現破折號不算。
_PLACEHOLDER_RE = re.compile(
    r"^(?:[\s　]*(?:（略）|\(略\)|TODO|TBD|待補|待填|N/A|NA|—|–|-|…|\.\.\.)[\s　]*)+$",
    re.I,
)

_TAG_RE = re.compile(r"<[^>]+>")
_SECTION_RE = re.compile(r'<section\b[^>]*\bid="(?P<sid>[^"]+)"[^>]*>(?P<body>.*?)</section>', re.S)
_LEAD_RE = re.compile(r'<p\b[^>]*class="[^"]*\blead\b[^"]*"[^>]*>(.*?)</p>', re.S)
_LI_RE = re.compile(r"<li\b[^>]*>(.*?)</li>", re.S)
_TABLE_BY_ID_RE = r'<table\b[^>]*\bid="{0}"[^>]*>(.*?)</table>'
_ANY_TABLE_RE = re.compile(r"<table\b[^>]*>(.*?)</table>", re.S)
_ROW_RE = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.S)
_MACH_RE = re.compile(r'<div\b[^>]*class="[^"]*\bmach\b[^"]*"[^>]*>.*?</div>', re.S)
_DETAILS_RE = re.compile(r"<details\b.*?</details>", re.S)


def _text(html_fragment: str) -> str:
    """去標籤＋還原常用 entity＋收斂空白。只給長度與關鍵詞比對用。"""
    t = _TAG_RE.sub(" ", html_fragment)
    for ent, ch in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&nbsp;", " "),
                    ("&quot;", '"'), ("&#39;", "'")):
        t = t.replace(ent, ch)
    return re.sub(r"\s+", " ", t).strip()


def _is_placeholder(text: str) -> bool:
    return not text.strip() or bool(_PLACEHOLDER_RE.match(text.strip()))


def _sections(html_text: str) -> dict:
    return {m.group("sid"): m.group("body") for m in _SECTION_RE.finditer(html_text)}


def _authored_text(body: str) -> str:
    """段內「散文 agent 自己寫的」文字：扣掉機械注入的折疊區、表格與段尾機器小字。"""
    t = _DETAILS_RE.sub(" ", body)
    t = _ANY_TABLE_RE.sub(" ", t)
    t = _MACH_RE.sub(" ", t)
    return t


def _table_has_data_row(table_inner: str) -> bool:
    """至少一列有 `<td>` 且該列不是整列佔位。只有 `<th>` 表頭＝空表。"""
    for row in _ROW_RE.finditer(table_inner):
        inner = row.group(1)
        if "<td" not in inner:
            continue
        cells = re.findall(r"<td\b[^>]*>(.*?)</td>", inner, re.S)
        if any(not _is_placeholder(_text(c)) for c in cells):
            return True
    return False


def _check_six_questions(sections: dict) -> list:
    findings = []
    for sid, label in SIX_QUESTION_SIDS.items():
        body = sections.get(sid)
        if body is None:
            findings.append((sid, "{0}：整段不存在（v19 版面 13 段皆為必交）".format(label)))
            continue
        leads = _LEAD_RE.findall(body)
        if not leads:
            findings.append((sid, "{0}：缺一句 <p class=\"lead\"> 結論".format(label)))
        else:
            lead_text = _text(leads[0])
            if _is_placeholder(lead_text):
                findings.append((sid, "{0}：lead 是佔位文字（{1!r}）".format(label, lead_text[:20])))
            elif len(lead_text) > LEAD_MAX_CHARS:
                findings.append((sid, "{0}：lead {1} 字 > {2} 字——lead 是一句結論不是摘要段".format(
                    label, len(lead_text), LEAD_MAX_CHARS)))
        authored = _authored_text(body)
        bullets = [_text(b) for b in _LI_RE.findall(authored)]
        real = [b for b in bullets if not _is_placeholder(b)]
        if len(real) < MIN_BULLETS:
            findings.append((sid, "{0}：實質條列 {1} 條 < {2} 條（佔位條不算）".format(
                label, len(real), MIN_BULLETS)))
        with_fact = [b for b in real if _FACT_ID_RE.search(b)]
        if len(with_fact) < MIN_FACT_REF_BULLETS:
            findings.append((sid, "{0}：帶 fact id（f_*）的條列 {1} 條 < {2} 條——"
                                  "承重條列要追得回事實表".format(
                                      label, len(with_fact), MIN_FACT_REF_BULLETS)))
    return findings


def _check_three_views(sections: dict) -> list:
    body = sections.get("s12")
    if body is None:
        return [("s12", "三視角反證：s12 整段不存在")]
    bullets = [_text(b) for b in _LI_RE.findall(_authored_text(body))]
    findings = []
    for view in THREE_VIEWS:
        hit = [b for b in bullets if view in b]
        if not hit:
            findings.append(("s12", "三視角反證缺「{0}」——每個視角至少一條".format(view)))
            continue
        # 「有這個詞」不等於「寫了東西」：扣掉視角名之後還要剩實質內容。
        if all(_is_placeholder(b.replace(view, "").strip(" ：:｜|")) for b in hit):
            findings.append(("s12", "三視角反證「{0}」只有標題沒有內容".format(view)))
    return findings


def _check_action_conditions(sections: dict) -> list:
    body = sections.get("decision")
    if body is None:
        return [("decision", "行動條件：decision 整段不存在")]
    bullets = [_text(b) for b in _LI_RE.findall(_authored_text(body))]
    findings = []
    for cond in ACTION_CONDITIONS:
        hit = [b for b in bullets if cond in b]
        if not hit:
            findings.append(("decision", "行動條件缺「{0}」——三種情境各一條獨立條列".format(cond)))
        elif all(_is_placeholder(b.replace(cond, "").strip(" ：:｜|")) for b in hit):
            findings.append(("decision", "行動條件「{0}」只有標題沒有條件與動作".format(cond)))
    return findings


def _check_required_tables(html_text: str, sections: dict) -> list:
    findings = []

    def _by_id(table_id):
        m = re.search(_TABLE_BY_ID_RE.format(re.escape(table_id)), html_text, re.S)
        return m.group(1) if m else None

    def _first_table_in(sid):
        body = sections.get(sid)
        if body is None:
            return None
        m = _ANY_TABLE_RE.search(body)
        return m.group(1) if m else None

    for sid, label, inner in (
        ("s2", "H1–H3 核心假設表", _first_table_in("s2")),
        ("s10", "情境樹（table#stree）", _by_id("stree")),
        ("decision", "監測與觸發器（table#triggers）", _by_id("triggers")),
        ("revlog", "版本紀錄", _first_table_in("revlog")),
    ):
        if inner is None:
            findings.append((sid, "必要表格缺席：{0}".format(label)))
        elif not _table_has_data_row(inner):
            findings.append((sid, "必要表格是空表（只有表頭或整列佔位）：{0}".format(label)))
    return findings


def _check_numbers(sections: dict, ref_numbers: set) -> list:
    findings = []
    for sid, body in sections.items():
        text = _text(_authored_text(body))
        # `uncovered_in_text` 回 [(raw, context), ...]，不是 dict。
        misses = validate_prose.uncovered_in_text(text, ref_numbers)
        if misses:
            sample = "、".join("{0}（{1}）".format(raw, ctx) for raw, ctx in misses[:3])
            findings.append((sid, "{0} 個數字不在白名單：{1}".format(len(misses), sample)))
    return findings


# 機械段：內容全由 gen_dd_tables.py 的 v19 分支生成（表格／折疊區），散文 agent
# 不寫也不該寫——整段佔位掃描把它們排除，否則「內容是一張表」會被誤判成空段。
MECHANICAL_SIDS = ("s14", "appA", "appB", "appC", "revlog")


def _check_placeholders(sections: dict) -> list:
    """lead／條列以外的整段佔位：整個 section 扣掉標題後沒有實質文字。"""
    findings = []
    for sid, body in sections.items():
        if sid in MECHANICAL_SIDS:
            continue
        authored = _text(re.sub(r"<h2\b.*?</h2>", " ", _authored_text(body), flags=re.S))
        if _is_placeholder(authored):
            findings.append((sid, "整段是佔位或空白——標題齊全不算寫完"))
    return findings


def validate(report_path, judgment_path=None, facts_path=None, scenario_meta_path=None):
    html_text = Path(report_path).read_text(encoding="utf-8")
    sections = _sections(html_text)
    findings = []
    findings += _check_placeholders(sections)
    findings += _check_six_questions(sections)
    findings += _check_three_views(sections)
    findings += _check_action_conditions(sections)
    findings += _check_required_tables(html_text, sections)

    if judgment_path:
        numbers = set()
        for path in (judgment_path, facts_path, scenario_meta_path):
            if path and Path(path).exists():
                numbers |= validate_prose.collect_numbers(
                    json.loads(Path(path).read_text(encoding="utf-8")))
        findings += _check_numbers(sections, numbers)
    return (not findings), findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", help="組裝後的 v19 報告 HTML")
    ap.add_argument("--judgment", help="judgment.json（數字白名單來源；不給則跳過數字檢查）")
    ap.add_argument("--facts", help="facts.json（白名單補充）")
    ap.add_argument("--scenario-meta", help="scenario_meta.json（白名單補充）")
    ap.add_argument("--json", action="store_true", help="輸出 JSON（供 ddreport 逐 sid 歸因）")
    args = ap.parse_args(argv)

    ok, findings = validate(args.report, args.judgment, args.facts, args.scenario_meta)
    if args.json:
        print(json.dumps({"ok": ok, "findings": [{"sid": s, "reason": r} for s, r in findings]},
                         ensure_ascii=False))
        return 0 if ok else 1
    if ok:
        print("[PASS] v19 結構驗收：六問、三視角、行動條件、必要表格、數字白名單、佔位掃描全過")
        return 0
    print("[FAIL] v19 結構驗收：{0} 項".format(len(findings)))
    for sid, reason in findings:
        print("- {0}：{1}".format(sid, reason))
    return 1


if __name__ == "__main__":
    sys.exit(main())
