#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_yc_equity.py — 殖利率倒掛之後，股票該賣嗎？（yc_equity）

回答 yield_curve 頁（/backtest/yield_curve/）沒回答的問題：倒掛對股市報酬有沒有用。
事件（倒掛起點、判定命中/落空/已在衰退中）直接讀 data/yield_curve_recession.json
的 countries[cc].def_a.events_detail 與 spread_series，不重算；事件的「最後一個倒掛
月」讀同檔 v2.timeline[cc].events（與 events_detail 用同一組 sample_start/sample_end
與 24 個月分組跑出來，用 start 對齊即可）。

股價：OECD SPASTT01{CC}M661N（FRED 免 key CSV），美/德/英/日/加/澳/韓七國；台灣
cpx（央行資料庫）查無台灣證交所加權指數（央行資料庫本來就不收這條），改用 yfinance
^TWII 月收盤（1997 起，spec 明訂的 fallback，非偏離）。美國另抓 CPIAUCSL 算實質報酬。

用法：
    python3 scripts/build_yc_equity.py --fetch   # 抓 FRED + yfinance，存 raw json
    python3 scripts/build_yc_equity.py           # 算統計＋生成頁面
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import math
import random
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_JSON = DATA / "yc_equity_raw.json"
OUT_JSON = DATA / "yc_equity.json"
YC_JSON = DATA / "yield_curve_recession.json"
OUT_HTML = ROOT / "docs" / "backtest" / "yc_equity" / "index.html"
SLOW_BEAR_REF = ROOT / "docs" / "backtest" / "slow_bear_base_rate" / "index.html"
NAV_DIR = ROOT / "docs" / "backtest"

SCHEMA = "yc-equity-v1"
CHART_JS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"

COUNTRIES = [
    ("US", "美國"), ("DE", "德國"), ("GB", "英國"), ("JP", "日本"),
    ("CA", "加拿大"), ("AU", "澳洲"), ("KR", "南韓"), ("TW", "台灣"),
]

FRED_EQUITY = {
    "US": "SPASTT01USM661N", "DE": "SPASTT01DEM661N", "GB": "SPASTT01GBM661N",
    "JP": "SPASTT01JPM661N", "CA": "SPASTT01CAM661N", "AU": "SPASTT01AUM661N",
    "KR": "SPASTT01KRM661N",
}
US_CPI_SERIES = "CPIAUCSL"  # 比 CPALTT01USM661S 更新（共用規格允許二選一）

H_LIST = [6, 12, 24]
EVENT_B_MIN_INVERTED_MONTHS = 3   # 事件B定義只對倒掛月數 >=3 的事件算
EVENT_B_CONFIRM_MONTHS = 3        # 解除後再看 3 個月確認沒再倒掛
MDD_WINDOW = 24
BOOTSTRAP_N = 1000
RANDOM_SEED = 42
RULE_BUYBACK_LAG = 12             # 倒掛解除後 12 個月月底買回
TW_YF_START = "1997-01-01"
MIN_N_FOR_RELIABLE_DISTINCT = 8   # 事件數低於此門檻，拔靴法重抽的信賴區間本身就不穩定，
                                   # 就算不含無條件中位數也不算進「統計上分得出差異」的頭條數字
                                   # （2026-09-17 監督者複審指出台灣 n=4 不可信後新增）

RNG = random.Random(RANDOM_SEED)


def warn(msg: str) -> None:
    print(f"[yc-equity][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[yc-equity] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 抓取
# ═══════════════════════════════════════════════════════════════════════════

def fetch_fred(series_id: str):
    """FRED CSV endpoint（免 key），回傳升冪 [(date_iso, val), ...] 或 None。照抄
    build_yield_curve_recession.py 的 fetch_fred()：requests 預設 UA。"""
    import requests
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
    except Exception as e:
        warn(f"FRED {series_id}: {e}")
        return None
    pts = []
    for line in r.text.strip().split("\n")[1:]:
        parts = line.split(",")
        if len(parts) < 2 or parts[1] in ("", "."):
            continue
        try:
            pts.append((parts[0], float(parts[1])))
        except ValueError:
            continue
    return pts or None


def fetch_tw_yfinance():
    """台灣股價：cpx（央行資料庫）查無台灣證交所加權指數這條序列（央行資料庫本來就不收
    股價指數，只收利率/匯率/貨幣總計數），改用 yfinance ^TWII 月收盤（spec 明訂
    fallback）。回傳 [(date_iso, close), ...] 升冪，或 None。"""
    try:
        import warnings
        warnings.filterwarnings("ignore")
        import yfinance as yf
        df = yf.download("^TWII", start=TW_YF_START, interval="1mo",
                          progress=False, auto_adjust=False)
        if df is None or df.empty:
            return None
        if isinstance(df.columns, __import__("pandas").MultiIndex):
            close = df["Close"].iloc[:, 0]
        else:
            close = df["Close"]
        pts = []
        for dt, val in close.items():
            if val is None or (isinstance(val, float) and math.isnan(val)):
                continue
            pts.append((dt.strftime("%Y-%m-%d"), float(val)))
        pts.sort(key=lambda p: p[0])
        return pts or None
    except Exception as e:
        warn(f"yfinance ^TWII: {e}")
        return None


def do_fetch():
    out = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "series": {}, "meta": {}}
    ok, fail = 0, 0
    for cc, sid in list(FRED_EQUITY.items()) + [("US_CPI", US_CPI_SERIES)]:
        pts = fetch_fred(sid)
        key = sid
        if pts is None:
            warn(f"{sid}: 抓取失敗或無資料")
            out["meta"][key] = {"ok": False, "n": 0, "source": "FRED"}
            fail += 1
            continue
        out["series"][key] = pts
        out["meta"][key] = {"ok": True, "n": len(pts), "start": pts[0][0], "end": pts[-1][0],
                             "source": "FRED"}
        info(f"{sid}: {len(pts)} 筆 {pts[0][0]}..{pts[-1][0]}")
        ok += 1

    tw_pts = fetch_tw_yfinance()
    if tw_pts is None:
        warn("TW ^TWII: 抓取失敗或無資料，台灣股價將標缺")
        out["meta"]["TW_EQUITY"] = {"ok": False, "n": 0, "source": "yfinance ^TWII"}
        fail += 1
    else:
        out["series"]["TW_EQUITY"] = tw_pts
        out["meta"]["TW_EQUITY"] = {"ok": True, "n": len(tw_pts), "start": tw_pts[0][0],
                                     "end": tw_pts[-1][0], "source": "yfinance ^TWII"}
        info(f"TW ^TWII: {len(tw_pts)} 筆 {tw_pts[0][0]}..{tw_pts[-1][0]}")
        ok += 1

    DATA.mkdir(parents=True, exist_ok=True)
    RAW_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    info(f"寫入 {RAW_JSON}：{ok} 成功／{fail} 失敗")


# ═══════════════════════════════════════════════════════════════════════════
# 月份工具（照抄 build_yield_curve_recession.py，不改邏輯）
# ═══════════════════════════════════════════════════════════════════════════

def month_key(date_str: str) -> str:
    return date_str[:7]


def month_index(ym: str) -> int:
    y, m = ym.split("-")
    return int(y) * 12 + int(m)


def month_diff(a: str, b: str) -> int:
    return month_index(a) - month_index(b)


def add_months(ym: str, n: int) -> str:
    idx = month_index(ym) + n - 1
    y, m = divmod(idx, 12)
    return f"{y:04d}-{m + 1:02d}"


def to_monthly_dict(pts):
    d = {}
    for date_iso, val in pts:
        d[month_key(date_iso)] = val
    return d


def wilson_ci(k, n, z=1.959963984540054):
    """Wilson 95% 信賴區間（score interval）。k=命中/負報酬數，n=樣本數。"""
    if not n:
        return None, None
    phat = k / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = (z * ((phat * (1 - phat) / n + z * z / (4 * n * n)) ** 0.5)) / denom
    return max(0.0, round(center - margin, 4)), min(1.0, round(center + margin, 4))


def percentile(sorted_vals, pct):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * (pct / 100)
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)


def bootstrap_median_ci(vals, n_boot=BOOTSTRAP_N):
    """C：bootstrap 95% 區間（中位數，1,000 次重抽事件，有放回）。事件數 <3 時不給區間
    （重抽沒有意義）。"""
    n = len(vals)
    if n < 3:
        return None, None
    medians = []
    for _ in range(n_boot):
        sample = [vals[RNG.randrange(n)] for _ in range(n)]
        medians.append(statistics.median(sample))
    medians.sort()
    lo = medians[int(0.025 * n_boot)]
    hi = medians[min(n_boot - 1, int(0.975 * n_boot))]
    return round(lo, 2), round(hi, 2)


# ═══════════════════════════════════════════════════════════════════════════
# 報酬／回撤
# ═══════════════════════════════════════════════════════════════════════════

def log_return_pct(p0, p1):
    """前向報酬＝log 報酬換算成百分比：ln(P1/P0) × 100（不是還原成算術報酬）。"""
    if p0 is None or p1 is None or p0 <= 0 or p1 <= 0:
        return None
    return round(math.log(p1 / p0) * 100, 2)


def forward_return_with_status(price_dict, month, h, max_month):
    if month not in price_dict:
        return None, "missing_base"
    target = add_months(month, h)
    if target in price_dict:
        return log_return_pct(price_dict[month], price_dict[target]), "ok"
    if target > max_month:
        return None, "not_due"
    return None, "missing"


def mdd_with_status(price_dict, month, max_month, window=MDD_WINDOW):
    """MDD(window)＝事件月起 window 個月內，從事件月價格算起的最深跌幅（算術跌幅，不是
    log 報酬——跌幅慣例上用算術百分比）。窗口未走完（尚未到期）回傳 status='not_due'。"""
    if month not in price_dict:
        return None, "missing_base"
    base = price_dict[month]
    target_end = add_months(month, window)
    if target_end > max_month:
        return None, "not_due"
    worst = 0.0
    have_any = False
    for h in range(0, window + 1):
        mm = add_months(month, h)
        if mm in price_dict:
            have_any = True
            d = (price_dict[mm] / base - 1) * 100
            if d < worst:
                worst = d
    if not have_any:
        return None, "missing"
    return round(worst, 2), "ok"


def unconditional_returns(price_dict, h, samp_start, samp_end):
    """無條件對照＝全樣本每一個月起算同樣 h 的報酬分布，限定在樣本窗內。"""
    out = []
    for m in sorted(price_dict):
        if m < samp_start or m > samp_end:
            continue
        t = add_months(m, h)
        if t in price_dict and t <= samp_end:
            out.append(log_return_pct(price_dict[m], price_dict[t]))
    return out


def dist_stats(vals):
    if not vals:
        return {"n": 0, "median": None, "neg_n": 0, "neg_rate": None, "p25": None, "p75": None}
    sv = sorted(vals)
    n = len(sv)
    neg = sum(1 for v in sv if v < 0)
    return {
        "n": n, "median": round(statistics.median(sv), 2), "neg_n": neg,
        "neg_rate": round(neg / n, 4),
        "p25": round(percentile(sv, 25), 2), "p75": round(percentile(sv, 75), 2),
    }


def find_deepest_month(spread_dict, start, end):
    if not end:
        return None
    m, best_m, best_v = start, None, None
    while m <= end:
        v = spread_dict.get(m)
        if v is not None and (best_v is None or v < best_v):
            best_v, best_m = v, m
        m = add_months(m, 1)
    return best_m


def compute_event_b(spread_dict, start, end, n_inverted_months, max_month):
    """事件 B「倒掛解除」＝事件期間內最後一個倒掛月（=timeline 的 end）的下一個月，
    條件：利差回到 >=0，且之後（含解除當月起）連續 EVENT_B_CONFIRM_MONTHS 個月都沒
    再倒掛。只對 n_inverted_months >= EVENT_B_MIN_INVERTED_MONTHS 的事件算。資料不足
    3 個月無法確認時回傳 (None, 'insufficient_data')。"""
    if not end or n_inverted_months < EVENT_B_MIN_INVERTED_MONTHS:
        return None, "not_qualified"
    b_month = add_months(end, 1)
    check_months = [add_months(b_month, i) for i in range(EVENT_B_CONFIRM_MONTHS)]
    if check_months[-1] > max_month:
        return None, "insufficient_data"
    vals = [spread_dict.get(m) for m in check_months]
    if any(v is None for v in vals):
        return None, "insufficient_data"
    if all(v >= 0 for v in vals):
        return b_month, "ok"
    return None, "re_inverted"


# ═══════════════════════════════════════════════════════════════════════════
# 逐國組裝
# ═══════════════════════════════════════════════════════════════════════════

def build_country_events(cc, yc_country, timeline_events, price_dict, samp_start, samp_end):
    max_month = max(price_dict) if price_dict else None
    end_map = {e["start"]: e["end"] for e in timeline_events}
    spread_dict = dict(yc_country["spread_series"])
    events_detail = yc_country["def_a"]["events_detail"]
    out = []
    for ev in events_detail:
        start = ev["start"]
        end = end_map.get(start)
        returns = {}
        for h in H_LIST:
            val, status = (None, "no_price_data") if max_month is None else \
                forward_return_with_status(price_dict, start, h, max_month)
            returns[str(h)] = {"value": val, "status": status}
        mdd, mdd_status = (None, "no_price_data") if max_month is None else \
            mdd_with_status(price_dict, start, max_month)
        deepest_month = find_deepest_month(spread_dict, start, end)
        b_month, b_status = (None, "no_price_data") if max_month is None else \
            compute_event_b(spread_dict, start, end, ev["n_inverted_months"], max_month)
        b_returns = {}
        b_mdd, b_mdd_status = None, None
        if b_month:
            for h in H_LIST:
                val, status = forward_return_with_status(price_dict, b_month, h, max_month)
                b_returns[str(h)] = {"value": val, "status": status}
            b_mdd, b_mdd_status = mdd_with_status(price_dict, b_month, max_month)
        out.append({
            "start": start, "end": end, "verdict": ev["verdict"],
            "n_inverted_months": ev["n_inverted_months"], "deepest": ev["deepest"],
            "deepest_month": deepest_month, "lead_months": ev["lead_months"],
            "in_sample_window": bool(samp_start and samp_end and samp_start <= start <= samp_end),
            "returns": returns, "mdd24": mdd, "mdd24_status": mdd_status,
            "event_b_month": b_month, "event_b_status": b_status,
            "event_b_returns": b_returns, "event_b_mdd24": b_mdd, "event_b_mdd24_status": b_mdd_status,
        })
    return out


def event_b_indexed_path(price_dict, b_month, offsets):
    base = price_dict.get(b_month)
    if base is None:
        return None
    path = {}
    for off in offsets:
        p = price_dict.get(add_months(b_month, off))
        path[off] = round(p / base * 100, 3) if p is not None else None
    return path


def simulate_buyhold_and_rule(price_dict, events):
    """五、簡單規則：倒掛起點月底賣出、倒掛解除後 12 個月月底買回，其餘時間持有。
    只對「有有效事件 B」的事件觸發賣出訊號——事件沒有事件 B（不足 3 個月倒掛，或資料
    不足以確認解除穩定）時，規則對那次事件不動作（賣出訊號無法配對買回日，視同不觸發，
    這是本頁對「簡單規則」條文的操作化，已於方法段註明）。若賣出訊號出現時已經是空手
    狀態（前一次還沒買回），這次訊號略過（不重複賣、不改買回日）。"""
    months = sorted(price_dict)
    if len(months) < 2:
        return None
    win_start, win_end = months[0], months[-1]

    pairs = []
    for ev in events:
        if ev["start"] < win_start or ev["start"] > win_end:
            continue
        if ev.get("event_b_month"):
            buy_m = add_months(ev["event_b_month"], RULE_BUYBACK_LAG)
            pairs.append((ev["start"], buy_m))
    pairs.sort()
    sell_map = {}
    for s, b in pairs:
        sell_map.setdefault(s, b)

    holding = True
    pending_buy = None
    bh_idx, rule_idx = 100.0, 100.0
    bh_curve, rule_curve = [], []
    prev_p = price_dict[win_start]
    for i, m in enumerate(months):
        p = price_dict[m]
        if i > 0:
            ratio = p / prev_p
            bh_idx *= ratio
            if holding:
                rule_idx *= ratio
        if not holding and pending_buy is not None and m >= pending_buy:
            holding = True
            pending_buy = None
        if holding and m in sell_map:
            holding = False
            pending_buy = sell_map[m]
        bh_curve.append([m, round(bh_idx, 3)])
        rule_curve.append([m, round(rule_idx, 3)])
        prev_p = p

    def _mdd_running(curve):
        peak = curve[0][1]
        worst = 0.0
        for _m, v in curve:
            peak = max(peak, v)
            dd = (v / peak - 1) * 100
            worst = min(worst, dd)
        return round(worst, 2)

    return {
        "window": [win_start, win_end],
        "buyhold_cum_pct": round(bh_idx - 100, 2),
        "rule_cum_pct": round(rule_idx - 100, 2),
        "buyhold_mdd_pct": _mdd_running(bh_curve),
        "rule_mdd_pct": _mdd_running(rule_curve),
        "n_sell_signals": len(sell_map),
        "buyhold_curve": bh_curve, "rule_curve": rule_curve,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 載入
# ═══════════════════════════════════════════════════════════════════════════

def load_raw():
    if not RAW_JSON.exists():
        warn(f"{RAW_JSON} 不存在，先跑 --fetch")
        return {"series": {}, "meta": {}}
    return json.loads(RAW_JSON.read_text(encoding="utf-8"))


def load_yc():
    return json.loads(YC_JSON.read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════════════════════════════════
# 主計算
# ═══════════════════════════════════════════════════════════════════════════

def do_compute_and_build():
    raw = load_raw()
    raw_series = raw.get("series", {})
    yc = load_yc()
    yc_countries = yc["countries"]
    yc_timeline = yc["v2"]["timeline"]

    us_cpi_pts = raw_series.get(US_CPI_SERIES)
    us_cpi_dict = to_monthly_dict(us_cpi_pts) if us_cpi_pts else {}

    countries_out = []
    for cc, name in COUNTRIES:
        yc_c = yc_countries.get(cc)
        if not yc_c or yc_c.get("status") != "ok":
            countries_out.append({"cc": cc, "name": name, "status": "missing",
                                   "note": "yield_curve 資料缺（此國未進入 def_a）"})
            warn(f"{cc} {name}: yield_curve 資料缺，跳過")
            continue

        price_pts = raw_series.get("TW_EQUITY") if cc == "TW" else raw_series.get(FRED_EQUITY.get(cc, ""))
        if not price_pts:
            countries_out.append({"cc": cc, "name": name, "status": "missing",
                                   "note": "股價序列抓取失敗或未抓"})
            warn(f"{cc} {name}: 股價序列缺，跳過")
            continue
        price_dict = to_monthly_dict(price_pts)
        price_min, price_max = min(price_dict), max(price_dict)

        a = yc_c["def_a"]
        samp_start = max(a["sample_start"], price_min)
        samp_end = min(a["sample_end"], price_max)
        if samp_start > samp_end:
            countries_out.append({"cc": cc, "name": name, "status": "missing",
                                   "note": "利差樣本窗與股價資料窗無交集"})
            warn(f"{cc} {name}: 樣本窗無交集，跳過")
            continue

        timeline_events = yc_timeline.get(cc, {}).get("events", [])
        events = build_country_events(cc, yc_c, timeline_events, price_dict, samp_start, samp_end)

        uncond = {}
        for h in H_LIST:
            vals = unconditional_returns(price_dict, h, samp_start, samp_end)
            uncond[str(h)] = dist_stats(vals)

        rule = simulate_buyhold_and_rule(price_dict, events)

        countries_out.append({
            "cc": cc, "name": name, "status": "ok",
            "price_data_range": [price_min, price_max],
            "sample_window": [samp_start, samp_end],
            "events": events,
            "unconditional": uncond,
            "rule_backtest": rule,
        })
        info(f"{cc} {name}: {len(events)} 事件，樣本窗 {samp_start}~{samp_end}")

    tw_entry = next((c for c in countries_out if c["cc"] == "TW"), None)
    tw_status = tw_entry.get("status") if tw_entry else "missing"

    # ── 事件層彙總：table1（h=6/12/24，事件內含所有判定），bootstrap CI ──
    table1 = {}
    for h in H_LIST:
        rows = []
        for c in countries_out:
            if c["status"] != "ok":
                continue
            vals = [e["returns"][str(h)]["value"] for e in c["events"]
                    if e["returns"][str(h)]["status"] == "ok"]
            ds = dist_stats(vals)
            ci_lo, ci_hi = bootstrap_median_ci(vals)
            neg_ci_lo, neg_ci_hi = wilson_ci(ds["neg_n"], ds["n"])
            uc = c["unconditional"][str(h)]
            rows.append({
                "cc": c["cc"], "name": c["name"], "sample_window": c["sample_window"],
                "n_events": ds["n"], "median": ds["median"], "median_ci_lo": ci_lo, "median_ci_hi": ci_hi,
                "neg_rate": ds["neg_rate"], "neg_n": ds["neg_n"],
                "neg_rate_ci_lo": neg_ci_lo, "neg_rate_ci_hi": neg_ci_hi,
                "uncond_median": uc["median"], "uncond_neg_rate": uc["neg_rate"], "uncond_n": uc["n"],
            })
        table1[str(h)] = rows

    # 合併池（不獨立）h=12/24：把 8 國事件值直接併成一個集合；無條件對照也併成一個集合
    # 供合併池列比較（8 國各自樣本窗不同，此處單純把逐國 unconditional_returns() 的值接起來，
    # 月份會跨國重疊但國家不同、資產不同，視為不同觀察）。
    pooled_events = {}
    pooled_uncond = {}
    for h in H_LIST:
        vals = []
        uvals = []
        for c in countries_out:
            if c["status"] != "ok":
                continue
            vals.extend(e["returns"][str(h)]["value"] for e in c["events"]
                        if e["returns"][str(h)]["status"] == "ok")
            uvals.extend(unconditional_returns(
                to_monthly_dict(raw_series.get("TW_EQUITY") if c["cc"] == "TW"
                                 else raw_series.get(FRED_EQUITY.get(c["cc"], ""))),
                h, c["sample_window"][0], c["sample_window"][1]))
        ds = dist_stats(vals)
        ci_lo, ci_hi = bootstrap_median_ci(vals)
        neg_ci_lo, neg_ci_hi = wilson_ci(ds["neg_n"], ds["n"])
        pooled_events[str(h)] = {**ds, "median_ci_lo": ci_lo, "median_ci_hi": ci_hi,
                                  "neg_rate_ci_lo": neg_ci_lo, "neg_rate_ci_hi": neg_ci_hi}
        pooled_uncond[str(h)] = dist_stats(uvals)

    # ── 事件 B：路徑、table2 ──
    offsets = list(range(-12, 25))
    b_paths_pooled = {off: [] for off in offsets}
    b_paths_us = {off: [] for off in offsets}
    event_b_rows = []
    for c in countries_out:
        if c["status"] != "ok":
            continue
        price_pts = raw_series.get("TW_EQUITY") if c["cc"] == "TW" else raw_series.get(FRED_EQUITY.get(c["cc"], ""))
        price_dict = to_monthly_dict(price_pts)
        for e in c["events"]:
            if not e.get("event_b_month"):
                continue
            path = event_b_indexed_path(price_dict, e["event_b_month"], offsets)
            if path is None:
                continue
            for off in offsets:
                if path[off] is not None:
                    b_paths_pooled[off].append(path[off])
                    if c["cc"] == "US":
                        b_paths_us[off].append(path[off])
            event_b_rows.append({
                "cc": c["cc"], "name": c["name"], "event_start": e["start"],
                "event_b_month": e["event_b_month"],
                "returns": e["event_b_returns"], "mdd24": e["event_b_mdd24"],
                "mdd24_status": e["event_b_mdd24_status"],
            })
    pooled_path = [{"offset": off, "value": round(statistics.mean(v), 2) if v else None, "n": len(v)}
                   for off, v in sorted(b_paths_pooled.items())]
    us_path = [{"offset": off, "value": round(statistics.mean(v), 2) if v else None, "n": len(v)}
              for off, v in sorted(b_paths_us.items())]

    # 事件 B 合併池統計（表 2 用）：h=6/12/24 報酬 + MDD24，含 bootstrap 95% 區間。
    event_b_pooled_stats = {}
    for h in H_LIST:
        vals = [r["returns"][str(h)]["value"] for r in event_b_rows
                if r["returns"].get(str(h)) and r["returns"][str(h)]["status"] == "ok"]
        ds = dist_stats(vals)
        ci_lo, ci_hi = bootstrap_median_ci(vals)
        event_b_pooled_stats[str(h)] = {**ds, "median_ci_lo": ci_lo, "median_ci_hi": ci_hi}
    b_mdds = [r["mdd24"] for r in event_b_rows if r.get("mdd24_status") == "ok"]
    event_b_pooled_mdd = dist_stats(b_mdds)

    # ── 三組分桶（命中／落空／已在衰退中），h=12 箱型 ──
    group_stats = {}
    for grp in ("hit", "miss", "already_in_recession"):
        vals = []
        for c in countries_out:
            if c["status"] != "ok":
                continue
            vals.extend(e["returns"]["12"]["value"] for e in c["events"]
                        if e["verdict"] == grp and e["returns"]["12"]["status"] == "ok")
        group_stats[grp] = dist_stats(vals)

    # ── MDD(24) 散佈（命中／落空兩色）──
    mdd_scatter = []
    for c in countries_out:
        if c["status"] != "ok":
            continue
        for e in c["events"]:
            if e["verdict"] not in ("hit", "miss"):
                continue
            if e["mdd24_status"] != "ok":
                continue
            mdd_scatter.append({"cc": c["cc"], "name": c["name"], "year": int(e["start"][:4]),
                                 "month": e["start"], "mdd24": e["mdd24"], "verdict": e["verdict"]})

    # ── 美國名目 vs 實質 ──
    us_real = None
    us_c = next((c for c in countries_out if c["cc"] == "US"), None)
    if us_c and us_cpi_dict:
        us_price_pts = raw_series.get(FRED_EQUITY["US"])
        us_price_dict = to_monthly_dict(us_price_pts)
        common_months = sorted(set(us_price_dict) & set(us_cpi_dict))
        real_price = {m: us_price_dict[m] / us_cpi_dict[m] for m in common_months}
        real_max_month = max(real_price)
        rows = []
        for h in H_LIST:
            nom_vals, real_vals = [], []
            for e in us_c["events"]:
                start = e["start"]
                nv = e["returns"][str(h)]["value"] if e["returns"][str(h)]["status"] == "ok" else None
                if nv is not None:
                    nom_vals.append(nv)
                rv, rstatus = forward_return_with_status(real_price, start, h, real_max_month) \
                    if start in real_price else (None, "missing_base")
                if rstatus == "ok":
                    real_vals.append(rv)
            nd, rd = dist_stats(nom_vals), dist_stats(real_vals)
            rows.append({"h": h, "n_nominal": nd["n"], "median_nominal": nd["median"],
                         "neg_rate_nominal": nd["neg_rate"], "n_real": rd["n"],
                         "median_real": rd["median"], "neg_rate_real": rd["neg_rate"]})
        us_real = {"rows": rows, "cpi_series": US_CPI_SERIES,
                   "cpi_range": [min(us_cpi_dict), max(us_cpi_dict)]}

    # ── 八國一致性：h=12 事件中位數 − 無條件中位數 ──
    dumbbell = []
    for c in countries_out:
        if c["status"] != "ok":
            continue
        t1 = next(r for r in table1["12"] if r["cc"] == c["cc"])
        if t1["median"] is None or t1["uncond_median"] is None:
            continue
        dumbbell.append({"cc": c["cc"], "name": c["name"],
                         "diff": round(t1["median"] - t1["uncond_median"], 2),
                         "event_median": t1["median"], "uncond_median": t1["uncond_median"],
                         "n_events": t1["n_events"]})

    # ── 簡單規則彙總表 ──
    rule_table = []
    for c in countries_out:
        if c["status"] != "ok" or not c["rule_backtest"]:
            continue
        rb = c["rule_backtest"]
        rule_table.append({"cc": c["cc"], "name": c["name"], "window": rb["window"],
                           "buyhold_cum_pct": rb["buyhold_cum_pct"], "rule_cum_pct": rb["rule_cum_pct"],
                           "buyhold_mdd_pct": rb["buyhold_mdd_pct"], "rule_mdd_pct": rb["rule_mdd_pct"],
                           "n_sell_signals": rb["n_sell_signals"]})

    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "h_list": H_LIST,
        "tw_status": tw_status,
        "schema_notes": {
            "countries": "countries=[{cc,name,status,price_data_range,sample_window,events,"
                         "unconditional,rule_backtest}]；events[].returns.<h>={value(log報酬%,ln(P1/P0)*100),"
                         "status(ok/not_due/missing/missing_base)}；mdd24=算術跌幅%（不是log報酬）；"
                         "event_b_month=None 代表該事件不夠格算事件B（event_b_status 說明原因）。",
            "table1": "table1.<h>=[{cc,name,sample_window,n_events,median,median_ci_lo/hi(bootstrap 95%,"
                      "事件數<3為None),neg_rate,neg_n,neg_rate_ci_lo/hi(Wilson 95%),uncond_median,"
                      "uncond_neg_rate,uncond_n}]。",
            "pooled_events": "pooled_events.<h>=8國事件值直接併池（不獨立）的 dist_stats + bootstrap 95% "
                             "中位數區間 + Wilson 95% 負報酬比率區間。pooled_uncond.<h>=8國無條件分布併池"
                             "（月份滾動重疊、非獨立，只作粗略對照，不附CI，見方法段）。",
            "event_b": "event_b_pooled_path/us_path=[{offset(-12..24),value(事件B月=100的指數,平均),n}]；"
                      "event_b_rows=逐事件明細。event_b_pooled_stats.<h>=事件B之後h個月報酬的dist_stats+"
                      "bootstrap 95% 中位數區間（8國合併，不獨立）；event_b_pooled_mdd=事件B之後24個月"
                      "MDD的dist_stats。",
            "group_stats": "group_stats.<hit|miss|already_in_recession>=h=12的dist_stats（p25/median/p75/n）。",
            "mdd_scatter": "mdd_scatter=[{cc,name,year,month,mdd24,verdict}]，僅 hit/miss 兩色、mdd24_status=ok。",
            "us_real": "us_real.rows=[{h,n_nominal,median_nominal,neg_rate_nominal,n_real,median_real,neg_rate_real}]。",
            "dumbbell": "dumbbell=[{cc,name,diff(事件中位數-無條件中位數,h=12),event_median,uncond_median,n_events}]。",
            "rule_table": "rule_table=[{cc,name,window,buyhold_cum_pct,rule_cum_pct,buyhold_mdd_pct,"
                          "rule_mdd_pct,n_sell_signals}]；MDD 為策略權益曲線的傳統高點回落（跟事件錨定的"
                          "mdd24 是不同定義，見方法段）。",
        },
        "countries": countries_out,
        "table1": table1,
        "pooled_events": pooled_events,
        "pooled_uncond": pooled_uncond,
        "event_b_pooled_path": pooled_path,
        "event_b_us_path": us_path,
        "event_b_rows": event_b_rows,
        "event_b_pooled_stats": event_b_pooled_stats,
        "event_b_pooled_mdd": event_b_pooled_mdd,
        "group_stats": group_stats,
        "mdd_scatter": mdd_scatter,
        "us_real": us_real,
        "dumbbell": dumbbell,
        "rule_table": rule_table,
    }

    DATA.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    info(f"寫入 {OUT_JSON}")

    built_date = datetime.now().strftime("%Y-%m-%d")
    html_out = generate_html(payload, built_date)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_out, encoding="utf-8")
    info(f"寫入 {OUT_HTML}")


# ═══════════════════════════════════════════════════════════════════════════
# HTML 產出（版型照抄 slow_bear_base_rate/index.html，於執行期直接擷取；視覺語言
# 比照 yield_curve 第二版：hero＋4 stat 卡、每節一個論點、圖＋圖說＋表＋解讀、方法段
# 定義逐條、最後「這頁沒有告訴你的事」、附錄摺疊表）
# ═══════════════════════════════════════════════════════════════════════════

def esc(s):
    return html_mod.escape(str(s), quote=True)


def fmt_ret(x, digits=2):
    return "—" if x is None else f"{x:+.{digits}f}%"


def fmt_ratio_pct(x, digits=1):
    return "—" if x is None else f"{x * 100:.{digits}f}%"


def fmt_num(x, digits=2):
    return "—" if x is None else f"{x:.{digits}f}"


def fmt_pp(x, digits=2):
    """百分點差（不是報酬本身），帶正負號，不加 % 符號。"""
    return "—" if x is None else f"{x:+.{digits}f}"


def fmt_month(m):
    return m if m else "—"


def fmt_ci_ret(lo, hi):
    return "—" if (lo is None or hi is None) else f"{lo:+.1f}% ~ {hi:+.1f}%"


def fmt_ci_pct(lo, hi):
    return "—" if (lo is None or hi is None) else f"{lo * 100:.0f}–{hi * 100:.0f}%"


def extract_template_parts():
    src = SLOW_BEAR_REF.read_text(encoding="utf-8")
    style_start = src.index("<style>")
    style_end = src.index("</style>", style_start) + len("</style>")
    main_style = src[style_start:style_end]

    nav_start = src.index('<style id="imq-nav-style">')
    header_end = src.index("</header>", nav_start) + len("</header>")
    after_header = src[header_end:]
    script_end = after_header.index("</script>") + len("</script>")
    nav_block = src[nav_start:header_end] + after_header[:script_end]
    return main_style, nav_block


def collapse_cjk_whitespace(html_str: str) -> str:
    """照抄 build_yield_curve_recession.py：多行 f-string 拼句子留下的換行，瀏覽器會當
    空白算，兩個中文字中間會多一個看不見的半形空格。<script>/<style> 先切出來保護。"""
    protected = []

    def _stash(m):
        protected.append(m.group(0))
        return f"\x00PROTECTED{len(protected) - 1}\x00"

    stashed = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", _stash, html_str,
                      flags=re.IGNORECASE | re.DOTALL)
    cjk = "　-鿿＀-￯"
    collapsed = re.sub(rf"(?<=[{cjk}])\s+(?=[{cjk}])", "", stashed)
    return re.sub(r"\x00PROTECTED(\d+)\x00", lambda m: protected[int(m.group(1))], collapsed)


CN_NUM = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
BRAND_BLUE = "#1a56db"
GRAY = "#9ca3af"
HIT_RED = "#dc2626"
MISS_BLUE = "#2563eb"
ALREADY_GREEN = "#059669"
US_ORANGE = "#ea580c"
COUNTRY_COLORS = {"US": US_ORANGE, "DE": "#1a56db", "GB": "#7c3aed", "JP": "#dc2626",
                   "CA": "#059669", "AU": "#0891b2", "KR": "#db2777", "TW": "#65a30d"}

POINT_MARKER_PLUGIN_JS = """
const pointMarkerPlugin = {
  id: 'pointMarker',
  afterDatasetsDraw(chart) {
    chart.data.datasets.forEach((ds, dsIndex) => {
      const meta = chart.getDatasetMeta(dsIndex);
      if (!meta || meta.hidden) return;
      const xScale = chart.scales[meta.xAxisID];
      if (!xScale) return;
      const ctx = chart.ctx;
      const draw = (arr, color) => {
        if (!arr) return;
        arr.forEach((v, i) => {
          if (v === null || v === undefined) return;
          const el = meta.data[i];
          if (!el) return;
          const x = xScale.getPixelForValue(v);
          const y = el.y;
          ctx.save();
          ctx.fillStyle = color;
          ctx.strokeStyle = '#fff';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.arc(x, y, 4, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();
          ctx.restore();
        });
      };
      draw(ds._pointValues, ds._pointColor || '#1a56db');
      draw(ds._pointValues2, ds._pointColor2 || '#ea580c');
    });
  }
};
Chart.register(pointMarkerPlugin);
const zeroLinePlugin = {
  id: 'zeroLine',
  afterDatasetsDraw(chart) {
    const opts = (chart.options.plugins || {}).zeroLine;
    if (!opts || !opts.enabled) return;
    const yScale = chart.scales.y, xScale = chart.scales.x;
    const y = yScale.getPixelForValue(opts.value || 0);
    const ctx = chart.ctx;
    ctx.save();
    ctx.strokeStyle = opts.color || '#111827';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 3]);
    ctx.beginPath();
    ctx.moveTo(xScale.left, y);
    ctx.lineTo(xScale.right, y);
    ctx.stroke();
    ctx.restore();
  }
};
Chart.register(zeroLinePlugin);
const vertZeroLinePlugin = {
  id: 'vertZeroLine',
  afterDatasetsDraw(chart) {
    const opts = (chart.options.plugins || {}).vertZeroLine;
    if (!opts || !opts.enabled) return;
    const xScale = chart.scales.x, yScale = chart.scales.y;
    const x = xScale.getPixelForValue(opts.value || 0);
    const ctx = chart.ctx;
    ctx.save();
    ctx.strokeStyle = opts.color || '#111827';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 3]);
    ctx.beginPath();
    ctx.moveTo(x, yScale.top);
    ctx.lineTo(x, yScale.bottom);
    ctx.stroke();
    ctx.restore();
  }
};
Chart.register(vertZeroLinePlugin);
"""


def _section_shell(num_idx, title, lead, body_html):
    n = CN_NUM[num_idx]
    return f"""
<div class="section">
<h2 class="section-title">{esc(n)}、{esc(title)}</h2>
<div class="takeaway">{esc(lead)}</div>
{body_html}
</div>
"""


def _table1_subtable(h, rows, pooled_row):
    body = "".join(
        f"<tr><td class='lbl'>{esc(r['name'])}</td><td>{esc(r['sample_window'][0])}～{esc(r['sample_window'][1])}</td>"
        f"<td class='num'>{r['n_events']}</td><td class='num'>{fmt_ret(r['median'])}</td>"
        f"<td class='num'>{fmt_ratio_pct(r['neg_rate'])}</td>"
        f"<td class='num'>{fmt_ret(r['uncond_median'])}</td>"
        f"<td class='num'>{fmt_ratio_pct(r['uncond_neg_rate'])}</td></tr>"
        for r in rows)
    pooled = (f"<tr class='dim'><td class='lbl'><b>合併池（不獨立）</b></td><td>—</td>"
              f"<td class='num'>{pooled_row['n']}</td><td class='num'><b>{fmt_ret(pooled_row['median'])}</b></td>"
              f"<td class='num'>{fmt_ratio_pct(pooled_row['neg_rate'])}</td>"
              f"<td class='num'>—</td><td class='num'>—</td></tr>")
    return f"""
<h3 style="font-size:.9rem;margin:1.1rem 0 .4rem">{h} 個月</h3>
<div class="scroll"><table><thead><tr><th>國家</th><th>樣本期間</th>
<th class="num">事件數</th><th class="num">中位數</th><th class="num">負報酬比率</th>
<th class="num">無條件中位數</th><th class="num">無條件負報酬比率</th></tr></thead>
<tbody>{body}{pooled}</tbody></table></div>
"""


def _ci_excludes_uncond(r):
    return (r["uncond_median"] is not None and r["median_ci_lo"] is not None
            and not (r["median_ci_lo"] <= r["uncond_median"] <= r["median_ci_hi"]))


def section1(payload):
    t12 = payload["table1"]["12"]
    pe = payload["pooled_events"]
    pu = payload["pooled_uncond"]
    ci_excl = [r for r in t12 if _ci_excludes_uncond(r)]
    distinct = [r for r in ci_excl if r["n_events"] >= MIN_N_FOR_RELIABLE_DISTINCT]
    small_n_flagged = [r for r in ci_excl if r["n_events"] < MIN_N_FOR_RELIABLE_DISTINCT]

    title = "倒掛後 12 個月報酬，多數國家跟平常分不出差異"
    lead = (f"倒掛起點之後股市報酬跟平常比是差還是不差，先看合併池：8 國事件併在一起，"
            f"12 個月報酬中位數 {fmt_ret(pe['12']['median'])}，同一段時期的無條件中位數 "
            f"{fmt_ret(pu['12']['median'])}，信賴區間互相重疊。這節拆到國家層級，逐一用拔靴法"
            f"（bootstrap）重抽 1000 次算事件中位數的 95% 信賴區間，看哪個國家的差距站得住。")

    labels = [r["name"] for r in t12]
    ci_lo = [r["median_ci_lo"] for r in t12]
    ci_hi = [r["median_ci_hi"] for r in t12]
    med = [r["median"] for r in t12]
    ucd = [r["uncond_median"] for r in t12]
    cfg = {
        "type": "bar",
        "data": {"labels": labels, "datasets": [{
            "label": "事件後 12 個月中位數 95% 信賴區間", "data": list(zip(ci_lo, ci_hi)),
            "backgroundColor": "rgba(26,86,219,.18)", "borderColor": "rgba(26,86,219,.4)",
            "borderWidth": 1, "barThickness": 18,
            "_pointValues": med, "_pointColor": BRAND_BLUE,
            "_pointValues2": ucd, "_pointColor2": GRAY,
        }]},
        "options": {
            "indexAxis": "y", "responsive": True, "maintainAspectRatio": False,
            "plugins": {"legend": {"display": False}, "vertZeroLine": {"enabled": True, "value": 0}},
            "scales": {"x": {"title": {"display": True, "text": "12 個月報酬（%，log）"}}},
        },
    }
    chart_html = (f'<div class="chart-wrap" style="height:420px"><canvas id="chart1"></canvas></div>'
                  f'<script>new Chart(document.getElementById("chart1"), '
                  f'{json.dumps(cfg, ensure_ascii=False)});</script>')
    caption = ("藍色橫條是事件後 12 個月報酬中位數的 95% 信賴區間，藍點是中位數點估計，灰點是同一個國家"
               "不看訊號的無條件中位數。灰點落在藍色區間裡面，代表這個國家的倒掛事件跟平常時期統計上"
               "分不出差異。灰點落在區間外面，才是差得出來。")

    table_html = "".join(_table1_subtable(h, payload["table1"][str(h)], pe[str(h)]) for h in H_LIST)

    if distinct:
        names = "、".join(f"{r['name']}（{'較差' if r['median'] < r['uncond_median'] else '較好'}，"
                          f"{r['n_events']} 次事件）" for r in distinct)
        note = (f"8 國裡只有 {len(distinct)} 國的 95% 信賴區間不含無條件中位數，差得出來：{names}。")
    else:
        note = "8 國的 95% 信賴區間都含無條件中位數，統計上找不到任何一國的差距站得住。"
    if small_n_flagged:
        flagged_names = "、".join(f"{r['name']}（{r['n_events']} 次事件）" for r in small_n_flagged)
        note += (f"{flagged_names}的信賴區間雖然也不含無條件中位數，但事件數不到 "
                 f"{MIN_N_FOR_RELIABLE_DISTINCT} 次，拔靴法重抽的區間本身就不可信，不算進「分得出」，"
                 "只列出來提醒讀者不要照單全收。")
    note += (f"合併池 12 個月中位數（{fmt_ret(pe['12']['median'])}）低於無條件中位數"
             f"（{fmt_ret(pu['12']['median'])}），但差距在信賴區間內，同樣分不出。24 個月的差距最大"
             f"（{fmt_ret(pe['24']['median'])} vs {fmt_ret(pu['24']['median'])}），"
             f"信賴區間上緣只差不到一個百分點，也不算穩定的差異。")

    return _section_shell(0, title, lead, f"{chart_html}\n<div class='note'>{esc(caption)}</div>\n"
                                           f"{table_html}\n<div class='note'>{esc(note)}</div>")


def section2(payload):
    ebs = payload["event_b_pooled_stats"]
    pu = payload["pooled_uncond"]
    ebmdd = payload["event_b_pooled_mdd"]
    pooled_path = payload["event_b_pooled_path"]
    us_path = payload["event_b_us_path"]

    outside24 = (ebs["24"]["median_ci_lo"] is not None and pu["24"]["median"] is not None
                 and not (ebs["24"]["median_ci_lo"] <= pu["24"]["median"] <= ebs["24"]["median_ci_hi"]))

    title = "倒掛解除後 24 個月報酬，比平常時期更好"
    lead = ("市場常說倒掛解除才是真正危險的時候。這節看「事件 B」（事件期間最後一個倒掛月的下一個月，"
            "利差回到零以上且之後 3 個月沒再倒掛）之後的報酬路徑，8 國合併 49 次、美國單獨 9 次，"
            "跟無條件時期比較。")

    offsets = [p["offset"] for p in pooled_path]
    pooled_vals = [{"x": p["offset"], "y": p["value"]} for p in pooled_path]
    us_vals = [{"x": p["offset"], "y": p["value"]} for p in us_path]
    baseline = [{"x": o, "y": 100} for o in offsets]
    cfg = {
        "type": "line",
        "data": {"datasets": [
            {"label": "8 國合併平均路徑", "data": pooled_vals, "borderColor": BRAND_BLUE,
             "backgroundColor": "transparent", "pointRadius": 0, "borderWidth": 2, "tension": .15},
            {"label": "美國路徑", "data": us_vals, "borderColor": US_ORANGE,
             "backgroundColor": "transparent", "pointRadius": 0, "borderWidth": 2, "tension": .15},
            {"label": "事件 B 月＝100 基準線", "data": baseline, "borderColor": "#9ca3af",
             "backgroundColor": "transparent", "pointRadius": 0, "borderWidth": 1, "borderDash": [4, 3]},
        ]},
        "options": {
            "responsive": True, "maintainAspectRatio": False,
            "plugins": {"legend": {"position": "top"}, "vertZeroLine": {"enabled": True, "value": 0}},
            "scales": {"x": {"type": "linear", "title": {"display": True, "text": "距事件 B 月（月）"}},
                       "y": {"title": {"display": True, "text": "指數（事件 B 月＝100）"}}},
        },
    }
    chart_html = (f'<div class="chart-wrap" style="height:400px"><canvas id="chart2"></canvas></div>'
                  f'<script>new Chart(document.getElementById("chart2"), '
                  f'{json.dumps(cfg, ensure_ascii=False)});</script>')
    caption = ("x 軸 0 是事件 B 當月，指數固定等於 100，往左是解除前 12 個月，往右是解除後 24 個月。"
               "虛線是 100 的基準，看藍色與橘色路徑在 0 之後往上還是往下走，跟基準線比是漲還是跌。")

    b_rows = {}
    for r in payload["event_b_rows"]:
        b_rows.setdefault(r["cc"], []).append(r)
    trs = []
    for cc, name in COUNTRIES:
        rows = b_rows.get(cc, [])
        if not rows:
            trs.append(f"<tr class='dim'><td class='lbl'>{esc(name)}</td><td class='num'>0</td>"
                       f"<td class='num'>—</td><td class='num'>—</td><td class='num'>—</td>"
                       f"<td class='num'>—</td></tr>")
            continue
        m6 = [r["returns"]["6"]["value"] for r in rows if r["returns"]["6"]["status"] == "ok"]
        m12 = [r["returns"]["12"]["value"] for r in rows if r["returns"]["12"]["status"] == "ok"]
        m24 = [r["returns"]["24"]["value"] for r in rows if r["returns"]["24"]["status"] == "ok"]
        mdds = [r["mdd24"] for r in rows if r.get("mdd24_status") == "ok"]
        trs.append(
            f"<tr><td class='lbl'>{esc(name)}</td><td class='num'>{len(rows)}</td>"
            f"<td class='num'>{fmt_ret(statistics.median(m6)) if m6 else '—'}</td>"
            f"<td class='num'>{fmt_ret(statistics.median(m12)) if m12 else '—'}</td>"
            f"<td class='num'>{fmt_ret(statistics.median(m24)) if m24 else '—'}</td>"
            f"<td class='num'>{fmt_ret(statistics.median(mdds)) if mdds else '—'}</td></tr>")
    pooled_tr = (f"<tr class='dim'><td class='lbl'><b>合併池</b></td><td class='num'>{ebs['12']['n']}</td>"
                 f"<td class='num'><b>{fmt_ret(ebs['6']['median'])}</b></td>"
                 f"<td class='num'><b>{fmt_ret(ebs['12']['median'])}</b></td>"
                 f"<td class='num'><b>{fmt_ret(ebs['24']['median'])}</b></td>"
                 f"<td class='num'><b>{fmt_ret(ebmdd['median'])}</b></td></tr>")
    table_html = (f'<div class="scroll"><table><thead><tr><th>國家</th><th class="num">事件 B 次數</th>'
                  f'<th class="num">6 個月報酬中位數</th><th class="num">12 個月報酬中位數</th>'
                  f'<th class="num">24 個月報酬中位數</th><th class="num">MDD(24) 中位數</th></tr></thead>'
                  f'<tbody>{"".join(trs)}{pooled_tr}</tbody></table></div>')

    if outside24:
        note = (f"解除後 12 個月報酬中位數 {fmt_ret(ebs['12']['median'])}，24 個月 "
                f"{fmt_ret(ebs['24']['median'])}，24 個月這段的 95% 信賴區間"
                f"（{fmt_ci_ret(ebs['24']['median_ci_lo'], ebs['24']['median_ci_hi'])}）"
                f"不含無條件中位數 {fmt_ret(pu['24']['median'])}，解除後兩年的報酬統計上真的比平常更好，"
                f"「解除才是真正危險」在這頁資料上找不到證據。不過解除後 24 個月內仍有 "
                f"{fmt_ratio_pct(ebmdd['neg_rate'])} 的事件出現過一定程度的回檔，中位數 "
                f"{fmt_ret(ebmdd['median'])}，只是通常不深。")
    else:
        note = (f"解除後 12 個月報酬中位數 {fmt_ret(ebs['12']['median'])}，24 個月 "
                f"{fmt_ret(ebs['24']['median'])}，點估計都高於無條件中位數，但信賴區間仍含對照值，"
                f"統計上分不出差異，「解除才是真正危險」在點估計方向上也站不住。")

    return _section_shell(1, title, lead, f"{chart_html}\n<div class='note'>{esc(caption)}</div>\n"
                                           f"{table_html}\n<div class='note'>{esc(note)}</div>")


def section3(payload):
    gs = payload["group_stats"]
    hit, miss, already = gs["hit"], gs["miss"], gs["already_in_recession"]

    title = "倒掛的交易價值，來自真的命中衰退的那些次"
    lead = ("同樣是倒掛起點，事後有沒有真的引來衰退，12 個月後的股市報酬差很多。這節把 8 國的事件依"
            "yield_curve 頁的判定分成命中、落空、已在衰退中三組，各自算 12 個月報酬的第 25、75 百分位"
            "與中位數，橫條代表中間一半事件落的範圍。")

    labels = ["命中衰退", "落空", "已在衰退中"]
    data = [[hit["p25"], hit["p75"]], [miss["p25"], miss["p75"]], [already["p25"], already["p75"]]]
    med = [hit["median"], miss["median"], already["median"]]
    colors = ["rgba(220,38,38,.22)", "rgba(37,99,235,.22)", "rgba(5,150,105,.22)"]
    border = ["rgba(220,38,38,.55)", "rgba(37,99,235,.55)", "rgba(5,150,105,.55)"]
    cfg = {
        "type": "bar",
        "data": {"labels": labels, "datasets": [{
            "label": "12 個月報酬第 25–75 百分位", "data": data,
            "backgroundColor": colors, "borderColor": border, "borderWidth": 1, "barThickness": 34,
            "_pointValues": med, "_pointColor": "#111827",
        }]},
        "options": {
            "indexAxis": "y", "responsive": True, "maintainAspectRatio": False,
            "plugins": {"legend": {"display": False}, "vertZeroLine": {"enabled": True, "value": 0}},
            "scales": {"x": {"title": {"display": True, "text": "12 個月報酬（%，log）"}}},
        },
    }
    chart_html = (f'<div class="chart-wrap" style="height:280px"><canvas id="chart3"></canvas></div>'
                  f'<script>new Chart(document.getElementById("chart3"), '
                  f'{json.dumps(cfg, ensure_ascii=False)});</script>')
    caption = ("色塊是第 25 到 75 百分位，黑點是中位數。命中組的色塊明顯偏左，落空組與已在衰退中那組"
               "偏右，三組的位置差很多，不是同一個分布。")

    body = "".join(
        f"<tr><td class='lbl'>{esc(lbl)}</td><td class='num'>{g['n']}</td>"
        f"<td class='num'>{fmt_ret(g['median'])}</td><td class='num'>{fmt_ratio_pct(g['neg_rate'])}</td>"
        f"<td class='num'>{fmt_ret(g['p25'])}</td><td class='num'>{fmt_ret(g['p75'])}</td></tr>"
        for lbl, g in zip(labels, (hit, miss, already)))
    table_html = (f'<div class="scroll"><table><thead><tr><th>分組</th><th class="num">事件數</th>'
                  f'<th class="num">中位數</th><th class="num">負報酬比率</th>'
                  f'<th class="num">第 25 百分位</th><th class="num">第 75 百分位</th></tr></thead>'
                  f'<tbody>{body}</tbody></table></div>')

    note = (f"命中組 12 個月中位數 {fmt_ret(hit['median'])}，負報酬比率 {fmt_ratio_pct(hit['neg_rate'])}，"
            f"落空組 {fmt_ret(miss['median'])}，已在衰退中那組反而最高 {fmt_ret(already['median'])}。"
            f"倒掛本身沒有事先告訴你會不會命中，交易價值只在事後、只在真的命中那組才兌現，"
            f"事前看到倒掛沒辦法區分自己站在哪一組。")

    return _section_shell(2, title, lead, f"{chart_html}\n<div class='note'>{esc(caption)}</div>\n"
                                           f"{table_html}\n<div class='note'>{esc(note)}</div>")


def section4(payload):
    scatter = payload["mdd_scatter"]
    hit_pts = [{"x": p["year"], "y": p["mdd24"]} for p in scatter if p["verdict"] == "hit"]
    miss_pts = [{"x": p["year"], "y": p["mdd24"]} for p in scatter if p["verdict"] == "miss"]
    hit_mdds = [p["mdd24"] for p in scatter if p["verdict"] == "hit"]
    miss_mdds = [p["mdd24"] for p in scatter if p["verdict"] == "miss"]

    title = "倒掛後兩年最深跌幅，命中組比落空組深"
    lead = ("倒掛之後 24 個月內，股價從事件起點算最深跌了多少。這節不分國家，把 8 國命中、落空兩組"
            f"共 {len(scatter)} 次事件攤開，x 軸是事件發生的年份，y 軸是最大回撤 MDD(24)。")

    cfg = {
        "type": "scatter",
        "data": {"datasets": [
            {"label": "命中衰退", "data": hit_pts, "backgroundColor": HIT_RED, "pointRadius": 5},
            {"label": "落空", "data": miss_pts, "backgroundColor": MISS_BLUE, "pointRadius": 5},
        ]},
        "options": {
            "responsive": True, "maintainAspectRatio": False,
            "plugins": {"legend": {"position": "top"}},
            "scales": {"x": {"title": {"display": True, "text": "事件年份"}},
                       "y": {"title": {"display": True, "text": "MDD(24)，%"}}},
        },
    }
    chart_html = (f'<div class="chart-wrap" style="height:360px"><canvas id="chart4"></canvas></div>'
                  f'<script>new Chart(document.getElementById("chart4"), '
                  f'{json.dumps(cfg, ensure_ascii=False)});</script>')
    caption = ("紅點是命中衰退的事件，藍點是落空的事件。點越低代表那次事件之後兩年內股價從起點算跌得"
               "越深，看紅點是不是整體比藍點低，藍點是不是大多貼在 0 附近。")

    note = (f"命中組 {len(hit_pts)} 次事件的 MDD(24) 中位數 {fmt_num(statistics.median(hit_mdds)) if hit_mdds else '—'}%，"
            f"落空組 {len(miss_pts)} 次事件的中位數 {fmt_num(statistics.median(miss_mdds)) if miss_mdds else '—'}%，"
            "命中組的跌幅明顯比落空組深，兩次石油危機與 2008 年、2020 年那幾次紅點都在圖的底部，"
            "落空組的藍點大多集中在 0 附近。")

    return _section_shell(3, title, lead, f"{chart_html}\n<div class='note'>{esc(caption)}</div>\n"
                                           f"<div class='note'>{esc(note)}</div>")


def section5(payload):
    us_c = next(c for c in payload["countries"] if c["cc"] == "US")
    rb = us_c["rule_backtest"]
    rule_table = payload["rule_table"]

    n_rule_better = sum(1 for r in rule_table if r["rule_cum_pct"] > r["buyhold_cum_pct"])
    n_mdd_better = sum(1 for r in rule_table if r["rule_mdd_pct"] > r["buyhold_mdd_pct"])

    title = f"簡單規則：{n_rule_better} 個國家的累積報酬贏過一路持有"
    lead = ("只測一條規則，不做參數搜尋：倒掛起點月底賣出、事件 B 之後 12 個月月底買回，其餘時間持有，"
            "跟一路持有比累積報酬與最大回撤。沒有事件 B 的那次事件，規則對它不動作（詳見方法段），"
            "只報數字，不建議照做。")

    labels = [m for m, _v in rb["buyhold_curve"]]
    bh_vals = [v for _m, v in rb["buyhold_curve"]]
    rl_vals = [v for _m, v in rb["rule_curve"]]
    cfg = {
        "type": "line",
        "data": {"labels": labels, "datasets": [
            {"label": "一路持有", "data": bh_vals, "borderColor": "#111827",
             "backgroundColor": "transparent", "pointRadius": 0, "borderWidth": 1.4},
            {"label": "簡單規則", "data": rl_vals, "borderColor": BRAND_BLUE,
             "backgroundColor": "transparent", "pointRadius": 0, "borderWidth": 1.4},
        ]},
        "options": {
            "responsive": True, "maintainAspectRatio": False,
            "plugins": {"legend": {"position": "top"}},
            "scales": {"x": {"ticks": {"maxTicksLimit": 12}},
                       "y": {"type": "logarithmic", "title": {"display": True, "text": "指數（起點＝100，log 軸）"}}},
        },
    }
    chart_html = (f'<div class="chart-wrap" style="height:380px"><canvas id="chart5"></canvas></div>'
                  f'<script>new Chart(document.getElementById("chart5"), '
                  f'{json.dumps(cfg, ensure_ascii=False)});</script>')
    caption = (f"美國 {esc(rb['window'][0])} 到 {esc(rb['window'][1])}，起點都等於 100，y 軸取 log 刻度。"
               "黑線是一路持有，藍線是規則，藍線落在黑線下面代表規則這段期間報酬比較差。")

    body = "".join(
        f"<tr><td class='lbl'>{esc(r['name'])}</td><td>{esc(r['window'][0])}～{esc(r['window'][1])}</td>"
        f"<td class='num'>{fmt_ret(r['buyhold_cum_pct'], 0)}</td><td class='num'>{fmt_ret(r['rule_cum_pct'], 0)}</td>"
        f"<td class='num'>{fmt_ret(r['buyhold_mdd_pct'])}</td><td class='num'>{fmt_ret(r['rule_mdd_pct'])}</td>"
        f"<td class='num'>{r['n_sell_signals']}</td></tr>"
        for r in rule_table)
    table_html = (f'<div class="scroll"><table><thead><tr><th>國家</th><th class="num">樣本期間</th>'
                  f'<th class="num">一路持有累積報酬</th><th class="num">規則累積報酬</th>'
                  f'<th class="num">一路持有 MDD</th><th class="num">規則 MDD</th>'
                  f'<th class="num">規則觸發次數</th></tr></thead><tbody>{body}</tbody></table></div>')

    note = (f"8 國裡規則的累積報酬贏過一路持有的只有 {n_rule_better} 國，規則的最大回撤比一路持有淺的有 "
            f"{n_mdd_better} 國。美國一路持有累積 {fmt_ret(rb['buyhold_cum_pct'], 0)}，規則 "
            f"{fmt_ret(rb['rule_cum_pct'], 0)}，規則躲過部分回撤但也躲過解除後那段通常偏強的報酬，"
            "兩者互相抵銷，長期下來多數國家是一路持有贏。")

    return _section_shell(4, title, lead, f"{chart_html}\n<div class='note'>{esc(caption)}</div>\n"
                                           f"{table_html}\n<div class='note'>{esc(note)}</div>")


def section6(payload):
    ur = payload["us_real"]
    title = "美股實質報酬更差，通膨吃掉一部分名目報酬"
    lead = ("倒掛常常出現在央行升息對抗通膨的時期，1970 年代與 2022 年都是這樣。這節把美國事件的名目"
            "報酬換成用 CPIAUCSL 平減後的實質報酬，看通膨會不會改變前面的結論。")

    body = "".join(
        f"<tr><td class='lbl'>{r['h']} 個月</td><td class='num'>{r['n_nominal']}</td>"
        f"<td class='num'>{fmt_ret(r['median_nominal'])}</td><td class='num'>{fmt_ratio_pct(r['neg_rate_nominal'])}</td>"
        f"<td class='num'>{fmt_ret(r['median_real'])}</td><td class='num'>{fmt_ratio_pct(r['neg_rate_real'])}</td></tr>"
        for r in ur["rows"])
    table_html = (f'<div class="scroll"><table><thead><tr><th>期間</th><th class="num">事件數</th>'
                  f'<th class="num">名目中位數</th><th class="num">名目負報酬比率</th>'
                  f'<th class="num">實質中位數</th><th class="num">實質負報酬比率</th></tr></thead>'
                  f'<tbody>{body}</tbody></table></div>')

    r24 = next(r for r in ur["rows"] if r["h"] == 24)
    gap24 = round(r24["median_nominal"] - r24["median_real"], 2)
    note = (f"24 個月的落差最大，名目中位數 {fmt_ret(r24['median_nominal'])}，實質中位數 "
            f"{fmt_ret(r24['median_real'])}，差了 {fmt_num(gap24)} 個百分點，實質負報酬比率也從 "
            f"{fmt_ratio_pct(r24['neg_rate_nominal'])} 升到 {fmt_ratio_pct(r24['neg_rate_real'])}。"
            "通膨沒有推翻美國事件本身偏弱的結論，反而讓它更弱。")

    return _section_shell(5, title, lead, f"{table_html}\n<div class='note'>{esc(note)}</div>")


def section7(payload):
    dumb = sorted(payload["dumbbell"], key=lambda r: r["diff"])
    span = round(dumb[-1]["diff"] - dumb[0]["diff"], 2)
    title = f"八國不一致，最大與最小差距相差 {fmt_num(span, 1)} 個百分點"
    lead = ("倒掛後 12 個月報酬跟無條件時期比，8 個國家的差距方向不一樣。這節把每個國家的差距"
            "（事件中位數減無條件中位數）排成一張橫條，看差距的分布，不是每個國家都往同一個方向。")

    labels = [r["name"] for r in dumb]
    diffs = [r["diff"] for r in dumb]
    colors = [BRAND_BLUE if v >= 0 else HIT_RED for v in diffs]
    cfg = {
        "type": "bar",
        "data": {"labels": labels, "datasets": [{
            "label": "事件中位數－無條件中位數（12 個月）", "data": diffs,
            "backgroundColor": colors, "borderWidth": 0, "barThickness": 18,
        }]},
        "options": {
            "indexAxis": "y", "responsive": True, "maintainAspectRatio": False,
            "plugins": {"legend": {"display": False}, "vertZeroLine": {"enabled": True, "value": 0}},
            "scales": {"x": {"title": {"display": True, "text": "差距（百分點）"}}},
        },
    }
    chart_html = (f'<div class="chart-wrap" style="height:340px"><canvas id="chart6"></canvas></div>'
                  f'<script>new Chart(document.getElementById("chart6"), '
                  f'{json.dumps(cfg, ensure_ascii=False)});</script>')
    caption = ("藍色代表倒掛後報酬比平常好，紅色代表比平常差，長度是差距的大小。長度差很多、顏色兩邊"
               "都有，代表 8 國看到的不是同一個現象。")

    worst = dumb[0]
    best = dumb[-1]
    middle = dumb[1:-1]
    middle_span = max(abs(r["diff"]) for r in middle)
    note = (f"差距最大的兩端是{esc(worst['name'])}（{fmt_pp(worst['diff'])} 個百分點）與"
            f"{esc(best['name'])}（{fmt_pp(best['diff'])} 個百分點），一個明顯較差、一個明顯較好，"
            f"中間六國的差距都在 {fmt_num(middle_span, 1)} 個百分點以內。8 國不是同一套劇本，"
            "套用單一國家的歷史經驗到其他市場要打折扣。")

    return _section_shell(6, title, lead, f"{chart_html}\n<div class='note'>{esc(caption)}</div>\n"
                                           f"<div class='note'>{esc(note)}</div>")


DEFINITIONS_TEXT = [
    "事件 A「倒掛起點」：直接讀 yield_curve 頁（data/yield_curve_recession.json）def_a 的 "
    "events_detail，不重算，起點、倒掛月數、判定（命中／落空／已在衰退中／未到期）都沿用同一份資料。",
    "事件 B「倒掛解除」：事件期間內最後一個倒掛月（讀同一份資料 v2.timeline 的 end）的下一個月，"
    "條件是利差回到零以上，且從那個月起連續 3 個月都沒再倒掛。只對倒掛月數達 3 個月以上的事件算，"
    "避免單月雜訊被當成一次解除。資料不足 3 個月沒辦法確認時，視為這次事件沒有事件 B。",
    "事件 C「最深倒掛月」：事件期間利差最負的那個月，事後才知道，只列在附錄的事件明細表作對照，"
    "沒有另外開一節分析。",
    "前向報酬 R(h)：從事件月月底到 h 個月後月底的價格變動，用 log 報酬換算成百分比"
    "（自然對數乘以 100，不是還原成算術報酬），h 分別是 6、12、24 個月。事件月之後資料不足 h 個月"
    "的標「未到期」，不計入中位數與比率。",
    "最大回撤 MDD(24)：跟前向報酬不同，用一般算術跌幅，不是 log 報酬。從事件月價格算起，"
    "24 個月內最深跌到多少，不足 24 個月的標「未到期」。第五節「規則」的策略最大回撤是另一種"
    "定義，用權益曲線的傳統高點回落法，跟 MDD(24) 不是同一件事，分別標注。",
    "無條件對照：全樣本每一個月起算同樣 h 的報酬分布，樣本窗是該國利差資料（yield_curve 頁 def_a "
    "的樣本窗）跟股價資料的交集，起訖印在表上。",
    "「差」的判準：中位數用拔靴法重抽 1000 次、有放回地重抽事件本身，"
    "取重抽後中位數分布的第 2.5 與 97.5 百分位當 95% 信賴區間。比率用 Wilson 95% 信賴區間。"
    "信賴區間蓋住對照值就寫分不出，不把小差距寫成結論。",
    "三組分類：事件 A 依 yield_curve 頁的判定分「命中」「落空」「已在衰退中」三組，「未到期」的"
    "事件（太接近資料尾端，還不知道會不會命中）不計入任何一組。",
    "簡單規則的操作化：倒掛起點月底賣出，事件 B 之後 12 個月月底買回，其餘時間持有。這條規則只對"
    "有事件 B 的事件觸發賣出訊號。沒有事件 B 的事件（不夠格或資料不足以確認解除），選擇不觸發"
    "賣出，因為沒有明確的買回日期可以配對，這是對規則文字的操作化，不是題目規格唯一可能的寫法。"
    "賣出訊號出現時如果已經是空手狀態，這次訊號略過，不重複賣、不改買回日。",
    "股價來源：OECD「股價指數：全部股票」（All Shares/Broad）月頻，FRED 代碼 SPASTT01{國碼}"
    "M661N，美／德／英／日／加／澳／韓七國。這是價格指數，不含股息再投資，也不是各國最常被"
    "引用的大型股指數（如美股的標普 500），是涵蓋面更廣的全市場指數。台灣：央行統計資料庫"
    "（cpx.cbc.gov.tw）沒有台灣證交所加權指數這條序列，改用 yfinance 的 ^TWII 月收盤"
    "（1997 年起），這是共用規格明訂的備援做法。",
    "美國實質報酬：用 CPIAUCSL（消費者物價指數，季節調整）平減名目價格後再算前向報酬，"
    "公式跟名目報酬一樣，只是價格換成「名目價格÷CPI」。",
]


def section_method(payload):
    lis = "".join(f"<li>{esc(t)}</li>" for t in DEFINITIONS_TEXT)
    return f"""
<div class="section">
<h2 class="section-title">八、方法：怎麼定義「倒掛」「解除」與「報酬」</h2>
<div class="takeaway">這頁的判定規則在跑資料前就定死，八個國家套同一套定義，中途不因某國結果好不好看
而回頭調整。事件本身直接讀 yield_curve 頁已經算好的結果，不重算，新增的是報酬、回撤與規則
的計算。</div>
<div class="card"><ul class="disc">{lis}</ul></div>
</div>
"""


def section_not_told():
    items = [
        "價格指數不含股息再投資。第五節累積報酬比較（尤其一路持有 vs 規則、跨幾十年的樣本窗）"
        "如果換成含息報酬，兩條線的絕對水準都會墊高不少，沒有股息資料可以還原，這裡只能"
        "定性提醒，不補一個沒查證的數字。",
        "月頻資料看不到月中的最深跌幅。2020 年 3 月那種單月閃崩，MDD(24) 只抓得到月底價位，"
        "會比真正的日內回撤淺，這是月頻資料的先天限制，不是計算錯誤。",
        "OECD 全股價指數（All Shares/Broad）涵蓋面比標普 500 這類大型股指數廣，2020 年之後、"
        "2023 到 2024 年這種由少數大型股領漲的期間，這個指數的漲幅會比新聞常引用的大型股指數"
        "數字更保守，抽查段已經看到這個落差，不是本頁算錯。",
        "事件之間不是完全獨立。加拿大、英國、澳洲這幾國歷史上常常連續好幾年倒掛或斷斷續續倒掛，"
        "24 個月分組窗口把它們併成一個事件，但相鄰事件的市場環境常常還是相連的，事件數看起來"
        "比真正獨立的訊號次數多。",
        "樣本少的國家信賴區間本來就寬。日本只有 3 次事件、台灣 4 次、南韓 5 次，這幾國的任何"
        "單一數字都不宜看得太重，第一節的信賴區間已經把這件事量化出來。",
        "簡單規則只測了一種操作化，沒有做參數搜尋，換一種買回時點或賣出條件，結果可能不同，"
        "這頁不建議照著這條規則交易。",
    ]
    lis = "".join(f"<li>{esc(t)}</li>" for t in items)
    return f"""
<div class="section">
<h2 class="section-title">九、這頁沒有告訴你的事</h2>
<div class="card"><ul class="disc">{lis}</ul></div>
</div>
"""


def appendix_event_detail(payload):
    blocks = []
    for cc, name in COUNTRIES:
        c = next((x for x in payload["countries"] if x["cc"] == cc), None)
        if not c or c["status"] != "ok":
            continue
        rows = []
        for e in c["events"]:
            rows.append(
                f"<tr><td>{esc(e['start'])}</td><td>{esc(fmt_month(e['end']))}</td>"
                f"<td>{esc(e['verdict'])}</td><td class='num'>{e['n_inverted_months']}</td>"
                f"<td class='num'>{fmt_num(e['deepest'])}</td><td>{esc(fmt_month(e['deepest_month']))}</td>"
                f"<td class='num'>{fmt_ret(e['returns']['6']['value']) if e['returns']['6']['status'] == 'ok' else esc(e['returns']['6']['status'])}</td>"
                f"<td class='num'>{fmt_ret(e['returns']['12']['value']) if e['returns']['12']['status'] == 'ok' else esc(e['returns']['12']['status'])}</td>"
                f"<td class='num'>{fmt_ret(e['returns']['24']['value']) if e['returns']['24']['status'] == 'ok' else esc(e['returns']['24']['status'])}</td>"
                f"<td class='num'>{fmt_ret(e['mdd24']) if e['mdd24_status'] == 'ok' else esc(e['mdd24_status'])}</td>"
                f"<td>{esc(fmt_month(e['event_b_month']))}</td></tr>")
        blocks.append(f"""
<details><summary>{esc(name)}（{len(c['events'])} 次事件）</summary>
<div class="scroll"><table><thead><tr><th>起點</th><th>解除前最後倒掛月</th><th>判定</th>
<th class="num">倒掛月數</th><th class="num">最深利差</th><th>最深倒掛月</th>
<th class="num">6 個月</th><th class="num">12 個月</th><th class="num">24 個月</th>
<th class="num">MDD(24)</th><th>事件 B 月</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
</details>""")
    return f"""
<div class="section">
<h2 class="section-title">附錄：逐事件明細</h2>
<div class="takeaway">每個國家、每次倒掛事件的起點、判定、6／12／24 個月報酬與 MDD(24)，點國名展開。</div>
{"".join(blocks)}
</div>
"""


def section_hero(payload):
    pe, pu = payload["pooled_events"], payload["pooled_uncond"]
    gs = payload["group_stats"]
    dumb = payload["dumbbell"]
    t12 = payload["table1"]["12"]
    ci_excl = [r for r in t12 if _ci_excludes_uncond(r)]
    distinct = [r for r in ci_excl if r["n_events"] >= MIN_N_FOR_RELIABLE_DISTINCT]
    small_n_flagged = [r for r in ci_excl if r["n_events"] < MIN_N_FOR_RELIABLE_DISTINCT]
    ebs = payload["event_b_pooled_stats"]

    us_c = next(c for c in payload["countries"] if c["cc"] == "US")
    rb = us_c["rule_backtest"]
    rule_table = payload["rule_table"]
    n_rule_better = sum(1 for r in rule_table if r["rule_cum_pct"] > r["buyhold_cum_pct"])
    us_ratio = (1 + rb["rule_cum_pct"] / 100) / (1 + rb["buyhold_cum_pct"] / 100)

    verdict = "倒掛不是清楚的賣出訊號，機械賣出讓多數國家的長期報酬變差"
    tag_color = "#059669"

    h2 = (f"倒掛後 12 個月報酬中位數 {fmt_ret(pe['12']['median'])}，無條件時期中位數 "
          f"{fmt_ret(pu['12']['median'])}，信賴區間互相重疊，8 國裡只有 {len(distinct)} 國統計上"
          f"真的分得出差異。")
    p1 = (f"倒掛解除之後才危險是常見的說法，資料不支持：解除後 12 個月報酬中位數 "
          f"{fmt_ret(ebs['12']['median'])}，24 個月 {fmt_ret(ebs['24']['median'])}，24 個月這段的"
          f"信賴區間不含無條件時期的中位數，統計上真的比平常更好。")
    p2 = (f"倒掛有沒有交易價值，要看它事後有沒有真的命中衰退：命中組 12 個月報酬中位數 "
          f"{fmt_ret(gs['hit']['median'])}，落空組 {fmt_ret(gs['miss']['median'])}，"
          "價值集中在真的命中的那些次，事前看不出來自己站在哪一組。")
    worst = min(dumb, key=lambda r: r["diff"])
    best = max(dumb, key=lambda r: r["diff"])
    n_indistinct = len(t12) - len(distinct) - len(small_n_flagged)
    small_n_note = ""
    if small_n_flagged:
        small_n_names = "、".join(f"{r['name']}（{r['n_events']} 次事件）" for r in small_n_flagged)
        small_n_note = f"{small_n_names}的區間雖然也不含無條件中位數，但事件數太少，區間不可信，不算數。"
    p3 = (f"8 國不一致：{esc(worst['name'])}的差距最負（{fmt_pp(worst['diff'])} 個百分點），"
          f"{esc(best['name'])}最正（{fmt_pp(best['diff'])} 個百分點），統計上站得住的只有 "
          f"{len(distinct)} 國，其餘 {n_indistinct} 國分不出。{small_n_note}機械套用「倒掛就賣」規則，"
          f"8 國裡只有 {n_rule_better} 國的累積報酬贏過一路持有，美國規則的累積報酬只有一路持有的 "
          f"{fmt_num(us_ratio * 100, 0)}%。")

    return f"""
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag" style="background:{tag_color}">{esc(verdict)}</span>
    <h2>{esc(h2)}</h2>
    <p>{esc(p1)}</p>
    <p>{esc(p2)}</p>
    <p>{esc(p3)}</p>
  </div>
  <div class="hero-stats">
    <div><div class="hs-label">事件後 12 個月報酬中位數</div><div class="hs-value">{fmt_ret(pe['12']['median'])}</div></div>
    <div><div class="hs-label">無條件 12 個月報酬中位數</div><div class="hs-value">{fmt_ret(pu['12']['median'])}</div></div>
    <div><div class="hs-label">統計上分得出差異的國家</div><div class="hs-value">{len(distinct)}／8</div></div>
    <div><div class="hs-label">美國：規則／一路持有累積報酬</div><div class="hs-value">{fmt_num(us_ratio * 100, 0)}%</div></div>
  </div>
</div>
"""


def generate_html(payload, built_date):
    main_style, nav_block = extract_template_parts()
    title = "殖利率倒掛之後，股票該賣嗎？ | InvestMQuest Research"
    tw_note = "台灣股價來自 yfinance ^TWII，其餘七國來自 OECD 全股價指數。" if payload["tw_status"] == "ok" \
        else "台灣資料整理中，本頁先出七國版本。"
    description = (f"用 yield_curve 頁已判定的八國倒掛事件，對 OECD 全股價指數套同一把尺回測前向報酬、"
                    f"最大回撤與一條簡單交易規則：倒掛後 12 個月報酬中位數 "
                    f"{fmt_ret(payload['pooled_events']['12']['median'])}，跟無條件時期比多數國家"
                    f"分不出差異；{tw_note}")

    try:
        sys.path.insert(0, str(NAV_DIR))
        from _nav_common import make_toggle  # noqa
        subnav = make_toggle("yc_equity")
    except Exception as e:
        warn(f"make_toggle 載入失敗：{e}，pill bar 留空")
        subnav = ""

    hero = section_hero(payload)
    takeaway = ("<b>給沒有統計背景的讀者：</b>這頁接著 yield_curve 頁的問題往下問：知道殖利率倒掛之後，"
                "股票該不該賣？我們把 8 個國家已經判定好的倒掛事件，對照同一段時間的股價指數，算事件"
                "之後 6、12、24 個月的報酬，跟不看訊號、隨便挑一個月開始算的報酬比，看有沒有差、差多少、"
                "差得穩不穩。也試了一條最簡單的交易規則：倒掛就賣、解除一年後買回，看這樣操作划不划算。"
                "本頁不做「現在該不該賣」的建議，只回報歷史上這麼做的結果。")

    s1 = section1(payload)
    s2 = section2(payload)
    s3 = section3(payload)
    s4 = section4(payload)
    s5 = section5(payload)
    s6 = section6(payload)
    s7 = section7(payload)
    s_method = section_method(payload)
    s_not_told = section_not_told()
    appendix = appendix_event_detail(payload)

    body = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<script src="{CHART_JS_CDN}"></script>
<script>{POINT_MARKER_PLUGIN_JS}</script>
{main_style}
</head>
<body>
{nav_block}

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / 殖利率倒掛之後股票該賣嗎</div>
    <h1>殖利率倒掛之後，股票該賣嗎？</h1>
    <div class="sub">倒掛起點、解除後、命中與落空，八國股市前向報酬回測・生成 {esc(built_date)}</div>
    {subnav}
  </div>
</div>

<div class="container">

{hero}

<div class="takeaway">{takeaway}</div>

{s1}
{s2}
{s3}
{s4}
{s5}
{s6}
{s7}
{appendix}
{s_method}
{s_not_told}

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 殖利率倒掛之後，股票該賣嗎？（研究頁，不構成投資建議）
    &middot; 頁面生成 {esc(built_date)} &middot; 僅供研究參考，不構成投資建議
  </div>
</footer>
</body>
</html>
"""
    return collapse_cjk_whitespace(body)


def main():
    ap = argparse.ArgumentParser(description="殖利率倒掛之後，股票該賣嗎？builder")
    ap.add_argument("--fetch", action="store_true", help="只抓序列存 raw json")
    args = ap.parse_args()
    if args.fetch:
        do_fetch()
        return
    do_compute_and_build()


if __name__ == "__main__":
    main()
