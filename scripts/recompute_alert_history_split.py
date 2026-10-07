#!/usr/bin/env python3
"""recompute_alert_history_split.py — 一次性：警戒度拆分後重算實盤歷史（2026-10-06）.

ONE-SHOT，非 cron、非 pipeline。警戒度改成只數壓力面、另加熱度（見
build_detective.compute_alert_level／compute_heat_level）後，docs/detective/data/
alert_history.json 裡的舊分數是舊公式的值，必須用同一套新函數重算，圖上才是同一把尺。

做法：對 alert_history.json 的每個實盤日，取 `git log` 裡 docs/detective/data/
latest.json 當天（JSON 的 as_of 為準）最後一次 commit 的快照，用它儲存的 signals／
composites 重跑新分數與熱度。spx_close 沿用原值。points 變成
[date, score, band, spx_close, heat_count]（append only，讀取端用 p[1..3]）。

不誠實重建的日子（找不到當天快照、快照缺 signals／composites、快照自身 counts 與
signals 筆數對不上）不動原點的分數，只補第 5 欄 null，並在輸出列出。

用法：python3 scripts/recompute_alert_history_split.py [--dry-run]
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_detective as bd  # noqa: E402

LATEST_REL = "docs/detective/data/latest.json"
HIST_PATH = os.path.join(ROOT, "docs", "detective", "data", "alert_history.json")


def _git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL)


def snapshots_by_asof(pre_split_only=False):
    """{as_of: (commit, latest.json dict)}，同一 as_of 取最後一次 commit。
    pre_split_only：略過拆分後（帶 heat_level）的快照，供驗證讀「舊分數」。"""
    revs = [ln.split()[0] for ln in
            _git("log", "--format=%H", "--", LATEST_REL).decode().splitlines() if ln.strip()]
    out = {}
    for h in reversed(revs):                      # 舊 → 新，後者覆蓋前者
        try:
            d = json.loads(_git("show", f"{h}:{LATEST_REL}"))
        except Exception:
            continue
        if pre_split_only and "heat_level" in d:
            continue
        a = d.get("as_of")
        if a:
            out[a] = (h, d)
    return out


def check_faithful(d):
    """快照能否忠實重算；回傳 (ok, 原因)。"""
    sigs, comps = d.get("signals"), d.get("composites")
    if not isinstance(sigs, list) or not isinstance(comps, list):
        return False, "快照缺 signals／composites"
    if any("key" not in s for s in sigs):
        return False, "signals 缺 key（舊格式）"
    total = (d.get("counts") or {}).get("total")
    if total is not None and total != len(sigs):
        return False, f"counts.total={total} 與 signals 筆數 {len(sigs)} 不符"
    return True, ""


def recompute(points, snaps):
    new_points, report = [], {"recomputed": 0, "unfaithful": []}
    for p in points:
        date, old_score, old_band, spx = p[0], p[1], p[2], (p[3] if len(p) > 3 else None)
        snap = snaps.get(date)
        if not snap:
            report["unfaithful"].append((date, "找不到當天的 latest.json 快照"))
            new_points.append([date, old_score, old_band, spx, None])
            continue
        _, d = snap
        ok, why = check_faithful(d)
        if not ok:
            report["unfaithful"].append((date, why))
            new_points.append([date, old_score, old_band, spx, None])
            continue
        al = bd.compute_alert_level(d["signals"], d["composites"], date)
        hl = bd.compute_heat_level(d["signals"], d["composites"], date)
        new_points.append([date, al["score"], al["band"], spx, hl["count"]])
        report["recomputed"] += 1
    return new_points, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    hist = json.load(open(HIST_PATH, encoding="utf-8"))
    snaps = snapshots_by_asof()
    new_points, report = recompute(hist["points"], snaps)
    print(f"重算 {report['recomputed']}／{len(hist['points'])} 天")
    for date, why in report["unfaithful"]:
        print(f"  無法忠實重建 {date}：{why}（保留原分數，熱度欄 null）")
    if args.dry_run:
        return
    hist["points"] = new_points
    with open(HIST_PATH, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(hist, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    print(f"寫入 {HIST_PATH}")


if __name__ == "__main__":
    main()
