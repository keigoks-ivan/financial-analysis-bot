#!/usr/bin/env python3
"""Legacy DCA verdict calibration: realized returns by verdict class.

Rerunnable — weekly_cache refreshes weekly, so the observation window grows
over time. First run 2026-07-02 (median window 1.5 months); rerun quarterly
for a longer, more meaningful window. Findings log: knowledge/calibration_legacy_dca_*.md

Parses <!-- dca-verdict: X --> from docs/dca/DCA_*.html, joins weekly_cache
closes (price at decision week vs latest), reports return distribution per
verdict class + top missed winners in 觀望/迴避 + QQQ excess return.
"""
import json
import re
import statistics as st
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
DCA = ROOT / "docs" / "dca"
CACHE = ROOT / "data" / "weekly_cache"

V_RE = re.compile(r"<!--\s*dca-verdict:\s*([^>]*?)\s*-->")
F_RE = re.compile(r"^DCA_([A-Za-z0-9]+?)(TW|KS)?_(\d{8})\.html$")


def norm_verdict(raw):
    raw = re.sub(r"<[^>]*>|&gt;.*", "", raw).strip()
    if raw.startswith("進場") or raw == "試倉":
        return "進場"
    if raw.startswith("觀望"):
        return "觀望"
    if raw.startswith("迴避"):
        return "迴避"
    return None


def cache_ticker(base, suffix):
    if suffix == "TW":
        return f"{base}.TW"
    if suffix == "KS":
        return f"{base}.KS"
    return base


def load_bars(tk):
    p = CACHE / f"{tk}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())["weekly_bars"]


def close_at(bars, date_str):
    """Weekly close at or just before the decision date."""
    d = datetime.strptime(date_str, "%Y%m%d")
    best = None
    for b in bars:
        we = datetime.strptime(b["week_end"], "%Y-%m-%d")
        if we <= d + timedelta(days=6):
            best = b["close"]
        else:
            break
    return best


qqq = load_bars("QQQ")
rows, missing_price = [], []
for p in sorted(DCA.glob("DCA_*.html")):
    m = F_RE.match(p.name)
    if not m:
        continue
    base, suffix, date = m.groups()
    text = p.read_text(encoding="utf-8", errors="ignore")
    vm = V_RE.search(text)
    if not vm:
        continue
    verdict = norm_verdict(vm.group(1))
    if not verdict:
        continue
    tk = cache_ticker(base, suffix)
    bars = load_bars(tk)
    if not bars:
        missing_price.append((tk, date, verdict, "no-cache"))
        continue
    p0 = close_at(bars, date)
    p1 = bars[-1]["close"]
    if not p0 or not p1:
        missing_price.append((tk, date, verdict, "no-bar"))
        continue
    ret = (p1 / p0 - 1) * 100
    bench = None
    if qqq:
        q0, q1 = close_at(qqq, date), qqq[-1]["close"]
        if q0 and q1:
            bench = (q1 / q0 - 1) * 100
    rows.append({"ticker": tk, "date": date, "verdict": verdict,
                 "ret_pct": round(ret, 1),
                 "excess_pct": round(ret - bench, 1) if bench is not None else None,
                 "months": round((datetime.strptime(bars[-1]["week_end"], "%Y-%m-%d") - datetime.strptime(date, "%Y%m%d")).days / 30.4, 1)})

print(f"樣本 {len(rows)} 筆（缺價 {len(missing_price)}）｜視窗中位 "
      f"{st.median(r['months'] for r in rows):.1f} 個月\n")

for v in ("進場", "觀望", "迴避"):
    sub = [r for r in rows if r["verdict"] == v]
    if not sub:
        continue
    rets = [r["ret_pct"] for r in sub]
    exc = [r["excess_pct"] for r in sub if r["excess_pct"] is not None]
    print(f"【{v}】n={len(sub)}  中位 {st.median(rets):+.1f}%  平均 {st.mean(rets):+.1f}%  "
          f"最大 {max(rets):+.1f}%  最小 {min(rets):+.1f}%")
    print(f"        >+30%: {sum(1 for x in rets if x > 30)} 筆｜>+50%: {sum(1 for x in rets if x > 50)} 筆"
          f"｜>+100%: {sum(1 for x in rets if x > 100)} 筆"
          + (f"｜對 QQQ 超額中位 {st.median(exc):+.1f}%" if exc else ""))

print("\n=== 觀望/迴避裡被漏掉的大贏家（ret >= +30%，按報酬排）===")
missed = sorted((r for r in rows if r["verdict"] in ("觀望", "迴避") and r["ret_pct"] >= 30),
                key=lambda r: -r["ret_pct"])
for r in missed[:20]:
    print(f"  {r['ticker']:<10} {r['date']}  {r['verdict']}  {r['ret_pct']:+7.1f}%  "
          f"({r['months']} 個月)")

print("\n=== 進場的實際表現（按報酬排）===")
ent = sorted((r for r in rows if r["verdict"] == "進場"), key=lambda r: -r["ret_pct"])
for r in ent:
    print(f"  {r['ticker']:<10} {r['date']}  {r['ret_pct']:+7.1f}%")


