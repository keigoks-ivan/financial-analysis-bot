"""台股財報日的第二來源：公開資訊觀測站重大訊息裡的「董事會通過財報」日期（2026-10-10）。

yfinance 對不少台股沒有財報日，或停在好幾年前（2026-10-10 台股池 86 檔有 22 檔）。
build_dd_screener.py --universe tw 只在 yfinance 沒有日期、或日期早於「法定期限已過的
最近一季」季底隔天（tw_filing_calendar.latest_due_quarter_start）時改用這裡的日期，
其餘照用 yfinance。

這是董事會通過財報的公告日，不一定是第一次公布數字的日子：大公司常在法說會先公布
（台積電 2026 第二季 07-16 法說、08-11 董事會；南亞科 07-09 法說、08-05 董事會）。
所以只當 yfinance 的後備，不取代 yfinance。

來源：POST https://mopsov.twse.com.tw/mops/web/ajax_t05st01（一家公司一年一次查詢，
上市、上櫃、興櫃都有；mops.twse.com.tw 舊網域會回安全阻擋頁）。主旨文字的寫法不一，
規則見 parse_approvals()。快取 data/tw_mops_earnings_cache.json，3 天內不重查。
網路失敗只回舊快取，不擋 build。
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path

from tw_filing_calendar import latest_due_quarter_start

ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT / "data" / "tw_mops_earnings_cache.json"
URL = "https://mopsov.twse.com.tw/mops/web/ajax_t05st01"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
MAX_AGE_DAYS = 3
SLEEP_S = 1.2
MAX_FAILURES = 3            # consecutive request failures before giving up for this run
MAX_LAG_DAYS = 150          # approval must land within this many days after the period end

# 財務資訊＝KY 公司董事會通過的自結數（AES-KY）。
_REPORT = re.compile(r"財務報[告表]|財報|財務資訊")
# 通過／決議＝董事會決議（神基寫「業經董事會決議」）；提報＝向董事會提報（亞德客）；
# 發布＝財報發布（創意）。
_VERB = re.compile(r"通過|決議|提報|發布")
# 預計／召開＝預告董事會日期；更正／補正／重編／變更＝事後修正；子公司＝不是本公司的財報。
_SKIP = re.compile(r"子公司|預計|召開|更正|補正|重編|變更")
# 年份：民國數字（114）、西元（2025）、中文數字（一一四，緯穎）。
_PERIOD = re.compile(r"(\d{2,4}|[〇○零一二三四五六七八九]{3})\s*年\s*度?\s*(?:第\s*([一二三四1-4])\s*季|(上半年))?")
_ZH_DIGIT = {c: str(i) for i, c in enumerate("零一二三四五六七八九")} | {"〇": "0", "○": "0"}
_QUARTER = {"一": 1, "二": 2, "三": 3, "四": 4, "1": 1, "2": 2, "3": 3, "4": 4}
_PERIOD_END = {1: (3, 31), 2: (6, 30), 3: (9, 30), 4: (12, 31)}
_ROC_DATE = re.compile(r"(\d{2,3})/(\d{2})/(\d{2})")


def _roc_to_date(s: str) -> date | None:
    m = _ROC_DATE.fullmatch(s.strip())
    if not m:
        return None
    try:
        return date(int(m.group(1)) + 1911, int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def parse_approvals(rows) -> dict[str, str]:
    """rows = [(ROC 發言日期 "115/08/11", 主旨), ...] -> {"2026Q2": "2026-08-11", ...}.

    Keeps rows whose 主旨 says the board approved (通過／決議／提報) or released
    (發布) a 財務報告/報表/財報/財務資訊 and
    names its period: 第N季, 上半年 (= Q2), or a bare 年度 / 第四季 (= FY,
    keyed Q4). The approval must fall within MAX_LAG_DAYS after the period
    end, which also drops late corrections whose wording slipped past _SKIP.
    Earliest row per period wins (re-postings come later)."""
    out: dict[str, date] = {}
    for roc_day, subject in rows:
        d = _roc_to_date(roc_day)
        if d is None or not _VERB.search(subject) or not _REPORT.search(subject) or _SKIP.search(subject):
            continue
        m = _PERIOD.search(subject)
        if not m:
            continue
        year = int("".join(_ZH_DIGIT.get(c, c) for c in m.group(1)))
        year += 1911 if year < 1911 else 0
        q = 2 if m.group(3) else _QUARTER.get(m.group(2) or "", 4)
        end = date(year, *_PERIOD_END[q])
        if not (end < d <= end + timedelta(days=MAX_LAG_DAYS)):
            continue
        key = f"{year}Q{q}"
        if key not in out or d < out[key]:
            out[key] = d
    return {k: v.isoformat() for k, v in sorted(out.items())}


def _fetch_rows(code: str, roc_year: int):
    """[(ROC date, subject), ...] for one company-year, or None on any failure."""
    import requests
    form = dict(encodeURIComponent=1, step=1, firstin=1, off=1, keyword4="", code1="", TYPEK2="",
                checkbtn="", queryName="co_id", inpuType="co_id", TYPEK="all", co_id=code,
                year=roc_year, month="")
    try:
        r = requests.post(URL, data=form, headers=UA, timeout=20)
        r.raise_for_status()
        r.encoding = "utf-8"
        html = r.text
    except Exception as exc:  # noqa: BLE001 — never abort the build
        print(f"  WARN: MOPS t05st01 {code}/{roc_year}: {type(exc).__name__}: {exc}", file=sys.stderr)
        return None
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html, flags=re.S):
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c).replace("&nbsp;", " ")).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
        if len(cells) >= 5 and _ROC_DATE.fullmatch(cells[2]):
            rows.append((cells[2], cells[4]))
    return rows


def load_cache(path: Path | None = None) -> dict:
    try:
        return json.loads((path or CACHE_PATH).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_cache(cache: dict, path: Path | None = None) -> None:
    p = path or CACHE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cache, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                 encoding="utf-8")


def needs_fallback(last_earnings_date: str | None, today: date) -> bool:
    """Same staleness test as build_dd_screener.tw_quarter_anchor_date()."""
    start = latest_due_quarter_start(today)
    if start is None:
        return False
    try:
        return last_earnings_date is None or date.fromisoformat(last_earnings_date[:10]) < start
    except ValueError:
        return True


def prefetch(codes, cache: dict, today: date, fetch=_fetch_rows, sleep=time.sleep) -> dict[str, dict]:
    """{code: {period: ISO date}} for `codes`, refreshing cache entries older
    than MAX_AGE_DAYS (current and previous ROC year, one request each).
    Mutates `cache`; stops querying after MAX_FAILURES consecutive failures
    and serves whatever is cached."""
    roc = today.year - 1911
    failures = 0
    out: dict[str, dict] = {}
    for code in sorted(set(codes)):
        hit = cache.get(code) or {}
        try:
            fresh = (today - date.fromisoformat(hit.get("checked", ""))).days < MAX_AGE_DAYS
        except ValueError:
            fresh = False
        if not fresh and failures < MAX_FAILURES:
            rows, ok = [], True
            for y in (roc - 1, roc):
                got = fetch(code, y)
                sleep(SLEEP_S)
                if got is None:
                    ok = False
                    break
                rows += got
            if ok:
                failures = 0
                hit = {"approvals": parse_approvals(rows), "checked": today.isoformat()}
                cache[code] = hit
            else:
                failures += 1
                if failures == MAX_FAILURES:
                    print(f"  WARN: MOPS t05st01 failed {MAX_FAILURES}x in a row — "
                          "serving cached dates only", file=sys.stderr)
        if hit.get("approvals"):
            out[code] = hit["approvals"]
    return out


def merge(cal: dict, approvals: dict | None, today: date) -> dict:
    """yfinance earnings calendar -> same shape, with MOPS dates when yfinance
    is missing or stale (needs_fallback). Adds earnings_date_source
    ("yfinance" / "mops_board" / None). next_earnings_date stays yfinance's:
    MOPS only has it inside the 預計召開 announcement text."""
    out = dict(cal)
    out["earnings_date_source"] = "yfinance" if cal.get("last_earnings_date") else None
    if not needs_fallback(cal.get("last_earnings_date"), today):
        return out
    known = {k: v for k, v in (approvals or {}).items() if date.fromisoformat(v) <= today}
    if not known:
        return out
    past = sorted(known.values())
    if cal.get("last_earnings_date") and cal["last_earnings_date"][:10] >= past[-1]:
        return out
    # yfinance dates only up to the end of the first quarter MOPS covers: one
    # date per quarter (eps_fy_shift reads this list to find the annual report).
    # yfinance tends to date a quarter before the board approval, so cutting at
    # the first MOPS date would keep both dates for that quarter.
    first = min(known)
    first_end = date(int(first[:4]), *_PERIOD_END[int(first[-1])]).isoformat()
    older = [d for d in (cal.get("past_earnings_dates") or []) if d[:10] <= first_end]
    out["last_earnings_date"] = past[-1]
    out["past_earnings_dates"] = sorted(set(older) | set(past))
    out["earnings_date_source"] = "mops_board"
    return out
