#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETF 儀表板「本站挑選」候選數據（雲端月評與季度重挑的證據包）。

讀 docs/etf-dash/data/{KEY}.json（頁面自有指標）、data/etf_dash/flows/、
data/etf_dash/long_pe/，再用 yfinance 抓 21 檔（加 TWD=X、JPY=X）的還原收盤
（auto_adjust=True，含息），算各區間含息報酬、最大回檔、波動、週 beta。
台幣、日圓計價的基金除以當日匯率換成美元。

輸出 data/etf_dash/picks_candidates.json（schema picks-candidates-v1）。
--brief 另把同一份資料印成中文純文字證據包（≤ 8 KB）：模型只能引用這份的數字。

資料品質：yfinance 偶有壞 K 棒（例如 1475.T 在 2024-08-08、08-09 收盤少一位數，
還把當日配息放大成 13.9% 的還原係數）。偵測到單日收盤偏離前後五根中位數一倍
以上的 K 棒就剔除，改用未還原收盤加配息自己算含息指數（配息併到下一根保留的
K 棒），並寫進 notes。

可單獨跑：python3 scripts/etf_dash/picks_candidates.py [--brief] [--no-write]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_etf_dash as etfdash  # noqa: E402 — 只借 yf_call_with_backoff()
import picks_track as pt  # noqa: E402 — 借 flow_1m_net()、latest_aum_usd()

REPO_ROOT = Path(__file__).resolve().parents[2]
FUND_DATA_DIR = REPO_ROOT / "docs" / "etf-dash" / "data"
LONG_PE_DIR = REPO_ROOT / "data" / "etf_dash" / "long_pe"
OUT_PATH = REPO_ROOT / "data" / "etf_dash" / "picks_candidates.json"
BENCH = "SPY"
FX_TICKER = {"TWD": "TWD=X", "JPY": "JPY=X"}
FETCH_START = "2021-01-01"
RELIABLE_FLOW_SOURCES = {"ssga_navhist", "vaneck_navhist_derived"}
# 基金 → 長期本益比檔（同 data/etf_dash/long_pe/README.md）
LONG_PE_MAP = {"SPY": "sp500", "QQQ": "ndx", "XLK": "s5inft", "XLF": "s5finl", "XLY": "s5cond",
               "XLP": "s5cons", "SMH": "sox", "SMH_UCITS": "sox", "0050": "twse", "TAIEX": "twse",
               "TOPIX": "jpx"}
BRIEF_MAX_BYTES = 8 * 1024


def fund_keys() -> list[str]:
    ov = json.loads((FUND_DATA_DIR / "overview.json").read_text(encoding="utf-8"))
    return [f["etf_key"] for f in ov["funds"]]


# ── 價格 ─────────────────────────────────────────────────────────────────
def _naive_date_index(idx):
    import pandas as pd
    idx = pd.DatetimeIndex(idx)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    return idx.normalize()


def find_bad_bars(close) -> list:
    """單日收盤偏離前後各兩根（共四根，不含自己）中位數 > 100% 或 < 50% 的日期。"""
    import numpy as np
    vals = close.values.astype(float)
    bad = []
    for i in range(len(vals)):
        nb = np.concatenate([vals[max(0, i - 2):i], vals[i + 1:i + 3]])
        nb = nb[~np.isnan(nb)]
        if len(nb) < 2 or np.isnan(vals[i]):
            continue
        med = float(np.median(nb))
        if med > 0 and (vals[i] / med < 0.5 or vals[i] / med > 2.0):
            bad.append(close.index[i])
    return bad


def fetch_total_return(tk: str, notes: list[str]):
    """回傳含息還原收盤 pandas.Series（index＝當地日期、無時區）。"""
    import pandas as pd
    import yfinance as yf

    h = etfdash.yf_call_with_backoff(
        lambda: yf.Ticker(tk).history(start=FETCH_START, auto_adjust=True), label=f"cand {tk}")
    if h is None or h.empty:
        raise RuntimeError("empty history")
    h = h.copy()
    h.index = _naive_date_index(h.index)
    h = h[~h.index.duplicated(keep="last")]
    adj = h["Close"].dropna()
    bad = find_bad_bars(adj)
    if not bad:
        return adj
    # 壞 K 棒：改用未還原收盤＋配息自己算
    raw = etfdash.yf_call_with_backoff(
        lambda: yf.Ticker(tk).history(start=FETCH_START, auto_adjust=False), label=f"cand-raw {tk}")
    raw = raw.copy()
    raw.index = _naive_date_index(raw.index)
    raw = raw[~raw.index.duplicated(keep="last")]
    close = raw["Close"].dropna()
    divs = raw["Dividends"].fillna(0.0) if "Dividends" in raw else pd.Series(0.0, index=close.index)
    bad_raw = find_bad_bars(close)
    carry, factor, prev, out = 0.0, 1.0, None, {}
    for d, c in close.items():
        dv = float(divs.get(d, 0.0))
        if d in bad_raw:
            carry += dv
            continue
        dv += carry
        carry = 0.0
        if prev is not None and dv > 0 and prev > 0:
            factor *= 1.0 + dv / prev
        out[d] = c * factor
        prev = c
    s = pd.Series(out).sort_index()
    s.index = pd.DatetimeIndex(s.index)
    notes.append(f"{tk} 的 yfinance 資料在 {', '.join(b.strftime('%Y-%m-%d') for b in bad_raw)} 有壞 K 棒（收盤偏離前後中位數一倍以上），"
                 f"已剔除，含息報酬改用未還原收盤加配息自己算（配息併到下一根保留的 K 棒）。")
    return s


def last_closed_date(now: datetime.datetime | None = None) -> datetime.date:
    """美股最後一個已收盤的交易日上界：紐約時間 16:30 前，今天的 K 棒算盤中，不用。"""
    from zoneinfo import ZoneInfo
    now = (now or datetime.datetime.now(datetime.timezone.utc)).astimezone(ZoneInfo("America/New_York"))
    d = now.date()
    if now.hour < 16 or (now.hour == 16 and now.minute < 30):
        d -= datetime.timedelta(days=1)
    return d


# ── 指標 ─────────────────────────────────────────────────────────────────
def window_return(s, start: str, end: str | None = None, *, pre_start: bool = False):
    """回傳 (報酬 %, 起點日) 或 (None, None)。起點＝start 當日或之後第一根（pre_start＝start 之前最後一根）；
    序列首日比起點晚超過 6 天視為歷史不足。"""
    import pandas as pd
    st = pd.Timestamp(start)
    sub = s[s.index <= pd.Timestamp(end)] if end else s
    if sub.empty:
        return None, None
    if pre_start:
        before = sub[sub.index < st]
        if before.empty:
            return None, None
        base_d = before.index[-1]
    else:
        after = sub[sub.index >= st]
        if after.empty or (after.index[0] - st).days > 6 or sub.index[0] > st + pd.Timedelta(days=6):
            return None, None
        base_d = after.index[0]
    seg = sub[sub.index >= base_d]
    if len(seg) < 2:
        return None, None
    return round((seg.iloc[-1] / seg.iloc[0] - 1) * 100, 1), base_d.strftime("%Y-%m-%d")


def window_mdd(s, start: str):
    import pandas as pd
    st = pd.Timestamp(start)
    seg = s[s.index >= st]
    if len(seg) < 2 or (seg.index[0] - st).days > 6 or s.index[0] > st + pd.Timedelta(days=6):
        return None
    return round(float((seg / seg.cummax() - 1).min()) * 100, 1)


def vol_beta(s, spy, start: str):
    """近三年年化波動（日報酬，同 build 慣例用實際交易日數年化）與對 SPY 的週報酬 beta。"""
    import numpy as np
    import pandas as pd
    st = pd.Timestamp(start)
    if s.index[0] > st + pd.Timedelta(days=6):
        return None, None
    sub = s[s.index >= st]
    r = sub.pct_change().dropna()
    yrs = (sub.index[-1] - sub.index[0]).days / 365.25
    vol = round(float(r.std() * np.sqrt(len(r) / yrs)) * 100, 1) if len(r) > 20 and yrs > 0 else None
    u = pd.concat([s.rename("f"), spy.rename("m")], axis=1).sort_index().ffill()
    u = u[(u.index >= st) & (u.index <= s.index[-1])]
    wk = u.resample("W-FRI").last().pct_change().dropna()
    beta = None
    if len(wk) > 20 and wk["m"].var() > 0:
        beta = round(float(wk.cov().iloc[0, 1] / wk["m"].var()), 2)
    return vol, beta


def overlap_matrix(fund_json: dict[str, dict]) -> dict[str, float]:
    """加權 min 和：兩檔持股（只算有 EPS 的成分股 constituents）相同代號各取較小權重相加。"""
    w = {}
    for k, d in fund_json.items():
        m: dict[str, float] = {}
        for x in d.get("constituents") or []:
            m[x["ticker"]] = m.get(x["ticker"], 0.0) + x["weight_pct"]
        w[k] = m
    keys = list(fund_json)
    out = {}
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            out[f"{a}|{b}"] = round(float(sum(min(v, w[b][t]) for t, v in w[a].items() if t in w[b])), 1)
    return out


def page_metrics(key: str, d: dict, fx_now: dict) -> dict:
    per = {p["key"]: p for p in d.get("periods") or []}
    fs = ((d.get("forward_summary") or {}).get("fy1")) or {}
    cons = sorted(d.get("constituents") or [], key=lambda x: -x["weight_pct"])
    cur, src, aum = None, None, None
    try:
        rows = [ln for ln in (REPO_ROOT / "data" / "etf_dash" / "flows" / f"{key}.jsonl").read_text(encoding="utf-8").splitlines() if ln.strip()]
        last = json.loads(rows[-1])
        cur, src = last.get("nav_currency"), last.get("source")
        fx = fx_now.get(cur or "USD") or 1.0
        if last.get("shares_outstanding") and last.get("nav"):
            aum = float(last["shares_outstanding"]) * float(last["nav"]) / fx
    except (OSError, ValueError, IndexError, TypeError):
        fx = fx_now.get("USD") or 1.0
    flow = pt.flow_1m_net(d)
    flow_fx = fx_now.get(((d.get("flows") or {}).get("daily") or [{}])[-1].get("nav_currency") or "USD") or 1.0
    flow_usd = round(flow / flow_fx / 1e9, 2) if flow is not None else None
    out = {
        "fwd_pe": (d.get("weighted_forward_pe") or {}).get("value"),
        "fy1_eps_growth_pct": fs.get("eps_growth_pct"), "fy1_peg": fs.get("peg"), "fy1_rev_3m_pct": fs.get("rev_3m_pct"),
        "eps_chg_30d_pct": (per.get("30d") or {}).get("eps_chg_pct"),
        "price_chg_30d_pct": (per.get("30d") or {}).get("price_chg_pct"),
        "implied_pe_chg_30d_pct": (per.get("30d") or {}).get("implied_pe_chg_pct"),
        "eps_chg_90d_pct": (per.get("90d") or {}).get("eps_chg_pct"),
        "breadth_90d_up_pct": (((d.get("breadth") or {}).get("90d")) or {}).get("up_weight_pct"),
        "top10_pct": round(sum(x["weight_pct"] for x in cons[:10]), 1) if cons else None,
        "n_holdings": d.get("n_holdings"),
        "scale_usd_bn": round(aum / 1e9, 1) if aum else None,
        "flow_1m_usd_bn": flow_usd,
        "flow_source": src, "flow_reliable": bool(src in RELIABLE_FLOW_SOURCES),
        "holdings_approx": bool(d.get("holdings_approximation_zh")),
        "holdings_as_of": d.get("holdings_as_of"), "eps_as_of": d.get("eps_as_of"),
        "pe_hist_pctile": None, "pe_hist_median": None, "pe_hist_from": None,
    }
    for k in ("fwd_pe", "fy1_eps_growth_pct", "fy1_peg", "fy1_rev_3m_pct", "eps_chg_30d_pct", "price_chg_30d_pct",
              "implied_pe_chg_30d_pct", "eps_chg_90d_pct", "breadth_90d_up_pct"):
        if out[k] is not None:
            out[k] = round(float(out[k]), 2)
    lp = LONG_PE_MAP.get(key)
    if lp and (LONG_PE_DIR / f"{lp}.csv").exists() and out["fwd_pe"] is not None:
        import pandas as pd
        s = pd.read_csv(LONG_PE_DIR / f"{lp}.csv", parse_dates=["date"])
        cur_pe = float(s["pe"].iloc[-1])
        out["pe_hist_pctile"] = round(float((s["pe"] <= cur_pe).mean() * 100), 0)
        out["pe_hist_median"] = round(float(s["pe"].median()), 1)
        out["pe_hist_from"] = s["date"].iloc[0].strftime("%Y-%m")
    return out


# ── 主流程 ───────────────────────────────────────────────────────────────
def build_candidates(prices_override: dict | None = None) -> dict:
    """prices_override：測試用，{ticker: pandas.Series} 直接給價格，不抓 yfinance。"""
    import pandas as pd

    notes: list[str] = []
    keys = fund_keys()
    fund_json, ticker_of = {}, {}
    for k in keys:
        p = FUND_DATA_DIR / f"{k}.json"
        try:
            fund_json[k] = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            notes.append(f"{k}：頁面資料 {p.name} 讀不到，頁面指標留空。")
            continue
    for k in keys:
        d = fund_json.get(k) or {}
        ticker_of[k] = d.get("yf_ticker")
    cur_of = {k: ("TWD" if (ticker_of[k] or "").endswith(".TW") or ticker_of[k] == "^TWII"
                  else "JPY" if (ticker_of[k] or "").endswith(".T") else "USD") for k in keys}

    tickers = sorted({t for t in ticker_of.values() if t} | set(FX_TICKER.values()))
    series, fetch_notes = {}, notes
    for tk in tickers:
        try:
            s = (prices_override or {}).get(tk)
            series[tk] = s if s is not None else fetch_total_return(tk, fetch_notes)
        except Exception as e:  # noqa: BLE001
            notes.append(f"{tk}：價格抓取失敗（{e}），相關報酬格留空。")

    cutoff = pd.Timestamp(last_closed_date())
    for tk in list(series):
        series[tk] = series[tk][series[tk].index <= cutoff]

    spy_tk = ticker_of.get(BENCH)
    if spy_tk not in series or series[spy_tk].empty:
        raise RuntimeError("SPY 價格抓取失敗，無法決定 as_of")
    as_of_ts = series[spy_tk].index[-1]
    as_of = as_of_ts.strftime("%Y-%m-%d")

    usd = {}
    for k in keys:
        tk = ticker_of.get(k)
        if tk not in series:
            continue
        s = series[tk].dropna()
        cur = cur_of[k]
        if cur != "USD":
            fxs = series.get(FX_TICKER[cur])
            if fxs is None:
                notes.append(f"{k}：缺 {FX_TICKER[cur]} 匯率，無法換美元，報酬格留空。")
                continue
            fx = fxs.reindex(s.index.union(fxs.index)).ffill().reindex(s.index)
            s = (s / fx).dropna()
        usd[k] = s
    spy = usd[BENCH]

    fx_now = {"USD": 1.0}
    for cur, ft in FX_TICKER.items():
        if ft in series and not series[ft].empty:
            fx_now[cur] = float(series[ft].iloc[-1])

    d_as = as_of_ts.to_pydatetime()
    def minus(months=0, years=0):
        return (as_of_ts - pd.DateOffset(months=months, years=years)).strftime("%Y-%m-%d")
    starts = {"r3m": minus(months=3), "r6m": minus(months=6), "r1y": minus(years=1), "r3y": minus(years=3)}
    ytd_start = f"{d_as.year}-01-01"

    funds = []
    for k in keys:
        s = usd.get(k)
        row = {"key": k, "label_zh": (fund_json.get(k) or {}).get("label_zh"), "yf_ticker": ticker_of.get(k),
               "currency": cur_of[k], "first_date": None, "last_date": None,
               "r3m_pct": None, "r6m_pct": None, "ytd_pct": None, "r1y_pct": None, "r3y_pct": None,
               "bear2022_pct": None, "mdd_1y_pct": None, "mdd_3y_pct": None, "mdd_5y_pct": None,
               "vol_3y_pct": None, "beta_3y_weekly": None, "r1y_start": None, "r3y_start": None}
        if s is not None and len(s) > 1:
            row["first_date"] = s.index[0].strftime("%Y-%m-%d")
            row["last_date"] = s.index[-1].strftime("%Y-%m-%d")
            if (as_of_ts - s.index[-1]).days > 4:
                notes.append(f"{k}：價格只到 {row['last_date']}，各區間報酬以該日為終點，與 {as_of} 差 {(as_of_ts - s.index[-1]).days} 天。")
            for name, st in starts.items():
                v, base = window_return(s, st)
                row[f"{name}_pct"] = v
                if name in ("r1y", "r3y"):
                    row[f"{name}_start"] = base
            row["ytd_pct"], _ = window_return(s, ytd_start, pre_start=True)
            row["bear2022_pct"], _ = window_return(s, "2022-01-03", "2022-10-12")
            row["mdd_1y_pct"] = window_mdd(s, starts["r1y"])
            row["mdd_3y_pct"] = window_mdd(s, starts["r3y"])
            row["mdd_5y_pct"] = window_mdd(s, minus(years=5))
            row["vol_3y_pct"], row["beta_3y_weekly"] = vol_beta(s, spy, starts["r3y"])
            if row["r3y_pct"] is None:
                notes.append(f"{k}：{row['first_date']} 才開始有價格，近三年與 2022 空頭留空。")
            elif row["bear2022_pct"] is None:
                notes.append(f"{k}：{row['first_date']} 才開始有價格，2022 空頭留空。")
        else:
            notes.append(f"{k}：沒有價格資料。")
        d = fund_json.get(k)
        row.update(page_metrics(k, d, fx_now) if d else {})
        funds.append(row)
    # 欄位固定：頁面指標缺檔時補 None
    page_keys = list(page_metrics("_", {}, fx_now).keys())
    for r in funds:
        for pk in page_keys:
            r.setdefault(pk, None)

    for k in keys:
        fd = fund_json.get(k) or {}
        if fd.get("holdings_approximation_zh"):
            notes.append(f"{k}：持股是近似值（{fd['holdings_approximation_zh']}）")
        if fd.get("holdings_stale"):
            notes.append(f"{k}：持股檔已過期。")
    notes.append("近一個月申贖與規模：flow_reliable=false 的基金（yfinance 推算的流通單位）不要拿來比大小或下結論。")
    notes.append("今年以來＝上年最後一個交易日收盤起算；其餘區間＝起算日當天（或之後第一個交易日）收盤起算。")

    return {
        "schema": "picks-candidates-v1", "as_of": as_of, "benchmark": BENCH,
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "windows": {"r3m_start": starts["r3m"], "r6m_start": starts["r6m"], "r1y_start": starts["r1y"],
                    "r3y_start": starts["r3y"], "ytd_base": "上年最後交易日收盤", "bear2022": "2022-01-03～2022-10-12"},
        "funds": funds, "overlap": overlap_matrix({k: v for k, v in fund_json.items()}), "notes": notes,
    }


# ── 證據包 ───────────────────────────────────────────────────────────────
def _f(v, nd=1, sign=False, suffix=""):
    if v is None:
        return "—"
    return (f"{v:+.{nd}f}" if sign else f"{v:.{nd}f}") + suffix


def brief_text(c: dict, pair_min: float = 25.0) -> str:
    L = []
    A = L.append
    A(f"ETF 儀表板 21 檔候選證據包｜資料日 {c['as_of']}｜基準 {c['benchmark']}")
    A("只有這份裡出現的數字可以引用；表上沒有的數字不要寫。報酬一律美元含息（台幣、日圓基金已換美元），單位 %。")
    A(f"起算日：近三個月 {c['windows']['r3m_start']}、近六個月 {c['windows']['r6m_start']}、近一年 {c['windows']['r1y_start']}、近三年 {c['windows']['r3y_start']}；"
      f"今年以來自上年最後交易日收盤；2022 空頭 {c['windows']['bear2022']}。— 代表資料不足或缺值。")
    A("")
    A("一、含息報酬與風險")
    A(f"{'基金':<10}{'3個月':>7}{'6個月':>7}{'今年':>7}{'1年':>7}{'3年':>8}{'2022':>7}{'回檔1y':>8}{'回檔3y':>8}{'回檔5y':>8}{'波動3y':>7}{'beta':>6}")
    for r in c["funds"]:
        A(f"{r['key']:<10}{_f(r['r3m_pct'], sign=True):>7}{_f(r['r6m_pct'], sign=True):>7}{_f(r['ytd_pct'], sign=True):>7}"
          f"{_f(r['r1y_pct'], sign=True):>7}{_f(r['r3y_pct'], sign=True):>8}{_f(r['bear2022_pct'], sign=True):>7}"
          f"{_f(r['mdd_1y_pct']):>8}{_f(r['mdd_3y_pct']):>8}{_f(r['mdd_5y_pct']):>8}{_f(r['vol_3y_pct']):>7}{_f(r['beta_3y_weekly'], 2):>6}")
    A("回檔＝區間內最大回檔；波動＝近三年年化；beta＝近三年週報酬對 SPY。")
    A("")
    A("二、估值、盈餘與成分股（成分股加權，明年度 EPS）")
    A(f"{'基金':<10}{'遠期PE':>7}{'歷史位':>7}{'EPS成長':>8}{'PEG':>6}{'3月上修':>8}{'上修寬度':>8}{'30日EPS':>8}{'30日價':>8}{'前十大':>7}")
    for r in c["funds"]:
        pe_h = f"{int(r['pe_hist_pctile'])}" if r["pe_hist_pctile"] is not None else "—"
        A(f"{r['key']:<10}{_f(r['fwd_pe']):>7}{pe_h:>7}{_f(r['fy1_eps_growth_pct'], sign=True):>8}{_f(r['fy1_peg'], 2):>6}"
          f"{_f(r['fy1_rev_3m_pct'], sign=True):>8}{_f(r['breadth_90d_up_pct']):>8}{_f(r['eps_chg_30d_pct'], sign=True):>8}"
          f"{_f(r['price_chg_30d_pct'], sign=True):>8}{_f(r['top10_pct']):>7}")
    hist = [f"{r['key']} 中位數 {r['pe_hist_median']:.1f}（{r['pe_hist_from']} 起）" for r in c["funds"] if r["pe_hist_median"] is not None]
    A("歷史位＝現值在自己長期預估本益比樣本裡的百分位；" + "、".join(hist) + "。")
    A("")
    A("三、規模與近一月申贖（億美元）")
    A(f"{'基金':<10}{'規模':>8}{'近一月淨申贖':>12}  可信")
    for r in c["funds"]:
        sc = f"{r['scale_usd_bn'] * 10:,.0f}" if r["scale_usd_bn"] is not None else "—"
        fl = f"{r['flow_1m_usd_bn'] * 10:+,.1f}" if r["flow_1m_usd_bn"] is not None else "—"
        A(f"{r['key']:<10}{sc:>8}{fl:>12}  {'是' if r['flow_reliable'] else '否'}")
    A("")
    pairs = sorted(((v, k) for k, v in c["overlap"].items() if v >= pair_min), reverse=True)
    A(f"四、持股重疊（加權 min 和，只列 ≥ {pair_min:.0f}%；其餘組合低於此值，完整矩陣在 picks_candidates.json）")
    A("、".join(f"{k.replace('|', '×')} {v:.1f}%" for v, k in pairs) if pairs else "無")
    A("")
    A("五、資料品質註記")
    for n in c["notes"]:
        A("・" + n)
    return "\n".join(L) + "\n"


def brief_within_limit(c: dict) -> str:
    """超過 8 KB 時依序收緊：重疊門檻 25→30→40，註記只留前 12 條。"""
    for pair_min in (25.0, 30.0, 40.0):
        t = brief_text(c, pair_min)
        if len(t.encode("utf-8")) <= BRIEF_MAX_BYTES:
            return t
    c2 = dict(c, notes=c["notes"][:12])
    return brief_text(c2, 40.0)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--brief", action="store_true", help="印中文證據包（≤ 8 KB）")
    ap.add_argument("--no-write", action="store_true", help="不寫 data/etf_dash/picks_candidates.json")
    args = ap.parse_args()
    c = build_candidates()
    if not args.no_write:
        OUT_PATH.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.brief:
        t = brief_within_limit(c)
        sys.stdout.write(t)
        print(f"[brief] {len(t.encode('utf-8'))} bytes", file=sys.stderr)
    else:
        print(f"as_of={c['as_of']} funds={len(c['funds'])} notes={len(c['notes'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
