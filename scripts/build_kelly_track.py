#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_kelly_track.py — G5 Kelly 傾斜 paper 組合機械建構器。

WHAT THIS IS
------------
市況主控台（market cockpit）合成層下的另一條機械化 paper track——把議會
（council）對 SPY 21 日上漲機率的估計（p）與其 climatology 基準（p_clim）之
間的差距，轉成一個相對 100% 基準的 Kelly 傾斜曝險 E（quarter-Kelly，clip
0.5–1.5），回答「議會的 p 有沒有錢的價值」。與市況曝險規則（描述環境的三因
子 vol／trend／credit，見 scripts/build_exposure_track.py）並列、**不合
併**——曝險規則是描述器，本規則是對「機率本身」的下注測試。paper only，永
不連實倉，不是收斂面：不產名單、不進 picks/GRP/三軌/cockpit 任何清單，不得
被引用為個股或資產配置依據。上線即 paper 記分，SPRT 判紅即撤（見 PREREG
kill_conditions，下同）。

FROZEN SPEC（設計稿 2026-09-02 §4，PREREG 凍結至判決或 24 個月——本檔只實
作，不得調參；完整逐字條文見下 PREREG dict，同時原樣寫入輸出 JSON 供稽核）
--------------------------------------------------------------------------
Cadence : 掛 weekly-market-update.yml，於 build_exposure_track.py 之後執
          行；週六班車以週五收盤算、週一生效；inception＝首次執行的效力週
          一，NAV=100。
Inputs  : council＝docs/market/data/state.json council_summary.spy_up_21d
          （p／p_clim／n_sources）；rv_blend＝
          docs/market/data/exposure_track.json factors_history[-1].rv_blend
          （缺→自算，公式逐字同 scripts/build_exposure_track.py：
          0.5×RV21＋0.5×RV63）；financing＝docs/monitor/data/latest.json
          rates 類別 dgs3mo 項目 val（如「3.91%」）；prices＝SPY 日線＝
          data/flowmap_prices.json（唯讀，本檔不寫入）。
Rule    : edge＝p − p_clim。若 |edge| < 0.05（5 個百分點）、或 n_sources
          < 2、或任一輸入缺 → E＝1.0（reason：no_edge／thin_council／
          missing_input）。否則 z＝Φ⁻¹(p) − Φ⁻¹(p_clim)（statistics.
          NormalDist().inv_cdf），σ21＝(rv_blend／100) × √(21／252)，
          **E＝clip(1 ＋ 0.25 × z ／ σ21, 0.5, 1.5)**（四分之一 Kelly，相
          對 100% 基準的傾斜）。5pp 門檻與 read_zh 的「無邊際」同一把尺。
Book    : inception＝首次執行的效力週一，NAV＝100；日 NAV_t＝NAV_{t−1} ×
          (1 ＋ E × r_SPY,t − fin_t)，fin_t＝max(E − 1, 0) × (dgs3mo ＋
          1.5)／100／252（槓桿部分付 3 個月國庫券＋1.5% 年息，同 long-track
          慣例）；E < 1 的現金不計息（同曝險規則慣例，對本規則偏保守，寫進
          prereg）。基準＝SPY buy-and-hold。
Scoring : 月樣本＝當月 paper 報酬 − SPY 報酬 > 0 為命中；SPRT 同 forecast
          ledger v2 §3.3，鎖存（實作照抄 build_exposure_track.py 的
          sprt_with_latch）；Sharpe／MaxDD ≥ 3 個月才列（資訊欄）。
          scripts/score_flowmap.py 加 kelly_rule 區（讀法同
          exposure_rule），n_sprt_modules 3 → 4。
Kill    : SPRT accept_h0 → 撤下；資料層：連續 8 週因 missing_input E＝1.0
          → gaps 標紅（非 kill，由下游消費者統計，本檔只誠實記每輪
          reason）。

日 NAV 迴圈設計（本檔與 build_exposure_track.py 的差異點）
--------------------------------------------------------------------------
build_exposure_track.py 的 NAV 簿記是「週跳」——每週執行只用上週 as_of 與
本週 as_of 兩個端點算一段報酬。本規則設計稿明寫「日 NAV_t」，故本檔改為**逐
日**：exposure_history 每週新增一列（記當週算出的 E／edge／z／σ21／
reason），nav_series 則是把 data/flowmap_prices.json 裡「inception 起算日
以後」的每一個 SPY 交易日都攤開，逐日用「當時生效中的 exposure_history 列
（依 date＝生效週一 stepping）」的 E 與 dgs3mo 計算報酬與融資成本、逐日複
利。因為 flowmap_prices.json 是持續累積的全歷史日線快取（非只留最新一
週），即使本檔只被週頻呼叫，仍可在每次執行時對「上次執行到這次執行之間」
的每個交易日做冪等重算（重算結果與逐日跑一次的結果相同，因為 E 在每週生
效日之前保持不變）。

PRE-INCEPTION 行為（鏡射 build_exposure_track.py）
--------------------------------------------------------------------------
若 inception 生效週一尚無 SPY 收盤資料涵蓋（例如今日執行、下一個生效週一
還沒到，或剛好卡到假日），nav_series 留空、sprt/stats 皆以 0 筆計，但
exposure_history（E／edge／z／σ21／reason）仍照常寫入，供事前檢視「議會的
p 現在有沒有錢的價值」——不得在此之前捏造報酬。

CLI（非規格要求，僅供測試不動真帳簿；生產路徑=不帶參數執行）
--------------------------------------------------------------------------
--state PATH  覆寫 state.json 讀取路徑（預設 docs/market/data/state.json）
--out   PATH  覆寫輸出路徑（預設 docs/market/data/kelly_track.json）
測試完務必用不帶參數的方式對真實輸入跑一次，才能落到真正的 committed 路
徑——scratch 測試絕不可留在 docs/ 底下。

Runs in the weekly-market-update GitHub Actions workflow, right after the
市況曝險規則（exposure track）step.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from statistics import NormalDist, StatisticsError

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FLOWMAP_PRICES = DATA / "flowmap_prices.json"
STATE_JSON = ROOT / "docs" / "market" / "data" / "state.json"
EXPOSURE_TRACK = ROOT / "docs" / "market" / "data" / "exposure_track.json"
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
OUT_JSON = ROOT / "docs" / "market" / "data" / "kelly_track.json"

sys.path.insert(0, str(ROOT / "scripts"))
import build_exposure_track as _bet  # noqa: E402  (reuse next_monday_after / compute_rv_pair — no drift)
import score_flowmap as _sf  # noqa: E402  (reuse SPRT helper + latch, same as build_exposure_track.py)

SCHEMA = "kelly-track-v1"
_ND = NormalDist()

# ═══════════════════════════════════════════════════════════════════════
# CONFIG — PREREG 凍結（設計稿 §4；不得依單一案例調參）
# ═══════════════════════════════════════════════════════════════════════

EDGE_THRESHOLD = 0.05          # 5 個百分點（機率單位 0..1）
MIN_N_SOURCES = 2
KELLY_FRACTION = 0.25          # 四分之一 Kelly
E_CLIP = (0.5, 1.5)
SIGMA_WINDOW_TRADING_DAYS = 21
YEAR_TRADING_DAYS = 252
FINANCING_SPREAD_PP = 1.5      # dgs3mo + 1.5% 年息

KELLY_KILL_TEXT = (
    "SPRT（p0=0.5／p1=0.65／α=0.05／β=0.10，n_eff≥20，樣本＝逐月「當月 paper 報酬 − "
    "SPY B&H 報酬 > 0」命中序列）累積 LLR ≤ B(-2.2513) → accept_h0 → 規則撤下；期間"
    "不調參；paper only 永不連實倉（設計稿 "
    "notes/site-internal/root/_forecast_p2_design_20260902.md §4）。"
)

PREREG = {
    "title": "G5 Kelly 傾斜 paper 組合（PREREG 凍結至判決或 24 個月）",
    "source_doc": "notes/site-internal/root/_forecast_p2_design_20260902.md §4",
    "frozen_date": "2026-09-02",
    "positioning": (
        "回答『議會的 p 有沒有錢的價值』，與市況曝險規則（描述環境的三因子）並列、不"
        "合併。paper only，永不連實倉；不是收斂面，不產名單、不進 picks/GRP/三軌/"
        "cockpit 任何清單，不得被引用為個股或資產配置依據。"
    ),
    "cadence": (
        "掛 weekly-market-update.yml，於 build_exposure_track.py 之後執行；週六班車"
        "以週五收盤算、週一生效；inception＝首次執行的效力週一，NAV=100。"
    ),
    "inputs": {
        "council": "docs/market/data/state.json council_summary.spy_up_21d（p／p_clim／n_sources）。",
        "rv_blend": (
            "docs/market/data/exposure_track.json factors_history[-1].rv_blend；缺→"
            "自算，公式逐字同 scripts/build_exposure_track.py（0.5×RV21＋0.5×RV63）。"
        ),
        "financing_rate": "docs/monitor/data/latest.json rates 類別 dgs3mo 項目 val（如 3.91%）。",
        "prices": "SPY 日線＝data/flowmap_prices.json（唯讀，本檔不寫入）。",
    },
    "rule": {
        "edge": "edge＝p − p_clim。",
        "gate": (
            "若 |edge| < 0.05（5 個百分點）、或 n_sources < 2、或任一輸入缺 → E＝1.0"
            "（reason：no_edge／thin_council／missing_input）。"
        ),
        "tilt": (
            "否則 z＝Φ⁻¹(p) − Φ⁻¹(p_clim)（statistics.NormalDist().inv_cdf），σ21＝"
            "(rv_blend／100) × √(21／252)，E＝clip(1 ＋ 0.25 × z ／ σ21, 0.5, 1.5)（四"
            "分之一 Kelly，相對 100% 基準的傾斜）。5pp 門檻與 read_zh 的『無邊際』同一"
            "把尺。"
        ),
    },
    "book": {
        "nav": (
            "日 NAV_t＝NAV_{t−1} × (1 ＋ E × r_SPY,t − fin_t)，fin_t＝max(E − 1, 0) × "
            "(dgs3mo ＋ 1.5)／100／252（槓桿部分付 3 個月國庫券＋1.5% 年息，同"
            "long-track 慣例）。"
        ),
        "cash_policy": "E < 1 的現金不計息（同曝險規則慣例，對本規則偏保守，PREREG 明列）。",
        "benchmark": "SPY buy-and-hold（inception 當日買入，永不再平衡）。",
    },
    "scoring": {
        "monthly_sample": "月樣本＝當月 paper 報酬 − SPY B&H 報酬 > 0 為命中。",
        "sprt": (
            "SPRT 同 forecast ledger v2 §3.3 參數：p0=0.5／p1=0.65／α=0.05／β=0.10，"
            "上界 A=ln(18)=2.8904，下界 B=ln(0.1/0.95)=−2.2513，n_eff<20 一律"
            "continue，決策一旦落定即鎖存（decided_at／decided_n），只有校準輪可重"
            "設。實作照抄 scripts/build_exposure_track.py 的 sprt_with_latch，不得另"
            "開一份可能漂移的複製邏輯。"
        ),
        "info_only": "另列 Sharpe／MaxDD 對 SPY B&H（資訊欄，≥3 個月才計算，不做決策）。",
    },
    "kill_conditions": {
        "kill_1": KELLY_KILL_TEXT,
        "data_layer_note": "連續 8 週因 missing_input E＝1.0 → gaps 標紅（非 kill）。",
    },
    "disclosure": (
        "誠實標注：paper track、無交易成本、無滑價、機械式、非投資建議；不是收斂面，"
        "不產名單、不進 picks/GRP/三軌/cockpit 任何清單。"
    ),
}


def warn(msg):
    print(f"[kelly-track][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[kelly-track] {msg}")


def clip(x, lo, hi):
    return max(lo, min(hi, x))


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


def _parse_pct(val):
    """『3.91%』→ 3.91（float）；解析失敗回傳 None。"""
    if val is None:
        return None
    s = str(val).strip()
    if s.endswith("%"):
        s = s[:-1].strip()
    try:
        return float(s)
    except ValueError:
        return None


def load_council_inputs(state_path, gaps):
    state = load_json(state_path, {}) or {}
    if not state:
        gaps.append({"date": None, "reason": f"{state_path} 不存在或無法解析，council 輸入視為全缺"})
    council = (state.get("council_summary") or {}).get("spy_up_21d")
    if not council:
        gaps.append({"date": state.get("as_of"),
                     "reason": "state.json 找不到 council_summary.spy_up_21d，council 輸入視為全缺"})
        council = {}
    return council.get("p"), council.get("p_clim"), council.get("n_sources"), state.get("as_of")


def load_rv_blend(price_as_of, spy_closes_asc, gaps):
    et = load_json(EXPOSURE_TRACK, {}) or {}
    fh = et.get("factors_history") or []
    if fh and fh[-1].get("rv_blend") is not None:
        return fh[-1]["rv_blend"], "exposure_track"

    gaps.append({"date": price_as_of,
                 "reason": "exposure_track.json 無可用 rv_blend（factors_history 空或缺欄），"
                           "改自算（公式同 build_exposure_track.py）"})
    if len(spy_closes_asc) < _bet.RV_WINDOW_63 + 1:
        gaps.append({"date": price_as_of,
                     "reason": f"SPY 收盤數不足以自算 rv_blend（需 ≥{_bet.RV_WINDOW_63 + 1}，"
                               f"實得 {len(spy_closes_asc)}）"})
        return None, "unavailable"
    rv21, rv63 = _bet.compute_rv_pair(spy_closes_asc, gaps, price_as_of)
    if rv21 is None or rv63 is None:
        return None, "unavailable"
    return round(0.5 * rv21 + 0.5 * rv63, 4), "recomputed"


def load_dgs3mo(gaps):
    data = load_json(MONITOR_LATEST, {}) or {}
    for cat in data.get("categories") or []:
        if cat.get("key") != "rates":
            continue
        for it in cat.get("items") or []:
            if it.get("key") == "dgs3mo":
                pct = _parse_pct(it.get("val"))
                if pct is None:
                    gaps.append({"date": it.get("date"), "reason": f"dgs3mo val 無法解析：{it.get('val')!r}"})
                return pct, it.get("date")
    gaps.append({"date": None, "reason": "docs/monitor/data/latest.json rates 類別找不到 dgs3mo 項目"})
    return None, None


# ═══════════════════════════════════════════════════════════════════════
# Kelly 傾斜規則（設計稿 §4，PREREG 凍結）
# ═══════════════════════════════════════════════════════════════════════

def compute_kelly(p, p_clim, n_sources, rv_blend, dgs3mo, as_of, gaps):
    z = None
    if p is not None and p_clim is not None:
        try:
            z = _ND.inv_cdf(p) - _ND.inv_cdf(p_clim)
        except (StatisticsError, ValueError) as e:
            gaps.append({"date": as_of, "reason": f"Φ⁻¹(p)/Φ⁻¹(p_clim) 計算失敗（p={p}, p_clim={p_clim}）：{e}"})
            z = None

    sigma21 = None
    if rv_blend is not None:
        sigma21 = (rv_blend / 100.0) * math.sqrt(SIGMA_WINDOW_TRADING_DAYS / YEAR_TRADING_DAYS)

    edge = (p - p_clim) if (p is not None and p_clim is not None) else None

    missing = [name for name, v in (
        ("p", p), ("p_clim", p_clim), ("n_sources", n_sources), ("rv_blend", rv_blend), ("dgs3mo", dgs3mo),
    ) if v is None]
    if missing:
        gaps.append({"date": as_of, "reason": f"輸入缺漏（{', '.join(missing)}），E 退回 1.0（reason=missing_input）"})
        return {"edge": edge, "z": _r(z), "sigma21": _r(sigma21), "E": 1.0, "reason": "missing_input"}

    if n_sources < MIN_N_SOURCES:
        gaps.append({"date": as_of, "reason": f"n_sources={n_sources} < {MIN_N_SOURCES}，"
                                               "E 退回 1.0（reason=thin_council）"})
        return {"edge": _r(edge), "z": _r(z), "sigma21": _r(sigma21), "E": 1.0, "reason": "thin_council"}

    if abs(edge) < EDGE_THRESHOLD:
        return {"edge": _r(edge), "z": _r(z), "sigma21": _r(sigma21), "E": 1.0, "reason": "no_edge"}

    if sigma21 is None or sigma21 == 0 or z is None:
        gaps.append({"date": as_of, "reason": "sigma21 或 z 無法計算（rv_blend 退化或 Φ⁻¹ 失敗），"
                                               "E 退回 1.0（reason=missing_input）"})
        return {"edge": _r(edge), "z": _r(z), "sigma21": _r(sigma21), "E": 1.0, "reason": "missing_input"}

    raw = 1.0 + KELLY_FRACTION * z / sigma21
    E = round(clip(raw, *E_CLIP), 4)
    return {"edge": _r(edge), "z": _r(z), "sigma21": _r(sigma21), "E": E, "reason": "kelly_tilt"}


def _r(v, d=6):
    return None if v is None else round(v, d)


# ═══════════════════════════════════════════════════════════════════════
# 日 NAV 迴圈（設計稿 §4：「日 NAV_t」，見檔頭說明本檔與 build_exposure_track.py 的差異）
# ═══════════════════════════════════════════════════════════════════════

def build_daily_nav_loop(exposure_history, spy_series_asc, inception_date, gaps):
    if not exposure_history:
        return []
    if not spy_series_asc:
        gaps.append({"date": inception_date, "reason": "SPY 價格序列為空，NAV 簿記尚未起算"})
        return []

    idx_start = None
    for i, (d, _c) in enumerate(spy_series_asc):
        if d >= inception_date:
            idx_start = i
            break
    if idx_start is None:
        gaps.append({"date": inception_date,
                     "reason": f"SPY 價格序列尚無 {inception_date}（含）以後的收盤，"
                               "NAV 簿記尚未起算，不捏造 nav_series。"})
        return []

    hist_sorted = sorted(exposure_history, key=lambda r: r["date"])

    def active_row_for(d):
        active = hist_sorted[0]
        for r in hist_sorted:
            if r["date"] <= d:
                active = r
            else:
                break
        return active

    nav_series = []
    nav = 100.0
    spy_bh = 100.0
    prev_close = None
    for i in range(idx_start, len(spy_series_asc)):
        d, close = spy_series_asc[i]
        active = active_row_for(d)
        e_active = active.get("E", 1.0)
        dgs3mo_active = active.get("dgs3mo")
        spy_ret = None
        fin = None
        if i > idx_start:
            spy_ret = close / prev_close - 1.0
            fin = (max(e_active - 1.0, 0.0) * (dgs3mo_active + FINANCING_SPREAD_PP) / 100.0 / YEAR_TRADING_DAYS
                   if dgs3mo_active is not None else 0.0)
            nav = nav * (1.0 + e_active * spy_ret - fin)
            spy_bh = spy_bh * (1.0 + spy_ret)
        nav_series.append({
            "date": d,
            "nav": round(nav, 4),
            "spy_bh": round(spy_bh, 4),
            "spy_close": round(close, 4),
            "E_applied": e_active,
            "spy_ret_pct": round(spy_ret * 100, 4) if spy_ret is not None else None,
            "fin_pct": round(fin * 100, 6) if fin is not None else None,
        })
        prev_close = close
    return nav_series


# ═══════════════════════════════════════════════════════════════════════
# SPRT 序貫檢定（復用 scripts/score_flowmap.py，見檔頭說明）
# ═══════════════════════════════════════════════════════════════════════

def compute_monthly_samples(nav_series):
    """按 nav_series[].date（本檔的 date 即真實交易日，非 build_exposure_track.py
    那種「效力週一」標籤，故不需要像該檔一樣另外用 as_of 分月）分桶，桶內取最後一
    列；最後一個月視為進行中不計分。"""
    by_month = {}
    order = []
    for row in nav_series:
        m = row["date"][:7]
        if m not in by_month:
            order.append(m)
        by_month[m] = row
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
        "kill_condition": KELLY_KILL_TEXT,
    }


# ═══════════════════════════════════════════════════════════════════════
# Sharpe／MaxDD（資訊欄，≥3 個完整月才算，設計稿 §4）
# ═══════════════════════════════════════════════════════════════════════

def _monthly_returns(nav_series, key, n_closed_months):
    by_month = {}
    order = []
    for row in nav_series:
        m = row["date"][:7]
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
    for label, key in (("paper", "nav"), ("spy_bh", "spy_bh")):
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

def build(state_path, out_path):
    gaps = []

    price_series, price_built_at = load_price_series()
    spy_series = price_series.get("SPY") or []
    if spy_series:
        price_as_of = spy_series[-1][0]
        spy_closes_asc = [c for _d, c in spy_series]
    else:
        price_as_of = date.today().isoformat()
        spy_closes_asc = []
        gaps.append({"date": price_as_of, "reason": "data/flowmap_prices.json 無 SPY 序列"})

    p, p_clim, n_sources, state_as_of = load_council_inputs(state_path, gaps)
    rv_blend, rv_blend_source = load_rv_blend(price_as_of, spy_closes_asc, gaps)
    dgs3mo, dgs3mo_asof = load_dgs3mo(gaps)

    kelly = compute_kelly(p, p_clim, n_sources, rv_blend, dgs3mo, price_as_of, gaps)

    info(f"as_of={price_as_of}  p={p}  p_clim={p_clim}  n_sources={n_sources}  "
         f"rv_blend={rv_blend} ({rv_blend_source})  dgs3mo={dgs3mo}%  "
         f"edge={kelly['edge']}  z={kelly['z']}  sigma21={kelly['sigma21']}  "
         f"E={kelly['E']}  reason={kelly['reason']}")

    existing = load_json(out_path, {}) or {}
    exposure_history = existing.get("exposure_history") or []

    eff = _bet.next_monday_after(date.fromisoformat(price_as_of)).isoformat() if spy_series \
        else date.today().isoformat()
    inception_date = existing.get("inception_date") or eff

    row = {
        "date": eff, "as_of": price_as_of, "state_as_of": state_as_of,
        "p": p, "p_clim": p_clim, "n_sources": n_sources,
        "rv_blend": rv_blend, "rv_blend_source": rv_blend_source,
        "dgs3mo": dgs3mo, "dgs3mo_asof": dgs3mo_asof,
        "edge": kelly["edge"], "z": kelly["z"], "sigma21": kelly["sigma21"],
        "E": kelly["E"], "reason": kelly["reason"],
    }
    if exposure_history and exposure_history[-1].get("as_of") == price_as_of:
        exposure_history[-1] = row
        info(f"    same as_of rerun overwritten in place: as_of={price_as_of}")
    else:
        exposure_history.append(row)
        info(f"    exposure_history row appended: date={eff} (as_of={price_as_of})")

    nav_series = build_daily_nav_loop(exposure_history, spy_series, inception_date, gaps)
    if not nav_series:
        info(f"    pre-inception or no data yet at/after {inception_date} — nav_series 留空")

    prior_sprt = existing.get("sprt")
    sprt_block = build_sprt_block(nav_series, prior_sprt)
    _, n_closed_months = compute_monthly_samples(nav_series)
    stats_block = build_stats_block(nav_series, n_closed_months)

    out = {
        "schema": SCHEMA,
        "prereg": PREREG,
        "as_of": price_as_of,
        "inception_date": inception_date,
        "exposure_history": exposure_history,
        "nav_series": nav_series,
        "bench": {
            "name": "spy_bh",
            "description": "SPY buy-and-hold（inception 當日買入，永不再平衡）；序列見 nav_series[].spy_bh。",
        },
        "sprt": sprt_block,
        "stats": stats_block,
        "data_gaps": gaps,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "meta": {
            "flowmap_prices_built_at": price_built_at,
            "note": ("exposure_history 逐週由本檔重算並冪等覆蓋（同 as_of 不重複 append）；"
                     "nav_series 為逐日重算（見檔頭『日 NAV 迴圈設計』），下游消費者請讀 "
                     "exposure_history／nav_series／sprt／stats。"),
        },
    }
    return out


def parse_args():
    ap = argparse.ArgumentParser(description="G5 Kelly 傾斜 paper 組合 builder")
    ap.add_argument("--state", default=str(STATE_JSON),
                     help="覆寫 state.json 讀取路徑（測試用，預設讀真實路徑，不動真帳簿）")
    ap.add_argument("--out", default=str(OUT_JSON),
                     help="覆寫輸出路徑（測試用，預設寫真實 docs/market/data/kelly_track.json）")
    return ap.parse_args()


def main():
    args = parse_args()
    state_path = Path(args.state)
    out_path = Path(args.out)
    try:
        out = build(state_path, out_path)
    except Exception as e:  # noqa: BLE001 — mirrors build_exposure_track.py's top-level guard
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — {out_path} left unchanged")
        sys.exit(0)
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  ✓ wrote {out_path}")


if __name__ == "__main__":
    main()
