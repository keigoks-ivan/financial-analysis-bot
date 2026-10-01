"""Current pick list of the monthly-revenue momentum rule (V1a, docs/RevMom_Backtest_Spec.md §3).

python3 -m src.revmom_backtest.picks [YYYY-MM-DD]      # as-of date, default = last day in data/revmom
-> results/revmom/picks_<signal day>.{json,csv,md}

The list in force on the as-of date is the one from the latest signal day on or before it (first trading day
on/after the 11th of the month, using the previous month's revenue); it trades at the next trading day's open
and stays in force until the next signal day. Rules are imported from signals.py unchanged.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from . import data as D
from . import signals as S

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "revmom"
MARKET = {"twse": "上市", "tpex": "上櫃"}


def _names() -> pd.DataFrame:
    f = D.DATA / "names.parquet"
    return pd.read_parquet(f).set_index("code") if f.exists() else pd.DataFrame(columns=["name", "market"])


def row_for(pn, pre, names, code, sig, ex, asof, rank):
    last = pd.Period(sig, "M") - 1
    months = [last - 2, last - 1, last]
    rev = pn.rev[code] if code in pn.rev.columns else pd.Series(dtype=float)
    cur = [float(rev.get(m, np.nan)) for m in months]
    prev = [float(rev.get(m - 12, np.nan)) for m in months]
    r12 = rev.loc[:last].iloc[-12:]
    close, tri = float(pn.close.at[sig, code]), float(pre["tri"].at[sig, code])
    ma = {n: float(pre["ma"][n].at[sig, code]) * close / tri for n in (20, 60, 120)}    # TR-index MA at today's price scale
    o = float(pn.open.at[ex, code]) if ex is not None else np.nan
    ret = np.nan
    if ex is not None and o == o and o > 0:
        tri_ex, tri_now = pre["tri"].at[ex, code], pre["tri"].loc[:asof, code].dropna()
        if len(tri_now) and tri_ex == tri_ex:
            ret = float(tri_now.iloc[-1] / tri_ex * pn.close.at[ex, code] / o - 1)
    return {"rank": rank, "code": code, "name": str(names["name"].get(code, "")) if len(names) else "",
            "market": MARKET.get(str(names["market"].get(code, "")), "") if len(names) else "",
            "rev_ratio_3m_12m": float(r12.iloc[-3:].mean() / r12.mean()),
            "rev_months": [str(m) for m in months], "rev_3m_k": cur, "rev_3m_last_year_k": prev,
            "rev_3m_yoy": float(sum(cur) / sum(prev) - 1) if all(x == x for x in cur + prev) and sum(prev) > 0 else None,
            "signal_close": close, "ma20": ma[20], "ma60": ma[60], "ma120": ma[120],
            "ret5": float(pre["ret5"].at[sig, code]), "val20_ntd": float(pre["val20"].at[sig, code]),
            "buy_open": o if o == o else None, "ret_since_buy_to_asof": ret if ret == ret else None}


def _pct(x):
    return "—" if x is None else f"{x * 100:+.1f}%".replace("-", "−")


def _num(x):
    return "—" if x is None or x != x else (f"{x:,.2f}".rstrip("0").rstrip(".") if x < 1000 else f"{x:,.0f}")


def write_markdown(res, path):
    sig, ex, asof = res["signal_day"], res["buy_day"], res["as_of"]
    md, ad = sig[5:].replace("-", "/").lstrip("0"), (ex or "")[5:].replace("-", "/").lstrip("0")
    od = asof[5:].replace("-", "/").lstrip("0")
    P, A = res["picks"], res["alternates"]
    rets = [p["ret_since_buy_to_asof"] for p in P if p["ret_since_buy_to_asof"] is not None]
    lines = [f"# 台股月營收動能選股：{sig} 這一期的名單", "",
             "這份名單由回測規則（V1a）機械產生，不是投資建議。名單從買進日開盤生效，到下一個換股日前有效。", "",
             "## 這一期", "",
             f"- 判斷日：{sig} 收盤，用 {res['revenue_month_used']} 月營收（10 日前已公布）。",
             f"- 買進日：{ex} 開盤，10 檔各占 10%。",
             f"- 母體：上市櫃 4 位數普通股，不含創新板，近 20 個交易日平均成交金額 1,000 萬元以上，共 {res['n_universe']:,} 檔；"
             f"同時符合營收與股價條件的有 {res['n_pass']} 檔，取營收比值最高的 10 檔。",
             f"- 資料截止：{res['data_last_day']}（證交所、櫃買每日行情）；月營收到 {res['revenue_last_month']}。", "",
             f"| 名次 | 代號 | 名稱 | 市場 | 營收比值 | 近 3 月營收（億元） | 與去年同期比 | {md} 收盤 | {ad} 開盤 | 至 {od} 報酬 |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for p in P:
        lines.append(f"| {p['rank']} | {p['code']} | {p['name']} | {p['market']} | {p['rev_ratio_3m_12m']:.2f} | "
                     f"{sum(p['rev_3m_k']) / 1e5:,.1f} | {_pct(p['rev_3m_yoy'])} | {_num(p['signal_close'])} | "
                     f"{_num(p['buy_open'])} | {_pct(p['ret_since_buy_to_asof'])} |")
    lines += ["",
              f"- 營收比值＝近 3 個月平均營收 ÷ 近 12 個月平均營收；近 3 個月是 {P[0]['rev_months'][0]}～{P[0]['rev_months'][-1]}。",
              "- 股價條件全部用還原權息價格：把除權息加回去後，股價要高於 20、60、120 日平均，且比 5 個交易日前高。"
              "CSV 裡的 ma20／ma60／ma120 是還原權息均線換算到判斷日的價格水準。",
              f"- 至 {od} 報酬：從買進日開盤價算到 {od} 收盤，含除權息，不含手續費與稅。"
              + (f"10 檔平均 {_pct(sum(rets) / len(rets))}。" if rets else ""),
              "- 創新板股票（名稱以「-創」結尾）不在母體裡：一般投資人不一定能買。", "",
              "## 備取（同樣通過全部條件，排第 11～20 名）", "",
              "前 10 名有股票買不到時，規則本身不遞補；這份清單只供參考。", "",
              f"| 名次 | 代號 | 名稱 | 市場 | 營收比值 | 近 3 月營收與去年同期比 | {md} 收盤 |", "|---|---|---|---|---|---|---|"]
    for a in A:
        lines.append(f"| {a['rank']} | {a['code']} | {a['name']} | {a['market']} | {a['rev_ratio_3m_12m']:.2f} | "
                     f"{_pct(a['rev_3m_yoy'])} | {_num(a['signal_close'])} |")
    lines += ["", "## 下一次換股", "", f"- {res['next_signal']}；{res['next_list']}。", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main(asof=None):
    pn = D.load("2007-01-01")
    pre = S.precompute(pn)
    asof = pd.Timestamp(asof) if asof else pn.dates[-1]
    asof = pn.dates[pn.dates <= asof][-1]
    sig = S.signal_days(pn.dates, asof - pd.Timedelta(days=62), asof)[-1]
    i = pn.dates.searchsorted(sig, side="right")
    ex = pn.dates[i] if i < len(pn.dates) else None
    top20, diag = S.select(pn, pre, sig, "V1a", n_pick=20)
    top10, _ = S.select(pn, pre, sig, "V1a")
    assert top20[:10] == top10, "top-10 differs between n_pick=10 and n_pick=20"
    names = _names()
    picks = [row_for(pn, pre, names, c, sig, ex, asof, k + 1) for k, c in enumerate(top10)]
    alts = [row_for(pn, pre, names, c, sig, ex, asof, k + 11) for k, c in enumerate(top20[10:])]
    nxt_month = (pd.Period(sig, "M") + 1)
    res = {"rule": "V1a", "as_of": str(asof.date()), "data_last_day": str(pn.dates[-1].date()),
           "revenue_last_month": str(pn.rev.index[-1]), "signal_day": str(sig.date()),
           "revenue_month_used": str(pd.Period(sig, "M") - 1), "buy_day": str(ex.date()) if ex is not None else None,
           "weight_each": 0.10, "n_universe": diag["n_universe"], "n_pass": diag["n_pass"],
           "next_signal": f"{nxt_month} 月第一個 11 日以後的交易日（用 {pd.Period(sig, 'M')} 營收）",
           "next_list": f"待 {pd.Period(sig, 'M')} 營收公布後" if pn.rev.index[-1] < pd.Period(sig, "M") else "可計算",
           "picks": picks, "alternates": alts}
    OUT.mkdir(parents=True, exist_ok=True)
    stem = OUT / f"picks_{sig.date()}"
    stem.with_suffix(".json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    pd.DataFrame([dict(p, kind="picks") for p in picks] + [dict(a, kind="alternate") for a in alts]).to_csv(
        stem.with_suffix(".csv"), index=False)
    write_markdown(res, stem.with_suffix(".md"))
    print(json.dumps({k: v for k, v in res.items() if k not in ("picks", "alternates")}, ensure_ascii=False))
    for p in picks + alts:
        r = p["ret_since_buy_to_asof"]
        print(p["rank"], p["code"], p["name"], p["market"], round(p["rev_ratio_3m_12m"], 3), p["buy_open"],
              None if r is None else round(r, 4))
    return res


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
