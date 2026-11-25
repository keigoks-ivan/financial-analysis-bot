#!/usr/bin/env python3
"""dd5 歷史倍數（零 LLM）：各會計年度年底的「過去十二個月」本益比、市銷率、EV／營收、股價／自由現金流。

- 股價：price_store 未還原股息收盤，取會計年度結束日當天或之前最近一個交易日。
- 每股盈餘：yfinance 年度稀釋 EPS；每股營收＝營收÷年度稀釋平均股數；每股自由現金流＝（營運現金流＋資本支出）÷稀釋平均股數。
- EV＝股價×年度稀釋平均股數＋（總債務－現金）；股數用平均股數是近似，不是年底流通股數。
- 現在的過去十二個月：最近四季加總（yfinance 季報），股數用最近一季稀釋平均股數，淨負債用最近一季資產負債表。
- EPS 為負、資料缺或股數缺的年度，該項留空並在 notes 註明。只做過去十二個月口徑；預估口徑只有現在一點（由呼叫端用共識 EPS 算）。
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path.home() / "v7-backtest"))

METRICS = [("pe", "本益比"), ("ps", "市銷率"), ("evs", "EV／營收"), ("pfcf", "股價／自由現金流")]


def _g(df, names, col):
    if df is None or col not in getattr(df, "columns", []):
        return None
    for n in ([names] if isinstance(names, str) else names):
        if n in df.index and pd.notna(df.loc[n, col]):
            return float(df.loc[n, col])
    return None


_FX_CACHE = {}


def currencies(yt):
    """回傳 (報表幣別, 報價幣別)；抓不到 info 就回 (None, None)，呼叫端當作同幣別。"""
    try:
        i = yt.info or {}
    except Exception:
        return None, None
    return i.get("financialCurrency"), i.get("currency")


def _per_usd(cur):
    """每 1 美元兌多少 cur 的日線（yfinance「XXX=X」）；USD 回 None（＝1）。"""
    if not cur or cur == "USD":
        return None
    if cur not in _FX_CACHE:
        from src.price_store import get_ohlcv
        _FX_CACHE[cur] = get_ohlcv(cur + "=X", start="2000-01-01")["close"].dropna()
    return _FX_CACHE[cur]


def fx_rate(fin, quote, end, how="end", window_days=365):
    """1 單位 fin 幣＝多少 quote 幣。how=end：end 當日或之前最近一個匯率；how=avg：(end－window_days, end] 的平均。
    回傳 (rate, 匯率日期字串)；同幣別回 (1.0, "")。抓不到丟例外。"""
    if not fin or not quote or fin == quote:
        return 1.0, ""
    sf, sq = _per_usd(fin), _per_usd(quote)
    idx = None
    for s_ in (sf, sq):
        if s_ is not None:
            idx = s_.index if idx is None else idx.union(s_.index)
    cf_ = sf.reindex(idx).ffill() if sf is not None else pd.Series(1.0, index=idx)
    cq_ = sq.reindex(idx).ffill() if sq is not None else pd.Series(1.0, index=idx)
    ser = (cq_ / cf_).dropna()  # quote 每 fin ＝（quote 每美元）÷（fin 每美元）
    end = pd.Timestamp(end)
    if how == "avg":
        w = ser[(ser.index > end - pd.Timedelta(days=window_days)) & (ser.index <= end)]
        if w.empty:
            raise ValueError("匯率 {0}→{1} 在 {2} 前沒有資料".format(fin, quote, end.date()))
        return float(w.mean()), "{0}～{1} 平均".format(w.index[0].date(), w.index[-1].date())
    w = ser[ser.index <= end]
    if w.empty:
        raise ValueError("匯率 {0}→{1} 在 {2} 前沒有資料".format(fin, quote, end.date()))
    return float(w.iloc[-1]), str(w.index[-1].date())


def _mult(price, eps=None, rev_ps=None, fcf_ps=None, net_debt=None, shares=None, rev=None):
    r = {"pe": None, "ps": None, "evs": None, "pfcf": None}
    n = []
    if eps is None:
        n.append("EPS 缺")
    elif eps <= 0:
        n.append("EPS 為負，本益比留空")
    else:
        r["pe"] = price / eps
    if rev_ps is None or rev_ps <= 0:
        n.append("營收或股數缺，市銷率留空")
    else:
        r["ps"] = price / rev_ps
    if shares and rev and net_debt is not None and rev > 0:
        r["evs"] = (price * shares + net_debt) / rev
    else:
        n.append("淨負債或股數缺，EV／營收留空")
    if fcf_ps is None or fcf_ps <= 0:
        n.append("自由現金流缺或為負，股價／自由現金流留空")
    else:
        r["pfcf"] = price / fcf_ps
    return r, n


def build(ticker, as_of=None, max_years=5, price_override=None):
    import yfinance as yf
    from src.price_store import get_ohlcv
    yt = yf.Ticker(ticker)
    inc, cf, bs = yt.income_stmt, yt.cashflow, yt.balance_sheet
    fin_cur, quote_cur = currencies(yt)
    cross = bool(fin_cur and quote_cur and fin_cur != quote_cur)
    fxinfo = {"fin": fin_cur, "quote": quote_cur, "cross": cross, "rows": [], "now": None, "errors": []}
    px = get_ohlcv(ticker, start="2000-01-01")["close"].dropna()
    rows = []
    for c in list(inc.columns)[:max_years]:
        sub = px[px.index <= c]
        if sub.empty:
            continue
        p = float(sub.iloc[-1])
        rev, sh = _g(inc, "Total Revenue", c), _g(inc, "Diluted Average Shares", c)
        eps = _g(inc, "Diluted EPS", c)
        ocf, capex = _g(cf, "Operating Cash Flow", c), _g(cf, "Capital Expenditure", c)
        debt, cash = _g(bs, "Total Debt", c), _g(bs, ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"], c)
        nd = debt - cash if debt is not None and cash is not None else None
        fa = fe = 1.0
        if cross:
            try:
                fa, _ = fx_rate(fin_cur, quote_cur, c, "avg")
                fe, fed = fx_rate(fin_cur, quote_cur, c, "end")
                fxinfo["rows"].append({"fy_end": str(c.date()), "avg": fa, "end": fe, "end_date": fed})
            except Exception as e:
                fxinfo["errors"].append("{0}：{1}".format(c.date(), str(e)[:60]))
                rows.append({"fy_end": str(c.date()), "price": p, "price_date": str(sub.index[-1].date()), "eps": None,
                             "pe": None, "ps": None, "evs": None, "pfcf": None, "notes": ["匯率取不到，整年倍數留空"]})
                continue
        # 流量項（EPS、營收、現金流）換成報價幣別用該年平均匯率，餘額項（淨負債）用年底匯率
        eps_q = eps * fa if eps is not None else None
        rev_q = rev * fa if rev else None
        m, notes = _mult(p, eps_q, rev_q / sh if rev_q and sh else None, (ocf + capex) * fa / sh if ocf is not None and capex is not None and sh else None,
                         nd * fe if nd is not None else None, sh, rev_q)
        rows.append({"fy_end": str(c.date()), "price": p, "price_date": str(sub.index[-1].date()), "eps": eps_q, "eps_fin": eps, **m, "notes": notes})
    dropped = [r["fy_end"] for r in rows if all(r[k] is None for k, _ in METRICS)]
    rows = [r for r in rows if r["fy_end"] not in dropped]
    rows.reverse()  # 舊到新
    now = None
    try:
        qi, qc, qb = yt.quarterly_income_stmt, yt.quarterly_cashflow, yt.quarterly_balance_sheet
        qcols = [c for c in qi.columns if _g(qi, "Total Revenue", c) is not None][:4]
        if len(qcols) == 4:
            eps = sum(_g(qi, "Diluted EPS", c) or 0 for c in qcols) if all(_g(qi, "Diluted EPS", c) is not None for c in qcols) else None
            rev = sum(_g(qi, "Total Revenue", c) for c in qcols)
            sh = _g(qi, "Diluted Average Shares", qcols[0])
            ocf = sum(_g(qc, "Operating Cash Flow", c) or 0 for c in qcols)
            capex = sum(_g(qc, "Capital Expenditure", c) or 0 for c in qcols)
            debt, cash = _g(qb, "Total Debt", qcols[0]), _g(qb, ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"], qcols[0])
            nd = debt - cash if debt is not None and cash is not None else None
            p = float(price_override) if price_override else float(px.iloc[-1])
            fa = fe = 1.0
            if cross:
                fa, _ = fx_rate(fin_cur, quote_cur, qcols[0], "avg")
                fe, fed = fx_rate(fin_cur, quote_cur, px.index[-1], "end")
                fxinfo["now"] = {"avg": fa, "avg_window_end": str(qcols[0].date()), "end": fe, "end_date": fed}
            eps_q = eps * fa if eps is not None else None
            rev_q = rev * fa
            m, notes = _mult(p, eps_q, rev_q / sh if sh else None, (ocf + capex) * fa / sh if sh else None,
                             nd * fe if nd is not None else None, sh, rev_q)
            now = {"price": p, "price_date": str(px.index[-1].date()), "ttm_end": str(qcols[0].date()), "eps": eps_q, "eps_fin": eps, **m, "notes": notes}
    except Exception as e:
        now = {"error": str(e)[:100]}
    stats = {}
    for k, _ in METRICS:
        v = [r[k] for r in rows if r.get(k) is not None]
        stats[k] = {"min": min(v), "med": statistics.median(v), "max": max(v), "n": len(v)} if v else None
    return {"ticker": ticker, "years": rows, "now": now, "stats": stats, "dropped_years": dropped, "fx": fxinfo}


if __name__ == "__main__":
    import json
    print(json.dumps(build(sys.argv[1]), ensure_ascii=False, indent=1, default=str))
