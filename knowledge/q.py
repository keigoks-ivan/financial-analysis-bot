#!/usr/bin/env python3
"""
q.py — 知識層查詢介面（Phase 1，服務 a：自我導航）。

  python knowledge/q.py NVDA          # 某 entity 的全部決策史 + canonical + 圖譜鄰居
  python knowledge/q.py --stale [N]   # canonical view 超過 N 天（預設 180）的公司
  python knowledge/q.py --theme CoWoS # 含關鍵字的產業節點 + 成員 ticker 現裁決
  python knowledge/q.py --verdicts    # 全公司「最新裁決」分布
  python knowledge/q.py --calibration # 命中率 / 校準（需 outcome）；無 outcome 則給覆蓋報告
  python knowledge/q.py --rebuild     # 重建 decisions.jsonl + graph.json

decisions.jsonl / graph.json 不存在時會自動先 rebuild（衍生物，每台機本地重建）。
"""
import sys
import json
import subprocess
from pathlib import Path
from collections import Counter, defaultdict

KDIR = Path(__file__).resolve().parent
DECISIONS = KDIR / "decisions.jsonl"
GRAPH = KDIR / "graph.json"
BUILD = KDIR / "build_knowledge.py"


def _rebuild():
    subprocess.run([sys.executable, str(BUILD)], check=True)


def _load():
    if not DECISIONS.exists() or not GRAPH.exists():
        print("（衍生物不存在，先重建…）")
        _rebuild()
    decisions = [json.loads(l) for l in DECISIONS.read_text(encoding="utf-8").splitlines() if l.strip()]
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    return decisions, graph


def _node(graph, nid):
    for n in graph["nodes"]:
        if n["id"] == nid:
            return n
    return None


def cmd_entity(name):
    decisions, graph = _load()
    name = name.upper()
    aliases = graph.get("aliases", {})
    canonical = aliases.get(name, name)
    members = {canonical} | {a for a, c in aliases.items() if c == canonical}

    mine = sorted([d for d in decisions if (d.get("entity") or "").upper() in members],
                  key=lambda d: d.get("date") or "")
    node = _node(graph, canonical)

    if not mine and not node:
        print(f"找不到 {name}（沒有 DD、也不在任何 ID 的 related_tickers）")
        return

    alias_note = f"  (含別名: {', '.join(sorted(members - {canonical}))})" if len(members) > 1 else ""
    if node and node.get("canonical"):
        c = node["canonical"]
        print(f"━━ {canonical} ━━{alias_note}  現裁決: {c.get('verdict') or '—'}  "
              f"(基本面 {c.get('fundamental_grade') or '—'}, {c.get('date') or '—'}, {c.get('freshness')})")
    else:
        print(f"━━ {canonical} ━━{alias_note}  （無 DD，只在產業圖中被引用）")

    if mine:
        print(f"\n決策史（{len(mine)} 筆）：")
        for d in mine:
            exp = d.get("expected") or {}
            irr = exp.get("irr_base_pct")
            ev = exp.get("ev5y_pct")
            tag = f" IRR~{irr}%/5Y EV~{ev}%" if (irr is not None or ev is not None) else ""
            px = d.get("price_at_decision")
            print(f"  {d.get('date') or '????-??-??'}  [{d.get('verdict') or '—'}]"
                  f"  ${px if px is not None else '—'}{tag}")
            if d.get("thesis_one_line"):
                print(f"      {d['thesis_one_line']}")
            if d.get("outcome"):
                o = d["outcome"]
                print(f"      ▸ OUTCOME {o.get('reviewed_date','')}: "
                      f"realized {o.get('realized_return_pct','?')}%  held={o.get('verdict_held')}  "
                      f"{o.get('lesson','')}")

    # 圖譜鄰居：此 ticker 屬於哪些產業/主題（belongs_to）
    themes = sorted({e["to"] for e in graph["edges"]
                     if e["from"] == canonical and e.get("rel") == "belongs_to"})
    if themes:
        print(f"\n所屬產業/主題（{len(themes)}）：")
        for t in themes:
            print(f"  • {t}")

    # 供應鏈位置（supplies）：此 ticker 在哪些供應鏈 topic 的哪個製程節點
    supplies = sorted({(e["to"], e.get("node") or "") for e in graph["edges"]
                       if e["from"] == canonical and e.get("rel") == "supplies"})
    if supplies:
        print(f"\n供應鏈位置（{len(supplies)}）：")
        for tid, proc in supplies:
            print(f"  • {tid}: {proc}")


def cmd_stale(n):
    _, graph = _load()
    rows = [nd for nd in graph["nodes"]
            if nd["type"] == "company" and nd.get("canonical")
            and nd["canonical"].get("freshness") in ("aging", "stale")]
    rows.sort(key=lambda nd: nd["canonical"].get("date") or "")
    print(f"需要重跑 DD 的公司（canonical 已 aging/stale，門檻見 build_knowledge.py）：{len(rows)} 檔\n")
    for nd in rows:
        c = nd["canonical"]
        print(f"  {c.get('date') or '????-??-??'}  {nd['id']:8s}  "
              f"{c.get('freshness'):6s}  裁決:{c.get('verdict') or '—'}")


def cmd_theme(kw):
    decisions, graph = _load()
    kw_l = kw.lower()
    hits = [nd for nd in graph["nodes"]
            if nd["type"] in ("industry", "supplychain")
            and (kw_l in (nd["id"] or "").lower() or kw_l in (nd.get("title") or "").lower())]
    if not hits:
        print(f"沒有產業/供應鏈節點含「{kw}」")
        return
    canon = {nd["id"]: nd.get("canonical", {}) for nd in graph["nodes"] if nd["type"] == "company"}
    for nd in hits:
        if nd["type"] == "supplychain":
            print(f"━━ {nd['id']} ━━  [供應鏈] {nd.get('title') or ''}")
            members = [e for e in graph["edges"]
                       if e["to"] == nd["id"] and e.get("rel") == "supplies"]
            print(f"  節點 × 廠商（{len(members)}）：")
            for e in sorted(members, key=lambda e: (e.get("node") or "", e["from"])):
                c = canon.get(e["from"], {})
                print(f"    {e['from']:8s}  {(e.get('node') or '')[:18]:18s}  "
                      f"裁決:{c.get('verdict') or '—':4s}  {c.get('freshness') or 'no-DD'}")
            print()
            continue
        print(f"━━ {nd['id']} ━━  ({nd.get('thesis_type') or '—'}, {nd.get('publish_date') or '—'}, {nd.get('freshness')})")
        if nd.get("oneliner"):
            print(f"  {nd['oneliner']}")
        if nd.get("action"):
            print(f"  ▸ action: {nd['action']}")
        members = [e for e in graph["edges"]
                   if e["to"] == nd["id"] and e.get("rel") == "belongs_to"]
        print(f"\n  成員 ticker（{len(members)}）：")
        for e in sorted(members, key=lambda e: e["from"]):
            c = canon.get(e["from"], {})
            print(f"    {e['from']:8s}  現裁決:{c.get('verdict') or '—':4s}  "
                  f"{c.get('freshness') or 'no-DD':7s}  depth:{e.get('depth') or '—'}")
        print()


def cmd_verdicts():
    _, graph = _load()
    cnt = Counter()
    for nd in graph["nodes"]:
        if nd["type"] == "company" and nd.get("canonical"):
            cnt[nd["canonical"].get("verdict") or "（無裁決/舊版）"] += 1
    print("全公司「最新裁決」分布：")
    for k, v in cnt.most_common():
        print(f"  {k:12s} {v}")


def cmd_calibration():
    decisions, _ = _load()
    with_o = [d for d in decisions if d.get("outcome")]
    print(f"決策總數 {len(decisions)}；有 outcome {len(with_o)}\n")
    if not with_o:
        print("尚無 outcome 回填。覆蓋現況：")
        v = Counter(d.get("verdict") or "（無裁決）" for d in decisions)
        for k, val in v.most_common():
            print(f"  {k:12s} {val}")
        print("\n→ 回填方式：在 knowledge/ledger.manual.jsonl 加一行 kind=outcome（見 README）。")
        return
    held = sum(1 for d in with_o if d["outcome"].get("verdict_held"))
    by_verdict = defaultdict(lambda: [0, 0])
    for d in with_o:
        b = by_verdict[d.get("verdict") or "—"]
        b[0] += 1
        b[1] += 1 if d["outcome"].get("verdict_held") else 0
    print(f"整體命中率：{held}/{len(with_o)} = {held/len(with_o)*100:.0f}%\n")
    print("依裁決別：")
    for k, (tot, ok) in by_verdict.items():
        print(f"  {k:8s} {ok}/{tot} = {ok/tot*100:.0f}%")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    a0 = args[0]
    if a0 == "--rebuild":
        _rebuild()
    elif a0 == "--stale":
        cmd_stale(int(args[1]) if len(args) > 1 else 180)
    elif a0 == "--theme":
        cmd_theme(args[1] if len(args) > 1 else "")
    elif a0 == "--verdicts":
        cmd_verdicts()
    elif a0 == "--calibration":
        cmd_calibration()
    elif a0.startswith("--"):
        print(__doc__)
    else:
        cmd_entity(a0)


if __name__ == "__main__":
    main()
