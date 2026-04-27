"""Reusable dd-meta JSON reader for v12+ DD HTML files.

This module is the canonical way for any consumer (research index sync,
portfolio-manager skill, morning-briefing, custom analysis scripts) to
read structured metadata from DD HTML files. It replaces ad-hoc regex
parsing of HTML body content.

Stdlib-only (no third-party deps) — safe to copy/import from any repo.

Public API:

  read_dd_meta(path) -> dict | None
      Parse one DD HTML file, return its dd-meta JSON dict (or None if
      missing / unparseable).

  iter_dd_metas(dd_dir) -> Iterator[(Path, dict)]
      Yield (path, meta) for every DD in dd_dir that has a valid
      dd-meta block. Skips files without it. Useful for batch analysis.

  filter_v12(metas) -> list[dict]
      Keep only entries whose schema starts with 'v12'.

  latest_per_ticker(metas) -> list[dict]
      Dedupe by ticker, keeping the most recent date per ticker.

Example (morning-briefing earnings-driven re-eval):

  from dd_meta_reader import iter_dd_metas, latest_per_ticker
  metas = [m for _, m in iter_dd_metas("/path/to/financial-analysis-bot/docs/dd")]
  latest = latest_per_ticker(metas)
  for m in latest:
      if m['ticker'] in earnings_today and m['signal'] in ('A', 'A+'):
          print(f"{m['ticker']}: signal {m['signal']}, mid R:R {m['upside_mid_pct']}%")
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterator, Optional

__all__ = [
    "read_dd_meta",
    "iter_dd_metas",
    "filter_v12",
    "latest_per_ticker",
    # Industry DD (ID) helpers
    "read_id_meta",
    "iter_id_metas",
    "find_ids_for_ticker",
]

_DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)


def read_dd_meta(path: str | Path) -> Optional[dict]:
    """Return parsed dd-meta dict for one DD HTML, or None if absent / invalid."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = _DD_META_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None


def iter_dd_metas(dd_dir: str | Path) -> Iterator[tuple[Path, dict]]:
    """Yield (path, meta) for every DD HTML in dd_dir with a valid dd-meta block.

    DDs without a dd-meta block are silently skipped — use validate_dd_meta.py
    to surface those gaps.
    """
    d = Path(dd_dir)
    for p in sorted(d.glob("DD_*.html")):
        meta = read_dd_meta(p)
        if meta is not None:
            yield p, meta


def filter_v12(metas: list[dict]) -> list[dict]:
    """Keep only entries whose schema starts with 'v12'."""
    return [m for m in metas if str(m.get("schema", "")).startswith("v12")]


def latest_per_ticker(metas: list[dict]) -> list[dict]:
    """Dedupe by ticker, keeping the most recent date. Inputs missing
    'ticker' or 'date' are dropped."""
    latest: dict[str, dict] = {}
    for m in metas:
        t, d = m.get("ticker"), m.get("date")
        if not t or not d:
            continue
        prev = latest.get(t)
        if prev is None or d > prev["date"]:
            latest[t] = m
    return list(latest.values())


# === Industry DD (ID) =========================================================

_ID_META_RE = re.compile(
    r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)


def read_id_meta(path: str | Path) -> Optional[dict]:
    """Return parsed id-meta dict for one ID HTML, or None if absent / invalid.

    The ID schema is sector-focused (theme, related_tickers, TAM, CAGR, ...)
    rather than ticker-focused. Schema definition is in
    scripts/validate_id_meta.py REQUIRED_FIELDS.
    """
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = _ID_META_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None


def iter_id_metas(id_dir: str | Path) -> Iterator[tuple[Path, dict]]:
    """Yield (path, meta) for every ID HTML in id_dir with a valid id-meta block."""
    d = Path(id_dir)
    for p in sorted(d.glob("ID_*.html")):
        meta = read_id_meta(p)
        if meta is not None:
            yield p, meta


def find_ids_for_ticker(id_dir: str | Path, ticker: str) -> list[tuple[Path, dict]]:
    """Find all IDs whose related_tickers list contains the given ticker.

    Returns [(path, meta), ...] for IDs where any related_tickers[].ticker
    matches (case-insensitive). Useful for stock-analyst skill §11 cross-reference.

    Example:
        for path, idm in find_ids_for_ticker(ID_DIR, "AVGO"):
            print(f"{path.name}: theme={idm['theme']}")
    """
    target = ticker.strip().upper()
    out: list[tuple[Path, dict]] = []
    for path, meta in iter_id_metas(id_dir):
        rt = meta.get("related_tickers") or []
        for entry in rt:
            t = (entry.get("ticker") or "").strip().upper()
            if t == target:
                out.append((path, meta))
                break
    return out
