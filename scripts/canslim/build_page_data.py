#!/usr/bin/env python3
"""CAN SLIM 頁（/canslim/）資料建置：讀 v7-backtest 最新一份 CAN SLIM 篩選輸出與價格，寫 docs/canslim/data/*.json。

要用 v7 的 venv 跑（需要 pandas、pyarrow、yfinance）：
    ~/.venvs/v7bt/bin/python scripts/canslim/build_page_data.py
    ~/.venvs/v7bt/bin/python scripts/canslim/build_page_data.py --v7 ~/v7-backtest --src ~/v7-backtest/data/canslim_screen_2026-10-17

輸入（自動挑最新）：
    <v7>/data/canslim_screen_*/ 之中日期最新、且含 screen_all_v2.csv（ROIC 修補版）或 screen_all.csv 的資料夾；兩者都有就用 v2。
    同資料夾的 market_state.csv、screen_large.pkl、screen_midsmall.pkl（年度 EPS 序列，缺就略過）、screen_v2_summary.json（有就用）。
    <v7>/data/us_ohlcv{,_midsmall}/ohlcv_adj.parquet（小圖用的還原收盤價）。

輸出（docs/canslim/data/）：
    meta.json     資料截至日、版本、母體檔數
    market.json   SPY／QQQ／IJR 狀態表、近 1 年收盤與 50／200 日線、出貨日
    funnel.json   兩個母體的漏斗
    picks.json    五關全過名單（含小圖資料）與差一條名單
    table.json    全部檔數的篩選結果（精簡欄位）
    profile_cache.json  公司全名與產業（只替名單內的股票向 yfinance 補，抓過的不重抓）
不碰 evidence.json（證據段，手動維護）。

單位約定：比率一律存小數（0.439 = 43.9%）；FCF 存「億美元」；平均量存「萬股」。
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import math
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "docs" / "canslim" / "data"

GATES = [("q_ok", "品質"), ("c_ok", "C"), ("a_ok", "A"), ("n_ok", "N"), ("l_ok", "L")]
GATE_DESC = {
    "q_ok": "TTM ROIC ≥15% 且 TTM FCF >0",
    "c_ok": "最近一季 EPS 年增 ≥25%，且營收年增 ≥25% 或連續三季加速",
    "a_ok": "近 3 個完整年度 EPS 每年成長、3 年複合成長 ≥25%",
    "n_ok": "收盤 ≥ 52 週高 × 0.85",
    "l_ok": "RS ≥80（組內百分位）",
}
GROUP_LABEL = {"large": "大型股", "midsmall": "中小型股"}
SECTOR_ZH = {
    "Technology": "資訊科技", "Healthcare": "醫療保健", "Energy": "能源", "Financial Services": "金融",
    "Consumer Cyclical": "非必需消費", "Consumer Defensive": "必需消費", "Industrials": "工業",
    "Basic Materials": "原物料", "Communication Services": "通訊服務", "Utilities": "公用事業",
    "Real Estate": "不動產",
}
CHART_BARS = 252
DIST_THRESHOLD = 5  # 近 25 日出貨日 ≥5 視為警訊（書中以 5～6 天以上為警訊，取下緣）


# --------------------------------------------------------------------------- 小工具
def clean(x):
    """numpy／NaN 轉成可 JSON 的 Python 值。"""
    if x is None:
        return None
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return None if (math.isnan(x) or math.isinf(x)) else float(x)
    if isinstance(x, (pd.Timestamp, dt.datetime, dt.date)):
        return pd.Timestamp(x).strftime("%Y-%m-%d")
    if x is pd.NaT:
        return None
    return x


def r(x, nd):
    x = clean(x)
    return None if x is None else round(x, nd)


def dump(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    p.write_text(s, encoding="utf-8")
    return len(s.encode("utf-8"))


_FIX = {" Llc": " LLC", " Lp": " LP", " Plc": " plc", " Nv": " NV", " Sa": " SA", " Ag": " AG", " Se": " SE",
        " Adr": " ADR", " Ii": " II", " Iii": " III", "'S": "'s", " Us ": " US ", " Usa": " USA"}


def nice_name(name):
    """SEC 公司名常是全大寫；轉成一般大小寫。已是混合大小寫的不動。"""
    if not isinstance(name, str) or not name:
        return ""
    letters = re.sub(r"[^A-Za-z]", "", name)
    if letters and letters.isupper():
        s = name.title()
        for a, b in _FIX.items():
            s = s.replace(a, b)
        s = re.sub(r"\b(Inc|Corp|Co|Ltd)\b(?!\.)", r"\1.", s)
        return s
    return name


def third_friday(d: pd.Timestamp) -> pd.Timestamp:
    first = d.replace(day=1)
    off = (4 - first.weekday()) % 7
    return first + pd.Timedelta(days=off + 14)


# --------------------------------------------------------------------------- 讀 v7 輸出
def pick_src(v7: Path, explicit: str | None) -> tuple[Path, str]:
    if explicit:
        d = Path(explicit).expanduser()
        dirs = [d]
    else:
        dirs = sorted(Path(p) for p in glob.glob(str(v7 / "data" / "canslim_screen_*")) if os.path.isdir(p))[::-1]
    for d in dirs:
        if (d / "screen_all_v2.csv").exists():
            return d, "v2"
        if (d / "screen_all.csv").exists():
            return d, "v1"
    raise SystemExit(f"找不到 CAN SLIM 篩選輸出（{v7}/data/canslim_screen_*/screen_all[_v2].csv）")


def pick_forward(v7: Path) -> tuple[Path, Path] | None:
    """v7 每週往後追蹤存下的最新一份 (canslim_all.csv, canslim_market.csv)。
    欄位與 screen_all_v2.csv 相同（多一欄 asof），週六 10:30 的 launchd 先重算再呼叫本腳本，
    所以名單與大盤日期都是當週的；canslim_screen_* 資料夾是 2026-10-17 一次性的，不會自己更新。"""
    for f in sorted(glob.glob(str(v7 / "data" / "forward_tracking" / "*_canslim_all.csv")))[::-1]:
        m = Path(f.replace("_canslim_all.csv", "_canslim_market.csv"))
        if m.exists():
            return Path(f), m
    return None


def load_screen(src: Path, version: str, csv: Path | None = None) -> pd.DataFrame:
    f = csv or src / ("screen_all_v2.csv" if version == "v2" else "screen_all.csv")
    d = pd.read_csv(f).set_index("ticker")
    for c in ("q_ok", "c_eps_ok", "c_rev_ok", "c_ok", "a_ok", "bo5"):
        d[c] = d[c].eq(True)
    # 價格面兩關照 report.py 的口徑重算，避免舊旗標與數值不一致
    d["n_ok"] = (d["off_high"] >= -0.15).fillna(False)
    d["l_ok"] = (d["rs"] >= 80).fillna(False)
    d["c_ok"] = d["c_eps_ok"] & d["c_rev_ok"]
    keys = [k for k, _ in GATES]
    d["nfail"] = (~d[keys]).sum(axis=1)
    d["passes"] = 5 - d["nfail"]
    d["name_n"] = d["name"].map(nice_name)
    return d


def load_a_eps(src: Path) -> dict:
    """年度 EPS 序列（四個連續年度）與是否每年成長。pkl 缺就回空 dict。"""
    out = {}
    for f in ("screen_large.pkl", "screen_midsmall.pkl"):
        p = src / f
        if not p.exists():
            continue
        try:
            x = pd.read_pickle(p)
        except Exception as e:  # noqa: BLE001
            print(f"warn: 讀不到 {f}：{e}", file=sys.stderr)
            continue
        for t, row in x.iterrows():
            v = row.get("a_eps")
            if isinstance(v, (list, tuple, np.ndarray)) and len(v) == 4:
                vals = [float(i) for i in v]
                out[t] = dict(eps=vals, grows=bool(all(vals[i + 1] > vals[i] for i in range(3))))
    return out


# --------------------------------------------------------------------------- 漏斗、差一條
def funnel_for(d: pd.DataFrame) -> dict:
    keys = [k for k, _ in GATES]
    f = pd.Series(True, index=d.index)
    gates = []
    for k, lab in GATES:
        f = f & d[k]
        gates.append(dict(key=k, label=lab, cond=GATE_DESC[k], single=int(d[k].sum()), cum=int(f.sum())))
    return dict(
        n=int(len(d)), gates=gates,
        c_eps=int(d["c_eps_ok"].sum()), c_rev=int(d["c_rev_ok"].sum()),
        bo5=int(d["bo5"].sum()), roic_na=int(d["roic"].isna().sum()),
        dist=[int((d["passes"] == k).sum()) for k in range(6)],
        full=int((d["passes"] == 5).sum()), near=int((d["passes"] == 4).sum()),
    )


def failing_gate(row) -> str:
    for k, _ in GATES:
        if not row[k]:
            return k
    return ""


def miss_text(row, gate, a_info) -> str:
    def pct(x, sign=False):
        return f"{x * 100:+.1f}%" if sign else f"{x * 100:.1f}%"

    if gate == "q_ok":
        if pd.isna(row["roic"]):
            return "ROIC 算不出來"
        if row["roic"] < 0.15:
            return f"ROIC {pct(row['roic'])}（門檻 15%）"
        return f"自由現金流 {row['fcf'] / 1e8:,.1f} 億美元，未大於 0"
    if gate == "c_ok":
        s = []
        if not row["c_eps_ok"]:
            s.append(f"EPS 季增 {pct(row['e0'], True)}（門檻 +25%）")
        if not row["c_rev_ok"]:
            s.append(f"營收季增 {pct(row['g0'], True)}，且未連續加速")
        return "；".join(s)
    if gate == "a_ok":
        if pd.isna(row["a_cagr"]):
            return "基期 EPS ≤0，3 年複合成長無法計算"
        extra = ""
        if a_info is not None and not a_info["grows"]:
            extra = "，且不是每年成長"
        return f"3 年 EPS 複合成長 {pct(row['a_cagr'], True)}（門檻 +25%）{extra}"
    if gate == "n_ok":
        return f"距 52 週高 {pct(row['off_high'], True)}（門檻 -15%），差 {abs(row['off_high'] + 0.15) * 100:.1f} 個百分點"
    if gate == "l_ok":
        return f"RS {row['rs']:.1f}（門檻 80），差 {80 - row['rs']:.1f}"
    return ""


# --------------------------------------------------------------------------- 價格（小圖）
def load_chart_series(v7: Path, d: pd.DataFrame, tickers_by_group: dict) -> tuple[dict, str | None]:
    series, last = {}, None
    paths = {"large": v7 / "data/us_ohlcv/ohlcv_adj.parquet", "midsmall": v7 / "data/us_ohlcv_midsmall/ohlcv_adj.parquet"}
    for g, tks in tickers_by_group.items():
        if not tks:
            continue
        want = {t: t for t in tks}
        want.update({t: t.replace(".", "-") for t in tks if "." in t})
        px = pd.read_parquet(paths[g], columns=["date", "ticker", "close"], filters=[("ticker", "in", sorted(set(want.values())))])
        px["date"] = pd.to_datetime(px["date"])
        for t, pt in want.items():
            s = px[px["ticker"] == pt].sort_values("date").set_index("date")["close"].dropna()
            if len(s) < 210:
                continue
            ma = {n: s.rolling(n).mean() for n in (50, 150, 200)}
            tail = s.iloc[-CHART_BARS:]
            idx = tail.index
            series[t] = dict(
                t=[x.strftime("%Y-%m-%d") for x in idx], c=[r(v, 2) for v in tail.values],
                m50=[r(v, 2) for v in ma[50].reindex(idx).values],
                m150=[r(v, 2) for v in ma[150].reindex(idx).values],
                m200=[r(v, 2) for v in ma[200].reindex(idx).values],
            )
            last = max(last, idx[-1].strftime("%Y-%m-%d")) if last else idx[-1].strftime("%Y-%m-%d")
    return series, last


# --------------------------------------------------------------------------- 公司全名與產業
def load_profiles(tickers: list[str]) -> dict:
    p = OUT / "profile_cache.json"
    cache = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    missing = [t for t in tickers if t not in cache or not cache[t].get("name")]
    if missing:
        try:
            import yfinance as yf
        except Exception as e:  # noqa: BLE001
            print(f"warn: 沒有 yfinance，略過公司全名與產業：{e}", file=sys.stderr)
            return cache
        for t in missing:
            try:
                i = yf.Ticker(t.replace(".", "-")).info
                cache[t] = dict(name=i.get("longName") or i.get("shortName") or "", sector=i.get("sector") or "",
                                industry=i.get("industry") or "")
            except Exception as e:  # noqa: BLE001
                print(f"warn: {t} 的公司資料抓不到：{e}", file=sys.stderr)
            time.sleep(0.4)
        dump("profile_cache.json", cache)
    return cache


# --------------------------------------------------------------------------- 大盤
def market_block(src: Path, csv_path: Path | None = None) -> dict:
    csv = pd.read_csv(csv_path or src / "market_state.csv")
    csv["date"] = pd.to_datetime(csv["date"])
    block = dict(chart_ok=False, rows=[], series={}, notes=[])
    series, rows = {}, []
    try:
        import yfinance as yf
        for t in ("SPY", "QQQ", "IJR"):
            h = yf.Ticker(t).history(start="2025-01-01", auto_adjust=False)
            h.index = pd.to_datetime(h.index).tz_localize(None)
            h = h[["Close", "Volume"]].dropna()
            c_row = csv[csv["ticker"] == t].iloc[0]
            h = h[h.index <= c_row["date"]]   # 週六排程之外手動重跑時，不讓比 csv 更新的收盤造成對不上
            c, v = h["Close"], h["Volume"]
            ma50, ma200 = c.rolling(50).mean(), c.rolling(200).mean()
            dist = ((c.pct_change() <= -0.002) & (v > v.shift(1)))
            d25 = dist.iloc[-25:]
            dd = list(d25.index[d25.values])
            if c.index[-1] != c_row["date"] or abs(c.iloc[-1] / c_row["close"] - 1) > 1e-4:
                raise ValueError(f"{t} 重抓的最新收盤與 market_state.csv 對不上（{c.index[-1].date()} {c.iloc[-1]:.2f} 對 {c_row['date'].date()} {c_row['close']:.2f}）")
            tail = c.iloc[-CHART_BARS:]
            series[t] = dict(t=[x.strftime("%Y-%m-%d") for x in tail.index], c=[r(x, 2) for x in tail.values],
                             m50=[r(x, 2) for x in ma50.reindex(tail.index).values],
                             m200=[r(x, 2) for x in ma200.reindex(tail.index).values],
                             dist=[x.strftime("%Y-%m-%d") for x in dd])
            hi52 = c.iloc[-252:].max()
            rows.append(dict(ticker=t, date=c.index[-1].strftime("%Y-%m-%d"), close=r(c.iloc[-1], 2), ma50=r(ma50.iloc[-1], 2),
                             ma200=r(ma200.iloc[-1], 2), pct50=r(c.iloc[-1] / ma50.iloc[-1] - 1, 4),
                             pct200=r(c.iloc[-1] / ma200.iloc[-1] - 1, 4), above50=bool(c.iloc[-1] > ma50.iloc[-1]),
                             above200=bool(c.iloc[-1] > ma200.iloc[-1]), dist25=int(d25.sum()),
                             dist_dates=[x.strftime("%Y-%m-%d") for x in dd], off_hi52=r(c.iloc[-1] / hi52 - 1, 4)))
        block["chart_ok"] = True
    except Exception as e:  # noqa: BLE001
        print(f"warn: 大盤圖資料改用 market_state.csv（沒有圖）：{e}", file=sys.stderr)
        series, rows = {}, []
        for _, x in csv.iterrows():
            dd = [f"{x['date'].year}-{s}" for s in str(x["dist_dates"]).split(",") if s and s != "nan"]
            rows.append(dict(ticker=x["ticker"], date=x["date"].strftime("%Y-%m-%d"), close=r(x["close"], 2), ma50=r(x["ma50"], 2),
                             ma200=r(x["ma200"], 2), pct50=r(x["pct_vs50"], 4), pct200=r(x["pct_vs200"], 4),
                             above50=bool(x["above50"]), above200=bool(x["above200"]), dist25=int(x["dist25"]),
                             dist_dates=dd, off_hi52=r(x["off_hi52"], 4)))
    # 月選擇權到期日（每月第三個週五）當天的出貨日：成交量常被到期部位墊大
    for row in rows:
        ex = [d for d in row["dist_dates"] if pd.Timestamp(d) == third_friday(pd.Timestamp(d))]
        row["opex_dates"] = ex
        row["dist25_ex_opex"] = row["dist25"] - len(ex)
    warn = [x for x in rows if x["dist25"] >= DIST_THRESHOLD]
    names = "、".join(x["ticker"] for x in warn)
    dist_txt = "、".join(f"{x['ticker']} {x['dist25']} 天" for x in rows)
    if len(warn) == len(rows) and rows:
        light = "red"
        head = f"{names} 三個指數近 25 個交易日的出貨日都在 {DIST_THRESHOLD} 天以上（{dist_txt}）。書上的做法是先不買新股。"
    elif warn:
        light = "amber"
        head = f"{names} 的近 25 日出貨日在 {DIST_THRESHOLD} 天以上（{dist_txt}），其餘指數還沒到警訊。大盤已有出貨跡象，新買進要更挑。"
    else:
        light = "green"
        head = f"三個指數近 25 個交易日的出貨日都在 {DIST_THRESHOLD - 1} 天以下（{dist_txt}），大盤沒有出貨警訊。"
    below50 = [x["ticker"] for x in rows if not x["above50"]]
    below200 = [x["ticker"] for x in rows if not x["above200"]]
    trend = []
    if len(below50) == len(rows):
        trend.append("三個指數都在 50 日線下方")
    elif below50:
        trend.append("、".join(below50) + " 在 50 日線下方")
    else:
        trend.append("三個指數都在 50 日線上方")
    if below200:
        trend.append("、".join(below200) + " 已跌破 200 日線")
    else:
        trend.append("三個指數都在 200 日線上方")
    opex_all = sorted({d for x in rows for d in x["opex_dates"]})
    block.update(rows=rows, series=series, light=light, headline=head, trend="，".join(trend) + "。",
                 warn_n=len(warn), threshold=DIST_THRESHOLD, opex_dates=opex_all,
                 ex_opex_min=min((x["dist25_ex_opex"] for x in rows), default=None))
    return block


# --------------------------------------------------------------------------- 主程式
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v7", default=os.environ.get("V7_ROOT", "~/v7-backtest"))
    ap.add_argument("--src", default=None, help="指定篩選輸出資料夾（預設自動挑最新）")
    ap.add_argument("--no-profiles", action="store_true", help="不向 yfinance 補公司全名與產業")
    a = ap.parse_args()
    v7 = Path(a.v7).expanduser()
    src, version = pick_src(v7, a.src)
    print(f"來源 {src.name}（{version}）")
    ft = None if a.src else pick_forward(v7)
    if ft:
        print(f"名單與大盤改用往後追蹤快照 {ft[0].name}")
    d = load_screen(src, version, ft[0] if ft else None)
    a_info = load_a_eps(src)

    # ---- 漏斗
    fun = {g: funnel_for(d[d["group"] == g]) for g in GROUP_LABEL if (d["group"] == g).any()}

    # ---- 名單
    full = d[d["passes"] == 5].sort_values("rs", ascending=False)
    near = d[d["passes"] == 4].copy()
    near["gate"] = near.apply(failing_gate, axis=1)
    order = {k: i for i, (k, _) in enumerate(GATES)}
    near = near.assign(_o=near["gate"].map(order)).sort_values(["_o", "rs"], ascending=[True, False])
    listed = list(full.index) + list(near.index)
    prof = {} if a.no_profiles else load_profiles(listed)

    tbg = {g: [t for t in full.index if full.loc[t, "group"] == g] for g in GROUP_LABEL}
    chart, px_last = load_chart_series(v7, d, tbg)

    def prof_of(t):
        p = prof.get(t, {})
        return dict(name=p.get("name") or d.loc[t, "name_n"], sector=SECTOR_ZH.get(p.get("sector", ""), p.get("sector", "")),
                    industry=p.get("industry", ""))

    cards = []
    for t, x in full.iterrows():
        p = prof_of(t)
        ai = a_info.get(t)
        cards.append(dict(
            ticker=t, group=x["group"], name=p["name"], sector=p["sector"], industry=p["industry"],
            roic=r(x["roic"], 4), fcf_yi=r(x["fcf"] / 1e8, 1), e0=r(x["e0"], 4), g0=r(x["g0"], 4), g1=r(x["g1"], 4), g2=r(x["g2"], 4),
            rev_path=("年增 ≥25%" if x["g0"] >= 0.25 else "連續三季加速"),
            a_cagr=r(x["a_cagr"], 4), a_eps=(ai["eps"] if ai else None), a_fy_end=clean(x["a_fy_end"]),
            off_high=r(x["off_high"], 4), close=r(x["close"], 2), hi252=r(x["hi252"], 2), rs=r(x["rs"], 1),
            bo5=bool(x["bo5"]), bo_dates=(x["bo_dates"] if isinstance(x["bo_dates"], str) else ""),
            avgvol_wan=r(x["avgvol50"] / 1e4, 0), sh_chg=r(x["sh_chg"], 4), sh_src=(x["sh_src"] if isinstance(x["sh_src"], str) else ""),
            q_end=clean(x["g_end"]), filed=clean(x["g_avail"]), chart=chart.get(t),
        ))
    nears = []
    for t, x in near.iterrows():
        p = prof_of(t)
        ai = a_info.get(t)
        nears.append(dict(
            ticker=t, group=x["group"], name=p["name"], sector=p["sector"], industry=p["industry"], gate=x["gate"],
            gate_label=dict(GATES)[x["gate"]], miss=miss_text(x, x["gate"], ai),
            roic=r(x["roic"], 4), e0=r(x["e0"], 4), a_cagr=r(x["a_cagr"], 4), off_high=r(x["off_high"], 4),
            rs=r(x["rs"], 1), bo5=bool(x["bo5"]),
        ))

    # ---- 全部表（精簡欄位）
    cols = ["t", "n", "g", "p", "q", "roic", "ce", "e0", "cr", "g0", "a", "cagr", "nn", "off", "l", "rs", "bo"]
    rows = []
    for t, x in d.sort_values(["passes", "rs"], ascending=[False, False]).iterrows():
        rows.append([t, x["name_n"], 0 if x["group"] == "large" else 1, int(x["passes"]),
                     int(x["q_ok"]), r(x["roic"], 4), int(x["c_eps_ok"]), r(x["e0"], 4), int(x["c_rev_ok"]), r(x["g0"], 4),
                     int(x["a_ok"]), r(x["a_cagr"], 4), int(x["n_ok"]), r(x["off_high"], 4), int(x["l_ok"]), r(x["rs"], 1),
                     int(x["bo5"])])

    # ---- 大盤
    mk = market_block(src, ft[1] if ft else None)

    # ---- 日期
    price_asof = px_last or mk["rows"][0]["date"] if mk["rows"] else None
    if mk["rows"]:
        price_asof = max([price_asof or ""] + [x["date"] for x in mk["rows"]])
    filed = pd.to_datetime(d["g_avail"], errors="coerce").max()
    summ = {}
    sp = src / "screen_v2_summary.json"
    if sp.exists():
        try:
            summ = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            summ = {}
    roic_before = {g: summ[g].get("roic_na_before") for g in summ if isinstance(summ.get(g), dict)}
    snap_date, ov_large = None, None
    try:
        sn = pd.read_csv(v7 / "data" / "sp400_600_pit" / "snapshots.csv")
        snap_date = str(sn["snapshot_date"].max())
        latest = sn[sn["snapshot_date"] == snap_date]
        large_t = set(d.index[d["group"] == "large"])
        ov_large = int(len(set(latest["ticker"].dropna()) & large_t))
    except Exception as e:  # noqa: BLE001
        print(f"warn: 讀不到 sp400_600_pit 快照：{e}", file=sys.stderr)
    meta = dict(
        midsmall_snapshot=snap_date, overlap_large_sp=ov_large,
        generated_at=dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M"),
        price_asof=price_asof, filings_asof=clean(filed), src_dir=src.name, version=version,
        n_total=int(len(d)), n_group={g: f["n"] for g, f in fun.items()},
        roic_na={g: f["roic_na"] for g, f in fun.items()}, roic_na_before=roic_before,
        full_n=int(len(full)), near_n=int(len(near)),
        update_note="每週六更新",
    )

    sizes = {
        "meta.json": dump("meta.json", meta),
        "market.json": dump("market.json", mk),
        "funnel.json": dump("funnel.json", dict(groups=fun, labels=GROUP_LABEL)),
        "picks.json": dump("picks.json", dict(full=cards, near=nears)),
        "table.json": dump("table.json", dict(cols=cols, rows=rows)),
    }
    for k, v in sizes.items():
        print(f"{k:14s} {v / 1024:7.1f} KB")
    pc = OUT / "profile_cache.json"
    ev = OUT / "evidence.json"
    tot = sum(sizes.values()) + (pc.stat().st_size if pc.exists() else 0) + (ev.stat().st_size if ev.exists() else 0)
    print(f"合計（含 profile_cache、evidence）{tot / 1024:.1f} KB")
    print(f"全過 {len(full)} 檔、差一條 {len(near)} 檔、價格截至 {price_asof}、財報申報截至 {meta['filings_asof']}")


if __name__ == "__main__":
    main()
