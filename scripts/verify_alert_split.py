#!/usr/bin/env python3
"""verify_alert_split.py — 警戒度拆分（2026-10-06）驗證報告，一次性，只印數字不調參.

(a) 實盤 58 天：舊分數與新分數，對「過去 5 日／過去 1 日／未來 5 日」S&P 報酬的相關。
    過關條件（擁有者訂）：新分數不再隨過去 5 日報酬上升（相關約 0 或為負；舊值 +0.37）。
(b) 回測窗（alert_history_backfill.json）：同樣的相關，以及三次最大 S&P 回撤
    谷底前後 5 天的新分數，對照整段中位數。
(c) 實盤最後 15 天：日期、舊分、新分、熱度、S&P 收盤。
(d) 以現行 latest.json 渲染 2026-10-05 的 email 一分鐘版。

舊分數＝拆分前每天最後一次 latest.json 快照裡存的 alert_level.score，只在拆分前
的日期有效（--old-until，預設 2026-10-05）。新分數＝alert_history.json 現值。
相關用日序列（連續交易日列），報酬以列為單位，不補假日。
"""
import argparse
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import recompute_alert_history_split as rec  # noqa: E402
import notify_render as nr  # noqa: E402

DATA = os.path.join(ROOT, "docs", "detective", "data")


def pearson(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pairs)
    if n < 5:
        return None, n
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    sx = sum((p[0] - mx) ** 2 for p in pairs) ** 0.5
    sy = sum((p[1] - my) ** 2 for p in pairs) ** 0.5
    if sx == 0 or sy == 0:
        return None, n
    return sum((p[0] - mx) * (p[1] - my) for p in pairs) / (sx * sy), n


def returns(closes, k, direction):
    """direction 'past'：close[t]/close[t-k]-1；'next'：close[t+k]/close[t]-1。"""
    out = []
    for i in range(len(closes)):
        j = i - k if direction == "past" else i + k
        if 0 <= j < len(closes) and closes[i] and closes[j]:
            out.append(closes[i] / closes[j] - 1 if direction == "past"
                       else closes[j] / closes[i] - 1)
        else:
            out.append(None)
    return out


def corr_block(label, scores, closes):
    res = {}
    for name, (k, d) in {"過去5日": (5, "past"), "過去1日": (1, "past"),
                         "未來5日": (5, "next")}.items():
        r, n = pearson(scores, returns(closes, k, d))
        res[name] = (r, n)
    txt = "  ".join(f"{k} {('%+.2f' % r) if r is not None else 'n/a'}(n={n})"
                    for k, (r, n) in res.items())
    print(f"  {label:<10s} {txt}")
    return res


def drawdown_episodes(closes):
    """回傳依深度排序的回撤事件 [(depth, peak_i, trough_i, recover_i or None)]。"""
    eps, peak_i, i, n = [], 0, 0, len(closes)
    peak = closes[0]
    in_dd, trough_i = False, 0
    for i in range(1, n):
        c = closes[i]
        if c >= peak:
            if in_dd:
                eps.append((closes[trough_i] / peak - 1, peak_i, trough_i, i))
                in_dd = False
            peak, peak_i = c, i
        else:
            if not in_dd:
                in_dd, trough_i = True, i
            if c < closes[trough_i]:
                trough_i = i
    if in_dd:
        eps.append((closes[trough_i] / peak - 1, peak_i, trough_i, None))
    return sorted(eps, key=lambda e: e[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old-until", default="2026-10-05")
    args = ap.parse_args()

    # ── (a) 實盤 ──
    hist = json.load(open(os.path.join(DATA, "alert_history.json"), encoding="utf-8"))["points"]
    snaps = rec.snapshots_by_asof(pre_split_only=True)
    dates = [p[0] for p in hist]
    new = [p[1] for p in hist]
    heat = [p[4] if len(p) > 4 else None for p in hist]
    close = [p[3] for p in hist]
    old = []
    for d in dates:
        sn = snaps.get(d)
        old.append(((sn[1].get("alert_level") or {}).get("score"))
                   if sn and d <= args.old_until else None)
    print(f"(a) 實盤 {len(hist)} 天（{dates[0]} → {dates[-1]}）")
    ra = corr_block("舊分數", old, close)
    rb = corr_block("新分數", new, close)
    ph = [h for h in heat]
    corr_block("熱度欄", ph, close)
    r5 = rb["過去5日"][0]
    verdict = "PASS" if (r5 is not None and r5 <= 0.10) else "FAIL"
    print(f"  條件：新分數對過去 5 日報酬相關 ≈0 或為負（舊值 +0.37）→ 新值 "
          f"{r5:+.2f}，{verdict}" if r5 is not None else "  無法計算")
    print(f"  新分數：中位 {statistics.median(new)}，範圍 {min(new)}–{max(new)}；"
          f"舊分數中位 {statistics.median([x for x in old if x is not None])}")

    # ── (b) 回測 ──
    bpath = os.path.join(DATA, "alert_history_backfill.json")
    if os.path.exists(bpath):
        bt = json.load(open(bpath, encoding="utf-8"))["points"]
        bd_ = [p[0] for p in bt]
        bs = [p[1] for p in bt]
        bc = [p[3] for p in bt]
        print(f"\n(b) 回測 {len(bt)} 天（{bd_[0]} → {bd_[-1]}），S&P 收盤取實際歷史")
        corr_block("新分數", bs, bc)
        med = statistics.median(bs)
        print(f"  整段新分數：中位 {med}，平均 {sum(bs) / len(bs):.1f}，範圍 {min(bs)}–{max(bs)}")
        for depth, pi, ti, ri in drawdown_episodes(bc)[:3]:
            lo, hi = max(ti - 2, 0), min(ti + 3, len(bt))
            seg = bs[lo:hi]
            ep_max = max(bs[pi:(ri if ri is not None else len(bt))])
            print(f"  回撤 {depth * 100:+.1f}%：高點 {bd_[pi]} → 谷底 {bd_[ti]}"
                  f"（{'收復 ' + bd_[ri] if ri is not None else '未收復'}）")
            print(f"    谷底前後 5 天新分數 {seg}（{bd_[lo]}～{bd_[hi - 1]}），"
                  f"對整段中位 {med}；該回撤期間最高 {ep_max}")
    else:
        print("\n(b) 缺 alert_history_backfill.json")

    # ── (c) 最後 15 天 ──
    print("\n(c) 實盤最後 15 天")
    print("  日期        舊分  新分  熱度  S&P 收盤")
    for i in range(max(0, len(hist) - 15), len(hist)):
        o = old[i] if old[i] is not None else "—"
        print(f"  {dates[i]}  {str(o):>4s}  {new[i]:>4d}  {str(heat[i]):>4s}  {close[i]}")

    # ── (d) email 一分鐘版 ──
    latest = json.load(open(os.path.join(DATA, "latest.json"), encoding="utf-8"))
    state = json.load(open(os.path.join(DATA, "state.json"), encoding="utf-8"))
    print(f"\n(d) {latest['as_of']} 每日摘要（純文字版）")
    print(nr.render_digest(latest, state, force=True))


if __name__ == "__main__":
    main()
