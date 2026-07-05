#!/usr/bin/env python3
"""Cross-Asset Crowding Monitor — weekly data pipeline.

Single entry point that builds four independent-but-composable layers and
emits one contract JSON (docs/crowding/data/latest.json) plus a compact HTML
dashboard block injected into docs/crowding/index.html between the
CROWDING_AUTO_DASH_START / _END markers.

Layers
------
  COT     : CFTC Commitments of Traders speculative positioning across 15
            cross-asset futures markets.  Maintains a compact derived weekly
            series cache (data/cot_history.json); does NOT store CFTC zips.
  Theme   : 5-dimension crowding engine over the site's own Industry-DD
            themes (docs/id/ID_*.html id-meta) using weekly close cache,
            dd-screener EPS revisions/verdicts and the official picks list.
  Volume  : gap-fill layer (dim D + ETF volume_z) from a dedicated weekly
            volume cache (data/crowding_volume.json), yfinance -> stooq
            fallback, incremental, zero-churn.
  ETF     : 15 cross-asset ETF momentum / deviation percentiles.

CLI
---
  python scripts/build_crowding.py            full weekly refresh (default)
  python scripts/build_crowding.py --skip-fetch   offline: recompute from
                                                    existing caches only

Design contracts
----------------
  * Zero churn: every cache / output is compared to its current on-disk value
    and only written when the content actually changes.  JSON is emitted with
    sorted keys and fixed decimals so a no-op week produces an empty diff.
  * data/weekly_cache is read-only (multi-consumer, zero-churn protocol).
  * Fault tolerance: every layer is warn-and-continue.  The process exits
    non-zero only if BOTH the COT and Theme layers fail entirely.
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import statistics
import sys
import zipfile
from datetime import datetime, timezone
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
DATA = os.path.join(ROOT, "data")
WEEKLY_CACHE = os.path.join(DATA, "weekly_cache")
COT_HISTORY = os.path.join(DATA, "cot_history.json")
VOLUME_CACHE = os.path.join(DATA, "crowding_volume.json")
OUT_DIR = os.path.join(ROOT, "docs", "crowding")
OUT_JSON = os.path.join(OUT_DIR, "data", "latest.json")
INDEX_HTML = os.path.join(OUT_DIR, "index.html")
DASH_START = "<!-- CROWDING_AUTO_DASH_START -->"
DASH_END = "<!-- CROWDING_AUTO_DASH_END -->"

sys.path.insert(0, SCRIPTS)


def warn(msg: str) -> None:
    print(f"[crowding][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[crowding] {msg}")


# ───────────────────────────────────────────────────────────────────────────
# Small numeric helpers
# ───────────────────────────────────────────────────────────────────────────

def pctile_incl(values, x):
    """Inclusive percentile rank (fraction of values <= x), 0..100."""
    v = [z for z in values if z is not None]
    n = len(v)
    if n == 0 or x is None:
        return None
    return round(100.0 * sum(1 for z in v if z <= x) / n, 1)


def pctile_frac(values, x):
    """Inclusive percentile rank as a 0..1 fraction (theme dev-percentile)."""
    v = [z for z in values if z is not None]
    n = len(v)
    if n == 0 or x is None:
        return None
    return sum(1 for z in v if z <= x) / n


def mean_avail(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 1) if xs else None


def rnd(v, d):
    if v is None:
        return None
    try:
        return round(float(v), d)
    except (TypeError, ValueError):
        return None


def mean_pairwise_corr(series_list):
    cs = []
    for a, b in combinations(range(len(series_list)), 2):
        x, y = series_list[a], series_list[b]
        n = min(len(x), len(y))
        if n < 3:
            continue
        try:
            cs.append(statistics.correlation(x[-n:], y[-n:]))
        except statistics.StatisticsError:
            continue
    return statistics.mean(cs) if cs else None


def weekly_returns(closes):
    return [closes[i] / closes[i - 1] - 1 for i in range(1, len(closes)) if closes[i - 1]]


def vol_zscore(vols, recent=4, base=52):
    """z-score of mean(last `recent` weekly vols) vs trailing `base` window."""
    v = [x for x in vols if x is not None]
    if len(v) < base or len(v) < recent + 1:
        return None
    window = v[-base:]
    mu = statistics.mean(window)
    sd = statistics.pstdev(window)
    if sd == 0:
        return None
    return (statistics.mean(v[-recent:]) - mu) / sd


# ───────────────────────────────────────────────────────────────────────────
# Zero-churn IO
# ───────────────────────────────────────────────────────────────────────────

def _serialize(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _strip_volatile(obj, keys):
    """Deep copy with volatile (timestamp) keys removed, so a no-op week whose
    only difference is the run timestamp compares equal."""
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def write_json_if_changed(path, obj, volatile=("generated_at", "built_at")) -> bool:
    """Write JSON only when the *substantive* content differs.  Timestamp
    fields listed in `volatile` are ignored for the comparison so an
    unchanged week produces an empty diff.  Returns wrote?"""
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_serialize(obj))
    return True


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        warn(f"could not read {os.path.basename(path)}: {e}")
        return default


# ───────────────────────────────────────────────────────────────────────────
# Network helpers (lazy imports; tolerant)
# ───────────────────────────────────────────────────────────────────────────

def _http_get(url, timeout=60):
    try:
        import requests
        r = requests.get(url, timeout=timeout,
                         headers={"User-Agent": "Mozilla/5.0 crowding-monitor"})
        r.raise_for_status()
        return r.content
    except Exception:
        # stdlib fallback
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 crowding-monitor"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


# ═══════════════════════════════════════════════════════════════════════════
# LAYER 1 — COT
# ═══════════════════════════════════════════════════════════════════════════

# CFTC contract-market code -> display label.  Matched by CODE (stable across
# report-name changes); see build_cot pilot / cot_notes.md.
COT_MARKETS = [
    ("13874A", "S&P 500 E-mini"),
    ("209742", "Nasdaq-100 E-mini"),
    ("239742", "Russell 2000 E-mini"),
    ("1170E1", "VIX futures"),
    ("042601", "US Treasury 2Y"),
    ("044601", "US Treasury 5Y"),
    ("043602", "US Treasury 10Y"),
    ("020601", "US Treasury Bonds (30Y)"),
    ("098662", "US Dollar Index (DX)"),
    ("099741", "EUR (Euro FX)"),
    ("097741", "JPY (Japanese Yen)"),
    ("088691", "Gold"),
    ("084691", "Silver"),
    ("085692", "Copper"),
    ("067651", "WTI Crude"),
]
# Legacy futures-only column indices.
C_DATE_YMD, C_CODE, C_OI, C_NC_LONG, C_NC_SHORT = 2, 3, 7, 8, 9
CFTC_ANNUAL_URL = "https://www.cftc.gov/files/dea/history/deacot{year}.zip"
COT_BOOTSTRAP_START = 2021


def _cot_scratch_dir():
    """Best-effort locate the pilot cot_raw/ for offline bootstrap."""
    import glob as _g
    hits = _g.glob("/private/tmp/claude-*/**/scratchpad/cot_raw", recursive=True)
    for h in hits:
        if os.path.isdir(h):
            return h
    return None


def _parse_annual_text(text, series):
    """Accumulate net_pct_oi observations from one legacy annual.txt body."""
    import csv
    reader = csv.reader(io.StringIO(text))
    next(reader, None)
    wanted = {c for c, _ in COT_MARKETS}
    for row in reader:
        if len(row) <= C_NC_SHORT:
            continue
        code = row[C_CODE]
        if code not in wanted:
            continue
        try:
            d = datetime.strptime(row[C_DATE_YMD], "%Y-%m-%d").date().isoformat()
            oi = int(row[C_OI]); ncl = int(row[C_NC_LONG]); ncs = int(row[C_NC_SHORT])
        except (ValueError, IndexError):
            continue
        if not oi:
            continue
        series.setdefault(code, {})[d] = round(100.0 * (ncl - ncs) / oi, 2)


def _zip_annual_text(raw_bytes):
    with zipfile.ZipFile(io.BytesIO(raw_bytes)) as zf:
        name = next((n for n in zf.namelist() if n.lower().endswith(".txt")), None)
        if not name:
            return None
        return zf.read(name).decode("latin-1")


def cot_bootstrap(skip_fetch):
    """Build the full 2021->current derived series into cot_history.json."""
    series: dict[str, dict[str, float]] = {}
    scratch = _cot_scratch_dir()
    if scratch:
        info(f"COT bootstrap from local pilot archives: {scratch}")
        for path in sorted(glob.glob(os.path.join(scratch, "d20*/annual.txt"))):
            with open(path, encoding="latin-1") as f:
                _parse_annual_text(f.read(), series)
    elif not skip_fetch:
        cur = datetime.now(timezone.utc).year
        info(f"COT bootstrap by downloading CFTC annual {COT_BOOTSTRAP_START}..{cur}")
        for yr in range(COT_BOOTSTRAP_START, cur + 1):
            try:
                txt = _zip_annual_text(_http_get(CFTC_ANNUAL_URL.format(year=yr)))
                if txt:
                    _parse_annual_text(txt, series)
            except Exception as e:
                warn(f"COT annual {yr} download failed: {e}")
    else:
        warn("COT bootstrap skipped (--skip-fetch and no cache/pilot archive)")
        return None
    if not series:
        return None
    return _series_to_history(series)


def _series_to_history(series):
    markets = {}
    label = {c: l for c, l in COT_MARKETS}
    for code, by_date in series.items():
        pts = sorted(by_date.items())
        markets[code] = {"label": label.get(code, code),
                         "series": [[d, v] for d, v in pts]}
    return {
        "meta": {
            "source": "CFTC Commitments of Traders — legacy futures-only (deacot annual archives)",
            "methodology": "net_pct_oi = (noncomm long - noncomm short) / total OI * 100; "
                           "markets matched by stable CFTC contract code.",
            "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "markets": markets,
    }


def cot_append_current(history, skip_fetch):
    """Download only the current-year annual and append any newer weeks."""
    if skip_fetch:
        return history
    cur = datetime.now(timezone.utc).year
    try:
        txt = _zip_annual_text(_http_get(CFTC_ANNUAL_URL.format(year=cur)))
    except Exception as e:
        warn(f"COT current-year ({cur}) download failed, using cache: {e}")
        return history
    if not txt:
        warn("COT current-year zip had no txt member; using cache")
        return history
    series: dict[str, dict[str, float]] = {}
    _parse_annual_text(txt, series)
    label = {c: l for c, l in COT_MARKETS}
    added = 0
    for code, by_date in series.items():
        m = history["markets"].setdefault(code, {"label": label.get(code, code), "series": []})
        have = {d for d, _ in m["series"]}
        for d, v in sorted(by_date.items()):
            if d not in have:
                m["series"].append([d, v])
                added += 1
        m["series"].sort()
    if added:
        info(f"COT appended {added} new market-week observations")
    return history


def cot_compute(history):
    """Derive the current positioning table from the cached series."""
    rows = []
    gaps = []
    latest = None
    for code, label in COT_MARKETS:
        m = history["markets"].get(code)
        if not m or not m["series"]:
            gaps.append(f"COT {label} ({code}): 無資料")
            continue
        s = sorted(m["series"])
        vals = [v for _, v in s]
        cur_date, cur_val = s[-1]
        if latest is None or cur_date > latest:
            latest = cur_date
        win5, win3 = vals[-260:], vals[-156:]
        p5 = pctile_incl(win5, cur_val)
        p3 = pctile_incl(win3, cur_val)

        def ago(k):
            i = len(vals) - 1 - k
            return vals[i] if i >= 0 else None

        v4, v13 = ago(4), ago(13)
        d4 = rnd(cur_val - v4, 2) if v4 is not None else None
        d13 = rnd(cur_val - v13, 2) if v13 is not None else None
        direction = "net long" if cur_val > 0 else ("net short" if cur_val < 0 else "flat")
        extreme = None
        if p5 is not None:
            if p5 >= 90:
                extreme = "stretched_long"
            elif p5 <= 10:
                extreme = "stretched_short"
        if len(win5) < 150:
            gaps.append(f"COT {label}: 5y 樣本僅 {len(win5)} 週 (<150)，百分位可信度打折")
        rows.append({
            "market": label,
            "net_pct_oi": rnd(cur_val, 2),
            "pctile_3y": p3,
            "pctile_5y": p5,
            "delta_4w": d4,
            "delta_13w": d13,
            "extreme": extreme,
            "direction": direction,
        })
    return rows, latest, gaps


# ═══════════════════════════════════════════════════════════════════════════
# LAYER 2 — THEME engine  (+ dim D from volume layer)
# ═══════════════════════════════════════════════════════════════════════════

ETF_UNIVERSE = [
    ("UUP", "US Dollar"), ("QQQ", "Nasdaq 100"), ("IWM", "US Small Cap"),
    ("SPY", "S&P 500"), ("USO", "Crude Oil"), ("EEM", "EM Equities"),
    ("EFA", "Developed ex-US"), ("TLT", "20Y+ Treasuries"), ("IEF", "7-10Y Treasuries"),
    ("LQD", "IG Credit"), ("SLV", "Silver"), ("GLD", "Gold"),
    ("FXY", "Japanese Yen"), ("HYG", "High Yield"), ("IBIT", "Bitcoin (spot ETF)"),
]
ETF_TICKERS = [t for t, _ in ETF_UNIVERSE]


def load_weekly_closes():
    closes = {}
    for f in glob.glob(os.path.join(WEEKLY_CACHE, "*.json")):
        d = load_json(f)
        if not d:
            continue
        tk = d.get("ticker")
        bars = d.get("weekly_bars") or []
        closes[tk] = [(b["week_end"], b["close"]) for b in bars if b.get("close") is not None]
    return closes


def load_themes():
    """Dedup id-meta themes: keep the variant with most related_tickers, then
    latest publish_date."""
    from dd_meta_reader import iter_id_metas
    by_theme = {}
    for p, m in iter_id_metas(os.path.join(ROOT, "docs", "id")):
        th = m.get("theme")
        if not th:
            continue
        rts = m.get("related_tickers") or []
        key = (len(rts), m.get("publish_date", ""))
        if th not in by_theme or key > by_theme[th][0]:
            by_theme[th] = (key, m, p.name)
    return by_theme


def load_screener():
    scr = load_json(os.path.join(ROOT, "docs", "dd-screener", "latest.json"), {})
    rev, verd = {}, {}
    for s in scr.get("stocks", []):
        rev[s["ticker"]] = s.get("eps_fy_curr_revision_pct")
        verd[s["ticker"]] = s.get("dca_verdict")
    return rev, verd


def load_picks():
    pk = load_json(os.path.join(ROOT, "docs", "picks", "candidates.json"), {})
    official, cand = set(), set()
    for k in ("official_changhao", "official_baofa"):
        official |= {x["ticker"] for x in pk.get(k, [])}
    for k in ("changhao", "baofa"):
        cand |= {x["ticker"] for x in pk.get(k, [])}
    return official, cand


def theme_raws(closes, rev, verd, official, cand, vol_series):
    """Compute per-theme raw metrics (A/B/C/D/E inputs)."""
    themes = load_themes()
    out = []
    for th, (_key, m, fname) in themes.items():
        members = list(dict.fromkeys(
            r["ticker"] for r in (m.get("related_tickers") or []) if r.get("ticker")))
        cov = [t for t in members if t in closes and len(closes[t]) >= 53]
        rec = {
            "theme": th, "file": fname,
            "n_members": len(members), "n_cache_cov": len(cov),
            "cache_cov_ratio": round(len(cov) / len(members), 3) if members else 0.0,
            "conviction": m.get("conviction"),
        }
        if len(members) < 4 or len(cov) < 3:
            rec["status"] = "insufficient_coverage"
            out.append(rec)
            continue
        rec["status"] = "ok"

        # A — momentum extension
        ret12, devp = [], []
        for t in cov:
            cl = [c for _, c in closes[t]]
            if len(cl) >= 53 and cl[-53]:
                ret12.append(cl[-1] / cl[-53] - 1)
            if len(cl) >= 52:
                gaps = []
                for i in range(51, len(cl)):
                    ma = sum(cl[i - 51:i + 1]) / 52
                    gaps.append(cl[i] / ma - 1 if ma else None)
                gaps = [g for g in gaps if g is not None]
                if gaps:
                    devp.append(pctile_frac(gaps[-130:], gaps[-1]))
        rec["mom_ret_12m"] = rnd(statistics.mean(ret12), 4) if ret12 else None
        devp = [d for d in devp if d is not None]
        rec["mom_dev_pctile_med"] = rnd(statistics.median(devp), 4) if devp else None

        # B — correlation tightness
        rl = {t: weekly_returns([c for _, c in closes[t]]) for t in cov}
        rec13 = [rl[t][-13:] for t in cov if len(rl[t]) >= 13]
        recb = [rl[t][-104:] for t in cov if len(rl[t]) >= 13]
        cr = mean_pairwise_corr(rec13) if len(rec13) >= 2 else None
        cb = mean_pairwise_corr(recb) if len(recb) >= 2 else None
        rec["corr_recent_13w"] = rnd(cr, 4)
        rec["corr_base_2y"] = rnd(cb, 4)
        rec["corr_delta"] = rnd(cr - cb, 4) if (cr is not None and cb is not None) else None

        # C — revision chasing
        rvals = [rev[t] for t in members if rev.get(t) is not None]
        rec["n_rev_cov"] = len(rvals)
        rec["rev_fy1_median"] = rnd(statistics.median(rvals), 4) if rvals else None
        rec["rev_up_frac"] = rnd(sum(1 for v in rvals if v > 0) / len(rvals), 4) if rvals else None

        # D — volume (gap-fill layer)
        mzs = []
        for t in cov:
            vs = vol_series.get(t)
            if vs:
                z = vol_zscore([v for _, v in vs])
                if z is not None:
                    mzs.append(z)
        rec["n_vol_cov"] = len(mzs)
        rec["vol_z_med"] = rnd(statistics.median(mzs), 4) if mzs else None

        # E — self-consensus
        vv = [verd[t] for t in members if verd.get(t)]
        rec["n_dd_verdict"] = len(vv)
        rec["entry_frac"] = rnd(sum(1 for v in vv if v == "進場") / len(vv), 4) if vv else None
        rec["picks_official"] = sum(1 for t in members if t in official)
        rec["picks_cand"] = sum(1 for t in members if t in cand)
        out.append(rec)
    return out


def theme_score(raws):
    """Cross-theme percentile transform -> dims -> composite -> rank."""
    scor = [r for r in raws if r["status"] == "ok"]
    if not scor:
        return [], []
    A_ret = [r["mom_ret_12m"] for r in scor]
    A_dev = [r["mom_dev_pctile_med"] for r in scor]
    B_d = [r["corr_delta"] for r in scor]
    C_m = [r["rev_fy1_median"] for r in scor]
    C_u = [r["rev_up_frac"] for r in scor]
    D_v = [r["vol_z_med"] for r in scor]
    E_e = [r["entry_frac"] for r in scor]
    E_p = [r["picks_official"] for r in scor]

    scored = []
    for r in scor:
        A = mean_avail([pctile_incl(A_ret, r["mom_ret_12m"]),
                        pctile_incl(A_dev, r["mom_dev_pctile_med"])])
        B = pctile_incl(B_d, r["corr_delta"])
        C = mean_avail([pctile_incl(C_m, r["rev_fy1_median"]),
                        pctile_incl(C_u, r["rev_up_frac"])])
        D = pctile_incl(D_v, r["vol_z_med"])
        E = mean_avail([pctile_incl(E_e, r["entry_frac"]),
                        pctile_incl(E_p, r["picks_official"])])
        comp5 = mean_avail([A, B, C, D, E])
        comp4 = mean_avail([A, B, C, E])  # legacy four-dim (for diagnostics)
        low = (r["n_cache_cov"] <= 5 or r["cache_cov_ratio"] < 0.4)
        scored.append({
            "name": r["theme"],
            "score": comp5,
            "score_4dim": comp4,
            "dims": {"momentum": A, "correlation": B, "revision": C,
                     "volume": D, "consensus": E},
            "members_covered": r["n_cache_cov"],
            "members_total": r["n_members"],
            "low_coverage": low,
        })
    scored.sort(key=lambda x: (x["score"] is not None, x["score"]), reverse=True)
    for i, s in enumerate(scored, 1):
        s["rank"] = i
    insufficient = [r["theme"] for r in raws if r["status"] != "ok"]
    return scored, insufficient


# ═══════════════════════════════════════════════════════════════════════════
# LAYER 3 — VOLUME cache  (yfinance -> stooq fallback, incremental, zero-churn)
# ═══════════════════════════════════════════════════════════════════════════

def _yf_weekly(tickers, period="2y"):
    """Batch weekly download -> {ticker: [(week_end, close, volume), ...]}."""
    import yfinance as yf
    import pandas as pd  # noqa: F401
    out = {}
    if not tickers:
        return out
    df = yf.download(tickers, period=period, interval="1wk", auto_adjust=True,
                     group_by="ticker", threads=True, progress=False)
    single = len(tickers) == 1
    for tk in tickers:
        try:
            sub = df if single else df[tk]
            rows = []
            for idx, row in sub.iterrows():
                c = row.get("Close")
                v = row.get("Volume")
                if c is None or (isinstance(c, float) and c != c):
                    continue
                rows.append((idx.date().isoformat(), float(c),
                             None if (v is None or v != v) else int(v)))
            if rows:
                out[tk] = rows
        except (KeyError, AttributeError, ValueError):
            continue
    return out


def _stooq_weekly(ticker):
    """Fallback single-ticker weekly series from stooq CSV."""
    sym = ticker.lower()
    if "." not in sym:
        sym = sym + ".us"
    else:  # e.g. 2330.tw -> 2330.tw already stooq-shaped for many TW names
        sym = sym
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
        if len(parts) < 6:
            continue
        try:
            rows.append((parts[0], float(parts[4]),
                         int(float(parts[5])) if parts[5] not in ("", "N/D") else None))
        except ValueError:
            continue
    return rows or None


def build_volume_cache(member_universe, skip_fetch):
    """Incrementally refresh data/crowding_volume.json.  Returns
    {ticker: [(date, volume)]} plus {ticker: [(date, close)]} for ETFs."""
    cache = load_json(VOLUME_CACHE, {"meta": {}, "tickers": {}})
    tickers = cache.setdefault("tickers", {})
    targets = sorted(set(member_universe) | set(ETF_TICKERS))

    fetched = {}
    if not skip_fetch:
        try:
            import yfinance  # noqa: F401
        except ImportError:
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", "-q",
                             "yfinance>=0.2.40", "pandas"])
        # incremental: bootstrap missing = 2y, existing = 3mo top-up
        missing = [t for t in targets if t not in tickers or not tickers[t].get("volume")]
        existing = [t for t in targets if t not in missing]
        for label, batch, period in (("bootstrap", missing, "2y"),
                                     ("topup", existing, "3mo")):
            for i in range(0, len(batch), 40):
                chunk = batch[i:i + 40]
                got = None
                for attempt in range(3):
                    try:
                        got = _yf_weekly(chunk, period=period)
                        break
                    except Exception as e:
                        warn(f"yfinance {label} chunk {i//40} attempt {attempt+1} failed: {e}")
                if got:
                    fetched.update(got)
            info(f"volume {label}: requested {len(batch)}, got {sum(1 for t in batch if t in fetched)}")
        # stooq fallback for names yfinance missed entirely
        for t in targets:
            if t in fetched or (t in tickers and tickers[t].get("volume")):
                continue
            s = _stooq_weekly(t)
            if s:
                fetched[t] = s
                info(f"volume stooq fallback: {t} ({len(s)} wks)")

    # merge fetched into cache (append new weeks only)
    for t, rows in fetched.items():
        is_etf = t in ETF_TICKERS
        ent = tickers.setdefault(t, {"source": None, "volume": [], "close": [] if is_etf else None})
        ent["source"] = "yfinance"  # stooq-origin rows are shaped identically
        have_v = {d for d, _ in ent.get("volume", [])}
        for d, c, v in rows:
            if v is not None and d not in have_v:
                ent["volume"].append([d, v])
        ent["volume"].sort()
        if is_etf:
            have_c = {d for d, _ in ent.get("close") or []}
            ent["close"] = ent.get("close") or []
            for d, c, v in rows:
                if c is not None and d not in have_c:
                    ent["close"].append([d, rnd(c, 4)])
            ent["close"].sort()

    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_tickers": len(tickers),
        "note": "weekly volume (all) + close (ETFs) cache; yfinance->stooq; incremental.",
    }
    wrote = write_json_if_changed(VOLUME_CACHE, cache)
    info(f"volume cache: {len(tickers)} tickers, {'written' if wrote else 'no change'}")

    vol_series = {t: [(d, v) for d, v in e.get("volume", [])] for t, e in tickers.items()}
    etf_close = {t: [(d, c) for d, c in (tickers.get(t, {}).get("close") or [])]
                 for t in ETF_TICKERS}
    return vol_series, etf_close


# ═══════════════════════════════════════════════════════════════════════════
# LAYER 4 — ETF cross-asset
# ═══════════════════════════════════════════════════════════════════════════

def etf_compute(etf_close, vol_series):
    rows = []
    gaps = []
    for tk, label in ETF_UNIVERSE:
        cl = [c for _, c in etf_close.get(tk, [])]
        if len(cl) < 53:
            gaps.append(f"ETF {tk}: 收盤資料不足（{len(cl)} 週）")
            rows.append({"ticker": tk, "label": label, "momentum_pctile": None,
                         "deviation_pctile": None, "volume_z": None, "ret_12m": None})
            continue
        ret12 = cl[-1] / cl[-53] - 1 if cl[-53] else None
        # 52wk rolling-return self-percentile
        r52 = [cl[i] / cl[i - 52] - 1 for i in range(52, len(cl)) if cl[i - 52]]
        mom_p = pctile_incl(r52, r52[-1]) if r52 else None
        # 52wMA deviation self-percentile
        gaps_s = []
        for i in range(51, len(cl)):
            ma = sum(cl[i - 51:i + 1]) / 52
            gaps_s.append(cl[i] / ma - 1 if ma else None)
        gaps_s = [g for g in gaps_s if g is not None]
        dev_p = pctile_incl(gaps_s, gaps_s[-1]) if gaps_s else None
        vz = vol_zscore([v for _, v in vol_series.get(tk, [])])
        rows.append({
            "ticker": tk, "label": label,
            "momentum_pctile": mom_p, "deviation_pctile": dev_p,
            "volume_z": rnd(vz, 2), "ret_12m": rnd(ret12, 4),
        })
    return rows, gaps


# ═══════════════════════════════════════════════════════════════════════════
# HTML dashboard injection
# ═══════════════════════════════════════════════════════════════════════════

def render_dashboard(payload):
    cot = payload["cot"]
    themes = payload["themes"]
    etf = payload["etf"]
    hot = [c for c in cot if c["extreme"] == "stretched_long"]
    cold = [c for c in cot if c["extreme"] == "stretched_short"]
    top = themes[:5]
    etf_hot = sorted([e for e in etf if e.get("momentum_pctile") is not None],
                     key=lambda e: e["momentum_pctile"], reverse=True)[:3]

    st = ("font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
          "background:#12161f;border:1px solid #2a3242;border-radius:12px;"
          "padding:18px 20px;color:#e6e9ef;line-height:1.6;font-size:14px")
    pill = ("display:inline-block;font-family:ui-monospace,monospace;font-size:11px;"
            "padding:2px 8px;border-radius:5px;margin:2px 3px 2px 0")

    def chips(items, bg, fg):
        return "".join(
            f'<span style="{pill};background:{bg};color:{fg}">{i}</span>' for i in items) or \
            '<span style="color:#6b7484">—</span>'

    cot_hot = chips([f'{c["market"]} {c["pctile_5y"]:.0f}' for c in hot], "#7f1d1d", "#fecaca")
    cot_cold = chips([f'{c["market"]} {c["pctile_5y"]:.0f}' for c in cold], "#0c4a6e", "#bae6fd")
    theme_rows = "".join(
        f'<tr><td style="padding:3px 8px;color:#9aa4b5;font-family:ui-monospace,monospace">'
        f'{t["rank"]}</td><td style="padding:3px 8px">{t["name"]}'
        f'{" ⚠" if t["low_coverage"] else ""}</td>'
        f'<td style="padding:3px 8px;text-align:right;font-family:ui-monospace,monospace;'
        f'font-weight:700;color:{"#f87171" if (t["score"] or 0)>=65 else "#fbbf24"}">'
        f'{t["score"]:.1f}</td></tr>' for t in top)
    etf_chips = chips(
        [f'{e["ticker"]} {e["momentum_pctile"]:.0f}' for e in etf_hot], "#7c2d12", "#fed7aa")

    return (
        f'{DASH_START}\n'
        f'<div style="{st}">'
        f'<div style="font-family:ui-monospace,monospace;font-size:11px;letter-spacing:.14em;'
        f'text-transform:uppercase;color:#5b9bff;margin-bottom:10px">跨資產擁擠交易 · 自動儀表</div>'
        f'<div style="margin-bottom:8px"><b>COT 極端偏多（5y ≥ 90）：</b><br>{cot_hot}</div>'
        f'<div style="margin-bottom:8px"><b>COT 極端偏空（5y ≤ 10）：</b><br>{cot_cold}</div>'
        f'<div style="margin:10px 0 6px"><b>自家主題擁擠 Top 5</b>（五維綜合分）</div>'
        f'<table style="border-collapse:collapse;width:100%;font-size:13px">{theme_rows}</table>'
        f'<div style="margin:10px 0 6px"><b>跨資產 ETF 動能極端 Top 3</b></div>{etf_chips}'
        f'<div style="margin-top:12px;font-family:ui-monospace,monospace;font-size:11px;'
        f'color:#6b7484">COT as-of {payload["cot_as_of"] or "—"} · '
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
    block = render_dashboard(payload)
    new = pre + block + post
    if new == html:
        info("dashboard: no change")
        return
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(new)
    info("dashboard: injected into index.html")


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Cross-asset crowding weekly builder")
    ap.add_argument("--skip-fetch", action="store_true",
                    help="offline: skip all network fetches, recompute from caches")
    args = ap.parse_args()

    gaps = []
    cot_ok = theme_ok = False

    # ── COT layer ──────────────────────────────────────────────────────────
    cot_rows, cot_as_of = [], None
    history = load_json(COT_HISTORY)
    try:
        if history is None:
            history = cot_bootstrap(args.skip_fetch)
        else:
            history = cot_append_current(history, args.skip_fetch)
        if history:
            write_json_if_changed(COT_HISTORY, history)
            cot_rows, cot_as_of, cg = cot_compute(history)
            gaps += cg
            cot_ok = bool(cot_rows)
    except Exception as e:
        warn(f"COT layer failed: {e}")

    # ── Theme member universe (drives volume fetch) ─────────────────────────
    closes = load_weekly_closes()
    rev, verd = load_screener()
    official, cand = load_picks()
    themes_meta = load_themes()
    member_universe = set()
    for _th, (_k, m, _f) in themes_meta.items():
        for r in (m.get("related_tickers") or []):
            t = r.get("ticker")
            if t and t in closes:
                member_universe.add(t)

    # ── Volume layer ────────────────────────────────────────────────────────
    try:
        vol_series, etf_close = build_volume_cache(member_universe, args.skip_fetch)
    except Exception as e:
        warn(f"volume layer failed: {e}")
        vol_series, etf_close = {}, {}

    # ── Theme layer ──────────────────────────────────────────────────────────
    themes_out, insufficient = [], []
    try:
        raws = theme_raws(closes, rev, verd, official, cand, vol_series)
        themes_out, insufficient = theme_score(raws)
        theme_ok = bool(themes_out)
        n_novol = sum(1 for t in themes_out if t["dims"]["volume"] is None)
        if n_novol:
            gaps.append(f"主題引擎：{n_novol} 個主題缺量能維度（成員無 volume 快取）")
        if insufficient:
            gaps.append(f"主題引擎：{len(insufficient)} 個主題覆蓋不足未評分")
    except Exception as e:
        warn(f"Theme layer failed: {e}")

    # ── ETF layer ────────────────────────────────────────────────────────────
    etf_out = []
    try:
        etf_out, eg = etf_compute(etf_close, vol_series)
        gaps += eg
    except Exception as e:
        warn(f"ETF layer failed: {e}")

    # ── Assemble contract ────────────────────────────────────────────────────
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cot_as_of": cot_as_of,
        "cot": cot_rows,
        "themes": themes_out,
        "etf": etf_out,
        "gaps": gaps,
        "meta": {
            "n_themes_ranked": len(themes_out),
            "n_themes_insufficient": len(insufficient),
            "n_cot_markets": len(cot_rows),
            "n_etf": len(etf_out),
            "methodology": (
                "COT: noncomm net / OI, 3y/5y inclusive percentile. "
                "Themes: 5-dim (momentum/correlation/revision/volume/consensus) "
                "cross-theme percentile, composite = mean of available dims. "
                "ETF: 2y self-percentile momentum/deviation + 4w-vs-52w volume z. "
                "Descriptor, not a timing signal."
            ),
            "disclaimer": "描述器非擇時。相對排名於本主題集內，非市場絕對擁擠度。",
        },
    }
    wrote = write_json_if_changed(OUT_JSON, payload)
    info(f"latest.json: {'written' if wrote else 'no change'}")

    inject_dashboard(payload)

    if not cot_ok and not theme_ok:
        warn("both COT and Theme layers failed — exiting non-zero")
        sys.exit(1)
    info("done.")


if __name__ == "__main__":
    main()
