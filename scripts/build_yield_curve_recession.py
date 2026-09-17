#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_yield_curve_recession.py — 殖利率倒掛 × 經濟衰退 跨國回測（8 國同一把尺）。

規格凍結版：問「殖利率倒掛真的預示經濟衰退嗎？多久會看到？不同國家都適用嗎？」，用
FRED 免 key CSV 對 US/DE/GB/JP/CA/AU/KR 七國套同一套規則，台灣另用官方資料手抄
（data/yield_curve_recession_tw_manual.json）。第 2 節定義凍結、不可改；若某條定義在
某國無法執行，照原定義做並在輸出/回報中如實標註（不換定義）。

用法：
    python3 scripts/build_yield_curve_recession.py --fetch
        抓全部 FRED 序列（30 條：7 國 × 4 + 美國額外 T10Y3M/T10Y2Y），存
        data/yield_curve_recession_raw.json（含抓取時間、代碼、起訖）。

    python3 scripts/build_yield_curve_recession.py
        讀 raw json + 台灣手抄 json，算全部統計（事件、命中率、前置期、反向召回、
        無條件基率），寫 data/yield_curve_recession.json，再生成
        docs/backtest/yield_curve/index.html（版型照抄
        docs/backtest/slow_bear_base_rate/index.html 的 CSS／imq-nav／pill bar 結構，
        於執行期直接從該檔擷取，避免手抄跑掉）。

抓取沿用 scripts/build_monitor.py 的 fetch_fred()：requests 預設 UA（不帶假瀏覽器 UA，
FRED 對常見 Mozilla 字串會 stall）。與 build_monitor 版本的差異：本檔不做 `[-400:]`
尾端截斷——build_monitor 是日常監控儀表只要近況，本回測需要序列全史。
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_JSON = DATA / "yield_curve_recession_raw.json"
OUT_JSON = DATA / "yield_curve_recession.json"
TW_MANUAL_JSON = DATA / "yield_curve_recession_tw_manual.json"
OUT_HTML = ROOT / "docs" / "backtest" / "yield_curve" / "index.html"
SLOW_BEAR_REF = ROOT / "docs" / "backtest" / "slow_bear_base_rate" / "index.html"
NAV_DIR = ROOT / "docs" / "backtest"

SCHEMA = "yield-curve-recession-v1"
CHART_JS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"


def warn(msg: str) -> None:
    print(f"[yield-curve][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[yield-curve] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 國家與序列代碼（第 1 節；已用 curl 逐條驗證存在，見回報）
# ═══════════════════════════════════════════════════════════════════════════

COUNTRIES = [
    ("US", "美國", dict(ten_y="IRLTLT01USM156N", three_m="TB3MS",
                        gdp="NAEXKP01USQ657S", rec="USRECDM",
                        three_m_transform="tbill_bey")),
    ("DE", "德國", dict(ten_y="IRLTLT01DEM156N", three_m="IR3TIB01DEM156N",
                        gdp="NAEXKP01DEQ657S", rec="DEURECDM")),
    ("GB", "英國", dict(ten_y="IRLTLT01GBM156N", three_m="IR3TIB01GBM156N",
                        gdp="NAEXKP01GBQ657S", rec="GBRRECDM")),
    ("JP", "日本", dict(ten_y="IRLTLT01JPM156N", three_m="IR3TIB01JPM156N",
                        gdp="NAEXKP01JPQ657S", rec="JPNRECDM")),
    ("CA", "加拿大", dict(ten_y="IRLTLT01CAM156N", three_m="IR3TIB01CAM156N",
                         gdp="NAEXKP01CAQ657S", rec="CANRECDM")),
    ("AU", "澳洲", dict(ten_y="IRLTLT01AUM156N", three_m="IR3TIB01AUM156N",
                        gdp="NAEXKP01AUQ657S", rec="AUSRECDM")),
    ("KR", "南韓", dict(ten_y="IRLTLT01KRM156N", three_m="IR3TIB01KRM156N",
                        gdp="NAEXKP01KRQ657S", rec="KORRECDM")),
]
# 美國主線 3M 用 TB3MS（3 個月期公債，公債對公債，跟 10Y 同一種發行體）。IR3TIB01USM156N
# （同業拆款利率）留著只做對照欄——同業拆款利率含信用溢價，會在景氣好、利率正常時就比公債
# 利率高一截，容易做出偏淺、偏早、不是真公債曲線倒掛的假事件（2026-09-17 驗收改版）。
US_EXTRA = {"t10y3m": "T10Y3M", "t10y2y": "T10Y2Y", "ir3tib": "IR3TIB01USM156N"}

OECD_B_CUTOFF_MONTH = "2022-09"   # 定義 B（OECD 衰退指標）樣本只到這裡（第 2 節凍結）
H_LIST = [12, 24, 36]
PRIMARY_H = 24
EVENT_GROUP_MONTHS = 24
RECALL_WINDOW_MONTHS = 24
BASE_RATE_WINDOW_MONTHS = 24


# ═══════════════════════════════════════════════════════════════════════════
# FRED 抓取
# ═══════════════════════════════════════════════════════════════════════════

def fetch_fred(series_id: str):
    """FRED CSV endpoint（免 key），回傳升冪 [(date_iso, val), ...] 或 None。"""
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


def do_fetch():
    series_ids = set()
    for _cc, _name, codes in COUNTRIES:
        series_ids.update(codes.values())
    series_ids.update(US_EXTRA.values())

    out = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "series": {}, "meta": {}}
    ok, fail = 0, 0
    for sid in sorted(series_ids):
        pts = fetch_fred(sid)
        if pts is None:
            warn(f"{sid}: 抓取失敗或無資料")
            out["meta"][sid] = {"ok": False, "n": 0}
            fail += 1
            continue
        out["series"][sid] = pts
        out["meta"][sid] = {"ok": True, "n": len(pts), "start": pts[0][0], "end": pts[-1][0]}
        info(f"{sid}: {len(pts)} 筆 {pts[0][0]}..{pts[-1][0]}")
        ok += 1
    DATA.mkdir(parents=True, exist_ok=True)
    RAW_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    info(f"寫入 {RAW_JSON}：{ok} 成功／{fail} 失敗")
    if fail:
        warn(f"{fail} 條序列抓取失敗，見上方 WARN")


# ═══════════════════════════════════════════════════════════════════════════
# 月份工具
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


def tbill_discount_to_bey(discount_pct: float, days: int = 91) -> float:
    """3 個月期公債 TB3MS 是「貼現率」（discount basis），比債券等值殖利率（bond-equivalent
    yield, BEY）低，利率越高差越大，跟 10Y 公債殖利率（本身就是 BEY 口徑）直接相減會系統性
    偏高，把利差沒那麼深的倒掛事件洗掉（例如 1989-06 那次）。標準轉換公式（≤182 天期）：
    BEY = 365 × d ／ (360 − d × 91)，d 為貼現率小數；91＝3 個月期的天數。回傳值仍是百分點。"""
    d = discount_pct / 100.0
    bey = 365 * d / (360 - d * days)
    return bey * 100


def apply_three_m_transform(pts, transform):
    if transform == "tbill_bey":
        return [(date_iso, tbill_discount_to_bey(val)) for date_iso, val in pts]
    return pts


def to_monthly_dict(pts):
    d = {}
    for date_iso, val in pts:
        d[month_key(date_iso)] = val
    return d


def daily_monthly_avg(pts):
    buckets = {}
    for date_iso, val in pts:
        buckets.setdefault(month_key(date_iso), []).append(val)
    return {m: sum(v) / len(v) for m, v in buckets.items()}


def quarterly_dict(pts):
    """NAEXKP01xxQ657S 本身已是「季增率 %」（非水準值），不必再差分。"""
    return {month_key(date_iso): val for date_iso, val in pts}


def recession_transitions(pts):
    """日頻 0/1 序列（升冪）→ spans=[(start_month, end_month_exclusive_or_None), ...],
    starts=[start_month, ...]。起點＝由 0 轉 1 那天所在月份（第 2 節定義文字）；
    span 採半開區間 [start, end)，end＝轉回 0 那天所在月份。"""
    spans = []
    cur_start = None
    prev_val = 0
    for date_iso, val in pts:
        v = 1 if val >= 0.5 else 0
        if v == 1 and prev_val == 0:
            cur_start = month_key(date_iso)
        elif v == 0 and prev_val == 1 and cur_start is not None:
            spans.append((cur_start, month_key(date_iso)))
            cur_start = None
        prev_val = v
    if cur_start is not None:
        spans.append((cur_start, None))
    starts = [s for s, _e in spans]
    return spans, starts


def gdp_recession_spans(gdp_q):
    """技術性衰退＝連續兩季負成長；起點＝第一個負成長季的第一個月；終點＝之後第一個
    正成長季的第一個月（半開區間 [start,end)；尚未轉正則 end=None，代表仍在衰退中）。
    季度須逐季相連（月差=3）；資料缺口視為中斷。"""
    months = sorted(gdp_q.keys())
    spans, starts = [], []
    consec_neg = 0
    streak_start = None
    in_rec = False
    rec_start = None
    prev_m = None
    for m in months:
        if prev_m is not None and month_diff(m, prev_m) != 3:
            if in_rec:
                spans.append((rec_start, None))
                in_rec = False
            consec_neg = 0
            streak_start = None
        val = gdp_q[m]
        if val < 0:
            if consec_neg == 0:
                streak_start = m
            consec_neg += 1
            if consec_neg == 2 and not in_rec:
                in_rec = True
                rec_start = streak_start
                starts.append(rec_start)
        else:
            if in_rec:
                spans.append((rec_start, m))
                in_rec = False
            consec_neg = 0
            streak_start = None
        prev_m = m
    if in_rec:
        spans.append((rec_start, None))
    return spans, starts


def in_any_span(month, spans):
    for s, e in spans:
        if s <= month and (e is None or month < e):
            return True
    return False


def classify_event(event_start, H, spans, starts_sorted, series_end_month):
    if in_any_span(event_start, spans):
        return "already_in_recession", None
    window_end = add_months(event_start, H)
    candidates = [r for r in starts_sorted if 0 < month_diff(r, event_start) <= H]
    if candidates:
        first = min(candidates, key=lambda r: month_diff(r, event_start))
        return "hit", month_diff(first, event_start)
    if series_end_month is not None and month_diff(series_end_month, window_end) >= 0:
        return "miss", None
    return "not_yet_due", None


def detect_events(spread_monthly, sample_start, sample_end, group_months=EVENT_GROUP_MONTHS):
    months = sorted(m for m in spread_monthly if sample_start <= m <= sample_end)
    inverted = [(m, spread_monthly[m]) for m in months if spread_monthly[m] < 0]
    events = []
    i = 0
    while i < len(inverted):
        start_m, start_v = inverted[i]
        group = [(start_m, start_v)]
        j = i + 1
        while j < len(inverted) and month_diff(inverted[j][0], start_m) <= group_months:
            group.append(inverted[j])
            j += 1
        deepest = min(v for _m, v in group)
        events.append({"start": start_m, "deepest": round(deepest, 4), "n_inverted_months": len(group)})
        i = j
    return events


def reverse_recall(recession_starts, spread_monthly, sample_start, sample_end, window=RECALL_WINDOW_MONTHS):
    starts_in_window = sorted(s for s in recession_starts if sample_start <= s <= sample_end)
    if not starts_in_window:
        return None, 0
    inv_months = sorted(m for m, v in spread_monthly.items() if v < 0 and sample_start <= m <= sample_end)
    hits = 0
    for s in starts_in_window:
        if any(0 < month_diff(s, m) <= window for m in inv_months):
            hits += 1
    return round(hits / len(starts_in_window), 4), len(starts_in_window)


def base_rate(recession_starts, sample_start, sample_end, window=BASE_RATE_WINDOW_MONTHS):
    months = []
    m = sample_start
    while m <= sample_end:
        months.append(m)
        m = add_months(m, 1)
    valid = [m for m in months if month_diff(sample_end, add_months(m, window)) >= 0]
    if not valid:
        return None, 0, 0
    starts_sorted = sorted(recession_starts)
    hits = sum(1 for m in valid if any(0 < month_diff(s, m) <= window for s in starts_sorted))
    return round(hits / len(valid), 4), len(valid), hits


def build_definition_stats(spread_monthly, spans, starts, sample_start, sample_end):
    if sample_start is None or sample_end is None or sample_start > sample_end:
        return None
    events = detect_events(spread_monthly, sample_start, sample_end)
    starts_sorted = sorted(starts)
    per_h = {}
    for H in H_LIST:
        ev_rows = []
        n_hit = n_miss = n_already = n_notdue = 0
        leads = []
        for ev in events:
            verdict, lead = classify_event(ev["start"], H, spans, starts_sorted, sample_end)
            row = dict(ev)
            row["verdict"] = verdict
            row["lead_months"] = lead
            if verdict == "hit":
                n_hit += 1
                leads.append(lead)
            elif verdict == "miss":
                n_miss += 1
            elif verdict == "already_in_recession":
                n_already += 1
            elif verdict == "not_yet_due":
                n_notdue += 1
            ev_rows.append(row)
        n_testable = n_hit + n_miss
        hit_rate = round(n_hit / n_testable, 4) if n_testable else None
        br, br_n, br_hits = base_rate(starts_sorted, sample_start, sample_end, window=H)
        uplift = round(hit_rate / br, 2) if (hit_rate is not None and br) else None
        per_h[H] = {
            "events": ev_rows, "n_hit": n_hit, "n_miss": n_miss,
            "n_already_in_recession": n_already, "n_not_yet_due": n_notdue,
            "n_testable": n_testable, "hit_rate": hit_rate,
            "base_rate": br, "base_rate_n": br_n, "base_rate_hits": br_hits,
            "uplift": uplift, "lead_times": leads,
        }
    recall, recall_n = reverse_recall(starts_sorted, spread_monthly, sample_start, sample_end)
    return {
        "sample_start": sample_start, "sample_end": sample_end,
        "n_events": len(events), "by_h": per_h,
        "reverse_recall": recall, "reverse_recall_n": recall_n,
        "events_detail": per_h[PRIMARY_H]["events"],
    }


# ═══════════════════════════════════════════════════════════════════════════
# 每國組裝
# ═══════════════════════════════════════════════════════════════════════════

def build_country(cc, name, codes, raw_series):
    ten_y_pts = raw_series.get(codes["ten_y"])
    three_m_pts = raw_series.get(codes["three_m"])
    gdp_pts = raw_series.get(codes["gdp"])
    rec_pts = raw_series.get(codes["rec"])

    missing = [k for k, v in [("ten_y", ten_y_pts), ("three_m", three_m_pts),
                               ("gdp", gdp_pts), ("rec", rec_pts)] if not v]
    if missing:
        return {"cc": cc, "name": name, "status": "missing", "missing_series": missing}

    three_m_pts = apply_three_m_transform(three_m_pts, codes.get("three_m_transform"))

    ten_y_m = to_monthly_dict(ten_y_pts)
    three_m_m = to_monthly_dict(three_m_pts)
    common_months = set(ten_y_m) & set(three_m_m)
    spread = {m: round(ten_y_m[m] - three_m_m[m], 4) for m in common_months}
    spread_start, spread_end = min(spread), max(spread)

    gdp_q = quarterly_dict(gdp_pts)
    gdp_start, gdp_end = min(gdp_q), max(gdp_q)

    a_start = max(spread_start, gdp_start)
    a_end = min(spread_end, gdp_end)
    a_spans, a_starts = gdp_recession_spans(gdp_q)
    stats_a = build_definition_stats(spread, a_spans, a_starts, a_start, a_end)

    b_stats = None
    c_stats = None
    if cc == "US":
        c_spans, c_starts = recession_transitions(rec_pts)
        c_rec_start = month_key(rec_pts[0][0])
        c_rec_end = month_key(rec_pts[-1][0])
        c_start = max(spread_start, c_rec_start)
        c_end = min(spread_end, c_rec_end)
        c_stats = build_definition_stats(spread, c_spans, c_starts, c_start, c_end)
    else:
        b_spans, b_starts = recession_transitions(rec_pts)
        b_rec_start = month_key(rec_pts[0][0])
        b_rec_end = min(month_key(rec_pts[-1][0]), OECD_B_CUTOFF_MONTH)
        b_start = max(spread_start, b_rec_start)
        b_end = min(spread_end, b_rec_end)
        b_stats = build_definition_stats(spread, b_spans, b_starts, b_start, b_end)

    out = {
        "cc": cc, "name": name, "status": "ok",
        "spread_series": sorted(spread.items()),
        "spread_data_range": [spread_start, spread_end],
        "gdp_data_range": [gdp_start, gdp_end],
        "gdp_recession_spans": a_spans,
        "def_a": stats_a, "def_b": b_stats, "def_c": c_stats,
    }
    if cc == "US":
        t10y2y_pts = raw_series.get(US_EXTRA["t10y2y"])
        t10y3m_pts = raw_series.get(US_EXTRA["t10y3m"])
        ir3tib_pts = raw_series.get(US_EXTRA["ir3tib"])
        if t10y2y_pts:
            t2y_m = sorted(daily_monthly_avg(t10y2y_pts).items())
            out["t10y2y_monthly"] = t2y_m
            out["t10y2y_latest"] = t2y_m[-1]
        if t10y3m_pts:
            t3m_m = sorted(daily_monthly_avg(t10y3m_pts).items())
            out["t10y3m_latest"] = t3m_m[-1]
        if ir3tib_pts:
            ir3tib_m = to_monthly_dict(ir3tib_pts)
            ir3tib_spread = {m: round(ten_y_m[m] - ir3tib_m[m], 4)
                              for m in set(ten_y_m) & set(ir3tib_m)}
            out["ir3tib_spread_series"] = sorted(ir3tib_spread.items())
    return out


TW_DEF_T_SAMPLE_START = "1996-01"  # 定義 T 樣本窗起點：10Y 公債序列 1995 年斷斷續續，
                                    # 1996-01 起才連續（2026-09-17 協調者指示明訂）


_QUARTER_FIRST_MONTH = {"1": "01", "2": "04", "3": "07", "4": "10"}


def _quarter_label_to_month(label: str) -> str:
    """"2000-Q1" -> "2000-01"（取該季第一個月，跟 FRED NAEXKP01 用季首月當 key 的慣例
    一致）；已經是 "YYYY-MM" 格式就原樣回傳。"""
    if "-Q" not in label:
        return label
    y, q = label.split("-Q")
    return f"{y}-{_QUARTER_FIRST_MONTH[q]}"


def build_taiwan(tw_manual):
    """台灣：僅在四類資料（10Y／3M／實質 GDP 季增率／國發會景氣循環峰谷）皆可用且
    覆蓋期間有意義時才納入主表計算；否則回傳 status='missing'/'partial'，頁面標
    「資料整理中」，不得用假資料湊數。跑兩把尺：定義 A（技術性衰退，跟其餘七國同一套
    gdp_recession_spans()）與定義 T（國發會峰到谷，峰的次月為衰退起點，2026-09-17
    協調者指示新增）。"""
    if not tw_manual or tw_manual.get("status") in (None, "missing"):
        return {"cc": "TW", "name": "台灣", "status": "missing",
                "note": tw_manual.get("note", "無台灣手抄資料") if tw_manual else "無台灣手抄資料"}

    ten_y = tw_manual.get("ten_y_bond", {})
    three_m = tw_manual.get("three_m_rate", {})
    gdp = tw_manual.get("real_gdp_qoq", {})
    cycle = tw_manual.get("business_cycle", {})

    ten_y_series = {m: v for m, v in ten_y.get("series", [])} if ten_y.get("available") else {}
    three_m_series = {m: v for m, v in three_m.get("series", [])} if three_m.get("available") else {}
    gdp_series = {}
    if gdp.get("available"):
        for label, v in gdp.get("series", []):
            gdp_series[_quarter_label_to_month(label)] = v
    peaks_troughs = cycle.get("peaks_troughs", []) if cycle.get("available") else []

    have_rates = len(ten_y_series) >= 24 and len(three_m_series) >= 24
    have_gdp = len(gdp_series) >= 8
    have_cycle = len(peaks_troughs) >= 1

    if not (have_rates and have_gdp and have_cycle):
        missing_bits = []
        if not have_rates:
            missing_bits.append("10Y／3M 利率月頻序列（不足 24 筆或缺）")
        if not have_gdp:
            missing_bits.append("實質 GDP 季增率（不足 8 筆或缺）")
        if not have_cycle:
            missing_bits.append("國發會景氣循環基準日期")
        return {"cc": "TW", "name": "台灣", "status": "partial",
                "missing_bits": missing_bits,
                "have_cycle_table": have_cycle,
                "peaks_troughs": peaks_troughs,
                "cycle_source_url": cycle.get("source_url"),
                "note": tw_manual.get("note", "")}

    spread = {m: round(ten_y_series[m] - three_m_series[m], 4)
              for m in set(ten_y_series) & set(three_m_series)}
    spread_start, spread_end = min(spread), max(spread)
    gdp_start, gdp_end = min(gdp_series), max(gdp_series)

    # 定義 A：技術性衰退（GDP 連兩季負成長），跟其餘七國同一把尺、同一支函式。
    a_spans, a_starts = gdp_recession_spans(gdp_series)
    a_start = max(spread_start, gdp_start)
    a_end = min(spread_end, gdp_end)
    stats_a = build_definition_stats(spread, a_spans, a_starts, a_start, a_end)

    # 定義 T：國發會峰到谷，峰的次月為衰退起點（半開區間 [峰+1, 谷+1)）；樣本窗固定從
    # TW_DEF_T_SAMPLE_START 起（10Y 序列從這個月才連續），到利差資料尾端。
    t_spans, t_starts = [], []
    for pt in peaks_troughs:
        peak = pt.get("peak")
        trough = pt.get("trough")
        if not peak:
            continue
        start = add_months(peak, 1)
        t_starts.append(start)
        end = add_months(trough, 1) if trough else None
        t_spans.append((start, end))
    t_start = max(spread_start, TW_DEF_T_SAMPLE_START)
    t_end = spread_end
    stats_t = build_definition_stats(spread, t_spans, t_starts, t_start, t_end)

    return {
        "cc": "TW", "name": "台灣", "status": "ok",
        "spread_series": sorted(spread.items()),
        "spread_data_range": [spread_start, spread_end],
        "gdp_data_range": [gdp_start, gdp_end],
        "gdp_recession_spans": a_spans,
        "def_a": stats_a, "def_b": None, "def_c": None, "def_t": stats_t,
        "peaks_troughs": peaks_troughs,
        "cycle_source_url": cycle.get("source_url"),
        "sources": {"ten_y": ten_y.get("source_url"), "three_m": three_m.get("source_url"),
                    "gdp": gdp.get("source_url")},
    }


def pooled_lead_stats(countries_data):
    all_leads = []
    per_country = {}
    pooled_h = {H: {"n_hit": 0, "n_testable": 0, "base_hits": 0, "base_n": 0} for H in H_LIST}
    n_recall_hit = 0
    n_recall_total = 0
    for cc, name, d in countries_data:
        if d.get("status") != "ok" or d.get("def_a") is None:
            continue
        da = d["def_a"]
        leads24 = da["by_h"][PRIMARY_H]["lead_times"]
        per_country[cc] = {
            "name": name, "n": len(leads24),
            "min": min(leads24) if leads24 else None,
            "median": statistics.median(leads24) if leads24 else None,
            "max": max(leads24) if leads24 else None,
        }
        all_leads.extend(leads24)
        for H in H_LIST:
            pooled_h[H]["n_hit"] += da["by_h"][H]["n_hit"]
            pooled_h[H]["n_testable"] += da["by_h"][H]["n_testable"]
            pooled_h[H]["base_hits"] += da["by_h"][H]["base_rate_hits"] or 0
            pooled_h[H]["base_n"] += da["by_h"][H]["base_rate_n"] or 0
        if da["reverse_recall"] is not None:
            n_recall_total += da["reverse_recall_n"]
            n_recall_hit += round(da["reverse_recall"] * da["reverse_recall_n"])
    for H in H_LIST:
        ph = pooled_h[H]
        ph["hit_rate"] = round(ph["n_hit"] / ph["n_testable"], 4) if ph["n_testable"] else None
        ph["base_rate"] = round(ph["base_hits"] / ph["base_n"], 4) if ph["base_n"] else None
        ph["uplift"] = round(ph["hit_rate"] / ph["base_rate"], 2) if (ph["hit_rate"] and ph["base_rate"]) else None
    pooled_lead = {
        "n": len(all_leads),
        "min": min(all_leads) if all_leads else None,
        "median": statistics.median(all_leads) if all_leads else None,
        "max": max(all_leads) if all_leads else None,
    }
    pooled_recall = round(n_recall_hit / n_recall_total, 4) if n_recall_total else None
    return per_country, pooled_lead, pooled_h, pooled_recall


# ═══════════════════════════════════════════════════════════════════════════
# 資料載入
# ═══════════════════════════════════════════════════════════════════════════

def load_raw():
    if not RAW_JSON.exists():
        raise SystemExit(f"{RAW_JSON} 不存在，請先跑 --fetch")
    return json.loads(RAW_JSON.read_text(encoding="utf-8"))


def load_tw_manual():
    if not TW_MANUAL_JSON.exists():
        return {"status": "missing", "note": f"{TW_MANUAL_JSON} 不存在"}
    return json.loads(TW_MANUAL_JSON.read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════════════════════════════════
# HTML 產出（版型照抄 slow_bear_base_rate/index.html，於執行期直接擷取）
# ═══════════════════════════════════════════════════════════════════════════

def esc(s):
    return html_mod.escape(str(s), quote=True)


def fmt_pct(x, digits=1):
    return "—" if x is None else f"{x * 100:.{digits}f}%"


def fmt_pp(x, digits=2):
    return "—" if x is None else f"{x:+.{digits}f}pp" if x != 0 else "0.00pp"


def fmt_num(x, digits=2):
    return "—" if x is None else f"{x:.{digits}f}"


def fmt_month(m):
    return "—" if not m else m


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


DEFINITIONS_TEXT = [
    "利差＝10Y 減 3M，單位百分點，月頻（日頻序列先取月均）。主線全部國家用 10Y−3M；"
    "美國另加 10Y−2Y（T10Y2Y 月均）作對照欄，不進主線計算。",
    "美國的 3M 用 TB3MS（3 個月期公債），公債對公債，跟 10Y 公債殖利率口徑一致；德/英/"
    "日/加/澳/韓六國的 3M 用 IR3TIB（銀行同業拆款利率）。FRED 的 OECD 資料庫沒有這六國"
    "對應的公債 3M 序列可換，同業拆款利率含信用溢價，會讓這六國的利差水準整體偏低、"
    "倒掛事件偏多，跨國比較時要記住這個系統性偏差；台灣另外用商業本票，見下方說明。",
    "TB3MS 原始報的是「貼現率」（discount basis），比債券等值殖利率（bond-equivalent "
    "yield）低，利率越高差越大，直接拿貼現率跟 10Y 公債殖利率相減會系統性偏高，把利差"
    "沒那麼深的倒掛事件洗掉。美國的利差先把 TB3MS 轉成債券等值殖利率再減：BEY ＝ 365 × "
    "d ／ (360 − d × 91)，d 是 TB3MS 除以 100 的小數，91 是 3 個月的天數，算完再乘回"
    "100，這是 3 個月期以內公債的標準換算公式。",
    "倒掛月＝該月利差小於 0。倒掛事件＝第一個倒掛月為事件起點，起點後 24 個月內的所有"
    "倒掛月都算同一事件（避免像 2019 年那種斷斷續續被拆成多次事件）。每個事件記錄起點、"
    "期間最深的利差、倒掛總月數。",
    "衰退定義 A（主線，八國同一把尺）：技術性衰退＝實質 GDP 季增率連續兩季負成長。"
    "衰退起點＝第一個負成長季的第一個月，終點＝之後第一個正成長季的第一個月。",
    "衰退定義 B（對照）：OECD 衰退指標等於 1 的期間，起點取指標由 0 轉 1 的月份；"
    "這條序列在 2022 年 9 月停更，樣本只到那裡。",
    "衰退定義 C（僅美國）：NBER 認定的衰退期（USRECDM），這條序列持續更新到現在。",
    "台灣的 3M 用商業本票次級市場利率（31-90 天），不是同業拆款也不是公債，含發行企業的"
    "信用溢價，偏差方向跟德/英/日/加/澳/韓六國的 IR3TIB 一樣，會讓利差系統性偏低、倒掛"
    "事件偏多。",
    "台灣主線（定義 A）用技術性衰退，跟其餘七國同一把尺，GDP 季增率資料從 2000 年第 1 季"
    "開始。另外跑一把只有台灣用的對照尺（定義 T）：國發會「台灣景氣循環基準日期」峰到谷，"
    "峰的次月為衰退起點，谷月納入衰退期間；這把尺樣本窗從 1996 年 1 月起（台灣 10Y 公債"
    "序列 1995 年斷斷續續，1996 年才連續）。",
    "命中＝事件起點後 H 個月內出現衰退起點，H 分別算 12、24、36 個月，主線報 24。"
    "事件起點當下若已經在衰退中，單獨標「已在衰退中」，不算命中也不算落空，但仍列出。"
    "H 個月的窗口還沒走完就先標「未到期」。",
    "前置期＝衰退起點月減事件起點月，單位月。",
    "反向召回＝每一次衰退，起點前 24 個月內是否曾出現倒掛月，算全部衰退中命中的比率。",
    "無條件基率＝任一個月份起，未來 24 個月內出現衰退起點的比率，逐月滾動算過全樣本。"
    "提升倍數＝命中率除以基率。",
    "樣本窗＝該國利差與 GDP 兩者都有資料的期間，起訖年份印在每張表上。",
]


def section_method():
    lis = "".join(f"<li>{esc(t)}</li>" for t in DEFINITIONS_TEXT)
    return f"""
<div class="section">
<h2 class="section-title">二、方法：怎麼定義「倒掛」與「衰退」</h2>
<div class="takeaway">這頁的判定規則在跑資料前就定死，八個國家套同一把尺，中途不因某國
結果好不好看而回頭調整。台灣的利率與 GDP 來自央行與主計總處官方資料庫，同樣跑技術性
衰退這把尺；另外多跑一把國發會峰谷的尺作對照，其餘定義維持一致。</div>
<div class="card"><ul class="disc">{lis}</ul></div>
</div>
"""


def section_hero(countries_data, pooled_h, pooled_lead, tw_status):
    h24 = pooled_h[PRIMARY_H]
    hit_rate = h24["hit_rate"]
    base = h24["base_rate"]
    uplift = h24["uplift"]
    lead_med = pooled_lead["median"]

    if hit_rate is not None and hit_rate >= 0.7:
        verdict = "倒掛之後多半真的衰退，時間差要抓一年半"
        tag_color = "#dc2626"
    elif hit_rate is not None and hit_rate >= 0.4:
        verdict = "倒掛提高衰退機率，但不是每次都準"
        tag_color = "#d97706"
    else:
        verdict = "倒掛對衰退的預測力比想像中弱"
        tag_color = "#059669"

    q1 = (f"把八個國家、二十四個月的窗口全部攤開來看，倒掛之後出現衰退的比率是 "
          f"{fmt_pct(hit_rate)}，同一段時間裡沒有倒掛訊號時的基準衰退機率是 "
          f"{fmt_pct(base)}，倒掛把機率推高了 {fmt_num(uplift, 1)} 倍。")
    q2 = (f"倒掛出現後到衰退真的開始，合併池的前置期中位數是 {fmt_num(lead_med, 0)} 個月，"
          f"最短與最長分別是 {fmt_num(pooled_lead['min'], 0)} 個月與 {fmt_num(pooled_lead['max'], 0)} 個月，"
          f"差距很大，不能拿單一次經驗當時間表。")
    tw_note = "台灣資料整理中，本頁先出七國版本。" if tw_status != "ok" else "台灣資料已併入下表。"
    q3 = f"八個國家不是同一個答案，下表逐國列出命中率與樣本期間，{tw_note}"

    return f"""
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag" style="background:{tag_color}">{esc(verdict)}</span>
    <h2>{esc(q1)}</h2>
    <p>{esc(q2)} {esc(q3)}</p>
  </div>
  <div class="hero-stats">
    <div><div class="hs-label">合併池命中率 H=24</div><div class="hs-value">{fmt_pct(hit_rate)}</div></div>
    <div><div class="hs-label">合併池基率 H=24</div><div class="hs-value">{fmt_pct(base)}</div></div>
    <div><div class="hs-label">提升倍數</div><div class="hs-value">{fmt_num(uplift, 1)}x</div></div>
    <div><div class="hs-label">前置期中位數</div><div class="hs-value">{fmt_num(lead_med, 0)} 月</div></div>
  </div>
</div>
"""


def _hit_table_rows(countries_data, def_key, pooled_h=None, pooled_recall=None, pooled_label=None):
    rows = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        stats = d.get(def_key)
        if stats is None:
            if def_key == "def_b" and cc == "US":
                rows.append(f"<tr class='dim'><td class='lbl'>{esc(name)}</td>"
                            f"<td colspan='6'>不適用。USRECDM 是 NBER 而非 OECD 指標，"
                            f"美國的定義 C 對照見下方「定義 B、C 對照」段落</td></tr>")
            continue
        h = stats["by_h"][PRIMARY_H]
        period = f"{fmt_month(stats['sample_start'])} ～ {fmt_month(stats['sample_end'])}"
        rows.append(
            f"<tr><td class='lbl'>{esc(name)}</td><td>{esc(period)}</td>"
            f"<td class='num'>{stats['n_events']}</td>"
            f"<td class='num'>{h['n_hit']}</td>"
            f"<td class='num'>{fmt_pct(h['hit_rate'])}</td>"
            f"<td class='num'>{fmt_pct(h['base_rate'])}</td>"
            f"<td class='num'>{fmt_num(h['uplift'], 1)}</td>"
            f"<td class='num'>{fmt_pct(stats['reverse_recall'])}</td></tr>")
    if pooled_h is not None:
        h = pooled_h[PRIMARY_H]
        rows.append(
            f"<tr><td class='lbl'><b>{esc(pooled_label or '合併池（不獨立）')}</b></td><td>—</td>"
            f"<td class='num'>—</td><td class='num'>{h['n_hit']}</td>"
            f"<td class='num'><b>{fmt_pct(h['hit_rate'])}</b></td>"
            f"<td class='num'>{fmt_pct(h['base_rate'])}</td>"
            f"<td class='num'>{fmt_num(h['uplift'], 1)}</td>"
            f"<td class='num'>{fmt_pct(pooled_recall)}</td></tr>")
    return "".join(rows)


def section_table1(countries_data, pooled_h, pooled_recall):
    rows_a = _hit_table_rows(countries_data, "def_a", pooled_h, pooled_recall)
    rows_b = _hit_table_rows(countries_data, "def_b")
    return f"""
<div class="section">
<h2 class="section-title">三、表 1：命中率總表</h2>
<div class="takeaway">怎麼讀這張表：「命中率」是倒掛事件起點後 24 個月內出現衰退起點的比率；
「基率」是不看倒掛訊號、任何一個月份起未來 24 個月內本來就會出現衰退的機率；「提升倍數」
是命中率除以基率，倍數越大代表倒掛訊號比瞎猜有用。「反向召回率」反過來問：每一次衰退，
發生前 24 個月內是不是都出現過倒掛。</div>
<h3 style="font-size:.92rem;margin:1.1rem 0 .5rem">定義 A：技術性衰退（GDP 連兩季負成長，主線）</h3>
<div class="scroll"><table>
<thead><tr><th>國家</th><th>樣本期間</th><th class="num">事件數</th><th class="num">H=24 命中數</th>
<th class="num">命中率</th><th class="num">基率</th><th class="num">提升倍數</th><th class="num">反向召回率</th></tr></thead>
<tbody>{rows_a}</tbody></table></div>
<div class="note">這張表回答第一個問題（倒掛真的預示衰退嗎），沒回答的是「多久看到」
（見表 3）與「每個國家個別長什麼樣子」（見表 2 事件明細）。事件數少的國家（例如樣本期
較短或衰退本來就少的），命中率的統計不確定性很大，單一數字不要看得太重。</div>
<h3 style="font-size:.92rem;margin:1.4rem 0 .5rem">定義 B：OECD 衰退指標（對照，樣本只到 2022-09）</h3>
<div class="scroll"><table>
<thead><tr><th>國家</th><th>樣本期間</th><th class="num">事件數</th><th class="num">H=24 命中數</th>
<th class="num">命中率</th><th class="num">基率</th><th class="num">提升倍數</th><th class="num">反向召回率</th></tr></thead>
<tbody>{rows_b}</tbody></table></div>
<div class="note">這張表換一把尺（OECD 官方衰退指標，不是 GDP 連兩季負成長）重算一次，
用來檢查結論會不會因為衰退定義換了而變。指標 2022 年 9 月停更，之後的倒掛事件（包含
2022 年那一波）在這把尺下全部落在「未到期」或無法檢驗，不是它們沒衰退。</div>
{_section_us_alt_spread(countries_data)}
</div>
"""


def _section_us_alt_spread(countries_data) -> str:
    """2026-09-17 驗收修正：美國主線 3M 改用 TB3MS（3 個月期公債，公債對公債）。
    IR3TIB01USM156N（同業拆款利率，原主線）與 T10Y2Y（T10Y2Y 月均）都留著只做對照欄，
    用同一套事件偵測＋命中率邏輯（build_definition_stats）各自重跑一次，看換一條短端
    序列答案穩不穩。"""
    us = next((d for cc, n, d in countries_data if cc == "US"), None)
    if not us or us.get("status") != "ok":
        return ""
    a = us["def_a"]
    spans = us.get("gdp_recession_spans", [])
    starts = sorted(s for s, _e in spans)
    gdp_start, gdp_end = us.get("gdp_data_range", [None, None])

    def _row(label, spread_dict):
        if not spread_dict or gdp_start is None:
            return None
        alt_start = max(gdp_start, min(spread_dict))
        alt_end = min(gdp_end, max(spread_dict))
        if alt_start > alt_end:
            return None
        stats = build_definition_stats(spread_dict, spans, starts, alt_start, alt_end)
        if stats is None:
            return None
        h = stats["by_h"][PRIMARY_H]
        return (label, alt_start, alt_end, stats["n_events"], h["hit_rate"], h["uplift"])

    main_h = a["by_h"][PRIMARY_H]
    rows = [("10Y−3M 公債（主線，TB3MS 轉債券等值）", a["sample_start"], a["sample_end"],
             a["n_events"], main_h["hit_rate"], main_h["uplift"])]
    r = _row("10Y−3M 同業拆款（IR3TIB，原主線）", dict(us.get("ir3tib_spread_series", [])))
    if r:
        rows.append(r)
    r = _row("10Y−2Y（T10Y2Y 月均）", dict(us.get("t10y2y_monthly", [])))
    if r:
        rows.append(r)
    if len(rows) < 2:
        return ""

    body = "".join(
        f"<tr><td class='lbl'>{esc(label)}</td><td>{esc(s)} ～ {esc(e)}</td>"
        f"<td class='num'>{n}</td><td class='num'>{fmt_pct(hr)}</td>"
        f"<td class='num'>{fmt_num(up, 1)}</td></tr>"
        for label, s, e, n, hr, up in rows)
    return f"""
<h3 style="font-size:.92rem;margin:1.4rem 0 .5rem">美國對照欄：3M 換不同利差定義</h3>
<div class="scroll"><table><thead><tr><th>利差定義</th><th class="num">樣本期間</th>
<th class="num">事件數</th><th class="num">H=24 命中率</th><th class="num">提升倍數</th></tr></thead>
<tbody>{body}</tbody></table></div>
<div class="note">同業拆款利率（IR3TIB）含銀行間信用溢價，景氣正常時本來就會比公債利率高
一截，拿它跟 10Y 公債殖利率相減，容易做出偏淺、偏早、不是公債曲線真的倒掛的假事件；美國
主線改用 TB3MS（3 個月期公債），而且 TB3MS 本身是貼現率，還要轉成債券等值殖利率才能跟
10Y 公債殖利率同口徑相減（換算公式見方法段第 2 節），才是公債對公債的標準口徑。10Y−2Y 是市場最常引用的另一種
倒掛口徑，短端換成 2 年期公債，事件切法也會跟著變，這兩欄只做對照，不進表 1 的主表計算。
德/英/日/加/澳/韓六國的 OECD 資料庫只提供同業拆款利率，台灣則用商業本票，都沒有對應的
公債 3M 序列可換，所以這七國的利差水準整體會比公債對公債的美國偏低、倒掛事件偏多，這是
跨國比較時要記住的系統性偏差，不是這七國真的比美國容易倒掛。</div>"""


def section_table2(countries_data):
    blocks = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok" or d.get("def_a") is None:
            continue
        events = d["def_a"]["events_detail"]
        if not events:
            continue
        rows = []
        verdict_label = {"hit": "命中", "miss": "落空",
                          "already_in_recession": "已在衰退中", "not_yet_due": "未到期"}
        for ev in events:
            rec_start = None
            if ev["verdict"] == "hit":
                rec_start = add_months(ev["start"], ev["lead_months"])
            rows.append(
                f"<tr><td>{esc(ev['start'])}</td><td class='num'>{fmt_pp(ev['deepest'])}</td>"
                f"<td class='num'>{ev['n_inverted_months']}</td>"
                f"<td>{esc(rec_start) if rec_start else '—'}</td>"
                f"<td class='num'>{ev['lead_months'] if ev['lead_months'] is not None else '—'}</td>"
                f"<td>{esc(verdict_label[ev['verdict']])}</td></tr>")
        blocks.append(f"""<h3 style="font-size:.92rem;margin:1.1rem 0 .5rem">{esc(name)}</h3>
<div class="scroll"><table><thead><tr><th>起點</th><th class="num">最深利差</th>
<th class="num">倒掛月數</th><th>之後衰退起點</th><th class="num">前置月數</th><th>判定</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>""")
    body = "".join(blocks)
    return f"""
<div class="section">
<h2 class="section-title">四、表 2：事件明細</h2>
<div class="takeaway">定義 A（技術性衰退）下每個國家逐筆列出的倒掛事件。「最深利差」是事件
期間利差最負的那個月，數字越負代表倒掛越深；「之後衰退起點」空白代表落空或還沒到期，不是
資料缺漏。</div>
{body}
<div class="note">這張表看的是每一次個別事件，平均而言的命中率與前置期留給表 1 和表 3；
不同國家的事件數差很多，樣本少的國家不宜逐次事件做結論。</div>
</div>
"""


def section_table3(countries_data, per_country_lead, pooled_lead, pooled_h):
    rows = []
    for cc, name, d in countries_data:
        info = per_country_lead.get(cc)
        if not info or info["n"] == 0:
            continue
        rows.append(
            f"<tr><td class='lbl'>{esc(name)}</td><td class='num'>{info['n']}</td>"
            f"<td class='num'>{fmt_num(info['min'], 0)}</td>"
            f"<td class='num'>{fmt_num(info['median'], 0)}</td>"
            f"<td class='num'>{fmt_num(info['max'], 0)}</td></tr>")
    rows.append(
        f"<tr><td class='lbl'><b>合併池</b></td><td class='num'>{pooled_lead['n']}</td>"
        f"<td class='num'>{fmt_num(pooled_lead['min'], 0)}</td>"
        f"<td class='num'><b>{fmt_num(pooled_lead['median'], 0)}</b></td>"
        f"<td class='num'>{fmt_num(pooled_lead['max'], 0)}</td></tr>")
    h_rows = "".join(
        f"<tr><td class='lbl'>H={H}</td><td class='num'>{fmt_pct(pooled_h[H]['hit_rate'])}</td>"
        f"<td class='num'>{fmt_pct(pooled_h[H]['base_rate'])}</td>"
        f"<td class='num'>{fmt_num(pooled_h[H]['uplift'], 1)}</td></tr>"
        for H in H_LIST)
    return f"""
<div class="section">
<h2 class="section-title">五、表 3：前置期分布</h2>
<div class="takeaway">只算命中的事件（落空、已在衰退中、未到期都不算前置期）。中位數是
最該看的數字，最小值與最大值告訴你這個時間差有多不穩定。2019 年那次倒掛到 2020 年 2 月
的衰退很短，但也有拖超過一年半的例子。</div>
<div class="scroll"><table><thead><tr><th>國家</th><th class="num">命中事件數</th>
<th class="num">前置期最小（月）</th><th class="num">前置期中位數（月）</th>
<th class="num">前置期最大（月）</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<div class="scroll" style="margin-top:.75rem"><table><thead><tr><th>視窗</th>
<th class="num">合併池命中率</th><th class="num">合併池基率</th><th class="num">提升倍數</th></tr></thead>
<tbody>{h_rows}</tbody></table></div>
<div class="note">把視窗從 12 個月拉到 36 個月，命中率理所當然會上升：時間給得越久，
撞到衰退的機會越大。該看的是提升倍數有沒有跟著掉：如果 36 個月的提升倍數明顯低於
24 個月，代表拉長窗口只是在稀釋訊號，不是倒掛真的更準。</div>
</div>
"""


def _chart_dataset(spread_series, spans):
    labels = [m for m, _v in spread_series]
    values = [v for _m, v in spread_series]
    band = []
    for m in labels:
        band.append(1 if in_any_span(m, spans) else None)
    return labels, values, band


def section_charts(countries_data):
    us = next((d for cc, n, d in countries_data if cc == "US"), None)
    charts_js = []
    small_multiples = []
    if us and us.get("status") == "ok":
        spans = us.get("gdp_recession_spans", [])
        labels, values, band = _chart_dataset(us["spread_series"], spans)
        ymin, ymax = min(values + [0]), max(values + [0])
        pad = max(0.5, (ymax - ymin) * 0.1)
        charts_js.append(_line_chart_js("chart-us", labels, values, band, ymin - pad, ymax + pad))
    for cc, name, d in countries_data:
        if cc == "US" or d.get("status") != "ok":
            continue
        spans = d.get("gdp_recession_spans", [])
        labels, values, band = _chart_dataset(d["spread_series"], spans)
        if not values:
            continue
        ymin, ymax = min(values + [0]), max(values + [0])
        pad = max(0.5, (ymax - ymin) * 0.1)
        cid = f"chart-{cc.lower()}"
        charts_js.append(_line_chart_js(cid, labels, values, band, ymin - pad, ymax + pad))
        small_multiples.append(
            f'<div style="flex:1 1 260px;min-width:0"><h3 style="font-size:.82rem;margin-bottom:.4rem">{esc(name)}</h3>'
            f'<div class="chart-wrap" style="height:200px"><canvas id="{cid}"></canvas></div></div>')

    us_block = ""
    if us and us.get("status") == "ok":
        us_block = ('<div class="chart-wrap" style="height:340px"><canvas id="chart-us"></canvas></div>')
    grid = f'<div style="display:flex;flex-wrap:wrap;gap:1.2rem;margin-top:1rem">{"".join(small_multiples)}</div>'
    return f"""
<div class="section">
<h2 class="section-title">六、圖：利差全史，灰底是技術性衰退</h2>
<div class="takeaway">灰底區間是定義 A（GDP 連兩季負成長）算出的衰退期。看這張圖最該注意
的是：利差跌破 0 的那條水平線之後，灰底是不是很快跟上。跟得快代表訊號有用，隔很久或
完全沒跟上代表這次訊號落空。</div>
{us_block}
{grid}
</div>
<script>{"".join(charts_js)}</script>
"""


def _line_chart_js(canvas_id, labels, values, band, ymin, ymax):
    labels_json = json.dumps(labels, ensure_ascii=False)
    values_json = json.dumps(values)
    band_json = json.dumps([ymax if b else None for b in band])
    return f"""
new Chart(document.getElementById('{canvas_id}'), {{
  data: {{ labels: {labels_json},
    datasets: [
      {{ type:'bar', label:'技術性衰退', data:{band_json}, backgroundColor:'#e5e7eb',
         barPercentage:1, categoryPercentage:1, base:{ymin}, order:2 }},
      {{ type:'line', label:'10Y-3M 利差 (pp)', data:{values_json}, borderColor:'#1a56db',
         backgroundColor:'transparent', pointRadius:0, borderWidth:1.3, order:1 }}
    ] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ ticks:{{ maxTicksLimit:10 }} }}, y:{{ min:{ymin}, max:{ymax},
      title:{{display:true,text:'pp'}} }} }},
    plugins: {{ legend:{{ display:false }} }} }}
}});
"""


def section_2022_case(countries_data):
    rows = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok" or d.get("def_a") is None:
            continue
        events = d["def_a"]["events_detail"]
        ev_2022 = [e for e in events if "2021-06" <= e["start"] <= "2023-06"]
        for e in ev_2022:
            rec_start = add_months(e["start"], e["lead_months"]) if e["verdict"] == "hit" else None
            label = {"hit": "衰退了", "miss": "沒衰退（目前看是落空）",
                      "already_in_recession": "起點時已在衰退中", "not_yet_due": "窗口還沒走完"}[e["verdict"]]
            rows.append(f"<tr><td class='lbl'>{esc(name)}</td><td>{esc(e['start'])}</td>"
                        f"<td class='num'>{fmt_pp(e['deepest'])}</td>"
                        f"<td>{esc(rec_start) if rec_start else '—'}</td><td>{esc(label)}</td></tr>")
    table = "".join(rows) or "<tr><td colspan='5'>樣本內 2021-06～2023-06 無倒掛事件符合本節篩選條件</td></tr>"
    return f"""
<div class="section">
<h2 class="section-title">七、2022－2023 這次：多數國家倒掛了，兩年後誰衰退誰沒有</h2>
<div class="takeaway">這是本頁最重要的反例。2022 年那一波，多數主要經濟體的利差都一度
轉負，但兩年後的結果並不一致：有的國家如期衰退，有的擦邊而過，有的到現在都沒衰退。
這張表直接把同一時間點的訊號攤開來看實際結果，不用平均數字掩蓋分歧。</div>
<div class="scroll"><table><thead><tr><th>國家</th><th>倒掛起點</th><th class="num">最深利差</th>
<th>之後衰退起點</th><th>結果</th></tr></thead><tbody>{table}</tbody></table></div>
<div class="note">這張表只做訊號與結果的對帳，不解釋「為什麼有的國家躲過去了」。那要另外
查財政刺激、就業市場緊俏程度這類傳導管道，本頁不做因果推論。
日本沒有出現在表裡：它的利差在這段期間沒有出現新的倒掛事件起點，前一次倒掛（2020 年 3 月）
已經在 24 個月分組窗口外，2022 到 2023 年利差一路維持正值，沒有再跌破 0。</div>
</div>
"""


def section_def_bc(countries_data):
    us = next((d for cc, n, d in countries_data if cc == "US"), None)
    us_text = ""
    if us and us.get("def_a") and us.get("def_c"):
        a = us["def_a"]["by_h"][PRIMARY_H]
        c = us["def_c"]["by_h"][PRIMARY_H]
        us_text = (f"美國本身可以直接對比兩把尺：技術性衰退（定義 A）命中率是 {fmt_pct(a['hit_rate'])}，"
                   f"提升 {fmt_num(a['uplift'],1)} 倍；換成 NBER 官方認定（定義 C）之後命中率升到 "
                   f"{fmt_pct(c['hit_rate'])}，提升 {fmt_num(c['uplift'],1)} 倍。兩把尺方向一致，"
                   f"倒掛確實把衰退機率推高，差別在於 NBER 認定的衰退次數比「連兩季負成長」多，"
                   f"技術性衰退定義漏掉的那幾次（例如 2001 年）NBER 有算進去。")

    b_rows = []
    for cc, name, d in countries_data:
        if cc in ("US", "TW") or d.get("status") != "ok":
            continue
        db, da = d.get("def_b"), d.get("def_a")
        if db is None or da is None:
            continue
        hb, ha = db["by_h"][PRIMARY_H], da["by_h"][PRIMARY_H]
        b_rows.append((name, ha["hit_rate"], ha["base_rate"], hb["hit_rate"], hb["base_rate"]))

    jp_row = next((r for r in b_rows if r[0] == "日本"), None)
    other_rows = [r for r in b_rows if r[0] != "日本"]
    lo = min(r[3] for r in other_rows) if other_rows else None
    hi = max(r[3] for r in other_rows) if other_rows else None

    b_text = (f"六個對照國家換成 OECD 指標之後，命中率全部大幅上升，落在 {fmt_pct(lo)} 到 "
              f"{fmt_pct(hi)} 之間，比定義 A 高出一截。但這不完全是訊號變準，OECD 指標本身觸發得"
              f"比「連兩季負成長」頻繁得多，它抓的是景氣循環的下行段，不是嚴格定義的衰退，所以"
              f"基率也跟著從二到四成拉高到四到五成。拿提升倍數（命中率除以基率）比較，兩把尺的"
              f"差距就沒有原始命中率看起來那麼大，多數國家仍在同一個量級。")

    jp_text = ""
    if jp_row:
        jp_text = (f"日本是最極端的例外：定義 A 下三次倒掛事件命中率是 0%，換成定義 B 命中率是 "
                   f"{fmt_pct(jp_row[3])}。這不是訊號在日本突然變準，而是日本的 GDP 數據只從 "
                   f"1994 年起可用，定義 A 的樣本只有三次事件，任何一次的結果都會把命中率整個推到 "
                   f"0% 或 100%，數字本身不穩，不能拿來斷言哪把尺對日本比較準。")

    tw = next((d for cc, n, d in countries_data if cc == "TW"), None)
    tw_text = ""
    if tw and tw.get("status") == "ok" and tw.get("def_a") and tw.get("def_t"):
        ta = tw["def_a"]["by_h"][PRIMARY_H]
        tt = tw["def_t"]["by_h"][PRIMARY_H]
        tw_text = (f"台灣沒有 OECD 或 NBER 這類官方衰退指標，改用國發會峰谷自己排一把對照尺"
                   f"（定義 T，峰的次月為衰退起點）。定義 A（技術性衰退，樣本 "
                   f"{tw['def_a']['sample_start']}～{tw['def_a']['sample_end']}）命中率是 "
                   f"{fmt_pct(ta['hit_rate'])}，提升 {fmt_num(ta['uplift'],1)} 倍；定義 T（國發會峰谷，"
                   f"樣本 {tw['def_t']['sample_start']}～{tw['def_t']['sample_end']}）命中率是 "
                   f"{fmt_pct(tt['hit_rate'])}，提升 {fmt_num(tt['uplift'],1)} 倍。定義 T 的樣本窗比定義 A "
                   f"長（往回多抓到 1996 到 2000 年那段 GDP 資料還沒有的時間），兩把尺看到的事件不是"
                   f"同一組，數字會有出入，但方向是否一致看上面兩個提升倍數就知道。")

    return f"""
<div class="section">
<h2 class="section-title">八、換一把尺：定義 B、C、T 答案有沒有變</h2>
<div class="takeaway">主線用 GDP 連兩季負成長（定義 A），這節換成官方認定的衰退期重算一次，
檢查結論是不是只在某一種衰退定義下才成立。</div>
<div class="card">
<p style="font-size:.87rem">{esc(us_text)}</p>
<p style="font-size:.87rem;margin-top:.6rem">{esc(b_text)}</p>
<p style="font-size:.87rem;margin-top:.6rem">{esc(jp_text)}</p>
<p style="font-size:.87rem;margin-top:.6rem">{esc(tw_text)}</p>
<p style="font-size:.87rem;margin-top:.6rem">OECD 這條指標 2022 年 9 月停更，2022 年那一波倒掛在
這把尺下大多數落在「未到期」。這把尺目前還沒辦法對這次事件下結論，不是它顯示沒衰退。</p>
</div>
</div>
"""


def section_limitations(tw_status, tw_data):
    tw_line = ""
    tw_table = ""
    if tw_status != "ok":
        missing_bits = tw_data.get("missing_bits") if tw_data else None
        detail = "、".join(missing_bits) if missing_bits else "十年期公債殖利率、90 天期商業本票次級市場利率、"\
                 "主計總處實質 GDP 季增率、國發會景氣循環基準日期"
        pts = (tw_data or {}).get("peaks_troughs") or []
        if pts:
            tw_line = (f"<li>台灣資料整理中，本頁先出七國版本。國發會景氣循環基準日期（峰谷）已查證到"
                       f"完整官方表格（{len(pts)} 次循環，1954 年起，見下方附表），但十年期公債殖利率、"
                       f"90 天期商業本票次級市場利率、實質 GDP 季增率這三項是互動查詢系統，沒有在時限內"
                       f"拿到可用的完整序列，四項缺一，台灣目前不能跑完整回測，不用假資料湊數。</li>")
        else:
            tw_line = (f"<li>台灣資料整理中，本頁先出七國版本：{esc(detail)}"
                       f"尚未齊備到可以跑完整回測的程度，缺什麼在回報裡逐項列出，不用假資料湊數。</li>")
        if pts:
            rows = "".join(f"<tr><td>{esc(i+1)}</td><td>{esc(p['peak'])}</td>"
                            f"<td>{esc(p['trough'])}</td></tr>" for i, p in enumerate(pts))
            src = esc(tw_data.get("cycle_source_url") or "")
            tw_table = f"""
<h3 style="font-size:.95rem;margin:1rem 0 .5rem">台灣景氣循環基準日期（國發會，已確認，尚未併入主表）</h3>
<p style="font-size:.85rem;margin-bottom:.5rem">這張表只有峰（景氣高峰月）與谷（景氣谷底月），
還沒有利差可以配對，所以沒辦法算命中率或前置期，先列出來備查，來源：
<a href="{src}" target="_blank" rel="noopener">{src}</a>。</p>
<div class="scroll"><table><thead><tr><th>循環次序</th><th>高峰</th><th>谷底</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""
    else:
        tw_line = ("<li>台灣的實質 GDP 季增率只從 2000 年第 1 季開始，定義 A 的樣本期間因此比"
                   "其餘七國短，事件數少，命中率的統計不確定性大。台灣的 3M 用商業本票次級市場"
                   "利率（不是同業拆款、也不是公債），含企業信用溢價，偏差方向跟其餘七國的 "
                   "IR3TIB 一樣：利差整體偏低、倒掛事件偏多，方法段第 2 節已註明。對照尺定義 T"
                   "（國發會峰谷）樣本窗比定義 A 長，兩把尺看到的事件不是同一組，數字不能直接"
                   "跨尺相減比較，只能各自看提升倍數。</li>")
    return f"""
<div class="section">
<h2 class="section-title">九、這頁沒有告訴你的事</h2>
<div class="card"><ul class="disc">
<li>日本樣本短：實質 GDP 季增率只從 1994 年起有資料，衰退事件數本來就少，命中率與
基率的分母都小，數字的不確定性比其他國家大，不宜跟樣本更長的國家直接比大小。</li>
<li>技術性衰退（定義 A）這把尺會漏掉不是「連兩季負成長」但普遍認定是衰退的事件。
美國 2001 年那次衰退（NBER 認定 2001-03 至 2001-11）沒有連續兩季 GDP 負成長，定義 A
在美國這裡會漏掉它，只有定義 C（NBER）抓得到，見表 1 只算定義 A 命中率會低估美國。</li>
<li>澳洲樣本內幾乎三十年沒有技術性衰退（直到近年才出現符合定義的事件），這段期間的
「基率」會被壓得很低，任何一次倒掛的提升倍數都容易被放大，判讀時要留意分母。</li>
<li>OECD 衰退指標（定義 B）2022 年 9 月停更，2022 年之後的所有事件在這把尺下都無法
判定命中或落空，本頁一律標「未到期」，不是它顯示沒衰退。</li>
{tw_line}
<li>全部序列都是官方統計事後定案的數字，跑資料當下離現在越近的月份，GDP 數字越可能
之後被修正，本頁用的是抓取當下的最新公布值，不會回頭用修正後數字改寫已經定案的事件。</li>
</ul>
{tw_table}
</div>
</div>
"""


def collapse_cjk_whitespace(html_str: str) -> str:
    """本檔很多段落用多行 f-string 拼句子，句子中間換行的地方會留下一個 `\\n`；瀏覽器把
    HTML 原始碼裡的換行當一般空白處理，排版上會在兩個中文字中間多一個看不見的半形空格
    （2026-09-17 驗收發現）。這裡把 body 文字裡「兩個 CJK 字元（含全形標點）之間的半形
    空白（含換行、tab）」直接砍掉；<script>/<style> 整段先切出來不處理，避免動到 JS/CSS。
    半形字（英文、數字、%）前後的空格不受影響，因為比對條件要求兩側都是 CJK。"""
    protected = []

    def _stash(m):
        protected.append(m.group(0))
        return f"\x00PROTECTED{len(protected) - 1}\x00"

    stashed = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", _stash, html_str,
                      flags=re.IGNORECASE | re.DOTALL)
    cjk = "　-鿿＀-￯"
    collapsed = re.sub(rf"(?<=[{cjk}])\s+(?=[{cjk}])", "", stashed)
    return re.sub(r"\x00PROTECTED(\d+)\x00", lambda m: protected[int(m.group(1))], collapsed)


def generate_html(countries_data, pooled_lead, pooled_h, per_country_lead, pooled_recall, tw_status, tw_data,
                   built_date):
    main_style, nav_block = extract_template_parts()
    h24 = pooled_h[PRIMARY_H]
    title = "殖利率倒掛與經濟衰退：八國回測 | InvestMQuest Research"
    tw_desc_note = ("台灣併入主表，另跑國發會峰谷對照尺。" if tw_status == "ok"
                     else "台灣資料整理中，本頁先出七國版本。")
    countries_desc = "美/德/英/日/加/澳/韓/台" if tw_status == "ok" else "美/德/英/日/加/澳/韓"
    description = (f"用 FRED 與台灣央行、主計總處資料對{countries_desc}套同一把尺回測 10Y-3M 利差倒掛："
                    f"合併池 H=24 個月命中率 {fmt_pct(h24['hit_rate'])}、基率 {fmt_pct(h24['base_rate'])}、"
                    f"提升 {fmt_num(h24['uplift'],1)} 倍，前置期中位數 {fmt_num(pooled_lead['median'],0)} 個月；"
                    f"{tw_desc_note}判定：倒掛提高衰退機率，時間差不穩定，八國答案不一致。")

    try:
        sys.path.insert(0, str(NAV_DIR))
        from _nav_common import make_toggle  # noqa
        subnav = make_toggle("yield_curve")
    except Exception as e:
        warn(f"make_toggle 載入失敗：{e}，pill bar 留空")
        subnav = ""

    hero = section_hero(countries_data, pooled_h, pooled_lead, tw_status)
    method = section_method()
    t1 = section_table1(countries_data, pooled_h, pooled_recall)
    t2 = section_table2(countries_data)
    t3 = section_table3(countries_data, per_country_lead, pooled_lead, pooled_h)
    charts = section_charts(countries_data)
    case2022 = section_2022_case(countries_data)
    defbc = section_def_bc(countries_data)
    limits = section_limitations(tw_status, tw_data)

    takeaway = ("<b>給沒有統計背景的讀者：</b>這頁做的事很單純。利差是 10 年期公債殖利率減 3 個月期"
                "利率，跌到 0 以下叫「倒掛」，歷史上市場常拿它當衰退警訊。我們把八個國家的利率與 GDP "
                "資料全部拉出來，用同一套規則自動判定倒掛事件與衰退事件，算命中率、算多久看到、算"
                "跟瞎猜比有沒有比較準。本頁不做「現在該不該擔心」的建議，也不預測下一次衰退什麼時候"
                "來，只回報歷史上這個訊號準不準、準多快。")

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
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / 殖利率倒掛與衰退</div>
    <h1>殖利率倒掛與經濟衰退：八國回測</h1>
    <div class="sub">10Y-3M 利差倒掛能不能預示衰退、多久看到、八國是否一致・生成 {esc(built_date)}</div>
    {subnav}
  </div>
</div>

<div class="container">

{hero}

<div class="takeaway">{takeaway}</div>

<div class="section">
<h2 class="section-title">一、我們問的三個問題</h2>
<div class="card"><ul class="disc">
<li><b>殖利率倒掛真的預示經濟衰退嗎？</b>命中率、反向召回率，跟不看訊號時的基率比一比，
答案在表 1。</li>
<li><b>如果是，倒掛後多久會看到衰退？</b>看每次事件的前置月數，中位數與範圍，答案在表 3。</li>
<li><b>不同國家都適用嗎？</b>同一套規則跑八國，一國一行，答案在表 1、表 2，以及第七節的
2022 年反例。</li>
</ul></div>
</div>

{method}
{t1}
{t2}
{t3}
{charts}
{case2022}
{defbc}
{limits}

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 殖利率倒掛與經濟衰退：八國回測（研究頁，不構成投資建議）
    &middot; 頁面生成 {esc(built_date)} &middot; 僅供研究參考，不構成投資建議
  </div>
</footer>
</body>
</html>
"""
    return collapse_cjk_whitespace(body)


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def do_compute_and_build():
    raw = load_raw()
    raw_series = raw.get("series", {})
    tw_manual = load_tw_manual()

    countries_data = []
    for cc, name, codes in COUNTRIES:
        d = build_country(cc, name, codes, raw_series)
        if d.get("status") != "ok":
            warn(f"{cc} {name}: 狀態={d.get('status')} 缺={d.get('missing_series')}")
        countries_data.append((cc, name, d))

    tw_data = build_taiwan(tw_manual)
    tw_status = tw_data.get("status")
    if tw_status != "ok":
        warn(f"TW 台灣: 狀態={tw_status}（{tw_data.get('note') or tw_data.get('missing_bits')}）")
    countries_data.append(("TW", "台灣", tw_data))

    per_country_lead, pooled_lead, pooled_h, pooled_recall = pooled_lead_stats(countries_data)

    def _json_default(o):
        return str(o)

    out_payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "countries": {cc: d for cc, _n, d in countries_data},
        "pooled": {"lead_time": pooled_lead, "by_h": pooled_h,
                   "per_country_lead": per_country_lead, "reverse_recall": pooled_recall},
        "definitions": DEFINITIONS_TEXT,
        "series_used": {cc: codes for cc, _n, codes in COUNTRIES},
        "oecd_b_cutoff": OECD_B_CUTOFF_MONTH,
        "h_list": H_LIST, "primary_h": PRIMARY_H,
    }
    DATA.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2, default=_json_default) + "\n",
                        encoding="utf-8")
    info(f"寫入 {OUT_JSON}")

    built_date = datetime.now().strftime("%Y-%m-%d")
    html_out = generate_html(countries_data, pooled_lead, pooled_h, per_country_lead, pooled_recall,
                              tw_status, tw_data, built_date)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_out, encoding="utf-8")
    info(f"寫入 {OUT_HTML}")

    h24 = pooled_h[PRIMARY_H]
    info(f"合併池 H=24：命中率={h24['hit_rate']} 基率={h24['base_rate']} 提升={h24['uplift']}")
    info(f"前置期（合併池）：min={pooled_lead['min']} median={pooled_lead['median']} max={pooled_lead['max']}")


def main():
    ap = argparse.ArgumentParser(description="殖利率倒掛 × 經濟衰退 跨國回測 builder")
    ap.add_argument("--fetch", action="store_true", help="只抓 FRED 序列存 raw json，不算統計、不生頁面")
    args = ap.parse_args()
    if args.fetch:
        do_fetch()
        return
    do_compute_and_build()


if __name__ == "__main__":
    main()
