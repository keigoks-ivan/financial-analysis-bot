#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/active-etf/ 五個分析模組的機械層——經理人功力(M1)、擁擠度(M2)、資金流(M3)、
風格與偏好(M4)、操作習慣(M5)。純函式(輸入既有持股快照/股價快取/個股基本資料,
輸出 dict),不打任何網路請求(抓取在 prices.py / security_meta.py),供
scripts/active_etf/build_active_etf.py 呼叫組裝、也供
scripts/tests/test_active_etf_analytics.py 用合成資料單元測試。

已知限制(逐一寫在對應函式 docstring 與輸出 dict 的 *_note_zh 欄位,頁面
「方法論」段落要原樣轉述,不可省略):
    - 0050 權重只有「目前」一份快照,沒有逐日歷史——M1a 主動報酬歸因全程用
      同一份靜態權重,不是逐日真實 0050 權重,期間越長失真越大。
    - 基金持股快照本身不是逐日(每檔約每週 2-4 次),M1a/M5 週轉率一律用
      「最近一次已揭露快照的權重/股數維持到下次快照前」這個階梯狀假設。
    - 個股市值分位(M4 size bucket)僅在「22 檔基金史上曾持有過的個股」母體
      (約 350+ 檔)內排名,不是全市場排名——沒有抓全市場每日股價,母體較小,
      分位數會比全市場排名更集中。
    - M1b 遠期報酬用該檔個股「自己有股價資料的交易日序列」往前數 20/60 格,
      不是嚴格對齊台股完整交易曆(個股若當日無成交量資料會被跳過),與 TAIEX
      同期報酬用最近可得收盤對齊,非同一交易曆逐日勾稽。
"""
from __future__ import annotations

import bisect
import datetime
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ETF_DASH_DATA_DIR = REPO_ROOT / "docs" / "etf-dash" / "data"

sys.path.insert(0, str(REPO_ROOT / "scripts" / "active_etf"))
import fetch_holdings as fh  # noqa: E402 — weight_band_for()

M1B_HORIZONS = (20, 60)  # 交易日


# ── 共用小工具 ────────────────────────────────────────────────────────────
def _dates_of(series):
    return [r[0] for r in series]


dates_of = _dates_of  # 公開別名——build_active_etf.py 組 taiex_dates 時用得到


def _closest_on_or_before(series, dates, target):
    idx = bisect.bisect_right(dates, target) - 1
    return series[idx] if idx >= 0 else None


def _closest_on_or_after(series, dates, target):
    idx = bisect.bisect_left(dates, target)
    return series[idx] if idx < len(series) else None


def snapshot_weights_asof(weight_steps, date):
    """weight_steps: [(as_of, {ticker: weight_pct}), ...] 依 as_of 升冪。回傳
    <=date 裡最新一筆的權重 dict;找不到回空 dict。"""
    out = {}
    for as_of, w in weight_steps:
        if as_of <= date:
            out = w
        else:
            break
    return out


def _weight_steps(snapshots):
    return [(s["as_of"], {r[0]: r[2] for r in s["holdings"]}) for s in snapshots]


def _shares_steps(snapshots):
    return [(s["as_of"], {r[0]: r[1] for r in s["holdings"]}) for s in snapshots]


def median(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None


def load_benchmark_extras():
    """讀 docs/etf-dash/data/0050.json 的 periods(90d eps/price 變動%)與加權遠期
    本益比,供 M4 風格偏好跟 0050 對比。檔案不存在或格式不對回 (None, None)。"""
    path = ETF_DASH_DATA_DIR / "0050.json"
    if not path.exists():
        return None, None
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, None
    periods = {p["key"]: p for p in d.get("periods") or []}
    fwd_pe = (d.get("weighted_forward_pe") or {}).get("value")
    return periods, fwd_pe


# ══════════════════════════════════════════════════════════════════════════
# M1a — 持股法主動報酬歸因 vs 0050
# ══════════════════════════════════════════════════════════════════════════
def active_return_attribution(snapshots, price_history, bench_weights, end_date, window_days,
                               etf_yf_ticker, bench_yf_ticker="0050.TW"):
    """回傳 dict:total_active_return_pct(持股法主動報酬加總)、
    actual_fund_return_pct(ETF 自身股價報酬)、bench_return_pct(0050 同期報酬)、
    residual_pct(= actual - bench - total_active,交易/費用/現金缺口)、
    top_positive/top_negative(各 5 檔逐股累計貢獻)、n_trading_days_used、
    start_date/end_date。任一段缺資料回 None 系列欄位 + note。"""
    dates = sorted(price_history)
    if not dates:
        return {"status": "no_price_data"}
    start_target = (datetime.date.fromisoformat(end_date) - datetime.timedelta(days=window_days)).isoformat()
    usable = [d for d in dates if start_target <= d <= end_date]
    if len(usable) < 2:
        return {"status": "insufficient_trading_days", "n_trading_days_used": len(usable)}

    weight_steps = _weight_steps(snapshots)
    contrib = defaultdict(float)
    n_days = 0
    for i in range(1, len(usable)):
        prev, cur = usable[i - 1], usable[i]
        w_fund = snapshot_weights_asof(weight_steps, prev)
        if not w_fund:
            continue
        close_prev, close_cur = price_history[prev]["close"], price_history[cur]["close"]
        tickers = set(w_fund) | set(bench_weights)
        day_has_data = False
        for t in tickers:
            cp, cc = close_prev.get(t), close_cur.get(t)
            if cp is None or cc is None or cp == 0:
                continue
            r = cc / cp - 1
            active_w = (w_fund.get(t, 0.0) - bench_weights.get(t, 0.0)) / 100.0
            contrib[t] += active_w * r * 100
            day_has_data = True
        if day_has_data:
            n_days += 1

    total_active = round(sum(contrib.values()), 4)

    def _nearest_close(yf_ticker, target_idx, max_lookback=5):
        # yfinance 對個別 ETF ticker 偶爾會有單日資料延遲(該檔當天收盤還沒補進
        # vendor feed,其他檔都有),往前找最近 max_lookback 個 usable 交易日內
        # 有值的那天,跟頁面其餘地方(如 _closest_close_on_or_before)容忍缺口
        # 的做法一致,不因單一 ticker 單日缺值就整段報酬率變 null。
        for back in range(max_lookback + 1):
            idx = target_idx - back
            if idx < 0:
                break
            v = price_history[usable[idx]]["close"].get(yf_ticker)
            if v is not None:
                return v
        return None

    def _fund_price_return(yf_ticker):
        p0 = _nearest_close(yf_ticker, 0)
        p1 = _nearest_close(yf_ticker, len(usable) - 1)
        if p0 and p1:
            return round((p1 / p0 - 1) * 100, 4)
        return None

    actual_return = _fund_price_return(etf_yf_ticker)
    bench_return = _fund_price_return(bench_yf_ticker)
    residual = None
    if actual_return is not None and bench_return is not None:
        residual = round(actual_return - bench_return - total_active, 4)

    ranked = sorted(contrib.items(), key=lambda kv: kv[1], reverse=True)
    top_pos = [{"ticker": t, "contribution_pct": round(v, 4)} for t, v in ranked[:5] if v > 0]
    top_neg = [{"ticker": t, "contribution_pct": round(v, 4)} for t, v in ranked[::-1][:5] if v < 0]

    return {
        "status": "ok", "start_date": usable[0], "end_date": usable[-1],
        "n_trading_days_used": n_days,
        "total_active_return_pct": total_active,
        "actual_fund_return_pct": actual_return,
        "bench_return_pct": bench_return,
        "residual_pct": residual,
        "top_positive": top_pos, "top_negative": top_neg,
    }


def manager_skill_return_attribution(snapshots, price_history, bench_weights, etf_yf_ticker):
    """M1a 三段:1M/3M/since_available。since_available 以最早快照日或最早股價
    資料日(取較晚者)為起點。"""
    if not snapshots:
        return {}
    end_date = snapshots[-1]["as_of"]
    earliest_snap = snapshots[0]["as_of"]
    earliest_price = min(price_history) if price_history else end_date
    since_start = max(earliest_snap, earliest_price)
    since_days = max((datetime.date.fromisoformat(end_date) - datetime.date.fromisoformat(since_start)).days, 1)
    out = {}
    for key, days in (("1m", 30), ("3m", 90), ("since_available", since_days)):
        out[key] = active_return_attribution(snapshots, price_history, bench_weights, end_date, days, etf_yf_ticker)
    return out


# ══════════════════════════════════════════════════════════════════════════
# M1b — 異動後績效(新增/加碼 vs 剔除/減碼的往後 20/60 交易日超額報酬)
# ══════════════════════════════════════════════════════════════════════════
def _forward_excess_return(ticker_series_by_t, taiex_series, taiex_dates, ticker, event_date, horizon):
    series = ticker_series_by_t.get(ticker)
    if not series:
        return None
    dates = _dates_of(series)
    idx0 = bisect.bisect_left(dates, event_date)
    if idx0 >= len(dates):
        return None
    idx1 = idx0 + horizon
    if idx1 >= len(dates):
        return None  # 沒有完整的往後窗口(呼叫端要求:只算走完整個窗口的事件)
    start_date, start_close = dates[idx0], series[idx0][1]
    end_date, end_close = dates[idx1], series[idx1][1]
    if not start_close:
        return None
    stock_ret = end_close / start_close - 1
    t0 = _closest_on_or_after(taiex_series, taiex_dates, start_date)
    t1 = _closest_on_or_after(taiex_series, taiex_dates, end_date)
    if not t0 or not t1 or not t0[1]:
        return None
    taiex_ret = t1[1] / t0[1] - 1
    return {"excess_return_pct": round((stock_ret - taiex_ret) * 100, 4),
            "start_date": start_date, "end_date": end_date}


def build_move_events(code, snapshots, compute_moves_fn):
    """走遍全部連續快照對(不只 week/month/since_earliest 三個定點),用呼叫端
    傳入的 compute_moves_fn(等同 build_active_etf.compute_manager_moves,由
    build_active_etf.py 傳自己的函式進來,analytics.py 因此不必 import
    build_active_etf——避免兩個模組互相 import)判斷 new/increase/exit/decrease。
    事件日 = 偵測到異動的那筆快照 as_of(真實交易可能發生在前一筆快照之後、這筆
    之前,取不到更精確的日期)。回傳 [{ticker, kind, event_date}]。"""
    events = []
    for i in range(1, len(snapshots)):
        moves = compute_moves_fn(snapshots[i], snapshots[i - 1])
        event_date = snapshots[i]["as_of"]
        for kind in ("new", "increase"):
            for rec in moves.get(kind, []):
                events.append({"ticker": rec["ticker"], "kind": kind, "event_date": event_date})
        for kind in ("exit", "decrease"):
            for rec in moves.get(kind, []):
                events.append({"ticker": rec["ticker"], "kind": kind, "event_date": event_date})
    return events


def post_trade_performance(code, snapshots, ticker_series_by_t, taiex_series, taiex_dates, compute_moves_fn):
    """回傳 {"buys": {20: {...}, 60: {...}}, "sells": {20: {...}, 60: {...}}}——
    每個 {n_events, hit_rate_pct, median_excess_return_pct}(n<20 時
    hit_rate_pct/median 仍算但呼叫端/頁面要標「樣本不足」,見 site 規則)。
    buys = new+increase 事件;sells = exit+decrease 事件。"""
    if len(snapshots) < 2:
        return {"buys": {}, "sells": {}, "n_events_total": 0}
    events = build_move_events(code, snapshots, compute_moves_fn)
    out = {"buys": {}, "sells": {}}
    for side, kinds in (("buys", ("new", "increase")), ("sells", ("exit", "decrease"))):
        side_events = [e for e in events if e["kind"] in kinds]
        for h in M1B_HORIZONS:
            excess_list = []
            for e in side_events:
                r = _forward_excess_return(ticker_series_by_t, taiex_series, taiex_dates,
                                            e["ticker"], e["event_date"], h)
                if r is not None:
                    excess_list.append(r["excess_return_pct"])
            n = len(excess_list)
            hit = round(sum(1 for x in excess_list if x > 0) / n * 100, 1) if n else None
            out[side][h] = {
                "n_events": n,
                "hit_rate_pct": hit,
                "median_excess_return_pct": round(median(excess_list), 4) if n else None,
                "sample_sufficient": n >= 20,
            }
    out["n_events_total"] = len(events)
    return out


# ── 持股明細表輔助:近期已出清(權重 0 / 從清單消失)的個股 ────────────────────
def recent_exited_holdings(snapshots, window_days=30):
    """完整持股明細只該顯示「目前真的持有」(weight_pct>0)的個股(見
    build_active_etf.py build_fund() 的過濾)——這裡另外算一份「最近 window_days
    天內出清」的清單給頁面的收合區塊用:出清日 = 該檔股票最後一次 weight_pct>0
    的快照日(下限估計,真正出清發生在那天跟下一筆快照之間,無法精確得知)。
    涵蓋兩種情況:(a) 目前快照裡權重已掛 0 但股票代號還留在清單上,(b) 股票
    代號整個從目前快照的清單消失。從未在任何一筆快照裡出現過 weight_pct>0 的
    代號(純占位列、從未真正持有過)不算「出清」,不列入。回傳依出清天數升冪
    排序的 [{ticker, last_weight_date, days_since}]。"""
    if not snapshots:
        return []
    cur = snapshots[-1]
    today = datetime.date.fromisoformat(cur["as_of"])
    cur_w = {r[0]: r[2] for r in cur["holdings"]}
    cutoff = (today - datetime.timedelta(days=window_days)).isoformat()
    candidates = {t for t, w in cur_w.items() if not w}  # 目前掛 0(或缺值)
    for s in snapshots:
        if s["as_of"] < cutoff:
            continue
        for row in s["holdings"]:
            if row[0] not in cur_w:
                candidates.add(row[0])  # 目前快照完全沒有這檔(整個從清單消失)

    out = []
    for t in candidates:
        last_nonzero = None
        for s in snapshots:
            w = {r[0]: r[2] for r in s["holdings"]}
            if w.get(t, 0):
                last_nonzero = s["as_of"]
        if last_nonzero is None:
            continue  # 從未真正持有過(純占位列),不算出清
        days = (today - datetime.date.fromisoformat(last_nonzero)).days
        if days > window_days:
            continue
        out.append({"ticker": t, "last_weight_date": last_nonzero, "days_since": days})
    out.sort(key=lambda r: r["days_since"])
    return out


# ══════════════════════════════════════════════════════════════════════════
# M2 — 擁擠度(overview,22 檔合併)
# ══════════════════════════════════════════════════════════════════════════
def compute_crowding(fund_results, security_meta, ticker_series_by_t):
    """fund_results:build_fund() 回傳的 list(要有 code/holdings 兩個欄位)。
    回傳 total_shares_held、pct_of_shares_outstanding、n_funds_holding、
    days_to_liquidate(=總持股股數 / 20 日均量)逐檔明細 + top20 x2 + overlap
    matrix(22x22,Σmin(w_i,w_j),百分點)。

    只計入 weight_pct>0 的持股列——部分投信的 PCF 會把已出清的股票留在清單裡、
    權重長期掛 0%(股數則是一個不具意義的最低量,如 1000 股占位),這種列不是
    真的持有,計進 n_funds_holding/total_shares_held 會虛增擁擠度(見
    build_active_etf.py build_fund() 的 holdings_out 已先過濾掉這類列,這裡
    再防禦性判斷一次,不依賴呼叫端一定有做)。"""
    total_shares = defaultdict(float)
    n_funds = defaultdict(int)
    fund_weights = {}
    for f in fund_results:
        w = {}
        for h in f.get("holdings", []):
            if not h.get("weight_pct"):
                continue  # 權重 0(或缺值)＝非真實持有,見上方 docstring
            t = h["ticker"]
            total_shares[t] += h.get("shares") or 0
            n_funds[t] += 1
            w[t] = h.get("weight_pct") or 0.0
        fund_weights[f["code"]] = w

    rows = []
    for t, shares in total_shares.items():
        meta = security_meta.get(t) or {}
        so = meta.get("shares_outstanding")
        pct_so = round(shares / so * 100, 4) if so else None
        series = ticker_series_by_t.get(t) or []
        recent_vol = [r[2] for r in series[-20:] if r[2]]
        adv20 = statistics.mean(recent_vol) if recent_vol else None
        dtl = round(shares / adv20, 2) if adv20 else None
        rows.append({"ticker": t, "name": meta.get("name"), "total_shares_held": int(shares),
                      "n_funds_holding": n_funds[t], "shares_outstanding": so,
                      "pct_of_shares_outstanding": pct_so, "adv20_shares": int(adv20) if adv20 else None,
                      "days_to_liquidate": dtl})

    top_by_pct_so = sorted([r for r in rows if r["pct_of_shares_outstanding"] is not None],
                            key=lambda r: r["pct_of_shares_outstanding"], reverse=True)[:20]
    top_by_dtl = sorted([r for r in rows if r["days_to_liquidate"] is not None],
                         key=lambda r: r["days_to_liquidate"], reverse=True)[:20]

    codes = sorted(fund_weights)
    overlap = []
    for i, ci in enumerate(codes):
        row = []
        for cj in codes:
            wi, wj = fund_weights[ci], fund_weights[cj]
            tickers = set(wi) | set(wj)
            row.append(round(sum(min(wi.get(t, 0.0), wj.get(t, 0.0)) for t in tickers), 2))
        overlap.append(row)

    return {
        "n_stocks_total": len(rows),
        "n_stocks_with_shares_outstanding": sum(1 for r in rows if r["shares_outstanding"]),
        "n_stocks_with_adv20": sum(1 for r in rows if r["adv20_shares"]),
        "top_by_pct_shares_outstanding": top_by_pct_so,
        "top_by_days_to_liquidate": top_by_dtl,
        "overlap_matrix": {"codes": codes, "matrix": overlap},
    }


# ══════════════════════════════════════════════════════════════════════════
# M3 — 資金流(每檔:價格效果 + 淨申贖;overview:全體週淨流入)
# ══════════════════════════════════════════════════════════════════════════
def compute_fund_flows(snapshots):
    """逐連續快照對:price_effect = units_{t-1}*(nav_t - nav_{t-1});
    net_flow = (units_t - units_{t-1}) * nav_t(TWD)。回傳
    {events:[{date,price_effect_100m,net_flow_100m}], cumulative_net_flow_100m,
    n_events_with_units, n_snapshots}。單位:億元(100M TWD),與既有 aum_100m_twd
    欄位同一單位方便對照。任一邊快照缺 nav.units/nav_per_unit 的那一步跳過
    (不計入,也不中斷後續)。"""
    events = []
    for i in range(1, len(snapshots)):
        prev, cur = snapshots[i - 1], snapshots[i]
        u0 = (prev.get("nav") or {}).get("units")
        u1 = (cur.get("nav") or {}).get("units")
        n0 = (prev.get("nav") or {}).get("nav_per_unit")
        n1 = (cur.get("nav") or {}).get("nav_per_unit")
        if not (u0 and u1 and n0 and n1):
            continue
        price_effect = u0 * (n1 - n0)
        net_flow = (u1 - u0) * n1
        events.append({"date": cur["as_of"], "price_effect_100m": round(price_effect / 1e8, 4),
                        "net_flow_100m": round(net_flow / 1e8, 4)})
    cumulative = round(sum(e["net_flow_100m"] for e in events), 4) if events else None
    weekly_net = _bucket_weekly(events, "net_flow_100m")
    weekly_price = {r["week"]: r["value_100m"] for r in _bucket_weekly(events, "price_effect_100m")}
    weekly = [{"week": r["week"], "net_flow_100m": r["value_100m"],
               "price_effect_100m": weekly_price.get(r["week"])} for r in weekly_net]
    return {"events": events, "weekly": weekly, "cumulative_net_flow_100m": cumulative,
            "n_events_with_units": len(events), "n_snapshots": len(snapshots)}


def _bucket_weekly(events, value_key):
    # 2026-09-25：單一基金的資金流圖表改成週彙總(見 build_fund 的 flows.weekly)
    # ——連續 7 個月每日/每次快照事件的長條圖太密看不清楚,跟 overview 的週淨流入
    # 圖表(build_overview_flows() 本來就是週彙總)一致。
    buckets = defaultdict(float)
    for e in events:
        d = datetime.date.fromisoformat(e["date"])
        iso_year, iso_week, _ = d.isocalendar()
        key = "{}-W{:02d}".format(iso_year, iso_week)
        buckets[key] += e[value_key]
    return [{"week": k, "value_100m": round(v, 4)} for k, v in sorted(buckets.items())]


def compute_overview_flows(fund_flows_by_code, fund_names):
    """整合各基金 compute_fund_flows() 結果:週淨流入(全體 22 檔加總,供 overview
    長條圖)+ 逐基金表(累計淨流入、近 30 天淨流入)。"""
    all_events = []
    table = []
    for code, flows in fund_flows_by_code.items():
        all_events.extend(flows["events"])
        last30 = [e["net_flow_100m"] for e in flows["events"]
                  if e["date"] >= (datetime.date.today() - datetime.timedelta(days=30)).isoformat()]
        table.append({"code": code, "name": fund_names.get(code), "cumulative_net_flow_100m": flows["cumulative_net_flow_100m"],
                       "net_flow_last30d_100m": round(sum(last30), 4) if last30 else None,
                       "n_events_with_units": flows["n_events_with_units"]})
    weekly_total = defaultdict(float)
    for e in all_events:
        d = datetime.date.fromisoformat(e["date"])
        iso_year, iso_week, _ = d.isocalendar()
        key = "{}-W{:02d}".format(iso_year, iso_week)
        weekly_total[key] += e["net_flow_100m"]
    weekly_series = [{"week": k, "net_flow_100m": round(v, 4)} for k, v in sorted(weekly_total.items())]
    table.sort(key=lambda r: r["cumulative_net_flow_100m"] or 0, reverse=True)
    return {"weekly_net_flow_100m": weekly_series, "by_fund": table}


# ══════════════════════════════════════════════════════════════════════════
# M4 — 風格與偏好(產業、規模、估值、EPS修正、動能 tilt,vs 0050)
# ══════════════════════════════════════════════════════════════════════════
def _industry_weights(holdings_weight, security_meta):
    out = defaultdict(float)
    for t, w in holdings_weight.items():
        meta = security_meta.get(t)
        out[meta["industry_name"] if meta else "未分類"] += w
    return dict(out)


def _market_caps(tickers, security_meta, latest_close_by_t):
    out = {}
    for t in tickers:
        meta = security_meta.get(t)
        close = latest_close_by_t.get(t)
        if meta and meta.get("shares_outstanding") and close:
            out[t] = meta["shares_outstanding"] * close
    return out


def compute_style_tilts(fund_holdings, bench_weights, security_meta, latest_close_by_t,
                         fund_periods_90d, bench_periods_90d, fund_fwd_pe, bench_fwd_pe,
                         held_universe_tickers):
    """fund_holdings:[{ticker,weight_pct}]。bench_weights:{ticker:weight_pct}
    (0050)。held_universe_tickers:22 檔基金史上曾持有過的全部 ticker(供市值
    分位母體,見模組 docstring 限制說明)。"""
    fund_w = {h["ticker"]: h["weight_pct"] for h in fund_holdings}
    fund_ind = _industry_weights(fund_w, security_meta)
    bench_ind = _industry_weights(bench_weights, security_meta)
    all_ind = set(fund_ind) | set(bench_ind)
    diffs = sorted(
        [{"industry": i, "fund_weight_pct": round(fund_ind.get(i, 0.0), 2),
          "bench_weight_pct": round(bench_ind.get(i, 0.0), 2),
          "diff_pp": round(fund_ind.get(i, 0.0) - bench_ind.get(i, 0.0), 2)} for i in all_ind],
        key=lambda r: r["diff_pp"], reverse=True)
    top_overweight = [r for r in diffs if r["diff_pp"] > 0][:5]
    top_underweight = [r for r in diffs[::-1] if r["diff_pp"] < 0][:5]

    universe_mc = _market_caps(held_universe_tickers, security_meta, latest_close_by_t)
    fund_mc = {t: universe_mc[t] for t in fund_w if t in universe_mc}
    size_note = None
    weighted_median_mc = None
    bucket_share = {"large": 0.0, "mid": 0.0, "small": 0.0}
    if universe_mc:
        sorted_mc = sorted(universe_mc.values())
        n = len(sorted_mc)
        p_large = sorted_mc[int(n * 2 / 3)] if n >= 3 else sorted_mc[-1]
        p_mid = sorted_mc[int(n / 3)] if n >= 3 else sorted_mc[0]

        def _bucket(mc):
            if mc >= p_large:
                return "large"
            if mc >= p_mid:
                return "mid"
            return "small"

        weighted_vals = []
        for t, w in fund_w.items():
            mc = universe_mc.get(t)
            if mc is None:
                continue
            weighted_vals.append((mc, w))
            bucket_share[_bucket(mc)] += w
        if weighted_vals:
            weighted_vals.sort(key=lambda x: x[0])
            total_w = sum(w for _, w in weighted_vals)
            cum = 0.0
            for mc, w in weighted_vals:
                cum += w
                if cum >= total_w / 2:
                    weighted_median_mc = mc
                    break
        coverage = len(fund_mc) / len(fund_w) * 100 if fund_w else 0
        size_note = "市值分位母體為 22 檔基金史上曾持有過的 {} 檔個股(非全市場排名);本基金持股市值覆蓋率 {:.1f}%".format(len(universe_mc), coverage)

    return {
        "industry_top_overweight": top_overweight, "industry_top_underweight": top_underweight,
        "industry_diffs_all": diffs,
        "weighted_median_market_cap_100m_twd": round(weighted_median_mc / 1e8, 1) if weighted_median_mc else None,
        "size_bucket_share_pct": {k: round(v, 2) for k, v in bucket_share.items()},
        "size_note_zh": size_note,
        "fwd_pe_diff": (round(fund_fwd_pe - bench_fwd_pe, 2)
                        if (fund_fwd_pe is not None and bench_fwd_pe is not None) else None),
        "fund_fwd_pe": fund_fwd_pe, "bench_fwd_pe": bench_fwd_pe,
        "eps_revision_90d_tilt_pp": (round(fund_periods_90d - bench_periods_90d, 4)
                                      if (fund_periods_90d is not None and bench_periods_90d is not None) else None),
        "momentum_90d_tilt_pp": None,  # 由呼叫端填(見 build_active_etf 傳入 price_chg_pct_90d 差)
    }


def style_snapshot_trend(snapshots, security_meta, months_back=9):
    """M4「監月趨勢」的可行子集(見模組 docstring 限制):只用既有快照的持股權重
    +靜態產業別,算每月最後一筆快照的產業權重(取權重最高的 3 個產業)——不含
    估值/EPS修正/動能趨勢(那些需要「歷史當天」的 EPS 預估與股價快照,現有
    eps_cache 只保留最新一份,無法回推)。回傳 [{month, top_industries:[...]}]。"""
    by_month = {}
    for s in snapshots:
        month = s["as_of"][:7]
        by_month[month] = s  # 保留每月最後一筆(snapshots 依時間升冪,後面的覆蓋前面的)
    months = sorted(by_month)[-months_back:]
    out = []
    for m in months:
        s = by_month[m]
        w = {r[0]: r[2] for r in s["holdings"]}
        ind = _industry_weights(w, security_meta)
        top3 = sorted(ind.items(), key=lambda kv: kv[1], reverse=True)[:3]
        out.append({"month": m, "as_of": s["as_of"],
                     "top_industries": [{"industry": i, "weight_pct": round(v, 2)} for i, v in top3]})
    return out


# ══════════════════════════════════════════════════════════════════════════
# M5 — 操作習慣(週轉率、平均持有期、檔數、集中度、股票部位)
# ══════════════════════════════════════════════════════════════════════════
def monthly_turnover(snapshots, price_history):
    """turnover_pair = (Σ|Δshares_i| × price_i) / 2 / AUM_cur,依 cur 快照所在
    月份加總同月內所有相鄰快照對的 turnover_pair(月度週轉率,非年化)。價格取
    price_history 中 cur.as_of 當天(找不到當天用最近一個 <= 的收盤)。"""
    dates = sorted(price_history)
    monthly = defaultdict(float)
    pairs_used = defaultdict(int)
    for i in range(1, len(snapshots)):
        prev, cur = snapshots[i - 1], snapshots[i]
        aum = (cur.get("nav") or {}).get("scale")
        if not aum:
            continue
        prev_h = {r[0]: r[1] for r in prev["holdings"]}
        cur_h = {r[0]: r[1] for r in cur["holdings"]}
        # price_history 的 key 是日期字串橫斷面(非逐檔 series),直接用日期字串
        # 二分搜尋找「cur.as_of 當天或最近之前」那一個交易日的收盤價橫斷面。
        idx = bisect.bisect_right(dates, cur["as_of"]) - 1
        px_date = dates[idx] if idx >= 0 else None
        closes = price_history[px_date]["close"] if px_date else {}
        trade_value = 0.0
        covered = 0
        for t in set(prev_h) | set(cur_h):
            dshares = abs(cur_h.get(t, 0) - prev_h.get(t, 0))
            if dshares == 0:
                continue
            price = closes.get(t)
            if price is None:
                continue
            trade_value += dshares * price
            covered += 1
        month = cur["as_of"][:7]
        monthly[month] += trade_value / 2 / aum * 100
        pairs_used[month] += 1
    return [{"month": m, "turnover_pct": round(v, 3), "n_snapshot_pairs": pairs_used[m]}
            for m, v in sorted(monthly.items())]


def avg_holding_period_days(snapshots):
    """closed position = 一段「連續出現」的區間,在最新快照之前就結束(之後的
    快照不再持有)。end_date 取「最後一次確認持有」那筆快照日,不是真正出場日
    (出場發生在 end_date 與下一筆快照之間的某一天,無法精確得知)——因此
    days 是持有期間的下限估計,不是精確值。回傳 {avg_days, n_closed_positions,
    closed:[{ticker,start_date,end_date,days}]}。"""
    presence = defaultdict(list)  # ticker -> [as_of,...] 出現過的快照日期(升冪)
    for s in snapshots:
        held = {r[0] for r in s["holdings"]}
        for t in held:
            presence[t].append(s["as_of"])
    latest = snapshots[-1]["as_of"] if snapshots else None
    all_dates = [s["as_of"] for s in snapshots]
    closed = []
    for t, dates in presence.items():
        # 把 dates 切成連續段(用 all_dates 的相鄰關係判斷是否連續出現,即中間
        # 沒有任何一筆快照「有資料但不含這檔」)
        date_set = set(dates)
        spans = []
        span_start = None
        prev_in = False
        for d in all_dates:
            in_now = d in date_set
            if in_now and not prev_in:
                span_start = d
            if not in_now and prev_in:
                spans.append((span_start, prev_date))
            prev_in = in_now
            prev_date = d
        if prev_in:
            spans.append((span_start, prev_date))
        for start, end in spans:
            if end == latest:
                continue  # 仍持有中,不是「已平倉」
            days = (datetime.date.fromisoformat(end) - datetime.date.fromisoformat(start)).days
            closed.append({"ticker": t, "start_date": start, "end_date": end, "days": days})
    avg_days = round(statistics.mean([c["days"] for c in closed]), 1) if closed else None
    return {"avg_days": avg_days, "n_closed_positions": len(closed),
            "closed": sorted(closed, key=lambda c: c["end_date"], reverse=True)[:20]}


def compute_operations(code, snapshots, price_history):
    turnover = monthly_turnover(snapshots, price_history)
    holding = avg_holding_period_days(snapshots)
    band_min, band_max, band_note = fh.weight_band_for(code)
    n_names_series, top10_series, stockweight_series = [], [], []
    for s in snapshots:
        w = [r[2] for r in s["holdings"]]
        total_w = round(sum(w), 2)
        top10 = round(sum(sorted(w, reverse=True)[:10]), 2)
        n_names_series.append({"date": s["as_of"], "n_holdings": len(s["holdings"])})
        top10_series.append({"date": s["as_of"], "top10_pct": top10})
        stockweight_series.append({"date": s["as_of"], "stock_weight_pct": total_w,
                                    "low_equity": total_w < band_min})
    return {
        "monthly_turnover": turnover,
        "holding_period": holding,
        "n_holdings_over_time": n_names_series,
        "top10_concentration_over_time": top10_series,
        "stock_weight_over_time": stockweight_series,
        "weight_band_min_pct": band_min, "weight_band_note_zh": band_note,
    }
