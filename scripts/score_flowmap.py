#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score_flowmap.py — flowmap 成績單：凍結預測 vs 實際的機械對帳（v2，設計稿

notes/site-internal/root/_forecast_v2_design_20260902.md §6／§3.3／§3.2）。
判斷已在設計稿凍結，本檔只負責對帳與舉旗——**不刪除任何模組、不調整任何
CONFIG／門檻**；kill 條款觸發時只在輸出標記 🔴，處決一律留給持有人於校準輪
決定。

三個對帳對象
------------
  CTA 模組     ：對 docs/flowmap/data/forecast_history.jsonl 逐日凍結的
                 nearest-flip-level，判斷次一交易日價格是否穿越（用
                 data/flowmap_prices.json 判定）；穿越週依 CFTC COT 報告週界
                 分組（多次穿越取淨向），對帳對象為該市場 COT 淨部位的週變化
                 方向（data/cot_history.json）。樣本定義（週度分組邏輯）沿用
                 v1 不動，決策機制改為 SPRT（見下）。另計「自我一致性」：穿越
                 後重新計算的實際 composite 是否等於凍結時記錄的
                 if_breached_composite（sanity 欄，非 kill 依據）。
  月末件       ：對凍結於生效窗首日的方向，比對生效窗 3 個交易日的實際
                 SPY−AGG 相對報酬方向。樣本定義沿用 v1，決策機制改為 SPRT。
  ledger_sources：逐字複製 knowledge/forecast_settlement.json 的 `sources`
                 摘要（由 knowledge/settle_forecasts.py 產生，本檔不重跑、
                 不重算——A2 只讀不算）。含 rv-model／vix-model／cot-model／
                 tsmom／vrp／dd-verdict／macro-falsifier／sentinel-noise。
  vol_control  ：降為描述器，不評分（無可對帳的公開流量資料，設計稿 §0-4）。

SPRT 序貫檢定（所有 kill 決策的唯一機制，設計稿 §3.3，PREREG 凍結）
-----------------------------------------------------------------------------
CTA／月末件的樣本＝逐週／逐次「命中」序列（hit=True/False，依樣本日期升冪）；
ledger_sources 的 SPRT 由 settle_forecasts.py 算好、本檔逐字讀出。
  H0 命中率 p0=0.50；H1 p1=0.65；α=0.05；β=0.10。
  上界 A=ln((1−β)/α)=ln(18)=2.8904；下界 B=ln(β/(1−α))=ln(0.1/0.95)=−2.2513。
  每樣本 LLR 增量：命中 +ln(0.65/0.50)=+0.26236；未命中 +ln(0.35/0.50)=−0.35667。
  決策：n_eff<20 一律 continue（🟡）；n_eff≥20 且累積 LLR≥A → accept_h1（🟢）；
  ≤B → accept_h0（🔴＝kill 門檻觸發，舉旗待校準輪處決）；否則 continue（🟡）。
  決策一旦落定即**鎖存**（記 decided_at／decided_n，讀上一輪 scorecard.json 取
  得）：之後樣本繼續累計顯示但狀態不變；只有校準輪可重設。
2026-09-02 起本檔移除 α=0.10 固定 n 二項檢定（原因：無法處理反覆偷看，設計稿
§3.3）；改用序貫檢定，CTA／月末件的「rolling window」上限亦一併移除——SPRT
本身就是對全部歷史樣本累計，不需要再另外裁一個滾動視窗。

CTA 對帳的 COT 類別選擇（沿用 v1 判斷，設計稿未變更此段）
-----------------------------------------------------------------------------
data/cot_history.json 由 scripts/build_crowding.py 維護，其 meta.methodology
明文為 legacy futures-only 報告的 net_pct_oi（僅 non-commercial 一種類別，
無 disaggregated report 的 leveraged funds 細分）。本檔因此落在「無 leveraged
funds 則用 non-commercial」分支，非本檔自行選擇——已寫入輸出 meta 供稽核。

multiplicity（多重比較揭露，設計稿 §3.3 揭露義務／§6）
-----------------------------------------------------------------------------
每次輸出附「同時受檢 source／模組數」與「預期假綠數＝數目 × α」；不做 BH 校
正（序貫檢定不適用），以哨兵（sentinel-noise）為經驗對照。

輸出
----
  docs/flowmap/data/scorecard.json（schema="flowmap-scorecard-v2"，zero-churn
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

SCHEMA = "flowmap-scorecard-v2"

# ═══════════════════════════════════════════════════════════════════════════
# CONFIG — PREREG 凍結（設計稿 §3.3／§A6／§E2；SPRT 常數不得依單一案例調參）。
# ═══════════════════════════════════════════════════════════════════════════

SPRT_P0 = 0.5
SPRT_P1 = 0.65
SPRT_ALPHA = 0.05
SPRT_BETA = 0.10
SPRT_A = 2.8904          # ln((1-beta)/alpha) = ln(18)
SPRT_B = -2.2513         # ln(beta/(1-alpha)) = ln(0.1/0.95)
SPRT_LLR_HIT = 0.26236   # ln(0.65/0.50)
SPRT_LLR_MISS = -0.35667  # ln(0.35/0.50)
SPRT_N_EFF_FLOOR = 20

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
    "report 的 leveraged funds 細分——依設計稿優先序「無 leveraged funds 則用 "
    "non-commercial」，本檔落在此分支，非本檔自行選擇。"
)

CTA_KILL_TEXT = (
    "SPRT（p0=0.5／p1=0.65／α=0.05／β=0.10，n_eff≥20，樣本＝frozen_forecast 與 "
    "CFTC COT 週度部位變化方向逐週命中序列）累積 LLR ≤ B(-2.2513) → accept_h0 "
    "→ 模組降級為 gaps 或刪除（2026-09-02 由固定 n 二項檢定改列 SPRT，處理反覆"
    "偷看，設計稿 §3.3）"
)
MONTH_END_KILL_TEXT = (
    "SPRT（p0=0.5／p1=0.65／α=0.05／β=0.10，n_eff≥20，樣本＝逐次月末方向對帳"
    "命中序列）累積 LLR ≤ B(-2.2513) → accept_h0 → 模組降級為 gaps 或刪除（月頻"
    "樣本慢，約需 2 年才足量；2026-09-02 由 α=0.10 精確二項檢定改列 SPRT，設計稿 "
    "§3.3）"
)

VOL_CONTROL_BLOCK = {
    "status": "descriptor",
    "status_label": "描述器，不評分（無可對帳的公開流量資料）",
}

# 白話名（首現括號原名，設計稿 §6）——供 HTML／其他消費者共用同一份對照表。
SOURCE_LABEL = {
    "rv-model": "波動率模型",
    "vix-model": "VIX 期限結構模型",
    "cot-model": "COT 極端部位模型",
    "tsmom": "趨勢方向模型",
    "vrp": "波動風險溢酬模型",
    "dd-verdict": "個股裁決",
    "macro-falsifier": "總經證偽表",
    "sentinel-noise": "哨兵（無技巧對照組）",
}
SENTINEL_KEY = "sentinel-noise"


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
# SPRT 序貫檢定（設計稿 §3.3，PREREG 凍結——不得改常數／不得改決策規則）
# ═══════════════════════════════════════════════════════════════════════════

def sprt_compute(hit_seq):
    """hit_seq：依樣本日期升冪排序的 bool 序列（True=命中）。回傳 §3.2 schema
    的 sprt 子物件（不含 decided_at／decided_n——那兩欄由 sprt_with_latch 依
    上一輪 scorecard.json 補上，本函式只算「這次重新從頭累計會是什麼狀態」）。
    """
    llr = 0.0
    for h in hit_seq:
        llr += SPRT_LLR_HIT if h else SPRT_LLR_MISS
    n_used = len(hit_seq)
    if n_used < SPRT_N_EFF_FLOOR:
        state = "continue"
    elif llr >= SPRT_A:
        state = "accept_h1"
    elif llr <= SPRT_B:
        state = "accept_h0"
    else:
        state = "continue"
    return {
        "p0": SPRT_P0, "p1": SPRT_P1, "alpha": SPRT_ALPHA, "beta": SPRT_BETA,
        "A": SPRT_A, "B": SPRT_B,
        "llr": round(llr, 5), "n_used": n_used, "state": state,
    }


def sprt_with_latch(hit_seq, prior_sprt):
    """套用鎖存語意：若上一輪 scorecard.json 該模組已 accept_h1／accept_h0，
    狀態與 decided_at／decided_n 維持上一輪的值不變（樣本仍重新累計顯示 llr／
    n_used，只是不再改變 state）；否則用這次算出的新狀態，若新狀態剛好落定，
    記今天為 decided_at。"""
    fresh = sprt_compute(hit_seq)
    prior_state = (prior_sprt or {}).get("state")
    if prior_state in ("accept_h1", "accept_h0"):
        fresh["state"] = prior_state
        fresh["decided_at"] = (prior_sprt or {}).get("decided_at")
        fresh["decided_n"] = (prior_sprt or {}).get("decided_n")
    elif fresh["state"] in ("accept_h1", "accept_h0"):
        fresh["decided_at"] = date.today().isoformat()
        fresh["decided_n"] = fresh["n_used"]
    else:
        fresh["decided_at"] = None
        fresh["decided_n"] = None
    return fresh


SPRT_STATE_TO_STATUS = {"accept_h1": "green", "accept_h0": "red", "continue": "yellow"}


def sprt_status_label(status, sprt, n_eff):
    if status == "yellow":
        if n_eff < SPRT_N_EFF_FLOOR:
            return f"證據累積中：有效樣本 {n_eff}／需先滿 {SPRT_N_EFF_FLOOR} 筆才開始判定"
        return (f"證據累積中：有效樣本 {n_eff}，累積 LLR={sprt['llr']}"
                f"（判綠需 ≥{sprt['A']}，判紅需 ≤{sprt['B']}）")
    if status == "green":
        return f"已證實優於基準（SPRT accept_h1，判定於 {sprt.get('decided_at') or '—'}，n={sprt.get('decided_n')}）"
    return (f"已證實不優於基準（SPRT accept_h0），等校準輪處決"
            f"（判定於 {sprt.get('decided_at') or '—'}，n={sprt.get('decided_n')}）")


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


def build_cta_report(fh_rows, price_series, gaps, prior_sprt):
    events, consistency = _detect_cta_breaches(fh_rows, price_series, gaps)
    samples = _aggregate_cta_weekly(events, gaps)  # 已升冪排序，SPRT 用全部歷史累計，不裁滾動視窗

    hit_seq = [s["hit"] for s in samples]
    n_eff = len(hit_seq)
    hits = sum(1 for h in hit_seq if h)
    hit_rate = rnd(hits / n_eff, 3) if n_eff else None

    sprt = sprt_with_latch(hit_seq, prior_sprt)
    status = SPRT_STATE_TO_STATUS[sprt["state"]]
    status_label = sprt_status_label(status, sprt, n_eff)

    consistency_rate = rnd(consistency["consistent"] / consistency["n"], 3) if consistency["n"] else None

    return {
        "status": status,
        "status_label": status_label,
        "n_eff": n_eff,
        "n_required": SPRT_N_EFF_FLOOR,
        "hits": hits,
        "hit_rate": hit_rate,
        "sprt": sprt,
        "self_consistency": {
            "n": consistency["n"],
            "consistent": consistency["consistent"],
            "rate": consistency_rate,
            "mismatches": consistency["mismatches"],
        },
        "cot_category_used": COT_CATEGORY_USED,
        "recent_samples": samples[-20:],
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


def build_month_end_report(fh_rows, price_series, gaps, prior_sprt):
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

    # SPRT 用全部歷史累計，不裁滾動視窗（resolved 已依 as_of 升冪串接）
    hit_seq = [r["hit"] for r in resolved]
    n_eff = len(hit_seq)
    hits = sum(1 for h in hit_seq if h)
    hit_rate = rnd(hits / n_eff, 3) if n_eff else None

    sprt = sprt_with_latch(hit_seq, prior_sprt)
    status = SPRT_STATE_TO_STATUS[sprt["state"]]
    status_label = sprt_status_label(status, sprt, n_eff)
    if status == "yellow":
        status_label += "——月頻更新，約需 2 年才足量"

    return {
        "status": status,
        "status_label": status_label,
        "n_eff": n_eff,
        "n_required": SPRT_N_EFF_FLOOR,
        "hits": hits,
        "hit_rate": hit_rate,
        "sprt": sprt,
        "n_pending_resolution": pending,
        "recent_samples": resolved[-20:],
        "kill_condition": MONTH_END_KILL_TEXT,
    }


# ═══════════════════════════════════════════════════════════════════════════
# ledger_sources（逐字複製 knowledge/forecast_settlement.json 的 sources 摘要
# ——A2 只讀不算，SPRT／BSS 由 knowledge/settle_forecasts.py 算好）
# ═══════════════════════════════════════════════════════════════════════════

def load_ledger_sources(gaps):
    if not FORECAST_SETTLEMENT.exists():
        gaps.append("ledger_sources：knowledge/forecast_settlement.json 不存在"
                    "（尚未跑過 knowledge/settle_forecasts.py），本次以空集合計")
        return {}
    data = load_json(FORECAST_SETTLEMENT, {}) or {}
    sources = data.get("sources")
    if not sources:
        gaps.append("ledger_sources：knowledge/forecast_settlement.json 尚無 "
                    "sources 欄位（帳簿仍是 v1 舊格式或尚未產生），本次以空集合計，"
                    "待帳簿升級 v2 後自動補上")
        return {}
    return sources


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

    prior = load_json(OUT_JSON, {}) or {}
    prior_modules = prior.get("modules") or {}
    prior_cta_sprt = (prior_modules.get("cta") or {}).get("sprt")
    prior_month_end_sprt = (prior_modules.get("month_end") or {}).get("sprt")

    cta_report = build_cta_report(fh_rows, price_series, gaps, prior_cta_sprt)
    month_end_report = build_month_end_report(fh_rows, price_series, gaps, prior_month_end_sprt)
    ledger_sources = load_ledger_sources(gaps)

    n_sprt_modules = 2  # cta, month_end
    n_tested = n_sprt_modules + len([k for k in ledger_sources if k != SENTINEL_KEY])
    multiplicity = {
        "n_tested": n_tested,
        "alpha": SPRT_ALPHA,
        "expected_false_green": round(n_tested * SPRT_ALPHA, 3),
    }

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
                          "CTA 對 CFTC COT 週度部位變化方向、月末件對生效窗 3 日 SPY−AGG 相對報酬方向，"
                          "決策一律走 SPRT 序貫檢定；ledger_sources 為 knowledge/forecasts.jsonl 全部"
                          "predictor 的機械結算摘要（逐字複製，本檔不重算）。本檔只舉旗，不自動刪除"
                          "模組、不自動改動任何 CONFIG——處決與調整一律走校準輪＋rule_ledger。",
            "cot_category_used": COT_CATEGORY_USED,
            "cot_category_reason": COT_CATEGORY_REASON,
            "sprt_note": ("決策機制＝SPRT 序貫檢定（p0=0.5／p1=0.65／α=0.05／β=0.10，n_eff≥20 才開始判定；"
                         "2026-09-02 由固定 n 二項檢定改列，設計稿 §3.3）。真實技巧 60% 時預期約需 200 樣本"
                         "才判綠，完全無技巧時預期約 50 樣本即判紅——判紅遠快於判綠是序貫檢定的設計特性，"
                         "不是門檻不對稱的錯誤。"),
            "multiplicity": multiplicity,
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
        },
        "vol_control": VOL_CONTROL_BLOCK,
        "ledger_sources": ledger_sources,
        "gaps": gaps,
    }

    wrote = write_json_if_changed(OUT_JSON, payload)
    info(f"scorecard.json: {'written' if wrote else 'no change'} (as_of={as_of}, "
         f"cta={cta_report['status']}/{cta_report['n_eff']}, "
         f"month_end={month_end_report['status']}/{month_end_report['n_eff']}, "
         f"ledger_sources={len(ledger_sources)})")


if __name__ == "__main__":
    main()
