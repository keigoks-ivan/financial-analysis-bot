#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETF 儀表板「本站挑選」攻方理由的歷史基率（每季登記前必跑，skill picks-monthly v1.3）。

  python3 scripts/etf_dash/picks_base_rate.py --attack SMH --registered-on 2026-10-29 \\
      [--out /tmp/picks/base_rate_etf-dash.json] [--brief] [--price-source auto|store|yf]

對攻方的三條挑選規則，各問一次：「歷史上這個條件成立的那些週，之後 52 週贏 SPY 的機率與
平均超額，跟所有週比起來有沒有比較好？」

  (a) 近一年贏基準：該檔過去 52 週含息報酬高於 SPY（該檔自己的週資料，非美元計價換美元）。
  (b) 三個月上修高於基準且寬度 > 60%：代理口徑＝代理指數的隱含預估 EPS（未還原收盤 ÷ 預估
      本益比）13 週變化高於標普 500 的同一數字。寬度沒有歷史，不進條件。
  (c) PEG 最低：代理口徑＝代理指數預估本益比在過去十年的分位 ≤ 50（十年窗含當週，至少滿五年才算）。

代理序列（data/etf_dash/long_pe/）：SMH、SMH_UCITS→SOX；QQQ→NDX；XLK→INFT；XLF→FINL；
XLY→COND；XLP→CONS；SPY、RSP→SP500。其他檔（XLV、XLE、XLI、XLB、XLC、單一國家）只有 (a)，
(b)(c) 輸出「無基率」。RSP 的 (b) 代理就是基準本身，條件無法區分，也是「無基率」。

報酬一律用攻方自己的含息收盤對 SPY 含息收盤（SMH_UCITS 用 SMH 代替，歷史較長）；只用登記日
（含）以前已經走完 52 週的樣本，不偷看未來。

判定門檻（寫死，見 THRESHOLD）：條件內平均超額減所有週 ≥ 3 個百分點，且條件內對條件外的
Newey-West t ≥ 2，才判「有預測力」；條件內不足 52 週或獨立事件不足 5 次判「無基率」；其餘「沒有」。
這是事先寫死的分類線，不是結論。

價格來源：--price-source auto（預設）＝本機有 ~/v7-backtest/src/price_store.py 就用共用價格庫，
否則用 yfinance（雲端 CI）。yfinance 只在記憶體裡用，不存檔。

輸出 JSON（schema picks-base-rate-v1）；brief 欄是中文證據行，check_picks_text.py 會把它併進證據。
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LONG_PE_DIR = REPO_ROOT / "data" / "etf_dash" / "long_pe"
CANDIDATES_PATH = REPO_ROOT / "data" / "etf_dash" / "picks_candidates.json"
PRICE_STORE_SRC = Path.home() / "v7-backtest" / "src"
BENCH = "SPY"
H = 52  # 持有週數
MINUS = "−"

# 代理序列：名稱 → (long_pe 檔, 訊號用未還原收盤代號)
SERIES = {
    "SOX": ("sox.csv", "^SOX"), "NDX": ("ndx.csv", "^NDX"), "SP500": ("sp500.csv", "^GSPC"),
    "INFT": ("s5inft.csv", "XLK"), "FINL": ("s5finl.csv", "XLF"), "COND": ("s5cond.csv", "XLY"),
    "CONS": ("s5cons.csv", "XLP"),
}
SERIES_ZH = {"SOX": "費城半導體", "NDX": "那斯達克 100", "SP500": "標普 500", "INFT": "標普 500 資訊科技",
             "FINL": "標普 500 金融", "COND": "標普 500 非必需消費", "CONS": "標普 500 必需消費"}
PROXY = {"SMH": "SOX", "SMH_UCITS": "SOX", "QQQ": "NDX", "XLK": "INFT", "XLF": "FINL", "XLY": "COND",
         "XLP": "CONS", "SPY": "SP500", "RSP": "SP500"}
RET_PROXY = {"SMH_UCITS": "SMH"}  # 報酬改用同指數、歷史較長的美國掛牌
FX_TICKER = {"TWD": "TWD=X", "JPY": "JPY=X"}

THRESHOLD = {
    "min_diff_pp": 3.0, "min_nw_t": 2.0, "min_cond_weeks": 52, "min_episodes": 5, "episode_gap_days": 91,
    "note": "判定門檻是事先寫死的分類線，不是結論：差＝條件內平均超額減所有週；t＝條件內對條件外的 "
            "Newey-West t（落後＝持有週數）。獨立次數少、多條規則一起測，t 都會偏樂觀。",
}
VERDICT_YES, VERDICT_NO, VERDICT_NA = "有預測力", "沒有", "無基率"
RULE_NAMES = {"a": "近一年贏基準", "b": "三個月上修高於基準且寬度 > 60%", "c": "PEG 最低（評價最便宜）"}


class BaseRateError(Exception):
    pass


# ── 價格 ─────────────────────────────────────────────────────────────────
def _naive(idx):
    import pandas as pd
    idx = pd.DatetimeIndex(idx)
    return (idx.tz_localize(None) if idx.tz is not None else idx).normalize()


def load_prices(tickers: list[str], source: str = "auto", end: str | None = None):
    """回傳 (adj 寬表, close 寬表, 實際來源)。adj＝含息還原收盤，close＝未還原收盤。"""
    import pandas as pd
    tickers = list(dict.fromkeys(tickers))
    use_store = source == "store" or (source == "auto" and (PRICE_STORE_SRC / "price_store.py").exists())
    if use_store:
        if str(PRICE_STORE_SRC) not in sys.path:
            sys.path.insert(0, str(PRICE_STORE_SRC))
        from price_store import get_prices  # type: ignore
        adj = get_prices(tickers, "1989-01-01", end, field="adj_close")
        cl = get_prices(tickers, "1989-01-01", end, field="close")
        return adj, cl, "price_store"
    import yfinance as yf
    raw = yf.download(tickers, start="1989-01-01", auto_adjust=False, actions=False, progress=False,
                      group_by="column", threads=True)
    if raw is None or raw.empty:
        raise BaseRateError("yfinance 沒有回傳價格")
    adj = raw["Adj Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Adj Close"]].set_axis(tickers, axis=1)
    cl = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].set_axis(tickers, axis=1)
    adj.index, cl.index = _naive(adj.index), _naive(cl.index)
    if end:
        adj, cl = adj.loc[:pd.Timestamp(end)], cl.loc[:pd.Timestamp(end)]
    return adj, cl, "yfinance"


def asof(series, dates, tol_days: int = 6):
    """每個日期取 ≤ 該日最近一筆，距離超過 tol_days 給 NaN。"""
    import numpy as np
    import pandas as pd
    s = series.dropna()
    dates = pd.DatetimeIndex(dates)
    if s.empty:
        return np.full(len(dates), np.nan)
    idx = s.index.searchsorted(dates, side="right") - 1
    ok = idx >= 0
    ci = np.clip(idx, 0, None)
    lag = (dates - s.index[ci]).days
    return np.where(ok & (lag <= tol_days), s.values[ci], np.nan)


# ── 統計 ─────────────────────────────────────────────────────────────────
def nw_t(x, d, lag: int) -> float:
    """x 對 0／1 虛擬變數 d 迴歸的斜率 t（Newey-West，Bartlett 權重）。斜率＝條件內減條件外。"""
    import numpy as np
    x = np.asarray(x, float)
    d = np.asarray(d, float)
    if d.sum() < 2 or (1 - d).sum() < 2:
        return float("nan")
    X = np.column_stack([np.ones(len(x)), d])
    # 用 einsum 不用 @：macOS Accelerate 版 numpy 的 matmul 會丟假的除以零警告
    XtX = np.einsum("ni,nj->ij", X, X)
    beta = np.linalg.solve(XtX, np.einsum("ni,n->i", X, x))
    e = x - np.einsum("ni,i->n", X, beta)
    S = X * e[:, None]
    n = len(S)
    L = min(lag, n - 1)
    om = np.einsum("ni,nj->ij", S, S)
    for k in range(1, L + 1):
        w = 1 - k / (L + 1)
        g = np.einsum("ni,nj->ij", S[k:], S[:-k])
        om += w * (g + g.T)
    xi = np.linalg.inv(XtX)
    v = np.einsum("ij,jk,kl->il", xi, om, xi)
    se = math.sqrt(v[1, 1]) if v[1, 1] > 0 else float("nan")
    return float(beta[1] / se) if se and not math.isnan(se) else float("nan")


def episodes(dates, gap_days: int) -> int:
    import pandas as pd
    n, last = 0, None
    for dt in pd.DatetimeIndex(dates):
        if last is None or (dt - last).days > gap_days:
            n += 1
        last = dt
    return n


def _r(v, nd=1):
    return None if v is None or (isinstance(v, float) and math.isnan(v)) else round(float(v), nd) + 0.0  # −0.0 → 0.0


def summarize(dates, x, mask, lag: int) -> dict:
    """dates 依序；x＝之後 52 週超額（小數）；mask＝條件成立。回傳百分比、四捨五入後的統計與判定。"""
    import numpy as np
    import pandas as pd
    dates = pd.DatetimeIndex(dates)
    x = np.asarray(x, float)
    m = np.asarray(mask, bool)
    out = {"sample_start": dates[0].strftime("%Y-%m-%d") if len(dates) else None,
           "sample_end": dates[-1].strftime("%Y-%m-%d") if len(dates) else None,
           "n_weeks": int(len(x)), "n_cond_weeks": int(m.sum())}
    if len(x) == 0 or m.sum() == 0:
        out.update(episodes=0, excess_cond_pct=None, excess_all_pct=_r(x.mean() * 100) if len(x) else None,
                   diff_pct=None, hit_cond_pct=None, hit_all_pct=_r((x > 0).mean() * 100) if len(x) else None,
                   nw_t=None)
        return out
    ec, ea = x[m].mean() * 100, x.mean() * 100
    out.update(episodes=episodes(dates[m], THRESHOLD["episode_gap_days"]),
               excess_cond_pct=_r(ec), excess_all_pct=_r(ea), diff_pct=_r(ec - ea),
               hit_cond_pct=_r((x[m] > 0).mean() * 100), hit_all_pct=_r((x > 0).mean() * 100),
               nw_t=_r(nw_t(x, m, lag), 2))
    return out


def verdict(st: dict) -> tuple[str, str]:
    th = THRESHOLD
    if st.get("excess_cond_pct") is None:
        return VERDICT_NA, "條件在樣本裡沒有成立過"
    if st["n_cond_weeks"] == st["n_weeks"]:
        return VERDICT_NA, "條件每一週都成立，沒有對照組"
    if st["n_cond_weeks"] < th["min_cond_weeks"] or st["episodes"] < th["min_episodes"]:
        return VERDICT_NA, (f"樣本不足：條件內 {st['n_cond_weeks']} 週、獨立 {st['episodes']} 次"
                            f"（門檻 {th['min_cond_weeks']} 週、{th['min_episodes']} 次）")
    t = st.get("nw_t")
    if st["diff_pct"] >= th["min_diff_pp"] and t is not None and t >= th["min_nw_t"]:
        return VERDICT_YES, "差與 t 都過門檻"
    if st["diff_pct"] <= -th["min_diff_pp"] and t is not None and t <= -th["min_nw_t"]:
        return VERDICT_NO, "反向：條件成立的週之後反而比較差"
    return VERDICT_NO, "差或 t 沒過門檻"


# ── 序列 ─────────────────────────────────────────────────────────────────
def weekly(s):
    """日線 → 每週最後一個交易日（保留實際日期，不用週五標籤）。"""
    s = s.dropna()
    return s.groupby(s.index.to_period("W-FRI")).tail(1)


def fund_usd(adj, ticker: str, currency: str):
    s = adj[ticker].dropna() if ticker in adj else None
    if s is None or s.empty:
        raise BaseRateError(f"{ticker} 沒有價格")
    if currency and currency != "USD":
        fxt = FX_TICKER.get(currency)
        if not fxt or fxt not in adj or adj[fxt].dropna().empty:
            raise BaseRateError(f"{ticker} 是 {currency} 計價，缺匯率 {fxt}")
        fx = adj[fxt].dropna()
        fx = fx.reindex(s.index.union(fx.index)).ffill().reindex(s.index)
        s = (s / fx).dropna()
    return s


def forward_excess(fund, spy, dates, cutoff):
    """dates 起算之後 52 週（364 天）含息報酬差；終點超過 cutoff 的給 NaN。"""
    import numpy as np
    import pandas as pd
    dates = pd.DatetimeIndex(dates)
    tgt = dates + pd.Timedelta(days=7 * H)
    a0, a1 = asof(fund, dates), asof(fund, tgt)
    b0, b1 = asof(spy, dates), asof(spy, tgt)
    ok = np.asarray(tgt <= pd.Timestamp(cutoff))
    return np.where(ok, (a1 / a0 - 1) - (b1 / b0 - 1), np.nan)


def pe_panel(name: str, close, long_pe_dir: Path = LONG_PE_DIR):
    """一條代理序列：date、pe、隱含 EPS 13 週變化 eps13、十年分位 pct10。"""
    import numpy as np
    import pandas as pd
    fn, sig = SERIES[name]
    pe = pd.read_csv(long_pe_dir / fn, parse_dates=["date"]).sort_values("date").drop_duplicates("date")
    pe = pe[pe["pe"] > 0].reset_index(drop=True)
    monthly = pe["date"].diff().dt.days.median() > 20
    tol_lag = 12 if monthly else 5
    if sig not in close or close[sig].dropna().empty:
        raise BaseRateError(f"{name} 的訊號價格 {sig} 沒有資料")
    pe["sigp"] = asof(close[sig], pe["date"])
    pe["eps"] = pe["sigp"] / pe["pe"]
    ref = pe.set_index("date")
    t0 = pd.DatetimeIndex(pe["date"] - pd.Timedelta(days=91))
    near = ref.index.get_indexer(t0, method="nearest")
    dd = np.abs((ref.index[near] - t0).days)
    eps_l = np.where(dd <= tol_lag, ref["eps"].values[near], np.nan)
    pe["eps13"] = pe["eps"] / eps_l - 1
    dates, pv = pe["date"].values, pe["pe"].values
    pct = np.full(len(pe), np.nan)
    for i in range(len(pe)):
        lo = dates[i] - np.timedelta64(3652, "D")
        j0 = np.searchsorted(dates, lo, side="left")
        w = pv[j0:i + 1]
        if (dates[i] - dates[j0]) >= np.timedelta64(5 * 365, "D"):
            pct[i] = (w <= pv[i]).mean() * 100
    pe["pct10"] = pct
    return pe


def _lag(p) -> int:
    """Newey-West 落後期數：週資料＝持有週數，月資料（金融）換算成月數。"""
    return math.ceil(H / 4.33) if p["date"].diff().dt.days.median() > 20 else H


# ── 三條規則 ─────────────────────────────────────────────────────────────
def rule_a(code: str, fund, spy, cutoff) -> dict:
    import numpy as np
    import pandas as pd
    f, b = weekly(fund), weekly(spy)
    f, b = f[f.index <= pd.Timestamp(cutoff)], b[b.index <= pd.Timestamp(cutoff)]
    df = pd.concat([f.rename("f"), b.rename("b")], axis=1).dropna()
    past = (df["f"] / df["f"].shift(H) - 1) - (df["b"] / df["b"].shift(H) - 1)
    x = forward_excess(fund, spy, df.index, cutoff)
    ok = past.notna().values & ~np.isnan(x)
    st = summarize(df.index[ok], x[ok], (past.values > 0)[ok], H)
    now_i = past.dropna()
    now = None
    if not now_i.empty:
        last = now_i.index[-1]
        fr = df["f"].iloc[-1] / df["f"].shift(H).iloc[-1] - 1
        br = df["b"].iloc[-1] / df["b"].shift(H).iloc[-1] - 1
        now = {"as_of": last.strftime("%Y-%m-%d"), "met": bool(now_i.iloc[-1] > 0),
               "fund_52w_pct": _r(fr * 100), "bench_52w_pct": _r(br * 100)}
    return {"condition": f"{code} 過去 52 週含息報酬高於 {BENCH}", "proxy": f"{code} 自己的週收盤（美元含息）",
            **st, "now": now}


def _ret_note(code: str, ret_tk: str) -> str:
    return f"；報酬用 {ret_tk} 代替" if ret_tk != code else ""


def rule_b(code: str, proxy: str, panels: dict, fund, spy, cutoff, ret_tk: str) -> dict:
    import numpy as np
    import pandas as pd
    p, sp = panels[proxy], panels["SP500"]
    base = {"condition": f"{SERIES_ZH[proxy]}隱含預估 EPS 13 週變化高於標普 500",
            "proxy": f"{proxy}（data/etf_dash/long_pe，隱含 EPS＝未還原收盤 ÷ 預估本益比；上修寬度沒有歷史，"
                     f"不進條件{_ret_note(code, ret_tk)}）"}
    if proxy == "SP500":
        return {**base, "unavailable": "代理序列就是基準標普 500，條件無法區分"}
    p = p[p["date"] <= pd.Timestamp(cutoff)]
    sp_eps13 = asof(sp.set_index("date")["eps13"], p["date"], tol_days=7)
    x = forward_excess(fund, spy, p["date"], cutoff)
    ok = ~np.isnan(p["eps13"].values) & ~np.isnan(sp_eps13) & ~np.isnan(x)
    cond = p["eps13"].values > sp_eps13
    lag = _lag(p)
    st = summarize(p["date"].values[ok], x[ok], cond[ok], lag)
    now = None
    okn = ~np.isnan(p["eps13"].values) & ~np.isnan(sp_eps13)
    if okn.any():
        i = np.where(okn)[0][-1]
        now = {"as_of": pd.Timestamp(p["date"].values[i]).strftime("%Y-%m-%d"), "met": bool(cond[i]),
               "proxy_eps13_pct": _r(p["eps13"].values[i] * 100), "bench_eps13_pct": _r(sp_eps13[i] * 100)}
    return {**base, **st, "now": now}


def rule_c(code: str, proxy: str, panels: dict, fund, spy, cutoff, ret_tk: str) -> dict:
    import numpy as np
    import pandas as pd
    p = panels[proxy]
    p = p[p["date"] <= pd.Timestamp(cutoff)]
    x = forward_excess(fund, spy, p["date"], cutoff)
    ok = ~np.isnan(p["pct10"].values) & ~np.isnan(x)
    cond = p["pct10"].values <= 50
    lag = _lag(p)
    st = summarize(p["date"].values[ok], x[ok], cond[ok], lag)
    now = None
    okn = ~np.isnan(p["pct10"].values)
    if okn.any():
        i = np.where(okn)[0][-1]
        now = {"as_of": pd.Timestamp(p["date"].values[i]).strftime("%Y-%m-%d"), "met": bool(cond[i]),
               "pe": _r(p["pe"].values[i], 2), "pct10": _r(p["pct10"].values[i])}
    return {"condition": f"{SERIES_ZH[proxy]}預估本益比在過去十年的分位 ≤ 50",
            "proxy": f"{proxy} 預估本益比十年分位（PEG 沒有歷史，用本益比分位代替{_ret_note(code, ret_tk)}）",
            **st, "now": now}


def _finish(rid: str, body: dict) -> dict:
    out = {"id": rid, "rule": RULE_NAMES[rid], **body}
    if body.get("unavailable"):
        out.update(verdict=VERDICT_NA, reason=body.pop("unavailable"))
        out.pop("unavailable", None)
        return out
    v, why = verdict(out)
    out.update(verdict=v, reason=why)
    return out


def compute(code: str, registered_on: str, adj, close, *, currency: str = "USD", yf_ticker: str | None = None,
            long_pe_dir: Path = LONG_PE_DIR, price_source: str = "test") -> dict:
    """主計算（不抓網路）：adj／close 是寬表（欄＝代號），要含 SPY、攻方代號，以及代理序列的訊號代號。"""
    import pandas as pd
    if code == BENCH:
        raise BaseRateError(f"{BENCH} 是基準，不能當攻方")
    cutoff = pd.Timestamp(registered_on)
    adj = adj.loc[:cutoff]
    close = close.loc[:cutoff]
    if adj[BENCH].dropna().empty:
        raise BaseRateError(f"{BENCH} 沒有價格")
    cutoff = min(cutoff, adj[BENCH].dropna().index[-1])  # 只算到最後一個有收盤的日子，終點不能靠外推
    tk = yf_ticker or code
    ret_tk = RET_PROXY.get(code, tk)
    fund = fund_usd(adj, ret_tk, "USD" if ret_tk != tk else currency)
    spy = adj[BENCH].dropna()
    rules = [_finish("a", rule_a(code, fund_usd(adj, tk, currency), spy, cutoff))]
    proxy = PROXY.get(code)
    if proxy is None:
        na = {"condition": "", "proxy": "long_pe 沒有這檔的代理序列", "unavailable": "沒有代理序列"}
        rules.append(_finish("b", dict(na, condition="三個月上修高於基準（代理）")))
        rules.append(_finish("c", dict(na, condition="評價便宜（代理）")))
    else:
        panels = {n: pe_panel(n, close, long_pe_dir) for n in {proxy, "SP500"}}
        rules.append(_finish("b", rule_b(code, proxy, panels, fund, spy, cutoff, ret_tk)))
        rules.append(_finish("c", rule_c(code, proxy, panels, fund, spy, cutoff, ret_tk)))
    out = {"schema": "picks-base-rate-v1", "attack": code, "benchmark": BENCH, "registered_on": registered_on,
           "horizon_weeks": H, "price_source": price_source,
           "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "threshold": THRESHOLD, "rules": rules}
    out["brief"] = brief(out)
    return out


# ── 中文證據行 ───────────────────────────────────────────────────────────
def _p(v, sign=True):
    if v is None:
        return "—"
    s = f"{v:+.1f}" if sign else f"{v:.1f}"
    return s.replace("-", MINUS) + "%"


def _t(v):
    return "—" if v is None else f"{v:.1f}".replace("-", MINUS)


def brief(d: dict) -> str:
    th = d["threshold"]
    lines = [f"# 攻方理由的歷史基率（{d['attack']}，登記日 {d['registered_on']}，之後 {d['horizon_weeks']} 週對 {d['benchmark']}）",
             f"判定門檻：差 ≥ {th['min_diff_pp']:.0f} 個百分點且 t ≥ {th['min_nw_t']:.0f} 才算有預測力；"
             f"條件內不足 {th['min_cond_weeks']} 週或獨立事件不足 {th['min_episodes']} 次算無基率。門檻不是結論。"]
    for r in d["rules"]:
        head = f"({r['id']}) {r['rule']}"
        if r["verdict"] == VERDICT_NA and r.get("excess_cond_pct") is None:
            lines.append(f"{head}：無基率（{r['reason']}）。")
            continue
        s = (f"{head}：條件＝{r['condition']}。代理：{r['proxy']}。樣本 {r['sample_start']}～{r['sample_end']}，"
             f"{r['n_weeks']:,} 週，條件內 {r['n_cond_weeks']:,} 週、獨立 {r['episodes']} 次。"
             f"條件內之後 52 週平均超額 {_p(r['excess_cond_pct'])}，所有週 {_p(r['excess_all_pct'])}，"
             f"差 {_t(r['diff_pct'])} 個百分點；勝率 {_p(r['hit_cond_pct'], False)}，所有週 {_p(r['hit_all_pct'], False)}；"
             f"NW t {_t(r['nw_t'])}。判定：{r['verdict']}（{r['reason']}）。")
        now = r.get("now")
        if now:
            s += f"登記日前最近一期（{now['as_of']}）條件{'成立' if now['met'] else '不成立'}。"
        lines.append(s)
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────
def fund_info(code: str, cands_path: Path) -> tuple[str, str]:
    try:
        cands = json.loads(cands_path.read_text(encoding="utf-8"))
        for r in cands.get("funds", []):
            if r.get("key") == code:
                return r.get("yf_ticker") or code, r.get("currency") or "USD"
    except (OSError, ValueError):
        pass
    return code, "USD"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--attack", required=True, help="攻方代號（picks_candidates 的 key）")
    ap.add_argument("--registered-on", required=True, help="登記日 YYYY-MM-DD；只用這天（含）以前的資料")
    ap.add_argument("--out", default=None, help="輸出 JSON 路徑（省略就印到 stdout）")
    ap.add_argument("--brief", action="store_true", help="另把中文證據行印到 stderr")
    ap.add_argument("--price-source", default="auto", choices=["auto", "store", "yf"])
    ap.add_argument("--candidates", default=str(CANDIDATES_PATH))
    a = ap.parse_args(argv)
    try:
        datetime.date.fromisoformat(a.registered_on)
        tk, cur = fund_info(a.attack, Path(a.candidates))
        ret_tk = RET_PROXY.get(a.attack, tk)
        need = [BENCH, tk, ret_tk]
        if cur in FX_TICKER:
            need.append(FX_TICKER[cur])
        proxy = PROXY.get(a.attack)
        if proxy:
            need += [SERIES[proxy][1], SERIES["SP500"][1]]
        adj, close, src = load_prices(need, a.price_source, a.registered_on)
        out = compute(a.attack, a.registered_on, adj, close, currency=cur, yf_ticker=tk, price_source=src)
    except (BaseRateError, OSError, ValueError, KeyError) as e:
        print(f"[失敗] {e}", file=sys.stderr)
        return 2
    js = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(js + "\n", encoding="utf-8")
        print(f"[ok] {a.out}", file=sys.stderr)
    else:
        print(js)
    if a.brief:
        print(out["brief"], file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
