#!/usr/bin/env python3
"""scripts/intel/calendar_ext.py — earnings-date calendar extension via
yfinance. 對應 notes/site-internal/intel/DESIGN.md §3（經濟數據維度的「事前
進日曆」）／§5（個股層）。

單一入口 `earnings_events(date, days_ahead=7)`，回傳格式跟 fetch.py
fetch_ff_calendar() 的 CALENDAR 條目一致：
    {date, time, country, text, hi, impact, source}
（比 DESIGN 原始要求多了 `time`／`country` 兩個 ff_calendar 也有的欄位，方便
呼叫端把兩份日曆條目直接合併排序，不用另外判斷 schema 差異。）

**本檔刻意不 import summarize.py／不修改 summarize.py**——依規範只提供函式，
由另一個 agent 在 summarize.py 的 build_calendar() 裡加一行接進去，例如：

    from calendar_ext import earnings_events
    events = build_calendar(date) + earnings_events(date)

Watchlist：dd-meta 裡 dca_verdict ∈ {"進場","觀望"} 的 ticker ∪ 一份固定
mega-cap 清單（美股＋台積電/鴻海代表性台股）。逐檔呼叫 yfinance
`Ticker(t).calendar`（跟 scripts/check_dd_earnings_freshness.py 用的
`Ticker(t).earnings_dates` 是同一族 API，但 `.calendar` 給的是「下一次」預估
財報日＋EPS 一致預期，正是日曆要的「事前」資訊，不是「事後」reported EPS）。

穩健性：
  - 逐檔 try/except，單檔失敗不拖垮整批。
  - 總時間預算 ~60 秒（TIME_BUDGET_SECONDS），超過就跳過剩下的 ticker
    （沿用它們的舊快取，沒有快取就這次不出現，不阻塞排程）。
  - 磁碟快取 docs/intel/data/earnings_cache.json，key=ticker，3 天內重用
    （財報日期公布後變動不頻繁，不需要每天都打 yfinance）。

獨立測試：
    python3 -c "from calendar_ext import earnings_events; print(earnings_events('2026-08-19'))"
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DD_DIR = ROOT / "docs" / "dd"
DATA_DIR = ROOT / "docs" / "intel" / "data"
CACHE_FILE = DATA_DIR / "earnings_cache.json"

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL
)

# DESIGN 指定的固定清單：美股 mega-cap ＋兩檔代表性台股（供應鏈骨幹：台積電、鴻海）。
MEGA_CAP_FIXED = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "TSM",
    "ASML", "2330.TW", "2317.TW",
]

WATCHLIST_VERDICTS = ("進場", "觀望")
CACHE_TTL_DAYS = 3
TIME_BUDGET_SECONDS = 60


def _load_watchlist() -> list[str]:
    """MEGA_CAP_FIXED ∪ dd-meta 裡 dca_verdict ∈ {進場,觀望} 的 ticker，大寫
    排序回傳（穩定順序，方便快取檔案 diff 好讀）。"""
    tickers = set(MEGA_CAP_FIXED)
    if DD_DIR.exists():
        for p in DD_DIR.glob("DD_*.html"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            m = DD_META_RE.search(text)
            if not m:
                continue
            try:
                d = json.loads(m.group(1).strip())
            except json.JSONDecodeError:
                continue
            verdict = d.get("dca_verdict")
            ticker = d.get("ticker")
            if ticker and verdict in WATCHLIST_VERDICTS:
                tickers.add(ticker.upper())
    return sorted(tickers)


def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _country_for(ticker: str) -> str:
    """跟 ff_calendar 的 country 欄位同慣例：其實是幣別/市場代碼，不是國名。"""
    if ticker.endswith(".TW"):
        return "TWD"
    if ticker.endswith(".KL"):
        return "MYR"
    if ticker.endswith((".DE", ".PA", ".AS")):
        return "EUR"
    if ticker.endswith(".T"):
        return "JPY"
    return "USD"


def _fetch_one(ticker: str) -> dict | None:
    """查一檔的 yfinance forward calendar。回傳 {"earnings_date","eps_avg"} 或
    None（連線/解析層級的失敗——呼叫端保留舊快取，不覆蓋）。calendar 本身查
    得到但沒有 Earnings Date 欄位＝合法情況（回 dict 但 earnings_date=None），
    不是失敗，要覆蓋快取（清空舊的過期日期）。"""
    import yfinance as yf  # 延遲 import：模組本身可以在沒裝 yfinance 的環境被 import 不炸

    try:
        cal = yf.Ticker(ticker).calendar
    except Exception:
        return None
    if not cal:
        return {"earnings_date": None, "eps_avg": None}
    ed = cal.get("Earnings Date")
    edate = None
    if isinstance(ed, list) and ed:
        d0 = ed[0]
        edate = d0.isoformat() if hasattr(d0, "isoformat") else str(d0)
    eps_avg = cal.get("Earnings Average")
    if isinstance(eps_avg, (int, float)):
        eps_avg = round(float(eps_avg), 4)
    else:
        eps_avg = None
    return {"earnings_date": edate, "eps_avg": eps_avg}


def earnings_events(date: str, days_ahead: int = 7) -> list[dict]:
    """回傳 [date, days_ahead] 窗口內、watchlist 裡有下一次財報日的日曆條目。
    純函式，唯一副作用是讀寫 earnings_cache.json（快取，不是狀態機——多跑幾次
    結果一樣，冪等）。"""
    try:
        anchor = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        anchor = datetime.now(timezone.utc).date()
    window_end = anchor + timedelta(days=days_ahead)

    watchlist = _load_watchlist()
    cache = _load_cache()
    now = datetime.now(timezone.utc)
    t0 = time.time()
    budget_exhausted = False

    for ticker in watchlist:
        entry = cache.get(ticker)
        fresh = False
        if entry:
            try:
                fetched_at = datetime.strptime(
                    entry["fetched_at"], "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc)
                fresh = (now - fetched_at) < timedelta(days=CACHE_TTL_DAYS)
            except (KeyError, ValueError):
                fresh = False
        if fresh:
            continue
        if budget_exhausted or (time.time() - t0) > TIME_BUDGET_SECONDS:
            budget_exhausted = True
            continue  # 剩下的留給下次排程；已有的舊快取（若有）繼續沿用
        result = _fetch_one(ticker)
        if result is None:
            continue  # 暫時性失敗：不覆蓋快取，下次排程重試
        cache[ticker] = {**result, "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%SZ")}

    _save_cache(cache)

    events = []
    for ticker in watchlist:
        entry = cache.get(ticker)
        if not entry or not entry.get("earnings_date"):
            continue
        try:
            edate = datetime.strptime(entry["earnings_date"], "%Y-%m-%d").date()
        except ValueError:
            continue
        if not (anchor <= edate <= window_end):
            continue
        eps = entry.get("eps_avg")
        eps_txt = f"（估 EPS {eps}）" if isinstance(eps, (int, float)) else ""
        events.append(
            {
                "date": edate.strftime("%Y-%m-%d"),
                "time": None,
                "country": _country_for(ticker),
                "text": f"{ticker} 財報{eps_txt}",
                "hi": True,
                "impact": "high",
                "source": "yfinance",
            }
        )
    events.sort(key=lambda e: e["date"])
    return events


if __name__ == "__main__":
    import sys

    d = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    t0 = time.time()
    out = earnings_events(d)
    print(f"date={d} events={len(out)} elapsed={time.time()-t0:.1f}s")
    for e in out:
        print(" -", e)
