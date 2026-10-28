#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主動式 ETF「到底多主動」每日儀表的資料：docs/active-etf/data/activeness.json。

每檔每天算：
  1. 對 0050 的 active share＝½ Σ|w_基金 − w_0050|（聯集，缺的一邊當 0），跟
     build_active_etf.active_share() 同一條公式、同一種權重（基金官方 weight_pct，
     不重新歸一）。
  2. 台積電權重減 0050 的台積電權重（百分點）。
  3. 60 日滾動：每日主動報酬（基金含息日報酬 − 0050 含息日報酬）的平均配對相關、
     各檔對其他檔的平均相關、第一主成分解釋比例（相關矩陣最大特徵值 ÷ 檔數）。
  4. 換手：相鄰兩份持股快照之間 ½ Σ|w_今天 − w_預期|，w_預期＝前一份權重照這段
     期間個股漲跌自然漂移後的權重（扣掉股價漲跌造成的權重變化，只留買賣）。同時
     輸出不扣漂移的原始版。近 20／60 個交易日累加；快照缺日不補，標出缺幾天。
  5. 整體：22 檔平均 active share、平均配對相關、第一主成分，和約一個月前（21 個
     交易日）比，比較時只用兩個日期都有資料的基金。
  6. 本站挑選：data/active_etf/picks.json 最新一筆登記的攻方 active share 與
     active_share_min 查核點門檻。

0050 權重：data/etf_dash/snapshots/0050/*.json 每天一份（2026-09-24 起）。某日的
0050 權重＝該日之前最近一份快照，再用個股收盤價把權重漂移到該日；早於第一份快照的
日子用第一份快照往回漂移（0050 季度調整的成分股進出因此沒算到，見 notes）。最新
一天的 0050 權重跟 docs/etf-dash/data/0050.json 同一份，所以 active share 跟
picks_candidates.json 的 active_share_vs_0050_pct 一致。

價格：
  --price-source yf     （預設，CI 用）yfinance auto_adjust=False，Adj Close 算含息報酬
  --price-source store  （本機）~/v7-backtest/src/price_store.py，refresh=False，不下載
兩種來源的收盤都會跟 data/active_etf/prices.jsonl 對一次：某日一半以上基金差 0.3%
以上（多半是盤中價）就整天剔除；全部價格跟前一天一模一樣的日子（Yahoo 假日補行）
也剔除。漂移用的個股收盤一律讀 data/active_etf/prices.jsonl（不還原，市值權重本來
就跟著不還原價格走）。

  python3 scripts/active_etf/activeness.py
  python3 scripts/active_etf/activeness.py --price-source store
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
HOLDINGS_DIR = REPO_ROOT / "data" / "active_etf" / "holdings"
PRICES_PATH = REPO_ROOT / "data" / "active_etf" / "prices.jsonl"
PICKS_PATH = REPO_ROOT / "data" / "active_etf" / "picks.json"
BENCH_SNAP_DIR = REPO_ROOT / "data" / "etf_dash" / "snapshots" / "0050"
BENCH_CURRENT = REPO_ROOT / "docs" / "etf-dash" / "data" / "0050.json"
OVERVIEW_PATH = REPO_ROOT / "docs" / "active-etf" / "data" / "overview.json"
OUT_PATH = REPO_ROOT / "docs" / "active-etf" / "data" / "activeness.json"

BENCH = "0050.TW"
TSMC = "2330"
DOWNLOAD_START = "2025-05-01"
CORR_WINDOW = 60
SKIP_AFTER_LISTING = 5          # 上市後前 5 個交易日的報酬不用（跟 10-28 深度檢驗同一做法）
MONTH_BACK = 21                 # 「一個月前」＝21 個交易日前
STALE_FFILL = 5                 # 中位數序列：快照最多沿用 5 個交易日
CLOSE_TOL = 0.003               # 收盤核對容忍 0.3%
MIN_FUNDS_CORR = 3


# ── 讀資料 ────────────────────────────────────────────────────────────────
def base(ticker: str) -> str:
    """去掉 .TW／.TWO 後綴。官方持股檔偶爾把上櫃股標成 .TW（例如 00981A 2026-10-13
    的第二份），用代號本身比對才不會把同一檔股票算成一賣一買。"""
    return ticker.split(".")[0]


def load_holdings() -> dict:
    """{code: [(as_of, {ticker: weight_pct}), ...]}，同一天多份只留最後一份。"""
    out = {}
    for p in sorted(HOLDINGS_DIR.glob("*.jsonl")):
        by_day = {}
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            w = {}
            for t, _sh, wp in r.get("holdings") or []:
                if wp is not None:
                    k = base(t)
                    w[k] = w.get(k, 0.0) + float(wp)
            if w:
                by_day[r["as_of"]] = w
        out[p.stem] = sorted(by_day.items())
    return out


def load_raw_closes() -> tuple[pd.DataFrame, pd.Series]:
    """data/active_etf/prices.jsonl → (收盤寬表, 0050 成交量)。"""
    rows, vol = {}, {}
    for line in PRICES_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            rows[r["date"]] = r.get("close") or {}
            vol[r["date"]] = (r.get("volume") or {}).get(BENCH)
    df = pd.DataFrame.from_dict(rows, orient="index").sort_index()
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    # 欄位改成去後綴的代號；同一代號有 .TW 與 .TWO 兩欄時合併（先取有值的）
    df = df.T.groupby(lambda t: base(t)).first().T
    v = pd.Series(vol, dtype=float)
    v.index = pd.to_datetime(v.index)
    return df.astype(float), v.sort_index()


def stale_rows(df: pd.DataFrame, share: float = 0.9) -> list:
    """全部（≥90%）價格跟前一列一模一樣的日期（Yahoo 在休市日補的重複列）。"""
    out = []
    prev = None
    for d, row in df.iterrows():
        if prev is not None:
            both = row.notna() & prev.notna()
            n = int(both.sum())
            if n >= 3 and (row[both] == prev[both]).mean() >= share:
                out.append(d)
        prev = row
    return out


def load_bench_snapshots() -> list:
    """[(holdings_as_of, {ticker: weight_pct}), ...]，依日期排序，同日去重（後者覆蓋）。"""
    by_day = {}
    paths = sorted(BENCH_SNAP_DIR.glob("*.json")) if BENCH_SNAP_DIR.exists() else []
    for p in paths + ([BENCH_CURRENT] if BENCH_CURRENT.exists() else []):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        ha = d.get("holdings_as_of")
        w = {base(c["ticker"]): float(c["weight_pct"]) for c in d.get("constituents") or []
             if c.get("ticker") and c.get("weight_pct") is not None}
        if ha and w:
            by_day[ha] = w
    return sorted(by_day.items())


def load_names() -> dict:
    try:
        ov = json.loads(OVERVIEW_PATH.read_text(encoding="utf-8"))
        return {f["code"]: f.get("name") for f in ov.get("funds") or []}
    except (OSError, ValueError):
        return {}


def load_attack_pick() -> dict:
    try:
        reg = json.loads(PICKS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    regs = sorted(reg.get("registrations") or [], key=lambda r: (r.get("registered_on") or "", r.get("id") or ""))
    if not regs:
        return {}
    last = regs[-1]
    atk = next((p for p in last.get("picks") or [] if p.get("role") == "攻"), None)
    if not atk:
        return {}
    cp = next((c for c in last.get("checkpoints") or []
               if c.get("kind") == "active_share_min" and c.get("code") == atk["code"]), None)
    return {"registration_id": last.get("id"), "registered_on": last.get("registered_on"),
            "code": atk["code"], "name": atk.get("name"),
            "checkpoint_id": cp.get("id") if cp else None,
            "threshold_pct": cp.get("min") if cp else None,
            "checkpoint_text": cp.get("text") if cp else None}


# ── 含息價格 ──────────────────────────────────────────────────────────────
def prices_from_yf(tickers: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    import yfinance as yf
    last_err = None
    for attempt in range(3):
        try:
            raw = yf.download(tickers, start=DOWNLOAD_START, auto_adjust=False, group_by="ticker",
                              progress=False, threads=True)
            break
        except Exception as e:  # noqa: BLE001 — 網路錯誤一律重試
            last_err = e
            time.sleep(5 * (attempt + 1))
    else:
        raise RuntimeError("yfinance 下載失敗：%s" % last_err)
    close, adj = {}, {}
    for t in tickers:
        try:
            sub = raw[t]
        except KeyError:
            continue
        close[t] = sub["Close"]
        adj[t] = sub["Adj Close"]
    c, a = pd.DataFrame(close), pd.DataFrame(adj)
    for df in (c, a):
        df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
    return c, a


def prices_from_store(tickers: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    sys.path.insert(0, str(Path.home() / "v7-backtest" / "src"))
    from price_store import get_prices  # noqa: E402
    c = get_prices(tickers, start=DOWNLOAD_START, field="close", refresh=False)
    a = get_prices(tickers, start=DOWNLOAD_START, field="adj_close", refresh=False)
    return c, a


def clean_prices(close: pd.DataFrame, adj: pd.DataFrame, official: pd.DataFrame, notes: list) -> pd.DataFrame:
    """剔除休市補行與盤中價的日子，回傳乾淨的含息收盤寬表。"""
    close = close.dropna(how="all")
    adj = adj.reindex(close.index)
    drop = set(stale_rows(close))
    if drop:
        notes.append("價格來源有 %d 天跟前一天完全相同，是休市日的補行，已剔除：%s。"
                     % (len(drop), "、".join(sorted(d.strftime("%Y-%m-%d") for d in drop)[-5:])))
    bad = []
    for d in close.index:
        if d in drop or d not in official.index:
            continue
        a = close.loc[d].rename(base)
        b = official.loc[d].reindex(a.index)
        both = a.notna() & b.notna() & (b > 0)
        if int(both.sum()) < 3:
            continue
        diff = (a[both] / b[both] - 1).abs()
        if (diff > CLOSE_TOL).mean() > 0.5:
            bad.append(d)
    if bad:
        notes.append("價格來源有 %d 天的收盤跟每日收盤快取對不上，一半以上基金差 0.3%% 以上，多半是盤中價，整天剔除：%s。"
                     % (len(bad), "、".join(d.strftime("%Y-%m-%d") for d in bad[-5:])))
        drop |= set(bad)
    return adj.drop(index=sorted(drop))


# ── 0050 權重 ─────────────────────────────────────────────────────────────
class BenchWeights:
    """某日的 0050 權重＝最近一份快照漂移到該日（早於第一份就往回漂移）。"""

    def __init__(self, snaps: list, raw: pd.DataFrame):
        self.snaps = [(pd.Timestamp(d), w) for d, w in snaps]
        self.raw = raw
        self.cache = {}

    def _px(self, d: pd.Timestamp) -> pd.Series:
        idx = self.raw.index[self.raw.index <= d]
        if len(idx) == 0:
            idx = self.raw.index[:1]
        return self.raw.loc[idx[-1]]

    def get(self, day: str) -> tuple[dict, str, str]:
        if day in self.cache:
            return self.cache[day]
        d = pd.Timestamp(day)
        before = [s for s in self.snaps if s[0] <= d]
        anchor_d, w0 = before[-1] if before else self.snaps[0]
        if anchor_d == d:
            res = (w0, anchor_d.strftime("%Y-%m-%d"), "snapshot")
        else:
            p0, p1 = self._px(anchor_d), self._px(d)
            out = {}
            for t, x in w0.items():
                a, b = p0.get(t), p1.get(t)
                f = b / a if (a and b and not math.isnan(a) and not math.isnan(b) and a > 0) else 1.0
                out[t] = x * f
            s0, s1 = sum(w0.values()), sum(out.values())
            out = {t: v * s0 / s1 for t, v in out.items()} if s1 else w0
            res = (out, anchor_d.strftime("%Y-%m-%d"), "drift_fwd" if before else "drift_back")
        self.cache[day] = res
        return res


def active_share(fw: dict, bw: dict) -> float:
    tickers = set(fw) | set(bw)
    return sum(abs(fw.get(t, 0.0) - bw.get(t, 0.0)) for t in tickers) / 2


def drift_weights(w: dict, p0: pd.Series, p1: pd.Series) -> dict:
    out = {}
    for t, x in w.items():
        a, b = p0.get(t), p1.get(t)
        f = b / a if (a is not None and b is not None and not math.isnan(a) and not math.isnan(b) and a > 0) else 1.0
        out[t] = x * f
    s0, s1 = sum(w.values()), sum(out.values())
    return {t: v * s0 / s1 for t, v in out.items()} if s1 else dict(w)


# ── 主動報酬相關 ──────────────────────────────────────────────────────────
def corr_stats(M: pd.DataFrame):
    C = np.corrcoef(M.values, rowvar=False)
    n = C.shape[0]
    iu = np.triu_indices(n, 1)
    mean_pair = float(C[iu].mean())
    ev = np.linalg.eigvalsh(C)
    pc1 = float(ev[-1] / n)
    per = {c: float((C[i].sum() - 1) / (n - 1)) for i, c in enumerate(M.columns)}
    return mean_pair, pc1, per


def r2(x, nd=2):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return None
    return round(float(x), nd)


# ── 主流程 ────────────────────────────────────────────────────────────────
def build(price_source: str) -> dict:
    t0 = time.time()
    notes = []
    holdings = load_holdings()
    codes = sorted(holdings)
    names = load_names()
    raw, vol0050 = load_raw_closes()
    raw_stale = set(stale_rows(raw)) | set(vol0050[vol0050 == 0].index)
    raw_clean = raw.drop(index=sorted(d for d in raw_stale if d in raw.index))
    bench_snaps = load_bench_snapshots()
    if not bench_snaps:
        raise RuntimeError("找不到 0050 持股快照（data/etf_dash/snapshots/0050／docs/etf-dash/data/0050.json）")
    bw = BenchWeights(bench_snaps, raw_clean)

    # 交易日曆：prices.jsonl（去掉休市補行）∪ 所有持股快照日
    cal = sorted(set(raw_clean.index.strftime("%Y-%m-%d")) |
                 {d for c in codes for d, _ in holdings[c]})
    cal_pos = {d: i for i, d in enumerate(cal)}

    # ── 1, 2, 4：逐份快照 ──
    funds = {}
    for c in codes:
        snaps = holdings[c]
        ser = {"d": [], "as": [], "tsmc": [], "to": [], "to_raw": [], "span": []}
        prev = None
        for d, w in snaps:
            b, _anchor, _src = bw.get(d)
            ser["d"].append(d)
            ser["as"].append(r2(active_share(w, b)))
            ser["tsmc"].append(r2(w.get(TSMC, 0.0) - b.get(TSMC, 0.0)))
            if prev is None:
                ser["to"].append(None)
                ser["to_raw"].append(None)
                ser["span"].append(None)
            else:
                pd0, pw = prev
                p0 = raw_clean.loc[raw_clean.index[raw_clean.index <= pd.Timestamp(pd0)][-1]] \
                    if (raw_clean.index <= pd.Timestamp(pd0)).any() else pd.Series(dtype=float)
                p1 = raw_clean.loc[raw_clean.index[raw_clean.index <= pd.Timestamp(d)][-1]] \
                    if (raw_clean.index <= pd.Timestamp(d)).any() else pd.Series(dtype=float)
                exp = drift_weights(pw, p0, p1)
                ser["to"].append(r2(active_share(w, exp)))
                ser["to_raw"].append(r2(active_share(w, pw)))
                ser["span"].append(cal_pos[d] - cal_pos[pd0])
            prev = (d, w)
        funds[c] = {"code": c, "name": names.get(c), "series": ser}

    # 換手：以該檔最後一份快照日為終點，往回 N 個交易日
    def turnover_window(ser, end_idx, n):
        end_d = ser["d"][end_idx]
        start_pos = cal_pos[end_d] - n
        tot, tot_raw, covered = 0.0, 0.0, 0
        for i in range(end_idx, 0, -1):
            d0 = ser["d"][i - 1]
            if cal_pos[d0] < start_pos:
                break
            tot += ser["to"][i] or 0.0
            tot_raw += ser["to_raw"][i] or 0.0
            covered += 1
        missing = n - covered
        if start_pos < cal_pos[ser["d"][0]]:
            return None, None, None
        return r2(tot, 1), r2(tot_raw, 1), missing

    for c, f in funds.items():
        ser = f["series"]
        ser["to20"], ser["to60"] = [], []
        for i in range(len(ser["d"])):
            a, _, m = turnover_window(ser, i, 20)
            ser["to20"].append(a)
            b, _, _ = turnover_window(ser, i, 60)
            ser["to60"].append(b)
        last = len(ser["d"]) - 1
        to20, to20r, miss20 = turnover_window(ser, last, 20)
        to60, to60r, miss60 = turnover_window(ser, last, 60)
        f["latest"] = {
            "as_of": ser["d"][last],
            "active_share_pct": ser["as"][last],
            "tsmc_dev_pp": ser["tsmc"][last],
            "turnover_20d_pct": to20, "turnover_20d_raw_pct": to20r, "missing_days_20d": miss20,
            "turnover_60d_pct": to60, "turnover_60d_raw_pct": to60r, "missing_days_60d": miss60,
            "n_snapshots": len(ser["d"]), "first_snapshot": ser["d"][0],
        }

    # ── 3：含息價格與主動報酬 ──
    tickers = [c + ".TW" for c in codes] + [BENCH]
    if price_source == "store":
        close, adj = prices_from_store(tickers)
    else:
        close, adj = prices_from_yf(tickers)
    adj = clean_prices(close, adj, raw, notes)
    if BENCH not in adj or adj[BENCH].dropna().empty:
        raise RuntimeError("沒有 0050 含息價格")
    adj = adj[adj[BENCH].notna()]
    ret = adj.pct_change(fill_method=None).iloc[1:]
    act = pd.DataFrame(index=ret.index)
    listing = {}
    for c in codes:
        t = c + ".TW"
        if t not in ret:
            continue
        s = adj[t].dropna()
        if s.empty:
            continue
        listing[c] = s.index[0]
        r = ret[t].copy()
        first_ok = ret.index[ret.index > s.index[0]]
        if len(first_ok) > SKIP_AFTER_LISTING:
            r[r.index < first_ok[SKIP_AFTER_LISTING]] = np.nan
        else:
            r[:] = np.nan
        act[c] = r - ret[BENCH]
    price_last = adj.index[-1].strftime("%Y-%m-%d")

    roll_dates, roll_mean, roll_pc1, roll_n = [], [], [], []
    per_fund_corr = {c: {} for c in codes}
    for i in range(CORR_WINDOW - 1, len(act)):
        W = act.iloc[i - CORR_WINDOW + 1:i + 1]
        cols = [c for c in W.columns if W[c].notna().all()]
        if len(cols) < MIN_FUNDS_CORR:
            continue
        mp, pc1, per = corr_stats(W[cols])
        d = act.index[i].strftime("%Y-%m-%d")
        roll_dates.append(d)
        roll_mean.append(r2(mp, 3))
        roll_pc1.append(r2(pc1, 3))
        roll_n.append(len(cols))
        for c, v in per.items():
            per_fund_corr[c][d] = r2(v, 3)

    # 近一年對 0050 超額（上市不到一年用上市後第 6 個交易日起）
    last_dt = adj.index[-1]
    one_y = last_dt - pd.DateOffset(years=1)
    for c in codes:
        f = funds[c]
        t = c + ".TW"
        ex, since, start_d = None, None, None
        if t in adj and c in listing:
            s = adj[t].dropna()
            idx_after = s.index[SKIP_AFTER_LISTING:] if len(s) > SKIP_AFTER_LISTING else s.index[:0]
            if len(idx_after):
                base_d = max(idx_after[0], adj.index[adj.index >= one_y][0])
                since = "listing" if base_d > adj.index[adj.index >= one_y][0] else "1y"
                if s.index[-1] == last_dt:
                    ex = (s.iloc[-1] / s.loc[base_d]) / (adj[BENCH].iloc[-1] / adj[BENCH].loc[base_d]) - 1
                    start_d = base_d.strftime("%Y-%m-%d")
        pc = per_fund_corr[c]
        last_corr_d = max(pc) if pc else None
        f["latest"].update({
            "excess_1y_pct": r2(ex * 100 if ex is not None else None, 1),
            "excess_1y_basis": since, "excess_1y_start": start_d,
            "avg_corr_others": pc.get(roll_dates[-1]) if roll_dates else None,
            "avg_corr_as_of": roll_dates[-1] if roll_dates and roll_dates[-1] in pc else last_corr_d,
            "listing_date": listing[c].strftime("%Y-%m-%d") if c in listing else None,
        })
        f["series"]["corr"] = {"d": sorted(pc), "v": [pc[d] for d in sorted(pc)]}
        f["stale"] = (cal_pos.get(price_last, len(cal) - 1) - cal_pos[f["latest"]["as_of"]]) > 3 \
            if price_last in cal_pos else False

    # ── 5：整體時間序列與一行摘要 ──
    as_median = {"d": [], "median": [], "mean": [], "n": []}
    snap_map = {c: dict(zip(funds[c]["series"]["d"], funds[c]["series"]["as"])) for c in codes}
    first_any = min(funds[c]["series"]["d"][0] for c in codes)
    for d in cal:
        if d < first_any:
            continue
        p = cal_pos[d]
        vals = []
        for c in codes:
            for k in range(0, STALE_FFILL + 1):
                if p - k < 0:
                    break
                v = snap_map[c].get(cal[p - k])
                if v is not None:
                    vals.append(v)
                    break
        if vals:
            as_median["d"].append(d)
            as_median["median"].append(r2(float(np.median(vals))))
            as_median["mean"].append(r2(float(np.mean(vals))))
            as_median["n"].append(len(vals))

    def as_at(c, d):
        """該檔在 d（含）之前最近一份快照的 active share，沿用最多 STALE_FFILL 個交易日。"""
        p = cal_pos[d]
        for k in range(0, STALE_FFILL + 1):
            if p - k < 0:
                break
            v = snap_map[c].get(cal[p - k])
            if v is not None:
                return v
        return None

    latest_hold = max(f["latest"]["as_of"] for f in funds.values())
    month_ago_hold = cal[max(0, cal_pos[latest_hold] - MONTH_BACK)]
    as_now = {c: funds[c]["latest"]["active_share_pct"] for c in codes}
    as_then = {c: as_at(c, month_ago_hold) for c in codes}
    common_as = [c for c in codes if as_now[c] is not None and as_then[c] is not None]
    mean_as_all = float(np.mean([v for v in as_now.values() if v is not None]))

    overall = {
        "active_share_mean_pct": r2(mean_as_all),
        "active_share_median_pct": r2(float(np.median([v for v in as_now.values() if v is not None]))),
        "active_share_n": sum(v is not None for v in as_now.values()),
        "active_share_holdings_as_of": latest_hold,
        "active_share_change_1m_pp": r2(float(np.mean([as_now[c] for c in common_as]) -
                                            np.mean([as_then[c] for c in common_as]))) if common_as else None,
        "active_share_compare_date": month_ago_hold,
        "active_share_compare_n": len(common_as),
    }
    if roll_dates:
        i_now = len(roll_dates) - 1
        d_now = roll_dates[i_now]
        p_now = list(act.index.strftime("%Y-%m-%d")).index(d_now)
        d_then = act.index[max(0, p_now - MONTH_BACK)].strftime("%Y-%m-%d")
        Wn = act.iloc[p_now - CORR_WINDOW + 1:p_now + 1]
        p_then = p_now - MONTH_BACK
        Wt = act.iloc[p_then - CORR_WINDOW + 1:p_then + 1] if p_then - CORR_WINDOW + 1 >= 0 else None
        cols_now = [c for c in Wn.columns if Wn[c].notna().all()]
        cols_then = [c for c in Wt.columns if Wt[c].notna().all()] if Wt is not None else []
        common = [c for c in cols_now if c in cols_then]
        chg_corr = chg_pc1 = None
        if len(common) >= MIN_FUNDS_CORR:
            a_mp, a_pc, _ = corr_stats(Wn[common])
            b_mp, b_pc, _ = corr_stats(Wt[common])
            chg_corr, chg_pc1 = a_mp - b_mp, a_pc - b_pc
        overall.update({
            "corr_as_of": d_now, "corr_window_days": CORR_WINDOW,
            "mean_pair_corr": roll_mean[i_now], "pc1_share": roll_pc1[i_now], "corr_n": roll_n[i_now],
            "corr_change_1m": r2(chg_corr, 3), "pc1_change_1m": r2(chg_pc1, 3),
            "corr_compare_date": d_then, "corr_compare_n": len(common),
            "corr_funds": cols_now,
        })

    # ── 6：本站挑選 ──
    pick = load_attack_pick()
    if pick.get("code") in funds:
        lf = funds[pick["code"]]["latest"]
        pick.update({"active_share_pct": lf["active_share_pct"], "as_of": lf["as_of"],
                     "margin_pp": r2(lf["active_share_pct"] - pick["threshold_pct"])
                     if pick.get("threshold_pct") is not None and lf["active_share_pct"] is not None else None,
                     "series": {"d": funds[pick["code"]]["series"]["d"], "v": funds[pick["code"]]["series"]["as"]}})

    first_bench = bench_snaps[0][0]
    notes += [
        "active share 用各投信官方持股檔的占淨值比，現金不扣、權重不重新歸一。期貨部位不算持股，期貨多的基金（例如 00406A）active share 會偏高。",
        "0050 權重 %s 起用每日持股。更早的日子用 %s 那份持股照個股股價往回推，0050 季度調整時的成分股進出沒有算到。" % (first_bench, first_bench),
        "換手先扣掉股價漲跌造成的權重漂移，剩下的是買賣與申贖後的現金調整。不扣漂移的原始數字也放在資料檔裡，大約高出一倍。",
        "主動報酬是基金含息日報酬減 0050 含息日報酬，上市後前 %d 個交易日不用。60 日視窗裡每天都有報酬的基金才計入相關，所以早期的檔數比較少。" % SKIP_AFTER_LISTING,
        "近一年超額是 (1＋基金含息報酬)÷(1＋0050 含息報酬)−1。上市不滿一年的從上市後第 %d 個交易日算起。" % (SKIP_AFTER_LISTING + 1),
    ]
    stale = [c for c in codes if funds[c]["stale"]]
    if stale:
        notes.append("持股快照落後超過 3 個交易日：%s。" % "、".join("%s（%s）" % (c, funds[c]["latest"]["as_of"]) for c in stale))

    out = {
        "schema": "active-etf-activeness-v1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "price_source": price_source,
        "price_as_of": price_last,
        "holdings_as_of": latest_hold,
        "bench_snapshot_first": first_bench,
        "bench_snapshot_last": bench_snaps[-1][0],
        "overall": overall,
        "pick": pick,
        "series": {
            "active_share": as_median,
            "corr": {"d": roll_dates, "mean_pair": roll_mean, "pc1": roll_pc1, "n": roll_n},
        },
        "funds": [funds[c] for c in codes],
        "notes": notes,
        "runtime_sec": None,
    }
    out["runtime_sec"] = round(time.time() - t0, 1)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--price-source", choices=["yf", "store"], default="yf")
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args()
    data = build(args.price_source)
    Path(args.out).write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    o = data["overall"]
    print("activeness.json：價格到 %s、持股到 %s，%d 檔；平均 active share %.2f%%，平均配對相關 %s，PC1 %s（%s 秒）"
          % (data["price_as_of"], data["holdings_as_of"], len(data["funds"]), o["active_share_mean_pct"],
             o.get("mean_pair_corr"), o.get("pc1_share"), data["runtime_sec"]))
    for n in data["notes"]:
        print("  ·", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
