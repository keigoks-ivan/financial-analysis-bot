#!/usr/bin/env python3
"""貪婪／恐懼溫度計：每週更新（美股 4 項材料、台股 3 項材料）→ 頁面 /fear-greed/、latest.json、狀態改變通知。

定位：提醒，不是交易規則。只服務 30% 個股部位與現金，不碰 70% W52 引擎，不改任何 long-track 的計算。
研究出處：v7-backtest docs/FearGreed_Cap_Spec.md（事前登記）與 experiments/fear_greed/thermo.py。
研究結論：拿來調引擎槓桿（H1）兩市場皆不通過；保留「進入恐懼」當長期加碼提醒。

計算方法（與 thermo.py 相同，整數比較）
  每個材料先在自身頻率上算過去 10 年滾動百分位（含當筆；日資料窗 2520／最少 1260，月資料 120／60），
  方向統一成「越高越貪婪」；對齊到週五（取 ≤ 該週五的最後一筆，超過 45 天未更新視為缺值）；
  等權平均後四捨五入成 0–100 整數；可用材料數 < n−1 時當週不出分，狀態沿用前一週。
  狀態機：貪婪 ≥80 進、≤60 出；恐懼 ≤20 進、≥40 出（遲滯）。

資料（docs/fear-greed/data/，CI 不依賴 v7-backtest 本機路徑）
  raw/*.csv        各材料原始序列（種子取自 v7-backtest，之後每週增量追加）
  history_us.csv   每週分數、狀態、各材料百分位（種子＝v7-backtest thermo_weekly_us.csv，之後每週追加一列）
  history_tw.csv   同上，台股（種子由同一份原始序列重算，見下方「已修正的研究 bug」）
  latest.json      最新一週（頁面、long-track 一行、通知都讀它）

已修正的研究 bug：v7-backtest thermo.py 的 load_tw_median_pbr 用固定欄位 r[4] 取股價淨值比；
TWSE BWIBBU_d 在 2017-04 起欄位順序改變（r[4] 變成「股利年度」105…114），
2017 年以後該材料實為股利年度的階梯數字，百分位恆為 100。本檔改用欄位名稱「股價淨值比」取值。

資料抓取（任何一項失敗都不中斷，沿用上期資料並在 latest.json 標 stale）
  VIX／Baa 利差：FRED fredgraph.csv（免 key）。CAPE：shillerdata.com 首頁的 ie_data.xls 連結。
  融資餘額：FINRA margin-statistics.xlsx。選擇權賣買權未平倉比：期交所 pcRatioDown。
  台股融資餘額、個股股價淨值比：TWSE MI_MARGN／BWIBBU_d，每月只抓「最後一個週五所在週的最後交易日」
  （TWSE 會封快速連線，故單執行緒慢速、遇封鎖立刻放棄該端點）。

通知（只在狀態改變時）：寫 fg_alert.txt／fg_title.txt／fg_mail.html，由 workflow 寄 email 與 Discord；
本腳本自己不寄任何東西。--no-notify 不寫通知檔。

用法
  python3 scripts/update_fear_greed.py                 # 每週正常跑
  python3 scripts/update_fear_greed.py --no-notify     # 不寫通知檔（首次上線、手動重跑用）
  python3 scripts/update_fear_greed.py --no-fetch      # 只用現有 raw 檔重算（不連網）
  python3 scripts/update_fear_greed.py --rebuild       # 從 raw 重算整份 history（種子建立／驗算用）
  python3 scripts/update_fear_greed.py --test-alert    # 只寫一份標題含「測試」的通知檔（不比對狀態）
"""
from __future__ import annotations

import argparse
import html
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DOCS = ROOT / "docs" / "fear-greed"
DATA = DOCS / "data"
RAW = DATA / "raw"
LATEST = DATA / "latest.json"
PAGE = DOCS / "index.html"
PAGE_URL = "https://research.investmquest.com/fear-greed/"
TAIPEI = timezone(timedelta(hours=8))

# 狀態機門檻（事前登記，不准調）
GREED_IN, GREED_OUT, FEAR_IN, FEAR_OUT = 80, 60, 20, 40
NORMAL, GREED, FEAR = 0, 1, -1
STATE_ZH = {NORMAL: "普通", GREED: "貪婪", FEAR: "恐懼"}
STATE_KEY = {NORMAL: "normal", GREED: "greed", FEAR: "fear"}
STALE_DAYS = 45

START_FRIDAY = {"us": "2001-01-26", "tw": "2009-01-02"}
UA = {"User-Agent": "Mozilla/5.0 (InvestMQuest weekly reminder; polite)"}


# ---------------------------------------------------------------------------
# 滾動百分位與狀態機（同 thermo.py）
# ---------------------------------------------------------------------------
def rolling_pct(s: pd.Series, window: int, min_obs: int) -> pd.Series:
    s = s.dropna()
    v = s.to_numpy(dtype=float)
    out = np.full(len(v), np.nan)
    for i in range(len(v)):
        if i + 1 < min_obs:
            continue
        w = v[max(0, i + 1 - window): i + 1]
        out[i] = 100.0 * float((w <= v[i]).sum()) / len(w)
    return pd.Series(out, index=s.index)


def _month_end_avail(idx: pd.DatetimeIndex, lag_months: int = 1) -> pd.DatetimeIndex:
    return (idx + pd.offsets.MonthEnd(0) + pd.offsets.MonthEnd(lag_months)).normalize()


def step_state(st: int, sc: int) -> int:
    """單步遲滯狀態機（整數比較）。"""
    if st == GREED:
        if sc <= GREED_OUT:
            st = NORMAL
            if sc <= FEAR_IN:
                st = FEAR
    elif st == FEAR:
        if sc >= FEAR_OUT:
            st = NORMAL
            if sc >= GREED_IN:
                st = GREED
    else:
        if sc >= GREED_IN:
            st = GREED
        elif sc <= FEAR_IN:
            st = FEAR
    return st


# ---------------------------------------------------------------------------
# 材料載入（從 docs/fear-greed/data/raw/*.csv）
# ---------------------------------------------------------------------------
def _read_dated(name: str, col: str = "value") -> pd.Series:
    d = pd.read_csv(RAW / name, parse_dates=["date"]).set_index("date")[col]
    return d.astype(float).dropna().sort_index()


def load_vix() -> pd.Series:
    return _read_dated("vix.csv")


def load_baa10y() -> pd.Series:
    return _read_dated("baa10y.csv")


def load_cape() -> pd.Series:
    x = pd.read_csv(RAW / "cape.csv")
    idx = pd.to_datetime(dict(year=x["year"], month=x["month"], day=1)) + pd.offsets.MonthEnd(0)
    s = pd.Series(x["cape"].to_numpy(dtype=float), index=idx).dropna()
    s.index = _month_end_avail(s.index, 1)          # 月資料，次月月底起可用
    return s


def load_finra_margin_yoy() -> pd.Series:
    d = _read_dated("finra_margin.csv")
    d.index = d.index + pd.offsets.MonthEnd(0)
    yoy = ((d / d.shift(12) - 1.0) * 100.0).dropna()
    yoy.index = _month_end_avail(yoy.index, 1)      # FINRA 次月下旬公布 → 次月月底起可用
    return yoy


def load_tw_pcr() -> pd.Series:
    d = pd.read_csv(RAW / "tw_pcr.csv", parse_dates=["日期"]).set_index("日期").sort_index()
    return d["買賣權未平倉量比率%"].astype(float).rolling(20, min_periods=15).mean().dropna()


def _monthly_last(s: pd.Series):
    per = s.index.to_period("M")
    val = s.groupby(per).last()
    dt = pd.Series(s.index, index=s.index).groupby(per).last()
    return val, dt


def load_tw_margin_yoy() -> pd.Series:
    s = _read_dated("tw_margin.csv")
    val, dt = _monthly_last(s)
    prev = val.reindex(val.index - 12)
    yoy = pd.Series((val.to_numpy() / prev.to_numpy() - 1.0) * 100.0, index=pd.DatetimeIndex(dt.values))
    return yoy.dropna()


def load_tw_median_pbr() -> pd.Series:
    s = _read_dated("tw_pbr.csv")
    val, dt = _monthly_last(s)
    return pd.Series(val.to_numpy(), index=pd.DatetimeIndex(dt.values))


# name -> (loader, 方向 +1 越高越貪婪／-1 越低越貪婪, 窗, 最少觀察數, 顯示名, 單位格式)
US_MATERIALS = {
    "VIX": (load_vix, -1, 2520, 1260, "VIX 波動率指數（越低越貪婪）", "{:.1f}"),
    "BAA10Y": (load_baa10y, -1, 2520, 1260, "Baa 公司債對 10 年公債利差（越窄越貪婪）", "{:.2f} 個百分點"),
    "CAPE": (load_cape, +1, 120, 60, "席勒本益比 CAPE（越高越貪婪）", "{:.1f} 倍"),
    "MARGIN_YOY": (load_finra_margin_yoy, +1, 120, 60, "FINRA 融資餘額年增率（越高越貪婪）", "{:+.1f}%"),
}
TW_MATERIALS = {
    "PCR_OI20": (load_tw_pcr, -1, 2520, 1260, "選擇權賣買權未平倉比，20 日均（越低越貪婪）", "{:.1f}%"),
    "MARGIN_YOY": (load_tw_margin_yoy, +1, 120, 60, "TWSE 融資餘額年增率（越高越貪婪）", "{:+.1f}%"),
    "MEDIAN_PBR": (load_tw_median_pbr, +1, 120, 60, "上市個股股價淨值比中位數（越高越貪婪）", "{:.2f} 倍"),
}
REG = {"us": US_MATERIALS, "tw": TW_MATERIALS}
MARKET_ZH = {"us": "美股", "tw": "台股"}


def compute_materials(market: str):
    """回傳 {name: (raw 原始值序列, pct 貪婪百分位序列)}；index 皆為「可用日」。"""
    out = {}
    for name, (loader, sign, win, mn, _lbl, _fmt) in REG[market].items():
        raw = loader()
        out[name] = (raw, rolling_pct(raw * sign, win, mn))
    return out


def _asof(s: pd.Series, fridays: pd.DatetimeIndex):
    """每個週五取 ≤ 該日最後一筆；回傳（值, 該筆日期）。"""
    u = s.index.union(fridays)
    val = s.reindex(u).ffill().reindex(fridays)
    obs = pd.Series(s.index, index=s.index).reindex(u).ffill().reindex(fridays)
    return val, pd.DatetimeIndex(obs.values)


def weekly_tables(mats: dict, fridays: pd.DatetimeIndex):
    """每週五的各材料（百分位, 原始值, 資料日）；超過 45 天沒更新的材料該週視為缺值。"""
    pct, raw, asof = {}, {}, {}
    for k, (r, p) in mats.items():
        pv, pd_ = _asof(p, fridays)
        rv, _ = _asof(r, fridays)
        stale = (fridays - pd_).days > STALE_DAYS
        pv[stale] = np.nan
        pct[k], raw[k], asof[k] = pv, rv, pd_
    return pd.DataFrame(pct), pd.DataFrame(raw), pd.DataFrame(asof, index=fridays)


def score_from_pct(panel: pd.DataFrame, min_materials: int) -> pd.Series:
    n = panel.notna().sum(axis=1)
    m = panel.mean(axis=1, skipna=True)
    sc = np.floor(m + 0.5)
    sc[n < min_materials] = np.nan
    return sc


def run_weeks(market: str, mats: dict, fridays: pd.DatetimeIndex, st0: int) -> pd.DataFrame:
    """對 fridays 逐週算分數與狀態（從 st0 接續）。"""
    pct, raw, asof = weekly_tables(mats, fridays)
    n = len(REG[market])
    score = score_from_pct(pct, max(1, n - 1))
    st, states = st0, []
    for x in score.to_numpy():
        if not np.isnan(x):
            st = step_state(st, int(x))
        states.append(st)
    out = pct.copy()
    out["score"] = score
    out["state"] = states
    return out


# ---------------------------------------------------------------------------
# 抓取
# ---------------------------------------------------------------------------
def http_get(url: str, data: bytes | None = None, tries: int = 3, timeout: int = 60, headers: dict | None = None) -> bytes:
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as ex:
            last = ex
            if k < tries - 1:
                time.sleep(3 * (k + 1))
    raise RuntimeError(f"GET failed: {url[:80]} ({type(last).__name__})")


def _merge_csv(path: Path, new: pd.DataFrame, key: str | list[str]) -> int:
    """把 new 併進既有 csv（以 key 去重、新值覆蓋），回傳新增列數。"""
    old = pd.read_csv(path)
    n0 = len(old)
    both = pd.concat([old, new[old.columns]], ignore_index=True)
    both = both.drop_duplicates(key, keep="last").sort_values(key).reset_index(drop=True)
    both.to_csv(path, index=False)
    return len(both) - n0


def fetch_fred(series_id: str, fname: str, today: date) -> int:
    path = RAW / fname
    last = pd.read_csv(path, parse_dates=["date"])["date"].max()
    cosd = (last - pd.Timedelta(days=45)).strftime("%Y-%m-%d")
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={cosd}"
    df = pd.read_csv(io.BytesIO(http_get(url)))
    df.columns = ["date", "value"]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna()
    if df.empty:
        raise RuntimeError("FRED 回空表")
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    old = pd.read_csv(path)
    old["date"] = pd.to_datetime(old["date"]).dt.strftime("%Y-%m-%d")
    old.to_csv(path, index=False)
    return _merge_csv(path, df, "date")


def fetch_finra() -> int:
    url = "https://www.finra.org/sites/default/files/2021-03/margin-statistics.xlsx"
    book = pd.read_excel(io.BytesIO(http_get(url)), sheet_name=None, header=None)
    df = next(iter(book.values()))
    rows = []
    for i in range(len(df)):
        k = str(df.iloc[i, 0]).strip()
        if re.fullmatch(r"\d{4}-\d{2}", k):
            v = pd.to_numeric(df.iloc[i, 1], errors="coerce")
            if v == v:
                rows.append((k + "-01", float(v)))
    if not rows:
        raise RuntimeError("FINRA 解析不到資料列")
    return _merge_csv(RAW / "finra_margin.csv", pd.DataFrame(rows, columns=["date", "value"]), "date")


def fetch_cape() -> int:
    page = http_get("https://shillerdata.com/").decode("utf8", "replace")
    m = re.search(r'href="((?:https:)?//[^"]*ie_data\.xls[^"]*)"', page)
    if not m:
        raise RuntimeError("shillerdata.com 找不到 ie_data.xls 連結")
    link = m.group(1)
    if link.startswith("//"):
        link = "https:" + link
    df = pd.read_excel(io.BytesIO(http_get(link, timeout=120)), sheet_name="Data", header=None)
    rows = []
    for i in range(8, len(df)):
        d = pd.to_numeric(df.iloc[i, 0], errors="coerce")
        c = pd.to_numeric(df.iloc[i, 12], errors="coerce")
        if d != d or c != c:
            continue
        y = int(d)
        mth = int(round((d - y) * 100))     # 2026.1 = 2026 年 10 月
        if 1 <= mth <= 12:
            rows.append((y, mth, float(c)))
    if not rows:
        raise RuntimeError("Shiller 解析不到 CAPE")
    return _merge_csv(RAW / "cape.csv", pd.DataFrame(rows, columns=["year", "month", "cape"]), ["year", "month"])


def fetch_tw_pcr(today: date) -> int:
    path = RAW / "tw_pcr.csv"
    old = pd.read_csv(path)
    last = pd.to_datetime(old["日期"]).max().date()
    if last >= today - timedelta(days=3):
        return 0
    s = last + timedelta(days=1)
    frames = []
    while s <= today:
        e = min(s + timedelta(days=30), today)
        body = urllib.parse.urlencode({"queryStartDate": s.strftime("%Y/%m/%d"), "queryEndDate": e.strftime("%Y/%m/%d")}).encode()
        raw = http_get("https://www.taifex.com.tw/cht/3/pcRatioDown", data=body,
                       headers={"Referer": "https://www.taifex.com.tw/cht/3/pcRatioDown",
                                "Content-Type": "application/x-www-form-urlencoded"})
        if raw[:9] != b"<!DOCTYPE" and len(raw) > 50:
            df = pd.read_csv(io.BytesIO(raw), encoding="cp950", index_col=False)
            df.columns = [c.strip() for c in df.columns]
            frames.append(df)
        s = e + timedelta(days=1)
        time.sleep(0.6)
    if not frames:
        return 0
    new = pd.concat(frames, ignore_index=True)
    new["日期"] = pd.to_datetime(new["日期"]).dt.strftime("%Y-%m-%d")
    return _merge_csv(path, new, "日期")


TWSE_URL = {
    "margin": "https://www.twse.com.tw/rwd/zh/marginTrading/MI_MARGN?date={d}&selectType=MS&response=json",
    "pe": "https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?date={d}&selectType=ALL&response=json",
}
TWSE_SLEEP = 4.0


class TwseBlocked(RuntimeError):
    pass


def _twse_json(url: str):
    """回傳 dict；連線或非 JSON（被封鎖）→ 重試 2 次後丟 TwseBlocked。"""
    for k in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf8"))
        except Exception:
            time.sleep(15 * (k + 1))
    raise TwseBlocked("TWSE 無回應或回非 JSON（疑被封鎖）")


def _last_friday(y: int, m: int) -> date:
    d = date(y, m, monthrange(y, m)[1])
    while d.weekday() != 4:
        d -= timedelta(days=1)
    return d


def _twse_value(ep: str, js: dict):
    if ep == "margin":
        for t in js.get("tables", []):
            for r in t.get("data", []):
                if str(r[0]).startswith("融資金額"):
                    return float(str(r[5]).replace(",", ""))
        return None
    fields = js.get("fields") or []
    if "股價淨值比" not in fields:
        return None
    i = fields.index("股價淨值比")
    vals = []
    for r in js.get("data", []):
        try:
            v = float(str(r[i]).replace(",", ""))
        except ValueError:
            continue
        if v > 0:
            vals.append(v)
    return float(np.median(vals)) if len(vals) > 300 else None


def fetch_twse(ep: str, today: date) -> int:
    """補上缺的月份：每月只抓「最後一個週五所在週的最後交易日」。月底尚未到的月份不抓。"""
    path = RAW / ("tw_margin.csv" if ep == "margin" else "tw_pbr.csv")
    old = pd.read_csv(path, parse_dates=["date"])
    last_month = old["date"].max().to_period("M")
    cur = pd.Period(today, "M")
    added = []
    m = last_month + 1
    while m <= cur:
        fri = _last_friday(m.year, m.month)
        if fri > today - timedelta(days=1):         # 月底那週還沒收完
            break
        got = None
        for week_back in (0, 7):                    # 該週整週休市（農曆年）→ 退一週
            f = fri - timedelta(days=week_back)
            for back in range(5):
                d = f - timedelta(days=back)
                if d.weekday() > 4:
                    continue
                js = _twse_json(TWSE_URL[ep].format(d=f"{d:%Y%m%d}"))
                time.sleep(TWSE_SLEEP)
                if js.get("stat") == "OK":
                    v = _twse_value(ep, js)
                    if v is not None:
                        got = (d, v)
                        break
            if got:
                break
        if got:
            added.append((got[0].strftime("%Y-%m-%d"), got[1]))
        m += 1
    if not added:
        return 0
    return _merge_csv(path, pd.DataFrame(added, columns=["date", "value"]), "date")


def run_fetch(today: date) -> dict:
    jobs = [
        ("vix", lambda: fetch_fred("VIXCLS", "vix.csv", today)),
        ("baa10y", lambda: fetch_fred("BAA10Y", "baa10y.csv", today)),
        ("cape", fetch_cape),
        ("finra_margin", fetch_finra),
        ("tw_pcr", lambda: fetch_tw_pcr(today)),
        ("tw_margin", lambda: fetch_twse("margin", today)),
        ("tw_pbr", lambda: fetch_twse("pe", today)),
    ]
    status = {}
    for name, fn in jobs:
        try:
            status[name] = {"ok": True, "added": int(fn())}
        except Exception as ex:  # noqa: BLE001 — 任何失敗都不中斷，沿用上期資料
            status[name] = {"ok": False, "error": f"{type(ex).__name__}: {str(ex)[:120]}"}
        print(f"fetch {name}: {status[name]}", flush=True)
    return status


# ---------------------------------------------------------------------------
# 歷史與最新
# ---------------------------------------------------------------------------
def hist_path(market: str) -> Path:
    return DATA / f"history_{market}.csv"


def read_history(market: str) -> pd.DataFrame:
    return pd.read_csv(hist_path(market), index_col=0, parse_dates=True)


def target_friday(today: date) -> pd.Timestamp:
    """台北今天的前一天往回找最近的週五（週六早上跑 → 昨天的週五；週五當天跑 → 上一個週五）。"""
    d = today - timedelta(days=1)
    d -= timedelta(days=(d.weekday() - 4) % 7)
    return pd.Timestamp(d)


def update_history(market: str, mats: dict, target: pd.Timestamp, rebuild: bool):
    """回傳（history 全表, 本次新增的列數, 接續前最後一列的狀態）。"""
    path = hist_path(market)
    if rebuild or not path.exists():
        fr = pd.date_range(START_FRIDAY[market], target, freq="W-FRI")
        new = run_weeks(market, mats, fr, NORMAL)
        new.index.name = "date"
        new.to_csv(path)
        return new, len(new), None
    hist = read_history(market)
    prev_state = int(hist["state"].iloc[-1])
    fr = pd.date_range(hist.index[-1] + pd.Timedelta(days=7), target, freq="W-FRI")
    if len(fr) == 0:
        return hist, 0, prev_state
    new = run_weeks(market, mats, fr, prev_state)
    new = new[hist.columns]
    full = pd.concat([hist, new])
    full.index.name = "date"
    full.to_csv(path)
    return full, len(new), prev_state


def spells(state: pd.Series, score: pd.Series, which: int) -> list[dict]:
    out, start, prev, vals = [], None, None, []
    for d, s in state.items():
        if s == which:
            if start is None:
                start, vals = d, []
            vals.append(score.get(d))
        elif start is not None:
            out.append({"start": start, "end": prev, "weeks": len(vals), "min": float(np.nanmin(vals)) if vals else None, "open": False})
            start = None
        prev = d
    if start is not None:
        out.append({"start": start, "end": prev, "weeks": len(vals), "min": float(np.nanmin(vals)) if vals else None, "open": True})
    return out


def fmt_raw(market: str, name: str, v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return REG[market][name][5].format(v)


def build_market_block(market: str, hist: pd.DataFrame, mats: dict, target: pd.Timestamp, n_new: int, prev_run_state) -> dict:
    last = hist.iloc[-1]
    fr = pd.DatetimeIndex([hist.index[-1]])
    pct, raw, asof = weekly_tables(mats, fr)
    materials = {}
    for k in REG[market]:
        p = pct[k].iloc[0]
        age = (fr[0] - asof[k].iloc[0]).days if pd.notna(asof[k].iloc[0]) else None
        materials[k] = {
            "label": REG[market][k][4],
            "pct": None if pd.isna(p) else int(round(float(p))),
            "raw": None if pd.isna(raw[k].iloc[0]) else round(float(raw[k].iloc[0]), 4),
            "raw_text": fmt_raw(market, k, raw[k].iloc[0]),
            "asof": None if pd.isna(asof[k].iloc[0]) else asof[k].iloc[0].strftime("%Y-%m-%d"),
            "age_days": age,
            "stale": bool(age is not None and age > STALE_DAYS),
        }
    state = int(last["state"])
    prev_state = int(hist["state"].iloc[-2]) if len(hist) > 1 else NORMAL
    prev_score = None if len(hist) < 2 or pd.isna(hist["score"].iloc[-2]) else int(hist["score"].iloc[-2])
    # 本狀態從哪一週開始
    k = len(hist) - 1
    while k > 0 and int(hist["state"].iloc[k - 1]) == state:
        k -= 1
    since = hist.index[k]
    return {
        "week": hist.index[-1].strftime("%Y-%m-%d"),
        "score": None if pd.isna(last["score"]) else int(last["score"]),
        "state": STATE_KEY[state],
        "state_code": state,
        "state_zh": STATE_ZH[state],
        "prev_score": prev_score,
        "prev_state": STATE_KEY[prev_state],
        "changed_vs_prev_week": state != prev_state,
        "since": since.strftime("%Y-%m-%d"),
        "weeks_in_state": int(len(hist) - k),
        "n_materials_used": int(sum(1 for m in materials.values() if m["pct"] is not None)),
        "materials": materials,
        "reference_only": market == "tw",
        "new_weeks_this_run": n_new,
        "state_before_this_run": None if prev_run_state is None else STATE_KEY[prev_run_state],
    }


# ---------------------------------------------------------------------------
# 通知檔
# ---------------------------------------------------------------------------
REMIND = "長期加碼提醒：去看 30% 個股與現金部位，不是買進訊號；不影響 70% W52 引擎。"
GREED_NOTE = "僅供參考，不作操作。"
TW_NOTE = "台股材料歷史較短（分數最早從 2013 年底才有，材料至少要 5 年資料），僅供參考。"


def _change_phrase(market: str, old: str, new: str) -> str:
    z = MARKET_ZH[market]
    if new == "fear":
        return f"{z}進入恐懼區"
    if old == "fear":
        return f"{z}離開恐懼區"
    if new == "greed":
        return f"{z}進入貪婪區"
    if old == "greed":
        return f"{z}離開貪婪區"
    return f"{z}狀態改變"


def build_alerts(latest: dict, test: bool = False) -> list[dict]:
    alerts = []
    for market in ("us", "tw"):
        b = latest[market]
        old, new = b["state_before_this_run"], b["state"]
        if test:
            old = new
            phrase = f"{MARKET_ZH[market]}目前為{b['state_zh']}區"
        elif old is None or old == new or b["new_weeks_this_run"] == 0:
            continue
        else:
            phrase = _change_phrase(market, old, new)
        alerts.append({"market": market, "old": old, "new": new, "phrase": phrase, "block": b})
    return alerts


def alert_text(alerts: list[dict]) -> tuple[str, str]:
    title = "市場溫度：" + "；".join(f"{a['phrase']}（{a['block']['score']} 分）" for a in alerts)
    key_code = {"normal": 0, "greed": 1, "fear": -1}
    lines = []
    for a in alerts:
        b = a["block"]
        head = f"{a['phrase']}。{b['score']} 分"
        if b["prev_score"] is not None:
            head += f"（上週 {b['prev_score']} 分）"
        if a["old"] != a["new"]:
            head += f"，狀態 {STATE_ZH[key_code[a['old']]]} → {b['state_zh']}"
        lines.append(head + f"，資料週 {b['week']}。")
        lines.append("各材料貪婪百分位（0＝10 年來最恐懼，100＝最貪婪）：")
        for m in b["materials"].values():
            p = "停更" if m["pct"] is None else str(m["pct"])
            lines.append(f"・{m['label'].split('（')[0]}：{p}（目前 {m['raw_text']}）")
        fear_related = "fear" in (a["old"], a["new"])
        lines.append(REMIND if fear_related else GREED_NOTE)
        if a["market"] == "tw":
            lines.append(TW_NOTE)
        lines.append("")
    lines.append(f"完整頁面：{PAGE_URL}")
    return title, "\n".join(lines)


def alert_mail_html(title: str, body: str) -> str:
    esc = html.escape
    paras = "".join(f'<p style="margin:0 0 10px 0;">{esc(l)}</p>' if l else "" for l in body.split("\n"))
    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title></head>
<body style="margin:0;padding:0;background-color:#f6f5f2;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f6f5f2;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background-color:#ffffff;border:1px solid #e6e2d8;border-radius:8px;font-family:-apple-system,'PingFang TC','Noto Sans TC','Segoe UI',sans-serif;">
<tr><td style="background-color:#0f1f3d;color:#ffffff;padding:18px 24px;font-size:16px;font-weight:700;">{esc(title)}</td></tr>
<tr><td style="padding:18px 24px;font-size:14px;line-height:1.7;color:#1c1c1c;">{paras}</td></tr>
<tr><td style="padding:0 24px 22px 24px;text-align:center;"><a href="{PAGE_URL}" style="display:inline-block;background-color:#0f1f3d;color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 28px;border-radius:6px;">查看市場溫度頁</a></td></tr>
<tr><td style="padding:0 24px 20px 24px;font-size:12px;color:#6b6b6b;text-align:center;">InvestMQuest · 市場溫度計每週提醒（只在狀態改變時寄出）</td></tr>
</table></td></tr></table></body></html>
"""


def write_alert_files(alerts: list[dict]) -> None:
    title, body = alert_text(alerts)
    (ROOT / "fg_title.txt").write_text(title + "\n", encoding="utf-8")
    (ROOT / "fg_alert.txt").write_text(body + "\n", encoding="utf-8")
    (ROOT / "fg_mail.html").write_text(alert_mail_html(title, body), encoding="utf-8")
    print("ALERT:", title)


# ---------------------------------------------------------------------------
# 頁面
# ---------------------------------------------------------------------------
# 美股歷次恐懼區間之後的納斯達克 100 價格指數表現（不含股息；^NDX 收盤，取自 v7-backtest 原始檔）。
# 進入週收盤 → 52 週後報酬；進入後 18 個月內最低收盤相對進入週的跌幅。新出現的區間沒有這兩欄，顯示「—」。
NDX_AFTER_FEAR = {
    "2001-09-21": (-22.7, -28.6),
    "2002-07-05": (16.1, -24.2),
    "2008-03-07": (-37.6, -39.3),
    "2011-11-18": (12.4, -4.6),
    "2020-05-01": (59.0, 0.0),
}
STATE_COLOR = {"fear": "#2563eb", "normal": "#6b7280", "greed": "#d97706"}


def _svg_chart(hist: pd.DataFrame, start: str, label_id: str) -> str:
    h = hist.loc[start:]
    if h.empty:
        return ""
    W, H, L, R, T, B = 800, 230, 34, 10, 10, 24
    x0, x1 = h.index[0].value, h.index[-1].value
    px = lambda d: L + (d.value - x0) / max(1, x1 - x0) * (W - L - R)          # noqa: E731
    py = lambda v: T + (100 - v) / 100 * (H - T - B)                            # noqa: E731
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="{label_id}" style="width:100%;height:auto;display:block">']
    for sp, col in ((FEAR, "#2563eb"), (GREED, "#d97706")):
        for s in spells(h["state"], h["score"], sp):
            xa = px(s["start"])
            xb = px(s["end"]) + 3
            parts.append(f'<rect x="{xa:.1f}" y="{T}" width="{max(2, xb - xa):.1f}" height="{H - T - B}" fill="{col}" opacity="0.13"/>')
    for v in (20, 40, 60, 80):
        parts.append(f'<line x1="{L}" x2="{W - R}" y1="{py(v):.1f}" y2="{py(v):.1f}" stroke="#d1d5db" stroke-width="1" stroke-dasharray="{"" if v in (20, 80) else "3 3"}"/>')
        parts.append(f'<text x="{L - 5}" y="{py(v) + 4:.1f}" text-anchor="end" font-size="10" fill="#6b7280">{v}</text>')
    pts = " ".join(f"{px(d):.1f},{py(v):.1f}" for d, v in h["score"].dropna().items())
    parts.append(f'<polyline points="{pts}" fill="none" stroke="#111827" stroke-width="1.6" stroke-linejoin="round"/>')
    yr0, yr1 = h.index[0].year, h.index[-1].year
    step = 2 if yr1 - yr0 > 12 else 1
    for y in range(yr0 + (yr0 % step), yr1 + 1, step):
        xx = px(pd.Timestamp(f"{y}-01-01")) if pd.Timestamp(f"{y}-01-01") > h.index[0] else L
        parts.append(f'<text x="{xx:.1f}" y="{H - 7}" text-anchor="middle" font-size="10" fill="#6b7280">{y}</text>')
    parts.append("</svg>")
    return "".join(parts)


def _materials_rows(block: dict) -> str:
    rows = []
    for m in block["materials"].values():
        p = "停更" if m["pct"] is None else str(m["pct"])
        note = ""
        if m["stale"]:
            note = f' <span style="color:#b45309">（資料已 {m["age_days"]} 天未更新，本週不計入）</span>'
        rows.append(f'<tr><td>{html.escape(m["label"])}</td><td class="num">{html.escape(m["raw_text"])}</td>'
                    f'<td class="num"><b>{p}</b></td><td class="num">{m["asof"] or "—"}{note}</td></tr>')
    return "".join(rows)


def _market_card(market: str, block: dict) -> str:
    z = MARKET_ZH[market]
    col = STATE_COLOR[block["state"]]
    score = "—" if block["score"] is None else block["score"]
    ref = '<span class="tag-ref">參考，歷史短</span>' if block["reference_only"] else ""
    since = f'自 {block["since"]} 起，已 {block["weeks_in_state"]} 週'
    chg = ""
    if block["prev_score"] is not None:
        chg = f'上週 {block["prev_score"]} 分'
    return f"""<div class="card">
  <div class="mk-head"><h3>{z}</h3>{ref}</div>
  <div class="score-row"><span class="score" style="color:{col}">{score}</span><span class="unit">分</span>
    <span class="pill" style="background:{col}">{block["state_zh"]}</span></div>
  <div class="fine">{since}；{chg}；資料週 {block["week"]}</div>
  <div class="tbl-wrap"><table><thead><tr><th>材料</th><th class="num">目前值</th><th class="num">貪婪百分位</th><th class="num">資料日</th></tr></thead>
  <tbody>{_materials_rows(block)}</tbody></table></div>
</div>"""


def _fear_table(market: str, hist: pd.DataFrame) -> str:
    sp = spells(hist["state"], hist["score"], FEAR)
    if not sp:
        return "<p class='fine'>尚無進入恐懼區的紀錄。</p>"
    us = market == "us"
    head = "<tr><th>進入週</th><th>離開週</th><th class='num'>持續週數</th><th class='num'>最低分</th>"
    if us:
        head += "<th class='num'>進入後 52 週<br>NDX 報酬</th><th class='num'>進入後 18 個月內<br>最深再跌</th>"
    head += "</tr>"
    rows = []
    for s in sp:
        a = s["start"].strftime("%Y-%m-%d")
        b = "仍在恐懼區" if s["open"] else s["end"].strftime("%Y-%m-%d")
        r = f"<tr><td>{a}</td><td>{b}</td><td class='num'>{s['weeks']}</td><td class='num'>{int(s['min'])}</td>"
        if us:
            ndx = NDX_AFTER_FEAR.get(a)
            r += (f"<td class='num'>{ndx[0]:+.1f}%</td><td class='num'>{ndx[1]:.1f}%</td>" if ndx
                  else "<td class='num'>—</td><td class='num'>—</td>")
        rows.append(r + "</tr>")
    return f"<div class='tbl-wrap'><table><thead>{head}</thead><tbody>{''.join(rows)}</tbody></table></div>"


def build_page(latest: dict, hist: dict) -> str:
    sys.path.insert(0, str(HERE))
    from site_nav import full_nav_block  # noqa: E402

    nav = full_nav_block("system", "lthub")
    us, tw = latest["us"], latest["tw"]
    stale_msgs = [f"{k}（{v['error']}）" for k, v in latest["fetch"].items() if not v.get("ok")]
    stale_html = ""
    if stale_msgs:
        stale_html = ('<div class="warn">本週有材料抓取失敗，沿用上期資料：'
                      + html.escape("、".join(stale_msgs)) + "。</div>")
    h_us = hist["us"]
    min22 = h_us.loc["2022", "score"]
    min22_s = f'{int(min22.min())} 分（{min22.idxmin():%Y-%m}）'
    chart_us = _svg_chart(h_us, "2001-01-01", "cus")
    tw_first = hist["tw"]["score"].first_valid_index()
    chart_tw = _svg_chart(hist["tw"], tw_first.strftime("%Y-%m-%d"), "ctw")
    n_tw_fear = len(spells(hist["tw"]["state"], hist["tw"]["score"], FEAR))
    gen = latest["generated"]
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>市場溫度計：貪婪與恐懼 | InvestMQuest</title>
<style>
:root{{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;--text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-text:#92400e;--blue:#2563eb}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans TC',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:15px}}
a{{color:var(--brand);text-decoration:none}}a:hover{{text-decoration:underline}}
.container{{max-width:1080px;margin:0 auto;padding:0 1.5rem}}
.page-hdr{{padding:1.6rem 0 1.1rem;background:linear-gradient(180deg,#eff6ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}}
.page-hdr h1{{font-size:1.5rem;font-weight:700;letter-spacing:-.03em}}
.page-hdr .sub{{color:var(--muted);font-size:.9rem;margin-top:.25rem;max-width:76ch}}
.crumb{{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}}.crumb a{{color:var(--muted)}}
.remind{{background:var(--amber-bg);border:2px solid var(--amber);border-radius:10px;padding:.9rem 1.15rem;margin:1.1rem 0 .4rem;font-size:.93rem;color:var(--amber-text)}}
.warn{{background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:.6rem .9rem;margin:.8rem 0;font-size:.86rem;color:#991b1b}}
.section{{padding:1.6rem 0 0}}
.section-title{{font-size:1.15rem;font-weight:700;margin-bottom:.9rem;padding-bottom:.45rem;border-bottom:2px solid var(--brand)}}
.cards2{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
@media(max-width:820px){{.cards2{{grid-template-columns:1fr}}}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.1rem 1.2rem;margin-bottom:1rem}}
.card h3{{font-size:1.02rem;font-weight:600}}
.mk-head{{display:flex;align-items:center;gap:.6rem;margin-bottom:.4rem}}
.tag-ref{{font-size:.72rem;font-weight:700;color:#92400e;background:#fef3c7;border-radius:6px;padding:.1rem .5rem}}
.score-row{{display:flex;align-items:baseline;gap:.4rem;margin:.2rem 0 .3rem}}
.score{{font-size:2.8rem;font-weight:800;line-height:1;font-variant-numeric:tabular-nums}}
.unit{{color:var(--muted);font-size:.95rem}}
.pill{{color:#fff;font-weight:700;font-size:.85rem;border-radius:999px;padding:.1rem .8rem;margin-left:.4rem}}
.fine{{font-size:.82rem;color:var(--muted);margin:.35rem 0 .7rem;line-height:1.7}}
table{{width:100%;border-collapse:collapse;font-size:.84rem}}
th,td{{text-align:left;padding:.45rem .6rem;border-bottom:1px solid var(--border);vertical-align:top}}
th{{background:#f9fafb;font-weight:600;font-size:.74rem;color:var(--muted)}}
td.num,th.num{{text-align:right;font-variant-numeric:tabular-nums}}
.tbl-wrap{{overflow-x:auto}}
.prose{{font-size:.92rem;max-width:80ch}}.prose p{{margin-bottom:.7rem}}
.prose ul{{margin:.2rem 0 .8rem 1.2rem}}.prose li{{margin-bottom:.25rem}}
.legend{{font-size:.78rem;color:var(--muted);margin-top:.3rem}}
.legend i{{display:inline-block;width:.9rem;height:.7rem;border-radius:2px;vertical-align:-1px;margin:0 .25rem 0 .6rem;opacity:.5}}
footer{{padding:2rem 0 3rem;font-size:.8rem;color:var(--muted)}}
</style>
</head>
<body>
{nav}
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / <a href="/long-track/">追蹤總覽</a> / 市場溫度計</div>
  <h1>市場溫度計：貪婪與恐懼</h1>
  <div class="sub">每週五收盤後更新。美股用 4 項材料、台股用 3 項材料，各自換算成過去 10 年的百分位後取平均，得到 0 到 100 分。</div>
</div></div>
<div class="container">
<div class="remind"><b>這是提醒你去看的訊號，不是買進訊號。</b>分數進入恐懼區時，請回頭檢視 30% 個股與現金部位。它不影響 70% 指數部的 W52 引擎，也不改動 long-track 的任何計算。</div>
{stale_html}

<div class="section"><div class="section-title">本週讀數（資料週 {us["week"]}）</div>
<div class="cards2">
{_market_card("us", us)}
{_market_card("tw", tw)}
</div>
<div class="fine">貪婪百分位：0 代表該材料處在過去 10 年最恐懼的水準，100 代表最貪婪。VIX 與利差越低越貪婪，所以 VIX 在 10 年最低檔時，百分位是 100。月資料（CAPE、融資、台股融資與股價淨值比）按公布後的可用日計入，超過 45 天沒更新的材料該週不計入。</div>
</div>

<div class="section"><div class="section-title">分數怎麼分區</div>
<div class="prose"><ul>
<li><b>恐懼</b>：分數降到 20 以下進入，回到 40 以上才離開。</li>
<li><b>貪婪</b>：分數升到 80 以上進入，回到 60 以下才離開。</li>
<li><b>普通</b>：其餘情況。進出門檻不同，是為了避免分數在邊界上來回跳動。</li>
</ul></div></div>

<div class="section"><div class="section-title">美股分數走勢（2001 年起）</div>
<span id="cus" style="display:none">美股溫度計每週分數與恐懼、貪婪區間</span>
{chart_us}
<div class="legend"><i style="background:#2563eb"></i>恐懼區<i style="background:#d97706"></i>貪婪區　虛線為 20／80（進入），點線為 40／60（離開）</div>
</div>

<div class="section"><div class="section-title">美股歷次進入恐懼區</div>
{_fear_table("us", h_us)}
<div class="prose" style="margin-top:.8rem">
<p>進入恐懼區的時點不等於底部。2001-09、2002-07 與 2008-03 進入後，納斯達克 100 還各自再跌了 24% 至 39%；2011-11 與 2020-05 進入時，低點已經過去。所以它只能提醒你去看，不能用來抓底。</p>
<p>2022 年沒有觸發：全年分數最低是 {min22_s}，沒有降到 20 的進入門檻。</p>
<p class="fine">NDX 為納斯達克 100 價格指數，不含股息；52 週報酬與最深再跌皆以進入週收盤為基準。</p>
</div></div>

<div class="section"><div class="section-title">台股分數走勢與恐懼區（參考）</div>
{chart_tw}
<div class="legend"><i style="background:#2563eb"></i>恐懼區<i style="background:#d97706"></i>貪婪區</div>
<div style="margin-top:.8rem">{_fear_table("tw", hist["tw"])}</div>
<div class="prose" style="margin-top:.8rem"><p>台股的選擇權、融資與股價淨值比資料較短，材料至少要 5 年資料才算得出百分位，分數最早從 {tw_first:%Y 年 %-m 月}才有，至今只經歷 {n_tw_fear} 次恐懼區，樣本太少，只標為參考。</p></div>
</div>

<div class="section"><div class="section-title">研究結論與用途</div>
<div class="prose">
<p>這個溫度計拿來調引擎槓桿沒有用。研究的做法是：進入貪婪區就把槓桿上限由 1.5 降到 1.0。美股與台股的最大回撤都沒有改善（改善 0.0 個百分點，事前訂的驗收是至少 3 個百分點），所以引擎不使用它。</p>
<p>保留下來的用途只有一個：進入恐懼區時，提醒你回頭看 30% 個股與現金部位，考慮長期加碼。進入與離開貪婪區也會通知，但僅供參考，不作操作。通知只在狀態改變時寄出，不寄每週例行信。</p>
<p class="fine">研究規格與結果見 v7-backtest 的 FearGreed_Cap_Spec。美股材料：VIX、Baa 對 10 年公債利差（FRED）、席勒 CAPE、FINRA 融資餘額年增率。台股材料：期交所選擇權賣買權未平倉比、TWSE 融資餘額年增率、上市個股股價淨值比中位數（個股中位數，不是市值加權）。</p>
</div></div>

<footer>最後更新 {gen}（台北時間）。資料檔：<a href="/fear-greed/data/latest.json">latest.json</a>、<a href="/fear-greed/data/history_us.csv">美股每週紀錄</a>、<a href="/fear-greed/data/history_tw.csv">台股每週紀錄</a>。</footer>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--no-notify", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--test-alert", action="store_true")
    ap.add_argument("--today", help="YYYY-MM-DD，測試用（預設台北今天）")
    a = ap.parse_args()

    now = datetime.now(TAIPEI)
    today = date.fromisoformat(a.today) if a.today else now.date()
    prior = json.loads(LATEST.read_text(encoding="utf-8")) if LATEST.exists() else {}

    fetch = {"skipped": {"ok": True, "added": 0}} if a.no_fetch else run_fetch(today)
    target = target_friday(today)

    hist, blocks, n_new = {}, {}, {}
    for market in ("us", "tw"):
        mats = compute_materials(market)
        hist[market], n_new[market], prev_state = update_history(market, mats, target, a.rebuild)
        blocks[market] = build_market_block(market, hist[market], mats, target, n_new[market], prev_state)

    latest = {
        "generated": now.strftime("%Y-%m-%d %H:%M"),
        "week": blocks["us"]["week"],
        "stale": any(not v.get("ok") for v in fetch.values()),
        "fetch": fetch,
        "thresholds": {"greed_in": GREED_IN, "greed_out": GREED_OUT, "fear_in": FEAR_IN, "fear_out": FEAR_OUT},
        "us": blocks["us"],
        "tw": blocks["tw"],
        "note": "提醒，不是買進訊號；不影響 70% W52 引擎。台股歷史短，僅供參考。",
    }
    if a.no_fetch and prior.get("fetch"):
        latest["fetch"] = prior["fetch"]
        latest["stale"] = prior.get("stale", False)
    LATEST.write_text(json.dumps(latest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    PAGE.write_text(build_page(latest, hist), encoding="utf-8")
    print(f"week {latest['week']}: US {blocks['us']['score']} {blocks['us']['state_zh']} | TW {blocks['tw']['score']} {blocks['tw']['state_zh']} | new weeks {n_new}")

    if a.test_alert:
        alerts = build_alerts(latest, test=True)
        title, body = alert_text(alerts)
        (ROOT / "fg_title.txt").write_text("【測試】" + title + "\n", encoding="utf-8")
        (ROOT / "fg_alert.txt").write_text("這是測試訊息，不是真實狀態改變。\n\n" + body + "\n", encoding="utf-8")
        (ROOT / "fg_mail.html").write_text(alert_mail_html("【測試】" + title, "這是測試訊息，不是真實狀態改變。\n\n" + body), encoding="utf-8")
        print("TEST ALERT written")
    elif not a.no_notify and not a.rebuild:
        alerts = build_alerts(latest)
        if alerts:
            write_alert_files(alerts)
        else:
            print("no state change — no alert")
    return 0


if __name__ == "__main__":
    sys.exit(main())
