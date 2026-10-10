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
  3. TPEx OpenAPI mopsfin_t187ap03_R (興櫃名冊) -> "<code>.TWO", market
     "TPEx-emerging" (2026-10-10: 3595 / 6826 / 7861 / 7892 / 7924 are
     興櫃 names, not new TPEx listings; before this step they went through
     the probe and showed up with no Chinese name).
  4. yfinance 1-month history probe, .TWO then .TW, for anything on none of
     the three rosters.
  5. Otherwise unresolved. The caller drops the row and reports it, so a
     bare code never reaches yfinance and silently returns all-None data.

Each roster row also carries the official industry code (TWSE 產業別 /
TPEx SecuritiesIndustryCode); TW_INDUSTRY turns it into the Chinese name.

The two roster URLs and the UA match scripts/build_price_momentum_tw.py.
Network failures degrade to the probe step. They never raise.
"""
from __future__ import annotations

import sys

TWSE_LISTED_URL = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
TPEX_LISTED_URL = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"
TPEX_EMERGING_URL = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_R"
BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"


# Industry code -> name. Checked 2026-10-10 by joining the three rosters with
# the ISIN pages (isin.twse.com.tw C_public.jsp strMode 2/4/5): every code
# mapped to exactly one name (code 20 had one 數位雲端 row out of 113).
TW_INDUSTRY = {
    "01": "水泥工業", "02": "食品工業", "03": "塑膠工業", "04": "紡織纖維",
    "05": "電機機械", "06": "電器電纜", "08": "玻璃陶瓷", "09": "造紙工業",
    "10": "鋼鐵工業", "11": "橡膠工業", "12": "汽車工業", "14": "建材營造業",
    "15": "航運業", "16": "觀光餐旅", "17": "金融保險業", "18": "貿易百貨業",
    "20": "其他業", "21": "化學工業", "22": "生技醫療業", "23": "油電燃氣業",
    "24": "半導體業", "25": "電腦及週邊設備業", "26": "光電業", "27": "通信網路業",
    "28": "電子零組件業", "29": "電子通路業", "30": "資訊服務業", "31": "其他電子業",
    "32": "文化創意業", "33": "農業科技業", "35": "綠能環保", "36": "數位雲端",
    "37": "運動休閒", "38": "居家生活",
}


def _fetch_roster(url: str, code_key: str, name_key: str,
                  industry_key: str) -> dict[str, dict]:
    try:
        import requests
        rows = requests.get(url, headers={"User-Agent": BROWSER_UA}, timeout=60).json()
    except Exception as exc:  # noqa: BLE001 — roster outage degrades to the probe step
        print(f"  WARN: TW roster fetch failed ({url}): {type(exc).__name__}: {exc}", file=sys.stderr)
        return {}
    out: dict[str, dict] = {}
    for r in rows or []:
        code = str(r.get(code_key, "")).strip()
        if code:
            ind = str(r.get(industry_key, "")).strip()
            out[code] = {"name": str(r.get(name_key, "")).strip(),
                         "industry": TW_INDUSTRY.get(ind)}
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
    """Returns ({code: {"ticker", "name", "market", "industry"}}, unresolved_codes).

    market is "TWSE", "TPEx", "TPEx-emerging" or "probe" (yfinance probe;
    name and industry unknown, so name falls back to the ticker and industry
    is None)."""
    codes = sorted({str(c).strip() for c in codes if str(c).strip()})
    rosters = (
        (".TW", "TWSE", _fetch_roster(TWSE_LISTED_URL, "公司代號", "公司簡稱", "產業別")),
        (".TWO", "TPEx", _fetch_roster(TPEX_LISTED_URL, "SecuritiesCompanyCode",
                                       "CompanyAbbreviation", "SecuritiesIndustryCode")),
        (".TWO", "TPEx-emerging", _fetch_roster(TPEX_EMERGING_URL, "SecuritiesCompanyCode",
                                                "CompanyAbbreviation", "SecuritiesIndustryCode")),
    )
    resolved: dict[str, dict] = {}
    unresolved: list[str] = []
    for c in codes:
        hit = next(((suffix, market, roster[c]) for suffix, market, roster in rosters
                    if c in roster), None)
        if hit:
            suffix, market, row = hit
            resolved[c] = {"ticker": c + suffix, "name": row["name"] or c + suffix,
                           "market": market, "industry": row["industry"]}
        else:
            t = _probe_yfinance(c)
            if t:
                resolved[c] = {"ticker": t, "name": t, "market": "probe", "industry": None}
            else:
                unresolved.append(c)
    return resolved, unresolved
