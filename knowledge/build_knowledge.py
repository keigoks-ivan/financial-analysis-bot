#!/usr/bin/env python3
"""
build_knowledge.py — 從現有 dd-meta / id-meta 回填知識層（Phase 0）。

掃 docs/dd/DD_*.html + docs/id/ID_*.html，產出：
  - decisions.jsonl  (DERIVED, gitignored)：每份 DD = 一筆決策事件，並合併 ledger.manual.jsonl
  - graph.json       (DERIVED, gitignored)：實體圖（公司 / 產業 / 主題節點 + 關係邊）

真相來源 = 已 commit 的 DD/ID HTML + ledger.manual.jsonl（人工 outcome / 非 DD 決策）。
本檔產物可隨時重建，故 gitignore；跨機只同步真相、不同步衍生物 → 零 git 衝突。

用法：python knowledge/build_knowledge.py
"""
import re
import json
import glob
import os
from pathlib import Path
from datetime import datetime, date

REPO = Path(__file__).resolve().parent.parent          # financial-analysis-bot/
KDIR = Path(__file__).resolve().parent                 # knowledge/
DD_GLOB = str(REPO / "docs" / "dd" / "DD_*.html")
ID_GLOB = str(REPO / "docs" / "id" / "ID_*.html")

DECISIONS_OUT = KDIR / "decisions.jsonl"
GRAPH_OUT = KDIR / "graph.json"
MANUAL_IN = KDIR / "ledger.manual.jsonl"

# canonical 解析器：與 scripts/update_dd_index.py 同一條 regex（read-before-write 確認過）
DD_META_RE = re.compile(r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL)
ID_META_RE = re.compile(r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL)

# 新鮮度門檻（天）
FRESH_DAYS = 90
AGING_DAYS = 180


def _rel(path):
    return os.path.relpath(str(path), str(REPO))


def _extract(path, regex):
    try:
        t = Path(path).read_text(encoding="utf-8")
    except Exception:
        return None
    m = regex.search(t)
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None


def _date_from_name(path):
    # DD_TICKER_YYYYMMDD.html → 2026-05-22
    m = re.search(r"_(\d{8})\.html$", os.path.basename(path))
    if not m:
        return None
    s = m.group(1)
    return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"


def _freshness(d):
    if not d:
        return "unknown"
    try:
        dd = datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return "unknown"
    age = (date.today() - dd).days
    if age <= FRESH_DAYS:
        return "fresh"
    if age <= AGING_DAYS:
        return "aging"
    return "stale"


def _read_manual():
    """讀 ledger.manual.jsonl（真相）：略過 # 註解行與空行。"""
    decisions, outcomes = [], {}
    if not MANUAL_IN.exists():
        return decisions, outcomes
    for line in MANUAL_IN.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        try:
            rec = json.loads(s)
        except json.JSONDecodeError:
            print(f"  WARN: ledger.manual.jsonl 無法解析: {s[:80]}")
            continue
        if rec.get("kind") == "outcome" and rec.get("decision_id"):
            outcomes[rec["decision_id"]] = rec
        else:
            rec.setdefault("kind", "decision")
            rec.setdefault("source", "manual")
            decisions.append(rec)
    return decisions, outcomes


def build_decisions(manual_decisions, outcomes):
    rows = []
    for f in sorted(glob.glob(DD_GLOB)):
        meta = _extract(f, DD_META_RE)
        if not meta:
            continue
        ticker = meta.get("ticker") or os.path.basename(f).split("_")[1]
        d = meta.get("date") or _date_from_name(f)
        expected = {k: meta.get(k) for k in
                    ("irr_base_pct", "ev5y_pct", "max_dd_pct", "upside_5y_pct")
                    if meta.get(k) is not None}
        rows.append({
            "id": f"{ticker}-{(d or '').replace('-', '')}",
            "kind": "decision",
            "date": d,
            "entity": ticker,
            "entity_type": "company",
            "verdict": meta.get("dca_verdict"),              # 進場/觀望/迴避（v13+；舊版可能 None）
            "fundamental_grade": meta.get("verdict") or meta.get("signal"),  # A+/A/B/C/X
            "conviction": meta.get("long_term_confidence"),
            "role": meta.get("dca_role"),
            "price_at_decision": meta.get("price_at_dd"),
            "thesis_one_line": meta.get("oneliner"),
            "moat_trend": meta.get("moat_trend"),
            "expected": expected,
            "schema": meta.get("schema"),
            "source_report": _rel(f),
            "source": "dd-meta",
            "outcome": None,
        })

    rows.extend(manual_decisions)

    # 掛上人工 outcome（真相）
    for r in rows:
        if r.get("id") in outcomes:
            r["outcome"] = outcomes[r["id"]]
    return rows


def build_graph(decisions, id_metas):
    nodes = {}
    edges = []

    # 公司節點：canonical = 每個 ticker 最新一筆決策
    latest = {}
    for d in decisions:
        if d.get("entity_type") != "company":
            continue
        t = d["entity"]
        if t not in latest or (d.get("date") or "") > (latest[t].get("date") or ""):
            latest[t] = d
    for t, d in latest.items():
        nodes[t] = {
            "id": t,
            "type": "company",
            "canonical": {
                "verdict": d.get("verdict"),
                "fundamental_grade": d.get("fundamental_grade"),
                "date": d.get("date"),
                "freshness": _freshness(d.get("date")),
                "source": d.get("source_report"),
            },
        }

    # 產業/主題節點 + 邊（來自 id-meta related_tickers）
    seen_theme = {}  # theme -> publish_date（去重取最新）
    for meta, path in id_metas:
        theme = meta.get("theme")
        if not theme:
            continue
        pub = meta.get("publish_date") or _date_from_name(path) or ""
        if theme in seen_theme and pub <= seen_theme[theme]:
            continue
        seen_theme[theme] = pub
        nodes[theme] = {
            "id": theme,
            "type": "industry",
            "thesis_type": meta.get("thesis_type"),
            "oneliner": meta.get("oneliner"),
            "action": meta.get("action"),
            "publish_date": pub,
            "freshness": _freshness(pub),
            "source": _rel(path),
        }
        for rt in meta.get("related_tickers", []):
            tk = rt.get("ticker")
            if not tk:
                continue
            nodes.setdefault(tk, {"id": tk, "type": "company"})  # 可能尚無 DD
            edges.append({
                "from": tk,
                "to": theme,
                "rel": "belongs_to",
                "beneficiary": rt.get("beneficiary"),
                "depth": rt.get("depth"),
            })

    return {
        "generated": date.today().isoformat(),
        "nodes": list(nodes.values()),
        "edges": edges,
    }


def main():
    manual_decisions, outcomes = _read_manual()

    decisions = build_decisions(manual_decisions, outcomes)
    DECISIONS_OUT.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in decisions) + "\n",
        encoding="utf-8",
    )

    id_metas = []
    for f in sorted(glob.glob(ID_GLOB)):
        meta = _extract(f, ID_META_RE)
        if meta:
            id_metas.append((meta, f))

    graph = build_graph(decisions, id_metas)
    GRAPH_OUT.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    # 摘要
    n_verdict = sum(1 for d in decisions if d.get("verdict"))
    n_outcome = sum(1 for d in decisions if d.get("outcome"))
    companies = [n for n in graph["nodes"] if n["type"] == "company"]
    industries = [n for n in graph["nodes"] if n["type"] == "industry"]
    print(f"✅ decisions.jsonl  : {len(decisions)} 筆決策"
          f"（{n_verdict} 有 dca_verdict、{n_outcome} 有 outcome、"
          f"{len(manual_decisions)} 人工）")
    print(f"✅ graph.json       : {len(companies)} 公司節點 / "
          f"{len(industries)} 產業節點 / {len(graph['edges'])} 條邊")


if __name__ == "__main__":
    main()
