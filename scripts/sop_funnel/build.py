#!/usr/bin/env python3
"""Pure MA SOP 漏斗 — 每日 orchestrator。

流程：價格 stitch → 全 universe 訊號掃描 → ledger append（永不改舊事件）→
T+1 進場 fill → open trades 重模擬（冪等；closed 凍結）→ 待命區/築基中/記分板
聚合 → 寫 latest.json + server-render sop-funnel.html。

用法：
  python3 scripts/sop_funnel/build.py                      # 每日（CI Step 9）
  python3 scripts/sop_funnel/build.py --backfill-from 2026-05-17   # 首跑回填
  python3 scripts/sop_funnel/build.py --no-benchmark-refresh      # 離線（測試）

冪等保證：事件以 id 去重；非回填模式只收「最近 8 個交易日」內的新訊號
（防止未來 quality 漂移在歷史憑空生事件）；closed trades 永久凍結。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sop_funnel import earnings_guard, prices  # noqa: E402
from sop_funnel.engine import (  # noqa: E402
    PARAMS, PREREG, QUALITY_GATE, build_frame, fixed_horizon_ret,
    next_trading_close, position_pct, quality_check, scan_ticker,
    simulate_trade, stop_dist_pct,
)
from sop_funnel.render import render_page  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DD_LATEST = REPO_ROOT / "docs" / "dd-screener" / "latest.json"
OUT_DIR = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel"
LEDGER_PATH = OUT_DIR / "ledger.json"
LATEST_PATH = OUT_DIR / "latest.json"
PAGE_PATH = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel.html"
BACKTEST_PATH = OUT_DIR / "backtest.json"
RECENT_TRADING_DAYS = 8   # 非回填模式的新事件收納窗


def load_quality() -> dict[str, dict]:
    data = json.loads(DD_LATEST.read_text(encoding="utf-8"))
    return {s["ticker"]: s for s in data.get("stocks", [])}


def load_ledger() -> dict:
    if LEDGER_PATH.exists():
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return {"schema_version": "1.0", "events": [], "meta": {}}


def b_watch(frame, events, today: pd.Timestamp, params=PARAMS) -> dict | None:
    """B 第二班車待命狀態（display 用）：最近 A1 錨存活、未 fired、回踩中。"""
    a1s = [e for e in events if e["type"] == "A1"]
    if not a1s:
        return None
    anchor = a1s[-1]
    if any(e for e in events if e["type"] == "B"
           and e["anchor_a1_date"] == anchor["date"]):
        return None   # 本錨 B 已用
    # 錨作廢：錨後完成週收盤 < MA52w
    pos = frame._frozen_pos(today)
    w52 = frame.wma[52]
    for j in range(pos + 1):
        if frame.wclose.index[j] <= anchor["date"]:
            continue
        if not pd.isna(w52.iloc[j]) and float(frame.wclose.iloc[j]) < float(w52.iloc[j]):
            return None
    px = float(frame.close.iloc[-1])
    since = frame.close.loc[frame.close.index > anchor["date"]]
    peak = float(since.max()) if not since.empty else px
    if px >= peak * 0.99:
        return None   # 未在回踩中
    m60 = frame.ma60.iloc[-1]
    m60 = float(m60) if not pd.isna(m60) else None
    weeks = (today - anchor["date"]).days / 7.0
    return {
        "anchor_date": str(anchor["date"].date()),
        "weeks_since_anchor": round(weeks, 1),
        "exceeded": weeks > params["b_window_weeks"],
        "pullback_pct": round((px / peak - 1) * 100, 1),
        "dist_60ma_pct": round((px / m60 - 1) * 100, 1) if m60 else None,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill-from", default=None,
                    help="首跑回填起日 YYYY-MM-DD（僅 ledger 為空時生效）")
    ap.add_argument("--no-benchmark-refresh", action="store_true")
    args = ap.parse_args()

    closes = prices.load_closes()
    spy, spy_stale = prices.load_benchmark(refresh=not args.no_benchmark_refresh)
    quality = load_quality()
    ledger = load_ledger()
    known_ids = {e["id"] for e in ledger["events"]}
    today = closes.index.max()

    backfilling = bool(args.backfill_from) and not ledger["events"]
    if backfilling:
        window_start = pd.Timestamp(args.backfill_from)
    else:
        window_start = closes.index[-RECENT_TRADING_DAYS] \
            if len(closes.index) >= RECENT_TRADING_DAYS else closes.index[0]

    universe = [t for t in quality if t in closes.columns]
    frames: dict[str, object] = {}
    qmeta: dict[str, tuple] = {}
    insufficient: list[dict] = []
    standby_a1: list[dict] = []
    standby_a2: list[dict] = []
    standby_b: list[dict] = []
    base_building: list[dict] = []
    population: list[dict] = []        # 五條件全過的母體（頁面 §6）
    moat_excluded: list[dict] = []     # 四質量過、卡護城河 gate（26→23 對帳）
    n_qpass = n_state1 = 0
    new_events = 0

    for t in universe:
        frame = build_frame(closes[t])
        if frame is None:
            continue
        frames[t] = frame
        row = quality[t]
        qpass, qfails, qused = quality_check(row)
        qmeta[t] = (qpass, qfails, qused)
        if qpass:
            n_qpass += 1
        events = scan_ticker(frame, qpass, qfails)

        # ── ledger append（窗內新事件）──
        # 噪音控制：五條件 fail/缺資料的票不進帳本（漏斗外，頁面以「五條件過閘 N」
        # 呈現即可）；過閘票的否決（態②/排列/歷史不足）才是 SOP 張力證據，必記。
        for e in events:
            if not qpass:
                continue
            if e["date"] < window_start or e["date"] > today:
                continue
            eid = f"{t}:{e['date'].date()}:{e['type']}"
            if eid in known_ids:
                continue
            known_ids.add(eid)
            new_events += 1
            sd = stop_dist_pct(frame, e["date"], e["close"])
            status = "vetoed" if e["vetoes"] else "pending"
            vetoes = list(e["vetoes"])
            # 財報窗標記（2026-06-11 用戶裁決：不擋、只標）— 回測顯示被擋 14 筆
            # 放行後全數獲利（含 FIX +186%），惟證據含凍結名單 survivorship 偏誤；
            # forward 標記持續累積無偏數據，季檢複查是否恢復禁令
            earnings_check, next_earnings = None, None
            if not backfilling and status == "pending":
                earnings_check, next_earnings = earnings_guard.check(t, e["date"])
            ledger["events"].append({
                "id": eid, "ticker": t,
                "name": row.get("name"), "sector": row.get("sector"),
                "entry_type": e["type"],
                "base_age_weeks": e["base_age_weeks"],
                "base_star": e["base_star"],
                "anchor_a1_date": str(e["anchor_a1_date"].date()) if e["anchor_a1_date"] is not None else None,
                "signal_date": str(e["date"].date()),
                "signal_close": round(e["close"], 4),
                "stop_dist_pct": round(sd, 2) if sd is not None else None,
                "suggested_position_pct": position_pct(sd),
                "status": status,
                "vetoes": vetoes,
                "backfilled": backfilling,
                "earnings_check": earnings_check,
                "next_earnings": next_earnings,
                "moat_review_due": (row.get("dd_age_days") or 0)
                                   > QUALITY_GATE["moat_review_age_days"],
                "quality_at_signal": qused,
                "dd_path": row.get("dd_path"), "dca_path": row.get("dca_path"),
                "sim": None, "fixed": None,
            })

        # ── 待命區 / 築基中（今日快照）──
        px = float(frame.close.iloc[-1])
        full_max = float(frame.close.max())
        dist_ath = (px / full_max - 1) * 100
        ath_date = frame.close.idxmax()
        ath_age_w = (today - ath_date).days / 7.0
        ok1, reasons1 = frame.state1(today, px)
        if ok1:
            n_state1 += 1

        # ── 母體清單（頁面 §6）+ 護城河 gate 對帳 ──
        moat_fail_only = (qpass is False and qfails
                          and all(f.startswith("護城河") for f in qfails))
        if qpass or moat_fail_only:
            (population if qpass else moat_excluded).append({
                "ticker": t, "name": row.get("name"), "sector": row.get("sector"),
                "moat_grade": row.get("moat_grade"), "moat_trend": row.get("moat_trend"),
                "moat_score": row.get("moat_score"), "signal": row.get("signal"),
                "cagr": qused.get("eps_fy1_fy3_cagr_pct"), "roic": qused.get("roic"),
                "fcf": qused.get("fcf"), "peg": qused.get("peg_used"),
                "dist_ath_pct": round(dist_ath, 1), "ath_age_weeks": round(ath_age_w, 1),
                "state1": ok1, "state1_fails": reasons1,
                "moat_cut": [f for f in qfails if f.startswith("護城河")] if moat_fail_only else [],
                "moat_review_due": (row.get("dd_age_days") or 0)
                                   > QUALITY_GATE["moat_review_age_days"],
                "dd_age_days": row.get("dd_age_days"),
                "dd_path": row.get("dd_path"), "dca_path": row.get("dca_path"),
            })

        if "歷史不足" in reasons1 and qpass:
            insufficient.append({"ticker": t, "name": row.get("name")})
            continue
        if not qpass:
            continue
        common = {"ticker": t, "name": row.get("name"), "sector": row.get("sector"),
                  "dist_ath_pct": round(dist_ath, 1),
                  "ath_age_weeks": round(ath_age_w, 1),
                  "state1": ok1, "state1_fails": reasons1,
                  "dd_path": row.get("dd_path")}
        if ok1 and dist_ath >= -PARAMS["near_ath_pct"]:
            (standby_a1 if ath_age_w >= PARAMS["base_age_min_weeks"]
             else standby_a2).append(common)
        elif ok1 and (-PARAMS["base_watch_dist"][1] <= dist_ath <= -PARAMS["base_watch_dist"][0]
                      and ath_age_w >= PARAMS["base_watch_min_weeks"]):
            base_building.append(common)
        bw = b_watch(frame, events, today)
        if bw:
            standby_b.append({**common, **bw})

    # ── T+1 進場 fill + 模擬（按訊號日時序處理；每 ticker 同時最多一筆 open）──
    occupied: dict[str, str] = {}   # ticker → 佔用至（exit_date 或 "open"）
    for ev in sorted(ledger["events"], key=lambda x: x["signal_date"]):
        t = ev["ticker"]
        frame = frames.get(t)
        if frame is None or ev["status"] in ("vetoed", "closed", "skipped"):
            if ev["status"] == "closed" and ev.get("sim"):
                occupied[t] = ev["sim"].get("exit_date") or "open"
            continue
        sig_d = pd.Timestamp(ev["signal_date"])
        occ = occupied.get(t)
        if occ == "open" or (occ and ev["signal_date"] <= occ):
            ev["status"] = "skipped"   # 已持倉中（charter：每 ticker 單筆）
            ev["vetoes"] = ["已持倉"]
            continue
        if ev["status"] == "pending":
            ntc = next_trading_close(frame.close, sig_d)
            if ntc is None:
                continue   # T+1 收盤未到
            ev["status"] = "entered"
            ev["entry_date"] = str(ntc[0].date())
        entry_d = pd.Timestamp(ev["entry_date"])
        res = simulate_trade(frame, entry_d)
        end_d = pd.Timestamp(res["exit_date"]) if res["exit_date"] else today
        spy_ret = prices.benchmark_ret_pct(spy, entry_d, end_d)
        res["spy_ret_pct"] = round(spy_ret, 2) if spy_ret is not None else None
        res["alpha_pct"] = round(res["ret_pct"] - spy_ret, 2) \
            if (res["ret_pct"] is not None and spy_ret is not None) else None
        ev["sim"] = res
        ev["fixed"] = {
            "ret_13w": fixed_horizon_ret(frame.close, entry_d, 91),
            "ret_26w": fixed_horizon_ret(frame.close, entry_d, 182),
        }
        if res["status"] == "closed":
            ev["status"] = "closed"   # 凍結
            occupied[t] = res["exit_date"] or "open"
        else:
            occupied[t] = "open"

    # ── 記分板聚合 ──
    def agg(etype: str) -> dict:
        evs = [e for e in ledger["events"] if e["entry_type"] == etype]
        entered = [e for e in evs if e["status"] in ("entered", "closed")]
        closed = [e for e in entered if e["status"] == "closed"
                  and e["sim"] and e["sim"]["ret_pct"] is not None]
        rets = sorted(e["sim"]["ret_pct"] for e in closed)
        alphas = [e["sim"]["alpha_pct"] for e in closed if e["sim"]["alpha_pct"] is not None]
        rs = [e["sim"]["r_multiple"] for e in closed if e["sim"]["r_multiple"] is not None]
        return {
            "signals": len(evs),
            "vetoed": sum(1 for e in evs if e["status"] == "vetoed"),
            "skipped": sum(1 for e in evs if e["status"] == "skipped"),
            "pending": sum(1 for e in evs if e["status"] == "pending"),
            "entered": len(entered),
            "open": sum(1 for e in entered if e["status"] == "entered"),
            "closed": len(closed),
            "win_rate": round(sum(1 for r in rets if r > 0) / len(rets) * 100, 1) if rets else None,
            "median_ret_pct": rets[len(rets) // 2] if rets else None,
            "mean_alpha_pct": round(sum(alphas) / len(alphas), 2) if alphas else None,
            "mean_r": round(sum(rs) / len(rs), 2) if rs else None,
            "thin": len(closed) < 20,
        }

    today_str = str(today.date())
    today_signals = [e for e in ledger["events"]
                     if e["signal_date"] == today_str and e["status"] != "vetoed"]
    today_vetoed = [e for e in ledger["events"]
                    if e["signal_date"] == today_str and e["status"] == "vetoed"]
    open_trades = [e for e in ledger["events"] if e["status"] == "entered" and e["sim"]]
    closed_trades = [e for e in ledger["events"] if e["status"] == "closed"]

    # ── 否決原因分布（帳本累計 + 近 30 日窗）──
    veto_evs = [e for e in ledger["events"] if e["status"] == "vetoed"]
    cutoff_30d = today - pd.Timedelta(days=30)
    reason_all, reason_recent = Counter(), Counter()
    recent_total = 0
    for e in veto_evs:
        is_recent = pd.Timestamp(e["signal_date"]) >= cutoff_30d
        if is_recent:
            recent_total += 1
        for r in (e.get("vetoes") or []):
            reason_all[r] += 1
            if is_recent:
                reason_recent[r] += 1
    veto_distribution = {
        "total": len(veto_evs),
        "recent_window_days": 30,
        "recent_total": recent_total,
        "by_reason": [{"reason": r, "count": n} for r, n in reason_all.most_common()],
        "recent_by_reason": [{"reason": r, "count": n} for r, n in reason_recent.most_common()],
    }

    backtest = None
    if BACKTEST_PATH.exists():
        try:
            backtest = json.loads(BACKTEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            backtest = None

    latest = {
        "schema_version": "1.0",
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": today_str,
        "params": {k: v for k, v in PARAMS.items() if not k.startswith("_")},
        "universe_total": len(universe),
        "quality_pass": n_qpass,
        "state1_count": n_state1,
        "spy_benchmark_stale": spy_stale,
        "today_signals": today_signals,
        "today_vetoed": today_vetoed,
        "veto_distribution": veto_distribution,
        "standby_a1": sorted(standby_a1, key=lambda x: -x["ath_age_weeks"]),
        "standby_a2": sorted(standby_a2, key=lambda x: x["dist_ath_pct"], reverse=True),
        "standby_b": sorted(standby_b, key=lambda x: x["weeks_since_anchor"]),
        "base_building": sorted(base_building, key=lambda x: -x["ath_age_weeks"]),
        "insufficient_history": insufficient,
        "prereg": PREREG,
        "population": sorted(population, key=lambda x: (
            {"S": 0, "A": 1, "B": 2}.get(x["moat_grade"], 9), -(x["moat_score"] or 0))),
        "moat_excluded": moat_excluded,
        "open_trades": open_trades,
        "closed_trades": closed_trades,
        "scoreboard": {k: agg(k) for k in ("A1", "A2", "B")},
        "backtest": backtest,
    }

    ledger["meta"] = {"last_run": latest["run_timestamp"], "as_of": today_str,
                      "backfill_from": ledger["meta"].get("backfill_from") or args.backfill_from}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    LATEST_PATH.write_text(json.dumps(latest, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    PAGE_PATH.write_text(render_page(latest), encoding="utf-8")
    print(f"sop-funnel: as_of={today_str} universe={len(universe)} 五條件pass={n_qpass} "
          f"新事件={new_events} 持倉={len(open_trades)} 已平倉={len(closed_trades)} "
          f"今日板機={len(today_signals)} 今日否決={len(today_vetoed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
