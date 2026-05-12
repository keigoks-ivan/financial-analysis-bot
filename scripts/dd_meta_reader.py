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
    # Industry Discourse (DS) helpers
    "read_ds_meta",
    "iter_ds_metas",
    "find_ds_for_ticker",
    # Unified ID + DS helpers (DS reuse same taxonomy / cross-link mechanism)
    "find_research_for_ticker",
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


# === Industry Discourse (DS) =================================================
# Sibling to ID — same sector taxonomy + §11 ticker hook, different analytical
# structure (narrative-led supply/demand cycle vs ID's table-led dashboard).
# Same theme can have both ID and DS co-existing.

_DS_META_RE = re.compile(
    r'<script\s+id="ds-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)


def read_ds_meta(path: str | Path) -> Optional[dict]:
    """Return parsed ds-meta dict for one DS HTML, or None if absent / invalid.

    The DS schema mirrors ID's sector-taxonomy fields (theme, related_tickers,
    mega, sub_group) and adds DS-specific fields (ds_version, history_window_years,
    forecast_horizon_years, related_ids). See scripts/validate_ds_meta.py.
    """
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = _DS_META_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None


def iter_ds_metas(ds_dir: str | Path) -> Iterator[tuple[Path, dict]]:
    """Yield (path, meta) for every DS HTML in ds_dir with a valid ds-meta block."""
    d = Path(ds_dir)
    for p in sorted(d.glob("DS_*.html")):
        meta = read_ds_meta(p)
        if meta is not None:
            yield p, meta


def find_ds_for_ticker(ds_dir: str | Path, ticker: str) -> list[tuple[Path, dict]]:
    """Find all DS reports whose related_tickers list contains the given ticker.

    Mirror of find_ids_for_ticker but for DS. Returns [(path, meta), ...].
    """
    target = ticker.strip().upper()
    out: list[tuple[Path, dict]] = []
    for path, meta in iter_ds_metas(ds_dir):
        rt = meta.get("related_tickers") or []
        for entry in rt:
            t = (entry.get("ticker") or "").strip().upper()
            if t == target:
                out.append((path, meta))
                break
    return out


# === Unified ID + DS helpers =================================================


def find_research_for_ticker(
    id_dir: str | Path,
    ds_dir: str | Path,
    ticker: str,
    dedup_by_related_ids: bool = True,
) -> list[tuple[Path, dict, str]]:
    """Find all industry research (ID + DS) referencing the given ticker.

    Returns [(path, meta, kind), ...] where kind ∈ {"id", "ds"}.

    Dedup behaviour:

    When `dedup_by_related_ids=True` (default): if any DS lists an ID stem
    in its `related_ids[]` (i.e., explicit cross-link "same theme as that ID"),
    AND both the DS and that ID match the ticker, drop the older one of the
    pair (compare publish_date). This implements the互補-but-not-redundant
    intent: stock-analyst §11 cites the newer view of a paired ID/DS topic
    rather than both.

    Note this dedup is intentionally CONSERVATIVE — it only triggers on
    explicit related_ids cross-link, never on heuristic theme matching.
    Unrelated IDs and standalone DS reports are always kept.

    When `dedup_by_related_ids=False`: return all matches as-is. Useful when
    the consumer (e.g., research index page) wants to show every cross-link
    surface to the reader.

    Example (stock-analyst §11 cross-reference):
        for path, meta, kind in find_research_for_ticker(ID_DIR, DS_DIR, "AVGO"):
            print(f"[{kind.upper()}] {path.name} — {meta['theme']}")
    """
    id_hits = list(find_ids_for_ticker(id_dir, ticker))
    ds_hits = list(find_ds_for_ticker(ds_dir, ticker))

    candidates: list[tuple[Path, dict, str]] = (
        [(p, m, "id") for p, m in id_hits]
        + [(p, m, "ds") for p, m in ds_hits]
    )

    if not dedup_by_related_ids:
        return candidates

    # Build set of (DS path, paired ID stems) from DS's related_ids[]
    # and choose newer of each pair to keep.
    keep: dict[Path, tuple[Path, dict, str]] = {}
    for path, meta, kind in candidates:
        keep[path] = (path, meta, kind)

    for ds_path, ds_meta in ds_hits:
        ds_related = ds_meta.get("related_ids") or []
        if not isinstance(ds_related, list):
            continue
        ds_date = ds_meta.get("publish_date") or ""
        for id_stem in ds_related:
            # Resolve ID stem to actual path object among id_hits
            for id_path, id_meta in id_hits:
                if id_path.stem == id_stem or id_path.name == f"{id_stem}.html":
                    id_date = id_meta.get("publish_date") or ""
                    # Drop the older of the pair
                    if ds_date > id_date:
                        keep.pop(id_path, None)
                    else:
                        keep.pop(ds_path, None)
                    break

    # Preserve original ordering: IDs first (alphabetical), DSs second
    ordered = [keep[p] for p, _, _ in candidates if p in keep]
    # Dedup while preserving order (in case both branches added same path)
    seen: set[Path] = set()
    out: list[tuple[Path, dict, str]] = []
    for entry in ordered:
        if entry[0] in seen:
            continue
        seen.add(entry[0])
        out.append(entry)
    return out
