#!/usr/bin/env python3
"""Aggregate dd-meta JSON across all DDs into a stats panel HTML.

Outputs a self-contained HTML block to be injected into docs/research/index.html
between <!-- DD_AUTO_STATS_START --> and <!-- DD_AUTO_STATS_END --> markers.

Stats included:
  - Signal distribution (A+/A/B/C/X)
  - Latest 8 DD updates (date, ticker, signal, oneliner)
  - PEG (FY+2) cheap top 5 (excluding X)
  - 5Y P/E percentile cheap top 5 (excluding X)
  - 2Y mid-term upside top 5 (A+/A/B only)
  - X cohort split (val=🔴 vs MA brake)

Stdlib + (no yfinance — pure local aggregation, fast).
"""
import json
import re
import sys
from collections import Counter
from html import escape
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent.parent
DD_DIR = ROOT / "docs" / "dd"
RESEARCH_HTML = ROOT / "docs" / "research" / "index.html"
META_RE = re.compile(r'<script id="dd-meta"[^>]*>(.*?)</script>', re.DOTALL)
# Parse <tr class="searchable" data-ticker=...> rows from the research table —
# the user-visible source of truth for moat-trend / munger-gate / signal.
TABLE_ROW_RE = re.compile(
    r'<tr class="searchable"\s+([^>]*?)>',
    re.DOTALL,
)


def _build_table_attrs_map(table_html: Optional[str] = None) -> dict:
    """Parse research table <tr> rows; return {ticker: {signal, moat_trend, munger_gate, eps_cagr, ev5y}}.

    moat_trend: int (3=↑, 2=→, 1=↓, 0=unknown — matches data-moat-trend convention).
    munger_gate: int (0-11 or 0 if missing).
    eps_cagr: float (2Y EPS CAGR %; 0.0 if missing/non-numeric).
    ev5y: float (DCA §4 prob-weighted 5Y annualized IRR %; 0.0 if missing/no DCA).

    Source priority:
      1. Explicit table_html arg (in-memory fresh table from update_dd_index)
      2. Disk file docs/research/index.html (standalone runs)
    """
    if table_html is None:
        try:
            table_html = RESEARCH_HTML.read_text(encoding="utf-8")
        except Exception:
            return {}
    out = {}
    for m in TABLE_ROW_RE.finditer(table_html):
        attrs = m.group(1)
        t = re.search(r'data-ticker="([^"]+)"', attrs)
        if not t:
            continue
        sig = re.search(r'data-signal="([^"]*)"', attrs)
        mt = re.search(r'data-moat-trend="(\d+)"', attrs)
        mg = re.search(r'data-munger-gate="(\d+)"', attrs)
        ec = re.search(r'data-eps-cagr="([^"]*)"', attrs)
        ev = re.search(r'data-ev5y="([^"]*)"', attrs)
        try:
            eps_cagr_val = float(ec.group(1)) if ec else 0.0
        except (ValueError, AttributeError):
            eps_cagr_val = 0.0
        try:
            ev5y_val = float(ev.group(1)) if ev else 0.0
        except (ValueError, AttributeError):
            ev5y_val = 0.0
        out[t.group(1)] = {
            "signal": sig.group(1) if sig else "",
            "moat_trend": int(mt.group(1)) if mt else 0,
            "munger_gate": int(mg.group(1)) if mg else 0,
            "eps_cagr": eps_cagr_val,
            "ev5y": ev5y_val,
        }
    return out


_table_attrs_cache: Optional[dict] = None


def _get_table_attrs():
    global _table_attrs_cache
    if _table_attrs_cache is None:
        _table_attrs_cache = _build_table_attrs_map()
    return _table_attrs_cache


def set_table_html(table_html: str) -> None:
    """Called by update_dd_index to inject the fresh in-memory table HTML
    before render() runs, so the moat-quality cards see the same table
    bytes that will be written to disk."""
    global _table_attrs_cache
    _table_attrs_cache = _build_table_attrs_map(table_html)

# ---------------------------------------------------------------------------
# DCA IRR helpers
# ---------------------------------------------------------------------------
_dca_irr_cache = None


def _get_dca_irr_map():
    global _dca_irr_cache
    if _dca_irr_cache is None:
        try:
            from update_dd_index import collect_dca_ev_map, compute_dca_irr
            ev_map = collect_dca_ev_map()
            _dca_irr_cache = {t: compute_dca_irr(ev) for t, ev in ev_map.items()}
        except Exception:
            _dca_irr_cache = {}
    return _dca_irr_cache


def _irr_str(ticker):
    irr_map = _get_dca_irr_map()
    irr = irr_map.get(ticker)
    if irr is None:
        _t_norm = re.sub(r"[^A-Za-z0-9]", "", ticker).upper()
        irr = irr_map.get(_t_norm)
    if irr is None:
        return "IRR —"
    if irr > 0:
        sign = "+"
    elif irr < 0:
        sign = "-"
    else:
        sign = ""
    return f"IRR {sign}{abs(irr):.1f}%/yr"


def load_records():
    """Return {ticker: meta_dict} keyed by latest DD per ticker.

    For filter-relevant fields (signal / moat-trend / §7 munger), the
    research table is the source of truth — see _build_table_attrs_map.
    """
    records = {}
    for p in sorted(DD_DIR.glob("DD_*.html")):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        m = META_RE.search(text)
        if not m:
            continue
        try:
            d = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        if not d.get("ticker") or not d.get("date"):
            continue
        d["_path"] = p.name
        t = d["ticker"]
        if t not in records or d["date"] > records[t]["date"]:
            records[t] = d
    # Overlay table-attrs (signal / moat_trend / munger_gate / eps_cagr / ev5y) —
    # single source of truth = the rendered research table.
    table_attrs = _get_table_attrs()
    for t, r in records.items():
        ta = table_attrs.get(t)
        if ta:
            r["signal"] = ta["signal"] or r.get("signal")
            r["_moat_trend_int"] = ta["moat_trend"]  # 3=↑, 2=→, 1=↓, 0=unknown
            r["_munger_pass"] = ta["munger_gate"]
            r["_eps_cagr"] = ta["eps_cagr"]   # float; 0.0 = missing
            r["_ev5y"] = ta["ev5y"]           # float; 0.0 = no DCA
        else:
            r["_moat_trend_int"] = 0
            r["_munger_pass"] = 0
            r["_eps_cagr"] = 0.0
            r["_ev5y"] = 0.0
    return records


def signal_distribution(records):
    counts = Counter(r.get("signal", "?") for r in records.values())
    order = ["A+", "A", "B", "C", "X"]
    return [(s, counts.get(s, 0)) for s in order]


def latest_updates(records, n=3):
    return sorted(records.values(), key=lambda r: r["date"], reverse=True)[:n]


def peg_cheapest(records, n=5):
    pool = [
        r for r in records.values()
        if r.get("signal") != "X"
        and isinstance(r.get("peg_fy2"), (int, float))
        and r["peg_fy2"] > 0
    ]
    return sorted(pool, key=lambda r: r["peg_fy2"])[:n]


def pct5y_cheapest(records, n=5):
    pool = [
        r for r in records.values()
        if r.get("signal") != "X"
        and isinstance(r.get("pct_5y"), (int, float))
    ]
    return sorted(pool, key=lambda r: r["pct_5y"])[:n]


def eps_cagr_top(records, n=5):
    """Top n by 2Y EPS CAGR; excludes X and zero/missing values."""
    pool = [
        r for r in records.values()
        if r.get("signal") != "X"
        and isinstance(r.get("_eps_cagr"), float)
        and r["_eps_cagr"] > 0
    ]
    return sorted(pool, key=lambda r: -r["_eps_cagr"])[:n]


def irr_high(records, n=5, threshold=12):
    """Tickers with 5Y prob-weighted IRR >= threshold; excludes X and zero/missing."""
    pool = [
        r for r in records.values()
        if r.get("signal") != "X"
        and isinstance(r.get("_ev5y"), float)
        and r["_ev5y"] >= threshold
    ]
    return sorted(pool, key=lambda r: -r["_ev5y"])[:n]


def upside_top(records, n=5):
    pool = [
        r for r in records.values()
        if r.get("signal") in ("A+", "A", "B")
        and isinstance(r.get("upside_mid_pct"), (int, float))
    ]
    return sorted(pool, key=lambda r: -r["upside_mid_pct"])[:n]


def upside_5y_top(records, n=5):
    pool = [
        r for r in records.values()
        if r.get("signal") != "X"
        and isinstance(r.get("upside_5y_pct"), (int, float))
    ]
    return sorted(pool, key=lambda r: -r["upside_5y_pct"])[:n]


def x_cohort(records):
    x_recs = [r for r in records.values() if r.get("signal") == "X"]
    val_red = sorted([r["ticker"] for r in x_recs if r.get("val") == "🔴"])
    ma_brake = sorted([
        r["ticker"] for r in x_recs
        if r.get("ma") in ("❌", "🟠") and r.get("val") != "🔴"
    ])
    return val_red, ma_brake


def _is_trend_up(r):
    """Per data-moat-trend convention: 3 = ↑."""
    return r.get("_moat_trend_int") == 3


def _is_munger_green(r):
    return isinstance(r.get("_munger_pass"), int) and r["_munger_pass"] >= 8


def _sig_class(s):
    return {"A+": "Aplus", "A": "A", "B": "B", "C": "C", "X": "X"}.get(s, "X")


def _ticker_link(t, path):
    if path:
        return f'<a href="/dd/{escape(path)}" target="_blank" rel="noopener">{escape(t)}</a>'
    return escape(t)


def _truncate(s, n=50):
    if not s:
        return ""
    s = str(s).strip()
    if len(s) <= n:
        return s
    return s[:n].rstrip() + "…"


def _moat_card_lis(pool, n=5):
    """Render <li> rows for a moat-quality pool, ranked by 5Y 期望 IRR descending.
    Tickers without DCA IRR are excluded (cannot rank)."""
    irr_map = _get_dca_irr_map()
    enriched = []
    for r in pool:
        t = r["ticker"]
        irr = irr_map.get(t)
        if irr is None:
            _t_norm = re.sub(r"[^A-Za-z0-9]", "", t).upper()
            irr = irr_map.get(_t_norm)
        if irr is None:
            continue
        enriched.append((r, irr))
    enriched.sort(key=lambda x: -x[1])
    if not enriched:
        return '<li style="color:#94A3B8;font-style:italic;list-style:none">符合條件的標的：0 檔</li>'
    rows = ""
    for r, irr in enriched[:n]:
        ticker_html = _ticker_link(r["ticker"], r.get("_path", ""))
        moat = escape(str(r.get("moat", "?")))
        sig = escape(str(r.get("signal", "?")))
        mp = r.get("_munger_pass")
        mp_str = f"{mp}/11" if isinstance(mp, int) else "?"
        sign = "+" if irr > 0 else ("-" if irr < 0 else "")
        irr_str = f"IRR {sign}{abs(irr):.1f}%/yr"
        meta = f'({irr_str}) · {sig} · {moat}↑ · 🟢 {mp_str}'
        rows += (
            f'<li><span class="lead">{ticker_html}</span>'
            f'<span class="meta">{meta}</span></li>'
        )
    return rows


def render(records):
    sig_dist = signal_distribution(records)
    latest = latest_updates(records)
    peg = peg_cheapest(records)
    pct = pct5y_cheapest(records)
    cagr_top = eps_cagr_top(records)
    irr_top = irr_high(records)
    val_red, ma_brake = x_cohort(records)
    # Moat-quality cohorts ranked by 5Y 期望 IRR (excludes C/X verdicts)
    sa_pool = [
        r for r in records.values()
        if r.get("signal") in ("A+", "A", "B")
        and r.get("moat") in ("S", "A")
        and _is_trend_up(r)
        and _is_munger_green(r)
    ]
    bc_pool = [
        r for r in records.values()
        if r.get("signal") in ("A+", "A", "B")
        and r.get("moat") in ("B", "C")
        and _is_trend_up(r)
        and _is_munger_green(r)
    ]

    progress_count = sum(c for s, c in sig_dist if s in ("A+", "A"))
    watch_count = next((c for s, c in sig_dist if s == "B"), 0)
    avoid_count = sum(c for s, c in sig_dist if s in ("C", "X"))
    total = sum(c for _, c in sig_dist)

    # Latest update date
    latest_date = max((r["date"] for r in records.values()), default="—")

    sig_pills = "".join(
        f'<span class="sig-pill sig-{_sig_class(s)}">{escape(s)} · {c}</span>'
        for s, c in sig_dist
    )

    latest_lis = "".join(
        f'<li><span class="lead">{escape(r["date"][5:])} {_ticker_link(r["ticker"], r.get("_path", ""))}</span>'
        f'<span class="meta"><span class="sig-pill sig-{_sig_class(r.get("signal", "?"))}" '
        f'style="font-size:10px;padding:1px 6px">{escape(str(r.get("signal", "?")))}</span> '
        f'{escape(_truncate(r.get("oneliner", ""), 45))}</span></li>'
        for r in latest
    )

    peg_lis = "".join(
        f'<li><span class="lead">{_ticker_link(r["ticker"], r.get("_path", ""))}</span>'
        f'<span class="meta">PEG {r["peg_fy2"]:.2f} · {escape(str(r.get("signal", "?")))}</span></li>'
        for r in peg
    )

    pct_lis = "".join(
        f'<li><span class="lead">{_ticker_link(r["ticker"], r.get("_path", ""))}</span>'
        f'<span class="meta">{r["pct_5y"]:.0f}% · {escape(str(r.get("signal", "?")))}</span></li>'
        for r in pct
    )

    cagr_lis = "".join(
        f'<li><span class="lead">{_ticker_link(r["ticker"], r.get("_path", ""))}</span>'
        f'<span class="meta">+{r["_eps_cagr"]:.1f}% · {escape(str(r.get("signal", "?")))}</span></li>'
        for r in cagr_top
    )

    if irr_top:
        irr_lis = "".join(
            f'<li><span class="lead">{_ticker_link(r["ticker"], r.get("_path", ""))}</span>'
            f'<span class="meta">IRR +{r["_ev5y"]:.1f}%/yr · {escape(str(r.get("signal", "?")))}</span></li>'
            for r in irr_top
        )
    else:
        irr_lis = '<li style="color:#94A3B8;font-style:italic;list-style:none">符合條件的標的：0 檔</li>'

    val_red_str = " · ".join(escape(t) for t in val_red) if val_red else "—"
    ma_brake_str = " · ".join(escape(t) for t in ma_brake) if ma_brake else "—"

    sa_lis = _moat_card_lis(sa_pool)
    bc_lis = _moat_card_lis(bc_pool)

    return f'''<div class="auto-stats">
  <h3>
    📊 DD 組合快照
    <span class="auto-tag">FULL-AUTO</span>
    <span class="ts">最近更新：{escape(latest_date)} ｜ {total} 檔 unique tickers</span>
  </h3>

  <div class="stats-grid">

    <div class="stats-cell">
      <div class="stats-label">訊號分布</div>
      <div class="signal-bar">{sig_pills}</div>
      <div style="margin-top:10px;font-size:11.5px;color:#64748B">
        進場候選 (A+/A)：{progress_count} 檔 ｜ 觀望 (B)：{watch_count} 檔 ｜ 拒絕 (C/X)：{avoid_count} 檔
      </div>
    </div>

    <div class="stats-cell stats-cell-stacked">
      <div class="stats-label">最近 DD 更新（最新 {len(latest)} 檔）</div>
      <ul>{latest_lis}</ul>
    </div>

    <div class="stats-cell">
      <div class="stats-label">💎 PEG (FY+2) 最便宜（排除 X）</div>
      <ol>{peg_lis}</ol>
    </div>

    <div class="stats-cell">
      <div class="stats-label">📉 5Y P/E 分位最便宜（排除 X）</div>
      <ol>{pct_lis}</ol>
    </div>

    <div class="stats-cell">
      <div class="stats-label">🚀 2Y EPS CAGR 最高（排除 X）</div>
      <ol>{cagr_lis}</ol>
    </div>

    <div class="stats-cell">
      <div class="stats-label">💪 5Y 期望 IRR ≥ 12%（排除 X）</div>
      <ol>{irr_lis}</ol>
    </div>

    <div class="stats-cell">
      <div class="stats-label">🛡️ 護城河 S/A 擴大 + §7 🟢（依 5Y 期望 IRR 排序）</div>
      <ol>{sa_lis}</ol>
    </div>

    <div class="stats-cell">
      <div class="stats-label">🛡️ 護城河 B/C 擴大 + §7 🟢（依 5Y 期望 IRR 排序）</div>
      <ol>{bc_lis}</ol>
    </div>

    <div class="stats-cell x-cohort">
      <div class="stats-label">🚧 X 陣營拒絕原因（{len(val_red) + len(ma_brake)} 檔）</div>
      <div style="font-size:12px;color:#475569;line-height:1.65">
        <div style="margin:4px 0"><span style="color:#991B1B;font-weight:600">估值 🔴 拒絕 ({len(val_red)})：</span><span style="font-family:'IBM Plex Mono',monospace;font-size:11.5px">{val_red_str}</span></div>
        <div style="margin:4px 0"><span style="color:#92400E;font-weight:600">MA 煞車 ({len(ma_brake)})：</span><span style="font-family:'IBM Plex Mono',monospace;font-size:11.5px">{ma_brake_str}</span></div>
      </div>
    </div>

  </div>
</div>'''


def main():
    records = load_records()
    if "--json" in sys.argv:
        # Compact JSON for debug
        out = {
            "total": len(records),
            "signal": dict(signal_distribution(records)),
            "latest": [{"date": r["date"], "ticker": r["ticker"], "signal": r.get("signal")} for r in latest_updates(records)],
            "peg_top": [(r["ticker"], r["peg_fy2"]) for r in peg_cheapest(records)],
            "pct_top": [(r["ticker"], r["pct_5y"]) for r in pct5y_cheapest(records)],
            "upside_top": [(r["ticker"], r["upside_mid_pct"]) for r in upside_top(records)],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    print(render(records))


if __name__ == "__main__":
    main()
