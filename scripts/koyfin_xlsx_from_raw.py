#!/usr/bin/env python3
"""Koyfin raw-scrape (pipe-separated txt) -> DD_universe_EPS_estimates_YYYYMMDD.xlsx.

Promoted into the repo from the scratchpad prototype (build_xlsx_v2.py,
2026-09-17) when the two-column short-interest / insider refresh needed a
durable, re-runnable builder instead of a one-off scratch script — see
.claude/skills/refresh-eps-screener-web/SKILL.md v2.0 Step 6.

Same parsing rules and 54-column header contract as the scratchpad prototype
(itself the 2026-09-17 fundamental-gates refresh: 19 legacy columns + 35 new
capital/quality/valuation columns), PLUS two more appended columns (still the
same day, second refresh) sourced from Koyfin's "Short Interest > % Of Shares
Outstanding" and "Insider Transactions, Shares (Net) - 3M" watchlist columns:

  "Short Interest % Float"  (f[52]) -> percent already in % units
  "Insider Net Buy 3M"      (f[53]) -> signed raw share count (net buy - sell,
                                       trailing 3 months; NOT USD, NOT millions)

Raw txt row shape: 54 pipe-separated fields per row (f[0]=ticker, f[1..53]=
data columns; f[16]="Country" is scraped for the fingerprint/QA trail but not
written into the xlsx, matching the original 52-field prototype's behavior).

Usage:
    python3 scripts/koyfin_xlsx_from_raw.py --raw PATH --out PATH \\
        --snapshot-date YYYY-MM-DD [--universe-note "..."]

`--out` is a full path (no hardcoded DD_universe family name in this script),
so the v5 smallcap pool (2026-09-17, second Koyfin universe — see
scripts/build_dd_screener.py --universe smallcap) reuses this builder
unchanged, just pointing --out at data/eps-estimates/DD_smallcap_EPS_estimates_
YYYYMMDD.xlsx and passing --universe-note to label the Notes sheet.

Loader: scripts/load_eps_estimates_xlsx.py (exact-header match for all 35+2
fundamental-gates columns via `_NEW_FUND_HEADER_MAP`; legacy 7 + ROIC/FCF
columns via the loose substring rules — see that module's docstring for the
full header -> field contract).
"""
from __future__ import annotations

import argparse
import re

from openpyxl import Workbook


def blank(v: str) -> bool:
    return v.strip() in ("", "-", "—", "N/A")


def pct(s: str, gate: bool = True):
    """Percent field, already in "12.34 %" form -> plain float 12.34.
    `gate=True` applies the legacy sanity range (-100..200) used only on the
    6 original quality columns (ROIC/FCF Margin/ROIC 5Y/EBIT Margin/ROIC 3Y/
    Tax Rate) — every other percent column here passes `gate=False` (no range
    check), matching the 2026-09-17 fundamental-gates convention."""
    if blank(s):
        return None
    v = float(s.replace("%", "").replace(",", "").strip())
    return None if (gate and (v < -100 or v > 200)) else v


def num(s: str):
    """Generic signed number with optional K/M/B/T suffix, $ prefix, or
    accounting-style parens for negatives (e.g. Koyfin's insider net-shares
    column). Passed through as-is (no unit rescale) — used for ratios (x),
    counts (shares, CCC days), RSI, prices, and the two 2026-09-17b columns."""
    if blank(s):
        return None
    v = s.replace("$", "").replace(",", "").strip()
    neg = False
    if v.startswith("(") and v.endswith(")"):
        neg, v = True, v[1:-1]
    v = v.replace("x", "").strip()
    m = re.match(r"^(-?[\d.]+)\s*([KMBT]?)$", v)
    if not m:
        raise ValueError(s)
    x = float(m.group(1))
    u = m.group(2)
    out = x * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}[u] if u else x
    return round(-out if neg else out, 4)


def usd_m(s: str):
    """Money -> USD millions (unit-rescaling variant of num(), same K/M/B/T
    suffix table but always normalized to millions)."""
    if blank(s):
        return None
    v = s.replace("$", "").replace(",", "").strip()
    neg = False
    if v.startswith("(") and v.endswith(")"):
        neg, v = True, v[1:-1]
    m = re.match(r"^(-?[\d.]+)\s*([KMBT]?)$", v)
    if not m:
        raise ValueError(s)
    x = float(m.group(1))
    u = m.group(2)
    out = round(x * {"": 1e-6, "K": 1e-3, "M": 1, "B": 1e3, "T": 1e6}[u], 2)
    return -out if neg else out


def eps(s: str):
    return None if blank(s) else float(s.replace(",", ""))


HEADER = [
    "Ticker", "FY1E EPS", "FY2E EPS", "FY3E EPS", "FY1->FY2 Growth %", "FY2->FY3 Growth %", "FY1->FY3 CAGR %",
    "ROIC %", "FCF Margin %", "ROIC 5Y Avg %", "EBIT Margin %", "ROIC 3Y Avg %", "Tax Rate %",
    "Revenue FY", "Revenue FY-3", "EBIT FY", "EBIT FY-3", "Invested Capital FY", "Invested Capital FY-3",
    "Rev YoY FQ0 %", "Rev YoY FQ-1 %", "Rev YoY FQ-2 %", "Rev YoY FQ-3 %",
    "Gross Margin LTM %", "Gross Margin FY-1 %", "Gross Margin FY-2 %", "Gross Margin FY-3 %",
    "Sales LTM", "Op Income LTM", "Net Debt / EBITDA x", "Sales Growth YoY %", "Op Income Growth YoY %",
    "Diluted Shares FY", "Diluted Shares FY-3", "SBC LTM", "Capex LTM", "FCF LTM", "Net Debt LTM", "CCC Days",
    "PE NTM x", "PE NTM 5Y Avg x", "PB x", "PB 5Y Avg x", "RSI 14", "Price Chg 6M %", "Buyback LTM",
    "Target High", "Target Low", "Target Avg", "Net Income Margin LTM %", "Est Rev CAGR 3Y %",
    "Est EPS CAGR 3Y %", "Below 52W High %", "Last Price Local",
    # 2026-09-17b (second same-day refresh): 籌碼面 two-column addition.
    "Short Interest % Float", "Insider Net Buy 3M",
]


def build_row(f: list[str]):
    t = f[0]
    return [
        t, eps(f[1]), eps(f[2]), eps(f[3]), None, None, None,
        pct(f[4]), pct(f[5]), pct(f[6]), pct(f[7]), pct(f[8]), pct(f[9]),
        usd_m(f[10]), usd_m(f[11]), usd_m(f[12]), usd_m(f[13]), usd_m(f[14]), usd_m(f[15]),
        # f[16] = Country, scraped for QA/fingerprint only — not written to xlsx.
        pct(f[17], False), pct(f[18], False), pct(f[19], False), pct(f[20], False),
        pct(f[21], False), pct(f[22], False), pct(f[23], False), pct(f[24], False),
        usd_m(f[25]), usd_m(f[26]), num(f[27]), pct(f[28], False), pct(f[29], False),
        num(f[30]), num(f[31]), usd_m(f[32]), usd_m(f[33]), usd_m(f[34]), usd_m(f[35]), num(f[36]),
        num(f[37]), num(f[38]), num(f[39]), num(f[40]), num(f[41]), pct(f[42], False), usd_m(f[43]),
        num(f[44]), num(f[45]), num(f[46]), pct(f[47], False), pct(f[48], False), pct(f[49], False),
        pct(f[50], False), num(f[51]),
        # 2026-09-17b additions:
        pct(f[52], False) if len(f) > 52 else None,   # Short Interest % Float
        num(f[53]) if len(f) > 53 else None,           # Insider Net Buy 3M (raw shares, signed)
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw", required=True, help="Path to the KROW-dumped raw txt (pipe-separated)")
    ap.add_argument("--out", required=True, help="Output xlsx path")
    ap.add_argument("--snapshot-date", required=True, help="YYYY-MM-DD, written to Notes!B2")
    ap.add_argument("--universe-note", default=None,
                     help="Optional Notes!B4 label describing the source universe when it isn't the "
                          "default DD_universe watchlist (2026-09-17, v5 smallcap pool) — e.g. "
                          "\"dd_smallcap watchlist (screen dd_smallcap_v5: US, $1-20B, ROIC>=15, FCF>=10)\". "
                          "Omit for the default family (no B4 row written, output unchanged).")
    args = ap.parse_args()

    wb = Workbook()
    ws = wb.active
    ws.title = "EPS Estimates"
    ws.append(HEADER)
    n = 0
    with open(args.raw, encoding="utf-8") as fh:
        for line in fh:
            f = line.rstrip("\n").split("|")
            if len(f) < 52:
                continue
            ws.append(build_row(f))
            n += 1

    ws2 = wb.create_sheet("Notes")
    ws2["A2"] = "Snapshot Date"; ws2["B2"] = args.snapshot_date
    ws2["A3"] = "Quality Source"; ws2["B3"] = "koyfin-web"
    if args.universe_note:
        ws2["A4"] = "Universe"; ws2["B4"] = args.universe_note
    ws2["B5"] = (
        f"{args.snapshot_date} web scrape, {len(HEADER) - 1} fields (19 prior + 35 fundamental-gates "
        "cols [2026-09-17] + 2 short-interest/insider cols [2026-09-17b]). Money=USD mm; shares=mm "
        "(legacy cols) or raw share count (Insider Net Buy 3M — NOT thousands/millions); "
        "Target/Last Price=local ccy. Short Interest % Float = % of float (already in % units, "
        "no ratio conversion). Insider Net Buy 3M = net shares bought minus sold, trailing 3 months, "
        "signed (positive=net buying, negative=net selling; source: Koyfin 'Insider Transactions, "
        "Shares (Net) - 3M'). Range gate (-100..200) only on the 6 legacy pct cols."
    )
    wb.save(args.out)
    print("rows", n, "cols", len(HEADER), "->", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
