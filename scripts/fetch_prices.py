#!/usr/bin/env python3
"""
fetch_prices.py — 週度取價腳本（GitHub Actions 專用）

從 docs/dd/INDEX.md 抽出所有 v11+ DD 的 ticker，加上 watchlist 與 benchmark，
用 yfinance 抓現價 + 300 日歷史，輸出到 portfolio/prices.json 與
portfolio/history.json 供 CCR 遠端 PM 讀取。

為什麼需要：CCR 遠端環境有出站白名單，無法直接打 Finnhub / Yahoo / Stooq。
GitHub Actions 雲端無此限制，可正常使用 yfinance。
"""
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

REPO = Path(__file__).resolve().parent.parent
INDEX_MD = REPO / "docs" / "dd" / "INDEX.md"
PORTFOLIO_DIR = REPO / "portfolio"
WATCHLIST_FILE = PORTFOLIO_DIR / "watchlist.txt"

BENCHMARKS = ["^GSPC", "^NDX", "^TWII"]  # SPX / Nasdaq-100 / TAIEX

PORTFOLIO_DIR.mkdir(exist_ok=True)


def normalize_ticker(raw: str) -> str:
    """把 INDEX 上的 ticker 規範化為 yfinance 可用格式。

    規則：
      - `2330TW`  → `2330.TW`
      - `2383.TW` → 不變
      - 一般美股 → 不變
      - `2383TW_v10` 或 `v3` 等 suffix → 去除
    """
    raw = raw.strip()
    if not raw:
        return ""
    # 去除 legacy suffix 如 `_v10`, `_v3`, `v10` 等
    raw = re.sub(r"_?v\d+(\.\d+)?$", "", raw, flags=re.IGNORECASE)
    # TW 股代號補「.TW」
    if re.fullmatch(r"\d{4,5}", raw):
        return raw + ".TW"
    if re.fullmatch(r"\d{4,5}TW", raw):
        return raw[:-2] + ".TW"
    return raw


def extract_v11plus_tickers() -> list[str]:
    """解析 INDEX.md，抓出第 3 欄為 v11.x 或 v12.x 的 DD row 的 ticker。"""
    if not INDEX_MD.exists():
        print(f"[warn] {INDEX_MD} not found", file=sys.stderr)
        return []
    tickers: set[str] = set()
    for line in INDEX_MD.read_text().splitlines():
        # Example row: | 2026-04-17 | FN | v11.0 | 迴避 | ...
        if not re.search(r"\|\s*v1[12]\.", line):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 3:
            continue
        t = normalize_ticker(cols[2])
        if t:
            tickers.add(t)
    return sorted(tickers)


def load_watchlist() -> list[str]:
    if not WATCHLIST_FILE.exists():
        return []
    return [
        normalize_ticker(l)
        for l in WATCHLIST_FILE.read_text().splitlines()
        if l.strip() and not l.startswith("#")
    ]


def fetch_quote(ticker: str) -> dict | None:
    """用最近 5 個交易日收盤推算現價 + 前一日 close。"""
    try:
        hist = yf.Ticker(ticker).history(period="5d", auto_adjust=False)
        if hist.empty:
            return {"ticker": ticker, "error": "no data"}
        latest = hist.iloc[-1]
        prev = hist.iloc[-2] if len(hist) >= 2 else latest
        price = float(latest["Close"])
        prev_close = float(prev["Close"])
        return {
            "ticker": ticker,
            "price": round(price, 4),
            "prev_close": round(prev_close, 4),
            "change_pct": round((price / prev_close - 1) * 100, 2) if prev_close else 0,
            "volume": int(latest["Volume"]) if latest["Volume"] == latest["Volume"] else 0,
            "date": latest.name.strftime("%Y-%m-%d"),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def fetch_history(ticker: str, days: int = 300) -> dict | None:
    """抓 300 日日線 OHLC（供 MA 計算：W52 ≈ 365 日週線，W104 ≈ 2 年週線，
    W250 = 5 年週線；腳本抓 300 日，W250 需要較長區間另議）。"""
    try:
        hist = yf.Ticker(ticker).history(period=f"{days}d", auto_adjust=False)
        if hist.empty:
            return {"ticker": ticker, "error": "no data"}
        bars = []
        for idx, row in hist.iterrows():
            bars.append({
                "d": idx.strftime("%Y-%m-%d"),
                "o": round(float(row["Open"]), 4),
                "h": round(float(row["High"]), 4),
                "l": round(float(row["Low"]), 4),
                "c": round(float(row["Close"]), 4),
            })
        return {"ticker": ticker, "bars": bars}
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def main():
    tickers = sorted(set(extract_v11plus_tickers() + load_watchlist() + BENCHMARKS))
    print(f"Fetching {len(tickers)} tickers...")

    quotes = {}
    history = {}
    failures = []

    for i, t in enumerate(tickers, 1):
        q = fetch_quote(t)
        if q and "error" not in q:
            quotes[t] = q
            print(f"  [{i}/{len(tickers)}] Quote {t}: ${q['price']} ({q['change_pct']:+.2f}%)")
        else:
            failures.append({"ticker": t, "stage": "quote", "error": q.get("error", "unknown") if q else "none"})
            print(f"  [{i}/{len(tickers)}] Quote {t}: FAILED")
        time.sleep(0.25)

        h = fetch_history(t, days=300)
        if h and "error" not in h and h.get("bars"):
            history[t] = h
        else:
            failures.append({"ticker": t, "stage": "history", "error": h.get("error", "unknown") if h else "none"})
        time.sleep(0.25)

    timestamp = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")

    (PORTFOLIO_DIR / "prices.json").write_text(json.dumps({
        "fetched_at": timestamp,
        "source": "yfinance (via GitHub Actions)",
        "total_tickers": len(tickers),
        "success_count": len(quotes),
        "failures": failures,
        "quotes": quotes,
    }, indent=2))

    (PORTFOLIO_DIR / "history.json").write_text(json.dumps({
        "fetched_at": timestamp,
        "source": "yfinance (via GitHub Actions)",
        "bar_length_days": 300,
        "history": history,
    }, indent=2))

    print(f"\nDone. {len(quotes)} quotes + {len(history)} histories written.")
    if failures:
        print(f"Failures: {len(failures)}")


if __name__ == "__main__":
    main()
