#!/usr/bin/env python3
"""
Scan docs/dd/ for DD_*.html files, cross-reference INDEX.md for v9.0 metadata,
and update the deep research table in docs/research/index.html.

v9.0 update: Only show v9.0 reports. Display verdict, quality grade, R:R,
red lights, trap assessment from INDEX.md.
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
    r'多頭最強一句話</strong>[：:]\s*(.*?)</p>', re.DOTALL
)
BULL_ARGUMENT_RE = re.compile(
    r'多頭最強論據</td>\s*<td>(.*?)</td>', re.DOTALL
)
BULL_SHORT_RE = re.compile(
    r'多頭最強</(?:strong|td)>\s*</td>\s*<td>(.*?)</td>', re.DOTALL
)
TAG_RE = re.compile(r'<[^>]+>')


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
    """Parse INDEX.md and return a dict keyed by filename with v9.0 metadata."""
    data = {}
    if not INDEX_MD.exists():
        return data
    for line in INDEX_MD.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or "v9.0" not in line:
            continue
        cols = [c.strip() for c in line.split("|")]
        # cols: ['', date, ticker, schema, verdict, trap, rr, filename, '']
        if len(cols) < 9:
            continue
        date, ticker, schema, verdict, trap, rr, filename = cols[1:8]
        if schema != "v9.0":
            continue
        data[filename] = {
            "date": date,
            "ticker": ticker,
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
    """Build entries list for v9.0 DDs only, enriched with INDEX.md metadata."""
    entries = []
    for f in sorted(DD_DIR.glob("DD_*.html")):
        version = extract_version(f)
        if version != "v9.0":
            continue
        m = re.match(r"DD_(.+)_(\d{4})(\d{2})(\d{2})\.html", f.name)
        if not m:
            continue
        ticker = m.group(1)
        date_str = f"{m.group(2)}-{m.group(3)}-{m.group(4)}"

        md = index_data.get(f.name, {})
        comment = extract_comment(f)
        entries.append({
            "ticker": ticker,
            "date": date_str,
            "href": f"/dd/{f.name}",
            "verdict": md.get("verdict", "—"),
            "trap": md.get("trap", "—"),
            "quality": md.get("quality", "—"),
            "rr_value": md.get("rr_value", "—"),
            "red_lights": md.get("red_lights", "—"),
            "comment": comment,
        })

    # Sort: date desc, then ticker asc
    entries.sort(key=lambda e: e["ticker"])
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


def quality_badge(q: str) -> str:
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
    return f'<span class="quality-badge {cls}">{label}</span>'


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

    return {
        "quality": q_map.get(e.get("quality", "").strip(), 9),
        "verdict": v_map.get(e.get("verdict", "").strip(), 9),
        "rr": rr_num,
        "rl": rl_num,
        "trap": t_val,
    }


def build_rows(entries):
    rows = []
    for e in entries:
        sk = _sort_keys(e)
        rows.append(
            f'<tr class="searchable"'
            f' data-ticker="{e["ticker"]}"'
            f' data-date="{e["date"]}"'
            f' data-verdict="{sk["verdict"]}"'
            f' data-quality="{sk["quality"]}"'
            f' data-rr="{sk["rr"]}"'
            f' data-rl="{sk["rl"]}"'
            f' data-trap="{sk["trap"]}"'
            f'>\n'
            f'  <td><a href="{e["href"]}" class="ticker-link">{e["ticker"]}</a></td>\n'
            f'  <td class="date-cell">{e["date"]}</td>\n'
            f'  <td>{verdict_badge(e["verdict"])}</td>\n'
            f'  <td>{quality_badge(e["quality"])}</td>\n'
            f'  <td>{rr_badge(e["rr_value"])}</td>\n'
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
        '            <th class="sortable" data-sort="verdict">建議</th>\n'
        '            <th class="sortable sorted-asc" data-sort="quality">品質</th>\n'
        '            <th class="sortable" data-sort="rr">R:R</th>\n'
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
.comment-cell{color:#475569;font-size:.78rem;max-width:260px;line-height:1.45}
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
    print(f"Found {len(entries)} v9.0 DD files:")
    for e in entries:
        print(f"  {e['ticker']:8s} {e['date']}  {e['verdict']:4s}  {e['quality']:3s}  {e['rr_value']:6s}  {e['href']}")

    if update_index(entries):
        print(f"\nUpdated {INDEX_HTML}")
    else:
        print("\nFailed to update index.html")


if __name__ == "__main__":
    main()
