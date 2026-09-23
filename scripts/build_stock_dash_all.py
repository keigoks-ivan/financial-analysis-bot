#!/usr/bin/env python3
"""build_stock_dash_all.py — batch driver for scripts/build_stock_dash.py.

Builds every ticker in docs/dd-screener/latest.json's stocks[] (the universe
the /stock-dash/ page actually serves — see docs/stock-dash/index.html and
scripts/build_stock_dash.py's own docstring) with bounded parallelism, a
per-ticker timeout, and one hard rule: no single ticker's failure or hang can
kill the run. Failures are logged and the run continues; a small
docs/stock-dash/data/_build_report.json summarizes counts/timing/failures
for whoever (human or the daily workflow) checks the run afterwards.

Each ticker is built in its own subprocess (`python3 build_stock_dash.py T`),
matching how the script is normally invoked — a crash, an infinite hang, or
excess memory use in one ticker's build can never take down the batch, only
that one subprocess.

Shared, per-run (not per-ticker) work:
  - docs/stock-dash/data/_universe_dist.json (percentile-cut universe used by
    the trend/relative-strength/volume score dims) is pre-built once, before
    any ticker subprocess starts, by calling build_stock_dash.
    ensure_universe_distribution() directly. build_stock_dash.py's own
    freshness check (see that function) then makes every per-ticker call a
    same-day no-op read instead of a second ~518-ticker yfinance download.
  - docs/stock-dash/data/_market.json is likewise pre-built once via
    ensure_market_context() so the first tickers in the pool don't race each
    other rebuilding it (build_stock_dash.py's version of that function was
    made an atomic write for this reason — see its docstring — but the
    prewarm here still avoids the redundant work of N re-parses on a cold
    cache).
  - FINRA Reg SHO daily short-volume files and yfinance SPY history, which
    build_stock_dash.py used to redownload fresh for every ticker even though
    the content is identical across tickers on the same day, are now cached
    on disk (see build_stock_dash.py's FINRA_CACHE_DIR / HIST_CACHE_DIR) —
    this script sets STOCK_DASH_HIST_CACHE_DIR so every subprocess it spawns
    shares one SPY-history cache directory for the run (FINRA caching needs
    no env var; it defaults on to a fixed temp path, see build_stock_dash.py).

Usage:
    python3.12 scripts/build_stock_dash_all.py                  # full run, CI defaults
    python3.12 scripts/build_stock_dash_all.py --workers 3 --tickers NVDA,2330.TW
    python3.12 scripts/build_stock_dash_all.py --limit 12 --workers 3
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
BUILD_SCRIPT = SCRIPTS_DIR / "build_stock_dash.py"
DD_SCREENER_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
OUT_DIR = ROOT / "docs" / "stock-dash" / "data"
BUILD_REPORT_PATH = OUT_DIR / "_build_report.json"

DEFAULT_WORKERS = 2          # bounded parallelism — kept deliberately low: workers=6 got the
                              # GitHub runner's IP yfinance-rate-limited around ticker #186/339
                              # (run 35823204018, 2026-09-23), after which every remaining ticker
                              # failed in 1-2s with YFRateLimitError for the rest of the run.
DEFAULT_TIMEOUT_S = 240      # per-ticker hard timeout; typical build is ~40s
DEFAULT_STAGGER_S = 1.5      # minimum gap between *submitting* consecutive ticker builds, so a
                              # burst of `workers` subprocesses never all hit yfinance at once.
RATE_LIMIT_BACKOFFS_S = [60, 120, 240]  # wait before each retry pass over YFRateLimitError failures
FAIL_THRESHOLD_PCT = 10      # exit non-zero (job goes red) if more than this % of tickers still
                              # failed after retries — see main() for why this is safe for deploy.

sys.path.insert(0, str(SCRIPTS_DIR))
import build_stock_dash as bsd  # noqa: E402  (needs sys.path set up first)


def load_tickers():
    """dd-screener's stocks[] — the universe /stock-dash/ actually serves
    (Background in the task spec: 339 tickers today, updated daily by the
    existing dd-screener CI). Distinct from docs/screener/latest.json, which
    is a different, larger RS+VCP universe used only internally by
    build_stock_dash.py for percentile scoring."""
    if not DD_SCREENER_LATEST.exists():
        return [], None
    try:
        d = json.loads(DD_SCREENER_LATEST.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"[build_stock_dash_all] FAILED to parse {DD_SCREENER_LATEST}: {e}", file=sys.stderr)
        return [], None
    tickers = sorted({str(s["ticker"]).strip() for s in d.get("stocks", []) if s.get("ticker")})
    return tickers, d.get("as_of")


def prebuild_shared_files(refresh_universe):
    """Build the two shared JSON files once, sequentially, before any ticker
    subprocess starts — see module docstring. Returns a small status dict for
    _build_report.json. Failures here are logged but never abort the run:
    every per-ticker build falls back to building its own copy if these are
    missing (same behavior as running build_stock_dash.py standalone)."""
    status = {}

    t0 = time.time()
    try:
        _tickers, screener_as_of = bsd.load_universe_tickers()
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        ctx = bsd.ensure_universe_distribution(screener_as_of or today_str, force=refresh_universe)
        status["universe_distribution"] = {
            "ok": ctx.get("status") != "no_data",
            "status": ctx.get("status", "ok"),
            "n_tickers_requested": ctx.get("n_tickers_requested"),
            "seconds": round(time.time() - t0, 1),
        }
    except Exception as e:  # noqa: BLE001
        status["universe_distribution"] = {"ok": False, "error": str(e), "seconds": round(time.time() - t0, 1)}

    t0 = time.time()
    try:
        bsd.ensure_market_context()
        status["market_context"] = {"ok": OUT_DIR.joinpath("_market.json").exists(), "seconds": round(time.time() - t0, 1)}
    except Exception as e:  # noqa: BLE001
        status["market_context"] = {"ok": False, "error": str(e), "seconds": round(time.time() - t0, 1)}

    return status


def build_one(python_bin, ticker, timeout, env, extra_args):
    cmd = [python_bin, str(BUILD_SCRIPT), ticker] + extra_args
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd, timeout=timeout, capture_output=True, text=True, env=env, cwd=str(ROOT),
        )
        dt = time.time() - t0
        if proc.returncode != 0:
            stderr_tail = proc.stderr[-2000:] if proc.stderr else ""
            return {
                "ticker": ticker, "ok": False, "seconds": round(dt, 1),
                "error": f"exit {proc.returncode}",
                "stderr_tail": stderr_tail,
                # yfinance raises this uncaught (see yfinance.exceptions.YFRateLimitError),
                # so its class name always lands in the traceback build_stock_dash.py prints
                # to stderr on the way to its exit-1 — cheap, reliable signal to retry on.
                "rate_limited": "YFRateLimitError" in stderr_tail,
            }
        return {"ticker": ticker, "ok": True, "seconds": round(dt, 1)}
    except subprocess.TimeoutExpired:
        return {"ticker": ticker, "ok": False, "seconds": round(time.time() - t0, 1),
                 "error": f"timeout after {timeout}s", "rate_limited": False}
    except Exception as e:  # noqa: BLE001
        return {"ticker": ticker, "ok": False, "seconds": round(time.time() - t0, 1),
                 "error": str(e), "rate_limited": False}


def run_batch(tickers, python_bin, timeout, env, extra_args, workers, stagger):
    """Build `tickers` with bounded parallelism, pacing how fast new subprocesses
    are *submitted* (not just how many run at once) so `workers` of them never all
    hit yfinance in the same instant. Returns {ticker: result_dict}, one entry per
    input ticker."""
    results = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {}
        for i, t in enumerate(tickers):
            if i > 0 and stagger > 0:
                time.sleep(stagger)
            futs[ex.submit(build_one, python_bin, t, timeout, env, extra_args)] = t
        n_done = 0
        for fut in as_completed(futs):
            r = fut.result()
            results[r["ticker"]] = r
            n_done += 1
            tag = "ok" if r["ok"] else f"FAIL ({r.get('error')})"
            print(f"[build_stock_dash_all] ({n_done}/{len(tickers)}) {r['ticker']}: {tag} in {r['seconds']}s")
    return results


def main():
    ap = argparse.ArgumentParser(description="Batch-build docs/stock-dash/data/{T}.json for every dd-screener ticker.")
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"bounded parallelism (default {DEFAULT_WORKERS})")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S, help=f"per-ticker hard timeout, seconds (default {DEFAULT_TIMEOUT_S})")
    ap.add_argument("--tickers", default=None, help="comma-separated ticker list, overrides dd-screener/latest.json (testing)")
    ap.add_argument("--limit", type=int, default=None, help="build only the first N tickers (testing)")
    ap.add_argument("--refresh-universe", action="store_true", help="force-rebuild _universe_dist.json even if it looks fresh")
    ap.add_argument("--state-dir", default=None, help="passthrough to build_stock_dash.py --state-dir (testing)")
    ap.add_argument("--python", default=sys.executable, help="python interpreter to invoke build_stock_dash.py with")
    ap.add_argument("--hist-cache-dir", default=None,
                     help="dir for the shared SPY-history cache (default: a fresh temp dir, cleaned up on a clean exit)")
    ap.add_argument("--stagger", type=float, default=DEFAULT_STAGGER_S,
                     help=f"minimum seconds between submitting consecutive ticker builds (default {DEFAULT_STAGGER_S})")
    ap.add_argument("--fail-threshold-pct", type=float, default=FAIL_THRESHOLD_PCT,
                     help=f"exit non-zero if more than this %% of tickers still fail after retries (default {FAIL_THRESHOLD_PCT})")
    args = ap.parse_args()

    started_at = datetime.now(timezone.utc)
    t_start = time.time()

    if args.tickers:
        tickers = sorted({t.strip().upper() for t in args.tickers.split(",") if t.strip()})
        screener_as_of = None
    else:
        tickers, screener_as_of = load_tickers()
    if args.limit:
        tickers = tickers[: args.limit]

    if not tickers:
        print(f"[build_stock_dash_all] No tickers found (checked {DD_SCREENER_LATEST}) — nothing to build.", file=sys.stderr)
        sys.exit(1)

    print(f"[build_stock_dash_all] {len(tickers)} tickers, workers={args.workers}, timeout={args.timeout}s, "
          f"dd-screener as_of={screener_as_of}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("[build_stock_dash_all] pre-building shared files (universe distribution, market context)...")
    shared_status = prebuild_shared_files(args.refresh_universe)
    print(f"[build_stock_dash_all] shared files: {json.dumps(shared_status, ensure_ascii=False)}")

    hist_cache_dir = Path(args.hist_cache_dir) if args.hist_cache_dir else Path(tempfile.mkdtemp(prefix="stock_dash_hist_cache_"))
    own_hist_cache_dir = args.hist_cache_dir is None  # only clean up a dir we created ourselves
    env = dict(os.environ)
    env["STOCK_DASH_HIST_CACHE_DIR"] = str(hist_cache_dir)

    extra_args = []
    if args.refresh_universe:
        extra_args.append("--refresh-universe")
    if args.state_dir:
        extra_args += ["--state-dir", args.state_dir]

    results = run_batch(tickers, args.python, args.timeout, env, extra_args, args.workers, args.stagger)

    # Retry pass: a ticker that failed with YFRateLimitError gets a few more chances,
    # each after a longer backoff, on the theory that the runner's IP just needs to
    # cool off (see the run 35823204018 incident in the DEFAULT_WORKERS comment above).
    # Non-rate-limited failures (e.g. 5274.TW / 8299.TW's "Quote not found" 404, which
    # will never succeed) are left alone — retrying them would just burn backoff time.
    retry_passes = []
    for round_num, backoff in enumerate(RATE_LIMIT_BACKOFFS_S, start=1):
        rate_limited = [t for t in tickers if not results[t]["ok"] and results[t].get("rate_limited")]
        if not rate_limited:
            break
        print(f"[build_stock_dash_all] retry pass {round_num}/{len(RATE_LIMIT_BACKOFFS_S)}: "
              f"{len(rate_limited)} rate-limited ticker(s), waiting {backoff}s before retrying: "
              f"{', '.join(rate_limited)}")
        time.sleep(backoff)
        retry_results = run_batch(rate_limited, args.python, args.timeout, env, extra_args, args.workers, args.stagger)
        n_recovered = sum(1 for r in retry_results.values() if r["ok"])
        print(f"[build_stock_dash_all] retry pass {round_num} recovered {n_recovered}/{len(rate_limited)}")
        retry_passes.append({"pass": round_num, "backoff_seconds": backoff,
                              "n_retried": len(rate_limited), "n_recovered": n_recovered})
        results.update(retry_results)

    if own_hist_cache_dir:
        shutil.rmtree(hist_cache_dir, ignore_errors=True)

    finished_at = datetime.now(timezone.utc)
    total_seconds = time.time() - t_start
    results_list = [results[t] for t in tickers]
    seconds_list = sorted(r["seconds"] for r in results_list)
    failures = [{"ticker": r["ticker"], "error": r.get("error"), "seconds": r["seconds"],
                 "stderr_tail": r.get("stderr_tail", "")} for r in results_list if not r["ok"]]
    n_ok = len(results_list) - len(failures)

    def pct(p):
        if not seconds_list:
            return None
        idx = min(len(seconds_list) - 1, int(len(seconds_list) * p))
        return seconds_list[idx]

    report = {
        "schema": "stock-dash-build-report-v1",
        "started_at": started_at.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "finished_at": finished_at.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "duration_seconds": round(total_seconds, 1),
        "workers": args.workers,
        "per_ticker_timeout_seconds": args.timeout,
        "dd_screener_as_of": screener_as_of,
        "n_tickers": len(tickers),
        "n_ok": n_ok,
        "n_failed": len(failures),
        "timing_seconds": {
            "min": seconds_list[0] if seconds_list else None,
            "p50": pct(0.50),
            "p90": pct(0.90),
            "max": seconds_list[-1] if seconds_list else None,
            "mean": round(sum(seconds_list) / len(seconds_list), 1) if seconds_list else None,
        },
        "shared_files": shared_status,
        "retry_passes": retry_passes,
        "failures": failures,
    }
    BUILD_REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    fail_pct = (len(failures) / len(tickers) * 100) if tickers else 0.0
    print(f"[build_stock_dash_all] done in {total_seconds:.1f}s — {n_ok}/{len(tickers)} ok, "
          f"{len(failures)} failed ({fail_pct:.1f}%)")
    print(f"[build_stock_dash_all] report written to {BUILD_REPORT_PATH}")
    if failures:
        print(f"[build_stock_dash_all] failed tickers: {', '.join(f['ticker'] for f in failures)}")
    # A handful of individual ticker failures never fail the batch (that's the whole
    # point of this script) — but if more than --fail-threshold-pct still failed even
    # after the rate-limit retries above, something is systemically wrong (e.g. the
    # whole run got rate-limited again), so the job exits non-zero to go red instead of
    # silently publishing a run that's missing a large chunk of tickers. This is safe
    # for deploy-pages.yml: its artifact-restore step only ever downloads this
    # workflow's *last successful* run (`gh run list --status success`), so a failed
    # run here is simply skipped and the site keeps serving the previous good day's
    # data instead of this run's holes.
    if fail_pct > args.fail_threshold_pct:
        print(f"[build_stock_dash_all] FAILING: {fail_pct:.1f}% of tickers failed, "
              f"over the {args.fail_threshold_pct}% threshold.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
