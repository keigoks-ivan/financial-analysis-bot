#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETF 儀表板「本站挑選」的事前登記追蹤——讀 data/etf_dash/picks.json（登記日、
兩檔挑選、查核點定義，手寫、登記後不改），每天算：

  1. 登記日收盤起算的美元含息累計報酬（兩檔、兩檔各半、SPY）。收盤與配息
     一起用 yfinance Ticker.history(auto_adjust=False) 抓登記日以後的日線，
     快取在 data/etf_dash/picks_prices.json；抓不到就沿用快取，不讓整個 build
     掛掉。含息＝收盤 × 除息日還原係數（1 + 配息 ÷ 前一日收盤）累乘。
  2. 登記後最大回檔。
  3. 各查核點的現值與是否觸發（全部機械判定，資料來自 build_etf_dash.py 剛寫
     好的各基金 JSON 與 data/etf_dash/flows/）。

輸出 docs/etf-dash/data/picks_track.json，總覽頁最上面那一區讀它。
做法與 scripts/active_etf/picks.py 相同；含息指數、回檔、連續落後三個函式
是從那裡複製的（兩邊模組都叫 picks，不互相 import）。

可單獨跑：python3 scripts/etf_dash/picks_track.py [--no-fetch] [--registered-on YYYY-MM-DD] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_etf_dash as etfdash  # noqa: E402 — 只借 yf_call_with_backoff()

REPO_ROOT = Path(__file__).resolve().parents[2]
PICKS_PATH = REPO_ROOT / "data" / "etf_dash" / "picks.json"
PRICES_CACHE_PATH = REPO_ROOT / "data" / "etf_dash" / "picks_prices.json"
FLOWS_DIR = REPO_ROOT / "data" / "etf_dash" / "flows"
FUND_DATA_DIR = REPO_ROOT / "docs" / "etf-dash" / "data"
OUT_PATH = FUND_DATA_DIR / "picks_track.json"


# ── 收盤與配息 ─────────────────────────────────────────────────────────────
def load_prices_cache() -> dict:
    if not PRICES_CACHE_PATH.exists():
        return {}
    try:
        return json.loads(PRICES_CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def fetch_prices(tickers: list[str], since: str) -> tuple[dict, list[str]]:
    """回傳 {ticker: {"close": {date: close}, "dividends": {date: cash}}} 與錯誤清單。
    新抓到的日期覆蓋快取同一天的值（盤中跑到的半根 K 棒會被下次修正），抓失敗
    的代號整檔沿用快取。只留 since 當天以後。"""
    import pandas as pd  # 延後 import：--no-fetch 不需要
    import yfinance as yf

    cache = load_prices_cache()
    out, errors = {}, []
    for tk in tickers:
        base = {"close": dict((cache.get(tk) or {}).get("close") or {}),
                "dividends": dict((cache.get(tk) or {}).get("dividends") or {})}
        try:
            hist = etfdash.yf_call_with_backoff(
                lambda: yf.Ticker(tk).history(start=since, auto_adjust=False), label=f"picks {tk}")
            if hist is None or hist.empty:
                raise RuntimeError("empty history")
            for idx, r in hist.iterrows():
                d = idx.strftime("%Y-%m-%d")
                if d < since:
                    continue
                if not pd.isna(r["Close"]):
                    base["close"][d] = round(float(r["Close"]), 4)
                div = r.get("Dividends")
                if div is not None and not pd.isna(div) and float(div) > 0:
                    base["dividends"][d] = round(float(div), 4)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{tk}: {e}")
        out[tk] = base
    try:
        PRICES_CACHE_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass
    return out, errors


def close_series(prices: dict, ticker: str) -> list[tuple[str, float]]:
    closes = (prices.get(ticker) or {}).get("close") or {}
    return [(d, float(closes[d])) for d in sorted(closes)]


# ── 含息報酬（與 scripts/active_etf/picks.py 相同） ───────────────────────────
def total_return_index(series: list[tuple[str, float]], dividends: dict, base_date: str) -> list[dict]:
    rows = [(d, c) for d, c in series if d >= base_date]
    if not rows:
        return []
    base_close = rows[0][1]
    factor = 1.0
    prev_close = base_close
    out = []
    for d, c in rows:
        if d != base_date and d in dividends and prev_close > 0:
            factor *= 1.0 + dividends[d] / prev_close
        out.append({"date": d, "close": c, "tr": c / base_close * factor})
        prev_close = c
    return out


def max_drawdown(tr_rows: list[dict]) -> float | None:
    if not tr_rows:
        return None
    peak, mdd = -1.0, 0.0
    for r in tr_rows:
        peak = max(peak, r["tr"])
        mdd = min(mdd, r["tr"] / peak - 1.0)
    return round(mdd * 100, 2)


def consecutive_days_behind(fund_rows: list[dict], bench_rows: list[dict]) -> int:
    bench = {r["date"]: r["tr"] for r in bench_rows}
    n = 0
    for r in reversed(fund_rows):
        b = bench.get(r["date"])
        if b is None:
            continue
        if r["tr"] < b:
            n += 1
        else:
            break
    return n


# ── 查核點 ─────────────────────────────────────────────────────────────────
def latest_aum_usd(etf_key: str) -> float | None:
    """data/etf_dash/flows/{ETF}.jsonl 最後一行的 股數 × 淨值（美元）。"""
    p = FLOWS_DIR / f"{etf_key}.jsonl"
    if not p.exists():
        return None
    last = None
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            last = line
    if not last:
        return None
    try:
        row = json.loads(last)
        if row.get("nav_currency") != "USD" or not row.get("shares_outstanding") or not row.get("nav"):
            return None
        return float(row["shares_outstanding"]) * float(row["nav"])
    except (ValueError, TypeError):
        return None


def flow_1m_net(fund: dict) -> float | None:
    """近 30 個曆日淨申贖（美元），以最新快照日為基準，同 build_etf_dash._flow_amount_since()。"""
    f = fund.get("flows") or {}
    if f.get("skipped") or not f.get("daily"):
        return None
    latest = f.get("latest_date") or f["daily"][-1]["date"]
    cutoff = (datetime.date.fromisoformat(latest) - datetime.timedelta(days=30)).isoformat()
    return round(sum(d["flow_amount"] for d in f["daily"] if d["date"] > cutoff), 2)


def evaluate_checkpoints(picks: dict, funds_by_code: dict, tracks: dict, bench_track: list[dict]) -> list[dict]:
    bench = picks["benchmark"]
    out = []
    for cp in picks["checkpoints"]:
        kind = cp["kind"]
        row = {"id": cp["id"], "text": cp["text"], "consequence": cp["consequence"], "kind": kind,
               "current": None, "current_label": None, "triggered": False, "status": "untriggered"}
        if kind == "lag":
            parts, trig = [], False
            for p in picks["picks"]:
                n = consecutive_days_behind(tracks.get(p["code"], []), bench_track)
                parts.append(f"{p['code']} 連續落後 {n} 天")
                trig = trig or n >= cp["days"]
            row["current_label"] = "；".join(parts) + f"（門檻 {cp['days']} 天）"
            row["triggered"] = trig
        elif kind == "rev_3m":
            parts, trig, any_data = [], False, False
            for p in picks["picks"]:
                f = funds_by_code.get(p["code"]) or {}
                v = ((f.get("forward_summary") or {}).get("fy1") or {}).get("rev_3m_pct")
                if v is None:
                    parts.append(f"{p['code']} 無資料")
                    continue
                any_data = True
                parts.append(f"{p['code']} {v:+.1f}%")
                trig = trig or v < cp["min"]
            if any_data:
                row["current_label"] = "；".join(parts)
                row["triggered"] = trig
        elif kind == "pe_max":
            parts, trig, any_data = [], False, False
            for p in picks["picks"]:
                f = funds_by_code.get(p["code"]) or {}
                v = (f.get("weighted_forward_pe") or {}).get("value")
                if v is None:
                    parts.append(f"{p['code']} 無資料")
                    continue
                any_data = True
                parts.append(f"{p['code']} {v:.1f} 倍")
                trig = trig or v > cp["max"][p["code"]]
            if any_data:
                row["current_label"] = "；".join(parts)
                row["triggered"] = trig
        elif kind == "breadth":
            f = funds_by_code.get(cp["code"]) or {}
            v = ((f.get("breadth") or {}).get("90d") or {}).get("up_weight_pct")
            row["current"] = v
            if v is not None:
                row["current_label"] = f"{v:.1f}%"
                row["triggered"] = v < cp["min"]
        elif kind == "outflow":
            f = funds_by_code.get(cp["code"]) or {}
            net = flow_1m_net(f)
            aum = latest_aum_usd(cp["code"])
            if net is not None and aum:
                pct = net / aum * 100
                row["current"] = round(pct, 2)
                row["current_label"] = f"近一月淨{'流入' if net >= 0 else '流出'} {abs(net) / 1e8:.1f} 億美元（規模 {aum / 1e9:.0f} 億美元的 {pct:+.1f}%）"
                row["triggered"] = pct <= -cp["pct"]
        elif kind == "mdd_ratio":
            fund_mdd = max_drawdown(tracks.get(cp["code"], []))
            bench_mdd = max_drawdown(bench_track)
            if fund_mdd is not None and bench_mdd is not None:
                row["current_label"] = f"{cp['code']} {fund_mdd:.1f}%，{bench} {bench_mdd:.1f}%"
                armed = bench_mdd <= cp["bench_min_mdd_pct"]
                row["triggered"] = armed and bench_mdd < 0 and (fund_mdd / bench_mdd) >= cp["ratio"]
                if not armed:
                    row["current_label"] += f"（{bench} 回檔未達 {abs(cp['bench_min_mdd_pct']):.0f}%，尚未開始檢驗）"
        if row["current_label"] is None:
            row["current_label"] = "無資料"
            row["status"] = "no_data"
        elif row["triggered"]:
            row["status"] = "triggered"
        out.append(row)
    return out


# ── 主流程 ─────────────────────────────────────────────────────────────────
def build_picks_track(fetch: bool = True, registered_on_override: str | None = None) -> dict:
    picks = json.loads(PICKS_PATH.read_text(encoding="utf-8"))
    registered_on = registered_on_override or picks["registered_on"]
    bench = picks["benchmark"]
    pick_codes = [p["code"] for p in picks["picks"]]
    ticker_of = {p["code"]: p.get("yf_ticker") or p["code"] for p in picks["picks"]}
    ticker_of[bench] = bench
    tickers = [ticker_of[c] for c in pick_codes] + [bench]

    funds_by_code = {}
    for c in pick_codes:
        p = FUND_DATA_DIR / f"{c}.json"
        if p.exists():
            funds_by_code[c] = json.loads(p.read_text(encoding="utf-8"))

    if fetch:
        prices, fetch_errors = fetch_prices(tickers, registered_on)
    else:
        prices, fetch_errors = load_prices_cache(), []

    series = {tk: close_series(prices, tk) for tk in tickers}
    # 起算日＝登記日當天或之後、三檔都有收盤價的第一個交易日
    candidates = None
    for tk in tickers:
        ds = {d for d, _ in series[tk] if d >= registered_on}
        candidates = ds if candidates is None else candidates & ds
    base_date = min(candidates) if candidates else None

    dividends = {tk: (prices.get(tk) or {}).get("dividends") or {} for tk in tickers}
    out = {
        "registered_on": picks["registered_on"], "settle_on": picks["settle_on"],
        "benchmark": bench, "benchmark_name": picks.get("benchmark_name", bench),
        "picks": picks["picks"], "frozen": picks["frozen"], "note": picks.get("note"),
        "base_date": base_date, "as_of": None, "status": "pending" if base_date is None else "tracking",
        "rows": [], "series": {}, "checkpoints": [],
        "dividends": dividends, "fetch_errors": fetch_errors,
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    tracks, bench_track = {}, []
    if base_date is not None:
        bench_track = total_return_index(series[bench], dividends[bench], base_date)
        for c in pick_codes:
            tracks[c] = total_return_index(series[ticker_of[c]], dividends[ticker_of[c]], base_date)
        out["as_of"] = bench_track[-1]["date"] if bench_track else base_date
        bench_by_date = {r["date"]: r["tr"] for r in bench_track}

        def row_for(label, code, rows, dividend_map):
            if not rows:
                return {"label": label, "code": code, "no_data": True}
            last = rows[-1]
            b = bench_by_date.get(last["date"])
            return {
                "label": label, "code": code, "base_close": rows[0]["close"], "last_close": last["close"],
                "last_date": last["date"], "tr_pct": round((last["tr"] - 1) * 100, 2),
                "rel_bench_pp": round((last["tr"] - b) * 100, 2) if b is not None else None,
                "mdd_pct": max_drawdown(rows),
                "dividends_sum": round(sum(v for d, v in dividend_map.items() if base_date < d <= last["date"]), 4),
                "n_days": len(rows) - 1,
            }

        for p in picks["picks"]:
            out["rows"].append(row_for(p["name"], p["code"], tracks[p["code"]], dividends[ticker_of[p["code"]]]))
        # 兩檔各半、登記日買進後不再平衡＝兩條含息指數的平均
        if all(tracks[c] for c in pick_codes):
            by_date = [{r["date"]: r["tr"] for r in tracks[c]} for c in pick_codes]
            common = sorted(set(by_date[0]) & set(by_date[1]))
            ew = [{"date": d, "close": None, "tr": sum(m[d] for m in by_date) / len(by_date)} for d in common]
            r = row_for("兩檔各半", "EW", ew, {})
            r["base_close"] = r["last_close"] = None
            r["dividends_sum"] = None
            out["rows"].append(r)
        rb = row_for(out["benchmark_name"], bench, bench_track, dividends[bench])
        rb["rel_bench_pp"] = None
        out["rows"].append(rb)
        out["series"] = {c: [{"date": r["date"], "tr": round(r["tr"], 5)} for r in tracks[c]] for c in pick_codes}
        out["series"][bench] = [{"date": r["date"], "tr": round(r["tr"], 5)} for r in bench_track]

    out["checkpoints"] = evaluate_checkpoints(picks, funds_by_code, tracks, bench_track)
    return out


def write_picks_track(fetch: bool = True, registered_on_override: str | None = None) -> dict:
    out = build_picks_track(fetch=fetch, registered_on_override=registered_on_override)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-fetch", action="store_true", help="不抓收盤與配息，用快取")
    ap.add_argument("--registered-on", help="測試用：暫時改登記日看計算路徑（不寫回 picks.json）")
    ap.add_argument("--dry-run", action="store_true", help="只印結果不寫檔")
    args = ap.parse_args()
    if args.dry_run:
        out = build_picks_track(fetch=not args.no_fetch, registered_on_override=args.registered_on)
    else:
        out = write_picks_track(fetch=not args.no_fetch, registered_on_override=args.registered_on)
    print("status={} base_date={} as_of={}".format(out["status"], out["base_date"], out["as_of"]))
    for r in out["rows"]:
        print("  {:<16} tr={} rel={} mdd={} div={}".format(r["label"], r.get("tr_pct"), r.get("rel_bench_pp"),
                                                           r.get("mdd_pct"), r.get("dividends_sum")))
    for c in out["checkpoints"]:
        print("  {} {:<12} {}".format(c["id"], c["status"], c["current_label"]))
    if out["fetch_errors"]:
        print("fetch errors:", out["fetch_errors"], file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
