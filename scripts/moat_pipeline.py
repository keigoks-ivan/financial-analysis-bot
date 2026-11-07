#!/usr/bin/env python3
"""scripts/moat_pipeline.py {T} [--mode init|review] [--concurrency N] [--dry-run]
— 護城河三題出題管線，照 .claude/skills/moat-review/SKILL.md v2.0（2026-09-22
定案：三個關鍵問題）。

不下判斷、不給分數、不給寬窄——結論留給讀者。三步：

  1 蒐證（本檔，程式）：既有研究（DD）的護城河／報酬持續期章節全文、dd-meta
    護城河欄位（legacy）、dd-screener 該列與對手列（對手＝既有研究對手表；
    沒有就同 sector 前 3；再沒有就無），review 模式時附上一版三題。
  2 查證＋出題（sonnet + WebSearch/WebFetch，單通完成，初出 ≤10 次／重出
    ≤5 次）：輸出結構化 JSON——一句話機制、三題（每題：q_zh／why_zh／
    evidence／lean／lean_reason_zh／watch）、vs_prior_zh（重出才填）、
    rivals_found（沒有既有對手表時額外查的）。prompt 附 SKILL 的「示範」與
    「錯的出題法」整節。
  3 檢查（opus，只讀，單輪 --json-schema）：只回答四題——①三題是否公司專屬
    且答案會改變判斷 ②為什麼重要有沒有講機制與對手為何做不到 ③偏向與證據
    是否一致 ④追蹤條件是否可觀察。任一否 → 第 2 步帶理由重做一次，再不過
    不落檔。
  4 把關（scripts/check_moat_review.py，程式）：結構齊全、禁語、全形、正文
    無對手名字。FAIL 不落檔，記進 docs/stock-dash/data/moat/_failures.json。

出題者（sonnet）與檢查者（opus）永不同模型（repo 鐵律）。批次用
--concurrency 控制，--dry-run 只印證據包與各步驟即將送出的 prompt 大小，
不呼叫任何模型。

Usage:
    python3 scripts/moat_pipeline.py NVDA --mode init
    python3 scripts/moat_pipeline.py NVDA --mode review
    python3 scripts/moat_pipeline.py NVDA,TSM,AMD --mode init --concurrency 2
    python3 scripts/moat_pipeline.py NVDA --mode init --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
DD2_DIR = HERE / "dd2"
for _p in (str(HERE), str(DD2_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import build_stock_dash as bsd  # noqa: E402
import spawn as sp  # noqa: E402
import check_moat_review as cmr  # noqa: E402

MOAT_DIR = bsd.MOAT_DIR
DD_DIR = bsd.DD_DIR
FAILURES_PATH = MOAT_DIR / "_failures.json"
AGENTS_DIR = REPO_ROOT / "_build" / "moat_pipeline_agents"
PROMPTS_DIR = REPO_ROOT / "_build" / "moat_pipeline_prompts"

POSE_MODEL = "sonnet"
GATE_MODEL = "opus"
POSE_MAX_TURNS = {"init": 16, "review": 10}  # 10／5 次工具呼叫 + 幾通處理結果＋最終結構化答案的緩衝
SKILL_MD_PATH = REPO_ROOT / ".claude" / "skills" / "moat-review" / "SKILL.md"


def _load_skill_demo_section():
    """從 SKILL.md 現讀「## 示範」整節（含 NVDA 三題範例＋錯的出題法），原文
    附進出題 prompt 當範本——不在這裡複製一份寫死，SKILL.md 之後改範例，
    出題 prompt 自動跟著換，不用同步兩個地方。找不到就回空字串並讓呼叫端
    知道（prompt 會少一段，但不會整個炸掉）。"""
    try:
        text = SKILL_MD_PATH.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return ""
    m = re.search(r'(## 示範.*?)\n## (?!#)', text, re.S)
    if m:
        return m.group(1).strip()
    # 找不到下一個 "## " 邊界就抓到「## 流程」為止（示範是流程之前的最後一節）
    m = re.search(r'(## 示範.*?)\n## 流程', text, re.S)
    return m.group(1).strip() if m else ""


# ═══════════════════════════════════════════════════════ 第 1 步：蒐證 ════

def all_dd_tickers():
    tickers = set()
    for f in DD_DIR.glob("DD_*.html"):
        m = re.match(r'DD_([A-Z0-9.\-]+)_\d{8}\.html$', f.name)
        if m:
            tickers.add(m.group(1))
    return sorted(tickers)


def latest_dd_with_meta(ticker):
    latest = None
    for f in bsd.find_dd_files(ticker):
        meta, html = bsd.extract_dd_meta(f)
        if meta:
            latest = (f, meta, html)
    return latest


def _extract_durability_text(sections, max_chars=8000):
    for sid, inner in sections.items():
        block = bsd._find_subblock(inner, ["報酬持續期檢核", "ROIC durability", "報酬持續期"])
        if block:
            return sid, bsd._strip_tags(block)[:max_chars]
    return None, None


def _self_row_from_dd_screener(ticker, row):
    fund = (row.get("fund") if row else None) or {}
    return {
        "roic_ltm_pct": row.get("roic") if row else None,
        "roic_3y_avg_pct": row.get("roic_3y_avg_pct") if row else None,
        "roic_5y_avg_pct": row.get("roic_5y_avg_pct") if row else None,
        "roic_vs_5y_x": row.get("roic_vs_5y_x") if row else None,
        "roic_trend_5y": row.get("roic_trend_5y") if row else None,
        "incremental_roic_pct": row.get("incremental_roic_pct") if row else None,
        "gm_ltm_pct": fund.get("gm_ltm_pct"),
        "rev_yoy_fq0_pct": fund.get("rev_yoy_fq0_pct"), "rev_yoy_fq1_pct": fund.get("rev_yoy_fq1_pct"),
        "rev_yoy_fq2_pct": fund.get("rev_yoy_fq2_pct"), "rev_yoy_fq3_pct": fund.get("rev_yoy_fq3_pct"),
        "eps_fy_next": row.get("eps_fy_next") if row else None,
        "eps_fy_next_revision_pct": row.get("eps_fy_next_revision_pct") if row else None,
        "pe_ntm_x": fund.get("pe_ntm_x"), "sector": row.get("sector") if row else None,
    }


def _rival_rows_from_dd_stocks(rival_tickers, dd_stocks):
    stocks_by_ticker = {s.get("ticker"): s for s in (dd_stocks or [])}
    out = []
    for rt in rival_tickers:
        rr = stocks_by_ticker.get(rt)
        if not rr:
            continue
        rf = rr.get("fund") or {}
        out.append({"ticker": rt, "gm_ltm_pct": rf.get("gm_ltm_pct"), "roic": rr.get("roic"),
                    "rev_yoy_fq0_pct": rf.get("rev_yoy_fq0_pct"), "pe_ntm_x": rf.get("pe_ntm_x")})
    return out


def gather_evidence(ticker, mode, dd_stocks, as_of):
    """回傳 (packet, gaps)。packet 不含任何 LLM 產出，純機械組出的證據材料。"""
    gaps = []
    row, _ = bsd.find_dd_screener_row(ticker)
    if row is None:
        gaps.append("不在 dd-screener 名單，自身機械欄位缺")
    self_row = _self_row_from_dd_screener(ticker, row)

    dd_info = None
    found = latest_dd_with_meta(ticker)
    if found:
        dd_path, meta, html = found
        dd_rel = f"/dd/{dd_path.name}"
        sections = bsd._sections_by_id(html)
        moat_sid, moat_inner = bsd._find_section_by_keyword(sections, ["護城河"])
        moat_text = bsd._strip_tags(moat_inner)[:12000] if moat_inner else None
        if not moat_text:
            gaps.append("既有研究找不到護城河章節文字（標題關鍵字比對不到）")
        _, durability_text = _extract_durability_text(sections)
        parsed = bsd.parse_dd_moat_section(html, dd_rel)
        rival_table_raw = parsed.get("rival_table")
        dd_info = {
            "dd_date": meta.get("date"), "dd_path": dd_rel,
            "moat_section_text": moat_text, "durability_section_text": durability_text,
            "legacy": {"grade": meta.get("moat"), "score": meta.get("moat_score"),
                      "execution": meta.get("moat_execution"), "pricing_power": meta.get("moat_pricing_power"),
                      "trend": meta.get("moat_trend"), "growth_durability": meta.get("growth_durability"),
                      "endo_growth_ceiling": meta.get("endo_growth_ceiling"),
                      "kill_metrics": meta.get("kill_metrics") or []},
            "rival_table_raw": rival_table_raw,
        }
    else:
        gaps.append("找不到任何既有研究（DD）——本次為無研究出題，一樣要出三題，不寫「尚未出題」")

    rival_tickers = []
    rival_source = None
    if dd_info and dd_info.get("rival_table_raw"):
        rival_tickers = bsd._rival_tickers_from_table(dd_info["rival_table_raw"], ticker)
        if rival_tickers:
            rival_source = "既有研究對手表"
    if not rival_tickers:
        sector = self_row.get("sector")
        if sector:
            same_sector = [s["ticker"] for s in (dd_stocks or [])
                           if s.get("sector") == sector and s.get("ticker") != ticker]
            rival_tickers = same_sector[:3]
            if rival_tickers:
                rival_source = "dd-screener 同 sector 前 3"
    if not rival_tickers:
        gaps.append("沒有既有研究對手表，也沒有同 sector 名單可比——出題步會另外用查證補")
    rival_rows = _rival_rows_from_dd_stocks(rival_tickers, dd_stocks)

    prior = None
    if mode == "review":
        existing_path = MOAT_DIR / f"{ticker}.json"
        if existing_path.exists():
            try:
                existing = json.loads(existing_path.read_text(encoding="utf-8"))
                prior = existing.get("current")
            except Exception:  # noqa: BLE001
                pass
        if prior is None:
            gaps.append("--mode review 但找不到既有三題檔，退回等同初出處理")

    return {
        "ticker": ticker, "mode": mode, "as_of": as_of,
        "self_row": self_row, "dd_info": dd_info,
        "rival_tickers": rival_tickers, "rival_source": rival_source, "rival_rows": rival_rows,
        "prior_pose": prior,
    }, gaps


# ═══════════════════════════════════════════════ 證據池（給模型讀的機械摘要）════

def build_evidence_pool(packet):
    pool = []
    idx = [1]

    def add(kind, source, date, text):
        eid = f"e{idx[0]}"
        idx[0] += 1
        pool.append({"id": eid, "kind": kind, "source": source, "date": date, "text": text})
        return eid

    sr = packet["self_row"]
    as_of = packet["as_of"]
    ticker = packet["ticker"]
    if sr.get("roic_ltm_pct") is not None:
        add("mechanical", "dd-screener", as_of,
            f"{ticker} ROIC：LTM {sr['roic_ltm_pct']}%／3年均 {sr.get('roic_3y_avg_pct')}%／"
            f"5年均 {sr.get('roic_5y_avg_pct')}%（現值/5年均 {sr.get('roic_vs_5y_x')}x，5年趨勢 {sr.get('roic_trend_5y')}）")
    if sr.get("gm_ltm_pct") is not None:
        add("mechanical", "dd-screener", as_of, f"{ticker} 毛利率(LTM) {sr['gm_ltm_pct']}%")
    if sr.get("incremental_roic_pct") is not None:
        add("mechanical", "dd-screener", as_of, f"{ticker} 增量ROIC {sr['incremental_roic_pct']}%")
    fq = [sr.get("rev_yoy_fq3_pct"), sr.get("rev_yoy_fq2_pct"), sr.get("rev_yoy_fq1_pct"), sr.get("rev_yoy_fq0_pct")]
    if any(v is not None for v in fq):
        add("mechanical", "dd-screener", as_of,
            f"{ticker} 近4季營收年增（舊到新）：" + " → ".join(f"{v}%" if v is not None else "無資料" for v in fq))
    if sr.get("eps_fy_next") is not None:
        add("mechanical", "dd-screener", as_of,
            f"{ticker} 明年度EPS預估 {sr['eps_fy_next']}（近1月修正 {sr.get('eps_fy_next_revision_pct')}%）")
    if sr.get("pe_ntm_x") is not None:
        add("mechanical", "dd-screener", as_of, f"{ticker} NTM本益比 {sr['pe_ntm_x']}x")

    for rr in packet["rival_rows"]:
        add("mechanical", "dd-screener", as_of,
            f"對手 {rr['ticker']}：毛利率(LTM) {rr.get('gm_ltm_pct')}%／ROIC {rr.get('roic')}%／"
            f"營收年增(最新季) {rr.get('rev_yoy_fq0_pct')}%／NTM本益比 {rr.get('pe_ntm_x')}x")

    dd_info = packet.get("dd_info")
    if dd_info:
        lg = dd_info["legacy"]
        add("research", "既有研究 dd-meta", dd_info["dd_date"],
            f"既有研究護城河評級 {lg.get('grade')}（執行力 {lg.get('execution')}／定價權 {lg.get('pricing_power')}／"
            f"權威趨勢 {lg.get('trend')}）")
        if lg.get("kill_metrics"):
            for km in lg["kill_metrics"]:
                add("research", "既有研究 kill_metrics", dd_info["dd_date"],
                    f"{km.get('metric')}：{km.get('bear_threshold')}（{km.get('window')}）")
        if dd_info.get("moat_section_text"):
            add("research", "既有研究護城河章節全文", dd_info["dd_date"], dd_info["moat_section_text"])
        if dd_info.get("durability_section_text"):
            add("research", "既有研究報酬持續期章節全文", dd_info["dd_date"], dd_info["durability_section_text"])

    prior = packet.get("prior_pose")
    if prior:
        add("prior_pose", "上一版一句話", prior.get("date"), f"上一版一句話機制：{prior.get('one_liner_zh') or ''}")
        for q in (prior.get("questions") or []):
            add("prior_pose", "上一版問題", prior.get("date"),
                f"「{q.get('q_zh')}」→ 偏向 {q.get('lean')}（{q.get('lean_reason_zh') or ''}）")

    return pool


def _facts_to_pool_entries(facts, start_idx):
    entries = []
    idx = start_idx
    for f in facts or []:
        if not isinstance(f, dict):
            continue
        entries.append({"id": f"w{idx}", "kind": "web_verified",
                        "source": f.get("source") or "未指名來源", "date": f.get("date") or "未附日期",
                        "text": f.get("fact") or ""})
        idx += 1
    return entries


# ═══════════════════════════════════════════════════ 第 2 步：查證＋出題 ════

_POSE_PROMPT = """# 護城河查證＋出題（moat_pipeline.py 第 2 步，sonnet + WebSearch/WebFetch，單通完成）

方法照 `.claude/skills/moat-review/SKILL.md` v2.0。你要做兩件事：①查證事實
②幫這檔股票挑出**三個對這家公司最關鍵、答案會改變護城河判斷的專屬問題**。
**不下判斷、不給分數、不給寬窄**——結論留給讀者，你只負責把機制、證據、
偏向、追蹤條件擺清楚。

**查證上限：{max_queries} 次 WebSearch／WebFetch**（這是{mode_label}）。證據
包裡已經有的機械數字（ROIC／毛利率／營收成長，見下面「證據包」）不用重查，
只查機械層與既有研究都沒有、但對出題有幫助的事實（份額數字、對手技術或
產能追趕進度、最近的重大事件）。查不到就在對應事實寫「未能確認」，不要編。
每條事實都要附來源（網站名或報告名）與日期（找不到確切日期就寫「未附
日期」）。

## 怎麼挑三題
先想清楚這家公司靠什麼綁住客戶（一到兩個核心機制），三題要分別打在：
①核心機制會不會被繞過；②現在看到的變化是機制在鬆還是數字在動；③對手或
客戶最可能從哪裡突破。三題合起來要能讓讀者自己判斷「護城河現在如何、往哪
走」。**問題必須是這家公司專屬的**——把三題的答案都想成最壞情況，護城河會
不會不在？會＝題選對了；三題答案都不影響護城河＝重選。通用問題（像「客戶
會不會轉單？」「毛利率能不能維持？」「競爭會不會加劇？」）不算。**寫完每題
做一次替換測試：把公司換成一家同業，題目還讀得通，就是太通用，重寫。**

下面是 SKILL.md 的「示範」整節（含 NVDA 三題範例＋錯的出題法），照這個
標準做：

────────────────────────────────────────────────────────────────
{skill_demo_section}
────────────────────────────────────────────────────────────────

{feedback_section}
## 輸出格式（每題四樣東西）
one_liner_zh：一句話講清楚綁住客戶的機制是什麼（不用列點，一句話）。
questions：恰三題，每題：
- q_zh：問題本身，具體到「哪個客戶、哪一層、什麼事件」，不是通用問題。
- why_zh：為什麼這題重要——這題對應哪個綁住客戶的機制、這個機制為什麼是
  護城河的關鍵（**對手為什麼做不到**），2-4 句。**對手要按類型分開講**（例如
  「通用 GPU 對手」「客製化晶片設計商」「客戶自研晶片」），每一類各自講它缺
  的是哪個機制；引用的數字必須是那一類對手的數字，不能拿一家的數字代表全部
  同業。如果某一類對手的數字比本公司還好，要說明為什麼它不算反例，或直接承
  認這一段擋不住。只列數字、不講機制，不算回答了「對手為什麼做不到」。
- evidence：2-4 條事實，每條 {{text_zh, source, date}}；查不到的事實
  text_zh 直接寫「未能確認」，date 可留「未附日期」。
- lean：目前證據偏向，只能是「撐住」「鬆動」「不明」三選一——這是「證據
  往哪邊倒」不是判斷；證據互相打架就寫「不明」。
- lean_reason_zh：一句話理由，說明為什麼偏向這一邊。
- watch：1-2 條「什麼事會改變答案」，每條 {{desc_zh, metric_key, threshold,
  manual}}；desc_zh 是條件描述，metric_key 只能從下面清單挑（給下游機械層
  每天更新現在值用，括號是口徑）：
{metric_key_list}
  threshold 必須寫數字（如「連2季低於70%」）或具體事件（誰、做了什麼、在
  哪裡公開），不可以只寫「顯著」「大幅」。**門檻的口徑要跟 metric_key 一樣**：
  單季數字、公司財測、非 GAAP、分項營收這類，清單裡沒有同口徑欄位，就
  metric_key 留空字串、manual=true（機械層會標「需人工」，不自動判斷）。拿單
  季財測門檻去綁近四季累計欄位，條件會一開始就成立或永遠不觸發，這是錯的。
  程式會在送檢查前先擋這幾條。

vs_prior_zh：{vs_prior_instruction}

rivals_found：{rivals_found_instruction}

**禁止買進／賣出／加碼／減碼／建議持有這類指令語氣；正文不可出現「DD」
字樣，也不可以出現任何對手公司名稱或股票代號**（對手用類型稱呼，例如「通
用 GPU 對手」「客製化晶片設計商」「客戶自研晶片」，不要籠統寫「同業」；對手名字與數字只能放進 evidence 的 source 欄位或
rivals_found，絕對不要寫進 q_zh／why_zh／lean_reason_zh／
evidence.text_zh／watch.desc_zh 裡）。中文一律全形標點。

## 證據包（本檔既有的機械與既有研究資料）
```json
{evidence_json}
```

## 證據池（程式先組好的編號摘要，方便你快速掃過）
```json
{evidence_pool_json}
```

只用結構化輸出作答，不要多寫文字。
"""

_FEEDBACK_SECTION_TMPL = """## 上一輪被 opus 檢查退回，這次要修正
上一版的三題被 opus 檢查退回，理由如下，**這次出題必須針對每一條具體修正**
（不是隨便改個字就好，答不出來就換一題）：
{gate_notes}

────────────────────────────────────────────────────────────────

"""


def _pose_answer_schema():
    return {
        "type": "object",
        "properties": {
            "one_liner_zh": {"type": "string"},
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "q_zh": {"type": "string"}, "why_zh": {"type": "string"},
                        "evidence": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"text_zh": {"type": "string"}, "source": {"type": "string"},
                                              "date": {"type": "string"}},
                                "required": ["text_zh", "source", "date"],
                            },
                        },
                        "lean": {"type": "string"}, "lean_reason_zh": {"type": "string"},
                        "watch": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"desc_zh": {"type": "string"}, "metric_key": {"type": "string"},
                                              "threshold": {"type": "string"}, "manual": {"type": "boolean"}},
                                "required": ["desc_zh", "metric_key", "threshold", "manual"],
                            },
                        },
                    },
                    "required": ["q_zh", "why_zh", "evidence", "lean", "lean_reason_zh", "watch"],
                },
            },
            "vs_prior_zh": {"type": "string"},
            "rivals_found": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["one_liner_zh", "questions", "vs_prior_zh", "rivals_found"],
    }


def verify_and_pose(ticker, packet, evidence_pool, dry_run=False, feedback_notes=None, attempt=1):
    mode = packet["mode"]
    max_turns = POSE_MAX_TURNS.get(mode, 16)
    mode_label = "初出" if mode == "init" else "重出"
    n_queries = 10 if mode == "init" else 5

    if mode == "review" and packet.get("prior_pose"):
        p = packet["prior_pose"]
        prior_qs = "；".join(f"「{q.get('q_zh')}」→{q.get('lean')}" for q in (p.get("questions") or []))
        vs_prior_instruction = f"這是重出，要對上一版三題交代：哪題答案變了、哪題不再關鍵、換了什麼題，2-3 句。上一版三題：{prior_qs}"
    else:
        vs_prior_instruction = "這是初次出題，這裡填空字串 \"\"。"

    if packet.get("rival_tickers"):
        rivals_found_instruction = "證據包已經有既有對手清單，這裡可以留空陣列（不用重找）。"
    else:
        rivals_found_instruction = ("證據包沒有現成對手清單，請在查證時額外花 2-3 次查證，找出這檔真正的 2-3 家"
                                    "可比對手（ticker 代號），並各自查到至少一項可比數字（附來源與日期，寫進"
                                    "某一題的 evidence）；找到的 ticker 代號另外列進 rivals_found；真的查不到就"
                                    "給空陣列，不要硬湊。")

    feedback_section = ""
    if feedback_notes:
        feedback_section = _FEEDBACK_SECTION_TMPL.format(
            gate_notes="\n".join(f"- {n}" for n in feedback_notes))

    demo_section = _load_skill_demo_section() or "（SKILL.md 示範節讀取失敗，沒有範本可附——仍照上面的出題標準做）"
    evidence_json = json.dumps({k: v for k, v in packet.items()}, ensure_ascii=False, separators=(",", ":"))
    pool_json = json.dumps(evidence_pool, ensure_ascii=False, separators=(",", ":"))
    prompt_text = _POSE_PROMPT.format(max_queries=n_queries, mode_label=mode_label,
                                      skill_demo_section=demo_section, feedback_section=feedback_section,
                                      metric_key_list="\n".join(f"  - {k}（{v}）" for k, v in cmr.KNOWN_METRIC_KEYS.items()),
                                      vs_prior_instruction=vs_prior_instruction,
                                      rivals_found_instruction=rivals_found_instruction,
                                      evidence_json=evidence_json, evidence_pool_json=pool_json)
    if dry_run:
        return {"ok": True, "dry_run": True, "prompt_chars": len(prompt_text)}, None

    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    prompt_path = PROMPTS_DIR / f"{ticker}_pose_{attempt}.md"
    prompt_path.write_text(prompt_text, encoding="utf-8")
    out_json = AGENTS_DIR / f"{ticker}_pose_{attempt}.json"
    schema_str = json.dumps(_pose_answer_schema(), ensure_ascii=False)
    r = _oneshot_stream_more_turns(prompt_path, POSE_MODEL, out_json, REPO_ROOT,
                                   extra_args=["--json-schema", schema_str], max_turns=max_turns,
                                   tools=["WebSearch", "WebFetch"], timeout_s=1200)
    answer = None
    if r.get("ok"):
        so = r.get("structured_output")
        if isinstance(so, dict):
            answer = so
        elif r.get("result_text"):
            obj, _err = sp.strip_json(r["result_text"])
            if isinstance(obj, dict):
                answer = obj
    return r, answer


# ═══════════════════════════════════════════════════════════ 第 3 步：檢查 ════

_GATE_PROMPT = """# 護城河出題檢查（moat_pipeline.py 第 3 步，opus 唯讀，單輪 --json-schema）

方法照 `.claude/skills/moat-review/SKILL.md` v2.0 第 3 步「檢查」。你**只讀**
下面 sonnet 出的三題 JSON 與證據包，**不能改內容、不能自己查證**，只回答
四個問題（每個都是 true/false）：

① q_specific_ok：三題是否**這家公司專屬**、答案會不會改變護城河判斷？
   （通用問題像「客戶會不會轉單？」「毛利率能不能維持？」算不過；把每題
   答案都想成最壞情況，護城河會不會不在——會才算選對）
② why_mechanism_ok：每題的「為什麼重要」有沒有講到**機制**與**對手為什麼
   做不到**？只是列現象（份額、毛利率數字）沒有解釋機制算不過。
③ lean_consistent_ok：偏向（撐住／鬆動／不明）跟列出的證據是否一致？證據
   明明互相打架卻寫撐住或鬆動＝不過；證據都指向同一邊卻寫不明也算不過。
④ watch_observable_ok：每題的追蹤條件是否可觀察（有明確數字門檻或明確
   事件），不是空話？

任一題「否」，notes 裡要**針對那一題寫一句具體理由**（是哪一題、哪裡不
對，讓下一輪出題知道怎麼改），不要空泛。全部通過 notes 可以是空陣列。

## sonnet 出的三題 JSON
```json
{pose_json}
```

## 證據包（給你核對用，不是要你重新查證）
```json
{evidence_json}
```

只用結構化輸出作答，不要多寫文字。
"""


def _gate_answer_schema():
    return {
        "type": "object",
        "properties": {
            "q_specific_ok": {"type": "boolean"}, "why_mechanism_ok": {"type": "boolean"},
            "lean_consistent_ok": {"type": "boolean"}, "watch_observable_ok": {"type": "boolean"},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["q_specific_ok", "why_mechanism_ok", "lean_consistent_ok", "watch_observable_ok", "notes"],
    }


def gate_check(ticker, packet, pose_answer, dry_run=False, attempt=1):
    evidence_json = json.dumps({k: v for k, v in packet.items()}, ensure_ascii=False, separators=(",", ":"))
    pose_json = json.dumps(pose_answer, ensure_ascii=False, separators=(",", ":"))
    prompt_text = _GATE_PROMPT.format(pose_json=pose_json, evidence_json=evidence_json)
    if dry_run:
        return {"ok": True, "dry_run": True, "prompt_chars": len(prompt_text)}, None

    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    prompt_path = PROMPTS_DIR / f"{ticker}_gate_{attempt}.md"
    prompt_path.write_text(prompt_text, encoding="utf-8")
    out_json = AGENTS_DIR / f"{ticker}_gate_{attempt}.json"
    schema_str = json.dumps(_gate_answer_schema(), ensure_ascii=False)
    r = _oneshot_stream_more_turns(prompt_path, GATE_MODEL, out_json, REPO_ROOT,
                                   extra_args=["--json-schema", schema_str], max_turns=3)
    answer = None
    if r.get("ok"):
        so = r.get("structured_output")
        if isinstance(so, dict):
            answer = so
        elif r.get("result_text"):
            obj, _err = sp.strip_json(r["result_text"])
            if isinstance(obj, dict):
                answer = obj
    return r, answer


def _oneshot_stream_more_turns(prompt_path, model, out_json, cwd, extra_args, max_turns=4, timeout_s=900, tools=None):
    """跟 spawn.oneshot_stream 一樣的事件解析邏輯，但允許帶 max_turns 與（第
    2 步需要的）tools——spawn.py 的 agentic() 不支援 extra_args（無法同時帶
    --json-schema），共用契約不改，這裡自己複製一份，tools 給時額外組
    --allowedTools／--tools 前綴（避免 _stream_cmd 預設把工具清空）。"""
    import subprocess
    prompt_text = Path(prompt_path).read_text(encoding="utf-8")
    full_extra = list(extra_args or [])
    if tools:
        full_extra = ["--allowedTools"] + list(tools) + ["--tools"] + list(tools) + full_extra
    t0 = time.time()
    proc = subprocess.run(sp._stream_cmd(model, max_turns, full_extra), input=prompt_text, capture_output=True,
                          text=True, cwd=str(cwd) if cwd else None, timeout=timeout_s)
    texts, result_ev = [], None
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            content = (ev.get("message") or {}).get("content") or []
            t = "".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
            if t:
                texts.append(t)
        elif ev.get("type") == "result":
            result_ev = ev
    stitched = "".join(texts)
    result_ev = result_ev or {}
    structured_output = result_ev.get("structured_output")
    if not isinstance(structured_output, (dict, list)):
        structured_output = None
    result_text = stitched
    if not result_text and structured_output is not None:
        result_text = result_ev.get("result") or json.dumps(structured_output, ensure_ascii=False)
    if out_json:
        Path(out_json).parent.mkdir(parents=True, exist_ok=True)
        Path(out_json).write_text(json.dumps({"result_event": result_ev, "stitched_text": stitched},
                                             ensure_ascii=False, indent=1), encoding="utf-8")
    return {
        "ok": proc.returncode == 0 and bool(result_text) and result_ev.get("subtype", "success") == "success",
        "result_text": result_text, "structured_output": structured_output,
        "cost_usd": result_ev.get("total_cost_usd"), "subtype": result_ev.get("subtype"),
        "duration_ms": result_ev.get("duration_ms") or int((time.time() - t0) * 1000),
        "returncode": proc.returncode, "stderr_tail": (proc.stderr or "")[-800:],
    }


# ═══════════════════════════════════════════════════ 組裝 moat-v3 current ════

def assemble_current(ticker, packet, pose_answer, gate_answer):
    mode = packet["mode"]
    prior = packet.get("prior_pose")
    version = (prior.get("version", 0) + 1) if prior else 1
    status = "已重出" if mode == "review" else "初出"

    questions = []
    for q in (pose_answer.get("questions") or [])[:3]:
        if not isinstance(q, dict):
            continue
        evidence = [{"text_zh": e.get("text_zh"), "source": e.get("source"), "date": e.get("date")}
                   for e in (q.get("evidence") or []) if isinstance(e, dict)]
        watch = []
        for w in (q.get("watch") or []):
            if not isinstance(w, dict):
                continue
            metric_key = (w.get("metric_key") or "").strip() or None
            watch.append({"desc_zh": w.get("desc_zh"), "metric_key": metric_key,
                         "threshold": w.get("threshold") or None, "current_value": None, "hit": False,
                         "manual": bool(w.get("manual")) or metric_key is None})
        questions.append({"q_zh": q.get("q_zh"), "why_zh": q.get("why_zh"), "evidence": evidence,
                         "lean": q.get("lean"), "lean_reason_zh": q.get("lean_reason_zh"), "watch": watch})

    current = {
        "version": version, "date": packet["as_of"], "status": status,
        "one_liner_zh": pose_answer.get("one_liner_zh"),
        "questions": questions,
        "vs_prior_zh": (pose_answer.get("vs_prior_zh") or None) if mode == "review" else None,
        "rivals": packet["rival_tickers"],
        "legacy_scores": packet["dd_info"]["legacy"] if packet.get("dd_info") else None,
        "gate": gate_answer,
        # 輔助欄位（非 schema 原文逐字列出的部分，但機械層每天要用來更新
        # questions[].watch／變化表，不重新解析一次）：
        "mechanical_snapshot_at_judgment": packet["self_row"],
        "gaps": packet.get("gaps") or [],
    }
    history = list(prior.get("_self_history", [])) if prior else []
    if prior:
        history.append(prior)
    return {"schema": "moat-v3", "ticker": ticker, "current": current,
           "review_due": {"due": False, "reasons": []}, "history": history}


# ═══════════════════════════════════════════════════════════ 第 4 步：把關 ════

def _check_doc_direct(doc, ticker):
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / f"{ticker}.json"
        p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        orig = cmr.MOAT_DIR
        cmr.MOAT_DIR = Path(td)
        try:
            return cmr.check(ticker)
        finally:
            cmr.MOAT_DIR = orig


def _record_failure(ticker, errors, gaps, failures_path=None):
    failures_path = failures_path or FAILURES_PATH
    failures_path.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if failures_path.exists():
        try:
            data = json.loads(failures_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            data = {}
    data[ticker] = {"errors": errors, "gaps": gaps}
    failures_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def _clear_failure(ticker, failures_path=None):
    failures_path = failures_path or FAILURES_PATH
    if not failures_path.exists():
        return
    try:
        data = json.loads(failures_path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return
    if ticker in data:
        del data[ticker]
        failures_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# ═══════════════════════════════════════════════════════════════ 主流程 ════

def run_ticker(ticker, mode, dd_stocks, dry_run=False, out_dir=None):
    """out_dir：給時把最終三題檔寫到 {out_dir}/{ticker}.json 而不是正式
    docs/stock-dash/data/moat/（測試用），失敗紀錄也寫到 {out_dir}/_failures.json。"""
    t0 = time.time()
    as_of = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    target_dir = Path(out_dir) if out_dir else MOAT_DIR
    failures_path = target_dir / "_failures.json"

    packet, gaps = gather_evidence(ticker, mode, dd_stocks, as_of)
    packet["gaps"] = gaps
    evidence_pool = build_evidence_pool(packet)

    if dry_run:
        pose_r, _ = verify_and_pose(ticker, packet, evidence_pool, dry_run=True)
        gate_r, _ = gate_check(ticker, packet, {"placeholder": True}, dry_run=True)
        return {"ticker": ticker, "dry_run": True, "gaps": gaps, "evidence_pool_size": len(evidence_pool),
               "pose_prompt_chars": pose_r["prompt_chars"], "gate_prompt_chars": gate_r["prompt_chars"]}

    costs = {}
    check_keys = ("q_specific_ok", "why_mechanism_ok", "lean_consistent_ok", "watch_observable_ok")
    notes, gate_answer = None, None
    # v2.1：每一輪出題後先跑程式預檢（cmr.watch_rule_errors，不花錢），不過就不送 opus，
    # 直接帶理由重出；總共最多出題兩次，規則同 SKILL「帶理由重做一次，再不過不落檔」。
    for attempt in (1, 2):
        pose_r, pose_answer = verify_and_pose(ticker, packet, evidence_pool, feedback_notes=notes, attempt=attempt)
        costs[f"pose_{attempt}"] = {"cost_usd": pose_r.get("cost_usd"), "duration_ms": pose_r.get("duration_ms"), "ok": pose_r.get("ok")}
        if not pose_r.get("ok") or not pose_answer:
            _record_failure(ticker, [f"出題步驟失敗（第{attempt}次）：subtype={pose_r.get('subtype')} stderr={pose_r.get('stderr_tail')}"],
                            gaps, failures_path)
            return {"ticker": ticker, "ok": False, "costs": costs, "stage": "pose" if attempt == 1 else "pose_retry"}
        if not packet.get("rival_tickers") and pose_answer.get("rivals_found"):
            packet["rival_tickers"] = [str(x).strip().upper() for x in pose_answer["rivals_found"] if str(x).strip()][:3]

        pre = cmr.watch_rule_errors(pose_answer.get("questions") or [])
        if pre:
            costs[f"precheck_{attempt}"] = {"cost_usd": 0, "duration_ms": 0, "ok": False, "errors": pre}
            if attempt == 2:
                _record_failure(ticker, [f"程式預檢兩次都不過：{pre}"], gaps, failures_path)
                return {"ticker": ticker, "ok": False, "costs": costs, "stage": "precheck_final_fail", "notes": pre}
            notes = [f"程式預檢：{e}" for e in pre]
            continue

        gate_r, gate_answer = gate_check(ticker, packet, pose_answer, attempt=attempt)
        costs[f"gate_{attempt}"] = {"cost_usd": gate_r.get("cost_usd"), "duration_ms": gate_r.get("duration_ms"), "ok": gate_r.get("ok")}
        if not gate_r.get("ok") or not gate_answer:
            _record_failure(ticker, [f"檢查步驟失敗（第{attempt}次）：subtype={gate_r.get('subtype')} stderr={gate_r.get('stderr_tail')}"],
                            gaps, failures_path)
            return {"ticker": ticker, "ok": False, "costs": costs, "stage": "gate" if attempt == 1 else "gate_retry"}
        failed = [k for k in check_keys if not gate_answer.get(k)]
        if not failed:
            break
        if attempt == 2:
            _record_failure(ticker, [f"opus 檢查兩次都退回：{gate_answer.get('notes')}"], gaps, failures_path)
            return {"ticker": ticker, "ok": False, "costs": costs, "stage": "gate_final_fail", "notes": gate_answer.get("notes")}
        notes = gate_answer.get("notes") or [f"{k} 未通過" for k in failed]

    doc = assemble_current(ticker, packet, pose_answer, gate_answer)
    errors, warnings = _check_doc_direct(doc, ticker)
    if errors:
        _record_failure(ticker, [f"第4步把關失敗：{e}" for e in errors], gaps, failures_path)
        return {"ticker": ticker, "ok": False, "costs": costs, "stage": "check", "errors": errors}

    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / f"{ticker}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _clear_failure(ticker, failures_path)
    total_cost = sum((c.get("cost_usd") or 0) for c in costs.values())
    total_ms = sum((c.get("duration_ms") or 0) for c in costs.values())
    leans = [q.get("lean") for q in doc["current"]["questions"]]
    return {"ticker": ticker, "ok": True, "one_liner": doc["current"]["one_liner_zh"], "leans": leans,
           "costs": costs, "total_cost_usd": round(total_cost, 4), "total_duration_s": round(total_ms / 1000, 1),
           "warnings": warnings, "gaps": gaps, "gate_notes": gate_answer.get("notes") or [],
           "retried": "pose_2" in costs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", help="逗號分隔的 ticker 清單，或 --all-dd")
    ap.add_argument("--mode", choices=["init", "review"], default="init")
    ap.add_argument("--concurrency", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--all-dd", action="store_true")
    ap.add_argument("--out-dir", default=None,
                    help="三題檔寫到這個目錄而不是正式 docs/stock-dash/data/moat/（測試用）")
    args = ap.parse_args()

    if args.all_dd:
        tickers = all_dd_tickers()
    else:
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]

    dd_stocks = bsd.load_dd_screener().get("stocks", [])
    results = []
    kw = dict(out_dir=args.out_dir)
    if args.dry_run or args.concurrency <= 1:
        for t in tickers:
            results.append(run_ticker(t, args.mode, dd_stocks, dry_run=args.dry_run, **kw))
    else:
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futs = {ex.submit(run_ticker, t, args.mode, dd_stocks, args.dry_run, args.out_dir): t for t in tickers}
            for fut in as_completed(futs):
                results.append(fut.result())

    if args.dry_run:
        for r in results:
            print(f"{r['ticker']}：證據池 {r['evidence_pool_size']} 條｜出題prompt {r['pose_prompt_chars']} 字元｜"
                 f"檢查prompt {r['gate_prompt_chars']} 字元｜gaps={r['gaps']}")
        return

    n_ok = sum(1 for r in results if r.get("ok"))
    n_fail = len(results) - n_ok
    # 失敗路徑只帶 costs（逐步），沒有 total_cost_usd；兩種都算進總費用
    total_cost = sum((r.get("total_cost_usd") if r.get("total_cost_usd") is not None
                      else sum((c.get("cost_usd") or 0) for c in (r.get("costs") or {}).values()))
                     for r in results)
    total_time = sum((r.get("total_duration_s") or 0) for r in results)
    print(f"完成：{n_ok} 成功／{n_fail} 失敗（共 {len(tickers)} 檔）｜總費用 ${total_cost:.4f}｜總秒數 {total_time:.1f}s")
    for r in results:
        if r.get("ok"):
            print(f"  {r['ticker']}：leans={r['leans']} cost=${r['total_cost_usd']} time={r['total_duration_s']}s "
                 f"retried={r['retried']}")
        else:
            print(f"  {r['ticker']}：失敗於 {r.get('stage')}｜{r.get('errors') or r.get('notes')}")


if __name__ == "__main__":
    main()
