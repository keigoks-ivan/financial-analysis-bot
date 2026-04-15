#!/usr/bin/env python3
"""
Scan docs/dd/ for DD_*.html files, cross-reference INDEX.md for v9.x/v10.x metadata,
and update the deep research table in docs/research/index.html.

v10.0 update: Remove R:R/上檔/下檔/紅燈 columns, add 長期持有信心 column.
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
BULL_ONELINER_RE = re.compile(
    r'多頭最強一句話\s*(?:</(?:strong|b)>)?\s*[：:]\s*(?:</(?:strong|b)>)?\s*(.*?)</p>',
    re.DOTALL,
)
BULL_ARGUMENT_RE = re.compile(
    r'多頭最強論據\s*(?:</(?:strong|b)>)?\s*</td>\s*<td[^>]*>(.*?)</td>',
    re.DOTALL,
)
BULL_SHORT_RE = re.compile(
    r'多頭最強\s*(?:</(?:strong|b|td)>)\s*</td>\s*<td[^>]*>(.*?)</td>',
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

# Pattern to extract 長期持有信心 (v10.0+): 高/中/低
# Matches table row with 長期持有信心 and extracts the value cell
CONFIDENCE_RE = re.compile(
    r'長期持有信心\s*(?:</(?:strong|b)>)?\s*</td>'
    r'(?:\s*<td[^>]*>.*?</td>)*?'  # skip intermediate cells (e.g. "綜合判斷")
    r'\s*<td[^>]*>\s*(?:<[^>]*>)*\s*(高|中|低)',
    re.DOTALL,
)


def extract_quality_score(path: Path) -> str:
    """Extract numeric quality score (e.g. '8.60') from DD HTML."""
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

    m = BULL_ONELINER_RE.search(text)
    if not m:
        m = BULL_ARGUMENT_RE.search(text)
    if not m:
        m = BULL_SHORT_RE.search(text)
    if not m:
        return ""

    raw = TAG_RE.sub("", m.group(1)).strip()
    if len(raw) > max_len:
        raw = raw[:max_len].rstrip("，。、；") + "…"
    return raw


def extract_confidence(path: Path) -> str:
    """Extract 長期持有信心 (高/中/低) from DD HTML. v10.0+ only."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = CONFIDENCE_RE.search(text)
    return m.group(1) if m else ""


def parse_index_md() -> dict:
    """Parse INDEX.md and return a dict keyed by filename with metadata."""
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
        if not (version.startswith("v9") or version.startswith("v10")):
            continue
        m = re.match(r"DD_(.+?)_(\d{4})(\d{2})(\d{2})(?:_v\d+)?\.html", f.name)
        if not m:
            m = re.match(r"DD_(.+?)_v\d+_(\d{4})(\d{2})(\d{2})\.html", f.name)
        if not m:
            continue
        ticker = m.group(1)
        date_str = f"{m.group(2)}-{m.group(3)}-{m.group(4)}"

        md = index_data.get(f.name, {})
        comment = extract_comment(f)
        qscore = extract_quality_score(f)
        confidence = extract_confidence(f)
        entries.append({
            "ticker": ticker,
            "date": date_str,
            "version": version,
            "href": f"/dd/{f.name}",
            "verdict": md.get("verdict", "—"),
            "trap": md.get("trap", "—"),
            "quality": md.get("quality", "—"),
            "quality_score": qscore,
            "confidence": confidence,
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
    elif v == "觀望":
        return '<span class="verdict-badge verdict-watch">觀望</span>'
    elif v == "迴避":
        return '<span class="verdict-badge verdict-avoid">迴避</span>'
    return v


def quality_badge(q: str, score: str = "") -> str:
    q = q.strip()
    labels = {"H": "H 高品質", "MH": "MH 中高", "M": "M 中品質", "W": "W 觀望", "A": "A 級", "B": "B 級"}
    colors = {"H": "quality-h", "MH": "quality-mh", "M": "quality-m", "W": "quality-w", "A": "quality-h", "B": "quality-mh"}
    label = labels.get(q, q)
    cls = colors.get(q, "quality-m")
    score_str = f' <span class="quality-score">{score}</span>' if score else ""
    return f'<span class="quality-badge {cls}">{label}</span>{score_str}'


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
    if v.startswith("v10") or v == "v9.2":
        return f'<span class="version-badge version-latest">{v}</span>'
    return f'<span class="version-badge">{v}</span>'


def _sort_keys(e):
    qs = e.get("quality_score", "")
    try:
        q_sort = -float(qs)
    except (ValueError, TypeError):
        q_map_fallback = {"H": 1, "MH": 2, "M": 3, "W": 4, "A": 0, "B": 2}
        q_sort = q_map_fallback.get(e.get("quality", "").strip(), 9)
    v_map = {"進場": 1, "觀望": 2, "迴避": 3}
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
        rows.append(
            f'<tr class="searchable"'
            f' data-ticker="{e["ticker"]}"'
            f' data-date="{e["date"]}"'
            f' data-version="{e.get("version", "")}"'
            f' data-verdict="{sk["verdict"]}"'
            f' data-quality="{sk["quality"]}"'
            f' data-trap="{sk["trap"]}"'
            f' data-confidence="{sk["confidence"]}"'
            f'>\n'
            f'  <td><a href="{e["href"]}" class="ticker-link">{e["ticker"]}</a></td>\n'
            f'  <td class="date-cell">{e["date"]}</td>\n'
            f'  <td>{version_badge(e.get("version", ""))}</td>\n'
            f'  <td>{verdict_badge(e["verdict"])}</td>\n'
            f'  <td>{quality_badge(e["quality"], e.get("quality_score", ""))}</td>\n'
            f'  <td>{trap_short(e["trap"])}</td>\n'
            f'  <td>{confidence_badge(e.get("confidence", ""))}</td>\n'
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
        print(f"ERROR: Could not find <tbody id=\"dd-tbody\"> in {INDEX_HTML}")
        return False

    # Inject/update badge CSS
    badge_css = """
/* v10.0 Badge Styles */
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
.trap-ok{color:#059669;font-size:.8rem}.trap-watch{color:#d97706;font-size:.8rem}
.trap-danger{color:#dc2626;font-weight:700;font-size:.8rem}
.conf-high{color:#059669;font-weight:700;font-size:.82rem}
.conf-mid{color:#d97706;font-weight:600;font-size:.82rem}
.conf-low{color:#dc2626;font-weight:600;font-size:.82rem}
.conf-na{color:#94a3b8;font-size:.82rem}
.comment-cell{color:#475569;font-size:.78rem;max-width:260px;line-height:1.45}
.version-badge{display:inline-block;padding:.1rem .4rem;border-radius:3px;font-size:.7rem;font-family:'IBM Plex Mono',monospace;background:#f1f5f9;color:#64748b}
.version-latest{background:#dbeafe;color:#1e40af;font-weight:600}
td a.ticker-link{color:#1e293b;text-decoration:none;font-weight:700;font-size:.88rem;font-family:'IBM Plex Mono',monospace;letter-spacing:.02em;transition:color .15s}
td a.ticker-link:hover{color:#2563eb}
td.date-cell{color:#94a3b8;font-family:'IBM Plex Mono',monospace;font-size:.8rem;white-space:nowrap}
"""
    # Remove old badge CSS block and inject new one
    new_html = re.sub(
        r'/\* v9\.0 Badge Styles \*/.*?(?=</style>)',
        badge_css,
        new_html,
        count=1,
        flags=re.DOTALL,
    )
    if "v10.0 Badge Styles" not in new_html:
        # Fallback: just inject before </style>
        new_html = new_html.replace("</style>", badge_css + "</style>", 1)

    INDEX_HTML.write_text(new_html, encoding="utf-8")
    return True


def main():
    index_data = parse_index_md()
    entries = scan_files(index_data)
    print(f"Found {len(entries)} v9.x/v10.x DD files:")
    for e in entries:
        conf = e.get("confidence", "—") or "—"
        print(f"  {e['ticker']:8s} {e['date']}  {e['verdict']:4s}  {e['quality']:3s}  conf={conf}  {e['href']}")

    if update_index(entries):
        print(f"\nUpdated {INDEX_HTML}")
    else:
        print("\nFailed to update index.html")


if __name__ == "__main__":
    main()
