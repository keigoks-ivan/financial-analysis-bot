#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Public track-record scoreboard builder.

Parses every docs/dd/DD_*.html dd-meta block, computes forward returns
(+30/+90/+180 calendar days + to-date) from the publish-time price anchor
against weekly adjusted closes, benchmarks US-listed names against SPY
(absolute-only for non-US, disclosed), aggregates by verdict group × window
with era separation (v13+ dca_verdict vs legacy v12 signal grade), and renders
a self-contained docs/track-record/index.html + zero-churn data/latest.json.

描述器紀律：retrospective description only, no forward-looking claims.
Read-only w.r.t. data/weekly_cache. Owns data/track_record_prices.json cache.
No git operations.
"""
import argparse
import datetime as dt
import glob
import html
import json
import os
import re
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD_GLOB = os.path.join(ROOT, "docs", "dd", "DD_*.html")
WEEKLY_CACHE = os.path.join(ROOT, "data", "weekly_cache")
ROTATION_BENCH = os.path.join(ROOT, "data", "rotation_bench.json")
OWN_CACHE = os.path.join(ROOT, "data", "track_record_prices.json")
OUT_JSON = os.path.join(ROOT, "docs", "track-record", "data", "latest.json")
OUT_HTML = os.path.join(ROOT, "docs", "track-record", "index.html")
CANONICAL = os.path.join(ROOT, "docs", "mental-models", "index.html")

WINDOWS = [("d30", 30), ("d90", 90), ("d180", 180)]
# Non-US suffix -> yfinance symbol override for the own-cache fetch.
NONUS_MAP = {
    "5274.TW": "5274.TWO", "8299.TW": "8299.TWO",
    "BESI": "BESI.AS", "AENA": "AENA.MC", "LVMH": "MC.PA",
    "RMS": "RMS.PA", "SU": "SU.PA", "ABB": "ABB",
}


def warn(msg):
    print(f"  [warn] {msg}", file=sys.stderr)


# ── zero-churn IO (protocol copied from build_rotation_radar.py) ──
def _serialize(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _strip_volatile(obj, keys):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        warn(f"could not read {os.path.basename(path)}: {e}")
        return default


def write_if_changed(path, text, volatile_re=None):
    """Write text only if content (minus volatile regions) changed."""
    if os.path.exists(path):
        old = open(path, encoding="utf-8").read()
        a, b = old, text
        if volatile_re:
            a = re.sub(volatile_re, "", a)
            b = re.sub(volatile_re, "", b)
        if a == b:
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def write_json_if_changed(path, obj, volatile=("built_at",)):
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_serialize(obj))
    return True


# ── price series ──
def load_weekly_series():
    """Return {ticker: [(date_iso, close), ...] sorted asc} from read-only cache."""
    series = {}
    for f in glob.glob(os.path.join(WEEKLY_CACHE, "*.json")):
        d = load_json(f)
        if not d:
            continue
        tk = d.get("ticker") or os.path.basename(f)[:-5]
        bars = [(b["week_end"], float(b["close"])) for b in d.get("weekly_bars", [])
                if b.get("close") is not None]
        bars.sort()
        if bars:
            series[tk] = bars
    return series


def load_spy():
    """SPY weekly closes; prefer own-cache (fresher), fall back to rotation_bench."""
    own = load_json(OWN_CACHE, {}) or {}
    spy = (own.get("series") or {}).get("SPY")
    if spy:
        return sorted((d, float(c)) for d, c in spy)
    bench = load_json(ROTATION_BENCH, {}) or {}
    return sorted((d, float(c)) for d, c in bench.get("series", []))


def fetch_missing(needed_symbols):
    """Fetch weekly adjusted closes for uncovered tickers + SPY into own cache.
    Warn-and-continue; never touches weekly_cache. Zero-churn write."""
    try:
        import yfinance as yf
    except Exception as e:
        warn(f"yfinance unavailable ({e}); skipping fetch, uncovered names excluded")
        return load_json(OWN_CACHE, {}) or {"series": {}}
    cache = load_json(OWN_CACHE, {}) or {}
    series = dict(cache.get("series") or {})
    for tk, sym in needed_symbols.items():
        try:
            h = yf.Ticker(sym).history(period="2y", interval="1wk", auto_adjust=True)
            pts = [(ix.date().isoformat(), round(float(c), 4))
                   for ix, c in zip(h.index, h["Close"]) if c == c]
            if pts:
                series[tk] = pts
                print(f"  fetched {tk} via {sym}: {len(pts)} weekly bars "
                      f"({pts[0][0]}→{pts[-1][0]})")
            else:
                warn(f"no data for {tk} ({sym})")
        except Exception as e:
            warn(f"fetch failed {tk} ({sym}): {str(e)[:70]}")
    obj = {"built_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "source": "yfinance:2y:1wk auto_adjust=True",
           "note": "own cache for track-record: SPY + tickers absent from weekly_cache. "
                   "weekly_cache is read-only; do not merge.",
           "series": series}
    write_json_if_changed(OWN_CACHE, obj)
    return obj


def close_on_or_after(bars, target_iso):
    """Nearest weekly close with week_end >= target_iso. None if past last bar."""
    for d, c in bars:
        if d >= target_iso:
            return c
    return None


def close_on_or_before(bars, target_iso):
    """Nearest weekly close with week_end <= target_iso (last known at date).
    Falls back to earliest bar (on/after) if none precede."""
    prev = None
    for d, c in bars:
        if d <= target_iso:
            prev = c
        else:
            break
    return prev if prev is not None else (bars[0][1] if bars else None)


# ── DD parsing ──
def parse_dds():
    obs, excluded = [], []
    for f in sorted(glob.glob(DD_GLOB)):
        s = open(f, encoding="utf-8").read()
        m = re.search(r'<script id="dd-meta"[^>]*>(.*?)</script>', s, re.S)
        base = os.path.basename(f)
        if not m:
            excluded.append((base, "no dd-meta (v9-era, no structured verdict/price)"))
            continue
        try:
            d = json.loads(m.group(1))
        except Exception as e:
            excluded.append((base, f"dd-meta JSON error: {str(e)[:40]}"))
            continue
        tk = d.get("ticker")
        date = d.get("date")
        price = d.get("price_at_dd")
        sch = str(d.get("schema", ""))
        if not (tk and date and price):
            excluded.append((base, "missing ticker/date/price_at_dd"))
            continue
        era = "v13plus" if (sch.startswith("v13") or sch.startswith("v14")) else "v12"
        if era == "v13plus":
            group = d.get("dca_verdict")  # 進場/觀望/迴避
        else:
            group = d.get("signal")       # A+/A/B/C/X (fundamental grade)
        obs.append({
            "file": base, "ticker": tk, "date": date,
            "price_at_dd": float(price), "schema": sch, "era": era,
            "group": group,
            "is_us": "." not in tk,   # dotted suffix => non-US listing
        })
    return obs, excluded


def pct(x):
    return None if x is None else round(x * 100, 2)


def quantiles(vals):
    vals = sorted(vals)
    n = len(vals)
    if n == 0:
        return (None, None, None)
    med = statistics.median(vals)
    if n == 1:
        return (vals[0], med, vals[0])
    p25 = statistics.quantiles(vals, n=4, method="inclusive")[0]
    p75 = statistics.quantiles(vals, n=4, method="inclusive")[2]
    return (p25, med, p75)


def compute(obs, weekly, own_series, spy):
    """Attach forward returns + SPY excess to each observation."""
    as_of = None
    all_last = []
    for bars in weekly.values():
        if bars:
            all_last.append(bars[-1][0])
    for s in own_series.values():
        if s:
            all_last.append(sorted(s)[-1][0])
    as_of = max(all_last) if all_last else None
    spy_last = spy[-1][0] if spy else None

    for o in obs:
        tk = o["ticker"]
        bars = weekly.get(tk)
        if bars is None and tk in own_series:
            bars = sorted((d, float(c)) for d, c in own_series[tk])
        if not bars:
            o["price_covered"] = False
            for wk, _ in WINDOWS:
                o[f"ret_{wk}"] = None
                o[f"exc_{wk}"] = None
            o["ret_todate"] = None
            o["exc_todate"] = None
            continue
        o["price_covered"] = True
        pub = dt.date.fromisoformat(o["date"])
        # Base = split/dividend-adjusted weekly close as-of publish (same adjusted
        # scale as the forward closes). Using raw price_at_dd would break across a
        # post-publish split (e.g. KLAC/CRWD: raw pre-split price vs adjusted close).
        base = close_on_or_before(bars, o["date"])
        # Flag when the DD's recorded raw price diverges materially from the adjusted
        # base — i.e. a split/large dividend occurred since publish (disclosure only).
        o["split_rebased"] = bool(base and o["price_at_dd"]
                                  and not (0.7 <= o["price_at_dd"] / base <= 1.4))
        spy_base = close_on_or_before(spy, o["date"]) if (o["is_us"] and spy) else None
        for wk, days in WINDOWS:
            tgt = (pub + dt.timedelta(days=days)).isoformat()
            end = close_on_or_after(bars, tgt)
            if end is None:
                o[f"ret_{wk}"] = None
                o[f"exc_{wk}"] = None
                continue
            ret = end / base - 1.0
            o[f"ret_{wk}"] = round(ret, 5)
            if o["is_us"] and spy_base:
                spy_end = close_on_or_after(spy, tgt)
                o[f"exc_{wk}"] = round(ret - (spy_end / spy_base - 1.0), 5) if spy_end else None
            else:
                o[f"exc_{wk}"] = None
        # to-date
        last = bars[-1][1]
        ret = last / base - 1.0
        o["ret_todate"] = round(ret, 5)
        if o["is_us"] and spy_base and spy_last:
            spy_end = spy[-1][1]
            o["exc_todate"] = round(ret - (spy_end / spy_base - 1.0), 5)
        else:
            o["exc_todate"] = None
    return as_of


def agg_group(rows, wk):
    """Aggregate one verdict group for one window."""
    rets = [r[f"ret_{wk}"] for r in rows if r.get(f"ret_{wk}") is not None]
    exc = [r[f"exc_{wk}"] for r in rows if r.get(f"exc_{wk}") is not None]
    p25, med, p75 = quantiles(rets)
    n = len(rets)
    pos = sum(1 for x in rets if x > 0)
    beat = sum(1 for x in exc if x > 0)
    return {
        "n": n,
        "median": pct(med), "p25": pct(p25), "p75": pct(p75),
        "pct_positive": pct(pos / n) if n else None,
        "n_bench": len(exc),
        "pct_beat_spy": pct(beat / len(exc)) if exc else None,
    }


def build_tables(obs):
    windows = [w for w, _ in WINDOWS] + ["todate"]
    covered = [o for o in obs if o.get("price_covered")]

    def group_table(rows, order):
        groups = {}
        for g in order:
            sub = [r for r in rows if r["group"] == g]
            groups[g] = {"n_reports": len(sub),
                         "windows": {wk: agg_group(sub, wk) for wk in windows}}
        return groups

    v13 = [o for o in covered if o["era"] == "v13plus"]
    v12 = [o for o in covered if o["era"] == "v12"]
    tables = {
        "v13plus": group_table(v13, ["進場", "觀望", "迴避"]),
        "v12": group_table(v12, ["A+", "A", "B", "C", "X"]),
    }

    # best / worst 5 by to-date (both directions), per era
    def extremes(rows):
        rr = [r for r in rows if r.get("ret_todate") is not None]
        rr.sort(key=lambda r: r["ret_todate"])
        def fmt(r):
            return {"ticker": r["ticker"], "date": r["date"], "group": r["group"],
                    "ret_todate": pct(r["ret_todate"]),
                    "exc_todate": pct(r["exc_todate"]) if r["exc_todate"] is not None else None,
                    "is_us": r["is_us"]}
        return {"worst": [fmt(r) for r in rr[:5]],
                "best": [fmt(r) for r in reversed(rr[-5:])]}
    extr = {"v13plus": extremes(v13), "v12": extremes(v12)}

    # cohort by publish quarter × window median
    def quarter(dstr):
        y, m = int(dstr[:4]), int(dstr[5:7])
        return f"{y}-Q{(m - 1) // 3 + 1}"
    cohorts = {}
    for o in covered:
        cohorts.setdefault(quarter(o["date"]), []).append(o)
    cohort_tbl = []
    for q in sorted(cohorts):
        rows = cohorts[q]
        row = {"quarter": q, "n": len(rows)}
        for wk in windows:
            row[wk] = agg_group(rows, wk)
        cohort_tbl.append(row)

    # latest-verdict-per-ticker dedup
    latest = {}
    for o in covered:
        cur = latest.get(o["ticker"])
        if cur is None or o["date"] > cur["date"]:
            latest[o["ticker"]] = o
    latest_rows = list(latest.values())
    latest_tbl = {
        "n_tickers": len(latest_rows),
        "v13plus": group_table([r for r in latest_rows if r["era"] == "v13plus"],
                               ["進場", "觀望", "迴避"]),
        "v12": group_table([r for r in latest_rows if r["era"] == "v12"],
                           ["A+", "A", "B", "C", "X"]),
    }
    return tables, extr, cohort_tbl, latest_tbl


# ── HTML rendering ──
def extract_canonical():
    """Pull byte-identical font links + token block + nav + footer from canonical."""
    s = open(CANONICAL, encoding="utf-8").read()
    def grab(pat):
        m = re.search(pat, s, re.S)
        if not m:
            raise RuntimeError(f"canonical anchor not found: {pat[:40]}")
        return m.group(0)
    fonts_tokens = s[s.index('<link rel="preconnect"'):
                     s.index('.mono{font-family:var(--imq-font-mono)}')
                     + len('.mono{font-family:var(--imq-font-mono)}')]
    nav_style = grab(r'<style id="imq-nav-style">.*?</style>')
    nav_header = grab(r'<header class="imq-nav-root">.*?</header>')
    nav_script = grab(r'<script>\(function\(\)\{document\.querySelectorAll\(\'\.imq-dd-btn\'\).*?\}\)\(\);</script>')
    footer = grab(r'<footer class="imq-foot">.*?</footer>')
    return fonts_tokens, nav_style, nav_header, nav_script, footer


PAGE_CSS = """
/* ── track-record page ── */
.tr-wrap{max-width:1160px;margin:0 auto;padding:16px 32px 40px}
.tr-hero{max-width:1160px;margin:0 auto;padding:44px 32px 26px}
.tr-overline{font-family:var(--imq-font-mono);font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:14px}
.tr-title{font-family:'Noto Serif TC',Georgia,serif;font-weight:700;letter-spacing:-.01em;color:var(--ink);font-size:36px;line-height:1.18;margin-bottom:12px}
.tr-title em{font-style:italic;font-family:'Playfair Display','Noto Serif TC',Georgia,serif;color:var(--accent);font-weight:600}
.tr-lede{font-size:15px;color:var(--sec);max-width:720px;line-height:1.7;margin-bottom:18px}
.tr-statline{display:flex;flex-wrap:wrap;gap:10px 22px;align-items:center;font-family:var(--imq-font-mono);font-size:12.5px;color:var(--body);padding:12px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.tr-statline b{color:var(--accent);font-weight:700;font-size:15px}
.tr-statline .sep{color:var(--gold);opacity:.7}
.tr-sec{margin-top:38px}
.tr-sec-head{font-family:'Noto Serif TC',Georgia,serif;font-size:22px;font-weight:700;color:var(--ink);letter-spacing:-.01em;margin-bottom:6px;display:flex;align-items:baseline;gap:10px}
.tr-sec-head .num{font-family:var(--imq-font-mono);font-size:13px;color:var(--gold-deep);font-weight:600}
.tr-sec-sub{font-size:13.5px;color:var(--sec);line-height:1.7;margin-bottom:16px;max-width:820px}
.tr-note{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:var(--r);padding:14px 18px;font-size:13px;color:var(--body);line-height:1.75;margin:14px 0}
.tr-note b{color:var(--ink)}
.tr-note ul{margin:8px 0 0;padding-left:20px}
.tr-note li{margin:4px 0}
.tr-tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--card);margin:12px 0}
table.tr{border-collapse:collapse;width:100%;font-size:12.5px;min-width:640px}
table.tr caption{text-align:left;font-family:'Noto Serif TC',Georgia,serif;font-weight:700;color:var(--ink);font-size:15px;padding:14px 16px 4px}
table.tr th,table.tr td{padding:8px 12px;text-align:right;border-bottom:1px solid var(--line-soft);white-space:nowrap}
table.tr th{font-family:var(--imq-font-mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600;background:var(--paper);position:sticky;top:0}
table.tr td.lab,table.tr th.lab{text-align:left;font-weight:600;color:var(--ink)}
table.tr td.mono{font-family:var(--imq-font-mono)}
table.tr tr.grp-total td{background:var(--paper);font-weight:600}
.pos{color:var(--imq-green)}
.neg{color:var(--imq-rose)}
.mut{color:var(--muted)}
.vpill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:11.5px;font-weight:600;font-family:var(--imq-font-sans)}
.v-enter{background:rgba(15,110,86,.12);color:var(--imq-green)}
.v-watch{background:rgba(180,83,9,.12);color:var(--imq-amber)}
.v-avoid{background:rgba(192,57,43,.12);color:var(--imq-rose)}
.v-grade{background:var(--paper);color:var(--body);border:1px solid var(--line)}
.tr-strip{display:flex;flex-wrap:wrap;gap:22px;margin:14px 0}
.tr-strip .col{flex:1;min-width:280px}
.tr-strip h4{font-family:var(--imq-font-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:8px;font-weight:600}
ol.exlist{list-style:none;padding:0;margin:0}
ol.exlist li{display:flex;justify-content:space-between;gap:10px;padding:6px 10px;border-bottom:1px solid var(--line-soft);font-size:12.5px}
ol.exlist li .tk{font-weight:600;color:var(--ink)}
ol.exlist li .dt{color:var(--muted);font-family:var(--imq-font-mono);font-size:11px}
ol.exlist li .rt{font-family:var(--imq-font-mono);font-weight:600}
.tr-cal{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px 22px;margin:14px 0;line-height:1.85;font-size:13.5px;color:var(--body)}
.tr-cal h4{font-family:'Noto Serif TC',Georgia,serif;font-size:16px;color:var(--ink);margin-bottom:8px}
.tr-foot-disc{margin-top:40px;font-size:12.5px;color:var(--muted);line-height:1.8;border-top:1px solid var(--line);padding-top:18px}
@media(max-width:768px){.tr-hero,.tr-wrap{padding-left:16px;padding-right:16px}.tr-title{font-size:28px}}
"""


def cell_ret(v):
    if v is None:
        return '<td class="mono mut">—</td>'
    cls = "pos" if v > 0 else ("neg" if v < 0 else "mut")
    sign = "+" if v > 0 else ""
    return f'<td class="mono {cls}">{sign}{v:.1f}%</td>'


def cell_pct(v, good_high=True):
    if v is None:
        return '<td class="mono mut">—</td>'
    return f'<td class="mono">{v:.0f}%</td>'


VLABEL = {"進場": ("進場", "v-enter"), "觀望": ("觀望", "v-watch"),
          "迴避": ("迴避", "v-avoid")}


def vpill(g):
    if g in VLABEL:
        lab, cls = VLABEL[g]
        return f'<span class="vpill {cls}">{lab}</span>'
    return f'<span class="vpill v-grade">{html.escape(str(g))}</span>'


def render_dist_table(groups, order, title, us_only_note=True):
    """One era's verdict × window distribution table."""
    wins = [("d30", "+30 日"), ("d90", "+90 日"), ("d180", "+180 日"), ("todate", "至今")]
    rows = []
    for g in order:
        gd = groups.get(g)
        if not gd or gd["n_reports"] == 0:
            continue
        cells = [f'<td class="lab">{vpill(g)}</td>',
                 f'<td class="mono">{gd["n_reports"]}</td>']
        for wk, _ in wins:
            w = gd["windows"][wk]
            n = w["n"]
            med = w["median"]
            iqr = (f'{w["p25"]:.0f}~{w["p75"]:.0f}'
                   if w["p25"] is not None else "—")
            posp = w["pct_positive"]
            beat = w["pct_beat_spy"]
            medcell = cell_ret(med)[4:-5] if med is not None else "—"
            medcls = "pos" if (med is not None and med > 0) else ("neg" if (med is not None and med < 0) else "mut")
            sub = (f'<div class="mono {medcls}" style="font-weight:600">'
                   f'{("+" if (med is not None and med>0) else "")}{med:.1f}%</div>'
                   if med is not None else '<div class="mono mut">—</div>')
            iqrline = f'<div class="mut mono" style="font-size:10.5px">IQR {iqr}</div>' if med is not None else ''
            posline = (f'<div class="mono" style="font-size:10.5px">正報酬 {posp:.0f}%'
                       + (f' · 勝 SPY {beat:.0f}%' if beat is not None else '')
                       + '</div>') if n else ''
            cells.append(f'<td style="text-align:right">'
                         f'<div class="mut mono" style="font-size:10px">N={n}</div>'
                         f'{sub}{iqrline}{posline}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    head = ('<tr><th class="lab">裁決</th><th>報告數</th>'
            + "".join(f'<th>{lab}<br>中位／IQR／勝率</th>' for _, lab in wins) + "</tr>")
    return (f'<div class="tr-tablewrap"><table class="tr"><caption>{title}</caption>'
            f'<thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>')


def render_extremes(extr, era_label):
    def lst(items):
        out = []
        for r in items:
            rt = r["ret_todate"]
            cls = "pos" if (rt is not None and rt > 0) else "neg"
            sign = "+" if (rt is not None and rt > 0) else ""
            exc = (f' <span class="mut" style="font-size:10.5px">(超額 {("+" if r["exc_todate"]>0 else "")}{r["exc_todate"]:.0f}%)</span>'
                   if r["exc_todate"] is not None else
                   ' <span class="mut" style="font-size:10.5px">(非美股·無基準)</span>')
            out.append(f'<li><span><span class="tk">{html.escape(r["ticker"])}</span> '
                       f'{vpill(r["group"])} <span class="dt">{r["date"]}</span></span>'
                       f'<span class="rt {cls}">{sign}{rt:.0f}%{exc}</span></li>')
        return "<ol class='exlist'>" + "".join(out) + "</ol>"
    return (f'<div class="tr-strip">'
            f'<div class="col"><h4>{era_label}·至今報酬最高 5 檔</h4>{lst(extr["best"])}</div>'
            f'<div class="col"><h4>{era_label}·至今報酬最低 5 檔</h4>{lst(extr["worst"])}</div>'
            f'</div>')


def render_cohort(cohort_tbl):
    rows = []
    for c in cohort_tbl:
        cells = [f'<td class="lab">{c["quarter"]}</td>', f'<td class="mono">{c["n"]}</td>']
        for wk in ["d30", "d90", "d180", "todate"]:
            w = c[wk]
            med = w["median"]
            cells.append(f'<td style="text-align:right"><div class="mut mono" style="font-size:10px">N={w["n"]}</div>'
                         + (f'<div class="mono {"pos" if med>0 else "neg" if med<0 else "mut"}">{("+" if med>0 else "")}{med:.1f}%</div>' if med is not None else '<div class="mono mut">—</div>')
                         + '</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    head = ('<tr><th class="lab">發布季度</th><th>報告數</th>'
            '<th>+30 日<br>中位</th><th>+90 日<br>中位</th><th>+180 日<br>中位</th><th>至今<br>中位</th></tr>')
    return (f'<div class="tr-tablewrap"><table class="tr">'
            f'<caption>依發布季度分組（全體，跨裁決系統合併——僅供時點觀察，非裁決比較）</caption>'
            f'<thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>')


def render_html(payload, tables, extr, cohort_tbl, latest_tbl):
    fonts_tokens, nav_style, nav_header, nav_script, footer = extract_canonical()
    meta = payload["meta"]
    as_of = meta["data_as_of"]

    main_v13 = render_dist_table(tables["v13plus"], ["進場", "觀望", "迴避"],
                                 "v13／v14 era — 統一裁決（進場／觀望／迴避）× 前瞻窗口")
    main_v12 = render_dist_table(tables["v12"], ["A+", "A", "B", "C", "X"],
                                 "legacy v12 era — 基本面評級（A+／A／B／C／X，非行動裁決）× 前瞻窗口")
    latest_v13 = render_dist_table(latest_tbl["v13plus"], ["進場", "觀望", "迴避"],
                                   "每檔最新裁決去重 — v13／v14 era")
    latest_v12 = render_dist_table(latest_tbl["v12"], ["A+", "A", "B", "C", "X"],
                                   "每檔最新裁決去重 — legacy v12 era")

    doc = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>裁決實績 Track Record · 回顧性統計 — InvestMQuest Research</title>
  <meta name="description" content="本站個股 DD 裁決的回顧性前瞻報酬統計——每個裁決都計入、無挑選、雙裁決系統分era 呈現。描述器語言，非績效宣傳。">
  {fonts_tokens}
{PAGE_CSS}
  </style>
{nav_style}
</head>
<body>
{nav_header}
{nav_script}

<section class="tr-hero">
  <div class="tr-overline">TRACK RECORD · 回顧性裁決實績</div>
  <h1 class="tr-title">裁決實績 <em>Track Record</em></h1>
  <p class="tr-lede">「這些裁決後來兌現了嗎？」——本頁以前瞻報酬統計回答此問。這是<b>回顧性描述，非績效宣傳、非未來報酬預測</b>；每一份帶結構化裁決與價格錨的報告都計入，無挑選、無事後刪除。贏家與輸家永遠並列呈現。報酬以還原股價週線收盤計算，粒度為週。</p>
  <div class="tr-statline">
    <span><b>{meta['n_reports_total']}</b> 份 DD 報告</span><span class="sep">·</span>
    <span><b>{meta['n_observations']}</b> 個裁決觀察納入</span><span class="sep">·</span>
    <span><b>{meta['n_tickers']}</b> 檔標的</span><span class="sep">·</span>
    <span>資料截至 <b>{as_of}</b>（週線）</span>
  </div>
</section>

<div class="tr-wrap">

  <section class="tr-sec" id="method">
    <div class="tr-sec-head"><span class="num">01</span>方法論</div>
    <div class="tr-sec-sub">如何計算、窗口定義、基準、覆蓋率與已知侷限——全部明說。</div>
    <div class="tr-note">
      <b>報酬計算：</b>全程採 <b>還原股價</b>（auto_adjust，含股息／拆股還原）以確保基期與前瞻端在同一價格尺度。基期＝發布日「當日或之前最近一根週線收盤」（＝發布時點的已知還原收盤價）；<b>不直接採報告內的原始成交價 <span class="mono">price_at_dd</span></b>，因為若標的在發布後發生拆股（如 KLAC／CRWD），原始價與還原收盤價將不同尺度而使報酬嚴重失真。前瞻報酬取發布日 +30／+90／+180 日曆日目標日「當日或之後最近一根週線收盤」，另加「至今」（最新週線收盤，{as_of}）。本輪有 {meta['n_split_rebased']} 個觀察偵測到發布後拆股／大額股息、已自動改以還原基期計算。
      <ul>
        <li><b>窗口尚未走完即排除：</b>若某窗口目標日超過資料截止日，該觀察不計入該窗口——各窗口只呈現「可觀察 N」。<b>本 DD 語料自 2026-03 才起步、多數報告發布於近月</b>，故 +90／+180 日窗口在全語料層級皆尚未走完、可觀察樣本極少（v13／v14 era 更全數落在近月，+30 日窗口亦尚未走完，僅「至今」可觀察）。目前訊號主要由「至今」與 legacy +30 日承載；請勿以個位數樣本外推，隨時間經過本表 N 值會自然充實。</li>
        <li><b>基準（僅美股）：</b>美股標的以同窗口 SPY 還原報酬計超額；勝率＝該組超額為正的比例。<b>非美股（.TW／.T／.AX／.SW 等）僅報絕對報酬，不強套 SPY 超額</b>（基準錯配已標註）。</li>
        <li><b>週線粒度侷限：</b>基期為 price_at_dd（發布時點價），前瞻端為週線收盤，兩者非同一交易時點；SPY 基期取發布日之後最近週線收盤。此為週粒度近似，非逐日精算。</li>
        <li><b>覆蓋：</b>{meta['n_reports_total']} 份報告中 {meta['n_with_meta']} 份帶結構化 dd-meta 與價格錨（納入）；{meta['n_excluded_nometa']} 份早期 v9 版無結構化 metadata／無價格錨（<b>排除並在此揭露</b>，非事後刪除輸家）。價格覆蓋：{meta['n_price_covered']} 個觀察取得歷史價，{meta['n_price_uncovered']} 個因價格資料缺失排除報酬計算（多為海外冷門標的）。</li>
      </ul>
    </div>
  </section>

  <section class="tr-sec" id="main">
    <div class="tr-sec-head"><span class="num">02</span>主表：裁決 × 窗口 分布統計</div>
    <div class="tr-sec-sub">每格呈現該窗口的可觀察 N、報酬中位數、IQR（p25～p75）、正報酬比例，美股另附勝 SPY 比例。中位數與 IQR 比平均數更抗離群值。</div>
    {main_v13}
    <div class="tr-note" style="border-left-color:var(--accent)">
      <b>兩套裁決系統不可混比。</b>v13／v14 era（2026-06-22 起）輸出<b>統一行動裁決</b>：進場／觀望／迴避。legacy v12 era 的 <span class="mono">signal</span> 是 <b>A+／A／B／C／X 基本面評級</b>（餵 screener 的品質分級），<b>語義完全不同、不是買賣裁決</b>。兩者分表呈現，不合併、不跨系統排名。
    </div>
    {main_v12}
  </section>

  <section class="tr-sec" id="extremes">
    <div class="tr-sec-head"><span class="num">03</span>最佳與最差（永遠並列）</div>
    <div class="tr-sec-sub">依「至今」報酬排序，每個 era 各列最高 5 與最低 5——贏家與輸家一起看，不單獨秀贏家。</div>
    {render_extremes(extr['v13plus'], 'v13／v14')}
    {render_extremes(extr['v12'], 'legacy v12')}
  </section>

  <section class="tr-sec" id="cohort">
    <div class="tr-sec-head"><span class="num">04</span>依發布季度分組（cohort）</div>
    <div class="tr-sec-sub">不同時點發布的報告面對不同的後續市場環境；此表僅供時點效應觀察，跨裁決系統合併故不代表裁決品質比較。</div>
    {render_cohort(cohort_tbl)}
  </section>

  <section class="tr-sec" id="dedup">
    <div class="tr-sec-head"><span class="num">05</span>每檔最新裁決去重（次表）</div>
    <div class="tr-sec-sub">同一標的可能有多份報告；此表每檔只取最新一份裁決，避免高頻覆蓋標的在主表中被重複計數。</div>
    {latest_v13}
    {latest_v12}
  </section>

  <section class="tr-sec" id="calibration">
    <div class="tr-sec-head"><span class="num">06</span>誠實校準紀錄——裁決函數的演進</div>
    <div class="tr-cal">
      <h4>為什麼公開這一段</h4>
      <p>裁決系統會犯錯，把錯誤攤在陽光下、並記錄如何修正，是本頁存在的理由之一。</p>
      <p style="margin-top:12px"><b>2026-07 內部校準發現：</b>legacy 裁決在約 60 日窗口曾呈現<b>倒序</b>傾向——較保守的裁決在部分名字上錯過了尾部大漲，較樂觀的裁決則在另一些名字上躲掉了尾部大跌。換言之，當時的僵化閘門（如 MA 軟否決、AR≥4、動能過熱這類）共同的缺陷是<b>不可證偽</b>：沒有人追蹤它們擋掉的名字後來如何，所以錯誤能安穩存活。</p>
      <p style="margin-top:12px"><b>修正：</b>此發現促成 v14.6 裁決規則重構與數條僵化閘門退役，並確立「判斷類規則必須登記 kill condition、加一提刪一、每輪校準回填審計」的治理鐵律。門檻於上線時凍結（PREREG）至下一輪校準，避免因單一案例臨時調參過擬合。</p>
      <p style="margin-top:12px" class="mut">教條與紀律的分界＝可證偽性。本頁的統計本身，就是讓現行裁決函數持續可被證偽的公開帳本。</p>
    </div>
  </section>

  <div class="tr-foot-disc">
    <b>免責：</b>本頁為回顧性統計描述，非投資建議、非績效保證、非未來報酬預測。過往裁決的前瞻報酬不預示任何標的的未來表現，亦不構成任何買賣指示。報酬以週線收盤近似計算，非可交易之實際成交價。完整方法論與揭露見 <a href="/disclosures.html">方法論與揭露</a>。
  </div>

</div>

<script id="track-record-data" type="application/json">
{json.dumps(payload, ensure_ascii=False)}
</script>

{footer}
</body>
</html>
"""
    return doc


def main():
    ap = argparse.ArgumentParser(description="Public track-record scoreboard builder")
    ap.add_argument("--no-fetch", action="store_true",
                    help="skip yfinance fetch (offline); uncovered names excluded")
    args = ap.parse_args()

    print("Parsing DD reports…")
    obs, excluded = parse_dds()
    n_with_meta = len(obs)
    n_excluded_nometa = sum(1 for _, r in excluded if "no dd-meta" in r)
    print(f"  {n_with_meta} with dd-meta · {len(excluded)} excluded "
          f"({n_excluded_nometa} v9-era no-meta)")

    weekly = load_weekly_series()
    # tickers absent from weekly_cache
    missing = sorted({o["ticker"] for o in obs if o["ticker"] not in weekly})
    need = {t: NONUS_MAP.get(t, t) for t in missing}
    need["SPY"] = "SPY"  # always refresh SPY into own cache for freshness/alignment
    if args.no_fetch:
        print("  --no-fetch: skipping yfinance")
        own = load_json(OWN_CACHE, {}) or {"series": {}}
    else:
        print(f"Fetching {len(need)} symbols into own cache (SPY + {len(missing)} uncovered)…")
        own = fetch_missing(need)
    own_series = own.get("series") or {}
    spy = load_spy()

    as_of = compute(obs, weekly, own_series, spy)
    n_cov = sum(1 for o in obs if o.get("price_covered"))
    n_unc = n_with_meta - n_cov
    print(f"  price-covered {n_cov} · uncovered {n_unc} · data as-of {as_of}")

    tables, extr, cohort_tbl, latest_tbl = build_tables(obs)

    payload = {
        "meta": {
            "built_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data_as_of": as_of,
            "spy_as_of": spy[-1][0] if spy else None,
            "n_reports_total": n_with_meta + len(excluded),
            "n_with_meta": n_with_meta,
            "n_observations": n_cov,
            "n_price_covered": n_cov,
            "n_price_uncovered": n_unc,
            "n_excluded_nometa": n_excluded_nometa,
            "n_tickers": len({o["ticker"] for o in obs}),
            "n_split_rebased": sum(1 for o in obs if o.get("split_rebased")),
            "windows_days": {w: d for w, d in WINDOWS},
            "note": "回顧性描述統計；還原股價週線；非美股僅絕對報酬；描述器語言非投資建議。",
        },
        "tables": tables,
        "extremes": extr,
        "cohorts": cohort_tbl,
        "latest_dedup": latest_tbl,
        "excluded_examples": [{"file": f, "reason": r} for f, r in excluded[:20]],
        "uncovered_price": sorted({o["ticker"] for o in obs if not o.get("price_covered")}),
    }

    ch_json = write_json_if_changed(OUT_JSON, payload)
    print(f"  {'wrote' if ch_json else 'unchanged'} {os.path.relpath(OUT_JSON, ROOT)}")

    doc = render_html(payload, tables, extr, cohort_tbl, latest_tbl)
    ch_html = write_if_changed(OUT_HTML, doc,
                               volatile_re=r'"built_at":\s*"[^"]*"')
    print(f"  {'wrote' if ch_html else 'unchanged'} {os.path.relpath(OUT_HTML, ROOT)}")
    print("Done.")


if __name__ == "__main__":
    main()
