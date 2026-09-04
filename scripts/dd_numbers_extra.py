#!/usr/bin/env python3
"""dd_numbers_extra.py — v16.1 Stage 0a 數字包強化（0 LLM token，盡力而為，永不 abort）。

補五個結構化欄位到 evidence.json 的 numbers 區塊，解決 v16 dry-run critic 首輪常見的
「判斷層引用比最新一季更舊的數字」「口徑不一致」「共識修正沒查」「客戶集中度沒查原文」
「52 週新高時仍用 RSI」五類 🔴：

  numbers.valuation_history      — trailing P/E／P/S／EV/S 五年高低點與現值分位（誠實口徑：
                                    yfinance 免費層無歷史 fwd 共識，能算的一律標「trailing 口徑」；
                                    另用本地 data/eps-estimates/ 快照archive 算一段短窗真 fwd PE）
  numbers.momentum_26w           — 13w／26w 報酬、相對大盤超額、RSI14、rsi14_usable（52週新高
                                    3% 以內為 false）、距 52 週高低點 %
  numbers.consensus_revision     — 用 data/eps-estimates/ 最新與前一份（及約 90 天前）快照
                                    算 FY1/FY2/FY3 EPS 修正 %；stale=true 若最新快照距 DATE >21 天
  numbers.peer_financials        — 對手 + 自身 TTM 毛利率／營業利益率／FCF margin／R&D 強度
  numbers.edgar_concentrations   — 最新 10-Q（無則 10-K）Concentrations／customer concentration
                                    原文段落摘錄（≤3KB）
  numbers.latest_quarter_kpis    — 佔位符（腳本不算，留給採集 agent 填 items[]）

規則：每個欄位都帶 as_of／source／method；算不出來一律 null＋note 說明原因，**不得捏造**；
網路或 yfinance 失敗只影響該欄位，其餘欄位照常輸出。

用法：
  python3 scripts/dd_numbers_extra.py SNOW 20260904 \
      --peers DDOG,MDB,CFLT --evidence .dd_build/SNOW_20260904.evidence.json \
      --out .dd_build/evidence_parts/SNOW_numbers_extra.json
  python3 scripts/dd_numbers_extra.py DELL 20260904 --evidence .dd_build/DELL_20260904.evidence.json

輸出：頂層 {"numbers": {...}} 片段，可直接 `dd_evidence.py merge` 進 evidence.json。
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import warnings
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

warnings.filterwarnings("ignore")

from load_eps_estimates_xlsx import DEFAULT_DATA_DIR, FILENAME_RE, load_excel  # noqa: E402

CACHE_DIR = ROOT / ".dd_build" / "_cache"
SEC_HEADERS = {"User-Agent": "financial-analysis-bot keigoks@gmail.com"}


def _lazy_imports():
    """yfinance/pandas/numpy 延遲載入，讓 --help 與純本地邏輯（consensus_revision）
    不必依賴網路套件是否可用。"""
    import numpy as np
    import pandas as pd
    import yfinance as yf
    return np, pd, yf


# ---------------------------------------------------------------------------
# numbers.valuation_history
# ---------------------------------------------------------------------------

def _pct_rank(current, hist_values):
    hist_values = [v for v in hist_values if v is not None]
    if not hist_values or current is None:
        return None
    lo, hi = min(hist_values), max(hist_values)
    if hi == lo:
        return 50.0
    pct = (current - lo) / (hi - lo) * 100
    return round(max(0.0, min(100.0, pct)), 1)


def compute_valuation_history(ticker, date_dt):
    out = {
        "method": (
            "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing "
            "P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——"
            "樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 "
            "archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"
        ),
        "trailing": {},
        "fwd_recent_window": None,
        "note": None,
    }
    try:
        np, pd, yf = _lazy_imports()
        t = yf.Ticker(ticker)
        info = {}
        try:
            info = t.info or {}
        except Exception as e:
            out["note"] = f"info 讀取失敗：{e}"

        w = yf.download(ticker, period="6y", interval="1wk", auto_adjust=True, progress=False)
        if w is None or w.empty:
            out["note"] = ((out["note"] + "；") if out["note"] else "") + "週線價格序列為空"
            return out
        close = w["Close"][ticker] if hasattr(w["Close"], "columns") or ticker in getattr(w["Close"], "columns", []) else w["Close"]
        try:
            close = w["Close"][ticker]
        except Exception:
            close = w["Close"]
        close = close.dropna()

        ais = None
        abs_ = None
        try:
            ais = t.income_stmt
        except Exception:
            pass
        try:
            abs_ = t.balance_sheet
        except Exception:
            pass

        points = []
        if ais is not None and not ais.empty and "Total Revenue" in ais.index:
            for col in ais.columns:
                try:
                    rev = ais.loc["Total Revenue", col] if "Total Revenue" in ais.index else None
                    eps = ais.loc["Diluted EPS", col] if "Diluted EPS" in ais.index else None
                    shares = ais.loc["Diluted Average Shares", col] if "Diluted Average Shares" in ais.index else None
                    debt = None
                    cash = None
                    if abs_ is not None and not abs_.empty and col in abs_.columns:
                        debt = abs_.loc["Total Debt", col] if "Total Debt" in abs_.index else None
                        cash = abs_.loc["Cash And Cash Equivalents", col] if "Cash And Cash Equivalents" in abs_.index else None
                    if rev is None or (hasattr(rev, "__float__") and pd.isna(rev)) or float(rev) == 0:
                        continue
                    pos = close.index.get_indexer([col], method="nearest")[0]
                    price = float(close.iloc[pos])
                    price_date = close.index[pos]
                    mktcap = None
                    if shares is not None and not pd.isna(shares):
                        mktcap = price * float(shares)
                    pe = None
                    if eps is not None and not pd.isna(eps) and float(eps) > 0:
                        pe = price / float(eps)
                    ps = (mktcap / float(rev)) if mktcap else None
                    ev = None
                    if mktcap is not None:
                        d = float(debt) if debt is not None and not pd.isna(debt) else 0.0
                        c = float(cash) if cash is not None and not pd.isna(cash) else 0.0
                        ev = mktcap + d - c
                    evs = (ev / float(rev)) if ev is not None else None
                    points.append({
                        "fiscal_period_end": col.strftime("%Y-%m-%d"),
                        "price_used": round(price, 2),
                        "price_date": price_date.strftime("%Y-%m-%d"),
                        "pe": round(pe, 2) if pe else None,
                        "ps": round(ps, 2) if ps else None,
                        "ev_s": round(evs, 2) if evs else None,
                    })
                except Exception:
                    continue

        # current point
        current_price = float(close.iloc[-1])
        current_pe = info.get("trailingPE")
        if current_pe is None and info.get("trailingEps") not in (None, 0):
            try:
                if info["trailingEps"] > 0:
                    current_pe = current_price / info["trailingEps"]
            except Exception:
                current_pe = None
        current_ps = info.get("priceToSalesTrailing12Months")
        current_evs = None
        mkt_cap = info.get("marketCap")
        total_debt = info.get("totalDebt")
        total_cash = info.get("totalCash")
        if mkt_cap and current_ps:
            ttm_rev = mkt_cap / current_ps
            if total_debt is not None and total_cash is not None:
                ev = mkt_cap + total_debt - total_cash
                current_evs = ev / ttm_rev if ttm_rev else None

        for metric, cur in (("pe", current_pe), ("ps", current_ps), ("ev_s", current_evs)):
            hist_vals = [p[metric] for p in points if p.get(metric) is not None]
            entry = {"n_points": len(hist_vals), "current": round(cur, 2) if cur else None}
            if hist_vals:
                hi_p = max((p for p in points if p.get(metric) is not None), key=lambda p: p[metric])
                lo_p = min((p for p in points if p.get(metric) is not None), key=lambda p: p[metric])
                entry["high"] = {"value": hi_p[metric], "date": hi_p["fiscal_period_end"]}
                entry["low"] = {"value": lo_p[metric], "date": lo_p["fiscal_period_end"]}
                entry["current_percentile_within_annual_points"] = _pct_rank(cur, hist_vals)
            else:
                entry["high"] = None
                entry["low"] = None
                entry["current_percentile_within_annual_points"] = None
                entry["note"] = f"annual 財報樣本不足以算 {metric} 歷史高低點（GAAP 損則 pe 常年缺）"
            out["trailing"][metric] = entry

        # fwd_recent_window：用本站月度快照 archive 算一段短窗真 fwd PE
        try:
            files = sorted(
                (p for p in DEFAULT_DATA_DIR.glob("DD_universe_EPS_estimates_*.xlsx") if FILENAME_RE.search(p.name)),
                key=lambda p: FILENAME_RE.search(p.name).group(1),
            )
            fwd_points = []
            for p in files:
                snap = load_excel(p)
                rec = snap.get(ticker)
                if not rec or rec.get("fy1") in (None, 0):
                    continue
                snap_dt = datetime.strptime(FILENAME_RE.search(p.name).group(1), "%Y%m%d")
                pos = close.index.get_indexer([pd.Timestamp(snap_dt)], method="nearest")[0]
                price = float(close.iloc[pos])
                fwd_pe = price / rec["fy1"] if rec["fy1"] > 0 else None
                if fwd_pe is not None:
                    fwd_points.append({"snapshot_date": snap.snapshot_date, "price_used": round(price, 2),
                                        "fy1_eps": rec["fy1"], "fwd_pe": round(fwd_pe, 2)})
            if fwd_points:
                vals = [f["fwd_pe"] for f in fwd_points]
                out["fwd_recent_window"] = {
                    "points": fwd_points,
                    "current": vals[-1],
                    "high": max(vals),
                    "low": min(vals),
                    "current_percentile_within_window": _pct_rank(vals[-1], vals),
                    "window_note": (
                        f"僅涵蓋本站 data/eps-estimates/ 現存 {len(vals)} 份快照"
                        f"（{fwd_points[0]['snapshot_date']} ~ {fwd_points[-1]['snapshot_date']}），"
                        "非 5 年歷史，不得引用為『5年分位』"
                    ),
                }
            else:
                out["fwd_recent_window"] = {"note": f"{ticker} 不在任一 data/eps-estimates/ 快照，或 FY1 EPS 缺失"}
        except Exception as e:
            out["fwd_recent_window"] = {"note": f"短窗 fwd PE 計算失敗：{e}"}

    except Exception as e:
        out["note"] = ((out["note"] + "；") if out.get("note") else "") + f"整體計算失敗：{e}"
    return out


# ---------------------------------------------------------------------------
# numbers.price_at_dd / price_as_of / earnings_recency（v16.2 新增，扁平三欄）
# ---------------------------------------------------------------------------
# WHY（PANW 教訓，見設計稿 §15）：validate_evidence.py 的 NUMBERS_REQUIRED 三欄
# （price_at_dd／price_as_of／earnings_recency）過去全靠採集 agent 自由發揮回傳格式，
# PANW dry-run 實際回傳是巢狀鍵（塞在 top_banner 之類的物件裡），orchestrator 得手動
# 機械對映。這裡直接算好扁平三欄，採集 agent 只補值、不得改鍵名（見 data-collection.md）。


def compute_price_and_earnings_recency(ticker, date_dt):
    """回傳 (price_at_dd, price_as_of, earnings_recency) 三個扁平值。
    查不到一律 None，並在對應欄位帶 note 說明原因，不得捏造。"""
    price_at_dd = None
    price_as_of = None
    earnings_recency = {
        "last_earnings_date": None, "trading_days_since": None,
        "flag_within_3d": None, "note": None,
    }
    try:
        np, pd, yf = _lazy_imports()
        t = yf.Ticker(ticker)
        info = {}
        try:
            info = t.info or {}
        except Exception as e:
            price_at_dd = None
            price_as_of = None

        rth_close = info.get("regularMarketPrice")
        rth_time = info.get("regularMarketTime")  # yfinance 有時給 epoch int，有時缺
        if rth_close is None:
            # 退回：抓最近一筆日線收盤
            daily = yf.download(ticker, period="10d", interval="1d", auto_adjust=False, progress=False)
            if daily is not None and not daily.empty:
                try:
                    close_series = daily["Close"][ticker]
                except Exception:
                    close_series = daily["Close"]
                close_series = close_series.dropna()
                if not close_series.empty:
                    rth_close = float(close_series.iloc[-1])
                    price_as_of = close_series.index[-1].strftime("%Y-%m-%d") + "（RTH 收盤，日線 fallback）"
        if rth_close is not None:
            price_at_dd = round(float(rth_close), 2)
            if price_as_of is None:
                if isinstance(rth_time, (int, float)):
                    try:
                        price_as_of = datetime.utcfromtimestamp(rth_time).strftime("%Y-%m-%d") + "（RTH 收盤，UTC）"
                    except Exception:
                        price_as_of = date_dt.strftime("%Y-%m-%d") + "（RTH 收盤，regularMarketPrice，時間戳缺失以報告日代）"
                else:
                    price_as_of = date_dt.strftime("%Y-%m-%d") + "（RTH 收盤，regularMarketPrice）"
        else:
            earnings_recency["note"] = "價格查詢失敗，price_at_dd/price_as_of 留 null"

        try:
            edates = t.earnings_dates
            if edates is not None and not edates.empty:
                now = pd.Timestamp.now(tz=edates.index.tz)
                past = edates[edates.index <= now]
                if not past.empty:
                    last = past.index.max()
                    earnings_recency["last_earnings_date"] = last.strftime("%Y-%m-%d")
                    trading_days = int(np.busday_count(last.date(), date_dt.date()))
                    earnings_recency["trading_days_since"] = trading_days
                    earnings_recency["flag_within_3d"] = trading_days <= 3
                    if trading_days <= 3:
                        earnings_recency["note"] = (
                            f"距最近財報僅 {trading_days} 個交易日（≤3）——估值層須用財報後價格"
                            "（postMarketPrice/preMarketPrice），共識 EPS 標「財報前快照」"
                        )
                else:
                    earnings_recency["note"] = "earnings_dates 內查無已發生的財報日"
            else:
                earnings_recency["note"] = "t.earnings_dates 為空，改嘗試 t.calendar"
                cal = t.calendar
                if isinstance(cal, dict) and cal.get("Earnings Date"):
                    ed = cal["Earnings Date"]
                    earnings_recency["note"] += f"；calendar 顯示下次財報日 {ed}（非最近一次已發生財報，僅供參考）"
        except Exception as e:
            earnings_recency["note"] = ((earnings_recency["note"] + "；") if earnings_recency["note"] else "") + \
                f"earnings_dates 查詢失敗：{e}"
    except Exception as e:
        earnings_recency["note"] = ((earnings_recency["note"] + "；") if earnings_recency.get("note") else "") + \
            f"整體計算失敗：{e}"

    return price_at_dd, price_as_of, earnings_recency


# ---------------------------------------------------------------------------
# numbers.momentum_26w
# ---------------------------------------------------------------------------

def _compute_rsi(close, period=14):
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.ewm(alpha=1 / period, adjust=False).mean()
    roll_down = down.ewm(alpha=1 / period, adjust=False).mean()
    rs = roll_up / roll_down
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])


def compute_momentum_26w(ticker, idx_benchmark=None):
    out = {
        "return_13w_pct": None, "return_26w_pct": None,
        "excess_return_13w_pct": None, "excess_return_26w_pct": None,
        "benchmark": None, "rsi14": None, "rsi14_usable": None,
        "distance_from_52w_high_pct": None, "distance_from_52w_low_pct": None,
        "note": None,
    }
    try:
        np, pd, yf = _lazy_imports()
        daily = yf.download(ticker, period="14mo", interval="1d", auto_adjust=True, progress=False)
        if daily is None or daily.empty:
            out["note"] = "日線價格序列為空"
            return out
        try:
            close = daily["Close"][ticker]
        except Exception:
            close = daily["Close"]
        close = close.dropna()
        current = float(close.iloc[-1])
        current_date = close.index[-1]

        def ret_weeks(series, weeks):
            target = series.index[-1] - pd.Timedelta(weeks=weeks)
            pos = series.index.get_indexer([target], method="nearest")[0]
            base = float(series.iloc[pos])
            cur = float(series.iloc[-1])
            return (cur / base - 1) * 100 if base else None

        r13 = ret_weeks(close, 13)
        r26 = ret_weeks(close, 26)
        out["return_13w_pct"] = round(r13, 2) if r13 is not None else None
        out["return_26w_pct"] = round(r26, 2) if r26 is not None else None

        bench = idx_benchmark or ("^TWII" if ticker.upper().endswith(".TW") else "^GSPC")
        out["benchmark"] = bench
        try:
            bdaily = yf.download(bench, period="14mo", interval="1d", auto_adjust=True, progress=False)
            try:
                bclose = bdaily["Close"][bench]
            except Exception:
                bclose = bdaily["Close"]
            bclose = bclose.dropna()
            br13 = ret_weeks(bclose, 13)
            br26 = ret_weeks(bclose, 26)
            if r13 is not None and br13 is not None:
                out["excess_return_13w_pct"] = round(r13 - br13, 2)
            if r26 is not None and br26 is not None:
                out["excess_return_26w_pct"] = round(r26 - br26, 2)
        except Exception as e:
            out["note"] = f"benchmark {bench} 抓取失敗：{e}"

        try:
            out["rsi14"] = round(_compute_rsi(close, 14), 2)
        except Exception as e:
            out["rsi14"] = None
            out["note"] = ((out["note"] + "；") if out["note"] else "") + f"RSI14 計算失敗：{e}"

        w52_window = close[close.index >= (current_date - pd.Timedelta(weeks=52))]
        if not w52_window.empty:
            hi = float(w52_window.max())
            lo = float(w52_window.min())
            dist_hi = (current / hi - 1) * 100 if hi else None
            dist_lo = (current / lo - 1) * 100 if lo else None
            out["distance_from_52w_high_pct"] = round(dist_hi, 2) if dist_hi is not None else None
            out["distance_from_52w_low_pct"] = round(dist_lo, 2) if dist_lo is not None else None
            if dist_hi is not None:
                within_3pct_of_high = abs(dist_hi) <= 3
                out["rsi14_usable"] = not within_3pct_of_high
                if within_3pct_of_high:
                    out["note"] = ((out["note"] + "；") if out["note"] else "") + \
                        f"現價距52週高點 {dist_hi:.2f}%（3%以內）— 與52週新高互斥，RSI14 在此情境不具判讀意義，不得引用 RSI 超買/超賣結論"
        else:
            out["note"] = ((out["note"] + "；") if out["note"] else "") + "52週價格窗為空，無法算距高低點%"
    except Exception as e:
        out["note"] = ((out["note"] + "；") if out.get("note") else "") + f"整體計算失敗：{e}"
    return out


# ---------------------------------------------------------------------------
# numbers.consensus_revision
# ---------------------------------------------------------------------------

def compute_consensus_revision(ticker, date_dt):
    result = {
        "latest_snapshot": None, "previous_snapshot": None, "snapshot_90d_prior": None,
        "fy1": None, "fy2": None, "fy3": None,
        "fy1_revision_90d_pct": None, "fy2_revision_90d_pct": None, "fy3_revision_90d_pct": None,
        "stale": None, "note": None,
    }
    try:
        files = [p for p in DEFAULT_DATA_DIR.glob("DD_universe_EPS_estimates_*.xlsx") if FILENAME_RE.search(p.name)]
        if not files:
            result["note"] = "data/eps-estimates/ 無任何快照檔"
            return result
        valid = sorted(((p, FILENAME_RE.search(p.name).group(1)) for p in files), key=lambda x: x[1])
        latest_path, latest_d = valid[-1]
        latest_dt = datetime.strptime(latest_d, "%Y%m%d")
        stale = (date_dt - latest_dt).days > 21
        result["stale"] = stale

        latest_snap = load_excel(latest_path)
        latest_rec = latest_snap.get(ticker)
        if latest_rec is None:
            result["note"] = f"{ticker} 不在最新快照 {latest_path.name}"
            return result
        result["latest_snapshot"] = {
            "file": latest_path.name, "date": latest_snap.snapshot_date,
            "fy1": latest_rec.get("fy1"), "fy2": latest_rec.get("fy2"), "fy3": latest_rec.get("fy3"),
        }
        if stale:
            result["note"] = f"最新快照 {latest_snap.snapshot_date} 距報告日 {date_dt.date()} 已超過21天，FY 估值仍是財報前/舊季快照"

        if len(valid) >= 2:
            prev_path, prev_d = valid[-2]
            prev_snap = load_excel(prev_path)
            prev_rec = prev_snap.get(ticker)
            if prev_rec is not None:
                result["previous_snapshot"] = {
                    "file": prev_path.name, "date": prev_snap.snapshot_date,
                    "fy1": prev_rec.get("fy1"), "fy2": prev_rec.get("fy2"), "fy3": prev_rec.get("fy3"),
                }
                for fy in ("fy1", "fy2", "fy3"):
                    lv, pv = latest_rec.get(fy), prev_rec.get(fy)
                    if lv is not None and pv not in (None, 0):
                        result[fy] = {
                            "revision_pct": round((lv - pv) / abs(pv) * 100, 2),
                            "from": pv, "to": lv,
                            "from_date": prev_snap.snapshot_date, "to_date": latest_snap.snapshot_date,
                        }
            else:
                result["previous_snapshot"] = {"file": prev_path.name, "note": f"{ticker} 不在此快照"}
        else:
            result["previous_snapshot"] = None
            result["note"] = ((result["note"] + "；") if result["note"] else "") + "僅有一份快照，無法算修正%"

        target = latest_dt - timedelta(days=90)
        candidates = [(p, d) for p, d in valid if d != latest_d]
        if candidates:
            best_path, best_d = min(candidates, key=lambda x: abs((datetime.strptime(x[1], "%Y%m%d") - target).days))
            best_dt = datetime.strptime(best_d, "%Y%m%d")
            if abs((best_dt - target).days) <= 35:
                snap90 = load_excel(best_path)
                rec90 = snap90.get(ticker)
                if rec90 is not None:
                    result["snapshot_90d_prior"] = {
                        "file": best_path.name, "date": snap90.snapshot_date,
                        "fy1": rec90.get("fy1"), "fy2": rec90.get("fy2"), "fy3": rec90.get("fy3"),
                    }
                    for fy in ("fy1", "fy2", "fy3"):
                        lv, pv = latest_rec.get(fy), rec90.get(fy)
                        key = f"{fy}_revision_90d_pct"
                        if lv is not None and pv not in (None, 0):
                            result[key] = round((lv - pv) / abs(pv) * 100, 2)
            else:
                result["note"] = ((result["note"] + "；") if result["note"] else "") + \
                    f"最接近90天前的快照為 {best_dt.date()}，與目標相差 >35 天，未採用（archive 尚淺）"
    except Exception as e:
        result["note"] = ((result["note"] + "；") if result.get("note") else "") + f"整體計算失敗：{e}"
    return result


# ---------------------------------------------------------------------------
# numbers.peer_financials
# ---------------------------------------------------------------------------

def _ttm_financials(ticker):
    out = {
        "gross_margin_pct": None, "operating_margin_pct": None,
        "fcf_margin_pct": None, "rd_intensity_pct": None,
        "fiscal_period_as_of": None,
        "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）",
        "note": None,
    }
    try:
        np, pd, yf = _lazy_imports()
        t = yf.Ticker(ticker)
        qis = t.quarterly_income_stmt
        qcf = None
        try:
            qcf = t.quarterly_cashflow
        except Exception:
            pass
        if qis is None or qis.empty:
            out["note"] = "quarterly_income_stmt 無資料"
            return out
        n = min(4, qis.shape[1])
        cols = list(qis.columns[:n])

        def rowsum(df, name, use_cols):
            if df is None or df.empty or name not in df.index:
                return None
            vals = df.loc[name, use_cols].dropna()
            if vals.empty:
                return None
            return float(vals.sum())

        rev = rowsum(qis, "Total Revenue", cols)
        gp = rowsum(qis, "Gross Profit", cols)
        opinc = rowsum(qis, "Operating Income", cols)
        rd = rowsum(qis, "Research And Development", cols)

        fcf = None
        if qcf is not None and not qcf.empty:
            ccols = [c for c in cols if c in qcf.columns]
            if not ccols:
                ccols = list(qcf.columns[:n])
            fcf = rowsum(qcf, "Free Cash Flow", ccols)

        if rev:
            if gp is not None:
                out["gross_margin_pct"] = round(gp / rev * 100, 2)
            if opinc is not None:
                out["operating_margin_pct"] = round(opinc / rev * 100, 2)
            if fcf is not None:
                out["fcf_margin_pct"] = round(fcf / rev * 100, 2)
            if rd is not None:
                out["rd_intensity_pct"] = round(rd / rev * 100, 2)
            else:
                out["note"] = "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"
        else:
            out["note"] = "Total Revenue 缺失，無法算利潤率"

        out["fiscal_period_as_of"] = f"TTM ending {cols[0].strftime('%Y-%m-%d')}（{n}季加總）"
        if n < 4:
            out["note"] = ((out["note"] + "；") if out["note"] else "") + f"僅 {n} 季可得，非完整 TTM"
    except Exception as e:
        out["note"] = f"擷取失敗：{e}"
    return out


def compute_peer_financials(ticker, peers):
    result = {}
    result[ticker] = _ttm_financials(ticker)
    for p in peers:
        result[p] = _ttm_financials(p)
    return result


def _resolve_peers(args):
    if args.peers:
        return [p.strip() for p in args.peers.split(",") if p.strip()]
    if args.evidence:
        try:
            evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
            pv = (evidence.get("numbers") or {}).get("peer_valuation") or {}
            skip_keys = {"query", "gap_note", "note"}
            peers = [k for k in pv.keys() if k not in skip_keys]
            if peers:
                return peers
        except Exception:
            pass
    return []


# ---------------------------------------------------------------------------
# numbers.edgar_concentrations
# ---------------------------------------------------------------------------

def _load_company_tickers():
    import requests
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / "company_tickers.json"
    if cache.exists() and (time.time() - cache.stat().st_mtime) < 7 * 86400:
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except Exception:
            pass
    r = requests.get("https://www.sec.gov/files/company_tickers.json", headers=SEC_HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    try:
        cache.write_text(json.dumps(data), encoding="utf-8")
    except Exception:
        pass
    return data


def _resolve_cik(ticker):
    base = ticker.split(".")[0].upper()
    data = _load_company_tickers()
    for v in data.values():
        if v.get("ticker", "").upper() == base:
            return str(v["cik_str"]).zfill(10)
    return None


_CONCENTRATION_PATTERN = re.compile(
    r"(accounted for (approximately )?\d[\d.]*%[^.]{0,220}(revenue|receivable)[^.]{0,150}\.)",
    re.I,
)

_SENTENCE_BOUNDARY_RE = re.compile(r"[.!?]\s")


def _snap_excerpt(clean, anchor_pos, max_len=2700, max_back=400):
    """從 anchor_pos 附近取摘錄，起訖snap到句界（句號/問號/驚嘆號＋空白），而非從句中硬切。
    往前最多回溯 max_back 字元找最近的句界；找不到就退回該回溯上限（段落起點近似值）。
    往後在 max_len 預算內找最後一個句界收尾；找不到才硬切在預算邊界。"""
    back_limit = max(0, anchor_pos - max_back)
    lookback_region = clean[back_limit:anchor_pos]
    boundaries = [b.end() for b in _SENTENCE_BOUNDARY_RE.finditer(lookback_region)]
    start = back_limit + boundaries[-1] if boundaries else back_limit

    end_cap = min(len(clean), start + max_len)
    forward_region = clean[start:end_cap]
    fwd_boundaries = [b.end() for b in _SENTENCE_BOUNDARY_RE.finditer(forward_region)]
    end = start + fwd_boundaries[-1] if fwd_boundaries else end_cap
    return clean[start:end].strip()


def compute_edgar_concentrations(ticker):
    out = {"filing_type": None, "filing_date": None, "url": None, "excerpt": None, "note": None}
    try:
        import requests
        cik = _resolve_cik(ticker)
        if not cik:
            out["note"] = f"{ticker} 於 SEC company_tickers.json 查無對應 CIK（可能為外國私募發行人/ADR，改申報 20-F/6-K）"
            return out
        r = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=SEC_HEADERS, timeout=20)
        r.raise_for_status()
        sub = r.json()
        recent = sub["filings"]["recent"]
        forms = recent["form"]
        idxs_10q = [i for i, f in enumerate(forms) if f == "10-Q"]
        idxs_10k = [i for i, f in enumerate(forms) if f == "10-K"]
        if idxs_10q:
            i, ftype = idxs_10q[0], "10-Q"
        elif idxs_10k:
            i, ftype = idxs_10k[0], "10-K"
        else:
            out["note"] = f"{ticker} 無 10-Q/10-K（可能為外國私募發行人，改申報 20-F/6-K），本項留 null"
            return out
        accn_raw = recent["accessionNumber"][i]
        accn = accn_raw.replace("-", "")
        doc = recent["primaryDocument"][i]
        fdate = recent["filingDate"][i]
        cik_int = int(cik)
        url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{accn}/{doc}"
        out["filing_type"] = ftype
        out["filing_date"] = fdate
        out["url"] = url

        rr = requests.get(url, headers=SEC_HEADERS, timeout=30)
        rr.raise_for_status()
        text = rr.text
        clean = re.sub(r"<script.*?</script>", " ", text, flags=re.S | re.I)
        clean = re.sub(r"<style.*?</style>", " ", clean, flags=re.S | re.I)
        clean = re.sub(r"<[^>]+>", " ", clean)
        clean = html.unescape(clean)
        clean = re.sub(r"\s+", " ", clean)

        m = _CONCENTRATION_PATTERN.search(clean)
        excerpt = None
        if m:
            excerpt = _snap_excerpt(clean, m.start())
        else:
            m2 = re.search(r"concentrat", clean, re.I)
            if m2:
                excerpt = _snap_excerpt(clean, m2.start())
                out["note"] = (
                    "未命中『accounted for X% of revenue/receivable』specific 句型，"
                    "改取全文第一個含 concentrat 字串的段落——本檔可能未逐條揭露單一客戶營收集中度，"
                    "writer 需自行判讀此段是否足以回答客戶集中度問題（也可能代表該公司客戶分散無須揭露）"
                )
        if excerpt:
            out["excerpt"] = excerpt.strip()[:3000]
        else:
            out["note"] = "filing 全文內找不到 concentration／customer concentration 相關段落"
    except Exception as e:
        out["note"] = f"EDGAR 擷取失敗：{e}"
    return out


# ---------------------------------------------------------------------------
# numbers.latest_quarter_kpis（佔位符，不算，留給採集 agent 填）
# ---------------------------------------------------------------------------

def build_kpi_placeholder(ticker, evidence):
    quarter_label = None
    if evidence:
        header = (evidence.get("numbers") or {}).get("header") or {}
        if isinstance(header, dict):
            for k, v in header.items():
                if "quarter" in k.lower() and isinstance(v, str):
                    quarter_label = v
                    break
    if not quarter_label:
        try:
            np, pd, yf = _lazy_imports()
            t = yf.Ticker(ticker)
            edates = t.earnings_dates
            if edates is not None and not edates.empty:
                now = pd.Timestamp.now(tz=edates.index.tz)
                past = edates[edates.index <= now]
                if not past.empty:
                    last = past.index.max()
                    quarter_label = f"quarter ended around {last.date()}（標籤未定，需人工確認正式季別）"
        except Exception:
            pass
    return {"_required": True, "quarter": quarter_label, "items": []}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("date", help="YYYYMMDD")
    ap.add_argument("--peers", help="逗號分隔 ticker 清單；未給則嘗試從 --evidence 的 numbers.peer_valuation 取")
    ap.add_argument("--evidence", help="既有 evidence.json 路徑（供 peers 回退取值＋latest_quarter_kpis 季別）")
    ap.add_argument("--out", default=str(ROOT / ".dd_build" / "evidence_parts" / "numbers_extra.json"))
    args = ap.parse_args(argv)

    try:
        date_dt = datetime.strptime(args.date, "%Y%m%d")
    except ValueError:
        raise SystemExit(f"date 格式須為 YYYYMMDD，收到：{args.date!r}")

    evidence = None
    if args.evidence:
        try:
            evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[warn] 讀取 --evidence 失敗（不影響其餘欄位）：{e}", file=sys.stderr)

    peers = _resolve_peers(args)

    numbers = {}
    print(f"[dd_numbers_extra] {args.ticker} {args.date} peers={peers or '(none)'}", file=sys.stderr)

    print("  -> price_at_dd / price_as_of / earnings_recency (flat) ...", file=sys.stderr)
    price_at_dd, price_as_of, earnings_recency = compute_price_and_earnings_recency(args.ticker, date_dt)
    numbers["price_at_dd"] = price_at_dd
    numbers["price_as_of"] = price_as_of
    numbers["earnings_recency"] = earnings_recency

    print("  -> valuation_history ...", file=sys.stderr)
    numbers["valuation_history"] = compute_valuation_history(args.ticker, date_dt)

    print("  -> momentum_26w ...", file=sys.stderr)
    idx_benchmark = None
    if evidence:
        idx_benchmark = (evidence.get("numbers") or {}).get("idx_benchmark")
    numbers["momentum_26w"] = compute_momentum_26w(args.ticker, idx_benchmark)

    print("  -> consensus_revision ...", file=sys.stderr)
    numbers["consensus_revision"] = compute_consensus_revision(args.ticker, date_dt)

    print("  -> peer_financials ...", file=sys.stderr)
    if not peers:
        numbers["peer_financials"] = {
            args.ticker: _ttm_financials(args.ticker),
            "_note": "未給 --peers 且 --evidence 無 numbers.peer_valuation 可回退，只算自身一列",
        }
    else:
        numbers["peer_financials"] = compute_peer_financials(args.ticker, peers)

    print("  -> edgar_concentrations ...", file=sys.stderr)
    numbers["edgar_concentrations"] = compute_edgar_concentrations(args.ticker)

    print("  -> latest_quarter_kpis (placeholder) ...", file=sys.stderr)
    numbers["latest_quarter_kpis"] = build_kpi_placeholder(args.ticker, evidence)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"numbers": numbers}
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"寫入 {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
