#!/usr/bin/env python3
"""Daily prices cache builder — region-split (US / TW).

Builds `docs/cache/prices-{us,tw}.json` by **mirroring** existing screener
output JSONs. yfinance is only hit for the handful of DD tickers (EU/JP)
that are not in screener.py / screener_tw.py universes — typically ~5-30
tickers via `yf.download()` batch.

Refresh cadence: daily (Tue–Sat per region's market open). See plan: cache
layer is producer-only, no consumer is wired up yet.

Schema v1.0 — per ticker (~12 fields):
  currency
  price / close_change_pct / volume
  high_52w / low_52w / dist_52w_high_pct
  ma21_pct / ma50_pct / vs_200ma_pct
  rs_score / rs_rating / rs_1w / rs_4w / rs_13w
  rsi14 / atr_pct
  trend_ok
  source: screener-us-mirror | screener-tw-mirror | yfinance-fallback

Top-level `indices`:
  US: SPY + QQQ (from screener/market_state.json + six-state/state.json)
  TW: ^TWII (from yfinance batch)

CLI:
  python3 scripts/build_prices_cache.py --region us
  python3 scripts/build_prices_cache.py --region tw
  python3 scripts/build_prices_cache.py --region us --dry-run
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
import warnings
from datetime import datetime, timezone, timedelta
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "pandas", "numpy", "-q"])
    import yfinance as yf
    import pandas as pd
    import numpy as np

logging.getLogger("yfinance").setLevel(logging.CRITICAL)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_fundamentals_cache import (  # noqa: E402
    build_universe,
    _infer_currency,
    _yf_ticker_for_local,
    ABORT_FAILURE_RATIO,
    PARTIAL_ERROR_RATIO,
    PARTIAL_WARN_RATIO,
)

SCHEMA_VERSION = "1.0"
OUTPUT_DIR = ROOT / "docs" / "cache"

SCREENER_US_PATH = ROOT / "docs" / "screener" / "latest.json"
SCREENER_TW_PATH = ROOT / "docs" / "screener" / "tw_latest.json"
MARKET_STATE_PATH = ROOT / "docs" / "screener" / "market_state.json"
SIX_STATE_PATH = ROOT / "docs" / "six-state" / "state.json"


# Fields we mirror from screener.py / screener_tw.py per-ticker output
SCREENER_FIELDS = (
    "price", "close_change_pct",
    "rs_score", "rs_trend", "rs_1w", "rs_4w", "rs_13w", "rs_rating",
    "vcp_score", "pullback_count", "last_pullback_pct",
    "dist_from_high_pct", "dist_52w_high_pct",
    "ma21_pct", "ma50_pct", "vs_200ma_pct", "trend_ok",
    "atr_pct", "atr_ratio", "vol_ratio",
    "rsi14",
)


def _round(v, digits=2):
    if v is None:
        return None
    try:
        return round(float(v), digits)
    except (TypeError, ValueError):
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Screener mirror
# ─────────────────────────────────────────────────────────────────────────────

def mirror_screener(path: Path, source_tag: str) -> dict[str, dict]:
    """Read screener latest.json → per-ticker dict matching our schema."""
    out: dict[str, dict] = {}
    if not path.exists():
        print(f"  WARN: {path} not found", file=sys.stderr)
        return out
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"  WARN: failed to parse {path}: {e}", file=sys.stderr)
        return out

    for r in data.get("rankings", []) or []:
        t = r.get("ticker")
        if not t:
            continue
        row = {k: r.get(k) for k in SCREENER_FIELDS if k in r}
        row["currency"] = _infer_currency(t)
        row["source"] = source_tag
        out[t] = row
    return out


# ─────────────────────────────────────────────────────────────────────────────
# yfinance fallback (small batch, ~30 tickers max)
# ─────────────────────────────────────────────────────────────────────────────

def yfinance_fallback(missing: list[str]) -> dict[str, dict]:
    """For DD tickers not in screener output, compute snapshot via yf.download() batch.

    Returns {ticker: row} with same fields as screener mirror, source="yfinance-fallback".
    Falls back gracefully — tickers yfinance fails on get None values.
    """
    out: dict[str, dict] = {}
    if not missing:
        return out

    yf_map = {t: _yf_ticker_for_local(t) for t in missing}
    yf_tickers = list(set(yf_map.values()))
    print(f"  [fallback] batch download {len(yf_tickers)} yfinance tickers ...")

    try:
        raw = yf.download(yf_tickers, period="1y", interval="1d",
                          progress=False, group_by="ticker", auto_adjust=True,
                          threads=True)
    except Exception as e:
        print(f"  [fallback] download failed: {e}", file=sys.stderr)
        return out

    if raw is None or getattr(raw, "empty", True):
        return out

    for dd_t, yf_t in yf_map.items():
        try:
            # Single ticker: columns are top-level (Open/High/Low/Close/Volume)
            # Multi ticker: columns are MultiIndex (yf_t, field)
            if isinstance(raw.columns, pd.MultiIndex):
                if yf_t not in raw.columns.levels[0]:
                    continue
                df = raw[yf_t].dropna()
            else:
                df = raw.dropna()
            if df.empty or len(df) < 50:
                continue

            closes = df["Close"]
            highs = df["High"]
            lows = df["Low"]
            volumes = df["Volume"]

            price = float(closes.iloc[-1])
            prev_close = float(closes.iloc[-2]) if len(closes) > 1 else price
            close_change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0.0

            # 52w high/low (rolling)
            recent_52w = closes.iloc[-252:] if len(closes) >= 252 else closes
            high_52w = float(recent_52w.max())
            low_52w = float(recent_52w.min())
            dist_52w_high = (price - high_52w) / high_52w * 100

            # MAs
            ma21 = float(closes.iloc[-21:].mean()) if len(closes) >= 21 else None
            ma50 = float(closes.iloc[-50:].mean()) if len(closes) >= 50 else None
            ma200 = float(closes.iloc[-200:].mean()) if len(closes) >= 200 else None
            ma21_pct = (price - ma21) / ma21 * 100 if ma21 else None
            ma50_pct = (price - ma50) / ma50 * 100 if ma50 else None
            vs_200ma_pct = (price - ma200) / ma200 * 100 if ma200 else None

            # trend_ok: 200ma rising over last ~21d
            trend_ok = None
            if ma200 and len(closes) >= 221:
                ma200_21d_ago = float(closes.iloc[-221:-21].mean())
                trend_ok = ma200 > ma200_21d_ago

            # ATR(14)
            tr = pd.concat([
                highs - lows,
                (highs - closes.shift()).abs(),
                (lows - closes.shift()).abs(),
            ], axis=1).max(axis=1)
            atr14 = float(tr.iloc[-14:].mean()) if len(tr) >= 14 else None
            atr_pct = (atr14 / price * 100) if atr14 else None

            # RSI(14)
            delta = closes.diff()
            gain = delta.clip(lower=0).rolling(14).mean()
            loss = (-delta.clip(upper=0)).rolling(14).mean()
            rs = gain.iloc[-1] / loss.iloc[-1] if loss.iloc[-1] else None
            rsi14 = (100 - 100 / (1 + rs)) if rs else None

            out[dd_t] = {
                "currency": _infer_currency(dd_t),
                "price": _round(price, 2),
                "close_change_pct": _round(close_change_pct, 2),
                "high_52w": _round(high_52w, 2),
                "low_52w": _round(low_52w, 2),
                "dist_52w_high_pct": _round(dist_52w_high, 2),
                "ma21_pct": _round(ma21_pct, 1),
                "ma50_pct": _round(ma50_pct, 1),
                "vs_200ma_pct": _round(vs_200ma_pct, 1),
                "trend_ok": trend_ok,
                "atr_pct": _round(atr_pct, 2),
                "rsi14": _round(rsi14, 1),
                # No RS score from yfinance — left None (computed only by screener.py vs full universe)
                "rs_score": None, "rs_rating": None,
                "source": "yfinance-fallback",
            }
        except Exception:
            continue

    print(f"  [fallback] success: {len(out)}/{len(missing)} tickers")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Indices (US: SPY/QQQ from market_state + six-state; TW: TWII from yfinance)
# ─────────────────────────────────────────────────────────────────────────────

def _state_to_pure_ma(state: str) -> tuple[str, str]:
    """Convert market_state.json state → (label, color) approximating dd-screener convention."""
    if not state:
        return ("未知", "gray")
    mapping = {
        "confirmed_uptrend": ("確認上升", "green"),
        "early_uptrend": ("初升", "green"),
        "uptrend_under_pressure": ("上升承壓", "amber"),
        "rally_attempt": ("反彈嘗試", "amber"),
        "correction": ("修正", "red"),
        "downtrend": ("下降", "red"),
    }
    return mapping.get(state, (state.replace("_", " "), "gray"))


def build_us_indices() -> dict:
    """SPY + QQQ from market_state.json + QQQ six-state state.json + rs_peaks."""
    indices = {}
    # SPY / QQQ from market_state
    try:
        if MARKET_STATE_PATH.exists():
            ms = json.loads(MARKET_STATE_PATH.read_text(encoding="utf-8"))
            for sym in ("SPY", "QQQ"):
                d = (ms.get("indices") or {}).get(sym, {})
                if not d:
                    continue
                state = d.get("state")
                label, color = _state_to_pure_ma(state)
                indices[sym] = {
                    "currency": "USD",
                    "price": _round(d.get("close"), 2),
                    "close_change_pct": _round(d.get("close_change_pct"), 2),
                    "vs_50ma_pct": _round(d.get("vs_50dma_pct"), 1),
                    "vs_200ma_pct": _round(d.get("vs_200dma_pct"), 1),
                    "drawdown_52w_high_pct": _round(d.get("drawdown_52w_high_pct"), 2),
                    "ma50_above_200": d.get("ma50_above_200"),
                    "market_state": state,
                    "pure_ma_label": label,
                    "pure_ma_color": color,
                    "distribution_days_25d": (d.get("distribution_days") or {}).get("count_25d"),
                }
    except Exception as e:
        print(f"  WARN: market_state mirror failed: {e}", file=sys.stderr)

    # QQQ six-state overlay (separate from market_state — different methodology)
    try:
        if SIX_STATE_PATH.exists():
            ss = json.loads(SIX_STATE_PATH.read_text(encoding="utf-8"))
            if "QQQ" not in indices:
                indices["QQQ"] = {"currency": "USD"}
            indices["QQQ"].update({
                "six_state_id": ss.get("state"),
                "six_state_label": ss.get("state_name"),
                "six_state_exposure_pct": ss.get("exposure_pct"),
                "six_state_grid_enabled": ss.get("grid_enabled"),
            })
    except Exception as e:
        print(f"  WARN: six-state mirror failed: {e}", file=sys.stderr)

    return indices


def build_tw_indices() -> dict:
    """^TWII via yfinance."""
    indices = {}
    try:
        t = yf.Ticker("^TWII")
        hist = t.history(period="1y", interval="1d")
        if hist is None or hist.empty:
            return indices
        closes = hist["Close"].dropna()
        if closes.empty:
            return indices
        price = float(closes.iloc[-1])
        prev = float(closes.iloc[-2]) if len(closes) > 1 else price
        change_pct = (price - prev) / prev * 100 if prev else 0.0
        recent = closes.iloc[-252:] if len(closes) >= 252 else closes
        high_52w = float(recent.max())
        low_52w = float(recent.min())
        dd_pct = (price - high_52w) / high_52w * 100
        ma50 = float(closes.iloc[-50:].mean()) if len(closes) >= 50 else None
        ma200 = float(closes.iloc[-200:].mean()) if len(closes) >= 200 else None
        indices["TWII"] = {
            "currency": "TWD",
            "price": _round(price, 2),
            "close_change_pct": _round(change_pct, 2),
            "high_52w": _round(high_52w, 2),
            "low_52w": _round(low_52w, 2),
            "drawdown_52w_high_pct": _round(dd_pct, 2),
            "vs_50ma_pct": _round((price - ma50) / ma50 * 100 if ma50 else None, 1),
            "vs_200ma_pct": _round((price - ma200) / ma200 * 100 if ma200 else None, 1),
        }
    except Exception as e:
        print(f"  WARN: ^TWII fetch failed: {e}", file=sys.stderr)
    return indices


# ─────────────────────────────────────────────────────────────────────────────
# Main build
# ─────────────────────────────────────────────────────────────────────────────

def build_cache(region: str, dry_run: bool = False) -> dict:
    t0 = time.time()
    print(f"=== Prices cache build · region={region} · "
          f"{datetime.now().isoformat(timespec='seconds')} ===\n")

    universe = build_universe(region)
    print(f"  Universe: {len(universe)} tickers ({region})")

    # Mirror screener output
    if region == "us":
        mirror = mirror_screener(SCREENER_US_PATH, "screener-us-mirror")
        indices = build_us_indices()
    else:
        mirror = mirror_screener(SCREENER_TW_PATH, "screener-tw-mirror")
        indices = build_tw_indices()
    print(f"  Mirror: {len(mirror)} tickers from screener output")

    # Fallback for missing tickers in DD universe
    missing = [t for t in universe if t not in mirror]
    print(f"  Missing from screener: {len(missing)} tickers (will yfinance fallback)")
    fallback = yfinance_fallback(missing) if missing else {}

    # Combine — keep only tickers in our universe
    tickers: dict[str, dict] = {}
    failed: list[str] = []
    for t in universe:
        if t in mirror:
            tickers[t] = mirror[t]
        elif t in fallback:
            tickers[t] = fallback[t]
        else:
            failed.append(t)

    failure_ratio = len(failed) / max(1, len(universe))

    if failure_ratio >= ABORT_FAILURE_RATIO:
        print(f"\n  ABORT: {len(failed)}/{len(universe)} ({failure_ratio:.0%}) missing — "
              f"refusing to overwrite cache", file=sys.stderr)
        sys.exit(1)

    if failure_ratio >= PARTIAL_ERROR_RATIO:
        status = "partial-error"
    elif failure_ratio >= PARTIAL_WARN_RATIO:
        status = "partial-warn"
    else:
        status = "ok"

    src_counts: dict[str, int] = {}
    for row in tickers.values():
        s = row.get("source", "unknown")
        src_counts[s] = src_counts.get(s, 0) + 1
    src_counts["failed"] = len(failed)

    runtime = time.time() - t0

    out = {
        "schema_version": SCHEMA_VERSION,
        "region": region,
        "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "run_timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "universe_size": len(universe),
        "source_breakdown": src_counts,
        "health": {
            "status": status,
            "success_count": len(tickers),
            "failed_count": len(failed),
            "failure_ratio": round(failure_ratio, 4),
            "runtime_seconds": int(runtime),
        },
        "failed_tickers": sorted(failed),
        "indices": indices,
        "tickers": tickers,
    }

    print(f"\n  Source breakdown: {src_counts}")
    print(f"  Indices: {list(indices.keys())}")
    print(f"  Health: {status} (failure ratio {failure_ratio:.1%})")
    print(f"  Runtime: {runtime:.0f}s")

    if dry_run:
        print(f"\n  [dry-run] would write {OUTPUT_DIR}/prices-{region}.json "
              f"(~{len(json.dumps(out)) / 1024:.0f} KB)")
        return out

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"prices-{region}.json"
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, out_path)
    print(f"\n  ✓ Wrote {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--region", required=True, choices=("us", "tw"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    build_cache(args.region, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
