#!/usr/bin/env python3
"""黃金重播：生效日邊界對 repo 歷史。把重播結果跟當時 CI 實際提交的 state.json（git show）逐項對。

兩段：
1. 邊界場景（capture 找出的 bnd_<commit>：用該輪的前一版 state.json 當 prev_state、--now＝該輪 generated_at，
   跑現在的程式）對該輪提交的 state.json：各檔週／月方向、水位、目標、現持、權重、曝險、正二、債金、最後一筆 history。
2. 全史表（現在的程式＋快照價格）對快照裡 state.json 的 history 紀錄（Supertrend 生效後每天實錄的週／月方向、水位、目標）。
這是一次性的歷史核對，不是 compare 的替代：差異只列出、不判失敗（現在的程式本來就含 11-05 之後的改動）。

用法：boundary_check.py --snapshot <快照目錄> --result <replay 結果.json>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _golden as G  # noqa: E402

LEGS = ("QQQ", "SMH", "0050", "2330")
MISSING = "（無）"


def pick(s: dict) -> dict:
    out = {}
    hu, ht = s.get("history_us") or [], s.get("history_tw") or []
    out["資料日.us"] = hu[-1]["date"] if hu else None
    out["資料日.tw"] = ht[-1]["date"] if ht else None
    for t in LEGS:
        tk = (s.get("tickers") or {}).get(t) or {}
        st = tk.get("st") or {}
        out[f"{t}.rule"] = tk.get("rule")
        for f in ("w", "m", "trend_pct", "level_pct"):
            out[f"{t}.st.{f}"] = st.get(f, MISSING) if st else MISSING
        for f in ("trigger_z", "z", "start"):      # 下軌接回中才有；11-08 台股改還原全息會改寫 z
            out[f"{t}.st.tb_info.{f}"] = (st.get("tb_info") or {}).get(f, MISSING)
        for f in ("final_weight_pct", "executed_pct", "held_before_pct"):
            out[f"{t}.{f}"] = tk.get(f, MISSING)
        out[f"weights.{t}"] = (s.get("weights") or {}).get(t)
    for k in ("combined_exposure_us_pct", "combined_exposure_tw_pct", "last_change_date", "defensive_rule"):
        out[k] = s.get(k, MISSING)
    l2 = s.get("tw_l2")
    for f in ("applied", "level_pct", "target_pct", "exposure_pct", "tb", "tb_trigger_z", "active_from"):
        out[f"tw_l2.{f}"] = l2.get(f, MISSING) if l2 else MISSING
    ov = s.get("overlay") or {}
    for leg in ("ief", "gld"):
        for f in ("rule", "level_pct", "target_pct"):
            out[f"overlay.{leg}.{f}"] = (ov.get(leg) or {}).get(f, MISSING)
    for hk, legs in (("history_us", ("QQQ", "SMH")), ("history_tw", ("0050", "2330"))):
        rec = (s.get(hk) or [{}])[-1]
        for t in legs:
            tk = (rec.get("tickers") or {}).get(t) or {}
            out[f"{hk}[-1].{t}.final_pct"] = tk.get("final_pct", MISSING)
            out[f"{hk}[-1].{t}.st.level_pct"] = (tk.get("st") or {}).get("level_pct", MISSING)
        if hk == "history_tw":
            out["history_tw[-1].l2"] = rec.get("l2", MISSING)
    return out


def section_boundary(snap: Path, res: dict, meta: dict):
    print("== 一、邊界場景：重播（現在的程式）對當輪 CI 提交的 state.json ==")
    for sc in meta["scenarios"]:
        if not sc["name"].startswith("bnd_"):
            continue
        r = res["scenarios"].get(sc["name"])
        ref = json.loads((snap / "boundary" / sc["commit"][:12] / "state.json").read_text())
        print(f"\n[{sc['commit'][:10]}] --now {sc['now']}　涵蓋 {', '.join(sc['covers'])}")
        if not r or (r.get("outputs") or {}).get("error") or not (r.get("outputs") or {}).get("state"):
            print(f"  重播失敗：{((r or {}).get('outputs') or {}).get('error')}")
            continue
        a, b = pick(r["outputs"]["state"]), pick(ref)
        diff = [(k, b[k], a[k]) for k in a if not G.same(a[k], b.get(k))]
        print(f"  比 {len(a)} 項，一致 {len(a) - len(diff)}，不一致 {len(diff)}；"
              f"重播{'有' if r['outputs'].get('alert_exists') else '沒有'}寫可行動提醒檔")
        for k, vb, va in diff:
            print(f"    {k:<34} 提交 {json.dumps(vb, ensure_ascii=False):<28} 重播 {json.dumps(va, ensure_ascii=False)}")


def section_table(snap: Path, res: dict, meta: dict):
    print("\n== 二、全史表對 state.json 的 history 實錄（Supertrend 生效後每天）==")
    state = json.loads((snap / meta["inputs"][G.STATE_REL]).read_text())
    rows = {(r["d"], r["t"]): r for r in res["scenarios"]["table"]["outputs"]["rows"]}
    n = bad = 0
    for hk, legs in (("history_us", ("QQQ", "SMH")), ("history_tw", ("0050", "2330"))):
        for rec in state.get(hk) or []:
            if not any((rec["tickers"].get(t) or {}).get("rule") == "st_live" for t in legs):
                continue
            for t in legs:
                tk, st = rec["tickers"][t], rec["tickers"][t].get("st") or {}
                r = rows.get((rec["date"], t))
                if r is None:
                    print(f"  {rec['date']} {t}：全史表沒有這天（資料日不同）")
                    bad += 1
                    continue
                pairs = [("週線", st.get("w"), r["w"]), ("月線", st.get("m"), r["m"]),
                         ("水位", st.get("level_pct"), r["level"]),
                         ("目標 final_pct", tk.get("final_pct"), round(r["final_raw"] * 100, 1))]
                n += 1
                d = [(lab, x, y) for lab, x, y in pairs if x != y]
                if d:
                    bad += 1
                    print(f"  {rec['date']} {t}：" + "；".join(f"{lab} 實錄 {x} 重播 {y}" for lab, x, y in d))
            if hk == "history_tw" and "l2" in rec:
                r = rows.get((rec["date"], "00631L"))
                n += 1
                got = (r["level"], round(r["level"] * r["w_raw"], 1)) if r else None
                want = (rec["l2"].get("level_pct"), rec["l2"].get("target_pct"))
                if got != want:
                    bad += 1
                    print(f"  {rec['date']} 00631L：實錄 水位／占比 {want} 重播 {got}")
    print(f"  共 {n} 組（日期×檔），不一致 {bad}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--result", required=True)
    args = ap.parse_args()
    snap = Path(args.snapshot)
    meta = json.loads((snap / "meta.json").read_text())
    res = json.loads(Path(args.result).read_text())
    section_boundary(snap, res, meta)
    section_table(snap, res, meta)


if __name__ == "__main__":
    main()
