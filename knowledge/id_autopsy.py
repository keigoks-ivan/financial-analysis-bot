#!/usr/bin/env python3
"""
id_autopsy.py — ID 層機器裁決驗屍（重寫自 calibration_id_20260707.md 描述的方法；原腳本未入庫）。

方法：每份 ID 取 id-meta related_tickers 中 depth=🔴 且 beneficiary=True 的成分股做等權籃子，
自裁決 as-of 日（sections_refreshed.judgment，缺則 publish_date）起，結算 91 天（成熟者）與至今，
對基準（美股 QQQ／台股 0050.TW…，同 settle_excess.bench_for）算超額。
輸出：sd_verdict、sd_verdict×clock_phase、priced_in、conviction 的 n/超額中位/勝率；
另盤點 kill_metrics 的機器可讀狀態覆蓋（id-meta last_status、detective kill_watch 機械評估）。
離散比較（超額>0）在整數 bps 空間做。同一 as-of 日大批 backfill（2026-06-21）會讓樣本非獨立，表尾另列。
  python3.12 knowledge/id_autopsy.py
"""
import glob, json, re, statistics as st, sys
from collections import Counter, defaultdict
from pathlib import Path
K = Path(__file__).resolve().parent
sys.path.insert(0, str(K))
import settle_outcomes as so
import settle_excess as sx

ROOT = K.parent
META = re.compile(r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>', re.S)
bench = sx.load_bench()["series"]


def basket(tickers, d0, days):
    """等權籃子；days=None 表至今。回傳 (basket_bps, bench_bps, n_names) 或 None。"""
    legs = []
    for t in tickers:
        bars = so._bars(t); bs = bench.get(sx.bench_for(t))
        if not bars or not bs: continue
        a = so._close_at_or_before(bars, d0)
        if not a: continue
        last_d = bars[-1][0]
        if days is None:
            e = bars[-1]
        else:
            tgt = so._plus_days(d0, days)
            if last_d < tgt: continue
            e = so._close_at_or_before(bars, tgt)
        b0, b1 = sx.at_or_before(bs, a[0]), sx.at_or_before(bs, e[0])
        if not (b0 and b1): continue
        legs.append((sx.bps(a[1], e[1]), sx.bps(b0[1], b1[1])))
    if not legs: return None
    return (sum(l[0] for l in legs) // len(legs), sum(l[1] for l in legs) // len(legs), len(legs))


def main():
    ids = []; cov = Counter(); kstat = Counter(); kn = 0
    for p in sorted(glob.glob(str(ROOT / "docs/id/ID_*.html"))):
        t = open(p, errors="ignore").read(); m = META.search(t)
        if not m: cov["no_meta"] += 1; continue
        try: j = json.loads(m.group(1))
        except Exception: cov["bad_meta"] += 1; continue
        cov["meta"] += 1
        for k in (j.get("kill_metrics") or []):
            if isinstance(k, dict):
                kn += 1; kstat[str(k.get("last_status"))] += 1
        if not j.get("sd_verdict"): continue
        cov["sd_verdict"] += 1
        d0 = (j.get("sections_refreshed") or {}).get("judgment") or j.get("publish_date")
        rt = j.get("related_tickers") or []
        tk = [r["ticker"] for r in rt if isinstance(r, dict) and r.get("depth") == "🔴" and r.get("beneficiary")]
        if not (d0 and tk): continue
        ids.append((Path(p).name, j, d0, tk))
    print(f"ID 總覽：{dict(cov)}；kill_metrics 共 {kn} 條，last_status 分布 {dict(kstat)}")
    res = []
    for name, j, d0, tk in ids:
        r91 = basket(tk, d0, 91); rtd = basket(tk, d0, None)
        res.append(dict(name=name, d0=d0, sd=j["sd_verdict"], ph=str(j.get("clock_phase")), pi=str(j.get("priced_in")),
                        conv=str(j.get("conviction")), h91=r91, td=rtd))
    print(f"可結算 ID：{len(res)}（至今）；h91 成熟：{sum(1 for r in res if r['h91'])}")
    print("as-of 日分布：", Counter(r["d0"] for r in res).most_common(5))

    def tab(keyf, hz, title):
        g = defaultdict(list)
        for r in res:
            v = r[hz]
            if v: g[keyf(r)].append(v[0] - v[1])
        print(f"\n### {title}（{hz}）")
        for k in sorted(g):
            ex = g[k]; w = sum(1 for e in ex if e > 0)
            f = " ⚠n<10" if len(ex) < 10 else ""
            print(f"- {k}：n={len(ex)}{f}｜超額中位 {st.median(ex)/100:+.1f}%｜勝率 {w}/{len(ex)}")
    for hz in ("h91", "td"):
        tab(lambda r: r["sd"], hz, "sd_verdict")
        tab(lambda r: (r["sd"], r["ph"]), hz, "sd_verdict × clock_phase")
        tab(lambda r: r["pi"], hz, "priced_in")
        tab(lambda r: r["conv"], hz, "conviction")
    # 獨立性：排除 2026-06-21 backfill 批，只看之後新鮮的 ID
    fresh = [r for r in res if r["d0"] > "2026-06-30"]
    print(f"\n非 backfill 批（as-of > 2026-06-30）：{len(fresh)} 份")
    res_all = res; res = fresh
    tab(lambda r: r["sd"], "td", "sd_verdict（新鮮 ID）")
    tab(lambda r: r["pi"], "td", "priced_in（新鮮 ID）")
    res = res_all
    # detective 機械評估的 ID kill 覆蓋
    kw = ROOT / "docs/detective/data/kill_watch.json"
    if kw.exists():
        d = json.loads(kw.read_text()); items = d.get("items", [])
        idi = [i for i in items if str(i.get("doc", "")).startswith("docs/id/")]
        print(f"\ndetective kill_watch：機械評估 {len(items)} 條，其中 ID {len(idi)} 條；狀態 {dict(Counter(i.get('status') for i in idi))}；"
              f"coverage={d.get('coverage')}")


if __name__ == "__main__":
    main()
