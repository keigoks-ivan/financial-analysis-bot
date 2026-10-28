#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主動式 ETF「本站挑選」的事前登記追蹤——讀 data/active_etf/picks.json（picks-registry-v2：
登記清單，只能 append，每筆有登記日、兩檔挑選、文字、查核點定義，登記後不改），
data/active_etf/picks_reviews.json（月評，沒有檔案視為空）。每筆登記每天算：

  1. 登記日收盤起算的含息累計報酬（兩檔、兩檔各半、0050），用 prices.jsonl
     的收盤價 × 除息日的還原係數（1 + 配息 ÷ 前一日收盤）。
  2. 登記後最大回檔。
  3. 各查核點的現值與是否觸發（全部機械判定，資料來自 build_active_etf.py 剛
     算好的 22 檔 JSON 與 prices.jsonl）。

輸出 docs/active-etf/data/picks_track.json（schema picks-track-v2，最新登記在前），
頁面總覽最上面那一區讀它。結算日（settle_on）已過的登記，數字截在結算日並凍結：
第一次算到 settled 後，之後直接沿用上一次輸出的數字與查核點，只更新月評。
配息來自 yfinance Ticker.dividends，快取在 data/active_etf/picks_dividends.json，
各登記共用，抓的起始日＝最早一筆未結算登記的登記日；抓不到就沿用快取，不讓整個
build 掛掉。

可單獨跑（用現有快取，不抓股價）：python3 scripts/active_etf/picks.py
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "etf_dash"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "active_etf"))

import build_etf_dash as etfdash  # noqa: E402 — 只借 yf_call_with_backoff()
import prices as pr  # noqa: E402

PICKS_PATH = REPO_ROOT / "data" / "active_etf" / "picks.json"
REVIEWS_PATH = REPO_ROOT / "data" / "active_etf" / "picks_reviews.json"
DIVIDENDS_CACHE_PATH = REPO_ROOT / "data" / "active_etf" / "picks_dividends.json"
FUND_DATA_DIR = REPO_ROOT / "docs" / "active-etf" / "data"
OUT_PATH = FUND_DATA_DIR / "picks_track.json"


# ── 配息 ──────────────────────────────────────────────────────────────────
def load_dividend_cache() -> dict:
    if not DIVIDENDS_CACHE_PATH.exists():
        return {}
    try:
        return json.loads(DIVIDENDS_CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def fetch_dividends(tickers: list[str], since: str) -> tuple[dict, list[str]]:
    """回傳 {ticker: {ex_date: cash}}（只留 since 當天以後的除息日）與錯誤清單。
    抓失敗的代號沿用快取。"""
    import yfinance as yf  # 延後 import：單獨跑 --no-fetch 時不需要

    cache = load_dividend_cache()
    out, errors = {}, []
    for tk in tickers:
        # since 之前的除息日沿用快取（較早、已結算的登記還要用）；since 以後的重抓
        older = {d: v for d, v in (cache.get(tk) or {}).items() if d < since}
        try:
            s = etfdash.yf_call_with_backoff(lambda: yf.Ticker(tk).dividends, label=f"dividends {tk}")
            rows = dict(older)
            for idx, v in s.items():
                d = idx.strftime("%Y-%m-%d")
                if d >= since and v and float(v) > 0:
                    rows[d] = round(float(v), 4)
            out[tk] = dict(sorted(rows.items()))
        except Exception as e:  # noqa: BLE001
            errors.append(f"{tk}: {e}")
            out[tk] = cache.get(tk, {})
    for tk, rows in cache.items():  # 這次沒抓的代號（舊登記的挑選）原樣保留
        out.setdefault(tk, rows)
    try:
        DIVIDENDS_CACHE_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass
    return out, errors


# ── 含息報酬 ───────────────────────────────────────────────────────────────
def close_series(history: dict, ticker: str, end_date: str | None = None) -> list[tuple[str, float]]:
    out = []
    for d in sorted(history):
        if end_date is not None and d > end_date:
            break
        v = (history[d].get("close") or {}).get(ticker)
        if v is not None:
            out.append((d, float(v)))
    return out


def total_return_index(series: list[tuple[str, float]], dividends: dict, base_date: str) -> list[dict]:
    """從 base_date 那天收盤＝1.0 起算的含息指數。除息日 d 的還原係數＝
    1 + 配息 ÷ 前一交易日收盤；累乘後乘上 close_d ÷ close_base。"""
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
def holdings_overlap_pct(a: dict, b: dict) -> float | None:
    wa = {h["ticker"]: float(h.get("weight_pct") or 0) for h in (a.get("holdings") or [])}
    wb = {h["ticker"]: float(h.get("weight_pct") or 0) for h in (b.get("holdings") or [])}
    if not wa or not wb:
        return None
    return round(sum(min(wa.get(t, 0), wb.get(t, 0)) for t in set(wa) | set(wb)), 2)


def evaluate_checkpoints(picks: dict, funds_by_code: dict, tracks: dict, bench_track: list[dict],
                         bench_code: str = "0050") -> list[dict]:
    out = []
    for cp in picks.get("checkpoints") or []:
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
        elif kind == "aum_drop":
            f = funds_by_code.get(cp["code"]) or {}
            aum = (f.get("twse_aum") or {}).get("aum_100m_twd")
            row["current"] = aum
            if aum is not None:
                chg = (aum / cp["base"] - 1) * 100
                row["current_label"] = f"{aum:,.0f} 億（{chg:+.1f}%）"
                row["triggered"] = chg <= -cp["drop_pct"]
        elif kind == "top10":
            f = funds_by_code.get(cp["code"]) or {}
            v = f.get("top10_concentration_pct")
            row["current"] = v
            if v is not None:
                row["current_label"] = f"{v:.1f}%"
                row["triggered"] = v > cp["max"]
        elif kind == "overlap":
            codes = [p["code"] for p in picks["picks"]]
            v = holdings_overlap_pct(funds_by_code.get(codes[0]) or {}, funds_by_code.get(codes[1]) or {})
            row["current"] = v
            if v is not None:
                row["current_label"] = f"{v:.1f}%"
                row["triggered"] = v > cp["max"]
        elif kind == "mdd_ratio":
            fund_mdd = max_drawdown(tracks.get(cp["code"], []))
            bench_mdd = max_drawdown(bench_track)
            if fund_mdd is not None and bench_mdd is not None:
                row["current_label"] = f"{cp['code']} {fund_mdd:.1f}%，{bench_code} {bench_mdd:.1f}%"
                armed = bench_mdd <= cp["bench_min_mdd_pct"]
                row["triggered"] = armed and bench_mdd < 0 and (fund_mdd / bench_mdd) >= cp["ratio"]
                if not armed:
                    row["current_label"] += f"（{bench_code} 回檔未達 {abs(cp['bench_min_mdd_pct']):g}%，尚未開始檢驗）"
        if row["current_label"] is None:
            row["current_label"] = "無資料"
            row["status"] = "no_data"
        elif row["triggered"]:
            row["status"] = "triggered"
        out.append(row)
    return out


# ── 主流程 ─────────────────────────────────────────────────────────────────
def load_registry() -> dict:
    reg = json.loads(PICKS_PATH.read_text(encoding="utf-8"))
    if reg.get("schema") != "picks-registry-v2":
        raise ValueError(f"{PICKS_PATH} schema 不是 picks-registry-v2：{reg.get('schema')}")
    return reg


def load_reviews() -> dict[str, list[dict]]:
    """{reg_id: [review…]}，依 as_of 升冪。檔案不存在或壞掉視為空。"""
    if not REVIEWS_PATH.exists():
        return {}
    try:
        data = json.loads(REVIEWS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out: dict[str, list[dict]] = {}
    for r in data.get("reviews") or []:
        out.setdefault(r.get("reg_id"), []).append(r)
    for rid in out:
        out[rid].sort(key=lambda r: r.get("as_of") or "")
    return out


def load_prior_track() -> dict[str, dict]:
    if not OUT_PATH.exists():
        return {}
    try:
        data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if data.get("schema") != "picks-track-v2":
        return {}
    return {r["id"]: r for r in data.get("registrations") or []}


def _row_for(label, code, rows, dividend_map, base_date, bench_by_date):
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


def track_registration(reg: dict, bench: str, bench_name: str, price_history: dict, dividends: dict,
                       funds_by_code: dict, settled: bool) -> dict:
    """算一筆登記的追蹤數字與查核點。settled 時所有數字截在 settle_on 當天。"""
    registered_on = reg["registered_on"]
    end_date = reg["settle_on"] if settled else None
    bench_code = bench[:-3] if bench.endswith(".TW") else bench
    pick_codes = [p["code"] for p in reg["picks"]]
    tickers = [c + ".TW" for c in pick_codes] + [bench]

    series = {tk: close_series(price_history, tk, end_date) for tk in tickers}
    # 起算日＝登記日當天或之後、三檔都有收盤價的第一個交易日
    candidates = None
    for tk in tickers:
        ds = {d for d, _ in series[tk] if d >= registered_on}
        candidates = ds if candidates is None else candidates & ds
    base_date = min(candidates) if candidates else None

    out = {
        "id": reg["id"], "kind": reg["kind"], "registered_on": registered_on, "settle_on": reg["settle_on"],
        "written_by": reg.get("written_by"), "evidence_as_of": reg.get("evidence_as_of"),
        "picks": reg["picks"], "frozen": reg["frozen"], "text": reg.get("text"), "note": reg.get("note"),
        "status": "pending" if base_date is None else ("settled" if settled else "tracking"),
        "base_date": base_date, "as_of": None, "rows": [], "series": {}, "checkpoints": [], "reviews": [],
    }

    tracks, bench_track = {}, []
    if base_date is not None:
        bench_track = total_return_index(series[bench], dividends.get(bench, {}), base_date)
        for c in pick_codes:
            tracks[c] = total_return_index(series[c + ".TW"], dividends.get(c + ".TW", {}), base_date)
        out["as_of"] = bench_track[-1]["date"] if bench_track else base_date
        bench_by_date = {r["date"]: r["tr"] for r in bench_track}

        for p in reg["picks"]:
            out["rows"].append(_row_for(p["name"], p["code"], tracks[p["code"]],
                                        dividends.get(p["code"] + ".TW", {}), base_date, bench_by_date))
        # 兩檔各半、登記日買進後不再平衡＝兩條含息指數的平均
        if all(tracks[c] for c in pick_codes):
            by_date = [{r["date"]: r["tr"] for r in tracks[c]} for c in pick_codes]
            common = sorted(set(by_date[0]) & set(by_date[1]))
            ew = [{"date": d, "close": None, "tr": sum(m[d] for m in by_date) / len(by_date)} for d in common]
            r = _row_for("兩檔各半", "EW", ew, {}, base_date, bench_by_date)
            r["base_close"] = r["last_close"] = None
            r["dividends_sum"] = None
            out["rows"].append(r)
        rb = _row_for(bench_name, bench_code, bench_track, dividends.get(bench, {}), base_date, bench_by_date)
        rb["rel_bench_pp"] = None
        out["rows"].append(rb)
        out["series"] = {c: [{"date": r["date"], "tr": round(r["tr"], 5)} for r in tracks[c]] for c in pick_codes}
        out["series"][bench_code] = [{"date": r["date"], "tr": round(r["tr"], 5)} for r in bench_track]

    out["checkpoints"] = evaluate_checkpoints(reg, funds_by_code, tracks, bench_track, bench_code)
    return out


def build_picks_track(fund_results: list[dict] | None, price_history: dict | None, fetch: bool = True,
                      registered_on_override: str | None = None) -> dict:
    registry = load_registry()
    bench = registry["benchmark"]
    bench_name = registry.get("benchmark_name") or bench
    regs = sorted(registry["registrations"], key=lambda r: r["registered_on"])  # 舊→新
    if registered_on_override and regs:  # 測試用：只對最新一筆生效
        regs[-1] = dict(regs[-1], registered_on=registered_on_override)

    if price_history is None:
        price_history = pr.load_price_history()
    latest_date = max((d for d in price_history if (price_history[d].get("close") or {}).get(bench) is not None),
                      default=None)
    settled_ids = {r["id"] for r in regs if latest_date is not None and latest_date >= r["settle_on"]}
    prior = load_prior_track()

    funds_by_code = {f["code"]: f for f in (fund_results or [])}
    for r in regs:
        for p in r["picks"]:
            if p["code"] not in funds_by_code:
                fp = FUND_DATA_DIR / f"{p['code']}.json"
                if fp.exists():
                    funds_by_code[p["code"]] = json.loads(fp.read_text(encoding="utf-8"))

    # 配息：各登記共用一份快取，抓的起始日＝最早一筆未結算登記的登記日
    active = [r for r in regs if r["id"] not in settled_ids]
    div_errors: list[str] = []
    if fetch and active:
        since = min(r["registered_on"] for r in active)
        tickers = sorted({p["code"] + ".TW" for r in active for p in r["picks"]} | {bench})
        dividends, div_errors = fetch_dividends(tickers, since)
    else:
        dividends = load_dividend_cache()

    reviews = load_reviews()
    out_regs = []
    for r in regs:
        settled = r["id"] in settled_ids
        prev = prior.get(r["id"])
        if settled and prev and prev.get("status") == "settled" and not registered_on_override:
            # 結算後凍結：數字與查核點沿用上一次輸出，只換回登記檔的文字欄位與月評
            entry = dict(prev)
            entry.update({"kind": r["kind"], "registered_on": r["registered_on"], "settle_on": r["settle_on"],
                          "written_by": r.get("written_by"), "evidence_as_of": r.get("evidence_as_of"),
                          "picks": r["picks"], "frozen": r["frozen"], "text": r.get("text"),
                          "note": registry.get("note")})
        else:
            entry = track_registration(r, bench, bench_name, price_history, dividends, funds_by_code, settled)
            entry["note"] = registry.get("note")
        entry["reviews"] = reviews.get(r["id"], [])
        out_regs.append(entry)
    out_regs.sort(key=lambda e: e["registered_on"], reverse=True)  # 最新在前

    latest = out_regs[0] if out_regs else {}
    return {
        "schema": "picks-track-v2", "benchmark": bench, "benchmark_name": bench_name,
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        # 最新一筆的摘要：給 build_active_etf.py 的 log 行用（它讀頂層 status／base_date／as_of）
        "status": latest.get("status"), "base_date": latest.get("base_date"), "as_of": latest.get("as_of"),
        "registrations": out_regs,
        "dividends": dividends, "dividend_fetch_errors": div_errors,
    }


def write_picks_track(fund_results=None, price_history=None, fetch=True, registered_on_override=None) -> dict:
    out = build_picks_track(fund_results, price_history, fetch=fetch, registered_on_override=registered_on_override)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-fetch", action="store_true", help="不抓配息，用快取")
    ap.add_argument("--registered-on", help="測試用：暫時改最新一筆登記的登記日看計算路徑（不寫回 picks.json）")
    ap.add_argument("--dry-run", action="store_true", help="只印結果不寫檔")
    args = ap.parse_args()
    if args.dry_run:
        out = build_picks_track(None, None, fetch=not args.no_fetch, registered_on_override=args.registered_on)
    else:
        out = write_picks_track(fetch=not args.no_fetch, registered_on_override=args.registered_on)
    for reg in out["registrations"]:
        print("[{}] {} status={} base_date={} as_of={} reviews={}".format(
            reg["id"], reg["kind"], reg["status"], reg["base_date"], reg["as_of"], len(reg["reviews"])))
        for r in reg["rows"]:
            print("  {:<14} tr={} rel={} mdd={} div={}".format(r["label"], r.get("tr_pct"), r.get("rel_bench_pp"),
                                                               r.get("mdd_pct"), r.get("dividends_sum")))
        for c in reg["checkpoints"]:
            print("  {} {:<12} {}".format(c["id"], c["status"], c["current_label"]))
    if out["dividend_fetch_errors"]:
        print("dividend fetch errors:", out["dividend_fetch_errors"], file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
