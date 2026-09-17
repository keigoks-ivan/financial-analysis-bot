#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_first_cut.py — 央行第一次降息之後，股市是漲是跌？（跨國回測，八國同一把尺）。

規格凍結版：問「升息循環結束後第一次降息，之後 6／12／24 個月股市報酬如何？有沒有衰退是不是
比降息本身更重要？降息前市場是不是已經先反應？八國一致嗎？」用 OECD 隔夜／即期利率（美國主線
FEDFUNDS）與 OECD 股價指數（不含股息）對 US/DE/GB/JP/CA/AU/KR 七國套同一套規則，台灣另用央行
統計資料庫「中央銀行利率（重貼現率）」與「股票交易與股價指數（加權平均股價指數）」。

定義凍結（第 2 節，不可改；某國若無法執行照原定義做並在輸出／回報中如實標註，不換定義）：
    - 月利率序列先取 3 個月移動平均（trailing MA，要求三個月連續，缺月不補）。
    - 升息循環＝利率 3 個月均值從低點上升 ≥1.00pp（低點到高點期間 ≤36 個月）。低點採「事發時
      點回溯 36 個月內的滾動最低值」，不是狀態機重置後的最近低點——這樣 1994-95 升息循環在
      1997 年利率仍高掛時，1997 年的小波段高點依然能被判定為「升息循環後的高點」，才能讓
      1998 年那波（先前只小升 0.25pp 就被降息打斷）被正確歸位成「高點之後的第一次降息」，
      而不是被漏算。詳見方法段。
    - 循環高點＝升息循環後（局部）的最高月（利率序列由升轉降的轉折點）。
    - 第一次降息＝高點之後第一個「3 個月均值比高點低 ≥0.25pp」的月份，且高點到該月不超過 18
      個月（超過視為沒有降息循環、循環作廢，不登記事件）。
    - 事件＝第一次降息月。同一波高點群組（24 個月內）只留最高的一個高點對應的事件（沿用
      detect_events 的事件分組思路）。
    - 分組：事件月起前 6 個月到後 12 個月的區間，若與定義 A 技術性衰退區間重疊 →「有衰退」，
      否則「無衰退」。美國另用 NBER 分一次對照。
    - 前向報酬 R(h)，h=6/12/24，從事件月月底起算，log 報酬換算成百分比；另算 R(-6)。
    - 無條件對照＝該國全樣本逐月同 h 報酬分布（中位數、負報酬比率、第 25／75 百分位）。
    - 政策利率後續路徑＝事件後 12 個月利率總降幅（高點值減高點後 12 個月的 3 個月均值）。
    - MDD(12)＝事件月起 12 個月內（含事件月，共 13 個月點）最深跌幅。
    - 樣本窗＝該國利率與股價兩者都有資料的期間，起訖印在表上；事件月落在樣本窗外的不計入。

用法：
    python3 scripts/build_first_cut.py --fetch   抓 FRED＋台灣央行 cpx 序列存
                                                  data/first_cut_raw.json。
    python3 scripts/build_first_cut.py           讀 raw json＋data/yield_curve_recession.json
                                                  （八國技術性衰退區間，直接讀不重算），算全部
                                                  統計，寫 data/first_cut.json，生成
                                                  docs/backtest/first_cut/index.html（版型／CSS／
                                                  imq-nav 從 build_yield_curve_recession 模組
                                                  import，不改該檔）。
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_JSON = DATA / "first_cut_raw.json"
OUT_JSON = DATA / "first_cut.json"
YC_JSON = DATA / "yield_curve_recession.json"
OUT_HTML = ROOT / "docs" / "backtest" / "first_cut" / "index.html"
NAV_DIR = ROOT / "docs" / "backtest"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_yield_curve_recession as ycr  # noqa: E402  照共用規格：直接 import 不改該檔

SCHEMA = "first-cut-v1"
CHART_JS_CDN = ycr.CHART_JS_CDN


def warn(msg: str) -> None:
    print(f"[first_cut][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[first_cut] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 國家與序列代碼（第 1 節；OECD 隔夜／即期利率、OECD 股價指數，已用 curl 逐條驗證存在）
# ═══════════════════════════════════════════════════════════════════════════

COUNTRIES = [
    ("US", "美國", dict(rate="FEDFUNDS", stock="SPASTT01USM661N")),
    ("DE", "德國", dict(rate="IRSTCI01DEM156N", stock="SPASTT01DEM661N")),
    ("GB", "英國", dict(rate="IRSTCI01GBM156N", stock="SPASTT01GBM661N")),
    ("JP", "日本", dict(rate="IRSTCI01JPM156N", stock="SPASTT01JPM661N")),
    ("CA", "加拿大", dict(rate="IRSTCI01CAM156N", stock="SPASTT01CAM661N")),
    ("AU", "澳洲", dict(rate="IRSTCI01AUM156N", stock="SPASTT01AUM661N")),
    ("KR", "南韓", dict(rate="IRSTCI01KRM156N", stock="SPASTT01KRM661N")),
]
US_NBER = "USRECDM"

# 台灣：中央銀行統計資料庫 API（curl 直接回整張表 JSON）。
#   利率：https://cpx.cbc.gov.tw/api/dataapi/Get?FileName=EG2AM01
#     （29.利率 A.中央銀行利率依期間；Table1=[重貼現率,擔保放款融通利率,短期融通]，
#      dataSets 每列 = [月份, 重貼現率, 擔保放款融通利率, 短期融通]，取欄位 1＝重貼現率）
#   股價：https://cpx.cbc.gov.tw/api/dataapi/Get?FileName=EG27M01
#     （28.股票市場統計 B.股票交易與股價指數依期間；Table1×Table2＝6 指標×[原始值,年增率]，
#      dataSets 每列 13 欄＝[月份, ...11 個中間值..., 加權平均股價指數原始值, 年增率]，
#      取欄位 11＝加權平均股價指數原始值）
TW_RATE_FILE = "EG2AM01"
TW_RATE_COL = 1
TW_STOCK_FILE = "EG27M01"
TW_STOCK_COL = 11

HIKE_THRESHOLD = 1.00       # pp，升息循環的低點到高點門檻
CUT_THRESHOLD = 0.25        # pp，第一次降息的門檻
CYCLE_MAX_MONTHS = 36       # 低點到高點的最長月數
CUT_MAX_MONTHS = 18         # 高點到第一次降息的最長月數
EVENT_GROUP_MONTHS = 24     # 同一波高點群組視窗（沿用 detect_events 思路）
WINDOW_PRE = 6               # 分組視窗：事件前 6 個月
WINDOW_POST = 12             # 分組視窗：事件後 12 個月
H_LIST = [6, 12, 24]
PRIMARY_H = 12


# ═══════════════════════════════════════════════════════════════════════════
# 抓取
# ═══════════════════════════════════════════════════════════════════════════

def fetch_cpx(filename: str):
    """央行統計資料庫 REST：https://cpx.cbc.gov.tw/api/dataapi/Get?FileName=<px檔名>
    直接回整張表 JSON（curl 即可，見 macro_common.md）。"""
    import requests
    url = f"https://cpx.cbc.gov.tw/api/dataapi/Get?FileName={filename}"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        warn(f"cpx {filename}: {e}")
        return None


def do_fetch():
    series_ids = set()
    for _cc, _name, codes in COUNTRIES:
        series_ids.add(codes["rate"])
        series_ids.add(codes["stock"])
    series_ids.add(US_NBER)

    out = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "series": {}, "meta": {}, "tw": {}}
    ok, fail = 0, 0
    for sid in sorted(series_ids):
        pts = ycr.fetch_fred(sid)
        if pts is None:
            warn(f"{sid}: 抓取失敗或無資料")
            out["meta"][sid] = {"ok": False, "n": 0}
            fail += 1
            continue
        out["series"][sid] = pts
        out["meta"][sid] = {"ok": True, "n": len(pts), "start": pts[0][0], "end": pts[-1][0]}
        info(f"{sid}: {len(pts)} 筆 {pts[0][0]}..{pts[-1][0]}")
        ok += 1

    tw_rate = fetch_cpx(TW_RATE_FILE)
    tw_stock = fetch_cpx(TW_STOCK_FILE)
    out["tw"] = {
        "rate_raw": tw_rate, "rate_file": TW_RATE_FILE, "rate_col": TW_RATE_COL,
        "rate_source_url": f"https://cpx.cbc.gov.tw/api/dataapi/Get?FileName={TW_RATE_FILE}",
        "stock_raw": tw_stock, "stock_file": TW_STOCK_FILE, "stock_col": TW_STOCK_COL,
        "stock_source_url": f"https://cpx.cbc.gov.tw/api/dataapi/Get?FileName={TW_STOCK_FILE}",
    }
    if tw_rate:
        info(f"TW 重貼現率（{TW_RATE_FILE}）：{len(tw_rate.get('data', {}).get('dataSets', []))} 筆")
    else:
        warn("TW 重貼現率抓取失敗")
    if tw_stock:
        info(f"TW 加權平均股價指數（{TW_STOCK_FILE}）：{len(tw_stock.get('data', {}).get('dataSets', []))} 筆")
    else:
        warn("TW 股價指數抓取失敗")

    DATA.mkdir(parents=True, exist_ok=True)
    RAW_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    info(f"寫入 {RAW_JSON}：{ok} 成功／{fail} 失敗（FRED）")
    if fail:
        warn(f"{fail} 條 FRED 序列抓取失敗，見上方 WARN")


def load_raw():
    if not RAW_JSON.exists():
        warn(f"{RAW_JSON} 不存在，先跑 --fetch")
        return {}
    return json.loads(RAW_JSON.read_text(encoding="utf-8"))


def load_yc_recession():
    if not YC_JSON.exists():
        warn(f"{YC_JSON} 不存在，無法取得定義 A 衰退區間")
        return {}
    return json.loads(YC_JSON.read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════════════════════════════════
# 台灣 cpx 表格解析
# ═══════════════════════════════════════════════════════════════════════════

def _cpx_month_to_iso(s: str) -> str:
    """"1988M01" -> "1988-01"。"""
    y, m = s.split("M")
    return f"{y}-{m}"


def parse_cpx_series(raw_table, col_idx: int) -> dict:
    """cpx dataapi 回傳的 JSON-stat 風格表格 -> {month: value}，跳過 "-"（缺值）。"""
    if not raw_table:
        return {}
    rows = raw_table.get("data", {}).get("dataSets", [])
    out = {}
    for row in rows:
        if len(row) <= col_idx:
            continue
        raw_v = row[col_idx]
        if raw_v in (None, "-", ""):
            continue
        try:
            v = float(raw_v)
        except ValueError:
            continue
        out[_cpx_month_to_iso(row[0])] = v
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 第一次降息事件偵測（第 2 節定義，凍結）
# ═══════════════════════════════════════════════════════════════════════════

def three_month_ma(series: dict) -> dict:
    """3 個月移動平均（trailing，要求三個月連續，缺月不補）。"""
    months = sorted(series)
    out = {}
    for i, m in enumerate(months):
        if i < 2:
            continue
        m0, m1, m2 = months[i - 2], months[i - 1], months[i]
        if ycr.month_diff(m1, m0) != 1 or ycr.month_diff(m2, m1) != 1:
            continue
        out[m2] = (series[m0] + series[m1] + series[m2]) / 3.0
    return out


def _trailing_min(ma: dict, ma_months: list, i: int, lookback: int = CYCLE_MAX_MONTHS):
    m = ma_months[i]
    lo = None
    for j in range(i, -1, -1):
        m2 = ma_months[j]
        if ycr.month_diff(m, m2) > lookback:
            break
        v = ma[m2]
        if lo is None or v < lo:
            lo = v
    return lo


def _local_peaks(ma: dict, ma_months: list) -> list:
    """局部高點（轉折點：利率由升轉降前的最後一個月）。"""
    peaks = []
    direction = None
    for i in range(1, len(ma_months)):
        m0, m1 = ma_months[i - 1], ma_months[i]
        v0, v1 = ma[m0], ma[m1]
        if v1 > v0:
            newdir = "up"
        elif v1 < v0:
            newdir = "down"
        else:
            newdir = direction
        if direction is None:
            direction = newdir
            continue
        if newdir is not None and newdir != direction:
            if direction == "up":
                peaks.append(m0)
            direction = newdir
    return peaks


def detect_first_cut_events(ma: dict) -> list:
    """回傳 [{peak_month, peak_val, cut_month, cut_val}, ...]，已依 24 個月分組去重
    （同一波高點群組只留最高的一個高點）。"""
    ma_months = sorted(ma)
    peaks = _local_peaks(ma, ma_months)
    peak_idx = {m: i for i, m in enumerate(ma_months)}
    candidates = []
    for pm in peaks:
        i = peak_idx[pm]
        lo = _trailing_min(ma, ma_months, i)
        if lo is None or ma[pm] - lo < HIKE_THRESHOLD:
            continue
        pv = ma[pm]
        found = None
        for j in range(i + 1, len(ma_months)):
            m2 = ma_months[j]
            if ma[m2] <= pv - CUT_THRESHOLD:
                found = m2
                break
        if found is None:
            continue  # 尚未觸發降息（升息循環仍在進行或資料已到尾端）
        diff = ycr.month_diff(found, pm)
        if diff <= CUT_MAX_MONTHS:
            candidates.append({"peak_month": pm, "peak_val": round(pv, 4),
                                "cut_month": found, "cut_val": round(ma[found], 4)})
        # diff > 18：循環作廢，不登記事件（定義凍結）

    if not candidates:
        return []
    candidates.sort(key=lambda e: e["peak_month"])
    groups = []
    i = 0
    while i < len(candidates):
        start = candidates[i]["peak_month"]
        group = [candidates[i]]
        j = i + 1
        while j < len(candidates) and ycr.month_diff(candidates[j]["peak_month"], start) <= EVENT_GROUP_MONTHS:
            group.append(candidates[j])
            j += 1
        groups.append(group)
        i = j
    return [max(g, key=lambda e: e["peak_val"]) for g in groups]


# ═══════════════════════════════════════════════════════════════════════════
# 衰退分組、前向報酬、MDD、無條件對照
# ═══════════════════════════════════════════════════════════════════════════

def overlaps_recession(event_month: str, spans: list, pre=WINDOW_PRE, post=WINDOW_POST) -> bool:
    """事件月前 pre 個月到後 post 個月的區間，是否與任一衰退區間（半開區間 [start,end)）重疊。"""
    win_start = ycr.month_index(event_month) - pre
    win_end = ycr.month_index(event_month) + post
    for s, e in spans:
        s_idx = ycr.month_index(s)
        e_idx = ycr.month_index(e) if e else None
        if s_idx <= win_end and (e_idx is None or e_idx > win_start):
            return True
    return False


RECESSION_GROUPS = ["no_recession", "recession_after", "recession_during"]
RECESSION_GROUP_LABEL = {"no_recession": "無衰退", "recession_after": "衰退之後才開始",
                          "recession_during": "降息時已在衰退中"}
RECESSION_GROUP_COLOR = {"no_recession": None, "recession_after": "#d97706", "recession_during": "#dc2626"}


def classify_recession_group(event_month: str, spans: list, pre=WINDOW_PRE, post=WINDOW_POST) -> str:
    """三組分類（2026-09-17 協調者指示，取代原本「有衰退／無衰退」二分）。優先序：
    1. recession_during（降息時已在衰退中）：事件月本身落在任一衰退區間內（半開區間 [start,end)，
       這已經涵蓋「衰退起點在事件前 pre 個月內且尚未結束」的情況，兩者邏輯等價：只要衰退起點
       ≤ 事件月且還沒結束，事件月必然落在區間內）。事件前 pre 個月內雖有衰退重疊、但那段衰退在
       事件月之前就已經結束（殘餘重疊，不含事件月本身）也歸這組，因為市場當下剛走出衰退、離
       谷底更近，比「無衰退」或「衰退之後才開始」更貼近「已在衰退中」的處境。
    2. recession_after（衰退之後才開始）：不屬於第 1 類，且有衰退區間的起點落在事件月之後、
       事件月 + post 個月內。
    3. no_recession：事件前 pre 個月到事件後 post 個月的視窗內完全沒有衰退區間重疊。
    """
    if ycr.in_any_span(event_month, spans):
        return "recession_during"
    event_idx = ycr.month_index(event_month)
    win_start = event_idx - pre
    win_end = event_idx + post
    any_overlap = False
    starts_after = False
    for s, e in spans:
        s_idx = ycr.month_index(s)
        e_idx = ycr.month_index(e) if e else None
        if s_idx <= win_end and (e_idx is None or e_idx > win_start):
            any_overlap = True
        if event_idx < s_idx <= win_end:
            starts_after = True
    if starts_after:
        return "recession_after"
    if any_overlap:
        return "recession_during"
    return "no_recession"


def _log_ret_pct(p0, p1):
    if p0 is None or p1 is None or p0 <= 0 or p1 <= 0:
        return None
    return round(math.log(p1 / p0) * 100.0, 2)


def event_forward_returns(price: dict, event_month: str) -> dict:
    out = {}
    for h in H_LIST:
        m2 = ycr.add_months(event_month, h)
        out[f"r{h}"] = _log_ret_pct(price.get(event_month), price.get(m2))
    m_pre = ycr.add_months(event_month, -6)
    out["r_pre6"] = _log_ret_pct(price.get(m_pre), price.get(event_month))
    return out


def mdd_12(price: dict, event_month: str):
    months = [ycr.add_months(event_month, k) for k in range(0, 13)]
    vals = [price.get(m) for m in months]
    if any(v is None for v in vals):
        return None
    peak = vals[0]
    mdd = 0.0
    for v in vals:
        if v > peak:
            peak = v
        dd = v / peak - 1.0
        if dd < mdd:
            mdd = dd
    return round(mdd * 100.0, 2)


def event_index_path(price: dict, event_month: str, pre=6, post=24):
    """事件月＝100 的相對指數路徑，offset -pre..+post；缺值填 None。"""
    base = price.get(event_month)
    if not base or base <= 0:
        return None
    path = []
    for k in range(-pre, post + 1):
        m = ycr.add_months(event_month, k)
        v = price.get(m)
        path.append(None if v is None else round(v / base * 100.0, 3))
    return path


def unconditional_raw(price: dict, h: int, sample_start: str, sample_end: str) -> list:
    months = sorted(m for m in price if sample_start <= m <= sample_end)
    rets = []
    for m in months:
        m2 = ycr.add_months(m, h)
        if m2 in price:
            r = _log_ret_pct(price[m], price[m2])
            if r is not None:
                rets.append(r)
    return rets


def summarize_returns(vals: list) -> dict:
    vals = [v for v in vals if v is not None]
    n = len(vals)
    if n == 0:
        return {"n": 0, "median": None, "neg_rate": None, "neg_n": 0,
                "neg_ci_low": None, "neg_ci_high": None, "p25": None, "p75": None}
    sv = sorted(vals)
    median = round(statistics.median(sv), 2)
    neg_n = sum(1 for v in sv if v < 0)
    neg_rate = round(neg_n / n, 4)
    lo, hi = ycr.wilson_ci(neg_n, n)
    if n >= 4:
        qs = statistics.quantiles(sv, n=4)
        p25, p75 = round(qs[0], 2), round(qs[2], 2)
    else:
        p25, p75 = round(sv[0], 2), round(sv[-1], 2)
    return {"n": n, "median": median, "neg_rate": neg_rate, "neg_n": neg_n,
            "neg_ci_low": lo, "neg_ci_high": hi, "p25": p25, "p75": p75}


# ═══════════════════════════════════════════════════════════════════════════
# 單一國家組裝
# ═══════════════════════════════════════════════════════════════════════════

def build_country(cc, name, codes, raw_series, recession_spans, us_nber_spans=None):
    rate_pts = raw_series.get(codes["rate"])
    stock_pts = raw_series.get(codes["stock"])
    missing = [k for k, v in [("rate", rate_pts), ("stock", stock_pts)] if not v]
    if missing:
        return {"cc": cc, "name": name, "status": "missing", "missing_series": missing}

    rate_m = ycr.to_monthly_dict(rate_pts)
    price_m = ycr.to_monthly_dict(stock_pts)
    return _build_country_common(cc, name, rate_m, price_m, recession_spans, us_nber_spans)


def build_taiwan(tw_raw, recession_spans):
    rate_m = parse_cpx_series(tw_raw.get("rate_raw"), tw_raw.get("rate_col", TW_RATE_COL))
    price_m = parse_cpx_series(tw_raw.get("stock_raw"), tw_raw.get("stock_col", TW_STOCK_COL))
    if len(rate_m) < 24 or len(price_m) < 24:
        return {"cc": "TW", "name": "台灣", "status": "partial",
                "note": f"重貼現率 {len(rate_m)} 筆、加權平均股價指數 {len(price_m)} 筆，不足 24 筆",
                "rate_source_url": tw_raw.get("rate_source_url"),
                "stock_source_url": tw_raw.get("stock_source_url")}
    d = _build_country_common("TW", "台灣", rate_m, price_m, recession_spans, None)
    d["rate_source_url"] = tw_raw.get("rate_source_url")
    d["stock_source_url"] = tw_raw.get("stock_source_url")
    return d


def _build_country_common(cc, name, rate_m, price_m, recession_spans, us_nber_spans):
    ma = three_month_ma(rate_m)
    events_raw = detect_first_cut_events(ma)

    rate_start, rate_end = min(rate_m), max(rate_m)
    price_start, price_end = min(price_m), max(price_m)
    sample_start = max(rate_start, price_start)
    sample_end = min(rate_end, price_end)

    uncond = {}
    for h in H_LIST:
        rets = unconditional_raw(price_m, h, sample_start, sample_end)
        uncond[h] = summarize_returns(rets)

    events = []
    for ev in events_raw:
        cm = ev["cut_month"]
        if cm < sample_start or cm > sample_end:
            continue  # 事件月不在有價格資料的樣本窗內，跳過（不硬湊資料）
        rec_group = classify_recession_group(cm, recession_spans)
        has_rec_nber = overlaps_recession(cm, us_nber_spans) if us_nber_spans is not None else None
        rets = event_forward_returns(price_m, cm)
        mdd = mdd_12(price_m, cm)
        rate_decline_12 = None
        m12 = ycr.add_months(ev["peak_month"], 12)
        if m12 in ma:
            rate_decline_12 = round(ev["peak_val"] - ma[m12], 4)
        path = event_index_path(price_m, cm)
        events.append({
            "peak_month": ev["peak_month"], "peak_val": ev["peak_val"],
            "event_month": cm, "event_val": ev["cut_val"],
            "recession_group": rec_group, "has_recession_nber": has_rec_nber,
            "rate_decline_12m": rate_decline_12,
            "r6": rets["r6"], "r12": rets["r12"], "r24": rets["r24"], "r_pre6": rets["r_pre6"],
            "mdd12": mdd, "index_path": path,
        })

    return {"cc": cc, "name": name, "status": "ok",
            "sample_start": sample_start, "sample_end": sample_end,
            "rate_range": [rate_start, rate_end], "price_range": [price_start, price_end],
            "events": events, "unconditional": uncond,
            "price_series_tail": sorted(price_m.items())[-1] if price_m else None,
            "_price_m": price_m}  # 內部欄位，寫 JSON 前會剔除，供 pooled 無條件對照重算用


# ═══════════════════════════════════════════════════════════════════════════
# 主流程（先只算＋dump JSON，驗過數字再接 HTML）
# ═══════════════════════════════════════════════════════════════════════════

def do_compute():
    raw = load_raw()
    raw_series = raw.get("series", {})
    tw_raw = raw.get("tw", {})
    yc = load_yc_recession()
    yc_countries = yc.get("countries", {})

    us_nber_pts = raw_series.get(US_NBER)
    us_nber_spans = None
    if us_nber_pts:
        us_nber_spans, _starts = ycr.recession_transitions(us_nber_pts)

    countries_data = []
    for cc, name, codes in COUNTRIES:
        rec_spans = yc_countries.get(cc, {}).get("gdp_recession_spans", [])
        nber = us_nber_spans if cc == "US" else None
        d = build_country(cc, name, codes, raw_series, rec_spans, nber)
        if d.get("status") != "ok":
            warn(f"{cc} {name}: 狀態={d.get('status')} 缺={d.get('missing_series')}")
        countries_data.append((cc, name, d))

    tw_rec_spans = yc_countries.get("TW", {}).get("gdp_recession_spans", [])
    tw_d = build_taiwan(tw_raw, tw_rec_spans)
    if tw_d.get("status") != "ok":
        warn(f"TW 台灣：狀態={tw_d.get('status')}（{tw_d.get('note')}）")
    countries_data.append(("TW", "台灣", tw_d))

    return countries_data


# ═══════════════════════════════════════════════════════════════════════════
# 彙總（合併池、分組、散佈圖資料、附表）
# ═══════════════════════════════════════════════════════════════════════════

def all_events(countries_data):
    out = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        for e in d["events"]:
            out.append({**e, "cc": cc, "name": name})
    return out


def pooled_unconditional_raw(countries_data, h):
    out = []
    for _cc, _name, d in countries_data:
        if d.get("status") != "ok":
            continue
        pm = d.get("_price_m")
        if not pm:
            continue
        out.extend(unconditional_raw(pm, h, d["sample_start"], d["sample_end"]))
    return out


def build_table1(countries_data):
    rows = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        row = {"cc": cc, "name": name, "sample": f"{d['sample_start']}～{d['sample_end']}",
               "n_events": len(d["events"]), "by_h": {}}
        for h in H_LIST:
            vals = [e[f"r{h}"] for e in d["events"]]
            row["by_h"][h] = {"cond": summarize_returns(vals), "uncond": d["unconditional"][h]}
        rows.append(row)
    pooled_by_h = {}
    for h in H_LIST:
        vals = []
        for _cc, _name, d in countries_data:
            if d.get("status") != "ok":
                continue
            vals.extend(e[f"r{h}"] for e in d["events"])
        pooled_by_h[h] = {"cond": summarize_returns(vals),
                           "uncond": summarize_returns(pooled_unconditional_raw(countries_data, h))}
    return rows, pooled_by_h


def build_group_stats(countries_data):
    ev = all_events(countries_data)

    def _grp(lst):
        mdds = [e["mdd12"] for e in lst if e["mdd12"] is not None]
        return {"n": len(lst),
                "by_h": {h: summarize_returns([e[f"r{h}"] for e in lst]) for h in H_LIST},
                "mdd12_median": round(statistics.median(mdds), 2) if mdds else None,
                "mdd12_n": len(mdds)}
    return {g: _grp([e for e in ev if e["recession_group"] == g]) for g in RECESSION_GROUPS}


def build_avg_path(countries_data, only_cc=None, pre=6, post=24):
    ev = all_events(countries_data)
    if only_cc:
        ev = [e for e in ev if e["cc"] == only_cc]

    def _avg(lst):
        paths = [e["index_path"] for e in lst if e.get("index_path")]
        if not paths:
            return None
        n_points = pre + post + 1
        out = []
        for i in range(n_points):
            vals = [p[i] for p in paths if i < len(p) and p[i] is not None]
            out.append(round(sum(vals) / len(vals), 2) if vals else None)
        return out
    out = {}
    for g in RECESSION_GROUPS:
        grp_ev = [e for e in ev if e["recession_group"] == g]
        out[g] = _avg(grp_ev)
        out[f"n_{g}"] = len(grp_ev)
    return out


def build_scatter(countries_data, x_key):
    ev = all_events(countries_data)
    return [{"cc": e["cc"], "name": e["name"], "x": e[x_key], "y": e["r12"],
              "recession_group": e["recession_group"], "event_month": e["event_month"]}
             for e in ev if e[x_key] is not None and e["r12"] is not None]


def build_country_group_medians(countries_data):
    rows = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        row = {"cc": cc, "name": name}
        for g in RECESSION_GROUPS:
            vals = [e["r12"] for e in d["events"] if e["recession_group"] == g and e["r12"] is not None]
            row[f"{g}_median"] = round(statistics.median(vals), 2) if vals else None
            row[f"{g}_n"] = len(vals)
        rows.append(row)
    return rows


def _recent_row(cc, name, e, countries_data):
    d = next(dd for c, n, dd in countries_data if c == cc)
    pm = d.get("_price_m") or {}
    tail = d.get("price_series_tail")
    ret_to_date, as_of = None, None
    if tail:
        as_of, tail_val = tail
        r = _log_ret_pct(pm.get(e["event_month"]), tail_val)
        ret_to_date = r
    return {"cc": cc, "name": name, "event_month": e["event_month"], "peak_month": e["peak_month"],
            "recession_group": e["recession_group"], "r6": e["r6"], "r12": e["r12"], "r24": e["r24"],
            "ret_to_date": ret_to_date, "as_of": as_of}


def build_recent_table(countries_data):
    rows = []
    us_d = next((d for cc, n, d in countries_data if cc == "US" and d.get("status") == "ok"), None)
    if us_d:
        us_sorted = sorted(us_d["events"], key=lambda e: e["event_month"])
        for e in [ev for ev in us_sorted if ev["event_month"] >= "2018-01"][-2:]:
            rows.append(_recent_row("US", "美國", e, countries_data))
    for cc, name, d in countries_data:
        if cc == "US" or d.get("status") != "ok":
            continue
        for e in d["events"]:
            if e["event_month"].startswith("2024"):
                rows.append(_recent_row(cc, name, e, countries_data))
    most_recent_note = {}
    for cc, name, d in countries_data:
        if cc in ("US",) or d.get("status") != "ok" or not d["events"]:
            continue
        last = max(d["events"], key=lambda e: e["event_month"])
        if not last["event_month"].startswith("2024"):
            most_recent_note[cc] = {"name": name, "event_month": last["event_month"]}
    return rows, most_recent_note


# ═══════════════════════════════════════════════════════════════════════════
# 頁面文字（沿用 ycr 的版型工具，不改該模組）
# ═══════════════════════════════════════════════════════════════════════════

esc = ycr.esc
fmt_pct = ycr.fmt_pct
fmt_pp = ycr.fmt_pp
fmt_num = ycr.fmt_num
fmt_month = ycr.fmt_month
fmt_ci = ycr.fmt_ci
CN_NUM = ycr.CN_NUM
BRAND_BLUE = ycr.BRAND_BLUE
GRAY_MISS = ycr.GRAY_MISS
LIGHT_GRAY_BASE = ycr.LIGHT_GRAY_BASE
US_ORANGE = ycr.US_ORANGE
COUNTRY_COLORS = ycr.COUNTRY_COLORS
POINT_MARKER_PLUGIN_JS = ycr.POINT_MARKER_PLUGIN_JS
REC_RED = "#dc2626"
NOREC_GREEN = "#059669"


def fmt_ret(x, digits=1):
    return "—" if x is None else f"{x:+.{digits}f}%"


def _section_shell(num_idx, title, lead, body_html):
    n = CN_NUM[num_idx]
    return f"""
<div class="section">
<h2 class="section-title">{esc(n)}、{esc(title)}</h2>
<div class="takeaway">{esc(lead)}</div>
{body_html}
</div>
"""


DEFINITIONS_TEXT = [
    "月利率序列先取 3 個月移動平均（去雜訊，隔夜利率月間波動大，尤其 1970–80 年代），"
    "要求三個月連續，缺月不補。",
    "升息循環＝利率 3 個月均值從低點上升 1.00 個百分點以上，低點到高點期間不超過 36 個月。"
    "低點採「事件當下回溯 36 個月內的滾動最低值」，不是狀態機重置後最近一次的低點。"
    "這個選擇是為了處理 1994–1997 這種「大幅升息後盤整、再小升一段就降息」的情況：1997 年 "
    "3 個月均值只比 1996 年低點多升 0.25 個百分點，單獨看不夠格。但拉長回溯窗口到 36 個月，"
    "1997 年的高點仍在 1994 年那波升息的低點之上超過 1.00 個百分點，所以仍算數，1998 年那次"
    "降息才能被正確判定為「高點之後的第一次降息」，不會漏算。",
    "循環高點＝利率序列由升轉降前的最後一個月（局部高點），且該點符合上一條的升息循環門檻。",
    "第一次降息＝高點之後第一個「3 個月均值比高點低 0.25 個百分點以上」的月份，且高點到"
    "該月不超過 18 個月，超過視為沒有降息循環、整個循環作廢，不登記事件。",
    "事件＝第一次降息月。同一波高點如果在 24 個月內出現好幾個局部高點（大升息循環中間的"
    "小波動），只留最高的一個高點對應的事件，避免同一波循環被拆成好幾筆。",
    "分組（2026-09-17 由二分改三分）：先看事件月當下是不是已經落在定義 A（技術性衰退，實質 GDP "
    "連兩季負成長，資料直接讀 data/yield_curve_recession.json，不重算）的衰退區間內，是的話歸"
    "「降息時已在衰退中」。不是的話，再看事件月之後、事件月＋12 個月內有沒有衰退起點，有的話"
    "歸「衰退之後才開始」。兩者都不是，且事件前 6 個月到事件後 12 個月的視窗內完全沒有衰退區間"
    "重疊，才歸「無衰退」。初版只分「有衰退」「無衰退」兩組，「有衰退」組把「降息時衰退已經在"
    "發生、股市接近底部」跟「降息時還沒衰退、股市之後才開始跌」這兩種處境混在一起平均，兩種"
    "力道方向常常相反，平均後反而看不出模式，所以拆開來看。美國另外用 NBER（美國國家經濟研究局）"
    "認定的衰退期（USRECDM）分一次對照，只在美國"
    "逐事件表旁列出，不進八國合併統計。",
    "前向報酬 R(h)，h＝6、12、24 個月，從事件月月底的股價指數算到事件月＋h 個月月底，"
    "用 log 報酬換算成百分比（更貼近長期複利的算法，正負報酬不會因為算法本身產生偏誤）。"
    "另外算 R(−6)，事件前 6 個月到事件月的同一種報酬，衡量市場是不是已經先反應。",
    "無條件對照＝該國全樣本任一月份起算的同天期報酬分布（逐月滾動），跟事件月的報酬分布"
    "比中位數、負報酬比率、第 25／75 百分位。負報酬比率一律附 Wilson 95% 信賴區間"
    "（confidence interval）。",
    "政策利率後續路徑＝事件後 12 個月的利率總降幅，用循環高點的 3 個月均值減去高點後 12 個月"
    "的 3 個月均值。",
    "MDD(12)＝事件月起 12 個月內（含事件月，共 13 個月的月底值）的最深跌幅，逐月更新歷史"
    "高點後算相對回落。",
    "股價一律用 OECD「股價指數：全部股票」（FRED 代碼 SPASTT01{CC}M661N），這是價格指數，"
    "不含股息，長期報酬會系統性低於含息報酬，八國口徑一致。",
    "政策利率代理：美國主線用 FEDFUNDS（聯邦資金利率），其餘六國用 OECD 隔夜／即期利率"
    "（IRSTCI01{CC}M156N）。台灣用央行「重貼現率」（央行統計資料庫 EG2AM01），性質是央行"
    "對銀行融通的政策利率，不是市場利率，但同樣是央行主動調整、對外公告的政策工具，跟"
    "其餘七國的定位一致。",
    "台灣股價用央行統計資料庫「加權平均股價指數」（EG27M01），即台灣證券交易所發行量"
    "加權股價指數的月資料，口徑與其餘七國的 OECD 股價指數一致（價格指數、不含股息）。",
    "樣本窗＝該國利率與股價兩者都有資料的期間，起訖印在每張表上。事件月若落在樣本窗外"
    "（例如股價資料比利率資料晚開始），該事件不計入統計。",
]


def section_method(countries_data):
    lis = "".join(f"<li>{esc(t)}</li>" for t in DEFINITIONS_TEXT)
    return f"""
<div class="section">
<h2 class="section-title">七、方法：怎麼定義「第一次降息」與「有沒有衰退」</h2>
<div class="takeaway">這頁的判定規則在跑資料前就定死，八個國家套同一套定義，中途不因某國
結果好不好看而回頭調整。利率先取 3 個月移動平均去雜訊，降息事件的判定邏輯詳細寫在下面，
衰退區間直接讀已經上線的殖利率倒掛頁算好的技術性衰退資料，不重算。</div>
<div class="card"><ul class="disc">{lis}</ul></div>
</div>
"""


def section_reader_note():
    return ("<b>給沒有統計背景的讀者：</b>這頁做的事很單純。央行升息一段時間後，通常會有一次"
            "「風向轉了」的第一次降息，市場常把這個時間點當成訊號。我們把八個國家的利率跟股價"
            "資料拉出來，用同一套規則自動判定「升息循環」跟「第一次降息」，算第一次降息之後 "
            "6、12、24 個月股市漲跌多少，再跟「有沒有衰退」分組比、跟「降息前市場是不是已經"
            "先反應」對照、跟「降得越急股市越怎樣」對照。本頁不做「現在該不該進場」的建議，"
            "也不預測下一次降息什麼時候來，只回報歷史上這個訊號準不準、差在哪裡。")


def section_hero(table1_pooled, group_stats, scatter_pre, tw_status):
    h = table1_pooled[PRIMARY_H]
    cond, uncond = h["cond"], h["uncond"]
    norec = group_stats["no_recession"]
    after = group_stats["recession_after"]
    during = group_stats["recession_during"]
    norec_med = norec["by_h"][PRIMARY_H]["median"]
    after_med = after["by_h"][PRIMARY_H]["median"]
    during_med = during["by_h"][PRIMARY_H]["median"]

    if after_med is not None and during_med is not None and after_med < during_med - 10:
        verdict, tag_color = "衰退還沒開始最傷，已經在衰退中的降息反而落底", REC_RED
    elif after_med is not None and during_med is not None and during_med < after_med - 10:
        verdict, tag_color = "已經在衰退中的降息比較傷，衰退還沒開始的影響較小", "#d97706"
    else:
        verdict, tag_color = "有沒有衰退，比降息本身更關鍵", "#d97706"

    q1 = (f"第一次降息後 12 個月股市怎麼走？合併池 {cond['n']} 個事件，中位數報酬 "
          f"{fmt_ret(cond['median'])}，同一段時間不看訊號的中位數報酬 {fmt_ret(uncond['median'])}。")
    q2 = (f"降息本身是不是訊號？無衰退組 12 個月中位數 {fmt_ret(norec_med)}（{norec['n']} 個事件），"
          f"衰退之後才開始那組 {fmt_ret(after_med)}（{after['n']} 個事件），降息時已在衰退中那組 "
          f"{fmt_ret(during_med)}（{during['n']} 個事件），三組差很多。")
    n_pos_pre = sum(1 for p in scatter_pre if p["x"] is not None and p["x"] > 0)
    n_pre = len(scatter_pre)
    q3 = (f"降息前市場是不是已經先反應？{n_pre} 個可比對事件中，"
          f"{n_pos_pre} 個事件降息前 6 個月股市是正報酬。")
    tw_note = "台灣併入主表。" if tw_status == "ok" else "台灣資料整理中，本頁先出七國版本。"
    q4 = f"八國一致嗎？{tw_note}各國中位數差很多，事件數也不對稱，小樣本國家的單一數字不宜太當真。"

    return f"""
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag" style="background:{tag_color}">{esc(verdict)}</span>
    <h2>{esc(q1)}</h2>
    <p>{esc(q2)}</p>
    <p>{esc(q3)} {esc(q4)}</p>
  </div>
  <div class="hero-stats">
    <div><div class="hs-label">合併池事件數</div><div class="hs-value">{cond['n']}</div></div>
    <div><div class="hs-label">無衰退組中位數</div><div class="hs-value">{fmt_ret(norec_med, 0)}</div></div>
    <div><div class="hs-label">衰退之後才開始中位數</div><div class="hs-value">{fmt_ret(after_med, 0)}</div></div>
    <div><div class="hs-label">已在衰退中中位數</div><div class="hs-value">{fmt_ret(during_med, 0)}</div></div>
  </div>
</div>
"""


def section12_not_told(countries_data, tw_status):
    tw_bits = ""
    if tw_status != "ok":
        tw_bits = ("<li>台灣資料整理中，本頁先出七國版本。央行重貼現率與加權平均股價指數"
                    "任一項筆數不足時不硬湊，等資料補齊再併入主表。</li>")
    n_events_total = sum(len(d["events"]) for _cc, _n, d in countries_data if d.get("status") == "ok")
    return f"""
<div class="section">
<h2 class="section-title">八、這頁沒有告訴你的事</h2>
<div class="card"><ul class="disc">
<li>隔夜／即期利率不是官方公告的政策利率本身，是政策利率最直接反映在市場上的月頻代理。
美國主線改用 FEDFUNDS（聯邦資金利率）比較貼近官方目標區間，其餘六國仍是市場利率代理，
跟官方政策利率的宣告時點可能差幾天到幾週。</li>
<li>零利率年代（日本 1995 年後、美國 2009–2015 年與 2020–2021 年）利率長期貼近 0，升息
循環的門檻（低點上升 1.00 個百分點）自然很難觸發，這段期間幾乎沒有事件。這個定義本來就
抓不到貼零利率時代的政策轉向，跟模型漏算是兩回事。</li>
<li>全部 {n_events_total} 個事件分散在八個國家、將近七十年，多數國家個位數到十幾個事件，
小樣本下任何一個中位數都可能被單一極端事件拉動，表格上都附了事件數，數字小的地方不下結論。</li>
<li>股價一律用不含股息的價格指數，長期含息總報酬會比這裡算出來的數字高，尤其股息率較高
的市場（如英國、澳洲），差距會更明顯。</li>
{tw_bits}
<li>這裡只回報歷史上「第一次降息」附近股市怎麼走，不是進出場訊號。</li>
</ul></div>
</div>
"""


def appendix_event_detail(countries_data):
    blocks = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok" or not d["events"]:
            continue
        rows = []
        for e in d["events"]:
            rec_label = RECESSION_GROUP_LABEL[e["recession_group"]]
            nber = "" if e["has_recession_nber"] is None else ("／NBER 有衰退" if e["has_recession_nber"] else "／NBER 無衰退")
            rows.append(
                f"<tr><td>{esc(e['peak_month'])}</td><td class='num'>{fmt_num(e['peak_val'], 2)}</td>"
                f"<td>{esc(e['event_month'])}</td><td class='num'>{fmt_num(e['event_val'], 2)}</td>"
                f"<td>{esc(rec_label)}{esc(nber)}</td>"
                f"<td class='num'>{fmt_ret(e['r_pre6'])}</td>"
                f"<td class='num'>{fmt_ret(e['r6'])}</td><td class='num'>{fmt_ret(e['r12'])}</td>"
                f"<td class='num'>{fmt_ret(e['r24'])}</td>"
                f"<td class='num'>{'—' if e['rate_decline_12m'] is None else fmt_pp(e['rate_decline_12m'])}</td>"
                f"<td class='num'>{'—' if e['mdd12'] is None else fmt_ret(e['mdd12'])}</td></tr>")
        blocks.append(f"""<h4 style="font-size:.88rem;margin:1rem 0 .5rem">{esc(name)}</h4>
<div class="scroll"><table><thead><tr><th>循環高點</th><th class="num">高點利率</th>
<th>事件月（第一次降息）</th><th class="num">事件利率</th><th>分組</th>
<th class="num">R(−6)</th><th class="num">R(6)</th><th class="num">R(12)</th>
<th class="num">R(24)</th><th class="num">12 月降息幅度</th><th class="num">MDD(12)</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>""")
    body = "".join(blocks)
    return f"""
<div class="section">
<details>
<summary style="cursor:pointer;font-weight:700;font-size:1.02rem;padding:.4rem 0">
附錄：逐事件明細（八國逐筆列出）</summary>
<div class="card" style="margin-top:.75rem">
<p style="font-size:.85rem;margin-bottom:.5rem">前面各節的圖表都是這張表拆解後畫出來的，這裡
把原始逐筆事件列出來備查。R(h) 是空白代表事件太新、還沒走完那段窗口，不是資料缺漏。</p>
{body}
</div>
</details>
</div>
"""


# ═══════════════════════════════════════════════════════════════════════════
# 各節
# ═══════════════════════════════════════════════════════════════════════════

def section1(table1_rows, table1_pooled):
    hp = table1_pooled[PRIMARY_H]
    cond, uncond = hp["cond"], hp["uncond"]
    if cond["median"] is not None and uncond["median"] is not None:
        if cond["median"] >= uncond["median"] + 3:
            title = f"第一次降息後，股市中位數報酬（{fmt_ret(cond['median'])}）比平常月份高"
        elif cond["median"] <= uncond["median"] - 3:
            title = f"第一次降息後，股市中位數報酬（{fmt_ret(cond['median'])}）比平常月份低"
        else:
            title = "第一次降息後 12 個月的股市中位數報酬，跟平常月份分不出差別"
    else:
        title = "第一次降息後 12 個月的股市報酬，合併池數字如下"

    lead = (f"合併池 {cond['n']} 個第一次降息事件，12 個月中位數報酬 {fmt_ret(cond['median'])}，"
            f"同一段時間不看訊號、任一月份起算的 12 個月中位數報酬 {fmt_ret(uncond['median'])}。"
            f"這節先看 6、12、24 個月三種天期，用中位數跟負報酬比率跟無條件對照比，不是只看"
            f"合併池一個數字，逐國數字差多少見下表。")

    labels = [r["name"] for r in table1_rows] + ["合併池"]
    cond_med = [r["by_h"][PRIMARY_H]["cond"]["median"] for r in table1_rows] + [cond["median"]]
    cond_range = [[r["by_h"][PRIMARY_H]["cond"]["p25"], r["by_h"][PRIMARY_H]["cond"]["p75"]]
                  if r["by_h"][PRIMARY_H]["cond"]["p25"] is not None else None for r in table1_rows]
    cond_range.append([cond["p25"], cond["p75"]] if cond["p25"] is not None else None)
    uncond_med = [r["by_h"][PRIMARY_H]["uncond"]["median"] for r in table1_rows] + [uncond["median"]]

    chart_js = f"""
{POINT_MARKER_PLUGIN_JS}
new Chart(document.getElementById('chart1'), {{
  type: 'bar',
  data: {{ labels: {json.dumps(labels, ensure_ascii=False)},
    datasets: [
      {{ label:'無條件中位數（同天期，任一月份起算）', data:{json.dumps(uncond_med)},
         backgroundColor:'{LIGHT_GRAY_BASE}', order:2 }},
      {{ label:'第一次降息後 12 個月：25–75 百分位', data:{json.dumps(cond_range)},
         backgroundColor:'rgba(26,86,219,.30)', borderColor:'{BRAND_BLUE}', borderWidth:1, order:1,
         _pointValues:{json.dumps(cond_med)}, _pointColor:'{BRAND_BLUE}' }}
    ] }},
  options: {{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'log 報酬換算百分比'}} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:420px"><canvas id="chart1"></canvas></div>'
    caption = ("藍色區間是事件後 12 個月報酬的第 25～75 百分位，藍點是中位數，灰色長條是同一個"
               "國家不看訊號、任一月份起算 12 個月報酬的中位數。藍點在灰色長條右邊，代表降息後"
               "報酬中位數比平常高。在左邊代表比平常低。")

    def _row(r):
        cells = []
        for h in H_LIST:
            c, u = r["by_h"][h]["cond"], r["by_h"][h]["uncond"]
            neg = "—" if c["neg_rate"] is None else f"{fmt_pct(c['neg_rate'])}（{fmt_ci(c['neg_ci_low'], c['neg_ci_high'])}）"
            cells.append(
                f"<td class='num'>{c['n']}</td><td class='num'>{fmt_ret(c['median'])}</td>"
                f"<td class='num'>{neg}</td>"
                f"<td class='num'>{fmt_ret(u['median'])}</td>")
        return f"<tr><td class='lbl'>{esc(r['name'])}</td><td>{esc(r['sample'])}</td>{''.join(cells)}</tr>"

    table_rows = "".join(_row(r) for r in table1_rows)
    pooled_cells = []
    for h in H_LIST:
        c, u = table1_pooled[h]["cond"], table1_pooled[h]["uncond"]
        neg = "—" if c["neg_rate"] is None else f"{fmt_pct(c['neg_rate'])}（{fmt_ci(c['neg_ci_low'], c['neg_ci_high'])}）"
        pooled_cells.append(
            f"<td class='num'>{c['n']}</td><td class='num'><b>{fmt_ret(c['median'])}</b></td>"
            f"<td class='num'>{neg}</td>"
            f"<td class='num'>{fmt_ret(u['median'])}</td>")
    table_rows += f"<tr><td class='lbl'><b>合併池</b></td><td>—</td>{''.join(pooled_cells)}</tr>"

    h_headers = "".join(
        f"<th class='num'>n</th><th class='num'>R({h}) 中位數</th>"
        f"<th class='num'>負報酬比率（95% CI）</th><th class='num'>無條件中位數</th>" for h in H_LIST)
    table_html = (f'<div class="scroll"><table><thead><tr><th>國家</th><th>樣本期間</th>{h_headers}'
                  f'</tr></thead><tbody>{table_rows}</tbody></table></div>')

    straddlers = [r["name"] for r in table1_rows
                  if r["by_h"][PRIMARY_H]["cond"]["median"] is not None
                  and r["by_h"][PRIMARY_H]["uncond"]["median"] is not None
                  and abs(r["by_h"][PRIMARY_H]["cond"]["median"] - r["by_h"][PRIMARY_H]["uncond"]["median"]) < 3]
    small_n = [r["name"] for r in table1_rows if r["n_events"] <= 3]
    note_parts = []
    if straddlers:
        note_parts.append(f"{'、'.join(straddlers)}的 12 個月中位數報酬跟無條件對照差在 3 個百分點"
                           f"以內，分不太出差別。")
    if small_n:
        note_parts.append(f"{'、'.join(small_n)}事件數只有個位數，單一極端事件就能大幅拉動中位數，"
                           f"數字僅供參考。")
    note = "".join(note_parts) if note_parts else "各國中位數跟無條件對照的差距不小，逐國數字見上表。"

    html = _section_shell(0, title, lead,
                           f"{chart_html}\n<div class=\"note\">{esc(caption)}</div>\n{table_html}\n"
                           f"<div class=\"note\">{esc(note)}</div><script>{chart_js}</script>")
    return html


def section2(group_stats, avg_path_pooled, avg_path_us):
    norec = group_stats["no_recession"]
    after = group_stats["recession_after"]
    during = group_stats["recession_during"]
    norec_med = norec["by_h"][PRIMARY_H]["median"]
    after_med = after["by_h"][PRIMARY_H]["median"]
    during_med = during["by_h"][PRIMARY_H]["median"]

    if after_med is not None and during_med is not None and after_med < during_med - 10:
        title = "衰退還沒開始那組跌最深，已經在衰退中那組反而落底回升"
    elif after_med is not None and during_med is not None and during_med < after_med - 10:
        title = "已經在衰退中那組跌最深，衰退還沒開始那組影響較小"
    else:
        title = "衰退之後才開始、降息時已在衰退中，這兩組報酬沒有拉開明顯差距"

    lead = (f"無衰退組 {norec['n']} 個事件，12 個月中位數 {fmt_ret(norec_med)}。衰退之後才開始那組"
            f"（衰退起點落在事件月之後、12 個月內）{after['n']} 個事件，中位數 {fmt_ret(after_med)}。"
            f"降息時已在衰退中那組（事件月當下已經處於衰退區間）{during['n']} 個事件，中位數 "
            f"{fmt_ret(during_med)}。這節把原本籠統的「有衰退」拆成這兩組，看差距是不是被平均掉了。")

    offsets = list(range(-6, 25))
    labels = [str(k) for k in offsets]

    def _line(data, color, label, dash=None):
        dash_js = f", borderDash:{json.dumps(dash)}" if dash else ""
        return (f"{{ label:{json.dumps(label, ensure_ascii=False)}, data:{json.dumps(data)}, "
                f"borderColor:'{color}', backgroundColor:'transparent', pointRadius:0, "
                f"borderWidth:1.6{dash_js} }}")

    group_line_color = {"no_recession": NOREC_GREEN, "recession_after": RECESSION_GROUP_COLOR["recession_after"],
                         "recession_during": REC_RED}
    datasets = []
    for scope, avg_path, dash in (("八國合併", avg_path_pooled, None), ("美國", avg_path_us, [5, 4])):
        for g in RECESSION_GROUPS:
            if avg_path.get(g):
                datasets.append(_line(avg_path[g], group_line_color[g],
                                       f"{scope}．{RECESSION_GROUP_LABEL[g]}（共 {avg_path[f'n_{g}']} 個事件）",
                                       dash=dash))

    chart_js = f"""
new Chart(document.getElementById('chart2'), {{
  type: 'line',
  data: {{ labels: {json.dumps(labels)}, datasets: [{','.join(datasets)}] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'距離第一次降息的月數（0＝事件月）'}} }},
               y:{{ title:{{display:true,text:'指數（事件月＝100）'}} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }},
      verticalLine:{{ value:6, color:'#9ca3af' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:420px"><canvas id="chart2"></canvas></div>'
    caption = ("每條線把事件月的股價指數訂為 100，往前 6 個月、往後 24 個月逐月取平均路徑。"
               "虛線灰色直線標事件月往後第 6 個月。實線是八國合併，虛線是只看美國。綠色無衰退、"
               "橘色衰退之後才開始、紅色降息時已在衰退中，看的是橘線跟紅線是不是走不同方向。")

    def _grp_row(label, g):
        cells = "".join(f"<td class='num'>{fmt_ret(g['by_h'][h]['median'])}</td>" for h in H_LIST)
        neg12 = g['by_h'][PRIMARY_H]['neg_rate']
        neg_str = (f"{fmt_pct(neg12)}（{fmt_ci(g['by_h'][PRIMARY_H]['neg_ci_low'], g['by_h'][PRIMARY_H]['neg_ci_high'])}）"
                   if neg12 is not None else "—")
        return (f"<tr><td class='lbl'>{esc(label)}</td>{cells}"
                f"<td class='num'>{neg_str}</td>"
                f"<td class='num'>{fmt_ret(g['mdd12_median'])}</td><td class='num'>{g['n']}</td></tr>")

    table_html = (f'<div class="scroll"><table><thead><tr><th>分組</th>'
                  + "".join(f"<th class='num'>R({h}) 中位數</th>" for h in H_LIST)
                  + "<th class='num'>R(12) 負報酬比率（95% CI）</th>"
                  + "<th class='num'>MDD(12) 中位數</th><th class='num'>事件數</th></tr></thead>"
                  f'<tbody>{_grp_row("無衰退", norec)}{_grp_row("衰退之後才開始", after)}'
                  f'{_grp_row("降息時已在衰退中", during)}</tbody></table></div>')

    note = (f"最深跌幅（MDD，事件月起 12 個月內的最大回落）中位數，無衰退組 {fmt_ret(norec['mdd12_median'])}，"
            f"衰退之後才開始那組 {fmt_ret(after['mdd12_median'])}，降息時已在衰退中那組 "
            f"{fmt_ret(during['mdd12_median'])}。")

    html = _section_shell(1, title, lead,
                           f"{chart_html}\n<div class=\"note\">{esc(caption)}</div>\n{table_html}\n"
                           f"<div class=\"note\">{esc(note)}</div><script>{chart_js}</script>")
    return html


def section3(scatter_pre):
    n = len(scatter_pre)
    pos_pre = [p for p in scatter_pre if p["x"] > 0]
    neg_pre = [p for p in scatter_pre if p["x"] <= 0]
    pos_med12 = statistics.median([p["y"] for p in pos_pre]) if pos_pre else None
    neg_med12 = statistics.median([p["y"] for p in neg_pre]) if neg_pre else None

    if len(pos_pre) >= n * 0.5:
        title = "降息前 6 個月股市多半已經上漲"
    else:
        title = "降息前 6 個月股市不一定已經上漲"

    lead = (f"{n} 個可比對事件中，{len(pos_pre)} 個事件降息前 6 個月是正報酬。x 軸是降息前 6 個月的"
            f"報酬，y 軸是降息後 12 個月的報酬，看的是股市在降息前就先動，降息後還能不能延續同個"
            f"方向。")

    group_color = {"no_recession": NOREC_GREEN, "recession_after": RECESSION_GROUP_COLOR["recession_after"],
                   "recession_during": REC_RED}
    group_sets = []
    for g in RECESSION_GROUPS:
        pts = [{"x": p["x"], "y": p["y"]} for p in scatter_pre if p["recession_group"] == g]
        group_sets.append(f"{{ label:'{RECESSION_GROUP_LABEL[g]}', data:{json.dumps(pts)}, "
                           f"pointBackgroundColor:'{group_color[g]}', pointRadius:4.5 }}")
    chart_js = f"""
new Chart(document.getElementById('chart3'), {{
  type:'scatter',
  data: {{ datasets: [{','.join(group_sets)}] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'降息前 6 個月報酬 R(-6)，%'}} }},
               y:{{ title:{{display:true,text:'降息後 12 個月報酬 R(12)，%'}} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }},
      zeroLine:{{ enabled:true, color:'#d1d5db' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart3"></canvas></div>'
    caption = ("每個點是一次第一次降息事件，x 軸落在 0 右邊代表降息前 6 個月股市已經上漲，"
               "y 軸落在 0 上面代表降息後 12 個月股市續漲。綠點無衰退、橘點衰退之後才開始、紅點"
               "降息時已在衰退中，三色混在一起代表降息前有沒有先漲，不能用來判斷降息後屬於"
               "哪一組。")
    note = (f"降息前 6 個月是正報酬的 {len(pos_pre)} 個事件，降息後 12 個月中位數 "
            f"{fmt_ret(pos_med12)}。降息前是負報酬的 {len(neg_pre)} 個事件，降息後 12 個月中位數 "
            f"{fmt_ret(neg_med12)}。")

    html = _section_shell(2, title, lead,
                           f"{chart_html}\n<div class=\"note\">{esc(caption)}</div>\n"
                           f"<div class=\"note\">{esc(note)}</div><script>{chart_js}</script>")
    return html


def section4(scatter_decline):
    n = len(scatter_decline)
    fast = [p for p in scatter_decline if p["x"] is not None]
    fast_sorted = sorted(fast, key=lambda p: p["x"], reverse=True)
    half = max(1, len(fast_sorted) // 2)
    fast_half = fast_sorted[:half]
    slow_half = fast_sorted[half:]
    fast_med = statistics.median([p["y"] for p in fast_half]) if fast_half else None
    slow_med = statistics.median([p["y"] for p in slow_half]) if slow_half else None

    if fast_med is not None and slow_med is not None and fast_med < slow_med - 5:
        title = "降得越急，12 個月股市中位數報酬反而越低"
    elif fast_med is not None and slow_med is not None and fast_med > slow_med + 5:
        title = "降得越急，12 個月股市中位數報酬反而越高"
    else:
        title = "降息幅度跟 12 個月股市報酬，看不出明顯的線性關係"

    lead = (f"x 軸是事件後 12 個月的利率總降幅（高點減 12 個月後的值，數字越大代表降得越急），"
            f"y 軸是事件後 12 個月的股市報酬，共 {n} 個可比對事件，兩色分有衰退／無衰退。")

    rec_pts = [{"x": p["x"], "y": p["y"]} for p in scatter_decline if p["recession_group"] != "no_recession"]
    norec_pts = [{"x": p["x"], "y": p["y"]} for p in scatter_decline if p["recession_group"] == "no_recession"]
    chart_js = f"""
new Chart(document.getElementById('chart4'), {{
  type:'scatter',
  data: {{ datasets: [
    {{ label:'有衰退', data:{json.dumps(rec_pts)}, pointBackgroundColor:'{REC_RED}', pointRadius:4.5 }},
    {{ label:'無衰退', data:{json.dumps(norec_pts)}, pointBackgroundColor:'{NOREC_GREEN}', pointRadius:4.5 }}
  ] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'事件後 12 個月利率總降幅，pp'}} }},
               y:{{ title:{{display:true,text:'事件後 12 個月股市報酬 R(12)，%'}} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart4"></canvas></div>'
    caption = ("x 軸越往右代表央行降得越急、降幅越大，y 軸越往上代表股市 12 個月後漲越多。"
               "如果紅點（有衰退）系統性落在右邊，代表降得急的事件多半伴隨衰退，降息幅度本身"
               "可能只是反映衰退嚴重程度，不是獨立的股市訊號。")
    note = (f"降幅較大的一半事件（{len(fast_half)} 個）12 個月中位數 {fmt_ret(fast_med)}，"
            f"降幅較小的一半（{len(slow_half)} 個）中位數 {fmt_ret(slow_med)}。")

    html = _section_shell(3, title, lead,
                           f"{chart_html}\n<div class=\"note\">{esc(caption)}</div>\n"
                           f"<div class=\"note\">{esc(note)}</div><script>{chart_js}</script>")
    return html


def section5(country_group_medians):
    both = [r for r in country_group_medians
            if r["recession_after_median"] is not None and r["recession_during_median"] is not None]
    during_worse = [r for r in both if r["recession_during_median"] < r["recession_after_median"]]
    after_worse = [r for r in both if r["recession_after_median"] < r["recession_during_median"]]

    if both and len(during_worse) == len(both):
        title = "有資料可比的國家方向一致：已在衰退中都比較差"
    elif both and len(after_worse) == len(both):
        title = "有資料可比的國家方向一致：衰退之後才開始都比較差"
    else:
        title = "八國方向不完全一致，多數國家同時有三組資料才能比"

    lead = (f"{len(both)} 個國家同時有「衰退之後才開始」跟「降息時已在衰退中」的事件可以比較，"
            f"這節看的是每個國家自己內部，哪一組真的比較差，八國答案是不是一致。")

    labels = [r["name"] for r in country_group_medians]
    group_color = {"no_recession": NOREC_GREEN, "recession_after": RECESSION_GROUP_COLOR["recession_after"],
                   "recession_during": REC_RED}
    datasets_js = ",".join(
        f"{{ label:'{RECESSION_GROUP_LABEL[g]}中位數', "
        f"data:{json.dumps([r[f'{g}_median'] for r in country_group_medians])}, "
        f"backgroundColor:'{group_color[g]}' }}" for g in RECESSION_GROUPS)
    chart_js = f"""
new Chart(document.getElementById('chart5'), {{
  type: 'bar',
  data: {{ labels: {json.dumps(labels, ensure_ascii=False)}, datasets: [{datasets_js}] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ y:{{ title:{{display:true,text:'12 個月中位數報酬，%'}} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart5"></canvas></div>'
    caption = ("每個國家三根長條：綠色無衰退、橘色衰退之後才開始、紅色降息時已在衰退中，缺色"
               "代表那個國家該分組沒有事件，不是報酬為零。看的是紅色長條是不是普遍比橘色長條"
               "低，還是八國答案不一致。")

    rows = "".join(
        f"<tr><td class='lbl'>{esc(r['name'])}</td>"
        f"<td class='num'>{fmt_ret(r['no_recession_median'])}</td><td class='num'>{r['no_recession_n']}</td>"
        f"<td class='num'>{fmt_ret(r['recession_after_median'])}</td><td class='num'>{r['recession_after_n']}</td>"
        f"<td class='num'>{fmt_ret(r['recession_during_median'])}</td><td class='num'>{r['recession_during_n']}</td>"
        f"</tr>"
        for r in country_group_medians)
    table_html = (f'<div class="scroll"><table><thead><tr><th>國家</th>'
                  f'<th class="num">無衰退中位數</th><th class="num">事件數</th>'
                  f'<th class="num">衰退之後才開始中位數</th><th class="num">事件數</th>'
                  f'<th class="num">已在衰退中中位數</th><th class="num">事件數</th></tr></thead>'
                  f'<tbody>{rows}</tbody></table></div>')

    note = (f"{len(both)} 個國家同時有兩組數字可以比，其中 {len(during_worse)} 個國家已在衰退中那組"
            f"比較差，{len(after_worse)} 個國家反過來。多數國家單一分組事件數只有 1、2 筆，"
            f"一個事件就能決定中位數，不宜過度解讀方向。")

    html = _section_shell(4, title, lead,
                           f"{chart_html}\n<div class=\"note\">{esc(caption)}</div>\n{table_html}\n"
                           f"<div class=\"note\">{esc(note)}</div><script>{chart_js}</script>")
    return html


def section6(recent_rows, recent_note):
    rows = "".join(
        f"<tr><td class='lbl'>{esc(r['name'])}</td><td>{esc(r['event_month'])}</td>"
        f"<td>{esc(RECESSION_GROUP_LABEL[r['recession_group']])}</td>"
        f"<td class='num'>{fmt_ret(r['r6'])}</td><td class='num'>{fmt_ret(r['r12'])}</td>"
        f"<td class='num'>{fmt_ret(r['r24'])}</td>"
        f"<td class='num'>{fmt_ret(r['ret_to_date'])}</td><td>{esc(r['as_of'] or '—')}</td></tr>"
        for r in recent_rows)
    table_html = (f'<div class="scroll"><table><thead><tr><th>國家</th><th>事件月</th><th>分組</th>'
                  f'<th class="num">R(6)</th><th class="num">R(12)</th><th class="num">R(24)</th>'
                  f'<th class="num">到目前報酬</th><th>資料截至</th></tr></thead>'
                  f'<tbody>{rows}</tbody></table></div>')

    lead = "美國 2019 年與 2024 年這兩次第一次降息，加上其他七國 2024 年出現的第一次降息，逐筆列出到目前的報酬。"
    if recent_note:
        bits = "、".join(f"{info_['name']}（{info_['event_month']}）" for info_ in recent_note.values())
        note = f"{bits}最近一次第一次降息不在 2024 年，未列入本表。"
    else:
        note = "本表逐筆列出，數字截至各國股價資料最新一筆。"

    html = _section_shell(5, "最近三次：2019、2024 年美國與其他國家 2024 年的第一次降息", lead,
                           f"{table_html}\n<div class=\"note\">{esc(note)}</div>")
    return html


def generate_html(countries_data, table1_rows, table1_pooled, group_stats,
                   avg_path_pooled, avg_path_us, scatter_pre, scatter_decline,
                   country_group_medians, recent_rows, recent_note, built_date):
    main_style, nav_block = ycr.extract_template_parts()
    tw_status = next(d.get("status") for cc, n, d in countries_data if cc == "TW")
    hp = table1_pooled[PRIMARY_H]
    title = "央行第一次降息之後，股市是漲是跌 | InvestMQuest Research"
    countries_desc = "美/德/英/日/加/澳/韓/台" if tw_status == "ok" else "美/德/英/日/加/澳/韓"
    description = (f"用 OECD 隔夜利率（美國 FEDFUNDS）與 OECD 股價指數對{countries_desc}套用同一套定義，"
                    f"回測升息循環結束後第一次降息的股市報酬：合併池 {hp['cond']['n']} 個事件，"
                    f"12 個月中位數報酬 {fmt_ret(hp['cond']['median'])}，無條件中位數 "
                    f"{fmt_ret(hp['uncond']['median'])}。另拆有衰退／無衰退兩組、降息前市場先反應"
                    f"程度、降息幅度與股市關係、八國一致性。")

    try:
        sys.path.insert(0, str(NAV_DIR))
        from _nav_common import make_toggle  # noqa
        subnav = make_toggle("first_cut")
    except Exception as e:
        warn(f"make_toggle 載入失敗：{e}，pill bar 留空")
        subnav = ""

    hero = section_hero(table1_pooled, group_stats, scatter_pre, tw_status)
    reader_note = section_reader_note()
    s1 = section1(table1_rows, table1_pooled)
    s2 = section2(group_stats, avg_path_pooled, avg_path_us)
    s3 = section3(scatter_pre)
    s4 = section4(scatter_decline)
    s5 = section5(country_group_medians)
    s6 = section6(recent_rows, recent_note)
    s7 = section_method(countries_data)
    s8 = section12_not_told(countries_data, tw_status)
    appendix = appendix_event_detail(countries_data)

    body = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<script src="{CHART_JS_CDN}"></script>
{main_style}
</head>
<body>
{nav_block}

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / 央行第一次降息與股市</div>
    <h1>央行第一次降息之後，股市是漲是跌？</h1>
    <div class="sub">升息循環結束後第一次降息，八國股市 6／12／24 個月報酬回測・生成 {esc(built_date)}</div>
    {subnav}
  </div>
</div>

<div class="container">

{hero}

<div class="takeaway">{reader_note}</div>

{s1}
{s2}
{s3}
{s4}
{s5}
{s6}
{s7}
{s8}
{appendix}

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 央行第一次降息之後，股市是漲是跌？（研究頁，不構成投資建議）
    &middot; 頁面生成 {esc(built_date)} &middot; 僅供研究參考，不構成投資建議
  </div>
</footer>
</body>
</html>
"""
    return ycr.collapse_cjk_whitespace(body)


# ═══════════════════════════════════════════════════════════════════════════
# 主流程：算＋輸出 JSON＋生成頁面
# ═══════════════════════════════════════════════════════════════════════════

def _strip_internal(countries_data):
    for _cc, _name, d in countries_data:
        d.pop("_price_m", None)


def do_compute_and_build():
    countries_data = do_compute()

    table1_rows, table1_pooled = build_table1(countries_data)
    group_stats = build_group_stats(countries_data)
    avg_path_pooled = build_avg_path(countries_data)
    avg_path_us = build_avg_path(countries_data, only_cc="US")
    scatter_pre = build_scatter(countries_data, "r_pre6")
    scatter_decline = build_scatter(countries_data, "rate_decline_12m")
    country_group_medians = build_country_group_medians(countries_data)
    recent_rows, recent_note = build_recent_table(countries_data)

    schema_notes = {
        "countries": "cc -> {status, sample_start/end, rate_range, price_range, events:[...], "
                     "unconditional:{6:{...},12:{...},24:{...}}, price_series_tail}。status='ok' 才有"
                     "events／unconditional；'missing'/'partial' 只有 note 說明缺什麼。",
        "events": "每筆＝一次第一次降息事件：peak_month/peak_val＝升息循環高點；event_month/event_val"
                  "＝第一次降息月（事件月）；recession_group＝三組分類之一（no_recession／"
                  "recession_after／recession_during，見 classify_recession_group()），has_recession_nber"
                  "只有美國有值（仍是二分布林值，對照定義 A 三組用）；rate_decline_12m＝高點後 12 個月"
                  "利率總降幅（pp）；r6/r12/r24/r_pre6＝log 報酬換算百分比，事件太新沒走完窗口就是 "
                  "null；mdd12＝事件月起 12 個月內最深跌幅（%）；index_path＝offset -6..24、事件月＝100 "
                  "的相對指數路徑（31 個點，缺值 null）。",
        "unconditional": "h -> {n, median, neg_rate, neg_n, neg_ci_low/high（Wilson 95% CI）, p25, p75}，"
                          "該國全樣本任一月份起算的同天期報酬分布，逐月滾動。",
        "table1_rows/table1_pooled": "八國逐國＋合併池，h=6/12/24 各自 cond（事件後報酬）與 uncond"
                                      "（無條件對照）兩組 summarize_returns() 結果；合併池 uncond 是把"
                                      "八國各自的無條件月報酬序列直接併起來重算，不是八國 uncond 數字"
                                      "的平均。",
        "group_stats": "no_recession/recession_after/recession_during 三組（2026-09-17 拆分，取代原本"
                        "二分的 has_recession/no_recession），pooled 八國事件直接合併（不分國家），"
                        "含 by_h（同 summarize_returns 結構）與 mdd12_median。",
        "avg_path_pooled/avg_path_us": "no_recession/recession_after/recession_during 三條平均路徑"
                                        "（31 個點，offset -6..24，事件月＝100），avg_path_us 只用美國事件。",
        "scatter_pre": "每個事件一點：x＝R(-6)，y＝R(12)，recession_group 決定顏色，對應頁面圖 3。",
        "scatter_decline": "每個事件一點：x＝事件後 12 個月利率總降幅（pp），y＝R(12)，對應頁面圖 4"
                            "（圖 4 仍用二分：recession_group != no_recession 視為有衰退）。",
        "country_group_medians": "逐國 no_recession_median/recession_after_median/recession_during_median"
                                  "＋各自事件數，對應頁面圖 5。",
        "recent_rows": "美國最近兩次（2019 年那次＋2024 年那次）＋其他國家 2024 年出現的第一次降息，"
                       "ret_to_date＝事件月到 as_of（各國股價資料最新一筆）的 log 報酬。",
        "recent_note": "cc -> {name, event_month}，該國最近一次第一次降息不在 2024 年，未列進 "
                        "recent_rows，供頁面附註用。",
    }
    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "h_list": H_LIST, "primary_h": PRIMARY_H,
        "window_pre": WINDOW_PRE, "window_post": WINDOW_POST,
        "hike_threshold": HIKE_THRESHOLD, "cut_threshold": CUT_THRESHOLD,
        "cycle_max_months": CYCLE_MAX_MONTHS, "cut_max_months": CUT_MAX_MONTHS,
        "event_group_months": EVENT_GROUP_MONTHS,
        "schema_notes": schema_notes,
        "countries": {cc: {k: v for k, v in d.items() if k != "_price_m"} for cc, _n, d in countries_data},
        "table1_rows": table1_rows, "table1_pooled": table1_pooled,
        "group_stats": group_stats,
        "avg_path_pooled": avg_path_pooled, "avg_path_us": avg_path_us,
        "scatter_pre": scatter_pre, "scatter_decline": scatter_decline,
        "country_group_medians": country_group_medians,
        "recent_rows": recent_rows, "recent_note": recent_note,
    }
    DATA.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    info(f"寫入 {OUT_JSON}")

    built_date = datetime.now().strftime("%Y-%m-%d")
    html_out = generate_html(countries_data, table1_rows, table1_pooled, group_stats,
                              avg_path_pooled, avg_path_us, scatter_pre, scatter_decline,
                              country_group_medians, recent_rows, recent_note, built_date)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_out, encoding="utf-8")
    info(f"寫入 {OUT_HTML}")

    h12 = table1_pooled[PRIMARY_H]
    info(f"合併池 H=12：事件數={h12['cond']['n']} 中位數={h12['cond']['median']} "
         f"無條件中位數={h12['uncond']['median']}")
    info(f"無衰退 n={group_stats['no_recession']['n']} 衰退之後才開始 n={group_stats['recession_after']['n']} "
         f"已在衰退中 n={group_stats['recession_during']['n']}")
    _strip_internal(countries_data)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="央行第一次降息 × 股市 跨國回測 builder")
    ap.add_argument("--fetch", action="store_true", help="只抓序列存 raw json")
    ap.add_argument("--debug", action="store_true", help="只算並印出摘要，不寫 HTML")
    args = ap.parse_args()
    if args.fetch:
        do_fetch()
    elif args.debug:
        cd = do_compute()
        for cc, name, d in cd:
            if d.get("status") != "ok":
                print(f"{cc} {name}: {d.get('status')}")
                continue
            print(f"\n=== {cc} {name} ({d['sample_start']}~{d['sample_end']}) events={len(d['events'])} ===")
            for e in d["events"]:
                print(f"  peak={e['peak_month']}({e['peak_val']:.2f}) -> event={e['event_month']}"
                      f"({e['event_val']:.2f}) group={e['recession_group']} rec_NBER={e['has_recession_nber']}"
                      f" r6={e['r6']} r12={e['r12']} r24={e['r24']} r_pre6={e['r_pre6']} mdd12={e['mdd12']}")
    else:
        do_compute_and_build()

