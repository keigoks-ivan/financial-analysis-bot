#!/usr/bin/env python3
"""EPS estimates Excel loader.

Reads the monthly EPS estimates Excel export from data/eps-estimates/ and
exposes a normalized snapshot for build_dd_screener.py and snapshot_eps_estimates.py.

stdlib-only (zipfile + xml.etree) — no openpyxl/pandas dependency, mirrors how
the rest of the build pipeline keeps deps minimal.

Expected file pattern: data/eps-estimates/DD_universe_EPS_estimates_YYYYMMDD.xlsx
Sheet 1 "EPS Estimates" columns (row 1 header):
  Ticker | FY1E EPS | FY2E EPS | FY3E EPS |
  FY1->FY2 Growth % | FY2->FY3 Growth % | FY1->FY3 CAGR %

Optional columns (2026-09-09, refresh-eps-screener-web Koyfin quality import —
see .claude/skills/refresh-eps-screener-web/SKILL.md Step 1/6): any header
containing "roic" (case-insensitive) maps to `roic`; any header containing
both "fcf" and "margin" (or "free cash flow" and "margin") maps to
`fcf_margin`. Both are OPTIONAL — files without them (all pre-2026-09 xlsx,
and the sister `refresh-eps-screener` Excel-file skill until it adopts the
same two columns) load exactly as before, with `roic_pct`/`fcf_margin_pct`
simply None on every record.

A third optional column (2026-09-09, v3 席位資格 durability source — see
scripts/engine/build_dd_screener.py enrich_ticker's `durable_5y`/`durable_source`):
any header containing "roic" AND ("5y" or "5 yr") maps to `roic_5y_avg`
(checked BEFORE the plain "roic" rule above, since a header like "ROIC 5Y
Avg %" would otherwise match "roic" first). Also OPTIONAL, same
ratio-vs-percent rule as roic/fcf_margin below, output field `roic_5y_avg_pct`.
NOTE (2026-09-16): this rule used to also trigger on a bare "avg" in the
header, which meant "ROIC 3Y Avg %" was mis-captured as roic_5y_avg — tightened
to require "5y"/"5 yr" specifically, with a sibling "3y"/"3 yr" rule added
right below it for `roic_3y_avg`.

Nine more optional columns (2026-09-16, ROIC decomposition / persistence /
incremental-ROIC screener additions — see scripts/build_dd_screener.py
compute_roic_decomposition()): exact header strings, all OPTIONAL and all
None on any pre-2026-09-16 xlsx —
  "EBIT Margin %"          -> ebit_margin_pct   (LTM, percent)
  "ROIC 3Y Avg %"          -> roic_3y_avg_pct   (percent; see NOTE above)
  "Tax Rate %"             -> tax_rate_pct      (percent; may be blank/garbage —
                              sanity-checked and defaulted downstream in
                              build_dd_screener.py, NOT here)
  "Revenue FY" / "Revenue FY-3"                 -> rev_fy / rev_fy3   (USD millions)
  "EBIT FY" / "EBIT FY-3"                       -> ebit_fy / ebit_fy3 (USD millions; may be negative)
  "Invested Capital FY" / "Invested Capital FY-3" -> ic_fy / ic_fy3   (USD millions)
The three percent columns follow the same ratio-vs-percent rule as
roic/fcf_margin below. The six USD-millions columns are passed through as
plain floats (no ratio/percent handling — they're absolute dollar figures,
not margins) via `_to_num`.

Percent-unit rule for the optional columns: a value is treated as a raw
ratio (e.g. 0.19) and multiplied by 100 iff its header has no "%" marker AND
|value| <= 1.5 — real-world ROIC / FCF margins for this universe are well
under 150%, so this cleanly separates "0.19" (ratio) from "19.4" (already a
percent) without needing the header text as a cue. When the header itself
says "%" (e.g. "ROIC %", the column refresh-eps-screener-web writes), the
value is trusted as already being in percent units and passed through as-is.

35 more optional columns (2026-09-17, fundamental-gates screener additions —
see scripts/build_dd_screener.py compute_fundamental_gates()): EXACT header
strings only (`_NEW_FUND_HEADER_MAP` below), matched against the raw header
text BEFORE the loose substring rules above so there is no risk of a partial
token (e.g. "ebit", "revenue", "fy") from these new columns colliding with
the existing ebit_margin/tax_rate/rev_fy/ebit_fy/ic_fy loose rules — this is
exactly the bug that once made AAPL's legacy `ebit_fy` read 9.58 (a stray
"Op Income Growth YoY %" cell) instead of 133050 (the real "EBIT FY" cell).
All 35 are OPTIONAL and None on any pre-2026-09-17 xlsx. Every one of these
headers already carries an explicit unit marker ("%" or "x") in this
Koyfin export and the cell value is already in that unit (e.g. "ROIC %"
66.77 means 66.77%, not 0.6677) — so unlike roic_pct/fcf_margin_pct above,
no ratio-vs-percent detection is needed; all 35 are plain float passthrough
via `_to_num` (sign preserved — Capex LTM / Buyback LTM are negative
cash-flow figures, Net Debt LTM negative means net cash; abs()/derivation
happens downstream in compute_fundamental_gates, not here):

  "Rev YoY FQ0/-1/-2/-3 %"          -> rev_yoy_fq0_pct..rev_yoy_fq3_pct (quarterly revenue YoY, latest quarter first)
  "Gross Margin LTM/FY-1/-2/-3 %"   -> gm_ltm_pct, gm_fy1_pct, gm_fy2_pct, gm_fy3_pct
  "Sales LTM" / "Op Income LTM"     -> sales_ltm, ebit_ltm (USD millions)
  "Net Debt / EBITDA x"             -> net_debt_ebitda_x (blank when net cash / negative EBITDA)
  "Sales Growth YoY %" / "Op Income Growth YoY %" -> sales_growth_fy_pct, ebit_growth_fy_pct
  "Diluted Shares FY" / "-FY-3"     -> dil_shares_fy, dil_shares_fy3 (millions)
  "SBC/Capex/FCF/Net Debt/Buyback LTM" -> sbc_ltm, capex_ltm, fcf_ltm, net_debt_ltm, buyback_ltm (USD millions)
  "CCC Days"                        -> ccc_days
  "PE NTM x" / "PE NTM 5Y Avg x" / "PB x" / "PB 5Y Avg x" -> pe_ntm_x, pe_ntm_5y_avg_x, pb_x, pb_5y_avg_x
  "RSI 14" / "Price Chg 6M %"       -> rsi14, price_chg_6m_pct
  "Target High/Low/Avg" / "Last Price Local" -> target_high, target_low, target_avg, last_price_local (LOCAL listing currency)
  "Net Income Margin LTM %" / "Est Rev CAGR 3Y %" / "Est EPS CAGR 3Y %" / "Below 52W High %"
      -> ni_margin_ltm_pct, est_rev_cagr_3y_pct, est_eps_cagr_3y_pct, below_52w_high_pct

Two more optional columns (2026-09-17, short-interest / insider screener additions —
see scripts/build_dd_screener.py compute_fundamental_gates() §L and
scripts/engine/grp.py grp_score()'s high_short_interest): EXACT header strings, both
OPTIONAL and None on any pre-2026-09-17b (second same-day refresh) xlsx, matched in
`_NEW_FUND_HEADER_MAP` the same way as the 35 fields above — chosen to avoid the
substrings "revenue"/"ebit"+"fy" that would otherwise collide with the legacy loose
rules:
  "Short Interest % Float"  -> short_interest_pct_float (percent, already in % units —
                                Koyfin "Short Interest > % Of Shares Outstanding")
  "Insider Net Buy 3M"      -> insider_net_buy_3m (raw share count, signed — positive
                                = net buying, negative = net selling; Koyfin "Insider
                                Transactions, Shares (Net) - 3M")
Both plain float passthrough via `_to_num` (no ratio/percent detection needed).

Sheet 2 "Notes" stores snapshot date at B2, and — optionally, only present on
xlsx carrying the Koyfin ROIC/FCF Margin columns — a quality-source label at
B3 (defaults to "koyfin-web" when absent, matching the A2/B2 label/value
convention used for the snapshot date).

Edge cases handled (per Notes B10):
  - FY3 missing (SEZL) -> fy3=None, growth_fy2_fy3=None, cagr=None
  - FY1 negative (LYV) -> cagr=None (geometric mean undefined)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = ROOT / "data" / "eps-estimates"
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
FILENAME_RE = re.compile(r"DD_universe_EPS_estimates_(\d{8})\.xlsx$")

# 2026-09-12: ADR 換算表 — Koyfin 匯出的 fy1/fy2/fy3 EPS 有時是普通股口徑，不是
# ADR 口徑（例：TSM 1 ADR = 5 股普通股）。單一權威讀取點，dd_numbers_extra.py
# 與 build_dd_screener.py 都呼叫 apply_adr_ratio()，不各自寫一份換算。
ADR_RATIOS_PATH = ROOT / "data" / "adr_ratios.json"
_adr_ratios_cache = None


def load_adr_ratios(path=None):
    """讀 data/adr_ratios.json。查無檔案或格式錯一律回空 dict，不擋任何呼叫端
    （沒有表就等於沒有任何 ticker 需要換算，行為與換算表新增前完全相同）。"""
    global _adr_ratios_cache
    if path is None and _adr_ratios_cache is not None:
        return _adr_ratios_cache
    p = path or ADR_RATIOS_PATH
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    if path is None:
        _adr_ratios_cache = data
    return data


def apply_adr_ratio(ticker, record, ratios=None):
    """把 Koyfin 記錄的 fy1/fy2/fy3 EPS 由普通股口徑換成 ADR 口徑（僅 adr_ratios.json
    表列的 ticker）。growth_fy1_fy2_pct／growth_fy2_fy3_pct／cagr_fy1_fy3_pct 是比率，
    換算前後不變，原樣保留。查無表列的 ticker（絕大多數）原樣回傳同一個 dict——不新增
    任何鍵，確保非 ADR ticker 輸出零變化。"""
    if not record:
        return record
    if ratios is None:
        ratios = load_adr_ratios()
    info = ratios.get(ticker)
    ratio = info.get("ratio") if info else None
    if not ratio:
        return record
    out = dict(record)
    for k in ("fy1", "fy2", "fy3"):
        if out.get(k) is not None:
            out[k] = round(out[k] * ratio, 4)
    out["eps_basis"] = "adr-usd (koyfin ordinary ×{0})".format(
        int(ratio) if float(ratio).is_integer() else ratio
    )
    return out


# Foreign exchange suffix → bare TW/JP/etc. base used in Excel.
# Excel exports use bare numeric codes (2330, 6857) while the DD universe uses
# yfinance-style suffixed tickers (2330.TW, 6857.T). Strip the suffix on lookup.
_SUFFIX_STRIPS = (".TW", ".T", ".JP", ".HK", ".KS", ".KQ", ".SS", ".SZ", ".AX", ".SW")

# Explicit ticker aliases for cases where the DD-universe ticker doesn't match
# the Excel/Koyfin code via suffix-strip alone — typically ADRs whose Koyfin
# uses the primary listing code instead of the ADR ticker.
#   LVMH ADR (LVMUY in US OTC) vs Koyfin primary Euronext Paris code "MC"
# Add new pairs here as the universe expands; this is the single source of
# truth (no env var, no config file — keep it surgical and reviewable in git).
_EXPLICIT_ALIASES = {
    "LVMH": "MC",      # LVMH Moët Hennessy — Koyfin uses Paris primary "MC"
    "SU":   "SU.FR",   # Schneider Electric — Koyfin uses Euronext Paris "SU.FR"
                       # (raw "SU" key returned Suncor CAD data → bad; .FR disambiguates)
    # 2026-09-09 web-scrape additions (refresh-eps-screener-web): Bursa
    # Malaysia listings whose Koyfin symbol is the company mnemonic, not the
    # numeric Bursa code the DD universe uses. AAON truncates to "AAO" in
    # Koyfin's own ticker cell (confirmed via raw innerText, not a CSS clip).
    "5246.KL": "WPRTS",    # Westports Holdings Berhad
    "5326.KL": "99SMART",  # 99 Speed Mart Retail Holdings Berhad
    "5398.KL": "GAMUDA",   # Gamuda Berhad
    "6139.KL": "TAKAFUL",  # Syarikat Takaful Malaysia Keluarga Berhad
    "AAON":    "AAO",      # AAON, Inc. — Koyfin ticker cell renders "AAO"
}

# Excel rows to drop on load (treated as if not present → consumers fall back
# to yfinance). Use when Koyfin export has clearly bad data for a ticker
# (wrong currency, wrong mapping, all-None) and we don't want it polluting
# downstream consensus. Single source of truth — both snapshot + build see
# the same skip set. Public so build_dd_screener.py can distinguish "known
# bad Excel row" from "genuine naming mismatch" in the coverage banner.
SKIP_TICKERS: set[str] = set()
# 2026-05-26 update: ABB Koyfin export now returns valid FY data (was all-None),
# SU resolved via _EXPLICIT_ALIASES mapping to "SU.FR" (Euronext Paris primary).
# Both removed from skip-list. Re-add here if a future Koyfin export reverts to
# bad data.


def _alias_keys(ticker: str) -> list[str]:
    """Return candidate Excel keys to try for a given DD ticker.

    Lookup order:
      1. exact ticker (e.g., "AAPL")
      2. explicit alias from _EXPLICIT_ALIASES (e.g., "LVMH" → "MC")
      3. suffix-stripped form (e.g., "2330.TW" → "2330")
    """
    out = [ticker]
    if ticker in _EXPLICIT_ALIASES:
        out.append(_EXPLICIT_ALIASES[ticker])
    for suf in _SUFFIX_STRIPS:
        if ticker.endswith(suf):
            out.append(ticker[: -len(suf)])
            break
    return out


@dataclass
class ExcelSnapshot:
    snapshot_date: str
    source_file: str
    tickers: dict[str, dict] = field(default_factory=dict)
    # 2026-09-09: Notes!B3 label for the optional Koyfin-scraped ROIC / FCF
    # Margin columns (see module docstring). Defaults to "koyfin-web" — legacy
    # xlsx files carry no B3 cell at all, so this is a snapshot-level default
    # rather than a per-record field.
    quality_source: str = "koyfin-web"

    def has(self, ticker: str) -> bool:
        return any(k in self.tickers for k in _alias_keys(ticker))

    def get(self, ticker: str) -> dict | None:
        for k in _alias_keys(ticker):
            v = self.tickers.get(k)
            if v is not None:
                return v
        return None


def _read_sst(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    with z.open("xl/sharedStrings.xml") as f:
        root = ET.parse(f).getroot()
    out = []
    for si in root.findall("s:si", NS):
        out.append("".join(n.text or "" for n in si.iter() if n.tag.endswith("}t")))
    return out


def _cell_value(c, sst: list[str]):
    t = c.attrib.get("t")
    # Inline string: <c t="inlineStr"><is><t>text</t></is></c>. openpyxl writes
    # strings this way (no sharedStrings table), so without this branch an
    # openpyxl-resaved workbook parses to 0 tickers. Koyfin exports use t="s".
    if t == "inlineStr":
        is_el = c.find("s:is", NS)
        if is_el is None:
            return None
        return "".join(n.text or "" for n in is_el.iter() if n.tag.endswith("}t"))
    v = c.find("s:v", NS)
    if v is None or v.text is None:
        return None
    if t == "s":
        return sst[int(v.text)]
    if t == "b":
        return bool(int(v.text))
    if t == "str":  # formula string result
        return v.text
    try:
        return float(v.text)
    except ValueError:
        return v.text


def _col_letter(ref: str) -> str:
    """A1 -> A, AB12 -> AB."""
    return "".join(ch for ch in ref if ch.isalpha())


# 2026-09-17: exact-header → field-name map for the 35 new fundamental-gates
# columns (see module docstring). Matched verbatim against the stripped
# header text (case-sensitive, no substring/token matching) so these can
# never collide with the loose "ebit"/"revenue"/"fy"/"5y" rules below.
_NEW_FUND_HEADER_MAP: dict[str, str] = {
    "Rev YoY FQ0 %": "rev_yoy_fq0_pct",
    "Rev YoY FQ-1 %": "rev_yoy_fq1_pct",
    "Rev YoY FQ-2 %": "rev_yoy_fq2_pct",
    "Rev YoY FQ-3 %": "rev_yoy_fq3_pct",
    "Gross Margin LTM %": "gm_ltm_pct",
    "Gross Margin FY-1 %": "gm_fy1_pct",
    "Gross Margin FY-2 %": "gm_fy2_pct",
    "Gross Margin FY-3 %": "gm_fy3_pct",
    "Sales LTM": "sales_ltm",
    "Op Income LTM": "ebit_ltm",
    "Net Debt / EBITDA x": "net_debt_ebitda_x",
    "Sales Growth YoY %": "sales_growth_fy_pct",
    "Op Income Growth YoY %": "ebit_growth_fy_pct",
    "Diluted Shares FY": "dil_shares_fy",
    "Diluted Shares FY-3": "dil_shares_fy3",
    "SBC LTM": "sbc_ltm",
    "Capex LTM": "capex_ltm",
    "FCF LTM": "fcf_ltm",
    "Net Debt LTM": "net_debt_ltm",
    "Buyback LTM": "buyback_ltm",
    "CCC Days": "ccc_days",
    "PE NTM x": "pe_ntm_x",
    "PE NTM 5Y Avg x": "pe_ntm_5y_avg_x",
    "PB x": "pb_x",
    "PB 5Y Avg x": "pb_5y_avg_x",
    "RSI 14": "rsi14",
    "Price Chg 6M %": "price_chg_6m_pct",
    "Target High": "target_high",
    "Target Low": "target_low",
    "Target Avg": "target_avg",
    "Last Price Local": "last_price_local",
    "Net Income Margin LTM %": "ni_margin_ltm_pct",
    "Est Rev CAGR 3Y %": "est_rev_cagr_3y_pct",
    "Est EPS CAGR 3Y %": "est_eps_cagr_3y_pct",
    "Below 52W High %": "below_52w_high_pct",
    # 2026-09-17 (second same-day refresh): short-interest / insider columns —
    # see module docstring "Two more optional columns" section above.
    "Short Interest % Float": "short_interest_pct_float",
    "Insider Net Buy 3M": "insider_net_buy_3m",
}


def _parse_eps_sheet(sheet_root, sst: list[str]) -> dict[str, dict]:
    rows = sheet_root.findall(".//s:row", NS)
    if not rows:
        return {}

    # Header row: map column letter -> field name
    header_map: dict[str, str] = {}
    # 2026-09-09: per-field "%" marker on the header text — drives the ratio
    # vs already-percent decision for the optional roic/fcf_margin columns
    # (see module docstring). Unused for the other fields.
    field_has_pct: dict[str, bool] = {}
    for c in rows[0].findall("s:c", NS):
        v = _cell_value(c, sst)
        if not isinstance(v, str):
            continue
        col = _col_letter(c.attrib.get("r", ""))
        raw = v.strip()
        lv = raw.lower()
        if lv == "ticker":
            header_map[col] = "ticker"
        elif raw in _NEW_FUND_HEADER_MAP:
            # 2026-09-17: exact match, checked BEFORE any loose substring rule
            # below — see module docstring + _NEW_FUND_HEADER_MAP comment.
            header_map[col] = _NEW_FUND_HEADER_MAP[raw]
        elif "fy1" in lv and "eps" in lv:
            header_map[col] = "fy1"
        elif "fy2" in lv and "eps" in lv:
            header_map[col] = "fy2"
        elif "fy3" in lv and "eps" in lv:
            header_map[col] = "fy3"
        elif "fy1" in lv and "fy2" in lv and "growth" in lv:
            header_map[col] = "growth_fy1_fy2"
        elif "fy2" in lv and "fy3" in lv and "growth" in lv:
            header_map[col] = "growth_fy2_fy3"
        elif "fy1" in lv and "fy3" in lv and "cagr" in lv:
            header_map[col] = "cagr_fy1_fy3"
        elif "roic" in lv and ("5y" in lv or "5 yr" in lv):
            header_map[col] = "roic_5y_avg"
            field_has_pct["roic_5y_avg"] = "%" in lv
        elif "roic" in lv and ("3y" in lv or "3 yr" in lv):
            header_map[col] = "roic_3y_avg"
            field_has_pct["roic_3y_avg"] = "%" in lv
        elif "roic" in lv:
            header_map[col] = "roic"
            field_has_pct["roic"] = "%" in lv
        elif ("fcf" in lv and "margin" in lv) or ("free cash flow" in lv and "margin" in lv):
            header_map[col] = "fcf_margin"
            field_has_pct["fcf_margin"] = "%" in lv
        # 2026-09-16: ROIC decomposition / incremental-ROIC inputs (see module
        # docstring). "ebit" + "margin" checked BEFORE the bare "ebit fy" rule
        # so "EBIT Margin %" doesn't fall through to the FY/FY-3 branch.
        elif "ebit" in lv and "margin" in lv:
            header_map[col] = "ebit_margin"
            field_has_pct["ebit_margin"] = "%" in lv
        elif "tax" in lv and "rate" in lv:
            header_map[col] = "tax_rate"
            field_has_pct["tax_rate"] = "%" in lv
        elif "revenue" in lv and "fy" in lv:
            header_map[col] = "rev_fy3" if "3" in lv else "rev_fy"
        elif "ebit" in lv and "fy" in lv:
            header_map[col] = "ebit_fy3" if "3" in lv else "ebit_fy"
        elif "invested" in lv and "capital" in lv:
            header_map[col] = "ic_fy3" if "3" in lv else "ic_fy"

    out: dict[str, dict] = {}
    for r in rows[1:]:
        rec: dict = {}
        for c in r.findall("s:c", NS):
            col = _col_letter(c.attrib.get("r", ""))
            field_name = header_map.get(col)
            if not field_name:
                continue
            rec[field_name] = _cell_value(c, sst)

        ticker = rec.get("ticker")
        if not ticker or not isinstance(ticker, str):
            continue
        ticker = ticker.strip()
        if not ticker:
            continue
        if ticker in SKIP_TICKERS:
            continue

        # Excel stores growth/CAGR as fractions (0.0985 = 9.85%). Convert to pct.
        def _to_pct(x):
            if x is None or not isinstance(x, (int, float)):
                return None
            return round(float(x) * 100, 4)

        def _to_eps(x):
            if x is None or not isinstance(x, (int, float)):
                return None
            return round(float(x), 4)

        # 2026-09-16: rev_fy/rev_fy3/ebit_fy/ebit_fy3/ic_fy/ic_fy3 — raw USD
        # millions, no ratio/percent handling (they're absolute dollar figures,
        # not margins). Plain float passthrough, same rounding as _to_eps.
        def _to_num(x):
            if x is None or not isinstance(x, (int, float)):
                return None
            return round(float(x), 4)

        # 2026-09-09: roic_pct / fcf_margin_pct — see module docstring for the
        # ratio-vs-percent detection rule. `has_pct` comes from the header text
        # captured once above; absent header (field never mapped) -> has_pct
        # defaults False, but rec.get() will also be None so it's moot.
        def _to_quality_pct(x, has_pct: bool):
            if x is None or not isinstance(x, (int, float)):
                return None
            val = float(x)
            if not has_pct and abs(val) <= 1.5:
                val *= 100.0
            return round(val, 4)

        out[ticker] = {
            "fy1": _to_eps(rec.get("fy1")),
            "fy2": _to_eps(rec.get("fy2")),
            "fy3": _to_eps(rec.get("fy3")),
            "growth_fy1_fy2_pct": _to_pct(rec.get("growth_fy1_fy2")),
            "growth_fy2_fy3_pct": _to_pct(rec.get("growth_fy2_fy3")),
            "cagr_fy1_fy3_pct": _to_pct(rec.get("cagr_fy1_fy3")),
            "roic_pct": _to_quality_pct(rec.get("roic"), field_has_pct.get("roic", False)),
            "fcf_margin_pct": _to_quality_pct(rec.get("fcf_margin"), field_has_pct.get("fcf_margin", False)),
            "roic_5y_avg_pct": _to_quality_pct(rec.get("roic_5y_avg"), field_has_pct.get("roic_5y_avg", False)),
            # 2026-09-16: ROIC decomposition / persistence / incremental-ROIC
            # inputs (see module docstring + build_dd_screener.compute_roic_decomposition).
            # All OPTIONAL — None on every pre-2026-09-16 xlsx.
            "ebit_margin_pct": _to_quality_pct(rec.get("ebit_margin"), field_has_pct.get("ebit_margin", False)),
            "roic_3y_avg_pct": _to_quality_pct(rec.get("roic_3y_avg"), field_has_pct.get("roic_3y_avg", False)),
            "tax_rate_pct": _to_quality_pct(rec.get("tax_rate"), field_has_pct.get("tax_rate", False)),
            "rev_fy": _to_num(rec.get("rev_fy")),
            "rev_fy3": _to_num(rec.get("rev_fy3")),
            "ebit_fy": _to_num(rec.get("ebit_fy")),
            "ebit_fy3": _to_num(rec.get("ebit_fy3")),
            "ic_fy": _to_num(rec.get("ic_fy")),
            "ic_fy3": _to_num(rec.get("ic_fy3")),
        }
        # 2026-09-17: 35 fundamental-gates columns — plain float passthrough,
        # see module docstring (_NEW_FUND_HEADER_MAP already carries the
        # final field name, so no per-field renaming needed here).
        for _fname in _NEW_FUND_HEADER_MAP.values():
            out[ticker][_fname] = _to_num(rec.get(_fname))
    return out


def _parse_notes_snapshot_date(z: zipfile.ZipFile, sst: list[str]) -> str | None:
    if "xl/worksheets/sheet2.xml" not in z.namelist():
        return None
    with z.open("xl/worksheets/sheet2.xml") as f:
        root = ET.parse(f).getroot()
    for r in root.findall(".//s:row", NS):
        for c in r.findall("s:c", NS):
            if c.attrib.get("r") == "B2":
                v = _cell_value(c, sst)
                if isinstance(v, str):
                    return v.strip()
    return None


def _parse_notes_quality_source(z: zipfile.ZipFile, sst: list[str]) -> str:
    """Optional Notes!B3 — label for the Koyfin-scraped ROIC / FCF Margin
    columns (refresh-eps-screener-web Step 6). Absent on any xlsx that
    predates the 2026-09-09 Koyfin quality import (or hasn't adopted it yet),
    which is the common case — default to "koyfin-web" so callers never see
    None here."""
    if "xl/worksheets/sheet2.xml" not in z.namelist():
        return "koyfin-web"
    with z.open("xl/worksheets/sheet2.xml") as f:
        root = ET.parse(f).getroot()
    for r in root.findall(".//s:row", NS):
        for c in r.findall("s:c", NS):
            if c.attrib.get("r") == "B3":
                v = _cell_value(c, sst)
                if isinstance(v, str) and v.strip():
                    return v.strip()
    return "koyfin-web"


def load_excel(path: Path) -> ExcelSnapshot:
    """Parse a specific xlsx file."""
    with zipfile.ZipFile(path) as z:
        sst = _read_sst(z)
        with z.open("xl/worksheets/sheet1.xml") as f:
            sheet1 = ET.parse(f).getroot()
        tickers = _parse_eps_sheet(sheet1, sst)
        snap_date = _parse_notes_snapshot_date(z, sst)
        quality_source = _parse_notes_quality_source(z, sst)

    if not snap_date:
        # Fallback: derive from filename DD_universe_EPS_estimates_YYYYMMDD.xlsx
        m = FILENAME_RE.search(path.name)
        if m:
            d = m.group(1)
            snap_date = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
        else:
            snap_date = "unknown"

    return ExcelSnapshot(
        snapshot_date=snap_date,
        source_file=path.name,
        tickers=tickers,
        quality_source=quality_source,
    )


def find_latest_excel(data_dir: Path = DEFAULT_DATA_DIR) -> Path | None:
    """Scan data dir, return the lexicographically largest filename matching pattern."""
    if not data_dir.exists():
        return None
    candidates = sorted(
        (p for p in data_dir.glob("DD_universe_EPS_estimates_*.xlsx") if FILENAME_RE.search(p.name)),
        key=lambda p: FILENAME_RE.search(p.name).group(1),
        reverse=True,
    )
    return candidates[0] if candidates else None


def find_excel_for_month(month: str, data_dir: Path = DEFAULT_DATA_DIR) -> Path | None:
    """month = 'YYYY-MM'. Returns the Excel whose snapshot YYYYMM matches, else None."""
    if not data_dir.exists():
        return None
    target = month.replace("-", "")  # "YYYYMM"
    for p in data_dir.glob("DD_universe_EPS_estimates_*.xlsx"):
        m = FILENAME_RE.search(p.name)
        if m and m.group(1).startswith(target):
            return p
    return None


def load_latest_excel(data_dir: Path = DEFAULT_DATA_DIR) -> ExcelSnapshot | None:
    path = find_latest_excel(data_dir)
    if path is None:
        return None
    return load_excel(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    ap.add_argument("--month", help="YYYY-MM; if omitted uses latest")
    ap.add_argument("--dump", action="store_true", help="Print full ticker dict")
    ap.add_argument("--ticker", help="Print one ticker's record")
    args = ap.parse_args()

    if args.month:
        path = find_excel_for_month(args.month, args.data_dir)
    else:
        path = find_latest_excel(args.data_dir)

    if path is None:
        print(f"No xlsx found in {args.data_dir}", file=sys.stderr)
        return 1

    snap = load_excel(path)
    print(f"source_file: {snap.source_file}")
    print(f"snapshot_date: {snap.snapshot_date}")
    print(f"ticker count: {len(snap.tickers)}")
    if args.ticker:
        print(json.dumps({args.ticker: snap.get(args.ticker)}, indent=2, ensure_ascii=False))
    if args.dump:
        print(json.dumps(snap.tickers, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
