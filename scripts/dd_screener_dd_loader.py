"""DD Screener Phase 1 — identity + DD-meta-sourced fields loader.

Public API:
    load_dd_universe(dd_dir, dca_dir) -> list[dict]
    load_non_dd_universe(existing_tickers) -> list[dict]

CLI self-test:
    python3 scripts/dd_screener_dd_loader.py
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

# ── path setup ───────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from dd_meta_reader import iter_dd_metas, read_dd_meta  # noqa: E402
from engine.grp import market_ok  # noqa: E402

# ── constants ─────────────────────────────────────────────────────────────────

# Required fields in dd-meta (skip ticker if any absent)
_REQUIRED = ("moat_score", "signal", "trap", "val")

# Moat-grade key: newer DDs use 'moat_grade'; most use 'moat'
_MOAT_GRADE_KEYS = ("moat_grade", "moat")

# Known moat_trend text → arrow mappings (Chinese labels used in early DDs)
_TREND_NORM: dict[str, str] = {
    "加深": "↑",
    "擴大": "↑",
    "改善": "↑",
    "上升": "↑",
    "↑": "↑",
    "穩定": "→",
    "持平": "→",
    "→": "→",
    "縮窄": "↓",
    "衰退": "↓",
    "下降": "↓",
    "↓": "↓",
}

# DD filename date pattern: DD_{STEM}_{YYYYMMDD}[_suffix].html
# v17: also accepts the 快速版 filename brief/BRIEF_{STEM}_{YYYYMMDD}.html.
_DD_FILENAME_DATE_RE = re.compile(r"^(?:DD|BRIEF)_.+?_(\d{8})(?:_.*)?\.html$")

# ── 選股系統 v2 (2026-09) — non-DD universe from QGM (姊妹 repo quality pools) ──
# DD becomes optional: names that never got a DD report still need to be
# carriable in the screener universe. QGM (minervini-quality-backtest) already
# produces a fundamentals-gated + trend-template-gated quality pool for US
# (docs/qgm/latest.json) and TW (docs/qgm-tw/latest.json); load_non_dd_universe
# adapts those rows into the same shape load_dd_universe() returns, with every
# DD-derived field null so downstream consumers can branch on `dd_status`.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_QGM_SOURCES = (
    (_REPO_ROOT / "docs" / "qgm" / "latest.json", "qgm-us"),
    (_REPO_ROOT / "docs" / "qgm-tw" / "latest.json", "qgm-tw"),
)
_QGM_POOL_KEYS = ("candidates", "watch_list", "quality_pool")  # priority order

# 本地掛牌 → ADR（同一家公司只留一席）— 與 scripts/engine/build_arena.py 的
# LISTING_ALIAS 同一份對照表（維持單一事實來源的意圖，但兩處各自獨立載入，
# 改動時務必同步）。
_LISTING_ALIAS = {"2330.TW": "TSM"}

# Fields in load_dd_universe()'s output dict that are DD/DCA-derived and must
# be null for a non-DD (QGM-sourced) row.
_DD_ONLY_FIELDS = (
    "moat_score", "moat_grade", "moat_trend", "moat_execution", "moat_pricing_power",
    "signal", "trap", "val",
    "upside_mid_pct", "upside_5y_pct", "fpe_fy2",
    "pct_5y", "growth_durability", "quality_score", "ai_risk",
    "price_at_dd", "runway_post_y5",
    "bull_5y_price", "bear_5y_price", "p_bull_pct", "p_bear_pct",
    "dd_path", "dd_date", "dca_path", "dca_date", "dca_verdict", "dca_role",
)


# ── helpers ───────────────────────────────────────────────────────────────────


def _norm_dca_role(role):
    """v14.12 四值歸一（核心/衛星/追蹤/不持有）；legacy 值映射，canonical 定義見 aggregate_dca_stats._categorize。"""
    r = (role or "").strip()
    if not r:
        return r
    if r in ("核心", "衛星", "追蹤", "不持有"):
        return r
    if "候選" in r or "追蹤池" in r:
        return "追蹤"
    if r.startswith(("不持有", "暫不持有", "迴避")):
        return "不持有"
    if "核心" in r:
        return "核心"
    if "衛星" in r or "投機" in r or r.lower().startswith("satellite"):
        return "衛星"
    return r

def _ticker_to_filename_stem(ticker: str) -> str:
    """Convert canonical ticker to filename stem (strip dots).

    Examples:
        NVDA       -> NVDA
        2330.TW    -> 2330TW
        6857.T     -> 6857T
        RMS        -> RMS
    """
    return ticker.replace(".", "")


def _normalize_moat_trend(raw: Optional[str]) -> str:
    """Normalize moat_trend text to arrow symbol; default '↑' if absent/unknown."""
    if not raw:
        return "↑"
    normed = _TREND_NORM.get(raw.strip())
    if normed:
        return normed
    # If it's already an arrow, pass through
    if raw.strip() in ("↑", "→", "↓"):
        return raw.strip()
    # Unknown string — default to '↑' (locked decision per schema doc)
    return "↑"


def _extract_date_from_dd_filename(filename: str) -> Optional[str]:
    """Return 'YYYY-MM-DD' from 'DD_{STEM}_{YYYYMMDD}[_suffix].html', or None."""
    m = _DD_FILENAME_DATE_RE.match(filename)
    if not m:
        return None
    d = m.group(1)
    return f"{d[:4]}-{d[4:6]}-{d[6:8]}"


def _find_latest_dca(dca_dir: Path, ticker: str) -> tuple[Optional[str], Optional[str]]:
    """Return (dca_path, dca_date) for the latest DCA file for ticker.

    DCA files follow DCA_{STEM}_{YYYYMMDD}.html where STEM = ticker with dots stripped.
    Returns (None, None) if no DCA exists.
    """
    stem = _ticker_to_filename_stem(ticker)
    pattern = str(dca_dir / f"DCA_{stem}_*.html")
    matches = sorted(glob.glob(pattern))
    if not matches:
        return None, None

    # Pick latest by filename date (lexicographic sort of YYYYMMDD is correct)
    latest_path = Path(matches[-1])
    filename = latest_path.name

    # Parse date from filename: DCA_{STEM}_{YYYYMMDD}.html
    date_re = re.compile(r"^DCA_.+?_(\d{8})\.html$")
    dm = date_re.match(filename)
    if not dm:
        return None, None

    d = dm.group(1)
    dca_date = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    dca_path = f"/dca/{filename}"
    return dca_path, dca_date


def _iter_dd_and_brief_metas(dd_dir: Path):
    """Like dd_meta_reader.iter_dd_metas but also walks dd_dir/brief/BRIEF_*.html
    (v17 快速版 — same dd-meta schema, plus "brief":true). Yields (path, meta)."""
    yield from iter_dd_metas(dd_dir)
    brief_dir = dd_dir / "brief"
    if not brief_dir.exists():
        return
    for p in sorted(brief_dir.glob("BRIEF_*.html")):
        meta = read_dd_meta(p)
        if meta is not None:
            yield p, meta


def _dd_href(path: Path, dd_dir: Path) -> str:
    """Public /dd/... href for a DD or brief file, preserving the brief/
    subdirectory when present."""
    try:
        rel = path.relative_to(dd_dir)
    except ValueError:
        rel = Path(path.name)
    return f"/dd/{rel.as_posix()}"


def _latest_per_ticker_with_paths(
    dd_dir: Path,
) -> dict[str, tuple[Path, dict]]:
    """Return {ticker: (path, meta)} keeping the latest DD per ticker.

    Uses dd_meta_reader.iter_dd_metas plus the brief/BRIEF_*.html 快速版
    scan (_iter_dd_and_brief_metas); dedupes by ticker keeping the highest
    'date' value across BOTH file kinds — for downstream consumers a 快速版
    is just as much "the DD" as a full report (same dd-meta schema, plus
    "brief":true). Same-date ties keep whichever was seen first (full DDs
    are yielded before brief ones)."""
    best: dict[str, tuple[Path, dict]] = {}
    for path, meta in _iter_dd_and_brief_metas(dd_dir):
        ticker = meta.get("ticker")
        date = meta.get("date")
        if not ticker or not date:
            continue
        prev = best.get(ticker)
        if prev is None or date > prev[1].get("date", ""):
            best[ticker] = (path, meta)
    return best


def _qgm_seed_from_record(x: dict) -> dict:
    """Extract the raw QGM numbers a non-DD row carries forward as fallback
    inputs for the quality (Step 3) and EPS (Step 8+) stages — same numbers
    `get_quality_for_ticker()` / `enrich_ticker()` would read for a QGM-sourced
    DD ticker, just pre-shaped so those stages don't need to special-case
    'no dd-meta' vs 'has dd-meta but QGM-sourced quality'.
    """
    hfd = x.get("hard_filter_details") or {}

    def _hv(key: str):
        d = hfd.get(key)
        return d.get("value") if isinstance(d, dict) else None

    qb = x.get("quality_breakdown") or {}
    roic_stability = qb.get("roic_5y_stability") or {}
    conds = (x.get("trend_template") or {}).get("conditions") or {}

    return {
        "price": x.get("price"),
        "market_cap_b": x.get("market_cap_b"),
        "fy1_eps": x.get("fy1_eps"),
        "fy2_eps": x.get("fy2_eps"),
        "fy1_per": x.get("fy1_per"),
        "quality_score": x.get("quality_score"),  # QGM's own 0-100 score (NOT dd-meta's 1-10 field)
        "pool_tier": x.get("pool"),                # QGM MLB/3A tier tag
        "hard_filter_details": {
            "fcf_margin": _hv("fcf_margin"),
            "roic": _hv("roic"),
            "eps_cagr_2y_fwd": _hv("eps_cagr_2y_fwd"),
            "peg": _hv("peg"),
            "debt_to_equity": _hv("debt_to_equity"),
        },
        "roic_5y_stability_pct_above": roic_stability.get("pct_above"),
        "trend_template_conditions": conds,
    }


def load_non_dd_universe(existing_tickers: set) -> list[dict]:
    """QGM quality-pool rows (US + TW) for tickers with no DD report.

    Returns one dict per unique ticker in the SAME shape load_dd_universe()
    returns, with every DD/DCA-derived field (see `_DD_ONLY_FIELDS`) set to
    None, plus three additions:
        dd_status:       "none" (always — this loader never emits DD rows)
        universe_source: "qgm-us" | "qgm-tw" (which QGM file the row came from)
        qgm_seed:        raw QGM numbers (price / EPS / hard_filter_details /
                          roic_5y_stability / trend_template.conditions) for
                          the quality/eps stages to use as fallback input.

    Dedup / precedence rules:
      - A ticker already in `existing_tickers` (i.e. it has a DD) is skipped
        — the DD-sourced row is authoritative, this loader never shadows it.
      - Within and across the two QGM files, first-write-wins by pool
        priority candidates > watch_list > quality_pool, US file read before
        TW (mirrors `dd_screener_quality.load_qgm_index()`'s own priority).
      - ADR/local alias (`_LISTING_ALIAS`, e.g. "2330.TW" -> "TSM"): the local
        listing is dropped whenever the ADR ticker is present either in
        `existing_tickers` (has a DD) or in this loader's own collected set
        (QGM also carries the ADR) — same company, one seat.
    """
    collected: dict[str, dict] = {}

    for path, src_tag in _QGM_SOURCES:
        if not market_ok(f"0000{'.TW' if src_tag == 'qgm-tw' else ''}"):
            # 2026-09-02 持有人拍板：v2 先只做美股，台股另建——qgm-tw 源不產母體列
            # （探測值走 market_ok 而非硬寫死排除，未來拍板改變時自動跟著恢復）。
            print(f"  load_non_dd_universe: skipping {src_tag} source (market_ok gate)", file=sys.stderr)
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"WARN load_non_dd_universe: skipping {path} ({exc})", file=sys.stderr)
            continue

        for pool_key in _QGM_POOL_KEYS:
            for x in data.get(pool_key) or []:
                if not isinstance(x, dict):
                    continue
                ticker = x.get("ticker")
                if not ticker:
                    continue
                if not market_ok(ticker):
                    continue  # 2026-09-02 拍板：台股另建，逐檔亦排除 .TW（雙保險）
                if ticker in existing_tickers or ticker in collected:
                    continue  # DD-sourced row wins, or already claimed by a higher-priority pool

                row = {"ticker": ticker, "name": ticker, "sector": ""}
                for field in _DD_ONLY_FIELDS:
                    row[field] = None
                row["dd_status"] = "none"
                row["universe_source"] = src_tag
                row["qgm_seed"] = _qgm_seed_from_record(x)
                collected[ticker] = row

    for local, adr in _LISTING_ALIAS.items():
        if local in collected and (adr in existing_tickers or adr in collected):
            print(f"  load_non_dd_universe: dropping local listing {local} "
                  f"(ADR {adr} already covers this company)", file=sys.stderr)
            del collected[local]

    return [collected[t] for t in sorted(collected)]


# ── public API ────────────────────────────────────────────────────────────────

def load_dd_universe(
    dd_dir: str | Path = "docs/dd",
    dca_dir: str | Path = "docs/dca",
) -> list[dict]:
    """Return one dict per unique ticker (latest DD per ticker), populated with
    the identity + DD-meta-sourced fields per scripts/dd_screener_schema.md.

    Skip any DD whose dd-meta lacks moat_score / signal / trap / val
    (these are required by the schema). Log skipped tickers to stderr.

    Each returned dict has:
        ticker, name, sector,
        moat_score, moat_grade, moat_trend,
        moat_execution, moat_pricing_power,   # v12.3+ optional, None for legacy DDs
        signal, trap, val,
        upside_mid_pct, upside_5y_pct, fpe_fy2,
        pct_5y, growth_durability, quality_score, ai_risk,  # v1.2 quality-entry inputs
        dd_path, dd_date,
        dca_path, dca_date,
        dd_status ("dd"), universe_source (None), qgm_seed (None)  # see load_non_dd_universe
    """
    dd_dir = Path(dd_dir)
    dca_dir = Path(dca_dir)

    per_ticker = _latest_per_ticker_with_paths(dd_dir)
    results: list[dict] = []

    for ticker, (path, meta) in sorted(per_ticker.items()):
        # ── required field checks ─────────────────────────────────────────
        skip = False
        for field in _REQUIRED:
            if meta.get(field) is None:
                print(f"SKIP {ticker}: missing required field {field}", file=sys.stderr)
                skip = True
                break
        if skip:
            continue

        # moat_grade: prefer 'moat_grade', fallback to 'moat'
        moat_grade: Optional[str] = None
        for key in _MOAT_GRADE_KEYS:
            val = meta.get(key)
            if val is not None:
                moat_grade = str(val)
                break

        if moat_grade is None:
            print(f"SKIP {ticker}: missing required field moat_grade/moat", file=sys.stderr)
            continue

        # ── identity fields ───────────────────────────────────────────────
        name: str = (
            meta.get("company")
            or meta.get("name")
            or ticker
        )
        sector: str = meta.get("industry") or ""

        # ── moat fields ───────────────────────────────────────────────────
        moat_score: float = meta["moat_score"]
        moat_trend: str = _normalize_moat_trend(meta.get("moat_trend"))

        # ── signal / trap / val ───────────────────────────────────────────
        signal: str = meta["signal"]
        trap: str = meta["trap"]
        val_field: str = meta["val"]

        # ── upside fields ─────────────────────────────────────────────────
        upside_mid_pct = meta.get("upside_mid_pct")
        upside_5y_pct = meta.get("upside_5y_pct")

        # ── 2Y forward P/E (FY+2; same value the /research/ table shows) ─
        fpe_fy2 = meta.get("fpe_fy2")

        # ── quality-entry v1.2 fields (propagate dd-meta as-is, allow null) ──
        # `pct_5y` = 5Y FwdPE percentile (lower = cheaper); main Entry-pillar anchor.
        # `growth_durability` (1-10), `quality_score` (1-10) — DD §1 analyst scores.
        # `moat_execution` / `moat_pricing_power` (1-10) — v12.3+ two-axis decomp.
        # `ai_risk` — 🟢/🟡/🔴 disrupt-risk light, used as quality-entry veto.
        pct_5y = meta.get("pct_5y")
        growth_durability = meta.get("growth_durability")
        quality_score = meta.get("quality_score")
        moat_execution = meta.get("moat_execution")
        moat_pricing_power = meta.get("moat_pricing_power")
        ai_risk = meta.get("ai_risk")
        # v1.3: price_at_dd 用於 live FwdPE drift 計算 (live_fpe ≈ fpe_fy2 × price_now/price_at_dd)
        price_at_dd = meta.get("price_at_dd")

        # v1.9 (v14.3 F4): AR Live inputs — §11.5 Bull/Bear 5Y target prices +
        # scenario probabilities. Optional; present only in v14.3+ reports.
        # build_dd_screener recomputes ar_live daily from these + current price,
        # turning a static 觀望 verdict into a standing breakout-watch order.
        runway_post_y5 = meta.get("runway_post_y5")
        bull_5y_price = meta.get("bull_5y_price")
        bear_5y_price = meta.get("bear_5y_price")
        p_bull_pct = meta.get("p_bull_pct")
        p_bear_pct = meta.get("p_bear_pct")

        # ── dd_path / dd_date ─────────────────────────────────────────────
        # v17: path may be docs/dd/brief/BRIEF_{T}_{D}.html (快速版) — keep the
        # brief/ subdir in the href, use its filename for date extraction.
        dd_filename = path.name
        dd_path = _dd_href(path, dd_dir)
        dd_date = _extract_date_from_dd_filename(dd_filename) or meta.get("date")
        is_brief = bool(meta.get("brief"))

        # ── DCA lookup ────────────────────────────────────────────────────
        # v13 merged report folds the decision layer into the DD itself, so the
        # 定見 link is the DD's own #decision anchor (no separate /dca/ file).
        # 統一裁決（進場/觀望/迴避）只從 v13/v14 dd-meta 讀 — legacy DCA 檔已
        # 退役（2026-07 起不再作為裁決來源），v12-only ticker 留空待 DD 重跑補上。
        if str(meta.get("schema", "")).startswith(("v13", "v14", "v15")):
            dca_path, dca_date = f"{dd_path}#decision", dd_date
            dca_verdict = meta.get("dca_verdict")
            dca_role = _norm_dca_role(meta.get("dca_role"))
        else:
            dca_path, dca_date = _find_latest_dca(dca_dir, ticker)
            dca_verdict = dca_role = None

        results.append({
            "ticker": ticker,
            "name": name,
            "sector": sector,
            "moat_score": moat_score,
            "moat_grade": moat_grade,
            "moat_trend": moat_trend,
            "moat_execution": moat_execution,
            "moat_pricing_power": moat_pricing_power,
            "signal": signal,
            "trap": trap,
            "val": val_field,
            "upside_mid_pct": upside_mid_pct,
            "upside_5y_pct": upside_5y_pct,
            "fpe_fy2": fpe_fy2,
            "pct_5y": pct_5y,
            "growth_durability": growth_durability,
            "quality_score": quality_score,
            "ai_risk": ai_risk,
            "price_at_dd": price_at_dd,
            "runway_post_y5": runway_post_y5,
            "bull_5y_price": bull_5y_price,
            "bear_5y_price": bear_5y_price,
            "p_bull_pct": p_bull_pct,
            "p_bear_pct": p_bear_pct,
            "dd_path": dd_path,
            "dd_date": dd_date,
            "dca_path": dca_path,
            "dca_date": dca_date,
            "dca_verdict": dca_verdict,
            "dca_role": dca_role,
            # 選股系統 v2 (2026-09): DD becomes optional — every row (DD-sourced
            # or QGM-sourced via load_non_dd_universe) carries dd_status so
            # downstream consumers can branch without inferring it from which
            # fields happen to be null. "dd" here always means a real DD report.
            "dd_status": "dd",
            "universe_source": None,
            "qgm_seed": None,
            # v17: True for docs/dd/brief/BRIEF_*.html 快速版（判斷同完整版，
            # 未寫散文）；False for a full DD report. Same dd-meta schema either way.
            "brief": is_brief,
        })

    return results


# ── CLI self-test ─────────────────────────────────────────────────────────────

def main() -> None:
    import collections

    # Resolve relative to repo root (one level above scripts/)
    repo_root = Path(__file__).parent.parent
    dd_dir = repo_root / "docs" / "dd"
    dca_dir = repo_root / "docs" / "dca"

    universe = load_dd_universe(dd_dir, dca_dir)

    # ── summary stats ─────────────────────────────────────────────────────
    signal_counts: dict[str, int] = collections.Counter(u["signal"] for u in universe)
    with_dca = sum(1 for u in universe if u["dca_path"] is not None)
    with_explicit_trend = sum(1 for u in universe if u["moat_trend"] != "↑"
                               or (u["ticker"] in {v["ticker"] for v in universe
                                                    if v.get("moat_trend") != "↑"}))
    # Count how many had explicit moat_trend in dd-meta (not defaulted)
    # Reload to count: check raw meta
    raw_metas = [m for _, m in iter_dd_metas(dd_dir)]
    from dd_meta_reader import latest_per_ticker
    latest_raw = latest_per_ticker(raw_metas)
    explicit_trend_count = sum(1 for m in latest_raw if m.get("moat_trend"))

    print("=" * 60)
    print("DD Screener Universe — load_dd_universe() summary")
    print("=" * 60)
    print(f"Total tickers loaded:          {len(universe)}")
    print(f"  with DCA report:             {with_dca}")
    print(f"  with explicit moat_trend:    {explicit_trend_count}")
    print()
    print("Signal breakdown:")
    for sig in sorted(signal_counts, key=lambda s: ["A+", "A", "B", "C", "X"].index(s)
                      if s in ["A+", "A", "B", "C", "X"] else 99):
        print(f"  {sig:4s}: {signal_counts[sig]}")
    print()

    # ── sample dict ───────────────────────────────────────────────────────
    sample = universe[0] if universe else {}
    # Prefer NVDA for a meaningful sample
    nvda = next((u for u in universe if u["ticker"] == "NVDA"), None)
    if nvda:
        sample = nvda

    print("Sample entry:")
    print(json.dumps(sample, indent=2, ensure_ascii=False))

    # ── non-DD universe summary (選股系統 v2, 2026-09) ──────────────────────
    existing_tickers = {u["ticker"] for u in universe}
    non_dd = load_non_dd_universe(existing_tickers)
    src_counts = collections.Counter(r["universe_source"] for r in non_dd)
    print()
    print("=" * 60)
    print("load_non_dd_universe() summary")
    print("=" * 60)
    print(f"Total non-DD tickers loaded:    {len(non_dd)}")
    for src in sorted(src_counts):
        print(f"  {src:8s}: {src_counts[src]}")
    print()
    print(f"Sample entries (2 of {len(non_dd)}):")
    for row in non_dd[:2]:
        print(json.dumps(row, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
