#!/usr/bin/env python3
"""dd_facts.py — v19 六問事實表（`facts.json`）的零 LLM 抽取器與驗證器。

WP-H1（2026-09-11）。契約見 `scripts/dd_schema/facts.schema.json` 與
`scripts/dd_schema/facts.md`。

只做兩件事：

1. `extract`：從 `evidence.json`（必要時加 `digest.json`）抽出**機械可抽**的
   事實——`numbers` 底下有明確值、單位與 as-of 的欄位，以及 `coverage`／
   `events` 逐條 finding 的精簡清單（`findings_digest[]`，**不按方向裁掉**）。
   抽不到的題目留空 `facts: []` 並標 `needs_sonnet: true`＋一句說明，**不捏造、
   不假裝完整**——這支腳本沒有判斷，填不出來就要看得見。
2. `check`：用 `validate_judgment.py` 的 draft-07 子集直譯器驗 schema
   （單一權威，不另寫一份驗證器），外加兩條 schema 表達不了的規則：
   fact id 唯一、`value` 為 null 時必須標 `needs_sonnet`。

用法：
  python3 scripts/dd_facts.py extract --run-dir DIR --out facts.json
  python3 scripts/dd_facts.py extract --evidence E.json [--digest D.json] --out F.json
  python3 scripts/dd_facts.py check FACTS.json [--report]

`extract` 的產物是**半成品**：`needs_sonnet` 為 true 的題目由 H2 的事實表
agent 補完。exit 0＝無 FAIL。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import validate_judgment as vj  # noqa: E402 — 重用 schema 子集直譯器，不複製

SCHEMA_PATH = SCRIPT_DIR / "dd_schema" / "facts.schema.json"

QUESTION_KEYS = (
    "q1_business", "q2_moat", "q3_growth",
    "q4_capital", "q5_valuation", "q6_how_wrong",
)
QUESTION_LABELS = {
    "q1_business": "怎麼賺錢",
    "q2_moat": "競爭優勢",
    "q3_growth": "成長",
    "q4_capital": "現金與資本配置",
    "q5_valuation": "估值",
    "q6_how_wrong": "可能看錯在哪",
}

# 機械抽取抽不到、必須由事實表 agent 補的內容（逐題一句，寫進 needs_sonnet_note）。
NEEDS_SONNET_NOTE = {
    "q1_business": "分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。",
    "q2_moat": "護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。",
    "q3_growth": "TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。",
    "q4_capital": "近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。",
    "q5_valuation": "同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。",
    "q6_how_wrong": "歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。",
}

_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")
_COMPACT_DATE_RE = re.compile(r"^(\d{4})(\d{2})(\d{2})$")


def _norm_date(value):
    """evidence.json 的 `date` 兩種寫法都存在（`2026-09-11` 與 `20260906`）——
    facts.schema 只收帶連字號的形狀，這裡統一，不改 evidence 原檔。"""
    if not isinstance(value, str):
        return value
    m = _COMPACT_DATE_RE.match(value.strip())
    return "{0}-{1}-{2}".format(*m.groups()) if m else value.strip()


def _slug(text, maxlen=48):
    """把 metric 名稱轉成 fact id 尾段：只留英數與底線，中文轉成 cjk 序號由呼叫端補。"""
    s = re.sub(r"[^0-9a-zA-Z]+", "_", str(text or "")).strip("_").lower()
    return s[:maxlen]


def _fact(fid, label, value, period, unit, basis, kind, source, **extra):
    fact = {
        "id": fid,
        "label": label,
        "value": value,
        "period": period,
        "unit": unit,
        "basis": basis,
        "kind": kind,
        "source": source,
    }
    for k, v in extra.items():
        if v is not None:
            fact[k] = v
    # 2026-09-11（WP-H2-1）：抽出來就是空值的條目一律自己標 needs_sonnet——
    # `check()` 本來就擋「value 為 null 卻未標 needs_sonnet」，但抽取器沒有自己
    # 遵守，實檔（CIEN 的 `f_kpi3_free_cash_flow`，證據包該列 value 缺）因此讓
    # 機械初稿自己過不了自己的檢查。標記＝誠實的不完整，不是編造。
    if fact.get("value") is None and "needs_sonnet" not in fact:
        fact["needs_sonnet"] = True
    return fact


def _src(stype, ref, as_of=None, citation=None, locator=None):
    s = {"type": stype, "ref": ref}
    if as_of:
        s["as_of"] = as_of
    if citation:
        s["citation"] = citation
    if locator:
        s["locator"] = locator
    return s


# ---------------------------------------------------------------------------
# numbers → facts（逐欄硬對映，不猜）
# ---------------------------------------------------------------------------

def _kpi_facts(numbers, buckets):
    """`numbers.latest_quarter_kpis.items[]` 逐項轉事實。落題規則只看 metric
    字樣：含現金流／SBC／股權薪酬／負債→q4，其餘→q1。分不出來的一律留 q1
    （量化營運事實的預設居所），不另猜。"""
    lqk = numbers.get("latest_quarter_kpis") or {}
    quarter = lqk.get("quarter")
    for i, item in enumerate(lqk.get("items") or []):
        if not isinstance(item, dict):
            continue
        metric = item.get("metric") or f"kpi_{i}"
        # id 用位置（`numbers.latest_quarter_kpis.items[i]`）當骨架——metric 名稱是
        # 中文，轉不出有意義的英數 slug；有英數字樣才接在後面當可讀性提示。
        slug = _slug(metric, 24)
        fid = f"f_kpi{i}" + (f"_{slug}" if slug else "")
        target = "q4_capital" if re.search(
            r"現金流|FCF|SBC|股權薪酬|稀釋|負債|債務|股息|回購", metric
        ) else "q1_business"
        # kind 分類：帶「展望／指引／guidance／outlook／預估／目標」字樣的 KPI 是
        # **預期不是事實**（facts.md §二），一律記 guidance；其餘為已實現。分不出
        # 來的由事實表 agent 複核，程式不猜。
        kind = "guidance" if re.search(
            r"展望|指引|預估|預測|目標|guidance|outlook", metric, re.I) else "realized"
        fact = _fact(
            fid, metric, item.get("value"),
            item.get("as_of") or quarter, item.get("unit"),
            "evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）",
            kind,
            _src("evidence_numbers", f"numbers.latest_quarter_kpis.items[{i}]",
                 as_of=item.get("as_of") or quarter, citation=item.get("source")),
            note=item.get("vs_consensus"),
        )
        buckets[target]["facts"].append(fact)


def _valuation_facts(numbers, buckets):
    q5 = buckets["q5_valuation"]["facts"]
    price = numbers.get("price_at_dd")
    as_of = numbers.get("price_as_of")
    if price is not None:
        q5.append(_fact(
            "f_price_at_dd", "判斷日股價", price, as_of, "USD",
            "收盤價，與情境樹起點同源", "realized",
            _src("evidence_numbers", "numbers.price_at_dd", as_of=as_of),
        ))
    mom = numbers.get("momentum_26w") or {}
    if mom.get("return_26w_pct") is not None:
        q5.append(_fact(
            "f_week26_return_pct", "26 週報酬", mom.get("return_26w_pct"),
            as_of, "%", "含息前價格報酬，對照基準 " + str(mom.get("benchmark") or "—"),
            "realized",
            _src("evidence_numbers", "numbers.momentum_26w.return_26w_pct", as_of=as_of),
        ))
    if mom.get("rsi14") is not None:
        q5.append(_fact(
            "f_rsi14", "RSI(14)", mom.get("rsi14"), as_of, "",
            "日線 14 期；rsi14_usable=" + str(mom.get("rsi14_usable")), "realized",
            _src("evidence_numbers", "numbers.momentum_26w.rsi14", as_of=as_of),
        ))
    rev = numbers.get("consensus_revision") or {}
    latest = rev.get("latest_snapshot") or {}
    for fy in ("fy1", "fy2", "fy3"):
        node = rev.get(fy) or {}
        if node.get("revision_pct") is None:
            continue
        q5.append(_fact(
            f"f_consensus_rev_{fy}_pct", f"{fy.upper()} 共識修正",
            node.get("revision_pct"), node.get("to_date") or latest.get("date"), "%",
            "兩份 Koyfin 快照之間的 EPS 修正幅度（{0} → {1}）".format(
                node.get("from"), node.get("to")),
            "estimate",
            _src("evidence_numbers", f"numbers.consensus_revision.{fy}.revision_pct",
                 as_of=node.get("to_date"), citation=latest.get("file")),
        ))
    for fy in ("fy1", "fy2", "fy3"):
        if latest.get(fy) is None:
            continue
        q5.append(_fact(
            f"f_consensus_eps_{fy}", f"{fy.upper()} 共識 EPS", latest.get(fy),
            latest.get("date"), "USD/share",
            "Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis", "estimate",
            _src("evidence_numbers", f"numbers.consensus_revision.latest_snapshot.{fy}",
                 as_of=latest.get("date"), citation=latest.get("file")),
        ))
    prior90 = rev.get("snapshot_90d_prior") or {}
    if latest.get("fy1") and prior90.get("fy1"):
        try:
            pct = round((float(latest["fy1"]) / float(prior90["fy1"]) - 1) * 100, 2)
        except (TypeError, ValueError, ZeroDivisionError):
            pct = None
        if pct is not None:
            q5.append(_fact(
                "f_consensus_rev_3m_fy1_pct", "FY1 共識近 3 個月修正", pct,
                "{0} → {1}".format(prior90.get("date"), latest.get("date")), "%",
                "FY1 共識 EPS {0} → {1}（Koyfin 快照，約 90 天間距）；投影成 "
                "decision_inputs.consensus_rev_3m_pct".format(prior90.get("fy1"), latest.get("fy1")),
                "estimate",
                _src("evidence_numbers",
                     "numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1",
                     as_of=latest.get("date"), citation=latest.get("file")),
            ))

    vh = numbers.get("valuation_history") or {}
    trailing = vh.get("trailing") or {}
    for key, label in (("pe", "Trailing P/E"), ("ps", "P/S"), ("ev_s", "EV/S")):
        node = trailing.get(key) or {}
        if node.get("current") is None:
            continue
        q5.append(_fact(
            f"f_{key}_current", f"{label}（現值）", node.get("current"), as_of, "x",
            "{0} 個年度端點內的分位＝{1}".format(
                node.get("n_points"), node.get("current_percentile_within_annual_points")),
            "realized",
            _src("evidence_numbers", f"numbers.valuation_history.trailing.{key}",
                 as_of=as_of, citation=vh.get("method")),
        ))
        if node.get("current_percentile_within_annual_points") is not None:
            q5.append(_fact(
                f"f_{key}_percentile", f"{label} 年度端點分位",
                node.get("current_percentile_within_annual_points"), as_of, "%",
                "**非五年分位**：只用 {0} 個年度端點，valuation.percentile_5y 另有口徑".format(
                    node.get("n_points")),
                "realized",
                _src("evidence_numbers",
                     f"numbers.valuation_history.trailing.{key}.current_percentile_within_annual_points",
                     as_of=as_of),
            ))
    points = ((vh.get("fwd_recent_window") or {}).get("points")) or []
    if points:
        last = points[-1]
        q5.append(_fact(
            "f_fwd_pe_latest", "Forward P/E（最近快照）", last.get("fwd_pe"),
            last.get("snapshot_date"), "x",
            "分母＝FY1 EPS {0}，分子＝快照價 {1}".format(last.get("fy1_eps"), last.get("price_used")),
            "realized",
            _src("evidence_numbers",
                 "numbers.valuation_history.fwd_recent_window.points[-1]",
                 as_of=last.get("snapshot_date")),
        ))


def _peer_facts(numbers, buckets):
    peers = numbers.get("peer_financials") or {}
    for name, node in peers.items():
        if not isinstance(node, dict):
            continue
        for key, label, unit in (
            ("gross_margin_pct", "毛利率", "%"),
            ("operating_margin_pct", "營業利益率", "%"),
            ("fcf_margin_pct", "FCF 利潤率", "%"),
        ):
            if node.get(key) is None:
                continue
            buckets["q2_moat"]["facts"].append(_fact(
                "f_peer_{0}_{1}".format(_slug(name), key), f"{name} {label}",
                node.get(key), node.get("fiscal_period_as_of"), unit,
                node.get("source") or "evidence.numbers.peer_financials",
                "realized",
                _src("evidence_numbers", f"numbers.peer_financials.{name}.{key}",
                     as_of=node.get("fiscal_period_as_of")),
                note=node.get("note"),
            ))


# ---------------------------------------------------------------------------
# 2026-09-11（WP-H2-1）：同業對照表搬到事實層。判斷者不再抄同業數字，只寫
# strategy_note（對手為何無力／有力發動價格戰）與四檢查點燈號；本區塊的
# metrics／rows 由 dd_project.py 投影成舊形狀的 moat.spread_table（度量為列）
# 與 moat.competitors（對手為列）。度量 key 直接沿用 evidence 的欄名，不改名。
# ---------------------------------------------------------------------------

PEER_METRICS = (
    ("gross_margin_pct", "毛利率", "%"),
    ("operating_margin_pct", "營業利益率", "%"),
    ("fcf_margin_pct", "FCF 利潤率", "%"),
    ("rd_intensity_pct", "研發密度", "%"),
)


def build_peer_comparison(numbers, subject=None) -> dict:
    """evidence.numbers.peer_financials → facts.peer_comparison。

    只搬數字、期間、口徑、來源；一個判讀字都不加。某度量整欄皆 null（例：
    多數非軟體業者不單獨揭露研發）就整個 metric 不列，避免表上出現一整欄空白
    假裝有對照。沒有 peer_financials 時回空 dict（呼叫端不寫這個鍵）。"""
    peers = numbers.get("peer_financials") or {}
    rows = []
    for name, node in peers.items():
        if not isinstance(node, dict):
            continue
        values = {k: node.get(k) for k, _label, _unit in PEER_METRICS}
        row = {
            "name": name,
            "period": node.get("fiscal_period_as_of"),
            "basis": node.get("source") or "evidence.numbers.peer_financials",
            "values": values,
            "source": _src("evidence_numbers", "numbers.peer_financials.{0}".format(name),
                           as_of=node.get("fiscal_period_as_of")),
        }
        if subject and name == subject:
            row["is_subject"] = True
        if node.get("note"):
            row["note"] = node.get("note")
        rows.append(row)
    if not rows:
        return {}
    metrics = []
    for key, label, unit in PEER_METRICS:
        if all(r["values"].get(key) is None for r in rows):
            continue
        metrics.append({"key": key, "label": label, "unit": unit})
    if not metrics:
        return {}
    out = {"metrics": metrics, "rows": rows}
    if subject:
        out["subject"] = subject
    return out


def _recency_fact(numbers, buckets):
    rec = numbers.get("earnings_recency") or {}
    if rec.get("last_earnings_date"):
        buckets["q1_business"]["facts"].append(_fact(
            "f_earnings_recency", "最近一次財報日", rec.get("last_earnings_date"),
            rec.get("last_earnings_date"), "date",
            "距今 {0} 個交易日".format(rec.get("trading_days_since")), "realized",
            _src("evidence_numbers", "numbers.earnings_recency",
                 as_of=rec.get("last_earnings_date")),
        ))


# ---------------------------------------------------------------------------
# coverage／events → findings_digest（不按方向裁掉）
# ---------------------------------------------------------------------------

def build_findings_digest(evidence) -> list:
    """逐條抄 coverage／events 的 findings；查無料的軸（status=none／
    not_applicable 且無 findings）也各留一條 status 條目，讓缺口看得見。
    id 的算法與 validate_judgment.j1_traceability_checks 相同（無 id 時
    `{axis}#{index}`），兩邊對得上才能逐條追溯。"""
    out = []
    for section in ("coverage", "events"):
        block = evidence.get(section) or {}
        for axis, v in block.items():
            if not isinstance(v, dict):
                continue
            findings = v.get("findings") or []
            if not findings:
                out.append({
                    "id": f"{axis}#none",
                    "axis": axis,
                    "section": section,
                    "direction": None,
                    "claim": None,
                    "status": "none" if v.get("status") in ("none", None) else "gap",
                    "source": None,
                    "as_of": None,
                })
                continue
            for i, f in enumerate(findings):
                if not isinstance(f, dict):
                    continue
                out.append({
                    "id": f.get("id") or f"{axis}#{i}",
                    "axis": axis,
                    "section": section,
                    "direction": f.get("direction"),
                    "claim": f.get("claim"),
                    "source": f.get("source"),
                    "as_of": f.get("as_of"),
                    "affects": f.get("affects") or [],
                    "status": "ok",
                })
    return out


def extract(evidence, digest=None, evidence_ref=None, digest_ref=None, date=None) -> dict:
    numbers = evidence.get("numbers") or {}
    buckets = {
        k: {"label": QUESTION_LABELS[k], "facts": []} for k in QUESTION_KEYS
    }
    _kpi_facts(numbers, buckets)
    _valuation_facts(numbers, buckets)
    _peer_facts(numbers, buckets)
    _recency_fact(numbers, buckets)

    for k in QUESTION_KEYS:
        note = NEEDS_SONNET_NOTE[k]
        buckets[k]["needs_sonnet"] = True
        buckets[k]["needs_sonnet_note"] = note

    facts = {
        "meta": {
            "ticker": evidence.get("ticker"),
            "date": _norm_date(date or evidence.get("date")),
            "schema": "facts-v1",
            "generator": "dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）",
            "evidence_ref": evidence_ref,
            "digest_ref": digest_ref,
        },
        "questions": buckets,
        "findings_digest": build_findings_digest(evidence),
        "gaps": [],
    }
    # 2026-09-11（WP-H2-1）：同業對照表——判斷者不再抄數字。
    peer_comparison = build_peer_comparison(numbers, subject=evidence.get("ticker"))
    if peer_comparison:
        facts["peer_comparison"] = peer_comparison
        missing = [k for k, label, _u in PEER_METRICS
                   if k not in {m["key"] for m in peer_comparison["metrics"]}]
        if missing:
            facts["gaps"].append({
                "topic": "同業對照缺度量：{0}".format("、".join(missing)),
                "question": "q2_moat",
                "why": "evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），"
                       "事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。",
                "tried": ["evidence.numbers.peer_financials"],
            })
    else:
        facts["gaps"].append({
            "topic": "同業對照表",
            "question": "q2_moat",
            "why": "evidence.numbers.peer_financials 無資料，護城河同業數字整張缺——"
                   "事實表 agent 須補，補不到時判斷者要在 moat.peer_na_reason 說明為何沒有可比同業。",
            "tried": ["evidence.numbers.peer_financials"],
        })
    if digest:
        flags = digest.get("qa_flags") or []
        if flags:
            facts["gaps"].append({
                "topic": "法說問答未正面回答項",
                "question": "q6_how_wrong",
                "why": "digest.qa_flags 有 {0} 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口".format(len(flags)),
                "tried": ["digest.qa_flags"],
            })
    return facts


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------

def _expand_refs(node, root, depth=0):
    """把 `{"$ref": "#/definitions/X"}` 就地展開——`validate_judgment` 的
    schema 子集直譯器不支援 `$ref`／`definitions`，但 facts schema 用
    definitions 才不會把 fact 形狀抄六遍。定義之間無循環（fact → source 為
    止），depth 上限只是防呆。"""
    if depth > 10:
        return node
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/definitions/"):
            target = (root.get("definitions") or {}).get(ref.split("/")[-1])
            return _expand_refs(target, root, depth + 1) if target else {}
        return {k: _expand_refs(v, root, depth + 1) for k, v in node.items()}
    if isinstance(node, list):
        return [_expand_refs(v, root, depth + 1) for v in node]
    return node


def check(data: dict) -> tuple:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    expanded = _expand_refs(schema, schema)
    expanded.pop("definitions", None)
    fails = vj.schema_validate(data, expanded, "$")
    warns = []

    seen = {}
    for qk, q in (data.get("questions") or {}).items():
        for f in (q or {}).get("facts") or []:
            if not isinstance(f, dict):
                continue
            fid = f.get("id")
            if fid in seen:
                fails.append(f"fact id 重複：{fid}（{seen[fid]} 與 {qk}）")
            else:
                seen[fid] = qk
            if f.get("value") is None and not f.get("needs_sonnet"):
                fails.append(
                    f"$.questions.{qk}: fact {fid} 的 value 為 null 卻未標 needs_sonnet"
                    f"（抽不到要標記，不得留空假裝完整）"
                )
            src = f.get("source") or {}
            if src.get("type") == "transcript" and not src.get("locator"):
                warns.append(f"fact {fid} 來源是逐字稿但缺 locator（段落定位），閘無法核對原文")
    if not data.get("findings_digest"):
        warns.append("findings_digest 為空——evidence 逐條 finding 未帶入，判斷層看不到來源衝突與缺口")
    return fails, warns


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def cmd_extract(args) -> int:
    if args.run_dir:
        run_dir = Path(args.run_dir)
        evidence_path = run_dir / "evidence.json"
        digest_path = run_dir / "digest.json"
    else:
        if not args.evidence:
            print("extract：需要 --run-dir 或 --evidence", file=sys.stderr)
            return 2
        evidence_path = Path(args.evidence)
        digest_path = Path(args.digest) if args.digest else None
    if not evidence_path.exists():
        print(f"✗ 找不到 evidence：{evidence_path}", file=sys.stderr)
        return 1
    evidence = _load(evidence_path)
    digest = _load(digest_path) if (digest_path and digest_path.exists()) else None
    facts = extract(
        evidence, digest,
        date=args.date,
        evidence_ref=str(evidence_path),
        digest_ref=str(digest_path) if (digest_path and digest_path.exists()) else None,
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n_facts = sum(len(q["facts"]) for q in facts["questions"].values())
    print("寫入 {0}（{1} 條機械事實／{2} 條 findings_digest；六題全標 needs_sonnet，待事實表 agent 補）".format(
        out_path, n_facts, len(facts["findings_digest"])))
    return 0


def cmd_check(args) -> int:
    data = _load(args.file)
    fails, warns = check(data)
    tag = "FAIL" if fails else "PASS"
    print(f"[{tag}] {Path(args.file).name}（{len(fails)} FAIL／{len(warns)} WARN）")
    for f in fails:
        print(f"  ✗ {f}")
    for w in warns:
        print(f"  ⚠ {w}")
    if fails and not args.report:
        return 1
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ex = sub.add_parser("extract", help="從 evidence.json 抽機械可抽的事實")
    p_ex.add_argument("--run-dir", help=".dd_build/runs/{T}_{D}/ 目錄")
    p_ex.add_argument("--evidence", help="evidence.json 路徑（無 --run-dir 時必填）")
    p_ex.add_argument("--digest", help="digest.json 路徑（選填）")
    p_ex.add_argument("--date", help="判斷日（YYYY-MM-DD）；預設取 evidence.date，證據包沿用舊日期時用此旗標對齊判斷檔")
    p_ex.add_argument("--out", required=True, help="輸出 facts.json 路徑")
    p_ex.set_defaults(func=cmd_extract)

    p_ck = sub.add_parser("check", help="驗 facts.json")
    p_ck.add_argument("file", help="facts.json 路徑")
    p_ck.add_argument("--report", action="store_true", help="永遠 exit 0，只印報告")
    p_ck.set_defaults(func=cmd_check)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
