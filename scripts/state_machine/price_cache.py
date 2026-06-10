"""五狀態機 — price_cache.py：日線 OHLCV 抓取 + 持久化快取。

首次：period="max"（ATH 需全歷史）。之後：period="6mo" 增量併入快取，避免每日
重抓 max。auto_adjust=True 全程使用調整價（ATH 與 breakouts 同基準，§8.3）。
拆股偵測：相鄰收盤偏離 > 30% → 重抓 max 重新對齊整段（§8.3）。

快取存在 data/state_machine_cache/（非公開），CSV-per-ticker。批次下載 chunked +
retry/backoff，沿用 build_dd_screener 的 rate-limit 韌性策略。永不 raise — 抓不到的
ticker 回傳 None，由 run_daily 標 data_error。
"""
from __future__ import annotations

import sys
import time
import warnings
from typing import Optional

import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "pandas", "-q"])
    import yfinance as yf

from config import PRICE_CACHE_DIR, SPLIT_DETECT_THRESHOLD

warnings.filterwarnings("ignore")

_COLS = ["Open", "High", "Low", "Close", "Volume"]


def _safe_name(ticker: str) -> str:
    return ticker.replace("/", "_").replace("\\", "_")


def _cache_path(ticker: str):
    return PRICE_CACHE_DIR / f"{_safe_name(ticker)}.csv"


def _read_cache(ticker: str) -> Optional["pd.DataFrame"]:
    p = _cache_path(ticker)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p, index_col=0, parse_dates=True)
        df = df[[c for c in _COLS if c in df.columns]].dropna(how="all")
        df = df[~df.index.duplicated(keep="last")].sort_index()
        return df if not df.empty else None
    except Exception:
        return None


def _write_cache(ticker: str, df: "pd.DataFrame") -> None:
    try:
        PRICE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        df[[c for c in _COLS if c in df.columns]].to_csv(_cache_path(ticker))
    except Exception as exc:
        print(f"  [cache] write failed {ticker}: {exc}", file=sys.stderr)


def _chunked_download(tickers: list[str], period: str,
                      chunk_size: int = 40, max_retries: int = 3,
                      backoff=(15, 45, 120)) -> "pd.DataFrame":
    """批次 yf.download(daily)，chunk + retry。回傳 group_by='ticker' 的多層欄 DataFrame。"""
    if not tickers:
        return pd.DataFrame()
    chunks = []
    n = (len(tickers) + chunk_size - 1) // chunk_size
    for ci in range(n):
        part = tickers[ci * chunk_size:(ci + 1) * chunk_size]
        for attempt in range(max_retries):
            try:
                df = yf.download(part, period=period, interval="1d",
                                 group_by="ticker", progress=False, threads=True,
                                 auto_adjust=True)
                if df is None or df.empty:
                    raise RuntimeError("empty frame")
                chunks.append(df)
                break
            except Exception as exc:
                if attempt < max_retries - 1:
                    d = backoff[min(attempt, len(backoff) - 1)]
                    print(f"  [dl] chunk {ci+1}/{n} ({period}) retry {attempt+1} "
                          f"({type(exc).__name__}); sleep {d}s", file=sys.stderr)
                    time.sleep(d)
                else:
                    print(f"  [dl] chunk {ci+1}/{n} ({period}) gave up: {type(exc).__name__}; "
                          f"dropping {len(part)} tickers", file=sys.stderr)
        if ci < n - 1:
            time.sleep(2)
    if not chunks:
        return pd.DataFrame()
    try:
        return pd.concat(chunks, axis=1)
    except Exception:
        return pd.DataFrame()


def _extract(raw: "pd.DataFrame", yf_ticker: str, single: bool) -> Optional["pd.DataFrame"]:
    try:
        sub = raw if single else raw[yf_ticker]
        df = sub[[c for c in _COLS if c in sub.columns]].dropna(how="all")
        return df if not df.empty else None
    except (KeyError, TypeError):
        return None


def _merge(cached: Optional["pd.DataFrame"], fresh: Optional["pd.DataFrame"]) -> Optional["pd.DataFrame"]:
    if fresh is None and cached is None:
        return None
    if cached is None:
        return fresh
    if fresh is None:
        return cached
    out = pd.concat([cached, fresh])
    out = out[~out.index.duplicated(keep="last")].sort_index()
    return out


def _split_factor(cached: "pd.DataFrame", fresh: "pd.DataFrame") -> Optional[float]:
    """疑似拆股 → 回傳調整係數 factor = new/old（同一重疊日的新舊收盤比）；否則 None。

    auto_adjust=True 下，一旦發生拆股，整段歷史會被「重新」調整，使同一歷史日期的
    收盤在新舊兩份序列間出現倍數差。必須比對「重疊日期」的同日收盤，不能拿快取最後一根
    (≈今日) 去比增量第一根 (≈6 個月前) —— 那只是正常價格漂移，會誤判。

    factor 供 run_daily 把 breakouts.json 內 prior_ath 換算到新基準（§P1-2）。
    2:1 拆股 → 歷史價砍半 → factor≈0.5 → prior_ath 減半。
    """
    try:
        c = cached["Close"].dropna()
        f = fresh["Close"].dropna()
        if c.empty or f.empty:
            return None
        common = c.index.intersection(f.index)
        if len(common) == 0:
            return None
        d = common[0]   # 重疊區最早的同一交易日
        old, new = float(c.loc[d]), float(f.loc[d])
        if old <= 0:
            return None
        if abs(new / old - 1.0) > SPLIT_DETECT_THRESHOLD:
            return new / old
        return None
    except Exception:
        return None


def load_prices(yf_tickers: list[str]) -> tuple[dict[str, "pd.DataFrame"], dict[str, float]]:
    """回傳 (prices, split_factors)。
      prices: {yf_ticker: daily DataFrame}（抓不到者不在 dict 中）
      split_factors: {yf_ticker: factor}（本次偵測到拆股、已重抓 max 的標的；供 breakouts 換算）
    """
    out: dict[str, pd.DataFrame] = {}
    split_factors: dict[str, float] = {}
    need_full, need_incr = [], []
    cache_map: dict[str, pd.DataFrame] = {}
    for t in yf_tickers:
        c = _read_cache(t)
        if c is None:
            need_full.append(t)
        else:
            cache_map[t] = c
            need_incr.append(t)

    print(f"  [cache] {len(need_incr)} incremental · {len(need_full)} full-history",
          file=sys.stderr)

    # 增量（6mo）
    if need_incr:
        raw = _chunked_download(need_incr, period="6mo")
        single = (len(need_incr) == 1)
        refetch_full = []
        for t in need_incr:
            fresh = _extract(raw, t, single) if not raw.empty else None
            if fresh is None:
                out[t] = cache_map[t]   # 抓不到增量 → 沿用快取
                continue
            fac = _split_factor(cache_map[t], fresh)
            if fac is not None:
                refetch_full.append(t)  # 疑似拆股 → 改抓 max 重對齊
                split_factors[t] = fac
                continue
            merged = _merge(cache_map[t], fresh)
            _write_cache(t, merged)
            out[t] = merged
        need_full.extend(refetch_full)
        if refetch_full:
            print(f"  [cache] split-refetch {len(refetch_full)}: "
                  f"{ {k: round(v,3) for k,v in split_factors.items()} }", file=sys.stderr)

    # 全歷史（max）
    if need_full:
        raw = _chunked_download(need_full, period="max")
        single = (len(need_full) == 1)
        for t in need_full:
            df = _extract(raw, t, single) if not raw.empty else None
            if df is None:
                continue
            _write_cache(t, df)
            out[t] = df

    return out, split_factors
