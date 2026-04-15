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

# Pattern to extract 護城河 score from §2 B table (§9 or §10 評分 row)
MOAT_SCORE_RE = re.compile(
    r'護城河\s*</td>\s*<td[^>]*>\s*§(?:9|10)\b[^<]*</td>\s*<td[^>]*>\s*(?:<[^>]+>)?\s*(\d+)',
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


def extract_comment(path: Path, max_len: int = 500) -> str:
    """Extract the bull one-liner from DD HTML as a short comment."""
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
        if not any(f"v{n}" in line for n in range(9, 20)):
            continue
        cols = [c.strip() for c in line.split("|")]
        # cols: ['', date, ticker, schema, verdict, trap, rr, filename, '']
        if len(cols) < 9:
            continue
        date, ticker, schema, verdict, trap, rr, filename = cols[1:8]
        if not any(schema.startswith(f"v{n}") for n in range(9, 20)):
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
        comment = extract_comment(f)
        qscore = extract_quality_score(f)
        moat = extract_moat_score(f)
        moat_trend = extract_moat_trend(f)
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
            "moat_score": moat,
            "moat_trend": moat_trend,
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
            f'  <td><a href="{e["href"]}" class="ticker-link" target="_blank" rel="noopener">{e["ticker"]}</a></td>\n'
            f'  <td class="date-cell">{e["date"]}</td>\n'
            f'  <td>{version_badge(e.get("version", ""))}</td>\n'
            f'  <td>{verdict_badge(e["verdict"])}</td>\n'
            f'  <td>{quality_badge(e["quality"], e.get("quality_score", ""), e.get("moat_score", ""), e.get("moat_trend", ""))}</td>\n'
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
        '            <th class="sortable sorted-asc" data-sort="quality">護城河</th>\n'
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

    # Remove legacy injected CSS blocks (styles are now in the HTML template)
    new_html = re.sub(
        r'\n?/\* v(?:9|10)\.0 Badge Styles \*/.*?(?=</style>)',
        '\n',
        new_html,
        count=1,
        flags=re.DOTALL,
    )

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
