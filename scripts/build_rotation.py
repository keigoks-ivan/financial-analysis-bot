#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sector Rotation Monitor — weekly data pipeline.

Sibling of build_crowding.py.  Recomputes the RRG (Relative Rotation Graph)
rotation dataset over the site's own Industry-DD themes and emits one contract
JSON (docs/rotation/data/latest.json) plus a compact HTML dashboard block
injected into docs/rotation/index.html between the ROTATION_AUTO_DASH_START /
_END markers.

Compute (ported from the pilot compute_rrg.py)
----------------------------------------------
  * Per-theme equal-weight total-return index vs SPY benchmark.
  * JdK-style RS-Ratio (26w) and RS-Momentum (10w), centred at 100.
  * Quadrant (leading / weakening / lagging / improving), 7-week tail.
  * Breadth: % members above their own 40w MA.
  * Revision breadth: % members with FY1 EPS upward revision (dd-screener).
  * GRP picks landing per theme (official / candidate長熬/爆發).

Data sources
------------
  weekly_cache (read-only) · docs/id id-meta themes · docs/dd-screener FY1
  revisions · docs/picks GRP list · SPY benchmark (yfinance -> stooq fallback,
  cached incrementally in data/rotation_bench.json).

CLI
---
  python scripts/build_rotation.py            full weekly refresh (default)
  python scripts/build_rotation.py --skip-fetch   offline: recompute from
                                                    existing caches only

Design contracts (identical to build_crowding.py)
-------------------------------------------------
  * Zero churn: JSON emitted with sorted keys + fixed decimals; volatile
    timestamp fields are stripped before the on-disk comparison, so a no-op
    week produces an empty diff / no write.
  * data/weekly_cache is read-only (multi-consumer, zero-churn protocol).
  * Fault tolerance: benchmark fetch is warn-and-continue with cache fallback;
    the process exits non-zero only if it cannot rank any theme at all.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
DATA = os.path.join(ROOT, "data")
WEEKLY_CACHE = os.path.join(DATA, "weekly_cache")
BENCH_CACHE = os.path.join(DATA, "rotation_bench.json")
OUT_DIR = os.path.join(ROOT, "docs", "rotation")
OUT_JSON = os.path.join(OUT_DIR, "data", "latest.json")
INDEX_HTML = os.path.join(OUT_DIR, "index.html")
DASH_START = "<!-- ROTATION_AUTO_DASH_START -->"
DASH_END = "<!-- ROTATION_AUTO_DASH_END -->"

BENCH = "SPY"          # broad-market benchmark for sector RRG
SMA_RATIO = 26         # half-year trend window for RS-Ratio
SMA_MOM = 10           # momentum-of-ratio window
TAIL = 7               # trajectory tail points (weeks)
BREADTH_MA = 40        # 40-week MA breadth
WINDOW_WEEKS = 140     # analysis window (~2.7y) to leave SMA lookback

sys.path.insert(0, SCRIPTS)

_ID_META_RE = re.compile(
    r'id=["\']id-meta["\'][^>]*>(.*?)</script>', re.S)


def warn(msg: str) -> None:
    print(f"[rotation][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[rotation] {msg}")


# ───────────────────────────────────────────────────────────────────────────
# Zero-churn IO (identical protocol to build_crowding.py)
# ───────────────────────────────────────────────────────────────────────────

def _serialize(obj) -> str:
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


def write_json_if_changed(path, obj, volatile=("generated_at", "built_at", "generated")) -> bool:
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_serialize(obj))
    return True


# ───────────────────────────────────────────────────────────────────────────
# Network helpers (lazy imports; tolerant) — SPY benchmark
# ───────────────────────────────────────────────────────────────────────────

def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout,
                         headers={"User-Agent": "Mozilla/5.0 rotation-monitor"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 rotation-monitor"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


def _yf_weekly_bench(ticker, period="5y"):
    """Weekly SPY series via yfinance -> [(week_end, close), ...] or None."""
    import yfinance as yf
    import pandas as pd
    df = yf.download(ticker, period=period, interval="1wk", auto_adjust=True,
                     progress=False, threads=False)
    if df is None or len(df) == 0:
        return None
    close = df["Close"]
    if isinstance(close, pd.DataFrame):  # MultiIndex columns -> take first
        close = close.iloc[:, 0]
    out = []
    for idx, val in close.items():
        try:
            c = float(val)
        except (TypeError, ValueError):
            continue
        if c != c:  # NaN
            continue
        out.append((idx.date().isoformat(), round(c, 4)))
    return out or None


def _stooq_weekly_bench(ticker):
    sym = ticker.lower()
    if "." not in sym:
        sym = sym + ".us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=w"
    try:
        raw = _http_get(url, timeout=30).decode("utf-8", "replace")
    except Exception:
        return None
    lines = raw.strip().splitlines()
    if len(lines) < 2 or not lines[0].lower().startswith("date"):
        return None
    rows = []
    for ln in lines[1:]:
        parts = ln.split(",")
        if len(parts) < 5:
            continue
        try:
            rows.append((parts[0], round(float(parts[4]), 4)))
        except ValueError:
            continue
    return rows or None


def load_benchmark(skip_fetch):
    """Incrementally refresh the SPY benchmark weekly series.  Returns
    [(week_end, close), ...] sorted, or None if unavailable."""
    cache = load_json(BENCH_CACHE, {"meta": {}, "series": []})
    have = {d for d, _ in cache.get("series", [])}
    fetched = None
    if not skip_fetch:
        try:
            import yfinance  # noqa: F401
        except ImportError:
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", "-q",
                             "yfinance>=0.2.40", "pandas"])
        period = "5y" if not have else "3mo"
        for attempt in range(3):
            try:
                fetched = _yf_weekly_bench(BENCH, period=period)
                if fetched:
                    break
            except Exception as e:
                warn(f"yfinance {BENCH} attempt {attempt+1} failed: {e}")
        if not fetched:
            info(f"benchmark: yfinance empty, trying stooq fallback for {BENCH}")
            fetched = _stooq_weekly_bench(BENCH)
    if fetched:
        merged = {d: c for d, c in cache.get("series", [])}
        for d, c in fetched:
            merged[d] = c
        cache["series"] = sorted(merged.items())
        cache["meta"] = {
            "ticker": BENCH,
            "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "n_weeks": len(cache["series"]),
            "note": "weekly close benchmark for rotation RRG; yfinance->stooq; incremental.",
        }
        wrote = write_json_if_changed(BENCH_CACHE, cache)
        info(f"benchmark cache: {len(cache['series'])} weeks, {'written' if wrote else 'no change'}")
    series = cache.get("series") or []
    if not series:
        warn("benchmark series unavailable (no cache and fetch skipped/failed)")
        return None
    return [(d, c) for d, c in series]


# ───────────────────────────────────────────────────────────────────────────
# Site data layers: themes (id-meta), weekly closes, revisions, picks
# ───────────────────────────────────────────────────────────────────────────

def load_themes():
    """Read id-meta themes.  Dedup: keep the variant with most related_tickers,
    then latest publish_date.  Returns list of theme dicts with tickers + tags."""
    id_dir = os.path.join(ROOT, "docs", "id")
    by_theme = {}
    for p in sorted(glob.glob(os.path.join(id_dir, "ID_*.html"))):
        try:
            txt = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        m = _ID_META_RE.search(txt)
        if not m:
            continue
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        th = meta.get("theme")
        if not th:
            continue
        rts = [r.get("ticker") for r in (meta.get("related_tickers") or []) if r.get("ticker")]
        rts = list(dict.fromkeys(rts))
        key = (len(rts), meta.get("publish_date", ""))
        rec = {
            "theme": th,
            "file": os.path.basename(p),
            "tickers": rts,
            "ntick": len(rts),
            "sd_verdict": meta.get("sd_verdict"),
            "clock_phase": meta.get("clock_phase"),
            "conviction": meta.get("conviction"),
        }
        if th not in by_theme or key > by_theme[th][0]:
            by_theme[th] = (key, rec)
    return [v[1] for v in by_theme.values()]


def load_weekly_closes():
    """{ticker: [(week_end, close), ...]} from data/weekly_cache (read-only)."""
    closes = {}
    for f in glob.glob(os.path.join(WEEKLY_CACHE, "*.json")):
        d = load_json(f)
        if not d:
            continue
        tk = d.get("ticker")
        bars = d.get("weekly_bars") or []
        pts = [(b["week_end"], b["close"]) for b in bars if b.get("close") is not None]
        if tk and len(pts) >= 60:
            closes[tk] = sorted(pts)
    return closes


def load_revisions():
    scr = load_json(os.path.join(ROOT, "docs", "dd-screener", "latest.json"), {})
    rev = {}
    for s in scr.get("stocks", []):
        v = s.get("eps_fy_curr_revision_pct")
        if v is not None:
            rev[s["ticker"]] = v
    return rev


def load_picks():
    pk = load_json(os.path.join(ROOT, "docs", "picks", "candidates.json"), {})
    tier_lbl = {"official_changhao": "官方長熬", "official_baofa": "官方爆發",
                "changhao": "候選長熬", "baofa": "候選爆發"}
    pick_map = {}
    for grp, lbl in tier_lbl.items():
        for x in pk.get(grp, []):
            e = pick_map.setdefault(x["ticker"], {"groups": [], "grps": []})
            e["groups"].append(lbl)
            e["grps"].append(grp)
    return pick_map


# ───────────────────────────────────────────────────────────────────────────
# RRG compute (ported from pilot compute_rrg.py)
# ───────────────────────────────────────────────────────────────────────────

def quadrant(ratio, mom):
    if ratio >= 100 and mom >= 100:
        return "leading"
    if ratio >= 100 and mom < 100:
        return "weakening"
    if ratio < 100 and mom < 100:
        return "lagging"
    return "improving"


def compute_rotation(themes, closes, bench_pts, rev, pick_map):
    import pandas as pd
    import numpy as np

    def to_series(pts):
        idx = [pd.Timestamp(d) for d, _ in pts]
        return pd.Series([float(c) for _, c in pts], index=idx).sort_index()

    bench = to_series(bench_pts)
    cache = {t: to_series(pts) for t, pts in closes.items()}

    grid = bench.index[-WINDOW_WEEKS:]
    bench_g = bench.reindex(grid).interpolate().ffill().bfill()
    bench_norm = bench_g / bench_g.iloc[0] * 100.0

    def align(s):
        return s.reindex(grid, method="nearest", tolerance=pd.Timedelta("6D"))

    results = []
    for th in themes:
        name = th["theme"]
        members = th["tickers"]
        n_mem = len(members)
        cov = [t for t in members if t in cache]
        aligned = {}
        for t in cov:
            a = align(cache[t])
            if a.notna().sum() >= WINDOW_WEEKS * 0.6:
                aligned[t] = a.ffill().bfill()
        n_cov = len(aligned)
        entry = {
            "theme": name, "file": th["file"], "n_members": n_mem, "n_cache_cov": n_cov,
            "cov_ratio": round(n_cov / n_mem, 3) if n_mem else 0,
            "sd_verdict": th.get("sd_verdict"), "clock_phase": th.get("clock_phase"),
            "conviction": th.get("conviction"),
        }
        if n_mem < 4 or n_cov < 3:
            entry["status"] = "insufficient_coverage"
            results.append(entry)
            continue

        norm = []
        for t, a in aligned.items():
            base = a.iloc[0]
            if base and base > 0:
                norm.append(a / base * 100.0)
        ew = pd.concat(norm, axis=1).mean(axis=1)
        rs = 100.0 * ew / bench_norm
        rmean = rs.rolling(SMA_RATIO).mean()
        rstd = rs.rolling(SMA_RATIO).std()
        rs_ratio = 100.0 + (rs - rmean) / rstd
        mmean = rs_ratio.rolling(SMA_MOM).mean()
        mstd = rs_ratio.rolling(SMA_MOM).std()
        rs_mom = 100.0 + (rs_ratio - mmean) / mstd

        valid = pd.concat([rs_ratio, rs_mom], axis=1).dropna()
        if len(valid) < TAIL + 1:
            entry["status"] = "insufficient_history"
            results.append(entry)
            continue
        tail = valid.iloc[-TAIL:]
        trail = [{"ratio": round(float(r), 3), "mom": round(float(m), 3),
                  "wk": d.strftime("%Y-%m-%d")} for d, (r, m) in zip(tail.index, tail.values)]
        cur_ratio = float(tail.iloc[-1, 0])
        cur_mom = float(tail.iloc[-1, 1])

        above = 0
        bcnt = 0
        for t in aligned:
            ss = cache[t]
            if len(ss) >= BREADTH_MA:
                ma = ss.rolling(BREADTH_MA).mean().iloc[-1]
                if not math.isnan(ma):
                    bcnt += 1
                    if ss.iloc[-1] > ma:
                        above += 1
        breadth = round(100 * above / bcnt, 1) if bcnt else None

        rmem = [rev[t] for t in members if t in rev]
        rev_up = round(100 * sum(1 for v in rmem if v > 0) / len(rmem), 1) if rmem else None
        rev_med = round(float(np.median(rmem)), 2) if rmem else None

        theme_picks = []
        for t in members:
            if t in pick_map:
                for g in pick_map[t]["groups"]:
                    theme_picks.append({"ticker": t, "group": g})

        entry.update({
            "status": "ok", "benchmark": BENCH,
            "rs_ratio": round(cur_ratio, 3), "rs_mom": round(cur_mom, 3),
            "quadrant": quadrant(cur_ratio, cur_mom),
            "trail": trail, "breadth_ma40": breadth, "n_breadth": bcnt,
            "rev_up_frac": rev_up, "rev_med": rev_med, "n_rev": len(rmem),
            "ret_12m": round(float(ew.iloc[-1] / ew.iloc[-53] - 1) * 100, 1) if len(ew) > 53 else None,
            "picks": theme_picks,
        })
        results.append(entry)

    ok = [r for r in results if r["status"] == "ok"]
    ok.sort(key=lambda r: (-r["rs_ratio"], -r["rs_mom"]))
    insuff = [r for r in results if r["status"] != "ok"]
    data_asof = grid[-1].strftime("%Y-%m-%d")
    return ok, insuff, results, data_asof


# ───────────────────────────────────────────────────────────────────────────
# HTML dashboard injection (compact — mirrors crowding dashboard density)
# ───────────────────────────────────────────────────────────────────────────

QZH = {"leading": "領先", "weakening": "走弱", "lagging": "落後", "improving": "改善"}
QCOL = {"leading": "#12b312", "weakening": "#f0a825", "lagging": "#e66767", "improving": "#3987e5"}


def _short_name(name):
    for cut in ["（", "(", " — ", " ("]:
        if cut in name:
            name = name.split(cut)[0]
    return name.strip()


def _esc(s):
    import html
    return html.escape(str(s))


def render_dashboard(payload):
    themes = payload["themes"]
    counts = payload["quadrant_counts"]
    top = themes[:6]

    st = ("font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
          "background:#12161f;border:1px solid #2a3242;border-radius:12px;"
          "padding:18px 20px;color:#e6e9ef;line-height:1.6;font-size:14px")

    def qchip(q, n):
        return (f'<span style="display:inline-block;font-family:ui-monospace,monospace;'
                f'font-size:11px;padding:2px 9px;border-radius:5px;margin:2px 4px 2px 0;'
                f'background:{QCOL[q]}22;color:{QCOL[q]};border:1px solid {QCOL[q]}55">'
                f'{QZH[q]} {n}</span>')

    qrow = "".join(qchip(q, counts.get(q, 0)) for q in
                   ("leading", "improving", "weakening", "lagging"))

    def prow(rank, t):
        q = t["quadrant"]
        picks = ""
        seen = []
        for p in t.get("picks", []):
            mk = "●" if p["group"].startswith("官方") else "○"
            s = f'{mk}{p["ticker"]}'
            if s not in seen:
                seen.append(s)
        if seen:
            picks = ('<span style="color:#8fb3ff;font-family:ui-monospace,monospace;'
                     f'font-size:10.5px;margin-left:6px">{" ".join(seen[:4])}</span>')
        brd = t.get("breadth_ma40")
        rev = t.get("rev_up_frac")
        return (
            '<tr>'
            f'<td style="padding:3px 8px;color:#9aa4b5;font-family:ui-monospace,monospace">{rank}</td>'
            f'<td style="padding:3px 8px">{_esc(_short_name(t["theme"]))}{picks}</td>'
            f'<td style="padding:3px 8px"><span style="font-size:10.5px;font-weight:700;'
            f'color:{QCOL[q]}">{QZH[q]}</span></td>'
            f'<td style="padding:3px 8px;text-align:right;font-family:ui-monospace,monospace;'
            f'font-weight:700">{t["rs_ratio"]:.1f}</td>'
            f'<td style="padding:3px 8px;text-align:right;font-family:ui-monospace,monospace;'
            f'color:#9aa4b5">{t["rs_mom"]:.1f}</td>'
            f'<td style="padding:3px 8px;text-align:right;font-family:ui-monospace,monospace;'
            f'color:#9aa4b5">{("%.0f" % brd) if brd is not None else "—"}</td>'
            f'<td style="padding:3px 8px;text-align:right;font-family:ui-monospace,monospace;'
            f'color:#9aa4b5">{("%.0f" % rev) if rev is not None else "—"}</td>'
            '</tr>')

    head = ('<tr style="color:#6b7484;font-size:10.5px;text-transform:uppercase;'
            'letter-spacing:.04em">'
            '<th style="padding:3px 8px;text-align:left">#</th>'
            '<th style="padding:3px 8px;text-align:left">主題（GRP 落點）</th>'
            '<th style="padding:3px 8px;text-align:left">象限</th>'
            '<th style="padding:3px 8px;text-align:right">RS-R</th>'
            '<th style="padding:3px 8px;text-align:right">RS-M</th>'
            '<th style="padding:3px 8px;text-align:right">廣度</th>'
            '<th style="padding:3px 8px;text-align:right">上修</th></tr>')
    body = "".join(prow(i, t) for i, t in enumerate(top, 1))

    return (
        f'{DASH_START}\n'
        f'<div style="{st}">'
        f'<div style="font-family:ui-monospace,monospace;font-size:11px;letter-spacing:.14em;'
        f'text-transform:uppercase;color:#5b9bff;margin-bottom:10px">產業輪動 · 自動儀表（RRG 相對 {BENCH}）</div>'
        f'<div style="margin-bottom:8px"><b>象限分布</b>（{payload["counts"]["ranked"]} 主題入圖）：<br>{qrow}</div>'
        f'<div style="margin:10px 0 6px"><b>相對強度 Top 6</b>（依 RS-Ratio 排序 · ●官方榜 ○候選榜）</div>'
        f'<table style="border-collapse:collapse;width:100%;font-size:12.5px">{head}{body}</table>'
        f'<div style="margin-top:12px;font-family:ui-monospace,monospace;font-size:11px;'
        f'color:#6b7484">資料截至 {payload["data_asof_weekly"]}（週線）· '
        f'更新 {payload["generated_at"][:10]} · 描述器非擇時</div>'
        f'</div>\n{DASH_END}'
    )


def inject_dashboard(payload):
    if not os.path.exists(INDEX_HTML):
        warn(f"index.html not found ({INDEX_HTML}); skipping dashboard injection")
        return
    with open(INDEX_HTML, encoding="utf-8") as f:
        html = f.read()
    if DASH_START not in html or DASH_END not in html:
        warn("dashboard markers not found in index.html; skipping injection")
        return
    pre = html.split(DASH_START)[0]
    post = html.split(DASH_END, 1)[1]
    new = pre + render_dashboard(payload) + post
    if new == html:
        info("dashboard: no change")
        return
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(new)
    info("dashboard: injected into index.html")


# ───────────────────────────────────────────────────────────────────────────
# Orchestration
# ───────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Sector rotation weekly builder")
    ap.add_argument("--skip-fetch", action="store_true",
                    help="offline: skip benchmark fetch, recompute from caches")
    args = ap.parse_args()

    themes = load_themes()
    closes = load_weekly_closes()
    rev = load_revisions()
    pick_map = load_picks()
    bench_pts = load_benchmark(args.skip_fetch)

    if not themes:
        warn("no id-meta themes found — exiting non-zero")
        sys.exit(1)
    if not bench_pts:
        warn("no benchmark series available — exiting non-zero")
        sys.exit(1)

    try:
        ok, insuff, allres, data_asof = compute_rotation(themes, closes, bench_pts, rev, pick_map)
    except Exception as e:
        warn(f"RRG compute failed: {e}")
        sys.exit(1)

    from collections import Counter
    qc = Counter(r["quadrant"] for r in ok)

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": data_asof,
        "benchmark": BENCH,
        "data_asof_weekly": data_asof,
        "quadrant_counts": dict(qc),
        "method": {
            "rs_ratio": f"JdK-style: 100+(RS-SMA(RS,{SMA_RATIO}w))/STD(RS,{SMA_RATIO}w); "
                        f"RS=100*theme_EW_total_return_index/{BENCH}",
            "rs_mom": f"100+(RS-Ratio-SMA(RS-Ratio,{SMA_MOM}w))/STD(RS-Ratio,{SMA_MOM}w)",
            "quadrants": "leading=Ratio>=100&Mom>=100 / weakening=Ratio>=100&Mom<100 / "
                         "lagging=Ratio<100&Mom<100 / improving=Ratio<100&Mom>=100",
            "breadth": f"% members above own {BREADTH_MA}w MA",
            "rev_breadth": "% members with FY1 EPS revision>0 (dd-screener eps_fy_curr_revision_pct)",
            "gate": "n_members>=4 & cache coverage>=3 else insufficient_coverage",
            "disclaimer": "描述器非擇時。相對排名於本站週線宇宙內，非市場絕對輪動。",
        },
        "counts": {"ranked": len(ok), "insufficient": len(insuff), "total": len(allres)},
        "themes": ok,
        "insufficient": insuff,
    }

    wrote = write_json_if_changed(OUT_JSON, payload)
    info(f"latest.json: {'written' if wrote else 'no change'} "
         f"(ranked {len(ok)}, insufficient {len(insuff)}, quadrants {dict(qc)})")

    inject_dashboard(payload)

    if not ok:
        warn("no theme ranked — exiting non-zero")
        sys.exit(1)
    info("done.")


if __name__ == "__main__":
    main()
