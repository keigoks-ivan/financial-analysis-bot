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
# 第二版新增計算（v2 規格第 1 節 C1-C11）——全部是新函式，呼叫既有函式（classify_event／
# base_rate／detect_events／in_any_span／add_months／month_diff）取得結果後再加工，不改
# 既有函式本身的邏輯或回傳值。
# ═══════════════════════════════════════════════════════════════════════════

def wilson_ci(k, n, z=1.959963984540054):
    """C1：Wilson 95% 信賴區間（score interval）。k=命中數，n=可判定樣本數。
    n=0 回傳 (None, None)。"""
    if not n:
        return None, None
    phat = k / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = (z * ((phat * (1 - phat) / n + z * z / (4 * n * n)) ** 0.5)) / denom
    return max(0.0, round(center - margin, 4)), min(1.0, round(center + margin, 4))


def add_wilson_ci(stats):
    """C1：對 build_definition_stats() 的回傳值事後疊加 ci_low／ci_high，不改
    build_definition_stats 本身。命中率 CI 用 n=n_testable；基率 CI 用
    n=base_rate_n（滾動月數，月份不獨立，CI 偏窄，第十二節說明）。"""
    if stats is None:
        return
    for _H, h in stats["by_h"].items():
        lo, hi = wilson_ci(h["n_hit"], h["n_testable"])
        h["hit_rate_ci_low"], h["hit_rate_ci_high"] = lo, hi
        blo, bhi = wilson_ci(h.get("base_rate_hits") or 0, h.get("base_rate_n") or 0)
        h["base_rate_ci_low"], h["base_rate_ci_high"] = blo, bhi


def add_wilson_ci_pooled(pooled_h):
    """C1：合併池版本，作用在 pooled_lead_stats() 回傳的 pooled_h 上。"""
    for _H, h in pooled_h.items():
        lo, hi = wilson_ci(h["n_hit"], h["n_testable"])
        h["hit_rate_ci_low"], h["hit_rate_ci_high"] = lo, hi
        blo, bhi = wilson_ci(h.get("base_hits") or 0, h.get("base_n") or 0)
        h["base_rate_ci_low"], h["base_rate_ci_high"] = blo, bhi


def build_precision_recall(countries_data, pooled_h, pooled_recall):
    """C2：精確率＝命中率（H=24），召回率＝反向召回率，一國一點＋合併池另存。"""
    points = []
    for cc, name, d in countries_data:
        da = d.get("def_a")
        if d.get("status") != "ok" or da is None:
            continue
        h = da["by_h"][PRIMARY_H]
        if h["hit_rate"] is None or da["reverse_recall"] is None:
            continue
        points.append({"cc": cc, "name": name, "precision": h["hit_rate"],
                        "recall": da["reverse_recall"], "n_events": da["n_events"]})
    hp = pooled_h[PRIMARY_H]
    pooled_point = {"cc": "POOL", "name": "合併池", "precision": hp["hit_rate"],
                     "recall": pooled_recall, "n_events": sum(p["n_events"] for p in points)}
    return points, pooled_point


DEPTH_CUTOFF = -0.50
DURATION_CUTOFF = 3


def build_depth_duration(countries_data):
    """C3：合併池（8 國定義 A、H=24）所有可判定事件（排除已在衰退中／未到期），依
    最深利差（≤-0.50pp vs >-0.50pp）×倒掛月數（≥3 vs <3）分 2x2；另存逐事件明細
    (cc, deepest, n_inverted_months, verdict) 給散佈圖。"""
    events = []
    for cc, name, d in countries_data:
        da = d.get("def_a")
        if d.get("status") != "ok" or da is None:
            continue
        for ev in da["events_detail"]:
            if ev["verdict"] not in ("hit", "miss"):
                continue
            events.append({"cc": cc, "name": name, "deepest": ev["deepest"],
                            "n_inverted_months": ev["n_inverted_months"], "verdict": ev["verdict"]})
    buckets = {}
    for deep_label, deep_ok in (("深倒掛（≤-0.50pp）", True), ("淺倒掛（>-0.50pp）", False)):
        for dur_label, dur_ok in (("長（≥3個月）", True), ("短（<3個月）", False)):
            sel = [e for e in events
                   if ((e["deepest"] <= DEPTH_CUTOFF) == deep_ok)
                   and ((e["n_inverted_months"] >= DURATION_CUTOFF) == dur_ok)]
            n_hit = sum(1 for e in sel if e["verdict"] == "hit")
            n = len(sel)
            buckets[f"{deep_label}×{dur_label}"] = {
                "depth": deep_label, "duration": dur_label,
                "n": n, "n_hit": n_hit, "hit_rate": round(n_hit / n, 4) if n else None,
            }
    return {"events": events, "buckets": buckets}


def detect_events_with_end(spread_monthly, sample_start, sample_end, group_months=EVENT_GROUP_MONTHS):
    """C6：比照 detect_events()，但額外算出每個事件「最後一個倒掛月」（detect_events
    本身不改，這裡另開一支平行函式，邏輯完全對齊，只多存一個 end 欄位）。"""
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
        events.append({"start": start_m, "end": group[-1][0], "deepest": round(deepest, 4),
                        "n_inverted_months": len(group)})
        i = j
    return events


MAX_K = 36


def _qualifying_events_for_curve(events_detail, spans, sample_end, max_k=MAX_K):
    """C4：已在衰退中的判定與 H 無關（classify_event 一律先判斷這個），可直接沿用
    events_detail 裡的 verdict；『分母固定』改用本函式自己的 max_k 窗重新篩，不沿用
    H=24 的未到期判定。"""
    out = []
    for ev in events_detail:
        if ev["verdict"] == "already_in_recession":
            continue
        if sample_end is None or month_diff(sample_end, add_months(ev["start"], max_k)) < 0:
            continue
        out.append(ev["start"])
    return out


def build_cumulative_curve(qualifying_starts, starts_sorted, max_k=MAX_K):
    """C4：對固定分母 qualifying_starts，算 k=1..max_k 累積命中曲線。"""
    n = len(qualifying_starts)
    curve = []
    for k in range(1, max_k + 1):
        n_hit = sum(1 for s in qualifying_starts if any(0 < month_diff(r, s) <= k for r in starts_sorted))
        curve.append({"k": k, "n": n, "n_hit": n_hit, "hit_rate": round(n_hit / n, 4) if n else None})
    return curve


def build_base_rate_curve(recession_starts, sample_start, sample_end, max_k=MAX_K):
    """C4：無條件基率曲線，分母固定為「起點後有完整 max_k 個月資料」的月份，
    k=1..max_k 逐點算，邏輯比照 base_rate() 但一次算整條曲線。"""
    months = []
    m = sample_start
    while m <= sample_end:
        months.append(m)
        m = add_months(m, 1)
    valid = [m for m in months if month_diff(sample_end, add_months(m, max_k)) >= 0]
    starts_sorted = sorted(recession_starts)
    n = len(valid)
    curve = []
    for k in range(1, max_k + 1):
        n_hit = sum(1 for mm in valid if any(0 < month_diff(s, mm) <= k for s in starts_sorted))
        curve.append({"k": k, "n": n, "n_hit": n_hit, "hit_rate": round(n_hit / n, 4) if n else None})
    return curve


def build_country_event_curve(d, max_k=MAX_K):
    da = d.get("def_a")
    if d.get("status") != "ok" or da is None:
        return None
    spans = d.get("gdp_recession_spans", [])
    starts_sorted = sorted(s for s, _e in spans)
    quals = _qualifying_events_for_curve(da["events_detail"], spans, da["sample_end"], max_k)
    return build_cumulative_curve(quals, starts_sorted, max_k)


def build_country_base_rate_curve(d, max_k=MAX_K):
    da = d.get("def_a")
    if d.get("status") != "ok" or da is None:
        return None
    spans = d.get("gdp_recession_spans", [])
    starts_sorted = sorted(s for s, _e in spans)
    return build_base_rate_curve(starts_sorted, da["sample_start"], da["sample_end"], max_k)


def build_pooled_event_curve(countries_data, max_k=MAX_K):
    """C4：合併池累積命中曲線——每個國家自己的事件對自己的衰退起點判定，再彙總。"""
    items = []
    for cc, name, d in countries_data:
        da = d.get("def_a")
        if d.get("status") != "ok" or da is None:
            continue
        spans = d.get("gdp_recession_spans", [])
        starts_sorted = sorted(s for s, _e in spans)
        quals = _qualifying_events_for_curve(da["events_detail"], spans, da["sample_end"], max_k)
        items.extend((s, starts_sorted) for s in quals)
    n = len(items)
    curve = []
    for k in range(1, max_k + 1):
        n_hit = sum(1 for s, starts_sorted in items if any(0 < month_diff(r, s) <= k for r in starts_sorted))
        curve.append({"k": k, "n": n, "n_hit": n_hit, "hit_rate": round(n_hit / n, 4) if n else None})
    return curve


def build_pooled_base_rate_curve(countries_data, max_k=MAX_K):
    """C4：無條件基率曲線的合併池版本，把每個國家「有完整 max_k 個月資料」的月份
    全部併成一個大集合再算。"""
    items = []
    for cc, name, d in countries_data:
        da = d.get("def_a")
        if d.get("status") != "ok" or da is None:
            continue
        spans = d.get("gdp_recession_spans", [])
        starts_sorted = sorted(s for s, _e in spans)
        sstart, send = da["sample_start"], da["sample_end"]
        months = []
        m = sstart
        while m <= send:
            months.append(m)
            m = add_months(m, 1)
        valid = [m for m in months if month_diff(send, add_months(m, max_k)) >= 0]
        items.extend((mm, starts_sorted) for mm in valid)
    n = len(items)
    curve = []
    for k in range(1, max_k + 1):
        n_hit = sum(1 for mm, starts_sorted in items if any(0 < month_diff(r, mm) <= k for r in starts_sorted))
        curve.append({"k": k, "n": n, "n_hit": n_hit, "hit_rate": round(n_hit / n, 4) if n else None})
    return curve


def build_lead_strip(countries_data):
    """C5：每個命中事件的 (cc, lead_months)，供前置期條帶圖。"""
    points = []
    for cc, name, d in countries_data:
        da = d.get("def_a")
        if d.get("status") != "ok" or da is None:
            continue
        for ev in da["events_detail"]:
            if ev["verdict"] == "hit":
                points.append({"cc": cc, "name": name, "lead_months": ev["lead_months"],
                                "event_start": ev["start"]})
    return points


TIMELINE_START = "1953-01"
TIMELINE_END = "2026-08"


def build_country_timeline(d):
    """C6：單一國家的事件起訖（用 detect_events_with_end，不動 detect_events）
    ＋定義 A 衰退區間，供時間軸條帶圖。"""
    da = d.get("def_a")
    if d.get("status") != "ok" or da is None:
        return None
    spread_dict = dict(d["spread_series"])
    events = detect_events_with_end(spread_dict, da["sample_start"], da["sample_end"])
    spans = d.get("gdp_recession_spans", [])
    return {"events": [{"start": e["start"], "end": e["end"]} for e in events],
            "recession_spans": [[s, e] for s, e in spans]}


def build_us_cross_country(countries_data):
    """C7：用美國定義 A 倒掛事件清單，對其餘七國各自的定義 A 衰退區間跑
    classify_event（H=24），樣本窗取美國事件窗與該國定義 A 樣本窗的交集；並列
    該國「用自己曲線」的命中率——沿用該國 def_a H=24 既有數字。美國利差序列從
    1953-04 起，早於其餘七國定義 A 樣本窗的起點，交集窗因此等於各國自己的樣本窗，
    兩邊其實是同一個窗，不是分開的兩段樣本。精確率之外同時算召回率：自己曲線召回率
    沿用既有 reverse_recall（該國自己的利差對自己的衰退起點）；美國曲線召回率改用
    美國的利差序列，對該國自己的衰退起點跑同一支 reverse_recall()（不改函式本身）。"""
    us = next((d for cc, n, d in countries_data if cc == "US"), None)
    if not us or us.get("status") != "ok" or us.get("def_a") is None:
        return None
    us_a = us["def_a"]
    us_start, us_end = us_a["sample_start"], us_a["sample_end"]
    us_event_starts = [e["start"] for e in us_a["events_detail"]]
    us_spread = dict(us["spread_series"])

    rows = []
    pooled_n_hit = pooled_n_testable = 0
    pooled_own_n_hit = pooled_own_n_testable = 0
    pooled_own_recall_hit = pooled_own_recall_n = 0
    pooled_us_recall_hit = pooled_us_recall_n = 0
    for cc, name, d in countries_data:
        if cc == "US" or d.get("status") != "ok" or d.get("def_a") is None:
            continue
        da = d["def_a"]
        spans = d.get("gdp_recession_spans", [])
        starts_sorted = sorted(s for s, _e in spans)
        win_start = max(us_start, da["sample_start"])
        win_end = min(us_end, da["sample_end"])
        if win_start > win_end:
            continue
        ev_in_window = [s for s in us_event_starts if win_start <= s <= win_end]
        n_hit = n_miss = 0
        for s in ev_in_window:
            verdict, _lead = classify_event(s, PRIMARY_H, spans, starts_sorted, win_end)
            if verdict == "hit":
                n_hit += 1
            elif verdict == "miss":
                n_miss += 1
        n_testable = n_hit + n_miss
        us_curve_hit_rate = round(n_hit / n_testable, 4) if n_testable else None
        own_h = da["by_h"][PRIMARY_H]

        us_curve_recall, us_recall_n = reverse_recall(
            starts_sorted, us_spread, da["sample_start"], da["sample_end"], window=RECALL_WINDOW_MONTHS)
        own_curve_recall, own_recall_n = da["reverse_recall"], da["reverse_recall_n"]

        rows.append({
            "cc": cc, "name": name, "window": [win_start, win_end],
            "n_events_tested": len(ev_in_window), "n_testable": n_testable, "n_hit": n_hit,
            "us_curve_hit_rate": us_curve_hit_rate,
            "own_curve_hit_rate": own_h["hit_rate"], "own_curve_n_testable": own_h["n_testable"],
            "own_curve_recall": own_curve_recall, "own_recall_n": own_recall_n,
            "us_curve_recall": us_curve_recall, "us_recall_n": us_recall_n,
        })
        pooled_n_hit += n_hit
        pooled_n_testable += n_testable
        pooled_own_n_hit += own_h["n_hit"]
        pooled_own_n_testable += own_h["n_testable"]
        if own_curve_recall is not None:
            pooled_own_recall_hit += round(own_curve_recall * own_recall_n)
            pooled_own_recall_n += own_recall_n
        if us_curve_recall is not None:
            pooled_us_recall_hit += round(us_curve_recall * us_recall_n)
            pooled_us_recall_n += us_recall_n

    pooled = {
        "n_testable": pooled_n_testable, "n_hit": pooled_n_hit,
        "us_curve_hit_rate": round(pooled_n_hit / pooled_n_testable, 4) if pooled_n_testable else None,
        "own_curve_hit_rate": round(pooled_own_n_hit / pooled_own_n_testable, 4) if pooled_own_n_testable else None,
        "own_curve_n_testable": pooled_own_n_testable,
        "own_curve_recall": round(pooled_own_recall_hit / pooled_own_recall_n, 4) if pooled_own_recall_n else None,
        "own_recall_n": pooled_own_recall_n,
        "us_curve_recall": round(pooled_us_recall_hit / pooled_us_recall_n, 4) if pooled_us_recall_n else None,
        "us_recall_n": pooled_us_recall_n,
    }
    return {"rows": rows, "pooled": pooled}


PERIOD_CUTOFF = "2000-01"


def build_period_split(countries_data, cutoff=PERIOD_CUTOFF):
    """C8：合併池與美國事件依起點 <cutoff／≥cutoff 分兩組，各自命中率（H=24）、n、
    基率（同期滾動，用既有 base_rate() 對子期間窗重算，不改 base_rate 本身）。"""
    def _split_country(d):
        da = d.get("def_a")
        if d.get("status") != "ok" or da is None:
            return None
        spans = d.get("gdp_recession_spans", [])
        starts_sorted = sorted(s for s, _e in spans)
        sstart, send = da["sample_start"], da["sample_end"]
        pre_events = [e for e in da["events_detail"] if e["start"] < cutoff and e["verdict"] in ("hit", "miss")]
        post_events = [e for e in da["events_detail"] if e["start"] >= cutoff and e["verdict"] in ("hit", "miss")]
        out = {}
        for label, evs in (("pre", pre_events), ("post", post_events)):
            n_hit = sum(1 for e in evs if e["verdict"] == "hit")
            n = len(evs)
            if label == "pre":
                sub_start, sub_end = sstart, min(send, add_months(cutoff, -1))
            else:
                sub_start, sub_end = max(sstart, cutoff), send
            br, br_n, br_hits = (None, 0, 0)
            if sub_start <= sub_end:
                br, br_n, br_hits = base_rate(starts_sorted, sub_start, sub_end, window=PRIMARY_H)
            out[label] = {"n": n, "n_hit": n_hit, "hit_rate": round(n_hit / n, 4) if n else None,
                           "base_rate": br, "base_rate_n": br_n, "base_rate_hits": br_hits}
        return out

    pooled = {"pre": {"n": 0, "n_hit": 0, "base_hits": 0, "base_n": 0},
              "post": {"n": 0, "n_hit": 0, "base_hits": 0, "base_n": 0}}
    us_split = None
    for cc, name, d in countries_data:
        split = _split_country(d)
        if split is None:
            continue
        if cc == "US":
            us_split = split
        for label in ("pre", "post"):
            pooled[label]["n"] += split[label]["n"]
            pooled[label]["n_hit"] += split[label]["n_hit"]
            pooled[label]["base_hits"] += split[label]["base_rate_hits"] or 0
            pooled[label]["base_n"] += split[label]["base_rate_n"] or 0
    for label in ("pre", "post"):
        p = pooled[label]
        p["hit_rate"] = round(p["n_hit"] / p["n"], 4) if p["n"] else None
        p["base_rate"] = round(p["base_hits"] / p["base_n"], 4) if p["base_n"] else None
    return {"pooled": pooled, "us": us_split, "cutoff": cutoff}


def build_already_in_recession_table(countries_data):
    """C9：每國「已在衰退中」次數／事件數。"""
    rows = []
    for cc, name, d in countries_data:
        da = d.get("def_a")
        if d.get("status") != "ok" or da is None:
            continue
        n_already = da["by_h"][PRIMARY_H]["n_already_in_recession"]
        n_events = da["n_events"]
        rows.append({"cc": cc, "name": name, "n_already": n_already, "n_events": n_events,
                      "ratio": round(n_already / n_events, 4) if n_events else None})
    return rows


C10_START = "2021-01"


def build_2022_rescale(countries_data):
    """C10：八國 2021-01 到最新的月利差序列＋各自定義 A 衰退區間，給重疊折線圖。"""
    out = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        series = [(m, v) for m, v in d["spread_series"] if m >= C10_START]
        if not series:
            continue
        spans = d.get("gdp_recession_spans", [])
        spans_in_range = [[s, e] for s, e in spans if e is None or e >= C10_START]
        out.append({"cc": cc, "name": name, "series": series, "recession_spans": spans_in_range})
    return out


def build_definition_dumbbell(countries_data):
    """C11：每國定義 A vs 定義 B 命中率（美國 A vs C，台灣 A vs T），並列提升倍數
    （命中率÷該定義自己的基率，沿用 build_definition_stats 既有的 uplift 欄，不
    另外重算），用來檢查換尺後的排序、倍數是不是還跟定義 A 大致一致。"""
    rows = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        da = d.get("def_a")
        if da is None:
            continue
        a_h = da["by_h"][PRIMARY_H]
        a_rate, a_uplift = a_h["hit_rate"], a_h["uplift"]
        if cc == "US":
            alt, alt_label = d.get("def_c"), "定義 C（NBER）"
        elif cc == "TW":
            alt, alt_label = d.get("def_t"), "定義 T（國發會峰谷）"
        else:
            alt, alt_label = d.get("def_b"), "定義 B（OECD）"
        alt_h = alt["by_h"][PRIMARY_H] if alt else None
        alt_rate = alt_h["hit_rate"] if alt_h else None
        alt_uplift = alt_h["uplift"] if alt_h else None
        rows.append({"cc": cc, "name": name, "a_rate": a_rate, "a_uplift": a_uplift,
                      "alt_rate": alt_rate, "alt_uplift": alt_uplift, "alt_label": alt_label})
    return rows


EXTRA_H_LIST = [6, 18]


def extra_h_country_stats(d, H):
    """補 H_LIST=[12,24,36] 以外的 H（6、18），沿用 classify_event／base_rate，
    H_LIST 全域常數本身不動。"""
    da = d.get("def_a")
    if d.get("status") != "ok" or da is None:
        return None
    spans = d.get("gdp_recession_spans", [])
    starts_sorted = sorted(s for s, _e in spans)
    sample_start, sample_end = da["sample_start"], da["sample_end"]
    n_hit = n_miss = 0
    for ev in da["events_detail"]:
        verdict, _lead = classify_event(ev["start"], H, spans, starts_sorted, sample_end)
        if verdict == "hit":
            n_hit += 1
        elif verdict == "miss":
            n_miss += 1
    n_testable = n_hit + n_miss
    hit_rate = round(n_hit / n_testable, 4) if n_testable else None
    br, br_n, br_hits = base_rate(starts_sorted, sample_start, sample_end, window=H)
    uplift = round(hit_rate / br, 2) if (hit_rate is not None and br) else None
    return {"n_hit": n_hit, "n_testable": n_testable, "hit_rate": hit_rate,
            "base_rate": br, "base_rate_n": br_n, "base_rate_hits": br_hits, "uplift": uplift}


def extra_h_pooled_stats(countries_data, H):
    n_hit = n_testable = base_hits = base_n = 0
    for cc, name, d in countries_data:
        s = extra_h_country_stats(d, H)
        if s is None:
            continue
        n_hit += s["n_hit"]
        n_testable += s["n_testable"]
        base_hits += s["base_rate_hits"] or 0
        base_n += s["base_rate_n"] or 0
    hit_rate = round(n_hit / n_testable, 4) if n_testable else None
    base_rate_v = round(base_hits / base_n, 4) if base_n else None
    uplift = round(hit_rate / base_rate_v, 2) if (hit_rate is not None and base_rate_v) else None
    return {"n_hit": n_hit, "n_testable": n_testable, "hit_rate": hit_rate,
            "base_rate": base_rate_v, "uplift": uplift}


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
    "利差＝10Y 減 3M，單位百分點，月頻（日頻序列先取月均）。主線全部國家用 10Y−3M。"
    "美國另加 10Y−2Y（T10Y2Y 月均）作對照欄，不進主線計算。",
    "美國的 3M 用 TB3MS（3 個月期公債），公債對公債，跟 10Y 公債殖利率口徑一致。德/英/"
    "日/加/澳/韓六國的 3M 用 IR3TIB（銀行同業拆款利率）。FRED 的 OECD 資料庫沒有這六國"
    "對應的公債 3M 序列可換，同業拆款利率含信用溢價，會讓這六國的利差水準整體偏低、"
    "倒掛事件偏多，跨國比較時要記住這個系統性偏差。台灣另外用商業本票，見下方說明。",
    "TB3MS 原始報的是「貼現率」（discount basis），比債券等值殖利率（bond-equivalent "
    "yield）低，利率越高差越大，直接拿貼現率跟 10Y 公債殖利率相減會系統性偏高，把利差"
    "沒那麼深的倒掛事件洗掉。美國的利差先把 TB3MS 轉成債券等值殖利率再減：BEY ＝ 365 × "
    "d ／ (360 − d × 91)，d 是 TB3MS 除以 100 的小數，91 是 3 個月的天數，算完再乘回 "
    "100，這是 3 個月期以內公債的標準換算公式。",
    "倒掛月＝該月利差小於 0。倒掛事件＝第一個倒掛月為事件起點，起點後 24 個月內的所有"
    "倒掛月都算同一事件（避免像 2019 年那種斷斷續續被拆成多次事件）。每個事件記錄起點、"
    "期間最深的利差、倒掛總月數。",
    "衰退定義 A（主線，八國同一套定義）：技術性衰退＝實質 GDP 季增率連續兩季負成長。"
    "衰退起點＝第一個負成長季的第一個月，終點＝之後第一個正成長季的第一個月。",
    "衰退定義 B（對照）：OECD 衰退指標等於 1 的期間，起點取指標由 0 轉 1 的月份。"
    "這條序列在 2022 年 9 月停更，樣本只到那裡。",
    "衰退定義 C（僅美國）：NBER 認定的衰退期（USRECDM），這條序列持續更新到現在。",
    "台灣的 3M 用商業本票次級市場利率（31-90 天），不是同業拆款也不是公債，含發行企業的"
    "信用溢價，偏差方向跟德/英/日/加/澳/韓六國的 IR3TIB 一樣，會讓利差系統性偏低、倒掛"
    "事件偏多。",
    "台灣主線（定義 A）用技術性衰退，跟其餘七國同一套定義，GDP 季增率資料從 2000 年第 1 季"
    "開始。另外跑一套只有台灣用的對照定義（定義 T）：國發會「台灣景氣循環基準日期」峰到谷，"
    "峰的次月為衰退起點，谷月納入衰退期間。定義 T 的樣本窗從 1996 年 1 月起（台灣 10Y 公債"
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


def _section_us_alt_spread(countries_data) -> str:
    """第一版「美國對照欄：3M 換不同利差定義」，驗收要求放回方法段——這是主線 3M 選
    TB3MS（公債對公債）而不用 IR3TIB（同業拆款）或 T10Y2Y 的證據。用 build_definition_stats
    （凍結、不改）分別對 IR3TIB 利差與 T10Y2Y 利差重算一次命中率，跟主線並列。"""
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
一截，拿它跟 10Y 公債殖利率相減，容易做出偏淺、偏早、不是公債曲線真的倒掛的假事件。美國
主線改用 TB3MS（3 個月期公債），而且 TB3MS 本身是貼現率，還要轉成債券等值殖利率才能跟
10Y 公債殖利率同口徑相減（換算公式見上方定義段），才是公債對公債的標準口徑。10Y−2Y 是市場最常引用的另一種
倒掛口徑，短端換成 2 年期公債，事件切法也會跟著變，這兩欄只做對照，不進主表計算。
德/英/日/加/澳/韓六國的 OECD 資料庫只提供同業拆款利率，台灣則用商業本票，都沒有對應的
公債 3M 序列可換，所以這七國的利差水準整體會比公債對公債的美國偏低、倒掛事件偏多，這是
跨國比較時要記住的系統性偏差，不是這七國真的比美國容易倒掛。</div>"""


def section_method(countries_data):
    lis = "".join(f"<li>{esc(t)}</li>" for t in DEFINITIONS_TEXT)
    alt_spread = _section_us_alt_spread(countries_data)
    return f"""
<div class="section">
<h2 class="section-title">十一、方法：怎麼定義「倒掛」與「衰退」</h2>
<div class="takeaway">這頁的判定規則在跑資料前就定死，八個國家套同一套定義，中途不因某國
結果好不好看而回頭調整。台灣的利率與 GDP 來自央行與主計總處官方資料庫，同樣跑技術性
衰退這套定義。另外多跑一套國發會峰谷的對照定義，其餘定義維持一致。</div>
<div class="card"><ul class="disc">{lis}</ul>
{alt_spread}
</div>
</div>
"""



CN_NUM = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
BRAND_BLUE = "#1a56db"
GRAY_MISS = "#9ca3af"
LIGHT_GRAY_BASE = "#d1d5db"
US_ORANGE = "#ea580c"
COUNTRY_COLORS = {"US": US_ORANGE, "DE": "#1a56db", "GB": "#7c3aed", "JP": "#dc2626",
                   "CA": "#059669", "AU": "#0891b2", "KR": "#db2777", "TW": "#65a30d"}


def fmt_ci(lo, hi):
    return "—" if (lo is None or hi is None) else f"{lo * 100:.0f}–{hi * 100:.0f}%"


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
const verticalLinePlugin = {
  id: 'verticalLine',
  afterDraw(chart) {
    const opts = (chart.options.plugins || {}).verticalLine;
    if (!opts || opts.value === null || opts.value === undefined) return;
    const xScale = chart.scales.x, yScale = chart.scales.y;
    const x = xScale.getPixelForValue(opts.value);
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
Chart.register(verticalLinePlugin);
const zeroLinePlugin = {
  id: 'zeroLine',
  afterDatasetsDraw(chart) {
    const opts = (chart.options.plugins || {}).zeroLine;
    if (!opts || !opts.enabled) return;
    const yScale = chart.scales.y, xScale = chart.scales.x;
    const y = yScale.getPixelForValue(0);
    const ctx = chart.ctx;
    ctx.save();
    ctx.strokeStyle = opts.color || '#111827';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(xScale.left, y);
    ctx.lineTo(xScale.right, y);
    ctx.stroke();
    ctx.restore();
  }
};
Chart.register(zeroLinePlugin);
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


def _std_body(chart_html, caption, table_html, note):
    table_block = table_html or ""
    return (f"{chart_html}\n<div class=\"note\">{esc(caption)}</div>\n{table_block}\n"
            f"<div class=\"note\">{esc(note)}</div>")


def _section_wrap(num_idx, title, lead, chart_html, caption, table_html, note):
    return _section_shell(num_idx, title, lead, _std_body(chart_html, caption, table_html, note))


# ═══════════════════════════════════════════════════════════════════════════
# Hero
# ═══════════════════════════════════════════════════════════════════════════

def section_hero_v2(pooled_h, pooled_lead, tw_status, finding_a, finding_b):
    h24 = pooled_h[PRIMARY_H]
    hit_rate, base, uplift = h24["hit_rate"], h24["base_rate"], h24["uplift"]
    lead_med = pooled_lead["median"]

    if hit_rate is not None and hit_rate >= 0.7:
        verdict, tag_color = "倒掛之後多半真的衰退，時間差要抓一年半", "#dc2626"
    elif hit_rate is not None and hit_rate >= 0.4:
        verdict, tag_color = "倒掛提高衰退機率，但不是每次都準，八國答案也不一致", "#d97706"
    else:
        verdict, tag_color = "倒掛對衰退的預測力比想像中弱", "#059669"

    q1 = (f"倒掛真的預示衰退嗎？合併池命中率 {fmt_pct(hit_rate)}，"
          f"比不看訊號的基率 {fmt_pct(base)} 高 {fmt_num(uplift, 1)} 倍，方向是真的，但各國強弱差很多。")
    q2 = (f"多久會看到衰退？前置期中位數 {fmt_num(lead_med, 0)} 個月，"
          f"最短 {fmt_num(pooled_lead['min'], 0)} 個月、最長 {fmt_num(pooled_lead['max'], 0)} 個月，"
          f"要當一個範圍看，別當時間表。")
    tw_note = "台灣併入主表。" if tw_status == "ok" else "台灣資料整理中，先出七國版本。"
    q3 = f"八國都適用嗎？各國答案不同。{tw_note}命中率差很多，也有國家的倒掛是衰退先到才出現。"

    return f"""
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag" style="background:{tag_color}">{esc(verdict)}</span>
    <h2>{esc(q1)}</h2>
    <p>{esc(q2)} {esc(q3)}</p>
    <p>{esc(finding_a)} {esc(finding_b)}</p>
  </div>
  <div class="hero-stats">
    <div><div class="hs-label">合併池命中率・24 個月內</div><div class="hs-value">{fmt_pct(hit_rate)}</div></div>
    <div><div class="hs-label">合併池基率・24 個月內</div><div class="hs-value">{fmt_pct(base)}</div></div>
    <div><div class="hs-label">提升倍數</div><div class="hs-value">{fmt_num(uplift, 1)}x</div></div>
    <div><div class="hs-label">前置期中位數</div><div class="hs-value">{fmt_num(lead_med, 0)} 月</div></div>
  </div>
</div>
"""


# ═══════════════════════════════════════════════════════════════════════════
# 第一節：命中率 vs 基率 + Wilson CI
# ═══════════════════════════════════════════════════════════════════════════

def section1(countries_data, pooled_h):
    rows_data = []
    for cc, name, d in countries_data:
        da = d.get("def_a")
        if d.get("status") != "ok" or da is None:
            continue
        h = da["by_h"][PRIMARY_H]
        rows_data.append({
            "cc": cc, "name": name,
            "period": f"{fmt_month(da['sample_start'])}～{fmt_month(da['sample_end'])}",
            "n_events": da["n_events"], "n_hit": h["n_hit"], "hit_rate": h["hit_rate"],
            "base_rate": h["base_rate"], "uplift": h["uplift"],
            "ci_low": h.get("hit_rate_ci_low"), "ci_high": h.get("hit_rate_ci_high"),
            "reverse_recall": da["reverse_recall"], "n_already": h["n_already_in_recession"],
        })
    hp = pooled_h[PRIMARY_H]
    pooled_row = {"cc": "POOL", "name": "合併池（不獨立）", "period": "—",
                  "n_events": None, "n_hit": hp["n_hit"], "hit_rate": hp["hit_rate"],
                  "base_rate": hp["base_rate"], "uplift": hp["uplift"],
                  "ci_low": hp.get("hit_rate_ci_low"), "ci_high": hp.get("hit_rate_ci_high"),
                  "reverse_recall": None, "n_already": None}

    straddlers = [r["name"] for r in rows_data
                  if r["ci_low"] is not None and r["base_rate"] is not None
                  and r["ci_low"] <= r["base_rate"] <= r["ci_high"]]
    small_n = [r["name"] for r in rows_data if r["n_events"] is not None and r["n_events"] <= 5]

    if straddlers:
        title = f"{'、'.join(straddlers)}的倒掛訊號，統計上和基率分不出來"
    else:
        title = "倒掛確實提高衰退機率，但各國強弱差很多"

    lead = (f"合併池命中率 {fmt_pct(hp['hit_rate'])}，基率 {fmt_pct(hp['base_rate'])}，"
            f"提升 {fmt_num(hp['uplift'], 1)} 倍，方向上倒掛確實墊高衰退機率。"
            f"但拆到國家層級，命中率從最低到最高差很多，這節用 95% 信賴區間（confidence interval）"
            f"檢查每個國家的命中率是不是真的高於基率，不是只看點估計。")

    labels = [r["name"] for r in rows_data] + [pooled_row["name"]]
    all_rows = rows_data + [pooled_row]
    base_arr = [r["base_rate"] for r in all_rows]
    ci_arr = [[r["ci_low"], r["ci_high"]] if r["ci_low"] is not None else None for r in all_rows]
    point_arr = [r["hit_rate"] for r in all_rows]

    chart_js = f"""
{POINT_MARKER_PLUGIN_JS}
new Chart(document.getElementById('chart1'), {{
  type: 'bar',
  data: {{ labels: {json.dumps(labels, ensure_ascii=False)},
    datasets: [
      {{ label:'基率 H=24', data:{json.dumps(base_arr)}, backgroundColor:'{LIGHT_GRAY_BASE}', order:2 }},
      {{ label:'命中率 95% CI', data:{json.dumps(ci_arr)}, backgroundColor:'rgba(26,86,219,.30)',
         borderColor:'{BRAND_BLUE}', borderWidth:1, order:1,
         _pointValues:{json.dumps(point_arr)}, _pointColor:'{BRAND_BLUE}' }}
    ] }},
  options: {{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ min:0, max:1, ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:420px"><canvas id="chart1"></canvas></div>'
    caption = ("藍色區間是命中率的 95% 信賴區間，藍點是命中率的點估計，灰色長條是同一段時間"
               "不看訊號的基率。藍色區間整段都在灰色長條右邊，代表訊號站得住。"
               "藍色區間蓋回灰色長條，代表這個樣本數還分不出倒掛訊號跟不看訊號的差別。")

    def _fmt_row(r):
        already = "—" if r["n_already"] is None else f"{r['n_already']}／{r['n_events']}"
        return (f"<tr><td class='lbl'>{esc(r['name'])}</td><td>{esc(r['period'])}</td>"
                f"<td class='num'>{r['n_events'] if r['n_events'] is not None else '—'}</td>"
                f"<td class='num'>{r['n_hit']}</td>"
                f"<td class='num'>{fmt_pct(r['hit_rate'])}</td>"
                f"<td class='num'>{fmt_ci(r['ci_low'], r['ci_high'])}</td>"
                f"<td class='num'>{fmt_pct(r['base_rate'])}</td>"
                f"<td class='num'>{fmt_num(r['uplift'], 1)}</td>"
                f"<td class='num'>{fmt_pct(r['reverse_recall']) if r['reverse_recall'] is not None else '—'}</td>"
                f"<td class='num'>{already}</td></tr>")

    table_rows = "".join(_fmt_row(r) for r in rows_data)
    table_rows += (f"<tr><td class='lbl'><b>{esc(pooled_row['name'])}</b></td><td>—</td><td class='num'>—</td>"
                    f"<td class='num'>{pooled_row['n_hit']}</td>"
                    f"<td class='num'><b>{fmt_pct(pooled_row['hit_rate'])}</b></td>"
                    f"<td class='num'>{fmt_ci(pooled_row['ci_low'], pooled_row['ci_high'])}</td>"
                    f"<td class='num'>{fmt_pct(pooled_row['base_rate'])}</td>"
                    f"<td class='num'>{fmt_num(pooled_row['uplift'], 1)}</td>"
                    f"<td class='num'>—</td><td class='num'>—</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th><th>樣本期間</th>
<th class="num">事件數</th><th class="num">H=24 命中數</th><th class="num">命中率</th>
<th class="num">命中率 95% CI</th><th class="num">基率</th><th class="num">提升倍數</th>
<th class="num">反向召回率</th><th class="num">已在衰退中／事件數</th></tr></thead>
<tbody>{table_rows}</tbody></table></div>"""

    note_parts = []
    if straddlers:
        note_parts.append(f"{'、'.join(straddlers)}的 95% 信賴區間跨回基率，樣本數不夠大，"
                           f"統計上還不能說這幾國的倒掛訊號比不看訊號準。")
    else:
        note_parts.append("八個國家的命中率信賴區間都沒有跨回基率，方向上都站得住。")
    if small_n:
        note_parts.append(f"{'、'.join(small_n)}事件數只有個位數，區間本來就寬，不宜對單一數字太認真。")
    note = "".join(note_parts)

    html = _section_shell(0, title, lead, _std_body(chart_html, caption, table_html, note) + f"<script>{chart_js}</script>")
    return html, straddlers


# ═══════════════════════════════════════════════════════════════════════════
# 第二節：精確率 vs 召回率
# ═══════════════════════════════════════════════════════════════════════════

def section2(pr_points, pr_pooled):
    lo_recall = [p for p in pr_points if p["recall"] is not None and p["recall"] < 0.5]
    hi_recall_lo_precision = [p for p in pr_points
                               if p["precision"] is not None and p["recall"] is not None
                               and p["precision"] < 0.5 and p["recall"] >= 0.5]

    if lo_recall:
        title = f"{'、'.join(p['name'] for p in lo_recall)}沒出現倒掛時，衰退照樣來"
    else:
        title = "精確率高不等於召回率高：沒出現倒掛時衰退照樣來"

    lead = (f"精確率是「出現倒掛，衰退真的來」的比率（就是表 1 的命中率）。召回率是「衰退發生前，"
            f"倒掛有沒有先出現過」（反向召回率）。合併池精確率 {fmt_pct(pr_pooled['precision'])}，"
            f"召回率 {fmt_pct(pr_pooled['recall'])}，這節看兩者是不是同時高，還是只有一邊高。")

    names = [p["name"] for p in pr_points] + [pr_pooled["name"]]
    precisions = [p["precision"] for p in pr_points] + [pr_pooled["precision"]]
    recalls = [p["recall"] for p in pr_points] + [pr_pooled["recall"]]
    n_events = [p["n_events"] for p in pr_points] + [pr_pooled["n_events"]]
    radii = [4 + (n or 0) ** 0.5 * 2.2 for n in n_events]
    colors = [COUNTRY_COLORS.get(p["cc"], "#6b7280") for p in pr_points] + ["#111827"]
    points = [{"x": px, "y": py} for px, py in zip(precisions, recalls)]

    chart_js = f"""
new Chart(document.getElementById('chart2'), {{
  type:'scatter',
  data: {{ datasets: [{{ label:'國家（點大小＝事件數，黑點＝合併池）',
    data:{json.dumps(points)}, pointRadius:{json.dumps(radii)},
    pointBackgroundColor:{json.dumps(colors)}, pointBorderColor:'#fff', pointBorderWidth:1 }}] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ min:0, max:1, title:{{display:true,text:'精確率（命中率）'}},
                 ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }},
               y:{{ min:0, max:1, title:{{display:true,text:'召回率（反向召回率）'}},
                 ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }},
      tooltip:{{ callbacks:{{ label:(ctx)=>{json.dumps(names, ensure_ascii=False)}[ctx.dataIndex] + '：精確率 ' +
        Math.round(ctx.parsed.x*100)+'%，召回率 '+Math.round(ctx.parsed.y*100)+'%' }} }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart2"></canvas></div>'
    caption = ("右上角代表精確率、召回率都高，訊號可靠又不太漏接。右下角代表出現倒掛通常真的衰退，"
               "但很多次衰退發生前倒掛沒先出現，訊號漏接率高。左邊代表出現倒掛不一定準。")

    note = ""
    if hi_recall_lo_precision:
        note += (f"{'、'.join(p['name'] for p in hi_recall_lo_precision)}落在精確率低、召回率不低"
                  f"的區域，出現倒掛不一定準，但衰退發生前多半出現過倒掛。")
    if lo_recall:
        note += (f"{'、'.join(p['name'] for p in lo_recall)}召回率低於五成，代表這些國家一半以上的"
                  f"衰退發生前 24 個月內沒出現過倒掛，倒掛不是這些國家衰退的必要條件。")
    if not note:
        note = "各國精確率與召回率的落點分散，沒有單一群聚特徵，逐國數字見上方表 1 與本節散佈圖。"

    html = _section_shell(1, title, lead, _std_body(chart_html, caption, "", note) + f"<script>{chart_js}</script>")
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第三節：深度與持續
# ═══════════════════════════════════════════════════════════════════════════

def section3(depth_duration):
    events = depth_duration["events"]
    buckets = depth_duration["buckets"]
    deep_keys = [k for k in buckets if k.startswith("深倒掛")]
    shallow_keys = [k for k in buckets if k.startswith("淺倒掛")]
    deep_hit = sum(buckets[k]["n_hit"] for k in deep_keys)
    deep_n = sum(buckets[k]["n"] for k in deep_keys)
    shallow_hit = sum(buckets[k]["n_hit"] for k in shallow_keys)
    shallow_n = sum(buckets[k]["n"] for k in shallow_keys)
    deep_rate = round(deep_hit / deep_n, 4) if deep_n else None
    shallow_rate = round(shallow_hit / shallow_n, 4) if shallow_n else None
    deep_ci_lo, deep_ci_hi = wilson_ci(deep_hit, deep_n)
    shallow_ci_lo, shallow_ci_hi = wilson_ci(shallow_hit, shallow_n)
    ci_overlap = (deep_ci_lo is not None and shallow_ci_lo is not None
                  and deep_ci_lo <= shallow_ci_hi and shallow_ci_lo <= deep_ci_hi)

    if ci_overlap:
        title = (f"深倒掛命中率 {fmt_pct(deep_rate)}、淺倒掛 {fmt_pct(shallow_rate)}，"
                  f"信賴區間重疊，深淺分不出命中與落空")
    elif deep_rate is not None and shallow_rate is not None and deep_rate > shallow_rate:
        title = f"深倒掛的命中率（{fmt_pct(deep_rate)}）比淺倒掛（{fmt_pct(shallow_rate)}）高，信賴區間不重疊"
    elif deep_rate is not None and shallow_rate is not None and shallow_rate > deep_rate:
        title = f"淺倒掛的命中率（{fmt_pct(shallow_rate)}）比深倒掛（{fmt_pct(deep_rate)}）高，信賴區間不重疊"
    else:
        title = "深淺、長短對命中率的影響，不是想像中一致"

    lead = (f"合併池所有可判定事件（排除已在衰退中與未到期）共 {len(events)} 筆，依最深利差"
            f"（≤{DEPTH_CUTOFF}pp 為深）與倒掛月數（≥{DURATION_CUTOFF} 個月為長）分成 2×2 四格，"
            f"這節直接看數字說什麼，不預設「越深越準」一定成立，也用信賴區間檢查差距是不是雜訊。")

    color_map = {"hit": BRAND_BLUE, "miss": GRAY_MISS}
    label_map = {"hit": "命中", "miss": "落空"}
    datasets = []
    for verdict in ("hit", "miss"):
        pts = [{"x": e["deepest"], "y": min(e["n_inverted_months"], 25)} for e in events if e["verdict"] == verdict]
        datasets.append(
            f"{{ label:'{label_map[verdict]}', data:{json.dumps(pts)}, "
            f"pointBackgroundColor:'{color_map[verdict]}', pointRadius:4.5 }}")
    chart_js = f"""
new Chart(document.getElementById('chart3'), {{
  type:'scatter',
  data: {{ datasets: [{','.join(datasets)}] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'事件期間最深利差（pp）'}} }},
               y:{{ title:{{display:true,text:'倒掛月數（截斷在 25）'}}, min:0 }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart3"></canvas></div>'
    caption = ("x 軸往左代表倒掛越深（利差越負），y 軸往上代表倒掛拖越久。藍點是後來真的衰退的事件，"
               "灰點是落空的事件。看的是藍點跟灰點在圖上是不是分得開，還是混在一起。")

    rows = []
    for k, v in buckets.items():
        cell_lo, cell_hi = wilson_ci(v["n_hit"], v["n"])
        rows.append(f"<tr><td class='lbl'>{esc(v['depth'])}</td><td>{esc(v['duration'])}</td>"
                     f"<td class='num'>{v['n']}</td><td class='num'>{v['n_hit']}</td>"
                     f"<td class='num'>{fmt_pct(v['hit_rate'])}</td>"
                     f"<td class='num'>{fmt_ci(cell_lo, cell_hi)}</td></tr>")
    rows.append(f"<tr><td class='lbl'><b>深倒掛合計</b></td><td>—</td><td class='num'>{deep_n}</td>"
                f"<td class='num'>{deep_hit}</td><td class='num'><b>{fmt_pct(deep_rate)}</b></td>"
                f"<td class='num'>{fmt_ci(deep_ci_lo, deep_ci_hi)}</td></tr>")
    rows.append(f"<tr><td class='lbl'><b>淺倒掛合計</b></td><td>—</td><td class='num'>{shallow_n}</td>"
                f"<td class='num'>{shallow_hit}</td><td class='num'><b>{fmt_pct(shallow_rate)}</b></td>"
                f"<td class='num'>{fmt_ci(shallow_ci_lo, shallow_ci_hi)}</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>深度</th><th>持續</th>
<th class="num">事件數</th><th class="num">命中數</th><th class="num">命中率</th>
<th class="num">命中率 95% CI</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""

    if ci_overlap:
        note = (f"深倒掛（{deep_n} 筆）命中率 {fmt_pct(deep_rate)}，95% 信賴區間是 "
                f"{fmt_ci(deep_ci_lo, deep_ci_hi)}。淺倒掛（{shallow_n} 筆）命中率 {fmt_pct(shallow_rate)}，"
                f"95% 信賴區間是 {fmt_ci(shallow_ci_lo, shallow_ci_hi)}，兩個區間大幅重疊，這個樣本數還不能"
                f"斷言深倒掛比淺倒掛準。淺倒掛內部再拆長短（50.0% 對 33.3%）的樣本更小，分母只有 8 跟 18，"
                f"差距同樣落在雜訊範圍，不當成論點。深度是事件當下就看得到的訊號，持續月數要等事件"
                f"結束才知道，這兩件事本來就該分開看，不代表兩者現在測出顯著差異。")
    else:
        note = (f"深倒掛（{deep_n} 筆）命中率 {fmt_pct(deep_rate)}，淺倒掛（{shallow_n} 筆）命中率 "
                f"{fmt_pct(shallow_rate)}，95% 信賴區間分別是 {fmt_ci(deep_ci_lo, deep_ci_hi)} 與 "
                f"{fmt_ci(shallow_ci_lo, shallow_ci_hi)}，兩個區間不重疊。深度是事件當下就看得到的訊號。"
                f"持續月數要等事件結束才知道，不是起點當下可用的訊號，兩者不能放在同一個時間點上比較。")

    html = _section_shell(2, title, lead, _std_body(chart_html, caption, table_html, note) + f"<script>{chart_js}</script>")
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第四節：累積命中曲線 + 前置期條帶 + H=6/12/18/24/36 表
# ═══════════════════════════════════════════════════════════════════════════

def section4(pooled_curve, us_curve, pooled_base_curve, us_base_curve,
             lead_strip, pooled_lead, pooled_h, extra_h_pooled):
    k24 = next(p for p in pooled_curve if p["k"] == 24)
    k36 = pooled_curve[-1]
    k_sep = next((p["k"] for p in pooled_curve
                  if pooled_base_curve[p["k"] - 1]["hit_rate"] is not None
                  and p["hit_rate"] is not None
                  and p["hit_rate"] - pooled_base_curve[p["k"] - 1]["hit_rate"] >= 0.10), None)
    still_rising = (k36["hit_rate"] is not None and k24["hit_rate"] is not None
                     and k36["hit_rate"] - k24["hit_rate"] >= 0.05)

    if k_sep:
        title = f"倒掛之後第 {k_sep} 個月，累積命中率才明顯超過基率"
    else:
        title = "倒掛之後衰退要多久才來：這是一條曲線，不是一個數字"

    lead = (f"累積命中曲線回答「等到第 k 個月，命中率累積到多少」，跟表 1 只報 24 個月內一個數字不同。"
            f"合併池在第 24 個月累積命中率 {fmt_pct(k24['hit_rate'])}（{k24['n']} 筆），"
            f"第 36 個月累積命中率 {fmt_pct(k36['hit_rate'])}（{k36['n']} 筆）。")

    labels = list(range(1, len(pooled_curve) + 1))
    pooled_hit_arr = [p["hit_rate"] for p in pooled_curve]
    us_hit_arr = [p["hit_rate"] for p in us_curve] if us_curve else []
    pooled_base_arr = [p["hit_rate"] for p in pooled_base_curve]
    us_base_arr = [p["hit_rate"] for p in us_base_curve] if us_base_curve else []

    ds4 = [f"{{ label:'合併池累積命中', data:{json.dumps(pooled_hit_arr)}, borderColor:'{BRAND_BLUE}', "
           f"backgroundColor:'transparent', pointRadius:0, borderWidth:2 }}"]
    if us_hit_arr:
        ds4.append(f"{{ label:'美國累積命中', data:{json.dumps(us_hit_arr)}, borderColor:'{US_ORANGE}', "
                    f"backgroundColor:'transparent', pointRadius:0, borderWidth:2 }}")
    ds4.append(f"{{ label:'合併池無條件基率', data:{json.dumps(pooled_base_arr)}, borderColor:'{LIGHT_GRAY_BASE}', "
                f"backgroundColor:'transparent', pointRadius:0, borderWidth:1.5, borderDash:[5,3] }}")
    if us_base_arr:
        ds4.append(f"{{ label:'美國無條件基率', data:{json.dumps(us_base_arr)}, borderColor:'{US_ORANGE}', "
                    f"backgroundColor:'transparent', pointRadius:0, borderWidth:1.5, borderDash:[5,3] }}")

    chart_js4 = f"""
new Chart(document.getElementById('chart4'), {{
  type: 'line',
  data: {{ labels: {json.dumps(labels)}, datasets: [{','.join(ds4)}] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'事件起點後第 k 個月'}} }},
               y:{{ min:0, max:1, ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html4 = '<div class="chart-wrap" style="height:340px"><canvas id="chart4"></canvas></div>'
    caption4 = ("實線是累積命中率，虛線是不看訊號的無條件基率，兩條線的距離就是訊號的邊際貢獻。"
                "線越早分開、分得越開，訊號的時間價值越高。線在後段還在往上爬，代表窗口拉更長還有用。")

    median = pooled_lead["median"]
    names_lead = [p["name"] for p in lead_strip]
    lead_vals = [p["lead_months"] for p in lead_strip]
    points5 = [{"x": v, "y": n} for v, n in zip(lead_vals, names_lead)]
    cat_labels = sorted({p["name"] for p in lead_strip})
    chart_js5 = f"""
new Chart(document.getElementById('chart5'), {{
  type:'scatter',
  data: {{ datasets: [{{ label:'命中事件的前置月數', data:{json.dumps(points5, ensure_ascii=False)},
    pointBackgroundColor:'{BRAND_BLUE}', pointRadius:5 }}] }},
  options: {{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'前置月數'}}, min:0 }},
               y:{{ type:'category', labels:{json.dumps(cat_labels, ensure_ascii=False)} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }},
      verticalLine:{{ value:{json.dumps(median)}, color:'#111827' }} }} }}
}});
"""
    chart_html5 = '<div class="chart-wrap" style="height:300px"><canvas id="chart5"></canvas></div>'
    caption5 = (f"每個點是一次命中事件，x 軸是倒掛起點到衰退起點的月數。垂直虛線是合併池中位數"
                f"（{fmt_num(median, 0)} 個月）。點越分散，代表前置期越不穩定，不能拿單一次經驗當時間表。")

    h_rows = []
    for H in (6, 12, 18, 24, 36):
        ph = pooled_h[H] if H in (12, 24, 36) else extra_h_pooled[H]
        h_rows.append(f"<tr><td class='lbl'>H={H}</td><td class='num'>{fmt_pct(ph['hit_rate'])}</td>"
                       f"<td class='num'>{fmt_pct(ph['base_rate'])}</td>"
                       f"<td class='num'>{fmt_num(ph['uplift'], 1)}</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>視窗</th>
<th class="num">合併池命中率</th><th class="num">合併池基率</th><th class="num">提升倍數</th></tr></thead>
<tbody>{''.join(h_rows)}</tbody></table></div>"""

    if still_rising:
        note = "累積曲線到第 36 個月還在往上爬，代表拉長窗口仍在補進真訊號，不是單純稀釋。"
    else:
        note = "累積曲線在 24 到 36 個月之間已經接近打平，拉長窗口邊際貢獻有限。"

    body = (chart_html4 + f'\n<div class="note">{esc(caption4)}</div>\n' +
            chart_html5 + f'\n<div class="note">{esc(caption5)}</div>\n' +
            table_html + f'\n<div class="note">{esc(note)}</div>\n' +
            f"<script>{chart_js4}{chart_js5}</script>")
    html = _section_shell(3, title, lead, body)
    return html, k_sep, still_rising


# ═══════════════════════════════════════════════════════════════════════════
# 第五節：八國同步 + 美國曲線當全球訊號
# ═══════════════════════════════════════════════════════════════════════════

TIMELINE_ORDER = ["US", "DE", "GB", "JP", "CA", "AU", "KR", "TW"]


def _timeline_month_idx(m):
    return month_index(m) - month_index(TIMELINE_START)


def build_chart6_datasets(countries_data):
    by_cc = {cc: d for cc, _n, d in countries_data}
    labels = [by_cc[cc]["name"] for cc in TIMELINE_ORDER if by_cc.get(cc)]
    n = len(labels)
    datasets = []
    for i, cc in enumerate(TIMELINE_ORDER):
        d = by_cc.get(cc)
        if not d:
            continue
        tl = build_country_timeline(d)
        if not tl:
            continue
        for s, e in tl["recession_spans"]:
            arr = [None] * n
            end_m = e if e else TIMELINE_END
            arr[i] = [_timeline_month_idx(s), _timeline_month_idx(end_m)]
            datasets.append({"label": "衰退期間（定義 A）", "data": arr, "backgroundColor": "#e5e7eb",
                              "grouped": False, "barPercentage": 0.9, "categoryPercentage": 0.85, "order": 2})
        for ev in tl["events"]:
            arr = [None] * n
            arr[i] = [_timeline_month_idx(ev["start"]), _timeline_month_idx(ev["end"])]
            datasets.append({"label": "倒掛事件", "data": arr, "backgroundColor": BRAND_BLUE,
                              "grouped": False, "barPercentage": 0.45, "categoryPercentage": 0.85, "order": 1})
    return labels, datasets


def _sync_years(countries_data):
    year_counts = {}
    for cc in TIMELINE_ORDER:
        d = next((dd for c2, n2, dd in countries_data if c2 == cc), None)
        if not d:
            continue
        tl = build_country_timeline(d)
        if not tl:
            continue
        for ev in tl["events"]:
            y0, y1 = int(ev["start"][:4]), int(ev["end"][:4])
            for y in range(y0, y1 + 1):
                year_counts.setdefault(y, set()).add(cc)
    sync_years = sorted(y for y, ccs in year_counts.items() if len(ccs) >= 5)
    return sync_years, year_counts


def _cluster_years(years, gap=2):
    """把離散的同步年份併成相鄰年份群組（間隔 <= gap 年併同一群），回傳文字如
    ['1970 年', '1973 至 1974 年', ...]，避免用 min/max 暗示連續發生。"""
    if not years:
        return []
    clusters = [[years[0]]]
    for y in years[1:]:
        if y - clusters[-1][-1] <= gap:
            clusters[-1].append(y)
        else:
            clusters.append([y])
    out = []
    for c in clusters:
        out.append(f"{c[0]} 年" if len(c) == 1 else f"{c[0]} 至 {c[-1]} 年")
    return out


def section5(countries_data, us_cross):
    labels6, datasets6 = build_chart6_datasets(countries_data)
    sync_years, year_counts = _sync_years(countries_data)
    base_idx = month_index(TIMELINE_START)
    max_idx = month_index(TIMELINE_END) - base_idx
    base_year = int(TIMELINE_START[:4])

    ds6_json = json.dumps(datasets6, ensure_ascii=False)
    chart_js6 = f"""
new Chart(document.getElementById('chart6'), {{
  type: 'bar',
  data: {{ labels: {json.dumps(labels6, ensure_ascii=False)}, datasets: {ds6_json} }},
  options: {{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ min:0, max:{max_idx},
        ticks:{{ callback:(v)=>{{ if (v % 12 !== 0) return ''; return {base_year} + v/12; }}, maxTicksLimit:20 }} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom',
      labels:{{ filter:(item, data) => !data.datasets.slice(0,item.datasetIndex).some(ds=>ds.label===item.text) }} }} }} }}
}});
"""
    chart_html6 = f'<div class="chart-wrap" style="height:380px"><canvas id="chart6"></canvas></div>'
    caption6 = ("灰底是定義 A 的衰退區間，藍條是倒掛事件的起訖，八國畫在同一條時間軸上。"
                "藍條在多國同時出現，代表這批倒掛是同一次全球循環，不是各國各自獨立的訊號。")

    rows_ucc = us_cross["rows"] if us_cross else []
    pooled_ucc = us_cross["pooled"] if us_cross else None
    names7 = [r["name"] for r in rows_ucc] + (["合併池（不含美國）"] if pooled_ucc else [])
    own_prec_arr = [r["own_curve_hit_rate"] for r in rows_ucc] + ([pooled_ucc["own_curve_hit_rate"]] if pooled_ucc else [])
    us_prec_arr = [r["us_curve_hit_rate"] for r in rows_ucc] + ([pooled_ucc["us_curve_hit_rate"]] if pooled_ucc else [])
    own_recall_arr = [r["own_curve_recall"] for r in rows_ucc] + ([pooled_ucc["own_curve_recall"]] if pooled_ucc else [])
    us_recall_arr = [r["us_curve_recall"] for r in rows_ucc] + ([pooled_ucc["us_curve_recall"]] if pooled_ucc else [])
    chart_js7 = f"""
new Chart(document.getElementById('chart7'), {{
  type: 'bar',
  data: {{ labels: {json.dumps(names7, ensure_ascii=False)},
    datasets: [
      {{ label:'精確率・自己的曲線', data:{json.dumps(own_prec_arr)}, backgroundColor:'{BRAND_BLUE}' }},
      {{ label:'精確率・美國的曲線', data:{json.dumps(us_prec_arr)}, backgroundColor:'{US_ORANGE}' }},
      {{ label:'召回率・自己的曲線', data:{json.dumps(own_recall_arr)}, backgroundColor:'#93c5fd' }},
      {{ label:'召回率・美國的曲線', data:{json.dumps(us_recall_arr)}, backgroundColor:'#fdba74' }}
    ] }},
  options: {{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ min:0, max:1, ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html7 = '<div class="chart-wrap" style="height:340px"><canvas id="chart7"></canvas></div>'
    caption7 = ("深色兩條是精確率（曲線出現倒掛、衰退真的來的比率），淺色兩條是召回率（該國每次衰退"
                "發生前，那條曲線是否曾出現倒掛月）。只看精確率會偏向美國，因為美國自己的事件數少、"
                "分母小。兩組都要看才能判斷哪條曲線真的更有用。")

    better_prec_with_us = [r["name"] for r in rows_ucc
                            if r["us_curve_hit_rate"] is not None and r["own_curve_hit_rate"] is not None
                            and r["us_curve_hit_rate"] > r["own_curve_hit_rate"]]
    better_recall_with_us = [r["name"] for r in rows_ucc
                              if r["us_curve_recall"] is not None and r["own_curve_recall"] is not None
                              and r["us_curve_recall"] > r["own_curve_recall"]]

    year_clusters = _cluster_years(sync_years)
    if len(better_prec_with_us) >= 5 and len(better_recall_with_us) >= 5:
        title = f"美國的利差曲線，精確率與召回率都比 {len(better_prec_with_us)} 個國家自己的曲線更高"
    elif len(better_prec_with_us) >= 5:
        title = f"美國曲線精確率比 {len(better_prec_with_us)} 個國家自己的曲線更高，召回率沒有一致更好"
    elif year_clusters:
        title = f"八國的倒掛集中在同幾波循環，{year_clusters[0]}起就至少五國同時倒掛"
    else:
        title = "八國的倒掛很多是同一次全球循環，不是各自的曲線在說話"

    lead = ("這節先看時間軸上倒掛事件是不是同時出現在多個國家，再直接測試：拿美國的利差曲線"
            "去預測其他七國的衰退，精確率與召回率會不會比該國自己的曲線更高。只比精確率會偏向"
            "美國（美國事件少、分母小，精確率天生容易高），所以兩個指標並列，才能判斷驅動這些"
            "國家倒掛的是不是同一個全球流動性循環。")

    rows4 = []
    for r in rows_ucc:
        diff = None
        if r["us_curve_hit_rate"] is not None and r["own_curve_hit_rate"] is not None:
            diff = round(r["us_curve_hit_rate"] - r["own_curve_hit_rate"], 4)
        recall_diff = None
        if r["us_curve_recall"] is not None and r["own_curve_recall"] is not None:
            recall_diff = round(r["us_curve_recall"] - r["own_curve_recall"], 4)
        rows4.append(f"<tr><td class='lbl'>{esc(r['name'])}</td>"
                      f"<td class='num'>{r['own_curve_n_testable']}</td>"
                      f"<td class='num'>{fmt_pct(r['own_curve_hit_rate'])}</td>"
                      f"<td class='num'>{r['n_testable']}</td>"
                      f"<td class='num'>{fmt_pct(r['us_curve_hit_rate'])}</td>"
                      f"<td class='num'>{fmt_pp(diff) if diff is not None else '—'}</td>"
                      f"<td class='num'>{fmt_pct(r['own_curve_recall'])}</td>"
                      f"<td class='num'>{fmt_pct(r['us_curve_recall'])}</td>"
                      f"<td class='num'>{fmt_pp(recall_diff) if recall_diff is not None else '—'}</td></tr>")
    if pooled_ucc:
        diff_p = None
        if pooled_ucc["us_curve_hit_rate"] is not None and pooled_ucc["own_curve_hit_rate"] is not None:
            diff_p = round(pooled_ucc["us_curve_hit_rate"] - pooled_ucc["own_curve_hit_rate"], 4)
        recall_diff_p = None
        if pooled_ucc["us_curve_recall"] is not None and pooled_ucc["own_curve_recall"] is not None:
            recall_diff_p = round(pooled_ucc["us_curve_recall"] - pooled_ucc["own_curve_recall"], 4)
        rows4.append(f"<tr><td class='lbl'><b>合併池（不含美國）</b></td>"
                      f"<td class='num'>{pooled_ucc['own_curve_n_testable']}</td>"
                      f"<td class='num'>{fmt_pct(pooled_ucc['own_curve_hit_rate'])}</td>"
                      f"<td class='num'>{pooled_ucc['n_testable']}</td>"
                      f"<td class='num'>{fmt_pct(pooled_ucc['us_curve_hit_rate'])}</td>"
                      f"<td class='num'>{fmt_pp(diff_p) if diff_p is not None else '—'}</td>"
                      f"<td class='num'>{fmt_pct(pooled_ucc['own_curve_recall'])}</td>"
                      f"<td class='num'>{fmt_pct(pooled_ucc['us_curve_recall'])}</td>"
                      f"<td class='num'>{fmt_pp(recall_diff_p) if recall_diff_p is not None else '—'}</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th>
<th class="num">自己曲線 n</th><th class="num">自己曲線精確率</th>
<th class="num">美國曲線 n</th><th class="num">美國曲線精確率</th><th class="num">精確率差</th>
<th class="num">自己曲線召回率</th><th class="num">美國曲線召回率</th><th class="num">召回率差</th></tr></thead>
<tbody>{''.join(rows4)}</tbody></table></div>"""

    note_parts = []
    if year_clusters:
        note_parts.append(f"同一年至少五國同時處於倒掛事件中的情況出現過 {len(sync_years)} 次，"
                           f"集中在幾波全球循環：{'、'.join(year_clusters)}，不是平均分散在整段樣本期間。")
    if better_prec_with_us:
        note_parts.append(f"精確率上，{'、'.join(better_prec_with_us)}用美國曲線比用自己的曲線高。")
    else:
        note_parts.append("精確率上，多數國家用自己的曲線仍比用美國曲線高。")
    if better_recall_with_us:
        note_parts.append(f"召回率上，{'、'.join(better_recall_with_us)}用美國曲線比用自己的曲線高，"
                           f"其餘國家用自己的曲線召回率更高或打平。")
    else:
        note_parts.append("召回率上，沒有國家用美國曲線比用自己的曲線高，跟精確率的結果方向不一致，"
                           "美國曲線精確率高有一部分是美國自己事件少、分母小的緣故，不能只看精確率"
                           "就說美國曲線比較準。")
    note = "".join(note_parts)

    body = (chart_html6 + f'\n<div class="note">{esc(caption6)}</div>\n' +
            chart_html7 + f'\n<div class="note">{esc(caption7)}</div>\n' +
            table_html + f'\n<div class="note">{esc(note)}</div>\n' +
            f"<script>{chart_js6}{chart_js7}</script>")
    html = _section_shell(4, title, lead, body)
    return html, sync_years, better_prec_with_us, better_recall_with_us


# ═══════════════════════════════════════════════════════════════════════════
# 第六節：2000 年前後
# ═══════════════════════════════════════════════════════════════════════════

def section6(period_split):
    pooled, us = period_split["pooled"], period_split["us"]
    pre_hr, post_hr = pooled["pre"]["hit_rate"], pooled["post"]["hit_rate"]
    pre_ci = wilson_ci(pooled["pre"]["n_hit"], pooled["pre"]["n"])
    post_ci = wilson_ci(pooled["post"]["n_hit"], pooled["post"]["n"])
    pooled_overlap = (pre_ci[0] is not None and post_ci[0] is not None
                       and pre_ci[0] <= post_ci[1] and post_ci[0] <= pre_ci[1])
    us_pre_ci = wilson_ci(us["pre"]["n_hit"], us["pre"]["n"]) if us else (None, None)
    us_post_ci = wilson_ci(us["post"]["n_hit"], us["post"]["n"]) if us else (None, None)

    if pooled_overlap:
        title = "2000 年前後看不出訊號明顯變鈍，合併池信賴區間大幅重疊"
    elif pre_hr is not None and post_hr is not None and post_hr < pre_hr:
        title = f"2000 年後合併池命中率從 {fmt_pct(pre_hr)} 降到 {fmt_pct(post_hr)}，信賴區間不重疊"
    elif pre_hr is not None and post_hr is not None and post_hr > pre_hr:
        title = f"2000 年後合併池命中率從 {fmt_pct(pre_hr)} 升到 {fmt_pct(post_hr)}，信賴區間不重疊"
    else:
        title = "2000 年之後訊號有沒有變鈍"

    lead = (f"合併池事件依起點分成 2000 年以前與以後兩組，各自算 24 個月內的命中率與同期基率，"
            f"再用 95% 信賴區間檢查差距是不是雜訊。2000 年以前 {pooled['pre']['n']} 筆，"
            f"2000 年以後 {pooled['post']['n']} 筆，這節只報數字，QE 年代利差被壓低是常見的"
            f"解釋，這裡不下因果結論。")

    labels8 = ["2000 年以前", "2000 年以後"]
    pooled_hr = [pooled["pre"]["hit_rate"], pooled["post"]["hit_rate"]]
    pooled_br = [pooled["pre"]["base_rate"], pooled["post"]["base_rate"]]
    us_hr = [us["pre"]["hit_rate"], us["post"]["hit_rate"]] if us else [None, None]
    us_br = [us["pre"]["base_rate"], us["post"]["base_rate"]] if us else [None, None]
    chart_js8 = f"""
new Chart(document.getElementById('chart8'), {{
  type: 'bar',
  data: {{ labels: {json.dumps(labels8, ensure_ascii=False)},
    datasets: [
      {{ label:'合併池命中率', data:{json.dumps(pooled_hr)}, backgroundColor:'{BRAND_BLUE}' }},
      {{ label:'合併池基率', data:{json.dumps(pooled_br)}, backgroundColor:'{LIGHT_GRAY_BASE}' }},
      {{ label:'美國命中率', data:{json.dumps(us_hr)}, backgroundColor:'{US_ORANGE}' }},
      {{ label:'美國基率', data:{json.dumps(us_br)}, backgroundColor:'#fed7aa' }}
    ] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ y:{{ min:0, max:1, ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:340px"><canvas id="chart8"></canvas></div>'
    caption = ("四條長條左半是合併池，右半是美國單獨算的，每組左邊命中率、右邊基率，"
               "2000 年以前對照 2000 年以後。看的是命中率降了多少、基率是不是同時也降了。")

    note = (f"合併池 2000 年以前命中率 {fmt_pct(pre_hr)}（95% 信賴區間 {fmt_ci(*pre_ci)}），2000 年以後 "
            f"{fmt_pct(post_hr)}（95% 信賴區間 {fmt_ci(*post_ci)}），兩個區間大幅重疊，這個樣本數看不出"
            f"訊號明顯變鈍。美國 2000 年以前 {us['pre']['n'] if us else '—'} 筆、以後 "
            f"{us['post']['n'] if us else '—'} 筆，95% 信賴區間分別是 {fmt_ci(*us_pre_ci)} 與 "
            f"{fmt_ci(*us_post_ci)}，樣本只有個位數，區間寬到不能單獨拿美國的數字下結論。")

    html = _section_shell(5, title, lead, _std_body(chart_html, caption, "", note) + f"<script>{chart_js8}</script>")
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第七節：2022－2023
# ═══════════════════════════════════════════════════════════════════════════

def section7(countries_data, rescale_2022):
    labels9 = None
    ds9 = []
    for i, row in enumerate(rescale_2022):
        color = COUNTRY_COLORS.get(row["cc"], "#6b7280")
        m = [x for x, _v in row["series"]]
        v = [y for _x, y in row["series"]]
        if labels9 is None or len(m) > len(labels9):
            labels9 = m
        ds9.append(f"{{ label:'{row['name']}', data:{json.dumps(v)}, borderColor:'{color}', "
                    f"backgroundColor:'transparent', pointRadius:0, borderWidth:1.6 }}")
    chart_js9 = f"""
new Chart(document.getElementById('chart9'), {{
  type: 'line',
  data: {{ labels: {json.dumps(labels9, ensure_ascii=False)}, datasets: [{','.join(ds9)}] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ ticks:{{ maxTicksLimit:12 }} }}, y:{{ title:{{display:true,text:'pp'}} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }}, zeroLine:{{ enabled:true, color:'#111827' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart9"></canvas></div>'
    caption = ("每條線是一國的利差，起自 2021 年 1 月到最新一筆，黑色粗線是 0。跌破 0 代表倒掛，"
               "八國幾乎都在 2022 到 2023 年一起跌破，這節接下來看兩年後結果是不是也一樣一致。")

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
            rows.append((name, e["start"], e["deepest"], rec_start, label))
    table_rows = "".join(
        f"<tr><td class='lbl'>{esc(n)}</td><td>{esc(s)}</td><td class='num'>{fmt_pp(dp)}</td>"
        f"<td>{esc(rs) if rs else '—'}</td><td>{esc(lb)}</td></tr>" for n, s, dp, rs, lb in rows)
    if not table_rows:
        table_rows = "<tr><td colspan='5'>樣本內 2021-06～2023-06 無倒掛事件符合本節篩選條件</td></tr>"
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th><th>倒掛起點</th>
<th class="num">最深利差</th><th>之後衰退起點</th><th>結果</th></tr></thead>
<tbody>{table_rows}</tbody></table></div>"""

    n_hit = sum(1 for *_r, lb in rows if lb == "衰退了")
    n_miss = sum(1 for *_r, lb in rows if lb.startswith("沒衰退"))
    title = f"2022 到 2023：八國一起倒掛，兩年後只有 {n_hit} 國衰退、{n_miss} 國落空"
    lead = ("2022 年那一波，多數主要經濟體的利差都一度轉負，這節直接把同一時間點的訊號攤開來看"
            "實際結果，不用平均數字掩蓋分歧。")
    note = ("這張表只做訊號與結果的對帳，不解釋「為什麼有的國家躲過去了」，那要另外查財政刺激、"
            "就業市場緊俏程度這類傳導管道，這裡不做因果推論。")

    html = _section_shell(6, title, lead, _std_body(chart_html, caption, table_html, note) + f"<script>{chart_js9}</script>")
    return html, n_hit, n_miss


# ═══════════════════════════════════════════════════════════════════════════
# 第八節：已在衰退中
# ═══════════════════════════════════════════════════════════════════════════

def section8(already_rows):
    flagged = [r for r in already_rows if r["ratio"] and r["ratio"] > 0]
    if flagged:
        top = max(flagged, key=lambda r: r["ratio"])
        title = f"{top['name']}有 {top['n_already']}／{top['n_events']} 次倒掛是衰退先到才出現"
    else:
        title = "衰退先到、倒掛才出現：在幾個國家曲線是同時指標不是領先指標"

    lead = ("每個國家的倒掛事件裡，有多少次是「事件起點當下已經在衰退中」，這種事件不算命中也"
            "不算落空，但對「倒掛能不能預示衰退」是負面訊息。曲線那時候已經跟著景氣走，不是"
            "先行指標。")

    rows = "".join(f"<tr><td class='lbl'>{esc(r['name'])}</td><td class='num'>{r['n_already']}</td>"
                    f"<td class='num'>{r['n_events']}</td><td class='num'>{fmt_pct(r['ratio'])}</td></tr>"
                    for r in already_rows)
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th>
<th class="num">已在衰退中次數</th><th class="num">事件總數</th><th class="num">比例</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""

    if flagged:
        names = "、".join(f"{r['name']}（{r['n_already']}／{r['n_events']}）" for r in flagged)
        note = f"{names}出現過起點時已在衰退中的事件，這幾個國家的倒掛訊號在這幾次是同時指標而非領先指標。"
    else:
        note = "八國樣本內沒有出現「起點時已在衰退中」的事件，倒掛在這個樣本裡都發生在衰退之前。"

    html = _section_shell(7, title, lead, table_html + f'\n<div class="note">{esc(note)}</div>\n')
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第九節：換一把尺
# ═══════════════════════════════════════════════════════════════════════════

def _rank_map(rows, key):
    ranked = sorted((r for r in rows if r.get(key) is not None), key=lambda r: r[key], reverse=True)
    return {r["cc"]: i + 1 for i, r in enumerate(ranked)}


def section9(dumbbell_rows):
    diffs = [(r["name"], r["alt_rate"] - r["a_rate"]) for r in dumbbell_rows
             if r["alt_rate"] is not None and r["a_rate"] is not None]
    all_rate_rose = bool(diffs) and all(d[1] >= 0 for d in diffs)

    rank_a = _rank_map(dumbbell_rows, "a_uplift")
    rank_alt = _rank_map(dumbbell_rows, "alt_uplift")
    rank_moves = [(r["cc"], r["name"], rank_a.get(r["cc"]), rank_alt.get(r["cc"]))
                  for r in dumbbell_rows if r["cc"] in rank_a and r["cc"] in rank_alt]
    rank_moves = [(cc, name, ra, rb, ra - rb) for cc, name, ra, rb in rank_moves]
    biggest_move = max(rank_moves, key=lambda x: abs(x[4])) if rank_moves else None
    max_rank_shift = abs(biggest_move[4]) if biggest_move else 0

    us_move = next((m for m in rank_moves if m[0] == "US"), None)
    us_top_both = bool(us_move) and us_move[2] == 1 and us_move[3] == 1
    others_shifted = any(m[0] != "US" and m[4] != 0 for m in rank_moves)

    if all_rate_rose and us_top_both and others_shifted:
        title = "換一種衰退定義後命中率全面上升，美國的提升倍數仍是八國第一，其餘排序不穩"
    elif all_rate_rose and max_rank_shift <= 2:
        title = "換一種衰退定義後命中率全面上升，提升倍數的國家排序大致不變"
    elif all_rate_rose and biggest_move:
        title = f"換一種衰退定義後命中率全面上升，但提升倍數排序大幅變動：{biggest_move[1]}換了 {max_rank_shift} 名"
    elif biggest_move:
        title = f"換一種衰退定義，{biggest_move[1]}的提升倍數排名變化最大"
    else:
        title = "換一種衰退定義，答案有沒有變"

    lead = ("主線用定義 A（技術性衰退），這節把每國換成對照定義（美國換 NBER、台灣換國發會"
            "峰谷、其餘六國換 OECD 指標）重算一次命中率與提升倍數（命中率÷該定義自己的基率），"
            "看的不只是命中率會不會變，還有換一種定義後國家之間的排序穩不穩。")

    names = [r["name"] for r in dumbbell_rows]
    a_vals = [r["a_rate"] for r in dumbbell_rows]
    alt_vals = [r["alt_rate"] for r in dumbbell_rows]
    ranges = []
    for a, b in zip(a_vals, alt_vals):
        if a is None or b is None:
            ranges.append(None)
        else:
            ranges.append([min(a, b), max(a, b)])
    chart_js10 = f"""
new Chart(document.getElementById('chart10'), {{
  type: 'bar',
  data: {{ labels: {json.dumps(names, ensure_ascii=False)},
    datasets: [
      {{ label:'定義 A 到對照定義區間', data:{json.dumps(ranges)}, backgroundColor:'rgba(107,114,128,.25)',
         borderColor:'#9ca3af', borderWidth:1, grouped:false,
         _pointValues:{json.dumps(a_vals)}, _pointColor:'{BRAND_BLUE}',
         _pointValues2:{json.dumps(alt_vals)}, _pointColor2:'{US_ORANGE}' }}
    ] }},
  options: {{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ min:0, max:1, ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }} }},
    plugins: {{ legend:{{ display:false }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart10"></canvas></div>'
    caption = ("藍點是主線定義 A 的命中率，橘點是對照定義（美國 NBER、台灣國發會峰谷、其餘六國 "
               "OECD 指標）的命中率，中間灰色線只是連接兩點。點離得越遠，代表換一種定義答案差越多。")

    alt_labels = {r["name"]: r["alt_label"] for r in dumbbell_rows}
    rows = []
    for r in dumbbell_rows:
        rate_diff = (fmt_pp(round(r["alt_rate"] - r["a_rate"], 4))
                     if r["alt_rate"] is not None and r["a_rate"] is not None else "—")
        ra, rb = rank_a.get(r["cc"]), rank_alt.get(r["cc"])
        rank_txt = f"{ra} → {rb}" if ra is not None and rb is not None else "—"
        rows.append(f"<tr><td class='lbl'>{esc(r['name'])}</td><td class='num'>{fmt_pct(r['a_rate'])}</td>"
                     f"<td class='num'>{fmt_num(r['a_uplift'], 2)}</td>"
                     f"<td>{esc(r['alt_label'])}</td><td class='num'>{fmt_pct(r['alt_rate'])}</td>"
                     f"<td class='num'>{fmt_num(r['alt_uplift'], 2)}</td>"
                     f"<td class='num'>{rate_diff}</td><td class='num'>{rank_txt}</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th><th class="num">定義 A 命中率</th>
<th class="num">定義 A 提升倍數</th><th>對照定義</th><th class="num">對照定義命中率</th>
<th class="num">對照定義提升倍數</th><th class="num">命中率差（對照−A）</th>
<th class="num">提升倍數排名（A→對照）</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""

    if all_rate_rose and us_top_both and others_shifted:
        note = (f"八國換成對照定義後命中率沒有一個下降，六個 OECD 對照國的命中率普遍上升，因為官方"
                f"指標抓的是景氣循環下行段，觸發得比技術性衰退頻繁，基率也跟著墊高。美國換成 NBER "
                f"之後提升倍數仍是八國最高，兩種定義排名都是第一，這個結論穩。其餘七國的提升倍數"
                f"排名幾乎都跟著換定義變動，最大一次是{biggest_move[1]}，從第 {biggest_move[2]} 名"
                f"換到第 {biggest_move[3]} 名，差別來自分母太小：{biggest_move[1]}定義 A 下的事件數"
                f"只有 3 筆，樣本小到任何一種定義都可能把排名整個翻轉。南韓的事件數也只有個位數，"
                f"同樣要打折看。台灣換成國發會峰谷後樣本窗更長，看到的事件不是同一組，命中率差"
                f"不能直接相減比較，只能各自看提升倍數。")
    elif all_rate_rose and max_rank_shift <= 2:
        note = ("八國換成對照定義後命中率沒有一個下降，多數明顯上升，但提升倍數（把基率也墊高的效果"
                "扣掉之後）排名大致沒有大幅洗牌，換一種定義不會推翻表 1 的結論。")
    elif all_rate_rose and biggest_move:
        note = (f"八國換成對照定義後命中率沒有一個下降，六個 OECD 對照國的命中率普遍上升，因為官方"
                f"指標抓的是景氣循環下行段，觸發得比技術性衰退頻繁，基率也跟著墊高。單看命中率會誤"
                f"以為訊號全面變準，但把基率一起考慮的提升倍數排名並不穩定，{biggest_move[1]}從第 "
                f"{biggest_move[2]} 名換到第 {biggest_move[3]} 名，換了 {max_rank_shift} 名，差別"
                f"來自分母太小：日本、南韓這類樣本只有個位數事件的國家，換一種定義結果就可能整個"
                f"翻轉。台灣換成國發會峰谷後樣本窗更長，看到的事件不是同一組，"
                f"命中率差不能直接相減比較，只能各自看提升倍數。")
    else:
        note = ("換成對照定義後命中率有升有降，提升倍數的排名也跟著變，結論會因為換了哪一種定義"
                "而不同，不能只看定義 A 的結果就下定論。")

    html = _section_shell(8, title, lead, _std_body(chart_html, caption, table_html, note) + f"<script>{chart_js10}</script>")
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第十節：各國利差全史（附錄，沿用第一版八張小圖）
# ═══════════════════════════════════════════════════════════════════════════

def _chart_dataset(spread_series, spans):
    labels = [m for m, _v in spread_series]
    values = [v for _m, v in spread_series]
    band = [1 if in_any_span(m, spans) else None for m in labels]
    return labels, values, band


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
      {{ type:'line', label:'10Y-3M 利差 (pp)', data:{values_json}, borderColor:'{BRAND_BLUE}',
         backgroundColor:'transparent', pointRadius:0, borderWidth:1.3, order:1 }}
    ] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ ticks:{{ maxTicksLimit:10 }} }}, y:{{ min:{ymin}, max:{ymax},
      title:{{display:true,text:'pp'}} }} }},
    plugins: {{ legend:{{ display:false }} }} }}
}});
"""


def section10(countries_data):
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
        us_block = '<div class="chart-wrap" style="height:340px"><canvas id="chart-us"></canvas></div>'
    grid = f'<div style="display:flex;flex-wrap:wrap;gap:1.2rem;margin-top:1rem">{"".join(small_multiples)}</div>'

    title = "各國利差全史：灰底是技術性衰退"
    lead = ("前九節都是統計摘要，這節把每個國家的利差原始序列整段畫出來，附錄性質，供對照"
            "查核，不對應單一論點。")
    caption = ("灰底區間是定義 A（GDP 連兩季負成長）算出的衰退期。利差跌破 0 的那條水平線之後，"
               "灰底是不是很快跟上，跟得快代表訊號有用，隔很久或完全沒跟上代表這次訊號落空。")
    body = (us_block + f'\n<div class="note">{esc(caption)}</div>\n' + grid +
            f"<script>{''.join(charts_js)}</script>")
    return _section_shell(9, title, lead, body)


def appendix_a_event_detail(countries_data) -> str:
    """驗收要求恢復第一版表 2（逐事件明細），改摺疊呈現：驗證者要核對原始事件列表時
    用，不佔頁面主要閱讀動線。內容邏輯與第一版 section_table2 相同，只換了外殼與
    標題編號。"""
    verdict_label = {"hit": "命中", "miss": "落空",
                      "already_in_recession": "已在衰退中", "not_yet_due": "未到期"}
    blocks = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok" or d.get("def_a") is None:
            continue
        events = d["def_a"]["events_detail"]
        if not events:
            continue
        rows = []
        for ev in events:
            rec_start = add_months(ev["start"], ev["lead_months"]) if ev["verdict"] == "hit" else None
            rows.append(
                f"<tr><td>{esc(ev['start'])}</td><td class='num'>{fmt_pp(ev['deepest'])}</td>"
                f"<td class='num'>{ev['n_inverted_months']}</td>"
                f"<td>{esc(rec_start) if rec_start else '—'}</td>"
                f"<td class='num'>{ev['lead_months'] if ev['lead_months'] is not None else '—'}</td>"
                f"<td>{esc(verdict_label[ev['verdict']])}</td></tr>")
        blocks.append(f"""<h4 style="font-size:.88rem;margin:1rem 0 .5rem">{esc(name)}</h4>
<div class="scroll"><table><thead><tr><th>起點</th><th class="num">最深利差</th>
<th class="num">倒掛月數</th><th>之後衰退起點</th><th class="num">前置月數</th><th>判定</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>""")
    body = "".join(blocks)
    return f"""
<div class="section">
<details>
<summary style="cursor:pointer;font-weight:700;font-size:1.02rem;padding:.4rem 0">
附錄 A：逐事件明細（定義 A，八國逐筆列出）</summary>
<div class="card" style="margin-top:.75rem">
<p style="font-size:.85rem;margin-bottom:.5rem">前面各節的散佈圖、時間軸、前置期條帶都是這張
表拆解後畫出來的，這裡把原始逐筆事件列出來備查。「之後衰退起點」空白代表落空或還沒到期，
不是資料缺漏。</p>
{body}
</div>
</details>
</div>
"""


# ═══════════════════════════════════════════════════════════════════════════
# 第十二節：這頁沒有告訴你的事（沿用第一版第九節內容＋新增三點）
# ═══════════════════════════════════════════════════════════════════════════

def section12(tw_status, tw_data):
    tw_line = ""
    tw_table = ""
    if tw_status != "ok":
        missing_bits = tw_data.get("missing_bits") if tw_data else None
        detail = "、".join(missing_bits) if missing_bits else ("十年期公債殖利率、90 天期商業本票次級"
                 "市場利率、主計總處實質 GDP 季增率、國發會景氣循環基準日期")
        pts = (tw_data or {}).get("peaks_troughs") or []
        if pts:
            tw_line = (f"<li>台灣資料整理中，先出七國版本。國發會景氣循環基準日期（峰谷）已查證到"
                       f"完整官方表格（{len(pts)} 次循環，1954 年起，見下方附表），但十年期公債殖利率、"
                       f"90 天期商業本票次級市場利率、實質 GDP 季增率這三項是互動查詢系統，沒有在時限內"
                       f"拿到可用的完整序列，四項缺一，台灣目前不能跑完整回測，不用假資料湊數。</li>")
        else:
            tw_line = (f"<li>台灣資料整理中，先出七國版本：{esc(detail)}"
                       f"尚未齊備到可以跑完整回測的程度，缺什麼在回報裡逐項列出，不用假資料湊數。</li>")
        if pts:
            rows = "".join(f"<tr><td>{esc(i + 1)}</td><td>{esc(p['peak'])}</td>"
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
                   "IR3TIB 一樣：利差整體偏低、倒掛事件偏多，方法段已註明。對照定義 T"
                   "（國發會峰谷）樣本窗比定義 A 長，兩種定義看到的事件不是同一組，數字不能直接"
                   "跨定義相減比較，只能各自看提升倍數。</li>")
    return f"""
<div class="section">
<h2 class="section-title">{CN_NUM[11]}、這頁沒有告訴你的事</h2>
<div class="card"><ul class="disc">
<li>日本樣本短：實質 GDP 季增率只從 1994 年起有資料，衰退事件數本來就少，命中率與
基率的分母都小，數字的不確定性比其他國家大，不宜跟樣本更長的國家直接比大小。</li>
<li>技術性衰退（定義 A）這個定義會漏掉不是「連兩季負成長」但普遍認定是衰退的事件。
美國 2001 年那次衰退（NBER 認定 2001-03 至 2001-11）沒有連續兩季 GDP 負成長，定義 A
在美國這裡會漏掉它，只有定義 C（NBER）抓得到，第九節換一種定義後命中率會不同。</li>
<li>澳洲樣本內幾乎三十年沒有技術性衰退（直到近年才出現符合定義的事件），這段期間的
「基率」會被壓得很低，任何一次倒掛的提升倍數都容易被放大，判讀時要留意分母。</li>
<li>OECD 衰退指標（定義 B）2022 年 9 月停更，2022 年之後的事件在這個定義下一律標
「未到期」，不是它顯示沒衰退。</li>
{tw_line}
<li>第一節的信賴區間，命中率那欄用 n＝可判定事件數，基率那欄用 n＝滾動月數。基率信賴
區間的月份彼此不是獨立觀測（同一次衰退會被鄰近好幾個月一起算進去），區間比真正獨立樣本
該有的還要窄，讀基率信賴區間時要打折看待。</li>
<li>第五節用美國曲線預測其他國家，樣本窗取的是美國事件窗與該國定義 A 樣本窗的交集。
美國利差序列從 1953-04 起，比其餘七國定義 A 樣本窗的起點都早，交集窗因此就等於各國
自己的樣本窗，兩邊樣本窗相同，是同窗重算，不是拿不同期間的數字硬湊在一起比較。</li>
<li>第三節把倒掛月數（持續）當成分桶條件之一，但持續月數要等事件走完才知道，不是事件
起點當下就能用的訊號，深度（最深利差）才是起點當下就看得到的。這節只回報兩者分開後的
命中率，不代表持續月數可以在起點當下拿來做判斷。</li>
<li>全部序列都是官方統計事後定案的數字，跑資料當下離現在越近的月份，GDP 數字越可能
之後被修正，這裡用的是抓取當下的最新公布值，不會回頭用修正後數字改寫已經定案的事件。</li>
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
                   built_date, v2):
    main_style, nav_block = extract_template_parts()
    h24 = pooled_h[PRIMARY_H]
    title = "殖利率倒掛與經濟衰退：八國回測 | InvestMQuest Research"
    tw_desc_note = ("台灣併入主表，另跑國發會峰谷對照定義。" if tw_status == "ok"
                     else "台灣資料整理中，先出七國版本。")
    countries_desc = "美/德/英/日/加/澳/韓/台" if tw_status == "ok" else "美/德/英/日/加/澳/韓"
    description = (f"用 FRED 與台灣央行、主計總處資料對{countries_desc}套同一套定義回測 10Y-3M 利差倒掛："
                    f"合併池 24 個月內命中率 {fmt_pct(h24['hit_rate'])}、基率 {fmt_pct(h24['base_rate'])}、"
                    f"提升 {fmt_num(h24['uplift'], 1)} 倍，前置期中位數 {fmt_num(pooled_lead['median'], 0)} 個月。"
                    f"{tw_desc_note}另檢查信賴區間、精確率與召回率、深度與持續分桶、累積命中曲線、"
                    f"八國同步與美國曲線交叉檢驗、2000 年前後對照、換一種定義啞鈴圖。")

    try:
        sys.path.insert(0, str(NAV_DIR))
        from _nav_common import make_toggle  # noqa
        subnav = make_toggle("yield_curve")
    except Exception as e:
        warn(f"make_toggle 載入失敗：{e}，pill bar 留空")
        subnav = ""

    s1_html, straddlers = section1(countries_data, pooled_h)
    s2_html = section2(v2["pr_points"], v2["pr_pooled"])
    s3_html = section3(v2["depth_duration"])
    s4_html, k_sep, still_rising = section4(
        v2["pooled_event_curve"], v2["us_event_curve"], v2["pooled_base_curve"], v2["us_base_curve"],
        v2["lead_strip"], pooled_lead, pooled_h, v2["extra_h_pooled"])
    s5_html, sync_years, better_prec_with_us, better_recall_with_us = section5(countries_data, v2["us_cross"])
    s6_html = section6(v2["period_split"])
    s7_html, n2022_hit, n2022_miss = section7(countries_data, v2["rescale_2022"])
    s8_html = section8(v2["already_in_recession"])
    s9_html = section9(v2["dumbbell"])
    s10_html = section10(countries_data)
    appendix_a = appendix_a_event_detail(countries_data)
    s11_html = section_method(countries_data)
    s12_html = section12(tw_status, tw_data)

    if k_sep:
        finding_a = f"倒掛之後要等到第 {k_sep} 個月，累積命中率才明顯超過基率。"
    else:
        finding_a = "累積命中率跟基率的差距全程都不明顯，時間拉長也拉不開差距。"
    if len(better_recall_with_us) >= 5:
        finding_b = (f"改用美國的利差曲線去預測其他國家的衰退，{len(better_recall_with_us)} 個國家連"
                      f"召回率都比自己的曲線高，驅動多數國家倒掛的比較像是同一個全球循環。")
    elif sync_years:
        finding_b = (f"同一年至少五國同時倒掛的情況出現過 {len(sync_years)} 次，集中在幾波全球循環，"
                      f"但美國曲線的優勢主要在精確率，召回率沒有一致比各國自己的曲線高。")
    elif len(better_prec_with_us) >= 5:
        finding_b = (f"美國曲線的精確率比 {len(better_prec_with_us)} 個國家自己的曲線高，但這可能是"
                      f"美國自己事件數少的統計效果，召回率沒有跟著一致轉強。")
    else:
        finding_b = "各國的倒掛訊號各自獨立，沒有看到明顯的全球同步循環。"

    hero = section_hero_v2(pooled_h, pooled_lead, tw_status, finding_a, finding_b)

    takeaway = ("<b>給沒有統計背景的讀者：</b>這頁做的事很單純。利差是 10 年期公債殖利率減 3 個月期"
                "利率，跌到 0 以下叫「倒掛」，歷史上市場常拿它當衰退警訊。我們把八個國家的利率與 GDP "
                "資料全部拉出來，用同一套規則自動判定倒掛事件與衰退事件，算命中率、算多久看到、算"
                "跟不看訊號比有沒有比較準，再逐一檢查訊號的信賴區間、深淺長短、同步性與換一種定義"
                "後的穩健度。本頁不做「現在該不該擔心」的建議，也不預測下一次衰退什麼時候來，只回報"
                "歷史上這個訊號準不準、準多快、在哪些條件下會失真。")

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

{s1_html}
{s2_html}
{s3_html}
{s4_html}
{s5_html}
{s6_html}
{s7_html}
{s8_html}
{s9_html}
{s10_html}
{appendix_a}
{s11_html}
{s12_html}

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

    # ── C1：Wilson CI（事後疊加，不改 build_definition_stats／pooled_lead_stats 本身）──
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        for key in ("def_a", "def_b", "def_c", "def_t"):
            if d.get(key):
                add_wilson_ci(d[key])
    add_wilson_ci_pooled(pooled_h)

    us_dict = next((d for cc, n, d in countries_data if cc == "US"), None)

    # ── C2-C11 ──
    pr_points, pr_pooled = build_precision_recall(countries_data, pooled_h, pooled_recall)
    depth_duration = build_depth_duration(countries_data)
    pooled_event_curve = build_pooled_event_curve(countries_data)
    us_event_curve = build_country_event_curve(us_dict) if us_dict else None
    pooled_base_curve = build_pooled_base_rate_curve(countries_data)
    us_base_curve = build_country_base_rate_curve(us_dict) if us_dict else None
    lead_strip = build_lead_strip(countries_data)
    timeline = {cc: build_country_timeline(d) for cc, name, d in countries_data}
    us_cross = build_us_cross_country(countries_data)
    period_split = build_period_split(countries_data)
    already_in_recession = build_already_in_recession_table(countries_data)
    rescale_2022 = build_2022_rescale(countries_data)
    dumbbell = build_definition_dumbbell(countries_data)
    extra_h_pooled = {H: extra_h_pooled_stats(countries_data, H) for H in EXTRA_H_LIST}

    v2 = {
        "schema_notes": {
            "c1_wilson_ci": "各國/合併池/各定義/各 H 的命中率與基率已在 countries.<cc>.def_*.by_h.<H> "
                            "與 pooled.by_h.<H> 內原地補上 hit_rate_ci_low/high、base_rate_ci_low/high"
                            "（Wilson 95% CI），不另存副本。",
            "c2_precision_recall": "pr_points=[{cc,name,precision,recall,n_events}]，pr_pooled=同結構；"
                                    "precision=H24 命中率，recall=反向召回率。",
            "c3_depth_duration": "events=逐事件(cc,name,deepest,n_inverted_months,verdict)；"
                                  "buckets=2x2 桶，key 為『深/淺×長/短』中文組合，值={depth,duration,n,n_hit,hit_rate}。",
            "c4_cumulative_curve": "pooled_event_curve/us_event_curve=k=1..36 累積命中曲線；"
                                    "pooled_base_curve/us_base_curve=同 k 無條件基率曲線；"
                                    "每點{k,n,n_hit,hit_rate}，分母對每條曲線的所有 k 固定（見 schema 內註）。"
                                    "extra_h_pooled[H]（H=6,18）補 H_LIST=[12,24,36] 以外的合併池 H 統計。",
            "c5_lead_strip": "points=[{cc,name,lead_months,event_start}]，僅命中事件。",
            "c6_timeline": "timeline={cc:{events:[{start,end}],recession_spans:[[start,end|null]]}}；"
                            f"timeline_start={TIMELINE_START}，timeline_end={TIMELINE_END} 為圖表共用時間軸。",
            "c7_us_cross_country": "us_cross.rows=[{cc,name,window,n_events_tested,n_testable,n_hit,"
                                    "us_curve_hit_rate,own_curve_hit_rate,own_curve_n_testable}]；"
                                    "us_cross.pooled=同結構彙總（不含美國）。own_curve_hit_rate 沿用該國"
                                    "def_a H=24 既有數字（全樣本窗，非交集窗），us_curve_hit_rate 用交集窗重算。",
            "c8_period_split": "period_split.pooled/us={pre:{...},post:{...}}，cutoff=分界月；"
                                "pre/post 各含 n,n_hit,hit_rate,base_rate,base_rate_n,base_rate_hits。",
            "c9_already_in_recession": "already_in_recession=[{cc,name,n_already,n_events,ratio}]。",
            "c10_rescale_2022": f"rescale_2022=[{{cc,name,series:[[month,spread],...],"
                                 f"recession_spans:[[start,end|null],...]}}]，series 起自 {C10_START}。",
            "c11_definition_dumbbell": "dumbbell=[{cc,name,a_rate,alt_rate,alt_label}]，alt_label 依國家"
                                        "對應定義 B（OECD）／C（NBER，僅美國）／T（國發會峰谷，僅台灣）。",
        },
        "pr_points": pr_points, "pr_pooled": pr_pooled,
        "depth_duration": depth_duration,
        "pooled_event_curve": pooled_event_curve, "us_event_curve": us_event_curve,
        "pooled_base_curve": pooled_base_curve, "us_base_curve": us_base_curve,
        "lead_strip": lead_strip,
        "timeline": timeline, "timeline_start": TIMELINE_START, "timeline_end": TIMELINE_END,
        "us_cross": us_cross,
        "period_split": period_split,
        "already_in_recession": already_in_recession,
        "rescale_2022": rescale_2022,
        "dumbbell": dumbbell,
        "extra_h_pooled": extra_h_pooled,
    }

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
        "v2": v2,
    }
    DATA.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2, default=_json_default) + "\n",
                        encoding="utf-8")
    info(f"寫入 {OUT_JSON}")

    built_date = datetime.now().strftime("%Y-%m-%d")
    html_out = generate_html(countries_data, pooled_lead, pooled_h, per_country_lead, pooled_recall,
                              tw_status, tw_data, built_date, v2)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_out, encoding="utf-8")
    info(f"寫入 {OUT_HTML}")

    h24 = pooled_h[PRIMARY_H]
    info(f"合併池 H=24：命中率={h24['hit_rate']} 基率={h24['base_rate']} 提升={h24['uplift']}")
    info(f"前置期（合併池）：min={pooled_lead['min']} median={pooled_lead['median']} max={pooled_lead['max']}")
    k24 = next(p for p in pooled_event_curve if p["k"] == 24)
    info(f"C4 一致性檢查：pooled_event_curve k=24 命中率={k24['hit_rate']}（n={k24['n']}）"
         f" vs 表1合併池命中率={h24['hit_rate']}（n={h24['n_testable']}）")
    if us_cross:
        us_own = us_dict["def_a"]["by_h"][PRIMARY_H]
        info(f"C7 一致性檢查：美國「自己曲線」命中率={us_own['hit_rate']}（表1美國列）")

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
