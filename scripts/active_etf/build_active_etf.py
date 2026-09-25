#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 scripts/active_etf/fetch_holdings.py 存下的官方持股(data/active_etf/holdings/
{code}.jsonl)+ TWSE AUM(data/active_etf/aum/{date}.json)組裝成 /active-etf/ 頁面
要讀的 JSON(docs/active-etf/data/{code}.json + overview.json)。

**EPS/股價/加權遠期本益比一律重用 scripts/etf_dash/build_etf_dash.py 的既有函式**
(import,不重寫):
    classify_revision            期間修正%分類(basis 排除/封頂規則)
    compute_weighted_forward_pe  調和平均加權遠期本益比(3x-300x guard)
    decide_mode                  FULL(週六)/PRICE(其他日)判斷
    fetch_ticker_eps_and_price   單檔 yfinance eps_trend + fast_info
    fetch_etf_price_history      ETF 自身股價history
    fetch_prices_batch           PRICE 模式批次股價
    PERIOD_DEFS                  30d/60d/90d(≈1M/2M/3M)三期間定義
本檔案只負責 active-etf 特有的部分,不重做 EPS/股價機械:
    - 從自家 holdings jsonl 讀最新持股 + 任一歷史日期(供經理人異動比較)
    - EPS cache 用「每檔股票一個檔案」(data/active_etf/eps_cache/{ticker}.json),
      22 檔基金持股高度重疊台股,同一檔股票只抓一次 yfinance,天天重用;首次
      建置會先嘗試從 data/etf_dash/eps_cache/TAIEX.json 的 tickers dict 讀「已經
      抓過的」eps_trend 結果暖啟動(新鮮:eps_as_of 為今天或近 3 天內),沒有才
      真的打 yfinance——這是「重用 eps_cache,不重打已經抓過的」的字面實作。
    - 經理人異動(manager moves):比較兩個時間點的持股,優先用「股數 ÷ 已發行
      單位數」比值(排除純粹因申購/買回造成的規模縮放,見 compute_manager_moves()
      docstring),units 缺其中一邊時退回權重(weight_pct)差值。
    - active share vs 0050:½ Σ|w_fund - w_0050|(聯集),0050 權重讀
      docs/etf-dash/data/0050.json。
    - 跨基金 consensus moves:整週/整月各檔經理人異動,依「幾檔基金同向」計數
      + AUM 加權求和。
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "etf_dash"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "active_etf"))

import build_etf_dash as etfdash  # noqa: E402  — 見模組 docstring,重用其 EPS/股價機械
import fetch_holdings as fh  # noqa: E402       — FUND_REGISTRY / read_fund_jsonl / expand_holdings

DATA_DIR = REPO_ROOT / "docs" / "active-etf" / "data"
EPS_CACHE_DIR = REPO_ROOT / "data" / "active_etf" / "eps_cache"
GLOBAL_META_PATH = EPS_CACHE_DIR / "_meta.json"
ETF_DASH_DATA_DIR = REPO_ROOT / "docs" / "etf-dash" / "data"
AUM_DIR = REPO_ROOT / "data" / "active_etf" / "aum"

MOVE_WEIGHT_MIN_DELTA_PP = 0.10   # 權重法門檻:|Δweight_pct| < 此值視為雜訊,不算異動
MOVE_SHARE_RATIO_MIN_DELTA = 0.05  # 股數/單位法門檻:比值相對變化 < 5% 視為雜訊


# ── EPS 快取(每檔股票一個檔案,22 檔基金共用) ──────────────────────────────
def _cache_path(ticker):
    return EPS_CACHE_DIR / "{}.json".format(ticker.replace("/", "_"))


def load_ticker_cache(ticker):
    p = _cache_path(ticker)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def save_ticker_cache(ticker, data):
    EPS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _cache_path(ticker).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def warm_start_from_etf_dash(max_age_days=3):
    """把 data/etf_dash/eps_cache/{TAIEX,0050}.json 裡「新鮮」的 tickers 記錄
    預先寫進我們自己的 per-ticker 快取(還沒有才寫,不覆蓋),減少重複打
    yfinance。TAIEX/0050 本身也是台股,跟我們 22 檔基金的持股高度重疊。"""
    today = datetime.date.today()
    n_warmed = 0
    for src_key in ("TAIEX", "0050"):
        path = ETF_DASH_DATA_DIR / "{}.json".format(src_key)
        if not path.exists():
            continue
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        eps_as_of = d.get("eps_as_of")
        try:
            age = (today - datetime.date.fromisoformat(eps_as_of)).days
        except (TypeError, ValueError):
            continue
        if age > max_age_days:
            continue
        tickers = d.get("tickers") or {}
        # etf-dash 的 chart data 檔案不一定含 per-ticker tickers dict(那份在
        # eps_cache/{key}.json,不是 docs/etf-dash/data/{key}.json)——兩個目錄
        # 都試,存在才用。
        if not tickers:
            cache_path = REPO_ROOT / "data" / "etf_dash" / "eps_cache" / "{}.json".format(src_key)
            if cache_path.exists():
                try:
                    tickers = (json.loads(cache_path.read_text(encoding="utf-8")) or {}).get("tickers") or {}
                except (OSError, ValueError):
                    tickers = {}
        for ticker, rec in tickers.items():
            if load_ticker_cache(ticker) is not None:
                continue
            if rec.get("status") != "ok" or rec.get("eps_fy_next_local") is None:
                continue
            save_ticker_cache(ticker, dict(rec, eps_as_of=eps_as_of, warm_started_from=src_key))
            n_warmed += 1
    return n_warmed


def get_eps_for_ticker(ticker, mode, eps_as_of_today, pace_sec=None):
    """PRICE 模式:有快取就用(不論新鮮度,EPS 預估本身變動慢);FULL 模式:今天
    還沒重抓過(cache 的 eps_as_of != 今天)才重抓——22 檔基金持股高度重疊,
    同一輪 FULL 跑下來,同一檔股票被好幾檔基金共用時只在第一次遇到時真的打
    yfinance,之後那幾檔基金直接讀本輪已經寫回的快取,不會重複呼叫。兩種模式
    都沒抓到資料回 None(呼叫端跳過該檔,不計入 EPS 覆蓋率)。"""
    cached = load_ticker_cache(ticker)
    if cached and cached.get("status") == "ok" and cached.get("eps_as_of") == eps_as_of_today:
        return cached  # 本輪(或今天稍早)已經重抓過,直接重用
    if mode == "price" and cached and cached.get("status") == "ok":
        return cached
    data = etfdash.fetch_ticker_eps_and_price(ticker)
    data["eps_as_of"] = eps_as_of_today
    save_ticker_cache(ticker, data)
    time.sleep(pace_sec if pace_sec is not None else etfdash.TICKER_FETCH_PACING_S)
    return data


# ── /stock-dash/ 連結 ────────────────────────────────────────────────────
# /stock-dash/ 只給 docs/dd-screener/latest.json 裡的 ticker 建頁(沿用 etf_dash 的
# load_stock_dash_universe())。dd-screener 對部分上櫃股用 .TW 後綴(如 5274.TW),
# 我們的持股依 TPEx 清單標 .TWO——兩種後綴都比對,連結用 dd-screener 那一種。
_STOCK_DASH = None


def stock_dash_ticker(ticker):
    global _STOCK_DASH
    if _STOCK_DASH is None:
        _STOCK_DASH = etfdash.load_stock_dash_universe()
    if ticker in _STOCK_DASH:
        return ticker
    base = ticker.rsplit(".", 1)[0]
    for alt in (base + ".TW", base + ".TWO"):
        if alt in _STOCK_DASH:
            return alt
    return None


# ── 經理人異動(manager moves) ────────────────────────────────────────────
def compute_manager_moves(current_snap, past_snap):
    """比較兩個 jsonl 快照(compact schema,見 fetch_holdings.py 模組 docstring)
    的持股,回傳 {new, exit, increase, decrease}(各為 list,依 |變動| 降冪)。

    方法:優先用「股數 ÷ 已發行受益權單位數(nav.units)」比值——這個比值只在
    經理人真的改變持股/單位比例時才會動,單純申購/買回(單位數與股數同比例
    縮放)不會讓比值改變,藉此濾掉「基金變大/變小」這種非經理人主動決策的
    雜訊。兩個快照的 nav.units 都要有值才能用這個方法;缺任一邊就退回用
    weight_pct 差值(較粗略——weight_pct 本身也會被股價漲跌影響,不是純持股
    訊號,但至少方向大致對得上,見頁面方法論段落)。
    """
    cur_h = {r[0]: r[1] for r in current_snap["holdings"]}  # ticker -> shares
    past_h = {r[0]: r[1] for r in past_snap["holdings"]}
    cur_w = {r[0]: r[2] for r in current_snap["holdings"]}  # ticker -> weight_pct
    past_w = {r[0]: r[2] for r in past_snap["holdings"]}
    cur_units = (current_snap.get("nav") or {}).get("units")
    past_units = (past_snap.get("nav") or {}).get("units")
    use_shares_method = bool(cur_units and past_units)

    out = {"new": [], "exit": [], "increase": [], "decrease": [], "method": None}
    all_tickers = set(cur_h) | set(past_h)
    for t in all_tickers:
        in_cur, in_past = t in cur_h, t in past_h
        w_now, w_before = cur_w.get(t), past_w.get(t)
        if in_cur and not in_past:
            out["new"].append({"ticker": t, "weight_pct": w_now})
            continue
        if in_past and not in_cur:
            out["exit"].append({"ticker": t, "weight_pct_before": w_before})
            continue
        # 兩邊都有:判斷是加碼還是減碼
        if use_shares_method:
            ratio_now = cur_h[t] / cur_units
            ratio_before = past_h[t] / past_units
            if ratio_before == 0:
                continue
            rel_delta = (ratio_now / ratio_before) - 1
            if abs(rel_delta) < MOVE_SHARE_RATIO_MIN_DELTA:
                continue
            rec = {"ticker": t, "weight_pct": w_now, "weight_pct_before": w_before,
                   "shares_per_unit_change_pct": round(rel_delta * 100, 2)}
            (out["increase"] if rel_delta > 0 else out["decrease"]).append(rec)
        else:
            if w_now is None or w_before is None:
                continue
            delta = w_now - w_before
            if abs(delta) < MOVE_WEIGHT_MIN_DELTA_PP:
                continue
            rec = {"ticker": t, "weight_pct": w_now, "weight_pct_before": w_before,
                   "weight_pct_change_pp": round(delta, 4)}
            (out["increase"] if delta > 0 else out["decrease"]).append(rec)
    out["method"] = "shares_per_unit" if use_shares_method else "weight_pct_delta"
    sort_key = ((lambda r: abs(r.get("shares_per_unit_change_pct", 0))) if use_shares_method
                else (lambda r: abs(r.get("weight_pct_change_pp", 0))))
    out["increase"].sort(key=sort_key, reverse=True)
    out["decrease"].sort(key=sort_key, reverse=True)
    out["new"].sort(key=lambda r: r["weight_pct"] or 0, reverse=True)
    out["exit"].sort(key=lambda r: r["weight_pct_before"] or 0, reverse=True)
    return out


def snapshot_near(snapshots, target_date):
    """snapshots 依 as_of 升冪排序;回傳 as_of <= target_date 裡最新的一筆(找不到回 None)。"""
    candidates = [s for s in snapshots if s["as_of"] <= target_date]
    return candidates[-1] if candidates else None


def fund_moves(code, snapshots):
    """回傳 {week: moves_dict|None, month: moves_dict|None, since_earliest: moves_dict|None}。"""
    if not snapshots:
        return {"week": None, "month": None, "since_earliest": None}
    current = snapshots[-1]
    today = datetime.date.fromisoformat(current["as_of"])
    week_ago = snapshot_near(snapshots[:-1], (today - datetime.timedelta(days=7)).isoformat())
    month_ago = snapshot_near(snapshots[:-1], (today - datetime.timedelta(days=30)).isoformat())
    earliest = snapshots[0] if snapshots[0] is not current else None
    return {
        "week": compute_manager_moves(current, week_ago) if week_ago else None,
        "month": compute_manager_moves(current, month_ago) if month_ago else None,
        "since_earliest": compute_manager_moves(current, earliest) if earliest else None,
        "week_base_date": week_ago["as_of"] if week_ago else None,
        "month_base_date": month_ago["as_of"] if month_ago else None,
        "since_earliest_base_date": earliest["as_of"] if earliest else None,
    }


# ── active share vs 0050 ─────────────────────────────────────────────────
def load_0050_weights():
    """讀 docs/etf-dash/data/0050.json 的成分股權重(ticker -> weight_pct)。找
    不到檔案或格式不對回空 dict(active share 該檔會是 None,不是 0——見呼叫端)。"""
    path = ETF_DASH_DATA_DIR / "0050.json"
    if not path.exists():
        return {}, None
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}, None
    out = {}
    for c in d.get("constituents") or []:
        if c.get("ticker") and c.get("weight_pct") is not None:
            out[c["ticker"]] = c["weight_pct"]
    return out, d.get("holdings_as_of")


def active_share(fund_weights, bench_weights):
    """½ Σ|w_fund - w_bench|(聯集,缺的一邊當 0)。回傳百分比(0-100)。"""
    if not bench_weights:
        return None
    tickers = set(fund_weights) | set(bench_weights)
    total = sum(abs(fund_weights.get(t, 0) - bench_weights.get(t, 0)) for t in tickers)
    return round(total / 2, 2)


# ── 單一基金組裝 ──────────────────────────────────────────────────────────
def build_fund(code, mode, bench_0050_weights, aum_by_code, pace_sec):
    info = fh.FUND_REGISTRY[code]
    snapshots = fh.read_fund_jsonl(code)
    if not snapshots:
        return None, "沒有已存持股快照(尚未跑過 fetch_holdings.py)"
    current = snapshots[-1]
    names = json.loads(fh.NAMES_PATH.read_text(encoding="utf-8")) if fh.NAMES_PATH.exists() else {}
    holdings = fh.expand_holdings(current["holdings"], names)
    other = fh.expand_other(current["other"])
    # ETF 本身一律用 .TW(22 檔全數上市,非上櫃;成分股才會有 .TWO)。
    yf_ticker = code + ".TW"

    today_iso = current["as_of"]
    eps_today = 0
    price_today = 0
    constituents = []
    for h in holdings:
        eps_data = get_eps_for_ticker(h["ticker"], mode, today_iso, pace_sec)
        c = dict(h, eps_status=eps_data.get("status") if eps_data else "fetch_failed")
        if eps_data and eps_data.get("status") == "ok":
            c["eps_fy_next_local"] = eps_data.get("eps_fy_next_local")
            c["eps_currency"] = eps_data.get("eps_currency")
            c["price_local"] = eps_data.get("price")
            c["anchors"] = eps_data.get("eps_fy_next_anchors_local") or eps_data.get("anchors") or {}
            # compute_weighted_forward_pe()/classify_revision() 是通用(非美股限定)純函式,
            # 只認 *_usd 這個欄位名——我們全部持股都是 TWD 計價,直接把本地值當「基準幣別」
            # 傳進去,不做真的美元換算(基準幣別=TWD,只是沿用對方的欄位命名)。
            c["eps_fy_next_usd"] = eps_data.get("eps_fy_next_local")
            c["price_usd"] = eps_data.get("price")
            for key, _col, _label, _days in etfdash.PERIOD_DEFS:
                base = (c["anchors"] or {}).get(key)
                status, reason, raw_pct, capped_pct = etfdash.classify_revision(base, c["eps_fy_next_local"])
                c.setdefault("revisions_pct", {})[key] = capped_pct
        constituents.append(c)

    total_weight = sum(h["weight_pct"] for h in holdings)
    weighted_fwd_pe, pe_coverage_pct, pe_excluded = etfdash.compute_weighted_forward_pe(constituents, total_weight)

    price_series = etfdash.fetch_etf_price_history(yf_ticker, calendar_days=200)
    today_price_pt = price_series[-1] if price_series else None

    periods = []
    for key, _col, label, days in etfdash.PERIOD_DEFS:
        covered = [c for c in constituents if (c.get("revisions_pct") or {}).get(key) is not None]
        covered_weight = sum(c["weight_pct"] or 0 for c in covered)
        eps_chg_pct = None
        if covered_weight > 0:
            eps_chg_pct = round(sum((c["weight_pct"] / covered_weight) * c["revisions_pct"][key]
                                     for c in covered), 4)
        anchor_date = (datetime.date.fromisoformat(today_iso) - datetime.timedelta(days=days)).isoformat()
        anchor_pt = etfdash._closest_close_on_or_before(price_series, anchor_date)
        price_chg_pct = None
        if anchor_pt and today_price_pt and anchor_pt["close"]:
            price_chg_pct = round((today_price_pt["close"] / anchor_pt["close"] - 1) * 100, 4)
        implied_pe_chg_pct = None
        if eps_chg_pct is not None and price_chg_pct is not None:
            eps_factor = 1 + eps_chg_pct / 100
            if eps_factor != 0:
                implied_pe_chg_pct = round(((1 + price_chg_pct / 100) / eps_factor - 1) * 100, 4)
        periods.append({"key": key, "label": label, "days": days,
                         "base_date": anchor_pt["date"] if anchor_pt else None,
                         "eps_chg_pct": eps_chg_pct, "price_chg_pct": price_chg_pct,
                         "implied_pe_chg_pct": implied_pe_chg_pct,
                         "coverage_pct": round(covered_weight / total_weight * 100, 2) if total_weight else None})

    p90 = next((p for p in periods if p["key"] == "90d"), {})

    # 簡化版「anchor line」(呼應 etf-dash 的 anchor_history 4 點 fallback 概念,
    # 但不重建整套持久化 run 快照機制——用我們自己已經算好的 periods 反推每個
    # 錨點當時的相對水準:今天=100,N 天前 = 100/(1+該期間變動%))。股價/EPS
    # 兩條線都在今天訂為 100,可以直接比誰漲得快,跟 etf-dash Exhibit 2 同樣的
    # 讀法。
    chart_points = []
    for p in periods:
        if p["eps_chg_pct"] is not None and p["price_chg_pct"] is not None and p["base_date"]:
            eps_factor, price_factor = 1 + p["eps_chg_pct"] / 100, 1 + p["price_chg_pct"] / 100
            chart_points.append({
                "date": p["base_date"],
                "eps_index": round(100 / eps_factor, 2) if eps_factor else None,
                "price_index": round(100 / price_factor, 2) if price_factor else None,
            })
    chart_points.sort(key=lambda x: x["date"])
    if chart_points:
        chart_points.append({"date": today_iso, "eps_index": 100.0, "price_index": 100.0})

    moves = fund_moves(code, snapshots)
    for w in ("week", "month", "since_earliest"):
        for kind in ("new", "exit", "increase", "decrease"):
            for rec in (moves.get(w) or {}).get(kind, []):
                rec["name"] = names.get(rec["ticker"])
                rec["stock_dash_ticker"] = stock_dash_ticker(rec["ticker"])
    top10 = sorted(holdings, key=lambda h: h["weight_pct"], reverse=True)[:10]
    top10_pct = round(sum(h["weight_pct"] for h in top10), 2)
    tsmc = next((h for h in holdings if h["ticker"] == "2330.TW"), None)
    fund_weights = {h["ticker"]: h["weight_pct"] for h in holdings}
    ashare = active_share(fund_weights, bench_0050_weights)

    aum_row = aum_by_code.get(code) or {}

    # 持股明細表要的逐檔欄位:EPS 現值/3 個月修正%(從 constituents 帶回,原本只
    # 進加總沒進 JSON,頁面整欄顯示無資料)+ 相對「約一個月前」快照的權重變動
    # (pp;沒有一個月前的快照就退回最早一筆,基準日一併寫出)。
    by_ticker = {c["ticker"]: c for c in constituents}
    ref_snap = (snapshot_near(snapshots[:-1], (datetime.date.fromisoformat(today_iso)
                                               - datetime.timedelta(days=30)).isoformat())
                or (snapshots[0] if len(snapshots) > 1 else None))
    ref_w = {r[0]: r[2] for r in ref_snap["holdings"]} if ref_snap else None
    holdings_out = []
    for h in holdings:
        c = by_ticker.get(h["ticker"], {})
        rev = c.get("revisions_pct") or {}
        holdings_out.append(dict(
            h, eps_fy_next_local=c.get("eps_fy_next_local"),
            revisions_pct={"30d": rev.get("30d"), "90d": rev.get("90d")},
            weight_change_pp=(round(h["weight_pct"] - ref_w.get(h["ticker"], 0.0), 4)
                              if ref_w is not None else None),
            stock_dash_ticker=stock_dash_ticker(h["ticker"])))

    return {
        "code": code, "name": info["name"], "issuer": info["issuer"], "yf_ticker": yf_ticker,
        "as_of": today_iso, "mode": mode,
        "holdings_as_of": today_iso, "n_holdings": len(holdings),
        "holdings": holdings_out, "other": other,
        "weight_change_base_date": ref_snap["as_of"] if ref_snap else None,
        "nav": current.get("nav") or {}, "weight_band_note": current.get("weight_band_note"),
        "source_url": current.get("source_url"),
        "twse_aum": {"aum_100m_twd": aum_row.get("aum_100m_twd"),
                     "holders_10k_people": aum_row.get("holders_10k_people"),
                     "as_of": aum_row.get("as_of")},
        "price": today_price_pt, "chart_points": chart_points,
        "periods": periods,
        "weighted_forward_pe": {"value": weighted_fwd_pe, "coverage_pct": pe_coverage_pct,
                                 "pe_excluded": pe_excluded},
        "eps_chg_pct_30d": periods[0]["eps_chg_pct"] if len(periods) > 0 else None,
        "eps_chg_pct_90d": p90.get("eps_chg_pct"), "price_chg_pct_90d": p90.get("price_chg_pct"),
        "implied_pe_chg_pct_90d": p90.get("implied_pe_chg_pct"),
        "top10_concentration_pct": top10_pct, "top10": top10,
        "tsmc_weight_pct": tsmc["weight_pct"] if tsmc else 0.0,
        "active_share_vs_0050_pct": ashare,
        "moves": moves,
        "n_snapshots_stored": len(snapshots), "earliest_stored_date": snapshots[0]["as_of"],
        "methods_note_zh": (
            "股票持股與資料日一律取自基金官方 PCF/持股揭露頁(見 source_url),不依賴任何第三方彙整站。"
            "EPS 預估、股價、加權遠期本益比機械沿用 scripts/etf_dash/build_etf_dash.py 既有規則"
            "(yfinance Ticker.eps_trend 明年度估計、個股遠期本益比 3x-300x guard、期間修正% 的基期"
            "排除/±50%封頂)。經理人異動優先用「股數÷已發行受益權單位數」比值判斷(排除純申購/買回"
            "縮放),兩邊快照缺 nav.units 才退回權重(weight_pct)差值——本檔 moves.week/month 的 "
            "method 欄位會標示實際用了哪一種。active share 為 ½Σ|本基金權重-元大台灣50權重|(聯集),"
            "元大台灣50權重讀 /etf-dash/ 資料,若當天缺資料則為 null。"
        ),
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }, None


# ── 跨基金 consensus moves ──────────────────────────────────────────────
def build_consensus(fund_results, window_key):
    """window_key: 'week' 或 'month'。回傳依「淨買超基金數」排序的買超/賣超清單,
    每筆含 ticker/name/n_funds_buy/n_funds_sell/net_funds/sum_weight_change_pp/
    aum_weighted_score(以 twse_aum.aum_100m_twd 加權的權重變動總和,粗略反映
    「越大的基金動作,訊號權重越高」)。純計數+加總,機械語句,不下判斷字眼。"""
    agg = {}
    for f in fund_results:
        moves = (f.get("moves") or {}).get(window_key)
        if not moves:
            continue
        aum = (f.get("twse_aum") or {}).get("aum_100m_twd") or 0
        for rec in moves.get("new", []) + moves.get("increase", []):
            t = rec["ticker"]
            a = agg.setdefault(t, {"ticker": t, "n_funds_buy": 0, "n_funds_sell": 0,
                                    "sum_weight_change_pp": 0.0, "aum_weighted_score": 0.0, "funds": []})
            delta = rec.get("weight_pct_change_pp")
            if delta is None:
                delta = (rec.get("weight_pct") or 0) - (rec.get("weight_pct_before") or 0)
            a["n_funds_buy"] += 1
            a["sum_weight_change_pp"] += delta or 0
            a["aum_weighted_score"] += (delta or 0) * aum
            a["funds"].append(f["code"])
        for rec in moves.get("exit", []) + moves.get("decrease", []):
            t = rec["ticker"]
            a = agg.setdefault(t, {"ticker": t, "n_funds_buy": 0, "n_funds_sell": 0,
                                    "sum_weight_change_pp": 0.0, "aum_weighted_score": 0.0, "funds": []})
            delta = rec.get("weight_pct_change_pp")
            if delta is None:
                base = rec.get("weight_pct_before") or 0
                delta = (rec.get("weight_pct") or 0) - base if "weight_pct" in rec else -base
            a["n_funds_sell"] += 1
            a["sum_weight_change_pp"] += delta or 0
            a["aum_weighted_score"] += (delta or 0) * aum
            a["funds"].append(f["code"])
    rows = list(agg.values())
    for r in rows:
        r["net_funds"] = r["n_funds_buy"] - r["n_funds_sell"]
    bought = sorted([r for r in rows if r["net_funds"] > 0], key=lambda r: (r["net_funds"], r["aum_weighted_score"]), reverse=True)
    sold = sorted([r for r in rows if r["net_funds"] < 0], key=lambda r: (r["net_funds"], -r["aum_weighted_score"]))
    return {"bought": bought[:20], "sold": sold[:20]}


# ── overview + main ───────────────────────────────────────────────────────
def load_benchmark_rows():
    """讀 docs/etf-dash/data/{0050,TAIEX}.json,萃取跟主動式 ETF 同樣的幾個欄位,
    當成總覽表格的兩列基準指標(issuer 標「Benchmark」,不是主動式 ETF,前端
    需要用這個欄位跟真正的基金分開處理排序/連結)。任一檔讀不到就跳過,不讓
    整份總覽失敗。"""
    rows = []
    for key, code_label, name in (("0050", "0050", "元大台灣50"), ("TAIEX", "TAIEX", "台灣加權指數")):
        path = ETF_DASH_DATA_DIR / "{}.json".format(key)
        if not path.exists():
            continue
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        periods = {p["key"]: p for p in d.get("periods") or []}
        p30, p90 = periods.get("30d", {}), periods.get("90d", {})
        rows.append({
            "code": code_label, "name": d.get("label_zh") or name, "issuer": "Benchmark",
            "as_of": d.get("as_of"), "n_holdings": d.get("n_holdings"),
            "eps_chg_pct_30d": p30.get("eps_chg_pct"), "eps_chg_pct_90d": p90.get("eps_chg_pct"),
            "price_chg_pct_90d": p90.get("price_chg_pct"), "implied_pe_chg_pct_90d": p90.get("implied_pe_chg_pct"),
            "weighted_forward_pe": (d.get("weighted_forward_pe") or {}).get("value"),
            "aum_100m_twd": None, "holders_10k_people": None,
            "top10_concentration_pct": None, "tsmc_weight_pct": None, "active_share_vs_0050_pct": None,
            "is_benchmark": True,
        })
    return rows


def build_overview(fund_results):
    funds = []
    for f in fund_results:
        funds.append({
            "code": f["code"], "name": f["name"], "issuer": f["issuer"],
            "as_of": f["as_of"], "n_holdings": f["n_holdings"],
            "eps_chg_pct_30d": f["eps_chg_pct_30d"], "eps_chg_pct_90d": f["eps_chg_pct_90d"],
            "price_chg_pct_90d": f["price_chg_pct_90d"], "implied_pe_chg_pct_90d": f["implied_pe_chg_pct_90d"],
            "weighted_forward_pe": (f.get("weighted_forward_pe") or {}).get("value"),
            "aum_100m_twd": (f.get("twse_aum") or {}).get("aum_100m_twd"),
            "holders_10k_people": (f.get("twse_aum") or {}).get("holders_10k_people"),
            "top10_concentration_pct": f["top10_concentration_pct"], "tsmc_weight_pct": f["tsmc_weight_pct"],
            "active_share_vs_0050_pct": f["active_share_vs_0050_pct"], "is_benchmark": False,
        })
    funds.sort(key=lambda f: f.get("aum_100m_twd") or 0, reverse=True)
    funds.extend(load_benchmark_rows())
    names = json.loads(fh.NAMES_PATH.read_text(encoding="utf-8")) if fh.NAMES_PATH.exists() else {}
    consensus = {w: build_consensus(fund_results, w) for w in ("week", "month")}
    for c in consensus.values():
        for r in c["bought"] + c["sold"]:
            r["name"] = names.get(r["ticker"])
            r["stock_dash_ticker"] = stock_dash_ticker(r["ticker"])
    return {
        "funds": funds,
        "consensus_week": consensus["week"],
        "consensus_month": consensus["month"],
        "as_of": max((f["as_of"] for f in fund_results), default=None),
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }


def load_global_eps_meta():
    if GLOBAL_META_PATH.exists():
        try:
            return json.loads(GLOBAL_META_PATH.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
    return None


def save_global_eps_meta(eps_as_of):
    EPS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    GLOBAL_META_PATH.write_text(json.dumps({"eps_as_of": eps_as_of}, ensure_ascii=False), encoding="utf-8")


def load_aum_latest():
    if not AUM_DIR.exists():
        return {}
    files = sorted(AUM_DIR.glob("*.json"))
    if not files:
        return {}
    rows = json.loads(files[-1].read_text(encoding="utf-8"))
    return {r["code"]: r for r in rows if r.get("code")}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", help="逗號分隔代號子集")
    ap.add_argument("--mode", choices=["auto", "full", "price"], default="auto")
    ap.add_argument("--pace", type=float, default=0.4)
    args = ap.parse_args()
    codes = [c.strip() for c in args.only.split(",")] if args.only else list(fh.FUND_REGISTRY)

    meta = load_global_eps_meta()
    now_taipei = etfdash.taipei_now()
    mode, reason = etfdash.decide_mode(args.mode, meta, now_taipei)
    print("mode={} ({})".format(mode, reason))
    if mode == "full":
        n = warm_start_from_etf_dash()
        print("warm-started {} tickers from etf-dash eps_cache".format(n))

    bench_weights, bench_as_of = load_0050_weights()
    aum_by_code = load_aum_latest()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for code in codes:
        try:
            fund, err = build_fund(code, mode, bench_weights, aum_by_code, args.pace)
        except Exception as e:  # noqa: BLE001 — 單檔失敗不能讓整批掛掉
            fund, err = None, str(e)
        if err:
            print("FAIL {}: {}".format(code, err), file=sys.stderr)
            continue
        results.append(fund)
        (DATA_DIR / "{}.json".format(code)).write_text(
            json.dumps(fund, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("OK   {} eps90={} price90={} fwdpe={} moves(week new/inc/dec/exit)={}/{}/{}/{}".format(
            code, fund["eps_chg_pct_90d"], fund["price_chg_pct_90d"],
            (fund["weighted_forward_pe"] or {}).get("value"),
            len((fund["moves"]["week"] or {}).get("new", [])) if fund["moves"]["week"] else "-",
            len((fund["moves"]["week"] or {}).get("increase", [])) if fund["moves"]["week"] else "-",
            len((fund["moves"]["week"] or {}).get("decrease", [])) if fund["moves"]["week"] else "-",
            len((fund["moves"]["week"] or {}).get("exit", [])) if fund["moves"]["week"] else "-"))

    if not results:
        print("no funds built successfully", file=sys.stderr)
        return 1

    overview = build_overview(results)
    (DATA_DIR / "overview.json").write_text(
        json.dumps(overview, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if mode == "full":
        save_global_eps_meta(overview["as_of"])

    print("\n完成: {}/{} 檔".format(len(results), len(codes)))
    return 0 if len(results) == len(codes) else (1 if len(results) < len(codes) - 5 else 0)


if __name__ == "__main__":
    sys.exit(main())
