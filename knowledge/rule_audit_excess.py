#!/usr/bin/env python3
"""
rule_audit_excess.py — 把 rule_audit.json 的規則觸發名單接上 settlement_excess.json（對基準超額）。
另對 DD 判斷類規則補幾個 rule_audit 沒有的結構化切面（估值燈×裁決、MA×進場、QC-49 翻面）。
先跑 settle_excess.py 與 rule_audit.py。印 markdown。n<10 標「樣本太薄」。成熟＝裁決齡>=28 天。
  python3.12 knowledge/rule_audit_excess.py
"""
import json, re, statistics as st, glob
from pathlib import Path
from collections import defaultdict
K = Path(__file__).resolve().parent; ROOT = K.parent
ex = {r["id"]: r for r in json.loads((K / "settlement_excess.json").read_text())["rows"]}
RA = json.loads((K / "rule_audit.json").read_text())

def fmt(vs, label=""):
    if not vs: return f"{label}n=0"
    e = [v for v in vs]; w = sum(1 for x in e if x > 0)
    f = " ⚠n<10" if len(e) < 10 else ""
    return f"{label}n={len(e)}{f}｜超額中位 {st.median(e)/100:+.1f}%｜均 {sum(e)/len(e)/100:+.1f}%｜跑贏 {w}/{len(e)}"

def td28(i):
    r = ex.get(i); return r["td"]["ex_bps"] if r and r["days"] >= 28 and r.get("td") else None
def h91(i):
    r = ex.get(i); return r["h91"]["ex_bps"] if r and r.get("h91") else None

print("## A. rule_audit 觸發名單 × 超額（只含 mechanical/partial）")
for r in RA["rules"]:
    if r["coverage"] == "manual": continue
    ids = [h["decision_id"] for h in r["hits"]]
    a = [td28(i) for i in ids]; a = [x for x in a if x is not None]
    b = [h91(i) for i in ids]; b = [x for x in b if x is not None]
    print(f"- {r['rule'][:40]}｜觸發 {len(ids)}｜td28 {fmt(a)}｜h91 {fmt(b)}")

# dd-meta 結構化切面
meta = {}
for p in glob.glob(str(ROOT / "docs/dd/DD_*.html")):
    t = open(p, errors="ignore").read()
    m = re.search(r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', t, re.S)
    if not m: continue
    try: j = json.loads(m.group(1))
    except Exception: continue
    if j.get("ticker") and j.get("date"):
        meta[f"{j['ticker']}-{j['date'].replace('-', '')}"] = j

def grp(title, keyf, sel=lambda j: True, ver=None):
    g = defaultdict(list)
    for i, j in meta.items():
        if i not in ex or not sel(j): continue
        if ver and ex[i]["verdict"] != ver: continue
        v = td28(i)
        if v is not None: g[keyf(j)].append(v)
    print(f"\n### {title}（td28）")
    for k in sorted(g, key=str): print(f"- {k}：{fmt(g[k])}")

print("\n## B. dd-meta 切面")
grp("觀望 × 估值燈 val（row 8 基線）", lambda j: j.get("val"), ver="觀望")
grp("進場 × MA（✅ vs 🟡，MA 對決策矩陣合併）", lambda j: j.get("ma"), ver="進場")
grp("進場 × cycle_position（8b/QC-42）", lambda j: j.get("cycle_position") or "非循環", ver="進場")
grp("觀望 × cycle_position", lambda j: j.get("cycle_position") or "非循環", ver="觀望")
grp("全部裁決 × signal 訊號", lambda j: (ex[f"{j['ticker']}-{j['date'].replace('-','')}"]["verdict"], j.get("signal")))
grp("進場 × industry_clock_phase", lambda j: j.get("industry_clock_phase"), ver="進場")

# QC-49：同檔 90 天內連續兩份 DD，翻面 vs 承繼
print("\n### QC-49 hysteresis：同檔 <=90 天連續兩份 DD")
by = defaultdict(list)
for i, r in ex.items(): by[r["entity"]].append(r)
flip, hold = [], []
from datetime import date
for t, rs in by.items():
    rs.sort(key=lambda r: r["date"])
    for a, b in zip(rs, rs[1:]):
        d = (date.fromisoformat(b["date"]) - date.fromisoformat(a["date"])).days
        if d > 90: continue
        (hold if a["verdict"] == b["verdict"] else flip).append((t, a["date"], a["verdict"], b["date"], b["verdict"], d, td28(b["id"])))
print(f"- 相鄰配對 {len(flip)+len(hold)}：承繼同裁決 {len(hold)}／翻面 {len(flip)}（翻面率 {len(flip)/max(1,len(flip)+len(hold)):.0%}）")
print("- 承繼組（第二份 DD 後）：", fmt([x[6] for x in hold if x[6] is not None]))
print("- 翻面組（第二份 DD 後）：", fmt([x[6] for x in flip if x[6] is not None]))
for x in flip[:20]: print("  翻面:", x)
