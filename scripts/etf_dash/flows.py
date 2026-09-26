#!/usr/bin/env python3
"""flows.py — 資金流 (creation/redemption flow) tracking for build_etf_dash.py.

flows = Δ(shares outstanding) × NAV — the standard ETF creation/redemption
flow proxy. Needs a daily shares-outstanding number per fund.

Source survey (2026-09-26, updated same day after a coordinator review flagged
yfinance's `sharesOutstanding` as often stale/irregularly-updated for ETFs —
confirmed: yfinance reported QQQ sharesOutstanding=393,100,000 vs Invesco's
own official current figure of 675,750,000 the same day). Three tiers, from
best to worst:

  1. **Official daily history file** (best — real point-in-time history, not
     just "today"):
     - SSGA (SPY + the 9 SPDR sector funds): the "NAV History" download
       (`navhist-us-en-{ticker}.xlsx`, sibling to the holdings file already
       used) has explicit **Date / NAV / Shares Outstanding / Total Net
       Assets** columns going back years — see fetch_ssga_navhist_rows().
       source tag: "ssga_navhist".
     - VanEck US-listed SMH (not the Irish UCITS share class — see below):
       the fund page's "NAV & Premium/Discount History" download
       (`downloads/fundhistoprices/`) has Date/NAV/.../AUM columns; no
       explicit shares-outstanding column, so it's derived as AUM/NAV per
       row (same identity as tier 3, just applied to a real daily *history*
       instead of a single snapshot) — see fetch_vaneck_navhist_rows().
       source tag: "vaneck_navhist_derived".
  2. **Official current-day snapshot, no history** (better than yfinance for
     "today", but can't backfill):
     - Invesco QQQ/RSP: `dng-api.invesco.com/.../shareclasses/{TICKER}
       ?variationType=fundDetails` returns a live `sharesOutstanding` +
       `nav` (confirmed QQQ=675,750,000 vs yfinance's stale 393,100,000
       the same day) — see fetch_invesco_fund_details(). Empirically this
       endpoint is unreliable for RSP (consistently returns `""`, same
       flakiness as RSP's holdings endpoint — see
       build_etf_dash.py::get_holdings_with_fallback()'s existing SPY
       equal-weight fallback for RSP holdings); RSP therefore falls through
       to tier 3. source tag: "invesco_direct".
  3. **yfinance `get_info()` fallback** (SMH_UCITS — VanEck's Irish page has
     no AUM column in its history file, see above; TOPIX/1475.T; 0050.TW;
     and QQQ/RSP if Invesco is down that day): `sharesOutstanding` when
     present ("yfinance_direct"), else `totalAssets/navPrice`
     ("yfinance_derived"). Because this tier is the one known to go stale
     (identical value for many days while AUM keeps moving), every read of
     it is run through detect_staleness() and the result is surfaced to the
     page as `stale_shares_flag` + a 「資料更新不規律」 note rather than
     silently presented as precise daily flow numbers.

TAIEX is an index, not a fund — no shares outstanding, skipped entirely by
the caller (see build_etf_dash.py FUND_REGISTRY / attach_flows()).

Storage: append-only-ish JSONL, one row per calendar day per fund,
data/etf_dash/flows/{ETF}.jsonl:
    {"date": "YYYY-MM-DD", "shares_outstanding": 917782016, "nav": 767.4363,
     "nav_currency": "USD", "source": "ssga_navhist"|"vaneck_navhist_derived"|
     "invesco_direct"|"yfinance_direct"|"yfinance_derived"}
Tier-1 sources return a whole history file each run — merge_history() merges
by date (a given date's row is fully replaced if refetched, same idempotency
convention as dd_eps_history.py/anchor_history.py's "same day rewrites the
last line", generalized to "same date anywhere in the file rewrites that
line") and caps storage to MAX_HISTORY_DAYS calendar days. Tier 2/3 sources
only ever know "today" — append_today() covers those (and is what
merge_history() reduces to for a single-row list).
"""
from __future__ import annotations

import datetime
import io
import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent.parent
FLOWS_DIR = ROOT / "data" / "etf_dash" / "flows"

MAX_HISTORY_DAYS = 200  # calendar days retained per fund — "~6 個月" with margin, keeps the repo lean

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def _path(etf_key: str) -> Path:
    return FLOWS_DIR / f"{etf_key}.jsonl"


def load_rows(etf_key: str) -> list[dict]:
    path = _path(etf_key)
    if not path.exists():
        return []
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError as e:
            print(f"[flows] WARNING skipping malformed line {i + 1} in {path}: {e}", file=sys.stderr)
    return out


def _save_rows(etf_key: str, rows: list[dict]) -> None:
    rows = sorted(rows, key=lambda r: r["date"])
    if len(rows) > MAX_HISTORY_DAYS:
        rows = rows[-MAX_HISTORY_DAYS:]
    path = _path(etf_key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows),
        encoding="utf-8",
    )


def append_today(etf_key: str, row: dict) -> None:
    """單日快照（tier 2／3 來源用）——同一天重跑覆寫同一行，不是同一天疊加
    兩行，跟 dd_eps_history.py／anchor_history.py 既有慣例一致。"""
    rows = load_rows(etf_key)
    if rows and rows[-1].get("date") == row.get("date"):
        rows[-1] = row
    else:
        rows.append(row)
    _save_rows(etf_key, rows)


def merge_history(etf_key: str, new_rows: list[dict]) -> None:
    """整批歷史合併（tier 1 官方歷史檔用）——`new_rows` 是這次抓到的完整（或
    局部）歷史，依 date 覆寫既有序列裡同一天的紀錄（官方檔案本身偶爾會回頭
    修正過去幾天的數字，這裡選擇信任最新抓到的版本），其餘既有天數保留，
    再裁到最近 MAX_HISTORY_DAYS 天存回——單一 xlsx 下載動輒帶回幾年份資料，
    只留近 ~6 個月才不會讓公開 repo 的檔案無限成長。"""
    if not new_rows:
        return
    existing = {r["date"]: r for r in load_rows(etf_key)}
    for r in new_rows:
        existing[r["date"]] = r
    _save_rows(etf_key, list(existing.values()))


# ---------------------------------------------------------------------------
# Tier 1a — SSGA NAV History xlsx (SPY + the 9 SPDR sector funds).
# ---------------------------------------------------------------------------


def fetch_ssga_navhist_xlsx(yf_ticker: str) -> bytes:
    url = ("https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/"
           f"navhist-us-en-{yf_ticker.lower()}.xlsx")
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30, allow_redirects=True)
    r.raise_for_status()
    ct = r.headers.get("content-type", "")
    if "spreadsheet" not in ct and "excel" not in ct and "octet-stream" not in ct:
        raise RuntimeError(f"unexpected content-type {ct!r} (body len={len(r.content)}) from {url}")
    if len(r.content) < 500:
        raise RuntimeError(f"suspiciously small response ({len(r.content)} bytes) from {url}")
    return r.content


def parse_ssga_navhist_xlsx(raw: bytes, max_days: int = MAX_HISTORY_DAYS) -> list[dict]:
    """欄位（2026-09-26 實測）：Date（"24-Sep-2026"）／NAV／Shares Outstanding／
    Total Net Assets——直接就是官方逐日份額歷史，不需要推算。回傳依日期由舊到
    新排序，只留最近 max_days 天（檔案本身常常有數年份資料）。"""
    df = pd.read_excel(io.BytesIO(raw), header=None)
    header_row_idx = None
    for i in range(min(6, len(df))):
        row_vals = [str(v).strip() for v in df.iloc[i].tolist()]
        if "Date" in row_vals and "NAV" in row_vals and "Shares Outstanding" in row_vals:
            header_row_idx = i
            break
    if header_row_idx is None:
        raise RuntimeError("could not locate header row ('Date'/'NAV'/'Shares Outstanding') in SSGA NAV history sheet")
    cols = [str(c).strip() for c in df.iloc[header_row_idx].tolist()]
    body = df.iloc[header_row_idx + 1:]
    date_i, nav_i, so_i = cols.index("Date"), cols.index("NAV"), cols.index("Shares Outstanding")

    rows = []
    for _, row in body.iterrows():
        raw_date = row.iloc[date_i]
        try:
            d = pd.to_datetime(raw_date, format="%d-%b-%Y", errors="raise")
        except (ValueError, TypeError):
            break  # 撞到 footer 免責聲明列，資料列結束
        if pd.isna(d):
            # 2026-09-26 實測：資料表最後一筆日期列後面是一長串全空白列（不是
            # 馬上接免責聲明文字），pd.to_datetime(NaN, errors="raise") 不會
            # 拋例外（NaN 本身被當成合法的缺值輸入），回傳 NaT——d.strftime()
            # 才會炸（NaTType 沒有 strftime）。空白列視同資料列結束（跟遇到
            # 不合法字串時的既有 break 邏輯一致），不能只靠上面那個
            # try/except 判斷。
            break
        try:
            nav = float(row.iloc[nav_i])
            shares = float(row.iloc[so_i])
        except (TypeError, ValueError):
            continue
        rows.append({"date": d.strftime("%Y-%m-%d"), "nav": round(nav, 6), "nav_currency": "USD",
                      "shares_outstanding": round(shares), "source": "ssga_navhist", "reason": None})
    if not rows:
        raise RuntimeError("parsed 0 rows from SSGA NAV history sheet")
    rows.sort(key=lambda r: r["date"])
    return rows[-max_days:]


def fetch_ssga_navhist_rows(yf_ticker: str) -> list[dict]:
    return parse_ssga_navhist_xlsx(fetch_ssga_navhist_xlsx(yf_ticker))


# ---------------------------------------------------------------------------
# Tier 1b — VanEck "NAV & Premium/Discount History" xlsx (US-listed SMH
# only — the Irish UCITS share class's equivalent file has no AUM column,
# see module docstring, so SMH_UCITS stays on the yfinance tier).
# ---------------------------------------------------------------------------


def fetch_vaneck_navhist_xlsx(fund_history_url: str, cookies: dict) -> bytes:
    r = requests.get(fund_history_url, headers={"User-Agent": UA}, cookies=cookies, timeout=30,
                      allow_redirects=True)
    r.raise_for_status()
    ct = r.headers.get("content-type", "")
    if "spreadsheet" not in ct and "excel" not in ct and "octet-stream" not in ct:
        raise RuntimeError(f"unexpected content-type {ct!r} (body len={len(r.content)}) from {fund_history_url}")
    if len(r.content) < 500:
        raise RuntimeError(f"suspiciously small response ({len(r.content)} bytes) from {fund_history_url}")
    return r.content


def parse_vaneck_navhist_xlsx(raw: bytes, max_days: int = MAX_HISTORY_DAYS) -> list[dict]:
    """欄位（2026-09-26 實測，US 版）：Date（"09/25/2026"，MM/DD/YYYY）／NAV／
    Change／% Change／Last Trade／Volume／Premium/Discount／% Premium/Discount／
    AUM／Index Level——沒有直接的 Shares Outstanding 欄，用 AUM/NAV 逐日推算
    （identity 跟既有 yfinance fallback 相同，但套用在真正的逐日官方歷史上，
    不是單一快照，見 module docstring）。"""
    df = pd.read_excel(io.BytesIO(raw), header=None)
    header_row_idx = None
    for i in range(min(6, len(df))):
        row_vals = [str(v).strip() for v in df.iloc[i].tolist()]
        if "Date" in row_vals and "NAV" in row_vals and "AUM" in row_vals:
            header_row_idx = i
            break
    if header_row_idx is None:
        raise RuntimeError("could not locate header row ('Date'/'NAV'/'AUM') in VanEck NAV history sheet")
    cols = [str(c).strip() for c in df.iloc[header_row_idx].tolist()]
    body = df.iloc[header_row_idx + 1:]
    date_i, nav_i, aum_i = cols.index("Date"), cols.index("NAV"), cols.index("AUM")

    rows = []
    for _, row in body.iterrows():
        raw_date = row.iloc[date_i]
        try:
            d = pd.to_datetime(raw_date, format="%m/%d/%Y", errors="raise")
        except (ValueError, TypeError):
            break
        if pd.isna(d):
            break  # 見 parse_ssga_navhist_xlsx() 同一段註解——NaN 不會讓 to_datetime 拋例外
        try:
            nav = float(row.iloc[nav_i])
            aum = float(str(row.iloc[aum_i]).replace(",", ""))
        except (TypeError, ValueError):
            continue
        if nav <= 0:
            continue
        rows.append({"date": d.strftime("%Y-%m-%d"), "nav": round(nav, 6), "nav_currency": "USD",
                      "shares_outstanding": round(aum / nav), "source": "vaneck_navhist_derived", "reason": None})
    if not rows:
        raise RuntimeError("parsed 0 rows from VanEck NAV history sheet")
    rows.sort(key=lambda r: r["date"])
    return rows[-max_days:]


def fetch_vaneck_navhist_rows(fund_history_url: str, cookies: dict) -> list[dict]:
    return parse_vaneck_navhist_xlsx(fetch_vaneck_navhist_xlsx(fund_history_url, cookies))


# ---------------------------------------------------------------------------
# Tier 2 — Invesco fundDetails API (QQQ/RSP). Empirically unreliable for RSP
# (returns a bare `""` body consistently, same flakiness affecting RSP's
# holdings endpoint elsewhere in this pipeline) — caller falls through to
# yfinance when this returns source=None. Retried with the same backoff
# schedule as the holdings 406-retry (build_etf_dash.py
# INVESCO_406_RETRY_BACKOFFS_S) since Invesco's WAF throttling behavior is
# shared across their endpoints.
# ---------------------------------------------------------------------------

INVESCO_FUND_DETAILS_RETRY_BACKOFFS_S = [10, 30, 60, 90]


def fetch_invesco_fund_details(ticker: str) -> dict:
    url = f"https://dng-api.invesco.com/cache/v1/accounts/en_US/shareclasses/{ticker}"
    last_exc: Exception | None = None
    for attempt, wait_s in enumerate([0] + INVESCO_FUND_DETAILS_RETRY_BACKOFFS_S):
        if wait_s:
            time.sleep(wait_s)
        try:
            r = requests.get(url, params={"idType": "ticker", "variationType": "fundDetails", "productType": "ETF"},
                              headers={"User-Agent": UA, "Accept": "application/json, text/plain, */*",
                                       "Referer": "https://www.invesco.com/", "Origin": "https://www.invesco.com"},
                              timeout=30)
            if r.status_code >= 400:
                raise RuntimeError(f"{r.status_code} from {url}")
            data = r.json()
            if not isinstance(data, dict) or "sharesOutstanding" not in data or "nav" not in data:
                raise RuntimeError(f"empty or missing sharesOutstanding/nav (body={r.text[:120]!r})")
            return data
        except (RuntimeError, requests.RequestException, ValueError) as e:
            last_exc = e
    raise RuntimeError(f"Invesco fundDetails still unusable after "
                        f"{len(INVESCO_FUND_DETAILS_RETRY_BACKOFFS_S) + 1} attempts (last error: {last_exc})") from last_exc


def fetch_shares_snapshot_invesco(ticker: str) -> dict:
    try:
        data = fetch_invesco_fund_details(ticker)
    except Exception as e:  # noqa: BLE001
        return {"shares_outstanding": None, "nav": None, "nav_currency": None,
                "source": None, "reason": f"Invesco fundDetails fetch failed: {e}"}
    return {
        "shares_outstanding": round(data["sharesOutstanding"]),
        "nav": round(float(data["nav"]), 6),
        "nav_currency": (data.get("currencyCode") or "USD").upper(),
        "source": "invesco_direct",
        "reason": None,
    }


# ---------------------------------------------------------------------------
# Tier 3 — yfinance get_info() fallback (SMH_UCITS, TOPIX, 0050, and QQQ/RSP
# on days Invesco is down). Known to go stale — see detect_staleness().
# ---------------------------------------------------------------------------


def fetch_shares_snapshot_yfinance(yf_module, yf_ticker: str) -> dict:
    """回傳 {"shares_outstanding", "nav", "nav_currency", "source", "reason"}；
    抓不到（get_info() 掛掉，或 sharesOutstanding／推算所需的
    totalAssets／navPrice 都缺）回傳 source=None，呼叫端不寫入這天的紀錄
    （跟既有 EPS 快取一樣：沒有真資料就不要用假資料蓋掉，缺這天就是缺這天，
    下游 Δshares 算法本來就能跳過缺值的日子——見 compute_flow_series()）。"""
    try:
        info = yf_module.Ticker(yf_ticker).get_info()
    except Exception as e:  # noqa: BLE001
        return {"shares_outstanding": None, "nav": None, "nav_currency": None,
                "source": None, "reason": f"get_info() failed: {e}"}
    so = info.get("sharesOutstanding")
    nav = info.get("navPrice")
    total_assets = info.get("totalAssets")
    currency = info.get("currency")
    source = None
    reason = None
    if so and nav:
        source = "yfinance_direct"
    elif total_assets and nav:
        so = total_assets / nav
        source = "yfinance_derived"
        reason = "sharesOutstanding 缺值，用 totalAssets/navPrice 推算（見本檔 module docstring）"
    else:
        reason = f"get_info() 缺 sharesOutstanding／navPrice／totalAssets（有的欄位：" \
                  f"nav={nav!r}, totalAssets={total_assets!r}）"
    return {
        "shares_outstanding": round(so) if so else None,
        "nav": round(float(nav), 6) if nav is not None else None,
        "nav_currency": str(currency).upper() if currency else None,
        "source": source,
        "reason": reason,
    }


# 舊名保留給既有呼叫端／測試相容（2026-09-26 稍早版本只有這一個 tier）。
fetch_shares_snapshot = fetch_shares_snapshot_yfinance


# ---------------------------------------------------------------------------
# Staleness detection — only meaningful for the yfinance tier (tier 1/2
# sources are issuer-reported and trusted as-is).
# ---------------------------------------------------------------------------

STALE_YFINANCE_SOURCES = {"yfinance_direct", "yfinance_derived"}
STALE_MIN_REPEATS = 8          # 連續幾天 shares_outstanding 完全沒變才算「疑似不規律」
STALE_NAV_CHANGE_PCT = 0.3     # 同一段期間 NAV 至少要變動這個百分比，否則「份額沒變」可能只是市場真的很平靜


def detect_staleness(rows: list[dict], min_repeats: int = STALE_MIN_REPEATS,
                      nav_change_pct: float = STALE_NAV_CHANGE_PCT) -> bool:
    """純函式：只看 source 屬於 STALE_YFINANCE_SOURCES 的最新一段連續紀錄——
    如果最新 min_repeats 筆（或全部，不足 min_repeats 筆時）shares_outstanding
    完全相同、但同一段期間 NAV 變動幅度超過 nav_change_pct%，判定為「資料
    更新不規律」（yfinance 的 sharesOutstanding／totalAssets 欄位卡住沒動，
    但基金淨值明顯在變，代表這串資料不是每天都真的刷新）。日期需已排序或
    未排序皆可（函式內部自己排序）。"""
    valid = sorted(
        [r for r in rows if r.get("source") in STALE_YFINANCE_SOURCES and r.get("shares_outstanding") is not None
         and r.get("nav") is not None],
        key=lambda r: r["date"],
    )
    if len(valid) < 2:
        return False
    window = valid[-min_repeats:] if len(valid) >= min_repeats else valid
    shares_vals = {r["shares_outstanding"] for r in window}
    if len(shares_vals) != 1:
        return False  # 有變動，不是卡住
    navs = [r["nav"] for r in window]
    nav_range_pct = (max(navs) - min(navs)) / min(navs) * 100 if min(navs) else 0
    return nav_range_pct >= nav_change_pct


STALE_QUALITY_NOTE_ZH = ("偵測到份額資料疑似更新不規律（連續多天數值完全相同，但同期間 NAV 已明顯變動）"
                          "——來源為 yfinance 而非發行商官方逐日歷史，Δ份額算出的資金流可能不準，僅供參考。")


def compute_flow_series(rows: list[dict]) -> dict:
    """純函式：把逐日 shares_outstanding／nav 紀錄轉成每日流量、週流量、累計
    流量。回傳：
      daily — [{"date","flow_shares","flow_amount","nav_currency"}, ...]
              （第一天沒有前一天可比，不產生 daily 紀錄；缺值的日子被跳過，
              下一筆有值的日子會跟「上一筆有值的日子」比，不是跟前一個曆
              日比，這樣缺資料的日子不會被錯誤地算成 0 流量）。
      weekly — 依 ISO 週彙總 daily 的 flow_shares 加總 × 週最後一天的 nav。
      cumulative_since_start — 從第一筆有值的日子累計到最新一筆的 flow_amount
              加總（tier 1 來源這就是官方歷史涵蓋的整段期間；tier 2/3 來源
              是「這份紀錄自己開始追蹤以來的累計」，見 module docstring）。
      stale_shares_flag／quality_note_zh — 見 detect_staleness()；tier 1/2
              來源（source 不在 STALE_YFINANCE_SOURCES）恆為 False／None。
    """
    valid = [r for r in rows if r.get("shares_outstanding") is not None and r.get("nav") is not None]
    valid.sort(key=lambda r: r["date"])
    daily = []
    for prev, cur in zip(valid, valid[1:]):
        flow_shares = cur["shares_outstanding"] - prev["shares_outstanding"]
        flow_amount = flow_shares * cur["nav"]
        daily.append({
            "date": cur["date"], "flow_shares": flow_shares, "flow_amount": round(flow_amount, 2),
            "nav_currency": cur.get("nav_currency"),
        })

    weekly_map: dict[str, list[dict]] = {}
    for d in daily:
        # ISO 週（year, week）當 key——同一週的每日流量加總成一筆週流量。
        iso = datetime.date.fromisoformat(d["date"]).isocalendar()
        wk_key = f"{iso[0]}-W{iso[1]:02d}"
        weekly_map.setdefault(wk_key, []).append(d)
    weekly = []
    for wk_key in sorted(weekly_map.keys()):
        items = weekly_map[wk_key]
        weekly.append({
            "week": wk_key,
            "week_end_date": items[-1]["date"],
            "flow_shares": sum(i["flow_shares"] for i in items),
            "flow_amount": round(sum(i["flow_amount"] for i in items), 2),
            "n_days": len(items),
            "nav_currency": items[-1].get("nav_currency"),
        })

    cumulative_since_start = round(sum(d["flow_amount"] for d in daily), 2) if daily else None
    stale = detect_staleness(valid)
    return {
        "n_snapshots": len(valid),
        "start_date": valid[0]["date"] if valid else None,
        "latest_date": valid[-1]["date"] if valid else None,
        "daily": daily,
        "weekly": weekly,
        "cumulative_since_start": cumulative_since_start,
        "nav_currency": valid[-1].get("nav_currency") if valid else None,
        "latest_source": valid[-1].get("source") if valid else None,
        "stale_shares_flag": stale,
        "quality_note_zh": STALE_QUALITY_NOTE_ZH if stale else None,
    }
