#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score_flowmap.py — flowmap 成績單：凍結預測 vs 實際的機械對帳（設計稿 §F2）。

設計依據：notes/site-internal/root/_flowmap_forecast_ledger_design_20260901.md
§F（自動對帳與進化迴路）。判斷已在設計稿凍結，本檔只負責對帳與舉旗——**不刪除
任何模組、不調整任何 CONFIG／門檻**；kill 條款觸發時只在輸出標記 🔴，處決一律
留給持有人於校準輪決定（§F4）。

三個對帳對象
------------
  CTA 模組     ：對 docs/flowmap/data/forecast_history.jsonl 逐日凍結的
                 nearest-flip-level，判斷次一交易日價格是否穿越（用
                 data/flowmap_prices.json 判定）；穿越週依 CFTC COT 報告週界
                 分組（多次穿越取淨向），對帳對象為該市場 COT 淨部位的週變化
                 方向（data/cot_history.json）。rolling 26 週命中率。另計
                 「自我一致性」：穿越後重新計算的實際 composite 是否等於凍結
                 時記錄的 if_breached_composite（sanity 欄，非 kill 依據）。
  月末件       ：對凍結於生效窗首日的方向，比對生效窗 3 個交易日的實際
                 SPY−AGG 相對報酬方向。rolling 8 次。
  rv-model     ：讀 knowledge/forecast_settlement.json（由
                 knowledge/settle_forecasts.py 產生，本檔不重跑），算 raw
                 Brier；resolved ≥20 筆才算 BSS（口徑與 knowledge/q.py
                 cmd_forecasts 逐字一致：base_rate=該 source resolved 集合的
                 in-sample outcome 頻率，brier_clim=base_rate×(1−base_rate)，
                 BSS=1−Brier/Brier_clim）。

CTA 對帳的 COT 類別選擇（設計稿 §F2：「優先 leveraged funds，快取無此類別則
用 non-commercial，實際採用類別寫進 scorecard meta」）
-----------------------------------------------------------------------------
data/cot_history.json 由 scripts/build_crowding.py 維護，其 meta.methodology
明文為 legacy futures-only 報告的 net_pct_oi（僅 non-commercial 一種類別，
無 disaggregated report 的 leveraged funds 細分）。本檔因此落在「無 leveraged
funds 則用 non-commercial」分支，非本檔自行選擇——已寫入輸出 meta 供稽核。

顯著性檢定（kill 判定用，設計稿未指定顯著水準，本檔選定，供持有人複審）
-------------------------------------------------------------------------
精確二項檢定（雙尾），α=0.10。n 達到 rolling 視窗大小（CTA=26／月末=8）才
評分；n 不足一律 🟡 樣本不足不評分。判定規則：
  🟢 健康  — p ≤ α 且命中率 > 50%（統計上顯著優於擲硬幣）
  🔴 kill  — 其餘情形（含「與擲硬幣無統計差異」的字面 kill 條件，以及本檔
             額外判為同等失格的「顯著劣於擲硬幣」——後者是本檔在設計稿字面
             之外的判斷延伸，非逐字條文，供持有人於校準輪複審是否要收斂
             回原字面定義）。
rv-model 的 kill 判準則是設計稿逐字條文：resolved≥20 筆後 BSS<0 → 🔴。

輸出
----
  docs/flowmap/data/scorecard.json（schema="flowmap-scorecard-v1"，zero-churn
  寫入：剝除 generated_at 後內容不變則不落盤）。

CLI
---
  python scripts/score_flowmap.py          正常執行

本檔零 LLM、零網路請求（只讀本地已存在的 JSON／JSONL 快取與 forecast_history）。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FLOWMAP_DATA_DIR = ROOT / "docs" / "flowmap" / "data"
FORECAST_HISTORY = FLOWMAP_DATA_DIR / "forecast_history.jsonl"
FLOWMAP_PRICES = DATA / "flowmap_prices.json"
COT_HISTORY = DATA / "cot_history.json"
FORECAST_SETTLEMENT = ROOT / "knowledge" / "forecast_settlement.json"
OUT_JSON = FLOWMAP_DATA_DIR / "scorecard.json"

SCHEMA = "flowmap-scorecard-v1"

# ═══════════════════════════════════════════════════════════════════════════
# CONFIG — PREREG 凍結（設計稿 §F2／§A6／§E2／§E3）。不得依單一案例調參。
# ═══════════════════════════════════════════════════════════════════════════

CTA_ROLLING_WEEKS = 26          # 設計稿 §A6：「連兩季（26 週）」
CTA_MIN_SAMPLES = CTA_ROLLING_WEEKS
MONTH_END_ROLLING_N = 8          # 設計稿 §E2：「連八次月末」
RV_MIN_RESOLVED_FOR_BSS = 20     # 設計稿 §E3：「resolved ≥20 筆」
SIGNIFICANCE_ALPHA = 0.10        # 本檔選定（見檔頭說明），非設計稿逐字給定

CTA_MARKET_TO_PROXY = {"SPX": "SPY", "NDX": "QQQ", "RTY": "IWM"}
# COT 合約代碼（data/cot_history.json 的 markets key），對齊 build_flowmap.py CTA_MARKETS
CTA_MARKET_TO_COT_CODE = {
    "SPX": "13874A",  # S&P 500 E-mini
    "NDX": "209742",  # Nasdaq-100 E-mini
    "RTY": "239742",  # Russell 2000 E-mini
}
COT_CATEGORY_USED = "non_commercial"
COT_CATEGORY_REASON = (
    "data/cot_history.json（scripts/build_crowding.py 維護）meta.methodology="
    "legacy futures-only net_pct_oi，僅 non-commercial 一種類別、無 disaggregated "
    "report 的 leveraged funds 細分——依設計稿 §F2 優先序「無 leveraged funds 則用 "
    "non-commercial」，本檔落在此分支，非本檔自行選擇。"
)

CTA_KILL_TEXT = "連兩季（26 週）COT 方向對帳命中率與擲硬幣無統計差異 → 模組降級為 gaps 或刪除（設計稿 §A6）"
MONTH_END_KILL_TEXT = ("連八次月末（含季末）方向對帳命中與擲硬幣無統計差異 → 模組降級為 gaps 或刪除"
                       "（月頻樣本慢，約需 2 年才足量，設計稿 §E2）")
RV_KILL_TEXT = "rv-model source resolved ≥20 筆後 BSS < 0（輸給 climatology）→ producer 砍（設計稿 §E3）"


def warn(msg: str) -> None:
    print(f"[score-flowmap][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[score-flowmap] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# reuse build_flowmap.py 的 CTA 模組邏輯（PREREG 凍結的窗長／CTA_MARKETS 常數與
# cta_module() 函式）——自我一致性檢查直接重算「實際 composite」，不得另開一份
# 可能與原模組漂移的複製邏輯。
# ═══════════════════════════════════════════════════════════════════════════
sys.path.insert(0, str(ROOT / "scripts"))
import build_flowmap as _bf  # noqa: E402


# ═══════════════════════════════════════════════════════════════════════════
# I/O（zero-churn 寫入協議，同 build_flowmap.py／build_regime.py）
# ═══════════════════════════════════════════════════════════════════════════

def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        warn(f"could not read {os.path.basename(path)}: {e}")
        return default


def _serialize(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _strip_volatile(obj, keys):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def write_json_if_changed(path, obj, volatile=("generated_at",)) -> bool:
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_serialize(obj))
    return True


def rnd(v, d):
    if v is None:
        return None
    try:
        return round(float(v), d)
    except (TypeError, ValueError):
        return None


def load_forecast_history():
    rows = []
    if not FORECAST_HISTORY.exists():
        return rows
    with FORECAST_HISTORY.open(encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                rows.append(json.loads(ln))
            except json.JSONDecodeError:
                continue
    rows.sort(key=lambda r: r.get("date") or "")
    return rows


def load_price_series():
    data = load_json(FLOWMAP_PRICES, {}) or {}
    series = data.get("series") or {}
    out = {}
    for t, rows in series.items():
        try:
            out[t] = sorted(((d, c) for d, c in rows), key=lambda x: x[0])
        except (TypeError, ValueError):
            out[t] = []
    built_at = (data.get("meta") or {}).get("built_at")
    return out, built_at


def load_cot_series(code):
    data = load_json(COT_HISTORY, {}) or {}
    m = (data.get("markets") or {}).get(code)
    if not m:
        return []
    try:
        return sorted(((d, v) for d, v in m.get("series") or []), key=lambda x: x[0])
    except (TypeError, ValueError):
        return []


def _close_on(series_pts, ymd):
    for d, c in series_pts:
        if d == ymd:
            return c
    return None


def _close_before(series_pts, ymd):
    """最近一根 date < ymd 的收盤；series_pts 已升冪排序。"""
    best = None
    for d, c in series_pts:
        if d < ymd:
            best = c
        else:
            break
    return best


# ═══════════════════════════════════════════════════════════════════════════
# 顯著性檢定：精確二項檢定（雙尾）
# ═══════════════════════════════════════════════════════════════════════════

def _binom_two_sided_pvalue(hits, n, p=0.5):
    if n == 0:
        return None
    p_obs = math.comb(n, hits) * (p ** hits) * ((1 - p) ** (n - hits))
    total = 0.0
    for k in range(n + 1):
        pk = math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
        if pk <= p_obs * (1 + 1e-9):
            total += pk
    return round(total, 6)


def _status_from_binom(n, hits, min_n, alpha=SIGNIFICANCE_ALPHA):
    """回傳 (status, hit_rate, p_value)。status ∈ {"yellow","green","red"}。
    yellow：n < min_n（樣本不足不評分）。
    green：n ≥ min_n 且統計上顯著優於擲硬幣（p ≤ alpha 且命中率 > 0.5）。
    red：其餘（含「與擲硬幣無統計差異」的字面 kill 條件，以及本檔判為同等
         失格的「顯著劣於擲硬幣」，見檔頭說明）。"""
    if n < min_n:
        hit_rate = rnd(hits / n, 3) if n else None
        return "yellow", hit_rate, None
    hit_rate = hits / n
    p_value = _binom_two_sided_pvalue(hits, n)
    if p_value is not None and p_value <= alpha and hit_rate > 0.5:
        return "green", rnd(hit_rate, 3), p_value
    return "red", rnd(hit_rate, 3), p_value


# ═══════════════════════════════════════════════════════════════════════════
# CTA 模組對帳
# ═══════════════════════════════════════════════════════════════════════════

def _cot_week_for_date(cot_dates_sorted, ymd):
    """回傳 (prev_report_date, report_date)：ymd 落在哪個 COT 報告週
    （週期定義＝(prev_report_date, report_date]）。ymd 早於第一份報告（週期
    不完整）或晚於最新報告日（週期尚未結束）→ (None, None)。"""
    for i, d in enumerate(cot_dates_sorted):
        if ymd <= d:
            if i == 0:
                return (None, None)
            return (cot_dates_sorted[i - 1], d)
    return (None, None)


def _cot_weekly_change_direction(cot_series, report_date):
    dates = [d for d, _ in cot_series]
    if report_date not in dates:
        return None, None, None
    idx = dates.index(report_date)
    if idx == 0:
        return None, None, None
    cur_v = cot_series[idx][1]
    prev_v = cot_series[idx - 1][1]
    delta = cur_v - prev_v
    direction = 1 if delta > 1e-9 else (-1 if delta < -1e-9 else 0)
    return direction, cur_v, prev_v


def _detect_cta_breaches(fh_rows, price_series, gaps):
    """逐日比對「前一日凍結的 nearest_flip_level」vs「當日實際收盤」，判斷是否
    穿越。回傳 (events, consistency)：
      events       — [{"date","market","direction"(+1/-1)}, ...]
      consistency  — {"n":int,"consistent":int,"mismatches":[...]}（自我一致性
                     sanity 欄：穿越後重算的實際 composite 是否等於凍結時記錄的
                     if_breached_composite；用 build_flowmap.cta_module 原生邏輯
                     重算，不是另開一份複製邏輯）。"""
    events = []
    consistency = {"n": 0, "consistent": 0, "mismatches": []}

    for i in range(1, len(fh_rows)):
        prev_row, cur_row = fh_rows[i - 1], fh_rows[i]
        cur_date = cur_row.get("date")
        prev_fc = (prev_row.get("frozen_forecast") or {}).get("cta") or []
        if not cur_date or not prev_fc:
            continue

        trunc_series = {t: [(d, c) for d, c in price_series.get(t, []) if d <= cur_date]
                        for t in ("SPY", "QQQ", "IWM")}
        actual_today = {}
        try:
            for m in _bf.cta_module(trunc_series, []):
                actual_today[m["market"]] = m["composite_signal"]
        except Exception as e:
            warn(f"CTA 自我一致性重算失敗（{cur_date}）：{e}")

        for entry in prev_fc:
            market = entry.get("market")
            flip_level = entry.get("nearest_flip_level")
            prev_dist = entry.get("dist_pct")
            proxy = CTA_MARKET_TO_PROXY.get(market)
            if not proxy or flip_level is None or prev_dist is None:
                continue
            proxy_pts = price_series.get(proxy) or []
            cur_close = _close_on(proxy_pts, cur_date)
            if cur_close is None:
                continue  # 價格快取當天沒有這個日期（非交易日或快取缺口），跳過

            prior_side = 1 if prev_dist > 0 else (-1 if prev_dist < 0 else 0)
            if prior_side == 0:
                continue
            diff = cur_close - flip_level
            new_side = 1 if diff > 0 else (-1 if diff < 0 else 0)
            if new_side == 0 or new_side == prior_side:
                continue  # 未穿越

            events.append({"date": cur_date, "market": market, "direction": new_side})

            consistency["n"] += 1
            predicted_composite = entry.get("if_breached_composite")
            actual_composite = actual_today.get(market)
            if predicted_composite is not None and actual_composite is not None:
                if predicted_composite == actual_composite:
                    consistency["consistent"] += 1
                elif len(consistency["mismatches"]) < 10:
                    consistency["mismatches"].append({
                        "date": cur_date, "market": market,
                        "predicted": predicted_composite, "actual": actual_composite,
                    })
    return events, consistency


def _aggregate_cta_weekly(events, gaps):
    """把穿越事件依 (market, COT 報告週) 分組取淨向，比對該市場 COT 類別的週
    變化方向。回傳 samples（升冪 by report_date）。"""
    cot_series_by_market = {mkt: load_cot_series(code) for mkt, code in CTA_MARKET_TO_COT_CODE.items()}
    groups = {}
    for e in events:
        cot_series = cot_series_by_market.get(e["market"]) or []
        cot_dates_sorted = [d for d, _ in cot_series]
        prev_report, report_date = _cot_week_for_date(cot_dates_sorted, e["date"])
        if report_date is None:
            gaps.append(f"CTA {e['market']}：{e['date']} 落在 COT 報告週界之外（早於首份或晚於最新報告），"
                        "該筆穿越暫不計分")
            continue
        groups.setdefault((e["market"], report_date), []).append(e["direction"])

    samples = []
    for (market, report_date), dirs in sorted(groups.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        net = sum(dirs)
        if net == 0:
            gaps.append(f"CTA {market}：{report_date} 當週多次穿越淨向持平（{dirs}），不列入樣本")
            continue
        pred_dir = 1 if net > 0 else -1
        cot_series = cot_series_by_market.get(market) or []
        actual_dir, cur_v, prev_v = _cot_weekly_change_direction(cot_series, report_date)
        if actual_dir is None:
            gaps.append(f"CTA {market}：{report_date} 週界不完整或無 COT 資料，不列入樣本")
            continue
        if actual_dir == 0:
            gaps.append(f"CTA {market}：{report_date} 當週 COT 淨部位變化為零，不列入樣本")
            continue
        samples.append({
            "market": market, "report_date": report_date,
            "n_crossings": len(dirs), "pred_dir": pred_dir,
            "cot_net_pct_oi_delta": round(cur_v - prev_v, 3),
            "actual_dir": actual_dir, "hit": bool(pred_dir == actual_dir),
        })
    return samples


def build_cta_report(fh_rows, price_series, gaps):
    events, consistency = _detect_cta_breaches(fh_rows, price_series, gaps)
    samples = _aggregate_cta_weekly(events, gaps)

    distinct_dates = sorted({s["report_date"] for s in samples})
    rolling_dates = set(distinct_dates[-CTA_ROLLING_WEEKS:])
    rolling = [s for s in samples if s["report_date"] in rolling_dates]
    n = len(rolling)
    hits = sum(1 for s in rolling if s["hit"])

    status, hit_rate, p_value = _status_from_binom(n, hits, CTA_MIN_SAMPLES)
    status_label = {
        "yellow": f"樣本累積中（{n}／需 {CTA_MIN_SAMPLES}）",
        "green": "健康：命中率統計上顯著優於擲硬幣",
        "red": "kill 門檻觸發：命中率與擲硬幣無統計差異或更差，待校準輪處決",
    }[status]

    consistency_rate = rnd(consistency["consistent"] / consistency["n"], 3) if consistency["n"] else None

    return {
        "status": status,
        "status_label": status_label,
        "n_samples": n,
        "n_required": CTA_MIN_SAMPLES,
        "hits": hits,
        "hit_rate": hit_rate,
        "p_value": p_value,
        "significance_alpha": SIGNIFICANCE_ALPHA,
        "self_consistency": {
            "n": consistency["n"],
            "consistent": consistency["consistent"],
            "rate": consistency_rate,
            "mismatches": consistency["mismatches"],
        },
        "cot_category_used": COT_CATEGORY_USED,
        "recent_samples": rolling[-20:],
        "kill_condition": CTA_KILL_TEXT,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 月末件對帳
# ═══════════════════════════════════════════════════════════════════════════

DIR_LABEL = {
    "sell_equity_buy_bond": "股票跑贏，月底傾向賣股買債",
    "buy_equity_sell_bond": "債券跑贏，月底傾向買股賣債",
    "flat": "股債報酬大致持平，方向不明顯",
}


def build_month_end_report(fh_rows, price_series, gaps):
    events = []
    for row in fh_rows:
        me = (row.get("frozen_forecast") or {}).get("month_end")
        if me:
            events.append(me)
    events.sort(key=lambda e: e.get("as_of") or "")

    spy_pts = price_series.get("SPY") or []
    agg_pts = price_series.get("AGG") or []

    resolved = []
    pending = 0
    for e in events:
        window_start = e.get("window_start")
        window_end = e.get("window_end")
        direction_pred = e.get("direction")
        if not window_start or not window_end or not direction_pred:
            gaps.append(f"月末件：{e.get('as_of')} 凍結記錄欄位不完整，跳過")
            continue
        prior_spy = _close_before(spy_pts, window_start)
        prior_agg = _close_before(agg_pts, window_start)
        end_spy = _close_on(spy_pts, window_end)
        end_agg = _close_on(agg_pts, window_end)
        if prior_spy is None or prior_agg is None or end_spy is None or end_agg is None:
            pending += 1
            continue
        ret_spy = end_spy / prior_spy - 1.0
        ret_agg = end_agg / prior_agg - 1.0
        divergence = ret_spy - ret_agg
        if divergence > 1e-9:
            actual_dir = "sell_equity_buy_bond"
        elif divergence < -1e-9:
            actual_dir = "buy_equity_sell_bond"
        else:
            actual_dir = "flat"
        resolved.append({
            "window_start": window_start, "window_end": window_end,
            "pred_dir": direction_pred, "actual_dir": actual_dir,
            "window_ret_spy_pct": rnd(ret_spy * 100, 3),
            "window_ret_agg_pct": rnd(ret_agg * 100, 3),
            "divergence_pct": rnd(divergence * 100, 3),
            "hit": bool(direction_pred == actual_dir),
        })

    rolling = resolved[-MONTH_END_ROLLING_N:]
    n = len(rolling)
    hits = sum(1 for r in rolling if r["hit"])
    status, hit_rate, p_value = _status_from_binom(n, hits, MONTH_END_ROLLING_N)
    status_label = {
        "yellow": f"樣本累積中（{n}／需 {MONTH_END_ROLLING_N}）——月頻更新，約需 2 年才足量",
        "green": "健康：命中率統計上顯著優於擲硬幣",
        "red": "kill 門檻觸發：命中率與擲硬幣無統計差異或更差，待校準輪處決",
    }[status]

    return {
        "status": status,
        "status_label": status_label,
        "n_samples": n,
        "n_required": MONTH_END_ROLLING_N,
        "hits": hits,
        "hit_rate": hit_rate,
        "p_value": p_value,
        "significance_alpha": SIGNIFICANCE_ALPHA,
        "n_pending_resolution": pending,
        "recent_samples": rolling,
        "kill_condition": MONTH_END_KILL_TEXT,
    }


# ═══════════════════════════════════════════════════════════════════════════
# rv-model 對帳（讀 knowledge/forecast_settlement.json，本檔不重跑 settle）
# ═══════════════════════════════════════════════════════════════════════════

def build_rv_report(gaps):
    base = {
        "n_resolved": 0, "n_required": RV_MIN_RESOLVED_FOR_BSS,
        "raw_brier_mean": None, "bss": None, "base_rate": None,
        "kill_condition": RV_KILL_TEXT,
    }
    if not FORECAST_SETTLEMENT.exists():
        gaps.append("rv-model：knowledge/forecast_settlement.json 不存在（尚未跑過 "
                    "knowledge/settle_forecasts.py），本次以 0 筆計")
        base["status"] = "yellow"
        base["status_label"] = f"樣本累積中（0／需 {RV_MIN_RESOLVED_FOR_BSS}）"
        return base

    data = load_json(FORECAST_SETTLEMENT, {}) or {}
    rows = data.get("rows") or []
    resolved = [r for r in rows if r.get("source") == "rv-model"
               and r.get("status") in ("resolved_yes", "resolved_no")
               and r.get("p") is not None and r.get("outcome") is not None
               and r.get("brier") is not None]
    n = len(resolved)
    base["n_resolved"] = n
    if n == 0:
        base["status"] = "yellow"
        base["status_label"] = f"樣本累積中（0／需 {RV_MIN_RESOLVED_FOR_BSS}）"
        return base

    mean_brier = sum(r["brier"] for r in resolved) / n
    base["raw_brier_mean"] = round(mean_brier, 4)

    if n < RV_MIN_RESOLVED_FOR_BSS:
        base["status"] = "yellow"
        base["status_label"] = f"樣本累積中（{n}／需 {RV_MIN_RESOLVED_FOR_BSS}），只列 raw Brier 不出 BSS"
        return base

    base_rate = sum(r["outcome"] for r in resolved) / n
    brier_clim = base_rate * (1 - base_rate)
    base["base_rate"] = round(base_rate, 4)
    if brier_clim > 0:
        bss = 1 - mean_brier / brier_clim
        base["bss"] = round(bss, 4)
        base["status"] = "green" if bss >= 0 else "red"
        base["status_label"] = ("健康：BSS ≥ 0（優於 climatology 基準）" if bss >= 0
                                else "kill 門檻觸發：BSS < 0（輸給 climatology），待校準輪處決")
    else:
        base["status"] = "yellow"
        base["status_label"] = "climatology 為 0 或 1（分母為 0），無法算 BSS"
    return base


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="flowmap 成績單 — 凍結預測 vs 實際的機械對帳")
    ap.parse_args()

    gaps = []
    fh_rows = load_forecast_history()
    if not fh_rows:
        gaps.append("forecast_history.jsonl 不存在或為空，CTA／月末件本次皆以 0 筆計")

    price_series, price_built_at = load_price_series()

    cta_report = build_cta_report(fh_rows, price_series, gaps)
    month_end_report = build_month_end_report(fh_rows, price_series, gaps)
    rv_report = build_rv_report(gaps)

    forecast_settlement_last_run = None
    if FORECAST_SETTLEMENT.exists():
        forecast_settlement_last_run = (load_json(FORECAST_SETTLEMENT, {}) or {}).get("last_run")

    as_of = fh_rows[-1]["date"] if fh_rows else date.today().isoformat()

    payload = {
        "schema": SCHEMA,
        "as_of": as_of,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "meta": {
            "method_note": "把每日凍結的 flowmap 預測（forecast_history.jsonl）與後續實際資料對帳："
                          "CTA 對 CFTC COT 週度部位變化方向、月末件對生效窗 3 日 SPY−AGG 相對報酬方向、"
                          "rv-model 對 knowledge/forecasts.jsonl 的機械結算 Brier／BSS。本檔只舉旗，"
                          "不自動刪除模組、不自動改動任何 CONFIG——處決與調整一律走校準輪＋rule_ledger"
                          "（設計稿 §F4）。",
            "cot_category_used": COT_CATEGORY_USED,
            "cot_category_reason": COT_CATEGORY_REASON,
            "significance_test": (f"精確二項檢定（雙尾），α={SIGNIFICANCE_ALPHA}"
                                  "（設計稿未指定顯著水準，本檔選定，供持有人於校準輪複審或調整）"),
            "data_asof": {
                "forecast_history_last_date": fh_rows[-1]["date"] if fh_rows else None,
                "forecast_history_n_rows": len(fh_rows),
                "flowmap_prices_built_at": price_built_at,
                "forecast_settlement_last_run": forecast_settlement_last_run,
            },
        },
        "modules": {
            "cta": cta_report,
            "month_end": month_end_report,
            "rv_model": rv_report,
        },
        "gaps": gaps,
    }

    wrote = write_json_if_changed(OUT_JSON, payload)
    info(f"scorecard.json: {'written' if wrote else 'no change'} (as_of={as_of}, "
         f"cta={cta_report['status']}/{cta_report['n_samples']}, "
         f"month_end={month_end_report['status']}/{month_end_report['n_samples']}, "
         f"rv_model={rv_report['status']}/{rv_report['n_resolved']})")


if __name__ == "__main__":
    main()
