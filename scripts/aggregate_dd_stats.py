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

ROOT = Path(__file__).parent.parent
DD_DIR = ROOT / "docs" / "dd"
META_RE = re.compile(r'<script id="dd-meta"[^>]*>(.*?)</script>', re.DOTALL)


def load_records():
    """Return {ticker: meta_dict} keyed by latest DD per ticker."""
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
    return records


def signal_distribution(records):
    counts = Counter(r.get("signal", "?") for r in records.values())
    order = ["A+", "A", "B", "C", "X"]
    return [(s, counts.get(s, 0)) for s in order]


def latest_updates(records, n=8):
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


def upside_top(records, n=5):
    pool = [
        r for r in records.values()
        if r.get("signal") in ("A+", "A", "B")
        and isinstance(r.get("upside_mid_pct"), (int, float))
    ]
    return sorted(pool, key=lambda r: -r["upside_mid_pct"])[:n]


def x_cohort(records):
    x_recs = [r for r in records.values() if r.get("signal") == "X"]
    val_red = sorted([r["ticker"] for r in x_recs if r.get("val") == "🔴"])
    ma_brake = sorted([
        r["ticker"] for r in x_recs
        if r.get("ma") in ("❌", "🟠") and r.get("val") != "🔴"
    ])
    return val_red, ma_brake


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


def render(records):
    sig_dist = signal_distribution(records)
    latest = latest_updates(records)
    peg = peg_cheapest(records)
    pct = pct5y_cheapest(records)
    ups = upside_top(records)
    val_red, ma_brake = x_cohort(records)

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

    ups_lis = "".join(
        f'<li><span class="lead">{_ticker_link(r["ticker"], r.get("_path", ""))}</span>'
        f'<span class="meta">+{r["upside_mid_pct"]:.1f}% · {escape(str(r.get("signal", "?")))}</span></li>'
        for r in ups
    )

    val_red_str = " · ".join(escape(t) for t in val_red) if val_red else "—"
    ma_brake_str = " · ".join(escape(t) for t in ma_brake) if ma_brake else "—"

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
      <div class="stats-label">🚀 中期 Upside 最高（A+/A/B）</div>
      <ol>{ups_lis}</ol>
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
