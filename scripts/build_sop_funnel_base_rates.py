#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_sop_funnel_base_rates.py — sop-funnel 板機訊號 producer 的 base rate 機械餵料
（市況主控台設計稿 §9，包 F1）。

供 scripts/generate_sop_funnel_forecasts.py 讀表用，輸出 data/sop_funnel_base_rates.json：

  對 docs/dd-screener/sop-funnel/backtest.json 的 `trades_charter[]`（53 筆，2021–2026，
  態①-⑤ SOP 規則的歷史質量閘門回測），每筆 trade 取
    - ticker 在 entry_date 當日或之前的最近週線收盤（data/weekly_cache/<ticker>.json）
    - ticker 在 entry_date + 91 曆日 當日或之前的最近週線收盤
    - SPY 在同兩個日期的收盤（data/dd_verdict_base_rates_raw_cache.json，本檔唯讀，
      由 scripts/build_dd_verdict_base_rates.py 維護，不在此重抓）
  hit = ticker 報酬 > SPY 同窗報酬；freq_beat_91d = pooled hit 頻率（跨全部有效 trade）。

  by_type（A1／A2／B）僅供觀察列出，**不採**——producer（generate_sop_funnel_forecasts.py）
  只讀 pooled freq_beat_91d，設計稿 §9 明文「by_type 只列不採」。

  n_valid < 30 時 producer 改用 PREREG 0.58（本檔只誠實報告 n_valid，不做該項判斷；判斷邏輯
  在 producer 端，理由同 scripts/build_dd_verdict_base_rates.py 與其 producer 的 CONFIG 分工）。

視窗到期判斷：ticker 與 SPY 兩邊最後一根資料日皆須 ≥ 目標日（entry_date + 91），否則整筆
trade 跳過，不用「離目標日很遠的最近可得收盤」偷渡（照抄 knowledge/settle_outcomes.py /
scripts/build_dd_verdict_base_rates.py 既有慣例）。

無網路存取：本檔完全離線——backtest.json、weekly_cache、dd_verdict_base_rates_raw_cache.json
三者皆為既有本地檔案，不呼叫 yfinance／stooq／任何 HTTP。

用法
----
  python scripts/build_sop_funnel_base_rates.py            重算（完全離線）
  python scripts/build_sop_funnel_base_rates.py --if-due    現有輸出 built_at <85 天則跳過
  python scripts/build_sop_funnel_base_rates.py --out PATH  輸出路徑（測試用）
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"
CACHE_DIR = DATA / "weekly_cache"
BACKTEST = DOCS / "dd-screener" / "sop-funnel" / "backtest.json"
RAW_CACHE = DATA / "dd_verdict_base_rates_raw_cache.json"   # 唯讀，build_dd_verdict_base_rates.py 維護
DD_BASE_RATES = DATA / "dd_verdict_base_rates.json"         # 唯讀，同上
OUT_JSON = DATA / "sop_funnel_base_rates.json"

SCHEMA = "sop-funnel-base-rates-v1"
HORIZON_DAYS = 91                 # PREREG 凍結（設計稿 §9 F1）
N_VALID_MIN = 30                  # PREREG 凍結：n_valid ≥ 30 用表，否則 producer 端退回 0.58
PREREG_FALLBACK_P = 0.58
IF_DUE_MAX_AGE_DAYS = 85          # 同 build_dd_verdict_base_rates.py 慣例

# decisions/ledger entity → weekly_cache 檔名（逐字照抄 knowledge/settle_outcomes.py ALIAS）
ALIAS = {
    "5274.TW": "5274.TWO",
    "8299.TW": "8299.TWO",
    "AENA": "AENA.MC",
    "BESI": "BESI.AS",
    "RMS": "RMS.PA",
    "SU": "SU.PA",
    "LVMH": "MC.PA",
    "ABB": "ABBNY",
}


def warn(msg):
    print(f"[sop-funnel-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[sop-funnel-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日期 / 收盤查表工具（逐字照抄 scripts/build_dd_verdict_base_rates.py 語意）
# ═══════════════════════════════════════════════════════════════════════════

def _split(bars):
    return [d for d, _ in bars], [c for _, c in bars]


def _at_or_before(dates, closes, ymd):
    """最近一根 date ≤ ymd 的收盤；無則 None（dates 已升冪排序，bisect 加速）。"""
    idx = bisect.bisect_right(dates, ymd) - 1
    if idx < 0:
        return None
    return dates[idx], closes[idx]


def _plus_days(ymd, n):
    y, m, d = map(int, ymd.split("-"))
    return (date(y, m, d) + timedelta(days=n)).isoformat()


def _load_ticker_bars(path):
    try:
        raw = json.loads(path.read_text(encoding="utf-8")).get("weekly_bars") or []
    except (OSError, json.JSONDecodeError, KeyError):
        return None
    bars = [(b["week_end"], b["close"]) for b in raw if b.get("week_end") and b.get("close")]
    bars.sort(key=lambda x: x[0])
    return bars or None


def _load_spy_raw_cache():
    if not RAW_CACHE.exists():
        raise SystemExit(f"找不到 {RAW_CACHE} —— 先跑 python scripts/build_dd_verdict_base_rates.py"
                          f"（本檔唯讀該快取，不自抓）")
    try:
        data = json.loads(RAW_CACHE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {RAW_CACHE}: {e}")
    bars = (data.get("series") or {}).get("SPY")
    if not bars:
        raise SystemExit(f"{RAW_CACHE} 無 SPY 序列")
    return sorted((d, c) for d, c in bars)


def _load_backtest():
    if not BACKTEST.exists():
        raise SystemExit(f"找不到 {BACKTEST}")
    try:
        return json.loads(BACKTEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {BACKTEST}: {e}")


def _load_dd_p_clim():
    """讀 dd_verdict_base_rates.json 的 p_clim.dd_beat_spy_91d，僅供本檔輸出的
    p_clim_ref 交叉引用（不影響本檔自身的 freq_beat_91d 計算）。缺檔不 crash。"""
    if not DD_BASE_RATES.exists():
        return None, None
    try:
        d = json.loads(DD_BASE_RATES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, None
    return (d.get("p_clim") or {}).get("dd_beat_spy_91d"), d.get("built_at")


# ═══════════════════════════════════════════════════════════════════════════
# 核心計算
# ═══════════════════════════════════════════════════════════════════════════

def compute(trades_charter, spy_dates, spy_closes):
    spy_last = spy_dates[-1] if spy_dates else None
    n_trades = len(trades_charter)
    n_valid = n_hit = 0
    by_type = {}
    skip_counts = Counter()
    bars_cache = {}

    for t in trades_charter:
        ticker = t.get("ticker")
        typ = t.get("type")
        entry_date = t.get("entry_date")
        if not ticker or not entry_date:
            skip_counts["missing_fields"] += 1
            continue

        alias_fname = ALIAS.get(ticker, ticker)
        if alias_fname not in bars_cache:
            path = CACHE_DIR / f"{alias_fname}.json"
            bars_cache[alias_fname] = _load_ticker_bars(path) if path.exists() else None
        bars = bars_cache[alias_fname]
        if not bars:
            skip_counts["ticker_not_in_weekly_cache"] += 1
            continue

        t_dates, t_closes = _split(bars)
        end_date = _plus_days(entry_date, HORIZON_DAYS)

        if t_dates[-1] < end_date:
            skip_counts["window_not_matured_ticker"] += 1
            continue
        if not spy_last or spy_last < end_date:
            skip_counts["window_not_matured_spy"] += 1
            continue

        c0 = _at_or_before(t_dates, t_closes, entry_date)
        c1 = _at_or_before(t_dates, t_closes, end_date)
        s0 = _at_or_before(spy_dates, spy_closes, entry_date)
        s1 = _at_or_before(spy_dates, spy_closes, end_date)
        if not c0 or not c1 or not s0 or not s1:
            skip_counts["missing_close"] += 1
            continue
        _, c0v = c0
        _, c1v = c1
        _, s0v = s0
        _, s1v = s1
        if not c0v or not s0v:
            skip_counts["zero_base_close"] += 1
            continue

        ticker_ret = c1v / c0v - 1.0
        spy_ret = s1v / s0v - 1.0
        hit = ticker_ret > spy_ret

        n_valid += 1
        if hit:
            n_hit += 1
        bt = by_type.setdefault(typ, {"n": 0, "hit": 0})
        bt["n"] += 1
        if hit:
            bt["hit"] += 1

    for typ, bt in by_type.items():
        bt["freq"] = round(bt["hit"] / bt["n"], 4) if bt["n"] else None

    freq = round(n_hit / n_valid, 4) if n_valid else None
    return {
        "n_trades": n_trades,
        "n_valid": n_valid,
        "n_hit": n_hit,
        "freq_beat_91d": freq,
        "by_type": by_type,
        "skip_counts": dict(skip_counts),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(
        description="sop-funnel 板機訊號 producer 的 base rate builder（backtest.json trades_charter "
                     "91 曆日對 SPY pooled 勝率，完全離線）")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/sop_funnel_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建")
    args = ap.parse_args()

    out_path = Path(args.out)

    if args.if_due and out_path.exists():
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
            built_at = existing.get("built_at")
            if built_at:
                built_dt = datetime.strptime(built_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                age_days = (datetime.now(timezone.utc) - built_dt).total_seconds() / 86400.0
                if age_days < IF_DUE_MAX_AGE_DAYS:
                    info(f"--if-due: {out_path} built_at={built_at}（{age_days:.1f} 天前）< "
                         f"{IF_DUE_MAX_AGE_DAYS} 天門檻，not due，本次不重建")
                    return
                info(f"--if-due: {out_path} built_at={built_at}（{age_days:.1f} 天前）≥ "
                     f"{IF_DUE_MAX_AGE_DAYS} 天門檻，due，繼續重建")
            else:
                info(f"--if-due: {out_path} 無 built_at 欄位，視為需要重建")
        except (OSError, json.JSONDecodeError, ValueError) as e:
            warn(f"--if-due: 無法讀取/解析既有 {out_path}（{e}），視為需要重建")

    backtest = _load_backtest()
    trades_charter = backtest.get("trades_charter") or []
    if not trades_charter:
        raise SystemExit(f"{BACKTEST} 無 trades_charter[]")

    spy_bars = _load_spy_raw_cache()
    spy_dates, spy_closes = _split(spy_bars)

    result = compute(trades_charter, spy_dates, spy_closes)

    dd_p_clim, dd_built_at = _load_dd_p_clim()
    if dd_p_clim is not None:
        p_clim_ref = (f"data/dd_verdict_base_rates.json p_clim.dd_beat_spy_91d={dd_p_clim}"
                      f"（built_at={dd_built_at}）—— 宇宙相對 SPY 無條件基準，供對照本表的 "
                      f"sop-funnel 板機訊號 pooled 勝率是否有邊際訊號，不用於本表自身計算")
    else:
        p_clim_ref = (f"{DD_BASE_RATES} 不存在或無 p_clim.dd_beat_spy_91d —— 先跑 "
                      f"python scripts/build_dd_verdict_base_rates.py")

    use_table = result["n_valid"] >= N_VALID_MIN and result["freq_beat_91d"] is not None

    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_backtest": str(BACKTEST.relative_to(ROOT)),
        "source_backtest_run_timestamp": backtest.get("run_timestamp"),
        "horizon_days": HORIZON_DAYS,
        "n_trades": result["n_trades"],
        "n_valid": result["n_valid"],
        "n_hit": result["n_hit"],
        "freq_beat_91d": result["freq_beat_91d"],
        "by_type": result["by_type"],
        "n_valid_min": N_VALID_MIN,
        "prereg_fallback_p": PREREG_FALLBACK_P,
        "use_table": use_table,
        "p_clim_ref": p_clim_ref,
        "skip_counts": result["skip_counts"],
        "spy_data_start": spy_dates[0],
        "spy_data_end": spy_dates[-1],
        "n_spy_daily_bars": len(spy_dates),
        "methodology_note": (
            "對 docs/dd-screener/sop-funnel/backtest.json 的 trades_charter[]（態①-⑤ SOP 規則的"
            "歷史質量閘門回測，2021–2026），每筆 trade 取 ticker 在 entry_date 當日或之前的最近"
            "週線收盤（data/weekly_cache/）與 entry_date+91 曆日當日或之前的最近週線收盤，同兩個"
            "日期查 SPY（data/dd_verdict_base_rates_raw_cache.json，唯讀）收盤；"
            "hit = ticker 報酬 > SPY 同窗報酬；freq_beat_91d = pooled hit 頻率（跨全部有效 trade，"
            "不分 type）。ticker／SPY 兩端皆採「目標日或之前最近收盤」，任一端缺資料或視窗尚未"
            "到期（最後一根資料日 < 目標日）即整筆跳過，不補值、不外推。by_type 僅供觀察列出，"
            "producer（scripts/generate_sop_funnel_forecasts.py）只讀 pooled freq_beat_91d，"
            f"n_valid < {N_VALID_MIN} 時退回 PREREG {PREREG_FALLBACK_P}（設計稿 §9 F1，PREREG 凍結）。"
        ),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")

    info(f"wrote {out_path}")
    info(f"n_trades={result['n_trades']} n_valid={result['n_valid']} n_hit={result['n_hit']} "
         f"freq_beat_91d={result['freq_beat_91d']} use_table={use_table}")
    info(f"by_type={result['by_type']}")
    if result["skip_counts"]:
        info(f"skip_counts={result['skip_counts']}")


if __name__ == "__main__":
    main()
