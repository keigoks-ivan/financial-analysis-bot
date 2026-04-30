#!/usr/bin/env python3
"""Backfill upside_5y_pct in dd-meta JSON blocks for all v12 DD HTML files.

Reads each DD HTML, finds the rr-long block, extracts the 5Y upside %, and
injects the value into the <script id="dd-meta"> JSON without re-sorting keys.

Usage:
  python3 scripts/backfill_upside_5y.py [--dry-run]
"""
import re
import sys
import glob
from pathlib import Path

ROOT = Path(__file__).parent.parent
DD_DIR = ROOT / "docs" / "dd"

DD_META_RE = re.compile(
    r'(<script\s+id="dd-meta"\s+type="application/json"\s*>)(.*?)(</script>)',
    re.DOTALL,
)

META_VERSION_RE = re.compile(
    r'<meta\s+name="dd-schema-version"\s+content="([^"]+)"', re.IGNORECASE
)


def extract_upside_5y(text: str):
    """Try to extract the 5Y upside percentage from the rr-long block.

    Returns a float (e.g. 106.0, -10.0) or None if not found.
    """
    # Find the rr-long block (skip CSS-definition lines)
    # The block is a <div ...rr-long...> element
    block_m = re.search(r'<div[^>]*rr-long[^>]*>(.*?)</div>', text, re.DOTALL)
    if not block_m:
        return None

    block = block_m.group(1)

    # Strategy 1: table row pattern
    # <tr><td>上行</td><td ...>+67%（5Y 累計）</td></tr>
    # <tr><td>上行空間</td><td ...>+30.3%</td></tr>
    # <tr><td>上行距離</td><td ...>+88.3%</td></tr>
    row_m = re.search(
        r'<td>上行[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
        block,
        re.DOTALL,
    )
    if row_m:
        val = row_m.group(1).strip()
        pct_m = re.search(r'([+\-−]?\d+(?:\.\d+)?)\s*%', val)
        if pct_m:
            raw = pct_m.group(1).replace('−', '-')
            return float(raw)

    # Strategy 2: inline format — 上行：+64%  /  上行: +172%  /  上行：+138%（5 年）
    inline_m = re.search(r'上行[：:]\s*([+\-−]?\d+(?:\.\d+)?)\s*%', block)
    if inline_m:
        raw = inline_m.group(1).replace('−', '-')
        return float(raw)

    # Strategy 3: "5 年上行：+21% to +45%"  → take the lower bound
    range_m = re.search(
        r'5\s*年上行[^+\-−\d]*([+\-−]?\d+(?:\.\d+)?)\s*%',
        block,
    )
    if range_m:
        raw = range_m.group(1).replace('−', '-')
        return float(raw)

    # Strategy 4: fallback — any % that appears within 80 chars after 上行
    fallback_m = re.search(r'上行.{0,80}?([+\-−]?\d+(?:\.\d+)?)\s*%', block, re.DOTALL)
    if fallback_m:
        raw = fallback_m.group(1).replace('−', '-')
        return float(raw)

    return None


def inject_upside(raw_json: str, value: float) -> str:
    """Insert  ,\n  "upside_5y_pct": VALUE  before the final } in the JSON text."""
    # Format: integer if .0, else float
    if value == int(value):
        formatted = str(int(value))
    else:
        formatted = str(value)

    # Find the last closing brace
    last_brace = raw_json.rfind('}')
    if last_brace == -1:
        raise ValueError("No closing } found in JSON block")

    insertion = f',\n  "upside_5y_pct": {formatted}'
    return raw_json[:last_brace] + insertion + raw_json[last_brace:]


def process_file(path: Path, dry_run: bool = False) -> dict:
    """Process one DD file. Returns a result dict."""
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except OSError as e:
        return {'status': 'read_error', 'reason': str(e)}

    # Only process v12 files
    version_m = META_VERSION_RE.search(text)
    version = version_m.group(1) if version_m else ''
    if not version.startswith('v12'):
        return {'status': 'non_v12', 'version': version}

    meta_m = DD_META_RE.search(text)
    if not meta_m:
        return {'status': 'no_meta_block'}

    raw_json = meta_m.group(2)

    # Skip if already has upside_5y_pct
    if '"upside_5y_pct"' in raw_json:
        return {'status': 'already_present'}

    # Extract 5Y upside from HTML
    value = extract_upside_5y(text)
    if value is None:
        return {'status': 'no_upside_found'}

    # Inject into JSON
    try:
        new_json = inject_upside(raw_json, value)
    except ValueError as e:
        return {'status': 'inject_error', 'reason': str(e)}

    new_meta_block = meta_m.group(1) + new_json + meta_m.group(3)
    new_text = text[:meta_m.start()] + new_meta_block + text[meta_m.end():]

    if not dry_run:
        path.write_text(new_text, encoding='utf-8')

    return {'status': 'updated', 'value': value}


def main():
    dry_run = '--dry-run' in sys.argv

    files = sorted(DD_DIR.glob('DD_*.html'))

    counts = {
        'total': 0,
        'non_v12': 0,
        'already_present': 0,
        'updated': 0,
        'no_upside_found': 0,
        'no_meta_block': 0,
        'error': 0,
    }

    no_upside_tickers = []
    updated_tickers = []
    error_files = []

    for path in files:
        counts['total'] += 1
        result = process_file(path, dry_run=dry_run)
        status = result['status']

        if status in ('non_v12', 'already_present', 'no_meta_block'):
            counts[status] = counts.get(status, 0) + 1
        elif status == 'updated':
            counts['updated'] += 1
            updated_tickers.append((path.name, result['value']))
        elif status == 'no_upside_found':
            counts['no_upside_found'] += 1
            # Extract ticker from dd-meta or filename for reporting
            try:
                text = path.read_text(encoding='utf-8', errors='ignore')
                ticker_m = re.search(r'"ticker"\s*:\s*"([^"]+)"', text)
                ticker = ticker_m.group(1) if ticker_m else path.stem
            except Exception:
                ticker = path.stem
            no_upside_tickers.append(ticker)
        else:
            counts['error'] += 1
            error_files.append((path.name, result))

    # Report
    prefix = '[DRY RUN] ' if dry_run else ''
    print(f'{prefix}=== backfill_upside_5y results ===')
    print(f'Total DD files scanned : {counts["total"]}')
    print(f'Non-v12 (skipped)      : {counts["non_v12"]}')
    print(f'Already had value      : {counts["already_present"]}')
    print(f'No dd-meta block       : {counts["no_meta_block"]}')
    print(f'Updated (5Y upside)    : {counts["updated"]}')
    print(f'No upside found (null) : {counts["no_upside_found"]}')
    if counts['error']:
        print(f'Errors                 : {counts["error"]}')
        for fname, r in error_files:
            print(f'  {fname}: {r}')

    if no_upside_tickers:
        print()
        print('Tickers with no 5Y upside (留空 null / no rr-long block):')
        for t in sorted(no_upside_tickers):
            print(f'  {t}')

    if updated_tickers:
        print()
        print('Updated:')
        for fname, val in updated_tickers:
            print(f'  {fname} -> {val}')


if __name__ == '__main__':
    main()
