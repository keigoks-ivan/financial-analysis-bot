#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asset Rotation Radar — daily RRG data pipeline.

Sibling of build_rotation.py.  Where build_rotation.py runs weekly over the
site's own Industry-DD themes vs SPY, this builder runs DAILY over three fixed
ETF universes (cross-asset / US sectors / global markets), each against its own
benchmark, and emits one contract JSON (docs/rotation/data/radar.json) consumed
by a separate frontend page.

Compute (JdK-style RRG, same normalization as build_rotation.py but daily)
-------------------------------------------------------------------------
  * RS       = 100 * price / benchmark_price  (aligned on the benchmark's
               trading-day grid, forward-filled).
  * rs_ratio = 100 + (RS - SMA(RS, W)) / STD(RS, max(W, 60)).
  * rs_mom   = 100 + (rs_ratio - SMA(rs_ratio, Wm)) / STD(rs_ratio, max(Wm, 24)).
    The mean window stays at W / Wm, but the STD (denominator) uses a floored
    window so the short frame's dispersion estimate is not whipped by too few
    samples (a W=20 rolling std has only ~20 points — too noisy).
  * Three frames (all daily trail points, oldest -> newest, last = current):
        "120" -> W=120, Wm=30, trail=30
        "60"  -> W=60,  Wm=15, trail=20
        "20"  -> W=20,  Wm=8,  trail=10

Data
----
  Daily adjusted closes, fetch period 3y (need 120d SMA + std + trail headroom).
  yfinance batch (auto_adjust=True) first, stooq per-ticker fallback (symbol.us).
  Each unique ticker fetched once (SPY appears in multiple universes).  Warn and
  continue per ticker; a member with no data becomes status "insufficient".
  Incremental per-ticker cache at data/rotation_radar_daily.json (merge by date,
  sorted, zero-churn write; incremental refresh fetches only ~3mo).

CLI
---
  python scripts/build_rotation_radar.py            full daily refresh (default)
  python scripts/build_rotation_radar.py --skip-fetch   recompute from cache only

Design contracts (identical to build_rotation.py)
-------------------------------------------------
  * Zero churn: JSON emitted with sorted keys + fixed decimals; volatile
    timestamp fields stripped before the on-disk comparison, so a no-op day
    (e.g. a weekend run) produces an empty diff / no write.
  * Fault tolerance: per-ticker fetch is warn-and-continue with cache fallback;
    the process exits non-zero only if a whole universe has zero ok members.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(DATA, "rotation_radar_daily.json")
OUT_JSON = os.path.join(ROOT, "docs", "rotation", "data", "radar.json")
# 每日快照：累積歷史供未來長程輪動回放與復盤驗證（零 churn，週末 as_of 不變即 no-op）
SNAP_DIR = os.path.join(ROOT, "docs", "rotation", "data", "snapshots")

# ── Universe config (order preserved end-to-end; frontend keys color by it) ──
UNIVERSES = [
    {
        "key": "cross_asset",
        "label": "全球資產輪動",
        "benchmark": {"ticker": "AOR", "label": "全球 60/40"},
        "members": [
            ("VNQ", "房地產REIT"), ("SPY", "美股"), ("EFA", "成熟市場股"),
            ("EEM", "新興市場股"), ("DBC", "大宗商品"), ("GLD", "黃金"),
            ("TLT", "美長天期公債"), ("LQD", "投資級公司債"), ("HYG", "高收益債"),
            ("UUP", "美元"), ("IBIT", "比特幣"),
        ],
    },
    {
        "key": "us_sectors",
        "label": "美股板塊輪動",
        "benchmark": {"ticker": "SPY", "label": "標普500"},
        "members": [
            ("XLK", "科技"), ("XLC", "通訊服務"), ("XLY", "非必需消費"),
            ("XLP", "必需消費"), ("XLV", "醫療保健"), ("XLF", "金融"),
            ("XLI", "工業"), ("XLE", "能源"), ("XLB", "原物料"),
            ("XLRE", "房地產"), ("XLU", "公用事業"),
        ],
    },
    {
        "key": "global_markets",
        "label": "全球市場輪動",
        "benchmark": {"ticker": "ACWI", "label": "全球股票"},
        "members": [
            ("SPY", "美股"), ("VGK", "歐股"), ("EWJ", "日股"),
            ("EWT", "台股"), ("EWY", "韓股"), ("INDA", "印度"),
            ("EWA", "澳洲"),
        ],
    },
]

# Frame -> (W ratio window, Wm momentum window, trail length in trading days)
FRAMES = {
    "120": (120, 30, 30),
    "60": (60, 15, 20),
    "20": (20, 8, 10),
}
FRAME_ORDER = ["120", "60", "20"]
TRAIL_SMOOTH = 3   # 3 日 SMA 平滑 rs_ratio / rs_mom，彗尾才不會鋸齒
STD_FLOOR = 60     # rs_ratio std 窗下限（樣本太少 std 抖）
MOM_STD_FLOOR = 24  # rs_mom std 窗下限


def warn(msg: str) -> None:
    print(f"[radar][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[radar] {msg}")


# ───────────────────────────────────────────────────────────────────────────
# Zero-churn IO (identical protocol to build_rotation.py)
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
# Network helpers (lazy imports; tolerant) — daily adjusted closes
# ───────────────────────────────────────────────────────────────────────────

def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout,
                         headers={"User-Agent": "Mozilla/5.0 rotation-radar"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 rotation-radar"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


def _clean_close(idx, val):
    try:
        c = float(val)
    except (TypeError, ValueError):
        return None
    if c != c or c <= 0:  # NaN or non-positive
        return None
    return (idx.date().isoformat() if hasattr(idx, "date") else str(idx), round(c, 4))


def _yf_batch_daily(tickers, period):
    """Batch daily adjusted closes via yfinance.
    Returns {ticker: [(date, close), ...]} for tickers that came back non-empty."""
    import yfinance as yf
    import pandas as pd
    if not tickers:
        return {}
    df = yf.download(tickers, period=period, interval="1d", auto_adjust=True,
                     progress=False, threads=True, group_by="column")
    if df is None or len(df) == 0:
        return {}
    out = {}
    # Single ticker -> flat columns; multi -> "Close" is a DataFrame of tickers.
    if isinstance(df.columns, pd.MultiIndex):
        try:
            close = df["Close"]
        except KeyError:
            return {}
        for tk in close.columns:
            pts = []
            for idx, val in close[tk].items():
                cc = _clean_close(idx, val)
                if cc:
                    pts.append(cc)
            if pts:
                out[str(tk)] = pts
    else:
        close = df["Close"]
        pts = []
        for idx, val in close.items():
            cc = _clean_close(idx, val)
            if cc:
                pts.append(cc)
        if pts:
            out[tickers[0]] = pts
    return out


def _stooq_daily(ticker):
    sym = ticker.lower()
    if "." not in sym:
        sym = sym + ".us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
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
            c = float(parts[4])
        except ValueError:
            continue
        if c <= 0:
            continue
        rows.append((parts[0], round(c, 4)))
    return rows or None


def _ratio_splice(cached_pts, new_pts, ticker):
    """Scale new_pts (raw split-adjusted-only stooq closes) so they line up with
    cached_pts (yfinance dividend-adjusted history) on their overlapping dates.

    yfinance auto_adjust=True is dividend-adjusted; _stooq_daily() is not, so for
    high-yield tickers (TLT/LQD/HYG/VNQ) merging the two raw would (a) distort RS
    and (b) leave a seam jump in the trail where the two sources meet.  We take the
    median (cached / stooq) ratio over the last ~10 overlapping dates and rescale
    the whole stooq series by it — a level splice that removes the seam and the
    systematic dividend-adjustment offset.  No overlap -> accept as-is + WARN."""
    import statistics
    cached = {d: c for d, c in cached_pts}
    overlap = [(d, c) for d, c in new_pts if d in cached and c]
    if not overlap:
        warn(f"stooq splice {ticker}: no date overlap with cached yfinance history — "
             f"accepting raw stooq closes as-is (possible dividend-adjustment seam)")
        return new_pts
    overlap.sort()  # new_pts is date-ascending, but be defensive
    ratios = [cached[d] / c for d, c in overlap[-10:]]
    k = statistics.median(ratios)
    if not (k == k) or k <= 0:  # NaN / non-positive guard
        warn(f"stooq splice {ticker}: degenerate ratio {k} — accepting as-is")
        return new_pts
    return [(d, round(c * k, 4)) for d, c in new_pts]


def refresh_cache(tickers, skip_fetch):
    """Incrementally refresh per-ticker daily series cache.  Returns
    ({ticker: [(date, close), ...]}, set_of_stooq_fallback_tickers)."""
    cache = load_json(CACHE, {"meta": {}, "series": {}})
    series = dict(cache.get("series", {}))
    prior_sources = dict((cache.get("meta") or {}).get("sources", {}))
    sources = dict(prior_sources)
    stooq_used = set()

    if not skip_fetch:
        try:
            import yfinance  # noqa: F401
        except ImportError:
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", "-q",
                             "yfinance>=0.2.40", "pandas"])
        # Split: known tickers get a light 3mo top-up, new tickers a full 3y.
        old = [t for t in tickers if series.get(t)]
        new = [t for t in tickers if not series.get(t)]
        fetched = {}
        for group, period in ((new, "3y"), (old, "3mo")):
            if not group:
                continue
            for attempt in range(3):
                try:
                    got = _yf_batch_daily(group, period)
                    if got:
                        fetched.update(got)
                        break
                except Exception as e:
                    warn(f"yfinance batch ({period}) attempt {attempt+1} failed: {e}")
        # stooq per-ticker fallback for anything yfinance did not return.
        for t in tickers:
            if t in fetched:
                continue
            got = _stooq_daily(t)
            if got:
                fetched[t] = got
                stooq_used.add(t)
                info(f"stooq fallback used for {t} ({len(got)} bars)")
        # Merge fetched into cached series (by date, sorted).  Stooq points get
        # ratio-spliced onto any existing yfinance history first, and each
        # ticker's source is recorded so a mixed-source state stays visible.
        for t, pts in fetched.items():
            prior = series.get(t, [])
            if t in stooq_used:
                if prior:
                    pts = _ratio_splice(prior, pts, t)
                    sources[t] = "mixed"  # yfinance history + spliced stooq tail
                else:
                    sources[t] = "stooq"
            else:
                # yfinance path: brand-new ticker is pure yfinance; a top-up over
                # a prior stooq/mixed series stays labelled mixed.
                if prior_sources.get(t) in (None, "yfinance"):
                    sources[t] = "yfinance"
            merged = {d: c for d, c in prior}
            for d, c in pts:
                merged[d] = c
            series[t] = sorted(merged.items())

    # Any ticker in the cache without an explicit label predates source tracking
    # and came from the yfinance batch path — default it so meta is complete.
    for t in series:
        sources.setdefault(t, "yfinance")

    cache["series"] = series
    n_bars = sum(len(v) for v in series.values())
    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_tickers": len(series),
        "n_bars": n_bars,
        "sources": {t: sources[t] for t in sorted(sources) if t in series},
        "note": "daily adjusted closes for rotation radar RRG; yfinance->stooq "
                "(stooq tail ratio-spliced onto yfinance); incremental.",
    }
    wrote = write_json_if_changed(CACHE, cache)
    info(f"daily cache: {len(series)} tickers / {n_bars} bars, "
         f"{'written' if wrote else 'no change'}")
    return series, stooq_used


# ───────────────────────────────────────────────────────────────────────────
# RRG compute
# ───────────────────────────────────────────────────────────────────────────

def quadrant(r, m):
    if r >= 100 and m >= 100:
        return "leading"
    if r >= 100 and m < 100:
        return "weakening"
    if r < 100 and m < 100:
        return "lagging"
    return "improving"


def _compute_frames(rs, pd):
    """Given an RS series (already aligned/ffilled on the bench grid), return
    {frame: [{"d","r","m"}, ...]} for each frame (trail possibly empty)."""
    frames = {}
    for fk in FRAME_ORDER:
        W, Wm, trail_n = FRAMES[fk]
        # Mean windows stay at W / Wm; STD windows are floored (max(W,60) /
        # max(Wm,24)) so a short frame's dispersion isn't estimated from too few
        # samples — that estimation noise is what whipped the short-frame trails.
        Wstd = max(W, STD_FLOOR)
        Wmstd = max(Wm, MOM_STD_FLOOR)
        rmean = rs.rolling(W).mean()
        rstd = rs.rolling(Wstd).std()
        rs_ratio = 100.0 + (rs - rmean) / rstd
        mmean = rs_ratio.rolling(Wm).mean()
        mstd = rs_ratio.rolling(Wmstd).std()
        rs_mom = 100.0 + (rs_ratio - mmean) / mstd
        # 3 日平滑：日線 z-score 逐日抖動大，不平滑畫出來是鋸齒折線
        rs_ratio = rs_ratio.rolling(TRAIL_SMOOTH).mean()
        rs_mom = rs_mom.rolling(TRAIL_SMOOTH).mean()
        valid = pd.concat([rs_ratio, rs_mom], axis=1).dropna()
        tail = valid.iloc[-trail_n:] if len(valid) else valid
        trail = [{"d": d.strftime("%Y-%m-%d"),
                  "r": round(float(r), 3), "m": round(float(m), 3)}
                 for d, (r, m) in zip(tail.index, tail.values)]
        frames[fk] = {"trail": trail}
    return frames


def compute(series):
    import pandas as pd

    def to_series(pts):
        idx = [pd.Timestamp(d) for d, _ in pts]
        return pd.Series([float(c) for _, c in pts], index=idx).sort_index()

    cache_s = {t: to_series(pts) for t, pts in series.items() if pts}

    out_universes = []
    latest_date = None

    for uni in UNIVERSES:
        bench_tk = uni["benchmark"]["ticker"]
        bench = cache_s.get(bench_tk)
        members_out = []
        n_ok = 0

        if bench is None or len(bench) < FRAMES["20"][0] + FRAMES["20"][1] + 1:
            warn(f"universe {uni['key']}: benchmark {bench_tk} unavailable/short")
            for tk, label in uni["members"]:
                members_out.append({"ticker": tk, "label": label, "status": "insufficient"})
            out_universes.append({
                "key": uni["key"], "label": uni["label"],
                "benchmark": uni["benchmark"], "members": members_out,
            })
            continue

        grid = bench.index
        d_last = grid[-1].strftime("%Y-%m-%d")
        if latest_date is None or d_last > latest_date:
            latest_date = d_last

        for tk, label in uni["members"]:
            s = cache_s.get(tk)
            if s is None:
                members_out.append({"ticker": tk, "label": label, "status": "insufficient"})
                continue
            aligned = s.reindex(grid).ffill()
            rs = 100.0 * aligned / bench
            rs = rs.dropna()
            frames = _compute_frames(rs, pd)
            has_any = any(frames[fk]["trail"] for fk in FRAME_ORDER)
            if not has_any:
                members_out.append({"ticker": tk, "label": label, "status": "insufficient"})
                continue
            n_ok += 1
            members_out.append({
                "ticker": tk, "label": label, "status": "ok", "frames": frames,
            })

        out_universes.append({
            "key": uni["key"], "label": uni["label"],
            "benchmark": uni["benchmark"], "members": members_out,
            "_n_ok": n_ok,
        })

    return out_universes, latest_date


# ───────────────────────────────────────────────────────────────────────────
# Orchestration
# ───────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Asset rotation radar daily builder")
    ap.add_argument("--skip-fetch", action="store_true",
                    help="offline: skip fetch, recompute from cache only")
    args = ap.parse_args()

    # Unique tickers across all universes (benchmarks included), first-seen order.
    tickers = []
    for uni in UNIVERSES:
        for t in [uni["benchmark"]["ticker"]] + [m[0] for m in uni["members"]]:
            if t not in tickers:
                tickers.append(t)

    series, stooq_used = refresh_cache(tickers, args.skip_fetch)
    out_universes, latest_date = compute(series)

    # Zero-ok gate: exit non-zero only if a whole universe has no ok members.
    empty_unis = [u["key"] for u in out_universes if u.get("_n_ok", 0) == 0]

    method = {
        "rs_ratio": "JdK-style: 100+(RS-SMA(RS,W))/STD(RS,max(W,60)); "
                    "RS=100*price/benchmark_price aligned on benchmark grid (ffill)",
        "rs_mom": "100+(rs_ratio-SMA(rs_ratio,Wm))/STD(rs_ratio,max(Wm,24)); "
                  f"both smoothed with SMA({TRAIL_SMOOTH}d) before trail extraction",
        "frames": "120: W=120,Wm=30,trail=30 · 60: W=60,Wm=15,trail=20 · "
                  "20: W=20,Wm=8,trail=10 (daily trading days, oldest->newest, "
                  "last point = current)",
        "std_window": "均值窗＝W／Wm，但標準差（分母）用有下限的窗："
                      f"rs_ratio 用 max(W,{STD_FLOOR})、rs_mom 用 max(Wm,{MOM_STD_FLOOR})。"
                      "短框架（20d）的離散度若只用 20 個樣本估計會過度抖動，"
                      "拉高 std 窗讓歸一化分母穩定、彗尾不再因估計噪音亂甩。",
        "semantics": "本圖為波動歸一化的 z-score 版 RRG——圖上距離代表相對強弱變化的"
                     "統計顯著度，不是絕對超額報酬幅度；低波動資產（如投資級債）與"
                     "高波動資產（如比特幣）在圖上移動相同距離，對應的實際報酬差異很大。"
                     f"標準差窗採下限制（rs_ratio max(W,{STD_FLOOR})、rs_mom max(Wm,{MOM_STD_FLOOR})），"
                     "使短框架的歸一化分母不被少樣本估計噪音放大。",
        "disclaimer": "描述器非擇時。相對輪動排名，衡量各資產／板塊相對其基準的"
                      "強度與動能方向，非買賣訊號、非市場絕對報酬預測。",
    }

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": latest_date or "",
        "frames": FRAME_ORDER,
        "universes": [{k: v for k, v in u.items() if k != "_n_ok"} for u in out_universes],
        "method": method,
    }

    wrote = write_json_if_changed(OUT_JSON, payload, volatile=("generated_at",))
    info(f"radar.json: {'written' if wrote else 'no change'} (as_of {payload['as_of']})")

    # Daily snapshot: same payload keyed by as_of — 累積歷史供未來長程輪動回放與復盤驗證.
    # Zero-churn / idempotent: a re-run on the same as_of hits an identical file
    # (generated_at stripped) so it is a no-op; weekends keep as_of unchanged so
    # they naturally write nothing new.
    if payload["as_of"]:
        snap_path = os.path.join(SNAP_DIR, f"{payload['as_of']}.json")
        snap_wrote = write_json_if_changed(snap_path, payload, volatile=("generated_at",))
        info(f"snapshot {payload['as_of']}.json: {'written' if snap_wrote else 'no change'}")

    # Summary: per-universe quadrant placement using the mid frame ("60") current.
    print("\n── quadrant placement (frame 60, current point) ──")
    for u in out_universes:
        from collections import Counter
        qc = Counter()
        detail = []
        for m in u["members"]:
            if m.get("status") != "ok":
                detail.append(f"{m['ticker']}:insuf")
                continue
            tr = m["frames"]["60"]["trail"]
            if not tr:
                detail.append(f"{m['ticker']}:no60")
                continue
            r, mm = tr[-1]["r"], tr[-1]["m"]
            q = quadrant(r, mm)
            qc[q] += 1
            detail.append(f"{m['ticker']}:{q[:4]}({r:.1f},{mm:.1f})")
        print(f"  [{u['key']}] ok={u.get('_n_ok',0)}/{len(u['members'])} "
              f"{dict(qc)}")
        print("     " + "  ".join(detail))

    if stooq_used:
        info(f"stooq fallback tickers: {sorted(stooq_used)}")
    if empty_unis:
        warn(f"universes with zero ok members: {empty_unis} — exiting non-zero")
        sys.exit(1)
    info("done.")


if __name__ == "__main__":
    main()
