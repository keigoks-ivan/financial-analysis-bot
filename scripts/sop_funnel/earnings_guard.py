#!/usr/bin/env python3
"""財報靜默期守衛（forward-only）— charter S-7：財報前 5 個交易日禁止新建倉。

定位：只擋「新進場」，不影響既有部位（charter：既有部位可持有過財報，gap 風險
為知情選擇）。

資料源：yfinance Ticker.calendar 的下次財報日。repo 沒有歷史財報日資料 →
回填段與 5 年回測**不受本守衛保護**（已知向下偏誤：真實 SOP 躲得掉部分財報雷、
歷史模擬躲不掉），頁面 caveat 明標；歷史覆蓋列入季檢待辦（PREREG）。

誠實失敗：查詢失敗 / 無資料 → 不否決，事件標 earnings_check="unverified"，
頁面顯示「⚠靜默期未驗」。寧可標不確定，不要假裝驗過。

Cache：docs/dd-screener/sop-funnel/earnings_cache.json（per-ticker TTL 7 天；
CI commit sop-funnel/ 整目錄 → cache 跨日持久）。
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

CACHE_PATH = Path(__file__).resolve().parent.parent.parent / "docs" / "dd-screener" / "sop-funnel" / "earnings_cache.json"
SILENT_CAL_DAYS = 7     # 前 5 個交易日 ≈ 7 個曆日（含週末）近似
CACHE_TTL_DAYS = 7


def _verdict(next_earnings: pd.Timestamp | None, signal_date: pd.Timestamp) -> str:
    """純判定（可測）：ok | silent。next_earnings None 由呼叫端標 unverified。"""
    if next_earnings is None:
        return "ok"
    delta = (next_earnings - signal_date).days
    return "silent" if 0 <= delta <= SILENT_CAL_DAYS else "ok"


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _fetch_next_earnings(ticker: str) -> str | None:
    """yfinance 下次財報日（YYYY-MM-DD）；查無/失敗 raise。"""
    import yfinance as yf
    cal = yf.Ticker(ticker).calendar
    dates = None
    if isinstance(cal, dict):                      # yfinance >= 0.2.x
        dates = cal.get("Earnings Date")
    elif cal is not None and hasattr(cal, "loc"):  # 舊版 DataFrame
        try:
            dates = list(cal.loc["Earnings Date"])
        except Exception:
            dates = None
    if not dates:
        raise RuntimeError("calendar 無 Earnings Date")
    d0 = dates[0] if isinstance(dates, (list, tuple)) else dates
    return pd.Timestamp(d0).strftime("%Y-%m-%d")


def check(ticker: str, signal_date: pd.Timestamp) -> tuple[str, str | None]:
    """回傳 (verdict, next_earnings)。verdict ∈ ok | silent | unverified。"""
    cache = _load_cache()
    now = datetime.now(timezone.utc)
    rec = cache.get(ticker)
    if rec:
        age = (now - datetime.fromisoformat(rec["fetched"])).days
        if age <= CACHE_TTL_DAYS:
            ne = rec.get("next_earnings")
            if ne is None:
                return "unverified", None
            return _verdict(pd.Timestamp(ne), signal_date), ne
    try:
        ne = _fetch_next_earnings(ticker)
    except Exception:
        cache[ticker] = {"next_earnings": None, "fetched": now.isoformat()}
        _save(cache)
        return "unverified", None
    cache[ticker] = {"next_earnings": ne, "fetched": now.isoformat()}
    _save(cache)
    return _verdict(pd.Timestamp(ne), signal_date), ne


def _save(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=1),
                          encoding="utf-8")
