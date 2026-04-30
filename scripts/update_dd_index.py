#!/usr/bin/env python3
"""
Scan docs/dd/ for DD_*.html files, cross-reference INDEX.md for v9.x/v10.x metadata,
and update the deep research table in docs/research/index.html.

v10.0 update: Remove R:R/上檔/下檔/紅燈 columns, add 長期持有信心 column.

Usage:
  python scripts/update_dd_index.py                  # normal regenerate (upside = DD 快照)
  python scripts/update_dd_index.py --refresh-prices # fetch yfinance and recompute upside
"""
import argparse
import datetime as dt
import json
import re
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"
DD_DIR = DOCS / "dd"
INDEX_HTML = DOCS / "research" / "index.html"
INDEX_MD = DD_DIR / "INDEX.md"
PRICE_CACHE = DOCS / "research" / "price_cache.json"

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


def build_row_v12(entry: dict) -> str:
    """Render one v12 row (data-* attrs + 9 td cells) matching the hand-curated
    schema in docs/research/index.html. Missing fields render as '?' or 0."""
    sig = entry.get("signal", "") or "?"
    trap_emoji = entry.get("trap_emoji", "") or "?"
    moat = entry.get("moat", "") or "?"
    val_emoji = entry.get("val_emoji", "") or "?"
    ma_state = entry.get("ma_state", "") or "?"
    fpe = entry.get("fpe", "")
    pct = entry.get("pct", "")
    peg = entry.get("peg", "")
    upside = entry.get("upside", "")
    upside_5y = entry.get("upside_5y", "")
    sp, st = entry.get("stress_pass", 0), entry.get("stress_total", 4)

    # Numeric data attrs (for sorting); fallback to 0 when empty.
    rank = _SIGNAL_RANK.get(sig, 0)
    trap_rank = _TRAP_RANK.get(trap_emoji, 0)
    quality = _MOAT_QUALITY.get(moat, 0)
    try:
        fpe_num = float(fpe) if fpe else 0.0
    except ValueError:
        fpe_num = 0.0
    try:
        pct_num = float(pct) if pct else 0.0
    except ValueError:
        pct_num = 0.0
    try:
        peg_num = float(peg) if peg else 0.0
    except ValueError:
        peg_num = 0.0
    try:
        up_num = float(upside) if upside else 0.0
    except ValueError:
        up_num = 0.0
    try:
        up5y_num = float(upside_5y) if upside_5y else None
    except ValueError:
        up5y_num = None
    stress_frac = sp / st if st else 0.0

    # CSS classes
    verdict_cls = _VERDICT_CSS.get(sig, "verdict-hold")
    trap_cls, trap_label = _TRAP_CSS.get(trap_emoji, ("trap-watch", trap_emoji))

    # Upside cell color (matches hand-curated convention)
    if up_num >= 30:
        u_color = "#166534"  # deep green
    elif up_num >= 0:
        u_color = "#15803D"  # green
    else:
        u_color = "#991B1B"  # red
    up_sign = "+" if up_num > 0 else ""
    up_cell_text = f"{up_sign}{up_num:.0f}%" if upside else "?"

    # 5Y upside cell
    if up5y_num is not None:
        u5y_sign = "+" if up5y_num > 0 else ""
        if up5y_num >= 50:
            u5y_color = "#166534"
        elif up5y_num >= 0:
            u5y_color = "#15803D"
        else:
            u5y_color = "#991B1B"
        up5y_cell_text = f"{u5y_sign}{up5y_num:.0f}%"
    else:
        u5y_color = ""
        up5y_cell_text = "—"

    # Cell display values (fallback strings when missing)
    fpe_disp = f"{fpe}x" if fpe else "?"
    pct_disp = f"{pct}%" if pct else "?"
    peg_disp = f"{peg}" if peg else "?"
    triax_disp = f"{moat}/{val_emoji}/{ma_state}"
    stress_disp = f"{sp}/{st}"

    up5y_style = f"color:{u5y_color};font-weight:600" if u5y_color else "color:#94A3B8"
    up5y_num_attr = f"{up5y_num:.0f}" if up5y_num is not None else "0"

    return (
        f'<tr class="searchable" data-ticker="{entry["ticker"]}"'
        f' data-signal="{sig}" data-trap="{trap_emoji}"'
        f' data-rank="{rank}" data-trap-rank="{trap_rank}" data-quality="{quality}"'
        f' data-fpe="{fpe_num}" data-pct="{pct_num}" data-peg="{peg_num}"'
        f' data-upside="{up_num}" data-upside5y="{up5y_num_attr}" data-stress="{stress_frac}">\n'
        f'  <td><a href="{entry["href"]}" class="ticker-link" target="_blank" rel="noopener">{entry["ticker"]}</a></td>'
        f'<td><span class="{verdict_cls}"><strong>{sig}</strong></span></td>'
        f'<td><span class="{trap_cls}">{trap_label}</span></td>'
        f'<td class="num-cell">{triax_disp}</td>'
        f'<td class="num-cell">{fpe_disp}</td>'
        f'<td class="num-cell">{pct_disp}</td>'
        f'<td class="num-cell">{peg_disp}</td>'
        f'<td class="num-cell" style="color:{u_color};font-weight:600">{up_cell_text}</td>'
        f'<td class="num-cell" style="{up5y_style}">{up5y_cell_text}</td>'
        f'<td class="num-cell">{stress_disp}</td>\n'
        f'</tr>'
    )


def collect_v12_entries():
    """Walk INDEX.md + DD HTMLs and produce per-row v12 entries.

    Per-DD priority for field extraction:
      1) <script id="dd-meta" type="application/json"> block in DD HTML head
         (canonical, plan-A lasting fix; v12.1+ DDs emit this).
      2) INDEX.md rr_raw column (triax: moat / val / ma).
      3) Regex extractors over DD HTML body (legacy fallback).

    Only includes DDs where INDEX.md schema starts with 'v12'.
    """
    index_data = parse_index_md()
    entries = []
    for fname, md in index_data.items():
        if not md["schema"].startswith("v12"):
            continue
        path = DD_DIR / fname
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")

        # Priority 1: dd-meta JSON block (canonical) ---------------------------
        meta = extract_dd_meta_json(text)
        if meta:
            stress = meta.get("stress", {}) or {}
            entry = {
                "ticker": meta.get("ticker") or md["ticker"],
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
            "ticker": md["ticker"],
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
        })
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


def update_index_v12_full(html: str) -> tuple:
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

    entries = _sort_v12_entries(collect_v12_entries())
    rows = "\n".join(build_row_v12(e) for e in entries)
    new_block = open_tag + "\n" + rows + "\n" + close_tag
    new_html = html[:m.start()] + new_block + html[m.end():]
    return new_html, len(entries)


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


def update_index(entries, dry_run: bool = False):
    html = INDEX_HTML.read_text(encoding="utf-8")
    original_html = html

    # v12 mode: page uses <tbody id="dd-tbody-v12"> with rows that include
    # sortable data-* attrs (data-signal / data-fpe / data-pct / data-peg /
    # data-upside / data-stress) — schema incompatible with v11 build_rows().
    # Strategy: APPEND-ONLY. Add rows for v12 DDs not yet in the table; never
    # overwrite existing hand-curated rows so QA tweaks survive.
    v12_mode = '<tbody id="dd-tbody-v12">' in html
    if v12_mode:
        new_html, row_count = update_index_v12_full(html)
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
        from aggregate_dd_stats import load_records as _load_recs, render as _render_stats
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
        "--dry-run",
        action="store_true",
        help="Show unified diff of changes without writing the file.",
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

    if update_index(entries, dry_run=args.dry_run):
        if args.dry_run:
            print(f"\n(dry-run; no file written)")
        else:
            print(f"\nUpdated {INDEX_HTML}")
    else:
        print("\nFailed to update index.html")


if __name__ == "__main__":
    main()
