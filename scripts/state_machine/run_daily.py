#!/usr/bin/env python3
"""五狀態機每日判定 — run_daily.py（主程式）。

管線（SPEC §2 / §4 / §6）：
  load universe + positions(held) + earnings → fetch/cache 日線 → 逐檔算指標 →
  state_machine.evaluate（讀 state.json/breakouts.json 記憶）→ 寫 state.json /
  breakouts.json（記憶，commit 回 repo）+ daily.json（公開，只 held 布林、無部位數字）。

用法：
  python3 scripts/state_machine/run_daily.py            # 全 universe
  python3 scripts/state_machine/run_daily.py --top 12   # 冒煙測試前 12 檔
  python3 scripts/state_machine/run_daily.py --dry-run  # 不寫檔
  python3 scripts/state_machine/run_daily.py --as-of 2026-06-10   # 固定判定日（測試/回放）
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np

ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent))   # scripts/ — for dd_screener_quality ticker maps

import config as CFG  # noqa: E402
from indicators import compute_indicators  # noqa: E402
from price_cache import load_prices  # noqa: E402
import state_machine as SM  # noqa: E402

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance>=0.2.40", "-q"])
    import yfinance as yf

# yfinance ticker resolution — reuse the site-wide EU/override maps for consistency.
try:
    from dd_screener_quality import EU_SUFFIX_MAP, TICKER_YF_OVERRIDE
except Exception:
    EU_SUFFIX_MAP, TICKER_YF_OVERRIDE = {}, {}

TAIPEI_TZ = timezone(timedelta(hours=8))
EARNINGS_CACHE = CFG.PRICE_CACHE_DIR / "earnings.json"
EARNINGS_REFRESH_DAYS = 3


# ── helpers ─────────────────────────────────────────────────────────────────
def _yf_ticker(dd_ticker: str) -> str:
    if dd_ticker in TICKER_YF_OVERRIDE:
        return TICKER_YF_OVERRIDE[dd_ticker]
    if dd_ticker in EU_SUFFIX_MAP:
        return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}"
    return dd_ticker


def _parse_held(positions) -> set:
    """positions.json → held symbol set。容忍三種格式（皆只讀「是否持有」，不讀數字）：
      {"held": ["NVDA", ...]} / {"held": {"NVDA": true}} / {"NVDA": true|{...}}。
    """
    if not isinstance(positions, dict):
        return set()
    body = positions.get("held", positions)
    held = set()
    if isinstance(body, list):
        return set(body)
    if isinstance(body, dict):
        for k, v in body.items():
            if isinstance(v, dict):
                if v.get("held", True):
                    held.add(k)
            elif v:
                held.add(k)
    return held


def _market_of(t: str) -> str:
    if t.endswith(".TW") or t.endswith(".TWO"):
        return "TW"
    if t.endswith(".T"):
        return "JP"
    if "." in t:
        return "EU"
    return "US"


def _load_json(p: Path, default):
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  WARN: failed to read {p.name}: {exc}", file=sys.stderr)
        return default


def _write_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def load_universe() -> list[dict]:
    """universe.json → [{symbol, market, quality_pass}]. 若缺檔，從 dd-screener
    latest.json 自動 seed（symbol + market + quality_pass = QGM pass_count ≥ 4）。"""
    raw = _load_json(CFG.UNIVERSE_PATH, None)
    if raw is None:
        seed = _seed_universe_from_dd_screener()
        _write_json(CFG.UNIVERSE_PATH, seed)
        raw = seed
    return raw.get("tickers", raw) if isinstance(raw, dict) else raw


def _seed_universe_from_dd_screener() -> dict:
    p = CFG.REPO_ROOT / "docs" / "dd-screener" / "latest.json"
    data = _load_json(p, {"stocks": []})
    tickers = []
    for s in data.get("stocks", []):
        t = s.get("ticker")
        if not t:
            continue
        tickers.append({
            "symbol": t,
            "market": _market_of(t),
            # quality_pass：v1 proxy for 總守則「質量四條件」= QGM-MLB 通過 ≥ 4/5。
            # 可在 universe.json 手動覆寫（§4.4 / §4.6）。
            "quality_pass": bool((s.get("pass_count") or 0) >= 4),
            "name": s.get("name") or t,
        })
    return {
        "schema_version": CFG.SCHEMA_VERSION,
        "seeded_from": "docs/dd-screener/latest.json",
        "quality_pass_rule": "QGM-MLB pass_count >= 4 (v1 proxy; overridable)",
        "tickers": tickers,
    }


# ── earnings ────────────────────────────────────────────────────────────────
def _fetch_earnings_one(dd_ticker: str) -> dict:
    """回傳 {dates: [ISO...]} 近 8 筆（含過去與未來）。失敗回 {dates: None}。"""
    try:
        df = yf.Ticker(_yf_ticker(dd_ticker)).get_earnings_dates(limit=8)
        if df is None or df.empty:
            return {"dates": None}
        dates = sorted({d.strftime("%Y-%m-%d") for d in df.index.to_pydatetime()})
        return {"dates": dates}
    except Exception:
        return {"dates": None}


def load_earnings(symbols: list[str], overrides: dict, as_of: str,
                  workers: int = 8) -> dict[str, dict]:
    """回傳 {symbol: {next, last, unknown}}。override 最高優先。快取 EARNINGS_REFRESH_DAYS。"""
    cache = _load_json(EARNINGS_CACHE, {})
    stale_or_missing = []
    for s in symbols:
        rec = cache.get(s)
        if not rec or not rec.get("fetched"):
            stale_or_missing.append(s)
            continue
        try:
            age = (datetime.strptime(as_of, "%Y-%m-%d")
                   - datetime.strptime(rec["fetched"], "%Y-%m-%d")).days
        except Exception:
            age = 999
        if age > EARNINGS_REFRESH_DAYS or rec.get("dates") is None:
            stale_or_missing.append(s)

    if stale_or_missing:
        print(f"  earnings: fetching {len(stale_or_missing)} (cache miss/stale) ...",
              file=sys.stderr)
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(_fetch_earnings_one, s): s for s in stale_or_missing}
            for fut in as_completed(futs):
                s = futs[fut]
                try:
                    r = fut.result()
                except Exception:
                    r = {"dates": None}
                cache[s] = {"dates": r["dates"], "fetched": as_of}
        try:
            _write_json(EARNINGS_CACHE, cache)
        except Exception:
            pass

    out: dict[str, dict] = {}
    for s in symbols:
        dates = None
        if s in overrides and overrides[s]:
            dates = [overrides[s]]                 # 手動覆寫即下次財報日
        else:
            dates = (cache.get(s) or {}).get("dates")
        if not dates:
            out[s] = {"next": None, "last": None, "unknown": True}
            continue
        future = [d for d in dates if d >= as_of]
        past = [d for d in dates if d < as_of]
        out[s] = {
            "next": future[0] if future else None,
            "last": past[-1] if past else None,
            "unknown": False,
        }
    return out


def _earnings_ctx(erec: dict, as_of: str, prev_bar_date) -> dict:
    """blackout（距下次財報 ≤ 5 交易日）+ is_first_day_after_earnings（§5/§4.6）。"""
    nxt = erec.get("next")
    last = erec.get("last")
    blackout = False
    if nxt:
        try:
            bdays = int(np.busday_count(as_of, nxt))   # [as_of, nxt) 的工作日數
            blackout = 0 <= bdays <= CFG.EARNINGS_BLACKOUT_DAYS
        except Exception:
            blackout = False
    first_after = False
    if last and prev_bar_date:
        # 財報日落在 (prev_bar_date, today] → 今日為財報後首個交易日
        first_after = (prev_bar_date < last <= as_of)
    return {
        "next_earnings": nxt,
        "earnings_blackout": blackout,
        "earnings_unknown": erec.get("unknown", False),
        "is_first_day_after_earnings": first_after,
    }


# ── public daily.json row（隱私：只 held 布林、無部位數字）─────────────────────
def _round(v, n=4):
    return round(v, n) if isinstance(v, (int, float)) else None


def _daily_row(symbol, held, res, ind, ectx) -> dict:
    m = res["mem"]
    return {
        "symbol": symbol,
        "held": bool(held),
        "state": res["state"],
        "state_since": m.get("state_since"),
        "action": res["action"],
        "flags": res["flags"],
        "entry_signal": res["entry_signal"],
        "metrics": {
            "close": _round(ind.get("close"), 2) if ind else None,
            "pct_vs_52w": _round(ind.get("pct_vs_52w")) if ind else None,
            "pct_vs_60d": _round(ind.get("pct_vs_60d")) if ind else None,
            "pct_vs_ath": _round(ind.get("pct_vs_ath")) if ind else None,
            "bb_position": _round(ind.get("bb_position"), 2) if ind else None,
            "volume_ratio": _round(ind.get("volume_ratio"), 2) if ind else None,
            "next_earnings": ectx.get("next_earnings"),
        },
        "notes": [f for f in res["flags"] if f in ("short_history", "earnings_unknown",
                                                    "data_error", "seed_init")],
    }


# ── main build ──────────────────────────────────────────────────────────────
def build(top_n=None, dry_run=False, as_of=None, workers=8) -> dict:
    now = datetime.now(TAIPEI_TZ)
    as_of = as_of or now.strftime("%Y-%m-%d")
    print(f"=== 五狀態機 run_daily · as_of={as_of} · {now.isoformat(timespec='seconds')} ===")

    universe = load_universe()
    if top_n:
        universe = universe[:top_n]
    symbols = [u["symbol"] for u in universe]
    qmap = {u["symbol"]: bool(u.get("quality_pass")) for u in universe}
    print(f"  universe: {len(symbols)} symbols  ({dict(Counter(_market_of(s) for s in symbols))})")

    positions = _load_json(CFG.POSITIONS_PATH, {})   # gitignored；缺省 = 全 watchlist
    held_set = _parse_held(positions)
    print(f"  positions: {len(held_set)} held (positions.json {'present' if CFG.POSITIONS_PATH.exists() else 'ABSENT → all watchlist'})")

    overrides = _load_json(CFG.EARNINGS_OVERRIDE_PATH, {})
    earnings = load_earnings(symbols, overrides if isinstance(overrides, dict) else {},
                             as_of, workers=workers)
    n_unknown = sum(1 for e in earnings.values() if e.get("unknown"))
    print(f"  earnings: {len(symbols)-n_unknown} known · {n_unknown} unknown")

    # 價格
    yf_map = {s: _yf_ticker(s) for s in symbols}
    prices = load_prices(sorted(set(yf_map.values())))
    print(f"  prices: {len(prices)} fetched/cached of {len(set(yf_map.values()))} yf tickers")

    # 記憶
    state_mem = _load_json(CFG.STATE_PATH, {})
    breakouts = _load_json(CFG.BREAKOUTS_PATH, {})
    seed_run = (len(state_mem) == 0)
    if seed_run:
        print("  state.json empty → FIRST RUN seed (§8.6: 保守初始化記憶旗標)")

    new_state_mem, new_breakouts = dict(state_mem), dict(breakouts)
    rows, changes = [], []
    error_streak_alerts = []
    ind_by_symbol: dict[str, dict] = {}

    for u in universe:
        s = u["symbol"]
        yf_t = yf_map[s]
        df = prices.get(yf_t)
        ind = compute_indicators(df) if df is not None else None
        ind_by_symbol[s] = ind
        ectx = _earnings_ctx(earnings.get(s, {}), as_of,
                             ind.get("prev_bar_date") if ind else None)
        ctx = {
            "held": s in held_set,
            "quality_pass": qmap.get(s, False),
            "today": as_of,
            "data_error": ind is None,
            "seed": seed_run,
            **ectx,
        }
        res = SM.evaluate(s, ind, state_mem.get(s), breakouts.get(s), ctx)
        new_state_mem[s] = res["mem"]
        if res["breakout"] is not None:
            new_breakouts[s] = res["breakout"]
        elif s in new_breakouts and res["breakout"] is None:
            pass
        if res["change"]:
            changes.append(res["change"])
        if res["mem"].get("data_error_streak", 0) >= CFG.DATA_ERROR_ALERT_STREAK:
            error_streak_alerts.append(s)
        rows.append(_daily_row(s, ctx["held"], res, ind, ectx))

    # run_type：US 樣本最後一根是否週五（多數）。複用已算好的 indicators。
    us_ind = [ind_by_symbol[s] for s in symbols if _market_of(s) == "US"]
    us_ind = [i for i in us_ind if i]
    fri_votes = sum(1 for i in us_ind if i.get("last_bar_is_friday"))
    run_type = "friday_weekly" if (us_ind and fri_votes > len(us_ind) / 2) else "daily"

    # frozen_week_of：取最常見的 frozen_week_date
    fw_counter = Counter(i["frozen_week_date"] for i in ind_by_symbol.values()
                         if i and i.get("frozen_week_date"))
    frozen_week_of = fw_counter.most_common(1)[0][0] if fw_counter else None

    # 排序：動作嚴重度 desc → 距 52 週線 asc（§7）
    def _sort_key(r):
        sev = CFG.ACTION_SEVERITY.get(r["action"], 0)
        if r["entry_signal"]:
            sev = max(sev, CFG.ACTION_SEVERITY.get(r["entry_signal"], 0))
        d52 = r["metrics"].get("pct_vs_52w")
        return (-sev, d52 if d52 is not None else 1e9, r["symbol"])
    rows.sort(key=_sort_key)

    state_dist = Counter(r["state"] for r in rows)
    action_dist = Counter(r["action"] for r in rows)
    print(f"  state dist: {dict(sorted(state_dist.items()))}")
    print(f"  action dist: {dict(action_dist)}")
    print(f"  changes today: {len(changes)} · run_type={run_type} · frozen_week_of={frozen_week_of}")
    if error_streak_alerts:
        print(f"  ⚠ data_error streak ≥{CFG.DATA_ERROR_ALERT_STREAK}: {error_streak_alerts}")

    daily = {
        "schema_version": CFG.SCHEMA_VERSION,
        "ruleset": CFG.RULESET_VERSION,
        "run_date": as_of,
        "run_timestamp": now.isoformat(timespec="seconds"),
        "run_type": run_type,
        "frozen_week_of": frozen_week_of,
        "universe_size": len(rows),
        "held_count": len(held_set),
        "summary": {
            "state_dist": {str(k): v for k, v in sorted(state_dist.items())},
            "action_dist": dict(action_dist),
            "earnings_unknown": n_unknown,
            "data_error_alerts": error_streak_alerts,
        },
        "config": {
            "BB_LEN_WEEKS": CFG.BB_LEN_WEEKS, "BB_DDOF": CFG.BB_DDOF,
            "VOLUME_SPIKE": CFG.VOLUME_SPIKE, "EARNINGS_BLACKOUT_DAYS": CFG.EARNINGS_BLACKOUT_DAYS,
            "RETEST_BAND": CFG.RETEST_BAND, "ATH_PROXIMITY": CFG.ATH_PROXIMITY,
            "MA_DAILY": CFG.MA_DAILY, "MA_W": list(CFG.MA_W),
        },
        "tickers": rows,
        "changes_today": changes,
    }

    if dry_run:
        print("  (dry-run) 不寫檔")
    else:
        _write_json(CFG.DAILY_PATH, daily)
        _write_json(CFG.STATE_PATH, new_state_mem)
        _write_json(CFG.BREAKOUTS_PATH, new_breakouts)
        if not CFG.EARNINGS_OVERRIDE_PATH.exists():
            _write_json(CFG.EARNINGS_OVERRIDE_PATH, {})
        print(f"  ✓ wrote daily.json ({len(rows)} rows) · state.json · breakouts.json")
    return daily


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top", type=int, default=None)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--as-of", type=str, default=None, help="YYYY-MM-DD 判定日（測試/回放）")
    p.add_argument("--workers", type=int, default=8)
    args = p.parse_args()
    build(top_n=args.top, dry_run=args.dry_run, as_of=args.as_of, workers=args.workers)


if __name__ == "__main__":
    main()
