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
SC_DIR = REPO / "docs" / "supply-chain" / "data"

DECISIONS_OUT = KDIR / "decisions.jsonl"
GRAPH_OUT = KDIR / "graph.json"
MANUAL_IN = KDIR / "ledger.manual.jsonl"

# canonical 解析器：與 scripts/update_dd_index.py 同一條 regex（read-before-write 確認過）
DD_META_RE = re.compile(r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL)
ID_META_RE = re.compile(r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL)

# 新鮮度門檻（天）
FRESH_DAYS = 90
AGING_DAYS = 180

# 同一家公司的多重掛牌 → 正規化到主 ticker（取有最新/v13 DD 的那邊為主）。
# 注意：價格幣別不同（ADR USD vs 當地幣），合併後決策史會混幣，看 thesis 文字區分。可持續擴充。
ALIASES = {
    "2330.TW": "TSM",   # 台積電：v13 DD 在 ADR
    "GOOG": "GOOGL",     # Alphabet：DD 在 GOOGL
}


def canon_ticker(t):
    return ALIASES.get(t, t)


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
    decisions, outcomes, event_outcomes = [], {}, []
    if not MANUAL_IN.exists():
        return decisions, outcomes, event_outcomes
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
        elif rec.get("kind") == "event_outcome":
            # T-minus 鏈事件複盤（財報/催化劑 vs 凍結快照），錨是 snapshot JSON，
            # 不走價格結算（settle 只吃 kind=decision）、不進 calibration 裁決統計。
            rec.setdefault("source", "manual")
            rec.setdefault("entity_type", "event")
            event_outcomes.append(rec)
        else:
            rec.setdefault("kind", "decision")
            rec.setdefault("source", "manual")
            decisions.append(rec)
    return decisions, outcomes, event_outcomes


def _load_sc_topics():
    """讀 active 的 supply-chain topic JSON（topics.json manifest 的 active 決定）。"""
    out = []
    manifest = SC_DIR / "topics.json"
    if not manifest.exists():
        return out
    try:
        topics = json.loads(manifest.read_text(encoding="utf-8")).get("topics", [])
    except json.JSONDecodeError:
        return out
    for t in topics:
        if not t.get("active"):
            continue
        p = SC_DIR / f"{t.get('id')}.json"
        if not p.exists():
            continue
        try:
            out.append((json.loads(p.read_text(encoding="utf-8")), p))
        except json.JSONDecodeError:
            print(f"  WARN: supply-chain JSON parse error: {p.name}")
    return out


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
            # signal 才是乾淨評級（A+/A/B/C/X）；v12 的 verdict 欄是 stance 長文，故 signal 優先
            "fundamental_grade": meta.get("signal") or meta.get("verdict"),
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


def build_graph(decisions, id_metas, sc_topics):
    nodes = {}
    edges = []

    # 公司節點：canonical = 每個（正規化後）ticker 最新一筆決策；多重掛牌合併
    latest = {}
    for d in decisions:
        if d.get("entity_type") != "company":
            continue
        t = canon_ticker(d["entity"])
        if t not in latest or (d.get("date") or "") > (latest[t].get("date") or ""):
            latest[t] = d
    for t, d in latest.items():
        node = {
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
        members = sorted({a for a, c in ALIASES.items() if c == t})
        if members:
            node["aliases"] = [t] + members
        nodes[t] = node

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
            # v2.5/v2.6 趨勢結構化欄位（QC-52 DD↔ID 對帳消費;legacy ID 無值＝None）
            "sd_verdict": meta.get("sd_verdict"),
            "clock_phase": meta.get("clock_phase"),
            "conviction": meta.get("conviction"),
            "priced_in": meta.get("priced_in"),
            "publish_date": pub,
            "freshness": _freshness(pub),
            "source": _rel(path),
        }
        for rt in meta.get("related_tickers", []):
            tk = rt.get("ticker")
            if not tk:
                continue
            tk = canon_ticker(tk)
            nodes.setdefault(tk, {"id": tk, "type": "company"})  # 可能尚無 DD
            edges.append({
                "from": tk,
                "to": theme,
                "rel": "belongs_to",
                "beneficiary": rt.get("beneficiary"),
                "depth": rt.get("depth"),
            })

    # 供應鏈 topic 節點 + 邊（來自 docs/supply-chain/data/<topic>.json，僅 active）
    for topic, path in sc_topics:
        tid = topic.get("id")
        if not tid:
            continue
        nodes[tid] = {
            "id": tid,
            "type": "supplychain",
            "title": topic.get("title"),
            "tab": topic.get("tab"),
            "source": _rel(path),
        }
        seen_pair = set()
        for nd in topic.get("nodes", []):
            proc = nd.get("name")
            comp = nd.get("competition")
            for co in nd.get("companies", []):
                raw = (co.get("ticker") or "").strip()
                if not raw:
                    continue
                # 一格可能併多個 ticker（"MRVL / GOOGL"）；拆開、濾掉未上市佔位（—）
                for tk in re.split(r"[/,、]", raw):
                    tk = tk.strip()
                    if not tk or tk in {"—", "-", "–", "N/A", "n/a", "未上市"}:
                        continue
                    tk = canon_ticker(tk)
                    key = (tk, proc)
                    if key in seen_pair:
                        continue
                    seen_pair.add(key)
                    nodes.setdefault(tk, {"id": tk, "type": "company"})
                    edges.append({
                        "from": tk,
                        "to": tid,
                        "rel": "supplies",
                        "node": proc,
                        "competition": comp,
                        "country": co.get("country"),
                    })

    return {
        "generated": date.today().isoformat(),
        "aliases": ALIASES,
        "nodes": list(nodes.values()),
        "edges": edges,
    }


def main():
    manual_decisions, outcomes, event_outcomes = _read_manual()

    decisions = build_decisions(manual_decisions, outcomes)
    DECISIONS_OUT.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False)
                  for r in decisions + event_outcomes) + "\n",
        encoding="utf-8",
    )

    id_metas = []
    for f in sorted(glob.glob(ID_GLOB)):
        meta = _extract(f, ID_META_RE)
        if meta:
            id_metas.append((meta, f))

    sc_topics = _load_sc_topics()
    graph = build_graph(decisions, id_metas, sc_topics)
    GRAPH_OUT.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    # 摘要
    n_verdict = sum(1 for d in decisions if d.get("verdict"))
    n_outcome = sum(1 for d in decisions if d.get("outcome"))
    companies = [n for n in graph["nodes"] if n["type"] == "company"]
    industries = [n for n in graph["nodes"] if n["type"] == "industry"]
    sc_nodes = [n for n in graph["nodes"] if n["type"] == "supplychain"]
    sc_edges = [e for e in graph["edges"] if e.get("rel") == "supplies"]
    print(f"✅ decisions.jsonl  : {len(decisions)} 筆決策"
          f"（{n_verdict} 有 dca_verdict、{n_outcome} 有 outcome、"
          f"{len(manual_decisions)} 人工、{len(event_outcomes)} 事件複盤）")
    print(f"✅ graph.json       : {len(companies)} 公司 / {len(industries)} 產業 / "
          f"{len(sc_nodes)} 供應鏈 topic / {len(graph['edges'])} 邊（含 {len(sc_edges)} supplies）")


if __name__ == "__main__":
    main()
