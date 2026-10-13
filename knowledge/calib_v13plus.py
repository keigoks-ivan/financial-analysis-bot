#!/usr/bin/env python3
"""calib_v13plus.py — v13+ DD 裁決校準表（讀 settlement_excess.json，印 markdown）。n<10 標「樣本太薄」。"""
import json, statistics as st, sys
from pathlib import Path
from collections import defaultdict
K = Path(__file__).resolve().parent
rows = json.loads((K / "settlement_excess.json").read_text())["rows"]
for _r in rows:  # td28＝至今且裁決齡 >=28 天（README 讀數紀律）；其餘 to-date 太新不入統計
    _r["td28"] = _r["td"] if _r["days"] >= 28 else None
ORDER = ["進場", "觀望", "迴避"]

def stat(vals):
    if not vals: return "—"
    ex = [v["ex_bps"] for v in vals]; ab = [v["abs_bps"] for v in vals]
    hit = sum(1 for e in ex if e > 0)
    big_up = sum(1 for e in ex if e >= 2000); big_dn = sum(1 for e in ex if e <= -2000)  # 整數 bps
    flag = " ⚠n<10" if len(vals) < 10 else ""
    return (f"n={len(vals)}{flag}｜超額中位 {st.median(ex)/100:+.1f}%｜均 {sum(ex)/len(ex)/100:+.1f}%｜"
            f"跑贏 {hit}/{len(ex)}｜超額>=+20% {big_up}／<=-20% {big_dn}｜絕對中位 {st.median(ab)/100:+.1f}%")

def table(keyf, hz, subset=None, title=""):
    g = defaultdict(list)
    for r in (subset if subset is not None else rows):
        v = r.get(hz)
        if v is not None: g[keyf(r)].append(v)
    print(f"\n### {title}（{hz}）")
    for k in sorted(g, key=lambda x: (ORDER.index(x[0]) if isinstance(x, tuple) and x[0] in ORDER else 9, str(x))):
        print(f"- {k}：{stat(g[k])}")

def dedup(rs):
    seen, out = set(), []
    for r in sorted(rs, key=lambda r: r["date"]):
        if r["entity"] in seen: continue
        seen.add(r["entity"]); out.append(r)
    return out

for name, sub in (("全部（含同檔重複裁決）", rows), ("去重（每檔首次裁決）", dedup(rows))):
    print(f"\n## {name}  總 {len(sub)} 筆")
    for hz in ("h91", "h182", "td28"):
        table(lambda r: r["verdict"], hz, sub, "依裁決")
    table(lambda r: (r["verdict"], r["gen"]), "h91", sub, "裁決×世代")
    table(lambda r: (r["verdict"], r["gen"]), "td28", sub, "裁決×世代 to-date")
    table(lambda r: (r["verdict"], r["role"]), "h91", sub, "裁決×角色")
    table(lambda r: (r["verdict"], r["role"]), "td28", sub, "裁決×角色 to-date")
    table(lambda r: (r["verdict"], r["bench"]), "h91", sub, "裁決×市場基準")
    table(lambda r: (r["verdict"], r["grade"]), "h91", sub, "裁決×基本面評級")

    import random
    random.seed(7)
    for hz in ("h91", "td28"):
        a = [r[hz]["ex_bps"] for r in sub if r[hz] and r["verdict"] == "進場"]
        b = [r[hz]["ex_bps"] for r in sub if r[hz] and r["verdict"] == "觀望"]
        if len(a) >= 5 and len(b) >= 5:
            ds = sorted(st.median(random.choices(a, k=len(a))) - st.median(random.choices(b, k=len(b))) for _ in range(5000))
            print(f"\n進場−觀望 超額中位差（{hz}）：{(st.median(a)-st.median(b))/100:+.1f}pp，bootstrap 90% 區間 [{ds[250]/100:+.1f}, {ds[4750]/100:+.1f}]pp（n={len(a)}/{len(b)}）")
