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

Sheet 2 "Notes" stores snapshot date at B2.

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


# Foreign exchange suffix → bare TW/JP/etc. base used in Excel.
# Excel exports use bare numeric codes (2330, 6857) while the DD universe uses
# yfinance-style suffixed tickers (2330.TW, 6857.T). Strip the suffix on lookup.
_SUFFIX_STRIPS = (".TW", ".T", ".JP", ".HK", ".KS", ".KQ", ".SS", ".SZ")

# Explicit ticker aliases for cases where the DD-universe ticker doesn't match
# the Excel/Koyfin code via suffix-strip alone — typically ADRs whose Koyfin
# uses the primary listing code instead of the ADR ticker.
#   LVMH ADR (LVMUY in US OTC) vs Koyfin primary Euronext Paris code "MC"
# Add new pairs here as the universe expands; this is the single source of
# truth (no env var, no config file — keep it surgical and reviewable in git).
_EXPLICIT_ALIASES = {
    "LVMH": "MC",   # LVMH Moët Hennessy — Koyfin uses Paris primary "MC"
}


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
    v = c.find("s:v", NS)
    if v is None or v.text is None:
        return None
    if t == "s":
        return sst[int(v.text)]
    if t == "b":
        return bool(int(v.text))
    try:
        return float(v.text)
    except ValueError:
        return v.text


def _col_letter(ref: str) -> str:
    """A1 -> A, AB12 -> AB."""
    return "".join(ch for ch in ref if ch.isalpha())


def _parse_eps_sheet(sheet_root, sst: list[str]) -> dict[str, dict]:
    rows = sheet_root.findall(".//s:row", NS)
    if not rows:
        return {}

    # Header row: map column letter -> field name
    header_map: dict[str, str] = {}
    for c in rows[0].findall("s:c", NS):
        v = _cell_value(c, sst)
        if not isinstance(v, str):
            continue
        col = _col_letter(c.attrib.get("r", ""))
        lv = v.strip().lower()
        if lv == "ticker":
            header_map[col] = "ticker"
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

        # Excel stores growth/CAGR as fractions (0.0985 = 9.85%). Convert to pct.
        def _to_pct(x):
            if x is None or not isinstance(x, (int, float)):
                return None
            return round(float(x) * 100, 4)

        def _to_eps(x):
            if x is None or not isinstance(x, (int, float)):
                return None
            return round(float(x), 4)

        out[ticker] = {
            "fy1": _to_eps(rec.get("fy1")),
            "fy2": _to_eps(rec.get("fy2")),
            "fy3": _to_eps(rec.get("fy3")),
            "growth_fy1_fy2_pct": _to_pct(rec.get("growth_fy1_fy2")),
            "growth_fy2_fy3_pct": _to_pct(rec.get("growth_fy2_fy3")),
            "cagr_fy1_fy3_pct": _to_pct(rec.get("cagr_fy1_fy3")),
        }
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


def load_excel(path: Path) -> ExcelSnapshot:
    """Parse a specific xlsx file."""
    with zipfile.ZipFile(path) as z:
        sst = _read_sst(z)
        with z.open("xl/worksheets/sheet1.xml") as f:
            sheet1 = ET.parse(f).getroot()
        tickers = _parse_eps_sheet(sheet1, sst)
        snap_date = _parse_notes_snapshot_date(z, sst)

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
