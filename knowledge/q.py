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
SETTLE = KDIR / "settlement.json"
SETTLE_BUILD = KDIR / "settle_outcomes.py"


def _rebuild():
    subprocess.run([sys.executable, str(BUILD)], check=True)


def _load_settlement():
    """機械結算（settle_outcomes.py 產出）。無檔、或比 decisions.jsonl／週線 cache 舊
    → 自動重跑（weekly cache 由 GitHub Actions 每週推、git pull 進來，pull 完首次查詢即重算）。
    回傳 ({decision_id: row}, as_of)；結算失敗回傳 ({}, None)（不擋其他查詢）。"""
    try:
        stale = not SETTLE.exists()
        if not stale:
            t = SETTLE.stat().st_mtime
            if DECISIONS.exists() and t < DECISIONS.stat().st_mtime:
                stale = True
            else:
                import os
                cache_dir = KDIR.parent / "data" / "weekly_cache"
                with os.scandir(cache_dir) as it:
                    stale = any(e.stat().st_mtime > t for e in it if e.name.endswith(".json"))
        if stale:
            subprocess.run([sys.executable, str(SETTLE_BUILD)], check=True)
        data = json.loads(SETTLE.read_text(encoding="utf-8"))
        return {r["id"]: r for r in data.get("rows", [])}, data.get("as_of")
    except Exception as e:  # cache 缺漏等，降級為無結算
        print(f"（結算不可用：{e}）")
        return {}, None


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
        settlement, _ = _load_settlement()
        print(f"\n決策史（{len(mine)} 筆）：")
        for d in mine:
            exp = d.get("expected") or {}
            irr = exp.get("irr_base_pct")
            ev = exp.get("ev5y_pct")
            tag = f" IRR~{irr}%/5Y EV~{ev}%" if (irr is not None or ev is not None) else ""
            px = d.get("price_at_decision")
            st = settlement.get(d.get("id"))
            sett = ""
            if st:
                mark = "⚠" if st.get("flags") else ""
                sett = f"  ▸結算 {st['to_date_pct']:+.1f}%/{st['days']}d{mark}"
            print(f"  {d.get('date') or '????-??-??'}  [{d.get('verdict') or '—'}]"
                  f"  ${px if px is not None else '—'}{tag}{sett}")
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


def _pct_table(title, buckets, order):
    """buckets: {label: [row, ...]}；每列印 n / 中位 / 平均 / 虧損比例（to-date），
    及 h91 到期樣本的中位。"""
    import statistics
    print(title)
    print(f"  {'':6s}{'n':>4}  {'中位%':>7}  {'平均%':>7}  {'虧損':>5}  {'h91中位%':>9}")
    for label in order:
        rows = buckets.get(label)
        if not rows:
            continue
        rets = [r["to_date_pct"] for r in rows]
        h91 = [r["h91"] for r in rows if r.get("h91") is not None]
        h91_s = f"{statistics.median(h91):>8.1f}" if h91 else f"{'—':>8}"
        print(f"  {label:6s}{len(rows):>4}  {statistics.median(rets):>7.1f}  "
              f"{statistics.mean(rets):>7.1f}  {sum(1 for x in rets if x < 0)/len(rets)*100:>4.0f}%  {h91_s}")
    print()


def cmd_calibration():
    decisions, _ = _load()
    settlement, as_of = _load_settlement()
    print(f"決策總數 {len(decisions)}；機械結算 {len(settlement)} 筆（價格 as_of {as_of}）\n")

    # ── 機械結算（settle_outcomes.py：weekly_cache 對答案）─────────────
    if settlement:
        MIN_DAYS = 28  # 太新鮮的裁決不進聚合（雜訊）
        rows = [r for r in settlement.values() if r["days"] >= MIN_DAYS]
        print(f"聚合樣本 = 結算齡 ≥ {MIN_DAYS} 天者 {len(rows)} 筆；報酬＝裁決日→as_of（各筆視窗不等長，方向可信、量級慎讀）\n")

        by_v = defaultdict(list)
        for r in rows:
            by_v[r["verdict"] or "（無裁決）"].append(r)
        _pct_table("依裁決（v13+ 才有；觀望/迴避的正報酬＝錯過成本）：",
                   by_v, ["進場", "觀望", "迴避", "（無裁決）"])

        by_g = defaultdict(list)
        for r in rows:
            by_g[r["grade"] or "—"].append(r)
        _pct_table("依基本面評級：", by_g, ["A+", "A", "B", "C", "X", "—"])

        # 錯過成本排行：說了觀望/迴避之後大漲的名字（觀望複審的觸發清單）。
        # 警報性質、非統計 → 不吃 MIN_DAYS 門檻，全樣本掃。
        missed = sorted((r for r in settlement.values()
                         if r["verdict"] in ("觀望", "迴避") and r["to_date_pct"] > 30),
                        key=lambda r: -r["to_date_pct"])
        if missed:
            print(f"⚠ 錯過成本 top（觀望/迴避後 > +30%，候選複審）：")
            for r in missed[:10]:
                print(f"  {r['entity']:8s} {r['date']}  [{r['verdict']}]  "
                      f"{r['to_date_pct']:+.0f}% / {r['days']}d")
            print()

    # ── 人工 outcome（ledger.manual.jsonl：verdict_held / lesson 是人的判斷）──
    with_o = [d for d in decisions if d.get("outcome")]
    if not with_o:
        print("人工 outcome 回填 0 筆（機械結算不取代人的複盤——lesson 仍要人寫）。")
        print("→ 回填方式：在 knowledge/ledger.manual.jsonl 加一行 kind=outcome（見 README）。")
        return
    held = sum(1 for d in with_o if d["outcome"].get("verdict_held"))
    by_verdict = defaultdict(lambda: [0, 0])
    for d in with_o:
        b = by_verdict[d.get("verdict") or "—"]
        b[0] += 1
        b[1] += 1 if d["outcome"].get("verdict_held") else 0
    print(f"人工 outcome 命中率：{held}/{len(with_o)} = {held/len(with_o)*100:.0f}%\n")
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
