#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_exposure_track.py — 市況曝險規則 v0（paper track）機械建構器。

WHAT THIS IS
------------
市況主控台（market cockpit）合成層下的一條機械化目標曝險 paper track——三因子
（波動 vol／趨勢 trend／信用 credit）合成一個 0.25–1.0 的目標曝險，週頻（週五收
盤算、週一生效）記一本 NAV 帳，對兩個基準（SPY buy-and-hold；60/40 SPY/AGG 月初
再平衡）打分，月樣本走 SPRT 序貫檢定淘汰賽。**不是收斂面**：不產名單、不進
picks/GRP/三軌/cockpit 任何清單，不得被引用為個股或資產配置依據；描述器紀
律——公開頁只講機率與條件、不下買賣指令。上線即 paper 記分，SPRT 判綠前只顯
示不執行；判紅即撤（見 PREREG kill_conditions，下同）。

FROZEN SPEC（設計稿 2026-09-02 §4，PREREG 凍結至判決或 24 個月——本檔只實作，
不得調參；完整逐字條文見下 PREREG dict，同時原樣寫入輸出 JSON 供稽核）
--------------------------------------------------------------------------
Cadence    : 週頻，每週六 weekly-market-update 班車以週五收盤算，週一生效；
             inception 2026-09-07，NAV=100。
Data       : SPY／AGG 日線 = data/flowmap_prices.json（唯讀，本檔不寫入）；
             HY OAS 21 交易日變化 = docs/monitor/data/latest.json hy_oas
             spark（最近 30 個交易日值，百分點）。
Factors    : vol = clip(0.15 / RV_blend, 0.25, 1.0)，RV_blend = 0.5×RV21 +
             0.5×RV63（SPY 日對數報酬年化 %，口徑逐字同
             scripts/build_rv_base_rates.py：21／63 交易日日對數報酬
             sample std〔ddof=1〕× sqrt(252) × 100，單位＝vol 點）。
             trend = 1.0 若 SPY 12-1 動能（t-252 至 t-21 總報酬）> 0，否則
             0.5（口徑逐字同 scripts/build_trend_track.py 的
             c.iloc[-22]/c.iloc[-253]-1）。
             credit = 0.5 若 HY OAS 近 21 交易日上升 > 0.50 個百分點，否則
             1.0。
Target     : 目標曝險 = clip(vol × trend × credit, 0.25, 1.0)；其餘現金 0%
             （不計息，同 trend-track 的現金 slot 慣例）。
Benchmarks : SPY buy-and-hold（inception 當日買入，永不再平衡）；60/40
             （SPY／AGG，月初再平衡——沿用 build_trend_track.py 的
             last_rebalance_month 慣例，判定＝本次執行的效力週一所在日曆
             月 ≠ 上次 rebalance 月份）。
Gates      : core 恆「open」；satellite_structural：目標曝險 ≥ 0.5 →
             「open」否則「caution」；satellite_cyclical：trend=1.0 且
             credit=1.0 且 RV21 < 19.93（rv 表 Q5 切點，來源見下）→「open」
             否則「closed」。三軌新倉閘寫進本檔，PM／各判讀 skill 讀為輸入
             之一，非指令。
Scoring    : 月樣本 = 當月 paper 報酬 − SPY B&H 報酬 > 0 為命中；SPRT 同
             forecast ledger v2 §3.3 參數（p0=0.5／p1=0.65／α=0.05／
             β=0.10，A=2.8904，B=-2.2513，n_eff floor 20，決策落定即鎖
             存）；另列 Sharpe／MaxDD 對兩基準（資訊欄，≥3 個月才計算，不
             做決策）。
Kill       : SPRT accept_h0 → 規則撤下、三軌新倉閘回「僅顯示無規則」；期
             間不調參；paper only 永不連實倉。

RV21 < 19.93 常數來源（PREREG，非本檔即時重算）
--------------------------------------------------------------------------
data/rv_base_rates.json 的 quintile_cutoffs_pct20_40_60_80[3]（Q4/Q5 分
界，built_at 2026-09-01T23:51:11Z 快照）。凍結為常數是刻意的：本規則的
gate 門檻不應隨每次 rv-model 重建 base rate 表而漂移（PREREG 精神同 rv 表
本身的五分位切點）。

vol 因子單位換算（設計稿字面寫 0.15 / RV_blend，本檔顯性註記避免誤讀）
--------------------------------------------------------------------------
σ_target 帳面寫作 0.15（15% 年化波動目標），RV_blend 依 rv-model 慣例輸出
成「vol 點」（年化百分比數字，如 14.08 代表 14.08%）。兩者必須同單位相
除，否則 0.15 除以兩位數字會恆等於下限 0.25、gate 永遠鎖死。本檔採
clip(15.0 / RV_blend_vol_points, 0.25, 1.0)——與 clip(0.15 /
(RV_blend_vol_points/100), 0.25, 1.0) 數學等價，只是把單位換算寫顯性。

SPRT 序貫檢定 — 復用 scripts/score_flowmap.py 的既有實作（非另開一份可
能漂移的複製邏輯；score_flowmap.py 頂層只有 stdlib 匯入，安全 import）
--------------------------------------------------------------------------
sprt_compute() / sprt_with_latch() / SPRT_STATE_TO_STATUS /
sprt_status_label() 四個函式與常數逐字沿用，鎖存語意（decided_at／
decided_n 只有校準輪可重設）完全相同。

RV21／RV63 計算 — 復用 scripts/build_rv_base_rates.py 的
compute_rv21_by_index()（window 參數化支援 21 與 63 兩窗），避免另開一份
可能漂移的年化 sample-std 複製邏輯。

FAIL-SAFE（鏡射 build_trend_track.py／build_flowmap.py）
--------------------------------------------------------------------------
SPY 價格序列為空、或可用收盤數 < 253（12-1 動能所需最低長度）→ 印警告、
exit 0、exposure_track.json 完全不動。任何未捕捉例外同樣 exit 0 不落盤。

PRE-INCEPTION 行為
--------------------------------------------------------------------------
若執行當下（系統日期）早於 INCEPTION_DATE（2026-09-07），本檔仍寫
prereg／as_of／factors_history（供事前檢視三因子與閘是否合理），但
nav_series 留空並在 data_gaps 記一筆說明——NAV 簿記要到 inception 才起
算，不得在此之前捏造報酬。

Runs in the weekly-market-update GitHub Actions workflow, right after the
Trend-Track (TSMOM) step.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FLOWMAP_PRICES = DATA / "flowmap_prices.json"
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
OUT_JSON = ROOT / "docs" / "market" / "data" / "exposure_track.json"

sys.path.insert(0, str(ROOT / "scripts"))
import build_rv_base_rates as _rv  # noqa: E402  (top-level imports stdlib-only; reuse RV21/RV63 calc)
import score_flowmap as _sf  # noqa: E402  (top-level imports stdlib-only; reuse SPRT helper + latch)

SCHEMA = "exposure-track-v0"

# ═══════════════════════════════════════════════════════════════════════
# CONFIG — PREREG 凍結（設計稿 §4；不得依單一案例調參）
# ═══════════════════════════════════════════════════════════════════════

INCEPTION_DATE = "2026-09-07"

SIGMA_TARGET_VOL_POINTS = 15.0   # σ_target=0.15（帳面 15%）換算成 vol 點單位，見上 docstring
VOL_CLIP = (0.25, 1.0)
TARGET_CLIP = (0.25, 1.0)
CREDIT_HY_OAS_RISE_THRESHOLD_PP = 0.50
RV21_CYCLICAL_GATE_CUTOFF = 19.93  # data/rv_base_rates.json quintile_cutoffs_pct20_40_60_80[3]（Q4/Q5），PREREG 常數
RV_WINDOW_21 = 21
RV_WINDOW_63 = 63
MOM_FAR_IDX = -253   # ~12 個月前（同 build_trend_track.py FAR_IDX）
MOM_NEAR_IDX = -22   # ~1 個月前（同 build_trend_track.py NEAR_IDX）
MIN_CLOSES_FOR_MOM = 253

BH_WEIGHT_SPY = 0.6
BH_WEIGHT_AGG = 0.4

EXPOSURE_KILL_TEXT = (
    "SPRT（p0=0.5／p1=0.65／α=0.05／β=0.10，n_eff≥20，樣本＝逐月「當月 paper 報酬 − "
    "SPY B&H 報酬 > 0」命中序列）累積 LLR ≤ B(-2.2513) → accept_h0 → 規則撤下、三軌"
    "新倉閘回「僅顯示無規則」；期間不調參；paper only 永不連實倉（設計稿 §4）。"
)

PREREG = {
    "title": "市況曝險規則 v0（paper，PREREG 凍結至判決或 24 個月）",
    "source_doc": "notes/site-internal/root/_market_cockpit_design_20260902.md §4",
    "frozen_date": "2026-09-02",
    "positioning": (
        "本規則是市況主控台（market cockpit）合成層下的機械化目標曝險 paper "
        "track，非收斂面：不產名單、不進 picks/GRP/三軌/cockpit 任何清單，不得"
        "被引用為個股或資產配置依據；描述器紀律——公開頁只講機率與條件、不下"
        "買賣指令。上線即 paper 記分，SPRT 判綠前只顯示不執行；判紅即撤。"
    ),
    "cadence": (
        "週頻：每週六 weekly-market-update 班車以週五收盤算，週一生效；"
        "inception 2026-09-07，NAV=100。"
    ),
    "data_sources": {
        "prices": "SPY／AGG 日線＝data/flowmap_prices.json（唯讀，本檔不寫入）。",
        "credit": "HY OAS 21 交易日變化＝docs/monitor/data/latest.json hy_oas spark（百分點）。",
    },
    "factors": {
        "vol": (
            "vol＝clip(0.15 / RV_blend, 0.25, 1.0)，RV_blend＝0.5×RV21＋0.5×RV63"
            "（SPY 日對數報酬年化 %，口徑同 rv-model）。"
        ),
        "vol_unit_note": (
            "σ_target 0.15（15% 年化波動目標）與 RV_blend（rv-model 慣例，以「vol "
            "點」＝年化百分比數字表示，例如 14.08 代表 14.08%）需同單位相除；本檔"
            "實作為 clip(15.0 / RV_blend_vol_points, 0.25, 1.0)——與寫成 clip(0.15 "
            "/ (RV_blend_vol_points/100), 0.25, 1.0) 數學等價，僅顯性化單位換算，"
            "避免 0.15 除以兩位數 vol 點數字被誤讀成恆等於下限 0.25。"
        ),
        "trend": "trend＝1.0 若 SPY 12-1 動能（t−252 至 t−21 總報酬）> 0，否則 0.5。",
        "credit": "credit＝0.5 若 HY OAS 近 21 交易日上升 > 0.50 個百分點，否則 1.0。",
    },
    "target": {
        "formula": "目標曝險＝clip(vol × trend × credit, 0.25, 1.0)；其餘現金 0%。",
    },
    "benchmarks": {
        "spy_bh": "SPY buy-and-hold（inception 當日買入，永不再平衡）。",
        "b6040": "60/40（SPY／AGG，月初再平衡）。",
    },
    "gates": {
        "core": "core 恆「open」。",
        "satellite_structural": "satellite_structural：目標曝險 ≥ 0.5 →「open」否則「caution」。",
        "satellite_cyclical": (
            "satellite_cyclical：trend=1.0 且 credit=1.0 且 RV21 < 19.93（rv 表 Q5 "
            "切點）→「open」否則「closed」。19.93 來源＝data/rv_base_rates.json "
            "quintile_cutoffs_pct20_40_60_80[3]（Q4/Q5 分界，built_at "
            "2026-09-01T23:51:11Z 快照，PREREG 凍結為常數，非本檔即時重算）。"
        ),
        "note": "三軌新倉閘寫進本檔／state.json，PM 讀為輸入之一，非指令。",
    },
    "scoring": {
        "monthly_sample": "月樣本＝當月 paper 報酬 − SPY B&H 報酬 > 0 為命中。",
        "sprt": (
            "SPRT 同 forecast ledger v2 §3.3 參數：p0=0.5／p1=0.65／α=0.05／"
            "β=0.10，上界 A=ln(18)=2.8904，下界 B=ln(0.1/0.95)=−2.2513，"
            "n_eff<20 一律 continue，決策一旦落定即鎖存（decided_at／"
            "decided_n），只有校準輪可重設。"
        ),
        "info_only": "另列 Sharpe／MaxDD 對兩基準（資訊欄，≥3 個月才計算，不做決策）。",
    },
    "kill_conditions": {
        "kill_1": (
            "SPRT accept_h0 → 規則撤下、三軌新倉閘回「僅顯示無規則」；期間不調"
            "參；paper only 永不連實倉。"
        ),
    },
    "disclosure": (
        "誠實標注：paper track、無交易成本、無滑價、機械式、非投資建議。目標曝"
        "險與三軌新倉閘皆為描述性資訊，PM 與各判讀 skill 讀為輸入之一，非執行"
        "指令。"
    ),
}


class FailSafeAbort(Exception):
    """PREREG'd fail-safe conditions — caught in main() to print a warning
    and exit 0 without touching exposure_track.json."""


def warn(msg):
    print(f"[exposure-track][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[exposure-track] {msg}")


def clip(x, lo, hi):
    return max(lo, min(hi, x))


def month_of(date_str):
    return date_str[:7]


# ═══════════════════════════════════════════════════════════════════════
# I/O
# ═══════════════════════════════════════════════════════════════════════

def load_json(path, default=None):
    if not path.exists():
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        warn(f"could not read {path.name}: {e}")
        return default


def load_price_series():
    data = load_json(FLOWMAP_PRICES, {}) or {}
    series = data.get("series") or {}
    out = {}
    for t, rows in series.items():
        try:
            out[t] = sorted(((d, float(c)) for d, c in rows), key=lambda x: x[0])
        except (TypeError, ValueError):
            out[t] = []
    built_at = (data.get("meta") or {}).get("built_at")
    return out, built_at


def _close_on(series_pts, ymd):
    for d, c in series_pts:
        if d == ymd:
            return c
    return None


def _close_at_or_before(series_pts, ymd):
    best = None
    for d, c in series_pts:
        if d <= ymd:
            best = c
        else:
            break
    return best


def load_hy_oas_item():
    data = load_json(MONITOR_LATEST, {}) or {}
    for cat in data.get("categories") or []:
        for it in cat.get("items") or []:
            if it.get("key") == "hy_oas":
                return it
    return None


# ═══════════════════════════════════════════════════════════════════════
# Factors（設計稿 §4，PREREG 凍結）
# ═══════════════════════════════════════════════════════════════════════

def compute_rv_pair(closes_asc, gaps, as_of):
    """closes_asc：升冪收盤價 float 列表（截至 as_of）。回傳 (rv21, rv63)，
    復用 build_rv_base_rates.compute_rv21_by_index（window 參數化），任一
    None 表資料不足（記 gaps）。"""
    rv21_series = _rv.compute_rv21_by_index(closes_asc, window=RV_WINDOW_21)
    rv63_series = _rv.compute_rv21_by_index(closes_asc, window=RV_WINDOW_63)
    rv21 = rv21_series[-1] if rv21_series else None
    rv63 = rv63_series[-1] if rv63_series else None
    if rv21 is None:
        gaps.append({"date": as_of, "reason": f"RV21 資料不足（需 ≥{RV_WINDOW_21 + 1} 筆收盤）"})
    if rv63 is None:
        gaps.append({"date": as_of, "reason": f"RV63 資料不足（需 ≥{RV_WINDOW_63 + 1} 筆收盤）"})
    return rv21, rv63


def compute_mom_12_1(closes_asc, gaps, as_of):
    """口徑逐字同 scripts/build_trend_track.py：
    ret_12_1 = c.iloc[-22] / c.iloc[-253] − 1。"""
    if len(closes_asc) < MIN_CLOSES_FOR_MOM:
        gaps.append({"date": as_of, "reason": f"12-1 動能資料不足（需 ≥{MIN_CLOSES_FOR_MOM} 筆收盤，"
                                               f"實得 {len(closes_asc)}），trend 因子退回保守值 0.5"})
        return None
    far = closes_asc[MOM_FAR_IDX]
    near = closes_asc[MOM_NEAR_IDX]
    if not far:
        gaps.append({"date": as_of, "reason": "12-1 動能遠端錨為 0/NaN，trend 因子退回保守值 0.5"})
        return None
    return near / far - 1.0


def compute_hy_oas_chg_21td(gaps, as_of):
    """HY OAS 近 21 交易日變化（百分點）＝spark[-1] − spark[-22]（spark 為
    docs/monitor/data/latest.json hy_oas 項目，最近 30 個交易日值）。"""
    item = load_hy_oas_item()
    if not item:
        gaps.append({"date": as_of, "reason": "docs/monitor/data/latest.json 找不到 hy_oas 項目，"
                                               "credit 因子退回保守值 1.0（無資訊時不額外懲罰曝險）"})
        return None, None
    spark = item.get("spark") or []
    if len(spark) < 22:
        gaps.append({"date": as_of, "reason": f"hy_oas spark 長度不足（{len(spark)} < 22），"
                                               "credit 因子退回保守值 1.0"})
        return None, item
    chg = round(spark[-1] - spark[-22], 4)
    if item.get("stale"):
        gaps.append({"date": as_of, "reason": f"hy_oas 標記 stale（as_of={item.get('date')}），"
                                               "本次仍照常使用，僅記錄供稽核"})
    return chg, item


def compute_factors(as_of, spy_closes_asc, gaps):
    rv21, rv63 = compute_rv_pair(spy_closes_asc, gaps, as_of)
    if rv21 is None or rv63 is None:
        return None

    rv_blend = round(0.5 * rv21 + 0.5 * rv63, 4)
    vol = round(clip(SIGMA_TARGET_VOL_POINTS / rv_blend, *VOL_CLIP), 4) if rv_blend else VOL_CLIP[0]

    mom = compute_mom_12_1(spy_closes_asc, gaps, as_of)
    trend = 1.0 if (mom is not None and mom > 0) else 0.5

    hy_chg, hy_item = compute_hy_oas_chg_21td(gaps, as_of)
    credit = 0.5 if (hy_chg is not None and hy_chg > CREDIT_HY_OAS_RISE_THRESHOLD_PP) else 1.0

    target = round(clip(vol * trend * credit, *TARGET_CLIP), 4)

    gates = {
        "core": "open",
        "satellite_structural": "open" if target >= 0.5 else "caution",
        "satellite_cyclical": ("open" if (trend == 1.0 and credit == 1.0 and rv21 < RV21_CYCLICAL_GATE_CUTOFF)
                                else "closed"),
    }

    return {
        "date": as_of,
        "rv21": rv21,
        "rv63": rv63,
        "rv_blend": rv_blend,
        "vol": vol,
        "mom_12_1": round(mom * 100, 4) if mom is not None else None,  # 百分點，與 rv21/rv63/hy_oas_chg_21td 同單位慣例
        "trend": trend,
        "hy_oas_chg_21td": hy_chg,
        "hy_oas_asof": hy_item.get("date") if hy_item else None,
        "credit": credit,
        "target": target,
        "gates": gates,
    }


# ═══════════════════════════════════════════════════════════════════════
# NAV 簿記 — paper 線與兩個基準（週頻，設計稿 §4）
# ═══════════════════════════════════════════════════════════════════════

def next_monday_after(d):
    """回傳嚴格晚於 d 的下一個週一（週五收盤 +3 天＝下週一，符合「週五收盤
    算、週一生效」）。"""
    days_ahead = 7 - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)


def build_inception_b6040(spy_px, agg_px, effective_date_str):
    nav = 100.0
    units = {"SPY": (nav * BH_WEIGHT_SPY) / spy_px, "AGG": (nav * BH_WEIGHT_AGG) / agg_px}
    return {"units": units, "cash": 0.0, "last_rebalance_month": month_of(effective_date_str)}, nav


def mark_to_market_b6040(state, spy_px, agg_px):
    u = state["units"]
    return u["SPY"] * spy_px + u["AGG"] * agg_px + state.get("cash", 0.0)


def update_b6040(state, spy_px, agg_px, effective_date_str):
    nav_pre = mark_to_market_b6040(state, spy_px, agg_px)
    this_month = month_of(effective_date_str)
    if this_month != state.get("last_rebalance_month"):
        state["units"] = {"SPY": (nav_pre * BH_WEIGHT_SPY) / spy_px, "AGG": (nav_pre * BH_WEIGHT_AGG) / agg_px}
        state["last_rebalance_month"] = this_month
    return nav_pre  # 再平衡不含成本，總值不變


def build_nav_row(effective_date, as_of, nav_paper, nav_spy_bh, nav_b6040, spy_px, agg_px, target_now):
    return {
        "date": effective_date, "as_of": as_of,
        "nav": round(nav_paper, 4), "spy_bh": round(nav_spy_bh, 4), "b6040": round(nav_b6040, 4),
        "spy_close": round(spy_px, 4), "agg_close": round(agg_px, 4),
        "target": target_now,  # 本列 as_of 算出的目標曝險，適用於「下一段」（到下次生效週一為止）
    }


def update_nav(state, as_of, spy_px, agg_px, target_now, gaps):
    """冪等的週頻 NAV 更新：
      - 首次啟動（nav_series 空）＝inception，NAV 全部 =100，本列 target 供下一段使用。
      - 若本次算出的「生效週一」與最後一列相同＝同段重跑，就地覆蓋（不重複
        append、不重複套用報酬）。
      - 若生效週一晚於最後一列＝新的一段，用「最後一列當時算出的 target」對
        這段的 SPY 報酬打分（paper 線），60/40 走月度再平衡簿記，SPY B&H 單
        純跟收盤價。
    """
    nav_series = state.setdefault("nav_series", [])
    bk = state.setdefault("_bookkeeping", {})

    eff = next_monday_after(date.fromisoformat(as_of)).isoformat()
    eff = max(eff, INCEPTION_DATE)  # inception 是凍結日期，首段生效日不得早於它

    if not nav_series:
        b6040_state, _ = build_inception_b6040(spy_px, agg_px, eff)
        row = build_nav_row(eff, as_of, 100.0, 100.0, 100.0, spy_px, agg_px, target_now)
        nav_series.append(row)
        bk["spy_close_inception"] = spy_px
        bk["b6040"] = b6040_state
        info(f"    inception booked: date={eff} (as_of={as_of}) nav=100/100/100")
        return

    last = nav_series[-1]
    if eff == last["date"]:
        # 同段重跑：以「上一段收尾（nav_series[-2] 或無則維持 100）」為基礎，
        # 用上一段的 target 重算本段報酬，就地覆蓋，不二次套用。
        prior = nav_series[-2] if len(nav_series) >= 2 else None
        prior_nav_paper = prior["nav"] if prior else 100.0
        prior_nav_spy = prior["spy_bh"] if prior else 100.0
        prior_target = prior["target"] if prior else target_now
        prior_spy_px = prior["spy_close"] if prior else bk.get("spy_close_inception", spy_px)
        spy_ret = spy_px / prior_spy_px - 1.0
        nav_paper = prior_nav_paper * (1.0 + prior_target * spy_ret)
        nav_spy_bh = nav_spy_bh_calc(bk.get("spy_close_inception", spy_px), spy_px)
        nav_b6040 = update_b6040(bk["b6040"], spy_px, agg_px, eff) if bk.get("b6040") else prior_nav_paper
        nav_series[-1] = build_nav_row(eff, as_of, nav_paper, nav_spy_bh, nav_b6040, spy_px, agg_px, target_now)
        info(f"    same-period rerun overwritten in place: date={eff} (as_of={as_of})")
        return

    # 新的一段：套用上一列的 target 到這段的 SPY 報酬
    prior_target = last["target"]
    prior_spy_px = last["spy_close"]
    spy_ret = spy_px / prior_spy_px - 1.0
    nav_paper = last["nav"] * (1.0 + prior_target * spy_ret)
    nav_spy_bh = nav_spy_bh_calc(bk.get("spy_close_inception", prior_spy_px), spy_px)
    nav_b6040 = update_b6040(bk["b6040"], spy_px, agg_px, eff)
    nav_series.append(build_nav_row(eff, as_of, nav_paper, nav_spy_bh, nav_b6040, spy_px, agg_px, target_now))
    info(f"    new period booked: date={eff} (as_of={as_of}) target_applied={prior_target} spy_ret={spy_ret:+.4%}")


def nav_spy_bh_calc(spy_close_inception, spy_px):
    return 100.0 * spy_px / spy_close_inception


# ═══════════════════════════════════════════════════════════════════════
# SPRT 序貫檢定（復用 scripts/score_flowmap.py，見檔頭說明）
# ═══════════════════════════════════════════════════════════════════════

def compute_monthly_samples(nav_series):
    """依 as_of（週五收盤所屬月份，非生效週一）分桶，桶內取最後一列；最後
    一個月視為「進行中」不計分（本月尚未走完，不能宣稱月末報酬），其餘相
    鄰兩個完整月的桶算「當月 paper 報酬 − SPY B&H 報酬 > 0」為命中。刻意
    用 as_of 而非 date（生效週一）分月——月底最後一個週五的生效週一可能跨
    入下個月（如 10/30 週五 → 生效 11/02 週一），若用生效日分桶會把該週的
    市場報酬錯記到下個月，造成月度歸因系統性偏移。"""
    by_month = {}
    order = []
    for row in nav_series:
        m = month_of(row["as_of"])
        if m not in by_month:
            order.append(m)
        by_month[m] = row  # 保留該月最後一列
    closed_months = order[:-1] if len(order) >= 1 else []
    samples = []
    for i in range(1, len(closed_months)):
        m_prev, m_cur = closed_months[i - 1], closed_months[i]
        row_prev, row_cur = by_month[m_prev], by_month[m_cur]
        ret_paper = row_cur["nav"] / row_prev["nav"] - 1.0
        ret_spy = row_cur["spy_bh"] / row_prev["spy_bh"] - 1.0
        hit = (ret_paper - ret_spy) > 1e-12
        samples.append({
            "month": m_cur,
            "ret_paper_pct": round(ret_paper * 100, 4),
            "ret_spy_bh_pct": round(ret_spy * 100, 4),
            "hit": bool(hit),
        })
    return samples, len(closed_months)


def build_sprt_block(nav_series, prior_sprt):
    samples, n_closed_months = compute_monthly_samples(nav_series)
    hit_seq = [s["hit"] for s in samples]
    sprt = _sf.sprt_with_latch(hit_seq, prior_sprt)
    status = _sf.SPRT_STATE_TO_STATUS[sprt["state"]]
    status_label = _sf.sprt_status_label(status, sprt, len(hit_seq))
    return {
        **sprt,
        "status": status,
        "status_label": status_label,
        "n_required": _sf.SPRT_N_EFF_FLOOR,
        "samples": samples,
        "n_closed_months": n_closed_months,
        "kill_condition": EXPOSURE_KILL_TEXT,
    }


# ═══════════════════════════════════════════════════════════════════════
# Sharpe／MaxDD（資訊欄，≥3 個完整月才算，設計稿 §4）
# ═══════════════════════════════════════════════════════════════════════

def _monthly_returns(nav_series, key, n_closed_months):
    """月份分桶依 as_of（同 compute_monthly_samples），理由同上。"""
    by_month = {}
    order = []
    for row in nav_series:
        m = month_of(row["as_of"])
        if m not in by_month:
            order.append(m)
        by_month[m] = row
    closed = order[:n_closed_months]
    rets = []
    for i in range(1, len(closed)):
        v_prev = by_month[closed[i - 1]][key]
        v_cur = by_month[closed[i]][key]
        rets.append(v_cur / v_prev - 1.0)
    return rets


def _sharpe_annualized(monthly_rets):
    n = len(monthly_rets)
    if n < 2:
        return None
    mean = sum(monthly_rets) / n
    var = sum((x - mean) ** 2 for x in monthly_rets) / (n - 1)
    sd = var ** 0.5
    if sd == 0:
        return None
    return round((mean / sd) * math.sqrt(12), 4)


def _max_drawdown_pct(values):
    peak = None
    mdd = 0.0
    for v in values:
        if peak is None or v > peak:
            peak = v
        dd = (v / peak - 1.0) if peak else 0.0
        if dd < mdd:
            mdd = dd
    return round(mdd * 100, 4)


def build_stats_block(nav_series, n_closed_months):
    if n_closed_months < 3:
        return None
    out = {"n_months": n_closed_months, "note": "資訊欄，不做決策；決策唯一機制為月樣本 SPRT（見 sprt 區）。"}
    for label, key in (("paper", "nav"), ("spy_bh", "spy_bh"), ("b6040", "b6040")):
        rets = _monthly_returns(nav_series, key, n_closed_months)
        values = [row[key] for row in nav_series]
        out[label] = {
            "sharpe_annualized": _sharpe_annualized(rets),
            "max_dd_pct": _max_drawdown_pct(values),
        }
    return out


# ═══════════════════════════════════════════════════════════════════════
# Main build
# ═══════════════════════════════════════════════════════════════════════

def build():
    gaps = []

    price_series, price_built_at = load_price_series()
    spy_series = price_series.get("SPY") or []
    agg_series = price_series.get("AGG") or []
    if not spy_series:
        raise FailSafeAbort("SPY price series empty (data/flowmap_prices.json) — cannot compute any factor")

    as_of = spy_series[-1][0]
    spy_closes_asc = [c for _, c in spy_series if _ <= as_of]
    if len(spy_closes_asc) < RV_WINDOW_63 + 1:
        raise FailSafeAbort(f"only {len(spy_closes_asc)} SPY closes available — below RV63 minimum "
                             f"({RV_WINDOW_63 + 1})")

    spy_px = spy_closes_asc[-1]
    agg_px = _close_at_or_before(agg_series, as_of)
    if agg_px is None:
        gaps.append({"date": as_of, "reason": "AGG 收盤在 as_of 或之前查無資料，60/40 基準本次跳過更新"})

    factors_row = compute_factors(as_of, spy_closes_asc, gaps)
    if factors_row is None:
        raise FailSafeAbort("RV21/RV63 均無法計算（資料不足），無法產出本週因子列")

    info(f"as_of={as_of}  rv21={factors_row['rv21']}  rv63={factors_row['rv63']}  "
         f"rv_blend={factors_row['rv_blend']}  vol={factors_row['vol']}  "
         f"mom_12_1={factors_row['mom_12_1']}%  trend={factors_row['trend']}  "
         f"hy_oas_chg_21td={factors_row['hy_oas_chg_21td']}  credit={factors_row['credit']}  "
         f"target={factors_row['target']}  gates={factors_row['gates']}")

    state = load_json(OUT_JSON, {}) or {}
    prior_sprt = state.get("sprt")

    factors_history = state.get("factors_history") or []
    if factors_history and factors_history[-1]["date"] == as_of:
        factors_history[-1] = factors_row
    else:
        factors_history.append(factors_row)

    today = date.today()
    is_pre_inception = today.isoformat() < INCEPTION_DATE

    nav_state = {"nav_series": state.get("nav_series") or [], "_bookkeeping": state.get("_bookkeeping") or {}}

    if is_pre_inception:
        gaps.append({
            "date": as_of,
            "reason": (f"pre-inception：今日（{today.isoformat()}）< inception_date（{INCEPTION_DATE}），"
                       "NAV 簿記尚未起算，本次僅寫入 factors_history 供事前檢視，不捏造 nav_series。"),
        })
        info(f"    pre-inception（today={today.isoformat()} < inception={INCEPTION_DATE}）— "
             "nav_series 留空，不起 NAV 簿記")
    elif agg_px is not None:
        update_nav(nav_state, as_of, spy_px, agg_px, factors_row["target"], gaps)
    else:
        gaps.append({"date": as_of, "reason": "AGG 價格缺失，本次跳過 NAV 更新（不用陳舊價格捏造 60/40）"})

    nav_series = nav_state["nav_series"]
    sprt_block = build_sprt_block(nav_series, prior_sprt)
    _, n_closed_months = compute_monthly_samples(nav_series)
    stats_block = build_stats_block(nav_series, n_closed_months)

    out = {
        "schema": SCHEMA,
        "prereg": PREREG,
        "as_of": as_of,
        "inception_date": INCEPTION_DATE,
        "factors_history": factors_history,
        "nav_series": nav_series,
        "sprt": sprt_block,
        "stats": stats_block,
        "data_gaps": gaps,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_bookkeeping": nav_state["_bookkeeping"] if nav_series else None,
        "meta": {
            "flowmap_prices_built_at": price_built_at,
            "note": ("三因子與 NAV 簿記逐週由本檔重算；factors_history／nav_series 依日期冪等覆蓋，"
                     "不重複 append。'_bookkeeping' 為簿記內部狀態（60/40 units／現金／上次再平衡月份），"
                     "非 §4 凍結輸出契約的一部分，供本檔自身冪等重算使用，下游消費者請讀 "
                     "factors_history／nav_series／sprt／stats。"),
        },
    }
    return out


def main():
    try:
        out = build()
    except FailSafeAbort as e:
        print(f"  ✗ fail-safe triggered: {e} — exposure_track.json left unchanged")
        sys.exit(0)
    except Exception as e:  # noqa: BLE001 — mirrors build_trend_track.py's top-level guard
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — exposure_track.json left unchanged")
        sys.exit(0)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  ✓ wrote {OUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
