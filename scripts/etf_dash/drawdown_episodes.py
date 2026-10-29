#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETF 儀表板「基準回檔情境表」資料：SPY 每一次回檔 10% 以上時，21 檔各跌多少、反彈多少。

頁面 docs/etf-dash/drawdowns.html 讀這支產出的 docs/etf-dash/data/drawdowns.json。

口徑（與 2026-10-28 深度檢驗一致）：
  - 基準 SPY，含息還原收盤；起點 1999-01-01，前高從這一天起算（running max）。
  - 回檔區段：SPY 由前高跌到谷底 ≥ 10%。峰＝跌破前高前最後一次創高的日子；
    谷＝峰到回前高之間最低的一天（取最深）；回前高日＝第一天收盤 ≥ 峰值。
  - 各檔：同一個峰日到谷日的跌幅（點對點，不是各檔自己的最大回檔）、相對 SPY 的差
    （個百分點，正數＝比 SPY 少跌）、谷到 SPY 回前高日的反彈、峰到 SPY 回前高日的整段報酬。
    還沒回前高的區段以最新一天代替回前高日。
  - 台幣（0050、TAIEX）、日圓（TOPIX＝1475.T）資產除以當日匯率（TWD=X、JPY=X）換美元，
    再對齊 SPY 交易日（當地休市日用前一日收盤）。TAIEX 是價格指數，不含息。
  - 彙總只算已回前高的區段；進行中的區段回前高後自動計入。
  - SPY 離前高 ≥ 5% 但還沒到 10%：標「觀察中」，列各檔從同一峰日起的跌幅；
    到 10% 即成為正式一列，標「進行中」。

資料來源：
  --source yfinance（預設，雲端 CI）：yfinance Ticker.history(period="max", auto_adjust=True)。
  --source price_store（本機驗證）：~/v7-backtest/src/price_store.py 的 get_prices（共用正本，
    不另存檔）。

可單獨跑：python3 scripts/etf_dash/drawdown_episodes.py [--source price_store] [--no-write]
抓價失敗（SPY 抓不到）時 exit 1、不覆蓋舊 JSON；單一基金抓不到只把該檔留空並寫進 notes。
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_common import RESEARCH_UNIVERSE  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
FUND_DATA_DIR = REPO_ROOT / "docs" / "etf-dash" / "data"
OUT_PATH = FUND_DATA_DIR / "drawdowns.json"
SCHEMA = "etf-dash-drawdowns-v1"

BENCH = "SPY"
START = "1999-01-01"
EPISODE_THRESHOLD = 0.10        # 正式區段：峰到谷 ≥ 10%
WATCH_THRESHOLD = 0.05          # 觀察中：離前高 ≥ 5%
SUMMARY_THRESHOLDS = (10, 15, 20)
TEN_YEARS = 10

FX_TICKER = {"TWD": "TWD=X", "JPY": "JPY=X"}

# 1475.T（TOPIX）Yahoo 資料的兩個已知問題：
#  1. 2024-08-08、2024-08-09 收盤少一位數（25.23、25.51，前後約 254～261），整天剔除。
#  2. Yahoo 還原係數在 2024-08-09 一次跳 16.1%（其餘半年配息的跳動中位數約 1.0%），判斷是壞的配息記錄。
#     修正法：2024-08-09 以前的還原價乘 1.1496（＝1.1611 ÷ 1.0099，估計值，讓該次配息只跳中位數）。
#     只有偵測到還原係數在該日仍跳 10% 以上才套用；Yahoo 若已修好資料就不動。
TOPIX_TICKER = "1475.T"
TOPIX_BAD_DATES = ("2024-08-08", "2024-08-09")
TOPIX_FIX_BEFORE = "2024-08-09"
TOPIX_FIX_FACTOR = 1.1496       # 估計值，見上
TOPIX_FIX_DETECT = 1.10         # 還原係數單日跳動超過這個才視為仍是壞記錄


# ── 基金清單 ─────────────────────────────────────────────────────────────
def fund_list() -> list[dict]:
    ov = json.loads((FUND_DATA_DIR / "overview.json").read_text(encoding="utf-8"))
    out = []
    for f in ov["funds"]:
        k = f["etf_key"]
        if k not in RESEARCH_UNIVERSE:  # 2026-10-29 總覽加 XLU、XLRE，回檔表母體維持原 21 檔
            continue
        tk = f.get("yf_ticker")
        if not tk:
            try:
                tk = json.loads((FUND_DATA_DIR / f"{k}.json").read_text(encoding="utf-8")).get("yf_ticker")
            except (OSError, ValueError):
                tk = None
        cur = "TWD" if tk and (tk.endswith(".TW") or tk == "^TWII") else "JPY" if tk and tk.endswith(".T") else "USD"
        out.append({"key": k, "yf_ticker": tk, "currency": cur, "label_zh": f.get("label_zh")})
    return out


# ── 價格 ─────────────────────────────────────────────────────────────────
def _naive(idx):
    import pandas as pd
    idx = pd.DatetimeIndex(idx)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    return idx.normalize()


def last_closed_date() -> datetime.date:
    """紐約 16:30 前，今天的 K 棒算盤中，不用。"""
    from zoneinfo import ZoneInfo
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(ZoneInfo("America/New_York"))
    d = now.date()
    if now.hour < 16 or (now.hour == 16 and now.minute < 30):
        d -= datetime.timedelta(days=1)
    return d


def fetch_yfinance(tickers: list[str], notes: list[str]) -> tuple[dict, "object"]:
    """回傳 ({ticker: 含息還原收盤 Series}, 1475.T 未還原收盤 Series 或 None)。"""
    import yfinance as yf
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_etf_dash as etfdash  # noqa: E402 — 只借 yf_call_with_backoff()

    out, raw_topix = {}, None
    for tk in tickers:
        try:
            h = etfdash.yf_call_with_backoff(
                lambda tk=tk: yf.Ticker(tk).history(period="max", auto_adjust=True), label=f"dd {tk}")
            if h is None or h.empty:
                raise RuntimeError("空資料")
            s = h["Close"].copy()
            s.index = _naive(s.index)
            s = s[~s.index.duplicated(keep="last")].dropna()
            out[tk] = s
        except Exception as e:  # noqa: BLE001
            notes.append(f"{tk}：yfinance 抓取失敗（{e}），該檔留空。")
    if TOPIX_TICKER in tickers:
        try:
            h = etfdash.yf_call_with_backoff(
                lambda: yf.Ticker(TOPIX_TICKER).history(period="max", auto_adjust=False), label="dd 1475.T raw")
            raw_topix = h["Close"].copy()
            raw_topix.index = _naive(raw_topix.index)
            raw_topix = raw_topix[~raw_topix.index.duplicated(keep="last")].dropna()
        except Exception as e:  # noqa: BLE001
            notes.append(f"1475.T 未還原收盤抓取失敗（{e}），無法判斷配息記錄是否仍是壞的，還原價不修正。")
    return out, raw_topix


def fetch_price_store(tickers: list[str], notes: list[str]) -> tuple[dict, "object"]:
    sys.path.insert(0, str(Path.home() / "v7-backtest"))
    from src.price_store import get_prices  # noqa: E402

    px = get_prices(tickers, start=None)
    out = {}
    for tk in tickers:
        if tk in px and px[tk].notna().any():
            out[tk] = px[tk].dropna()
        else:
            notes.append(f"{tk}：價格庫沒有資料，該檔留空。")
    raw_topix = None
    if TOPIX_TICKER in tickers:
        raw = get_prices([TOPIX_TICKER], field="close", refresh=False)
        if TOPIX_TICKER in raw:
            raw_topix = raw[TOPIX_TICKER].dropna()
    return out, raw_topix


def fix_topix(adj, raw, notes: list[str]):
    import pandas as pd
    bad = [pd.Timestamp(d) for d in TOPIX_BAD_DATES]
    adj = adj.drop([d for d in bad if d in adj.index])
    if raw is None:
        return adj
    raw = raw.drop([d for d in bad if d in raw.index])
    ratio = (adj / raw.reindex(adj.index)).dropna()
    fix_at = pd.Timestamp(TOPIX_FIX_BEFORE)
    before, after = ratio[ratio.index < fix_at], ratio[ratio.index >= fix_at]
    if before.empty or after.empty:
        return adj
    jump = float(after.iloc[0] / before.iloc[-1])
    if jump > TOPIX_FIX_DETECT:
        adj = adj.copy()
        adj[adj.index < fix_at] *= TOPIX_FIX_FACTOR
        notes.append(f"1475.T（TOPIX）：2024-08-08、08-09 收盤少一位數，整天剔除；Yahoo 還原係數在 2024-08-09 跨過時跳 {100 * (jump - 1):.1f}%，"
                     f"判斷是壞配息記錄，該日以前的還原價乘 {TOPIX_FIX_FACTOR}（估計值）。")
    else:
        notes.append("1475.T（TOPIX）：2024-08-08、08-09 收盤少一位數，整天剔除；還原係數已無異常跳動，不另修正。")
    return adj


# ── 計算 ─────────────────────────────────────────────────────────────────
def to_usd_panel(funds: list[dict], series: dict, cutoff, notes: list[str]):
    """回傳 (以 SPY 交易日為列、基金鍵為欄的美元含息價寬表, {key: 最後一筆自有資料日})。"""
    import pandas as pd
    spy_tk = next(f["yf_ticker"] for f in funds if f["key"] == BENCH)
    spy = series[spy_tk]
    cal = spy.index[(spy.index >= pd.Timestamp(START)) & (spy.index <= cutoff)]
    panel, last_own = {}, {}
    for f in funds:
        s = series.get(f["yf_ticker"])
        if s is None or s.empty:
            continue
        s = s[s.index <= cutoff]
        if f["currency"] != "USD":
            fxs = series.get(FX_TICKER[f["currency"]])
            if fxs is None:
                notes.append(f"{f['key']}：缺 {FX_TICKER[f['currency']]} 匯率，無法換美元，留空。")
                continue
            fx = fxs.reindex(s.index.union(fxs.index)).ffill().reindex(s.index)
            s = (s / fx).dropna()
        if s.empty:
            continue
        last_own[f["key"]] = s.index[-1]
        panel[f["key"]] = s.reindex(cal.union(s.index)).ffill().reindex(cal)
    return pd.DataFrame(panel, index=cal), last_own


def find_episodes(spy) -> tuple[list[dict], dict]:
    """SPY 由前高跌 ≥ 10% 的區段，以及目前這一段（還沒回前高）的狀態。"""
    vals, idx = spy.values, spy.index
    eps = []
    pk_i, tr_i, in_dd = 0, None, False
    for i in range(1, len(vals)):
        if vals[i] >= vals[pk_i]:
            if in_dd and vals[tr_i] / vals[pk_i] - 1 <= -EPISODE_THRESHOLD:
                eps.append({"peak_i": pk_i, "trough_i": tr_i, "rec_i": i})
            pk_i, tr_i, in_dd = i, None, False
        else:
            if not in_dd or vals[i] < vals[tr_i]:
                tr_i = i
            in_dd = True
    cur = {"peak_i": pk_i, "trough_i": tr_i if in_dd else None}
    if in_dd and vals[tr_i] / vals[pk_i] - 1 <= -EPISODE_THRESHOLD:
        eps.append({"peak_i": pk_i, "trough_i": tr_i, "rec_i": None})
    return eps, cur


def _pct(a, b):
    import math
    if a is None or b is None or not (a == a) or not (b == b) or b == 0:
        return None
    v = 100.0 * (a / b - 1.0)
    return None if math.isnan(v) else round(v, 2)


def _val(s, i):
    v = float(s.iloc[i])
    return None if v != v else v


def build(source: str) -> dict:
    import pandas as pd

    t0 = time.time()
    notes: list[str] = []
    funds = fund_list()
    tickers = sorted({f["yf_ticker"] for f in funds if f["yf_ticker"]} | set(FX_TICKER.values()))
    if source == "price_store":
        series, raw_topix = fetch_price_store(tickers, notes)
    else:
        series, raw_topix = fetch_yfinance(tickers, notes)
    if TOPIX_TICKER in series:
        series[TOPIX_TICKER] = fix_topix(series[TOPIX_TICKER], raw_topix, notes)

    spy_tk = next(f["yf_ticker"] for f in funds if f["key"] == BENCH)
    if spy_tk not in series or series[spy_tk].empty:
        raise RuntimeError("SPY 價格抓取失敗")
    cutoff = pd.Timestamp(last_closed_date())
    P, last_own = to_usd_panel(funds, series, cutoff, notes)
    spy = P[BENCH]
    idx = P.index
    as_of = idx[-1]
    D = lambda i: idx[i].strftime("%Y-%m-%d")  # noqa: E731

    for f in funds:
        k = f["key"]
        if k in last_own and (as_of - last_own[k]).days > 4:
            notes.append(f"{k}：自有資料只到 {last_own[k]:%Y-%m-%d}，之後以該日收盤持平計算。")
    if "TAIEX" in P:
        notes.append("TAIEX 是加權價格指數，不含息，不能直接買，只列作對照。")

    eps_raw, cur = find_episodes(spy)
    last_i = len(idx) - 1

    def fund_cells(pk, tr, end):
        cells = {}
        s_dd = _pct(_val(spy, tr), _val(spy, pk))
        s_rb = _pct(_val(spy, end), _val(spy, tr))
        for f in funds:
            k = f["key"]
            if k not in P or k == BENCH:
                continue
            s = P[k]
            a, b, c = _val(s, pk), _val(s, tr), _val(s, end)
            if a is None or b is None:
                cells[k] = None
                continue
            dd, rb, full = _pct(b, a), _pct(c, b), _pct(c, a)
            cells[k] = {"dd_pct": dd, "rel_pp": None if dd is None else round(dd - s_dd, 2),
                        "rebound_pct": rb, "rebound_rel_pp": None if rb is None else round(rb - s_rb, 2),
                        "full_pct": full}
        return cells

    episodes = []
    for n, e in enumerate(eps_raw, 1):
        pk, tr, rc = e["peak_i"], e["trough_i"], e["rec_i"]
        end = rc if rc is not None else last_i
        spy_cell = {"dd_pct": _pct(_val(spy, tr), _val(spy, pk)), "rebound_pct": _pct(_val(spy, end), _val(spy, tr)),
                    "full_pct": _pct(_val(spy, end), _val(spy, pk))}
        episodes.append({
            "id": n, "status": "closed" if rc is not None else "ongoing",
            "peak": D(pk), "trough": D(tr), "recovery": D(rc) if rc is not None else None, "end_used": D(end),
            "days_peak_to_trough": (idx[tr] - idx[pk]).days, "days_trough_to_recovery": (idx[end] - idx[tr]).days,
            "days_total": (idx[end] - idx[pk]).days,
            "tdays_peak_to_trough": tr - pk, "tdays_trough_to_recovery": end - tr,
            "spy": spy_cell, "funds": fund_cells(pk, tr, end),
        })

    # 三個門檻的彙總（只算已回前高的區段）
    keys = [f["key"] for f in funds if f["key"] != BENCH and f["key"] in P]
    summary = {}
    for th in SUMMARY_THRESHOLDS:
        sel = [e for e in episodes if e["status"] == "closed" and e["spy"]["dd_pct"] <= -th]
        rows = {}
        for k in keys:
            cs = [e["funds"].get(k) for e in sel]
            cs = [c for c in cs if c and c["dd_pct"] is not None]
            if not cs:
                rows[k] = {"n": 0, "shallower": 0, "avg_rel_pp": None, "avg_rebound_rel_pp": None, "avg_dd_pct": None}
                continue
            rb = [c["rebound_rel_pp"] for c in cs if c["rebound_rel_pp"] is not None]
            rows[k] = {"n": len(cs), "shallower": sum(1 for c in cs if c["rel_pp"] > 0),
                       "avg_rel_pp": round(sum(c["rel_pp"] for c in cs) / len(cs), 2),
                       "avg_rebound_rel_pp": round(sum(rb) / len(rb), 2) if rb else None,
                       "avg_dd_pct": round(sum(c["dd_pct"] for c in cs) / len(cs), 2)}
        summary[str(th)] = {
            "threshold_pct": th, "episode_ids": [e["id"] for e in sel], "n_episodes": len(sel),
            "spy_avg_dd_pct": round(sum(e["spy"]["dd_pct"] for e in sel) / len(sel), 2) if sel else None,
            "spy_avg_rebound_pct": round(sum(e["spy"]["rebound_pct"] for e in sel) / len(sel), 2) if sel else None,
            "funds": rows,
        }

    # 目前狀態
    pk = cur["peak_i"]
    now_dd = _pct(_val(spy, last_i), _val(spy, pk))
    spell_min = _pct(_val(spy, cur["trough_i"]), _val(spy, pk)) if cur["trough_i"] is not None else 0.0
    if spell_min is not None and spell_min <= -100 * EPISODE_THRESHOLD:
        status = "ongoing"
    elif now_dd is not None and now_dd <= -100 * WATCH_THRESHOLD:
        status = "watch"
    else:
        status = "normal"
    current = {"date": D(last_i), "spy_peak": D(pk), "spy_dd_pct": now_dd,
               "spell_trough": D(cur["trough_i"]) if cur["trough_i"] is not None else None,
               "spell_min_pct": spell_min, "status": status,
               "episode_id": episodes[-1]["id"] if status == "ongoing" else None, "funds": None}
    if status in ("watch", "ongoing"):
        cf = {}
        for k in keys:
            a, c = _val(P[k], pk), _val(P[k], last_i)
            dd = _pct(c, a)
            cf[k] = None if dd is None else {"dd_pct": dd, "rel_pp": round(dd - now_dd, 2),
                                              "last_date": last_own[k].strftime("%Y-%m-%d")}
        current["funds"] = cf

    # 十年報酬與對 SPY 超額（幾何：(1+基金)/(1+SPY)−1）
    ten_start = as_of - pd.DateOffset(years=TEN_YEARS)
    i0 = int(idx.searchsorted(ten_start, side="right")) - 1
    i0 = max(i0, 0)
    spy10 = _pct(_val(spy, last_i), _val(spy, i0))
    fund_meta = []
    for f in funds:
        k = f["key"]
        row = {"key": k, "label_zh": f["label_zh"], "yf_ticker": f["yf_ticker"], "currency": f["currency"],
               "first_date": None, "last_date": None, "ten_year_return_pct": None, "ten_year_excess_pct": None}
        if k in P:
            s = P[k].dropna()
            row["first_date"] = s.index[0].strftime("%Y-%m-%d")
            row["last_date"] = last_own[k].strftime("%Y-%m-%d")
            # 自有資料要早於十年起點才算（避免 ffill 前段空白被當成有資料）
            if s.index[0] <= idx[i0]:
                r = _pct(_val(P[k], last_i), _val(P[k], i0))
                row["ten_year_return_pct"] = r
                if r is not None and spy10 is not None and k != BENCH:
                    row["ten_year_excess_pct"] = round(100 * ((1 + r / 100) / (1 + spy10 / 100) - 1), 2)
        fund_meta.append(row)

    return {
        "schema": SCHEMA,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": D(last_i), "source": source, "bench": BENCH, "start": D(0),
        "episode_threshold_pct": int(100 * EPISODE_THRESHOLD), "watch_threshold_pct": int(100 * WATCH_THRESHOLD),
        "summary_thresholds": list(SUMMARY_THRESHOLDS),
        "ten_year_start": D(i0), "spy_ten_year_return_pct": spy10,
        "funds": fund_meta, "episodes": episodes, "summary": summary, "current": current,
        "notes": notes, "runtime_s": round(time.time() - t0, 1),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", choices=["yfinance", "price_store"], default="yfinance")
    ap.add_argument("--no-write", action="store_true", help="只印摘要，不寫 drawdowns.json")
    args = ap.parse_args()
    try:
        out = build(args.source)
    except Exception as e:  # noqa: BLE001
        print(f"[drawdowns] 失敗，不覆蓋舊檔：{e}", file=sys.stderr)
        sys.exit(1)
    cur = out["current"]
    print(f"[drawdowns] as_of {out['as_of']}  區段 {len(out['episodes'])}  SPY 離前高 {cur['spy_dd_pct']}%（{cur['status']}）  {out['runtime_s']}s")
    for e in out["episodes"]:
        x = e["funds"].get("XLV") or {}
        print(f"  #{e['id']} {e['peak']}→{e['trough']}→{e['recovery']}  SPY {e['spy']['dd_pct']}  XLV {x.get('dd_pct')}  {e['status']}")
    if not args.no_write:
        OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"[drawdowns] 寫入 {OUT_PATH.relative_to(REPO_ROOT)}（{OUT_PATH.stat().st_size / 1024:.0f} KB）")


if __name__ == "__main__":
    main()
