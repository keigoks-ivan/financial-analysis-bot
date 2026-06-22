#!/usr/bin/env python3
"""
Scan docs/dd/ for DD_*.html files, cross-reference INDEX.md for v9.x/v10.x metadata,
and update the deep research table in docs/research/index.html.

v10.0 update: Remove R:R/上檔/下檔/紅燈 columns, add 長期持有信心 column.

Usage:
  python scripts/update_dd_index.py                  # normal regenerate (upside = DD 快照)
  python scripts/update_dd_index.py --refresh-prices # fetch yfinance and recompute upside
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
from functools import lru_cache
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"
DD_DIR = DOCS / "dd"
DCA_DIR = DOCS / "dca"
INDEX_HTML = DOCS / "research" / "index.html"
INDEX_MD = DD_DIR / "INDEX.md"
PRICE_CACHE = DOCS / "research" / "price_cache.json"
EPS_CAGR_CACHE = DOCS / "research" / ".eps_cagr_cache.json"

DCA_FILENAME_RE = re.compile(r"^DCA_([A-Z0-9]+)_(\d{8})\.html$")


def collect_dca_map() -> dict:
    """Scan docs/dca/ for DCA_{TICKER}_{YYYYMMDD}.html and return
    {ticker: latest_dca_href}. Same ticker → keep newest by date suffix.

    href format mirrors DD: '/dca/DCA_TICKER_YYYYMMDD.html' (absolute path).
    Returns empty dict if dca/ folder missing or empty (research page just
    shows '—' for every row).
    """
    out: dict = {}
    if DCA_DIR.exists():
        latest: dict[str, tuple[str, str]] = {}  # ticker -> (date_str, filename)
        for path in DCA_DIR.glob("DCA_*.html"):
            m = DCA_FILENAME_RE.match(path.name)
            if not m:
                continue
            ticker, date_str = m.group(1), m.group(2)
            prev = latest.get(ticker)
            if prev is None or date_str > prev[0]:
                latest[ticker] = (date_str, path.name)
        out = {t: f"/dca/{fname}" for t, (_, fname) in latest.items()}
    # v13 merged reports: 定見 points at the DD's own #decision anchor (v13 wins).
    for norm, fields in _v13_dca_overlay().items():
        out[norm] = fields["href"]
    return out


_DCA_EV_ANCHORS = (
    "機率加權期望值",
    "機率加權 5 年期望值",
    "機率加權 5年期望值",
    "機率加權 EV（5Y）",
    "機率加權 EV (5Y)",
    "機率加權EV（5Y）",
    "機率加權EV(5Y)",
    "期望值（機率加權）",
    "期望值(機率加權)",
    "5Y 累積",      # IRR decomposition table total row (catches hand-written DCAs)
    "機率加權",  # bare label — must be last so longer anchors win
)
_DCA_EV_CELL_CLOSE_RE = re.compile(
    r"</(td|th|p|h[1-6]|li|div|section|tr|article)\b", re.IGNORECASE
)
_DCA_EV_TR_CLOSE_RE = re.compile(r"</tr\s*>", re.IGNORECASE)
# Strips the canonical "/ IRR ≈ ±X.X%/yr" tag emitted by patch_dca_irr.py
# so a fresh extract on already-patched HTML doesn't mis-parse our own tag
# as the 5Y EV.
_DCA_EV_OUR_IRR_RE = re.compile(
    r"\s*/\s*IRR\s*[~≈]?\s*[+\-−]?\s*\d+(?:\.\d+)?\s*%(?:\s*/\s*(?:yr|年))?"
)
# Detects annualized-return markers in <strong> text or trailing context.
# Used to skip IRR/yr cells in _from_window's <strong> scan.
_DCA_EV_IRR_MARKER_RE = re.compile(
    r"/\s*(?:yr|年)|CAGR|年化|IRR", re.IGNORECASE
)
# Strips "X%/yr" and "IRR ≈ X%/yr" patterns from flat window text so the
# signed-percent parser doesn't land on the annualized value first.
_DCA_EV_STRIP_ANNUALIZED_RE = re.compile(
    r"(?:IRR\s*[≈~]?\s*)?[+\-−]?\s*\d+(?:\.\d+)?\s*%\s*/\s*(?:yr|年)",
    re.IGNORECASE,
)


def _dca_ev_find_all(s: str, kw: str) -> list[int]:
    out: list[int] = []
    start = 0
    while True:
        i = s.find(kw, start)
        if i < 0:
            return out
        out.append(i)
        start = i + len(kw)


def _dca_ev_in_cell(html: str, anchor_idx: int) -> bool:
    """First block-level close tag after anchor must be </td> or </th>."""
    m = _DCA_EV_CELL_CLOSE_RE.search(html[anchor_idx : anchor_idx + 400])
    return bool(m and m.group(1).lower() in ("td", "th"))


def _dca_ev_row_window(html: str, anchor_idx: int) -> str:
    """Window from anchor to the next </tr>, capped at 1500 bytes."""
    cap = min(len(html), anchor_idx + 1500)
    candidate = html[anchor_idx:cap]
    m = _DCA_EV_TR_CLOSE_RE.search(candidate)
    return candidate[: m.end()] if m else candidate


def extract_dca_ev_5y(dca_path) -> float | None:
    """Parse the 5-year probability-weighted EV from §4 Asymmetry Analysis.

    Returns the absolute 5-year return as a percentage float (e.g. 47.5 for
    "+47.5%", -32.25 for "-32.25%"). Returns None when no parseable EV is
    found in any table-cell-anchored EV row.

    Filters out narrative anchors in <p>/<h2>/<li> contexts where stray
    percentages (e.g. position-sizing 1.5%) could mislead the regex.
    Recognized number forms: "+57%", "1.49x", "+25% to +30%", "+88%（年化 ...）".
    """
    try:
        html = Path(dca_path).read_text(encoding="utf-8")
    except OSError:
        return None

    def _strip_tags(s: str) -> str:
        return re.sub(r"<[^>]+>", "", s)

    _SIGN = r"[+\-−]"

    def _norm_sign(s: str) -> str:
        return "-" if s in ("-", "−") else "+"

    def _parse_pct(text: str) -> float | None:
        rng = re.search(
            rf"({_SIGN})?\s*(\d+(?:\.\d+)?)\s*%\s*(?:to|~|至|–|—|-)\s*({_SIGN})?\s*(\d+(?:\.\d+)?)\s*%",
            text,
        )
        if rng:
            s1 = _norm_sign(rng.group(1) or "+")
            v1 = float(rng.group(2)) * (1 if s1 == "+" else -1)
            s2 = _norm_sign(rng.group(3) or s1)
            v2 = float(rng.group(4)) * (1 if s2 == "+" else -1)
            return (v1 + v2) / 2
        signed = re.search(rf"({_SIGN})\s*(\d+(?:\.\d+)?)\s*%", text)
        if signed:
            sign = _norm_sign(signed.group(1))
            val = float(signed.group(2))
            return val if sign == "+" else -val
        bare = re.search(r"(?<![=×x.\d])(\d+(?:\.\d+)?)\s*%", text)
        if bare:
            return float(bare.group(1))
        return None

    def _parse_mult(text: str) -> float | None:
        m = re.search(r"(?<![\d.×])(\d+\.\d+)\s*x", text)
        if m:
            mult = float(m.group(1))
            if mult >= 1.0:
                return (mult - 1) * 100
        return None

    def _from_window(window: str) -> float | None:
        for sm in re.finditer(r"<strong>(.*?)</strong>", window, re.DOTALL):
            text = _DCA_EV_OUR_IRR_RE.sub("", _strip_tags(sm.group(1)))
            if "期望值" in text and "%" not in text and "x" not in text:
                continue
            # Skip annualized rows: reject if text or immediate trailing context
            # contains /yr, /年, CAGR, 年化, or IRR — those are IRR cells, not 5Y absolute.
            # Clip trailing context to within current </td> so "年化" in the *next*
            # cell (e.g. separate IRR column) doesn't poison the check.
            _trail_raw = window[sm.end() : sm.end() + 80]
            _td_end = re.search(r"</td\s*>", _trail_raw, re.IGNORECASE)
            trail = _strip_tags(_trail_raw[: _td_end.start()] if _td_end else _trail_raw[:30])
            if _DCA_EV_IRR_MARKER_RE.search(text) or _DCA_EV_IRR_MARKER_RE.search(trail):
                continue
            pct = _parse_pct(text)
            if pct is not None:
                return pct
            mult = _parse_mult(text)
            if mult is not None:
                return mult
        # Strip annualized patterns (e.g. "+8.4%/yr") before the signed-percent
        # search so the parser doesn't land on an IRR/yr value in flat text.
        flat = _DCA_EV_STRIP_ANNUALIZED_RE.sub(
            "", _DCA_EV_OUR_IRR_RE.sub("", _strip_tags(window))
        )
        for kw in _DCA_EV_ANCHORS:
            flat = flat.replace(kw, "", 1)
        pct = _parse_pct(flat)
        if pct is not None:
            return pct
        return _parse_mult(flat)

    positions = sorted({
        idx for kw in _DCA_EV_ANCHORS for idx in _dca_ev_find_all(html, kw)
    })
    _BARE_KW = "機率加權"
    _LONGER_ANCHORS = set(_DCA_EV_ANCHORS) - {_BARE_KW}

    for anchor_idx in positions:
        if not _dca_ev_in_cell(html, anchor_idx):
            continue
        # Guard: if matched by the bare "機率加權" anchor (not a longer variant),
        # skip if trailing context contains "IRR" — that's the annualized row.
        is_bare = not any(
            html[anchor_idx:].startswith(a) for a in _LONGER_ANCHORS
        )
        if is_bare and "IRR" in html[anchor_idx + len(_BARE_KW): anchor_idx + len(_BARE_KW) + 15]:
            continue
        ev = _from_window(_dca_ev_row_window(html, anchor_idx))
        if ev is not None:
            return ev
    return None


def compute_dca_irr(ev_5y_pct: float) -> float:
    """Annualized IRR (%) from 5-year absolute return (%).

    e.g. +58% 5Y → 9.59%/yr; -51% → -13.36%/yr."""
    base = 1 + ev_5y_pct / 100
    if base <= 0:
        return -100.0
    return (base ** (1 / 5) - 1) * 100


_TR_PATTERN = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD_PATTERN = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)


def _parse_row_return(row_html: str) -> float | None:
    """Best-effort 5Y absolute return % from a scenario <tr>.

    Tries signed pct first (+92%, −47%, -15%), then x-multiple (1.92x → 92%).
    Strips our own canonical "/ IRR ≈ ..." tag so re-runs don't pick it up."""
    text = _DCA_EV_OUR_IRR_RE.sub("", re.sub(r"<[^>]+>", " ", row_html))
    # Skip a "vs $XYZ" anchor column by searching for first signed percent.
    signed = re.search(r"([+\-−])\s*(\d+(?:\.\d+)?)\s*%", text)
    if signed:
        sign = -1 if signed.group(1) in ("-", "−") else 1
        return sign * float(signed.group(2))
    mult = re.search(r"(?<![\d.])(\d+\.\d+)\s*x", text)
    if mult:
        return (float(mult.group(1)) - 1) * 100
    return None


def _parse_row_prob(row_html: str) -> float | None:
    """Probability % from the LAST <td> in a scenario <tr>. Returns None if
    no parseable percent."""
    tds = _TD_PATTERN.findall(row_html)
    if not tds:
        return None
    last = re.sub(r"<[^>]+>", "", tds[-1])
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", last)
    return float(m.group(1)) if m else None


def _extract_scenario_rows(html: str, anchor_idx: int) -> list[dict] | None:
    """Find Bull/Base/Bear (or N) scenario rows in the §4 table containing
    `anchor_idx` (the 機率加權期望值 EV-row anchor).

    Returns list of {"return": pct, "prob": pct} for each scenario row, or
    None when the table can't be identified or fewer than 2 rows parsed.
    Caller decides which row is the worst (Bear)."""
    # Walk back to <table>... opening that holds the EV row.
    table_start = html.rfind("<table", 0, anchor_idx)
    if table_start < 0:
        return None
    table_end = html.find("</table>", anchor_idx)
    if table_end < 0:
        return None
    table_html = html[table_start : table_end + len("</table>")]

    scenarios: list[dict] = []
    for m in _TR_PATTERN.finditer(table_html):
        row = m.group(0)
        # Stop at the EV summary row itself.
        if any(kw in row for kw in _DCA_EV_ANCHORS):
            break
        # Skip header rows (no <td>, only <th>).
        if "<td" not in row.lower():
            continue
        # Scenario rows have ≥3 cells (label / return / basis / prob, etc).
        # Excludes 2-cell dashboard "description" rows whose narrative text
        # can spuriously match signed-pct patterns (e.g. "53-63% 寡占").
        tds = _TD_PATTERN.findall(row)
        if len(tds) < 3:
            continue
        ret = _parse_row_return(row)
        prob = _parse_row_prob(row)
        if ret is None or prob is None:
            continue
        if not (0 < prob <= 100):
            continue
        scenarios.append({"return": ret, "prob": prob})
    if len(scenarios) < 2:
        return None
    return scenarios


_DCA_CELL_RE = re.compile(
    r'<div[^>]*class="(?:(?:status-)?cell)[^"]*"[^>]*>',
    re.DOTALL,
)
_DCA_VALUE_RE = re.compile(
    r'<div[^>]*class="(?:value|body|status-value|status-main)[^"]*"[^>]*>(.*?)</div>',
    re.DOTALL,
)
_DCA_ARROWS = ("↑", "→", "↓")


def _dca_find_arrow_in_html(html_fragment: str) -> "str | None":
    """Find first moat trend arrow in html_fragment.

    Prefers arrows found inside value/body/status-value/status-main divs
    (the big display element) to avoid false hits from narrative text.
    """
    for vm in _DCA_VALUE_RE.finditer(html_fragment):
        content = vm.group(1)
        for arrow in _DCA_ARROWS:
            if arrow in content:
                return arrow
    # Fallback: any arrow in the fragment
    for arrow in _DCA_ARROWS:
        if arrow in html_fragment:
            return arrow
    return None


def extract_dca_moat_trend(dca_path) -> "str | None":
    """Return the moat trend arrow (↑/→/↓) from a DCA HTML file, or None.

    Extraction strategy (first hit wins):
    0. Machine-readable marker `<!-- dca-moat-trend: X -->` in <head>
       (DCA skill v1.2+ guarantees this). Deterministic primary path.
    1. Status Bar 2nd cell — authoritative moat_trend visual output.
       Cell boundary detection uses class="cell"/"status-cell" divs.
       Arrow search within the 2nd cell prefers value/body/status-value/
       status-main div content to avoid stray arrows in narrative text.
    2. Frequency count of literal '↑ widening', '→ holding', '↓ narrowing'
       patterns across the whole file. The spec template lists each exactly
       once as a guide; the chosen value gets repeated in Status Bar + Phase
       A1 conclusion + §1 — so frequency wins.
    3. Last resort: 'moat_trend [↑→↓]' keyword pattern.
    """
    try:
        html = Path(dca_path).read_text(encoding="utf-8")
    except OSError:
        return None

    # Strategy 0: machine-readable marker (v1.2+ guarantee)
    m0 = re.search(r"<!--\s*dca-moat-trend:\s*([↑→↓])\s*-->", html)
    if m0:
        return m0.group(1)

    # Strategy 1: status-bar 2nd cell
    sb_idx = html.find('class="status-bar"')
    if sb_idx >= 0:
        sb_html = html[sb_idx : sb_idx + 3000]
        cell_starts = [m.start() for m in _DCA_CELL_RE.finditer(sb_html)]
        if len(cell_starts) >= 2:
            end = cell_starts[2] if len(cell_starts) > 2 else len(sb_html)
            second_cell = sb_html[cell_starts[1] : end]
            arrow = _dca_find_arrow_in_html(second_cell)
            if arrow:
                return arrow

    # Strategy 2: named pattern frequency
    counts = {
        "↑": len(re.findall(r"↑\s*widening", html)),
        "→": len(re.findall(r"→\s*holding", html)),
        "↓": len(re.findall(r"↓\s*narrowing", html)),
    }
    if any(v > 0 for v in counts.values()):
        return max(counts, key=lambda k: counts[k])

    # Strategy 3: explicit moat_trend keyword
    m3 = re.search(r"moat_trend\s*([↑→↓])", html)
    if m3:
        return m3.group(1)

    return None


def collect_dca_moat_trend_map() -> dict:
    """Return {ticker: arrow} for each ticker's latest DCA.

    arrow is one of '↑'/'→'/'↓'. Tickers where extraction fails are omitted.
    Mirrors collect_dca_bear_maps() scan pattern but returns a single dict.
    """
    out: dict = {}
    if DCA_DIR.exists():
        latest: dict = {}
        for path in DCA_DIR.glob("DCA_*.html"):
            m = DCA_FILENAME_RE.match(path.name)
            if not m:
                continue
            ticker, date_str = m.group(1), m.group(2)
            prev = latest.get(ticker)
            if prev is None or date_str > prev[0]:
                latest[ticker] = (date_str, path)
        for ticker, (_, path) in latest.items():
            arrow = extract_dca_moat_trend(path)
            if arrow is not None:
                out[ticker] = arrow
    # v13 merged reports: authoritative moat_trend comes from dd-meta (v13 wins).
    for norm, fields in _v13_dca_overlay().items():
        if fields["moat_trend"] is not None:
            out[norm] = fields["moat_trend"]
    return out


def collect_dca_ev_map() -> dict:
    """Return {ticker: ev_5y_pct} parsed from each ticker's latest DCA file.

    Tickers without a parseable §4 EV are omitted. Caller should treat
    missing ticker as "no EV available" and render '—'.
    """
    out: dict[str, float] = {}
    if DCA_DIR.exists():
        # Pick latest DCA per ticker (mirrors collect_dca_map logic).
        latest: dict[str, tuple[str, Path]] = {}
        for path in DCA_DIR.glob("DCA_*.html"):
            m = DCA_FILENAME_RE.match(path.name)
            if not m:
                continue
            ticker, date_str = m.group(1), m.group(2)
            prev = latest.get(ticker)
            if prev is None or date_str > prev[0]:
                latest[ticker] = (date_str, path)
        for ticker, (_, path) in latest.items():
            ev = extract_dca_ev_5y(path)
            if ev is not None:
                out[ticker] = ev
    # v13 merged reports: 5Y EV comes from dd-meta ev5y_pct (v13 wins).
    for norm, fields in _v13_dca_overlay().items():
        if fields["ev5y"] is not None:
            out[norm] = fields["ev5y"]
    return out

META_RE = re.compile(
    r'<meta\s+name="dd-schema-version"\s+content="([^"]+)"', re.IGNORECASE
)

# === dd-meta JSON (v12.0+ canonical, plan-A "lasting fix") ====================
# DD HTML emits a <script id="dd-meta" type="application/json">{...}</script>
# block in <head> with structured fields. Script reads JSON when present;
# falls back to regex extractors below for legacy DDs without it.
DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)


def extract_dd_meta_json(text: str):
    """Return parsed dd-meta dict if present and valid JSON, else None."""
    m = DD_META_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError as e:
        print(f"  WARN: dd-meta JSON parse error: {e}")
        return None


def _norm_ticker(t: str) -> str:
    """Normalize ticker to the DCA-filename form (alnum, upper): 2330.TW→2330TW.
    Matches DCA_FILENAME_RE group keys and the consumer dot-stripped lookups."""
    return re.sub(r"[^A-Za-z0-9]", "", t or "").upper()


@lru_cache(maxsize=1)
def _v13_dca_overlay() -> dict:
    """Scan docs/dd/ for v13 merged reports and return the decision-layer fields
    that used to live in a separate DCA file, keyed by normalized ticker:

        {norm_ticker: {"ev5y": float|None, "moat_trend": str|None, "href": str}}

    v13 reports fold the DCA decision layer into the DD, so these come straight
    from dd-meta (no fragile §4 HTML regex). Latest v13 DD per ticker wins.
    The three collect_dca_* maps overlay this over their legacy /dca/ scan so a
    v13 report supersedes any stale DCA file. Empty until v13 DDs exist, so this
    is a no-op for the current all-v12 corpus. lru_cache: files are stable within
    a single sync run (separate processes get their own cache)."""
    if not DD_DIR.exists():
        return {}
    latest: dict[str, tuple[str, dict, str]] = {}  # norm -> (date, meta, fname)
    for path in DD_DIR.glob("DD_*.html"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        meta = extract_dd_meta_json(text)
        if not meta or not str(meta.get("schema", "")).startswith(("v13", "v14")):
            continue
        ticker = meta.get("ticker")
        if not ticker:
            continue
        norm = _norm_ticker(ticker)
        date = meta.get("date") or ""
        prev = latest.get(norm)
        if prev is None or date > prev[0]:
            latest[norm] = (date, meta, path.name)
    out: dict = {}
    for norm, (_, meta, fname) in latest.items():
        ev = meta.get("ev5y_pct")
        trend = meta.get("moat_trend")
        out[norm] = {
            "ev5y": ev if isinstance(ev, (int, float)) else None,
            "moat_trend": trend if trend in ("↑", "→", "↓") else None,
            "href": f"/dd/{fname}#decision",
        }
    return out


# === v12 extractors (regex fallback for DDs without dd-meta JSON) ===============
# Signal-light (A+/A/B/C/X) — universal anchor first ("綜合訊號：" prefix +
# any tag wrapping the letter), then fallback to class-based for newer
# layouts (INTC/RMBS) that don't use the 綜合訊號：prefix.
SIGNAL_INLINE_RE = re.compile(
    r'綜合訊號[^<]{0,40}<[^>]+>\s*([ABCSX][+]?)\s*[<｜|]'
)
SIGNAL_BOX_RE = re.compile(
    r'class="(?:grade|big|signal-huge|signal-letter|dashboard-signal|big-signal|signal-big|signal-x|signal-a|signal-b|signal-c)"'
    r'[^>]*>\s*([ABCSX][+]?)\s*[<｜|]?',
)
SIGNAL_LIGHT_RE = SIGNAL_INLINE_RE  # legacy alias, prefer extract_signal_light()

# FY+2 / NTM Forward P/E — try in order of specificity:
#   A) Newer v12 (INTC/RMBS): "當前 FY+2 Forward P/E</td><td...>$X / $Y = <strong>57x</strong>"
#   B) Older v12 (TXN/LRCX/VRT/GEV): "NTM Forward P/E 30.69x" narrative
#   C) Older v12 alt: "當前 NTM Fwd PE</td><td>30.69x</td>" table cell
FPE_FY2_STRONG_RE = re.compile(
    r'當前\s*FY\+2\s*Forward\s*P/E\s*</td>\s*<td[^>]*>[^<]{0,200}?'
    r'<strong>\s*(\d+(?:\.\d+)?)\s*x',
)
FPE_NTM_NARRATIVE_RE = re.compile(
    r'NTM\s*Forward\s*P/E\s*(?:[（(][^）)]*[）)])?\s*~?\s*(\d+(?:\.\d+)?)'
    # Allow optional range tail "-100x" or "～30x"; just match the first number.
    r'(?:\s*[\-－—~～]\s*\d+(?:\.\d+)?)?\s*x?',
    re.IGNORECASE,
)
FPE_NTM_TABLE_RE = re.compile(
    r'當前\s*NTM\s*Fwd\s*PE\s*(?:[（(][^）)]*[）)])?\s*</td>\s*<td[^>]*>\s*'
    r'(?:<[^>]*>\s*)?(\d+(?:\.\d+)?)\s*x',
    re.IGNORECASE,
)

# 5Y 分位 — multiple anchor variants:
#   A) "5Y 分位 89%" (older v12, clean)
#   B) "5Y 95+ 分位" / "5Y 歷史 95+ 分位" (newer v12, narrative)
#   C) "5Y ~95% 分位" (newer v12 alt)
PCT_5Y_TABLE_RE = re.compile(
    r'5Y\s*分位\s*~?\s*(\d+(?:\.\d+)?)\+?\s*%'
)
PCT_5Y_NARRATIVE_RE = re.compile(
    r'5Y(?:\s*[一-鿿]{0,4})?\s*~?\s*(\d+(?:\.\d+)?)\s*[%＋+]?\s*分位'
)

# PEG (FY+2) — pick first PEG value mentioned in §2 Dashboard (older) or §12 D (newer).
# We restrict to anchors near "估值燈" / "PEG" labels to avoid grabbing prose mentions.
PEG_RE_V12 = re.compile(
    r'PEG\s*(?:[（(]\s*(?:FY\+?[12]|3Y|2Y|Non-GAAP)[^）)]*[）)]\s*)?'
    r'(?:[<:：=]?\s*)?(\d+\.\d+)'
)

# Stress: "壓力測試通過率：0 / 4" or variants
STRESS_RE = re.compile(
    r'壓力測試\s*(?:通過率)?\s*[:：]?\s*(\d+)\s*/\s*(\d+)'
)

# Triax field in INDEX.md rr column for v12 entries: "A/🔴/✅", "S/🟢/✅", "C/🔴/-".
# Letters are S/A/B/C (護城河等級); emojis cover val + MA.
TRIAX_RE_V12 = re.compile(
    r'^\s*([SABCX]|拒絕)\s*/\s*([🟢🟡🟠🔴])\s*/\s*([✅🟡🟠❌🟢🔴]|-|—)\s*$'
)

# Mid-term (FY+2) upside, multiple layouts:
#   1) "上行空間  ...  -40.2%" (newer v12, §12 E table)
#   2) "中期 ... $277.20 − $267.78 = $9.42" (older v12, compute upside%)
#   3) Comment fallback: "+18% upside" or similar in INDEX.md last column
UPSIDE_PCT_RE = re.compile(r'上行空間.*?([+\-−]?\d+(?:\.\d+)?)\s*%', re.DOTALL)

# Long-term (5Y) upside — §2 E ③ 長期 R:R card: "<td>上行</td><td>+106%（5Y 累計）</td>"
# Also handles rr-long block containing "上行" row with a percentage.
UPSIDE_5Y_RE = re.compile(
    r'rr-long.*?<td>上行</td>\s*<td>\s*([+\-−]?\d+(?:\.\d+)?)\s*%',
    re.DOTALL,
)


def extract_signal_light(text: str) -> str:
    """Return one of A+/A/B/C/X, empty if not found.

    Tries universal "綜合訊號：<tag>X</tag>" anchor first, falls back to
    class-based pattern for newer DDs (INTC/RMBS) that wrap the letter
    in <div class="grade">X</div> without the 綜合訊號 prefix.
    """
    for pat in (SIGNAL_INLINE_RE, SIGNAL_BOX_RE):
        m = pat.search(text)
        if m:
            sig = m.group(1).strip()
            if sig in {"A+", "A", "B", "C", "X", "S"}:
                return sig
    return ""


def extract_fpe_fy2(text: str) -> str:
    """Return FY+2 (or NTM as fallback) Forward P/E like '45.1', empty if not found.

    Priority order:
      1) <strong>X.Yx</strong> in §12 C 當前 FY+2 Forward P/E table cell (newer v12)
      2) "NTM Forward P/E X.Yx" narrative form (older v12 §1 Dashboard)
      3) "當前 NTM Fwd PE</td><td>X.Yx" table cell form
    """
    for pat in (FPE_FY2_STRONG_RE, FPE_NTM_NARRATIVE_RE, FPE_NTM_TABLE_RE):
        m = pat.search(text)
        if m:
            return m.group(1)
    return ""


def extract_5y_pct(text: str) -> str:
    """Return 5Y 分位 percentile, e.g. '89' (no % sign), empty if not found.

    Priority order:
      1) "5Y 分位 89%" clean table form (older v12)
      2) "5Y [歷史] 95+ 分位" narrative form (newer v12, 0-4 CJK chars between)
    """
    m = PCT_5Y_TABLE_RE.search(text)
    if m:
        return m.group(1)
    m = PCT_5Y_NARRATIVE_RE.search(text)
    return m.group(1) if m else ""


def extract_peg_v12(text: str) -> str:
    """Return PEG value, e.g. '1.09'. Picks first PEG match within the first
    occurrence of 估值燈 + 1500 chars window so prose mentions don't hijack."""
    anchor = text.find("估值燈")
    if anchor < 0:
        anchor = 0
    window = text[anchor:anchor + 3000]
    m = PEG_RE_V12.search(window)
    if m:
        return m.group(1)
    # Last-ditch: any PEG value anywhere
    m = PEG_RE_V12.search(text)
    return m.group(1) if m else ""


def extract_stress_v12(text: str):
    """Return (passed, total) ints, or (0, 4) if not found."""
    m = STRESS_RE.search(text)
    if m:
        return int(m.group(1)), int(m.group(2))
    return 0, 4  # default for newer DDs that may not have QC-29 section


# === EPS CAGR (2Y) + 2Y PE — yfinance fetch + cache ==========================
# Single yfinance call per ticker yields:
#   - yearAgoEps (FY-1 actual, used as base for 2Y CAGR)
#   - FY+2 EPS estimate (avg consensus from t.earnings_estimate)
#   - currentPrice (used for 2Y PE = price / FY+2 EPS)
# Cache keeps these per-ticker so daily reruns of update_dd_index.py don't
# re-hit yfinance. Cache is auto-populated when a new ticker appears (e.g. after
# a fresh DD is added). Use --refresh-eps-cagr to force re-fetch all tickers.


def load_eps_cagr_cache() -> dict:
    if EPS_CAGR_CACHE.exists():
        try:
            return json.loads(EPS_CAGR_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_eps_cagr_cache(cache: dict) -> None:
    EPS_CAGR_CACHE.parent.mkdir(parents=True, exist_ok=True)
    EPS_CAGR_CACHE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def fetch_eps_metrics_yf(ticker: str) -> dict:
    """Fetch FY-1 EPS, FY+2 EPS estimate, current price for one ticker.

    Returns {
      'fy_minus_1_eps': float|None,
      'fy_2_eps': float|None,
      'current_price': float|None,
      'eps_cagr_2y_pct': float|None,
      'pe_2y': float|None,
      'fetched_at': iso8601 str,
      'status': 'ok' | 'no_estimate' | 'no_base' | 'error',
    }
    """
    out = {
        "fy_minus_1_eps": None,
        "fy_2_eps": None,
        "current_price": None,
        "eps_cagr_2y_pct": None,
        "pe_2y": None,
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "status": "error",
    }
    try:
        import yfinance as yf
    except ImportError:
        return out
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        out["current_price"] = float(price) if price else None
        # earnings_estimate has rows: 0q, +1q, 0y (=FY+1 = current year), +1y (=FY+2)
        ee = t.earnings_estimate
        if ee is None or ee.empty:
            out["status"] = "no_estimate"
            return out
        # FY+2 = +1y row, avg column
        if "+1y" in ee.index and "avg" in ee.columns:
            fy2 = ee.loc["+1y", "avg"]
            out["fy_2_eps"] = float(fy2) if fy2 == fy2 else None  # NaN check
        # Base = yearAgoEps of 0y row (= FY-1 actual, i.e. base year for FY+2 / base 2Y CAGR)
        if "0y" in ee.index and "yearAgoEps" in ee.columns:
            base = ee.loc["0y", "yearAgoEps"]
            out["fy_minus_1_eps"] = float(base) if base == base else None
    except Exception:
        return out

    fy2 = out["fy_2_eps"]
    base = out["fy_minus_1_eps"]
    price = out["current_price"]

    if not fy2 or fy2 <= 0:
        out["status"] = "no_estimate"
        return out

    # 2Y EPS CAGR = (FY+2 / base)^(1/2) − 1; needs positive base
    if base and base > 0:
        out["eps_cagr_2y_pct"] = ((fy2 / base) ** 0.5 - 1) * 100
    else:
        out["status"] = "no_base"

    # 2Y PE = current price / FY+2 EPS
    if price and price > 0:
        out["pe_2y"] = price / fy2

    if out["eps_cagr_2y_pct"] is not None and out["pe_2y"] is not None:
        out["status"] = "ok"
    return out


def get_eps_metrics(ticker: str, cache: dict, force_refresh: bool = False) -> dict:
    """Cache-first lookup. Returns {eps_cagr_2y_pct, pe_2y, status}.

    On cache miss (or force_refresh), hits yfinance and writes back to cache."""
    if not ticker:
        return {"eps_cagr_2y_pct": None, "pe_2y": None, "status": "missing"}
    if not force_refresh and ticker in cache:
        c = cache[ticker]
        return {
            "eps_cagr_2y_pct": c.get("eps_cagr_2y_pct"),
            "pe_2y": c.get("pe_2y"),
            "status": c.get("status", "cached"),
        }
    fetched = fetch_eps_metrics_yf(ticker)
    cache[ticker] = fetched
    return {
        "eps_cagr_2y_pct": fetched.get("eps_cagr_2y_pct"),
        "pe_2y": fetched.get("pe_2y"),
        "status": fetched.get("status", "error"),
    }


def extract_upside_fy2(text: str, index_comment: str = "") -> str:
    """Return FY+2 upside as numeric string, e.g. '-40.2' or '18.0'.
    Tries §12 E mid-term (上行空間), then INDEX.md comment fallback."""
    # Path 1: existing extract_upsides() logic — second 上行空間 hit is mid-term
    anchor = SECTION_E_ANCHOR_RE.search(text)
    if anchor:
        scope = text[anchor.start():anchor.start() + 8000]
        end_markers = ("</tr>", "下行距離", "下檔", "<h2", "<h3")
        upsides = []
        for mm in re.finditer(r"上行空間", scope):
            window = scope[mm.end():mm.end() + 400]
            cut = len(window)
            for marker in end_markers:
                idx = window.find(marker)
                if 0 < idx < cut:
                    cut = idx
            for pct in PCT_RE.findall(window[:cut]):
                upsides.append(pct.replace("−", "-"))
            if len(upsides) >= 2:
                break
        if len(upsides) >= 2:
            return upsides[1]
    # Path 2: parse INDEX.md comment for "+XX% upside" pattern (older v12 fallback)
    m = re.search(r'隱含\s*([+\-−]?\d+(?:\.\d+)?)\s*%\s*upside', index_comment)
    if m:
        return m.group(1).replace("−", "-")
    return ""


def parse_triax(rr_raw: str):
    """Parse v12 INDEX.md rr column 'A/🔴/✅' → ('A', '🔴', '✅')."""
    m = TRIAX_RE_V12.match(rr_raw.strip())
    if m:
        moat = m.group(1)
        if moat == "拒絕":
            moat = "X"
        return moat, m.group(2), m.group(3)
    return "", "", ""


# === end v12 extractors =======================================================


# Pattern to extract §2 G "一句話說明" (balanced conclusion, not bull-only)
# Matches <strong>一句話</strong>：text</p> or similar variants
ONELINER_RE = re.compile(
    r'一句話(?:</(?:strong|b)>)?\s*[：:]\s*(?:</(?:strong|b)>)?\s*(.*?)</p>',
    re.DOTALL,
)
# Fallback: extract from 裁決理由 table cell in §3
VERDICT_REASON_RE = re.compile(
    r'裁決理由\s*(?:</(?:strong|b|td)>)\s*</td>\s*<td[^>]*>(.*?)</td>',
    re.DOTALL,
)
TAG_RE = re.compile(r'<[^>]+>')

# Pattern to extract numeric quality score from §7.7 A / §2 B table
QUALITY_SCORE_RE = re.compile(
    r'綜合品質分\s*(?:</(?:strong|b)>)?\s*</td>'
    r'(?:\s*<td[^>]*>\s*</td>)*'
    r'\s*<td[^>]*>\s*(?:<(?:strong|b)[^>]*>)?\s*'
    r'([\d]+\.[\d]+)',
    re.DOTALL,
)

# Pattern to extract 護城河 score from §12 B table (v10: §9/§10 評分, v11: §7 評分)
# Accepts any section reference and decimal scores like "9.5".
MOAT_SCORE_RE = re.compile(
    r'護城河\s*</td>\s*<td[^>]*>\s*§\d+\b[^<]*</td>\s*<td[^>]*>\s*(?:<[^>]+>\s*)*(\d+(?:\.\d+)?)',
    re.DOTALL,
)

# Pattern to extract 護城河趨勢 row, then search for trend keyword inside
MOAT_TREND_ROW_RE = re.compile(
    r'護城河趨勢.*?</tr>',
    re.DOTALL,
)

# Pattern to extract 長期持有信心 (v10.0+): 高/中/低
# Matches table row with 長期持有信心 and extracts the value cell
CONFIDENCE_RE = re.compile(
    r'長期持有信心\s*(?:</(?:strong|b)>)?\s*</td>'
    r'(?:\s*<td[^>]*>.*?</td>)*?'  # skip intermediate cells (e.g. "綜合判斷")
    r'\s*<td[^>]*>\s*(?:<[^>]*>)*\s*(高|中|低)',
    re.DOTALL,
)

# Anchor to §12 雙時距目標價與 R:R section (where FY+1 / FY+2 上行空間 live)
# Accepts E|/D|/F| prefix variants (standard v11 uses E, some DDs use D or F).
# Requires the section-letter prefix so inline prose mentioning 雙時距 R:R doesn't match.
SECTION_E_ANCHOR_RE = re.compile(
    r'(?:雙\s*R:R\s*計算|[A-F]\s*[\|｜]\s*雙時距(?:目標價|\s*R:R))',
)
# Percentage value with optional sign (supports full-width minus −, U+2212)
PCT_RE = re.compile(r'([+\-−]?\d+(?:\.\d+)?)\s*%')


def extract_quality_score(path: Path) -> str:
    """Extract numeric quality score (e.g. '8.60') from DD HTML."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = QUALITY_SCORE_RE.search(text)
    return m.group(1) if m else ""


def extract_moat_score(path: Path) -> str:
    """Extract moat (護城河) score (e.g. '8') from §2 B / §9 in DD HTML."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = MOAT_SCORE_RE.search(text)
    return m.group(1) if m else ""


def extract_moat_trend(path: Path) -> str:
    """Extract moat trend (護城河趨勢) from §2 G or §9 table row."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = MOAT_TREND_ROW_RE.search(text)
    if not m:
        return ""
    row = TAG_RE.sub("", m.group(0))  # strip all HTML tags
    for kw in ("穩定至加深", "加深", "擴大", "穩定至縮減", "縮減", "穩定"):
        if kw in row:
            return kw
    return ""


def extract_version(path: Path) -> str:
    """Read <meta name="dd-schema-version" content="vX.Y"> from DD HTML head."""
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            head = fh.read(4096)
        m = META_RE.search(head)
        return m.group(1) if m else ""
    except OSError:
        return ""


def extract_comment(path: Path, max_len: int = 120) -> str:
    """Extract the bull one-liner from DD HTML as a short comment.

    v12.0 policy: 備註欄限 120 字（約 1-2 句話），超過以第一個 '。' 後截斷或加 '…'。
    CJK 字 120 個約等於視覺寬度 240 字元，適合表格單格 1.5 行顯示。
    歷史：500 (v11) → 180 (v12.0 initial) → 120 (v12.0 tighter)
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

    m = ONELINER_RE.search(text)
    if not m:
        m = VERDICT_REASON_RE.search(text)
    if not m:
        return ""

    raw = TAG_RE.sub("", m.group(1)).strip()
    if len(raw) > max_len:
        # 優先在句號切斷（保留完整句），fallback 硬截
        cut = raw[:max_len]
        last_period = max(cut.rfind("。"), cut.rfind("."))
        if last_period > max_len * 0.5:  # 若找到句號且位置不會太短
            raw = cut[:last_period + 1]
        else:
            raw = cut.rstrip("，。、；,.:;") + "…"
    return raw


def extract_confidence(path: Path) -> str:
    """Extract 長期持有信心 (高/中/低) from DD HTML. v10.0+ only."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = CONFIDENCE_RE.search(text)
    return m.group(1) if m else ""


def extract_upsides(path: Path):
    """Extract (FY+1, FY+2) 上行空間 from §12 E as numeric strings, e.g. '75.1' / '-32.5'.
    Handles three v11 layouts:
      - list-style per timeframe (NVDA/AMZN): two 上行空間 occurrences, one % each.
      - separate tables per timeframe (GOOGL/STX): two 上行空間 rows, one % each.
      - single table with 2 value cells (MSFT): one 上行空間 row, two % values.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return "", ""
    anchor = SECTION_E_ANCHOR_RE.search(text)
    if not anchor:
        return "", ""
    scope = text[anchor.start():anchor.start() + 8000]

    end_markers = ("</tr>", "下行距離", "下檔", "<h2", "<h3")
    upsides = []
    for mm in re.finditer(r"上行空間", scope):
        window = scope[mm.end():mm.end() + 400]
        cut = len(window)
        for marker in end_markers:
            idx = window.find(marker)
            if 0 < idx < cut:
                cut = idx
        for pct in PCT_RE.findall(window[:cut]):
            upsides.append(pct.replace("−", "-"))
        if len(upsides) >= 2:
            break

    fy1 = upsides[0] if len(upsides) >= 1 else ""
    fy2 = upsides[1] if len(upsides) >= 2 else ""
    return fy1, fy2


# Target-price patterns seen in v11 DDs (§12 E "雙時距目標價").
# Prefixes: $ (US/general) or TWD (台股)
_TARGET_NUM = r'([0-9][\d,]*(?:\.\d+)?)'
TARGET_PATTERNS = [
    # $ amount inside <strong> / <b> (with or without class)
    re.compile(rf'<(?:strong|b)[^>]*>\s*\$\s*{_TARGET_NUM}\s*</(?:strong|b)>'),
    # class="num|mono" wrapping a <strong>/<b>$amount</...> (STX / 2330.TW style)
    re.compile(rf'class="(?:num|mono)"[^>]*>\s*<(?:strong|b)[^>]*>\s*\$\s*{_TARGET_NUM}\s*</(?:strong|b)>'),
    # class="num|mono" span with $amount directly
    re.compile(rf'<span[^>]*class="(?:num|mono)"[^>]*>\s*\$\s*{_TARGET_NUM}\s*</span>'),
    # TWD amounts in <strong>/<b>
    re.compile(rf'<(?:strong|b)[^>]*>\s*TWD\s*{_TARGET_NUM}\s*</(?:strong|b)>'),
    # TWD inside class="mono|num" wrapper
    re.compile(rf'class="(?:num|mono)"[^>]*>\s*<(?:strong|b)[^>]*>\s*TWD\s*{_TARGET_NUM}\s*</(?:strong|b)>'),
]


def extract_targets(path: Path):
    """Extract (short_target, mid_target, currency) from §12 E.
    Returns (None, None, '') if not found."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None, None, ""
    anchor = SECTION_E_ANCHOR_RE.search(text)
    if not anchor:
        return None, None, ""
    scope = text[anchor.start():anchor.start() + 8000]
    s_m = re.search(r'短期(?:\s*[（(][1１一][^）)]*[）)])?', scope)
    if not s_m:
        return None, None, ""
    m_m = re.search(r'中期(?:\s*[（(][2２二][^）)]*[）)])?', scope[s_m.end():])
    if not m_m:
        return None, None, ""
    mid_start_abs = s_m.end() + m_m.start()
    short_win = scope[s_m.start():mid_start_abs]
    after = scope[mid_start_abs:mid_start_abs + 2000]
    cut = len(after)
    for marker in ("Bear", "下檔", "W52", "項目"):
        idx = after.find(marker)
        if 0 < idx < cut:
            cut = idx
    mid_win = after[:cut]

    def _find(win):
        for pat in TARGET_PATTERNS:
            hit = pat.search(win)
            if hit:
                val = float(hit.group(1).replace(",", ""))
                cur = "TWD" if "TWD" in hit.group(0) else "USD"
                return val, cur
        return None, ""

    s_val, s_cur = _find(short_win)
    m_val, m_cur = _find(mid_win)
    currency = s_cur or m_cur
    return s_val, m_val, currency


def normalize_ticker(raw: str) -> str:
    """Convert row ticker (e.g. '2308TW', '2383TW_v10') to yfinance form ('2308.TW')."""
    t = raw.strip()
    # Strip _v10/_v11 suffixes
    t = re.sub(r'_v\d+$', '', t)
    # TW stock: 4-digit + TW → 4-digit.TW
    m = re.match(r'^(\d{4,5})TW$', t)
    if m:
        return f"{m.group(1)}.TW"
    # Already has dot suffix
    if re.match(r'^\d{4,5}\.TW$', t):
        return t
    return t


def load_price_cache() -> dict:
    if PRICE_CACHE.exists():
        try:
            return json.loads(PRICE_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_price_cache(data: dict) -> None:
    PRICE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    PRICE_CACHE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_prices(tickers: list) -> dict:
    """Fetch current close price for each yfinance-normalized ticker.
    Returns {ticker: price}. Missing / failed tickers are omitted."""
    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run: pip install yfinance")
        return {}
    result = {}
    if not tickers:
        return result
    print(f"Fetching prices for {len(tickers)} tickers via yfinance...")
    try:
        data = yf.download(
            tickers, period="5d", interval="1d", progress=False, group_by="ticker", auto_adjust=False
        )
    except Exception as e:
        print(f"yfinance batch fetch failed: {e}")
        return result
    for t in tickers:
        try:
            if len(tickers) == 1:
                closes = data["Close"].dropna()
            else:
                closes = data[t]["Close"].dropna()
            if len(closes) == 0:
                continue
            result[t] = float(closes.iloc[-1])
        except (KeyError, IndexError, AttributeError):
            continue
    print(f"Got {len(result)}/{len(tickers)} prices.")
    return result


def parse_index_md() -> dict:
    """Parse INDEX.md and return a dict keyed by filename with metadata."""
    data = {}
    if not INDEX_MD.exists():
        return data
    for line in INDEX_MD.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if not any(f"v{n}" in line for n in range(9, 20)):
            continue
        cols = [c.strip() for c in line.split("|")]
        # cols: ['', date, ticker, schema, verdict, trap, rr, filename, '']
        if len(cols) < 9:
            continue
        date, ticker, schema, verdict, trap, rr, filename = cols[1:8]
        if not any(schema.startswith(f"v{n}") for n in range(9, 20)):
            continue
        # col[8:] is the 備註 column; rejoin if it contains pipe chars
        comment_raw = "|".join(cols[8:-1]).strip() if len(cols) > 9 else (cols[8].strip() if len(cols) > 8 else "")
        data[filename] = {
            "date": date,
            "ticker": ticker,
            "schema": schema,
            "verdict": verdict,
            "trap": trap,
            "rr_raw": rr,
            "filename": filename,
            "comment": comment_raw,
        }
        # Parse R:R field for quality level
        rr_parts = [p.strip() for p in rr.split("/")]
        if len(rr_parts) >= 1:
            data[filename]["quality"] = rr_parts[0]
    return data


def scan_files(index_data: dict):
    """Build entries list for v9.x/v10.x DDs, enriched with INDEX.md metadata."""
    entries = []
    for f in sorted(DD_DIR.glob("DD_*.html")):
        version = extract_version(f)
        # Only show v11+ on the website
        try:
            major = int(version.lstrip("v").split(".")[0])
        except (ValueError, IndexError):
            continue
        if major < 11:
            continue
        m = re.match(r"DD_(.+?)_(\d{4})(\d{2})(\d{2})(?:_v\d+)?\.html", f.name)
        if not m:
            m = re.match(r"DD_(.+?)_v\d+_(\d{4})(\d{2})(\d{2})\.html", f.name)
        if not m:
            continue
        ticker = m.group(1)
        date_str = f"{m.group(2)}-{m.group(3)}-{m.group(4)}"

        md = index_data.get(f.name, {})
        comment = extract_comment(f) or md.get("comment", "")
        # v12.0 policy: 無論來源為何（DD HTML §2 I 或 INDEX.md fallback），
        # 備註統一套用 120 字上限 + 句號切斷邏輯。
        # 原先 fallback 到 INDEX.md 的 8-bullet Dashboard 會漏掉截斷（例如 UBER v12）。
        if comment:
            # 先移除 <br> / <br/> 等換行 tag，替換為「；」保留語意分隔
            comment_flat = re.sub(r'<br\s*/?>', '；', comment)
            comment_flat = re.sub(r'<[^>]+>', '', comment_flat).strip()
            if len(comment_flat) > 120:
                cut = comment_flat[:120]
                last_period = max(cut.rfind("。"), cut.rfind("."), cut.rfind("；"))
                if last_period > 60:
                    comment = cut[:last_period + 1]
                else:
                    comment = cut.rstrip("，。、；,.:;") + "…"
            else:
                comment = comment_flat
        qscore = extract_quality_score(f)
        moat = extract_moat_score(f)
        moat_trend = extract_moat_trend(f)
        confidence = extract_confidence(f)
        upside1, upside2 = extract_upsides(f)
        t1, t2, currency = extract_targets(f)
        entries.append({
            "ticker": ticker,
            "ticker_yf": normalize_ticker(ticker),
            "target1": t1,
            "target2": t2,
            "currency": currency,
            "date": date_str,
            "version": version,
            "href": f"/dd/{f.name}",
            "verdict": md.get("verdict", "—"),
            "trap": md.get("trap", "—"),
            "quality": md.get("quality", "—"),
            "quality_score": qscore,
            "moat_score": moat,
            "moat_trend": moat_trend,
            "confidence": confidence,
            "upside1": upside1,
            "upside2": upside2,
            "comment": comment,
        })

    entries.sort(key=lambda e: e["ticker"])
    entries.sort(key=lambda e: e["version"], reverse=True)
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries


def verdict_badge(v: str) -> str:
    v = v.strip()
    if v == "進場":
        return '<span class="verdict-badge verdict-buy">進場</span>'
    elif v == "觀望偏進場":
        return '<span class="verdict-badge verdict-lean-buy">觀望偏進場</span>'
    elif v == "觀望":
        return '<span class="verdict-badge verdict-watch">觀望</span>'
    elif v == "迴避":
        return '<span class="verdict-badge verdict-avoid">迴避</span>'
    return v


def quality_badge(q: str, score: str = "", moat: str = "", moat_trend: str = "") -> str:
    trend_str = f"·{moat_trend}" if moat_trend else ""
    if moat:
        return f'<span class="quality-score">{moat}/10{trend_str}</span>'
    return "—"


def upside_badge(v: str) -> str:
    """Render upside as +/- percent with color styling."""
    if not v:
        return "—"
    try:
        f = float(v)
    except ValueError:
        return "—"
    sign = "+" if f > 0 else ""  # negative number already carries '-'
    if f > 0:
        cls = "upside-pos"
    elif f < 0:
        cls = "upside-neg"
    else:
        cls = "upside-zero"
    return f'<span class="{cls}">{sign}{f:.1f}%</span>'


def confidence_badge(c: str) -> str:
    c = c.strip()
    if c == "高":
        return '<span class="conf-high">高</span>'
    elif c == "中":
        return '<span class="conf-mid">中</span>'
    elif c == "低":
        return '<span class="conf-low">低</span>'
    return '<span class="conf-na">—</span>'


def trap_short(t: str) -> str:
    t = t.strip()
    if "非陷阱" in t:
        return '<span class="trap-ok">非陷阱</span>'
    elif "觀察期" in t:
        return '<span class="trap-watch">觀察期</span>'
    elif "高風險" in t:
        return '<span class="trap-danger">高風險</span>'
    return t


def version_badge(v: str) -> str:
    v = v.strip()
    if v.startswith("v11"):
        return f'<span class="version-badge version-latest">{v}</span>'
    return f'<span class="version-badge">{v}</span>'


def _sort_keys(e):
    qs = e.get("quality_score", "")
    try:
        q_sort = -float(qs)
    except (ValueError, TypeError):
        q_map_fallback = {"H": 1, "MH": 2, "M": 3, "W": 4, "A": 0, "B": 2}
        q_sort = q_map_fallback.get(e.get("quality", "").strip(), 9)
    v_map = {"進場": 1, "觀望偏進場": 2, "觀望": 3, "迴避": 4}
    trap = e.get("trap", "")
    if "非陷阱" in trap:
        t_val = 1
    elif "觀察期" in trap:
        t_val = 2
    else:
        t_val = 3
    conf_map = {"高": 1, "中": 2, "低": 3}
    conf_val = conf_map.get(e.get("confidence", "").strip(), 9)
    return {
        "quality": q_sort,
        "verdict": v_map.get(e.get("verdict", "").strip(), 9),
        "trap": t_val,
        "confidence": conf_val,
    }


def build_rows(entries):
    rows = []
    for e in entries:
        sk = _sort_keys(e)
        try:
            up1_val = float(e.get("upside1", "") or 0)
        except ValueError:
            up1_val = 0.0
        try:
            up2_val = float(e.get("upside2", "") or 0)
        except ValueError:
            up2_val = 0.0
        rows.append(
            f'<tr class="searchable"'
            f' data-ticker="{e["ticker"]}"'
            f' data-date="{e["date"]}"'
            f' data-version="{e.get("version", "")}"'
            f' data-verdict="{sk["verdict"]}"'
            f' data-quality="{sk["quality"]}"'
            f' data-moat="{e.get("moat_score", "") or 0}"'
            f' data-upside1="{up1_val}"'
            f' data-upside2="{up2_val}"'
            f' data-trap="{sk["trap"]}"'
            f' data-confidence="{sk["confidence"]}"'
            f'>\n'
            f'  <td><a href="{e["href"]}" class="ticker-link" target="_blank" rel="noopener">{e["ticker"]}</a></td>\n'
            f'  <td class="date-cell">{e["date"]}</td>\n'
            f'  <td>{verdict_badge(e["verdict"])}</td>\n'
            f'  <td>{quality_badge(e["quality"], e.get("quality_score", ""), e.get("moat_score", ""), e.get("moat_trend", ""))}</td>\n'
            f'  <td>{upside_badge(e.get("upside1", ""))}</td>\n'
            f'  <td>{upside_badge(e.get("upside2", ""))}</td>\n'
            f'  <td>{trap_short(e["trap"])}</td>\n'
            f'  <td>{confidence_badge(e.get("confidence", ""))}</td>\n'
            f'  <td class="comment-cell">{e["comment"]}</td>\n'
            f'</tr>'
        )
    return "\n".join(rows)


# === v12 row builder (additive append-only mode) =============================

# Maps for v12 cell rendering
_SIGNAL_RANK = {"A+": 5, "A": 4, "B": 3, "C": 2, "X": 1, "S": 5}
_TRAP_RANK = {"🟢": 3, "🟡": 2, "🔴": 1}
_MOAT_QUALITY = {"S": 4, "A": 3, "B": 2, "C": 1, "X": 0}
_VERDICT_CSS = {
    "A+": "verdict-ok",
    "A": "verdict-ok",
    "B": "verdict-watch-buy",
    "C": "verdict-hold",
    "X": "verdict-avoid",
    "S": "verdict-ok",
}
_TRAP_CSS = {"🟢": ("trap-ok", "🟢 非陷阱"), "🟡": ("trap-watch", "🟡 觀察期"), "🔴": ("trap-danger", "🔴 高風險")}


def _verdict_to_signal(verdict_raw: str) -> str:
    """Map INDEX.md verdict column → v12 signal letter (fallback when DD HTML
    extraction fails). Heuristic — treat first letter / keyword as signal."""
    v = verdict_raw.strip()
    if not v:
        return ""
    # Direct letter — covers "B", "A+", "C" etc.
    head = v[:2] if v[:2] == "A+" else v[:1]
    if head in {"A+", "A", "B", "C", "X", "S"}:
        return head
    # Keyword mapping for full Chinese verdict
    if "強進場" in v: return "A+"
    if "拒絕" in v or "迴避" in v: return "C"
    if "MA煞車" in v or "追蹤池" in v: return "C"
    if "進場" in v: return "A"
    if "試倉" in v: return "B"
    return ""


def extract_munger_threshold(dd_text: str) -> "tuple[str | None, int | None, int | None]":
    """Extract Munger §7 evaluation from a DD HTML file.

    Returns (emoji, pass_count, total_count):
      emoji:       🟢/🟡/🔴 from 'Munger 三維評級' paragraph (or None).
      pass_count:  count of rows classified as PASS in the gate table,
                   or None if section not found / parse failed.
      total_count: actual number of evaluated rows in the table (any count
                   in range 5-15 accepted; old-schema DDs may have 7-10 rows),
                   or None if section not found / parse failed.

    Gate table location patterns (priority order):
      1. <h3>/<h4> named '門檻檢核表'
      2. <h3>/<h4> named 'Munger 護城河維度...' (AMD/RCL style)
      3. <h3>/<h4> named 'Munger 三維護城河...' (ETN style)
      4. <div class='section-title'> containing §7 (2330TW style)

    Pass/partial/fail detection:
      PASS    = ✅ / ✓✓ / single ✓ / class=pass/beat / badge-beat / 是(standalone)
      PARTIAL = 部分 / 接近 / 邊緣 / ⚠️ / 🟡 / warn-cell (not counted in pass)
      FAIL    = ❌ / 否 / 高 / 低 / 擴張中 / class=fail
    Special row '護城河強度': cell may be numeric → ≥8 pass / 6-7 partial / <6 fail.
    """
    td_pat_check = re.compile(r"<td[^>]*>.*?</td>", re.DOTALL | re.IGNORECASE)
    tr_pat_check = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)

    h_patterns = [
        re.compile(r"<h[34][^>]*>門檻檢核表[^<]*</h[34]>", re.IGNORECASE),  # broader: allows suffix like （含 Munger 維度）— covers 3017.TW
        re.compile(r"<h[34][^>]*>Munger\s+護城河維度[^<]*</h[34]>", re.IGNORECASE),
        re.compile(r"<h[34][^>]*>Munger\s+三維護城河[^<]*</h[34]>", re.IGNORECASE),
        # single-line div.section-title that mentions §7 (no DOTALL to avoid greedy span)
        re.compile(r"<div[^>]*section-title[^>]*>[^<]*§7[^<]*</div>", re.IGNORECASE),
        # h2-level §7 section headers — covers APP, KEYS, 6146T, 6857T, BESI, CAMT, DELL etc.
        re.compile(r"<h2[^>]*>[^<]*§7[^<]*(?:門檻|核心門檻)[^<]*</h2>", re.IGNORECASE),
    ]

    gate_start: "int | None" = None
    gate_section: "str | None" = None

    for pat in h_patterns:
        m = pat.search(dd_text)
        if not m:
            continue
        table_end = dd_text.find("</table>", m.end())
        if table_end == -1:
            continue
        candidate = dd_text[m.start(): table_end + 8]
        has_3col = any(
            len(list(td_pat_check.finditer(tr.group(1)))) >= 3
            for tr in tr_pat_check.finditer(candidate)
        )
        if has_3col:
            gate_start = m.start()
            gate_section = candidate
            break

    if gate_start is None or gate_section is None:
        return (None, None, None)

    # Munger三維評級 emoji — DOTALL search within 5000 chars of header
    munger_emoji: "str | None" = None
    em = re.search(r"Munger\s+三維評級.*?([🟢🟡🔴])", dd_text[gate_start: gate_start + 5000], re.DOTALL)
    if em:
        munger_emoji = em.group(1)

    # Parse gate table rows
    tr_pat = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
    td_pat = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
    tag_pat = re.compile(r"<[^>]+>", re.DOTALL)

    pass_c = fail_c = partial_c = 0

    for tr in tr_pat.finditer(gate_section):
        tds = list(td_pat.finditer(tr.group(1)))
        if len(tds) < 3:
            continue
        raw3 = tds[2].group(1)
        cell_text = tag_pat.sub("", raw3).strip()
        cell_html = raw3
        label = tag_pat.sub("", tds[0].group(1)).strip()

        # Special row: 護城河強度 — cell may be numeric score
        if any(k in label for k in ("護城河強度", "護城河強")):
            nums = re.findall(r"\d+", cell_text)
            if nums:
                val = int(nums[0])
                if val >= 8:
                    pass_c += 1
                elif val >= 6:
                    partial_c += 1
                else:
                    fail_c += 1
            elif re.search(r"[✅✓]", cell_text):
                pass_c += 1
            elif "⚠️" in cell_text:
                partial_c += 1
            else:
                fail_c += 1
            continue

        is_partial = (
            "部分" in cell_text or "接近" in cell_text or "邊緣" in cell_text
            or "warn-cell" in cell_html or "🟡" in cell_text or "⚠️" in cell_text
        )
        is_pass = (
            "✅" in cell_text or "✓✓" in cell_text
            or 'class="pass"' in cell_html or 'class="beat"' in cell_html
            or "badge-beat" in cell_html
        )
        if not is_pass and not is_partial and re.search(r"✓", cell_text):
            is_pass = True
        if not is_pass and not is_partial and cell_text == "是":
            is_pass = True
        is_fail = (
            "❌" in cell_text or cell_text in ("否", "高", "低", "擴張中")
            or bool(re.match(r"^否", cell_text))
            or 'class="fail"' in cell_html
        )

        if is_partial:
            partial_c += 1
        elif is_pass:
            pass_c += 1
        elif is_fail:
            fail_c += 1
        else:
            fail_c += 1

    total = pass_c + partial_c + fail_c
    # Accept any table with 5-15 rows; reject pathological counts (0 or 30+).
    if total < 5 or total > 15:
        return (munger_emoji, None, None)
    return (munger_emoji, pass_c, total)


def _render_moat_trend_cell(arrow: "str | None") -> "tuple[str, str]":
    """(td_html, num_attr) for the DCA moat trend column.

    arrow: '↑' (widening) / '→' (holding) / '↓' (narrowing) / None.
    Color scheme:
      ↑ → #166534 green   (護城河正在擴大)
      → → #64748B gray    (持平)
      ↓ → #991B1B red     (護城河正在縮窄，silent thesis decay 警示)
      None → #CBD5E1 gray (無 DCA)
    num_attr for sorting (desc = widening first): ↑=3, →=2, ↓=1, None=0.
    """
    if arrow == "↑":
        color, num_attr = "#166534", "3"
    elif arrow == "→":
        color, num_attr = "#64748B", "2"
    elif arrow == "↓":
        color, num_attr = "#991B1B", "1"
    else:
        return '<td class="num-cell" style="color:#CBD5E1;text-align:center">—</td>', "0"
    td = (
        f'<td class="num-cell" style="color:{color};font-size:18px;'
        f'font-weight:700;text-align:center">{arrow}</td>'
    )
    return td, num_attr


def build_row_v12(entry: dict, dca_map: dict | None = None,
                   dca_ev_map: dict | None = None,
                   dca_moat_trend_map: dict | None = None) -> str:
    """Render one v12 row (data-* attrs + td cells) matching the hand-curated
    schema in docs/research/index.html. Missing fields render as '?' or 0.

    dca_map: optional {ticker: dca_href} from collect_dca_map(). When provided
    and ticker has a DCA report, inject a 📋 link cell after Ticker; else '—'.
    dca_ev_map: optional {ticker: ev_5y_pct} from collect_dca_ev_map(). When
    provided, the next cell after 定見 shows the parsed §4 5Y probability-
    weighted expected value; else '—'.
    dca_moat_trend_map: optional {ticker: arrow} from collect_dca_moat_trend_map().
    When provided, inject a moat trend arrow cell (↑/→/↓) after the IRR cell.
    """
    sig = entry.get("signal", "") or "?"
    trap_emoji = entry.get("trap_emoji", "") or "?"
    moat = entry.get("moat", "") or "?"
    val_emoji = entry.get("val_emoji", "") or "?"
    ma_state = entry.get("ma_state", "") or "?"
    fpe = entry.get("fpe", "")
    peg = entry.get("peg", "")
    eps_cagr = entry.get("eps_cagr_2y_value")
    pe_2y = entry.get("pe_2y_value")
    munger_emoji = entry.get("munger_emoji")
    munger_pass = entry.get("munger_pass")
    munger_total = entry.get("munger_total") or 11

    # Numeric data attrs (for sorting); fallback to 0 when empty.
    rank = _SIGNAL_RANK.get(sig, 0)
    trap_rank = _TRAP_RANK.get(trap_emoji, 0)
    quality = _MOAT_QUALITY.get(moat, 0)
    try:
        fpe_num = float(fpe) if fpe else 0.0
    except ValueError:
        fpe_num = 0.0
    try:
        peg_num = float(peg) if peg else 0.0
    except ValueError:
        peg_num = 0.0
    # CSS classes
    verdict_cls = _VERDICT_CSS.get(sig, "verdict-hold")
    trap_cls, trap_label = _TRAP_CSS.get(trap_emoji, ("trap-watch", trap_emoji))

    # Cell display values
    fpe_disp = f"{fpe}x" if fpe else "?"
    peg_disp = f"{peg}" if peg else "?"

    # EPS CAGR (2Y) cell — yfinance live consensus (FY+2 vs FY-1 actual).
    if eps_cagr is None:
        eps_cell = '<td class="num-cell" style="color:#94A3B8">—</td>'
        eps_num_attr = "0"
    else:
        if eps_cagr >= 20:
            eps_color = "#166534"     # deep green
        elif eps_cagr >= 10:
            eps_color = "#15803D"     # green
        elif eps_cagr >= 0:
            eps_color = "#92400E"     # amber
        else:
            eps_color = "#991B1B"     # red
        eps_sign = "+" if eps_cagr > 0 else ""
        eps_cell_text = f"{eps_sign}{eps_cagr:.1f}%"
        eps_cell = f'<td class="num-cell" style="color:{eps_color};font-weight:600">{eps_cell_text}</td>'
        eps_num_attr = f"{eps_cagr:.1f}"

    # 2Y PE cell — yfinance live (current price / FY+2 EPS estimate).
    if pe_2y is None:
        pe2y_cell = '<td class="num-cell" style="color:#94A3B8">—</td>'
        pe2y_num_attr = "0"
    else:
        # Color heuristic mirrors Fwd PE bands (low = green, high = red)
        if pe_2y < 15:
            pe2y_color = "#166534"
        elif pe_2y < 25:
            pe2y_color = "#15803D"
        elif pe_2y < 40:
            pe2y_color = "#92400E"
        else:
            pe2y_color = "#991B1B"
        pe2y_cell = f'<td class="num-cell" style="color:{pe2y_color};font-weight:600">{pe_2y:.1f}x</td>'
        pe2y_num_attr = f"{pe_2y:.1f}"

    # Date: compact MM-DD display with ISO tooltip; data-date keeps full ISO for sort.
    date_iso = entry.get("date") or ""
    if date_iso and len(date_iso) == 10:
        date_compact = date_iso[5:]   # MM-DD
        date_cell = f'<td class="num-cell"><span title="{date_iso}">{date_compact}</span></td>'
    else:
        date_cell = f'<td class="num-cell">{date_iso or "—"}</td>'

    # Normalize ticker for DCA lookup: DD entries use "2330.TW" with dot,
    # DCA filenames strip non-alphanumeric ("2330TW"). Try both forms.
    _dm = dca_map or {}
    _t_raw = entry["ticker"]
    _t_norm = re.sub(r"[^A-Za-z0-9]", "", _t_raw).upper()
    dca_href = _dm.get(_t_raw) or _dm.get(_t_norm)
    if dca_href:
        dca_cell = (
            f'<td class="num-cell"><a href="{dca_href}" target="_blank" '
            f'rel="noopener" title="Deep Conviction Analysis 投資決策報告" '
            f'style="text-decoration:none">📋</a></td>'
        )
    else:
        dca_cell = '<td class="num-cell" style="color:#CBD5E1">—</td>'

    # 5Y 機率加權期望 IRR（§4 Asymmetry）— color band: <8% weak / 8-12% mid /
    # >12% strong (matches SKILL.md IRR 落點解讀). data-ev5y stores IRR so the
    # column sorts by user-visible value.
    _ev = (dca_ev_map or {}).get(_t_raw)
    if _ev is None:
        _ev = (dca_ev_map or {}).get(_t_norm)
    if _ev is None:
        ev_cell = '<td class="num-cell" style="color:#CBD5E1">—</td>'
        ev_num_attr = "0"
    else:
        _irr = compute_dca_irr(_ev)
        if _irr >= 12:
            ev_color = "#166534"  # strong
        elif _irr >= 8:
            ev_color = "#15803D"  # mid (beats SPX baseline)
        elif _irr >= 0:
            ev_color = "#92400E"  # weak (positive but below SPX)
        else:
            ev_color = "#991B1B"  # negative IRR
        ev_sign = "+" if _irr > 0 else ("−" if _irr < 0 else "")
        ev_text = f"{ev_sign}{abs(_irr):.1f}%/yr"
        ev_cell = f'<td class="num-cell" style="color:{ev_color};font-weight:600">{ev_text}</td>'
        ev_num_attr = f"{_irr:.2f}"

    # Moat trend arrow — DCA Phase A1 authoritative output.
    _mt_arrow = (dca_moat_trend_map or {}).get(_t_raw)
    if _mt_arrow is None:
        _mt_arrow = (dca_moat_trend_map or {}).get(_t_norm)
    _mt_num = {"↑": "3", "→": "2", "↓": "1"}.get(_mt_arrow or "", "0")

    # Four-axis cell: {moat}{arrow}/{val}/{ma}  e.g. "S↑/🟢/✅"
    # Arrow is embedded inline with color span (tight to the moat letter, no space).
    if _mt_arrow == "↑":
        arrow_span = '<span style="color:#166534">↑</span>'
    elif _mt_arrow == "→":
        arrow_span = '<span style="color:#64748B">→</span>'
    elif _mt_arrow == "↓":
        arrow_span = '<span style="color:#991B1B">↓</span>'
    else:
        arrow_span = ""
    four_axis_html = f'{moat}{arrow_span}/{val_emoji}/{ma_state}'
    four_axis_cell = f'<td class="num-cell">{four_axis_html}</td>'

    # §7 門檻 cell: {emoji} {pass}/{total}, colour-coded background by pass %.
    # Thresholds are percentage-based so old-schema DDs (≠ 11 rows) render correctly:
    #   pct ≥ 0.73 (≈ 8/11 baseline) → green
    #   pct ≥ 0.55 (≈ 6/11 baseline) → yellow
    #   else → red
    if munger_pass is not None:
        _gate_total = munger_total if munger_total else 11
        pct = munger_pass / _gate_total if _gate_total > 0 else 0.0
        if pct >= 0.73:
            eff_emoji = "🟢"
            gate_bg = "background:#DCFCE7;color:#166534"
        elif pct >= 0.55:
            eff_emoji = "🟡"
            gate_bg = "background:#FEF9C3;color:#854D0E"
        else:
            eff_emoji = "🔴"
            gate_bg = "background:#FEE2E2;color:#991B1B"
        gate_cell = (
            f'<td class="num-cell" style="{gate_bg};font-weight:600;border-radius:4px">'
            f'{eff_emoji} {munger_pass}/{_gate_total}</td>'
        )
    else:
        gate_cell = '<td class="num-cell" style="color:#94A3B8">—</td>'

    _munger_gate_num = str(munger_pass) if munger_pass is not None else "0"
    return (
        f'<tr class="searchable" data-ticker="{entry["ticker"]}" data-date="{date_iso}"'
        f' data-signal="{sig}" data-trap="{trap_emoji}"'
        f' data-rank="{rank}" data-trap-rank="{trap_rank}" data-quality="{quality}"'
        f' data-fpe="{fpe_num}" data-pe2y="{pe2y_num_attr}" data-peg="{peg_num}"'
        f' data-eps-cagr="{eps_num_attr}"'
        f' data-upside="{entry.get("upside", 0) or 0}" data-upside5y="{entry.get("upside_5y", 0) or 0}"'
        f' data-ev5y="{ev_num_attr}"'
        f' data-moat-trend="{_mt_num}" data-munger-gate="{_munger_gate_num}">\n'
        f'  <td><a href="{entry["href"]}" class="ticker-link" target="_blank" rel="noopener">{entry["ticker"]}</a></td>'
        f'{date_cell}'
        f'{dca_cell}'
        f'{ev_cell}'
        f'<td><span class="{verdict_cls}"><strong>{sig}</strong></span></td>'
        f'<td><span class="{trap_cls}">{trap_label}</span></td>'
        f'{four_axis_cell}'
        f'{gate_cell}'
        f'<td class="num-cell">{fpe_disp}</td>'
        f'{pe2y_cell}'
        f'<td class="num-cell">{peg_disp}</td>'
        f'{eps_cell}\n'
        f'</tr>'
    )


def build_row_dca_only(ticker: str, dca_href: str, dca_date: str,
                        ev_5y: float | None,
                        moat_trend_arrow: "str | None" = None) -> str:
    """Render a row for a ticker that has a DCA report but NO DD coverage.

    DD-derived columns render '—'. The ticker link points to the DCA file
    (since there is no DD). data-rank=0 keeps these rows sorted to the
    bottom in the default signal-desc view.

    Column order (12 cols, matches build_row_v12 new schema):
      1 Ticker  2 DD日期  3 定見  4 5Y IRR
      5-12: signal trap 四軸 §7門檻 fpe pe2y peg eps-cagr (8 em-dashes)
    """
    if ev_5y is None:
        ev_cell = '<td class="num-cell" style="color:#CBD5E1">—</td>'
        ev_num_attr = "0"
    else:
        irr = compute_dca_irr(ev_5y)
        if irr >= 12:
            ev_color = "#166534"
        elif irr >= 8:
            ev_color = "#15803D"
        elif irr >= 0:
            ev_color = "#92400E"
        else:
            ev_color = "#991B1B"
        sign = "+" if irr > 0 else ("−" if irr < 0 else "")
        ev_text = f"{sign}{abs(irr):.1f}%/yr"
        ev_cell = (
            f'<td class="num-cell" style="color:{ev_color};font-weight:600">'
            f'{ev_text}</td>'
        )
        ev_num_attr = f"{irr:.2f}"

    _mt_num = {"↑": "3", "→": "2", "↓": "1"}.get(moat_trend_arrow or "", "0")

    # Compact date display (MM-DD with ISO tooltip)
    if dca_date and len(dca_date) == 10:
        date_compact = dca_date[5:]
        date_cell = f'<td class="num-cell"><span title="{dca_date}">{date_compact}</span></td>'
    else:
        date_cell = f'<td class="num-cell">{dca_date or "—"}</td>'

    em = '<td class="num-cell" style="color:#CBD5E1">—</td>'
    return (
        f'<tr class="searchable" data-ticker="{ticker}" data-date="{dca_date}"'
        f' data-signal="" data-trap=""'
        f' data-rank="0" data-trap-rank="0" data-quality="0"'
        f' data-fpe="0" data-pe2y="0" data-peg="0"'
        f' data-eps-cagr="0"'
        f' data-upside="0" data-upside5y="0" data-ev5y="{ev_num_attr}"'
        f' data-moat-trend="{_mt_num}" data-munger-gate="0">\n'
        f'  <td><a href="{dca_href}" class="ticker-link" target="_blank" '
        f'rel="noopener" title="僅 DCA 報告，無對應 DD（DD 已輪替/未建檔）">'
        f'{ticker}</a></td>'
        f'{date_cell}'
        f'<td class="num-cell"><a href="{dca_href}" target="_blank" '
        f'rel="noopener" title="Deep Conviction Analysis 投資決策報告" '
        f'style="text-decoration:none">📋</a></td>'
        f'{ev_cell}'
        # 8 em-dashes: signal, trap, 四軸, §7門檻, fpe, pe2y, peg, eps-cagr
        f'{em}{em}{em}{em}{em}{em}{em}{em}\n'
        f'</tr>'
    )


def collect_dca_only_rows(entries, dca_map: dict, dca_ev_map: dict,
                           dca_moat_trend_map: dict | None = None) -> list:
    """Return list of HTML row strings for DCAs without matching DD entries.

    Picks tickers in dca_map whose normalized form does not appear in any
    DD entry's ticker. Date is parsed from the DCA filename in dca_map.
    """
    if not dca_map:
        return []
    dd_tickers: set[str] = set()
    for e in entries:
        t = e["ticker"]
        dd_tickers.add(t)
        dd_tickers.add(re.sub(r"[^A-Za-z0-9]", "", t).upper())
    rows: list[str] = []
    for ticker, href in sorted(dca_map.items()):
        if ticker in dd_tickers:
            continue
        m = re.search(r"DCA_[A-Z0-9]+_(\d{8})\.html", href)
        date_str = ""
        if m:
            d = m.group(1)
            date_str = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
        ev = dca_ev_map.get(ticker)
        moat_trend_arrow = (dca_moat_trend_map or {}).get(ticker)
        rows.append(build_row_dca_only(ticker, href, date_str, ev, moat_trend_arrow))
    return rows


def collect_v12_entries(force_refresh_eps: bool = False):
    """Walk INDEX.md + DD HTMLs and produce per-row v12 entries.

    Per-DD priority for field extraction:
      1) <script id="dd-meta" type="application/json"> block in DD HTML head
         (canonical, plan-A lasting fix; v12.1+ DDs emit this).
      2) INDEX.md rr_raw column (triax: moat / val / ma).
      3) Regex extractors over DD HTML body (legacy fallback).

    Only includes DDs where INDEX.md schema starts with 'v12' or 'v13'
    (v13 = merged DD+DCA report; its decision layer lives inside the DD).
    """
    index_data = parse_index_md()
    eps_cache = load_eps_cagr_cache()
    cache_dirty = False  # track whether we fetched anything new

    entries = []
    for fname, md in index_data.items():
        if not md["schema"].startswith(("v12", "v13", "v14")):
            continue
        path = DD_DIR / fname
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")

        # Priority 1: dd-meta JSON block (canonical) ---------------------------
        meta = extract_dd_meta_json(text)
        ticker = (meta.get("ticker") if meta else None) or md["ticker"]
        cache_miss = ticker not in eps_cache
        eps_metrics = get_eps_metrics(ticker, eps_cache, force_refresh=force_refresh_eps)
        if cache_miss or force_refresh_eps:
            cache_dirty = True

        # §7 Munger gate table — extract for all DDs (runs once per DD file)
        munger_emoji, munger_pass, munger_total = extract_munger_threshold(text)

        if meta:
            stress = meta.get("stress", {}) or {}
            entry = {
                "ticker": ticker,
                "filename": fname,
                "href": f"/dd/{fname}",
                "date": meta.get("date") or md["date"],
                "signal": meta.get("signal", ""),
                "trap_emoji": meta.get("trap", "") or (md["trap"][:1] if md["trap"] else ""),
                "moat": meta.get("moat", ""),
                "val_emoji": meta.get("val", ""),
                "ma_state": meta.get("ma", ""),
                "fpe": str(meta["fpe_fy2"]) if meta.get("fpe_fy2") is not None else "",
                "pct": str(meta["pct_5y"]) if meta.get("pct_5y") is not None else "",
                "peg": str(meta["peg_fy2"]) if meta.get("peg_fy2") is not None else "",
                "upside": str(meta["upside_mid_pct"]) if meta.get("upside_mid_pct") is not None else "",
                "upside_5y": str(int(meta["upside_5y_pct"])) if meta.get("upside_5y_pct") is not None else "",
                "stress_pass": int(stress.get("pass", 0)),
                "stress_total": int(stress.get("total", 4) or 4),
                "eps_cagr_2y_value": eps_metrics["eps_cagr_2y_pct"],
                "pe_2y_value": eps_metrics["pe_2y"],
                "munger_emoji": munger_emoji,
                "munger_pass": munger_pass,
                "munger_total": munger_total,
            }
            entries.append(entry)
            continue

        # Priority 2 + 3: legacy regex fallback --------------------------------
        moat, val_emoji, ma_state = parse_triax(md["rr_raw"])
        sig = extract_signal_light(text) or _verdict_to_signal(md["verdict"])
        sp, st = extract_stress_v12(text)
        # 5Y upside: regex fallback from rr-long block
        m5y = UPSIDE_5Y_RE.search(text)
        upside_5y_fallback = m5y.group(1).replace("−", "-") if m5y else ""
        entries.append({
            "ticker": ticker,
            "filename": fname,
            "href": f"/dd/{fname}",
            "date": md["date"],
            "signal": sig,
            "trap_emoji": md["trap"][:1] if md["trap"] else "",
            "moat": moat,
            "val_emoji": val_emoji,
            "ma_state": ma_state,
            "fpe": extract_fpe_fy2(text),
            "pct": extract_5y_pct(text),
            "peg": extract_peg_v12(text),
            "upside": extract_upside_fy2(text, md.get("comment", "")),
            "upside_5y": upside_5y_fallback,
            "stress_pass": sp,
            "stress_total": st,
            "eps_cagr_2y_value": eps_metrics["eps_cagr_2y_pct"],
            "pe_2y_value": eps_metrics["pe_2y"],
            "munger_emoji": munger_emoji,
            "munger_pass": munger_pass,
            "munger_total": munger_total,
        })

    # Persist cache if any ticker was fetched (auto-backfill on new DD or refresh)
    if cache_dirty:
        save_eps_cagr_cache(eps_cache)

    # Latest DD per ticker only (date desc)
    latest = {}
    for e in entries:
        t = e["ticker"]
        if t not in latest or e["date"] > latest[t]["date"]:
            latest[t] = e
    return list(latest.values())


def _ticker_key(t: str) -> str:
    """Normalize ticker for de-dup comparison: strip dot/underscore so
    '2330.TW' == '2330TW', 'BRK.B' == 'BRKB'. Hand-curated rows historically
    drop the dot for TW/JP/HK tickers."""
    return t.replace(".", "").replace("_", "").upper()


def _sort_v12_entries(entries: list) -> list:
    """Sort v12 entries for the research index table.

    Order (highest priority first):
      1) signal rank descending (A+ → X)
      2) trap rank descending (🟢 → 🔴)
      3) upside_mid_pct descending (positive upside first)
      4) date descending (newest first)
    """
    def key(e):
        sig_rank = _SIGNAL_RANK.get(e.get("signal", ""), 0)
        trap_rank = _TRAP_RANK.get(e.get("trap_emoji", ""), 0)
        try:
            upside = float(e.get("upside") or 0)
        except (ValueError, TypeError):
            upside = 0.0
        date = e.get("date", "")
        # Negate values so default ascending sort yields desc order
        return (-sig_rank, -trap_rank, -upside, date)
    return sorted(entries, key=key, reverse=False)


def update_index_v12_full(html: str, force_refresh_eps: bool = False) -> tuple:
    """Full regenerate of v12 tbody from collect_v12_entries() (dd-meta SSOT).

    Replaces every row in <tbody id="dd-tbody-v12"> with freshly-built rows
    sorted by signal rank → trap rank → upside → date. Any manual HTML
    tweaks to existing rows are OVERWRITTEN — dd-meta JSON is the single
    source of truth, so corrections must be made there (not in row HTML).

    Returns (new_html, row_count).
    """
    tbody_re = re.compile(
        r'(<tbody id="dd-tbody-v12">)(.*?)(</tbody>)', re.DOTALL
    )
    m = tbody_re.search(html)
    if not m:
        return html, 0
    open_tag, _, close_tag = m.group(1), m.group(2), m.group(3)

    entries = _sort_v12_entries(collect_v12_entries(force_refresh_eps=force_refresh_eps))
    # The three collect_dca_* maps are v13-aware (overlay dd-meta decision-layer
    # fields over the legacy /dca/ scan, v13 wins) — see _v13_dca_overlay().
    dca_map = collect_dca_map()
    dca_ev_map = collect_dca_ev_map()
    dca_moat_trend_map = collect_dca_moat_trend_map()
    dd_rows = [build_row_v12(e, dca_map, dca_ev_map, dca_moat_trend_map)
               for e in entries]
    orphan_rows = collect_dca_only_rows(
        entries, dca_map, dca_ev_map, dca_moat_trend_map
    )
    if orphan_rows:
        print(f"  DCA-only rows (no DD coverage): {len(orphan_rows)} appended")
    rows = "\n".join(dd_rows + orphan_rows)
    new_block = open_tag + "\n" + rows + "\n" + close_tag
    new_html = html[:m.start()] + new_block + html[m.end():]
    return new_html, len(entries) + len(orphan_rows)


# === end v12 row builder =====================================================


def build_weekly_review(entries):
    """Compute 3 lists for the Weekly Review panel:
    - candidates: 建議 in {進場, 觀望偏進場} + 非陷阱 + 長期高信心, sorted by upside2 desc, top 15
    - downgrades: latest DD per ticker has worse verdict than previous DD
    - stale: latest DD per ticker older than 60 days
    Returns (candidates_html, downgrades_html, stale_html).
    """
    from datetime import date
    v_map = {"進場": 1, "觀望偏進場": 2, "觀望": 3, "迴避": 4}
    today = date.today()

    # Dedupe to latest DD per ticker (by date desc; if tied, keep the one with newer version)
    latest = {}
    for e in entries:
        t = e["ticker"]
        if t not in latest or e["date"] > latest[t]["date"]:
            latest[t] = e

    def up2_val(e):
        try:
            return float(e.get("upside2", "") or -1e9)
        except ValueError:
            return -1e9

    def link(e):
        href = e.get("href", "#")
        return f'<a href="{href}" target="_blank" rel="noopener">{e["ticker"]}</a>'

    # 1) Candidates
    candidates = [
        e for e in latest.values()
        if e.get("verdict", "").strip() in ("進場", "觀望偏進場")
           and "非陷阱" in e.get("trap", "")
           and e.get("confidence", "").strip() == "高"
    ]
    candidates.sort(key=up2_val, reverse=True)
    candidates = candidates[:15]

    def up2_str(e):
        v = up2_val(e)
        if v <= -1e8:
            return '<span class="wr-empty">N/A</span>'
        cls = "wr-up" if v >= 0 else "wr-down"
        sign = "+" if v >= 0 else ""
        return f'<span class="{cls}">{sign}{v:.1f}%</span>'

    cands_html = "\n".join(
        f'            <li>{link(e)} {up2_str(e)}</li>'
        for e in candidates
    ) or '            <li class="wr-empty">無符合條件的標的</li>'

    # 2) Downgrades
    by_ticker = {}
    for e in entries:
        by_ticker.setdefault(e["ticker"], []).append(e)
    downgrades = []
    for t, arr in by_ticker.items():
        if len(arr) < 2:
            continue
        arr_sorted = sorted(arr, key=lambda x: x["date"], reverse=True)
        cur, prev = arr_sorted[0], arr_sorted[1]
        cur_rank = v_map.get(cur.get("verdict", "").strip(), 9)
        prev_rank = v_map.get(prev.get("verdict", "").strip(), 9)
        if cur_rank > prev_rank and cur_rank < 9 and prev_rank < 9:
            downgrades.append({"entry": cur, "prev": prev, "diff": cur_rank - prev_rank})
    downgrades.sort(key=lambda x: (-x["diff"], x["entry"]["date"]), reverse=False)
    downgrades = sorted(downgrades, key=lambda x: (-x["diff"], x["entry"]["date"]))[:10]

    downs_html = "\n".join(
        f'            <li>{link(d["entry"])} <span class="wr-down">{d["prev"]["verdict"]} → {d["entry"]["verdict"]}</span></li>'
        for d in downgrades
    ) or '            <li class="wr-empty">近期無降級紀錄</li>'

    # 3) Stale (> 60 days, latest per ticker)
    stale = []
    for t, e in latest.items():
        try:
            dt = date.fromisoformat(e["date"])
        except (ValueError, KeyError, TypeError):
            continue
        days = (today - dt).days
        if days > 60:
            stale.append({"entry": e, "days": days})
    stale.sort(key=lambda x: -x["days"])
    stale = stale[:10]

    stale_html = "\n".join(
        f'            <li>{link(s["entry"])} <span class="wr-age">{s["days"]} 天</span></li>'
        for s in stale
    ) or '            <li class="wr-empty">所有 DD 均在 60 天內</li>'

    return cands_html, downs_html, stale_html


def build_outdated_dd_banner() -> str:
    """Build banner HTML reminding which DDs need re-run because the ticker
    has reported earnings after the DD date. Returns empty string if none.
    """
    try:
        from find_outdated_dds import find_outdated
    except ImportError:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).parent))
        from find_outdated_dds import find_outdated  # type: ignore
    rows = find_outdated()
    if not rows:
        return ""  # auto-hide when caught up
    chips = "\n      ".join(
        f'<span style="background:rgba(255,255,255,.2);padding:4px 10px;border-radius:4px;font-family:\'IBM Plex Mono\',monospace;font-weight:600">'
        f'{r["ticker"]} <span style="opacity:.75;font-weight:400;font-size:12px">({r["earnings_date"][5:]})</span></span>'
        for r in rows
    )
    return (
        '<div style="background:linear-gradient(90deg,#B45309,#D97706);color:#fff;padding:14px 0;margin:0 0 20px 0">\n'
        '  <div class="container">\n'
        '    <div style="font-size:14px;font-weight:600;margin-bottom:8px">\n'
        f'      ⚠️ 已發財報但 DD 未更新（{len(rows)} 檔）— 提醒重跑\n'
        '    </div>\n'
        '    <div style="font-size:13px;display:flex;flex-wrap:wrap;gap:6px">\n'
        f'      {chips}\n'
        '    </div>\n'
        '  </div>\n'
        '</div>'
    )


# === PM marker injection ======================================================

PM_DIR = DOCS / "pm"
PM_INDEX_MD = PM_DIR / "INDEX.md"


def parse_latest_pm():
    """Find latest PM_YYYYMMDD.html by filename date, return (path, date_str).
    Returns (None, None) if no PM files found."""
    pm_files = sorted(PM_DIR.glob("PM_[0-9]*.html"))
    if not pm_files:
        return None, None
    # Sort by embedded date in filename (last 8 digits before .html)
    def _pm_date(p):
        m = re.match(r'PM_(\d{8})\.html$', p.name)
        return m.group(1) if m else ""
    pm_files = [f for f in pm_files if _pm_date(f)]
    if not pm_files:
        return None, None
    latest = max(pm_files, key=_pm_date)
    raw_date = _pm_date(latest)
    date_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
    return latest, date_str


def _pm_mtime_cst(path: Path) -> str:
    """Return file mtime in CST (UTC+8) as 'YYYY-MM-DD HH:MM CST'."""
    import datetime
    mtime = path.stat().st_mtime
    utc_dt = datetime.datetime.utcfromtimestamp(mtime)
    cst_dt = utc_dt + datetime.timedelta(hours=8)
    return cst_dt.strftime("%Y-%m-%d %H:%M CST")


def inject_pm_last_run(html: str, pm_path: Path) -> str:
    """Inject PM_LAST_RUN_START/END with file mtime in CST."""
    try:
        ts = _pm_mtime_cst(pm_path)
        new_html = re.sub(
            r'<!-- PM_LAST_RUN_START -->.*?<!-- PM_LAST_RUN_END -->',
            f'<!-- PM_LAST_RUN_START -->{ts}<!-- PM_LAST_RUN_END -->',
            html,
            flags=re.DOTALL,
        )
        return new_html
    except Exception as e:
        print(f"WARN: PM_LAST_RUN injection skipped — {e}")
        return html


def inject_pm_holdings(html: str, pm_path: Path, pm_date: str) -> str:
    """Parse §1 'after rebalance' table in PM HTML and inject PM_HOLDINGS block."""
    try:
        text = pm_path.read_text(encoding="utf-8", errors="ignore")
        pm_filename = pm_path.name

        # Build link to the PM file (strip .html → /pm/<filename>)
        pm_href = f"/pm/{pm_filename}"

        # Parse the §1 holdings table: look for <thead> with 本週後 column,
        # then extract rows. We use the table right after "after rebalance" h3.
        # Structure: <tr><td rowspan="N"><strong>核心 N/N</strong></td><td>TICKER</td>
        #   ...<td class="num-cell">X%</td><td class="num-cell">Y%</td>...
        #   <td><span class="signal-Aplus">A+</span>...</td>...</tr>
        # and <tr><td><strong>現金</strong></td>...<td class="num-cell"><strong>Z%</strong>...</td>

        # Find the table section after "after rebalance"
        rebalance_anchor = text.find("after rebalance")
        if rebalance_anchor < 0:
            rebalance_anchor = text.find("§1")
        if rebalance_anchor < 0:
            raise ValueError("Cannot find §1 / 'after rebalance' section")

        table_start = text.find("<table", rebalance_anchor)
        table_end = text.find("</table>", table_start) + len("</table>")
        if table_start < 0 or table_end < len("</table>"):
            raise ValueError("Cannot find holdings table")
        table_html = text[table_start:table_end]

        # Parse rows with regex
        # rowspan-group rows: <tr><td rowspan="N"><strong>TYPE N/N</strong></td><td>TICKER...
        # continuation rows: <tr><td>TICKER...
        # cash row: <tr><td><strong>現金</strong></td>...
        row_re = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL)
        # Match full <td ...>content</td> keeping the tag attrs
        full_cell_re = re.compile(r'(<td([^>]*)>)(.*?)</td>', re.DOTALL)
        signal_re = re.compile(r'class="signal-([^"]+)"[^>]*>([^<]+)<')

        holdings = []  # list of (tier, ticker, pct, signal)
        cash_pct = ""
        current_tier = ""

        for row_m in row_re.finditer(table_html):
            row = row_m.group(1)
            full_cells = [(m.group(2), TAG_RE.sub("", m.group(3)).strip())
                          for m in full_cell_re.finditer(row)]
            # full_cells: list of (attrs, text_content)

            if not full_cells or full_cells[0][1] == "類別":
                continue  # header row

            # Check for tier group cell (rowspan)
            tier_m = re.search(r'rowspan[^>]*>.*?<strong>([^<]+)</strong>', row)
            if tier_m:
                current_tier = tier_m.group(1).strip()

            cell_texts = [c[1] for c in full_cells]
            cell_attrs = [c[0] for c in full_cells]

            # Cash row detection — "現金" in first cell text
            if cell_texts and "現金" in cell_texts[0]:
                # num-cell columns: attrs contain 'num-cell'
                num_cell_vals = [cell_texts[i] for i, a in enumerate(cell_attrs)
                                 if 'num-cell' in a]
                # 本週後 is second num-cell (index 1)
                raw_val = num_cell_vals[1] if len(num_cell_vals) >= 2 else (
                    num_cell_vals[0] if num_cell_vals else "")
                pct_m = re.search(r'(\d+)', raw_val)
                cash_pct = pct_m.group(1) + "%" if pct_m else raw_val
                continue

            # Holdings row: first cell (after possible rowspan) is ticker
            ticker_cell_idx = 1 if tier_m else 0
            if len(cell_texts) < ticker_cell_idx + 2:
                continue
            ticker = cell_texts[ticker_cell_idx].strip()
            if not ticker or "現金" in ticker or "類別" in ticker or ticker == "—":
                continue
            # Skip rows that start with tier labels (核心/衛星/新進)
            if any(kw in ticker for kw in ("核心", "衛星", "候選", "§")):
                continue

            # Find 本週後 % — the second num-cell column
            num_cell_vals = [cell_texts[i] for i, a in enumerate(cell_attrs)
                             if 'num-cell' in a]
            after_pct = ""
            raw_val = num_cell_vals[1] if len(num_cell_vals) >= 2 else (
                num_cell_vals[0] if num_cell_vals else "")
            pct_m = re.search(r'(\d+)', raw_val)
            if pct_m:
                after_pct = pct_m.group(1) + "%"

            # Extract signal from the row HTML
            sig_m = signal_re.search(row)
            signal = ""
            if sig_m:
                sig_class = sig_m.group(1)  # "Aplus", "A", "B", "C", "X"
                sig_text = sig_m.group(2).strip()
                # Normalize signal text (might have trailing noise like " (↓)")
                sig_clean = re.match(r'([A-Z][+]?)', sig_text)
                if sig_clean and sig_clean.group(1) in {"A+", "A", "B", "C", "X", "S"}:
                    signal = sig_clean.group(1)
                elif sig_class == "Aplus":
                    signal = "A+"

            if ticker and after_pct:
                holdings.append((current_tier, ticker, after_pct, signal))

        if not holdings:
            raise ValueError("No holdings parsed from PM HTML table")

        # Build the HTML block
        lines = []
        lines.append(f'          <div style="font-size:12px;color:#64748b;margin-bottom:6px">'
                     f'提案日：{pm_date} · <a href="{pm_href}">詳細→</a></div>')
        lines.append('          <ul style="padding-left:18px;margin:4px 0;list-style:none;font-size:13px">')

        last_tier_label = None
        core_count = sum(1 for t, _, _, _ in holdings if "核心" in t)
        sat_count = sum(1 for t, _, _, _ in holdings if "衛星" in t)

        tier_order = []
        for tier, ticker, pct, signal in holdings:
            if tier not in tier_order:
                tier_order.append(tier)

        first_tier = tier_order[0] if tier_order else None
        seen_tiers = set()
        for tier, ticker, pct, signal in holdings:
            if tier not in seen_tiers:
                seen_tiers.add(tier)
                margin = (' style="font-weight:600"' if tier == first_tier
                          else ' style="font-weight:600;margin-top:6px"')
                lines.append(f'            <li{margin}>{tier}</li>')
            sig_str = f" · {signal}" if signal else ""
            lines.append(f'            <li><strong>{ticker}</strong> {pct}{sig_str}</li>')

        # Cash
        lines.append('            <li style="font-weight:600;margin-top:6px">現金</li>')
        if cash_pct:
            lines.append(f'            <li>{cash_pct}</li>')
        else:
            lines.append('            <li>—</li>')
        lines.append('          </ul>')

        block = "\n".join(lines)

        new_html = re.sub(
            r'<!-- PM_HOLDINGS_START -->.*?<!-- PM_HOLDINGS_END -->',
            f'<!-- PM_HOLDINGS_START -->\n{block}\n<!-- PM_HOLDINGS_END -->',
            html,
            flags=re.DOTALL,
        )
        return new_html
    except Exception as e:
        print(f"WARN: PM_HOLDINGS injection skipped — {e}")
        return html


def inject_pm_actions(html: str) -> str:
    """Parse PM INDEX.md last row's action_summary + note to inject PM_ACTIONS block.

    Uses Strategy B (INDEX.md note column split on <br>) to build bullet list.
    The note column is col[8] in the last data row.
    """
    try:
        if not PM_INDEX_MD.exists():
            raise FileNotFoundError(f"{PM_INDEX_MD} not found")

        lines = PM_INDEX_MD.read_text(encoding="utf-8").splitlines()
        # Find last row that starts with "| 20"
        last_row = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("|") and re.match(r'\|\s*20\d{2}-', stripped):
                last_row = stripped
        if not last_row:
            raise ValueError("No data rows found in PM INDEX.md")

        cols = [c.strip() for c in last_row.split("|")]
        # cols[0] = '', cols[1]=date, cols[2]=NAV, cols[3]=cash%,
        # cols[4]=core, cols[5]=sat, cols[6]=action_summary, cols[7]=override,
        # cols[8]=filename, cols[9:]=note (rejoin if contains |)
        if len(cols) < 9:
            raise ValueError(f"Not enough columns in last PM row: {len(cols)}")

        # Note is cols[9] onward (rejoin), fallback to action_summary (cols[6])
        if len(cols) >= 10:
            note_raw = "|".join(cols[9:-1]).strip() if len(cols) > 10 else cols[9].strip()
        else:
            note_raw = cols[6].strip()  # action_summary fallback

        if not note_raw:
            note_raw = cols[6].strip()

        # Split note on <br> or <br/> tags to get bullet items
        items = re.split(r'<br\s*/?>', note_raw)
        items = [TAG_RE.sub("", item).strip() for item in items]
        items = [item for item in items if item]

        if not items:
            # Fallback to action_summary split on "/"
            action_summary = cols[6].strip() if len(cols) > 6 else ""
            items = [i.strip() for i in action_summary.split("/") if i.strip()]

        if not items:
            raise ValueError("No action items found in INDEX.md note or action_summary")

        li_items = "\n".join(
            f'            <li>{item}</li>'
            for item in items
        )
        block = (
            '          <ol style="padding-left:20px;margin:4px 0;font-size:13px">\n'
            f'{li_items}\n'
            '          </ol>'
        )

        new_html = re.sub(
            r'<!-- PM_ACTIONS_START -->.*?<!-- PM_ACTIONS_END -->',
            f'<!-- PM_ACTIONS_START -->\n{block}\n<!-- PM_ACTIONS_END -->',
            html,
            flags=re.DOTALL,
        )
        return new_html
    except Exception as e:
        print(f"WARN: PM_ACTIONS injection skipped — {e}")
        return html


# === end PM marker injection ==================================================


def update_index(entries, dry_run: bool = False, force_refresh_eps: bool = False):
    html = INDEX_HTML.read_text(encoding="utf-8")
    original_html = html

    # v12 mode: page uses <tbody id="dd-tbody-v12"> with rows that include
    # sortable data-* attrs (data-signal / data-fpe / data-pe2y / data-peg /
    # data-eps-cagr / data-upside / data-upside5y / data-ev5y / data-moat-trend)
    # — schema incompatible with v11 build_rows().
    # Strategy: APPEND-ONLY. Add rows for v12 DDs not yet in the table; never
    # overwrite existing hand-curated rows so QA tweaks survive.
    v12_mode = '<tbody id="dd-tbody-v12">' in html
    if v12_mode:
        new_html, row_count = update_index_v12_full(html, force_refresh_eps=force_refresh_eps)
        print(
            f"v12 mode: regenerated dd-tbody-v12 from dd-meta JSON "
            f"({row_count} row(s) total — full overwrite)."
        )
        # Note: thead, CSS cleanup, and v11 build_rows() stay disabled in v12 mode.
        # WR_STALE / timestamp updates below still run.
    else:
        # Legacy v11.x path: regenerate thead + tbody from entries
        new_thead = (
            '<thead>\n'
            '          <tr>\n'
            '            <th class="sortable" data-sort="ticker">公司</th>\n'
            '            <th class="sortable" data-sort="date">日期</th>\n'
            '            <th class="sortable" data-sort="verdict">建議</th>\n'
            '            <th class="sortable" data-sort="moat">護城河</th>\n'
            '            <th class="sortable" data-sort="upside1">FY+1 Upside</th>\n'
            '            <th class="sortable sorted-desc" data-sort="upside2">FY+2 Upside</th>\n'
            '            <th class="sortable" data-sort="trap">陷阱</th>\n'
            '            <th class="sortable" data-sort="confidence">長期持有</th>\n'
            '            <th>備註</th>\n'
            '          </tr>\n'
            '        </thead>'
        )
        html = re.sub(
            r'<thead>.*?</thead>',
            new_thead,
            html,
            count=1,
            flags=re.DOTALL,
        )

        # Replace tbody
        pattern = r'(<tbody id="dd-tbody">)\n?.*?(\s*</tbody>)'
        replacement = r'\1\n' + build_rows(entries) + r'\2'
        new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)

        if count == 0:
            print(
                f"ERROR: Could not find <tbody id=\"dd-tbody\"> nor "
                f"<tbody id=\"dd-tbody-v12\"> in {INDEX_HTML}"
            )
            return False

        # Remove legacy injected CSS blocks (styles are now in the HTML template)
        new_html = re.sub(
            r'\n?/\* v(?:9|10)\.0 Badge Styles \*/.*?(?=</style>)',
            '\n',
            new_html,
            count=1,
            flags=re.DOTALL,
        )

    # Stamp price-refresh timestamp from cache (if present)
    cache = load_price_cache()
    ts_raw = cache.get("refreshed_at", "")
    ts_display = ts_raw.replace("T", " ")[:16] if ts_raw else "尚未刷新"
    new_html = re.sub(
        r'(<strong id="meta-refresh">)[^<]*(</strong>)',
        rf'\g<1>{ts_display}\g<2>',
        new_html,
        count=1,
    )

    # Inject Weekly Review lists
    cands_html, downs_html, stale_html = build_weekly_review(entries)
    new_html = re.sub(
        r'<!-- WR_CANDIDATES_START -->.*?<!-- WR_CANDIDATES_END -->',
        f'<!-- WR_CANDIDATES_START -->\n{cands_html}\n            <!-- WR_CANDIDATES_END -->',
        new_html,
        flags=re.DOTALL,
    )
    new_html = re.sub(
        r'<!-- WR_DOWNGRADES_START -->.*?<!-- WR_DOWNGRADES_END -->',
        f'<!-- WR_DOWNGRADES_START -->\n{downs_html}\n            <!-- WR_DOWNGRADES_END -->',
        new_html,
        flags=re.DOTALL,
    )
    new_html = re.sub(
        r'<!-- WR_STALE_START -->.*?<!-- WR_STALE_END -->',
        f'<!-- WR_STALE_START -->\n{stale_html}\n            <!-- WR_STALE_END -->',
        new_html,
        flags=re.DOTALL,
    )

    # Inject DD auto-stats panel (replaces former hand-curated insight-box)
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).parent))
        from aggregate_dd_stats import load_records as _load_recs, render as _render_stats, set_table_html as _set_table_html
        _set_table_html(new_html)  # 直接抓現在表格有的（in-memory fresh table）
        stats_html = _render_stats(_load_recs())
        new_html = re.sub(
            r'<!-- DD_AUTO_STATS_START -->.*?<!-- DD_AUTO_STATS_END -->',
            f'<!-- DD_AUTO_STATS_START -->\n    {stats_html}\n    <!-- DD_AUTO_STATS_END -->',
            new_html,
            flags=re.DOTALL,
        )
        print("DD_AUTO_STATS injected.")
    except Exception as e:
        print(f"WARN: DD_AUTO_STATS injection skipped — {e}")

    # Inject DCA auto-stats panel (mirrors DD_AUTO_STATS, reads docs/dca/)
    try:
        from aggregate_dca_stats import load_dca_records, render as render_dca_stats
        _dca_records = load_dca_records()
        _dca_stats_html = render_dca_stats(_dca_records)
        new_html = re.sub(
            r'<!-- DCA_AUTO_STATS_START -->.*?<!-- DCA_AUTO_STATS_END -->',
            f'<!-- DCA_AUTO_STATS_START -->\n    {_dca_stats_html}\n    <!-- DCA_AUTO_STATS_END -->',
            new_html,
            flags=re.DOTALL,
        )
        print("DCA_AUTO_STATS injected.")
    except Exception as e:
        print(f"WARN: DCA_AUTO_STATS injection skipped — {e}")

    # Inject DD freshness panel (yfinance scan, cached 6h)
    try:
        from check_dd_earnings_freshness import (
            load_records as _frload,
            scan_all as _frscan,
            load_cache as _frload_cache,
            save_cache as _frsave_cache,
            filter_cached_against_current as _frfilter,
            render_html as _frrender,
        )
        fr_records = _frload()
        cached, age = _frload_cache()
        if cached is not None:
            stale_list = _frfilter(cached, fr_records)
            print(f"DD_STALE_FRESH: using cache ({len(cached)}→{len(stale_list)} after filter, age={int(age)}s)")
        else:
            print(f"DD_STALE_FRESH: scanning {len(fr_records)} tickers via yfinance (cache miss/expired)...")
            stale_list = _frscan(fr_records, progress=False)
            _frsave_cache(stale_list)
            print(f"DD_STALE_FRESH: cached {len(stale_list)} stale entries")
        fresh_html = _frrender(stale_list)
        new_html = re.sub(
            r'<!-- DD_STALE_FRESH_START -->.*?<!-- DD_STALE_FRESH_END -->',
            f'<!-- DD_STALE_FRESH_START -->\n    {fresh_html}\n    <!-- DD_STALE_FRESH_END -->',
            new_html,
            flags=re.DOTALL,
        )
        print("DD_STALE_FRESH injected.")
    except Exception as e:
        print(f"WARN: DD_STALE_FRESH injection skipped — {e}")

    # Inject PM marker blocks (PM_LAST_RUN, PM_HOLDINGS, PM_ACTIONS)
    pm_path, pm_date = parse_latest_pm()
    if pm_path:
        if "<!-- PM_LAST_RUN_START -->" in new_html:
            new_html = inject_pm_last_run(new_html, pm_path)
            print(f"PM_LAST_RUN injected ({pm_path.name}).")
        if "<!-- PM_HOLDINGS_START -->" in new_html:
            new_html = inject_pm_holdings(new_html, pm_path, pm_date)
            print(f"PM_HOLDINGS injected ({pm_path.name}).")
        if "<!-- PM_ACTIONS_START -->" in new_html:
            new_html = inject_pm_actions(new_html)
            print(f"PM_ACTIONS injected (INDEX.md Strategy B).")
    else:
        print("WARN: No PM_*.html files found — PM markers not updated.")

    if dry_run:
        # Print unified diff and skip the write
        import difflib
        diff = list(difflib.unified_diff(
            original_html.splitlines(keepends=False),
            new_html.splitlines(keepends=False),
            fromfile="docs/research/index.html (current)",
            tofile="docs/research/index.html (after regen)",
            n=2,
        ))
        if diff:
            print()
            print("=" * 70)
            print("DRY RUN — diff preview (no files written)")
            print("=" * 70)
            for line in diff[:200]:
                print(line)
            if len(diff) > 200:
                print(f"... ({len(diff) - 200} more lines truncated)")
            print("=" * 70)
            print(f"Total diff lines: {len(diff)}. Run without --dry-run to apply.")
        else:
            print("DRY RUN: no changes (file would be written identically).")
        return True

    INDEX_HTML.write_text(new_html, encoding="utf-8")
    return True


def refresh_upsides(entries: list) -> int:
    """Fetch current prices via yfinance and overwrite upside1/2 based on targets.
    Returns count of rows actually refreshed."""
    yf_tickers = sorted({
        e["ticker_yf"] for e in entries
        if e.get("ticker_yf") and (e.get("target1") or e.get("target2"))
    })
    prices = fetch_prices(yf_tickers)
    refreshed = 0
    missing = []
    for e in entries:
        yf_t = e.get("ticker_yf")
        price = prices.get(yf_t)
        if price is None or price == 0:
            if e.get("target1") or e.get("target2"):
                missing.append(e["ticker"])
            continue
        if e.get("target1"):
            e["upside1"] = f"{(e['target1'] - price) / price * 100:.1f}"
        if e.get("target2"):
            e["upside2"] = f"{(e['target2'] - price) / price * 100:.1f}"
        e["current_price"] = price
        refreshed += 1
    # persist to cache
    cache = {
        "refreshed_at": dt.datetime.now().isoformat(timespec="seconds"),
        "prices": {t: round(p, 4) for t, p in prices.items()},
    }
    save_price_cache(cache)
    if missing:
        print(f"Missing prices for {len(missing)} ticker(s): {', '.join(missing)}")
    print(f"Refreshed upsides for {refreshed} row(s). Cache → {PRICE_CACHE}")
    return refreshed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh-prices",
        action="store_true",
        help="Fetch current prices via yfinance and recompute upsides.",
    )
    parser.add_argument(
        "--refresh-eps-cagr",
        action="store_true",
        help="Force re-fetch EPS CAGR / 2Y PE for all tickers via yfinance "
             "(default: cache-only; new tickers auto-backfilled).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show unified diff of changes without writing the file.",
    )
    parser.add_argument(
        "--skip-dd-screener",
        action="store_true",
        help="Skip the auto-trigger of scripts/build_dd_screener.py at the end "
             "(use when you want only the research index sync — e.g. offline).",
    )
    args = parser.parse_args()

    index_data = parse_index_md()
    entries = scan_files(index_data)
    print(f"Found {len(entries)} v9.x/v10.x DD files:")
    for e in entries:
        conf = e.get("confidence", "—") or "—"
        print(f"  {e['ticker']:8s} {e['date']}  {e['verdict']:4s}  {e['quality']:3s}  conf={conf}  {e['href']}")

    if args.refresh_prices:
        print()
        refresh_upsides(entries)

    if update_index(entries, dry_run=args.dry_run, force_refresh_eps=args.refresh_eps_cagr):
        if args.dry_run:
            print(f"\n(dry-run; no file written)")
        else:
            print(f"\nUpdated {INDEX_HTML}")
    else:
        print("\nFailed to update index.html")

    # Auto-trigger DD Screener rebuild so /research/ and /dd-screener/ stay in
    # lockstep. New DD/DCA additions are picked up via the stateless glob in
    # build_dd_screener.py. Failure here (e.g. yfinance network blip) must NOT
    # abort the research-sync caller — it's a separate, supplementary page.
    if args.dry_run or args.skip_dd_screener:
        return
    import subprocess  # local import — only used in this terminal hook
    screener_script = Path(__file__).resolve().parent / "build_dd_screener.py"
    if not screener_script.exists():
        return

    # v1.4: Cascade debounce — 連續寫多 DD/DCA 時，每次寫完都 trigger 此 cascade，
    # 每次都跑 yfinance batch (~127 檔 5Y weekly = ~25-30s)，連跑 N 次極易把 yfinance
    # rate-limit 撞炸。Debounce 60s：若 latest.json 在 60s 內已 rebuild，跳過 cascade。
    # 連寫 7 個 DD 的情況下，只第一次 trigger 完整 cascade，後 6 次 skip — 等使用者寫
    # 完整批後手動跑 `python3 scripts/build_dd_screener.py` 一次補齊。
    DEBOUNCE_SEC = 60
    screener_latest = DOCS / "dd-screener" / "latest.json"
    if screener_latest.exists():
        try:
            age = time.time() - screener_latest.stat().st_mtime
            if age < DEBOUNCE_SEC:
                print(
                    f"\n⏸ DD Screener cascade debounced — latest.json updated "
                    f"{age:.0f}s ago (< {DEBOUNCE_SEC}s window).\n"
                    f"   Skipping build_dd_screener + quality-entry + bottom-out + breakout + earnings-acceleration + entry-state.\n"
                    f"   寫完整批後請手動跑：python3 scripts/build_dd_screener.py "
                    f"&& python3 scripts/build_quality_entry.py "
                    f"&& python3 scripts/build_bottom_out.py "
                    f"&& python3 scripts/build_breakout.py "
                    f"&& python3 scripts/build_earnings_acceleration.py "
                    f"&& python3 scripts/build_entry_state.py"
                )
                return
        except OSError:
            pass

    print(f"\n→ Auto-trigger: {screener_script.name} (rebuild /dd-screener/ to match universe)")
    screener_ok = False
    try:
        subprocess.run(
            [sys.executable, str(screener_script)],
            check=True,
        )
        screener_ok = True
    except subprocess.CalledProcessError as e:
        print(
            f"\n⚠ DD Screener rebuild failed (exit {e.returncode}). "
            f"/research/ sync succeeded; rerun `python3 {screener_script}` "
            f"manually if /dd-screener/ needs to refresh.",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"\n⚠ DD Screener rebuild errored: {e}. "
            f"/research/ sync succeeded.",
            file=sys.stderr,
        )

    # Event-driven trigger for supply-chain DD link map. Independent of screener
    # — pure file glob, no network. Always run so /supply-chain/ company tables
    # deep-link to the latest DD reports even when yfinance / screener flaked.
    sc_script = Path(__file__).resolve().parent / "build_supply_chain_dd_index.py"
    if sc_script.exists():
        print(f"\n→ Auto-trigger: {sc_script.name} (rebuild /supply-chain/ DD link map)")
        try:
            subprocess.run([sys.executable, str(sc_script)], check=True)
        except subprocess.CalledProcessError as e:
            print(
                f"\n⚠ supply-chain DD link rebuild failed (exit {e.returncode}). "
                f"Rerun `python3 {sc_script}` manually.",
                file=sys.stderr,
            )

    # ARCHIVED: alpha-rank.html is archived (stub at URL). Auto-trigger for DD Alpha Ranker
    # is disabled so update_dd_index.py does not regenerate the page.
    # To re-enable: uncomment the block below and restore _archived/dd-screener/alpha-rank.html.
    # Event-driven trigger for DD Alpha Ranker fundamental layer (angles 1/3/4).
    # Per TASK §修正 7: must run only after update_dd_index + build_dd_screener
    # fully succeed — never on half-stale data. Failure here is non-fatal
    # (alpha-rank is supplementary).
    # if not screener_ok:
    #     return
    # alpha_script = Path(__file__).resolve().parent / "dd_alpha_ranker.py"
    # if not alpha_script.exists():
    #     return
    # print(f"\n→ Auto-trigger: {alpha_script.name} --layers fundamental")
    # try:
    #     subprocess.run(
    #         [sys.executable, str(alpha_script), "--layers", "fundamental"],
    #         check=True,
    #     )
    # except subprocess.CalledProcessError as e:
    #     print(
    #         f"\n⚠ Alpha Ranker fundamental layer failed (exit {e.returncode}). "
    #         f"Other layers (momentum/jensen) still reflect their last state. "
    #         f"Rerun `python3 {alpha_script} --layers fundamental` manually.",
    #         file=sys.stderr,
    #     )
    # except Exception as e:
    #     print(
    #         f"\n⚠ Alpha Ranker errored: {e}.",
    #         file=sys.stderr,
    #     )
    if not screener_ok:
        return

    # Event-driven trigger for Quality-Entry screener (品質複利者 + 勝率切入點).
    # Reads latest.json (schema v1.2+) and emits docs/dd-screener/quality-entry.{html,json}
    # plus a daily snapshot. Independent of Alpha Ranker — its failure must not block
    # this; both are supplementary to the canonical /research/ + /dd-screener/.
    qe_script = Path(__file__).resolve().parent / "build_quality_entry.py"
    if not qe_script.exists():
        return
    print(f"\n→ Auto-trigger: {qe_script.name}")
    try:
        subprocess.run(
            [sys.executable, str(qe_script)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"\n⚠ Quality-Entry build failed (exit {e.returncode}). "
            f"Rerun `python3 {qe_script}` manually.",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"\n⚠ Quality-Entry errored: {e}.",
            file=sys.stderr,
        )

    # Event-driven trigger for Bottom-Out screener (深回檔逆向訊號).
    # Reads latest.json (schema v1.2+) and emits docs/dd-screener/bottom-out.{html,json}
    # plus a daily snapshot. Runs after Quality-Entry — its failure is non-fatal.
    bo_script = Path(__file__).resolve().parent / "build_bottom_out.py"
    if not bo_script.exists():
        return
    print(f"\n→ Auto-trigger: {bo_script.name}")
    try:
        subprocess.run(
            [sys.executable, str(bo_script)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"\n⚠ Bottom-Out build failed (exit {e.returncode}). "
            f"Rerun `python3 {bo_script}` manually.",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"\n⚠ Bottom-Out errored: {e}.",
            file=sys.stderr,
        )

    # Event-driven trigger for Breakout screener (突破動能追擊).
    # Reads latest.json (schema v1.2+) and emits docs/dd-screener/breakout.{html,json}
    # plus a daily snapshot. Runs after Bottom-Out — its failure is non-fatal.
    brk_script = Path(__file__).resolve().parent / "build_breakout.py"
    if not brk_script.exists():
        return
    print(f"\n→ Auto-trigger: {brk_script.name}")
    try:
        subprocess.run(
            [sys.executable, str(brk_script)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"\n⚠ Breakout build failed (exit {e.returncode}). "
            f"Rerun `python3 {brk_script}` manually.",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"\n⚠ Breakout errored: {e}.",
            file=sys.stderr,
        )

    # Event-driven trigger for Earnings Acceleration screener (EPS 加速篩選).
    # Reads latest.json (schema v1.2+) + fetches yfinance eps_trend/earnings_history
    # and emits docs/dd-screener/earnings-acceleration.{html,json} plus a daily snapshot.
    # Runs after Breakout — its failure is non-fatal.
    ea_script = Path(__file__).resolve().parent / "build_earnings_acceleration.py"
    if not ea_script.exists():
        return
    print(f"\n→ Auto-trigger: {ea_script.name}")
    try:
        subprocess.run(
            [sys.executable, str(ea_script)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"\n⚠ Earnings Acceleration build failed (exit {e.returncode}). "
            f"Rerun `python3 {ea_script}` manually.",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"\n⚠ Earnings Acceleration errored: {e}.",
            file=sys.stderr,
        )

    # Event-driven trigger for Entry State screener (BREAKOUT / RIDING / WATCH classifier).
    # Reads quality-entry.json (Q≥0.55 / G≥0.50 universe with archetype=成長型) +
    # yfinance MA/RSI snapshots and emits docs/dd-screener/entry-state.{html,json}
    # plus a daily snapshot + state_store (WATCH hysteresis counters).
    # Runs after Earnings Acceleration — its failure is non-fatal.
    es_script = Path(__file__).resolve().parent / "build_entry_state.py"
    if not es_script.exists():
        return
    print(f"\n→ Auto-trigger: {es_script.name}")
    try:
        subprocess.run(
            [sys.executable, str(es_script)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"\n⚠ Entry State build failed (exit {e.returncode}). "
            f"Rerun `python3 {es_script}` manually.",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"\n⚠ Entry State errored: {e}.",
            file=sys.stderr,
        )

    # Self-heal pass for the canonical site header (scripts/site_nav.py):
    # any page newly written by a skill/generator since the last sync gets the
    # unified nav injected; pages already canonical are untouched (idempotent).
    # Runs last — its failure is non-fatal.
    nav_script = Path(__file__).resolve().parent / "site_nav.py"
    if not nav_script.exists():
        return
    print(f"\n→ Auto-trigger: {nav_script.name} (site header self-heal)")
    try:
        subprocess.run(
            [sys.executable, str(nav_script)],
            check=True,
        )
    except Exception as e:
        print(
            f"\n⚠ site_nav self-heal errored: {e}. "
            f"Rerun `python3 {nav_script}` manually.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
