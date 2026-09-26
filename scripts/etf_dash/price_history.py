#!/usr/bin/env python3
"""price_history.py — compact, append-only daily cross-section of constituent
closing prices for build_etf_dash.py's 報酬貢獻 (price-return contribution)
feature.

Background: 報酬貢獻 needs each constituent's price ~30 and ~90 calendar days
ago to compute a 1M/3M return per name. build_etf_dash.py already fetches a
batched, multi-day price history for every constituent during PRICE-mode runs
(see fetch_prices_batch() in build_etf_dash.py) — up to 200 calendar days, but
that history lives only in memory for the run that fetched it and is thrown
away once "today's" close is read out of it (see build_fund_price()). FULL
mode fetches only a single current price per ticker (fast_info), no history
at all.

Rather than re-fetching ~100 days of history from Yahoo every single day for
every constituent (expensive, and this is a public repo — "keep lean"), this
module persists ONE compact JSONL row per calendar day:

    {"date": "YYYY-MM-DD", "closes": {"NVDA": 181.2, "AAPL": 254.1, ...}}

data/etf_dash/prices.jsonl — shared across ALL funds (not one file per ETF):
most constituents overlap across funds (NVDA is in SMH/QQQ/SPY/XLK/...), so a
single cross-fund file avoids storing the same ticker's close N times per day.
Each day's row is the UNION of whatever tickers this run's funds touched that
day — coverage of any one ticker on any one day depends on which funds ran
that day and whether they were in FULL or PRICE mode (FULL mode only knows
"today's" price for tickers newly fetched this run — see build_etf_dash.py's
ticker_cache design — so a FULL-mode day can still contribute a fairly full
cross-section since most tickers get fetched fresh across the funds in a
normal daily run).

Same idempotency convention as dd_eps_history.py / anchor_history.py: a
same-day rerun merges into (not duplicates) that day's row. The file is
pruned to the most recent MAX_ROWS calendar-day rows on every write — this is
"~70 trading days" of memory (see build_etf_dash.py's 報酬貢獻 lookback of 30
and 90 calendar days; a 100-calendar-day window comfortably covers both with
margin for weekends/holidays without the file growing unbounded).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PRICES_JSONL_PATH = ROOT / "data" / "etf_dash" / "prices.jsonl"

MAX_ROWS = 100  # calendar-day rows retained (~70 trading days + weekend/holiday margin)


def load_days() -> dict[str, dict[str, float]]:
    """回傳 {date: {ticker: close}}，依檔案順序（理論上已經是日期由舊到新，
    因為只 append／改最後一行）。不存在或壞掉的行都不會讓整個讀取失敗，跟
    dd_eps_history.py／anchor_history.py 的既有行為一致。"""
    if not PRICES_JSONL_PATH.exists():
        return {}
    out: dict[str, dict[str, float]] = {}
    for i, line in enumerate(PRICES_JSONL_PATH.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            out[row["date"]] = row.get("closes") or {}
        except (ValueError, KeyError) as e:
            print(f"[price_history] WARNING skipping malformed line {i + 1} in {PRICES_JSONL_PATH}: {e}",
                  file=sys.stderr)
    return out


def append_today(date_str: str, closes: dict[str, float]) -> None:
    """把今天蒐集到的收盤價（可能是這次 run 涵蓋的多檔基金合併起來的聯集）
    併入既有序列——同一天重跑合併（新值覆寫舊值，不會的 ticker 保留舊值），
    再裁到最近 MAX_ROWS 天，整份寫回（規模天生很小：MAX_ROWS 天 × 全站
    ~1000 檔獨立 ticker，仍是幾百 KB 量級，跟 dd_eps_history.py 一樣「整份讀
    出、必要時改最後一行、整份寫回」不會有效能問題）。"""
    days = load_days()
    if date_str in days:
        days[date_str] = {**days[date_str], **closes}
    else:
        days[date_str] = dict(closes)
    ordered_dates = sorted(days.keys())[-MAX_ROWS:]
    PRICES_JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
    PRICES_JSONL_PATH.write_text(
        "".join(
            json.dumps({"date": d, "closes": days[d]}, ensure_ascii=False, separators=(",", ":")) + "\n"
            for d in ordered_dates
        ),
        encoding="utf-8",
    )


def closest_close_on_or_before(days: dict[str, dict[str, float]], ticker: str, target_date: str) -> tuple[str, float] | None:
    """在 days 裡找「日期 <= target_date、且最接近」的那一天，回傳
    (該天日期, 該 ticker 當天收盤價)；那個 ticker 在該天沒有收盤價，或完全
    沒有 <= target_date 的資料，回傳 None——跟
    build_etf_dash.py::_closest_close_on_or_before() 同一種近似（不內插）。"""
    candidates = sorted(d for d in days if d <= target_date)
    for d in reversed(candidates):
        v = days[d].get(ticker)
        if v is not None:
            return d, v
    return None
