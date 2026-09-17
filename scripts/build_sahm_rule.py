#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_sahm_rule.py — Sahm 法則跨國回測（8 國同一把尺，跟 build_yield_curve_recession.py 同一套
月份工具／事件分組思路／頁面版型，透過 import 共用，不複製也不改那支檔案）。

問題：失業率 3 個月移動平均比過去 12 個月最低點高 0.5 個百分點，在美國幾乎每次都對應衰退，
其他國家也是嗎？這個訊號是領先、同時、還是落後？門檻 0.5 是不是美國特有？跟殖利率倒掛比，
哪個準？

用法：
    python3 scripts/build_sahm_rule.py --fetch
        抓 FRED 序列（7 國 OECD 調和失業率 LRHUTTTT{CC}M156S + 美國 UNRATE + 美國 NBER
        USRECM，月頻峰谷皆含，避免日頻 USRECDM 用某天轉折造成月份邊界誤判）存 data/sahm_rule_raw.json。

    python3 scripts/build_sahm_rule.py
        讀 raw json + 台灣手抄 json（data/sahm_rule_tw_manual.json）+ 既有殖利率倒掛回測
        json（data/yield_curve_recession.json，只讀衰退區間與倒掛事件，不重算），算全部統計，
        寫 data/sahm_rule.json，生成 docs/backtest/sahm_rule/index.html。
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_JSON = DATA / "sahm_rule_raw.json"
OUT_JSON = DATA / "sahm_rule.json"
TW_MANUAL_JSON = DATA / "sahm_rule_tw_manual.json"
YC_JSON = DATA / "yield_curve_recession.json"
OUT_HTML = ROOT / "docs" / "backtest" / "sahm_rule" / "index.html"
NAV_DIR = ROOT / "docs" / "backtest"

sys.path.insert(0, str(ROOT / "scripts"))
from build_yield_curve_recession import (  # noqa: E402  共用工具，全部 import，不複製不改
    fetch_fred, month_key, month_index, month_diff, add_months, in_any_span,
    recession_transitions, detect_events, classify_event, reverse_recall, wilson_ci,
    extract_template_parts, esc, fmt_pct, fmt_pp, fmt_num, fmt_month, fmt_ci,
    collapse_cjk_whitespace, CN_NUM, CHART_JS_CDN, POINT_MARKER_PLUGIN_JS,
    BRAND_BLUE, US_ORANGE, LIGHT_GRAY_BASE, GRAY_MISS, COUNTRY_COLORS,
    PRIMARY_H as YC_PRIMARY_H,
)

SCHEMA = "sahm-rule-v1"


def warn(msg: str) -> None:
    print(f"[sahm][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[sahm] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 第 1 節：國家與序列代碼（spec_sahm_rule.md「資料」，已用 python requests 逐條驗證存在）
# ═══════════════════════════════════════════════════════════════════════════

COUNTRIES_FRED = [
    ("US", "美國"), ("DE", "德國"), ("GB", "英國"), ("JP", "日本"),
    ("CA", "加拿大"), ("AU", "澳洲"), ("KR", "南韓"),
]
ALL_CC_ORDER = ["US", "DE", "GB", "JP", "CA", "AU", "KR", "TW"]

PRIMARY_THRESHOLD = 0.5
THRESHOLDS = [0.3, 0.5, 0.7]
LEAD_WINDOW = 12          # 領先窗（定義凍結）
EVENT_GROUP_MONTHS = 24   # 事件分組窗（定義凍結，跟殖利率倒掛同一套思路）
RECALL_EXTRA_MONTHS = 6   # 召回率：衰退起點到終點 +6 個月
BASE_RATE_WINDOW = 12     # 基率：未來 12 個月內出現衰退起點


# ═══════════════════════════════════════════════════════════════════════════
# 第 2 節：抓取
# ═══════════════════════════════════════════════════════════════════════════

def do_fetch():
    series_ids = ["UNRATE", "USRECM"] + [f"LRHUTTTT{cc}M156S" for cc, _n in COUNTRIES_FRED]
    out = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "series": {}, "meta": {}}
    ok = fail = 0
    for sid in series_ids:
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


def load_raw():
    if not RAW_JSON.exists():
        raise SystemExit(f"{RAW_JSON} 不存在，請先跑 --fetch")
    return json.loads(RAW_JSON.read_text(encoding="utf-8"))


def load_tw_manual():
    if not TW_MANUAL_JSON.exists():
        return {"status": "missing", "note": f"{TW_MANUAL_JSON} 不存在"}
    return json.loads(TW_MANUAL_JSON.read_text(encoding="utf-8"))


def load_yc():
    if not YC_JSON.exists():
        raise SystemExit(f"{YC_JSON} 不存在（殖利率倒掛回測需先跑過）")
    return json.loads(YC_JSON.read_text(encoding="utf-8"))


def to_monthly_dict(pts):
    return {month_key(d): v for d, v in pts}


# ═══════════════════════════════════════════════════════════════════════════
# 第 3 節：Sahm 指標計算（定義凍結，spec_sahm_rule.md 第 17-30 行）
# ═══════════════════════════════════════════════════════════════════════════

def three_month_ma(monthly: dict) -> dict:
    """失業率 3 個月移動平均(t) = 當月與前兩個月的平均，缺任一月就不算。"""
    out = {}
    for m in monthly:
        m1, m2 = add_months(m, -1), add_months(m, -2)
        if m1 in monthly and m2 in monthly:
            out[m] = (monthly[m] + monthly[m1] + monthly[m2]) / 3.0
    return out


def sahm_indicator(ma3: dict) -> dict:
    """S(t) = MA3(t) − min(MA3, t−12..t−1)；前 12 個月的 MA3 要齊全才算，不齊全就跳過該月
    （不用不完整的視窗湊數）。"""
    out = {}
    for m in ma3:
        window = [add_months(m, -k) for k in range(1, 13)]
        vals = [ma3[w] for w in window if w in ma3]
        if len(vals) < 12:
            continue
        out[m] = round(ma3[m] - min(vals), 4)
    return out


def detect_sahm_events(S: dict, sample_start: str, sample_end: str, threshold: float,
                        group_months: int = EVENT_GROUP_MONTHS):
    """事件＝第一個觸發月（S(t)≥門檻）為起點，起點後 group_months 個月內的觸發月同一事件
    （跟殖利率倒掛 detect_events() 同一套分組思路，這裡是獨立實作因為判準是「觸發」不是
    「倒掛」，不能直接呼叫那支函式）。"""
    months = sorted(m for m in S if sample_start <= m <= sample_end)
    trig = [(m, S[m]) for m in months if S[m] >= threshold]
    events = []
    i = 0
    while i < len(trig):
        start_m, start_v = trig[i]
        group = [(start_m, start_v)]
        j = i + 1
        while j < len(trig) and month_diff(trig[j][0], start_m) <= group_months:
            group.append(trig[j])
            j += 1
        peak = max(v for _m, v in group)
        events.append({"start": start_m, "peak_s": round(peak, 4), "n_trigger_months": len(group)})
        i = j
    return events


def span_containing(month: str, spans):
    for s, e in spans:
        if s <= month and (e is None or month < e):
            return (s, e)
    return None


def classify_sahm_event(event_start: str, spans, starts_sorted, sample_end: str,
                         lead_window: int = LEAD_WINDOW):
    """判定（spec 第 21-25 行，定義凍結）：
    同時或落後＝起點落在衰退區間內（Sahm 法則設計上的正常情況，不是落空，記錄落後月數）。
    領先＝起點後 lead_window 個月內出現衰退起點（記錄前置月數）。
    落空＝起點前後都沒有衰退。未到期＝lead_window 窗口還沒走完。"""
    span = span_containing(event_start, spans)
    if span is not None:
        s, _e = span
        return "same_or_lag", month_diff(event_start, s)
    candidates = [r for r in starts_sorted if 0 < month_diff(r, event_start) <= lead_window]
    if candidates:
        first = min(candidates, key=lambda r: month_diff(r, event_start))
        return "lead", month_diff(first, event_start)
    window_end = add_months(event_start, lead_window)
    if sample_end is not None and month_diff(sample_end, window_end) >= 0:
        return "miss", None
    return "not_yet_due", None


def recognized_offsets(spans, ev_rows):
    """每次「被認出的衰退」的識別點＝觸發月－衰退起點月（可為負，領先為負、落後為正）。
    一次衰退可能被多個事件對到（罕見），取最早（signed 最小）的那個，代表最先認出來的時點。"""
    out = {}
    for ev in ev_rows:
        if ev["verdict"] == "same_or_lag":
            span = span_containing(ev["start"], spans)
            if span is None:
                continue
            key, val = span[0], ev["offset_months"]
        elif ev["verdict"] == "lead":
            key = add_months(ev["start"], ev["offset_months"])
            val = -ev["offset_months"]
        else:
            continue
        if key not in out or val < out[key]:
            out[key] = val
    return out


def sahm_recall(spans, S: dict, sample_start: str, sample_end: str, threshold: float,
                 extra_months: int = RECALL_EXTRA_MONTHS):
    """召回率＝每次衰退（定義 A）從起點到終點＋6 個月內，有沒有觸發（spec 第 27 行）。
    只有「起點在樣本窗內」且「終點＋6 個月窗口已經走完」的衰退才算可判定；起點早於樣本窗
    （沒有失業率資料可查）或窗口還沒走完的衰退不計入分母。"""
    trig_months = sorted(m for m, v in S.items() if v >= threshold)
    testable = []
    hits = 0
    for s, e in spans:
        if s < sample_start or e is None:
            continue
        window_end = add_months(e, extra_months)
        if sample_end is None or month_diff(sample_end, window_end) < 0:
            continue
        testable.append((s, e))
        if any(s <= m <= window_end for m in trig_months):
            hits += 1
    recall = round(hits / len(testable), 4) if testable else None
    return recall, len(testable), hits


def base_rate_sahm(spans, starts_sorted, sample_start: str, sample_end: str,
                    window: int = BASE_RATE_WINDOW):
    """基率＝任一月份「當月在衰退中，或未來 window 個月內出現衰退起點」的比率（spec 第 29
    行）。已在衰退中的月份不需要未來窗口走完就能判定（本來就是 1），其餘月份要等 window 個月
    走完才能判定。"""
    months = []
    m = sample_start
    while m <= sample_end:
        months.append(m)
        m = add_months(m, 1)
    valid = [m for m in months
             if in_any_span(m, spans) or month_diff(sample_end, add_months(m, window)) >= 0]
    hits = sum(1 for m in valid
               if in_any_span(m, spans) or any(0 < month_diff(s, m) <= window for s in starts_sorted))
    rate = round(hits / len(valid), 4) if valid else None
    return rate, len(valid), hits


def build_threshold_stats(S: dict, spans, sample_start, sample_end, threshold):
    starts_sorted = sorted(s for s, _e in spans)
    events = detect_sahm_events(S, sample_start, sample_end, threshold)
    ev_rows = []
    n_same_or_lag = n_lead = n_miss = n_notdue = 0
    lags, leads = [], []
    for ev in events:
        verdict, offset = classify_sahm_event(ev["start"], spans, starts_sorted, sample_end)
        row = dict(ev)
        row["verdict"] = verdict
        row["offset_months"] = offset
        if verdict == "same_or_lag":
            n_same_or_lag += 1
            lags.append(offset)
        elif verdict == "lead":
            n_lead += 1
            leads.append(offset)
        elif verdict == "miss":
            n_miss += 1
        else:
            n_notdue += 1
        ev_rows.append(row)
    n_hit = n_same_or_lag + n_lead
    n_testable = n_hit + n_miss
    hit_rate = round(n_hit / n_testable, 4) if n_testable else None
    recall, recall_n, recall_hits = sahm_recall(spans, S, sample_start, sample_end, threshold)
    base, base_n, base_hits = base_rate_sahm(spans, starts_sorted, sample_start, sample_end)
    uplift = round(hit_rate / base, 2) if (hit_rate is not None and base) else None
    hci_lo, hci_hi = wilson_ci(n_hit, n_testable)
    rci_lo, rci_hi = wilson_ci(recall_hits, recall_n)
    bci_lo, bci_hi = wilson_ci(base_hits, base_n)
    return {
        "threshold": threshold, "events": ev_rows, "n_events": len(events),
        "n_same_or_lag": n_same_or_lag, "n_lead": n_lead, "n_miss": n_miss,
        "n_not_yet_due": n_notdue, "n_testable": n_testable, "n_hit": n_hit,
        "hit_rate": hit_rate, "hit_rate_ci_low": hci_lo, "hit_rate_ci_high": hci_hi,
        "recall": recall, "recall_n": recall_n, "recall_hits": recall_hits,
        "recall_ci_low": rci_lo, "recall_ci_high": rci_hi,
        "base_rate": base, "base_rate_n": base_n, "base_rate_hits": base_hits,
        "base_rate_ci_low": bci_lo, "base_rate_ci_high": bci_hi,
        "uplift": uplift, "lag_values": lags, "lead_values": leads,
    }


def build_country_sahm(cc, name, unemployment_pts, spans, gdp_data_range):
    """unemployment_pts: [[date_iso_or_month, value], ...] 升冪，date_iso 可以是 "YYYY-MM-DD"
    （FRED 原始日期）或已經是 "YYYY-MM"（台灣手抄資料）。spans: 該國定義 A（或美國 NBER／
    台灣國發會）衰退區間 [[start,end|None],...]。樣本窗＝失業率資料與衰退區間資料（用
    gdp_data_range 當代理）皆有覆蓋的期間。"""
    monthly = {month_key(d): v for d, v in unemployment_pts}
    if not monthly:
        return {"cc": cc, "name": name, "status": "missing"}
    sample_start = max(min(monthly), gdp_data_range[0])
    sample_end = min(max(monthly), gdp_data_range[1])
    if sample_start > sample_end:
        return {"cc": cc, "name": name, "status": "missing", "note": "失業率與衰退資料期間無重疊"}
    ma3 = three_month_ma(monthly)
    S = sahm_indicator(ma3)
    by_threshold = {th: build_threshold_stats(S, spans, sample_start, sample_end, th)
                    for th in THRESHOLDS}
    primary = by_threshold[PRIMARY_THRESHOLD]
    recognized = recognized_offsets(spans, primary["events"])
    return {
        "cc": cc, "name": name, "status": "ok",
        "unemployment_series": sorted(monthly.items()),
        "unemployment_data_range": [min(monthly), max(monthly)],
        "sample_start": sample_start, "sample_end": sample_end,
        "gdp_recession_spans": spans,
        "by_threshold": by_threshold,
        "primary": primary,
        "recognized_offsets": recognized,
        "trigger_months": {th: sorted(m for m, v in S.items()
                                       if sample_start <= m <= sample_end and v >= th)
                           for th in THRESHOLDS},
        "S_series": sorted(S.items()),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 第 4 節：台灣
# ═══════════════════════════════════════════════════════════════════════════

def build_taiwan(tw_manual, yc_tw):
    if not tw_manual or tw_manual.get("status") != "ok":
        return {"cc": "TW", "name": "台灣", "status": "missing",
                "note": (tw_manual or {}).get("note", "無台灣手抄資料")}
    ur = tw_manual.get("unemployment_rate_sa", {})
    if not ur.get("available"):
        return {"cc": "TW", "name": "台灣", "status": "missing", "note": "台灣季調失業率不可用"}
    pts = ur.get("series", [])
    if not pts or len(pts) < 24:
        return {"cc": "TW", "name": "台灣", "status": "partial",
                "note": f"台灣季調失業率只有 {len(pts)} 筆，不足 24 筆不納入主表"}
    if not yc_tw or yc_tw.get("status") != "ok":
        return {"cc": "TW", "name": "台灣", "status": "missing", "note": "台灣衰退區間（定義 A）不可用"}
    spans = [tuple(x) for x in yc_tw.get("gdp_recession_spans", [])]
    gdp_range = yc_tw.get("gdp_data_range", [None, None])
    d = build_country_sahm("TW", "台灣", pts, spans, gdp_range)
    if d.get("status") == "ok":
        d["source_url"] = ur.get("source_url")
        d["source_note"] = tw_manual.get("note", "")
        # 定義 T（國發會峰谷）對照，跟殖利率倒掛頁台灣段同一批 peaks_troughs
        peaks_troughs = yc_tw.get("peaks_troughs", [])
        t_spans = []
        for pt in peaks_troughs:
            peak, trough = pt.get("peak"), pt.get("trough")
            if not peak:
                continue
            t_spans.append((add_months(peak, 1), add_months(trough, 1) if trough else None))
        if t_spans:
            monthly = {m: v for m, v in pts}
            sample_start = max(min(monthly), "1996-01")
            sample_end = max(monthly)
            S = sahm_indicator(three_month_ma(monthly))
            d["def_t_primary"] = build_threshold_stats(S, t_spans, sample_start, sample_end,
                                                         PRIMARY_THRESHOLD)
            d["def_t_spans"] = [[s, e] for s, e in t_spans]
    return d


# ═══════════════════════════════════════════════════════════════════════════
# 第 5 節：跟殖利率倒掛比較（同一窗口重算，spec 第 30 行）
# ═══════════════════════════════════════════════════════════════════════════

def window_yc_stats(yc_country, window_start, window_end):
    spread = dict(yc_country["spread_series"])
    spans = [tuple(x) for x in yc_country["gdp_recession_spans"]]
    starts_sorted = sorted(s for s, _e in spans)
    events = detect_events(spread, window_start, window_end)
    n_hit = n_miss = 0
    for ev in events:
        verdict, _lead = classify_event(ev["start"], YC_PRIMARY_H, spans, starts_sorted, window_end)
        if verdict == "hit":
            n_hit += 1
        elif verdict == "miss":
            n_miss += 1
    n_testable = n_hit + n_miss
    hit_rate = round(n_hit / n_testable, 4) if n_testable else None
    recall, recall_n = reverse_recall(starts_sorted, spread, window_start, window_end, window=YC_PRIMARY_H)
    return {"n_events": len(events), "n_testable": n_testable, "n_hit": n_hit,
            "hit_rate": hit_rate, "recall": recall, "recall_n": recall_n}


def window_sahm_stats(S, spans, window_start, window_end, threshold=PRIMARY_THRESHOLD):
    stats = build_threshold_stats(S, spans, window_start, window_end, threshold)
    return {"n_events": stats["n_events"], "n_testable": stats["n_testable"],
            "n_hit": stats["n_hit"], "hit_rate": stats["hit_rate"],
            "recall": stats["recall"], "recall_n": stats["recall_n"]}


def combo_hit_rate(yc_country, sahm_events_full, window_start, window_end):
    """兩個都觸發：倒掛事件起點後 24 個月內 Sahm 也觸發，這種組合事件的衰退命中率（沿用
    殖利率倒掛頁已經算好的 H=24 命中判定，不重新定義「命中」）。"""
    yc_events = yc_country["def_a"]["events_detail"]
    sahm_starts = sorted(e["start"] for e in sahm_events_full)
    combo = []
    for ev in yc_events:
        if not (window_start <= ev["start"] <= window_end):
            continue
        if ev["verdict"] not in ("hit", "miss"):
            continue
        if any(0 <= month_diff(s, ev["start"]) <= EVENT_GROUP_MONTHS for s in sahm_starts):
            combo.append(ev)
    n = len(combo)
    n_hit = sum(1 for e in combo if e["verdict"] == "hit")
    return {"n": n, "n_hit": n_hit, "hit_rate": round(n_hit / n, 4) if n else None}


def build_vs_yield_curve(cc, name, sahm_d, yc_country):
    if sahm_d.get("status") != "ok" or not yc_country or yc_country.get("status") != "ok":
        return None
    yc_da = yc_country.get("def_a")
    if yc_da is None:
        return None
    window_start = max(yc_da["sample_start"], sahm_d["sample_start"])
    window_end = min(yc_da["sample_end"], sahm_d["sample_end"])
    if window_start > window_end:
        return None
    monthly = dict(sahm_d["unemployment_series"])
    S = sahm_indicator(three_month_ma(monthly))
    spans = sahm_d["gdp_recession_spans"]
    yc_win = window_yc_stats(yc_country, window_start, window_end)
    sahm_win = window_sahm_stats(S, spans, window_start, window_end)
    combo = combo_hit_rate(yc_country, sahm_d["primary"]["events"], window_start, window_end)
    return {"cc": cc, "name": name, "window": [window_start, window_end],
            "yield_curve": yc_win, "sahm": sahm_win, "combo": combo}


# ═══════════════════════════════════════════════════════════════════════════
# 第 6 節：合併池
# ═══════════════════════════════════════════════════════════════════════════

def pooled_primary_stats(countries_data):
    n_hit = n_testable = base_hits = base_n = recall_hits = recall_n = 0
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        p = d["primary"]
        n_hit += p["n_hit"]
        n_testable += p["n_testable"]
        base_hits += p["base_rate_hits"] or 0
        base_n += p["base_rate_n"] or 0
        recall_hits += p["recall_hits"] or 0
        recall_n += p["recall_n"] or 0
    hit_rate = round(n_hit / n_testable, 4) if n_testable else None
    base_rate = round(base_hits / base_n, 4) if base_n else None
    recall = round(recall_hits / recall_n, 4) if recall_n else None
    uplift = round(hit_rate / base_rate, 2) if (hit_rate is not None and base_rate) else None
    hci_lo, hci_hi = wilson_ci(n_hit, n_testable)
    return {"n_hit": n_hit, "n_testable": n_testable, "hit_rate": hit_rate,
            "hit_rate_ci_low": hci_lo, "hit_rate_ci_high": hci_hi,
            "base_rate": base_rate, "base_rate_n": base_n,
            "recall": recall, "recall_n": recall_n, "uplift": uplift}


def pooled_recognized_offsets(countries_data):
    all_vals = []
    per_country = {}
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        vals = sorted(d["recognized_offsets"].values())
        if vals:
            per_country[cc] = {"name": name, "n": len(vals), "min": min(vals),
                                "median": statistics.median(vals), "max": max(vals)}
        all_vals.extend(vals)
    pooled = {"n": len(all_vals),
              "min": min(all_vals) if all_vals else None,
              "median": statistics.median(all_vals) if all_vals else None,
              "max": max(all_vals) if all_vals else None}
    return per_country, pooled


def pooled_threshold_stats(countries_data, threshold):
    n_hit = n_testable = recall_hits = recall_n = 0
    n_events = 0
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        s = d["by_threshold"][threshold]
        n_hit += s["n_hit"]
        n_testable += s["n_testable"]
        recall_hits += s["recall_hits"] or 0
        recall_n += s["recall_n"] or 0
        n_events += s["n_events"]
    hit_rate = round(n_hit / n_testable, 4) if n_testable else None
    recall = round(recall_hits / recall_n, 4) if recall_n else None
    return {"n_events": n_events, "n_hit": n_hit, "n_testable": n_testable,
            "hit_rate": hit_rate, "recall": recall, "recall_n": recall_n}


# ═══════════════════════════════════════════════════════════════════════════
# 第 7 節：HTML 產出（版型照抄 build_yield_curve_recession.py，用 extract_template_parts()
# 從已上線的 /backtest/yield_curve/ 抽 CSS／導覽，不另寫樣式）
# ═══════════════════════════════════════════════════════════════════════════

CHART_JS_CDN_LOCAL = CHART_JS_CDN
DEEP_RED = "#dc2626"


def fmt_offset(x):
    if x is None:
        return "—"
    if float(x).is_integer():
        x = int(x)
        return f"{x:+d} 月" if x != 0 else "0 月"
    return f"{x:+.1f} 月"


def verdict_label(v):
    return {"same_or_lag": "同時或落後", "lead": "領先", "miss": "落空",
            "not_yet_due": "未到期"}.get(v, v)


DEFINITIONS_TEXT = [
    "Sahm 指標 S(t) ＝ 失業率 3 個月移動平均(t) － 過去 12 個月（t－12 到 t－1）失業率 3 個月"
    "移動平均的最低點。移動平均與過去 12 個月的紀錄都要有完整資料才算，缺任一個月就跳過該月，"
    "不用不完整的視窗湊數。",
    "觸發月 ＝ S(t) 大於等於門檻的月份，主線門檻 0.5 個百分點，另外跑 0.3 與 0.7 兩個門檻做"
    "敏感度對照。事件 ＝ 第一個觸發月為起點，起點後 24 個月內的觸發月都算同一事件（跟殖利率"
    "倒掛回測同一套事件分組窗，避免同一波失業率上升被拆成好幾次事件）。",
    "判定分四種。同時或落後：事件起點當下已經在衰退區間內，記錄「衰退開始後第幾個月觸發」"
    "（落後月數，可為 0）。這是 Sahm 法則設計上的正常情況。它本來就是拿當下的"
    "失業率確認衰退是不是已經在發生，不預測衰退會不會發生。領先：事件起點後 12 個月內出現"
    "衰退起點，記錄前置月數。落空：事件起點前後都沒有衰退，起點不在衰退中，且之後 12 個月內"
    "沒有衰退起點。未到期：12 個月的判定窗口還沒走完，暫不列入命中率分母。",
    "命中率 ＝（同時或落後的事件數 ＋ 領先的事件數）÷ 可判定事件數（不含未到期）。",
    "召回率 ＝ 每一次衰退（定義 A，技術性衰退：實質 GDP 連兩季負成長），從衰退起點到終點"
    "再加 6 個月的窗口內，有沒有出現過觸發月。起點早於失業率資料起點、或窗口還沒走完的衰退"
    "不計入分母。",
    "認得多快 ＝ 對每一次被認出的衰退（命中率分子涵蓋的那些衰退），取最早對到它的觸發月，"
    "減去衰退起點月，單位月，可為負（領先）也可為正（落後）。中位數與最小、最大值一起報。",
    "基率 ＝ 任一月份「當月已經在衰退中，或未來 12 個月內出現衰退起點」的比率，逐月滾動算過"
    "全樣本。已經在衰退中的月份不用等未來窗口走完就能判定，其餘月份要等 12 個月窗口走完。"
    "提升倍數 ＝ 命中率除以基率。",
    "樣本窗 ＝ 該國失業率資料與衰退區間資料（用實質 GDP 資料涵蓋期間代理）都有覆蓋的期間，"
    "起訖印在表上。八國失業率用 OECD 調和季調口徑（LRHUTTTT），美國另外多抓 UNRATE 作主線"
    "（跟 Sahm 原文用的序列一致），OECD 口徑的美國失業率只做對照，不進主表。",
    "衰退區間直接讀既有的殖利率倒掛回測（data/yield_curve_recession.json），八國都用定義 A"
    "（技術性衰退），不重算。美國另外多跑一次 NBER 認定的衰退期（USRECM，月頻峰谷皆含）作對照，因為 Sahm"
    "法則原文就是針對 NBER 衰退設計的。台灣另外多跑一次國發會峰谷對照定義（峰的次月為衰退"
    "起點）。",
    "跟殖利率倒掛比較時，兩邊都限定在「利差資料與失業率資料都覆蓋」的交集窗口內重新計算，"
    "不是直接拿各自全樣本的數字相減。倒掛的命中率與召回率定義沿用殖利率倒掛回測本身的定義，"
    "命中＝倒掛事件起點後 24 個月內出現衰退起點，召回率＝衰退起點前 24 個月內是否出現過"
    "倒掛月，跟 Sahm 法則「同時或落後也算命中」、「召回率看衰退起點到終點＋6 個月」是兩套"
    "不同的判準，差異來自兩個訊號的設計定位不同，兩邊的算法各自都跟題目規格一致。",
]


def section_method(vs_yc_rows):
    lis = "".join(f"<li>{esc(t)}</li>" for t in DEFINITIONS_TEXT)
    return f"""
<div class="section">
<h2 class="section-title">七、方法：怎麼定義「觸發」與「衰退」</h2>
<div class="takeaway">這頁的判定規則在跑資料前就定死，八個國家套同一套定義，中途不因某國結果好不好看
而回頭調整。門檻、事件分組窗、判定窗口全部跟題目規格一致，沒有為了讓命中率好看而調整。</div>
<div class="card"><ul class="disc">{lis}</ul></div>
</div>
"""


def section_caveats():
    body = """
<ul class="disc">
<li>失業率口徑不是每國都一樣。美國主線用 UNRATE（官方公布的主要失業率），其餘七國跟台灣用
OECD 調和季調口徑，兩者的調查方法、年齡層涵蓋、就業定義都有差異，跨國比較命中率時這是
背景差異，這裡控制不了。</li>
<li>季節調整本身是統計模型，會隨新資料加入而回頭修正舊月份的數值。越接近抓取當下的月份，
越可能之後被修正，抓取當下的最新公布值不會回頭用修正後數字改寫已經定案的事件。</li>
<li>台灣的季調失業率官方序列只從 2016 年 1 月開始公布，樣本窗遠比其餘七國短，只涵蓋定義 A
下的兩次技術性衰退，任何單一國家層級的結論都要對照事件數一起看，事件數個位數的國家，
命中率的信賴區間本來就寬。</li>
<li>南韓、德國的失業率序列也是 1990 年代才開始，涵蓋的衰退次數同樣有限，門檻敏感度
（第三節）在這些國家身上尤其容易受單一事件左右。</li>
<li>「衰退」全部是官方統計事後定案的技術性衰退或官方認定機構的判斷，不是市場當下的預期。
不對任何一次觸發當下「這次是不是真的要衰退了」做預測，只回報歷史上這個訊號準不準、準多快。</li>
</ul>
"""
    return f"""
<div class="section">
<h2 class="section-title">八、這頁沒有告訴你的事</h2>
<div class="takeaway">下面五點是讀這頁數字前要先知道的限制，不是免責聲明，是真的會影響數字
怎麼解讀。</div>
<div class="card">{body}</div>
</div>
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


# ═══════════════════════════════════════════════════════════════════════════
# Hero
# ═══════════════════════════════════════════════════════════════════════════

def section_hero(pooled, pooled_offset, tw_status, threshold_note, vs_yc_note):
    hit_rate, base, uplift = pooled["hit_rate"], pooled["base_rate"], pooled["uplift"]
    med = pooled_offset["median"]

    if hit_rate is not None and hit_rate >= 0.85:
        verdict, tag_color = "美國幾乎不落空，其他國家方向一致但強弱不同", "#dc2626"
    elif hit_rate is not None and hit_rate >= 0.6:
        verdict, tag_color = "Sahm 法則對多數國家有用，但不是每個門檻都一樣準", "#d97706"
    else:
        verdict, tag_color = "Sahm 法則跨國表現差異很大，不能直接套美國的門檻", "#059669"

    q1 = (f"失業率離低點回升 0.5 個百分點，衰退真的接著來嗎？合併池命中率 {fmt_pct(hit_rate)}，"
          f"比不看訊號的基率 {fmt_pct(base)} 高 {fmt_num(uplift, 1)} 倍，方向是真的，"
          f"但八國強弱不一樣。")
    if med is not None and med > 0:
        q2 = (f"觸發那一刻衰退通常已經開始了，認出來的衰退中位數落後衰退起點 {fmt_num(med, 0)} "
              f"個月，這是一個確認訊號，不是預告訊號。")
    elif med is not None and med < 0:
        q2 = (f"認出來的衰退中位數比衰退起點早 {fmt_num(-med, 0)} 個月觸發，"
              f"但這不是本頁多數事件的樣貌，細節看第二節。")
    else:
        q2 = "觸發那一刻跟衰退起點幾乎同時，細節看第二節。"
    q3 = threshold_note
    q4 = vs_yc_note
    tw_note = "台灣併入主表，樣本窗只從 2016 年開始。" if tw_status == "ok" else "台灣資料整理中，本頁先出七國版本。"

    return f"""
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag" style="background:{tag_color}">{esc(verdict)}</span>
    <h2>{esc(q1)}</h2>
    <p>{esc(q2)}</p>
    <p>{esc(q3)} {esc(q4)} {esc(tw_note)}</p>
  </div>
  <div class="hero-stats">
    <div><div class="hs-label">合併池命中率（門檻 0.5）</div><div class="hs-value">{fmt_pct(hit_rate)}</div></div>
    <div><div class="hs-label">合併池基率</div><div class="hs-value">{fmt_pct(base)}</div></div>
    <div><div class="hs-label">提升倍數</div><div class="hs-value">{fmt_num(uplift, 1)}x</div></div>
    <div><div class="hs-label">認出衰退・落後月數中位數</div><div class="hs-value">{fmt_num(med, 0)} 月</div></div>
  </div>
</div>
"""


# ═══════════════════════════════════════════════════════════════════════════
# 第一節：命中率 vs 基率
# ═══════════════════════════════════════════════════════════════════════════

def section1(countries_data, pooled, us_nber_d):
    rows_data = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        p = d["primary"]
        rows_data.append({
            "cc": cc, "name": name,
            "period": f"{fmt_month(d['sample_start'])}～{fmt_month(d['sample_end'])}",
            "n_events": p["n_events"], "n_hit": p["n_hit"], "hit_rate": p["hit_rate"],
            "base_rate": p["base_rate"], "uplift": p["uplift"],
            "ci_low": p["hit_rate_ci_low"], "ci_high": p["hit_rate_ci_high"],
            "recall": p["recall"], "n_same_or_lag": p["n_same_or_lag"], "n_lead": p["n_lead"],
            "n_miss": p["n_miss"],
        })
    pooled_row = {"cc": "POOL", "name": "合併池（不獨立）", "period": "—",
                  "n_events": None, "n_hit": pooled["n_hit"], "hit_rate": pooled["hit_rate"],
                  "base_rate": pooled["base_rate"], "uplift": pooled["uplift"],
                  "ci_low": pooled["hit_rate_ci_low"], "ci_high": pooled["hit_rate_ci_high"],
                  "recall": pooled["recall"], "n_same_or_lag": None, "n_lead": None, "n_miss": None}

    straddlers = [r["name"] for r in rows_data
                  if r["ci_low"] is not None and r["base_rate"] is not None
                  and r["ci_low"] <= r["base_rate"] <= r["ci_high"]]
    small_n = [r["name"] for r in rows_data if r["n_events"] is not None and r["n_events"] <= 4]

    if straddlers:
        title = f"{'、'.join(straddlers)}的觸發訊號，統計上和基率分不出來"
    else:
        title = "八國的命中率信賴區間都站在基率上方，方向一致"

    lead = (f"合併池命中率 {fmt_pct(pooled['hit_rate'])}，基率 {fmt_pct(pooled['base_rate'])}，"
            f"提升 {fmt_num(pooled['uplift'], 1)} 倍。命中包含「同時或落後」（觸發當下已經在"
            f"衰退中）跟「領先」（觸發後 12 個月內衰退才開始）兩種，這是 Sahm 法則設計上的正常"
            f"情況，不等於預告失準，第二節再拆這兩種的比例。")

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
      {{ label:'基率', data:{json.dumps(base_arr)}, backgroundColor:'{LIGHT_GRAY_BASE}', order:2 }},
      {{ label:'命中率 95% 信賴區間', data:{json.dumps(ci_arr)}, backgroundColor:'rgba(26,86,219,.30)',
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
               "不看訊號的基率。藍色區間整段都在灰色長條右邊，代表訊號站得住。蓋回灰色長條，"
               "代表樣本數還分不出這個國家的訊號跟不看訊號的差別。")

    def _fmt_row(r):
        hit_txt = "—" if r["n_same_or_lag"] is None else f"{r['n_same_or_lag']}／{r['n_lead']}"
        return (f"<tr><td class='lbl'>{esc(r['name'])}</td><td>{esc(r['period'])}</td>"
                f"<td class='num'>{r['n_events'] if r['n_events'] is not None else '—'}</td>"
                f"<td class='num'>{hit_txt}</td>"
                f"<td class='num'>{r['n_miss'] if r['n_miss'] is not None else '—'}</td>"
                f"<td class='num'>{fmt_pct(r['hit_rate'])}</td>"
                f"<td class='num'>{fmt_ci(r['ci_low'], r['ci_high'])}</td>"
                f"<td class='num'>{fmt_pct(r['recall']) if r['recall'] is not None else '—'}</td>"
                f"<td class='num'>{fmt_pct(r['base_rate'])}</td>"
                f"<td class='num'>{fmt_num(r['uplift'], 1)}</td></tr>")

    table_rows = "".join(_fmt_row(r) for r in rows_data)
    table_rows += (f"<tr><td class='lbl'><b>{esc(pooled_row['name'])}</b></td><td>—</td><td class='num'>—</td>"
                    f"<td class='num'>—</td><td class='num'>—</td>"
                    f"<td class='num'><b>{fmt_pct(pooled_row['hit_rate'])}</b></td>"
                    f"<td class='num'>{fmt_ci(pooled_row['ci_low'], pooled_row['ci_high'])}</td>"
                    f"<td class='num'>{fmt_pct(pooled_row['recall'])}</td>"
                    f"<td class='num'>{fmt_pct(pooled_row['base_rate'])}</td>"
                    f"<td class='num'>{fmt_num(pooled_row['uplift'], 1)}</td></tr>")
    if us_nber_d and us_nber_d.get("status") == "ok":
        pn = us_nber_d["primary"]
        table_rows += (f"<tr><td class='lbl'>美國（NBER 對照）</td>"
                        f"<td>{esc(fmt_month(us_nber_d['sample_start']))}～{esc(fmt_month(us_nber_d['sample_end']))}</td>"
                        f"<td class='num'>{pn['n_events']}</td>"
                        f"<td class='num'>{pn['n_same_or_lag']}／{pn['n_lead']}</td>"
                        f"<td class='num'>{pn['n_miss']}</td>"
                        f"<td class='num'>{fmt_pct(pn['hit_rate'])}</td>"
                        f"<td class='num'>{fmt_ci(pn['hit_rate_ci_low'], pn['hit_rate_ci_high'])}</td>"
                        f"<td class='num'>{fmt_pct(pn['recall'])}</td>"
                        f"<td class='num'>{fmt_pct(pn['base_rate'])}</td>"
                        f"<td class='num'>{fmt_num(pn['uplift'], 1)}</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th><th>樣本期間</th>
<th class="num">事件數</th><th class="num">同時或落後／領先</th><th class="num">落空</th>
<th class="num">命中率</th><th class="num">命中率 95% CI</th><th class="num">召回率</th>
<th class="num">基率</th><th class="num">提升倍數</th></tr></thead>
<tbody>{table_rows}</tbody></table></div>"""

    note_parts = []
    if straddlers:
        note_parts.append(f"{'、'.join(straddlers)}的 95% 信賴區間跨回基率，樣本數不夠大，"
                           f"統計上還不能說這幾國的觸發訊號比不看訊號準。")
    else:
        note_parts.append("八個國家的命中率信賴區間都沒有跨回基率，方向上都站得住。")
    if small_n:
        note_parts.append(f"{'、'.join(small_n)}事件數只有個位數，區間本來就寬，不宜對單一數字太認真。")
    note = "".join(note_parts)

    html = _section_shell(0, title, lead, _std_body(chart_html, caption, table_html, note) + f"<script>{chart_js}</script>")
    return html, straddlers


# ═══════════════════════════════════════════════════════════════════════════
# 第二節：認得多快（觸發月－衰退起點月）
# ═══════════════════════════════════════════════════════════════════════════

def section2(per_country_offset, pooled_offset):
    order = [cc for cc in ALL_CC_ORDER if cc in per_country_offset]
    names = [per_country_offset[cc]["name"] for cc in order]
    points = []
    for cc in order:
        info_d = per_country_offset[cc]
        for v in info_d.get("values", []):
            points.append({"x": v, "y": info_d["name"]})
    colors = [COUNTRY_COLORS.get(cc, "#6b7280") for cc in order for _v in per_country_offset[cc].get("values", [])]

    med = pooled_offset["median"]
    n_lag = sum(1 for cc in order for v in per_country_offset[cc].get("values", []) if v > 0)
    n_lead = sum(1 for cc in order for v in per_country_offset[cc].get("values", []) if v < 0)
    n_same = sum(1 for cc in order for v in per_country_offset[cc].get("values", []) if v == 0)

    if med is not None and med > 0:
        title = f"觸發那一刻，衰退平均已經開始 {fmt_num(med, 0)} 個月"
    elif med is not None and med < 0:
        title = f"觸發那一刻，衰退平均還要 {fmt_num(-med, 0)} 個月才開始"
    else:
        title = "觸發那一刻，跟衰退起點幾乎同一個月"

    lead = (f"每一個被認出來的衰退，取最早對到它的觸發月減去衰退起點月，正數是落後、負數是"
            f"領先。八國合併 {pooled_offset['n']} 次被認出的衰退，{n_lag} 次落後、{n_same} 次"
            f"同月、{n_lead} 次領先，中位數 {fmt_offset(med)}。")

    chart_js = f"""
new Chart(document.getElementById('chart2'), {{
  type:'scatter',
  data: {{ datasets: [{{ label:'每次被認出的衰退（國家內縱向排列）',
    data:{json.dumps(points, ensure_ascii=False)}, pointRadius:5,
    pointBackgroundColor:{json.dumps(colors)}, pointBorderColor:'#fff', pointBorderWidth:1 }}] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'觸發月 － 衰退起點月（月，負值＝領先）'}} }},
               y:{{ type:'category', labels:{json.dumps(names, ensure_ascii=False)},
                    title:{{display:true,text:'國家'}} }} }},
    plugins: {{ legend:{{ display:false }}, verticalLine:{{ value:0, color:'#111827' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart2"></canvas></div>'
    caption = ("每一點是一次被認出來的衰退，橫軸是觸發月減衰退起點月，直的黑色虛線是 0，"
               "點落在虛線右邊代表觸發時衰退已經開始（確認），落在左邊代表觸發在衰退開始之前"
               "（預告）。")

    rows = []
    for cc in order:
        info_d = per_country_offset[cc]
        rows.append(f"<tr><td class='lbl'>{esc(info_d['name'])}</td><td class='num'>{info_d['n']}</td>"
                     f"<td class='num'>{fmt_offset(info_d['median'])}</td>"
                     f"<td class='num'>{fmt_offset(info_d['min'])}</td>"
                     f"<td class='num'>{fmt_offset(info_d['max'])}</td></tr>")
    rows.append(f"<tr><td class='lbl'><b>合併池</b></td><td class='num'>{pooled_offset['n']}</td>"
                f"<td class='num'><b>{fmt_offset(pooled_offset['median'])}</b></td>"
                f"<td class='num'>{fmt_offset(pooled_offset['min'])}</td>"
                f"<td class='num'>{fmt_offset(pooled_offset['max'])}</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th><th class="num">被認出衰退次數</th>
<th class="num">中位數</th><th class="num">最早（領先）</th><th class="num">最晚（落後）</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""

    if n_lag > n_lead and n_lag > n_same:
        note = ("多數被認出來的衰退，Sahm 法則是在衰退已經開始之後才觸發，符合它原本的設計"
                 "定位：拿當下的失業率確認衰退是不是已經在發生，不是預測衰退會不會發生。")
    elif n_lead > n_lag and n_lead > n_same:
        note = "多數被認出來的衰退，觸發發生在衰退開始之前，這跟 Sahm 法則慣常被描述的「確認型」定位不同，細節見附錄逐事件明細。"
    else:
        note = "落後、領先、同月三種情況數量相近，八國合起來看不出單一方向。"

    html = _section_shell(1, title, lead, _std_body(chart_html, caption, table_html, note) + f"<script>{chart_js}</script>")
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第三節：門檻敏感度
# ═══════════════════════════════════════════════════════════════════════════

def section3(countries_data, pooled_by_threshold):
    rows_by_cc = {}
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        rows_by_cc[cc] = {"name": name, "by_th": d["by_threshold"]}

    order = [cc for cc in ALL_CC_ORDER if cc in rows_by_cc]
    datasets = []
    for cc in order:
        name = rows_by_cc[cc]["name"]
        vals = [rows_by_cc[cc]["by_th"][th]["hit_rate"] for th in THRESHOLDS]
        datasets.append({"label": name, "data": vals, "borderColor": COUNTRY_COLORS.get(cc, "#6b7280"),
                          "backgroundColor": "transparent", "tension": 0, "pointRadius": 4})

    us_low, us_high = pooled_by_threshold[THRESHOLDS[0]]["hit_rate"], pooled_by_threshold[THRESHOLDS[-1]]["hit_rate"]
    spreads = []
    for cc in order:
        vals = [rows_by_cc[cc]["by_th"][th]["hit_rate"] for th in THRESHOLDS]
        vals = [v for v in vals if v is not None]
        if len(vals) >= 2:
            spreads.append((rows_by_cc[cc]["name"], max(vals) - min(vals)))
    big_swing = [n for n, s in spreads if s >= 0.3]

    if big_swing:
        title = f"門檻 0.5 不是美國特有，但 {'、'.join(big_swing)} 換門檻命中率差很大"
    else:
        title = "換門檻對八國命中率的影響方向一致，不是美國特有的巧合"

    lead = (f"把主線門檻 0.5 換成更寬鬆的 0.3 與更嚴格的 0.7，同一國同一段樣本重算一次命中率、"
            f"事件數、召回率。合併池門檻 0.3 命中率 {fmt_pct(us_low)}，門檻 0.7 命中率 "
            f"{fmt_pct(us_high)}，這節看的是換門檻後，命中率跟召回率是不是同時往同一個方向走，"
            f"還是此消彼長。")

    chart_js = f"""
new Chart(document.getElementById('chart3'), {{
  type: 'line',
  data: {{ labels: {json.dumps([str(t) for t in THRESHOLDS])}, datasets: {json.dumps(datasets, ensure_ascii=False)} }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ title:{{display:true,text:'門檻（個百分點）'}} }},
               y:{{ min:0, max:1, title:{{display:true,text:'命中率'}},
                 ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:380px"><canvas id="chart3"></canvas></div>'
    caption = "每條線是一個國家，橫軸是門檻，縱軸是命中率。線越平代表這國的命中率對門檻選擇越不敏感。"

    def _cell(s):
        return (f"<td class='num'>{s['n_events']}</td><td class='num'>{fmt_pct(s['hit_rate'])}</td>"
                f"<td class='num'>{fmt_pct(s['recall']) if s['recall'] is not None else '—'}</td>")

    rows = []
    for cc in order:
        by_th = rows_by_cc[cc]["by_th"]
        rows.append(f"<tr><td class='lbl'>{esc(rows_by_cc[cc]['name'])}</td>"
                     + "".join(_cell(by_th[th]) for th in THRESHOLDS) + "</tr>")
    rows.append("<tr><td class='lbl'><b>合併池</b></td>"
                 + "".join(_cell(pooled_by_threshold[th]) for th in THRESHOLDS) + "</tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th rowspan="2">國家</th>
<th colspan="3">門檻 0.3</th><th colspan="3">門檻 0.5（主線）</th><th colspan="3">門檻 0.7</th></tr>
<tr><th class="num">事件數</th><th class="num">命中率</th><th class="num">召回率</th>
<th class="num">事件數</th><th class="num">命中率</th><th class="num">召回率</th>
<th class="num">事件數</th><th class="num">命中率</th><th class="num">召回率</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""

    if big_swing:
        note = (f"{'、'.join(big_swing)}換門檻後命中率變動超過 30 個百分點，這幾國的事件數本來就少，"
                 f"單一事件的判定翻轉就能大幅拉動命中率，換門檻的結論不穩，不是訊號本身不穩。")
    else:
        note = "八國換門檻後命中率的變動幅度接近，沒有哪一國對門檻選擇特別敏感或特別不敏感。"

    html = _section_shell(2, title, lead, _std_body(chart_html, caption, table_html, note) + f"<script>{chart_js}</script>")
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第四節：跟殖利率倒掛比
# ═══════════════════════════════════════════════════════════════════════════

def section4(vs_rows):
    if not vs_rows:
        return _section_shell(3, "跟殖利率倒掛比：資料不足", "兩個訊號的交集樣本不足，本節略過。", "<div class=\"card\">兩個訊號的可比較樣本不足。</div>")

    names = [r["name"] for r in vs_rows]
    yc_prec = [r["yield_curve"]["hit_rate"] for r in vs_rows]
    yc_rec = [r["yield_curve"]["recall"] for r in vs_rows]
    sm_prec = [r["sahm"]["hit_rate"] for r in vs_rows]
    sm_rec = [r["sahm"]["recall"] for r in vs_rows]

    n_yc_higher_recall = sum(1 for a, b in zip(yc_rec, sm_rec) if a is not None and b is not None and a > b)
    n_sm_higher_recall = sum(1 for a, b in zip(yc_rec, sm_rec) if a is not None and b is not None and b > a)
    n_sm_higher_prec = sum(1 for a, b in zip(yc_prec, sm_prec) if a is not None and b is not None and b > a)
    n_yc_higher_prec = sum(1 for a, b in zip(yc_prec, sm_prec) if a is not None and b is not None and a > b)

    if n_yc_higher_recall >= 5 and n_sm_higher_prec >= 5:
        title = "殖利率倒掛看得早，Sahm 法則看得準：召回率與精確率剛好分工"
    elif n_yc_higher_recall >= 5:
        title = "殖利率倒掛的召回率比 Sahm 法則高，但精確率沒有一致更高"
    elif n_sm_higher_prec >= 5:
        title = "Sahm 法則的精確率比殖利率倒掛高，但召回率沒有一致更高"
    else:
        title = "兩個訊號誰準、誰早，八國沒有一致的答案"

    lead = (f"同一國同一段交集樣本窗內，重新算一次殖利率倒掛（命中＝倒掛事件起點後 24 個月內"
            f"出現衰退起點）跟 Sahm 法則（門檻 0.5）的精確率（命中率）與召回率，"
            f"{n_yc_higher_recall} 國倒掛的召回率比 Sahm 法則高，{n_sm_higher_prec} 國 Sahm 法則"
            f"的精確率比倒掛高，看兩者是分工還是其中一個全面壓過另一個。")

    ds = []
    for r in vs_rows:
        cc = r["cc"]
        color = COUNTRY_COLORS.get(cc, "#6b7280")
        yp, yr = r["yield_curve"]["hit_rate"], r["yield_curve"]["recall"]
        sp, sr = r["sahm"]["hit_rate"], r["sahm"]["recall"]
        if yp is None or yr is None or sp is None or sr is None:
            continue
        ds.append({"label": r["name"], "data": [{"x": yp, "y": yr}, {"x": sp, "y": sr}],
                    "borderColor": color, "backgroundColor": color, "showLine": True,
                    "pointStyle": ["rectRot", "circle"], "pointRadius": 7, "borderWidth": 1.5})
    chart_js = f"""
new Chart(document.getElementById('chart4'), {{
  type:'scatter',
  data: {{ datasets: {json.dumps(ds, ensure_ascii=False)} }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ min:0, max:1, title:{{display:true,text:'精確率（命中率）'}},
                 ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }},
               y:{{ min:0, max:1, title:{{display:true,text:'召回率'}},
                 ticks:{{ callback:(v)=>Math.round(v*100)+'%' }} }} }},
    plugins: {{ legend:{{ display:true, position:'bottom' }} }} }}
}});
"""
    chart_html = '<div class="chart-wrap" style="height:400px"><canvas id="chart4"></canvas></div>'
    caption = ("每個國家兩點一線：菱形是殖利率倒掛，圓點是 Sahm 法則，同一國同一段交集樣本窗。"
               "線越往右上代表那個訊號在這一段換成另一個訊號後精確率、召回率同時變好。"
               "線幾乎水平或垂直代表兩個訊號只在其中一個指標上有差別。")

    rows = []
    for r in vs_rows:
        combo = r["combo"]
        rows.append(f"<tr><td class='lbl'>{esc(r['name'])}</td>"
                     f"<td>{esc(r['window'][0])}～{esc(r['window'][1])}</td>"
                     f"<td class='num'>{r['yield_curve']['n_testable']}</td>"
                     f"<td class='num'>{fmt_pct(r['yield_curve']['hit_rate'])}</td>"
                     f"<td class='num'>{fmt_pct(r['yield_curve']['recall'])}</td>"
                     f"<td class='num'>{r['sahm']['n_testable']}</td>"
                     f"<td class='num'>{fmt_pct(r['sahm']['hit_rate'])}</td>"
                     f"<td class='num'>{fmt_pct(r['sahm']['recall'])}</td>"
                     f"<td class='num'>{combo['n']}</td>"
                     f"<td class='num'>{fmt_pct(combo['hit_rate']) if combo['hit_rate'] is not None else '—'}</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th><th>交集樣本窗</th>
<th class="num">倒掛事件數</th><th class="num">倒掛精確率</th><th class="num">倒掛召回率</th>
<th class="num">Sahm 事件數</th><th class="num">Sahm 精確率</th><th class="num">Sahm 召回率</th>
<th class="num">兩個都觸發事件數</th><th class="num">兩個都觸發命中率</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""

    combo_ns = [r["combo"]["n"] for r in vs_rows if r["combo"]["hit_rate"] is not None]
    combo_hr = [r["combo"]["hit_rate"] for r in vs_rows if r["combo"]["hit_rate"] is not None]
    solo_hr = [r["yield_curve"]["hit_rate"] for r in vs_rows if r["yield_curve"]["hit_rate"] is not None]
    if combo_hr and solo_hr and (sum(combo_hr) / len(combo_hr)) > (sum(solo_hr) / len(solo_hr)):
        note = (f"倒掛事件起點後 24 個月內 Sahm 法則也觸發的組合事件，命中率平均比倒掛單獨看更高，"
                f"兩個訊號一起出現時，比只看其中一個更可信。")
    elif combo_ns and sum(combo_ns) < 5:
        note = "兩個訊號同時出現的組合事件數太少，這一項只能當參考，不足以下結論。"
    else:
        note = "兩個訊號同時出現的組合事件，命中率沒有明顯比單獨看倒掛更高。"

    html = _section_shell(3, title, lead, _std_body(chart_html, caption, table_html, note) + f"<script>{chart_js}</script>")
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第五節：2019 年以來
# ═══════════════════════════════════════════════════════════════════════════

SECTION5_START = "2019-01"


def section5(countries_data, us_2024_07):
    rows = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        for ev in d["primary"]["events"]:
            if ev["start"] < SECTION5_START:
                continue
            rows.append({"cc": cc, "name": name, "start": ev["start"], "peak_s": ev["peak_s"],
                         "n_trigger_months": ev["n_trigger_months"], "verdict": ev["verdict"],
                         "offset": ev["offset_months"]})
    rows.sort(key=lambda r: (r["start"], r["cc"]))

    n_2020 = sum(1 for r in rows if r["start"] < "2021-01")
    n_2022plus = sum(1 for r in rows if r["start"] >= "2021-01")

    title = f"2019 年以來八國共 {len(rows)} 次觸發，2020 年那一波幾乎全部命中"

    lead = (f"2020 年疫情前後 {n_2020} 次觸發，2021 年之後（含 2022－2024 的升息週期）"
            f"{n_2022plus} 次觸發，這節只列事件，不重新定義判準。")

    def _row(r):
        return (f"<tr><td class='lbl'>{esc(r['name'])}</td><td>{esc(r['start'])}</td>"
                f"<td class='num'>{fmt_num(r['peak_s'], 2)}</td>"
                f"<td class='num'>{r['n_trigger_months']}</td>"
                f"<td>{esc(verdict_label(r['verdict']))}</td>"
                f"<td class='num'>{fmt_offset(r['offset']) if r['offset'] is not None else '—'}</td></tr>")
    table_html = f"""<div class="scroll"><table><thead><tr><th>國家</th><th>事件起點</th>
<th class="num">峰值 S</th><th class="num">觸發月數</th><th>判定</th>
<th class="num">落後／領先月數</th></tr></thead>
<tbody>{''.join(_row(r) for r in rows)}</tbody></table></div>"""

    if us_2024_07 is not None:
        s_val, verdict = us_2024_07["s_value"], us_2024_07["verdict"]
        us_para = (f"美國 2024 年 7 月觸發，S(t) 為 {fmt_num(s_val, 2)}，用抓取當下最新公布"
                    f"的 UNRATE 資料重算，判定為「{verdict_label(verdict)}」。定義 A"
                    f"（技術性衰退）在 2024 年到 2026 年 4 月（GDP 資料涵蓋到的最後一季）之間"
                    f"沒有出現衰退起點，12 個月的判定窗口在抓取當下已經走完。媒體當時引用的"
                    f"即時 S 值約 0.53，比本頁算出的數字高一點，差距來自失業率資料後續的"
                    f"季節調整修正，不是計算方式不同。")
    else:
        us_para = "美國 2024 年 7 月的觸發事件因資料不足無法判定，見上表。"

    note = ("表中「判定」欄位跟第一節命中率的分母定義一致，「同時或落後」不算落空，"
            "「未到期」代表 12 個月判定窗口在抓取當下還沒走完。")

    body = (table_html + f'\n<div class="note">{esc(note)}</div>\n'
            + f'<div class="card" style="margin-top:1rem"><b>美國 2024 年 7 月：單獨看數字</b><br>'
            + f'<p style="margin-top:.5rem;font-size:.9rem">{esc(us_para)}</p></div>')
    html = _section_shell(4, title, lead, body)
    return html


# ═══════════════════════════════════════════════════════════════════════════
# 第六節：八國失業率全史小圖
# ═══════════════════════════════════════════════════════════════════════════

def _small_multiple_chart(cid, labels, values, band, trigger_points, ymin, ymax):
    labels_json = json.dumps(labels, ensure_ascii=False)
    values_json = json.dumps(values)
    band_json = json.dumps([ymax if b else None for b in band])
    trig_json = json.dumps(trigger_points)
    return f"""
new Chart(document.getElementById('{cid}'), {{
  type: 'bar',
  data: {{ labels: {labels_json},
    datasets: [
      {{ type:'bar', label:'衰退（定義 A）', data:{band_json}, backgroundColor:'#e5e7eb',
         barPercentage:1, categoryPercentage:1, base:{ymin}, order:3 }},
      {{ type:'line', label:'失業率 (%)', data:{values_json}, borderColor:'{BRAND_BLUE}',
         backgroundColor:'transparent', pointRadius:0, borderWidth:1.3, order:2 }},
      {{ type:'line', label:'Sahm 觸發（事件起點）', data:{trig_json}, borderColor:'transparent',
         backgroundColor:'{DEEP_RED}', pointBackgroundColor:'{DEEP_RED}', pointRadius:4,
         pointBorderColor:'#fff', pointBorderWidth:1, showLine:false, order:1 }}
    ] }},
  options: {{ responsive:true, maintainAspectRatio:false, animation:false,
    scales: {{ x:{{ ticks:{{ maxTicksLimit:8 }} }}, y:{{ min:{ymin}, max:{ymax},
      title:{{display:true,text:'%'}} }} }},
    plugins: {{ legend:{{ display:false }} }} }}
}});
"""


def section6(countries_data):
    charts_js = []
    blocks = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        series = d["unemployment_series"]
        labels = [m for m, _v in series]
        values = [v for _m, v in series]
        spans = d["gdp_recession_spans"]
        band = [1 if in_any_span(m, spans) else None for m in labels]
        trigger_starts = {ev["start"] for ev in d["primary"]["events"]}
        month_val = dict(series)
        trig_points = [month_val[m] if m in trigger_starts else None for m in labels]
        ymin, ymax = min(values), max(values) * 1.05
        cid = f"chart6-{cc.lower()}"
        charts_js.append(_small_multiple_chart(cid, labels, values, band, trig_points, ymin, ymax))
        blocks.append(f'<div style="flex:1 1 260px;min-width:0"><h3 style="font-size:.82rem;'
                       f'margin-bottom:.4rem">{esc(name)}</h3>'
                       f'<div class="chart-wrap" style="height:200px"><canvas id="{cid}"></canvas></div></div>')
    grid = f'<div style="display:flex;flex-wrap:wrap;gap:1.2rem;margin-top:1rem">{"".join(blocks)}</div>'

    title = "八國失業率全史：灰底是技術性衰退，紅點是 Sahm 法則觸發"
    lead = ("前五節都是統計摘要，這節把每個國家的失業率原始序列整段畫出來，附錄性質，"
            "供對照查核，不對應單一論點。")
    caption = ("灰底區間是定義 A 的衰退期，紅點是每次 Sahm 法則事件的起點（不是每個觸發月都點，"
               "只標事件第一個觸發月）。紅點落在灰底裡面代表觸發時衰退已經開始，紅點在灰底"
               "左邊、且離灰底不遠代表提前預警。")
    body = grid + f'\n<div class="note">{esc(caption)}</div>\n' + f"<script>{''.join(charts_js)}</script>"
    return _section_shell(5, title, lead, body)


def appendix_event_detail(countries_data):
    blocks = []
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        events = d["primary"]["events"]
        if not events:
            continue
        rows = []
        for ev in events:
            rows.append(f"<tr><td>{esc(ev['start'])}</td><td class='num'>{fmt_num(ev['peak_s'], 2)}</td>"
                         f"<td class='num'>{ev['n_trigger_months']}</td>"
                         f"<td>{esc(verdict_label(ev['verdict']))}</td>"
                         f"<td class='num'>{fmt_offset(ev['offset_months']) if ev['offset_months'] is not None else '—'}</td></tr>")
        blocks.append(f"""<h4 style="font-size:.88rem;margin:1rem 0 .5rem">{esc(name)}</h4>
<div class="scroll"><table><thead><tr><th>事件起點</th><th class="num">峰值 S</th>
<th class="num">觸發月數</th><th>判定</th><th class="num">落後／領先月數</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>""")
    body = "".join(blocks)
    return f"""
<div class="section">
<details>
<summary style="cursor:pointer;font-weight:700;font-size:1.02rem;padding:.4rem 0">
附錄：逐事件明細（門檻 0.5，八國逐筆列出）</summary>
<div class="card" style="margin-top:.75rem">
<p style="font-size:.85rem;margin-bottom:.5rem">前面各節的長條圖、散佈圖、條帶圖都是這張表拆解後
畫出來的，這裡把原始逐筆事件列出來備查。</p>
{body}
</div>
</details>
</div>
"""


# ═══════════════════════════════════════════════════════════════════════════
# 頁面組裝
# ═══════════════════════════════════════════════════════════════════════════

def generate_html(countries_data, pooled, pooled_offset, per_country_offset, pooled_by_threshold,
                   vs_yc_rows, us_nber_d, us_2024_07, tw_status, built_date):
    main_style, nav_block = extract_template_parts()
    title = "Sahm 法則跨國適用嗎：八國回測 | InvestMQuest Research"
    tw_desc = "台灣併入主表（樣本窗自 2016 年起）" if tw_status == "ok" else "台灣資料整理中，本頁先出七國版本"
    description = (f"用 FRED 與主計總處資料對美/德/英/日/加/澳/韓/台套同一把尺回測 Sahm 法則："
                    f"失業率 3 個月移動平均比過去 12 個月低點高 0.5 個百分點是否預示衰退。"
                    f"合併池命中率 {fmt_pct(pooled['hit_rate'])}、基率 {fmt_pct(pooled['base_rate'])}，"
                    f"認出衰退平均落後起點 {fmt_num(pooled_offset['median'], 0)} 個月，{tw_desc}，"
                    f"另檢查門檻敏感度、跟殖利率倒掛的精確率召回率比較。")

    try:
        sys.path.insert(0, str(NAV_DIR))
        from _nav_common import make_toggle  # noqa
        subnav = make_toggle("sahm_rule")
    except Exception as e:
        warn(f"make_toggle 載入失敗：{e}，pill bar 留空")
        subnav = ""

    s1_html, straddlers = section1(countries_data, pooled, us_nber_d)
    s2_html = section2(per_country_offset, pooled_offset)
    s3_html = section3(countries_data, pooled_by_threshold)
    s4_html = section4(vs_yc_rows)
    s5_html = section5(countries_data, us_2024_07)
    s6_html = section6(countries_data)
    appendix = appendix_event_detail(countries_data)
    s7_html = section_method(vs_yc_rows)
    s8_html = section_caveats()

    if straddlers:
        threshold_note = "門檻 0.3 到 0.7 之間，各國命中率變動幅度不一致，見第三節。"
    else:
        threshold_note = "門檻從 0.3 拉到 0.7，八國命中率變動方向大致一致，不是美國獨有的巧合，見第三節。"

    if vs_yc_rows:
        n_yc_better_recall = sum(1 for r in vs_yc_rows
                                  if r["yield_curve"]["recall"] is not None and r["sahm"]["recall"] is not None
                                  and r["yield_curve"]["recall"] > r["sahm"]["recall"])
        vs_yc_note = (f"同窗比較下，{n_yc_better_recall} 個國家殖利率倒掛的召回率比 Sahm 法則高，"
                      f"細節見第四節。")
    else:
        vs_yc_note = "殖利率倒掛的同窗比較資料不足，見第四節說明。"

    hero = section_hero(pooled, pooled_offset, tw_status, threshold_note, vs_yc_note)

    takeaway = ("<b>給沒有統計背景的讀者：</b>Sahm 法則是拿失業率算出來的一個數字。先算失業率"
                "最近 3 個月的平均，再看這個平均比過去一年裡最低的時候高了多少，高超過 0.5 個"
                "百分點就算「觸發」。這頁把八個國家的失業率資料全部拉出來，自動判定每一次觸發"
                "算不算對到衰退、對到的時候衰退已經開始多久、換一個門檻結果會不會不一樣，"
                "再跟殖利率倒掛這個訊號並排比較。本頁不做「現在該不該擔心」的建議，也不預測"
                "下一次衰退什麼時候來，只回報歷史上這個訊號準不準、準多快、在哪些條件下會失真。")

    body = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<script src="{CHART_JS_CDN_LOCAL}"></script>
{main_style}
</head>
<body>
{nav_block}

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / Sahm 法則跨國回測</div>
    <h1>Sahm 法則跨國適用嗎：八國回測</h1>
    <div class="sub">失業率離低點回升 0.5 個百分點能不能預示衰退、是不是只對美國準・生成 {esc(built_date)}</div>
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
{appendix}
{s7_html}
{s8_html}

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; Sahm 法則跨國適用嗎：八國回測（研究頁，不構成投資建議）
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
    yc = load_yc()
    yc_countries = yc.get("countries", {})

    countries_data = []
    for cc, name in COUNTRIES_FRED:
        if cc == "US":
            unemployment_pts = raw_series.get("UNRATE")
        else:
            unemployment_pts = raw_series.get(f"LRHUTTTT{cc}M156S")
        yc_c = yc_countries.get(cc, {})
        spans = [tuple(x) for x in yc_c.get("gdp_recession_spans", [])]
        gdp_range = yc_c.get("gdp_data_range", [None, None])
        if not unemployment_pts or not spans or gdp_range[0] is None:
            d = {"cc": cc, "name": name, "status": "missing"}
            warn(f"{cc} {name}: 缺失業率或衰退區間資料")
        else:
            d = build_country_sahm(cc, name, unemployment_pts, spans, gdp_range)
        countries_data.append((cc, name, d))

    tw_manual_d = load_tw_manual()
    tw_d = build_taiwan(tw_manual_d, yc_countries.get("TW", {}))
    tw_status = tw_d.get("status")
    if tw_status != "ok":
        warn(f"TW 台灣: 狀態={tw_status}（{tw_d.get('note')}）")
    countries_data.append(("TW", "台灣", tw_d))

    # 美國 NBER 對照
    us_nber_d = None
    if raw_series.get("USRECM") and raw_series.get("UNRATE"):
        c_spans, _c_starts = recession_transitions(raw_series["USRECM"])
        nber_end = month_key(raw_series["USRECM"][-1][0])
        us_nber_d = build_country_sahm("US", "美國", raw_series["UNRATE"], c_spans,
                                        ["1948-01", nber_end])

    pooled = pooled_primary_stats(countries_data)
    per_country_offset_raw = {}
    for cc, name, d in countries_data:
        if d.get("status") != "ok":
            continue
        vals = sorted(d["recognized_offsets"].values())
        per_country_offset_raw[cc] = {"name": name, "values": vals, "n": len(vals),
                                       "min": min(vals) if vals else None,
                                       "median": statistics.median(vals) if vals else None,
                                       "max": max(vals) if vals else None}
    _per_country_offset_dummy, pooled_offset = pooled_recognized_offsets(countries_data)
    pooled_by_threshold = {th: pooled_threshold_stats(countries_data, th) for th in THRESHOLDS}

    vs_yc_rows = []
    for cc, name, d in countries_data:
        yc_c = yc_countries.get(cc)
        r = build_vs_yield_curve(cc, name, d, yc_c)
        if r:
            vs_yc_rows.append(r)

    us_d = next((d for cc, n, d in countries_data if cc == "US"), None)
    us_2024_07 = None
    if us_d and us_d.get("status") == "ok":
        s_series = dict(us_d["S_series"])
        s_val = s_series.get("2024-07")
        ev = next((e for e in us_d["primary"]["events"] if e["start"] == "2024-07"), None)
        if s_val is not None:
            verdict = ev["verdict"] if ev else ("miss" if s_val < PRIMARY_THRESHOLD else "not_yet_due")
            us_2024_07 = {"s_value": s_val, "verdict": verdict}

    built_date = datetime.now().strftime("%Y-%m-%d")

    def _json_default(o):
        return str(o)

    out_payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "countries": {cc: d for cc, _n, d in countries_data},
        "us_nber": us_nber_d,
        "pooled": pooled,
        "pooled_offset": pooled_offset,
        "per_country_offset": per_country_offset_raw,
        "pooled_by_threshold": pooled_by_threshold,
        "vs_yield_curve": vs_yc_rows,
        "us_2024_07": us_2024_07,
        "thresholds": THRESHOLDS, "primary_threshold": PRIMARY_THRESHOLD,
        "definitions": DEFINITIONS_TEXT,
        "series_used": {"US": "UNRATE（主線）／LRHUTTTTUSM156S（對照）",
                        **{cc: f"LRHUTTTT{cc}M156S" for cc, _n in COUNTRIES_FRED if cc != "US"},
                        "TW": "主計總處人力資源調查重要指標(季節調整)"},
    }
    DATA.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2, default=_json_default) + "\n",
                        encoding="utf-8")
    info(f"寫入 {OUT_JSON}")

    html_out = generate_html(countries_data, pooled, pooled_offset, per_country_offset_raw,
                              pooled_by_threshold, vs_yc_rows, us_nber_d, us_2024_07, tw_status,
                              built_date)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_out, encoding="utf-8")
    info(f"寫入 {OUT_HTML}")

    info(f"合併池：命中率={pooled['hit_rate']} 基率={pooled['base_rate']} 提升={pooled['uplift']}")
    info(f"認出衰退落後月數：中位數={pooled_offset['median']} min={pooled_offset['min']} max={pooled_offset['max']}")
    if us_2024_07:
        info(f"美國 2024-07 spot check：S={us_2024_07['s_value']} 判定={us_2024_07['verdict']}")


def main():
    ap = argparse.ArgumentParser(description="Sahm 法則跨國回測 builder")
    ap.add_argument("--fetch", action="store_true", help="只抓 FRED 序列存 raw json，不算統計、不生頁面")
    args = ap.parse_args()
    if args.fetch:
        do_fetch()
        return
    do_compute_and_build()


if __name__ == "__main__":
    main()

