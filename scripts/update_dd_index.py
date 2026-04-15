#!/usr/bin/env python3
"""
Scan docs/dd/ for DD_*.html files, cross-reference INDEX.md for v9.x metadata,
and update the deep research table in docs/research/index.html.

v9.1 update: Show all v9.x reports with version column.
Same ticker + same date + different versions can coexist.
"""
import re
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"
DD_DIR = DOCS / "dd"
INDEX_HTML = DOCS / "research" / "index.html"
INDEX_MD = DD_DIR / "INDEX.md"

META_RE = re.compile(
    r'<meta\s+name="dd-schema-version"\s+content="([^"]+)"', re.IGNORECASE
)

# Patterns to extract the bull one-liner from DD HTML (used as comment)
# "多頭最強一句話" variants:
#   1) ...一句話</strong>：text</p>       (strong before colon)
#   2) ...一句話：</strong>text</p>       (strong after colon)
#   3) ...一句話：text</p>               (no strong, e.g. bare <p> with style)
BULL_ONELINER_RE = re.compile(
    r'多頭最強一句話\s*(?:</(?:strong|b)>)?\s*[：:]\s*(?:</(?:strong|b)>)?\s*(.*?)</p>',
    re.DOTALL,
)
# "多頭最強論據" in table cell — handle optional <strong>/<b> wrapping
BULL_ARGUMENT_RE = re.compile(
    r'多頭最強論據\s*(?:</(?:strong|b)>)?\s*</td>\s*<td[^>]*>(.*?)</td>',
    re.DOTALL,
)
BULL_SHORT_RE = re.compile(
    r'多頭最強\s*(?:</(?:strong|b|td)>)\s*</td>\s*<td[^>]*>(.*?)</td>',
    re.DOTALL,
)
TAG_RE = re.compile(r'<[^>]+>')

# Pattern to extract numeric quality score from §7.7 A table
# Matches "綜合品質分" in a table row, then finds the first decimal number
# after closing tags. Handles <strong>, <b>, colspan variants, extra <td> cells.
QUALITY_SCORE_RE = re.compile(
    r'綜合品質分\s*(?:</(?:strong|b)>)?\s*</td>'
    r'(?:\s*<td[^>]*>\s*</td>)*'           # skip empty <td></td> cells
    r'\s*<td[^>]*>\s*(?:<(?:strong|b)[^>]*>)?\s*'
    r'([\d]+\.[\d]+)',
    re.DOTALL,
)

# Patterns to extract upside / downside from §7.7 H table
# Handle <tr> with optional class/style attributes
UPSIDE_RE = re.compile(
    r'<tr[^>]*>\s*<td[^>]*>上行空間</td>\s*<td[^>]*>(.*?)</td>', re.DOTALL
)
DOWNSIDE_RE = re.compile(
    r'<tr[^>]*>\s*<td[^>]*>下行距離</td>\s*<td[^>]*>(.*?)</td>', re.DOTALL
)
PCT_RE = re.compile(r'[+\-−]?\d+(?:\.\d+)?%')


def _extract_pct(html: str, pattern: re.Pattern) -> str:
    """Extract a percentage value from HTML using the given pattern."""
    m = pattern.search(html)
    if not m:
        return ""
    raw = TAG_RE.sub("", m.group(1)).strip()
    # Find the first percentage in the raw text
    pm = PCT_RE.search(raw)
    return pm.group(0).replace("−", "-") if pm else raw


def extract_updown(path: Path) -> tuple[str, str]:
    """Extract upside % and downside % from DD HTML §7.7 table."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ("", "")
    return (_extract_pct(text, UPSIDE_RE), _extract_pct(text, DOWNSIDE_RE))


def extract_quality_score(path: Path) -> str:
    """Extract numeric quality score (e.g. '8.60') from §7.7 A table."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = QUALITY_SCORE_RE.search(text)
    return m.group(1) if m else ""


def extract_version(path: Path) -> str:
    """Read <meta name="dd-schema-version" content="vX.Y"> from DD HTML head."""
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            head = fh.read(4096)
        m = META_RE.search(head)
        return m.group(1) if m else ""
    except OSError:
        return ""


def extract_comment(path: Path, max_len: int = 60) -> str:
    """Extract the bull one-liner from DD HTML as a short comment."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

    # Try "多頭最強一句話" paragraph first
    m = BULL_ONELINER_RE.search(text)
    if not m:
        # Fallback to "多頭最強論據" table cell
        m = BULL_ARGUMENT_RE.search(text)
    if not m:
        # Fallback to "多頭最強" short form
        m = BULL_SHORT_RE.search(text)
    if not m:
        return ""

    raw = TAG_RE.sub("", m.group(1)).strip()
    # Truncate with ellipsis
    if len(raw) > max_len:
        raw = raw[:max_len].rstrip("，。、；") + "…"
    return raw


def parse_index_md() -> dict:
    """Parse INDEX.md and return a dict keyed by filename with v9.x/v10.x metadata."""
    data = {}
    if not INDEX_MD.exists():
        return data
    for line in INDEX_MD.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if "v9" not in line and "v10" not in line:
            continue
        cols = [c.strip() for c in line.split("|")]
        # cols: ['', date, ticker, schema, verdict, trap, rr, filename, '']
        if len(cols) < 9:
            continue
        date, ticker, schema, verdict, trap, rr, filename = cols[1:8]
        if not (schema.startswith("v9") or schema.startswith("v10")):
            continue
        data[filename] = {
            "date": date,
            "ticker": ticker,
            "schema": schema,
            "verdict": verdict,
            "trap": trap,
            "rr_raw": rr,
            "filename": filename,
        }
        # Parse R:R field: "H / 2.4x / 0"
        rr_parts = [p.strip() for p in rr.split("/")]
        if len(rr_parts) == 3:
            data[filename]["quality"] = rr_parts[0]
            data[filename]["rr_value"] = rr_parts[1]
            data[filename]["red_lights"] = rr_parts[2]
        else:
            data[filename]["quality"] = rr
            data[filename]["rr_value"] = ""
            data[filename]["red_lights"] = ""
    return data


def scan_v9_files(index_data: dict):
    """Build entries list for v9.x DDs, enriched with INDEX.md metadata."""
    entries = []
    for f in sorted(DD_DIR.glob("DD_*.html")):
        version = extract_version(f)
        if not (version.startswith("v9") or version.startswith("v10")):
            continue
        # Support: DD_TICKER_DATE.html, DD_TICKER_DATE_v2.html, DD_TICKER_v10_DATE.html
        m = re.match(r"DD_(.+?)_(\d{4})(\d{2})(\d{2})(?:_v\d+)?\.html", f.name)
        if not m:
            # Try alternate pattern: DD_TICKER_vNN_DATE.html
            m = re.match(r"DD_(.+?)_v\d+_(\d{4})(\d{2})(\d{2})\.html", f.name)
        if not m:
            continue
        ticker = m.group(1)
        date_str = f"{m.group(2)}-{m.group(3)}-{m.group(4)}"

        md = index_data.get(f.name, {})
        comment = extract_comment(f)
        upside, downside = extract_updown(f)
        qscore = extract_quality_score(f)
        entries.append({
            "ticker": ticker,
            "date": date_str,
            "version": version,
            "href": f"/dd/{f.name}",
            "verdict": md.get("verdict", "—"),
            "trap": md.get("trap", "—"),
            "quality": md.get("quality", "—"),
            "quality_score": qscore,
            "rr_value": md.get("rr_value", "—"),
            "red_lights": md.get("red_lights", "—"),
            "upside": upside,
            "downside": downside,
            "comment": comment,
        })

    # Sort: date desc, then ticker asc, then version desc (v9.1 before v9.0)
    entries.sort(key=lambda e: e["ticker"])
    entries.sort(key=lambda e: e["version"], reverse=True)
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries


def verdict_badge(v: str) -> str:
    v = v.strip()
    if v == "進場":
        return '<span class="verdict-badge verdict-buy">進場</span>'
    elif v == "觀望":
        return '<span class="verdict-badge verdict-watch">觀望</span>'
    elif v == "迴避":
        return '<span class="verdict-badge verdict-avoid">迴避</span>'
    return v


def quality_badge(q: str, score: str = "") -> str:
    q = q.strip()
    labels = {"H": "H 高品質", "MH": "MH 中高", "M": "M 中品質", "W": "W 觀望"}
    colors = {
        "H": "quality-h",
        "MH": "quality-mh",
        "M": "quality-m",
        "W": "quality-w",
    }
    label = labels.get(q, q)
    cls = colors.get(q, "quality-m")
    score_str = f' <span class="quality-score">{score}</span>' if score else ""
    return f'<span class="quality-badge {cls}">{label}</span>{score_str}'


def rr_badge(rr: str) -> str:
    rr = rr.strip()
    if rr in ("neg", "—", ""):
        return '<span class="rr-neg">neg</span>'
    try:
        val = float(rr.replace("x", ""))
        if val >= 2.5:
            return f'<span class="rr-pass">{rr}</span>'
        elif val >= 1.0:
            return f'<span class="rr-mid">{rr}</span>'
        else:
            return f'<span class="rr-fail">{rr}</span>'
    except ValueError:
        return rr


def updown_badge(val: str, is_upside: bool = True) -> str:
    """Format upside/downside percentage with color coding."""
    val = val.strip()
    if not val:
        return '<span class="ud-na">—</span>'
    # Parse numeric value
    try:
        num = float(val.replace("%", "").replace("+", "").replace("−", "-"))
    except ValueError:
        return f'<span class="ud-na">{val}</span>'
    if is_upside:
        if num >= 100:
            cls = "ud-up-strong"
        elif num >= 30:
            cls = "ud-up"
        elif num > 0:
            cls = "ud-up-weak"
        else:
            cls = "ud-negative"
    else:
        # downside: higher magnitude = worse
        if abs(num) >= 70:
            cls = "ud-down-severe"
        elif abs(num) >= 50:
            cls = "ud-down"
        else:
            cls = "ud-down-mild"
    return f'<span class="{cls}">{val}</span>'


def red_light_display(r: str) -> str:
    r = r.strip()
    if r in ("0", ""):
        return '<span class="rl-0">0</span>'
    elif r == "1":
        return '<span class="rl-1">1</span>'
    elif r == "2":
        return '<span class="rl-2">2</span>'
    else:
        return f'<span class="rl-3">{r}</span>'


def trap_short(t: str) -> str:
    t = t.strip()
    if "非陷阱" in t:
        return '<span class="trap-ok">非陷阱</span>'
    elif "觀察期" in t:
        return '<span class="trap-watch">觀察期</span>'
    elif "高風險" in t:
        return '<span class="trap-danger">高風險</span>'
    return t


def _sort_keys(e):
    """Compute numeric sort keys for data attributes."""
    # Use negative quality_score for sort (higher score = sort first = lower number)
    qs = e.get("quality_score", "")
    try:
        q_sort = -float(qs)  # negative so higher scores sort first (ascending)
    except (ValueError, TypeError):
        q_map_fallback = {"H": 1, "MH": 2, "M": 3, "W": 4}
        q_sort = q_map_fallback.get(e.get("quality", "").strip(), 9)
    q_map = {"H": 1, "MH": 2, "M": 3, "W": 4}
    v_map = {"進場": 1, "觀望": 2, "迴避": 3}
    t_map = {}  # trap
    trap = e.get("trap", "")
    if "非陷阱" in trap:
        t_val = 1
    elif "觀察期" in trap:
        t_val = 2
    else:
        t_val = 3

    rr_raw = e.get("rr_value", "").strip()
    try:
        rr_num = float(rr_raw.replace("x", ""))
    except (ValueError, AttributeError):
        rr_num = -999

    rl_raw = e.get("red_lights", "").strip()
    try:
        rl_num = int(rl_raw)
    except (ValueError, AttributeError):
        rl_num = 0

    def _parse_pct(s):
        try:
            return float(s.strip().replace("%", "").replace("+", "").replace("−", "-"))
        except (ValueError, AttributeError):
            return -999

    return {
        "quality": q_sort,
        "verdict": v_map.get(e.get("verdict", "").strip(), 9),
        "rr": rr_num,
        "rl": rl_num,
        "trap": t_val,
        "upside": _parse_pct(e.get("upside", "")),
        "downside": _parse_pct(e.get("downside", "")),
    }


def version_badge(v: str) -> str:
    v = v.strip()
    if v.startswith("v10") or v == "v9.2":
        return f'<span class="version-badge version-latest">{v}</span>'
    return f'<span class="version-badge">{v}</span>'


def build_rows(entries):
    rows = []
    for e in entries:
        sk = _sort_keys(e)
        rows.append(
            f'<tr class="searchable"'
            f' data-ticker="{e["ticker"]}"'
            f' data-date="{e["date"]}"'
            f' data-version="{e.get("version", "")}"'
            f' data-verdict="{sk["verdict"]}"'
            f' data-quality="{sk["quality"]}"'
            f' data-rr="{sk["rr"]}"'
            f' data-upside="{sk["upside"]}"'
            f' data-downside="{sk["downside"]}"'
            f' data-rl="{sk["rl"]}"'
            f' data-trap="{sk["trap"]}"'
            f'>\n'
            f'  <td><a href="{e["href"]}" class="ticker-link">{e["ticker"]}</a></td>\n'
            f'  <td class="date-cell">{e["date"]}</td>\n'
            f'  <td>{version_badge(e.get("version", ""))}</td>\n'
            f'  <td>{verdict_badge(e["verdict"])}</td>\n'
            f'  <td>{quality_badge(e["quality"], e.get("quality_score", ""))}</td>\n'
            f'  <td>{rr_badge(e["rr_value"])}</td>\n'
            f'  <td class="updown-cell">{updown_badge(e["upside"], True)}</td>\n'
            f'  <td class="updown-cell">{updown_badge(e["downside"], False)}</td>\n'
            f'  <td>{red_light_display(e["red_lights"])}</td>\n'
            f'  <td>{trap_short(e["trap"])}</td>\n'
            f'  <td class="comment-cell">{e["comment"]}</td>\n'
            f'</tr>'
        )
    return "\n".join(rows)


def update_index(entries):
    html = INDEX_HTML.read_text(encoding="utf-8")

    # Replace thead
    new_thead = (
        '<thead>\n'
        '          <tr>\n'
        '            <th class="sortable" data-sort="ticker">公司</th>\n'
        '            <th class="sortable" data-sort="date">日期</th>\n'
        '            <th class="sortable" data-sort="version">版本</th>\n'
        '            <th class="sortable" data-sort="verdict">建議</th>\n'
        '            <th class="sortable sorted-asc" data-sort="quality">品質</th>\n'
        '            <th class="sortable" data-sort="rr">R:R</th>\n'
        '            <th class="sortable" data-sort="upside">上檔</th>\n'
        '            <th class="sortable" data-sort="downside">下檔</th>\n'
        '            <th class="sortable" data-sort="rl">紅燈</th>\n'
        '            <th class="sortable" data-sort="trap">陷阱</th>\n'
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
        print(f"ERROR: Could not find <tbody id=\"dd-tbody\"> in {INDEX_HTML}")
        return False

    # Inject custom CSS for badges if not already present
    if "verdict-badge" not in new_html:
        badge_css = """
/* v9.0 Badge Styles */
.verdict-badge{display:inline-block;padding:.2rem .6rem;border-radius:5px;font-size:.75rem;font-weight:600;letter-spacing:.01em}
.verdict-buy{background:rgba(5,150,105,.08);color:#059669}
.verdict-watch{background:rgba(217,119,6,.08);color:#d97706}
.verdict-avoid{background:rgba(220,38,38,.07);color:#dc2626}
.quality-badge{display:inline-block;padding:.15rem .5rem;border-radius:4px;font-size:.72rem;font-weight:600}
.quality-h{background:#dbeafe;color:#1e40af}
.quality-mh{background:#ede9fe;color:#5b21b6}
.quality-m{background:#f1f5f9;color:#475569}
.quality-w{background:rgba(220,38,38,.07);color:#991b1b}
.quality-score{font-family:'IBM Plex Mono',monospace;font-size:.72rem;font-weight:700;color:#64748b;margin-left:2px}
.rr-pass{color:#059669;font-weight:700;font-family:'IBM Plex Mono',monospace;font-size:.85rem}
.rr-mid{color:#d97706;font-weight:600;font-family:'IBM Plex Mono',monospace;font-size:.85rem}
.rr-fail{color:#dc2626;font-weight:600;font-family:'IBM Plex Mono',monospace;font-size:.85rem}
.rr-neg{color:#94a3b8;font-style:italic;font-family:'IBM Plex Mono',monospace;font-size:.85rem}
.rl-0{color:#059669;font-weight:600;font-family:'IBM Plex Mono',monospace}
.rl-1{color:#d97706;font-weight:600;font-family:'IBM Plex Mono',monospace}
.rl-2{color:#ea580c;font-weight:700;font-family:'IBM Plex Mono',monospace}
.rl-3{color:#dc2626;font-weight:700;font-family:'IBM Plex Mono',monospace}
.trap-ok{color:#059669;font-size:.8rem}.trap-watch{color:#d97706;font-size:.8rem}
.trap-danger{color:#dc2626;font-weight:700;font-size:.8rem}
.updown-cell{font-family:'IBM Plex Mono',monospace;font-size:.82rem;font-weight:600;white-space:nowrap}
.ud-up-strong{color:#059669}.ud-up{color:#059669}.ud-up-weak{color:#6b7280}.ud-negative{color:#dc2626}
.ud-down-severe{color:#dc2626}.ud-down{color:#ea580c}.ud-down-mild{color:#d97706}.ud-na{color:#94a3b8}
.comment-cell{color:#475569;font-size:.78rem;max-width:260px;line-height:1.45}
.version-badge{display:inline-block;padding:.1rem .4rem;border-radius:3px;font-size:.7rem;font-family:'IBM Plex Mono',monospace;background:#f1f5f9;color:#64748b}
.version-latest{background:#dbeafe;color:#1e40af;font-weight:600}
td a.ticker-link{color:#1e293b;text-decoration:none;font-weight:700;font-size:.88rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.02em;transition:color .15s}
td a.ticker-link:hover{color:#2563eb}
td.date-cell{color:#94a3b8;font-family:'IBM Plex Mono',monospace;font-size:.8rem;white-space:nowrap}
"""
        new_html = new_html.replace("</style>", badge_css + "</style>", 1)

    INDEX_HTML.write_text(new_html, encoding="utf-8")
    return True


def main():
    index_data = parse_index_md()
    entries = scan_v9_files(index_data)
    print(f"Found {len(entries)} v9.x/v10.x DD files:")
    for e in entries:
        print(f"  {e['ticker']:8s} {e['date']}  {e['verdict']:4s}  {e['quality']:3s}  {e['rr_value']:6s}  {e['href']}")

    if update_index(entries):
        print(f"\nUpdated {INDEX_HTML}")
    else:
        print("\nFailed to update index.html")


if __name__ == "__main__":
    main()
