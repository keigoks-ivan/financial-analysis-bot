"""交易日與收盤時間（美股／台股）——2026-10-21，給每日 EPS 快照的「財報後第 k 天」對位用。

stdlib only（python3 3.9 與 3.12 都能 import）。

美股：週一到週五，扣掉 NYSE 假日（用規則算，不查表）。提前收盤（13:00）不處理，
一律用 16:00 ET。
台股：週一到週五，扣掉固定日期的假日（元旦、228、勞動節、國慶日）。農曆春節、清明、
端午、中秋等逐年變動的假日沒有建表，遇到時視窗會差一天，用 TW_EXTRA_HOLIDAYS 補。
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")
TAIPEI = ZoneInfo("Asia/Taipei")

# 逐年變動的台股休市日，需要時手動補（YYYY-MM-DD）。
TW_EXTRA_HOLIDAYS: set[str] = set()
_TW_FIXED = {(1, 1), (2, 28), (5, 1), (10, 10)}


def _to_date(v) -> date:
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(year: int, month: int, weekday: int) -> date:
    d = date(year + (month == 12), month % 12 + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def _easter(year: int) -> date:
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(year, month, day)


def _observed(d: date) -> date:
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def us_holidays(year: int) -> set[date]:
    h = {
        _nth_weekday(year, 1, 0, 3),            # MLK
        _nth_weekday(year, 2, 0, 3),            # Presidents
        _easter(year) - timedelta(days=2),      # Good Friday
        _last_weekday(year, 5, 0),              # Memorial
        _observed(date(year, 6, 19)),           # Juneteenth
        _observed(date(year, 7, 4)),
        _nth_weekday(year, 9, 0, 1),            # Labor
        _nth_weekday(year, 11, 3, 4),           # Thanksgiving
        _observed(date(year, 12, 25)),
    }
    # 1/1：週日順延到週一；週六 NYSE 不補休（前一年 12/31 照常開市）
    if date(year, 1, 1).weekday() != 5:
        h.add(_observed(date(year, 1, 1)))
    return h


def is_us_session(d) -> bool:
    d = _to_date(d)
    if d.weekday() >= 5:
        return False
    return d not in us_holidays(d.year)


def is_tw_session(d) -> bool:
    d = _to_date(d)
    if d.weekday() >= 5:
        return False
    if (d.month, d.day) in _TW_FIXED:
        return False
    return d.isoformat() not in TW_EXTRA_HOLIDAYS


def _is_session(market: str, d) -> bool:
    return is_tw_session(d) if market == "TW" else is_us_session(d)


def next_session(market: str, d, n: int = 1) -> date:
    """d 之後第 n 個交易日（n >= 1）；d 本身不算。"""
    d = _to_date(d)
    while n > 0:
        d += timedelta(days=1)
        if _is_session(market, d):
            n -= 1
    return d


def prev_session(market: str, d, n: int = 1) -> date:
    """d 之前第 n 個交易日（n >= 1）；d 本身不算。"""
    d = _to_date(d)
    while n > 0:
        d -= timedelta(days=1)
        if _is_session(market, d):
            n -= 1
    return d


def first_session_on_or_after(market: str, d) -> date:
    d = _to_date(d)
    return d if _is_session(market, d) else next_session(market, d)


def close_utc(market: str, d) -> datetime:
    """交易日 d 的收盤時刻（UTC，aware）。美股 16:00 ET，台股 13:30 台北。"""
    d = _to_date(d)
    if market == "TW":
        return datetime(d.year, d.month, d.day, 13, 30, tzinfo=TAIPEI).astimezone(timezone.utc)
    return datetime(d.year, d.month, d.day, 16, 0, tzinfo=EASTERN).astimezone(timezone.utc)


def latest_closed_session(market: str, now_utc: datetime) -> date:
    """now_utc 當下最近一個「已收盤」的交易日。"""
    tz = TAIPEI if market == "TW" else EASTERN
    d = now_utc.astimezone(tz).date()
    while True:
        if _is_session(market, d) and close_utc(market, d) <= now_utc:
            return d
        d -= timedelta(days=1)


def sessions_elapsed(market: str, start, end) -> int:
    """(start, end] 之間有幾個交易日（start 不算、end 算）。end <= start 回 0。"""
    start, end = _to_date(start), _to_date(end)
    n, d = 0, start
    while d < end:
        d += timedelta(days=1)
        if _is_session(market, d):
            n += 1
    return n
