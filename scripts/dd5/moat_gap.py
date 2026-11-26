#!/usr/bin/env python3
"""護城河寬度初判（程式算、零成本）：本檔對同業中位數的三年差距。

輸入：run 目錄的 peers.json（peers.py 產生，data[代號]["years"] 由新到舊，fin＝是否金融業）。
輸出：
  - moat_gap.md：給寫稿模型看的一段資料（引用標記 [p:moat_gap]），也進 lint 的參考文字
  - moat_gap.json：機器欄位，排版後併進 machine.json 的 moat

規則（2026-11-26 持有人選「程式算差距＋模型挑上限」，規格見記憶 project-dd5-moat-grading-1126）：
  - 主指標：一般公司用投入資本報酬率；金融業用股東權益報酬率；
    本檔任一年投入資本報酬率超過 60%（資本基數太小、資產輕）或拿不到時，改用營業利益率。
  - 差距＝本檔減同業中位數（百分點），同一年序對齊（最新、前一年、前兩年；各家會計年度結束月不同，不再對日期）。
    某一年有值的同業不到 2 家，那一年不算。
  - 初判寬度：三年都有值、平均 ≥10 且每年為正 → 寬；平均 3～10 → 窄；不到 3 → 無（份額第一且報酬為正時模型可改窄）；
    本檔最新一年主指標為負 → 無。只有兩年資料時照算，但標「年數不足」。
  - 初判走勢：差距連兩年縮小、每年至少 1 個百分點且至少是原差距的 5%、而且本檔主指標最新一年沒有高於兩年前 → 變弱；
    連兩年擴大、門檻相同、而且本檔沒有低於兩年前 → 變強（同業跌得比較多不算本檔變強）；其餘持平。虧損股不判。
  - 循環股初判是寬時，谷底年本檔要 ≥10%、而且谷底年差距 ≥10 個百分點，否則壓到窄。
  - 循環提示：本檔主指標三年內最高減最低超過 30 個百分點，或有一年為負另一年超過 20%，標「可能是循環股」，並給谷底年數字。
這些只是初判；降級上限、份額例外、循環股看谷底、未量化優勢由寫稿模型照規則卡判斷，最後的寬度以模型為準。
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

METRIC_NAME = {"roic": "投入資本報酬率", "roe": "股東權益報酬率", "om": "營業利益率"}


def _val(years, i, key):
    if i >= len(years):
        return None
    v = years[i].get(key)
    return float(v) if isinstance(v, (int, float)) else None


def pick_metric(me, others):
    if me.get("fin"):
        return "roe", "金融業用股東權益報酬率"
    ys = me.get("years") or []
    rs = [r for r in (_val(ys, i, "roic") for i in range(3)) if r is not None]
    if not rs:
        if any(_val(ys, i, "roe") is not None for i in range(3)):
            return "roe", "投入資本報酬率拿不到，改用股東權益報酬率"
        return "om", "投入資本報酬率拿不到，改用營業利益率"
    if max(rs) > 0.60:
        return "om", "本檔投入資本報酬率超過 60%（資本基數小），改用營業利益率"
    for i in range(3):
        pv = [x for x in (_val(v["years"], i, "roic") for v in others.values()) if x is not None]
        if len(pv) >= 2 and statistics.median(pv) > 0.60:
            return "om", "同業中位數的投入資本報酬率超過 60%（資產輕），改用營業利益率"
    return "roic", ""


def compute(ticker, peers_json):
    data = peers_json.get("data") or {}
    me = data.get(ticker)
    if not me or not me.get("years"):
        return None
    others = {k: v for k, v in data.items() if k != ticker and v.get("years")}
    metric, why = pick_metric(me, others)
    rows = []
    for i in range(3):
        mine = _val(me["years"], i, metric)
        pv = [x for x in (_val(v["years"], i, metric) for v in others.values()) if x is not None]
        med = statistics.median(pv) if len(pv) >= 2 else None
        gap = round((mine - med) * 100, 1) if (mine is not None and med is not None) else None
        rows.append({"fy": me["years"][i].get("fy") if i < len(me["years"]) else None,
                     "mine": None if mine is None else round(mine * 100, 1),
                     "peer_median": None if med is None else round(med * 100, 1),
                     "n_peers": len(pv), "gap": gap})
    gaps = [r["gap"] for r in rows]  # 新到舊
    have = [g for g in gaps if g is not None]
    notes = []
    if why:
        notes.append(why)
    mine_vals = [r["mine"] for r in rows if r["mine"] is not None]
    width, trend = None, None
    if len(have) < 2:
        notes.append("缺同業：可比的年度不到兩年")
    else:
        if len(have) < 3:
            notes.append("年數不足：只有 {0} 年可比".format(len(have)))
        avg = sum(have) / len(have)
        latest_mine = rows[0]["mine"]
        if latest_mine is not None and latest_mine < 0:
            width = "無"
            notes.append("本檔最新一年{0}為負".format(METRIC_NAME[metric]))
        elif len(have) == 3 and avg >= 10 and all(g > 0 for g in have):
            width = "寬"
        elif avg >= 3:
            width = "窄"
        else:
            width = "無"
        # 走勢：用三年都有值的情況判；舊→新。虧損股不判，改看毛利率與單位經濟（模型寫）
        loss = latest_mine is not None and latest_mine < 0
        if loss:
            notes.append("虧損股：走勢不用差距判，改看毛利率與單位經濟")
        elif all(g is not None for g in gaps):
            g2, g1, g0 = gaps[2], gaps[1], gaps[0]
            m_old, m_new = rows[2]["mine"], rows[0]["mine"]
            th1, th2 = max(1.0, abs(g2) * 0.05), max(1.0, abs(g1) * 0.05)  # 每年至少 1 個百分點、且至少是原差距的 5%
            if (g1 - g2) <= -th1 and (g0 - g1) <= -th2 and not (m_new is not None and m_old is not None and m_new > m_old):
                trend = "變弱"
            elif (g1 - g2) >= th1 and (g0 - g1) >= th2 and not (m_new is not None and m_old is not None and m_new < m_old):
                trend = "變強"
            else:
                trend = "持平"
    cyc = None
    if len(mine_vals) >= 2:
        hi, lo = max(mine_vals), min(mine_vals)
        if hi > 0 and (hi - lo > 30 or (lo < 0 and hi > 20)):
            trough = min(rows, key=lambda r: r["mine"] if r["mine"] is not None else 9e9)
            cyc = {"trough_fy": trough["fy"], "trough_mine": trough["mine"], "trough_gap": trough["gap"]}
            notes.append("可能是循環股：三年內{0}從 {1}% 到 {2}%，谷底年 {3}".format(METRIC_NAME[metric], lo, hi, trough["fy"]))
            if width == "寬" and not (trough["gap"] is not None and trough["gap"] >= 10 and trough["mine"] >= 10):
                width = "窄"
                notes.append("循環股上限：谷底年本檔不到 10% 或差距不到 10 個百分點，初判從寬壓到窄")
    avg_gap = round(sum(have) / len(have), 1) if have else None
    return {"width_metric": METRIC_NAME[metric], "metric_key": metric, "rows": rows,
            "gap_vs_peer_median": gaps, "avg_gap": avg_gap,
            "width_initial": width, "trend_initial": trend, "cyclical": cyc, "notes": notes}


def to_md(res):
    if not res:
        return ""
    L = ["## [p:moat_gap] 護城河寬度初判（程式算）", "",
         "主指標：{0}。差距＝本檔減同業中位數（百分點），三年由新到舊，同業各自取同一年序（會計年度結束月不同，沒有對日期）。".format(res["width_metric"]), "",
         "| 年度（本檔） | 本檔 | 同業中位數 | 可比同業家數 | 差距（百分點） |", "|---|---|---|---|---|"]
    f = lambda x, s="": "—" if x is None else "{0}{1}".format(x, s)
    for r in res["rows"]:
        L.append("| {0} | {1} | {2} | {3} | {4} |".format(r["fy"] or "—", f(r["mine"], "%"), f(r["peer_median"], "%"), r["n_peers"], f(r["gap"])))
    L += ["", "- 三年平均差距：{0} 個百分點".format(f(res["avg_gap"])),
          "- 初判寬度：{0}（寬＝三年平均 ≥10 且每年為正；窄＝3～10；無＝不到 3 或本檔為負）".format(res["width_initial"] or "無法判斷"),
          "- 初判走勢：{0}（變弱＝差距連兩年縮、每年至少 1 個百分點且至少是原差距的 5%、本檔沒有升；變強＝連兩年擴大，門檻相同、本檔沒有降）".format(res["trend_initial"] or "無法判斷")]
    for n in res["notes"]:
        L.append("- 注意：" + n)
    return "\n".join(L) + "\n"


def build(run_dir, ticker):
    run_dir = Path(run_dir)
    pj = run_dir / "peers.json"
    if not pj.exists():
        return None
    res = compute(ticker, json.loads(pj.read_text(encoding="utf-8")))
    if not res:
        return None
    (run_dir / "moat_gap.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    (run_dir / "moat_gap.md").write_text(to_md(res), encoding="utf-8")
    return res


def merge_into_machine(run_dir):
    """把程式算的欄位併進 machine.json 的 moat（程式數字為準；模型的 width 保留，另存初判）。"""
    run_dir = Path(run_dir)
    gj, mj = run_dir / "moat_gap.json", run_dir / "machine.json"
    if not (gj.exists() and mj.exists()):
        return
    res = json.loads(gj.read_text(encoding="utf-8"))
    mach = json.loads(mj.read_text(encoding="utf-8"))
    mo = mach.get("moat") or {}
    mo["width_metric"] = res["width_metric"]
    mo["gap_vs_peer_median"] = res["gap_vs_peer_median"]
    mo["width_initial"] = res["width_initial"]
    mo["trend_initial"] = res["trend_initial"]
    mach["moat"] = mo
    mj.write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    # 用法：python3 moat_gap.py RUN_DIR TICKER  → 印出 moat_gap.md
    r = build(sys.argv[1], sys.argv[2])
    print(to_md(r) if r else "（沒有 peers.json 或本檔不在表內）")
