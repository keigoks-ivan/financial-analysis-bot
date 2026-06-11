#!/usr/bin/env python3
"""SOP 漏斗完整回測（2022-01-01 → 今）— Tier 1 per-trade + Tier 2 NAV 組合模擬。

定位：一次性研究 script（非 CI 排程）。輸出 docs/dd-screener/sop-funnel/backtest-full.json
供 render_backtest.py 生成 sop-funnel-backtest.html。

誠實邊界（頁面大字明標）：
- 五條件閘門凍結今日值（無歷史分析師預估/護城河評級）→ 本回測驗證的是
  「技術執行層在今日 23 檔倖存精英上的歷史行為」，不是漏斗選股能力
- universe 本身是今日策展的 DD 名單 → 結構性 survivorship
- 價格 = 還原股價（auto_adjust，含息含拆股；用戶 2026-06-11 指定）
- 歷史財報靜默期：yfinance get_earnings_dates 覆蓋 22/23 檔；查無窗 → 標未驗

Tier 1：per-trade（gated 23 檔 + ungated 全 universe 對照）、年度拆分、
        型態拆分、態④ charter vs staged A/B、歷史靜默期守衛
Tier 2：NAV 組合模擬（charter S-2）— 部位 = min(10%, 1.5%/停損距離)×NAV、
        總曝險 ≤100%（純現股）、同日優先序 A1>B>A2 再按基期、
        斷路器：NAV 自高點回撤 ≥10% → 停新倉+停回補；回到 -5% 內且
        ≥5 交易日後解除。回補/進場被擋時 trade 標記，出場腿永遠執行。

用法：python3 scripts/sop_funnel/backtest_full.py [--start 2022-01-01] [--skip-earnings-fetch]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sop_funnel import prices  # noqa: E402
from sop_funnel.engine import (  # noqa: E402
    PARAMS, build_frame, next_trading_close, quality_check, scan_ticker,
    simulate_trade,
)
from sop_funnel.build import DD_LATEST, OUT_DIR  # noqa: E402

OUT_JSON = OUT_DIR / "backtest-full.json"
EARNINGS_CACHE = OUT_DIR / "earnings_history.json"
SILENT_CAL_DAYS = 7          # 財報前 5 交易日 ≈ 7 曆日
EARNINGS_COVER_DAYS = 100    # 訊號前後 100 日內无任何財報日記錄 = 覆蓋缺口 → 未驗
MIN_ENTRY_W = 0.5            # 額度不足下限（%NAV），低於此 skip
BREAKER_DD = -10.0           # 斷路器觸發（%）
BREAKER_RELEASE_DD = -5.0    # 解除門檻
BREAKER_RELEASE_DAYS = 5     # 解除最少經過交易日


# ── 歷史財報日 ───────────────────────────────────────────────────────────────
def load_earnings_history(tickers: list[str], fetch: bool = True) -> dict[str, list[str]]:
    cache: dict[str, list[str]] = {}
    if EARNINGS_CACHE.exists():
        cache = json.loads(EARNINGS_CACHE.read_text(encoding="utf-8"))
    missing = [t for t in tickers if t not in cache]
    if fetch and missing:
        import yfinance as yf
        for t in missing:
            try:
                ed = yf.Ticker(t).get_earnings_dates(limit=60)
                dates = sorted({pd.Timestamp(d).tz_localize(None).strftime("%Y-%m-%d")
                                for d in ed.index}) if ed is not None and not ed.empty else []
            except Exception:
                dates = []
            cache[t] = dates
            print(f"  earnings {t}: {len(dates)} 筆")
        EARNINGS_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1),
                                  encoding="utf-8")
    return cache


def earnings_verdict(dates: list[str], signal_date: pd.Timestamp) -> str:
    """silent | ok | unverified（訊號前後 100 日無任何記錄 = 覆蓋缺口）。"""
    if not dates:
        return "unverified"
    ts = [pd.Timestamp(d) for d in dates]
    if not any(abs((d - signal_date).days) <= EARNINGS_COVER_DAYS for d in ts):
        return "unverified"
    for d in ts:
        if 0 <= (d - signal_date).days <= SILENT_CAL_DAYS:
            return "silent"
    return "ok"


# ── Tier 1：訊號 → per-trade ────────────────────────────────────────────────
def collect_trades(closes: pd.DataFrame, tickers: list[str],
                   start: pd.Timestamp, end: pd.Timestamp,
                   earnings: dict[str, list[str]] | None,
                   params: dict) -> list[dict]:
    """每 ticker 掃描 → 窗內乾淨訊號 → 靜默期守衛 → 時序去重（每檔單筆）→ 模擬。"""
    trades: list[dict] = []
    for t in tickers:
        if t not in closes.columns:
            continue
        frame = build_frame(closes[t])
        if frame is None:
            continue
        events = [e for e in scan_ticker(frame, True, [], params)
                  if not e["vetoes"] and start <= e["date"] <= end]
        busy_until: pd.Timestamp | None = None
        for e in events:
            if busy_until is not None and e["date"] <= busy_until:
                continue
            echeck = None
            if earnings is not None:
                echeck = earnings_verdict(earnings.get(t, []), e["date"])
                if echeck == "silent":
                    trades.append({"ticker": t, "entry_type": e["type"],
                                   "signal_date": str(e["date"].date()),
                                   "earnings_check": "silent", "sim": None,
                                   "base_age_weeks": e["base_age_weeks"]})
                    continue
            ntc = next_trading_close(frame.close, e["date"])
            if ntc is None:
                continue
            res = simulate_trade(frame, ntc[0], params=params)
            trades.append({"ticker": t, "entry_type": e["type"],
                           "signal_date": str(e["date"].date()),
                           "earnings_check": echeck,
                           "base_age_weeks": e["base_age_weeks"], "sim": res})
            busy_until = (pd.Timestamp(res["exit_date"])
                          if res["exit_date"] else end)
    return trades


def attach_alpha(trades: list[dict], spy: pd.Series, end: pd.Timestamp) -> None:
    for tr in trades:
        s = tr.get("sim")
        if not s:
            continue
        e0 = pd.Timestamp(s["entry_date"])
        e1 = pd.Timestamp(s["exit_date"]) if s["exit_date"] else end
        sr = prices.benchmark_ret_pct(spy, e0, e1)
        s["spy_ret_pct"] = round(sr, 2) if sr is not None else None
        s["alpha_pct"] = round(s["ret_pct"] - sr, 2) \
            if (s["ret_pct"] is not None and sr is not None) else None


def stat_block(trades: list[dict]) -> dict:
    """雙口徑統計（all = open 按期末 mark；closed-only 輔助）。"""
    sims = [t["sim"] for t in trades if t.get("sim")]
    silent = sum(1 for t in trades if t.get("earnings_check") == "silent")
    unver = sum(1 for t in trades if t.get("earnings_check") == "unverified")

    def agg(sub):
        rets = sorted(s["ret_pct"] for s in sub if s["ret_pct"] is not None)
        alphas = [s["alpha_pct"] for s in sub if s.get("alpha_pct") is not None]
        rs = [s["r_multiple"] for s in sub if s["r_multiple"] is not None]
        hold = sorted(s["holding_days"] for s in sub)
        return {"n": len(sub),
                "win_rate": round(sum(1 for r in rets if r > 0) / len(rets) * 100, 1) if rets else None,
                "median_ret_pct": rets[len(rets) // 2] if rets else None,
                "mean_ret_pct": round(float(np.mean(rets)), 2) if rets else None,
                "mean_alpha_pct": round(float(np.mean(alphas)), 2) if alphas else None,
                "mean_r": round(float(np.mean(rs)), 2) if rs else None,
                "median_holding_days": hold[len(hold) // 2] if hold else None}
    closed = [s for s in sims if s["status"] == "closed"]
    return {"n_signals": len(trades), "n_entered": len(sims),
            "n_silent_blocked": silent, "n_unverified": unver,
            "n_closed": len(closed), "n_open_at_end": len(sims) - len(closed),
            **agg(sims), "closed_only": agg(closed)}


# ── Tier 2：NAV 組合模擬 ────────────────────────────────────────────────────
def nav_simulation(trades: list[dict], closes: pd.DataFrame,
                   start: pd.Timestamp, end: pd.Timestamp,
                   use_breaker: bool = True) -> dict:
    """重放 per-trade legs 進組合帳。NAV 起始 100；現金不計息。

    - 進場（T+1 收盤，即 sim.entry_date）：w = min(10%, 1.5%/停損)% × 當日 NAV，
      受現金上限（總曝險 ≤100%）與斷路器約束；同日多筆按 A1>B>A2、基期長者優先
    - 腿重放：賣腿（態③/④/⑤）永遠執行；回補腿受斷路器與現金約束
    - 斷路器：收盤 NAV 自高點回撤 ≤ -10% → 觸發；回到 -5% 內且 ≥5 交易日 → 解除
    """
    cal = closes.loc[start:end].index
    # 預組事件表
    entries: dict[pd.Timestamp, list[dict]] = {}
    legs_by_day: dict[pd.Timestamp, list[tuple[dict, dict]]] = {}
    type_rank = {"A1": 0, "B": 1, "A2": 2}
    sims = [t for t in trades if t.get("sim")]
    for tr in sims:
        s = tr["sim"]
        d = pd.Timestamp(s["entry_date"])
        entries.setdefault(d, []).append(tr)
        for leg in s["legs"]:
            legs_by_day.setdefault(pd.Timestamp(leg["date"]), []).append((tr, leg))
    for d in entries:
        entries[d].sort(key=lambda tr: (type_rank.get(tr["entry_type"], 9),
                                        -(tr.get("base_age_weeks") or 0)))

    cash = 100.0
    positions: dict[str, dict] = {}   # ticker → {units, init_units}
    nav_series: list[tuple[str, float, float]] = []   # (date, nav, exposure_pct)
    peak = 100.0
    breaker = False
    breaker_since: pd.Timestamp | None = None
    breaker_episodes: list[dict] = []
    blocked_entries = 0
    scaled_entries = 0
    blocked_rebuys = 0
    trade_weights: dict[int, float] = {}

    def px(t, d):
        s = closes[t].loc[:d].dropna()
        return float(s.iloc[-1]) if not s.empty else None

    for d in cal:
        # ── 1) 腿重放（賣腿永遠執行；回補受限）──
        for tr, leg in legs_by_day.get(d, []):
            key = id(tr)
            pos = positions.get(tr["ticker"])
            if pos is None or pos.get("trade_key") != key:
                continue   # 進場被斷路器擋掉的 trade，無持倉可動
            if leg["reason"] == "態④回補":
                if breaker:
                    blocked_rebuys += 1
                    continue
                qty = leg["fraction"] * pos["init_units"]
                cost = qty * leg["price"]
                cost = min(cost, cash)   # 現金上限
                if cost <= 0:
                    blocked_rebuys += 1
                    continue
                qty = cost / leg["price"]
                cash -= cost
                pos["units"] += qty
            else:   # 賣腿
                qty = min(leg["fraction"] * pos["init_units"], pos["units"])
                cash += qty * leg["price"]
                pos["units"] -= qty
                if pos["units"] <= 1e-12:
                    del positions[tr["ticker"]]

        # ── 2) 進場（斷路器 / 額度）──
        nav_now = cash + sum(p["units"] * (px(t, d) or 0)
                             for t, p in positions.items())
        for tr in entries.get(d, []):
            if tr["ticker"] in positions:
                continue   # 每 ticker 單筆
            if breaker:
                tr["nav_blocked"] = "斷路器"
                blocked_entries += 1
                continue
            s = tr["sim"]
            w = s.get("suggested_position_pct")
            if not w:
                tr["nav_blocked"] = "無部位建議"
                blocked_entries += 1
                continue
            cost = w / 100.0 * nav_now
            if cost > cash:
                if cash / nav_now * 100.0 < MIN_ENTRY_W:
                    tr["nav_blocked"] = "額度不足"
                    blocked_entries += 1
                    continue
                cost = cash
                scaled_entries += 1
                tr["nav_scaled"] = True
            units = cost / s["entry_close"]
            cash -= cost
            positions[tr["ticker"]] = {"units": units, "init_units": units,
                                       "trade_key": id(tr)}
            trade_weights[id(tr)] = round(cost / nav_now * 100, 2)

        # ── 3) 收盤估值 + 斷路器狀態機 ──
        nav = cash + sum(p["units"] * (px(t, d) or 0)
                         for t, p in positions.items())
        peak = max(peak, nav)
        dd = (nav / peak - 1) * 100
        if use_breaker and not breaker and dd <= BREAKER_DD:
            breaker, breaker_since = True, d
            breaker_episodes.append({"trigger": str(d.date()), "release": None,
                                     "dd_at_trigger": round(dd, 1)})
        elif breaker and dd >= BREAKER_RELEASE_DD \
                and (d - breaker_since).days >= BREAKER_RELEASE_DAYS:
            breaker = False
            breaker_episodes[-1]["release"] = str(d.date())
        exposure = (nav - cash) / nav * 100 if nav > 0 else 0
        nav_series.append((str(d.date()), round(nav, 3), round(exposure, 1)))

    navs = [v for _, v, _ in nav_series]
    years = (cal[-1] - cal[0]).days / 365.25
    cagr = ((navs[-1] / 100.0) ** (1 / years) - 1) * 100
    running = np.maximum.accumulate(navs)
    mdd = float(np.min(np.array(navs) / running - 1) * 100)
    daily_ret = pd.Series(navs).pct_change().dropna()
    sharpe = float(daily_ret.mean() / daily_ret.std() * np.sqrt(252)) \
        if daily_ret.std() > 0 else None
    expo = [e for _, _, e in nav_series]
    return {
        "nav_series": nav_series,
        "final_nav": navs[-1],
        "cagr_pct": round(cagr, 2),
        "mdd_pct": round(mdd, 1),
        "sharpe": round(sharpe, 2) if sharpe is not None else None,
        "avg_exposure_pct": round(float(np.mean(expo)), 1),
        "pct_days_flat": round(sum(1 for e in expo if e < 1) / len(expo) * 100, 1),
        "pct_days_full": round(sum(1 for e in expo if e > 90) / len(expo) * 100, 1),
        "breaker_episodes": breaker_episodes,
        "blocked_entries": blocked_entries,
        "scaled_entries": scaled_entries,
        "blocked_rebuys": blocked_rebuys,
        "trade_weights": {str(k): v for k, v in trade_weights.items()},
    }


def benchmark_series(ticker: str, cal: pd.DatetimeIndex) -> list[float] | None:
    """SPY/QQQ 還原收盤對齊 NAV 日曆並正規化 100。"""
    try:
        if ticker == "SPY":
            ser, _ = prices.load_benchmark(refresh=False)
        else:
            import yfinance as yf
            h = yf.Ticker(ticker).history(period="max", auto_adjust=True)["Close"]
            h.index = h.index.tz_localize(None).normalize()
            ser = h
    except Exception:
        return None
    if ser is None or ser.empty:
        return None
    ser = ser[ser.notna() & (ser > 0)]   # QQQ 即時抓也可能含 nan 空 bar
    vals = []
    base = None
    for d in cal:
        s = ser.loc[:d]
        v = float(s.iloc[-1]) if not s.empty else None
        if v is None:
            vals.append(None)
            continue
        if base is None:
            base = v
        vals.append(round(v / base * 100, 3))
    return vals


# ── 主流程 ───────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2022-01-01")
    ap.add_argument("--skip-earnings-fetch", action="store_true")
    args = ap.parse_args()

    closes = prices.load_closes()
    spy, _ = prices.load_benchmark(refresh=False)
    start, end = pd.Timestamp(args.start), closes.index.max()

    dd = json.loads(DD_LATEST.read_text(encoding="utf-8"))
    gated, ungated = [], []
    for s in dd.get("stocks", []):
        p, _, _ = quality_check(s)
        (gated if p else ungated).append(s["ticker"])
    all_universe = gated + ungated

    print(f"窗口 {start.date()} → {end.date()} | gated {len(gated)} / 全 universe {len(all_universe)}")
    print("① 歷史財報日 cache …")
    earnings = load_earnings_history(gated, fetch=not args.skip_earnings_fetch)
    coverage = {t: len(v) for t, v in earnings.items()}

    print("② Tier1 gated（charter 態④）…")
    p_charter = dict(PARAMS)
    trades = collect_trades(closes, gated, start, end, earnings, p_charter)
    attach_alpha(trades, spy, end)

    print("③ Tier1 gated（staged 態④ A/B）…")
    p_staged = dict(PARAMS); p_staged["t4_staged"] = True
    trades_staged = collect_trades(closes, gated, start, end, earnings, p_staged)
    attach_alpha(trades_staged, spy, end)

    print("④ Tier1 ungated 全 universe 對照（無五條件閘門、無靜默期守衛）…")
    trades_ungated = collect_trades(closes, all_universe, start, end, None, p_charter)
    attach_alpha(trades_ungated, spy, end)

    print("⑤ Tier2 NAV 模擬（charter 斷路器 + 無斷路器對照）…")
    nav = nav_simulation(trades, closes, start, end, use_breaker=True)
    import copy
    nav_nb = nav_simulation(copy.deepcopy(trades), closes, start, end,
                            use_breaker=False)
    cal = closes.loc[start:end].index
    spy_norm = benchmark_series("SPY", cal)
    qqq_norm = benchmark_series("QQQ", cal)

    # 年度拆分（gated charter，按進場年）
    yearly = {}
    for y in range(start.year, end.year + 1):
        sub = [t for t in trades if t.get("sim")
               and t["sim"]["entry_date"].startswith(str(y))]
        yearly[str(y)] = stat_block(sub)
        yearly[str(y)]["n_silent_blocked"] = sum(
            1 for t in trades if t.get("earnings_check") == "silent"
            and t["signal_date"].startswith(str(y)))

    by_type = {et: stat_block([t for t in trades if t["entry_type"] == et])
               for et in ("A1", "A2", "B")}

    out = {
        "schema_version": "1.0",
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_start": str(start.date()), "window_end": str(end.date()),
        "price_basis": "還原股價（yfinance auto_adjust=True，含息含拆股）",
        "n_gated": len(gated), "n_universe": len(all_universe),
        "gated_tickers": gated,
        "earnings_coverage": coverage,
        "caveats": [
            "五條件閘門凍結 2026-06-11 今日值（無歷史分析師預估 / 護城河評級）— 本回測驗證技術執行層，非選股能力",
            "universe 為今日策展的 DD 名單 → 結構性 survivorship，數字必然偏樂觀",
            "歷史財報靜默期：22/23 檔足額覆蓋；查無窗標未驗（3653.TW 僅 4 筆）",
            "ungated 對照組未套靜默期守衛（公平性：兩組都含財報雷時段才可比 → 對照僅看相對差）",
            "態⑤ 執行 = 週收盤確認後次一交易日收盤（無開盤價資料層）",
        ],
        "tier1": {
            "gated_charter": stat_block(trades),
            "gated_staged": stat_block(trades_staged),
            "ungated_all": stat_block(trades_ungated),
            "by_type": by_type,
            "yearly": yearly,
        },
        "tier2": {**nav, "spy_norm": spy_norm, "qqq_norm": qqq_norm},
        "tier2_no_breaker": {k: v for k, v in nav_nb.items()
                             if k != "trade_weights"},
        "trades": [{
            "ticker": t["ticker"], "type": t["entry_type"],
            "signal_date": t["signal_date"],
            "earnings_check": t.get("earnings_check"),
            "nav_blocked": t.get("nav_blocked"),
            "nav_weight_pct": nav["trade_weights"].get(str(id(t))),
            **({"entry_date": t["sim"]["entry_date"],
                "entry_close": t["sim"]["entry_close"],
                "exit_date": t["sim"]["exit_date"],
                "exit_reason": t["sim"]["exit_reason"],
                "ret_pct": t["sim"]["ret_pct"],
                "r": t["sim"]["r_multiple"],
                "alpha_pct": t["sim"].get("alpha_pct"),
                "holding_days": t["sim"]["holding_days"],
                "status": t["sim"]["status"]} if t.get("sim") else {}),
        } for t in sorted(trades, key=lambda x: x["signal_date"])],
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    g = out["tier1"]["gated_charter"]
    print(f"\ngated: 訊號{g['n_signals']} 進場{g['n_entered']} 靜默擋{g['n_silent_blocked']} "
          f"| all口徑 勝率{g['win_rate']}% 中位{g['median_ret_pct']}% α{g['mean_alpha_pct']}%")
    print(f"NAV(charter): 終值{nav['final_nav']:.1f} CAGR {nav['cagr_pct']}% MDD {nav['mdd_pct']}% 斷路器{len(nav['breaker_episodes'])}次 擋{nav['blocked_entries']}筆")
    print(f"NAV(無斷路器): 終值{nav_nb['final_nav']:.1f} CAGR {nav_nb['cagr_pct']}% MDD {nav_nb['mdd_pct']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
