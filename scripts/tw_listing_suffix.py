"""Bare Taiwan stock code -> yfinance listing ticker (.TW 上市 / .TWO 上櫃).

Introduced 2026-10-09 for the isolated TW Koyfin pool (dd_tw_v1 screen ->
dd_tw_80col watchlist -> DD_tw_EPS_estimates_*.xlsx; see
notes/site-internal/root/_koyfin_tw_watchlist_20261009.md). Koyfin exports TW
names as bare codes ("2330", "5274"), so the xlsx alone cannot tell a TWSE
listing from a TPEx one. yfinance needs the right suffix: "5274.TW" returns
nothing, while "5274.TWO" works.

build_dd_screener.py --universe tw and snapshot_eps_estimates.py --universe tw
both key rows through this one module, so the monthly revision baseline and
the daily build agree on ticker strings. If they ever disagreed,
`prev_tickers.get(ticker)` would never match and every revision would stay
None.

Resolution order per code:
  1. TWSE OpenAPI t187ap03_L (上市名冊)       -> "<code>.TW"
  2. TPEx OpenAPI mopsfin_t187ap03_O (上櫃名冊) -> "<code>.TWO"
  3. yfinance 1-month history probe, .TWO then .TW. This catches names that
     just moved up from the emerging board and are not on the TPEx roster
     yet (3595 / 6826 / 7861 on 2026-10-09 all resolved as .TWO this way).
  4. Otherwise unresolved. The caller drops the row and reports it, so a
     bare code never reaches yfinance and silently returns all-None data.

The two roster URLs and the UA match scripts/build_price_momentum_tw.py.
Network failures degrade to the probe step. They never raise.
"""
from __future__ import annotations

import sys

TWSE_LISTED_URL = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
TPEX_LISTED_URL = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"
BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"


def _fetch_roster(url: str, code_key: str, name_key: str) -> dict[str, str]:
    try:
        import requests
        rows = requests.get(url, headers={"User-Agent": BROWSER_UA}, timeout=60).json()
    except Exception as exc:  # noqa: BLE001 — roster outage degrades to the probe step
        print(f"  WARN: TW roster fetch failed ({url}): {type(exc).__name__}: {exc}", file=sys.stderr)
        return {}
    out: dict[str, str] = {}
    for r in rows or []:
        code = str(r.get(code_key, "")).strip()
        if code:
            out[code] = str(r.get(name_key, "")).strip()
    return out


def _probe_yfinance(code: str) -> str | None:
    try:
        import yfinance as yf
    except ImportError:
        return None
    for suffix in (".TWO", ".TW"):
        try:
            h = yf.Ticker(code + suffix).history(period="1mo")
        except Exception:  # noqa: BLE001
            continue
        if h is not None and not h.empty:
            return code + suffix
    return None


def resolve_tw_codes(codes) -> tuple[dict[str, dict], list[str]]:
    """Returns ({code: {"ticker", "name", "market"}}, unresolved_codes).

    market is "TWSE", "TPEx" or "probe" (yfinance probe; name unknown, so it
    falls back to the ticker)."""
    codes = sorted({str(c).strip() for c in codes if str(c).strip()})
    twse = _fetch_roster(TWSE_LISTED_URL, "公司代號", "公司簡稱")
    tpex = _fetch_roster(TPEX_LISTED_URL, "SecuritiesCompanyCode", "CompanyAbbreviation")
    resolved: dict[str, dict] = {}
    unresolved: list[str] = []
    for c in codes:
        if c in twse:
            resolved[c] = {"ticker": f"{c}.TW", "name": twse[c] or f"{c}.TW", "market": "TWSE"}
        elif c in tpex:
            resolved[c] = {"ticker": f"{c}.TWO", "name": tpex[c] or f"{c}.TWO", "market": "TPEx"}
        else:
            t = _probe_yfinance(c)
            if t:
                resolved[c] = {"ticker": t, "name": t, "market": "probe"}
            else:
                unresolved.append(c)
    return resolved, unresolved
