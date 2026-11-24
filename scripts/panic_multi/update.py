#!/usr/bin/env python3
"""「多類同時」恐慌訊號：每天更新資料、全史重播、寫狀態與頁面，新事件才寫通知檔。

頁面 /backtest/viable/panic_multi/，workflow .github/workflows/panic-multi-daily.yml。
規則照 v7-backtest docs/Panic_Call_Prereg.md 第 41～77 行，上線版不改規則。

本資料夾的 signals.py、live_core.py、twvix_core.py、breadth_core.py 是 v7-backtest 的逐字副本
（`python3 -m src.panic_call.ci_copy` 產生），不要手改。本檔只負責：
  1. 美股：yfinance 抓最近兩個月 ^GSPC、^NDX、^VIX、^VXN、^VIX3M，接到 data/panic_multi/us_inputs.csv。
     舊資料是 v7 共用價格庫的原值，只覆蓋最後 5 列並往後接；五項沒到齊的日子不接。
  2. 台股：證交所 FMTQIK（加權指數收盤）、期交所 dlOptDataDown（台指選擇權每日行情，算自算台指 VIX）、
     Release revmom-data 的上市櫃日線（算鎖跌停家數比率）。三項都到齊的最後一天才算台股狀態。
  3. 三個市場全史重播（live_core.replay），寫 state.json、state_log.csv、頁面；
     某市場出現新事件（同一市場同一天只通知一次，記在 notified.json）才寫通知檔。

用法：
  python scripts/panic_multi/update.py                     # 抓新資料並更新
  python scripts/panic_multi/update.py --offline           # 不抓資料，只用現有檔重播與產頁
  python scripts/panic_multi/update.py --revmom DIR        # revmom 資料夾（含 prices.parquet）；沒給就不更新鎖跌停比率
  python scripts/panic_multi/update.py --test-notify       # 另寫一份標題含「測試」的通知檔（內容用最近一次真實事件）
  python scripts/panic_multi/update.py --no-us / --no-tw   # 跳過某一邊的抓取
通知檔（工作目錄）：panic_alert.txt（純文字）、panic_title.txt（標題一行）、panic_mail.html。
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import io
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import live_core as L  # noqa: E402
import twvix_core as TV  # noqa: E402
import breadth_core as BC  # noqa: E402

ROOT = HERE.parents[1]
D = ROOT / "data" / "panic_multi"
PAGE_URL = "https://research.investmquest.com/backtest/viable/panic_multi/"
TPE = ZoneInfo("Asia/Taipei")
NY = ZoneInfo("America/New_York")
UA = "Mozilla/5.0 (research data fetch)"

US_T = {"gspc": "^GSPC", "ndx": "^NDX", "vix": "^VIX", "vxn": "^VXN", "vix3m": "^VIX3M"}
NAMES = {"SPX": "S&P 500", "NDX": "Nasdaq-100", "TW": "台股加權指數"}
VOLNAME = {"SPX": "VIX", "NDX": "VXN", "TW": "台指 VIX（自算）"}
RATIONAME = {"SPX": "VIX ÷ VIX3M", "NDX": "VIX ÷ VIX3M", "TW": "鎖跌停家數比率"}
LOG: list[str] = []


def log(msg: str) -> None:
    print(msg, flush=True)
    LOG.append(msg)


# ───────────────────────── 美股 ─────────────────────────
def read_us() -> pd.DataFrame:
    return pd.read_csv(D / "us_inputs.csv", parse_dates=["date"], float_precision="round_trip").set_index("date")


def fetch_us(us: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    import yfinance as yf
    tick = list(US_T.values()) + ["QQQ", "^IRX"]
    raw = yf.download(tick, period="2mo", interval="1d", auto_adjust=False, progress=False, threads=False)
    close = raw["Close"].copy()
    close.index = pd.to_datetime(close.index).tz_localize(None).normalize()
    now_ny = dt.datetime.now(NY)
    if now_ny.hour < 17 or (now_ny.hour == 17 and now_ny.minute < 30):
        close = close[close.index < pd.Timestamp(now_ny.date())]    # 美股當天還沒收完（含 VIX 16:15）不接
    new = close.rename(columns={v: k for k, v in US_T.items()})[list(US_T)]
    complete = new.notna().all(axis=1)
    if len(new) and not complete.iloc[-1]:
        log(f"美股最後一列 {new.index[-1].date()} 五項沒到齊（Yahoo 午夜後常見），這次不接")
    new = new[complete]
    aux = {}
    for t in ("QQQ", "^IRX"):
        s = close[t].dropna()
        if len(s):
            aux[t] = (str(s.index[-1].date()), float(s.iloc[-1]))
    if new.empty:
        return us, aux
    keep_upto = us.index[-6] if len(us) > 6 else us.index[0]   # 舊資料只覆蓋最後 5 列
    add = new[new.index > keep_upto].copy()
    changed = []
    for d_, row in add.iterrows():
        if d_ in us.index:
            old = us.loc[d_, list(US_T)]
            # Yahoo 每次回傳的值常差一個 float32 尾數（Nasdaq-100 約 0.004 點）：差不到百萬分之一就保留舊值，不讓檔案每天跟著變
            if np.allclose(old.to_numpy(float), row.to_numpy(float), rtol=1e-6, atol=0, equal_nan=True):
                add.loc[d_, list(US_T)] = old.to_numpy(float)
            else:
                changed.append(str(d_.date()))
    out = pd.concat([us[us.index <= keep_upto], add]).sort_index()
    out = out[~out.index.duplicated(keep="last")]
    out.index.name = "date"
    if changed:
        log(f"美股覆蓋改值的日子：{changed}")
    log(f"美股資料到 {out.index[-1].date()}（原本 {us.index[-1].date()}）")
    return out, aux


def us_frames(us: pd.DataFrame) -> dict:
    """同 v7 src/panic_call/data.py 的美股欄位。"""
    out = {}
    for name, idx, vcol in [("SPX", "gspc", "vix"), ("NDX", "ndx", "vxn")]:
        px = us[idx].dropna()
        px = px[px > 0]
        df = pd.DataFrame({"close": px})
        df["vol"] = us[vcol].reindex(df.index)
        df["ratio"] = us["vix"].reindex(df.index) / us["vix3m"].reindex(df.index)
        out[name] = df
    return out


# ───────────────────────── 台股 ─────────────────────────
def months_back(n: int) -> list[tuple[int, int]]:
    t = dt.datetime.now(TPE).date()
    y, m = t.year, t.month
    out = []
    for _ in range(n):
        out.append((y, m))
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return sorted(out)


def http(url: str, data: bytes | None = None, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA})
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"{url} 失敗：{last}")


def fetch_taiex() -> pd.DataFrame:
    """證交所 FMTQIK（同 v7 tools/fetch_taiex_fmtqik.py）：本月與上月。"""
    rows = []
    for y, m in months_back(2):
        js = json.loads(http(f"https://www.twse.com.tw/rwd/zh/afterTrading/FMTQIK?date={y}{m:02d}01&response=json",
                             timeout=30).decode("utf-8"))
        if js.get("stat") != "OK":
            continue
        for r in js["data"]:
            ry, rm, rd = (int(x) for x in r[0].strip().split("/"))
            rows.append({"date": pd.Timestamp(ry + 1911, rm, rd), "close": float(str(r[4]).replace(",", ""))})
        time.sleep(3)
    return pd.DataFrame(rows).drop_duplicates("date").set_index("date").sort_index()


TXO_COLS = {"交易日期": "date", "契約": "contract", "到期月份(週別)": "expiry", "履約價": "strike",
            "買賣權": "cp", "成交量": "volume", "結算價": "settle", "最後最佳買價": "bid",
            "最後最佳賣價": "ask", "交易時段": "session"}


def parse_txo(body: bytes) -> pd.DataFrame:
    """同 v7 tools/fetch_txo_daily.py 的 build()：只留月選與季選（到期月份 6 碼）、一般交易時段。"""
    txt = body.decode("big5", "ignore")
    df = pd.read_csv(io.StringIO(txt), dtype=str, index_col=False)
    df.columns = [c.strip() for c in df.columns]
    df = df[[c for c in TXO_COLS if c in df.columns]].rename(columns=TXO_COLS)
    for c in df.columns:
        df[c] = df[c].str.strip()
    if "session" not in df.columns:
        df["session"] = "一般"
    df["session"] = df["session"].fillna("一般")
    df = df[(df["session"] == "一般") & df["expiry"].str.fullmatch(r"\d{6}")]
    df["date"] = pd.to_datetime(df["date"], format="%Y/%m/%d")
    df["cp"] = df["cp"].map({"買權": "C", "賣權": "P"})
    for c in ["strike", "volume", "settle", "bid", "ask"]:
        df[c] = pd.to_numeric(df[c].replace({"-": None, "": None}), errors="coerce")
    df = df.drop(columns=["contract", "session"]).sort_values(["date", "expiry", "cp", "strike"])
    return df.drop_duplicates(["date", "expiry", "cp", "strike"], keep="last").reset_index(drop=True)


def fetch_txo() -> pd.DataFrame:
    frames = []
    for y, m in months_back(2):
        last = calendar.monthrange(y, m)[1]
        data = urllib.parse.urlencode({"down_type": "1", "commodity_id": "TXO", "commodity_id2": "",
                                       "queryStartDate": f"{y}/{m:02d}/01",
                                       "queryEndDate": f"{y}/{m:02d}/{last:02d}"}).encode()
        body = http("https://www.taifex.com.tw/cht/3/dlOptDataDown", data=data)
        if not body[:20].decode("big5", "ignore").startswith("交易日期"):
            raise RuntimeError(f"期交所 TXO {y}-{m:02d} 回應不是 CSV：{body[:80]!r}")
        frames.append(parse_txo(body))
        time.sleep(2)
    return pd.concat(frames, ignore_index=True)


def exp_map_for(expiries) -> dict:
    """同 v7 build.expiry_dates：已結算的用 final_settle.csv 的最後結算日，其餘用第三個星期三。"""
    f = pd.read_csv(D / "final_settle.csv", parse_dates=["final_date"], dtype={"expiry": str})
    m = dict(zip(f.expiry, f.final_date))
    for e in expiries:
        if e not in m:
            m[e] = TV.third_wednesday(e)
    return m


def proxy_rows(d: pd.DataFrame) -> pd.DataFrame:
    """同 v7 src/twvix_proxy/build.py 的 build() 每日迴圈（只算傳入的日子）。"""
    d = d[d.expiry.str.len() == 6].copy()
    valid = d.bid.notna() & d.ask.notna() & (d.ask >= d.bid)
    d["px_settle"] = d.settle
    d["px_mid"] = np.where(valid, (d.bid + d.ask) / 2.0, d.settle)
    dates = sorted(d.date.unique())
    tdays = pd.DatetimeIndex(dates).append(pd.bdate_range(dates[-1] + pd.Timedelta(days=1), periods=90))
    exp_map = exp_map_for(sorted(d.expiry.unique()))
    rows = []
    for dt_, g in d.groupby("date"):
        dt_ = pd.Timestamp(dt_)
        exps = sorted(set(g.expiry), key=lambda e: exp_map[e])
        exps = [e for e in exps if exp_map[e] >= dt_]
        i0 = tdays.searchsorted(dt_)
        usable = [e for e in exps if tdays.searchsorted(exp_map[e], side="left") - i0 > TV.ROLL_TD]
        if len(usable) < 2:
            rows.append(dict(date=dt_))
            continue
        near, nxt = usable[0], usable[1]
        r = dict(date=dt_, near_expiry=near, next_expiry=nxt)
        for tag, col in (("settle", "px_settle"), ("mid", "px_mid")):
            out = TV.vix_one_day(g, dt_, near, nxt, exp_map, col)
            r["vix_" + tag] = out["vix"] if out else np.nan
            if tag == "settle":
                if out:
                    for t in ("near", "next"):
                        o = out[t]
                        r["near_days" if t == "near" else "next_days"] = o["days"]
                        r[f"n_strikes_{t}"] = o["n"]
                        r[f"forward_{t}"] = o["F"]
                        r[f"k0_{t}"] = o["K0"]
                        r[f"var_{t}"] = o["var"]
                else:
                    r["near_days"] = (exp_map[near] - dt_).days
                    r["next_days"] = (exp_map[nxt] - dt_).days
        rows.append(r)
    return pd.DataFrame(rows).set_index("date")


def update_proxy(txo: pd.DataFrame) -> pd.Timestamp:
    p = D / "twvix_proxy_daily.csv"
    old = pd.read_csv(p, dtype={"near_expiry": str, "next_expiry": str}, float_precision="round_trip")
    cols = list(old.columns)
    new = proxy_rows(txo)
    off = ROOT / "data" / "tw_chips" / "vix.jsonl"
    if off.exists():
        o = pd.read_json(off, lines=True)
        o["d"] = pd.to_datetime(o["d"])
        new["official"] = o.drop_duplicates("d", keep="last").set_index("d")["v"].reindex(new.index)
    new = new.reset_index()
    new["date"] = new["date"].dt.strftime("%Y-%m-%d")
    for c in cols:
        if c not in new:
            new[c] = np.nan
    new = new[cols].round(6)
    for c in ("near_days", "next_days"):
        if new[c].notna().all():
            new[c] = new[c].astype(int)
    chk = old[old.date >= new.date.min()].set_index("date")["vix_settle"]
    cmp = new.set_index("date")["vix_settle"].reindex(chk.index)
    diff = chk[((chk - cmp).abs() > 1e-6) | (chk.isna() != cmp.isna())]
    if len(diff):
        log(f"台指 VIX 重算後改值的日子：{list(diff.index)}")
    out = pd.concat([old[~old.date.isin(new.date)], new]).sort_values("date")
    out.to_csv(p, index=False)
    log(f"台指 VIX（自算）到 {out.date.iloc[-1]}，最後一天 {out.vix_settle.iloc[-1]}")
    return pd.Timestamp(out.date.iloc[-1])


def load_prices_panel(data_dir: Path):
    """同 v7 src/tw_panic_limitdown/run.py 的 load_panel，只留價格部分（不讀月營收）。"""
    p = pd.read_parquet(data_dir / "prices.parquet")
    p = p[p.code.str.fullmatch(r"\d{4}") & ~p.code.str.startswith("00") & ~p.code.str.startswith("91")]
    w = {c: p.pivot(index="date", columns="code", values=c) for c in ("close", "value", "mark", "ref")}
    dates = w["ref"].index
    codes = w["ref"].columns
    w = {k: v.reindex(index=dates, columns=codes) for k, v in w.items()}
    t = pd.Timestamp("2011-07-27")
    if t in dates and "3454" in codes and abs(w["ref"].at[t, "3454"] + 2.3) < 1e-9:
        w["ref"].at[t, "3454"] = 79.07
    listed = w["ref"].notna() & (w["ref"] > 0)
    return dates, codes, w, listed


def update_breadth(revmom_dir: Path) -> pd.Timestamp:
    p = D / "tw_limit_down_breadth_daily.csv"
    old = pd.read_csv(p, parse_dates=["date"], float_precision="round_trip").set_index("date")
    dates, codes, w, listed = load_prices_panel(revmom_dir)
    br, _, _ = BC.breadth(dates, codes, w, listed)
    br = br.rename(columns={"n_universe": "universe_count", "n_locked_down": "locked_limit_down_count",
                            "n_no_trade": "no_trade_count", "ratio": "locked_limit_down_ratio"})
    br.index = pd.to_datetime(br.index)
    br.index.name = "date"
    cut = old.index[-21] if len(old) > 21 else old.index[0]     # 舊資料只覆蓋最後 20 列
    add = br[br.index > cut].copy()
    ints = ["universe_count", "locked_limit_down_count", "no_trade_count"]
    ov = old.index.intersection(add.index)
    bad = [str(x.date()) for x in ov if (old.loc[x, ints].astype(int) != add.loc[x, ints].astype(int)).any()]
    if bad:
        log(f"鎖跌停比率重算後改值的日子：{bad}")
    same = [x for x in ov if str(x.date()) not in bad]
    add = add.drop(index=same)          # 家數沒變的舊列整列保留原值（比率只差浮點尾數，不讓文字跟著變）
    out = pd.concat([old[~old.index.isin(add.index)], add]).sort_index()
    out = out[~out.index.duplicated(keep="last")]
    out[ints] = out[ints].astype(int)
    out.to_csv(p, date_format="%Y-%m-%d")
    log(f"鎖跌停比率到 {out.index[-1].date()}（原本 {old.index[-1].date()}），最後一天 {out.iloc[-1]['locked_limit_down_ratio']:.4f}")
    return out.index[-1]


def tw_frame() -> pd.DataFrame:
    """同 v7 src/panic_call/data.py 的台股欄位；三項都到齊的最後一天為止。"""
    tx = pd.read_csv(D / "taiex_close.csv", parse_dates=["date"]).set_index("date").sort_index()
    tv = pd.read_csv(D / "twvix_proxy_daily.csv", parse_dates=["date"]).set_index("date")["vix_settle"]
    ld = pd.read_csv(D / "tw_limit_down_breadth_daily.csv", parse_dates=["date"]).set_index("date")["locked_limit_down_ratio"]
    tw = pd.DataFrame({"close": tx["close"].astype(float)})
    tw["vol"] = tv.reindex(tw.index)
    tw["ratio"] = ld.reindex(tw.index)
    last = min(tw.index.max(), tv.index.max(), ld.index.max())
    return tw[tw.index <= last]


# ───────────────────────── 隔天要買的規格 ─────────────────────────
def next_weekday(d: pd.Timestamp) -> pd.Timestamp:
    n = d + pd.Timedelta(days=1)
    while n.weekday() >= 5:
        n += pd.Timedelta(days=1)
    return n


def third_friday(y: int, m: int) -> pd.Timestamp:
    d = pd.Timestamp(y, m, 1)
    return d + pd.Timedelta(days=(4 - d.weekday()) % 7 + 14)


def pick_91(cands: dict):
    """同 v7 weekly_bb_put.tw_pricing.pick_expiry 規格 B：60～100 天內最接近 91 天（平手取較近）。"""
    c = [(abs(days - 91), days, e) for e, days in cands.items() if 60 <= days <= 100]
    return min(c)[2] if c else None


def bs_call(S, K, T, r, q, sg):
    if T <= 0:
        return max(S - K, 0.0)
    d1 = (math.log(S / K) + (r - q + 0.5 * sg * sg) * T) / (sg * math.sqrt(T))
    d2 = d1 - sg * math.sqrt(T)
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))  # noqa: E731
    return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d2)


def us_expiry(entry: pd.Timestamp):
    cands = {}
    for k in range(0, 6):
        y, m = entry.year + (entry.month - 1 + k) // 12, (entry.month - 1 + k) % 12 + 1
        e = third_friday(y, m)
        cands[e] = (e - entry).days
    return pick_91(cands)


def fut_month(exp: pd.Timestamp) -> str:
    """美股微型期貨只有季月，而且在到期那個星期五開盤就結算：取到期日之後才結算的第一個季月。"""
    y, m = exp.year, exp.month + (3 if exp.month % 3 == 0 else 0)
    while m % 3:
        m += 1
    if m > 12:
        y, m = y + 1, m - 12
    return f"{y}-{m:02d}"


def order_us(name: str, st: dict, us: pd.DataFrame, aux: dict) -> dict:
    d0 = pd.Timestamp(st["date"])
    entry = next_weekday(d0)
    exp = us_expiry(entry)
    days = (exp - entry).days
    r = aux.get("^IRX", (None, 4.0))[1] / 100.0
    row = us.loc[d0]
    # 偏斜同 v7 options.f_value：每 1% 價內加 0.5 個波動率點（價內 5% 加 2.5 點）；這只是估權利金，不是規則
    if name == "SPX":
        S = float(row["gspc"]) / 10.0                         # XSP＝S&P 500 ÷ 10
        K = float(math.floor(0.95 * S + 0.5))
        atm = float(row["vix3m"]) / 100.0
        sg = atm + 0.5 * 100.0 * (S - K) / S / 100.0
        prem = bs_call(S, K, days / 365.0, r, 0.013, sg)
        fut_per_call = 2.0                                    # 1 口 XSP（100×XSP＝10×指數）對 2 口 MES（5×指數）
        stop_pts = prem * 100.0 / (5.0 * fut_per_call)        # 換成 S&P 500 指數點
        return dict(entry_est=str(entry.date()), expiry=str(exp.date()), days=days,
                    call=dict(product="XSP（Mini-SPX，S&P 500 ÷ 10，歐式、現金結算）", strike=K, underlying=round(S, 2),
                              premium_est=round(prem, 2), premium_usd=round(prem * 100, 0), vol_used=round(sg * 100, 2),
                              alt="帳戶 500 萬美元以上可改 SPX（XSP 的 10 倍）"),
                    fut=dict(product="MES（微型 S&P 500 期貨，每點 5 美元）", per_call=fut_per_call,
                             month=fut_month(exp), stop_pts=round(stop_pts, 1),
                             stop_level=round(float(row["gspc"]) - stop_pts, 1)))
    q_ = aux.get("QQQ")
    ndx = float(row["ndx"])
    S = q_[1] if q_ else ndx / 41.0
    K = float(math.floor(0.95 * S + 0.5))
    atm = float(row["vxn"]) / 100.0
    sg = atm + 0.5 * 100.0 * (S - K) / S / 100.0
    prem = bs_call(S, K, days / 365.0, r, 0.006, sg)
    fut_per_call = 100.0 * S / (2.0 * ndx)                    # 名目：100×QQQ 對 2×NDX
    stop_pts = prem * ndx / S                                 # 換成 Nasdaq-100 指數點
    return dict(entry_est=str(entry.date()), expiry=str(exp.date()), days=days,
                call=dict(product="QQQ 選擇權（美式，到期日收盤前平倉，避免交割股票）", strike=K, underlying=round(S, 2),
                          premium_est=round(prem, 2), premium_usd=round(prem * 100, 0), vol_used=round(sg * 100, 2),
                          qqq_date=q_[0] if q_ else None,
                          alt=f"NDX 選擇權一口名目約 {ndx * 100 / 1e4:,.0f} 萬美元、XND 成交太少，所以用 QQQ"),
                fut=dict(product="MNQ（微型 Nasdaq-100 期貨，每點 2 美元）", per_call=round(fut_per_call, 2),
                         month=fut_month(exp), stop_pts=round(stop_pts, 1), stop_level=round(ndx - stop_pts, 1)))


def order_tw(st: dict, txo: pd.DataFrame | None) -> dict:
    d0 = pd.Timestamp(st["date"])
    entry = next_weekday(d0)
    out = dict(entry_est=str(entry.date()))
    if txo is None or txo.empty or d0 not in set(txo.date):
        out["note"] = "這次沒有抓到訊號日的台指選擇權行情，履約價與權利金請以隔天報價為準：到期 60～100 天、最接近 91 天，履約價最接近收盤的 95%。"
        return out
    g = txo[(txo.date == d0) & (txo.cp == "C")]
    exps = sorted(g.expiry.unique())
    em = exp_map_for(exps)
    cands = {e: (em[e] - entry).days for e in exps}
    e = pick_91(cands)
    if e is None:
        out["note"] = "沒有 60～100 天內到期的合約。"
        return out
    ge = g[(g.expiry == e) & g.settle.notna() & (g.settle > 0)].copy()
    ge["dist"] = (ge.strike - 0.95 * st["close"]).abs()
    k = ge.sort_values(["dist", "strike"]).iloc[0]
    out.update(expiry=e, expiry_date=str(em[e].date()), days=cands[e],
               call=dict(product="台指選擇權（TXO）買權，每點 50 元", strike=float(k.strike), settle=float(k.settle),
                         premium_twd=float(k.settle) * 50, volume=int(0 if pd.isna(k.volume) else k.volume),
                         bid=None if pd.isna(k.bid) else float(k.bid), ask=None if pd.isna(k.ask) else float(k.ask)),
               fut=dict(product=f"小型台指期貨（小台，每點 50 元）{e[:4]}-{e[4:]} 月", per_call=1,
                        stop_pts=float(k.settle), stop_level=round(st["close"] - float(k.settle), 1)))
    return out


# ───────────────────────── 狀態、紀錄、通知 ─────────────────────────
def build_state(frames: dict, us: pd.DataFrame, aux: dict, txo) -> dict:
    out = {}
    for name, df in frames.items():
        st = L.replay(df)["state"]
        st["name"] = NAMES[name]
        st["vol_name"] = VOLNAME[name]
        st["ratio_name"] = RATIONAME[name]
        st["events_this_year"] = sum(1 for e in st["events"] if e[:4] == st["date"][:4])
        recent = [e for e in st["events"][-1:] if (pd.Timestamp(st["date"]) - pd.Timestamp(e)).days <= 10]
        if recent:   # 最近 10 天內有事件（含今天）：用事件那天的資料算隔天要買的規格
            ev_st = st if st["event_today"] else L.replay(df[df.index <= pd.Timestamp(recent[0])])["state"]
            st["order"] = order_tw(ev_st, txo) if name == "TW" else order_us(name, ev_st, us, aux)
            st["order_for_event"] = ev_st["date"]
            st["event_state"] = {k: ev_st[k] for k in ("date", "close", "classes", "n_lit")}
        out[name] = st
    return out


def append_log(state: dict) -> None:
    p = D / "state_log.csv"
    cols = ["date", "market", "close", "vol", "vol_share", "vol_lit", "z3", "z3_share", "accel", "accel_lit",
            "ratio", "ratio_share", "ratio_lit", "n_lit", "armed_open", "event", "last_event"]
    old = pd.read_csv(p, dtype=str) if p.exists() else pd.DataFrame(columns=cols)
    rows = []
    for m, s in state.items():
        c = s["classes"]
        rows.append(dict(date=s["date"], market=m, close=s["close"], vol=c["vol"]["value"], vol_share=c["vol"]["share"],
                         vol_lit=c["vol"]["lit"], z3=c["accel"]["value"], z3_share=c["accel"]["share"],
                         accel=c["accel"]["accel"], accel_lit=c["accel"]["lit"], ratio=c["ratio"]["value"],
                         ratio_share=c["ratio"]["share"], ratio_lit=c["ratio"]["lit"], n_lit=s["n_lit"],
                         armed_open=s["armed_open"], event=s["event_today"], last_event=s["last_event"]))
    new = pd.DataFrame(rows, columns=cols).astype(str)
    out = pd.concat([old, new], ignore_index=True).drop_duplicates(["date", "market"], keep="last")
    out.sort_values(["date", "market"]).to_csv(p, index=False)


def pct(x) -> str:
    if x is None:
        return "—"
    v = x * 100
    return f"{v:.1f}%" if v >= 0.1 else "不到 0.1%"


def fmt_num(x, nd=2) -> str:
    return "—" if x is None else f"{x:,.{nd}f}"


def class_lines(m: str, ev: dict, names: dict) -> list[str]:
    c = ev["classes"]
    a, b, r = c["vol"], c["accel"], c["ratio"]
    rd = 4 if m == "TW" else 3
    bp = "、".join(f"{x / 100:+.2f}%" for x in b["last3_bp"]) if b["last3_bp"] else "—"
    return [
        f"甲 波動率水位（{names['vol_name']}）{fmt_num(a['value'])}：歷史上 {pct(a['share'])} 的日子一樣高或更高（門檻 5%），{'亮' if a['lit'] else '沒亮'}",
        f"乙 連三天加速下跌：最近三天 {bp}，{'跌幅一天比一天大' if b['accel'] else '不是一天比一天跌得多'}；"
        f"三日標準化報酬 {fmt_num(b['value'])}，歷史最差 {pct(b['share'])}，{'亮' if b['lit'] else '沒亮'}",
        f"丙 {names['ratio_name']} {fmt_num(r['value'], rd)}：歷史上 {pct(r['share'])} 的日子一樣高或更高（門檻 5%），{'亮' if r['lit'] else '沒亮'}",
    ]


def order_lines(m: str, st: dict) -> list[str]:
    o = st.get("order") or {}
    if not o:
        return []
    out = [f"進場：訊號日收盤後確認，隔天（{o.get('entry_est')}，遇休市順延）收盤進場。call 版、期貨版二選一。"]
    if m == "TW":
        if "call" not in o:
            return out + [o.get("note", "")]
        c, f = o["call"], o["fut"]
        out.append(f"call 版：台指選擇權 {o['expiry'][:4]}-{o['expiry'][4:]} 月（{o['expiry_date']} 到期，{o['days']} 天）、"
                   f"履約價 {c['strike']:,.0f} 的買權（約價內 5%）。訊號日結算價 {c['settle']:,.0f} 點，"
                   f"一口約 {c['premium_twd']:,.0f} 元；訊號日成交 {c['volume']} 口，要掛限價。抱到到期。")
        out.append(f"期貨版：每 1 口買權改買 1 口{f['product']}，名目一樣。收盤虧損達到權利金點數"
                   f"（約 {f['stop_pts']:,.0f} 點，加權指數約 {f['stop_level']:,.0f}）就在收盤停損，否則抱到同一個到期日。")
    else:
        c, f = o["call"], o["fut"]
        out.append(f"call 版：{c['product']}，{o['expiry']} 到期（{o['days']} 天）、履約價 {c['strike']:,.0f}（約價內 5%），"
                   f"公式估每口約 {c['premium_usd']:,.0f} 美元（隱含波動率 {c['vol_used']}%，下單看實際報價）。抱到到期。{c['alt']}。")
        out.append(f"期貨版：每 1 口 call 改買 {f['per_call']:g} 口 {f['product']}，{f['month']} 月合約，名目一樣。"
                   f"收盤虧損達到同一筆權利金（{st['name']} 從進場價跌約 {f['stop_pts']:,.0f} 點）就在收盤停損，否則抱到 {o['expiry']} 收盤。")
    out.append("預算：每次權利金＝帳戶的 1%（口數＝帳戶 1% ÷ 每口權利金，取整數），這條訊號一年最多 4 次，"
               f"今年已亮 {st['events_this_year']} 次。上一筆還沒到期時新訊號不加碼。")
    return out


def alert_text(m: str, st: dict, test: bool) -> tuple[str, str]:
    ev = st["event_state"]
    title = ("【測試】" if test else "") + f"恐慌訊號：{st['name']}「多類同時」亮起（{ev['date']} 收盤，{ev['n_lit']} 類）"
    body = []
    if test:
        body.append("這是測試信，用來確認格式；內容是最近一次真實事件，不是新的訊號。")
    sep = "" if st["name"].endswith("數") else " "
    body.append(f"{st['name']}{sep}在 {ev['date']} 收盤（{ev['close']:,.2f}），三類裡亮了 {ev['n_lit']} 類：")
    body += ["- " + x for x in class_lines(m, ev, st)]
    body.append("")
    body += order_lines(m, st)
    body.append("")
    body.append(f"下次重新觸發：要等 {st['vol_name']} 收盤回到自己歷史中位數（目前約 {fmt_num(st.get('vol_median_next'))}）以下，"
                "之後三類再有兩類同一天亮，才算新的一波。")
    body.append(f"頁面：{PAGE_URL}")
    body.append("提醒：每個市場的歷史只有 5～12 筆，最賺三筆占大部分獲利；證明不了，只能當線索。")
    return title, "\n".join(body)


def write_alert(items: list[tuple[str, str]], test: bool) -> None:
    import html as H
    title = items[0][0] if len(items) == 1 else ("【測試】" if test else "") + "恐慌訊號：" + "、".join(
        t.split("：", 1)[1] for t, _ in items)
    body = "\n\n——\n\n".join(b for _, b in items)
    Path("panic_title.txt").write_text(title + "\n", encoding="utf-8")
    Path("panic_alert.txt").write_text(body + "\n", encoding="utf-8")
    paras = "".join(f"<p style='margin:.35em 0'>{H.escape(x)}</p>" if x.strip() else "<br>" for x in body.split("\n"))
    Path("panic_mail.html").write_text(
        "<div style='font-family:-apple-system,Segoe UI,Noto Sans TC,sans-serif;font-size:15px;line-height:1.6;color:#111827'>"
        f"<h2 style='font-size:17px'>{H.escape(title)}</h2>{paras}"
        "<p style='color:#6b7280;font-size:13px'>InvestMQuest · 多類同時恐慌訊號（只在新事件那天寄出）</p></div>",
        encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--no-us", action="store_true")
    ap.add_argument("--no-tw", action="store_true")
    ap.add_argument("--revmom", default="")
    ap.add_argument("--test-notify", action="store_true")
    ap.add_argument("--no-notify", action="store_true")
    a = ap.parse_args()
    us, aux, txo = read_us(), {}, None
    if not a.offline and not a.no_us:
        try:
            us, aux = fetch_us(us)
            us.to_csv(D / "us_inputs.csv", date_format="%Y-%m-%d")
        except Exception as e:  # noqa: BLE001
            log(f"美股抓取失敗，沿用舊資料：{e}")
    if not a.offline and not a.no_tw:
        try:
            tx = fetch_taiex()
            old = pd.read_csv(D / "taiex_close.csv", parse_dates=["date"], float_precision="round_trip").set_index("date")
            out = pd.concat([old[~old.index.isin(tx.index)], tx]).sort_index()
            out.to_csv(D / "taiex_close.csv", date_format="%Y-%m-%d")
            log(f"加權指數到 {out.index[-1].date()}")
        except Exception as e:  # noqa: BLE001
            log(f"加權指數抓取失敗，沿用舊資料：{e}")
        try:
            txo = fetch_txo()
            update_proxy(txo)
        except Exception as e:  # noqa: BLE001
            log(f"台指選擇權抓取或計算失敗，沿用舊資料：{e}")
        if a.revmom:
            try:
                update_breadth(Path(a.revmom))
            except Exception as e:  # noqa: BLE001
                log(f"鎖跌停比率計算失敗，沿用舊資料：{e}")
    frames = us_frames(us)
    frames["TW"] = tw_frame()
    state = build_state(frames, us, aux, txo)
    notified = json.loads((D / "notified.json").read_text()) if (D / "notified.json").exists() else {}
    items = []
    for m, st in state.items():
        if st["event_today"] and notified.get(m) != st["date"]:
            items.append(alert_text(m, st, False))
            notified[m] = st["date"]
    if a.test_notify:
        m = max(state, key=lambda k: state[k]["last_event"] or "")
        st = dict(state[m])
        if "event_state" not in st:   # 最近沒有事件：用最近一次事件那天重播
            ev = L.replay(frames[m][frames[m].index <= pd.Timestamp(st["last_event"])])["state"]
            st["event_state"] = {k: ev[k] for k in ("date", "close", "classes", "n_lit")}
            st["order"] = order_tw(ev, txo) if m == "TW" else order_us(m, ev, us, aux)
        items = [alert_text(m, st, True)]
    if items and not a.no_notify:
        write_alert(items, a.test_notify)
        log(f"寫入通知檔：{len(items)} 則")
    if not a.test_notify:
        (D / "notified.json").write_text(json.dumps(notified, ensure_ascii=False, indent=1) + "\n")
    gen = dt.datetime.now(TPE).strftime("%Y-%m-%d %H:%M")
    slim = {m: {k: v for k, v in s.items() if k != "last_event_i"} for m, s in state.items()}
    for m, s in state.items():
        log(f"{m} {s['date']}：亮 {s['n_lit']} 類，可觸發 {s['armed_open']}，今天事件 {s['event_today']}，上次 {s['last_event']}")
    (D / "state.json").write_text(json.dumps(dict(generated=gen, markets=slim, log=LOG), ensure_ascii=False, indent=1) + "\n")
    append_log(state)
    import page
    page.write(slim, gen)


if __name__ == "__main__":
    main()
